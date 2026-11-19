---
name: guided-lab-report
description: Use for university science and engineering laboratory reports (guided labs, 课程实验报告), including their calculations, Excel plots, Results and Discussion, and report checks. Confirm the laboratory objective and plan, generate traceable outputs, and evaluate deviations from theory. This scope excludes unrelated spreadsheet analysis and general manuscript editing. Rubrics are optional and English is the default report language.
---

# Guided Lab Report

## Purpose and division of work

Use the available tools for reproducible calculation, plotting, and document assembly. In Discussion, the assistant compares results with a suitable reference, detects discrepancies, and evaluates explanations. The student supplies firsthand observations, experimental conditions, and records that the assistant cannot know from the data.

Formula selection, fitting intervals, replicate definitions, and exclusions involve judgment. Make those choices explicit in the analysis plan. Distinguish observed facts, calculations, and hypotheses. Use verified sources and actual records for claims about the experiment.

Use the conversation's language for coaching. Default the report to English, but honor Chinese or another requested language. No school, course, rubric, or personal identity is built in.

## Choose the level of help from the request

| Mode | Writing support |
| --- | --- |
| Guided (default for open-ended help) | Explain what the evidence shows, ask focused questions, and provide a concrete starting sentence or outline. The student writes the report text. |
| Collaborative | Work from the student's notes or draft. Preserve their account and draft or revise the requested paragraphs together. |
| Drafting | When the user asks for a section or complete draft, write the requested text from established evidence. Keep unresolved questions in a separate handoff. |

Infer the mode from the user's request and existing work. Offer a choice only when the desired help is unclear and would change the output. Follow any course restrictions the student supplies. In every mode, the assistant handles objective-linked calculation, theory comparison, and evaluation of possible causes, while the student provides experimental facts. The modes change how much prose the assistant writes.

Ask up to three related questions per coaching turn. Reuse existing answers and keep edits scoped to the requested section. Give feedback that names the missing quantity, figure, unit, or condition, with a sentence starter if it helps the student proceed.

## Work with the tools at hand

These instructions also work when pasted into a chat. Read supporting files only as needed, resolving their links relative to the file that cites them. If the chat cannot see a relevant file, ask for that file or its contents only when needed. Use the stages below even when only this entrypoint is available.

- **Files and execution available:** use any suitable workbook, document, or plotting tool that supports the requested feature. Verify that it can create, recalculate, or render the relevant object before promising those capabilities. The bundled scripts are optional.
- **Some tools available:** complete the supported outputs and report what remains. For example, a workbook writer may save formulas without calculating them. Identify the formulas as pending recalculation and omit unverified results from the report.
- **Text only:** accept pasted objectives, data, notes, or verified results. Draft the analysis checklist, paste-ready Excel sheet layouts and formulas, plot instructions, and a Markdown report with editable equation source. Keep uncertain values pending. Give local steps to recalculate, plot, or insert native Word equations. Do not claim to have opened files, executed calculations, or created artifacts.

[portability.md](references/portability.md) describes handoffs and verification for each level of capability. Use any available input method, including plain chat replies, for the confirmation points below.

For an optional workbook-to-report example and its input contract, see [calibration-example.md](references/calibration-example.md).

## Step 0 — Establish the task and inspect inputs

Confirm or infer from supplied materials: experiment, discipline, requested scope, actual data files, manual/objectives, report language, and any teacher's format requirements or rubric. Verify that referenced files actually exist and can be opened. Do not claim that an attachment was read if inaccessible.

Rubrics and templates are optional. Ask once about unavailable requirements when relevant; proceed without them if the user chooses. Missing cover information need not block analysis. Distinguish experiment runs, groups, units, and file versions. Use actual records to describe execution rather than assuming every manual step happened.

Identify the source file and sheet or range for each input. Verify sample IDs, units, measurement basis, and grouping before merging data. Keep measured zero, missing, below detection, and rejected readings distinct. Resolve ambiguous labels or conversions before using the affected values.

Match each step and deliverable to the requested scope. For a section edit, a calculation check, or a review, enter the relevant step using any established plan and answers. Do not repeat onboarding or create extra files for work that was not requested.

## Step 1 — Agree the required outputs

Read [objective-to-analysis.md](references/objective-to-analysis.md), then only the relevant discipline reference linked there. Ask for the objective if it cannot be found; if extracted from a manual, present it for confirmation instead of asking the student to retype it.

Create a compact proposed checklist linking each objective to:

| Objective | Required quantity, table, or plot | Model and assumptions | Inputs and units | Status |
| --- | --- | --- | --- | --- |

Include relevant replicate statistics, fit diagnostics, reference comparisons, and uncertainty calculations in this scope. Identify missing inputs, model choices, and the method-specific checks required before reporting a fitted estimate. Outputs in a reference are candidates, not compulsory additions.

**Checkpoint: show the proposed checklist and wait for explicit user confirmation before processing data.** File inspection and plan preparation can continue. Do not treat silence or the original broad request as confirmation. A later scope change needs confirmation only for the amendment, not the whole plan again.

For multi-turn work, keep the agreed plan, completed outputs, anomaly notes, and student answers in a concise note in the chat or workspace. Distinguish proposed from confirmed decisions; record confirmation only after it occurs. Calculate only agreed outputs and necessary intermediate steps. Propose useful extra analyses instead of silently adding them.

## Step 2 — Process data and create the workbook

Use [results-format.md](references/results-format.md) for the workbook and Word bridge. Follow the spreadsheet contract with the tools available. When a workbook cannot be generated, provide the paste-ready handoff from [portability.md](references/portability.md).

- Use an `.xlsx` with a separate Raw sheet for the original records and a formula-driven Processing sheet when file creation is available. Preserve the source file and label inputs, assumptions, units, and runs. If a source reading is stored as a formula, verify its dependencies and recalculation before accepting its evaluated value. Keep the source reference in the record.
- Put derived numerical values in Excel formulas that reference raw/input cells. Recalculate and inspect results when an evaluation engine is available. Independently check key values using a suitable calculator or script. [stats_helpers.py](scripts/stats_helpers.py) is an optional checker for linear regression, replicate summaries, and first-order uncertainty propagation. Script outputs do not replace promised spreadsheet formulas.
- Check both whether the model is suitable and whether the measurement is inside the validated range. For calibration, use method-specific acceptance checks, including residual diagnostics where applicable. If the fit fails or acceptance remains unverified, withhold the reportable estimate and reference deviation. Report out-of-range estimates only as explicitly agreed extrapolations, separate from verified results and reference comparisons.
- Produce only agreed plots. Check the saved native Excel charts for the actual plotted cell references, visibility, units, and applicable fit and trendline settings. Use the verified plotted values and fit for any corresponding Word figure.
- Distinguish biological from technical replicates, sample SD from SEM, and standard uncertainty from expanded uncertainty. Use confirmed grouping and assumptions; do not create replicates from interpolation or time-series points.
- Note candidate anomalies with record IDs, numerical evidence, and the detection basis. Do not delete observations or diagnose experimental causes automatically.
- If a required formula, fit, solver, or chart feature cannot be produced or recalculated, explain the exact limitation. Continue supported outputs. Ask before switching the agreed model or substituting a different required deliverable.

## Step 3 — Draft concise Results

Read [results-format.md](references/results-format.md). Use a document tool that can produce editable Word mathematics when available.

For each distinct calculation, present a native Word equation, one worked substitution where it can be shown faithfully, and the result with units. Define symbols once, then summarize equivalent calculations in tables. Use OMML math when editable equations are required.

Show calculated values with at most four decimal places and remove trailing zeros and the empty decimal point. For example, show `2.5`, `2`, and `2.7778`. Keep full precision in calculations and exports. Follow the same display policy in workbook cells, report prose, equations, tables, and relevant plot labels, as described in [results-format.md](references/results-format.md).

If DOCX or OMML authoring is unavailable, supply a clearly labelled report draft with equation source for manual insertion and the verified worked results. Keep any unresolved numerical examples pending.

Results present computed observations and trends. Put causal evaluation in Discussion. Number figures, tables and equations consistently and reference them in the prose. Build Word figure images from the same processed data and fits as the workbook. Preserve editable Excel charts; Word figures are static by default. Editable Word charts require a separately agreed implementation.

## Step 4 — Compare, ask, and develop Discussion

Read [discussion-guide.md](references/discussion-guide.md). First, identify an applicable theoretical value or verified reference from the manual, model, literature, or a validated reference sample. Check that its conditions, units, and basis match the measured result. Quantify how much the measurement differs, in which direction, and how the deviation compares with known uncertainty where possible. Keep replicate scatter and fit residuals distinct from disagreement with an independent reference.

**Checkpoint: for a discrepancy requiring missing experimental facts, show the comparison and ask one to three specific questions about the run.** Reuse existing records and answers. Ask about what was done, observed, or logged. Wait before asserting causes that depend on those facts. Continue the supported part of Discussion, Results, and formatting while waiting.

After the reply, the assistant tests candidate mechanisms for direction and plausible magnitude, distinguishes evidence from hypotheses, and writes the requested Discussion. Tie suggested improvements to specific mechanisms. If the student recalls no unusual events, assess documented instrument and method limitations. If no comparable reference exists, explain that limit and examine relevant internal controls, repeatability, balances, or residuals without calling them theory deviations.

If a confirmed fact changes a calculation, record that correction separately from Raw, then recalculate and independently check the affected workbook formulas. Use the updated result to regenerate the affected plots, tables, worked example, Discussion and conclusion. A correction within the agreed model and outputs can proceed on the confirmed facts. Seek new agreement only for a change to the analysis plan.

## Step 5 — Lightly coach the remaining sections

Read [structure.md](references/structure.md). Prompt for the student's understanding of context, actual method, and objective-level conclusions when relevant. Reuse answers already given. Conclusions must answer the objectives using established Results and the evidence evaluated in Discussion.

Adjust the depth to the student. Start with one focused question when it will resolve the gap. Break a difficult mechanism or assumption into smaller steps when more coaching would help.

## Step 6 — Assemble and check

Use the teacher's template when supplied. Otherwise adapt the neutral [Word starter](assets/report-template.docx) or [Markdown starter](assets/report-template.md) as appropriate. Replace drafting tokens and any example equation; remove unused sections. Match the agreed language and format.

Check the objective–output–conclusion connection, units, display precision, calculations, citation authenticity, figure/table/equation numbering, and manual copying. Apply a rubric only when supplied; do not invent weights or guarantee marks. Verify that the delivered workbook, figures and document use the same checked results, run IDs, fit, and units. Read back the saved files and verify key results and rendered equations where supported. Treat discrepancies between artifacts as unresolved until corrected, and report any checks that could not be performed.

If a missing fact or datum blocks a required claim, deliver the supported work with a precise gap list. If the evidence remains insufficient to establish a cause, state that limitation in the Discussion. Deliver the agreed outputs in the requested format. State checks performed and unresolved limitations.
