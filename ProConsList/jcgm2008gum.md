# JCGM 100:2008 (GUM): Guide to the Expression of Uncertainty in Measurement

**Source:** https://www.bipm.org/documents/20126/2071204/JCGM_100_2008_E.pdf  
**Evidence boundary:** Full text read 2026-09-22 (clauses 2.3, 4.2, 4.3, 5.1, 5.2, 6.1–6.3, F.1.2.3, G.6.6 verbatim). **Venue flag: international guide** of BIPM/IEC/IFCC/ILAC/ISO/IUPAC/IUPAP/OIML; content-identical to ISO/IEC Guide 98-3. Cite by document number, never as "ISO GUM".

## Sensors

Not applicable: metrology guide. Its worked examples use resistors and thermometers.

### Pros

- The internationally agreed document; there is no higher authority for an uncertainty budget.
- Freely and permanently available, so the pilot's uncertainty budget is fully checkable.

### Cons

- Frequentist/Taylor-series framework only; **does not cover Monte Carlo propagation** (that is the separate JCGM 101:2008, Supplement 1).
- Says nothing about drift as a stochastic process, clock-alignment error models, or co-location protocol — those stay with `wmo2023no8`, `cen2021ts17660`, `astm2022d8406`.

## Physical Box, Materials, and Geometry

Not applicable. Content used here: combined standard uncertainty `u_c^2(y) = sum (df/dx_i)^2 u^2(x_i)` (Eq. 10, **uncorrelated inputs only**); sensitivity coefficients incl. the **numerical** form (5.1.3 Note 2) for models that are not analytically differentiable; the correlated-input law (Eqs. 13/14/16); and expanded uncertainty `U = k * u_c(y)` (Eq. 18).

### Pros

- **§5.2.2's worked example is this project's pilot design:** ten resistors each calibrated against *the same* standard. Because `r = +1`, uncertainties add **linearly** (1 Ω), not in quadrature (0.32 Ω); the Guide states flatly that the quadrature answer "is incorrect". Ignoring a shared reference therefore errs **anti-conservatively**, here by ~3x.
- **§5.2.4 gives an actionable alternative to estimating covariances:** redefine inputs as the uncorrected quantities and introduce the calibration-curve parameters as additional independent inputs — "the correlation between X_i and X_j is removed". Its own example is a thermometer.
- Fixes what the project's `U95 <= 0.5 degC` target actually means: `2 * u_c(dT) <= 0.5 degC`, i.e. `u_c <= 0.25 degC`.

### Cons

- The propagation law is **first-order**; a strongly nonlinear lumped model needs either a justification of linearity at the operating point or the numerical sensitivity route (5.1.3 Note 2).
- **`k = 2` gives ~95 % only under the four G.6.6 conditions** — well-behaved input distributions, *comparable* contributions, adequate linear approximation, and effective degrees of freedom above about 10. It is not automatic.
- The Guide refuses the term "confidence interval" for the interval defined by `U` unless all contributions are Type A (6.2.2).

## Selection Lessons for This Project

- Cite for: standard / combined / expanded uncertainty definitions; Type A vs Type B; Eqs. 10, 11, 13, 14, 16, 18; numerical sensitivity coefficients; **the shared-reference correlation case and the decorrelation-by-reparameterisation recipe**; and `k = 2` ≈ 95 % **together with** the G.6.6 conditions.
- Do **not** cite for: Monte Carlo propagation (that is JCGM 101:2008); any drift, clock-sync or co-location protocol; or any claim that `k = 2` gives exactly 95 %.
