from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor
from contextlib import closing
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
from unittest.mock import MagicMock, patch

from tools.aegis_delivery_control.adapters import (
    SyntheticEffectRequest,
    SyntheticExecutionAdapter,
    SyntheticValidatorAdapter,
    SyntheticValidatorRequest as SyntheticValidatorRequestContract,
    synthetic_validator_output_size,
    validate_synthetic_validator_containment,
)
from tools.aegis_delivery_control.authority import (
    SyntheticAuthority,
    SyntheticCapability,
    SyntheticGrant,
    SyntheticOperatorGrant,
    SyntheticValidatorGrant as SyntheticValidatorGrantContract,
)
from tools.aegis_delivery_control.contracts import (
    ApplicationReceipt,
    BudgetDisposition,
    BudgetSettlementRequest as BudgetSettlementContract,
    BindingMismatchKind,
    BindingMismatchRequest,
    CommitReceipt,
    DispatchDenied,
    EffectAdoptionReceipt,
    EffectObservationCommand,
    FinalizeOperationRequest,
    InjectedFailure,
    IntentRequest,
    LifecycleState,
    PauseExternalMutationRequest,
    PauseBeforeDispatchRequest,
    PauseLocalExecutionRequest,
    PauseReconciliationRequest,
    PauseValidationRequest,
    PlanAcceptanceRequest as PlanAcceptanceContract,
    ReconcileVerifiedReceiptRequest,
    ReconcileValidatorResultRequest,
    ReconciliationPauseResumeRequest,
    ResumeRequest,
    SourceControlClassification,
    SourceControlEvidenceRequest,
    SourceControlSettlementRequest,
    SourceControlUncertaintyBinding,
    StopMode,
    StopEscalationRequest,
    StopEscalationSettlement,
    StopRequest,
    StorageIntegrityError,
    ValidationApplicationRequest,
    ValidationLaunchRequest,
    ValidatorCessationRequest,
    ValidatorContainmentSpec,
    ValidatorIntentRequest as ValidatorIntentRequestContract,
    ValidatorObservationCommand,
    SYNTHETIC_VALIDATOR_SUPPORT_DIGEST,
    SYNTHETIC_VALIDATOR_SUPPORT_ID,
    validator_containment_digest,
    validator_containment_spec_json,
)
from tools.aegis_delivery_control.dispatch import (
    SyntheticDispatchCoordinator,
    SyntheticFinalizationCoordinator,
    SyntheticValidationCoordinator,
)
from tools.aegis_delivery_control.engine import TransitionEngine
from tools.aegis_delivery_control.storage import raise_at
from tools.aegis_delivery_control.tests._legacy_schema import (
    strip_t28_foundation_schema,
)

ProductionSyntheticValidationCoordinator = SyntheticValidationCoordinator


class SyntheticValidationCoordinator(ProductionSyntheticValidationCoordinator):
    """Legacy test facade that exercises the production prepared-launch path."""

    def launch(
        self, intent, capability, request, *, usage_units=0, lose_result=False
    ):
        intent.validate()
        request.validate()
        if usage_units is not None and (
            type(usage_units) is not int or usage_units < 0
        ):
            raise ValueError("usage_units must be non-negative or unknown")
        self._authority.verify_validator_issued(capability)
        self._adapter._validate_request_binding(capability, request, intent)
        validate_synthetic_validator_containment(capability, request, intent)
        with self._authority._lock:
            committed = capability.claim_id in self._authority._committed_claims
        if not committed:
            self._authority.release_uncommitted_validator_claim(capability)
        with closing(sqlite3.connect(self._store._database_path)) as connection:
            plan_id = connection.execute(
                "SELECT plan_id FROM validation_plans WHERE run_id = ?",
                (intent.run_id,),
            ).fetchone()[0]
        suffix = intent.command_id
        launch = self._store.prepare_validation_launch(
            ValidationLaunchRequest(
                f"test-launch-evaluation:{suffix}",
                f"test-launch-decision:{suffix}",
                f"test-launch-command:{suffix}",
                f"test-launch-event:{suffix}",
                f"test-launch-decision-event:{suffix}",
                intent.repository_id, intent.run_id, intent.item_id,
                intent.logical_effect_id, plan_id, intent.revision_digest,
                intent.check_id,
            ),
            self._authority,
        )
        if not launch.ready:
            raise DispatchDenied("test fixture validation launch is blocked")
        snapshot = self._store.load_validation_launch_snapshot(
            launch.snapshot_id, self._authority
        )
        return super().launch_prepared(
            intent, grant_id=capability.grant_id,
            scope_digest=capability.scope_digest,
            launch_snapshot=snapshot, request=request,
            usage_units=usage_units, lose_result=lose_result,
        )
from tools.aegis_delivery_control.tests._trusted_readiness_store import (
    SQLiteStateStore,
)


def BudgetSettlementRequest(*args, **kwargs):
    kwargs.setdefault("repository_id", "repo-1")
    kwargs.setdefault("run_id", "run-1")
    kwargs.setdefault("item_id", "item-1")
    kwargs.setdefault("logical_effect_id", "effect-1")
    kwargs.setdefault("attempt_id", "attempt-1")
    return BudgetSettlementContract(*args, **kwargs)


def PlanAcceptanceRequest(*args, **kwargs):
    """Build a newly accepted synthetic plan with explicit immutable pins."""
    check_ids = kwargs.get("check_ids", args[11] if len(args) > 11 else ())
    kwargs.setdefault(
        "check_dependency_ids",
        tuple((check_id, ()) for check_id in check_ids),
    )
    kwargs.setdefault(
        "check_launch_gate_ids",
        tuple((check_id, ()) for check_id in check_ids),
    )
    kwargs.setdefault("source_tree_digest", "source-tree-1")
    kwargs.setdefault("item_definition_digest", "item-definition-1")
    kwargs.setdefault("plan_schema_version", "plan-schema-1")
    kwargs.setdefault("reducer_version", "reducer-1")
    return PlanAcceptanceContract(*args, **kwargs)


def _validator_containment(input_digest: str, suffix: str):
    safe_suffix = suffix.replace(":", "-")
    spec = ValidatorContainmentSpec(
        1,
        SYNTHETIC_VALIDATOR_SUPPORT_ID,
        SYNTHETIC_VALIDATOR_SUPPORT_DIGEST,
        input_digest,
        f"inputs/{safe_suffix}",
        f"outputs/{safe_suffix}",
        f"scratch/{safe_suffix}",
        ("READ_PINNED_INPUT", "EMIT_BOUNDED_RESULT"),
        4096,
        "DENY",
        "DENY",
        "DENY",
    )
    return spec, validator_containment_spec_json(spec), validator_containment_digest(spec)


def SyntheticValidatorGrant(*args, **kwargs):
    input_digest = kwargs.get("input_digest", args[5])
    suffix = kwargs.get("validator_attempt_id", args[6])
    _, _, digest = _validator_containment(input_digest, suffix)
    kwargs.setdefault("containment_digest", digest)
    return SyntheticValidatorGrantContract(*args, **kwargs)


def ValidatorIntentRequest(*args, **kwargs):
    input_digest = kwargs.get("input_digest", args[12])
    suffix = kwargs.get("validator_attempt_id", args[13])
    _, spec_json, _ = _validator_containment(input_digest, suffix)
    kwargs.setdefault("containment_spec_json", spec_json)
    return ValidatorIntentRequestContract(*args, **kwargs)


def SyntheticValidatorRequest(*args, **kwargs):
    input_digest = kwargs.get("input_digest", args[4])
    suffix = kwargs.get("validator_attempt_id", args[5])
    spec, _, digest = _validator_containment(input_digest, suffix)
    kwargs.setdefault("containment_digest", digest)
    kwargs.setdefault("requested_actions", spec.allowed_actions)
    kwargs.setdefault("read_path", spec.input_root)
    kwargs.setdefault("output_path", f"{spec.output_root}/result.json")
    kwargs.setdefault("scratch_path", f"{spec.scratch_root}/work")
    result_digest = kwargs.get("result_digest", args[7])
    verdict = kwargs.get("verdict", args[8])
    kwargs.setdefault(
        "output_bytes", synthetic_validator_output_size(result_digest, verdict)
    )
    return SyntheticValidatorRequestContract(*args, **kwargs)


class AlwaysFreshOracle:
    def verify(self, repository_id, catalog_head, run_heads):
        return repository_id == "repo-1"


class NeverFreshOracle:
    def verify(self, repository_id, catalog_head, run_heads):
        return False


def _launch_validator_until_terminated(
    root,
    issuer_key,
    grant,
    intent,
    request,
    ready,
    errors,
):
    state_root = (
        patch(
            "tools.aegis_delivery_control.storage.known_local_state_base",
            return_value=Path(root),
        )
        if sys.platform == "win32"
        else patch.dict(os.environ, {"XDG_STATE_HOME": str(root)})
    )
    try:
        authority = SyntheticAuthority(issuer_key)
        authority.register_validator(grant)
        capability = authority.claim_validator(*grant.__dict__.values())
        with state_root:
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
    def test_t28_coordinator_mediates_adoption_without_adapter_contact(
        self,
    ) -> None:
        authority = SyntheticAuthority(b"t" * 32)
        store = MagicMock()
        store.is_canonical = True
        adapter = MagicMock()
        expected = EffectAdoptionReceipt(
            "adoption-1", "adoption-key-1", "command-1", "event-1",
            2, "event-hash-1", LifecycleState.VALIDATING,
            "adoption:adoption-key-1", 1, False,
        )

        def adopt(*args, **kwargs):
            kwargs["authorize_transition"](
                LifecycleState.PLANNED, LifecycleState.VALIDATING
            )
            return expected

        store.adopt_verified_effect.side_effect = adopt
        coordinator = SyntheticDispatchCoordinator(
            store, TransitionEngine(), authority, adapter
        )
        request = MagicMock()
        readiness = MagicMock()
        capability = MagicMock()

        actual = coordinator.adopt_verified_effect(
            request, readiness, capability
        )

        self.assertIs(actual, expected)
        store.adopt_verified_effect.assert_called_once()
        adapter.assert_not_called()

    def test_t17_ordered_source_control_settlement_evidence_is_exact(self) -> None:
        authority = SyntheticAuthority(b"s" * 32)
        binding = SourceControlUncertaintyBinding(
            "uncertainty-source-1", "pause-event-1", "pause-hash-1"
        )
        request = SourceControlSettlementRequest(
            repository_id="repo-1", run_id="run-1", item_id="item-1",
            logical_effect_id="effect-1", attempt_id="attempt-1",
            observation_id="observation-1",
            observation_event_hash="observation-hash-1",
            source_receipt_id="receipt-1", source_claim_id="claim-1",
            source_payload_digest="payload-1",
            expected_catalog_head="catalog-head-1",
            expected_run_head="run-head-1",
            authoritative_query_id="query-1",
            authoritative_queried_at_utc="2026-09-21T12:00:00+00:00",
            authoritative_query_after_event_id="pause-event-1",
            authoritative_query_after_event_hash="pause-hash-1",
            authoritative_source_id="synthetic-source-control:v1:claim-1",
            authoritative_response_id="receipt-1",
            authoritative_response_digest="response-digest-1",
            resulting_classification=SourceControlClassification.KNOWN,
            covered_source_bindings=(binding,),
        )
        evidence = authority.issue_source_control_settlement_evidence(
            "source-settlement-1", request
        )
        authority.verify_source_control_settlement_evidence(evidence, request)
        with self.assertRaisesRegex(DispatchDenied, "was not issued here"):
            authority.verify_source_control_settlement_evidence(
                evidence, replace(request, expected_run_head="newer-run-head")
            )

    def test_t17_retained_validator_result_contract_and_coordinator_route(
        self,
    ) -> None:
        request = ReconcileValidatorResultRequest(
            reconciliation_id="reconciliation-validator-result-1",
            command_id="reconciliation-validator-result-command-1",
            event_id="reconciliation-validator-result-event-1",
            repository_id="repo-1",
            run_id="run-1",
            item_id="item-1",
            logical_effect_id="effect-1",
            plan_id="plan-1",
            revision_digest="revision-1",
            observation_id="validator-observation-1",
            observation_event_hash="validator-observation-hash-1",
            cessation_id="validator-cessation-1",
            cessation_event_id="validator-cessation-event-1",
            cessation_event_hash="validator-cessation-hash-1",
            settlement_event_id="validator-settlement-1",
            settlement_hash="validator-settlement-hash-1",
            resolved_uncertainty_ids=("validator-billing-uncertainty-1",),
            expected_slot_attempt_id="attempt-1",
            expected_slot_generation=1,
            expected_run_head="run-head-1",
            expected_continuation_cursor="VALIDATING",
        )
        request.validate()
        self.assertTrue(
            hasattr(SyntheticValidationCoordinator, "reconcile_result")
        )

    def _prepare_t17_validator_reconciliation(
        self, root: Path, suffix: str
    ) -> tuple[
        SyntheticAuthority,
        SQLiteStateStore,
        SyntheticValidationCoordinator,
        ReconcileValidatorResultRequest,
        tuple[str, ...],
        tuple[str, ...],
    ]:
        (
            authority, store, _dispatch, validator_adapter,
            _validator_intent, _validator_capability, _committed,
        ) = self._prepare_t08_active_validator(
            root, contact=True, result=True, cessation=True,
            result_usage_units=None,
        )
        connection = sqlite3.connect(store._database_path)
        try:
            observation = connection.execute(
                "SELECT observation_id, event_hash FROM validator_observations "
                "WHERE observation_id = ?", ("validator-observation-t08",),
            ).fetchone()
            uncertainties = connection.execute(
                "SELECT uncertainty_id, fence_id FROM uncertainty_instances "
                "WHERE origin_event_id = ? ORDER BY uncertainty_kind",
                ("validator-observe-event-t08",),
            ).fetchall()
            cessation = connection.execute(
                "SELECT cessation_id, event_id, event_hash FROM "
                "validator_cessations WHERE validator_intent_id = ?",
                ("validator-intent-t08",),
            ).fetchone()
            unknown_head = connection.execute(
                "SELECT settlement_head_hash FROM budget_reservations WHERE "
                "reservation_id = ?", ("validator-reservation-t08",),
            ).fetchone()[0]
        finally:
            connection.close()
        adjusted_request = BudgetSettlementRequest(
            f"validator-adjusted-t17-{suffix}", "validator-reservation-t08",
            unknown_head, BudgetDisposition.ADJUSTED, 1,
            f"authoritative-validator-billing-t17-{suffix}",
            "USAGE_REPORTED", attempt_id="validator-attempt-1",
        )
        adjusted = store._settle_budget(
            adjusted_request,
            authority.issue_settlement_proof(
                f"validator-adjusted-proof-t17-{suffix}", adjusted_request
            ),
            authority,
        )
        validation = SyntheticValidationCoordinator(
            store, TransitionEngine(), authority, validator_adapter
        )
        request = ReconcileValidatorResultRequest(
            f"reconciliation-validator-result-t17-{suffix}",
            f"reconciliation-validator-result-command-t17-{suffix}",
            f"reconciliation-validator-result-event-t17-{suffix}",
            "repo-1", "run-1", "item-1", "effect-1", "plan:run-1",
            "revision-1", observation[0], observation[1],
            cessation[0], cessation[1], cessation[2],
            adjusted.settlement_event_id, adjusted.settlement_hash,
            tuple(row[0] for row in uncertainties), "attempt-1", 1,
            adjusted.settlement_hash, None,
        )
        return (
            authority, store, validation, request,
            tuple(row[0] for row in uncertainties),
            tuple(row[1] for row in uncertainties),
        )

    def test_t17_authoritative_validator_billing_restores_same_result(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (
                authority, store, _dispatch, validator_adapter,
                _validator_intent, _validator_capability, _committed,
            ) = self._prepare_t08_active_validator(
                root, contact=True, result=True, cessation=True,
                result_usage_units=None,
            )
            connection = sqlite3.connect(store._database_path)
            try:
                observation = connection.execute(
                    "SELECT observation_id, event_hash FROM "
                    "validator_observations WHERE observation_id = ?",
                    ("validator-observation-t08",),
                ).fetchone()
                uncertainties = connection.execute(
                    "SELECT uncertainty_id, fence_id FROM uncertainty_instances "
                    "WHERE origin_event_id = ? ORDER BY uncertainty_kind",
                    ("validator-observe-event-t08",),
                ).fetchall()
                cessation = connection.execute(
                    "SELECT cessation_id, event_id, event_hash FROM "
                    "validator_cessations WHERE validator_intent_id = ?",
                    ("validator-intent-t08",),
                ).fetchone()
                unknown_head = connection.execute(
                    "SELECT settlement_head_hash FROM budget_reservations WHERE "
                    "reservation_id = ?",
                    ("validator-reservation-t08",),
                ).fetchone()[0]
            finally:
                connection.close()
            self.assertIsNotNone(observation)
            self.assertEqual(len(uncertainties), 2)
            self.assertIsNotNone(cessation)
            adjusted_request = BudgetSettlementRequest(
                "validator-adjusted-t17", "validator-reservation-t08",
                unknown_head, BudgetDisposition.ADJUSTED, 1,
                "authoritative-validator-billing-t17", "USAGE_REPORTED",
                attempt_id="validator-attempt-1",
            )
            adjusted = store._settle_budget(
                adjusted_request,
                authority.issue_settlement_proof(
                    "validator-adjusted-proof-t17", adjusted_request
                ),
                authority,
            )
            validation = SyntheticValidationCoordinator(
                store, TransitionEngine(), authority, validator_adapter
            )
            request = ReconcileValidatorResultRequest(
                "reconciliation-validator-result-t17",
                "reconciliation-validator-result-command-t17",
                "reconciliation-validator-result-event-t17",
                "repo-1", "run-1", "item-1", "effect-1", "plan:run-1",
                "revision-1", observation[0], observation[1],
                cessation[0], cessation[1], cessation[2],
                adjusted.settlement_event_id, adjusted.settlement_hash,
                tuple(row[0] for row in uncertainties), "attempt-1", 1,
                adjusted.settlement_hash, None,
            )
            receipt = validation.reconcile_result(request)
            self.assertEqual(receipt.resulting_state, LifecycleState.VALIDATING)
            connection = sqlite3.connect(store._database_path)
            try:
                state = connection.execute(
                    "SELECT lifecycle_state, continuation_cursor FROM runs "
                    "WHERE run_id = 'run-1'"
                ).fetchone()
                retained = connection.execute(
                    "SELECT applied FROM validator_observations WHERE "
                    "observation_id = ?", (observation[0],)
                ).fetchone()[0]
                fence = connection.execute(
                    "SELECT COUNT(*) FROM dispatch_fences WHERE fence_id IN "
                    "(?, ?)",
                    tuple(row[1] for row in uncertainties),
                ).fetchone()[0]
                resolutions = connection.execute(
                    "SELECT proof_event_hash FROM uncertainty_resolutions WHERE "
                    "uncertainty_id IN (?, ?) ORDER BY proof_kind",
                    tuple(row[0] for row in uncertainties),
                ).fetchall()
            finally:
                connection.close()
            self.assertEqual(
                state,
                (
                    "VALIDATING",
                    "validation-application:v1:validator-observation-t08:"
                    "check-1:validator-attempt-1",
                ),
            )
            self.assertEqual((retained, fence), (0, 0))
            self.assertEqual(
                {row[0] for row in resolutions},
                {cessation[2], adjusted.settlement_hash},
            )
            self.assertEqual(store.table_counts()["outstanding_slot"], 1)
            store.load_verified("repo-1", authority=authority)
            applied = validation.apply_result(
                ValidationApplicationRequest(
                    "application-after-t17", "apply-command-after-t17",
                    "apply-event-after-t17", "repo-1", "run-1", "item-1",
                    "effect-1", "revision-1", "check-1",
                    "validator-attempt-1", observation[0],
                )
            )
            self.assertEqual(applied.resulting_state, LifecycleState.BLOCKED)
            store.load_verified("repo-1", authority=authority)

    def test_t17_validator_reconciliation_crash_boundaries_are_atomic(
        self,
    ) -> None:
        rollback_points = (
            "after_reconciliation_event_before_uncertainty_clearance",
            "after_reconciliation_writes_before_commit",
        )
        for point in rollback_points:
            with self.subTest(point=point), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                (
                    authority, store, validation, request, uncertainty_id,
                    fence_id,
                ) = self._prepare_t17_validator_reconciliation(root, point)
                connection = sqlite3.connect(store._database_path)
                try:
                    before_head = connection.execute(
                        "SELECT head_hash FROM runs WHERE run_id = 'run-1'"
                    ).fetchone()[0]
                finally:
                    connection.close()
                with self.assertRaises(InjectedFailure):
                    validation.reconcile_result(
                        request, failure_hook=raise_at(point)
                    )
                connection = sqlite3.connect(store._database_path)
                try:
                    state = connection.execute(
                        "SELECT (SELECT COUNT(*) FROM reconciliation_actions), "
                        "(SELECT COUNT(*) FROM uncertainty_resolutions), "
                        "(SELECT COUNT(*) FROM dispatch_fences WHERE reason_code "
                        "IN ('VALIDATOR_ACTIVITY_UNKNOWN', "
                        "'VALIDATOR_BILLING_UNKNOWN')), (SELECT head_hash "
                        "FROM runs WHERE run_id = 'run-1')",
                    ).fetchone()
                finally:
                    connection.close()
                self.assertEqual(
                    state, (0, 0, len(uncertainty_id), before_head)
                )
                recovered = validation.reconcile_result(request)
                self.assertFalse(recovered.replayed)
                store.load_verified("repo-1", authority=authority)

        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (
                authority, store, validation, request, _uncertainty_id,
                _fence_id,
            ) = self._prepare_t17_validator_reconciliation(root, "post-commit")
            with self.assertRaises(InjectedFailure):
                validation.reconcile_result(
                    request,
                    failure_hook=raise_at(
                        "after_reconciliation_commit_before_acknowledgement"
                    ),
                )
            replay = validation.reconcile_result(request)
            self.assertTrue(replay.replayed)
            store.load_verified("repo-1", authority=authority)

    def test_t17_recovery_rejects_projection_and_event_schema_tamper(self) -> None:
        projection_tampers = (
            (
                "uncertainty_instances", "origin_event_hash",
                "tampered-observation-hash", "uncertainty-instance projection",
            ),
            (
                "uncertainty_resolutions", "proof_event_hash",
                "tampered-settlement-hash", "uncertainty-resolution projection",
            ),
            (
                "reconciliation_actions", "source_event_hash",
                "tampered-source-hash", "reconciliation-action projection",
            ),
        )
        for table, column, value, message in projection_tampers:
            with (
                self.subTest(table=table, column=column),
                tempfile.TemporaryDirectory() as directory,
            ):
                root = Path(directory)
                (
                    authority, store, validation, request, _uncertainty_id,
                    _fence_id,
                ) = self._prepare_t17_validator_reconciliation(
                    root, f"tamper-{table}-{column}"
                )
                validation.reconcile_result(request)
                connection = sqlite3.connect(store._database_path)
                try:
                    connection.execute(
                        f"UPDATE {table} SET {column} = ?", (value,)
                    )
                    connection.commit()
                finally:
                    connection.close()
                with self.assertRaisesRegex(StorageIntegrityError, message):
                    store.load_verified("repo-1", authority=authority)

        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (
                authority, store, validation, request, _uncertainty_id,
                _fence_id,
            ) = self._prepare_t17_validator_reconciliation(root, "event-surplus")
            validation.reconcile_result(request)
            connection = sqlite3.connect(store._database_path)
            connection.row_factory = sqlite3.Row
            try:
                row = connection.execute(
                    "SELECT body_json FROM events WHERE event_id = ?",
                    (request.event_id,),
                ).fetchone()
                body = json.loads(row["body_json"])
                body["surplus_field"] = "forbidden"
                event_hash = store._event_hash(body)
                body_json = json.dumps(
                    body, sort_keys=True, separators=(",", ":")
                )
                connection.execute(
                    "UPDATE events SET event_hash = ?, body_json = ? WHERE "
                    "event_id = ?", (event_hash, body_json, request.event_id)
                )
                connection.execute(
                    "UPDATE reconciliation_actions SET event_hash = ?, "
                    "body_json = ? WHERE reconciliation_id = ?",
                    (event_hash, body_json, request.reconciliation_id),
                )
                connection.execute(
                    "UPDATE command_outcomes SET event_hash = ? WHERE "
                    "command_id = ?", (event_hash, request.command_id)
                )
                connection.execute(
                    "UPDATE runs SET head_hash = ? WHERE run_id = 'run-1'",
                    (event_hash,),
                )
                connection.execute(
                    "UPDATE repositories SET catalog_head = ? WHERE "
                    "repository_id = 'repo-1'", (event_hash,),
                )
                connection.commit()
            finally:
                connection.close()
            with self.assertRaisesRegex(
                StorageIntegrityError, "validator reconciliation"
            ):
                store.load_verified("repo-1", authority=authority)

    def test_t17_recovery_ignores_later_same_scope_pause_in_another_run(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (
                authority, store, validation, request, _uncertainty_id,
                _fence_id,
            ) = self._prepare_t17_validator_reconciliation(
                root, "future-cross-run-pause"
            )
            validation.reconcile_result(request)
            connection = sqlite3.connect(store._database_path)
            try:
                catalog_head = connection.execute(
                    "SELECT catalog_head FROM repositories WHERE "
                    "repository_id = 'repo-1'"
                ).fetchone()[0]
                writer_epoch = connection.execute(
                    "SELECT MAX(writer_epoch) + 1 FROM events WHERE "
                    "repository_id = 'repo-1'"
                ).fetchone()[0]
            finally:
                connection.close()
            plan = store.accept_plan(
                PlanAcceptanceRequest(
                    "plan:run-2", "plan-command-run-2", "plan-event-run-2",
                    "repo-1", "run-2", "item-1", "effect-1", "revision-2",
                    "payload-1", "scope-2", "budget-2", ("check-1",),
                ),
                expected_head=catalog_head,
                writer_epoch=writer_epoch,
            )
            grant = SyntheticOperatorGrant(
                "pause-grant-run-2", "repo-1", "run-2", "PAUSE",
                "pause-scope-run-2",
            )
            authority.register_operator(grant)
            store.pause_before_dispatch(
                PauseBeforeDispatchRequest(
                    "pause-run-2", "pause-command-run-2",
                    "pause-request-run-2", "pause-settled-run-2",
                    "pause-fence-run-2", "repo-1", "run-2", "item-1",
                    "OPERATOR_PAUSE", None,
                ),
                authority.claim_operator(*grant.__dict__.values()), authority,
            )
            connection = sqlite3.connect(store._database_path)
            connection.row_factory = sqlite3.Row
            try:
                row = connection.execute(
                    "SELECT body_json FROM events WHERE event_id = ?",
                    (request.event_id,),
                ).fetchone()
                body = json.loads(row["body_json"])
                body["lifecycle_to"] = LifecycleState.PAUSED.value
                body["continuation_cursor"] = None
                event_hash = store._event_hash(body)
                body_json = json.dumps(
                    body, sort_keys=True, separators=(",", ":")
                )
                connection.execute(
                    "UPDATE events SET event_hash = ?, body_json = ? WHERE "
                    "event_id = ?", (event_hash, body_json, request.event_id)
                )
                connection.execute(
                    "UPDATE reconciliation_actions SET event_hash = ?, "
                    "body_json = ?, resulting_state = 'PAUSED', "
                    "continuation_cursor = NULL WHERE reconciliation_id = ?",
                    (event_hash, body_json, request.reconciliation_id),
                )
                connection.execute(
                    "UPDATE command_outcomes SET event_hash = ? WHERE "
                    "command_id = ?", (event_hash, request.command_id)
                )
                connection.execute(
                    "UPDATE runs SET head_hash = ?, lifecycle_state = 'PAUSED', "
                    "continuation_cursor = NULL WHERE run_id = 'run-1'",
                    (event_hash,),
                )
                connection.commit()
            finally:
                connection.close()
            self.assertNotEqual(plan.event_hash, event_hash)
            with self.assertRaisesRegex(
                StorageIntegrityError, "validator reconciliation"
            ):
                store.load_verified("repo-1", authority=authority)

        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (
                authority, store, validation, request, _uncertainty_id,
                _fence_id,
            ) = self._prepare_t17_validator_reconciliation(root, "route-tamper")
            validation.reconcile_result(request)
            connection = sqlite3.connect(store._database_path)
            connection.row_factory = sqlite3.Row
            try:
                row = connection.execute(
                    "SELECT body_json FROM events WHERE event_id = ?",
                    (request.event_id,),
                ).fetchone()
                body = json.loads(row["body_json"])
                body["lifecycle_to"] = LifecycleState.BLOCKED.value
                body["continuation_cursor"] = None
                event_hash = store._event_hash(body)
                body_json = json.dumps(
                    body, sort_keys=True, separators=(",", ":")
                )
                connection.execute(
                    "UPDATE events SET event_hash = ?, body_json = ? WHERE "
                    "event_id = ?", (event_hash, body_json, request.event_id)
                )
                connection.execute(
                    "UPDATE reconciliation_actions SET event_hash = ?, "
                    "body_json = ?, resulting_state = 'BLOCKED', "
                    "continuation_cursor = NULL WHERE reconciliation_id = ?",
                    (event_hash, body_json, request.reconciliation_id),
                )
                connection.execute(
                    "UPDATE command_outcomes SET event_hash = ? WHERE "
                    "command_id = ?", (event_hash, request.command_id)
                )
                connection.execute(
                    "UPDATE runs SET head_hash = ?, lifecycle_state = 'BLOCKED', "
                    "continuation_cursor = NULL WHERE run_id = 'run-1'",
                    (event_hash,),
                )
                connection.execute(
                    "UPDATE repositories SET catalog_head = ? WHERE "
                    "repository_id = 'repo-1'", (event_hash,)
                )
                connection.commit()
            finally:
                connection.close()
            with self.assertRaisesRegex(
                StorageIntegrityError, "validator reconciliation"
            ):
                store.load_verified("repo-1", authority=authority)

    def test_t17_preexisting_cross_run_same_effect_pause_is_blocker(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (
                authority, store, validation, request, _uncertainty_ids,
                _fence_ids,
            ) = self._prepare_t17_validator_reconciliation(
                root, "prior-cross-run-pause"
            )
            connection = sqlite3.connect(store._database_path)
            try:
                catalog_head = connection.execute(
                    "SELECT catalog_head FROM repositories WHERE "
                    "repository_id = 'repo-1'"
                ).fetchone()[0]
                writer_epoch = connection.execute(
                    "SELECT MAX(writer_epoch) + 1 FROM events WHERE "
                    "repository_id = 'repo-1'"
                ).fetchone()[0]
            finally:
                connection.close()
            store.accept_plan(
                PlanAcceptanceRequest(
                    "plan:run-2", "plan-command-prior-run-2",
                    "plan-event-prior-run-2", "repo-1", "run-2", "item-1",
                    "effect-1", "revision-2", "payload-1", "scope-2",
                    "budget-2", ("check-1",),
                ),
                expected_head=catalog_head,
                writer_epoch=writer_epoch,
            )
            grant = SyntheticOperatorGrant(
                "pause-grant-prior-run-2", "repo-1", "run-2", "PAUSE",
                "pause-scope-prior-run-2",
            )
            authority.register_operator(grant)
            pause = store.pause_before_dispatch(
                PauseBeforeDispatchRequest(
                    "pause-prior-run-2", "pause-command-prior-run-2",
                    "pause-request-prior-run-2", "pause-settled-prior-run-2",
                    "pause-fence-prior-run-2", "repo-1", "run-2", "item-1",
                    "OPERATOR_PAUSE", None,
                ),
                authority.claim_operator(*grant.__dict__.values()), authority,
            )

            reconciled = validation.reconcile_result(request)

            self.assertEqual(reconciled.resulting_state, LifecycleState.BLOCKED)
            self.assertEqual(
                store.load_run_lifecycle("run-2"), LifecycleState.PAUSED
            )
            connection = sqlite3.connect(store._database_path)
            try:
                fence = connection.execute(
                    "SELECT originating_event_id FROM dispatch_fences WHERE "
                    "fence_id = 'pause-fence-prior-run-2'"
                ).fetchone()
            finally:
                connection.close()
            self.assertEqual(fence, ("pause-request-prior-run-2",))
            store.load_verified("repo-1", authority=authority)

    def test_t17_legacy_uncertainty_projection_missing_trusted_source_fails_closed(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (
                authority, store, _validation, _request, uncertainty_id,
                fence_id,
            ) = self._prepare_t17_validator_reconciliation(root, "legacy")
            connection = sqlite3.connect(store._database_path)
            try:
                event_bytes = connection.execute(
                    "SELECT event_id, body_json FROM events ORDER BY rowid"
                ).fetchall()
                connection.executemany(
                    "DELETE FROM dispatch_fences WHERE fence_id = ?",
                    ((value,) for value in fence_id),
                )
                connection.execute("DROP TABLE reconciliation_actions")
                connection.execute("DROP TABLE uncertainty_resolutions")
                connection.execute("DROP TABLE uncertainty_instances")
                connection.execute(
                    "DROP TABLE verified_receipt_reconciliation_actions"
                )
                connection.execute("DROP TABLE operation_retry_authorizations")
                connection.execute("DROP TABLE operation_recovery_actions")
                connection.execute(
                    "DROP TABLE operation_nonexecution_resume_actions"
                )
                connection.execute("DROP TABLE proven_nonexecution_actions")
                connection.execute("DROP TABLE proof_free_disposition_actions")
                connection.execute(
                    "DROP TABLE settled_validation_pause_resume_actions"
                )
                connection.execute("DROP TABLE validation_pause_settlements")
                connection.execute("DROP TABLE active_validation_pause_actions")
                strip_t28_foundation_schema(connection)
                connection.execute("PRAGMA user_version = 0")
                connection.commit()
            finally:
                connection.close()
            migrated = SQLiteStateStore(
                store._database_path, store._freshness_oracle, "repo-1"
            )
            migrated._bind_classification_authority(authority)
            connection = sqlite3.connect(store._database_path)
            try:
                migrated_event_bytes = connection.execute(
                    "SELECT event_id, body_json FROM events ORDER BY rowid"
                ).fetchall()
                restored = connection.execute(
                    "SELECT uncertainty_id, fence_id FROM "
                    "uncertainty_instances ORDER BY uncertainty_kind"
                ).fetchall()
            finally:
                connection.close()
            self.assertEqual(migrated_event_bytes, event_bytes)
            self.assertEqual(
                restored, list(zip(uncertainty_id, fence_id, strict=True))
            )
            with self.assertRaisesRegex(
                StorageIntegrityError, "readiness event semantics"
            ):
                migrated.load_verified("repo-1", authority=authority)

    def test_t17_partial_reconciliation_schema_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            store = SQLiteStateStore(
                root / "state.sqlite3", AlwaysFreshOracle(), "repo-1"
            )
            connection = sqlite3.connect(store._database_path)
            try:
                connection.execute("DROP TABLE reconciliation_actions")
                connection.commit()
            finally:
                connection.close()
            with self.assertRaisesRegex(
                StorageIntegrityError, "partially migrated"
            ):
                SQLiteStateStore(
                    store._database_path, store._freshness_oracle, "repo-1"
                )

    def test_t17_v1_to_v2_preserves_validator_history_and_fails_closed_without_trusted_source(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as directory:
            (
                authority, store, validation, request, _uncertainty_ids,
                _fence_ids,
            ) = self._prepare_t17_validator_reconciliation(
                Path(directory), "v1-to-v2-preservation"
            )
            validation.reconcile_result(request)
            connection = sqlite3.connect(store._database_path)
            try:
                before = connection.execute(
                    "SELECT event_hash, body_json FROM events WHERE event_kind "
                    "= 'RECONCILIATION_RECORDED'"
                ).fetchone()
                connection.execute(
                    "DROP TABLE verified_receipt_reconciliation_actions"
                )
                connection.execute("DROP TABLE operation_retry_authorizations")
                connection.execute("DROP TABLE operation_recovery_actions")
                connection.execute(
                    "DROP TABLE operation_nonexecution_resume_actions"
                )
                connection.execute("DROP TABLE proven_nonexecution_actions")
                connection.execute("DROP TABLE proof_free_disposition_actions")
                connection.execute(
                    "DROP TABLE settled_validation_pause_resume_actions"
                )
                connection.execute("DROP TABLE validation_pause_settlements")
                connection.execute("DROP TABLE active_validation_pause_actions")
                strip_t28_foundation_schema(connection)
                connection.execute("PRAGMA user_version = 1")
                connection.commit()
            finally:
                connection.close()
            migrated = SQLiteStateStore(
                store._database_path, store._freshness_oracle, "repo-1"
            )
            connection = sqlite3.connect(store._database_path)
            try:
                after = connection.execute(
                    "SELECT event_hash, body_json FROM events WHERE event_kind "
                    "= 'RECONCILIATION_RECORDED'"
                ).fetchone()
                version = connection.execute(
                    "PRAGMA user_version"
                ).fetchone()[0]
                action_count = connection.execute(
                    "SELECT COUNT(*) FROM "
                    "verified_receipt_reconciliation_actions"
                ).fetchone()[0]
            finally:
                connection.close()
            self.assertEqual(after, before)
            self.assertEqual(version, 8)
            self.assertEqual(action_count, 0)
            with self.assertRaisesRegex(
                StorageIntegrityError, "readiness event semantics"
            ):
                migrated.load_verified("repo-1", authority=authority)

    def test_t17_v2_missing_verified_receipt_projection_fails_closed(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as directory:
            store = SQLiteStateStore(
                Path(directory) / "state.sqlite3",
                AlwaysFreshOracle(), "repo-1",
            )
            connection = sqlite3.connect(store._database_path)
            try:
                connection.execute(
                    "DROP TABLE verified_receipt_reconciliation_actions"
                )
                connection.commit()
            finally:
                connection.close()
            with self.assertRaisesRegex(
                StorageIntegrityError,
                "verified-receipt action schema is missing or incompatible",
            ):
                SQLiteStateStore(
                    store._database_path, store._freshness_oracle, "repo-1"
                )

    def test_t17_semantic_version_reopen_is_stable_and_surplus_fails_closed(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as directory:
            store = SQLiteStateStore(
                Path(directory) / "state.sqlite3",
                AlwaysFreshOracle(),
                "repo-1",
            )
            reopened = SQLiteStateStore(
                store._database_path, store._freshness_oracle, "repo-1"
            )
            self.assertEqual(reopened.table_counts(), store.table_counts())
            connection = sqlite3.connect(store._database_path)
            try:
                self.assertEqual(
                    connection.execute("PRAGMA user_version").fetchone()[0], 8
                )
                connection.execute(
                    "INSERT INTO dispatch_fences VALUES ("
                    "'surplus-operation-uncertainty', 'repo-1', NULL, NULL, "
                    "'OPERATION_OUTCOME_UNKNOWN', 'fabricated-origin')"
                )
                connection.commit()
            finally:
                connection.close()
            with self.assertRaisesRegex(
                StorageIntegrityError,
                "operation-uncertainty projection diverges",
            ):
                SQLiteStateStore(
                    store._database_path, store._freshness_oracle, "repo-1"
                )

    def test_t17_unknown_semantic_version_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            store = SQLiteStateStore(
                Path(directory) / "state.sqlite3",
                AlwaysFreshOracle(),
                "repo-1",
            )
            connection = sqlite3.connect(store._database_path)
            try:
                connection.execute("PRAGMA user_version = 9")
                connection.commit()
            finally:
                connection.close()
            with self.assertRaisesRegex(
                StorageIntegrityError, "semantic version is unsupported"
            ):
                SQLiteStateStore(
                    store._database_path, store._freshness_oracle, "repo-1"
                )

    def test_t17_v0_surplus_operation_uncertainty_is_not_healed(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            (
                _authority, store, _validation, _request, _uncertainty_ids,
                _fence_ids,
            ) = self._prepare_t17_validator_reconciliation(
                Path(directory), "legacy-operation-surplus"
            )
            connection = sqlite3.connect(store._database_path)
            try:
                observation = connection.execute(
                    "SELECT event_id, event_hash, repository_id, run_id, "
                    "item_id, logical_effect_id, attempt_id FROM "
                    "effect_observations LIMIT 1"
                ).fetchone()
                reservation_id = connection.execute(
                    "SELECT reservation_id FROM budget_reservations WHERE "
                    "repository_id = ? AND run_id = ? AND "
                    "logical_effect_id = ? AND attempt_id = ?",
                    (
                        observation[2], observation[3], observation[5],
                        observation[6],
                    ),
                ).fetchone()[0]
                connection.execute(
                    "DROP TABLE verified_receipt_reconciliation_actions"
                )
                connection.execute("PRAGMA user_version = 0")
                connection.execute(
                    "INSERT INTO dispatch_fences VALUES ("
                    "'fabricated-operation-uncertainty', ?, ?, ?, "
                    "'OPERATION_OUTCOME_UNKNOWN', ?)",
                    (observation[2], observation[4], observation[5], observation[0]),
                )
                connection.execute(
                    "INSERT INTO uncertainty_instances VALUES ("
                    "'fabricated-operation-uncertainty', "
                    "'fabricated-operation-uncertainty', 'OUTCOME', ?, ?, ?, ?, "
                    "?, NULL, ?, ?, ?, NULL, '{}')",
                    (
                        observation[2], observation[3], observation[4],
                        observation[5], observation[6], observation[0],
                        observation[1], reservation_id,
                    ),
                )
                connection.commit()
            finally:
                connection.close()
            with self.assertRaisesRegex(
                StorageIntegrityError, "legacy operation uncertainty"
            ):
                SQLiteStateStore(
                    store._database_path, store._freshness_oracle, "repo-1"
                )

    def test_t17_v0_disguised_operation_uncertainty_is_not_healed(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            (
                _authority, store, _validation, _request, _uncertainty_ids,
                _fence_ids,
            ) = self._prepare_t17_validator_reconciliation(
                Path(directory), "legacy-operation-disguised-surplus"
            )
            connection = sqlite3.connect(store._database_path)
            try:
                observation = connection.execute(
                    "SELECT event_id, event_hash, repository_id, run_id, "
                    "item_id, logical_effect_id, attempt_id FROM "
                    "effect_observations LIMIT 1"
                ).fetchone()
                reservation_id = connection.execute(
                    "SELECT reservation_id FROM budget_reservations WHERE "
                    "repository_id = ? AND run_id = ? AND "
                    "logical_effect_id = ? AND attempt_id = ?",
                    (
                        observation[2], observation[3], observation[5],
                        observation[6],
                    ),
                ).fetchone()[0]
                connection.execute(
                    "DROP TABLE verified_receipt_reconciliation_actions"
                )
                connection.execute("PRAGMA user_version = 0")
                connection.execute(
                    "INSERT INTO dispatch_fences VALUES ("
                    "'disguised-operation-uncertainty', ?, ?, ?, "
                    "'VALIDATOR_BILLING_UNKNOWN', ?)",
                    (observation[2], observation[4], observation[5], observation[0]),
                )
                connection.execute(
                    "INSERT INTO uncertainty_instances VALUES ("
                    "'disguised-operation-uncertainty', "
                    "'disguised-operation-uncertainty', 'BILLING', ?, ?, ?, ?, "
                    "?, 'fake-validator-check', ?, ?, ?, NULL, '{}')",
                    (
                        observation[2], observation[3], observation[4],
                        observation[5], observation[6], observation[0],
                        observation[1], reservation_id,
                    ),
                )
                connection.commit()
            finally:
                connection.close()
            with self.assertRaisesRegex(
                StorageIntegrityError, "legacy operation uncertainty"
            ):
                SQLiteStateStore(
                    store._database_path, store._freshness_oracle, "repo-1"
                )
            connection = sqlite3.connect(store._database_path)
            try:
                version = connection.execute("PRAGMA user_version").fetchone()[0]
                disguised = connection.execute(
                    "SELECT check_id FROM uncertainty_instances WHERE "
                    "uncertainty_id = 'disguised-operation-uncertainty'"
                ).fetchone()
            finally:
                connection.close()
            self.assertEqual(version, 0)
            self.assertEqual(disguised, ("fake-validator-check",))

    def test_t17_v0_settlement_projection_tamper_rolls_back(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            (
                _authority, store, _validation, _request, _uncertainty_ids,
                _fence_ids,
            ) = self._prepare_t17_validator_reconciliation(
                Path(directory), "legacy-settlement-projection-tamper"
            )
            connection = sqlite3.connect(store._database_path)
            try:
                settlement_event_id = connection.execute(
                    "SELECT settlement_event_id FROM effect_observations LIMIT 1"
                ).fetchone()[0]
                connection.execute(
                    "DROP TABLE verified_receipt_reconciliation_actions"
                )
                connection.execute("PRAGMA user_version = 0")
                connection.execute(
                    "UPDATE budget_settlements SET disposition = ?, "
                    "uncertainty = 1 WHERE settlement_event_id = ?",
                    (
                        BudgetDisposition.UNKNOWN_WORST_CASE_CHARGED.value,
                        settlement_event_id,
                    ),
                )
                connection.commit()
            finally:
                connection.close()
            with self.assertRaisesRegex(
                StorageIntegrityError,
                "settlement projection diverges from history",
            ):
                SQLiteStateStore(
                    store._database_path, store._freshness_oracle, "repo-1"
                )
            connection = sqlite3.connect(store._database_path)
            try:
                version = connection.execute("PRAGMA user_version").fetchone()[0]
                tampered = connection.execute(
                    "SELECT disposition, uncertainty FROM budget_settlements "
                    "WHERE settlement_event_id = ?",
                    (settlement_event_id,),
                ).fetchone()
            finally:
                connection.close()
            self.assertEqual(version, 0)
            self.assertEqual(
                tampered,
                (BudgetDisposition.UNKNOWN_WORST_CASE_CHARGED.value, 1),
            )

    def test_t17_backfill_failure_rolls_back_new_schema(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (
                _authority, store, _validation, _request, uncertainty_ids,
                fence_ids,
            ) = self._prepare_t17_validator_reconciliation(
                root, "backfill-rollback"
            )
            connection = sqlite3.connect(store._database_path)
            try:
                connection.executemany(
                    "DELETE FROM dispatch_fences WHERE fence_id = ?",
                    ((value,) for value in fence_ids),
                )
                connection.execute("DROP TABLE reconciliation_actions")
                connection.execute("DROP TABLE uncertainty_resolutions")
                connection.execute("DROP TABLE uncertainty_instances")
                connection.execute(
                    "DROP TABLE verified_receipt_reconciliation_actions"
                )
                connection.execute("PRAGMA user_version = 0")
                connection.execute(
                    "INSERT INTO dispatch_fences VALUES (?, 'repo-1', "
                    "'item-1', 'effect-1', 'CONFLICTING_LEGACY_FENCE', "
                    "'validator-observe-event-t08')",
                    (uncertainty_ids[0],),
                )
                connection.commit()
            finally:
                connection.close()
            with self.assertRaises(sqlite3.IntegrityError):
                SQLiteStateStore(
                    store._database_path, store._freshness_oracle, "repo-1"
                )
            connection = sqlite3.connect(store._database_path)
            try:
                tables = {
                    row[0]
                    for row in connection.execute(
                        "SELECT name FROM sqlite_master WHERE type = 'table' "
                        "AND name IN ('uncertainty_instances', "
                        "'uncertainty_resolutions', 'reconciliation_actions')"
                    )
                }
                semantic_version = connection.execute(
                    "PRAGMA user_version"
                ).fetchone()[0]
            finally:
                connection.close()
            self.assertEqual(tables, set())
            self.assertEqual(semantic_version, 0)

    def test_t17_legacy_projection_tamper_rolls_back_new_schema(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (
                _authority, store, _validation, _request, _uncertainty_ids,
                fence_ids,
            ) = self._prepare_t17_validator_reconciliation(
                root, "legacy-projection-tamper"
            )
            connection = sqlite3.connect(store._database_path)
            try:
                connection.executemany(
                    "DELETE FROM dispatch_fences WHERE fence_id = ?",
                    ((value,) for value in fence_ids),
                )
                connection.execute("DROP TABLE reconciliation_actions")
                connection.execute("DROP TABLE uncertainty_resolutions")
                connection.execute("DROP TABLE uncertainty_instances")
                connection.execute(
                    "DROP TABLE verified_receipt_reconciliation_actions"
                )
                connection.execute("PRAGMA user_version = 0")
                connection.execute(
                    "UPDATE validator_observations SET event_hash = ? WHERE "
                    "observation_id = 'validator-observation-t08'",
                    ("tampered-legacy-observation-hash",),
                )
                connection.commit()
            finally:
                connection.close()
            with self.assertRaisesRegex(
                StorageIntegrityError, "legacy validator-observation"
            ):
                SQLiteStateStore(
                    store._database_path, store._freshness_oracle, "repo-1"
                )
            connection = sqlite3.connect(store._database_path)
            try:
                tables = {
                    row[0]
                    for row in connection.execute(
                        "SELECT name FROM sqlite_master WHERE type = 'table' "
                        "AND name IN ('uncertainty_instances', "
                        "'uncertainty_resolutions', 'reconciliation_actions')"
                    )
                }
            finally:
                connection.close()
            self.assertEqual(tables, set())

    def test_t17_operation_derivation_failure_rolls_back_validator_backfill(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (
                _authority, store, _validation, _request, _uncertainty_ids,
                fence_ids,
            ) = self._prepare_t17_validator_reconciliation(
                root, "operation-phase-rollback"
            )
            connection = sqlite3.connect(store._database_path)
            try:
                connection.executemany(
                    "DELETE FROM dispatch_fences WHERE fence_id = ?",
                    ((value,) for value in fence_ids),
                )
                connection.execute("DROP TABLE reconciliation_actions")
                connection.execute("DROP TABLE uncertainty_resolutions")
                connection.execute("DROP TABLE uncertainty_instances")
                connection.execute(
                    "DROP TABLE verified_receipt_reconciliation_actions"
                )
                connection.execute("PRAGMA user_version = 0")
                connection.execute(
                    "UPDATE effect_observations SET source_claim_id = "
                    "'tampered-operation-claim'"
                )
                connection.commit()
            finally:
                connection.close()
            with self.assertRaisesRegex(
                StorageIntegrityError, "effect-observation projection"
            ):
                SQLiteStateStore(
                    store._database_path, store._freshness_oracle, "repo-1"
                )
            connection = sqlite3.connect(store._database_path)
            try:
                tables = {
                    row[0]
                    for row in connection.execute(
                        "SELECT name FROM sqlite_master WHERE type = 'table' "
                        "AND name IN ('uncertainty_instances', "
                        "'uncertainty_resolutions', 'reconciliation_actions')"
                    )
                }
                semantic_version = connection.execute(
                    "PRAGMA user_version"
                ).fetchone()[0]
            finally:
                connection.close()
            self.assertEqual(tables, set())
            self.assertEqual(semantic_version, 0)

    def test_t17_rejects_incomplete_activity_proof_and_rebound_slot(self) -> None:
        mutations = (
            ("cessation", lambda request: replace(
                request, cessation_event_hash="wrong-cessation-hash"
            )),
            ("uncertainty", lambda request: replace(
                request,
                resolved_uncertainty_ids=request.resolved_uncertainty_ids[:1],
            )),
            ("slot", lambda request: replace(
                request, expected_slot_generation=2
            )),
        )
        for label, mutate in mutations:
            with (
                self.subTest(label=label),
                tempfile.TemporaryDirectory() as directory,
            ):
                root = Path(directory)
                (
                    _authority, _store, validation, request,
                    _uncertainty_ids, _fence_ids,
                ) = self._prepare_t17_validator_reconciliation(root, label)
                with self.assertRaises(DispatchDenied):
                    validation.reconcile_result(mutate(request))

    def test_t17_resolved_validator_result_retains_stacked_t09_pause(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (
                authority, store, validation, request, _uncertainty_ids,
                _fence_ids,
            ) = self._prepare_t17_validator_reconciliation(root, "stacked-pause")
            connection = sqlite3.connect(store._database_path)
            try:
                source = connection.execute(
                    "SELECT event_id, head_hash FROM runs JOIN events ON "
                    "events.event_hash = runs.head_hash WHERE runs.run_id = ?",
                    ("run-1",),
                ).fetchone()
            finally:
                connection.close()
            pause_request = PauseReconciliationRequest(
                "t17-stacked-pause", "t17-stacked-pause-command",
                "t17-stacked-pause-event", "t17-stacked-pause-fence",
                "repo-1", "run-1", "item-1", "effect-1", "plan:run-1",
                "revision-1", "OPERATOR_PAUSE_RECONCILIATION", source[0],
                source[1], None,
            )
            grant = SyntheticOperatorGrant(
                "t17-stacked-pause-grant", "repo-1", "run-1", "PAUSE",
                "t17-stacked-pause-scope",
            )
            authority.register_operator(grant)
            paused = store.pause_reconciliation(
                pause_request,
                authority.claim_operator(*grant.__dict__.values()),
                authority,
            )
            second_pause_request = PauseReconciliationRequest(
                "t17-stacked-pause-2", "t17-stacked-pause-command-2",
                "t17-stacked-pause-event-2", "t17-stacked-pause-fence-2",
                "repo-1", "run-1", "item-1", "effect-1", "plan:run-1",
                "revision-1", "OPERATOR_PAUSE_RECONCILIATION",
                paused.event_id, paused.event_hash, None,
            )
            second_pause_grant = SyntheticOperatorGrant(
                "t17-stacked-pause-grant-2", "repo-1", "run-1", "PAUSE",
                "t17-stacked-pause-scope-2",
            )
            authority.register_operator(second_pause_grant)
            second_paused = store.pause_reconciliation(
                second_pause_request,
                authority.claim_operator(*second_pause_grant.__dict__.values()),
                authority,
            )
            reconciled = validation.reconcile_result(
                replace(request, expected_run_head=second_paused.event_hash)
            )
            self.assertEqual(reconciled.resulting_state, LifecycleState.PAUSED)
            connection = sqlite3.connect(store._database_path)
            try:
                fences = connection.execute(
                    "SELECT fence_id FROM dispatch_fences ORDER BY fence_id"
                ).fetchall()
            finally:
                connection.close()
            self.assertEqual(
                fences,
                [
                    (pause_request.fence_id,),
                    (second_pause_request.fence_id,),
                ],
            )
            store.load_verified("repo-1", authority=authority)
            connection = sqlite3.connect(store._database_path)
            try:
                run_state = connection.execute(
                    "SELECT continuation_cursor FROM runs WHERE run_id = ?",
                    ("run-1",),
                ).fetchone()
                run_heads = dict(
                    connection.execute(
                        "SELECT run_id, head_hash FROM runs ORDER BY run_id"
                    )
                )
                catalog_head = connection.execute(
                    "SELECT catalog_head FROM repositories WHERE "
                    "repository_id = 'repo-1'"
                ).fetchone()[0]
            finally:
                connection.close()
            self.assertTrue(
                run_state[0].startswith("validation-application:v1:")
            )
            resume_request = ReconciliationPauseResumeRequest(
                "t17-t09-resume", "t17-t09-resume-command",
                "t17-t09-resume-event", "repo-1", "run-1", "item-1",
                "effect-1", "plan:run-1", "revision-1",
                pause_request.pause_id, pause_request.event_id,
                paused.event_hash, pause_request.fence_id,
                request.reconciliation_id, reconciled.event_id,
                reconciled.event_hash, run_state[0], catalog_head,
                reconciled.event_hash,
                store._run_heads_digest(run_heads),
            )
            resume_grant = SyntheticOperatorGrant(
                "t17-t09-resume-grant", "repo-1", "run-1", "RESUME",
                "t17-t09-resume-scope",
            )
            authority.register_operator(resume_grant)
            resume_capability = authority.claim_operator(
                *resume_grant.__dict__.values()
            )
            resume_evidence = authority.issue_reconciliation_resume_evidence(
                "t17-t09-resume-proof", resume_request
            )
            with self.assertRaises(InjectedFailure):
                store.resume_reconciliation_pause(
                    resume_request, resume_capability, resume_evidence,
                    authority,
                    failure_hook=raise_at(
                        "after_reconciliation_resume_writes_before_commit"
                    ),
                )
            self.assertEqual(
                store.table_counts()["reconciliation_resume_actions"], 0
            )
            self.assertEqual(store.table_counts()["dispatch_fences"], 2)
            resumed = store.resume_reconciliation_pause(
                resume_request, resume_capability, resume_evidence, authority,
            )
            self.assertEqual(resumed.resulting_state, LifecycleState.PAUSED)
            self.assertEqual(store.table_counts()["outstanding_slot"], 1)
            store.load_verified("repo-1", authority=authority)
            replay = store.resume_reconciliation_pause(
                resume_request, resume_capability, resume_evidence, authority,
            )
            self.assertTrue(replay.replayed)
            self.assertEqual(replay.event_hash, resumed.event_hash)
            self.assertEqual(
                store.table_counts()["reconciliation_resume_actions"], 1
            )
            self.assertEqual(store.table_counts()["dispatch_fences"], 1)

            connection = sqlite3.connect(store._database_path)
            try:
                run_heads = dict(connection.execute(
                    "SELECT run_id, head_hash FROM runs ORDER BY run_id"
                ))
                catalog_head = connection.execute(
                    "SELECT catalog_head FROM repositories WHERE "
                    "repository_id = 'repo-1'"
                ).fetchone()[0]
            finally:
                connection.close()
            second_resume_request = ReconciliationPauseResumeRequest(
                "t17-t09-resume-2", "t17-t09-resume-command-2",
                "t17-t09-resume-event-2", "repo-1", "run-1", "item-1",
                "effect-1", "plan:run-1", "revision-1",
                second_pause_request.pause_id, second_pause_request.event_id,
                second_paused.event_hash, second_pause_request.fence_id,
                request.reconciliation_id, reconciled.event_id,
                reconciled.event_hash, run_state[0], catalog_head,
                resumed.event_hash, store._run_heads_digest(run_heads),
            )
            second_resume_grant = SyntheticOperatorGrant(
                "t17-t09-resume-grant-2", "repo-1", "run-1", "RESUME",
                "t17-t09-resume-scope-2",
            )
            authority.register_operator(second_resume_grant)
            second_resume_capability = authority.claim_operator(
                *second_resume_grant.__dict__.values()
            )
            second_resume_evidence = (
                authority.issue_reconciliation_resume_evidence(
                    "t17-t09-resume-proof-2", second_resume_request
                )
            )
            second_resumed = store.resume_reconciliation_pause(
                second_resume_request, second_resume_capability,
                second_resume_evidence, authority,
            )
            self.assertEqual(
                second_resumed.resulting_state, LifecycleState.VALIDATING
            )
            self.assertEqual(store.table_counts()["dispatch_fences"], 0)
            store.load_verified("repo-1", authority=authority)
            second_replay = store.resume_reconciliation_pause(
                second_resume_request, second_resume_capability,
                second_resume_evidence, authority,
            )
            self.assertTrue(second_replay.replayed)
            self.assertEqual(second_replay.event_hash, second_resumed.event_hash)
            self.assertEqual(
                store.table_counts()["reconciliation_resume_actions"], 2
            )

            connection = sqlite3.connect(store._database_path)
            try:
                body = json.loads(connection.execute(
                    "SELECT body_json FROM reconciliation_resume_actions "
                    "WHERE resume_id = ?", (second_resume_request.resume_id,)
                ).fetchone()[0])
                body["source_kind"] = "LEGACY_INFERRED"
                event_hash = store._event_hash(body)
                body_json = json.dumps(
                    body, sort_keys=True, separators=(",", ":")
                )
                connection.execute(
                    "UPDATE events SET event_hash = ?, body_json = ? WHERE "
                    "event_id = ?",
                    (event_hash, body_json, second_resumed.event_id),
                )
                connection.execute(
                    "UPDATE reconciliation_resume_actions SET event_hash = ?, "
                    "body_json = ? WHERE resume_id = ?",
                    (event_hash, body_json, second_resume_request.resume_id),
                )
                connection.execute(
                    "UPDATE command_outcomes SET event_hash = ? WHERE "
                    "command_id = ?", (event_hash, second_resumed.command_id),
                )
                connection.execute(
                    "UPDATE runs SET head_hash = ? WHERE run_id = ?",
                    (event_hash, second_resume_request.run_id),
                )
                connection.execute(
                    "UPDATE repositories SET catalog_head = ? WHERE "
                    "repository_id = ?",
                    (event_hash, second_resume_request.repository_id),
                )
                connection.commit()
            finally:
                connection.close()
            with self.assertRaisesRegex(
                StorageIntegrityError, "reconciliation.*resume"
            ):
                store.load_verified("repo-1", authority=authority)

    def test_t17_resolved_validator_result_retains_t08_pause(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (
                authority, store, dispatch, validator_adapter,
                validator_intent, validator_capability, committed,
            ) = self._prepare_t08_active_validator(
                root, contact=True, result=True, intake_result=False
            )
            pause_request = self._t08_pause_request(
                store, suffix="t17-stacked-t08"
            )
            grant = SyntheticOperatorGrant(
                "t17-t08-pause-grant", "repo-1", "run-1", "PAUSE",
                "t17-t08-pause-scope",
            )
            authority.register_operator(grant)
            pause_receipt = dispatch.pause_validation(
                pause_request,
                authority.claim_operator(*grant.__dict__.values()),
            )
            self.assertEqual(
                pause_receipt.resulting_state,
                LifecycleState.RECONCILIATION_REQUIRED,
            )
            validation = SyntheticValidationCoordinator(
                store, TransitionEngine(), authority, validator_adapter
            )
            connection = sqlite3.connect(store._database_path)
            try:
                settlement_hash = connection.execute(
                    "SELECT settlement_head_hash FROM budget_reservations WHERE "
                    "reservation_id = 'validator-reservation-t08'"
                ).fetchone()[0]
            finally:
                connection.close()
            observation = validation.intake_result(
                ValidatorObservationCommand(
                    "validator-observation-t08",
                    "validator-observe-command-t08",
                    "validator-observe-event-t08", "repo-1", "run-1",
                    "item-1", "validator-intent-t08",
                    "validator-settlement-t08", settlement_hash,
                )
            )
            attestation = authority.issue_validator_cessation_attestation(
                "t17-t08-cessation-attestation", "t17-t08-cessation",
                validator_adapter._target_digest("repo-1"),
                validator_capability.claim_id,
                "VALIDATOR:validator-intent-t08", committed.event_hash,
                "repo-1", "run-1", "item-1", "effect-1", "revision-1",
                "check-1", "validator-attempt-1",
            )
            cessation_seal = validator_adapter.seal_cessation(
                attestation, authority
            )
            cessation = store.record_validator_cessation(
                ValidatorCessationRequest(
                    "t17-t08-cessation", "t17-t08-cessation-command",
                    "t17-t08-cessation-event", "repo-1", "run-1", "item-1",
                    "effect-1", validator_intent.validator_intent_id,
                    "validator-attempt-1", "revision-1", "check-1",
                    cessation_seal.cessation_hash,
                ),
                authority,
            )
            connection = sqlite3.connect(store._database_path)
            try:
                uncertainty_ids = tuple(
                    row[0]
                    for row in connection.execute(
                        "SELECT uncertainty_id FROM uncertainty_instances WHERE "
                        "origin_event_id = ?", (observation.event_id,)
                    )
                )
            finally:
                connection.close()
            reconciled = validation.reconcile_result(
                ReconcileValidatorResultRequest(
                    "t17-t08-reconciliation", "t17-t08-reconcile-command",
                    "t17-t08-reconcile-event", "repo-1", "run-1", "item-1",
                    "effect-1", "plan:run-1", "revision-1",
                    observation.observation_id, observation.event_hash,
                    "t17-t08-cessation", "t17-t08-cessation-event",
                    cessation.event_hash, "validator-settlement-t08",
                    settlement_hash, uncertainty_ids, "attempt-1", 1,
                    cessation.event_hash, None,
                )
            )
            self.assertEqual(reconciled.resulting_state, LifecycleState.PAUSED)
            store.load_verified("repo-1", authority=authority)

    def test_t09_reconciliation_pause_contract_and_coordinator_route(self) -> None:
        request = PauseReconciliationRequest(
            pause_id="reconciliation-pause-1",
            command_id="reconciliation-pause-command-1",
            event_id="reconciliation-pause-event-1",
            fence_id="reconciliation-pause-fence-1",
            repository_id="repo-1",
            run_id="run-1",
            item_id="item-1",
            logical_effect_id="effect-1",
            plan_id="plan-1",
            revision_digest="revision-1",
            reason_code="OPERATOR_PAUSE_RECONCILIATION",
            source_event_id="source-event-1",
            source_event_hash="source-hash-1",
            expected_preserved_continuation_cursor="operation-recovery:attempt-1",
        )
        request.validate()
        self.assertTrue(
            hasattr(SyntheticDispatchCoordinator, "pause_reconciliation"),
            "T09 requires a coordinator-owned reconciliation pause route",
        )
        with self.assertRaisesRegex(ValueError, "source event"):
            replace(request, source_event_hash="").validate()

    def test_t09_operation_reconciliation_pause_is_atomic_stacked_and_recoverable(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            authority, store, dispatch, adapter, effect_capability = (
                self._prepare_t09_operation_reconciliation(root)
            )
            target_before = adapter.reconcile(effect_capability.claim_id)
            connection = sqlite3.connect(store._database_path)
            try:
                before = connection.execute(
                    "SELECT (SELECT COUNT(*) FROM dispatch_fences), "
                    "(SELECT COUNT(*) FROM outstanding_slot), "
                    "(SELECT continuation_cursor FROM runs WHERE run_id = "
                    "'run-1'), (SELECT disposition || ':' || charged_units || "
                    "':' || uncertainty FROM budget_reservations WHERE "
                    "reservation_id = 'reservation-t09')"
                ).fetchone()
            finally:
                connection.close()
            pause_grant = SyntheticOperatorGrant(
                "pause-grant-t09", "repo-1", "run-1", "PAUSE",
                "pause-scope-t09",
            )
            stale_grant = SyntheticOperatorGrant(
                "pause-grant-t09-stale", "repo-1", "run-1", "PAUSE",
                "pause-scope-t09-stale",
            )
            authority.register_operator(pause_grant)
            authority.register_operator(stale_grant)
            request = self._t09_pause_request(store, suffix="operation")
            stale_request = replace(
                request,
                pause_id="reconciliation-pause-stale",
                command_id="reconciliation-pause-command-stale",
                event_id="reconciliation-pause-event-stale",
                fence_id="reconciliation-pause-fence-stale",
            )
            capability = authority.claim_operator(*pause_grant.__dict__.values())
            with patch.object(
                adapter, "reconcile", wraps=adapter.reconcile
            ) as reconcile_spy:
                receipt = dispatch.pause_reconciliation(request, capability)
                reconcile_spy.assert_not_called()
            self.assertEqual(
                receipt.resulting_state, LifecycleState.RECONCILIATION_REQUIRED
            )
            with self.assertRaisesRegex(DispatchDenied, "source head or cursor"):
                dispatch.pause_reconciliation(
                    stale_request,
                    authority.claim_operator(*stale_grant.__dict__.values()),
                )
            replay = dispatch.pause_reconciliation(request, capability)
            self.assertTrue(replay.replayed)
            connection = sqlite3.connect(store._database_path)
            try:
                after = connection.execute(
                    "SELECT (SELECT COUNT(*) FROM dispatch_fences), "
                    "(SELECT COUNT(*) FROM outstanding_slot), "
                    "(SELECT continuation_cursor FROM runs WHERE run_id = "
                    "'run-1'), (SELECT disposition || ':' || charged_units || "
                    "':' || uncertainty FROM budget_reservations WHERE "
                    "reservation_id = 'reservation-t09'), "
                    "(SELECT COUNT(*) FROM reconciliation_pause_actions), "
                    "(SELECT lifecycle_state FROM runs WHERE run_id = 'run-1')"
                ).fetchone()
            finally:
                connection.close()
            self.assertEqual(after[:4], (before[0] + 1, *before[1:]))
            self.assertEqual(after[4:], (1, "RECONCILIATION_REQUIRED"))
            self.assertEqual(
                adapter.reconcile(effect_capability.claim_id), target_before,
                "T09 must not observe, cancel, retry or mutate the adapter",
            )
            stacked_grant = SyntheticOperatorGrant(
                "pause-grant-t09-stacked", "repo-1", "run-1", "PAUSE",
                "pause-scope-t09-stacked",
            )
            authority.register_operator(stacked_grant)
            stacked = self._t09_pause_request(store, suffix="stacked")
            dispatch.pause_reconciliation(
                stacked,
                authority.claim_operator(*stacked_grant.__dict__.values()),
            )
            connection = sqlite3.connect(store._database_path)
            try:
                counts = connection.execute(
                    "SELECT (SELECT COUNT(*) FROM reconciliation_pause_actions), "
                    "(SELECT COUNT(*) FROM dispatch_fences), "
                    "(SELECT COUNT(*) FROM outstanding_slot)"
                ).fetchone()
            finally:
                connection.close()
            self.assertEqual(counts, (2, before[0] + 2, 1))
            store.load_verified("repo-1", authority=authority)

    def test_t09_validator_reconciliation_retains_checkpoint_and_uncertainty(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (
                authority, store, dispatch, validator_adapter,
                _validator_intent, _validator_capability, _committed,
            ) = self._prepare_t08_active_validator(root, contact=True)
            t08_grant = SyntheticOperatorGrant(
                "pause-grant-t09-t08", "repo-1", "run-1", "PAUSE",
                "pause-scope-t09-t08",
            )
            authority.register_operator(t08_grant)
            dispatch.pause_validation(
                self._t08_pause_request(store, suffix="for-t09"),
                authority.claim_operator(*t08_grant.__dict__.values()),
            )
            connection = sqlite3.connect(store._database_path)
            try:
                before = connection.execute(
                    "SELECT (SELECT COUNT(*) FROM adapter_contacts WHERE "
                    "contact_kind = 'VALIDATOR'), "
                    "(SELECT COUNT(*) FROM validator_observations), "
                    "(SELECT COUNT(*) FROM dispatch_fences), "
                    "(SELECT COUNT(*) FROM outstanding_slot), "
                    "(SELECT disposition || ':' || charged_units || ':' || "
                    "uncertainty FROM budget_reservations WHERE "
                    "reservation_id = 'validator-reservation-t08'), "
                    "(SELECT continuation_cursor FROM runs WHERE run_id = "
                    "'run-1')"
                ).fetchone()
            finally:
                connection.close()
            t09_grant = SyntheticOperatorGrant(
                "pause-grant-t09-validator", "repo-1", "run-1", "PAUSE",
                "pause-scope-t09-validator",
            )
            authority.register_operator(t09_grant)
            request = self._t09_pause_request(store, suffix="validator")
            with patch.object(
                validator_adapter, "reconcile", wraps=validator_adapter.reconcile
            ) as reconcile_spy:
                receipt = dispatch.pause_reconciliation(
                    request,
                    authority.claim_operator(*t09_grant.__dict__.values()),
                )
                reconcile_spy.assert_not_called()
            self.assertEqual(
                receipt.resulting_state, LifecycleState.RECONCILIATION_REQUIRED
            )
            connection = sqlite3.connect(store._database_path)
            try:
                after = connection.execute(
                    "SELECT (SELECT COUNT(*) FROM adapter_contacts WHERE "
                    "contact_kind = 'VALIDATOR'), "
                    "(SELECT COUNT(*) FROM validator_observations), "
                    "(SELECT COUNT(*) FROM dispatch_fences), "
                    "(SELECT COUNT(*) FROM outstanding_slot), "
                    "(SELECT disposition || ':' || charged_units || ':' || "
                    "uncertainty FROM budget_reservations WHERE "
                    "reservation_id = 'validator-reservation-t08'), "
                    "(SELECT continuation_cursor FROM runs WHERE run_id = "
                    "'run-1'), (SELECT lifecycle_state FROM runs WHERE "
                    "run_id = 'run-1')"
                ).fetchone()
            finally:
                connection.close()
            self.assertEqual(after[:2], before[:2])
            self.assertEqual(after[2], before[2] + 1)
            self.assertEqual(after[3:6], before[3:6])
            self.assertEqual(after[6], "RECONCILIATION_REQUIRED")
            store.load_verified("repo-1", authority=authority)

    def test_t09_action_history_does_not_block_future_exact_fence_clearance(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            authority, store, dispatch, _adapter, _capability = (
                self._prepare_t09_operation_reconciliation(root)
            )
            request = self._t09_pause_request(store, suffix="future-clearance")
            pause_grant = SyntheticOperatorGrant(
                "pause-grant-t09-future-clearance", "repo-1", "run-1",
                "PAUSE", "pause-scope-t09-future-clearance",
            )
            authority.register_operator(pause_grant)
            dispatch.pause_reconciliation(
                request,
                authority.claim_operator(*pause_grant.__dict__.values()),
            )
            connection = sqlite3.connect(store._database_path)
            connection.execute("PRAGMA foreign_keys = ON")
            try:
                foreign_targets = {
                    row[2]
                    for row in connection.execute(
                        "PRAGMA foreign_key_list(reconciliation_pause_actions)"
                    )
                }
                self.assertNotIn("dispatch_fences", foreign_targets)
                connection.execute("BEGIN IMMEDIATE")
                deleted = connection.execute(
                    "DELETE FROM dispatch_fences WHERE fence_id = ?",
                    (request.fence_id,),
                ).rowcount
                retained = connection.execute(
                    "SELECT COUNT(*) FROM reconciliation_pause_actions WHERE "
                    "pause_id = ?",
                    (request.pause_id,),
                ).fetchone()[0]
                self.assertEqual((deleted, retained), (1, 1))
                connection.rollback()
            finally:
                connection.close()
            store.load_verified("repo-1", authority=authority)

    def test_t09_reconciliation_pause_crash_boundaries_are_atomic_and_replayable(
        self,
    ) -> None:
        for hook_name in (
            "after_reconciliation_pause_event_before_fence",
            "after_reconciliation_pause_writes_before_commit",
        ):
            with self.subTest(hook=hook_name), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                authority, store, dispatch, _adapter, _capability = (
                    self._prepare_t09_operation_reconciliation(root)
                )
                request = self._t09_pause_request(store, suffix=hook_name)
                pause_grant = SyntheticOperatorGrant(
                    f"pause-grant-{hook_name}", "repo-1", "run-1", "PAUSE",
                    f"pause-scope-{hook_name}",
                )
                authority.register_operator(pause_grant)
                capability = authority.claim_operator(*pause_grant.__dict__.values())
                connection = sqlite3.connect(store._database_path)
                try:
                    before = connection.execute(
                        "SELECT head_hash FROM runs WHERE run_id = 'run-1'"
                    ).fetchone()[0]
                finally:
                    connection.close()
                with self.assertRaises(InjectedFailure):
                    dispatch.pause_reconciliation(
                        request, capability, failure_hook=raise_at(hook_name)
                    )
                connection = sqlite3.connect(store._database_path)
                try:
                    counts = connection.execute(
                        "SELECT (SELECT COUNT(*) FROM "
                        "reconciliation_pause_actions), (SELECT COUNT(*) FROM "
                        "dispatch_fences WHERE fence_id = ?), (SELECT head_hash "
                        "FROM runs WHERE run_id = 'run-1')",
                        (request.fence_id,),
                    ).fetchone()
                finally:
                    connection.close()
                self.assertEqual(counts, (0, 0, before))
                recovered = dispatch.pause_reconciliation(request, capability)
                self.assertFalse(recovered.replayed)
                store.load_verified("repo-1", authority=authority)

        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            authority, store, dispatch, _adapter, _capability = (
                self._prepare_t09_operation_reconciliation(root)
            )
            request = self._t09_pause_request(store, suffix="post-commit")
            pause_grant = SyntheticOperatorGrant(
                "pause-grant-t09-post-commit", "repo-1", "run-1", "PAUSE",
                "pause-scope-t09-post-commit",
            )
            authority.register_operator(pause_grant)
            capability = authority.claim_operator(*pause_grant.__dict__.values())
            with self.assertRaises(InjectedFailure):
                dispatch.pause_reconciliation(
                    request, capability,
                    failure_hook=raise_at(
                        "after_reconciliation_pause_commit_before_acknowledgement"
                    ),
                )
            replay = dispatch.pause_reconciliation(request, capability)
            self.assertTrue(replay.replayed)
            store.load_verified("repo-1", authority=authority)

    def test_t09_recovery_rejects_capability_projection_and_event_schema_tamper(
        self,
    ) -> None:
        tampered_values = {
            "capability_claim_id": "tampered-claim",
            "capability_grant_id": "tampered-grant",
            "capability_repository_id": "tampered-repository",
            "capability_run_id": "tampered-run",
            "capability_action": "tampered-action",
            "capability_scope_digest": "tampered-scope",
            "capability_issuer_mac": "tampered-mac",
            "capability_issuer_fingerprint": "tampered-fingerprint",
        }
        for column, value in tampered_values.items():
            with self.subTest(column=column), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                authority, store, dispatch, _adapter, _capability = (
                    self._prepare_t09_operation_reconciliation(root)
                )
                request = self._t09_pause_request(store, suffix=f"tamper-{column}")
                pause_grant = SyntheticOperatorGrant(
                    f"pause-grant-t09-{column}", "repo-1", "run-1", "PAUSE",
                    f"pause-scope-t09-{column}",
                )
                authority.register_operator(pause_grant)
                dispatch.pause_reconciliation(
                    request,
                    authority.claim_operator(*pause_grant.__dict__.values()),
                )
                connection = sqlite3.connect(store._database_path)
                try:
                    connection.execute("PRAGMA ignore_check_constraints = ON")
                    connection.execute(
                        f"UPDATE reconciliation_pause_actions SET {column} = ?",
                        (value,),
                    )
                    connection.commit()
                finally:
                    connection.close()
                with self.assertRaisesRegex(
                    StorageIntegrityError, "reconciliation-pause projection"
                ):
                    store.load_verified("repo-1", authority=authority)

        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            authority, store, dispatch, _adapter, _capability = (
                self._prepare_t09_operation_reconciliation(root)
            )
            request = self._t09_pause_request(store, suffix="surplus")
            pause_grant = SyntheticOperatorGrant(
                "pause-grant-t09-surplus", "repo-1", "run-1", "PAUSE",
                "pause-scope-t09-surplus",
            )
            authority.register_operator(pause_grant)
            dispatch.pause_reconciliation(
                request,
                authority.claim_operator(*pause_grant.__dict__.values()),
            )
            connection = sqlite3.connect(store._database_path)
            connection.row_factory = sqlite3.Row
            try:
                row = connection.execute(
                    "SELECT body_json FROM events WHERE event_id = ?",
                    (request.event_id,),
                ).fetchone()
                body = json.loads(row["body_json"])
                body["surplus_field"] = "forbidden"
                event_hash = store._event_hash(body)
                body_json = json.dumps(body, sort_keys=True, separators=(",", ":"))
                connection.execute(
                    "UPDATE events SET event_hash = ?, body_json = ? WHERE "
                    "event_id = ?",
                    (event_hash, body_json, request.event_id),
                )
                connection.execute(
                    "UPDATE reconciliation_pause_actions SET event_hash = ?, "
                    "body_json = ? WHERE pause_id = ?",
                    (event_hash, body_json, request.pause_id),
                )
                connection.execute(
                    "UPDATE command_outcomes SET event_hash = ? WHERE "
                    "command_id = ?",
                    (event_hash, request.command_id),
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
            with self.assertRaisesRegex(
                StorageIntegrityError, "reconciliation"
            ):
                store.load_verified("repo-1", authority=authority)

    def test_t09_recovery_rejects_self_consistent_source_retarget(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            authority, store, dispatch, _adapter, _capability = (
                self._prepare_t09_operation_reconciliation(root)
            )
            request = self._t09_pause_request(store, suffix="source-retarget")
            pause_grant = SyntheticOperatorGrant(
                "pause-grant-t09-source-retarget", "repo-1", "run-1",
                "PAUSE", "pause-scope-t09-source-retarget",
            )
            authority.register_operator(pause_grant)
            dispatch.pause_reconciliation(
                request,
                authority.claim_operator(*pause_grant.__dict__.values()),
            )
            connection = sqlite3.connect(store._database_path)
            connection.row_factory = sqlite3.Row
            try:
                earlier = connection.execute(
                    "SELECT event_id, event_hash FROM events WHERE run_id = "
                    "'run-1' AND event_kind = 'PLAN_ACCEPTED'"
                ).fetchone()
                row = connection.execute(
                    "SELECT body_json FROM events WHERE event_id = ?",
                    (request.event_id,),
                ).fetchone()
                body = json.loads(row["body_json"])
                retargeted = replace(
                    request,
                    source_event_id=str(earlier["event_id"]),
                    source_event_hash=str(earlier["event_hash"]),
                )
                retargeted.validate()
                payload = {
                    **retargeted.__dict__,
                    "pause_kind": "RECONCILIATION",
                    "pause_binding_version": 1,
                    "capability_evidence": body["capability_evidence"],
                    "capability_issuer_fingerprint": body[
                        "capability_issuer_fingerprint"
                    ],
                }
                payload_digest = store._event_hash(payload)
                body["source_event_id"] = retargeted.source_event_id
                body["source_event_hash"] = retargeted.source_event_hash
                body["payload_digest"] = payload_digest
                event_hash = store._event_hash(body)
                body_json = json.dumps(body, sort_keys=True, separators=(",", ":"))
                connection.execute(
                    "UPDATE events SET event_hash = ?, body_json = ? WHERE "
                    "event_id = ?",
                    (event_hash, body_json, request.event_id),
                )
                connection.execute(
                    "UPDATE reconciliation_pause_actions SET source_event_id = ?, "
                    "source_event_hash = ?, payload_digest = ?, event_hash = ?, "
                    "body_json = ? WHERE pause_id = ?",
                    (
                        retargeted.source_event_id,
                        retargeted.source_event_hash,
                        payload_digest,
                        event_hash,
                        body_json,
                        request.pause_id,
                    ),
                )
                connection.execute(
                    "UPDATE command_outcomes SET payload_digest = ?, "
                    "event_hash = ? WHERE command_id = ?",
                    (payload_digest, event_hash, request.command_id),
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
            with self.assertRaisesRegex(
                StorageIntegrityError, "reconciliation pause proof"
            ):
                store.load_verified("repo-1", authority=authority)

    def test_t09_competing_pause_commands_serialize_on_the_exact_source_head(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            authority, store, dispatch, _adapter, _capability = (
                self._prepare_t09_operation_reconciliation(root)
            )
            first = self._t09_pause_request(store, suffix="race-first")
            second = replace(
                first,
                pause_id="reconciliation-pause-race-second",
                command_id="reconciliation-pause-command-race-second",
                event_id="reconciliation-pause-event-race-second",
                fence_id="reconciliation-pause-fence-race-second",
            )
            grants = (
                SyntheticOperatorGrant(
                    "pause-grant-t09-race-first", "repo-1", "run-1", "PAUSE",
                    "pause-scope-t09-race-first",
                ),
                SyntheticOperatorGrant(
                    "pause-grant-t09-race-second", "repo-1", "run-1", "PAUSE",
                    "pause-scope-t09-race-second",
                ),
            )
            for grant in grants:
                authority.register_operator(grant)
            capabilities = tuple(
                authority.claim_operator(*grant.__dict__.values())
                for grant in grants
            )
            barrier = threading.Barrier(2)

            def pause(request, capability):
                barrier.wait()
                return dispatch.pause_reconciliation(request, capability)

            results = []
            errors = []
            with ThreadPoolExecutor(max_workers=2) as executor:
                futures = (
                    executor.submit(pause, first, capabilities[0]),
                    executor.submit(pause, second, capabilities[1]),
                )
                for future in futures:
                    try:
                        results.append(future.result())
                    except BaseException as error:
                        errors.append(error)
            self.assertEqual(len(results), 1, repr(errors))
            self.assertEqual(len(errors), 1, repr(errors))
            self.assertIsInstance(errors[0], DispatchDenied)
            connection = sqlite3.connect(store._database_path)
            try:
                counts = connection.execute(
                    "SELECT (SELECT COUNT(*) FROM reconciliation_pause_actions), "
                    "(SELECT COUNT(*) FROM dispatch_fences WHERE reason_code = "
                    "'OPERATOR_PAUSE_RECONCILIATION'), "
                    "(SELECT COUNT(*) FROM outstanding_slot)"
                ).fetchone()
            finally:
                connection.close()
            self.assertEqual(counts, (1, 1, 1))
            store.load_verified("repo-1", authority=authority)

    def test_t08_validation_pause_contract_and_coordinator_route(self) -> None:
        request = PauseValidationRequest(
            pause_id="validation-pause-1",
            command_id="validation-pause-command-1",
            request_event_id="validation-pause-request-event-1",
            checkpoint_event_id="validation-pause-checkpoint-event-1",
            fence_id="validation-pause-fence-1",
            repository_id="repo-1",
            run_id="run-1",
            item_id="item-1",
            logical_effect_id="effect-1",
            plan_id="plan-1",
            revision_digest="revision-1",
            reason_code="OPERATOR_PAUSE_VALIDATION",
            expected_preserved_continuation_cursor="validation:plan-1",
            expected_checkpoint_kind="IDLE",
            expected_slot_attempt_id=None,
            expected_slot_generation=None,
            validator_intent_id=None,
            validator_intent_event_id=None,
            validator_intent_event_hash=None,
            validator_attempt_id=None,
            check_id=None,
            reservation_id=None,
            expected_settlement_head_hash=None,
            contact_id=None,
            contact_event_id=None,
            contact_event_hash=None,
            contact_target_digest=None,
            observation_id=None,
            observation_event_id=None,
            observation_event_hash=None,
            observation_settlement_event_id=None,
            observation_settlement_event_hash=None,
        )
        request.validate()
        self.assertTrue(
            hasattr(SyntheticDispatchCoordinator, "pause_validation"),
            "T08 requires a coordinator-owned validation pause route",
        )
        with self.assertRaisesRegex(ValueError, "active validator tuple"):
            replace(request, expected_slot_attempt_id="validator-attempt-1").validate()

    def test_t08_idle_validation_pauses_without_adapter_contact_and_recovers(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            authority = SyntheticAuthority()
            effect_grant = SyntheticGrant(
                "grant-t08", "repo-1", "effect-1", "attempt-1", "scope-1"
            )
            authority.register(effect_grant)
            effect_capability = authority.claim(*effect_grant.__dict__.values())
            with self.state_root_context(root):
                store = SQLiteStateStore.open_canonical(
                    "repo-1", AlwaysFreshOracle()
                )
                adapter = SyntheticExecutionAdapter.open_canonical("repo-1")
            coordinator = SyntheticDispatchCoordinator(
                store, TransitionEngine(), authority, adapter
            )
            intent = IntentRequest(
                "repo-1", "run-1", "item-1", "command-t08", "event-t08",
                "effect-1", "payload-1", "attempt-1", "permission-t08",
                "reservation-t08", "budget-1", 1, 1, 10,
            )
            plan = self._accept_operation_plan(store, intent)
            coordinator.dispatch(
                intent,
                effect_capability,
                SyntheticEffectRequest(
                    "repo-1", "effect-1", "attempt-1", "scope-1", "payload-1"
                ),
                expected_head=plan.event_hash,
                writer_epoch=2,
                usage_units=1,
            )
            coordinator.intake_effect_receipt(
                EffectObservationCommand(
                    "observation-t08", "observe-command-t08",
                    "observation-event-t08", "repo-1", "run-1", "item-1",
                    "effect-1", "attempt-1", effect_capability.claim_id,
                    "settlement-t08", "",
                )
            )
            pause_grant = SyntheticOperatorGrant(
                "pause-grant-t08", "repo-1", "run-1", "PAUSE",
                "pause-scope-t08",
            )
            authority.register_operator(pause_grant)
            request = PauseValidationRequest(
                pause_id="validation-pause-t08",
                command_id="validation-pause-command-t08",
                request_event_id="validation-pause-request-t08",
                checkpoint_event_id="validation-pause-checkpoint-t08",
                fence_id="validation-pause-fence-t08",
                repository_id="repo-1",
                run_id="run-1",
                item_id="item-1",
                logical_effect_id="effect-1",
                plan_id="plan:run-1",
                revision_digest="revision-1",
                reason_code="OPERATOR_PAUSE_VALIDATION",
                expected_preserved_continuation_cursor=None,
                expected_checkpoint_kind="IDLE",
                expected_slot_attempt_id=None,
                expected_slot_generation=None,
                validator_intent_id=None,
                validator_intent_event_id=None,
                validator_intent_event_hash=None,
                validator_attempt_id=None,
                check_id=None,
                reservation_id=None,
                expected_settlement_head_hash=None,
                contact_id=None,
                contact_event_id=None,
                contact_event_hash=None,
                contact_target_digest=None,
                observation_id=None,
                observation_event_id=None,
                observation_event_hash=None,
                observation_settlement_event_id=None,
                observation_settlement_event_hash=None,
            )
            receipt = coordinator.pause_validation(
                request,
                authority.claim_operator(*pause_grant.__dict__.values()),
            )
            self.assertEqual(receipt.resulting_state, LifecycleState.PAUSED)
            self.assertEqual(store.load_run_lifecycle("run-1"), LifecycleState.PAUSED)
            self.assertIsNotNone(adapter.reconcile(effect_capability.claim_id))
            catalog_head, run_heads = store.load_verified(
                "repo-1", authority=authority
            )
            resume_grant = SyntheticOperatorGrant(
                "resume-grant-t08", "repo-1", "run-1", "RESUME",
                "resume-scope-t08",
            )
            authority.register_operator(resume_grant)
            resume_request = ResumeRequest(
                "resume-t08", "resume-command-t08", "resume-event-t08",
                "repo-1", "run-1", "item-1", "effect-1", "plan:run-1",
                "revision-1", request.pause_id, request.checkpoint_event_id,
                receipt.event_hash, request.fence_id,
                LifecycleState.VALIDATING, None, catalog_head,
                run_heads["run-1"], store._run_heads_digest(run_heads),
            )
            resumed = coordinator.resume(
                resume_request,
                authority.claim_operator(*resume_grant.__dict__.values()),
                authority.issue_resume_evidence(
                    "resume-proof-t08", resume_request
                ),
            )
            self.assertEqual(resumed.resulting_state, LifecycleState.VALIDATING)
            self.assertEqual(
                store.load_run_lifecycle("run-1"), LifecycleState.VALIDATING
            )

    def test_t08_uncontacted_validator_is_fenced_without_budget_charge(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (
                authority, store, dispatch, validator_adapter,
                validator_intent, validator_capability, committed,
            ) = self._prepare_t08_active_validator(root, contact=False)
            request = self._t08_pause_request(store, suffix="uncontacted")
            self.assertEqual(
                request.expected_checkpoint_kind, "UNCONTACTED_UNRESOLVED"
            )
            pause_grant = SyntheticOperatorGrant(
                "pause-grant-uncontacted", "repo-1", "run-1", "PAUSE",
                "pause-scope-uncontacted",
            )
            authority.register_operator(pause_grant)
            receipt = dispatch.pause_validation(
                request,
                authority.claim_operator(*pause_grant.__dict__.values()),
            )
            self.assertEqual(
                receipt.resulting_state, LifecycleState.RECONCILIATION_REQUIRED
            )
            connection = sqlite3.connect(store._database_path)
            try:
                accounting = connection.execute(
                    "SELECT disposition, held_units, charged_units, uncertainty "
                    "FROM budget_reservations WHERE reservation_id = "
                    "'validator-reservation-t08'"
                ).fetchone()
                contacts = connection.execute(
                    "SELECT COUNT(*) FROM adapter_contacts WHERE contact_kind = "
                    "'VALIDATOR'"
                ).fetchone()[0]
            finally:
                connection.close()
            self.assertEqual(accounting, ("RESERVED", 1, 0, 0))
            self.assertEqual(contacts, 0)
            self.assertIsNone(
                validator_adapter.reconcile(validator_capability.claim_id)
            )
            with self.assertRaisesRegex(DispatchDenied, "VALIDATING state"):
                store._contact_committed_validator(
                    validator_intent, validator_capability, committed,
                    validator_adapter._target_digest("repo-1"), authority,
                )
            store.load_verified("repo-1", authority=authority)

    def test_t08_contacted_validator_is_atomically_worst_case_charged(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (
                authority, store, dispatch, validator_adapter,
                _validator_intent, validator_capability, _committed,
            ) = self._prepare_t08_active_validator(root, contact=True)
            request = self._t08_pause_request(store, suffix="contacted")
            self.assertEqual(
                request.expected_checkpoint_kind, "CONTACTED_UNRESOLVED"
            )
            pause_grant = SyntheticOperatorGrant(
                "pause-grant-contacted", "repo-1", "run-1", "PAUSE",
                "pause-scope-contacted",
            )
            authority.register_operator(pause_grant)
            receipt = dispatch.pause_validation(
                request,
                authority.claim_operator(*pause_grant.__dict__.values()),
            )
            self.assertEqual(
                receipt.resulting_state, LifecycleState.RECONCILIATION_REQUIRED
            )
            connection = sqlite3.connect(store._database_path)
            try:
                accounting = connection.execute(
                    "SELECT disposition, held_units, charged_units, uncertainty "
                    "FROM budget_reservations WHERE reservation_id = "
                    "'validator-reservation-t08'"
                ).fetchone()
                projection = connection.execute(
                    "SELECT unknown_settlement_event_id, "
                    "unknown_settlement_hash FROM validation_pause_actions"
                ).fetchone()
                fence_count = connection.execute(
                    "SELECT COUNT(*) FROM dispatch_fences WHERE fence_id = ?",
                    (request.fence_id,),
                ).fetchone()[0]
            finally:
                connection.close()
            self.assertEqual(
                accounting, ("UNKNOWN_WORST_CASE_CHARGED", 0, 2, 1)
            )
            self.assertTrue(projection[0].startswith("validation-pause-unknown:"))
            self.assertTrue(projection[1])
            self.assertEqual(fence_count, 1)
            self.assertIsNone(
                validator_adapter.reconcile(validator_capability.claim_id)
            )
            store.load_verified("repo-1", authority=authority)

    def test_t08_settled_result_pauses_resumes_and_applies_without_rerun(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (
                authority, store, dispatch, validator_adapter,
                _validator_intent, validator_capability, _committed,
            ) = self._prepare_t08_active_validator(
                root, contact=True, result=True, cessation=True
            )
            connection = sqlite3.connect(store._database_path)
            try:
                observation = connection.execute(
                    "SELECT observation_id, event_hash, settlement_event_id, "
                    "settlement_hash FROM validator_observations WHERE "
                    "observation_id = 'validator-observation-t08'"
                ).fetchone()
                uncertainty_ids = tuple(
                    row[0]
                    for row in connection.execute(
                        "SELECT uncertainty_id FROM uncertainty_instances "
                        "WHERE origin_event_id = 'validator-observe-event-t08'"
                    )
                )
                cessation = connection.execute(
                    "SELECT cessation_id, event_id, event_hash FROM "
                    "validator_cessations WHERE cessation_id = 'cessation-t08'"
                ).fetchone()
            finally:
                connection.close()
            validation = SyntheticValidationCoordinator(
                store, TransitionEngine(), authority, validator_adapter
            )
            reconciled = validation.reconcile_result(
                ReconcileValidatorResultRequest(
                    "reconcile-settled-result", "reconcile-command-settled-result",
                    "reconcile-event-settled-result", "repo-1", "run-1",
                    "item-1", "effect-1", "plan:run-1", "revision-1",
                    observation[0], observation[1], cessation[0], cessation[1],
                    cessation[2], observation[2], observation[3],
                    uncertainty_ids, "attempt-1", 1, cessation[2], None,
                )
            )
            self.assertEqual(reconciled.resulting_state, LifecycleState.VALIDATING)
            request = self._t08_pause_request(store, suffix="settled-result")
            self.assertEqual(
                request.expected_checkpoint_kind, "ELIGIBLE_RESULT_SETTLED"
            )
            result_before = validator_adapter.reconcile(
                validator_capability.claim_id
            )
            pause_grant = SyntheticOperatorGrant(
                "pause-grant-settled-result", "repo-1", "run-1", "PAUSE",
                "pause-scope-settled-result",
            )
            authority.register_operator(pause_grant)
            paused = dispatch.pause_validation(
                request,
                authority.claim_operator(*pause_grant.__dict__.values()),
            )
            self.assertEqual(paused.resulting_state, LifecycleState.PAUSED)
            catalog_head, run_heads = store.load_verified(
                "repo-1", authority=authority
            )
            resume_grant = SyntheticOperatorGrant(
                "resume-grant-settled-result", "repo-1", "run-1", "RESUME",
                "resume-scope-settled-result",
            )
            authority.register_operator(resume_grant)
            resume_request = ResumeRequest(
                "resume-settled-result", "resume-command-settled-result",
                "resume-event-settled-result", "repo-1", "run-1", "item-1",
                "effect-1", "plan:run-1", "revision-1", request.pause_id,
                request.checkpoint_event_id, paused.event_hash,
                request.fence_id, LifecycleState.VALIDATING,
                "validation-application:v1:validator-observation-t08:"
                "check-1:validator-attempt-1",
                catalog_head, run_heads["run-1"],
                store._run_heads_digest(run_heads),
            )
            resumed = dispatch.resume(
                resume_request,
                authority.claim_operator(*resume_grant.__dict__.values()),
                authority.issue_resume_evidence(
                    "resume-proof-settled-result", resume_request
                ),
            )
            self.assertEqual(resumed.resulting_state, LifecycleState.VALIDATING)
            applied = validation.apply_result(
                ValidationApplicationRequest(
                    "application-settled-result", "apply-command-settled-result",
                    "apply-event-settled-result", "repo-1", "run-1", "item-1",
                    "effect-1", "revision-1", "check-1",
                    "validator-attempt-1", "validator-observation-t08",
                )
            )
            self.assertEqual(applied.resulting_state, LifecycleState.BLOCKED)
            self.assertEqual(
                validator_adapter.reconcile(validator_capability.claim_id),
                result_before,
            )
            store.load_verified("repo-1", authority=authority)

    def test_t08_result_without_authoritative_cessation_stays_in_reconciliation(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (
                authority, store, dispatch, _validator_adapter,
                _validator_intent, _validator_capability, _committed,
            ) = self._prepare_t08_active_validator(
                root, contact=True, result=True, cessation=False
            )
            request = self._t08_pause_request(
                store, suffix="result-without-cessation"
            )
            self.assertEqual(
                request.expected_checkpoint_kind, "CONTACTED_UNRESOLVED"
            )
            pause_grant = SyntheticOperatorGrant(
                "pause-grant-result-without-cessation", "repo-1", "run-1",
                "PAUSE", "pause-scope-result-without-cessation",
            )
            authority.register_operator(pause_grant)
            with self.assertRaises(DispatchDenied):
                dispatch.pause_validation(
                    request,
                    authority.claim_operator(*pause_grant.__dict__.values()),
                )
            connection = sqlite3.connect(store._database_path)
            try:
                accounting = connection.execute(
                    "SELECT disposition, charged_units, uncertainty FROM "
                    "budget_reservations WHERE reservation_id = "
                    "'validator-reservation-t08'"
                ).fetchone()
                observations = connection.execute(
                    "SELECT COUNT(*) FROM validator_observations WHERE "
                    "observation_id = 'validator-observation-t08'"
                ).fetchone()[0]
                lifecycle = connection.execute(
                    "SELECT lifecycle_state FROM runs WHERE run_id = 'run-1'"
                ).fetchone()[0]
                activity_fences = connection.execute(
                    "SELECT COUNT(*) FROM dispatch_fences WHERE reason_code = "
                    "'VALIDATOR_ACTIVITY_UNKNOWN'"
                ).fetchone()[0]
            finally:
                connection.close()
            self.assertEqual(accounting, ("CONSUMED", 1, 0))
            self.assertEqual(observations, 1)
            self.assertEqual((lifecycle, activity_fences), ("RECONCILIATION_REQUIRED", 1))
            store.load_verified("repo-1", authority=authority)

    def test_t08_existing_validator_accounting_is_never_downgraded_or_recharged(
        self,
    ) -> None:
        cases = (
            (BudgetDisposition.UNKNOWN_WORST_CASE_CHARGED, None, 2, 1),
            (BudgetDisposition.CONSUMED, 1, 1, 0),
        )
        for disposition, actual_units, charged_units, uncertainty in cases:
            with self.subTest(disposition=disposition.value), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                (
                    authority, store, dispatch, _validator_adapter,
                    _validator_intent, _validator_capability, _committed,
                ) = self._prepare_t08_active_validator(root, contact=True)
                settlement_request = BudgetSettlementRequest(
                    f"pre-pause-settlement-{disposition.value}",
                    "validator-reservation-t08", "", disposition,
                    actual_units, f"evidence-{disposition.value}",
                    f"PRE_PAUSE_{disposition.value}",
                    attempt_id="validator-attempt-1",
                )
                store._settle_budget(
                    settlement_request,
                    authority.issue_settlement_proof(
                        f"proof-{disposition.value}", settlement_request
                    ),
                    authority,
                )
                request = self._t08_pause_request(
                    store, suffix=disposition.value.lower()
                )
                pause_grant = SyntheticOperatorGrant(
                    f"pause-grant-{disposition.value}", "repo-1", "run-1",
                    "PAUSE", f"pause-scope-{disposition.value}",
                )
                authority.register_operator(pause_grant)
                dispatch.pause_validation(
                    request,
                    authority.claim_operator(*pause_grant.__dict__.values()),
                )
                connection = sqlite3.connect(store._database_path)
                try:
                    accounting = connection.execute(
                        "SELECT disposition, charged_units, uncertainty FROM "
                        "budget_reservations WHERE reservation_id = "
                        "'validator-reservation-t08'"
                    ).fetchone()
                    settlement_count = connection.execute(
                        "SELECT COUNT(*) FROM budget_settlements WHERE "
                        "reservation_id = 'validator-reservation-t08'"
                    ).fetchone()[0]
                    synthetic_settlement = connection.execute(
                        "SELECT unknown_settlement_event_id FROM "
                        "validation_pause_actions"
                    ).fetchone()[0]
                finally:
                    connection.close()
                self.assertEqual(
                    accounting,
                    (disposition.value, charged_units, uncertainty),
                )
                self.assertEqual(settlement_count, 1)
                self.assertIsNone(synthetic_settlement)
                store.load_verified("repo-1", authority=authority)

    def test_t08_validation_pause_crash_boundaries_are_atomic_and_replayable(
        self,
    ) -> None:
        rollback_points = (
            "after_validation_pause_unknown_settlement_before_request",
            "after_validation_pause_request_before_checkpoint",
            "after_validation_pause_writes_before_commit",
        )
        for point in rollback_points:
            with self.subTest(point=point), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                (
                    authority, store, dispatch, _validator_adapter,
                    _validator_intent, _validator_capability, _committed,
                ) = self._prepare_t08_active_validator(root, contact=True)
                request = self._t08_pause_request(store, suffix=point)
                pause_grant = SyntheticOperatorGrant(
                    f"pause-grant-{point}", "repo-1", "run-1", "PAUSE",
                    f"pause-scope-{point}",
                )
                authority.register_operator(pause_grant)
                capability = authority.claim_operator(
                    *pause_grant.__dict__.values()
                )
                with self.assertRaises(InjectedFailure):
                    dispatch.pause_validation(
                        request, capability, failure_hook=raise_at(point)
                    )
                connection = sqlite3.connect(store._database_path)
                try:
                    counts = connection.execute(
                        "SELECT (SELECT COUNT(*) FROM validation_pause_actions), "
                        "(SELECT COUNT(*) FROM events WHERE event_kind IN "
                        "('VALIDATION_PAUSE_REQUESTED', "
                        "'VALIDATION_PAUSE_CHECKPOINTED')), "
                        "(SELECT COUNT(*) FROM budget_settlements WHERE "
                        "settlement_event_id LIKE 'validation-pause-unknown:%')"
                    ).fetchone()
                    accounting = connection.execute(
                        "SELECT disposition FROM budget_reservations WHERE "
                        "reservation_id = 'validator-reservation-t08'"
                    ).fetchone()[0]
                finally:
                    connection.close()
                self.assertEqual(counts, (0, 0, 0))
                self.assertEqual(accounting, "RESERVED")
                recovered = dispatch.pause_validation(request, capability)
                self.assertFalse(recovered.replayed)
                store.load_verified("repo-1", authority=authority)

        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (
                authority, store, dispatch, _validator_adapter,
                _validator_intent, _validator_capability, _committed,
            ) = self._prepare_t08_active_validator(root, contact=True)
            request = self._t08_pause_request(store, suffix="post-commit")
            pause_grant = SyntheticOperatorGrant(
                "pause-grant-post-commit", "repo-1", "run-1", "PAUSE",
                "pause-scope-post-commit",
            )
            authority.register_operator(pause_grant)
            capability = authority.claim_operator(*pause_grant.__dict__.values())
            with self.assertRaises(InjectedFailure):
                dispatch.pause_validation(
                    request, capability,
                    failure_hook=raise_at(
                        "after_validation_pause_commit_before_acknowledgement"
                    ),
                )
            replay = dispatch.pause_validation(request, capability)
            self.assertTrue(replay.replayed)
            store.load_verified("repo-1", authority=authority)

    def test_t08_recovery_rejects_every_persisted_operator_capability_tamper(
        self,
    ) -> None:
        tampered_values = {
            "capability_claim_id": "tampered-claim",
            "capability_grant_id": "tampered-grant",
            "capability_repository_id": "tampered-repository",
            "capability_run_id": "tampered-run",
            "capability_action": "tampered-action",
            "capability_scope_digest": "tampered-scope",
            "capability_issuer_mac": "tampered-mac",
            "capability_issuer_fingerprint": "tampered-fingerprint",
        }
        for column, value in tampered_values.items():
            with self.subTest(column=column), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                (
                    authority, store, dispatch, _validator_adapter,
                    _validator_intent, _validator_capability, _committed,
                ) = self._prepare_t08_active_validator(root, contact=False)
                request = self._t08_pause_request(store, suffix=f"tamper-{column}")
                pause_grant = SyntheticOperatorGrant(
                    f"pause-grant-{column}", "repo-1", "run-1", "PAUSE",
                    f"pause-scope-{column}",
                )
                authority.register_operator(pause_grant)
                dispatch.pause_validation(
                    request,
                    authority.claim_operator(*pause_grant.__dict__.values()),
                )
                connection = sqlite3.connect(store._database_path)
                try:
                    connection.execute("PRAGMA ignore_check_constraints = ON")
                    connection.execute(
                        f"UPDATE validation_pause_actions SET {column} = ?",
                        (value,),
                    )
                    connection.commit()
                finally:
                    connection.close()
                with self.assertRaisesRegex(
                    StorageIntegrityError, "validation-pause projection"
                ):
                    store.load_verified("repo-1", authority=authority)

    def test_t08_recovery_rejects_self_consistent_checkpoint_surplus_field(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (
                authority, store, dispatch, _validator_adapter,
                _validator_intent, _validator_capability, _committed,
            ) = self._prepare_t08_active_validator(root, contact=False)
            request = self._t08_pause_request(store, suffix="surplus")
            pause_grant = SyntheticOperatorGrant(
                "pause-grant-surplus", "repo-1", "run-1", "PAUSE",
                "pause-scope-surplus",
            )
            authority.register_operator(pause_grant)
            dispatch.pause_validation(
                request,
                authority.claim_operator(*pause_grant.__dict__.values()),
            )
            connection = sqlite3.connect(store._database_path)
            connection.row_factory = sqlite3.Row
            try:
                row = connection.execute(
                    "SELECT body_json FROM events WHERE event_id = ?",
                    (request.checkpoint_event_id,),
                ).fetchone()
                body = json.loads(row["body_json"])
                body["surplus_field"] = "forbidden"
                event_hash = store._event_hash(body)
                body_json = json.dumps(
                    body, sort_keys=True, separators=(",", ":")
                )
                connection.execute(
                    "UPDATE events SET event_hash = ?, body_json = ? WHERE "
                    "event_id = ?",
                    (event_hash, body_json, request.checkpoint_event_id),
                )
                connection.execute(
                    "UPDATE validation_pause_actions SET "
                    "checkpoint_event_hash = ?, body_json = ? WHERE pause_id = ?",
                    (event_hash, body_json, request.pause_id),
                )
                connection.execute(
                    "UPDATE command_outcomes SET event_hash = ? WHERE "
                    "command_id = ?",
                    (event_hash, request.command_id),
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
            with self.assertRaisesRegex(
                StorageIntegrityError, "validation pause proof"
            ):
                store.load_verified("repo-1", authority=authority)

    def test_t08_recovery_rejects_self_consistent_contact_retarget(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (
                authority, store, dispatch, _validator_adapter,
                _validator_intent, _validator_capability, _committed,
            ) = self._prepare_t08_active_validator(root, contact=True)
            request = self._t08_pause_request(store, suffix="contact-retarget")
            pause_grant = SyntheticOperatorGrant(
                "pause-grant-contact-retarget", "repo-1", "run-1", "PAUSE",
                "pause-scope-contact-retarget",
            )
            authority.register_operator(pause_grant)
            dispatch.pause_validation(
                request,
                authority.claim_operator(*pause_grant.__dict__.values()),
            )
            retargeted = replace(
                request, contact_event_hash="retargeted-contact-hash"
            )
            retargeted.validate()
            connection = sqlite3.connect(store._database_path)
            connection.row_factory = sqlite3.Row
            try:
                request_row = connection.execute(
                    "SELECT body_json FROM events WHERE event_id = ?",
                    (request.request_event_id,),
                ).fetchone()
                checkpoint_row = connection.execute(
                    "SELECT body_json FROM events WHERE event_id = ?",
                    (request.checkpoint_event_id,),
                ).fetchone()
                request_body = json.loads(request_row["body_json"])
                checkpoint_body = json.loads(checkpoint_row["body_json"])
                payload = {
                    **retargeted.__dict__,
                    "pause_kind": "VALIDATION_CHECKPOINT",
                    "pause_binding_version": 1,
                    "capability_evidence": checkpoint_body[
                        "capability_evidence"
                    ],
                    "capability_issuer_fingerprint": checkpoint_body[
                        "capability_issuer_fingerprint"
                    ],
                }
                payload_digest = store._event_hash(payload)
                for key, value in retargeted.__dict__.items():
                    request_body[key] = value
                    checkpoint_body[key] = value
                request_body["payload_digest"] = payload_digest
                request_hash = store._event_hash(request_body)
                request_json = json.dumps(
                    request_body, sort_keys=True, separators=(",", ":")
                )
                checkpoint_body["payload_digest"] = payload_digest
                checkpoint_body["previous_event_hash"] = request_hash
                checkpoint_body["request_event_hash"] = request_hash
                checkpoint_body["checkpoint_snapshot"][
                    "contact_event_hash"
                ] = retargeted.contact_event_hash
                checkpoint_hash = store._event_hash(checkpoint_body)
                checkpoint_json = json.dumps(
                    checkpoint_body, sort_keys=True, separators=(",", ":")
                )
                connection.execute(
                    "UPDATE events SET event_hash = ?, body_json = ? WHERE "
                    "event_id = ?",
                    (request_hash, request_json, request.request_event_id),
                )
                connection.execute(
                    "UPDATE events SET previous_event_hash = ?, event_hash = ?, "
                    "body_json = ? WHERE event_id = ?",
                    (
                        request_hash, checkpoint_hash, checkpoint_json,
                        request.checkpoint_event_id,
                    ),
                )
                connection.execute(
                    "UPDATE validation_pause_actions SET contact_event_hash = ?, "
                    "payload_digest = ?, request_event_hash = ?, "
                    "checkpoint_event_hash = ?, body_json = ? WHERE pause_id = ?",
                    (
                        retargeted.contact_event_hash, payload_digest,
                        request_hash, checkpoint_hash, checkpoint_json,
                        request.pause_id,
                    ),
                )
                connection.execute(
                    "UPDATE command_outcomes SET payload_digest = ?, "
                    "event_hash = ? WHERE command_id = ?",
                    (payload_digest, checkpoint_hash, request.command_id),
                )
                connection.execute(
                    "UPDATE runs SET head_hash = ? WHERE run_id = 'run-1'",
                    (checkpoint_hash,),
                )
                connection.execute(
                    "UPDATE repositories SET catalog_head = ? WHERE "
                    "repository_id = 'repo-1'",
                    (checkpoint_hash,),
                )
                connection.commit()
            finally:
                connection.close()
            with self.assertRaisesRegex(
                StorageIntegrityError, "validation pause proof"
            ):
                store.load_verified("repo-1", authority=authority)

    def test_t08_pause_and_validator_contact_race_has_only_bounded_outcomes(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (
                authority, store, dispatch, validator_adapter,
                validator_intent, validator_capability, committed,
            ) = self._prepare_t08_active_validator(root, contact=False)
            request = self._t08_pause_request(store, suffix="contact-race")
            pause_grant = SyntheticOperatorGrant(
                "pause-grant-contact-race", "repo-1", "run-1", "PAUSE",
                "pause-scope-contact-race",
            )
            authority.register_operator(pause_grant)
            pause_capability = authority.claim_operator(
                *pause_grant.__dict__.values()
            )
            barrier = threading.Barrier(2)

            def pause():
                barrier.wait()
                try:
                    return dispatch.pause_validation(request, pause_capability)
                except DispatchDenied:
                    return None

            def contact():
                barrier.wait()
                try:
                    store._contact_committed_validator(
                        validator_intent, validator_capability, committed,
                        validator_adapter._target_digest("repo-1"), authority,
                    )
                    return True
                except DispatchDenied:
                    return False

            with ThreadPoolExecutor(max_workers=2) as executor:
                pause_future = executor.submit(pause)
                contact_future = executor.submit(contact)
                pause_result = pause_future.result()
                contact_result = contact_future.result()
            self.assertNotEqual(pause_result is not None, contact_result)
            if contact_result:
                request = self._t08_pause_request(
                    store, suffix="contact-race-followup"
                )
                pause_result = dispatch.pause_validation(
                    request, pause_capability
                )
            self.assertIsNotNone(pause_result)
            self.assertEqual(
                pause_result.resulting_state,
                LifecycleState.RECONCILIATION_REQUIRED,
            )
            connection = sqlite3.connect(store._database_path)
            try:
                counts = connection.execute(
                    "SELECT (SELECT COUNT(*) FROM validation_pause_actions), "
                    "(SELECT COUNT(*) FROM adapter_contacts WHERE contact_kind = "
                    "'VALIDATOR'), (SELECT COUNT(*) FROM budget_settlements "
                    "WHERE settlement_event_id LIKE "
                    "'validation-pause-unknown:%'), "
                    "(SELECT COUNT(*) FROM outstanding_slot), "
                    "(SELECT COUNT(*) FROM dispatch_fences WHERE fence_id = ?)",
                    (request.fence_id,),
                ).fetchone()
                accounting = connection.execute(
                    "SELECT disposition, charged_units, uncertainty FROM "
                    "budget_reservations WHERE reservation_id = "
                    "'validator-reservation-t08'"
                ).fetchone()
            finally:
                connection.close()
            self.assertEqual(counts[0], 1)
            self.assertEqual(counts[3:], (1, 1))
            if counts[1] == 0:
                self.assertEqual(counts[2], 0)
                self.assertEqual(accounting, ("RESERVED", 0, 0))
            else:
                self.assertEqual((counts[1], counts[2]), (1, 1))
                self.assertEqual(
                    accounting, ("UNKNOWN_WORST_CASE_CHARGED", 2, 1)
                )
            store.load_verified("repo-1", authority=authority)

    def test_t08_pause_and_result_intake_race_retains_result_in_reconciliation(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (
                authority, store, dispatch, validator_adapter,
                _validator_intent, _validator_capability, _committed,
            ) = self._prepare_t08_active_validator(
                root, contact=True, result=True, intake_result=False
            )
            request = self._t08_pause_request(store, suffix="result-race")
            self.assertEqual(
                request.expected_checkpoint_kind, "CONTACTED_UNRESOLVED"
            )
            pause_grant = SyntheticOperatorGrant(
                "pause-grant-result-race", "repo-1", "run-1", "PAUSE",
                "pause-scope-result-race",
            )
            authority.register_operator(pause_grant)
            pause_capability = authority.claim_operator(
                *pause_grant.__dict__.values()
            )
            validation = SyntheticValidationCoordinator(
                store, TransitionEngine(), authority, validator_adapter
            )
            connection = sqlite3.connect(store._database_path)
            try:
                settlement_hash = connection.execute(
                    "SELECT settlement_head_hash FROM budget_reservations WHERE "
                    "reservation_id = 'validator-reservation-t08'"
                ).fetchone()[0]
            finally:
                connection.close()
            observation_command = ValidatorObservationCommand(
                "validator-observation-t08", "validator-observe-command-t08",
                "validator-observe-event-t08", "repo-1", "run-1", "item-1",
                "validator-intent-t08", "validator-settlement-t08",
                settlement_hash,
            )
            barrier = threading.Barrier(2)

            def pause():
                barrier.wait()
                try:
                    return dispatch.pause_validation(request, pause_capability)
                except DispatchDenied:
                    return None

            def intake():
                barrier.wait()
                try:
                    return validation.intake_result(observation_command)
                except DispatchDenied:
                    return None

            with ThreadPoolExecutor(max_workers=2) as executor:
                pause_future = executor.submit(pause)
                intake_future = executor.submit(intake)
                paused = pause_future.result()
                observed = intake_future.result()
            if observed is None:
                observed = validation.intake_result(observation_command)
            if paused is not None:
                self.assertEqual(
                    paused.resulting_state,
                    LifecycleState.RECONCILIATION_REQUIRED,
                )
            self.assertIn(
                observed.resulting_state,
                {
                    LifecycleState.RECONCILIATION_REQUIRED,
                },
                "the observation receipt reflects its own commit order; the "
                "durable final state below must still be reconciliation",
            )
            connection = sqlite3.connect(store._database_path)
            try:
                counts = connection.execute(
                    "SELECT (SELECT COUNT(*) FROM validation_pause_actions), "
                    "(SELECT COUNT(*) FROM validator_observations), "
                    "(SELECT COUNT(*) FROM budget_settlements WHERE "
                    "reservation_id = 'validator-reservation-t08'), "
                    "(SELECT COUNT(*) FROM outstanding_slot), "
                    "(SELECT COUNT(*) FROM dispatch_fences WHERE fence_id = ?)",
                    (request.fence_id,),
                ).fetchone()
                accounting = connection.execute(
                    "SELECT disposition, charged_units, uncertainty FROM "
                    "budget_reservations WHERE reservation_id = "
                    "'validator-reservation-t08'"
                ).fetchone()
                activity_fence_count = connection.execute(
                    "SELECT COUNT(*) FROM dispatch_fences WHERE reason_code = "
                    "'VALIDATOR_ACTIVITY_UNKNOWN'"
                ).fetchone()[0]
            finally:
                connection.close()
            self.assertEqual(
                counts,
                (1, 1, 1, 1, 1)
                if paused is not None
                else (0, 1, 1, 1, 0),
            )
            self.assertEqual(activity_fence_count, 1)
            self.assertEqual(accounting, ("CONSUMED", 1, 0))
            store.load_verified("repo-1", authority=authority)

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
            with self.state_root_context(root):
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
                uncertainty_rows = connection.execute(
                    "SELECT uncertainty_kind, fence_id FROM "
                    "uncertainty_instances WHERE origin_event_id = "
                    "'external-pause-event-1' ORDER BY uncertainty_kind"
                ).fetchall()
            finally:
                connection.close()
            self.assertEqual(
                reservation, ("UNKNOWN_WORST_CASE_CHARGED", 0, 2, 1)
            )
            self.assertEqual(slot_count, 1)
            self.assertEqual(fence_count, 1)
            self.assertEqual(
                [row[0] for row in uncertainty_rows],
                ["ACTIVITY", "BILLING", "OUTCOME", "SOURCE_CONTROL"],
            )
            self.assertTrue(
                all(row[1] != "external-pause-fence-1" for row in uncertainty_rows)
            )
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

            connection = store._connect()
            try:
                run = connection.execute(
                    "SELECT * FROM runs WHERE run_id = 'run-1'"
                ).fetchone()
                repository = connection.execute(
                    "SELECT * FROM repositories WHERE repository_id = 'repo-1'"
                ).fetchone()
                slot = connection.execute(
                    "SELECT * FROM outstanding_slot WHERE repository_id = "
                    "'repo-1'"
                ).fetchone()
                observation = connection.execute(
                    "SELECT * FROM effect_observations WHERE observation_id = "
                    "'late-observation-1'"
                ).fetchone()
                uncertainties = connection.execute(
                    "SELECT * FROM uncertainty_instances WHERE run_id = 'run-1' "
                    "ORDER BY uncertainty_id"
                ).fetchall()
            finally:
                connection.close()
            source_rows = [
                row for row in uncertainties
                if row["uncertainty_kind"] == "SOURCE_CONTROL"
            ]
            source_bindings = tuple(
                SourceControlUncertaintyBinding(
                    str(row["uncertainty_id"]),
                    str(row["origin_event_id"]),
                    str(row["origin_event_hash"]),
                )
                for row in source_rows
            )
            source_request = SourceControlSettlementRequest(
                repository_id="repo-1", run_id="run-1", item_id="item-1",
                logical_effect_id="effect-1", attempt_id="attempt-1",
                observation_id="late-observation-1",
                observation_event_hash=observation["event_hash"],
                source_receipt_id=canonical_before_pause.receipt_id,
                source_claim_id=canonical_before_pause.claim_id,
                source_payload_digest=canonical_before_pause.payload_digest,
                expected_catalog_head=repository["catalog_head"],
                expected_run_head=run["head_hash"],
                authoritative_query_id="source-query-1",
                authoritative_queried_at_utc=(
                    "2026-09-21T12:00:00+00:00"
                ),
                authoritative_query_after_event_id=(
                    "external-pause-event-1"
                ),
                authoritative_query_after_event_hash=(
                    source_rows[0]["origin_event_hash"]
                ),
                authoritative_source_id=(
                    "synthetic-source-control:v1:"
                    + canonical_before_pause.claim_id
                ),
                authoritative_response_id=canonical_before_pause.receipt_id,
                authoritative_response_digest=(
                    store._source_control_response_digest(observation)
                ),
                resulting_classification=SourceControlClassification.KNOWN,
                covered_source_bindings=source_bindings,
            )
            source_evidence = authority.issue_source_control_settlement_evidence(
                "source-settlement-evidence-1", source_request
            )
            validation_cursor = (
                "operation-validation:v1:late-observation-1:attempt-1:"
                "plan:run-1:revision-1"
            )
            reconcile_request = ReconcileVerifiedReceiptRequest(
                    reconciliation_id="verified-receipt-reconciliation-1",
                    command_id="verified-receipt-command-1",
                    event_id="verified-receipt-event-1",
                    repository_id="repo-1", run_id="run-1",
                    item_id="item-1", logical_effect_id="effect-1",
                    attempt_id="attempt-1", plan_id="plan:run-1",
                    revision_digest="revision-1",
                    observation_id="late-observation-1",
                    observation_event_id=observation["event_id"],
                    observation_event_hash=observation["event_hash"],
                    source_receipt_id=canonical_before_pause.receipt_id,
                    source_claim_id=canonical_before_pause.claim_id,
                    source_payload_digest=canonical_before_pause.payload_digest,
                    settlement_event_id=observation["settlement_event_id"],
                    settlement_hash=observation["settlement_hash"],
                    resolved_uncertainty_ids=tuple(
                        str(row["uncertainty_id"])
                        for row in uncertainties
                    ),
                    source_control_bindings=source_bindings,
                    source_control_query_id=source_request.authoritative_query_id,
                    source_control_queried_at_utc=(
                        source_request.authoritative_queried_at_utc
                    ),
                    source_control_query_after_event_id=(
                        source_request.authoritative_query_after_event_id
                    ),
                    source_control_query_after_event_hash=(
                        source_request.authoritative_query_after_event_hash
                    ),
                    source_control_authority_id=(
                        source_request.authoritative_source_id
                    ),
                    source_control_response_id=(
                        source_request.authoritative_response_id
                    ),
                    source_control_response_digest=(
                        source_request.authoritative_response_digest
                    ),
                    source_control_resulting_classification=(
                        SourceControlClassification.KNOWN
                    ),
                    source_control_evidence_id=source_evidence.evidence_id,
                    source_control_evidence_digest=(
                        source_evidence.request_digest
                    ),
                    source_control_issuer_fingerprint=(
                        source_evidence.issuer_fingerprint
                    ),
                    source_control_issuer_mac=source_evidence.issuer_mac,
                    expected_slot_attempt_id="attempt-1",
                    expected_slot_generation=int(slot["generation"]),
                    expected_catalog_head=repository["catalog_head"],
                    expected_run_head=run["head_hash"],
                    expected_continuation_cursor=run["continuation_cursor"],
                    expected_validation_cursor=validation_cursor,
                )

            def retargeted_lookup(
                suffix: str, **changes: object
            ) -> ReconcileVerifiedReceiptRequest:
                retargeted_source = replace(source_request, **changes)
                retargeted_evidence = (
                    authority.issue_source_control_settlement_evidence(
                        f"retargeted-source-evidence-{suffix}",
                        retargeted_source,
                    )
                )
                return replace(
                    reconcile_request,
                    source_control_query_after_event_id=(
                        retargeted_source.authoritative_query_after_event_id
                    ),
                    source_control_query_after_event_hash=(
                        retargeted_source.authoritative_query_after_event_hash
                    ),
                    source_control_authority_id=(
                        retargeted_source.authoritative_source_id
                    ),
                    source_control_response_id=(
                        retargeted_source.authoritative_response_id
                    ),
                    source_control_response_digest=(
                        retargeted_source.authoritative_response_digest
                    ),
                    source_control_evidence_id=retargeted_evidence.evidence_id,
                    source_control_evidence_digest=(
                        retargeted_evidence.request_digest
                    ),
                    source_control_issuer_fingerprint=(
                        retargeted_evidence.issuer_fingerprint
                    ),
                    source_control_issuer_mac=retargeted_evidence.issuer_mac,
                )

            for substituted in (
                replace(
                    reconcile_request,
                    expected_slot_generation=(
                        reconcile_request.expected_slot_generation + 1
                    ),
                ),
                replace(
                    reconcile_request,
                    resolved_uncertainty_ids=tuple(sorted(
                        reconcile_request.resolved_uncertainty_ids
                        + ("uncertainty:fabricated",)
                    )),
                ),
                replace(
                    reconcile_request,
                    source_control_issuer_mac="forged-source-mac",
                ),
                retargeted_lookup(
                    "stale-order",
                    authoritative_query_after_event_id=(
                        dispatched.intent.event_id
                    ),
                    authoritative_query_after_event_hash=(
                        dispatched.intent.event_hash
                    ),
                ),
                retargeted_lookup(
                    "wrong-source",
                    authoritative_source_id="synthetic-source-control:v1:other",
                ),
                retargeted_lookup(
                    "wrong-response",
                    authoritative_response_id="other-receipt",
                    authoritative_response_digest="other-response-digest",
                ),
            ):
                with self.assertRaises(DispatchDenied):
                    coordinator.reconcile_verified_receipt(substituted)
            with self.assertRaisesRegex(ValueError, "must result in KNOWN"):
                replace(
                    source_request,
                    resulting_classification=(
                        SourceControlClassification.UNKNOWN
                    ),
                ).validate()
            self.assertEqual(
                store.table_counts()[
                    "verified_receipt_reconciliation_actions"
                ],
                0,
            )

            for boundary in (
                "after_verified_receipt_event_before_clearance",
                "after_verified_receipt_writes_before_commit",
            ):
                with self.assertRaises(InjectedFailure):
                    coordinator.reconcile_verified_receipt(
                        reconcile_request, failure_hook=raise_at(boundary)
                    )
                self.assertEqual(
                    store.table_counts()[
                        "verified_receipt_reconciliation_actions"
                    ],
                    0,
                )
                store.load_verified("repo-1", authority=authority)

            with self.assertRaises(InjectedFailure):
                coordinator.reconcile_verified_receipt(
                    reconcile_request,
                    failure_hook=raise_at(
                        "after_verified_receipt_commit_before_acknowledgement"
                    ),
                )
            store.load_verified("repo-1", authority=authority)
            reconciled = coordinator.reconcile_verified_receipt(
                reconcile_request
            )
            self.assertTrue(reconciled.replayed)
            self.assertEqual(reconciled.resulting_state, LifecycleState.PAUSED)
            connection = store._connect()
            try:
                self.assertEqual(
                    connection.execute(
                        "SELECT COUNT(*) FROM uncertainty_resolutions WHERE "
                        "reconciliation_id = ?",
                        (reconciled.control_id,),
                    ).fetchone()[0],
                    4,
                )
                self.assertEqual(
                    connection.execute(
                        "SELECT COUNT(*) FROM dispatch_fences WHERE fence_id "
                        "LIKE 'uncertainty:%'"
                    ).fetchone()[0],
                    0,
                )
                self.assertEqual(
                    tuple(connection.execute(
                        "SELECT lifecycle_state, continuation_cursor FROM runs "
                        "WHERE run_id = 'run-1'"
                    ).fetchone()),
                    (LifecycleState.PAUSED.value, validation_cursor),
                )
            finally:
                connection.close()
            store.load_verified("repo-1", authority=authority)
            replay = coordinator.reconcile_verified_receipt(reconcile_request)
            self.assertTrue(replay.replayed)
            self.assertEqual(replay.event_hash, reconciled.event_hash)
            store._freshness_oracle = NeverFreshOracle()
            stale_freshness_replay = coordinator.reconcile_verified_receipt(
                reconcile_request
            )
            self.assertTrue(stale_freshness_replay.replayed)
            self.assertEqual(
                stale_freshness_replay.event_hash, reconciled.event_hash
            )
            with self.assertRaisesRegex(
                StorageIntegrityError,
                "command ID was reused with a different payload",
            ):
                coordinator.reconcile_verified_receipt(
                    replace(
                        reconcile_request,
                        event_id="conflicting-replay-event",
                    )
                )
            store._freshness_oracle = AlwaysFreshOracle()

            connection = store._connect()
            try:
                recorded_body = json.loads(connection.execute(
                    "SELECT body_json FROM events WHERE event_id = ?",
                    (reconcile_request.event_id,),
                ).fetchone()[0])
                surplus_body = dict(recorded_body)
                surplus_body["surplus_lookup_field"] = "forbidden"
                missing_body = dict(recorded_body)
                missing_body.pop("source_control_response_digest")
                for malformed in (surplus_body, missing_body):
                    with self.assertRaisesRegex(
                        StorageIntegrityError,
                        "verified-receipt reconciliation semantics are invalid",
                    ):
                        store._validate_verified_receipt_reconciliation_event(
                            connection,
                            malformed,
                            LifecycleState.RECONCILIATION_REQUIRED,
                            reconcile_request.expected_continuation_cursor,
                        )
            finally:
                connection.close()

            connection = store._connect()
            try:
                action_digest = connection.execute(
                    "SELECT source_response_digest FROM "
                    "verified_receipt_reconciliation_actions WHERE "
                    "reconciliation_id = ?",
                    (reconcile_request.reconciliation_id,),
                ).fetchone()[0]
                connection.execute(
                    "UPDATE verified_receipt_reconciliation_actions SET "
                    "source_response_digest = 'tampered-response' WHERE "
                    "reconciliation_id = ?",
                    (reconcile_request.reconciliation_id,),
                )
                connection.commit()
            finally:
                connection.close()
            with self.assertRaisesRegex(
                StorageIntegrityError, "verified-receipt projection diverges"
            ):
                store.load_verified("repo-1", authority=authority)
            connection = store._connect()
            try:
                connection.execute(
                    "UPDATE verified_receipt_reconciliation_actions SET "
                    "source_response_digest = ? WHERE reconciliation_id = ?",
                    (action_digest, reconcile_request.reconciliation_id),
                )
                resolution = connection.execute(
                    "SELECT * FROM uncertainty_resolutions ORDER BY "
                    "uncertainty_id LIMIT 1"
                ).fetchone()
                connection.execute(
                    "DELETE FROM uncertainty_resolutions WHERE uncertainty_id = ?",
                    (resolution["uncertainty_id"],),
                )
                connection.commit()
            finally:
                connection.close()
            with self.assertRaisesRegex(
                StorageIntegrityError,
                "uncertainty-resolution projection diverges",
            ):
                store.load_verified("repo-1", authority=authority)
            connection = store._connect()
            try:
                connection.execute(
                    "INSERT INTO uncertainty_resolutions VALUES (?, ?, ?, ?, "
                    "?, ?, ?)",
                    tuple(resolution),
                )
                connection.commit()
            finally:
                connection.close()
            store.load_verified("repo-1", authority=authority)

    def test_t17_verified_receipt_reconciles_observation_billing_ancestry(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            authority = SyntheticAuthority()
            grant = SyntheticGrant(
                "billing-grant", "repo-1", "effect-1", "attempt-1",
                "scope-1",
            )
            authority.register(grant)
            capability = authority.claim(*grant.__dict__.values())
            with self.state_root_context(root):
                store = SQLiteStateStore.open_canonical(
                    "repo-1", AlwaysFreshOracle()
                )
                adapter = SyntheticExecutionAdapter.open_canonical("repo-1")
            coordinator = SyntheticDispatchCoordinator(
                store, TransitionEngine(), authority, adapter
            )
            intent = IntentRequest(
                "repo-1", "run-1", "item-1", "billing-command",
                "billing-event", "effect-1", "payload-1", "attempt-1",
                "billing-permission", "billing-reservation", "budget-1",
                1, 2, 5,
            )
            plan = self._accept_operation_plan(store, intent)
            coordinator.dispatch(
                intent, capability,
                SyntheticEffectRequest(
                    "repo-1", "effect-1", "attempt-1", "scope-1",
                    "payload-1",
                ),
                expected_head=plan.event_hash, writer_epoch=2,
                usage_units=None, lose_receipt=True,
            )
            receipt = adapter.reconcile(capability.claim_id)
            self.assertIsNotNone(receipt)
            observed = coordinator.intake_effect_receipt(
                EffectObservationCommand(
                    "billing-observation", "billing-observe-command",
                    "billing-observe-event", "repo-1", "run-1", "item-1",
                    "effect-1", "attempt-1", capability.claim_id,
                    "billing-unknown-settlement", "",
                )
            )
            self.assertEqual(
                observed.resulting_state,
                LifecycleState.RECONCILIATION_REQUIRED,
            )
            connection = store._connect()
            try:
                observation = connection.execute(
                    "SELECT * FROM effect_observations WHERE observation_id = "
                    "'billing-observation'"
                ).fetchone()
                uncertainty = connection.execute(
                    "SELECT * FROM uncertainty_instances WHERE origin_event_id "
                    "= 'billing-observe-event'"
                ).fetchone()
            finally:
                connection.close()
            self.assertEqual(uncertainty["uncertainty_kind"], "BILLING")
            adjusted = store._settle_budget(
                BudgetSettlementRequest(
                    "billing-authoritative-settlement", "billing-reservation",
                    observation["settlement_hash"],
                    BudgetDisposition.ADJUSTED, 1,
                    "billing-authoritative-evidence", "AUTHORITATIVE_USAGE",
                ),
                authority.issue_settlement_proof(
                    "billing-authoritative-proof",
                    BudgetSettlementRequest(
                        "billing-authoritative-settlement",
                        "billing-reservation", observation["settlement_hash"],
                        BudgetDisposition.ADJUSTED, 1,
                        "billing-authoritative-evidence",
                        "AUTHORITATIVE_USAGE",
                    ),
                ),
                authority,
            )
            connection = store._connect()
            try:
                run = connection.execute(
                    "SELECT * FROM runs WHERE run_id = 'run-1'"
                ).fetchone()
                repository = connection.execute(
                    "SELECT * FROM repositories WHERE repository_id = 'repo-1'"
                ).fetchone()
                slot = connection.execute(
                    "SELECT * FROM outstanding_slot WHERE repository_id = "
                    "'repo-1'"
                ).fetchone()
            finally:
                connection.close()
            source_request = SourceControlSettlementRequest(
                repository_id="repo-1", run_id="run-1", item_id="item-1",
                logical_effect_id="effect-1", attempt_id="attempt-1",
                observation_id="billing-observation",
                observation_event_hash=observation["event_hash"],
                source_receipt_id=receipt.receipt_id,
                source_claim_id=receipt.claim_id,
                source_payload_digest=receipt.payload_digest,
                expected_catalog_head=repository["catalog_head"],
                expected_run_head=run["head_hash"],
                authoritative_query_id="billing-query",
                authoritative_queried_at_utc=(
                    "2026-09-21T12:01:00+00:00"
                ),
                authoritative_query_after_event_id=observation["event_id"],
                authoritative_query_after_event_hash=observation["event_hash"],
                authoritative_source_id=(
                    "synthetic-source-control:v1:" + receipt.claim_id
                ),
                authoritative_response_id=receipt.receipt_id,
                authoritative_response_digest=(
                    store._source_control_response_digest(observation)
                ),
                resulting_classification=SourceControlClassification.KNOWN,
                covered_source_bindings=(),
            )
            source_evidence = authority.issue_source_control_settlement_evidence(
                "billing-source-evidence", source_request
            )
            validation_cursor = (
                "operation-validation:v1:billing-observation:attempt-1:"
                "plan:run-1:revision-1"
            )
            reconciled = coordinator.reconcile_verified_receipt(
                ReconcileVerifiedReceiptRequest(
                    reconciliation_id="billing-reconciliation",
                    command_id="billing-reconcile-command",
                    event_id="billing-reconcile-event",
                    repository_id="repo-1", run_id="run-1",
                    item_id="item-1", logical_effect_id="effect-1",
                    attempt_id="attempt-1", plan_id="plan:run-1",
                    revision_digest="revision-1",
                    observation_id="billing-observation",
                    observation_event_id=observation["event_id"],
                    observation_event_hash=observation["event_hash"],
                    source_receipt_id=receipt.receipt_id,
                    source_claim_id=receipt.claim_id,
                    source_payload_digest=receipt.payload_digest,
                    settlement_event_id=adjusted.settlement_event_id,
                    settlement_hash=adjusted.settlement_hash,
                    resolved_uncertainty_ids=(
                        str(uncertainty["uncertainty_id"]),
                    ),
                    source_control_bindings=(),
                    source_control_query_id=source_request.authoritative_query_id,
                    source_control_queried_at_utc=(
                        source_request.authoritative_queried_at_utc
                    ),
                    source_control_query_after_event_id=(
                        source_request.authoritative_query_after_event_id
                    ),
                    source_control_query_after_event_hash=(
                        source_request.authoritative_query_after_event_hash
                    ),
                    source_control_authority_id=(
                        source_request.authoritative_source_id
                    ),
                    source_control_response_id=(
                        source_request.authoritative_response_id
                    ),
                    source_control_response_digest=(
                        source_request.authoritative_response_digest
                    ),
                    source_control_resulting_classification=(
                        SourceControlClassification.KNOWN
                    ),
                    source_control_evidence_id=source_evidence.evidence_id,
                    source_control_evidence_digest=(
                        source_evidence.request_digest
                    ),
                    source_control_issuer_fingerprint=(
                        source_evidence.issuer_fingerprint
                    ),
                    source_control_issuer_mac=source_evidence.issuer_mac,
                    expected_slot_attempt_id="attempt-1",
                    expected_slot_generation=int(slot["generation"]),
                    expected_catalog_head=repository["catalog_head"],
                    expected_run_head=run["head_hash"],
                    expected_continuation_cursor=run["continuation_cursor"],
                    expected_validation_cursor=validation_cursor,
                )
            )
            self.assertEqual(
                reconciled.resulting_state, LifecycleState.VALIDATING
            )
            store.load_verified("repo-1", authority=authority)

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
            with self.state_root_context(root):
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
    def state_root_context(root: Path):
        if sys.platform == "win32":
            return patch(
                "tools.aegis_delivery_control.storage.known_local_state_base",
                return_value=root,
            )
        return patch.dict(os.environ, {"XDG_STATE_HOME": str(root)})

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

    def _prepare_t08_active_validator(
        self,
        root: Path,
        *,
        contact: bool,
        result: bool = False,
        cessation: bool = False,
        intake_result: bool = True,
        result_usage_units: int | None = 1,
    ):
        authority = SyntheticAuthority()
        effect_grant = SyntheticGrant(
            "effect-grant-t08", "repo-1", "effect-1", "attempt-1", "scope-1"
        )
        authority.register(effect_grant)
        effect_capability = authority.claim(*effect_grant.__dict__.values())
        with self.state_root_context(root):
            store = SQLiteStateStore.open_canonical(
                "repo-1", AlwaysFreshOracle()
            )
            effect_adapter = SyntheticExecutionAdapter.open_canonical("repo-1")
            validator_adapter = SyntheticValidatorAdapter.open_canonical("repo-1")
        dispatch = SyntheticDispatchCoordinator(
            store, TransitionEngine(), authority, effect_adapter
        )
        operation = IntentRequest(
            "repo-1", "run-1", "item-1", "operation-command-t08",
            "operation-event-t08", "effect-1", "payload-1", "attempt-1",
            "operation-permission-t08", "operation-reservation-t08",
            "budget-1", 1, 1, 10,
        )
        plan = self._accept_operation_plan(store, operation)
        dispatch.dispatch(
            operation, effect_capability,
            SyntheticEffectRequest(
                "repo-1", "effect-1", "attempt-1", "scope-1", "payload-1"
            ),
            expected_head=plan.event_hash, writer_epoch=2, usage_units=1,
        )
        parent = dispatch.intake_effect_receipt(
            EffectObservationCommand(
                "parent-observation-t08", "parent-observe-command-t08",
                "parent-observe-event-t08", "repo-1", "run-1", "item-1",
                "effect-1", "attempt-1", effect_capability.claim_id,
                "operation-settlement-t08", "",
            )
        )
        validator_grant = SyntheticValidatorGrant(
            "validator-grant-t08", "repo-1", "effect-1", "revision-1",
            "check-1", "input-1", "validator-attempt-1", "read-only-1",
        )
        authority.register_validator(validator_grant)
        validator_capability = authority.claim_validator(
            *validator_grant.__dict__.values()
        )
        validator_intent = ValidatorIntentRequest(
            "validator-intent-t08", "validator-command-t08",
            "validator-event-t08", "repo-1", "run-1", "item-1", "effect-1",
            "attempt-1", "parent-observation-t08", parent.event_hash,
            "revision-1", "check-1", "input-1", "validator-attempt-1",
            "validator-permission-t08", "validator-reservation-t08",
            "budget-1", 1, 2, 10,
        )
        if result:
            validation = SyntheticValidationCoordinator(
                store, TransitionEngine(), authority, validator_adapter
            )
            launched = validation.launch(
                validator_intent,
                validator_capability,
                SyntheticValidatorRequest(
                    "repo-1", "effect-1", "revision-1", "check-1",
                    "input-1", "validator-attempt-1", "read-only-1",
                    "result-digest-t08", "PASS",
                ),
                usage_units=result_usage_units,
            )
            committed = launched.intent
            settlement_request = BudgetSettlementRequest(
                "validator-settlement-t08", "validator-reservation-t08", "",
                (
                    BudgetDisposition.CONSUMED
                    if result_usage_units is not None
                    else BudgetDisposition.UNKNOWN_WORST_CASE_CHARGED
                ),
                result_usage_units,
                launched.result.result_id, "VALIDATOR_USAGE_REPORTED",
                attempt_id="validator-attempt-1",
            )
            settlement = store._settle_budget(
                settlement_request,
                authority.issue_settlement_proof(
                    "validator-settlement-proof-t08", settlement_request
                ),
                authority,
            )
            if intake_result:
                validation.intake_result(
                    ValidatorObservationCommand(
                        "validator-observation-t08",
                        "validator-observe-command-t08",
                        "validator-observe-event-t08", "repo-1", "run-1",
                        "item-1", "validator-intent-t08",
                        "validator-settlement-t08", settlement.settlement_hash,
                    )
                )
            if cessation:
                cessation_attestation = (
                    authority.issue_validator_cessation_attestation(
                        "cessation-attestation-t08", "cessation-t08",
                        validator_adapter._target_digest("repo-1"),
                        validator_capability.claim_id,
                        "VALIDATOR:validator-intent-t08",
                        committed.event_hash, "repo-1", "run-1", "item-1",
                        "effect-1", "revision-1", "check-1",
                        "validator-attempt-1",
                    )
                )
                cessation_seal = validator_adapter.seal_cessation(
                    cessation_attestation, authority
                )
                store.record_validator_cessation(
                    ValidatorCessationRequest(
                        "cessation-t08", "cessation-command-t08",
                        "cessation-event-t08", "repo-1", "run-1", "item-1",
                        "effect-1", "validator-intent-t08",
                        "validator-attempt-1", "revision-1", "check-1",
                        cessation_seal.cessation_hash,
                    ),
                    authority,
                )
        else:
            committed = store.commit_validator_intent(
                validator_intent, validator_capability, authority
            )
        if contact and not result:
            store._contact_committed_validator(
                validator_intent, validator_capability, committed,
                validator_adapter._target_digest("repo-1"), authority,
            )
        return (
            authority, store, dispatch, validator_adapter, validator_intent,
            validator_capability, committed,
        )

    def _prepare_t09_operation_reconciliation(self, root: Path):
        authority = SyntheticAuthority()
        effect_grant = SyntheticGrant(
            "effect-grant-t09", "repo-1", "effect-1", "attempt-1", "scope-1"
        )
        authority.register(effect_grant)
        effect_capability = authority.claim(*effect_grant.__dict__.values())
        with self.state_root_context(root):
            store = SQLiteStateStore.open_canonical(
                "repo-1", AlwaysFreshOracle()
            )
            adapter = SyntheticExecutionAdapter.open_canonical("repo-1")
        dispatch = SyntheticDispatchCoordinator(
            store, TransitionEngine(), authority, adapter
        )
        intent = IntentRequest(
            "repo-1", "run-1", "item-1", "operation-command-t09",
            "operation-event-t09", "effect-1", "payload-1", "attempt-1",
            "operation-permission-t09", "reservation-t09", "budget-1",
            1, 2, 5,
        )
        plan = self._accept_operation_plan(store, intent)
        dispatched = dispatch.dispatch(
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
        initial_pause_grant = SyntheticOperatorGrant(
            "external-pause-grant-t09", "repo-1", "run-1", "PAUSE",
            "external-pause-scope-t09",
        )
        authority.register_operator(initial_pause_grant)
        dispatch.pause_external_mutation(
            PauseExternalMutationRequest(
                "external-pause-t09", "external-pause-command-t09",
                "external-pause-event-t09", "external-pause-fence-t09",
                "repo-1", "run-1", "item-1", "effect-1", "attempt-1",
                dispatched.intent.event_id, dispatched.intent.event_hash,
                launch["launch_id"], launch["event_id"], launch["event_hash"],
                contact["contact_id"], contact["event_id"],
                contact["event_hash"], contact["target_digest"], 1,
                "OPERATOR_PAUSE_EXTERNAL_MUTATION",
            ),
            authority.claim_operator(*initial_pause_grant.__dict__.values()),
        )
        return authority, store, dispatch, adapter, effect_capability

    @staticmethod
    def _t09_pause_request(
        store: SQLiteStateStore,
        *,
        suffix: str,
    ) -> PauseReconciliationRequest:
        connection = store._connect()
        try:
            run = connection.execute(
                "SELECT * FROM runs WHERE run_id = 'run-1'"
            ).fetchone()
            source = connection.execute(
                "SELECT event_id FROM events WHERE event_hash = ?",
                (run["head_hash"],),
            ).fetchone()
            plan = connection.execute(
                "SELECT * FROM validation_plans WHERE run_id = 'run-1'"
            ).fetchone()
        finally:
            connection.close()
        return PauseReconciliationRequest(
            pause_id=f"reconciliation-pause-{suffix}",
            command_id=f"reconciliation-pause-command-{suffix}",
            event_id=f"reconciliation-pause-event-{suffix}",
            fence_id=f"reconciliation-pause-fence-{suffix}",
            repository_id="repo-1",
            run_id="run-1",
            item_id=str(plan["item_id"]),
            logical_effect_id=str(plan["logical_effect_id"]),
            plan_id=str(plan["plan_id"]),
            revision_digest=str(plan["revision_digest"]),
            reason_code="OPERATOR_PAUSE_RECONCILIATION",
            source_event_id=str(source["event_id"]),
            source_event_hash=str(run["head_hash"]),
            expected_preserved_continuation_cursor=run["continuation_cursor"],
        )

    @staticmethod
    def _t08_pause_request(
        store: SQLiteStateStore,
        *,
        suffix: str,
    ) -> PauseValidationRequest:
        connection = store._connect()
        try:
            checkpoint = store._validator_pause_checkpoint(
                connection, "repo-1", "run-1"
            )
            cursor = connection.execute(
                "SELECT continuation_cursor FROM runs WHERE run_id = 'run-1'"
            ).fetchone()["continuation_cursor"]
        finally:
            connection.close()
        return PauseValidationRequest(
            pause_id=f"validation-pause-{suffix}",
            command_id=f"validation-pause-command-{suffix}",
            request_event_id=f"validation-pause-request-{suffix}",
            checkpoint_event_id=f"validation-pause-checkpoint-{suffix}",
            fence_id=f"validation-pause-fence-{suffix}",
            repository_id="repo-1",
            run_id="run-1",
            item_id="item-1",
            logical_effect_id="effect-1",
            plan_id="plan:run-1",
            revision_digest="revision-1",
            reason_code="OPERATOR_PAUSE_VALIDATION",
            expected_preserved_continuation_cursor=cursor,
            expected_checkpoint_kind=str(checkpoint["checkpoint_kind"]),
            **{
                field: checkpoint[field]
                for field in (
                    "expected_slot_attempt_id", "expected_slot_generation",
                    "validator_intent_id", "validator_intent_event_id",
                    "validator_intent_event_hash", "validator_attempt_id",
                    "check_id", "reservation_id",
                    "expected_settlement_head_hash", "contact_id",
                    "contact_event_id", "contact_event_hash",
                    "contact_target_digest", "observation_id",
                    "observation_event_id", "observation_event_hash",
                    "observation_settlement_event_id",
                    "observation_settlement_event_hash",
                )
            },
        )

    def _prepare_t25_effect(self, root: Path):
        authority = SyntheticAuthority()
        grant = SyntheticGrant(
            "grant-1", "repo-1", "effect-1", "attempt-1", "scope-1"
        )
        authority.register(grant)
        capability = authority.claim(*grant.__dict__.values())
        with self.state_root_context(root):
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
            with self.state_root_context(root):
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
            with self.state_root_context(root):
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
            with self.state_root_context(root):
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
            with self.state_root_context(root):
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
            with self.state_root_context(root):
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
            with self.state_root_context(root):
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
            with self.state_root_context(root):
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
            with self.state_root_context(root):
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

            with self.state_root_context(root):
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
            with self.state_root_context(root):
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
            with self.state_root_context(root):
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
            command = [
                sys.executable,
                "-m",
                "tools.aegis_delivery_control",
            ]
            if sys.platform == "win32":
                command = [
                    sys.executable,
                    "-c",
                    (
                        "import sys; from pathlib import Path; "
                        "from unittest.mock import patch; "
                        "scope = patch("
                        "'tools.aegis_delivery_control.storage.known_local_state_base', "
                        "return_value=Path(sys.argv.pop(1))); "
                        "scope.start(); "
                        "from tools.aegis_delivery_control.cli import main; "
                        "raise SystemExit(main())"
                    ),
                    str(root),
                ]
            else:
                environment["XDG_STATE_HOME"] = str(root)
            command.extend(
                [
                    "--repository-id", "repo-1", "verify",
                    "--expected-vector", str(expected_vector),
                    "--authority-key-file", str(authority_key),
                ]
            )
            verified = subprocess.run(
                command,
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
            with self.state_root_context(root):
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
            with self.state_root_context(root):
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
            with self.state_root_context(root):
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
            with self.state_root_context(root):
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
            with self.state_root_context(root):
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
            with self.state_root_context(root):
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
            with self.state_root_context(root):
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
            with self.state_root_context(root):
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
            with self.state_root_context(root):
                recovered_store = SQLiteStateStore.open_canonical(
                    "repo-1", AlwaysFreshOracle()
                )
            recovered_store.load_verified("repo-1", authority=authority)
            recovered_coordinator = SyntheticDispatchCoordinator(
                recovered_store, TransitionEngine(), authority, adapter
            )
            replay = recovered_coordinator.intake_effect_receipt(command)

            self.assertTrue(replay.replayed)
            self.assertEqual(recovered_store.table_counts()["events"], 7)
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

    def test_t17_unknown_source_with_known_usage_creates_only_source_fence(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            authority = SyntheticAuthority()
            grant = SyntheticGrant(
                "grant-source-unknown", "repo-1", "effect-1", "attempt-1",
                "scope-1",
            )
            authority.register(grant)
            capability = authority.claim(*grant.__dict__.values())
            with self.state_root_context(root):
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
            coordinator.dispatch(
                intent, capability,
                SyntheticEffectRequest(
                    "repo-1", "effect-1", "attempt-1", "scope-1",
                    "payload-1",
                ),
                expected_head=plan.event_hash, writer_epoch=2,
                usage_units=1, lose_receipt=True,
            )
            receipt = adapter.reconcile(capability.claim_id)
            self.assertIsNotNone(receipt)
            evidence_request = SourceControlEvidenceRequest(
                receipt.repository_id, receipt.run_id, receipt.item_id,
                receipt.logical_effect_id, receipt.attempt_id,
                receipt.claim_id, receipt.receipt_id, receipt.payload_digest,
                receipt.usage_units, receipt.accepted,
                SourceControlClassification.UNKNOWN,
            )
            evidence = authority.issue_source_control_evidence(
                "source-unknown-proof-1", evidence_request
            )
            observed = coordinator.intake_effect_receipt(
                EffectObservationCommand(
                    "observation-1", "observe-command-1",
                    "observation-event-1", "repo-1", "run-1", "item-1",
                    "effect-1", "attempt-1", capability.claim_id,
                    "settlement-1", "",
                ),
                source_control_classification=(
                    SourceControlClassification.UNKNOWN
                ),
                source_control_evidence=evidence,
            )
            self.assertEqual(
                observed.resulting_state,
                LifecycleState.RECONCILIATION_REQUIRED,
            )
            connection = sqlite3.connect(store._database_path)
            try:
                kinds = connection.execute(
                    "SELECT uncertainty_kind FROM uncertainty_instances "
                    "WHERE origin_event_id = 'observation-event-1' ORDER BY 1"
                ).fetchall()
            finally:
                connection.close()
            self.assertEqual(kinds, [("SOURCE_CONTROL",)])
            store.load_verified("repo-1", authority=authority)
            connection = sqlite3.connect(store._database_path)
            try:
                uncertainty_id = connection.execute(
                    "SELECT uncertainty_id FROM uncertainty_instances WHERE "
                    "origin_event_id = 'observation-event-1'"
                ).fetchone()[0]
                connection.execute(
                    "DELETE FROM dispatch_fences WHERE fence_id = ?",
                    (uncertainty_id,),
                )
                connection.execute(
                    "DELETE FROM uncertainty_instances WHERE uncertainty_id = ?",
                    (uncertainty_id,),
                )
                connection.commit()
            finally:
                connection.close()
            with self.assertRaisesRegex(
                StorageIntegrityError,
                "operation-uncertainty projection diverges",
            ):
                SQLiteStateStore(
                    store._database_path, store._freshness_oracle, "repo-1"
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
            with self.state_root_context(root):
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
            with self.state_root_context(root):
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
            valid_contained_request = SyntheticValidatorRequest(
                "repo-1", "effect-1", "revision-1", "check-1", "input-1",
                "validator-attempt-1", "read-only-1", "result-digest-1",
                "PASS",
            )
            with self.assertRaisesRegex(DispatchDenied, "output size binding"):
                validation.launch(
                    validator_intent,
                    validator_capability,
                    replace(valid_contained_request, output_bytes=0),
                    usage_units=1,
                )
            base_spec = json.loads(validator_intent.containment_spec_json)
            invalid_specs = (
                {
                    **base_spec,
                    "output_root": f"{base_spec['input_root']}/nested",
                },
                {
                    **base_spec,
                    "input_root": f"{base_spec['output_root']}/nested",
                },
                {**base_spec, "max_output_bytes": 4097},
            )
            for invalid_spec in invalid_specs:
                with self.subTest(invalid_spec=invalid_spec), self.assertRaisesRegex(
                    ValueError, "containment"
                ):
                    validation.launch(
                        replace(
                            validator_intent,
                            containment_spec_json=json.dumps(
                                invalid_spec,
                                sort_keys=True,
                                separators=(",", ":"),
                            ),
                        ),
                        validator_capability,
                        valid_contained_request,
                        usage_units=1,
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
            cessation_attestation = (
                authority.issue_validator_cessation_attestation(
                    "cessation-attestation-1", "cessation-1",
                    validator_adapter._target_digest("repo-1"),
                    validator_capability.claim_id,
                    "VALIDATOR:launch:command-1", launched.intent.event_hash,
                    "repo-1", "run-1", "item-1", "effect-1", "revision-1",
                    "check-1", "validator-attempt-1",
                )
            )
            cessation_seal = validator_adapter.seal_cessation(
                cessation_attestation, authority
            )
            cessation = store.record_validator_cessation(
                ValidatorCessationRequest(
                    "cessation-1", "cessation-command-1", "cessation-event-1",
                    "repo-1", "run-1", "item-1", "effect-1",
                    "launch:command-1", "validator-attempt-1", "revision-1",
                    "check-1", cessation_seal.cessation_hash,
                ),
                authority,
            )
            connection = sqlite3.connect(store._database_path)
            try:
                observation = connection.execute(
                    "SELECT event_hash FROM validator_observations WHERE "
                    "observation_id = 'validator-observation-1'"
                ).fetchone()
                uncertainty_ids = tuple(
                    row[0]
                    for row in connection.execute(
                        "SELECT uncertainty_id FROM uncertainty_instances WHERE "
                        "origin_event_id = 'validator-observation-event-1'"
                    )
                )
            finally:
                connection.close()
            reconciliation = validation.reconcile_result(
                ReconcileValidatorResultRequest(
                    "reconciliation-1", "reconciliation-command-1",
                    "reconciliation-event-1", "repo-1", "run-1", "item-1",
                    "effect-1", "plan-1", "revision-1",
                    "validator-observation-1", observation[0], "cessation-1",
                    "cessation-event-1", cessation.event_hash,
                    "validator-settlement-1", validator_settlement.settlement_hash,
                    uncertainty_ids, "attempt-1", 1, cessation.event_hash, None,
                )
            )
            self.assertEqual(
                reconciliation.resulting_state, LifecycleState.VALIDATING
            )
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
            with self.state_root_context(root):
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
