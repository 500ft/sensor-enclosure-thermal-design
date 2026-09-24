"""Study A -- nondimensional reduction: limiting behaviours, reduction accuracy, and the HONEST
regime-dependent collapse result. Numbers are SIMULATION reductions of the existing lumped model."""
import unittest
from dataclasses import replace
from analysis import thermal_bias as model
from analysis import nondimensional as ND

INP = ND._inputs()
TAIR, DTSKY, EPS = INP["T_air"], INP["T_sky_offset"], INP["eps_surface"]


def _v0():
    return model.build_variants()[0]


class GroupsAndLimitsTests(unittest.TestCase):
    def test_h_rad_linear_matches_hand_value(self):
        # 4*eps*sigma*T^3 at 30 degC, eps 0.9 -> ~5.69 W/m2K
        self.assertAlmostEqual(ND.h_rad_linear(30.0, 0.90), 5.687, places=2)

    def test_biot_flags_printed_polymers_and_clears_metal(self):
        self.assertGreater(ND.biot(7.0, 0.003, 0.13), 0.1)     # PLA wall: NOT isothermal (lumped strained)
        self.assertLess(ND.biot(7.0, 0.003, 205.0), 0.01)      # aluminium: isothermal, lumped valid

    def test_zero_bias_when_no_solar_no_internal_no_preheat_and_no_sky_depression(self):
        # dT_sky>0 must stay in the denominator; use a tiny depression and zero all drives
        v = replace(_v0(), q_internal=0.0)
        theta = ND.theta_full(v, 0.0, 5.0, 0.0, TAIR, 1e-6)
        self.assertAlmostEqual(theta * 1e-6, 0.0, places=6)    # dT -> 0

    def test_theta_increases_with_heating_number(self):
        v = _v0()
        low = ND.theta_full(v, 400.0, 1.0, 0.0, TAIR, DTSKY)
        high = ND.theta_full(v, 1000.0, 1.0, 0.0, TAIR, DTSKY)
        self.assertGreater(high, low)                          # more solar -> more bias

    def test_theta_decreases_with_wind(self):
        v = _v0()
        calm = ND.theta_full(v, 1000.0, 0.2, 0.0, TAIR, DTSKY)
        windy = ND.theta_full(v, 1000.0, 4.0, 0.0, TAIR, DTSKY)
        self.assertLess(windy, calm)                           # more convection -> less bias


class ReductionAccuracyTests(unittest.TestCase):
    def test_linear_reduction_tracks_full_solver_for_daytime_bias(self):
        # the closed-form law predicts the full nonlinear solver to a few percent for solar-driven bias
        v = _v0()
        for G, wind in [(1000, 0.5), (700, 1.0), (1000, 3.0), (600, 2.0)]:
            tf = ND.theta_full(v, G, wind, 0.0, TAIR, DTSKY)
            tl = ND.theta_linear(v, G, wind, 0.0, TAIR, DTSKY, EPS)
            self.assertLess(abs(tf - tl) / abs(tf), 0.05, f"G={G} wind={wind}: reduction off by >5%")

    def test_linearisation_underpredicts_more_as_bias_grows(self):
        # honest limit: radiation nonlinearity means the linear law drifts at large dT (documented)
        v = _v0()
        small = ND.theta_full(v, 400.0, 3.0, 0.0, TAIR, DTSKY)
        large = ND.theta_full(v, 1000.0, 0.2, 0.0, TAIR, DTSKY)
        err_small = abs(ND.theta_linear(v, 400.0, 3.0, 0.0, TAIR, DTSKY, EPS) - small)
        err_large = abs(ND.theta_linear(v, 1000.0, 0.2, 0.0, TAIR, DTSKY, EPS) - large)
        self.assertGreater(large, small)                       # sanity: larger bias case
        self.assertGreaterEqual(err_large, err_small)          # absolute reduction error grows with bias


class LinearisationErrorTests(unittest.TestCase):
    """CORRECTED 2026-09-24. These tests measure how well the LINEARISED closed form approximates
    the nonlinear solver -- approximation error. They do NOT test dimensionless similarity, and an
    exceeded threshold does not falsify a dimensionless representation (see ExactBalanceTests).
    Previously named CollapseIsRegimeDependentTests and read as a scientific kill criterion."""

    def setUp(self):
        self.samples = list(ND.doe_samples(TAIR, DTSKY, EPS))
        self.m = ND.collapse_metric([(tf, tl) for _, tf, tl, _ in self.samples], DTSKY)

    def test_doe_is_full_factorial_and_nonempty(self):
        self.assertEqual(self.m["n"], 1944)                    # 3*3*2*2*3*3*3*2

    def test_median_approximation_is_tight_but_the_tail_exceeds_the_threshold(self):
        self.assertLess(self.m["rel_median"], 0.05)            # median: good collapse (~a few %)
        self.assertLess(self.m["abs_median_c"], 0.5)           # median absolute error < 0.5 degC
        self.assertGreater(self.m["rel_p95"], 0.03)            # p95 tail exceeds the 3% approximation band
        self.assertGreater(self.m["r2"], 0.90)                 # overall R^2 still high despite tail

    def test_absolute_error_is_bounded_even_where_relative_error_explodes(self):
        # near theta~0 the relative residual is meaningless; the absolute degC residual stays bounded
        self.assertLess(self.m["abs_p95_c"], 5.0)
        self.assertGreater(self.m["rel_max"], 1.0)             # some relative residual > 100% (near-zero bias)


if __name__ == "__main__":
    unittest.main()


class ExactBalanceTests(unittest.TestCase):
    """The correction that matters: the EXACT nonlinear dimensionless balance is consistent with the
    same solver across the whole DOE. Dimensionless representation is therefore not falsified by the
    linearisation residual -- what degrades is the approximation, not the similarity."""

    def test_exact_nonlinear_balance_holds_across_the_whole_doe(self):
        from dataclasses import replace
        inp = ND._inputs()
        worst = 0.0
        base = model.build_variants()[0]
        for p, tf, tl, g in ND.doe_samples(TAIR, DTSKY, EPS):
            v = replace(base, alpha=p["alpha"], solar_factor=p["solar_factor"], a_proj=p["a_proj"],
                        a_conv=p["a_conv"], q_internal=p["q_internal"], f_sky=p["f_sky"],
                        conv_boost=1.0, eps=EPS)
            delta = 0.0
            if p["solar_factor"] < 1.0:
                delta = model.shield_air_preheat(p["wind"], inp["shield_air_preheat_calm"],
                                                 inp["preheat_wind_halflife"], forced=False) * (p["g_solar"] / 1000.0)
            worst = max(worst, abs(ND.balance_residual(v, p["g_solar"], p["wind"], delta, TAIR, DTSKY, tf)))
        self.assertLess(worst, 1e-6, f"exact balance residual {worst:.2e} exceeds solver tolerance")

    def test_nonsingular_form_is_defined_when_sky_equals_or_exceeds_ambient(self):
        # dt_sky = 0 makes the D-normalised form singular; the T0-normalised form must still work
        v = model.build_variants()[0]
        for t_sky in (TAIR, TAIR + 5.0):       # sky equal to, then warmer than, ambient
            r = ND.balance_residual_nonsingular(v, 0.0, 1.0, 0.0, TAIR, t_sky)
            self.assertLess(abs(r), 1e-6, f"nonsingular residual {r:.2e} at t_sky={t_sky}")

    def test_doe_uses_one_emissivity_for_both_sides(self):
        # regression for the 2026-09-24 bug: theta_full ignored the eps argument
        a = [tf for _, tf, _, _ in ND.doe_samples(TAIR, DTSKY, 0.9)]
        b = [tf for _, tf, _, _ in ND.doe_samples(TAIR, DTSKY, 0.5)]
        self.assertNotEqual(a, b, "theta_full must respond to the eps argument")


class RegimeDiagnosticTests(unittest.TestCase):
    """W3 diagnostic mode: regime labels are set by mechanism, the CSV is deterministic, defaults
    are never mutated, and near-zero bias never yields a meaningless relative residual."""

    def test_regime_labels_follow_the_documented_mechanism_bins(self):
        self.assertEqual(ND.regime(-0.01, DTSKY), "radiation_dominated")   # sub-ambient
        self.assertEqual(ND.regime(0.02, DTSKY), "near_zero")              # 0.4 degC
        self.assertEqual(ND.regime(0.3, DTSKY), "solar_driven")            # 6 degC
        self.assertEqual(ND.regime(1.5, DTSKY), "high_nonlinearity")       # 30 degC

    def test_every_doe_point_gets_exactly_one_regime_and_all_four_occur(self):
        labels = [ND.regime(tf, DTSKY) for _, tf, _, _ in ND.doe_samples(TAIR, DTSKY, EPS)]
        self.assertEqual(len(labels), 1944)
        self.assertEqual(set(labels), {"solar_driven", "near_zero", "radiation_dominated", "high_nonlinearity"})

    def test_doe_is_deterministic_and_does_not_mutate_model_defaults(self):
        before = [(v.vid, v.alpha, v.solar_factor, v.conv_boost, v.q_internal) for v in model.build_variants()]
        a = [(tf, tl) for _, tf, tl, _ in ND.doe_samples(TAIR, DTSKY, EPS)]
        b = [(tf, tl) for _, tf, tl, _ in ND.doe_samples(TAIR, DTSKY, EPS)]
        self.assertEqual(a, b)                                            # same order, same values
        self.assertEqual(before, [(v.vid, v.alpha, v.solar_factor, v.conv_boost, v.q_internal) for v in model.build_variants()])

    def test_csv_blanks_relative_residual_near_zero_and_refuses_overwrite(self):
        import csv, subprocess, sys, tempfile
        from pathlib import Path
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "doe.csv"
            r = subprocess.run([sys.executable, "-m", "analysis.nondimensional", "--out", str(out)],
                               cwd=Path(__file__).resolve().parents[2], capture_output=True, text=True)
            self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
            rows = list(csv.DictReader(out.open()))
            self.assertEqual(len(rows), 1944)
            self.assertIn("Pi_G", rows[0]); self.assertIn("regime", rows[0])
            for row in rows:
                if abs(float(row["dT_full_c"])) < ND.NEAR_ZERO_C:
                    self.assertEqual(row["rel_residual"], "", "near-zero bias must not report a relative residual")
                else:
                    self.assertNotEqual(row["rel_residual"], "")
            r2 = subprocess.run([sys.executable, "-m", "analysis.nondimensional", "--out", str(out)],
                                cwd=Path(__file__).resolve().parents[2], capture_output=True, text=True)
            self.assertNotEqual(r2.returncode, 0)                        # refuses to overwrite
