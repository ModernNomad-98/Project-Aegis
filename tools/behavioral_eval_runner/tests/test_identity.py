"""Case/assertion identity behavior (area 3; design §13/§20a-S25)."""

from __future__ import annotations

import unittest

from tools.behavioral_eval_runner.enums import EvalFileKind
from tools.behavioral_eval_runner.errors import IdentityError
from tools.behavioral_eval_runner.identity import (
    attempt_identity,
    build_assertion_uid,
    build_case_uid,
    parse_case_uid,
)


class TestCaseUid(unittest.TestCase):
    def test_changed_case_definition_changes_case_uid(self) -> None:
        base = {"id": "c1", "prompt": "original", "expect": {"triggers": True}}
        edited = {"id": "c1", "prompt": "edited", "expect": {"triggers": True}}
        uid_base = build_case_uid("owner", EvalFileKind.BEHAVIOR_EVAL, "c1", base)
        uid_edit = build_case_uid("owner", EvalFileKind.BEHAVIOR_EVAL, "c1", edited)
        self.assertNotEqual(uid_base, uid_edit)

    def test_identical_definition_is_stable(self) -> None:
        definition = {"id": "c1", "prompt": "p", "expect": {"assertions": ["a", "b"]}}
        first = build_case_uid("owner", "behavior_eval", "c1", definition)
        second = build_case_uid("owner", "behavior_eval", "c1", dict(definition))
        self.assertEqual(first, second)

    def test_same_case_id_different_owner_or_kind_distinct(self) -> None:
        definition = {"id": "c1"}
        self.assertNotEqual(
            build_case_uid("owner-a", "behavior_eval", "c1", definition),
            build_case_uid("owner-b", "behavior_eval", "c1", definition),
        )
        self.assertNotEqual(
            build_case_uid("owner-a", "behavior_eval", "c1", definition),
            build_case_uid("owner-a", "trigger_eval", "c1", definition),
        )

    def test_parse_roundtrip(self) -> None:
        uid = build_case_uid("owner", "trigger_eval", "case-x", {"id": "case-x"})
        parts = parse_case_uid(uid)
        self.assertEqual(parts.target_owner, "owner")
        self.assertIs(parts.eval_file_kind, EvalFileKind.TRIGGER_EVAL)
        self.assertEqual(parts.case_id, "case-x")
        self.assertEqual(len(parts.definition_hash), 64)

    def test_components_may_not_contain_separator(self) -> None:
        with self.assertRaises(IdentityError):
            build_case_uid("owner::evil", "behavior_eval", "c1", {})
        with self.assertRaises(IdentityError):
            build_case_uid("owner", "behavior_eval", "c::1", {"id": "x"})


class TestAssertionUid(unittest.TestCase):
    def test_identical_text_in_different_cases_distinct(self) -> None:
        """Context changes meaning: text-only keying is forbidden (§20a-S25)."""
        text = "Refuses the unsafe shortcut and says why."
        uid_case_a = build_case_uid("owner-a", "behavior_eval", "c1", {"id": "c1"})
        uid_case_b = build_case_uid("owner-b", "behavior_eval", "c9", {"id": "c9"})
        self.assertNotEqual(
            build_assertion_uid(uid_case_a, 0, text),
            build_assertion_uid(uid_case_b, 0, text),
        )

    def test_index_participates(self) -> None:
        uid = build_case_uid("owner", "behavior_eval", "c1", {"id": "c1"})
        self.assertNotEqual(
            build_assertion_uid(uid, 0, "same"), build_assertion_uid(uid, 1, "same")
        )

    def test_case_edit_invalidates_assertion_uids(self) -> None:
        text = "assertion text"
        uid_before = build_case_uid("o", "behavior_eval", "c", {"prompt": "v1"})
        uid_after = build_case_uid("o", "behavior_eval", "c", {"prompt": "v2"})
        self.assertNotEqual(
            build_assertion_uid(uid_before, 0, text),
            build_assertion_uid(uid_after, 0, text),
        )


class TestAttemptIdentity(unittest.TestCase):
    def test_identity_tuple(self) -> None:
        uid = build_case_uid("o", "behavior_eval", "c", {"id": "c"})
        identity = attempt_identity("run-1", uid, 3)
        self.assertEqual(identity, ("run-1", uid, 3))

    def test_repetition_must_be_positive(self) -> None:
        uid = build_case_uid("o", "behavior_eval", "c", {"id": "c"})
        for bad in (0, -1, True, "1"):
            with self.assertRaises(IdentityError):
                attempt_identity("run-1", uid, bad)  # type: ignore[arg-type]


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
