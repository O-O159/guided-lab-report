# Reaction kinetics

## Confirm before calculating

Identify reaction/stoichiometry, batch or flow operation, concentration basis, temperature records, and the measurement-to-concentration relation. Conductivity is not automatically concentration: establish the manual's calibration or justified relationship, including endpoint/background values. Check whether initial reactants are equal or one is in excess before proposing a simplified rate law.

## Candidate outputs

- Concentration versus time, optionally the recorded signal versus time if that answers the objective.
- For a justified constant-volume single-reactant model: zero order `C=C₀−kt`; first order `ln(C/C₀)=−kt`; second order `1/C−1/C₀=kt`. These equations do not automatically describe unequal-reactant second-order kinetics or changing-volume systems.
- Fitted k, fit interval, units and diagnostics per condition. Rate-constant units depend on order and concentration/time units.
- Arrhenius `ln(k/k_ref)=ln(A/k_ref)−Ea/(RT)` for an agreed constant numerical reference unit, Kelvin temperature, and a consistent kinetic model. Slope against `1/T` is `−Ea/R`; keep R and energy units compatible. At least two temperatures define a line, but two points do not provide a residual-based slope uncertainty or a convincing linearity assessment.

Propose model/order and interval in the checklist. If several orders are genuinely to be tested, make that comparison explicit. Do not select the physical model solely by the largest R² across different response transformations.

## Prompts to carry into Discussion

Record curvature, timing offsets, temperature changes, and between-run variability as numerical observations. Ask the student what was actually observed during mixing, thermal equilibration or sampling. For temperature explanations of Ea, recompute the full affected fit when agreed; the position of the point and the actual/nominal temperatures matter. Do not write the illustrative “12% deviation” as experimental data.
