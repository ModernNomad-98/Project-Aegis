"""Single mediated path for synthetic effect dispatch."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

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
    SyntheticCapability,
    SyntheticValidatorCapability,
)
from .contracts import (
    CommitReceipt,
    DispatchDenied,
    EffectObservationCommand,
    EffectObservationRequest,
    IntentRequest,
    LifecycleState,
    ObservationReceipt,
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
        self._store = store
        self._engine = engine
        self._authority = authority
        self._adapter = adapter

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
        before_adapter_hook: Callable[[], None] | None = None,
    ) -> SyntheticDispatchReceipt:
        if not self._adapter.is_canonical_for(intent.repository_id):
            raise DispatchDenied(
                "synthetic target is not the canonical repository root"
            )
        intent.validate()
        self._engine.authorize(
            "T03",
            LifecycleState.PLANNED,
            LifecycleState.RUNNING,
            TRANSITIONS["T03"].required_guards,
        )
        if effect.payload_digest != intent.effect_descriptor_digest:
            raise DispatchDenied("effect payload does not match the committed descriptor")
        commit = self._store.commit_intent(
            intent,
            capability,
            self._authority,
            expected_head=expected_head,
            writer_epoch=writer_epoch,
        )
        if commit.replayed:
            raise DispatchDenied("synthetic capability was already redeemed")
        if before_adapter_hook is not None:
            before_adapter_hook()
        receipt = self._adapter._execute_committed(
            capability,
            effect,
            self._authority,
            commit,
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
            receipt.logical_effect_id,
            receipt.attempt_id,
        )
        command_binding = (
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
        return self._store.record_effect_observation(
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
                settlement_hash=command.settlement_hash,
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
        self._engine.authorize(
            "T27",
            LifecycleState.VALIDATING,
            LifecycleState.VALIDATING,
            TRANSITIONS["T27"].required_guards,
        )
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
            commit,
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
            command.validator_intent_id
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
        return self._store.record_validator_observation(
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