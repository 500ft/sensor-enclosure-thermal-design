# Holder et al. (2020): Field Evaluation of Low-Cost PM Sensors for Wildfire Smoke

**Source:** https://doi.org/10.3390/s20174796  
**Evidence boundary:** Full text read 2026-09-22 via the publisher-deposited PMC copy (direct MDPI fetch blocked). Archival open-access journal. **This is one of the two origin papers behind the "2.7 to 5.3 °C" range that Barkjohn et al. 2021 quotes — Holder supplies the 5.3 °C / 24.3 % end. Holder reports a single value, not a range.**

## Sensors

PurpleAir PA-II-SD (2x Plantower PMS5003 + onboard T/RH under the PVC cap), Aeroqual AQY, SenSevere RAMP. PM reference: GRIMM EDM 180 (EPA FEM); fire sites Met One BAM 1020. **The temperature/RH reference instrument is never identified** — only "the ambient reference" — and carries no stated uncertainty.

### Pros

- Largest and longest PurpleAir T/RH dataset of the two origin papers: n = 5454 hourly pairs (temperature), 4654 (RH), Aug 2018 - Apr 2019.
- Full regression statistics tabulated (slope, intercept, R^2, NRMSE), not prose only.

### Cons

- **T/RH statistics come from only 2 sensors of each type**; unit-to-unit variability is uncharacterised.
- The T/RH reference is unnamed with no uncertainty, so the 5.23 degC figure carries an unquantified reference-side error.

## Physical Box, Materials, and Geometry

PurpleAir PVC cap with the meteorological sensor positioned above the particle sensors. Packages mounted in portable containers with pole mount, solar panel and battery.

### Pros

- **Measured PurpleAir bias: temperature MBE = 5.23 degC** (text rounds to 5.3), slope 0.9, R^2 0.91, NRMSE 34 %; **RH MBE = -24.30 %**, slope 0.57, R^2 0.84. Comparators: AQY +1.83 degC / -4.90 %; RAMP +1.36 degC / -4.10 %.
- Contains a discriminating signature the authors do not follow up: the PurpleAir bias is a near-constant offset, whereas the RAMP's is **diurnal** (+10 degC midday, 0 to -2 degC overnight; RH ~14 % low overnight, near-zero by day).

### Cons

- **Cause is asserted, not measured:** the bias is "likely due to the location of the temperature and RH sensor inside the PA case where it is heated from the sensor electronics." No wattage, no thermal experiment, no shaded or unpowered control.
- The paper's **only** quasi-empirical cause test (RAMP, rainy vs cloudy days) concluded the opposite mechanism: "possible that the higher measured temperature is partly due to radiant heating from the sun."
- Including T and RH terms in the smoke correction "did not improve the r^2 or the MAE or NRMSE" — so no downstream PM benefit was demonstrated here (RH was typically below 60 % near fires).

## Selection Lessons for This Project

- Cite for: the measured PurpleAir onboard bias (+5.23 degC, -24.30 %) and the operational conclusion that PA T/RH must be read as an **internal**, not ambient, measurement; and for the RAMP diurnal signature as evidence of solar-driven bias.
- Do **not** cite as evidence that electronics self-heating causes the PurpleAir bias — the paper says "likely", measures nothing about it, and its only cause-probing experiment found sun. Do **not** cite it for a bias *range*.
