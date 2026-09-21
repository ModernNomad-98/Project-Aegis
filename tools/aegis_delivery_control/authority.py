"""Synthetic-only one-use authority for offline kernel testing."""

from __future__ import annotations

import hashlib
import hmac
import json
import secrets
import threading
from dataclasses import dataclass

from .contracts import (
    AuthorityLifecycleFactRequest,
    BindingMismatchRequest,
    BudgetSettlementRequest,
    DispatchDenied,
    FailureClassification,
    ReconciliationPauseResumeRequest,
    ResumeActivitySettlementRequest,
    ResumeRequest,
)

SYNTHETIC_FAILURE_POLICY_ID = "failure-policy"
SYNTHETIC_FAILURE_POLICY_VERSION = "1"
SYNTHETIC_FINALIZATION_POLICY_ID = "finalization-policy"
SYNTHETIC_FINALIZATION_POLICY_VERSION = "1"
SYNTHETIC_VALIDATION_RECOVERY_POLICY_ID = "validation-recovery-policy"
SYNTHETIC_VALIDATION_RECOVERY_POLICY_VERSION = "1"
SYNTHETIC_NONEXECUTION_POLICY_ID = "nonexecution-policy"
SYNTHETIC_NONEXECUTION_POLICY_VERSION = "1"
SYNTHETIC_VALIDATOR_CESSATION_POLICY_ID = "validator-cessation-policy"
SYNTHETIC_VALIDATOR_CESSATION_POLICY_VERSION = "1"


@dataclass(frozen=True)
class SyntheticGrant:
    grant_id: str
    repository_id: str
    logical_effect_id: str
    attempt_id: str
    scope_digest: str


@dataclass(frozen=True)
class SyntheticCapability:
    claim_id: str
    grant_id: str
    repository_id: str
    logical_effect_id: str
    attempt_id: str
    scope_digest: str
    issuer_mac: str


@dataclass(frozen=True)
class SyntheticValidatorGrant:
    grant_id: str
    repository_id: str
    logical_effect_id: str
    revision_digest: str
    check_id: str
    input_digest: str
    validator_attempt_id: str
    scope_digest: str


@dataclass(frozen=True)
class SyntheticValidatorCapability:
    claim_id: str
    grant_id: str
    repository_id: str
    logical_effect_id: str
    revision_digest: str
    check_id: str
    input_digest: str
    validator_attempt_id: str
    scope_digest: str
    issuer_mac: str


@dataclass(frozen=True)
class SyntheticOperatorGrant:
    grant_id: str
    repository_id: str
    run_id: str
    action: str
    scope_digest: str


@dataclass(frozen=True)
class SyntheticOperatorCapability:
    claim_id: str
    grant_id: str
    repository_id: str
    run_id: str
    action: str
    scope_digest: str
    issuer_mac: str


@dataclass(frozen=True)
class SyntheticSettlementProof:
    proof_id: str
    reservation_id: str
    non_dispatch_proven: bool
    zero_liability_proven: bool
    all_obligations_settled: bool
    request_digest: str
    issuer_mac: str


@dataclass(frozen=True)
class SyntheticClassificationEvidence:
    """Issuer-verifiable T12 evidence binding a FAIL observation to a disposition."""

    classification_id: str
    repository_id: str
    run_id: str
    item_id: str
    logical_effect_id: str
    revision_digest: str
    check_id: str
    validator_attempt_id: str
    observation_id: str
    observation_event_hash: str
    result_digest: str
    verdict: str
    policy_id: str
    policy_version: str
    classification: str
    issuer_mac: str


@dataclass(frozen=True)
class SyntheticFinalizationAttestation:
    attestation_id: str
    repository_id: str
    run_id: str
    item_id: str
    logical_effect_id: str
    plan_id: str
    plan_event_hash: str
    revision_digest: str
    evaluated_run_head: str
    finalization_key: str
    gate_set_digest: str
    slot_attempt_id: str
    slot_generation: int
    verdict: str
    policy_id: str
    policy_version: str
    issuer_mac: str


@dataclass(frozen=True)
class SyntheticValidationRecoveryAttestation:
    attestation_id: str
    recovery_id: str
    repository_id: str
    run_id: str
    item_id: str
    logical_effect_id: str
    plan_id: str
    plan_event_hash: str
    revision_digest: str
    check_id: str
    failed_application_id: str
    failed_application_event_hash: str
    failed_validator_attempt_id: str
    successor_validator_attempt_id: str
    remediation_evidence_digest: str
    evaluated_run_head: str
    slot_attempt_id: str
    slot_generation: int
    action: str
    policy_id: str
    policy_version: str
    issuer_mac: str


@dataclass(frozen=True)
class SyntheticNonexecutionAttestation:
    attestation_id: str
    seal_id: str
    contact_kind: str
    target_digest: str
    claim_id: str
    source_id: str
    source_event_hash: str
    reservation_id: str
    repository_id: str
    run_id: str
    item_id: str
    logical_effect_id: str
    attempt_id: str
    action: str
    policy_id: str
    policy_version: str
    issuer_mac: str


@dataclass(frozen=True)
class SyntheticValidatorCessationAttestation:
    attestation_id: str
    cessation_id: str
    target_digest: str
    claim_id: str
    source_id: str
    source_event_hash: str
    repository_id: str
    run_id: str
    item_id: str
    logical_effect_id: str
    revision_digest: str
    check_id: str
    validator_attempt_id: str
    action: str
    policy_id: str
    policy_version: str
    issuer_mac: str


@dataclass(frozen=True)
class SyntheticAuthorityLifecycleEvidence:
    proof_id: str
    request_digest: str
    issuer_fingerprint: str
    issuer_mac: str


@dataclass(frozen=True)
class SyntheticBindingObservation:
    observation_id: str
    request_digest: str
    issuer_fingerprint: str
    issuer_mac: str


@dataclass(frozen=True)
class SyntheticResumeEvidence:
    proof_id: str
    request_digest: str
    issuer_fingerprint: str
    issuer_mac: str


@dataclass(frozen=True)
class SyntheticActivityResumeEvidence:
    proof_id: str
    request_digest: str
    issuer_fingerprint: str
    issuer_mac: str


@dataclass(frozen=True)
class SyntheticReconciliationResumeEvidence:
    proof_id: str
    request_digest: str
    issuer_fingerprint: str
    issuer_mac: str


class SyntheticAuthority:
    """Atomically claim in-memory test grants; never authenticates real authority."""

    def __init__(self, issuer_key: bytes | None = None) -> None:
        if issuer_key is not None and len(issuer_key) < 32:
            raise ValueError("synthetic issuer key must contain at least 32 bytes")
        self._lock = threading.Lock()
        self._issuer_key = issuer_key if issuer_key is not None else secrets.token_bytes(32)
        self._grants: dict[str, SyntheticGrant] = {}
        self._claims: dict[str, SyntheticCapability] = {}
        self._validator_grants: dict[str, SyntheticValidatorGrant] = {}
        self._validator_claims: dict[str, SyntheticValidatorCapability] = {}
        self._operator_grants: dict[str, SyntheticOperatorGrant] = {}
        self._operator_claims: dict[str, SyntheticOperatorCapability] = {}
        self._committed_claims: set[str] = set()

    def _mac(self, domain: str, **fields: object) -> str:
        encoded = json.dumps(
            {"domain": domain, "fields": fields, "version": 1},
            ensure_ascii=True,
            separators=(",", ":"),
            sort_keys=True,
        ).encode("utf-8")
        return hmac.new(
            self._issuer_key, encoded, hashlib.sha256
        ).hexdigest()

    @property
    def issuer_fingerprint(self) -> str:
        return hashlib.sha256(self._issuer_key).hexdigest()

    @staticmethod
    def _authority_fact_digest(request: AuthorityLifecycleFactRequest) -> str:
        payload = {
            **request.__dict__,
            "fact_kind": request.fact_kind.value,
            "governed_order": request.governed_order.value,
        }
        return hashlib.sha256(
            json.dumps(
                payload, ensure_ascii=True, separators=(",", ":"), sort_keys=True
            ).encode("utf-8")
        ).hexdigest()

    @staticmethod
    def _binding_mismatch_digest(request: BindingMismatchRequest) -> str:
        return hashlib.sha256(
            json.dumps(
                {
                    **request.__dict__,
                    "mismatch_kind": request.mismatch_kind.value,
                },
                ensure_ascii=True,
                separators=(",", ":"),
                sort_keys=True,
            ).encode("utf-8")
        ).hexdigest()

    @staticmethod
    def _resume_request_digest(request: ResumeRequest) -> str:
        return hashlib.sha256(
            json.dumps(
                {
                    **request.__dict__,
                    "expected_preserved_lifecycle": (
                        request.expected_preserved_lifecycle.value
                    ),
                },
                ensure_ascii=True,
                separators=(",", ":"),
                sort_keys=True,
            ).encode("utf-8")
        ).hexdigest()

    def issue_resume_evidence(
        self, proof_id: str, request: ResumeRequest
    ) -> SyntheticResumeEvidence:
        request.validate()
        if not isinstance(proof_id, str) or not proof_id.strip():
            raise ValueError("resume evidence proof ID must be non-empty")
        request_digest = self._resume_request_digest(request)
        return SyntheticResumeEvidence(
            proof_id,
            request_digest,
            self.issuer_fingerprint,
            self._mac(
                "RESUME_EVIDENCE",
                proof_id=proof_id,
                request_digest=request_digest,
                issuer_fingerprint=self.issuer_fingerprint,
            ),
        )

    def verify_resume_evidence(
        self,
        evidence: SyntheticResumeEvidence,
        request: ResumeRequest,
    ) -> None:
        request.validate()
        if any(
            not isinstance(value, str) or not value.strip()
            for value in evidence.__dict__.values()
        ):
            raise DispatchDenied("resume evidence is malformed")
        request_digest = self._resume_request_digest(request)
        expected_mac = self._mac(
            "RESUME_EVIDENCE",
            proof_id=evidence.proof_id,
            request_digest=request_digest,
            issuer_fingerprint=self.issuer_fingerprint,
        )
        if (
            evidence.request_digest != request_digest
            or evidence.issuer_fingerprint != self.issuer_fingerprint
            or not hmac.compare_digest(evidence.issuer_mac, expected_mac)
        ):
            raise DispatchDenied("resume evidence was not issued here")

    @staticmethod
    def _activity_resume_request_digest(
        request: ResumeActivitySettlementRequest,
    ) -> str:
        return hashlib.sha256(
            json.dumps(
                request.__dict__, ensure_ascii=True,
                separators=(",", ":"), sort_keys=True,
            ).encode("utf-8")
        ).hexdigest()

    def issue_activity_resume_evidence(
        self, proof_id: str, request: ResumeActivitySettlementRequest
    ) -> SyntheticActivityResumeEvidence:
        request.validate()
        if not isinstance(proof_id, str) or not proof_id.strip():
            raise ValueError(
                "activity resume evidence proof ID must be non-empty"
            )
        request_digest = self._activity_resume_request_digest(request)
        return SyntheticActivityResumeEvidence(
            proof_id,
            request_digest,
            self.issuer_fingerprint,
            self._mac(
                "ACTIVITY_RESUME_EVIDENCE",
                proof_id=proof_id,
                request_digest=request_digest,
                issuer_fingerprint=self.issuer_fingerprint,
            ),
        )

    def verify_activity_resume_evidence(
        self,
        evidence: SyntheticActivityResumeEvidence,
        request: ResumeActivitySettlementRequest,
    ) -> None:
        request.validate()
        if any(
            not isinstance(value, str) or not value.strip()
            for value in evidence.__dict__.values()
        ):
            raise DispatchDenied("activity resume evidence is malformed")
        request_digest = self._activity_resume_request_digest(request)
        expected_mac = self._mac(
            "ACTIVITY_RESUME_EVIDENCE",
            proof_id=evidence.proof_id,
            request_digest=request_digest,
            issuer_fingerprint=self.issuer_fingerprint,
        )
        if (
            evidence.request_digest != request_digest
            or evidence.issuer_fingerprint != self.issuer_fingerprint
            or not hmac.compare_digest(evidence.issuer_mac, expected_mac)
        ):
            raise DispatchDenied(
                "activity resume evidence was not issued here"
            )

    @staticmethod
    def _reconciliation_resume_request_digest(
        request: ReconciliationPauseResumeRequest,
    ) -> str:
        return hashlib.sha256(
            json.dumps(
                request.__dict__, ensure_ascii=True,
                separators=(",", ":"), sort_keys=True,
            ).encode("utf-8")
        ).hexdigest()

    def issue_reconciliation_resume_evidence(
        self, proof_id: str, request: ReconciliationPauseResumeRequest
    ) -> SyntheticReconciliationResumeEvidence:
        request.validate()
        if not isinstance(proof_id, str) or not proof_id.strip():
            raise ValueError(
                "reconciliation resume proof ID must be non-empty"
            )
        request_digest = self._reconciliation_resume_request_digest(request)
        return SyntheticReconciliationResumeEvidence(
            proof_id, request_digest, self.issuer_fingerprint,
            self._mac(
                "RECONCILIATION_PAUSE_RESUME_EVIDENCE",
                proof_id=proof_id,
                request_digest=request_digest,
                issuer_fingerprint=self.issuer_fingerprint,
            ),
        )

    def verify_reconciliation_resume_evidence(
        self,
        evidence: SyntheticReconciliationResumeEvidence,
        request: ReconciliationPauseResumeRequest,
    ) -> None:
        request.validate()
        if any(
            not isinstance(value, str) or not value.strip()
            for value in evidence.__dict__.values()
        ):
            raise DispatchDenied("reconciliation resume evidence is malformed")
        request_digest = self._reconciliation_resume_request_digest(request)
        expected_mac = self._mac(
            "RECONCILIATION_PAUSE_RESUME_EVIDENCE",
            proof_id=evidence.proof_id,
            request_digest=request_digest,
            issuer_fingerprint=self.issuer_fingerprint,
        )
        if (
            evidence.request_digest != request_digest
            or evidence.issuer_fingerprint != self.issuer_fingerprint
            or not hmac.compare_digest(evidence.issuer_mac, expected_mac)
        ):
            raise DispatchDenied(
                "reconciliation resume evidence was not issued here"
            )

    def issue_binding_observation(
        self, request: BindingMismatchRequest
    ) -> SyntheticBindingObservation:
        request.validate()
        request_digest = self._binding_mismatch_digest(request)
        return SyntheticBindingObservation(
            request.observation_id,
            request_digest,
            self.issuer_fingerprint,
            self._mac(
                "BINDING_MISMATCH_OBSERVATION",
                observation_id=request.observation_id,
                request_digest=request_digest,
                issuer_fingerprint=self.issuer_fingerprint,
            ),
        )

    def verify_binding_observation(
        self,
        observation: SyntheticBindingObservation,
        request: BindingMismatchRequest,
    ) -> None:
        request.validate()
        if any(
            not isinstance(value, str) or not value.strip()
            for value in observation.__dict__.values()
        ):
            raise DispatchDenied("binding mismatch observation is malformed")
        request_digest = self._binding_mismatch_digest(request)
        expected_mac = self._mac(
            "BINDING_MISMATCH_OBSERVATION",
            observation_id=observation.observation_id,
            request_digest=request_digest,
            issuer_fingerprint=self.issuer_fingerprint,
        )
        if (
            observation.observation_id != request.observation_id
            or observation.request_digest != request_digest
            or observation.issuer_fingerprint != self.issuer_fingerprint
            or not hmac.compare_digest(observation.issuer_mac, expected_mac)
        ):
            raise DispatchDenied("binding mismatch observation was not issued here")

    def issue_authority_lifecycle_evidence(
        self, proof_id: str, request: AuthorityLifecycleFactRequest
    ) -> SyntheticAuthorityLifecycleEvidence:
        request.validate()
        self.verify_authority_fact_binding(request)
        if not proof_id.strip():
            raise ValueError("authority lifecycle proof ID must be non-empty")
        digest = self._authority_fact_digest(request)
        return SyntheticAuthorityLifecycleEvidence(
            proof_id,
            digest,
            self.issuer_fingerprint,
            self._mac(
                "AUTHORITY_LIFECYCLE_EVIDENCE",
                proof_id=proof_id,
                request_digest=digest,
                issuer_fingerprint=self.issuer_fingerprint,
            ),
        )

    def verify_authority_fact_binding(
        self, request: AuthorityLifecycleFactRequest
    ) -> None:
        request.validate()
        with self._lock:
            if request.grant_kind == "EFFECT":
                grant = self._grants.get(request.grant_id)
                binding = (
                    grant.repository_id, grant.logical_effect_id,
                    "EXECUTE_EFFECT", grant.scope_digest,
                ) if grant is not None else None
                requested = (
                    request.repository_id, request.logical_effect_id,
                    request.action, request.scope_digest,
                )
                grants: dict[str, object] = self._grants
            elif request.grant_kind == "VALIDATOR":
                grant = self._validator_grants.get(request.grant_id)
                binding = (
                    grant.repository_id, grant.logical_effect_id,
                    "RUN_VALIDATOR", grant.scope_digest,
                ) if grant is not None else None
                requested = (
                    request.repository_id, request.logical_effect_id,
                    request.action, request.scope_digest,
                )
                grants = self._validator_grants
            else:
                grant = self._operator_grants.get(request.grant_id)
                binding = (
                    grant.repository_id, grant.run_id, grant.action,
                    grant.scope_digest,
                ) if grant is not None else None
                requested = (
                    request.repository_id, request.run_id, request.action,
                    request.scope_digest,
                )
                grants = self._operator_grants
            if binding != requested:
                raise DispatchDenied(
                    "authority lifecycle fact grant binding mismatch"
                )
            if request.successor_grant_id is not None:
                successor = grants.get(request.successor_grant_id)
                if successor is None:
                    raise DispatchDenied(
                        "authority supersession successor is unavailable"
                    )
                if request.grant_kind == "EFFECT":
                    successor_binding = (
                        successor.repository_id, successor.logical_effect_id,
                        "EXECUTE_EFFECT", successor.scope_digest,
                    )
                elif request.grant_kind == "VALIDATOR":
                    successor_binding = (
                        successor.repository_id, successor.logical_effect_id,
                        "RUN_VALIDATOR", successor.scope_digest,
                    )
                else:
                    successor_binding = (
                        successor.repository_id, successor.run_id,
                        successor.action, successor.scope_digest,
                    )
                if successor_binding != requested:
                    raise DispatchDenied(
                        "authority supersession successor binding mismatch"
                    )

    def verify_authority_lifecycle_evidence(
        self,
        evidence: SyntheticAuthorityLifecycleEvidence,
        request: AuthorityLifecycleFactRequest,
    ) -> None:
        request.validate()
        digest = self._authority_fact_digest(request)
        expected = self._mac(
            "AUTHORITY_LIFECYCLE_EVIDENCE",
            proof_id=evidence.proof_id,
            request_digest=digest,
            issuer_fingerprint=self.issuer_fingerprint,
        )
        if (
            evidence.request_digest != digest
            or evidence.issuer_fingerprint != self.issuer_fingerprint
            or not hmac.compare_digest(evidence.issuer_mac, expected)
        ):
            raise DispatchDenied("authority lifecycle evidence was not issued here")

    @property
    def finalization_issuer_fingerprint(self) -> str:
        return hashlib.sha256(b"FINALIZATION\0" + self._issuer_key).hexdigest()

    def register(self, grant: SyntheticGrant) -> None:
        if not all(
            (
                grant.grant_id,
                grant.repository_id,
                grant.logical_effect_id,
                grant.attempt_id,
                grant.scope_digest,
            )
        ):
            raise ValueError("synthetic grant fields must be non-empty")
        with self._lock:
            if grant.grant_id in self._grants:
                raise DispatchDenied("synthetic grant ID already exists")
            self._grants[grant.grant_id] = grant

    def claim(
        self,
        grant_id: str,
        repository_id: str,
        logical_effect_id: str,
        attempt_id: str,
        scope_digest: str,
    ) -> SyntheticCapability:
        with self._lock:
            grant = self._grants.get(grant_id)
            if grant is None:
                raise DispatchDenied("synthetic grant is unavailable")
            expected = (
                grant.repository_id,
                grant.logical_effect_id,
                grant.attempt_id,
                grant.scope_digest,
            )
            requested = (
                repository_id,
                logical_effect_id,
                attempt_id,
                scope_digest,
            )
            if requested != expected:
                raise DispatchDenied("synthetic grant binding mismatch")
            if grant_id in self._claims:
                raise DispatchDenied("synthetic grant was already claimed")
            claim_id = hashlib.sha256(
                "\0".join((grant_id, *requested)).encode("utf-8")
            ).hexdigest()
            capability = SyntheticCapability(
                claim_id,
                grant_id,
                *requested,
                self._mac(
                    "EFFECT_CAPABILITY",
                    claim_id=claim_id,
                    grant_id=grant_id,
                    repository_id=repository_id,
                    logical_effect_id=logical_effect_id,
                    attempt_id=attempt_id,
                    scope_digest=scope_digest,
                ),
            )
            self._claims[grant_id] = capability
            return capability

    def verify_issued(self, capability: SyntheticCapability) -> None:
        expected_mac = self._mac(
            "EFFECT_CAPABILITY",
            claim_id=capability.claim_id,
            grant_id=capability.grant_id,
            repository_id=capability.repository_id,
            logical_effect_id=capability.logical_effect_id,
            attempt_id=capability.attempt_id,
            scope_digest=capability.scope_digest,
        )
        with self._lock:
            issued = self._claims.get(capability.grant_id)
            if issued != capability or not hmac.compare_digest(
                expected_mac, capability.issuer_mac
            ):
                raise DispatchDenied("synthetic capability was not issued here")

    def verify_for_intent(self, capability: SyntheticCapability) -> None:
        self.verify_issued(capability)
        with self._lock:
            if capability.claim_id in self._committed_claims:
                raise DispatchDenied("synthetic capability already committed an intent")

    def mark_intent_committed(self, capability: SyntheticCapability) -> None:
        self.verify_for_intent(capability)
        with self._lock:
            self._committed_claims.add(capability.claim_id)

    def register_validator(self, grant: SyntheticValidatorGrant) -> None:
        if any(not value for value in grant.__dict__.values()):
            raise ValueError("synthetic validator grant fields must be non-empty")
        with self._lock:
            if grant.grant_id in self._validator_grants:
                raise DispatchDenied("synthetic validator grant ID already exists")
            self._validator_grants[grant.grant_id] = grant

    def claim_validator(
        self,
        grant_id: str,
        repository_id: str,
        logical_effect_id: str,
        revision_digest: str,
        check_id: str,
        input_digest: str,
        validator_attempt_id: str,
        scope_digest: str,
    ) -> SyntheticValidatorCapability:
        requested = (
            repository_id,
            logical_effect_id,
            revision_digest,
            check_id,
            input_digest,
            validator_attempt_id,
            scope_digest,
        )
        with self._lock:
            grant = self._validator_grants.get(grant_id)
            if grant is None:
                raise DispatchDenied("synthetic validator grant is unavailable")
            expected = tuple(grant.__dict__.values())[1:]
            if requested != expected:
                raise DispatchDenied("synthetic validator grant binding mismatch")
            if grant_id in self._validator_claims:
                raise DispatchDenied("synthetic validator grant was already claimed")
            claim_id = hashlib.sha256(
                "\0".join(("VALIDATOR", grant_id, *requested)).encode("utf-8")
            ).hexdigest()
            capability = SyntheticValidatorCapability(
                claim_id,
                grant_id,
                *requested,
                self._mac(
                    "VALIDATOR_CAPABILITY",
                    claim_id=claim_id,
                    grant_id=grant_id,
                    repository_id=repository_id,
                    logical_effect_id=logical_effect_id,
                    revision_digest=revision_digest,
                    check_id=check_id,
                    input_digest=input_digest,
                    validator_attempt_id=validator_attempt_id,
                    scope_digest=scope_digest,
                ),
            )
            self._validator_claims[grant_id] = capability
            return capability

    def verify_validator_issued(
        self, capability: SyntheticValidatorCapability
    ) -> None:
        expected_mac = self._mac(
            "VALIDATOR_CAPABILITY",
            **{
                name: value
                for name, value in capability.__dict__.items()
                if name != "issuer_mac"
            },
        )
        with self._lock:
            issued = self._validator_claims.get(capability.grant_id)
            if issued != capability or not hmac.compare_digest(
                expected_mac, capability.issuer_mac
            ):
                raise DispatchDenied(
                    "synthetic validator capability was not issued here"
                )

    def verify_validator_for_intent(
        self, capability: SyntheticValidatorCapability
    ) -> None:
        self.verify_validator_issued(capability)
        with self._lock:
            if capability.claim_id in self._committed_claims:
                raise DispatchDenied(
                    "synthetic validator capability already committed an intent"
                )

    def mark_validator_intent_committed(
        self, capability: SyntheticValidatorCapability
    ) -> None:
        self.verify_validator_for_intent(capability)
        with self._lock:
            self._committed_claims.add(capability.claim_id)

    def register_operator(self, grant: SyntheticOperatorGrant) -> None:
        if any(not value for value in grant.__dict__.values()):
            raise ValueError("synthetic operator grant fields must be non-empty")
        if grant.action not in {
            "PAUSE", "RESUME", "STOP_GRACEFUL", "STOP_IMMEDIATE",
            "STOP_ESCALATE",
        }:
            raise ValueError("unsupported synthetic operator action")
        with self._lock:
            if grant.grant_id in self._operator_grants:
                raise DispatchDenied("synthetic operator grant ID already exists")
            self._operator_grants[grant.grant_id] = grant

    def claim_operator(
        self,
        grant_id: str,
        repository_id: str,
        run_id: str,
        action: str,
        scope_digest: str,
    ) -> SyntheticOperatorCapability:
        requested = (repository_id, run_id, action, scope_digest)
        with self._lock:
            grant = self._operator_grants.get(grant_id)
            if grant is None:
                raise DispatchDenied("synthetic operator grant is unavailable")
            if requested != tuple(grant.__dict__.values())[1:]:
                raise DispatchDenied("synthetic operator grant binding mismatch")
            if grant_id in self._operator_claims:
                raise DispatchDenied("synthetic operator grant was already claimed")
            claim_id = hashlib.sha256(
                "\0".join(("OPERATOR", grant_id, *requested)).encode("utf-8")
            ).hexdigest()
            capability = SyntheticOperatorCapability(
                claim_id,
                grant_id,
                *requested,
                self._mac(
                    "OPERATOR_CAPABILITY",
                    claim_id=claim_id,
                    grant_id=grant_id,
                    repository_id=repository_id,
                    run_id=run_id,
                    action=action,
                    scope_digest=scope_digest,
                ),
            )
            self._operator_claims[grant_id] = capability
            return capability

    def verify_operator_issued(
        self, capability: SyntheticOperatorCapability
    ) -> None:
        expected_mac = self._mac(
            "OPERATOR_CAPABILITY",
            **{
                name: value
                for name, value in capability.__dict__.items()
                if name != "issuer_mac"
            },
        )
        with self._lock:
            issued = self._operator_claims.get(capability.grant_id)
            if issued != capability or not hmac.compare_digest(
                expected_mac, capability.issuer_mac
            ):
                raise DispatchDenied(
                    "synthetic operator capability was not issued here"
                )

    def verify_operator_for_action(
        self, capability: SyntheticOperatorCapability
    ) -> None:
        self.verify_operator_issued(capability)
        with self._lock:
            if capability.claim_id in self._committed_claims:
                raise DispatchDenied(
                    "synthetic operator capability already committed an action"
                )

    def mark_operator_action_committed(
        self, capability: SyntheticOperatorCapability
    ) -> None:
        self.verify_operator_for_action(capability)
        with self._lock:
            self._committed_claims.add(capability.claim_id)

    def issue_settlement_proof(
        self,
        proof_id: str,
        request: BudgetSettlementRequest,
    ) -> SyntheticSettlementProof:
        request.validate()
        request_digest = self._settlement_request_digest(request)
        return SyntheticSettlementProof(
            proof_id,
            request.reservation_id,
            request.non_dispatch_proven,
            request.zero_liability_proven,
            request.all_obligations_settled,
            request_digest,
            self._mac(
                "SETTLEMENT_PROOF",
                proof_id=proof_id,
                request_digest=request_digest,
            ),
        )

    def verify_settlement_proof(
        self,
        proof: SyntheticSettlementProof,
        request: BudgetSettlementRequest,
    ) -> None:
        request_digest = self._settlement_request_digest(request)
        expected = self._mac(
            "SETTLEMENT_PROOF",
            proof_id=proof.proof_id,
            request_digest=request_digest,
        )
        if not hmac.compare_digest(request_digest, proof.request_digest) or not hmac.compare_digest(
            expected, proof.issuer_mac
        ):
            raise DispatchDenied("synthetic settlement proof was not issued here")

    @staticmethod
    def _settlement_request_digest(request: BudgetSettlementRequest) -> str:
        payload = {
            "actual_units": request.actual_units,
            "additional_liability": request.additional_liability,
            "all_obligations_settled": request.all_obligations_settled,
            "disposition": request.disposition.value,
            "evidence_digest": request.evidence_digest,
            "expected_previous_hash": request.expected_previous_hash,
            "non_dispatch_proven": request.non_dispatch_proven,
            "reason_code": request.reason_code,
            "repository_id": request.repository_id,
            "run_id": request.run_id,
            "item_id": request.item_id,
            "logical_effect_id": request.logical_effect_id,
            "nonexecution_seal_id": request.nonexecution_seal_id,
            "attempt_id": request.attempt_id,
            "release_slot": request.release_slot,
            "reservation_id": request.reservation_id,
            "settlement_event_id": request.settlement_event_id,
            "zero_liability_proven": request.zero_liability_proven,
        }
        encoded = json.dumps(
            payload, ensure_ascii=True, separators=(",", ":"), sort_keys=True
        ).encode("utf-8")
        return hashlib.sha256(encoded).hexdigest()

    def issue_nonexecution_attestation(
        self,
        attestation_id: str,
        seal_id: str,
        contact_kind: str,
        target_digest: str,
        claim_id: str,
        source_id: str,
        source_event_hash: str,
        reservation_id: str,
        repository_id: str,
        run_id: str,
        item_id: str,
        logical_effect_id: str,
        attempt_id: str,
        *,
        action: str = "SEAL_NONEXECUTION",
        policy_id: str = SYNTHETIC_NONEXECUTION_POLICY_ID,
        policy_version: str = SYNTHETIC_NONEXECUTION_POLICY_VERSION,
    ) -> SyntheticNonexecutionAttestation:
        values = (
            attestation_id, seal_id, contact_kind, target_digest, claim_id,
            source_id, source_event_hash, reservation_id, repository_id,
            run_id, item_id, logical_effect_id, attempt_id, action,
            policy_id, policy_version,
        )
        if any(not isinstance(value, str) or not value.strip() for value in values):
            raise ValueError("synthetic nonexecution fields must be non-empty")
        if contact_kind not in {"EFFECT", "VALIDATOR"}:
            raise ValueError("unsupported synthetic nonexecution contact kind")
        if action != "SEAL_NONEXECUTION":
            raise ValueError("unsupported synthetic nonexecution action")
        if (
            policy_id != SYNTHETIC_NONEXECUTION_POLICY_ID
            or policy_version != SYNTHETIC_NONEXECUTION_POLICY_VERSION
        ):
            raise ValueError("unsupported synthetic nonexecution policy")
        fields = {
            "attestation_id": attestation_id,
            "seal_id": seal_id,
            "contact_kind": contact_kind,
            "target_digest": target_digest,
            "claim_id": claim_id,
            "source_id": source_id,
            "source_event_hash": source_event_hash,
            "reservation_id": reservation_id,
            "repository_id": repository_id,
            "run_id": run_id,
            "item_id": item_id,
            "logical_effect_id": logical_effect_id,
            "attempt_id": attempt_id,
            "action": action,
            "policy_id": policy_id,
            "policy_version": policy_version,
        }
        return SyntheticNonexecutionAttestation(
            **fields,
            issuer_mac=self._mac("NONEXECUTION_ATTESTATION", **fields),
        )

    def verify_nonexecution_attestation(
        self, attestation: SyntheticNonexecutionAttestation
    ) -> None:
        expected_mac = self._mac(
            "NONEXECUTION_ATTESTATION",
            **{
                name: value
                for name, value in attestation.__dict__.items()
                if name != "issuer_mac"
            },
        )
        if not hmac.compare_digest(expected_mac, attestation.issuer_mac):
            raise DispatchDenied(
                "synthetic nonexecution attestation was not issued here"
            )
        if attestation.contact_kind not in {"EFFECT", "VALIDATOR"}:
            raise DispatchDenied(
                "synthetic nonexecution attestation has an unsupported kind"
            )
        if attestation.action != "SEAL_NONEXECUTION" or (
            attestation.policy_id != SYNTHETIC_NONEXECUTION_POLICY_ID
            or attestation.policy_version
            != SYNTHETIC_NONEXECUTION_POLICY_VERSION
        ):
            raise DispatchDenied(
                "synthetic nonexecution attestation has an unsupported policy"
            )

    def issue_validator_cessation_attestation(
        self,
        attestation_id: str,
        cessation_id: str,
        target_digest: str,
        claim_id: str,
        source_id: str,
        source_event_hash: str,
        repository_id: str,
        run_id: str,
        item_id: str,
        logical_effect_id: str,
        revision_digest: str,
        check_id: str,
        validator_attempt_id: str,
        *,
        action: str = "CEASE_VALIDATOR",
        policy_id: str = SYNTHETIC_VALIDATOR_CESSATION_POLICY_ID,
        policy_version: str = SYNTHETIC_VALIDATOR_CESSATION_POLICY_VERSION,
    ) -> SyntheticValidatorCessationAttestation:
        fields = {
            "attestation_id": attestation_id,
            "cessation_id": cessation_id,
            "target_digest": target_digest,
            "claim_id": claim_id,
            "source_id": source_id,
            "source_event_hash": source_event_hash,
            "repository_id": repository_id,
            "run_id": run_id,
            "item_id": item_id,
            "logical_effect_id": logical_effect_id,
            "revision_digest": revision_digest,
            "check_id": check_id,
            "validator_attempt_id": validator_attempt_id,
            "action": action,
            "policy_id": policy_id,
            "policy_version": policy_version,
        }
        if any(
            not isinstance(value, str) or not value.strip()
            for value in fields.values()
        ):
            raise ValueError("synthetic validator cessation fields must be non-empty")
        if action != "CEASE_VALIDATOR" or (
            policy_id != SYNTHETIC_VALIDATOR_CESSATION_POLICY_ID
            or policy_version != SYNTHETIC_VALIDATOR_CESSATION_POLICY_VERSION
        ):
            raise ValueError("unsupported synthetic validator cessation policy")
        return SyntheticValidatorCessationAttestation(
            **fields,
            issuer_mac=self._mac("VALIDATOR_CESSATION_ATTESTATION", **fields),
        )

    def verify_validator_cessation_attestation(
        self, attestation: SyntheticValidatorCessationAttestation
    ) -> None:
        expected_mac = self._mac(
            "VALIDATOR_CESSATION_ATTESTATION",
            **{
                name: value
                for name, value in attestation.__dict__.items()
                if name != "issuer_mac"
            },
        )
        if not hmac.compare_digest(expected_mac, attestation.issuer_mac):
            raise DispatchDenied(
                "synthetic validator cessation attestation was not issued here"
            )
        if attestation.action != "CEASE_VALIDATOR" or (
            attestation.policy_id != SYNTHETIC_VALIDATOR_CESSATION_POLICY_ID
            or attestation.policy_version
            != SYNTHETIC_VALIDATOR_CESSATION_POLICY_VERSION
        ):
            raise DispatchDenied(
                "synthetic validator cessation attestation has an unsupported policy"
            )

    def issue_classification(
        self,
        classification_id: str,
        repository_id: str,
        run_id: str,
        item_id: str,
        logical_effect_id: str,
        revision_digest: str,
        check_id: str,
        validator_attempt_id: str,
        observation_id: str,
        observation_event_hash: str,
        result_digest: str,
        *,
        verdict: str,
        policy_id: str,
        policy_version: str,
        classification: str,
    ) -> SyntheticClassificationEvidence:
        if verdict != "FAIL":
            raise ValueError(
                "synthetic classification evidence only classifies a FAIL verdict"
            )
        if classification not in {
            FailureClassification.RECOVERABLE.value,
            FailureClassification.FINAL.value,
        }:
            raise ValueError("unsupported synthetic failure classification")
        if (
            policy_id != SYNTHETIC_FAILURE_POLICY_ID
            or policy_version != SYNTHETIC_FAILURE_POLICY_VERSION
        ):
            raise ValueError("unsupported synthetic failure classification policy")
        values = (
            classification_id, repository_id, run_id, item_id,
            logical_effect_id, revision_digest, check_id,
            validator_attempt_id, observation_id, observation_event_hash,
            result_digest, verdict, policy_id, policy_version, classification,
        )
        if any(
            not isinstance(value, str) or not value.strip()
            for value in values
        ):
            raise ValueError("synthetic classification fields must be non-empty")
        return SyntheticClassificationEvidence(
            *values,
            self._mac(
                "FAILURE_CLASSIFICATION",
                classification_id=classification_id,
                repository_id=repository_id,
                run_id=run_id,
                item_id=item_id,
                logical_effect_id=logical_effect_id,
                revision_digest=revision_digest,
                check_id=check_id,
                validator_attempt_id=validator_attempt_id,
                observation_id=observation_id,
                observation_event_hash=observation_event_hash,
                result_digest=result_digest,
                verdict=verdict,
                policy_id=policy_id,
                policy_version=policy_version,
                classification=classification,
            ),
        )

    def verify_classification(
        self, evidence: SyntheticClassificationEvidence
    ) -> None:
        if any(
            not isinstance(value, str) or not value.strip()
            for value in evidence.__dict__.values()
        ):
            raise DispatchDenied(
                "synthetic classification fields must be non-empty strings"
            )
        expected_mac = self._mac(
            "FAILURE_CLASSIFICATION",
            **{
                name: value
                for name, value in evidence.__dict__.items()
                if name != "issuer_mac"
            },
        )
        if not hmac.compare_digest(expected_mac, evidence.issuer_mac):
            raise DispatchDenied(
                "synthetic classification evidence was not issued here"
            )
        if evidence.verdict != "FAIL":
            raise DispatchDenied(
                "synthetic classification evidence must classify a FAIL verdict"
            )
        if evidence.classification not in {
            FailureClassification.RECOVERABLE.value,
            FailureClassification.FINAL.value,
        }:
            raise DispatchDenied(
                "synthetic classification evidence has an unsupported classification"
            )
        if (
            evidence.policy_id != SYNTHETIC_FAILURE_POLICY_ID
            or evidence.policy_version != SYNTHETIC_FAILURE_POLICY_VERSION
        ):
            raise DispatchDenied(
                "synthetic classification evidence has an unsupported policy"
            )

    def issue_finalization_attestation(
        self,
        attestation_id: str,
        repository_id: str,
        run_id: str,
        item_id: str,
        logical_effect_id: str,
        plan_id: str,
        plan_event_hash: str,
        revision_digest: str,
        evaluated_run_head: str,
        finalization_key: str,
        gate_set_digest: str,
        slot_attempt_id: str,
        slot_generation: int,
        *,
        verdict: str = "PASS",
        policy_id: str = SYNTHETIC_FINALIZATION_POLICY_ID,
        policy_version: str = SYNTHETIC_FINALIZATION_POLICY_VERSION,
    ) -> SyntheticFinalizationAttestation:
        string_values = (
            attestation_id, repository_id, run_id, item_id, logical_effect_id,
            plan_id, plan_event_hash, revision_digest, evaluated_run_head,
            finalization_key, gate_set_digest, slot_attempt_id, verdict,
            policy_id, policy_version,
        )
        if any(
            not isinstance(value, str) or not value.strip()
            for value in string_values
        ):
            raise ValueError("synthetic finalization fields must be non-empty")
        if type(slot_generation) is not int or slot_generation <= 0:
            raise ValueError("synthetic finalization slot generation must be positive")
        if verdict != "PASS":
            raise ValueError("synthetic finalization attestation must be PASS")
        if (
            policy_id != SYNTHETIC_FINALIZATION_POLICY_ID
            or policy_version != SYNTHETIC_FINALIZATION_POLICY_VERSION
        ):
            raise ValueError("unsupported synthetic finalization policy")
        return SyntheticFinalizationAttestation(
            attestation_id, repository_id, run_id, item_id, logical_effect_id,
            plan_id, plan_event_hash, revision_digest, evaluated_run_head,
            finalization_key, gate_set_digest, slot_attempt_id, slot_generation,
            verdict, policy_id, policy_version,
            self._mac(
                "FINALIZATION_ATTESTATION",
                attestation_id=attestation_id,
                repository_id=repository_id,
                run_id=run_id,
                item_id=item_id,
                logical_effect_id=logical_effect_id,
                plan_id=plan_id,
                plan_event_hash=plan_event_hash,
                revision_digest=revision_digest,
                evaluated_run_head=evaluated_run_head,
                finalization_key=finalization_key,
                gate_set_digest=gate_set_digest,
                slot_attempt_id=slot_attempt_id,
                slot_generation=slot_generation,
                verdict=verdict,
                policy_id=policy_id,
                policy_version=policy_version,
            ),
        )

    def verify_finalization_attestation(
        self, attestation: SyntheticFinalizationAttestation
    ) -> None:
        string_values = tuple(attestation.__dict__.values())[:12] + tuple(
            attestation.__dict__.values()
        )[13:]
        if any(
            not isinstance(value, str) or not value.strip()
            for value in string_values
        ) or (
            type(attestation.slot_generation) is not int
            or attestation.slot_generation <= 0
        ):
            raise DispatchDenied(
                "synthetic finalization fields have invalid types"
            )
        expected_mac = self._mac(
            "FINALIZATION_ATTESTATION",
            **{
                name: value
                for name, value in attestation.__dict__.items()
                if name != "issuer_mac"
            },
        )
        if not hmac.compare_digest(expected_mac, attestation.issuer_mac):
            raise DispatchDenied(
                "synthetic finalization attestation was not issued here"
            )
        if attestation.verdict != "PASS":
            raise DispatchDenied("synthetic finalization attestation must be PASS")
        if (
            attestation.policy_id != SYNTHETIC_FINALIZATION_POLICY_ID
            or attestation.policy_version != SYNTHETIC_FINALIZATION_POLICY_VERSION
        ):
            raise DispatchDenied(
                "synthetic finalization attestation has an unsupported policy"
            )

    def issue_validation_recovery_attestation(
        self,
        attestation_id: str,
        recovery_id: str,
        repository_id: str,
        run_id: str,
        item_id: str,
        logical_effect_id: str,
        plan_id: str,
        plan_event_hash: str,
        revision_digest: str,
        check_id: str,
        failed_application_id: str,
        failed_application_event_hash: str,
        failed_validator_attempt_id: str,
        successor_validator_attempt_id: str,
        remediation_evidence_digest: str,
        evaluated_run_head: str,
        slot_attempt_id: str,
        slot_generation: int,
        *,
        action: str = "RETRY_VALIDATION",
        policy_id: str = SYNTHETIC_VALIDATION_RECOVERY_POLICY_ID,
        policy_version: str = SYNTHETIC_VALIDATION_RECOVERY_POLICY_VERSION,
    ) -> SyntheticValidationRecoveryAttestation:
        values = (
            attestation_id, recovery_id, repository_id, run_id, item_id,
            logical_effect_id, plan_id, plan_event_hash, revision_digest,
            check_id, failed_application_id, failed_application_event_hash,
            failed_validator_attempt_id, successor_validator_attempt_id,
            remediation_evidence_digest, evaluated_run_head, slot_attempt_id,
            action, policy_id, policy_version,
        )
        if any(not isinstance(value, str) or not value.strip() for value in values):
            raise ValueError("synthetic validation recovery fields must be non-empty")
        if type(slot_generation) is not int or slot_generation <= 0:
            raise ValueError("validation recovery slot generation must be positive")
        if action != "RETRY_VALIDATION":
            raise ValueError("unsupported synthetic validation recovery action")
        if failed_validator_attempt_id == successor_validator_attempt_id:
            raise ValueError("validation recovery requires a new validator attempt")
        if (
            policy_id != SYNTHETIC_VALIDATION_RECOVERY_POLICY_ID
            or policy_version != SYNTHETIC_VALIDATION_RECOVERY_POLICY_VERSION
        ):
            raise ValueError("unsupported synthetic validation recovery policy")
        fields = {
            "attestation_id": attestation_id,
            "recovery_id": recovery_id,
            "repository_id": repository_id,
            "run_id": run_id,
            "item_id": item_id,
            "logical_effect_id": logical_effect_id,
            "plan_id": plan_id,
            "plan_event_hash": plan_event_hash,
            "revision_digest": revision_digest,
            "check_id": check_id,
            "failed_application_id": failed_application_id,
            "failed_application_event_hash": failed_application_event_hash,
            "failed_validator_attempt_id": failed_validator_attempt_id,
            "successor_validator_attempt_id": successor_validator_attempt_id,
            "remediation_evidence_digest": remediation_evidence_digest,
            "evaluated_run_head": evaluated_run_head,
            "slot_attempt_id": slot_attempt_id,
            "slot_generation": slot_generation,
            "action": action,
            "policy_id": policy_id,
            "policy_version": policy_version,
        }
        return SyntheticValidationRecoveryAttestation(
            *fields.values(), self._mac("VALIDATION_RECOVERY", **fields)
        )

    def verify_validation_recovery_attestation(
        self, attestation: SyntheticValidationRecoveryAttestation
    ) -> None:
        expected_mac = self._mac(
            "VALIDATION_RECOVERY",
            **{
                name: value
                for name, value in attestation.__dict__.items()
                if name != "issuer_mac"
            },
        )
        if not hmac.compare_digest(expected_mac, attestation.issuer_mac):
            raise DispatchDenied(
                "synthetic validation recovery attestation was not issued here"
            )
        if attestation.action != "RETRY_VALIDATION":
            raise DispatchDenied(
                "synthetic validation recovery has an unsupported action"
            )
        if (
            attestation.policy_id != SYNTHETIC_VALIDATION_RECOVERY_POLICY_ID
            or attestation.policy_version
            != SYNTHETIC_VALIDATION_RECOVERY_POLICY_VERSION
        ):
            raise DispatchDenied(
                "synthetic validation recovery has an unsupported policy"
            )


def reject_real_authority(authority_kind: str) -> None:
    raise DispatchDenied(
        f"authority kind {authority_kind!r} is unavailable in the synthetic kernel"
    )
