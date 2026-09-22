# Baraboi et al. (2026): Heat Transfer Through 3D-Printed Plates

**Source:** https://doi.org/10.3390/ma19132793  
**Evidence boundary:** Full text read 2026-09-22 (publisher PDF). Archival open-access journal. **Highest-credibility single number per material: guarded hot plate under ASTM C177 / EN 12667 / EN 12939 with a k=2 uncertainty budget.**

## Sensors

Feutron 4110 guarded hot plate, steady state ~25-27 degC, three independent repeats per sample. Heat flux uncertainty +/-0.5 %; **expanded uncertainty (k=2) +/-3.2 % to +/-4.8 %**.

### Pros

- Most authoritative standard set of any source here, with an explicit k=2 budget.
- Print parameters fully reported, including build orientation and the heat-flow-vs-layer geometry.

### Cons

- Only 100 % infill (plus one deliberately foamed variant); no infill sweep.
- One mean temperature only (~25-27 degC); no temperature dependence.
- 10 mm specimens at 200x200 mm; a 3 mm enclosure wall has a different perimeter/infill ratio and void population.

## Physical Box, Materials, and Geometry

Bambu Lab A1 FDM, 0.4 mm nozzle, 0.12 mm layers, **100 % rectilinear infill, 10 wall loops, +/-45 deg cross-ply**, printed flat so **layer deposition is perpendicular to heat flow** (stated explicitly).

### Pros

- **Measured through-thickness lambda_eff:** PLA Basic **0.267 +/- 0.011**; PETG **0.290 +/- 0.012**; PLA Aero (foaming) **0.114 +/- 0.005**; PET-CF 0.533 +/- 0.021 W/mK.
- **PETG at 0.290 essentially confirms the handbook 0.29** - by this measurement the PETG value this project used is defensible.
- PLA Aero at 0.114 shows a foaming filament drives printed wall k *below* any handbook value - a real design lever that makes Bi worse.

### Cons

- **PLA at 0.267 is ~2.05x the handbook 0.13 this project used** - the single strongest evidence that the PLA handbook value is wrong for printed parts.
- The authors explicitly forbid anisotropy conclusions: "no in-plane measurements were performed in this study; thus, conclusions regarding distinct anisotropic ratios remain hypothetical."

## Selection Lessons for This Project

- Cite for: guarded-hot-plate through-thickness lambda_eff of printed PLA and PETG at 100 % infill with a named standard and k=2 uncertainty.
- Do **not** cite for anisotropy (the authors forbid it), infill dependence, or temperature dependence.
