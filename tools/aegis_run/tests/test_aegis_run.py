"""Tests for Aegis Run Record v1 (standard-library unittest)."""

from __future__ import annotations

import contextlib
import hashlib
import io
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time
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
        code, out, err = run_cli(
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
        self.assertIn("refusing to overwrite", err)
        self.assertNotIn("Traceback", out + err)

    def test_init_rejects_record_file_as_directory_cleanly(self) -> None:
        self.init()
        code, out, err = run_cli(
            "init",
            "--dir",
            str(self.record_path),
            "--app",
            "other",
            "--aegis-commit",
            COMMIT,
            "--host",
            "host-b",
        )
        self.assertEqual(code, 1)
        self.assertIn("not a directory", err)
        self.assertNotIn("Traceback", out + err)

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
        self.add_event()
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

    def test_export_rejects_empty_events(self) -> None:
        self.init()
        self.finish()
        code, _out, err = run_cli("export", "--dir", str(self.run_dir))
        self.assertEqual(code, 1)
        self.assertIn("events", err)
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

    def test_verify_rejects_empty_events(self) -> None:
        self.export_full()
        self.rewrite(lambda record: record.update(events=[]))
        (self.run_dir / "events.jsonl").write_text("", encoding="utf-8")
        code, out, _err = run_cli("verify", "--dir", str(self.run_dir))
        self.assertEqual(code, 1)
        self.assertIn("events", out)

    def test_verify_rejects_missing_events(self) -> None:
        self.export_full()
        self.rewrite(lambda record: record.pop("events"))
        code, out, _err = run_cli("verify", "--dir", str(self.run_dir))
        self.assertEqual(code, 1)
        self.assertIn("events", out)

    def test_verify_handles_non_utf8_event_log(self) -> None:
        self.export_full()
        (self.run_dir / "events.jsonl").write_bytes(b"\xff\xfe\x00")
        code, out, err = run_cli("verify", "--dir", str(self.run_dir))
        self.assertEqual(code, 1)
        self.assertIn("not valid UTF-8", out)
        self.assertNotIn("Traceback", out + err)

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


# -- project-state sync, watch and hook --------------------------------

STATE_SECTION = (
    "## State snapshots (append-only) \u2014 the LATEST row is the current state\n"
    "\n"
    "| ID | Date | Current stage (plain language) | Next recommended action |\n"
    "|----|------|--------------------------------|-------------------------|\n"
)

SNAPSHOT_ROWS = [
    ("SS-001", "2026-11-21", "Defining the product", "Approve the first-release scope."),
    (
        "SS-002",
        "2026-11-22",
        "Design: how it will be built",
        "Answer the reminder-link question.",
    ),
]

THIRD_ROW = (
    "SS-003",
    "2026-11-23",
    "Building the first version",
    "Run the acceptance tests.",
)


def find_posix_sh() -> str | None:
    """Locate a POSIX sh so a written hook can actually be executed."""
    candidate = shutil.which("sh")
    if candidate:
        return candidate
    git = shutil.which("git")
    if git:
        root = Path(git).resolve().parent.parent
        for relative in ("bin/sh.exe", "usr/bin/sh.exe", "bin/sh", "usr/bin/sh"):
            if (root / relative).is_file():
                return str(root / relative)
    return None


def state_document(rows) -> str:
    body = "".join("| %s | %s | %s | %s |\n" % row for row in rows)
    return (
        "# Project State \u2014 demo\n\n"
        + STATE_SECTION
        + body
        + "\n## Decision log (append-only)\n"
        "\n| ID | Date |\n| --- | --- |\n| PS-001 | 2026-03-03 |\n"
    )


class ProjectStateSyncTest(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.root = Path(self._tmp.name)
        self.run_dir = self.root / "run"
        self.record_path = self.run_dir / "aegis-run.json"
        self.events_path = self.run_dir / "events.jsonl"
        self.state_path = self.root / "project-state.md"
        self._stamp = 1_000_000.0

    def init(self) -> None:
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
        )
        self.assertEqual(code, 0, err)

    def write_state(self, rows) -> None:
        self.state_path.write_text(state_document(rows), encoding="utf-8")
        self._stamp += 10.0
        os.utime(self.state_path, (self._stamp, self._stamp))

    def events(self) -> list:
        return load_json(self.record_path)["events"]

    def log_lines(self) -> list:
        return [
            json.loads(line)
            for line in self.events_path.read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]

    def sync(self, *extra: str) -> tuple[int, str, str]:
        return run_cli(
            "sync",
            "--dir",
            str(self.run_dir),
            "--project-state",
            str(self.state_path),
            *extra,
        )

    # -- sync ---------------------------------------------------------

    def test_first_sync_marks_history_as_note_and_latest_as_stage(self) -> None:
        self.init()
        self.write_state(SNAPSHOT_ROWS)
        code, out, err = self.sync()
        self.assertEqual(code, 0, err)
        events = self.events()
        self.assertEqual(len(events), 2)
        self.assertEqual([event["source_id"] for event in events], ["SS-001", "SS-002"])
        self.assertEqual([event["type"] for event in events], ["note", "stage"])
        for event, row in zip(events, SNAPSHOT_ROWS):
            self.assertEqual(
                set(event),
                {"ts", "type", "stage", "status", "note", "actor", "source_id"},
            )
            self.assertEqual(event["stage"], row[2])
            self.assertEqual(event["status"], "started")
            self.assertEqual(event["actor"], "project-state-sync")
            self.assertTrue(event["ts"].endswith("Z"))
        self.assertEqual(
            events[0]["note"],
            "historical snapshot SS-001 imported from project-state;"
            " not observed live",
        )
        self.assertEqual(
            events[1]["note"], "Imported from project-state; next: %s" % SNAPSHOT_ROWS[1][3]
        )
        self.assertEqual(self.log_lines(), events)
        self.assertEqual({event["status"] for event in events}, {"started"})
        self.assertIn("sync: 2 new", out)

    def test_single_row_first_sync_is_a_stage_event(self) -> None:
        self.init()
        self.write_state([SNAPSHOT_ROWS[1]])
        code, _out, err = self.sync()
        self.assertEqual(code, 0, err)
        self.assertEqual([event["type"] for event in self.events()], ["stage"])

    def test_sync_never_emits_a_passed_status(self) -> None:
        self.init()
        self.write_state(SNAPSHOT_ROWS)
        self.assertEqual(self.sync()[0], 0)
        self.write_state(SNAPSHOT_ROWS + [THIRD_ROW])
        self.assertEqual(self.sync()[0], 0)
        self.assertEqual({event["status"] for event in self.events()}, {"started"})
        self.assertNotIn('"passed"', self.record_path.read_text(encoding="utf-8"))

    def test_sync_imports_a_duplicate_source_id_once(self) -> None:
        self.init()
        self.write_state([SNAPSHOT_ROWS[0], SNAPSHOT_ROWS[0]])
        code, out, err = self.sync()
        self.assertEqual(code, 0, err)
        self.assertEqual(len(self.events()), 1)
        self.assertEqual(self.events()[0]["source_id"], "SS-001")
        self.assertIn("sync: 1 new, 1 already imported", out)

    def test_sync_ignores_rows_in_other_tables(self) -> None:
        self.init()
        self.write_state([SNAPSHOT_ROWS[1]])
        code, _out, err = self.sync()
        self.assertEqual(code, 0, err)
        self.assertEqual([event["source_id"] for event in self.events()], ["SS-002"])

    def test_sync_rejects_ragged_columns(self) -> None:
        self.init()
        self.write_raw(
            "# Project State\n\n"
            + STATE_SECTION
            + "| SS-001 | 2026-11-21 | Design | Next action. | extra |\n"
        )
        code, out, err = self.sync()
        self.assertEqual(code, 1)
        self.assertIn("expected 4 columns", err)
        self.assertNotIn("Traceback", out + err)
        self.assertEqual(self.events(), [])

    def test_sync_second_run_reports_zero_new(self) -> None:
        self.init()
        self.write_state(SNAPSHOT_ROWS)
        self.assertEqual(self.sync()[0], 0)
        code, out, err = self.sync()
        self.assertEqual(code, 0, err)
        self.assertEqual(len(self.events()), 2)
        self.assertEqual(len(self.log_lines()), 2)
        self.assertIn("sync: 0 new, 2 already imported", out)

    def test_sync_appends_exactly_one_for_a_third_snapshot(self) -> None:
        self.init()
        self.write_state(SNAPSHOT_ROWS)
        self.assertEqual(self.sync()[0], 0)
        self.write_state(SNAPSHOT_ROWS + [THIRD_ROW])
        code, out, err = self.sync()
        self.assertEqual(code, 0, err)
        events = self.events()
        self.assertEqual(len(events), 3)
        self.assertEqual(events[-1]["source_id"], "SS-003")
        self.assertEqual(events[-1]["stage"], THIRD_ROW[2])
        self.assertIn("sync: 1 new, 2 already imported", out)
        self.assertEqual(self.log_lines(), events)

    def test_sync_dry_run_writes_nothing(self) -> None:
        self.init()
        self.write_state(SNAPSHOT_ROWS)
        record_before = self.record_path.read_bytes()
        log_before = self.events_path.read_bytes()
        code, out, err = self.sync("--dry-run")
        self.assertEqual(code, 0, err)
        self.assertIn("would append SS-001", out)
        self.assertIn("would append SS-002", out)
        self.assertIn("0 written", out)
        self.assertEqual(self.record_path.read_bytes(), record_before)
        self.assertEqual(self.events_path.read_bytes(), log_before)
        self.assertEqual(self.events(), [])

    def test_sync_missing_table_exits_cleanly(self) -> None:
        self.init()
        self.state_path.write_text("# Project State\n\nNo snapshots here.\n", encoding="utf-8")
        code, out, err = self.sync()
        self.assertEqual(code, 1)
        self.assertIn("State snapshots", err)
        self.assertNotIn("Traceback", out + err)
        self.assertEqual(self.events(), [])

    def test_sync_missing_file_exits_cleanly(self) -> None:
        self.init()
        code, out, err = self.sync()
        self.assertEqual(code, 1)
        self.assertIn("not found", err)
        self.assertNotIn("Traceback", out + err)
        self.assertEqual(self.events(), [])

    def write_raw(self, text: str) -> None:
        self.state_path.write_text(text, encoding="utf-8")
        self._stamp += 10.0
        os.utime(self.state_path, (self._stamp, self._stamp))

    def test_sync_malformed_rows_exit_cleanly_and_write_nothing(self) -> None:
        self.init()
        bad_documents = [
            state_document([("SS-001", "not-a-date", "Design", "Next action.")]),
            state_document([("SS-001", "2026-11-21", "", "Next action.")]),
            state_document([("", "2026-11-21", "Design", "Next action.")]),
            "# Project State\n\n" + STATE_SECTION + "| SS-001 | 2026-11-21 | Design |\n",
        ]
        record_before = self.record_path.read_bytes()
        for document in bad_documents:
            with self.subTest(document=document):
                self.write_raw(document)
                code, out, err = self.sync()
                self.assertEqual(code, 1)
                self.assertNotIn("Traceback", out + err)
                self.assertEqual(self.record_path.read_bytes(), record_before)
                self.assertEqual(self.events_path.read_bytes(), b"")

    def test_sync_missing_header_exits_cleanly(self) -> None:
        self.init()
        self.state_path.write_text(
            "## State snapshots (append-only)\n\n| a | b |\n| --- | --- |\n| 1 | 2 |\n",
            encoding="utf-8",
        )
        code, out, err = self.sync()
        self.assertEqual(code, 1)
        self.assertIn("header", err)
        self.assertNotIn("Traceback", out + err)

    def test_sync_does_not_modify_project_state(self) -> None:
        self.init()
        self.write_state(SNAPSHOT_ROWS)
        before = self.state_path.read_bytes()
        self.assertEqual(self.sync()[0], 0)
        self.assertEqual(self.state_path.read_bytes(), before)

    def test_synced_events_export_and_verify(self) -> None:
        self.init()
        self.write_state(SNAPSHOT_ROWS)
        self.assertEqual(self.sync()[0], 0)
        code, _out, err = run_cli(
            "finish",
            "--dir",
            str(self.run_dir),
            "--outcome",
            "delivered",
            "--limitation",
            "one host only",
        )
        self.assertEqual(code, 0, err)
        code, _out, err = run_cli("export", "--dir", str(self.run_dir))
        self.assertEqual(code, 0, err)
        code, out, _err = run_cli("verify", "--dir", str(self.run_dir))
        self.assertEqual(code, 0, out)
        self.assertIn("PASS", out)

    def rewrite(self, mutate) -> None:
        record = load_json(self.record_path)
        mutate(record)
        text = json.dumps(record, sort_keys=True, indent=2, ensure_ascii=False) + "\n"
        self.record_path.write_text(text, encoding="utf-8")
        manifest_path = self.run_dir / "manifest.json"
        manifest = load_json(manifest_path)
        manifest["artifacts"] = [
            {field: item.get(field) for field in MANIFEST_FIELDS}
            for item in record["artifacts"]
        ]
        manifest["record_sha256"] = sha256_bytes(text.encode("utf-8"))
        manifest_path.write_text(
            json.dumps(manifest, sort_keys=True, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )

    def finish_and_export(self) -> None:
        code, _out, err = run_cli(
            "finish",
            "--dir",
            str(self.run_dir),
            "--outcome",
            "delivered",
            "--limitation",
            "one host only",
        )
        self.assertEqual(code, 0, err)
        code, _out, err = run_cli("export", "--dir", str(self.run_dir))
        self.assertEqual(code, 0, err)

    def test_verify_rejects_a_bad_source_id_pattern(self) -> None:
        self.init()
        self.write_state(SNAPSHOT_ROWS)
        self.assertEqual(self.sync()[0], 0)
        self.finish_and_export()
        self.rewrite(lambda record: record["events"][0].update(source_id="BAD-1"))
        code, out, _err = run_cli("verify", "--dir", str(self.run_dir))
        self.assertEqual(code, 1)
        self.assertIn("events/0/source_id", out)
        self.assertIn("pattern", out)

    def test_verify_rejects_a_null_or_empty_source_id(self) -> None:
        self.init()
        self.write_state(SNAPSHOT_ROWS)
        self.assertEqual(self.sync()[0], 0)
        self.finish_and_export()
        for bad_value in (None, ""):
            with self.subTest(bad_value=bad_value):
                self.rewrite(
                    lambda record: record["events"][0].update(source_id=bad_value)
                )
                code, out, _err = run_cli("verify", "--dir", str(self.run_dir))
                self.assertEqual(code, 1)
                self.assertIn("events/0/source_id", out)
                self.assertIn("non-empty string", out)

    def test_verify_rejects_source_id_on_a_hand_written_event(self) -> None:
        self.init()
        self.write_state(SNAPSHOT_ROWS)
        self.assertEqual(self.sync()[0], 0)
        self.finish_and_export()
        self.rewrite(lambda record: record["events"][0].update(actor="someone-else"))
        code, out, _err = run_cli("verify", "--dir", str(self.run_dir))
        self.assertEqual(code, 1)
        self.assertIn("source_id is only allowed", out)

    # -- sync locking -------------------------------------------------

    def test_sync_locks_the_run_directory(self) -> None:
        self.init()
        self.write_state(SNAPSHOT_ROWS)
        self.assertEqual(self.sync()[0], 0)
        self.assertFalse((self.run_dir / cli.LOCK_NAME).exists())

    def test_sync_reports_a_held_lock_without_writing(self) -> None:
        self.init()
        self.write_state(SNAPSHOT_ROWS)
        lock = self.run_dir / cli.LOCK_NAME
        lock.write_text("12345\n", encoding="utf-8")
        with mock.patch.object(cli, "LOCK_TIMEOUT_SECONDS", 0.2):
            code, out, err = self.sync()
        self.assertEqual(code, 1)
        self.assertIn("sync lock is held", err)
        self.assertNotIn("Traceback", out + err)
        self.assertEqual(self.events(), [])
        self.assertEqual(self.events_path.read_bytes(), b"")

    def test_sync_refuses_a_stale_lock_and_leaves_it(self) -> None:
        self.init()
        self.write_state(SNAPSHOT_ROWS)
        lock = self.run_dir / cli.LOCK_NAME
        lock.write_text("999\n", encoding="utf-8")
        old = time.time() - (cli.LOCK_STALE_SECONDS + 60)
        os.utime(lock, (old, old))
        code, out, err = self.sync()
        self.assertEqual(code, 1)
        self.assertIn("stale sync lock", err)
        self.assertIn("remove it manually if no sync is running", err)
        self.assertIn(str(Path(self.run_dir).resolve() / cli.LOCK_NAME), err)
        self.assertNotIn("Traceback", out + err)
        self.assertTrue(lock.exists())
        self.assertEqual(self.events(), [])
        self.assertEqual(self.events_path.read_bytes(), b"")

    def test_sync_rejects_an_invalid_snapshot_id_without_writing(self) -> None:
        self.init()
        record_before = self.record_path.read_bytes()
        for bad_id in ("SNAP-1", "SS-01", "ss-001", "SS-001x"):
            with self.subTest(bad_id=bad_id):
                self.write_state(
                    [(bad_id, "2026-11-21", "Design", "Next action.")]
                )
                code, out, err = self.sync()
                self.assertEqual(code, 1)
                self.assertIn("ID must match SS-", err)
                self.assertNotIn("Traceback", out + err)
                self.assertEqual(self.record_path.read_bytes(), record_before)
                self.assertEqual(self.events_path.read_bytes(), b"")

    def test_two_concurrent_sync_processes_import_one_event(self) -> None:
        self.init()
        self.write_state(SNAPSHOT_ROWS)
        self.assertEqual(self.sync()[0], 0)
        self.write_state(SNAPSHOT_ROWS + [THIRD_ROW])
        command = [
            sys.executable,
            "-B",
            "-m",
            "tools.aegis_run",
            "sync",
            "--dir",
            str(self.run_dir),
            "--project-state",
            str(self.state_path),
        ]
        processes = [
            subprocess.Popen(
                command,
                cwd=str(REPO_ROOT),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )
            for _ in range(2)
        ]
        results = []
        try:
            for process in processes:
                results.append(process.communicate(timeout=180))
        finally:
            for process in processes:
                if process.poll() is None:
                    process.kill()
        for _out, err in results:
            self.assertNotIn("Traceback", err)
        for process in processes:
            self.assertEqual(
                process.returncode,
                0,
                "a concurrent sync failed instead of finding nothing new",
            )
        events = self.events()
        self.assertEqual(len(events), 3)
        self.assertEqual(
            [event["source_id"] for event in events].count("SS-003"), 1
        )
        self.assertFalse((self.run_dir / cli.LOCK_NAME).exists())


    # -- watch --------------------------------------------------------

    def test_watch_step_syncs_only_on_change(self) -> None:
        self.init()
        self.write_state(SNAPSHOT_ROWS)
        args = cli.build_parser().parse_args(
            ["sync", "--dir", str(self.run_dir), "--project-state", str(self.state_path)]
        )
        with contextlib.redirect_stdout(io.StringIO()) as noticed:
            last, ran = cli._watch_once(args, None)
        self.assertTrue(ran)
        self.assertIn("changed:", noticed.getvalue())
        self.assertEqual(len(self.events()), 2)
        with contextlib.redirect_stdout(io.StringIO()):
            again, ran = cli._watch_once(args, last)
        self.assertFalse(ran)
        self.assertEqual(again, last)
        self.assertEqual(len(self.events()), 2)
        self.write_state(SNAPSHOT_ROWS + [THIRD_ROW])
        with contextlib.redirect_stdout(io.StringIO()):
            _current, ran = cli._watch_once(args, last)
        self.assertTrue(ran)
        self.assertEqual(len(self.events()), 3)
        self.assertEqual(self.events()[-1]["source_id"], "SS-003")

    def test_watch_interval_has_a_five_second_floor(self) -> None:
        self.assertEqual(cli.MIN_WATCH_INTERVAL, 5)
        stderr = io.StringIO()
        with contextlib.redirect_stderr(stderr):
            self.assertEqual(cli._watch_interval(1), 5.0)
        self.assertIn("minimum", stderr.getvalue())
        with contextlib.redirect_stderr(io.StringIO()):
            self.assertEqual(cli._watch_interval(30), 30.0)

    def test_watch_parser_defaults_to_30_seconds(self) -> None:
        args = cli.build_parser().parse_args(
            ["watch", "--dir", "d", "--project-state", "p"]
        )
        self.assertEqual(args.interval, 30.0)
        self.assertEqual(args.func, cli.cmd_watch)

    # -- post-commit hook ---------------------------------------------

    def make_repo(self) -> Path:
        repo = self.root / "repo"
        (repo / ".git" / "hooks").mkdir(parents=True, exist_ok=True)
        return repo

    def hook_path(self, repo: Path) -> Path:
        return repo / ".git" / "hooks" / "post-commit"

    def install(self, repo: Path, *extra: str) -> tuple[int, str, str]:
        return run_cli(
            "install-hook",
            "--repo",
            str(repo),
            "--dir",
            str(self.run_dir),
            "--project-state",
            str(self.state_path),
            "--aegis-path",
            str(REPO_ROOT),
            *extra,
        )

    def test_install_hook_writes_marker_and_sync_command(self) -> None:
        self.init()
        self.write_state(SNAPSHOT_ROWS)
        repo = self.make_repo()
        code, out, err = self.install(repo)
        self.assertEqual(code, 0, err)
        hook = self.hook_path(repo)
        text = hook.read_text(encoding="utf-8")
        self.assertTrue(text.startswith("#!/bin/sh"))
        self.assertIn(cli.HOOK_MARKER, text)
        self.assertIn("python -P -m tools.aegis_run sync", text)
        self.assertIn(
            "cd '%s' || exit 0" % Path(REPO_ROOT).as_posix(), text
        )
        self.assertIn(Path(self.run_dir).resolve().as_posix(), text)
        self.assertIn(Path(self.state_path).resolve().as_posix(), text)
        self.assertIn("PYTHONPATH=", text)
        self.assertIn("exit 0", text)
        self.assertIn("installed post-commit hook", out)

    def test_install_hook_refuses_foreign_hook_without_force(self) -> None:
        self.init()
        self.write_state(SNAPSHOT_ROWS)
        repo = self.make_repo()
        hook = self.hook_path(repo)
        original = "#!/bin/sh\necho mine\n"
        hook.write_text(original, encoding="utf-8")
        code, out, err = self.install(repo)
        self.assertEqual(code, 1)
        self.assertIn("refusing", err)
        self.assertNotIn("Traceback", out + err)
        self.assertEqual(hook.read_text(encoding="utf-8"), original)

    def test_install_hook_force_backs_up_foreign_hook(self) -> None:
        self.init()
        self.write_state(SNAPSHOT_ROWS)
        repo = self.make_repo()
        hook = self.hook_path(repo)
        original = "#!/bin/sh\necho mine\n"
        hook.write_text(original, encoding="utf-8")
        code, out, err = self.install(repo, "--force")
        self.assertEqual(code, 0, err)
        backups = sorted(hook.parent.glob("post-commit.bak-*"))
        self.assertEqual(len(backups), 1)
        self.assertEqual(backups[0].read_text(encoding="utf-8"), original)
        self.assertIn(cli.HOOK_MARKER, hook.read_text(encoding="utf-8"))
        self.assertIn("backed up", out)

    def test_uninstall_hook_removes_only_ours(self) -> None:
        self.init()
        self.write_state(SNAPSHOT_ROWS)
        repo = self.make_repo()
        hook = self.hook_path(repo)
        code, _out, err = run_cli("uninstall-hook", "--repo", str(repo))
        self.assertEqual(code, 1)
        self.assertIn("no post-commit hook installed", err)
        original = "#!/bin/sh\necho mine\n"
        hook.write_text(original, encoding="utf-8")
        code, _out, err = run_cli("uninstall-hook", "--repo", str(repo))
        self.assertEqual(code, 1)
        self.assertIn("refusing", err)
        self.assertEqual(hook.read_text(encoding="utf-8"), original)
        hook.unlink()
        self.assertEqual(self.install(repo)[0], 0)
        code, out, err = run_cli("uninstall-hook", "--repo", str(repo))
        self.assertEqual(code, 0, err)
        self.assertIn("removed post-commit hook", out)
        self.assertFalse(hook.exists())
        self.assertEqual(len(list(hook.parent.glob("post-commit.bak-*"))), 0)

    def test_install_and_uninstall_require_a_git_directory(self) -> None:
        self.init()
        self.write_state(SNAPSHOT_ROWS)
        plain = self.root / "plain"
        plain.mkdir()
        code, out, err = self.install(plain)
        self.assertEqual(code, 1)
        self.assertIn("not a git repository", err)
        self.assertNotIn("Traceback", out + err)
        code, out, err = run_cli("uninstall-hook", "--repo", str(plain))
        self.assertEqual(code, 1)
        self.assertIn("not a git repository", err)
        self.assertNotIn("Traceback", out + err)

    def test_hook_ignores_a_repo_local_shadow_tools_package(self) -> None:
        sh = find_posix_sh()
        if sh is None:
            self.skipTest("POSIX sh unavailable on this host")
        self.init()
        self.write_state(SNAPSHOT_ROWS)
        repo = self.make_repo()
        shadow = repo / "tools" / "aegis_run"
        shadow.mkdir(parents=True)
        (repo / "tools" / "__init__.py").write_text("", encoding="utf-8")
        (shadow / "__init__.py").write_text("", encoding="utf-8")
        (shadow / "__main__.py").write_text(
            "print('SHADOW-EXECUTED')\n", encoding="utf-8"
        )
        code, _out, err = self.install(repo)
        self.assertEqual(code, 0, err)
        environment = dict(os.environ)
        environment.pop("PYTHONPATH", None)
        environment["PATH"] = (
            str(Path(sys.executable).parent) + os.pathsep + environment.get("PATH", "")
        )
        result = subprocess.run(
            [sh, str(self.hook_path(repo))],
            cwd=str(repo),
            env=environment,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=180,
        )
        combined = result.stdout + result.stderr
        self.assertEqual(result.returncode, 0, combined)
        self.assertNotIn("SHADOW-EXECUTED", combined)
        self.assertEqual(len(self.events()), 2)
        self.assertEqual(
            [event["source_id"] for event in self.events()], ["SS-001", "SS-002"]
        )

    def test_hook_script_carries_no_network_commands(self) -> None:
        self.init()
        self.write_state(SNAPSHOT_ROWS)
        repo = self.make_repo()
        self.assertEqual(self.install(repo)[0], 0)
        text = self.hook_path(repo).read_text(encoding="utf-8")
        for token in ("curl", "wget", "http://", "https://"):
            self.assertNotIn(token, text)
        module = Path(cli.__file__).read_text(encoding="utf-8")
        for token in ("urllib", "import requests", "import socket"):
            self.assertNotIn(token, module)


if __name__ == "__main__":
    unittest.main(verbosity=2)
