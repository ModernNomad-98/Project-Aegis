"""Runtime-file classification and fail-closed ambiguity (areas 7, 8)."""

from __future__ import annotations

import unittest

from tools.behavioral_eval_runner.enums import RuntimeClassification
from tools.behavioral_eval_runner.errors import ClassificationError
from tools.behavioral_eval_runner.runtime_surface import agent_visible, classify_skill_file, classify_skill_package


class TestClassificationRules(unittest.TestCase):
    def test_all_evals_content_control_plane(self) -> None:
        for path in (
            "evals/evals.json",
            "evals/trigger-evals.json",
            "evals/helper-notes.md",
            "evals/sub/inner.txt",
        ):
            self.assertIs(
                classify_skill_file(path).classification,
                RuntimeClassification.CONTROL_PLANE_ONLY,
                path,
            )

    def test_eval_files_control_plane_wherever_they_appear(self) -> None:
        self.assertIs(
            classify_skill_file("references/evals.json").classification,
            RuntimeClassification.CONTROL_PLANE_ONLY,
        )

    def test_expected_answers_rubrics_manifests_control_plane(self) -> None:
        for path in (
            "references/grading-rubric.md",
            "assets/answer-bank.json",
            "references/expected-answers.md",
            "assets/case-manifest.json",
            "references/result-expectations.md",
        ):
            self.assertIs(
                classify_skill_file(path).classification,
                RuntimeClassification.CONTROL_PLANE_ONLY,
                path,
            )

    def test_skill_md_is_runtime_required(self) -> None:
        self.assertIs(
            classify_skill_file("SKILL.md").classification,
            RuntimeClassification.RUNTIME_REQUIRED,
        )

    def test_legitimate_runtime_material(self) -> None:
        for path in (
            "references/blueprint.md",
            "references/checklist.md",
            "assets/report-template.md",
            "scripts/helper.py",
            "assets/example.csv",
        ):
            self.assertIs(
                classify_skill_file(path).classification,
                RuntimeClassification.RUNTIME_REQUIRED,
                path,
            )

    def test_unknown_files_fail_closed_to_ambiguous(self) -> None:
        for path in (
            "notes.md",  # unrecognized location, even with a known extension
            "references/blob.bin",  # unrecognized shape in a runtime dir
            "data/mystery.md",  # unrecognized directory
            "SKILLS.md",  # near-miss of the entry point
        ):
            classified = classify_skill_file(path)
            self.assertIs(
                classified.classification,
                RuntimeClassification.AMBIGUOUS_NEEDS_OWNER_REVIEW,
                path,
            )
            self.assertFalse(agent_visible(classified.classification), path)

    def test_extension_alone_never_decides(self) -> None:
        """Same extension, different classification by role/context."""
        results = {
            path: classify_skill_file(path).classification
            for path in (
                "references/guide.md",  # runtime
                "evals/guide.md",  # control plane
                "guide.md",  # ambiguous
            )
        }
        self.assertEqual(len(set(results.values())), 3, results)

    def test_traversal_segments_rejected(self) -> None:
        for path in ("../SKILL.md", "references/../../etc", "./x", ""):
            with self.assertRaises(ClassificationError):
                classify_skill_file(path)

    def test_package_classification_deterministic_order(self) -> None:
        paths = ["b.md", "SKILL.md", "evals/evals.json", "references/a.md"]
        first = classify_skill_package(paths)
        second = classify_skill_package(list(reversed(paths)))
        self.assertEqual(
            [item.relative_path for item in first],
            [item.relative_path for item in second],
        )


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
