"""Offline shared-ledger regression checks for synthetic authority claims."""

from contextlib import closing
from pathlib import Path
import sqlite3
import tempfile
import unittest
from unittest.mock import patch

from tools.aegis_delivery_control.authority import (
    SyntheticAuthority, SyntheticGrant, SyntheticValidatorGrant,
)
from tools.aegis_delivery_control.contracts import DispatchDenied


class SharedAuthorityClaimTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary_directory.cleanup)
        self.path = Path(self.temporary_directory.name) / "claims.sqlite3"
        self.key = b"offline-shared-authority-test-key-32bytes"
        self.first = SyntheticAuthority(self.key, self.path)
        self.second = SyntheticAuthority(self.key, self.path)

    def test_effect_verification_observes_other_instance_commit(self) -> None:
        grant = SyntheticGrant("grant", "repo", "effect", "attempt", "scope")
        self.first.register(grant)
        self.second.register(grant)
        capability = self.first.claim_or_recover(*grant.__dict__.values())
        self.second.claim_or_recover(*grant.__dict__.values())
        self.first.verify_for_intent(capability)
        self.second.mark_intent_committed(capability, "event", "hash")
        with self.assertRaisesRegex(DispatchDenied, "already committed"):
            self.first.verify_for_intent(capability)
        with self.assertRaisesRegex(DispatchDenied, "another durable intent"):
            self.first.mark_intent_committed(capability, "other-event", "other-hash")
        self.first.mark_or_recover_intent_committed(capability, "event", "hash")
        self.first.verify_intent_committed(capability, "event", "hash")

    def test_validator_verification_observes_other_instance_commit(self) -> None:
        grant = SyntheticValidatorGrant(
            "grant", "repo", "effect", "revision", "check", "input",
            "attempt", "scope", "containment",
        )
        self.first.register_validator(grant)
        self.second.register_validator(grant)
        capability = self.first.claim_or_recover_validator(*grant.__dict__.values())
        self.second.claim_or_recover_validator(*grant.__dict__.values())
        self.first.verify_validator_for_intent(capability)
        self.second.mark_validator_intent_committed(capability, "event", "hash")
        with self.assertRaisesRegex(DispatchDenied, "already committed"):
            self.first.verify_validator_for_intent(capability)
        self.first.verify_validator_intent_committed(capability, "event", "hash")

    def test_explicit_validator_claim_is_durable_and_strict(self) -> None:
        grant = SyntheticValidatorGrant(
            "grant", "repo", "effect", "revision", "check", "input",
            "attempt", "scope", "containment",
        )
        self.first.register_validator(grant)
        self.second.register_validator(grant)
        capability = self.first.claim_validator(*grant.__dict__.values())
        with self.assertRaisesRegex(DispatchDenied, "already claimed"):
            self.second.claim_validator(*grant.__dict__.values())
        self.assertEqual(
            self.second.claim_or_recover_validator(*grant.__dict__.values()),
            capability,
        )
        self.first.verify_validator_for_intent(capability)
        self.first.mark_validator_intent_committed(capability, "event", "hash")
        restarted = SyntheticAuthority(self.key, self.path)
        restarted.register_validator(grant)
        recovered = restarted.claim_or_recover_validator(*grant.__dict__.values())
        restarted.verify_validator_intent_committed(recovered, "event", "hash")

    def test_release_retains_durable_claim_for_exact_recovery(self) -> None:
        grant = SyntheticValidatorGrant(
            "grant", "repo", "effect", "revision", "check", "input",
            "attempt", "scope", "containment",
        )
        self.first.register_validator(grant)
        capability = self.first.claim_validator(*grant.__dict__.values())
        self.first.release_uncommitted_validator_claim(capability)
        with self.assertRaisesRegex(DispatchDenied, "already claimed"):
            self.first.claim_validator(*grant.__dict__.values())
        self.assertEqual(
            self.first.claim_or_recover_validator(*grant.__dict__.values()),
            capability,
        )
        self.first.verify_validator_for_intent(capability)

    def test_release_denies_other_instance_commit(self) -> None:
        grant = SyntheticValidatorGrant(
            "grant", "repo", "effect", "revision", "check", "input",
            "attempt", "scope", "containment",
        )
        self.first.register_validator(grant)
        self.second.register_validator(grant)
        capability = self.first.claim_validator(*grant.__dict__.values())
        self.second.claim_or_recover_validator(*grant.__dict__.values())
        self.second.mark_validator_intent_committed(capability, "event", "hash")
        with self.assertRaisesRegex(DispatchDenied, "already committed"):
            self.first.release_uncommitted_validator_claim(capability)
        self.first.verify_validator_issued(capability)

    def test_cached_commit_fails_closed_when_shared_row_disappears(self) -> None:
        grant = SyntheticGrant("grant", "repo", "effect", "attempt", "scope")
        self.first.register(grant)
        capability = self.first.claim_or_recover(*grant.__dict__.values())
        self.first.mark_intent_committed(capability, "event", "hash")
        with closing(sqlite3.connect(self.path)) as connection:
            connection.execute("DELETE FROM effect_source_claims WHERE grant_id = ?", (grant.grant_id,))
            connection.commit()
        with self.assertRaisesRegex(DispatchDenied, "binding is unavailable"):
            self.first.mark_or_recover_intent_committed(capability, "event", "hash")
        with self.assertRaisesRegex(DispatchDenied, "not bound"):
            self.first.verify_intent_committed(capability, "event", "hash")

    def test_shared_store_error_denies_both_intent_verifiers(self) -> None:
        effect = SyntheticGrant("effect-grant", "repo", "effect", "attempt", "scope")
        validator = SyntheticValidatorGrant(
            "validator-grant", "repo", "effect", "revision", "check",
            "input", "attempt", "scope", "containment",
        )
        self.first.register(effect)
        self.first.register_validator(validator)
        effect_capability = self.first.claim_or_recover(*effect.__dict__.values())
        validator_capability = self.first.claim_or_recover_validator(
            *validator.__dict__.values()
        )
        with patch.object(
            self.first, "_validator_claim_connection",
            side_effect=sqlite3.OperationalError("offline test store unavailable"),
        ):
            with self.assertRaisesRegex(DispatchDenied, "state is unavailable"):
                self.first.verify_for_intent(effect_capability)
            with self.assertRaisesRegex(DispatchDenied, "state is unavailable"):
                self.first.verify_validator_for_intent(validator_capability)

    def test_without_shared_store_uses_in_memory_claim_state(self) -> None:
        authority = SyntheticAuthority(self.key)
        grant = SyntheticGrant("grant", "repo", "effect", "attempt", "scope")
        authority.register(grant)
        capability = authority.claim(*grant.__dict__.values())
        authority.verify_for_intent(capability)
        authority.mark_intent_committed(capability)
        with self.assertRaisesRegex(DispatchDenied, "already committed"):
            authority.verify_for_intent(capability)


if __name__ == "__main__":
    unittest.main()
