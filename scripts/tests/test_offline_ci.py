#!/usr/bin/env python3
"""Regression checks for evidence exit codes and the actual protected-file guard."""
from __future__ import annotations

import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

import yaml

REPO = Path(__file__).resolve().parents[2]
RECORDER = REPO / "scripts/ci/record-check.py"
WORKFLOW = REPO / ".github/workflows/validate-skills.yml"


class RecorderTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="aegis-ci-recorder-")
        self.addCleanup(self.temp.cleanup)
        self.output = Path(self.temp.name) / "evidence"
        self.env = dict(os.environ, AEGIS_CI_EVIDENCE_DIR=str(self.output))

    def run_check(self, label, command):
        return subprocess.run([sys.executable, str(RECORDER), label, "--", *command],
                              cwd=REPO, env=self.env, capture_output=True)

    def test_failure_preserves_native_status_and_both_streams(self):
        result = self.run_check("failure", [sys.executable, "-c",
            "import sys; print('stdout evidence'); sys.stderr.write('stderr evidence\\n'); sys.exit(7)"])
        self.assertEqual(7, result.returncode, result.stdout + result.stderr)
        log = (self.output / "failure.log").read_bytes()
        self.assertIn(b"stdout evidence", log)
        self.assertIn(b"stderr evidence", log)
        report = json.loads((self.output / "failure.json").read_text(encoding="utf-8"))
        self.assertEqual(7, report["exit_code"])
        self.assertEqual(subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=REPO,
                                                text=True).strip(), report["checkout_sha"])

    def test_missing_command_is_recorded_as_failure(self):
        result = self.run_check("missing", ["aegis-nonexistent-ci-command-3ba68f"])
        self.assertEqual(127, result.returncode)
        report = json.loads((self.output / "missing.json").read_text(encoding="utf-8"))
        self.assertEqual(127, report["exit_code"])
        self.assertIn(b"Cannot execute check", (self.output / "missing.log").read_bytes())

    def test_repeated_label_cannot_replace_prior_evidence(self):
        self.assertEqual(0, self.run_check("once", [sys.executable, "-c", "print('original')"]).returncode)
        before = {p.name: p.read_bytes() for p in self.output.iterdir()}
        self.assertNotEqual(0, self.run_check("once", [sys.executable, "-c", "print('replacement')"]).returncode)
        self.assertEqual(before, {p.name: p.read_bytes() for p in self.output.iterdir()})

    def test_label_cannot_escape_evidence_directory(self):
        self.assertNotEqual(0, self.run_check("../escape", [sys.executable, "-c", "pass"]).returncode)
        self.assertFalse(self.output.exists())


@unittest.skipUnless(os.name == "posix" and shutil.which("bash"), "the gate-guard job executes on Linux")
class ProtectedFileGuardTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # BaseLoader preserves GitHub's literal `on` key instead of YAML 1.1 bools.
        workflow = yaml.load(WORKFLOW.read_text(encoding="utf-8"), Loader=yaml.BaseLoader)
        cls.guard = next(step["run"] for step in workflow["jobs"]["gate-guard"]["steps"]
                         if "gate_pattern=" in step.get("run", ""))

    def run_guard(self, paths, *, rename=False):
        with tempfile.TemporaryDirectory(prefix="aegis-ci-guard-") as temporary:
            root = Path(temporary)
            repo = root / "repo"
            repo.mkdir()
            def git(*args):
                return subprocess.run(["git", "-c", "user.name=Fixture", "-c",
                                       "user.email=fixture@example.invalid", *args], cwd=repo,
                                      check=True, capture_output=True)
            git("init", "--quiet")
            (repo / "README.md").write_text("fixture\n", encoding="utf-8")
            if rename:
                old = repo / ".github/workflows/previous.yml"
                old.parent.mkdir(parents=True)
                old.write_text("protected fixture\n", encoding="utf-8")
            git("add", ".")
            git("commit", "--quiet", "-m", "fixture base")
            git("branch", "fixture-base")
            git("remote", "add", "origin", str(repo))
            if rename:
                (repo / "docs").mkdir()
                git("mv", ".github/workflows/previous.yml", "docs/previous.yml")
            else:
                for path in paths:
                    file = repo / path
                    file.parent.mkdir(parents=True, exist_ok=True)
                    file.write_text("changed fixture\n", encoding="utf-8")
            git("add", ".")
            git("commit", "--quiet", "-m", "fixture change")
            return subprocess.run(["bash", "--noprofile", "--norc", "-eo", "pipefail", "-c", self.guard],
                                  cwd=repo, env=dict(os.environ, BASE_REF="fixture-base", RUNNER_TEMP=str(root)),
                                  capture_output=True, text=True)

    def test_each_enforcement_surface_requires_manual_merge(self):
        for path in (".github/workflows/check.yml", ".github/CODEOWNERS",
                     "scripts/validate-skills.py", "scripts/check_dco.py", "scripts/tests/fixture.py",
                     "scripts/ci/record-check.py", "scripts/audit-skill-contracts.py",
                     "scripts/acceptance/scenario-a-fixture/manifest.json", "tools.py", "tools/__init__.py",
                     "tools/behavioral_eval_runner/tests/fixture.py",
                     "tools/behavioral_eval_runner/schemas/fixture.json",
                     "tools/behavioral_eval_runner/graders/fixture.py", "requirements.txt", "requirements-ci.txt"):
            with self.subTest(path=path):
                result = self.run_guard([path])
                self.assertEqual(1, result.returncode, result.stdout + result.stderr)
                self.assertIn("requires manual review and merge", result.stdout)

    def test_ordinary_skill_and_document_changes_pass(self):
        result = self.run_guard(["README.md", "docs/notes.md", ".claude/skills/example/SKILL.md"])
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)

    def test_renaming_a_protected_file_outside_the_set_is_still_guarded(self):
        result = self.run_guard([], rename=True)
        self.assertEqual(1, result.returncode, result.stdout + result.stderr)
        self.assertIn("requires manual review and merge", result.stdout)

    def test_unicode_and_newline_names_cannot_bypass_the_guard(self):
        result = self.run_guard([".github/workflows/\u2603\ncheck.yml"])
        self.assertEqual(1, result.returncode, result.stdout + result.stderr)
        self.assertIn("requires manual review and merge", result.stdout)


if __name__ == "__main__":
    unittest.main(verbosity=2)
