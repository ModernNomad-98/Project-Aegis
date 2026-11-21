#!/usr/bin/env python3
"""Tests for scripts/build-review-packet.py.

The packet builder is offline and deterministic; these tests invoke its main()
in-process. Each test gets a throwaway directory created with a plain
Path.mkdir under the system temporary root, because tempfile.mkdtemp's 0o700
mode can be denied by the ACL on some sandboxed Windows hosts; when that
directory cannot be created the test skips with the reason printed.

Run:
    python -B -P scripts/tests/test_build_review_packet.py
"""
from __future__ import annotations

import contextlib
import hashlib
import importlib.util
import io
import json
import os
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
SCRIPT_PATH = REPO_ROOT / "scripts" / "build-review-packet.py"
BOUND_FIELDS_PATH = REPO_ROOT / "scripts" / "ci" / "bound_fields_hash.py"

HEAD = "0123456789abcdef0123456789abcdef01234567"
BASE = "f37fd8f43b1a974d8700014246c0466a837f88c9"

BODY_TEXT = (
    "# Review packet fixture\n"
    "\n"
    "Intro prose.\n"
    "\n"
    "<!-- bound-field: witness -->\n"
    "Witness: local test run, no network.\n"
    "<!-- bound-field: end -->\n"
    "\n"
    "<!-- bound-field: skills -->\n"
    "| Skill | How applied |\n"
    "<!-- bound-field: end -->\n"
    "\n"
    "<!-- bound-field: security -->\n"
    "No new attack surface.\n"
    "<!-- bound-field: end -->\n"
)
BODY_BYTES = BODY_TEXT.encode("utf-8")


def load_module(name, path):
    """Load a hyphenated script by path; it is not an importable name."""
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


PACKET = load_module("build_review_packet_under_test", SCRIPT_PATH)
BOUND = load_module("bound_fields_hash_under_test", BOUND_FIELDS_PATH)


def skip(reason):
    """Print the reason, then raise unittest's skip signal."""
    print(f"SKIP: {reason}", file=sys.stderr)
    raise unittest.SkipTest(reason)


def make_temp_root():
    """Create a unique writable directory under the system temp root."""
    base = Path(tempfile.gettempdir())
    for index in range(1000):
        candidate = base / f"aegis-review-packet-{os.getpid()}-{index}"
        try:
            candidate.mkdir()
        except FileExistsError:
            continue
        return candidate.resolve()
    raise RuntimeError("could not create a unique temporary directory")


def entry(name, conclusion, status="completed"):
    """One check-run entry in the shape the builder consumes."""
    return {"name": name, "status": status, "conclusion": conclusion}


class BuildReviewPacketTests(unittest.TestCase):
    def setUp(self):
        try:
            self.tmp = make_temp_root()
        except OSError as error:
            skip(f"temporary directory could not be created: {error}")
        self.addCleanup(shutil.rmtree, self.tmp, ignore_errors=True)
        self.body_path = self.tmp / "body.md"
        self.body_path.write_bytes(BODY_BYTES)
        self.checks_path = self.write_checks(
            [entry("gate-guard", "success"), entry("validate-skills", "success")]
        )
        self.out_path = self.tmp / "packet.json"

    def write_checks(self, payload, name="checks.json"):
        path = self.tmp / name
        path.write_text(
            json.dumps(payload, indent=2) + "\n", encoding="utf-8", newline=""
        )
        return path

    def run_packet(self, *, body=None, head=None, base=None, checks=None,
                   out=None, pr=None, required=None, force=False,
                   include_checks=True):
        argv = [
            "--body", str(body if body is not None else self.body_path),
            "--head", head if head is not None else HEAD,
            "--base", base if base is not None else BASE,
            "--out", str(out if out is not None else self.out_path),
        ]
        if include_checks:
            argv.extend(
                ["--checks", str(checks if checks is not None else self.checks_path)]
            )
        if pr is not None:
            argv.extend(["--pr", str(pr)])
        for name in required or []:
            argv.extend(["--required", name])
        if force:
            argv.append("--force")
        stderr = io.StringIO()
        with contextlib.redirect_stderr(stderr):
            code = PACKET.main(argv)
        return code, stderr.getvalue()

    def assert_error(self, code, stderr):
        self.assertEqual(2, code, stderr)
        lines = stderr.strip().splitlines()
        self.assertEqual(1, len(lines), stderr)
        self.assertIn("ERROR", lines[0])

    def build_packet(self, **kwargs):
        code, stderr = self.run_packet(**kwargs)
        self.assertEqual(0, code, stderr)
        out = kwargs.get("out") or self.out_path
        return json.loads(Path(out).read_text(encoding="utf-8"))

    def test_valid_packet_with_success_skipped_and_cancelled(self):
        self.write_checks([
            entry("gate-guard", "success"),
            entry("validate-skills", "success"),
            entry("docs-lint", "skipped"),
            entry("security", "cancelled"),
            entry("style", "neutral"),
        ])
        packet = self.build_packet()
        self.assertEqual("aegis.review-packet/1", packet["schema"])
        self.assertIsNone(packet["pr"])
        self.assertEqual(HEAD, packet["head"])
        self.assertEqual(BASE, packet["base"])
        checks = packet["checks"]
        self.assertEqual(
            ["gate-guard", "validate-skills"],
            [record["name"] for record in checks["required"]],
        )
        self.assertTrue(all(r["present"] and r["success"]
                            for r in checks["required"]))
        self.assertTrue(checks["all_required_success"])
        self.assertEqual([], checks["failures"])
        self.assertEqual(["docs-lint"], checks["skipped"])
        self.assertEqual(["security"], checks["cancelled"])
        by_name = {item["name"]: item for item in checks["entries"]}
        self.assertFalse(by_name["docs-lint"]["is_success"])
        self.assertFalse(by_name["security"]["is_success"])
        self.assertFalse(by_name["style"]["is_success"])

    def test_body_facts_match_hashlib_and_imported_report(self):
        packet = self.build_packet()
        body = packet["body"]
        self.assertEqual(len(BODY_BYTES), body["bytes"])
        self.assertEqual(
            BODY_BYTES.count(b"\n")
            + (0 if BODY_BYTES.endswith(b"\n") else 1),
            body["lines"],
        )
        self.assertEqual(hashlib.sha256(BODY_BYTES).hexdigest(), body["sha256"])
        expected = BOUND.report(BODY_TEXT)
        self.assertEqual(
            {key: expected[key]
             for key in ("hash16", "sha256", "method", "tool", "version")},
            body["bound_fields"],
        )

    def test_explicit_pr_and_custom_required_names(self):
        self.write_checks([entry("custom-check", "success")])
        packet = self.build_packet(pr=123, required=["custom-check"])
        self.assertEqual(123, packet["pr"])
        checks = packet["checks"]
        self.assertEqual(
            [{"name": "custom-check", "present": True, "success": True}],
            checks["required"],
        )
        self.assertTrue(checks["all_required_success"])

    def test_required_failure_sets_all_required_false(self):
        self.write_checks([
            entry("gate-guard", "success"),
            entry("validate-skills", "failure"),
        ])
        checks = self.build_packet()["checks"]
        self.assertFalse(checks["all_required_success"])
        records = {record["name"]: record for record in checks["required"]}
        self.assertTrue(records["gate-guard"]["success"])
        self.assertFalse(records["validate-skills"]["success"])
        self.assertEqual(["validate-skills"], checks["failures"])

    def test_missing_required_sets_all_required_false(self):
        self.write_checks([entry("gate-guard", "success")])
        checks = self.build_packet()["checks"]
        self.assertFalse(checks["all_required_success"])
        records = {record["name"]: record for record in checks["required"]}
        self.assertFalse(records["validate-skills"]["present"])
        self.assertFalse(records["validate-skills"]["success"])

    def test_duplicate_name_with_one_failure_sets_all_required_false(self):
        self.write_checks([
            entry("gate-guard", "success"),
            entry("gate-guard", "failure"),
            entry("validate-skills", "success"),
        ])
        checks = self.build_packet()["checks"]
        self.assertEqual(3, len(checks["entries"]))
        self.assertFalse(checks["all_required_success"])
        records = {record["name"]: record for record in checks["required"]}
        self.assertTrue(records["gate-guard"]["present"])
        self.assertFalse(records["gate-guard"]["success"])
        self.assertEqual(["gate-guard"], checks["failures"])

    def test_duplicate_success_entries_keep_the_name_successful(self):
        self.write_checks([
            entry("gate-guard", "success"),
            entry("gate-guard", "success"),
            entry("validate-skills", "success"),
        ])
        checks = self.build_packet()["checks"]
        self.assertEqual(3, len(checks["entries"]))
        self.assertTrue(checks["all_required_success"])
        records = {record["name"]: record for record in checks["required"]}
        self.assertTrue(records["gate-guard"]["success"])

    def test_startup_failure_and_pending_are_not_success(self):
        self.write_checks([
            entry("gate-guard", "startup_failure"),
            entry("validate-skills", None, status="queued"),
        ])
        checks = self.build_packet()["checks"]
        self.assertFalse(checks["all_required_success"])
        by_name = {item["name"]: item for item in checks["entries"]}
        self.assertTrue(by_name["gate-guard"]["is_failure"])
        self.assertFalse(by_name["gate-guard"]["is_success"])
        self.assertEqual("pending", by_name["validate-skills"]["conclusion"])
        self.assertFalse(by_name["validate-skills"]["is_success"])
        self.assertEqual(["gate-guard"], checks["failures"])

    def test_skipped_and_cancelled_required_names_are_not_success(self):
        self.write_checks([
            entry("gate-guard", "skipped"),
            entry("validate-skills", "cancelled"),
        ])
        checks = self.build_packet()["checks"]
        self.assertFalse(checks["all_required_success"])
        self.assertEqual(["gate-guard"], checks["skipped"])
        self.assertEqual(["validate-skills"], checks["cancelled"])
        self.assertTrue(all(not item["is_success"] for item in checks["entries"]))

    def test_gh_shaped_check_runs_object_is_accepted(self):
        self.write_checks({
            "total_count": 2,
            "check_runs": [
                entry("gate-guard", "success"),
                entry("validate-skills", "success"),
            ],
        })
        checks = self.build_packet()["checks"]
        self.assertEqual(2, len(checks["entries"]))
        self.assertTrue(checks["all_required_success"])

    def test_invalid_head_exits_2(self):
        for value in ("A" * 40, "a" * 39, "g" * 40, "a" * 41):
            with self.subTest(head=value):
                code, stderr = self.run_packet(head=value)
                self.assert_error(code, stderr)
                self.assertIn("--head", stderr)

    def test_invalid_base_exits_2(self):
        for value in ("B" * 40, "b" * 39):
            with self.subTest(base=value):
                code, stderr = self.run_packet(base=value)
                self.assert_error(code, stderr)
                self.assertIn("--base", stderr)

    def test_invalid_pr_exits_2(self):
        for value in (0, -1, "abc", "1.5"):
            with self.subTest(pr=value):
                code, stderr = self.run_packet(pr=value)
                self.assert_error(code, stderr)
                self.assertIn("--pr", stderr)

    def test_invalid_json_exits_2(self):
        (self.tmp / "broken.json").write_text(
            "{not json\n", encoding="utf-8", newline=""
        )
        code, stderr = self.run_packet(checks=self.tmp / "broken.json")
        self.assert_error(code, stderr)
        self.assertIn("JSON", stderr)

    def test_malformed_checks_entries_exit_2(self):
        payloads = [
            [{"status": "completed", "conclusion": "success"}],
            [{"name": 3, "status": "completed", "conclusion": "success"}],
            [{"name": "gate-guard", "status": "completed"}],
            [{"name": "gate-guard", "status": "completed", "conclusion": 3}],
            {"total_count": 1},
            "check runs",
        ]
        for index, payload in enumerate(payloads):
            with self.subTest(payload=payload):
                path = self.write_checks(payload, name=f"bad-{index}.json")
                code, stderr = self.run_packet(checks=path)
                self.assert_error(code, stderr)

    def test_missing_body_exits_2(self):
        code, stderr = self.run_packet(body=self.tmp / "absent.md")
        self.assert_error(code, stderr)
        self.assertIn("body", stderr.lower())

    def test_body_without_sentinels_exits_2(self):
        path = self.tmp / "plain.md"
        path.write_text("just prose, no bound fields\n", encoding="utf-8",
                        newline="")
        code, stderr = self.run_packet(body=path)
        self.assert_error(code, stderr)
        self.assertIn("bound", stderr.lower())

    def test_invalid_utf8_body_exits_2(self):
        path = self.tmp / "binary.md"
        path.write_bytes(b"\xff\xfe\x00not-utf8")
        code, stderr = self.run_packet(body=path)
        self.assert_error(code, stderr)
        self.assertIn("UTF-8", stderr)

    def test_missing_checks_file_exits_2(self):
        code, stderr = self.run_packet(checks=self.tmp / "absent.json")
        self.assert_error(code, stderr)
        self.assertIn("checks", stderr.lower())

    def test_missing_checks_argument_exits_2(self):
        code, stderr = self.run_packet(include_checks=False)
        self.assert_error(code, stderr)
        self.assertIn("--checks", stderr)

    def test_missing_out_parent_exits_2(self):
        out = self.tmp / "missing" / "packet.json"
        code, stderr = self.run_packet(out=out)
        self.assert_error(code, stderr)
        self.assertIn("parent", stderr.lower())
        self.assertFalse(out.exists())

    def test_existing_out_without_force_exits_2(self):
        self.out_path.write_bytes(b"old packet\n")
        code, stderr = self.run_packet()
        self.assert_error(code, stderr)
        self.assertIn("--force", stderr)
        self.assertEqual(b"old packet\n", self.out_path.read_bytes())

    def test_force_overwrites_existing_out(self):
        self.out_path.write_bytes(b"old packet\n")
        code, stderr = self.run_packet(force=True)
        self.assertEqual(0, code, stderr)
        packet = json.loads(self.out_path.read_text(encoding="utf-8"))
        self.assertEqual("aegis.review-packet/1", packet["schema"])

    def test_two_runs_are_byte_identical_and_lf(self):
        first = self.tmp / "first.json"
        second = self.tmp / "second.json"
        self.build_packet(out=first)
        self.build_packet(out=second)
        first_bytes = first.read_bytes()
        self.assertEqual(first_bytes, second.read_bytes())
        self.assertTrue(first_bytes.endswith(b"\n"))
        self.assertNotIn(b"\r\n", first_bytes)
        self.assertTrue(first_bytes.startswith(b'{\n  "base"'))
        self.assertNotIn("timestamp", first_bytes.decode("utf-8").lower())


if __name__ == "__main__":
    unittest.main(verbosity=2)
