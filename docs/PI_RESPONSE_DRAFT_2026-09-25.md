# PI response — draft for owner review (2026-09-25)

**NOT SENT.** Prepared for the owner to check, edit and send. **The PI's exact wording was not
supplied to this session**, so the three answers below address the topics as recorded, not
quotations — **verify the correspondence before sending.** Every number is a **model output**, not a
measurement. Repo inspected at `444705f`; all figures below were recomputed against the committed
solver on 2026-09-25.

---

## 1. Can the parameters be listed finitely in advance, and how far does the reduction go?

The assumptions ledger has **23 entries, but these are not 23 independent physical variables** — it
mixes operating conditions, per-variant settings, empirical closures and sweep ranges. So I would
**not** claim Buckingham's theorem takes 23 independent parameters to five; that would conflate a
bookkeeping count with the independent variables of one governing relation.

For the stated steady-state single-node model, linearising the long-wave term gives a dimensionless
bias described by **five input groups**: absorbed solar relative to convection; internal heat
relative to solar; radiation relative to convection; sky-view fraction; and normalised air pre-heat.
That is a useful organisation of the *assumed* balance — not elimination of the measurements needed
to fix those inputs, and **not a claim that the group set is unique** (Buckingham notes explicitly
that several equivalent sets exist).

Two caveats I would state up front:
- For the **exact nonlinear** radiation balance, the **sky-depression-to-absolute-ambient ratio**
  must also be specified. It happens to be fixed in the original sweep, which is why five sufficed.
- At **zero solar**, the heat-to-solar ratio is singular; an absolute normalised internal-heat term
  replaces it, and a separate normalisation handles sky ≈ ambient.

**Correction I should flag:** an earlier internal write-up reported that the collapse "failed" and a
kill criterion was "tripped". That was wrong and is withdrawn. The exact nonlinear reformulation
reproduces the original solver to numerical tolerance (max residual ~5.5e-9 across 1,944 cases).
What the earlier residual actually diagnosed was the **linear approximation**, not dimensional
analysis, and certainly not anything about real hardware.

## 2. Can the variables that carry the biggest weight be identified before building?

**Partly — and the honest answer is more useful than a clean one.**

At the reference daytime point (1000 W/m², 0.5 m/s), the painted box is predicted at **+4.48 °C**
and the passive shield at **+3.00 °C**: an absolute-error advantage of **≈1.48 °C** to the shield.

Changing the three uncertain assumptions **one at a time** leaves the shield ahead, but by very
different margins:

| Change (one at a time) | Shield bias | Advantage retained |
|---|---|---|
| shading factor 0.18 → 0.30 | +4.38 °C | **+0.10 °C** |
| convection enhancement 1.4 → 1.0 | +3.45 °C | +1.03 °C |
| calm air pre-heat 1.2 → 2.4 K | +3.93 °C | +0.55 °C |
| **all three together** | **+6.03 °C** | **−1.55 °C — reversed** |

So the *ranking* of single effects is identifiable in advance, but **the conclusion is not robust to
combinations**: the shield's advantage disappears and reverses. These are **selected illustrative
scenarios**, not measured bounds, confidence intervals, or a probability of superiority. Their value
is that they name the measurement priorities: **shading, airflow coupling, and plate-to-air heat
transfer.**

## 3. How can a predictive model be validated without deployment?

**It cannot be — not fully — and I would not claim otherwise.** The current model plus an
uncontrolled day/night comparison **cannot uniquely attribute** the observed bias. Concretely,
night-time radiative cooling can offset electronics heating, so near-zero night bias does **not**
establish zero self-heating. (In our own model a heat input of ~0.10 W returns a night bias of
~1e-8 °C — nonzero cause, zero apparent effect.)

What *can* be done without deployment is bounded: internal consistency of the reduction, and
cross-model comparison. Neither touches physical accuracy.

**The smallest informative experiment** is one enclosure with an independently logged probe and a
characterised reference, at **two or more measured load states**, holding airflow, probe location
and radiative exposure fixed; load blocks repeated and counterbalanced; a step response measured to
set settling time; power and environment logged throughout. That estimates a **temperature response
per watt** for that configuration. If changing power also changes the fan, the result is a
**combined** intervention unless the two are separated. A controlled heater is an alternative, with
an explicit statement of how well its heat path represents distributed electronics heat.

A simultaneous matched-finish comparison then establishes practical performance under observed
conditions. **Transfer to an untested geometry is a separate study** requiring a withheld design and
frozen predictor provenance.

**Proposed immediate scope:** the bounded engineering study, with **temperature as the minimum
endpoint**. RH becomes an endpoint only once an appropriate reference and uncertainty route exist.
Broader transfer stays a follow-on — and the contribution must be more specific than "a forward
thermal model", because Air-STORM already models enclosure temperature from materials, weather and
internal heat.

**Outstanding inputs before the protocol can be frozen:** intended use and accuracy requirement;
hardware and reference inventory; calibration evidence; and permission for the specific load
intervention and site. **No physical validation is claimed.**

---

*Pointers (trim before sending):* `analysis/nondimensional.py`,
`analysis/matched_control_sensitivity.py`, [studyA_nondimensional.md](studyA_nondimensional.md);
Buckingham (1914) https://doi.org/10.1103/PhysRev.4.345; Air-STORM (2025)
https://doi.org/10.3390/s25154798
