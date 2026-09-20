# Nakamura and Mahrt (2005): Errors in Naturally Ventilated Radiation Shields

**Source:** https://doi.org/10.1175/JTECH1762.1  
**Evidence boundary:** Full text read 2026-09-22 (publisher HTML; equations rendered as images, tables read from table images). Single-site field study establishing the canonical empirical wind/shortwave correction for a passive multiplate shield.

## Sensors

Onset HOBO Pro thermistor (±0.2 °C) in a Davis 7714 multiplate shield; reference RM Young 43347 RTD in an RM Young 43408 aspirated shield (radiation error < 0.2 °C at 1100 W/m²); Vaisala WS425 sonic; Kipp & Zonen CNR1; LI-COR pyranometers.

### Pros

- True aspirated reference with stated specifications; sensors intercompared in an ice bath.
- Coefficients fitted on 2002 and verified on an independent 2003 season.

### Cons

- The corrected residual (0.11–0.13 °C RMSE) is comparable to the reference's own radiation error, so the floor is reference-limited.
- 30-min averaging removes transient behaviour.

## Physical Box, Materials, and Geometry

Multiplate shield, plates 0.188 × 0.213 m, 7.0 cm interior height, 1 m above grass; thermistor 2.5–6 cm above the next plate. Shield material not reported; plate conductivity assumed "sufficiently high."

### Pros

- A single nondimensional forcing ratio X = Rad/(ρ·Cp·T·U) explains 98 % of bin-averaged daytime error variance (day: C0 = 0.13, C1 = 373.40; night, net radiation: 0.047, 355.84).
- Direct measurements of shortwave penetration into the shield (1.4–3.1 % of ambient by ground albedo) and of shield-surface temperature.

### Cons

- One shield model, one site, one surface type; the authors state coefficients "may not be optimum for surface types other than grass."
- Fit has a spurious non-zero intercept and breaks down for X < 1.0 × 10⁻⁴; no geometry or material parameter enters the model.
- Flow efficiency inside the shield is explicitly not modelled.

## Selection Lessons for This Project

- Supports testing Rad/(ρ·Cp·T·U) as the primary regressor with a day/night split and recording ground albedo. This project's heating number `Pi_G` is a **generalisation of X** (adds absorptance, shading, projected/convective area ratio and radiation–convection coupling), not a new construct.
- Cannot justify predicting coefficients from enclosure design, any internally heated case, or transferring coefficients across shields or surfaces.
