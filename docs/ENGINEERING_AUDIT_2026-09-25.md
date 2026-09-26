# Engineering audit — provenance and evidence chain (2026-09-25)

**Method.** Repository inspected at `main` `6d63e98`: `thermal_bias.ASSUMPTIONS`, the protocol and
pilot thresholds, Study A/B documents, the literature review's model-input table, the owner packet
and the task ledgers. Values were read from the files, not from prior summaries. **No measurement,
property, coefficient or citation was invented; nothing was reclassified upward.**

**Scope note.** This is a *documentation and provenance* audit. It changes no model value, no
threshold and no acceptance criterion. Where a number is unsupported, it is **marked**, not fixed —
fixing several of these moves every published figure and is an owner decision.

---

## F1 — Five overlapping provenance taxonomies, no canonical register *(priority: high)*

The repository already tracks provenance in **five different, unreconciled schemes**:

| # | Scheme | Vocabulary | Where |
|---|---|---|---|
| 1 | Assumption status | `bounded` (13) · `physics` (2) · `swept` (2) · `TODO-from-lab` (6) | `thermal_bias.ASSUMPTIONS` |
| 2 | Model-input provenance | `cited` (3) · `cited-but-revise` (7) · `still uncited` (6) · `lab` (3) | `literature/REVIEW_2026-09-22.md` §2 |
| 3 | Evidence class | `ANALYTICAL` · `SYNTHETIC` · `HISTORICAL-EXTERNAL` · `PHYSICAL-PILOT` | weekly plan / evidence packets |
| 4 | Acquisition route | `measurement` · `vendor_drawing` · `design_then_inspect` | `specs/study-b-cht/design.md` §5 |
| 5 | Claim status | `simulated` · `derived` · `blocked` | `research-direction-2026-09-21.md` §6 |

**Consequence.** A reader cannot answer "what kind of number is this, and how do I know?" from one
place, and the same quantity can be described differently in two documents without either being
wrong. **Action:** one canonical register (F2), cross-referenced rather than duplicated. The five
existing schemes are **retained where they serve a local purpose** — the register reconciles them,
it does not replace `ASSUMPTIONS`.

## F2 — No canonical parameter register existed *(priority: high, now addressed)*

`0.25` appears in **6** documents and `0.5 °C` in **7**, with no single definition either points to.
One instance was already a real defect: a `0.25 °C` *instrument uncertainty* target had been reused
as a *model-structure* threshold (corrected in PR #37). **Action:** `PARAMETER_REGISTER.csv`, with
stable IDs, one canonical definition per quantity, and cross-references from the local analyses.

## F3 — Provenance conflated with evidence status *(priority: high)*

The existing schemes mix *what kind of number it is* with *how well it is established*. These are
independent: a **selected design value** can be unverified, analytically assessed, or bench-measured.
**Action:** the register carries `provenance` and `evidence_status` as separate columns.

## F4 — Six model inputs remain uncited *(priority: high — this is the real engineering gap)*

Unsupported by any source located in the search record, yet all are consequential:
`f_sky_V0` (0.50), `f_sky_shield` (0.05), `shield_solar_factor` (0.18), `shield_conv_boost` (1.4),
`shield_air_preheat_calm` (1.2 K), `preheat_wind_halflife` (1.5 m/s), `h_fan_V2` (25 W/m²K).

**Consequence.** `shield_solar_factor` and `shield_conv_boost` are two of the three axes whose
*combination* reverses the shield's advantage (+1.4771 → −1.5531 °C). **The reversal is driven
largely by uncited numbers.** That does not make the reversal wrong — it makes it a **measurement
priority**, which is exactly how it is now recorded.

## F5 — Four inputs are cited-but-contradicted *(priority: high, recorded not applied)*

`T_sky_offset` 20 K, `h_free_floor` 5.0, `h_wind_slope` 4.0, `eps_surface` 0.90, `alpha_V0` 0.90 —
each has a source that **disagrees** (review §1). Left as `cited-but-revise`: changing them moves
every published number, so it is an owner decision, not an audit action.

## F6 — External measured results were at risk of reading as our inputs *(priority: medium)*

`+2.6 °C` (Couzo), `+5.23 °C` (Holder), `+1.88 / +6.48 °C` (Air-STORM), `1–5 W` are **measured
results for other systems** — legitimate sanity bounds, **not** measured inputs for this enclosure.
**Action:** register class `measured_result_external`, explicitly not usable as an input.

## F7 — Two thresholds are unresolved and must stay that way *(priority: medium)*

The **application tolerance** (owner packet #16) and the **node-equivalence tolerance** (experiment
contract §1) are both genuinely undetermined. **Action:** registered as `unresolved` with the
decision each blocks — never defaulted.

## F8 — No traceability index *(priority: medium, now addressed)*

Nothing connected a decision to its requirement, analysis, canonical inputs and validation status.
**Action:** `TRACEABILITY_INDEX.md`, links only — equations stay beside their decisions.

---

## What this audit deliberately did **not** do

- Did not change any model value, threshold or acceptance criterion.
- Did not upgrade any `unverified` status; **no calculation was reclassified as validation**.
- Did not invent a source for the six uncited inputs (F4) — they are marked, with a measurement task.
- Did not resolve F5; that is an owner decision with repository-wide numeric consequences.
