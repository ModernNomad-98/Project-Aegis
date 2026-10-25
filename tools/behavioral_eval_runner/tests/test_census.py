"""Census reproducibility, expected baseline, MANUAL-ONLY parsing, typed
targets (areas 4, 5, 6)."""

from __future__ import annotations

import json
import unittest

from tools.behavioral_eval_runner import (
    AUTHORIZATION_MERGE_SHA,
    CENSUS_RUNNER_VERSION,
    CENSUS_SCHEMA_VERSION,
    RUNNER_VERSION,
    SCHEMA_VERSION,
    SCHEDULING_POLICY_VERSION,
)
from tools.behavioral_eval_runner.canonical import canonical_bytes
from tools.behavioral_eval_runner.census import (
    EXPECTED_PINNED_BASELINE,
    MANUAL_ONLY_SENTINEL,
    build_census,
    is_manual_only,
    parse_frontmatter,
    validate_census_record,
    verify_expected_baseline,
)
from tools.behavioral_eval_runner.enums import TargetKind
from tools.behavioral_eval_runner.errors import (
    CensusBaselineMismatchError,
    SchemaValidationError,
)
from tools.behavioral_eval_runner.materialize import SyntheticSnapshot
from tools.behavioral_eval_runner.models import parse_target
from tools.behavioral_eval_runner.tests.helpers import REPO_ROOT, synthetic_corpus_files

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
            # C3: keys are TYPED (skill::name / subagent::name).
            self.assertRegex(target, r"^(skill|subagent)::.+")

    def test_reverse_index_keeps_skill_and_subagent_distinct(self) -> None:
        reverse = _census()["reverse_negative_neighbor_index"]
        # release-readiness-reviewer exists as BOTH a skill and a subagent;
        # both typed keys must be present and distinct.
        self.assertIn("subagent::release-readiness-reviewer", reverse)
        self.assertIn("skill::release-readiness-reviewer", reverse)

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



def _trigger_cases_files(trigger_cases: list[dict]) -> dict[str, bytes]:
    """Synthetic corpus with skill-a's trigger-evals replaced by test cases."""
    files = dict(synthetic_corpus_files())
    files[".claude/skills/skill-a/evals/trigger-evals.json"] = json.dumps(
        {
            "skill": "skill-a",
            "overlaps_with": ["skill-b"],
            "cases": trigger_cases,
        }
    ).encode("utf-8")
    return files


def _census_for(trigger_cases: list[dict]) -> dict:
    return build_census(
        REPO_ROOT,
        "synthetic",
        snapshot=SyntheticSnapshot(_trigger_cases_files(trigger_cases)),
    )


class TestVersionRegistration(unittest.TestCase):
    """PKG-04 REV-3: the additive census shape is a registered version."""

    def test_registered_version_constants(self) -> None:
        # The exact strings are the registration for the additive census shape;
        # docs/behavioral-eval-runner-schema-compatibility.md names the same
        # values. A later bump must update both together.
        self.assertEqual(CENSUS_SCHEMA_VERSION, "1.1.0-census-wp2b1")
        self.assertEqual(CENSUS_RUNNER_VERSION, "0.2.0-census-wp2b1")
        # The additive change is scoped to the census record family: the
        # WP-2B-1 result/evidence family and the scheduling policy are
        # unchanged, because no other published record shape changed.
        self.assertEqual(SCHEMA_VERSION, "1.0.0-wp2b1")
        self.assertEqual(RUNNER_VERSION, "0.1.0-wp2b1")
        self.assertEqual(SCHEDULING_POLICY_VERSION, "1.0.0-wp2b1")

    def test_pinned_census_carries_registered_versions(self) -> None:
        census = _census()
        self.assertEqual(census["schema_version"], CENSUS_SCHEMA_VERSION)
        self.assertEqual(census["runner_version"], CENSUS_RUNNER_VERSION)

    def test_pinned_baseline_registers_zero_route_cases(self) -> None:
        self.assertEqual(EXPECTED_PINNED_BASELINE["documentation_route_cases"], 0)
        census = _census()
        verify_expected_baseline(census)  # includes the zero route-case check
        self.assertEqual(census["totals"]["documentation_route_cases"], 0)
        self.assertEqual(census["documentation_route_cases"], [])

class TestDocumentationRouteCases(unittest.TestCase):
    """Documented-route negatives are non-skill cases, never fake skills."""

    TRIGGER_PATH = ".claude/skills/skill-a/evals/trigger-evals.json"

    def _census(self, trigger_cases: list[dict]) -> dict:
        return _census_for(trigger_cases)

    def test_route_case_is_recorded_without_fake_skill_or_activation_edge(
        self,
    ) -> None:
        census = self._census(
            [
                {
                    "id": "route-case-1",
                    "prompt": "List the shipped meta skills and where each is documented.",
                    "expected_route": "docs/skills-catalog.md",
                    "should_not_trigger": ["skill-b"],
                    "reason": "Catalogue lookup is a documentation route.",
                }
            ]
        )
        self.assertEqual(census["totals"]["documentation_route_cases"], 1)
        self.assertEqual(census["totals"]["discrimination_cases"], 1)
        routes = census["documentation_route_cases"]
        self.assertEqual(len(routes), 1)
        self.assertEqual(routes[0]["owner"], "skill-a")
        self.assertEqual(routes[0]["route"], "docs/skills-catalog.md")
        self.assertIn("::", routes[0]["case_uid"])
        reverse = census["reverse_negative_neighbor_index"]
        self.assertIn("skill::skill-b", reverse)
        self.assertFalse(
            [key for key in reverse if "docs/" in key or "route" in key]
        )
        entry = {s["skill"]: s for s in census["skills"]}["skill-a"]
        self.assertEqual(entry["documentation_route_cases"], 1)
        self.assertEqual(entry["discrimination_cases"], 1)

    def test_expected_skill_case_is_unchanged(self) -> None:
        census = self._census(
            [
                {
                    "id": "skill-case-1",
                    "prompt": "Route this to the neighbouring skill.",
                    "expected_skill": "skill-b",
                    "should_not_trigger": ["skill-a"],
                    "reason": "Activation target case.",
                }
            ]
        )
        self.assertEqual(census["totals"]["documentation_route_cases"], 0)
        self.assertEqual(census["documentation_route_cases"], [])
        reverse = census["reverse_negative_neighbor_index"]
        self.assertIn("skill::skill-b", reverse)
        # The owning skill's own name is not a negative-neighbour edge for its
        # own file, so no skill::skill-a self-edge is created by this case.
        self.assertNotIn("skill::skill-a", reverse)

    def test_missing_target_and_route_fails_closed_with_owning_case(self) -> None:
        with self.assertRaises(SchemaValidationError) as raised:
            self._census([{"id": "broken-case-1", "prompt": "p"}])
        message = str(raised.exception)
        self.assertIn("broken-case-1", message)
        self.assertIn("trigger-evals.json", message)
        self.assertIn("expected_skill", message)
        self.assertIn("expected_route", message)

    def test_both_target_and_route_fails_closed(self) -> None:
        with self.assertRaises(SchemaValidationError) as raised:
            self._census(
                [
                    {
                        "id": "ambiguous-case-1",
                        "prompt": "p",
                        "expected_skill": "skill-b",
                        "expected_route": "docs/skills-catalog.md",
                    }
                ]
            )
        self.assertIn("ambiguous-case-1", str(raised.exception))
        self.assertIn("both expected_skill and expected_route", str(raised.exception))

    def test_missing_case_id_is_named_in_diagnostic(self) -> None:
        # R3-DS-11: absent id must not print as None; use a stable marker.
        with self.assertRaises(SchemaValidationError) as raised:
            self._census([{"prompt": "p"}])
        self.assertIn("<missing id>", str(raised.exception))

    def test_pinned_snapshot_has_no_route_cases(self) -> None:
        census = _census()
        self.assertEqual(census["totals"]["documentation_route_cases"], 0)
        self.assertEqual(census["documentation_route_cases"], [])


class TestTriggerCaseFailClosed(unittest.TestCase):
    """Exactly one present non-blank key; diagnostics carry the owning case."""

    TRIGGER_PATH = ".claude/skills/skill-a/evals/trigger-evals.json"

    def _census(self, trigger_cases: list[dict]) -> dict:
        return _census_for(trigger_cases)

    def _assert_owns_case(self, case_id: str, exc: Exception) -> None:
        message = str(exc)
        self.assertIn(case_id, message)
        self.assertIn(self.TRIGGER_PATH, message)

    def test_present_but_blank_expected_skill_fails_closed(self) -> None:
        with self.assertRaises(SchemaValidationError) as raised:
            self._census(
                [{"id": "blank-skill", "prompt": "p", "expected_skill": "   "}]
            )
        self._assert_owns_case("blank-skill", raised.exception)
        self.assertIn("blank expected_skill", str(raised.exception))

    def test_present_but_blank_expected_route_fails_closed(self) -> None:
        with self.assertRaises(SchemaValidationError) as raised:
            self._census(
                [{"id": "blank-route", "prompt": "p", "expected_route": ""}]
            )
        self._assert_owns_case("blank-route", raised.exception)
        self.assertIn("blank expected_route", str(raised.exception))

    def test_both_keys_with_blank_counterpart_fails_closed(self) -> None:
        with self.assertRaises(SchemaValidationError) as raised:
            self._census(
                [
                    {
                        "id": "blank-counterpart",
                        "prompt": "p",
                        "expected_skill": "",
                        "expected_route": "docs/skills-catalog.md",
                    }
                ]
            )
        self._assert_owns_case("blank-counterpart", raised.exception)
        self.assertIn("both expected_skill and expected_route", str(raised.exception))

    def test_non_string_skill_diagnostic_owns_case(self) -> None:
        with self.assertRaises(SchemaValidationError) as raised:
            self._census(
                [{"id": "typed-skill", "prompt": "p", "expected_skill": 7}]
            )
        self._assert_owns_case("typed-skill", raised.exception)
        self.assertIn("non-string expected_skill", str(raised.exception))

    def test_malformed_non_blank_expected_skill_owns_case(self) -> None:
        # R3-DS-2: parse_target rejects an annotated target with no name; the
        # error must carry the owning file and case id, not escape bare.
        with self.assertRaises(SchemaValidationError) as raised:
            self._census(
                [{"id": "malformed-skill", "prompt": "p",
                  "expected_skill": " (subagent)"}]
            )
        self._assert_owns_case("malformed-skill", raised.exception)
        self.assertIn("malformed expected_skill", str(raised.exception))

    def test_expected_skill_trimming_is_explicit_and_documented(self) -> None:
        # R3-DS-7: the existing parse_target contract trims surrounding
        # whitespace; reverse-index keys use the parsed (trimmed) name.
        census = self._census(
            [{"id": "spaced-skill", "prompt": "p",
              "expected_skill": "  skill-b  "}]
        )
        reverse = census["reverse_negative_neighbor_index"]
        self.assertIn("skill::skill-b", reverse)
        self.assertNotIn("skill::  skill-b  ", reverse)

    def test_authored_route_is_preserved_exactly(self) -> None:
        authored = "  docs/skills-catalog.md#anchor  "
        census = self._census(
            [{"id": "spaced-route", "prompt": "p", "expected_route": authored}]
        )
        routes = census["documentation_route_cases"]
        self.assertEqual(len(routes), 1)
        self.assertEqual(routes[0]["route"], authored)
        self.assertEqual(census["totals"]["documentation_route_cases"], 1)

    def test_route_shape_heuristic(self) -> None:
        # R3-DS-6: reject schemes/absolute/empty-segment routes; accept a
        # top-level repository document such as README.md.
        for route in (
            "/",
            "//",
            "skill-b/",
            "https://example.com",
            "docs//x.md",
        ):
            with self.subTest(route=route):
                with self.assertRaises(SchemaValidationError):
                    self._census([{"id": "bad-shape", "prompt": "p",
                                   "expected_route": route}])
        census = self._census(
            [{"id": "readme-route", "prompt": "p",
              "expected_route": "README.md"}]
        )
        self.assertEqual(census["documentation_route_cases"][0]["route"], "README.md")

    def test_route_case_excluded_from_proposed_runnable_denominator(self) -> None:
        route_census = self._census(
            [{"id": "route-denominator", "prompt": "p",
              "expected_route": "docs/skills-catalog.md"}]
        )
        target_census = self._census(
            [{"id": "target-denominator", "prompt": "p",
              "expected_skill": "skill-b"}]
        )
        route_count = route_census["honest_denominator"][
            "proposed_empty_consumer_runnable_single_prompt_cases"]
        target_count = target_census["honest_denominator"][
            "proposed_empty_consumer_runnable_single_prompt_cases"]
        self.assertEqual(target_count, route_count + 1)
        self.assertIn(
            "excluded from the proposed-empty-consumer-runnable",
            route_census["honest_denominator"]["note"],
        )


class TestCensusRecordRoundTripAndVersionGating(unittest.TestCase):
    """R3-DS-1/R3-DS-3: serialized census record survives a round trip and
    only the registered census version family is accepted."""

    def test_round_trip_with_canonical_bytes(self) -> None:
        census = _census()
        payload = json.loads(canonical_bytes(census))
        validate_census_record(payload)

    def test_missing_old_and_unknown_versions_fail_closed(self) -> None:
        census = _census()
        for mutation, label in (
            (lambda p: p.pop("schema_version"), "missing schema_version"),
            (lambda p: p.update({"schema_version": "1.0.0-wp2b1"}),
             "old schema_version"),
            (lambda p: p.update({"schema_version": "9.9.9-census-wp2b1"}),
             "unknown schema_version"),
            (lambda p: p.pop("runner_version"), "missing runner_version"),
            (lambda p: p.update({"runner_version": "0.1.0-wp2b1"}),
             "old runner_version"),
        ):
            with self.subTest(label=label):
                payload = json.loads(canonical_bytes(census))
                mutation(payload)
                with self.assertRaises(SchemaValidationError):
                    validate_census_record(payload)

    def test_registered_versions_are_the_census_family(self) -> None:
        payload = json.loads(canonical_bytes(_census()))
        self.assertEqual(payload["schema_version"], CENSUS_SCHEMA_VERSION)
        self.assertEqual(payload["runner_version"], CENSUS_RUNNER_VERSION)
        # The package-wide WP-2B-1 family is unchanged by the census family.
        self.assertEqual(SCHEMA_VERSION, "1.0.0-wp2b1")
        self.assertEqual(RUNNER_VERSION, "0.1.0-wp2b1")


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
