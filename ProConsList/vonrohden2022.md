# von Rohden et al. (2022): Laboratory Radiation-Error Characterisation of the RS41

**Source:** https://doi.org/10.5194/amt-15-383-2022  
**Evidence boundary:** Full text read 2026-09-22. Laboratory wind-tunnel characterisation of a bare radiosonde sensor; the nearest heat-transfer treatment of ventilation-speed dependence, but not an enclosure.

## Sensors

Vaisala RS41 temperature sensor and boom (housing removed); four upstream reference thermistors (models not given; up to 0.5 K inhomogeneity); Kipp & Zonen CMP21; 2-D laser Doppler anemometry.

### Pros

- Clean separation of the three drivers (irradiance, density/pressure, ventilation speed) with a traceable uncertainty budget; parameterisation uncertainty < 0.2 K (k = 2) at realistic ventilation.
- ΔT is linear in irradiance, so one flux level per (p, v) scales to any modelled flux.

### Cons

- One unit characterised; sensor-to-sensor spread not studied.
- The largest uncertainty term is ventilation speed (0.5 m/s).

## Physical Box, Materials, and Geometry

No enclosure: boom at 45° to flow, sonde rotated at 16 s, incidence 0–90° plus a diffuse configuration. Sensor and boom materials not reported. Chamber: quartz tube 180 mm × 1 m, 3–1020 hPa, 0–7 m/s, 2500 W Xe lamp.

### Pros

- Conductive coupling between illuminated boom and sensor is deliberately included in the experiment.
- Independent field check against the manufacturer correction over 154 daytime soundings.

### Cons

- **Fitted on the built object** (2-D polynomial in p⁻¹ᐟ² and v⁻¹ᐟ²), then applied as a forward correction; the paper explicitly prefers this to heat-balance theory because of material-property assumptions.
- No vents, no internal dissipation; the dominant pressure effects are irrelevant to ground enclosures.

## Selection Lessons for This Project

- Supports a lab step-response protocol (shutter open/close, exponential fit) and testing ΔT ∝ v⁻ᵇ with b ≈ 0.3–0.65 and ΔT linear in irradiance.
- Cannot justify predicting enclosure bias before build, or any statement about vented boxes or self-heating.
