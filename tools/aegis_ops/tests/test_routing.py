"""C3.2: routing matrix, required-check invariant and the bounded E1 shape.

Covers AC-C3.2-1, AC-C3.2-2 and AC-C3.2-3's static invariants.
"""

from __future__ import annotations

import json
import pathlib
import unittest

from tools.aegis_ops import routing, schema

import _fixtures


class RoutingMatrixTests(unittest.TestCase):
    def test_valid_matrix(self) -> None:
        result = routing.validate(_fixtures.load("routing-matrix-valid.json"))
        self.assertTrue(result["valid"])
        self.assertEqual(result["required_checks"], ["gate-guard", "validate-skills"])
        for path, checks in result["affected_checks"].items():
            self.assertIn("validate-skills", checks, path)
            self.assertIn("gate-guard", checks, path)
        self.assertFalse(result["docs_skills"])
        self.assertEqual(result["skipped_advisory"], [])
        self.assertIn(
            "tools-tests-linux", result["affected_checks"]["tools/aegis_ops/schema.py"]
        )
        self.assertIn(
            "windows-offline-checks",
            result["affected_checks"]["tools/aegis_ops/schema.py"],
        )

    def test_required_check_skip_is_refused(self) -> None:
        result = routing.validate(
            _fixtures.load("routing-required-check-skip-refused.json")
        )
        self.assertFalse(result["valid"])
        codes = [issue["code"] for issue in result["issues"]]
        self.assertIn("ROUTING_REQUIRED_CHECK_SKIPPABLE", codes)
        self.assertIn("ROUTING_REQUIRED_CHECK_ROUTED_AWAY", codes)

    def test_unmapped_path_fails_closed(self) -> None:
        result = routing.validate(_fixtures.load("routing-unmapped-path.json"))
        self.assertFalse(result["valid"])
        self.assertIn(
            "ROUTING_UNMAPPED_PATH", [issue["code"] for issue in result["issues"]]
        )

    def test_determinism(self) -> None:
        first = routing.validate(_fixtures.load("routing-matrix-valid.json"))
        second = routing.validate(_fixtures.load("routing-matrix-valid.json"))
        self.assertEqual(json.dumps(first, sort_keys=True), json.dumps(second, sort_keys=True))

    def test_docs_skills_closed_predicate(self) -> None:
        self.assertTrue(schema.classify_docs_skills(["docs/operations/README.md"]))
        self.assertTrue(schema.classify_docs_skills([".claude/skills/x/SKILL.md"]))
        self.assertTrue(
            schema.classify_docs_skills(
                ["docs/a.md", ".claude/skills/b/SKILL.md"]
            )
        )
        self.assertFalse(schema.classify_docs_skills([]))
        self.assertFalse(
            schema.classify_docs_skills(
                ["docs/a.md", "tools/aegis_ops/schema.py"]
            )
        )
        self.assertFalse(schema.classify_docs_skills(["README.md"]))

    def _matrix(self, changed):
        document = json.loads(json.dumps(_fixtures.load("routing-matrix-valid.json")))
        document["changed_paths"] = list(changed)
        return routing.validate(document)

    def test_schema_only_runs_tools_and_skips_offline(self) -> None:
        result = self._matrix(["docs/instrumentation/workflow-outcomes-v1.schema.json"])
        self.assertTrue(result["valid"], result["issues"])
        self.assertTrue(result["docs_skills"])
        self.assertEqual(result["skipped_advisory"], ["windows-offline-checks"])
        for name in ("tools-tests-linux", "tools-tests-windows"):
            self.assertIn(
                name,
                result["affected_checks"]["docs/instrumentation/workflow-outcomes-v1.schema.json"],
            )
        self.assertNotIn(
            "windows-offline-checks",
            result["affected_checks"]["docs/instrumentation/workflow-outcomes-v1.schema.json"],
        )

    def test_docs_only_skips_all_advisory(self) -> None:
        result = self._matrix(["docs/operations/README.md"])
        self.assertTrue(result["valid"], result["issues"])
        self.assertTrue(result["docs_skills"])
        self.assertEqual(
            result["skipped_advisory"],
            ["tools-tests-linux", "tools-tests-windows", "windows-offline-checks"],
        )

    def test_mixed_docs_schema_runs_tools_and_skips_offline(self) -> None:
        result = self._matrix(
            [
                "docs/operations/README.md",
                "docs/instrumentation/workflow-outcomes-v1.schema.json",
            ]
        )
        self.assertTrue(result["valid"], result["issues"])
        self.assertTrue(result["docs_skills"])
        self.assertEqual(result["skipped_advisory"], ["windows-offline-checks"])
        self.assertIn(
            "tools-tests-linux",
            result["affected_checks"]["docs/instrumentation/workflow-outcomes-v1.schema.json"],
        )

    def test_docs_and_tools_run_tools_and_offline(self) -> None:
        result = self._matrix(
            ["docs/operations/README.md", "tools/aegis_ops/schema.py"]
        )
        self.assertTrue(result["valid"], result["issues"])
        self.assertFalse(result["docs_skills"])
        self.assertEqual(result["skipped_advisory"], [])

    def test_offline_only_runs_offline_and_skips_tools(self) -> None:
        result = self._matrix(["requirements-ci.txt"])
        self.assertTrue(result["valid"], result["issues"])
        self.assertFalse(result["docs_skills"])
        self.assertEqual(
            result["skipped_advisory"],
            ["tools-tests-linux", "tools-tests-windows"],
        )
        self.assertIn(
            "windows-offline-checks", result["affected_checks"]["requirements-ci.txt"]
        )

    def test_path_matching(self) -> None:
        self.assertTrue(routing.path_matches("tools/**", "tools/aegis_ops/x.py"))
        self.assertTrue(routing.path_matches("tools/**", "tools"))
        self.assertFalse(routing.path_matches("tools/**", "docs/x.md"))
        self.assertTrue(routing.path_matches("**", "anything"))
        self.assertTrue(routing.path_matches("requirements-ci.txt", "requirements-ci.txt"))


class WorkflowTests(unittest.TestCase):
    def _workflow_text(self) -> str:
        return (_fixtures.ROOT / ".github" / "workflows" / "validate-skills.yml").read_text(
            encoding="utf-8"
        )

    def test_repository_workflow_matches_e1(self) -> None:
        result = routing.check_workflow_text(self._workflow_text())
        self.assertTrue(result["valid"], result["issues"])
        self.assertEqual(
            result["jobs"],
            [
                "changes",
                "gate-guard",
                "tools-tests-linux",
                "tools-tests-windows",
                "validate-skills",
                "windows-offline-checks",
            ],
        )

    def test_missing_docs_skills_is_refused(self) -> None:
        text = self._workflow_text()
        text = text.replace(
            "      docs_skills: $" + "{{ steps.filter.outputs.docs_skills }}\n", ""
        )
        text = text.replace("docs_skills=true\n", "")
        result = routing.check_workflow_text(text)
        self.assertFalse(result["valid"])
        codes = [issue["code"] for issue in result["issues"]]
        self.assertIn("E1_DOCS_SKILLS_OUTPUT", codes)

    def test_job_added_is_refused(self) -> None:
        text = self._workflow_text().replace(
            "  validate-skills:\n    runs-on: ubuntu-latest",
            "  extra-job:\n    runs-on: ubuntu-latest\n\n  validate-skills:\n    runs-on: ubuntu-latest",
        )
        result = routing.check_workflow_text(text)
        self.assertFalse(result["valid"])
        self.assertIn(
            "E1_JOB_SET_CHANGED", [issue["code"] for issue in result["issues"]]
        )

    def test_required_validate_conditional_is_refused(self) -> None:
        text = self._workflow_text().replace(
            "  validate-skills:\n    runs-on: ubuntu-latest",
            "  validate-skills:\n    if: github.event_name == 'push'\n    runs-on: ubuntu-latest",
        )
        result = routing.check_workflow_text(text)
        self.assertFalse(result["valid"])
        self.assertIn(
            "E1_REQUIRED_VALIDATE_CONDITIONAL",
            [issue["code"] for issue in result["issues"]],
        )

    def test_tools_condition_retaining_docs_skip_is_refused(self) -> None:
        fixed = "if: github.event_name == 'push' || needs.changes.outputs.tools == 'true'"
        old = (
            "if: github.event_name == 'push' || (needs.changes.outputs.tools == 'true' "
            "&& needs.changes.outputs.docs_skills != 'true')"
        )
        text = self._workflow_text().replace(fixed, old)
        self.assertEqual(text.count(old), 2)
        result = routing.check_workflow_text(text)
        self.assertFalse(result["valid"])
        codes = [issue["code"] for issue in result["issues"]]
        self.assertIn("E1_ADVISORY_TOOLS_DOCS_SKIP", codes)
        self.assertNotIn("E1_ADVISORY_DOCS_SKIP", codes)

    def test_offline_without_docs_skip_is_refused(self) -> None:
        fixed = (
            "if: github.event_name == 'push' || (needs.changes.outputs.offline == 'true' "
            "&& needs.changes.outputs.docs_skills != 'true')"
        )
        no_skip = "if: github.event_name == 'push' || needs.changes.outputs.offline == 'true'"
        text = self._workflow_text().replace(fixed, no_skip)
        self.assertEqual(text.count(fixed), 0)
        result = routing.check_workflow_text(text)
        self.assertFalse(result["valid"])
        self.assertIn(
            "E1_ADVISORY_DOCS_SKIP", [issue["code"] for issue in result["issues"]]
        )

    def test_malformed_multiline_condition_does_not_false_pass(self) -> None:
        fixed = "if: github.event_name == 'push' || needs.changes.outputs.tools == 'true'"
        folded = (
            "if: >-\n"
            "      github.event_name == 'push' ||\n"
            "      needs.changes.outputs.tools == 'true' &&\n"
            "      needs.changes.outputs.docs_skills != 'true'"
        )
        text = self._workflow_text().replace(fixed, folded, 1)
        result = routing.check_workflow_text(text)
        self.assertFalse(result["valid"])
        codes = [issue["code"] for issue in result["issues"]]
        self.assertIn("E1_ADVISORY_PUSH_LANE", codes)
        self.assertIn("E1_ADVISORY_TOOLS_DOCS_SKIP", codes)

    def test_unpinned_action_is_refused(self) -> None:
        text = self._workflow_text().replace(
            "actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1",
            "actions/checkout@v4",
        )
        result = routing.check_workflow_text(text)
        self.assertFalse(result["valid"])
        self.assertIn(
            "E1_ACTION_UNPINNED", [issue["code"] for issue in result["issues"]]
        )


if __name__ == "__main__":
    unittest.main()
