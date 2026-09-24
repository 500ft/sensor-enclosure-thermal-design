# Weekly evidence packet — week of 2026-09-21 (F1–F4)

**Scope of this packet: planning, literature and specification only.** No physical validation, no
owner/PI gate closed by software, no private data added. Every numerical result below is
**ANALYTICAL** (model output) or **SYNTHETIC** (generated fixture). No HISTORICAL-EXTERNAL or
PHYSICAL-PILOT data exists in this repository.

## Commits

| | SHA |
|---|---|
| Week baseline (Day 1 start) | `84e0ef3` |
| `main` at packet time | `5b5ec24` |
| Candidate (this branch, stacked on PR #32) | `1e14d51` |

Local env: Python 3.11.8, numpy 2.1.1, matplotlib 3.10.1, pandas 2.2.3, reportlab 4.5.1 — these
differ from the CI pins; **hosted CI is authoritative and local results are not claimed as the
pinned reproduction.**

## What changed this week, and why

| PR | Day | Change | Why |
|---|---|---|---|
| #21 | Mon | Research-direction decision record; Study A regime diagnostic | Two research questions coexisted; and the collapse needed a failure map |
| #22 | Tue | Six competitors read in full; competitor matrix; K2 benchmark defined | The novelty argument was abstract-level; **two author mis-citations found and corrected** |
| #23 | Wed | Study B CHT design + dimensionless extension contract | Section 9 CAD amendment; a thermal benchmark must precede any CHT claim |
| #25 | — | 27 further sources; model-input provenance table; **Biot table corrected** | The model's own constants were uncited; the handbook PLA `k` was wrong |
| #29, #31 | — | `setup-python@v7`, `checkout@v7` | Dependabot; #31 supersedes #30 (unrebaseable after #29) |
| #32 | Thu | Pilot design, data contract, uncertainty budget, owner packet | Task 3 (P0.3) |
| *(this)* | Fri | F1 consistency review, F2 gates, F3 packet | Integration |

## F1 — cross-document consistency

14 automated checks pass. Six flags were raised and **all six were individually inspected and
confirmed false positives**; none was dismissed without reading the line.

| Flag | Verdict |
|---|---|
| `10 %` in pilot spec read as a coverage threshold | **False positive** — it is `berdahlbretz1997`'s "10 % accuracy in `(h_r + h_c)` is not feasible", an uncertainty statement |
| 4 × "universal" in scope/direction/Study-B docs | **False positive** — one is "rather than assuming universality"; one describes the *falsified* claim; one is the **prohibited-wording column** of the claim matrix; one is "not a universal tolerance" split across lines |
| `EN-R03S` near "blocked acquisition" in `SPRINT_PROGRESS.md` | **False positive** — it is the 2026-09-16 erratum quoting the error it corrects |

**Known weaknesses of the checker** (recorded so the next run is not falsely reassured): it is
line-scoped, so a negation on the previous line is missed; and it cannot distinguish a coverage
percentage from an uncertainty percentage.

Checks that passed: thresholds quoted from the protocol not redefined · no new coverage percentage
introduced · `EN-R03S` never equated with physical acquisition · the simulated 1.4771 °C never used
as a threshold · every ProConsList entry carries an evidence boundary · full-read-pending entries
flagged (`churchill1975`, `barcohen1984`) · bib = ProConsList = matrix = 59 · all relative links
resolve (0 broken) · ledger IDs unique, 13 columns.

## F2 — full gate set

| # | Command | Result |
|---|---|---|
| 1 | `python -m compileall -q analysis` | exit 0 |
| 2 | `python -m unittest discover -s analysis/tests` | **104 passed** |
| 3 | `python analysis/check_literature_coverage.py` | 59/59, complete |
| 4 | `python tools/check_presentation.py …` | exit 0 |
| 5 | `python tools/test_presentation.py` | OK |
| 6 | `python -m analysis.nondimensional` | R² 0.97217; **kill criterion TRIPPED** (regime-dependent, as documented) |
| 7 | `python -m analysis.matched_control_sensitivity --out <fresh>` | 24 paired cases; nominal advantage +1.4771 °C |
| 8–9 | thermal day/night tables regenerated to a temp dir, `diff` | **byte-identical** |
| 10 | `git diff --check` | exit 0 |

All outputs written to a fresh temporary directory; **no committed artifact was modified.**

## Literature source status

59 sources, 1:1 with ProConsList and the matrix. **57 read in full**; **2 full-read pending**
(`churchill1975`, `barcohen1984` — paywalled, bibliographic identity verified, **no content
attributed**). Non-archival venues flagged in-place: `sonin2001` (course monograph), `ostrach1953`
(NACA report), `morgan2017` (unreviewed LANL report), `ishizuka2012` (conference proceedings).
Preprint / author-manuscript reads declared per entry.

## Study A diagnostic result (ANALYTICAL)

| Regime | n | abs med / p95 | rel med / p95 |
|---|---:|---|---|
| solar_driven | 1220 | 0.10 / 0.46 °C | 1.6 % / 15.9 % |
| near_zero | 169 | 0.05 / 0.47 °C | n/a |
| radiation_dominated | 349 | 0.36 / 0.47 °C | n/a |
| high_nonlinearity (ΔT>20 °C) | 206 | **1.9 / 14.2 °C** | 6.2 % / 19.5 % |

The preregistered 3 % relative kill criterion is **tripped in every regime**. Reported as the
result, not softened.

## Corrections this week found in already-merged work

1. **Two author mis-citations** from the abstract-level novelty scan: the competitor is **Bernard
   et al. 2019** (not "Barbaresco"); the PurpleAir T/RH paper is **Couzo et al. 2024** (not "Cha").
   **Barkjohn 2021 measures no T/RH at all.** Corrected in place with a visible erratum.
2. **The Biot table used handbook bulk `k`.** Three labs measured printed PLA at 0.182–0.267 W/mK,
   not 0.13 — the old table **inflated Bi by 40–105 %**. Rebuilt on measured values; the claim is
   retained and better supported, with the mechanism reattributed to through-layer anisotropy
   (1.60), infill pattern and foaming filaments.
3. **Three further model constants are unsupported or mis-referenced** (`T_sky` fixed 20 K;
   `h = 5.0 + 4.0·U`; `eps`; `alpha` dark). **Recorded, not silently applied** — changing them moves
   every published number, so it is an owner decision.

## Owner-gated decisions still pending

All 15 rows of [`OWNER_DECISIONS_2026-09-24.md`](../../docs/OWNER_DECISIONS_2026-09-24.md) are
`open`, including: Direction A vs B; kill criterion relative → absolute; CAD tooling rewording;
whether the historical-log request may be sent; whether a pilot is permitted in principle; and
whether CI Python may move to ≥3.12 (which would unblock dependabot #27/#28 but could change the
byte-exact thermal tables). `EN-S02`, `EN-S09B`, `EN-S11`, `EN-R03` remain blocked; all nine CAD
tasks remain `deferred`; FEA remains a stub.

## What remains simulation-only

Every number this project has produced. The five-group law, the regime map, the 24-case control
screen and the Biot envelope are all model outputs or handbook/measured *material* properties — none
is a measurement of this enclosure. The pilot that would change that is specified but **not
authorised**.

## What was not attempted, and why

- **CAD authoring — not attempted.** `EN-CAD-02` (owner inventory of actual enclosure geometry) is
  the blocking predecessor and is `deferred`; seven geometry entries are `TODO-from-lab` and **no
  enclosure dimension is accepted**. Modelling now would require inventing dimensions, which the
  weekly plan explicitly prohibits. The CAD host is configured but there is nothing to model.
- **Solver/toolchain install — not attempted.** Explicitly out of scope for the week.
- **numpy/pandas dependabot PRs — not merged.** Their branches add `contourpy==1.4.0`, which needs
  Python ≥3.12 while CI pins 3.11; merging would break `main`.
- **Owner/PI actions — not performed.** No request sent, no permission assumed, no decision closed.

## Next exact command

```
PYTHONPATH=. python -m unittest discover -s analysis/tests
```

**Next gate:** the owner answers row 13 (Direction A or B) in `OWNER_DECISIONS_2026-09-24.md`. Until
then the agent-buildable queue is empty of unblocked substantive work — the remaining items are the
manifest validator (needs an approved implementation PR) and Study B's CHT half (needs a toolchain
allocation).
