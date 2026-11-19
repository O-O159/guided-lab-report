# Enzyme kinetics and cell growth

Read the relevant branch only. Confirm units, blanks, independent experimental units and whether repeats are technical or biological. Do not inflate the biological sample size by counting multiple readings of one culture as independent cultures.

## Enzymes

Determine initial rates from a justified early linear interval; confirm blank correction, signal-to-product calibration, reaction volume and enzyme amount where used. A time-course endpoint is not automatically an initial rate.

Candidates: initial rate versus substrate concentration; Michaelis–Menten `v=Vmax[S]/(Km+[S])` where assumptions apply; Km and Vmax. The familiar reciprocal representation `1/v=(Km/Vmax)(1/[S])+1/Vmax` can be included when assigned. It changes the error structure and magnifies low-rate errors; do not require it for every enzyme report or treat an unweighted reciprocal fit as automatically preferable to direct nonlinear fitting. Confirm the fitting method and its Excel implementation in the plan. Do not choose inhibition or allostery models without the required design/data.

Ask about substrate ranges, timing, enzyme storage, temperature/pH control, and whether those factors were actually recorded. Do not infer loss of activity from an unverified handling event.

## Microbial/cell growth

Confirm what was measured (OD, count, viable count, mass), blank/dilution corrections, and the validated range of the measurement. OD is a proxy and cannot become cell concentration or viability without an appropriate calibration/method.

Candidates: measurement versus time; `ln(X/Xref)` versus time over a user-confirmed exponential interval; slope μ with inverse-time units; doubling time `ln(2)/μ` for positive exponential growth. If μ is zero or negative, do not report a positive doubling time. Lag or stationary points do not belong automatically to an exponential fit.

Ask the student which interval appears exponential and why; present numerical evidence to help them choose. Flag saturation, inconsistent dilutions and between-culture differences without diagnosing contamination from the curve alone.

When direct enzyme fitting is needed, consult the selected fitting tool's official documentation and an appropriate authoritative method source. Do not add nonlinear dependencies merely to generate an unrequested alternative fit.
