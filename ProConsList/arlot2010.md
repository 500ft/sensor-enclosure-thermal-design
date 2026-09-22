# Arlot and Celisse (2010): A Survey of Cross-Validation Procedures for Model Selection

**Source:** https://doi.org/10.1214/09-SS054  
**Evidence boundary:** Full text read 2026-09-22, **as the arXiv:0907.4728v1 preprint, not the typeset article** (the Project Euclid PDF endpoint served an HTML interstitial). Published identity verified on the Euclid landing page. **Do not use pinpoint page cites without checking the typeset PDF.** Archival open-access statistics survey.

## Sensors

Not applicable: statistics methodology.

### Pros

- Open access and archival, so the project's validation standard is checkable without a subscription.
- Explicitly links cross-validation and information criteria as two implementations of one unbiased-risk-estimation principle — the bridge this project needs between "held-out validation" and "penalise parameter count".

### Cons

- A survey: it deliberately declines to prescribe a procedure, concluding no optimal method can be named in general.
- **Does not write down a parameter-count penalty.** It names AIC and Mallows' C_p but gives no formula; a further source is required before the repo states one.

## Physical Box, Materials, and Geometry

Not applicable. Content used: the in-sample optimism premise; the hold-out estimator (Eq. 8) and CV as an average of hold-outs (Eq. 9); the bias identity `E[CV] = E[risk at n_t]`, so CV's bias is the risk difference between `n_t` and `n` training points; and the penalisation framing where the penalty is a measure of model complexity.

### Pros

- Supplies the formal reason an **in-sample** comparison between a pre-build prediction and a post-build fitted correction is inadmissible — exactly the K2 benchmark's failure mode.
- §10.1's three criteria (bias / variability / computational cost) are a usable protocol for choosing a split scheme; §10.2 gives the stratification rule, relevant if the DOE is stratified by regime.
- Records the estimation-vs-identification distinction and Yang's (2005) impossibility result — no procedure is simultaneously model-consistent and minimax-rate optimal.

### Cons

- **The i.i.d. assumption is a live problem here:** consecutive samples from one enclosure are autocorrelated, and the dependent-data case needs a different literature than this survey.
- CV is biased upward by construction, because it estimates risk at `n_t < n`.
- Penalties such as AIC or C_p "depend on some assumptions on the distribution of data" and on factors that are not always known (e.g. the noise level for C_p).

## Selection Lessons for This Project

- Cite for: the in-sample-optimism premise; the hold-out and CV estimators; the bias identity; the penalisation framing linking AIC/C_p/LOO/GCV; the estimation-vs-identification distinction; the three-criteria guidance; and the i.i.d. caveat.
- Do **not** cite for: the AIC or BIC formula, a parameter-count penalty value, or any claim that a specific split fraction is correct — nor as prescribing CV over an information criterion, which it explicitly declines to do.
