# Berdahl and Martin (1984): Emissivity of Clear Skies

**Source:** https://doi.org/10.1016/0038-092X(84)90144-0  
**Evidence boundary:** Full text read 2026-09-22 **as the LBL-15367 lab report (1982)**, which carries the full derivation; the Elsevier version of record is a 2-page technical note and was paywalled. Archival journal. **This is the measured basis for any clear-sky temperature depression - and it shows the depression is not a constant.**

## Sensors

LBL spectral sky radiometer (coated germanium lens) at zenith angles 0-80 deg, hemispherically weighted into a "pseudo-pyrgeometer"; a real pyrgeometer cross-calibrated monthly; ground-level dewpoint.

### Pros

- Genuinely measured: **30,835 half-hourly clear-sky observations, 57 months, 6 US sites**.
- Quotes an explicit **RMS deviation of 0.018** in emissivity - rare for constants of this kind.

### Cons

- Six southern-US, low-elevation sites; no high-altitude, high-latitude or maritime-tropical validation, and Gaithersburg already breaks the "universal curve" by 0.024.
- Fits **monthly averages**, so the 0.018 RMS is *not* the error on a single hour of enclosure data.
- Nothing about cloudy skies.

## Physical Box, Materials, and Geometry

Not applicable. Content: 24-hour-average clear-sky emissivity `eps = 0.711 + 0.56*(T_dp/100) + 0.73*(T_dp/100)^2` with **T_dp the near-ground dewpoint in degC**; diurnal correction `d_eps = 0.013*cos(2*pi*t/24)`; an equivalent Brunt form `eps = 0.564 + 0.059*sqrt(e)` agreeing to within 0.003.

### Pros

- Gives two functional forms so a project can use whichever input it actually has (dewpoint or vapour pressure).
- States where the universal-curve claim holds: midlatitude, below 1 km elevation, systematic deviation <= 0.02.

### Cons

- **Does not support this project's fixed `T_sky = T_air - 20 K`.** Over the paper's own stated validity range (T_dp -20 to +30 degC) the implied depression spans roughly **4 K to 34 K**; a fixed 20 K corresponds to T_dp ~8-12 degC, a mid-latitude moderately-humid special case. (That K-range is arithmetic derived from the paper's equation, not a number the paper states.)
- Validity stated only for T_dp in about [-20, +30] degC.

## Selection Lessons for This Project

- Cite for: the clear-sky emissivity correlation, its RMS scatter, and its dewpoint validity range - and as **the reason the model should take `T_sky` from dewpoint rather than a fixed offset**.
- Do **not** cite it for a fixed 20 K depression (it never states one), for cloudy-sky behaviour, for instantaneous accuracy, or outside midlatitude low elevation.
