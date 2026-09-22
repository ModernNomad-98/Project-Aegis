from __future__ import annotations

import tempfile
import unittest
from concurrent.futures import ThreadPoolExecutor
from dataclasses import replace
from pathlib import Path
from unittest.mock import patch

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
    OperationLaunchReceipt,
    PlanAcceptanceRequest as PlanAcceptanceContract,
)
from tools.aegis_delivery_control.storage import default_state_root
from tools.aegis_delivery_control.tests._trusted_readiness_store import (
    SQLiteStateStore,
)


def PlanAcceptanceRequest(*args, **kwargs):
    """Build a newly accepted synthetic plan with explicit immutable pins."""
    kwargs.setdefault("source_tree_digest", "source-tree-1")
    kwargs.setdefault("item_definition_digest", "item-definition-1")
    kwargs.setdefault("plan_schema_version", "plan-schema-1")
    kwargs.setdefault("reducer_version", "reducer-1")
    return PlanAcceptanceContract(*args, **kwargs)


class MutableFreshnessOracle:
    def __init__(self) -> None:
        self.allowed_head = ""

    def verify(self, repository_id, catalog_head, run_heads):
        return repository_id == "repo-1"


class SyntheticBoundaryTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary_directory.cleanup)
        self.state_root = patch(
            "tools.aegis_delivery_control.storage.known_local_state_base",
            return_value=Path(self.temporary_directory.name),
        )
        self.state_root.start()
        self.addCleanup(self.state_root.stop)
        self.ledger_path = default_state_root("repo-1") / "synthetic-target.sqlite3"
        self.authority = SyntheticAuthority()
        self.oracle = MutableFreshnessOracle()
        self.store = SQLiteStateStore.open_canonical("repo-1", self.oracle)
        self.store._bind_classification_authority(self.authority)
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

    @staticmethod
    def launch() -> OperationLaunchReceipt:
        return OperationLaunchReceipt(
            "launch:command-1", "launch:event-1", "repo-1", "run-1",
            "item-1", "effect-1", "attempt-1", "event-hash-1",
            "launch-hash-1", False,
        )

    def prepare_launch(self):
        capability = self.claim()
        plan = self.store.accept_plan(
            PlanAcceptanceRequest(
                "plan-1", "plan-command-1", "plan-event-1", "repo-1",
                "run-1", "item-1", "effect-1", "revision-1", "payload-1",
                "scope-1", "budget-1", ("check-1",),
            ),
            expected_head="",
            writer_epoch=1,
        )
        self.oracle.allowed_head = plan.event_hash
        commit = self.store.commit_intent(
            self.intent(), capability, self.authority,
            expected_head=plan.event_hash, writer_epoch=2,
        )
        self.oracle.allowed_head = commit.event_hash
        launch = self.store.claim_operation_launch(self.intent(), commit)
        self.oracle.allowed_head = launch.event_hash
        return capability, commit, launch

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
        adapter = SyntheticExecutionAdapter.open_canonical("repo-1")
        capability, commit, launch = self.prepare_launch()
        self.assertIsNone(
            adapter._execute_committed(
                capability,
                self.request(),
                self.authority,
            self.store,
            commit,
            launch,
                self.intent(),
                usage_units=None,
                lose_receipt=True,
            )
        )
        recovered = SyntheticExecutionAdapter.open_canonical("repo-1").reconcile(
            capability.claim_id
        )
        self.assertIsNotNone(recovered)
        self.assertIsNone(recovered.usage_units)
        with self.assertRaisesRegex(DispatchDenied, "already claimed"):
            adapter._execute_committed(
                capability, self.request(), self.authority, self.store,
                commit, launch, self.intent()
            )
        alternate = SyntheticExecutionAdapter(
            Path(self.temporary_directory.name) / "alternate-target.sqlite3"
        )
        with self.assertRaisesRegex(DispatchDenied, "canonical repository root"):
            alternate._execute_committed(
                capability, self.request(), self.authority, self.store,
                commit, launch, self.intent()
            )
        self.assertIsNone(alternate.reconcile(capability.claim_id))

    def test_f03_capability_cannot_be_rebound(self) -> None:
        adapter = SyntheticExecutionAdapter.open_canonical("repo-1")
        capability, commit, launch = self.prepare_launch()
        wrong_request = SyntheticEffectRequest(
            repository_id="repo-2",
            logical_effect_id="effect-1",
            attempt_id="attempt-1",
            scope_digest="scope-1",
            payload_digest="payload-1",
        )
        with self.assertRaisesRegex(DispatchDenied, "does not bind"):
            adapter._execute_committed(
                capability, wrong_request, self.authority, self.store,
                commit, launch, self.intent()
            )

    def test_f03_launch_claim_cannot_be_rebound(self) -> None:
        adapter = SyntheticExecutionAdapter.open_canonical("repo-1")
        capability, commit, launch = self.prepare_launch()
        with self.assertRaisesRegex(DispatchDenied, "durable launch"):
            adapter._execute_committed(
                capability, self.request(), self.authority, self.store,
                commit, replace(launch, run_id="run-2"), self.intent(),
            )
        self.assertIsNone(adapter.reconcile(capability.claim_id))

    def test_f03_fabricated_handoff_cannot_contact_target(self) -> None:
        adapter = SyntheticExecutionAdapter.open_canonical("repo-1")
        capability = self.claim()
        with self.assertRaisesRegex(DispatchDenied, "durable operation launch"):
            adapter._execute_committed(
                capability, self.request(), self.authority, self.store,
                self.commit(), self.launch(), self.intent(),
            )
        self.assertIsNone(adapter.reconcile(capability.claim_id))

    def test_f03_forged_capability_is_not_issuer_verifiable(self) -> None:
        forged = SyntheticCapability(
            "claim", "grant-1", "repo-1", "effect-1", "attempt-1", "scope-1", "forged"
        )
        with self.assertRaisesRegex(DispatchDenied, "not issued"):
            self.authority.verify_issued(forged)

    def test_f03_concurrent_redemption_has_one_winner(self) -> None:
        adapter = SyntheticExecutionAdapter.open_canonical("repo-1")
        capability, commit, launch = self.prepare_launch()

        def redeem() -> bool:
            try:
                adapter._execute_committed(
                    capability, self.request(), self.authority, self.store,
                    commit, launch, self.intent()
                )
            except DispatchDenied:
                return False
            return True

        with ThreadPoolExecutor(max_workers=8) as executor:
            results = list(executor.map(lambda _: redeem(), range(8)))
        self.assertEqual(results.count(True), 1)


if __name__ == "__main__":
    unittest.main()
