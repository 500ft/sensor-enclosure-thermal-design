# Implementation evidence — 2026-09-16 (A1/A2/A3 from DAY_PLAN_2026-09-15)

Base: `main` at `cf1a8fa` (plan PR #17 merged). Implementation branch:
`impl/pilot-readiness-a1a2a3-20260916`. Python 3.11.8, existing analysis environment; local
dependency versions differ from `requirements.txt` CI pins — hosted CI is authoritative. Synthetic
fixtures only; no physical data, permissions, or outside exports were accessed. This is agent
implementation, not independent human scientific validation.

## A1 — refusal now precedes generation writes (`analysis/colocation_rehearsal.py`)

Defect (reproduced at base): the generation CLI called `write_inputs()` into `--out-dir` **before**
`snapshot()` checked for a collision, so a refused rerun exited 5 yet still overwrote the previous
run's `rehearsal.csv` / `rehearsal.metadata.json`. The prior report and snapshot survived; the
inputs did not.

Base reproduction (first run uses `bias_c=2.0` so an overwrite cannot hide behind identical bytes):

```json
{ "rerun_exit": 5, "changed_files": ["rehearsal.csv", "rehearsal.metadata.json"],
  "source_csv_matches_saved_report": false }
```

Fix: added `require_free_output()` (refuses, before any write, if `--out-dir` already holds
`rehearsal.csv`/`.metadata.json`/`rehearsal.json`/`snapshot`; resolves symlinks; leaves unrelated
files and a fresh/empty dir alone) and moved generate→write→rehearse inside the `CollisionError`
try-block. `snapshot()` is unchanged and still guards the rehearse step and external-input replays.
Smallest change consistent with the existing checks — no transaction or locking framework.

After fix, the same rerun exits 5 with `changed_files: []` (including an unrelated sentinel),
`source_csv_matches_saved_report: true`; fresh generation still exits 0, `SYNTHETIC_ONLY`, `ALL OK`.

Regression: `GenerationRefusalTests` (4 tests) in `analysis/tests/test_colocation_rehearsal.py`,
driven through the real `python -m analysis.colocation_rehearsal` CLI, comparing a recursive
path→sha256 manifest before/after a refused command. Proof they are meaningful: run against the
unfixed source from `main`, the three collision cases FAIL (`FAILED (failures=3)`); against the fix,
all pass. The fourth (fresh/empty dir works, unrelated files survive) is a functional guard.

## A2 — corrected `EN-R03S` mis-attribution (`docs/SPRINT_PROGRESS.md`)

The 2026-09-11 summary named `EN-R03S` for "actual co-location acquisition/review blocked."
Per the ledger that is `EN-R03` (Owner, blocked); `EN-R03S` is the separate synthetic rehearsal
added 2026-09-12 and marked done (it did not exist on 2026-09-11). Corrected the ID inline and left
a dated `[Corrected 2026-09-16: …]` marker distinguishing the two evidence routes. Dated historical
entries, ledger statuses, and ledger bytes are otherwise unchanged; `LedgerIntegrityTests` pass.

## A3 — matched-control sensitivity screen (optional; `analysis/matched_control_sensitivity.py`)

Finite 24-case screen (8 illustrated V1 assumption combinations × 3 operating cases) on the existing
solver. Reproduces the review's Finding 2: day-case nominal absolute-bias advantage of V1 over the
painted control V0P is **+1.4771 °C** (V0P +4.4796, V1 +3.0025); combining all three illustrated V1
perturbations (`solar_factor` 0.30, `conv_boost` 1.0, calm pre-heat 2.4 K) reverses it to
**−1.5531 °C** (V1 +6.0327). At G=0, night V1 bias is independent of `solar_factor`/pre-heat
(absorptance and pre-heat terms vanish); `conv_boost` still matters. 3 of 24 cases reverse the
nominal advantage. Tests: `test_matched_control_sensitivity.py` (8 tests) — nominal/solver
agreement, no base-variant mutation, zero-solar removal, identical-variant zero-contrast control,
both-signs-present, and the fresh-path CLI. Illustrative only: no uncertainty bound or validation
band. Reproduce: `python -m analysis.matched_control_sensitivity --out <fresh-path>.csv`. Results
section appended to `analysis/thermal_bias_results.md`.

## Verification

| Check | Result |
| --- | --- |
| `python -m unittest discover -s analysis/tests` | 90 passed (was 78; +4 A1, +8 A3) |
| `python -m compileall -q analysis` | exit 0 |
| `python analysis/check_literature_coverage.py` | coverage complete (26/26) |
| `python tools/check_presentation.py …` / `tools/test_presentation.py` | exit 0; 4 presentation tests pass |
| thermal day/night tables regenerated to temp dir | byte-identical to committed outputs |
| new-test regression proof vs unfixed `main` source | `FAILED (failures=3)`, as intended |

## What remains open (unchanged by this software work)

- **O1** (historic deployment provenance, `EN-S02`) and **O2** (prospective pilot decision) are
  owner/PI actions; not performed here. `EN-S02`, `EN-S09B`, `EN-S11`, `EN-R03` stay blocked;
  `EN-R03`'s dependency on `EN-S02` is unchanged (no silent bypass).
- CAD work orders stay deferred; the FEA module stays a stub (kept per the plan).
- No experiment, outreach, acquisition, spend, or physical-validation claim is part of this change.
