#!/usr/bin/env python3
"""T2 -- combined standard uncertainty by linear propagation (GUM 100:2008).

A small linear covariance calculation, deliberately NOT a symbolic metrology engine:

    u_c^2 = c^T Sigma c            (single output)
    Sigma_y = J Sigma J^T          (several outputs)

`c` (or `J`) is supplied explicitly. Distribution names and evaluation method (Type A/B) are
recorded as *provenance for how u was obtained* -- this module never infers `u` from a distribution
name and never evaluates a free-text equation.

What it refuses to do, and why (each is a way uncertainty budgets go quietly wrong):
  - default a missing uncertainty to zero;
  - accept a covariance matrix that is not positive semidefinite, even when every pairwise
    correlation is individually legal;
  - apply the identical-reference cancellation to inputs that are not the same node;
  - print a coverage probability that no supplied basis justifies.

A shared reference is represented as the SAME input node, so for y1 = A - R and y2 = B - R the
contrast y1 - y2 = A - B cancels R *algebraically*. Other error sources do not thereby cancel.
Monte Carlo propagation (JCGM 101:2008) is out of scope.
"""
from __future__ import annotations

import math
from dataclasses import dataclass, field

PSD_TOL = 1e-9          # eigenvalue floor, relative to the largest diagonal entry
SYM_TOL = 1e-12


class UncertaintyError(ValueError):
    """An input the budget cannot honestly accept."""


@dataclass(frozen=True)
class Input:
    """One input quantity. `u` is the standard uncertainty; `provenance` says how it was obtained."""
    name: str
    value: float
    u: float
    unit: str
    provenance: str
    evaluation: str = "B"          # 'A' or 'B' -- HOW u was evaluated, not a property of the effect

    def __post_init__(self):
        if not math.isfinite(self.value):
            raise UncertaintyError(f"{self.name}: value must be finite")
        if self.u is None or not math.isfinite(self.u):
            raise UncertaintyError(f"{self.name}: u must be finite and present -- a missing "
                                   "uncertainty is never treated as zero")
        if self.u < 0:
            raise UncertaintyError(f"{self.name}: u must be >= 0, got {self.u}")
        if self.u == 0 and not self.provenance:
            raise UncertaintyError(f"{self.name}: u = 0 is accepted only with explicit provenance "
                                   "(exact input or deliberate model treatment)")
        if self.evaluation not in ("A", "B"):
            raise UncertaintyError(f"{self.name}: evaluation must be 'A' or 'B'")


def _eigvals_sym(m):
    """Eigenvalues of a small real symmetric matrix via the cyclic Jacobi method (stdlib only)."""
    n = len(m)
    a = [row[:] for row in m]
    for _ in range(100):
        off = math.sqrt(sum(a[i][j] ** 2 for i in range(n) for j in range(n) if i != j))
        if off <= 1e-14:
            break
        for p in range(n - 1):
            for q in range(p + 1, n):
                if abs(a[p][q]) <= 1e-18:
                    continue
                theta = (a[q][q] - a[p][p]) / (2.0 * a[p][q])
                t = (1.0 if theta >= 0 else -1.0) / (abs(theta) + math.sqrt(theta * theta + 1.0))
                c = 1.0 / math.sqrt(t * t + 1.0)
                s = t * c
                for k in range(n):
                    akp, akq = a[k][p], a[k][q]
                    a[k][p], a[k][q] = c * akp - s * akq, s * akp + c * akq
                for k in range(n):
                    apk, aqk = a[p][k], a[q][k]
                    a[p][k], a[q][k] = c * apk - s * aqk, s * apk + c * aqk
    return [a[i][i] for i in range(n)]


def validate_covariance(sigma, names=None):
    """Reject a covariance matrix that cannot be honest. Singular matrices are PRESERVED.

    A physically required singular Sigma (e.g. a perfectly shared reference) is valid and must not
    be rejected; only *negative* directions are impossible.
    """
    n = len(sigma)
    if any(len(r) != n for r in sigma):
        raise UncertaintyError("covariance must be square")
    if names is not None and len(names) != n:
        raise UncertaintyError("covariance dimension does not match the input list")
    for i in range(n):
        for j in range(n):
            if not math.isfinite(sigma[i][j]):
                raise UncertaintyError("covariance entries must be finite")
    for i in range(n):
        if sigma[i][i] < 0:
            raise UncertaintyError(f"negative variance on the diagonal at index {i}")
    scale = max((sigma[i][i] for i in range(n)), default=1.0) or 1.0
    for i in range(n):
        for j in range(i + 1, n):
            if abs(sigma[i][j] - sigma[j][i]) > SYM_TOL * max(1.0, scale):
                raise UncertaintyError(f"covariance is not symmetric at ({i},{j})")
            bound = math.sqrt(sigma[i][i] * sigma[j][j])
            if abs(sigma[i][j]) > bound * (1.0 + 1e-9):
                raise UncertaintyError(
                    f"|cov({i},{j})| exceeds sqrt(var_i*var_j): correlation outside [-1,1]")
    # pairwise legality is necessary but NOT sufficient -- check the whole matrix
    if n > 1 and min(_eigvals_sym(sigma)) < -PSD_TOL * scale:
        raise UncertaintyError(
            "covariance is not positive semidefinite: every pairwise correlation can be legal "
            "while the matrix as a whole is impossible")
    return True


def covariance_from(inputs, correlations=None):
    """Build Sigma from standard uncertainties plus optional pairwise correlations {(a,b): r}."""
    idx = {x.name: i for i, x in enumerate(inputs)}
    n = len(inputs)
    sigma = [[0.0] * n for _ in range(n)]
    for i, x in enumerate(inputs):
        sigma[i][i] = x.u ** 2
    for (a, b), r in (correlations or {}).items():
        if a not in idx or b not in idx:
            raise UncertaintyError(f"correlation names unknown: {a}, {b}")
        if not (-1.0 <= r <= 1.0):
            raise UncertaintyError(f"correlation r({a},{b}) = {r} outside [-1,1]")
        i, j = idx[a], idx[b]
        cov = r * inputs[i].u * inputs[j].u
        sigma[i][j] = sigma[j][i] = cov
    validate_covariance(sigma, [x.name for x in inputs])
    return sigma


@dataclass
class Result:
    u_c: float
    unit: str
    variance_terms: dict = field(default_factory=dict)      # per-input c_i^2 * var_i
    covariance_terms: dict = field(default_factory=dict)    # per-pair 2*c_i*c_j*cov_ij (may be < 0)
    k: float | None = None
    U: float | None = None
    coverage_basis: str | None = None

    @property
    def coverage_probability(self):
        """Never asserted without a supplied basis. `None` means unspecified, not 95 %."""
        return None if not self.coverage_basis else self.coverage_basis

    def report(self):
        s = f"u_c = {self.u_c:.7g} {self.unit}"
        if self.U is not None:
            s += (f"; U = {self.U:.7g} {self.unit} at k = {self.k}"
                  f" (basis: {self.coverage_basis})" if self.coverage_basis
                  else f"; U = {self.U:.7g} {self.unit} at k = {self.k} (supplied; "
                       "coverage probability UNSPECIFIED)")
        return s


def combine(inputs, sensitivities, sigma=None, correlations=None, unit=None,
            k=None, coverage_basis=None):
    """Combined standard uncertainty for one output.

    `sensitivities` maps input name -> c_i = dy/dx_i. Inputs omitted from it take c_i = 0.
    Variance and covariance contributions are returned SEPARATELY: a covariance term may be
    negative, so a single set of positive 'percentage shares' would mislead.
    """
    names = [x.name for x in inputs]
    if len(set(names)) != len(names):
        raise UncertaintyError("input names must be unique -- a shared reference is ONE node")
    unknown = set(sensitivities) - set(names)
    if unknown:
        raise UncertaintyError(f"sensitivities reference unknown inputs: {sorted(unknown)}")
    units = {x.unit for x in inputs if sensitivities.get(x.name)}
    if unit is None:
        if len(units) != 1:
            raise UncertaintyError(f"cannot infer output unit from mixed inputs {sorted(units)}; "
                                   "pass unit= explicitly")
        unit = units.pop()
    if sigma is None:
        sigma = covariance_from(inputs, correlations)
    else:
        if correlations:
            raise UncertaintyError("pass either sigma= or correlations=, not both")
        validate_covariance(sigma, names)

    c = [float(sensitivities.get(n, 0.0)) for n in names]
    var_terms, cov_terms, total = {}, {}, 0.0
    for i, n in enumerate(names):
        t = c[i] * c[i] * sigma[i][i]
        if c[i]:
            var_terms[n] = t
        total += t
    for i in range(len(names)):
        for j in range(i + 1, len(names)):
            t = 2.0 * c[i] * c[j] * sigma[i][j]
            if t:
                cov_terms[(names[i], names[j])] = t
            total += t
    if total < 0:
        if total < -PSD_TOL * max(1.0, abs(total)):
            raise UncertaintyError("negative combined variance -- covariance model is inconsistent")
        total = 0.0
    res = Result(u_c=math.sqrt(total), unit=unit, variance_terms=var_terms, covariance_terms=cov_terms)
    if k is not None:
        if k <= 0 or not math.isfinite(k):
            raise UncertaintyError("coverage factor k must be finite and positive")
        res.k, res.U, res.coverage_basis = float(k), float(k) * res.u_c, coverage_basis
    return res


def difference(inputs, a, b, shared_reference=None, sigma=None, correlations=None,
               k=None, coverage_basis=None):
    """Uncertainty of (a - b).

    If `shared_reference` names an input, it is the SAME node in both measurement equations, so it
    cancels algebraically (c = 0 in the contrast). That is the only cancellation performed: nothing
    else is assumed to cancel. With distinct references, supply the covariance model instead -- the
    contrast is still valid; what is refused is the automatic identical-reference shortcut.
    """
    names = {x.name for x in inputs}
    for n in (a, b):
        if n not in names:
            raise UncertaintyError(f"unknown input {n!r}")
    if shared_reference is not None and shared_reference not in names:
        raise UncertaintyError(
            f"shared_reference {shared_reference!r} is not an input node. Represent a shared "
            "reference as one node; do not apply the identical-reference formula to distinct ones.")
    sens = {a: 1.0, b: -1.0}          # a shared reference appears in both and cancels: c = 0
    return combine(inputs, sens, sigma=sigma, correlations=correlations,
                   k=k, coverage_basis=coverage_basis)
