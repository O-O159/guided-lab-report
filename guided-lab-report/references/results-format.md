# Traceable workbook and concise Word Results

## Workbook contract

Use an available workbook editor or file writer. Preserve the original source files. Raw observations belong in a separate Raw sheet; preserve values, IDs, recorded units, run order and missingness. If copied from multiple sources, note the source/range next to the data. Do not overwrite Raw with corrected numbers. Follow the text handoff in [portability.md](portability.md) when file creation is unavailable.

Processing contains formulas for derived values, linked to raw cells and clearly labelled inputs/constants. Text labels and documented input constants need not be formulas; derived numbers must not be pasted script results. Keep units in headers and numbers numeric. Avoid hidden calculation dependencies.

Record the source file/version, sheet/range, run labels, and units for included inputs. Put corrections such as dilution, baseline, or instrument offsets in a separate labelled input with their source and applicable runs. Preserve raw readings and use the same confirmed measurement basis throughout. Never silently fill a blank, interpret text as a number, or convert a non-detect to zero.

Inspect designated raw readings in the formula view as well as the evaluated view when using a workbook. A numeric formula cache is not an independently observed value. If an input is derived in the source, trace and recalculate its dependencies before recording the verified value with the source cell and basis. The bundled example expects literal observations in Raw.

Common formula patterns, with actual ranges chosen for the current data:

- Mean: `AVERAGE(range)`; sample SD: `STDEV.S(range)` with `COUNT(range)>1`; SEM: SD / `SQRT(COUNT(range))` only for independent replicate measurements. One observation has no estimable sample SD; do not display it as zero.
- OLS: `SLOPE(y_range,x_range)`, `INTERCEPT(y_range,x_range)`, `RSQ(y_range,x_range)`; predicted value `slope*x+intercept`; residual `observed-predicted`. All use identical valid paired records. Undefined R² for constant response is not evidence of a perfect model.
- First-order propagation: `u_y² = gᵀΣg`; explicit derivative terms and covariance entries must remain traceable. Use documented standard uncertainties. A rectangular bound ±a gives `a/SQRT(3)` only when that distribution is justified. Do not confuse this with sample SD or SEM.
- `scripts/stats_helpers.py` independently checks sample summaries, ordinary linear regression with intercept, and supplied-gradient propagation. It does not select the model or validate causal interpretations. It needs NumPy; check availability in the selected runtime before invoking it.

Never hide invalid inputs with `IFERROR(...,0)`. Distinguish missing from measured zero. Keep exclusions as explicit, justified selection decisions and preserve original records. Label candidate anomalies with values and row/run IDs; do not automatically remove them.

For nonlinear fits, an ordinary Excel trendline is not necessarily the physical model. Explain the implementation and seek agreement: a transparent formula-based objective/iteration or supported Solver workflow may be suitable. Solver parameter cells are explicitly labelled adjustable inputs; downstream quantities and the objective remain formulas. A script-only fit pasted as unexplained constants does not meet this contract. Test recalculation behavior and disclose features needing manual re-solving. Do not claim an unavailable solver ran.

## Figures and the Excel–Word bridge

Keep native Excel charts linked to the processed data, not screenshots. Use the agreed fit, equation and R² where meaningful; a growth trajectory or nonlinear physical model does not need an unrelated linear trendline. Show fit range and axis transformations. R² on different transformed response scales is not directly comparable evidence of the best physical model.

In Word, use static high-resolution figures generated from the same processed values and fit coefficients, or export the verified Excel chart. Match series, exclusion decisions, axes, units and rounding. Do not maintain an independently typed second dataset. Prefer ~300 dpi at the placed size; verify label readability. State in delivery that Excel charts remain editable and Word figures are static. Native editable/embedded Word charts are possible in some workflows but are outside this default implementation; do not claim they are universally impossible.

Verify that key derived workbook cells still contain the expected formulas as well as evaluated values. Recalculate the saved workbook, read back the evaluated quantities and units, and spot-check the actual saved result against Raw independently. Check the native chart's saved X and Y ranges, relevant hidden-row settings, and trendline model against the verified values. Verify the fit statistics from the same points and use the verified fit for a Word figure.

Use one verified results export or worksheet range as the source for the report. If any approved input or correction changes, make new readback data, rebuild the affected static plots and prose, and check the revised figures, tables and conclusion against the revised workbook. Keep a diagnostic estimate or discarded revision visibly separate from the result reported to the user.

The [calibration walkthrough](calibration-example.md) shows one optional implementation that transfers evaluated workbook values into the figure and Word example. Adapt the approach for other models, measurement units, and figure types.

## Calculation presentation

For each distinct calculation, show:

1. General equation as native OMML, numbered if referenced later; define symbols and units once.
2. One worked substitution from an identified real run, also using native math.
3. Result with the appropriate unit and the display policy below.

Use the unrounded inputs for calculations and an approximation sign when showing a rounded result. Keep original readings at their recorded precision. If a numerical substitution using the permitted display precision would disagree with its reported result, show the symbolic equation and the rounded result, and point to the unrounded values in the workbook.

For example, a confirmed first-order decay model could use `k = ln(C₀/Cₜ)/t`; use actual values only when available. An enzyme model, balance equation, and uncertainty expression are distinct calculations; repeated rows of the same equation are not.

Summarize equivalent results in a table. Include condition/run, value and unit; include uncertainty only when supported, with its type stated. Full raw/processed records belong in the appendix or accompanying workbook according to submission requirements. Do not round intermediate values or repeatedly print identical derivations.

## Native Word equations

Use a document tool with native equation support. [word_math.py](../scripts/word_math.py) provides optional constructors for fractions, subscripts, superscripts, square roots, and editable symbols; its docstring shows composition. Check the DOCX ZIP XML for `m:oMath`/`m:oMathPara`. Fractions should use `m:f`; scripts use `m:sSub`, `m:sSup` or `m:sSubSup`; roots use `m:rad`; symbols such as μ, σ and Δ must remain editable math text. A picture or a regular text run with caret notation does not meet the requirement.

Replace any equation placeholder in the template with the applicable experiment equation. Replace or remove all drafting tokens. When native equation authoring is unavailable, supply the equation source with the draft and name the remaining conversion step.

Render all final pages and inspect fractions, superscripts, subscripts, Greek characters and units for clipping, glyph loss and alignment. Do not rasterize equations silently to make a rendering failure disappear. If rendering/editability cannot be verified, report the specific limitation.

## Cross-references and precision

Number figures, tables and equations consistently. Cite each in the text and keep captions next to the objects. Use appropriate Word caption/cross-reference fields where the authoring tool supports them; check displayed numbers after assembly.

Display calculated values at most to four decimal places in Excel and the report. Round to nearest, with exact halfway values rounded away from zero. Strip trailing zeros and the decimal point when no fractional digits remain. Examples: `2.5000 → 2.5`, `2.0000 → 2`, `2.777777... → 2.7778`. Apply the rule to calculated percentages, fit statistics, and deviations. Keep calculations and machine-readable exports at full precision. Four places are a display limit, not an estimate of measurement uncertainty.

When a nonzero difference would round to zero, distinguish that from an exact zero with a clear bound and direction where relevant. If rounded operands look equal but the difference is visible, say that the difference comes from unrounded values and provide a link or cell reference. When displaying uncertainty, label what it represents and keep precision consistent with the evidence.

Method references for implementers: [NIST calibration](https://www.itl.nist.gov/div898/handbook/pmd/section5/pmd521.htm), [NIST propagation](https://www.itl.nist.gov/div898/handbook/mpc/section5/mpc55.htm), [SciPy OLS reference definitions](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.linregress.html). These do not automatically become citations in the student's report.
