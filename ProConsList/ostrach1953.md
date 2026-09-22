# Ostrach (1953): Laminar Free Convection About a Flat Plate (NACA Report 1111)

**Source:** https://ntrs.nasa.gov/api/citations/19930092147/downloads/19930092147.pdf  
**Evidence boundary:** Full text read 2026-09-22 (OCR lossy; summary p. 63 and results p. 72 confirmed by visual page render). **Venue flag: government technical report (NACA Report, committee-reviewed archival tier) — not a journal.** Geometry is an **external flat plate in an infinite medium, not an enclosure.**

## Sensors

Not applicable: analytical/numerical study. Reports comparison against prior experiments (air, oil, mercury).

### Pros

- Free, permanent, citable URL; every number is verifiable by a reader.
- Similarity reduction of free convection to two coupled ODEs, "analogous to Prandtl's forced-flow boundary-layer theory".

### Cons

- 1953 numerics; the semiempirical correlations it quotes have been superseded.
- Laminar throughout; no Rayleigh regime map (no laminar/transition/turbulent boundaries).

## Physical Box, Materials, and Geometry

Flat plate parallel to the body force, constant plate temperature, constant body force, infinite medium. Profiles computed for Pr = 0.01 to 1000. Reports `Nu_av = 0.548 [(Pr)(Gr)]^(1/4)` for air and the local form `Nu = 0.411 [(Pr)(Gr_X)]^(1/4)`.

### Pros

- **"The type of flow is found to be dependent on the Grashof number alone"** (p. 63) — the textbook warrant that a buoyant regime is set by a single group.
- **Documented precedent for a regime-limited power law:** the common semiempirical relation "will yield good results only in restricted Prandtl number ranges" — very good near Pr ≈ 1, poor at small Pr. Structurally the same claim this project makes about its own collapse.
- States its Boussinesq-type assumption (small relative temperature difference) explicitly, which this project must mirror.

### Cons

- **Wrong geometry for the core need:** no enclosure, no cavity, no vent, no chimney/stack driving, no aspect ratio.
- Boundary-layer development carried out only for large Grashof number.
- Oil experiments deviate up to ~20 % from theory (viscosity variation with temperature, end effects) — constant-property assumption is fragile.

## Selection Lessons for This Project

- Cite for: the similarity reduction of free convection to Gr and Pr; "Grashof number alone determines the type of flow"; the small-relative-temperature-difference assumption; and the precedent that a quarter-power law holds in a restricted parameter range and degrades outside it.
- Do **not** cite for: enclosures, cavities, vents, chimney flow, turbulent natural convection, or Rayleigh regime boundaries. It is **not** a substitute for an enclosure-convection source.
