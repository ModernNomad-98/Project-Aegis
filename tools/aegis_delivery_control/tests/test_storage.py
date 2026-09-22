from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor
from dataclasses import replace
from datetime import datetime, timezone
import hashlib
import gc
import inspect
import json
import multiprocessing
import sqlite3
import shutil
import tempfile
import threading
import unittest
from unittest.mock import patch
from pathlib import Path
from typing import Mapping

import tools.aegis_delivery_control.contracts as contract_types
import tools.aegis_delivery_control.storage as storage_module
from tools.aegis_delivery_control.authority import (
    SyntheticAuthority,
    SyntheticAuthorityLifecycleEvidence,
    SyntheticGrant,
    SyntheticOperatorGrant,
    SyntheticSettlementProof,
    SyntheticSourceGrant,
    SyntheticValidatorGrant,
)
from tools.aegis_delivery_control.adapters import (
    SyntheticExecutionAdapter,
    SyntheticValidatorAdapter,
    SyntheticValidatorRequest,
    synthetic_validator_output_size,
    validate_synthetic_validator_containment,
)
from tools.aegis_delivery_control.contracts import (
    AuthorityFactKind,
    AuthorityLifecycleFactRequest,
    BindingMismatchKind,
    BindingMismatchRequest,
    BudgetDisposition,
    BudgetSettlementRequest as BudgetSettlementContract,
    CommitReceipt,
    DispatchDenied,
    EffectAdoptionRequest,
    EffectRelationshipKind,
    EffectObservationRequest,
    FinalizeOperationRequest,
    InjectedFailure,
    IntentRequest,
    LifecycleState,
    OperationOriginKind,
    GovernedOrder,
    PauseBeforeDispatchRequest,
    PauseActivitySettlementRequest,
    PauseExternalMutationRequest,
    PauseLocalExecutionRequest,
    PauseReconciliationRequest,
    PlanAcceptanceRequest as PlanAcceptanceContract,
    ReadinessEvaluationRequest,
    RecoverProvenNonexecutionRequest,
    ProvenNonexecutionIntentRequest,
    ResumeActivitySettlementRequest,
    ResumeOperationNonexecutionRequest,
    ResumeRequest,
    SourceControlClassification,
    SourceControlEvidenceRequest,
    StopMode,
    StopEscalationRequest,
    StopEscalationSettlement,
    StopRequest,
    StorageIntegrityError,
    SyntheticGrantKind,
    SyntheticSourceConsumerKind,
    DispatchPosture,
    TerminalRestartDisposition,
    TerminalRestartRequest,
    TerminalRestartVerification,
    TerminalValidationSettlementRequest,
    ValidationApplicationRequest,
    ValidationRecoveryRequest,
    ValidatorCessationRequest,
    ValidatorContainmentSpec,
    ValidatorIntentRequest,
    ValidatorObservationRequest as ValidatorObservationRequestContract,
    SYNTHETIC_VALIDATOR_SUPPORT_DIGEST,
    SYNTHETIC_VALIDATOR_SUPPORT_ID,
    validator_containment_digest,
    validator_containment_spec_json,
    parse_validator_containment_spec,
)
from tools.aegis_delivery_control.engine import TRANSITIONS, TransitionEngine
from tools.aegis_delivery_control.dispatch import SyntheticReadCoordinator
from tools.aegis_delivery_control.storage import (
    SQLiteStateReader,
    SQLiteStateStore,
    raise_at,
)
from tools.aegis_delivery_control.tests._legacy_schema import (
    strip_t28_foundation_schema,
)


def BudgetSettlementRequest(*args, **kwargs):
    kwargs.setdefault("repository_id", "repo-1")
    kwargs.setdefault("run_id", "run-1")
    kwargs.setdefault("item_id", "item-1")
    kwargs.setdefault("logical_effect_id", "effect-1")
    reservation_id = kwargs.get("reservation_id")
    if reservation_id is None and len(args) > 1:
        reservation_id = args[1]
    if isinstance(reservation_id, str) and reservation_id.startswith(
        "validator-reservation-"
    ):
        kwargs.setdefault(
            "attempt_id",
            reservation_id.replace("validator-reservation-", "validator-attempt-", 1),
        )
    else:
        kwargs.setdefault("attempt_id", "attempt-1")
    return BudgetSettlementContract(*args, **kwargs)


def PlanAcceptanceRequest(*args, **kwargs):
    """Build a newly accepted synthetic plan with explicit immutable pins."""
    kwargs.setdefault("source_tree_digest", "source-tree-1")
    kwargs.setdefault("item_definition_digest", "item-definition-1")
    kwargs.setdefault("plan_schema_version", "plan-schema-1")
    kwargs.setdefault("reducer_version", "reducer-1")
    return PlanAcceptanceContract(*args, **kwargs)


def validator_containment(input_digest: str, suffix: str = "1"):
    spec = ValidatorContainmentSpec(
        1,
        SYNTHETIC_VALIDATOR_SUPPORT_ID,
        SYNTHETIC_VALIDATOR_SUPPORT_DIGEST,
        input_digest,
        f"inputs/{suffix}",
        f"outputs/{suffix}",
        f"scratch/{suffix}",
        ("READ_PINNED_INPUT", "EMIT_BOUNDED_RESULT"),
        4096,
        "DENY",
        "DENY",
        "DENY",
    )
    return validator_containment_spec_json(spec), validator_containment_digest(spec)


def ValidatorObservationRequest(*args, **kwargs):
    input_digest = kwargs.get("input_digest", args[13])
    validator_attempt_id = kwargs.get("validator_attempt_id", args[8])
    suffix = validator_attempt_id.replace("validator-attempt-", "", 1)
    _, containment_digest = validator_containment(input_digest, suffix)
    kwargs.setdefault("containment_digest", containment_digest)
    return ValidatorObservationRequestContract(*args, **kwargs)


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


class CompleteFreshnessOracle:
    def __init__(self, catalog_head: str, run_heads: Mapping[str, str]) -> None:
        self.catalog_head = catalog_head
        self.run_heads = dict(run_heads)

    def verify(
        self,
        repository_id: str,
        catalog_head: str,
        run_heads: Mapping[str, str],
    ) -> bool:
        return (
            repository_id == "repo-1"
            and catalog_head == self.catalog_head
            and dict(run_heads) == self.run_heads
        )


def _settle_until_terminated(
    database_path,
    issuer_key,
    allowed_head,
    request,
    stop_stage,
    ready,
):
    oracle = MutableFreshnessOracle()
    oracle.allowed_head = allowed_head
    store = SQLiteStateStore(Path(database_path), oracle, "repo-1")
    authority = SyntheticAuthority(issuer_key)
    store._bind_classification_authority(authority)

    def hold(stage):
        if stage == stop_stage:
            ready.set()
            threading.Event().wait()

    store._settle_budget(
        request,
        authority.issue_settlement_proof("process-proof", request),
        authority,
        failure_hook=hold,
    )


class SQLiteStateStoreTests(unittest.TestCase):
    def _row_count(self, table_name: str) -> int:
        connection = sqlite3.connect(self.database_path)
        try:
            return int(
                connection.execute(
                    f"SELECT COUNT(*) FROM {table_name}"
                ).fetchone()[0]
            )
        finally:
            connection.close()

    def test_proven_nonexecution_exposes_typed_recovery_contracts(self) -> None:
        for name in (
            "ResumeOperationNonexecutionRequest",
            "RecoverProvenNonexecutionRequest",
            "ProvenNonexecutionIntentRequest",
        ):
            self.assertTrue(
                hasattr(contract_types, name),
                f"proven nonexecution requires typed {name}",
            )

    def test_t07_exposes_typed_activity_pause_settlement_contract(self) -> None:
        self.assertTrue(
            hasattr(contract_types, "PauseActivitySettlementRequest"),
            "T07 requires a typed PauseActivitySettlementRequest contract",
        )

    def test_t05_exposes_typed_local_execution_pause_contract(self) -> None:
        self.assertTrue(
            hasattr(contract_types, "PauseLocalExecutionRequest"),
            "T05 requires a typed PauseLocalExecutionRequest contract",
        )
        request_type = contract_types.PauseLocalExecutionRequest
        request = request_type(
            pause_id="local-pause-1",
            command_id="local-pause-command-1",
            event_id="local-pause-event-1",
            fence_id="local-pause-fence-1",
            repository_id="repo-1",
            run_id="run-1",
            item_id="item-1",
            logical_effect_id="effect-1",
            attempt_id="attempt-1",
            intent_event_id="event-1",
            intent_event_hash="intent-hash-1",
            expected_slot_generation=1,
            reason_code="OPERATOR_PAUSE",
        )
        request.validate()
        with self.assertRaisesRegex(ValueError, "local pause"):
            replace(request, expected_slot_generation=0).validate()

    def test_t14_exposes_typed_resume_request_contract(self) -> None:
        self.assertTrue(
            hasattr(contract_types, "ResumeRequest"),
            "T14 requires a typed ResumeRequest contract",
        )
        request_type = contract_types.ResumeRequest
        request = request_type(
            resume_id="resume-1",
            command_id="resume-command-1",
            event_id="resume-event-1",
            repository_id="repo-1",
            run_id="run-1",
            item_id="item-1",
            logical_effect_id="effect-1",
            plan_id="plan-1",
            revision_digest="revision-1",
            source_pause_id="pause-1",
            source_pause_settled_event_id="pause-settled-event-1",
            source_pause_settled_event_hash="pause-settled-hash-1",
            pause_fence_id="pause-fence-1",
            expected_preserved_lifecycle=LifecycleState.PLANNED,
            expected_preserved_continuation_cursor=None,
            expected_catalog_head="catalog-head-1",
            expected_run_head="run-head-1",
            expected_run_heads_digest="run-heads-digest-1",
        )
        request.validate()
        self.assertEqual(request.expected_preserved_lifecycle, LifecycleState.PLANNED)
        with self.assertRaisesRegex(ValueError, "resume"):
            replace(request, expected_run_heads_digest="").validate()

    def setUp(self) -> None:
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary_directory.cleanup)
        database_path = Path(self.temporary_directory.name) / "state.sqlite3"
        self.database_path = database_path
        self.oracle = MutableFreshnessOracle()
        self.store = SQLiteStateStore(
            database_path,
            self.oracle,
            "repo-1",
            utc_now=lambda: datetime(2026, 9, 21, tzinfo=timezone.utc),
        )
        self.authority = SyntheticAuthority()
        self.store._bind_classification_authority(self.authority)
        self.authority.register(
            SyntheticGrant(
                "grant-1", "repo-1", "effect-1", "attempt-1", "scope-1"
            )
        )
        self.capability = self.authority.claim(
            "grant-1", "repo-1", "effect-1", "attempt-1", "scope-1"
        )

    def test_t28_source_head_is_in_complete_freshness_vector(self) -> None:
        plan = self.store.accept_plan(
            PlanAcceptanceRequest(
                plan_id="source-plan-1",
                command_id="source-plan-command-1",
                event_id="source-plan-event-1",
                repository_id="repo-1",
                run_id="source-run-1",
                item_id="source-item-1",
                logical_effect_id="source-effect-1",
                revision_digest="source-revision-1",
                effect_descriptor_digest="source-descriptor-1",
                permission_scope_digest="source-permission-1",
                budget_policy_digest="source-budget-1",
                check_ids=("source-check-1",),
            ),
            expected_head="",
            writer_epoch=1,
        )
        self.oracle.allowed_head = plan.event_hash
        grant = self.authority.issue_source_grant(
            grant_id="source-grant-1",
            grant_kind=SyntheticGrantKind.ADOPTION,
            action="ADOPT_VERIFIED_EFFECT",
            repository_id="repo-1",
            logical_effect_id="source-effect-1",
            source_id="synthetic-source-1",
            source_version="1",
            terms_digest="source-terms-1",
            scope_digest="source-scope-1",
            binding_digest="source-binding-1",
            not_before="2026-09-20T00:00:00.000000Z",
            expires_at="2026-09-22T00:00:00.000000Z",
            use_limit=1,
        )
        registered = self.store.register_synthetic_source_grant(
            grant, self.authority
        )
        self.oracle.allowed_head = registered.event_hash
        before_catalog, before_heads = self.store.load_verified("repo-1")
        self.assertIn("@aegis/source/synthetic-authority", before_heads)
        rollback_path = Path(self.temporary_directory.name) / "source-rollback.sqlite3"
        source = sqlite3.connect(self.database_path)
        target = sqlite3.connect(rollback_path)
        try:
            source.backup(target)
        finally:
            target.close()
            source.close()
        capability = self.authority.issue_source_capability(
            grant,
            consumer_kind=SyntheticSourceConsumerKind.MANUAL,
            consumer_key="manual-source-use-1",
            binding_digest="source-binding-1",
        )
        consumed = self.store.consume_synthetic_source_for_test(
            capability, self.authority
        )
        replayed = self.store.consume_synthetic_source_for_test(
            capability, self.authority
        )
        self.assertTrue(replayed.replayed)
        self.assertEqual(replayed.event_hash, consumed.event_hash)
        self.oracle.allowed_head = consumed.event_hash
        after_catalog, after_heads = self.store.load_verified("repo-1")
        self.assertEqual(
            before_heads["source-run-1"], after_heads["source-run-1"]
        )
        self.assertNotEqual(
            before_heads["@aegis/source/synthetic-authority"],
            after_heads["@aegis/source/synthetic-authority"],
        )
        rollback = SQLiteStateStore(
            rollback_path,
            CompleteFreshnessOracle(after_catalog, after_heads),
            "repo-1",
            utc_now=lambda: datetime(2026, 9, 21, tzinfo=timezone.utc),
        )
        with self.assertRaisesRegex(DispatchDenied, "freshness"):
            rollback.load_verified("repo-1")
        connection = sqlite3.connect(rollback_path)
        try:
            before_stale_use = tuple(connection.iterdump())
        finally:
            connection.close()
        with self.assertRaisesRegex(DispatchDenied, "freshness"):
            rollback.consume_synthetic_source_for_test(
                capability, self.authority
            )
        connection = sqlite3.connect(rollback_path)
        try:
            after_stale_use = tuple(connection.iterdump())
        finally:
            connection.close()
        self.assertEqual(after_stale_use, before_stale_use)
        del rollback
        gc.collect()

    def test_f05_older_valid_effect_checkpoint_denies_current_dispatch(self) -> None:
        plan = self.store.accept_plan(
            PlanAcceptanceRequest(
                "plan-1", "plan-command-1", "plan-event-1", "repo-1",
                "run-1", "item-1", "effect-1", "revision-1",
                "descriptor-digest", "scope-1", "budget-policy-digest",
                ("check-1",),
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
        rollback_path = Path(self.temporary_directory.name) / "effect-rollback.sqlite3"
        source = sqlite3.connect(self.database_path)
        target = sqlite3.connect(rollback_path)
        try:
            source.backup(target)
        finally:
            target.close()
            source.close()
        settlement_request = BudgetSettlementRequest(
            "settlement-1", "reservation-1", "", BudgetDisposition.CONSUMED,
            2, "receipt-1", "USAGE_REPORTED",
        )
        settlement = self.store._settle_budget(
            settlement_request,
            self.authority.issue_settlement_proof("proof-1", settlement_request),
            self.authority,
        )
        self.oracle.allowed_head = settlement.settlement_hash
        receipt = self._record_signed_effect_observation(
            EffectObservationRequest(
                "observation-1", "observe-command-1", "observation-event-1",
                "repo-1", "run-1", "item-1", "effect-1", "attempt-1",
                "receipt-1", self.capability.claim_id, "descriptor-digest", 2,
                "settlement-1", settlement.settlement_hash,
            )
        )
        self.oracle.allowed_head = receipt.event_hash
        current_catalog, current_heads = self.store.load_verified(
            "repo-1", authority=self.authority
        )
        stale = SQLiteStateStore(
            rollback_path,
            CompleteFreshnessOracle(current_catalog, current_heads),
            "repo-1",
        )
        with self.assertRaisesRegex(DispatchDenied, "freshness"):
            stale.load_verified("repo-1", authority=self.authority)

    def test_f05_complete_freshness_vector_rejects_every_inexact_map(self) -> None:
        current_catalog = "catalog-current"
        current_heads = {
            "run-1": "run-1-current",
            "run-2": "run-2-current",
            "@aegis/source/synthetic-authority": "source-current",
        }
        oracle = CompleteFreshnessOracle(current_catalog, current_heads)
        self.assertTrue(
            oracle.verify("repo-1", current_catalog, current_heads)
        )
        inexact_vectors = {
            "older effect/run head": {
                **current_heads,
                "run-1": "run-1-older-valid",
            },
            "older one-use source consumption": {
                **current_heads,
                "@aegis/source/synthetic-authority": "source-older-valid",
            },
            "omitted source": {
                key: value
                for key, value in current_heads.items()
                if key != "@aegis/source/synthetic-authority"
            },
            "omitted run": {
                key: value
                for key, value in current_heads.items()
                if key != "run-2"
            },
            "additional unproven run": {
                **current_heads,
                "run-unproven": "unproven-head",
            },
            "source and export heads substituted": {
                **current_heads,
                "run-1": current_heads["@aegis/source/synthetic-authority"],
                "@aegis/source/synthetic-authority": current_heads["run-1"],
            },
        }
        for condition, candidate_heads in inexact_vectors.items():
            with self.subTest(condition=condition):
                self.assertFalse(
                    oracle.verify("repo-1", current_catalog, candidate_heads)
                )
        for condition, candidate_catalog in {
            "stale anchor": "catalog-older-valid",
            "rewritten local anchor": "catalog-rewritten",
            "newer pending commit omitted": "catalog-before-pending-commit",
            "contradictory anchor": current_heads["run-1"],
        }.items():
            with self.subTest(condition=condition):
                self.assertFalse(
                    oracle.verify("repo-1", candidate_catalog, current_heads)
                )
        self.assertFalse(
            oracle.verify("foreign-repository", current_catalog, current_heads)
        )

    def test_f05_every_dispatch_capable_boundary_declares_freshness_guard(self) -> None:
        guarded_methods = (
            "register_synthetic_source_grant",
            "consume_synthetic_source_for_test",
            "accept_plan",
            "resume",
            "resume_reconciliation_pause",
            "resume_operation_nonexecution",
            "recover_proven_nonexecution",
            "resume_activity_settlement",
            "commit_intent",
            "claim_operation_launch",
            "_contact_claimed_operation",
            "_contact_committed_validator",
            "resolve_validation_blocker",
            "commit_validator_intent",
            "adopt_verified_effect",
            "_finalize_operation",
            "load_verified",
        )
        for method_name in guarded_methods:
            with self.subTest(method=method_name):
                source = inspect.getsource(
                    getattr(SQLiteStateStore, method_name)
                )
                self.assertIn(
                    "_freshness_oracle.verify",
                    source,
                    f"{method_name} lost its independent freshness guard",
                )

    def test_f05_stale_operation_boundaries_deny_without_mutation(self) -> None:
        plan = self.store.accept_plan(
            PlanAcceptanceRequest(
                "plan-1", "plan-command-1", "plan-event-1", "repo-1",
                "run-1", "item-1", "effect-1", "revision-1",
                "descriptor-digest", "scope-1", "budget-policy-digest",
                ("check-1",),
            ),
            expected_head="", writer_epoch=1,
        )
        self.oracle.allowed_head = plan.event_hash

        def snapshot():
            connection = sqlite3.connect(self.database_path)
            try:
                return tuple(connection.iterdump())
            finally:
                connection.close()

        before = snapshot()
        self.oracle.allowed_head = "stale-before-intent"
        with self.assertRaisesRegex(DispatchDenied, "freshness"):
            self.store.commit_intent(
                self.request(), self.capability, self.authority,
                expected_head=plan.event_hash, writer_epoch=2,
            )
        self.assertEqual(snapshot(), before)

        self.oracle.allowed_head = plan.event_hash
        committed = self.store.commit_intent(
            self.request(), self.capability, self.authority,
            expected_head=plan.event_hash, writer_epoch=2,
        )
        self.oracle.allowed_head = committed.event_hash
        before = snapshot()
        self.oracle.allowed_head = "stale-before-launch"
        with self.assertRaisesRegex(DispatchDenied, "freshness"):
            self.store.claim_operation_launch(self.request(), committed)
        self.assertEqual(snapshot(), before)

        self.oracle.allowed_head = committed.event_hash
        launched = self.store.claim_operation_launch(
            self.request(), committed
        )
        self.oracle.allowed_head = launched.event_hash
        before = snapshot()
        self.oracle.allowed_head = "stale-before-contact"
        with self.assertRaisesRegex(DispatchDenied, "freshness"):
            self.store._contact_claimed_operation(
                self.request(), self.capability, committed, launched,
                self.store._adapter_target_digest("repo-1", "EFFECT"),
            )
        self.assertEqual(snapshot(), before)

    def test_f05_stale_validator_boundaries_deny_without_mutation(self) -> None:
        observation = self._record_effect_observation(check_ids=("check-1",))
        intent, capability = self._validator_intent(observation)

        def snapshot():
            connection = sqlite3.connect(self.database_path)
            try:
                return tuple(connection.iterdump())
            finally:
                connection.close()

        before = snapshot()
        self.oracle.allowed_head = "stale-before-validator-intent"
        with self.assertRaisesRegex(DispatchDenied, "freshness"):
            self.store.commit_validator_intent(
                intent, capability, self.authority
            )
        self.assertEqual(snapshot(), before)

        self.oracle.allowed_head = observation.event_hash
        committed = self.store.commit_validator_intent(
            intent, capability, self.authority
        )
        self.oracle.allowed_head = committed.event_hash
        validator_path = self.database_path.parent / "synthetic-validator.sqlite3"
        adapter = SyntheticValidatorAdapter(validator_path)
        adapter._canonical_repository_id = "repo-1"
        adapter._canonical_ledger_path = validator_path.resolve()
        spec = parse_validator_containment_spec(intent.containment_spec_json)
        request = SyntheticValidatorRequest(
            "repo-1", "effect-1", "revision-1", "check-1", "input-1",
            "validator-attempt-1", "read-only-scope-1", "result-digest-1",
            "PASS", capability.containment_digest, spec.allowed_actions,
            spec.input_root, f"{spec.output_root}/result.json",
            f"{spec.scratch_root}/work",
            synthetic_validator_output_size("result-digest-1", "PASS"),
        )
        before = snapshot()
        self.oracle.allowed_head = "stale-before-validator-contact"
        with self.assertRaisesRegex(DispatchDenied, "freshness"):
            adapter._execute_committed(
                capability, request, self.authority, self.store, committed,
                intent, usage_units=1,
            )
        self.assertEqual(snapshot(), before)
        self.assertIsNone(adapter.reconcile(capability.claim_id))

    def test_f06_same_owner_cannot_start_other_run_before_or_after_stop(self) -> None:
        first = self._commit_planned_intent(
            self.request(), self.capability, self.authority,
            expected_head="", writer_epoch=1,
        )
        self.oracle.allowed_head = first.event_hash
        second_grant = SyntheticGrant(
            "grant-2", "repo-1", "effect-2", "attempt-2", "scope-2"
        )
        self.authority.register(second_grant)
        second_capability = self.authority.claim(*second_grant.__dict__.values())
        second_plan = self.store.accept_plan(
            PlanAcceptanceRequest(
                "plan-2", "plan-command-2", "plan-event-2", "repo-1",
                "run-2", "item-2", "effect-2", "revision-2",
                "descriptor-2", "scope-2", "budget-2", ("check-2",),
            ),
            expected_head=first.event_hash,
            writer_epoch=3,
        )
        self.oracle.allowed_head = second_plan.event_hash
        second_request = IntentRequest(
            "repo-1", "run-2", "item-2", "command-2", "event-2",
            "effect-2", "descriptor-2", "attempt-2", "permission-2",
            "reservation-2", "budget-2", 1, 2, 10,
        )
        for target_store in (
            self.store,
            SQLiteStateStore(self.database_path, self.oracle, "repo-1"),
        ):
            with self.assertRaisesRegex(DispatchDenied, "repository slot"):
                target_store.commit_intent(
                    second_request, second_capability, self.authority,
                    expected_head=second_plan.event_hash, writer_epoch=4,
                )
        self.assertEqual(self.store.table_counts()["effects"], 1)
        self.assertEqual(self.store.table_counts()["budget_reservations"], 1)
        stop = self.store.stop(
            self._stop_request(),
            self._stop_capability(StopMode.IMMEDIATE),
            self.authority,
        )
        self.oracle.allowed_head = stop.event_hash
        reopened = SQLiteStateStore(self.database_path, self.oracle, "repo-1")
        with self.assertRaisesRegex(DispatchDenied, "repository slot"):
            reopened.commit_intent(
                second_request, second_capability, self.authority,
                expected_head=stop.event_hash, writer_epoch=6,
            )
        connection = sqlite3.connect(self.database_path)
        try:
            slot = connection.execute(
                "SELECT run_id, logical_effect_id, attempt_id, generation FROM "
                "outstanding_slot"
            ).fetchone()
        finally:
            connection.close()
        self.assertEqual(slot, ("run-1", "effect-1", "attempt-1", 1))

    def test_f06_slot_denies_other_operations_across_reachable_dispositions(self) -> None:
        primary = self._commit_planned_intent(
            self.request(), self.capability, self.authority,
            expected_head="", writer_epoch=1,
        )
        self.oracle.allowed_head = primary.event_hash
        contenders = []
        current_head = primary.event_hash
        for number in (2, 3):
            suffix = str(number)
            grant = SyntheticGrant(
                f"grant-{suffix}", "repo-1", f"effect-{suffix}",
                f"attempt-{suffix}", f"scope-{suffix}",
            )
            self.authority.register(grant)
            capability = self.authority.claim(*grant.__dict__.values())
            plan = self.store.accept_plan(
                PlanAcceptanceRequest(
                    f"plan-{suffix}", f"plan-command-{suffix}",
                    f"plan-event-{suffix}", "repo-1", f"run-{suffix}",
                    f"item-{suffix}", f"effect-{suffix}",
                    f"revision-{suffix}", f"descriptor-{suffix}",
                    f"scope-{suffix}", f"budget-{suffix}",
                    (f"check-{suffix}",),
                ),
                expected_head=current_head,
                writer_epoch=number + 1,
            )
            current_head = plan.event_hash
            self.oracle.allowed_head = current_head
            contenders.append(
                (
                    IntentRequest(
                        "repo-1", f"run-{suffix}", f"item-{suffix}",
                        f"command-{suffix}", f"event-{suffix}",
                        f"effect-{suffix}", f"descriptor-{suffix}",
                        f"attempt-{suffix}", f"permission-{suffix}",
                        f"reservation-{suffix}", f"budget-{suffix}",
                        1, 2, 10,
                    ),
                    capability,
                )
            )
        source = self.database_path.parent / "f06-source.sqlite3"
        shutil.copy2(self.database_path, source)

        def repository_head(path: Path) -> str:
            connection = sqlite3.connect(path)
            try:
                return connection.execute(
                    "SELECT catalog_head FROM repositories WHERE "
                    "repository_id = 'repo-1'"
                ).fetchone()[0]
            finally:
                connection.close()

        dispositions = (
            "initiated",
            "launched-unsettled",
            "contacted-uncertain",
            "pausing",
            "graceful-draining",
            "validating",
            "reconciliation",
            "stopped",
        )
        for disposition in dispositions:
            with self.subTest(disposition=disposition):
                path = self.database_path.parent / f"f06-{disposition}.sqlite3"
                shutil.copy2(source, path)
                oracle = MutableFreshnessOracle()
                oracle.allowed_head = current_head
                branch = SQLiteStateStore(path, oracle, "repo-1")
                branch._bind_classification_authority(self.authority)
                if disposition in {"launched-unsettled", "contacted-uncertain"}:
                    launched = branch.claim_operation_launch(
                        self.request(), primary
                    )
                    oracle.allowed_head = launched.event_hash
                    if disposition == "contacted-uncertain":
                        branch._contact_claimed_operation(
                            self.request(), self.capability, primary, launched,
                            branch._adapter_target_digest("repo-1", "EFFECT"),
                        )
                        oracle.allowed_head = repository_head(path)
                elif disposition == "pausing":
                    paused = branch.pause_local_execution(
                        self._local_pause_request(
                            primary, suffix="f06-matrix"
                        ),
                        self._pause_capability("f06-matrix"),
                        self.authority,
                    )
                    oracle.allowed_head = paused.event_hash
                elif disposition == "graceful-draining":
                    stopped = branch.stop(
                        self._stop_request(
                            StopMode.GRACEFUL, "f06-graceful"
                        ),
                        self._stop_capability(
                            StopMode.GRACEFUL, "f06-graceful"
                        ),
                        self.authority,
                    )
                    oracle.allowed_head = stopped.event_hash
                elif disposition in {"validating", "reconciliation"}:
                    observation = self._record_signed_effect_observation(
                        EffectObservationRequest(
                            f"f06-{disposition}-observation",
                            f"f06-{disposition}-command",
                            f"f06-{disposition}-event",
                            "repo-1", "run-1", "item-1", "effect-1",
                            "attempt-1", f"f06-{disposition}-receipt",
                            self.capability.claim_id, "descriptor-digest",
                            2 if disposition == "validating" else None,
                            f"f06-{disposition}-settlement", "",
                        ),
                        classification=(
                            SourceControlClassification.KNOWN
                            if disposition == "validating"
                            else SourceControlClassification.UNKNOWN
                        ),
                        store=branch,
                    )
                    oracle.allowed_head = observation.event_hash
                elif disposition == "stopped":
                    stopped = branch.stop(
                        self._stop_request(
                            StopMode.IMMEDIATE, "f06-immediate"
                        ),
                        self._stop_capability(
                            StopMode.IMMEDIATE, "f06-immediate"
                        ),
                        self.authority,
                    )
                    oracle.allowed_head = stopped.event_hash

                reopened = SQLiteStateStore(path, oracle, "repo-1")
                reopened._bind_classification_authority(self.authority)
                connection = sqlite3.connect(path)
                try:
                    before = tuple(connection.iterdump())
                    original_slot = connection.execute(
                        "SELECT run_id, logical_effect_id, attempt_id, "
                        "generation FROM outstanding_slot"
                    ).fetchone()
                finally:
                    connection.close()
                for contender, capability in contenders:
                    with self.assertRaisesRegex(
                        DispatchDenied, "repository slot"
                    ):
                        reopened.commit_intent(
                            contender,
                            capability,
                            self.authority,
                            expected_head=oracle.allowed_head,
                            writer_epoch=100,
                        )
                connection = sqlite3.connect(path)
                try:
                    after = tuple(connection.iterdump())
                    retained_slot = connection.execute(
                        "SELECT run_id, logical_effect_id, attempt_id, "
                        "generation FROM outstanding_slot"
                    ).fetchone()
                finally:
                    connection.close()
                self.assertEqual(after, before)
                self.assertEqual(retained_slot, original_slot)
                reopened.load_verified("repo-1", authority=self.authority)

    def test_f06_proven_nonexecution_with_unknown_billing_retains_slot(self) -> None:
        committed = self._commit_planned_intent(
            self.request(), self.capability, self.authority,
            expected_head="", writer_epoch=1,
        )
        self.oracle.allowed_head = committed.event_hash
        target_path = self.database_path.parent / "synthetic-target.sqlite3"
        adapter = SyntheticExecutionAdapter(target_path)
        adapter._canonical_repository_id = "repo-1"
        adapter._canonical_ledger_path = target_path.resolve()
        attestation = self.authority.issue_nonexecution_attestation(
            "f06-unknown-attestation", "f06-unknown-seal", "EFFECT",
            adapter._target_digest("repo-1"), self.capability.claim_id,
            f"EFFECT-INTENT:{committed.command_id}", committed.event_hash,
            "reservation-1", "repo-1", "run-1", "item-1", "effect-1",
            "attempt-1",
        )
        seal = adapter.seal_nonexecution(attestation, self.authority)
        unknown = BudgetSettlementRequest(
            "f06-unknown-settlement", "reservation-1", "",
            BudgetDisposition.UNKNOWN_WORST_CASE_CHARGED, None,
            "f06-unknown-evidence", "NONDISPATCH_BILLING_UNKNOWN",
            non_dispatch_proven=True,
            zero_liability_proven=False,
            release_slot=False,
            all_obligations_settled=False,
            nonexecution_seal_id=seal.seal_id,
        )
        settled = self.store._settle_budget(
            unknown,
            self.authority.issue_settlement_proof(
                "f06-unknown-settlement-proof", unknown
            ),
            self.authority,
        )
        self.oracle.allowed_head = settled.settlement_hash
        self.assertEqual(
            self.store.load_run_lifecycle("run-1"),
            LifecycleState.RECONCILIATION_REQUIRED,
        )
        connection = sqlite3.connect(self.database_path)
        try:
            accounting = connection.execute(
                "SELECT disposition, charged_units, uncertainty FROM "
                "budget_reservations WHERE reservation_id = 'reservation-1'"
            ).fetchone()
        finally:
            connection.close()
        self.assertEqual(
            accounting,
            (BudgetDisposition.UNKNOWN_WORST_CASE_CHARGED.value, 5, 1),
        )
        self._assert_f06_contenders_denied_on_copy(
            label="proven-no-effect-unknown-billing",
            expected_head=settled.settlement_hash,
        )

    def test_t28_adopts_completed_effect_without_delivery_or_reused_charge(
        self,
    ) -> None:
        semantic_inputs = (("input", "digest-1"),)
        descriptor = self.store.canonical_effect_descriptor_digest(
            "WRITE", "synthetic-target-1", semantic_inputs, 1
        )
        plan = self.store.accept_plan(
            PlanAcceptanceRequest(
                "plan-1", "plan-command-1", "plan-event-1", "repo-1",
                "run-1", "item-1", "effect-1", "revision-1",
                descriptor, "scope-1", "budget-policy-digest",
                ("check-1",), ("check-1",),
                effect_action="WRITE",
                effect_target="synthetic-target-1",
                effect_semantic_inputs=semantic_inputs,
                target_generation=1,
            ),
            expected_head="", writer_epoch=1,
        )
        self.oracle.allowed_head = plan.event_hash
        operation_request = replace(
            self.request(), effect_descriptor_digest=descriptor
        )
        committed = self.store.commit_intent(
            operation_request, self.capability, self.authority,
            expected_head=plan.event_hash, writer_epoch=2,
        )
        self.oracle.allowed_head = committed.event_hash
        settlement_request = BudgetSettlementRequest(
            "settlement-1", "reservation-1", "",
            BudgetDisposition.CONSUMED, 2, "receipt-1", "USAGE_REPORTED",
        )
        settlement = self.store._settle_budget(
            settlement_request,
            self.authority.issue_settlement_proof(
                "proof-1", settlement_request
            ),
            self.authority,
        )
        self.oracle.allowed_head = settlement.settlement_hash
        root_observation = self._record_signed_effect_observation(
            EffectObservationRequest(
                "observation-1", "observe-command-1",
                "observation-event-1", "repo-1", "run-1", "item-1",
                "effect-1", "attempt-1", "receipt-1",
                self.capability.claim_id, descriptor, 2, "settlement-1",
                settlement.settlement_hash,
            )
        )
        self.oracle.allowed_head = root_observation.event_hash
        validator_observation = self._record_validator_result_for(
            root_observation, suffix="1", verdict="PASS"
        )
        applied = self.store._apply_validator_observation(
            ValidationApplicationRequest(
                "application-1", "apply-command-1", "apply-event-1",
                "repo-1", "run-1", "item-1", "effect-1", "revision-1",
                "check-1", "validator-attempt-1",
                validator_observation.observation_id,
            )
        )
        self.oracle.allowed_head = applied.event_hash
        root_request, root_attestation = (
            self._finalization_request_and_attestation(applied.event_hash)
        )
        root_finalization = self.store._finalize_operation(
            root_request, root_attestation, self.authority
        )
        self.oracle.allowed_head = root_finalization.event_hash
        adopted_plan = self.store.accept_plan(
            PlanAcceptanceRequest(
                "plan-2", "plan-command-2", "plan-event-2", "repo-1",
                "run-2", "item-2", "effect-1", "revision-2",
                descriptor, "scope-2", "budget-policy-2", ("check-2",),
                ("check-2",), effect_action="WRITE",
                effect_target="synthetic-target-1",
                effect_semantic_inputs=semantic_inputs,
                target_generation=1,
            ),
            expected_head=root_finalization.event_hash, writer_epoch=100,
        )
        self.oracle.allowed_head = adopted_plan.event_hash
        connection = sqlite3.connect(self.database_path)
        try:
            connection.row_factory = sqlite3.Row
            root_row = connection.execute(
                "SELECT observation_digest FROM effect_observations WHERE "
                "observation_id = 'observation-1'"
            ).fetchone()
            intent_hash = connection.execute(
                "SELECT event_hash FROM events WHERE event_id = 'event-1'"
            ).fetchone()[0]
        finally:
            connection.close()
        preliminary = EffectAdoptionRequest(
            "adoption-1", "adoption-command-1", "adoption-event-1",
            "repo-1", "run-2", "item-2", "plan-2", "revision-2",
            "effect-1", descriptor, 1, "run-1", "attempt-1",
            "observation-1", root_observation.event_hash,
            root_row["observation_digest"], root_finalization.finalization_id,
            root_finalization.finalization_key, root_finalization.event_hash,
            OperationOriginKind.EXECUTION_INTENT, "attempt-1", intent_hash,
            root_finalization.finalization_key, adopted_plan.event_hash,
            adopted_plan.event_hash, "placeholder-vector",
            LifecycleState.PLANNED, None, "adoption-readiness-1",
            "adoption-grant-1",
            self.store.adoption_check_set_digest(("check-2",)),
            "synthetic-adoption-source", "1", "adoption-terms-1",
            "adoption-scope-1",
        )
        adoption_key = self.store.adoption_key(preliminary)
        for rebound in (
            replace(
                preliminary,
                root_observation_event_hash="changed-root-observation-event",
            ),
            replace(
                preliminary,
                root_finalization_event_hash="changed-root-finalization-event",
            ),
            replace(
                preliminary,
                immediate_origin_kind=OperationOriginKind.EFFECT_ADOPTION,
                immediate_origin_id="different-immediate-adoption",
                immediate_origin_event_hash="different-immediate-event",
                immediate_finalization_key="different-immediate-finalization",
            ),
            replace(
                preliminary,
                current_check_set_digest=self.store.adoption_check_set_digest(
                    ("check-2", "check-3")
                ),
            ),
            replace(preliminary, adoption_source_id="changed-source"),
            replace(preliminary, adoption_source_version="2"),
            replace(preliminary, adoption_terms_digest="changed-terms"),
            replace(preliminary, adoption_scope_digest="changed-scope"),
        ):
            self.assertNotEqual(self.store.adoption_key(rebound), adoption_key)
        binding_digest = self.store.adoption_binding_digest(preliminary)
        grant = self.authority.issue_source_grant(
            grant_id="adoption-grant-1",
            grant_kind=SyntheticGrantKind.ADOPTION,
            action="ADOPT_VERIFIED_EFFECT",
            repository_id="repo-1",
            logical_effect_id="effect-1",
            source_id="synthetic-adoption-source",
            source_version="1",
            terms_digest="adoption-terms-1",
            scope_digest="adoption-scope-1",
            binding_digest=binding_digest,
            not_before="2026-09-20T00:00:00.000000Z",
            expires_at="2026-09-22T00:00:00.000000Z",
            use_limit=1,
        )
        registered = self.store.register_synthetic_source_grant(
            grant, self.authority
        )
        self.oracle.allowed_head = registered.event_hash
        catalog_head, heads = self.store.load_verified("repo-1")
        request = replace(
            preliminary,
            expected_catalog_head=catalog_head,
            expected_run_head=heads["run-2"],
            expected_head_vector_digest=(
                self.store._complete_head_vector_digest(heads)
            ),
        )
        request_digest = self.store._event_hash(
            {
                **request.__dict__,
                "immediate_origin_kind": request.immediate_origin_kind.value,
                "expected_lifecycle": request.expected_lifecycle.value,
            }
        )
        semantic_input_digest = self.store._event_hash(
            {
                "domain": "AEGIS:EFFECT_SEMANTIC_INPUTS:v1",
                "semantic_inputs": [list(item) for item in semantic_inputs],
            }
        )
        readiness = self.authority.issue_adoption_readiness_evidence(
            evidence_id="adoption-readiness-1",
            source_id="synthetic-adoption-source",
            source_version="1",
            repository_id="repo-1", run_id="run-2", item_id="item-2",
            plan_id="plan-2", revision_digest="revision-2",
            source_tree_digest="source-tree-1",
            item_definition_digest="item-definition-1",
            semantic_input_digest=semantic_input_digest,
            prerequisites_met=True, catalog_head=catalog_head,
            head_vector_digest=request.expected_head_vector_digest,
            evidence_head=heads["run-2"],
            observed_at="2026-09-21T00:00:00.000000Z",
            request_digest=request_digest,
        )
        capability = self.authority.issue_source_capability(
            grant,
            consumer_kind=SyntheticSourceConsumerKind.EFFECT_ADOPTION,
            consumer_key=self.store.adoption_key(request),
            binding_digest=binding_digest,
        )
        connection = sqlite3.connect(self.database_path)
        try:
            before_stale_adoption = tuple(connection.iterdump())
        finally:
            connection.close()
        self.oracle.allowed_head = "stale-before-adoption"
        with self.assertRaisesRegex(DispatchDenied, "freshness"):
            self.store.adopt_verified_effect(
                request, readiness, capability, self.authority
            )
        connection = sqlite3.connect(self.database_path)
        try:
            after_stale_adoption = tuple(connection.iterdump())
        finally:
            connection.close()
        self.assertEqual(after_stale_adoption, before_stale_adoption)
        self.oracle.allowed_head = registered.event_hash
        spent_path = Path(self.temporary_directory.name) / "spent-adoption.sqlite3"
        shutil.copy2(self.database_path, spent_path)
        spent_oracle = MutableFreshnessOracle()
        spent_oracle.allowed_head = registered.event_hash
        spent_store = SQLiteStateStore(
            spent_path, spent_oracle, "repo-1",
            utc_now=lambda: datetime(2026, 9, 21, tzinfo=timezone.utc),
        )
        spent_store._bind_classification_authority(self.authority)
        manual_capability = self.authority.issue_source_capability(
            grant, consumer_kind=SyntheticSourceConsumerKind.MANUAL,
            consumer_key="manual-spend-before-adoption",
            binding_digest=binding_digest,
        )
        manual_use = spent_store.consume_synthetic_source_for_test(
            manual_capability, self.authority
        )
        spent_oracle.allowed_head = manual_use.event_hash
        spent_catalog, spent_heads = spent_store.load_verified("repo-1")
        spent_request = replace(
            request,
            expected_catalog_head=spent_catalog,
            expected_run_head=spent_heads["run-2"],
            expected_head_vector_digest=(
                spent_store._complete_head_vector_digest(spent_heads)
            ),
        )
        spent_request_digest = spent_store._event_hash(
            {
                **spent_request.__dict__,
                "immediate_origin_kind": (
                    spent_request.immediate_origin_kind.value
                ),
                "expected_lifecycle": spent_request.expected_lifecycle.value,
            }
        )
        spent_readiness = self.authority.issue_adoption_readiness_evidence(
            evidence_id="adoption-readiness-1",
            source_id="synthetic-adoption-source", source_version="1",
            repository_id="repo-1", run_id="run-2", item_id="item-2",
            plan_id="plan-2", revision_digest="revision-2",
            source_tree_digest="source-tree-1",
            item_definition_digest="item-definition-1",
            semantic_input_digest=semantic_input_digest,
            prerequisites_met=True, catalog_head=spent_catalog,
            head_vector_digest=spent_request.expected_head_vector_digest,
            evidence_head=spent_heads["run-2"],
            observed_at="2026-09-21T00:00:00.000000Z",
            request_digest=spent_request_digest,
        )
        spent_capability = self.authority.issue_source_capability(
            grant,
            consumer_kind=SyntheticSourceConsumerKind.EFFECT_ADOPTION,
            consumer_key=spent_store.adoption_key(spent_request),
            binding_digest=binding_digest,
        )
        with self.assertRaisesRegex(DispatchDenied, "use limit"):
            spent_store.adopt_verified_effect(
                spent_request, spent_readiness, spent_capability,
                self.authority,
            )
        connection = sqlite3.connect(spent_path)
        try:
            self.assertEqual(
                connection.execute(
                    "SELECT COUNT(*) FROM synthetic_authority_uses WHERE "
                    "grant_id = 'adoption-grant-1'"
                ).fetchone()[0],
                1,
            )
        finally:
            connection.close()
        occupied_path = (
            Path(self.temporary_directory.name) / "occupied-adoption.sqlite3"
        )
        shutil.copy2(self.database_path, occupied_path)
        occupied_oracle = MutableFreshnessOracle()
        occupied_oracle.allowed_head = registered.event_hash
        occupied_store = SQLiteStateStore(
            occupied_path, occupied_oracle, "repo-1",
            utc_now=lambda: datetime(2026, 9, 21, tzinfo=timezone.utc),
        )
        occupied_store._bind_classification_authority(self.authority)
        occupied_plan = occupied_store.accept_plan(
            PlanAcceptanceRequest(
                "occupied-plan", "occupied-plan-command",
                "occupied-plan-event", "repo-1", "occupied-run",
                "occupied-item", "occupied-effect", "occupied-revision",
                "occupied-descriptor", "occupied-scope", "occupied-budget",
                ("occupied-check",), (),
            ),
            expected_head=registered.event_hash, writer_epoch=101,
        )
        occupied_oracle.allowed_head = occupied_plan.event_hash
        occupied_grant = SyntheticGrant(
            "occupied-operation-grant", "repo-1", "occupied-effect",
            "occupied-attempt", "occupied-scope",
        )
        self.authority.register(occupied_grant)
        occupied_capability = self.authority.claim(
            *occupied_grant.__dict__.values()
        )
        occupied_intent = occupied_store.commit_intent(
            IntentRequest(
                "repo-1", "occupied-run", "occupied-item",
                "occupied-intent-command", "occupied-intent-event",
                "occupied-effect", "occupied-descriptor", "occupied-attempt",
                "occupied-permission", "occupied-reservation",
                "occupied-budget", 1, 2, 100,
            ),
            occupied_capability, self.authority,
            expected_head=occupied_plan.event_hash, writer_epoch=102,
        )
        occupied_oracle.allowed_head = occupied_intent.event_hash
        occupied_catalog, occupied_heads = occupied_store.load_verified(
            "repo-1", authority=self.authority
        )
        occupied_request = replace(
            request,
            expected_catalog_head=occupied_catalog,
            expected_run_head=occupied_heads["run-2"],
            expected_head_vector_digest=(
                occupied_store._complete_head_vector_digest(occupied_heads)
            ),
        )
        occupied_request_digest = occupied_store._event_hash(
            {
                **occupied_request.__dict__,
                "immediate_origin_kind": (
                    occupied_request.immediate_origin_kind.value
                ),
                "expected_lifecycle": (
                    occupied_request.expected_lifecycle.value
                ),
            }
        )
        occupied_readiness = self.authority.issue_adoption_readiness_evidence(
            evidence_id="adoption-readiness-1",
            source_id="synthetic-adoption-source", source_version="1",
            repository_id="repo-1", run_id="run-2", item_id="item-2",
            plan_id="plan-2", revision_digest="revision-2",
            source_tree_digest="source-tree-1",
            item_definition_digest="item-definition-1",
            semantic_input_digest=semantic_input_digest,
            prerequisites_met=True, catalog_head=occupied_catalog,
            head_vector_digest=occupied_request.expected_head_vector_digest,
            evidence_head=occupied_heads["run-2"],
            observed_at="2026-09-21T00:00:00.000000Z",
            request_digest=occupied_request_digest,
        )
        with self.assertRaisesRegex(DispatchDenied, "slot to be free"):
            occupied_store.adopt_verified_effect(
                occupied_request, occupied_readiness, capability,
                self.authority,
            )
        stale_readiness = self.authority.issue_adoption_readiness_evidence(
            **{
                key: value
                for key, value in readiness.__dict__.items()
                if key not in {"issuer_fingerprint", "issuer_mac"}
            }
            | {"semantic_input_digest": "changed-input-digest"}
        )
        with self.assertRaisesRegex(DispatchDenied, "accepted inputs"):
            self.store.adopt_verified_effect(
                request, stale_readiness, capability, self.authority
            )
        with self.assertRaises(InjectedFailure):
            self.store.adopt_verified_effect(
                request, readiness, capability, self.authority,
                failure_hook=raise_at("after_adoption_writes_before_commit"),
            )
        connection = sqlite3.connect(self.database_path)
        try:
            self.assertEqual(
                connection.execute(
                    "SELECT COUNT(*) FROM effect_adoptions"
                ).fetchone()[0],
                0,
            )
        finally:
            connection.close()
        with self.assertRaises(InjectedFailure):
            self.store.adopt_verified_effect(
                request, readiness, capability, self.authority,
                failure_hook=raise_at(
                    "after_adoption_commit_before_acknowledgement"
                ),
            )
        connection = sqlite3.connect(self.database_path)
        try:
            committed_adoption_hash = connection.execute(
                "SELECT event_hash FROM effect_adoptions WHERE adoption_id = "
                "'adoption-1'"
            ).fetchone()[0]
        finally:
            connection.close()
        self.oracle.allowed_head = committed_adoption_hash
        receipt = self.store.adopt_verified_effect(
            request, readiness, capability, self.authority
        )
        self.assertEqual(receipt.resulting_state, LifecycleState.VALIDATING)
        self.assertTrue(receipt.replayed)
        replay = self.store.adopt_verified_effect(
            request, readiness, capability, self.authority
        )
        self.assertTrue(replay.replayed)
        rebound_grant = self.authority.issue_source_grant(
            **{
                key: value
                for key, value in grant.__dict__.items()
                if key not in {"issuer_fingerprint", "issuer_mac"}
            }
            | {"source_version": "2"}
        )
        rebound_capability = self.authority.issue_source_capability(
            rebound_grant,
            consumer_kind=SyntheticSourceConsumerKind.EFFECT_ADOPTION,
            consumer_key=self.store.adoption_key(request),
            binding_digest=binding_digest,
        )
        with self.assertRaisesRegex(
            DispatchDenied, "does not bind the exact adoption"
        ):
            self.store.adopt_verified_effect(
                request, readiness, rebound_capability, self.authority
            )
        contrary_path = (
            Path(self.temporary_directory.name) / "contrary-adoption.sqlite3"
        )
        shutil.copy2(self.database_path, contrary_path)
        contrary_oracle = MutableFreshnessOracle()
        contrary_oracle.allowed_head = receipt.event_hash
        contrary_store = SQLiteStateStore(
            contrary_path, contrary_oracle, "repo-1",
            utc_now=lambda: datetime(2026, 9, 21, tzinfo=timezone.utc),
        )
        contrary_store._bind_classification_authority(self.authority)
        contrary_settlement_request = BudgetSettlementRequest(
            "contrary-settlement", "reservation-1",
            settlement.settlement_hash, BudgetDisposition.ADJUSTED, 2,
            "contrary-receipt", "LATE_USAGE_CONFIRMED",
        )
        contrary_settlement = contrary_store._settle_budget(
            contrary_settlement_request,
            self.authority.issue_settlement_proof(
                "contrary-settlement-proof", contrary_settlement_request
            ),
            self.authority,
        )
        contrary_oracle.allowed_head = contrary_settlement.settlement_hash
        contrary = self._record_signed_effect_observation(
            EffectObservationRequest(
                "contrary-observation", "contrary-command", "contrary-event",
                "repo-1", "run-1", "item-1", "effect-1", "attempt-1",
                "contrary-receipt", self.capability.claim_id, descriptor, 2,
                "contrary-settlement", contrary_settlement.settlement_hash,
            ),
            store=contrary_store,
        )
        connection = sqlite3.connect(contrary_path)
        try:
            contrary_oracle.allowed_head = connection.execute(
                "SELECT catalog_head FROM repositories WHERE repository_id = "
                "'repo-1'"
            ).fetchone()[0]
        finally:
            connection.close()
        self.assertEqual(
            contrary_store.load_run_lifecycle("run-2"),
            LifecycleState.RECONCILIATION_REQUIRED,
        )
        contrary_store.load_verified("repo-1", authority=self.authority)
        connection = contrary_store._connect()
        try:
            contrary_head = connection.execute(
                "SELECT catalog_head FROM repositories WHERE repository_id = "
                "'repo-1'"
            ).fetchone()[0]
            next_epoch = int(connection.execute(
                "SELECT MAX(writer_epoch) + 1 FROM events"
            ).fetchone()[0])
        finally:
            connection.close()
        collision_fact = AuthorityLifecycleFactRequest(
            "contrary-observation", "collision-fact-command",
            "collision-fact-event", "repo-1", "run-2", "item-2",
            "effect-1", "EFFECT", "grant-1", "EXECUTE_EFFECT", "scope-1",
            AuthorityFactKind.REVOKED, GovernedOrder.BEFORE, "NO_ACTION",
            None, None,
        )
        collision_denial = contrary_store.record_authority_fact(
            collision_fact,
            self.authority.issue_authority_lifecycle_evidence(
                "collision-fact-proof", collision_fact
            ),
            self.authority,
            expected_head=contrary_head, writer_epoch=next_epoch,
        )
        contrary_oracle.allowed_head = collision_denial.event_hash
        collision_correction = AuthorityLifecycleFactRequest(
            "collision-correction", "collision-correction-command",
            "collision-correction-event", "repo-1", "run-2", "item-2",
            "effect-1", "EFFECT", "grant-1", "EXECUTE_EFFECT", "scope-1",
            AuthorityFactKind.CORRECTION, GovernedOrder.BEFORE, "NO_ACTION",
            None, None, corrected_fact_id=collision_fact.fact_id,
            corrected_event_hash=collision_denial.event_hash,
        )
        collision_corrected = contrary_store.record_authority_fact(
            collision_correction,
            self.authority.issue_authority_lifecycle_evidence(
                "collision-correction-proof", collision_correction
            ),
            self.authority,
            expected_head=collision_denial.event_hash,
            writer_epoch=next_epoch + 1,
        )
        contrary_oracle.allowed_head = collision_corrected.event_hash
        connection = contrary_store._connect()
        try:
            contrary_fences = connection.execute(
                "SELECT COUNT(*) FROM dispatch_fences WHERE reason_code = "
                "'DEPENDENT_ADOPTION_CONTRARY_RECEIPT'"
            ).fetchone()[0]
            contrary_dependencies = connection.execute(
                "SELECT COUNT(*) FROM dependent_adoption_fences WHERE "
                "correction_owner_id = 'contrary-observation'"
            ).fetchone()[0]
        finally:
            connection.close()
        self.assertEqual((contrary_fences, contrary_dependencies), (1, 1))
        self.assertEqual(
            contrary_store.load_run_lifecycle("run-2"),
            LifecycleState.RECONCILIATION_REQUIRED,
        )
        contrary_store.load_verified("repo-1", authority=self.authority)
        connection = sqlite3.connect(self.database_path)
        try:
            self.assertEqual(
                connection.execute(
                    "SELECT COUNT(*) FROM events WHERE event_kind = "
                    "'INTENT_COMMITTED'"
                ).fetchone()[0],
                1,
            )
            self.assertEqual(
                connection.execute(
                    "SELECT COUNT(*) FROM budget_reservations"
                ).fetchone()[0],
                2,
            )
            self.assertEqual(
                connection.execute(
                    "SELECT COUNT(*) FROM synthetic_authority_uses WHERE "
                    "consumer_kind = 'EFFECT_ADOPTION'"
                ).fetchone()[0],
                1,
            )
        finally:
            connection.close()
        self.store.load_verified("repo-1")
        connection = sqlite3.connect(self.database_path)
        try:
            source_use = connection.execute(
                "SELECT source_event_id, event_hash, recorded_at FROM "
                "synthetic_authority_uses WHERE grant_id = ?",
                ("adoption-grant-1",),
            ).fetchone()
        finally:
            connection.close()
        advancing_times = iter(
            datetime(2026, 9, 21, 1, 0, second, tzinfo=timezone.utc)
            for second in range(10)
        )
        self.store._utc_now = lambda: next(advancing_times)
        expiry_fact = AuthorityLifecycleFactRequest(
            "adoption-expiry-1", "adoption-expiry-command-1",
            "adoption-expiry-event-1", "repo-1", "run-2", "item-2",
            "effect-1", "ADOPTION", "adoption-grant-1",
            "ADOPT_VERIFIED_EFFECT", "adoption-scope-1",
            AuthorityFactKind.EXPIRED, GovernedOrder.AFTER, "SOURCE_USE",
            source_use[0], source_use[1],
            recorded_at_utc=None,
            effective_at_utc="2026-09-21T00:30:00.000000Z",
        )
        expiry = self.store.record_authority_fact(
            expiry_fact,
            self.authority.issue_authority_lifecycle_evidence(
                "adoption-expiry-proof-1", expiry_fact
            ),
            self.authority,
            expected_head=receipt.event_hash,
            writer_epoch=102,
        )
        self.assertEqual(expiry.resulting_state, LifecycleState.VALIDATING)
        self.oracle.allowed_head = expiry.event_hash
        self.store.load_verified("repo-1", authority=self.authority)
        connection = sqlite3.connect(self.database_path)
        try:
            persisted_recorded_at = connection.execute(
                "SELECT recorded_at FROM synthetic_authority_lifecycle_facts "
                "WHERE fact_id = 'adoption-expiry-1'"
            ).fetchone()[0]
        finally:
            connection.close()
        self.assertEqual(
            persisted_recorded_at, "2026-09-21T01:00:00.000000Z"
        )
        adopted_containment_json, adopted_containment_digest = (
            validator_containment("input-2", "adopted")
        )
        validator_grant = SyntheticValidatorGrant(
            "validator-grant-adopted", "repo-1", "effect-1", "revision-2",
            "check-2", "input-2", "validator-attempt-adopted",
            "read-only-scope-adopted", adopted_containment_digest,
        )
        self.authority.register_validator(validator_grant)
        validator_capability = self.authority.claim_validator(
            *validator_grant.__dict__.values()
        )
        validator_intent = self.store.commit_validator_intent(
            ValidatorIntentRequest(
                "validator-intent-adopted", "validator-command-adopted",
                "validator-event-adopted", "repo-1", "run-2", "item-2",
                "effect-1", receipt.slot_attempt_id, "observation-1",
                root_observation.event_hash, "revision-2", "check-2",
                "input-2", "validator-attempt-adopted",
                "validator-permission-adopted", "validator-reservation-adopted",
                "validator-budget-policy-adopted", 1, 2, 10, None,
                adopted_containment_json,
            ),
            validator_capability,
            self.authority,
        )
        self.oracle.allowed_head = validator_intent.event_hash
        self.store.load_verified("repo-1")
        stop_grant = SyntheticOperatorGrant(
            "stop-grant-adopted", "repo-1", "run-2", "STOP_IMMEDIATE",
            "stop-scope-adopted",
        )
        self.authority.register_operator(stop_grant)
        stop_capability = self.authority.claim_operator(
            *stop_grant.__dict__.values()
        )
        stopped = self.store.stop(
            StopRequest(
                "stop-adopted", "stop-command-adopted",
                "stop-event-adopted", "repo-1", "run-2",
                StopMode.IMMEDIATE, "OPERATOR_STOP",
            ),
            stop_capability,
            self.authority,
        )
        self.oracle.allowed_head = stopped.event_hash
        validator_path = (
            Path(self.temporary_directory.name) / "adopted-validator.sqlite3"
        )
        adapter = SyntheticValidatorAdapter(validator_path)
        adapter._canonical_repository_id = "repo-1"
        adapter._canonical_ledger_path = validator_path.resolve()
        nonexecution_attestation = self.authority.issue_nonexecution_attestation(
            "adopted-nonexecution-attestation", "adopted-nonexecution-seal",
            "VALIDATOR", adapter._target_digest("repo-1"),
            validator_capability.claim_id,
            "VALIDATOR:validator-intent-adopted", validator_intent.event_hash,
            "validator-reservation-adopted", "repo-1", "run-2", "item-2",
            "effect-1", "validator-attempt-adopted",
        )
        seal = adapter.seal_nonexecution(
            nonexecution_attestation, self.authority
        )
        nonexecution_request = BudgetSettlementRequest(
            "adopted-nonexecution", "validator-reservation-adopted", "",
            BudgetDisposition.RELEASED, None,
            "adopted-nonexecution-evidence", "NONDISPATCH_PROVEN",
            non_dispatch_proven=True, zero_liability_proven=True,
            all_obligations_settled=True, run_id="run-2", item_id="item-2",
            attempt_id="validator-attempt-adopted",
        )
        nonexecution = self.store._settle_budget(
            nonexecution_request,
            self.authority.issue_settlement_proof(
                "adopted-nonexecution-proof", nonexecution_request
            ),
            self.authority,
        )
        self.oracle.allowed_head = nonexecution.settlement_hash
        terminal = self.store.settle_terminal_validation(
            TerminalValidationSettlementRequest(
                "adopted-terminal-settlement", "adopted-terminal-command",
                "adopted-terminal-event", "repo-1", "run-2", "item-2",
                "effect-1", "plan-2", "revision-2", "check-2",
                "NONDISPATCH_PROVEN", "adopted-nonexecution",
                nonexecution.settlement_hash, "CANCELLED_WITHOUT_START",
                "validator-intent-adopted", "validator-attempt-adopted",
            )
        )
        self.oracle.allowed_head = terminal.event_hash
        self.assertTrue(terminal.slot_released)
        self.assertEqual(self.store.table_counts()["outstanding_slot"], 0)
        self.store.load_verified("repo-1", authority=self.authority)
        reopened = SQLiteStateStore(
            self.database_path, self.oracle, "repo-1",
            utc_now=lambda: datetime(2026, 9, 21, 1, tzinfo=timezone.utc),
        )
        reopened._bind_classification_authority(self.authority)
        reopened.load_verified("repo-1", authority=self.authority)

    def test_t28_source_recovery_rejects_historically_ineffective_uses(
        self,
    ) -> None:
        def make_store(name: str) -> tuple[SQLiteStateStore, MutableFreshnessOracle]:
            oracle = MutableFreshnessOracle()
            path = Path(self.temporary_directory.name) / f"{name}.sqlite3"
            store = SQLiteStateStore(
                path, oracle, "repo-1",
                utc_now=lambda: datetime(2026, 9, 21, tzinfo=timezone.utc),
            )
            store._bind_classification_authority(self.authority)
            return store, oracle

        def issue_grant(
            name: str, *, not_before: str, expires_at: str, use_limit: int = 1,
        ) -> SyntheticSourceGrant:
            return self.authority.issue_source_grant(
                grant_id=f"{name}-grant",
                grant_kind=SyntheticGrantKind.ADOPTION,
                action="ADOPT_VERIFIED_EFFECT", repository_id="repo-1",
                logical_effect_id="effect-1", source_id=f"{name}-source",
                source_version="1", terms_digest=f"{name}-terms",
                scope_digest=f"{name}-scope",
                binding_digest=f"{name}-binding",
                not_before=not_before, expires_at=expires_at,
                use_limit=use_limit,
            )

        def capability(grant: SyntheticSourceGrant, consumer: str):
            return self.authority.issue_source_capability(
                grant,
                consumer_kind=SyntheticSourceConsumerKind.MANUAL,
                consumer_key=consumer,
                binding_digest=grant.binding_digest,
            )

        for name, column, effective_value, temporary_value in (
            (
                "not-yet-effective", "not_before",
                "2026-09-22T00:00:00.000000Z",
                "2026-09-20T00:00:00.000000Z",
            ),
            (
                "already-expired", "expires_at",
                "2026-09-20T00:00:00.000000Z",
                "2026-09-22T00:00:00.000000Z",
            ),
        ):
            with self.subTest(name=name):
                store, _oracle = make_store(name)
                grant = issue_grant(
                    name,
                    not_before=(
                        effective_value if column == "not_before"
                        else "2026-09-19T00:00:00.000000Z"
                    ),
                    expires_at=(
                        effective_value if column == "expires_at"
                        else "2026-09-23T00:00:00.000000Z"
                    ),
                )
                store.register_synthetic_source_grant(grant, self.authority)
                connection = store._connect()
                try:
                    connection.execute("BEGIN IMMEDIATE")
                    connection.execute(
                        f"UPDATE synthetic_authority_grants SET {column} = ? "
                        "WHERE grant_id = ?",
                        (temporary_value, grant.grant_id),
                    )
                    store._consume_synthetic_source(
                        connection, capability(grant, f"{name}-consumer"),
                        self.authority,
                        recorded_at="2026-09-21T00:00:00.000000Z",
                        expected_consumer_kind=(
                            SyntheticSourceConsumerKind.MANUAL
                        ),
                    )
                    connection.execute(
                        f"UPDATE synthetic_authority_grants SET {column} = ? "
                        "WHERE grant_id = ?",
                        (effective_value, grant.grant_id),
                    )
                    connection.commit()
                finally:
                    connection.close()
                with self.assertRaisesRegex(
                    StorageIntegrityError, "source projection is invalid"
                ):
                    store.load_verified("repo-1", authority=self.authority)

        store, _oracle = make_store("use-limit")
        grant = issue_grant(
            "use-limit", not_before="2026-09-20T00:00:00.000000Z",
            expires_at="2026-09-22T00:00:00.000000Z", use_limit=1,
        )
        store.register_synthetic_source_grant(grant, self.authority)
        connection = store._connect()
        try:
            connection.execute("BEGIN IMMEDIATE")
            connection.execute(
                "UPDATE synthetic_authority_grants SET use_limit = 2 WHERE "
                "grant_id = ?", (grant.grant_id,),
            )
            for index in (1, 2):
                store._consume_synthetic_source(
                    connection,
                    capability(grant, f"use-limit-consumer-{index}"),
                    self.authority,
                    recorded_at=f"2026-09-21T00:00:0{index}.000000Z",
                    expected_consumer_kind=SyntheticSourceConsumerKind.MANUAL,
                )
            connection.execute(
                "UPDATE synthetic_authority_grants SET use_limit = 1 WHERE "
                "grant_id = ?", (grant.grant_id,),
            )
            connection.commit()
        finally:
            connection.close()
        with self.assertRaisesRegex(
            StorageIntegrityError, "source projection is invalid"
        ):
            store.load_verified("repo-1", authority=self.authority)

        store, _oracle = make_store("revoked-before-use")
        grant = issue_grant(
            "revoked-before-use",
            not_before="2026-09-20T00:00:00.000000Z",
            expires_at="2026-09-22T00:00:00.000000Z",
        )
        store.register_synthetic_source_grant(grant, self.authority)
        lifecycle = AuthorityLifecycleFactRequest(
            "revoked-source-fact", "revoked-source-command",
            "revoked-source-event", "repo-1", "synthetic-run",
            "synthetic-item", "effect-1", "ADOPTION", grant.grant_id,
            grant.action, grant.scope_digest, AuthorityFactKind.REVOKED,
            GovernedOrder.BEFORE, "NO_ACTION", None, None,
            effective_at_utc="2026-09-20T00:00:00.000000Z",
        )
        evidence = self.authority.issue_authority_lifecycle_evidence(
            "revoked-source-proof", lifecycle
        )
        connection = store._connect()
        try:
            connection.execute("BEGIN IMMEDIATE")
            source_recorded_at = "2026-09-21T00:00:01.000000Z"
            payload = {
                **lifecycle.__dict__,
                "fact_kind": lifecycle.fact_kind.value,
                "governed_order": lifecycle.governed_order.value,
            }
            source_event_id = "source-authority-fact:revoked-source-fact"
            _sequence, event_hash, body_json = store._append_source_event(
                connection, source_event_id=source_event_id,
                repository_id="repo-1",
                event_kind="SYNTHETIC_AUTHORITY_LIFECYCLE_RECORDED",
                recorded_at=source_recorded_at,
                effective_at=lifecycle.effective_at_utc,
                event_fields=payload | {
                    "source_recorded_at_utc": source_recorded_at,
                    "issuer_fingerprint": self.authority.issuer_fingerprint,
                    "issuer_mac": evidence.issuer_mac,
                    "proof_id": evidence.proof_id,
                    "proof_digest": evidence.request_digest,
                },
            )
            connection.execute(
                "INSERT INTO synthetic_authority_lifecycle_facts VALUES ("
                + ", ".join("?" for _ in range(20)) + ")",
                (
                    lifecycle.fact_id, lifecycle.repository_id,
                    lifecycle.grant_kind, lifecycle.grant_id,
                    lifecycle.logical_effect_id, lifecycle.action,
                    lifecycle.scope_digest, lifecycle.fact_kind.value,
                    lifecycle.governed_order.value,
                    lifecycle.governed_event_id,
                    lifecycle.governed_event_hash, source_recorded_at,
                    lifecycle.effective_at_utc, lifecycle.corrected_fact_id,
                    lifecycle.successor_grant_id,
                    self.authority.issuer_fingerprint, evidence.issuer_mac,
                    source_event_id, event_hash, body_json,
                ),
            )
            store._consume_synthetic_source(
                connection, capability(grant, "revoked-consumer"),
                self.authority,
                recorded_at="2026-09-21T00:00:02.000000Z",
                expected_consumer_kind=SyntheticSourceConsumerKind.MANUAL,
            )
            connection.commit()
        finally:
            connection.close()
        with self.assertRaisesRegex(
            StorageIntegrityError, "source projection is invalid"
        ):
            store.load_verified("repo-1", authority=self.authority)

    def test_f01_canonical_identity_and_approved_relationship_are_durable(
        self,
    ) -> None:
        semantic_inputs = (("input", "digest-1"),)
        descriptor = self.store.canonical_effect_descriptor_digest(
            "WRITE", "synthetic-target-1", semantic_inputs, 1
        )
        root = self.store.accept_plan(
            PlanAcceptanceRequest(
                "identity-plan-1", "identity-command-1", "identity-event-1",
                "repo-1", "identity-run-1", "identity-item-1", "effect-1",
                "identity-revision-1", descriptor, "scope-1", "budget-1",
                ("check-1",), (), effect_action="WRITE",
                effect_target="synthetic-target-1",
                effect_semantic_inputs=semantic_inputs, target_generation=1,
            ),
            expected_head="", writer_epoch=1,
        )
        self.oracle.allowed_head = root.event_hash
        changed_inputs = (("input", "digest-2"),)
        changed_descriptor = self.store.canonical_effect_descriptor_digest(
            "WRITE", "synthetic-target-1", changed_inputs, 1
        )
        with self.assertRaisesRegex(DispatchDenied, "predecessor relationship"):
            self.store.accept_plan(
                PlanAcceptanceRequest(
                    "unrelated-plan", "unrelated-command", "unrelated-event",
                    "repo-1", "unrelated-run", "unrelated-item",
                    "unrelated-effect", "unrelated-revision",
                    changed_descriptor, "unrelated-scope", "unrelated-budget",
                    ("unrelated-check",), (), effect_action="WRITE",
                    effect_target="synthetic-target-1",
                    effect_semantic_inputs=changed_inputs,
                    target_generation=1,
                ),
                expected_head=root.event_hash, writer_epoch=2,
            )
        with self.assertRaisesRegex(DispatchDenied, "retain.*canonical semantics"):
            self.store.accept_plan(
                PlanAcceptanceRequest(
                    "bad-repeat-plan", "bad-repeat-command",
                    "bad-repeat-event", "repo-1", "bad-repeat-run",
                    "bad-repeat-item", "bad-repeat-effect",
                    "bad-repeat-revision", changed_descriptor,
                    "bad-repeat-scope", "bad-repeat-budget",
                    ("bad-repeat-check",), (), effect_action="WRITE",
                    effect_target="synthetic-target-1",
                    effect_semantic_inputs=changed_inputs,
                    target_generation=1,
                    relationship_kind=EffectRelationshipKind.REPEAT_OF,
                    predecessor_logical_effect_id="effect-1",
                    relationship_grant_id="bad-repeat-grant",
                    predecessor_descriptor_digest=descriptor,
                    predecessor_defining_plan_id="identity-plan-1",
                    predecessor_defining_event_hash=root.event_hash,
                    relationship_source_id="bad-repeat-source",
                    relationship_source_version="1",
                    relationship_terms_digest="bad-repeat-terms",
                    relationship_scope_digest="bad-repeat-source-scope",
                ),
                expected_head=root.event_hash, writer_epoch=2,
            )
        for relationship_kind in (
            EffectRelationshipKind.DIFFERENT_FROM,
            EffectRelationshipKind.COMPENSATES,
        ):
            with self.subTest(relationship_kind=relationship_kind.value):
                with self.assertRaisesRegex(
                    DispatchDenied, "different canonical semantics"
                ):
                    self.store.accept_plan(
                        PlanAcceptanceRequest(
                            f"bad-{relationship_kind.value}-plan",
                            f"bad-{relationship_kind.value}-command",
                            f"bad-{relationship_kind.value}-event",
                            "repo-1", f"bad-{relationship_kind.value}-run",
                            f"bad-{relationship_kind.value}-item",
                            f"bad-{relationship_kind.value}-effect",
                            f"bad-{relationship_kind.value}-revision",
                            descriptor, f"bad-{relationship_kind.value}-scope",
                            f"bad-{relationship_kind.value}-budget",
                            (f"bad-{relationship_kind.value}-check",), (),
                            effect_action="WRITE",
                            effect_target="synthetic-target-1",
                            effect_semantic_inputs=semantic_inputs,
                            target_generation=1,
                            relationship_kind=relationship_kind,
                            predecessor_logical_effect_id="effect-1",
                            relationship_grant_id=(
                                f"bad-{relationship_kind.value}-grant"
                            ),
                            predecessor_descriptor_digest=descriptor,
                            predecessor_defining_plan_id="identity-plan-1",
                            predecessor_defining_event_hash=root.event_hash,
                            relationship_source_id="bad-source",
                            relationship_source_version="1",
                            relationship_terms_digest="bad-terms",
                            relationship_scope_digest="bad-source-scope",
                        ),
                        expected_head=root.event_hash, writer_epoch=2,
                    )
        with self.assertRaisesRegex(DispatchDenied, "predecessor relationship"):
            self.store.accept_plan(
                PlanAcceptanceRequest(
                    "alias-plan", "alias-command", "alias-event", "repo-1",
                    "alias-run", "alias-item", "alias-effect",
                    "alias-revision", descriptor, "alias-scope", "alias-budget",
                    ("alias-check",), (), effect_action="WRITE",
                    effect_target="synthetic-target-1",
                    effect_semantic_inputs=semantic_inputs,
                    target_generation=1,
                ),
                expected_head=root.event_hash, writer_epoch=2,
            )
        repeat = PlanAcceptanceRequest(
            "repeat-plan", "repeat-command", "repeat-event", "repo-1",
            "repeat-run", "repeat-item", "repeat-effect", "repeat-revision",
            descriptor, "repeat-scope", "repeat-budget", ("repeat-check",), (),
            effect_action="WRITE", effect_target="synthetic-target-1",
            effect_semantic_inputs=semantic_inputs, target_generation=1,
            relationship_kind=EffectRelationshipKind.REPEAT_OF,
            predecessor_logical_effect_id="effect-1",
            relationship_grant_id="relationship-grant-1",
            predecessor_descriptor_digest=descriptor,
            predecessor_defining_plan_id="identity-plan-1",
            predecessor_defining_event_hash=root.event_hash,
            relationship_source_id="synthetic-relationship-source",
            relationship_source_version="1",
            relationship_terms_digest="relationship-terms",
            relationship_scope_digest="relationship-scope",
        )
        binding_digest = self.store.effect_relationship_binding_digest(repeat)
        relationship_key = self.store.effect_relationship_key(repeat)
        self.assertNotEqual(
            self.store.effect_relationship_key(
                replace(
                    repeat,
                    predecessor_defining_event_hash="changed-predecessor-history",
                )
            ),
            relationship_key,
        )
        self.assertNotEqual(
            self.store.effect_relationship_key(
                replace(repeat, relationship_terms_digest="changed-terms")
            ),
            relationship_key,
        )
        grant = self.authority.issue_source_grant(
            grant_id="relationship-grant-1",
            grant_kind=SyntheticGrantKind.EFFECT_RELATIONSHIP,
            action="DEFINE_EFFECT_RELATIONSHIP", repository_id="repo-1",
            logical_effect_id="repeat-effect",
            source_id="synthetic-relationship-source", source_version="1",
            terms_digest="relationship-terms",
            scope_digest="relationship-scope",
            binding_digest=binding_digest,
            not_before="2026-09-20T00:00:00.000000Z",
            expires_at="2026-09-22T00:00:00.000000Z", use_limit=1,
        )
        registered = self.store.register_synthetic_source_grant(
            grant, self.authority
        )
        self.oracle.allowed_head = registered.event_hash
        capability = self.authority.issue_source_capability(
            grant,
            consumer_kind=SyntheticSourceConsumerKind.EFFECT_RELATIONSHIP,
            consumer_key=self.store.effect_relationship_key(repeat),
            binding_digest=binding_digest,
        )
        accepted = self.store.accept_plan(
            repeat, expected_head=registered.event_hash, writer_epoch=3,
            relationship_capability=capability,
        )
        self.oracle.allowed_head = "deliberately-stale-freshness-head"
        replay = self.store.accept_plan(
            repeat, expected_head="also-deliberately-stale", writer_epoch=99,
            relationship_capability=capability,
        )
        self.assertTrue(replay.replayed)
        self.assertEqual(replay.event_hash, accepted.event_hash)
        with self.assertRaisesRegex(
            DispatchDenied, "capability was not issued here|authority is rebound"
        ):
            self.store.accept_plan(
                repeat, expected_head="ignored-on-replay", writer_epoch=100,
                relationship_capability=replace(
                    capability, consumer_key="rebound-relationship-key"
                ),
            )
        self.oracle.allowed_head = accepted.event_hash
        self.store.load_verified("repo-1", authority=self.authority)
        connection = sqlite3.connect(self.database_path)
        try:
            relationship = connection.execute(
                "SELECT relationship_kind, predecessor_logical_effect_id "
                "FROM effect_relationships WHERE logical_effect_id = ?",
                ("repeat-effect",),
            ).fetchone()
            uses = connection.execute(
                "SELECT COUNT(*) FROM synthetic_authority_uses WHERE "
                "grant_id = ?", ("relationship-grant-1",),
            ).fetchone()[0]
        finally:
            connection.close()
        self.assertEqual(relationship, ("REPEAT_OF", "effect-1"))
        self.assertEqual(uses, 1)

    def test_f01_all_relationship_kinds_require_settled_predecessor_at_t03(
        self,
    ) -> None:
        root_inputs = (("input", "root"),)
        root_descriptor = self.store.canonical_effect_descriptor_digest(
            "WRITE", "synthetic-target", root_inputs, 1
        )
        root = self.store.accept_plan(
            PlanAcceptanceRequest(
                "relationship-root-plan", "relationship-root-command",
                "relationship-root-event", "repo-1", "relationship-root-run",
                "relationship-root-item", "relationship-root-effect",
                "relationship-root-revision", root_descriptor,
                "relationship-root-scope", "relationship-root-budget",
                ("relationship-root-check",), (), effect_action="WRITE",
                effect_target="synthetic-target",
                effect_semantic_inputs=root_inputs, target_generation=1,
            ),
            expected_head="", writer_epoch=1,
        )
        self.oracle.allowed_head = root.event_hash
        current_head = root.event_hash
        writer_epoch = 2
        for index, relationship_kind in enumerate(
            (
                EffectRelationshipKind.REPEAT_OF,
                EffectRelationshipKind.DIFFERENT_FROM,
                EffectRelationshipKind.COMPENSATES,
            ),
            start=1,
        ):
            suffix = relationship_kind.value.lower()
            semantic_inputs = (
                root_inputs
                if relationship_kind is EffectRelationshipKind.REPEAT_OF
                else (("input", f"{suffix}-{index}"),)
            )
            descriptor = self.store.canonical_effect_descriptor_digest(
                "WRITE", "synthetic-target", semantic_inputs, 1
            )
            plan_request = PlanAcceptanceRequest(
                f"{suffix}-plan", f"{suffix}-plan-command",
                f"{suffix}-plan-event", "repo-1", f"{suffix}-run",
                f"{suffix}-item", f"{suffix}-effect", f"{suffix}-revision",
                descriptor, f"{suffix}-scope", f"{suffix}-budget",
                (f"{suffix}-check",), (), effect_action="WRITE",
                effect_target="synthetic-target",
                effect_semantic_inputs=semantic_inputs, target_generation=1,
                relationship_kind=relationship_kind,
                predecessor_logical_effect_id="relationship-root-effect",
                relationship_grant_id=f"{suffix}-relationship-grant",
                predecessor_descriptor_digest=root_descriptor,
                predecessor_defining_plan_id="relationship-root-plan",
                predecessor_defining_event_hash=root.event_hash,
                relationship_source_id=f"{suffix}-relationship-source",
                relationship_source_version="1",
                relationship_terms_digest=f"{suffix}-terms",
                relationship_scope_digest=f"{suffix}-relationship-scope",
            )
            binding_digest = self.store.effect_relationship_binding_digest(
                plan_request
            )
            relationship_grant = self.authority.issue_source_grant(
                grant_id=f"{suffix}-relationship-grant",
                grant_kind=SyntheticGrantKind.EFFECT_RELATIONSHIP,
                action="DEFINE_EFFECT_RELATIONSHIP", repository_id="repo-1",
                logical_effect_id=f"{suffix}-effect",
                source_id=f"{suffix}-relationship-source",
                source_version="1", terms_digest=f"{suffix}-terms",
                scope_digest=f"{suffix}-relationship-scope",
                binding_digest=binding_digest,
                not_before="2026-09-20T00:00:00.000000Z",
                expires_at="2026-09-22T00:00:00.000000Z", use_limit=1,
            )
            registered = self.store.register_synthetic_source_grant(
                relationship_grant, self.authority
            )
            self.oracle.allowed_head = registered.event_hash
            relationship_capability = self.authority.issue_source_capability(
                relationship_grant,
                consumer_kind=(
                    SyntheticSourceConsumerKind.EFFECT_RELATIONSHIP
                ),
                consumer_key=self.store.effect_relationship_key(plan_request),
                binding_digest=binding_digest,
            )
            accepted = self.store.accept_plan(
                plan_request, expected_head=registered.event_hash,
                writer_epoch=writer_epoch,
                relationship_capability=relationship_capability,
            )
            writer_epoch += 1
            current_head = accepted.event_hash
            self.oracle.allowed_head = current_head
            operation_grant = SyntheticGrant(
                f"{suffix}-operation-grant", "repo-1", f"{suffix}-effect",
                f"{suffix}-attempt", f"{suffix}-scope",
            )
            self.authority.register(operation_grant)
            operation_capability = self.authority.claim(
                *operation_grant.__dict__.values()
            )
            with self.subTest(relationship_kind=relationship_kind.value):
                with self.assertRaisesRegex(
                    DispatchDenied, "unsettled or disputed"
                ):
                    self.store.commit_intent(
                        IntentRequest(
                            "repo-1", f"{suffix}-run", f"{suffix}-item",
                            f"{suffix}-intent-command",
                            f"{suffix}-intent-event", f"{suffix}-effect",
                            descriptor, f"{suffix}-attempt",
                            f"{suffix}-permission", f"{suffix}-reservation",
                            f"{suffix}-budget", 1, 2, 100,
                        ),
                        operation_capability, self.authority,
                        expected_head=current_head, writer_epoch=writer_epoch,
                    )
            writer_epoch += 1
        self.store.load_verified("repo-1", authority=self.authority)

    def _record_signed_effect_observation(
        self,
        request: EffectObservationRequest,
        *,
        classification: SourceControlClassification = (
            SourceControlClassification.KNOWN
        ),
        store: SQLiteStateStore | None = None,
        **kwargs,
    ):
        evidence_request = SourceControlEvidenceRequest(
            request.repository_id,
            request.run_id,
            request.item_id,
            request.logical_effect_id,
            request.attempt_id,
            request.source_claim_id,
            request.source_receipt_id,
            request.payload_digest,
            request.usage_units,
            True,
            classification,
        )
        evidence = self.authority.issue_source_control_evidence(
            f"source-control:{request.source_receipt_id}:{classification.value}",
            evidence_request,
        )
        signed = replace(
            request,
            source_control_classification=classification.value,
            source_control_evidence_id=evidence.evidence_id,
            source_control_evidence_digest=evidence.request_digest,
            source_control_issuer_fingerprint=evidence.issuer_fingerprint,
            source_control_issuer_mac=evidence.issuer_mac,
        )
        target_store = self.store if store is None else store
        return SQLiteStateStore._record_effect_observation(
            target_store, signed, authority=self.authority, **kwargs
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

    def _contact_committed_operation(
        self,
        committed,
        request: IntentRequest | None = None,
    ):
        operation_request = self.request() if request is None else request
        launch = self.store.claim_operation_launch(
            operation_request, committed
        )
        self.oracle.allowed_head = launch.event_hash
        self.store._contact_claimed_operation(
            operation_request,
            self.capability,
            committed,
            launch,
            self.store._adapter_target_digest("repo-1", "EFFECT"),
        )
        connection = sqlite3.connect(self.database_path)
        try:
            self.oracle.allowed_head = connection.execute(
                "SELECT catalog_head FROM repositories WHERE repository_id = "
                "'repo-1'"
            ).fetchone()[0]
        finally:
            connection.close()
        return launch

    def _commit_planned_intent(
        self,
        request: IntentRequest,
        capability,
        authority: SyntheticAuthority,
        *,
        expected_head: str,
        writer_epoch: int,
        failure_hook=None,
    ):
        connection = sqlite3.connect(self.database_path)
        try:
            accepted = connection.execute(
                "SELECT event_hash FROM validation_plans WHERE run_id = ?",
                (request.run_id,),
            ).fetchone()
        finally:
            connection.close()
        if accepted is None:
            plan = self.store.accept_plan(
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
                    capability.scope_digest,
                    request.budget_policy_digest,
                    ("check-1",),
                ),
                expected_head=expected_head,
                writer_epoch=writer_epoch,
            )
            self.oracle.allowed_head = plan.event_hash
            expected_head = plan.event_hash
            writer_epoch += 1
        return self.store.commit_intent(
            request,
            capability,
            authority,
            expected_head=expected_head,
            writer_epoch=writer_epoch,
            failure_hook=failure_hook,
        )

    def _assert_f06_contenders_denied_on_copy(
        self, *, label: str, expected_head: str
    ) -> None:
        path = self.database_path.parent / f"f06-boundary-{label}.sqlite3"
        shutil.copy2(self.database_path, path)
        oracle = MutableFreshnessOracle()
        oracle.allowed_head = expected_head
        branch = SQLiteStateStore(path, oracle, "repo-1")
        branch._bind_classification_authority(self.authority)
        connection = sqlite3.connect(path)
        try:
            writer_epoch = connection.execute(
                "SELECT COALESCE(MAX(writer_epoch), 0) + 1 FROM events"
            ).fetchone()[0]
        finally:
            connection.close()
        contenders = []
        for dimension, run_id, item_id in (
            ("different-item", f"f06-item-run-{label}", f"other-item-{label}"),
            ("different-run", f"f06-other-run-{label}", "item-1"),
        ):
            effect_id = f"f06-{dimension}-effect-{label}"
            attempt_id = f"f06-{dimension}-attempt-{label}"
            scope = f"f06-{dimension}-scope-{label}"
            grant = SyntheticGrant(
                f"f06-{dimension}-grant-{label}",
                "repo-1", effect_id, attempt_id, scope,
            )
            self.authority.register(grant)
            capability = self.authority.claim(*grant.__dict__.values())
            plan = branch.accept_plan(
                PlanAcceptanceRequest(
                    f"f06-{dimension}-plan-{label}",
                    f"f06-{dimension}-plan-command-{label}",
                    f"f06-{dimension}-plan-event-{label}",
                    "repo-1", run_id, item_id, effect_id,
                    f"f06-{dimension}-revision-{label}",
                    f"f06-{dimension}-descriptor-{label}", scope,
                    f"f06-{dimension}-budget-{label}",
                    (f"f06-{dimension}-check-{label}",),
                ),
                expected_head=oracle.allowed_head,
                writer_epoch=writer_epoch,
            )
            writer_epoch += 1
            oracle.allowed_head = plan.event_hash
            contenders.append(
                (
                    IntentRequest(
                        "repo-1", run_id, item_id,
                        f"f06-{dimension}-command-{label}",
                        f"f06-{dimension}-event-{label}", effect_id,
                        f"f06-{dimension}-descriptor-{label}", attempt_id,
                        f"f06-{dimension}-permission-{label}",
                        f"f06-{dimension}-reservation-{label}",
                        f"f06-{dimension}-budget-{label}", 1, 2, 100,
                    ),
                    capability,
                )
            )
        connection = sqlite3.connect(path)
        try:
            before = tuple(connection.iterdump())
            slot_before = connection.execute(
                "SELECT * FROM outstanding_slot"
            ).fetchall()
            uncertainty_before = connection.execute(
                "SELECT * FROM uncertainty_instances"
            ).fetchall()
        finally:
            connection.close()
        reopened = SQLiteStateStore(path, oracle, "repo-1")
        reopened._bind_classification_authority(self.authority)
        for request, capability in contenders:
            with self.assertRaisesRegex(DispatchDenied, "repository slot"):
                reopened.commit_intent(
                    request, capability, self.authority,
                    expected_head=oracle.allowed_head,
                    writer_epoch=writer_epoch,
                )
        connection = sqlite3.connect(path)
        try:
            self.assertEqual(tuple(connection.iterdump()), before)
            self.assertEqual(
                connection.execute("SELECT * FROM outstanding_slot").fetchall(),
                slot_before,
            )
            self.assertEqual(
                connection.execute(
                    "SELECT * FROM uncertainty_instances"
                ).fetchall(),
                uncertainty_before,
            )
        finally:
            connection.close()

    def _assert_f13_contrary_receipt_on_copy(
        self,
        *,
        label: str,
        expected_head: str,
        expected_state: LifecycleState,
        source_path: Path | None = None,
    ) -> None:
        original = self.database_path if source_path is None else source_path
        for accounting, classification, usage, disposition in (
            (
                "known",
                SourceControlClassification.KNOWN,
                3,
                BudgetDisposition.ADJUSTED.value,
            ),
            (
                "unknown",
                SourceControlClassification.UNKNOWN,
                None,
                BudgetDisposition.UNKNOWN_WORST_CASE_CHARGED.value,
            ),
        ):
            path = self.database_path.parent / (
                f"f13-proof-first-{label}-{accounting}.sqlite3"
            )
            shutil.copy2(original, path)
            oracle = MutableFreshnessOracle()
            oracle.allowed_head = expected_head
            branch = SQLiteStateStore(path, oracle, "repo-1")
            branch._bind_classification_authority(self.authority)
            connection = sqlite3.connect(path)
            try:
                lifecycle_before = connection.execute(
                    "SELECT lifecycle_state FROM runs WHERE run_id = 'run-1'"
                ).fetchone()[0]
                slot_before = connection.execute(
                    "SELECT * FROM outstanding_slot"
                ).fetchall()
                proof_before = connection.execute(
                    "SELECT * FROM proven_nonexecution_actions WHERE "
                    "settlement_event_id = 'nonexecution-1'"
                ).fetchone()
            finally:
                connection.close()
            self.assertEqual(lifecycle_before, expected_state.value)
            self.assertIsNotNone(proof_before)
            recorded = self._record_signed_effect_observation(
                EffectObservationRequest(
                    f"f13-{label}-{accounting}-observation",
                    f"f13-{label}-{accounting}-command",
                    f"f13-{label}-{accounting}-event",
                    "repo-1", "run-1", "item-1", "effect-1", "attempt-1",
                    f"f13-{label}-{accounting}-receipt",
                    self.capability.claim_id, "descriptor-digest", usage,
                    f"f13-{label}-{accounting}-settlement", "",
                ),
                classification=classification,
                store=branch,
            )
            oracle.allowed_head = recorded.event_hash
            connection = sqlite3.connect(path)
            try:
                event_kind = connection.execute(
                    "SELECT event_kind FROM events WHERE event_id = ?",
                    (recorded.event_id,),
                ).fetchone()[0]
                lifecycle = connection.execute(
                    "SELECT lifecycle_state FROM runs WHERE run_id = 'run-1'"
                ).fetchone()[0]
                slot_after = connection.execute(
                    "SELECT * FROM outstanding_slot"
                ).fetchall()
                proof_after = connection.execute(
                    "SELECT * FROM proven_nonexecution_actions WHERE "
                    "settlement_event_id = 'nonexecution-1'"
                ).fetchone()
                accounting_row = connection.execute(
                    "SELECT disposition, uncertainty FROM budget_reservations "
                    "WHERE reservation_id = 'reservation-1'"
                ).fetchone()
                fence = connection.execute(
                    "SELECT reason_code FROM dispatch_fences WHERE "
                    "reason_code = 'LATE_ACCOUNTING_AFTER_RELEASE'"
                ).fetchone()
            finally:
                connection.close()
            terminal = expected_state in {
                LifecycleState.COMPLETED,
                LifecycleState.FAILED_FINAL,
                LifecycleState.STOPPED,
            }
            self.assertEqual(event_kind, "LATE_RECEIPT_RECORDED")
            self.assertEqual(
                lifecycle,
                expected_state.value
                if terminal
                else LifecycleState.RECONCILIATION_REQUIRED.value,
            )
            self.assertEqual(recorded.resulting_state.value, lifecycle)
            self.assertEqual(proof_after, proof_before)
            self.assertEqual(accounting_row[0], disposition)
            self.assertEqual(
                accounting_row[1],
                int(disposition == BudgetDisposition.UNKNOWN_WORST_CASE_CHARGED.value),
            )
            self.assertIsNotNone(fence)
            if not terminal:
                self.assertEqual(slot_after, slot_before)
            branch.load_verified("repo-1", authority=self.authority)

    def _build_f13_terminal_successor_state(
        self,
        *,
        label: str,
        source_path: Path,
        source_head: str,
        retry_capability,
        verdict: str,
    ) -> tuple[Path, str, LifecycleState]:
        path = self.database_path.parent / f"f13-successor-{label}.sqlite3"
        shutil.copy2(source_path, path)
        oracle = MutableFreshnessOracle()
        oracle.allowed_head = source_head
        store = SQLiteStateStore(path, oracle, "repo-1")
        store._bind_classification_authority(self.authority)
        operation_observation = self._record_signed_effect_observation(
            EffectObservationRequest(
                f"f13-{label}-effect-observation",
                f"f13-{label}-effect-command",
                f"f13-{label}-effect-event",
                "repo-1", "run-1", "item-1", "effect-1", "attempt-2",
                f"f13-{label}-effect-receipt", retry_capability.claim_id,
                "descriptor-digest", 2, f"f13-{label}-effect-settlement", "",
            ),
            store=store,
        )
        oracle.allowed_head = operation_observation.event_hash
        suffix = f"f13-{label}"
        containment_json, containment_digest = validator_containment(
            "input-1", suffix
        )
        grant = SyntheticValidatorGrant(
            f"validator-grant-{suffix}", "repo-1", "effect-1",
            "revision-1", "check-1", "input-1",
            f"validator-attempt-{suffix}", f"read-only-scope-{suffix}",
            containment_digest,
        )
        self.authority.register_validator(grant)
        capability = self.authority.claim_validator(*grant.__dict__.values())
        intent_request = ValidatorIntentRequest(
            f"validator-intent-{suffix}", f"validator-command-{suffix}",
            f"validator-event-{suffix}", "repo-1", "run-1", "item-1",
            "effect-1", "attempt-2", operation_observation.observation_id,
            operation_observation.event_hash, "revision-1", "check-1",
            "input-1", f"validator-attempt-{suffix}",
            f"validator-permission-{suffix}",
            f"validator-reservation-{suffix}", "validator-budget-policy-1",
            1, 2, 10, None, containment_json,
        )
        committed = store.commit_validator_intent(
            intent_request, capability, self.authority
        )
        oracle.allowed_head = committed.event_hash
        validator_path = path.parent / "synthetic-validator.sqlite3"
        adapter = SyntheticValidatorAdapter(validator_path)
        adapter._canonical_repository_id = "repo-1"
        adapter._canonical_ledger_path = validator_path.resolve()
        spec = parse_validator_containment_spec(containment_json)
        result_digest = f"result-digest-{suffix}"
        validator_request = SyntheticValidatorRequest(
            "repo-1", "effect-1", "revision-1", "check-1", "input-1",
            f"validator-attempt-{suffix}", f"read-only-scope-{suffix}",
            result_digest, verdict, containment_digest, spec.allowed_actions,
            spec.input_root, f"{spec.output_root}/result.json",
            f"{spec.scratch_root}/work",
            synthetic_validator_output_size(result_digest, verdict),
        )
        result = adapter._execute_committed(
            capability, validator_request, self.authority, store, committed,
            intent_request, usage_units=1,
        )
        self.assertIsNotNone(result)
        connection = sqlite3.connect(path)
        try:
            oracle.allowed_head = connection.execute(
                "SELECT catalog_head FROM repositories WHERE "
                "repository_id = 'repo-1'"
            ).fetchone()[0]
        finally:
            connection.close()
        settlement_request = BudgetSettlementRequest(
            f"validator-settlement-{suffix}",
            f"validator-reservation-{suffix}", "",
            BudgetDisposition.CONSUMED, 1, result.result_id,
            "VALIDATOR_USAGE_REPORTED",
        )
        settlement = store._settle_budget(
            settlement_request,
            self.authority.issue_settlement_proof(
                f"validator-proof-{suffix}", settlement_request
            ),
            self.authority,
        )
        oracle.allowed_head = settlement.settlement_hash
        cessation = self.authority.issue_validator_cessation_attestation(
            f"cessation-attestation-{suffix}", f"cessation-{suffix}",
            adapter._target_digest("repo-1"), capability.claim_id,
            f"VALIDATOR:{intent_request.validator_intent_id}",
            committed.event_hash, "repo-1", "run-1", "item-1", "effect-1",
            "revision-1", "check-1", f"validator-attempt-{suffix}",
        )
        cessation_seal = adapter.seal_cessation(cessation, self.authority)
        ceased = store.record_validator_cessation(
            ValidatorCessationRequest(
                f"cessation-{suffix}", f"cessation-command-{suffix}",
                f"cessation-event-{suffix}", "repo-1", "run-1", "item-1",
                "effect-1", intent_request.validator_intent_id,
                f"validator-attempt-{suffix}", "revision-1", "check-1",
                cessation_seal.cessation_hash,
            ),
            self.authority,
        )
        oracle.allowed_head = ceased.event_hash
        validator_observation = store._record_validator_observation(
            ValidatorObservationRequest(
                f"validator-observation-{suffix}",
                f"validator-observe-command-{suffix}",
                f"validator-observation-event-{suffix}",
                "repo-1", "run-1", "item-1", "effect-1",
                intent_request.validator_intent_id,
                f"validator-attempt-{suffix}", result.result_id,
                capability.claim_id, "revision-1", "check-1", "input-1",
                result_digest, verdict, 1,
                settlement_request.settlement_event_id,
                settlement.settlement_hash,
            )
        )
        oracle.allowed_head = validator_observation.event_hash
        classification = None
        if verdict == "FAIL":
            classification = self.authority.issue_classification(
                f"classification-{suffix}", "repo-1", "run-1", "item-1",
                "effect-1", "revision-1", "check-1",
                f"validator-attempt-{suffix}",
                validator_observation.observation_id,
                validator_observation.event_hash, result_digest,
                verdict="FAIL", policy_id="failure-policy",
                policy_version="1", classification="FINAL",
            )
        applied = store._apply_validator_observation(
            ValidationApplicationRequest(
                f"application-{suffix}", f"apply-command-{suffix}",
                f"apply-event-{suffix}", "repo-1", "run-1", "item-1",
                "effect-1", "revision-1", "check-1",
                f"validator-attempt-{suffix}",
                validator_observation.observation_id,
            ),
            classification=classification,
        )
        oracle.allowed_head = applied.event_hash
        if verdict == "FAIL":
            self.assertEqual(applied.resulting_state, LifecycleState.FAILED_FINAL)
            return path, applied.event_hash, LifecycleState.FAILED_FINAL
        self.assertEqual(applied.resulting_state, LifecycleState.BLOCKED)
        plan_id = "plan:run-1"
        request = FinalizeOperationRequest(
            f"finalization-{suffix}", f"finalize-command-{suffix}",
            f"finalize-event-{suffix}", "repo-1", "run-1", "item-1",
            "effect-1", plan_id, "revision-1", "attempt-2", 2,
        )
        connection = sqlite3.connect(path)
        try:
            plan_event_hash, gate_set_digest = connection.execute(
                "SELECT event_hash, gate_set_digest FROM validation_plans "
                "WHERE plan_id = ?", (plan_id,),
            ).fetchone()
        finally:
            connection.close()
        finalization_key = store.finalization_key(
            "repo-1", "run-1", "item-1", "effect-1", plan_id, "revision-1"
        )
        attestation = self.authority.issue_finalization_attestation(
            f"attestation-{suffix}", "repo-1", "run-1", "item-1",
            "effect-1", plan_id, plan_event_hash, "revision-1",
            applied.event_hash, finalization_key, gate_set_digest,
            "attempt-2", 2,
        )
        finalized = store._finalize_operation(
            request, attestation, self.authority
        )
        oracle.allowed_head = finalized.event_hash
        self.assertEqual(finalized.resulting_state, LifecycleState.COMPLETED)
        return path, finalized.event_hash, LifecycleState.COMPLETED

    def _prepare_t07_activity_settlement(self):
        committed = self._commit_planned_intent(
            self.request(), self.capability, self.authority,
            expected_head="", writer_epoch=1,
        )
        self.oracle.allowed_head = committed.event_hash
        pause_grant = SyntheticOperatorGrant(
            "pause-grant-1", "repo-1", "run-1", "PAUSE", "pause-scope-1"
        )
        self.authority.register_operator(pause_grant)
        pause = self.store.pause_local_execution(
            PauseLocalExecutionRequest(
                "pause-1", "pause-command-1", "pause-event-1",
                "pause-fence-1", "repo-1", "run-1", "item-1",
                "effect-1", "attempt-1", committed.event_id,
                committed.event_hash, 1, "OPERATOR_PAUSE_LOCAL_EXECUTION",
            ),
            self.authority.claim_operator(*pause_grant.__dict__.values()),
            self.authority,
        )
        self.oracle.allowed_head = pause.event_hash
        target_path = self.database_path.parent / "synthetic-target.sqlite3"
        adapter = SyntheticExecutionAdapter(target_path)
        adapter._canonical_repository_id = "repo-1"
        adapter._canonical_ledger_path = target_path.resolve()
        attestation = self.authority.issue_nonexecution_attestation(
            "intent-nonexecution-attestation-1",
            "intent-nonexecution-seal-1", "EFFECT",
            adapter._target_digest("repo-1"), self.capability.claim_id,
            f"EFFECT-INTENT:{committed.command_id}", committed.event_hash,
            "reservation-1", "repo-1", "run-1", "item-1", "effect-1",
            "attempt-1",
        )
        seal = adapter.seal_nonexecution(attestation, self.authority)
        nonexecution_request = BudgetSettlementRequest(
            "nonexecution-1", "reservation-1", "",
            BudgetDisposition.RELEASED, None,
            "nonexecution-evidence-1", "NONDISPATCH_PROVEN",
            non_dispatch_proven=True, zero_liability_proven=True,
            release_slot=False, all_obligations_settled=True,
            nonexecution_seal_id=seal.seal_id,
        )
        nonexecution = self.store._settle_budget(
            nonexecution_request,
            self.authority.issue_settlement_proof(
                "nonexecution-proof-1", nonexecution_request
            ),
            self.authority,
        )
        self.oracle.allowed_head = nonexecution.settlement_hash
        request = PauseActivitySettlementRequest(
            "activity-settlement-1", "activity-settlement-command-1",
            "activity-settlement-event-1", "repo-1", "run-1", "item-1",
            "effect-1", "attempt-1", "pause-1", pause.event_id,
            pause.event_hash, "pause-fence-1", committed.event_id,
            committed.event_hash, "nonexecution-1",
            nonexecution.settlement_hash, "reservation-1",
            nonexecution.settlement_hash, 1,
            "operation-recovery:attempt-1",
        )
        return request, pause, nonexecution

    def test_t07_settles_exact_t05_after_authoritative_t25_proof(self) -> None:
        request, _, nonexecution = self._prepare_t07_activity_settlement()

        receipt = self.store.settle_activity_pause(request)
        self.oracle.allowed_head = receipt.event_hash

        self.assertEqual(receipt.resulting_state, LifecycleState.PAUSED)
        connection = sqlite3.connect(self.database_path)
        try:
            run = connection.execute(
                "SELECT lifecycle_state, continuation_cursor FROM runs "
                "WHERE run_id = 'run-1'"
            ).fetchone()
            reservation = connection.execute(
                "SELECT disposition, settlement_head_hash FROM "
                "budget_reservations WHERE reservation_id = 'reservation-1'"
            ).fetchone()
            slot = connection.execute(
                "SELECT attempt_id, generation FROM outstanding_slot WHERE "
                "repository_id = 'repo-1'"
            ).fetchone()
            fence = connection.execute(
                "SELECT originating_event_id FROM dispatch_fences WHERE "
                "fence_id = 'pause-fence-1'"
            ).fetchone()
            action = connection.execute(
                "SELECT path_class, resolved_uncertainty_ids_json FROM "
                "proven_nonexecution_actions WHERE settlement_event_id = "
                "'nonexecution-1'"
            ).fetchone()
        finally:
            connection.close()
        self.assertEqual(run, ("PAUSED", "operation-recovery:attempt-1"))
        self.assertEqual(
            reservation,
            ("RELEASED", nonexecution.settlement_hash),
            "T07 must reference rather than duplicate the T25 settlement",
        )
        self.assertEqual(slot, ("attempt-1", 1))
        self.assertEqual(fence, ("pause-event-1",))
        self.assertEqual(action, ("INTENT_ONLY", "[]"))
        self._assert_f06_contenders_denied_on_copy(
            label="paused", expected_head=receipt.event_hash
        )
        self._assert_f13_contrary_receipt_on_copy(
            label="paused", expected_head=receipt.event_hash,
            expected_state=LifecycleState.PAUSED,
        )
        self.store.load_verified("repo-1")

    def test_t07_recovery_accepts_intervening_nonaccounting_fact(self) -> None:
        request, _, nonexecution = self._prepare_t07_activity_settlement()
        fact = AuthorityLifecycleFactRequest(
            "fact-between-t25-t07", "fact-between-t25-t07-command",
            "fact-between-t25-t07-event", "repo-1", "run-1", "item-1",
            "effect-1", "EFFECT", "grant-1", "EXECUTE_EFFECT", "scope-1",
            AuthorityFactKind.SOURCE_UNAVAILABLE, GovernedOrder.UNKNOWN,
            "INTENT", request.intent_event_id, request.intent_event_hash,
        )
        recorded = self.store.record_authority_fact(
            fact,
            self.authority.issue_authority_lifecycle_evidence(
                "fact-between-t25-t07-proof", fact
            ),
            self.authority,
            expected_head=nonexecution.settlement_hash,
            writer_epoch=5,
        )
        self.assertEqual(recorded.resulting_state, LifecycleState.PAUSING)
        self.oracle.allowed_head = recorded.event_hash

        settled = self.store.settle_activity_pause(request)
        self.oracle.allowed_head = settled.event_hash

        connection = sqlite3.connect(self.database_path)
        try:
            previous_hash = connection.execute(
                "SELECT previous_event_hash FROM events WHERE event_id = ?",
                (settled.event_id,),
            ).fetchone()[0]
            fences = {
                row[0] for row in connection.execute(
                    "SELECT fence_id FROM dispatch_fences"
                )
            }
        finally:
            connection.close()
        self.assertEqual(previous_hash, recorded.event_hash)
        self.assertEqual(
            request.nonexecution_event_hash, nonexecution.settlement_hash
        )
        self.assertIn(request.pause_fence_id, fences)
        self.assertIn("authority:fact-between-t25-t07", fences)
        self.store.load_verified("repo-1", authority=self.authority)

    def test_t14_resumes_t07_only_to_blocked_with_recovery_cursor(self) -> None:
        settlement_request, pause, _ = self._prepare_t07_activity_settlement()
        settled = self.store.settle_activity_pause(settlement_request)
        self.oracle.allowed_head = settled.event_hash
        self._assert_f13_contrary_receipt_on_copy(
            label="paused", expected_head=settled.event_hash,
            expected_state=LifecycleState.PAUSED,
        )
        _, run_heads = self.store.load_verified("repo-1")
        resume_grant = SyntheticOperatorGrant(
            "resume-grant-1", "repo-1", "run-1", "RESUME",
            "resume-scope-1",
        )
        self.authority.register_operator(resume_grant)
        request = ResumeActivitySettlementRequest(
            "activity-resume-1", "activity-resume-command-1",
            "activity-resume-event-1", "repo-1", "run-1", "item-1",
            "effect-1", "attempt-1", "plan:run-1", "revision-1",
            settlement_request.settlement_id, settled.event_id,
            settled.event_hash, settlement_request.source_pause_id,
            pause.event_id, pause.event_hash, "pause-fence-1",
            "operation-recovery:attempt-1", settled.event_hash,
            settled.event_hash, self.store._run_heads_digest(run_heads),
        )
        resume_capability = self.authority.claim_operator(
            *resume_grant.__dict__.values()
        )
        resume_evidence = self.authority.issue_activity_resume_evidence(
            "activity-resume-proof-1", request
        )
        connection = sqlite3.connect(self.database_path)
        try:
            before_stale_resume = tuple(connection.iterdump())
        finally:
            connection.close()
        self.oracle.allowed_head = "stale-before-t14-resume"
        with self.assertRaisesRegex(DispatchDenied, "freshness"):
            self.store.resume_activity_settlement(
                request, resume_capability, resume_evidence, self.authority
            )
        connection = sqlite3.connect(self.database_path)
        try:
            after_stale_resume = tuple(connection.iterdump())
        finally:
            connection.close()
        self.assertEqual(after_stale_resume, before_stale_resume)
        self.oracle.allowed_head = settled.event_hash
        receipt = self.store.resume_activity_settlement(
            request,
            resume_capability,
            resume_evidence,
            self.authority,
        )
        self.oracle.allowed_head = receipt.event_hash

        self.assertEqual(receipt.resulting_state, LifecycleState.BLOCKED)
        connection = sqlite3.connect(self.database_path)
        try:
            run = connection.execute(
                "SELECT lifecycle_state, continuation_cursor FROM runs "
                "WHERE run_id = 'run-1'"
            ).fetchone()
            slot = connection.execute(
                "SELECT attempt_id, generation FROM outstanding_slot"
            ).fetchone()
            pause_fence = connection.execute(
                "SELECT 1 FROM dispatch_fences WHERE fence_id = "
                "'pause-fence-1'"
            ).fetchone()
        finally:
            connection.close()
        self.assertEqual(run, ("BLOCKED", "operation-recovery:attempt-1"))
        self.assertEqual(slot, ("attempt-1", 1))
        self.assertIsNone(pause_fence)
        self._assert_f06_contenders_denied_on_copy(
            label="pre-generation-transfer", expected_head=receipt.event_hash
        )
        self._assert_f13_contrary_receipt_on_copy(
            label="blocked", expected_head=receipt.event_hash,
            expected_state=LifecycleState.BLOCKED,
        )
        self.store.load_verified("repo-1")

        recovery_grant = SyntheticOperatorGrant(
            "activity-recovery-grant-1", "repo-1", "run-1",
            "RECOVER_OPERATION", "activity-recovery-scope-1",
        )
        self.authority.register_operator(recovery_grant)
        connection = sqlite3.connect(self.database_path)
        try:
            source_hash = connection.execute(
                "SELECT event_hash FROM proven_nonexecution_actions WHERE "
                "settlement_event_id = 'nonexecution-1'"
            ).fetchone()[0]
        finally:
            connection.close()
        recovered = self.store.recover_proven_nonexecution(
            RecoverProvenNonexecutionRequest(
                "activity-operation-recovery-1",
                "activity-retry-authorization-1",
                "activity-operation-recovery-command-1",
                "activity-operation-recovery-event-1", "repo-1", "run-1",
                "item-1", "effect-1", "attempt-1", "attempt-2",
                "plan:run-1", "revision-1", "descriptor-digest",
                "nonexecution-1", source_hash, (),
                "operation-recovery:attempt-1", 1, 2,
                receipt.event_hash, receipt.event_hash,
            ),
            self.authority.claim_operator(*recovery_grant.__dict__.values()),
            self.authority,
        )
        self.oracle.allowed_head = recovered.event_hash
        self.assertEqual(recovered.resulting_state, LifecycleState.PLANNED)
        self._assert_f06_contenders_denied_on_copy(
            label="authorized-retry", expected_head=recovered.event_hash
        )
        self._assert_f13_contrary_receipt_on_copy(
            label="planned", expected_head=recovered.event_hash,
            expected_state=LifecycleState.PLANNED,
        )
        self.store.load_verified("repo-1", authority=self.authority)

        retry_grant = SyntheticGrant(
            "activity-retry-grant-1", "repo-1", "effect-1", "attempt-2",
            "scope-1",
        )
        self.authority.register(retry_grant)
        retry_capability = self.authority.claim(*retry_grant.__dict__.values())
        retry_request = ProvenNonexecutionIntentRequest(
            "repo-1", "run-1", "item-1", "activity-retry-command-1",
            "activity-retry-event-1", "effect-1", "descriptor-digest",
            "attempt-2", "activity-retry-permission-1",
            "activity-retry-reservation-1", "budget-policy-digest",
            3, 5, 10, "activity-retry-authorization-1", "attempt-1", 1, 2,
        )
        connection = sqlite3.connect(self.database_path)
        try:
            writer_epoch = connection.execute(
                "SELECT MAX(writer_epoch) + 1 FROM events"
            ).fetchone()[0]
        finally:
            connection.close()
        retry_intent = self.store.commit_intent(
            retry_request, retry_capability, self.authority,
            expected_head=recovered.event_hash, writer_epoch=writer_epoch,
        )
        self.oracle.allowed_head = retry_intent.event_hash
        self._assert_f06_contenders_denied_on_copy(
            label="post-generation-transfer", expected_head=retry_intent.event_hash
        )
        self._assert_f13_contrary_receipt_on_copy(
            label="running", expected_head=retry_intent.event_hash,
            expected_state=LifecycleState.RUNNING,
        )

        pausing_path = (
            self.database_path.parent / "f13-successor-pausing.sqlite3"
        )
        shutil.copy2(self.database_path, pausing_path)
        pausing_oracle = MutableFreshnessOracle()
        pausing_oracle.allowed_head = retry_intent.event_hash
        pausing_store = SQLiteStateStore(
            pausing_path, pausing_oracle, "repo-1"
        )
        pausing_store._bind_classification_authority(self.authority)
        pausing_grant = SyntheticOperatorGrant(
            "f13-successor-pausing-grant", "repo-1", "run-1", "PAUSE",
            "f13-successor-pausing-scope",
        )
        self.authority.register_operator(pausing_grant)
        pausing_receipt = pausing_store.pause_local_execution(
            PauseLocalExecutionRequest(
                "f13-successor-pausing", "f13-successor-pausing-command",
                "f13-successor-pausing-event", "f13-successor-pausing-fence",
                "repo-1", "run-1", "item-1", "effect-1", "attempt-2",
                retry_intent.event_id, retry_intent.event_hash, 2,
                "OPERATOR_PAUSE_LOCAL_EXECUTION",
            ),
            self.authority.claim_operator(*pausing_grant.__dict__.values()),
            self.authority,
        )
        pausing_oracle.allowed_head = pausing_receipt.event_hash
        self.assertEqual(
            pausing_receipt.resulting_state, LifecycleState.PAUSING
        )
        self._assert_f13_contrary_receipt_on_copy(
            label="pausing", expected_head=pausing_receipt.event_hash,
            expected_state=LifecycleState.PAUSING,
            source_path=pausing_path,
        )

        for state_label, classification, usage, expected_state in (
            (
                "validating", SourceControlClassification.KNOWN, 2,
                LifecycleState.VALIDATING,
            ),
            (
                "reconciliation", SourceControlClassification.UNKNOWN, None,
                LifecycleState.RECONCILIATION_REQUIRED,
            ),
        ):
            state_path = self.database_path.parent / (
                f"f13-successor-{state_label}.sqlite3"
            )
            shutil.copy2(self.database_path, state_path)
            state_oracle = MutableFreshnessOracle()
            state_oracle.allowed_head = retry_intent.event_hash
            state_store = SQLiteStateStore(state_path, state_oracle, "repo-1")
            state_store._bind_classification_authority(self.authority)
            state_receipt = self._record_signed_effect_observation(
                EffectObservationRequest(
                    f"f13-successor-{state_label}-observation",
                    f"f13-successor-{state_label}-command",
                    f"f13-successor-{state_label}-event",
                    "repo-1", "run-1", "item-1", "effect-1", "attempt-2",
                    f"f13-successor-{state_label}-receipt",
                    retry_capability.claim_id, "descriptor-digest", usage,
                    f"f13-successor-{state_label}-settlement", "",
                ),
                classification=classification,
                store=state_store,
            )
            state_oracle.allowed_head = state_receipt.event_hash
            self.assertEqual(state_receipt.resulting_state, expected_state)
            self._assert_f13_contrary_receipt_on_copy(
                label=state_label,
                expected_head=state_receipt.event_hash,
                expected_state=expected_state,
                source_path=state_path,
            )

        stopped_path = self.database_path.parent / "f13-successor-stopped.sqlite3"
        shutil.copy2(self.database_path, stopped_path)
        stopped_oracle = MutableFreshnessOracle()
        stopped_oracle.allowed_head = retry_intent.event_hash
        stopped_store = SQLiteStateStore(stopped_path, stopped_oracle, "repo-1")
        stopped_store._bind_classification_authority(self.authority)
        stopped_receipt = stopped_store.stop(
            self._stop_request(StopMode.IMMEDIATE, "f13-successor"),
            self._stop_capability(StopMode.IMMEDIATE, "f13-successor"),
            self.authority,
        )
        stopped_oracle.allowed_head = stopped_receipt.event_hash
        self._assert_f13_contrary_receipt_on_copy(
            label="stopped", expected_head=stopped_receipt.event_hash,
            expected_state=LifecycleState.STOPPED,
            source_path=stopped_path,
        )
        for terminal_label, verdict in (
            ("completed", "PASS"),
            ("failed-final", "FAIL"),
        ):
            terminal_path, terminal_head, terminal_state = (
                self._build_f13_terminal_successor_state(
                    label=terminal_label,
                    source_path=self.database_path,
                    source_head=retry_intent.event_hash,
                    retry_capability=retry_capability,
                    verdict=verdict,
                )
            )
            self._assert_f13_contrary_receipt_on_copy(
                label=terminal_label,
                expected_head=terminal_head,
                expected_state=terminal_state,
                source_path=terminal_path,
            )
        retry_launch = self.store.claim_operation_launch(
            retry_request, retry_intent
        )
        self.oracle.allowed_head = retry_launch.event_hash
        self.store._contact_claimed_operation(
            retry_request, retry_capability, retry_intent, retry_launch,
            self.store._adapter_target_digest("repo-1", "EFFECT"),
        )
        connection = sqlite3.connect(self.database_path)
        connection.row_factory = sqlite3.Row
        try:
            retry_contact = connection.execute(
                "SELECT * FROM adapter_contacts WHERE source_id = ?",
                (f"EFFECT:{retry_launch.launch_id}",),
            ).fetchone()
            self.oracle.allowed_head = connection.execute(
                "SELECT catalog_head FROM repositories WHERE repository_id = "
                "'repo-1'"
            ).fetchone()[0]
        finally:
            connection.close()
        external_grant = SyntheticOperatorGrant(
            "activity-external-pause-grant-1", "repo-1", "run-1", "PAUSE",
            "activity-external-pause-scope-1",
        )
        self.authority.register_operator(external_grant)
        external_request = PauseExternalMutationRequest(
            "activity-external-pause-1", "activity-external-pause-command-1",
            "activity-external-pause-event-1",
            "activity-external-pause-fence-1", "repo-1", "run-1", "item-1",
            "effect-1", "attempt-2", retry_intent.event_id,
            retry_intent.event_hash, retry_launch.launch_id,
            retry_launch.event_id, retry_launch.event_hash,
            retry_contact["contact_id"], retry_contact["event_id"],
            retry_contact["event_hash"], retry_contact["target_digest"], 2,
            "OPERATOR_PAUSE_EXTERNAL_MUTATION",
        )
        external_pause = self.store.pause_external_mutation(
            external_request,
            self.authority.claim_operator(*external_grant.__dict__.values()),
            self.authority,
        )
        self.oracle.allowed_head = external_pause.event_hash

        target_path = self.database_path.parent / "synthetic-target.sqlite3"
        adapter = SyntheticExecutionAdapter(target_path)
        adapter._canonical_repository_id = "repo-1"
        adapter._canonical_ledger_path = target_path.resolve()
        retry_attestation = self.authority.issue_nonexecution_attestation(
            "activity-retry-nonexecution-attestation-1",
            "activity-retry-nonexecution-seal-1", "EFFECT",
            adapter._target_digest("repo-1"), retry_capability.claim_id,
            f"EFFECT:{retry_launch.launch_id}", retry_launch.event_hash,
            "activity-retry-reservation-1", "repo-1", "run-1", "item-1",
            "effect-1", "attempt-2",
        )
        retry_seal = adapter.seal_nonexecution(
            retry_attestation, self.authority
        )
        retry_settlement_request = BudgetSettlementRequest(
            "activity-retry-nonexecution-1",
            "activity-retry-reservation-1", "",
            BudgetDisposition.RELEASED, None,
            "activity-retry-nonexecution-evidence-1", "NONDISPATCH_PROVEN",
            non_dispatch_proven=True, zero_liability_proven=True,
            release_slot=False, all_obligations_settled=True,
            nonexecution_seal_id=retry_seal.seal_id,
            attempt_id="attempt-2",
        )

        def settle_and_resume_external(
            target_store, target_oracle, *, suffix: str,
        ):
            connection = sqlite3.connect(target_store._database_path)
            try:
                current_settlement_head = connection.execute(
                    "SELECT settlement_head_hash FROM budget_reservations "
                    "WHERE reservation_id = 'activity-retry-reservation-1'"
                ).fetchone()[0]
            finally:
                connection.close()
            target_settlement_request = replace(
                retry_settlement_request,
                expected_previous_hash=current_settlement_head,
            )
            settled_retry = target_store._settle_budget(
                target_settlement_request,
                self.authority.issue_settlement_proof(
                    f"activity-retry-nonexecution-proof-{suffix}",
                    target_settlement_request,
                ),
                self.authority,
            )
            target_oracle.allowed_head = settled_retry.settlement_hash
            connection = sqlite3.connect(target_store._database_path)
            try:
                catalog_head = connection.execute(
                    "SELECT catalog_head FROM repositories WHERE "
                    "repository_id = 'repo-1'"
                ).fetchone()[0]
                resolved_ids = tuple(
                    row[0] for row in connection.execute(
                        "SELECT uncertainty_id FROM uncertainty_resolutions "
                        "WHERE reconciliation_id = ? ORDER BY uncertainty_id",
                        (
                            "proven-nonexecution:"
                            "activity-retry-nonexecution-1",
                        ),
                    )
                )
            finally:
                connection.close()
            resume_grant = SyntheticOperatorGrant(
                f"activity-external-resume-grant-{suffix}", "repo-1",
                "run-1", "RESUME",
                f"activity-external-resume-scope-{suffix}",
            )
            self.authority.register_operator(resume_grant)
            resume_request = ResumeOperationNonexecutionRequest(
                f"activity-external-resume-{suffix}",
                f"activity-external-resume-command-{suffix}",
                f"activity-external-resume-event-{suffix}", "repo-1",
                "run-1", "item-1", "effect-1", "attempt-2",
                "plan:run-1", "revision-1", "descriptor-digest",
                external_request.pause_id, external_pause.event_id,
                external_pause.event_hash, external_request.fence_id,
                target_settlement_request.settlement_event_id,
                settled_retry.settlement_hash,
                "activity-retry-reservation-1",
                settled_retry.settlement_hash, resolved_ids,
                "operation-recovery:attempt-2", "attempt-2", 2,
                catalog_head, catalog_head,
                target_store._run_heads_digest({"run-1": catalog_head}),
            )
            resume_receipt = target_store.resume_operation_nonexecution(
                resume_request,
                self.authority.claim_operator(*resume_grant.__dict__.values()),
                self.authority.issue_operation_nonexecution_resume_evidence(
                    f"activity-external-resume-proof-{suffix}",
                    resume_request,
                ),
                self.authority,
            )
            target_oracle.allowed_head = resume_receipt.event_hash
            target_store.load_verified("repo-1", authority=self.authority)
            return resume_receipt

        stacked_path = self.database_path.parent / "stacked-t14.sqlite3"
        shutil.copy2(self.database_path, stacked_path)
        stacked_oracle = MutableFreshnessOracle()
        stacked_oracle.allowed_head = external_pause.event_hash
        stacked_store = SQLiteStateStore(
            stacked_path, stacked_oracle, "repo-1"
        )
        stacked_store._bind_classification_authority(self.authority)
        stacked_grant = SyntheticOperatorGrant(
            "activity-stacked-pause-grant-1", "repo-1", "run-1", "PAUSE",
            "activity-stacked-pause-scope-1",
        )
        self.authority.register_operator(stacked_grant)
        stacked_pause = stacked_store.pause_reconciliation(
            PauseReconciliationRequest(
                "activity-stacked-pause-1",
                "activity-stacked-pause-command-1",
                "activity-stacked-pause-event-1",
                "activity-stacked-pause-fence-1", "repo-1", "run-1",
                "item-1", "effect-1", "plan:run-1", "revision-1",
                "OPERATOR_PAUSE_RECONCILIATION", external_pause.event_id,
                external_pause.event_hash, None,
            ),
            self.authority.claim_operator(*stacked_grant.__dict__.values()),
            self.authority,
        )
        stacked_oracle.allowed_head = stacked_pause.event_hash
        stacked_resume = settle_and_resume_external(
            stacked_store, stacked_oracle, suffix="stacked"
        )
        self.assertEqual(stacked_resume.resulting_state, LifecycleState.PAUSED)

        cleared_resume = settle_and_resume_external(
            self.store, self.oracle, suffix="cleared-prior"
        )
        self.assertEqual(cleared_resume.resulting_state, LifecycleState.BLOCKED)

    def test_t14_slot_generation_is_derived_from_exact_t07_source(self) -> None:
        settlement_request, _, _ = self._prepare_t07_activity_settlement()
        settled = self.store.settle_activity_pause(settlement_request)
        connection = self.store._connect()
        try:
            source = connection.execute(
                "SELECT * FROM activity_pause_settlements WHERE "
                "settlement_id = ?",
                (settlement_request.settlement_id,),
            ).fetchone()
            source_body = json.loads(source["body_json"])
        finally:
            connection.close()
        future_body = {
            **source_body,
            "expected_slot_generation": 2,
        }

        self.assertEqual(
            self.store._activity_pause_slot_generation(
                {**dict(source), "slot_generation": 2}, future_body
            ),
            2,
        )
        with self.assertRaisesRegex(StorageIntegrityError, "slot generation"):
            self.store._activity_pause_slot_generation(source, future_body)
        self.oracle.allowed_head = settled.event_hash
        self.store.load_verified("repo-1")

    def test_t07_crash_is_atomic_and_committed_retry_replays(self) -> None:
        request, _, nonexecution = self._prepare_t07_activity_settlement()
        with self.assertRaises(InjectedFailure):
            self.store.settle_activity_pause(
                request,
                failure_hook=raise_at(
                    "after_activity_pause_settlement_writes_before_commit"
                ),
            )
        connection = sqlite3.connect(self.database_path)
        try:
            state = connection.execute(
                "SELECT lifecycle_state FROM runs WHERE run_id = 'run-1'"
            ).fetchone()[0]
            count = connection.execute(
                "SELECT COUNT(*) FROM activity_pause_settlements"
            ).fetchone()[0]
        finally:
            connection.close()
        self.assertEqual((state, count), ("PAUSING", 0))
        self.assertEqual(self.oracle.allowed_head, nonexecution.settlement_hash)

        with self.assertRaises(InjectedFailure):
            self.store.settle_activity_pause(
                request,
                failure_hook=raise_at(
                    "after_activity_pause_settlement_commit_before_acknowledgement"
                ),
            )
        connection = sqlite3.connect(self.database_path)
        try:
            committed_hash = connection.execute(
                "SELECT event_hash FROM activity_pause_settlements"
            ).fetchone()[0]
        finally:
            connection.close()
        self.oracle.allowed_head = committed_hash
        replay = self.store.settle_activity_pause(request)
        self.assertTrue(replay.replayed)
        self.assertEqual(replay.event_hash, committed_hash)
        self.store.load_verified("repo-1")

    def test_t07_rejects_stale_or_rebound_t25_accounting(self) -> None:
        request, _, _ = self._prepare_t07_activity_settlement()
        connection = sqlite3.connect(self.database_path)
        try:
            before = tuple(connection.iterdump())
        finally:
            connection.close()
        with self.assertRaisesRegex(DispatchDenied, "accounting head"):
            self.store.settle_activity_pause(
                replace(request, settlement_head_hash="rebound-head")
            )
        connection = sqlite3.connect(self.database_path)
        try:
            after = tuple(connection.iterdump())
        finally:
            connection.close()
        self.assertEqual(after, before)

    def test_t23_late_receipt_after_t07_preserves_history_and_slot(self) -> None:
        request, _, nonexecution = self._prepare_t07_activity_settlement()
        settled = self.store.settle_activity_pause(request)
        self.oracle.allowed_head = settled.event_hash
        late_accounting_request = BudgetSettlementRequest(
            "late-accounting-1", "reservation-1",
            nonexecution.settlement_hash, BudgetDisposition.ADJUSTED, 2,
            "late-receipt-1", "USAGE_REPORTED",
        )
        late_accounting = self.store._settle_budget(
            late_accounting_request,
            self.authority.issue_settlement_proof(
                "late-accounting-proof-1", late_accounting_request
            ),
            self.authority,
        )
        self.oracle.allowed_head = late_accounting.settlement_hash
        observation = self._record_signed_effect_observation(
            EffectObservationRequest(
                "late-observation-1", "late-observation-command-1",
                "late-observation-event-1", "repo-1", "run-1", "item-1",
                "effect-1", "attempt-1", "late-receipt-1",
                self.capability.claim_id, "descriptor-digest", 2,
                "late-accounting-1", late_accounting.settlement_hash,
            )
        )
        self.oracle.allowed_head = observation.event_hash

        self.assertEqual(
            observation.resulting_state,
            LifecycleState.RECONCILIATION_REQUIRED,
        )
        connection = sqlite3.connect(self.database_path)
        try:
            event_kind = connection.execute(
                "SELECT event_kind FROM events WHERE event_id = "
                "'late-observation-event-1'"
            ).fetchone()[0]
            slot_count = connection.execute(
                "SELECT COUNT(*) FROM outstanding_slot"
            ).fetchone()[0]
            fences = {
                row[0] for row in connection.execute(
                    "SELECT reason_code FROM dispatch_fences"
                )
            }
        finally:
            connection.close()
        self.assertEqual(event_kind, "LATE_RECEIPT_RECORDED")
        self.assertEqual(slot_count, 1)
        self.assertIn("LATE_ACCOUNTING_AFTER_RELEASE", fences)
        self.store.load_verified("repo-1")
        resume_grant = SyntheticOperatorGrant(
            "late-resume-grant-1", "repo-1", "run-1", "RESUME",
            "late-resume-scope-1",
        )
        self.authority.register_operator(resume_grant)
        _, run_heads = self.store.load_verified("repo-1")
        resume_request = ResumeActivitySettlementRequest(
            "late-resume-1", "late-resume-command-1", "late-resume-event-1",
            "repo-1", "run-1", "item-1", "effect-1", "attempt-1",
            "plan:run-1", "revision-1", request.settlement_id,
            settled.event_id, settled.event_hash, request.source_pause_id,
            request.source_pause_event_id, request.source_pause_event_hash,
            request.pause_fence_id, request.continuation_cursor,
            observation.event_hash, observation.event_hash,
            self.store._run_heads_digest(run_heads),
        )
        with self.assertRaisesRegex(DispatchDenied, "PAUSED"):
            self.store.resume_activity_settlement(
                resume_request,
                self.authority.claim_operator(*resume_grant.__dict__.values()),
                self.authority.issue_activity_resume_evidence(
                    "late-resume-proof-1", resume_request
                ),
                self.authority,
            )

    def test_t07_recovery_rejects_self_consistent_source_retarget(self) -> None:
        request, _, _ = self._prepare_t07_activity_settlement()
        settled = self.store.settle_activity_pause(request)
        connection = sqlite3.connect(self.database_path)
        connection.row_factory = sqlite3.Row
        try:
            body = json.loads(
                connection.execute(
                    "SELECT body_json FROM activity_pause_settlements"
                ).fetchone()["body_json"]
            )
            body["source_pause_event_hash"] = "retargeted-pause-hash"
            rebound = PauseActivitySettlementRequest(
                **{
                    key: body[key]
                    for key in PauseActivitySettlementRequest.__dataclass_fields__
                }
            )
            body["payload_digest"] = self.store._event_hash(
                {
                    **rebound.__dict__,
                    "pause_kind": "ACTIVITY_SETTLEMENT",
                    "pause_binding_version": 1,
                    "source_kind": "NONDISPATCH_PROVEN",
                }
            )
            event_hash = self.store._event_hash(body)
            body_json = json.dumps(body, sort_keys=True, separators=(",", ":"))
            connection.execute(
                "UPDATE events SET event_hash = ?, body_json = ? WHERE "
                "event_id = ?",
                (event_hash, body_json, settled.event_id),
            )
            connection.execute(
                "UPDATE activity_pause_settlements SET "
                "source_pause_event_hash = ?, payload_digest = ?, "
                "event_hash = ?, body_json = ?",
                (
                    body["source_pause_event_hash"], body["payload_digest"],
                    event_hash, body_json,
                ),
            )
            connection.execute(
                "UPDATE command_outcomes SET payload_digest = ?, "
                "event_hash = ? WHERE command_id = ?",
                (body["payload_digest"], event_hash, body["command_id"]),
            )
            connection.execute(
                "UPDATE runs SET head_hash = ? WHERE run_id = 'run-1'",
                (event_hash,),
            )
            connection.execute(
                "UPDATE repositories SET catalog_head = ? WHERE "
                "repository_id = 'repo-1'",
                (event_hash,),
            )
            connection.commit()
        finally:
            connection.close()
        self.oracle.allowed_head = event_hash

        with self.assertRaisesRegex(
            StorageIntegrityError, "activity pause settlement"
        ):
            self.store.load_verified("repo-1")

    def test_t07_accepts_launched_precontact_only_after_canonical_t25_seal(
        self,
    ) -> None:
        intent_request = self.request()
        committed = self._commit_planned_intent(
            intent_request, self.capability, self.authority,
            expected_head="", writer_epoch=1,
        )
        self.oracle.allowed_head = committed.event_hash
        launched = self.store.claim_operation_launch(intent_request, committed)
        self.oracle.allowed_head = launched.event_hash
        pause_grant = SyntheticOperatorGrant(
            "launched-pause-grant-1", "repo-1", "run-1", "PAUSE",
            "launched-pause-scope-1",
        )
        self.authority.register_operator(pause_grant)
        pause = self.store.pause_local_execution(
            PauseLocalExecutionRequest(
                "launched-pause-1", "launched-pause-command-1",
                "launched-pause-event-1", "launched-pause-fence-1",
                "repo-1", "run-1", "item-1", "effect-1", "attempt-1",
                committed.event_id, committed.event_hash, 1,
                "OPERATOR_PAUSE_LOCAL_EXECUTION",
            ),
            self.authority.claim_operator(*pause_grant.__dict__.values()),
            self.authority,
        )
        self.oracle.allowed_head = pause.event_hash
        target_path = self.database_path.parent / "synthetic-target.sqlite3"
        adapter = SyntheticExecutionAdapter(target_path)
        adapter._canonical_repository_id = "repo-1"
        adapter._canonical_ledger_path = target_path.resolve()
        attestation = self.authority.issue_nonexecution_attestation(
            "launched-nonexecution-attestation-1",
            "launched-nonexecution-seal-1", "EFFECT",
            adapter._target_digest("repo-1"), self.capability.claim_id,
            f"EFFECT:{launched.launch_id}", launched.event_hash,
            "reservation-1", "repo-1", "run-1", "item-1", "effect-1",
            "attempt-1",
        )
        seal = adapter.seal_nonexecution(attestation, self.authority)
        nonexecution_request = BudgetSettlementRequest(
            "launched-nonexecution-1", "reservation-1", "",
            BudgetDisposition.RELEASED, None,
            "launched-nonexecution-evidence-1", "NONDISPATCH_PROVEN",
            non_dispatch_proven=True, zero_liability_proven=True,
            release_slot=False, all_obligations_settled=True,
            nonexecution_seal_id=seal.seal_id,
        )
        nonexecution = self.store._settle_budget(
            nonexecution_request,
            self.authority.issue_settlement_proof(
                "launched-nonexecution-proof-1", nonexecution_request
            ),
            self.authority,
        )
        self.oracle.allowed_head = nonexecution.settlement_hash
        settled = self.store.settle_activity_pause(
            PauseActivitySettlementRequest(
                "launched-activity-settlement-1",
                "launched-activity-settlement-command-1",
                "launched-activity-settlement-event-1", "repo-1", "run-1",
                "item-1", "effect-1", "attempt-1", "launched-pause-1",
                pause.event_id, pause.event_hash, "launched-pause-fence-1",
                committed.event_id, committed.event_hash,
                "launched-nonexecution-1", nonexecution.settlement_hash,
                "reservation-1", nonexecution.settlement_hash, 1,
                "operation-recovery:attempt-1",
            )
        )
        self.oracle.allowed_head = settled.event_hash

        self.assertEqual(settled.resulting_state, LifecycleState.PAUSED)
        connection = sqlite3.connect(self.database_path)
        try:
            path_class = connection.execute(
                "SELECT path_class FROM proven_nonexecution_actions WHERE "
                "settlement_event_id = 'launched-nonexecution-1'"
            ).fetchone()[0]
        finally:
            connection.close()
        self.assertEqual(path_class, "LAUNCHED")
        self.store.load_verified("repo-1")

    def test_t25_intent_only_recovery_denies_missing_or_rebound_seal(self) -> None:
        committed = self._running_operation()
        paused = self.store.pause_local_execution(
            self._local_pause_request(committed, suffix="intent-proof"),
            self._pause_capability("intent-proof"), self.authority,
        )
        self.oracle.allowed_head = paused.event_hash
        request = BudgetSettlementRequest(
            "intent-proof-settlement", "reservation-1", "",
            BudgetDisposition.RELEASED, None, "intent-proof-evidence",
            "NONDISPATCH_PROVEN", non_dispatch_proven=True,
            zero_liability_proven=True, release_slot=False,
            all_obligations_settled=True,
        )
        with self.assertRaisesRegex(DispatchDenied, "canonical nonexecution seal"):
            self.store._settle_budget(
                request,
                self.authority.issue_settlement_proof(
                    "intent-proof-missing", request
                ),
                self.authority,
            )
        self.assertEqual(
            self.store.table_counts()["proven_nonexecution_actions"], 0
        )

        target_path = self.database_path.parent / "synthetic-target.sqlite3"
        adapter = SyntheticExecutionAdapter(target_path)
        adapter._canonical_repository_id = "repo-1"
        adapter._canonical_ledger_path = target_path.resolve()
        rebound = self.authority.issue_nonexecution_attestation(
            "intent-proof-rebound-attestation", "intent-proof-rebound-seal",
            "EFFECT", adapter._target_digest("repo-1"),
            self.capability.claim_id, "EFFECT-INTENT:other-command",
            committed.event_hash, "reservation-1", "repo-1", "run-1",
            "item-1", "effect-1", "attempt-1",
        )
        rebound_seal = adapter.seal_nonexecution(rebound, self.authority)
        rebound_request = replace(
            request,
            settlement_event_id="intent-proof-rebound-settlement",
            nonexecution_seal_id=rebound_seal.seal_id,
        )
        with self.assertRaisesRegex(DispatchDenied, "does not bind"):
            self.store._settle_budget(
                rebound_request,
                self.authority.issue_settlement_proof(
                    "intent-proof-rebound", rebound_request
                ),
                self.authority,
            )
        self.assertEqual(
            self.store.table_counts()["proven_nonexecution_actions"], 0
        )
        self.store.load_verified("repo-1", authority=self.authority)

    def _rewrite_application_tail(self, body: dict[str, object]) -> str:
        event_hash = self.store._event_hash(body)
        body_json = json.dumps(body, sort_keys=True, separators=(",", ":"))
        connection = sqlite3.connect(self.database_path)
        try:
            connection.execute(
                "UPDATE events SET event_hash = ?, body_json = ? "
                "WHERE event_id = ?",
                (event_hash, body_json, body["event_id"]),
            )
            connection.execute(
                "UPDATE validation_applications SET event_hash = ?, "
                "resulting_state = ?, continuation_cursor = ?, body_json = ? "
                "WHERE application_id = ?",
                (
                    event_hash, body["lifecycle_to"],
                    body["continuation_cursor"], body_json,
                    body["application_id"],
                ),
            )
            connection.execute(
                "UPDATE command_outcomes SET event_hash = ? WHERE command_id = ?",
                (event_hash, body["command_id"]),
            )
            connection.execute(
                "UPDATE runs SET lifecycle_state = ?, continuation_cursor = ?, "
                "head_hash = ? WHERE run_id = ?",
                (
                    body["lifecycle_to"], body["continuation_cursor"],
                    event_hash, body["run_id"],
                ),
            )
            connection.execute(
                "UPDATE repositories SET catalog_head = ? WHERE repository_id = ?",
                (event_hash, body["repository_id"]),
            )
            connection.commit()
        finally:
            connection.close()
        return event_hash

    def test_c01_failure_before_commit_leaves_no_authoritative_state(self) -> None:
        plan = self.store.accept_plan(
            PlanAcceptanceRequest(
                "plan-1", "plan-command-1", "plan-event-1", "repo-1",
                "run-1", "item-1", "effect-1", "revision-1",
                "descriptor-digest", "scope-1", "budget-policy-digest",
                ("check-1",),
            ),
            expected_head="",
            writer_epoch=1,
        )
        self.oracle.allowed_head = plan.event_hash
        connection = sqlite3.connect(self.database_path)
        try:
            before_failure = tuple(connection.iterdump())
        finally:
            connection.close()
        with self.assertRaises(InjectedFailure):
            self.store.commit_intent(
                self.request(),
                self.capability,
                self.authority,
                expected_head=plan.event_hash,
                writer_epoch=2,
                failure_hook=raise_at("after_intent_writes_before_commit"),
            )
        connection = sqlite3.connect(self.database_path)
        try:
            after_failure = tuple(connection.iterdump())
        finally:
            connection.close()
        self.assertEqual(after_failure, before_failure)

    def test_t01_denies_plan_without_bound_classification_issuer(self) -> None:
        unbound_path = Path(self.temporary_directory.name) / "unbound.sqlite3"
        unbound_store = SQLiteStateStore(unbound_path, self.oracle, "repo-1")
        with self.assertRaisesRegex(DispatchDenied, "classification authority"):
            unbound_store.accept_plan(
                PlanAcceptanceRequest(
                    "plan-unbound", "command-unbound", "event-unbound",
                    "repo-1", "run-unbound", "item-unbound", "effect-unbound",
                    "revision-unbound", "descriptor-unbound", "scope-unbound",
                    "budget-unbound", ("check-unbound",),
                ),
                expected_head="",
                writer_epoch=1,
            )
        self.assertEqual(unbound_store.table_counts()["validation_plans"], 0)

        self.assertEqual(
            self.store.table_counts(),
            {
                "repositories": 0,
                "runs": 0,
                "validation_plans": 0,
                "validation_requirements": 0,
                "readiness_evaluations": 0,
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
                "validator_cessations": 0,
                "validation_applications": 0,
                "validation_recoveries": 0,
                "terminal_validation_settlements": 0,
                "operation_finalizations": 0,
                "operation_launches": 0,
                "control_actions": 0,
                "local_pause_actions": 0,
                "external_pause_actions": 0,
                "reconciliation_pause_actions": 0,
                "uncertainty_instances": 0,
                "uncertainty_resolutions": 0,
                "reconciliation_actions": 0,
                "verified_receipt_reconciliation_actions": 0,
                "proven_nonexecution_actions": 0,
                "operation_nonexecution_resume_actions": 0,
                "operation_recovery_actions": 0,
                "operation_retry_authorizations": 0,
                "validation_pause_actions": 0,
                "resume_actions": 0,
                "reconciliation_resume_actions": 0,
                "stop_actions": 0,
                "stop_escalations": 0,
                "operator_redemptions": 0,
                "outstanding_slot": 0,
                "dispatch_fences": 0,
                "binding_mismatches": 0,
            },
        )

    def test_t15_new_plan_requires_explicit_immutable_binding_pins(self) -> None:
        with self.assertRaisesRegex(ValueError, "immutable binding pins"):
            self.store.accept_plan(
                PlanAcceptanceContract(
                    "plan-unpinned", "command-unpinned", "event-unpinned",
                    "repo-1", "run-unpinned", "item-unpinned", "effect-unpinned",
                    "revision-unpinned", "descriptor-unpinned", "scope-unpinned",
                    "budget-unpinned", ("check-unpinned",),
                ),
                expected_head="",
                writer_epoch=1,
            )
        with self.assertRaisesRegex(ValueError, "immutable binding pins"):
            PlanAcceptanceContract(
                "plan-partial", "command-partial", "event-partial",
                "repo-1", "run-partial", "item-partial", "effect-partial",
                "revision-partial", "descriptor-partial", "scope-partial",
                "budget-partial", ("check-partial",),
                source_tree_digest="only-one-pin",
            ).validate()
        with self.assertRaisesRegex(ValueError, "must differ"):
            BindingMismatchRequest(
                "mismatch-equal", "observation-equal", "command-equal",
                "event-equal", "repo-1", "run-1", "item-1", "effect-1",
                BindingMismatchKind.SOURCE, "same", "same", "head",
                "BINDING_MISMATCH_SOURCE",
            ).validate()

    def test_t15_persists_semantic_and_complete_policy_bindings(self) -> None:
        receipt = self.store.accept_plan(
            PlanAcceptanceRequest(
                "plan-pinned", "command-pinned", "event-pinned",
                "repo-1", "run-pinned", "item-pinned", "effect-pinned",
                "revision-pinned", "descriptor-pinned", "scope-pinned",
                "budget-pinned", ("check-b", "check-a"), ("gate-b", "gate-a"),
                source_tree_digest="source-pinned",
                item_definition_digest="item-definition-pinned",
                plan_schema_version="schema-pinned",
                reducer_version="reducer-pinned",
            ),
            expected_head="",
            writer_epoch=1,
        )
        connection = sqlite3.connect(self.database_path)
        connection.row_factory = sqlite3.Row
        try:
            columns = {
                row["name"]
                for row in connection.execute("PRAGMA table_info(validation_plans)")
            }
            row = connection.execute(
                "SELECT * FROM validation_plans WHERE plan_id = 'plan-pinned'"
            ).fetchone()
            body = json.loads(row["body_json"])
        finally:
            connection.close()
        expected_columns = {
            "source_tree_digest", "item_definition_digest",
            "plan_schema_version", "reducer_version",
            "accepted_plan_semantic_digest", "complete_policy_digest",
        }
        self.assertTrue(expected_columns.issubset(columns))
        self.assertEqual(row["source_tree_digest"], "source-pinned")
        self.assertEqual(row["item_definition_digest"], "item-definition-pinned")
        self.assertTrue(row["accepted_plan_semantic_digest"])
        self.assertTrue(row["complete_policy_digest"])
        self.assertEqual(body["failure_policy_id"], "failure-policy")
        self.assertEqual(body["failure_policy_version"], "1")
        self.oracle.allowed_head = receipt.event_hash
        catalog_head, run_heads = self.store.load_verified("repo-1")
        self.assertEqual(catalog_head, receipt.event_hash)
        self.assertEqual(run_heads["run-pinned"], receipt.event_hash)

    def test_t15_source_mismatch_atomically_fences_and_blocks_idle_run(self) -> None:
        plan = self.store.accept_plan(
            PlanAcceptanceRequest(
                "plan-1", "plan-command-1", "plan-event-1", "repo-1",
                "run-1", "item-1", "effect-1", "revision-1",
                "descriptor-digest", "scope-1", "budget-policy-digest",
                ("check-1",),
            ),
            expected_head="",
            writer_epoch=1,
        )
        self.oracle.allowed_head = plan.event_hash
        request = BindingMismatchRequest(
            "mismatch-1", "observation-1", "mismatch-command-1",
            "mismatch-event-1", "repo-1", "run-1", "item-1", "effect-1",
            BindingMismatchKind.SOURCE, "source-tree-1", "source-tree-2",
            plan.event_hash, "BINDING_MISMATCH_SOURCE",
        )
        receipt = self.store.record_binding_mismatch(
            request,
            self.authority.issue_binding_observation(request),
            self.authority,
            expected_head=plan.event_hash,
            writer_epoch=2,
        )
        self.assertEqual(receipt.resulting_state, LifecycleState.BLOCKED)
        connection = sqlite3.connect(self.database_path)
        try:
            mismatch = connection.execute(
                "SELECT mismatch_kind, fence_id FROM binding_mismatches"
            ).fetchone()
            fences = connection.execute(
                "SELECT reason_code FROM dispatch_fences"
            ).fetchall()
        finally:
            connection.close()
        self.assertEqual(mismatch[0], BindingMismatchKind.SOURCE.value)
        self.assertTrue(mismatch[1].startswith("binding:"))
        self.assertEqual(fences, [("BINDING_MISMATCH_SOURCE",)])
        self.oracle.allowed_head = receipt.event_hash
        catalog_head, run_heads = self.store.load_verified(
            "repo-1", authority=self.authority
        )
        self.assertEqual(catalog_head, receipt.event_hash)
        self.assertEqual(run_heads["run-1"], receipt.event_hash)
        readiness = self.store.evaluate_readiness(
            ReadinessEvaluationRequest(
                "readiness-after-t15", "readiness-command-after-t15",
                "readiness-event-after-t15", "repo-1", "run-1", "item-1",
                "plan-1", "revision-1", receipt.event_hash, None,
                "inputs-after-t15", True,
            )
        )
        self.assertEqual(readiness.resulting_state, LifecycleState.BLOCKED)
        self.oracle.allowed_head = readiness.event_hash
        self.store.load_verified("repo-1", authority=self.authority)

    def test_t15_exact_kind_mapping_recovery_and_observation_freshness(self) -> None:
        head = self.store.accept_plan(
            PlanAcceptanceRequest(
                "plan-1", "plan-command-1", "plan-event-1", "repo-1",
                "run-1", "item-1", "effect-1", "revision-1",
                "descriptor-digest", "scope-1", "budget-policy-digest",
                ("check-1",),
            ),
            expected_head="", writer_epoch=1,
        ).event_hash
        connection = sqlite3.connect(self.database_path)
        connection.row_factory = sqlite3.Row
        try:
            plan = connection.execute(
                "SELECT * FROM validation_plans WHERE plan_id = 'plan-1'"
            ).fetchone()
            expected_by_kind = {
                BindingMismatchKind.SOURCE: plan["source_tree_digest"],
                BindingMismatchKind.ITEM: plan["item_definition_digest"],
                BindingMismatchKind.PLAN: plan["accepted_plan_semantic_digest"],
                BindingMismatchKind.POLICY: plan["complete_policy_digest"],
            }
        finally:
            connection.close()
        first_request = None
        for index, (kind, expected) in enumerate(expected_by_kind.items(), start=2):
            self.oracle.allowed_head = head
            request = BindingMismatchRequest(
                f"mismatch-{index}", f"observation-{index}",
                f"mismatch-command-{index}", f"mismatch-event-{index}",
                "repo-1", "run-1", "item-1", "effect-1", kind,
                str(expected), f"observed-{kind.value.lower()}", head,
                f"BINDING_MISMATCH_{kind.value}",
            )
            receipt = self.store.record_binding_mismatch(
                request, self.authority.issue_binding_observation(request),
                self.authority, expected_head=head, writer_epoch=index,
            )
            self.assertEqual(receipt.resulting_state, LifecycleState.BLOCKED)
            head = receipt.event_hash
            if first_request is None:
                first_request = request
        self.oracle.allowed_head = head
        self.store.load_verified("repo-1", authority=self.authority)
        connection = sqlite3.connect(self.database_path)
        try:
            recorded_kinds = {
                row[0]
                for row in connection.execute(
                    "SELECT mismatch_kind FROM binding_mismatches"
                )
            }
        finally:
            connection.close()
        self.assertEqual(
            recorded_kinds, {kind.value for kind in BindingMismatchKind}
        )
        assert first_request is not None
        replayed_observation = replace(
            first_request,
            mismatch_id="mismatch-rebound",
            command_id="mismatch-command-rebound",
            event_id="mismatch-event-rebound",
            evidence_head=head,
        )
        with self.assertRaisesRegex(StorageIntegrityError, "identity was rebound"):
            self.store.record_binding_mismatch(
                replayed_observation,
                self.authority.issue_binding_observation(replayed_observation),
                self.authority,
                expected_head=head,
                writer_epoch=6,
            )

    def test_t15_rejects_forged_stale_and_store_unverified_mismatch(self) -> None:
        plan = self.store.accept_plan(
            PlanAcceptanceRequest(
                "plan-1", "plan-command-1", "plan-event-1", "repo-1",
                "run-1", "item-1", "effect-1", "revision-1",
                "descriptor-digest", "scope-1", "budget-policy-digest",
                ("check-1",),
            ),
            expected_head="", writer_epoch=1,
        )
        self.oracle.allowed_head = plan.event_hash
        valid = BindingMismatchRequest(
            "mismatch-1", "observation-1", "mismatch-command-1",
            "mismatch-event-1", "repo-1", "run-1", "item-1", "effect-1",
            BindingMismatchKind.SOURCE, "source-tree-1", "source-tree-2",
            plan.event_hash, "BINDING_MISMATCH_SOURCE",
        )
        connection = sqlite3.connect(self.database_path)
        try:
            before = tuple(connection.iterdump())
        finally:
            connection.close()
        forged = replace(
            self.authority.issue_binding_observation(valid), issuer_mac="0" * 64
        )
        with self.assertRaisesRegex(DispatchDenied, "not issued here"):
            self.store.record_binding_mismatch(
                valid, forged, self.authority,
                expected_head=plan.event_hash, writer_epoch=2,
            )
        cross_bound = replace(
            valid, mismatch_id="mismatch-cross", command_id="command-cross",
            event_id="event-cross", observed_digest="source-tree-cross",
        )
        with self.assertRaisesRegex(DispatchDenied, "not issued here"):
            self.store.record_binding_mismatch(
                cross_bound,
                self.authority.issue_binding_observation(valid),
                self.authority,
                expected_head=plan.event_hash,
                writer_epoch=2,
            )
        wrong_expected = replace(
            valid, mismatch_id="mismatch-2", observation_id="observation-2",
            command_id="mismatch-command-2", event_id="mismatch-event-2",
            expected_digest="caller-invented-binding",
        )
        with self.assertRaisesRegex(DispatchDenied, "accepted binding"):
            self.store.record_binding_mismatch(
                wrong_expected,
                self.authority.issue_binding_observation(wrong_expected),
                self.authority,
                expected_head=plan.event_hash, writer_epoch=2,
            )
        stale = replace(
            valid, mismatch_id="mismatch-3", observation_id="observation-3",
            command_id="mismatch-command-3", event_id="mismatch-event-3",
            evidence_head="stale-head",
        )
        with self.assertRaisesRegex(DispatchDenied, "evidence head is stale"):
            self.store.record_binding_mismatch(
                stale, self.authority.issue_binding_observation(stale),
                self.authority,
                expected_head="stale-head", writer_epoch=2,
            )
        foreign_item = replace(
            valid, mismatch_id="mismatch-foreign",
            observation_id="observation-foreign",
            command_id="command-foreign", event_id="event-foreign",
            item_id="item-foreign",
        )
        with self.assertRaisesRegex(DispatchDenied, "accepted plan"):
            self.store.record_binding_mismatch(
                foreign_item,
                self.authority.issue_binding_observation(foreign_item),
                self.authority,
                expected_head=plan.event_hash,
                writer_epoch=2,
            )
        connection = sqlite3.connect(self.database_path)
        try:
            after = tuple(connection.iterdump())
        finally:
            connection.close()
        self.assertEqual(after, before)

    def test_t15_recovery_rejects_rehashed_forged_observation(self) -> None:
        plan = self.store.accept_plan(
            PlanAcceptanceRequest(
                "plan-1", "plan-command-1", "plan-event-1", "repo-1",
                "run-1", "item-1", "effect-1", "revision-1",
                "descriptor-digest", "scope-1", "budget-policy-digest",
                ("check-1",),
            ),
            expected_head="", writer_epoch=1,
        )
        self.oracle.allowed_head = plan.event_hash
        request = BindingMismatchRequest(
            "mismatch-1", "observation-1", "mismatch-command-1",
            "mismatch-event-1", "repo-1", "run-1", "item-1", "effect-1",
            BindingMismatchKind.SOURCE, "source-tree-1", "source-tree-2",
            plan.event_hash, "BINDING_MISMATCH_SOURCE",
        )
        receipt = self.store.record_binding_mismatch(
            request, self.authority.issue_binding_observation(request),
            self.authority,
            expected_head=plan.event_hash, writer_epoch=2,
        )
        connection = sqlite3.connect(self.database_path)
        try:
            body = json.loads(
                connection.execute(
                    "SELECT body_json FROM events WHERE event_id = ?",
                    (request.event_id,),
                ).fetchone()[0]
            )
            body["observation_issuer_mac"] = "0" * 64
            body_json = json.dumps(body, sort_keys=True, separators=(",", ":"))
            forged_hash = self.store._event_hash(body)
            connection.execute(
                "UPDATE events SET event_hash = ?, body_json = ? WHERE event_id = ?",
                (forged_hash, body_json, request.event_id),
            )
            connection.execute(
                "UPDATE binding_mismatches SET issuer_mac = ?, event_hash = ?, "
                "body_json = ? WHERE mismatch_id = ?",
                ("0" * 64, forged_hash, body_json, request.mismatch_id),
            )
            connection.execute(
                "UPDATE command_outcomes SET event_hash = ? WHERE command_id = ?",
                (forged_hash, request.command_id),
            )
            connection.execute(
                "UPDATE runs SET head_hash = ? WHERE run_id = ?",
                (forged_hash, request.run_id),
            )
            connection.execute(
                "UPDATE repositories SET catalog_head = ? WHERE repository_id = ?",
                (forged_hash, request.repository_id),
            )
            connection.commit()
        finally:
            connection.close()
        self.assertNotEqual(forged_hash, receipt.event_hash)
        self.oracle.allowed_head = forged_hash
        with self.assertRaisesRegex(
            StorageIntegrityError, "binding mismatch proof or schema"
        ):
            self.store.load_verified("repo-1", authority=self.authority)

    def test_t15_recovery_rederives_plan_and_policy_digests(self) -> None:
        receipt = self.store.accept_plan(
            PlanAcceptanceRequest(
                "plan-1", "plan-command-1", "plan-event-1", "repo-1",
                "run-1", "item-1", "effect-1", "revision-1",
                "descriptor-digest", "scope-1", "budget-policy-digest",
                ("check-1",),
            ),
            expected_head="", writer_epoch=1,
        )
        connection = sqlite3.connect(self.database_path)
        connection.row_factory = sqlite3.Row
        try:
            plan = connection.execute(
                "SELECT * FROM validation_plans WHERE plan_id = 'plan-1'"
            ).fetchone()
            original_body_json = plan["body_json"]
            original_body = json.loads(original_body_json)
            original_values = {
                "accepted_plan_semantic_digest": plan[
                    "accepted_plan_semantic_digest"
                ],
                "complete_policy_digest": plan["complete_policy_digest"],
            }
        finally:
            connection.close()
        for field in original_values:
            with self.subTest(field=field):
                forged_body = dict(original_body)
                forged_body[field] = f"forged-{field}"
                forged_body_json = json.dumps(
                    forged_body, sort_keys=True, separators=(",", ":")
                )
                forged_hash = self.store._event_hash(forged_body)
                connection = sqlite3.connect(self.database_path)
                try:
                    connection.execute(
                        "UPDATE events SET event_hash = ?, body_json = ? "
                        "WHERE event_id = 'plan-event-1'",
                        (forged_hash, forged_body_json),
                    )
                    connection.execute(
                        f"UPDATE validation_plans SET {field} = ?, "
                        "event_hash = ?, body_json = ? WHERE plan_id = 'plan-1'",
                        (forged_body[field], forged_hash, forged_body_json),
                    )
                    connection.execute(
                        "UPDATE command_outcomes SET event_hash = ? "
                        "WHERE command_id = 'plan-command-1'",
                        (forged_hash,),
                    )
                    connection.execute(
                        "UPDATE runs SET head_hash = ? WHERE run_id = 'run-1'",
                        (forged_hash,),
                    )
                    connection.execute(
                        "UPDATE repositories SET catalog_head = ? "
                        "WHERE repository_id = 'repo-1'",
                        (forged_hash,),
                    )
                    connection.commit()
                finally:
                    connection.close()
                self.oracle.allowed_head = forged_hash
                with self.assertRaisesRegex(
                    StorageIntegrityError,
                    "plan (semantic|policy) digest diverges",
                ):
                    self.store.load_verified("repo-1", authority=self.authority)
                connection = sqlite3.connect(self.database_path)
                try:
                    connection.execute(
                        "UPDATE events SET event_hash = ?, body_json = ? "
                        "WHERE event_id = 'plan-event-1'",
                        (receipt.event_hash, original_body_json),
                    )
                    connection.execute(
                        f"UPDATE validation_plans SET {field} = ?, "
                        "event_hash = ?, body_json = ? WHERE plan_id = 'plan-1'",
                        (
                            original_values[field], receipt.event_hash,
                            original_body_json,
                        ),
                    )
                    connection.execute(
                        "UPDATE command_outcomes SET event_hash = ? "
                        "WHERE command_id = 'plan-command-1'",
                        (receipt.event_hash,),
                    )
                    connection.execute(
                        "UPDATE runs SET head_hash = ? WHERE run_id = 'run-1'",
                        (receipt.event_hash,),
                    )
                    connection.execute(
                        "UPDATE repositories SET catalog_head = ? "
                        "WHERE repository_id = 'repo-1'",
                        (receipt.event_hash,),
                    )
                    connection.commit()
                finally:
                    connection.close()
                self.oracle.allowed_head = receipt.event_hash
                self.store.load_verified("repo-1", authority=self.authority)

    def test_t15_crash_replay_is_atomic_and_preserves_effect_identity(self) -> None:
        plan = self.store.accept_plan(
            PlanAcceptanceRequest(
                "plan-1", "plan-command-1", "plan-event-1", "repo-1",
                "run-1", "item-1", "effect-1", "revision-1",
                "descriptor-digest", "scope-1", "budget-policy-digest",
                ("check-1",),
            ),
            expected_head="", writer_epoch=1,
        )
        self.oracle.allowed_head = plan.event_hash
        request = BindingMismatchRequest(
            "mismatch-1", "observation-1", "mismatch-command-1",
            "mismatch-event-1", "repo-1", "run-1", "item-1", "effect-1",
            BindingMismatchKind.ITEM, "item-definition-1", "item-definition-2",
            plan.event_hash, "BINDING_MISMATCH_ITEM",
        )
        observation = self.authority.issue_binding_observation(request)
        connection = sqlite3.connect(self.database_path)
        try:
            immutable_before = {
                table: tuple(connection.execute(f"SELECT * FROM {table}"))
                for table in (
                    "validation_plans", "validation_requirements", "effects",
                    "permission_uses", "budget_reservations", "outstanding_slot",
                )
            }
            database_before = tuple(connection.iterdump())
        finally:
            connection.close()
        with self.assertRaises(InjectedFailure):
            self.store.record_binding_mismatch(
                request, observation, self.authority,
                expected_head=plan.event_hash, writer_epoch=2,
                failure_hook=raise_at(
                    "after_binding_mismatch_writes_before_commit"
                ),
            )
        connection = sqlite3.connect(self.database_path)
        try:
            self.assertEqual(tuple(connection.iterdump()), database_before)
        finally:
            connection.close()
        with self.assertRaises(InjectedFailure):
            self.store.record_binding_mismatch(
                request, observation, self.authority,
                expected_head=plan.event_hash, writer_epoch=2,
                failure_hook=raise_at(
                    "after_binding_mismatch_commit_before_acknowledgement"
                ),
            )
        connection = sqlite3.connect(self.database_path)
        try:
            committed_head = connection.execute(
                "SELECT head_hash FROM runs WHERE run_id = 'run-1'"
            ).fetchone()[0]
            immutable_after = {
                table: tuple(connection.execute(f"SELECT * FROM {table}"))
                for table in immutable_before
            }
        finally:
            connection.close()
        self.assertEqual(immutable_after, immutable_before)
        self.oracle.allowed_head = committed_head
        replay = self.store.record_binding_mismatch(
            request, observation, self.authority,
            expected_head=plan.event_hash, writer_epoch=2,
        )
        self.assertTrue(replay.replayed)
        self.assertEqual(replay.event_hash, committed_head)
        with self.assertRaisesRegex(DispatchDenied, "durable PLANNED state"):
            self.store.commit_intent(
                self.request(), self.capability, self.authority,
                expected_head=committed_head, writer_epoch=3,
            )

    def test_t15_partial_plan_binding_schema_is_rejected_without_completion(self) -> None:
        connection = sqlite3.connect(self.database_path)
        try:
            connection.execute(
                "ALTER TABLE validation_plans DROP COLUMN complete_policy_digest"
            )
            connection.commit()
            before_columns = tuple(
                row[1]
                for row in connection.execute(
                    "PRAGMA table_info(validation_plans)"
                )
            )
        finally:
            connection.close()
        with self.assertRaisesRegex(StorageIntegrityError, "partially migrated"):
            SQLiteStateStore(self.database_path, self.oracle, "repo-1")
        connection = sqlite3.connect(self.database_path)
        try:
            after_columns = tuple(
                row[1]
                for row in connection.execute(
                    "PRAGMA table_info(validation_plans)"
                )
            )
        finally:
            connection.close()
        self.assertEqual(after_columns, before_columns)

    def test_t15_active_mismatch_reconciles_without_changing_effect_or_slot(self) -> None:
        committed = self._commit_planned_intent(
            self.request(), self.capability, self.authority,
            expected_head="", writer_epoch=1,
        )
        self.oracle.allowed_head = committed.event_hash
        connection = sqlite3.connect(self.database_path)
        try:
            effects_before = tuple(connection.execute("SELECT * FROM effects"))
            slot_before = tuple(
                connection.execute("SELECT * FROM outstanding_slot")
            )
            plan_before = tuple(
                connection.execute("SELECT * FROM validation_plans")
            )
        finally:
            connection.close()
        request = BindingMismatchRequest(
            "mismatch-active", "observation-active", "command-active",
            "event-active", "repo-1", "run-1", "item-1", "effect-1",
            BindingMismatchKind.SOURCE, "source-tree-1", "source-tree-2",
            committed.event_hash, "BINDING_MISMATCH_SOURCE",
        )
        receipt = self.store.record_binding_mismatch(
            request, self.authority.issue_binding_observation(request),
            self.authority,
            expected_head=committed.event_hash, writer_epoch=3,
        )
        self.assertEqual(
            receipt.resulting_state, LifecycleState.RECONCILIATION_REQUIRED
        )
        connection = sqlite3.connect(self.database_path)
        try:
            self.assertEqual(
                tuple(connection.execute("SELECT * FROM effects")),
                effects_before,
            )
            self.assertEqual(
                tuple(connection.execute("SELECT * FROM outstanding_slot")),
                slot_before,
            )
            self.assertEqual(
                tuple(connection.execute("SELECT * FROM validation_plans")),
                plan_before,
            )
        finally:
            connection.close()

    def test_t15_lifecycle_route_is_closed_and_preserves_paused(self) -> None:
        expected = {
            LifecycleState.PLANNED: LifecycleState.BLOCKED,
            LifecycleState.BLOCKED: LifecycleState.BLOCKED,
            LifecycleState.PAUSED: LifecycleState.PAUSED,
            LifecycleState.RUNNING: LifecycleState.RECONCILIATION_REQUIRED,
            LifecycleState.PAUSING: LifecycleState.RECONCILIATION_REQUIRED,
            LifecycleState.VALIDATING: LifecycleState.RECONCILIATION_REQUIRED,
            LifecycleState.RECONCILIATION_REQUIRED: (
                LifecycleState.RECONCILIATION_REQUIRED
            ),
        }
        for current, resulting in expected.items():
            with self.subTest(current=current):
                self.assertEqual(
                    self.store._binding_mismatch_route(
                        current, active_or_uncertain=False
                    ),
                    resulting,
                )
        self.assertEqual(
            self.store._binding_mismatch_route(
                LifecycleState.BLOCKED, active_or_uncertain=True
            ),
            LifecycleState.RECONCILIATION_REQUIRED,
        )
        for terminal in (
            LifecycleState.COMPLETED,
            LifecycleState.FAILED_FINAL,
            LifecycleState.STOPPED,
        ):
            with self.subTest(terminal=terminal):
                with self.assertRaisesRegex(DispatchDenied, "nonterminal"):
                    self.store._binding_mismatch_route(
                        terminal, active_or_uncertain=False
                    )

    def test_t15_blocked_owned_slot_routes_to_reconciliation(self) -> None:
        self._prepare_finalization()
        connection = sqlite3.connect(self.database_path)
        try:
            state_before = connection.execute(
                "SELECT lifecycle_state, continuation_cursor, head_hash "
                "FROM runs WHERE run_id = 'run-1'"
            ).fetchone()
            writer_epoch = connection.execute(
                "SELECT MAX(writer_epoch) + 1 FROM events"
            ).fetchone()[0]
            slot_before = tuple(
                connection.execute("SELECT * FROM outstanding_slot")
            )
        finally:
            connection.close()
        self.assertEqual(state_before[:2], ("BLOCKED", "FINALIZING"))
        self.assertEqual(len(slot_before), 1)
        request = BindingMismatchRequest(
            "mismatch-blocked", "observation-blocked", "command-blocked",
            "event-blocked", "repo-1", "run-1", "item-1", "effect-1",
            BindingMismatchKind.SOURCE, "source-tree-1", "source-tree-2",
            state_before[2], "BINDING_MISMATCH_SOURCE",
        )
        observation = self.authority.issue_binding_observation(request)
        with self.assertRaises(InjectedFailure):
            self.store.record_binding_mismatch(
                request, observation, self.authority,
                expected_head=state_before[2], writer_epoch=writer_epoch,
                failure_hook=raise_at(
                    "after_binding_mismatch_writes_before_commit"
                ),
            )
        self.assertEqual(
            self.store.load_run_lifecycle("run-1"), LifecycleState.BLOCKED
        )
        receipt = self.store.record_binding_mismatch(
            request, observation, self.authority,
            expected_head=state_before[2], writer_epoch=writer_epoch,
        )
        self.assertEqual(
            receipt.resulting_state, LifecycleState.RECONCILIATION_REQUIRED
        )
        connection = sqlite3.connect(self.database_path)
        try:
            state_after = connection.execute(
                "SELECT lifecycle_state, continuation_cursor FROM runs "
                "WHERE run_id = 'run-1'"
            ).fetchone()
            slot_after = tuple(
                connection.execute("SELECT * FROM outstanding_slot")
            )
        finally:
            connection.close()
        self.assertEqual(
            state_after, ("RECONCILIATION_REQUIRED", "FINALIZING")
        )
        self.assertEqual(slot_after, slot_before)
        self.oracle.allowed_head = receipt.event_hash
        self.store.load_verified("repo-1", authority=self.authority)

    def test_t15_paused_run_retains_pause_and_terminal_run_rejects(self) -> None:
        plan = self.store.accept_plan(
            PlanAcceptanceRequest(
                "plan-1", "plan-command-1", "plan-event-1", "repo-1",
                "run-1", "item-1", "effect-1", "revision-1",
                "descriptor-digest", "scope-1", "budget-policy-digest",
                ("check-1",),
            ),
            expected_head="", writer_epoch=1,
        )
        self.oracle.allowed_head = plan.event_hash
        paused = self.store.pause_before_dispatch(
            self._pause_request("t15"), self._pause_capability("t15"),
            self.authority,
        )
        self.oracle.allowed_head = paused.event_hash
        request = BindingMismatchRequest(
            "mismatch-paused", "observation-paused", "command-paused",
            "event-paused", "repo-1", "run-1", "item-1", "effect-1",
            BindingMismatchKind.SOURCE, "source-tree-1", "source-tree-2",
            paused.event_hash, "BINDING_MISMATCH_SOURCE",
        )
        mismatch = self.store.record_binding_mismatch(
            request, self.authority.issue_binding_observation(request),
            self.authority,
            expected_head=paused.event_hash, writer_epoch=3,
        )
        self.assertEqual(mismatch.resulting_state, LifecycleState.PAUSED)
        self.oracle.allowed_head = mismatch.event_hash
        stopped = self.store.stop(
            self._stop_request(StopMode.IMMEDIATE, "t15"),
            self._stop_capability(StopMode.IMMEDIATE, "t15"),
            self.authority,
        )
        self.oracle.allowed_head = stopped.event_hash
        connection = sqlite3.connect(self.database_path)
        try:
            policy_digest = connection.execute(
                "SELECT complete_policy_digest FROM validation_plans "
                "WHERE plan_id = 'plan-1'"
            ).fetchone()[0]
        finally:
            connection.close()
        terminal_request = BindingMismatchRequest(
            "mismatch-terminal", "observation-terminal", "command-terminal",
            "event-terminal", "repo-1", "run-1", "item-1", "effect-1",
            BindingMismatchKind.POLICY,
            policy_digest,
            "changed-policy", stopped.event_hash, "BINDING_MISMATCH_POLICY",
        )
        connection = sqlite3.connect(self.database_path)
        try:
            before = tuple(connection.iterdump())
        finally:
            connection.close()
        with self.assertRaisesRegex(DispatchDenied, "nonterminal"):
            self.store.record_binding_mismatch(
                terminal_request,
                self.authority.issue_binding_observation(terminal_request),
                self.authority,
                expected_head=stopped.event_hash,
                writer_epoch=5,
            )
        connection = sqlite3.connect(self.database_path)
        try:
            after = tuple(connection.iterdump())
        finally:
            connection.close()
        self.assertEqual(after, before)

    def test_t03_requires_exact_accepted_plan_and_rejects_run_substitution(self) -> None:
        connection = sqlite3.connect(self.database_path)
        try:
            empty_state = tuple(connection.iterdump())
        finally:
            connection.close()
        with self.assertRaisesRegex(DispatchDenied, "accepted plan"):
            self.store.commit_intent(
                self.request(), self.capability, self.authority,
                expected_head="", writer_epoch=1,
            )
        connection = sqlite3.connect(self.database_path)
        try:
            after_missing_plan = tuple(connection.iterdump())
        finally:
            connection.close()
        self.assertEqual(after_missing_plan, empty_state)

        plan = self.store.accept_plan(
            PlanAcceptanceRequest(
                "plan-1", "plan-command-1", "plan-event-1", "repo-1",
                "run-1", "item-1", "effect-1", "revision-1",
                "descriptor-digest", "scope-1", "budget-policy-digest",
                ("check-1",),
            ),
            expected_head="", writer_epoch=1,
        )
        self.oracle.allowed_head = plan.event_hash
        alternate_grant = SyntheticGrant(
            "grant-plan-scope", "repo-1", "effect-1", "attempt-1", "scope-2"
        )
        self.authority.register(alternate_grant)
        alternate_capability = self.authority.claim(
            *alternate_grant.__dict__.values()
        )
        for changed_request, changed_capability in (
            (
                replace(
                    self.request(), effect_descriptor_digest="descriptor-revision-2"
                ),
                self.capability,
            ),
            (
                replace(self.request(), budget_policy_digest="budget-revision-2"),
                self.capability,
            ),
            (self.request(), alternate_capability),
        ):
            connection = sqlite3.connect(self.database_path)
            try:
                before_pin_denial = tuple(connection.iterdump())
            finally:
                connection.close()
            with self.assertRaisesRegex(DispatchDenied, "execution pins"):
                self.store.commit_intent(
                    changed_request, changed_capability, self.authority,
                    expected_head=plan.event_hash, writer_epoch=2,
                )
            connection = sqlite3.connect(self.database_path)
            try:
                after_pin_denial = tuple(connection.iterdump())
            finally:
                connection.close()
            self.assertEqual(after_pin_denial, before_pin_denial)

        substituted = replace(
            self.request(), run_id="run-2", item_id="item-2",
            command_id="command-2", event_id="event-2",
        )
        connection = sqlite3.connect(self.database_path)
        try:
            before_substitution = tuple(connection.iterdump())
        finally:
            connection.close()
        with self.assertRaisesRegex(DispatchDenied, "accepted plan"):
            self.store.commit_intent(
                substituted, self.capability, self.authority,
                expected_head=plan.event_hash, writer_epoch=2,
            )
        connection = sqlite3.connect(self.database_path)
        try:
            after_substitution = tuple(connection.iterdump())
        finally:
            connection.close()
        self.assertEqual(after_substitution, before_substitution)

        committed = self.store.commit_intent(
            self.request(), self.capability, self.authority,
            expected_head=plan.event_hash, writer_epoch=2,
        )
        connection = sqlite3.connect(self.database_path)
        try:
            body = json.loads(
                connection.execute(
                    "SELECT body_json FROM events WHERE event_id = 'event-1'"
                ).fetchone()[0]
            )
        finally:
            connection.close()
        self.assertEqual(body["plan_id"], "plan-1")
        self.assertEqual(body["revision_digest"], "revision-1")
        self.assertEqual(committed.sequence, 2)

    def test_intent_commit_is_atomic_and_replay_is_idempotent(self) -> None:
        first = self._commit_planned_intent(
            self.request(), self.capability, self.authority, expected_head="", writer_epoch=1
        )
        self.oracle.allowed_head = first.event_hash
        replay = self._commit_planned_intent(
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
                "validation_plans": 1,
                "validation_requirements": 1,
                "readiness_evaluations": 0,
                "events": 2,
                "command_outcomes": 2,
                "effects": 1,
                "permission_uses": 1,
                "capability_redemptions": 1,
                "budget_reservations": 1,
                "budget_settlements": 0,
                "effect_observations": 0,
                "validator_intents": 0,
                "validator_observations": 0,
                "validator_cessations": 0,
                "validation_applications": 0,
                "validation_recoveries": 0,
                "terminal_validation_settlements": 0,
                "operation_finalizations": 0,
                "operation_launches": 0,
                "control_actions": 0,
                "local_pause_actions": 0,
                "external_pause_actions": 0,
                "reconciliation_pause_actions": 0,
                "uncertainty_instances": 0,
                "uncertainty_resolutions": 0,
                "reconciliation_actions": 0,
                "verified_receipt_reconciliation_actions": 0,
                "proven_nonexecution_actions": 0,
                "operation_nonexecution_resume_actions": 0,
                "operation_recovery_actions": 0,
                "operation_retry_authorizations": 0,
                "validation_pause_actions": 0,
                "resume_actions": 0,
                "reconciliation_resume_actions": 0,
                "stop_actions": 0,
                "stop_escalations": 0,
                "operator_redemptions": 0,
                "outstanding_slot": 1,
                "dispatch_fences": 0,
                "binding_mismatches": 0,
            },
        )

    def test_recovery_rejects_tampered_operation_launch_projection(self) -> None:
        committed = self._commit_planned_intent(
            self.request(), self.capability, self.authority,
            expected_head="", writer_epoch=1,
        )
        self.oracle.allowed_head = committed.event_hash
        connection = sqlite3.connect(self.database_path)
        try:
            before_rebound = tuple(connection.iterdump())
        finally:
            connection.close()
        with self.assertRaisesRegex(DispatchDenied, "changed the durable intent"):
            self.store.claim_operation_launch(
                replace(self.request(), item_id="item-2"), committed
            )
        connection = sqlite3.connect(self.database_path)
        try:
            after_rebound = tuple(connection.iterdump())
        finally:
            connection.close()
        self.assertEqual(after_rebound, before_rebound)
        launched = self.store.claim_operation_launch(self.request(), committed)
        self.oracle.allowed_head = launched.event_hash
        baseline_path = (
            Path(self.temporary_directory.name) / "launch-baseline.sqlite3"
        )
        shutil.copy2(self.database_path, baseline_path)
        tamper_cases = (
            (
                "delete",
                "DELETE FROM operation_launches WHERE launch_id = ?",
                (launched.launch_id,),
            ),
            (
                "body",
                "UPDATE operation_launches SET body_json = '{}' "
                "WHERE launch_id = ?",
                (launched.launch_id,),
            ),
            (
                "event-link",
                "UPDATE operation_launches SET intent_event_id = 'other-event' "
                "WHERE launch_id = ?",
                (launched.launch_id,),
            ),
            (
                "cross-run",
                "UPDATE operation_launches SET run_id = 'other-run' "
                "WHERE launch_id = ?",
                (launched.launch_id,),
            ),
            (
                "extra-row",
                "INSERT INTO operation_launches SELECT launch_id || ':extra', "
                "event_id || ':extra', repository_id, run_id, item_id, "
                "logical_effect_id || ':extra', attempt_id || ':extra', "
                "capability_claim_id || ':extra', "
                "intent_event_id, intent_event_hash, 'extra-hash', '{}' "
                "FROM operation_launches WHERE launch_id = ?",
                (launched.launch_id,),
            ),
        )
        for name, statement, parameters in tamper_cases:
            with self.subTest(name=name):
                test_path = (
                    Path(self.temporary_directory.name)
                    / f"launch-tamper-{name}.sqlite3"
                )
                shutil.copy2(baseline_path, test_path)
                connection = sqlite3.connect(test_path)
                try:
                    connection.execute(statement, parameters)
                    connection.commit()
                finally:
                    connection.close()
                with self.assertRaisesRegex(
                    StorageIntegrityError, "operation-launch projection"
                ):
                    SQLiteStateStore(
                        test_path, self.oracle, "repo-1"
                    ).load_verified("repo-1")

    def test_contact_claim_without_target_receipt_denies_redispatch(self) -> None:
        committed = self._commit_planned_intent(
            self.request(), self.capability, self.authority,
            expected_head="", writer_epoch=1,
        )
        self.oracle.allowed_head = committed.event_hash
        launch = self.store.claim_operation_launch(self.request(), committed)
        self.oracle.allowed_head = launch.event_hash

        self.store._contact_claimed_operation(
            self.request(), self.capability, committed, launch,
            self.store._adapter_target_digest("repo-1", "EFFECT"),
        )
        connection = sqlite3.connect(self.database_path)
        try:
            contact_count, contact_head = connection.execute(
                "SELECT COUNT(*), MAX(event_hash) FROM adapter_contacts"
            ).fetchone()
        finally:
            connection.close()
        self.assertEqual(contact_count, 1)
        self.oracle.allowed_head = contact_head
        with self.assertRaisesRegex(DispatchDenied, "already claimed"):
            self.store._contact_claimed_operation(
                self.request(), self.capability, committed, launch,
                self.store._adapter_target_digest("repo-1", "EFFECT"),
            )
        self.store.load_verified("repo-1")
        connection = sqlite3.connect(self.database_path)
        try:
            connection.execute("DELETE FROM adapter_contacts")
            connection.commit()
        finally:
            connection.close()
        with self.assertRaisesRegex(StorageIntegrityError, "contact projection"):
            self.store.load_verified("repo-1")

    def test_f04_unknown_usage_charges_worst_case_and_retains_slot(self) -> None:
        committed = self._commit_planned_intent(self.request(), self.capability, self.authority, expected_head="", writer_epoch=1)
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
            request,
        )
        receipt = self.store._settle_budget(request, proof, self.authority)
        self.assertEqual(receipt.charged_units, 5)
        self.assertTrue(receipt.uncertainty)
        self.assertEqual(self.store.table_counts()["outstanding_slot"], 1)

    def test_recovery_derives_settlement_charges_instead_of_trusting_event(
        self,
    ) -> None:
        committed = self._commit_planned_intent(
            self.request(), self.capability, self.authority,
            expected_head="", writer_epoch=1,
        )
        self.oracle.allowed_head = committed.event_hash
        request = BudgetSettlementRequest(
            "settlement-1", "reservation-1", "",
            BudgetDisposition.UNKNOWN_WORST_CASE_CHARGED, None,
            "missing-telemetry", "USAGE_UNKNOWN",
        )
        receipt = self.store._settle_budget(
            request,
            self.authority.issue_settlement_proof("proof-1", request),
            self.authority,
        )
        connection = sqlite3.connect(self.database_path)
        connection.row_factory = sqlite3.Row
        try:
            body = json.loads(
                connection.execute(
                    "SELECT body_json FROM budget_settlements WHERE "
                    "settlement_event_id = 'settlement-1'"
                ).fetchone()["body_json"]
            )
            body["charged_units"] = 1
            event_hash = self.store._event_hash(body)
            body_json = json.dumps(
                body, sort_keys=True, separators=(",", ":")
            )
            connection.execute(
                "UPDATE budget_settlements SET charged_units = 1, "
                "settlement_hash = ?, body_json = ? WHERE "
                "settlement_event_id = 'settlement-1'",
                (event_hash, body_json),
            )
            connection.execute(
                "UPDATE budget_reservations SET charged_units = 1, "
                "settlement_head_hash = ? WHERE reservation_id = 'reservation-1'",
                (event_hash,),
            )
            connection.execute(
                "UPDATE events SET event_hash = ?, body_json = ? WHERE "
                "event_id = 'settlement-1'",
                (event_hash, body_json),
            )
            connection.execute(
                "UPDATE runs SET head_hash = ? WHERE run_id = 'run-1'",
                (event_hash,),
            )
            connection.execute(
                "UPDATE repositories SET catalog_head = ? WHERE "
                "repository_id = 'repo-1'",
                (event_hash,),
            )
            connection.commit()
        finally:
            connection.close()
        self.oracle.allowed_head = event_hash

        with self.assertRaisesRegex(
            StorageIntegrityError, "settlement accounting semantics"
        ):
            self.store.load_verified("repo-1")

    def test_recovery_derives_effect_receipt_lifecycle_routing(self) -> None:
        observation = self._record_effect_observation()
        connection = sqlite3.connect(self.database_path)
        connection.row_factory = sqlite3.Row
        try:
            body = json.loads(
                connection.execute(
                    "SELECT body_json FROM effect_observations WHERE "
                    "observation_id = 'observation-1'"
                ).fetchone()["body_json"]
            )
            body["lifecycle_to"] = LifecycleState.COMPLETED.value
            event_hash = self.store._event_hash(body)
            body_json = json.dumps(
                body, sort_keys=True, separators=(",", ":")
            )
            connection.execute(
                "UPDATE effect_observations SET resulting_state = 'COMPLETED', "
                "event_hash = ?, body_json = ? WHERE observation_id = "
                "'observation-1'",
                (event_hash, body_json),
            )
            connection.execute(
                "UPDATE events SET event_hash = ?, body_json = ? WHERE "
                "event_id = 'observation-event-1'",
                (event_hash, body_json),
            )
            connection.execute(
                "UPDATE command_outcomes SET event_hash = ? WHERE "
                "command_id = 'observe-command-1'",
                (event_hash,),
            )
            connection.execute(
                "UPDATE runs SET lifecycle_state = 'COMPLETED', head_hash = ? "
                "WHERE run_id = 'run-1'",
                (event_hash,),
            )
            connection.execute(
                "UPDATE repositories SET catalog_head = ? WHERE "
                "repository_id = 'repo-1'",
                (event_hash,),
            )
            connection.commit()
        finally:
            connection.close()
        self.oracle.allowed_head = event_hash

        with self.assertRaisesRegex(
            StorageIntegrityError, "effect observation semantics"
        ):
            self.store.load_verified("repo-1")

    def test_recovery_derives_contradiction_fence_from_prior_evidence(self) -> None:
        committed = self._commit_planned_intent(
            self.request(), self.capability, self.authority,
            expected_head="", writer_epoch=1,
        )
        self.oracle.allowed_head = committed.event_hash
        request = BudgetSettlementRequest(
            "settlement-1", "reservation-1", "",
            BudgetDisposition.UNKNOWN_WORST_CASE_CHARGED, None,
            "missing-telemetry", "USAGE_UNKNOWN",
        )
        self.store._settle_budget(
            request,
            self.authority.issue_settlement_proof("proof-1", request),
            self.authority,
        )
        connection = sqlite3.connect(self.database_path)
        connection.row_factory = sqlite3.Row
        try:
            body = json.loads(
                connection.execute(
                    "SELECT body_json FROM budget_settlements WHERE "
                    "settlement_event_id = 'settlement-1'"
                ).fetchone()["body_json"]
            )
            body["contradiction"] = True
            event_hash = self.store._event_hash(body)
            body_json = json.dumps(
                body, sort_keys=True, separators=(",", ":")
            )
            connection.execute(
                "UPDATE budget_settlements SET settlement_hash = ?, "
                "body_json = ? WHERE settlement_event_id = 'settlement-1'",
                (event_hash, body_json),
            )
            connection.execute(
                "UPDATE budget_reservations SET settlement_head_hash = ? "
                "WHERE reservation_id = 'reservation-1'",
                (event_hash,),
            )
            connection.execute(
                "UPDATE events SET event_hash = ?, body_json = ? WHERE "
                "event_id = 'settlement-1'",
                (event_hash, body_json),
            )
            connection.execute(
                "INSERT INTO dispatch_fences VALUES (?, ?, ?, ?, ?, ?)",
                (
                    "nonexecution-contradiction:settlement-1", "repo-1",
                    "item-1", "effect-1", "NONEXECUTION_CONTRADICTION",
                    "settlement-1",
                ),
            )
            connection.execute(
                "UPDATE runs SET head_hash = ? WHERE run_id = 'run-1'",
                (event_hash,),
            )
            connection.execute(
                "UPDATE repositories SET catalog_head = ? WHERE "
                "repository_id = 'repo-1'",
                (event_hash,),
            )
            connection.commit()
        finally:
            connection.close()
        self.oracle.allowed_head = event_hash

        with self.assertRaisesRegex(
            StorageIntegrityError, "settlement contradiction semantics"
        ):
            self.store.load_verified("repo-1")

    def test_settlement_proof_rejects_cross_domain_delimiter_collision(self) -> None:
        authority = SyntheticAuthority(b"a" * 32)
        grant = SyntheticGrant(
            "grant-1", "repo-1", "1", "1", "1"
        )
        authority.register(grant)
        capability = authority.claim(*grant.__dict__.values())
        forged = SyntheticSettlementProof(
            capability.claim_id,
            "grant-1\0repo-1",
            True,
            True,
            True,
            capability.issuer_mac,
            capability.issuer_mac,
        )

        with self.assertRaisesRegex(DispatchDenied, "was not issued here"):
            authority.verify_settlement_proof(
                forged,
                BudgetSettlementRequest(
                    "settlement-1", "reservation-1", "",
                    BudgetDisposition.CONSUMED, 1, "evidence-1", "USAGE_REPORTED",
                ),
            )

    def test_settlement_proof_rejects_altered_request(self) -> None:
        request = BudgetSettlementRequest(
            "settlement-1", "reservation-1", "",
            BudgetDisposition.CONSUMED, 1, "evidence-1", "USAGE_REPORTED",
        )
        proof = self.authority.issue_settlement_proof("proof-1", request)
        altered = BudgetSettlementRequest(
            **{**request.__dict__, "actual_units": 2}
        )

        with self.assertRaisesRegex(DispatchDenied, "was not issued here"):
            self.authority.verify_settlement_proof(proof, altered)

    def test_settlement_proof_binds_every_request_field_without_state_change(self) -> None:
        committed = self._commit_planned_intent(
            self.request(), self.capability, self.authority,
            expected_head="", writer_epoch=1,
        )
        self.oracle.allowed_head = committed.event_hash
        request = BudgetSettlementRequest(
            "settlement-1", "reservation-1", "",
            BudgetDisposition.UNKNOWN_WORST_CASE_CHARGED, None,
            "evidence-1", "USAGE_UNKNOWN",
        )
        proof = self.authority.issue_settlement_proof("proof-1", request)
        mutations = {
            "settlement_event_id": "settlement-2",
            "reservation_id": "reservation-2",
            "expected_previous_hash": "predecessor-2",
            "disposition": BudgetDisposition.CONSUMED,
            "actual_units": 1,
            "evidence_digest": "evidence-2",
            "reason_code": "OTHER_REASON",
            "non_dispatch_proven": True,
            "zero_liability_proven": True,
            "release_slot": True,
            "all_obligations_settled": True,
            "additional_liability": True,
            "repository_id": "repo-2",
            "run_id": "run-2",
            "item_id": "item-2",
            "logical_effect_id": "effect-2",
            "attempt_id": "attempt-2",
            "nonexecution_seal_id": "nonexecution-seal-1",
        }
        connection = sqlite3.connect(self.database_path)
        try:
            unchanged = tuple(connection.iterdump())
        finally:
            connection.close()

        self.assertEqual(
            set(mutations), set(BudgetSettlementContract.__dataclass_fields__)
        )
        for field, value in mutations.items():
            with self.subTest(field=field), self.assertRaisesRegex(
                DispatchDenied, "was not issued here"
            ):
                self.store._settle_budget(
                    replace(request, **{field: value}), proof, self.authority
                )
            connection = sqlite3.connect(self.database_path)
            try:
                after_denial = tuple(connection.iterdump())
            finally:
                connection.close()
            self.assertEqual(after_denial, unchanged)

    def test_settlement_rejects_non_boolean_control_flags_before_state_change(self) -> None:
        committed = self._commit_planned_intent(
            self.request(), self.capability, self.authority,
            expected_head="", writer_epoch=1,
        )
        self.oracle.allowed_head = committed.event_hash
        request = BudgetSettlementRequest(
            "settlement-1", "reservation-1", "",
            BudgetDisposition.UNKNOWN_WORST_CASE_CHARGED, None,
            "evidence-1", "USAGE_UNKNOWN",
        )
        connection = sqlite3.connect(self.database_path)
        try:
            unchanged = tuple(connection.iterdump())
        finally:
            connection.close()

        for field in (
            "non_dispatch_proven",
            "zero_liability_proven",
            "release_slot",
            "all_obligations_settled",
            "additional_liability",
        ):
            malformed = replace(request, **{field: "false"})
            with self.subTest(field=field), self.assertRaisesRegex(
                ValueError, "must be booleans"
            ):
                self.store._settle_budget(
                    malformed,
                    SyntheticSettlementProof(
                        "proof", "reservation-1", False, False, False,
                        "digest", "mac",
                    ),
                    self.authority,
                )
            connection = sqlite3.connect(self.database_path)
            try:
                after_denial = tuple(connection.iterdump())
            finally:
                connection.close()
            self.assertEqual(after_denial, unchanged)

    def test_f04_release_requires_both_proofs_and_releases_slot_once(self) -> None:
        committed = self._commit_planned_intent(self.request(), self.capability, self.authority, expected_head="", writer_epoch=1)
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
                incomplete,
            )
            self.store._settle_budget(incomplete, proof, self.authority)

        attacker = SyntheticAuthority(b"x" * 32)
        reopened = SQLiteStateStore(
            self.database_path, self.oracle, "repo-1"
        )
        forged_release = replace(incomplete, zero_liability_proven=True)
        forged_proof = attacker.issue_settlement_proof(
            "attacker-proof", forged_release
        )
        connection = sqlite3.connect(self.database_path)
        try:
            before_forged_release = tuple(connection.iterdump())
        finally:
            connection.close()
        with self.assertRaisesRegex(DispatchDenied, "accepted plan"):
            reopened._settle_budget(
                forged_release, forged_proof, attacker
            )
        connection = sqlite3.connect(self.database_path)
        try:
            after_forged_release = tuple(connection.iterdump())
        finally:
            connection.close()
        self.assertEqual(after_forged_release, before_forged_release)

        rebound = replace(incomplete, item_id="item-2")
        with self.assertRaisesRegex(DispatchDenied, "was not issued here"):
            self.authority.verify_settlement_proof(proof, rebound)

        complete = BudgetSettlementRequest(
            **{**incomplete.__dict__, "zero_liability_proven": True}
        )
        proof = self.authority.issue_settlement_proof(
            "proof-complete",
            complete,
        )
        receipt = reopened._settle_budget(complete, proof, self.authority)
        self.oracle.allowed_head = receipt.settlement_hash
        replay = self.store._settle_budget(complete, proof, self.authority)
        self.assertTrue(receipt.slot_released)
        self.assertTrue(replay.replayed)
        self.assertEqual(self.store.table_counts()["outstanding_slot"], 0)
        self.assertEqual(self.store.load_run_lifecycle("run-1"), LifecycleState.BLOCKED)
        recovered = SQLiteStateStore(self.database_path, self.oracle, "repo-1")
        recovered._bind_classification_authority(self.authority)
        recovered.load_verified("repo-1")
        self.assertEqual(
            recovered.load_run_lifecycle("run-1"), LifecycleState.BLOCKED
        )

    def test_restart_rejects_replacement_issuer_before_settlement_or_replay(self) -> None:
        committed = self._commit_planned_intent(
            self.request(), self.capability, self.authority,
            expected_head="", writer_epoch=1,
        )
        self.oracle.allowed_head = committed.event_hash
        attacker = SyntheticAuthority(b"x" * 32)
        reopened = SQLiteStateStore(
            self.database_path, self.oracle, "repo-1"
        )

        connection = sqlite3.connect(self.database_path)
        try:
            before_bind = tuple(connection.iterdump())
        finally:
            connection.close()
        with self.assertRaisesRegex(DispatchDenied, "accepted plan"):
            reopened._bind_classification_authority(attacker)
        connection = sqlite3.connect(self.database_path)
        try:
            after_bind = tuple(connection.iterdump())
        finally:
            connection.close()
        self.assertEqual(after_bind, before_bind)

        receipt = EffectObservationRequest(
            "attacker-observation", "attacker-observe-command",
            "attacker-observation-event", "repo-1", "run-1", "item-1",
            "effect-1", "attempt-1", "attacker-receipt",
            self.capability.claim_id, "descriptor-digest", 2,
            "attacker-settlement", "",
        )
        attacker_evidence_request = SourceControlEvidenceRequest(
            receipt.repository_id, receipt.run_id, receipt.item_id,
            receipt.logical_effect_id, receipt.attempt_id,
            receipt.source_claim_id, receipt.source_receipt_id,
            receipt.payload_digest, receipt.usage_units, True,
            SourceControlClassification.KNOWN,
        )
        attacker_evidence = attacker.issue_source_control_evidence(
            "attacker-source-evidence", attacker_evidence_request
        )
        receipt = replace(
            receipt,
            source_control_classification="KNOWN",
            source_control_evidence_id=attacker_evidence.evidence_id,
            source_control_evidence_digest=attacker_evidence.request_digest,
            source_control_issuer_fingerprint=(
                attacker_evidence.issuer_fingerprint
            ),
            source_control_issuer_mac=attacker_evidence.issuer_mac,
        )
        with self.assertRaisesRegex(DispatchDenied, "authority is not bound"):
            reopened._record_effect_observation(receipt, authority=attacker)
        connection = sqlite3.connect(self.database_path)
        try:
            after_receipt = tuple(connection.iterdump())
        finally:
            connection.close()
        self.assertEqual(after_receipt, before_bind)

        settlement_request = BudgetSettlementRequest(
            "settlement-1", "reservation-1", "",
            BudgetDisposition.CONSUMED, 2, "receipt-1", "USAGE_REPORTED",
        )
        settlement = self.store._settle_budget(
            settlement_request,
            self.authority.issue_settlement_proof(
                "proof-1", settlement_request
            ),
            self.authority,
        )
        self.oracle.allowed_head = settlement.settlement_hash
        connection = sqlite3.connect(self.database_path)
        try:
            before_replay = tuple(connection.iterdump())
        finally:
            connection.close()
        with self.assertRaisesRegex(DispatchDenied, "accepted plan"):
            reopened._settle_budget(
                settlement_request,
                attacker.issue_settlement_proof(
                    "attacker-replay-proof", settlement_request
                ),
                attacker,
            )
        connection = sqlite3.connect(self.database_path)
        try:
            after_replay = tuple(connection.iterdump())
        finally:
            connection.close()
        self.assertEqual(after_replay, before_replay)

    def test_known_usage_cannot_be_rewritten_as_release_or_unknown(self) -> None:
        committed = self._commit_planned_intent(
            self.request(), self.capability, self.authority,
            expected_head="", writer_epoch=1,
        )
        self.oracle.allowed_head = committed.event_hash
        consumed = BudgetSettlementRequest(
            "settlement-1", "reservation-1", "",
            BudgetDisposition.CONSUMED, 2, "receipt-1", "USAGE_REPORTED",
        )
        consumed_receipt = self.store._settle_budget(
            consumed,
            self.authority.issue_settlement_proof("proof-1", consumed),
            self.authority,
        )
        self.oracle.allowed_head = consumed_receipt.settlement_hash

        for disposition, actual_units in (
            (BudgetDisposition.RELEASED, None),
            (BudgetDisposition.UNKNOWN_WORST_CASE_CHARGED, None),
        ):
            request = BudgetSettlementRequest(
                f"settlement-{disposition.value}", "reservation-1",
                consumed_receipt.settlement_hash, disposition, actual_units,
                "contradictory-evidence", "CONTRADICTORY_SETTLEMENT",
                non_dispatch_proven=disposition is BudgetDisposition.RELEASED,
                zero_liability_proven=disposition is BudgetDisposition.RELEASED,
            )
            proof = self.authority.issue_settlement_proof(
                f"proof-{disposition.value}", request
            )
            with self.subTest(disposition=disposition), self.assertRaisesRegex(
                DispatchDenied,
                "illegal budget settlement transition|cannot downgrade known usage",
            ):
                self.store._settle_budget(request, proof, self.authority)

        self.assertEqual(self.store.table_counts()["budget_settlements"], 1)
        self.assertEqual(self.store.table_counts()["dispatch_fences"], 0)

    def test_additional_unknown_liability_preserves_known_charge_and_fences(self) -> None:
        committed = self._commit_planned_intent(
            self.request(), self.capability, self.authority,
            expected_head="", writer_epoch=1,
        )
        self.oracle.allowed_head = committed.event_hash
        consumed = BudgetSettlementRequest(
            "settlement-1", "reservation-1", "",
            BudgetDisposition.CONSUMED, 2, "receipt-1", "USAGE_REPORTED",
        )
        consumed_receipt = self.store._settle_budget(
            consumed,
            self.authority.issue_settlement_proof("proof-1", consumed),
            self.authority,
        )
        self.oracle.allowed_head = consumed_receipt.settlement_hash
        additional = BudgetSettlementRequest(
            "settlement-2", "reservation-1",
            consumed_receipt.settlement_hash,
            BudgetDisposition.UNKNOWN_WORST_CASE_CHARGED, None,
            "additional-exposure-1", "ADDITIONAL_LIABILITY_UNKNOWN",
            additional_liability=True,
        )

        under_bound = replace(additional, additional_liability=False)
        under_bound_proof = self.authority.issue_settlement_proof(
            "proof-under-bound", under_bound
        )
        connection = sqlite3.connect(self.database_path)
        try:
            before_rebind = tuple(connection.iterdump())
        finally:
            connection.close()
        with self.assertRaisesRegex(DispatchDenied, "was not issued here"):
            self.store._settle_budget(
                additional, under_bound_proof, self.authority
            )
        connection = sqlite3.connect(self.database_path)
        try:
            after_rebind = tuple(connection.iterdump())
        finally:
            connection.close()
        self.assertEqual(after_rebind, before_rebind)

        receipt = self.store._settle_budget(
            additional,
            self.authority.issue_settlement_proof("proof-2", additional),
            self.authority,
        )
        self.oracle.allowed_head = receipt.settlement_hash

        self.assertEqual(receipt.charged_units, 7)
        self.assertTrue(receipt.uncertainty)
        self.assertEqual(self.store.table_counts()["dispatch_fences"], 1)
        self.store.load_verified("repo-1")

    def test_f05_recovery_requires_independent_current_head(self) -> None:
        oracle = MutableFreshnessOracle()
        database_path = Path(self.temporary_directory.name) / "freshness.sqlite3"
        store = SQLiteStateStore(database_path, oracle, "repo-1")
        authority = SyntheticAuthority()
        store._bind_classification_authority(authority)
        authority.register(SyntheticGrant("grant-2", "repo-1", "effect-1", "attempt-1", "scope-1"))
        capability = authority.claim("grant-2", "repo-1", "effect-1", "attempt-1", "scope-1")
        plan = store.accept_plan(
            PlanAcceptanceRequest(
                "plan-1", "plan-command-1", "plan-event-1", "repo-1",
                "run-1", "item-1", "effect-1", "revision-1",
                "descriptor-digest", "scope-1", "budget-policy-digest",
                ("check-1",),
            ),
            expected_head="", writer_epoch=1,
        )
        oracle.allowed_head = plan.event_hash
        committed = store.commit_intent(
            self.request(), capability, authority,
            expected_head=plan.event_hash, writer_epoch=2,
        )
        with self.assertRaisesRegex(DispatchDenied, "freshness"):
            store.load_verified("repo-1")
        oracle.allowed_head = committed.event_hash
        catalog_head, run_heads = store.load_verified("repo-1")
        self.assertEqual(catalog_head, committed.event_hash)
        self.assertEqual(run_heads["run-1"], committed.event_hash)
        self.assertIn("@aegis/source/synthetic-authority", run_heads)

    def test_database_rejects_another_repository_identity(self) -> None:
        database_path = Path(self.temporary_directory.name) / "bound.sqlite3"
        SQLiteStateStore(database_path, MutableFreshnessOracle(), "repo-1")
        with self.assertRaisesRegex(Exception, "another repository"):
            SQLiteStateStore(database_path, MutableFreshnessOracle(), "repo-2")

    def test_recovery_rejects_deleted_slot_projection(self) -> None:
        committed = self._commit_planned_intent(
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

    def test_recovery_rejects_tampered_run_head_sequence(self) -> None:
        receipt = self._commit_planned_intent(
            self.request(), self.capability, self.authority,
            expected_head="", writer_epoch=1,
        )
        self.oracle.allowed_head = receipt.event_hash
        connection = sqlite3.connect(self.database_path)
        try:
            connection.execute(
                "UPDATE runs SET head_sequence = head_sequence + 1 "
                "WHERE run_id = 'run-1'"
            )
            connection.commit()
        finally:
            connection.close()
        with self.assertRaisesRegex(StorageIntegrityError, "head sequence"):
            self.store.load_verified("repo-1")

    def test_recovery_rejects_tampered_slot_run_and_generation(self) -> None:
        for column, value in (
            ("run_id", "other-run"),
            ("logical_effect_id", "other-effect"),
            ("attempt_id", "other-attempt"),
            ("generation", 2),
        ):
            with self.subTest(column=column):
                self.oracle.allowed_head = ""
                test_path = (
                    Path(self.temporary_directory.name) / f"slot-{column}.sqlite3"
                )
                store = SQLiteStateStore(test_path, self.oracle, "repo-1")
                authority = SyntheticAuthority()
                store._bind_classification_authority(authority)
                grant = SyntheticGrant(
                    f"grant-{column}", "repo-1", "effect-1", "attempt-1",
                    "scope-1",
                )
                authority.register(grant)
                capability = authority.claim(*grant.__dict__.values())
                plan = store.accept_plan(
                    PlanAcceptanceRequest(
                        "plan-1", "plan-command-1", "plan-event-1", "repo-1",
                        "run-1", "item-1", "effect-1", "revision-1",
                        "descriptor-digest", "scope-1", "budget-policy-digest",
                        ("check-1",),
                    ),
                    expected_head="", writer_epoch=1,
                )
                self.oracle.allowed_head = plan.event_hash
                receipt = store.commit_intent(
                    self.request(), capability, authority,
                    expected_head=plan.event_hash, writer_epoch=2,
                )
                self.oracle.allowed_head = receipt.event_hash
                connection = sqlite3.connect(test_path)
                try:
                    connection.execute(
                        f"UPDATE outstanding_slot SET {column} = ?", (value,)
                    )
                    connection.commit()
                finally:
                    connection.close()
                with self.assertRaisesRegex(StorageIntegrityError, "slot projection"):
                    store.load_verified("repo-1")

    def test_recovery_rejects_tampered_command_and_redemption_projections(self) -> None:
        committed = self._commit_planned_intent(
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
        committed = self._commit_planned_intent(
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
        committed = self._commit_planned_intent(
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
            settlement,
        )
        self.store._settle_budget(settlement, proof, self.authority)

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
        self._commit_planned_intent(
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
            request,
        )
        with self.assertRaisesRegex(DispatchDenied, "freshness"):
            self.store._settle_budget(request, proof, self.authority)
        self.assertEqual(self.store.table_counts()["budget_settlements"], 0)

    def test_c09_failure_before_settlement_commit_preserves_reservation_and_slot(self) -> None:
        committed = self._commit_planned_intent(
            self.request(), self.capability, self.authority, expected_head="", writer_epoch=1
        )
        self.oracle.allowed_head = committed.event_hash
        request = BudgetSettlementRequest(
            "settlement-1",
            "reservation-1",
            "",
            BudgetDisposition.RELEASED,
            None,
            "usage-evidence",
            "NONDISPATCH_PROVEN",
            non_dispatch_proven=True,
            zero_liability_proven=True,
            release_slot=True,
            all_obligations_settled=True,
        )
        proof = self.authority.issue_settlement_proof(
            "proof-1",
            request,
        )

        with self.assertRaises(InjectedFailure):
            self.store._settle_budget(
                request,
                proof,
                self.authority,
                failure_hook=raise_at("after_settlement_writes_before_commit"),
            )

        self.assertEqual(self.store.table_counts()["budget_settlements"], 0)
        self.assertEqual(self.store.table_counts()["outstanding_slot"], 1)
        catalog_head, run_heads = self.store.load_verified("repo-1")
        self.assertEqual(catalog_head, committed.event_hash)
        self.assertEqual(run_heads["run-1"], committed.event_hash)
        self.assertIn("@aegis/source/synthetic-authority", run_heads)

        receipt = self.store._settle_budget(request, proof, self.authority)
        self.oracle.allowed_head = receipt.settlement_hash
        self.assertFalse(receipt.replayed)
        self.assertEqual(receipt.held_units, 0)
        self.assertEqual(receipt.charged_units, 0)
        self.assertFalse(receipt.uncertainty)
        self.assertTrue(receipt.slot_released)
        self.assertEqual(self.store.table_counts()["events"], 3)
        self.assertEqual(self.store.table_counts()["budget_reservations"], 1)
        self.assertEqual(self.store.table_counts()["budget_settlements"], 1)
        self.assertEqual(self.store.table_counts()["outstanding_slot"], 0)
        self.store.load_verified("repo-1")

    def test_c09_failure_after_settlement_commit_replays_without_duplicate_release(self) -> None:
        committed = self._commit_planned_intent(
            self.request(), self.capability, self.authority, expected_head="", writer_epoch=1
        )
        self.oracle.allowed_head = committed.event_hash
        request = BudgetSettlementRequest(
            "settlement-1",
            "reservation-1",
            "",
            BudgetDisposition.RELEASED,
            None,
            "usage-evidence",
            "NONDISPATCH_PROVEN",
            non_dispatch_proven=True,
            zero_liability_proven=True,
            release_slot=True,
            all_obligations_settled=True,
        )
        proof = self.authority.issue_settlement_proof(
            "proof-1",
            request,
        )

        with self.assertRaises(InjectedFailure):
            self.store._settle_budget(
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
        replay = self.store._settle_budget(request, proof, self.authority)

        self.assertTrue(replay.replayed)
        self.assertEqual(replay.settlement_hash, settlement_hash)
        self.assertEqual(replay.held_units, 0)
        self.assertEqual(replay.charged_units, 0)
        self.assertFalse(replay.uncertainty)
        self.assertTrue(replay.slot_released)
        connection = sqlite3.connect(self.database_path)
        try:
            reservation = connection.execute(
                "SELECT held_units, charged_units, uncertainty FROM budget_reservations WHERE reservation_id = 'reservation-1'"
            ).fetchone()
        finally:
            connection.close()
        self.assertEqual(reservation, (0, 0, 0))
        self.assertEqual(self.store.table_counts()["events"], 3)
        self.assertEqual(self.store.table_counts()["budget_reservations"], 1)
        self.assertEqual(self.store.table_counts()["budget_settlements"], 1)
        self.assertEqual(self.store.table_counts()["outstanding_slot"], 0)
        self.store.load_verified("repo-1")

    def test_c04_observation_intake_survives_crash_without_duplicate_or_slot_release(self) -> None:
        committed = self._commit_planned_intent(
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
            settlement_request,
        )
        settlement = self.store._settle_budget(
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
            self._record_signed_effect_observation(
                observation,
                failure_hook=raise_at("after_observation_writes_before_commit"),
            )
        self.assertEqual(self.store.table_counts()["effect_observations"], 0)
        self.assertEqual(self.store.table_counts()["outstanding_slot"], 1)
        with self.assertRaises(InjectedFailure):
            self._record_signed_effect_observation(
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
        replay = self._record_signed_effect_observation(observation)

        self.assertTrue(replay.replayed)
        self.assertEqual(replay.event_hash, observation_hash)
        self.assertEqual(replay.resulting_state.value, "VALIDATING")


    def test_t25_recovery_derives_lifecycle_instead_of_trusting_event(self) -> None:
        committed = self._commit_planned_intent(
            self.request(), self.capability, self.authority,
            expected_head="", writer_epoch=1,
        )
        self.oracle.allowed_head = committed.event_hash
        request = BudgetSettlementRequest(
            "settlement-1", "reservation-1", "",
            BudgetDisposition.RELEASED, None, "usage-evidence",
            "NONDISPATCH_PROVEN", non_dispatch_proven=True,
            zero_liability_proven=True, release_slot=True,
            all_obligations_settled=True,
        )
        receipt = self.store._settle_budget(
            request,
            self.authority.issue_settlement_proof("proof-1", request),
            self.authority,
        )
        connection = sqlite3.connect(self.database_path)
        connection.row_factory = sqlite3.Row
        try:
            body = json.loads(
                connection.execute(
                    "SELECT body_json FROM budget_settlements WHERE "
                    "settlement_event_id = 'settlement-1'"
                ).fetchone()["body_json"]
            )
            body["lifecycle_to"] = LifecycleState.COMPLETED.value
            body["continuation_cursor"] = None
            event_hash = self.store._event_hash(body)
            body_json = json.dumps(
                body, sort_keys=True, separators=(",", ":")
            )
            connection.execute(
                "UPDATE budget_settlements SET settlement_hash = ?, "
                "body_json = ? WHERE settlement_event_id = 'settlement-1'",
                (event_hash, body_json),
            )
            connection.execute(
                "UPDATE budget_reservations SET settlement_head_hash = ? "
                "WHERE reservation_id = 'reservation-1'",
                (event_hash,),
            )
            connection.execute(
                "UPDATE events SET event_hash = ?, body_json = ? WHERE "
                "event_id = 'settlement-1'",
                (event_hash, body_json),
            )
            connection.execute(
                "UPDATE runs SET lifecycle_state = 'COMPLETED', "
                "continuation_cursor = NULL, head_hash = ? WHERE run_id = 'run-1'",
                (event_hash,),
            )
            connection.execute(
                "UPDATE repositories SET catalog_head = ? WHERE "
                "repository_id = 'repo-1'",
                (event_hash,),
            )
            connection.commit()
        finally:
            connection.close()
        self.oracle.allowed_head = event_hash

        with self.assertRaisesRegex(
            StorageIntegrityError, "T25 lifecycle semantics"
        ):
            self.store.load_verified("repo-1")

    def test_t25_historical_slot_requires_prior_exact_intent(self) -> None:
        self._commit_planned_intent(
            self.request(), self.capability, self.authority,
            expected_head="", writer_epoch=1,
        )
        connection = sqlite3.connect(self.database_path)
        connection.row_factory = sqlite3.Row
        try:
            reservation = connection.execute(
                "SELECT * FROM budget_reservations WHERE reservation_id = ?",
                ("reservation-1",),
            ).fetchone()
            intent_sequence = connection.execute(
                "SELECT sequence FROM events WHERE event_kind = ?",
                ("INTENT_COMMITTED",),
            ).fetchone()["sequence"]
            self.assertFalse(
                self.store._operation_slot_current_before(
                    connection, reservation, int(intent_sequence)
                )
            )
            self.assertTrue(
                self.store._operation_slot_current_before(
                    connection, reservation, int(intent_sequence) + 1
                )
            )
            self.assertFalse(
                self.store._operation_slot_current_before(
                    connection, reservation, int(intent_sequence) + 1,
                    expected_generation=2,
                )
            )
        finally:
            connection.close()

    def test_historical_slot_ignores_release_fields_on_budget_event(self) -> None:
        self._record_effect_observation(check_ids=("check-1",))
        connection = sqlite3.connect(self.database_path)
        connection.row_factory = sqlite3.Row
        try:
            settlement = connection.execute(
                "SELECT settlement_event_id, body_json FROM budget_settlements "
                "WHERE reservation_id = ?",
                ("reservation-1",),
            ).fetchone()
            body = json.loads(settlement["body_json"])
            body.update(
                {
                    "slot_released": True,
                    "slot_attempt_id": "attempt-1",
                    "slot_generation": 1,
                }
            )
            connection.execute(
                "UPDATE events SET body_json = ? WHERE event_id = ?",
                (
                    json.dumps(body, sort_keys=True, separators=(",", ":")),
                    settlement["settlement_event_id"],
                ),
            )
            reservation = connection.execute(
                "SELECT * FROM budget_reservations WHERE reservation_id = ?",
                ("reservation-1",),
            ).fetchone()
            self.assertTrue(
                self.store._operation_slot_current_before(
                    connection, reservation, 100
                )
            )
        finally:
            connection.close()

    def test_recovery_rejects_settlement_moved_to_another_run(self) -> None:
        committed = self._commit_planned_intent(
            self.request(), self.capability, self.authority,
            expected_head="", writer_epoch=1,
        )
        self.oracle.allowed_head = committed.event_hash
        settlement_request = BudgetSettlementRequest(
            "settlement-1", "reservation-1", "",
            BudgetDisposition.CONSUMED, 2, "usage-evidence", "USAGE_REPORTED",
        )
        settlement = self.store._settle_budget(
            settlement_request,
            self.authority.issue_settlement_proof(
                "settlement-proof-1", settlement_request
            ),
            self.authority,
        )
        self.oracle.allowed_head = settlement.settlement_hash
        second_plan = self.store.accept_plan(
            PlanAcceptanceRequest(
                "plan-2", "plan-command-2", "plan-event-2", "repo-1",
                "run-2", "item-2", "effect-2", "revision-2",
                "descriptor-2", "scope-2", "budget-policy-2", ("check-2",),
            ),
            expected_head=settlement.settlement_hash,
            writer_epoch=4,
        )
        connection = sqlite3.connect(self.database_path)
        try:
            body = json.loads(
                connection.execute(
                    "SELECT body_json FROM budget_settlements WHERE "
                    "settlement_event_id = ?",
                    ("settlement-1",),
                ).fetchone()[0]
            )
            body.update(
                {
                    "run_id": "run-2",
                    "item_id": "item-2",
                    "sequence": 2,
                    "previous_event_hash": second_plan.event_hash,
                }
            )
            payload_keys = (
                "actual_units", "additional_liability",
                "all_obligations_settled", "disposition", "evidence_digest",
                "expected_previous_hash", "non_dispatch_proven", "reason_code",
                "release_slot", "reservation_id", "settlement_event_id",
                "zero_liability_proven", "repository_id", "run_id", "item_id",
                "logical_effect_id", "attempt_id", "nonexecution_seal_id",
                "settlement_binding_version",
            )
            payload_digest = self.store._event_hash(
                {key: body[key] for key in payload_keys}
            )
            event_hash = self.store._event_hash(body)
            body_json = json.dumps(
                body, sort_keys=True, separators=(",", ":")
            )
            connection.execute(
                "UPDATE budget_settlements SET settlement_hash = ?, "
                "payload_digest = ?, body_json = ? WHERE settlement_event_id = ?",
                (event_hash, payload_digest, body_json, "settlement-1"),
            )
            connection.execute(
                "UPDATE budget_reservations SET settlement_head_hash = ? "
                "WHERE reservation_id = ?",
                (event_hash, "reservation-1"),
            )
            connection.execute(
                "UPDATE events SET run_id = ?, item_id = ?, sequence = 2, "
                "previous_event_hash = ?, event_hash = ?, body_json = ? "
                "WHERE event_id = ?",
                (
                    "run-2", "item-2", second_plan.event_hash, event_hash,
                    body_json, "settlement-1",
                ),
            )
            connection.execute(
                "UPDATE runs SET head_sequence = 2, head_hash = ? WHERE run_id = ?",
                (event_hash, "run-2"),
            )
            connection.execute(
                "UPDATE runs SET head_sequence = 2, head_hash = ? WHERE run_id = ?",
                (committed.event_hash, "run-1"),
            )
            connection.execute(
                "UPDATE repositories SET catalog_head = ? WHERE repository_id = ?",
                (event_hash, "repo-1"),
            )
            connection.commit()
        finally:
            connection.close()
        self.oracle.allowed_head = event_hash

        with self.assertRaisesRegex(
            StorageIntegrityError,
            "writer epoch|settlement scope binding",
        ):
            self.store.load_verified("repo-1")

    def test_recovery_rejects_surplus_settlement_key(self) -> None:
        committed = self._commit_planned_intent(
            self.request(), self.capability, self.authority,
            expected_head="", writer_epoch=1,
        )
        self.oracle.allowed_head = committed.event_hash
        settlement_request = BudgetSettlementRequest(
            "surplus-settlement", "reservation-1", "",
            BudgetDisposition.CONSUMED, 2, "usage-evidence", "USAGE_REPORTED",
        )
        settlement = self.store._settle_budget(
            settlement_request,
            self.authority.issue_settlement_proof(
                "surplus-settlement-proof", settlement_request
            ),
            self.authority,
        )
        connection = sqlite3.connect(self.database_path)
        try:
            body = json.loads(
                connection.execute(
                    "SELECT body_json FROM budget_settlements WHERE "
                    "settlement_event_id = ?",
                    ("surplus-settlement",),
                ).fetchone()[0]
            )
            body["surplus_authority_claim"] = True
            event_hash = self.store._event_hash(body)
            body_json = json.dumps(
                body, sort_keys=True, separators=(",", ":")
            )
            connection.execute(
                "UPDATE budget_settlements SET settlement_hash = ?, "
                "body_json = ? WHERE settlement_event_id = ?",
                (event_hash, body_json, "surplus-settlement"),
            )
            connection.execute(
                "UPDATE budget_reservations SET settlement_head_hash = ? "
                "WHERE reservation_id = ?",
                (event_hash, "reservation-1"),
            )
            connection.execute(
                "UPDATE events SET event_hash = ?, body_json = ? WHERE event_id = ?",
                (event_hash, body_json, "surplus-settlement"),
            )
            connection.execute(
                "UPDATE runs SET head_hash = ? WHERE run_id = ?",
                (event_hash, "run-1"),
            )
            connection.execute(
                "UPDATE repositories SET catalog_head = ? WHERE repository_id = ?",
                (event_hash, "repo-1"),
            )
            connection.commit()
        finally:
            connection.close()
        self.oracle.allowed_head = event_hash

        with self.assertRaisesRegex(StorageIntegrityError, "settlement schema"):
            self.store.load_verified("repo-1")

    def test_recovery_rejects_settlement_bool_for_integer(self) -> None:
        committed = self._commit_planned_intent(
            self.request(), self.capability, self.authority,
            expected_head="", writer_epoch=1,
        )
        self.oracle.allowed_head = committed.event_hash
        settlement_request = BudgetSettlementRequest(
            "typed-settlement", "reservation-1", "",
            BudgetDisposition.CONSUMED, 0, "usage-evidence", "USAGE_REPORTED",
        )
        settlement = self.store._settle_budget(
            settlement_request,
            self.authority.issue_settlement_proof(
                "typed-settlement-proof", settlement_request
            ),
            self.authority,
        )
        connection = sqlite3.connect(self.database_path)
        try:
            body = json.loads(
                connection.execute(
                    "SELECT body_json FROM budget_settlements WHERE "
                    "settlement_event_id = ?",
                    ("typed-settlement",),
                ).fetchone()[0]
            )
            body["charged_units"] = False
            event_hash = self.store._event_hash(body)
            body_json = json.dumps(
                body, sort_keys=True, separators=(",", ":")
            )
            connection.execute(
                "UPDATE budget_settlements SET settlement_hash = ?, "
                "body_json = ? WHERE settlement_event_id = ?",
                (event_hash, body_json, "typed-settlement"),
            )
            connection.execute(
                "UPDATE budget_reservations SET settlement_head_hash = ? "
                "WHERE reservation_id = ?",
                (event_hash, "reservation-1"),
            )
            connection.execute(
                "UPDATE events SET event_hash = ?, body_json = ? WHERE event_id = ?",
                (event_hash, body_json, "typed-settlement"),
            )
            connection.execute(
                "UPDATE runs SET head_hash = ? WHERE run_id = ?",
                (event_hash, "run-1"),
            )
            connection.execute(
                "UPDATE repositories SET catalog_head = ? WHERE repository_id = ?",
                (event_hash, "repo-1"),
            )
            connection.commit()
        finally:
            connection.close()
        self.oracle.allowed_head = event_hash

        with self.assertRaisesRegex(StorageIntegrityError, "settlement schema"):
            self.store.load_verified("repo-1")

    def test_recovery_rejects_ordinary_receipt_slot_release_forgery(self) -> None:
        recorded = self._record_effect_observation(check_ids=("check-1",))
        connection = sqlite3.connect(self.database_path)
        try:
            body = json.loads(
                connection.execute(
                    "SELECT body_json FROM events WHERE event_id = ?",
                    (recorded.event_id,),
                ).fetchone()[0]
            )
            self.assertFalse(body["slot_released"])
            body["slot_released"] = True
            event_hash = self.store._event_hash(body)
            body_json = json.dumps(
                body, sort_keys=True, separators=(",", ":")
            )
            connection.execute(
                "UPDATE events SET event_hash = ?, body_json = ? WHERE event_id = ?",
                (event_hash, body_json, recorded.event_id),
            )
            connection.execute(
                "UPDATE effect_observations SET event_hash = ?, body_json = ? "
                "WHERE observation_id = ?",
                (event_hash, body_json, recorded.observation_id),
            )
            connection.execute(
                "UPDATE command_outcomes SET event_hash = ? WHERE command_id = ?",
                (event_hash, recorded.command_id),
            )
            connection.execute(
                "UPDATE runs SET head_hash = ? WHERE run_id = ?",
                (event_hash, "run-1"),
            )
            connection.execute(
                "UPDATE repositories SET catalog_head = ? WHERE repository_id = ?",
                (event_hash, "repo-1"),
            )
            connection.execute("DELETE FROM outstanding_slot")
            connection.commit()
        finally:
            connection.close()
        self.oracle.allowed_head = event_hash

        with self.assertRaisesRegex(
            StorageIntegrityError, "effect observation semantics"
        ):
            self.store.load_verified("repo-1")

    def test_observation_requests_reject_boolean_usage(self) -> None:
        with self.assertRaisesRegex(ValueError, "usage"):
            EffectObservationRequest(
                "observation-bool", "observe-command-bool",
                "observation-event-bool", "repo-1", "run-1", "item-1",
                "effect-1", "attempt-1", "receipt-bool", "claim-bool",
                "descriptor-digest", True, "settlement-bool", "",
            ).validate()
        with self.assertRaisesRegex(ValueError, "usage"):
            ValidatorObservationRequest(
                "validator-observation-bool", "validator-command-bool",
                "validator-event-bool", "repo-1", "run-1", "item-1",
                "effect-1", "validator-intent-bool",
                "validator-attempt-bool", "validator-result-bool",
                "claim-bool", "revision-1", "check-1", "input-1",
                "result-bool", "PASS", True, "validator-settlement-bool",
                "validator-settlement-hash-bool",
            ).validate()

    def test_c04_unknown_receipt_usage_is_recorded_for_reconciliation(self) -> None:
        committed = self._commit_planned_intent(
            self.request(), self.capability, self.authority, expected_head="", writer_epoch=1
        )
        self.oracle.allowed_head = committed.event_hash
        settlement_request = BudgetSettlementRequest(
            "settlement-1", "reservation-1", "",
            BudgetDisposition.UNKNOWN_WORST_CASE_CHARGED, None,
            "receipt-unknown-1", "USAGE_UNKNOWN",
        )
        proof = self.authority.issue_settlement_proof(
            "proof-1", settlement_request
        )
        settlement = self.store._settle_budget(
            settlement_request,
            proof,
            self.authority,
        )
        self.oracle.allowed_head = settlement.settlement_hash

        recorded = self._record_signed_effect_observation(
            EffectObservationRequest(
                "observation-unknown-1", "observe-unknown-command-1",
                "observation-unknown-event-1", "repo-1", "run-1", "item-1",
                "effect-1", "attempt-1", "receipt-unknown-1",
                self.capability.claim_id, "descriptor-digest", None,
                "settlement-1", settlement.settlement_hash,
            )
        )
        self.oracle.allowed_head = recorded.event_hash

        self.assertEqual(recorded.resulting_state.value, "RECONCILIATION_REQUIRED")
        self.assertEqual(self.store.table_counts()["effect_observations"], 1)
        self.assertEqual(self.store.table_counts()["outstanding_slot"], 1)

        release = BudgetSettlementRequest(
            "settlement-release-1", "reservation-1",
            settlement.settlement_hash, BudgetDisposition.RELEASED, None,
            "non-dispatch-proof", "NONDISPATCH",
            non_dispatch_proven=True, zero_liability_proven=True,
        )
        connection = sqlite3.connect(self.database_path)
        try:
            before_denial = tuple(connection.iterdump())
        finally:
            connection.close()
        with self.assertRaisesRegex(
            DispatchDenied, "cannot release liability"
        ):
            self.store._settle_budget(
                release,
                self.authority.issue_settlement_proof(
                    "proof-release-1", release
                ),
                self.authority,
            )
        connection = sqlite3.connect(self.database_path)
        try:
            after_denial = tuple(connection.iterdump())
        finally:
            connection.close()
        self.assertEqual(after_denial, before_denial)

    def test_t17_exact_legacy_billing_projection_migrates_without_event_rewrite(
        self,
    ) -> None:
        committed = self._commit_planned_intent(
            self.request(), self.capability, self.authority,
            expected_head="", writer_epoch=1,
        )
        self.oracle.allowed_head = committed.event_hash
        self._contact_committed_operation(committed)
        settlement_request = BudgetSettlementRequest(
            "legacy-settlement", "reservation-1", "",
            BudgetDisposition.UNKNOWN_WORST_CASE_CHARGED, None,
            "legacy-receipt", "USAGE_UNKNOWN",
        )
        settlement = self.store._settle_budget(
            settlement_request,
            self.authority.issue_settlement_proof(
                "legacy-settlement-proof", settlement_request
            ),
            self.authority,
        )
        self.oracle.allowed_head = settlement.settlement_hash
        observed = self._record_signed_effect_observation(
            EffectObservationRequest(
                "legacy-observation", "legacy-observation-command",
                "legacy-observation-event", "repo-1", "run-1", "item-1",
                "effect-1", "attempt-1", "legacy-receipt",
                self.capability.claim_id, "descriptor-digest", None,
                "legacy-settlement", settlement.settlement_hash,
            )
        )
        self.oracle.allowed_head = observed.event_hash
        connection = sqlite3.connect(self.database_path)
        connection.row_factory = sqlite3.Row
        try:
            event_bytes = connection.execute(
                "SELECT body_json FROM events WHERE event_id = ?",
                (observed.event_id,),
            ).fetchone()[0]
            row = connection.execute(
                "SELECT * FROM uncertainty_instances WHERE origin_event_id = ?",
                (observed.event_id,),
            ).fetchone()
            origin = json.loads(event_bytes)
            legacy_body = {
                "attempt_id": origin["attempt_id"],
                "check_id": None,
                "fence_id": row["uncertainty_id"],
                "item_id": origin["item_id"],
                "logical_effect_id": origin["logical_effect_id"],
                "origin_event_hash": row["origin_event_hash"],
                "origin_event_id": row["origin_event_id"],
                "repository_id": origin["repository_id"],
                "reservation_id": row["reservation_id"],
                "run_id": origin["run_id"],
                "schema_version": 1,
                "settlement_head_hash": row["settlement_head_hash"],
                "uncertainty_id": row["uncertainty_id"],
                "uncertainty_kind": "BILLING",
            }
            connection.execute(
                "UPDATE uncertainty_instances SET body_json = ? WHERE "
                "uncertainty_id = ?",
                (
                    json.dumps(
                        legacy_body, sort_keys=True, separators=(",", ":")
                    ),
                    row["uncertainty_id"],
                ),
            )
            connection.execute(
                "DROP TABLE verified_receipt_reconciliation_actions"
            )
            connection.execute("DROP TABLE operation_retry_authorizations")
            connection.execute("DROP TABLE operation_recovery_actions")
            connection.execute(
                "DROP TABLE operation_nonexecution_resume_actions"
            )
            connection.execute("DROP TABLE proven_nonexecution_actions")
            strip_t28_foundation_schema(connection)
            connection.execute("PRAGMA user_version = 0")
            connection.commit()
        finally:
            connection.close()

        tampered_path = self.database_path.parent / "legacy-tampered.sqlite3"
        shutil.copy2(self.database_path, tampered_path)
        connection = sqlite3.connect(tampered_path)
        try:
            tampered = dict(legacy_body)
            tampered["retargeted"] = True
            connection.execute(
                "UPDATE uncertainty_instances SET body_json = ? WHERE "
                "uncertainty_id = ?",
                (
                    json.dumps(
                        tampered, sort_keys=True, separators=(",", ":")
                    ),
                    row["uncertainty_id"],
                ),
            )
            connection.commit()
        finally:
            connection.close()
        with self.assertRaisesRegex(
            StorageIntegrityError, "legacy operation uncertainty was tampered"
        ):
            SQLiteStateStore(tampered_path, self.oracle, "repo-1")

        migrated = SQLiteStateStore(
            self.database_path, self.oracle, "repo-1"
        )
        connection = sqlite3.connect(self.database_path)
        try:
            migrated_event_bytes = connection.execute(
                "SELECT body_json FROM events WHERE event_id = ?",
                (observed.event_id,),
            ).fetchone()[0]
            migrated_body = json.loads(
                connection.execute(
                    "SELECT body_json FROM uncertainty_instances WHERE "
                    "origin_event_id = ?",
                    (observed.event_id,),
                ).fetchone()[0]
            )
            semantic_version = connection.execute(
                "PRAGMA user_version"
            ).fetchone()[0]
        finally:
            connection.close()
        self.assertEqual(migrated_event_bytes, event_bytes)
        self.assertEqual(migrated_body["schema_version"], 2)
        self.assertEqual(semantic_version, 5)
        migrated.load_verified("repo-1", authority=self.authority)

    def test_validator_containment_schema_version_is_five(self) -> None:
        connection = sqlite3.connect(self.database_path)
        try:
            semantic_version = connection.execute(
                "PRAGMA user_version"
            ).fetchone()[0]
        finally:
            connection.close()
        self.assertEqual(semantic_version, 5)

    def test_t28_v4_reopen_rejects_schema_or_projection_healing(self) -> None:
        semantic_inputs = (("input", "digest-1"),)
        descriptor = self.store.canonical_effect_descriptor_digest(
            "WRITE", "synthetic-target-1", semantic_inputs, 1
        )
        accepted = self.store.accept_plan(
            PlanAcceptanceRequest(
                "schema-plan", "schema-command", "schema-event", "repo-1",
                "schema-run", "schema-item", "schema-effect",
                "schema-revision", descriptor, "schema-scope",
                "schema-budget", ("schema-check",), (),
                effect_action="WRITE", effect_target="synthetic-target-1",
                effect_semantic_inputs=semantic_inputs, target_generation=1,
            ),
            expected_head="", writer_epoch=1,
        )
        self.oracle.allowed_head = accepted.event_hash
        for name, mutation in (
            (
                "missing-definition",
                "DELETE FROM effect_definitions WHERE logical_effect_id = "
                "'schema-effect'",
            ),
            (
                "surplus-origin",
                "INSERT INTO operation_origins VALUES ("
                "'repo-1', 'schema-run', 'schema-effect', 'EXECUTION_INTENT', "
                "'surplus-attempt', 'schema-event', '"
                + accepted.event_hash
                + "', 'schema-run', 'surplus-attempt', NULL, NULL, NULL)",
            ),
            (
                "altered-schema",
                "ALTER TABLE effect_definitions ADD COLUMN unexpected TEXT",
            ),
        ):
            with self.subTest(name=name):
                case_path = Path(self.temporary_directory.name) / f"{name}.sqlite3"
                shutil.copy2(self.database_path, case_path)
                connection = sqlite3.connect(case_path)
                try:
                    connection.execute(mutation)
                    connection.commit()
                finally:
                    connection.close()
                with self.assertRaisesRegex(
                    StorageIntegrityError,
                    "T28 foundation (schema|projections)",
                ):
                    SQLiteStateStore(case_path, self.oracle, "repo-1")
                connection = sqlite3.connect(case_path)
                try:
                    if name == "missing-definition":
                        remaining = connection.execute(
                            "SELECT COUNT(*) FROM effect_definitions WHERE "
                            "logical_effect_id = 'schema-effect'"
                        ).fetchone()[0]
                        self.assertEqual(remaining, 0)
                finally:
                    connection.close()

    def test_c04_conflicting_durable_identities_fail_closed(self) -> None:
        committed = self._commit_planned_intent(
            self.request(), self.capability, self.authority,
            expected_head="", writer_epoch=1,
        )
        self.oracle.allowed_head = committed.event_hash
        self._contact_committed_operation(committed)
        base = EffectObservationRequest(
            "observation-1", "observe-command-1", "observation-event-1",
            "repo-1", "run-1", "item-1", "effect-1", "attempt-1",
            "receipt-1", self.capability.claim_id, "descriptor-digest", 2,
            "settlement-1", "",
        )
        recorded = self._record_signed_effect_observation(base)
        self.assertFalse(recorded.replayed)
        self.oracle.allowed_head = recorded.event_hash
        for conflicting in (
            EffectObservationRequest(
                *(
                    "observation-1", "observe-command-2", "observation-event-2",
                    "repo-1", "run-1", "item-1", "effect-1", "attempt-1",
                    "receipt-2", self.capability.claim_id, "descriptor-digest", 2,
                    "settlement-2", "",
                )
            ),
            EffectObservationRequest(
                *(
                    "observation-2", "observe-command-2", "event-1",
                    "repo-1", "run-1", "item-1", "effect-1", "attempt-1",
                    "receipt-2", self.capability.claim_id, "descriptor-digest", 2,
                    "settlement-2", "",
                )
            ),
            EffectObservationRequest(
                *(
                    "observation-2", "observe-command-2", "observation-event-2",
                    "repo-1", "run-1", "item-1", "effect-1", "attempt-1",
                    "receipt-2", self.capability.claim_id, "descriptor-digest", 2,
                    "event-1", "",
                )
            ),
        ):
            with self.subTest(conflicting=conflicting), self.assertRaises(
                StorageIntegrityError
            ):
                self._record_signed_effect_observation(conflicting)
            self.assertEqual(self.store.table_counts()["budget_settlements"], 1)
            self.assertEqual(self.store.table_counts()["effect_observations"], 1)

    def test_c04_recovery_rejects_tampered_observation_projection(self) -> None:
        observation = self._record_effect_observation(check_ids=("check-1",))
        self.oracle.allowed_head = observation.event_hash
        connection = sqlite3.connect(self.database_path)
        try:
            connection.execute(
                "UPDATE effect_observations SET source_claim_id = 'tampered' "
                "WHERE observation_id = 'observation-1'"
            )
            connection.commit()
        finally:
            connection.close()
        with self.assertRaisesRegex(
            StorageIntegrityError, "effect-observation projection"
        ):
            SQLiteStateStore(
                self.database_path, self.oracle, "repo-1"
            ).load_verified("repo-1")

    def test_t17_new_observation_requires_typed_source_evidence(self) -> None:
        self._record_effect_observation(check_ids=("check-1",))
        with self.assertRaisesRegex(
            DispatchDenied, "complete source/control evidence"
        ):
            self.store._record_effect_observation(
                EffectObservationRequest(
                    "unsigned-observation", "unsigned-command",
                    "unsigned-event", "repo-1", "run-1", "item-1",
                    "effect-1", "attempt-1", "unsigned-receipt",
                    self.capability.claim_id, "descriptor-digest", 2,
                    "settlement-1", "",
                )
            )

    def test_t17_v2_observation_recovery_requires_and_verifies_authority(
        self,
    ) -> None:
        observation = self._record_effect_observation(check_ids=("check-1",))
        self.oracle.allowed_head = observation.event_hash
        with self.assertRaisesRegex(
            StorageIntegrityError, "evidence authority is required"
        ):
            SQLiteStateStore(
                self.database_path, self.oracle, "repo-1"
            ).load_verified("repo-1")
        SQLiteStateStore(
            self.database_path, self.oracle, "repo-1"
        ).load_verified("repo-1", authority=self.authority)

        retargeted_path = (
            self.database_path.parent / "retargeted-source-control.sqlite3"
        )
        shutil.copy2(self.database_path, retargeted_path)
        connection = sqlite3.connect(retargeted_path)
        connection.row_factory = sqlite3.Row
        try:
            row = connection.execute(
                "SELECT * FROM effect_observations WHERE observation_id = "
                "'observation-1'"
            ).fetchone()
            body = json.loads(row["body_json"])
            body["source_control_classification"] = "UNKNOWN"
            request_fields = {
                field: body[field]
                for field in EffectObservationRequest.__dataclass_fields__
            }
            request_fields["settlement_hash"] = body[
                "requested_settlement_hash"
            ]
            request = EffectObservationRequest(**request_fields)
            body["command_payload_digest"] = self.store._event_hash(
                self.store._effect_observation_request_payload(request)
            )
            body["observation_digest"] = self.store._observation_digest(
                request
            )
            retargeted_hash = self.store._event_hash(body)
            body_json = json.dumps(body, sort_keys=True, separators=(",", ":"))
            connection.execute(
                "UPDATE events SET event_hash = ?, body_json = ? WHERE "
                "event_id = 'observation-event-1'",
                (retargeted_hash, body_json),
            )
            connection.execute(
                "UPDATE effect_observations SET observation_digest = ?, "
                "command_payload_digest = ?, event_hash = ?, body_json = ? "
                "WHERE observation_id = 'observation-1'",
                (
                    body["observation_digest"],
                    body["command_payload_digest"],
                    retargeted_hash,
                    body_json,
                ),
            )
            connection.execute(
                "UPDATE command_outcomes SET payload_digest = ?, "
                "event_hash = ? WHERE command_id = 'observe-command-1'",
                (body["command_payload_digest"], retargeted_hash),
            )
            connection.execute(
                "UPDATE runs SET head_hash = ? WHERE run_id = 'run-1'",
                (retargeted_hash,),
            )
            connection.execute(
                "UPDATE repositories SET catalog_head = ? WHERE "
                "repository_id = 'repo-1'",
                (retargeted_hash,),
            )
            reservation = connection.execute(
                "SELECT reservation_id FROM budget_reservations WHERE "
                "repository_id = 'repo-1' AND run_id = 'run-1' AND "
                "logical_effect_id = 'effect-1' AND attempt_id = 'attempt-1'"
            ).fetchone()[0]
            specs = self.store._derive_operation_uncertainty_specs(
                origin_body=body,
                origin_event_hash=retargeted_hash,
                reservation_id=reservation,
                settlement_head_hash=body["settlement_hash"],
                categories=("SOURCE_CONTROL",),
            )
            self.store._insert_operation_uncertainties(connection, specs)
            connection.commit()
        finally:
            connection.close()
        retargeted_oracle = MutableFreshnessOracle()
        retargeted_oracle.allowed_head = retargeted_hash
        with self.assertRaisesRegex(
            StorageIntegrityError, "effect observation semantics"
        ):
            SQLiteStateStore(
                retargeted_path, retargeted_oracle, "repo-1"
            ).load_verified("repo-1", authority=self.authority)

        connection = sqlite3.connect(self.database_path)
        connection.row_factory = sqlite3.Row
        try:
            row = connection.execute(
                "SELECT * FROM effect_observations WHERE observation_id = "
                "'observation-1'"
            ).fetchone()
            body = json.loads(row["body_json"])
            body["source_control_issuer_mac"] = "0" * 64
            request_fields = {
                field: body[field]
                for field in EffectObservationRequest.__dataclass_fields__
            }
            request_fields["settlement_hash"] = body[
                "requested_settlement_hash"
            ]
            request = EffectObservationRequest(**request_fields)
            body["command_payload_digest"] = self.store._event_hash(
                self.store._effect_observation_request_payload(request)
            )
            body["observation_digest"] = self.store._observation_digest(
                request
            )
            event_hash = self.store._event_hash(body)
            body_json = json.dumps(body, sort_keys=True, separators=(",", ":"))
            connection.execute(
                "UPDATE events SET event_hash = ?, body_json = ? WHERE "
                "event_id = 'observation-event-1'",
                (event_hash, body_json),
            )
            connection.execute(
                "UPDATE effect_observations SET observation_digest = ?, "
                "command_payload_digest = ?, event_hash = ?, body_json = ? "
                "WHERE observation_id = 'observation-1'",
                (
                    body["observation_digest"],
                    body["command_payload_digest"],
                    event_hash,
                    body_json,
                ),
            )
            connection.execute(
                "UPDATE command_outcomes SET payload_digest = ?, "
                "event_hash = ? WHERE command_id = 'observe-command-1'",
                (body["command_payload_digest"], event_hash),
            )
            connection.execute(
                "UPDATE runs SET head_hash = ? WHERE run_id = 'run-1'",
                (event_hash,),
            )
            connection.execute(
                "UPDATE repositories SET catalog_head = ? WHERE "
                "repository_id = 'repo-1'",
                (event_hash,),
            )
            connection.commit()
        finally:
            connection.close()
        self.oracle.allowed_head = event_hash
        with self.assertRaisesRegex(
            StorageIntegrityError, "effect observation semantics"
        ):
            SQLiteStateStore(
                self.database_path, self.oracle, "repo-1"
            ).load_verified("repo-1", authority=self.authority)

    def _record_effect_observation(
        self,
        check_ids=("check-1", "check-2"),
        aggregate_gate_ids=None,
    ):
        if aggregate_gate_ids is None:
            aggregate_gate_ids = check_ids
        plan = self.store.accept_plan(
            PlanAcceptanceRequest(
                "plan-1", "plan-command-1", "plan-event-1", "repo-1",
                "run-1", "item-1", "effect-1", "revision-1",
                "descriptor-digest", "scope-1", "budget-policy-digest",
                check_ids, aggregate_gate_ids,
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
            settlement_request,
        )
        settlement = self.store._settle_budget(
            settlement_request, proof, self.authority
        )
        self.oracle.allowed_head = settlement.settlement_hash
        receipt = self._record_signed_effect_observation(
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
            "item-1", "effect-1", "revision-1", "descriptor-digest",
            "scope-1", "budget-policy-digest", ("check-2", "check-1"),
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
                    "run-2", "item-2", "effect-2", "revision-2",
                    "descriptor-2", "scope-2", "budget-2", (),
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
            "item-1", "effect-1", "revision-1", "descriptor-digest",
            "scope-1", "budget-policy-digest", ("check-1",),
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

    def test_t01_recovery_rejects_self_consistent_terminal_entry(self) -> None:
        accepted = self.store.accept_plan(
            PlanAcceptanceRequest(
                "plan-1", "plan-command-1", "plan-event-1", "repo-1",
                "run-1", "item-1", "effect-1", "revision-1",
                "descriptor-digest", "scope-1", "budget-policy-digest",
                ("check-1",),
            ),
            expected_head="",
            writer_epoch=1,
        )
        connection = sqlite3.connect(self.database_path)
        try:
            body = json.loads(
                connection.execute(
                    "SELECT body_json FROM events WHERE event_id = ?",
                    ("plan-event-1",),
                ).fetchone()[0]
            )
            body["lifecycle_to"] = LifecycleState.COMPLETED.value
            event_hash = self.store._event_hash(body)
            body_json = json.dumps(
                body, sort_keys=True, separators=(",", ":")
            )
            connection.execute(
                "UPDATE events SET event_hash = ?, body_json = ? WHERE event_id = ?",
                (event_hash, body_json, "plan-event-1"),
            )
            connection.execute(
                "UPDATE validation_plans SET event_hash = ?, body_json = ? "
                "WHERE plan_id = ?",
                (event_hash, body_json, "plan-1"),
            )
            connection.execute(
                "UPDATE command_outcomes SET event_hash = ? WHERE command_id = ?",
                (event_hash, "plan-command-1"),
            )
            connection.execute(
                "UPDATE runs SET lifecycle_state = ?, head_hash = ? WHERE run_id = ?",
                (LifecycleState.COMPLETED.value, event_hash, "run-1"),
            )
            connection.execute(
                "UPDATE repositories SET catalog_head = ? WHERE repository_id = ?",
                (event_hash, "repo-1"),
            )
            connection.commit()
        finally:
            connection.close()
        self.oracle.allowed_head = event_hash

        with self.assertRaisesRegex(StorageIntegrityError, "lifecycle route"):
            self.store.load_verified("repo-1")

    def test_t01_recovery_rejects_missing_lifecycle_key(self) -> None:
        self.store.accept_plan(
            PlanAcceptanceRequest(
                "plan-1", "plan-command-1", "plan-event-1", "repo-1",
                "run-1", "item-1", "effect-1", "revision-1",
                "descriptor-digest", "scope-1", "budget-policy-digest",
                ("check-1",),
            ),
            expected_head="",
            writer_epoch=1,
        )
        connection = sqlite3.connect(self.database_path)
        try:
            body = json.loads(
                connection.execute(
                    "SELECT body_json FROM events WHERE event_id = ?",
                    ("plan-event-1",),
                ).fetchone()[0]
            )
            del body["lifecycle_from"]
            event_hash = self.store._event_hash(body)
            body_json = json.dumps(
                body, sort_keys=True, separators=(",", ":")
            )
            connection.execute(
                "UPDATE events SET event_hash = ?, body_json = ? WHERE event_id = ?",
                (event_hash, body_json, "plan-event-1"),
            )
            connection.execute(
                "UPDATE validation_plans SET event_hash = ?, body_json = ? "
                "WHERE plan_id = ?",
                (event_hash, body_json, "plan-1"),
            )
            connection.execute(
                "UPDATE command_outcomes SET event_hash = ? WHERE command_id = ?",
                (event_hash, "plan-command-1"),
            )
            connection.execute(
                "UPDATE runs SET head_hash = ? WHERE run_id = ?",
                (event_hash, "run-1"),
            )
            connection.execute(
                "UPDATE repositories SET catalog_head = ? WHERE repository_id = ?",
                (event_hash, "repo-1"),
            )
            connection.commit()
        finally:
            connection.close()
        self.oracle.allowed_head = event_hash

        with self.assertRaisesRegex(StorageIntegrityError, "lifecycle schema"):
            self.store.load_verified("repo-1")

    def test_t02_readiness_is_atomic_replay_safe_and_reversible(self) -> None:
        accepted = self.store.accept_plan(
            PlanAcceptanceRequest(
                "plan-1", "plan-command-1", "plan-event-1", "repo-1",
                "run-1", "item-1", "effect-1", "revision-1",
                "descriptor-digest", "scope-1", "budget-policy-digest",
                ("check-1",),
            ),
            expected_head="", writer_epoch=1,
        )
        self.oracle.allowed_head = accepted.event_hash
        blocked_request = ReadinessEvaluationRequest(
            "readiness-1", "readiness-command-1", "readiness-event-1",
            "repo-1", "run-1", "item-1", "plan-1", "revision-1",
            accepted.event_hash, None, "inputs-evidence-1", False,
        )
        with self.assertRaises(InjectedFailure):
            self.store.evaluate_readiness(
                blocked_request,
                failure_hook=raise_at("after_readiness_writes_before_commit"),
            )
        self.assertEqual(self.store.table_counts()["readiness_evaluations"], 0)
        blocked = self.store.evaluate_readiness(blocked_request)
        self.oracle.allowed_head = blocked.event_hash
        self.assertEqual(blocked.resulting_state, LifecycleState.BLOCKED)
        replay = self.store.evaluate_readiness(blocked_request)
        self.assertTrue(replay.replayed)
        ready_request = ReadinessEvaluationRequest(
            "readiness-2", "readiness-command-2", "readiness-event-2",
            "repo-1", "run-1", "item-1", "plan-1", "revision-1",
            blocked.event_hash, None, "inputs-evidence-2", True,
        )
        ready = self.store.evaluate_readiness(ready_request)
        self.oracle.allowed_head = ready.event_hash
        self.assertEqual(ready.resulting_state, LifecycleState.PLANNED)
        self.store.load_verified("repo-1")

    def test_t02_cannot_clear_t16_recovery_blocker(self) -> None:
        _, failed = self._prepare_recoverable_application()
        request = ReadinessEvaluationRequest(
            "readiness-1", "readiness-command-1", "readiness-event-1",
            "repo-1", "run-1", "item-1", "plan-1", "revision-1",
            failed.event_hash, LifecycleState.VALIDATING.value,
            "inputs-evidence-1", True,
        )
        evaluated = self.store.evaluate_readiness(request)
        self.oracle.allowed_head = evaluated.event_hash

        self.assertEqual(evaluated.resulting_state, LifecycleState.BLOCKED)
        connection = sqlite3.connect(self.database_path)
        try:
            state, cursor = connection.execute(
                "SELECT lifecycle_state, continuation_cursor FROM runs "
                "WHERE run_id = 'run-1'"
            ).fetchone()
        finally:
            connection.close()
        self.assertEqual(state, LifecycleState.BLOCKED.value)
        self.assertEqual(cursor, LifecycleState.VALIDATING.value)
        self.store.load_verified("repo-1")

    def test_t02_unknown_cursor_fails_closed_before_append(self) -> None:
        accepted = self.store.accept_plan(
            PlanAcceptanceRequest(
                "plan-1", "plan-command-1", "plan-event-1", "repo-1",
                "run-1", "item-1", "effect-1", "revision-1",
                "descriptor-digest", "scope-1", "budget-policy-digest",
                ("check-1",),
            ),
            expected_head="", writer_epoch=1,
        )
        self.oracle.allowed_head = accepted.event_hash
        connection = sqlite3.connect(self.database_path)
        try:
            connection.execute(
                "UPDATE runs SET lifecycle_state = 'BLOCKED', "
                "continuation_cursor = 'unknown:obligation' WHERE run_id = 'run-1'"
            )
            connection.commit()
        finally:
            connection.close()

        with self.assertRaisesRegex(StorageIntegrityError, "lifecycle|cursor"):
            self.store.evaluate_readiness(
                ReadinessEvaluationRequest(
                    "readiness-1", "readiness-command-1", "readiness-event-1",
                    "repo-1", "run-1", "item-1", "plan-1", "revision-1",
                    accepted.event_hash, "unknown:obligation",
                    "inputs-evidence-1", True,
                )
            )
        self.assertEqual(self.store.table_counts()["readiness_evaluations"], 0)

    def test_t02_repository_slot_in_another_run_blocks_readiness(self) -> None:
        committed = self._commit_planned_intent(
            self.request(), self.capability, self.authority,
            expected_head="", writer_epoch=1,
        )
        self.oracle.allowed_head = committed.event_hash
        accepted = self.store.accept_plan(
            PlanAcceptanceRequest(
                "plan-2", "plan-command-2", "plan-event-2", "repo-1",
                "run-2", "item-2", "effect-2", "revision-2",
                "descriptor-2", "scope-2", "budget-policy-2", ("check-2",),
            ),
            expected_head=committed.event_hash, writer_epoch=3,
        )
        self.oracle.allowed_head = accepted.event_hash

        evaluated = self.store.evaluate_readiness(
            ReadinessEvaluationRequest(
                "readiness-2", "readiness-command-2", "readiness-event-2",
                "repo-1", "run-2", "item-2", "plan-2", "revision-2",
                accepted.event_hash, None, "inputs-evidence-2", True,
            )
        )

        self.assertEqual(evaluated.resulting_state, LifecycleState.BLOCKED)
        connection = sqlite3.connect(self.database_path)
        try:
            blocker_codes = json.loads(
                connection.execute(
                    "SELECT body_json FROM readiness_evaluations WHERE "
                    "readiness_id = 'readiness-2'"
                ).fetchone()[0]
            )["blocker_codes"]
        finally:
            connection.close()
        self.assertIn("OPERATION_SLOT_OCCUPIED", blocker_codes)

    def test_t02_historical_cross_run_fence_survives_later_clearance(self) -> None:
        request, attestation = self._prepare_finalization()
        finalized = self.store._finalize_operation(
            request, attestation, self.authority
        )
        self.oracle.allowed_head = finalized.event_hash
        connection = sqlite3.connect(self.database_path)
        try:
            previous_hash = connection.execute(
                "SELECT settlement_head_hash FROM budget_reservations "
                "WHERE reservation_id = 'reservation-1'"
            ).fetchone()[0]
        finally:
            connection.close()
        unknown = BudgetSettlementRequest(
            "late-unknown", "reservation-1", previous_hash,
            BudgetDisposition.UNKNOWN_WORST_CASE_CHARGED, None,
            "late-unknown-evidence", "ADDITIONAL_LIABILITY_UNKNOWN",
            additional_liability=True,
        )
        unknown_receipt = self.store._settle_budget(
            unknown,
            self.authority.issue_settlement_proof("late-unknown-proof", unknown),
            self.authority,
        )
        self.oracle.allowed_head = unknown_receipt.settlement_hash
        accepted = self.store.accept_plan(
            PlanAcceptanceRequest(
                "plan-2", "plan-command-2", "plan-event-2", "repo-1",
                "run-2", "item-2", "effect-2", "revision-2",
                "descriptor-2", "scope-2", "budget-policy-2", ("check-2",),
            ),
            expected_head=unknown_receipt.settlement_hash, writer_epoch=100,
        )
        self.oracle.allowed_head = accepted.event_hash
        evaluated = self.store.evaluate_readiness(
            ReadinessEvaluationRequest(
                "readiness-2", "readiness-command-2", "readiness-event-2",
                "repo-1", "run-2", "item-2", "plan-2", "revision-2",
                accepted.event_hash, None, "inputs-evidence-2", True,
            )
        )
        self.assertEqual(evaluated.resulting_state, LifecycleState.BLOCKED)

        self.oracle.allowed_head = evaluated.event_hash
        correction = BudgetSettlementRequest(
            "late-correction", "reservation-1",
            unknown_receipt.settlement_hash, BudgetDisposition.ADJUSTED, 3,
            "late-authoritative-evidence", "AUTHORITATIVE_CORRECTION",
        )
        corrected = self.store._settle_budget(
            correction,
            self.authority.issue_settlement_proof(
                "late-correction-proof", correction
            ),
            self.authority,
        )
        self.oracle.allowed_head = corrected.settlement_hash
        self.assertEqual(self.store.table_counts()["dispatch_fences"], 0)
        self.store.load_verified("repo-1")

    def test_t02_missing_slot_reservation_fails_closed(self) -> None:
        committed = self._commit_planned_intent(
            self.request(), self.capability, self.authority,
            expected_head="", writer_epoch=1,
        )
        self.oracle.allowed_head = committed.event_hash
        accepted = self.store.accept_plan(
            PlanAcceptanceRequest(
                "plan-2", "plan-command-2", "plan-event-2", "repo-1",
                "run-2", "item-2", "effect-2", "revision-2",
                "descriptor-2", "scope-2", "budget-policy-2", ("check-2",),
            ),
            expected_head=committed.event_hash, writer_epoch=3,
        )
        self.oracle.allowed_head = accepted.event_hash
        connection = sqlite3.connect(self.database_path)
        try:
            connection.execute(
                "DELETE FROM budget_reservations WHERE reservation_id = "
                "'reservation-1'"
            )
            connection.commit()
        finally:
            connection.close()

        with self.assertRaisesRegex(StorageIntegrityError, "budget projection"):
            self.store.evaluate_readiness(
                ReadinessEvaluationRequest(
                    "readiness-2", "readiness-command-2", "readiness-event-2",
                    "repo-1", "run-2", "item-2", "plan-2", "revision-2",
                    accepted.event_hash, None, "inputs-evidence-2", True,
                )
            )
        self.assertEqual(self.store.table_counts()["readiness_evaluations"], 0)

    def test_repository_writer_epoch_must_advance(self) -> None:
        accepted = self.store.accept_plan(
            PlanAcceptanceRequest(
                "plan-1", "plan-command-1", "plan-event-1", "repo-1",
                "run-1", "item-1", "effect-1", "revision-1",
                "descriptor-digest", "scope-1", "budget-policy-digest",
                ("check-1",),
            ),
            expected_head="", writer_epoch=1,
        )
        self.oracle.allowed_head = accepted.event_hash
        with self.assertRaisesRegex(DispatchDenied, "writer epoch"):
            self.store.accept_plan(
                PlanAcceptanceRequest(
                    "plan-2", "plan-command-2", "plan-event-2", "repo-1",
                    "run-2", "item-2", "effect-2", "revision-2",
                    "descriptor-2", "scope-2", "budget-policy-2", ("check-2",),
                ),
                expected_head=accepted.event_hash, writer_epoch=1,
            )

        with self.assertRaisesRegex(DispatchDenied, "writer epoch"):
            self.store.commit_intent(
                self.request(), self.capability, self.authority,
                expected_head=accepted.event_hash, writer_epoch=1,
            )
        self.assertEqual(self.store.table_counts()["events"], 1)

    def test_recovery_rejects_reused_repository_writer_epoch(self) -> None:
        first = self.store.accept_plan(
            PlanAcceptanceRequest(
                "plan-1", "plan-command-1", "plan-event-1", "repo-1",
                "run-1", "item-1", "effect-1", "revision-1",
                "descriptor-1", "scope-1", "budget-policy-1", ("check-1",),
            ),
            expected_head="", writer_epoch=1,
        )
        self.oracle.allowed_head = first.event_hash
        second = self.store.accept_plan(
            PlanAcceptanceRequest(
                "plan-2", "plan-command-2", "plan-event-2", "repo-1",
                "run-2", "item-2", "effect-2", "revision-2",
                "descriptor-2", "scope-2", "budget-policy-2", ("check-2",),
            ),
            expected_head=first.event_hash, writer_epoch=2,
        )
        connection = sqlite3.connect(self.database_path)
        try:
            body = json.loads(
                connection.execute(
                    "SELECT body_json FROM events WHERE event_id = 'plan-event-2'"
                ).fetchone()[0]
            )
            body["writer_epoch"] = 1
            event_hash = self.store._event_hash(body)
            body_json = json.dumps(
                body, sort_keys=True, separators=(",", ":")
            )
            connection.execute(
                "UPDATE events SET writer_epoch = 1, event_hash = ?, "
                "body_json = ? WHERE event_id = 'plan-event-2'",
                (event_hash, body_json),
            )
            connection.execute(
                "UPDATE validation_plans SET event_hash = ?, body_json = ? "
                "WHERE plan_id = 'plan-2'",
                (event_hash, body_json),
            )
            connection.execute(
                "UPDATE command_outcomes SET event_hash = ? WHERE "
                "command_id = 'plan-command-2'",
                (event_hash,),
            )
            connection.execute(
                "UPDATE runs SET head_hash = ? WHERE run_id = 'run-2'",
                (event_hash,),
            )
            connection.execute(
                "UPDATE repositories SET catalog_head = ? WHERE "
                "repository_id = 'repo-1'",
                (event_hash,),
            )
            connection.commit()
        finally:
            connection.close()
        self.oracle.allowed_head = event_hash

        with self.assertRaisesRegex(StorageIntegrityError, "writer epoch"):
            self.store.load_verified("repo-1")

    def test_t16_schema_migrates_populated_pre_t16_plan_fail_closed(self) -> None:
        accepted = self.store.accept_plan(
            PlanAcceptanceRequest(
                "plan-1", "plan-command-1", "plan-event-1", "repo-1",
                "run-1", "item-1", "effect-1", "revision-1",
                "descriptor-digest", "scope-1", "budget-policy-digest",
                ("check-1",),
            ),
            expected_head="",
            writer_epoch=1,
        )
        connection = sqlite3.connect(self.database_path)
        try:
            body = json.loads(
                connection.execute(
                    "SELECT body_json FROM events WHERE event_id = 'plan-event-1'"
                ).fetchone()[0]
            )
            for key in (
                "effect_descriptor_digest", "permission_scope_digest",
                "budget_policy_digest",
                "aggregate_gate_ids", "gate_set_digest",
                "finalization_policy_id", "finalization_policy_version",
                "finalization_issuer_fingerprint",
                "failure_policy_id", "failure_policy_version",
                "source_tree_digest", "item_definition_digest",
                "plan_schema_version", "reducer_version",
                "accepted_plan_semantic_digest", "complete_policy_digest",
            ):
                body.pop(key)
            body_json = json.dumps(body, sort_keys=True, separators=(",", ":"))
            event_hash = self.store._event_hash(body)
            payload_digest = self.store._event_hash(
                {
                    key: body[key]
                    for key in PlanAcceptanceContract.__dataclass_fields__
                    if key in body
                }
            )
            connection.execute(
                "UPDATE events SET event_hash = ?, body_json = ? WHERE event_id = ?",
                (event_hash, body_json, "plan-event-1"),
            )
            connection.execute(
                "UPDATE validation_plans SET payload_digest = ?, event_hash = ?, "
                "body_json = ? WHERE plan_id = 'plan-1'",
                (payload_digest, event_hash, body_json),
            )
            connection.execute(
                "UPDATE command_outcomes SET payload_digest = ?, event_hash = ? "
                "WHERE command_id = 'plan-command-1'",
                (payload_digest, event_hash),
            )
            connection.execute(
                "UPDATE runs SET head_hash = ? WHERE run_id = 'run-1'",
                (event_hash,),
            )
            connection.execute(
                "UPDATE repositories SET catalog_head = ? WHERE repository_id = 'repo-1'",
                (event_hash,),
            )
            connection.execute("PRAGMA foreign_keys = OFF")
            connection.execute("DROP TABLE operation_finalizations")
            connection.execute("ALTER TABLE runs DROP COLUMN continuation_cursor")
            for column_name in (
                "effect_descriptor_digest", "permission_scope_digest",
                "budget_policy_digest",
                "aggregate_gate_ids_json", "gate_set_digest",
                "finalization_policy_id", "finalization_policy_version",
                "finalization_issuer_fingerprint",
                "source_tree_digest", "item_definition_digest",
                "plan_schema_version", "reducer_version",
                "accepted_plan_semantic_digest", "complete_policy_digest",
            ):
                connection.execute(
                    f"ALTER TABLE validation_plans DROP COLUMN {column_name}"
                )
            connection.commit()
        finally:
            connection.close()
        self.oracle.allowed_head = event_hash
        migrated = SQLiteStateStore(
            self.database_path, self.oracle, "repo-1"
        )
        migrated._bind_classification_authority(self.authority)
        migrated.load_verified("repo-1")
        connection = sqlite3.connect(self.database_path)
        try:
            run_columns = {
                row[1] for row in connection.execute("PRAGMA table_info(runs)")
            }
            plan_columns = {
                row[1]
                for row in connection.execute(
                    "PRAGMA table_info(validation_plans)"
                )
            }
            gate_json = connection.execute(
                "SELECT aggregate_gate_ids_json FROM validation_plans"
            ).fetchone()[0]
            migrated_bindings = connection.execute(
                "SELECT source_tree_digest, item_definition_digest, "
                "plan_schema_version, reducer_version, "
                "accepted_plan_semantic_digest, complete_policy_digest "
                "FROM validation_plans"
            ).fetchone()
        finally:
            connection.close()
        self.assertIn("continuation_cursor", run_columns)
        self.assertIn("finalization_issuer_fingerprint", plan_columns)
        self.assertIsNone(gate_json)
        self.assertEqual(migrated_bindings, (None,) * 6)
        self.assertNotEqual(accepted.event_hash, event_hash)
        connection = sqlite3.connect(self.database_path)
        try:
            before_denial = tuple(connection.iterdump())
        finally:
            connection.close()
        with self.assertRaisesRegex(
            StorageIntegrityError, "command ID was reused with a different payload"
        ):
            migrated.accept_plan(
                PlanAcceptanceRequest(
                    "plan-1", "plan-command-1", "plan-event-1", "repo-1",
                    "run-1", "item-1", "effect-1", "revision-1",
                    "descriptor-digest", "scope-1", "budget-policy-digest",
                    ("check-1",),
                ),
                expected_head=event_hash,
                writer_epoch=2,
            )
        with self.assertRaisesRegex(
            DispatchDenied, "predates required finalization pins"
        ):
            migrated.commit_intent(
                self.request(), self.capability, self.authority,
                expected_head=event_hash, writer_epoch=2,
            )
        connection = sqlite3.connect(self.database_path)
        try:
            after_denial = tuple(connection.iterdump())
        finally:
            connection.close()
        self.assertEqual(after_denial, before_denial)

    def _pause_capability(self, suffix: str = "1"):
        grant = SyntheticOperatorGrant(
            f"operator-grant-{suffix}", "repo-1", "run-1", "PAUSE",
            f"operator-scope-{suffix}",
        )
        self.authority.register_operator(grant)
        return self.authority.claim_operator(
            grant.grant_id, grant.repository_id, grant.run_id, grant.action,
            grant.scope_digest,
        )

    @staticmethod
    def _pause_request(suffix: str = "1") -> PauseBeforeDispatchRequest:
        return PauseBeforeDispatchRequest(
            f"pause-{suffix}", f"pause-command-{suffix}",
            f"pause-request-event-{suffix}", f"pause-settled-event-{suffix}",
            f"pause-fence-{suffix}", "repo-1", "run-1", "item-1",
            "OPERATOR_PAUSE", None,
        )

    @staticmethod
    def _resume_request(
        *,
        catalog_head: str,
        run_heads_digest: str,
        suffix: str = "1",
    ) -> ResumeRequest:
        return ResumeRequest(
            f"resume-{suffix}", f"resume-command-{suffix}",
            f"resume-event-{suffix}", "repo-1", "run-1", "item-1",
            "effect-1", "plan-1", "revision-1", f"pause-{suffix}",
            f"pause-settled-event-{suffix}", catalog_head,
            f"pause-fence-{suffix}", LifecycleState.PLANNED, None,
            catalog_head, catalog_head, run_heads_digest,
        )

    def test_t14_resume_request_has_exact_signed_evidence(self) -> None:
        request = self._resume_request(
            catalog_head="pause-settled-hash-1",
            run_heads_digest="run-heads-digest-1",
        )
        self.assertTrue(
            hasattr(self.authority, "issue_resume_evidence"),
            "T14 requires exact signed resume evidence",
        )
        evidence = self.authority.issue_resume_evidence("resume-proof-1", request)
        self.authority.verify_resume_evidence(evidence, request)
        with self.assertRaisesRegex(DispatchDenied, "resume evidence"):
            self.authority.verify_resume_evidence(
                evidence,
                replace(request, expected_run_head="other-head"),
            )

    def _stop_capability(self, mode: StopMode, suffix: str = "1"):
        action = (
            "STOP_GRACEFUL"
            if mode is StopMode.GRACEFUL
            else "STOP_IMMEDIATE"
        )
        grant = SyntheticOperatorGrant(
            f"stop-grant-{suffix}", "repo-1", "run-1", action,
            f"stop-scope-{suffix}",
        )
        self.authority.register_operator(grant)
        return self.authority.claim_operator(
            grant.grant_id, grant.repository_id, grant.run_id, grant.action,
            grant.scope_digest,
        )

    @staticmethod
    def _local_pause_request(
        committed,
        *,
        suffix: str = "1",
        expected_slot_generation: int = 1,
    ) -> PauseLocalExecutionRequest:
        return PauseLocalExecutionRequest(
            f"local-pause-{suffix}", f"local-pause-command-{suffix}",
            f"local-pause-event-{suffix}", f"local-pause-fence-{suffix}",
            "repo-1", "run-1", "item-1", "effect-1", "attempt-1",
            committed.event_id, committed.event_hash,
            expected_slot_generation, "OPERATOR_PAUSE_LOCAL_EXECUTION",
        )

    def _running_operation(self):
        committed = self._commit_planned_intent(
            self.request(), self.capability, self.authority,
            expected_head="", writer_epoch=1,
        )
        self.oracle.allowed_head = committed.event_hash
        return committed

    def _contacted_operation(self, suffix: str = "1"):
        committed = self._running_operation()
        launched = self.store.claim_operation_launch(self.request(), committed)
        self.oracle.allowed_head = launched.event_hash
        self.store._contact_claimed_operation(
            self.request(), self.capability, committed, launched,
            self.store._adapter_target_digest("repo-1", "EFFECT"),
        )
        connection = sqlite3.connect(self.database_path)
        connection.row_factory = sqlite3.Row
        try:
            contact = connection.execute(
                "SELECT * FROM adapter_contacts WHERE run_id = 'run-1'"
            ).fetchone()
            self.oracle.allowed_head = connection.execute(
                "SELECT catalog_head FROM repositories WHERE repository_id = "
                "'repo-1'"
            ).fetchone()[0]
        finally:
            connection.close()
        request = PauseExternalMutationRequest(
            f"external-pause-{suffix}", f"external-pause-command-{suffix}",
            f"external-pause-event-{suffix}",
            f"external-pause-fence-{suffix}", "repo-1", "run-1", "item-1",
            "effect-1", "attempt-1", committed.event_id,
            committed.event_hash, launched.launch_id, launched.event_id,
            launched.event_hash, contact["contact_id"], contact["event_id"],
            contact["event_hash"], contact["target_digest"], 1,
            "OPERATOR_PAUSE_EXTERNAL_MUTATION",
        )
        return committed, launched, contact, request

    def test_t05_pauses_owned_prelaunch_attempt_and_retains_obligations(self) -> None:
        committed = self._running_operation()
        receipt = self.store.pause_local_execution(
            self._local_pause_request(committed), self._pause_capability(),
            self.authority,
        )
        self.assertEqual(receipt.resulting_state, LifecycleState.PAUSING)
        self.assertFalse(receipt.replayed)
        connection = sqlite3.connect(self.database_path)
        try:
            state = connection.execute(
                "SELECT lifecycle_state FROM runs WHERE run_id = 'run-1'"
            ).fetchone()[0]
            slot = connection.execute(
                "SELECT run_id, logical_effect_id, attempt_id, generation "
                "FROM outstanding_slot"
            ).fetchone()
            reservation = connection.execute(
                "SELECT disposition, held_units, charged_units FROM "
                "budget_reservations WHERE reservation_id = 'reservation-1'"
            ).fetchone()
            fence = connection.execute(
                "SELECT item_id, logical_effect_id FROM dispatch_fences "
                "WHERE fence_id = 'local-pause-fence-1'"
            ).fetchone()
        finally:
            connection.close()
        self.assertEqual(state, "PAUSING")
        self.assertEqual(slot, ("run-1", "effect-1", "attempt-1", 1))
        self.assertEqual(reservation, ("RESERVED", 3, 0))
        self.assertEqual(fence, ("item-1", "effect-1"))

    def test_t06_exact_contact_history_survives_verified_recovery(self) -> None:
        _, _, _, request = self._contacted_operation("recovery")
        receipt = self.store.pause_external_mutation(
            request, self._pause_capability("external-recovery"), self.authority
        )
        self.oracle.allowed_head = receipt.event_hash
        self.store.load_verified("repo-1", authority=self.authority)
        self.assertEqual(
            receipt.resulting_state, LifecycleState.RECONCILIATION_REQUIRED
        )

    def test_t25_contacted_nonexecution_clears_exact_uncertainty_and_pauses(
        self,
    ) -> None:
        _, launched, _, pause_request = self._contacted_operation(
            "proven-nonexecution"
        )
        pause = self.store.pause_external_mutation(
            pause_request,
            self._pause_capability("proven-nonexecution"),
            self.authority,
        )
        self.oracle.allowed_head = pause.event_hash
        target_path = self.database_path.parent / "synthetic-target.sqlite3"
        adapter = SyntheticExecutionAdapter(target_path)
        adapter._canonical_repository_id = "repo-1"
        adapter._canonical_ledger_path = target_path.resolve()
        attestation = self.authority.issue_nonexecution_attestation(
            "contacted-nonexecution-attestation",
            "contacted-nonexecution-seal", "EFFECT",
            adapter._target_digest("repo-1"), self.capability.claim_id,
            f"EFFECT:{launched.launch_id}", launched.event_hash,
            "reservation-1", "repo-1", "run-1", "item-1", "effect-1",
            "attempt-1",
        )
        seal = adapter.seal_nonexecution(attestation, self.authority)
        connection = sqlite3.connect(self.database_path)
        try:
            settlement_head = connection.execute(
                "SELECT settlement_head_hash FROM budget_reservations WHERE "
                "reservation_id = 'reservation-1'"
            ).fetchone()[0]
        finally:
            connection.close()
        request = BudgetSettlementRequest(
            "contacted-nonexecution", "reservation-1", settlement_head,
            BudgetDisposition.RELEASED, None,
            "contacted-nonexecution-evidence", "NONDISPATCH_PROVEN",
            non_dispatch_proven=True, zero_liability_proven=True,
            release_slot=False, all_obligations_settled=True,
            nonexecution_seal_id=seal.seal_id,
        )
        settled = self.store._settle_budget(
            request,
            self.authority.issue_settlement_proof(
                "contacted-nonexecution-proof", request
            ),
            self.authority,
        )
        self.oracle.allowed_head = settled.settlement_hash
        connection = sqlite3.connect(self.database_path)
        try:
            run = connection.execute(
                "SELECT lifecycle_state, continuation_cursor FROM runs WHERE "
                "run_id = 'run-1'"
            ).fetchone()
            operation_fences = connection.execute(
                "SELECT COUNT(*) FROM dispatch_fences WHERE reason_code IN ("
                "'OPERATION_OUTCOME_UNKNOWN', 'OPERATION_ACTIVITY_UNKNOWN', "
                "'EFFECT_BILLING_UNKNOWN', 'EFFECT_SOURCE_CONTROL_UNKNOWN')"
            ).fetchone()[0]
            pause_fence = connection.execute(
                "SELECT COUNT(*) FROM dispatch_fences WHERE fence_id = ?",
                (pause_request.fence_id,),
            ).fetchone()[0]
            resolutions = connection.execute(
                "SELECT COUNT(*) FROM uncertainty_resolutions WHERE "
                "reconciliation_id = ?",
                ("proven-nonexecution:contacted-nonexecution",),
            ).fetchone()[0]
            action = connection.execute(
                "SELECT path_class, resulting_state FROM "
                "proven_nonexecution_actions WHERE settlement_event_id = ?",
                ("contacted-nonexecution",),
            ).fetchone()
        finally:
            connection.close()
        self.assertEqual(run, ("PAUSED", "operation-recovery:attempt-1"))
        self.assertEqual(operation_fences, 0)
        self.assertEqual(pause_fence, 1)
        self.assertEqual(resolutions, 4)
        self.assertEqual(action, ("CONTACTED", "PAUSED"))
        self.store.load_verified("repo-1", authority=self.authority)

        backfill_path = self.database_path.parent / "v2-t25-backfill.sqlite3"
        shutil.copy2(self.database_path, backfill_path)

        def downgrade_t25_fixture(path: Path) -> None:
            connection = sqlite3.connect(path)
            connection.row_factory = sqlite3.Row
            try:
                uncertainty_rows = connection.execute(
                    "SELECT instance.* FROM uncertainty_instances AS instance "
                    "JOIN uncertainty_resolutions AS resolution ON "
                    "resolution.uncertainty_id = instance.uncertainty_id "
                    "WHERE resolution.reconciliation_id = "
                    "'proven-nonexecution:contacted-nonexecution'"
                ).fetchall()
                reason_codes = {
                    "OUTCOME": "OPERATION_OUTCOME_UNKNOWN",
                    "ACTIVITY": "OPERATION_ACTIVITY_UNKNOWN",
                    "BILLING": "EFFECT_BILLING_UNKNOWN",
                    "SOURCE_CONTROL": "EFFECT_SOURCE_CONTROL_UNKNOWN",
                }
                connection.execute(
                    "DELETE FROM uncertainty_resolutions WHERE "
                    "reconciliation_id = "
                    "'proven-nonexecution:contacted-nonexecution'"
                )
                for row in uncertainty_rows:
                    connection.execute(
                        "INSERT INTO dispatch_fences VALUES (?, 'repo-1', "
                        "'item-1', 'effect-1', ?, ?)",
                        (
                            row["fence_id"],
                            reason_codes[row["uncertainty_kind"]],
                            row["origin_event_id"],
                        ),
                    )
                connection.execute(
                    "DROP TABLE operation_retry_authorizations"
                )
                connection.execute("DROP TABLE operation_recovery_actions")
                connection.execute(
                    "DROP TABLE operation_nonexecution_resume_actions"
                )
                connection.execute("DROP TABLE proven_nonexecution_actions")
                strip_t28_foundation_schema(connection)
                connection.execute("PRAGMA user_version = 2")
                connection.commit()
            finally:
                connection.close()

        downgrade_t25_fixture(backfill_path)
        backfill_oracle = MutableFreshnessOracle()
        backfill_oracle.allowed_head = settled.settlement_hash
        migrated = SQLiteStateStore(backfill_path, backfill_oracle, "repo-1")
        migrated._bind_classification_authority(self.authority)
        migrated.load_verified("repo-1", authority=self.authority)
        connection = sqlite3.connect(backfill_path)
        try:
            migrated_state = (
                connection.execute("PRAGMA user_version").fetchone()[0],
                connection.execute(
                    "SELECT COUNT(*) FROM proven_nonexecution_actions"
                ).fetchone()[0],
                connection.execute(
                    "SELECT COUNT(*) FROM uncertainty_resolutions WHERE "
                    "reconciliation_id = "
                    "'proven-nonexecution:contacted-nonexecution'"
                ).fetchone()[0],
                connection.execute(
                    "SELECT COUNT(*) FROM dispatch_fences WHERE reason_code IN "
                    "('OPERATION_OUTCOME_UNKNOWN', "
                    "'OPERATION_ACTIVITY_UNKNOWN', 'EFFECT_BILLING_UNKNOWN', "
                    "'EFFECT_SOURCE_CONTROL_UNKNOWN')"
                ).fetchone()[0],
            )
        finally:
            connection.close()
        self.assertEqual(migrated_state, (5, 1, 4, 0))

        late_observation = self._record_signed_effect_observation(
            EffectObservationRequest(
                "backfill-late-observation", "backfill-late-command",
                "backfill-late-event", "repo-1", "run-1", "item-1",
                "effect-1", "attempt-1", "backfill-late-receipt",
                self.capability.claim_id, "descriptor-digest", 0,
                "backfill-late-settlement", "",
            ),
            classification=SourceControlClassification.UNKNOWN,
            store=migrated,
        )
        backfill_oracle.allowed_head = late_observation.event_hash
        migrated.load_verified("repo-1", authority=self.authority)
        connection = sqlite3.connect(backfill_path)
        try:
            later_uncertainty_ids = tuple(
                row[0]
                for row in connection.execute(
                    "SELECT uncertainty_id FROM uncertainty_instances WHERE "
                    "origin_event_id = ? ORDER BY uncertainty_id",
                    (late_observation.event_id,),
                )
            )
        finally:
            connection.close()
        self.assertTrue(later_uncertainty_ids)

        downgrade_t25_fixture(backfill_path)
        later_resolution_path = (
            self.database_path.parent / "v2-t25-later-resolution.sqlite3"
        )
        shutil.copy2(backfill_path, later_resolution_path)
        connection = sqlite3.connect(later_resolution_path)
        try:
            uncertainty_id, fence_id = connection.execute(
                "SELECT uncertainty_id, fence_id FROM uncertainty_instances "
                "WHERE origin_event_id = ? ORDER BY uncertainty_id LIMIT 1",
                (pause_request.event_id,),
            ).fetchone()
            connection.execute(
                "DELETE FROM dispatch_fences WHERE fence_id = ?", (fence_id,)
            )
            later_resolution_body = json.dumps(
                {
                    "event_id": late_observation.event_id,
                    "proof_event_hash": late_observation.event_hash,
                    "proof_event_id": late_observation.event_id,
                    "proof_kind": "LATER_OWNER",
                    "reconciliation_id": "later-owner",
                    "schema_version": 1,
                    "uncertainty_id": uncertainty_id,
                },
                sort_keys=True,
                separators=(",", ":"),
            )
            connection.execute(
                "INSERT INTO uncertainty_resolutions VALUES (?, ?, ?, ?, ?, "
                "?, ?)",
                (
                    uncertainty_id, "later-owner", late_observation.event_id,
                    "LATER_OWNER", late_observation.event_id,
                    late_observation.event_hash, later_resolution_body,
                ),
            )
            connection.commit()
            before_failed_migration = tuple(connection.iterdump())
            connection.row_factory = sqlite3.Row
            with self.assertRaisesRegex(
                StorageIntegrityError, "later resolution ownership"
            ):
                SQLiteStateStore._migrate_proven_nonexecution_version(
                    connection
                )
            after_failed_migration = tuple(connection.iterdump())
        finally:
            connection.close()
        self.assertEqual(after_failed_migration, before_failed_migration)

        remigrated = SQLiteStateStore(
            backfill_path, backfill_oracle, "repo-1"
        )
        remigrated._bind_classification_authority(self.authority)
        remigrated.load_verified("repo-1", authority=self.authority)
        connection = sqlite3.connect(backfill_path)
        try:
            resolved_by_t25 = tuple(json.loads(connection.execute(
                "SELECT resolved_uncertainty_ids_json FROM "
                "proven_nonexecution_actions WHERE settlement_event_id = "
                "'contacted-nonexecution'"
            ).fetchone()[0]))
            surviving_later_fences = connection.execute(
                "SELECT COUNT(*) FROM uncertainty_instances AS instance JOIN "
                "dispatch_fences AS fence ON fence.fence_id = "
                "instance.fence_id WHERE instance.uncertainty_id IN ("
                + ",".join("?" for _ in later_uncertainty_ids)
                + ")",
                later_uncertainty_ids,
            ).fetchone()[0]
        finally:
            connection.close()
        self.assertTrue(set(resolved_by_t25).isdisjoint(later_uncertainty_ids))
        self.assertEqual(surviving_later_fences, len(later_uncertainty_ids))

        grant = SyntheticOperatorGrant(
            "resume-nonexecution-grant", "repo-1", "run-1", "RESUME",
            "resume-nonexecution-scope",
        )
        self.authority.register_operator(grant)
        capability = self.authority.claim_operator(*grant.__dict__.values())
        connection = sqlite3.connect(self.database_path)
        try:
            catalog_head = connection.execute(
                "SELECT catalog_head FROM repositories WHERE repository_id = "
                "'repo-1'"
            ).fetchone()[0]
            run_head = connection.execute(
                "SELECT head_hash FROM runs WHERE run_id = 'run-1'"
            ).fetchone()[0]
            resolved_ids = tuple(
                row[0] for row in connection.execute(
                    "SELECT uncertainty_id FROM uncertainty_resolutions WHERE "
                    "reconciliation_id = ? ORDER BY uncertainty_id",
                    ("proven-nonexecution:contacted-nonexecution",),
                )
            )
        finally:
            connection.close()
        resume_request = ResumeOperationNonexecutionRequest(
            "resume-nonexecution", "resume-nonexecution-command",
            "resume-nonexecution-event", "repo-1", "run-1", "item-1",
            "effect-1", "attempt-1", "plan:run-1", "revision-1",
            "descriptor-digest", pause_request.pause_id,
            pause_request.event_id, pause.event_hash, pause_request.fence_id,
            "contacted-nonexecution", settled.settlement_hash,
            "reservation-1", settled.settlement_hash, resolved_ids,
            "operation-recovery:attempt-1", "attempt-1", 1,
            catalog_head, run_head,
            self.store._run_heads_digest({"run-1": run_head}),
        )
        resume_evidence = (
            self.authority.issue_operation_nonexecution_resume_evidence(
                "resume-nonexecution-proof", resume_request
            )
        )
        with self.assertRaises(InjectedFailure):
            self.store.resume_operation_nonexecution(
                resume_request, capability, resume_evidence, self.authority,
                failure_hook=raise_at(
                    "after_operation_nonexecution_resume_commit_before_acknowledgement"
                ),
            )
        resume = self.store.resume_operation_nonexecution(
            resume_request, capability,
            resume_evidence, self.authority,
        )
        self.assertTrue(resume.replayed)
        self.oracle.allowed_head = resume.event_hash
        self.assertEqual(resume.resulting_state, LifecycleState.BLOCKED)
        connection = sqlite3.connect(self.database_path)
        try:
            run = connection.execute(
                "SELECT lifecycle_state, continuation_cursor FROM runs WHERE "
                "run_id = 'run-1'"
            ).fetchone()
            pause_fence = connection.execute(
                "SELECT COUNT(*) FROM dispatch_fences WHERE fence_id = ?",
                (pause_request.fence_id,),
            ).fetchone()[0]
            slot = connection.execute(
                "SELECT attempt_id, generation FROM outstanding_slot WHERE "
                "repository_id = 'repo-1'"
            ).fetchone()
        finally:
            connection.close()
        self.assertEqual(run, ("BLOCKED", "operation-recovery:attempt-1"))
        self.assertEqual(pause_fence, 0)
        self.assertEqual(slot, ("attempt-1", 1))
        self.store.load_verified("repo-1", authority=self.authority)
        pre_recovery_path = (
            self.database_path.parent / "pre-recovery.sqlite3"
        )
        shutil.copy2(self.database_path, pre_recovery_path)
        recovery_grant = SyntheticOperatorGrant(
            "recover-nonexecution-grant", "repo-1", "run-1",
            "RECOVER_OPERATION", "recover-nonexecution-scope",
        )
        self.authority.register_operator(recovery_grant)
        recovery_capability = self.authority.claim_operator(
            *recovery_grant.__dict__.values()
        )
        recovery_request = RecoverProvenNonexecutionRequest(
            "recover-nonexecution", "retry-authorization-1",
            "recover-nonexecution-command", "recover-nonexecution-event",
            "repo-1", "run-1", "item-1", "effect-1", "attempt-1",
            "attempt-2", "plan:run-1", "revision-1", "descriptor-digest",
            "contacted-nonexecution", settled.settlement_hash, resolved_ids,
            "operation-recovery:attempt-1", 1, 2,
            resume.event_hash, resume.event_hash,
        )
        with self.assertRaises(InjectedFailure):
            self.store.recover_proven_nonexecution(
                recovery_request, recovery_capability, self.authority,
                failure_hook=raise_at(
                    "after_operation_recovery_commit_before_acknowledgement"
                ),
            )
        recovered = self.store.recover_proven_nonexecution(
            recovery_request, recovery_capability, self.authority
        )
        self.assertTrue(recovered.replayed)
        self.oracle.allowed_head = recovered.event_hash
        self.assertEqual(recovered.resulting_state, LifecycleState.PLANNED)
        connection = sqlite3.connect(self.database_path)
        try:
            run = connection.execute(
                "SELECT lifecycle_state, continuation_cursor FROM runs WHERE "
                "run_id = 'run-1'"
            ).fetchone()
            authorization = connection.execute(
                "SELECT status, prior_attempt_id, successor_attempt_id, "
                "source_generation, target_generation FROM "
                "operation_retry_authorizations WHERE authorization_id = "
                "'retry-authorization-1'"
            ).fetchone()
            slot = connection.execute(
                "SELECT attempt_id, generation FROM outstanding_slot WHERE "
                "repository_id = 'repo-1'"
            ).fetchone()
        finally:
            connection.close()
        self.assertEqual(run, ("PLANNED", None))
        self.assertEqual(
            authorization, ("AVAILABLE", "attempt-1", "attempt-2", 1, 2)
        )
        self.assertEqual(slot, ("attempt-1", 1))
        self.store.load_verified("repo-1", authority=self.authority)
        available_recovery_path = (
            self.database_path.parent / "available-recovery.sqlite3"
        )
        shutil.copy2(self.database_path, available_recovery_path)

        retry_grant = SyntheticGrant(
            "grant-retry", "repo-1", "effect-1", "attempt-2", "scope-1"
        )
        self.authority.register(retry_grant)
        retry_capability = self.authority.claim(*retry_grant.__dict__.values())
        retry_request = ProvenNonexecutionIntentRequest(
            "repo-1", "run-1", "item-1", "command-2", "event-2",
            "effect-1", "descriptor-digest", "attempt-2",
            "permission-use-2", "reservation-2", "budget-policy-digest",
            3, 5, 10, "retry-authorization-1", "attempt-1", 1, 2,
        )
        connection = sqlite3.connect(self.database_path)
        try:
            writer_epoch = connection.execute(
                "SELECT MAX(writer_epoch) + 1 FROM events WHERE "
                "repository_id = 'repo-1'"
            ).fetchone()[0]
        finally:
            connection.close()
        with self.assertRaises(InjectedFailure):
            self.store.commit_intent(
                retry_request, retry_capability, self.authority,
                expected_head=recovered.event_hash, writer_epoch=writer_epoch,
                failure_hook=raise_at("after_intent_writes_before_commit"),
            )
        connection = sqlite3.connect(self.database_path)
        try:
            rolled_back = connection.execute(
                "SELECT status FROM operation_retry_authorizations WHERE "
                "authorization_id = 'retry-authorization-1'"
            ).fetchone()[0]
        finally:
            connection.close()
        self.assertEqual(rolled_back, "AVAILABLE")
        retried = self.store.commit_intent(
            retry_request, retry_capability, self.authority,
            expected_head=recovered.event_hash, writer_epoch=writer_epoch,
        )
        self.oracle.allowed_head = retried.event_hash
        retry_replay = self.store.commit_intent(
            retry_request, retry_capability, self.authority,
            expected_head=retried.event_hash, writer_epoch=writer_epoch + 1,
        )
        self.assertTrue(retry_replay.replayed)
        connection = sqlite3.connect(self.database_path)
        try:
            slot = connection.execute(
                "SELECT attempt_id, generation FROM outstanding_slot WHERE "
                "repository_id = 'repo-1'"
            ).fetchone()
            authorization = connection.execute(
                "SELECT status, consuming_event_id FROM "
                "operation_retry_authorizations WHERE authorization_id = "
                "'retry-authorization-1'"
            ).fetchone()
        finally:
            connection.close()
        self.assertEqual(slot, ("attempt-2", 2))
        self.assertEqual(authorization, ("CONSUMED", "event-2"))
        self.store.load_verified("repo-1", authority=self.authority)
        consumed_recovery_path = (
            self.database_path.parent / "consumed-recovery.sqlite3"
        )
        shutil.copy2(self.database_path, consumed_recovery_path)
        retry_launch = self.store.claim_operation_launch(
            retry_request, retried
        )
        self.oracle.allowed_head = retry_launch.event_hash
        self.store._contact_claimed_operation(
            retry_request, retry_capability, retried, retry_launch,
            self.store._adapter_target_digest("repo-1", "EFFECT"),
        )
        connection = sqlite3.connect(self.database_path)
        try:
            self.oracle.allowed_head = connection.execute(
                "SELECT catalog_head FROM repositories WHERE repository_id = "
                "'repo-1'"
            ).fetchone()[0]
            launch_body, contact_body = (
                json.loads(row[0]) for row in connection.execute(
                    "SELECT body_json FROM events WHERE event_id = ? OR "
                    "event_id = (SELECT event_id FROM adapter_contacts WHERE "
                    "source_id = ?) ORDER BY sequence",
                    (retry_launch.event_id, f"EFFECT:{retry_launch.launch_id}"),
                )
            )
        finally:
            connection.close()
        recovered_bodies = (launch_body, contact_body)
        self.assertEqual(
            {body["slot_generation"] for body in recovered_bodies}, {2}
        )
        self.assertEqual(
            {
                body["recovery_authorization_id"]
                for body in recovered_bodies
            },
            {"retry-authorization-1"},
        )
        self.store.load_verified("repo-1", authority=self.authority)

        retry_contact_path = (
            self.database_path.parent / "retry-contact.sqlite3"
        )
        shutil.copy2(self.database_path, retry_contact_path)

        terminal_oracle = MutableFreshnessOracle()
        terminal_oracle.allowed_head = self.oracle.allowed_head
        terminal_store = SQLiteStateStore(
            retry_contact_path, terminal_oracle, "repo-1",
            utc_now=lambda: datetime(2026, 9, 21, tzinfo=timezone.utc),
        )
        terminal_store._bind_classification_authority(self.authority)
        terminal_stop = terminal_store.stop(
            self._stop_request(suffix="retry-terminal"),
            self._stop_capability(
                StopMode.IMMEDIATE, suffix="retry-terminal"
            ),
            self.authority,
        )
        terminal_oracle.allowed_head = terminal_stop.event_hash
        connection = sqlite3.connect(retry_contact_path)
        try:
            retry_plan_hash = connection.execute(
                "SELECT event_hash FROM validation_plans WHERE plan_id = "
                "'plan:run-1'"
            ).fetchone()[0]
            retry_stop_accounting = connection.execute(
                "SELECT held_units, charged_units, uncertainty, disposition "
                "FROM budget_reservations WHERE reservation_id = "
                "'reservation-2'"
            ).fetchone()
        finally:
            connection.close()
        self.assertEqual(
            retry_stop_accounting,
            (
                0, 5, 1,
                BudgetDisposition.UNKNOWN_WORST_CASE_CHARGED.value,
            ),
        )
        terminal_request = TerminalValidationSettlementRequest(
            "terminal-settlement-retry", "terminal-command-retry",
            "terminal-event-retry", "repo-1", "run-1", "item-1",
            "effect-1", "plan:run-1", "revision-1", "check-1", "PLAN",
            "plan:run-1", retry_plan_hash, "CANCELLED_WITHOUT_START",
        )
        with self.assertRaises(InjectedFailure):
            terminal_store.settle_terminal_validation(
                terminal_request,
                failure_hook=raise_at(
                    "after_terminal_settlement_writes_before_commit"
                ),
            )
        self.assertEqual(
            terminal_store.table_counts()["terminal_validation_settlements"],
            0,
        )
        with self.assertRaises(InjectedFailure):
            terminal_store.settle_terminal_validation(
                terminal_request,
                failure_hook=raise_at(
                    "after_terminal_settlement_commit_before_acknowledgement"
                ),
            )
        connection = sqlite3.connect(retry_contact_path)
        try:
            terminal_hash = connection.execute(
                "SELECT event_hash FROM terminal_validation_settlements "
                "WHERE terminal_settlement_id = 'terminal-settlement-retry'"
            ).fetchone()[0]
            terminal_generation = json.loads(connection.execute(
                "SELECT body_json FROM terminal_validation_settlements "
                "WHERE terminal_settlement_id = 'terminal-settlement-retry'"
            ).fetchone()[0])["slot_generation"]
        finally:
            connection.close()
        terminal_oracle.allowed_head = terminal_hash
        reopened_terminal_store = SQLiteStateStore(
            retry_contact_path, terminal_oracle, "repo-1"
        )
        reopened_terminal_store._bind_classification_authority(self.authority)
        terminal_replay = reopened_terminal_store.settle_terminal_validation(
            terminal_request
        )
        self.assertTrue(terminal_replay.replayed)
        self.assertEqual(terminal_generation, 2)
        self.assertFalse(terminal_replay.slot_released)
        self.assertEqual(
            reopened_terminal_store.table_counts()["outstanding_slot"], 1
        )
        reopened_terminal_store.load_verified(
            "repo-1", authority=self.authority
        )

        retry_observation_request = EffectObservationRequest(
            "retry-observation", "retry-observe-command",
            "retry-observation-event", "repo-1", "run-1", "item-1",
            "effect-1", "attempt-2", "retry-receipt",
            retry_capability.claim_id, "descriptor-digest", 2,
            "retry-settlement", "",
        )
        with self.assertRaises(InjectedFailure):
            self._record_signed_effect_observation(
                retry_observation_request,
                failure_hook=raise_at(
                    "after_observation_settlement_before_observation"
                ),
            )
        self.assertEqual(
            self.store.table_counts()["effect_observations"], 0
        )
        with self.assertRaises(InjectedFailure):
            self._record_signed_effect_observation(
                retry_observation_request,
                failure_hook=raise_at(
                    "after_observation_commit_before_acknowledgement"
                ),
            )
        connection = sqlite3.connect(self.database_path)
        try:
            retry_observation_hash = connection.execute(
                "SELECT event_hash FROM effect_observations WHERE "
                "observation_id = 'retry-observation'"
            ).fetchone()[0]
        finally:
            connection.close()
        self.oracle.allowed_head = retry_observation_hash
        retry_observation = self._record_signed_effect_observation(
            retry_observation_request
        )
        self.assertTrue(retry_observation.replayed)
        self.assertEqual(
            retry_observation.resulting_state, LifecycleState.VALIDATING
        )
        self.store.load_verified("repo-1", authority=self.authority)

        retry_containment_json, retry_containment_digest = validator_containment(
            "input-1", "retry"
        )
        validator_grant = SyntheticValidatorGrant(
            "validator-grant-retry", "repo-1", "effect-1", "revision-1",
            "check-1", "input-1", "validator-attempt-retry",
            "read-only-scope-retry", retry_containment_digest,
        )
        self.authority.register_validator(validator_grant)
        validator_capability = self.authority.claim_validator(
            *validator_grant.__dict__.values()
        )
        validator_request = ValidatorIntentRequest(
            "validator-intent-retry", "validator-command-retry",
            "validator-event-retry", "repo-1", "run-1", "item-1",
            "effect-1", "attempt-2", "retry-observation",
            retry_observation.event_hash, "revision-1", "check-1",
            "input-1", "validator-attempt-retry",
            "validator-permission-retry", "validator-reservation-retry",
            "validator-budget-policy-1", 1, 2, 10, None,
            retry_containment_json,
        )
        with self.assertRaises(InjectedFailure):
            self.store.commit_validator_intent(
                validator_request, validator_capability, self.authority,
                failure_hook=raise_at(
                    "after_validator_intent_writes_before_commit"
                ),
            )
        with self.assertRaises(InjectedFailure):
            self.store.commit_validator_intent(
                validator_request, validator_capability, self.authority,
                failure_hook=raise_at(
                    "after_validator_intent_commit_before_acknowledgement"
                ),
            )
        connection = sqlite3.connect(self.database_path)
        try:
            validator_intent_hash = connection.execute(
                "SELECT event_hash FROM validator_intents WHERE "
                "validator_intent_id = 'validator-intent-retry'"
            ).fetchone()[0]
        finally:
            connection.close()
        self.oracle.allowed_head = validator_intent_hash
        validator_intent = self.store.commit_validator_intent(
            validator_request, validator_capability, self.authority
        )
        self.assertTrue(validator_intent.replayed)
        self.store.load_verified("repo-1", authority=self.authority)
        validator_target = self.store._adapter_target_digest(
            "repo-1", "VALIDATOR"
        )
        with self.assertRaises(InjectedFailure):
            self.store._contact_committed_validator(
                validator_request, validator_capability, validator_intent,
                validator_target, self.authority,
                failure_hook=raise_at(
                    "after_validator_contact_writes_before_commit"
                ),
            )
        with self.assertRaises(InjectedFailure):
            self.store._contact_committed_validator(
                validator_request, validator_capability, validator_intent,
                validator_target, self.authority,
                failure_hook=raise_at(
                    "after_validator_contact_commit_before_acknowledgement"
                ),
            )
        connection = sqlite3.connect(self.database_path)
        try:
            self.oracle.allowed_head = connection.execute(
                "SELECT catalog_head FROM repositories WHERE repository_id = "
                "'repo-1'"
            ).fetchone()[0]
        finally:
            connection.close()
        self.store._contact_committed_validator(
            validator_request, validator_capability, validator_intent,
            validator_target, self.authority,
        )
        self.store.load_verified("repo-1", authority=self.authority)

        for tampered_field, tampered_value in (
            ("slot_generation", 1),
            ("recovery_authorization_id", "forged-retry-authorization"),
        ):
            tamper_path = self.database_path.parent / (
                f"retry-validator-contact-{tampered_field}.sqlite3"
            )
            shutil.copy2(self.database_path, tamper_path)
            connection = sqlite3.connect(tamper_path)
            try:
                contact_event_id, contact_body_json = connection.execute(
                    "SELECT event_id, body_json FROM adapter_contacts WHERE "
                    "source_id = 'VALIDATOR:validator-intent-retry'"
                ).fetchone()
                contact_body = json.loads(contact_body_json)
                contact_body[tampered_field] = tampered_value
                forged_hash = self.store._event_hash(contact_body)
                forged_json = json.dumps(
                    contact_body, sort_keys=True, separators=(",", ":")
                )
                connection.execute(
                    "UPDATE events SET event_hash = ?, body_json = ? WHERE "
                    "event_id = ?",
                    (forged_hash, forged_json, contact_event_id),
                )
                connection.execute(
                    "UPDATE adapter_contacts SET event_hash = ?, "
                    "body_json = ? WHERE event_id = ?",
                    (forged_hash, forged_json, contact_event_id),
                )
                connection.execute(
                    "UPDATE runs SET head_hash = ? WHERE run_id = 'run-1'",
                    (forged_hash,),
                )
                connection.execute(
                    "UPDATE repositories SET catalog_head = ? WHERE "
                    "repository_id = 'repo-1'",
                    (forged_hash,),
                )
                connection.commit()
            finally:
                connection.close()
            tamper_oracle = MutableFreshnessOracle()
            tamper_oracle.allowed_head = forged_hash
            tampered_store = SQLiteStateStore(
                tamper_path, tamper_oracle, "repo-1"
            )
            tampered_store._bind_classification_authority(self.authority)
            with self.assertRaisesRegex(
                StorageIntegrityError, "recovered validator contact"
            ):
                tampered_store.load_verified(
                    "repo-1", authority=self.authority
                )

        validator_settlement_request = BudgetSettlementRequest(
            "validator-settlement-retry", "validator-reservation-retry", "",
            BudgetDisposition.CONSUMED, 1, "validator-result-retry",
            "VALIDATOR_USAGE_REPORTED",
        )
        validator_settlement = self.store._settle_budget(
            validator_settlement_request,
            self.authority.issue_settlement_proof(
                "validator-proof-retry", validator_settlement_request
            ),
            self.authority,
        )
        self.oracle.allowed_head = validator_settlement.settlement_hash
        self._record_validator_cessation_for(
            suffix="retry", result_available=True, check_id="check-1"
        )
        validator_observation = self.store._record_validator_observation(
            ValidatorObservationRequest(
                "validator-observation-retry",
                "validator-observe-command-retry",
                "validator-observation-event-retry", "repo-1", "run-1",
                "item-1", "effect-1", "validator-intent-retry",
                "validator-attempt-retry", "validator-result-retry",
                validator_capability.claim_id, "revision-1", "check-1",
                "input-1", "result-digest-retry", "PASS", 1,
                "validator-settlement-retry",
                validator_settlement.settlement_hash,
            )
        )
        self.oracle.allowed_head = validator_observation.event_hash
        application_request = ValidationApplicationRequest(
            "application-retry", "apply-command-retry", "apply-event-retry",
            "repo-1", "run-1", "item-1", "effect-1", "revision-1",
            "check-1", "validator-attempt-retry",
            "validator-observation-retry",
        )
        with self.assertRaises(InjectedFailure):
            self.store._apply_validator_observation(
                application_request,
                failure_hook=raise_at(
                    "after_validation_application_writes_before_commit"
                ),
            )
        with self.assertRaises(InjectedFailure):
            self.store._apply_validator_observation(
                application_request,
                failure_hook=raise_at(
                    "after_validation_application_commit_before_acknowledgement"
                ),
            )
        connection = sqlite3.connect(self.database_path)
        try:
            application_hash = connection.execute(
                "SELECT event_hash FROM validation_applications WHERE "
                "application_id = 'application-retry'"
            ).fetchone()[0]
        finally:
            connection.close()
        self.oracle.allowed_head = application_hash
        application = self.store._apply_validator_observation(
            application_request
        )
        self.assertTrue(application.replayed)
        self.assertEqual(application.resulting_state, LifecycleState.BLOCKED)
        self.store.load_verified("repo-1", authority=self.authority)

        finalization_request = FinalizeOperationRequest(
            "finalization-retry", "finalize-command-retry",
            "finalize-event-retry", "repo-1", "run-1", "item-1",
            "effect-1", "plan:run-1", "revision-1", "attempt-2", 2,
        )
        connection = sqlite3.connect(self.database_path)
        try:
            plan_event_hash, gate_set_digest = connection.execute(
                "SELECT event_hash, gate_set_digest FROM validation_plans "
                "WHERE plan_id = 'plan:run-1'"
            ).fetchone()
        finally:
            connection.close()
        finalization_key = self.store.finalization_key(
            "repo-1", "run-1", "item-1", "effect-1", "plan:run-1",
            "revision-1",
        )
        finalization_attestation = (
            self.authority.issue_finalization_attestation(
                "attestation-retry", "repo-1", "run-1", "item-1",
                "effect-1", "plan:run-1", plan_event_hash, "revision-1",
                application.event_hash, finalization_key, gate_set_digest,
                "attempt-2", 2,
            )
        )
        with self.assertRaises(InjectedFailure):
            self.store._finalize_operation(
                finalization_request, finalization_attestation,
                self.authority,
                failure_hook=raise_at("after_finalization_writes_before_commit"),
            )
        with self.assertRaises(InjectedFailure):
            self.store._finalize_operation(
                finalization_request, finalization_attestation,
                self.authority,
                failure_hook=raise_at(
                    "after_finalization_commit_before_acknowledgement"
                ),
            )
        connection = sqlite3.connect(self.database_path)
        try:
            finalization_hash = connection.execute(
                "SELECT event_hash FROM operation_finalizations WHERE "
                "finalization_id = 'finalization-retry'"
            ).fetchone()[0]
        finally:
            connection.close()
        self.oracle.allowed_head = finalization_hash
        finalization = self.store._finalize_operation(
            finalization_request, finalization_attestation, self.authority
        )
        self.assertTrue(finalization.replayed)
        self.assertEqual(finalization.resulting_state, LifecycleState.COMPLETED)
        self.assertEqual(self.store.table_counts()["outstanding_slot"], 0)
        self.store.load_verified("repo-1", authority=self.authority)

        def record_original_receipt(suffix: str):
            receipt = self._record_signed_effect_observation(
                EffectObservationRequest(
                    f"late-original-{suffix}",
                    f"late-original-command-{suffix}",
                    f"late-original-event-{suffix}",
                    "repo-1", "run-1", "item-1", "effect-1", "attempt-1",
                    f"late-original-receipt-{suffix}",
                    self.capability.claim_id, "descriptor-digest", 0,
                    f"late-original-settlement-{suffix}", "",
                )
            )
            self.oracle.allowed_head = receipt.event_hash
            return receipt

        shutil.copy2(consumed_recovery_path, self.database_path)
        self.oracle.allowed_head = retried.event_hash
        consumed_receipt = record_original_receipt("consumed")
        connection = sqlite3.connect(self.database_path)
        try:
            invalidation = connection.execute(
                "SELECT status, consuming_event_id, disabling_event_id FROM "
                "operation_retry_authorizations WHERE authorization_id = "
                "'retry-authorization-1'"
            ).fetchone()
            initiation_fence = connection.execute(
                "SELECT reason_code, originating_event_id FROM "
                "dispatch_fences WHERE fence_id = "
                "'retry-initiation-disabled:retry-authorization-1'"
            ).fetchone()
        finally:
            connection.close()
        self.assertEqual(
            invalidation,
            ("DISABLED", "event-2", consumed_receipt.event_id),
        )
        self.assertEqual(
            initiation_fence,
            ("RECOVERY_INITIATION_DISABLED", consumed_receipt.event_id),
        )
        self.store.load_verified("repo-1", authority=self.authority)
        with self.assertRaises(DispatchDenied):
            self.store.claim_operation_launch(retry_request, retried)

        shutil.copy2(available_recovery_path, self.database_path)
        self.oracle.allowed_head = recovered.event_hash
        available_receipt = record_original_receipt("available")
        connection = sqlite3.connect(self.database_path)
        try:
            invalidation = connection.execute(
                "SELECT status, consuming_event_id, disabling_event_id FROM "
                "operation_retry_authorizations WHERE authorization_id = "
                "'retry-authorization-1'"
            ).fetchone()
            initiation_fences = connection.execute(
                "SELECT COUNT(*) FROM dispatch_fences WHERE reason_code = "
                "'RECOVERY_INITIATION_DISABLED'"
            ).fetchone()[0]
        finally:
            connection.close()
        self.assertEqual(
            invalidation, ("DISABLED", None, available_receipt.event_id)
        )
        self.assertEqual(initiation_fences, 0)
        self.store.load_verified("repo-1", authority=self.authority)

        shutil.copy2(pre_recovery_path, self.database_path)
        self.oracle.allowed_head = resume.event_hash
        pre_recovery_receipt = record_original_receipt("pre-recovery")
        denied_grant = SyntheticOperatorGrant(
            "recover-after-receipt-grant", "repo-1", "run-1",
            "RECOVER_OPERATION", "recover-after-receipt-scope",
        )
        self.authority.register_operator(denied_grant)
        denied_capability = self.authority.claim_operator(
            *denied_grant.__dict__.values()
        )
        denied_request = replace(
            recovery_request,
            recovery_id="recover-after-receipt",
            authorization_id="retry-after-receipt",
            command_id="recover-after-receipt-command",
            event_id="recover-after-receipt-event",
            expected_catalog_head=pre_recovery_receipt.event_hash,
            expected_run_head=pre_recovery_receipt.event_hash,
        )
        with self.assertRaises(DispatchDenied):
            self.store.recover_proven_nonexecution(
                denied_request, denied_capability, self.authority
            )
        self.assertEqual(
            self.store.table_counts()["operation_recovery_actions"], 0
        )
        self.store.load_verified("repo-1", authority=self.authority)

    def test_t06_rejects_wrong_contact_chain_and_slot_without_mutation(self) -> None:
        _, _, _, request = self._contacted_operation("bindings")
        capability = self._pause_capability("external-bindings")
        variants = (
            replace(request, item_id="other-item"),
            replace(request, logical_effect_id="other-effect"),
            replace(request, attempt_id="other-attempt"),
            replace(request, intent_event_hash="other-intent-hash"),
            replace(request, launch_id="other-launch"),
            replace(request, launch_event_hash="other-launch-hash"),
            replace(request, contact_id="other-contact"),
            replace(request, contact_event_hash="other-contact-hash"),
            replace(request, target_digest="other-target"),
            replace(request, expected_slot_generation=2),
        )
        for variant in variants:
            with self.subTest(variant=variant), self.assertRaises(DispatchDenied):
                self.store.pause_external_mutation(
                    variant, capability, self.authority
                )
        connection = sqlite3.connect(self.database_path)
        try:
            state = connection.execute(
                "SELECT lifecycle_state FROM runs WHERE run_id = 'run-1'"
            ).fetchone()[0]
        finally:
            connection.close()
        self.assertEqual(state, "RUNNING")
        self.assertEqual(self.store.table_counts()["external_pause_actions"], 0)
        self.assertEqual(self.store.table_counts()["budget_settlements"], 0)

    def test_t06_requires_contact_and_denies_already_recorded_receipt(self) -> None:
        committed = self._running_operation()
        launched = self.store.claim_operation_launch(self.request(), committed)
        self.oracle.allowed_head = launched.event_hash
        fabricated = PauseExternalMutationRequest(
            "external-pause-precontact", "external-command-precontact",
            "external-event-precontact", "external-fence-precontact",
            "repo-1", "run-1", "item-1", "effect-1", "attempt-1",
            committed.event_id, committed.event_hash, launched.launch_id,
            launched.event_id, launched.event_hash, "missing-contact",
            "missing-contact-event", "missing-contact-hash",
            self.store._adapter_target_digest("repo-1", "EFFECT"), 1,
            "OPERATOR_PAUSE_EXTERNAL_MUTATION",
        )
        with self.assertRaisesRegex(DispatchDenied, "adapter contact"):
            self.store.pause_external_mutation(
                fabricated, self._pause_capability("external-precontact"),
                self.authority,
            )

    def test_t06_exact_replay_conflict_and_crash_boundaries(self) -> None:
        _, _, _, request = self._contacted_operation("crash")
        capability = self._pause_capability("external-crash")
        with self.assertRaises(InjectedFailure):
            self.store.pause_external_mutation(
                request, capability, self.authority,
                failure_hook=raise_at(
                    "after_external_pause_settlement_before_pause"
                ),
            )
        self.assertEqual(self.store.table_counts()["budget_settlements"], 0)
        self.assertEqual(self.store.table_counts()["external_pause_actions"], 0)
        with self.assertRaises(InjectedFailure):
            self.store.pause_external_mutation(
                request, capability, self.authority,
                failure_hook=raise_at(
                    "after_external_pause_commit_before_acknowledgement"
                ),
            )
        connection = sqlite3.connect(self.database_path)
        try:
            self.oracle.allowed_head = connection.execute(
                "SELECT catalog_head FROM repositories WHERE repository_id = "
                "'repo-1'"
            ).fetchone()[0]
        finally:
            connection.close()
        replay = self.store.pause_external_mutation(
            request, capability, self.authority
        )
        self.assertTrue(replay.replayed)
        self.assertEqual(replay.event_hash, self.oracle.allowed_head)
        with self.assertRaisesRegex(StorageIntegrityError, "different payload"):
            self.store.pause_external_mutation(
                replace(request, reason_code="DIFFERENT"),
                capability, self.authority,
            )
        self.assertEqual(self.store.table_counts()["budget_settlements"], 1)
        self.assertEqual(self.store.table_counts()["external_pause_actions"], 1)
        self.assertEqual(self.store.table_counts()["outstanding_slot"], 1)

    def test_t06_retains_existing_unknown_settlement_without_double_charge(
        self,
    ) -> None:
        _, _, _, request = self._contacted_operation("existing-unknown")
        settlement = BudgetSettlementRequest(
            "existing-unknown-settlement", "reservation-1", "",
            BudgetDisposition.UNKNOWN_WORST_CASE_CHARGED, None,
            "existing-missing-telemetry", "USAGE_UNKNOWN",
        )
        settled = self.store._settle_budget(
            settlement,
            self.authority.issue_settlement_proof(
                "existing-unknown-proof", settlement
            ),
            self.authority,
        )
        self.oracle.allowed_head = settled.settlement_hash
        paused = self.store.pause_external_mutation(
            request, self._pause_capability("external-existing-unknown"),
            self.authority,
        )
        self.assertEqual(
            paused.resulting_state, LifecycleState.RECONCILIATION_REQUIRED
        )
        self.assertEqual(self.store.table_counts()["budget_settlements"], 1)
        connection = sqlite3.connect(self.database_path)
        try:
            row = connection.execute(
                "SELECT settlement_event_id, settlement_hash FROM "
                "external_pause_actions"
            ).fetchone()
        finally:
            connection.close()
        self.assertEqual(
            row, ("existing-unknown-settlement", settled.settlement_hash)
        )

    def test_t06_known_accounting_does_not_create_billing_uncertainty(
        self,
    ) -> None:
        _, _, _, request = self._contacted_operation("existing-known")
        settlement = BudgetSettlementRequest(
            "existing-known-settlement", "reservation-1", "",
            BudgetDisposition.CONSUMED, 2,
            "existing-known-usage", "USAGE_REPORTED",
        )
        settled = self.store._settle_budget(
            settlement,
            self.authority.issue_settlement_proof(
                "existing-known-proof", settlement
            ),
            self.authority,
        )
        self.oracle.allowed_head = settled.settlement_hash
        self.store.pause_external_mutation(
            request, self._pause_capability("external-existing-known"),
            self.authority,
        )
        connection = sqlite3.connect(self.database_path)
        try:
            accounting = connection.execute(
                "SELECT disposition, charged_units, uncertainty FROM "
                "budget_reservations WHERE reservation_id = 'reservation-1'"
            ).fetchone()
            kinds = connection.execute(
                "SELECT uncertainty_kind FROM uncertainty_instances WHERE "
                "origin_event_id = ? ORDER BY uncertainty_kind",
                (request.event_id,),
            ).fetchall()
        finally:
            connection.close()
        self.assertEqual(accounting, ("CONSUMED", 2, 0))
        self.assertEqual(
            kinds, [("ACTIVITY",), ("OUTCOME",), ("SOURCE_CONTROL",)]
        )

    def test_t06_unknown_late_receipt_retains_worst_case_and_fence(self) -> None:
        _, _, _, request = self._contacted_operation("unknown-late")
        paused = self.store.pause_external_mutation(
            request, self._pause_capability("external-unknown-late"),
            self.authority,
        )
        self.oracle.allowed_head = paused.event_hash
        observed = self._record_signed_effect_observation(
            EffectObservationRequest(
                "unknown-late-observation", "unknown-late-command",
                "unknown-late-event", "repo-1", "run-1", "item-1",
                "effect-1", "attempt-1", "unknown-late-receipt",
                self.capability.claim_id, self.request().effect_descriptor_digest,
                None, "unknown-late-settlement", "",
            )
        )
        self.assertEqual(
            observed.resulting_state, LifecycleState.RECONCILIATION_REQUIRED
        )
        connection = sqlite3.connect(self.database_path)
        try:
            accounting = connection.execute(
                "SELECT disposition, charged_units, uncertainty FROM "
                "budget_reservations WHERE reservation_id = 'reservation-1'"
            ).fetchone()
            retained = connection.execute(
                "SELECT (SELECT COUNT(*) FROM outstanding_slot), "
                "(SELECT COUNT(*) FROM dispatch_fences WHERE fence_id = "
                "'external-pause-fence-unknown-late')"
            ).fetchone()
        finally:
            connection.close()
        self.assertEqual(accounting, ("UNKNOWN_WORST_CASE_CHARGED", 5, 1))
        self.assertEqual(retained, (1, 1))

    def test_t17_missing_usage_preserves_known_accounting_without_billing(
        self,
    ) -> None:
        self._contacted_operation("known-accounting-observation")
        settlement = BudgetSettlementRequest(
            "known-observation-settlement", "reservation-1", "",
            BudgetDisposition.CONSUMED, 2,
            "known-observation-receipt", "USAGE_REPORTED",
        )
        settled = self.store._settle_budget(
            settlement,
            self.authority.issue_settlement_proof(
                "known-observation-proof", settlement
            ),
            self.authority,
        )
        self.oracle.allowed_head = settled.settlement_hash
        observed = self._record_signed_effect_observation(
            EffectObservationRequest(
                "known-observation", "known-observation-command",
                "known-observation-event", "repo-1", "run-1", "item-1",
                "effect-1", "attempt-1", "known-observation-receipt",
                self.capability.claim_id,
                self.request().effect_descriptor_digest, None,
                "known-observation-settlement", settled.settlement_hash,
            )
        )
        self.assertEqual(observed.resulting_state, LifecycleState.VALIDATING)
        connection = sqlite3.connect(self.database_path)
        try:
            accounting = connection.execute(
                "SELECT disposition, charged_units, uncertainty FROM "
                "budget_reservations WHERE reservation_id = 'reservation-1'"
            ).fetchone()
            uncertainty_count = connection.execute(
                "SELECT COUNT(*) FROM uncertainty_instances WHERE "
                "origin_event_id = 'known-observation-event'"
            ).fetchone()[0]
        finally:
            connection.close()
        self.assertEqual(accounting, ("CONSUMED", 2, 0))
        self.assertEqual(uncertainty_count, 0)

    def test_t06_recovery_rejects_external_pause_projection_loss(self) -> None:
        _, _, _, request = self._contacted_operation("projection-tamper")
        paused = self.store.pause_external_mutation(
            request, self._pause_capability("external-projection-tamper"),
            self.authority,
        )
        connection = sqlite3.connect(self.database_path)
        try:
            connection.execute("DELETE FROM external_pause_actions")
            connection.commit()
        finally:
            connection.close()
        self.oracle.allowed_head = paused.event_hash
        with self.assertRaisesRegex(StorageIntegrityError, "external-pause"):
            self.store.load_verified("repo-1", authority=self.authority)

    def test_t06_recovery_rejects_surplus_event_schema(self) -> None:
        _, _, _, request = self._contacted_operation("schema-tamper")
        paused = self.store.pause_external_mutation(
            request, self._pause_capability("external-schema-tamper"),
            self.authority,
        )
        connection = sqlite3.connect(self.database_path)
        connection.row_factory = sqlite3.Row
        try:
            row = connection.execute(
                "SELECT * FROM external_pause_actions"
            ).fetchone()
            body = json.loads(row["body_json"])
            body["surplus"] = "forbidden"
            event_hash = self.store._event_hash(body)
            body_json = json.dumps(body, sort_keys=True, separators=(",", ":"))
            connection.execute(
                "UPDATE events SET event_hash = ?, body_json = ? WHERE event_id = ?",
                (event_hash, body_json, body["event_id"]),
            )
            connection.execute(
                "UPDATE external_pause_actions SET event_hash = ?, body_json = ?",
                (event_hash, body_json),
            )
            connection.execute(
                "UPDATE command_outcomes SET event_hash = ? WHERE command_id = ?",
                (event_hash, body["command_id"]),
            )
            connection.execute(
                "UPDATE runs SET head_hash = ? WHERE run_id = 'run-1'",
                (event_hash,),
            )
            connection.execute(
                "UPDATE repositories SET catalog_head = ? WHERE repository_id = "
                "'repo-1'",
                (event_hash,),
            )
            connection.commit()
        finally:
            connection.close()
        self.oracle.allowed_head = event_hash
        with self.assertRaisesRegex(
            StorageIntegrityError, "external PAUSE_REQUESTED"
        ):
            self.store.load_verified("repo-1", authority=self.authority)

    def test_t06_recovery_rejects_self_consistent_contact_snapshot_rewrite(
        self,
    ) -> None:
        _, _, _, request = self._contacted_operation("snapshot-tamper")
        paused = self.store.pause_external_mutation(
            request, self._pause_capability("external-snapshot-tamper"),
            self.authority,
        )
        connection = sqlite3.connect(self.database_path)
        connection.row_factory = sqlite3.Row
        try:
            row = connection.execute(
                "SELECT * FROM external_pause_actions"
            ).fetchone()
            body = json.loads(row["body_json"])
            body["uncertainty_snapshot"]["contact_event_hash"] = "forged-contact"
            event_hash = self.store._event_hash(body)
            body_json = json.dumps(body, sort_keys=True, separators=(",", ":"))
            connection.execute(
                "UPDATE events SET event_hash = ?, body_json = ? WHERE event_id = ?",
                (event_hash, body_json, body["event_id"]),
            )
            connection.execute(
                "UPDATE external_pause_actions SET event_hash = ?, body_json = ?",
                (event_hash, body_json),
            )
            connection.execute(
                "UPDATE command_outcomes SET event_hash = ? WHERE command_id = ?",
                (event_hash, body["command_id"]),
            )
            connection.execute(
                "UPDATE runs SET head_hash = ? WHERE run_id = 'run-1'",
                (event_hash,),
            )
            connection.execute(
                "UPDATE repositories SET catalog_head = ? WHERE repository_id = "
                "'repo-1'",
                (event_hash,),
            )
            connection.commit()
        finally:
            connection.close()
        self.oracle.allowed_head = event_hash
        with self.assertRaisesRegex(StorageIntegrityError, "external pause proof"):
            self.store.load_verified("repo-1", authority=self.authority)

    def test_t06_recovery_rejects_retained_settlement_head_retarget(self) -> None:
        _, _, _, request = self._contacted_operation("head-retarget")
        unknown_request = BudgetSettlementRequest(
            "head-retarget-unknown", "reservation-1", "",
            BudgetDisposition.UNKNOWN_WORST_CASE_CHARGED, None,
            "head-retarget-missing", "USAGE_UNKNOWN",
        )
        unknown = self.store._settle_budget(
            unknown_request,
            self.authority.issue_settlement_proof(
                "head-retarget-unknown-proof", unknown_request
            ),
            self.authority,
        )
        self.oracle.allowed_head = unknown.settlement_hash
        adjusted_request = BudgetSettlementRequest(
            "head-retarget-adjusted", "reservation-1",
            unknown.settlement_hash, BudgetDisposition.ADJUSTED, 2,
            "head-retarget-known", "USAGE_REPORTED",
        )
        adjusted = self.store._settle_budget(
            adjusted_request,
            self.authority.issue_settlement_proof(
                "head-retarget-adjusted-proof", adjusted_request
            ),
            self.authority,
        )
        self.oracle.allowed_head = adjusted.settlement_hash
        paused = self.store.pause_external_mutation(
            request, self._pause_capability("external-head-retarget"),
            self.authority,
        )
        connection = sqlite3.connect(self.database_path)
        connection.row_factory = sqlite3.Row
        try:
            row = connection.execute(
                "SELECT * FROM external_pause_actions"
            ).fetchone()
            body = json.loads(row["body_json"])
            body["uncertainty_snapshot"].update(
                {
                    "historical_disposition": (
                        BudgetDisposition.UNKNOWN_WORST_CASE_CHARGED.value
                    ),
                    "resulting_disposition": (
                        BudgetDisposition.UNKNOWN_WORST_CASE_CHARGED.value
                    ),
                    "settlement_event_id": unknown.settlement_event_id,
                    "settlement_hash": unknown.settlement_hash,
                }
            )
            event_hash = self.store._event_hash(body)
            body_json = json.dumps(body, sort_keys=True, separators=(",", ":"))
            connection.execute(
                "UPDATE events SET event_hash = ?, body_json = ? WHERE event_id = ?",
                (event_hash, body_json, body["event_id"]),
            )
            connection.execute(
                "UPDATE external_pause_actions SET settlement_event_id = ?, "
                "settlement_hash = ?, event_hash = ?, body_json = ?",
                (
                    unknown.settlement_event_id, unknown.settlement_hash,
                    event_hash, body_json,
                ),
            )
            connection.execute(
                "UPDATE command_outcomes SET event_hash = ? WHERE command_id = ?",
                (event_hash, body["command_id"]),
            )
            connection.execute(
                "UPDATE runs SET head_hash = ? WHERE run_id = 'run-1'",
                (event_hash,),
            )
            connection.execute(
                "UPDATE repositories SET catalog_head = ? WHERE repository_id = "
                "'repo-1'",
                (event_hash,),
            )
            connection.commit()
        finally:
            connection.close()
        self.oracle.allowed_head = event_hash
        with self.assertRaisesRegex(StorageIntegrityError, "external pause proof"):
            self.store.load_verified("repo-1", authority=self.authority)

    def test_t06_recovery_rejects_self_consistent_contact_effect_retarget(
        self,
    ) -> None:
        _, _, _, request = self._contacted_operation("contact-retarget")
        paused = self.store.pause_external_mutation(
            request, self._pause_capability("external-contact-retarget"),
            self.authority,
        )
        connection = sqlite3.connect(self.database_path)
        connection.row_factory = sqlite3.Row
        try:
            contact = connection.execute(
                "SELECT * FROM adapter_contacts"
            ).fetchone()
            pause = connection.execute(
                "SELECT * FROM external_pause_actions"
            ).fetchone()
            settlement = connection.execute(
                "SELECT * FROM budget_settlements WHERE settlement_event_id = ?",
                (pause["settlement_event_id"],),
            ).fetchone()

            contact_body = json.loads(contact["body_json"])
            contact_body["logical_effect_id"] = "forged-effect"
            contact_hash = self.store._event_hash(contact_body)
            contact_json = json.dumps(
                contact_body, sort_keys=True, separators=(",", ":")
            )
            connection.execute(
                "UPDATE events SET event_hash = ?, body_json = ? WHERE event_id = ?",
                (contact_hash, contact_json, contact["event_id"]),
            )
            connection.execute(
                "UPDATE adapter_contacts SET event_hash = ?, body_json = ? "
                "WHERE contact_id = ?",
                (contact_hash, contact_json, contact["contact_id"]),
            )

            pause_body = json.loads(pause["body_json"])
            settlement_body = json.loads(settlement["body_json"])
            settlement_binding = {
                "pause_id": pause_body["pause_id"],
                "pause_event_id": pause_body["event_id"],
                "reservation_id": settlement["reservation_id"],
                "expected_previous_hash": settlement["previous_hash"],
                "intent_event_hash": pause_body["intent_event_hash"],
                "launch_event_hash": pause_body["launch_event_hash"],
                "contact_event_hash": contact_hash,
            }
            evidence_digest = self.store._event_hash(settlement_binding)
            settlement_event_id = "external-pause-unknown:" + evidence_digest
            settlement_body.update(
                {
                    "settlement_event_id": settlement_event_id,
                    "evidence_digest": evidence_digest,
                    "event_id": settlement_event_id,
                    "command_id": f"settlement:{settlement_event_id}",
                    "previous_event_hash": contact_hash,
                }
            )
            payload_keys = {
                "actual_units", "additional_liability",
                "all_obligations_settled", "disposition", "evidence_digest",
                "expected_previous_hash", "non_dispatch_proven",
                "reason_code", "release_slot", "reservation_id",
                "settlement_event_id", "zero_liability_proven",
                "repository_id", "run_id", "item_id", "logical_effect_id",
                "attempt_id", "settlement_binding_version",
            }
            settlement_payload_digest = self.store._event_hash(
                {key: settlement_body[key] for key in payload_keys}
            )
            settlement_hash = self.store._event_hash(settlement_body)
            settlement_json = json.dumps(
                settlement_body, sort_keys=True, separators=(",", ":")
            )
            connection.execute(
                "UPDATE events SET event_id = ?, command_id = ?, "
                "previous_event_hash = ?, event_hash = ?, body_json = ? "
                "WHERE event_id = ?",
                (
                    settlement_event_id, settlement_body["command_id"],
                    contact_hash, settlement_hash, settlement_json,
                    settlement["settlement_event_id"],
                ),
            )
            connection.execute(
                "UPDATE budget_settlements SET settlement_event_id = ?, "
                "settlement_hash = ?, evidence_digest = ?, payload_digest = ?, "
                "body_json = ? WHERE settlement_event_id = ?",
                (
                    settlement_event_id, settlement_hash, evidence_digest,
                    settlement_payload_digest, settlement_json,
                    settlement["settlement_event_id"],
                ),
            )
            connection.execute(
                "UPDATE budget_reservations SET settlement_head_hash = ? "
                "WHERE reservation_id = ?",
                (settlement_hash, settlement["reservation_id"]),
            )

            pause_body["contact_event_hash"] = contact_hash
            pause_body["previous_event_hash"] = settlement_hash
            pause_body["uncertainty_snapshot"].update(
                {
                    "contact_event_hash": contact_hash,
                    "settlement_event_id": settlement_event_id,
                    "settlement_hash": settlement_hash,
                }
            )
            pause_payload = {
                **{
                    key: pause_body[key]
                    for key in PauseExternalMutationRequest.__dataclass_fields__
                },
                "pause_kind": pause_body["pause_kind"],
                "pause_binding_version": pause_body["pause_binding_version"],
                "capability_evidence": pause_body["capability_evidence"],
                "capability_issuer_fingerprint": pause_body[
                    "capability_issuer_fingerprint"
                ],
            }
            pause_body["payload_digest"] = self.store._event_hash(pause_payload)
            pause_hash = self.store._event_hash(pause_body)
            pause_json = json.dumps(
                pause_body, sort_keys=True, separators=(",", ":")
            )
            connection.execute(
                "UPDATE events SET previous_event_hash = ?, event_hash = ?, "
                "body_json = ? WHERE event_id = ?",
                (
                    settlement_hash, pause_hash, pause_json,
                    pause_body["event_id"],
                ),
            )
            connection.execute(
                "UPDATE external_pause_actions SET contact_event_hash = ?, "
                "settlement_event_id = ?, settlement_hash = ?, "
                "payload_digest = ?, event_hash = ?, body_json = ?",
                (
                    contact_hash, settlement_event_id, settlement_hash,
                    pause_body["payload_digest"], pause_hash, pause_json,
                ),
            )
            connection.execute(
                "UPDATE command_outcomes SET payload_digest = ?, event_hash = ? "
                "WHERE command_id = ?",
                (
                    pause_body["payload_digest"], pause_hash,
                    pause_body["command_id"],
                ),
            )
            connection.execute(
                "UPDATE runs SET head_hash = ? WHERE run_id = 'run-1'",
                (pause_hash,),
            )
            connection.execute(
                "UPDATE repositories SET catalog_head = ? WHERE repository_id = "
                "'repo-1'",
                (pause_hash,),
            )
            connection.commit()
        finally:
            connection.close()
        self.oracle.allowed_head = pause_hash
        with self.assertRaisesRegex(StorageIntegrityError, "external pause proof"):
            self.store.load_verified("repo-1", authority=self.authority)

    def test_t05_pauses_launched_uncontacted_attempt(self) -> None:
        committed = self._running_operation()
        launched = self.store.claim_operation_launch(self.request(), committed)
        self.oracle.allowed_head = launched.event_hash
        receipt = self.store.pause_local_execution(
            self._local_pause_request(committed, suffix="launched"),
            self._pause_capability("launched"), self.authority,
        )
        self.assertEqual(receipt.resulting_state, LifecycleState.PAUSING)
        self.oracle.allowed_head = receipt.event_hash
        self.store.load_verified("repo-1", authority=self.authority)

    def test_t05_pause_fence_denies_later_adapter_contact(self) -> None:
        committed = self._running_operation()
        launched = self.store.claim_operation_launch(self.request(), committed)
        self.oracle.allowed_head = launched.event_hash
        paused = self.store.pause_local_execution(
            self._local_pause_request(committed, suffix="race"),
            self._pause_capability("race"), self.authority,
        )
        self.oracle.allowed_head = paused.event_hash
        with self.assertRaisesRegex(DispatchDenied, "RUNNING|dispatch fence"):
            self.store._contact_claimed_operation(
                self.request(), self.capability, committed, launched,
                "synthetic-target-digest",
            )

    def test_t05_rejects_non_owned_attempt_bindings_without_mutation(self) -> None:
        committed = self._running_operation()
        capability = self._pause_capability("bindings")
        base = self._local_pause_request(committed, suffix="bindings")
        variants = (
            replace(base, repository_id="other-repo"),
            replace(base, run_id="other-run"),
            replace(base, item_id="other-item"),
            replace(base, logical_effect_id="other-effect"),
            replace(base, attempt_id="other-attempt"),
            replace(base, intent_event_id="other-event"),
            replace(base, intent_event_hash="other-hash"),
            replace(base, expected_slot_generation=2),
        )
        for request in variants:
            with self.subTest(request=request):
                with self.assertRaises(DispatchDenied):
                    self.store.pause_local_execution(
                        request, capability, self.authority
                    )
        connection = sqlite3.connect(self.database_path)
        try:
            self.assertEqual(
                connection.execute(
                    "SELECT lifecycle_state FROM runs WHERE run_id = 'run-1'"
                ).fetchone()[0],
                "RUNNING",
            )
            self.assertEqual(
                connection.execute(
                    "SELECT COUNT(*) FROM local_pause_actions"
                ).fetchone()[0],
                0,
            )
            self.assertEqual(
                connection.execute(
                    "SELECT COUNT(*) FROM dispatch_fences"
                ).fetchone()[0],
                0,
            )
        finally:
            connection.close()

    def test_t05_rejects_nonrunning_state_and_redeemed_operator(self) -> None:
        plan = self.store.accept_plan(
            PlanAcceptanceRequest(
                "plan-1", "plan-command-1", "plan-event-1", "repo-1",
                "run-1", "item-1", "effect-1", "revision-1",
                "descriptor-digest", "scope-1", "budget-policy-digest",
                ("check-1",),
            ),
            expected_head="", writer_epoch=1,
        )
        self.oracle.allowed_head = plan.event_hash
        planned_capability = self._pause_capability("planned")
        with self.assertRaisesRegex(DispatchDenied, "RUNNING"):
            self.store.pause_local_execution(
                PauseLocalExecutionRequest(
                    "local-pause-planned", "local-pause-command-planned",
                    "local-pause-event-planned", "local-pause-fence-planned",
                    "repo-1", "run-1", "item-1", "effect-1", "attempt-1",
                    "event-1", "intent-hash", 1, "OPERATOR_PAUSE",
                ),
                planned_capability, self.authority,
            )
        committed = self.store.commit_intent(
            self.request(), self.capability, self.authority,
            expected_head=plan.event_hash, writer_epoch=2,
        )
        self.oracle.allowed_head = committed.event_hash
        redeemed = self._pause_capability("redeemed")
        self.authority.mark_operator_action_committed(redeemed)
        with self.assertRaisesRegex(DispatchDenied, "already committed"):
            self.store.pause_local_execution(
                self._local_pause_request(committed, suffix="redeemed"),
                redeemed, self.authority,
            )

    def test_t05_rejects_contacted_attempt_for_t06_route(self) -> None:
        committed = self._running_operation()
        launched = self.store.claim_operation_launch(self.request(), committed)
        self.oracle.allowed_head = launched.event_hash
        self.store._contact_claimed_operation(
            self.request(), self.capability, committed, launched,
            self.store._adapter_target_digest("repo-1", "EFFECT"),
        )
        connection = sqlite3.connect(self.database_path)
        try:
            self.oracle.allowed_head = connection.execute(
                "SELECT catalog_head FROM repositories WHERE repository_id = 'repo-1'"
            ).fetchone()[0]
        finally:
            connection.close()
        with self.assertRaisesRegex(DispatchDenied, "T06"):
            self.store.pause_local_execution(
                self._local_pause_request(committed, suffix="contacted"),
                self._pause_capability("contacted"), self.authority,
            )

    def test_t05_local_pause_replays_exactly_and_rejects_conflict(self) -> None:
        committed = self._running_operation()
        request = self._local_pause_request(committed, suffix="replay")
        capability = self._pause_capability("replay")
        original = self.store.pause_local_execution(
            request, capability, self.authority
        )
        self.oracle.allowed_head = original.event_hash
        replay = self.store.pause_local_execution(
            request, capability, self.authority
        )
        self.assertTrue(replay.replayed)
        self.assertEqual(replay.event_hash, original.event_hash)
        with self.assertRaisesRegex(StorageIntegrityError, "different payload"):
            self.store.pause_local_execution(
                replace(request, reason_code="DIFFERENT_REASON"),
                capability, self.authority,
            )

    def test_t05_local_pause_precommit_rolls_back_and_postcommit_replays(self) -> None:
        committed = self._running_operation()
        request = self._local_pause_request(committed, suffix="crash")
        capability = self._pause_capability("crash")
        with self.assertRaises(InjectedFailure):
            self.store.pause_local_execution(
                request, capability, self.authority,
                failure_hook=raise_at("after_local_pause_writes_before_commit"),
            )
        self.assertEqual(self.store.table_counts()["local_pause_actions"], 0)
        self.assertEqual(self.store.table_counts()["dispatch_fences"], 0)
        with self.assertRaises(InjectedFailure):
            self.store.pause_local_execution(
                request, capability, self.authority,
                failure_hook=raise_at(
                    "after_local_pause_commit_before_acknowledgement"
                ),
            )
        connection = sqlite3.connect(self.database_path)
        try:
            committed_head = connection.execute(
                "SELECT catalog_head FROM repositories WHERE repository_id = 'repo-1'"
            ).fetchone()[0]
        finally:
            connection.close()
        self.oracle.allowed_head = committed_head
        replay = self.store.pause_local_execution(
            request, capability, self.authority
        )
        self.assertTrue(replay.replayed)
        self.assertEqual(replay.event_hash, committed_head)
        self.assertEqual(self.store.table_counts()["local_pause_actions"], 1)
        self.assertEqual(self.store.table_counts()["dispatch_fences"], 1)
        self.assertEqual(self.store.table_counts()["outstanding_slot"], 1)

    def test_t05_recovery_rejects_self_consistent_capability_rewrite(self) -> None:
        committed = self._running_operation()
        paused = self.store.pause_local_execution(
            self._local_pause_request(committed, suffix="tamper"),
            self._pause_capability("tamper"), self.authority,
        )
        connection = sqlite3.connect(self.database_path)
        connection.row_factory = sqlite3.Row
        try:
            row = connection.execute(
                "SELECT * FROM local_pause_actions WHERE pause_id = "
                "'local-pause-tamper'"
            ).fetchone()
            body = json.loads(row["body_json"])
            with self.assertRaises(sqlite3.IntegrityError):
                connection.execute(
                    "UPDATE local_pause_actions SET capability_action = "
                    "'STOP_IMMEDIATE' WHERE pause_id = 'local-pause-tamper'"
                )
            connection.rollback()
            body["capability_evidence"].update(
                {
                    "grant_id": "forged-grant",
                    "scope_digest": "forged-scope",
                    "issuer_mac": "forged-mac",
                }
            )
            request_payload = {
                key: body[key]
                for key in PauseLocalExecutionRequest.__dataclass_fields__
            }
            payload = {
                **request_payload,
                "pause_kind": body["pause_kind"],
                "pause_binding_version": body["pause_binding_version"],
                "capability_evidence": body["capability_evidence"],
                "capability_issuer_fingerprint": body[
                    "capability_issuer_fingerprint"
                ],
            }
            body["payload_digest"] = self.store._event_hash(payload)
            event_hash = self.store._event_hash(body)
            body_json = json.dumps(body, sort_keys=True, separators=(",", ":"))
            connection.execute(
                "UPDATE events SET event_hash = ?, body_json = ? WHERE event_id = ?",
                (event_hash, body_json, body["event_id"]),
            )
            connection.execute(
                "UPDATE local_pause_actions SET capability_grant_id = ?, "
                "capability_scope_digest = ?, capability_issuer_mac = ?, "
                "payload_digest = ?, event_hash = ?, body_json = ? "
                "WHERE pause_id = ?",
                (
                    "forged-grant", "forged-scope", "forged-mac",
                    body["payload_digest"], event_hash,
                    body_json, body["pause_id"],
                ),
            )
            connection.execute(
                "UPDATE operator_redemptions SET grant_id = 'forged-grant', "
                "scope_digest = 'forged-scope' "
                "WHERE command_id = ?",
                (body["command_id"],),
            )
            connection.execute(
                "UPDATE command_outcomes SET payload_digest = ?, event_hash = ? "
                "WHERE command_id = ?",
                (body["payload_digest"], event_hash, body["command_id"]),
            )
            connection.execute(
                "UPDATE runs SET head_hash = ? WHERE run_id = ?",
                (event_hash, body["run_id"]),
            )
            connection.execute(
                "UPDATE repositories SET catalog_head = ? WHERE repository_id = ?",
                (event_hash, body["repository_id"]),
            )
            connection.commit()
        finally:
            connection.close()
        self.oracle.allowed_head = event_hash
        with self.assertRaisesRegex(StorageIntegrityError, "local pause"):
            self.store.load_verified("repo-1", authority=self.authority)

    def test_t05_recovery_rejects_surplus_event_schema(self) -> None:
        committed = self._running_operation()
        paused = self.store.pause_local_execution(
            self._local_pause_request(committed, suffix="surplus"),
            self._pause_capability("surplus"), self.authority,
        )
        connection = sqlite3.connect(self.database_path)
        connection.row_factory = sqlite3.Row
        try:
            row = connection.execute(
                "SELECT * FROM local_pause_actions WHERE pause_id = "
                "'local-pause-surplus'"
            ).fetchone()
            body = json.loads(row["body_json"])
            body["surplus"] = "forbidden"
            event_hash = self.store._event_hash(body)
            body_json = json.dumps(body, sort_keys=True, separators=(",", ":"))
            connection.execute(
                "UPDATE events SET event_hash = ?, body_json = ? WHERE event_id = ?",
                (event_hash, body_json, body["event_id"]),
            )
            connection.execute(
                "UPDATE local_pause_actions SET event_hash = ?, body_json = ? "
                "WHERE pause_id = ?",
                (event_hash, body_json, body["pause_id"]),
            )
            connection.execute(
                "UPDATE command_outcomes SET event_hash = ? WHERE command_id = ?",
                (event_hash, body["command_id"]),
            )
            connection.execute(
                "UPDATE runs SET head_hash = ? WHERE run_id = ?",
                (event_hash, body["run_id"]),
            )
            connection.execute(
                "UPDATE repositories SET catalog_head = ? WHERE repository_id = ?",
                (event_hash, body["repository_id"]),
            )
            connection.commit()
        finally:
            connection.close()
        self.oracle.allowed_head = event_hash
        with self.assertRaisesRegex(StorageIntegrityError, "PAUSE_REQUESTED"):
            self.store.load_verified("repo-1", authority=self.authority)

    def test_t05_recovery_rejects_self_consistent_cursor_rewrite(self) -> None:
        committed = self._running_operation()
        paused = self.store.pause_local_execution(
            self._local_pause_request(committed, suffix="cursor"),
            self._pause_capability("cursor"), self.authority,
        )
        connection = sqlite3.connect(self.database_path)
        connection.row_factory = sqlite3.Row
        try:
            row = connection.execute(
                "SELECT * FROM local_pause_actions WHERE pause_id = "
                "'local-pause-cursor'"
            ).fetchone()
            body = json.loads(row["body_json"])
            body["retained_continuation_cursor"] = "forged:cursor"
            event_hash = self.store._event_hash(body)
            body_json = json.dumps(body, sort_keys=True, separators=(",", ":"))
            connection.execute(
                "UPDATE events SET event_hash = ?, body_json = ? WHERE event_id = ?",
                (event_hash, body_json, body["event_id"]),
            )
            connection.execute(
                "UPDATE local_pause_actions SET event_hash = ?, body_json = ? "
                "WHERE pause_id = ?",
                (event_hash, body_json, body["pause_id"]),
            )
            connection.execute(
                "UPDATE command_outcomes SET event_hash = ? WHERE command_id = ?",
                (event_hash, body["command_id"]),
            )
            connection.execute(
                "UPDATE runs SET head_hash = ?, continuation_cursor = ? "
                "WHERE run_id = ?",
                (event_hash, "forged:cursor", body["run_id"]),
            )
            connection.execute(
                "UPDATE repositories SET catalog_head = ? WHERE repository_id = ?",
                (event_hash, body["repository_id"]),
            )
            connection.commit()
        finally:
            connection.close()
        self.oracle.allowed_head = event_hash
        with self.assertRaisesRegex(StorageIntegrityError, "local pause predecessor"):
            self.store.load_verified("repo-1", authority=self.authority)

    def test_t05_rejects_forged_or_foreign_operator_capability(self) -> None:
        committed = self._running_operation()
        request = self._local_pause_request(committed, suffix="authority")
        capability = self._pause_capability("authority")
        with self.assertRaises(DispatchDenied):
            self.store.pause_local_execution(
                request, replace(capability, issuer_mac="forged"), self.authority
            )
        foreign = SyntheticAuthority(b"foreign-t05-issuer-key-0000000000")
        foreign_grant = SyntheticOperatorGrant(
            "foreign-pause-grant", "repo-1", "run-1", "PAUSE",
            "foreign-pause-scope",
        )
        foreign.register_operator(foreign_grant)
        with self.assertRaises(DispatchDenied):
            self.store.pause_local_execution(
                replace(request, pause_id="foreign-pause"),
                foreign.claim_operator(*foreign_grant.__dict__.values()),
                foreign,
            )
        self.assertEqual(self.store.table_counts()["local_pause_actions"], 0)

    def test_t05_recovery_rejects_projection_and_fence_tampering(self) -> None:
        committed = self._running_operation()
        paused = self.store.pause_local_execution(
            self._local_pause_request(committed, suffix="projection"),
            self._pause_capability("projection"), self.authority,
        )
        self.oracle.allowed_head = paused.event_hash
        connection = sqlite3.connect(self.database_path)
        try:
            connection.execute(
                "UPDATE local_pause_actions SET attempt_id = 'other-attempt' "
                "WHERE pause_id = 'local-pause-projection'"
            )
            connection.commit()
        finally:
            connection.close()
        with self.assertRaisesRegex(StorageIntegrityError, "local-pause projection"):
            self.store.load_verified("repo-1", authority=self.authority)
        connection = sqlite3.connect(self.database_path)
        try:
            connection.execute(
                "UPDATE local_pause_actions SET attempt_id = 'attempt-1' "
                "WHERE pause_id = 'local-pause-projection'"
            )
            connection.execute(
                "UPDATE dispatch_fences SET item_id = 'other-item' "
                "WHERE fence_id = 'local-pause-fence-projection'"
            )
            connection.commit()
        finally:
            connection.close()
        with self.assertRaisesRegex(StorageIntegrityError, "dispatch-fence"):
            self.store.load_verified("repo-1", authority=self.authority)

    def test_t05_contact_and_pause_serialize_at_the_fence(self) -> None:
        committed = self._running_operation()
        launched = self.store.claim_operation_launch(self.request(), committed)
        self.store._freshness_oracle = type(
            "AlwaysFresh", (), {"verify": lambda self, *args: True}
        )()
        request = self._local_pause_request(committed, suffix="concurrent")
        capability = self._pause_capability("concurrent")
        barrier = threading.Barrier(2)
        outcomes: list[str] = []
        errors: list[BaseException] = []

        def contact() -> None:
            try:
                barrier.wait()
                self.store._contact_claimed_operation(
                    self.request(), self.capability, committed, launched,
                    self.store._adapter_target_digest("repo-1", "EFFECT"),
                )
                outcomes.append("contact")
            except BaseException as error:
                errors.append(error)

        def pause() -> None:
            try:
                barrier.wait()
                self.store.pause_local_execution(
                    request, capability, self.authority
                )
                outcomes.append("pause")
            except BaseException as error:
                errors.append(error)

        threads = (threading.Thread(target=contact), threading.Thread(target=pause))
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join(timeout=5)
        self.assertTrue(all(not thread.is_alive() for thread in threads))
        self.assertEqual(len(outcomes), 1)
        self.assertEqual(len(errors), 1)
        self.assertIsInstance(errors[0], DispatchDenied)
        connection = sqlite3.connect(self.database_path)
        try:
            contact_count = connection.execute(
                "SELECT COUNT(*) FROM adapter_contacts"
            ).fetchone()[0]
            fence_count = connection.execute(
                "SELECT COUNT(*) FROM dispatch_fences WHERE fence_id = "
                "'local-pause-fence-concurrent'"
            ).fetchone()[0]
            state = connection.execute(
                "SELECT lifecycle_state FROM runs WHERE run_id = 'run-1'"
            ).fetchone()[0]
        finally:
            connection.close()
        if outcomes == ["contact"]:
            self.assertEqual((contact_count, fence_count, state), (1, 0, "RUNNING"))
        else:
            self.assertEqual((contact_count, fence_count, state), (0, 1, "PAUSING"))

    def _resume_capability(self, suffix: str = "1"):
        grant = SyntheticOperatorGrant(
            f"resume-grant-{suffix}", "repo-1", "run-1", "RESUME",
            f"resume-scope-{suffix}",
        )
        self.authority.register_operator(grant)
        return self.authority.claim_operator(*grant.__dict__.values())

    def test_t14_authority_issues_only_bound_resume_capability(self) -> None:
        capability = self._resume_capability()
        self.assertEqual(capability.action, "RESUME")
        self.authority.verify_operator_for_action(capability)

    @staticmethod
    def _run_heads_digest(run_heads: Mapping[str, str]) -> str:
        return hashlib.sha256(
            json.dumps(
                sorted(run_heads.items()),
                ensure_ascii=True,
                separators=(",", ":"),
            ).encode("utf-8")
        ).hexdigest()

    @staticmethod
    def _rebuild_legacy_control_actions(database_path: Path) -> None:
        connection = sqlite3.connect(database_path)
        try:
            connection.executescript(
                """
                ALTER TABLE control_actions RENAME TO control_actions_upgraded;
                CREATE TABLE control_actions (
                    control_id TEXT PRIMARY KEY,
                    command_id TEXT NOT NULL UNIQUE,
                    request_event_id TEXT NOT NULL UNIQUE REFERENCES events(event_id),
                    settled_event_id TEXT NOT NULL UNIQUE REFERENCES events(event_id),
                    repository_id TEXT NOT NULL REFERENCES repositories(repository_id),
                    run_id TEXT NOT NULL REFERENCES runs(run_id),
                    item_id TEXT NOT NULL,
                    action TEXT NOT NULL CHECK (action IN ('PAUSE')),
                    reason_code TEXT NOT NULL,
                    continuation_cursor TEXT NOT NULL,
                    capability_claim_id TEXT NOT NULL UNIQUE,
                    capability_grant_id TEXT NOT NULL,
                    capability_scope_digest TEXT NOT NULL,
                    payload_digest TEXT NOT NULL,
                    event_hash TEXT NOT NULL UNIQUE,
                    resulting_state TEXT NOT NULL,
                    body_json TEXT NOT NULL
                );
                INSERT INTO control_actions SELECT
                    control_id, command_id, request_event_id, settled_event_id,
                    repository_id, run_id, item_id, action, reason_code,
                    continuation_cursor, capability_claim_id,
                    capability_grant_id, capability_scope_digest,
                    payload_digest, event_hash, resulting_state, body_json
                FROM control_actions_upgraded;
                DROP TABLE control_actions_upgraded;
                """
            )
        finally:
            connection.close()

    def test_t14_planned_resume_clears_only_pause_fence_atomically(self) -> None:
        plan = self.store.accept_plan(
            PlanAcceptanceRequest(
                "plan-1", "plan-command-1", "plan-event-1", "repo-1",
                "run-1", "item-1", "effect-1", "revision-1",
                "descriptor-digest", "scope-1", "budget-policy-digest",
                ("check-1",),
            ),
            expected_head="", writer_epoch=1,
        )
        self.oracle.allowed_head = plan.event_hash
        paused = self.store.pause_before_dispatch(
            self._pause_request(), self._pause_capability(), self.authority
        )
        self.oracle.allowed_head = paused.event_hash
        request = self._resume_request(
            catalog_head=paused.event_hash,
            run_heads_digest=self._run_heads_digest(
                {"run-1": paused.event_hash}
            ),
        )
        evidence = self.authority.issue_resume_evidence("resume-proof-1", request)
        resumed = self.store.resume(
            request, self._resume_capability(), evidence, self.authority
        )
        self.assertEqual(resumed.resulting_state, LifecycleState.PLANNED)
        self.assertEqual(self.store.table_counts()["dispatch_fences"], 0)
        self.assertEqual(self.store.table_counts()["resume_actions"], 1)
        self.oracle.allowed_head = resumed.event_hash
        self.store.load_verified("repo-1", authority=self.authority)

    def test_t14_legacy_pause_projection_migrates_without_rewriting_history(self) -> None:
        plan = self.store.accept_plan(
            PlanAcceptanceRequest(
                "plan-1", "plan-command-1", "plan-event-1", "repo-1",
                "run-1", "item-1", "effect-1", "revision-1",
                "descriptor-digest", "scope-1", "budget-policy-digest",
                ("check-1",),
            ),
            expected_head="", writer_epoch=1,
        )
        self.oracle.allowed_head = plan.event_hash
        paused = self.store.pause_before_dispatch(
            self._pause_request(), self._pause_capability(), self.authority
        )
        connection = sqlite3.connect(self.database_path)
        try:
            before = connection.execute(
                "SELECT body_json, continuation_cursor FROM control_actions"
            ).fetchone()
        finally:
            connection.close()
        self._rebuild_legacy_control_actions(self.database_path)
        migrated = SQLiteStateStore(self.database_path, self.oracle, "repo-1")
        connection = sqlite3.connect(self.database_path)
        connection.row_factory = sqlite3.Row
        try:
            columns = tuple(
                row["name"]
                for row in connection.execute(
                    "PRAGMA table_info(control_actions)"
                )
            )
            after = connection.execute(
                "SELECT * FROM control_actions"
            ).fetchone()
        finally:
            connection.close()
        self.assertEqual(after["body_json"], before[0])
        self.assertEqual(after["continuation_cursor"], before[1])
        self.assertEqual(after["preserved_lifecycle"], "PLANNED")
        self.assertIsNone(after["preserved_continuation_cursor"])
        self.assertEqual(
            columns[-2:],
            ("preserved_lifecycle", "preserved_continuation_cursor"),
        )
        self.oracle.allowed_head = paused.event_hash
        migrated.load_verified("repo-1", authority=self.authority)

    def test_t14_true_legacy_blocked_pause_migrates_and_recovers_cursor(self) -> None:
        self._prepare_finalization()
        paused = self.store.pause_before_dispatch(
            replace(
                self._pause_request(), continuation_cursor="FINALIZING"
            ),
            self._pause_capability(),
            self.authority,
        )
        connection = sqlite3.connect(self.database_path)
        try:
            request_body = json.loads(
                connection.execute(
                    "SELECT body_json FROM events WHERE event_id = ?",
                    ("pause-request-event-1",),
                ).fetchone()[0]
            )
            settled_body = json.loads(
                connection.execute(
                    "SELECT body_json FROM events WHERE event_id = ?",
                    ("pause-settled-event-1",),
                ).fetchone()[0]
            )
            for body in (request_body, settled_body):
                body.pop("pause_binding_version")
                body.pop("preserved_lifecycle")
                body.pop("preserved_continuation_cursor")
            request_hash = self.store._event_hash(request_body)
            settled_body["previous_event_hash"] = request_hash
            settled_body["request_event_hash"] = request_hash
            settled_hash = self.store._event_hash(settled_body)
            request_json = json.dumps(
                request_body, sort_keys=True, separators=(",", ":")
            )
            settled_json = json.dumps(
                settled_body, sort_keys=True, separators=(",", ":")
            )
            connection.execute(
                "UPDATE events SET event_hash = ?, body_json = ? "
                "WHERE event_id = 'pause-request-event-1'",
                (request_hash, request_json),
            )
            connection.execute(
                "UPDATE events SET previous_event_hash = ?, event_hash = ?, "
                "body_json = ? WHERE event_id = 'pause-settled-event-1'",
                (request_hash, settled_hash, settled_json),
            )
            connection.execute(
                "UPDATE control_actions SET event_hash = ?, body_json = ?",
                (settled_hash, settled_json),
            )
            connection.execute(
                "UPDATE command_outcomes SET event_hash = ? "
                "WHERE command_id = 'pause-command-1'",
                (settled_hash,),
            )
            connection.execute(
                "UPDATE runs SET head_hash = ? WHERE run_id = 'run-1'",
                (settled_hash,),
            )
            connection.execute(
                "UPDATE repositories SET catalog_head = ? "
                "WHERE repository_id = 'repo-1'",
                (settled_hash,),
            )
            connection.commit()
        finally:
            connection.close()

        self._rebuild_legacy_control_actions(self.database_path)
        migrated = SQLiteStateStore(self.database_path, self.oracle, "repo-1")
        connection = sqlite3.connect(self.database_path)
        try:
            row = connection.execute(
                "SELECT body_json, preserved_lifecycle, "
                "preserved_continuation_cursor FROM control_actions"
            ).fetchone()
        finally:
            connection.close()
        self.assertEqual(row, (settled_json, "BLOCKED", "FINALIZING"))
        self.oracle.allowed_head = settled_hash
        migrated.load_verified("repo-1", authority=self.authority)

    def test_t14_partial_pause_projection_migration_fails_closed(self) -> None:
        self._rebuild_legacy_control_actions(self.database_path)
        connection = sqlite3.connect(self.database_path)
        try:
            connection.execute(
                "ALTER TABLE control_actions ADD COLUMN preserved_lifecycle TEXT"
            )
            connection.commit()
        finally:
            connection.close()
        with self.assertRaisesRegex(StorageIntegrityError, "partially migrated"):
            SQLiteStateStore(self.database_path, self.oracle, "repo-1")
        connection = sqlite3.connect(self.database_path)
        try:
            columns = {
                row[1]
                for row in connection.execute(
                    "PRAGMA table_info(control_actions)"
                )
            }
        finally:
            connection.close()
        self.assertIn("preserved_lifecycle", columns)
        self.assertNotIn("preserved_continuation_cursor", columns)

    def test_t14_legacy_pause_migration_rolls_back_on_bad_prefix(self) -> None:
        plan = self.store.accept_plan(
            PlanAcceptanceRequest(
                "plan-1", "plan-command-1", "plan-event-1", "repo-1",
                "run-1", "item-1", "effect-1", "revision-1",
                "descriptor-digest", "scope-1", "budget-policy-digest",
                ("check-1",),
            ),
            expected_head="", writer_epoch=1,
        )
        self.oracle.allowed_head = plan.event_hash
        self.store.pause_before_dispatch(
            self._pause_request(), self._pause_capability(), self.authority
        )
        self._rebuild_legacy_control_actions(self.database_path)
        connection = sqlite3.connect(self.database_path)
        try:
            connection.execute(
                "UPDATE events SET event_kind = 'STOP_RECORDED' "
                "WHERE event_id = 'pause-request-event-1'"
            )
            connection.commit()
        finally:
            connection.close()
        with self.assertRaisesRegex(StorageIntegrityError, "prefix"):
            SQLiteStateStore(self.database_path, self.oracle, "repo-1")
        connection = sqlite3.connect(self.database_path)
        try:
            columns = tuple(
                row[1]
                for row in connection.execute(
                    "PRAGMA table_info(control_actions)"
                )
            )
        finally:
            connection.close()
        self.assertNotIn("preserved_lifecycle", columns)
        self.assertNotIn("preserved_continuation_cursor", columns)

    def test_t14_route_restores_clean_validation_but_retains_t16_blockers(self) -> None:
        self.assertTrue(
            hasattr(storage_module, "_derive_resume_route"),
            "T14 requires a deterministic route decision",
        )
        derive = storage_module._derive_resume_route
        self.assertEqual(
            derive(LifecycleState.VALIDATING, LifecycleState.VALIDATING.value, ()),
            LifecycleState.VALIDATING,
        )
        for cursor in (
            LifecycleState.VALIDATING.value,
            "validation-recovery:recovery-1",
            "FINALIZING",
        ):
            with self.subTest(cursor=cursor):
                self.assertEqual(
                    derive(
                        LifecycleState.BLOCKED,
                        cursor,
                        ("T16_OBLIGATION_PENDING",),
                    ),
                    LifecycleState.BLOCKED,
                )

    def test_t14_resume_retains_readiness_blocker_and_cursor(self) -> None:
        plan = self.store.accept_plan(
            PlanAcceptanceRequest(
                "plan-1", "plan-command-1", "plan-event-1", "repo-1",
                "run-1", "item-1", "effect-1", "revision-1",
                "descriptor-digest", "scope-1", "budget-policy-digest",
                ("check-1",),
            ),
            expected_head="", writer_epoch=1,
        )
        self.oracle.allowed_head = plan.event_hash
        blocked = self.store.evaluate_readiness(
            ReadinessEvaluationRequest(
                "readiness-1", "readiness-command-1", "readiness-event-1",
                "repo-1", "run-1", "item-1", "plan-1", "revision-1",
                plan.event_hash, None, "inputs-evidence-1", False,
            )
        )
        self.oracle.allowed_head = blocked.event_hash
        paused = self.store.pause_before_dispatch(
            self._pause_request(), self._pause_capability(), self.authority
        )
        self.oracle.allowed_head = paused.event_hash
        request = self._resume_request(
            catalog_head=paused.event_hash,
            run_heads_digest=self._run_heads_digest(
                {"run-1": paused.event_hash}
            ),
        )
        request = replace(
            request, expected_preserved_lifecycle=LifecycleState.BLOCKED
        )
        resumed = self.store.resume(
            request,
            self._resume_capability(),
            self.authority.issue_resume_evidence("resume-proof-1", request),
            self.authority,
        )
        self.assertEqual(resumed.resulting_state, LifecycleState.BLOCKED)
        connection = sqlite3.connect(self.database_path)
        try:
            blocker_codes = json.loads(
                connection.execute(
                    "SELECT blocker_codes_json FROM resume_actions"
                ).fetchone()[0]
            )
        finally:
            connection.close()
        self.assertIn("INPUTS_NOT_READY", blocker_codes)

    def test_t14_resume_cannot_bypass_recoverable_validation_blocker(self) -> None:
        _, failed = self._prepare_recoverable_application()
        paused = self.store.pause_before_dispatch(
            replace(
                self._pause_request(),
                continuation_cursor=LifecycleState.VALIDATING.value,
            ),
            self._pause_capability(),
            self.authority,
        )
        self.oracle.allowed_head = paused.event_hash
        request = replace(
            self._resume_request(
                catalog_head=paused.event_hash,
                run_heads_digest=self._run_heads_digest(
                    {"run-1": paused.event_hash}
                ),
            ),
            expected_preserved_lifecycle=LifecycleState.BLOCKED,
            expected_preserved_continuation_cursor=LifecycleState.VALIDATING.value,
        )
        resumed = self.store.resume(
            request,
            self._resume_capability(),
            self.authority.issue_resume_evidence("resume-proof-1", request),
            self.authority,
        )
        self.assertEqual(failed.resulting_state, LifecycleState.BLOCKED)
        self.assertEqual(resumed.resulting_state, LifecycleState.BLOCKED)
        connection = sqlite3.connect(self.database_path)
        try:
            state = connection.execute(
                "SELECT lifecycle_state, continuation_cursor FROM runs "
                "WHERE run_id = 'run-1'"
            ).fetchone()
        finally:
            connection.close()
        self.assertEqual(state, ("BLOCKED", LifecycleState.VALIDATING.value))
        self.assertEqual(self.store.table_counts()["outstanding_slot"], 1)
        self.oracle.allowed_head = resumed.event_hash
        self.store.load_verified("repo-1", authority=self.authority)

    def test_t14_finalizing_cursor_remains_blocked_after_restart(self) -> None:
        self._prepare_finalization()
        paused = self.store.pause_before_dispatch(
            replace(
                self._pause_request(), continuation_cursor="FINALIZING"
            ),
            self._pause_capability(),
            self.authority,
        )
        self.oracle.allowed_head = paused.event_hash
        request = replace(
            self._resume_request(
                catalog_head=paused.event_hash,
                run_heads_digest=self._run_heads_digest(
                    {"run-1": paused.event_hash}
                ),
            ),
            expected_preserved_lifecycle=LifecycleState.BLOCKED,
            expected_preserved_continuation_cursor="FINALIZING",
        )
        resumed = self.store.resume(
            request,
            self._resume_capability(),
            self.authority.issue_resume_evidence("resume-proof-1", request),
            self.authority,
        )
        self.assertEqual(resumed.resulting_state, LifecycleState.BLOCKED)
        connection = sqlite3.connect(self.database_path)
        try:
            state = connection.execute(
                "SELECT lifecycle_state, continuation_cursor FROM runs "
                "WHERE run_id = 'run-1'"
            ).fetchone()
        finally:
            connection.close()
        self.assertEqual(state, ("BLOCKED", "FINALIZING"))
        self.oracle.allowed_head = resumed.event_hash
        self.store.load_verified("repo-1", authority=self.authority)

    def test_t14_unrelated_active_validator_blocks_but_survives_recovery(self) -> None:
        observation = self._record_effect_observation(("check-1",))
        validator_request, validator_capability = self._validator_intent(
            observation
        )
        validator_intent = self.store.commit_validator_intent(
            validator_request, validator_capability, self.authority
        )
        self.oracle.allowed_head = validator_intent.event_hash
        connection = sqlite3.connect(self.database_path)
        try:
            writer_epoch = connection.execute(
                "SELECT MAX(writer_epoch) + 1 FROM events"
            ).fetchone()[0]
        finally:
            connection.close()
        plan = self.store.accept_plan(
            PlanAcceptanceRequest(
                "plan-2", "plan-command-2", "plan-event-2", "repo-1",
                "run-2", "item-2", "effect-2", "revision-2",
                "descriptor-2", "scope-2", "budget-policy-2", ("check-2",),
            ),
            expected_head=validator_intent.event_hash,
            writer_epoch=writer_epoch,
        )
        self.oracle.allowed_head = plan.event_hash
        blocked = self.store.evaluate_readiness(
            ReadinessEvaluationRequest(
                "readiness-2", "readiness-command-2", "readiness-event-2",
                "repo-1", "run-2", "item-2", "plan-2", "revision-2",
                plan.event_hash, None, "inputs-evidence-2", True,
            )
        )
        self.oracle.allowed_head = blocked.event_hash
        pause_grant = SyntheticOperatorGrant(
            "operator-grant-2", "repo-1", "run-2", "PAUSE",
            "operator-scope-2",
        )
        self.authority.register_operator(pause_grant)
        pause_capability = self.authority.claim_operator(
            *pause_grant.__dict__.values()
        )
        paused = self.store.pause_before_dispatch(
            PauseBeforeDispatchRequest(
                "pause-2", "pause-command-2", "pause-request-event-2",
                "pause-settled-event-2", "pause-fence-2", "repo-1",
                "run-2", "item-2", "OPERATOR_PAUSE", None,
            ),
            pause_capability,
            self.authority,
        )
        self.oracle.allowed_head = paused.event_hash
        connection = sqlite3.connect(self.database_path)
        try:
            run_heads = dict(
                connection.execute("SELECT run_id, head_hash FROM runs")
            )
        finally:
            connection.close()
        request = ResumeRequest(
            "resume-2", "resume-command-2", "resume-event-2", "repo-1",
            "run-2", "item-2", "effect-2", "plan-2", "revision-2",
            "pause-2", "pause-settled-event-2", paused.event_hash,
            "pause-fence-2", LifecycleState.BLOCKED, None,
            paused.event_hash, paused.event_hash,
            self._run_heads_digest(run_heads),
        )
        resume_grant = SyntheticOperatorGrant(
            "resume-grant-2", "repo-1", "run-2", "RESUME",
            "resume-scope-2",
        )
        self.authority.register_operator(resume_grant)
        resumed = self.store.resume(
            request,
            self.authority.claim_operator(*resume_grant.__dict__.values()),
            self.authority.issue_resume_evidence("resume-proof-2", request),
            self.authority,
        )
        self.assertEqual(resumed.resulting_state, LifecycleState.BLOCKED)
        self.oracle.allowed_head = resumed.event_hash
        self.store.load_verified("repo-1", authority=self.authority)

    def test_t14_intervening_binding_fact_survives_exact_pause_resume(self) -> None:
        plan = self.store.accept_plan(
            PlanAcceptanceRequest(
                "plan-1", "plan-command-1", "plan-event-1", "repo-1",
                "run-1", "item-1", "effect-1", "revision-1",
                "descriptor-digest", "scope-1", "budget-policy-digest",
                ("check-1",),
            ),
            expected_head="", writer_epoch=1,
        )
        self.oracle.allowed_head = plan.event_hash
        paused = self.store.pause_before_dispatch(
            self._pause_request(), self._pause_capability(), self.authority
        )
        self.oracle.allowed_head = paused.event_hash
        mismatch_request = BindingMismatchRequest(
            "mismatch-t14", "observation-t14", "mismatch-command-t14",
            "mismatch-event-t14", "repo-1", "run-1", "item-1", "effect-1",
            BindingMismatchKind.SOURCE, "source-tree-1", "source-tree-later",
            paused.event_hash, "BINDING_MISMATCH_SOURCE",
        )
        mismatch = self.store.record_binding_mismatch(
            mismatch_request,
            self.authority.issue_binding_observation(mismatch_request),
            self.authority,
            expected_head=paused.event_hash,
            writer_epoch=3,
        )
        self.assertEqual(mismatch.resulting_state, LifecycleState.PAUSED)
        self.oracle.allowed_head = mismatch.event_hash
        request = replace(
            self._resume_request(
                catalog_head=mismatch.event_hash,
                run_heads_digest=self._run_heads_digest(
                    {"run-1": mismatch.event_hash}
                ),
            ),
            source_pause_settled_event_hash=paused.event_hash,
            expected_run_head=mismatch.event_hash,
        )
        resumed = self.store.resume(
            request,
            self._resume_capability(),
            self.authority.issue_resume_evidence("resume-proof-1", request),
            self.authority,
        )
        self.assertEqual(resumed.resulting_state, LifecycleState.BLOCKED)
        connection = sqlite3.connect(self.database_path)
        try:
            fences = connection.execute(
                "SELECT reason_code FROM dispatch_fences"
            ).fetchall()
        finally:
            connection.close()
        self.assertEqual(fences, [("BINDING_MISMATCH_SOURCE",)])
        self.oracle.allowed_head = resumed.event_hash
        self.store.load_verified("repo-1", authority=self.authority)

    def test_t14_resume_vector_mismatch_denies_without_clearing_pause(self) -> None:
        plan = self.store.accept_plan(
            PlanAcceptanceRequest(
                "plan-1", "plan-command-1", "plan-event-1", "repo-1",
                "run-1", "item-1", "effect-1", "revision-1",
                "descriptor-digest", "scope-1", "budget-policy-digest",
                ("check-1",),
            ),
            expected_head="", writer_epoch=1,
        )
        self.oracle.allowed_head = plan.event_hash
        paused = self.store.pause_before_dispatch(
            self._pause_request(), self._pause_capability(), self.authority
        )
        self.oracle.allowed_head = paused.event_hash
        request = self._resume_request(
            catalog_head=paused.event_hash,
            run_heads_digest=self._run_heads_digest({}),
        )
        with self.assertRaisesRegex(DispatchDenied, "head vector"):
            self.store.resume(
                request,
                self._resume_capability(),
                self.authority.issue_resume_evidence("resume-proof-1", request),
                self.authority,
            )
        self.assertEqual(self.store.load_run_lifecycle("run-1"), LifecycleState.PAUSED)
        self.assertEqual(self.store.table_counts()["dispatch_fences"], 1)
        self.assertEqual(self.store.table_counts()["resume_actions"], 0)

    def test_t14_resume_precommit_rollback_and_postcommit_replay(self) -> None:
        plan = self.store.accept_plan(
            PlanAcceptanceRequest(
                "plan-1", "plan-command-1", "plan-event-1", "repo-1",
                "run-1", "item-1", "effect-1", "revision-1",
                "descriptor-digest", "scope-1", "budget-policy-digest",
                ("check-1",),
            ),
            expected_head="", writer_epoch=1,
        )
        self.oracle.allowed_head = plan.event_hash
        paused = self.store.pause_before_dispatch(
            self._pause_request(), self._pause_capability(), self.authority
        )
        self.oracle.allowed_head = paused.event_hash
        request = self._resume_request(
            catalog_head=paused.event_hash,
            run_heads_digest=self._run_heads_digest(
                {"run-1": paused.event_hash}
            ),
        )
        capability = self._resume_capability()
        evidence = self.authority.issue_resume_evidence("resume-proof-1", request)
        with self.assertRaises(InjectedFailure):
            self.store.resume(
                request, capability, evidence, self.authority,
                failure_hook=raise_at("after_resume_writes_before_commit"),
            )
        self.assertEqual(self.store.load_run_lifecycle("run-1"), LifecycleState.PAUSED)
        self.assertEqual(self.store.table_counts()["resume_actions"], 0)
        self.assertEqual(self.store.table_counts()["dispatch_fences"], 1)

        with self.assertRaises(InjectedFailure):
            self.store.resume(
                request, capability, evidence, self.authority,
                failure_hook=raise_at(
                    "after_resume_commit_before_acknowledgement"
                ),
            )
        connection = sqlite3.connect(self.database_path)
        try:
            committed_hash = connection.execute(
                "SELECT event_hash FROM resume_actions"
            ).fetchone()[0]
        finally:
            connection.close()
        self.oracle.allowed_head = committed_hash
        replay = self.store.resume(
            request, capability, evidence, self.authority
        )
        self.assertTrue(replay.replayed)
        self.assertEqual(replay.event_hash, committed_hash)
        self.assertEqual(self.store.table_counts()["resume_actions"], 1)
        self.assertEqual(self.store.table_counts()["dispatch_fences"], 0)

    def test_t14_recovery_rejects_self_consistent_capability_mac_rewrite(self) -> None:
        plan = self.store.accept_plan(
            PlanAcceptanceRequest(
                "plan-1", "plan-command-1", "plan-event-1", "repo-1",
                "run-1", "item-1", "effect-1", "revision-1",
                "descriptor-digest", "scope-1", "budget-policy-digest",
                ("check-1",),
            ),
            expected_head="", writer_epoch=1,
        )
        self.oracle.allowed_head = plan.event_hash
        paused = self.store.pause_before_dispatch(
            self._pause_request(), self._pause_capability(), self.authority
        )
        self.oracle.allowed_head = paused.event_hash
        request = self._resume_request(
            catalog_head=paused.event_hash,
            run_heads_digest=self._run_heads_digest(
                {"run-1": paused.event_hash}
            ),
        )
        resumed = self.store.resume(
            request,
            self._resume_capability(),
            self.authority.issue_resume_evidence("resume-proof-1", request),
            self.authority,
        )
        connection = sqlite3.connect(self.database_path)
        connection.row_factory = sqlite3.Row
        try:
            row = connection.execute(
                "SELECT body_json FROM resume_actions"
            ).fetchone()
            body = json.loads(row["body_json"])
            body["capability_evidence"]["issuer_mac"] = "0" * 64
            event_hash = self.store._event_hash(body)
            body_json = json.dumps(body, sort_keys=True, separators=(",", ":"))
            connection.execute(
                "UPDATE events SET event_hash = ?, body_json = ? "
                "WHERE event_id = ?",
                (event_hash, body_json, resumed.event_id),
            )
            connection.execute(
                "UPDATE resume_actions SET capability_issuer_mac = ?, "
                "event_hash = ?, body_json = ?",
                ("0" * 64, event_hash, body_json),
            )
            connection.execute(
                "UPDATE command_outcomes SET event_hash = ? WHERE command_id = ?",
                (event_hash, resumed.command_id),
            )
            connection.execute(
                "UPDATE runs SET head_hash = ? WHERE run_id = 'run-1'",
                (event_hash,),
            )
            connection.execute(
                "UPDATE repositories SET catalog_head = ? WHERE repository_id = 'repo-1'",
                (event_hash,),
            )
            connection.commit()
        finally:
            connection.close()
        self.oracle.allowed_head = event_hash
        with self.assertRaisesRegex(
            (DispatchDenied, StorageIntegrityError), "resume|operator|capability"
        ):
            self.store.load_verified("repo-1", authority=self.authority)

    def test_t14_recovery_rejects_self_consistent_route_rewrite(self) -> None:
        plan = self.store.accept_plan(
            PlanAcceptanceRequest(
                "plan-1", "plan-command-1", "plan-event-1", "repo-1",
                "run-1", "item-1", "effect-1", "revision-1",
                "descriptor-digest", "scope-1", "budget-policy-digest",
                ("check-1",),
            ),
            expected_head="", writer_epoch=1,
        )
        self.oracle.allowed_head = plan.event_hash
        paused = self.store.pause_before_dispatch(
            self._pause_request(), self._pause_capability(), self.authority
        )
        self.oracle.allowed_head = paused.event_hash
        request = self._resume_request(
            catalog_head=paused.event_hash,
            run_heads_digest=self._run_heads_digest(
                {"run-1": paused.event_hash}
            ),
        )
        resumed = self.store.resume(
            request,
            self._resume_capability(),
            self.authority.issue_resume_evidence("resume-proof-1", request),
            self.authority,
        )
        connection = sqlite3.connect(self.database_path)
        connection.row_factory = sqlite3.Row
        try:
            body = json.loads(
                connection.execute(
                    "SELECT body_json FROM resume_actions"
                ).fetchone()["body_json"]
            )
            body["blocker_codes"] = ["FABRICATED_BLOCKER"]
            body["lifecycle_to"] = LifecycleState.BLOCKED.value
            event_hash = self.store._event_hash(body)
            body_json = json.dumps(body, sort_keys=True, separators=(",", ":"))
            connection.execute(
                "UPDATE events SET event_hash = ?, body_json = ? "
                "WHERE event_id = ?",
                (event_hash, body_json, resumed.event_id),
            )
            connection.execute(
                "UPDATE resume_actions SET blocker_codes_json = ?, "
                "resulting_state = 'BLOCKED', event_hash = ?, body_json = ?",
                ('["FABRICATED_BLOCKER"]', event_hash, body_json),
            )
            connection.execute(
                "UPDATE command_outcomes SET event_hash = ? WHERE command_id = ?",
                (event_hash, resumed.command_id),
            )
            connection.execute(
                "UPDATE runs SET lifecycle_state = 'BLOCKED', head_hash = ? "
                "WHERE run_id = 'run-1'",
                (event_hash,),
            )
            connection.execute(
                "UPDATE repositories SET catalog_head = ? WHERE repository_id = 'repo-1'",
                (event_hash,),
            )
            connection.commit()
        finally:
            connection.close()
        self.oracle.allowed_head = event_hash
        with self.assertRaisesRegex(StorageIntegrityError, "resume.*route|route.*resume"):
            self.store.load_verified("repo-1", authority=self.authority)

    def test_t14_recovery_rejects_unknown_resume_schema_fields_and_version(self) -> None:
        plan = self.store.accept_plan(
            PlanAcceptanceRequest(
                "plan-1", "plan-command-1", "plan-event-1", "repo-1",
                "run-1", "item-1", "effect-1", "revision-1",
                "descriptor-digest", "scope-1", "budget-policy-digest",
                ("check-1",),
            ),
            expected_head="", writer_epoch=1,
        )
        self.oracle.allowed_head = plan.event_hash
        paused = self.store.pause_before_dispatch(
            self._pause_request(), self._pause_capability(), self.authority
        )
        self.oracle.allowed_head = paused.event_hash
        request = self._resume_request(
            catalog_head=paused.event_hash,
            run_heads_digest=self._run_heads_digest(
                {"run-1": paused.event_hash}
            ),
        )
        resumed = self.store.resume(
            request,
            self._resume_capability(),
            self.authority.issue_resume_evidence("resume-proof-1", request),
            self.authority,
        )
        connection = sqlite3.connect(self.database_path)
        try:
            original_body = json.loads(
                connection.execute(
                    "SELECT body_json FROM resume_actions"
                ).fetchone()[0]
            )
        finally:
            connection.close()

        for mutation in ("extra-field", "unknown-version"):
            with self.subTest(mutation=mutation):
                body = dict(original_body)
                if mutation == "extra-field":
                    body["unexpected_resume_field"] = "must-deny"
                else:
                    body["schema_version"] = 2
                event_hash = self.store._event_hash(body)
                body_json = json.dumps(
                    body, sort_keys=True, separators=(",", ":")
                )
                connection = sqlite3.connect(self.database_path)
                try:
                    connection.execute(
                        "UPDATE events SET event_hash = ?, body_json = ? "
                        "WHERE event_id = ?",
                        (event_hash, body_json, resumed.event_id),
                    )
                    connection.execute(
                        "UPDATE resume_actions SET event_hash = ?, body_json = ?",
                        (event_hash, body_json),
                    )
                    connection.execute(
                        "UPDATE command_outcomes SET event_hash = ? WHERE command_id = ?",
                        (event_hash, resumed.command_id),
                    )
                    connection.execute(
                        "UPDATE runs SET head_hash = ? WHERE run_id = 'run-1'",
                        (event_hash,),
                    )
                    connection.execute(
                        "UPDATE repositories SET catalog_head = ? "
                        "WHERE repository_id = 'repo-1'",
                        (event_hash,),
                    )
                    connection.commit()
                finally:
                    connection.close()
                self.oracle.allowed_head = event_hash
                if mutation == "extra-field":
                    with self.assertRaisesRegex(
                        StorageIntegrityError, "RESUME.*schema|schema.*RESUME"
                    ):
                        self.store.load_verified(
                            "repo-1", authority=self.authority
                        )
                else:
                    with self.assertRaises(StorageIntegrityError):
                        self.store.load_verified(
                            "repo-1", authority=self.authority
                        )

    def test_t13_pre_action_revocation_blocks_matching_effect_grant(self) -> None:
        request = self.request()
        plan = self.store.accept_plan(
            PlanAcceptanceRequest(
                "plan-t13", "plan-command-t13", "plan-event-t13",
                request.repository_id, request.run_id, request.item_id,
                request.logical_effect_id, "revision-1",
                request.effect_descriptor_digest, self.capability.scope_digest,
                request.budget_policy_digest, ("check-1",),
            ),
            expected_head="",
            writer_epoch=1,
        )
        fact = AuthorityLifecycleFactRequest(
            "fact-t13", "fact-command-t13", "fact-event-t13",
            request.repository_id, request.run_id, request.item_id,
            request.logical_effect_id, "EFFECT", self.capability.grant_id,
            "EXECUTE_EFFECT", self.capability.scope_digest,
            AuthorityFactKind.REVOKED, GovernedOrder.BEFORE, "NO_ACTION",
            None, None,
        )
        evidence: SyntheticAuthorityLifecycleEvidence = (
            self.authority.issue_authority_lifecycle_evidence("proof-t13", fact)
        )
        self.oracle.allowed_head = plan.event_hash

        recorded = self.store.record_authority_fact(
            fact,
            evidence,
            self.authority,
            expected_head=plan.event_hash,
            writer_epoch=2,
        )

        self.assertEqual(recorded.resulting_state, LifecycleState.BLOCKED)
        self.oracle.allowed_head = recorded.event_hash
        with self.assertRaisesRegex(DispatchDenied, "authority"):
            self.store.commit_intent(
                request,
                self.capability,
                self.authority,
                expected_head=recorded.event_hash,
                writer_epoch=3,
            )

    def test_t13_after_action_expiry_is_future_only(self) -> None:
        intent = self._commit_planned_intent(
            self.request(), self.capability, self.authority,
            expected_head="", writer_epoch=1,
        )
        self.oracle.allowed_head = intent.event_hash
        fact = AuthorityLifecycleFactRequest(
            "fact-after", "fact-command-after", "fact-event-after",
            "repo-1", "run-1", "item-1", "effect-1", "EFFECT",
            "grant-1", "EXECUTE_EFFECT", "scope-1",
            AuthorityFactKind.EXPIRED, GovernedOrder.AFTER, "INTENT",
            intent.event_id, intent.event_hash,
        )
        recorded = self.store.record_authority_fact(
            fact,
            self.authority.issue_authority_lifecycle_evidence(
                "proof-after", fact
            ),
            self.authority,
            expected_head=intent.event_hash,
            writer_epoch=3,
        )
        self.assertEqual(recorded.resulting_state, LifecycleState.RUNNING)
        connection = self.store._connect()
        try:
            self.assertEqual(
                connection.execute(
                    "SELECT COUNT(*) FROM effective_authority"
                ).fetchone()[0],
                1,
            )
            self.assertEqual(
                connection.execute(
                    "SELECT COUNT(*) FROM dispatch_fences"
                ).fetchone()[0],
                0,
            )
        finally:
            connection.close()
        self.oracle.allowed_head = recorded.event_hash
        self.store.load_verified("repo-1")

    def test_t13_unknown_claim_status_retains_slot_and_disputes_history(self) -> None:
        intent = self._commit_planned_intent(
            self.request(), self.capability, self.authority,
            expected_head="", writer_epoch=1,
        )
        self.oracle.allowed_head = intent.event_hash
        fact = AuthorityLifecycleFactRequest(
            "fact-unknown", "fact-command-unknown", "fact-event-unknown",
            "repo-1", "run-1", "item-1", "effect-1", "EFFECT",
            "grant-1", "EXECUTE_EFFECT", "scope-1",
            AuthorityFactKind.CLAIM_STATUS_UNKNOWN, GovernedOrder.UNKNOWN,
            "INTENT", intent.event_id, intent.event_hash,
        )
        recorded = self.store.record_authority_fact(
            fact,
            self.authority.issue_authority_lifecycle_evidence(
                "proof-unknown", fact
            ),
            self.authority,
            expected_head=intent.event_hash,
            writer_epoch=3,
        )
        self.assertEqual(
            recorded.resulting_state, LifecycleState.RECONCILIATION_REQUIRED
        )
        connection = sqlite3.connect(self.database_path)
        try:
            self.assertEqual(
                connection.execute(
                    "SELECT status FROM effective_authority"
                ).fetchone()[0],
                "UNKNOWN",
            )
            self.assertEqual(
                connection.execute(
                    "SELECT COUNT(*) FROM outstanding_slot"
                ).fetchone()[0],
                1,
            )
        finally:
            connection.close()

    def test_t13_own_consumption_is_nonbreaching_and_mismatch_rejects(self) -> None:
        intent = self._commit_planned_intent(
            self.request(), self.capability, self.authority,
            expected_head="", writer_epoch=1,
        )
        self.oracle.allowed_head = intent.event_hash
        fact = AuthorityLifecycleFactRequest(
            "fact-own", "fact-command-own", "fact-event-own", "repo-1",
            "run-1", "item-1", "effect-1", "EFFECT", "grant-1",
            "EXECUTE_EFFECT", "scope-1", AuthorityFactKind.OWN_CONSUMED,
            GovernedOrder.DURING, "INTENT", intent.event_id, intent.event_hash,
        )
        recorded = self.store.record_authority_fact(
            fact,
            self.authority.issue_authority_lifecycle_evidence("proof-own", fact),
            self.authority,
            expected_head=intent.event_hash,
            writer_epoch=3,
        )
        self.assertEqual(recorded.resulting_state, LifecycleState.RUNNING)
        connection = sqlite3.connect(self.database_path)
        try:
            self.assertEqual(
                connection.execute(
                    "SELECT COUNT(*) FROM effective_authority"
                ).fetchone()[0],
                1,
            )
            self.assertEqual(
                connection.execute(
                    "SELECT COUNT(*) FROM dispatch_fences"
                ).fetchone()[0],
                0,
            )
        finally:
            connection.close()
        self.oracle.allowed_head = recorded.event_hash
        launch = self.store.claim_operation_launch(self.request(), intent)
        self.oracle.allowed_head = launch.event_hash
        self.store._contact_claimed_operation(
            self.request(), self.capability, intent, launch,
            self.store._adapter_target_digest("repo-1", "EFFECT"),
        )
        connection = self.store._connect()
        try:
            contact_head = connection.execute(
                "SELECT catalog_head FROM repositories WHERE repository_id = 'repo-1'"
            ).fetchone()[0]
            with self.assertRaisesRegex(DispatchDenied, "authority"):
                self.store._require_effective_authority(
                    connection, self.authority.issuer_fingerprint, "EFFECT",
                    "grant-1", "EXECUTE_EFFECT", "scope-1",
                    continuing_event_id="different-intent",
                    continuing_event_hash="different-hash",
                )
        finally:
            connection.close()
        self.oracle.allowed_head = contact_head
        self.store.load_verified("repo-1")
        mismatched = replace(
            fact,
            fact_id="fact-own-bad",
            command_id="fact-command-own-bad",
            event_id="fact-event-own-bad",
            governed_event_hash="0" * 64,
        )
        self.oracle.allowed_head = contact_head
        with self.assertRaisesRegex(DispatchDenied, "boundary"):
            self.store.record_authority_fact(
                mismatched,
                self.authority.issue_authority_lifecycle_evidence(
                    "proof-own-bad", mismatched
                ),
                self.authority,
                expected_head=contact_head,
                writer_epoch=6,
            )

    def test_t13_exact_correction_clears_only_its_effective_generation(self) -> None:
        request = self.request()
        plan = self.store.accept_plan(
            PlanAcceptanceRequest(
                "plan-correct", "plan-command-correct", "plan-event-correct",
                "repo-1", "run-1", "item-1", "effect-1", "revision-1",
                request.effect_descriptor_digest, "scope-1",
                request.budget_policy_digest, ("check-1",),
            ),
            expected_head="", writer_epoch=1,
        )
        self.oracle.allowed_head = plan.event_hash
        denied = AuthorityLifecycleFactRequest(
            "fact-denied", "fact-command-denied", "fact-event-denied",
            "repo-1", "run-1", "item-1", "effect-1", "EFFECT",
            "grant-1", "EXECUTE_EFFECT", "scope-1",
            AuthorityFactKind.REVOKED, GovernedOrder.BEFORE, "NO_ACTION",
            None, None,
        )
        denial = self.store.record_authority_fact(
            denied,
            self.authority.issue_authority_lifecycle_evidence(
                "proof-denied", denied
            ),
            self.authority,
            expected_head=plan.event_hash, writer_epoch=2,
        )
        self.oracle.allowed_head = denial.event_hash
        correction = AuthorityLifecycleFactRequest(
            "fact-correct", "fact-command-correct", "fact-event-correct",
            "repo-1", "run-1", "item-1", "effect-1", "EFFECT",
            "grant-1", "EXECUTE_EFFECT", "scope-1",
            AuthorityFactKind.CORRECTION, GovernedOrder.BEFORE, "NO_ACTION",
            None, None, corrected_fact_id=denied.fact_id,
            corrected_event_hash=denial.event_hash,
        )
        corrected = self.store.record_authority_fact(
            correction,
            self.authority.issue_authority_lifecycle_evidence(
                "proof-correct", correction
            ),
            self.authority,
            expected_head=denial.event_hash, writer_epoch=3,
        )
        self.assertEqual(corrected.resulting_state, LifecycleState.BLOCKED)
        connection = sqlite3.connect(self.database_path)
        try:
            self.assertEqual(
                connection.execute(
                    "SELECT COUNT(*) FROM effective_authority"
                ).fetchone()[0],
                0,
            )
            self.assertEqual(
                connection.execute(
                    "SELECT COUNT(*) FROM dispatch_fences"
                ).fetchone()[0],
                0,
            )
        finally:
            connection.close()
        self.oracle.allowed_head = corrected.event_hash
        self.store.load_verified("repo-1")

    def test_t13_correction_restores_older_uncorrected_denial(self) -> None:
        request = self.request()
        plan = self.store.accept_plan(
            PlanAcceptanceRequest(
                "plan-stack", "plan-command-stack", "plan-event-stack",
                "repo-1", "run-1", "item-1", "effect-1", "revision-1",
                request.effect_descriptor_digest, "scope-1",
                request.budget_policy_digest, ("check-1",),
            ),
            expected_head="", writer_epoch=1,
        )
        self.oracle.allowed_head = plan.event_hash
        first = AuthorityLifecycleFactRequest(
            "fact-stack-1", "fact-command-stack-1", "fact-event-stack-1",
            "repo-1", "run-1", "item-1", "effect-1", "EFFECT",
            "grant-1", "EXECUTE_EFFECT", "scope-1",
            AuthorityFactKind.REVOKED, GovernedOrder.BEFORE, "NO_ACTION",
            None, None,
        )
        first_receipt = self.store.record_authority_fact(
            first,
            self.authority.issue_authority_lifecycle_evidence(
                "proof-stack-1", first
            ),
            self.authority,
            expected_head=plan.event_hash, writer_epoch=2,
        )
        self.oracle.allowed_head = first_receipt.event_hash
        second = replace(
            first,
            fact_id="fact-stack-2", command_id="fact-command-stack-2",
            event_id="fact-event-stack-2",
            fact_kind=AuthorityFactKind.SOURCE_UNAVAILABLE,
            governed_order=GovernedOrder.UNKNOWN,
        )
        second_receipt = self.store.record_authority_fact(
            second,
            self.authority.issue_authority_lifecycle_evidence(
                "proof-stack-2", second
            ),
            self.authority,
            expected_head=first_receipt.event_hash, writer_epoch=3,
        )
        self.oracle.allowed_head = second_receipt.event_hash
        correction = replace(
            first,
            fact_id="fact-stack-correction",
            command_id="fact-command-stack-correction",
            event_id="fact-event-stack-correction",
            fact_kind=AuthorityFactKind.CORRECTION,
            corrected_fact_id=second.fact_id,
            corrected_event_hash=second_receipt.event_hash,
        )
        corrected = self.store.record_authority_fact(
            correction,
            self.authority.issue_authority_lifecycle_evidence(
                "proof-stack-correction", correction
            ),
            self.authority,
            expected_head=second_receipt.event_hash, writer_epoch=4,
        )
        connection = sqlite3.connect(self.database_path)
        try:
            effective = connection.execute(
                "SELECT originating_fact_id FROM effective_authority"
            ).fetchone()[0]
            fences = {
                row[0] for row in connection.execute(
                    "SELECT fence_id FROM dispatch_fences"
                )
            }
        finally:
            connection.close()
        self.assertEqual(effective, first.fact_id)
        self.assertEqual(fences, {f"authority:{first.fact_id}"})
        self.oracle.allowed_head = corrected.event_hash
        self.store.load_verified("repo-1")
        with self.assertRaisesRegex(DispatchDenied, "authority"):
            self.store.commit_intent(
                request, self.capability, self.authority,
                expected_head=corrected.event_hash, writer_epoch=5,
            )

    def test_t13_fact_write_is_atomic_replay_safe_and_tamper_evident(self) -> None:
        request = self.request()
        plan = self.store.accept_plan(
            PlanAcceptanceRequest(
                "plan-atomic", "plan-command-atomic", "plan-event-atomic",
                "repo-1", "run-1", "item-1", "effect-1", "revision-1",
                request.effect_descriptor_digest, "scope-1",
                request.budget_policy_digest, ("check-1",),
            ),
            expected_head="", writer_epoch=1,
        )
        self.oracle.allowed_head = plan.event_hash
        fact = AuthorityLifecycleFactRequest(
            "fact-atomic", "fact-command-atomic", "fact-event-atomic",
            "repo-1", "run-1", "item-1", "effect-1", "EFFECT",
            "grant-1", "EXECUTE_EFFECT", "scope-1",
            AuthorityFactKind.SOURCE_UNAVAILABLE, GovernedOrder.UNKNOWN,
            "NO_ACTION", None, None,
        )
        evidence = self.authority.issue_authority_lifecycle_evidence(
            "proof-atomic", fact
        )
        with self.assertRaises(InjectedFailure):
            self.store.record_authority_fact(
                fact, evidence, self.authority,
                expected_head=plan.event_hash, writer_epoch=2,
                failure_hook=raise_at("after_authority_fact_writes_before_commit"),
            )
        connection = sqlite3.connect(self.database_path)
        try:
            self.assertEqual(
                connection.execute(
                    "SELECT COUNT(*) FROM authority_facts"
                ).fetchone()[0],
                0,
            )
        finally:
            connection.close()
        recorded = self.store.record_authority_fact(
            fact, evidence, self.authority,
            expected_head=plan.event_hash, writer_epoch=2,
        )
        self.oracle.allowed_head = recorded.event_hash
        replay = self.store.record_authority_fact(
            fact, evidence, self.authority,
            expected_head=recorded.event_hash, writer_epoch=3,
        )
        self.assertTrue(replay.replayed)
        connection = sqlite3.connect(self.database_path)
        try:
            connection.execute(
                "UPDATE effective_authority SET generation = 99"
            )
            connection.commit()
        finally:
            connection.close()
        with self.assertRaisesRegex(StorageIntegrityError, "effective-authority"):
            self.store.load_verified("repo-1")

    def test_t13_lifecycle_decision_table(self) -> None:
        terminal = {
            LifecycleState.COMPLETED,
            LifecycleState.FAILED_FINAL,
            LifecycleState.STOPPED,
        }
        for state in LifecycleState:
            with self.subTest(state=state):
                expected = (
                    state
                    if state in terminal
                    or state in {
                        LifecycleState.PAUSED,
                        LifecycleState.PAUSING,
                        LifecycleState.RECONCILIATION_REQUIRED,
                    }
                    else LifecycleState.RECONCILIATION_REQUIRED
                    if state in {LifecycleState.RUNNING, LifecycleState.VALIDATING}
                    else LifecycleState.BLOCKED
                )
                self.assertEqual(
                    self.store._authority_fact_route(
                        state, AuthorityFactKind.REVOKED, GovernedOrder.BEFORE
                    ),
                    expected,
                )
                self.assertEqual(
                    self.store._authority_fact_route(
                        state, AuthorityFactKind.EXPIRED, GovernedOrder.AFTER
                    ),
                    state,
                )

    def test_t13_future_denial_is_rechecked_before_adapter_contact(self) -> None:
        request = self.request()
        intent = self._commit_planned_intent(
            request, self.capability, self.authority,
            expected_head="", writer_epoch=1,
        )
        self.oracle.allowed_head = intent.event_hash
        fact = AuthorityLifecycleFactRequest(
            "fact-contact", "fact-command-contact", "fact-event-contact",
            "repo-1", "run-1", "item-1", "effect-1", "EFFECT",
            "grant-1", "EXECUTE_EFFECT", "scope-1",
            AuthorityFactKind.REVOKED, GovernedOrder.AFTER, "INTENT",
            intent.event_id, intent.event_hash,
        )
        recorded = self.store.record_authority_fact(
            fact,
            self.authority.issue_authority_lifecycle_evidence(
                "proof-contact", fact
            ),
            self.authority,
            expected_head=intent.event_hash, writer_epoch=3,
        )
        self.oracle.allowed_head = recorded.event_hash
        with self.assertRaisesRegex(DispatchDenied, "authority"):
            self.store.claim_operation_launch(request, intent)

    def test_t13_operator_consumer_uses_grant_wide_effective_index(self) -> None:
        request = self.request()
        plan = self.store.accept_plan(
            PlanAcceptanceRequest(
                "plan-operator", "plan-command-operator",
                "plan-event-operator", "repo-1", "run-1", "item-1",
                "effect-1", "revision-1", request.effect_descriptor_digest,
                "scope-1", request.budget_policy_digest, ("check-1",),
            ),
            expected_head="", writer_epoch=1,
        )
        capability = self._pause_capability("t13")
        self.oracle.allowed_head = plan.event_hash
        fact = AuthorityLifecycleFactRequest(
            "fact-operator", "fact-command-operator", "fact-event-operator",
            "repo-1", "run-1", "item-1", "effect-1", "OPERATOR",
            capability.grant_id, "PAUSE", capability.scope_digest,
            AuthorityFactKind.REVOKED, GovernedOrder.BEFORE, "NO_ACTION",
            None, None,
        )
        recorded = self.store.record_authority_fact(
            fact,
            self.authority.issue_authority_lifecycle_evidence(
                "proof-operator", fact
            ),
            self.authority,
            expected_head=plan.event_hash, writer_epoch=2,
        )
        self.oracle.allowed_head = recorded.event_hash
        with self.assertRaisesRegex(DispatchDenied, "authority"):
            self.store.pause_before_dispatch(
                self._pause_request("t13"), capability, self.authority
            )

    def test_t13_unknown_operator_claim_binds_exact_operator_redemption(self) -> None:
        request = self.request()
        plan = self.store.accept_plan(
            PlanAcceptanceRequest(
                "plan-operator-unknown", "plan-command-operator-unknown",
                "plan-event-operator-unknown", "repo-1", "run-1", "item-1",
                "effect-1", "revision-1", request.effect_descriptor_digest,
                "scope-1", request.budget_policy_digest, ("check-1",),
            ),
            expected_head="", writer_epoch=1,
        )
        self.oracle.allowed_head = plan.event_hash
        capability = self._pause_capability("unknown")
        paused = self.store.pause_before_dispatch(
            self._pause_request("unknown"), capability, self.authority
        )
        self.oracle.allowed_head = paused.event_hash
        fact = AuthorityLifecycleFactRequest(
            "fact-operator-unknown", "fact-command-operator-unknown",
            "fact-event-operator-unknown", "repo-1", "run-1", "item-1",
            "effect-1", "OPERATOR", capability.grant_id, "PAUSE",
            capability.scope_digest, AuthorityFactKind.CLAIM_STATUS_UNKNOWN,
            GovernedOrder.UNKNOWN, "REDEMPTION", paused.event_id,
            paused.event_hash,
        )
        recorded = self.store.record_authority_fact(
            fact,
            self.authority.issue_authority_lifecycle_evidence(
                "proof-operator-unknown", fact
            ),
            self.authority,
            expected_head=paused.event_hash, writer_epoch=4,
        )
        self.assertEqual(recorded.resulting_state, LifecycleState.PAUSED)

    def test_t13_unknown_claim_rejects_cross_kind_grant_id_collision(self) -> None:
        request = self.request()
        plan = self.store.accept_plan(
            PlanAcceptanceRequest(
                "plan-collision", "plan-command-collision",
                "plan-event-collision", "repo-1", "run-1", "item-1",
                "effect-1", "revision-1", request.effect_descriptor_digest,
                "scope-1", request.budget_policy_digest, ("check-1",),
            ),
            expected_head="", writer_epoch=1,
        )
        self.oracle.allowed_head = plan.event_hash
        operator_grant = SyntheticOperatorGrant(
            "grant-1", "repo-1", "run-1", "PAUSE", "scope-1"
        )
        self.authority.register_operator(operator_grant)
        operator_capability = self.authority.claim_operator(
            *operator_grant.__dict__.values()
        )
        paused = self.store.pause_before_dispatch(
            self._pause_request("collision"), operator_capability, self.authority
        )
        self.oracle.allowed_head = paused.event_hash
        fact = AuthorityLifecycleFactRequest(
            "fact-collision", "fact-command-collision", "fact-event-collision",
            "repo-1", "run-1", "item-1", "effect-1", "EFFECT", "grant-1",
            "EXECUTE_EFFECT", "scope-1",
            AuthorityFactKind.CLAIM_STATUS_UNKNOWN, GovernedOrder.UNKNOWN,
            "REDEMPTION", paused.event_id, paused.event_hash,
        )
        with self.assertRaisesRegex(DispatchDenied, "local use"):
            self.store.record_authority_fact(
                fact,
                self.authority.issue_authority_lifecycle_evidence(
                    "proof-collision", fact
                ),
                self.authority,
                expected_head=paused.event_hash, writer_epoch=4,
            )

    def test_t13_unknown_validator_claim_binds_exact_validator_redemption(self) -> None:
        observation = self._record_effect_observation(check_ids=("check-1",))
        validator_request, capability = self._validator_intent(observation)
        intent = self.store.commit_validator_intent(
            validator_request, capability, self.authority
        )
        self.oracle.allowed_head = intent.event_hash
        fact = AuthorityLifecycleFactRequest(
            "fact-validator-unknown", "fact-command-validator-unknown",
            "fact-event-validator-unknown", "repo-1", "run-1", "item-1",
            "effect-1", "VALIDATOR", capability.grant_id, "RUN_VALIDATOR",
            capability.scope_digest, AuthorityFactKind.CLAIM_STATUS_UNKNOWN,
            GovernedOrder.UNKNOWN, "INTENT", intent.event_id,
            intent.event_hash,
        )
        recorded = self.store.record_authority_fact(
            fact,
            self.authority.issue_authority_lifecycle_evidence(
                "proof-validator-unknown", fact
            ),
            self.authority,
            expected_head=intent.event_hash, writer_epoch=6,
        )
        self.assertEqual(
            recorded.resulting_state, LifecycleState.RECONCILIATION_REQUIRED
        )

    def test_t13_own_validator_consumption_allows_exact_contact(self) -> None:
        observation = self._record_effect_observation(check_ids=("check-1",))
        validator_request, capability = self._validator_intent(observation)
        intent = self.store.commit_validator_intent(
            validator_request, capability, self.authority
        )
        self.oracle.allowed_head = intent.event_hash
        fact = AuthorityLifecycleFactRequest(
            "fact-validator-own", "fact-command-validator-own",
            "fact-event-validator-own", "repo-1", "run-1", "item-1",
            "effect-1", "VALIDATOR", capability.grant_id, "RUN_VALIDATOR",
            capability.scope_digest, AuthorityFactKind.OWN_CONSUMED,
            GovernedOrder.DURING, "INTENT", intent.event_id,
            intent.event_hash,
        )
        recorded = self.store.record_authority_fact(
            fact,
            self.authority.issue_authority_lifecycle_evidence(
                "proof-validator-own", fact
            ),
            self.authority,
            expected_head=intent.event_hash, writer_epoch=6,
        )
        self.oracle.allowed_head = recorded.event_hash
        self.store._contact_committed_validator(
            validator_request, capability, intent,
            self.store._adapter_target_digest("repo-1", "VALIDATOR"),
            self.authority,
        )
        connection = sqlite3.connect(self.database_path)
        try:
            contact_head = connection.execute(
                "SELECT catalog_head FROM repositories WHERE repository_id = 'repo-1'"
            ).fetchone()[0]
        finally:
            connection.close()
        self.oracle.allowed_head = contact_head
        self.store.load_verified("repo-1")

    def test_t13_supersession_rejects_cycles_and_never_revives_predecessor(
        self,
    ) -> None:
        request = self.request()
        successor = SyntheticGrant(
            "grant-successor", "repo-1", "effect-1", "attempt-1", "scope-1"
        )
        self.authority.register(successor)
        final_successor = SyntheticGrant(
            "grant-final", "repo-1", "effect-1", "attempt-1", "scope-1"
        )
        self.authority.register(final_successor)
        plan = self.store.accept_plan(
            PlanAcceptanceRequest(
                "plan-super", "plan-command-super", "plan-event-super",
                "repo-1", "run-1", "item-1", "effect-1", "revision-1",
                request.effect_descriptor_digest, "scope-1",
                request.budget_policy_digest, ("check-1",),
            ),
            expected_head="", writer_epoch=1,
        )
        self.oracle.allowed_head = plan.event_hash
        superseded = AuthorityLifecycleFactRequest(
            "fact-super", "fact-command-super", "fact-event-super",
            "repo-1", "run-1", "item-1", "effect-1", "EFFECT",
            "grant-1", "EXECUTE_EFFECT", "scope-1",
            AuthorityFactKind.SUPERSEDED, GovernedOrder.BEFORE, "NO_ACTION",
            None, None, successor_grant_id="grant-successor",
        )
        recorded = self.store.record_authority_fact(
            superseded,
            self.authority.issue_authority_lifecycle_evidence(
                "proof-super", superseded
            ),
            self.authority,
            expected_head=plan.event_hash, writer_epoch=2,
        )
        self.oracle.allowed_head = recorded.event_hash
        chain = replace(
            superseded,
            fact_id="fact-chain", command_id="fact-command-chain",
            event_id="fact-event-chain", grant_id="grant-successor",
            successor_grant_id="grant-final",
        )
        chained = self.store.record_authority_fact(
            chain,
            self.authority.issue_authority_lifecycle_evidence(
                "proof-chain", chain
            ),
            self.authority,
            expected_head=recorded.event_hash, writer_epoch=3,
        )
        self.oracle.allowed_head = chained.event_hash
        conflict = replace(
            superseded,
            fact_id="fact-conflict", command_id="fact-command-conflict",
            event_id="fact-event-conflict", successor_grant_id="grant-final",
        )
        with self.assertRaisesRegex(DispatchDenied, "conflicts"):
            self.store.record_authority_fact(
                conflict,
                self.authority.issue_authority_lifecycle_evidence(
                    "proof-conflict", conflict
                ),
                self.authority,
                expected_head=chained.event_hash, writer_epoch=4,
            )
        cycle = replace(
            superseded,
            fact_id="fact-cycle", command_id="fact-command-cycle",
            event_id="fact-event-cycle", grant_id="grant-final",
            successor_grant_id="grant-1",
        )
        with self.assertRaisesRegex(DispatchDenied, "cyclic"):
            self.store.record_authority_fact(
                cycle,
                self.authority.issue_authority_lifecycle_evidence(
                    "proof-cycle", cycle
                ),
                self.authority,
                expected_head=chained.event_hash, writer_epoch=4,
            )
        correction = replace(
            chain,
            fact_id="fact-chain-correction",
            command_id="fact-command-chain-correction",
            event_id="fact-event-chain-correction",
            fact_kind=AuthorityFactKind.CORRECTION,
            successor_grant_id=None,
            corrected_fact_id=chain.fact_id,
            corrected_event_hash=chained.event_hash,
        )
        corrected = self.store.record_authority_fact(
            correction,
            self.authority.issue_authority_lifecycle_evidence(
                "proof-chain-correction", correction
            ),
            self.authority,
            expected_head=chained.event_hash, writer_epoch=4,
        )
        connection = sqlite3.connect(self.database_path)
        try:
            self.assertEqual(
                connection.execute(
                    "SELECT status FROM effective_authority WHERE grant_id = 'grant-1'"
                ).fetchone()[0],
                "DENIED",
            )
            self.assertEqual(
                connection.execute(
                    "SELECT COUNT(*) FROM authority_supersessions"
                ).fetchone()[0],
                1,
            )
        finally:
            connection.close()
        self.oracle.allowed_head = corrected.event_hash
        self.store.load_verified("repo-1")

    def test_t13_supersession_graph_is_namespaced_by_full_typed_binding(self) -> None:
        request = self.request()
        self.authority.register(
            SyntheticGrant(
                "grant-successor", "repo-1", "effect-1", "attempt-1",
                "scope-1",
            )
        )
        for grant_id in ("grant-1", "grant-successor"):
            _, containment_digest = validator_containment("input-1", grant_id)
            self.authority.register_validator(
                SyntheticValidatorGrant(
                    grant_id, "repo-1", "effect-1", "revision-1", "check-1",
                    "input-1", "validator-attempt-1", "validator-scope-1",
                    containment_digest,
                )
            )
        plan = self.store.accept_plan(
            PlanAcceptanceRequest(
                "plan-typed", "plan-command-typed", "plan-event-typed",
                "repo-1", "run-1", "item-1", "effect-1", "revision-1",
                request.effect_descriptor_digest, "scope-1",
                request.budget_policy_digest, ("check-1",),
            ),
            expected_head="", writer_epoch=1,
        )
        self.oracle.allowed_head = plan.event_hash
        effect_fact = AuthorityLifecycleFactRequest(
            "fact-effect-typed", "fact-command-effect-typed",
            "fact-event-effect-typed", "repo-1", "run-1", "item-1",
            "effect-1", "EFFECT", "grant-1", "EXECUTE_EFFECT", "scope-1",
            AuthorityFactKind.SUPERSEDED, GovernedOrder.BEFORE, "NO_ACTION",
            None, None, successor_grant_id="grant-successor",
        )
        effect_recorded = self.store.record_authority_fact(
            effect_fact,
            self.authority.issue_authority_lifecycle_evidence(
                "proof-effect-typed", effect_fact
            ),
            self.authority,
            expected_head=plan.event_hash, writer_epoch=2,
        )
        self.oracle.allowed_head = effect_recorded.event_hash
        validator_fact = replace(
            effect_fact,
            fact_id="fact-validator-typed",
            command_id="fact-command-validator-typed",
            event_id="fact-event-validator-typed",
            grant_kind="VALIDATOR",
            action="RUN_VALIDATOR",
            scope_digest="validator-scope-1",
        )
        validator_recorded = self.store.record_authority_fact(
            validator_fact,
            self.authority.issue_authority_lifecycle_evidence(
                "proof-validator-typed", validator_fact
            ),
            self.authority,
            expected_head=effect_recorded.event_hash, writer_epoch=3,
        )
        connection = sqlite3.connect(self.database_path)
        try:
            self.assertEqual(
                connection.execute(
                    "SELECT COUNT(*) FROM authority_supersessions"
                ).fetchone()[0],
                2,
            )
        finally:
            connection.close()
        self.oracle.allowed_head = validator_recorded.event_hash
        self.store.load_verified("repo-1")

    def _stop_escalation_capability(self, suffix: str = "1"):
        grant = SyntheticOperatorGrant(
            f"escalation-grant-{suffix}", "repo-1", "run-1",
            "STOP_ESCALATE", f"escalation-scope-{suffix}",
        )
        self.authority.register_operator(grant)
        return self.authority.claim_operator(*grant.__dict__.values())

    @staticmethod
    def _stop_request(
        mode: StopMode = StopMode.IMMEDIATE, suffix: str = "1"
    ) -> StopRequest:
        return StopRequest(
            f"stop-{suffix}", f"stop-command-{suffix}",
            f"stop-event-{suffix}", "repo-1", "run-1", mode,
            "OPERATOR_STOP",
            "2030-01-01T00:00:00Z" if mode is StopMode.GRACEFUL else None,
        )

    def test_t19_immediate_stop_is_atomic_before_fence(self) -> None:
        plan = self.store.accept_plan(
            PlanAcceptanceRequest(
                "plan-1", "plan-command-1", "plan-event-1", "repo-1",
                "run-1", "item-1", "effect-1", "revision-1",
                "descriptor-digest", "scope-1", "budget-policy-digest",
                ("check-1",),
            ),
            expected_head="", writer_epoch=1,
        )
        self.oracle.allowed_head = plan.event_hash
        capability = self._stop_capability(StopMode.IMMEDIATE)
        request = self._stop_request()

        with self.assertRaises(InjectedFailure):
            self.store.stop(
                request, capability, self.authority,
                failure_hook=raise_at("after_stop_recorded_before_fence"),
            )
        counts = self.store.table_counts()
        self.assertEqual(counts["events"], 1)
        self.assertEqual(counts["stop_actions"], 0)
        self.assertEqual(counts["operator_redemptions"], 0)
        self.assertEqual(counts["dispatch_fences"], 0)
        self.assertEqual(
            self.store.load_run_lifecycle("run-1"), LifecycleState.PLANNED
        )

        with self.assertRaises(InjectedFailure):
            self.store.stop(
                request, capability, self.authority,
                failure_hook=raise_at(
                    "after_stop_commit_before_acknowledgement"
                ),
            )
        connection = sqlite3.connect(self.database_path)
        try:
            committed_hash = connection.execute(
                "SELECT event_hash FROM stop_actions WHERE stop_id = 'stop-1'"
            ).fetchone()[0]
        finally:
            connection.close()
        self.oracle.allowed_head = committed_hash
        replay = self.store.stop(request, capability, self.authority)
        self.assertEqual(replay.resulting_state, LifecycleState.STOPPED)
        self.assertEqual(self.store.table_counts()["stop_actions"], 1)
        self.assertEqual(self.store.table_counts()["dispatch_fences"], 1)
        self.assertTrue(replay.replayed)
        self.assertEqual(replay.event_hash, committed_hash)
        with self.assertRaisesRegex(StorageIntegrityError, "different payload"):
            self.store.stop(
                replace(request, reason_code="DIFFERENT_REASON"),
                capability,
                self.authority,
            )
        with self.assertRaises(DispatchDenied):
            self.store.stop(
                self._stop_request(StopMode.IMMEDIATE, "2"),
                self._stop_capability(StopMode.IMMEDIATE, "2"),
                self.authority,
            )
        self.store.load_verified("repo-1")

    def test_t19_alternate_identity_replay_authenticates_capability(self) -> None:
        plan = self.store.accept_plan(
            PlanAcceptanceRequest(
                "plan-1", "plan-command-1", "plan-event-1", "repo-1",
                "run-1", "item-1", "effect-1", "revision-1",
                "descriptor-digest", "scope-1", "budget-policy-digest",
                ("check-1",),
            ),
            expected_head="", writer_epoch=1,
        )
        self.oracle.allowed_head = plan.event_hash
        request = self._stop_request()
        capability = self._stop_capability(StopMode.IMMEDIATE)
        stopped = self.store.stop(request, capability, self.authority)
        self.oracle.allowed_head = stopped.event_hash

        forged = replace(capability, issuer_mac="forged-issuer-mac")
        with self.assertRaisesRegex(DispatchDenied, "was not issued here"):
            self.store.stop(
                replace(
                    request,
                    command_id="alternate-stop-command",
                    event_id="alternate-stop-event",
                ),
                forged,
                self.authority,
            )

    def test_t19_operator_issuer_and_grant_identity_survive_restart(self) -> None:
        plan = self.store.accept_plan(
            PlanAcceptanceRequest(
                "plan-1", "plan-command-1", "plan-event-1", "repo-1",
                "run-1", "item-1", "effect-1", "revision-1",
                "descriptor-digest", "scope-1", "budget-policy-digest",
                ("check-1",),
            ),
            expected_head="", writer_epoch=1,
        )
        self.oracle.allowed_head = plan.event_hash
        request = self._stop_request()
        stopped = self.store.stop(
            request,
            self._stop_capability(StopMode.IMMEDIATE),
            self.authority,
        )
        self.oracle.allowed_head = stopped.event_hash

        replacement = SyntheticAuthority(b"r" * 32)
        replay_grant = SyntheticOperatorGrant(
            "stop-grant-1", "repo-1", "run-1", "STOP_IMMEDIATE",
            "stop-scope-1",
        )
        replacement.register_operator(replay_grant)
        replay_capability = replacement.claim_operator(
            *replay_grant.__dict__.values()
        )
        with self.assertRaisesRegex(DispatchDenied, "issuer"):
            self.store.stop(request, replay_capability, replacement)

        plan_2 = self.store.accept_plan(
            PlanAcceptanceRequest(
                "plan-2", "plan-command-2", "plan-event-2", "repo-1",
                "run-2", "item-2", "effect-2", "revision-2",
                "descriptor-digest", "operator-scope-2",
                "budget-policy-digest", ("check-2",),
            ),
            expected_head=stopped.event_hash, writer_epoch=3,
        )
        self.oracle.allowed_head = plan_2.event_hash
        rebound = SyntheticAuthority(b"b" * 32)
        rebound_grant = SyntheticOperatorGrant(
            "stop-grant-1", "repo-1", "run-2", "STOP_IMMEDIATE",
            "stop-scope-2",
        )
        rebound.register_operator(rebound_grant)
        rebound_capability = rebound.claim_operator(
            *rebound_grant.__dict__.values()
        )
        with self.assertRaisesRegex(DispatchDenied, "grant was already redeemed"):
            self.store.stop(
                replace(
                    self._stop_request(StopMode.IMMEDIATE, "2"),
                    run_id="run-2",
                ),
                rebound_capability,
                rebound,
            )

    def test_t19_legacy_stop_event_has_typed_compatibility_rejection(
        self,
    ) -> None:
        plan = self.store.accept_plan(
            PlanAcceptanceRequest(
                "plan-1", "plan-command-1", "plan-event-1", "repo-1",
                "run-1", "item-1", "effect-1", "revision-1",
                "descriptor-digest", "scope-1", "budget-policy-digest",
                ("check-1",),
            ),
            expected_head="", writer_epoch=1,
        )
        self.oracle.allowed_head = plan.event_hash
        stopped = self.store.stop(
            self._stop_request(),
            self._stop_capability(StopMode.IMMEDIATE),
            self.authority,
        )
        connection = sqlite3.connect(self.database_path)
        connection.row_factory = sqlite3.Row
        try:
            row = connection.execute(
                "SELECT body_json FROM stop_actions WHERE stop_id = 'stop-1'"
            ).fetchone()
            body = json.loads(row["body_json"])
            del body["mode"]
            legacy_hash = self.store._event_hash(body)
            body_json = json.dumps(
                body, sort_keys=True, separators=(",", ":")
            )
            connection.execute(
                "UPDATE events SET event_hash = ?, body_json = ? WHERE "
                "event_id = 'stop-event-1'",
                (legacy_hash, body_json),
            )
            connection.execute(
                "UPDATE stop_actions SET event_hash = ?, body_json = ? WHERE "
                "stop_id = 'stop-1'",
                (legacy_hash, body_json),
            )
            connection.execute(
                "UPDATE command_outcomes SET event_hash = ? WHERE "
                "command_id = 'stop-command-1'",
                (legacy_hash,),
            )
            connection.execute(
                "UPDATE runs SET head_hash = ? WHERE run_id = 'run-1'",
                (legacy_hash,),
            )
            connection.execute(
                "UPDATE repositories SET catalog_head = ? WHERE "
                "repository_id = 'repo-1'",
                (legacy_hash,),
            )
            connection.commit()
        finally:
            connection.close()
        self.oracle.allowed_head = legacy_hash

        with self.assertRaisesRegex(
            StorageIntegrityError, "unsupported STOP_RECORDED event schema"
        ):
            self.store.load_verified("repo-1")

    def test_t19_stop_event_decoder_rejects_extensions_and_mode_mismatch(
        self,
    ) -> None:
        plan = self.store.accept_plan(
            PlanAcceptanceRequest(
                "plan-1", "plan-command-1", "plan-event-1", "repo-1",
                "run-1", "item-1", "effect-1", "revision-1",
                "descriptor-digest", "scope-1", "budget-policy-digest",
                ("check-1",),
            ),
            expected_head="", writer_epoch=1,
        )
        self.oracle.allowed_head = plan.event_hash
        stopped = self.store.stop(
            self._stop_request(),
            self._stop_capability(StopMode.IMMEDIATE),
            self.authority,
        )
        self.oracle.allowed_head = stopped.event_hash
        connection = sqlite3.connect(self.database_path)
        connection.row_factory = sqlite3.Row
        try:
            body = json.loads(
                connection.execute(
                    "SELECT body_json FROM stop_actions WHERE stop_id = 'stop-1'"
                ).fetchone()["body_json"]
            )
        finally:
            connection.close()

        with self.assertRaisesRegex(
            StorageIntegrityError, "unsupported STOP_RECORDED event schema"
        ):
            self.store._validate_stop_event_body(body | {"extension": True})
        with self.assertRaisesRegex(
            StorageIntegrityError, "STOP_RECORDED event semantics are invalid"
        ):
            self.store._validate_stop_event_body(
                body | {"action": "STOP_GRACEFUL"}
            )
        with self.assertRaisesRegex(
            StorageIntegrityError, "STOP_RECORDED event semantics are invalid"
        ):
            self.store._validate_stop_event_body(body | {"sequence": "2"})

    def test_t19_recovery_rejects_forged_stop_predecessor_state_and_cursor(
        self,
    ) -> None:
        plan = self.store.accept_plan(
            PlanAcceptanceRequest(
                "plan-1", "plan-command-1", "plan-event-1", "repo-1",
                "run-1", "item-1", "effect-1", "revision-1",
                "descriptor-digest", "scope-1", "budget-policy-digest",
                ("check-1",),
            ),
            expected_head="", writer_epoch=1,
        )
        self.oracle.allowed_head = plan.event_hash
        committed = self.store.commit_intent(
            self.request(), self.capability, self.authority,
            expected_head=plan.event_hash, writer_epoch=2,
        )
        self.oracle.allowed_head = committed.event_hash
        stopped = self._stop_run()

        for suffix, changes in (
            ("state", {"lifecycle_from": LifecycleState.PLANNED.value}),
            ("cursor", {"retained_continuation_cursor": "forged-cursor"}),
        ):
            tampered_path = self.database_path.with_name(
                f"tampered-stop-{suffix}.sqlite3"
            )
            shutil.copy2(self.database_path, tampered_path)
            connection = sqlite3.connect(tampered_path)
            connection.row_factory = sqlite3.Row
            try:
                body = json.loads(
                    connection.execute(
                        "SELECT body_json FROM stop_actions WHERE stop_id = 'stop-1'"
                    ).fetchone()["body_json"]
                ) | changes
                event_hash = self.store._event_hash(body)
                body_json = json.dumps(
                    body, sort_keys=True, separators=(",", ":")
                )
                connection.execute(
                    "UPDATE events SET event_hash = ?, body_json = ? WHERE "
                    "event_id = 'stop-event-1'",
                    (event_hash, body_json),
                )
                connection.execute(
                    "UPDATE stop_actions SET retained_continuation_cursor = ?, "
                    "event_hash = ?, body_json = ? WHERE stop_id = 'stop-1'",
                    (
                        body["retained_continuation_cursor"], event_hash,
                        body_json,
                    ),
                )
                connection.execute(
                    "UPDATE command_outcomes SET event_hash = ? WHERE "
                    "command_id = 'stop-command-1'",
                    (event_hash,),
                )
                connection.execute(
                    "UPDATE runs SET head_hash = ? WHERE run_id = 'run-1'",
                    (event_hash,),
                )
                connection.execute(
                    "UPDATE repositories SET catalog_head = ? WHERE "
                    "repository_id = 'repo-1'",
                    (event_hash,),
                )
                connection.commit()
            finally:
                connection.close()
            oracle = MutableFreshnessOracle()
            oracle.allowed_head = event_hash
            with self.subTest(suffix=suffix), self.assertRaisesRegex(
                StorageIntegrityError, "(event lifecycle|stop predecessor)"
            ):
                SQLiteStateStore(
                    tampered_path, oracle, "repo-1"
                ).load_verified("repo-1")

    def test_t19_recovery_rejects_stop_fence_retargeted_from_plan(self) -> None:
        plan = self.store.accept_plan(
            PlanAcceptanceRequest(
                "plan-1", "plan-command-1", "plan-event-1", "repo-1",
                "run-1", "item-1", "effect-1", "revision-1",
                "descriptor-digest", "scope-1", "budget-policy-digest",
                ("check-1",),
            ),
            expected_head="", writer_epoch=1,
        )
        self.oracle.allowed_head = plan.event_hash
        stopped = self._stop_run()
        connection = sqlite3.connect(self.database_path)
        connection.row_factory = sqlite3.Row
        try:
            body = json.loads(
                connection.execute(
                    "SELECT body_json FROM stop_actions WHERE stop_id = 'stop-1'"
                ).fetchone()["body_json"]
            )
            body["item_id"] = "forged-item"
            body["logical_effect_id"] = "forged-effect"
            event_hash = self.store._event_hash(body)
            body_json = json.dumps(
                body, sort_keys=True, separators=(",", ":")
            )
            connection.execute(
                "UPDATE events SET item_id = 'forged-item', event_hash = ?, "
                "body_json = ? WHERE event_id = 'stop-event-1'",
                (event_hash, body_json),
            )
            connection.execute(
                "UPDATE stop_actions SET item_id = 'forged-item', "
                "logical_effect_id = 'forged-effect', event_hash = ?, "
                "body_json = ? WHERE stop_id = 'stop-1'",
                (event_hash, body_json),
            )
            connection.execute(
                "UPDATE dispatch_fences SET item_id = 'forged-item', "
                "logical_effect_id = 'forged-effect' WHERE fence_id = ?",
                (body["fence_id"],),
            )
            connection.execute(
                "UPDATE command_outcomes SET event_hash = ? WHERE "
                "command_id = 'stop-command-1'",
                (event_hash,),
            )
            connection.execute(
                "UPDATE runs SET head_hash = ? WHERE run_id = 'run-1'",
                (event_hash,),
            )
            connection.execute(
                "UPDATE repositories SET catalog_head = ? WHERE "
                "repository_id = 'repo-1'",
                (event_hash,),
            )
            connection.commit()
        finally:
            connection.close()
        self.oracle.allowed_head = event_hash

        with self.assertRaisesRegex(
            StorageIntegrityError, "stop plan binding"
        ):
            self.store.load_verified("repo-1")

    def test_t18_graceful_stop_persists_deadline_and_rejects_mode_mismatch(
        self,
    ) -> None:
        plan = self.store.accept_plan(
            PlanAcceptanceRequest(
                "plan-1", "plan-command-1", "plan-event-1", "repo-1",
                "run-1", "item-1", "effect-1", "revision-1",
                "descriptor-digest", "scope-1", "budget-policy-digest",
                ("check-1",),
            ),
            expected_head="", writer_epoch=1,
        )
        self.oracle.allowed_head = plan.event_hash
        request = self._stop_request(StopMode.GRACEFUL)
        stopped = self.store.stop(
            request,
            self._stop_capability(StopMode.GRACEFUL),
            self.authority,
        )
        self.oracle.allowed_head = stopped.event_hash
        connection = sqlite3.connect(self.database_path)
        try:
            persisted = connection.execute(
                "SELECT mode, drain_deadline_utc FROM stop_actions "
                "WHERE stop_id = 'stop-1'"
            ).fetchone()
        finally:
            connection.close()
        self.assertEqual(persisted, ("GRACEFUL", "2030-01-01T00:00:00Z"))
        with self.assertRaisesRegex(ValueError, "cannot carry"):
            replace(
                self._stop_request(StopMode.IMMEDIATE, "2"),
                drain_deadline_utc="2030-01-01T00:00:00Z",
            ).validate()
        with self.assertRaisesRegex(ValueError, "requires"):
            replace(request, drain_deadline_utc=None).validate()
        self.store.load_verified("repo-1")

    def test_t19_active_stop_retains_slot_and_admits_late_receipt(self) -> None:
        committed = self._commit_planned_intent(
            self.request(), self.capability, self.authority,
            expected_head="", writer_epoch=1,
        )
        self.oracle.allowed_head = committed.event_hash
        stopped = self.store.stop(
            self._stop_request(),
            self._stop_capability(StopMode.IMMEDIATE),
            self.authority,
        )
        self.oracle.allowed_head = stopped.event_hash
        with self.assertRaisesRegex(DispatchDenied, "requires RUNNING"):
            self.store.claim_operation_launch(self.request(), committed)
        self.assertEqual(self.store.table_counts()["operation_launches"], 0)
        self.assertEqual(self.store.table_counts()["outstanding_slot"], 1)
        connection = sqlite3.connect(self.database_path)
        try:
            reservation_before = connection.execute(
                "SELECT held_units, charged_units, uncertainty, disposition "
                "FROM budget_reservations WHERE reservation_id = 'reservation-1'"
            ).fetchone()
        finally:
            connection.close()
        self.assertEqual(reservation_before, (3, 0, 0, "RESERVED"))

        late = self._record_signed_effect_observation(
            EffectObservationRequest(
                "late-observation-1", "late-observe-command-1",
                "late-observation-event-1", "repo-1", "run-1", "item-1",
                "effect-1", "attempt-1", "late-receipt-1",
                self.capability.claim_id, "descriptor-digest", 2,
                "late-settlement-1", "",
            )
        )
        self.oracle.allowed_head = late.event_hash
        self.assertEqual(late.resulting_state, LifecycleState.STOPPED)
        self.assertEqual(self.store.table_counts()["outstanding_slot"], 1)
        connection = sqlite3.connect(self.database_path)
        try:
            event_kind = connection.execute(
                "SELECT event_kind FROM events WHERE event_id = ?",
                (late.event_id,),
            ).fetchone()[0]
            reservation_after = connection.execute(
                "SELECT held_units, charged_units, uncertainty, disposition "
                "FROM budget_reservations WHERE reservation_id = 'reservation-1'"
            ).fetchone()
        finally:
            connection.close()
        self.assertEqual(event_kind, "LATE_RECEIPT_RECORDED")
        self.assertEqual(reservation_after, (0, 2, 0, "CONSUMED"))
        self.store.load_verified("repo-1")

    def test_t23_late_receipt_from_validating_preserves_evidence(self) -> None:
        self._record_effect_observation(check_ids=("check-1",))
        late = self._record_signed_effect_observation(
            EffectObservationRequest(
                "observation-2", "observe-command-2", "observation-event-2",
                "repo-1", "run-1", "item-1", "effect-1", "attempt-1",
                "receipt-2", self.capability.claim_id, "descriptor-digest",
                3, "settlement-event-2", "",
            )
        )
        self.oracle.allowed_head = late.event_hash
        connection = sqlite3.connect(self.database_path)
        try:
            event_kind = connection.execute(
                "SELECT event_kind FROM events WHERE event_id = ?",
                (late.event_id,),
            ).fetchone()[0]
            accounting = connection.execute(
                "SELECT charged_units, disposition FROM budget_reservations "
                "WHERE reservation_id = 'reservation-1'"
            ).fetchone()
        finally:
            connection.close()
        self.assertEqual(event_kind, "LATE_RECEIPT_RECORDED")
        self.assertEqual(
            late.resulting_state, LifecycleState.RECONCILIATION_REQUIRED
        )
        self.assertEqual(accounting, (3, "ADJUSTED"))
        self.assertEqual(self.store.table_counts()["outstanding_slot"], 1)
        self.store.load_verified("repo-1")

    def test_t23_terminal_receipt_preserves_completed_and_released_slot(
        self,
    ) -> None:
        request, attestation = self._prepare_finalization()
        finalized = self.store._finalize_operation(
            request, attestation, self.authority
        )
        self.oracle.allowed_head = finalized.event_hash
        late = self._record_signed_effect_observation(
            EffectObservationRequest(
                "observation-2", "observe-command-2", "observation-event-2",
                "repo-1", "run-1", "item-1", "effect-1", "attempt-1",
                "receipt-2", self.capability.claim_id, "descriptor-digest",
                3, "settlement-event-2", "",
            )
        )
        self.oracle.allowed_head = late.event_hash
        connection = sqlite3.connect(self.database_path)
        try:
            event_kind = connection.execute(
                "SELECT event_kind FROM events WHERE event_id = ?",
                (late.event_id,),
            ).fetchone()[0]
        finally:
            connection.close()
        self.assertEqual(event_kind, "LATE_RECEIPT_RECORDED")
        self.assertEqual(late.resulting_state, LifecycleState.COMPLETED)
        self.assertEqual(self.store.table_counts()["outstanding_slot"], 0)
        self.store.load_verified("repo-1")

    def test_t19_t23_before_t26_keeps_stop_fence_target_scoped(self) -> None:
        committed = self._commit_planned_intent(
            self.request(), self.capability, self.authority,
            expected_head="", writer_epoch=1,
        )
        self.oracle.allowed_head = committed.event_hash
        self._stop_run()
        late = self._record_signed_effect_observation(
            EffectObservationRequest(
                "late-observation-1", "late-observe-command-1",
                "late-observation-event-1", "repo-1", "run-1", "item-1",
                "effect-1", "attempt-1", "late-receipt-1",
                self.capability.claim_id, "descriptor-digest", 2,
                "late-settlement-1", "",
            )
        )
        self.oracle.allowed_head = late.event_hash
        connection = sqlite3.connect(self.database_path)
        try:
            event_kind, plan_id, plan_hash = connection.execute(
                "SELECT event_kind, (SELECT plan_id FROM validation_plans "
                "WHERE run_id = 'run-1'), (SELECT event_hash FROM "
                "validation_plans WHERE run_id = 'run-1') FROM events "
                "WHERE event_id = ?",
                (late.event_id,),
            ).fetchone()
        finally:
            connection.close()
        self.assertEqual(event_kind, "LATE_RECEIPT_RECORDED")
        settled = self.store.settle_terminal_validation(
            TerminalValidationSettlementRequest(
                "terminal-settlement-1", "terminal-command-1",
                "terminal-event-1", "repo-1", "run-1", "item-1",
                "effect-1", plan_id, "revision-1", "check-1", "PLAN",
                plan_id, plan_hash, "CANCELLED_WITHOUT_START",
            )
        )
        self.oracle.allowed_head = settled.event_hash
        self.assertTrue(settled.slot_released)

        def prepare_intent(
            suffix: str, item_id: str, logical_effect_id: str
        ):
            grant = SyntheticGrant(
                f"grant-{suffix}", "repo-1", logical_effect_id,
                f"attempt-{suffix}", f"scope-{suffix}",
            )
            self.authority.register(grant)
            capability = self.authority.claim(*grant.__dict__.values())
            plan = self.store.accept_plan(
                PlanAcceptanceRequest(
                    f"plan-{suffix}", f"plan-command-{suffix}",
                    f"plan-event-{suffix}", "repo-1", f"run-{suffix}",
                    item_id, logical_effect_id, f"revision-{suffix}",
                    "descriptor-digest", grant.scope_digest,
                    "budget-policy-digest", (f"check-{suffix}",),
                ),
                expected_head=self.oracle.allowed_head,
                writer_epoch=20 + int(suffix),
            )
            self.oracle.allowed_head = plan.event_hash
            request = replace(
                self.request(), run_id=f"run-{suffix}", item_id=item_id,
                command_id=f"command-{suffix}", event_id=f"event-{suffix}",
                logical_effect_id=logical_effect_id,
                attempt_id=f"attempt-{suffix}",
                permission_use_id=f"permission-use-{suffix}",
                reservation_id=f"reservation-{suffix}",
            )
            return request, capability, plan

        for suffix, item_id, logical_effect_id in (
            ("2", "item-1", "effect-2"),
            ("3", "item-3", "effect-1"),
        ):
            with self.subTest(
                item_id=item_id, logical_effect_id=logical_effect_id
            ):
                request, capability, plan = prepare_intent(
                    suffix, item_id, logical_effect_id
                )
                with self.assertRaisesRegex(
                    DispatchDenied, "active dispatch fence"
                ):
                    self.store.commit_intent(
                        request, capability, self.authority,
                        expected_head=plan.event_hash,
                        writer_epoch=30 + int(suffix),
                    )

        request, capability, plan = prepare_intent("4", "item-4", "effect-4")
        committed = self.store.commit_intent(
            request, capability, self.authority,
            expected_head=plan.event_hash, writer_epoch=34,
        )
        self.oracle.allowed_head = committed.event_hash
        self.assertFalse(committed.replayed)
        self.assertEqual(
            self.store.load_run_lifecycle("run-4"), LifecycleState.RUNNING
        )
        self.store.load_verified("repo-1")

    def test_t19_stop_blocks_new_validator_launch_and_tamper_fails_recovery(
        self,
    ) -> None:
        parent = self._record_effect_observation(check_ids=("check-1",))
        intent, validator_capability = self._validator_intent(parent)
        stopped = self.store.stop(
            self._stop_request(),
            self._stop_capability(StopMode.IMMEDIATE),
            self.authority,
        )
        self.oracle.allowed_head = stopped.event_hash
        with self.assertRaisesRegex(DispatchDenied, "durable VALIDATING"):
            self.store.commit_validator_intent(
                intent, validator_capability, self.authority
            )
        self.assertEqual(self.store.table_counts()["validator_intents"], 0)

        connection = sqlite3.connect(self.database_path)
        try:
            connection.execute(
                "UPDATE stop_actions SET reason_code = 'TAMPERED' "
                "WHERE stop_id = 'stop-1'"
            )
            connection.commit()
        finally:
            connection.close()
        with self.assertRaisesRegex(StorageIntegrityError, "stop-action"):
            self.store.load_verified("repo-1")

    def test_t04_pause_is_atomic_and_dual_events_are_hash_chained(self) -> None:
        plan = self.store.accept_plan(
            PlanAcceptanceRequest(
                "plan-1", "plan-command-1", "plan-event-1", "repo-1",
                "run-1", "item-1", "effect-1", "revision-1",
                "descriptor-digest", "scope-1", "budget-policy-digest",
                ("check-1",),
            ),
            expected_head="", writer_epoch=1,
        )
        self.oracle.allowed_head = plan.event_hash
        capability = self._pause_capability()
        request = self._pause_request()
        with self.assertRaises(InjectedFailure):
            self.store.pause_before_dispatch(
                request, capability, self.authority,
                failure_hook=raise_at("after_pause_requested_before_settled"),
            )
        counts = self.store.table_counts()
        self.assertEqual(counts["events"], 1)
        self.assertEqual(counts["control_actions"], 0)
        self.assertEqual(counts["operator_redemptions"], 0)
        self.assertEqual(counts["dispatch_fences"], 0)
        self.assertEqual(self.store.load_run_lifecycle("run-1").value, "PLANNED")

        receipt = self.store.pause_before_dispatch(
            request, capability, self.authority
        )
        self.oracle.allowed_head = receipt.event_hash
        self.assertEqual(receipt.resulting_state.value, "PAUSED")
        connection = sqlite3.connect(self.database_path)
        connection.row_factory = sqlite3.Row
        try:
            rows = connection.execute(
                "SELECT event_id, event_kind, previous_event_hash, event_hash "
                "FROM events WHERE command_id = ? ORDER BY sequence",
                (request.command_id,),
            ).fetchall()
        finally:
            connection.close()
        self.assertEqual(
            [row["event_kind"] for row in rows],
            ["PAUSE_REQUESTED", "PAUSE_SETTLED"],
        )
        self.assertEqual(rows[1]["previous_event_hash"], rows[0]["event_hash"])
        self.store.load_verified("repo-1")

    def test_t04_acknowledgement_loss_replays_and_capability_cannot_rebind(self) -> None:
        plan = self.store.accept_plan(
            PlanAcceptanceRequest(
                "plan-1", "plan-command-1", "plan-event-1", "repo-1",
                "run-1", "item-1", "effect-1", "revision-1",
                "descriptor-digest", "scope-1", "budget-policy-digest",
                ("check-1",),
            ),
            expected_head="", writer_epoch=1,
        )
        self.oracle.allowed_head = plan.event_hash
        capability = self._pause_capability()
        request = self._pause_request()
        with self.assertRaises(InjectedFailure):
            self.store.pause_before_dispatch(
                request, capability, self.authority,
                failure_hook=raise_at("after_pause_commit_before_acknowledgement"),
            )
        connection = sqlite3.connect(self.database_path)
        try:
            committed_hash = connection.execute(
                "SELECT event_hash FROM control_actions WHERE control_id = ?",
                (request.pause_id,),
            ).fetchone()[0]
        finally:
            connection.close()
        self.oracle.allowed_head = committed_hash
        replay = self.store.pause_before_dispatch(
            request, capability, self.authority
        )
        self.assertTrue(replay.replayed)
        self.assertEqual(replay.event_hash, committed_hash)
        with self.assertRaisesRegex(DispatchDenied, "already redeemed"):
            self.store.pause_before_dispatch(
                self._pause_request("2"), capability, self.authority
            )

    def test_t04_recovery_rejects_tampered_pause_fence(self) -> None:
        plan = self.store.accept_plan(
            PlanAcceptanceRequest(
                "plan-1", "plan-command-1", "plan-event-1", "repo-1",
                "run-1", "item-1", "effect-1", "revision-1",
                "descriptor-digest", "scope-1", "budget-policy-digest",
                ("check-1",),
            ),
            expected_head="", writer_epoch=1,
        )
        self.oracle.allowed_head = plan.event_hash
        receipt = self.store.pause_before_dispatch(
            self._pause_request(), self._pause_capability(), self.authority
        )
        self.oracle.allowed_head = receipt.event_hash
        connection = sqlite3.connect(self.database_path)
        try:
            connection.execute(
                "UPDATE dispatch_fences SET reason_code = 'TAMPERED' "
                "WHERE fence_id = 'pause-fence-1'"
            )
            connection.commit()
        finally:
            connection.close()
        with self.assertRaisesRegex(StorageIntegrityError, "dispatch-fence"):
            self.store.load_verified("repo-1")

    def _validator_intent(
        self,
        observation,
        *,
        suffix: str = "1",
        check_id: str | None = None,
        validator_attempt_id: str | None = None,
        recovery_id: str | None = None,
        cap_units: int = 10,
    ):
        check_id = check_id or f"check-{suffix}"
        validator_attempt_id = validator_attempt_id or f"validator-attempt-{suffix}"
        containment_json, containment_digest = validator_containment(
            "input-1", suffix
        )
        grant = SyntheticValidatorGrant(
            f"validator-grant-{suffix}",
            "repo-1",
            "effect-1",
            "revision-1",
            check_id,
            "input-1",
            validator_attempt_id,
            f"read-only-scope-{suffix}",
            containment_digest,
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
            check_id,
            "input-1",
            validator_attempt_id,
            f"validator-permission-{suffix}",
            f"validator-reservation-{suffix}",
            "validator-budget-policy-1",
            1,
            2,
            cap_units,
            recovery_id,
            containment_json,
        )
        return request, capability

    def _prepared_validator_execution(self):
        observation = self._record_effect_observation(check_ids=("check-1",))
        intent, capability = self._validator_intent(observation)
        committed = self.store.commit_validator_intent(
            intent, capability, self.authority
        )
        self.oracle.allowed_head = committed.event_hash
        validator_path = self.database_path.parent / "synthetic-validator.sqlite3"
        adapter = SyntheticValidatorAdapter(validator_path)
        adapter._canonical_repository_id = "repo-1"
        adapter._canonical_ledger_path = validator_path.resolve()
        spec = parse_validator_containment_spec(intent.containment_spec_json)
        request = SyntheticValidatorRequest(
            "repo-1", "effect-1", "revision-1", "check-1", "input-1",
            "validator-attempt-1", "read-only-scope-1", "result-digest-1",
            "PASS", capability.containment_digest, spec.allowed_actions,
            spec.input_root, f"{spec.output_root}/result.json",
            f"{spec.scratch_root}/work",
            synthetic_validator_output_size("result-digest-1", "PASS"),
        )
        return intent, capability, committed, adapter, request

    def _record_validator_result(
        self,
        *,
        verdict: str = "PASS",
        only_check: bool = False,
        aggregate_gate_ids=None,
    ):
        check_ids = ("check-1",) if only_check else ("check-1", "check-2")
        observation = self._record_effect_observation(
            check_ids, aggregate_gate_ids
        )
        return self._record_validator_result_for(
            observation, suffix="1", verdict=verdict
        )

    def _record_validator_result_for(
        self, observation, *, suffix: str, verdict: str = "PASS"
    ):
        intent_request, capability = self._validator_intent(
            observation, suffix=suffix
        )
        intent = self.store.commit_validator_intent(
            intent_request, capability, self.authority
        )
        self.oracle.allowed_head = intent.event_hash
        settlement_request = BudgetSettlementRequest(
            f"validator-settlement-{suffix}",
            f"validator-reservation-{suffix}", "",
            BudgetDisposition.CONSUMED, 1,
            f"validator-result-{suffix}",
            "VALIDATOR_USAGE_REPORTED",
        )
        settlement = self.store._settle_budget(
            settlement_request,
            self.authority.issue_settlement_proof(
                f"validator-proof-{suffix}",
                settlement_request,
            ),
            self.authority,
        )
        self.oracle.allowed_head = settlement.settlement_hash
        self._record_validator_cessation_for(
            suffix=suffix, result_available=True, verdict=verdict
        )
        recorded = self.store._record_validator_observation(
            ValidatorObservationRequest(
                f"validator-observation-{suffix}",
                f"validator-observe-command-{suffix}",
                f"validator-observation-event-{suffix}",
                "repo-1", "run-1", "item-1", "effect-1",
                f"validator-intent-{suffix}", f"validator-attempt-{suffix}",
                f"validator-result-{suffix}", capability.claim_id,
                "revision-1", f"check-{suffix}", "input-1",
                f"result-digest-{suffix}", verdict, 1,
                f"validator-settlement-{suffix}", settlement.settlement_hash,
            )
        )
        self.oracle.allowed_head = recorded.event_hash
        return recorded

    def _record_validator_cessation_for(
        self, *, suffix: str = "1", result_available: bool = False,
        verdict: str = "PASS", check_id: str | None = None,
    ):
        check_id = check_id or f"check-{suffix}"
        connection = sqlite3.connect(self.database_path)
        connection.row_factory = sqlite3.Row
        try:
            intent = connection.execute(
                "SELECT * FROM validator_intents WHERE validator_intent_id = ?",
                (f"validator-intent-{suffix}",),
            ).fetchone()
        finally:
            connection.close()
        assert intent is not None
        validator_path = self.database_path.parent / "synthetic-validator.sqlite3"
        adapter = SyntheticValidatorAdapter(validator_path)
        adapter._canonical_repository_id = "repo-1"
        adapter._canonical_ledger_path = validator_path.resolve()
        if result_available:
            connection = sqlite3.connect(validator_path)
            try:
                connection.execute(
                    "INSERT OR IGNORE INTO synthetic_validator_results VALUES "
                    "(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 1, 1, ?)",
                    (
                        intent["capability_claim_id"],
                        f"validator-result-{suffix}", "repo-1", "effect-1",
                        "revision-1", check_id, "input-1",
                        f"validator-attempt-{suffix}",
                        f"result-digest-{suffix}", verdict, 1,
                        intent["containment_digest"],
                    ),
                )
                connection.commit()
            finally:
                connection.close()
        attestation = self.authority.issue_validator_cessation_attestation(
            f"cessation-attestation-{suffix}", f"cessation-{suffix}",
            adapter._target_digest("repo-1"), intent["capability_claim_id"],
            f"VALIDATOR:validator-intent-{suffix}", intent["event_hash"],
            "repo-1", "run-1", "item-1", "effect-1", "revision-1",
            check_id, f"validator-attempt-{suffix}",
        )
        seal = adapter.seal_cessation(attestation, self.authority)
        receipt = self.store.record_validator_cessation(
            ValidatorCessationRequest(
                f"cessation-{suffix}", f"cessation-command-{suffix}",
                f"cessation-event-{suffix}", "repo-1", "run-1", "item-1",
                "effect-1", f"validator-intent-{suffix}",
                f"validator-attempt-{suffix}", "revision-1",
                check_id, seal.cessation_hash,
            ),
            self.authority,
        )
        connection = sqlite3.connect(self.database_path)
        try:
            self.oracle.allowed_head = connection.execute(
                "SELECT head_hash FROM runs WHERE run_id = 'run-1'"
            ).fetchone()[0]
        finally:
            connection.close()
        return receipt

    def _stop_run(self) -> str:
        receipt = self.store.stop(
            self._stop_request(),
            self._stop_capability(StopMode.IMMEDIATE),
            self.authority,
        )
        self.oracle.allowed_head = receipt.event_hash
        return receipt.event_hash

    def test_unknown_validator_usage_cannot_be_released_after_result(self) -> None:
        observation = self._record_effect_observation(check_ids=("check-1",))
        intent_request, capability = self._validator_intent(observation)
        intent = self.store.commit_validator_intent(
            intent_request, capability, self.authority
        )
        self.oracle.allowed_head = intent.event_hash
        unknown = BudgetSettlementRequest(
            "validator-settlement-1", "validator-reservation-1", "",
            BudgetDisposition.UNKNOWN_WORST_CASE_CHARGED, None,
            "validator-result-1", "VALIDATOR_USAGE_UNKNOWN",
        )
        settlement = self.store._settle_budget(
            unknown,
            self.authority.issue_settlement_proof("validator-proof-1", unknown),
            self.authority,
        )
        self.oracle.allowed_head = settlement.settlement_hash
        recorded = self.store._record_validator_observation(
            ValidatorObservationRequest(
                "validator-observation-1", "validator-observe-command-1",
                "validator-observation-event-1", "repo-1", "run-1", "item-1",
                "effect-1", "validator-intent-1", "validator-attempt-1",
                "validator-result-1", capability.claim_id, "revision-1",
                "check-1", "input-1", "result-digest-1", "PASS", None,
                "validator-settlement-1", settlement.settlement_hash,
            )
        )
        self.oracle.allowed_head = recorded.event_hash
        release = BudgetSettlementRequest(
            "validator-release-1", "validator-reservation-1",
            settlement.settlement_hash, BudgetDisposition.RELEASED, None,
            "validator-nondispatch-proof", "NONDISPATCH",
            non_dispatch_proven=True, zero_liability_proven=True,
        )

        with self.assertRaisesRegex(
            DispatchDenied, "cannot release liability"
        ):
            self.store._settle_budget(
                release,
                self.authority.issue_settlement_proof(
                    "validator-release-proof-1", release
                ),
                self.authority,
            )
        self.assertEqual(self.store.table_counts()["budget_settlements"], 2)

    def test_recovery_rejects_validator_unknown_usage_state_suppression(
        self,
    ) -> None:
        observation = self._record_effect_observation(check_ids=("check-1",))
        intent_request, capability = self._validator_intent(observation)
        intent = self.store.commit_validator_intent(
            intent_request, capability, self.authority
        )
        self.oracle.allowed_head = intent.event_hash
        unknown = BudgetSettlementRequest(
            "validator-settlement-1", "validator-reservation-1", "",
            BudgetDisposition.UNKNOWN_WORST_CASE_CHARGED, None,
            "validator-result-1", "VALIDATOR_USAGE_UNKNOWN",
        )
        settlement = self.store._settle_budget(
            unknown,
            self.authority.issue_settlement_proof(
                "validator-proof-1", unknown
            ),
            self.authority,
        )
        self.oracle.allowed_head = settlement.settlement_hash
        recorded = self.store._record_validator_observation(
            ValidatorObservationRequest(
                "validator-observation-1", "validator-observe-command-1",
                "validator-observation-event-1", "repo-1", "run-1", "item-1",
                "effect-1", "validator-intent-1", "validator-attempt-1",
                "validator-result-1", capability.claim_id, "revision-1",
                "check-1", "input-1", "result-digest-1", "PASS", None,
                "validator-settlement-1", settlement.settlement_hash,
            )
        )
        self.assertEqual(
            recorded.resulting_state, LifecycleState.RECONCILIATION_REQUIRED
        )
        connection = sqlite3.connect(self.database_path)
        try:
            body = json.loads(
                connection.execute(
                    "SELECT body_json FROM events WHERE event_id = ?",
                    (recorded.event_id,),
                ).fetchone()[0]
            )
            body["lifecycle_to"] = LifecycleState.VALIDATING.value
            event_hash = self.store._event_hash(body)
            body_json = json.dumps(
                body, sort_keys=True, separators=(",", ":")
            )
            connection.execute(
                "UPDATE events SET event_hash = ?, body_json = ? WHERE event_id = ?",
                (event_hash, body_json, recorded.event_id),
            )
            connection.execute(
                "UPDATE validator_observations SET event_hash = ?, "
                "resulting_state = ?, body_json = ? WHERE observation_id = ?",
                (
                    event_hash, LifecycleState.VALIDATING.value, body_json,
                    recorded.observation_id,
                ),
            )
            connection.execute(
                "UPDATE command_outcomes SET event_hash = ? WHERE command_id = ?",
                (event_hash, recorded.command_id),
            )
            connection.execute(
                "UPDATE runs SET lifecycle_state = ?, head_hash = ? WHERE run_id = ?",
                (LifecycleState.VALIDATING.value, event_hash, "run-1"),
            )
            connection.execute(
                "UPDATE repositories SET catalog_head = ? WHERE repository_id = ?",
                (event_hash, "repo-1"),
            )
            connection.commit()
        finally:
            connection.close()
        self.oracle.allowed_head = event_hash

        with self.assertRaisesRegex(
            StorageIntegrityError,
            "uncertainty-instance projection|validator observation semantics",
        ):
            self.store.load_verified("repo-1")

    def _classification(self, observation, classification: str):
        return self.authority.issue_classification(
            f"classification-{classification.lower()}", "repo-1", "run-1",
            "item-1", "effect-1", "revision-1", "check-1",
            "validator-attempt-1", "validator-observation-1",
            observation.event_hash, "result-digest-1", verdict="FAIL",
            policy_id="failure-policy", policy_version="1",
            classification=classification,
        )

    def _prepare_recoverable_application(self):
        observation = self._record_validator_result(
            verdict="FAIL", only_check=True
        )
        failed = self.store._apply_validator_observation(
            ValidationApplicationRequest(
                "application-1", "apply-command-1", "apply-event-1",
                "repo-1", "run-1", "item-1", "effect-1", "revision-1",
                "check-1", "validator-attempt-1", "validator-observation-1",
            ),
            classification=self._classification(observation, "RECOVERABLE"),
        )
        self.oracle.allowed_head = failed.event_hash
        return observation, failed

    def _validation_recovery_pair(
        self,
        failed,
        *,
        suffix: str = "1",
        expected_run_head: str | None = None,
        successor_validator_attempt_id: str = "validator-attempt-2",
    ):
        recovery_id = f"recovery-{suffix}"
        request = ValidationRecoveryRequest(
            recovery_id, f"recovery-command-{suffix}",
            f"recovery-event-{suffix}", "repo-1", "run-1", "item-1",
            "effect-1", "plan-1", "revision-1", "check-1",
            "application-1", "validator-attempt-1",
            successor_validator_attempt_id,
            f"remediation-evidence-{suffix}",
            expected_run_head or failed.event_hash, "attempt-1", 1,
        )
        connection = sqlite3.connect(self.database_path)
        try:
            plan_event_hash = connection.execute(
                "SELECT event_hash FROM validation_plans WHERE plan_id = 'plan-1'"
            ).fetchone()[0]
            parent_event_hash = connection.execute(
                "SELECT event_hash FROM effect_observations "
                "WHERE observation_id = 'observation-1'"
            ).fetchone()[0]
        finally:
            connection.close()
        attestation = self.authority.issue_validation_recovery_attestation(
            f"recovery-attestation-{suffix}", request.recovery_id,
            request.repository_id, request.run_id, request.item_id,
            request.logical_effect_id, request.plan_id, plan_event_hash,
            request.revision_digest, request.check_id,
            request.failed_application_id, failed.event_hash,
            request.failed_validator_attempt_id,
            request.successor_validator_attempt_id,
            request.remediation_evidence_digest, request.expected_run_head,
            request.expected_slot_attempt_id, request.expected_slot_generation,
        )
        return request, attestation, parent_event_hash

    def _prepare_finalization(
        self, *, aggregate_gate_ids=None
    ):
        self._record_validator_result(
            only_check=True, aggregate_gate_ids=aggregate_gate_ids
        )
        applied = self.store._apply_validator_observation(
            ValidationApplicationRequest(
                "application-1", "apply-command-1", "apply-event-1", "repo-1",
                "run-1", "item-1", "effect-1", "revision-1", "check-1",
                "validator-attempt-1", "validator-observation-1",
            ),
        )
        self.oracle.allowed_head = applied.event_hash
        return self._finalization_request_and_attestation(applied.event_hash)

    def _finalization_request_and_attestation(self, evaluated_run_head: str):
        request = FinalizeOperationRequest(
            "finalization-1", "finalize-command-1", "finalize-event-1",
            "repo-1", "run-1", "item-1", "effect-1", "plan-1",
            "revision-1", "attempt-1", 1,
        )
        finalization_key = self.store.finalization_key(
            "repo-1", "run-1", "item-1", "effect-1", "plan-1", "revision-1"
        )
        connection = sqlite3.connect(self.database_path)
        try:
            plan_event_hash, gate_set_digest = connection.execute(
                "SELECT event_hash, gate_set_digest FROM validation_plans "
                "WHERE plan_id = 'plan-1'"
            ).fetchone()
        finally:
            connection.close()
        attestation = self.authority.issue_finalization_attestation(
            "attestation-1", "repo-1", "run-1", "item-1", "effect-1",
            "plan-1", plan_event_hash, "revision-1", evaluated_run_head,
            finalization_key, gate_set_digest, "attempt-1", 1,
        )
        return request, attestation

    def _reissue_finalization_attestation(self, attestation, **changes):
        values = {
            name: getattr(attestation, name)
            for name in attestation.__dataclass_fields__
            if name != "issuer_mac"
        }
        values.update(changes)
        return self.authority.issue_finalization_attestation(**values)

    def test_c05_pass_application_is_atomic_replay_safe_and_retains_slot(self) -> None:
        self._record_validator_result()
        request = ValidationApplicationRequest(
            "application-1", "apply-command-1", "apply-event-1", "repo-1",
            "run-1", "item-1", "effect-1", "revision-1", "check-1",
            "validator-attempt-1", "validator-observation-1",
        )
        with self.assertRaises(InjectedFailure):
            self.store._apply_validator_observation(
                request,
                failure_hook=raise_at(
                    "after_validation_application_writes_before_commit"
                ),
            )
        self.assertEqual(self.store.table_counts()["validation_applications"], 0)
        with self.assertRaises(InjectedFailure):
            self.store._apply_validator_observation(
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
        replay = self.store._apply_validator_observation(
            request
        )
        self.assertTrue(replay.replayed)
        self.assertEqual(replay.resulting_state.value, "VALIDATING")
        self.assertEqual(self.store.table_counts()["validation_applications"], 1)
        self.assertEqual(self.store.table_counts()["outstanding_slot"], 1)
        self.store.load_verified("repo-1")

    def test_c05_last_pass_blocks_for_distinct_finalization(self) -> None:
        self._record_validator_result(only_check=True)
        applied = self.store._apply_validator_observation(
            ValidationApplicationRequest(
                "application-1", "apply-command-1", "apply-event-1", "repo-1",
                "run-1", "item-1", "effect-1", "revision-1", "check-1",
                "validator-attempt-1", "validator-observation-1",
            ),
        )
        self.assertEqual(applied.resulting_state.value, "BLOCKED")
        self.assertEqual(self.store.table_counts()["outstanding_slot"], 1)
        connection = sqlite3.connect(self.database_path)
        try:
            cursor = connection.execute(
                "SELECT continuation_cursor FROM validation_applications "
                "WHERE application_id = 'application-1'"
            ).fetchone()[0]
        finally:
            connection.close()
        self.assertEqual(cursor, "FINALIZING")

    def _terminal_application_request(
        self, disposition: str
    ) -> TerminalValidationSettlementRequest:
        connection = sqlite3.connect(self.database_path)
        try:
            application_hash = connection.execute(
                "SELECT event_hash FROM validation_applications "
                "WHERE application_id = 'application-1'"
            ).fetchone()[0]
        finally:
            connection.close()
        return TerminalValidationSettlementRequest(
            "terminal-settlement-1", "terminal-command-1",
            "terminal-event-1", "repo-1", "run-1", "item-1",
            "effect-1", "plan-1", "revision-1", "check-1",
            "VALIDATION_APPLICATION", "application-1", application_hash,
            disposition, "validator-intent-1", "validator-attempt-1",
        )

    def _assert_r_stop_01_application_closure(
        self, *, verdict: str, mode: StopMode
    ) -> None:
        if verdict == "PASS":
            self._prepare_finalization()
            expected_cursor = "FINALIZING"
            disposition = "PASSED"
        else:
            self._prepare_recoverable_application()
            expected_cursor = LifecycleState.VALIDATING.value
            disposition = "FAILED"
        stopped = self.store.stop(
            self._stop_request(mode),
            self._stop_capability(mode),
            self.authority,
        )
        self.oracle.allowed_head = stopped.event_hash
        self.assertEqual(self.store.table_counts()["outstanding_slot"], 1)
        connection = sqlite3.connect(self.database_path)
        try:
            run_cursor, retained_cursor = connection.execute(
                "SELECT run.continuation_cursor, stop.retained_continuation_cursor "
                "FROM runs AS run JOIN stop_actions AS stop ON "
                "stop.run_id = run.run_id WHERE run.run_id = 'run-1'"
            ).fetchone()
        finally:
            connection.close()
        self.assertEqual(run_cursor, expected_cursor)
        self.assertEqual(retained_cursor, expected_cursor)

        second_grant = SyntheticGrant(
            "grant-2", "repo-1", "effect-2", "attempt-2", "scope-2"
        )
        self.authority.register(second_grant)
        second_capability = self.authority.claim(
            *second_grant.__dict__.values()
        )
        second_plan = self.store.accept_plan(
            PlanAcceptanceRequest(
                "plan-2", "plan-command-2", "plan-event-2", "repo-1",
                "run-2", "item-2", "effect-2", "revision-2",
                "descriptor-digest", "scope-2", "budget-policy-digest",
                ("check-2",),
            ),
            expected_head=stopped.event_hash,
            writer_epoch=40,
        )
        self.oracle.allowed_head = second_plan.event_hash
        second_request = replace(
            self.request(), run_id="run-2", item_id="item-2",
            command_id="command-2", event_id="event-2",
            logical_effect_id="effect-2", attempt_id="attempt-2",
            permission_use_id="permission-use-2",
            reservation_id="reservation-2",
        )
        with self.assertRaisesRegex(DispatchDenied, "repository slot"):
            self.store.commit_intent(
                second_request, second_capability, self.authority,
                expected_head=second_plan.event_hash, writer_epoch=41,
            )

        settled = self.store.settle_terminal_validation(
            self._terminal_application_request(disposition)
        )
        self.assertEqual(settled.resulting_state, LifecycleState.STOPPED)
        self.assertTrue(settled.slot_released)
        self.assertEqual(self.store.table_counts()["outstanding_slot"], 0)
        self.oracle.allowed_head = settled.event_hash
        self.store.load_verified("repo-1")

        committed = self.store.commit_intent(
            second_request, second_capability, self.authority,
            expected_head=settled.event_hash, writer_epoch=42,
        )
        self.oracle.allowed_head = committed.event_hash
        replay = self.store.commit_intent(
            second_request, second_capability, self.authority,
            expected_head=committed.event_hash, writer_epoch=43,
        )
        self.assertTrue(replay.replayed)
        self.assertEqual(replay.event_hash, committed.event_hash)
        self.assertEqual(self.store.table_counts()["outstanding_slot"], 1)

    def test_t14_pause_rejects_caller_fabricated_preserved_cursor(self) -> None:
        plan = self.store.accept_plan(
            PlanAcceptanceRequest(
                "plan-1", "plan-command-1", "plan-event-1", "repo-1",
                "run-1", "item-1", "effect-1", "revision-1",
                "descriptor-digest", "scope-1", "budget-policy-digest",
                ("check-1",),
            ),
            expected_head="", writer_epoch=1,
        )
        self.oracle.allowed_head = plan.event_hash
        with self.assertRaisesRegex(DispatchDenied, "preserved cursor"):
            self.store.pause_before_dispatch(
                replace(
                    self._pause_request(),
                    continuation_cursor="fabricated-validation-cursor",
                ),
                self._pause_capability(),
                self.authority,
            )
        self.assertEqual(self.store.load_run_lifecycle("run-1"), LifecycleState.PLANNED)
        self.assertEqual(self.store.table_counts()["dispatch_fences"], 0)

    def test_r_stop_03_immediate_stop_charges_contacted_unknown(self) -> None:
        request = self.request()
        committed = self._commit_planned_intent(
            request, self.capability, self.authority,
            expected_head="", writer_epoch=1,
        )
        self.oracle.allowed_head = committed.event_hash
        launched = self.store.claim_operation_launch(request, committed)
        self.oracle.allowed_head = launched.event_hash
        self.store._contact_claimed_operation(
            request, self.capability, committed, launched,
            self.store._adapter_target_digest("repo-1", "EFFECT"),
        )
        connection = sqlite3.connect(self.database_path)
        try:
            contact_hash = connection.execute(
                "SELECT event_hash FROM adapter_contacts WHERE "
                "contact_kind = 'EFFECT'"
            ).fetchone()[0]
        finally:
            connection.close()
        self.oracle.allowed_head = contact_hash

        stopped = self.store.stop(
            self._stop_request(),
            self._stop_capability(StopMode.IMMEDIATE),
            self.authority,
        )
        self.oracle.allowed_head = stopped.event_hash
        connection = sqlite3.connect(self.database_path)
        try:
            accounting = connection.execute(
                "SELECT held_units, charged_units, uncertainty, disposition "
                "FROM budget_reservations WHERE reservation_id = ?",
                ("reservation-1",),
            ).fetchone()
            stop_body = json.loads(connection.execute(
                "SELECT body_json FROM stop_actions WHERE stop_id = 'stop-1'"
            ).fetchone()[0])
            epoch_rows = connection.execute(
                "SELECT event_kind, event_id, sequence FROM events WHERE "
                "writer_epoch = ? ORDER BY rowid",
                (stop_body["writer_epoch"],),
            ).fetchall()
        finally:
            connection.close()
        self.assertEqual(
            accounting,
            (0, 5, 1, BudgetDisposition.UNKNOWN_WORST_CASE_CHARGED.value),
        )
        self.assertEqual(
            epoch_rows,
            [
                (
                    "BUDGET_SETTLED",
                    stop_body["uncertainty_snapshot"][0]["settlement_event_id"],
                    stop_body["sequence"] - 1,
                ),
                ("STOP_RECORDED", "stop-event-1", stop_body["sequence"]),
            ],
        )
        self.store.load_verified("repo-1")

    def test_r_stop_03_precontact_stop_retains_reserve(self) -> None:
        request = self.request()
        committed = self._commit_planned_intent(
            request, self.capability, self.authority,
            expected_head="", writer_epoch=1,
        )
        self.oracle.allowed_head = committed.event_hash
        launched = self.store.claim_operation_launch(request, committed)
        self.oracle.allowed_head = launched.event_hash
        stopped = self.store.stop(
            self._stop_request(), self._stop_capability(StopMode.IMMEDIATE),
            self.authority,
        )
        self.oracle.allowed_head = stopped.event_hash
        connection = sqlite3.connect(self.database_path)
        try:
            accounting = connection.execute(
                "SELECT held_units, charged_units, disposition FROM "
                "budget_reservations WHERE reservation_id = 'reservation-1'"
            ).fetchone()
            body = json.loads(connection.execute(
                "SELECT body_json FROM stop_actions WHERE stop_id = 'stop-1'"
            ).fetchone()[0])
        finally:
            connection.close()
        self.assertEqual(accounting, (3, 0, BudgetDisposition.RESERVED.value))
        self.assertEqual(body["uncertainty_snapshot"], [])
        self.store.load_verified("repo-1")

    def test_r_stop_03_crash_boundaries_replay_exactly_once(self) -> None:
        request = self.request()
        committed = self._commit_planned_intent(
            request, self.capability, self.authority,
            expected_head="", writer_epoch=1,
        )
        self.oracle.allowed_head = committed.event_hash
        launched = self.store.claim_operation_launch(request, committed)
        self.oracle.allowed_head = launched.event_hash
        self.store._contact_claimed_operation(
            request, self.capability, committed, launched,
            self.store._adapter_target_digest("repo-1", "EFFECT"),
        )
        connection = sqlite3.connect(self.database_path)
        try:
            self.oracle.allowed_head = connection.execute(
                "SELECT event_hash FROM adapter_contacts WHERE "
                "contact_kind = 'EFFECT'"
            ).fetchone()[0]
        finally:
            connection.close()
        stop_request = self._stop_request()
        capability = self._stop_capability(StopMode.IMMEDIATE)
        for point in (
            "after_stop_unknown_settlement_before_stop_recorded",
            "after_stop_writes_before_commit",
        ):
            with self.assertRaises(InjectedFailure):
                self.store.stop(
                    stop_request, capability, self.authority,
                    failure_hook=raise_at(point),
                )
            self.assertEqual(self.store.table_counts()["stop_actions"], 0)
            self.assertEqual(self.store.table_counts()["budget_settlements"], 0)
        with self.assertRaises(InjectedFailure):
            self.store.stop(
                stop_request, capability, self.authority,
                failure_hook=raise_at(
                    "after_stop_commit_before_acknowledgement"
                ),
            )
        connection = sqlite3.connect(self.database_path)
        try:
            stop_hash = connection.execute(
                "SELECT event_hash FROM stop_actions WHERE stop_id = 'stop-1'"
            ).fetchone()[0]
        finally:
            connection.close()
        self.oracle.allowed_head = stop_hash
        replay = self.store.stop(stop_request, capability, self.authority)
        self.assertTrue(replay.replayed)
        self.assertEqual(self.store.table_counts()["stop_actions"], 1)
        self.assertEqual(self.store.table_counts()["budget_settlements"], 1)
        self.store.load_verified("repo-1")

    def test_r_stop_03_recovery_rejects_snapshot_retarget(self) -> None:
        request = self.request()
        committed = self._commit_planned_intent(
            request, self.capability, self.authority,
            expected_head="", writer_epoch=1,
        )
        self.oracle.allowed_head = committed.event_hash
        launched = self.store.claim_operation_launch(request, committed)
        self.oracle.allowed_head = launched.event_hash
        self.store._contact_claimed_operation(
            request, self.capability, committed, launched,
            self.store._adapter_target_digest("repo-1", "EFFECT"),
        )
        connection = sqlite3.connect(self.database_path)
        try:
            self.oracle.allowed_head = connection.execute(
                "SELECT event_hash FROM adapter_contacts WHERE "
                "contact_kind = 'EFFECT'"
            ).fetchone()[0]
        finally:
            connection.close()
        stopped = self.store.stop(
            self._stop_request(), self._stop_capability(StopMode.IMMEDIATE),
            self.authority,
        )
        connection = sqlite3.connect(self.database_path)
        try:
            body = json.loads(connection.execute(
                "SELECT body_json FROM stop_actions WHERE stop_id = 'stop-1'"
            ).fetchone()[0])
            body["uncertainty_snapshot"][0]["contact_id"] = "forged-contact"
            forged_hash = self.store._event_hash(body)
            body_json = json.dumps(body, sort_keys=True, separators=(",", ":"))
            connection.execute(
                "UPDATE events SET event_hash = ?, body_json = ? WHERE "
                "event_id = 'stop-event-1'", (forged_hash, body_json)
            )
            connection.execute(
                "UPDATE stop_actions SET event_hash = ?, body_json = ? WHERE "
                "stop_id = 'stop-1'", (forged_hash, body_json)
            )
            connection.execute(
                "UPDATE command_outcomes SET event_hash = ? WHERE "
                "command_id = 'stop-command-1'", (forged_hash,)
            )
            connection.execute(
                "UPDATE runs SET head_hash = ? WHERE run_id = 'run-1'",
                (forged_hash,),
            )
            connection.execute(
                "UPDATE repositories SET catalog_head = ? WHERE "
                "repository_id = 'repo-1'", (forged_hash,),
            )
            connection.commit()
        finally:
            connection.close()
        self.oracle.allowed_head = forged_hash
        with self.assertRaises(StorageIntegrityError):
            self.store.load_verified("repo-1")

    def test_r_stop_03_validator_contact_is_unknown_but_known_effect_retained(
        self,
    ) -> None:
        observation = self._record_effect_observation(check_ids=("check-1",))
        request, capability = self._validator_intent(observation)
        committed = self.store.commit_validator_intent(
            request, capability, self.authority
        )
        self.oracle.allowed_head = committed.event_hash
        self.store._contact_committed_validator(
            request, capability, committed,
            self.store._adapter_target_digest("repo-1", "VALIDATOR"),
            self.authority,
        )
        connection = sqlite3.connect(self.database_path)
        try:
            self.oracle.allowed_head = connection.execute(
                "SELECT event_hash FROM adapter_contacts WHERE "
                "contact_kind = 'VALIDATOR'"
            ).fetchone()[0]
        finally:
            connection.close()
        stopped = self.store.stop(
            self._stop_request(), self._stop_capability(StopMode.IMMEDIATE),
            self.authority,
        )
        self.oracle.allowed_head = stopped.event_hash
        connection = sqlite3.connect(self.database_path)
        try:
            accounting = connection.execute(
                "SELECT reservation_id, disposition, charged_units FROM "
                "budget_reservations ORDER BY reservation_id"
            ).fetchall()
            body = json.loads(connection.execute(
                "SELECT body_json FROM stop_actions WHERE stop_id = 'stop-1'"
            ).fetchone()[0])
        finally:
            connection.close()
        self.assertEqual(accounting[0][1], BudgetDisposition.CONSUMED.value)
        self.assertEqual(
            accounting[1],
            (
                "validator-reservation-1",
                BudgetDisposition.UNKNOWN_WORST_CASE_CHARGED.value,
                2,
            ),
        )
        self.assertEqual(
            body["uncertainty_snapshot"][0]["contact_kind"], "VALIDATOR"
        )
        self.store.load_verified("repo-1")

    def test_r_stop_03_late_authoritative_usage_adjusts_without_reopen(self) -> None:
        request = self.request()
        committed = self._commit_planned_intent(
            request, self.capability, self.authority,
            expected_head="", writer_epoch=1,
        )
        self.oracle.allowed_head = committed.event_hash
        launched = self.store.claim_operation_launch(request, committed)
        self.oracle.allowed_head = launched.event_hash
        self.store._contact_claimed_operation(
            request, self.capability, committed, launched,
            self.store._adapter_target_digest("repo-1", "EFFECT"),
        )
        connection = sqlite3.connect(self.database_path)
        try:
            self.oracle.allowed_head = connection.execute(
                "SELECT event_hash FROM adapter_contacts WHERE "
                "contact_kind = 'EFFECT'"
            ).fetchone()[0]
        finally:
            connection.close()
        stopped = self.store.stop(
            self._stop_request(), self._stop_capability(StopMode.IMMEDIATE),
            self.authority,
        )
        self.oracle.allowed_head = stopped.event_hash
        connection = sqlite3.connect(self.database_path)
        try:
            unknown_hash = connection.execute(
                "SELECT settlement_head_hash FROM budget_reservations WHERE "
                "reservation_id = 'reservation-1'"
            ).fetchone()[0]
        finally:
            connection.close()
        adjustment = BudgetSettlementRequest(
            "late-stop-adjustment-1", "reservation-1", unknown_hash,
            BudgetDisposition.ADJUSTED, 2, "late-authoritative-bill-1",
            "AUTHORITATIVE_LATE_USAGE",
        )
        adjusted = self.store._settle_budget(
            adjustment,
            self.authority.issue_settlement_proof(
                "late-stop-adjustment-proof-1", adjustment
            ),
            self.authority,
        )
        self.oracle.allowed_head = adjusted.settlement_hash
        self.assertEqual(
            self.store.load_run_lifecycle("run-1"), LifecycleState.STOPPED
        )
        connection = sqlite3.connect(self.database_path)
        try:
            accounting = connection.execute(
                "SELECT charged_units, uncertainty, disposition FROM "
                "budget_reservations WHERE reservation_id = 'reservation-1'"
            ).fetchone()
        finally:
            connection.close()
        self.assertEqual(accounting, (2, 0, BudgetDisposition.ADJUSTED.value))
        reopened = SQLiteStateStore(
            self.database_path, self.oracle, "repo-1"
        )
        reopened.load_verified("repo-1", authority=self.authority)

    def test_r_stop_03_reused_attempt_on_other_run_cannot_hide_contact(
        self,
    ) -> None:
        self._prepare_finalization()
        stopped_1 = self.store.stop(
            self._stop_request(), self._stop_capability(StopMode.IMMEDIATE),
            self.authority,
        )
        self.oracle.allowed_head = stopped_1.event_hash
        connection = sqlite3.connect(self.database_path)
        try:
            first_stop_body = json.loads(connection.execute(
                "SELECT body_json FROM stop_actions WHERE stop_id = 'stop-1'"
            ).fetchone()[0])
            first_disposition = connection.execute(
                "SELECT disposition FROM budget_reservations WHERE "
                "reservation_id = 'reservation-1'"
            ).fetchone()[0]
        finally:
            connection.close()
        self.assertEqual(first_stop_body["uncertainty_snapshot"], [])
        self.assertEqual(first_disposition, BudgetDisposition.CONSUMED.value)
        closed = self.store.settle_terminal_validation(
            self._terminal_application_request("PASSED")
        )
        self.oracle.allowed_head = closed.event_hash
        plan_2 = self.store.accept_plan(
            PlanAcceptanceRequest(
                "plan-2", "plan-command-2", "plan-event-2", "repo-1",
                "run-2", "item-2", "effect-2", "revision-2",
                "descriptor-2", "scope-2", "budget-policy-2", ("check-2",),
            ),
            expected_head=closed.event_hash, writer_epoch=90,
        )
        self.oracle.allowed_head = plan_2.event_hash
        grant_2 = SyntheticGrant(
            "grant-2", "repo-1", "effect-2", "attempt-1", "scope-2"
        )
        self.authority.register(grant_2)
        capability_2 = self.authority.claim(*grant_2.__dict__.values())
        request_2 = replace(
            self.request(), run_id="run-2", item_id="item-2",
            command_id="command-2", event_id="event-2",
            logical_effect_id="effect-2", permission_use_id="permission-use-2",
            reservation_id="reservation-2", effect_descriptor_digest="descriptor-2",
            budget_policy_digest="budget-policy-2",
        )
        committed_2 = self.store.commit_intent(
            request_2, capability_2, self.authority,
            expected_head=plan_2.event_hash, writer_epoch=91,
        )
        self.oracle.allowed_head = committed_2.event_hash
        launched_2 = self.store.claim_operation_launch(request_2, committed_2)
        self.oracle.allowed_head = launched_2.event_hash
        self.store._contact_claimed_operation(
            request_2, capability_2, committed_2, launched_2,
            self.store._adapter_target_digest("repo-1", "EFFECT"),
        )
        connection = sqlite3.connect(self.database_path)
        try:
            self.oracle.allowed_head = connection.execute(
                "SELECT event_hash FROM adapter_contacts WHERE run_id = 'run-2'"
            ).fetchone()[0]
        finally:
            connection.close()
        stop_2 = replace(
            self._stop_request(StopMode.IMMEDIATE, "2"), run_id="run-2"
        )
        stop_grant_2 = SyntheticOperatorGrant(
            "stop-grant-2", "repo-1", "run-2", "STOP_IMMEDIATE",
            "stop-scope-2",
        )
        self.authority.register_operator(stop_grant_2)
        stopped_2 = self.store.stop(
            stop_2,
            self.authority.claim_operator(*stop_grant_2.__dict__.values()),
            self.authority,
        )
        self.oracle.allowed_head = stopped_2.event_hash
        connection = sqlite3.connect(self.database_path)
        try:
            disposition = connection.execute(
                "SELECT disposition FROM budget_reservations WHERE "
                "reservation_id = 'reservation-2'"
            ).fetchone()[0]
        finally:
            connection.close()
        self.assertEqual(
            disposition, BudgetDisposition.UNKNOWN_WORST_CASE_CHARGED.value
        )
        self.store.load_verified("repo-1")

    def test_t20_escalation_atomically_charges_unknown_and_replays(self) -> None:
        request = self.request()
        committed = self._commit_planned_intent(
            request, self.capability, self.authority,
            expected_head="", writer_epoch=1,
        )
        self.oracle.allowed_head = committed.event_hash
        launched = self.store.claim_operation_launch(request, committed)
        self.oracle.allowed_head = launched.event_hash
        graceful_request = replace(
            self._stop_request(StopMode.GRACEFUL),
            drain_deadline_utc="2000-01-01T00:00:00Z",
        )
        stopped = self.store.stop(
            graceful_request,
            self._stop_capability(StopMode.GRACEFUL),
            self.authority,
        )
        self.oracle.allowed_head = stopped.event_hash
        escalation_request = StopEscalationRequest(
            "escalation-1", "escalation-command-1", "escalation-event-1",
            "repo-1", "run-1", graceful_request.stop_id,
            graceful_request.event_id,
            graceful_request.drain_deadline_utc,
            "GRACEFUL_DEADLINE_EXPIRED",
            (
                StopEscalationSettlement(
                    "reservation-1", "escalation-settlement-event-1", ""
                ),
            ),
        )
        capability = self._stop_escalation_capability()

        escalated = self.store.escalate_stop(
            escalation_request, capability, self.authority
        )
        self.oracle.allowed_head = escalated.event_hash
        connection = sqlite3.connect(self.database_path)
        try:
            accounting = connection.execute(
                "SELECT held_units, charged_units, uncertainty, disposition "
                "FROM budget_reservations WHERE reservation_id = ?",
                ("reservation-1",),
            ).fetchone()
        finally:
            connection.close()
        self.assertEqual(
            accounting,
            (0, 5, 1, BudgetDisposition.UNKNOWN_WORST_CASE_CHARGED.value),
        )
        self.assertEqual(escalated.resulting_state, LifecycleState.STOPPED)
        self.assertEqual(self.store.table_counts()["outstanding_slot"], 1)
        replay = self.store.escalate_stop(
            escalation_request, capability, self.authority
        )
        self.assertTrue(replay.replayed)
        self.assertEqual(replay.event_hash, escalated.event_hash)
        self.assertEqual(self.store.table_counts()["budget_settlements"], 1)
        self.store.load_verified("repo-1")

    def test_t20_crash_boundaries_are_atomic_and_exactly_once(self) -> None:
        request = self.request()
        committed = self._commit_planned_intent(
            request, self.capability, self.authority,
            expected_head="", writer_epoch=1,
        )
        self.oracle.allowed_head = committed.event_hash
        launched = self.store.claim_operation_launch(request, committed)
        self.oracle.allowed_head = launched.event_hash
        graceful = replace(
            self._stop_request(StopMode.GRACEFUL),
            drain_deadline_utc="2000-01-01T00:00:00Z",
        )
        stopped = self.store.stop(
            graceful, self._stop_capability(StopMode.GRACEFUL), self.authority
        )
        self.oracle.allowed_head = stopped.event_hash
        escalation = StopEscalationRequest(
            "escalation-1", "escalation-command-1", "escalation-event-1",
            "repo-1", "run-1", graceful.stop_id, graceful.event_id,
            graceful.drain_deadline_utc, "GRACEFUL_DEADLINE_EXPIRED",
            (StopEscalationSettlement(
                "reservation-1", "escalation-settlement-event-1", ""
            ),),
        )
        capability = self._stop_escalation_capability()

        with self.assertRaises(InjectedFailure):
            self.store.escalate_stop(
                escalation, capability, self.authority,
                failure_hook=raise_at(
                    "after_stop_escalation_writes_before_commit"
                ),
            )
        self.assertEqual(self.store.table_counts()["stop_escalations"], 0)
        self.assertEqual(self.store.table_counts()["budget_settlements"], 0)
        connection = sqlite3.connect(self.database_path)
        try:
            self.assertEqual(
                connection.execute(
                    "SELECT disposition FROM budget_reservations WHERE "
                    "reservation_id = 'reservation-1'"
                ).fetchone()[0],
                BudgetDisposition.RESERVED.value,
            )
        finally:
            connection.close()

        with self.assertRaises(InjectedFailure):
            self.store.escalate_stop(
                escalation, capability, self.authority,
                failure_hook=raise_at(
                    "after_stop_escalation_commit_before_acknowledgement"
                ),
            )
        connection = sqlite3.connect(self.database_path)
        try:
            escalation_hash = connection.execute(
                "SELECT event_hash FROM stop_escalations WHERE "
                "escalation_id = 'escalation-1'"
            ).fetchone()[0]
        finally:
            connection.close()
        self.oracle.allowed_head = escalation_hash
        replay = self.store.escalate_stop(
            escalation, capability, self.authority
        )
        self.assertTrue(replay.replayed)
        self.assertEqual(self.store.table_counts()["stop_escalations"], 1)
        self.assertEqual(self.store.table_counts()["budget_settlements"], 1)
        self.assertEqual(self.store.table_counts()["operator_redemptions"], 2)
        self.store.load_verified("repo-1")

    def test_t20_denies_predeadline_immediate_and_no_activity(self) -> None:
        request = self.request()
        committed = self._commit_planned_intent(
            request, self.capability, self.authority,
            expected_head="", writer_epoch=1,
        )
        self.oracle.allowed_head = committed.event_hash
        launched = self.store.claim_operation_launch(request, committed)
        self.oracle.allowed_head = launched.event_hash
        graceful = self._stop_request(StopMode.GRACEFUL)
        stopped = self.store.stop(
            graceful, self._stop_capability(StopMode.GRACEFUL), self.authority
        )
        self.oracle.allowed_head = stopped.event_hash
        escalation = StopEscalationRequest(
            "escalation-1", "escalation-command-1", "escalation-event-1",
            "repo-1", "run-1", graceful.stop_id, graceful.event_id,
            graceful.drain_deadline_utc, "GRACEFUL_DEADLINE_EXPIRED",
            (StopEscalationSettlement(
                "reservation-1", "escalation-settlement-event-1", ""
            ),),
        )
        with self.assertRaisesRegex(DispatchDenied, "has not expired"):
            self.store.escalate_stop(
                escalation, self._stop_escalation_capability(), self.authority
            )

        with tempfile.TemporaryDirectory() as directory:
            oracle = MutableFreshnessOracle()
            store = SQLiteStateStore(
                Path(directory) / "state.sqlite3", oracle, "repo-1"
            )
            authority = SyntheticAuthority()
            store._bind_classification_authority(authority)
            plan = store.accept_plan(
                PlanAcceptanceRequest(
                    "plan-x", "plan-command-x", "plan-event-x", "repo-1",
                    "run-x", "item-x", "effect-x", "revision-x",
                    "descriptor-x", "scope-x", "budget-x", ("check-x",),
                ),
                expected_head="", writer_epoch=1,
            )
            oracle.allowed_head = plan.event_hash
            stop_grant = SyntheticOperatorGrant(
                "stop-grant-x", "repo-1", "run-x", "STOP_GRACEFUL",
                "stop-scope-x",
            )
            authority.register_operator(stop_grant)
            stop_capability = authority.claim_operator(
                *stop_grant.__dict__.values()
            )
            no_activity_stop = StopRequest(
                "stop-x", "stop-command-x", "stop-event-x", "repo-1",
                "run-x", StopMode.GRACEFUL, "OPERATOR_STOP",
                "2000-01-01T00:00:00Z",
            )
            stopped_x = store.stop(
                no_activity_stop, stop_capability, authority
            )
            oracle.allowed_head = stopped_x.event_hash
            escalation_grant = SyntheticOperatorGrant(
                "escalation-grant-x", "repo-1", "run-x", "STOP_ESCALATE",
                "escalation-scope-x",
            )
            authority.register_operator(escalation_grant)
            escalation_capability = authority.claim_operator(
                *escalation_grant.__dict__.values()
            )
            with self.assertRaisesRegex(DispatchDenied, "drain obligations"):
                store.escalate_stop(
                    StopEscalationRequest(
                        "escalation-x", "escalation-command-x",
                        "escalation-event-x", "repo-1", "run-x", "stop-x",
                        "stop-event-x", "2000-01-01T00:00:00Z",
                        "GRACEFUL_DEADLINE_EXPIRED",
                    ),
                    escalation_capability,
                    authority,
                )

    def test_t20_retains_known_and_existing_unknown_accounting(self) -> None:
        observation = self._record_effect_observation(check_ids=("check-1",))
        intent_request, validator_capability = self._validator_intent(observation)
        intent = self.store.commit_validator_intent(
            intent_request, validator_capability, self.authority
        )
        self.oracle.allowed_head = intent.event_hash
        unknown = BudgetSettlementRequest(
            "validator-unknown-1", "validator-reservation-1", "",
            BudgetDisposition.UNKNOWN_WORST_CASE_CHARGED, None,
            "deadline-unknown", "VALIDATOR_DRAIN_UNKNOWN",
        )
        settled = self.store._settle_budget(
            unknown,
            self.authority.issue_settlement_proof("validator-proof-1", unknown),
            self.authority,
        )
        self.oracle.allowed_head = settled.settlement_hash
        graceful = replace(
            self._stop_request(StopMode.GRACEFUL),
            drain_deadline_utc="2000-01-01T00:00:00Z",
        )
        stopped = self.store.stop(
            graceful, self._stop_capability(StopMode.GRACEFUL), self.authority
        )
        self.oracle.allowed_head = stopped.event_hash
        escalated = self.store.escalate_stop(
            StopEscalationRequest(
                "escalation-1", "escalation-command-1",
                "escalation-event-1", "repo-1", "run-1", graceful.stop_id,
                graceful.event_id, graceful.drain_deadline_utc,
                "GRACEFUL_DEADLINE_EXPIRED",
            ),
            self._stop_escalation_capability(),
            self.authority,
        )
        self.oracle.allowed_head = escalated.event_hash
        connection = sqlite3.connect(self.database_path)
        try:
            accounting = connection.execute(
                "SELECT reservation_id, disposition, charged_units, "
                "settlement_head_hash FROM budget_reservations ORDER BY "
                "reservation_id"
            ).fetchall()
        finally:
            connection.close()
        self.assertEqual(len(accounting), 2)
        self.assertEqual(accounting[0][1], BudgetDisposition.CONSUMED.value)
        self.assertEqual(
            accounting[1],
            (
                "validator-reservation-1",
                BudgetDisposition.UNKNOWN_WORST_CASE_CHARGED.value,
                2,
                settled.settlement_hash,
            ),
        )
        self.assertEqual(self.store.table_counts()["budget_settlements"], 2)
        self.store.load_verified("repo-1")

    def test_t20_history_survives_later_adjustment_release_and_restart(self) -> None:
        request = self.request()
        committed = self._commit_planned_intent(
            request, self.capability, self.authority,
            expected_head="", writer_epoch=1,
        )
        self.oracle.allowed_head = committed.event_hash
        launched = self.store.claim_operation_launch(request, committed)
        self.oracle.allowed_head = launched.event_hash
        graceful = replace(
            self._stop_request(StopMode.GRACEFUL),
            drain_deadline_utc="2000-01-01T00:00:00Z",
        )
        stopped = self.store.stop(
            graceful, self._stop_capability(StopMode.GRACEFUL), self.authority
        )
        self.oracle.allowed_head = stopped.event_hash
        escalated = self.store.escalate_stop(
            StopEscalationRequest(
                "escalation-1", "escalation-command-1",
                "escalation-event-1", "repo-1", "run-1", graceful.stop_id,
                graceful.event_id, graceful.drain_deadline_utc,
                "GRACEFUL_DEADLINE_EXPIRED",
                (StopEscalationSettlement(
                    "reservation-1", "escalation-settlement-event-1", ""
                ),),
            ),
            self._stop_escalation_capability(), self.authority,
        )
        self.oracle.allowed_head = escalated.event_hash
        connection = sqlite3.connect(self.database_path)
        try:
            unknown_hash = connection.execute(
                "SELECT settlement_head_hash FROM budget_reservations WHERE "
                "reservation_id = 'reservation-1'"
            ).fetchone()[0]
        finally:
            connection.close()
        adjustment_request = BudgetSettlementRequest(
            "late-adjustment-event-1", "reservation-1", unknown_hash,
            BudgetDisposition.ADJUSTED, 2, "late-receipt-1",
            "AUTHORITATIVE_LATE_USAGE",
        )
        adjusted = self.store._settle_budget(
            adjustment_request,
            self.authority.issue_settlement_proof(
                "late-adjustment-proof-1", adjustment_request
            ),
            self.authority,
        )
        self.oracle.allowed_head = adjusted.settlement_hash
        late = self._record_signed_effect_observation(
            EffectObservationRequest(
                "late-observation-1", "late-observe-command-1",
                "late-observation-event-1", "repo-1", "run-1", "item-1",
                "effect-1", "attempt-1", "late-receipt-1",
                self.capability.claim_id, "descriptor-digest", 2,
                "late-adjustment-event-1", adjusted.settlement_hash,
            )
        )
        self.oracle.allowed_head = late.event_hash
        connection = sqlite3.connect(self.database_path)
        try:
            plan_id, plan_hash = connection.execute(
                "SELECT plan_id, event_hash FROM validation_plans WHERE "
                "run_id = 'run-1'"
            ).fetchone()
        finally:
            connection.close()
        terminal = self.store.settle_terminal_validation(
            TerminalValidationSettlementRequest(
                "terminal-settlement-1", "terminal-command-1",
                "terminal-event-1", "repo-1", "run-1", "item-1",
                "effect-1", plan_id, "revision-1", "check-1", "PLAN",
                plan_id, plan_hash, "CANCELLED_WITHOUT_START",
            )
        )
        self.assertTrue(terminal.slot_released)
        self.oracle.allowed_head = terminal.event_hash
        reopened = SQLiteStateStore(
            self.database_path, self.oracle, "repo-1"
        )
        reopened.load_verified("repo-1", authority=self.authority)

    def test_t20_recovery_rejects_self_consistent_snapshot_tamper(self) -> None:
        request = self.request()
        committed = self._commit_planned_intent(
            request, self.capability, self.authority,
            expected_head="", writer_epoch=1,
        )
        self.oracle.allowed_head = committed.event_hash
        launched = self.store.claim_operation_launch(request, committed)
        self.oracle.allowed_head = launched.event_hash
        graceful = replace(
            self._stop_request(StopMode.GRACEFUL),
            drain_deadline_utc="2000-01-01T00:00:00Z",
        )
        stopped = self.store.stop(
            graceful, self._stop_capability(StopMode.GRACEFUL), self.authority
        )
        self.oracle.allowed_head = stopped.event_hash
        escalated = self.store.escalate_stop(
            StopEscalationRequest(
                "escalation-1", "escalation-command-1",
                "escalation-event-1", "repo-1", "run-1", graceful.stop_id,
                graceful.event_id, graceful.drain_deadline_utc,
                "GRACEFUL_DEADLINE_EXPIRED",
                (StopEscalationSettlement(
                    "reservation-1", "escalation-settlement-event-1", ""
                ),),
            ),
            self._stop_escalation_capability(), self.authority,
        )
        connection = sqlite3.connect(self.database_path)
        connection.row_factory = sqlite3.Row
        try:
            body = json.loads(
                connection.execute(
                    "SELECT body_json FROM stop_escalations WHERE "
                    "escalation_id = 'escalation-1'"
                ).fetchone()["body_json"]
            )
            body["obligation_snapshot"][0]["activity_id"] = "forged-launch"
            forged_hash = self.store._event_hash(body)
            body_json = json.dumps(
                body, sort_keys=True, separators=(",", ":")
            )
            connection.execute(
                "UPDATE events SET event_hash = ?, body_json = ? WHERE "
                "event_id = 'escalation-event-1'",
                (forged_hash, body_json),
            )
            connection.execute(
                "UPDATE stop_escalations SET event_hash = ?, body_json = ? "
                "WHERE escalation_id = 'escalation-1'",
                (forged_hash, body_json),
            )
            connection.execute(
                "UPDATE command_outcomes SET event_hash = ? WHERE "
                "command_id = 'escalation-command-1'",
                (forged_hash,),
            )
            connection.execute(
                "UPDATE runs SET head_hash = ? WHERE run_id = 'run-1'",
                (forged_hash,),
            )
            connection.execute(
                "UPDATE repositories SET catalog_head = ? WHERE "
                "repository_id = 'repo-1'",
                (forged_hash,),
            )
            connection.commit()
        finally:
            connection.close()
        self.oracle.allowed_head = forged_hash
        with self.assertRaisesRegex(
            StorageIntegrityError, "obligation snapshot"
        ):
            self.store.load_verified("repo-1")

    def test_t20_recovery_rejects_self_consistent_item_retarget(self) -> None:
        request = self.request()
        committed = self._commit_planned_intent(
            request, self.capability, self.authority,
            expected_head="", writer_epoch=1,
        )
        self.oracle.allowed_head = committed.event_hash
        launched = self.store.claim_operation_launch(request, committed)
        self.oracle.allowed_head = launched.event_hash
        graceful = replace(
            self._stop_request(StopMode.GRACEFUL),
            drain_deadline_utc="2000-01-01T00:00:00Z",
        )
        stopped = self.store.stop(
            graceful, self._stop_capability(StopMode.GRACEFUL), self.authority
        )
        self.oracle.allowed_head = stopped.event_hash
        self.store.escalate_stop(
            StopEscalationRequest(
                "escalation-1", "escalation-command-1",
                "escalation-event-1", "repo-1", "run-1", graceful.stop_id,
                graceful.event_id, graceful.drain_deadline_utc,
                "GRACEFUL_DEADLINE_EXPIRED",
                (StopEscalationSettlement(
                    "reservation-1", "escalation-settlement-event-1", ""
                ),),
            ),
            self._stop_escalation_capability(), self.authority,
        )
        connection = sqlite3.connect(self.database_path)
        connection.row_factory = sqlite3.Row
        try:
            body = json.loads(
                connection.execute(
                    "SELECT body_json FROM stop_escalations WHERE "
                    "escalation_id = 'escalation-1'"
                ).fetchone()["body_json"]
            )
            body["item_id"] = "forged-item"
            forged_hash = self.store._event_hash(body)
            body_json = json.dumps(
                body, sort_keys=True, separators=(",", ":")
            )
            connection.execute(
                "UPDATE events SET item_id = ?, event_hash = ?, "
                "body_json = ? WHERE event_id = 'escalation-event-1'",
                ("forged-item", forged_hash, body_json),
            )
            connection.execute(
                "UPDATE stop_escalations SET item_id = ?, event_hash = ?, "
                "body_json = ? WHERE escalation_id = 'escalation-1'",
                ("forged-item", forged_hash, body_json),
            )
            connection.execute(
                "UPDATE command_outcomes SET event_hash = ? WHERE "
                "command_id = 'escalation-command-1'",
                (forged_hash,),
            )
            connection.execute(
                "UPDATE runs SET head_hash = ? WHERE run_id = 'run-1'",
                (forged_hash,),
            )
            connection.execute(
                "UPDATE repositories SET catalog_head = ? WHERE "
                "repository_id = 'repo-1'",
                (forged_hash,),
            )
            connection.commit()
        finally:
            connection.close()
        self.oracle.allowed_head = forged_hash
        with self.assertRaisesRegex(
            StorageIntegrityError, "source binding"
        ):
            self.store.load_verified("repo-1")

    def test_t20_rejects_incomplete_stale_and_forged_requests(self) -> None:
        request = self.request()
        committed = self._commit_planned_intent(
            request, self.capability, self.authority,
            expected_head="", writer_epoch=1,
        )
        self.oracle.allowed_head = committed.event_hash
        launched = self.store.claim_operation_launch(request, committed)
        self.oracle.allowed_head = launched.event_hash
        graceful = replace(
            self._stop_request(StopMode.GRACEFUL),
            drain_deadline_utc="2000-01-01T00:00:00Z",
        )
        stopped = self.store.stop(
            graceful, self._stop_capability(StopMode.GRACEFUL), self.authority
        )
        self.oracle.allowed_head = stopped.event_hash
        base = StopEscalationRequest(
            "escalation-1", "escalation-command-1", "escalation-event-1",
            "repo-1", "run-1", graceful.stop_id, graceful.event_id,
            graceful.drain_deadline_utc, "GRACEFUL_DEADLINE_EXPIRED",
            (StopEscalationSettlement(
                "reservation-1", "escalation-settlement-event-1", ""
            ),),
        )
        capability = self._stop_escalation_capability()
        with self.assertRaisesRegex(DispatchDenied, "exactly cover"):
            self.store.escalate_stop(
                replace(base, unknown_settlements=()),
                capability,
                self.authority,
            )
        with self.assertRaisesRegex(DispatchDenied, "stale"):
            self.store.escalate_stop(
                replace(
                    base,
                    unknown_settlements=(StopEscalationSettlement(
                        "reservation-1", "escalation-settlement-event-1",
                        "stale-hash",
                    ),),
                ),
                capability,
                self.authority,
            )
        with self.assertRaisesRegex(DispatchDenied, "was not issued here"):
            self.store.escalate_stop(
                base,
                replace(capability, issuer_mac="forged"),
                self.authority,
            )
        with self.assertRaisesRegex(DispatchDenied, "deadline binding"):
            self.store.escalate_stop(
                replace(
                    base,
                    expected_drain_deadline_utc="1999-01-01T00:00:00Z",
                ),
                capability,
                self.authority,
            )

    def test_t20_rejects_immediate_stop_as_source(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            oracle = MutableFreshnessOracle()
            store = SQLiteStateStore(
                Path(directory) / "state.sqlite3", oracle, "repo-1"
            )
            authority = SyntheticAuthority()
            store._bind_classification_authority(authority)
            effect_grant = SyntheticGrant(
                "grant-x", "repo-1", "effect-x", "attempt-x", "scope-x"
            )
            authority.register(effect_grant)
            effect_capability = authority.claim(*effect_grant.__dict__.values())
            intent = IntentRequest(
                "repo-1", "run-x", "item-x", "command-x", "event-x",
                "effect-x", "descriptor-x", "attempt-x", "permission-x",
                "reservation-x", "budget-x", 1, 2, 5,
            )
            plan = store.accept_plan(
                PlanAcceptanceRequest(
                    "plan-x", "plan-command-x", "plan-event-x", "repo-1",
                    "run-x", "item-x", "effect-x", "revision-x",
                    "descriptor-x", "scope-x", "budget-x", ("check-x",),
                ),
                expected_head="", writer_epoch=1,
            )
            oracle.allowed_head = plan.event_hash
            committed = store.commit_intent(
                intent, effect_capability, authority,
                expected_head=plan.event_hash, writer_epoch=2,
            )
            oracle.allowed_head = committed.event_hash
            launched = store.claim_operation_launch(intent, committed)
            oracle.allowed_head = launched.event_hash
            stop_grant = SyntheticOperatorGrant(
                "stop-grant-x", "repo-1", "run-x", "STOP_IMMEDIATE",
                "stop-scope-x",
            )
            authority.register_operator(stop_grant)
            immediate = StopRequest(
                "stop-x", "stop-command-x", "stop-event-x", "repo-1",
                "run-x", StopMode.IMMEDIATE, "OPERATOR_STOP",
            )
            stopped = store.stop(
                immediate,
                authority.claim_operator(*stop_grant.__dict__.values()),
                authority,
            )
            oracle.allowed_head = stopped.event_hash
            escalation_grant = SyntheticOperatorGrant(
                "escalation-grant-x", "repo-1", "run-x", "STOP_ESCALATE",
                "escalation-scope-x",
            )
            authority.register_operator(escalation_grant)
            with self.assertRaisesRegex(DispatchDenied, "graceful stop"):
                store.escalate_stop(
                    StopEscalationRequest(
                        "escalation-x", "escalation-command-x",
                        "escalation-event-x", "repo-1", "run-x", "stop-x",
                        "stop-event-x", "2000-01-01T00:00:00Z",
                        "GRACEFUL_DEADLINE_EXPIRED",
                        (StopEscalationSettlement(
                            "reservation-x", "escalation-settlement-x", ""
                        ),),
                    ),
                    authority.claim_operator(*escalation_grant.__dict__.values()),
                    authority,
                )

    def test_r_stop_01_t18_closes_applied_pass(self) -> None:
        self._assert_r_stop_01_application_closure(
            verdict="PASS", mode=StopMode.GRACEFUL
        )

    def test_r_stop_01_t19_closes_applied_pass(self) -> None:
        self._assert_r_stop_01_application_closure(
            verdict="PASS", mode=StopMode.IMMEDIATE
        )

    def test_r_stop_01_t18_closes_applied_recoverable_failure(self) -> None:
        self._assert_r_stop_01_application_closure(
            verdict="FAIL", mode=StopMode.GRACEFUL
        )

    def test_r_stop_01_t19_closes_applied_recoverable_failure(self) -> None:
        self._assert_r_stop_01_application_closure(
            verdict="FAIL", mode=StopMode.IMMEDIATE
        )

    def test_r_stop_01_application_closure_crash_replay_is_exactly_once(
        self,
    ) -> None:
        self._record_validator_result(verdict="PASS", only_check=True)
        application_request = ValidationApplicationRequest(
            "application-1", "apply-command-1", "apply-event-1", "repo-1",
            "run-1", "item-1", "effect-1", "revision-1", "check-1",
            "validator-attempt-1", "validator-observation-1",
        )
        with self.assertRaises(InjectedFailure):
            self.store._apply_validator_observation(
                application_request,
                failure_hook=raise_at(
                    "after_validation_application_commit_before_acknowledgement"
                ),
            )
        connection = sqlite3.connect(self.database_path)
        try:
            application_hash = connection.execute(
                "SELECT event_hash FROM validation_applications "
                "WHERE application_id = 'application-1'"
            ).fetchone()[0]
        finally:
            connection.close()
        self.oracle.allowed_head = application_hash
        application_replay = self.store._apply_validator_observation(
            application_request
        )
        self.assertTrue(application_replay.replayed)
        stopped = self.store.stop(
            self._stop_request(), self._stop_capability(StopMode.IMMEDIATE),
            self.authority,
        )
        self.oracle.allowed_head = stopped.event_hash
        request = self._terminal_application_request("PASSED")
        with self.assertRaises(InjectedFailure):
            self.store.settle_terminal_validation(
                request,
                failure_hook=raise_at(
                    "after_terminal_settlement_writes_before_commit"
                ),
            )
        self.assertEqual(
            self.store.table_counts()["terminal_validation_settlements"], 0
        )
        self.assertEqual(self.store.table_counts()["outstanding_slot"], 1)
        with self.assertRaises(InjectedFailure):
            self.store.settle_terminal_validation(
                request,
                failure_hook=raise_at(
                    "after_terminal_settlement_commit_before_acknowledgement"
                ),
            )
        connection = sqlite3.connect(self.database_path)
        try:
            terminal_hash = connection.execute(
                "SELECT event_hash FROM terminal_validation_settlements "
                "WHERE terminal_settlement_id = 'terminal-settlement-1'"
            ).fetchone()[0]
        finally:
            connection.close()
        self.oracle.allowed_head = terminal_hash
        reopened = SQLiteStateStore(
            self.database_path, self.oracle, "repo-1"
        )
        reopened._bind_classification_authority(self.authority)
        replay = reopened.settle_terminal_validation(request)
        self.assertTrue(replay.replayed)
        self.assertTrue(replay.slot_released)
        connection = sqlite3.connect(self.database_path)
        try:
            terminal_events = connection.execute(
                "SELECT COUNT(*) FROM events WHERE "
                "event_kind = 'TERMINAL_VALIDATION_SETTLED'"
            ).fetchone()[0]
            terminal_rows = connection.execute(
                "SELECT COUNT(*) FROM terminal_validation_settlements"
            ).fetchone()[0]
        finally:
            connection.close()
        self.assertEqual((terminal_events, terminal_rows), (1, 1))
        self.assertEqual(reopened.table_counts()["outstanding_slot"], 0)
        reopened.load_verified("repo-1")

    def test_r_stop_01_application_closure_rejects_misbound_sources(
        self,
    ) -> None:
        self._prepare_finalization()
        stopped = self.store.stop(
            self._stop_request(), self._stop_capability(StopMode.IMMEDIATE),
            self.authority,
        )
        self.oracle.allowed_head = stopped.event_hash
        request = self._terminal_application_request("PASSED")
        cases = {
            "application": {"source_id": "application-missing"},
            "hash": {"source_event_hash": "forged-application-hash"},
            "mapping": {"disposition": "FAILED"},
            "attempt": {"validator_attempt_id": "validator-attempt-old"},
            "check": {"check_id": "check-missing"},
        }
        before = self.store.table_counts()
        for name, changes in cases.items():
            with self.subTest(name=name), self.assertRaises(DispatchDenied):
                self.store.settle_terminal_validation(
                    replace(
                        request,
                        terminal_settlement_id=f"terminal-{name}",
                        command_id=f"terminal-command-{name}",
                        event_id=f"terminal-event-{name}",
                        **changes,
                    )
                )
            self.assertEqual(self.store.table_counts(), before)

    def test_r_stop_01_application_closure_requires_complete_accounting(
        self,
    ) -> None:
        self._prepare_finalization()
        stopped = self.store.stop(
            self._stop_request(), self._stop_capability(StopMode.IMMEDIATE),
            self.authority,
        )
        self.oracle.allowed_head = stopped.event_hash
        connection = sqlite3.connect(self.database_path)
        try:
            connection.execute(
                "UPDATE budget_reservations SET disposition = 'RELEASED' "
                "WHERE reservation_id = 'validator-reservation-1'"
            )
            connection.commit()
        finally:
            connection.close()
        with patch.object(self.store, "_verify_projections", return_value=None):
            with self.assertRaisesRegex(
                DispatchDenied, "accounting is not authoritative"
            ):
                self.store.settle_terminal_validation(
                    self._terminal_application_request("PASSED")
                )
        self.assertEqual(
            self.store.table_counts()["terminal_validation_settlements"], 0
        )
        self.assertEqual(self.store.table_counts()["outstanding_slot"], 1)

    def test_r_stop_01_application_closure_rejects_superseded_attempt(
        self,
    ) -> None:
        observation, failed = self._prepare_recoverable_application()
        recovery_request, attestation, parent_event_hash = (
            self._validation_recovery_pair(failed)
        )
        recovered = self.store.resolve_validation_blocker(
            recovery_request, attestation, self.authority
        )
        self.oracle.allowed_head = recovered.event_hash
        successor_request, successor_capability = self._validator_intent(
            replace(observation, event_hash=parent_event_hash),
            suffix="2", check_id="check-1", recovery_id="recovery-1",
        )
        successor = self.store.commit_validator_intent(
            successor_request, successor_capability, self.authority
        )
        self.oracle.allowed_head = successor.event_hash
        stopped = self.store.stop(
            self._stop_request(), self._stop_capability(StopMode.IMMEDIATE),
            self.authority,
        )
        self.oracle.allowed_head = stopped.event_hash

        with self.assertRaisesRegex(DispatchDenied, "current attempt"):
            self.store.settle_terminal_validation(
                self._terminal_application_request("FAILED")
            )
        self.assertEqual(
            self.store.table_counts()["terminal_validation_settlements"], 0
        )
        self.assertEqual(self.store.table_counts()["outstanding_slot"], 1)

    def test_r_stop_01_recovery_rejects_self_consistent_application_tampering(
        self,
    ) -> None:
        self._prepare_finalization()
        stopped = self.store.stop(
            self._stop_request(), self._stop_capability(StopMode.IMMEDIATE),
            self.authority,
        )
        self.oracle.allowed_head = stopped.event_hash
        settled = self.store.settle_terminal_validation(
            self._terminal_application_request("PASSED")
        )
        mutations = {
            "application": ("source_id", "application-missing"),
            "hash": ("source_event_hash", "forged-application-hash"),
            "mapping": ("disposition", "FAILED"),
            "attempt": ("validator_attempt_id", "validator-attempt-old"),
            "check": ("check_id", "check-missing"),
        }
        for name, (field, value) in mutations.items():
            with self.subTest(name=name):
                case_path = (
                    Path(self.temporary_directory.name)
                    / f"terminal-tamper-{name}.sqlite3"
                )
                shutil.copy2(self.database_path, case_path)
                connection = sqlite3.connect(case_path)
                try:
                    body = json.loads(
                        connection.execute(
                            "SELECT body_json FROM events WHERE event_id = ?",
                            (settled.event_id,),
                        ).fetchone()[0]
                    )
                    body[field] = value
                    request_body = {
                        key: body[key]
                        for key in TerminalValidationSettlementRequest.__dataclass_fields__
                    }
                    payload_digest = self.store._event_hash(request_body)
                    obligation_proof_key = self.store._event_hash(
                        {
                            key: value
                            for key, value in request_body.items()
                            if key not in {
                                "terminal_settlement_id", "command_id",
                                "event_id",
                            }
                        }
                    )
                    body["obligation_proof_key"] = obligation_proof_key
                    event_hash = self.store._event_hash(body)
                    body_json = json.dumps(
                        body, sort_keys=True, separators=(",", ":")
                    )
                    connection.execute(
                        "UPDATE events SET event_hash = ?, body_json = ? "
                        "WHERE event_id = ?",
                        (event_hash, body_json, settled.event_id),
                    )
                    connection.execute(
                        f"UPDATE terminal_validation_settlements SET {field} = ?, "
                        "obligation_proof_key = ?, payload_digest = ?, "
                        "event_hash = ?, body_json = ? WHERE "
                        "terminal_settlement_id = ?",
                        (
                            value, obligation_proof_key, payload_digest,
                            event_hash, body_json,
                            settled.terminal_settlement_id,
                        ),
                    )
                    connection.execute(
                        "UPDATE command_outcomes SET payload_digest = ?, "
                        "event_hash = ? WHERE command_id = ?",
                        (payload_digest, event_hash, settled.command_id),
                    )
                    connection.execute(
                        "UPDATE runs SET head_hash = ? WHERE run_id = 'run-1'",
                        (event_hash,),
                    )
                    connection.execute(
                        "UPDATE repositories SET catalog_head = ? "
                        "WHERE repository_id = 'repo-1'",
                        (event_hash,),
                    )
                    connection.commit()
                finally:
                    connection.close()
                self.oracle.allowed_head = event_hash
                with self.assertRaisesRegex(
                    StorageIntegrityError, "terminal validation history"
                ):
                    SQLiteStateStore(
                        case_path, self.oracle, "repo-1"
                    ).load_verified("repo-1", authority=self.authority)

    def test_t16_finalization_is_atomic_replay_safe_and_releases_slot(self) -> None:
        request, attestation = self._prepare_finalization()
        with self.assertRaises(InjectedFailure):
            self.store._finalize_operation(
                request, attestation, self.authority,
                failure_hook=raise_at("after_finalization_writes_before_commit"),
            )
        self.assertEqual(self.store.table_counts()["operation_finalizations"], 0)
        with self.assertRaises(InjectedFailure):
            self.store._finalize_operation(
                request, attestation, self.authority,
                failure_hook=raise_at(
                    "after_finalization_commit_before_acknowledgement"
                ),
            )
        connection = sqlite3.connect(self.database_path)
        try:
            final_hash, event_kind = connection.execute(
                "SELECT f.event_hash, e.event_kind FROM operation_finalizations f "
                "JOIN events e ON e.event_id = f.event_id"
            ).fetchone()
        finally:
            connection.close()
        self.assertEqual(event_kind, "OPERATION_FINALIZED")
        self.oracle.allowed_head = final_hash
        replay = self.store._finalize_operation(
            request, attestation, self.authority
        )
        self.assertTrue(replay.replayed)
        self.assertEqual(replay.resulting_state.value, "COMPLETED")
        semantic_replay = self.store._finalize_operation(
            replace(
                request,
                finalization_id="finalization-retry",
                command_id="finalize-command-retry",
                event_id="finalize-event-retry",
            ),
            attestation,
            self.authority,
        )
        self.assertEqual(semantic_replay, replace(replay, replayed=True))
        self.assertEqual(self.store.table_counts()["operation_finalizations"], 1)
        self.assertEqual(self.store.table_counts()["outstanding_slot"], 0)
        self.store.load_verified("repo-1")
        with self.assertRaisesRegex(StorageIntegrityError, "rebound"):
            self.store._finalize_operation(
                replace(request, event_id="rebound-finalize-event"),
                attestation,
                self.authority,
            )
        with self.assertRaisesRegex(StorageIntegrityError, "reused"):
            self.store._finalize_operation(
                replace(
                    request,
                    finalization_id="another-finalization-retry",
                    command_id="plan-command-1",
                    event_id="another-finalize-event-retry",
                ),
                attestation,
                self.authority,
            )

    def test_t16_accepts_latest_authoritative_adjustment(self) -> None:
        self._prepare_finalization()
        connection = sqlite3.connect(self.database_path)
        try:
            previous_hash = connection.execute(
                "SELECT settlement_head_hash FROM budget_reservations "
                "WHERE reservation_id = 'reservation-1'"
            ).fetchone()[0]
        finally:
            connection.close()
        adjustment = BudgetSettlementRequest(
            "settlement-adjusted", "reservation-1", previous_hash,
            BudgetDisposition.ADJUSTED, 3, "receipt-correction",
            "AUTHORITATIVE_CORRECTION",
        )
        adjusted = self.store._settle_budget(
            adjustment,
            self.authority.issue_settlement_proof(
                "proof-adjusted", adjustment
            ),
            self.authority,
        )
        self.oracle.allowed_head = adjusted.settlement_hash
        request, attestation = self._finalization_request_and_attestation(
            adjusted.settlement_hash
        )

        finalized = self.store._finalize_operation(
            request, attestation, self.authority
        )

        self.assertEqual(finalized.resulting_state.value, "COMPLETED")
        self.assertEqual(self.store.table_counts()["outstanding_slot"], 0)

    def test_t16_late_authoritative_adjustment_does_not_reopen_completion(self) -> None:
        request, attestation = self._prepare_finalization()
        finalized = self.store._finalize_operation(
            request, attestation, self.authority
        )
        self.oracle.allowed_head = finalized.event_hash
        connection = sqlite3.connect(self.database_path)
        try:
            previous_hash = connection.execute(
                "SELECT settlement_head_hash FROM budget_reservations "
                "WHERE reservation_id = 'reservation-1'"
            ).fetchone()[0]
        finally:
            connection.close()
        adjustment = BudgetSettlementRequest(
            "late-settlement-adjusted", "reservation-1", previous_hash,
            BudgetDisposition.ADJUSTED, 3, "late-receipt-correction",
            "AUTHORITATIVE_CORRECTION",
        )
        adjusted = self.store._settle_budget(
            adjustment,
            self.authority.issue_settlement_proof(
                "late-proof-adjusted", adjustment
            ),
            self.authority,
        )
        self.oracle.allowed_head = adjusted.settlement_hash
        self.store.load_verified("repo-1")
        connection = sqlite3.connect(self.database_path)
        try:
            charged_units, lifecycle_state = connection.execute(
                "SELECT b.charged_units, r.lifecycle_state "
                "FROM budget_reservations b JOIN runs r ON r.run_id = b.run_id "
                "WHERE b.reservation_id = 'reservation-1'"
            ).fetchone()
        finally:
            connection.close()
        self.assertEqual(charged_units, 3)
        self.assertEqual(lifecycle_state, "COMPLETED")
        self.assertEqual(self.store.table_counts()["operation_finalizations"], 1)
        self.assertEqual(self.store.table_counts()["outstanding_slot"], 0)

    def test_t16_late_unknown_accounting_recovers_for_correction(self) -> None:
        request, attestation = self._prepare_finalization()
        finalized = self.store._finalize_operation(
            request, attestation, self.authority
        )
        self.oracle.allowed_head = finalized.event_hash
        connection = sqlite3.connect(self.database_path)
        try:
            previous_hash = connection.execute(
                "SELECT settlement_head_hash FROM budget_reservations "
                "WHERE reservation_id = 'reservation-1'"
            ).fetchone()[0]
        finally:
            connection.close()
        unknown = BudgetSettlementRequest(
            "late-unknown", "reservation-1", previous_hash,
            BudgetDisposition.UNKNOWN_WORST_CASE_CHARGED, None,
            "late-unknown-evidence", "ADDITIONAL_LIABILITY_UNKNOWN",
            additional_liability=True,
        )
        unknown_receipt = self.store._settle_budget(
            unknown,
            self.authority.issue_settlement_proof("late-unknown-proof", unknown),
            self.authority,
        )
        self.oracle.allowed_head = unknown_receipt.settlement_hash

        reopened = SQLiteStateStore(
            self.database_path, self.oracle, "repo-1"
        )
        reopened._bind_classification_authority(self.authority)
        reopened.load_verified("repo-1")
        correction = BudgetSettlementRequest(
            "late-correction", "reservation-1",
            unknown_receipt.settlement_hash, BudgetDisposition.ADJUSTED, 3,
            "late-authoritative-evidence", "AUTHORITATIVE_CORRECTION",
        )
        corrected = reopened._settle_budget(
            correction,
            self.authority.issue_settlement_proof(
                "late-correction-proof", correction
            ),
            self.authority,
        )
        self.oracle.allowed_head = corrected.settlement_hash
        reopened.load_verified("repo-1")
        connection = sqlite3.connect(self.database_path)
        try:
            charged_units, uncertainty, lifecycle_state = connection.execute(
                "SELECT b.charged_units, b.uncertainty, r.lifecycle_state "
                "FROM budget_reservations b JOIN runs r ON r.run_id = b.run_id "
                "WHERE b.reservation_id = 'reservation-1'"
            ).fetchone()
        finally:
            connection.close()
        self.assertEqual((charged_units, uncertainty), (3, 0))
        self.assertEqual(lifecycle_state, "COMPLETED")
        self.assertEqual(reopened.table_counts()["operation_finalizations"], 1)
        self.assertEqual(reopened.table_counts()["outstanding_slot"], 0)
        self.assertEqual(reopened.table_counts()["dispatch_fences"], 0)

    def test_f21_process_termination_keeps_fence_clearance_atomic(self) -> None:
        request, attestation = self._prepare_finalization()
        finalized = self.store._finalize_operation(
            request, attestation, self.authority
        )
        self.oracle.allowed_head = finalized.event_hash
        connection = sqlite3.connect(self.database_path)
        try:
            previous_hash = connection.execute(
                "SELECT settlement_head_hash FROM budget_reservations "
                "WHERE reservation_id = 'reservation-1'"
            ).fetchone()[0]
        finally:
            connection.close()
        unknown = BudgetSettlementRequest(
            "late-unknown", "reservation-1", previous_hash,
            BudgetDisposition.UNKNOWN_WORST_CASE_CHARGED, None,
            "late-unknown-evidence", "ADDITIONAL_LIABILITY_UNKNOWN",
            additional_liability=True,
        )
        unknown_receipt = self.store._settle_budget(
            unknown,
            self.authority.issue_settlement_proof("late-unknown-proof", unknown),
            self.authority,
        )
        self.oracle.allowed_head = unknown_receipt.settlement_hash
        correction = BudgetSettlementRequest(
            "late-correction", "reservation-1",
            unknown_receipt.settlement_hash, BudgetDisposition.ADJUSTED, 3,
            "late-authoritative-evidence", "AUTHORITATIVE_CORRECTION",
        )
        context = multiprocessing.get_context("spawn")
        issuer_key = self.authority._issuer_key

        for stage in (
            "after_settlement_writes_before_commit",
            "after_settlement_commit_before_acknowledgement",
        ):
            ready = context.Event()
            process = context.Process(
                target=_settle_until_terminated,
                args=(
                    self.database_path,
                    issuer_key,
                    unknown_receipt.settlement_hash,
                    correction,
                    stage,
                    ready,
                ),
            )
            process.start()
            try:
                self.assertTrue(
                    ready.wait(10),
                    f"child did not reach {stage}",
                )
            finally:
                process.terminate()
                process.join(10)
                if process.is_alive():
                    process.kill()
                    process.join(10)
            self.assertFalse(process.is_alive())

            connection = sqlite3.connect(self.database_path)
            try:
                correction_row = connection.execute(
                    "SELECT settlement_hash FROM budget_settlements "
                    "WHERE settlement_event_id = 'late-correction'"
                ).fetchone()
                fence_ids = {
                    row[0] for row in connection.execute(
                        "SELECT fence_id FROM dispatch_fences"
                    )
                }
            finally:
                connection.close()
            if stage == "after_settlement_writes_before_commit":
                self.assertIsNone(correction_row)
                self.assertEqual(
                    fence_ids, {"additional-liability:late-unknown"}
                )
            else:
                self.assertIsNotNone(correction_row)
                self.assertEqual(fence_ids, set())

        self.oracle.allowed_head = correction_row[0]
        replay = self.store._settle_budget(
            correction,
            self.authority.issue_settlement_proof(
                "replay-proof", correction
            ),
            self.authority,
        )
        self.assertTrue(replay.replayed)
        self.store.load_verified("repo-1")

    def test_t16_accepts_zero_aggregate_gates_with_pass_attestation(self) -> None:
        request, attestation = self._prepare_finalization(aggregate_gate_ids=())
        finalized = self.store._finalize_operation(
            request, attestation, self.authority
        )
        self.assertEqual(finalized.resulting_state.value, "COMPLETED")
        self.assertEqual(self.store.table_counts()["outstanding_slot"], 0)

    def test_t16_waits_for_checks_and_aggregate_attestation_then_finalizes_once(self) -> None:
        observation = self._record_effect_observation(
            ("check-1", "check-2"), ("aggregate-release",)
        )
        self._record_validator_result_for(observation, suffix="1")
        first = self.store._apply_validator_observation(
            ValidationApplicationRequest(
                "application-1", "apply-command-1", "apply-event-1", "repo-1",
                "run-1", "item-1", "effect-1", "revision-1", "check-1",
                "validator-attempt-1", "validator-observation-1",
            )
        )
        self.oracle.allowed_head = first.event_hash
        self.assertEqual(first.resulting_state.value, "VALIDATING")
        with self.assertRaisesRegex(DispatchDenied, "BLOCKED/FINALIZING"):
            request, attestation = self._finalization_request_and_attestation(
                first.event_hash
            )
            self.store._finalize_operation(
                request, attestation, self.authority
            )
        self._record_validator_result_for(observation, suffix="2")
        second = self.store._apply_validator_observation(
            ValidationApplicationRequest(
                "application-2", "apply-command-2", "apply-event-2", "repo-1",
                "run-1", "item-1", "effect-1", "revision-1", "check-2",
                "validator-attempt-2", "validator-observation-2",
            )
        )
        self.oracle.allowed_head = second.event_hash
        self.assertEqual(second.resulting_state.value, "BLOCKED")
        request, attestation = self._finalization_request_and_attestation(
            second.event_hash
        )
        with self.assertRaisesRegex(DispatchDenied, "attestation is unavailable"):
            self.store._finalize_operation(
                request, None, self.authority
            )
        self.assertEqual(self.store.table_counts()["outstanding_slot"], 1)
        finalized = self.store._finalize_operation(
            request, attestation, self.authority
        )
        self.assertEqual(finalized.resulting_state.value, "COMPLETED")
        self.assertEqual(self.store.table_counts()["operation_finalizations"], 1)

    def test_t16_denies_stale_head_attestation_and_slot_rebinding(self) -> None:
        request, attestation = self._prepare_finalization()
        with self.assertRaisesRegex(ValueError, "generation must be positive"):
            self.store._finalize_operation(
                replace(request, expected_slot_generation=True),
                attestation,
                self.authority,
            )
        stale = self.authority.issue_finalization_attestation(
            "attestation-stale", "repo-1", "run-1", "item-1", "effect-1",
            "plan-1", attestation.plan_event_hash, "revision-1", "stale-head",
            attestation.finalization_key, attestation.gate_set_digest,
            "attempt-1", 1,
        )
        with self.assertRaisesRegex(DispatchDenied, "current durable state"):
            self.store._finalize_operation(request, stale, self.authority)
        rebound_request = replace(
            request, expected_slot_attempt_id="another-attempt"
        )
        rebound = self.authority.issue_finalization_attestation(
            "attestation-rebound", "repo-1", "run-1", "item-1", "effect-1",
            "plan-1", attestation.plan_event_hash, "revision-1",
            attestation.evaluated_run_head, attestation.finalization_key,
            attestation.gate_set_digest, "another-attempt", 1,
        )
        with patch.object(
            self.store, "_accounting_closure_error", return_value=None
        ):
            with self.assertRaisesRegex(DispatchDenied, "own the slot"):
                self.store._finalize_operation(
                    rebound_request, rebound, self.authority
                )

    def test_t16_denies_forged_rebound_and_unsupported_attestations(self) -> None:
        request, attestation = self._prepare_finalization()
        with self.assertRaisesRegex(DispatchDenied, "not issued"):
            self.store._finalize_operation(
                request,
                replace(attestation, issuer_mac="0" * 64),
                self.authority,
            )
        rebound_values = {
            "repository_id": "repo-other",
            "run_id": "run-other",
            "item_id": "item-other",
            "logical_effect_id": "effect-other",
            "plan_id": "plan-other",
            "plan_event_hash": "plan-hash-other",
            "revision_digest": "revision-other",
            "evaluated_run_head": "run-head-other",
            "finalization_key": "finalization-key-other",
            "gate_set_digest": "gate-digest-other",
            "slot_attempt_id": "attempt-other",
            "slot_generation": 2,
        }
        for field, value in rebound_values.items():
            with self.subTest(field=field):
                rebound = self._reissue_finalization_attestation(
                    attestation,
                    attestation_id=f"attestation-{field}",
                    **{field: value},
                )
                with self.assertRaisesRegex(
                    DispatchDenied, "current durable state"
                ):
                    self.store._finalize_operation(
                        request, rebound, self.authority
                    )
        for field, value in (
            ("verdict", "FAIL"),
            ("policy_id", "unsupported-policy"),
            ("policy_version", "unsupported-version"),
        ):
            with self.subTest(field=field):
                with self.assertRaises(ValueError):
                    self._reissue_finalization_attestation(
                        attestation, **{field: value}
                    )
        other_authority = SyntheticAuthority(b"o" * 32)
        other_attestation = other_authority.issue_finalization_attestation(
            **{
                name: getattr(attestation, name)
                for name in attestation.__dataclass_fields__
                if name != "issuer_mac"
            }
        )
        with self.assertRaisesRegex(DispatchDenied, "not issued"):
            self.store._finalize_operation(
                request, other_attestation, self.authority
            )
        self.assertEqual(self.store.table_counts()["outstanding_slot"], 1)
        self.assertEqual(self.store.table_counts()["operation_finalizations"], 0)

    def test_t16_denies_event_derived_budget_fence(self) -> None:
        self._prepare_finalization()
        connection = sqlite3.connect(self.database_path)
        try:
            previous_settlement_hash = connection.execute(
                "SELECT settlement_head_hash FROM budget_reservations "
                "WHERE reservation_id = 'reservation-1'"
            ).fetchone()[0]
        finally:
            connection.close()
        settlement_request = BudgetSettlementRequest(
            "settlement-fence", "reservation-1",
            previous_settlement_hash, BudgetDisposition.ADJUSTED, 11,
            "receipt-reconciled", "USAGE_RECONCILED",
        )
        settlement = self.store._settle_budget(
            settlement_request,
            self.authority.issue_settlement_proof(
                "proof-reconciled", settlement_request,
            ),
            self.authority,
        )
        self.oracle.allowed_head = settlement.settlement_hash
        request, attestation = self._finalization_request_and_attestation(
            settlement.settlement_hash
        )
        with self.assertRaisesRegex(DispatchDenied, "active dispatch fence"):
            self.store._finalize_operation(request, attestation, self.authority)
        self.assertEqual(self.store.table_counts()["outstanding_slot"], 1)

    def test_t16_final_effect_observation_must_bind_slot_attempt(self) -> None:
        request, attestation = self._prepare_finalization()
        connection = sqlite3.connect(self.database_path)
        try:
            connection.execute(
                "UPDATE effect_observations SET attempt_id = 'other-attempt'"
            )
            connection.commit()
        finally:
            connection.close()
        with patch.object(self.store, "_verify_projections"):
            with self.assertRaisesRegex(
                DispatchDenied, "final effect observation"
            ):
                self.store._finalize_operation(
                    request, attestation, self.authority
                )

    def test_t16_denies_defense_in_depth_active_validator(self) -> None:
        request, attestation = self._prepare_finalization()
        connection = sqlite3.connect(self.database_path)
        try:
            connection.execute(
                "UPDATE validator_intents SET status = 'ACTIVE'"
            )
            connection.commit()
        finally:
            connection.close()
        with patch.object(self.store, "_verify_projections"):
            with self.assertRaisesRegex(DispatchDenied, "validator activity"):
                self.store._finalize_operation(
                    request, attestation, self.authority
                )

    def test_t16_denies_defense_in_depth_unsettled_accounting(self) -> None:
        request, attestation = self._prepare_finalization()
        for field, value in (
            ("held_units", 1),
            ("uncertainty", 1),
            ("disposition", "RESERVED"),
            ("disposition", "RELEASED"),
            ("charged_units", 3),
        ):
            with self.subTest(field=field):
                connection = sqlite3.connect(self.database_path)
                try:
                    connection.execute(
                        f"UPDATE budget_reservations SET {field} = ? "
                        "WHERE reservation_id = 'reservation-1'",
                        (value,),
                    )
                    connection.commit()
                finally:
                    connection.close()
                with patch.object(self.store, "_verify_projections"):
                    with self.assertRaisesRegex(
                        DispatchDenied, "accounting remains unsettled"
                    ):
                        self.store._finalize_operation(
                            request, attestation, self.authority
                        )
                connection = sqlite3.connect(self.database_path)
                try:
                    connection.execute(
                        "UPDATE budget_reservations SET held_units = 0, "
                        "uncertainty = 0, disposition = 'CONSUMED', "
                        "charged_units = 2 "
                        "WHERE reservation_id = 'reservation-1'"
                    )
                    connection.commit()
                finally:
                    connection.close()

    def test_t16_denies_released_validator_accounting(self) -> None:
        request, attestation = self._prepare_finalization()
        connection = sqlite3.connect(self.database_path)
        try:
            connection.execute(
                "UPDATE budget_reservations SET disposition = 'RELEASED' "
                "WHERE reservation_id = 'validator-reservation-1'"
            )
            connection.commit()
        finally:
            connection.close()

        with patch.object(self.store, "_verify_projections"):
            with self.assertRaisesRegex(
                DispatchDenied, "accounting remains unsettled"
            ):
                self.store._finalize_operation(
                    request, attestation, self.authority
                )
        self.assertEqual(self.store.table_counts()["outstanding_slot"], 1)

    def test_t16_denies_missing_final_effect_observation(self) -> None:
        request, attestation = self._prepare_finalization()
        connection = sqlite3.connect(self.database_path)
        try:
            connection.execute("DELETE FROM effect_observations")
            connection.commit()
        finally:
            connection.close()
        with patch.object(self.store, "_verify_projections"):
            with self.assertRaisesRegex(
                DispatchDenied, "final effect observation"
            ):
                self.store._finalize_operation(
                    request, attestation, self.authority
                )

    def test_t16_freshness_denial_leaves_finalization_state_unchanged(self) -> None:
        request, attestation = self._prepare_finalization()
        before = self.store.table_counts()
        self.oracle.allowed_head = "independently-stale"
        with self.assertRaisesRegex(DispatchDenied, "freshness proof"):
            self.store._finalize_operation(request, attestation, self.authority)
        after = self.store.table_counts()
        self.assertEqual(after, before)
        connection = sqlite3.connect(self.database_path)
        try:
            state = connection.execute(
                "SELECT lifecycle_state, continuation_cursor FROM runs "
                "WHERE run_id = 'run-1'"
            ).fetchone()
        finally:
            connection.close()
        self.assertEqual(state, ("BLOCKED", "FINALIZING"))
        self.assertEqual(after["outstanding_slot"], 1)

    def test_t16_recovery_rejects_finalization_state_tampering(self) -> None:
        request, attestation = self._prepare_finalization()
        finalized = self.store._finalize_operation(
            request, attestation, self.authority
        )
        self.oracle.allowed_head = finalized.event_hash
        mutations = {
            "deleted-projection": "DELETE FROM operation_finalizations",
            "changed-projection": (
                "UPDATE operation_finalizations "
                "SET attestation_digest = 'tampered'"
            ),
            "changed-projection-body": (
                "UPDATE operation_finalizations SET body_json = '{}'"
            ),
            "released-terminal-accounting": (
                "UPDATE budget_reservations SET disposition = 'RELEASED' "
                "WHERE reservation_id = 'reservation-1'"
            ),
            "restored-cursor": (
                "UPDATE runs SET continuation_cursor = 'FINALIZING' "
                "WHERE run_id = 'run-1'"
            ),
            "resurrected-slot": (
                "INSERT INTO outstanding_slot (singleton, repository_id, "
                "run_id, logical_effect_id, attempt_id, generation, "
                "origin_kind, origin_id) VALUES "
                "(1, 'repo-1', 'run-1', 'effect-1', 'attempt-1', 1, "
                "'EXECUTION_INTENT', 'attempt-1')"
            ),
            "changed-event": (
                "UPDATE events SET body_json = '{}' "
                "WHERE event_kind = 'OPERATION_FINALIZED'"
            ),
        }
        for name, statement in mutations.items():
            with self.subTest(name=name):
                case_path = Path(self.temporary_directory.name) / f"{name}.sqlite3"
                shutil.copy2(self.database_path, case_path)
                connection = sqlite3.connect(case_path)
                try:
                    connection.execute(statement)
                    connection.commit()
                finally:
                    connection.close()
                with self.assertRaises(StorageIntegrityError):
                    SQLiteStateStore(
                        case_path, self.oracle, "repo-1"
                    ).load_verified("repo-1", authority=self.authority)

    def test_t16_recovery_rejects_self_consistent_unsigned_finalization(self) -> None:
        request, attestation = self._prepare_finalization()
        finalized = self.store._finalize_operation(
            request, attestation, self.authority
        )
        connection = sqlite3.connect(self.database_path)
        try:
            body = json.loads(
                connection.execute(
                    "SELECT body_json FROM events WHERE event_id = ?",
                    (request.event_id,),
                ).fetchone()[0]
            )
            body["attestation_evidence"]["issuer_mac"] = "0" * 64
            body["attestation_digest"] = self.store._event_hash(
                body["attestation_evidence"]
            )
            event_hash = self.store._event_hash(body)
            body_json = json.dumps(
                body, sort_keys=True, separators=(",", ":")
            )
            connection.execute(
                "UPDATE events SET event_hash = ?, body_json = ? WHERE event_id = ?",
                (event_hash, body_json, request.event_id),
            )
            connection.execute(
                "UPDATE operation_finalizations SET attestation_digest = ?, "
                "event_hash = ?, body_json = ? WHERE finalization_id = ?",
                (
                    body["attestation_digest"], event_hash, body_json,
                    request.finalization_id,
                ),
            )
            connection.execute(
                "UPDATE command_outcomes SET event_hash = ? WHERE command_id = ?",
                (event_hash, request.command_id),
            )
            connection.execute(
                "UPDATE runs SET head_hash = ? WHERE run_id = ?",
                (event_hash, request.run_id),
            )
            connection.execute(
                "UPDATE repositories SET catalog_head = ? WHERE repository_id = ?",
                (event_hash, request.repository_id),
            )
            connection.commit()
        finally:
            connection.close()
        self.oracle.allowed_head = event_hash

        with self.assertRaisesRegex(
            StorageIntegrityError, "finalization attestation"
        ):
            self.store.load_verified("repo-1", authority=self.authority)

    def test_t16_recovery_rejects_accepted_plan_pin_tampering(self) -> None:
        self._prepare_finalization(aggregate_gate_ids=("aggregate-release",))
        mutations = {
            "effect-descriptor": ("effect_descriptor_digest", "tampered"),
            "permission-scope": ("permission_scope_digest", "tampered"),
            "budget-policy": ("budget_policy_digest", "tampered"),
            "gate-set": (
                "aggregate_gate_ids_json", '["aggregate-tampered"]'
            ),
            "gate-digest": ("gate_set_digest", "tampered"),
            "policy-id": ("finalization_policy_id", "tampered"),
            "policy-version": ("finalization_policy_version", "tampered"),
            "issuer": ("finalization_issuer_fingerprint", "tampered"),
        }
        for name, (column, value) in mutations.items():
            with self.subTest(name=name):
                case_path = (
                    Path(self.temporary_directory.name) / f"plan-{name}.sqlite3"
                )
                shutil.copy2(self.database_path, case_path)
                connection = sqlite3.connect(case_path)
                try:
                    connection.execute(
                        f"UPDATE validation_plans SET {column} = ? "
                        "WHERE plan_id = 'plan-1'",
                        (value,),
                    )
                    connection.commit()
                finally:
                    connection.close()
                with self.assertRaisesRegex(
                    StorageIntegrityError, "validation-plan projection"
                ):
                    SQLiteStateStore(
                        case_path, self.oracle, "repo-1"
                    ).load_verified("repo-1", authority=self.authority)

    def test_c05_denies_fail_without_trusted_classification(self) -> None:
        self._record_validator_result(verdict="FAIL")
        with self.assertRaisesRegex(DispatchDenied, "trusted failure classification"):
            self.store._apply_validator_observation(
                ValidationApplicationRequest(
                    "application-1", "apply-command-1", "apply-event-1",
                    "repo-1", "run-1", "item-1", "effect-1", "revision-1",
                    "check-1", "validator-attempt-1",
                    "validator-observation-1",
                ),
            )
        self.assertEqual(self.store.table_counts()["validation_applications"], 0)

    def test_c05_recoverable_failure_blocks_and_retains_slot(self) -> None:
        observation = self._record_validator_result(
            verdict="FAIL", only_check=True
        )
        classification = self._classification(observation, "RECOVERABLE")
        applied = self.store._apply_validator_observation(
            ValidationApplicationRequest(
                "application-1", "apply-command-1", "apply-event-1",
                "repo-1", "run-1", "item-1", "effect-1", "revision-1",
                "check-1", "validator-attempt-1", "validator-observation-1",
            ),
            classification=classification,
        )
        self.oracle.allowed_head = applied.event_hash
        self.assertEqual(applied.resulting_state.value, "BLOCKED")
        self.assertEqual(self.store.table_counts()["outstanding_slot"], 1)
        self.store.load_verified("repo-1")

    def test_t16_recovery_authorizes_exactly_one_t27_successor(self) -> None:
        observation, failed = self._prepare_recoverable_application()
        recovery_request, attestation, parent_event_hash = (
            self._validation_recovery_pair(failed)
        )
        recovered = self.store.resolve_validation_blocker(
            recovery_request, attestation, self.authority
        )
        self.oracle.allowed_head = recovered.event_hash
        retry_request, retry_capability = self._validator_intent(
            replace(observation, event_hash=parent_event_hash),
            suffix="2",
            check_id="check-1",
            recovery_id="recovery-1",
        )
        retry = self.store.commit_validator_intent(
            retry_request, retry_capability, self.authority
        )
        self.oracle.allowed_head = retry.event_hash

        self.assertEqual(self.store.table_counts()["validation_recoveries"], 1)
        self.store.load_verified("repo-1")
        duplicate_request, duplicate_capability = self._validator_intent(
            replace(observation, event_hash=parent_event_hash),
            suffix="3",
            check_id="check-1",
            validator_attempt_id="validator-attempt-2",
            recovery_id="recovery-1",
        )
        with self.assertRaisesRegex(DispatchDenied, "not current"):
            self.store.commit_validator_intent(
                duplicate_request,
                duplicate_capability,
                self.authority,
            )
        settlement_request = BudgetSettlementRequest(
            "validator-settlement-2", "validator-reservation-2", "",
            BudgetDisposition.CONSUMED, 1, "validator-result-2",
            "VALIDATOR_USAGE_REPORTED",
        )
        settlement = self.store._settle_budget(
            settlement_request,
            self.authority.issue_settlement_proof(
                "validator-proof-2", settlement_request
            ),
            self.authority,
        )
        self.oracle.allowed_head = settlement.settlement_hash
        self._record_validator_cessation_for(
            suffix="2", result_available=True, check_id="check-1"
        )
        passed_observation = self.store._record_validator_observation(
            ValidatorObservationRequest(
                "validator-observation-2", "validator-observe-command-2",
                "validator-observation-event-2", "repo-1", "run-1",
                "item-1", "effect-1", "validator-intent-2",
                "validator-attempt-2", "validator-result-2",
                retry_capability.claim_id, "revision-1", "check-1",
                "input-1", "result-digest-2", "PASS", 1,
                "validator-settlement-2", settlement.settlement_hash,
            )
        )
        self.oracle.allowed_head = passed_observation.event_hash
        passed = self.store._apply_validator_observation(
            ValidationApplicationRequest(
                "application-2", "apply-command-2", "apply-event-2",
                "repo-1", "run-1", "item-1", "effect-1", "revision-1",
                "check-1", "validator-attempt-2", "validator-observation-2",
            )
        )
        self.oracle.allowed_head = passed.event_hash
        finalization_request, finalization_attestation = (
            self._finalization_request_and_attestation(passed.event_hash)
        )
        finalized = self.store._finalize_operation(
            finalization_request, finalization_attestation, self.authority
        )
        self.oracle.allowed_head = finalized.event_hash

        self.assertEqual(finalized.resulting_state.value, "COMPLETED")
        self.assertEqual(self.store.table_counts()["validation_applications"], 2)
        SQLiteStateStore(
            self.database_path, self.oracle, "repo-1"
        ).load_verified("repo-1", authority=self.authority)

    def test_t16_recovery_is_atomic_replay_safe_and_rejects_rebinding(self) -> None:
        _, failed = self._prepare_recoverable_application()
        request, attestation, _ = self._validation_recovery_pair(failed)
        with self.assertRaises(InjectedFailure):
            self.store.resolve_validation_blocker(
                request, attestation, self.authority,
                failure_hook=raise_at(
                    "after_validation_recovery_writes_before_commit"
                ),
            )
        self.assertEqual(self.store.table_counts()["validation_recoveries"], 0)
        self.assertEqual(self.store.load_run_lifecycle("run-1").value, "BLOCKED")

        with self.assertRaises(InjectedFailure):
            self.store.resolve_validation_blocker(
                request, attestation, self.authority,
                failure_hook=raise_at(
                    "after_validation_recovery_commit_before_acknowledgement"
                ),
            )
        connection = sqlite3.connect(self.database_path)
        try:
            recovery_hash = connection.execute(
                "SELECT event_hash FROM validation_recoveries "
                "WHERE recovery_id = 'recovery-1'"
            ).fetchone()[0]
        finally:
            connection.close()
        self.oracle.allowed_head = recovery_hash
        replay = self.store.resolve_validation_blocker(
            request, attestation, self.authority
        )
        self.assertTrue(replay.replayed)
        with self.assertRaisesRegex(StorageIntegrityError, "was rebound"):
            self.store.resolve_validation_blocker(
                replace(
                    request,
                    remediation_evidence_digest="different-remediation",
                ),
                attestation,
                self.authority,
            )
        self.store.load_verified("repo-1")

    def test_t16_recovery_rejects_stale_or_forged_attestation(self) -> None:
        _, failed = self._prepare_recoverable_application()
        stale_request, stale_attestation, _ = self._validation_recovery_pair(
            failed, expected_run_head="stale-run-head"
        )
        with self.assertRaisesRegex(DispatchDenied, "run head is stale"):
            self.store.resolve_validation_blocker(
                stale_request, stale_attestation, self.authority
            )
        request, attestation, _ = self._validation_recovery_pair(failed)
        forged = replace(
            attestation, remediation_evidence_digest="forged-remediation"
        )
        with self.assertRaisesRegex(DispatchDenied, "was not issued here"):
            self.store.resolve_validation_blocker(
                request, forged, self.authority
            )
        self.assertEqual(self.store.table_counts()["validation_recoveries"], 0)

    def test_t16_recovery_rejects_self_consistent_unsigned_blocker_recovery(
        self,
    ) -> None:
        _, failed = self._prepare_recoverable_application()
        request, attestation, _ = self._validation_recovery_pair(failed)
        recovered = self.store.resolve_validation_blocker(
            request, attestation, self.authority
        )
        connection = sqlite3.connect(self.database_path)
        try:
            body = json.loads(
                connection.execute(
                    "SELECT body_json FROM events WHERE event_id = ?",
                    (recovered.event_id,),
                ).fetchone()[0]
            )
            body["attestation_evidence"]["issuer_mac"] = "0" * 64
            body["attestation_digest"] = self.store._event_hash(
                body["attestation_evidence"]
            )
            event_hash = self.store._event_hash(body)
            body_json = json.dumps(
                body, sort_keys=True, separators=(",", ":")
            )
            connection.execute(
                "UPDATE events SET event_hash = ?, body_json = ? WHERE event_id = ?",
                (event_hash, body_json, recovered.event_id),
            )
            connection.execute(
                "UPDATE validation_recoveries SET attestation_digest = ?, "
                "event_hash = ?, body_json = ? WHERE recovery_id = ?",
                (
                    body["attestation_digest"], event_hash, body_json,
                    recovered.recovery_id,
                ),
            )
            connection.execute(
                "UPDATE command_outcomes SET event_hash = ? WHERE command_id = ?",
                (event_hash, recovered.command_id),
            )
            connection.execute(
                "UPDATE runs SET head_hash = ? WHERE run_id = ?",
                (event_hash, request.run_id),
            )
            connection.execute(
                "UPDATE repositories SET catalog_head = ? WHERE repository_id = ?",
                (event_hash, request.repository_id),
            )
            connection.commit()
        finally:
            connection.close()
        self.oracle.allowed_head = event_hash

        with self.assertRaisesRegex(
            StorageIntegrityError, "validation recovery attestation"
        ):
            self.store.load_verified("repo-1", authority=self.authority)

    def test_t27_retry_requires_current_exact_recovery(self) -> None:
        observation, failed = self._prepare_recoverable_application()
        recovery_request, attestation, parent_event_hash = (
            self._validation_recovery_pair(failed)
        )
        missing_request, missing_capability = self._validator_intent(
            replace(observation, event_hash=parent_event_hash),
            suffix="2", check_id="check-1",
        )
        with self.assertRaisesRegex(DispatchDenied, "durable VALIDATING"):
            self.store.commit_validator_intent(
                missing_request, missing_capability, self.authority
            )
        recovered = self.store.resolve_validation_blocker(
            recovery_request, attestation, self.authority
        )
        self.oracle.allowed_head = recovered.event_hash
        wrong_request, wrong_capability = self._validator_intent(
            replace(observation, event_hash=parent_event_hash),
            suffix="3", check_id="check-1",
            validator_attempt_id="validator-attempt-2",
            recovery_id="wrong-recovery",
        )
        with self.assertRaisesRegex(DispatchDenied, "does not bind"):
            self.store.commit_validator_intent(
                wrong_request, wrong_capability, self.authority
            )
        self.assertEqual(self.store.table_counts()["validator_intents"], 1)

    def test_t27_denies_retry_of_already_passed_check(self) -> None:
        effect_observation = self._record_effect_observation()
        validator_observation = self._record_validator_result_for(
            effect_observation, suffix="1"
        )
        passed = self.store._apply_validator_observation(
            ValidationApplicationRequest(
                "application-1", "apply-command-1", "apply-event-1",
                "repo-1", "run-1", "item-1", "effect-1", "revision-1",
                "check-1", "validator-attempt-1", "validator-observation-1",
            )
        )
        self.oracle.allowed_head = passed.event_hash
        request, capability = self._validator_intent(
            effect_observation, suffix="3", check_id="check-1"
        )
        with self.assertRaisesRegex(DispatchDenied, "already passed"):
            self.store.commit_validator_intent(
                request, capability, self.authority
            )

    def test_t27_validator_contact_rechecks_recovery_binding(self) -> None:
        observation, failed = self._prepare_recoverable_application()
        recovery_request, attestation, parent_event_hash = (
            self._validation_recovery_pair(failed)
        )
        recovered = self.store.resolve_validation_blocker(
            recovery_request, attestation, self.authority
        )
        self.oracle.allowed_head = recovered.event_hash
        request, capability = self._validator_intent(
            replace(observation, event_hash=parent_event_hash),
            suffix="2", check_id="check-1", recovery_id="recovery-1",
        )
        committed = self.store.commit_validator_intent(
            request, capability, self.authority
        )
        self.oracle.allowed_head = committed.event_hash
        connection = sqlite3.connect(self.database_path)
        try:
            connection.execute(
                "UPDATE validation_recoveries SET "
                "successor_validator_attempt_id = 'tampered-attempt' "
                "WHERE recovery_id = 'recovery-1'"
            )
            connection.commit()
        finally:
            connection.close()
        with patch.object(self.store, "_verify_projections", return_value=None):
            with self.assertRaisesRegex(DispatchDenied, "lost its T16 recovery"):
                self.store._contact_committed_validator(
                    request, capability, committed,
                    self.store._adapter_target_digest("repo-1", "VALIDATOR"),
                    self.authority,
                )

    def test_t16_migrates_populated_legacy_validation_schema(self) -> None:
        _, failed = self._prepare_recoverable_application()
        connection = sqlite3.connect(self.database_path)
        try:
            connection.execute("PRAGMA foreign_keys = OFF")
            connection.execute(
                "DROP INDEX uq_validator_intents_recovery_id"
            )
            connection.execute("DROP TABLE validation_recoveries")
            connection.execute(
                "CREATE TABLE validation_applications_snapshot AS "
                "SELECT * FROM validation_applications"
            )
            connection.execute("DROP TABLE validation_applications")
            connection.execute(
                "ALTER TABLE validation_applications_snapshot "
                "RENAME TO validation_applications"
            )
            connection.execute(
                "CREATE UNIQUE INDEX legacy_plan_check_unique ON "
                "validation_applications(plan_id, check_id)"
            )
            connection.commit()
        finally:
            connection.close()

        migrated = SQLiteStateStore(
            self.database_path, self.oracle, "repo-1"
        )
        migrated._bind_classification_authority(self.authority)
        migrated.load_verified("repo-1")
        connection = sqlite3.connect(self.database_path)
        try:
            validator_columns = {
                row[1]
                for row in connection.execute(
                    "PRAGMA table_info(validator_intents)"
                )
            }
            application_indexes = {
                row[1]: tuple(
                    column[2]
                    for column in connection.execute(
                        f"PRAGMA index_info('{row[1]}')"
                    )
                )
                for row in connection.execute(
                    "PRAGMA index_list(validation_applications)"
                )
                if row[2]
            }
            foreign_key_errors = connection.execute(
                "PRAGMA foreign_key_check"
            ).fetchall()
            migrated_rows = connection.execute(
                "SELECT application_id, verdict, classification FROM "
                "validation_applications"
            ).fetchall()
            before_noop = tuple(connection.iterdump())
        finally:
            connection.close()
        self.assertIn("recovery_id", validator_columns)
        self.assertNotIn(("plan_id", "check_id"), application_indexes.values())
        self.assertEqual(foreign_key_errors, [])
        self.assertEqual(
            migrated_rows, [("application-1", "FAIL", "RECOVERABLE")]
        )

        reopened = SQLiteStateStore(
            self.database_path, self.oracle, "repo-1"
        )
        reopened._bind_classification_authority(self.authority)
        connection = sqlite3.connect(self.database_path)
        try:
            after_noop = tuple(connection.iterdump())
            with self.assertRaises(sqlite3.IntegrityError):
                connection.execute(
                    "UPDATE validation_applications SET verdict = 'INVALID' "
                    "WHERE application_id = 'application-1'"
                )
        finally:
            connection.close()
        self.assertEqual(after_noop, before_noop)
        recovery_request, attestation, _ = self._validation_recovery_pair(failed)
        recovered = reopened.resolve_validation_blocker(
            recovery_request, attestation, self.authority
        )
        self.oracle.allowed_head = recovered.event_hash
        reopened.load_verified("repo-1")

    def test_t16_rejects_malformed_existing_recovery_schema(self) -> None:
        connection = sqlite3.connect(self.database_path)
        try:
            connection.execute("DROP TABLE validation_recoveries")
            connection.execute("DROP INDEX uq_validator_intents_recovery_id")
            connection.execute(
                "CREATE TABLE validation_recoveries (recovery_id TEXT PRIMARY KEY)"
            )
            connection.execute(
                "CREATE INDEX uq_validator_intents_recovery_id ON "
                "validator_intents(command_id)"
            )
            connection.commit()
        finally:
            connection.close()
        with self.assertRaisesRegex(
            StorageIntegrityError, "recovery schema is incompatible"
        ):
            SQLiteStateStore(self.database_path, self.oracle, "repo-1")

    def test_t16_rejects_weakened_recovery_index_predicate(self) -> None:
        connection = sqlite3.connect(self.database_path)
        try:
            connection.execute("DROP INDEX uq_validator_intents_recovery_id")
            connection.execute(
                "CREATE UNIQUE INDEX uq_validator_intents_recovery_id ON "
                "validator_intents(recovery_id) WHERE recovery_id IS NULL"
            )
            connection.commit()
        finally:
            connection.close()
        with self.assertRaisesRegex(
            StorageIntegrityError, "recovery schema is incompatible"
        ):
            SQLiteStateStore(self.database_path, self.oracle, "repo-1")

    def test_t16_rejects_weakened_recovery_table_constraint(self) -> None:
        connection = sqlite3.connect(self.database_path)
        try:
            table_sql = connection.execute(
                "SELECT sql FROM sqlite_master WHERE type = 'table' AND "
                "name = 'validation_recoveries'"
            ).fetchone()[0]
            weakened_sql = table_sql.replace(
                "resulting_state TEXT NOT NULL CHECK (resulting_state = 'VALIDATING')",
                "resulting_state TEXT NOT NULL",
            )
            self.assertNotEqual(weakened_sql, table_sql)
            connection.execute("DROP TABLE validation_recoveries")
            connection.execute(weakened_sql)
            connection.commit()
        finally:
            connection.close()
        with self.assertRaisesRegex(
            StorageIntegrityError, "recovery schema is incompatible"
        ):
            SQLiteStateStore(self.database_path, self.oracle, "repo-1")

    def test_r_stop_01_migrates_populated_terminal_validation_schema(
        self,
    ) -> None:
        observation = self._record_validator_result(verdict="FAIL")
        applied = self.store._apply_validator_observation(
            ValidationApplicationRequest(
                "application-1", "apply-command-1", "apply-event-1",
                "repo-1", "run-1", "item-1", "effect-1", "revision-1",
                "check-1", "validator-attempt-1",
                "validator-observation-1",
            ),
            classification=self._classification(observation, "FINAL"),
        )
        self.oracle.allowed_head = applied.event_hash
        connection = sqlite3.connect(self.database_path)
        try:
            plan_hash = connection.execute(
                "SELECT event_hash FROM validation_plans WHERE plan_id = 'plan-1'"
            ).fetchone()[0]
        finally:
            connection.close()
        settled = self.store.settle_terminal_validation(
            TerminalValidationSettlementRequest(
                "terminal-settlement-1", "terminal-command-1",
                "terminal-event-1", "repo-1", "run-1", "item-1",
                "effect-1", "plan-1", "revision-1", "check-2", "PLAN",
                "plan-1", plan_hash, "CANCELLED_WITHOUT_START",
            )
        )
        self.oracle.allowed_head = settled.event_hash

        connection = sqlite3.connect(self.database_path)
        try:
            connection.execute("PRAGMA foreign_keys = OFF")
            target_sql = connection.execute(
                "SELECT sql FROM sqlite_master WHERE type = 'table' AND "
                "name = 'terminal_validation_settlements'"
            ).fetchone()[0]
            legacy_sql = target_sql.replace(
                "'VALIDATION_APPLICATION', ", ""
            )
            self.assertNotEqual(legacy_sql, target_sql)
            before_rows = connection.execute(
                "SELECT * FROM terminal_validation_settlements"
            ).fetchall()
            before_event_bodies = connection.execute(
                "SELECT event_id, body_json FROM events ORDER BY event_id"
            ).fetchall()
            connection.execute(
                "ALTER TABLE terminal_validation_settlements RENAME TO "
                "terminal_validation_settlements_snapshot"
            )
            connection.execute(legacy_sql)
            columns = ", ".join(
                row[1]
                for row in connection.execute(
                    "PRAGMA table_info(terminal_validation_settlements)"
                )
            )
            connection.execute(
                f"INSERT INTO terminal_validation_settlements ({columns}) "
                f"SELECT {columns} FROM terminal_validation_settlements_snapshot"
            )
            connection.execute(
                "DROP TABLE terminal_validation_settlements_snapshot"
            )
            connection.commit()
        finally:
            connection.close()

        migrated = SQLiteStateStore(
            self.database_path, self.oracle, "repo-1"
        )
        migrated._bind_classification_authority(self.authority)
        connection = sqlite3.connect(self.database_path)
        try:
            after_rows = connection.execute(
                "SELECT * FROM terminal_validation_settlements"
            ).fetchall()
            after_event_bodies = connection.execute(
                "SELECT event_id, body_json FROM events ORDER BY event_id"
            ).fetchall()
            migrated_sql = connection.execute(
                "SELECT sql FROM sqlite_master WHERE type = 'table' AND "
                "name = 'terminal_validation_settlements'"
            ).fetchone()[0]
            foreign_key_errors = connection.execute(
                "PRAGMA foreign_key_check"
            ).fetchall()
        finally:
            connection.close()
        self.assertEqual(after_rows, before_rows)
        self.assertEqual(after_event_bodies, before_event_bodies)
        self.assertIn("VALIDATION_APPLICATION", migrated_sql)
        self.assertEqual(foreign_key_errors, [])
        migrated.load_verified("repo-1")

    def test_terminal_validation_migrates_exact_head_generation_schema(
        self,
    ) -> None:
        self._prepare_finalization()
        stopped = self.store.stop(
            self._stop_request(),
            self._stop_capability(StopMode.IMMEDIATE),
            self.authority,
        )
        self.oracle.allowed_head = stopped.event_hash
        settled = self.store.settle_terminal_validation(
            self._terminal_application_request("PASSED")
        )
        self.oracle.allowed_head = settled.event_hash

        connection = sqlite3.connect(self.database_path)
        try:
            connection.execute("PRAGMA foreign_keys = OFF")
            target_sql = connection.execute(
                "SELECT sql FROM sqlite_master WHERE type = 'table' AND "
                "name = 'terminal_validation_settlements'"
            ).fetchone()[0]
            head_sql = target_sql.replace(
                "slot_generation INTEGER NOT NULL CHECK (slot_generation > 0)",
                "slot_generation INTEGER NOT NULL CHECK (slot_generation = 1)",
            )
            self.assertNotEqual(head_sql, target_sql)
            self.assertIn("VALIDATION_APPLICATION", head_sql)
            before_rows = connection.execute(
                "SELECT * FROM terminal_validation_settlements"
            ).fetchall()
            before_event_bodies = connection.execute(
                "SELECT event_id, body_json FROM events ORDER BY event_id"
            ).fetchall()
            connection.execute(
                "ALTER TABLE terminal_validation_settlements RENAME TO "
                "terminal_validation_settlements_snapshot"
            )
            connection.execute(head_sql)
            columns = ", ".join(
                row[1]
                for row in connection.execute(
                    "PRAGMA table_info(terminal_validation_settlements)"
                )
            )
            connection.execute(
                f"INSERT INTO terminal_validation_settlements ({columns}) "
                f"SELECT {columns} FROM "
                "terminal_validation_settlements_snapshot"
            )
            connection.execute(
                "DROP TABLE terminal_validation_settlements_snapshot"
            )
            connection.commit()
        finally:
            connection.close()

        migrated = SQLiteStateStore(
            self.database_path, self.oracle, "repo-1"
        )
        migrated._bind_classification_authority(self.authority)
        connection = sqlite3.connect(self.database_path)
        try:
            after_rows = connection.execute(
                "SELECT * FROM terminal_validation_settlements"
            ).fetchall()
            after_event_bodies = connection.execute(
                "SELECT event_id, body_json FROM events ORDER BY event_id"
            ).fetchall()
            migrated_sql = connection.execute(
                "SELECT sql FROM sqlite_master WHERE type = 'table' AND "
                "name = 'terminal_validation_settlements'"
            ).fetchone()[0]
            foreign_key_errors = connection.execute(
                "PRAGMA foreign_key_check"
            ).fetchall()
        finally:
            connection.close()
        self.assertEqual(after_rows, before_rows)
        self.assertEqual(after_event_bodies, before_event_bodies)
        self.assertIn(
            "slot_generation > 0", "".join(migrated_sql.splitlines())
        )
        self.assertEqual(foreign_key_errors, [])
        migrated.load_verified("repo-1", authority=self.authority)

    def test_r_stop_01_rejects_incompatible_terminal_schema_without_mutation(
        self,
    ) -> None:
        connection = sqlite3.connect(self.database_path)
        try:
            target_sql = connection.execute(
                "SELECT sql FROM sqlite_master WHERE type = 'table' AND "
                "name = 'terminal_validation_settlements'"
            ).fetchone()[0]
            weakened_sql = target_sql.replace(
                "slot_generation INTEGER NOT NULL CHECK (slot_generation > 0)",
                "slot_generation INTEGER NOT NULL",
            )
            self.assertNotEqual(weakened_sql, target_sql)
            connection.execute("DROP TABLE terminal_validation_settlements")
            connection.execute(weakened_sql)
            connection.commit()
            before = tuple(connection.iterdump())
        finally:
            connection.close()

        with self.assertRaisesRegex(
            StorageIntegrityError, "terminal validation schema is incompatible"
        ):
            SQLiteStateStore(self.database_path, self.oracle, "repo-1")
        connection = sqlite3.connect(self.database_path)
        try:
            after = tuple(connection.iterdump())
        finally:
            connection.close()
        self.assertEqual(after, before)

    def test_c05_recoverable_failure_rolls_back_and_replays_after_lost_ack(self) -> None:
        observation = self._record_validator_result(
            verdict="FAIL", only_check=True
        )
        classification = self._classification(observation, "RECOVERABLE")
        request = ValidationApplicationRequest(
            "application-1", "apply-command-1", "apply-event-1",
            "repo-1", "run-1", "item-1", "effect-1", "revision-1",
            "check-1", "validator-attempt-1", "validator-observation-1",
        )
        with self.assertRaises(InjectedFailure):
            self.store._apply_validator_observation(
                request, classification=classification,
                failure_hook=raise_at(
                    "after_validation_application_writes_before_commit"
                ),
            )
        self.assertEqual(self.store.table_counts()["validation_applications"], 0)
        with self.assertRaises(InjectedFailure):
            self.store._apply_validator_observation(
                request, classification=classification,
                failure_hook=raise_at(
                    "after_validation_application_commit_before_acknowledgement"
                ),
            )
        connection = sqlite3.connect(self.database_path)
        try:
            self.oracle.allowed_head = connection.execute(
                "SELECT event_hash FROM validation_applications "
                "WHERE application_id = 'application-1'"
            ).fetchone()[0]
        finally:
            connection.close()
        recovered = SQLiteStateStore(self.database_path, self.oracle, "repo-1")
        recovered._bind_classification_authority(self.authority)
        replay = recovered._apply_validator_observation(request)
        self.assertTrue(replay.replayed)
        self.assertEqual(replay.resulting_state.value, "BLOCKED")

    def test_c05_final_failure_is_atomic_replay_safe_and_permanently_fenced(self) -> None:
        observation = self._record_validator_result(
            verdict="FAIL", only_check=True
        )
        classification = self._classification(observation, "FINAL")
        request = ValidationApplicationRequest(
            "application-1", "apply-command-1", "apply-event-1",
            "repo-1", "run-1", "item-1", "effect-1", "revision-1",
            "check-1", "validator-attempt-1", "validator-observation-1",
        )
        with self.assertRaises(InjectedFailure):
            self.store._apply_validator_observation(
                request, classification=classification,
                failure_hook=raise_at(
                    "after_validation_application_writes_before_commit"
                ),
            )
        self.assertEqual(self.store.table_counts()["validation_applications"], 0)
        with self.assertRaises(InjectedFailure):
            self.store._apply_validator_observation(
                request, classification=classification,
                failure_hook=raise_at(
                    "after_validation_application_commit_before_acknowledgement"
                ),
            )
        connection = sqlite3.connect(self.database_path)
        try:
            event_hash = connection.execute(
                "SELECT event_hash FROM validation_applications "
                "WHERE application_id = 'application-1'"
            ).fetchone()[0]
        finally:
            connection.close()
        self.oracle.allowed_head = event_hash
        replay = self.store._apply_validator_observation(
            request,
        )
        self.assertTrue(replay.replayed)
        self.assertEqual(replay.resulting_state.value, "FAILED_FINAL")
        self.assertEqual(self.store.table_counts()["outstanding_slot"], 0)
        self.assertEqual(self.store.table_counts()["dispatch_fences"], 1)
        self.store.load_verified("repo-1")
        recovered_store = SQLiteStateStore(
            self.database_path, self.oracle, "repo-1"
        )
        recovered_store._bind_classification_authority(self.authority)
        recovered_replay = recovered_store._apply_validator_observation(request)
        self.assertTrue(recovered_replay.replayed)

        second_grant = SyntheticGrant(
            "grant-2", "repo-1", "effect-2", "attempt-2", "scope-2"
        )
        self.authority.register(second_grant)
        second_capability = self.authority.claim(*second_grant.__dict__.values())
        second_plan = recovered_store.accept_plan(
            PlanAcceptanceRequest(
                "plan-2", "plan-command-2", "plan-event-2", "repo-1",
                "run-2", "item-2", "effect-2", "revision-2",
                "descriptor-digest", "scope-2", "budget-policy-digest",
                ("check-2",),
            ),
            expected_head=replay.event_hash,
            writer_epoch=20,
        )
        self.oracle.allowed_head = second_plan.event_hash
        second_intent = recovered_store.commit_intent(
            replace(
                self.request(), run_id="run-2", item_id="item-2",
                command_id="command-2", event_id="event-2",
                logical_effect_id="effect-2", attempt_id="attempt-2",
                permission_use_id="permission-use-2",
                reservation_id="reservation-2",
            ),
            second_capability,
            self.authority,
            expected_head=second_plan.event_hash,
            writer_epoch=21,
        )
        self.assertFalse(second_intent.replayed)
        self.assertEqual(
            recovered_store.load_run_lifecycle("run-2").value, "RUNNING"
        )

    def test_c05_final_failure_with_pending_check_retains_slot(self) -> None:
        observation = self._record_validator_result(verdict="FAIL")
        applied = self.store._apply_validator_observation(
            ValidationApplicationRequest(
                "application-1", "apply-command-1", "apply-event-1",
                "repo-1", "run-1", "item-1", "effect-1", "revision-1",
                "check-1", "validator-attempt-1", "validator-observation-1",
            ),
            classification=self._classification(observation, "FINAL"),
        )
        self.oracle.allowed_head = applied.event_hash
        self.assertEqual(applied.resulting_state.value, "FAILED_FINAL")
        self.assertEqual(self.store.table_counts()["outstanding_slot"], 1)
        self.store.load_verified("repo-1")

    def test_t26_terminal_settlement_closes_unstarted_check_and_slot(self) -> None:
        observation = self._record_validator_result(verdict="FAIL")
        applied = self.store._apply_validator_observation(
            ValidationApplicationRequest(
                "application-1", "apply-command-1", "apply-event-1",
                "repo-1", "run-1", "item-1", "effect-1", "revision-1",
                "check-1", "validator-attempt-1", "validator-observation-1",
            ),
            classification=self._classification(observation, "FINAL"),
        )
        self.oracle.allowed_head = applied.event_hash
        connection = sqlite3.connect(self.database_path)
        try:
            plan_hash = connection.execute(
                "SELECT event_hash FROM validation_plans WHERE plan_id = 'plan-1'"
            ).fetchone()[0]
        finally:
            connection.close()
        request = TerminalValidationSettlementRequest(
            "terminal-settlement-1", "terminal-command-1", "terminal-event-1",
            "repo-1", "run-1", "item-1", "effect-1", "plan-1",
            "revision-1", "check-2", "PLAN", "plan-1", plan_hash,
            "CANCELLED_WITHOUT_START",
        )
        with self.assertRaises(InjectedFailure):
            self.store.settle_terminal_validation(
                request,
                failure_hook=raise_at(
                    "after_terminal_settlement_writes_before_commit"
                ),
            )
        self.assertEqual(self.store.table_counts()["outstanding_slot"], 1)
        with self.assertRaises(InjectedFailure):
            self.store.settle_terminal_validation(
                request,
                failure_hook=raise_at(
                    "after_terminal_settlement_commit_before_acknowledgement"
                ),
            )
        connection = sqlite3.connect(self.database_path)
        try:
            terminal_hash = connection.execute(
                "SELECT event_hash FROM terminal_validation_settlements WHERE "
                "terminal_settlement_id = 'terminal-settlement-1'"
            ).fetchone()[0]
        finally:
            connection.close()
        self.oracle.allowed_head = terminal_hash
        settled = self.store.settle_terminal_validation(request)

        self.assertEqual(settled.resulting_state, LifecycleState.FAILED_FINAL)
        self.assertTrue(settled.slot_released)
        self.assertTrue(settled.replayed)
        self.assertEqual(self.store.table_counts()["outstanding_slot"], 0)
        self.assertEqual(self.store.table_counts()["dispatch_fences"], 1)
        self.store.load_verified("repo-1")

    def test_t26_recovery_rejects_mandatory_slot_retention(self) -> None:
        observation = self._record_validator_result(verdict="FAIL")
        applied = self.store._apply_validator_observation(
            ValidationApplicationRequest(
                "application-1", "apply-command-1", "apply-event-1",
                "repo-1", "run-1", "item-1", "effect-1", "revision-1",
                "check-1", "validator-attempt-1", "validator-observation-1",
            ),
            classification=self._classification(observation, "FINAL"),
        )
        self.oracle.allowed_head = applied.event_hash
        connection = sqlite3.connect(self.database_path)
        try:
            plan_hash = connection.execute(
                "SELECT event_hash FROM validation_plans WHERE plan_id = 'plan-1'"
            ).fetchone()[0]
        finally:
            connection.close()
        settled = self.store.settle_terminal_validation(
            TerminalValidationSettlementRequest(
                "terminal-settlement-1", "terminal-command-1",
                "terminal-event-1", "repo-1", "run-1", "item-1",
                "effect-1", "plan-1", "revision-1", "check-2", "PLAN",
                "plan-1", plan_hash, "CANCELLED_WITHOUT_START",
            )
        )
        self.assertTrue(settled.slot_released)
        connection = sqlite3.connect(self.database_path)
        try:
            body = json.loads(
                connection.execute(
                    "SELECT body_json FROM events WHERE event_id = ?",
                    (settled.event_id,),
                ).fetchone()[0]
            )
            body["slot_released"] = False
            event_hash = self.store._event_hash(body)
            body_json = json.dumps(
                body, sort_keys=True, separators=(",", ":")
            )
            connection.execute(
                "UPDATE events SET event_hash = ?, body_json = ? WHERE event_id = ?",
                (event_hash, body_json, settled.event_id),
            )
            connection.execute(
                "UPDATE terminal_validation_settlements SET slot_released = 0, "
                "event_hash = ?, body_json = ? WHERE terminal_settlement_id = ?",
                (event_hash, body_json, settled.terminal_settlement_id),
            )
            connection.execute(
                "UPDATE command_outcomes SET event_hash = ? WHERE command_id = ?",
                (event_hash, settled.command_id),
            )
            connection.execute(
                "UPDATE runs SET head_hash = ? WHERE run_id = ?",
                (event_hash, "run-1"),
            )
            connection.execute(
                "UPDATE repositories SET catalog_head = ? WHERE repository_id = ?",
                (event_hash, "repo-1"),
            )
            connection.execute(
                "INSERT INTO outstanding_slot (singleton, repository_id, "
                "run_id, logical_effect_id, attempt_id, generation, "
                "origin_kind, origin_id) VALUES (1, ?, ?, ?, ?, 1, "
                "'EXECUTION_INTENT', ?)",
                ("repo-1", "run-1", "effect-1", "attempt-1", "attempt-1"),
            )
            connection.commit()
        finally:
            connection.close()
        self.oracle.allowed_head = event_hash

        with self.assertRaisesRegex(
            StorageIntegrityError, "terminal validation release decision"
        ):
            self.store.load_verified("repo-1")

    def test_t24_validator_cessation_is_target_serialized_and_replay_safe(
        self,
    ) -> None:
        parent = self._record_effect_observation(check_ids=("check-1",))
        intent, capability = self._validator_intent(parent)
        committed = self.store.commit_validator_intent(
            intent, capability, self.authority
        )
        self.oracle.allowed_head = committed.event_hash
        validator_path = self.database_path.parent / "synthetic-validator.sqlite3"
        adapter = SyntheticValidatorAdapter(validator_path)
        adapter._canonical_repository_id = "repo-1"
        adapter._canonical_ledger_path = validator_path.resolve()
        attestation = self.authority.issue_validator_cessation_attestation(
            "cessation-attestation-1", "cessation-1",
            adapter._target_digest("repo-1"), capability.claim_id,
            "VALIDATOR:validator-intent-1", committed.event_hash,
            "repo-1", "run-1", "item-1", "effect-1", "revision-1",
            "check-1", "validator-attempt-1",
        )
        seal = adapter.seal_cessation(attestation, self.authority)
        self.assertFalse(seal.result_available)
        request = ValidatorCessationRequest(
            "cessation-1", "cessation-command-1", "cessation-event-1",
            "repo-1", "run-1", "item-1", "effect-1",
            "validator-intent-1", "validator-attempt-1", "revision-1",
            "check-1", seal.cessation_hash,
        )
        receipt = self.store.record_validator_cessation(
            request, self.authority
        )
        self.oracle.allowed_head = receipt.event_hash
        replay = self.store.record_validator_cessation(request, self.authority)

        self.assertTrue(replay.replayed)
        self.assertEqual(replay.event_hash, receipt.event_hash)
        self.assertFalse(receipt.result_available)
        self.store.load_verified("repo-1")

        class ContactAlreadyClaimed:
            @staticmethod
            def _contact_committed_validator(*args, **kwargs) -> None:
                return None

        containment_spec = parse_validator_containment_spec(
            intent.containment_spec_json
        )
        with self.assertRaisesRegex(DispatchDenied, "sealed as ceased"):
            adapter._execute_committed(
                capability,
                SyntheticValidatorRequest(
                    "repo-1", "effect-1", "revision-1", "check-1",
                    "input-1", "validator-attempt-1", "read-only-scope-1",
                    "late-result", "PASS", capability.containment_digest,
                    containment_spec.allowed_actions,
                    containment_spec.input_root,
                    f"{containment_spec.output_root}/result.json",
                    f"{containment_spec.scratch_root}/work",
                    synthetic_validator_output_size("late-result", "PASS"),
                ),
                self.authority,
                ContactAlreadyClaimed(),
                committed,
                intent,
                usage_units=1,
            )

    def test_t26_terminal_result_is_atomic_and_replay_safe(self) -> None:
        parent = self._record_effect_observation()
        pending_observation = self._record_validator_result_for(
            parent, suffix="1", verdict="PASS"
        )
        cessation = self._record_validator_cessation_for(
            suffix="1", result_available=True
        )
        stop_hash = self._stop_run()
        request = TerminalValidationSettlementRequest(
            "terminal-settlement-1", "terminal-command-1", "terminal-event-1",
            "repo-1", "run-1", "item-1", "effect-1", "plan-1",
            "revision-1", "check-1", "VALIDATOR_OBSERVATION",
            "validator-observation-1", pending_observation.event_hash,
            "PASSED", "validator-intent-1", "validator-attempt-1",
            "cessation-1", cessation.event_hash,
        )
        with self.assertRaisesRegex(
            DispatchDenied, "does not bind cessation proof"
        ):
            self.store.settle_terminal_validation(
                replace(
                    request,
                    terminal_settlement_id="wrong-cessation-settlement",
                    command_id="wrong-cessation-command",
                    event_id="wrong-cessation-event",
                    cessation_event_hash="wrong-cessation-hash",
                )
            )
        with self.assertRaises(InjectedFailure):
            self.store.settle_terminal_validation(
                request,
                failure_hook=raise_at(
                    "after_terminal_settlement_writes_before_commit"
                ),
            )
        self.assertEqual(
            self.store.table_counts()["terminal_validation_settlements"], 0
        )
        self.assertEqual(self.store.table_counts()["outstanding_slot"], 1)

        with self.assertRaises(InjectedFailure):
            self.store.settle_terminal_validation(
                request,
                failure_hook=raise_at(
                    "after_terminal_settlement_commit_before_acknowledgement"
                ),
            )
        connection = sqlite3.connect(self.database_path)
        try:
            terminal_hash = connection.execute(
                "SELECT event_hash FROM terminal_validation_settlements WHERE "
                "terminal_settlement_id = 'terminal-settlement-1'"
            ).fetchone()[0]
        finally:
            connection.close()
        self.oracle.allowed_head = terminal_hash
        reopened = SQLiteStateStore(
            self.database_path, self.oracle, "repo-1"
        )
        reopened._bind_classification_authority(self.authority)
        replay = reopened.settle_terminal_validation(request)

        self.assertTrue(replay.replayed)
        self.assertFalse(replay.slot_released)
        self.assertEqual(replay.resulting_state, LifecycleState.STOPPED)
        misbound_path = self.database_path.parent / "misbound-t26.sqlite3"
        shutil.copy2(self.database_path, misbound_path)
        connection = sqlite3.connect(misbound_path)
        connection.row_factory = sqlite3.Row
        try:
            row = connection.execute(
                "SELECT body_json FROM terminal_validation_settlements WHERE "
                "terminal_settlement_id = 'terminal-settlement-1'"
            ).fetchone()
            body = json.loads(row["body_json"])
            body["source_event_hash"] = "forged-observation-hash"
            request_body = {
                key: body[key]
                for key in TerminalValidationSettlementRequest.__dataclass_fields__
            }
            payload_digest = self.store._event_hash(request_body)
            obligation_proof_key = self.store._event_hash(
                {
                    key: value
                    for key, value in request_body.items()
                    if key not in {
                        "terminal_settlement_id", "command_id", "event_id"
                    }
                }
            )
            body["obligation_proof_key"] = obligation_proof_key
            misbound_hash = self.store._event_hash(body)
            body_json = json.dumps(
                body, sort_keys=True, separators=(",", ":")
            )
            connection.execute(
                "UPDATE events SET event_hash = ?, body_json = ? WHERE "
                "event_id = 'terminal-event-1'",
                (misbound_hash, body_json),
            )
            connection.execute(
                "UPDATE terminal_validation_settlements SET "
                "source_event_hash = ?, obligation_proof_key = ?, "
                "payload_digest = ?, event_hash = ?, body_json = ? WHERE "
                "terminal_settlement_id = 'terminal-settlement-1'",
                (
                    "forged-observation-hash", obligation_proof_key,
                    payload_digest, misbound_hash, body_json,
                ),
            )
            connection.execute(
                "UPDATE command_outcomes SET payload_digest = ?, "
                "event_hash = ? WHERE command_id = 'terminal-command-1'",
                (payload_digest, misbound_hash),
            )
            connection.execute(
                "UPDATE runs SET head_hash = ? WHERE run_id = 'run-1'",
                (misbound_hash,),
            )
            connection.execute(
                "UPDATE repositories SET catalog_head = ? WHERE "
                "repository_id = 'repo-1'",
                (misbound_hash,),
            )
            connection.commit()
        finally:
            connection.close()
        misbound_oracle = MutableFreshnessOracle()
        misbound_oracle.allowed_head = misbound_hash
        with self.assertRaisesRegex(
            StorageIntegrityError, "result/cessation binding is invalid"
        ):
            SQLiteStateStore(
                misbound_path, misbound_oracle, "repo-1"
            ).load_verified("repo-1", authority=self.authority)
        tampered_path = self.database_path.parent / "tampered-t26.sqlite3"
        shutil.copy2(self.database_path, tampered_path)
        connection = sqlite3.connect(tampered_path)
        connection.row_factory = sqlite3.Row
        try:
            row = connection.execute(
                "SELECT body_json FROM terminal_validation_settlements WHERE "
                "terminal_settlement_id = 'terminal-settlement-1'"
            ).fetchone()
            body = json.loads(row["body_json"])
            body["slot_released"] = True
            tampered_hash = self.store._event_hash(body)
            body_json = json.dumps(
                body, sort_keys=True, separators=(",", ":")
            )
            connection.execute(
                "UPDATE events SET event_hash = ?, body_json = ? WHERE "
                "event_id = 'terminal-event-1'",
                (tampered_hash, body_json),
            )
            connection.execute(
                "UPDATE terminal_validation_settlements SET event_hash = ?, "
                "slot_released = 1, body_json = ? WHERE "
                "terminal_settlement_id = 'terminal-settlement-1'",
                (tampered_hash, body_json),
            )
            connection.execute(
                "UPDATE command_outcomes SET event_hash = ? WHERE "
                "command_id = 'terminal-command-1'",
                (tampered_hash,),
            )
            connection.execute(
                "UPDATE runs SET head_hash = ? WHERE run_id = 'run-1'",
                (tampered_hash,),
            )
            connection.execute(
                "UPDATE repositories SET catalog_head = ? WHERE "
                "repository_id = 'repo-1'",
                (tampered_hash,),
            )
            connection.execute(
                "DELETE FROM outstanding_slot WHERE repository_id = 'repo-1'"
            )
            connection.commit()
        finally:
            connection.close()
        tampered_oracle = MutableFreshnessOracle()
        tampered_oracle.allowed_head = tampered_hash
        with self.assertRaisesRegex(
            StorageIntegrityError, "required validation checks remain unsettled"
        ):
            SQLiteStateStore(
                tampered_path, tampered_oracle, "repo-1"
            ).load_verified("repo-1", authority=self.authority)
        connection = sqlite3.connect(self.database_path)
        try:
            plan_hash = connection.execute(
                "SELECT event_hash FROM validation_plans WHERE plan_id = 'plan-1'"
            ).fetchone()[0]
        finally:
            connection.close()
        final = reopened.settle_terminal_validation(
            TerminalValidationSettlementRequest(
                "terminal-settlement-2", "terminal-command-2",
                "terminal-event-2", "repo-1", "run-1", "item-1",
                "effect-1", "plan-1", "revision-1", "check-2", "PLAN",
                "plan-1", plan_hash, "CANCELLED_WITHOUT_START",
            )
        )
        self.oracle.allowed_head = final.event_hash
        self.assertTrue(final.slot_released)
        self.assertEqual(final.resulting_state, LifecycleState.STOPPED)
        self.assertEqual(reopened.table_counts()["outstanding_slot"], 0)
        reopened.load_verified("repo-1")

    def test_t26_before_t23_recovers_without_releasing_slot(self) -> None:
        plan = self.store.accept_plan(
            PlanAcceptanceRequest(
                "plan-1", "plan-command-1", "plan-event-1", "repo-1",
                "run-1", "item-1", "effect-1", "revision-1",
                "descriptor-digest", "scope-1", "budget-policy-digest",
                ("check-1", "check-2"),
            ),
            expected_head="", writer_epoch=1,
        )
        self.oracle.allowed_head = plan.event_hash
        committed = self.store.commit_intent(
            self.request(), self.capability, self.authority,
            expected_head=plan.event_hash, writer_epoch=2,
        )
        self.oracle.allowed_head = committed.event_hash
        self._stop_run()
        early = self.store.settle_terminal_validation(
            TerminalValidationSettlementRequest(
                "terminal-settlement-1", "terminal-command-1",
                "terminal-event-1", "repo-1", "run-1", "item-1",
                "effect-1", "plan-1", "revision-1", "check-1", "PLAN",
                "plan-1", plan.event_hash, "CANCELLED_WITHOUT_START",
            )
        )
        self.oracle.allowed_head = early.event_hash
        self.assertFalse(early.slot_released)
        self.assertEqual(self.store.table_counts()["outstanding_slot"], 1)

        tampered_path = self.database_path.parent / "tampered-t26-slot.sqlite3"
        shutil.copy2(self.database_path, tampered_path)
        connection = sqlite3.connect(tampered_path)
        connection.row_factory = sqlite3.Row
        try:
            row = connection.execute(
                "SELECT body_json FROM terminal_validation_settlements WHERE "
                "terminal_settlement_id = 'terminal-settlement-1'"
            ).fetchone()
            body = json.loads(row["body_json"])
            body["slot_attempt_id"] = "forged-attempt"
            tampered_hash = self.store._event_hash(body)
            body_json = json.dumps(
                body, sort_keys=True, separators=(",", ":")
            )
            connection.execute(
                "UPDATE events SET event_hash = ?, body_json = ? WHERE "
                "event_id = 'terminal-event-1'",
                (tampered_hash, body_json),
            )
            connection.execute(
                "UPDATE terminal_validation_settlements SET "
                "slot_attempt_id = 'forged-attempt', event_hash = ?, "
                "body_json = ? WHERE terminal_settlement_id = "
                "'terminal-settlement-1'",
                (tampered_hash, body_json),
            )
            connection.execute(
                "UPDATE command_outcomes SET event_hash = ? WHERE "
                "command_id = 'terminal-command-1'",
                (tampered_hash,),
            )
            connection.execute(
                "UPDATE runs SET head_hash = ? WHERE run_id = 'run-1'",
                (tampered_hash,),
            )
            connection.execute(
                "UPDATE repositories SET catalog_head = ? WHERE "
                "repository_id = 'repo-1'",
                (tampered_hash,),
            )
            connection.commit()
        finally:
            connection.close()
        tampered_oracle = MutableFreshnessOracle()
        tampered_oracle.allowed_head = tampered_hash
        with self.assertRaisesRegex(
            StorageIntegrityError, "operation slot attempt"
        ):
            SQLiteStateStore(
                tampered_path, tampered_oracle, "repo-1"
            ).load_verified("repo-1")

        reopened = SQLiteStateStore(
            self.database_path, self.oracle, "repo-1"
        )
        reopened._bind_classification_authority(self.authority)
        reopened.load_verified("repo-1")
        late = self._record_signed_effect_observation(
            EffectObservationRequest(
                "late-observation-1", "late-observe-command-1",
                "late-observation-event-1", "repo-1", "run-1", "item-1",
                "effect-1", "attempt-1", "late-receipt-1",
                self.capability.claim_id, "descriptor-digest", 2,
                "late-settlement-1", "",
            ),
            store=reopened,
        )
        self.oracle.allowed_head = late.event_hash
        reopened.load_verified("repo-1")
        final = reopened.settle_terminal_validation(
            TerminalValidationSettlementRequest(
                "terminal-settlement-2", "terminal-command-2",
                "terminal-event-2", "repo-1", "run-1", "item-1",
                "effect-1", "plan-1", "revision-1", "check-2", "PLAN",
                "plan-1", plan.event_hash, "CANCELLED_WITHOUT_START",
            )
        )
        self.oracle.allowed_head = final.event_hash
        self.assertTrue(final.slot_released)
        self.assertEqual(reopened.table_counts()["outstanding_slot"], 0)
        reopened.load_verified("repo-1")

    def test_t26_last_check_before_t23_releases_slot_on_late_receipt(
        self,
    ) -> None:
        plan = self.store.accept_plan(
            PlanAcceptanceRequest(
                "plan-1", "plan-command-1", "plan-event-1", "repo-1",
                "run-1", "item-1", "effect-1", "revision-1",
                "descriptor-digest", "scope-1", "budget-policy-digest",
                ("check-1",),
            ),
            expected_head="", writer_epoch=1,
        )
        self.oracle.allowed_head = plan.event_hash
        committed = self.store.commit_intent(
            self.request(), self.capability, self.authority,
            expected_head=plan.event_hash, writer_epoch=2,
        )
        self.oracle.allowed_head = committed.event_hash
        self._stop_run()
        early = self.store.settle_terminal_validation(
            TerminalValidationSettlementRequest(
                "terminal-settlement-1", "terminal-command-1",
                "terminal-event-1", "repo-1", "run-1", "item-1",
                "effect-1", "plan-1", "revision-1", "check-1", "PLAN",
                "plan-1", plan.event_hash, "CANCELLED_WITHOUT_START",
            )
        )
        self.oracle.allowed_head = early.event_hash
        self.assertFalse(early.slot_released)

        reopened = SQLiteStateStore(
            self.database_path, self.oracle, "repo-1"
        )
        reopened._bind_classification_authority(self.authority)
        reopened.load_verified("repo-1")
        late = self._record_signed_effect_observation(
            EffectObservationRequest(
                "late-observation-1", "late-observe-command-1",
                "late-observation-event-1", "repo-1", "run-1", "item-1",
                "effect-1", "attempt-1", "late-receipt-1",
                self.capability.claim_id, "descriptor-digest", 2,
                "late-settlement-1", "",
            ),
            store=reopened,
        )
        self.oracle.allowed_head = late.event_hash
        connection = sqlite3.connect(self.database_path)
        try:
            body = json.loads(
                connection.execute(
                    "SELECT body_json FROM events WHERE event_id = ?",
                    (late.event_id,),
                ).fetchone()[0]
            )
        finally:
            connection.close()
        self.assertTrue(body["slot_released"])
        self.assertEqual(body["slot_attempt_id"], "attempt-1")
        self.assertEqual(reopened.table_counts()["outstanding_slot"], 0)
        reopened.load_verified("repo-1")

    def test_t23_recovery_rejects_mandatory_late_receipt_slot_retention(
        self,
    ) -> None:
        plan = self.store.accept_plan(
            PlanAcceptanceRequest(
                "plan-1", "plan-command-1", "plan-event-1", "repo-1",
                "run-1", "item-1", "effect-1", "revision-1",
                "descriptor-digest", "scope-1", "budget-policy-digest",
                ("check-1",),
            ),
            expected_head="", writer_epoch=1,
        )
        self.oracle.allowed_head = plan.event_hash
        committed = self.store.commit_intent(
            self.request(), self.capability, self.authority,
            expected_head=plan.event_hash, writer_epoch=2,
        )
        self.oracle.allowed_head = committed.event_hash
        self._stop_run()
        early = self.store.settle_terminal_validation(
            TerminalValidationSettlementRequest(
                "terminal-settlement-1", "terminal-command-1",
                "terminal-event-1", "repo-1", "run-1", "item-1",
                "effect-1", "plan-1", "revision-1", "check-1", "PLAN",
                "plan-1", plan.event_hash, "CANCELLED_WITHOUT_START",
            )
        )
        self.oracle.allowed_head = early.event_hash
        self.assertFalse(early.slot_released)
        late = self._record_signed_effect_observation(
            EffectObservationRequest(
                "late-observation-1", "late-observe-command-1",
                "late-observation-event-1", "repo-1", "run-1", "item-1",
                "effect-1", "attempt-1", "late-receipt-1",
                self.capability.claim_id, "descriptor-digest", 2,
                "late-settlement-1", "",
            )
        )
        connection = sqlite3.connect(self.database_path)
        try:
            body = json.loads(
                connection.execute(
                    "SELECT body_json FROM events WHERE event_id = ?",
                    (late.event_id,),
                ).fetchone()[0]
            )
            self.assertTrue(body["slot_released"])
            body["slot_released"] = False
            event_hash = self.store._event_hash(body)
            body_json = json.dumps(
                body, sort_keys=True, separators=(",", ":")
            )
            connection.execute(
                "UPDATE events SET event_hash = ?, body_json = ? WHERE event_id = ?",
                (event_hash, body_json, late.event_id),
            )
            connection.execute(
                "UPDATE effect_observations SET event_hash = ?, body_json = ? "
                "WHERE observation_id = ?",
                (event_hash, body_json, late.observation_id),
            )
            connection.execute(
                "UPDATE command_outcomes SET event_hash = ? WHERE command_id = ?",
                (event_hash, late.command_id),
            )
            connection.execute(
                "UPDATE runs SET head_hash = ? WHERE run_id = ?",
                (event_hash, "run-1"),
            )
            connection.execute(
                "UPDATE repositories SET catalog_head = ? WHERE repository_id = ?",
                (event_hash, "repo-1"),
            )
            connection.execute(
                "INSERT INTO outstanding_slot (singleton, repository_id, "
                "run_id, logical_effect_id, attempt_id, generation, "
                "origin_kind, origin_id) VALUES (1, ?, ?, ?, ?, 1, "
                "'EXECUTION_INTENT', ?)",
                ("repo-1", "run-1", "effect-1", "attempt-1", "attempt-1"),
            )
            connection.commit()
        finally:
            connection.close()
        self.oracle.allowed_head = event_hash

        with self.assertRaisesRegex(
            StorageIntegrityError, "effect observation semantics"
        ):
            self.store.load_verified("repo-1")

    def test_t23_correction_after_t26_releases_failed_final_slot(
        self,
    ) -> None:
        observation = self._record_validator_result(verdict="FAIL")
        applied = self.store._apply_validator_observation(
            ValidationApplicationRequest(
                "application-1", "apply-command-1", "apply-event-1",
                "repo-1", "run-1", "item-1", "effect-1", "revision-1",
                "check-1", "validator-attempt-1", "validator-observation-1",
            ),
            classification=self._classification(observation, "FINAL"),
        )
        self.oracle.allowed_head = applied.event_hash
        unknown = self._record_signed_effect_observation(
            EffectObservationRequest(
                "late-unknown-observation", "late-unknown-command",
                "late-unknown-event", "repo-1", "run-1", "item-1",
                "effect-1", "attempt-1", "late-unknown-receipt",
                self.capability.claim_id, "descriptor-digest", None,
                "late-unknown-settlement", "",
            )
        )
        self.oracle.allowed_head = unknown.event_hash
        connection = sqlite3.connect(self.database_path)
        try:
            plan_hash = connection.execute(
                "SELECT event_hash FROM validation_plans WHERE plan_id = 'plan-1'"
            ).fetchone()[0]
        finally:
            connection.close()
        terminal = self.store.settle_terminal_validation(
            TerminalValidationSettlementRequest(
                "terminal-settlement-1", "terminal-command-1",
                "terminal-event-1", "repo-1", "run-1", "item-1",
                "effect-1", "plan-1", "revision-1", "check-2", "PLAN",
                "plan-1", plan_hash, "CANCELLED_WITHOUT_START",
            )
        )
        self.oracle.allowed_head = terminal.event_hash
        self.assertFalse(terminal.slot_released)

        corrected = self._record_signed_effect_observation(
            EffectObservationRequest(
                "late-known-observation", "late-known-command",
                "late-known-event", "repo-1", "run-1", "item-1",
                "effect-1", "attempt-1", "late-known-receipt",
                self.capability.claim_id, "descriptor-digest", 3,
                "late-known-settlement", "",
            )
        )
        self.oracle.allowed_head = corrected.event_hash
        connection = sqlite3.connect(self.database_path)
        try:
            body = json.loads(
                connection.execute(
                    "SELECT body_json FROM events WHERE event_id = ?",
                    (corrected.event_id,),
                ).fetchone()[0]
            )
        finally:
            connection.close()
        self.assertEqual(corrected.resulting_state, LifecycleState.FAILED_FINAL)
        self.assertTrue(body["slot_released"])
        self.assertEqual(self.store.table_counts()["outstanding_slot"], 0)
        self.store.load_verified("repo-1")

    def test_t26_settles_started_validator_from_authoritative_cessation(
        self,
    ) -> None:
        parent = self._record_effect_observation(check_ids=("check-1",))
        intent, capability = self._validator_intent(parent)
        committed = self.store.commit_validator_intent(
            intent, capability, self.authority
        )
        self.oracle.allowed_head = committed.event_hash
        cessation = self._record_validator_cessation_for()
        settlement_request = BudgetSettlementRequest(
            "validator-settlement-1", "validator-reservation-1", "",
            BudgetDisposition.CONSUMED, 1, "cessation-1",
            "VALIDATOR_CESSATION_COST_SETTLED",
        )
        settlement = self.store._settle_budget(
            settlement_request,
            self.authority.issue_settlement_proof(
                "validator-settlement-proof-1", settlement_request
            ),
            self.authority,
        )
        self.oracle.allowed_head = settlement.settlement_hash
        self._stop_run()
        request = TerminalValidationSettlementRequest(
            "terminal-settlement-1", "terminal-command-1", "terminal-event-1",
            "repo-1", "run-1", "item-1", "effect-1", "plan-1",
            "revision-1", "check-1", "VALIDATOR_CESSATION",
            "cessation-1", cessation.event_hash, "CANCELLED_AFTER_START",
            "validator-intent-1", "validator-attempt-1", "cessation-1",
            cessation.event_hash,
        )
        settled = self.store.settle_terminal_validation(request)
        self.oracle.allowed_head = settled.event_hash
        replay = self.store.settle_terminal_validation(
            replace(
                request,
                terminal_settlement_id="terminal-settlement-retry",
                command_id="terminal-command-retry",
                event_id="terminal-event-retry",
            )
        )

        self.assertEqual(settled.resulting_state, LifecycleState.STOPPED)
        self.assertTrue(settled.slot_released)
        self.assertTrue(replay.replayed)
        self.assertEqual(replay.terminal_settlement_id, "terminal-settlement-1")
        self.assertEqual(self.store.table_counts()["outstanding_slot"], 0)
        self.assertEqual(
            self.store.table_counts()["terminal_validation_settlements"], 1
        )
        self.store.load_verified("repo-1")

    def test_t24_retains_result_after_t26_started_cancellation(self) -> None:
        parent = self._record_effect_observation(check_ids=("check-1",))
        intent, capability = self._validator_intent(parent)
        committed = self.store.commit_validator_intent(
            intent, capability, self.authority
        )
        self.oracle.allowed_head = committed.event_hash
        cessation = self._record_validator_cessation_for(
            result_available=True
        )
        settlement_request = BudgetSettlementRequest(
            "validator-settlement-1", "validator-reservation-1", "",
            BudgetDisposition.CONSUMED, 1, "validator-result-1",
            "VALIDATOR_USAGE_REPORTED",
        )
        settlement = self.store._settle_budget(
            settlement_request,
            self.authority.issue_settlement_proof(
                "validator-settlement-proof-1", settlement_request
            ),
            self.authority,
        )
        self.oracle.allowed_head = settlement.settlement_hash
        self._stop_run()
        terminal = self.store.settle_terminal_validation(
            TerminalValidationSettlementRequest(
                "terminal-settlement-1", "terminal-command-1",
                "terminal-event-1", "repo-1", "run-1", "item-1",
                "effect-1", "plan-1", "revision-1", "check-1",
                "VALIDATOR_CESSATION", "cessation-1", cessation.event_hash,
                "CANCELLED_AFTER_START", "validator-intent-1",
                "validator-attempt-1", "cessation-1", cessation.event_hash,
            )
        )
        self.oracle.allowed_head = terminal.event_hash
        late = self.store._record_validator_observation(
            ValidatorObservationRequest(
                "validator-observation-1", "validator-observe-command-1",
                "validator-observation-event-1", "repo-1", "run-1",
                "item-1", "effect-1", "validator-intent-1",
                "validator-attempt-1", "validator-result-1",
                capability.claim_id, "revision-1", "check-1", "input-1",
                "result-digest-1", "PASS", 1, "validator-settlement-1",
                settlement.settlement_hash,
            )
        )
        self.oracle.allowed_head = late.event_hash

        self.assertEqual(late.resulting_state, LifecycleState.STOPPED)
        self.assertEqual(self.store.table_counts()["outstanding_slot"], 0)
        connection = sqlite3.connect(self.database_path)
        try:
            disposition = connection.execute(
                "SELECT disposition FROM terminal_validation_settlements"
            ).fetchone()[0]
        finally:
            connection.close()
        self.assertEqual(disposition, "CANCELLED_AFTER_START")
        self.store.load_verified("repo-1")

    def test_recovery_rejects_post_terminal_cessation_state_change(self) -> None:
        parent = self._record_effect_observation(check_ids=("check-1",))
        intent, capability = self._validator_intent(parent)
        committed = self.store.commit_validator_intent(
            intent, capability, self.authority
        )
        self.oracle.allowed_head = committed.event_hash
        self._stop_run()
        cessation = self._record_validator_cessation_for()
        connection = sqlite3.connect(self.database_path)
        try:
            body = json.loads(
                connection.execute(
                    "SELECT body_json FROM events WHERE event_id = ?",
                    (cessation.event_id,),
                ).fetchone()[0]
            )
            body["lifecycle_to"] = LifecycleState.COMPLETED.value
            event_hash = self.store._event_hash(body)
            body_json = json.dumps(
                body, sort_keys=True, separators=(",", ":")
            )
            connection.execute(
                "UPDATE events SET event_hash = ?, body_json = ? "
                "WHERE event_id = ?",
                (event_hash, body_json, cessation.event_id),
            )
            connection.execute(
                "UPDATE validator_cessations SET event_hash = ?, "
                "resulting_state = ?, body_json = ? WHERE cessation_id = ?",
                (
                    event_hash, LifecycleState.COMPLETED.value, body_json,
                    cessation.cessation_id,
                ),
            )
            connection.execute(
                "UPDATE command_outcomes SET event_hash = ? WHERE command_id = ?",
                (event_hash, cessation.command_id),
            )
            connection.execute(
                "UPDATE runs SET lifecycle_state = ?, head_hash = ? WHERE run_id = ?",
                (LifecycleState.COMPLETED.value, event_hash, "run-1"),
            )
            connection.execute(
                "UPDATE repositories SET catalog_head = ? WHERE repository_id = ?",
                (event_hash, "repo-1"),
            )
            connection.commit()
        finally:
            connection.close()
        self.oracle.allowed_head = event_hash

        with self.assertRaisesRegex(
            StorageIntegrityError, "terminal lifecycle"
        ):
            self.store.load_verified("repo-1")

    def test_t26_rejects_historical_result_after_successor_intent(self) -> None:
        observation = self._record_validator_result(
            verdict="FAIL", only_check=True
        )
        cessation = self._record_validator_cessation_for(
            result_available=True
        )
        failed = self.store._apply_validator_observation(
            ValidationApplicationRequest(
                "application-1", "apply-command-1", "apply-event-1",
                "repo-1", "run-1", "item-1", "effect-1", "revision-1",
                "check-1", "validator-attempt-1", "validator-observation-1",
            ),
            classification=self._classification(observation, "RECOVERABLE"),
        )
        self.oracle.allowed_head = failed.event_hash
        recovery_request, attestation, parent_event_hash = (
            self._validation_recovery_pair(failed)
        )
        recovered = self.store.resolve_validation_blocker(
            recovery_request, attestation, self.authority
        )
        self.oracle.allowed_head = recovered.event_hash
        successor, successor_capability = self._validator_intent(
            replace(observation, event_hash=parent_event_hash),
            suffix="2", check_id="check-1", recovery_id="recovery-1",
        )
        committed = self.store.commit_validator_intent(
            successor, successor_capability, self.authority
        )
        self.oracle.allowed_head = committed.event_hash
        self._stop_run()

        with self.assertRaisesRegex(DispatchDenied, "current attempt"):
            self.store.settle_terminal_validation(
                TerminalValidationSettlementRequest(
                    "terminal-settlement-1", "terminal-command-1",
                    "terminal-event-1", "repo-1", "run-1", "item-1",
                    "effect-1", "plan-1", "revision-1", "check-1",
                    "VALIDATOR_OBSERVATION", "validator-observation-1",
                    observation.event_hash, "FAILED", "validator-intent-1",
                    "validator-attempt-1", "cessation-1",
                    cessation.event_hash,
                )
            )
        self.assertEqual(
            self.store.table_counts()["terminal_validation_settlements"], 0
        )
        self.assertEqual(self.store.table_counts()["outstanding_slot"], 1)

    def test_t26_rejects_terminal_history_without_permanent_fence(self) -> None:
        observation = self._record_validator_result(verdict="FAIL")
        applied = self.store._apply_validator_observation(
            ValidationApplicationRequest(
                "application-1", "apply-command-1", "apply-event-1",
                "repo-1", "run-1", "item-1", "effect-1", "revision-1",
                "check-1", "validator-attempt-1", "validator-observation-1",
            ),
            classification=self._classification(observation, "FINAL"),
        )
        self.oracle.allowed_head = applied.event_hash
        connection = sqlite3.connect(self.database_path)
        try:
            plan_hash = connection.execute(
                "SELECT event_hash FROM validation_plans WHERE plan_id = 'plan-1'"
            ).fetchone()[0]
            connection.execute(
                "DELETE FROM dispatch_fences WHERE fence_id = "
                "'failed-final:application-1'"
            )
            connection.commit()
        finally:
            connection.close()

        with self.assertRaisesRegex(StorageIntegrityError, "dispatch-fence"):
            self.store.settle_terminal_validation(
                TerminalValidationSettlementRequest(
                    "terminal-settlement-1", "terminal-command-1",
                    "terminal-event-1", "repo-1", "run-1", "item-1",
                    "effect-1", "plan-1", "revision-1", "check-2",
                    "PLAN", "plan-1", plan_hash,
                    "CANCELLED_WITHOUT_START",
                )
            )
        self.assertEqual(
            self.store.table_counts()["terminal_validation_settlements"], 0
        )

    def test_t26_consumes_terminal_t25_nonexecution_proof(self) -> None:
        parent = self._record_effect_observation(check_ids=("check-1",))
        validator_request, validator_capability = self._validator_intent(parent)
        committed = self.store.commit_validator_intent(
            validator_request, validator_capability, self.authority
        )
        self.oracle.allowed_head = committed.event_hash
        self._stop_run()
        validator_path = self.database_path.parent / "synthetic-validator.sqlite3"
        adapter = SyntheticValidatorAdapter(validator_path)
        adapter._canonical_repository_id = "repo-1"
        adapter._canonical_ledger_path = validator_path.resolve()
        attestation = self.authority.issue_nonexecution_attestation(
            "terminal-nonexecution-attestation", "terminal-nonexecution-seal",
            "VALIDATOR", adapter._target_digest("repo-1"),
            validator_capability.claim_id, "VALIDATOR:validator-intent-1",
            committed.event_hash, "validator-reservation-1", "repo-1",
            "run-1", "item-1", "effect-1", "validator-attempt-1",
        )
        seal = adapter.seal_nonexecution(attestation, self.authority)
        nonexecution_request = BudgetSettlementRequest(
            "terminal-nonexecution", "validator-reservation-1", "",
            BudgetDisposition.RELEASED, None, "terminal-nonexecution-evidence",
            "NONDISPATCH_PROVEN", non_dispatch_proven=True,
            zero_liability_proven=True, all_obligations_settled=True,
            attempt_id="validator-attempt-1",
            nonexecution_seal_id=seal.seal_id,
        )
        nonexecution = self.store._settle_budget(
            nonexecution_request,
            self.authority.issue_settlement_proof(
                "terminal-nonexecution-proof", nonexecution_request
            ),
            self.authority,
        )
        self.oracle.allowed_head = nonexecution.settlement_hash
        connection = sqlite3.connect(self.database_path)
        try:
            status = connection.execute(
                "SELECT status FROM validator_intents WHERE "
                "validator_intent_id = 'validator-intent-1'"
            ).fetchone()[0]
        finally:
            connection.close()
        self.assertEqual(status, "ACTIVE")
        request = TerminalValidationSettlementRequest(
            "terminal-settlement-1", "terminal-command-1", "terminal-event-1",
            "repo-1", "run-1", "item-1", "effect-1", "plan-1",
            "revision-1", "check-1", "NONDISPATCH_PROVEN",
            "terminal-nonexecution", nonexecution.settlement_hash,
            "CANCELLED_WITHOUT_START", "validator-intent-1",
            "validator-attempt-1",
        )
        settled = self.store.settle_terminal_validation(request)
        self.oracle.allowed_head = settled.event_hash

        self.assertEqual(settled.resulting_state, LifecycleState.STOPPED)
        self.assertTrue(settled.slot_released)
        self.assertEqual(self.store.table_counts()["outstanding_slot"], 0)
        self.store.load_verified("repo-1")

    def test_c05_final_failure_with_unsettled_accounting_retains_slot(self) -> None:
        observation = self._record_validator_result(
            verdict="FAIL", only_check=True
        )
        connection = sqlite3.connect(self.database_path)
        try:
            connection.execute(
                "UPDATE budget_reservations SET disposition = 'RELEASED' "
                "WHERE reservation_id = 'reservation-1'"
            )
            connection.commit()
        finally:
            connection.close()

        with patch.object(self.store, "_verify_projections"):
            applied = self.store._apply_validator_observation(
                ValidationApplicationRequest(
                    "application-1", "apply-command-1", "apply-event-1",
                    "repo-1", "run-1", "item-1", "effect-1", "revision-1",
                    "check-1", "validator-attempt-1",
                    "validator-observation-1",
                ),
                classification=self._classification(observation, "FINAL"),
            )

        self.assertEqual(applied.resulting_state.value, "FAILED_FINAL")
        self.assertEqual(self.store.table_counts()["outstanding_slot"], 1)

    def test_c05_final_fence_denies_matching_item_or_effect(self) -> None:
        observation = self._record_validator_result(
            verdict="FAIL", only_check=True
        )
        applied = self.store._apply_validator_observation(
            ValidationApplicationRequest(
                "application-1", "apply-command-1", "apply-event-1",
                "repo-1", "run-1", "item-1", "effect-1", "revision-1",
                "check-1", "validator-attempt-1", "validator-observation-1",
            ),
            classification=self._classification(observation, "FINAL"),
        )
        self.oracle.allowed_head = applied.event_hash
        for suffix, item_id, effect_id, writer_epoch in (
            ("same-item", "item-1", "effect-2", 30),
            ("same-effect", "item-2", "effect-1", 32),
        ):
            grant = SyntheticGrant(
                f"grant-{suffix}", "repo-1", effect_id, f"attempt-{suffix}",
                f"scope-{suffix}",
            )
            self.authority.register(grant)
            capability = self.authority.claim(*grant.__dict__.values())
            with self.subTest(scope=suffix), self.assertRaisesRegex(
                DispatchDenied, "dispatch fence"
            ):
                self._commit_planned_intent(
                    replace(
                        self.request(), run_id=f"run-{suffix}", item_id=item_id,
                        command_id=f"command-{suffix}",
                        event_id=f"event-{suffix}", logical_effect_id=effect_id,
                        attempt_id=f"attempt-{suffix}",
                        permission_use_id=f"permission-{suffix}",
                        reservation_id=f"reservation-{suffix}",
                    ),
                    capability, self.authority,
                    expected_head=self.oracle.allowed_head,
                    writer_epoch=writer_epoch,
                )

    def test_c05_exact_replay_rejects_rebound_request(self) -> None:
        observation = self._record_validator_result(
            verdict="FAIL", only_check=True
        )
        request = ValidationApplicationRequest(
            "application-1", "apply-command-1", "apply-event-1",
            "repo-1", "run-1", "item-1", "effect-1", "revision-1",
            "check-1", "validator-attempt-1", "validator-observation-1",
        )
        applied = self.store._apply_validator_observation(
            request, classification=self._classification(observation, "FINAL")
        )
        self.oracle.allowed_head = applied.event_hash
        for rebound in (
            replace(request, item_id="item-2"),
            replace(request, revision_digest="revision-2"),
            replace(request, validator_attempt_id="validator-attempt-2"),
        ):
            with self.subTest(rebound=rebound):
                with self.assertRaisesRegex(StorageIntegrityError, "identity"):
                    self.store._apply_validator_observation(rebound)

    def test_c05_replay_rejects_supplied_contradictory_classification(self) -> None:
        observation = self._record_validator_result(
            verdict="FAIL", only_check=True
        )
        request = ValidationApplicationRequest(
            "application-1", "apply-command-1", "apply-event-1",
            "repo-1", "run-1", "item-1", "effect-1", "revision-1",
            "check-1", "validator-attempt-1", "validator-observation-1",
        )
        applied = self.store._apply_validator_observation(
            request, classification=self._classification(observation, "FINAL")
        )
        self.oracle.allowed_head = applied.event_hash
        contradictory = self.authority.issue_classification(
            "classification-contradictory", "repo-1", "run-1", "item-1",
            "effect-1", "revision-1", "check-1", "validator-attempt-1",
            "validator-observation-1", observation.event_hash,
            "result-digest-1", verdict="FAIL", policy_id="failure-policy",
            policy_version="1", classification="RECOVERABLE",
        )
        with self.assertRaisesRegex(StorageIntegrityError, "contradictory"):
            self.store._apply_validator_observation(
                request, classification=contradictory
            )

    def test_c05_rejects_replacement_issuer_after_restart(self) -> None:
        observation = self._record_validator_result(
            verdict="FAIL", only_check=True
        )
        replacement = SyntheticAuthority(b"r" * 32)
        reopened = SQLiteStateStore(self.database_path, self.oracle, "repo-1")
        with self.assertRaisesRegex(DispatchDenied, "accepted plan"):
            reopened._bind_classification_authority(replacement)
        self.assertEqual(observation.resulting_state, LifecycleState.VALIDATING)

    def test_c05_rejects_tampered_event_history_before_application(self) -> None:
        self._record_validator_result(verdict="FAIL", only_check=True)
        connection = sqlite3.connect(self.database_path)
        try:
            body_json = connection.execute(
                "SELECT body_json FROM events "
                "WHERE event_id = 'validator-observation-event-1'"
            ).fetchone()[0]
            body = json.loads(body_json)
            body["verdict"] = "PASS"
            connection.execute(
                "UPDATE events SET body_json = ? "
                "WHERE event_id = 'validator-observation-event-1'",
                (json.dumps(body, sort_keys=True, separators=(",", ":")),),
            )
            connection.execute(
                "UPDATE validator_observations SET verdict = 'PASS' "
                "WHERE observation_id = 'validator-observation-1'"
            )
            connection.commit()
        finally:
            connection.close()
        with self.assertRaisesRegex(StorageIntegrityError, "event body hash"):
            self.store._apply_validator_observation(
                ValidationApplicationRequest(
                    "application-1", "apply-command-1", "apply-event-1",
                    "repo-1", "run-1", "item-1", "effect-1", "revision-1",
                    "check-1", "validator-attempt-1",
                    "validator-observation-1",
                )
            )
        self.assertEqual(self.store.table_counts()["validation_applications"], 0)

    def test_c05_classification_policy_is_closed(self) -> None:
        observation = self._record_validator_result(
            verdict="FAIL", only_check=True
        )
        with self.assertRaisesRegex(ValueError, "unsupported.*policy"):
            self.authority.issue_classification(
                "classification-other", "repo-1", "run-1", "item-1",
                "effect-1", "revision-1", "check-1",
                "validator-attempt-1", "validator-observation-1",
                observation.event_hash, "result-digest-1", verdict="FAIL",
                policy_id="other-policy", policy_version="1",
                classification="FINAL",
            )

    def test_c05_rejects_pass_classification_and_untrusted_fail_evidence(self) -> None:
        pass_observation = self._record_validator_result(only_check=True)
        pass_classification = self.authority.issue_classification(
            "classification-pass", "repo-1", "run-1", "item-1", "effect-1",
            "revision-1", "check-1", "validator-attempt-1",
            "validator-observation-1", pass_observation.event_hash,
            "result-digest-1", verdict="FAIL", policy_id="failure-policy",
            policy_version="1", classification="FINAL",
        )
        with self.assertRaisesRegex(DispatchDenied, "PASS application"):
            self.store._apply_validator_observation(
                ValidationApplicationRequest(
                    "application-1", "apply-command-1", "apply-event-1",
                    "repo-1", "run-1", "item-1", "effect-1", "revision-1",
                    "check-1", "validator-attempt-1",
                    "validator-observation-1",
                ),
                classification=pass_classification,
            )

    def test_c05_rejects_forged_and_rebound_failure_classification(self) -> None:
        observation = self._record_validator_result(
            verdict="FAIL", only_check=True
        )
        valid = self._classification(observation, "FINAL")
        forged = replace(valid, issuer_mac="0" * len(valid.issuer_mac))
        rebound = self.authority.issue_classification(
            "classification-rebound", "repo-1", "run-1", "item-1",
            "effect-1", "revision-1", "check-1", "validator-attempt-1",
            "validator-observation-1", "wrong-event-hash", "result-digest-1",
            verdict="FAIL", policy_id="failure-policy", policy_version="1",
            classification="FINAL",
        )
        for evidence in (forged, rebound):
            with self.subTest(classification_id=evidence.classification_id):
                with self.assertRaises(DispatchDenied):
                    self.store._apply_validator_observation(
                        ValidationApplicationRequest(
                            "application-1", "apply-command-1", "apply-event-1",
                            "repo-1", "run-1", "item-1", "effect-1",
                            "revision-1", "check-1", "validator-attempt-1",
                            "validator-observation-1",
                        ),
                        classification=evidence,
                    )
        self.assertEqual(self.store.table_counts()["validation_applications"], 0)

    def test_c05_recovery_rejects_tampered_classification_projection(self) -> None:
        observation = self._record_validator_result(
            verdict="FAIL", only_check=True
        )
        applied = self.store._apply_validator_observation(
            ValidationApplicationRequest(
                "application-1", "apply-command-1", "apply-event-1",
                "repo-1", "run-1", "item-1", "effect-1", "revision-1",
                "check-1", "validator-attempt-1", "validator-observation-1",
            ),
            classification=self._classification(observation, "FINAL"),
        )
        self.oracle.allowed_head = applied.event_hash
        connection = sqlite3.connect(self.database_path)
        try:
            connection.execute(
                "UPDATE validation_applications SET classification = 'RECOVERABLE' "
                "WHERE application_id = 'application-1'"
            )
            connection.commit()
        finally:
            connection.close()
        with self.assertRaisesRegex(StorageIntegrityError, "validation-application"):
            self.store.load_verified("repo-1")

    def test_c05_recovery_rejects_tampered_final_fence_scope(self) -> None:
        observation = self._record_validator_result(
            verdict="FAIL", only_check=True
        )
        applied = self.store._apply_validator_observation(
            ValidationApplicationRequest(
                "application-1", "apply-command-1", "apply-event-1",
                "repo-1", "run-1", "item-1", "effect-1", "revision-1",
                "check-1", "validator-attempt-1", "validator-observation-1",
            ),
            classification=self._classification(observation, "FINAL"),
        )
        self.oracle.allowed_head = applied.event_hash
        connection = sqlite3.connect(self.database_path)
        try:
            connection.execute(
                "UPDATE dispatch_fences SET item_id = 'item-2' "
                "WHERE reason_code = 'FAILED_FINAL_APPLICATION'"
            )
            connection.commit()
        finally:
            connection.close()
        with self.assertRaisesRegex(StorageIntegrityError, "dispatch-fence"):
            self.store.load_verified("repo-1")

    def test_c05_recovery_rejects_released_terminal_accounting(self) -> None:
        observation = self._record_validator_result(
            verdict="FAIL", only_check=True
        )
        applied = self.store._apply_validator_observation(
            ValidationApplicationRequest(
                "application-1", "apply-command-1", "apply-event-1",
                "repo-1", "run-1", "item-1", "effect-1", "revision-1",
                "check-1", "validator-attempt-1", "validator-observation-1",
            ),
            classification=self._classification(observation, "FINAL"),
        )
        self.oracle.allowed_head = applied.event_hash
        connection = sqlite3.connect(self.database_path)
        try:
            connection.execute(
                "UPDATE budget_reservations SET disposition = 'RELEASED' "
                "WHERE reservation_id = 'reservation-1'"
            )
            connection.commit()
        finally:
            connection.close()

        with self.assertRaises(StorageIntegrityError):
            self.store.load_verified("repo-1")

    def test_c05_late_unknown_accounting_recovers_for_correction(self) -> None:
        observation = self._record_validator_result(
            verdict="FAIL", only_check=True
        )
        applied = self.store._apply_validator_observation(
            ValidationApplicationRequest(
                "application-1", "apply-command-1", "apply-event-1",
                "repo-1", "run-1", "item-1", "effect-1", "revision-1",
                "check-1", "validator-attempt-1", "validator-observation-1",
            ),
            classification=self._classification(observation, "FINAL"),
        )
        self.assertEqual(self.store.table_counts()["outstanding_slot"], 0)
        self.oracle.allowed_head = applied.event_hash
        connection = sqlite3.connect(self.database_path)
        try:
            previous_hash = connection.execute(
                "SELECT settlement_head_hash FROM budget_reservations "
                "WHERE reservation_id = 'reservation-1'"
            ).fetchone()[0]
        finally:
            connection.close()
        unknown = BudgetSettlementRequest(
            "failed-final-late-unknown", "reservation-1", previous_hash,
            BudgetDisposition.UNKNOWN_WORST_CASE_CHARGED, None,
            "failed-final-late-evidence", "ADDITIONAL_LIABILITY_UNKNOWN",
            additional_liability=True,
        )
        unknown_receipt = self.store._settle_budget(
            unknown,
            self.authority.issue_settlement_proof(
                "failed-final-late-proof", unknown
            ),
            self.authority,
        )
        self.oracle.allowed_head = unknown_receipt.settlement_hash
        reopened = SQLiteStateStore(self.database_path, self.oracle, "repo-1")
        reopened._bind_classification_authority(self.authority)
        reopened.load_verified("repo-1")

        correction = BudgetSettlementRequest(
            "failed-final-late-correction", "reservation-1",
            unknown_receipt.settlement_hash, BudgetDisposition.ADJUSTED, 3,
            "failed-final-authoritative-evidence", "AUTHORITATIVE_CORRECTION",
        )
        corrected = reopened._settle_budget(
            correction,
            self.authority.issue_settlement_proof(
                "failed-final-correction-proof", correction
            ),
            self.authority,
        )
        self.oracle.allowed_head = corrected.settlement_hash
        reopened.load_verified("repo-1")
        connection = sqlite3.connect(self.database_path)
        try:
            charged_units, uncertainty, lifecycle_state = connection.execute(
                "SELECT b.charged_units, b.uncertainty, r.lifecycle_state "
                "FROM budget_reservations b JOIN runs r ON r.run_id = b.run_id "
                "WHERE b.reservation_id = 'reservation-1'"
            ).fetchone()
        finally:
            connection.close()
        self.assertEqual((charged_units, uncertainty), (3, 0))
        self.assertEqual(lifecycle_state, "FAILED_FINAL")
        connection = sqlite3.connect(self.database_path)
        try:
            fences = connection.execute(
                "SELECT fence_id, reason_code, originating_event_id FROM "
                "dispatch_fences ORDER BY fence_id"
            ).fetchall()
        finally:
            connection.close()
        self.assertEqual(
            fences,
            [(
                "failed-final:application-1",
                "FAILED_FINAL_APPLICATION",
                "apply-event-1",
            )],
        )
        self.assertEqual(reopened.table_counts()["outstanding_slot"], 0)

    def test_c05_recovery_rejects_tampered_application_projection(self) -> None:
        self._record_validator_result(only_check=True)
        applied = self.store._apply_validator_observation(
            ValidationApplicationRequest(
                "application-1", "apply-command-1", "apply-event-1", "repo-1",
                "run-1", "item-1", "effect-1", "revision-1", "check-1",
                "validator-attempt-1", "validator-observation-1",
            ),
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

    def test_c05_recovery_rejects_self_consistent_completed_forgery(self) -> None:
        self._record_validator_result(only_check=True)
        applied = self.store._apply_validator_observation(
            ValidationApplicationRequest(
                "application-1", "apply-command-1", "apply-event-1",
                "repo-1", "run-1", "item-1", "effect-1", "revision-1",
                "check-1", "validator-attempt-1",
                "validator-observation-1",
            ),
        )
        connection = sqlite3.connect(self.database_path)
        try:
            body = json.loads(
                connection.execute(
                    "SELECT body_json FROM events WHERE event_id = ?",
                    ("apply-event-1",),
                ).fetchone()[0]
            )
            body["lifecycle_to"] = LifecycleState.COMPLETED.value
            body["continuation_cursor"] = None
            event_hash = self.store._event_hash(body)
            body_json = json.dumps(
                body, sort_keys=True, separators=(",", ":")
            )
            connection.execute(
                "UPDATE events SET event_hash = ?, body_json = ? "
                "WHERE event_id = ?",
                (event_hash, body_json, "apply-event-1"),
            )
            connection.execute(
                "UPDATE validation_applications SET event_hash = ?, "
                "resulting_state = ?, continuation_cursor = NULL, "
                "body_json = ? WHERE application_id = ?",
                (
                    event_hash, LifecycleState.COMPLETED.value, body_json,
                    "application-1",
                ),
            )
            connection.execute(
                "UPDATE command_outcomes SET event_hash = ? WHERE command_id = ?",
                (event_hash, "apply-command-1"),
            )
            connection.execute(
                "UPDATE runs SET lifecycle_state = ?, continuation_cursor = NULL, "
                "head_hash = ? WHERE run_id = ?",
                (LifecycleState.COMPLETED.value, event_hash, "run-1"),
            )
            connection.execute(
                "UPDATE repositories SET catalog_head = ? WHERE repository_id = ?",
                (event_hash, "repo-1"),
            )
            connection.commit()
        finally:
            connection.close()
        self.oracle.allowed_head = event_hash

        with self.assertRaisesRegex(
            StorageIntegrityError, "validation application semantics"
        ):
            self.store.load_verified("repo-1")

    def test_c05_recovery_rejects_self_consistent_pass_slot_release(self) -> None:
        self._record_validator_result(only_check=True)
        self.store._apply_validator_observation(
            ValidationApplicationRequest(
                "application-1", "apply-command-1", "apply-event-1",
                "repo-1", "run-1", "item-1", "effect-1", "revision-1",
                "check-1", "validator-attempt-1",
                "validator-observation-1",
            ),
        )
        connection = sqlite3.connect(self.database_path)
        try:
            body = json.loads(
                connection.execute(
                    "SELECT body_json FROM events WHERE event_id = ?",
                    ("apply-event-1",),
                ).fetchone()[0]
            )
            body["slot_released"] = True
            connection.execute("DELETE FROM outstanding_slot")
            connection.commit()
        finally:
            connection.close()
        self.oracle.allowed_head = self._rewrite_application_tail(body)

        with self.assertRaisesRegex(
            StorageIntegrityError, "validation application semantics"
        ):
            self.store.load_verified("repo-1")

    def test_c05_recovery_rejects_self_consistent_final_slot_retention(self) -> None:
        observation = self._record_validator_result(
            verdict="FAIL", only_check=True
        )
        self.store._apply_validator_observation(
            ValidationApplicationRequest(
                "application-1", "apply-command-1", "apply-event-1",
                "repo-1", "run-1", "item-1", "effect-1", "revision-1",
                "check-1", "validator-attempt-1",
                "validator-observation-1",
            ),
            classification=self._classification(observation, "FINAL"),
        )
        connection = sqlite3.connect(self.database_path)
        try:
            body = json.loads(
                connection.execute(
                    "SELECT body_json FROM events WHERE event_id = ?",
                    ("apply-event-1",),
                ).fetchone()[0]
            )
            body["slot_released"] = False
            connection.execute(
                "INSERT INTO outstanding_slot (singleton, repository_id, "
                "run_id, logical_effect_id, attempt_id, generation, "
                "origin_kind, origin_id) VALUES (1, ?, ?, ?, ?, 1, "
                "'EXECUTION_INTENT', ?)",
                ("repo-1", "run-1", "effect-1", "attempt-1", "attempt-1"),
            )
            connection.commit()
        finally:
            connection.close()
        self.oracle.allowed_head = self._rewrite_application_tail(body)

        with self.assertRaisesRegex(
            StorageIntegrityError, "validation application semantics"
        ):
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

    def test_f20_missing_containment_denies_before_validator_intent(self) -> None:
        observation = self._record_effect_observation()
        request, capability = self._validator_intent(observation)
        request = replace(request, containment_spec_json="")

        with self.assertRaisesRegex((ValueError, DispatchDenied), "containment"):
            self.store.commit_validator_intent(
                request, capability, self.authority
            )

        self.assertEqual(self.store.table_counts()["validator_intents"], 0)
        self.assertEqual(self.store.table_counts()["permission_uses"], 1)
        self.assertEqual(self.store.table_counts()["budget_reservations"], 1)

    def test_f20_closed_checker_denies_mutation_escape_and_unbounded_output(self) -> None:
        observation = self._record_effect_observation(check_ids=("check-1",))
        intent, capability = self._validator_intent(observation)
        spec = parse_validator_containment_spec(intent.containment_spec_json)
        valid = SyntheticValidatorRequest(
            "repo-1", "effect-1", "revision-1", "check-1", "input-1",
            "validator-attempt-1", "read-only-scope-1", "result-digest-1",
            "PASS", capability.containment_digest, spec.allowed_actions,
            spec.input_root, f"{spec.output_root}/result.json",
            f"{spec.scratch_root}/work",
            synthetic_validator_output_size("result-digest-1", "PASS"),
        )
        mutations = (
            replace(valid, requested_actions=("WRITE_TARGET",)),
            replace(valid, requested_actions=("WRITE_GIT",)),
            replace(valid, requested_actions=("DEPLOY",)),
            replace(valid, requested_actions=("WRITE_PRODUCTION_DATA",)),
            replace(valid, requested_actions=("WRITE_AUTHORITY",)),
            replace(valid, requested_actions=("REPAIR_CONTROLLER_STATE",)),
            replace(valid, output_path="../escape"),
            replace(valid, output_bytes=spec.max_output_bytes + 1),
            replace(valid, uses_subprocess=True),
            replace(valid, uses_tool=True),
            replace(valid, uses_network=True),
        )
        for mutation in mutations:
            with self.subTest(mutation=mutation):
                with self.assertRaisesRegex(DispatchDenied, "containment"):
                    validate_synthetic_validator_containment(
                        capability, mutation, intent
                    )
        self.assertEqual(self.store.table_counts()["validator_intents"], 0)
        self.assertEqual(self.store.table_counts()["permission_uses"], 1)
        self.assertEqual(self.store.table_counts()["budget_reservations"], 1)

    def test_f20_final_containment_loss_retains_committed_obligation(self) -> None:
        intent, capability, committed, _adapter, _request = (
            self._prepared_validator_execution()
        )

        def unavailable():
            raise DispatchDenied("validator containment support is unavailable")

        with self.assertRaisesRegex(DispatchDenied, "containment support"):
            self.store._contact_committed_validator(
                intent,
                capability,
                committed,
                self.store._adapter_target_digest("repo-1", "VALIDATOR"),
                self.authority,
                containment_digest=capability.containment_digest,
                containment_verifier=unavailable,
            )

        counts = self.store.table_counts()
        self.assertEqual(self._row_count("adapter_contacts"), 0)
        self.assertEqual(counts["validator_intents"], 1)
        self.assertEqual(counts["permission_uses"], 2)
        self.assertEqual(counts["budget_reservations"], 2)
        self.assertEqual(counts["outstanding_slot"], 1)
        self.store.load_verified("repo-1", authority=self.authority)

    def test_f20_crash_after_contact_retains_contacted_uncertainty(self) -> None:
        intent, capability, committed, adapter, request = (
            self._prepared_validator_execution()
        )
        with self.assertRaises(InjectedFailure):
            adapter._execute_committed(
                capability,
                request,
                self.authority,
                self.store,
                committed,
                intent,
                failure_hook=raise_at(
                    "after_validator_contact_before_result_transaction"
                ),
            )
        self.assertIsNone(adapter.reconcile(capability.claim_id))
        self.assertEqual(self._row_count("adapter_contacts"), 1)
        self.assertEqual(self.store.table_counts()["validator_intents"], 1)
        self.assertEqual(self.store.table_counts()["outstanding_slot"], 1)

    def test_f20_result_commit_crashes_never_launder_containment(self) -> None:
        intent, capability, committed, adapter, request = (
            self._prepared_validator_execution()
        )
        with self.assertRaises(InjectedFailure):
            adapter._execute_committed(
                capability,
                request,
                self.authority,
                self.store,
                committed,
                intent,
                failure_hook=raise_at(
                    "after_validator_result_commit_before_acknowledgement"
                ),
            )
        result = adapter.reconcile(capability.claim_id)
        self.assertIsNotNone(result)
        self.assertEqual(result.containment_version, 1)
        self.assertEqual(
            result.containment_digest, capability.containment_digest
        )
        self.assertEqual(self._row_count("adapter_contacts"), 1)

    def test_f20_result_precommit_crash_keeps_contact_without_result(self) -> None:
        intent, capability, committed, adapter, request = (
            self._prepared_validator_execution()
        )
        with self.assertRaises(InjectedFailure):
            adapter._execute_committed(
                capability,
                request,
                self.authority,
                self.store,
                committed,
                intent,
                failure_hook=raise_at(
                    "after_validator_result_insert_before_commit"
                ),
            )
        self.assertIsNone(adapter.reconcile(capability.claim_id))
        self.assertEqual(self._row_count("adapter_contacts"), 1)
        self.assertEqual(self.store.table_counts()["outstanding_slot"], 1)

    def test_f20_validator_ledger_migration_is_atomic_and_legacy_closed(self) -> None:
        def downgrade(path: Path, *, with_result: bool) -> None:
            SyntheticValidatorAdapter(path)
            connection = sqlite3.connect(path)
            try:
                if with_result:
                    connection.execute(
                        "INSERT INTO synthetic_validator_results VALUES ("
                        "'legacy-claim', 'legacy-result', 'repo-1', 'effect-1', "
                        "'revision-1', 'check-1', 'input-1', 'attempt-1', "
                        "'digest-1', 'PASS', 1, 1, 1, 'old-containment')"
                    )
                connection.execute(
                    "ALTER TABLE synthetic_validator_results RENAME TO "
                    "synthetic_validator_results_v1"
                )
                connection.execute(
                    "CREATE TABLE synthetic_validator_results ("
                    "claim_id TEXT PRIMARY KEY, result_id TEXT NOT NULL UNIQUE, "
                    "repository_id TEXT NOT NULL, logical_effect_id TEXT NOT NULL, "
                    "revision_digest TEXT NOT NULL, check_id TEXT NOT NULL, "
                    "input_digest TEXT NOT NULL, validator_attempt_id TEXT NOT NULL, "
                    "result_digest TEXT NOT NULL, verdict TEXT NOT NULL CHECK "
                    "(verdict IN ('PASS', 'FAIL')), usage_units INTEGER, "
                    "final INTEGER NOT NULL CHECK (final = 1))"
                )
                connection.execute(
                    "INSERT INTO synthetic_validator_results SELECT "
                    "claim_id, result_id, repository_id, logical_effect_id, "
                    "revision_digest, check_id, input_digest, "
                    "validator_attempt_id, result_digest, verdict, usage_units, "
                    "final FROM synthetic_validator_results_v1"
                )
                connection.execute("DROP TABLE synthetic_validator_results_v1")
                connection.execute("DROP TABLE synthetic_validator_metadata")
                connection.execute("PRAGMA user_version = 0")
                connection.commit()
            finally:
                connection.close()

        legacy_path = self.database_path.parent / "legacy-validator.sqlite3"
        downgrade(legacy_path, with_result=True)
        migrated = SyntheticValidatorAdapter(legacy_path)
        legacy_result = migrated.reconcile("legacy-claim")
        self.assertIsNotNone(legacy_result)
        self.assertIsNone(legacy_result.containment_version)
        self.assertIsNone(legacy_result.containment_digest)

        crash_path = self.database_path.parent / "crash-validator.sqlite3"
        downgrade(crash_path, with_result=False)
        with self.assertRaises(InjectedFailure):
            SyntheticValidatorAdapter(
                crash_path,
                migration_failure_hook=raise_at(
                    "after_validator_ledger_migration_writes_before_commit"
                ),
            )
        connection = sqlite3.connect(crash_path)
        try:
            self.assertEqual(
                connection.execute("PRAGMA user_version").fetchone()[0], 0
            )
        finally:
            connection.close()
        SyntheticValidatorAdapter(crash_path)

        partial_path = self.database_path.parent / "partial-validator.sqlite3"
        downgrade(partial_path, with_result=False)
        connection = sqlite3.connect(partial_path)
        try:
            connection.execute(
                "ALTER TABLE synthetic_validator_results ADD COLUMN "
                "containment_version INTEGER"
            )
            connection.commit()
        finally:
            connection.close()
        with self.assertRaisesRegex(DispatchDenied, "legacy result schema"):
            SyntheticValidatorAdapter(partial_path)

    def test_f20_populated_v4_active_intent_migrates_without_permission(self) -> None:
        intent, capability, committed, _adapter, _request = (
            self._prepared_validator_execution()
        )
        connection = sqlite3.connect(self.database_path)
        connection.row_factory = sqlite3.Row
        try:
            body = json.loads(
                connection.execute(
                    "SELECT body_json FROM events WHERE event_id = ?",
                    (committed.event_id,),
                ).fetchone()[0]
            )
            for field in (
                "containment_spec_json",
                "capability_evidence",
                "capability_issuer_fingerprint",
                "containment_binding_version",
                "containment_digest",
            ):
                body.pop(field)
            payload_digest = self.store._event_hash(
                {
                    key: body[key]
                    for key in ValidatorIntentRequest.__dataclass_fields__
                    if key in body
                }
            )
            event_hash = self.store._event_hash(body)
            body_json = json.dumps(body, sort_keys=True, separators=(",", ":"))
            connection.execute(
                "UPDATE events SET event_hash = ?, body_json = ? WHERE event_id = ?",
                (event_hash, body_json, committed.event_id),
            )
            connection.execute(
                "UPDATE validator_intents SET payload_digest = ?, event_hash = ?, "
                "body_json = ? WHERE validator_intent_id = ?",
                (payload_digest, event_hash, body_json, intent.validator_intent_id),
            )
            connection.execute(
                "UPDATE command_outcomes SET payload_digest = ?, event_hash = ? "
                "WHERE command_id = ?",
                (payload_digest, event_hash, intent.command_id),
            )
            connection.execute(
                "UPDATE runs SET head_hash = ? WHERE run_id = ?",
                (event_hash, intent.run_id),
            )
            connection.execute(
                "UPDATE repositories SET catalog_head = ? WHERE repository_id = ?",
                (event_hash, intent.repository_id),
            )
            for column in (
                "containment_binding_version",
                "containment_digest",
                "containment_spec_json",
                "containment_capability_json",
            ):
                connection.execute(
                    f"ALTER TABLE validator_intents DROP COLUMN {column}"
                )
            connection.execute("PRAGMA user_version = 4")
            connection.commit()
        finally:
            connection.close()
        self.oracle.allowed_head = event_hash
        reopened = SQLiteStateStore(
            self.database_path, self.oracle, "repo-1"
        )
        reopened._bind_classification_authority(self.authority)
        reopened.load_verified("repo-1", authority=self.authority)
        connection = sqlite3.connect(self.database_path)
        try:
            migrated = connection.execute(
                "SELECT containment_binding_version, containment_digest, "
                "containment_spec_json, containment_capability_json FROM "
                "validator_intents WHERE validator_intent_id = ?",
                (intent.validator_intent_id,),
            ).fetchone()
            version = connection.execute("PRAGMA user_version").fetchone()[0]
        finally:
            connection.close()
        self.assertEqual(version, 5)
        self.assertEqual(migrated, (None, None, None, None))
        legacy_commit = CommitReceipt(
            committed.command_id, committed.event_id, committed.sequence,
            event_hash, False,
        )
        with self.assertRaisesRegex(DispatchDenied, "legacy.*containment"):
            reopened._contact_committed_validator(
                intent,
                capability,
                legacy_commit,
                reopened._adapter_target_digest("repo-1", "VALIDATOR"),
                self.authority,
            )

    def test_f20_containment_history_requires_bound_authority_on_reopen(self) -> None:
        _intent, _capability, committed, _adapter, _request = (
            self._prepared_validator_execution()
        )
        self.oracle.allowed_head = committed.event_hash
        reopened = SQLiteStateStore(self.database_path, self.oracle, "repo-1")

        with self.assertRaisesRegex(
            StorageIntegrityError, "containment event evidence"
        ):
            reopened.load_verified("repo-1")
        reopened.load_verified("repo-1", authority=self.authority)

    def test_f20_self_consistent_containment_evidence_tamper_fails_closed(self) -> None:
        intent, _capability, _committed, _adapter, _request = (
            self._prepared_validator_execution()
        )

        def rewrite_copy(path: Path, mutation) -> str:
            shutil.copy2(self.database_path, path)
            connection = sqlite3.connect(path)
            try:
                body = json.loads(
                    connection.execute(
                        "SELECT body_json FROM events WHERE event_id = ?",
                        (intent.event_id,),
                    ).fetchone()[0]
                )
                mutation(body)
                event_hash = self.store._event_hash(body)
                body_json = json.dumps(
                    body, sort_keys=True, separators=(",", ":")
                )
                capability_json = json.dumps(
                    body["capability_evidence"],
                    sort_keys=True,
                    separators=(",", ":"),
                )
                connection.execute(
                    "UPDATE events SET event_hash = ?, body_json = ? "
                    "WHERE event_id = ?",
                    (event_hash, body_json, intent.event_id),
                )
                connection.execute(
                    "UPDATE validator_intents SET event_hash = ?, body_json = ?, "
                    "containment_capability_json = ? WHERE validator_intent_id = ?",
                    (
                        event_hash,
                        body_json,
                        capability_json,
                        intent.validator_intent_id,
                    ),
                )
                connection.execute(
                    "UPDATE command_outcomes SET event_hash = ? WHERE command_id = ?",
                    (event_hash, intent.command_id),
                )
                connection.execute(
                    "UPDATE runs SET head_hash = ? WHERE run_id = ?",
                    (event_hash, intent.run_id),
                )
                connection.execute(
                    "UPDATE repositories SET catalog_head = ? WHERE repository_id = ?",
                    (event_hash, intent.repository_id),
                )
                connection.commit()
                return event_hash
            finally:
                connection.close()

        mutations = {
            "issuer MAC": lambda body: body["capability_evidence"].__setitem__(
                "issuer_mac", "0" * 64
            ),
            "issuer fingerprint": lambda body: body.__setitem__(
                "capability_issuer_fingerprint", "0" * 64
            ),
            "surplus event field": lambda body: body.__setitem__(
                "untrusted_surplus", True
            ),
        }
        for suffix, mutation in mutations.items():
            with self.subTest(mutation=suffix):
                path = self.database_path.parent / (
                    suffix.replace(" ", "-") + ".sqlite3"
                )
                head = rewrite_copy(path, mutation)
                oracle = MutableFreshnessOracle()
                oracle.allowed_head = head
                reopened = SQLiteStateStore(path, oracle, "repo-1")
                with self.assertRaisesRegex(
                    StorageIntegrityError,
                    "containment event evidence|event schema",
                ):
                    reopened.load_verified("repo-1", authority=self.authority)

    def test_f20_validator_intent_schema_rejects_type_order_and_constraint_drift(self) -> None:
        self._prepared_validator_execution()
        mutations = {
            "type": lambda sql: sql.replace(
                "containment_digest TEXT", "containment_digest BLOB", 1
            ),
            "order": lambda sql: sql.replace(
                "containment_binding_version INTEGER, containment_digest TEXT",
                "containment_digest TEXT, containment_binding_version INTEGER",
                1,
            ),
            "constraint": lambda sql: sql.replace(
                " CHECK (status IN ('ACTIVE', 'SETTLED'))", "", 1
            ),
            "foreign-key-removed": lambda sql: sql.replace(
                " REFERENCES events(event_id)", "", 1
            ),
            "foreign-key-retargeted": lambda sql: sql.replace(
                "REFERENCES events(event_id)",
                "REFERENCES repositories(repository_id)",
                1,
            ),
            "surplus-constraint": lambda sql: sql.replace(
                "recovery_id TEXT,",
                "recovery_id TEXT CHECK (recovery_id <> ''),",
                1,
            ),
        }
        for suffix, mutation in mutations.items():
            with self.subTest(mutation=suffix):
                path = self.database_path.parent / f"schema-{suffix}.sqlite3"
                shutil.copy2(self.database_path, path)
                connection = sqlite3.connect(path)
                try:
                    original = connection.execute(
                        "SELECT sql FROM sqlite_master WHERE type = 'table' "
                        "AND name = 'validator_intents'"
                    ).fetchone()[0]
                    changed = mutation(original)
                    self.assertNotEqual(changed, original)
                    schema_version = connection.execute(
                        "PRAGMA schema_version"
                    ).fetchone()[0]
                    connection.execute("PRAGMA writable_schema = ON")
                    connection.execute(
                        "UPDATE sqlite_master SET sql = ? WHERE type = 'table' "
                        "AND name = 'validator_intents'",
                        (changed,),
                    )
                    connection.execute(
                        f"PRAGMA schema_version = {schema_version + 1}"
                    )
                    connection.execute("PRAGMA writable_schema = OFF")
                    connection.commit()
                finally:
                    connection.close()
                with self.assertRaisesRegex(
                    StorageIntegrityError, "schema is missing or incompatible"
                ):
                    SQLiteStateStore(path, self.oracle, "repo-1")

    def test_f20_validator_intent_schema_rejects_partial_index_drift(self) -> None:
        self._prepared_validator_execution()
        path = self.database_path.parent / "schema-index.sqlite3"
        shutil.copy2(self.database_path, path)
        connection = sqlite3.connect(path)
        try:
            schema_version = connection.execute(
                "PRAGMA schema_version"
            ).fetchone()[0]
            connection.execute("PRAGMA writable_schema = ON")
            connection.execute(
                "UPDATE sqlite_master SET sql = REPLACE(sql, "
                "'WHERE recovery_id IS NOT NULL', "
                "'WHERE recovery_id IS NULL') WHERE type = 'index' AND "
                "name = 'uq_validator_intents_recovery_id'"
            )
            connection.execute(
                f"PRAGMA schema_version = {schema_version + 1}"
            )
            connection.execute("PRAGMA writable_schema = OFF")
            connection.commit()
        finally:
            connection.close()
        with self.assertRaisesRegex(
            StorageIntegrityError,
            "schema is missing or incompatible|validation recovery schema",
        ):
            SQLiteStateStore(path, self.oracle, "repo-1")

    def test_t27_validator_contact_rejects_any_durable_request_change(self) -> None:
        observation = self._record_effect_observation(check_ids=("check-1",))
        request, capability = self._validator_intent(observation)
        committed = self.store.commit_validator_intent(
            request, capability, self.authority
        )
        self.oracle.allowed_head = committed.event_hash
        changed = replace(request, cap_units=request.cap_units + 1)
        with self.assertRaisesRegex(DispatchDenied, "changed the durable"):
            self.store._contact_committed_validator(
                changed,
                capability,
                committed,
                self.store._adapter_target_digest("repo-1", "VALIDATOR"),
                self.authority,
            )
        with self.assertRaisesRegex(DispatchDenied, "was not issued here"):
            self.store._contact_committed_validator(
                request,
                replace(capability, issuer_mac="forged-mac"),
                committed,
                self.store._adapter_target_digest("repo-1", "VALIDATOR"),
                self.authority,
            )
        replacement_authority = SyntheticAuthority(b"r" * 32)
        with self.assertRaisesRegex(DispatchDenied, "accepted plan"):
            self.store._contact_committed_validator(
                request,
                capability,
                committed,
                self.store._adapter_target_digest("repo-1", "VALIDATOR"),
                replacement_authority,
            )
        connection = sqlite3.connect(self.database_path)
        try:
            contact_count = connection.execute(
                "SELECT COUNT(*) FROM adapter_contacts"
            ).fetchone()[0]
        finally:
            connection.close()
        self.assertEqual(contact_count, 0)
        self.assertEqual(self.store.table_counts()["budget_reservations"], 2)
        self.assertEqual(self.store.table_counts()["effect_observations"], 1)
        self.assertEqual(self.store.table_counts()["outstanding_slot"], 1)
        self.store.load_verified("repo-1")

    def test_t27_validator_contact_denies_on_fence_alone(self) -> None:
        observation = self._record_effect_observation(check_ids=("check-1",))
        request, capability = self._validator_intent(observation)
        committed = self.store.commit_validator_intent(
            request, capability, self.authority
        )
        self.oracle.allowed_head = committed.event_hash
        connection = sqlite3.connect(self.database_path)
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

        with patch.object(self.store, "_verify_projections", return_value=None):
            with self.assertRaisesRegex(
                DispatchDenied, "active dispatch fence"
            ):
                self.store._contact_committed_validator(
                    request,
                    capability,
                    committed,
                    self.store._adapter_target_digest("repo-1", "VALIDATOR"),
                    self.authority,
                )

        connection = sqlite3.connect(self.database_path)
        try:
            contact_count = connection.execute(
                "SELECT COUNT(*) FROM adapter_contacts"
            ).fetchone()[0]
            reservation, fence = (
                connection.execute(
                    "SELECT disposition, settlement_head_hash FROM "
                    "budget_reservations WHERE reservation_id = ?",
                    (request.reservation_id,),
                ).fetchone(),
                connection.execute(
                    "SELECT fence_id, reason_code, originating_event_id FROM "
                    "dispatch_fences"
                ).fetchone(),
            )
        finally:
            connection.close()
        self.assertEqual(contact_count, 0)
        self.assertEqual(reservation, ("RESERVED", ""))
        self.assertEqual(fence, ("test-fence", "TEST_ONLY_FENCE", "test-origin"))

    def test_validator_contact_claim_prevents_non_dispatch_release(self) -> None:
        observation = self._record_effect_observation(check_ids=("check-1",))
        request, capability = self._validator_intent(observation)
        committed = self.store.commit_validator_intent(
            request, capability, self.authority
        )
        self.oracle.allowed_head = committed.event_hash
        self.store._contact_committed_validator(
            request,
            capability,
            committed,
            self.store._adapter_target_digest("repo-1", "VALIDATOR"),
            self.authority,
        )
        connection = sqlite3.connect(self.database_path)
        try:
            contact_hash, contact_body_json = connection.execute(
                "SELECT event_hash, body_json FROM adapter_contacts WHERE "
                "contact_kind = 'VALIDATOR'"
            ).fetchone()
            intent_body = json.loads(connection.execute(
                "SELECT body_json FROM validator_intents WHERE "
                "validator_intent_id = 'validator-intent-1'"
            ).fetchone()[0])
        finally:
            connection.close()
        recovery_intent_fields = {
            "validator_intent_binding_version",
            "parent_slot_generation",
            "parent_recovery_authorization_id",
        }
        recovery_contact_fields = {
            "contact_binding_version", "slot_generation",
            "recovery_authorization_id",
        }
        self.assertTrue(recovery_intent_fields.isdisjoint(intent_body))
        self.assertTrue(
            recovery_contact_fields.isdisjoint(json.loads(contact_body_json))
        )
        self.oracle.allowed_head = contact_hash
        release = BudgetSettlementRequest(
            "validator-release-1", "validator-reservation-1", "",
            BudgetDisposition.RELEASED, None, "non-dispatch-evidence",
            "NONDISPATCH_PROVEN", non_dispatch_proven=True,
            zero_liability_proven=True,
            attempt_id="validator-attempt-1",
        )
        connection = sqlite3.connect(self.database_path)
        try:
            before_denial = tuple(connection.iterdump())
        finally:
            connection.close()
        with self.assertRaisesRegex(
            DispatchDenied, "canonical nonexecution seal"
        ):
            self.store._settle_budget(
                release,
                self.authority.issue_settlement_proof(
                    "validator-release-proof-1", release
                ),
                self.authority,
            )
        connection = sqlite3.connect(self.database_path)
        try:
            after_denial = tuple(connection.iterdump())
        finally:
            connection.close()
        self.assertEqual(after_denial, before_denial)

    def test_state_owner_intents_enforce_accepted_plan_issuer_after_restart(self) -> None:
        plan = self.store.accept_plan(
            PlanAcceptanceRequest(
                "plan-1", "plan-command-1", "plan-event-1", "repo-1",
                "run-1", "item-1", "effect-1", "revision-1",
                "descriptor-digest", "scope-1", "budget-policy-digest",
                ("check-1",),
            ),
            expected_head="",
            writer_epoch=1,
        )
        self.oracle.allowed_head = plan.event_hash
        replacement = SyntheticAuthority(b"r" * 32)
        replacement_grant = SyntheticGrant(
            "replacement-grant", "repo-1", "effect-1", "attempt-1", "scope-1"
        )
        replacement.register(replacement_grant)
        replacement_capability = replacement.claim(
            *replacement_grant.__dict__.values()
        )
        reopened = SQLiteStateStore(self.database_path, self.oracle, "repo-1")
        connection = sqlite3.connect(self.database_path)
        try:
            before_denial = tuple(connection.iterdump())
        finally:
            connection.close()
        with self.assertRaisesRegex(DispatchDenied, "accepted plan"):
            reopened.commit_intent(
                self.request(), replacement_capability, replacement,
                expected_head=plan.event_hash, writer_epoch=2,
            )
        connection = sqlite3.connect(self.database_path)
        try:
            after_denial = tuple(connection.iterdump())
        finally:
            connection.close()
        self.assertEqual(after_denial, before_denial)

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
        second_store._bind_classification_authority(second_authority)
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
        settlement_request = BudgetSettlementRequest(
            "settlement-2",
            "reservation-1",
            previous_hash,
            BudgetDisposition.ADJUSTED,
            11,
            "receipt-adjustment-1",
            "AUTHORITATIVE_CORRECTION",
        )
        proof = self.authority.issue_settlement_proof(
            "proof-2", settlement_request
        )
        breached = self.store._settle_budget(
            settlement_request,
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
            settlement_request,
        )
        settlement = self.store._settle_budget(
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
            self.store._record_validator_observation(
                request,
                failure_hook=raise_at(
                    "after_validator_observation_writes_before_commit"
                ),
            )
        self.assertEqual(self.store.table_counts()["validator_observations"], 0)

        with self.assertRaises(InjectedFailure):
            self.store._record_validator_observation(
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
        replay = self.store._record_validator_observation(request)

        self.assertTrue(replay.replayed)
        self.assertEqual(result[1], 0)
        self.assertEqual(status, "ACTIVE")
        self.assertEqual(self.store.table_counts()["outstanding_slot"], 1)
        self.store.load_verified("repo-1")

    def test_operation_slot_release_denies_after_dispatch_with_active_validator(self) -> None:
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
        release_request = BudgetSettlementRequest(
            "release-settlement-1", "reservation-1", previous_hash,
            BudgetDisposition.RELEASED, None, "receipt-1",
            "ALL_OPERATION_OBLIGATIONS_CLAIMED_SETTLED",
            non_dispatch_proven=True, zero_liability_proven=True,
            release_slot=True, all_obligations_settled=True,
        )
        proof = self.authority.issue_settlement_proof(
            "release-proof-1", release_request
        )

        with self.assertRaisesRegex(DispatchDenied, "illegal budget settlement"):
            self.store._settle_budget(
                release_request,
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
        settlement_request = BudgetSettlementRequest(
            "validator-settlement-1", "validator-reservation-1", "",
            BudgetDisposition.UNKNOWN_WORST_CASE_CHARGED, None,
            "validator-result-unknown-1", "VALIDATOR_USAGE_UNKNOWN",
        )
        proof = self.authority.issue_settlement_proof(
            "validator-proof-1", settlement_request
        )
        settlement = self.store._settle_budget(
            settlement_request,
            proof,
            self.authority,
        )
        self.oracle.allowed_head = settlement.settlement_hash

        recorded = self.store._record_validator_observation(
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

    def test_consumed_settlement_cannot_release_slot_before_finalization(self) -> None:
        committed = self._commit_planned_intent(
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
            request,
        )
        with self.assertRaisesRegex(DispatchDenied, "T16 finalization"):
            self.store._settle_budget(request, proof, self.authority)
        self.assertEqual(self.store.table_counts()["budget_settlements"], 0)
        self.assertEqual(self.store.table_counts()["outstanding_slot"], 1)

    def test_budget_breach_records_fence_and_retains_operation_slot(self) -> None:
        committed = self._commit_planned_intent(
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
        )
        proof = self.authority.issue_settlement_proof(
            "proof-1",
            settlement,
        )
        settlement_receipt = self.store._settle_budget(
            settlement, proof, self.authority
        )
        self.oracle.allowed_head = settlement_receipt.settlement_hash
        second_authority = self.authority
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
        self.assertEqual(self.store.table_counts()["dispatch_fences"], 1)
        with self.assertRaisesRegex(DispatchDenied, "repository slot"):
            self._commit_planned_intent(
                second_request,
                second_capability,
                second_authority,
                expected_head=settlement_receipt.settlement_hash,
                writer_epoch=4,
            )

    def test_freshness_rejects_snapshot_missing_complete_settlement_tail(self) -> None:
        committed = self._commit_planned_intent(
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
            settlement,
        )
        settlement_receipt = self.store._settle_budget(
            settlement, proof, self.authority
        )
        self.oracle.allowed_head = settlement_receipt.settlement_hash
        stale_store = SQLiteStateStore(snapshot_path, self.oracle, "repo-1")
        with self.assertRaisesRegex(DispatchDenied, "freshness"):
            stale_store.load_verified("repo-1")

    def test_late_accounting_after_release_adds_fence_without_replacing_slot(self) -> None:
        committed = self._commit_planned_intent(
            self.request(), self.capability, self.authority, expected_head="", writer_epoch=1
        )
        self.oracle.allowed_head = committed.event_hash
        first = BudgetSettlementRequest(
            "settlement-1",
            "reservation-1",
            "",
            BudgetDisposition.RELEASED,
            None,
            "initial-usage",
            "NONDISPATCH_PROVEN",
            non_dispatch_proven=True,
            zero_liability_proven=True,
            release_slot=True,
            all_obligations_settled=True,
        )
        first_proof = self.authority.issue_settlement_proof(
            "proof-1",
            first,
        )
        first_receipt = self.store._settle_budget(first, first_proof, self.authority)
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
            late,
        )
        late_receipt = self.store._settle_budget(late, late_proof, self.authority)
        self.oracle.allowed_head = late_receipt.settlement_hash

        self.assertEqual(self.store.table_counts()["outstanding_slot"], 0)
        self.assertEqual(self.store.table_counts()["dispatch_fences"], 1)
        self.store.load_verified("repo-1")

    def test_f13_every_state_routes_contrary_receipts_before_ordinary_intake(self) -> None:
        terminals = {
            LifecycleState.COMPLETED,
            LifecycleState.FAILED_FINAL,
            LifecycleState.STOPPED,
        }
        for state in LifecycleState:
            for classification, usage, accounting_unknown in (
                (SourceControlClassification.KNOWN, 2, False),
                (SourceControlClassification.UNKNOWN, 2, False),
                (SourceControlClassification.KNOWN, None, True),
            ):
                with self.subTest(
                    state=state.value,
                    classification=classification.value,
                    usage=usage,
                ):
                    transition, event_kind, resulting_state = (
                        storage_module._derive_effect_observation_route(
                            state,
                            usage,
                            classification.value,
                            accounting_unknown=accounting_unknown,
                            force_late=True,
                        )
                    )
                    self.assertEqual(transition, "T23")
                    self.assertEqual(event_kind, "LATE_RECEIPT_RECORDED")
                    self.assertEqual(
                        resulting_state,
                        state
                        if state in terminals
                        else LifecycleState.RECONCILIATION_REQUIRED,
                    )

    def test_f13_post_release_receipt_preserves_different_slot_owner(self) -> None:
        committed = self._commit_planned_intent(
            self.request(), self.capability, self.authority,
            expected_head="", writer_epoch=1,
        )
        self.oracle.allowed_head = committed.event_hash
        release = BudgetSettlementRequest(
            "release-1", "reservation-1", "", BudgetDisposition.RELEASED,
            None, "nondispatch-proof-1", "NONDISPATCH_PROVEN",
            non_dispatch_proven=True,
            zero_liability_proven=True,
            release_slot=True,
            all_obligations_settled=True,
        )
        released = self.store._settle_budget(
            release,
            self.authority.issue_settlement_proof("release-proof-1", release),
            self.authority,
        )
        self.oracle.allowed_head = released.settlement_hash
        second_grant = SyntheticGrant(
            "grant-2", "repo-1", "effect-2", "attempt-2", "scope-2"
        )
        self.authority.register(second_grant)
        second_capability = self.authority.claim(*second_grant.__dict__.values())
        second_plan = self.store.accept_plan(
            PlanAcceptanceRequest(
                "plan-2", "plan-command-2", "plan-event-2", "repo-1",
                "run-2", "item-2", "effect-2", "revision-2",
                "descriptor-2", "scope-2", "budget-2", ("check-2",),
            ),
            expected_head=released.settlement_hash,
            writer_epoch=4,
        )
        self.oracle.allowed_head = second_plan.event_hash
        second_request = IntentRequest(
            "repo-1", "run-2", "item-2", "command-2", "event-2",
            "effect-2", "descriptor-2", "attempt-2", "permission-2",
            "reservation-2", "budget-2", 1, 2, 10,
        )
        second = self.store.commit_intent(
            second_request,
            second_capability,
            self.authority,
            expected_head=second_plan.event_hash,
            writer_epoch=5,
        )
        self.oracle.allowed_head = second.event_hash
        branch_source = self.database_path.parent / "f13-branch-source.sqlite3"
        shutil.copy2(self.database_path, branch_source)

        for label, classification, usage, expected_disposition in (
            (
                "known",
                SourceControlClassification.KNOWN,
                3,
                BudgetDisposition.ADJUSTED.value,
            ),
            (
                "unknown",
                SourceControlClassification.UNKNOWN,
                None,
                BudgetDisposition.UNKNOWN_WORST_CASE_CHARGED.value,
            ),
        ):
            with self.subTest(receipt=label):
                branch_path = self.database_path.parent / f"f13-{label}.sqlite3"
                shutil.copy2(branch_source, branch_path)
                oracle = MutableFreshnessOracle()
                oracle.allowed_head = second.event_hash
                branch = SQLiteStateStore(branch_path, oracle, "repo-1")
                branch._bind_classification_authority(self.authority)
                base = EffectObservationRequest(
                    f"late-{label}-observation",
                    f"late-{label}-command",
                    f"late-{label}-event",
                    "repo-1", "run-1", "item-1", "effect-1", "attempt-1",
                    f"late-{label}-receipt", self.capability.claim_id,
                    "descriptor-digest", usage, f"late-{label}-settlement", "",
                )
                if label == "known":
                    connection = sqlite3.connect(branch_path)
                    try:
                        before = tuple(connection.iterdump())
                    finally:
                        connection.close()
                    with self.assertRaisesRegex(DispatchDenied, "durable intent"):
                        self._record_signed_effect_observation(
                            replace(
                                base,
                                observation_id="foreign-observation",
                                command_id="foreign-command",
                                event_id="foreign-event",
                                source_receipt_id="foreign-receipt",
                                source_claim_id="foreign-claim",
                                settlement_event_id="foreign-settlement",
                            ),
                            store=branch,
                        )
                    connection = sqlite3.connect(branch_path)
                    try:
                        after = tuple(connection.iterdump())
                    finally:
                        connection.close()
                    self.assertEqual(after, before)
                recorded = self._record_signed_effect_observation(
                    base,
                    classification=classification,
                    store=branch,
                )
                oracle.allowed_head = recorded.event_hash
                connection = sqlite3.connect(branch_path)
                try:
                    slot = connection.execute(
                        "SELECT run_id, logical_effect_id, attempt_id FROM "
                        "outstanding_slot WHERE repository_id = 'repo-1'"
                    ).fetchone()
                    event_kind = connection.execute(
                        "SELECT event_kind FROM events WHERE event_id = ?",
                        (recorded.event_id,),
                    ).fetchone()[0]
                    disposition = connection.execute(
                        "SELECT disposition FROM budget_reservations WHERE "
                        "reservation_id = 'reservation-1'"
                    ).fetchone()[0]
                finally:
                    connection.close()
                self.assertEqual(slot, ("run-2", "effect-2", "attempt-2"))
                self.assertEqual(event_kind, "LATE_RECEIPT_RECORDED")
                self.assertEqual(
                    recorded.resulting_state,
                    LifecycleState.RECONCILIATION_REQUIRED,
                )
                self.assertEqual(disposition, expected_disposition)
                branch.load_verified("repo-1", authority=self.authority)

    def test_release_cannot_repeat_after_late_unknown_accounting(self) -> None:
        committed = self._commit_planned_intent(
            self.request(), self.capability, self.authority,
            expected_head="", writer_epoch=1,
        )
        self.oracle.allowed_head = committed.event_hash
        released = BudgetSettlementRequest(
            "settlement-1", "reservation-1", "", BudgetDisposition.RELEASED,
            None, "nondispatch-1", "NONDISPATCH_PROVEN",
            non_dispatch_proven=True, zero_liability_proven=True,
        )
        first = self.store._settle_budget(
            released,
            self.authority.issue_settlement_proof("proof-1", released),
            self.authority,
        )
        self.oracle.allowed_head = first.settlement_hash
        unknown = BudgetSettlementRequest(
            "settlement-2", "reservation-1", first.settlement_hash,
            BudgetDisposition.UNKNOWN_WORST_CASE_CHARGED, None,
            "late-unknown-1", "LATE_LIABILITY_UNKNOWN",
        )
        second = self.store._settle_budget(
            unknown,
            self.authority.issue_settlement_proof("proof-2", unknown),
            self.authority,
        )
        self.oracle.allowed_head = second.settlement_hash
        repeated = BudgetSettlementRequest(
            "settlement-3", "reservation-1", second.settlement_hash,
            BudgetDisposition.RELEASED, None, "nondispatch-2",
            "NONDISPATCH_REASSERTED", non_dispatch_proven=True,
            zero_liability_proven=True,
        )
        connection = sqlite3.connect(self.database_path)
        try:
            before_denial = tuple(connection.iterdump())
        finally:
            connection.close()

        with self.assertRaisesRegex(DispatchDenied, "already released"):
            self.store._settle_budget(
                repeated,
                self.authority.issue_settlement_proof("proof-3", repeated),
                self.authority,
            )
        connection = sqlite3.connect(self.database_path)
        try:
            after_denial = tuple(connection.iterdump())
        finally:
            connection.close()
        self.assertEqual(after_denial, before_denial)

    def _t22_report(
        self,
        expected_state: LifecycleState,
        *,
        database_path: Path | None = None,
        oracle=None,
        **request_changes,
    ):
        database_path = database_path or self.database_path
        catalog_head, run_heads = self.store.load_verified(
            "repo-1", authority=self.authority
        )
        reader = SQLiteStateReader(
            database_path,
            oracle or CompleteFreshnessOracle(catalog_head, run_heads),
            "repo-1",
            self.authority,
        )
        request = TerminalRestartRequest(
            "terminal-restart-1", "repo-1", "run-1", expected_state,
            **request_changes,
        )
        return SyntheticReadCoordinator(
            reader, TransitionEngine()
        ).report_terminal_restart(request)

    def test_t22_stopped_report_is_verified_and_strictly_read_only(self) -> None:
        plan = self.store.accept_plan(
            PlanAcceptanceRequest(
                "plan-1", "plan-command-1", "plan-event-1", "repo-1",
                "run-1", "item-1", "effect-1", "revision-1",
                "descriptor-digest", "scope-1", "budget-policy-digest",
                ("check-1",),
            ),
            expected_head="", writer_epoch=1,
        )
        self.oracle.allowed_head = plan.event_hash
        stopped = self.store.stop(
            self._stop_request(),
            self._stop_capability(StopMode.IMMEDIATE),
            self.authority,
        )
        self.oracle.allowed_head = stopped.event_hash
        read_root = Path(self.temporary_directory.name) / "read-only-copy"
        read_root.mkdir()
        read_database = read_root / "state.sqlite3"
        shutil.copy2(self.database_path, read_database)
        before = {
            path.name: path.read_bytes()
            for path in read_root.iterdir()
            if path.is_file()
        }

        report = self._t22_report(
            LifecycleState.STOPPED,
            database_path=read_database,
            expected_terminal_event_id=stopped.event_id,
            expected_terminal_event_hash=stopped.event_hash,
            expected_catalog_head=stopped.event_hash,
            expected_run_head=stopped.event_hash,
            expected_run_heads_digest=self.store._run_heads_digest(
                {"run-1": stopped.event_hash}
            ),
        )

        after = {
            path.name: path.read_bytes()
            for path in read_root.iterdir()
            if path.is_file()
        }
        self.assertEqual(report.verification, TerminalRestartVerification.VERIFIED_CURRENT)
        self.assertEqual(
            report.disposition,
            TerminalRestartDisposition.TERMINAL_RESTART_DENIED,
        )
        self.assertEqual(report.observed_state, LifecycleState.STOPPED)
        self.assertFalse(report.restart_advancement_authorized)
        self.assertEqual(report.dispatch_posture, DispatchPosture.CLOSED)
        self.assertFalse(report.reconciliation_authorized)
        self.assertEqual(report.terminal_event_id, stopped.event_id)
        self.assertEqual(before, after)
        self.assertNotIn("writer.lock", after)
        reader = SQLiteStateReader(
            read_database,
            CompleteFreshnessOracle(stopped.event_hash, {"run-1": stopped.event_hash}),
            "repo-1", self.authority,
        )
        self.assertFalse(hasattr(reader, "table_counts"))
        self.assertFalse(hasattr(reader, "accept_plan"))

    def test_t22_denies_restart_for_completed_and_failed_final(self) -> None:
        request, attestation = self._prepare_finalization()
        completed = self.store._finalize_operation(
            request, attestation, self.authority
        )
        self.oracle.allowed_head = completed.event_hash

        report = self._t22_report(LifecycleState.COMPLETED)

        self.assertEqual(report.observed_state, LifecycleState.COMPLETED)
        self.assertEqual(
            report.disposition,
            TerminalRestartDisposition.TERMINAL_RESTART_DENIED,
        )
        self.assertEqual(report.terminal_event_id, completed.event_id)

        failed_root = Path(self.temporary_directory.name) / "failed-terminal"
        failed_root.mkdir()
        failed_path = failed_root / "state.sqlite3"
        failed_oracle = MutableFreshnessOracle()
        failed_store = SQLiteStateStore(failed_path, failed_oracle, "repo-1")
        failed_authority = SyntheticAuthority()
        failed_authority.register(
            SyntheticGrant(
                "grant-1", "repo-1", "effect-1", "attempt-1", "scope-1"
            )
        )
        failed_capability = failed_authority.claim(
            "grant-1", "repo-1", "effect-1", "attempt-1", "scope-1"
        )
        failed_store._bind_classification_authority(failed_authority)
        original_store, original_path, original_oracle, original_authority, original_capability = (
            self.store, self.database_path, self.oracle, self.authority,
            self.capability,
        )
        self.store, self.database_path, self.oracle, self.authority, self.capability = (
            failed_store, failed_path, failed_oracle, failed_authority,
            failed_capability,
        )
        try:
            observation = self._record_validator_result(
                verdict="FAIL", only_check=True
            )
            failed = self.store._apply_validator_observation(
                ValidationApplicationRequest(
                    "application-1", "apply-command-1", "apply-event-1",
                    "repo-1", "run-1", "item-1", "effect-1",
                    "revision-1", "check-1", "validator-attempt-1",
                    "validator-observation-1",
                ),
                classification=self._classification(observation, "FINAL"),
            )
            self.oracle.allowed_head = failed.event_hash

            failed_report = self._t22_report(LifecycleState.FAILED_FINAL)
        finally:
            self.store, self.database_path, self.oracle, self.authority, self.capability = (
                original_store, original_path, original_oracle,
                original_authority, original_capability,
            )

        self.assertEqual(
            failed_report.observed_state, LifecycleState.FAILED_FINAL
        )
        self.assertEqual(
            failed_report.disposition,
            TerminalRestartDisposition.TERMINAL_RESTART_DENIED,
        )
        self.assertEqual(failed_report.terminal_event_id, failed.event_id)

    def test_t22_reports_nonterminal_without_evaluating_dispatch(self) -> None:
        plan = self.store.accept_plan(
            PlanAcceptanceRequest(
                "plan-1", "plan-command-1", "plan-event-1", "repo-1",
                "run-1", "item-1", "effect-1", "revision-1",
                "descriptor-digest", "scope-1", "budget-policy-digest",
                ("check-1",),
            ),
            expected_head="", writer_epoch=1,
        )
        self.oracle.allowed_head = plan.event_hash

        report = self._t22_report(LifecycleState.STOPPED)

        self.assertEqual(report.verification, TerminalRestartVerification.VERIFIED_CURRENT)
        self.assertEqual(report.disposition, TerminalRestartDisposition.NONTERMINAL)
        self.assertEqual(report.observed_state, LifecycleState.PLANNED)
        self.assertEqual(report.dispatch_posture, DispatchPosture.NOT_EVALUATED)
        self.assertFalse(report.restart_advancement_authorized)

    def test_t22_separates_freshness_and_caller_anchor_mismatches(self) -> None:
        plan = self.store.accept_plan(
            PlanAcceptanceRequest(
                "plan-1", "plan-command-1", "plan-event-1", "repo-1",
                "run-1", "item-1", "effect-1", "revision-1",
                "descriptor-digest", "scope-1", "budget-policy-digest",
                ("check-1",),
            ),
            expected_head="", writer_epoch=1,
        )
        self.oracle.allowed_head = plan.event_hash
        stopped = self.store.stop(
            self._stop_request(), self._stop_capability(StopMode.IMMEDIATE),
            self.authority,
        )
        self.oracle.allowed_head = stopped.event_hash

        stale = self._t22_report(
            LifecycleState.STOPPED,
            oracle=CompleteFreshnessOracle("stale", {}),
        )
        wrong_state = self._t22_report(LifecycleState.COMPLETED)
        wrong_anchor = self._t22_report(
            LifecycleState.STOPPED,
            expected_terminal_event_id="wrong-event",
            expected_terminal_event_hash="wrong-hash",
        )

        self.assertEqual(
            stale.verification,
            TerminalRestartVerification.LOCAL_FRESHNESS_UNVERIFIED,
        )
        self.assertEqual(stale.observed_state, LifecycleState.STOPPED)
        self.assertTrue(stale.observed_state_trusted)
        self.assertEqual(stale.dispatch_posture, DispatchPosture.CLOSED)
        self.assertEqual(
            wrong_state.verification,
            TerminalRestartVerification.VERIFIED_CURRENT,
        )
        self.assertEqual(
            wrong_state.disposition,
            TerminalRestartDisposition.EXPECTED_STATE_MISMATCH,
        )
        self.assertEqual(
            wrong_anchor.disposition,
            TerminalRestartDisposition.ANCHOR_MISMATCH,
        )

    def test_t22_corrupt_or_unsupported_state_is_unverified_without_repair(self) -> None:
        plan = self.store.accept_plan(
            PlanAcceptanceRequest(
                "plan-1", "plan-command-1", "plan-event-1", "repo-1",
                "run-1", "item-1", "effect-1", "revision-1",
                "descriptor-digest", "scope-1", "budget-policy-digest",
                ("check-1",),
            ),
            expected_head="", writer_epoch=1,
        )
        self.oracle.allowed_head = plan.event_hash
        stopped = self.store.stop(
            self._stop_request(), self._stop_capability(StopMode.IMMEDIATE),
            self.authority,
        )
        self.oracle.allowed_head = stopped.event_hash
        for name, mutation in (
            (
                "corrupt",
                "UPDATE runs SET lifecycle_state = 'COMPLETED' "
                "WHERE run_id = 'run-1'",
            ),
            ("legacy", "PRAGMA user_version = 2"),
        ):
            with self.subTest(name=name):
                case_root = Path(self.temporary_directory.name) / name
                case_root.mkdir()
                case_path = case_root / "state.sqlite3"
                shutil.copy2(self.database_path, case_path)
                connection = sqlite3.connect(case_path)
                try:
                    connection.execute(mutation)
                    connection.commit()
                finally:
                    connection.close()
                before = case_path.read_bytes()

                report = self._t22_report(
                    LifecycleState.STOPPED, database_path=case_path
                )

                self.assertEqual(
                    report.verification,
                    TerminalRestartVerification.UNVERIFIED_INTEGRITY_OR_SCHEMA,
                )
                self.assertEqual(
                    report.disposition, TerminalRestartDisposition.UNVERIFIED
                )
                self.assertFalse(report.observed_state_trusted)
                self.assertIsNone(report.terminal_event_id)
                self.assertEqual(case_path.read_bytes(), before)
                self.assertFalse((case_root / "writer.lock").exists())

    def test_t22_non_object_event_body_returns_typed_unverified_report(self) -> None:
        plan = self.store.accept_plan(
            PlanAcceptanceRequest(
                "plan-1", "plan-command-1", "plan-event-1", "repo-1",
                "run-1", "item-1", "effect-1", "revision-1",
                "descriptor-digest", "scope-1", "budget-policy-digest",
                ("check-1",),
            ),
            expected_head="", writer_epoch=1,
        )
        self.oracle.allowed_head = plan.event_hash
        stopped = self.store.stop(
            self._stop_request(), self._stop_capability(StopMode.IMMEDIATE),
            self.authority,
        )
        self.oracle.allowed_head = stopped.event_hash
        case_root = Path(self.temporary_directory.name) / "non-object"
        case_root.mkdir()
        case_path = case_root / "state.sqlite3"
        shutil.copy2(self.database_path, case_path)
        malformed_hash = self.store._event_hash([])
        connection = sqlite3.connect(case_path)
        try:
            connection.execute(
                "UPDATE events SET body_json = '[]', event_hash = ? "
                "WHERE event_id = ?",
                (malformed_hash, stopped.event_id),
            )
            connection.execute(
                "UPDATE runs SET head_hash = ? WHERE run_id = 'run-1'",
                (malformed_hash,),
            )
            connection.execute(
                "UPDATE repositories SET catalog_head = ? WHERE "
                "repository_id = 'repo-1'",
                (malformed_hash,),
            )
            connection.commit()
        finally:
            connection.close()
        before = case_path.read_bytes()

        report = self._t22_report(
            LifecycleState.STOPPED, database_path=case_path
        )

        self.assertEqual(
            report.verification,
            TerminalRestartVerification.UNVERIFIED_INTEGRITY_OR_SCHEMA,
        )
        self.assertEqual(report.dispatch_posture, DispatchPosture.CLOSED)
        self.assertFalse(report.observed_state_trusted)
        self.assertEqual(case_path.read_bytes(), before)
        self.assertFalse((case_root / "writer.lock").exists())

    def test_t22_proven_nonexecution_verifies_auxiliary_ledger_read_only(self) -> None:
        self._prepare_t07_activity_settlement()
        stopped = self.store.stop(
            self._stop_request(), self._stop_capability(StopMode.IMMEDIATE),
            self.authority,
        )
        self.oracle.allowed_head = stopped.event_hash
        tracked_paths = tuple(
            path
            for path in self.database_path.parent.iterdir()
            if path.name.startswith("state.sqlite3")
            or path.name.startswith("synthetic-target.sqlite3")
        )
        before = {path.name: path.read_bytes() for path in tracked_paths}

        report = self._t22_report(LifecycleState.STOPPED)

        after_paths = tuple(
            path
            for path in self.database_path.parent.iterdir()
            if path.name.startswith("state.sqlite3")
            or path.name.startswith("synthetic-target.sqlite3")
        )
        after = {path.name: path.read_bytes() for path in after_paths}
        self.assertEqual(
            report.disposition,
            TerminalRestartDisposition.TERMINAL_RESTART_DENIED,
        )
        self.assertEqual(after, before)

    def test_t22_missing_database_and_wrong_authority_fail_closed_without_creation(self) -> None:
        missing_root = Path(self.temporary_directory.name) / "missing"
        missing_path = missing_root / "state.sqlite3"
        missing_reader = SQLiteStateReader(
            missing_path, CompleteFreshnessOracle("", {}), "repo-1",
            self.authority,
        )
        missing_report = SyntheticReadCoordinator(
            missing_reader, TransitionEngine()
        ).report_terminal_restart(
            TerminalRestartRequest(
                "missing-request", "repo-1", "run-1",
                LifecycleState.STOPPED,
            )
        )
        self.assertEqual(
            missing_report.verification,
            TerminalRestartVerification.UNVERIFIED_INTEGRITY_OR_SCHEMA,
        )
        self.assertFalse(missing_root.exists())

        plan = self.store.accept_plan(
            PlanAcceptanceRequest(
                "plan-1", "plan-command-1", "plan-event-1", "repo-1",
                "run-1", "item-1", "effect-1", "revision-1",
                "descriptor-digest", "scope-1", "budget-policy-digest",
                ("check-1",),
            ),
            expected_head="", writer_epoch=1,
        )
        self.oracle.allowed_head = plan.event_hash
        stopped = self.store.stop(
            self._stop_request(), self._stop_capability(StopMode.IMMEDIATE),
            self.authority,
        )
        self.oracle.allowed_head = stopped.event_hash
        _, run_heads = self.store.load_verified(
            "repo-1", authority=self.authority
        )
        wrong_reader = SQLiteStateReader(
            self.database_path,
            CompleteFreshnessOracle(stopped.event_hash, run_heads),
            "repo-1", SyntheticAuthority(b"z" * 32),
        )
        wrong_report = SyntheticReadCoordinator(
            wrong_reader, TransitionEngine()
        ).report_terminal_restart(
            TerminalRestartRequest(
                "wrong-authority", "repo-1", "run-1",
                LifecycleState.STOPPED,
            )
        )
        self.assertEqual(
            wrong_report.verification,
            TerminalRestartVerification.UNVERIFIED_INTEGRITY_OR_SCHEMA,
        )
        self.assertFalse(wrong_report.reconciliation_authorized)

    def test_t22_repeated_restart_read_cannot_reset_budget_or_release_slot(self) -> None:
        committed = self._commit_planned_intent(
            self.request(), self.capability, self.authority,
            expected_head="", writer_epoch=1,
        )
        self.oracle.allowed_head = committed.event_hash
        stopped = self.store.stop(
            self._stop_request(), self._stop_capability(StopMode.IMMEDIATE),
            self.authority,
        )
        self.oracle.allowed_head = stopped.event_hash
        connection = sqlite3.connect(self.database_path)
        try:
            before = tuple(connection.iterdump())
        finally:
            connection.close()

        first = self._t22_report(LifecycleState.STOPPED)
        second = self._t22_report(LifecycleState.STOPPED)

        connection = sqlite3.connect(self.database_path)
        try:
            after = tuple(connection.iterdump())
            reservation = connection.execute(
                "SELECT disposition, held_units, charged_units FROM "
                "budget_reservations WHERE reservation_id = 'reservation-1'"
            ).fetchone()
            slot = connection.execute(
                "SELECT run_id, attempt_id, generation FROM outstanding_slot"
            ).fetchone()
        finally:
            connection.close()
        self.assertEqual(first, second)
        self.assertEqual(first.terminal_event_id, stopped.event_id)
        self.assertEqual(after, before)
        self.assertEqual(reservation, (BudgetDisposition.RESERVED.value, 3, 0))
        self.assertEqual(slot, ("run-1", "attempt-1", 1))

    def test_t22_freshness_oracle_failure_returns_local_non_authorizing_report(self) -> None:
        plan = self.store.accept_plan(
            PlanAcceptanceRequest(
                "plan-1", "plan-command-1", "plan-event-1", "repo-1",
                "run-1", "item-1", "effect-1", "revision-1",
                "descriptor-digest", "scope-1", "budget-policy-digest",
                ("check-1",),
            ),
            expected_head="", writer_epoch=1,
        )
        self.oracle.allowed_head = plan.event_hash
        stopped = self.store.stop(
            self._stop_request(), self._stop_capability(StopMode.IMMEDIATE),
            self.authority,
        )
        self.oracle.allowed_head = stopped.event_hash

        class RaisingFreshnessOracle:
            def verify(self, repository_id, catalog_head, run_heads):
                raise RuntimeError("synthetic oracle unavailable")

        report = self._t22_report(
            LifecycleState.STOPPED, oracle=RaisingFreshnessOracle()
        )

        self.assertEqual(
            report.verification,
            TerminalRestartVerification.LOCAL_FRESHNESS_UNVERIFIED,
        )
        self.assertEqual(report.observed_state, LifecycleState.STOPPED)
        self.assertEqual(report.dispatch_posture, DispatchPosture.CLOSED)
        self.assertFalse(report.restart_advancement_authorized)

    def test_t22_read_transaction_observes_one_snapshot_during_writer_commit(self) -> None:
        plan = self.store.accept_plan(
            PlanAcceptanceRequest(
                "plan-1", "plan-command-1", "plan-event-1", "repo-1",
                "run-1", "item-1", "effect-1", "revision-1",
                "descriptor-digest", "scope-1", "budget-policy-digest",
                ("check-1",),
            ),
            expected_head="", writer_epoch=1,
        )
        self.oracle.allowed_head = plan.event_hash
        _, run_heads = self.store.load_verified(
            "repo-1", authority=self.authority
        )
        reader = SQLiteStateReader(
            self.database_path,
            CompleteFreshnessOracle(plan.event_hash, run_heads),
            "repo-1", self.authority,
        )
        original_verify = reader._verifier._verify_projections
        start_writer = threading.Event()
        writes_staged = threading.Event()

        def stop_writer():
            start_writer.wait(timeout=5)

            def observe_stage(stage):
                if stage == "after_stop_writes_before_commit":
                    writes_staged.set()

            return self.store.stop(
                self._stop_request(),
                self._stop_capability(StopMode.IMMEDIATE),
                self.authority,
                failure_hook=observe_stage,
            )

        def verify_during_write(connection, repository_id):
            start_writer.set()
            if not writes_staged.wait(timeout=5):
                raise TimeoutError("writer did not stage the terminal transition")
            return original_verify(connection, repository_id)

        reader._verifier._verify_projections = verify_during_write
        with ThreadPoolExecutor(max_workers=1) as executor:
            writer = executor.submit(stop_writer)
            report = SyntheticReadCoordinator(
                reader, TransitionEngine()
            ).report_terminal_restart(
                TerminalRestartRequest(
                    "terminal-race-1", "repo-1", "run-1",
                    LifecycleState.STOPPED,
                )
            )
            stopped = writer.result(timeout=5)
        self.oracle.allowed_head = stopped.event_hash

        self.assertEqual(
            report.verification, TerminalRestartVerification.VERIFIED_CURRENT
        )
        self.assertEqual(report.disposition, TerminalRestartDisposition.NONTERMINAL)
        self.assertEqual(report.observed_state, LifecycleState.PLANNED)
        self.assertEqual(
            self.store.load_run_lifecycle("run-1"), LifecycleState.STOPPED
        )


if __name__ == "__main__":
    unittest.main()
