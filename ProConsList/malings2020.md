# Malings et al. (2020): Fine Particle Mass Monitoring with Low-Cost Sensors

**Source:** https://doi.org/10.1080/02786826.2019.1623863  
**Evidence boundary:** Full text read 2026-09-22 (publisher HTML full text via text extraction; direct PDF returned HTTP 403). **The online Supplement (Tables S2-S4) could not be accessed and nothing is cited from it.** Archival journal. **This is the second origin paper behind Barkjohn's quoted range — Malings supplies the 2.7 degC / 9.7 % end.**

## Sensors

PurpleAir PA-II (2x Plantower PMS5003) and Met One NPM, attached to RAMP monitors. PM reference: regulatory Beta Attenuation Monitors (federal equivalent methods), no stated uncertainty. **For the T/RH comparison the "outside" reference is not identified** — treat it as unstated.

### Pros

- Nine PurpleAir units at Lawrenceville (vs 2 in `holder2020`), 30 Mar - 4 Jun 2018.
- Candid QA note: of a batch of 30 PurpleAir units, 7 were found defective in lab testing and excluded.

### Cons

- **The bias number is a bare two-clause aside** with no n, no duration, no RMSE, no uncertainty, no named reference and no supporting figure — yet it is the most widely propagated number in this literature.
- Supplement unread, so the RH-resolved breakdown is unavailable.

## Physical Box, Materials, and Geometry

PurpleAir plastic shell enclosing the Plantower sensors and associated circuits.

### Pros

- **Measured offset, verbatim:** "RH inside the PurpleAir was found to be 9.7 percentage points lower on average than outside, while T was 2.7 degC higher."
- Advances a citable inversion: the internal drying may partly self-compensate hygroscopic overreading, so "the PurpleAir sensor may be less susceptible to humidity-driven changes" — the enclosure bias is not purely a degradation.
- The kappa-Koehler hygroscopic-growth correction decreased MAE by about 40 % for both sensor types.

### Cons

- **Cause is asserted and doubly hedged, and it is a DIFFERENT mechanism from Holder's:** "the plastic shell ... **can trap heat** inside the unit". Heat trapping by the shell is not electronics dissipation. Barkjohn 2021 merges the two attributions; this project must not repeat that merge.
- No wattage, no solar/electronics separation, no experiment on the mechanism.
- No PM-error-per-%RH coefficient is given.

## Selection Lessons for This Project

- Cite for: the +2.7 degC / -9.7 pp internal-vs-outside offset at Lawrenceville, **always with the caveat that it is reported without n, duration or uncertainty**; the ~40 % MAE reduction from hygroscopic correction; and the self-compensation argument.
- Do **not** cite as a measurement of self-heating (it attributes to heat *trapping*), for a PM-error-per-%RH slope (it has none), or as comparable in rigour to Holder's 5.23 degC.
