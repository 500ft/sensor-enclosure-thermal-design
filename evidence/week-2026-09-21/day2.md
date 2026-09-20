# Week 2026-09-21 — Day 2 (T1/T2/T3): competitor full reads

Base: `main` at `2de4cee` (PR #21 merged). Branch `week/day2-competitors-20260922`.
Inputs: LITERATURE only; no analytical, synthetic, historical or physical data touched.

## T1 — full-text reads (all six: FULL TEXT READ = YES)

| Key | Access route | Read status | Prediction timing |
|---|---|---|---|
| bernard2019 | mdpi.com 403 → `res.mdpi.com` PDF | full | fits after build (p0, p1 per shelter) |
| nakamura2005 | AMS HTML full text (PDF link empty); equations as images, tables from table images | full | empirical correction |
| vonrohden2022 | Copernicus PDF | full | fits after build (lab dT(p,v)) |
| barkjohn2021 | Copernicus PDF | full | empirical PM2.5 correction; **no own T/RH bias** |
| couzo2024 | mdpi.com 403 → `mdpi-res.com` PDF (revision markup pp. 3–7, cross-checked vs tables) | full | empirical correction; holds the +2.6 °C |
| ishizuka2012 | IOP PDF (curl hit captcha) | full | design Eqs pre-build; new K fitted post-build |

Not read (paywalled antecedents, not cited for content): Ishizuka 1987 ASME JHT; Ishizuka 2002
Proc. IMechE A. Ishizuka 2012 is peer-reviewed proceedings, flagged in bib `note` and ProConsList.

**Bibliographic corrections vs the 2026-09-16 abstract-level scan:** "Barbaresco 2019" → Bernard et
al.; "Cha 2024" → Couzo, Valencia & Gittis; the +2.6 °C is Couzo's, not Barkjohn's. Erratum
appended to `PHD_SCOPE_AND_NOVELTY.md`; names corrected in place in both direction docs.

## Files changed and why
- `paper/references.bib` +6, `literature/literature_matrix.csv` +6, `literature/sensor_material_geometry_summary.md` new section + 6 links, `ProConsList/{6}.md` — CONTRIBUTING literature protocol.
- `docs/COMPETITOR_MATRIX_2026-09-22.csv` — T2 (13 columns, 7 rows incl. this project).
- `docs/research-direction-2026-09-21.md` §9 (T3 gap→measurement) and §10 (T2 result; K2 benchmark defined).
- `docs/PHD_SCOPE_AND_NOVELTY.md` — erratum + in-place name corrections; verdict unchanged.

## Gates (candidate)
See PR body. `check_literature_coverage.py`: 32 bibliography / 32 analyses, complete.
