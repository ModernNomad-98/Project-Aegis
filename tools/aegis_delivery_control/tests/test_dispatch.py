from __future__ import annotations

import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from tools.aegis_delivery_control.adapters import (
    SyntheticEffectRequest,
    SyntheticExecutionAdapter,
    SyntheticValidatorAdapter,
    SyntheticValidatorRequest,
)
from tools.aegis_delivery_control.authority import (
    SyntheticAuthority,
    SyntheticCapability,
    SyntheticGrant,
    SyntheticValidatorGrant,
)
from tools.aegis_delivery_control.contracts import (
    BudgetDisposition,
    BudgetSettlementRequest,
    DispatchDenied,
    EffectObservationCommand,
    InjectedFailure,
    IntentRequest,
    PlanAcceptanceRequest,
    ValidationApplicationRequest,
    ValidatorIntentRequest,
    ValidatorObservationCommand,
)
from tools.aegis_delivery_control.dispatch import (
    SyntheticDispatchCoordinator,
    SyntheticValidationCoordinator,
)
from tools.aegis_delivery_control.engine import TransitionEngine
from tools.aegis_delivery_control.storage import SQLiteStateStore


class AlwaysFreshOracle:
    def verify(self, repository_id, catalog_head, run_heads):
        return repository_id == "repo-1"


class MediatedDispatchTests(unittest.TestCase):
    @staticmethod
    def state_environment(root: Path) -> dict[str, str]:
        if sys.platform == "win32":
            return {"LOCALAPPDATA": str(root)}
        return {"XDG_STATE_HOME": str(root)}

    def test_shared_store_allows_only_one_cross_instance_dispatch(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            issuer_key = b"synthetic-test-issuer-key-32-bytes"
            grant = SyntheticGrant(
                "grant-1", "repo-1", "effect-1", "attempt-1", "scope-1"
            )
            first_authority = SyntheticAuthority(issuer_key)
            second_authority = SyntheticAuthority(issuer_key)
            first_authority.register(grant)
            second_authority.register(grant)
            first_capability = first_authority.claim(*grant.__dict__.values())
            second_capability = second_authority.claim(*grant.__dict__.values())
            request = IntentRequest(
                repository_id="repo-1",
                run_id="run-1",
                item_id="item-1",
                command_id="command-1",
                event_id="event-1",
                logical_effect_id="effect-1",
                effect_descriptor_digest="payload-1",
                attempt_id="attempt-1",
                permission_use_id="permission-1",
                reservation_id="reservation-1",
                budget_policy_digest="budget-1",
                reserved_units=1,
                worst_case_units=1,
                cap_units=2,
            )
            effect = SyntheticEffectRequest(
                repository_id="repo-1",
                logical_effect_id="effect-1",
                attempt_id="attempt-1",
                scope_digest="scope-1",
                payload_digest="payload-1",
            )
            with patch.dict(os.environ, self.state_environment(root)):
                first = SyntheticDispatchCoordinator(
                    SQLiteStateStore.open_canonical("repo-1", AlwaysFreshOracle()),
                    TransitionEngine(),
                    first_authority,
                    SyntheticExecutionAdapter.open_canonical("repo-1"),
                )
                second = SyntheticDispatchCoordinator(
                    SQLiteStateStore.open_canonical("repo-1", AlwaysFreshOracle()),
                    TransitionEngine(),
                    second_authority,
                    SyntheticExecutionAdapter.open_canonical("repo-1"),
                )

            first.dispatch(
                request,
                first_capability,
                effect,
                expected_head="",
                writer_epoch=1,
            )

            with self.assertRaisesRegex(DispatchDenied, "already redeemed"):
                second.dispatch(
                    request,
                    second_capability,
                    effect,
                    expected_head="",
                    writer_epoch=2,
                )

    def test_alternate_state_and_target_roots_are_denied(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            authority = SyntheticAuthority()
            with patch.dict(os.environ, self.state_environment(root)):
                canonical_store = SQLiteStateStore.open_canonical(
                    "repo-1", AlwaysFreshOracle()
                )
                canonical_adapter = SyntheticExecutionAdapter.open_canonical("repo-1")
                alternate_store = SQLiteStateStore(
                    root / "alternate" / "state.sqlite3",
                    AlwaysFreshOracle(),
                    "repo-1",
                )
                alternate_adapter = SyntheticExecutionAdapter(
                    root / "alternate" / "target.sqlite3"
                )

                with self.assertRaisesRegex(DispatchDenied, "canonical repository root"):
                    SyntheticDispatchCoordinator(
                        alternate_store,
                        TransitionEngine(),
                        authority,
                        canonical_adapter,
                    )

                coordinator = SyntheticDispatchCoordinator(
                    canonical_store,
                    TransitionEngine(),
                    authority,
                    alternate_adapter,
                )
                with self.assertRaisesRegex(DispatchDenied, "canonical repository root"):
                    coordinator.dispatch(
                        IntentRequest(
                            "repo-1", "run-1", "item-1", "command-1", "event-1",
                            "effect-1", "payload-1", "attempt-1", "permission-1",
                            "reservation-1", "budget-1", 1, 1, 2,
                        ),
                        SyntheticCapability(
                            "claim", "grant", "repo-1", "effect-1", "attempt-1",
                            "scope-1", "untrusted",
                        ),
                        SyntheticEffectRequest(
                            "repo-1", "effect-1", "attempt-1", "scope-1", "payload-1"
                        ),
                        expected_head="",
                        writer_epoch=1,
                    )

    def test_unissued_capability_denies_before_state_or_adapter_contact(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            authority = SyntheticAuthority()
            grant = SyntheticGrant(
                "grant-1", "repo-1", "effect-1", "attempt-1", "scope-1"
            )
            authority.register(grant)
            capability = SyntheticCapability(
                "claim", "grant-1", "repo-1", "effect-1", "attempt-1",
                "scope-1", "untrusted",
            )
            with patch.dict(os.environ, self.state_environment(root)):
                store = SQLiteStateStore.open_canonical("repo-1", AlwaysFreshOracle())
                coordinator = SyntheticDispatchCoordinator(
                    store,
                    TransitionEngine(),
                    authority,
                    SyntheticExecutionAdapter.open_canonical("repo-1"),
                )

            with self.assertRaisesRegex(DispatchDenied, "not issued"):
                coordinator.dispatch(
                    IntentRequest(
                        "repo-1", "run-1", "item-1", "command-1", "event-1",
                        "effect-1", "payload-1", "attempt-1", "permission-1",
                        "reservation-1", "budget-1", 1, 1, 2,
                    ),
                    capability,
                    SyntheticEffectRequest(
                        "repo-1", "effect-1", "attempt-1", "scope-1", "payload-1"
                    ),
                    expected_head="",
                    writer_epoch=1,
                )

            self.assertEqual(sum(store.table_counts().values()), 0)

    def test_c02_crash_after_intent_before_target_contact_denies_redispatch(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            authority = SyntheticAuthority()
            grant = SyntheticGrant(
                "grant-1", "repo-1", "effect-1", "attempt-1", "scope-1"
            )
            authority.register(grant)
            capability = authority.claim(*grant.__dict__.values())
            with patch.dict(os.environ, self.state_environment(root)):
                store = SQLiteStateStore.open_canonical("repo-1", AlwaysFreshOracle())
                adapter = SyntheticExecutionAdapter.open_canonical("repo-1")
                coordinator = SyntheticDispatchCoordinator(
                    store, TransitionEngine(), authority, adapter
                )
            intent = IntentRequest(
                "repo-1", "run-1", "item-1", "command-1", "event-1",
                "effect-1", "payload-1", "attempt-1", "permission-1",
                "reservation-1", "budget-1", 1, 1, 2,
            )
            effect = SyntheticEffectRequest(
                "repo-1", "effect-1", "attempt-1", "scope-1", "payload-1"
            )

            with self.assertRaises(InjectedFailure):
                coordinator.dispatch(
                    intent,
                    capability,
                    effect,
                    expected_head="",
                    writer_epoch=1,
                    before_adapter_hook=lambda: (_ for _ in ()).throw(
                        InjectedFailure("before_adapter_contact")
                    ),
                )

            self.assertIsNone(
                SyntheticExecutionAdapter.open_canonical("repo-1").reconcile(
                    capability.claim_id
                )
            )
            with self.assertRaisesRegex(DispatchDenied, "already redeemed"):
                coordinator.dispatch(
                    intent,
                    capability,
                    effect,
                    expected_head="",
                    writer_epoch=2,
                )

    def test_c04_lost_receipt_is_intaken_from_canonical_ledger_without_redispatch(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            authority = SyntheticAuthority()
            grant = SyntheticGrant(
                "grant-1", "repo-1", "effect-1", "attempt-1", "scope-1"
            )
            authority.register(grant)
            capability = authority.claim(*grant.__dict__.values())
            with patch.dict(os.environ, self.state_environment(root)):
                store = SQLiteStateStore.open_canonical("repo-1", AlwaysFreshOracle())
                adapter = SyntheticExecutionAdapter.open_canonical("repo-1")
                coordinator = SyntheticDispatchCoordinator(
                    store, TransitionEngine(), authority, adapter
                )
            intent = IntentRequest(
                "repo-1", "run-1", "item-1", "command-1", "event-1",
                "effect-1", "payload-1", "attempt-1", "permission-1",
                "reservation-1", "budget-1", 1, 1, 2,
            )
            dispatched = coordinator.dispatch(
                intent,
                capability,
                SyntheticEffectRequest(
                    "repo-1", "effect-1", "attempt-1", "scope-1", "payload-1"
                ),
                expected_head="",
                writer_epoch=1,
                usage_units=1,
                lose_receipt=True,
            )
            self.assertIsNone(dispatched.effect)
            settlement_request = BudgetSettlementRequest(
                "settlement-1",
                "reservation-1",
                "",
                BudgetDisposition.CONSUMED,
                1,
                adapter.reconcile(capability.claim_id).receipt_id,
                "USAGE_REPORTED",
            )
            proof = authority.issue_settlement_proof(
                "proof-1",
                "reservation-1",
                non_dispatch_proven=False,
                zero_liability_proven=False,
                all_obligations_settled=False,
            )
            settlement = store.settle_budget(
                settlement_request, proof, authority
            )
            command = EffectObservationCommand(
                "observation-1",
                "observe-command-1",
                "observation-event-1",
                "repo-1",
                "run-1",
                "item-1",
                "effect-1",
                "attempt-1",
                capability.claim_id,
                "settlement-1",
                settlement.settlement_hash,
            )

            receipt = coordinator.intake_effect_receipt(command)
            replay = coordinator.intake_effect_receipt(command)

            self.assertFalse(receipt.replayed)
            self.assertTrue(replay.replayed)
            self.assertEqual(receipt.event_hash, replay.event_hash)
            self.assertEqual(store.table_counts()["effect_observations"], 1)
            self.assertEqual(store.table_counts()["outstanding_slot"], 1)
            with self.assertRaisesRegex(DispatchDenied, "already redeemed"):
                coordinator.dispatch(
                    intent,
                    capability,
                    SyntheticEffectRequest(
                        "repo-1", "effect-1", "attempt-1", "scope-1", "payload-1"
                    ),
                    expected_head=receipt.event_hash,
                    writer_epoch=2,
                )

    def test_c04_canonical_receipt_cannot_be_substituted_across_attempts(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            with patch.dict(os.environ, self.state_environment(root)):
                store = SQLiteStateStore.open_canonical("repo-1", AlwaysFreshOracle())
                adapter = SyntheticExecutionAdapter.open_canonical("repo-1")
                coordinator = SyntheticDispatchCoordinator(
                    store, TransitionEngine(), SyntheticAuthority(), adapter
                )
            command = EffectObservationCommand(
                "observation-1", "observe-command-1", "observation-event-1",
                "repo-1", "run-1", "item-1", "effect-1", "attempt-2",
                "missing-claim", "settlement-1", "settlement-hash",
            )
            with self.assertRaisesRegex(DispatchDenied, "unavailable"):
                coordinator.intake_effect_receipt(command)
            self.assertEqual(store.table_counts()["effect_observations"], 0)

    def test_t24_lost_validator_result_can_be_applied_and_replayed(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            authority = SyntheticAuthority()
            operation_grant = SyntheticGrant(
                "grant-1", "repo-1", "effect-1", "attempt-1", "scope-1"
            )
            authority.register(operation_grant)
            operation_capability = authority.claim(*operation_grant.__dict__.values())
            with patch.dict(os.environ, self.state_environment(root)):
                store = SQLiteStateStore.open_canonical("repo-1", AlwaysFreshOracle())
                dispatch = SyntheticDispatchCoordinator(
                    store,
                    TransitionEngine(),
                    authority,
                    SyntheticExecutionAdapter.open_canonical("repo-1"),
                )
                validator_adapter = SyntheticValidatorAdapter.open_canonical("repo-1")
                validation = SyntheticValidationCoordinator(
                    store, TransitionEngine(), authority, validator_adapter
                )
            plan = store.accept_plan(
                PlanAcceptanceRequest(
                    "plan-1", "plan-command-1", "plan-event-1", "repo-1",
                    "run-1", "item-1", "effect-1", "revision-1", ("check-1",),
                ),
                expected_head="",
                writer_epoch=1,
            )
            operation = dispatch.dispatch(
                IntentRequest(
                    "repo-1", "run-1", "item-1", "command-1", "event-1",
                    "effect-1", "payload-1", "attempt-1", "permission-1",
                    "reservation-1", "budget-1", 1, 1, 10,
                ),
                operation_capability,
                SyntheticEffectRequest(
                    "repo-1", "effect-1", "attempt-1", "scope-1", "payload-1"
                ),
                expected_head=plan.event_hash,
                writer_epoch=2,
                usage_units=1,
            )
            operation_settlement = store.settle_budget(
                BudgetSettlementRequest(
                    "settlement-1", "reservation-1", "",
                    BudgetDisposition.CONSUMED, 1, operation.effect.receipt_id,
                    "USAGE_REPORTED",
                ),
                authority.issue_settlement_proof(
                    "proof-1", "reservation-1", non_dispatch_proven=False,
                    zero_liability_proven=False, all_obligations_settled=False,
                ),
                authority,
            )
            operation_observation = dispatch.intake_effect_receipt(
                EffectObservationCommand(
                    "observation-1", "observe-command-1", "observation-event-1",
                    "repo-1", "run-1", "item-1", "effect-1", "attempt-1",
                    operation_capability.claim_id, "settlement-1",
                    operation_settlement.settlement_hash,
                )
            )
            validator_grant = SyntheticValidatorGrant(
                "validator-grant-1", "repo-1", "effect-1", "revision-1",
                "check-1", "input-1", "validator-attempt-1", "read-only-1",
            )
            authority.register_validator(validator_grant)
            validator_capability = authority.claim_validator(
                *validator_grant.__dict__.values()
            )
            validator_intent = ValidatorIntentRequest(
                "validator-intent-1", "validator-command-1", "validator-event-1",
                "repo-1", "run-1", "item-1", "effect-1", "attempt-1",
                "observation-1", operation_observation.event_hash,
                "revision-1", "check-1", "input-1", "validator-attempt-1",
                "validator-permission-1", "validator-reservation-1",
                "validator-budget-1", 1, 1, 10,
            )
            launched = validation.launch(
                validator_intent,
                validator_capability,
                SyntheticValidatorRequest(
                    "repo-1", "effect-1", "revision-1", "check-1", "input-1",
                    "validator-attempt-1", "read-only-1", "result-digest-1", "PASS",
                ),
                usage_units=1,
                lose_result=True,
            )
            self.assertIsNone(launched.result)
            result = validator_adapter.reconcile(validator_capability.claim_id)
            validator_settlement = store.settle_budget(
                BudgetSettlementRequest(
                    "validator-settlement-1", "validator-reservation-1", "",
                    BudgetDisposition.CONSUMED, 1, result.result_id,
                    "VALIDATOR_USAGE_REPORTED",
                ),
                authority.issue_settlement_proof(
                    "validator-proof-1", "validator-reservation-1",
                    non_dispatch_proven=False, zero_liability_proven=False,
                    all_obligations_settled=False,
                ),
                authority,
            )
            recorded = validation.intake_result(
                ValidatorObservationCommand(
                    "validator-observation-1", "validator-observe-command-1",
                    "validator-observation-event-1", "repo-1", "run-1", "item-1",
                    "validator-intent-1", "validator-settlement-1",
                    validator_settlement.settlement_hash,
                )
            )
            replay = validation.intake_result(
                ValidatorObservationCommand(
                    "validator-observation-1", "validator-observe-command-1",
                    "validator-observation-event-1", "repo-1", "run-1", "item-1",
                    "validator-intent-1", "validator-settlement-1",
                    validator_settlement.settlement_hash,
                )
            )

            self.assertFalse(recorded.replayed)
            self.assertTrue(replay.replayed)
            self.assertEqual(store.table_counts()["validator_observations"], 1)
            self.assertEqual(store.table_counts()["outstanding_slot"], 1)
            applied = validation.apply_result(
                ValidationApplicationRequest(
                    "application-1", "apply-command-1", "apply-event-1",
                    "repo-1", "run-1", "item-1", "effect-1", "revision-1",
                    "check-1", "validator-attempt-1",
                    "validator-observation-1",
                )
            )
            replay_after_apply = validation.intake_result(
                ValidatorObservationCommand(
                    "validator-observation-1", "validator-observe-command-1",
                    "validator-observation-event-1", "repo-1", "run-1",
                    "item-1", "validator-intent-1", "validator-settlement-1",
                    validator_settlement.settlement_hash,
                )
            )
            self.assertEqual(applied.resulting_state.value, "BLOCKED")
            self.assertTrue(replay_after_apply.replayed)
            self.assertEqual(store.table_counts()["validation_applications"], 1)


if __name__ == "__main__":
    unittest.main()