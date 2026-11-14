"""CLI, determinism, isolation, docs and closed-path checks.

Covers AC-PLAN-2/3/4's local evidence and AC-C3.2-4/AC-C3.3-1/AC-C3.3-2's
document-level checks.  Hosted CI, the gate-guard red and the owner merge line
remain UNRUN.
"""

from __future__ import annotations

import ast
import json
import pathlib
import subprocess
import tempfile
import unittest

from tools.aegis_ops import schema

import _fixtures


PACKAGE = _fixtures.ROOT / "tools" / "aegis_ops"
TESTS = PACKAGE / "tests"
OPS_DOCS = _fixtures.ROOT / "docs" / "operations"
WORKFLOW = _fixtures.ROOT / ".github" / "workflows" / "validate-skills.yml"


class CliTests(unittest.TestCase):
    def test_self_test(self) -> None:
        completed = _fixtures.run_cli("--self-test")
        self.assertEqual(completed.returncode, 0, completed.stderr)
        report = json.loads(completed.stdout)
        self.assertTrue(report["ok"])
        self.assertEqual(len(report["checks"]), 4)

    def test_valid_fixtures_exit_zero(self) -> None:
        cases = (
            ("validate", "event-catalogue-valid.json"),
            ("settle", "settlement-valid.json"),
            ("routing", "routing-matrix-valid.json"),
            ("holders", "holder-valid.json"),
            ("inbox", "inbox-disabled-valid.json"),
            ("pilot-metrics", "pilot-metrics-valid.json"),
        )
        for command, name in cases:
            completed = _fixtures.run_cli(command, "--input", str(TESTS / "fixtures" / name))
            self.assertEqual(completed.returncode, 0, (command, name, completed.stderr, completed.stdout))

    def test_negative_fixtures_exit_one(self) -> None:
        cases = (
            ("validate", "out-of-order-event.json"),
            ("settle", "settlement-pending-review.json"),
            ("routing", "routing-required-check-skip-refused.json"),
            ("holders", "holder-duplicate-active.json"),
            ("inbox", "inbox-invalid-value.json"),
            ("pilot-metrics", "pilot-metrics-dollar-invented.json"),
        )
        for command, name in cases:
            completed = _fixtures.run_cli(command, "--input", str(TESTS / "fixtures" / name))
            self.assertEqual(completed.returncode, 1, (command, name, completed.stderr))

    def test_malformed_input_exits_two(self) -> None:
        with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False, encoding="utf-8") as handle:
            handle.write("{not json")
            path = handle.name
        try:
            completed = _fixtures.run_cli("validate", "--input", path)
            self.assertEqual(completed.returncode, 2)
            self.assertIn("invalid input", completed.stderr)
        finally:
            pathlib.Path(path).unlink()

    def test_unknown_schema_exits_two(self) -> None:
        with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False, encoding="utf-8") as handle:
            json.dump({"schema_version": "aegis.unknown/v1"}, handle)
            path = handle.name
        try:
            completed = _fixtures.run_cli("validate", "--input", path)
            self.assertEqual(completed.returncode, 2)
        finally:
            pathlib.Path(path).unlink()

    def test_settle_prints_envelope(self) -> None:
        completed = _fixtures.run_cli(
            "settle", "--input", str(TESTS / "fixtures" / "settlement-valid.json")
        )
        self.assertEqual(completed.returncode, 0)
        envelope = json.loads(completed.stdout)
        self.assertIn("payload", envelope)
        self.assertIn("provenance", envelope)
        self.assertEqual(
            envelope["provenance"]["declared_payload_sha256"],
            schema.digest(envelope["payload"]),
        )

    def test_deterministic_output(self) -> None:
        first = _fixtures.run_cli(
            "pilot-metrics", "--input", str(TESTS / "fixtures" / "pilot-metrics-valid.json")
        )
        second = _fixtures.run_cli(
            "pilot-metrics", "--input", str(TESTS / "fixtures" / "pilot-metrics-valid.json")
        )
        self.assertEqual(first.returncode, 0)
        self.assertEqual(first.stdout, second.stdout)

    def test_routing_workflow_check(self) -> None:
        completed = _fixtures.run_cli(
            "routing",
            "--input",
            str(TESTS / "fixtures" / "routing-matrix-valid.json"),
            "--workflow",
            str(WORKFLOW),
        )
        self.assertEqual(completed.returncode, 0, completed.stdout + completed.stderr)
        result = json.loads(completed.stdout)
        self.assertTrue(result["workflow"]["valid"])


class IsolationTests(unittest.TestCase):
    def _package_modules(self) -> list:
        return sorted(path for path in PACKAGE.glob("*.py"))

    def test_no_network_or_write_imports(self) -> None:
        forbidden = {
            "asyncio",
            "ftplib",
            "http",
            "multiprocessing",
            "requests",
            "socket",
            "ssl",
            "subprocess",
            "telnetlib",
            "urllib",
        }
        for path in self._package_modules():
            tree = ast.parse(path.read_text(encoding="utf-8"))
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        self.assertNotIn(alias.name.split(".")[0], forbidden, path)
                elif isinstance(node, ast.ImportFrom) and node.module:
                    self.assertNotIn(node.module.split(".")[0], forbidden, path)
                elif isinstance(node, ast.Call):
                    if isinstance(node.func, ast.Name) and node.func.id == "open":
                        mode = ""
                        if len(node.args) > 1 and isinstance(node.args[1], ast.Constant):
                            mode = str(node.args[1].value)
                        self.assertNotRegex(mode, r"[wax+]", path)
                    if isinstance(node.func, ast.Attribute) and node.func.attr in (
                        "write_text",
                        "write_bytes",
                    ):
                        self.fail("write call in %s" % path)

    def test_repository_clean_after_cli(self) -> None:
        before = subprocess.run(
            ["git", "-C", str(_fixtures.ROOT), "status", "--porcelain"],
            capture_output=True,
            text=True,
            check=True,
        ).stdout
        _fixtures.run_cli("validate", "--input", str(TESTS / "fixtures" / "event-catalogue-valid.json"))
        after = subprocess.run(
            ["git", "-C", str(_fixtures.ROOT), "status", "--porcelain"],
            capture_output=True,
            text=True,
            check=True,
        ).stdout
        self.assertEqual(before, after)


class DocsAndScopeTests(unittest.TestCase):
    def test_closed_file_counts(self) -> None:
        self.assertEqual(len(list(PACKAGE.glob("*.py"))), 9)
        self.assertEqual(len(list(TESTS.glob("*.py"))), 7)
        self.assertEqual(len(list((TESTS / "fixtures").glob("*.json"))), 23)
        self.assertEqual(len(list(OPS_DOCS.glob("*.md"))), 7)
        self.assertTrue((PACKAGE / "README.md").is_file())

    def test_advisory_policy_subsection(self) -> None:
        text = (_fixtures.ROOT / "docs" / "delivery-workflow.md").read_text(
            encoding="utf-8"
        )
        for phrase in (
            "### Advisory review triggers and findings policy (C3.3)",
            "advisory is not a gate",
            "not a required context",
            "no severity-label waiver",
            "R3 finding-triage rubric",
            "carried findings",
            "trigger and yield measurement",
        ):
            self.assertIn(phrase.lower(), text.lower())
        self.assertFalse((_fixtures.ROOT / "docs" / "REVIEW-POLICY.md").exists())

    def test_preservation_inventory(self) -> None:
        text = (_fixtures.ROOT / "docs" / "operations" / "advisory-trigger-findings-policy.md").read_text(
            encoding="utf-8"
        )
        for phrase in (
            "Clause-by-clause preservation inventory (E2)",
            "MG1",
            "R3 finding-triage rubric",
            "No existing clause is removed, relaxed, renamed or duplicated.",
            "AUTH-C3-POLICY",
        ):
            self.assertIn(phrase, text)

    def test_all_planned_paths_exist(self) -> None:
        package = _fixtures.ROOT / "tools" / "aegis_ops"
        docs = _fixtures.ROOT / "docs" / "operations"
        expected = [
            package / "__init__.py",
            package / "__main__.py",
            package / "schema.py",
            package / "events.py",
            package / "settlement.py",
            package / "routing.py",
            package / "holders.py",
            package / "inbox_activity.py",
            package / "README.md",
            package / "pilot_metrics.py",
            package / "tests" / "_fixtures.py",
            package / "tests" / "test_events_settlement.py",
            package / "tests" / "test_routing.py",
            package / "tests" / "test_holders.py",
            package / "tests" / "test_inbox_activity.py",
            package / "tests" / "test_pilot_metrics.py",
            package / "tests" / "test_cli.py",
            docs / "README.md",
            docs / "overhead-controls.md",
            docs / "ci-routing-matrix.md",
            docs / "advisory-trigger-findings-policy.md",
            docs / "stage-holders-and-replacement.md",
            docs / "inbox-zero-activity.md",
            docs / "qualification-and-pilot-metrics.md",
            _fixtures.ROOT / ".github" / "workflows" / "validate-skills.yml",
            _fixtures.ROOT / "docs" / "delivery-workflow.md",
        ]
        for path in expected:
            self.assertTrue(path.is_file(), path)


if __name__ == "__main__":
    unittest.main()
