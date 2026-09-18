"""Synthetic-only one-use authority for offline kernel testing."""

from __future__ import annotations

import hashlib
import hmac
import secrets
import threading
from dataclasses import dataclass

from .contracts import DispatchDenied


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
class SyntheticSettlementProof:
    proof_id: str
    reservation_id: str
    non_dispatch_proven: bool
    zero_liability_proven: bool
    all_obligations_settled: bool
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
        self._committed_claims: set[str] = set()

    def _mac(self, *values: str) -> str:
        return hmac.new(
            self._issuer_key, "\0".join(values).encode("utf-8"), hashlib.sha256
        ).hexdigest()

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
                self._mac(claim_id, grant_id, *requested),
            )
            self._claims[grant_id] = capability
            return capability

    def verify_issued(self, capability: SyntheticCapability) -> None:
        expected_mac = self._mac(
            capability.claim_id,
            capability.grant_id,
            capability.repository_id,
            capability.logical_effect_id,
            capability.attempt_id,
            capability.scope_digest,
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
                self._mac("VALIDATOR", claim_id, grant_id, *requested),
            )
            self._validator_claims[grant_id] = capability
            return capability

    def verify_validator_issued(
        self, capability: SyntheticValidatorCapability
    ) -> None:
        values = tuple(capability.__dict__.values())
        expected_mac = self._mac("VALIDATOR", *values[:-1])
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

    def issue_settlement_proof(
        self,
        proof_id: str,
        reservation_id: str,
        *,
        non_dispatch_proven: bool,
        zero_liability_proven: bool,
        all_obligations_settled: bool,
    ) -> SyntheticSettlementProof:
        values = (
            proof_id,
            reservation_id,
            str(int(non_dispatch_proven)),
            str(int(zero_liability_proven)),
            str(int(all_obligations_settled)),
        )
        return SyntheticSettlementProof(
            proof_id,
            reservation_id,
            non_dispatch_proven,
            zero_liability_proven,
            all_obligations_settled,
            self._mac(*values),
        )

    def verify_settlement_proof(self, proof: SyntheticSettlementProof) -> None:
        expected = self._mac(
            proof.proof_id,
            proof.reservation_id,
            str(int(proof.non_dispatch_proven)),
            str(int(proof.zero_liability_proven)),
            str(int(proof.all_obligations_settled)),
        )
        if not hmac.compare_digest(expected, proof.issuer_mac):
            raise DispatchDenied("synthetic settlement proof was not issued here")


def reject_real_authority(authority_kind: str) -> None:
    raise DispatchDenied(
        f"authority kind {authority_kind!r} is unavailable in the synthetic kernel"
    )