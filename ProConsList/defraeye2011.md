# Defraeye et al. (2011): Convective Heat Transfer Coefficients for Exterior Building Surfaces

**Source:** https://doi.org/10.1016/j.enconman.2010.07.026  
**Evidence boundary:** Full text read 2026-09-22 **as the accepted author manuscript (KU Leuven Lirias)**, not the typeset version of record; it carries the full Tables 1 and 2. Archival journal. **This supplies the missing provenance of this project's `h = 5.0 + 4.0*U`.**

## Sensors

Not applicable to the authors' own work (steady RANS CFD with low-Reynolds-number wall modelling). The reviewed correlations come from published full-scale field measurements and wind-tunnel experiments.

### Pros

- Tabulates ~12 independent measured correlations **with their reference-wind definition and validity range**, so the spread can be shown rather than a single value asserted.
- Names the assumptions being inherited: smooth surfaces, windward/leeward binary, point-vs-average coefficient, stratification effects at low wind.

### Cons

- **Nothing in it is a small outdoor instrument enclosure.** The smallest objects are a 3 m cube and an 8.5 x 8.5 x 5.6 m building; scaling to a ~10 cm enclosure is unsupported.
- **No uncertainty figures**: it documents disagreement between correlations but never quantifies an RMS error for any of them.

## Physical Box, Materials, and Geometry

Building facades and wind-tunnel bluff bodies; the authors' own case is an isolated cube in a neutral atmospheric boundary layer.

### Pros

- **Gives the exact origin of the linear form:** Juerges' flat-plate wind-tunnel correlation, `h = 4.0*U + 5.6` for **U <= 5 m/s**, and `h = 7.1*U^0.78` above it. Explains why linear forms exist at all: "Linear correlations account for buoyancy effects at low wind speeds, using an intercept, while power-law correlations are generally used for forced convection."
- Own CFD gives surface-averaged **`h = 5.01*U10^0.85` (windward)**, exponent "comparable to what was found for flat plates (0.8)".

### Cons

- **Three specific problems with this project's current constant:** (1) the literature intercept is **5.6, not 5.0**; (2) Juerges holds only to **U <= 5 m/s**; (3) its `U` is a free-stream/near-surface speed, which the authors criticise as "some undefined wind speed near the building surface" - and **every measured linear fit referenced to weather-station U10 in Table 1 has a slope of 0.90-2.9, not 4.0**.
- The authors' own recommendation is **against** a linear form for forced convection: a power law "is more appropriate and also provides a better approximation of the data".

## Selection Lessons for This Project

- Cite for: the Juerges linear correlation and its 5 m/s limit; the table of measured `a + b*U10` coefficients; the CFD power laws; and the documented reasons these correlations are not transferable.
- Do **not** cite it as evidence that `5.0 + 4.0*U` is valid against **weather-station** wind, as support for small-enclosure geometry, or for an uncertainty band on h.
