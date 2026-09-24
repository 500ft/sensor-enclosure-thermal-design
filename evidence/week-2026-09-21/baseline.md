# Week 2026-09-21 — Day 1 baseline (M0) and diagnostic (W3)

Base: `main` at `84e0ef3836097206579a2eaf54e78f7549e5b6c7`, tree clean (0 dirty files).
Branch: `week/day1-direction-regime-20260921`. Local env: Python 3.11.8, numpy 2.1.1,
matplotlib 3.10.1, pandas 2.2.3, reportlab 4.5.1 — these differ from the CI pins; hosted CI is
authoritative, local results are not claimed as the pinned reproduction.
PR #20 (`docs/research-question-draft`) was OPEN and mergeable at baseline; not duplicated or edited.

## M0 gates at base (before any edit)

| Command | Result |
|---|---|
| `python -m compileall -q analysis` | exit 0 |
| `python -m unittest discover -s analysis/tests` | **100 tests OK** |
| `python analysis/check_literature_coverage.py` | Coverage complete |
| `python tools/check_presentation.py . "Sensor Enclosure Thermal Design" sensor-enclosure-thermal-design` | exit 0 |
| `python tools/test_presentation.py` | OK |
| `thermal_bias.py --no-figure --table/--night-table` → temp, `cmp` vs committed | day + night **byte-identical** |

## W3 — Study A regime diagnostic (ANALYTICAL only)

`python -m analysis.nondimensional` at candidate (regimes by mechanism: ΔT<0 radiation_dominated;
|ΔT|<1 °C near_zero; ΔT>20 °C high_nonlinearity; else solar_driven):

```
solar_driven         n=1220  abs med=0.101 p95=0.462  rel med=1.6% p95=15.9%
near_zero            n= 169  abs med=0.046 p95=0.469  rel med=18.9% p95=150.4%
radiation_dominated  n= 349  abs med=0.362 p95=0.468  rel med=23.8% p95=148.2%
high_nonlinearity    n= 206  abs med=1.938 p95=14.184  rel med=6.2% p95=19.5%
```
R² 0.972; preregistered 3% *relative* p95 kill criterion TRIPPED in every regime. Thresholds were
set from the error-vs-|ΔT| profile (abs error <0.5 °C p95 up to ~15 °C, 14 °C p95 above 25 °C),
not tuned to make any regime pass. `--out` CSV now carries the five groups, `dT_full_c`,
`abs_residual_c`, `rel_residual` (blank where |ΔT|<1 °C) and `regime`; refuses to overwrite.

## After edits

`unittest`: 104 OK (+4 `RegimeDiagnosticTests`). Thermal tables re-checked byte-identical.
No committed output changed. Inputs: ANALYTICAL/SYNTHETIC only; no HISTORICAL-EXTERNAL or
PHYSICAL-PILOT data touched.

`git diff --check` reports trailing whitespace on the appended ledger row: `SPRINT_TASKS.csv` is
CRLF throughout (all 25 rows on `main`), so the new row keeps the file's convention. Not converted,
to preserve the committed ledger bytes; recorded here rather than silently normalised.

---

> **Correction notice added 2026-09-24 (record preserved).** The numbers in this dated record are
> unchanged and were correctly reported at the time. Their *interpretation* has since been
> withdrawn: the "kill criterion TRIPPED / collapse is regime-dependent" verdict measured
> **linearisation error**, not a failure of dimensionless similarity. The exact nonlinear
> dimensionless balance is consistent with the same solver to tolerance (max residual 5.478e-9 over
> all 1,944 points). The 3 % relative band is a **selected approximation threshold**, not a
> preregistered scientific kill criterion. See
> [`docs/studyA_nondimensional.md`](../../docs/studyA_nondimensional.md) §5 and Erratum 2 in
> [`docs/PHD_SCOPE_AND_NOVELTY.md`](../../docs/PHD_SCOPE_AND_NOVELTY.md).
