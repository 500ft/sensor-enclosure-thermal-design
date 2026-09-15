"""A3 matched-control sensitivity screen: an illustrative combined-assumption check on the existing
solver. Numbers cross-check evidence/plan-review-2026-09-14 (Finding 2), same solver, same inputs."""
import tempfile, unittest
from pathlib import Path
from analysis import thermal_bias as model
from analysis import matched_control_sensitivity as S

ROOT = Path(__file__).resolve().parents[2]


def _by_combo():
    return {(r["case"], r["v1_solar_factor"], r["v1_conv_boost"], r["v1_calm_preheat_k"]): r for r in S.screen()}


class MatchedControlSensitivityTests(unittest.TestCase):
    def test_produces_24_paired_cases_eight_combos_by_three_cases(self):
        rows = S.screen()
        self.assertEqual(len(rows), 24)
        self.assertEqual(sum(1 for r in rows if r["is_default_v1"]), 3)   # one default per case

    def test_nominal_agrees_with_existing_solver_and_shows_the_documented_reversal(self):
        rows = _by_combo()
        nominal, combined = rows[("day", 0.18, 1.4, 1.2)], rows[("day", 0.30, 1.0, 2.4)]
        self.assertAlmostEqual(nominal["bias_v0p_c"], 4.4796, places=3)
        self.assertAlmostEqual(nominal["bias_v1_c"], 3.0025, places=3)
        self.assertAlmostEqual(nominal["abs_advantage_c"], 1.4771, places=3)
        self.assertAlmostEqual(combined["abs_advantage_c"], -1.5531, places=3)
        self.assertGreater(nominal["abs_advantage_c"], 0)   # nominal favors V1
        self.assertLess(combined["abs_advantage_c"], 0)     # combined perturbation reverses it

    def test_nominal_v1_bias_equals_a_direct_solver_call(self):
        inp = {n: v for n, v, *_ in model.ASSUMPTIONS}
        v1 = {v.vid: v for v in model.build_variants()}["V1"]
        h = model.h_external(0.5, inp["h_free_floor"], inp["h_wind_slope"])
        preheat = model.shield_air_preheat(0.5, 1.2, inp["preheat_wind_halflife"], forced=False) * (1000.0 / 1000.0)
        expected = model.solve_surface_temperature(v1, 1000.0, inp["T_air"], 10.0, h, air_preheat_k=preheat) - inp["T_air"]
        self.assertAlmostEqual(_by_combo()[("day", 0.18, 1.4, 1.2)]["bias_v1_c"], expected, places=12)

    def test_screen_does_not_mutate_base_variants(self):
        before = {v.vid: (v.solar_factor, v.conv_boost) for v in model.build_variants()}
        S.screen()
        after = {v.vid: (v.solar_factor, v.conv_boost) for v in model.build_variants()}
        self.assertEqual(before, after)
        self.assertEqual(before["V1"], (0.18, 1.4))         # defaults untouched

    def test_zero_solar_removes_absorptance_and_preheat_effects(self):
        # At G=0 the solar-absorptance term (alpha*solar_factor*G) and the plate pre-heat (preheat*G/1000)
        # both vanish, so V1 night bias must not depend on solar_factor or calm preheat. conv_boost still
        # legitimately matters (it is neither absorptance nor pre-heat), so group by it.
        rows = S.screen()
        for case in ("night_nominal", "night_warm_sky"):
            for cb in S.CONV_BOOSTS:
                group = {round(r["bias_v1_c"], 12) for r in rows if r["case"] == case and r["v1_conv_boost"] == cb}
                self.assertEqual(len(group), 1, f"{case} conv_boost={cb}: night V1 bias leaked solar_factor/preheat")

    def test_identical_variant_control_has_zero_contrast(self):
        b = S.bias_c({v.vid: v for v in model.build_variants()}["V0P"], 0.0, 1000.0, 0.5, 10.0)
        self.assertEqual(abs(b) - abs(b), 0.0)              # a variant compared to itself: exactly zero

    def test_screen_is_not_an_argument_that_v1_always_wins(self):
        rows = S.screen()                                   # must contain both signs; not a one-sided search
        self.assertTrue(any(r["abs_advantage_c"] < 0 for r in rows))
        self.assertTrue(any(r["abs_advantage_c"] > 0 for r in rows))

    def test_cli_writes_to_a_fresh_path_and_refuses_an_existing_one(self):
        import subprocess, sys
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "sub" / "screen.csv"
            r = subprocess.run([sys.executable, "-m", "analysis.matched_control_sensitivity", "--out", str(out)],
                               cwd=ROOT, capture_output=True, text=True)
            self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
            self.assertEqual(len(out.read_text().strip().splitlines()), 25)   # header + 24 rows
            r2 = subprocess.run([sys.executable, "-m", "analysis.matched_control_sensitivity", "--out", str(out)],
                                cwd=ROOT, capture_output=True, text=True)
            self.assertNotEqual(r2.returncode, 0)           # refuses to overwrite an existing file


if __name__ == "__main__":
    unittest.main()
