# Jayaratne et al. (2018): Influence of Humidity on a Low-Cost Air Particle Mass Sensor

**Source:** https://doi.org/10.5194/amt-11-4883-2018  
**Evidence boundary:** Full text read 2026-09-22 (publisher PDF). Archival open-access journal. Chamber plus 24-day field study. **This is the PM-error-per-RH source; it does not address enclosures at all.**

## Sensors

Plantower **PMS1003** (same family as the PMS5003 in PurpleAir), n = 1 per experiment. References: TSI 8530 DustTrak DRX (pre-calibrated against a TEOM to within 10 %), TSI 7545 IAQ meter for chamber RH, two TEOMs in the field, nephelometer as fog indicator. **No numeric uncertainty stated for any reference.**

### Pros

- Controlled chamber with true PM2.5 held at 10 +/- 1 ug/m^3, so the observed rise is unambiguously artefact.
- Field confirmation over 24 continuous days against TEOMs.

### Cons

- **PMS1003, not the PMS5003** used in PurpleAir; transferring the coefficient across models is an assumption the paper does not license.
- n = 1 sensor; the group's own screening notes unit CV ~0.07.
- The field TEOM is itself humidity-affected ("did not remove all of the liquid portion of the aerosols"), so the field baseline moves.

## Physical Box, Materials, and Geometry

Field housing was a sealed weather-proof box 150 x 120 x 100 mm drawing ambient air through an aperture via the sensor's own fan. Enclosure thermal effects are not studied.

### Pros

- **The usable transfer function:** PM2.5 response is flat until about **78 % RH**, then rises from ~9 to ~16 ug/m^3 by 89 % RH — an increase of almost 80 % at constant true concentration. Hysteresis: no significant reduction until RH falls to about 50 %.
- Mechanism is evidenced, not assumed: particle number in the 0.3-0.5 um bin rose only ~10 % while PM2.5 rose ~80 %, indicating growth of existing particles by water absorption rather than new droplet formation.
- Fog result: PMS1003 read +46 % against a reference +31 %.

### Cons

- The paper reports endpoints and a percentage, **not a per-%RH slope**; any linear coefficient is derived arithmetic, not the paper's value.
- Nothing about internal RH, enclosures, or self-heating.

## Selection Lessons for This Project

- Cite for: the magnitude, **~78 % threshold** and ~50 % hysteresis floor of the RH-driven PM2.5 artefact in a Plantower sensor, and the fog comparison — i.e. to bound how much PM error a given RH error can produce.
- Do **not** state it measured a PMS5003 or a PurpleAir, attribute a per-%RH linear coefficient to it, or cite it for enclosure/internal-RH effects. **Note the consequence for this project:** because a PurpleAir's internal RH reads ~10-24 points dry, a correction keyed to internal RH can place a genuinely humid ambient below this paper's 78 % threshold — an inference of this project's, not of the paper.
