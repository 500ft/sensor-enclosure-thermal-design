# Popoola et al. (2016): Baseline-Temperature Correction for Electrochemical Sensors

**Source:** https://doi.org/10.1016/j.atmosenv.2016.10.024  
**Evidence boundary:** Full text read 2026-09-22 via the Imperial Spiral open-access deposit of the CC-BY publisher PDF. Archival journal. **Field-scale counterpart to `samad2020`'s chamber study.**

## Sensors

Alphasense electrochemical NO, CO and NO2 nodes; reference chemiluminescence analyser. Cambridge, UK, Feb-Dec 2010, ambient 0.0-36.0 degC.

### Pros

- Ten months of ambient field data across a 36 degC temperature span, not a chamber.
- Separates **baseline** from **gain** effects explicitly.

### Cons

- The paper reports no per-degC coefficient in the text, and no internal power.
- Species-dependent: NO correlates strongly (R^2 ~0.9) while CO and NO2 give R^2 < 0.2, so the method does not transfer evenly.

## Physical Box, Materials, and Geometry

Not the subject; temperature is ambient, not enclosure-generated.

### Pros

- **Headline magnitude:** uncorrected NO against chemiluminescence gives `NO(EC1) = 1.40*NO(CHL) + 251.31 ppb` with **R^2 = 0.02**; after baseline-temperature correction the intercept falls to **-0.94 ppb with R^2 = 0.78** (residual RMSE < 2 ppb NO, < 10 ppb CO). That is a temperature-driven baseline error of order **250 ppb** on NO.
- Shows the temperature effect acts on the **baseline, not the gain** (gain-vs-temperature gradient 4.5e-3 +/- 5.2e-3 per K, p = 0.41) — a structural finding that tells this project *which* parameter an enclosure temperature bias corrupts.

### Cons

- Field study, so temperature covaries with other drivers; not a controlled isolation of the mechanism.
- Does not address enclosures, internal dissipation, or PM.

## Selection Lessons for This Project

- Cite for: the field-scale magnitude of temperature-driven electrochemical baseline error (~250 ppb NO intercept, R^2 0.02 -> 0.78 after correction) and the **baseline-versus-gain distinction**.
- Do **not** cite it for a per-degC coefficient (it publishes none), for enclosure effects, or for species other than those measured.
