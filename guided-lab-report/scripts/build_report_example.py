"""Build a synthetic calibration Results example from one workbook JSON export.

Usage: python scripts/build_report_example.py readings.json results.docx
Requires Python 3.10+, Pillow 10.1+, and python-docx. The embedded figure is
rendered directly from the same validated data as the Word equation and table.
"""

from __future__ import annotations

import argparse
from decimal import Decimal, localcontext
from pathlib import Path

from docx import Document
from docx.enum.table import WD_CELL_VERTICAL_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Inches, Pt

from display_numbers import DISPLAY_BOUND, bounded, fixed, tiny
from make_figure import close, load_calibration, render_figure
from word_math import equation, fraction, math_text, subscript


def concentration_text(value):
    if tiny(value):
        span = f"0 and {DISPLAY_BOUND}" if value > 0 else f"−{DISPLAY_BOUND} and 0"
        return f"between {span} mg/L"
    return f"{fixed(value)} mg/L"


def display_decimal(value):
    return Decimal(fixed(value).replace("−", "-"))


def reference_comparison(concentration, reference):
    difference = concentration - reference
    reference_phrase = f"the assigned synthetic original sample reference ({concentration_text(reference)})"
    if difference == 0:
        return f"The estimate matches {reference_phrase}."
    if tiny(difference):
        direction = "above" if difference > 0 else "below"
        text = f"The estimate was {direction} {reference_phrase} by less than {DISPLAY_BOUND} mg/L"
    else:
        text = f"The estimate differed from {reference_phrase} by {fixed(difference, signed=True)} mg/L"
    shown_sample, shown_reference = map(display_decimal, (concentration, reference))
    shown_difference = shown_sample - shown_reference
    rounding_note = tiny(difference) or fixed(float(shown_difference)) != fixed(difference)
    if reference != 0:
        percent = 100 * difference / reference
        if tiny(percent):
            direction = "positive" if percent > 0 else "negative"
            text += f" (a {direction} relative deviation smaller than {DISPLAY_BOUND}% in magnitude)"
        else:
            text += f" ({fixed(percent, signed=True)}% relative to the reference)"
        rounding_note = rounding_note or shown_reference == 0 or (
            fixed(float(100 * shown_difference / shown_reference)) != fixed(percent)
        )
    text += "."
    if rounding_note:
        text += " The deviations were computed before rounding."
    return text


def comparison(data):
    reference = data.reference_concentration
    concentration = data.unknown_concentration
    sentences = []
    if reference is not None and concentration is not None:
        sentences.append(reference_comparison(concentration, reference))
    sds = [(x, sd) for (x, _), sd in zip(data.standards, data.sample_sd) if sd is not None]
    if len(sds) >= 2:
        ordered = sorted(sds, key=lambda pair: pair[1])
        max_x, max_sd = ordered[-1]
        if not close(ordered[0][1], max_sd):
            rest_min, rest_max = ordered[0][1], ordered[-2][1]
            if close(rest_min, rest_max):
                rest = bounded(rest_min)
            else:
                rest = f"{bounded(rest_min)} to {bounded(rest_max)}"
            sentences.append(
                f"The standard at {concentration_text(max_x)} had a sample SD of "
                f"{bounded(max_sd)}, compared with {rest} at the other levels."
            )
    if reference is not None and concentration is not None and concentration != reference:
        sentences.append("The cause of the discrepancy remains unresolved.")
    return " ".join(sentences)


def substitution_operands(data):
    """Keep enough raw absorbance precision without extending displayed coefficients."""
    if any(tiny(value) for value in (data.measurement_concentration, data.slope, data.intercept)):
        return None
    printed_result = display_decimal(data.measurement_concentration)
    half_last_place = Decimal("0.00005")
    b = fixed(abs(data.intercept))
    m = fixed(data.slope)
    with localcontext() as context:
        context.prec = 36
        for digits in range(4, 18):
            a = f"{data.unknown_absorbance:.{digits}g}"
            intercept = Decimal(b) if data.intercept >= 0 else -Decimal(b)
            inverse = (Decimal(a) - intercept) / Decimal(m.replace("−", "-"))
            if abs(inverse - printed_result) <= half_last_place:
                return tuple(value.replace("-", "−") for value in (a, b, m))
    return None


def add_calculation(data, marker, definition, operands):
    diluted = data.dilution_factor != 1
    marker.clear()
    variable = subscript(math_text("C"), math_text("meas" if diluted else "u"))
    expression = variable + math_text(" = ") + fraction(
        subscript(math_text("A"), math_text("u")) + math_text(" − b"), math_text("m")
    )
    if operands is not None:
        absorbance, intercept, slope = operands
        operation = " + " if data.intercept < 0 else " − "
        expression += math_text(" = ") + fraction(
            math_text(absorbance + operation + intercept), math_text(slope)
        )
    if not tiny(data.measurement_concentration):
        expression += math_text(f" ≈ {fixed(data.measurement_concentration)}")
    marker._p.append(equation(expression))
    if diluted:
        correction = definition.insert_paragraph_before(style=marker.style)
        corrected = subscript(math_text("C"), math_text("sample")) + math_text(" = D × ")
        corrected += variable
        if not tiny(data.unknown_concentration):
            corrected += math_text(f" ≈ {fixed(data.unknown_concentration)}")
        correction._p.append(equation(corrected))


def remove_paragraph(paragraph):
    element = paragraph._p
    element.getparent().remove(element)


def fill_table(table, rows):
    borders = OxmlElement("w:tblBorders")
    for edge in ("top", "left", "bottom", "right", "insideH", "insideV"):
        border = OxmlElement(f"w:{edge}")
        for name, value in (("val", "single"), ("sz", "4"), ("color", "D9D9D9")):
            border.set(qn(f"w:{name}"), value)
        borders.append(border)
    table._tbl.tblPr.append(borders)
    for index, values in enumerate(rows):
        row = table.rows[index] if index < len(table.rows) else table.add_row()
        for column, value in enumerate(values):
            cell = row.cells[column]
            cell.text = value
            cell.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
            paragraph = cell.paragraphs[0]
            paragraph.paragraph_format.space_before = Pt(2)
            paragraph.paragraph_format.space_after = Pt(2)
            if column == 1:
                paragraph.alignment = WD_ALIGN_PARAGRAPH.RIGHT
            if index == 0:
                paragraph.runs[0].bold = True
                shade = OxmlElement("w:shd")
                shade.set(qn("w:fill"), "E9F1F4")
                cell._tc.get_or_add_tcPr().append(shade)


def build_report(data, output):
    chart = render_figure(data)
    template = Path(__file__).resolve().parents[1] / "assets" / "report-template.docx"
    report = Document(template)
    slots = {paragraph.text: paragraph for paragraph in report.paragraphs if paragraph.text}
    discussion = comparison(data)
    result_slot = slots["{{Introduce the measured trend or calculated quantity.}}"]
    definition = slots["{{Define symbols. Show one worked substitution and the result with units.}}"]
    marker = next(paragraph for paragraph in report.paragraphs if paragraph.style.name == "Lab Equation")
    references = "Table 1 reports the fit and Figure 1 shows the calibration."
    reportable = data.unknown_concentration is not None
    operands = substitution_operands(data) if reportable else None
    if operands is None:
        absorbance = f"{data.unknown_absorbance:.15g}".replace("-", "−")
        intercept, slope = map(bounded, (data.intercept, data.slope))
    else:
        absorbance, intercept, slope = operands
        if data.intercept < 0:
            intercept = "−" + intercept
    if data.fit_status != "accepted":
        result_slot.clear()
        if data.fit_status == "unverified":
            result_slot.add_run("Calibration fit unverified. ").bold = True
            result_slot.add_run(f"Confirm the fit criteria before reporting a sample concentration. {references}")
        else:
            criteria = data.fit_criteria
            result_slot.add_run("Calibration fit rejected. ").bold = True
            result_slot.add_run(
                f"The fit was checked before rounding against a minimum R² of {bounded(criteria.minimum_r_squared)} "
                f"and a maximum absolute residual of {bounded(criteria.maximum_absolute_residual)}. "
                f"Review the standards and repeat the calibration before reporting a sample concentration. {references}"
            )
        remove_paragraph(marker)
        remove_paragraph(definition)
    elif not data.in_calibration_range:
        levels = [x for x, _ in data.standards]
        result_slot.clear()
        result_slot.add_run("Outside the calibration range. ").bold = True
        result_slot.add_run(
            f"The unknown absorbance of {absorbance} lies outside "
            f"the fitted response range for the {fixed(min(levels))}–{fixed(max(levels))} mg/L calibration. "
            f"Remeasure with a suitable sample preparation or a calibration range that covers the response. {references}"
        )
        remove_paragraph(marker)
        remove_paragraph(definition)
    elif data.dilution_factor != 1:
        factor = bounded(data.dilution_factor)
        result_slot.text = (
            f"The measured solution concentration was {concentration_text(data.measurement_concentration)}. "
            f"Applying a dilution factor of {factor} to the unrounded value gives "
            f"{concentration_text(data.unknown_concentration)} for the original sample. {references}"
        )
        definition.text = (
            "The two C terms denote the measured solution and original sample concentrations in mg/L. "
            "Aᵤ is the unknown absorbance, m is the slope, b is the intercept, and D is the dilution factor."
        )
        add_calculation(data, marker, definition, operands)
    else:
        result_slot.text = (
            f"The unknown absorbance of {absorbance} corresponds to "
            f"{concentration_text(data.unknown_concentration)} for the original sample (dilution factor 1). {references}"
        )
        definition.text = (
            "Cᵤ is the unknown concentration in mg/L, Aᵤ is the unknown absorbance, "
            "m is the slope, and b is the intercept. The calculation used workbook precision."
        )
        add_calculation(data, marker, definition, operands)

    updates = {
        "{{Experiment title}}": "Linear Calibration of an Unknown Sample",
        "{{Name • Course • Date}}": "Synthetic calibration example for workflow testing",
        "{{State what the experiment measures or tests.}}":
            f"Estimate an unknown concentration from {len(data.standards)} standard points.",
        "{{Record the equipment, conditions, procedure, and any actual deviations.}}":
            "A linear model with an intercept was fitted to the simulated standard means. "
            "The fitted model and calibration range were used to assess the unknown absorbance.",
        "Table 1. {{Brief description of the comparison}}":
            "Table 1. Linear calibration coefficients and fit statistic.",
        "Figure 1. {{What the figure shows and under which conditions}}":
            "Figure 1. Simulated standard means and the workbook's linear fit.",
        "{{Interpret the evidence, compare results, and evaluate a specific limitation.}}":
            discussion,
    }
    for slot, value in updates.items():
        slots[slot].text = value

    fill_table(report.tables[0], [
        ("Quantity", "Value", "Unit"),
        ("Slope", slope, "L/mg"),
        ("Intercept", intercept, "Dimensionless"),
        ("R²", bounded(data.r_squared) if data.r_squared is not None else "Not reported", "Dimensionless"),
        ("Maximum absolute residual", bounded(data.maximum_absolute_residual), "Dimensionless"),
    ])
    figure = slots["{{Insert figure here and cite it in the text.}}"]
    figure.clear()
    figure.alignment = WD_ALIGN_PARAGRAPH.CENTER
    figure.paragraph_format.keep_with_next = True
    figure.paragraph_format.space_before = Pt(8)
    picture = figure.add_run().add_picture(chart, width=Inches(5.0))
    picture._inline.docPr.set("descr", "Simulated calibration standards and fitted line from the workbook.")

    unused = [
        "Conclusion", "{{Answer each objective using a result presented above.}}",
        "References", "{{List the sources cited in the report.}}",
        "Appendix", "{{Include supporting records or full calculations if required.}}",
    ]
    if not discussion:
        unused.extend(["Discussion", "{{Interpret the evidence, compare results, and evaluate a specific limitation.}}"])
    for placeholder in unused:
        remove_paragraph(slots[placeholder])
    report.save(output)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("readings", type=Path)
    parser.add_argument("report", type=Path)
    args = parser.parse_args()
    try:
        if args.report.suffix.lower() != ".docx":
            raise ValueError("report output must have a .docx extension")
        data = load_calibration(args.readings)
        build_report(data, args.report)
    except (OSError, KeyError, ValueError, OverflowError) as error:
        parser.error(str(error))
    print("DOCX created.")
    if data.fit_status == "unverified":
        print("Confirm the calibration fit criteria before reporting a sample concentration.")
    elif data.fit_status == "rejected":
        print("Review the rejected calibration fit before reporting a sample concentration.")
    elif not data.in_calibration_range:
        print("The unknown response requires remeasurement before reporting a concentration.")
    elif data.reference_concentration is not None and data.unknown_concentration != data.reference_concentration:
        print("Follow-up questions for the student, outside the report:")
        print("Was the unknown diluted again before measurement?")
        print("Did the standards and unknown use the same blank?")


if __name__ == "__main__":
    main()
