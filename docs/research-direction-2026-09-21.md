# Research-direction decision record — 2026-09-21

**Status: decision aid for the owner. Nothing here is frozen until the owner chooses.** Base:
`main` at `84e0ef3`. Companion to the open owner draft [PR #20](https://github.com/500ft/sensor-enclosure-thermal-design/pull/20)
(`docs/research-question-draft.md`), which is *not* duplicated here. Authority: scope decision in
[PHD_SCOPE_AND_NOVELTY.md](PHD_SCOPE_AND_NOVELTY.md); result in [studyA_nondimensional.md](studyA_nondimensional.md).
Every number below is **ANALYTICAL (simulation)** unless stated otherwise; no physical measurement exists.

## 1. The decision: two directions, one must be chosen

The repository currently carries **two different research questions**, and drifting between them is
the main risk this week:

| | **Direction A — pre-build prediction (narrowed)** | **Direction B — bounded engineering study (PR #20)** |
|---|---|---|
| Question | Do an internal-dissipation ratio, a vent-flow group and a wall-Biot group predict the onboard-T/RH bias of a low-cost 3D-printed AQ enclosure *before fabrication*, and where does that prediction fail? | How do surface finish and ventilation geometry affect the T/RH bias of *this project's* enclosure under varying solar and wind? |
| Scale | Research-programme scale **only if** validated experimentally on held-out geometries and it beats a post-build baseline | Design/ranking study; honest, achievable with the existing three variants |
| Physics it adds | Internal dissipation, resolved vent flow, wall conduction — axes classical shield work omits | None new; applies known shield physics to one enclosure |
| Demotes to | Direction B, if K2 fails | — |
| Needs | Multi-geometry/material printed variant set + held-out test + CHT | Three variants + reference, 24 h+ |

**Recommendation:** pursue **A with B as the guaranteed floor.** The three-variant pilot (Study C)
serves both: it is B's complete experiment and A's first held-out check. Do not write proposal text
that assumes A until K2 (below) has a defined benchmark.

## 2. Direction A, stated falsifiably

- **Main hypothesis (H1):** in the solar-driven regime, signed enclosure bias is predicted before
  fabrication by `(Pi_G, N_Q, N_r, f_sky, Pi_delta)` plus a wall-Biot correction, to within the
  registered instrument uncertainty, on geometries *not used* to build the law.
- **SQ1** — which groups predict signed bias in the solar-driven regime? *(Study A: answered
  analytically; see §3.)*
- **SQ2** — how do wall conduction (Bi) and resolved vent flow (Re_vent) change the prediction for
  printed polymer geometries? *(Study B: CHT; not started.)*
- **SQ3** — where does the reduction fail, and does that failure predict downstream PM/gas
  calibration error? *(Study A maps the analytical failure regime; the calibration link is
  untested.)*
- **Competing explanation (must be tested, not dismissed):** a **post-build empirical correction**
  (fitted energy-balance coefficients per built enclosure, Barbaresco et al. 2019 style; or a
  met-variable regression, Nakamura & Mahrt 2005 style) predicts as well or better at lower cost.
  **This is the K2 benchmark.** It must be implemented as an explicit comparator on the same
  held-out data before any pre-build claim.

## 3. What the analytical evidence supports today (ANALYTICAL only)

From `python -m analysis.nondimensional` at `84e0ef3` (1944-point daytime DOE; regimes set by
mechanism, see `nondimensional.regime`):

| Regime | n | abs residual med / p95 | rel residual med / p95 | Reading |
|---|---:|---|---|---|
| solar_driven | 1220 | **0.10 / 0.46 °C** | 1.6% / 15.9% | law holds in absolute terms |
| near_zero (|ΔT|<1 °C) | 169 | 0.05 / 0.47 °C | n/a | relative error meaningless |
| radiation_dominated (ΔT<0) | 349 | 0.36 / 0.47 °C | n/a | small absolute error, sub-ambient |
| high_nonlinearity (ΔT>20 °C) | 206 | **1.9 / 14.2 °C** | 6.2% / 19.5% | **law fails** |

Overall R² = 0.972. **Claim the evidence supports:** the five-group linear law reproduces the
lumped model's solar-driven daytime bias to ~0.1 °C median / <0.5 °C p95, and fails by several °C
once bias exceeds ~20 °C. **Claim already falsified:** a universal collapse at the preregistered
3% *relative* p95 band — tripped in every regime, including solar-driven.

**Open methodological point for the owner:** the kill criterion was preregistered as *relative*
3%, but the law's natural error is *absolute* °C, and the physical acceptance will be an absolute
uncertainty (U95). A relative band near ΔT→0 is unphysical. Proposal: **re-register the criterion
as absolute °C against the registered U95**, recorded as a prospective amendment — not applied
retroactively to call the current result a pass.

## 4. Kill criteria (Direction A → Direction B)

- **K1** — no reproducible physical bias above the registered instrument + propagation uncertainty.
- **K2** — pre-build groups do not predict *held-out* geometries better than the post-build
  benchmark (§2) after honest complexity accounting (parameters counted on both sides).
- **K3** — internal dissipation, vent flow and wall Biot cannot be independently varied *and*
  measured in the printed variant set.
- **K4** — the CHT/lumped disagreement cannot be bounded well enough to design the pilot (Study B).

Any one fired ⇒ present the work as Direction B. This is a legitimate outcome, not a failure.

## 5. Contribution boundary and permitted language

Contribution, if A survives: **a regime-dependent collapse domain and its failure boundary for
low-cost printed enclosures with internal dissipation**, with pre-build prediction demonstrated on
held-out geometries against a post-build baseline. **Not** a universal framework across sensing
systems. Claim levels: `simulated` (all of §3), `experimentally supported` (none yet),
`not supported` (universal collapse).

## 6. Claim / evidence matrix

| ID | Claim | Class | Evidence | Status | Permitted wording | Prohibited wording |
|---|---|---|---|---|---|---|
| C1 | dark enclosure has solar self-heating bias | ANALYTICAL | `thermal_bias_results.md` §2; day table | simulated | "the model predicts ~19 °C at 1000 W/m², 0.5 m/s" | "measured", "observed" |
| C2 | paint and passive shielding are separate variants (V0P vs V1) | ANALYTICAL | `thermal_bias.build_variants`; A3 screen | simulated | "same-geometry painted control" | "shield is better" (unqualified) |
| C3 | night bias can change sign with sky temperature | ANALYTICAL | `thermal_bias_results.md` night section | simulated | "conditional sign reversal in the model" | "nights are cold-biased" |
| C4 | five-group law is exact for the *linearised* model | ANALYTICAL | `studyA_nondimensional.md` §2 | derived | "exact for the linearised balance" | "exact" (unqualified) |
| C5 | full nonlinear collapse is regime-dependent | ANALYTICAL | §3 above; `test_nondimensional.CollapseIsRegimeDependentTests` | simulated | "holds in the solar-driven regime, fails above ~20 °C" | "universal", "validated" |
| C6 | printed-wall Biot is a first-order validity concern | ANALYTICAL (hand calc) | `studyA_nondimensional.md` §3 | derived from handbook k | "Bi ~0.1–0.6 for k=0.13–0.29 W/mK at 3 mm" | "printed walls are non-isothermal" (as measured fact) |
| C7 | internal dissipation is an under-addressed design axis | LITERATURE (abstract-level) | `PHD_SCOPE_AND_NOVELTY.md` §1 | **full-read pending** | "not found in the checked sources" | "no one has done this", "novel" |
| C8 | physical validation is pending | — | `SPRINT_TASKS.csv` EN-R03 blocked | blocked | "pending" | any agreement/accuracy claim |

## 7. Relationship to PR #20

PR #20's question is Direction B, and its literature review (Tarara 2007, Holden 2013, Theisen
2020, Botero 2022, Deford 2025) is the correct base for B. It does not cite the Direction-A
competitors (Barbaresco 2019, Nakamura & Mahrt 2005, Barkjohn/Cha) — that is Tuesday's work
(T1/T2), not an edit to #20. Merge/edit of #20 is the owner's call; if A is chosen, #20's
"Question" section needs one added sentence naming the pre-build prediction aim and the post-build
benchmark. Recorded here as a follow-up, not applied.

## 8. Unchanged

No physical data, permission, hardware, geometry or funding is created by this record. `EN-S02`,
`EN-R03`, `EN-S09B`, `EN-S11` stay blocked; CAD deferred; FEA a stub.
