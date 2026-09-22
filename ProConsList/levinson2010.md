# Levinson et al. (2010): Measuring Solar Reflectance, Part I

**Source:** https://doi.org/10.1016/j.solener.2010.04.018  
**Evidence boundary:** Full text read 2026-09-22 **as the LBNL author manuscript**; pagination differs from the version of record. Archival journal. **Reports no absorptance for any plastic - its value is in establishing what a quoted alpha means.**

## Sensors

Not applicable to the authors' own analysis (numerical, using generated solar spectral irradiances). It characterises three instrument classes by reference: pyranometer (ASTM E1918-06), spectrophotometer with integrating sphere (ASTM E903), and portable Solar Spectrum Reflectometer (ASTM C1549) - **the latter two limited to incidence angles <= 20 deg**.

### Pros

- Gives a defensible way to *state* an absorptance: name the standard and the spectrum rather than quoting a bare number.
- Documents the standards' current status (E891 withdrawn 1999; E903-06 withdrawn 2005 but still referenced by CRRC, Energy Star and ASHRAE 90.1/90.2).

### Cons

- **Purely computational**: the agreement figures are model-to-model, not an instrument round-robin.
- Tuned to roofs and pavements at slope <= 23 deg and mainland-US latitudes; a vertical or arbitrarily oriented small enclosure face is outside the analysed configurations.

## Physical Box, Materials, and Geometry

Not applicable - roofs and pavements, analysed numerically.

### Pros

- **Establishes that "solar absorptance" is not a single well-defined number:** it depends on the assumed incident spectrum. For a nonselective black glossy surface, measured reflectance is 0.04 under E903/C1549 but 0.045 (AM1GH), 0.06 (AM1.5GH) and 0.09 (AM2GH) - a spread of 0.05.
- **Supplies a directly usable sensitivity: 0.6 K of surface temperature per 10 W/m^2 of solar heat gain**, which converts an absorptance error straight into a self-heating bias. The widely used E891BN metric can underestimate annual peak solar heat gain by up to 89 W/m^2, i.e. peak surface temperature by up to 5 K.
- Over 99 % of AM1GH sunlight arrives in 300-2500 nm - the band any alpha measurement must cover.

### Cons

- **Reports no measured absorptance for any plastic, paint or enclosure material**, so it cannot by itself justify 0.90 or 0.30.

## Selection Lessons for This Project

- Cite for: the standards chain (E903, C1549, E1918, G173, G197) and their status; the spectrum-dependence of solar reflectance with the worked black-surface example; and the **0.6 K per 10 W/m^2** sensitivity.
- Do **not** cite it for any specific absorptance value, for plastics, or for surfaces at steep tilt or outside 49 S-49 N.
