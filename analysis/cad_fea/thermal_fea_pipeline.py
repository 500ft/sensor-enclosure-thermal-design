#!/usr/bin/env python3
"""Conjugate-heat-transfer (CHT) thermal-FEA pipeline -- INSTALL-PENDING STUB.

STATUS: SCAFFOLDING. This file documents and stubs the steady-state thermal /
conjugate-heat-transfer FEA workflow planned in ``docs/cad_fea_plan.md`` Section
3.2. It does NOT run a solve today: the CAD kernel (CadQuery) and the FEA stack
are not installed in this environment. The stub is written so that, once the
toolchain exists, the same file runs the geometry -> mesh -> steady thermal solve
end to end without re-architecting.

The lumped analytical model in ``analysis/thermal_bias.py`` is the baseline this
FEA refines. The FEA's job is to (a) resolve the internal natural-convection
field and plate-to-air coupling that the lumped model approximates with a single
``shield_air_preheat`` term, and (b) give a spatial sensor-surface temperature
instead of one node. All FEA outputs remain SIMULATION, pending lab co-location
data; no regulatory-grade or certified claim is implied.

------------------------------------------------------------------------------
INSTALL (pending -- not required for the current deliverable)
------------------------------------------------------------------------------
Option A -- open-source CFD/CHT (recommended for the internal-convection case):
    # Geometry + meshing
    pip install cadquery==2.*           # parametric solid geometry (build123d also OK)
    # Mesh + solve (pick one stack)
    #   1) OpenFOAM (chtMultiRegionFoam) for true conjugate heat transfer:
    #        brew install openfoam        # or the openfoam.org / .com distribution
    #        pip install gmsh             # mesh generation from the exported geometry
    #   2) Elmer FEM (multiphysics, easier setup) for thermal-FEA + convection BC:
    #        brew install elmerfem        # or build from source
    #        pip install gmsh

Option B -- thermal FEA + convection-coefficient BC (decoupled fallback):
    pip install cadquery==2.* gmsh
    pip install sfepy                     # or use CalculiX (ccx) for the thermal solve
    # External/internal convection enters as h*(T - T_ref) Robin BCs taken from
    # the same correlations used in analysis/thermal_bias.py (consistency check).

------------------------------------------------------------------------------
RUN (once installed)
------------------------------------------------------------------------------
    python analysis/cad_fea/thermal_fea_pipeline.py --variant V1 --g 1000 --wind 0.5
    # writes: analysis/cad_fea/out/<variant>_<g>_<wind>/  (mesh, field, summary)

------------------------------------------------------------------------------
PIPELINE STAGES (each is a stub raising NotImplementedError until wired)
------------------------------------------------------------------------------
  1. build_geometry(variant)      parametric CAD per docs/cad_fea_plan.md 3.1
  2. mesh_geometry(geom)          surface+volume mesh (gmsh), with refinement
                                  near the sensor and inter-plate gaps
  3. set_boundary_conditions()    solar flux on sun-facing faces (alpha*G),
                                  long-wave radiation to sky (eps,T_sky) and to
                                  surroundings (T_air), external convection
                                  (wind->h), internal heat source (electronics W)
  4. solve_steady(...)            steady CHT (or thermal-FEA + Robin BC fallback)
  5. extract_sensor_temperature() sample T at the sensor location -> delta-T
  6. write_summary(...)           per-run table row comparable to thermal_bias.py

The parameter table (alpha, eps, G, T_sky, areas, internal load, plate count/
spacing, vent area) is intentionally the SAME ledger as thermal_bias.ASSUMPTIONS
so the lumped baseline and the FEA refinement are driven from one source of
truth and can be cross-checked.
"""

from __future__ import annotations

import argparse


INSTALL_PENDING_MSG = (
    "thermal_fea_pipeline.py is an INSTALL-PENDING STUB.\n"
    "The CadQuery/gmsh/OpenFOAM(or Elmer/SfePy) toolchain is not installed, so "
    "no FEA solve runs yet.\n"
    "Use analysis/thermal_bias.py for the current analytical baseline result.\n"
    "See this file's header for the exact install and run steps."
)


def _require_toolchain() -> None:
    missing = []
    for mod in ("cadquery", "gmsh"):
        try:
            __import__(mod)
        except Exception:  # noqa: BLE001
            missing.append(mod)
    if missing:
        raise SystemExit(
            INSTALL_PENDING_MSG
            + f"\n\nMissing modules: {', '.join(missing)}"
        )


def build_geometry(variant: str):
    """Stage 1: parametric CAD per docs/cad_fea_plan.md 3.1. STUB."""
    raise NotImplementedError(
        "build_geometry: wire CadQuery/build123d parametric model of "
        f"variant {variant!r} here (plate count/spacing, vent area, sensor pos)."
    )


def mesh_geometry(geom):
    """Stage 2: gmsh surface+volume mesh with sensor/gap refinement. STUB."""
    raise NotImplementedError("mesh_geometry: wire gmsh meshing here.")


def set_boundary_conditions(mesh, g_solar: float, wind_ms: float):
    """Stage 3: solar/radiation/convection/internal-load BCs. STUB.

    BCs must reuse thermal_bias.ASSUMPTIONS (alpha, eps, T_sky offset, h(wind),
    internal W) so the FEA is a refinement of -- not a contradiction of -- the
    lumped baseline.
    """
    raise NotImplementedError("set_boundary_conditions: map ledger inputs to BCs.")


def solve_steady(mesh, bcs):
    """Stage 4: steady CHT solve (OpenFOAM/Elmer) or thermal-FEA fallback. STUB."""
    raise NotImplementedError("solve_steady: call the CHT/thermal solver here.")


def extract_sensor_temperature(field) -> float:
    """Stage 5: sample T at the sensor node -> return delta-T above ambient. STUB."""
    raise NotImplementedError("extract_sensor_temperature: sample sensor node.")


def run(variant: str, g_solar: float, wind_ms: float) -> None:
    """End-to-end CHT run for one operating point. Wired once toolchain exists."""
    _require_toolchain()
    geom = build_geometry(variant)
    mesh = mesh_geometry(geom)
    bcs = set_boundary_conditions(mesh, g_solar, wind_ms)
    field = solve_steady(mesh, bcs)
    delta_t = extract_sensor_temperature(field)
    print(f"[FEA] {variant} G={g_solar} wind={wind_ms} -> sensor delta-T = {delta_t:.2f} C")


def main() -> None:
    p = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    p.add_argument("--variant", default="V1", choices=["V0", "V1", "V2"])
    p.add_argument("--g", type=float, default=1000.0, help="solar flux [W/m^2]")
    p.add_argument("--wind", type=float, default=0.5, help="wind speed [m/s]")
    p.add_argument("--check", action="store_true",
                   help="Report toolchain status and exit (no solve).")
    args = p.parse_args()

    if args.check:
        try:
            _require_toolchain()
        except SystemExit as exc:
            print(exc)
            return
        print("Toolchain present. (Solver stages are still stubs -- wire them in run().)")
        return

    # Default behavior today: explain that this is install-pending, do not crash.
    print(INSTALL_PENDING_MSG)


if __name__ == "__main__":
    main()
