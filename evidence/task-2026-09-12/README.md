# EN-R03 — synthetic CSV-to-analysis rehearsal — 2026-09-12

Branch `audit/colocation-rehearsal-20260912` off `main` b200a7f. Sprint order task 6.

## What exists now
`analysis/colocation_rehearsal.py` is one workflow: generate a 1440-row synthetic co-location CSV with a **known** residual structure (bias 0.8 °C, drift 0.3 °C/day, night offset −0.5 °C, every 97th sensor value missing), run `analysis.colocation_intake` on it (hash-checked), run `compute_metrics` on the same bytes with the declared 24 h / 60 s schedule, and compare against the known answers. Known answers are computed from the values *as written* (6 dp), so the comparison is exact to 1e-12, not a fit.

## Observed run
```
intake: exit 3 SYNTHETIC_ONLY
metrics: n=1426 bias=0.699529 mae=0.699529 rmse=0.747896 paired_completeness=0.990278
known-answer comparison: ALL OK
```
`validates_thermal_model` is `false` in the intake result and in `rehearsal.json`.

## Tests (16)
Known answers: generated case exact; independent recomputation of the generator arithmetic; zero-residual case gives zero metrics; **negative control** — a wrong known answer is detected; CLI end to end.
Malformed data, each refused by the intake and stopping the chain before metrics: hash mismatch, duplicate slot, off-grid timestamp, non-chronological rows, negative/non-numeric weather, extra column, missing provenance, bad uncertainty, wrong window length. Plus: day-only data is `INCOMPLETE` (admitted, metrics still computed, night count 0); 20 % missing is `INCOMPLETE`; and a synthetic-shaped file *declared* physical is `REVIEWABLE_PILOT` with `validates_thermal_model` still `false` — the declaration is the owner's, the CLI cannot detect the mislabel.

One thing this exposed: the intake CLI exits 2 for both a refused file and an admitted-but-INCOMPLETE one; the rehearsal distinguishes them by whether a JSON result was produced, and says which.

## Checks observed (repo root on PYTHONPATH)
| command | observed |
|---|---|
| `python -m analysis.colocation_rehearsal --out-dir build/rehearsal` | exit 0 |
| `python -m unittest analysis.tests.test_colocation_rehearsal` | 16 OK |
| `python -m unittest discover -s analysis/tests` | 68 tests, 2 failures in `test_metrics_cli` that reproduce on untouched `main` in this sandbox and are green in CI |
| `python -m compileall -q analysis` / `check_literature_coverage.py` | 0 / 0 |

## Not done
No physical CSV, no field value, no thermal-model validation. EN-S02 and EN-S11 unchanged.
