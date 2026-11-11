"""C3.5: explicit inbox configuration and disabled zero-activity evidence.

Covers AC-C3.5-1 to AC-C3.5-7 at the record-validation level.
"""

from __future__ import annotations

import copy
import unittest

from tools.aegis_ops import inbox_activity, schema

import _fixtures


class InboxTests(unittest.TestCase):
    def test_disabled_valid(self) -> None:
        result = inbox_activity.validate(_fixtures.load("inbox-disabled-valid.json"))
        self.assertTrue(result["valid"], result["issues"])
        self.assertFalse(result["blocked"])
        self.assertFalse(result["enabled"])
        self.assertTrue(result["zero_activity_observed"])
        self.assertNotIn("approved", result["display_state"].lower())

    def test_invalid_config_value_refused(self) -> None:
        result = inbox_activity.validate(_fixtures.load("inbox-invalid-value.json"))
        self.assertFalse(result["valid"])
        self.assertIn(
            "INBOX_CONFIG_INVALID",
            [issue["code"] for issue in result["issues"]],
        )

    def test_hidden_activity_refused(self) -> None:
        result = inbox_activity.validate(
            _fixtures.load("inbox-zero-activity-evidence.json")
        )
        self.assertFalse(result["valid"])
        codes = [issue["code"] for issue in result["issues"]]
        self.assertIn("INBOX_HIDDEN_ACTIVITY", codes)
        self.assertIn("INBOX_ZERO_ACTIVITY_UNPROVEN", codes)

    def test_enabled_without_authority_refused(self) -> None:
        document = _fixtures.load("inbox-disabled-valid.json")
        document["config"] = {"inbox.supported": True, "inbox.enabled": True}
        document["config_identity"] = schema.digest(document["config"])
        result = inbox_activity.validate(document)
        self.assertFalse(result["valid"])
        self.assertIn(
            "INBOX_ENABLED_WITHOUT_AUTHORITY",
            [issue["code"] for issue in result["issues"]],
        )

    def test_identity_mismatch_refused(self) -> None:
        document = _fixtures.load("inbox-disabled-valid.json")
        document["config_identity"] = "0" * 64
        result = inbox_activity.validate(document)
        self.assertFalse(result["valid"])
        self.assertIn(
            "INBOX_CONFIG_IDENTITY_MISMATCH",
            [issue["code"] for issue in result["issues"]],
        )

    def test_new_dependency_refused(self) -> None:
        document = _fixtures.load("inbox-disabled-valid.json")
        document["dependencies"] = ["queue-service"]
        result = inbox_activity.validate(document)
        self.assertFalse(result["valid"])
        self.assertIn(
            "INBOX_NEW_DEPENDENCY",
            [issue["code"] for issue in result["issues"]],
        )

    def test_static_config_is_not_zero_activity_evidence(self) -> None:
        document = _fixtures.load("inbox-disabled-valid.json")
        document["evidence"]["kind"] = "STATIC_CONFIG_ONLY"
        result = inbox_activity.validate(document)
        self.assertFalse(result["valid"])
        self.assertIn(
            "INBOX_EVIDENCE_NOT_END_TO_END",
            [issue["code"] for issue in result["issues"]],
        )

    def test_wrong_display_refused(self) -> None:
        document = _fixtures.load("inbox-disabled-valid.json")
        document["display_state"] = "inbox disabled - approved"
        result = inbox_activity.validate(document)
        self.assertFalse(result["valid"])
        codes = [issue["code"] for issue in result["issues"]]
        self.assertIn("INBOX_DISPLAY_INVALID", codes)

    def test_local_path_evidence_required(self) -> None:
        document = _fixtures.load("inbox-disabled-valid.json")
        document["local_path_evidence"] = ""
        result = inbox_activity.validate(document)
        self.assertFalse(result["valid"])
        self.assertIn(
            "SCHEMA_EMPTY_STRING",
            [issue["code"] for issue in result["issues"]],
        )


if __name__ == "__main__":
    unittest.main()
