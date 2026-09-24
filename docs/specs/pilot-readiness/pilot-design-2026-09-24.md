# First physical experiment — design, data contract and uncertainty budget (R1–R3, 2026-09-24)

**Status: specification for owner/PI decision. No experiment is authorised, scheduled or performed
by this document. No hardware, dimension, calibration record, permission or measurement is invented
here — every unresolved value is a named placeholder with an acquisition route.** Base: `main`
`5b5ec24`. Authority: [`COLOCATION_PROTOCOL.md`](../../COLOCATION_PROTOCOL.md) (draft protocol; the
data-readiness thresholds below are **quoted from it, not redefined**),
[`research-direction-2026-09-21.md`](../../research-direction-2026-09-21.md) §9 (gap → observable),
[`REVIEW_2026-09-22.md`](../../../literature/REVIEW_2026-09-22.md) (measured magnitudes and method),
and `jcgm2008gum` for the uncertainty treatment. Decisions requiring the owner are in
[`OWNER_DECISIONS_2026-09-24.md`](../../OWNER_DECISIONS_2026-09-24.md).

---

## R1 — Three-variant pilot design

### R1.1 What this experiment must discriminate

The literature review established two things that change the design:

1. **No published source measures the internal power dissipated in a low-cost air-quality
   enclosure**, and the two origin papers assert *different* mechanisms — `holder2020`
   ("likely … heated from the sensor electronics") versus `malings2020` (the shell "can trap heat").
   Measuring the watts is therefore the pilot's genuine contribution, not a side observation.
2. **The only evidence-based cause separation in that literature points at solar, not electronics:**
   `shlipak2025` measured internal temperature converging to ambient at night, and `holder2020`'s
   only attribution test implicated sun. A continuous electronics-driven offset would **not** vanish
   at night.

So the experiment is designed around a **discriminator**, not just a comparison:

> **D1 (night/day contrast):** self-heating produces a bias floor that persists through the dark
> hours; solar loading does not. The campaign must therefore span a full diurnal cycle *and* record
> internal power continuously, so the two mechanisms can be separated rather than assumed.
>
> **D2 (powered/unpowered contrast, if the owner permits a fourth arm):** the same enclosure logged
> with its electronics powered versus externally logged and internally unpowered isolates the
> dissipation term directly. This is the single most decisive measurement available and is not in
> the literature. Recorded here as a **proposed option**, not a scheduled arm.

`shlipak2025` also found internal air, wall and battery temperatures agree within **0.25 °C even at
peak solar loading**, which (a) supports the lumped treatment and (b) means a single well-placed
internal probe is defensible — a finding that reduces, not increases, the instrumentation burden.
It also found internal fans largely ineffective and potentially net-heating; **no fan arm is
proposed.**

### R1.2 Variants

| Arm | Description | Differs from V0 by | Status |
|---|---|---|---|
| **V0** | Dark/closed baseline enclosure | — | geometry unresolved |
| **V0P** | **Identical geometry and identical sensor placement**, documented finish change only | surface finish (`alpha`) | geometry unresolved |
| **V1** | Passive vented shield | geometry + venting | geometry unresolved |
| *(V0-U, optional)* | *V0 hardware, electronics unpowered, external logging* | internal dissipation only | **owner decision (D2)** |
| **REF** | Independently characterised reference instrument at matched height and exposure | — | instrument unresolved |

V0P exists so that a shield advantage is never read against an unmatched control — the repo's own
matched-control screen showed the nominal advantage reverses under combined assumptions.

**Simultaneity.** Simultaneous measurement is required by default. If only one enclosure can be
instrumented at a time, the owner must approve a **paired-successive** design in advance, and every
resulting comparison must be labelled with its weather/time confounding. This is an owner decision,
not an agent substitution.

**Zone separation.** Separate the electronics/heat source from the ambient sensing zone where the
hardware permits; where it does not, the heat path must be **recorded and measured**, not assumed.

### R1.3 Pre-acquisition register (all fields required *before* data collection)

Every value carries units, an evidence state and an acquisition route
(`measurement` / `vendor_drawing` / `design_then_inspect`), matching the CAD contract in
[`study-b-cht/design.md`](../study-b-cht/design.md) §5. **A drawing cannot close a `measurement`
field.**

| Group | Fields | Route |
|---|---|---|
| Identity | hardware ID, sensor ID, firmware version, enclosure revision | `measurement` |
| Material & optics | material, finish, **solar absorptance `alpha` and emissivity `eps`, measured or bounded with the standard named** (per `levinson2010`: E903 / C1549 / E1918) | `measurement` — **no measured `alpha` for a printed wall exists in the literature; colour name is not evidence** |
| Geometry | wall thickness (mm), vent count and dimensions, open area, sensor stand-off, electronics location, plate gaps | `measurement` |
| Power | **electrical input power (W) and the point at which it is measured**, plus the fraction reaching the sensor zone | `measurement` — the novel quantity |
| Reference | instrument ID, calibration certificate, stated uncertainty, aspiration/shield description | `vendor_drawing` + `measurement` |
| Siting | mounting height, orientation, exposure, shade, ground/background, **site and data permission** | owner |
| Schedule | intended UTC start/end, cadence | owner |
| Environment | cloud/sky, solar irradiance, wind, wetness, interventions, maintenance events | `measurement` |

**Expected magnitudes for sanity-checking only (not acceptance criteria):** measured enclosure
biases in the literature run `+1.88 °C` mean / `+6.48 °C` daily max (`shlipak2025`, PurpleAir PVC),
`+2.6 °C` (`couzo2024`), `+5.23 °C` (`holder2020`). A pilot result far outside that band is a
reason to check instrumentation before it is a finding.

---

## R2 — Data schema and custody

### R2.1 Chosen mapping — one CSV per variant plus a campaign manifest

The existing intake (`analysis/colocation_intake.py`) validates **one sensor/reference pair per
CSV**, with `FIELDS = {timestamp, sensor_temperature, reference_temperature, solar_w_m2, wind_m_s}`.
Two options were available; **option (a) is adopted and option (b) is rejected**, and they must
never be mixed:

- **(a) ADOPTED — one CSV per variant, identical UTC timestamps, plus a campaign manifest mapping
  the files.** The fail-closed intake keeps working per file *unchanged*, and cross-variant pairing
  lives in the manifest.
- **(b) Rejected — one wide CSV** with one reference and per-variant columns. It would require
  changing the validated intake schema, discarding the existing regression coverage for no
  functional gain.

**Critical limit, stated in the protocol and restated here:** successful intake of each file
individually does **not** prove cross-variant pairing or authenticate the campaign. The manifest is
what carries that claim, and the manifest is **not yet implemented** — see R2.4.

### R2.2 Campaign manifest — required content

| Field | Rule |
|---|---|
| `campaign_id` | unique; never reused |
| `variant_id` → `csv_path`, `metadata_path` | one row per arm (V0, V0P, V1, optional V0-U) |
| `sensor_id`, `reference_id` | the **same** `reference_id` across arms is the expected case and **creates statistical correlation** — see R3.3 |
| `protocol_commit` | git SHA of the protocol version frozen before acquisition |
| `csv_sha256`, `metadata_sha256` | **raw-byte hash of every file**, recorded at acquisition |
| `calibration_record_ref`, `uncertainty_record_ref` | per instrument |
| `intended_window_start_utc`, `intended_window_end_utc` (exclusive), `cadence_s` | declared, not inferred |
| `event_log_path` | interventions and maintenance |
| `custody`, `authorized_storage`, `retention` | where raw bytes live; **never private raw data in git** |

### R2.3 Schema rules (no silent repair)

- **Timestamps:** ISO-8601 UTC, exactly on the declared grid; exclusive end. **No interpolation, no
  implicit rounding** into a passing intake.
- **Missing values:** empty field means missing; missing is never zero and never imputed.
- **Cross-variant slot matching:** a slot counts as paired **only** if every declared arm has a
  finite value at that identical timestamp. A slot missing in one arm is **dropped from
  cross-variant comparison and counted**, never back-filled from a neighbour.
- **Per-arm vs cross-variant coverage are reported separately.** The protocol's data-readiness
  criteria (≥90 % paired finite over the intended 24 h / 1,440 slots; ≥120 slots at solar ≥200 W/m²;
  ≥120 at ≤5 W/m²; declared `U95 ≤ 0.5 °C`) apply **per arm**; cross-variant coverage will be lower
  and must be stated as its own number.
- **No post-hoc threshold relaxation.** If coverage falls short, the result is retained as
  incomplete and the prospective extension or stop decision is recorded.
- Extra environmental channels (internal temperature, **input power**) are recorded in a **separate
  instrument file** keyed to the same timestamps, so the validated intake schema is not widened.

### R2.4 Implementation is a separate, owner-approved task

This is a **specification**. The manifest validator, the cross-variant pairing check and their
regression tests are **not implemented here** and require an approved implementation PR. Any such
change must **preserve the existing single-pair intake behaviour** and add a compatibility test.

---

## R3 — Uncertainty budget and decision worksheet

### R3.1 Components, listed separately

Per `jcgm2008gum`, each is a standard uncertainty `u(x_i)` with a sensitivity coefficient
`c_i = ∂f/∂x_i`; where the model is not analytically differentiable, use the Guide's **numerical**
form (5.1.3 Note 2). Units are °C unless stated.

| # | Component | Type | Notes |
|---|---|---|---|
| 1 | Sensor calibration | A/B | per unit, from its certificate |
| 2 | Reference calibration | B | from certificate |
| 3 | **Reference radiation/aspiration error** | B | the reference is not truth; `nakamura2005` shows a corrected passive shield's residual is reference-limited |
| 4 | Sensor-to-reference location mismatch | B | height and exposure difference |
| 5 | Clock alignment | B | maps to a temperature error through the local time gradient |
| 6 | Drift between pre/post checks | B | bracketing checks required |
| 7 | Solar and wind measurement uncertainty | B | enters the as-built prediction, not the bias itself |
| 8 | Model-input uncertainty (as-built prediction) | B | **`h_c` dominates** — `berdahlbretz1997` states 10 % accuracy in `(h_r + h_c)` "is not feasible"; see R3.4 |
| 9 | **Covariance: one reference serving all arms** | — | **see R3.3 — this is the component most likely to be got wrong** |

### R3.2 What `U95 ≤ 0.5 °C` actually requires

`U = k · u_c` (GUM Eq. 18). The protocol's `U95 ≤ 0.5 °C` therefore means **`u_c ≤ 0.25 °C` at
`k = 2`** — and `k = 2` corresponds to ~95 % **only** under the four GUM G.6.6 conditions:
well-behaved input distributions, **comparable** contributions from the components, an adequate
first-order approximation, and effective degrees of freedom above about 10. Those conditions must be
**demonstrated, not assumed**. If one Type B component dominates with few degrees of freedom,
`k = 2` does not deliver 95 %.

### R3.3 The shared-reference correlation — the anti-conservative trap

GUM §5.2.2's worked example **is this pilot's design**: ten resistors each calibrated against *the
same* standard. Because the correlation coefficient is `r = +1`, the uncertainties add **linearly**,
not in quadrature — `1 Ω` rather than `0.32 Ω`, and the Guide states flatly that the quadrature
answer "is incorrect". **Ignoring a shared reference understates the uncertainty by roughly 3× in
the Guide's own example, i.e. it errs anti-conservatively.**

Here, **one reference instrument serving V0, V0P and V1 correlates every cross-variant comparison.**
Two consequences:

- For a **difference between arms** (e.g. `bias_V0P − bias_V1`), the shared-reference term partly
  **cancels** — which is why a matched-control comparison is more precise than either absolute bias.
  That cancellation must be *derived*, not assumed, via GUM Eq. 13/16 with `r` stated.
- For an **absolute bias per arm**, the reference uncertainty enters in full and does **not** cancel.

**Adopted treatment (GUM §5.2.4):** re-parameterise so the shared reference enters **once, as an
explicit independent input**, rather than estimating pairwise covariances. The Guide gives a
thermometer as its own example of this case.

### R3.4 Model-input uncertainty for the as-built prediction

Feeding the T3 observables into the model carries the literature's own warnings:

- **`h_c` dominates** and cannot be pinned to 10 % (`berdahlbretz1997`). Carry it as a band.
- `h = 5.0 + 4.0·U` is **currently mis-referenced** (see the review §1): it is Jürges' correlation
  with intercept 5.6, valid `U ≤ 5 m/s`, on **free-stream** wind — and against weather-station `U10`
  the measured slopes are 0.90–2.9. **Which wind the pilot records must be declared**, because it
  changes which coefficient is even applicable.
- `T_sky = T_air − 20 K` is unsupported; record **dewpoint** so the sky term can be computed rather
  than assumed.
- `alpha` error converts to temperature at **0.6 K per 10 W/m²** of solar heat gain (`levinson2010`).

### R3.5 Two thresholds that must never be conflated

| | Data-readiness | Scientific comparison tolerance |
|---|---|---|
| Status | **Defined** — quoted from the protocol: ≥90 % paired finite over 1,440 intended slots; ≥120 slots ≥200 W/m²; ≥120 slots ≤5 W/m²; declared `U95 ≤ 0.5 °C` | **TBD — owner/application must supply** |
| Means | the dataset is *admissible for review* | a difference is *scientifically meaningful* |
| Set by | instrumentation and coverage | the application tolerance **plus** registered as-built model uncertainty |

**Prohibited:** using the simulated **1.4771 °C** nominal advantage — or any other model output — as
an acceptance threshold. It is a simulation result, not a tolerance. Both thresholds must be frozen
**before** comparative outcomes are inspected.

### R3.6 Analysis limits fixed in advance

- 1,440 minute samples are **temporally correlated**; do not report i.i.d. confidence intervals over
  them (protocol §; and `arlot2010` on the i.i.d. assumption).
- Report **signed bias and absolute error separately**. A cooler sensor is not a more accurate one.
- Stratify by the **registered** exposure regime, declared before comparative observation.
- One 24-hour campaign cannot establish seasonal or general accuracy.
