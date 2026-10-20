#!/usr/bin/env python3
"""T1-T8 contract tests for tools/record_verifier/run.py (production item 2).

The CLI extracts an exact-line embedded verifier from a readability record and
runs it CI-equivalently: scrubbed environment, isolated Python in a fresh temp
directory, repo-root cwd, timeout, Python-level network guard, and PASS/FAIL/
UNRUN output. These tests live in the existing CI-run readability suite so the
new tool is covered without a .github change; fixtures are written under
tempfile and no tracked data is created.

Coverage (plan AC1-AC6):
  T1  locator fails closed (valid block, missing/duplicated markers, bad
      fences, empty code, wrong order, decoys) with the generic diagnostic
      "no exact-line verifier block found" asserted explicitly; legacy
      fixture detected separately.
  T2  PASS / FAIL / expected-line mismatch semantics.
  T3  CI-equivalence: env allowlist scrub (secrets/proxies absent), isolated
      Python flags, repo-root cwd, fresh removed temp dir, no proxy.
  T4  usage errors exit 2; --help documents flags and exit codes.
  T4b timeout expiry => UNRUN exit 2 with a timeout diagnostic.
  T5  JSON schema/types, deterministic double-run, human output.
  T6  multi/glob input order + de-duplication + UNRUN>FAIL>PASS precedence;
      network guard => FAIL with network_blocked true.
  T7  real-record smoke: pilot + batch-23/24/25/26 PASS (graceful skip when
      the records or full history are absent).
  T7b real legacy records batch-21/22 => UNRUN with both legacy substrings and
      NOT the generic diagnostic.
  T8  repo state unchanged after a run; exactly the 3 planned paths; stdlib
      imports only; new README present.

    python -B -m unittest discover -s tools/readability_acceptance/tests \
        -p "test_*.py" -v
"""
from __future__ import annotations

import ast
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
CLI = ROOT / "tools" / "record_verifier" / "run.py"
README = ROOT / "tools" / "record_verifier" / "README.md"
REAL_DIR = ROOT / "docs" / "evidence" / "documentation"
BT = chr(96)

GENERIC = "no exact-line verifier block found"
LEGACY_A = "legacy verifier format (out of scope)"
LEGACY_B = "no exact-line verifier markers"
PLANNED_ADDED_PATHS = {
    "tools/record_verifier/run.py",
    "tools/record_verifier/README.md",
    "tools/readability_acceptance/tests/test_record_verifier_cli.py",
}
PLANNED_MODIFIED_PATHS = {
    # Owner-authorized test-only repair of the merged item-4 T6 scope test.
    "tools/readability_acceptance/tests/test_blocks.py",
}
PLANNED_PATHS = PLANNED_ADDED_PATHS | PLANNED_MODIFIED_PATHS
ALLOWED_IMPORTS = {
    "__future__", "argparse", "glob", "hashlib", "json", "os", "re",
    "shutil", "subprocess", "sys", "tempfile", "pathlib",
}
REAL_EXACT_LINE = [
    "readability-lane-c-paired-pilot-2026-10-19.md",
    "readability-lane-c-batch-23-2026-10-18.md",
    "readability-lane-c-batch-24-2026-10-18.md",
    "readability-lane-c-batch-25-2026-10-18.md",
    "readability-lane-c-batch-26-2026-10-18.md",
]
REAL_LEGACY = [
    "readability-lane-c-batch-21-2026-10-18.md",
    "readability-lane-c-batch-22-2026-10-18.md",
]
PASS_CODE = 'print("VERIFIER OK fixture")\n'
FAIL_CODE = 'import sys\nprint("VERIFIER FAIL fixture")\nsys.exit(1)\n'
MISMATCH_CODE = 'print("WRONG OUTPUT")\n'
SLEEP_CODE = 'import time\nprint("START")\ntime.sleep(60)\n'
NETWORK_CODE = (
    'import socket\n'
    'socket.create_connection(("127.0.0.1", 9), timeout=1)\n'
    'print("SHOULD NOT PRINT")\n'
)
ENV_CODE = (
    'import os, sys\n'
    'print("ENV " + " ".join(name + "=" + str(name in os.environ) '
    'for name in ("GITHUB_TOKEN", "SECRET", "TOKEN", "PASSWORD", '
    '"http_proxy", "HTTP_PROXY", "HTTPS_PROXY", "NO_PROXY")))\n'
    'print("FLAGS isolated=" + str(sys.flags.isolated) + " dontwrite=" + '
    'str(sys.flags.dont_write_bytecode))\n'
    'print("CWD " + os.getcwd())\n'
    'print("TEMP_DIR " + os.path.dirname(os.path.abspath(__file__)))\n'
    'print("CI " + os.environ.get("CI", ""))\n'
    'print("PATH_PRESENT " + str(bool(os.environ.get("PATH"))))\n'
)
SECRET_ENV = {
    "GITHUB_TOKEN": "secret-github-token",
    "SECRET": "secret-value",
    "TOKEN": "secret-token",
    "PASSWORD": "secret-password",
    "http_proxy": "http://proxy.invalid:3128",
    "HTTP_PROXY": "http://proxy.invalid:3128",
    "HTTPS_PROXY": "http://proxy.invalid:3128",
    "NO_PROXY": "example.invalid",
}


def _git(cwd, *args):
    proc = subprocess.run(["git", "-C", str(cwd), *args], capture_output=True)
    if proc.returncode != 0:
        raise AssertionError("git " + " ".join(args) + " failed: "
                             + proc.stderr.decode("utf-8", "replace")[:300])
    return proc.stdout.decode("utf-8", "replace")


def _run_cli(args, cwd=None, env_extra=None, timeout=300):
    env = dict(os.environ)
    if env_extra:
        env.update(env_extra)
    return subprocess.run(
        [sys.executable, "-B", str(CLI), *args], cwd=str(cwd or ROOT),
        capture_output=True, env=env, timeout=timeout)


def _run_json(args, **kwargs):
    proc = _run_cli([*args, "--json"], **kwargs)
    payload = json.loads(proc.stdout.decode("utf-8")) if proc.stdout.strip()         else None
    return proc, payload


def _make_repo(directory):
    directory.mkdir(parents=True, exist_ok=True)
    _git(directory, "init", "-q")
    _git(directory, "config", "user.email", "record-verifier@example.com")
    _git(directory, "config", "user.name", "record verifier test")
    _git(directory, "config", "core.autocrlf", "false")
    return directory


def _record(directory, name, code, expected=None, *, start=True, end=True,
            fence="~~~python", close="~~~", preamble=None, postamble=None):
    lines = ["# fixture record", ""]
    if preamble:
        lines.extend(preamble)
    if start:
        lines.append("<!-- verifier:start -->")
    if fence is not None:
        lines.append(fence)
    if code:
        lines.extend(code.rstrip("\n").split("\n"))
    if close is not None:
        lines.append(close)
    if end:
        lines.append("<!-- verifier:end -->")
    lines.append("")
    if expected is not None:
        lines.append("**Expected output line:** " + expected)
    if postamble:
        lines.extend(postamble)
    path = directory / name
    path.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")
    return path


def _legacy_record(directory, name, heading, fence):
    lines = [
        "# legacy fixture record", "", heading, "",
        "**Expected output line:** " + BT + "VERIFIER OK legacy" + BT, "",
        fence, "import sys", "print('VERIFIER OK legacy')", "~~~", "",
    ]
    path = directory / name
    path.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")
    return path


class T1Locator(unittest.TestCase):
    """T1: the locator fails closed with the right diagnostic."""

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.dir = Path(self._tmp.name)

    def tearDown(self):
        self._tmp.cleanup()

    def _assert_unrun_generic(self, path):
        proc, payload = _run_json(["--record", str(path)])
        self.assertEqual(proc.returncode, 2, proc.stderr.decode("utf-8", "replace"))
        self.assertIsNotNone(payload)
        self.assertEqual(payload["records"][0]["status"], "UNRUN")
        error = payload["records"][0]["error"] or ""
        self.assertIn(GENERIC, error)
        self.assertNotIn(LEGACY_A, error)

    def test_t1_valid_block_passes_and_decoys_are_ignored(self):
        decoy_lines = [
            "# <!-- verifier:start --> decoy comment",
            "# not a marker: <!-- verifier:end --> inline",
        ]
        path = _record(self.dir, "valid.md", PASS_CODE + "\n".join(decoy_lines)
                       + "\n", "VERIFIER OK fixture")
        proc, payload = _run_json(["--record", str(path)])
        self.assertEqual(proc.returncode, 0, proc.stderr.decode("utf-8", "replace"))
        record = payload["records"][0]
        self.assertEqual(record["status"], "PASS")
        self.assertTrue(record["expected_match"])
        self.assertEqual(record["exit_code"], 0)
        self.assertEqual(record["verifier"]["lines"], 3)

    def test_t1_missing_markers_generic_diagnostic_explicit(self):
        self._assert_unrun_generic(_record(self.dir, "no-start.md", PASS_CODE,
                                           start=False))
        self._assert_unrun_generic(_record(self.dir, "no-end.md", PASS_CODE,
                                           end=False))

    def test_t1_duplicate_and_ordered_markers_fail_closed(self):
        two_blocks = ("<!-- verifier:start -->\n~~~python\n"
                      "print('a')\n~~~\n<!-- verifier:end -->\n"
                      "<!-- verifier:start -->\n~~~python\n"
                      "print('b')\n~~~\n<!-- verifier:end -->\n")
        first = self.dir / "two-blocks.md"
        first.write_text(two_blocks, encoding="utf-8", newline="\n")
        self._assert_unrun_generic(first)
        reversed_path = self.dir / "reversed.md"
        reversed_path.write_text(
            "<!-- verifier:end -->\n~~~python\nprint('x')\n~~~\n"
            "<!-- verifier:start -->\n", encoding="utf-8", newline="\n")
        self._assert_unrun_generic(reversed_path)

    def test_t1_bad_fences_and_empty_code_fail_closed(self):
        self._assert_unrun_generic(_record(self.dir, "no-fence.md", PASS_CODE,
                                           fence=None))
        self._assert_unrun_generic(_record(self.dir, "text-fence.md", PASS_CODE,
                                           fence="~~~text"))
        self._assert_unrun_generic(_record(self.dir, "empty-code.md", ""))
        self._assert_unrun_generic(_record(self.dir, "no-close.md", PASS_CODE,
                                           close=None))

    def test_t1_legacy_fixture_is_its_own_fail_closed_diagnostic(self):
        legacy = _legacy_record(self.dir, "legacy.md",
                                "### Embedded verifier source (copy block)",
                                "~~~~python")
        proc, payload = _run_json(["--record", str(legacy)])
        self.assertEqual(proc.returncode, 2)
        error = payload["records"][0]["error"] or ""
        self.assertIn(LEGACY_A, error)
        self.assertIn(LEGACY_B, error)
        self.assertNotIn(GENERIC, error)


class T2PassFail(unittest.TestCase):
    """T2: PASS / FAIL / expected mismatch."""

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.dir = Path(self._tmp.name)

    def tearDown(self):
        self._tmp.cleanup()

    def test_t2_pass(self):
        path = _record(self.dir, "pass.md", PASS_CODE, "VERIFIER OK fixture")
        proc, payload = _run_json(["--record", str(path)])
        self.assertEqual(proc.returncode, 0)
        record = payload["records"][0]
        self.assertEqual(record["status"], "PASS")
        self.assertTrue(record["expected_match"])
        self.assertFalse(record["network_blocked"])

    def test_t2_fail_nonzero_and_mismatch(self):
        fail = _record(self.dir, "fail.md", FAIL_CODE)
        proc, payload = _run_json(["--record", str(fail)])
        self.assertEqual(proc.returncode, 1)
        self.assertEqual(payload["records"][0]["status"], "FAIL")
        self.assertEqual(payload["records"][0]["exit_code"], 1)
        mismatch = _record(self.dir, "mismatch.md", MISMATCH_CODE,
                           "VERIFIER OK fixture")
        proc, payload = _run_json(["--record", str(mismatch)])
        self.assertEqual(proc.returncode, 1)
        record = payload["records"][0]
        self.assertEqual(record["status"], "FAIL")
        self.assertEqual(record["exit_code"], 0)
        self.assertFalse(record["expected_match"])


class T3CiEquivalence(unittest.TestCase):
    """T3: scrubbed env, isolated Python, repo-root cwd, cleaned temp dir."""

    def test_t3_env_scrub_flags_cwd_and_temp(self):
        tmp = tempfile.TemporaryDirectory()
        try:
            repo = _make_repo(Path(tmp.name) / "repo")
            record = _record(repo, "env.md", ENV_CODE)
            proc, payload = _run_json(
                ["--record", str(record), "--repo", str(repo)],
                env_extra=SECRET_ENV)
            self.assertEqual(proc.returncode, 0,
                             proc.stderr.decode("utf-8", "replace"))
            record_result = payload["records"][0]
            self.assertEqual(record_result["status"], "PASS")
            stdout = record_result["stdout_tail"]
            for name in SECRET_ENV:
                self.assertIn(name + "=False", stdout,
                              name + " leaked into the verifier environment")
            self.assertIn("isolated=1 dontwrite=1", stdout)
            lines = dict(line.split(" ", 1) for line in stdout.splitlines()
                         if " " in line)
            self.assertEqual(lines["CWD"], str(repo.resolve()))
            self.assertEqual(lines["CI"], "true")
            self.assertEqual(lines["PATH_PRESENT"], "True")
            self.assertFalse(Path(lines["TEMP_DIR"]).exists(),
                             "verifier temp dir must be removed after the run")
        finally:
            tmp.cleanup()


class T4UsageAndTimeout(unittest.TestCase):
    """T4/T4b: usage errors exit 2; timeout is UNRUN."""

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.dir = Path(self._tmp.name)

    def tearDown(self):
        self._tmp.cleanup()

    def test_t4_usage_errors_exit_2(self):
        missing = self.dir / "absent.md"
        proc = _run_cli(["--record", str(missing)])
        self.assertEqual(proc.returncode, 2)
        proc = _run_cli(["--record", str(self.dir / "nothing-*.md")])
        self.assertEqual(proc.returncode, 2)
        valid = _record(self.dir, "valid.md", PASS_CODE)
        proc = _run_cli(["--record", str(valid), "--timeout", "0"])
        self.assertEqual(proc.returncode, 2)
        proc = _run_cli(["--record", str(valid), "--timeout", "not-a-number"])
        self.assertEqual(proc.returncode, 2)
        malformed = _record(self.dir, "malformed.md", PASS_CODE, start=False)
        proc, payload = _run_json(["--record", str(malformed)])
        self.assertEqual(proc.returncode, 2)
        self.assertIn(GENERIC, payload["records"][0]["error"] or "")
        legacy = _legacy_record(self.dir, "legacy.md",
                                "## 11. Embedded verifier source, extraction",
                                "~~~python")
        proc, payload = _run_json(["--record", str(legacy)])
        self.assertEqual(proc.returncode, 2)
        error = payload["records"][0]["error"] or ""
        self.assertIn(LEGACY_A, error)
        self.assertIn(LEGACY_B, error)

    def test_t4_help_documents_flags_and_exit_codes(self):
        proc = _run_cli(["--help"])
        self.assertEqual(proc.returncode, 0)
        help_text = proc.stdout.decode("utf-8")
        for flag in ("--record", "--repo", "--json", "--timeout", "--quiet"):
            self.assertIn(flag, help_text)
        self.assertIn("Exit codes", help_text)

    def test_t4b_timeout_is_unrun_exit_2(self):
        path = _record(self.dir, "sleep.md", SLEEP_CODE)
        proc, payload = _run_json(["--record", str(path), "--timeout", "1"])
        self.assertEqual(proc.returncode, 2)
        record = payload["records"][0]
        self.assertEqual(record["status"], "UNRUN")
        self.assertIsNone(record["exit_code"])
        self.assertIn("timeout", (record["error"] or "").lower())


class T5Output(unittest.TestCase):
    """T5: deterministic JSON schema and human output."""

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.dir = Path(self._tmp.name)

    def tearDown(self):
        self._tmp.cleanup()

    def test_t5_json_schema_and_double_run_determinism(self):
        passing = _record(self.dir, "pass.md", PASS_CODE, "VERIFIER OK fixture")
        failing = _record(self.dir, "fail.md", FAIL_CODE)
        args = ["--record", str(passing), "--record", str(failing)]
        first = _run_cli([*args, "--json"])
        second = _run_cli([*args, "--json"])
        self.assertEqual(first.stdout, second.stdout)
        payload = json.loads(first.stdout.decode("utf-8"))
        self.assertEqual(set(payload), {"schema_version", "records", "summary"})
        self.assertEqual(payload["schema_version"], 1)
        self.assertEqual(len(payload["records"]), 2)
        record_keys = {"record", "status", "exit_code", "expected_line",
                       "expected_match", "network_blocked", "verifier",
                       "stdout_tail", "stderr_tail", "error"}
        for record in payload["records"]:
            self.assertEqual(set(record), record_keys)
            self.assertEqual(
                set(record["verifier"]),
                {"start_line", "end_line", "lines", "lf", "sha256"})
            self.assertIsInstance(record["verifier"]["start_line"], int)
            self.assertIsInstance(record["verifier"]["end_line"], int)
            self.assertEqual(
                len(record["verifier"]["sha256"]), 64)
        summary = payload["summary"]
        self.assertEqual(set(summary),
                         {"total", "pass", "fail", "unrun", "exit_code"})
        self.assertEqual(summary["total"], 2)
        self.assertEqual(summary["pass"], 1)
        self.assertEqual(summary["fail"], 1)
        self.assertEqual(summary["unrun"], 0)
        self.assertEqual(summary["exit_code"], 1)
        self.assertNotIn("timestamp", first.stdout.decode("utf-8").lower())

    def test_t5_human_output(self):
        passing = _record(self.dir, "pass.md", PASS_CODE, "VERIFIER OK fixture")
        failing = _record(self.dir, "fail.md", FAIL_CODE)
        proc = _run_cli(["--record", str(passing), "--record", str(failing)])
        text = proc.stdout.decode("utf-8")
        self.assertEqual(proc.returncode, 1)
        self.assertIn("PASS " + str(passing.resolve()), text)
        self.assertIn("FAIL " + str(failing.resolve()), text)
        self.assertIn("summary:", text)
        self.assertIn("exit_code=1", text)
        quiet = _run_cli(["--record", str(passing), "--quiet"])
        self.assertNotIn("PASS ", quiet.stdout.decode("utf-8"))
        self.assertIn("summary:", quiet.stdout.decode("utf-8"))


class T6MultiAndNetwork(unittest.TestCase):
    """T6: multi/glob order + de-dup + precedence; network guard."""

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.dir = Path(self._tmp.name)

    def tearDown(self):
        self._tmp.cleanup()

    def test_t6_multi_glob_order_dedupe_precedence(self):
        pass_one = _record(self.dir, "fixture-1.md", PASS_CODE,
                           "VERIFIER OK fixture")
        pass_two = _record(self.dir, "fixture-2.md", PASS_CODE,
                           "VERIFIER OK fixture")
        fail = _record(self.dir, "fixture-3.md", FAIL_CODE)
        glob_pattern = str(self.dir / "fixture-*.md")
        proc, payload = _run_json(["--record", glob_pattern,
                                   "--record", str(pass_one)])
        self.assertEqual(proc.returncode, 1)
        names = [Path(item["record"]).name for item in payload["records"]]
        self.assertEqual(names, ["fixture-1.md", "fixture-2.md", "fixture-3.md"])
        self.assertEqual(payload["summary"]["total"], 3)
        self.assertEqual(payload["summary"]["exit_code"], 1)
        legacy = _legacy_record(self.dir, "fixture-4.md",
                                "### Embedded verifier source", "~~~python")
        proc, payload = _run_json(["--record", glob_pattern,
                                   "--record", str(legacy)])
        self.assertEqual(proc.returncode, 2)
        self.assertEqual(payload["summary"]["unrun"], 1)
        self.assertEqual(payload["summary"]["exit_code"], 2)
        proc, payload = _run_json(["--record", str(pass_two),
                                   "--record", str(pass_one)])
        self.assertEqual(proc.returncode, 0)
        self.assertEqual(payload["summary"]["exit_code"], 0)
        self.assertEqual([Path(item["record"]).name
                          for item in payload["records"]],
                         ["fixture-2.md", "fixture-1.md"])

    def test_t6_network_guard_fails_with_flag(self):
        path = _record(self.dir, "network.md", NETWORK_CODE)
        proc, payload = _run_json(["--record", str(path)])
        self.assertEqual(proc.returncode, 1)
        record = payload["records"][0]
        self.assertEqual(record["status"], "FAIL")
        self.assertTrue(record["network_blocked"])
        self.assertIn("NETWORK_BLOCKED", record["stderr_tail"])


class T7RealRecords(unittest.TestCase):
    """T7/T7b: real records at this checkout (skip when absent)."""

    def test_t7_real_exact_line_smoke(self):
        paths = [REAL_DIR / name for name in REAL_EXACT_LINE]
        if not all(path.is_file() for path in paths):
            self.skipTest("real exact-line records absent (shallow checkout)")
        args = []
        for path in paths:
            args.extend(["--record", str(path)])
        proc, payload = _run_json(args)
        self.assertEqual(proc.returncode, 0,
                         proc.stderr.decode("utf-8", "replace"))
        self.assertEqual(payload["summary"]["total"], len(REAL_EXACT_LINE))
        self.assertEqual(payload["summary"]["pass"], len(REAL_EXACT_LINE))
        for record in payload["records"]:
            self.assertEqual(record["status"], "PASS", record["record"])
            self.assertTrue(record["expected_match"], record["record"])
            self.assertEqual(record["exit_code"], 0)
            self.assertGreater(record["verifier"]["lines"], 50)

    def test_t7b_real_legacy_records_unrun(self):
        paths = [REAL_DIR / name for name in REAL_LEGACY]
        if not all(path.is_file() for path in paths):
            self.skipTest("real legacy records absent (shallow checkout)")
        args = []
        for path in paths:
            args.extend(["--record", str(path)])
        proc, payload = _run_json(args)
        self.assertEqual(proc.returncode, 2)
        self.assertEqual(payload["summary"]["unrun"], len(REAL_LEGACY))
        for record in payload["records"]:
            error = record["error"] or ""
            self.assertIn(LEGACY_A, error, record["record"])
            self.assertIn(LEGACY_B, error, record["record"])
            self.assertNotIn(GENERIC, error, record["record"])


class T8RepoStateAndScope(unittest.TestCase):
    """T8: repo state unchanged; exactly the 3 planned paths; stdlib only."""

    def _changed_paths(self):
        merge_base = _git(ROOT, "merge-base", "origin/main", "HEAD").strip()
        status = _git(ROOT, "diff", "--name-status", merge_base)
        entries = [line.split("\t") for line in status.splitlines() if line]
        untracked = _git(
            ROOT, "ls-files", "--others", "--exclude-standard").splitlines()
        for path in untracked:
            if path in PLANNED_ADDED_PATHS:
                entries.append(["A", path])
        return entries

    def test_t8_repo_state_unchanged_by_a_run(self):
        record = REAL_DIR / REAL_EXACT_LINE[1]
        if not record.is_file():
            self.skipTest("real record absent (shallow checkout)")
        before = _git(ROOT, "status", "--porcelain")
        _run_json(["--record", str(record)])
        after = _git(ROOT, "status", "--porcelain")
        self.assertEqual(before, after, "the verifier run modified the repo")

    def test_t8_exact_3_added_1_modified_paths(self):
        """AC6: exactly 3 added + 1 modified, statuses and no .github change.

        The 3 added paths are enumerated from git ls-files --others while they
        are untracked (and appear as A in the tracked diff once committed); the
        owner-authorized test-only repair appears as the tracked M path.
        """
        changes = self._changed_paths()
        if not changes:
            self.skipTest("no base diff (running on main after merge)")
        statuses = {entry[1]: entry[0] for entry in changes}
        self.assertEqual(set(statuses), PLANNED_PATHS)
        for path in PLANNED_ADDED_PATHS:
            self.assertEqual(statuses[path], "A", path)
        for path in PLANNED_MODIFIED_PATHS:
            self.assertIn(statuses[path], ("M", "A"), path)
        for path, status in statuses.items():
            self.assertFalse(path.startswith(".github/"), path)
            self.assertIn(status, ("A", "M"), path)

    def test_t8_stdlib_only_and_readme_present(self):
        tree = ast.parse(CLI.read_text(encoding="utf-8"))
        imports = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imports.update(alias.name.split(".")[0] for alias in node.names)
            elif isinstance(node, ast.ImportFrom) and node.module:
                imports.add(node.module.split(".")[0])
        self.assertEqual(imports, ALLOWED_IMPORTS)
        for banned in ("sock" + "et", "ur" + "llib", "ht" + "tp"):
            self.assertNotIn("import " + banned + "\n",
                             CLI.read_text(encoding="utf-8"))
        self.assertTrue(README.is_file(), "new package README is required")
        readme = README.read_text(encoding="utf-8").lower()
        for section in ("usage", "exit codes", "json", "network", "timeout"):
            self.assertIn(section, readme)


if __name__ == "__main__":
    unittest.main()
