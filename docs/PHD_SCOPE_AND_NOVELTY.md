# PhD scope & novelty gate — 2026-09-16

**Purpose.** Resolve, before investing in Studies B–D, the question the proposal itself flags as
exposed: is a dimensionless-collapse prediction of enclosure sensor bias a **PhD-scale open axis**,
or an **MS-scale design study**? This document records the novelty check, the Study A theory result,
the honest verdict, and the narrowed framing that reaches PhD scale.

## 1. Novelty verdict: **borderline — PhD only if narrowed**

A literature check (2015–2026, cross-checked against the repo's 26-source matrix) found:

**Established (not novel):**
- Radiation-shield/screen error and its wind + shortwave dependence — Nakamura & Mahrt 2005 (JTECH
  22:1046), empirical correction to ~0.13 °C RMSE; worst case low-wind + high-irradiance.
- Standard test methods already in the matrix: WMO No.8, Duvall 2021 (EPA 30-day protocol),
  ASTM D8406-22, CEN/TS 17660-1:2021.
- **Energy-balance shelter models already reduce error to a few coefficients** — Barbaresco et al.
  2019 (*Climate* 7(2):26): the direct methodological competitor.
- CFD-fitted per-geometry correction curves — repo's Liu 2023, Jin 2026.
- Low-cost AQ enclosure self-heating T/RH bias (~2.6 °C) — Barkjohn 2021, Cha 2024 (*Atmosphere*
  15:415) — documented and empirically corrected post-hoc.
- Dimensionless heat-transfer framework (Biot/Nusselt/Reynolds) — textbook.

**Open / under-addressed:**
- **No published dimensionless COLLAPSE of enclosure bias onto a-priori groups across
  geometry + material + ventilation + wind + irradiance simultaneously.** Existing models are
  empirical met-variable regressions (Nakamura–Mahrt), per-shelter coefficients fitted *after
  building* (Barbaresco), or single-geometry CFD curves (Liu/Jin).
- **Internal-dissipation ratio as a design axis** — classical shields have ~no internal power; AQ
  enclosures have watts. No source combines self-heating + vent geometry + surface optics in one
  predictive scaling.
- **Predict-before-build** — no validated forward model from material/finish/vent geometry to bias
  prior to fabrication.
- **3D-print-specific effects** (filament, finish, layer-induced emissivity; and low-k wall
  conduction — see Study A Biot gate) tied to a scaling model.

**Why borderline:** the *method* (similarity collapse) and the *internal-dissipation + predict-
before-build* framing are genuinely under-addressed, but every underlying phenomenon is established,
so novelty lives in **synthesis + method**, not new physics. Two substantive risks the proposer must
own: (1) radiation-dominated, low-Reynolds, buoyancy-mixed geometries may not nondimensionalise as
tidily as forced-convection Nu–Re; (2) Study A already shows the collapse is **not universal**
(kill criterion tripped in the radiation-dominated tail).

## 2. Study A result (done) — the collapse is real but bounded

See [studyA_nondimensional.md](studyA_nondimensional.md). The lumped model reduces exactly to five
groups (`Pi_G, N_Q, N_r, f_sky, Pi_d`); the closed form predicts the full nonlinear solver to
**~0.23 °C / 2–4% median** but the **p95 relative residual (12–64%) trips the preregistered ~3%
kill criterion** — the collapse holds in the solar-driven regime and **fails in the radiation-
dominated / near-zero-bias regime.** The Biot gate shows printed polymers (`Bi ~ 0.1–0.6`) violate
the isothermal-wall assumption that classical metal-screen physics relies on.

**Consequence for scope:** "bias always collapses onto a few groups" is falsified for the general
case. The defensible contribution is **the collapse domain and its boundary** — where prediction-
before-build works, where it fails, and why.

## 3. The narrowing that reaches PhD scale

Drop general shield physics. Anchor on the one axis meteorology never modelled:

> **Can an internal-dissipation ratio (self-heat vs solar load) together with a vent-Reynolds /
> vent-to-surface area-ratio group and a wall-Biot group predict the onboard-T/RH bias of a
> low-cost 3D-printed air-quality-sensor enclosure — and its downstream PM/gas calibration error —
> *before fabrication*, and where does that prediction break down?**

Three requirements to be PhD, not MS (all from the novelty check):
1. **Experimental**, not simulated only — a designed set of printed material/finish/vent variants.
2. Carries the **internal-dissipation, vent-Re, and wall-Biot** axes shield work omits.
3. **Maps where the collapse fails** (radiation-dominated regime) rather than assuming universality.

If the experimental collapse cannot beat Barbaresco's post-build coefficients on *prediction*, this
is honestly an MS design/ranking study and should be presented as such.

## 4. Reframed studies

| Study | What | Status |
|---|---|---|
| **A** | Nondimensional reduction + collapse test on the model | **Done** — regime-dependent; kill criterion tripped for universal claim |
| **B** | DOE over the model + CHT (`chtMultiRegionFoam`) on a subset with mesh-convergence; **add wall conduction (Biot) and resolved vent flow** the lumped model omits | Analytical DOE runnable now; CHT needs toolchain (FEA stub) — Owner/allocation gated |
| **C** | Pilot: 3 printed enclosures (**varied material/finish/vent**, instrumented for internal T + self-heat power), 1 reference, 2 weeks, through the committed intake gate + rehearsal; **Study-A prediction recorded before deployment** | Physical — PI/permission/hardware gated |
| **D** | Decisive: full material/finish/vent-ratio DOE, environmental-chamber control of wind + irradiance, two climates (adds the radiation-nonlinearity group) | Funded — chamber time + sensors |

## 5. Literature-matrix gaps to close (novelty defense)

The 26-source matrix is missing the sources this specific question must argue against. Add, with
full ProConsList assessments (currently characterised at abstract level only — **full reads
pending**, do not cite as assessed until read):

1. **Barbaresco et al. 2019, *Climate* 7(2):26** — the direct methodological competitor (energy-
   balance shelter coefficients). *Highest priority.*
2. **Nakamura & Mahrt 2005, JTECH 22:1046** — the canonical wind/shortwave shield-error correction.
3. **GRUAN RS41 radiation error, AMT 15:383 (2022)** — nearest heat-transfer/ventilation-speed
   treatment (bare sensor).
4. **Barkjohn 2021 / Cha 2024 (*Atmosphere* 15:415)** — the PurpleAir self-heating T/RH bias the
   thesis rests on.
5. **Vented-enclosure / electronics-cooling** (A_in/A_out optimum, buoyancy-driven vent flow) — the
   engineering base for the vent-Re / area-ratio axis.

## 6. What is unchanged

No physical data, permission, or PI approval is created by this analysis. `EN-S02`, `EN-R03`,
`EN-S09B`, `EN-S11` stay blocked; CAD deferred; FEA a stub. Studies C/D remain conditional on the
same external gates. This document is a scoping decision aid, not authority to run an experiment or
claim a validated framework. **Do not claim a "framework across sensing systems" — Study A has
already shown the collapse is not universal.**
