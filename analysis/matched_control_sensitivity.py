#!/usr/bin/env python3
"""Matched-control sensitivity screen (illustrative, NOT a measurement).

Question: is V1's nominal absolute-bias advantage over the identical-geometry painted box (V0P)
stable under the repository's OWN illustrated V1 assumption perturbations? This is a finite
24-case screen -- 8 V1 assumption combinations x 3 operating cases -- run on the existing
``thermal_bias`` solver with the existing illustrated values from ``thermal_bias.sensitivity_block``.

It supplies NO confidence interval, joint uncertainty bound, probability of superiority, or
as-built model-agreement tolerance. The perturbation values are the one-at-a-time illustrative
figures already in the repository, combined here to show the planning consequence -- they are not
measured bounds or a probability distribution. A positive advantage means V1 sits closer to TRUE
ambient; "cooler" alone is not "more accurate" when a bias may be negative. Duplicate night
predictions are meaningful controls, not additional independent evidence.

    python -m analysis.matched_control_sensitivity --out DIR/matched_control_sensitivity.csv
"""
from __future__ import annotations
import argparse, csv, itertools
from dataclasses import replace
from pathlib import Path

from analysis import thermal_bias as model

# Illustrated V1 perturbations, reused verbatim from thermal_bias.sensitivity_block:
#   solar_factor 0.18 -> 0.30 ("shading worse"), conv_boost 1.4 -> 1.0 ("no convection boost"),
#   calm plate air pre-heat 1.2 -> 2.4 K ("pre-heat doubled"). The first value in each pair is the default.
SOLAR_FACTORS = (0.18, 0.30)
CONV_BOOSTS = (1.4, 1.0)
CALM_PREHEATS_K = (1.2, 2.4)

# Three specified operating cases at air = T_air; sky is given as an absolute degC per the plan.
#   (name, g_solar_w_m2, wind_m_s, t_sky_c)
CASES = (
    ("day",            1000.0, 0.5, 10.0),   # G=1000, low wind; sky = T_air - T_sky_offset (30 - 20)
    ("night_nominal",     0.0, 0.0, 10.0),   # zero solar, calm, clear sky
    ("night_warm_sky",    0.0, 0.0, 29.0),   # zero solar, calm, warm (cloudy) sky
)

FIELDS = ["case", "g_solar_w_m2", "wind_m_s", "t_sky_c", "t_air_c", "v1_solar_factor",
          "v1_conv_boost", "v1_calm_preheat_k", "is_default_v1", "bias_v0p_c", "bias_v1_c",
          "abs_advantage_c"]


def _inputs() -> dict:
    return {name: value for name, value, *_ in model.ASSUMPTIONS}


def bias_c(variant, calm_preheat_k: float, g_solar: float, wind: float, t_sky_c: float) -> float:
    """Sensor delta-T above TRUE ambient [degC] for one variant at one operating point.

    Uses the existing solver and the existing pre-heat convention from ``sensitivity_block``:
    a shielded variant's plate air pre-heat scales with solar (G/1000) and decays with wind; an
    unshielded control (``solar_factor == 1``) sees no plate pre-heat.
    """
    inp = _inputs()
    air = inp["T_air"]
    h = model.h_external(wind, inp["h_free_floor"], inp["h_wind_slope"])
    preheat = 0.0
    if variant.solar_factor < 1.0:
        preheat = model.shield_air_preheat(
            wind, calm_preheat_k, inp["preheat_wind_halflife"], forced=variant.forced_h is not None
        ) * (g_solar / 1000.0)
    return model.solve_surface_temperature(variant, g_solar, air, t_sky_c, h, air_preheat_k=preheat) - air


def screen() -> list[dict]:
    """Return the 24 paired V0P/V1 rows. Base variants are never mutated (``replace()`` copies)."""
    base = {v.vid: v for v in model.build_variants()}
    v0p, v1 = base["V0P"], base["V1"]
    air = _inputs()["T_air"]
    default = (SOLAR_FACTORS[0], CONV_BOOSTS[0], CALM_PREHEATS_K[0])
    rows = []
    for case_name, g, wind, sky in CASES:
        bias_v0p = bias_c(v0p, 0.0, g, wind, sky)   # painted control: unshielded, no plate pre-heat
        for sf, cb, cp in itertools.product(SOLAR_FACTORS, CONV_BOOSTS, CALM_PREHEATS_K):
            bias_v1 = bias_c(replace(v1, solar_factor=sf, conv_boost=cb), cp, g, wind, sky)
            rows.append(dict(
                case=case_name, g_solar_w_m2=g, wind_m_s=wind, t_sky_c=sky, t_air_c=air,
                v1_solar_factor=sf, v1_conv_boost=cb, v1_calm_preheat_k=cp,
                is_default_v1=((sf, cb, cp) == default),
                bias_v0p_c=bias_v0p, bias_v1_c=bias_v1,
                abs_advantage_c=abs(bias_v0p) - abs(bias_v1)))   # > 0 => V1 closer to true ambient
    return rows


def _fmt(value):
    return f"{value:.6f}" if isinstance(value, float) else value


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--out", type=Path, required=True, help="CSV path to write (must not already exist)")
    a = ap.parse_args(argv)
    if a.out.exists():
        ap.error(f"{a.out} exists; write to a fresh path (this screen never overwrites)")
    rows = screen()
    a.out.parent.mkdir(parents=True, exist_ok=True)
    with a.out.open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=FIELDS)
        w.writeheader()
        for r in rows:
            w.writerow({k: _fmt(r[k]) for k in FIELDS})

    day_default = next(r for r in rows if r["case"] == "day" and r["is_default_v1"])
    reversals = [r for r in rows if r["abs_advantage_c"] < 0]
    print(f"wrote {a.out} ({len(rows)} paired V0P/V1 cases; illustrative screen, not measured)")
    print(f"day nominal advantage: {day_default['abs_advantage_c']:+.4f} degC "
          f"(V0P {day_default['bias_v0p_c']:+.4f}, V1 {day_default['bias_v1_c']:+.4f})")
    if reversals:
        print(f"{len(reversals)} case(s) REVERSE the nominal advantage -- V1 no longer closer to ambient:")
        for r in reversals:
            print(f"  {r['case']}: solar_factor={r['v1_solar_factor']} conv_boost={r['v1_conv_boost']} "
                  f"calm_preheat={r['v1_calm_preheat_k']}K -> advantage {r['abs_advantage_c']:+.4f} degC")
    else:
        print("no sign reversals in this finite screen")
    print("Assumptions implicated by a reversal are measurement priorities, not a hardware verdict; "
          "this screen supplies no uncertainty bound or validation band.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
