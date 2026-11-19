# Heat and mass transfer

## Confirm inputs and boundaries

Define the apparatus, stream directions, boundary, steady/transient operation, temperatures or concentrations, mass/volume-flow bases, properties at applicable conditions, and transfer area. Select thermal or mass-transfer calculations according to the objective; they are not interchangeable.

## Candidate outputs

- Sensible heat on a stream: `Q̇=ṁ cp ΔT` under the stated assumptions; include latent heat or other terms when applicable. Hot/cold duty disagreement may reveal an unclosed balance, not automatically heat lost to the room.
- Countercurrent terminal differences: `ΔT₁=Th,in−Tc,out`, `ΔT₂=Th,out−Tc,in`; use the appropriate endpoints for other arrangements. `LMTD=(ΔT₁−ΔT₂)/ln(ΔT₁/ΔT₂)`. For equal positive terminal differences, use the continuous limit `LMTD=ΔT₁` instead of a 0/0 formula. Nonpositive or inconsistent differences require checking the model/records, not taking absolute values to force a result.
- `U=Q̇/(A F LMTD)` only with the correct area basis, a justified duty and arrangement correction F when needed. Do not silently assume F=1 for every exchanger.
- Effectiveness, recovery and “efficiency” require explicit definitions. For suitable sensible heat exchange, `ε=Q̇/[Cmin(Th,in−Tc,in)]`; do not substitute this for an instructor's different efficiency definition.
- For mass transfer, use a model-specific driving force and coefficient basis, e.g. gas or liquid side and local or overall. Temperature LMTD is not automatically the concentration driving force.

## Pipe flow and pumps

- Pipe resistance: use the pressure loss across the correct length and distinguish straight-pipe loss from local losses or static head. Confirm diameter, fluid properties, and the measured-flow conversion. Plot friction factor versus Reynolds number when it serves the objective. Use the same Darcy or Fanning convention for calculations and reference correlations; the Darcy factor is four times the Fanning factor.
- Pump curves: use pressure, velocity, and elevation changes across the pump to determine head when applicable. Plot head, hydraulic power, or efficiency versus flow as assigned. State whether the efficiency denominator is shaft input or electrical input. Identify the best efficiency observed in the tested range and its operating conditions.
- For a comparison with a pump curve or correlation, match speed, fluid conditions, loss components, and geometry. Ask about actual speed or valve position, gauge zero, pressure-tap location, and stability only where they bear on the discrepancy.

## Discussion prompts

Quantify stream-duty mismatch or coefficient trends. Ask about documented insulation, flow stability, air bubbles, sensor location, fouling or equilibration relevant to the experiment. Check predicted effects through the actual formula; a temperature bias can affect both duty and driving force.
