"""Census reproducibility, expected baseline, MANUAL-ONLY parsing, typed
targets (areas 4, 5, 6)."""

from __future__ import annotations

import unittest

from tools.behavioral_eval_runner import AUTHORIZATION_MERGE_SHA
from tools.behavioral_eval_runner.canonical import canonical_bytes
from tools.behavioral_eval_runner.census import (
    EXPECTED_PINNED_BASELINE,
    MANUAL_ONLY_SENTINEL,
    build_census,
    is_manual_only,
    parse_frontmatter,
    verify_expected_baseline,
)
from tools.behavioral_eval_runner.enums import TargetKind
from tools.behavioral_eval_runner.errors import CensusBaselineMismatchError
from tools.behavioral_eval_runner.models import parse_target
from tools.behavioral_eval_runner.tests.helpers import REPO_ROOT

#: One census over the pinned snapshot, shared across the class (read-only).
_CENSUS: dict | None = None


def _census() -> dict:
    global _CENSUS
    if _CENSUS is None:
        _CENSUS = build_census(REPO_ROOT, AUTHORIZATION_MERGE_SHA)
    return _CENSUS


class TestFrontmatterParsing(unittest.TestCase):
    def test_single_quoted_description_with_doubled_apostrophes(self) -> None:
        text = "---\nname: x\ndescription: 'it''s quoted: yes'\n---\nbody\n"
        fields = parse_frontmatter(text)
        self.assertEqual(fields["description"], "it's quoted: yes")

    def test_manual_only_sentinel_parsed_never_name_list(self) -> None:
        manual = (
            "---\nname: x\n"
            f"description: '{MANUAL_ONLY_SENTINEL}Does something with side effects.'\n"
            "disable-model-invocation: true\n---\n"
        )
        plain = "---\nname: y\ndescription: 'An ordinary read-only skill.'\n---\n"
        self.assertTrue(is_manual_only(parse_frontmatter(manual)))
        self.assertFalse(is_manual_only(parse_frontmatter(plain)))

    def test_flag_alone_counts_as_manual_only(self) -> None:
        text = (
            "---\nname: x\ndescription: 'Writes files.'\n"
            "disable-model-invocation: true\n---\n"
        )
        self.assertTrue(is_manual_only(parse_frontmatter(text)))


class TestTypedTargets(unittest.TestCase):
    def test_subagent_annotation_changes_kind(self) -> None:
        target = parse_target("release-readiness-reviewer (subagent)")
        self.assertIs(target.target_kind, TargetKind.SUBAGENT)
        self.assertEqual(target.target_name, "release-readiness-reviewer")
        self.assertEqual(target.target_annotation, "(subagent)")

    def test_plain_name_is_skill(self) -> None:
        target = parse_target("code-reviewer")
        self.assertIs(target.target_kind, TargetKind.SKILL)
        self.assertIsNone(target.target_annotation)


class TestPinnedCorpusCensus(unittest.TestCase):
    """Census over the REAL pinned snapshot (read-only Git objects)."""

    def test_expected_baseline_counts(self) -> None:
        census = _census()
        verify_expected_baseline(census)  # raises on any mismatch
        totals = census["totals"]
        for key, expected in EXPECTED_PINNED_BASELINE.items():
            self.assertEqual(totals[key], expected, key)

    def test_case_type_distribution_matches_design_census(self) -> None:
        types = _census()["totals"]["behavior_case_types"]
        self.assertEqual(types["should_trigger"], 690)
        self.assertEqual(types["should_not_trigger"], 190)
        self.assertEqual(types["should_not_do"], 2)

    def test_degenerate_and_subagent_findings(self) -> None:
        census = _census()
        self.assertEqual(len(census["empty_neighbor_cases"]), 3)
        self.assertEqual(len(census["subagent_target_cases"]), 4)
        self.assertEqual(census["totals"]["distinct_subagent_targets"], 2)
        for case in census["subagent_target_cases"]:
            self.assertTrue(case["subagent_definition_present"], case)

    def test_manual_only_parsed_from_frontmatter(self) -> None:
        census = _census()
        manual = census["manual_only_skills"]
        self.assertGreater(len(manual), 0)
        self.assertEqual(census["totals"]["manual_only_skills"], len(manual))

    def test_reverse_index_present_and_sorted(self) -> None:
        reverse = _census()["reverse_negative_neighbor_index"]
        self.assertGreater(len(reverse), 0)
        for target, uids in reverse.items():
            self.assertEqual(uids, sorted(uids), target)

    def test_risk_classes_are_proposed_not_ratified(self) -> None:
        census = _census()
        self.assertIn("PROPOSED / NOT OWNER-RATIFIED", census["governance"]["risk_classes_status"])
        distribution = census["totals"]["proposed_risk_class_distribution"]
        self.assertEqual(
            sum(distribution.values()),
            census["totals"]["authored_single_prompt_cases"],
        )

    def test_census_reproducible_byte_for_byte(self) -> None:
        first = _census()
        second = build_census(REPO_ROOT, AUTHORIZATION_MERGE_SHA)
        self.assertEqual(canonical_bytes(first), canonical_bytes(second))

    def test_baseline_mismatch_raises(self) -> None:
        broken = dict(_census())
        broken_totals = dict(broken["totals"])
        broken_totals["behavior_cases"] = 1
        broken["totals"] = broken_totals
        with self.assertRaises(CensusBaselineMismatchError):
            verify_expected_baseline(broken)

    def test_no_behavioral_result_language(self) -> None:
        governance = _census()["governance"]
        self.assertIn("no eval case was executed", governance["behavioral_results"])


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
