# Kocar et al. (2024): Mechanical Properties and Color Changes of 3D-Printed Parts After Aging

**Source:** https://doi.org/10.3390/ma17235908  
**Evidence boundary:** Full text read 2026-09-22 (publisher full text, PMC11643522). Archival open-access journal. **Accelerated chamber exposure, not outdoor weathering.** No k, no alpha, no eps measured.

## Sensors

QUV accelerated weathering tester per **ISO 4892-3**, 432 h, 50 degC, cycle 8 h UV then spray; colorimetry in CIELAB; universal testing machine (ASTM D638/D790); Shore D durometer. **No uncertainty budget on Delta-E.**

### Pros

- Named standard exposure with cycle, temperature, humidity and dose (50 MJ/m^2) all stated.
- Colour, infill ratio and ageing crossed in one design, with both optical and mechanical outcomes.

### Cons

- **Accelerated chamber exposure with no natural-exposure correlation**, so real deployment lifetimes cannot be inferred.
- Only PLA in three warm colours (yellow/orange/red) - no white, black or grey, which is what an enclosure would actually use.
- Some mechanical results are non-monotonic and unexplained (yellow 100 % infill *gained* 6.9 % UTS).

## Physical Box, Materials, and Geometry

Filameon PLA, Creality Ender 3S-1, infill 20/60/100 %, 0.2 mm layers, 0.4 mm nozzle.

### Pros

- **Measured colour drift after 432 h at 100 % infill: Delta-E\* = 3.04 (yellow), 4.95 (orange), 6.14 (red)** - so a surface optical property assigned at t = 0 is **not stable over a deployment**.
- **Low-infill parts drift and degrade markedly more** than solid ones, both optically and mechanically (e.g. yellow 60 % infill UTS 22.69 -> 8.23 MPa).

### Cons

- The paper quantifies the **colour shift, not the resulting change in solar absorptance**. Delta-E\* must not be converted into an alpha change.
- Notes only qualitatively that red samples reach higher surface temperatures than yellow.

## Selection Lessons for This Project

- Cite for: "printed PLA colour measurably drifts under standardised UV + moisture exposure (Delta-E\* 3.0-6.1 in 432 h), and low-infill parts drift and degrade more" - i.e. an `alpha` registered at build time needs a re-inspection route.
- Do **not** cite it as evidence about outdoor deployment lifetime, and do **not** derive any alpha or eps change from Delta-E\*.
