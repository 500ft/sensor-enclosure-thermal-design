# Implementation tickets (WP4, 2026-09-24)

**Status: specifications, not implementations.** Each ticket gives affected files, an input/output
contract, **meaningful failure cases** (a test that cannot fail is not a test), and the evidence that
would close it. **None may be implemented without an approved PR**, and none closes an owner gate.

Three tickets from the critique are **already done** and are recorded here for traceability:

| Done | Where |
|---|---|
| `eps` input consistency in `doe_samples` | PR #34 — `theta_full` ignored the `eps` argument |
| Exact nonlinear dimensionless diagnostic | PR #34 — `nondimensional.balance_residual` |
| Non-singular normalisation | PR #34 — `balance_residual_nonsingular`, valid when `T_sky >= T_air` |

---

## T1 — Campaign manifest and cross-variant pairing

**Affected:** new `analysis/campaign_manifest.py`; `analysis/tests/test_campaign_manifest.py`.
**Must not touch:** `analysis/colocation_intake.py` (the validated single-pair intake stays
byte-compatible; a compatibility test proves it).

**Input:** a manifest file (fields fixed in `pilot-design-2026-09-24.md` R2.2) plus the per-variant
CSV and metadata paths it names.
**Output:** a pairing report — per-arm coverage, **per-contrast** valid-timestamp sets, all-arm
complete cases, and a missingness summary keyed by temperature and power state.

**Failure cases the tests must exercise (each must fail loudly, not degrade):**
1. A manifest naming a CSV whose recorded `csv_sha256` does not match the file on disk.
2. Two arms whose declared cadence or intended window differ.
3. A timestamp present in one arm and absent in another — must be **dropped from the cross-variant
   contrast and counted**, never back-filled or interpolated.
4. A missing optional arm — must **not** invalidate a valid V0/V0P contrast.
5. A duplicate `variant_id`, or a `campaign_id` reused from an existing manifest.
6. A manifest whose `protocol_commit` is absent or not a resolvable SHA.
7. Refusal to overwrite an existing pairing report (follow the rehearsal's refuse-before-write).

**Evidence to close:** the report on a synthetic three-arm campaign; the seven failures above
demonstrated; the existing intake regression suite unchanged and passing.

---

## T2 — Uncertainty computation

**Affected:** new `analysis/uncertainty.py`; `analysis/tests/test_uncertainty.py`.

**Input:** a component table — one row per component with measurement equation, value, distribution,
evaluation method (A/B), sensitivity coefficient (analytic **or numerical** per GUM 5.1.3 Note 2),
and correlation basis.
**Output:** `u_c` for each requested measurand, the coverage factor **with the basis for choosing
it**, `U`, and a **contribution table** showing each component's share.

**Contract — the two measurands behave differently and must be requested explicitly:**
- `absolute_bias(arm)` — the shared-reference component enters **in full**.
- `difference(arm_a, arm_b)` — for **simultaneous** readings of the **identical** reference, the
  shared term **cancels exactly**; location mismatch, per-probe calibration and timestamp mismatch
  do **not** cancel and must remain.

**Failure cases:**
1. Requesting `difference` while declaring the readings non-simultaneous or the references distinct
   — must refuse, not silently cancel.
2. A component with a declared correlation but no correlation basis — must refuse.
3. `k = 2` requested where the GUM G.6.6 conditions are not demonstrable from the inputs (dominant
   single Type B component, few effective degrees of freedom) — must **warn and report the basis**,
   never assert 95 % silently.
4. A regression pinning the sign convention: for a **sum**, positive correlation **increases** `u_c`;
   for a **difference**, it **decreases** it. *(This is the error the pilot spec originally made.)*
5. Zero or negative declared uncertainty on a component.

**Evidence to close:** GUM §5.2.2's own worked resistor example reproduced (1 Ω correlated vs 0.32 Ω
uncorrelated) as a **sum** fixture, plus a difference fixture showing the opposite direction.

---

## T3 — Auxiliary channel ingestion (T/RH, power, extra nodes)

**Affected:** new `analysis/aux_channels.py`; `analysis/tests/test_aux_channels.py`.
**Must not touch:** the intake schema — auxiliary data lives in a **separate instrument file** keyed
to the same timestamps, so `FIELDS` is not widened.

**Input:** an instrument CSV carrying any of: reference RH, sensor RH, their temperatures, measured
voltage and current, and node temperatures from the §1 map of the experiment contract.
**Output:** a validated, timestamp-aligned frame; derived **power `W = V·I`**; derived **vapour
pressure** `e = (RH/100)·e_sat(T)` for both reference and sensor; and a per-interval **state label**
joined from the power/airflow registers.

**Failure cases:**
1. RH present without its own co-located temperature — must refuse (RH is meaningless alone, and
   vapour pressure is uncomputable).
2. **Rated** power supplied instead of measured V and I — must refuse; the field is `measured_v` and
   `measured_i`, and there is no `rated_w` input.
3. An interval whose fan state is `unknown` — must be flagged **ineligible for the I1 contrast**,
   and retained rather than dropped.
4. Timestamps not on the declared grid, or outside the intended window.
5. RH outside 0–100 %, or a physically impossible dewpoint (`e > e_sat(T)`).
6. Silent unit coercion — units are declared per column and mismatches refuse.

**Evidence to close:** synthetic fixtures for all six; a vapour-pressure round-trip check; and a
demonstration that an `unknown` fan-state interval is excluded from I1 **but still counted** in
coverage.

---

## T4 — Predictor/target-leakage guard

**Affected:** new `analysis/prediction_contract.py`; tests.

Enforces §9.6 of the Study B design: a **before-build** prediction may consume only quantities
available before the target enclosure is built and measured.

**Input:** a declared predictor set, each tagged `design` / `independently_characterised` /
`environmental` / `target_derived`.
**Output:** admissible or refused, naming the offending predictors.

**Failure cases:** a `target_derived` predictor (solved `Re_vent`, measured vent velocity, or any
held-out response) in a contest-A prediction must **refuse**; the same predictor is admissible in
contest B **only** if declared inside the calibration allocation.

**Evidence to close:** a contest-A fixture refusing a solved-`Re_vent` predictor, and a contest-B
fixture accepting it with the allocation declared.

---

## Sequencing

T1 and T3 are prerequisites for handling any real campaign. T2 is needed before any bias is
reported with an interval. T4 is needed before the first transfer claim. **None is on the critical
path until the owner authorises a pilot** — they are specified now so the authorisation decision is
not delayed by unwritten software.
