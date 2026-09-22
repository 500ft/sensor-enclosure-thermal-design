# Janek and Hardon (2026): Directional Thermal Characterization of Anisotropic Polymers

**Source:** https://doi.org/10.3390/metrology6030048  
**Evidence boundary:** Full text read 2026-09-22 (publisher PDF). Archival open-access journal. **The load-bearing source for this project's Biot claim: the only one that resolves direction.**

## Sensors

Custom transient pulse method (0.200 s current pulse) on an asymmetric three-layer sandwich, inverse-solved with an implicit Crank-Nicolson 1-D model. 20x20 mm foil heater; two Amphenol MA 10 kOhm NTC thermistors; ADS1256 24-bit ADC at 10 Hz. **Full GUM-style budget: expanded (k=2) 10.7 % on lambda.**

### Pros

- Contact resistance and lateral spreading are quantified rather than assumed away.
- Validated against an isotropic reference standard (VUKOL N22, measured 0.2106 W/mK).

### Cons

- **No print parameters reported at all** - no printer, nozzle, layer height, raster angle or infill %. The result cannot be tied to a process window.
- Single material (ABS), single specimen set; specific heat c = 2000 J/(kg K) is **assumed**, not measured, and propagates directly into lambda.
- Custom, non-standardised apparatus validated against one reference only.

## Physical Box, Materials, and Geometry

FDM ABS specimens **cut in two directions from one printed block**, 1.5 mm thick (close to real wall scale); measured effective density 1040 kg/m^3, explicitly accounting for FDM micro-voids.

### Pros

- **Measured both directions:** transverse (heat flow **perpendicular to layer interfaces**, i.e. the direction a wall conducts) **lambda = 0.1039 W/mK**; axial (parallel to layers) **0.1664 W/mK**. **Anisotropy ratio A = 1.60.**
- The transverse value is **below every handbook value this project used** - at 3 mm it is the worst credible printed-ABS case for Bi.
- Bounds the anisotropy honestly: **1.6x, not an order of magnitude**, so ignoring direction in a 1-D wall model biases k high by at most ~60 %.

### Cons

- Its comparison to "Prajapati et al." ranges (0.10-0.12 through-plane, 0.15-0.20 in-plane) is **this paper's characterisation of a source not read here** - treat as secondary, not as a measurement.
- ABS only; does not extend to PLA or PETG.

## Selection Lessons for This Project

- Cite for: the measured in-plane versus through-thickness k of printed ABS and the **1.60 anisotropy ratio**, and for through-thickness printed ABS at ~0.10 W/mK.
- Do **not** cite it as a function of infill or raster angle (unreported), extend its ABS numbers to other polymers, or attribute the Prajapati ranges to Prajapati.
