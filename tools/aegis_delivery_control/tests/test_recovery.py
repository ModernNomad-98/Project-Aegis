from __future__ import annotations

import tempfile
import unittest
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from tools.aegis_delivery_control.adapters import (
    SyntheticEffectRequest,
    SyntheticExecutionAdapter,
)
from tools.aegis_delivery_control.authority import (
    SyntheticAuthority,
    SyntheticCapability,
    SyntheticGrant,
)
from tools.aegis_delivery_control.contracts import (
    CommitReceipt,
    DispatchDenied,
    IntentRequest,
)


class SyntheticBoundaryTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary_directory.cleanup)
        self.ledger_path = Path(self.temporary_directory.name) / "target.sqlite3"
        self.authority = SyntheticAuthority()
        self.grant = SyntheticGrant(
            grant_id="grant-1",
            repository_id="repo-1",
            logical_effect_id="effect-1",
            attempt_id="attempt-1",
            scope_digest="scope-1",
        )
        self.authority.register(self.grant)

    def claim(self):
        return self.authority.claim(
            self.grant.grant_id,
            self.grant.repository_id,
            self.grant.logical_effect_id,
            self.grant.attempt_id,
            self.grant.scope_digest,
        )

    def request(self) -> SyntheticEffectRequest:
        return SyntheticEffectRequest(
            repository_id="repo-1",
            logical_effect_id="effect-1",
            attempt_id="attempt-1",
            scope_digest="scope-1",
            payload_digest="payload-1",
        )

    @staticmethod
    def commit() -> CommitReceipt:
        return CommitReceipt("command-1", "event-1", 1, "event-hash-1", False)

    @staticmethod
    def intent() -> IntentRequest:
        return IntentRequest(
            "repo-1", "run-1", "item-1", "command-1", "event-1",
            "effect-1", "payload-1", "attempt-1", "permission-1",
            "reservation-1", "budget-1", 1, 1, 2,
        )

    def test_f03_one_use_grant_has_exactly_one_claim_winner(self) -> None:
        capability = self.claim()
        self.assertEqual(capability.grant_id, "grant-1")
        with self.assertRaisesRegex(DispatchDenied, "already claimed"):
            self.claim()

    def test_f03_binding_mismatch_denies_claim(self) -> None:
        with self.assertRaisesRegex(DispatchDenied, "binding mismatch"):
            self.authority.claim(
                "grant-1", "repo-1", "different-effect", "attempt-1", "scope-1"
            )

    def test_c03_lost_receipt_is_reconcilable_without_redispatch(self) -> None:
        adapter = SyntheticExecutionAdapter(self.ledger_path)
        capability = self.claim()
        self.assertIsNone(
            adapter._execute_committed(
                capability,
                self.request(),
                self.authority,
                self.commit(),
                self.intent(),
                usage_units=None,
                lose_receipt=True,
            )
        )
        recovered = SyntheticExecutionAdapter(self.ledger_path).reconcile(
            capability.claim_id
        )
        self.assertIsNotNone(recovered)
        self.assertIsNone(recovered.usage_units)
        with self.assertRaisesRegex(DispatchDenied, "already redeemed"):
            adapter._execute_committed(
                capability, self.request(), self.authority, self.commit(), self.intent()
            )

    def test_f03_capability_cannot_be_rebound(self) -> None:
        adapter = SyntheticExecutionAdapter(self.ledger_path)
        capability = self.claim()
        wrong_request = SyntheticEffectRequest(
            repository_id="repo-2",
            logical_effect_id="effect-1",
            attempt_id="attempt-1",
            scope_digest="scope-1",
            payload_digest="payload-1",
        )
        with self.assertRaisesRegex(DispatchDenied, "does not bind"):
            adapter._execute_committed(
                capability, wrong_request, self.authority, self.commit(), self.intent()
            )

    def test_f03_forged_capability_is_not_issuer_verifiable(self) -> None:
        forged = SyntheticCapability(
            "claim", "grant-1", "repo-1", "effect-1", "attempt-1", "scope-1", "forged"
        )
        with self.assertRaisesRegex(DispatchDenied, "not issued"):
            self.authority.verify_issued(forged)

    def test_f03_concurrent_redemption_has_one_winner(self) -> None:
        adapter = SyntheticExecutionAdapter(self.ledger_path)
        capability = self.claim()

        def redeem() -> bool:
            try:
                adapter._execute_committed(
                    capability, self.request(), self.authority, self.commit(), self.intent()
                )
            except DispatchDenied:
                return False
            return True

        with ThreadPoolExecutor(max_workers=8) as executor:
            results = list(executor.map(lambda _: redeem(), range(8)))
        self.assertEqual(results.count(True), 1)


if __name__ == "__main__":
    unittest.main()