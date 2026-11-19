# Calibration and analytical methods

## Establish the measurement model

Identify standards, blanks, unknowns, response units, concentration units, replicate groups, dilution/extraction steps, and the relevant measurement range. Match blank handling to the actual protocol. Do not force a calibration through the origin unless justified and confirmed.

## Candidate outputs

- Standard concentration versus response (absorbance, peak area or other stated signal), fitted equation, R², and residuals for the agreed range/model.
- For an accepted linear model `y=mC+b`, the inverse estimate `C=(y_unknown−b)/m` is for the measured solution. Check it against the validated range on that basis. Apply the documented dilution factor only to an estimate supported by the fit and range checks, then compare with a reference on the corresponding basis. A zero slope is not invertible. When the response is out of range, the fit fails, or model acceptance cannot be verified, withhold the reportable concentration and deviation. Identify the check to resolve before reporting.
- Beer–Lambert calculations require applicable path length, absorptivity, units and validity; do not assume a calibration slope equals molar absorptivity regardless of the concentration scale.
- HPLC quantification must specify external/internal-standard procedure, peak identity/integration and response basis. Retention time alone does not establish identity or quantitative recovery.
- Detection/quantification limits, recovery corrections and weighted fits are additional analyses requiring objective/protocol support and suitable blank/low-level data. Do not infer LOD from R² alone.

Use the method's actual acceptance criteria and residual behavior to establish model suitability. A point inside the standards' range does not establish a usable calibration, and neither does R² alone. Record what checks and thresholds apply and why. If no suitable criteria or supporting evidence are available, label the fit as pending verification rather than borrowing an example cutoff. Calibration uncertainty must include applicable measurement and fit contributions, including slope/intercept covariance.

## Discussion prompts

Show the actual unknown result, calibration range, signed deviation where a valid reference exists, and candidate residual anomalies. Ask about documented pipetting, dilution, blanks, cuvette condition, preparation age or integration decisions. Quantify a proposed dilution mistake by its actual factor only when the student confirms it occurred.

Implementation reference: [NIST inverse calibration](https://www.itl.nist.gov/div898/handbook/pmd/section5/pmd521.htm).
