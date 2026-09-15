"""End-to-end rehearsal: intake -> metrics on synthetic CSVs with known answers and malformed inputs."""
import copy, csv, hashlib, json, math, subprocess, sys, tempfile, unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path
from analysis import colocation_rehearsal as R

ROOT = Path(__file__).resolve().parents[2]
START = datetime(2026, 1, 1, tzinfo=timezone.utc)


def _run_files(rows, metadata, tmp):
    csv_path, meta_path = R.write_inputs(rows, metadata, Path(tmp))
    return R.rehearse(csv_path, meta_path, Path(tmp) / "out")


class KnownAnswerTests(unittest.TestCase):
    def test_generated_case_reproduces_its_known_answers_exactly(self):
        rows, metadata, known = R.generate(START)
        with tempfile.TemporaryDirectory() as tmp:
            csv_path, meta_path = R.write_inputs(rows, metadata, Path(tmp))
            rep = R.rehearse(csv_path, meta_path, Path(tmp) / "out", known)
        self.assertEqual(rep["intake_exit_code"], 3)                      # synthetic is never evidence
        self.assertEqual(rep["intake"]["classification"], "SYNTHETIC_ONLY")
        self.assertFalse(rep["intake"]["validates_thermal_model"])
        self.assertTrue(rep["comparison"]["all_ok"], rep["comparison"])
        self.assertEqual(rep["metrics"]["count"], known["paired_slots"])
        self.assertAlmostEqual(rep["metrics"]["bias"], known["bias"], places=12)
        self.assertAlmostEqual(rep["metrics"]["rmse"], known["rmse"], places=12)

    def test_known_answer_arithmetic_is_what_the_generator_says(self):
        # 14 rows are blanked (i in 97..1358 step 97 -> 14 values); 1426 paired; bias is the
        # exact mean of the constructed residual, computed here independently of generate().
        rows, _, known = R.generate(START)
        blanks = [i for i in range(1, 1440) if i % 97 == 0]
        self.assertEqual(len(blanks), 14)
        self.assertEqual(known["paired_slots"], 1440 - 14)
        resid = [0.8 + 0.3 * i / 1440 + (-0.5 if not (360 <= i < 1080) else 0.0) for i in range(1440) if i not in blanks]
        # known["bias"] is computed from the 6-dp values as written, so agreement is to ~1e-7, not 1e-12
        self.assertAlmostEqual(known["bias"], sum(resid) / len(resid), places=6)
        # and the residual read back from the CSV text equals known exactly
        back = [float(r["sensor_temperature"]) - float(r["reference_temperature"]) for r in rows if r["sensor_temperature"] != ""]
        self.assertEqual(sum(back) / len(back), known["bias"])
        self.assertEqual(sum(1 for r in rows if r["sensor_temperature"] == ""), 14)

    def test_zero_residual_case_gives_zero_metrics(self):
        rows, metadata, known = R.generate(START, bias_c=0.0, drift_c_per_day=0.0, night_offset_c=0.0, missing_every=None)
        with tempfile.TemporaryDirectory() as tmp:
            csv_path, meta_path = R.write_inputs(rows, metadata, Path(tmp))
            rep = R.rehearse(csv_path, meta_path, Path(tmp) / "out", known)
        self.assertEqual(rep["metrics"]["count"], 1440)
        for k in ("bias", "mae", "rmse"):
            self.assertAlmostEqual(rep["metrics"][k], 0.0, places=12)
        self.assertEqual(rep["metrics"]["paired_completeness"], 1.0)

    def test_negative_control_a_wrong_known_answer_is_detected(self):
        rows, metadata, known = R.generate(START)
        wrong = dict(known, bias=known["bias"] + 0.01)
        with tempfile.TemporaryDirectory() as tmp:
            csv_path, meta_path = R.write_inputs(rows, metadata, Path(tmp))
            rep = R.rehearse(csv_path, meta_path, Path(tmp) / "out", wrong)
        self.assertFalse(rep["comparison"]["all_ok"])
        self.assertFalse(rep["comparison"]["items"]["metrics.bias"]["ok"])

    def test_cli_generates_runs_and_reports(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = subprocess.run([sys.executable, "-m", "analysis.colocation_rehearsal", "--out-dir", tmp], cwd=ROOT, capture_output=True, text=True)
            self.assertEqual(p.returncode, 0, p.stdout + p.stderr)
            self.assertIn("SYNTHETIC_ONLY", p.stdout); self.assertIn("ALL OK", p.stdout)
            rep = json.loads((Path(tmp) / "rehearsal.json").read_text())
            self.assertEqual(rep["csv_sha256"], hashlib.sha256((Path(tmp) / "rehearsal.csv").read_bytes()).hexdigest())
            self.assertFalse(rep["validates_thermal_model"])


class GenerationRefusalTests(unittest.TestCase):
    """Review 3 (2026-09-16): the generation CLI called write_inputs() into out_dir BEFORE the
    collision check in snapshot(), so a refused rerun (exit 5) still overwrote the previous run's
    rehearsal.csv/.metadata.json. Refusal now precedes the first write. These drive the real CLI."""

    def _cli(self, out_dir):
        return subprocess.run([sys.executable, "-m", "analysis.colocation_rehearsal", "--out-dir", str(out_dir)],
                              cwd=ROOT, capture_output=True, text=True)

    def _manifest(self, root):
        root = Path(root)
        return {str(p.relative_to(root)): hashlib.sha256(p.read_bytes()).hexdigest()
                for p in sorted(root.rglob("*")) if p.is_file()}

    def _seed_run(self, out):
        # Seed the prior run with a DIFFERENT bias than the CLI default, so a buggy overwrite is
        # visible in a content hash instead of hiding behind identical regenerated bytes.
        rows, metadata, known = R.generate(START, bias_c=2.0)
        csv_path, meta_path = R.write_inputs(rows, metadata, out)
        R.rehearse(csv_path, meta_path, out, known)

    def test_rerun_over_existing_run_refuses_before_changing_creating_or_removing_anything(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "run"; out.mkdir()
            self._seed_run(out)
            (out / "sentinel.txt").write_text("do not touch")            # unrelated sentinel
            before = self._manifest(out)
            r = self._cli(out)                                           # CLI regenerates at default bias
            self.assertEqual(r.returncode, 5, r.stdout + r.stderr)
            self.assertIn("COLLISION", r.stdout)
            self.assertEqual(self._manifest(out), before)                # nothing changed/created/removed

    def test_preexisting_generated_inputs_without_a_report_are_refused_before_overwrite(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "run"; out.mkdir()
            (out / "rehearsal.csv").write_text("SENTINEL-OLD-CSV\n")      # inputs only, no report/snapshot
            (out / "rehearsal.metadata.json").write_text('{"sentinel": "old"}\n')
            before = self._manifest(out)
            r = self._cli(out)
            self.assertEqual(r.returncode, 5, r.stdout + r.stderr)
            self.assertEqual(self._manifest(out), before)                # generated filenames NOT overwritten

    def test_fresh_and_empty_directories_work_and_unrelated_files_survive(self):
        with tempfile.TemporaryDirectory() as tmp:
            self.assertEqual(self._cli(Path(tmp) / "fresh").returncode, 0)    # non-existent dir
            out = Path(tmp) / "empty"; out.mkdir()
            (out / "notes.txt").write_text("keep me")                        # unrelated existing file
            self.assertEqual(self._cli(out).returncode, 0)
            self.assertEqual((out / "notes.txt").read_text(), "keep me")     # preserved
            rep = json.loads((out / "rehearsal.json").read_text())
            self.assertEqual(rep["intake"]["classification"], "SYNTHETIC_ONLY")
            self.assertFalse(rep["validates_thermal_model"])
            self.assertEqual(rep["csv_sha256"], hashlib.sha256((out / "rehearsal.csv").read_bytes()).hexdigest())

    def test_occupied_directory_is_refused_through_a_symlink_too(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "run"; out.mkdir()
            self._seed_run(out)
            link = Path(tmp) / "run-link"
            try:
                link.symlink_to(out, target_is_directory=True)
            except (OSError, NotImplementedError):
                self.skipTest("symlinks unsupported on this platform")
            before = self._manifest(out)
            r = self._cli(link)
            self.assertEqual(r.returncode, 5, r.stdout + r.stderr)
            self.assertEqual(self._manifest(out), before)                # same occupied dir, still untouched


class IntegrityTests(unittest.TestCase):
    """Review finding 2026-09-12: the original CSV could be changed after intake and the metrics
    silently used the changed file. Now every step reads one read-only snapshot."""

    def test_mutating_the_original_after_snapshot_changes_nothing(self):
        rows, metadata, known = R.generate(START)
        with tempfile.TemporaryDirectory() as tmp:
            csv_path, meta_path = R.write_inputs(rows, metadata, Path(tmp))
            orig_intake = R.run_intake
            def mutate_original_then_intake(c, m):
                txt = csv_path.read_text().splitlines(); txt[1] = txt[1].replace(txt[1].split(",")[1], "99.0", 1)
                csv_path.write_text("\n".join(txt) + "\n")            # original changes; snapshot does not
                return orig_intake(c, m)
            R.run_intake = mutate_original_then_intake
            try:
                rep = R.rehearse(csv_path, meta_path, Path(tmp) / "out", known)
            finally:
                R.run_intake = orig_intake
        self.assertTrue(rep["comparison"]["all_ok"])
        self.assertEqual(rep["csv_sha256"], rep["intake"]["csv_sha256"])
        self.assertEqual(rep["metrics_input_sha256"], rep["intake"]["csv_sha256"])

    def test_tampering_with_the_snapshot_between_steps_is_an_integrity_failure(self):
        import os, stat
        rows, metadata, known = R.generate(START)
        with tempfile.TemporaryDirectory() as tmp:
            csv_path, meta_path = R.write_inputs(rows, metadata, Path(tmp))
            orig_intake = R.run_intake
            def intake_then_tamper_snapshot(c, m):
                out = orig_intake(c, m)
                c.chmod(stat.S_IWUSR | stat.S_IRUSR)
                txt = c.read_text().splitlines(); txt[1] = txt[1].replace(txt[1].split(",")[1], "99.0", 1); c.write_text("\n".join(txt) + "\n")
                return out
            R.run_intake = intake_then_tamper_snapshot
            try:
                with self.assertRaises(R.IntegrityError):
                    R.rehearse(csv_path, meta_path, Path(tmp) / "out", known)
            finally:
                R.run_intake = orig_intake

    def test_snapshot_files_are_read_only(self):
        import stat
        rows, metadata, _ = R.generate(START)
        with tempfile.TemporaryDirectory() as tmp:
            csv_path, meta_path = R.write_inputs(rows, metadata, Path(tmp))
            R.rehearse(csv_path, meta_path, Path(tmp) / "out")
            for name in ("input.csv", "input.metadata.json"):
                mode = (Path(tmp) / "out/snapshot" / name).stat().st_mode
                self.assertFalse(mode & stat.S_IWUSR, name)


class ReplayAndMetadataTests(unittest.TestCase):
    """Review 2 (2026-09-12): replaying a snapshot into its own run directory deleted the snapshot
    and left a report pointing at a missing file; metadata could change between snapshot and intake
    while metrics kept the original dictionary."""

    def _first_run(self, tmp):
        rows, metadata, known = R.generate(START)
        csv_path, meta_path = R.write_inputs(rows, metadata, Path(tmp) / "in")
        rep = R.rehearse(csv_path, meta_path, Path(tmp) / "out", known)
        return rep, Path(tmp) / "out"

    def test_replay_into_own_output_directory_is_refused_before_touching_anything(self):
        with tempfile.TemporaryDirectory() as tmp:
            rep, out = self._first_run(tmp)
            snap_csv, snap_meta = out / "snapshot/input.csv", out / "snapshot/input.metadata.json"
            before = (snap_csv.read_bytes(), (out / "rehearsal.json").read_bytes())
            with self.assertRaises(R.CollisionError):
                R.rehearse(snap_csv, snap_meta, out)
            self.assertTrue(snap_csv.exists() and snap_meta.exists())
            self.assertEqual((snap_csv.read_bytes(), (out / "rehearsal.json").read_bytes()), before)

    def test_replay_of_a_saved_snapshot_into_a_fresh_directory_reproduces_the_report(self):
        with tempfile.TemporaryDirectory() as tmp:
            rep, out = self._first_run(tmp)
            rep2 = R.rehearse(out / "snapshot/input.csv", out / "snapshot/input.metadata.json", Path(tmp) / "out2", rep["known"])
            self.assertEqual(rep2["csv_sha256"], rep["csv_sha256"]); self.assertEqual(rep2["metadata_sha256"], rep["metadata_sha256"])
            self.assertEqual(rep2["metrics"], rep["metrics"]); self.assertEqual(rep2["intake"]["classification"], rep["intake"]["classification"])

    def test_existing_run_directory_is_refused(self):
        with tempfile.TemporaryDirectory() as tmp:
            rep, out = self._first_run(tmp)
            rows, metadata, known = R.generate(START)
            csv_path, meta_path = R.write_inputs(rows, metadata, Path(tmp) / "in2")
            with self.assertRaises(R.CollisionError):
                R.rehearse(csv_path, meta_path, out, known)

    def test_metadata_swapped_between_snapshot_and_intake_is_an_integrity_failure(self):
        import stat
        rows, metadata, known = R.generate(START)
        with tempfile.TemporaryDirectory() as tmp:
            csv_path, meta_path = R.write_inputs(rows, metadata, Path(tmp) / "in")
            orig = R.run_intake
            def swap(c, m):
                m.chmod(stat.S_IWUSR | stat.S_IRUSR); mm = json.loads(m.read_text()); mm["evidence_kind"] = "physical"; m.write_text(json.dumps(mm))
                return orig(c, m)
            R.run_intake = swap
            try:
                with self.assertRaises(R.IntegrityError):
                    R.rehearse(csv_path, meta_path, Path(tmp) / "out", known)
            finally:
                R.run_intake = orig

    def test_report_binds_both_csv_and_metadata_hashes_to_the_intake(self):
        with tempfile.TemporaryDirectory() as tmp:
            rep, _ = self._first_run(tmp)
        self.assertEqual(rep["metadata_input_sha256"], rep["intake"]["metadata_sha256"])
        self.assertEqual(rep["metrics_input_sha256"], rep["intake"]["csv_sha256"])


class LedgerIntegrityTests(unittest.TestCase):
    def test_sprint_ledger_ids_are_unique(self):
        ids = [r["id"] for r in csv.DictReader((ROOT / "docs/SPRINT_TASKS.csv").open())]
        dupes = sorted({i for i in ids if ids.count(i) > 1})
        self.assertEqual(dupes, [], f"duplicate task ids: {dupes}")

    def test_owner_measurement_task_is_preserved_and_rehearsal_has_its_own_id(self):
        rows = {(r["id"], r["owner"]): r for r in csv.DictReader((ROOT / "docs/SPRINT_TASKS.csv").open())}
        self.assertIn(("EN-R03", "Owner"), rows); self.assertEqual(rows[("EN-R03", "Owner")]["status"], "blocked")
        self.assertIn(("EN-R03S", "Agent"), rows); self.assertEqual(rows[("EN-R03S", "Agent")]["status"], "done")


class MalformedDataTests(unittest.TestCase):
    def setUp(self):
        self.rows, self.metadata, _ = R.generate(START, missing_every=None)

    def _expect_refusal(self, rows, metadata, fragment):
        with tempfile.TemporaryDirectory() as tmp:
            rep = _run_files(rows, metadata, tmp)
        self.assertEqual(rep["intake_exit_code"], 2, rep)
        self.assertIsNone(rep["metrics"], "metrics must not be computed on refused input")
        self.assertIn(fragment, rep["intake_error"])

    def test_hash_mismatch_is_refused_before_anything_else(self):
        with tempfile.TemporaryDirectory() as tmp:
            csv_path, meta_path = R.write_inputs(self.rows, self.metadata, Path(tmp))
            csv_path.write_text(csv_path.read_text() + "\n")          # bytes change, metadata hash stale
            rep = R.rehearse(csv_path, meta_path, Path(tmp) / "out")
        self.assertEqual(rep["intake_exit_code"], 2); self.assertIn("csv_sha256 mismatch", rep["intake_error"])

    def test_duplicate_slot_is_refused(self):
        rows = self.rows + [self.rows[500]]
        rows.sort(key=lambda r: r["timestamp"])
        self._expect_refusal(rows, self.metadata, "duplicate sampling slot")

    def test_off_grid_timestamp_is_refused(self):
        rows = copy.deepcopy(self.rows); rows[10]["timestamp"] = (START + timedelta(minutes=10, seconds=30)).isoformat()
        self._expect_refusal(rows, self.metadata, "off the exact 60-second sample grid")

    def test_non_chronological_rows_are_refused(self):
        rows = copy.deepcopy(self.rows); rows[5], rows[6] = rows[6], rows[5]
        self._expect_refusal(rows, self.metadata, "chronological")

    def test_negative_or_nonnumeric_weather_is_refused(self):
        rows = copy.deepcopy(self.rows); rows[700]["solar_w_m2"] = "-5"
        self._expect_refusal(rows, self.metadata, "weather observations")
        rows = copy.deepcopy(self.rows); rows[700]["wind_m_s"] = "calm"
        self._expect_refusal(rows, self.metadata, "weather observations")

    def test_extra_column_is_refused(self):
        rows = [dict(r, humidity="50") for r in self.rows]
        with tempfile.TemporaryDirectory() as tmp:
            csv_path = Path(tmp) / "x.csv"
            with csv_path.open("w", newline="") as fh:
                w = csv.DictWriter(fh, fieldnames=R.FIELDS + ["humidity"]); w.writeheader(); w.writerows(rows)
            meta = dict(self.metadata, csv_sha256=hashlib.sha256(csv_path.read_bytes()).hexdigest())
            meta_path = Path(tmp) / "x.json"; meta_path.write_text(json.dumps(meta))
            rep = R.rehearse(csv_path, meta_path, Path(tmp) / "out")
        self.assertEqual(rep["intake_exit_code"], 2); self.assertIn("intake schema", rep["intake_error"])

    def test_missing_provenance_and_bad_uncertainty_are_refused(self):
        meta = dict(self.metadata); meta["calibration_reference"] = ""
        self._expect_refusal(self.rows, meta, "missing declared provenance")
        meta = dict(self.metadata, paired_u95_c=0)
        self._expect_refusal(self.rows, meta, "paired_u95_c")

    def test_wrong_window_length_is_refused(self):
        meta = dict(self.metadata, window_end=(START + timedelta(hours=23)).isoformat())
        self._expect_refusal(self.rows, meta, "24-hour window")

    def test_day_only_data_is_incomplete_not_refused_and_metrics_still_run(self):
        # INCOMPLETE is admitted data that fails the coverage thresholds; the CLI exits 2 like a
        # refusal but returns a result, and the metrics are still computed so the shortfall is visible.
        rows = [r for r in self.rows if float(r["solar_w_m2"]) > 5]                   # night removed
        with tempfile.TemporaryDirectory() as tmp:
            rep = _run_files(rows, self.metadata, tmp)
        self.assertEqual(rep["intake"]["classification"], "INCOMPLETE")
        self.assertEqual(rep["intake_exit_code"], 2)
        self.assertEqual(rep["intake"]["low_solar_paired_slots"], 0)
        self.assertIsNotNone(rep["metrics"]); self.assertEqual(rep["metrics"]["count"], 720)

    def test_too_much_missing_data_is_incomplete(self):
        rows, metadata, _ = R.generate(START, missing_every=5)                           # ~20 % blanked
        with tempfile.TemporaryDirectory() as tmp:
            rep = _run_files(rows, metadata, tmp)
        self.assertEqual(rep["intake"]["classification"], "INCOMPLETE")
        self.assertLess(rep["intake"]["paired_fraction"], 0.90)

    def test_physical_declaration_on_synthetic_shape_is_reviewable_not_validated(self):
        # The intake cannot tell a mislabelled synthetic file from a real one; this records that
        # the declaration is the owner's and that even then validates_thermal_model stays False.
        meta = dict(self.metadata, evidence_kind="physical")
        with tempfile.TemporaryDirectory() as tmp:
            rep = _run_files(self.rows, meta, tmp)
        self.assertEqual(rep["intake"]["classification"], "REVIEWABLE_PILOT")
        self.assertFalse(rep["intake"]["validates_thermal_model"]); self.assertFalse(rep["validates_thermal_model"])


if __name__ == "__main__":
    unittest.main()
