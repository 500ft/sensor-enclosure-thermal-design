#!/usr/bin/env python3
"""One reproducible workflow from a co-location CSV to the existing metrics, on synthetic data.

    python -m analysis.colocation_rehearsal --out-dir build/rehearsal            # generate + run
    python -m analysis.colocation_rehearsal --csv X.csv --metadata X.json --out-dir D   # run on given files

Steps, in the order the protocol (docs/COLOCATION_PROTOCOL.md) requires:
  1. intake   -> analysis.colocation_intake CLI on the CSV + metadata (hash-checked). Exit 2 stops here.
  2. metrics  -> analysis.compute_metrics.compute_metrics on the SAME rows, 1-min schedule, declared window.
  3. report   -> rehearsal.json: intake result, metrics, the generator's KNOWN answers where the
                 CSV was generated here, and the comparison. classification is carried unchanged.

What this is not: evidence. Every generated CSV is declared evidence_kind=synthetic, the intake
labels it SYNTHETIC_ONLY (exit 3), and validates_thermal_model is False throughout. The known
answers exist so the arithmetic chain is checked end to end BEFORE a real CSV arrives -- the
first physical file is then judged by the same, already-exercised commands.
"""
from __future__ import annotations
import argparse, csv, hashlib, json, math, subprocess, sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

from analysis.compute_metrics import compute_metrics, parse_timestamp

ROOT = Path(__file__).resolve().parents[1]
FIELDS = ["timestamp", "sensor_temperature", "reference_temperature", "solar_w_m2", "wind_m_s"]


def generate(start: datetime, *, bias_c: float = 0.8, drift_c_per_day: float = 0.3,
             night_offset_c: float = -0.5, day_solar: float = 600.0, missing_every: int | None = 97,
             seed_label: str = "SYNTHETIC-CASE") -> tuple[list[dict], dict, dict]:
    """1440 one-minute rows with a KNOWN residual structure; returns (rows, metadata, known).

    residual = bias + drift * t_days + (night_offset if solar <= 5 else 0); no noise, so the
    expected metrics are exact arithmetic on the written 6-dp values, not a fit. Every `missing_every`-th row has an empty
    sensor value (missing, never zero), which the intake must count as unpaired.
    """
    rows, residuals, times = [], [], []
    for i in range(1440):
        t = start + timedelta(minutes=i)
        solar = day_solar if 360 <= i < 1080 else 0.0
        ref = 20.0 + 6.0 * math.sin(math.pi * (i - 360) / 720) if 360 <= i < 1080 else 18.0
        resid = bias_c + drift_c_per_day * (i / 1440.0) + (night_offset_c if solar <= 5 else 0.0)
        missing = missing_every is not None and i % missing_every == 0 and i > 0
        sensor_txt, ref_txt = f"{ref + resid:.6f}", f"{ref:.6f}"
        rows.append(dict(timestamp=t.isoformat(), sensor_temperature="" if missing else sensor_txt,
                         reference_temperature=ref_txt, solar_w_m2=f"{solar:.1f}", wind_m_s="1.0"))
        if not missing:
            # Known answers are computed from the VALUES AS WRITTEN (6 dp), so the comparison is
            # exact arithmetic on the same bytes the intake and metrics read, not the pre-rounding floats.
            residuals.append(float(sensor_txt) - float(ref_txt)); times.append(i / 1440.0)
    n = len(residuals)
    mean_r = sum(residuals) / n
    known = dict(paired_slots=n, expected_slots=1440, paired_fraction=n / 1440,
                 bias=mean_r, mae=sum(abs(r) for r in residuals) / n,
                 rmse=math.sqrt(sum(r * r for r in residuals) / n),
                 illuminated_paired_slots=sum(1 for r, row in zip(residuals, [x for x in rows if x["sensor_temperature"] != ""]) if float(row["solar_w_m2"]) >= 200),
                 low_solar_paired_slots=sum(1 for row in rows if row["sensor_temperature"] != "" and float(row["solar_w_m2"]) <= 5),
                 inputs=dict(bias_c=bias_c, drift_c_per_day=drift_c_per_day, night_offset_c=night_offset_c, missing_every=missing_every))
    metadata = dict(window_start=start.isoformat(), window_end=(start + timedelta(days=1)).isoformat(),
                    sensor_id=f"{seed_label}-SENSOR", reference_id=f"{seed_label}-REFERENCE", site_id=f"{seed_label}-SITE",
                    firmware="rehearsal generator", clock_basis="UTC sample time",
                    calibration_reference="synthetic rehearsal only", uncertainty_reference="synthetic rehearsal only",
                    permission_reference="not actual permission", protocol_reference="docs/COLOCATION_PROTOCOL.md rehearsal",
                    evidence_kind="synthetic", paired_u95_c=0.2)
    return rows, metadata, known


def write_inputs(rows, metadata, out_dir: Path) -> tuple[Path, Path]:
    out_dir.mkdir(parents=True, exist_ok=True)
    csv_path, meta_path = out_dir / "rehearsal.csv", out_dir / "rehearsal.metadata.json"
    with csv_path.open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=FIELDS); w.writeheader(); w.writerows(rows)
    metadata = dict(metadata, csv_sha256=hashlib.sha256(csv_path.read_bytes()).hexdigest())
    meta_path.write_text(json.dumps(metadata, indent=2) + "\n")
    return csv_path, meta_path


def run_intake(csv_path: Path, meta_path: Path) -> tuple[int, dict | None, str]:
    p = subprocess.run([sys.executable, "-m", "analysis.colocation_intake", str(csv_path), "--metadata", str(meta_path)],
                       cwd=ROOT, capture_output=True, text=True)
    # The intake CLI exits 2 both for a REFUSED input (error text on stderr, no JSON) and for an
    # admitted-but-INCOMPLETE file (JSON on stdout). Distinguish by the presence of a result.
    try:
        return p.returncode, json.loads(p.stdout), ""
    except (json.JSONDecodeError, ValueError):
        return p.returncode, None, (p.stderr or p.stdout).strip()


def run_metrics(csv_path: Path, metadata: dict) -> dict:
    with csv_path.open(newline="") as fh:
        rows = [(parse_timestamp(r["timestamp"]), r["sensor_temperature"], r["reference_temperature"]) for r in csv.DictReader(fh)]
    m = compute_metrics(rows, 1, window_start=parse_timestamp(metadata["window_start"]), window_end=parse_timestamp(metadata["window_end"]))
    return {k: getattr(m, k) for k in ("count", "expected_count", "bias", "mae", "rmse", "correlation", "drift_per_day",
                                        "paired_completeness", "delivery_completeness", "duplicate_slot_records", "off_grid_records", "outside_window_records", "completeness_basis")}


def compare(known: dict | None, intake: dict | None, metrics: dict | None, tol: float = 1e-6) -> dict:
    if known is None or intake is None or metrics is None:
        return {"checked": False, "reason": "no known answers (external CSV) or intake refused"}
    checks = {
        "intake.paired_slots": (intake["paired_slots"], known["paired_slots"]),
        "intake.illuminated_paired_slots": (intake["illuminated_paired_slots"], known["illuminated_paired_slots"]),
        "intake.low_solar_paired_slots": (intake["low_solar_paired_slots"], known["low_solar_paired_slots"]),
        "metrics.count": (metrics["count"], known["paired_slots"]),
        "metrics.bias": (metrics["bias"], known["bias"]),
        "metrics.mae": (metrics["mae"], known["mae"]),
        "metrics.rmse": (metrics["rmse"], known["rmse"]),
        "metrics.paired_completeness": (metrics["paired_completeness"], known["paired_fraction"]),
    }
    out = {k: dict(got=g, expected=e, ok=abs(float(g) - float(e)) <= tol) for k, (g, e) in checks.items()}
    return {"checked": True, "all_ok": all(v["ok"] for v in out.values()), "tolerance": tol, "items": out}


def rehearse(csv_path: Path, meta_path: Path, out_dir: Path, known: dict | None = None) -> dict:
    metadata = json.loads(meta_path.read_text())
    rc, intake, err = run_intake(csv_path, meta_path)
    report = dict(schema_version=1, csv=str(csv_path), csv_sha256=hashlib.sha256(csv_path.read_bytes()).hexdigest(),
                  metadata_sha256=hashlib.sha256(meta_path.read_bytes()).hexdigest(),
                  intake_exit_code=rc, intake=intake, intake_error=err or None, metrics=None, known=known, comparison=None,
                  validates_thermal_model=False,
                  note="Synthetic rehearsal of the intake-to-metrics chain. Classification is the intake's, carried unchanged; SYNTHETIC_ONLY data is never evidence.")
    if intake is not None:
        report["metrics"] = run_metrics(csv_path, metadata)
        report["comparison"] = compare(known, intake, report["metrics"])
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "rehearsal.json").write_text(json.dumps(report, indent=2, allow_nan=False) + "\n")
    return report


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--csv", type=Path); ap.add_argument("--metadata", type=Path)
    ap.add_argument("--out-dir", type=Path, required=True)
    a = ap.parse_args(argv)
    if (a.csv is None) != (a.metadata is None):
        ap.error("--csv and --metadata go together")
    known = None
    if a.csv is None:
        rows, metadata, known = generate(datetime(2026, 1, 1, tzinfo=timezone.utc))
        a.csv, a.metadata = write_inputs(rows, metadata, a.out_dir)
    rep = rehearse(a.csv, a.metadata, a.out_dir, known)
    cls = rep["intake"]["classification"] if rep["intake"] else "REFUSED"
    cmp_ = rep["comparison"]
    print(f"intake: exit {rep['intake_exit_code']} {cls}" + (f" -- {rep['intake_error']}" if rep["intake_error"] else ""))
    if rep["metrics"]:
        print(f"metrics: n={rep['metrics']['count']} bias={rep['metrics']['bias']:.6f} mae={rep['metrics']['mae']:.6f} rmse={rep['metrics']['rmse']:.6f} paired_completeness={rep['metrics']['paired_completeness']:.6f}")
    if cmp_ and cmp_["checked"]:
        print("known-answer comparison:", "ALL OK" if cmp_["all_ok"] else "MISMATCH " + str([k for k, v in cmp_["items"].items() if not v["ok"]]))
    print("wrote", a.out_dir / "rehearsal.json")
    if rep["intake"] is None: return 2
    if cmp_ and cmp_["checked"] and not cmp_["all_ok"]: return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
