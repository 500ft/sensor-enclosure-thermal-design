# Tychanicz-Kwiecien et al. (2025): Thermal Conductivity of Selected 3D-Printed Materials

**Source:** https://doi.org/10.3390/ma18173950  
**Evidence boundary:** Full text read 2026-09-22 (publisher PDF). Archival open-access journal. **Only source found that sweeps infill density AND pattern AND temperature for all three of this project's polymers under a named standard.**

## Sensors

Unitherm TM 2022 guarded heat flow meter (ASTM E1530): calibrated heat flux sensor, guard heaters, PID control. Three repeats per point; total uncertainty **+/-0.004 to +/-0.006 W/mK (~3 %)**.

### Pros

- Per-point uncertainty reported on every value.
- Single printer, single filament brand, single colour (black) - internally consistent comparison.

### Cons

- **Anisotropy not reported**; only one specimen orientation, and the layer orientation relative to heat flow is never stated.
- 8 mm discs with real infill cells are not geometrically comparable to a 2-3 mm enclosure wall, which is mostly perimeter shells.

## Physical Box, Materials, and Geometry

Zortrax PLA / PET-G / ABS, FFF, 0.4 mm nozzle, 0.15 mm layers, **infill 40/60/80/100 %**, honeycomb and grid patterns; discs 50.8 mm diameter x 8 mm.

### Pros

- **Measured k at 100 % infill (~22 degC):** PLA **0.182**, PET-G **0.198**, ABS **0.172** W/mK (each +/-0.006), rising modestly with temperature to ~50 degC.
- **Infill dependence quantified:** relative to 100 %, k falls ~10 % at 80 %, ~18 % at 60 %, ~30 % at 40 %. At 40 % grid: PLA 0.129, PET-G 0.131, ABS 0.118.
- Honeycomb consistently conducts more than grid at equal density.

### Cons

- **Contradicts the handbook value this project used for PLA:** printed PLA measures 0.182-0.202, i.e. **1.4-1.6x higher than the handbook 0.13**.
- PET-G measures 0.198-0.211, ~30 % **lower** than the handbook 0.29 - so the handbook set is not uniformly biased in one direction.

## Selection Lessons for This Project

- Cite for: measured k of printed PLA/PET-G/ABS at stated infill densities and temperatures, and the ~30 % drop from 100 % to 40 % infill.
- Do **not** cite for anisotropy, for through-thickness versus in-plane, or as a wall-conduction value for a thin printed wall.
