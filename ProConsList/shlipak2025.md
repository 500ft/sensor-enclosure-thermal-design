# Shlipak et al. (2025): Air-STORM — Solar-Powered Air Quality Sampler Enclosure Thermal Modelling

**Source:** https://doi.org/10.3390/s25154798  
**Evidence boundary:** Full text **and Supplementary Information** read 2026-09-22 (Europe PMC full-text XML plus the SI PDF). Archival open-access journal. **The strongest single source for this project's internal-dissipation axis.**

## Sensors

Bare-end K-type thermocouples (OMEGABOND 300) on inner walls, battery surfaces and at the internal air centre, logged by Raspberry Pi 4 at 5-10 s. Ambient reference: Davis Vantage Pro2 weather station with solar sensor, ~1-1.5 m away, 5 min. No stated uncertainty for either.

### Pros

- One month of continuous rooftop data, 15 min averages, four enclosures compared side by side.
- Ships an open-source finite-difference 3-D thermal model, so the result is reproducible.

### Cons

- Reference instruments carry no stated uncertainty.
- Purpose is **instrument survival** (operating limits, battery over-temperature), not measurement bias: it reports no RH, no PM and no gas error.

## Physical Box, Materials, and Geometry

Four enclosures: aluminium (7.6 cm cube), fiberglass-reinforced polyester (40.6 x 40.6 x 20.3 cm), ABS (20.3 x 15.2 x 10.2 cm), and **a commercial PurpleAir enclosure (10.2 cm PVC endcap)**.

### Pros

- **Measured internal-vs-ambient elevation for a real PurpleAir enclosure: MB = +1.88 degC, RMSE = 2.84 degC, R^2 = 0.86, and +6.48 degC at daily maximum.** ABS +3.72, FRP +1.78, aluminium +3.43; daily-max biases reach -12.89 degC for aluminium. Predicting daily maximum from ambient alone gives "mean errors and biases exceeding 10 degC".
- **The most informative source on the solar/self-heating split, though it does not identify it:** "at night, simulated temperatures, ambient temperatures, and observed temperatures are nearly identical", with the largest deviation under variable solar. Internal heat generation and material emissivity are identified as the two dominant model uncertainties, with a per-watt sensitivity analysis.
- **Directly supports lumped-capacitance modelling:** internal air, wall and battery temperatures agreed within **0.25 degC even at peak solar loading**.
- Finds internal fans largely ineffective and potentially net-heating: "Bulk airflow on the inside of the sampler is generally an ineffective method of cooling."

### Cons

- **Internal heat generation is ESTIMATED from rated electrical input as an upper bound, never measured** — the authors state so explicitly. SI Table S1 lists 19 monitors (0.45 W Clarity Node to 480 W TEOM; "typical low-cost sensors consume between 1 and 5 W"); **PurpleAir is not in that table and has no wattage anywhere in the paper.**
- The internal dissipation of the four validation enclosures is not stated in the main comparison, so the PVC +1.88 degC cannot be decomposed into solar versus electronics.
- Model error grows for conductive enclosures (aluminium RMSE 3.50 degC) because radial conduction between sides is neglected.

## Selection Lessons for This Project

- Cite for: the measured PurpleAir-enclosure elevation (+1.88 degC mean, +6.48 degC daily max); the **1-5 W typical dissipation bracket** with SI Table S1; the internal air ~ wall ~ battery agreement within 0.25 degC (which justifies the lumped model); the ineffectiveness of internal fans; and the night-time convergence to ambient **as an observation about the combined heat balance only**.
  **Corrected 2026-09-24:** this entry previously offered that convergence as evidence that *solar
  dominates*. That inference is invalid — outward long-wave loss can exactly offset electronics
  heating, so near-zero night bias does not imply near-zero dissipation. (Verified counterexample in
  this repo's own model: `Q = 0.102972 W` returns a night bias of `-1.2e-8 °C`.) Causal attribution
  requires a controlled power intervention.
- Do **not** cite it as having *measured* watts (it estimated them from rated input, upper bound), for RH/PM/gas error, or to attribute the PVC +1.88 degC solely to self-heating.
