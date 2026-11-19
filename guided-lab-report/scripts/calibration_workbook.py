"""Optional synthetic calibration example using openpyxl.

1. python scripts/calibration_workbook.py build /path/to/input.json calibration.xlsx
2. Open calibration.xlsx in Excel or a compatible calculation engine,
   recalculate all formulas, then save and close the workbook.
3. python scripts/calibration_workbook.py export calibration.xlsx calibration-results.json

Input concentrations are in mg/L. Absorbance is dimensionless. The example
uses three complete replicates per standard and unknown, unweighted OLS with
an intercept, and no exclusions. Enter a confirmed numeric dilution factor in
Processing!I10, or leave 1 for an undiluted sample. The calibration limits
apply to the measured solution. A fit accepted under the supplied criteria and
an in-range result are both required to report the original-sample estimate.
If the input has no fit_criteria, the worksheet marks the fit unverified.
For real data, adapt the model and
criteria to the agreed analysis plan. openpyxl writes formulas but cannot
evaluate them.
"""

import argparse
import json
import math
import statistics
from pathlib import Path

FIRST_STANDARD = 5
IN_RANGE = "In calibration range"
OUT_OF_RANGE = "Out of calibration range"
DILUTION_CELL = "I10"
RAW_STANDARD_HEADERS = ("Standard ID", "Concentration (mg/L)", "Absorbance 1",
                        "Absorbance 2", "Absorbance 3")
RAW_UNKNOWN_HEADERS = ("Unknown ID", "Absorbance 1", "Absorbance 2", "Absorbance 3")
REFERENCE_LABEL = "Original-sample reference (mg/L)"
CRITERIA_LABELS = ("Minimum R² (illustrative criterion)",
                   "Maximum absolute residual (illustrative)")
NUMBER_DISPLAY = "0.####"
PERCENT_DISPLAY = "0.####%"
# Native chart labels do not share worksheet conditional formatting. Special
# format sections keep the usual exact R² endpoints free of a decimal point.
TRENDLINE_DISPLAY = "[=0]0;[=1]0;0.####"
AXIS_TITLES = ("Concentration (mg/L)", "Absorbance (dimensionless)")


def number(value, label):
    if type(value) not in (int, float) or not math.isfinite(value):
        raise ValueError(f"{label} must be a finite number")
    return value


def measurements(values):
    if len(values) != 3:
        raise ValueError("the example requires three absorbance readings per sample")
    return [number(value, "absorbance") for value in values]


def text_id(value):
    if not isinstance(value, str) or not value.strip():
        raise ValueError("sample ID must be nonempty text")
    return value


def dilution_input(value):
    value = number(value, f"Processing!{DILUTION_CELL} dilution factor")
    if value <= 0:
        raise ValueError(f"Processing!{DILUTION_CELL} dilution factor must be positive")
    return value


def reference_input(value):
    value = number(value, "original-sample reference concentration")
    if value < 0:
        raise ValueError("the original-sample reference concentration must be nonnegative")
    return value


def fit_criteria_input(criteria):
    if criteria is None:
        return None
    keys = {"minimum_r_squared", "maximum_absolute_residual"}
    if not isinstance(criteria, dict) or set(criteria) != keys:
        raise ValueError("supply both fit criteria or leave both unspecified")
    minimum = number(criteria["minimum_r_squared"], "minimum R²")
    maximum = number(criteria["maximum_absolute_residual"], "maximum absolute residual")
    if not 0 <= minimum <= 1 or maximum < 0:
        raise ValueError("minimum R² must be within [0, 1] and maximum absolute residual nonnegative")
    return {"minimum_r_squared": minimum, "maximum_absolute_residual": maximum}


def standard_formulas(row):
    return (
        f"=Raw!A{row}", f"=Raw!B{row}", f"=AVERAGE(Raw!C{row}:E{row})",
        f"=STDEV(Raw!C{row}:E{row})", f"=$I$5*B{row}+$I$6", f"=C{row}-E{row}",
    )


def metric_formulas(last_row):
    x_range = f"B{FIRST_STANDARD}:B{last_row}"
    y_range = f"C{FIRST_STANDARD}:C{last_row}"
    lower, upper = f"MIN({x_range})", f"MAX({x_range})"
    # Relative padding addresses numerical representation at exact range endpoints.
    margin = f"1E-12*MAX(1,ABS({lower}),ABS({upper}))"
    return {
        "I5": ("Slope (L/mg)", f"=SLOPE({y_range},{x_range})", NUMBER_DISPLAY),
        "I6": ("Intercept", f"=INTERCEPT({y_range},{x_range})", NUMBER_DISPLAY),
        "I7": ("R²", f"=RSQ({y_range},{x_range})", NUMBER_DISPLAY),
        "I8": ("Unknown mean absorbance", "=AVERAGE(Raw!H5:J5)", NUMBER_DISPLAY),
        "I9": ("Measured-solution estimate (mg/L)", '=IF(I5=0,"",(I8-I6)/I5)', NUMBER_DISPLAY),
        "I11": ("Measured-solution status",
                '=IF(NOT(ISNUMBER(I9)),"Calibration unavailable",'
                f'IF(AND(I9>={lower}-{margin},I9<={upper}+{margin}),'
                f'"{IN_RANGE}","{OUT_OF_RANGE}"))', "General"),
        "I12": ("Original-sample result (mg/L)",
                f'=IF(AND(I11="{IN_RANGE}",I16="accepted",ISNUMBER(I10),I10>0),I9*I10,"")',
                NUMBER_DISPLAY),
        "I13": ("Original-sample reference (mg/L)", "=Raw!H7", NUMBER_DISPLAY),
        "I14": ("Original-sample difference (mg/L)", '=IF(ISNUMBER(I12),I12-I13,"")',
                NUMBER_DISPLAY),
        "I15": ("Relative original-sample difference",
                '=IF(AND(ISNUMBER(I14),I13<>0),I14/I13,"")', PERCENT_DISPLAY),
        "I16": ("Fit status (see Raw criteria)",
                '=IF(COUNT(Raw!H10:H11)<>2,"unverified",'
                'IF(AND(I7>=Raw!H10-1E-12*MAX(1,ABS(Raw!H10)),'
                'I17<=Raw!H11+1E-12*MAX(1,ABS(Raw!H11))),"accepted","rejected"))', "General"),
        "I17": ("Maximum absolute residual",
                f"=MAX(ABS(MIN(F{FIRST_STANDARD}:F{last_row})),"
                f"ABS(MAX(F{FIRST_STANDARD}:F{last_row})))", NUMBER_DISPLAY),
    }


def workbook_from_fixture(input_path, output_path):
    from openpyxl import Workbook
    from openpyxl.chart import Reference, ScatterChart, Series
    from openpyxl.chart.data_source import NumFmt
    from openpyxl.chart.trendline import Trendline, TrendlineLabel
    from openpyxl.formatting.rule import Rule
    from openpyxl.styles import Alignment, Font, PatternFill
    from openpyxl.styles.differential import DifferentialStyle
    from openpyxl.styles.numbers import NumberFormat
    from openpyxl.workbook.properties import CalcProperties
    from openpyxl.worksheet.datavalidation import DataValidation

    fixture = json.loads(input_path.read_text(encoding="utf-8"))
    standards = [
        (text_id(row["id"]), number(row["concentration"], "concentration"),
         *measurements(row["absorbances"]))
        for row in fixture["standards"]
    ]
    concentrations = [row[1] for row in standards]
    if len(standards) < 3 or len(set(concentrations)) != len(standards):
        raise ValueError("supply at least three distinct standard concentrations")
    unknown = fixture["unknown"]
    unknown_values = (text_id(unknown["id"]), *measurements(unknown["absorbances"]))
    reference = reference_input(fixture["reference_concentration"])
    criteria = fit_criteria_input(fixture.get("fit_criteria"))

    workbook = Workbook()
    raw = workbook.active
    raw.title = "Raw"
    processing = workbook.create_sheet("Processing")
    workbook.calculation = CalcProperties(calcMode="auto", fullCalcOnLoad=True)
    workbook.active = processing

    def setup(sheet, title, subtitle, widths):
        sheet["A1"] = title
        sheet["A1"].font = Font(size=16, bold=True, color="27435E")
        sheet["A2"] = subtitle
        sheet["A2"].font = Font(italic=True, color="4A5662")
        sheet.sheet_view.showGridLines = False
        sheet.freeze_panes = "C5"
        for column, width in widths.items():
            sheet.column_dimensions[column].width = width

    def header(sheet, row, first_column, labels):
        for column, label in enumerate(labels, first_column):
            cell = sheet.cell(row, column, label)
            cell.fill = PatternFill("solid", fgColor="27435E")
            cell.font = Font(bold=True, color="FFFFFF")
            cell.alignment = Alignment(vertical="center", wrap_text=True)
        sheet.row_dimensions[row].height = 28

    def write_inputs(sheet, row, first_column, values):
        for column, value in enumerate(values, first_column):
            cell = sheet.cell(row, column, value)
            if isinstance(value, str):
                cell.data_type = "s"

    setup(raw, "Simulated calibration inputs",
          "Keep original readings here. Dimensions: concentration in mg/L, absorbance dimensionless.",
          {"A": 17, "B": 22, "C": 16, "D": 16, "E": 16, "G": 25,
           "H": 17, "I": 17, "J": 17})
    header(raw, 4, 1, RAW_STANDARD_HEADERS)
    header(raw, 4, 7, RAW_UNKNOWN_HEADERS)
    for row, values in enumerate(standards, FIRST_STANDARD):
        write_inputs(raw, row, 1, values)
    write_inputs(raw, 5, 7, unknown_values)
    raw["G7"] = REFERENCE_LABEL
    raw["H7"] = reference
    raw["G8"] = "Assigned independently for the original sample in this simulation"
    for row, label in enumerate(CRITERIA_LABELS, 10):
        raw.cell(row, 7, label)
    raw.column_dimensions["G"].width = 41
    if criteria is not None:
        raw["H10"] = criteria["minimum_r_squared"]
        raw["H11"] = criteria["maximum_absolute_residual"]
    raw["G12"] = "Use agreed method-specific criteria for an actual experiment."

    setup(processing, "Linear calibration",
          "Simulated data. Open in an Excel-compatible engine and recalculate before exporting results.",
          {"A": 16, "B": 22, "C": 20, "D": 15, "E": 19, "F": 16, "G": 4,
           "H": 38, "I": 27})
    header(processing, 4, 1, ("Standard ID", "Concentration (mg/L)", "Mean absorbance",
                              "Sample SD", "Fitted absorbance", "Residual"))
    header(processing, 4, 8, ("Fit and comparison", "Value"))
    last_row = FIRST_STANDARD + len(standards) - 1
    for row in range(FIRST_STANDARD, last_row + 1):
        for column, formula in enumerate(standard_formulas(row), 1):
            cell = processing.cell(row, column, formula)
            if column > 1:
                cell.number_format = NUMBER_DISPLAY
    for address, (label, formula, number_format) in metric_formulas(last_row).items():
        processing.cell(processing[address].row, 8, label)
        processing[address] = formula
        processing[address].number_format = number_format
    processing["H10"] = "Confirmed dilution factor (editable)"
    processing[DILUTION_CELL] = 1
    processing[DILUTION_CELL].number_format = NUMBER_DISPLAY
    processing[DILUTION_CELL].fill = PatternFill("solid", fgColor="DDEBF7")
    factor_validation = DataValidation(
        type="decimal", operator="greaterThan", formula1=0, allow_blank=False,
        showErrorMessage=True, errorStyle="stop",
        errorTitle="Invalid dilution factor", error="Enter a number greater than zero.",
    )
    processing.add_data_validation(factor_validation)
    factor_validation.add(DILUTION_CELL)
    processing["H19"] = "Use total volume ÷ aliquot volume only for a confirmed dilution."
    processing["H20"] = "Report requires an accepted fit and an in-range measured solution."
    processing["H21"] = "The display rounds to four decimals; the workbook and export keep full precision."

    def report_display(target, first, percentage=False):
        # Excel optional decimals still show a separator for whole numbers.
        scale = f"{first}*100" if percentage else first
        suffix = "%" if percentage else ""
        for condition, code, fmt_id in (
            (f"AND(ISNUMBER({first}),{first}<>0,ROUND({scale},4)=0)",
             f'[>0]"<0.0001{suffix}";[<0]">-0.0001{suffix}";0{suffix}', 168),
            (f"AND(ISNUMBER({first}),ROUND({scale},4)=ROUND({scale},0))", f"0{suffix}", 169),
        ):
            formatting = DifferentialStyle(numFmt=NumberFormat(numFmtId=fmt_id, formatCode=code))
            processing.conditional_formatting.add(
                target, Rule(type="expression", dxf=formatting,
                             stopIfTrue=True, formula=[condition])
            )

    report_display(f"B{FIRST_STANDARD}:F{last_row}", f"B{FIRST_STANDARD}")
    report_display("I5:I14", "I5")
    report_display("I15", "I15", percentage=True)
    report_display("I17", "I17")

    chart = ScatterChart()
    chart.title = "Calibration of the simulated standards"
    chart.x_axis.title, chart.y_axis.title = AXIS_TITLES
    chart.style = 2
    chart.scatterStyle = "marker"
    chart.legend = None
    chart.width = 18
    chart.height = 9
    chart.roundedCorners = False
    chart.title.overlay = False
    chart.x_axis.title.overlay = False
    chart.y_axis.title.overlay = False
    chart.x_axis.delete = False
    chart.y_axis.delete = False
    chart.x_axis.axPos = "b"
    chart.y_axis.axPos = "l"
    chart.x_axis.numFmt = "0.0"
    chart.y_axis.numFmt = "0.0"
    chart.x_axis.majorGridlines = None
    x_values = Reference(processing, min_col=2, min_row=FIRST_STANDARD, max_row=last_row)
    y_values = Reference(processing, min_col=3, min_row=FIRST_STANDARD, max_row=last_row)
    series = Series(y_values, x_values, title="Standard mean")
    series.marker.symbol = "circle"
    series.marker.size = 6
    series.graphicalProperties.line.noFill = True
    series.trendline = Trendline(
        trendlineType="linear", dispEq=True, dispRSqr=True,
        trendlineLbl=TrendlineLabel(numFmt=NumFmt(formatCode=TRENDLINE_DISPLAY,
                                                 sourceLinked=False)),
    )
    chart.series.append(series)
    processing.add_chart(chart, "H23")
    workbook.save(output_path)


def check_calculated(value, expected, label):
    if type(value) not in (int, float) or not math.isclose(
        value, expected, rel_tol=1e-9, abs_tol=1e-11
    ):
        raise ValueError(f"{label} is missing or inconsistent. Recalculate and save in Excel "
                         "or a compatible calculation engine before export.")
    return value


def check_formula(sheet, address, expected):
    cell = sheet[address]

    def normalized(formula):
        # Spreadsheet engines may quote sheet names or expand scientific notation.
        return (formula.replace(" ", "").upper().replace("'RAW'!", "RAW!")
                .replace("0.000000000001*", "1E-12*"))

    if cell.data_type != "f" or not isinstance(cell.value, str) or (
        normalized(cell.value) != normalized(expected)
    ):
        raise ValueError(f"Processing!{address} must retain its generated formula. "
                         "Restore the formula or rebuild before recalculating and exporting.")


def check_withheld(processing, address):
    if processing[address].value not in (None, ""):
        raise ValueError(f"Processing!{address} should be withheld. Recalculate and save "
                         "in Excel or a compatible calculation engine before export.")


def raw_literal(cell):
    value = cell.value
    if cell.data_type not in ("s", "inlineStr", "n") or (
        value is not None and type(value) not in (str, int, float)
    ):
        raise ValueError(f"Raw!{cell.coordinate} must contain a literal reading or label.")
    return value


def read_raw_inputs(raw):
    for cells, expected in (
        (raw["A4:E4"][0], RAW_STANDARD_HEADERS),
        (raw["G4:J4"][0], RAW_UNKNOWN_HEADERS),
        ((raw["G7"],), (REFERENCE_LABEL,)),
        ((raw["G10"], raw["G11"]), CRITERIA_LABELS),
    ):
        if tuple(raw_literal(cell) for cell in cells) != expected:
            raise ValueError("Raw sheet labels do not match the generated workbook.")
    rows = []
    for row, cells in enumerate(
        raw.iter_rows(min_row=FIRST_STANDARD, max_col=5), FIRST_STANDARD
    ):
        values = tuple(raw_literal(cell) for cell in cells)
        if any(value is not None for value in values):
            if row != FIRST_STANDARD + len(rows):
                raise ValueError("The Raw calibration standards must occupy consecutive rows.")
            text_id(values[0])
            rows.append((row, values))
    text_id(raw_literal(raw["G5"]))
    readings = measurements([raw_literal(raw[f"{col}5"]) for col in "HIJ"])
    reference = reference_input(raw_literal(raw["H7"]))
    minimum, maximum = (raw_literal(raw[address]) for address in ("H10", "H11"))
    criteria = None if minimum is None and maximum is None else fit_criteria_input({
        "minimum_r_squared": minimum,
        "maximum_absolute_residual": maximum,
    })
    return rows, readings, reference, criteria


def check_chart(processing, last_row):
    from openpyxl.chart import ScatterChart
    from openpyxl.utils.cell import column_index_from_string

    # openpyxl exposes loaded worksheet charts through _charts. They are read
    # through the saved sheet's drawing relationships, not inferred from cells.
    charts = processing._charts
    if len(charts) != 1 or not isinstance(charts[0], ScatterChart):
        raise ValueError("Processing must retain its native XY scatter chart.")
    chart = charts[0]
    if len(chart.series) != 1:
        raise ValueError("The Processing scatter chart must contain one standard series.")
    series = chart.series[0]

    def address(source):
        ref = getattr(source, "numRef", None)
        formula = getattr(ref, "f", None) or ""
        return formula.replace("'", "").replace("$", "").upper()

    expected_x = f"PROCESSING!B{FIRST_STANDARD}:B{last_row}"
    expected_y = f"PROCESSING!C{FIRST_STANDARD}:C{last_row}"
    if (address(series.xVal), address(series.yVal)) != (expected_x, expected_y):
        raise ValueError("The Processing scatter chart must reference the standard concentrations "
                         "and formula-backed mean absorbance in columns B and C.")
    if processing.sheet_state != "visible" or any(
        getattr(processing.row_dimensions.get(row), "hidden", False)
        for row in range(FIRST_STANDARD, last_row + 1)
    ):
        raise ValueError("The Processing chart and its referenced standards must remain visible.")
    for dimension in processing.column_dimensions.values():
        if dimension.hidden:
            lower = dimension.min or column_index_from_string(dimension.index)
            upper = dimension.max or lower
            if lower <= 3 and upper >= 2:
                raise ValueError("The Processing chart's source columns B and C must remain visible.")
    trendline = series.trendline
    if not trendline or trendline.trendlineType != "linear" or trendline.intercept is not None or (
        trendline.dispEq is not True or trendline.dispRSqr is not True
    ):
        raise ValueError("The chart must keep its unconstrained linear trendline, equation and R².")
    for axis, expected_title in zip((chart.x_axis, chart.y_axis), AXIS_TITLES):
        title = getattr(axis, "title", None)
        rich = getattr(getattr(title, "tx", None), "rich", None)
        actual_title = "".join(
            run.t for paragraph in getattr(rich, "p", ())
            for run in (paragraph.r or ()) if run.t
        )
        if axis is None or axis.delete or actual_title != expected_title:
            raise ValueError("Both chart axes must remain visible with their original quantity "
                             "and unit titles.")


def results_from_workbook(input_path):
    from openpyxl import load_workbook

    workbook = load_workbook(input_path, read_only=True, data_only=True)
    try:
        formula_book = load_workbook(input_path, data_only=False)
        try:
            return read_cached_results(formula_book["Raw"], workbook["Processing"],
                                       formula_book["Processing"])
        finally:
            formula_book.close()
    finally:
        workbook.close()


def read_cached_results(raw, processing, formula_sheet):
    rows, readings, reference, criteria = read_raw_inputs(raw)
    if len(rows) < 3:
        raise ValueError("expected at least three standards in Raw")
    check_chart(formula_sheet, rows[-1][0])
    for address, (_, expected_formula, _) in metric_formulas(rows[-1][0]).items():
        check_formula(formula_sheet, address, expected_formula)
    for row, _ in rows:
        for column, expected_formula in zip("ABCDEF", standard_formulas(row)):
            check_formula(formula_sheet, f"{column}{row}", expected_formula)
    factor = dilution_input(formula_sheet[DILUTION_CELL].value)
    check_calculated(processing[DILUTION_CELL].value, factor, f"Processing!{DILUTION_CELL}")
    x = [number(values[1], f"Raw!B{row}") for row, values in rows]
    replicates = [measurements(values[2:]) for _, values in rows]
    y = [statistics.mean(values) for values in replicates]
    mx, my = statistics.mean(x), statistics.mean(y)
    sxx = math.fsum((c - mx) ** 2 for c in x)
    syy = math.fsum((a - my) ** 2 for a in y)
    if sxx == 0 or syy == 0:
        raise ValueError("the calibration needs variation in concentration and absorbance")
    slope = math.fsum((c - mx) * (a - my) for c, a in zip(x, y)) / sxx
    if slope == 0:
        raise ValueError("a zero calibration slope cannot estimate an unknown")
    intercept = my - slope * mx
    fitted = [slope * c + intercept for c in x]
    residuals = [a - p for a, p in zip(y, fitted)]
    maximum_residual = max(abs(value) for value in residuals)
    r_squared = 1 - math.fsum(value ** 2 for value in residuals) / syy
    unknown_a = statistics.mean(readings)
    measurement = (unknown_a - intercept) / slope
    lower, upper = min(x), max(x)
    margin = 1e-12 * max(1, abs(lower), abs(upper))
    in_range = lower - margin <= measurement <= upper + margin
    status = IN_RANGE if in_range else OUT_OF_RANGE
    if processing["I11"].value != status:
        raise ValueError("Processing!I11 is missing or inconsistent. Recalculate and save "
                         "in Excel or a compatible calculation engine before export.")
    check_calculated(processing["I17"].value, maximum_residual, "Processing!I17")
    if criteria is None:
        fit_status = "unverified"
    else:
        minimum = criteria["minimum_r_squared"]
        maximum = criteria["maximum_absolute_residual"]
        acceptable = (r_squared >= minimum - 1e-12 * max(1, abs(minimum))
                      and maximum_residual <= maximum + 1e-12 * max(1, abs(maximum)))
        fit_status = "accepted" if acceptable else "rejected"
    if processing["I16"].value != fit_status:
        raise ValueError("Processing!I16 fit status is missing or inconsistent. Recalculate "
                         "and save in Excel or a compatible calculation engine before export.")
    checks = {
        "I5": ("slope", slope),
        "I6": ("intercept", intercept),
        "I7": ("r_squared", r_squared),
        "I8": ("unknown_absorbance", unknown_a),
        "I9": ("measurement_concentration", measurement),
        "I13": ("reference_concentration", reference),
    }
    result = {
        key: check_calculated(processing[address].value, expected, f"Processing!{address}")
        for address, (key, expected) in checks.items()
    }
    result["dilution_factor"] = factor
    result["in_calibration_range"] = in_range
    result["fit_criteria"] = criteria
    result["fit_status"] = fit_status
    if in_range and fit_status == "accepted":
        original = measurement * factor
        difference = original - reference
        result["unknown_concentration"] = check_calculated(
            processing["I12"].value, original, "Processing!I12"
        )
        check_calculated(processing["I14"].value, difference, "Processing!I14")
        if reference:
            check_calculated(processing["I15"].value, difference / reference, "Processing!I15")
        else:
            check_withheld(processing, "I15")
    else:
        for address in ("I12", "I14", "I15"):
            check_withheld(processing, address)
        result["unknown_concentration"] = None
    result["standards"] = []
    result["fitted"] = []
    result["sample_sd"] = []
    for index, (row, inputs) in enumerate(rows):
        if processing.cell(row, 1).value != text_id(inputs[0]):
            raise ValueError(f"Processing!A{row} is missing or inconsistent. "
                             "Recalculate and save the workbook before export.")
        saved = [
            check_calculated(processing.cell(row, col).value, expected, f"Processing row {row}")
            for col, expected in enumerate(
                (x[index], y[index], statistics.stdev(replicates[index]), fitted[index],
                 y[index] - fitted[index]), 2)
        ]
        result["standards"].append(saved[:2])
        result["sample_sd"].append(saved[2])
        result["fitted"].append(saved[3])
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    for name, input_help, output_help in (
        ("build", "synthetic fixture JSON", "formula workbook .xlsx"),
        ("export", "recalculated workbook .xlsx", "verified readback JSON"),
    ):
        command = commands.add_parser(name)
        command.add_argument("input", type=Path, help=input_help)
        command.add_argument("output", type=Path, help=output_help)
    args = parser.parse_args()
    if args.input.resolve() == args.output.resolve():
        parser.error("input and output must be different files")
    try:
        if args.command == "build":
            workbook_from_fixture(args.input, args.output)
        else:
            args.output.write_text(
                json.dumps(results_from_workbook(args.input), indent=2, allow_nan=False) + "\n",
                encoding="utf-8",
            )
    except ModuleNotFoundError as error:
        parser.exit(2, f"Optional workbook example dependency missing: {error.name}\n")
    except (ValueError, TypeError, KeyError, OSError) as error:
        parser.exit(2, f"Calibration example: {error}\n")


if __name__ == "__main__":
    main()
