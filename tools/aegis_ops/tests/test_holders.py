"""C3.4: active holder, replacement, unavailability and context bundle.

Covers AC-C3.4-1 to AC-C3.4-9 at the record-validation level.
"""

from __future__ import annotations

import copy
import json
import unittest

from tools.aegis_ops import holders

import _fixtures


class HolderTests(unittest.TestCase):
    def test_valid_holder_and_resume_bundle(self) -> None:
        result = holders.validate(_fixtures.load("holder-valid.json"))
        self.assertTrue(result["valid"], result["issues"])
        self.assertFalse(result["blocked"])
        self.assertEqual(result["active_holders"], {"D": ["h-1"]})
        self.assertEqual(result["overall_state"], "ACTIVE")
        document = _fixtures.load("holder-valid.json")
        bundle = document["context_bundles"][0]
        for field in (
            "candidate_id",
            "stage",
            "head_sha",
            "tree_sha",
            "base_sha",
            "verdict_refs",
            "deadline",
            "unrun",
            "next_action",
            "context_bundle_sha256",
        ):
            self.assertIn(field, bundle)
        self.assertEqual(bundle["context_bundle_sha256"], holders.schema.digest(
            {key: value for key, value in bundle.items() if key != "context_bundle_sha256"}
        ))

    def test_duplicate_active_holder_refused(self) -> None:
        result = holders.validate(_fixtures.load("holder-duplicate-active.json"))
        self.assertFalse(result["valid"])
        self.assertIn(
            "DUPLICATE_ACTIVE_HOLDER",
            [issue["code"] for issue in result["issues"]],
        )
        self.assertEqual(result["overall_state"], "BLOCKED")

    def test_valid_replacement_marks_old_holder(self) -> None:
        result = holders.validate(_fixtures.load("replacement-valid.json"))
        self.assertTrue(result["valid"], result["issues"])
        self.assertFalse(result["blocked"])
        self.assertEqual(result["active_holders"], {"D": ["h-new"]})
        document = _fixtures.load("replacement-valid.json")
        old = [h for h in document["holders"] if h["holder_id"] == "h-old"][0]
        self.assertTrue(old["state"] in ("REPLACED", "SUPERSEDED"))
        self.assertEqual(document["replacements"][0]["context_bundle_sha256"], document["context_bundles"][0]["context_bundle_sha256"])

    def test_replacement_missing_authority_refused(self) -> None:
        result = holders.validate(
            _fixtures.load("replacement-missing-authority.json")
        )
        self.assertFalse(result["valid"])
        codes = [issue["code"] for issue in result["issues"]]
        self.assertIn("SCHEMA_EMPTY_STRING", codes)
        self.assertIn("REPLACEMENT_AUTHORITY_INVALID", codes)

    def test_self_approved_replacement_refused(self) -> None:
        result = holders.validate(_fixtures.load("replacement-self-approve.json"))
        self.assertFalse(result["valid"])
        self.assertIn(
            "REPLACEMENT_SELF_APPROVAL",
            [issue["code"] for issue in result["issues"]],
        )

    def test_unavailability_without_t7_is_blocked(self) -> None:
        result = holders.validate(
            _fixtures.load("unavailability-no-t7-blocked.json")
        )
        self.assertTrue(result["valid"], result["issues"])
        self.assertTrue(result["blocked"])
        self.assertIn(
            "UNAVAILABLE_REVIEW_T7_OPEN:unavail-1", result["blockers"]
        )

    def test_context_bundle_mismatch_refused(self) -> None:
        result = holders.validate(_fixtures.load("context-bundle-mismatch.json"))
        self.assertFalse(result["valid"])
        self.assertIn(
            "BUNDLE_HASH_MISMATCH",
            [issue["code"] for issue in result["issues"]],
        )

    def test_invalidation_requires_rebind_and_suspends_holder(self) -> None:
        document = _fixtures.load("holder-valid.json")
        document["invalidation"] = {
            "head_moved": True,
            "base_moved": False,
            "policy_moved": False,
            "evidence_moved": False,
            "rebind_ref": None,
        }
        result = holders.validate(document)
        self.assertFalse(result["valid"])
        codes = [issue["code"] for issue in result["issues"]]
        self.assertIn("INVALIDATION_REBIND_MISSING", codes)
        self.assertIn("HOLDER_STALE_AFTER_MOVE", codes)
        document["invalidation"]["rebind_ref"] = "rebind-1"
        document["holders"][0]["state"] = "REPLACED"
        result = holders.validate(document)
        self.assertTrue(result["valid"], result["issues"])

    def test_head_budget_exception(self) -> None:
        document = _fixtures.load("holder-valid.json")
        document["head_budget"]["heads_used"] = 4
        result = holders.validate(document)
        self.assertFalse(result["valid"])
        self.assertIn(
            "HEAD_BUDGET_EXCEPTION_MISSING",
            [issue["code"] for issue in result["issues"]],
        )
        document["head_budget"]["exception_ref"] = "exception-1"
        document["head_budget"]["exception_basis"] = "R3 blocking finding"
        result = holders.validate(document)
        self.assertTrue(result["valid"], result["issues"])

    def test_component_owner_cannot_change(self) -> None:
        document = _fixtures.load("holder-valid.json")
        changed = copy.deepcopy(document["component_owner"])
        changed["owner_identity_ref"] = "someone-else"
        document["component_owner_after"] = changed
        result = holders.validate(document)
        self.assertFalse(result["valid"])
        self.assertIn(
            "COMPONENT_OWNER_CHANGED",
            [issue["code"] for issue in result["issues"]],
        )

    def test_status_is_deterministic_and_blocked_wins(self) -> None:
        valid = holders.validate(_fixtures.load("holder-valid.json"))
        duplicate = holders.validate(_fixtures.load("holder-duplicate-active.json"))
        self.assertEqual(valid["overall_state"], "ACTIVE")
        self.assertEqual(duplicate["overall_state"], "BLOCKED")
        self.assertEqual(
            json.dumps(valid["status"], sort_keys=True),
            json.dumps(valid["status"], sort_keys=True),
        )


if __name__ == "__main__":
    unittest.main()
