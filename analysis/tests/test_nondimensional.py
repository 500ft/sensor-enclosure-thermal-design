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


class CollapseIsRegimeDependentTests(unittest.TestCase):
    """The central, honest Study A finding: the collapse is GOOD in the median/solar-driven regime
    and FAILS in the low-bias/radiation-dominated tail -- so there is no single universal clean law
    at the preregistered ~3% band (the project's own kill criterion). This is a result to report,
    not a bug to hide."""

    def setUp(self):
        self.samples = list(ND.doe_samples(TAIR, DTSKY, EPS))
        self.m = ND.collapse_metric([(tf, tl) for _, tf, tl in self.samples], DTSKY)

    def test_doe_is_full_factorial_and_nonempty(self):
        self.assertEqual(self.m["n"], 1944)                    # 3*3*2*2*3*3*3*2

    def test_median_collapse_is_tight_but_the_tail_trips_the_kill_criterion(self):
        self.assertLess(self.m["rel_median"], 0.05)            # median: good collapse (~a few %)
        self.assertLess(self.m["abs_median_c"], 0.5)           # median absolute error < 0.5 degC
        self.assertGreater(self.m["rel_p95"], 0.03)            # p95 tail: kill criterion TRIPPED
        self.assertGreater(self.m["r2"], 0.90)                 # overall R^2 still high despite tail

    def test_absolute_error_is_bounded_even_where_relative_error_explodes(self):
        # near theta~0 the relative residual is meaningless; the absolute degC residual stays bounded
        self.assertLess(self.m["abs_p95_c"], 5.0)
        self.assertGreater(self.m["rel_max"], 1.0)             # some relative residual > 100% (near-zero bias)


if __name__ == "__main__":
    unittest.main()
