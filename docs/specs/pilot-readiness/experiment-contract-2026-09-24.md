# Experiment contract — interventions, nodes, contrasts and stopping rules (WP2, 2026-09-24)

**Status: specification for owner/PI decision. No experiment is authorised or performed. No
hardware, dimension, calibration record, permission or measurement is invented.** Base: `main`
`6d63e98`. Companion to [`pilot-design-2026-09-24.md`](pilot-design-2026-09-24.md) (variants, data
contract, uncertainty budget); this document adds what that one could not: **which claims are
earned by intervention and which remain association.**

**Governing rule.** Every mechanism claim is either (a) supported by a **controlled intervention**
with a named estimand, or (b) explicitly labelled **association**. There is no third category, and
an uncontrolled day/night comparison is never promoted to identification.

---

## 1. Node map — name the temperatures before comparing coefficients

The lumped model has one sensor node. The physical enclosure has at least six distinguishable
temperatures. Treating them as one is an assumption to be **tested at commissioning**, not assumed.

| Node | Symbol | Measured how | If unmeasured |
|---|---|---|---|
| Ambient air (true) | `T_air` | independently characterised reference at matched height | campaign is void — this is the measurand's reference |
| Sensor element | `T_s` | the enclosure's own sensor (the quantity of interest) | — |
| Internal air | `T_int` | independent probe in the sensing zone, own logger | single-node adequacy untested; state it |
| Inner wall | `T_w,i` | surface probe at a declared location | wall gradient unresolved; `Bi` screening only |
| Outer wall | `T_w,o` | surface probe, same station | ditto |
| Electronics / heat source | `T_e` | surface probe at the dissipating component | heat path unidentified |
| Mounting path | `T_m` | probe at the mast/bracket interface | conduction leak unquantified |

**Commissioning test (before the campaign):** log all available nodes for ≥1 full diurnal cycle and
report the spread. `shlipak2025` found internal air, wall and battery within **0.25 °C** even at
peak solar in *one ABS enclosure*; that does **not** establish isothermality for this geometry or
this sensor. If the measured spread here exceeds the pilot's `u_c` target (0.25 °C), the single-node
treatment is **not adequate** and the model comparison must say so.

**Area mapping must be written before any coefficient is compared.** `A_conv` for V0 and for V1 are
*different coupled systems*, not the same parameter measured twice. `A_conv` is an **effective
coupled** area, not total CAD surface; `A_proj` is a projection at a stated solar geometry.

---

## 2. Intervention matrix

Estimands are the quantity the experiment identifies. "Association" means the design cannot
separate the named confounder.

| # | Mechanism | Intervention | Held fixed | Likely confounders | Required measurements | Estimand |
|---|---|---|---|---|---|---|
| **I1** | **Internal dissipation** | ≥2 documented electronics load states, or a controlled resistive load at the same heat-source location | airflow state, enclosure, probe position, mounting, exposure | fan state coupled to power; self-heating of the added load's wiring; ambient drift between blocks | measured **V and I** (not rated W), all nodes §1, ambient, solar, wind, sky/long-wave | **°C per W** at the sensor node |
| **I2** | **Solar loading** | controlled radiative exposure (shade/unshade, or lamp on/off indoors) at fixed power state | power state, airflow, position | shading also changes long-wave view factor; wind gusts | irradiance on the projected plane, sky condition, all nodes | **°C per (W/m²)**, conditional on orientation |
| **I3** | **Ventilation / airflow** | change one vent parameter (total open area at fixed inlet/outlet positions), CAD-inspected | material, finish, source location, power state | vent change also alters radiation ingress and view factor | vent open area (inspected), airflow proxy or ΔP, all nodes | **°C per unit open-area ratio**, conditional |
| **I4** | **Surface finish** | V0 vs V0P — matched hardware, documented finish change only | geometry, sensor placement, exposure, power | **real paint changes `eps` as well as `alpha`** — an alpha-only change is a *model* intervention, not an experimental one | measured `alpha` **and** `eps` per finish, with the standard named | **°C per Δ(alpha, eps)** jointly — not `alpha` alone |
| **I5** | **Whole-design comparison** | V0P vs V1 | exposure, reference, window | geometry, ventilation, sensor position and heat coupling **all differ simultaneously** | as above | **association only** — a practical design ranking, **not** an isolated vent or material effect |
| **I6** | **Aspiration benchmark** *(optional, owner)* | fresh air drawn across an isolated probe (`deford2025` arrangement), **not** internal recirculation | enclosure, power accounting | fan adds heat and power; failure modes | fan power, inlet/outlet arrangement, airflow or failure indicator, **fan-off data** | **°C reduction vs passive**, at a stated power cost |

**I1 is the first experiment.** It is the only design here that identifies the dissipation term,
and the literature contains no measured value for a low-cost AQ enclosure.

### I1 protocol (the one the project's novelty rests on)

1. Temperature probes **independently powered and independently logged**, fixed in place, so the
   measurement chain does not change with the load state.
2. **At least two documented load states.** A controlled resistive load at the same heat-source
   location is preferred for a purely thermal test, because it decouples heat from firmware
   behaviour.
3. Log **actual voltage and current** with synchronised timestamps. **Rated watts are not data.**
4. **Hold airflow fixed.** Powering down a PM unit typically also stops its fan — that changes heat
   *and* ventilation and identifies neither. If the fan cannot be decoupled, the test estimates a
   **combined** heat+airflow effect and must be labelled as such.
5. **Randomise or counterbalance load order; repeat in blocks.** Record every transition; never
   silently drop an inconvenient interval.
6. **Settling rule:** derive it from a step-response test, not by assumption. Propose **≥5 estimated
   dominant time constants** as the first-order rule, then check it against the observed dynamics
   and revise prospectively if the response is not first-order.
7. **Begin under controlled radiative exposure**, then repeat under registered outdoor conditions.
   Log sky/long-wave information: **`G = 0` is not zero net radiation.**
8. Separate **measured electrical input**, **total enclosure heat release**, and **heat reaching the
   sensor zone**. The third requires a heat-path model or identification — a power meter cannot give
   it directly.

**Why this and not a night/day contrast:** at night, outward long-wave loss can exactly offset
electronics heating. Verified in this repo's own model — `Q = 0.102972 W` returns a night bias of
`-1.2e-8 °C`. **Near-zero night bias does not imply near-zero dissipation.** Night/day observations
constrain the *combined heat balance*; they do not attribute cause.

---

## 3. State registers (recorded per interval, not per campaign)

**Power state register:** `state_id`, nominal description, measured V, measured I, derived W,
fan state (`on`/`off`/`absent`/`unknown`), firmware mode, start/end UTC.

**Airflow state register:** `state_id`, vent configuration ID, measured open area, any forced-flow
device and its state, airflow proxy if available, start/end UTC.

A row whose fan state is `unknown` **disqualifies that interval from I1**, because heat and
ventilation cannot then be separated. Record it; do not delete it.

---

## 4. T/RH auxiliary channels — required before any RH claim

**A temperature-only campaign cannot validate an RH claim.** If RH is an endpoint:

| Channel | Requirement |
|---|---|
| Reference RH | independently characterised, with calibration record and stated uncertainty |
| Reference temperature | co-located with reference RH (RH is meaningless without its temperature) |
| Sensor RH | the enclosure sensor's own RH |
| Sensor temperature | already required |

Report RH differences in **percentage points**, and additionally compare **vapour pressure**
`e = (RH/100)·e_sat(T)`. *Testable hypothesis:* if the enclosure only warms the air, vapour pressure
is conserved and the RH drop follows from `e_sat(T)`. Wetting, condensation, air exchange and sensor
response can violate it — which is what makes it a test rather than an assumption.

**Wet/dry handling is registered in advance.** Do not remove wet intervals only after they produce
inconvenient errors.

**Scope reduction if unavailable:** if no RH reference exists, **narrow this campaign to
temperature** and state that the RH endpoint is deferred. Do not infer RH performance from
temperature performance.

**PM/gas endpoint is a later campaign.** Cleaner ambient T/RH is **not** proof of improved pollutant
accuracy, especially where the existing correction was fitted to *onboard* variables. Substituting a
corrected ambient RH into a fitted PM equation **requires retesting against pollutant references**.

---

## 5. Calibration plan

- **Pre- and post-campaign bracketing checks** for every sensor and the reference, against the same
  standard, with dates recorded. Drift between brackets is an uncertainty component (R3.1 #6), not a
  correction to be silently applied.
- **Independent property characterisation** before the campaign: `alpha` and `eps` per finish (with
  the measurement standard named), wall thickness and conductivity per printed variant, vent open
  area by CAD inspection.
- A drawing **cannot** close a `measurement`-route parameter. Changing an acquisition route requires
  a prospective, written amendment.

---

## 6. Contrast definitions — what each comparison can and cannot answer

| Contrast | Answers | Does **not** answer |
|---|---|---|
| V0 vs V0P | effect of the documented finish change on matched hardware, under matched exposure | `alpha` alone (paint moves `eps` too); any vent or material effect |
| V0P vs V1 | practical ranking of two complete designs | which of geometry / ventilation / sensor position / heat coupling caused it |
| I1 load states within one unit | **°C per W** for that unit and configuration | transfer of that coefficient to another geometry |
| I3 vent variants at fixed everything else | vent open-area effect for that material and source location | the same effect at a different power state, unless crossed (§7) |
| Any arm vs reference | absolute bias, carrying reference uncertainty in full | — |
| Difference between arms, simultaneous, same reference | relative bias with the shared-reference term cancelling exactly | location mismatch, per-probe calibration, timestamp mismatch — these do **not** cancel |

**Each contrast has its own valid-timestamp set.** Reserve all-arm complete cases for genuinely
joint comparisons; missing data on an optional arm must **not** discard a valid V0/V0P pair. Report
contrast-specific **and** all-arm coverage separately, and test whether missingness depends on
temperature or power state.

---

## 7. Replication and design of the follow-on

- **Cross the design contrast with power state.** More venting may change power sensitivity as well
  as solar bias; plan the interaction **before** fitting, or it cannot be estimated.
- **Independently printed units**, calibrated probes where available, **positions rotated in
  balanced blocks**; track enclosure, probe and position identifiers separately.
- **Replication count comes from the minimum useful effect and the pilot variance**, computed after
  commissioning. Do not pretend a handful of units establishes power; if the pilot cannot support
  the count, **reduce the claim**, not the standard.
- **Transfer requires a genuinely withheld geometry family.** A finish replicate is not an unseen
  geometry.

---

## 8. Stopping and extension rule (registered before observation)

1. **24 hours is a commissioning minimum**, not a sufficient campaign (existing protocol thresholds
   apply per arm and are not redefined here).
2. **Extend on missing exposure coverage**, never on whether a favoured design is winning. The
   registered exposure targets — illuminated and low-solar paired counts — are the only admissible
   trigger.
3. **Declare a maximum extension window before observing comparative results.**
4. If coverage remains incomplete at the window's end, **retain the result as incomplete** and record
   the stop decision. Do not relax a threshold after seeing outcomes.
5. One 24-hour campaign cannot establish seasonal or general accuracy, whatever it shows.

---

## 9. Claim ledger for this contract

| Claim | Earned by | Status |
|---|---|---|
| Enclosure bias exists and has this magnitude | absolute comparison vs reference | **association** until data exist |
| Finish changes bias | I4 (matched hardware) | intervention — but joint `(alpha, eps)` |
| Dissipation changes bias | **I1** | intervention — **°C/W** |
| Ventilation changes bias | I3 | intervention — conditional on material/source |
| Design V1 beats V0P | I5 | **association** — whole-system ranking only |
| Solar drives the bias | I2 | intervention |
| "Self-heating dominates" / "solar dominates" | — | **not claimable** without I1 and I2 together |
| Better T/RH improves PM/gas | — | **not claimable** — separate campaign with pollutant references |
