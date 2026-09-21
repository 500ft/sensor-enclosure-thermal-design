# Week 2026-09-21 — Day 3 (W1/W2): Study B design and dimensionless extension contract

Base: `week/day2-competitors-20260922` at `c3abe72` (PR #22 open, **stacked**, not merged by the
agent). Branch `week/day3-studyb-design-20260923`. Inputs: design documents only — no analytical
run, no solver, no geometry, no physical data. W3 was completed on Day 1 (PR #21) and is not repeated.

## Section 9 (CAD amendment) — read and applied
- `500ft/engineering-audit@cf56cdf:docs/cad_agent_briefing.md` read in full via the GitHub API.
  Proven there: native SOLIDWORKS-COM authoring, named-variable re-drive, CadQuery oracle
  agreement, STEP round-trip, IGES→MAPDL linear-static FEA. **Not** proven: any thermal solve,
  assembly mates, drawing automation, formal FEA acceptance.
- W1 extended with the required reuse assessment (design.md §5): shared components to call in
  engineering-audit; seven enclosure-specific components still needed here; accepted vs unresolved
  dimensions (**none accepted**); independent expected-geometry checks; thermal benchmark B1–B5
  required before any CHT claim.
- Tooling conflict identified: `CAD_PLAN.md` / EN-CAD-09 allocate CadQuery + Onshape; Section 9
  prefers SOLIDWORKS-COM authoring with CadQuery as checker. A scoped rewording is **proposed**
  (design.md §6) and **not applied** — CAD work orders stay `deferred`; owner decision required.

## Deliverable
`docs/specs/study-b-cht/design.md`: SQ2 statement; smallest CHT study (V0/V0P/V1, all dims
unresolved); solver modes (a) thermal-FEA fallback vs (b) CHT with what each validates; seven-step
validation hierarchy with numerical thresholds and rationale (mesh <0.1 °C between finest levels;
energy residual <1 %; limiting cases directional); five thermal benchmarks with independent
expected answers; W2 contract for Bi, Re_vent, A_vent/A_surface, N_Q (both forms), tau,
Ra — inputs, pre-fab measurability, lumped/CHT coverage, omission failure mode, limiting behaviour,
dimensional check; held-out rule tied to K2; triggers.

Model-agreement tolerance vs physical data: **TBD** (owner/application); not invented.

## Gates (candidate)
See PR. No analysis code changed; suite unchanged at 104; thermal tables byte-identical.
