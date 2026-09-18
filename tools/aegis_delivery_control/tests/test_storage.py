from __future__ import annotations

import sqlite3
import shutil
import tempfile
import unittest
from pathlib import Path
from typing import Mapping

from tools.aegis_delivery_control.authority import (
    SyntheticAuthority,
    SyntheticGrant,
    SyntheticValidatorGrant,
)
from tools.aegis_delivery_control.contracts import (
    BudgetDisposition,
    BudgetSettlementRequest,
    DispatchDenied,
    EffectObservationRequest,
    InjectedFailure,
    IntentRequest,
    PlanAcceptanceRequest,
    StorageIntegrityError,
    ValidationApplicationRequest,
    ValidatorIntentRequest,
    ValidatorObservationRequest,
)
from tools.aegis_delivery_control.storage import SQLiteStateStore, raise_at


class MutableFreshnessOracle:
    def __init__(self) -> None:
        self.allowed_head = ""

    def verify(
        self,
        repository_id: str,
        catalog_head: str,
        run_heads: Mapping[str, str],
    ) -> bool:
        return repository_id == "repo-1" and catalog_head == self.allowed_head


class SQLiteStateStoreTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary_directory.cleanup)
        database_path = Path(self.temporary_directory.name) / "state.sqlite3"
        self.database_path = database_path
        self.oracle = MutableFreshnessOracle()
        self.store = SQLiteStateStore(database_path, self.oracle, "repo-1")
        self.authority = SyntheticAuthority()
        self.authority.register(
            SyntheticGrant(
                "grant-1", "repo-1", "effect-1", "attempt-1", "scope-1"
            )
        )
        self.capability = self.authority.claim(
            "grant-1", "repo-1", "effect-1", "attempt-1", "scope-1"
        )

    @staticmethod
    def request() -> IntentRequest:
        return IntentRequest(
            repository_id="repo-1",
            run_id="run-1",
            item_id="item-1",
            command_id="command-1",
            event_id="event-1",
            logical_effect_id="effect-1",
            effect_descriptor_digest="descriptor-digest",
            attempt_id="attempt-1",
            permission_use_id="permission-use-1",
            reservation_id="reservation-1",
            budget_policy_digest="budget-policy-digest",
            reserved_units=3,
            worst_case_units=5,
            cap_units=10,
        )

    def test_c01_failure_before_commit_leaves_no_authoritative_state(self) -> None:
        with self.assertRaises(InjectedFailure):
            self.store.commit_intent(
                self.request(),
                self.capability,
                self.authority,
                expected_head="",
                writer_epoch=1,
                failure_hook=raise_at("after_intent_writes_before_commit"),
            )

        self.assertEqual(
            self.store.table_counts(),
            {
                "repositories": 0,
                "runs": 0,
                "validation_plans": 0,
                "validation_requirements": 0,
                "events": 0,
                "command_outcomes": 0,
                "effects": 0,
                "permission_uses": 0,
                "capability_redemptions": 0,
                "budget_reservations": 0,
                "budget_settlements": 0,
                "effect_observations": 0,
                "validator_intents": 0,
                "validator_observations": 0,
                "validation_applications": 0,
                "outstanding_slot": 0,
                "dispatch_fences": 0,
            },
        )

    def test_intent_commit_is_atomic_and_replay_is_idempotent(self) -> None:
        first = self.store.commit_intent(
            self.request(), self.capability, self.authority, expected_head="", writer_epoch=1
        )
        self.oracle.allowed_head = first.event_hash
        replay = self.store.commit_intent(
            self.request(), self.capability, self.authority, expected_head=first.event_hash, writer_epoch=2
        )

        self.assertFalse(first.replayed)
        self.assertTrue(replay.replayed)
        self.assertEqual(replay.event_hash, first.event_hash)
        self.assertEqual(
            self.store.table_counts(),
            {
                "repositories": 1,
                "runs": 1,
                "validation_plans": 0,
                "validation_requirements": 0,
                "events": 1,
                "command_outcomes": 1,
                "effects": 1,
                "permission_uses": 1,
                "capability_redemptions": 1,
                "budget_reservations": 1,
                "budget_settlements": 0,
                "effect_observations": 0,
                "validator_intents": 0,
                "validator_observations": 0,
                "validation_applications": 0,
                "outstanding_slot": 1,
                "dispatch_fences": 0,
            },
        )

    def test_f04_unknown_usage_charges_worst_case_and_retains_slot(self) -> None:
        committed = self.store.commit_intent(self.request(), self.capability, self.authority, expected_head="", writer_epoch=1)
        self.oracle.allowed_head = committed.event_hash
        request = BudgetSettlementRequest(
                settlement_event_id="settlement-1",
                reservation_id="reservation-1",
                expected_previous_hash="",
                disposition=BudgetDisposition.UNKNOWN_WORST_CASE_CHARGED,
                actual_units=None,
                evidence_digest="missing-telemetry",
                reason_code="USAGE_UNKNOWN",
                release_slot=False,
            )
        proof = self.authority.issue_settlement_proof(
            "proof-1",
            "reservation-1",
            non_dispatch_proven=False,
            zero_liability_proven=False,
            all_obligations_settled=False,
        )
        receipt = self.store.settle_budget(request, proof, self.authority)
        self.assertEqual(receipt.charged_units, 5)
        self.assertTrue(receipt.uncertainty)
        self.assertEqual(self.store.table_counts()["outstanding_slot"], 1)

    def test_f04_release_requires_both_proofs_and_releases_slot_once(self) -> None:
        committed = self.store.commit_intent(self.request(), self.capability, self.authority, expected_head="", writer_epoch=1)
        self.oracle.allowed_head = committed.event_hash
        incomplete = BudgetSettlementRequest(
            settlement_event_id="settlement-1",
            reservation_id="reservation-1",
            expected_previous_hash="",
            disposition=BudgetDisposition.RELEASED,
            actual_units=None,
            evidence_digest="proof-1",
            reason_code="NONDISPATCH",
            non_dispatch_proven=True,
            zero_liability_proven=False,
            release_slot=True,
            all_obligations_settled=True,
        )
        with self.assertRaisesRegex(DispatchDenied, "zero-liability"):
            proof = self.authority.issue_settlement_proof(
                "proof-incomplete",
                "reservation-1",
                non_dispatch_proven=True,
                zero_liability_proven=False,
                all_obligations_settled=True,
            )
            self.store.settle_budget(incomplete, proof, self.authority)

        complete = BudgetSettlementRequest(
            **{**incomplete.__dict__, "zero_liability_proven": True}
        )
        proof = self.authority.issue_settlement_proof(
            "proof-complete",
            "reservation-1",
            non_dispatch_proven=True,
            zero_liability_proven=True,
            all_obligations_settled=True,
        )
        receipt = self.store.settle_budget(complete, proof, self.authority)
        self.oracle.allowed_head = receipt.settlement_hash
        replay = self.store.settle_budget(complete, proof, self.authority)
        self.assertTrue(receipt.slot_released)
        self.assertTrue(replay.replayed)
        self.assertEqual(self.store.table_counts()["outstanding_slot"], 0)

    def test_f05_recovery_requires_independent_current_head(self) -> None:
        oracle = MutableFreshnessOracle()
        database_path = Path(self.temporary_directory.name) / "freshness.sqlite3"
        store = SQLiteStateStore(database_path, oracle, "repo-1")
        authority = SyntheticAuthority()
        authority.register(SyntheticGrant("grant-2", "repo-1", "effect-1", "attempt-1", "scope-1"))
        capability = authority.claim("grant-2", "repo-1", "effect-1", "attempt-1", "scope-1")
        committed = store.commit_intent(
            self.request(), capability, authority, expected_head="", writer_epoch=1
        )
        with self.assertRaisesRegex(DispatchDenied, "freshness"):
            store.load_verified("repo-1")
        oracle.allowed_head = committed.event_hash
        catalog_head, run_heads = store.load_verified("repo-1")
        self.assertEqual(catalog_head, committed.event_hash)
        self.assertEqual(run_heads, {"run-1": committed.event_hash})

    def test_database_rejects_another_repository_identity(self) -> None:
        database_path = Path(self.temporary_directory.name) / "bound.sqlite3"
        SQLiteStateStore(database_path, MutableFreshnessOracle(), "repo-1")
        with self.assertRaisesRegex(Exception, "another repository"):
            SQLiteStateStore(database_path, MutableFreshnessOracle(), "repo-2")

    def test_recovery_rejects_deleted_slot_projection(self) -> None:
        committed = self.store.commit_intent(
            self.request(), self.capability, self.authority, expected_head="", writer_epoch=1
        )
        self.oracle.allowed_head = committed.event_hash
        connection = sqlite3.connect(self.database_path)
        try:
            connection.execute("DELETE FROM outstanding_slot")
            connection.commit()
        finally:
            connection.close()
        with self.assertRaisesRegex(Exception, "slot projection"):
            self.store.load_verified("repo-1")

    def test_recovery_rejects_tampered_command_and_redemption_projections(self) -> None:
        committed = self.store.commit_intent(
            self.request(), self.capability, self.authority, expected_head="", writer_epoch=1
        )
        self.oracle.allowed_head = committed.event_hash
        connection = sqlite3.connect(self.database_path)
        try:
            connection.execute(
                "UPDATE command_outcomes SET event_hash = 'forged' WHERE command_id = 'command-1'"
            )
            connection.commit()
        finally:
            connection.close()
        with self.assertRaisesRegex(Exception, "command-outcome projection"):
            self.store.load_verified("repo-1")

        connection = sqlite3.connect(self.database_path)
        try:
            connection.execute(
                "UPDATE command_outcomes SET event_hash = ? WHERE command_id = 'command-1'",
                (committed.event_hash,),
            )
            connection.execute("DELETE FROM capability_redemptions")
            connection.commit()
        finally:
            connection.close()
        with self.assertRaisesRegex(Exception, "capability-redemption projection"):
            self.store.load_verified("repo-1")

    def test_recovery_rejects_tampered_lifecycle_projection(self) -> None:
        committed = self.store.commit_intent(
            self.request(), self.capability, self.authority, expected_head="", writer_epoch=1
        )
        self.oracle.allowed_head = committed.event_hash
        connection = sqlite3.connect(self.database_path)
        try:
            connection.execute(
                "UPDATE runs SET lifecycle_state = 'PLANNED' WHERE run_id = 'run-1'"
            )
            connection.commit()
        finally:
            connection.close()
        with self.assertRaisesRegex(Exception, "lifecycle projection"):
            self.store.load_verified("repo-1")

    def test_recovery_reconstructs_settlement_accounting_and_fences(self) -> None:
        committed = self.store.commit_intent(
            self.request(), self.capability, self.authority, expected_head="", writer_epoch=1
        )
        self.oracle.allowed_head = committed.event_hash
        settlement = BudgetSettlementRequest(
            settlement_event_id="settlement-1",
            reservation_id="reservation-1",
            expected_previous_hash="",
            disposition=BudgetDisposition.CONSUMED,
            actual_units=11,
            evidence_digest="usage-evidence",
            reason_code="USAGE_REPORTED",
        )
        proof = self.authority.issue_settlement_proof(
            "proof-1",
            "reservation-1",
            non_dispatch_proven=False,
            zero_liability_proven=False,
            all_obligations_settled=False,
        )
        self.store.settle_budget(settlement, proof, self.authority)

        connection = sqlite3.connect(self.database_path)
        try:
            connection.execute(
                "UPDATE budget_reservations SET charged_units = 1 WHERE reservation_id = 'reservation-1'"
            )
            connection.commit()
        finally:
            connection.close()
        with self.assertRaisesRegex(Exception, "accounting projection"):
            self.store.load_verified("repo-1")

        connection = sqlite3.connect(self.database_path)
        try:
            connection.execute(
                "UPDATE budget_reservations SET charged_units = 11 WHERE reservation_id = 'reservation-1'"
            )
            connection.execute("DELETE FROM dispatch_fences")
            connection.commit()
        finally:
            connection.close()
        with self.assertRaisesRegex(Exception, "dispatch-fence projection"):
            self.store.load_verified("repo-1")

    def test_settlement_requires_verified_fresh_state(self) -> None:
        self.store.commit_intent(
            self.request(), self.capability, self.authority, expected_head="", writer_epoch=1
        )
        request = BudgetSettlementRequest(
            "settlement-1",
            "reservation-1",
            "",
            BudgetDisposition.CONSUMED,
            1,
            "usage-evidence",
            "USAGE_REPORTED",
        )
        proof = self.authority.issue_settlement_proof(
            "proof-1",
            "reservation-1",
            non_dispatch_proven=False,
            zero_liability_proven=False,
            all_obligations_settled=False,
        )
        with self.assertRaisesRegex(DispatchDenied, "freshness"):
            self.store.settle_budget(request, proof, self.authority)
        self.assertEqual(self.store.table_counts()["budget_settlements"], 0)

    def test_c09_failure_before_settlement_commit_preserves_reservation_and_slot(self) -> None:
        committed = self.store.commit_intent(
            self.request(), self.capability, self.authority, expected_head="", writer_epoch=1
        )
        self.oracle.allowed_head = committed.event_hash
        request = BudgetSettlementRequest(
            "settlement-1",
            "reservation-1",
            "",
            BudgetDisposition.CONSUMED,
            2,
            "usage-evidence",
            "USAGE_REPORTED",
            release_slot=True,
            all_obligations_settled=True,
        )
        proof = self.authority.issue_settlement_proof(
            "proof-1",
            "reservation-1",
            non_dispatch_proven=False,
            zero_liability_proven=False,
            all_obligations_settled=True,
        )

        with self.assertRaises(InjectedFailure):
            self.store.settle_budget(
                request,
                proof,
                self.authority,
                failure_hook=raise_at("after_settlement_writes_before_commit"),
            )

        self.assertEqual(self.store.table_counts()["budget_settlements"], 0)
        self.assertEqual(self.store.table_counts()["outstanding_slot"], 1)
        catalog_head, run_heads = self.store.load_verified("repo-1")
        self.assertEqual(catalog_head, committed.event_hash)
        self.assertEqual(run_heads, {"run-1": committed.event_hash})

        receipt = self.store.settle_budget(request, proof, self.authority)
        self.oracle.allowed_head = receipt.settlement_hash
        self.assertFalse(receipt.replayed)
        self.assertEqual(receipt.held_units, 0)
        self.assertEqual(receipt.charged_units, 2)
        self.assertFalse(receipt.uncertainty)
        self.assertTrue(receipt.slot_released)
        self.assertEqual(self.store.table_counts()["events"], 2)
        self.assertEqual(self.store.table_counts()["budget_reservations"], 1)
        self.assertEqual(self.store.table_counts()["budget_settlements"], 1)
        self.assertEqual(self.store.table_counts()["outstanding_slot"], 0)
        self.store.load_verified("repo-1")

    def test_c09_failure_after_settlement_commit_replays_without_duplicate_release(self) -> None:
        committed = self.store.commit_intent(
            self.request(), self.capability, self.authority, expected_head="", writer_epoch=1
        )
        self.oracle.allowed_head = committed.event_hash
        request = BudgetSettlementRequest(
            "settlement-1",
            "reservation-1",
            "",
            BudgetDisposition.CONSUMED,
            2,
            "usage-evidence",
            "USAGE_REPORTED",
            release_slot=True,
            all_obligations_settled=True,
        )
        proof = self.authority.issue_settlement_proof(
            "proof-1",
            "reservation-1",
            non_dispatch_proven=False,
            zero_liability_proven=False,
            all_obligations_settled=True,
        )

        with self.assertRaises(InjectedFailure):
            self.store.settle_budget(
                request,
                proof,
                self.authority,
                failure_hook=raise_at(
                    "after_settlement_commit_before_acknowledgement"
                ),
            )

        connection = sqlite3.connect(self.database_path)
        try:
            settlement_hash = connection.execute(
                "SELECT settlement_hash FROM budget_settlements WHERE settlement_event_id = 'settlement-1'"
            ).fetchone()[0]
        finally:
            connection.close()
        self.oracle.allowed_head = settlement_hash
        replay = self.store.settle_budget(request, proof, self.authority)

        self.assertTrue(replay.replayed)
        self.assertEqual(replay.settlement_hash, settlement_hash)
        self.assertEqual(replay.held_units, 0)
        self.assertEqual(replay.charged_units, 2)
        self.assertFalse(replay.uncertainty)
        self.assertFalse(replay.slot_released)
        connection = sqlite3.connect(self.database_path)
        try:
            reservation = connection.execute(
                "SELECT held_units, charged_units, uncertainty FROM budget_reservations WHERE reservation_id = 'reservation-1'"
            ).fetchone()
        finally:
            connection.close()
        self.assertEqual(reservation, (0, 2, 0))
        self.assertEqual(self.store.table_counts()["events"], 2)
        self.assertEqual(self.store.table_counts()["budget_reservations"], 1)
        self.assertEqual(self.store.table_counts()["budget_settlements"], 1)
        self.assertEqual(self.store.table_counts()["outstanding_slot"], 0)
        self.store.load_verified("repo-1")

    def test_c04_observation_intake_survives_crash_without_duplicate_or_slot_release(self) -> None:
        committed = self.store.commit_intent(
            self.request(), self.capability, self.authority, expected_head="", writer_epoch=1
        )
        self.oracle.allowed_head = committed.event_hash
        settlement_request = BudgetSettlementRequest(
            "settlement-1",
            "reservation-1",
            "",
            BudgetDisposition.CONSUMED,
            2,
            "receipt-1",
            "USAGE_REPORTED",
        )
        proof = self.authority.issue_settlement_proof(
            "proof-1",
            "reservation-1",
            non_dispatch_proven=False,
            zero_liability_proven=False,
            all_obligations_settled=False,
        )
        settlement = self.store.settle_budget(
            settlement_request, proof, self.authority
        )
        self.oracle.allowed_head = settlement.settlement_hash
        observation = EffectObservationRequest(
            observation_id="observation-1",
            command_id="observe-command-1",
            event_id="observation-event-1",
            repository_id="repo-1",
            run_id="run-1",
            item_id="item-1",
            logical_effect_id="effect-1",
            attempt_id="attempt-1",
            source_receipt_id="receipt-1",
            source_claim_id=self.capability.claim_id,
            payload_digest="descriptor-digest",
            usage_units=2,
            settlement_event_id="settlement-1",
            settlement_hash=settlement.settlement_hash,
        )

        with self.assertRaises(InjectedFailure):
            self.store.record_effect_observation(
                observation,
                failure_hook=raise_at("after_observation_writes_before_commit"),
            )
        self.assertEqual(self.store.table_counts()["effect_observations"], 0)
        self.assertEqual(self.store.table_counts()["outstanding_slot"], 1)

        with self.assertRaises(InjectedFailure):
            self.store.record_effect_observation(
                observation,
                failure_hook=raise_at(
                    "after_observation_commit_before_acknowledgement"
                ),
            )
        connection = sqlite3.connect(self.database_path)
        try:
            observation_hash = connection.execute(
                "SELECT event_hash FROM effect_observations WHERE observation_id = 'observation-1'"
            ).fetchone()[0]
        finally:
            connection.close()
        self.oracle.allowed_head = observation_hash
        replay = self.store.record_effect_observation(observation)

        self.assertTrue(replay.replayed)
        self.assertEqual(replay.event_hash, observation_hash)
        self.assertEqual(replay.resulting_state.value, "VALIDATING")

    def test_c04_unknown_receipt_usage_is_recorded_for_reconciliation(self) -> None:
        committed = self.store.commit_intent(
            self.request(), self.capability, self.authority, expected_head="", writer_epoch=1
        )
        self.oracle.allowed_head = committed.event_hash
        proof = self.authority.issue_settlement_proof(
            "proof-1", "reservation-1", non_dispatch_proven=False,
            zero_liability_proven=False, all_obligations_settled=False,
        )
        settlement = self.store.settle_budget(
            BudgetSettlementRequest(
                "settlement-1", "reservation-1", "",
                BudgetDisposition.UNKNOWN_WORST_CASE_CHARGED, None,
                "receipt-unknown-1", "USAGE_UNKNOWN",
            ),
            proof,
            self.authority,
        )
        self.oracle.allowed_head = settlement.settlement_hash

        recorded = self.store.record_effect_observation(
            EffectObservationRequest(
                "observation-unknown-1", "observe-unknown-command-1",
                "observation-unknown-event-1", "repo-1", "run-1", "item-1",
                "effect-1", "attempt-1", "receipt-unknown-1",
                self.capability.claim_id, "descriptor-digest", None,
                "settlement-1", settlement.settlement_hash,
            )
        )

        self.assertEqual(recorded.resulting_state.value, "RECONCILIATION_REQUIRED")
        self.assertEqual(self.store.table_counts()["effect_observations"], 1)
        self.assertEqual(self.store.table_counts()["outstanding_slot"], 1)

    def _record_effect_observation(self, check_ids=("check-1", "check-2")):
        plan = self.store.accept_plan(
            PlanAcceptanceRequest(
                "plan-1", "plan-command-1", "plan-event-1", "repo-1",
                "run-1", "item-1", "effect-1", "revision-1",
                check_ids,
            ),
            expected_head="",
            writer_epoch=1,
        )
        self.oracle.allowed_head = plan.event_hash
        committed = self.store.commit_intent(
            self.request(), self.capability, self.authority,
            expected_head=plan.event_hash, writer_epoch=2,
        )
        self.oracle.allowed_head = committed.event_hash
        settlement_request = BudgetSettlementRequest(
            "settlement-1",
            "reservation-1",
            "",
            BudgetDisposition.CONSUMED,
            2,
            "receipt-1",
            "USAGE_REPORTED",
        )
        proof = self.authority.issue_settlement_proof(
            "proof-1",
            "reservation-1",
            non_dispatch_proven=False,
            zero_liability_proven=False,
            all_obligations_settled=False,
        )
        settlement = self.store.settle_budget(
            settlement_request, proof, self.authority
        )
        self.oracle.allowed_head = settlement.settlement_hash
        receipt = self.store.record_effect_observation(
            EffectObservationRequest(
                "observation-1",
                "observe-command-1",
                "observation-event-1",
                "repo-1",
                "run-1",
                "item-1",
                "effect-1",
                "attempt-1",
                "receipt-1",
                self.capability.claim_id,
                "descriptor-digest",
                2,
                "settlement-1",
                settlement.settlement_hash,
            )
        )
        self.oracle.allowed_head = receipt.event_hash
        return receipt

    def test_t01_plan_acceptance_replays_and_rejects_empty_or_tampered_checks(self) -> None:
        request = PlanAcceptanceRequest(
            "plan-1", "plan-command-1", "plan-event-1", "repo-1", "run-1",
            "item-1", "effect-1", "revision-1", ("check-2", "check-1"),
        )
        first = self.store.accept_plan(
            request, expected_head="", writer_epoch=1
        )
        self.oracle.allowed_head = first.event_hash
        replay = self.store.accept_plan(
            request, expected_head=first.event_hash, writer_epoch=2
        )
        self.assertTrue(replay.replayed)
        with self.assertRaisesRegex(ValueError, "at least one"):
            self.store.accept_plan(
                PlanAcceptanceRequest(
                    "plan-2", "plan-command-2", "plan-event-2", "repo-1",
                    "run-2", "item-2", "effect-2", "revision-2", (),
                ),
                expected_head=first.event_hash,
                writer_epoch=2,
            )
        connection = sqlite3.connect(self.database_path)
        try:
            connection.execute(
                "DELETE FROM validation_requirements WHERE plan_id = 'plan-1' AND check_id = 'check-2'"
            )
            connection.commit()
        finally:
            connection.close()
        with self.assertRaisesRegex(StorageIntegrityError, "validation-requirement"):
            self.store.load_verified("repo-1")

    def test_t01_plan_acceptance_is_atomic_across_acknowledgement_loss(self) -> None:
        request = PlanAcceptanceRequest(
            "plan-1", "plan-command-1", "plan-event-1", "repo-1", "run-1",
            "item-1", "effect-1", "revision-1", ("check-1",),
        )
        with self.assertRaises(InjectedFailure):
            self.store.accept_plan(
                request,
                expected_head="",
                writer_epoch=1,
                failure_hook=raise_at("after_plan_writes_before_commit"),
            )
        self.assertEqual(self.store.table_counts()["validation_plans"], 0)
        with self.assertRaises(InjectedFailure):
            self.store.accept_plan(
                request,
                expected_head="",
                writer_epoch=1,
                failure_hook=raise_at("after_plan_commit_before_acknowledgement"),
            )
        connection = sqlite3.connect(self.database_path)
        try:
            event_hash = connection.execute(
                "SELECT event_hash FROM validation_plans WHERE plan_id = 'plan-1'"
            ).fetchone()[0]
        finally:
            connection.close()
        self.oracle.allowed_head = event_hash
        replay = self.store.accept_plan(
            request, expected_head=event_hash, writer_epoch=2
        )
        self.assertTrue(replay.replayed)
        self.store.load_verified("repo-1")

    def _validator_intent(self, observation, *, suffix: str = "1", cap_units: int = 10):
        grant = SyntheticValidatorGrant(
            f"validator-grant-{suffix}",
            "repo-1",
            "effect-1",
            "revision-1",
            f"check-{suffix}",
            "input-1",
            f"validator-attempt-{suffix}",
            f"read-only-scope-{suffix}",
        )
        self.authority.register_validator(grant)
        capability = self.authority.claim_validator(*grant.__dict__.values())
        request = ValidatorIntentRequest(
            f"validator-intent-{suffix}",
            f"validator-command-{suffix}",
            f"validator-event-{suffix}",
            "repo-1",
            "run-1",
            "item-1",
            "effect-1",
            "attempt-1",
            "observation-1",
            observation.event_hash,
            "revision-1",
            f"check-{suffix}",
            "input-1",
            f"validator-attempt-{suffix}",
            f"validator-permission-{suffix}",
            f"validator-reservation-{suffix}",
            "validator-budget-policy-1",
            1,
            2,
            cap_units,
        )
        return request, capability

    def _record_validator_result(self, *, verdict: str = "PASS", only_check: bool = False):
        observation = self._record_effect_observation(
            ("check-1",) if only_check else ("check-1", "check-2")
        )
        intent_request, capability = self._validator_intent(observation)
        intent = self.store.commit_validator_intent(
            intent_request, capability, self.authority
        )
        self.oracle.allowed_head = intent.event_hash
        settlement = self.store.settle_budget(
            BudgetSettlementRequest(
                "validator-settlement-1", "validator-reservation-1", "",
                BudgetDisposition.CONSUMED, 1, "validator-result-1",
                "VALIDATOR_USAGE_REPORTED",
            ),
            self.authority.issue_settlement_proof(
                "validator-proof-1", "validator-reservation-1",
                non_dispatch_proven=False, zero_liability_proven=False,
                all_obligations_settled=False,
            ),
            self.authority,
        )
        self.oracle.allowed_head = settlement.settlement_hash
        recorded = self.store.record_validator_observation(
            ValidatorObservationRequest(
                "validator-observation-1", "validator-observe-command-1",
                "validator-observation-event-1", "repo-1", "run-1", "item-1",
                "effect-1", "validator-intent-1", "validator-attempt-1",
                "validator-result-1", capability.claim_id, "revision-1",
                "check-1", "input-1", "result-digest-1", verdict, 1,
                "validator-settlement-1", settlement.settlement_hash,
            )
        )
        self.oracle.allowed_head = recorded.event_hash
        return recorded

    def test_c05_pass_application_is_atomic_replay_safe_and_retains_slot(self) -> None:
        self._record_validator_result()
        request = ValidationApplicationRequest(
            "application-1", "apply-command-1", "apply-event-1", "repo-1",
            "run-1", "item-1", "effect-1", "revision-1", "check-1",
            "validator-attempt-1", "validator-observation-1",
        )
        with self.assertRaises(InjectedFailure):
            self.store.apply_validator_observation(
                request,
                failure_hook=raise_at(
                    "after_validation_application_writes_before_commit"
                ),
            )
        self.assertEqual(self.store.table_counts()["validation_applications"], 0)
        with self.assertRaises(InjectedFailure):
            self.store.apply_validator_observation(
                request,
                failure_hook=raise_at(
                    "after_validation_application_commit_before_acknowledgement"
                ),
            )
        connection = sqlite3.connect(self.database_path)
        try:
            event_hash = connection.execute(
                "SELECT event_hash FROM validation_applications WHERE application_id = 'application-1'"
            ).fetchone()[0]
        finally:
            connection.close()
        self.oracle.allowed_head = event_hash
        replay = self.store.apply_validator_observation(request)
        self.assertTrue(replay.replayed)
        self.assertEqual(replay.resulting_state.value, "VALIDATING")
        self.assertEqual(self.store.table_counts()["validation_applications"], 1)
        self.assertEqual(self.store.table_counts()["outstanding_slot"], 1)
        self.store.load_verified("repo-1")

    def test_c05_last_pass_blocks_for_distinct_finalization(self) -> None:
        self._record_validator_result(only_check=True)
        applied = self.store.apply_validator_observation(
            ValidationApplicationRequest(
                "application-1", "apply-command-1", "apply-event-1", "repo-1",
                "run-1", "item-1", "effect-1", "revision-1", "check-1",
                "validator-attempt-1", "validator-observation-1",
            )
        )
        self.assertEqual(applied.resulting_state.value, "BLOCKED")
        self.assertEqual(self.store.table_counts()["outstanding_slot"], 1)

    def test_c05_denies_fail_without_trusted_classification(self) -> None:
        self._record_validator_result(verdict="FAIL")
        with self.assertRaisesRegex(DispatchDenied, "trusted failure classification"):
            self.store.apply_validator_observation(
                ValidationApplicationRequest(
                    "application-1", "apply-command-1", "apply-event-1",
                    "repo-1", "run-1", "item-1", "effect-1", "revision-1",
                    "check-1", "validator-attempt-1",
                    "validator-observation-1",
                )
            )
        self.assertEqual(self.store.table_counts()["validation_applications"], 0)

    def test_c05_recovery_rejects_tampered_application_projection(self) -> None:
        self._record_validator_result(only_check=True)
        applied = self.store.apply_validator_observation(
            ValidationApplicationRequest(
                "application-1", "apply-command-1", "apply-event-1", "repo-1",
                "run-1", "item-1", "effect-1", "revision-1", "check-1",
                "validator-attempt-1", "validator-observation-1",
            )
        )
        self.oracle.allowed_head = applied.event_hash
        connection = sqlite3.connect(self.database_path)
        try:
            connection.execute(
                "UPDATE validation_applications SET revision_digest = 'tampered' "
                "WHERE application_id = 'application-1'"
            )
            connection.commit()
        finally:
            connection.close()
        with self.assertRaisesRegex(StorageIntegrityError, "validation-application"):
            self.store.load_verified("repo-1")

    def test_t27_validator_intent_is_atomic_replay_safe_and_subordinate_to_slot(self) -> None:
        observation = self._record_effect_observation()
        request, capability = self._validator_intent(observation)

        with self.assertRaises(InjectedFailure):
            self.store.commit_validator_intent(
                request,
                capability,
                self.authority,
                failure_hook=raise_at("after_validator_intent_writes_before_commit"),
            )
        self.assertEqual(self.store.table_counts()["validator_intents"], 0)
        self.assertEqual(self.store.table_counts()["budget_reservations"], 1)

        with self.assertRaises(InjectedFailure):
            self.store.commit_validator_intent(
                request,
                capability,
                self.authority,
                failure_hook=raise_at(
                    "after_validator_intent_commit_before_acknowledgement"
                ),
            )
        connection = sqlite3.connect(self.database_path)
        try:
            validator_hash = connection.execute(
                "SELECT event_hash FROM validator_intents WHERE validator_intent_id = 'validator-intent-1'"
            ).fetchone()[0]
        finally:
            connection.close()
        self.oracle.allowed_head = validator_hash
        replay = self.store.commit_validator_intent(
            request, capability, self.authority
        )

        self.assertTrue(replay.replayed)
        self.assertEqual(replay.event_hash, validator_hash)
        self.assertEqual(self.store.table_counts()["validator_intents"], 1)
        self.assertEqual(self.store.table_counts()["budget_reservations"], 2)
        self.assertEqual(self.store.table_counts()["effect_observations"], 1)
        self.assertEqual(self.store.table_counts()["outstanding_slot"], 1)
        self.store.load_verified("repo-1")

    def test_t27_denies_check_not_declared_by_accepted_plan(self) -> None:
        observation = self._record_effect_observation()
        request, capability = self._validator_intent(observation, suffix="3")
        with self.assertRaisesRegex(DispatchDenied, "not declared"):
            self.store.commit_validator_intent(request, capability, self.authority)
        self.assertEqual(self.store.table_counts()["validator_intents"], 0)

    def test_t27_denies_another_active_validator_and_budget_over_cap(self) -> None:
        observation = self._record_effect_observation()
        first_request, first_capability = self._validator_intent(observation)
        first = self.store.commit_validator_intent(
            first_request, first_capability, self.authority
        )
        self.oracle.allowed_head = first.event_hash
        second_request, second_capability = self._validator_intent(
            observation, suffix="2"
        )
        with self.assertRaisesRegex(DispatchDenied, "active"):
            self.store.commit_validator_intent(
                second_request, second_capability, self.authority
            )

        second_store = SQLiteStateStore(
            Path(self.temporary_directory.name) / "budget-state.sqlite3",
            MutableFreshnessOracle(),
            "repo-1",
        )
        second_authority = SyntheticAuthority()
        second_authority.register(
            SyntheticGrant("grant-1", "repo-1", "effect-1", "attempt-1", "scope-1")
        )
        second_capability = second_authority.claim(
            "grant-1", "repo-1", "effect-1", "attempt-1", "scope-1"
        )
        original_store, original_authority, original_capability, original_oracle = (
            self.store,
            self.authority,
            self.capability,
            self.oracle,
        )
        try:
            self.store = second_store
            self.authority = second_authority
            self.capability = second_capability
            self.oracle = second_store._freshness_oracle
            second_observation = self._record_effect_observation()
            over_cap_request, over_cap_capability = self._validator_intent(
                second_observation, cap_units=2
            )
            with self.assertRaisesRegex(DispatchDenied, "budget cap"):
                second_store.commit_validator_intent(
                    over_cap_request, over_cap_capability, second_authority
                )
        finally:
            self.store, self.authority, self.capability, self.oracle = (
                original_store,
                original_authority,
                original_capability,
                original_oracle,
            )

    def test_t27_rejects_stale_parent_and_tampered_projection(self) -> None:
        observation = self._record_effect_observation()
        stale_request, stale_capability = self._validator_intent(observation)
        stale_request = ValidatorIntentRequest(
            **{**stale_request.__dict__, "parent_event_hash": "stale-hash"}
        )
        with self.assertRaisesRegex(DispatchDenied, "parent observation"):
            self.store.commit_validator_intent(
                stale_request, stale_capability, self.authority
            )

        request, capability = self._validator_intent(observation, suffix="2")
        committed = self.store.commit_validator_intent(
            request, capability, self.authority
        )
        self.oracle.allowed_head = committed.event_hash
        connection = sqlite3.connect(self.database_path)
        try:
            connection.execute(
                "UPDATE validator_intents SET input_digest = 'tampered' WHERE validator_intent_id = ?",
                (request.validator_intent_id,),
            )
            connection.commit()
        finally:
            connection.close()
        with self.assertRaisesRegex(StorageIntegrityError, "validator-intent projection"):
            self.store.load_verified("repo-1")

    def test_t27_denies_when_repository_has_derived_dispatch_fence(self) -> None:
        observation = self._record_effect_observation()
        connection = sqlite3.connect(self.database_path)
        try:
            previous_hash = connection.execute(
                "SELECT settlement_head_hash FROM budget_reservations WHERE reservation_id = 'reservation-1'"
            ).fetchone()[0]
        finally:
            connection.close()
        proof = self.authority.issue_settlement_proof(
            "proof-2",
            "reservation-1",
            non_dispatch_proven=False,
            zero_liability_proven=False,
            all_obligations_settled=False,
        )
        breached = self.store.settle_budget(
            BudgetSettlementRequest(
                "settlement-2",
                "reservation-1",
                previous_hash,
                BudgetDisposition.ADJUSTED,
                11,
                "receipt-adjustment-1",
                "AUTHORITATIVE_CORRECTION",
            ),
            proof,
            self.authority,
        )
        self.oracle.allowed_head = breached.settlement_hash
        request, capability = self._validator_intent(
            observation, cap_units=20
        )

        with self.assertRaisesRegex(DispatchDenied, "active dispatch fence"):
            self.store.commit_validator_intent(
                request, capability, self.authority
            )
        self.assertEqual(self.store.table_counts()["validator_intents"], 0)

    def test_t24_result_intake_is_atomic_replay_safe_and_remains_unapplied(self) -> None:
        observation = self._record_effect_observation()
        intent_request, capability = self._validator_intent(observation)
        intent = self.store.commit_validator_intent(
            intent_request, capability, self.authority
        )
        self.oracle.allowed_head = intent.event_hash
        settlement_request = BudgetSettlementRequest(
            "validator-settlement-1",
            "validator-reservation-1",
            "",
            BudgetDisposition.CONSUMED,
            1,
            "validator-result-1",
            "VALIDATOR_USAGE_REPORTED",
        )
        proof = self.authority.issue_settlement_proof(
            "validator-proof-1",
            "validator-reservation-1",
            non_dispatch_proven=False,
            zero_liability_proven=False,
            all_obligations_settled=False,
        )
        settlement = self.store.settle_budget(
            settlement_request, proof, self.authority
        )
        self.oracle.allowed_head = settlement.settlement_hash
        request = ValidatorObservationRequest(
            "validator-observation-1",
            "validator-observe-command-1",
            "validator-observation-event-1",
            "repo-1",
            "run-1",
            "item-1",
            "effect-1",
            "validator-intent-1",
            "validator-attempt-1",
            "validator-result-1",
            capability.claim_id,
            "revision-1",
            "check-1",
            "input-1",
            "result-digest-1",
            "PASS",
            1,
            "validator-settlement-1",
            settlement.settlement_hash,
        )

        with self.assertRaises(InjectedFailure):
            self.store.record_validator_observation(
                request,
                failure_hook=raise_at(
                    "after_validator_observation_writes_before_commit"
                ),
            )
        self.assertEqual(self.store.table_counts()["validator_observations"], 0)

        with self.assertRaises(InjectedFailure):
            self.store.record_validator_observation(
                request,
                failure_hook=raise_at(
                    "after_validator_observation_commit_before_acknowledgement"
                ),
            )
        connection = sqlite3.connect(self.database_path)
        try:
            result = connection.execute(
                "SELECT event_hash, applied FROM validator_observations WHERE observation_id = ?",
                (request.observation_id,),
            ).fetchone()
            status = connection.execute(
                "SELECT status FROM validator_intents WHERE validator_intent_id = ?",
                (request.validator_intent_id,),
            ).fetchone()[0]
        finally:
            connection.close()
        self.oracle.allowed_head = result[0]
        replay = self.store.record_validator_observation(request)

        self.assertTrue(replay.replayed)
        self.assertEqual(result[1], 0)
        self.assertEqual(status, "ACTIVE")
        self.assertEqual(self.store.table_counts()["outstanding_slot"], 1)
        self.store.load_verified("repo-1")

    def test_active_validator_obligation_denies_operation_slot_release(self) -> None:
        observation = self._record_effect_observation()
        intent_request, capability = self._validator_intent(observation)
        intent = self.store.commit_validator_intent(
            intent_request, capability, self.authority
        )
        self.oracle.allowed_head = intent.event_hash
        connection = sqlite3.connect(self.database_path)
        try:
            previous_hash = connection.execute(
                "SELECT settlement_head_hash FROM budget_reservations WHERE reservation_id = 'reservation-1'"
            ).fetchone()[0]
        finally:
            connection.close()
        proof = self.authority.issue_settlement_proof(
            "release-proof-1",
            "reservation-1",
            non_dispatch_proven=False,
            zero_liability_proven=False,
            all_obligations_settled=True,
        )

        with self.assertRaisesRegex(DispatchDenied, "validator obligation"):
            self.store.settle_budget(
                BudgetSettlementRequest(
                    "release-settlement-1", "reservation-1", previous_hash,
                    BudgetDisposition.CONSUMED, 2, "receipt-1",
                    "ALL_OPERATION_OBLIGATIONS_CLAIMED_SETTLED",
                    release_slot=True, all_obligations_settled=True,
                ),
                proof,
                self.authority,
            )

        self.assertEqual(self.store.table_counts()["outstanding_slot"], 1)
        self.assertEqual(self.store.table_counts()["budget_settlements"], 1)

    def test_t24_unknown_validator_usage_is_recorded_unapplied_for_reconciliation(self) -> None:
        observation = self._record_effect_observation()
        intent_request, capability = self._validator_intent(observation)
        intent = self.store.commit_validator_intent(
            intent_request, capability, self.authority
        )
        self.oracle.allowed_head = intent.event_hash
        proof = self.authority.issue_settlement_proof(
            "validator-proof-1", "validator-reservation-1",
            non_dispatch_proven=False, zero_liability_proven=False,
            all_obligations_settled=False,
        )
        settlement = self.store.settle_budget(
            BudgetSettlementRequest(
                "validator-settlement-1", "validator-reservation-1", "",
                BudgetDisposition.UNKNOWN_WORST_CASE_CHARGED, None,
                "validator-result-unknown-1", "VALIDATOR_USAGE_UNKNOWN",
            ),
            proof,
            self.authority,
        )
        self.oracle.allowed_head = settlement.settlement_hash

        recorded = self.store.record_validator_observation(
            ValidatorObservationRequest(
                "validator-observation-unknown-1", "validator-observe-unknown-command-1",
                "validator-observation-unknown-event-1", "repo-1", "run-1",
                "item-1", "effect-1", "validator-intent-1",
                "validator-attempt-1", "validator-result-unknown-1",
                capability.claim_id, "revision-1", "check-1", "input-1",
                "result-digest-unknown-1", "FAIL", None,
                "validator-settlement-1", settlement.settlement_hash,
            )
        )

        self.assertEqual(recorded.resulting_state.value, "RECONCILIATION_REQUIRED")
        connection = sqlite3.connect(self.database_path)
        try:
            row = connection.execute(
                "SELECT applied FROM validator_observations WHERE observation_id = ?",
                ("validator-observation-unknown-1",),
            ).fetchone()
            status = connection.execute(
                "SELECT status FROM validator_intents WHERE validator_intent_id = 'validator-intent-1'"
            ).fetchone()[0]
        finally:
            connection.close()
        self.assertEqual(row[0], 0)
        self.assertEqual(status, "ACTIVE")
        self.assertEqual(self.store.table_counts()["outstanding_slot"], 1)

    def test_consumed_settlement_can_release_slot_and_recover(self) -> None:
        committed = self.store.commit_intent(
            self.request(), self.capability, self.authority, expected_head="", writer_epoch=1
        )
        self.oracle.allowed_head = committed.event_hash
        request = BudgetSettlementRequest(
            "settlement-1",
            "reservation-1",
            "",
            BudgetDisposition.CONSUMED,
            2,
            "usage-evidence",
            "USAGE_REPORTED",
            release_slot=True,
            all_obligations_settled=True,
        )
        proof = self.authority.issue_settlement_proof(
            "proof-1",
            "reservation-1",
            non_dispatch_proven=False,
            zero_liability_proven=False,
            all_obligations_settled=True,
        )
        receipt = self.store.settle_budget(request, proof, self.authority)
        self.oracle.allowed_head = receipt.settlement_hash
        self.assertTrue(receipt.slot_released)
        self.assertEqual(self.store.table_counts()["outstanding_slot"], 0)
        self.store.load_verified("repo-1")

    def test_budget_breach_fence_denies_new_intent_after_slot_release(self) -> None:
        committed = self.store.commit_intent(
            self.request(), self.capability, self.authority, expected_head="", writer_epoch=1
        )
        self.oracle.allowed_head = committed.event_hash
        settlement = BudgetSettlementRequest(
            "settlement-1",
            "reservation-1",
            "",
            BudgetDisposition.CONSUMED,
            11,
            "usage-evidence",
            "USAGE_REPORTED",
            release_slot=True,
            all_obligations_settled=True,
        )
        proof = self.authority.issue_settlement_proof(
            "proof-1",
            "reservation-1",
            non_dispatch_proven=False,
            zero_liability_proven=False,
            all_obligations_settled=True,
        )
        settlement_receipt = self.store.settle_budget(
            settlement, proof, self.authority
        )
        self.oracle.allowed_head = settlement_receipt.settlement_hash
        second_authority = SyntheticAuthority()
        second_authority.register(
            SyntheticGrant(
                "grant-2", "repo-1", "effect-2", "attempt-2", "scope-2"
            )
        )
        second_capability = second_authority.claim(
            "grant-2", "repo-1", "effect-2", "attempt-2", "scope-2"
        )
        second_request = IntentRequest(
            **{
                **self.request().__dict__,
                "run_id": "run-2",
                "item_id": "item-2",
                "command_id": "command-2",
                "event_id": "event-2",
                "logical_effect_id": "effect-2",
                "attempt_id": "attempt-2",
                "permission_use_id": "permission-use-2",
                "reservation_id": "reservation-2",
            }
        )
        with self.assertRaisesRegex(DispatchDenied, "dispatch fence"):
            self.store.commit_intent(
                second_request,
                second_capability,
                second_authority,
                expected_head=settlement_receipt.settlement_hash,
                writer_epoch=2,
            )

    def test_freshness_rejects_snapshot_missing_complete_settlement_tail(self) -> None:
        committed = self.store.commit_intent(
            self.request(), self.capability, self.authority, expected_head="", writer_epoch=1
        )
        self.oracle.allowed_head = committed.event_hash
        snapshot_path = Path(self.temporary_directory.name) / "pre-settlement.sqlite3"
        shutil.copy2(self.database_path, snapshot_path)
        settlement = BudgetSettlementRequest(
            "settlement-1",
            "reservation-1",
            "",
            BudgetDisposition.CONSUMED,
            2,
            "usage-evidence",
            "USAGE_REPORTED",
        )
        proof = self.authority.issue_settlement_proof(
            "proof-1",
            "reservation-1",
            non_dispatch_proven=False,
            zero_liability_proven=False,
            all_obligations_settled=False,
        )
        settlement_receipt = self.store.settle_budget(
            settlement, proof, self.authority
        )
        self.oracle.allowed_head = settlement_receipt.settlement_hash
        stale_store = SQLiteStateStore(snapshot_path, self.oracle, "repo-1")
        with self.assertRaisesRegex(DispatchDenied, "freshness"):
            stale_store.load_verified("repo-1")

    def test_late_accounting_after_release_does_not_restore_slot_obligation(self) -> None:
        committed = self.store.commit_intent(
            self.request(), self.capability, self.authority, expected_head="", writer_epoch=1
        )
        self.oracle.allowed_head = committed.event_hash
        first = BudgetSettlementRequest(
            "settlement-1",
            "reservation-1",
            "",
            BudgetDisposition.CONSUMED,
            2,
            "initial-usage",
            "USAGE_REPORTED",
            release_slot=True,
            all_obligations_settled=True,
        )
        first_proof = self.authority.issue_settlement_proof(
            "proof-1",
            "reservation-1",
            non_dispatch_proven=False,
            zero_liability_proven=False,
            all_obligations_settled=True,
        )
        first_receipt = self.store.settle_budget(first, first_proof, self.authority)
        self.oracle.allowed_head = first_receipt.settlement_hash
        late = BudgetSettlementRequest(
            "settlement-2",
            "reservation-1",
            first_receipt.settlement_hash,
            BudgetDisposition.ADJUSTED,
            3,
            "late-usage",
            "LATE_USAGE_REPORTED",
        )
        late_proof = self.authority.issue_settlement_proof(
            "proof-2",
            "reservation-1",
            non_dispatch_proven=False,
            zero_liability_proven=False,
            all_obligations_settled=False,
        )
        late_receipt = self.store.settle_budget(late, late_proof, self.authority)
        self.oracle.allowed_head = late_receipt.settlement_hash

        self.assertEqual(self.store.table_counts()["outstanding_slot"], 0)
        self.store.load_verified("repo-1")


if __name__ == "__main__":
    unittest.main()