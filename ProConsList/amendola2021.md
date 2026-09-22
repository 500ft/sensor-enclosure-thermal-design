# Amendola et al. (2021): Optical Characterization of 3D Printed PLA and ABS Filaments

**Source:** https://doi.org/10.1371/journal.pone.0253181  
**Evidence boundary:** Full text read 2026-09-22 (publisher PDF). Archival open-access journal. **Extinction spectra are presented in FIGURES ONLY - no tabulated values exist in the paper.** Numeric data are deposited at Zenodo (10.5281/zenodo.4736126); nothing numeric is quoted here.

## Sensors

Jasco V-570 UV/VIS/NIR spectrophotometer, **400-1300 nm**, 1 nm bandwidth, 2 nm pitch; screw micrometer for individual sheet thickness; XRD and digital microscopy for material characterisation. **No uncertainty budget for the spectra.**

### Pros

- 25 filaments (18 PLA, 7 ABS) across colours and brands, printed on one machine with fixed settings; every sheet thickness individually measured and tabulated.
- Data deposited openly, so spectra are recoverable if numbers are needed.

### Cons

- **No tabulated extinction values in the paper** - nothing may be quoted without pulling the Zenodo dataset.
- Band stops at 1300 nm; the solar spectrum runs to ~2500 nm, and the long-wave IR band relevant to emissivity is untouched.
- Sheets are 0.23-0.58 mm, 5-10x thinner than a 3 mm enclosure wall, so opacity conclusions do not transfer directly.

## Physical Box, Materials, and Geometry

Sharebot NG, 2 layers, 100 % rectilinear infill, 0.35 mm nozzle; sheets 20 x 20 mm, 0.23-0.58 mm thick. One white PLA additionally printed at six extruder temperatures.

### Pros

- **Two black PLA filaments of nominally the same colour from different producers gave "completely different spectral behaviour"** - XRD found CaCO3 in one only. Brand/filler, not colour, sets the optical behaviour.
- **Extruder temperature changes the spectra** (205 degC showed about half the attenuation at low wavelengths versus 190-215 degC).
- States directly that "the higher absorbance values are not always associated to the darker filaments".
- Demonstrates a real consequence: a probe printed from one black PLA leaked stray light and corrupted a fit (chi^2 2018 vs 1.21).

### Cons

- Neither solar absorptance nor thermal emissivity is measured.
- Optical only; no thermal property.

## Selection Lessons for This Project

- Cite for: "the shortwave optical behaviour of a printed wall is set by dye/filler/brand and print temperature, not by the base polymer, and thin printed sheets transmit in the 400-1300 nm band" - i.e. **a single alpha assigned by colour name is not defensible for a thin printed wall**, and a printed shell is not optically opaque the way a metal shield is.
- Do **not** quote any extinction number without the Zenodo data, and do **not** cite it for alpha or eps.
