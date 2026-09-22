# Barreira et al. (2021): Emissivity of Building Materials for Infrared Measurements

**Source:** https://doi.org/10.3390/s21061961  
**Evidence boundary:** Full text read 2026-09-22 (open-access version of record). Archival journal. **The measured source for this project's `eps_surface = 0.90`: nine pigmented polymer film surfaces, the closest reachable match to a painted/printed plastic skin.**

## Sensors

Portable differential-thermopile emissometer per **ASTM C1371-04a** (**accuracy +/-0.02**, linearity +/-0.01, 10 s time constant); IR camera 320 x 240 px (+/-2 degC or +/-2 %) with the black-tape method per ASTM E1933-14; three measurements per material.

### Pros

- Two independent methods compared against each other and against literature values.
- Quantifies the consequence of a wrong emissivity **in kelvin**.

### Cons

- **Instrument accuracy (+/-0.02) is the same order as the discrepancy being argued about**, so the paper narrows but does not close the question.
- No spectral resolution, no directional emissivity for the tapes, no elevated temperature, no weathering.

## Physical Box, Materials, and Geometry

Nine commercial tapes (pigmented PVC/vinyl and coated cloth films) in five colours and two gloss levels; plus nine building materials.

### Pros

- **Measured emissivity of the polymer surfaces: 0.86-0.89** (A 0.88, B 0.87, C 0.87, D 0.87, E 0.88, F 0.89, G 0.86, H 0.89, I 0.89).
- **Colour barely affects emissivity** across four bright vinyl colours, and gloss has little impact (matte slightly higher) - this **empirically justifies using the same eps for both the dark and the light variant**, which this project's model assumes.
- Quantifies the cost of a wrong eps: surface-temperature differences of **1.3 degC on average** for non-metals, and **up to 7 degC** versus literature values.
- Moisture content changes emissivity by **more than 10 %**, visible even at low moisture - relevant to an outdoor enclosure.

### Cons

- **Nudges this project's value down:** the authors state directly that their results "point to lower values than those usually found in the literature (0.90 to 0.95)". A central value of ~0.87-0.88 matches measurement better than 0.90, though this project's stated 0.85-0.95 band does bracket them.
- Adhesive tapes, not moulded, painted or 3D-printed enclosure plastic; no printed or textured surface tested.

## Selection Lessons for This Project

- Cite for: measured emissivity of pigmented polymer surfaces (0.86-0.89, +/-0.02, ASTM C1371); the finding that colour and gloss barely change eps; the emissometer-vs-literature discrepancy; and the K-per-emissivity-error sensitivity.
- Do **not** cite for painted metal, 3D-printed or weathered plastic, spectral or directional emissivity, or elevated temperature.
