from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor
import json
import multiprocessing
import os
import sqlite3
import subprocess
import sys
import tempfile
import threading
import unittest
from dataclasses import replace
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
    SyntheticOperatorGrant,
    SyntheticValidatorGrant,
)
from tools.aegis_delivery_control.contracts import (
    ApplicationReceipt,
    BudgetDisposition,
    BudgetSettlementRequest as BudgetSettlementContract,
    BindingMismatchKind,
    BindingMismatchRequest,
    CommitReceipt,
    DispatchDenied,
    EffectObservationCommand,
    FinalizeOperationRequest,
    InjectedFailure,
    IntentRequest,
    LifecycleState,
    PauseExternalMutationRequest,
    PauseLocalExecutionRequest,
    PlanAcceptanceRequest as PlanAcceptanceContract,
    StopMode,
    StopEscalationRequest,
    StopEscalationSettlement,
    StopRequest,
    ValidationApplicationRequest,
    ValidatorIntentRequest,
    ValidatorObservationCommand,
)
from tools.aegis_delivery_control.dispatch import (
    SyntheticDispatchCoordinator,
    SyntheticFinalizationCoordinator,
    SyntheticValidationCoordinator,
)
from tools.aegis_delivery_control.engine import TransitionEngine
from tools.aegis_delivery_control.storage import SQLiteStateStore, raise_at


def BudgetSettlementRequest(*args, **kwargs):
    kwargs.setdefault("repository_id", "repo-1")
    kwargs.setdefault("run_id", "run-1")
    kwargs.setdefault("item_id", "item-1")
    kwargs.setdefault("logical_effect_id", "effect-1")
    kwargs.setdefault("attempt_id", "attempt-1")
    return BudgetSettlementContract(*args, **kwargs)


def PlanAcceptanceRequest(*args, **kwargs):
    """Build a newly accepted synthetic plan with explicit immutable pins."""
    kwargs.setdefault("source_tree_digest", "source-tree-1")
    kwargs.setdefault("item_definition_digest", "item-definition-1")
    kwargs.setdefault("plan_schema_version", "plan-schema-1")
    kwargs.setdefault("reducer_version", "reducer-1")
    return PlanAcceptanceContract(*args, **kwargs)


class AlwaysFreshOracle:
    def verify(self, repository_id, catalog_head, run_heads):
        return repository_id == "repo-1"


def _launch_validator_until_terminated(
    root,
    issuer_key,
    grant,
    intent,
    request,
    ready,
    errors,
):
    environment = (
        {"LOCALAPPDATA": str(root)}
        if sys.platform == "win32"
        else {"XDG_STATE_HOME": str(root)}
    )
    try:
        authority = SyntheticAuthority(issuer_key)
        authority.register_validator(grant)
        capability = authority.claim_validator(*grant.__dict__.values())
        with patch.dict(os.environ, environment):
            store = SQLiteStateStore.open_canonical(
                "repo-1", AlwaysFreshOracle()
            )
            adapter = SyntheticValidatorAdapter.open_canonical("repo-1")
            coordinator = SyntheticValidationCoordinator(
                store, TransitionEngine(), authority, adapter
            )

        def hold_before_contact(*args, **kwargs):
            ready.set()
            threading.Event().wait()

        with patch.object(
            adapter, "_execute_committed", side_effect=hold_before_contact
        ):
            coordinator.launch(intent, capability, request, usage_units=1)
    except BaseException as error:
        errors.put(repr(error))
        raise


class MediatedDispatchTests(unittest.TestCase):
    def test_t07_coordinator_exposes_activity_pause_settlement_route(self) -> None:
        self.assertTrue(
            hasattr(SyntheticDispatchCoordinator, "settle_activity_pause"),
            "T07 requires a coordinator-owned activity settlement route",
        )

    def test_t05_coordinator_exposes_local_execution_pause_route(self) -> None:
        self.assertTrue(
            hasattr(SyntheticDispatchCoordinator, "pause_local_execution"),
            "T05 requires a coordinator-owned local execution pause route",
        )

    def test_t05_coordinator_commits_prelaunch_pause_without_adapter_contact(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            store = SQLiteStateStore(
                root / "state.sqlite3", AlwaysFreshOracle(), "repo-1"
            )
            store._is_canonical = True
            authority = SyntheticAuthority()
            adapter = SyntheticExecutionAdapter(root / "target.sqlite3")
            coordinator = SyntheticDispatchCoordinator(
                store, TransitionEngine(), authority, adapter
            )
            effect_grant = SyntheticGrant(
                "grant-1", "repo-1", "effect-1", "attempt-1", "scope-1"
            )
            authority.register(effect_grant)
            effect_capability = authority.claim(*effect_grant.__dict__.values())
            intent = IntentRequest(
                "repo-1", "run-1", "item-1", "command-1", "event-1",
                "effect-1", "descriptor-1", "attempt-1", "permission-1",
                "reservation-1", "budget-1", 1, 2, 5,
            )
            plan = self._accept_operation_plan(store, intent)
            committed = store.commit_intent(
                intent, effect_capability, authority,
                expected_head=plan.event_hash, writer_epoch=2,
            )
            pause_grant = SyntheticOperatorGrant(
                "pause-grant-1", "repo-1", "run-1", "PAUSE",
                "pause-scope-1",
            )
            authority.register_operator(pause_grant)
            receipt = coordinator.pause_local_execution(
                PauseLocalExecutionRequest(
                    "pause-1", "pause-command-1", "pause-event-1",
                    "pause-fence-1", "repo-1", "run-1", "item-1",
                    "effect-1", "attempt-1", committed.event_id,
                    committed.event_hash, 1, "OPERATOR_PAUSE_LOCAL_EXECUTION",
                ),
                authority.claim_operator(*pause_grant.__dict__.values()),
            )
            self.assertEqual(receipt.resulting_state, LifecycleState.PAUSING)
            self.assertIsNone(
                adapter.reconcile(effect_capability.claim_id),
                "T05 pause must not contact the synthetic target",
            )

    def test_t06_contact_without_intaken_receipt_is_fenced_and_worst_case_charged(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            authority = SyntheticAuthority()
            effect_grant = SyntheticGrant(
                "grant-1", "repo-1", "effect-1", "attempt-1", "scope-1"
            )
            authority.register(effect_grant)
            effect_capability = authority.claim(*effect_grant.__dict__.values())
            with patch.dict(os.environ, self.state_environment(root)):
                store = SQLiteStateStore.open_canonical(
                    "repo-1", AlwaysFreshOracle()
                )
                adapter = SyntheticExecutionAdapter.open_canonical("repo-1")
            coordinator = SyntheticDispatchCoordinator(
                store, TransitionEngine(), authority, adapter
            )
            intent = IntentRequest(
                "repo-1", "run-1", "item-1", "command-1", "event-1",
                "effect-1", "payload-1", "attempt-1", "permission-1",
                "reservation-1", "budget-1", 1, 2, 5,
            )
            plan = self._accept_operation_plan(store, intent)
            dispatched = coordinator.dispatch(
                intent,
                effect_capability,
                SyntheticEffectRequest(
                    "repo-1", "effect-1", "attempt-1", "scope-1", "payload-1"
                ),
                expected_head=plan.event_hash,
                writer_epoch=2,
                usage_units=1,
                lose_receipt=True,
            )
            self.assertIsNone(dispatched.effect)
            canonical_before_pause = adapter.reconcile(effect_capability.claim_id)
            self.assertIsNotNone(canonical_before_pause)
            connection = sqlite3.connect(store._database_path)
            connection.row_factory = sqlite3.Row
            try:
                launch = connection.execute(
                    "SELECT * FROM operation_launches WHERE run_id = 'run-1'"
                ).fetchone()
                contact = connection.execute(
                    "SELECT * FROM adapter_contacts WHERE run_id = 'run-1'"
                ).fetchone()
            finally:
                connection.close()
            pause_grant = SyntheticOperatorGrant(
                "pause-grant-t06", "repo-1", "run-1", "PAUSE", "pause-scope-t06"
            )
            authority.register_operator(pause_grant)
            receipt = coordinator.pause_external_mutation(
                PauseExternalMutationRequest(
                    "external-pause-1", "external-pause-command-1",
                    "external-pause-event-1", "external-pause-fence-1",
                    "repo-1", "run-1", "item-1", "effect-1", "attempt-1",
                    dispatched.intent.event_id, dispatched.intent.event_hash,
                    launch["launch_id"], launch["event_id"], launch["event_hash"],
                    contact["contact_id"], contact["event_id"],
                    contact["event_hash"], contact["target_digest"], 1,
                    "OPERATOR_PAUSE_EXTERNAL_MUTATION",
                ),
                authority.claim_operator(*pause_grant.__dict__.values()),
            )
            self.assertEqual(
                receipt.resulting_state, LifecycleState.RECONCILIATION_REQUIRED
            )
            connection = sqlite3.connect(store._database_path)
            try:
                reservation = connection.execute(
                    "SELECT disposition, held_units, charged_units, uncertainty "
                    "FROM budget_reservations WHERE reservation_id = 'reservation-1'"
                ).fetchone()
                slot_count = connection.execute(
                    "SELECT COUNT(*) FROM outstanding_slot"
                ).fetchone()[0]
                fence_count = connection.execute(
                    "SELECT COUNT(*) FROM dispatch_fences WHERE fence_id = "
                    "'external-pause-fence-1'"
                ).fetchone()[0]
            finally:
                connection.close()
            self.assertEqual(
                reservation, ("UNKNOWN_WORST_CASE_CHARGED", 0, 2, 1)
            )
            self.assertEqual(slot_count, 1)
            self.assertEqual(fence_count, 1)
            self.assertEqual(
                adapter.reconcile(effect_capability.claim_id),
                canonical_before_pause,
                "T06 must not contact, cancel, or mutate the target ledger",
            )
            late = coordinator.intake_effect_receipt(
                EffectObservationCommand(
                    "late-observation-1", "late-observation-command-1",
                    "late-observation-event-1", "repo-1", "run-1", "item-1",
                    "effect-1", "attempt-1", effect_capability.claim_id,
                    "late-settlement-1", "",
                )
            )
            self.assertEqual(
                late.resulting_state, LifecycleState.RECONCILIATION_REQUIRED
            )
            connection = sqlite3.connect(store._database_path)
            try:
                adjusted = connection.execute(
                    "SELECT disposition, charged_units, uncertainty FROM "
                    "budget_reservations WHERE reservation_id = 'reservation-1'"
                ).fetchone()
                event_kind = connection.execute(
                    "SELECT event_kind FROM events WHERE event_id = "
                    "'late-observation-event-1'"
                ).fetchone()[0]
                retained = connection.execute(
                    "SELECT (SELECT COUNT(*) FROM outstanding_slot), "
                    "(SELECT COUNT(*) FROM dispatch_fences WHERE fence_id = "
                    "'external-pause-fence-1')"
                ).fetchone()
            finally:
                connection.close()
            self.assertEqual(adjusted, ("ADJUSTED", 1, 0))
            self.assertEqual(event_kind, "LATE_RECEIPT_RECORDED")
            self.assertEqual(retained, (1, 1))

    def test_t14_coordinator_exposes_resume_route(self) -> None:
        self.assertTrue(
            hasattr(SyntheticDispatchCoordinator, "resume"),
            "T14 requires a coordinator-owned resume route",
        )

    def test_t06_receipt_and_pause_race_serializes_without_reopening_dispatch(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            authority = SyntheticAuthority()
            effect_grant = SyntheticGrant(
                "race-grant", "repo-1", "race-effect", "race-attempt",
                "scope-1",
            )
            authority.register(effect_grant)
            effect_capability = authority.claim(*effect_grant.__dict__.values())
            with patch.dict(os.environ, self.state_environment(root)):
                store = SQLiteStateStore.open_canonical(
                    "repo-1", AlwaysFreshOracle()
                )
                adapter = SyntheticExecutionAdapter.open_canonical("repo-1")
            coordinator = SyntheticDispatchCoordinator(
                store, TransitionEngine(), authority, adapter
            )
            intent = IntentRequest(
                "repo-1", "race-run", "race-item", "race-command",
                "race-event", "race-effect", "race-payload", "race-attempt",
                "race-permission", "race-reservation", "race-budget", 1, 3, 5,
            )
            plan = self._accept_operation_plan(store, intent)
            dispatched = coordinator.dispatch(
                intent,
                effect_capability,
                SyntheticEffectRequest(
                    "repo-1", "race-effect", "race-attempt", "scope-1",
                    "race-payload",
                ),
                expected_head=plan.event_hash,
                writer_epoch=2,
                usage_units=2,
                lose_receipt=True,
            )
            connection = sqlite3.connect(store._database_path)
            connection.row_factory = sqlite3.Row
            try:
                launch = connection.execute(
                    "SELECT * FROM operation_launches WHERE run_id = 'race-run'"
                ).fetchone()
                contact = connection.execute(
                    "SELECT * FROM adapter_contacts WHERE run_id = 'race-run'"
                ).fetchone()
            finally:
                connection.close()
            pause_grant = SyntheticOperatorGrant(
                "race-pause-grant", "repo-1", "race-run", "PAUSE",
                "race-pause-scope",
            )
            authority.register_operator(pause_grant)
            pause_request = PauseExternalMutationRequest(
                "race-pause", "race-pause-command", "race-pause-event",
                "race-pause-fence", "repo-1", "race-run", "race-item",
                "race-effect", "race-attempt", dispatched.intent.event_id,
                dispatched.intent.event_hash, launch["launch_id"],
                launch["event_id"], launch["event_hash"], contact["contact_id"],
                contact["event_id"], contact["event_hash"],
                contact["target_digest"], 1, "OPERATOR_PAUSE_EXTERNAL_MUTATION",
            )
            observation = EffectObservationCommand(
                "race-observation", "race-observation-command",
                "race-observation-event", "repo-1", "race-run", "race-item",
                "race-effect", "race-attempt", effect_capability.claim_id,
                "race-observation-settlement", "",
            )
            barrier = threading.Barrier(2)

            def pause():
                barrier.wait()
                return coordinator.pause_external_mutation(
                    pause_request,
                    authority.claim_operator(*pause_grant.__dict__.values()),
                )

            def observe():
                barrier.wait()
                return coordinator.intake_effect_receipt(observation)

            results = []
            errors = []
            with ThreadPoolExecutor(max_workers=2) as executor:
                futures = (executor.submit(pause), executor.submit(observe))
                for future in futures:
                    try:
                        results.append(future.result())
                    except BaseException as error:
                        errors.append(error)
            connection = sqlite3.connect(store._database_path)
            try:
                state = connection.execute(
                    "SELECT lifecycle_state FROM runs WHERE run_id = 'race-run'"
                ).fetchone()[0]
                counts = connection.execute(
                    "SELECT (SELECT COUNT(*) FROM external_pause_actions), "
                    "(SELECT COUNT(*) FROM effect_observations), "
                    "(SELECT COUNT(*) FROM outstanding_slot)"
                ).fetchone()
                accounting = connection.execute(
                    "SELECT disposition, charged_units, uncertainty FROM "
                    "budget_reservations WHERE reservation_id = 'race-reservation'"
                ).fetchone()
            finally:
                connection.close()
            if counts[:2] == (1, 0):
                results.append(coordinator.intake_effect_receipt(observation))
                errors.clear()
            elif counts[:2] == (0, 1):
                with self.assertRaises(DispatchDenied):
                    coordinator.pause_external_mutation(
                        pause_request,
                        authority.claim_operator(*pause_grant.__dict__.values()),
                    )
                errors.clear()
            connection = sqlite3.connect(store._database_path)
            try:
                state = connection.execute(
                    "SELECT lifecycle_state FROM runs WHERE run_id = 'race-run'"
                ).fetchone()[0]
                counts = connection.execute(
                    "SELECT (SELECT COUNT(*) FROM external_pause_actions), "
                    "(SELECT COUNT(*) FROM effect_observations), "
                    "(SELECT COUNT(*) FROM outstanding_slot)"
                ).fetchone()
                accounting = connection.execute(
                    "SELECT disposition, charged_units, uncertainty FROM "
                    "budget_reservations WHERE reservation_id = 'race-reservation'"
                ).fetchone()
            finally:
                connection.close()
            self.assertEqual(counts[1:], (1, 1), repr(errors))
            self.assertNotEqual(state, LifecycleState.PAUSING.value)
            if counts[0] == 1:
                self.assertEqual(state, LifecycleState.RECONCILIATION_REQUIRED.value)
                self.assertEqual(accounting, ("ADJUSTED", 2, 0))
                self.assertEqual(len(errors), 0)
                self.assertEqual(len(results), 2)
            else:
                self.assertEqual(state, LifecycleState.VALIDATING.value)
                self.assertEqual(accounting, ("CONSUMED", 2, 0))
                self.assertEqual(len(errors), 0)

    @staticmethod
    def state_environment(root: Path) -> dict[str, str]:
        if sys.platform == "win32":
            return {"LOCALAPPDATA": str(root)}
        return {"XDG_STATE_HOME": str(root)}

    @staticmethod
    def _accept_operation_plan(
        store: SQLiteStateStore,
        request: IntentRequest,
        *,
        expected_head: str = "",
        writer_epoch: int = 1,
    ):
        return store.accept_plan(
            PlanAcceptanceRequest(
                f"plan:{request.run_id}",
                f"plan:{request.command_id}",
                f"plan:{request.event_id}",
                request.repository_id,
                request.run_id,
                request.item_id,
                request.logical_effect_id,
                "revision-1",
                request.effect_descriptor_digest,
                "scope-1",
                request.budget_policy_digest,
                ("check-1",),
            ),
            expected_head=expected_head,
            writer_epoch=writer_epoch,
        )

    def _prepare_t25_effect(self, root: Path):
        authority = SyntheticAuthority()
        grant = SyntheticGrant(
            "grant-1", "repo-1", "effect-1", "attempt-1", "scope-1"
        )
        authority.register(grant)
        capability = authority.claim(*grant.__dict__.values())
        with patch.dict(os.environ, self.state_environment(root)):
            store = SQLiteStateStore.open_canonical(
                "repo-1", AlwaysFreshOracle()
            )
            adapter = SyntheticExecutionAdapter.open_canonical("repo-1")
        store._bind_classification_authority(authority)
        intent = IntentRequest(
            "repo-1", "run-1", "item-1", "command-1", "event-1",
            "effect-1", "payload-1", "attempt-1", "permission-1",
            "reservation-1", "budget-1", 1, 1, 2,
        )
        effect = SyntheticEffectRequest(
            "repo-1", "effect-1", "attempt-1", "scope-1", "payload-1"
        )
        plan = self._accept_operation_plan(store, intent)
        committed = store.commit_intent(
            intent, capability, authority,
            expected_head=plan.event_hash, writer_epoch=2,
        )
        launch = store.claim_operation_launch(intent, committed)
        attestation = authority.issue_nonexecution_attestation(
            "nonexecution-attestation-1", "nonexecution-seal-1",
            "EFFECT", adapter._target_digest("repo-1"),
            capability.claim_id, f"EFFECT:{launch.launch_id}",
            launch.event_hash, "reservation-1", "repo-1", "run-1",
            "item-1", "effect-1", "attempt-1",
        )
        return (
            authority, capability, store, adapter, intent, effect,
            committed, launch, attestation,
        )

    def test_coordinator_mediates_graceful_stop(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            authority = SyntheticAuthority()
            with patch.dict(os.environ, self.state_environment(root)):
                store = SQLiteStateStore.open_canonical(
                    "repo-1", AlwaysFreshOracle()
                )
                adapter = SyntheticExecutionAdapter.open_canonical("repo-1")
            coordinator = SyntheticDispatchCoordinator(
                store, TransitionEngine(), authority, adapter
            )
            plan = store.accept_plan(
                PlanAcceptanceRequest(
                    "plan-1", "plan-command-1", "plan-event-1", "repo-1",
                    "run-1", "item-1", "effect-1", "revision-1",
                    "descriptor-1", "scope-1", "budget-1", ("check-1",),
                ),
                expected_head="", writer_epoch=1,
            )
            grant = SyntheticOperatorGrant(
                "stop-grant-1", "repo-1", "run-1", "STOP_GRACEFUL",
                "stop-scope-1",
            )
            authority.register_operator(grant)
            capability = authority.claim_operator(*grant.__dict__.values())
            receipt = coordinator.stop(
                StopRequest(
                    "stop-1", "stop-command-1", "stop-event-1", "repo-1",
                    "run-1", StopMode.GRACEFUL, "OPERATOR_STOP",
                    "2030-01-01T00:00:00Z",
                ),
                capability,
            )

            self.assertEqual(receipt.resulting_state, LifecycleState.STOPPED)
            self.assertNotEqual(receipt.event_hash, plan.event_hash)
            store.load_verified("repo-1")

    def test_coordinator_mediates_t15_without_adapter_contact(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            authority = SyntheticAuthority()
            with patch.dict(os.environ, self.state_environment(root)):
                store = SQLiteStateStore.open_canonical(
                    "repo-1", AlwaysFreshOracle()
                )
                adapter = SyntheticExecutionAdapter.open_canonical("repo-1")
            coordinator = SyntheticDispatchCoordinator(
                store, TransitionEngine(), authority, adapter
            )
            plan = store.accept_plan(
                PlanAcceptanceRequest(
                    "plan-1", "plan-command-1", "plan-event-1", "repo-1",
                    "run-1", "item-1", "effect-1", "revision-1",
                    "descriptor-1", "scope-1", "budget-1", ("check-1",),
                ),
                expected_head="", writer_epoch=1,
            )
            request = BindingMismatchRequest(
                "mismatch-1", "observation-1", "mismatch-command-1",
                "mismatch-event-1", "repo-1", "run-1", "item-1", "effect-1",
                BindingMismatchKind.POLICY,
                store._complete_policy_digest(
                    PlanAcceptanceRequest(
                        "plan-1", "plan-command-1", "plan-event-1", "repo-1",
                        "run-1", "item-1", "effect-1", "revision-1",
                        "descriptor-1", "scope-1", "budget-1", ("check-1",),
                    ),
                    authority,
                ),
                "changed-policy", plan.event_hash, "BINDING_MISMATCH_POLICY",
            )
            with patch.object(
                adapter, "_execute_committed",
                side_effect=AssertionError("T15 contacted the adapter"),
            ) as contact:
                receipt = coordinator.record_binding_mismatch(
                    request, authority.issue_binding_observation(request),
                    expected_head=plan.event_hash, writer_epoch=2,
                )
            self.assertEqual(receipt.resulting_state, LifecycleState.BLOCKED)
            contact.assert_not_called()

    def test_coordinator_exposes_t20_stop_escalation(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            authority = SyntheticAuthority()
            with patch.dict(os.environ, self.state_environment(root)):
                store = SQLiteStateStore.open_canonical(
                    "repo-1", AlwaysFreshOracle()
                )
                adapter = SyntheticExecutionAdapter.open_canonical("repo-1")
            coordinator = SyntheticDispatchCoordinator(
                store, TransitionEngine(), authority, adapter
            )
            effect_grant = SyntheticGrant(
                "grant-1", "repo-1", "effect-1", "attempt-1", "scope-1"
            )
            authority.register(effect_grant)
            effect_capability = authority.claim(*effect_grant.__dict__.values())
            intent = IntentRequest(
                "repo-1", "run-1", "item-1", "command-1", "event-1",
                "effect-1", "descriptor-1", "attempt-1", "permission-1",
                "reservation-1", "budget-1", 1, 2, 5,
            )
            plan = self._accept_operation_plan(store, intent)
            committed = store.commit_intent(
                intent, effect_capability, authority,
                expected_head=plan.event_hash, writer_epoch=2,
            )
            store.claim_operation_launch(intent, committed)
            stop_grant = SyntheticOperatorGrant(
                "stop-grant-1", "repo-1", "run-1", "STOP_GRACEFUL",
                "stop-scope-1",
            )
            authority.register_operator(stop_grant)
            graceful = StopRequest(
                "stop-1", "stop-command-1", "stop-event-1", "repo-1",
                "run-1", StopMode.GRACEFUL, "OPERATOR_STOP",
                "2000-01-01T00:00:00Z",
            )
            coordinator.stop(
                graceful,
                authority.claim_operator(*stop_grant.__dict__.values()),
            )
            escalation_grant = SyntheticOperatorGrant(
                "escalation-grant-1", "repo-1", "run-1", "STOP_ESCALATE",
                "escalation-scope-1",
            )
            authority.register_operator(escalation_grant)
            escalated = coordinator.escalate_stop(
                StopEscalationRequest(
                    "escalation-1", "escalation-command-1",
                    "escalation-event-1", "repo-1", "run-1", "stop-1",
                    "stop-event-1", "2000-01-01T00:00:00Z",
                    "GRACEFUL_DEADLINE_EXPIRED",
                    (StopEscalationSettlement(
                        "reservation-1", "escalation-settlement-1", ""
                    ),),
                ),
                authority.claim_operator(*escalation_grant.__dict__.values()),
            )
            self.assertEqual(escalated.resulting_state, LifecycleState.STOPPED)
            store.load_verified("repo-1")

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
                store = SQLiteStateStore.open_canonical(
                    "repo-1", AlwaysFreshOracle()
                )
                first = SyntheticDispatchCoordinator(
                    store,
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

            plan = self._accept_operation_plan(store, request)

            first.dispatch(
                request,
                first_capability,
                effect,
                expected_head=plan.event_hash,
                writer_epoch=2,
            )

            with self.assertRaisesRegex(DispatchDenied, "already redeemed"):
                second.dispatch(
                    request,
                    second_capability,
                    effect,
                    expected_head=plan.event_hash,
                    writer_epoch=3,
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
                with self.assertRaisesRegex(
                    DispatchDenied, "canonical repository root"
                ):
                    SyntheticFinalizationCoordinator(
                        alternate_store, TransitionEngine(), authority
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

            intent = IntentRequest(
                "repo-1", "run-1", "item-1", "command-1", "event-1",
                "effect-1", "payload-1", "attempt-1", "permission-1",
                "reservation-1", "budget-1", 1, 1, 2,
            )
            plan = self._accept_operation_plan(store, intent)

            with self.assertRaisesRegex(DispatchDenied, "not issued"):
                coordinator.dispatch(
                    intent,
                    capability,
                    SyntheticEffectRequest(
                        "repo-1", "effect-1", "attempt-1", "scope-1", "payload-1"
                    ),
                    expected_head=plan.event_hash,
                    writer_epoch=2,
                )

            counts = store.table_counts()
            for table in (
                "effects", "permission_uses", "capability_redemptions",
                "budget_reservations", "outstanding_slot",
            ):
                self.assertEqual(counts[table], 0)
            with patch.dict(os.environ, self.state_environment(root)):
                self.assertIsNone(
                    SyntheticExecutionAdapter.open_canonical(
                        "repo-1"
                    ).reconcile(capability.claim_id)
                )

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
            plan = self._accept_operation_plan(store, intent)

            with patch.object(
                adapter,
                "_execute_committed",
                side_effect=InjectedFailure("before_adapter_contact"),
            ), self.assertRaises(InjectedFailure):
                coordinator.dispatch(
                    intent,
                    capability,
                    effect,
                    expected_head=plan.event_hash,
                    writer_epoch=2,
                )

            self.assertIsNone(
                SyntheticExecutionAdapter.open_canonical("repo-1").reconcile(
                    capability.claim_id
                )
            )
            self.assertEqual(store.table_counts()["operation_launches"], 1)
            release = BudgetSettlementRequest(
                "release-after-launch", "reservation-1", "",
                BudgetDisposition.RELEASED, None, "nondispatch-proof",
                "NONDISPATCH_PROVEN", non_dispatch_proven=True,
                zero_liability_proven=True, release_slot=True,
                all_obligations_settled=True,
            )
            connection = sqlite3.connect(store._database_path)
            try:
                before_release = tuple(connection.iterdump())
            finally:
                connection.close()
            with self.assertRaisesRegex(
                DispatchDenied, "canonical nonexecution seal"
            ):
                store._settle_budget(
                    release,
                    authority.issue_settlement_proof(
                        "release-after-launch-proof", release
                    ),
                    authority,
                )
            connection = sqlite3.connect(store._database_path)
            try:
                after_release = tuple(connection.iterdump())
            finally:
                connection.close()
            self.assertEqual(after_release, before_release)
            store.load_verified("repo-1")
            with self.assertRaisesRegex(DispatchDenied, "already redeemed"):
                coordinator.dispatch(
                    intent,
                    capability,
                    effect,
                    expected_head=plan.event_hash,
                    writer_epoch=3,
                )

    def test_t25_effect_seal_blocks_execution_and_releases_launch(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            authority = SyntheticAuthority()
            grant = SyntheticGrant(
                "grant-1", "repo-1", "effect-1", "attempt-1", "scope-1"
            )
            authority.register(grant)
            capability = authority.claim(*grant.__dict__.values())
            with patch.dict(os.environ, self.state_environment(root)):
                store = SQLiteStateStore.open_canonical(
                    "repo-1", AlwaysFreshOracle()
                )
                adapter = SyntheticExecutionAdapter.open_canonical("repo-1")
            store._bind_classification_authority(authority)
            intent = IntentRequest(
                "repo-1", "run-1", "item-1", "command-1", "event-1",
                "effect-1", "payload-1", "attempt-1", "permission-1",
                "reservation-1", "budget-1", 1, 1, 2,
            )
            effect = SyntheticEffectRequest(
                "repo-1", "effect-1", "attempt-1", "scope-1", "payload-1"
            )
            plan = self._accept_operation_plan(store, intent)
            committed = store.commit_intent(
                intent, capability, authority,
                expected_head=plan.event_hash, writer_epoch=2,
            )
            launch = store.claim_operation_launch(intent, committed)
            attestation = authority.issue_nonexecution_attestation(
                "nonexecution-attestation-1", "nonexecution-seal-1",
                "EFFECT", adapter._target_digest("repo-1"),
                capability.claim_id, f"EFFECT:{launch.launch_id}",
                launch.event_hash, "reservation-1", "repo-1", "run-1",
                "item-1", "effect-1", "attempt-1",
            )
            sealed = adapter.seal_nonexecution(attestation, authority)
            replay = adapter.seal_nonexecution(attestation, authority)
            self.assertFalse(sealed.replayed)
            self.assertTrue(replay.replayed)
            with patch.dict(os.environ, self.state_environment(root)):
                store = SQLiteStateStore.open_canonical(
                    "repo-1", AlwaysFreshOracle()
                )
                adapter = SyntheticExecutionAdapter.open_canonical("repo-1")
            with self.assertRaisesRegex(DispatchDenied, "sealed as nonexecuted"):
                adapter._execute_committed(
                    capability, effect, authority, store, committed, launch,
                    intent, usage_units=1,
                )
            connection = sqlite3.connect(store._database_path)
            try:
                contact_hash = connection.execute(
                    "SELECT event_hash FROM adapter_contacts WHERE "
                    "contact_kind = 'EFFECT'"
                ).fetchone()[0]
            finally:
                connection.close()
            release = BudgetSettlementRequest(
                "release-after-seal", "reservation-1", "",
                BudgetDisposition.RELEASED, None, "nonexecution-seal-evidence",
                "NONDISPATCH_PROVEN", non_dispatch_proven=True,
                zero_liability_proven=True, release_slot=True,
                all_obligations_settled=True,
                nonexecution_seal_id=sealed.seal_id,
            )
            settled = store._settle_budget(
                release,
                authority.issue_settlement_proof(
                    "release-after-seal-proof", release
                ),
                authority,
            )
            self.assertTrue(settled.slot_released)
            replayed_settlement = store._settle_budget(
                release,
                authority.issue_settlement_proof(
                    "release-after-seal-replay-proof", release
                ),
                authority,
            )
            self.assertTrue(replayed_settlement.replayed)
            self.assertTrue(replayed_settlement.slot_released)
            self.assertEqual(store.table_counts()["outstanding_slot"], 0)
            catalog_head, run_heads = store.load_verified("repo-1")
            expected_vector = root / "expected-vector.json"
            expected_vector.write_text(
                json.dumps(
                    {
                        "repository_id": "repo-1",
                        "catalog_head": catalog_head,
                        "run_heads": run_heads,
                    }
                ),
                encoding="utf-8",
            )
            authority_key = root / "authority-key.json"
            authority_key.write_text(
                json.dumps(
                    {
                        "synthetic_issuer_key_hex": authority._issuer_key.hex()
                    }
                ),
                encoding="utf-8",
            )
            environment = os.environ.copy()
            environment.update(self.state_environment(root))
            verified = subprocess.run(
                [
                    sys.executable, "-m", "tools.aegis_delivery_control",
                    "--repository-id", "repo-1", "verify",
                    "--expected-vector", str(expected_vector),
                    "--authority-key-file", str(authority_key),
                ],
                cwd=Path(__file__).parents[3],
                env=environment,
                capture_output=True,
                text=True,
                check=False,
                timeout=5,
            )
            self.assertEqual(verified.returncode, 0, verified.stderr)
            self.assertTrue(json.loads(verified.stdout)["verified"])

    def test_t25_seal_rejects_forgery_target_confusion_rebinding_and_tamper(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            (
                authority, capability, store, adapter, _intent, _effect,
                _committed, launch, attestation,
            ) = self._prepare_t25_effect(root)
            with self.assertRaisesRegex(DispatchDenied, "not issued here"):
                adapter.seal_nonexecution(
                    replace(attestation, source_event_hash="forged"), authority
                )
            with patch.dict(os.environ, self.state_environment(root)):
                validator_adapter = SyntheticValidatorAdapter.open_canonical(
                    "repo-1"
                )
            cross_target = authority.issue_nonexecution_attestation(
                "cross-target-attestation", "cross-target-seal", "VALIDATOR",
                validator_adapter._target_digest("repo-1"), capability.claim_id,
                f"EFFECT:{launch.launch_id}", launch.event_hash,
                "reservation-1", "repo-1", "run-1", "item-1", "effect-1",
                "attempt-1",
            )
            with self.assertRaisesRegex(DispatchDenied, "does not bind this target"):
                adapter.seal_nonexecution(cross_target, authority)
            sealed = adapter.seal_nonexecution(attestation, authority)
            rebound = authority.issue_nonexecution_attestation(
                "rebound-attestation", sealed.seal_id, "EFFECT",
                adapter._target_digest("repo-1"), capability.claim_id,
                f"EFFECT:{launch.launch_id}", "rebound-event-hash",
                "reservation-1", "repo-1", "run-1", "item-1", "effect-1",
                "attempt-1",
            )
            with self.assertRaisesRegex(DispatchDenied, "identity was rebound"):
                adapter.seal_nonexecution(rebound, authority)
            connection = sqlite3.connect(adapter._ledger_path)
            try:
                connection.execute(
                    "UPDATE synthetic_nonexecution_seals SET source_event_hash = ? "
                    "WHERE seal_id = ?",
                    ("tampered-event-hash", sealed.seal_id),
                )
                connection.commit()
            finally:
                connection.close()
            release = BudgetSettlementRequest(
                "release-after-tamper", "reservation-1", "",
                BudgetDisposition.CONSUMED, 1, "tampered-seal-evidence",
                "NONDISPATCH_PROVEN", non_dispatch_proven=True,
                all_obligations_settled=True,
                nonexecution_seal_id=sealed.seal_id,
            )
            with self.assertRaisesRegex(DispatchDenied, "does not bind"):
                store._settle_budget(
                    release,
                    authority.issue_settlement_proof(
                        "release-after-tamper-proof", release
                    ),
                    authority,
                )

    def test_t25_execution_prevents_later_nonexecution_seal(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            (
                authority, capability, store, adapter, intent, effect,
                committed, launch, attestation,
            ) = self._prepare_t25_effect(Path(temporary_directory))
            receipt = adapter._execute_committed(
                capability, effect, authority, store, committed, launch,
                intent, usage_units=1,
            )
            self.assertIsNotNone(receipt)
            with self.assertRaisesRegex(DispatchDenied, "contradicts target execution"):
                adapter.seal_nonexecution(attestation, authority)

    def test_t25_execution_and_nonexecution_seal_have_one_winner(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            (
                authority, capability, store, adapter, intent, effect,
                committed, launch, attestation,
            ) = self._prepare_t25_effect(Path(temporary_directory))
            barrier = threading.Barrier(2)

            def execute():
                barrier.wait()
                try:
                    adapter._execute_committed(
                        capability, effect, authority, store, committed, launch,
                        intent, usage_units=1,
                    )
                except DispatchDenied:
                    return "denied"
                return "executed"

            def seal():
                barrier.wait()
                try:
                    adapter.seal_nonexecution(attestation, authority)
                except DispatchDenied:
                    return "denied"
                return "sealed"

            with ThreadPoolExecutor(max_workers=2) as executor:
                execute_future = executor.submit(execute)
                seal_future = executor.submit(seal)
                results = {execute_future.result(), seal_future.result()}
            self.assertIn(results, ({"executed", "denied"}, {"sealed", "denied"}))
            connection = sqlite3.connect(adapter._ledger_path)
            try:
                executions = connection.execute(
                    "SELECT COUNT(*) FROM synthetic_effects"
                ).fetchone()[0]
                seals = connection.execute(
                    "SELECT COUNT(*) FROM synthetic_nonexecution_seals"
                ).fetchone()[0]
            finally:
                connection.close()
            self.assertEqual(executions + seals, 1)

    def test_t25_contradictory_target_facts_are_retained_and_fenced(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            (
                authority, capability, store, adapter, intent, _effect,
                _committed, _launch, attestation,
            ) = self._prepare_t25_effect(Path(temporary_directory))
            sealed = adapter.seal_nonexecution(attestation, authority)
            connection = sqlite3.connect(adapter._ledger_path)
            try:
                connection.execute(
                    "INSERT INTO synthetic_effects VALUES "
                    "(?, ?, ?, ?, ?, ?, ?, ?, ?, 1)",
                    (
                        capability.claim_id, "contradictory-receipt", "repo-1",
                        "run-1", "item-1", "effect-1", "attempt-1",
                        intent.effect_descriptor_digest, 1,
                    ),
                )
                connection.commit()
            finally:
                connection.close()
            contradiction = BudgetSettlementRequest(
                "contradictory-nonexecution", "reservation-1", "",
                BudgetDisposition.UNKNOWN_WORST_CASE_CHARGED, None,
                "contradictory-nonexecution-evidence", "NONDISPATCH_PROVEN",
                non_dispatch_proven=True,
                nonexecution_seal_id=sealed.seal_id,
            )
            settled = store._settle_budget(
                contradiction,
                authority.issue_settlement_proof(
                    "contradictory-nonexecution-proof", contradiction
                ),
                authority,
            )
            self.assertTrue(settled.uncertainty)
            self.assertFalse(settled.slot_released)
            self.assertEqual(
                store.load_run_lifecycle("run-1"),
                LifecycleState.RECONCILIATION_REQUIRED,
            )
            connection = sqlite3.connect(store._database_path)
            try:
                fence = connection.execute(
                    "SELECT item_id, logical_effect_id, reason_code FROM "
                    "dispatch_fences WHERE fence_id = ?",
                    ("nonexecution-contradiction:contradictory-nonexecution",),
                ).fetchone()
            finally:
                connection.close()
            self.assertEqual(
                fence, ("item-1", "effect-1", "NONEXECUTION_CONTRADICTION")
            )
            release = replace(
                contradiction,
                settlement_event_id="contradictory-release",
                expected_previous_hash=settled.settlement_hash,
                disposition=BudgetDisposition.RELEASED,
                zero_liability_proven=True,
                release_slot=True,
                all_obligations_settled=True,
            )
            with self.assertRaisesRegex(
                DispatchDenied, "cannot release liability"
            ):
                store._settle_budget(
                    release,
                    authority.issue_settlement_proof(
                        "contradictory-release-proof", release
                    ),
                    authority,
                )

    def test_t27_process_crash_after_intent_before_contact_denies_redispatch(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            issuer_key = b"validator-process-test-key-32-bytes"
            authority = SyntheticAuthority(issuer_key)
            operation_grant = SyntheticGrant(
                "grant-1", "repo-1", "effect-1", "attempt-1", "scope-1"
            )
            authority.register(operation_grant)
            operation_capability = authority.claim(
                *operation_grant.__dict__.values()
            )
            with patch.dict(os.environ, self.state_environment(root)):
                store = SQLiteStateStore.open_canonical(
                    "repo-1", AlwaysFreshOracle()
                )
                dispatch = SyntheticDispatchCoordinator(
                    store,
                    TransitionEngine(),
                    authority,
                    SyntheticExecutionAdapter.open_canonical("repo-1"),
                )
            intent = IntentRequest(
                "repo-1", "run-1", "item-1", "command-1", "event-1",
                "effect-1", "payload-1", "attempt-1", "permission-1",
                "reservation-1", "budget-1", 1, 1, 10,
            )
            plan = self._accept_operation_plan(store, intent)
            dispatch.dispatch(
                intent,
                operation_capability,
                SyntheticEffectRequest(
                    "repo-1", "effect-1", "attempt-1", "scope-1", "payload-1"
                ),
                expected_head=plan.event_hash,
                writer_epoch=2,
                usage_units=1,
            )
            observation = dispatch.intake_effect_receipt(
                EffectObservationCommand(
                    "observation-1", "observe-command-1", "observation-event-1",
                    "repo-1", "run-1", "item-1", "effect-1", "attempt-1",
                    operation_capability.claim_id, "settlement-1", "",
                )
            )
            validator_grant = SyntheticValidatorGrant(
                "validator-grant-1", "repo-1", "effect-1", "revision-1",
                "check-1", "input-1", "validator-attempt-1", "read-only-1",
            )
            validator_intent = ValidatorIntentRequest(
                "validator-intent-1", "validator-command-1", "validator-event-1",
                "repo-1", "run-1", "item-1", "effect-1", "attempt-1",
                "observation-1", observation.event_hash, "revision-1",
                "check-1", "input-1", "validator-attempt-1",
                "validator-permission-1", "validator-reservation-1",
                "validator-budget-1", 1, 1, 10,
            )
            validator_request = SyntheticValidatorRequest(
                "repo-1", "effect-1", "revision-1", "check-1", "input-1",
                "validator-attempt-1", "read-only-1", "result-digest-1", "PASS",
            )
            context = multiprocessing.get_context("spawn")
            ready = context.Event()
            errors = context.Queue()
            process = context.Process(
                target=_launch_validator_until_terminated,
                args=(
                    root,
                    issuer_key,
                    validator_grant,
                    validator_intent,
                    validator_request,
                    ready,
                    errors,
                ),
            )
            process.start()
            try:
                reached_contact = ready.wait(10)
                child_error = None if errors.empty() else errors.get()
                self.assertTrue(
                    reached_contact,
                    f"validator child failed before contact: {child_error}",
                )
            finally:
                process.terminate()
                process.join(10)
                if process.is_alive():
                    process.kill()
                    process.join(10)
            self.assertFalse(process.is_alive())

            authority.register_validator(validator_grant)
            validator_capability = authority.claim_validator(
                *validator_grant.__dict__.values()
            )
            with patch.dict(os.environ, self.state_environment(root)):
                reopened = SQLiteStateStore.open_canonical(
                    "repo-1", AlwaysFreshOracle()
                )
                validator_adapter = SyntheticValidatorAdapter.open_canonical(
                    "repo-1"
                )
                validation = SyntheticValidationCoordinator(
                    reopened, TransitionEngine(), authority, validator_adapter
                )
            connection = sqlite3.connect(reopened._database_path)
            try:
                active_intents = connection.execute(
                    "SELECT COUNT(*) FROM validator_intents WHERE status = 'ACTIVE'"
                ).fetchone()[0]
                validator_contacts = connection.execute(
                    "SELECT COUNT(*) FROM adapter_contacts "
                    "WHERE contact_kind = 'VALIDATOR'"
                ).fetchone()[0]
            finally:
                connection.close()
            self.assertEqual(active_intents, 1)
            self.assertEqual(validator_contacts, 0)
            self.assertIsNone(
                validator_adapter.reconcile(validator_capability.claim_id)
            )
            self.assertEqual(
                reopened.load_run_lifecycle("run-1"), LifecycleState.VALIDATING
            )
            self.assertEqual(reopened.table_counts()["outstanding_slot"], 1)
            with self.assertRaisesRegex(DispatchDenied, "already redeemed"):
                validation.launch(
                    validator_intent,
                    validator_capability,
                    validator_request,
                    usage_units=1,
                )
            self.assertIsNone(
                validator_adapter.reconcile(validator_capability.claim_id)
            )

    def test_t25_validator_seal_blocks_result_and_settles_subintent(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            authority = SyntheticAuthority()
            operation_grant = SyntheticGrant(
                "grant-1", "repo-1", "effect-1", "attempt-1", "scope-1"
            )
            authority.register(operation_grant)
            operation_capability = authority.claim(
                *operation_grant.__dict__.values()
            )
            with patch.dict(os.environ, self.state_environment(root)):
                store = SQLiteStateStore.open_canonical(
                    "repo-1", AlwaysFreshOracle()
                )
                effect_adapter = SyntheticExecutionAdapter.open_canonical(
                    "repo-1"
                )
                validator_adapter = SyntheticValidatorAdapter.open_canonical(
                    "repo-1"
                )
            dispatch = SyntheticDispatchCoordinator(
                store, TransitionEngine(), authority, effect_adapter
            )
            intent = IntentRequest(
                "repo-1", "run-1", "item-1", "command-1", "event-1",
                "effect-1", "payload-1", "attempt-1", "permission-1",
                "reservation-1", "budget-1", 1, 1, 10,
            )
            plan = self._accept_operation_plan(store, intent)
            dispatch.dispatch(
                intent, operation_capability,
                SyntheticEffectRequest(
                    "repo-1", "effect-1", "attempt-1", "scope-1", "payload-1"
                ),
                expected_head=plan.event_hash, writer_epoch=2, usage_units=1,
            )
            observation = dispatch.intake_effect_receipt(
                EffectObservationCommand(
                    "observation-1", "observe-command-1", "observation-event-1",
                    "repo-1", "run-1", "item-1", "effect-1", "attempt-1",
                    operation_capability.claim_id, "settlement-1", "",
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
                "observation-1", observation.event_hash, "revision-1",
                "check-1", "input-1", "validator-attempt-1",
                "validator-permission-1", "validator-reservation-1",
                "validator-budget-1", 1, 1, 10,
            )
            committed = store.commit_validator_intent(
                validator_intent, validator_capability, authority
            )
            attestation = authority.issue_nonexecution_attestation(
                "validator-nonexecution-attestation-1",
                "validator-nonexecution-seal-1", "VALIDATOR",
                validator_adapter._target_digest("repo-1"),
                validator_capability.claim_id,
                "VALIDATOR:validator-intent-1", committed.event_hash,
                "validator-reservation-1", "repo-1", "run-1", "item-1",
                "effect-1", "validator-attempt-1",
            )
            sealed = validator_adapter.seal_nonexecution(
                attestation, authority
            )
            with self.assertRaisesRegex(DispatchDenied, "sealed as nonexecuted"):
                validator_adapter._execute_committed(
                    validator_capability,
                    SyntheticValidatorRequest(
                        "repo-1", "effect-1", "revision-1", "check-1",
                        "input-1", "validator-attempt-1", "read-only-1",
                        "result-digest-1", "PASS",
                    ),
                    authority, store, committed, validator_intent, usage_units=1,
                )
            uncertain = BudgetSettlementRequest(
                "validator-unknown-after-seal", "validator-reservation-1", "",
                BudgetDisposition.UNKNOWN_WORST_CASE_CHARGED, None,
                "validator-nonexecution-seal-evidence", "NONDISPATCH_PROVEN",
                non_dispatch_proven=True,
                attempt_id="validator-attempt-1",
                nonexecution_seal_id=sealed.seal_id,
            )
            invalid_parent_release = replace(
                uncertain,
                settlement_event_id="validator-parent-release",
                disposition=BudgetDisposition.RELEASED,
                zero_liability_proven=True,
                release_slot=True,
                all_obligations_settled=True,
            )
            with self.assertRaisesRegex(
                DispatchDenied, "cannot release the parent operation slot"
            ):
                store._settle_budget(
                    invalid_parent_release,
                    authority.issue_settlement_proof(
                        "validator-parent-release-proof", invalid_parent_release
                    ),
                    authority,
                )
            uncertain_settlement = store._settle_budget(
                uncertain,
                authority.issue_settlement_proof(
                    "validator-unknown-after-seal-proof", uncertain
                ),
                authority,
            )
            self.assertTrue(uncertain_settlement.uncertainty)
            self.assertEqual(
                store.load_run_lifecycle("run-1"),
                LifecycleState.RECONCILIATION_REQUIRED,
            )
            release = BudgetSettlementRequest(
                "validator-release-after-seal", "validator-reservation-1",
                uncertain_settlement.settlement_hash,
                BudgetDisposition.ADJUSTED, 1,
                "validator-nonexecution-accounting", "USAGE_REPORTED",
                non_dispatch_proven=True,
                all_obligations_settled=True,
                attempt_id="validator-attempt-1",
                nonexecution_seal_id=sealed.seal_id,
            )
            settled = store._settle_budget(
                release,
                authority.issue_settlement_proof(
                    "validator-release-after-seal-proof", release
                ),
                authority,
            )
            self.assertFalse(settled.slot_released)
            self.assertEqual(settled.charged_units, 1)
            self.assertEqual(
                store.load_run_lifecycle("run-1"), LifecycleState.BLOCKED
            )
            connection = sqlite3.connect(store._database_path)
            try:
                status = connection.execute(
                    "SELECT status FROM validator_intents WHERE "
                    "validator_intent_id = 'validator-intent-1'"
                ).fetchone()[0]
            finally:
                connection.close()
            self.assertEqual(status, "SETTLED")
            self.assertEqual(store.table_counts()["outstanding_slot"], 1)
            store.load_verified("repo-1")

    def test_effect_binding_denial_precedes_durable_intent(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            authority = SyntheticAuthority()
            grant = SyntheticGrant(
                "grant-1", "repo-1", "effect-1", "attempt-1", "scope-1"
            )
            authority.register(grant)
            capability = authority.claim(*grant.__dict__.values())
            with patch.dict(os.environ, self.state_environment(root)):
                store = SQLiteStateStore.open_canonical(
                    "repo-1", AlwaysFreshOracle()
                )
                adapter = SyntheticExecutionAdapter.open_canonical("repo-1")
                coordinator = SyntheticDispatchCoordinator(
                    store, TransitionEngine(), authority, adapter
                )
            intent = IntentRequest(
                "repo-1", "run-1", "item-1", "command-1", "event-1",
                "effect-1", "payload-1", "attempt-1", "permission-1",
                "reservation-1", "budget-1", 1, 1, 2,
            )
            plan = self._accept_operation_plan(store, intent)
            connection = sqlite3.connect(store._database_path)
            try:
                before_denial = tuple(connection.iterdump())
            finally:
                connection.close()

            with self.assertRaisesRegex(DispatchDenied, "operation intent"):
                coordinator.dispatch(
                    intent,
                    capability,
                    SyntheticEffectRequest(
                        "repo-1", "effect-1", "attempt-1", "scope-2",
                        "payload-1",
                    ),
                    expected_head=plan.event_hash,
                    writer_epoch=2,
                )
            with self.assertRaisesRegex(ValueError, "non-negative"):
                coordinator.dispatch(
                    intent,
                    capability,
                    SyntheticEffectRequest(
                        "repo-1", "effect-1", "attempt-1", "scope-1",
                        "payload-1",
                    ),
                    expected_head=plan.event_hash,
                    writer_epoch=2,
                    usage_units=-1,
                )
            with self.assertRaisesRegex(ValueError, "non-negative"):
                coordinator.dispatch(
                    intent,
                    capability,
                    SyntheticEffectRequest(
                        "repo-1", "effect-1", "attempt-1", "scope-1",
                        "payload-1",
                    ),
                    expected_head=plan.event_hash,
                    writer_epoch=2,
                    usage_units=0.5,
                )

            connection = sqlite3.connect(store._database_path)
            try:
                after_denial = tuple(connection.iterdump())
            finally:
                connection.close()
            self.assertEqual(after_denial, before_denial)
            self.assertIsNone(adapter.reconcile(capability.claim_id))

    def test_post_launch_fence_alone_denies_adapter_contact(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            authority = SyntheticAuthority()
            grant = SyntheticGrant(
                "grant-1", "repo-1", "effect-1", "attempt-1", "scope-1"
            )
            authority.register(grant)
            capability = authority.claim(*grant.__dict__.values())
            with patch.dict(os.environ, self.state_environment(root)):
                store = SQLiteStateStore.open_canonical(
                    "repo-1", AlwaysFreshOracle()
                )
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
            plan = self._accept_operation_plan(store, intent)
            execute_committed = adapter._execute_committed

            def invalidate_launch(*args, **kwargs):
                connection = sqlite3.connect(store._database_path)
                try:
                    connection.execute(
                        "INSERT INTO dispatch_fences VALUES (?, ?, ?, ?, ?, ?)",
                        (
                            "test-fence", "repo-1", None, None,
                            "TEST_ONLY_FENCE", "test-origin",
                        ),
                    )
                    connection.commit()
                finally:
                    connection.close()
                return execute_committed(*args, **kwargs)

            with patch.object(
                store, "_verify_projections", return_value=None
            ), patch.object(
                adapter,
                "_execute_committed",
                side_effect=invalidate_launch,
            ):
                with self.assertRaisesRegex(
                    DispatchDenied, "active dispatch fence"
                ):
                    coordinator.dispatch(
                        intent, capability, effect,
                        expected_head=plan.event_hash, writer_epoch=2,
                    )

            self.assertIsNone(adapter.reconcile(capability.claim_id))
            self.assertEqual(store.table_counts()["operation_launches"], 1)
            self.assertEqual(store.table_counts()["budget_settlements"], 0)
            self.assertEqual(store.table_counts()["dispatch_fences"], 1)
            connection = sqlite3.connect(store._database_path)
            try:
                reservation, fence = (
                    connection.execute(
                        "SELECT disposition, settlement_head_hash FROM "
                        "budget_reservations WHERE reservation_id = 'reservation-1'"
                    ).fetchone(),
                    connection.execute(
                        "SELECT fence_id, reason_code, originating_event_id FROM "
                        "dispatch_fences"
                    ).fetchone(),
                )
            finally:
                connection.close()
            self.assertEqual(reservation, ("RESERVED", ""))
            self.assertEqual(fence, ("test-fence", "TEST_ONLY_FENCE", "test-origin"))

    def test_fabricated_validator_handoff_cannot_contact_adapter(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            authority = SyntheticAuthority()
            grant = SyntheticValidatorGrant(
                "validator-grant-1", "repo-1", "effect-1", "revision-1",
                "check-1", "input-1", "validator-attempt-1",
                "validator-scope-1",
            )
            authority.register_validator(grant)
            capability = authority.claim_validator(*grant.__dict__.values())
            with patch.dict(os.environ, self.state_environment(root)):
                store = SQLiteStateStore.open_canonical(
                    "repo-1", AlwaysFreshOracle()
                )
                adapter = SyntheticValidatorAdapter.open_canonical("repo-1")
            store._bind_classification_authority(authority)
            self._accept_operation_plan(
                store,
                IntentRequest(
                    "repo-1", "run-1", "item-1", "operation-command-1",
                    "operation-event-1", "effect-1", "input-1", "attempt-1",
                    "operation-permission-1", "operation-reservation-1",
                    "operation-budget-1", 1, 1, 2,
                ),
            )
            intent = ValidatorIntentRequest(
                "validator-intent-1", "validator-command-1",
                "validator-event-1", "repo-1", "run-1", "item-1",
                "effect-1", "attempt-1", "observation-1",
                "observation-event-hash", "revision-1", "check-1",
                "input-1", "validator-attempt-1", "validator-permission-1",
                "validator-reservation-1", "validator-budget-1", 1, 1, 2,
            )
            request = SyntheticValidatorRequest(
                "repo-1", "effect-1", "revision-1", "check-1", "input-1",
                "validator-attempt-1", "validator-scope-1", "result-1",
                "PASS",
            )

            with self.assertRaisesRegex(DispatchDenied, "durable active intent"):
                adapter._execute_committed(
                    capability, request, authority, store,
                    CommitReceipt(
                        "validator-command-1", "validator-event-1", 1,
                        "fabricated-event-hash", False,
                    ),
                    intent,
                )

            self.assertIsNone(adapter.reconcile(capability.claim_id))

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
            plan = self._accept_operation_plan(store, intent)
            dispatched = coordinator.dispatch(
                intent,
                capability,
                SyntheticEffectRequest(
                    "repo-1", "effect-1", "attempt-1", "scope-1", "payload-1"
                ),
                expected_head=plan.event_hash,
                writer_epoch=2,
                usage_units=1,
                lose_receipt=True,
            )
            self.assertIsNone(dispatched.effect)
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
                "",
            )

            with self.assertRaises(InjectedFailure):
                coordinator.intake_effect_receipt(
                    command,
                    failure_hook=raise_at(
                        "after_observation_settlement_before_observation"
                    ),
                )
            self.assertEqual(store.table_counts()["budget_settlements"], 0)
            self.assertEqual(store.table_counts()["effect_observations"], 0)
            self.assertEqual(store.table_counts()["outstanding_slot"], 1)

            with self.assertRaises(InjectedFailure):
                coordinator.intake_effect_receipt(
                    command,
                    failure_hook=raise_at(
                        "after_observation_commit_before_acknowledgement"
                    ),
                )
            with patch.dict(os.environ, self.state_environment(root)):
                recovered_store = SQLiteStateStore.open_canonical(
                    "repo-1", AlwaysFreshOracle()
                )
            recovered_store.load_verified("repo-1")
            recovered_coordinator = SyntheticDispatchCoordinator(
                recovered_store, TransitionEngine(), authority, adapter
            )
            replay = recovered_coordinator.intake_effect_receipt(command)

            self.assertTrue(replay.replayed)
            self.assertEqual(recovered_store.table_counts()["events"], 6)
            self.assertEqual(
                recovered_store.table_counts()["budget_settlements"], 1
            )
            self.assertEqual(
                recovered_store.table_counts()["effect_observations"], 1
            )
            self.assertEqual(recovered_store.table_counts()["outstanding_slot"], 1)
            with self.assertRaisesRegex(DispatchDenied, "already redeemed"):
                coordinator.dispatch(
                    intent,
                    capability,
                    SyntheticEffectRequest(
                        "repo-1", "effect-1", "attempt-1", "scope-1", "payload-1"
                    ),
                    expected_head=replay.event_hash,
                    writer_epoch=2,
                )

    def test_c04_canonical_receipt_cannot_be_substituted_across_attempts(self) -> None:
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
            coordinator.dispatch(
                intent := IntentRequest(
                    "repo-1", "run-1", "item-1", "command-1", "event-1",
                    "effect-1", "payload-1", "attempt-1", "permission-1",
                    "reservation-1", "budget-1", 1, 1, 2,
                ),
                capability,
                SyntheticEffectRequest(
                    "repo-1", "effect-1", "attempt-1", "scope-1", "payload-1"
                ),
                expected_head=(
                    self._accept_operation_plan(store, intent).event_hash
                ),
                writer_epoch=2,
                usage_units=1,
                lose_receipt=True,
            )
            command = EffectObservationCommand(
                "observation-1", "observe-command-1", "observation-event-1",
                "repo-1", "run-1", "item-1", "effect-1", "attempt-1",
                capability.claim_id, "settlement-1", "",
            )
            substitutions = {
                "repository_id": "repo-2",
                "run_id": "run-2",
                "item_id": "item-2",
                "logical_effect_id": "effect-2",
                "attempt_id": "attempt-2",
            }
            for field, value in substitutions.items():
                with self.subTest(field=field), self.assertRaises(DispatchDenied):
                    coordinator.intake_effect_receipt(
                        replace(command, **{field: value})
                    )
            self.assertEqual(store.table_counts()["effect_observations"], 0)
            self.assertEqual(store.table_counts()["budget_settlements"], 0)

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
                finalization = SyntheticFinalizationCoordinator(
                    store, TransitionEngine(), authority
                )
            plan = store.accept_plan(
                PlanAcceptanceRequest(
                    "plan-1", "plan-command-1", "plan-event-1", "repo-1",
                    "run-1", "item-1", "effect-1", "revision-1",
                    "payload-1", "scope-1", "budget-1",
                    ("check-1",), ("aggregate-release",),
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
            operation_observation = dispatch.intake_effect_receipt(
                EffectObservationCommand(
                    "observation-1", "observe-command-1", "observation-event-1",
                    "repo-1", "run-1", "item-1", "effect-1", "attempt-1",
                    operation_capability.claim_id, "settlement-1",
                    "",
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
                "launch:command-1", "validator-command-1", "validator-event-1",
                "repo-1", "run-1", "item-1", "effect-1", "attempt-1",
                "observation-1", operation_observation.event_hash,
                "revision-1", "check-1", "input-1", "validator-attempt-1",
                "validator-permission-1", "validator-reservation-1",
                "validator-budget-1", 1, 1, 10,
            )
            connection = sqlite3.connect(store._database_path)
            try:
                before_invalid_validator = tuple(connection.iterdump())
            finally:
                connection.close()
            invalid_validator_requests = (
                (
                    SyntheticValidatorRequest(
                        "repo-1", "effect-1", "revision-1", "check-1",
                        "input-1", "validator-attempt-1", "read-only-1", "",
                        "PASS",
                    ),
                    1,
                    "non-empty",
                ),
                (
                    SyntheticValidatorRequest(
                        "repo-1", "effect-1", "revision-1", "check-1",
                        "input-1", "validator-attempt-1", "read-only-1", 1,
                        "PASS",
                    ),
                    1,
                    "non-empty",
                ),
                (
                    SyntheticValidatorRequest(
                        "repo-1", "effect-1", "revision-1", "check-1",
                        "input-1", "validator-attempt-1", "read-only-1",
                        "result-digest-1", "UNKNOWN",
                    ),
                    1,
                    "PASS or FAIL",
                ),
                (
                    SyntheticValidatorRequest(
                        "repo-1", "effect-1", "revision-1", "check-1",
                        "input-1", "validator-attempt-1", "read-only-1",
                        "result-digest-1", "PASS",
                    ),
                    -1,
                    "non-negative",
                ),
                (
                    SyntheticValidatorRequest(
                        "repo-1", "effect-1", "revision-1", "check-1",
                        "input-1", "validator-attempt-1", "read-only-1",
                        "result-digest-1", "PASS",
                    ),
                    0.5,
                    "non-negative",
                ),
            )
            for invalid_request, invalid_usage, message in invalid_validator_requests:
                with self.assertRaisesRegex(ValueError, message):
                    validation.launch(
                        validator_intent,
                        validator_capability,
                        invalid_request,
                        usage_units=invalid_usage,
                    )
            connection = sqlite3.connect(store._database_path)
            try:
                after_invalid_validator = tuple(connection.iterdump())
            finally:
                connection.close()
            self.assertEqual(after_invalid_validator, before_invalid_validator)
            self.assertIsNone(
                validator_adapter.reconcile(validator_capability.claim_id)
            )
            validator_request = SyntheticValidatorRequest(
                "repo-1", "effect-1", "revision-1", "check-1", "input-1",
                "validator-attempt-1", "read-only-1", "result-digest-1", "PASS",
            )
            launched = validation.launch(
                validator_intent,
                validator_capability,
                validator_request,
                usage_units=1,
                lose_result=True,
            )
            self.assertIsNone(launched.result)
            alternate_validator = SyntheticValidatorAdapter(
                root / "alternate-validator.sqlite3"
            )
            with self.assertRaisesRegex(
                DispatchDenied, "canonical repository root"
            ):
                alternate_validator._execute_committed(
                    validator_capability,
                    validator_request,
                    authority,
                    store,
                    launched.intent,
                    validator_intent,
                    usage_units=1,
                )
            self.assertIsNone(
                alternate_validator.reconcile(validator_capability.claim_id)
            )
            result = validator_adapter.reconcile(validator_capability.claim_id)
            validator_settlement_request = BudgetSettlementRequest(
                "validator-settlement-1", "validator-reservation-1", "",
                BudgetDisposition.CONSUMED, 1, result.result_id,
                "VALIDATOR_USAGE_REPORTED",
                attempt_id="validator-attempt-1",
            )
            validator_settlement = store._settle_budget(
                validator_settlement_request,
                authority.issue_settlement_proof(
                    "validator-proof-1", validator_settlement_request,
                ),
                authority,
            )
            recorded = validation.intake_result(
                ValidatorObservationCommand(
                    "validator-observation-1", "validator-observe-command-1",
                    "validator-observation-event-1", "repo-1", "run-1", "item-1",
                    "launch:command-1", "validator-settlement-1",
                    validator_settlement.settlement_hash,
                )
            )
            replay = validation.intake_result(
                ValidatorObservationCommand(
                    "validator-observation-1", "validator-observe-command-1",
                    "validator-observation-event-1", "repo-1", "run-1", "item-1",
                    "launch:command-1", "validator-settlement-1",
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
                    "item-1", "launch:command-1", "validator-settlement-1",
                    validator_settlement.settlement_hash,
                )
            )
            self.assertEqual(applied.resulting_state.value, "BLOCKED")
            self.assertTrue(replay_after_apply.replayed)
            self.assertEqual(store.table_counts()["validation_applications"], 1)
            finalization_key = store.finalization_key(
                "repo-1", "run-1", "item-1", "effect-1", "plan-1",
                "revision-1",
            )
            finalization_request = FinalizeOperationRequest(
                "finalization-1", "finalize-command-1", "finalize-event-1",
                "repo-1", "run-1", "item-1", "effect-1", "plan-1",
                "revision-1", "attempt-1", 1,
            )
            attestation = authority.issue_finalization_attestation(
                "attestation-1", "repo-1", "run-1", "item-1", "effect-1",
                "plan-1", plan.event_hash, "revision-1", applied.event_hash,
                finalization_key,
                store._event_hash(
                    {"aggregate_gate_ids": ["aggregate-release"]}
                ),
                "attempt-1", 1,
            )
            with patch.dict(os.environ, self.state_environment(root)):
                second_store = SQLiteStateStore.open_canonical(
                    "repo-1", AlwaysFreshOracle()
                )
            second_finalization = SyntheticFinalizationCoordinator(
                second_store, TransitionEngine(), authority
            )
            retry_request = replace(
                finalization_request,
                finalization_id="finalization-2",
                command_id="finalize-command-2",
                event_id="finalize-event-2",
            )
            winner_holds_lock = threading.Event()
            release_winner = threading.Event()

            def hold_before_commit(stage):
                if stage == "after_finalization_writes_before_commit":
                    winner_holds_lock.set()
                    if not release_winner.wait(timeout=5):
                        raise TimeoutError("finalization race was not released")

            with ThreadPoolExecutor(max_workers=1) as executor:
                committed_future = executor.submit(
                    finalization.finalize,
                    finalization_request,
                    attestation,
                    failure_hook=hold_before_commit,
                )
                self.assertTrue(winner_holds_lock.wait(timeout=5))
                try:
                    with self.assertRaisesRegex(
                        DispatchDenied, "writer lock is unavailable"
                    ):
                        second_finalization.finalize(retry_request, attestation)
                finally:
                    release_winner.set()
                committed = committed_future.result()
            replay = second_finalization.finalize(retry_request, attestation)
            self.assertFalse(committed.replayed)
            self.assertTrue(replay.replayed)
            self.assertEqual(replay, replace(committed, replayed=True))
            self.assertEqual(committed.resulting_state.value, "COMPLETED")
            self.assertEqual(store.table_counts()["operation_finalizations"], 1)
            self.assertEqual(store.table_counts()["outstanding_slot"], 0)

    def test_c05_coordinator_forwards_classification_to_store_boundary(self) -> None:
        authority = SyntheticAuthority(b"c" * 32)
        classification = authority.issue_classification(
            "classification-1", "repo-1", "run-1", "item-1", "effect-1",
            "revision-1", "check-1", "validator-attempt-1",
            "validator-observation-1", "observation-hash", "result-digest-1",
            verdict="FAIL", policy_id="failure-policy", policy_version="1",
            classification="FINAL",
        )

        class CapturingStore:
            is_canonical = True

            def _bind_classification_authority(self, bound_authority):
                self.authority = bound_authority

            def _apply_validator_observation(self, request, **kwargs):
                self.classification = kwargs["classification"]
                return ApplicationReceipt(
                    request.application_id, request.command_id, request.event_id,
                    1, "event-hash", LifecycleState.FAILED_FINAL, False,
                )

        store = CapturingStore()
        coordinator = SyntheticValidationCoordinator(
            store, TransitionEngine(), authority, None
        )
        result = coordinator.apply_result(
            ValidationApplicationRequest(
                "application-1", "apply-command-1", "apply-event-1",
                "repo-1", "run-1", "item-1", "effect-1", "revision-1",
                "check-1", "validator-attempt-1", "validator-observation-1",
            ),
            classification=classification,
        )

        self.assertEqual(result.resulting_state, LifecycleState.FAILED_FINAL)
        self.assertIs(store.classification, classification)
        self.assertIs(store.authority, authority)


if __name__ == "__main__":
    unittest.main()
