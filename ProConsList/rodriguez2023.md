# Rodriguez et al. (2023): Thermal Conductivity of FDM Materials with a DTC-25 Meter

**Source:** https://doi.org/10.3390/ma16237384  
**Evidence boundary:** Full text read 2026-09-22 (publisher PDF). Archival open-access journal. **Value here is as an independent cross-lab check on printed PLA and ABS.**

## Sensors

DTC-25 guarded heat flow bench (ASTM E1530), hot side 55 degC / cold side 2 degC, 0.3 MPa load; N = 6 tests per material; five factory calibration standards.

### Pros

- Independent lab and instrument, **same standard** as `tychaniczkwiecien2025` - gives a cross-lab reproducibility check.
- Per-sample measured geometry and print parameters fully reported; a dedicated limitations section.

### Cons

- **Uncertainty is large relative to the spread (+/-0.06 on 0.22 = +/-27 %)**, so PLA, ABS, PEEK, TPU and ULTEM are barely distinguishable.
- Measurement spans a 2-55 degC gradient, so each value is gradient-averaged, not isothermal at a stated temperature.
- **Anisotropy not reported**; the authors list heat-flow direction as an unaddressed variable.

## Physical Box, Materials, and Geometry

Seven FDM materials at **100 % density, rectilinear 45 deg**; 0.8 mm nozzle, 0.3 mm layers; circular samples ~50 mm diameter at ~5 and ~10 mm thickness.

### Pros

- **Measured: PLA3080 0.22 +/- 0.06; ABS 0.22 +/- 0.06**; TPU 0.26 +/- 0.05; PEEK 0.25 +/- 0.05; Al-filled PLA 0.40 +/- 0.05 W/mK.
- Printed PLA at 0.22 is ~1.7x the handbook 0.13, and printed ABS at 0.22 is ~1.3x the handbook 0.17 - **the third independent dataset pointing the same way**.

### Cons

- Only 100 % infill; no infill or orientation variable.

## Selection Lessons for This Project

- Cite as a **corroborating independent measurement** that printed PLA and ABS at 100 % infill sit near 0.2 W/mK.
- Do **not** cite its values as precise (the +/-0.06 swamps the material differences), or use it for direction or infill.
