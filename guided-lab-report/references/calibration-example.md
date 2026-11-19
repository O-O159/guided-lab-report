# Optional calibration scripts

These scripts demonstrate an Excel-to-Word workflow for an unweighted linear calibration with a free intercept. They are optional examples. Adapt the model, units, grouping, and acceptance criteria to the approved method before using them for a different experiment. Supply your own input file.

## Input contract

Create a JSON file with these fields:

| Field | Required content |
| --- | --- |
| `standards` | At least three entries with a text `id`, distinct numeric `concentration` in mg/L, and `absorbances` containing three numeric readings. |
| `unknown` | A text `id` and `absorbances` containing three numeric readings. |
| `reference_concentration` | An independently assigned nonnegative concentration in mg/L on the original-sample basis. |
| `fit_criteria` | An object with `minimum_r_squared` and `maximum_absolute_residual` from the applicable method. Omit both if the criteria are unknown; the fit will be marked unverified. |

Absorbance is dimensionless. Enter a confirmed numeric dilution factor in `Processing!I10` where applicable. The measured solution must fall within the validated range, and the fit must pass its criteria, before an original-sample concentration or reference deviation is reported.

## Run the examples

Use Python 3.10 or later and run these commands from the skill folder. Workbook creation requires openpyxl. Plotting requires Pillow 10.1 or later. Word output also requires python-docx.

```text
python scripts/calibration_workbook.py build /path/to/input.json calibration.xlsx
```

Open the workbook in Excel or a verified compatible engine, recalculate the formulas, and save it. Then run:

```text
python scripts/calibration_workbook.py export calibration.xlsx calibration-results.json
python scripts/make_figure.py calibration-results.json calibration.png
python scripts/build_report_example.py calibration-results.json calibration-results.docx
```

The export checks the input cells, formulas, evaluated values, and chart bindings. The figure and Word document consume the same verified values and fit. Four-place decimal rounding is applied only for display. The Word script produces an example-format document; adapt it to the assignment before use.

Use new output files after a change to the workbook and stop if a step fails. Check the chart and rendered Word report before relying on them. For a conversation-based workflow without file tools, see the [portability guide](portability.md).

Script entry points: [workbook and results export](../scripts/calibration_workbook.py), [static figure](../scripts/make_figure.py), and [Word Results](../scripts/build_report_example.py).
