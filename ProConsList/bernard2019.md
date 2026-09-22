# Bernard et al. (2019): Semi-Empirical Shelter Performance Model

**Source:** https://doi.org/10.3390/cli7020026  
**Evidence boundary:** Full text read 2026-09-22. Field-data modelling paper on the WMO Ghardaïa 2008–2009 shelter intercomparison; the **direct methodological competitor** for this project's K2 benchmark. Note: an earlier abstract-level scan in this repository mis-cited the first author as "Barbaresco"; the author is Bernard.

## Sensors

PT100 in every shelter (manufacturer ±0.1 °C, 10-s samples averaged to 1 min); Gill WindSonic; Kipp & Zonen CMA11B albedometer. Reference = mean of two Davis 7714 naturally ventilated shelters (90 % of pair agreement within ±0.3 °C).

### Pros

- Year-long desert dataset: 101,195 1-min steps, 12 shelters of 8 types, 70/30 split repeated 50 times.
- Head-to-head against the Nakamura and Cheng empirical models on identical data.

### Cons

- The reference "truth" is itself a passive shelter; wind < 1 m/s and night are excluded.
- Sensor and internal air are assumed at the same temperature, which the authors note contradicts Erell et al. and de Podesta et al.

## Physical Box, Materials, and Geometry

Cuboid Stevenson types and cylindric multiplates; per-type volume, cross-section and surface tabulated (e.g. Davis 7714: 5.6 dm³ / 2.9 dm² / 19 dm²; large Stevenson 1000 dm³ / 100 dm² / 620 dm²). Materials per type (wood, plastic, plastic/steel, polyester/fiberglass, ABS/aluminium/nylon); no thicknesses, absorptance or emissivity reported.

### Pros

- Model is derived from an energy balance, so its two fitted coefficients read as a response time and a radiation sensitivity; fitted time constants (1.6 / 3.3 / 13.9 min) match step-response events (2 / 2 / 15 min).
- Internal airspeed enters as a linear function of outside wind with the shelter cross-section.

### Cons

- **Coefficients are fitted after the shelter is built**; the authors state the link between coefficients and shelter characteristics "has not been investigated."
- No internal-heat term, no wall-conduction term, no vent-area/porosity term; albedo is lumped into a fitted coefficient and long-wave is excluded.
- Error "does not tend toward zero when the wind speed increases."

## Selection Lessons for This Project

- Supports a two-coefficient (thermal time constant + radiation gain) description with outside wind and shortwave as drivers, and checking a fitted time constant against step events — this is the **post-build baseline the pre-build route must beat (K2)**.
- Cannot justify pre-build prediction from drawings, any claim about internally heated enclosures, or a vent-area design rule.
