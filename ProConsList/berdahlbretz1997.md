# Berdahl and Bretz (1997): Solar Reflectance of Cool Roofing Materials

**Source:** https://doi.org/10.1016/S0378-7788(96)01004-3  
**Evidence boundary:** Full text read 2026-09-22 (the eScholarship deposit LBNL-41294 contains the Elsevier typeset reprint, i.e. the version of record). Archival journal. **Closest published analogue to this project's lumped model: same linearized form, same three unknowns.**

## Sensors

Perkin-Elmer Lambda 9 UV/VIS/NIR spectrophotometer with Labsphere integrating sphere, 5 nm steps, 8 deg incidence, NIST-traceable Spectralon reference; portable emissometer (**emittance accurate to about +/-0.05**); thermocouples under 10 cm samples; IR thermography.

### Pros

- Both ends of this project's absorptance range measured on one instrument chain with a traceable reference.
- Uses and validates the **same linearized lumped model**, including a numeric **h_r = 5.5 W/m^2K at eps = 0.9**, which this project can cite for its radiative linearization.

### Cons

- **Roofing materials, not plastics:** no polymer enclosure, no printed surface, no painted-plastic sample. The "eps about 0.9 for most building materials" claim is asserted, not tabulated per material.
- Emittance accuracy +/-0.05 is too coarse to justify 0.90 over 0.85 or 0.95.
- Outdoor h_c values are **inferred from a regression slope with no wind measurement**, on 10 cm samples the authors show suffer a **+4 degC edge-effect artefact** - indicative magnitudes, not a validated correlation.
- The authors disclaim Table 1 for precise product comparison (coating thickness and substrate varied).

## Physical Box, Materials, and Geometry

White acrylic coatings, asphalt shingles, black acrylic paint, clay tile, galvanized steel; 10 cm square outdoor samples on foam.

### Pros

- **Measured solar absorptance:** black acrylic paint **0.95**; black asphalt shingle **0.95**; white roof coatings **alpha = 0.15-0.26**; "white" asphalt shingle **0.79**. Galvanized steel absorptance above 0.6 with emittance ~0.1: "nearly as hot as black".
- Warns that visible reflectance misleads: a white acrylic over 90 % visible-reflective is only **83 % solar**-reflective, because the solar spectrum is 49 % near-infrared.
- **States the cross-cutting uncertainty finding this project needs:** a 10 % error in (h_r + h_c) gives a 10 % error in (T_surface - T_air), and "knowledge of (h_r + h_c) with an accuracy of ten percent is not feasible because of the large uncertainty in the convection coefficient h_c" - "even sophisticated computer simulations of roof temperature also suffer from this same difficulty."
- Outdoor-inferred h_c ~18 W/m^2K (November) and ~25 (July); cited zero-wind estimates of 2.6 and 6.6 bracket this project's 5.0 floor.

### Cons

- **Measured black at 0.95 means this project's alpha = 0.90 under-predicts** absorbed solar for a genuinely black finish - the non-conservative direction for a self-heating model.
- Measured new white coatings at 0.15-0.26 mean **alpha = 0.30 over-predicts** for a good white - though it is defensible as a conservative allowance for a rough or soiled one (white shingle measured 0.79).

## Selection Lessons for This Project

- Cite for: measured solar absorptance of white coatings and black paints/shingles; the eps ~0.9 rule of thumb for non-metallic building surfaces **with its +/-0.05**; `h_r = 5.5 W/m^2K at eps = 0.9`; and the statement that **h_c dominates the uncertainty**.
- Do **not** cite for plastic or printed emissivity, for a wind-dependent h correlation, or as precise product data.
