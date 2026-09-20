# Barkjohn et al. (2021): US-Wide PurpleAir PM2.5 Correction

**Source:** https://doi.org/10.5194/amt-14-4617-2021  
**Evidence boundary:** Full text read 2026-09-22. Large multi-site PM2.5 calibration study; **contains no own temperature or RH bias measurement** — the T/RH bias figures it quotes are secondhand (Holder et al. 2020; Malings et al. 2020). It is not a source for the +2.6 °C figure.

## Sensors

PurpleAir PA-II: two Plantower PMS5003 and one Bosch BME280 under a PVC cap; FRM/FEM PM2.5 references at regulatory sites. No reference thermometer or hygrometer.

### Pros

- 50 sensors, 39 sites, 16 states, ~12,000 24-h pairs; PM2.5 RMSE 8 → 3 µg/m³ with an RH term.
- Documents QC artefacts of the onboard T/RH channel (glitch values, missing-data rates).

### Cons

- 24-h averaging hides diurnal self-heating.
- T/RH bias (2.7–5.3 °C warm, 9.7–24.3 % dry) is quoted from other papers, not measured.

## Physical Box, Materials, and Geometry

PVC cap; BME280 "positioned above the particle sensors nestled under the PVC cap." Otherwise not reported.

### Pros

- States the mechanism qualitatively: "higher internal temperature caused by the small volume containing the electronics."

### Cons

- No geometry, vent, wall, optical or power information; not a thermal-design paper.

## Selection Lessons for This Project

- Supports only the qualitative claim that PurpleAir onboard T reads warm / RH reads dry and that PM corrections absorb it.
- Cannot justify the 2.6 °C number (see Couzo et al. 2024) or any thermal-design inference.
