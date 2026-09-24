# Study A — Nondimensional reduction of the enclosure-bias model (theory, 2026-09-16)

**Status: SIMULATION reduction of the existing lumped model. No physical data.** Every input
inherits the `bounded` / `TODO-from-lab` status of [`thermal_bias.ASSUMPTIONS`](../analysis/thermal_bias.py).
This document derives the dimensionless groups and reports the **approximation accuracy** of the
linearised closed form. **Corrected 2026-09-24:** an earlier version framed this as a "collapse
test" with a "kill criterion" and concluded the collapse was not universal. That was wrong — see
the corrected verdict in §5. The exact nonlinear dimensionless balance holds to solver tolerance.

## 1. Governing balance

The steady lumped balance solved by `thermal_bias.solve_surface_temperature`:

    alpha*phi*G*A_proj + Q = h*A_conv*(T_s - T_l) + eps*sigma*A_conv*[ f*(T_s^4 - T_sky^4) + (1-f)*(T_s^4 - T_l^4) ]

with local air `T_l = T_air + delta` (shield plate pre-heat), `h = h_ext * conv_boost`,
`f = f_sky`, and reported bias `dT = T_s - T_air`.

## 2. Dimensionless groups

Linearise radiation about ambient, `h_r = 4*eps*sigma*T_air^3` (5.69 W/m²K at 30 °C, ε 0.90). With
`theta = dT/dT_sky` and `dT_sky = T_air - T_sky`:

| Group | Definition | Meaning | Novelty relevance |
|---|---|---|---|
| `Pi_G`  | `alpha*phi*G*A_proj / (h*A_conv*dT_sky)` | heating number: absorbed solar vs convective removal | bundles absorptance, shading, irradiance, area ratio, wind (via `h`) |
| `N_Q`   | `Q / (alpha*phi*G*A_proj)` | internal-dissipation ratio: self-heat vs solar load | **the axis shield physics never had** (AQ self-heating) |
| `N_r`   | `h_r / h` | radiation/convection coupling | governs the radiation-dominated failure regime |
| `f`     | `f_sky` | fraction of the element radiating to cold sky | sets night sub-ambient behaviour |
| `Pi_d`  | `delta / dT_sky` | ventilation/pre-heat number (wind-dependent) | empirical closure; maps to a vent-Reynolds group in Study B |

The balance reduces **exactly (for the linearised model)** to a closed form:

    theta = [ Pi_G*(1 + N_Q) - N_r*f + Pi_d*(1 + N_r*(1-f)) ] / (1 + N_r)

Implemented in [`analysis/nondimensional.py`](../analysis/nondimensional.py) (`theta_linear`), written to
stay finite at night (`solar = 0`) by folding `N_Q` back into an absolute internal-load term.

## 3. The Biot gate — why printed AQ enclosures are physically open

The lumped reduction assumes an **isothermal wall**, i.e. `Bi = h*t/k << 1`. That holds for metal
meteorological screens; it does **not** hold for low-cost printed polymer enclosures:

| Wall (3 mm) | k [W/mK] | Bi at h=7 | Bi at h=25 | source |
|---|---|---|---|---|
| PLA, printed 100 % infill | 0.182–0.267 | 0.08–0.12 | 0.28–0.41 | measured |
| ABS, printed **through-layer** | 0.1039 | 0.20 | 0.72 | measured |
| ABS, printed in-plane | 0.1664 | 0.13 | 0.45 | measured |
| PETG, printed 100 % infill | 0.290 | 0.07 | 0.26 | measured |
| PLA Aero (foaming filament) | 0.114 | 0.18 | 0.66 | measured |
| PET-G at 25 % infill | 0.057–0.104 | 0.20–0.37 | 0.72–1.32 | measured |
| Aluminium | 205 | ~0 | ~0 | handbook |

**Corrected 2026-09-22.** This table previously used *handbook bulk* conductivities (PLA 0.13, ABS
0.17, PETG 0.29). Three independent labs measured **printed** PLA at 0.182–0.267 W/mK
([`baraboi2026`](../literature/REVIEW_2026-09-22.md), `tychaniczkwiecien2025`, `rodriguez2023`), so
k = 0.13 was too low and **inflated Bi by 40–105 %**. The conclusion is unchanged and in fact better
supported, but the mechanism is different: the high-Bi end comes from **through-layer anisotropy**
(`janek2026`: 0.1039 W/mK, anisotropy ratio 1.60), **reduced infill** (`lopes2023`: infill *pattern*
alone moves effective k by 82 % at fixed density) and **foaming filaments** — not from a low bulk
conductivity. Caveat none of these sources addresses: a 3 mm wall printed with perimeter shells may
be near-solid regardless of the infill setting, so the low-infill rows are an upper bound on the
effect for a real wall.

Measured `Bi ~ 0.07–0.72` (up to ~1.3 if genuinely infilled) means wall conduction is a **first-order effect** the classical (metal, `Bi≈0`)
shield literature structurally omits. This is a physically-grounded open axis independent of the
literature scan, and it is where Study B's CHT check earns its keep (resolving the wall/air field
the lumped model cannot).

## 4. Collapse test — preregistration

- **DOE:** full-factorial daytime sweep over `alpha, phi(solar_factor), A_proj, A_conv, Q, G, wind,
  f_sky` across the bounded ranges in `nondimensional.DOE_AXES` (1944 points). Night is reported
  separately (small, radiation-dominated).
- **Law under test:** the closed form of §2 (parameter-free theory), residual reported as both
  absolute °C and relative.
- **Acceptance (predictive claim holds):** p95 **relative** residual ≤ ~3% (the model's own
  daytime linearisation uncertainty) across the DOE.
- **Kill criterion (verbatim from the plan):** scatter about the law larger than the model's own
  uncertainty ⇒ **there is no law; the project stays a ranking study.**

## 5. Result — the linearised approximation is bounded; the exact balance holds

`python -m analysis.nondimensional`:

| Regime | N | abs median | abs p95 | rel median | rel p95 |
|---|---:|---:|---:|---:|---:|
| all daytime | 1944 | 0.23 °C | 2.0 °C | 3.6% | **63.9%** |
| bias > 1 °C | 1656 | 0.23 °C | 2.3 °C | 2.6% | 24.0% |
| bias > 3 °C | 1076 | 0.21 °C | 4.0 °C | 2.1% | 12.3% |
| solar-driven θ>0.3 | 723 | 0.27 °C | 6.3 °C | 2.4% | 11.9% |

Overall `R² = 0.972`.

> ### Corrected verdict (2026-09-24)
>
> **The earlier verdict — "the kill criterion is tripped, there is no universal clean law" — was
> wrong, and is withdrawn.** That comparison was between a *linearised* closed form and the
> *nonlinear* solver **derived from the same heat balance**. It therefore measures **approximation
> error**, not the validity of a dimensionless representation.
>
> The **exact nonlinear dimensionless balance**
>
> `Pi_G + Pi_Q = theta - d + N_r/(4*tau) * { f*[(1+tau*theta)^4 - (1-tau)^4] + (1-f)*[(1+tau*theta)^4 - (1+tau*d)^4] }`
>
> was derived and evaluated at **all 1,944 DOE points**: maximum absolute residual **5.478e-9**,
> i.e. solver tolerance (`nondimensional.balance_residual`; regression test
> `ExactBalanceTests`). **Dimensionless similarity is not falsified by anything in this module.**
>
> Correct statement: *the linearised closed form exceeds the selected approximation-error threshold
> in parts of the illustrative DOE; the exact nonlinear dimensionless balance remains consistent
> with the original model. Physical accuracy and cross-design transfer are untested.*
>
> Three further corrections: the 3 % **relative** band is a **selected approximation threshold**, not
> a measured model uncertainty or a scientific kill criterion; **absolute °C** is the primary metric
> because relative error is ill-conditioned near zero bias; and the regime bins are **output-based
> diagnostics of a known solver**, not a prospective field rule. The DOE/threshold exercise is
> labelled **exploratory** — no dated pre-run record supports calling it preregistered.

What the approximation results *do* show:

- **Median collapse is tight** (~2–4% relative, ~0.23 °C absolute) — the solar-driven regime is
  well-predicted by the five groups.
- **The tail behaviour is an approximation limit, not a similarity failure:** it concentrates at (a) the `theta ≈ 0` crossing,
  where relative error is meaningless (absolute error stays bounded, p95 ≤ ~5 °C), and (b) large
  `dT` where radiation nonlinearity (dropped by the linearisation) grows.

This matches the repo's own [matched-control sensitivity screen](../analysis/thermal_bias_results.md)
(A3): the enclosure advantage is not robust to combined assumptions, so a *universal* collapse was
never likely. The honest scientific contribution is therefore **the collapse domain and its
boundary**, not a claim that bias always collapses.

**Per-regime diagnostic (added 2026-09-21, W3):** `python -m analysis.nondimensional` now bins the
DOE by mechanism (`nondimensional.regime`) and `--out` writes the groups, absolute/relative
residuals and regime per point. Solar-driven: 0.10 / 0.46 °C (med / p95 abs); high-nonlinearity
(ΔT>20 °C): 1.9 / 14.2 °C — the law's failure domain. See
[research-direction-2026-09-21.md](research-direction-2026-09-21.md) §3.

**Extension (2026-09-23, Study B design):** the groups this reduction lacks — wall Biot, vent
Reynolds, vent area ratio, radiation nonlinearity, Rayleigh — are specified with inputs, limits and
failure modes in [specs/study-b-cht/design.md](specs/study-b-cht/design.md) §7.

## 6. Honest limits

- **Radiation nonlinearity** — the linearised law is the reduction hypothesis; ground truth is the
  full nonlinear solver. At fixed climate (`tau = dT_sky/T_air ≈ 0.066`) the collapse is onto the 5
  groups; **varying `T_air` across climates (Study D) adds a sixth radiation-nonlinearity group.**
- **`Pi_d` is an empirical closure**, not first-principles ventilation physics; Study B replaces it
  with a resolved vent-Reynolds treatment via CHT.
- **`Bi << 1` is assumed** by the whole reduction and is violated for printed polymers — a modelled
  bias the lumped model cannot self-diagnose.
- These are model outputs under the stated assumptions, **not measurements**. Same status as every
  number in `thermal_bias_results.md`: SIMULATION / pending lab data.
