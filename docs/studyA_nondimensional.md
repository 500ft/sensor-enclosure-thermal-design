# Study A — Nondimensional reduction of the enclosure-bias model (theory, 2026-09-16)

**Status: SIMULATION reduction of the existing lumped model. No physical data.** Every input
inherits the `bounded` / `TODO-from-lab` status of [`thermal_bias.ASSUMPTIONS`](../analysis/thermal_bias.py).
This document derives the dimensionless groups, states the collapse test and its kill criterion, and
reports the honest result: **the collapse is regime-dependent, not universal.**

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

| Wall (3 mm) | k [W/mK] | Bi at h=7 | Bi at h=25 |
|---|---|---|---|
| PLA | 0.13 | 0.16 | 0.58 |
| ABS | 0.17 | 0.12 | 0.44 |
| PETG | 0.29 | 0.07 | 0.26 |
| Aluminium | 205 | ~0 | ~0 |

`Bi ~ 0.1–0.6` means wall conduction is a **first-order effect** the classical (metal, `Bi≈0`)
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

## 5. Result — regime-dependent, kill criterion tripped

`python -m analysis.nondimensional`:

| Regime | N | abs median | abs p95 | rel median | rel p95 |
|---|---:|---:|---:|---:|---:|
| all daytime | 1944 | 0.23 °C | 2.0 °C | 3.6% | **63.9%** |
| bias > 1 °C | 1656 | 0.23 °C | 2.3 °C | 2.6% | 24.0% |
| bias > 3 °C | 1076 | 0.21 °C | 4.0 °C | 2.1% | 12.3% |
| solar-driven θ>0.3 | 723 | 0.27 °C | 6.3 °C | 2.4% | 11.9% |

Overall `R² = 0.972`. **Verdict: the p95 relative residual (64% across the DOE; still 12–24% even
for meaningful bias) trips the kill criterion.** There is no single universal clean law at the
preregistered band. What *does* hold:

- **Median collapse is tight** (~2–4% relative, ~0.23 °C absolute) — the solar-driven regime is
  well-predicted by the five groups.
- **The tail failure is physical, not numerical:** it concentrates at (a) the `theta ≈ 0` crossing,
  where relative error is meaningless (absolute error stays bounded, p95 ≤ ~5 °C), and (b) large
  `dT` where radiation nonlinearity (dropped by the linearisation) grows.

This matches the repo's own [matched-control sensitivity screen](../analysis/thermal_bias_results.md)
(A3): the enclosure advantage is not robust to combined assumptions, so a *universal* collapse was
never likely. The honest scientific contribution is therefore **the collapse domain and its
boundary**, not a claim that bias always collapses.

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
