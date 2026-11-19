# Using this skill across AI environments

## Load the workflow

Use the `guided-lab-report/` folder with a client that loads Agent Skills. Keep `SKILL.md` at its root, next to `references/`, `assets/`, and `scripts/`. Follow the selected client's import mechanism. If the client takes a folder, unpack the archive first.

In a chat without a skill loader, paste or attach `SKILL.md` and ask the assistant to follow it for the current lab. Supply the relevant reference only when it would help. In a chat without file input, paste the objective, applicable rubric excerpts, and data as a small table or tab-separated text. Never guess what is in an inaccessible attachment.

## Choose a delivery path

| Available capabilities | Delivery |
| --- | --- |
| Worksheet authoring with native charts; a recalculation engine; DOCX authoring with native math; and a renderer | Formula workbook, editable native Excel charts, static matching figures in Word, and a Word report with native editable equations. Verify each supported item independently. |
| Spreadsheet or Word export, with partial calculation or preview support | Export the parts supported. State which calculations need recalculation, charts need inspection, equations need insertion, or pages need rendering. A saved formula or equation in the XML verifies structure, not its evaluated value or appearance. |
| Text only | Workbook layouts and paste-ready formulas, instructions for plot ranges and styling, and a Markdown draft with equation source. Carry pending calculations and coaching answers forward in the conversation. |

The workflow has no required packages. The optional numerical helper uses NumPy. The optional [calibration walkthrough](calibration-example.md) lists the packages for workbook creation, figure generation, and editable Word math. Use a verified spreadsheet engine to recalculate and a document renderer for layout inspection.

## Handoff for a text-only chat

1. Get the same explicit confirmation of the analysis plan as in the full workflow.
2. For each worksheet, specify its name, where it starts, columns and units, and exact formulas for the first data row and summary cells. Include fill-down ranges. Keep raw data unchanged. Include critical assumptions with source, unit and cell address.
3. Return tab-separated data and formula blocks separately. Import sample IDs and literal text into text columns so values such as `0012` and `1-2` keep their meaning. Verify the delimiter, numeric locale, units, and values after import. Use spreadsheet formulas only for the calculation block. Flag missing values and preserve observed zeros.
4. Specify each plot's exact x/y ranges, units, series labels, fit model and limits. Keep Excel and Word figures on the same fit and data selection. If the user recalculates locally, ask for the relevant output values or chart export when needed for Results.
5. Provide the report draft in Markdown with LaTeX-style equation source. Explain that an Office equation editor or DOCX authoring tool is needed to turn the source into native editable math. Keep insertion notes and outstanding questions outside the submitted report text.
6. Track plan confirmation and any unanswered questions about experimental facts in chat. For a client change, include verified inputs, agreed outputs, calculations or files produced, checks performed, the reference comparison and its source, and the student's recorded observations.

## Using partial verification

Check with a representative input and expected output when possible. For workbook formulas distinguish formula presence, evaluated values and a verified recalculation after an input changes. For Word, distinguish native equation markup from successful rendering. Report the specific level reached for the requested deliverable.
