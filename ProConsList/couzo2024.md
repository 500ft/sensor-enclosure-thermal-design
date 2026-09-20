# Couzo, Valencia and Gittis (2024): PurpleAir Temperature and RH Evaluation

**Source:** https://doi.org/10.3390/atmos15040415  
**Evidence boundary:** Full text read 2026-09-22 (deposited PDF carries revision markup on pp. 3–7; numbers cross-checked against the clean tables). Single-unit, single-site co-location; **the primary source for the low-cost AQ enclosure T/RH bias magnitude**. Note: an earlier abstract-level scan in this repository mis-cited this as "Cha et al."

## Sensors

One PurpleAir PA-II (Bosch BME280; two PMS-5003; WiFi; microSD) vs Campbell Scientific 107 temperature and Vaisala HMP45C RH probes at the NC ECONet UNCA tower.

### Pros

- 148,230 time-paired 5-min records over 553 days; PA completeness 91.4 %.
- Bias reported by ambient-temperature bin: +1.8 (≤ −5 °C) → +4.2 °C (> 25 °C); RH bias −17.4 %, worst at 80–100 % RH.
- Tests the vendor's constant offsets directly (−4.4 °C over-corrects to −1.9 °C bias).

### Cons

- n = 1 sensor; reproducibility across units not established.
- No wind, solar or power covariates, so self-heating cannot be separated from radiative loading.
- Reference probe uncertainties and shielding not stated; 1 m height offset uncorrected.

## Physical Box, Materials, and Geometry

White plastic shell 85 × 85 × 125 mm, open at the bottom; shell material/thickness not reported; PA at 3 m, references at 2 m.

### Pros

- Headline: temperature bias **+2.6 °C** (RMSE 2.8 °C, r = 0.99), 91 % of points high; linear correction (slope 1.07, intercept 1.60) reduces RMSE to 1.0 °C.

### Cons

- Cause is attributed by statement ("excess heat produced by the sensor's electronics"; vendor blames the WiFi module) — no wattage measured or modelled.
- No vent, wall or optical description beyond "white" and "open on the bottom."

## Selection Lessons for This Project

- Supports +2.6 °C (1.8–4.2 °C by ambient bin) and −17.4 % RH as the empirical magnitude of a small, bottom-open, internally powered plastic enclosure's bias, and a bias that grows with ambient temperature.
- Cannot justify attributing the whole bias to WiFi heat, any vent-flow relationship, or pre-fabrication prediction.
