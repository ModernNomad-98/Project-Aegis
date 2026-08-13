"""Execution-profile unknowns and baseline-ineligibility (areas 16, 17)."""

from __future__ import annotations

import unittest

from tools.behavioral_eval_runner.errors import ProfileError
from tools.behavioral_eval_runner.execution_profile import (
    ExecutionProfile,
    RealClaudeCodeProfileSource,
    UNAVAILABLE,
    UNKNOWN,
    synthetic_isolated_profile,
)


class TestRealHostProfile(unittest.TestCase):
    def test_real_host_reports_unavailable_or_unknown_never_defaults(self) -> None:
        profile = RealClaudeCodeProfileSource().capture()
        for name in profile.unobserved_fields():
            self.assertIn(getattr(profile, name), (UNAVAILABLE, UNKNOWN), name)
        # Every required field is unobserved on the real host in WP-2B-1 (R5).
        self.assertEqual(len(profile.unobserved_fields()), 16)

    def test_real_host_never_baseline_eligible(self) -> None:
        profile = RealClaudeCodeProfileSource().capture()
        self.assertFalse(profile.baseline_eligible)
        self.assertTrue(profile.baseline_ineligibility_reasons())


class TestBaselineEligibility(unittest.TestCase):
    def test_fully_observed_synthetic_profile_is_eligible(self) -> None:
        profile = synthetic_isolated_profile()
        self.assertTrue(profile.baseline_eligible)
        self.assertEqual(profile.unobserved_fields(), ())

    def test_any_required_unknown_field_makes_ineligible(self) -> None:
        base = synthetic_isolated_profile().to_dict(include_derived=False)
        for name in (
            "runtime_version",
            "managed_settings_status",
            "auto_memory_state",
            "mcp_scope",
            "permission_policy",
            "auto_update_state",
        ):
            payload = dict(base)
            payload[name] = UNKNOWN
            profile = ExecutionProfile.from_dict(payload)
            self.assertFalse(profile.baseline_eligible, name)

    def test_unisolated_memory_or_auto_update_ineligible(self) -> None:
        base = synthetic_isolated_profile().to_dict(include_derived=False)
        memory = dict(base, auto_memory_state="active-user-memory")
        self.assertFalse(ExecutionProfile.from_dict(memory).baseline_eligible)
        updates = dict(base, auto_update_state="auto")
        self.assertFalse(ExecutionProfile.from_dict(updates).baseline_eligible)

    def test_profile_hash_stable_and_sensitive(self) -> None:
        first = synthetic_isolated_profile()
        second = synthetic_isolated_profile()
        self.assertEqual(first.profile_hash, second.profile_hash)
        changed = ExecutionProfile.from_dict(
            dict(first.to_dict(include_derived=False), runtime_version="synthetic-2.0")
        )
        self.assertNotEqual(first.profile_hash, changed.profile_hash)

    def test_empty_string_field_rejected_no_silent_default(self) -> None:
        payload = synthetic_isolated_profile().to_dict(include_derived=False)
        payload["hook_scope"] = ""
        with self.assertRaises(ProfileError):
            ExecutionProfile.from_dict(payload)

    def test_unknown_keys_rejected(self) -> None:
        payload = synthetic_isolated_profile().to_dict(include_derived=False)
        payload["invented_flag"] = "on"
        with self.assertRaises(ProfileError):
            ExecutionProfile.from_dict(payload)


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
