# V0 baseline enclosure — parametric CAD

Mirrors `~/Projects/Sensor-Enclosure-Thermal-Design/cad`. The STEP artifact is **not** committed
here (binary-ish, 278 kB); it lives with the build output in the Projects folder.

**All dimensions are `provisional_design` (route `design_then_inspect`).** None is a measurement of
existing hardware, and none may enter [`docs/PARAMETER_REGISTER.csv`](../../../docs/PARAMETER_REGISTER.csv)
without inspection — see task `EN-M01`.

Accepted 2026-09-26: volume, three bounding-box dimensions, solid count and **STEP re-import** all
matched an independent closed-form oracle. Parameter re-drive proved by changing `vent_width`
40 → 55 mm and recovering exactly the predicted 2 880 mm³ change.

`oracle.py` deliberately does **not** import CadQuery, so the expectation is genuinely independent
of the authoring path.
