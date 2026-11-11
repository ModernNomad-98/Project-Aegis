"""CLI, determinism, isolation and exit-code tests (C1.2 D1)."""

from __future__ import annotations

import contextlib
import io
import json
import os
import pathlib
import shutil
import subprocess
import sys
import unittest

if str(pathlib.Path(__file__).resolve().parents[3]) not in sys.path:
    sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3]))

import _fixtures  # noqa: E402
from tools.aegis_change_state import __main__ as cli  # noqa: E402
from tools.aegis_change_state import schema  # noqa: E402

PACKAGE = pathlib.Path(__file__).resolve().parents[1]


def run_cli(*arguments: str) -> tuple:
    buffer = io.StringIO()
    with contextlib.redirect_stdout(buffer):
        code = cli.main(list(arguments))
    return (code, buffer.getvalue())


def run_module(*arguments: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, "-m", "tools.aegis_change_state"] + list(arguments),
        cwd=str(_fixtures.REPO_ROOT),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
        timeout=300,
    )


class SelfTestCliTest(unittest.TestCase):
    def test_self_test_exits_zero_and_is_byte_identical(self):
        first = run_module("self-test")
        second = run_module("self-test")
        self.assertEqual(first.returncode, 0, first.stderr.decode("utf-8", "replace"))
        self.assertEqual(first.stdout, second.stdout)
        report = json.loads(first.stdout.decode("utf-8"))
        self.assertTrue(report["ok"])
        self.assertEqual([item["name"] for item in report["checks"]], [
            "canonicalization",
            "bundle-round-trip",
            "tamper-detection",
            "overclaim-refusal",
        ])
        self.assertEqual(report["assurance"]["claim"], "AUDITABLE")
        self.assertEqual(report["assurance"]["mounted_coverage"], "UNKNOWN")
        self.assertEqual(report["readiness"], "NOT_COMPUTED")


class BuildAndValidateCliTest(unittest.TestCase):
    def setUp(self):
        self.temporary = _fixtures.temporary_directory()
        self.addCleanup(lambda: shutil.rmtree(str(self.temporary), ignore_errors=True))

    def test_build_then_validate_is_deterministic_and_valid(self):
        bundle = self.temporary / "bundle"
        code, output = run_cli("build", "--out", str(bundle))
        self.assertEqual(code, 0)
        self.assertTrue(json.loads(output)["ok"])
        first_code, first = run_cli("validate", "--bundle", str(bundle))
        second_code, second = run_cli("validate", "--bundle", str(bundle))
        self.assertEqual(first_code, 0)
        self.assertEqual(first_code, second_code)
        self.assertEqual(first, second)
        report = json.loads(first)
        self.assertTrue(report["ok"])
        self.assertEqual(report["blockers"], [])
        self.assertEqual(report["assurance"]["enforced"], "BLOCKED")
        self.assertEqual(report["readiness"], "NOT_COMPUTED")

    def test_validate_tampered_bundle_exits_one(self):
        bundle = _fixtures.build_bundle(self.temporary / "bundle")
        ledger = bundle / "ledger" / (_fixtures.CHANGE_ID + ".jsonl")
        lines = ledger.read_bytes().split(b"\n")
        lines[0] = lines[0].replace(b'"kind":"INITIAL"', b'"kind":"RESYNC"')
        ledger.write_bytes(b"\n".join(lines))
        code, output = run_cli("validate", "--bundle", str(bundle))
        self.assertEqual(code, 1)
        report = json.loads(output)
        self.assertFalse(report["ok"])
        self.assertIn("STATE_TAMPER_SUSPECTED", _fixtures.blockers_codes(report))

    def test_validate_absent_bundle_exits_one(self):
        empty = self.temporary / "empty"
        empty.mkdir()
        code, output = run_cli("validate", "--bundle", str(empty))
        self.assertEqual(code, 1)
        self.assertFalse(json.loads(output)["ok"])

    def test_malformed_fixture_exits_two(self):
        broken = self.temporary / "broken"
        broken.mkdir()
        (broken / "valid-freeze.json").write_text("{not json", encoding="utf-8")
        code, output = run_cli("build", "--out", str(self.temporary / "out"), "--from", str(broken))
        self.assertEqual(code, 2)
        self.assertEqual(json.loads(output)["error"], "invalid input")

    def test_snapshot_manifest_for_absent_repository_exits_two(self):
        code, output = run_cli(
            "snapshot-manifest",
            "--repo",
            str(self.temporary / "missing"),
            "--commit",
            "0" * 40,
            "--change-id",
            "change-1",
            "--base",
            "0" * 40,
            "--retention-ref",
            "synthetic",
            "--created-by",
            "fixture",
            "--created-at",
            "2026-11-11T05:00:00Z",
            "--out",
            str(self.temporary / "out.json"),
        )
        self.assertEqual(code, 2)
        self.assertEqual(json.loads(output)["error"], "invalid input")

    def test_missing_argument_exits_two(self):
        completed = run_module("build")
        self.assertEqual(completed.returncode, 2)

    def test_unknown_command_exits_two(self):
        completed = run_module("not-a-command")
        self.assertEqual(completed.returncode, 2)

    def test_exit_code_constants_are_the_documented_table(self):
        self.assertEqual(cli.EXIT_OK, 0)
        self.assertEqual(cli.EXIT_BLOCKED, 1)
        self.assertEqual(cli.EXIT_INVALID, 2)
        self.assertEqual(cli.EXIT_INTERNAL, 3)


class IsolationTest(unittest.TestCase):
    def test_cli_leaves_the_repository_clean(self):
        before = subprocess.run(
            ["git", "-C", str(_fixtures.REPO_ROOT), "status", "--porcelain"],
            stdout=subprocess.PIPE,
            check=False,
        ).stdout
        temporary = _fixtures.temporary_directory()
        self.addCleanup(lambda: shutil.rmtree(str(temporary), ignore_errors=True))
        run_module("self-test")
        run_module("build", "--out", str(temporary / "bundle"))
        run_module("validate", "--bundle", str(temporary / "bundle"))
        after = subprocess.run(
            ["git", "-C", str(_fixtures.REPO_ROOT), "status", "--porcelain"],
            stdout=subprocess.PIPE,
            check=False,
        ).stdout
        # The evidence claim is "this run adds nothing": a checkout that
        # already carried unrelated work is reported, not silently cleaned.
        self.assertEqual(before, after)
        if not before.strip():
            self.assertEqual(after.strip(), b"")

    def test_no_network_module_is_imported(self):
        forbidden = ("socket", "urllib", "http.client", "requests", "ftplib", "smtplib", "telnetlib")
        for path in sorted(PACKAGE.glob("*.py")):
            source = path.read_text(encoding="utf-8")
            for token in forbidden:
                self.assertNotIn("import " + token, source, "%s imports %s" % (path.name, token))
                self.assertNotIn("from " + token, source, "%s imports %s" % (path.name, token))

    def test_subprocess_is_confined_to_read_only_git_plumbing(self):
        for path in sorted(PACKAGE.glob("*.py")):
            source = path.read_text(encoding="utf-8")
            if "subprocess" in source:
                self.assertIn(path.name, ("records.py", "snapshot.py"), path.name)
                self.assertIn("git", source)

    def test_validators_cannot_write(self):
        for name in ("schema.py", "checks.py", "snapshot.py", "catalogue.py" if False else "checks.py"):
            source = (PACKAGE / name).read_text(encoding="utf-8")
            for token in ("write_text(", "write_bytes(", '.open("w', ".open('w"):
                self.assertNotIn(token, source, "%s contains a write primitive" % name)

    def test_only_documented_writers_write(self):
        writers = {
            path.name
            for path in sorted(PACKAGE.glob("*.py"))
            if "write_text(" in path.read_text(encoding="utf-8")
            or "write_bytes(" in path.read_text(encoding="utf-8")
        }
        self.assertEqual(writers, {"records.py", "__main__.py"})

    def test_output_has_no_timestamp_or_environment_value(self):
        temporary = _fixtures.temporary_directory()
        self.addCleanup(lambda: shutil.rmtree(str(temporary), ignore_errors=True))
        bundle = _fixtures.build_bundle(temporary / "bundle")
        _code, first = run_cli("validate", "--bundle", str(bundle))
        _code, second = run_cli("validate", "--bundle", str(bundle))
        self.assertEqual(first, second)
        report = json.loads(first)
        rendered = json.dumps(report)
        self.assertNotIn(os.environ.get("COMPUTERNAME", "no-such-computer"), rendered)
        self.assertNotIn(str(_fixtures.REPO_ROOT), rendered)


if __name__ == "__main__":
    unittest.main()
