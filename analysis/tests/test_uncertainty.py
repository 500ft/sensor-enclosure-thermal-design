"""T2 -- known-answer fixtures for linear uncertainty propagation.

Expected values are derived by hand in the docstrings, never copied from the implementation.
"""
import math
import unittest

from analysis.uncertainty import (Input, Result, UncertaintyError, combine, covariance_from,
                                  difference, validate_covariance)


def _probe(name, u, unit="degC", prov="calibration certificate"):
    return Input(name=name, value=0.0, u=u, unit=unit, provenance=prov)


class SharedReferenceTests(unittest.TestCase):
    """Fixture 1. A, B each u=0.1 degC; shared reference R u=0.2 degC; inputs independent.

    absolute bias  b_A = A - R  -> u = sqrt(0.1^2 + 0.2^2) = sqrt(0.05)  = 0.2236068
    contrast b_A - b_B = A - B  -> u = sqrt(0.1^2 + 0.1^2) = sqrt(0.02)  = 0.1414214
    R cancels ALGEBRAICALLY in the contrast because it is the same node -- not by a rule.
    """

    def setUp(self):
        self.ins = [_probe("A", 0.1), _probe("B", 0.1), _probe("R", 0.2)]

    def test_absolute_bias_carries_the_reference_in_full(self):
        r = combine(self.ins, {"A": 1.0, "R": -1.0})
        self.assertAlmostEqual(r.u_c, math.sqrt(0.05), places=9)
        self.assertAlmostEqual(r.u_c, 0.2236068, places=6)

    def test_difference_cancels_the_shared_reference_exactly(self):
        r = difference(self.ins, "A", "B", shared_reference="R")
        self.assertAlmostEqual(r.u_c, math.sqrt(0.02), places=9)
        self.assertAlmostEqual(r.u_c, 0.1414214, places=6)

    def test_difference_is_smaller_than_either_absolute_bias(self):
        abs_u = combine(self.ins, {"A": 1.0, "R": -1.0}).u_c
        self.assertLess(difference(self.ins, "A", "B", shared_reference="R").u_c, abs_u)

    def test_shared_reference_must_be_a_real_node(self):
        with self.assertRaises(UncertaintyError):
            difference(self.ins, "A", "B", shared_reference="some_other_reference")


class CovarianceSignTests(unittest.TestCase):
    """Fixture 2. Two unit-u inputs with r = 0.5.

    sum:        u^2 = 1 + 1 + 2(0.5) = 3      -> sqrt(3)
    difference: u^2 = 1 + 1 - 2(0.5) = 1      -> 1
    Positive correlation INCREASES a sum and DECREASES a difference. This is the direction the
    pilot spec originally got backwards, so it is pinned here.
    """

    def setUp(self):
        self.ins = [_probe("x1", 1.0), _probe("x2", 1.0)]
        self.corr = {("x1", "x2"): 0.5}

    def test_sum_increases_with_positive_correlation(self):
        r = combine(self.ins, {"x1": 1.0, "x2": 1.0}, correlations=self.corr)
        self.assertAlmostEqual(r.u_c, math.sqrt(3.0), places=12)

    def test_difference_decreases_with_positive_correlation(self):
        r = combine(self.ins, {"x1": 1.0, "x2": -1.0}, correlations=self.corr)
        self.assertAlmostEqual(r.u_c, 1.0, places=12)

    def test_ignoring_positive_correlation_overstates_a_difference(self):
        with_corr = combine(self.ins, {"x1": 1.0, "x2": -1.0}, correlations=self.corr).u_c
        without = combine(self.ins, {"x1": 1.0, "x2": -1.0}).u_c
        self.assertLess(with_corr, without)          # sqrt(2) > 1

    def test_covariance_terms_are_reported_separately_and_may_be_negative(self):
        r = combine(self.ins, {"x1": 1.0, "x2": -1.0}, correlations=self.corr)
        self.assertEqual(set(r.variance_terms), {"x1", "x2"})
        self.assertLess(r.covariance_terms[("x1", "x2")], 0.0)


class GumResistorTests(unittest.TestCase):
    """Fixture 3. Ten 1000-ohm resistors in SERIES, each u = 0.1 ohm (GUM 5.2.2 basis).

    perfectly shared calibration (r = +1): u = sum(u_i)          = 1.0 ohm
    independent errors:                    u = sqrt(10 * 0.01)   = sqrt(0.1) = 0.3162278 ohm
    """

    def setUp(self):
        self.ins = [_probe(f"R{i}", 0.1, unit="ohm") for i in range(10)]
        self.sens = {f"R{i}": 1.0 for i in range(10)}

    def test_independent_errors_add_in_quadrature(self):
        r = combine(self.ins, self.sens)
        self.assertAlmostEqual(r.u_c, math.sqrt(0.1), places=9)
        self.assertAlmostEqual(r.u_c, 0.3162278, places=6)

    def test_perfectly_shared_calibration_adds_linearly_in_a_sum(self):
        corr = {(f"R{i}", f"R{j}"): 1.0 for i in range(10) for j in range(i + 1, 10)}
        r = combine(self.ins, self.sens, correlations=corr)
        self.assertAlmostEqual(r.u_c, 1.0, places=9)


class InputValidationTests(unittest.TestCase):
    """Fixture 4. u=0 accepted with provenance; negative/NaN/inf/missing rejected."""

    def test_zero_uncertainty_accepted_with_provenance(self):
        x = Input("exact", 1.0, 0.0, "degC", provenance="defined constant")
        self.assertEqual(combine([x], {"exact": 1.0}).u_c, 0.0)

    def test_zero_uncertainty_without_provenance_rejected(self):
        with self.assertRaises(UncertaintyError):
            Input("bare", 1.0, 0.0, "degC", provenance="")

    def test_negative_nan_inf_and_missing_rejected(self):
        for bad in (-0.1, float("nan"), float("inf"), None):
            with self.assertRaises(UncertaintyError):
                Input("bad", 1.0, bad, "degC", provenance="p")

    def test_singular_shared_reference_covariance_is_preserved(self):
        # perfectly correlated pair -> singular Sigma, physically required, must NOT be rejected
        ins = [_probe("a", 0.2), _probe("b", 0.2)]
        sigma = covariance_from(ins, {("a", "b"): 1.0})
        self.assertTrue(validate_covariance(sigma))
        self.assertAlmostEqual(combine(ins, {"a": 1.0, "b": -1.0}, sigma=sigma).u_c, 0.0, places=12)


class PositiveSemidefiniteTests(unittest.TestCase):
    """Fixture 5. r = (0.9, 0.9, -0.9) is individually legal but NOT jointly possible."""

    def test_pairwise_legal_but_jointly_impossible_matrix_is_rejected(self):
        ins = [_probe("a", 1.0), _probe("b", 1.0), _probe("c", 1.0)]
        with self.assertRaises(UncertaintyError) as ctx:
            covariance_from(ins, {("a", "b"): 0.9, ("a", "c"): 0.9, ("b", "c"): -0.9})
        self.assertIn("semidefinite", str(ctx.exception).lower())

    def test_each_of_those_correlations_is_individually_legal(self):
        ins = [_probe("a", 1.0), _probe("b", 1.0)]
        for r in (0.9, -0.9):
            self.assertTrue(validate_covariance(covariance_from(ins, {("a", "b"): r})))

    def test_asymmetric_matrix_rejected(self):
        with self.assertRaises(UncertaintyError):
            validate_covariance([[1.0, 0.5], [0.4, 1.0]])


class DistinctReferenceTests(unittest.TestCase):
    """Fixture 6. Distinct references do not invalidate a contrast -- only the shortcut is refused."""

    def test_distinct_references_accepted_with_an_explicit_covariance_model(self):
        ins = [_probe("A", 0.1), _probe("B", 0.1), _probe("R1", 0.2), _probe("R2", 0.2)]
        r = combine(ins, {"A": 1.0, "R1": -1.0, "B": -1.0, "R2": 1.0},
                    correlations={("R1", "R2"): 0.5})
        # u^2 = 0.01+0.01+0.04+0.04 + 2(-1)(1)(0.5*0.2*0.2) = 0.10 - 0.04 = 0.06
        self.assertAlmostEqual(r.u_c, math.sqrt(0.06), places=9)

    def test_automatic_common_reference_shortcut_refused_for_distinct_nodes(self):
        ins = [_probe("A", 0.1), _probe("B", 0.1), _probe("R1", 0.2), _probe("R2", 0.2)]
        with self.assertRaises(UncertaintyError):
            difference(ins, "A", "B", shared_reference="R1_and_R2")

    def test_duplicate_input_names_refused(self):
        with self.assertRaises(UncertaintyError):
            combine([_probe("R", 0.1), _probe("R", 0.2)], {"R": 1.0})

    def test_mixed_units_refused_unless_declared(self):
        ins = [_probe("t", 0.1, unit="degC"), _probe("p", 0.1, unit="Pa")]
        with self.assertRaises(UncertaintyError):
            combine(ins, {"t": 1.0, "p": 1.0})
        self.assertAlmostEqual(combine(ins, {"t": 1.0, "p": 1.0}, unit="mixed").u_c,
                               math.sqrt(0.02), places=9)


class CoverageTests(unittest.TestCase):
    """Fixture 7. A result with no justified coverage probability never prints 95 %."""

    def setUp(self):
        self.ins = [_probe("A", 0.1), _probe("R", 0.2)]
        self.sens = {"A": 1.0, "R": -1.0}

    def test_no_basis_means_probability_unspecified_and_never_95(self):
        r = combine(self.ins, self.sens, k=2.0)
        self.assertAlmostEqual(r.U, 2.0 * r.u_c, places=12)
        self.assertIsNone(r.coverage_probability)
        self.assertNotIn("95", r.report())
        self.assertIn("UNSPECIFIED", r.report())

    def test_supplied_basis_is_reported_verbatim(self):
        r = combine(self.ins, self.sens, k=2.0, coverage_basis="GUM G.6.6 conditions demonstrated")
        self.assertIn("G.6.6", r.report())

    def test_standard_uncertainty_always_available_without_any_coverage_claim(self):
        r = combine(self.ins, self.sens)
        self.assertGreater(r.u_c, 0.0)
        self.assertIsNone(r.U)
        self.assertNotIn("95", r.report())

    def test_invalid_k_rejected(self):
        for bad in (0.0, -2.0, float("inf")):
            with self.assertRaises(UncertaintyError):
                combine(self.ins, self.sens, k=bad)


if __name__ == "__main__":
    unittest.main()
