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
)
from .authority import (
    SyntheticAuthority,
    SyntheticAuthorityLifecycleEvidence,
    SyntheticBindingObservation,
    SyntheticCapability,
    SyntheticClassificationEvidence,
    SyntheticFinalizationAttestation,
    SyntheticOperatorCapability,
    SyntheticResumeEvidence,
    SyntheticValidatorCapability,
)
from .contracts import (
    ApplicationReceipt,
    AuthorityLifecycleFactRequest,
    BindingMismatchRequest,
    CommitReceipt,
    ControlReceipt,
    DispatchDenied,
    EffectObservationCommand,
    EffectObservationRequest,
    FinalizeOperationRequest,
    IntentRequest,
    LifecycleState,
    ObservationReceipt,
    OperationFinalizationReceipt,
    PauseBeforeDispatchRequest,
    ResumeRequest,
    StopMode,
    StopEscalationRequest,
    StopRequest,
    ValidationApplicationRequest,
    ValidatorIntentRequest,
    ValidatorObservationCommand,
    ValidatorObservationRequest,
)
from .engine import TRANSITIONS, TransitionEngine
from .storage import FailureHook, SQLiteStateStore


@dataclass(frozen=True)
class SyntheticDispatchReceipt:
    intent: CommitReceipt
    effect: SyntheticReceipt | None


@dataclass(frozen=True)
class SyntheticValidationReceipt:
    intent: CommitReceipt
    result: SyntheticValidatorResult | None


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

    def intake_effect_receipt(
        self,
        command: EffectObservationCommand,
        *,
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
        resulting_state = (
            LifecycleState.RECONCILIATION_REQUIRED
            if receipt.usage_units is None
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
            ),
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

    def launch(
        self,
        intent: ValidatorIntentRequest,
        capability: SyntheticValidatorCapability,
        request: SyntheticValidatorRequest,
        *,
        usage_units: int | None = 0,
        lose_result: bool = False,
    ) -> SyntheticValidationReceipt:
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
        self._authority.verify_validator_issued(capability)
        self._adapter._validate_request_binding(capability, request, intent)
        commit = self._store.commit_validator_intent(
            intent, capability, self._authority
        )
        if commit.replayed:
            raise DispatchDenied(
                "synthetic validator capability was already redeemed"
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
