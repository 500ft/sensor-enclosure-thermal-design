# Lopes et al. (2023): 3D Microstructure Pattern and Infill Density in PET-G

**Source:** https://doi.org/10.3390/polym15102268  
**Evidence boundary:** Full text read 2026-09-22 (publisher PDF). Archival open-access journal. **Only source resolving infill *pattern* at fixed density - and the effect is large.**

## Sensors

Heat flow method per ISO 9869-1:2014 in a hotbox built to ASTM C1363-11. greenTEG heat flux and temperature sensors. Temperature accuracy +/-0.1 K, heat flux +/-3 %. Validated in-line against an XPS plate (0.030 vs manufacturer 0.029-0.036 W/mK).

### Pros

- Method validated against a known reference within the same study.
- Building-scale standards applied correctly.

### Cons

- **No uncertainty reported on the conductivity values themselves** - only instrument accuracies.
- **Geometrically remote from this project:** 100 mm thick panels, 1.2 mm nozzle, 0.60 mm layer height. A 3 mm enclosure wall shares almost nothing with this build.

## Physical Box, Materials, and Geometry

PET-G, Builder Extreme 1500 Pro, 12 infill patterns at fixed **25 % density**; specimens 175 x 250 x 100 mm.

### Pros

- **Pattern alone moved k by 82 % at fixed volume fraction:** Concentric **0.057**, Hilbert 0.074, Gyroid 0.074, Rectilinear 0.083, Honeycomb 0.090, ... 3D Honeycomb **0.104** W/mK. Overall "up to 70 % variation in thermal performance".
- **This refutes a naive volume-fraction effective-medium correction:** density alone does not predict k.
- At low infill, effective through-wall k of printed PET-G collapses to **0.057-0.104**, i.e. 3-5x below the handbook 0.29 - if a wall is genuinely infilled rather than near-solid, Bi is far larger than this project claimed.

### Cons

- The 5-20 % infill results appear only as U-values in a figure; **no k values are recoverable**, and the trend is reported as counterintuitive and unexplained (lower density did *not* insulate better).
- Thermal anisotropy not measured (only mechanical tests were directional).

## Selection Lessons for This Project

- Cite for: "infill pattern, not just density, controls effective through-wall k, by up to ~70-80 % at fixed volume fraction", and for the low-infill PET-G k range.
- Do **not** cite its absolute numbers as applicable to a 3 mm wall, or as evidence that lower infill always insulates better - the paper found otherwise below 25 %.
