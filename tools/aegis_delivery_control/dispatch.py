"""Single mediated path for synthetic effect dispatch."""

from __future__ import annotations

from dataclasses import dataclass

from .adapters import (
    SyntheticEffectRequest,
    SyntheticExecutionAdapter,
    SyntheticReceipt,
    SyntheticValidatorAdapter,
    SyntheticValidatorRequest,
    SyntheticValidatorResult,
    validate_synthetic_validator_containment,
)
from .authority import (
    SyntheticAuthority,
    SyntheticActivityResumeEvidence,
    SyntheticAuthorityLifecycleEvidence,
    SyntheticBindingObservation,
    SyntheticCapability,
    SyntheticClassificationEvidence,
    SyntheticFinalizationAttestation,
    SyntheticOperatorCapability,
    SyntheticProofFreeDispositionEvidence,
    SyntheticSettledValidationResumeEvidence,
    SyntheticSettledValidationPauseRecoveryAttestation,
    SyntheticOperationNonexecutionResumeEvidence,
    SyntheticSafeSameEffectRetryEvidence,
    SyntheticSafeRetrySourceControlEvidence,
    SyntheticReconciliationResumeEvidence,
    SyntheticResumeEvidence,
    SyntheticSourceControlEvidence,
    SyntheticSourceControlSettlementEvidence,
    SyntheticSourceCapability,
    SyntheticAdoptionReadinessEvidence,
    SyntheticValidationLaunchSnapshot,
    SyntheticValidatorCapability,
    SyntheticValidatorActivityAttestation,
)
from .capabilities import require_synthetic_dispatch, require_synthetic_validation
from .contracts import (
    ApplicationReceipt,
    ActiveValidationPauseRequest,
    AuthorizeSafeSameEffectRetryRequest,
    AuthorityLifecycleFactRequest,
    BindingMismatchRequest,
    CommitReceipt,
    ControlReceipt,
    DispatchDenied,
    EffectAdoptionReceipt,
    EffectAdoptionRequest,
    EffectObservationCommand,
    EffectObservationRequest,
    FinalizeOperationRequest,
    IntentRequest,
    LifecycleState,
    ObservationReceipt,
    OperationFinalizationReceipt,
    PauseBeforeDispatchRequest,
    PauseActivitySettlementRequest,
    PauseExternalMutationRequest,
    PauseLocalExecutionRequest,
    PauseReconciliationRequest,
    PauseValidationRequest,
    ProofFreeDispositionRequest,
    ReconcileVerifiedReceiptRequest,
    ReconcileValidatorResultRequest,
    ReconciliationPauseResumeRequest,
    RecoverProvenNonexecutionRequest,
    ResumeRequest,
    ResumeActivitySettlementRequest,
    ResumeSettledValidationPauseRequest,
    SettledValidationPauseRecoveryRequest,
    ResumeOperationNonexecutionRequest,
    SourceControlClassification,
    SourceControlEvidenceRequest,
    StopMode,
    StopEscalationRequest,
    StopRequest,
    TerminalRestartReport,
    TerminalRestartRequest,
    ValidationApplicationRequest,
    ValidationPauseSettlementRequest,
    ValidatorIntentRequest,
    ValidatorObservationCommand,
    ValidatorObservationRequest,
    ProvenNonexecutionIntentRequest,
    parse_validator_containment_spec,
    validator_containment_digest,
)
from .engine import TRANSITIONS, TransitionEngine
from .storage import FailureHook, SQLiteStateReader, SQLiteStateStore


@dataclass(frozen=True)
class SyntheticDispatchReceipt:
    intent: CommitReceipt
    effect: SyntheticReceipt | None


@dataclass(frozen=True)
class SyntheticValidationReceipt:
    intent: CommitReceipt
    result: SyntheticValidatorResult | None


class SyntheticReadCoordinator:
    """Expose non-authorizing verified reads without adapter access."""

    def __init__(
        self, reader: SQLiteStateReader, engine: TransitionEngine
    ) -> None:
        self._reader = reader
        self._engine = engine

    def report_terminal_restart(
        self, request: TerminalRestartRequest
    ) -> TerminalRestartReport:
        def authorize(
            current_state: LifecycleState, resulting_state: LifecycleState
        ) -> None:
            self._engine.authorize(
                "T22",
                current_state,
                resulting_state,
                TRANSITIONS["T22"].required_guards,
            )

        return self._reader.report_terminal_restart(
            request, authorize_transition=authorize
        )


class SyntheticDispatchCoordinator:
    """Authorize, durably reserve, then contact the synthetic adapter once."""

    def __init__(
        self,
        store: SQLiteStateStore,
        engine: TransitionEngine,
        authority: SyntheticAuthority,
        adapter: SyntheticExecutionAdapter,
    ) -> None:
        if not store.is_canonical:
            raise DispatchDenied("dispatch store is not the canonical repository root")
        store._bind_classification_authority(authority)
        self._store = store
        self._engine = engine
        self._authority = authority
        self._adapter = adapter

    def pause_before_dispatch(
        self,
        request: PauseBeforeDispatchRequest,
        capability: SyntheticOperatorCapability,
        *,
        failure_hook: FailureHook | None = None,
    ) -> ControlReceipt:
        def authorize(
            current_state: LifecycleState, resulting_state: LifecycleState
        ) -> None:
            self._engine.authorize(
                "T04",
                current_state,
                resulting_state,
                TRANSITIONS["T04"].required_guards,
            )

        return self._store.pause_before_dispatch(
            request,
            capability,
            self._authority,
            authorize_transition=authorize,
            failure_hook=failure_hook,
        )

    def stop(
        self,
        request: StopRequest,
        capability: SyntheticOperatorCapability,
        *,
        failure_hook: FailureHook | None = None,
    ) -> ControlReceipt:
        transition_id = "T18" if request.mode is StopMode.GRACEFUL else "T19"

        def authorize(
            current_state: LifecycleState, resulting_state: LifecycleState
        ) -> None:
            self._engine.authorize(
                transition_id,
                current_state,
                resulting_state,
                TRANSITIONS[transition_id].required_guards,
            )

        return self._store.stop(
            request,
            capability,
            self._authority,
            authorize_transition=authorize,
            failure_hook=failure_hook,
        )

    def adopt_verified_effect(
        self,
        request: EffectAdoptionRequest,
        readiness: SyntheticAdoptionReadinessEvidence,
        capability: SyntheticSourceCapability,
        *,
        failure_hook: FailureHook | None = None,
    ) -> EffectAdoptionReceipt:
        def authorize(
            current_state: LifecycleState, resulting_state: LifecycleState
        ) -> None:
            self._engine.authorize(
                "T28",
                current_state,
                resulting_state,
                TRANSITIONS["T28"].required_guards,
            )

        return self._store.adopt_verified_effect(
            request,
            readiness,
            capability,
            self._authority,
            authorize_transition=authorize,
            failure_hook=failure_hook,
        )

    def pause_local_execution(
        self,
        request: PauseLocalExecutionRequest,
        capability: SyntheticOperatorCapability,
        *,
        failure_hook: FailureHook | None = None,
    ) -> ControlReceipt:
        def authorize(
            current_state: LifecycleState, resulting_state: LifecycleState
        ) -> None:
            self._engine.authorize(
                "T05",
                current_state,
                resulting_state,
                TRANSITIONS["T05"].required_guards,
            )

        return self._store.pause_local_execution(
            request,
            capability,
            self._authority,
            authorize_transition=authorize,
            failure_hook=failure_hook,
        )

    def pause_external_mutation(
        self,
        request: PauseExternalMutationRequest,
        capability: SyntheticOperatorCapability,
        *,
        failure_hook: FailureHook | None = None,
    ) -> ControlReceipt:
        def authorize(
            current_state: LifecycleState, resulting_state: LifecycleState
        ) -> None:
            transition_id = (
                "T09"
                if current_state is LifecycleState.RECONCILIATION_REQUIRED
                else "T06"
            )
            self._engine.authorize(
                transition_id,
                current_state,
                resulting_state,
                TRANSITIONS[transition_id].required_guards
                | (frozenset({"effect_bound"}) if transition_id == "T09" else frozenset()),
                event_kind="PAUSE_REQUESTED",
            )

        return self._store.pause_external_mutation(
            request,
            capability,
            self._authority,
            authorize_transition=authorize,
            failure_hook=failure_hook,
        )

    def pause_validation(
        self,
        request: PauseValidationRequest,
        capability: SyntheticOperatorCapability,
        *,
        failure_hook: FailureHook | None = None,
    ) -> ControlReceipt:
        def authorize(
            current_state: LifecycleState, resulting_state: LifecycleState
        ) -> None:
            transition_id = (
                "T09"
                if current_state is LifecycleState.RECONCILIATION_REQUIRED
                else "T08"
            )
            self._engine.authorize(
                transition_id,
                current_state,
                resulting_state,
                TRANSITIONS[transition_id].required_guards,
                event_kind="VALIDATION_PAUSE_REQUESTED",
            )

        return self._store.pause_validation(
            request,
            capability,
            self._authority,
            authorize_transition=authorize,
            failure_hook=failure_hook,
        )

    def pause_active_validation(
        self,
        request: ActiveValidationPauseRequest,
        capability: SyntheticOperatorCapability,
        activity: SyntheticValidatorActivityAttestation,
        *,
        failure_hook: FailureHook | None = None,
    ) -> ControlReceipt:
        def authorize(
            current_state: LifecycleState, resulting_state: LifecycleState
        ) -> None:
            self._engine.authorize(
                "T08", current_state, resulting_state,
                TRANSITIONS["T08"].required_guards,
            )

        return self._store.pause_active_validation(
            request, capability, activity, self._authority,
            authorize_transition=authorize, failure_hook=failure_hook,
        )

    def settle_validation_pause(
        self,
        request: ValidationPauseSettlementRequest,
        *,
        failure_hook: FailureHook | None = None,
    ) -> ControlReceipt:
        def authorize(
            current_state: LifecycleState, resulting_state: LifecycleState
        ) -> None:
            self._engine.authorize(
                "T07", current_state, resulting_state,
                TRANSITIONS["T07"].required_guards,
            )

        return self._store.settle_validation_pause(
            request, authorize_transition=authorize,
            failure_hook=failure_hook,
        )

    def resume_settled_validation_pause(
        self,
        request: ResumeSettledValidationPauseRequest,
        capability: SyntheticOperatorCapability,
        evidence: SyntheticSettledValidationResumeEvidence,
        *,
        failure_hook: FailureHook | None = None,
    ) -> ControlReceipt:
        def authorize(
            current_state: LifecycleState, resulting_state: LifecycleState
        ) -> None:
            self._engine.authorize(
                "T14", current_state, resulting_state,
                TRANSITIONS["T14"].required_guards,
            )

        return self._store.resume_settled_validation_pause(
            request, capability, evidence, self._authority,
            authorize_transition=authorize, failure_hook=failure_hook,
        )

    def recover_settled_validation_pause(
        self,
        request: SettledValidationPauseRecoveryRequest,
        attestation: SyntheticSettledValidationPauseRecoveryAttestation,
        *,
        failure_hook: FailureHook | None = None,
    ):
        return self._store.recover_settled_validation_pause(
            request, attestation, self._authority,
            failure_hook=failure_hook,
        )

    def pause_reconciliation(
        self,
        request: PauseReconciliationRequest,
        capability: SyntheticOperatorCapability,
        *,
        failure_hook: FailureHook | None = None,
    ) -> ControlReceipt:
        def authorize(
            current_state: LifecycleState, resulting_state: LifecycleState
        ) -> None:
            self._engine.authorize(
                "T09",
                current_state,
                resulting_state,
                TRANSITIONS["T09"].required_guards,
            )

        return self._store.pause_reconciliation(
            request,
            capability,
            self._authority,
            authorize_transition=authorize,
            failure_hook=failure_hook,
        )

    def settle_activity_pause(
        self,
        request: PauseActivitySettlementRequest,
        *,
        failure_hook: FailureHook | None = None,
    ) -> ControlReceipt:
        def authorize(
            current_state: LifecycleState, resulting_state: LifecycleState
        ) -> None:
            self._engine.authorize(
                "T07",
                current_state,
                resulting_state,
                TRANSITIONS["T07"].required_guards,
            )

        return self._store.settle_activity_pause(
            request,
            authorize_transition=authorize,
            failure_hook=failure_hook,
        )

    def resume_activity_settlement(
        self,
        request: ResumeActivitySettlementRequest,
        capability: SyntheticOperatorCapability,
        resume_evidence: SyntheticActivityResumeEvidence,
        *,
        failure_hook: FailureHook | None = None,
    ) -> ControlReceipt:
        def authorize(
            current_state: LifecycleState, resulting_state: LifecycleState
        ) -> None:
            self._engine.authorize(
                "T14",
                current_state,
                resulting_state,
                TRANSITIONS["T14"].required_guards,
            )

        return self._store.resume_activity_settlement(
            request,
            capability,
            resume_evidence,
            self._authority,
            authorize_transition=authorize,
            failure_hook=failure_hook,
        )

    def resume_operation_nonexecution(
        self,
        request: ResumeOperationNonexecutionRequest,
        capability: SyntheticOperatorCapability,
        resume_evidence: SyntheticOperationNonexecutionResumeEvidence,
        *,
        failure_hook: FailureHook | None = None,
    ) -> ControlReceipt:
        def authorize(
            current_state: LifecycleState, resulting_state: LifecycleState
        ) -> None:
            self._engine.authorize(
                "T14", current_state, resulting_state,
                TRANSITIONS["T14"].required_guards,
            )

        return self._store.resume_operation_nonexecution(
            request,
            capability,
            resume_evidence,
            self._authority,
            authorize_transition=authorize,
            failure_hook=failure_hook,
        )

    def recover_proven_nonexecution(
        self,
        request: RecoverProvenNonexecutionRequest,
        capability: SyntheticOperatorCapability,
        *,
        failure_hook: FailureHook | None = None,
    ) -> ControlReceipt:
        def authorize(
            current_state: LifecycleState, resulting_state: LifecycleState
        ) -> None:
            self._engine.authorize(
                "T16", current_state, resulting_state,
                TRANSITIONS["T16"].required_guards,
            )

        return self._store.recover_proven_nonexecution(
            request,
            capability,
            self._authority,
            authorize_transition=authorize,
            failure_hook=failure_hook,
        )

    def authorize_safe_same_effect_retry(
        self,
        request: AuthorizeSafeSameEffectRetryRequest,
        capability: SyntheticOperatorCapability,
        evidence: SyntheticSafeSameEffectRetryEvidence,
        source_control_evidence: SyntheticSafeRetrySourceControlEvidence,
        *,
        failure_hook: FailureHook | None = None,
    ) -> ControlReceipt:
        return self._store.authorize_safe_same_effect_retry(
            request, capability, evidence, source_control_evidence,
            self._authority,
            failure_hook=failure_hook,
        )

    def resume(
        self,
        request: ResumeRequest,
        capability: SyntheticOperatorCapability,
        resume_evidence: SyntheticResumeEvidence,
        *,
        failure_hook: FailureHook | None = None,
    ) -> ControlReceipt:
        def authorize(
            current_state: LifecycleState, resulting_state: LifecycleState
        ) -> None:
            self._engine.authorize(
                "T14",
                current_state,
                resulting_state,
                TRANSITIONS["T14"].required_guards,
            )

        return self._store.resume(
            request,
            capability,
            resume_evidence,
            self._authority,
            authorize_transition=authorize,
            failure_hook=failure_hook,
        )

    def resume_reconciliation_pause(
        self,
        request: ReconciliationPauseResumeRequest,
        capability: SyntheticOperatorCapability,
        resume_evidence: SyntheticReconciliationResumeEvidence,
        *,
        failure_hook: FailureHook | None = None,
    ) -> ControlReceipt:
        def authorize(
            current_state: LifecycleState, resulting_state: LifecycleState
        ) -> None:
            self._engine.authorize(
                "T14", current_state, resulting_state,
                TRANSITIONS["T14"].required_guards,
            )

        return self._store.resume_reconciliation_pause(
            request, capability, resume_evidence, self._authority,
            authorize_transition=authorize, failure_hook=failure_hook,
        )

    def record_authority_fact(
        self,
        request: AuthorityLifecycleFactRequest,
        evidence: SyntheticAuthorityLifecycleEvidence,
        *,
        expected_head: str,
        writer_epoch: int,
        failure_hook: FailureHook | None = None,
    ) -> ControlReceipt:
        def authorize(
            current_state: LifecycleState, resulting_state: LifecycleState
        ) -> None:
            self._engine.authorize(
                "T13", current_state, resulting_state,
                TRANSITIONS["T13"].required_guards,
            )

        return self._store.record_authority_fact(
            request, evidence, self._authority,
            expected_head=expected_head,
            writer_epoch=writer_epoch,
            authorize_transition=authorize,
            failure_hook=failure_hook,
        )

    def record_binding_mismatch(
        self,
        request: BindingMismatchRequest,
        observation: SyntheticBindingObservation,
        *,
        expected_head: str,
        writer_epoch: int,
        failure_hook: FailureHook | None = None,
    ) -> ControlReceipt:
        def authorize(
            current_state: LifecycleState, resulting_state: LifecycleState
        ) -> None:
            self._engine.authorize(
                "T15", current_state, resulting_state,
                TRANSITIONS["T15"].required_guards,
            )

        return self._store.record_binding_mismatch(
            request, observation, self._authority,
            expected_head=expected_head,
            writer_epoch=writer_epoch,
            authorize_transition=authorize,
            failure_hook=failure_hook,
        )

    def escalate_stop(
        self,
        request: StopEscalationRequest,
        capability: SyntheticOperatorCapability,
        *,
        failure_hook: FailureHook | None = None,
    ) -> ControlReceipt:
        def authorize(
            current_state: LifecycleState, resulting_state: LifecycleState
        ) -> None:
            self._engine.authorize(
                "T20",
                current_state,
                resulting_state,
                TRANSITIONS["T20"].required_guards,
            )

        return self._store.escalate_stop(
            request,
            capability,
            self._authority,
            authorize_transition=authorize,
            failure_hook=failure_hook,
        )

    def dispatch(
        self,
        intent: IntentRequest,
        capability: SyntheticCapability,
        effect: SyntheticEffectRequest,
        *,
        expected_head: str,
        writer_epoch: int,
        usage_units: int | None = 0,
        lose_receipt: bool = False,
    ) -> SyntheticDispatchReceipt:
        require_synthetic_dispatch(self._authority, self._adapter)
        if not self._adapter.is_canonical_for(intent.repository_id):
            raise DispatchDenied(
                "synthetic target is not the canonical repository root"
            )
        intent.validate()
        effect.validate()
        if usage_units is not None and (
            type(usage_units) is not int or usage_units < 0
        ):
            raise ValueError("usage_units must be non-negative or unknown")
        self._engine.authorize(
            "T03",
            LifecycleState.PLANNED,
            LifecycleState.RUNNING,
            TRANSITIONS["T03"].required_guards,
        )
        self._authority.verify_issued(capability)
        self._adapter._validate_request_binding(capability, effect, intent)
        commit = self._store.commit_intent(
            intent,
            capability,
            self._authority,
            expected_head=expected_head,
            writer_epoch=writer_epoch,
        )
        if commit.replayed:
            raise DispatchDenied("synthetic capability was already redeemed")
        launch = self._store.claim_operation_launch(intent, commit)
        if launch.replayed:
            raise DispatchDenied("operation launch was already claimed")
        receipt = self._adapter._execute_committed(
            capability,
            effect,
            self._authority,
            self._store,
            commit,
            launch,
            intent,
            usage_units=usage_units,
            lose_receipt=lose_receipt,
        )
        return SyntheticDispatchReceipt(commit, receipt)

    def dispatch_proven_nonexecution_retry(
        self,
        intent: ProvenNonexecutionIntentRequest,
        capability: SyntheticCapability,
        effect: SyntheticEffectRequest,
        *,
        expected_head: str,
        writer_epoch: int,
        usage_units: int | None = 0,
        lose_receipt: bool = False,
    ) -> SyntheticDispatchReceipt:
        return self.dispatch(
            intent,
            capability,
            effect,
            expected_head=expected_head,
            writer_epoch=writer_epoch,
            usage_units=usage_units,
            lose_receipt=lose_receipt,
        )

    def intake_effect_receipt(
        self,
        command: EffectObservationCommand,
        *,
        source_control_classification: SourceControlClassification = (
            SourceControlClassification.KNOWN
        ),
        source_control_evidence: SyntheticSourceControlEvidence | None = None,
        failure_hook: FailureHook | None = None,
    ) -> ObservationReceipt:
        command.validate()
        if command.settlement_hash:
            raise DispatchDenied(
                "canonical observation intake derives its settlement hash"
            )
        if command.repository_id != self._store._repository_id:
            raise DispatchDenied("observation targets a different repository")
        if not self._adapter.is_canonical_for(command.repository_id):
            raise DispatchDenied(
                "synthetic target is not the canonical repository root"
            )
        receipt = self._adapter.reconcile(command.source_claim_id)
        if receipt is None or not receipt.accepted:
            raise DispatchDenied("canonical synthetic receipt is unavailable")
        receipt_binding = (
            receipt.repository_id,
            receipt.run_id,
            receipt.item_id,
            receipt.logical_effect_id,
            receipt.attempt_id,
        )
        command_binding = (
            command.repository_id,
            command.run_id,
            command.item_id,
            command.logical_effect_id,
            command.attempt_id,
        )
        if receipt_binding != command_binding:
            raise DispatchDenied("canonical receipt does not bind this observation")
        evidence_request = SourceControlEvidenceRequest(
            repository_id=receipt.repository_id,
            run_id=receipt.run_id,
            item_id=receipt.item_id,
            logical_effect_id=receipt.logical_effect_id,
            attempt_id=receipt.attempt_id,
            source_claim_id=receipt.claim_id,
            source_receipt_id=receipt.receipt_id,
            payload_digest=receipt.payload_digest,
            usage_units=receipt.usage_units,
            accepted=receipt.accepted,
            classification=source_control_classification,
        )
        evidence_request.validate()
        if source_control_evidence is None:
            if source_control_classification is not SourceControlClassification.KNOWN:
                raise DispatchDenied(
                    "unknown source/control classification requires explicit evidence"
                )
            source_control_evidence = self._authority.issue_source_control_evidence(
                f"source-control:{receipt.receipt_id}", evidence_request
            )
        self._authority.verify_source_control_evidence(
            source_control_evidence, evidence_request
        )
        resulting_state = (
            LifecycleState.RECONCILIATION_REQUIRED
            if (
                receipt.usage_units is None
                or source_control_classification
                is SourceControlClassification.UNKNOWN
            )
            else LifecycleState.VALIDATING
        )
        self._engine.authorize(
            "T10",
            LifecycleState.RUNNING,
            resulting_state,
            TRANSITIONS["T10"].required_guards,
        )
        return self._store._record_effect_observation(
            EffectObservationRequest(
                observation_id=command.observation_id,
                command_id=command.command_id,
                event_id=command.event_id,
                repository_id=command.repository_id,
                run_id=command.run_id,
                item_id=command.item_id,
                logical_effect_id=command.logical_effect_id,
                attempt_id=command.attempt_id,
                source_receipt_id=receipt.receipt_id,
                source_claim_id=receipt.claim_id,
                payload_digest=receipt.payload_digest,
                usage_units=receipt.usage_units,
                settlement_event_id=command.settlement_event_id,
                settlement_hash="",
                source_control_classification=(
                    source_control_classification.value
                ),
                source_control_evidence_id=source_control_evidence.evidence_id,
                source_control_evidence_digest=(
                    source_control_evidence.request_digest
                ),
                source_control_issuer_fingerprint=(
                    source_control_evidence.issuer_fingerprint
                ),
                source_control_issuer_mac=source_control_evidence.issuer_mac,
            ),
            authority=self._authority,
            failure_hook=failure_hook,
        )

    def reconcile_verified_receipt(
        self,
        request: ReconcileVerifiedReceiptRequest,
        *,
        failure_hook: FailureHook | None = None,
    ) -> ControlReceipt:
        """Resolve operation uncertainty from one durable verified receipt."""
        request.validate()
        evidence = SyntheticSourceControlSettlementEvidence(
            evidence_id=request.source_control_evidence_id,
            request_digest=request.source_control_evidence_digest,
            issuer_fingerprint=request.source_control_issuer_fingerprint,
            issuer_mac=request.source_control_issuer_mac,
        )
        self._authority.verify_source_control_settlement_evidence(
            evidence,
            self._store._source_control_settlement_request(request),
        )

        def authorize(
            current_state: LifecycleState, resulting_state: LifecycleState
        ) -> None:
            self._engine.authorize(
                "T17",
                current_state,
                resulting_state,
                TRANSITIONS["T17"].required_guards,
            )

        return self._store.reconcile_verified_receipt(
            request,
            authorize_transition=authorize,
            failure_hook=failure_hook,
        )


class SyntheticValidationCoordinator:
    """Commit a validator sub-intent, then use only its canonical result ledger."""

    def __init__(
        self,
        store: SQLiteStateStore,
        engine: TransitionEngine,
        authority: SyntheticAuthority,
        adapter: SyntheticValidatorAdapter,
    ) -> None:
        if not store.is_canonical:
            raise DispatchDenied("validation store is not the canonical repository root")
        self._store = store
        self._engine = engine
        self._authority = authority
        self._adapter = adapter
        self._store._bind_classification_authority(authority)

    def launch_prepared(
        self,
        intent: ValidatorIntentRequest,
        *,
        grant_id: str,
        scope_digest: str,
        launch_snapshot: SyntheticValidationLaunchSnapshot,
        request: SyntheticValidatorRequest,
        usage_units: int | None = 0,
        lose_result: bool = False,
    ) -> SyntheticValidationReceipt:
        """Launch from an unclaimed grant and a durable READY snapshot."""
        require_synthetic_validation(self._authority, self._adapter)
        if not self._adapter.is_canonical_for(intent.repository_id):
            raise DispatchDenied(
                "synthetic validator is not the canonical repository root"
            )
        intent.validate()
        request.validate()
        if usage_units is not None and (
            type(usage_units) is not int or usage_units < 0
        ):
            raise ValueError("usage_units must be non-negative or unknown")
        self._engine.authorize(
            "T27",
            LifecycleState.VALIDATING,
            LifecycleState.VALIDATING,
            TRANSITIONS["T27"].required_guards,
        )
        containment_digest = validator_containment_digest(
            parse_validator_containment_spec(intent.containment_spec_json)
        )
        if (
            request.repository_id,
            request.logical_effect_id,
            request.revision_digest,
            request.check_id,
            request.input_digest,
            request.validator_attempt_id,
            request.scope_digest,
            request.containment_digest,
        ) != (
            intent.repository_id,
            intent.logical_effect_id,
            intent.revision_digest,
            intent.check_id,
            intent.input_digest,
            intent.validator_attempt_id,
            scope_digest,
            containment_digest,
        ):
            raise DispatchDenied(
                "synthetic validator request does not bind the durable intent"
            )
        commit = self._store.commit_validator_intent(
            intent,
            None,
            self._authority,
            grant_id=grant_id,
            scope_digest=scope_digest,
            launch_snapshot=launch_snapshot,
        )
        if commit.replayed:
            raise DispatchDenied(
                "synthetic validator capability was already redeemed"
            )
        capability = self._authority.claim_or_recover_validator(
            grant_id,
            intent.repository_id,
            intent.logical_effect_id,
            intent.revision_digest,
            intent.check_id,
            intent.input_digest,
            intent.validator_attempt_id,
            scope_digest,
            containment_digest,
        )
        result = self._adapter._execute_committed(
            capability,
            request,
            self._authority,
            self._store,
            commit,
            intent,
            usage_units=usage_units,
            lose_result=lose_result,
        )
        return SyntheticValidationReceipt(commit, result)

    def reconcile_result(
        self,
        request: ReconcileValidatorResultRequest,
        *,
        failure_hook: FailureHook | None = None,
    ) -> ControlReceipt:
        request.validate()

        def authorize(
            current_state: LifecycleState, resulting_state: LifecycleState
        ) -> None:
            self._engine.authorize(
                "T17",
                current_state,
                resulting_state,
                TRANSITIONS["T17"].required_guards,
            )

        return self._store.reconcile_validator_result(
            request,
            authorize_transition=authorize,
            failure_hook=failure_hook,
        )

    def record_proof_free_disposition(
        self,
        request: ProofFreeDispositionRequest,
        capability: SyntheticOperatorCapability,
        evidence: SyntheticProofFreeDispositionEvidence,
        *,
        failure_hook: FailureHook | None = None,
    ) -> ControlReceipt:
        request.validate()

        def authorize(
            current_state: LifecycleState, resulting_state: LifecycleState
        ) -> None:
            self._engine.authorize(
                "T17", current_state, resulting_state,
                TRANSITIONS["T17"].required_guards,
            )

        return self._store.record_proof_free_disposition(
            request, capability, evidence, self._authority,
            authorize_transition=authorize,
            failure_hook=failure_hook,
        )

    def intake_result(
        self,
        command: ValidatorObservationCommand,
        *,
        failure_hook: FailureHook | None = None,
    ) -> ObservationReceipt:
        command.validate()
        if not self._adapter.is_canonical_for(command.repository_id):
            raise DispatchDenied(
                "synthetic validator is not the canonical repository root"
            )
        binding = self._store.load_validator_intent_binding(
            command.validator_intent_id, require_active=False
        )
        if (
            binding.repository_id,
            binding.run_id,
            binding.item_id,
        ) != (
            command.repository_id,
            command.run_id,
            command.item_id,
        ):
            raise DispatchDenied("validator command does not bind the durable intent")
        result = self._adapter.reconcile(binding.capability_claim_id)
        if result is None or not result.final:
            raise DispatchDenied("canonical final validator result is unavailable")
        current_state = self._store.load_run_lifecycle(command.run_id)
        resulting_state = (
            LifecycleState.RECONCILIATION_REQUIRED
            if result.usage_units is None
            else current_state
        )
        self._engine.authorize(
            "T24",
            current_state,
            resulting_state,
            TRANSITIONS["T24"].required_guards,
        )
        return self._store._record_validator_observation(
            ValidatorObservationRequest(
                command.observation_id, command.command_id, command.event_id,
                command.repository_id, command.run_id, command.item_id,
                binding.logical_effect_id, binding.validator_intent_id,
                binding.validator_attempt_id, result.result_id, result.claim_id,
                binding.revision_digest, binding.check_id, binding.input_digest,
                result.result_digest, result.verdict, result.usage_units,
                command.settlement_event_id, command.settlement_hash,
                result.containment_digest,
            ),
            failure_hook=failure_hook,
        )

    def apply_result(
        self,
        request: ValidationApplicationRequest,
        *,
        classification: SyntheticClassificationEvidence | None = None,
        failure_hook: FailureHook | None = None,
    ) -> ApplicationReceipt:
        return self._store._apply_validator_observation(
            request,
            classification=classification,
            failure_hook=failure_hook,
        )


class SyntheticFinalizationCoordinator:
    """Complete an operation only from attested, reconstructed durable state."""

    def __init__(
        self,
        store: SQLiteStateStore,
        engine: TransitionEngine,
        authority: SyntheticAuthority,
    ) -> None:
        if not store.is_canonical:
            raise DispatchDenied(
                "finalization store is not the canonical repository root"
            )
        self._store = store
        self._engine = engine
        self._authority = authority
        self._store._bind_classification_authority(authority)

    def finalize(
        self,
        request: FinalizeOperationRequest,
        attestation: SyntheticFinalizationAttestation,
        *,
        failure_hook: FailureHook | None = None,
    ) -> OperationFinalizationReceipt:
        self._engine.authorize(
            "T16", LifecycleState.BLOCKED, LifecycleState.COMPLETED,
            TRANSITIONS["T16"].required_guards,
        )
        return self._store._finalize_operation(
            request, attestation, self._authority, failure_hook=failure_hook
        )
