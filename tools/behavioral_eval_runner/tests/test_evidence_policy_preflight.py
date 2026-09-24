"""Synthetic host assertions never become a real-host attestation."""

from __future__ import annotations

import unittest
from dataclasses import replace
from unittest.mock import patch

from tools.behavioral_eval_runner.evidence_policy_preflight import (
    SyntheticHostFacts,
    evaluate_synthetic_host_facts,
)


def complete_facts() -> SyntheticHostFacts:
    return SyntheticHostFacts(
        expected_path="/synthetic-root-1",
        asserted_path="/synthetic-root-1",
        path_owned=True,
        acl_restricted=True,
        inheritance_disabled=True,
        encryption_enabled=True,
        recovery_key_custody_confirmed=True,
    )


class TestSyntheticEvidencePolicyPreflight(unittest.TestCase):
    def test_missing_facts_stop_with_sanitized_reasons(self) -> None:
        result = evaluate_synthetic_host_facts(SyntheticHostFacts())
        self.assertEqual(result.status, "STOP")
        self.assertEqual(result.reasons, (
            "EXACT_PATH_UNKNOWN", "OWNERSHIP_UNKNOWN", "ACL_UNKNOWN",
            "INHERITANCE_UNKNOWN", "ENCRYPTION_UNKNOWN", "RECOVERY_KEY_UNKNOWN",
        ))
        self.assertEqual(result.to_dict(), {
            "status": "STOP", "reasons": list(result.reasons),
        })

    def test_every_false_fact_stops(self) -> None:
        for field, reason in (
            ("path_owned", "OWNERSHIP_FALSE"),
            ("acl_restricted", "ACL_FALSE"),
            ("inheritance_disabled", "INHERITANCE_FALSE"),
            ("encryption_enabled", "ENCRYPTION_FALSE"),
            ("recovery_key_custody_confirmed", "RECOVERY_KEY_FALSE"),
        ):
            with self.subTest(field=field):
                result = evaluate_synthetic_host_facts(replace(complete_facts(), **{field: False}))
                self.assertEqual(result.status, "STOP")
                self.assertIn(reason, result.reasons)

    def test_conflicting_path_and_property_claims_stop(self) -> None:
        path = replace(complete_facts(), asserted_path="/other-synthetic-root")
        self.assertEqual(evaluate_synthetic_host_facts(path).reasons, ("EXACT_PATH_CONFLICT",))
        for field in (
            "path_owned", "acl_restricted", "inheritance_disabled",
            "encryption_enabled", "recovery_key_custody_confirmed",
        ):
            with self.subTest(field=field):
                result = evaluate_synthetic_host_facts(
                    replace(complete_facts(), **{field: (True, False)})
                )
                self.assertEqual(result.status, "STOP")
                self.assertIn("CONFLICT", result.reasons[0])

    def test_relative_ambiguous_and_volume_root_paths_stop(self) -> None:
        for path in (
            ".", "synthetic-root-1", "../synthetic-root-1", "/",
            "/synthetic/./root", "/synthetic/../root", "/synthetic//root",
            "C:synthetic\\root", "C:\\", "C:\\synthetic\\..\\root",
            "C:/synthetic/root", "\\\\server\\share\\root",
        ):
            with self.subTest(path=path):
                facts = replace(complete_facts(), expected_path=path, asserted_path=path)
                self.assertEqual(evaluate_synthetic_host_facts(facts).reasons,
                                 ("EXACT_PATH_INVALID",))

    def test_normalized_absolute_windows_path_is_simulation_only(self) -> None:
        facts = replace(complete_facts(), expected_path="C:\\synthetic\\root",
                        asserted_path="C:\\synthetic\\root")
        self.assertEqual(evaluate_synthetic_host_facts(facts).status, "SIMULATION_ONLY")

    def test_unknown_and_malformed_claims_stop(self) -> None:
        for claim in (None, (), (True, None), "true", 1, [True]):
            with self.subTest(claim=claim):
                result = evaluate_synthetic_host_facts(
                    replace(complete_facts(), acl_restricted=claim)
                )
                self.assertEqual(result.status, "STOP")
                self.assertTrue(result.reasons[0].startswith("ACL_"))
        self.assertEqual(evaluate_synthetic_host_facts(None).reasons, ("FACTS_INVALID",))

    def test_complete_assertions_are_only_simulation(self) -> None:
        facts = complete_facts()
        with patch("os.stat", side_effect=AssertionError("host probe")), \
             patch("os.listdir", side_effect=AssertionError("host probe")):
            result = evaluate_synthetic_host_facts(facts)
        self.assertEqual(result.status, "SIMULATION_ONLY")
        self.assertEqual(result.reasons, ())
        self.assertEqual(result.to_dict(), {"status": "SIMULATION_ONLY", "reasons": []})
        self.assertNotIn(facts.expected_path, str(result.to_dict()))


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
