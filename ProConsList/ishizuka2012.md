# Ishizuka et al. (2012): Natural Air Cooling of Electronics Casings — Outlet Vent Effects

**Source:** https://doi.org/10.1088/1742-6596/395/1/012122  
**Evidence boundary:** Full text read 2026-09-22. **Peer-reviewed conference proceedings** (Eurotherm 2012, IOP J. Phys.: Conf. Ser.), not an archival journal; its archival antecedents (Ishizuka et al. 1987 ASME J. Heat Transfer; 2002 Proc. IMechE A) were not read. Indoor still-air experiment with an internal heater — the only checked source coupling internal power to vent geometry.

## Sensors

Fourteen calibrated K-type thermocouples (0.1 mm, ±0.1 K): nine interior, four wall, one room. Wire heater 1.6 mm dia, 6–40 W.

### Pros

- Clean parametric sweep: six outlet porosities, three outlet heights, three heater heights, several powers.

### Cons

- No uncertainty analysis beyond thermocouple ±0.1 K; durations not reported.

## Physical Box, Materials, and Geometry

Casing 220 × 230 × 310 mm; wall 10 mm plastic with reported k = 0.01 W/mK (quoted as printed); bottom inlet 150 × 130 mm; single side outlet, reference 150 × 50 mm, six porosities, centre heights 275/200/150 mm; heater heights 25/125/225 mm.

### Pros

- Explicit two-path energy balance: closed-box wall loss Qs = 0.445·ΔTm¹·²⁵ (natural-convection exponent) plus vent heat carried by a buoyancy–resistance chimney balance.
- Vent effect collapses onto X = Re·β²/(1−β) with flow-resistance K = 0.4·X⁻¹·⁵; outlet-to-heater distance acts as chimney height.
- Provides a pre-fabrication design equation set (Eqs 1–4 from prior work).

### Cons

- **The new correlation is fitted after the fact** and its prefactor is stated to be "inherent in this apparatus and not a general value."
- No wind or solar; no bridge to outdoor shelter physics; wall conductivity value is unusual and should not be reinterpreted.
- Authors: "A more detailed discussion requires 3-dimensional thermo-fluid analysis."

## Selection Lessons for This Project

- Supports testing internal ΔT ∝ Q⁰·⁸ in the sealed limit, and the vent parameter β²/(1−β) and outlet-to-source height as design levers — the basis for this project's `Re_vent` / `A_vent/A_surface` groups.
- Cannot justify quantitative pre-build prediction with its constants, or any claim under wind or solar loading.
