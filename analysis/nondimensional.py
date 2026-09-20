#!/usr/bin/env python3
"""Study A -- nondimensional reduction of the existing lumped enclosure-bias model.

Reduces the steady-state balance in ``thermal_bias.solve_surface_temperature`` to five
dimensionless groups and a closed-form prediction of the normalised bias, then measures whether
the FULL nonlinear model collapses onto that prediction across a design-of-experiments (DOE) sweep.

Balance (per thermal_bias):
    alpha*phi*G*A_proj + Q = h*A_conv*(T_s - T_l) + eps*sigma*A_conv*[ f*(T_s^4 - T_sky^4)
                                                                       + (1-f)*(T_s^4 - T_l^4) ]
with T_l = T_air + delta (shield air pre-heat), h = h_ext * conv_boost.

Linearise the radiation term about T_air (h_r = 4*eps*sigma*T_air^3). With
    theta   = dT / dT_sky           (dT = T_s - T_air, dT_sky = T_air - T_sky)
    Pi_G    = alpha*phi*G*A_proj / (h*A_conv*dT_sky)      heating number
    N_Q     = Q / (alpha*phi*G*A_proj)                    internal-dissipation ratio
    N_r     = h_r / h                                     radiation/convection ratio
    f       = f_sky                                       sky-view fraction
    Pi_d    = delta / dT_sky                              ventilation/pre-heat number
the balance collapses to the closed form

    theta = [ Pi_G*(1 + N_Q) - N_r*f + Pi_d*(1 + N_r*(1-f)) ] / (1 + N_r).

This is EXACT for the linearised model and predicts the full nonlinear model to ~3% for daytime
bias (see docs/studyA_nondimensional.md). It is a SIMULATION reduction, not a measurement, and it
inherits every ``bounded``/``TODO-from-lab`` status of thermal_bias.ASSUMPTIONS. Kill criterion for
the collapse hypothesis: residual scatter about the law larger than the model's own linearisation
uncertainty means there is no clean law and the project is a ranking study, not a predictive one.
"""
from __future__ import annotations
import argparse, csv, itertools, math
from dataclasses import replace
from pathlib import Path

from analysis import thermal_bias as model

SIGMA = 5.670374419e-8  # Stefan-Boltzmann [W/m^2K^4]


def _inputs() -> dict:
    return {name: value for name, value, *_ in model.ASSUMPTIONS}


def h_rad_linear(t_air_c: float, eps: float) -> float:
    """Linearised radiative coefficient h_r = 4*eps*sigma*T_air^3 [W/m^2K] (T in kelvin)."""
    return 4.0 * eps * SIGMA * (t_air_c + 273.15) ** 3


def biot(h_w_m2k: float, wall_thickness_m: float, wall_conductivity_w_mk: float) -> float:
    """Wall Biot number Bi = h*t/k. The lumped model assumes Bi << 1 (isothermal wall).

    Low-cost printed polymers (k ~ 0.13-0.29 W/mK) at ~3 mm give Bi ~ 0.1-0.6, so wall conduction
    is first order; a metal screen (k ~ 200) gives Bi ~ 0. This is the validity gate for the whole
    lumped reduction and the physically-open axis for printed air-quality-sensor enclosures.
    """
    return h_w_m2k * wall_thickness_m / wall_conductivity_w_mk


def groups(variant, g_solar: float, wind: float, delta: float,
           t_air_c: float, dt_sky: float, eps: float) -> dict:
    """The five dimensionless groups at one operating point (plus raw h, h_r for traceability)."""
    h = model.h_external(wind, _inputs()["h_free_floor"], _inputs()["h_wind_slope"]) * variant.conv_boost
    if variant.forced_h is not None:
        h = variant.forced_h
    h_r = h_rad_linear(t_air_c, eps)
    solar = variant.alpha * variant.solar_factor * g_solar * variant.a_proj
    conv_cond = h * variant.a_conv
    return dict(
        Pi_G=(solar / (conv_cond * dt_sky)) if conv_cond > 0 else math.inf,
        N_Q=(variant.q_internal / solar) if solar > 0 else math.inf,   # inf at night (no solar drive)
        N_r=h_r / h,
        f_sky=variant.f_sky,
        Pi_delta=delta / dt_sky,
        _h=h, _h_r=h_r, _solar_w=solar)


def theta_linear(variant, g_solar: float, wind: float, delta: float,
                 t_air_c: float, dt_sky: float, eps: float) -> float:
    """Closed-form normalised bias theta = dT/dT_sky for the linearised model.

    Written so it is finite at night (solar = 0): the N_Q term is folded back into an absolute
    internal-load contribution rather than the ratio, so no division by a zero solar drive occurs.
    """
    g = groups(variant, g_solar, wind, delta, t_air_c, dt_sky, eps)
    h, h_r, solar = g["_h"], g["_h_r"], g["_solar_w"]
    conv_cond = h * variant.a_conv
    n_r, f = g["N_r"], g["f_sky"]
    # theta = [ (solar + Q)/(C*dT_sky) - N_r*f + Pi_d*(1 + N_r*(1-f)) ] / (1 + N_r)
    drive = (solar + variant.q_internal) / (conv_cond * dt_sky)
    return (drive - n_r * f + g["Pi_delta"] * (1.0 + n_r * (1.0 - f))) / (1.0 + n_r)


def theta_full(variant, g_solar: float, wind: float, delta: float,
               t_air_c: float, dt_sky: float) -> float:
    """Normalised bias from the FULL nonlinear solver (ground truth for the collapse test)."""
    h = model.h_external(wind, _inputs()["h_free_floor"], _inputs()["h_wind_slope"])
    t_s = model.solve_surface_temperature(variant, g_solar, t_air_c, t_air_c - dt_sky, h, air_preheat_k=delta)
    return (t_s - t_air_c) / dt_sky


# --- DOE and collapse metric -------------------------------------------------------------------

DOE_AXES = dict(   # bounded physical ranges; alpha/A/Q spans cover printed AQ enclosures + baselines
    alpha=(0.30, 0.60, 0.90),
    solar_factor=(0.15, 0.30, 1.0),
    a_proj=(0.010, 0.030),
    a_conv=(0.020, 0.090),
    q_internal=(0.1, 0.8, 1.6),
    g_solar=(400.0, 700.0, 1000.0),
    wind=(0.2, 1.0, 3.0),
    f_sky=(0.05, 0.50),
)


def doe_samples(t_air_c: float, dt_sky: float, eps: float):
    """Yield (params, theta_full, theta_linear, groups) over the full-factorial daytime DOE.

    Daytime only (G>0, solar drive present) -- the regime the predictive claim targets and where
    the linearisation holds; night bias is small, radiation-dominated, and reported separately.
    """
    base = model.build_variants()[0]
    keys = list(DOE_AXES)
    for combo in itertools.product(*(DOE_AXES[k] for k in keys)):
        p = dict(zip(keys, combo))
        v = replace(base, alpha=p["alpha"], solar_factor=p["solar_factor"], a_proj=p["a_proj"],
                    a_conv=p["a_conv"], q_internal=p["q_internal"], f_sky=p["f_sky"], conv_boost=1.0)
        # shield air pre-heat only for shaded variants, using the model's own convention
        delta = 0.0
        if p["solar_factor"] < 1.0:
            delta = model.shield_air_preheat(p["wind"], _inputs()["shield_air_preheat_calm"],
                                             _inputs()["preheat_wind_halflife"], forced=False) * (p["g_solar"] / 1000.0)
        tf = theta_full(v, p["g_solar"], p["wind"], delta, t_air_c, dt_sky)
        tl = theta_linear(v, p["g_solar"], p["wind"], delta, t_air_c, dt_sky, eps)
        yield p, tf, tl, groups(v, p["g_solar"], p["wind"], delta, t_air_c, dt_sky, eps)


NEAR_ZERO_C, HIGH_NONLINEAR_C = 1.0, 20.0   # diagnostic bins, set by mechanism (see docs), not by fit


def regime(theta_f: float, dt_sky: float) -> str:
    """Diagnostic regime label for one DOE point, from the FULL-model bias dT = theta*dt_sky.

    radiation_dominated: dT < 0 -- sky radiative loss exceeds absorbed solar + internal heat.
    near_zero:           |dT| < 1 degC -- relative residual is meaningless here; use absolute.
    high_nonlinearity:   dT > 20 degC -- the dropped T^4 terms grow; linear law drifts.
    solar_driven:        everything else -- the regime where the five-group law holds.
    """
    d = theta_f * dt_sky
    if d < 0:
        return "radiation_dominated"
    if abs(d) < NEAR_ZERO_C:
        return "near_zero"
    if d > HIGH_NONLINEAR_C:
        return "high_nonlinearity"
    return "solar_driven"


def collapse_metric(pairs, dt_sky: float = 1.0) -> dict:
    """Residual of the full model about the closed-form law. pairs = [(theta_full, theta_linear)].

    Reports BOTH an absolute residual in degC (|theta_full-theta_linear|*dt_sky, robust near zero
    bias) and a relative residual (meaningful only away from the theta~0 crossing). The relative
    tail is dominated by near-zero-bias points; the absolute residual is the honest bound there.
    """
    absres = sorted(abs(tf - tl) * dt_sky for tf, tl in pairs)
    rel = sorted(abs(tf - tl) / abs(tf) for tf, tl in pairs if abs(tf) > 1e-9)
    n, nr = len(absres), len(rel)
    mean_tf = sum(tf for tf, _ in pairs) / len(pairs)
    ss_tot = sum((tf - mean_tf) ** 2 for tf, _ in pairs)
    ss_res = sum((tf - tl) ** 2 for tf, tl in pairs)
    return dict(n=n, abs_median_c=absres[n // 2], abs_p95_c=absres[min(n - 1, int(0.95 * n))],
                rel_median=rel[nr // 2], rel_p95=rel[min(nr - 1, int(0.95 * nr))], rel_max=rel[-1],
                r2=1.0 - ss_res / ss_tot if ss_tot > 0 else float("nan"))


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--out", type=Path, help="optional CSV of the DOE (must not already exist)")
    a = ap.parse_args(argv)
    inp = _inputs()
    t_air, dt_sky, eps = inp["T_air"], inp["T_sky_offset"], inp["eps_surface"]
    samples = list(doe_samples(t_air, dt_sky, eps))
    m = collapse_metric([(tf, tl) for _, tf, tl, _ in samples], dt_sky)
    tripped = m["rel_p95"] > 0.03
    print(f"DOE points (daytime full-factorial): {m['n']}")
    print(f"collapse of full model onto the closed-form law: R^2={m['r2']:.5f}")
    print(f"  absolute residual: median={m['abs_median_c']:.3f} degC, p95={m['abs_p95_c']:.3f} degC")
    print(f"  relative residual: median={m['rel_median']*100:.2f}%, p95={m['rel_p95']*100:.2f}%, "
          f"max={m['rel_max']*100:.2f}% (tail = near-zero-bias crossings)")
    print(f"kill criterion (p95 relative > ~3% => no universal clean law): "
          f"{'TRIPPED -- collapse is regime-dependent, not universal' if tripped else 'not tripped'}")
    print("per-regime (abs residual degC; relative only where |dT|>=1):")
    by = {}
    for _, tf, tl, _ in samples:
        by.setdefault(regime(tf, dt_sky), []).append((tf, tl))
    for name in ("solar_driven", "near_zero", "radiation_dominated", "high_nonlinearity"):
        if name in by:
            r = collapse_metric(by[name], dt_sky)
            print(f"  {name:<20} n={r['n']:4d}  abs med={r['abs_median_c']:.3f} p95={r['abs_p95_c']:.3f}"
                  f"  rel med={r['rel_median']*100:.1f}% p95={r['rel_p95']*100:.1f}%")
    if a.out is not None:
        if a.out.exists():
            ap.error(f"{a.out} exists; write to a fresh path")
        a.out.parent.mkdir(parents=True, exist_ok=True)
        with a.out.open("w", newline="") as fh:
            w = csv.writer(fh)
            w.writerow(["alpha", "solar_factor", "a_proj", "a_conv", "q_internal", "g_solar", "wind", "f_sky",
                        "Pi_G", "N_Q", "N_r", "Pi_delta", "theta_full", "theta_linear", "dT_full_c",
                        "abs_residual_c", "rel_residual", "regime"])
            for p, tf, tl, g in samples:
                d = tf * dt_sky
                w.writerow([p["alpha"], p["solar_factor"], p["a_proj"], p["a_conv"], p["q_internal"],
                            p["g_solar"], p["wind"], p["f_sky"],
                            f"{g['Pi_G']:.6f}", f"{g['N_Q']:.6f}", f"{g['N_r']:.6f}", f"{g['Pi_delta']:.6f}",
                            f"{tf:.6f}", f"{tl:.6f}", f"{d:.6f}", f"{abs(tf-tl)*dt_sky:.6f}",
                            f"{abs(tf-tl)/abs(tf):.6f}" if abs(d) >= NEAR_ZERO_C else "",   # blank = not meaningful
                            regime(tf, dt_sky)])
        print("wrote", a.out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
