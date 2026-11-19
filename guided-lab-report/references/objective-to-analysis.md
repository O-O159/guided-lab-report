# Objective to required outputs

Use this reference in Step 1. An objective specifies the question; the manual and actual data constrain the model. Translate verbs such as determine, compare, verify, or evaluate into measurable outputs. If an objective is vague, ask what quantity or relationship the experiment is meant to establish.

## Select only relevant guidance

| Objective family | Candidate outputs | Read |
| --- | --- | --- |
| Reaction kinetics | Concentration/time curve, justified integrated-rate plot, rate constant; Arrhenius fit and activation energy only with multiple temperatures and that objective | [reaction-kinetics.md](discipline/reaction-kinetics.md) |
| Calibration and quantification | Standards plot, regression equation, R² and residuals, unknown concentration with dilution correction | [analytical-methods.md](discipline/analytical-methods.md) |
| Enzyme kinetics | Initial-rate/substrate curve, Km and Vmax, reciprocal plot if requested or taught | [enzyme-and-cell.md](discipline/enzyme-and-cell.md) |
| Microbial/cell growth | Growth curve, confirmed exponential interval, specific growth rate and doubling time | [enzyme-and-cell.md](discipline/enzyme-and-cell.md) |
| Heat/mass transfer | Relevant balance, driving force, overall coefficient, efficiency/effectiveness with an explicit definition | [heat-mass-transfer.md](discipline/heat-mass-transfer.md) |
| Pipe flow and pumps | Friction factor versus Reynolds number, or measured head, power, and efficiency versus flow | [heat-mass-transfer.md](discipline/heat-mass-transfer.md) |
| Distillation, extraction, absorption | Appropriate equilibrium/operating relationships, recovery or efficiency, ideal stages only when model and data support them | [separation.md](discipline/separation.md) |
| Filtration and drying | Cumulative filtrate and resistance estimate, or moisture content and drying rate on a defined basis | [separation.md](discipline/separation.md) |
| Conversion/selectivity/yield | Stoichiometrically defined conversion, selectivity, yield, and balance closure on a specified basis | [general-physics-chem.md](discipline/general-physics-chem.md) |
| Other science/engineering | Objective-specific measured relationship and derived physical quantity; replicate statistics where applicable | [general-physics-chem.md](discipline/general-physics-chem.md) |

These are a menu. Do not compute all items in a row by default. A biological lab need not involve enzyme kinetics; route by its objective, not its department name.

## Confirmation checklist

For each output state the input columns/run IDs, units, proposed equation/model, fitting interval, grouping, plot type, and reason it answers the objective. State which diagnostics and comparisons will be included. Separate required outputs from optional suggestions and mark missing information.

When a model determines a reportable quantity, identify the applicable model checks and their source before processing. For example, record a laboratory method's acceptance criteria for standard curves and what will be reported if they fail. Use the assignment or verified method to justify the checks.

Explain model choices in plain language. For example, reciprocal concentration is appropriate only under a justified second-order model; a request for a rate constant alone does not establish reaction order. A model mentioned in the manual can be proposed without claiming the experiment verifies it.

Ask: “These outputs would address the stated objectives. Are the scope, model, and fitting/grouping choices correct?” Wait for an answer. If the user revises the objective, update the checklist before calculating.

## Changes after confirmation

Necessary unit conversions and algebraic intermediate quantities belong to the agreed calculation. A new hypothesis test, additional fit, new plot family, or sensitivity study is an amendment: propose it with its purpose, then wait for confirmation. Do not repeatedly seek confirmation for the same established choice.

A confirmed factual correction within the agreed method, such as a recorded dilution, updates the agreed inputs. Keep the original readings, recalculate the dependent results, and revise each affected artifact together. If a correction requires a new model, different exclusions, or different outputs, confirm that change separately.
