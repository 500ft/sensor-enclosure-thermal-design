# Study B — CHT design and dimensionless extension contract (W1/W2, 2026-09-23)

**Status: design document. No solver is installed, no geometry is modelled, no run was made.**
Per the weekly plan and its Section 9 CAD amendment. Authority: [`cad_fea_plan.md`](../../cad_fea_plan.md)
§3.1–3.3 (design), [`CAD_PLAN.md`](../../CAD_PLAN.md) and [`CAD_TASKS.csv`](../../CAD_TASKS.csv)
(work orders, all still **deferred**), [`studyA_nondimensional.md`](../../studyA_nondimensional.md)
(the lumped result this study extends), and the engineering-audit CAD briefing at
`500ft/engineering-audit@cf56cdf:docs/cad_agent_briefing.md` (verified methods; read in full
2026-09-23). Nothing here changes a deferred status or supplies a missing dimension.

## 1. The question Study B answers — and the one it cannot

Study A reduced the lumped model to five groups and showed the linear law holds in the solar-driven
regime (~0.1 °C median) and fails above ~20 °C. The lumped model **assumes an isothermal wall
(Bi ≪ 1) and replaces vent flow with an empirical pre-heat closure `Pi_delta`.** For printed
polymer walls Bi ≈ 0.1–0.6, so both assumptions are the open physics.

**SQ2 (Study B):** how do resolved wall conduction and resolved vent flow change the predicted
bias for printed polymer geometries, relative to the lumped model? Output = disagreement in °C,
regime-binned, with the mechanism attributed.

**Not answered by Study B:** whether either model matches reality. That is Study C. A converged
CHT solve is a *numerical* result and inherits every `bounded`/`TODO-from-lab` input.

## 2. Smallest useful CHT study

| Item | Specification | Evidence state |
|---|---|---|
| Geometry set | V0 dark closed box; V0P identical geometry, finish only; V1 passive vented shield | **all dimensions unresolved** — placeholders bound to the owner inventory (EN-CAD-02) |
| Materials | ≥1 printed polymer with registered `k` (route: datasheet range for the *specific* filament, or measured); high-`k` reference (aluminium) only if the owner approves the comparison | unresolved |
| Boundary conditions | solar flux on sun-facing faces (`alpha*G`, sweep 400–1000 W/m²); long-wave to sky (`eps`, `T_sky`) and to surroundings (`T_air`); external convection `h(U)` or resolved external flow; internal heat source `Q` (W, located at the electronics zone); vent openings as pressure-outlet/inlet or resolved; sensor location | inputs from `thermal_bias.ASSUMPTIONS`, versioned as the illustrative baseline |
| Solver modes | (a) **decoupled thermal-FEA** — solid conduction + radiation with `h` as a Robin BC: validates wall conduction/Biot, **cannot** validate vent flow; (b) **CHT** (`chtMultiRegionFoam` or Elmer) — solid + fluid coupled, buoyancy-driven internal flow: validates both. Run (a) first; (b) only on a subset | toolchain not installed; not authorised this week |
| Outputs | sensor-surface temperature; wall temperature gradient (inner–outer, at designated points); vent mass flow / velocity field; heat-flux balance by surface; **ΔT relative to the lumped model** | — |

## 3. Validation hierarchy and acceptance numbers

Order is mandatory; a later step is meaningless if an earlier one fails. The numbers below are
**numerical-verification thresholds with rationale**, not application acceptance limits. The
model-agreement tolerance vs. physical data stays **TBD** until the owner/application supplies it.

| Step | Check | Threshold | Rationale |
|---|---|---|---|
| 1 | Input ledger | every BC value traceable to `ASSUMPTIONS` or the geometry JSON with units + evidence state | no untraceable input |
| 2 | Thermal **benchmark** (§4) | analytical vs solver within the stated per-case tolerance | proves the solver, not the enclosure |
| 3 | Mesh convergence | ≥3 levels; sensor ΔT change between the two finest < **0.1 °C** | one order below the ~0.5 °C absolute p95 of the lumped law's solar regime and below the pilot's 0.5 °C U95 target |
| 4 | Energy balance | net residual (in − out) < **1 %** of total applied heat | standard closure for a converged steady solve |
| 5 | Limiting cases | G=0 removes absorptance/pre-heat effects; Q=0 removes self-heating; `k→∞` recovers the isothermal lumped case; blocked vent → sealed-box limit; open vent lowers ΔT | directional, must match the lumped model's sign behaviour |
| 6 | Lumped comparison | disagreement reported in **°C** per regime bin (`nondimensional.regime`) and attributed to conduction vs vent flow | the actual Study B result |
| 7 | Physical | later (Study C); never inferred from 1–6 | — |

A solve that skips step 2 or 3 is **unverified (`accepted: null`)**, never a pass.

## 4. Thermal benchmark — required before any CHT claim

Section 9 is explicit: the briefing's proven workflow is IGES→MAPDL **linear-static structural**;
it demonstrates no radiation, no conduction–airflow coupling, no natural convection, no energy
balance. Geometry acceptance cannot qualify a thermal solver. Before Study B reports a number, run
these with an **independent expected answer computed first**:

| ID | Case | Independent expected answer | Validates | Tolerance |
|---|---|---|---|---|
| B1 | 1-D plane wall, thickness `t`, conductivity `k`, convection `h` both sides, fixed far-field temperatures | closed form (series resistance); wall ΔT and flux | conduction + Robin BC; the Biot mechanism | 0.5 % on flux |
| B2 | Heated vertical plate in still air | Churchill–Chu Nusselt correlation | external natural convection | 10 % on `h` (correlation scatter) |
| B3 | Two infinite parallel plates, emissivities `eps1, eps2`, temperatures fixed | closed-form net radiative flux | radiation model | 1 % on flux |
| B4 | Sealed heated box, isothermal high-`k` wall, `Q` internal, `h` external | the lumped model itself (`solve_surface_temperature` with `k→∞`) | end-to-end balance in the isothermal limit | 0.1 °C |
| B5 | Bottom-inlet / side-outlet heated box (Ishizuka 2012 configuration) | Ishizuka's *scaling*: internal rise ∝ `Q^0.8` in the sealed limit; monotone decrease with outlet porosity and outlet height | buoyancy-driven vent flow — **trend only**; Ishizuka's constants are apparatus-specific and are not a target | sign/monotonicity |

Tolerances are proposed, marked numerical; register them before the run. B1–B4 have closed forms
and are agent-buildable once a solver exists; B5 tests the mechanism Study A cannot see.

## 5. Reuse assessment (Section 9 deliverable)

**Shared machinery to call (lives in `500ft/engineering-audit`; do not copy):**
`cadloop/orchestrator.py` (job orchestration, bounded host deadlines), `cadloop/volume.py`
(independent expected-volume oracles, explicit unit parsing), `cadloop/fea/inspect_geometry.py`
(imported bounding box/orientation before any BC), the SOLIDWORKS COM authoring + re-drive +
STEP-export route, and the CadQuery oracle pattern. Proven for: native part authoring, named-
variable re-drive (1e-15), oracle agreement (1e-16), STEP round-trip (1e-16). Record the
engineering-audit revision with every run.

**Enclosure-specific components still needed (live here):**
1. `cad/enclosure/geometry.json` — **one** input file read by both the authoring script and the
   checker; every value carries units, evidence state, source and acquisition route
   (`measurement` / `vendor_drawing` / `design_then_inspect`). Generated from the accepted
   parameter register plus explicitly tagged `provisional_design` choices; never two hand-edited
   value sets.
2. An enclosure **oracle** — hand calculation for walls, vents and cutouts accounting for
   overlapping features; CadQuery construction for the plate stack. Shared inputs are fine;
   copying the author's measured output into the expected file is not verification.
3. An enclosure **contract beyond volume**: bounding dimensions and measured orientation, solid
   count, wall thickness at designated points, vent count and open area, sensor stand-off/position,
   plate gaps, and the reference-sensor mounting datum. Equal-volume parts can still have a
   misplaced vent.
4. A per-feature expected-vs-measured trace (shell, vent cuts, holes, sensor mount) with
   immediate checks on rejected equations and null feature returns.
5. A parameter-behaviour proof: change one parameter (vent width; sensor position), recompute the
   expectation independently, verify dependent positions and invariants, restore, recheck.
6. STEP export → re-import in a separate process → repeat the checks; tolerances registered by
   quantity and unit before the run (the briefing's 1e-15 agreements are observations, not a
   universal tolerance).
7. Result states: `accepted: true` only when all required checks pass; missing expected values or
   omitted checks → `null` (unverified); mismatch → `false`. Screenshots and clean rebuilds are
   explanatory only.

**Accepted vs unresolved dimensions:** as of this document **no enclosure dimension is accepted.**
The repository's geometry entries (`A_proj`, `A_conv`, wall thickness, vent area, sensor stand-off)
are `TODO-from-lab`. The owner's own printed revisions exist physically and can close them by the
`measurement` route; that is an owner action (EN-CAD-02), not something this document supplies.

**Mapping CAD → thermal ledger (must be explicit):** the lumped model's `A_conv` is an *effective
coupled* area, not the total CAD surface; `A_proj` is the sun-facing projection at a stated solar
angle; `Q` is heat *reaching the sensor zone*, not board power. Document the mapping, units and
uncertainty before any as-built prediction, and keep the current illustrative defaults as a
versioned baseline.

**Not demonstrated by the briefing (plan separately):** assembly mates, drawing automation and
tolerances, dependent-feature acceptance, any thermal solve, and a formal independent acceptance
check on the structural FEA output.

## 6. Proposed scoped update to `CAD_PLAN.md` / EN-CAD-09 (proposal — not applied)

Current allocation: *CadQuery for parameter-driven families and STEP checks; Onshape for
hand-modelled fixtures.* Section 9 prefers assessing the native SOLIDWORKS-COM authoring route
already proven in engineering-audit, with CadQuery as the **independent checker**.

Proposed wording for EN-CAD-09 "Done when": *Author with the engineering-audit SOLIDWORKS-COM
route where a host is available; use CadQuery as the independent oracle and STEP round-trip
checker in every case; Onshape only for fixtures the owner models interactively. Host availability
is checked at execution time and recorded per run; no host, no authoring claim.* Statuses stay
`deferred`; the geometry-verification contract in §5 becomes part of EN-CAD-01/03/04 acceptance.
**Owner decision required** before this edits `CAD_PLAN.md` or `CAD_TASKS.csv`.

## 7. Dimensionless extension contract (W2)

Groups the lumped model lacks or approximates. Each traces to a mechanism and a planned input; none
is introduced to improve a fit. `[m]` = measurable before fabrication from the design; `[built]` =
needs the fabricated part; `[field]` = needs the operating condition.

| Group | Definition | Inputs (units) | Pre-fab? | In lumped? | CHT resolves? | Omitted → failure mode | Limiting behaviour |
|---|---|---|---|---|---|---|---|
| Wall Biot | `Bi = h·t/k` | `h` W/m²K [field], `t` m [m], `k` W/mK [m: datasheet range / built: measured] | yes (with `k` range) | **no** — assumes Bi≪1 | yes (solid region) | isothermal wall overstates coupling; printed polymers (Bi 0.1–0.6) predicted too close to ambient | `k→∞` ⇒ Bi→0 ⇒ lumped recovered; `t→0` same |
| Vent Reynolds | `Re_vent = ρ·u_vent·D_h/μ` | `u_vent` m/s [field/CHT], `D_h` m [m], `ρ,μ` [field] | `D_h` yes; `u_vent` **no** — from CHT or a vent anemometer | **no** — replaced by `Pi_delta(U)` | yes (fluid region) | pre-heat closure has no geometry; two shields with the same outside wind but different vents get the same `Pi_delta` | `A_vent→0` ⇒ sealed box; `u_vent` is **not** ambient `U` |
| Vent area ratio | `A_vent/A_surface` | m² [m] | yes | no | yes | vent sizing invisible to the model | 0 ⇒ sealed; Ishizuka's `β²/(1−β)` form for the resistance |
| Internal dissipation | `N_Q = Q/(αφG·A_proj)` (G>0); night-safe absolute term `Q/(h·A_conv·ΔT_sky)` | `Q` W [built: measured at the enclosure], `α,φ,A_proj` [m] | `Q` only if measured on the electronics | yes (both forms, `nondimensional.theta_linear`) | yes (source term) | self-heating attributed to solar; the Couzo +2.6 °C mechanism unexplained | `Q→0` ⇒ pure shield case; `G→0` ⇒ absolute form only |
| Radiation nonlinearity | `tau = ΔT_sky/T_air` (K/K) with `h_r = 4εσT_air³` | `T_air`, `T_sky` K [field], `ε` [m/built] | yes for a design climate | no — linearised | yes (T⁴ radiation) | the >20 °C failure regime (Study A); cross-climate transfer (Study D) | `ΔT_sky→0` ⇒ no sky sink; large `ΔT` ⇒ linear law drifts |
| Buoyancy | `Ra_H = g·β_T·ΔT·H³/(ν·α_t)` (or `Gr`) on the vent-to-source height `H` | `H` m [m], `ΔT` K [CHT], air properties [field] | `H` yes; `ΔT` no | no | yes | natural vs forced regime misassigned at low wind — exactly the passive-shield worst case | `Ra→0` ⇒ conduction only; high `Ra` ⇒ chimney flow (Ishizuka) |

Dimensional check: every group above is dimensionless (`h·t/k` = W/m²K·m/(W/mK); `ρuD/μ` =
kg/m³·m/s·m/(Pa·s); `Q/(W)`; K/K; `g·β_T·ΔT·H³/(ν·α_t)` = m/s²·1/K·K·m³/(m²/s·m²/s)).

**Held-out rule (carries K2):** groups are chosen here, before data. Their coefficients, if any, are
fitted on the pilot's own data and judged only on held-out printed geometries against the Bernard
and Nakamura benchmarks defined in the direction record §10.

## 8. Triggers and what stays blocked

- **Thermal-FEA fallback (mode a):** may start when (i) B1–B4 pass on an installed solver and (ii)
  a geometry JSON with at least `provisional_design` dimensions exists. Toolchain install is
  **not** authorised this week.
- **CHT (mode b):** additionally needs B5 and an owner allocation for the verification budget.
- **CAD authoring:** EN-CAD-02 inventory (owner) → EN-CAD-01 register → EN-CAD-09 tooling with the
  §5 contract; host availability checked at run time, bounded deadlines, artifact inspected — never
  completion inferred from a launch call.
- `EN-S02`, `EN-R03`, `EN-S09B`, `EN-S11` unchanged; all CAD tasks remain `deferred`.
