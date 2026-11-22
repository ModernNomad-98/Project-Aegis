"""Tests for Aegis Run Record v1 (standard-library unittest)."""

from __future__ import annotations

import contextlib
import hashlib
import io
import json
import os
import sys
import tempfile
import unittest
import uuid
from pathlib import Path
from unittest import mock

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from tools.aegis_run import MANIFEST_SCHEMA, RECORD_SCHEMA, __version__
from tools.aegis_run import cli
from tools.aegis_run.cli import main

COMMIT = "0123456789abcdef0123456789abcdef01234567"
EXAMPLE_DIR = REPO_ROOT / "docs" / "aegis-run" / "example"
MANIFEST_FIELDS = ("path", "source", "bytes", "sha256", "portable", "external")


def run_cli(*argv: str) -> tuple[int, str, str]:
    stdout, stderr = io.StringIO(), io.StringIO()
    with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
        try:
            code = main(list(argv))
        except SystemExit as exc:
            code = int(exc.code or 0)
    return code, stdout.getvalue(), stderr.getvalue()


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


class RunRecordTest(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.root = Path(self._tmp.name)
        self.run_dir = self.root / "run"
        self.record_path = self.run_dir / "aegis-run.json"
        self.manifest_path = self.run_dir / "manifest.json"

    def init(self) -> dict:
        code, _out, err = run_cli(
            "init",
            "--dir",
            str(self.run_dir),
            "--app",
            "demo-app",
            "--aegis-commit",
            COMMIT,
            "--host",
            "host-a",
            "--model",
            "DeepSeek",
            "--owner",
            "owner-a",
        )
        self.assertEqual(code, 0, err)
        return load_json(self.record_path)

    def add_event(self) -> None:
        code, _out, err = run_cli(
            "event",
            "--dir",
            str(self.run_dir),
            "--type",
            "stage",
            "--stage",
            "build",
            "--status",
            "passed",
            "--note",
            "tests green",
            "--actor",
            "builder",
        )
        self.assertEqual(code, 0, err)

    def add_inside_artifact(self) -> Path:
        target = self.run_dir / "evidence" / "report.txt"
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(b"hello artifact")
        code, _out, err = run_cli(
            "artifact", "--dir", str(self.run_dir), "--path", str(target), "--kind", "log"
        )
        self.assertEqual(code, 0, err)
        return target

    def finish(self) -> None:
        code, _out, err = run_cli(
            "finish",
            "--dir",
            str(self.run_dir),
            "--outcome",
            "delivered",
            "--limitation",
            "one host only",
            "--limitation",
            "no live provider run",
        )
        self.assertEqual(code, 0, err)

    def export(self) -> None:
        code, _out, err = run_cli("export", "--dir", str(self.run_dir))
        self.assertEqual(code, 0, err)

    def export_full(self) -> Path:
        self.init()
        self.add_event()
        target = self.add_inside_artifact()
        self.finish()
        self.export()
        return target

    def copied_path(self, source: str) -> Path:
        record = load_json(self.record_path)
        entry = next(item for item in record["artifacts"] if item["source"] == source)
        return self.run_dir / entry["path"]

    def rewrite(self, mutate) -> None:
        record = load_json(self.record_path)
        mutate(record)
        text = json.dumps(record, sort_keys=True, indent=2, ensure_ascii=False) + "\n"
        self.record_path.write_text(text, encoding="utf-8")
        manifest = load_json(self.manifest_path)
        manifest["artifacts"] = [
            {field: item.get(field) for field in MANIFEST_FIELDS}
            for item in record["artifacts"]
        ]
        manifest["record_sha256"] = sha256_bytes(text.encode("utf-8"))
        self.manifest_path.write_text(
            json.dumps(manifest, sort_keys=True, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )

    # -- init ---------------------------------------------------------

    def test_init_writes_record_and_empty_event_log(self) -> None:
        record = self.init()
        self.assertEqual(record["schema"], RECORD_SCHEMA)
        self.assertEqual(RECORD_SCHEMA, "aegis.run-record/1")
        self.assertEqual(str(uuid.UUID(record["run_id"])), record["run_id"])
        self.assertTrue(record["created_at"].endswith("Z"))
        self.assertEqual(record["app"], "demo-app")
        self.assertEqual(record["aegis_commit"], COMMIT)
        self.assertEqual(record["host"], "host-a")
        self.assertEqual(record["model"], "DeepSeek")
        self.assertEqual(record["owner"], "owner-a")
        self.assertEqual(record["events"], [])
        self.assertEqual(record["artifacts"], [])
        self.assertEqual(record["limitations"], [])
        self.assertIsNone(record["outcome"])
        events_path = self.run_dir / "events.jsonl"
        self.assertTrue(events_path.is_file())
        self.assertEqual(events_path.read_bytes(), b"")

    def test_init_refuses_to_overwrite(self) -> None:
        self.init()
        code, _out, _err = run_cli(
            "init",
            "--dir",
            str(self.run_dir),
            "--app",
            "other",
            "--aegis-commit",
            COMMIT,
            "--host",
            "host-b",
        )
        self.assertEqual(code, 1)

    def test_version_flag(self) -> None:
        code, out, _err = run_cli("--version")
        self.assertEqual(code, 0)
        self.assertIn(__version__, out)

    # -- event --------------------------------------------------------

    def test_event_appends_jsonl_and_mirrors_state(self) -> None:
        self.init()
        self.add_event()
        code, _out, err = run_cli(
            "event",
            "--dir",
            str(self.run_dir),
            "--type",
            "approval",
            "--stage",
            "build",
            "--status",
            "skipped",
        )
        self.assertEqual(code, 0, err)
        lines = [
            json.loads(line)
            for line in (self.run_dir / "events.jsonl").read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]
        record = load_json(self.record_path)
        self.assertEqual(len(lines), 2)
        self.assertEqual(record["events"], lines)
        self.assertEqual(set(lines[0]), {"ts", "type", "stage", "status", "note", "actor"})
        self.assertEqual(lines[0]["type"], "stage")
        self.assertEqual(lines[0]["status"], "passed")
        self.assertEqual(lines[0]["note"], "tests green")
        self.assertEqual(lines[0]["actor"], "builder")
        self.assertIsNone(lines[1]["note"])
        self.assertIsNone(lines[1]["actor"])

    def test_event_rejects_invalid_type(self) -> None:
        self.init()
        code, _out, _err = run_cli(
            "event",
            "--dir",
            str(self.run_dir),
            "--type",
            "bogus",
            "--stage",
            "build",
            "--status",
            "started",
        )
        self.assertEqual(code, 2)

    # -- artifact -----------------------------------------------------

    def test_artifact_inside_is_copied_with_relative_paths(self) -> None:
        self.init()
        target = self.add_inside_artifact()
        data = target.read_bytes()
        entry = load_json(self.record_path)["artifacts"][0]
        expected = "artifacts/%s-report.txt" % sha256_bytes(data)[:12]
        self.assertEqual(entry["path"], expected)
        self.assertEqual(entry["source"], "evidence/report.txt")
        self.assertFalse(Path(entry["path"]).is_absolute())
        self.assertFalse(Path(entry["source"]).is_absolute())
        self.assertTrue(entry["portable"])
        self.assertFalse(entry["external"])
        self.assertEqual(entry["bytes"], len(data))
        self.assertEqual(entry["sha256"], sha256_bytes(data))
        self.assertEqual(entry["kind"], "log")
        self.assertEqual((self.run_dir / expected).read_bytes(), data)

    def test_artifact_outside_is_copied_not_absolute(self) -> None:
        self.init()
        outside = self.root / "outside.bin"
        outside.write_bytes(b"outside")
        code, _out, err = run_cli(
            "artifact", "--dir", str(self.run_dir), "--path", str(outside)
        )
        self.assertEqual(code, 0, err)
        entry = load_json(self.record_path)["artifacts"][0]
        self.assertEqual(entry["source"], "../outside.bin")
        self.assertFalse(Path(entry["source"]).is_absolute())
        self.assertFalse(Path(entry["path"]).is_absolute())
        self.assertTrue(entry["portable"])
        self.assertFalse(entry["external"])
        copied = self.run_dir / entry["path"]
        self.assertEqual(copied.read_bytes(), b"outside")
        self.assertEqual(entry["sha256"], sha256_bytes(b"outside"))

    def test_external_artifact_is_unverified_and_never_absolute(self) -> None:
        self.init()
        outside = self.root / "outside.bin"
        outside.write_bytes(b"outside")
        code, _out, err = run_cli(
            "artifact",
            "--dir",
            str(self.run_dir),
            "--path",
            str(outside),
            "--external",
        )
        self.assertEqual(code, 0, err)
        entry = load_json(self.record_path)["artifacts"][0]
        self.assertIsNone(entry["path"])
        self.assertEqual(entry["source"], "../outside.bin")
        self.assertFalse(Path(entry["source"]).is_absolute())
        self.assertFalse(entry["portable"])
        self.assertTrue(entry["external"])
        self.assertEqual(entry["sha256"], sha256_bytes(b"outside"))
        self.finish()
        self.export()
        record_text = self.record_path.read_text(encoding="utf-8")
        manifest_text = self.manifest_path.read_text(encoding="utf-8")
        self.assertNotIn(str(self.root), record_text)
        self.assertNotIn(str(self.root), manifest_text)
        code, out, _err = run_cli("verify", "--dir", str(self.run_dir))
        self.assertEqual(code, 1)
        self.assertIn("EXTERNAL", out)
        self.assertIn("UNVERIFIED", out)
        code, out, _err = run_cli("verify", "--dir", str(self.run_dir), "--allow-external")
        self.assertEqual(code, 0, out)
        self.assertIn("PASS", out)
        self.assertIn("EXTERNAL: 1 reference(s)", out)

    # -- finish / export ---------------------------------------------

    def test_finish_sets_outcome_and_limitations(self) -> None:
        self.init()
        self.finish()
        record = load_json(self.record_path)
        self.assertEqual(record["outcome"], "delivered")
        self.assertEqual(record["limitations"], ["one host only", "no live provider run"])

    def test_finish_rejects_empty_limitation(self) -> None:
        self.init()
        code, _out, _err = run_cli(
            "finish",
            "--dir",
            str(self.run_dir),
            "--outcome",
            "stopped",
            "--limitation",
            "   ",
        )
        self.assertEqual(code, 1)

    def test_export_writes_record_and_manifest(self) -> None:
        self.export_full()
        record_bytes = self.record_path.read_bytes()
        record = json.loads(record_bytes.decode("utf-8"))
        manifest = load_json(self.manifest_path)
        self.assertEqual(manifest["schema"], MANIFEST_SCHEMA)
        self.assertEqual(manifest["record"], "aegis-run.json")
        self.assertEqual(manifest["record_sha256"], sha256_bytes(record_bytes))
        self.assertEqual(
            manifest["artifacts"],
            [
                {field: entry[field] for field in MANIFEST_FIELDS}
                for entry in record["artifacts"]
            ],
        )
        self.assertEqual(record["outcome"], "delivered")

    def test_export_requires_finish(self) -> None:
        self.init()
        code, _out, _err = run_cli("export", "--dir", str(self.run_dir))
        self.assertEqual(code, 1)
        self.assertFalse(self.manifest_path.exists())

    # -- verify -------------------------------------------------------

    def test_verify_passes_and_prints_scope(self) -> None:
        self.export_full()
        code, out, _err = run_cli("verify", "--dir", str(self.run_dir))
        self.assertEqual(code, 0, out)
        self.assertTrue(out.startswith("PASS"))
        self.assertIn("VERIFIED: record structure and copied artifact hashes only.", out)
        self.assertIn("NOT PROVEN:", out)
        self.assertIn("universal support", out)

    def test_verify_fails_on_one_byte_artifact_tamper(self) -> None:
        self.export_full()
        copied = self.copied_path("evidence/report.txt")
        copied.write_bytes(copied.read_bytes() + b"!")
        code, out, _err = run_cli("verify", "--dir", str(self.run_dir))
        self.assertEqual(code, 1)
        self.assertIn("FAIL", out)
        self.assertIn("sha256 mismatch", out)

    def test_verify_fails_on_missing_artifact(self) -> None:
        self.export_full()
        self.copied_path("evidence/report.txt").unlink()
        code, out, _err = run_cli("verify", "--dir", str(self.run_dir))
        self.assertEqual(code, 1)
        self.assertIn("artifact missing", out)

    def test_verify_fails_on_missing_manifest(self) -> None:
        self.export_full()
        self.manifest_path.unlink()
        code, out, _err = run_cli("verify", "--dir", str(self.run_dir))
        self.assertEqual(code, 1)
        self.assertIn("missing manifest", out)

    def test_verify_fails_on_missing_required_field(self) -> None:
        self.export_full()
        self.rewrite(lambda record: record.pop("app"))
        code, out, _err = run_cli("verify", "--dir", str(self.run_dir))
        self.assertEqual(code, 1)
        self.assertIn("missing required field: app", out)

    def test_verify_fails_on_empty_limitations(self) -> None:
        self.export_full()
        self.rewrite(lambda record: record.update(limitations=[]))
        code, out, _err = run_cli("verify", "--dir", str(self.run_dir))
        self.assertEqual(code, 1)
        self.assertIn("limitations", out)

    def test_verify_fails_on_record_hash_mismatch(self) -> None:
        self.export_full()
        manifest = load_json(self.manifest_path)
        manifest["record_sha256"] = "0" * 64
        self.manifest_path.write_text(
            json.dumps(manifest, sort_keys=True, indent=2) + "\n", encoding="utf-8"
        )
        code, out, _err = run_cli("verify", "--dir", str(self.run_dir))
        self.assertEqual(code, 1)
        self.assertIn("record_sha256 mismatch", out)

    def test_verify_rejects_traversal_path(self) -> None:
        self.export_full()
        self.rewrite(lambda record: record["artifacts"][0].update(path="../outside.txt"))
        code, out, _err = run_cli("verify", "--dir", str(self.run_dir))
        self.assertEqual(code, 1)
        self.assertIn("escapes the run directory", out)

    def test_verify_rejects_absolute_path(self) -> None:
        self.export_full()
        absolute = str((self.root / "outside.txt").resolve())
        self.rewrite(lambda record: record["artifacts"][0].update(path=absolute))
        code, out, _err = run_cli("verify", "--dir", str(self.run_dir))
        self.assertEqual(code, 1)
        self.assertIn("must not be absolute", out)

    def test_verify_rejects_symlink_escape(self) -> None:
        self.export_full()
        outside = self.root / "outside.txt"
        outside.write_bytes(b"outside")
        link = self.run_dir / "link.txt"
        try:
            os.symlink(outside, link)
        except (OSError, NotImplementedError):
            self.skipTest("symbolic links unavailable on this host")
        self.rewrite(lambda record: record["artifacts"][0].update(path="link.txt"))
        code, out, _err = run_cli("verify", "--dir", str(self.run_dir))
        self.assertEqual(code, 1)
        self.assertIn("symbolic link", out)

    # -- schema enforcement (D3) -------------------------------------

    def test_schema_missing_fails_verify_and_export(self) -> None:
        self.export_full()
        missing = self.root / "missing-schema.json"
        with mock.patch.object(cli, "SCHEMA_PATH", missing):
            code, out, _err = run_cli("verify", "--dir", str(self.run_dir))
            self.assertEqual(code, 1)
            self.assertIn("SCHEMA_MISSING", out)
            code, _out, err = run_cli("export", "--dir", str(self.run_dir))
            self.assertEqual(code, 1)
            self.assertIn("SCHEMA_MISSING", err)

    def test_verify_rejects_unknown_root_property(self) -> None:
        self.export_full()
        self.rewrite(lambda record: record.update(unexpected=True))
        code, out, _err = run_cli("verify", "--dir", str(self.run_dir))
        self.assertEqual(code, 1)
        self.assertIn("unexpected property: unexpected", out)

    def test_verify_rejects_bad_created_at(self) -> None:
        self.export_full()
        self.rewrite(lambda record: record.update(created_at="2026-11-21 23:00:00"))
        code, out, _err = run_cli("verify", "--dir", str(self.run_dir))
        self.assertEqual(code, 1)
        self.assertIn("created_at", out)
        self.assertIn("RFC3339", out)

    def test_verify_rejects_bogus_event_timestamp(self) -> None:
        self.export_full()
        self.rewrite(lambda record: record["events"][0].update(ts="yesterday"))
        code, out, _err = run_cli("verify", "--dir", str(self.run_dir))
        self.assertEqual(code, 1)
        self.assertIn("events/0/ts", out)
        self.assertIn("RFC3339", out)

    def test_verify_rejects_numeric_event_note(self) -> None:
        self.export_full()
        self.rewrite(lambda record: record["events"][0].update(note=42))
        code, out, _err = run_cli("verify", "--dir", str(self.run_dir))
        self.assertEqual(code, 1)
        self.assertIn("events/0/note", out)
        self.assertIn("must be of type", out)

    def test_verify_rejects_missing_artifact_kind(self) -> None:
        self.export_full()
        self.rewrite(lambda record: record["artifacts"][0].pop("kind"))
        code, out, _err = run_cli("verify", "--dir", str(self.run_dir))
        self.assertEqual(code, 1)
        self.assertIn("missing required field: artifacts/0/kind", out)

    def test_verify_rejects_null_path_when_not_external(self) -> None:
        self.export_full()
        self.rewrite(lambda record: record["artifacts"][0].update(path=None))
        code, out, _err = run_cli("verify", "--dir", str(self.run_dir))
        self.assertEqual(code, 1)
        self.assertIn("artifacts/0/path", out)
        self.assertIn("external is false", out)

    def test_verify_rejects_bad_sha256(self) -> None:
        self.export_full()
        self.rewrite(lambda record: record["artifacts"][0].update(sha256="not-a-sha"))
        code, out, _err = run_cli("verify", "--dir", str(self.run_dir))
        self.assertEqual(code, 1)
        self.assertIn("artifacts/0/sha256", out)
        self.assertIn("pattern", out)

    def test_verify_rejects_unknown_event_property(self) -> None:
        self.export_full()
        self.rewrite(lambda record: record["events"][0].update(extra="x"))
        code, out, _err = run_cli("verify", "--dir", str(self.run_dir))
        self.assertEqual(code, 1)
        self.assertIn("unexpected property: events/0/extra", out)

    def test_export_rejects_empty_limitations(self) -> None:
        self.export_full()
        self.rewrite(lambda record: record.update(limitations=[]))
        code, _out, err = run_cli("export", "--dir", str(self.run_dir))
        self.assertEqual(code, 1)
        self.assertIn("limitations", err)

    def test_schema_kind_enum_matches_cli(self) -> None:
        schema = json.loads(cli.SCHEMA_PATH.read_text(encoding="utf-8"))
        enum = schema["$defs"]["artifact"]["properties"]["kind"]["enum"]
        self.assertEqual(set(enum), set(cli.ARTIFACT_KINDS) | {None})

    # -- example ------------------------------------------------------

    def test_example_run_verifies(self) -> None:
        self.assertTrue((EXAMPLE_DIR / "aegis-run.json").is_file())
        self.assertTrue((EXAMPLE_DIR / "manifest.json").is_file())
        self.assertTrue((EXAMPLE_DIR / "VERIFY.txt").is_file())
        code, out, _err = run_cli("verify", "--dir", str(EXAMPLE_DIR))
        self.assertEqual(code, 0, out)
        self.assertIn("PASS", out)


if __name__ == "__main__":
    unittest.main(verbosity=2)
