"""Offline falsifiers for future delivery capabilities; never real authority.

All declarations are closed. A passing synthetic observation says only that the
interface rejected the injected failure; it cannot authorize a real target.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from threading import Lock

from .contracts import DispatchDenied


class Capability(str, Enum):
    SOURCE_ATOMIC = "source_atomic"
    FRESHNESS = "freshness"
    CONTAINMENT = "containment"
    OWNED_PATH = "owned_path"
    EVIDENCE = "evidence"
    ACCOUNTING = "accounting"


class Finding(str, Enum):
    SYNTHETIC_PROVEN = "synthetic_proven"
    UNPROVEN = "unproven"
    DENIED = "denied"


@dataclass(frozen=True)
class CapabilityObservation:
    capability: Capability
    finding: Finding
    reason: str


def require_real_dispatch(observations: tuple[CapabilityObservation, ...]) -> None:
    """No offline report can grant real dispatch, including forged pass rows."""
    seen: set[Capability] = set()
    for row in observations:
        if type(row) is not CapabilityObservation or type(row.capability) is not Capability:
            raise DispatchDenied("invalid capability declaration")
        if row.capability in seen:
            raise DispatchDenied("duplicate capability declaration")
        seen.add(row.capability)
    missing = set(Capability) - seen
    if missing:
        raise DispatchDenied("real dispatch capability is unproven: " + ", ".join(sorted(x.value for x in missing)))
    raise DispatchDenied("real dispatch denied: offline proofs cannot verify source and host")


def require_synthetic_dispatch(authority: object, target: object) -> None:
    """The existing coordinator cannot be repurposed with a lookalike target."""
    from .adapters import SyntheticExecutionAdapter
    from .authority import SyntheticAuthority

    if type(authority) is not SyntheticAuthority or type(target) is not SyntheticExecutionAdapter:
        raise DispatchDenied("unsupported capability: synthetic dispatch boundary only")


def require_synthetic_validation(authority: object, target: object) -> None:
    from .adapters import SyntheticValidatorAdapter
    from .authority import SyntheticAuthority

    if type(authority) is not SyntheticAuthority or type(target) is not SyntheticValidatorAdapter:
        raise DispatchDenied("unsupported capability: synthetic validation boundary only")


class SyntheticClaimSource:
    """One shared source for controller and manual consumers in race probes."""

    def __init__(self, token: str, *, expires_at: int) -> None:
        self.token = token
        self.expires_at = expires_at
        self._lock = Lock()
        self._claimed_by: str | None = None
        self._revoked = False
        self._superseded = False
        self.available = True

    def revoke(self) -> None:
        with self._lock:
            self._revoked = True

    def supersede(self) -> None:
        with self._lock:
            self._superseded = True

    def claim(self, token: str, consumer: str, *, now: int) -> bool:
        if not token or not consumer or type(now) is not int:
            raise ValueError("invalid synthetic claim")
        with self._lock:
            if (not self.available or token != self.token or self._revoked
                    or self._superseded or now >= self.expires_at
                    or self._claimed_by is not None):
                return False
            self._claimed_by = consumer
            return True

    def recover_acknowledgement(self, token: str, consumer: str) -> bool:
        """A lost acknowledgement reveals the prior winner without a new claim."""
        with self._lock:
            return self.available and token == self.token and self._claimed_by == consumer

    def authorize_contact(self, token: str, consumer: str, *, now: int) -> bool:
        """Re-read source state before contact; the old claim alone is insufficient."""
        with self._lock:
            return (type(now) is int and self.available and token == self.token
                    and self._claimed_by == consumer and not self._revoked
                    and not self._superseded and now < self.expires_at)


@dataclass(frozen=True)
class FreshnessProof:
    sequence: int
    head_hash: str


def verify_freshness(
    candidate: FreshnessProof,
    *, independent_anchor: FreshnessProof | None = None,
    current_source: FreshnessProof | None = None,
) -> None:
    """Require an independent anchor or a complete current source view."""
    if (type(candidate) is not FreshnessProof or type(candidate.sequence) is not int
            or candidate.sequence < 0 or type(candidate.head_hash) is not str
            or not candidate.head_hash):
        raise DispatchDenied("invalid freshness proof")
    if independent_anchor is None and current_source is None:
        raise DispatchDenied("freshness capability unavailable")
    for reference in (independent_anchor, current_source):
        if reference is None:
            continue
        if (type(reference) is not FreshnessProof or type(reference.sequence) is not int
                or reference.sequence < 0 or type(reference.head_hash) is not str
                or not reference.head_hash):
            raise DispatchDenied("invalid freshness reference")
        if candidate != reference:
            raise DispatchDenied("stale or contradictory checkpoint")


@dataclass(frozen=True)
class ContainmentProbe:
    host_supported: bool
    descendants_ceased: bool
    leader_ceased: bool
    timed_out: bool
    fence_held: bool
    path_identity_stable: bool
    owner_verified: bool


def verify_containment(probe: ContainmentProbe) -> None:
    if type(probe) is not ContainmentProbe or not all(
        type(getattr(probe, name)) is bool for name in probe.__dataclass_fields__
    ):
        raise DispatchDenied("invalid containment declaration")
    if not probe.host_supported:
        raise DispatchDenied("unsupported host containment capability")
    if (not probe.descendants_ceased or not probe.leader_ceased or probe.timed_out
            or not probe.fence_held or not probe.path_identity_stable
            or not probe.owner_verified):
        raise DispatchDenied("containment or fencing proof failed")


@dataclass(frozen=True)
class SyntheticAccountingReceipt:
    receipt_id: str
    operation_id: str
    amount: int | None
    final: bool


class SyntheticLiabilityBook:
    """Retain worst-case liability until an exact, final source bill resolves it."""

    def __init__(self, operation_id: str, cap: int, worst_case: int) -> None:
        if (not operation_id or type(cap) is not int or type(worst_case) is not int
                or not 0 <= worst_case <= cap):
            raise ValueError("invalid synthetic liability bounds")
        self.operation_id = operation_id
        self.cap = cap
        self.worst_case = worst_case
        self._receipts: dict[str, SyntheticAccountingReceipt] = {}
        self._amount: int | None = None
        self._closed = False

    @property
    def liability(self) -> int:
        return self.worst_case if self._amount is None else self._amount

    @property
    def slot_held(self) -> bool:
        return not self._closed

    def intake(self, receipt: SyntheticAccountingReceipt, *, cancelled: bool = False) -> None:
        if (type(receipt) is not SyntheticAccountingReceipt or not receipt.receipt_id
                or receipt.operation_id != self.operation_id or type(receipt.final) is not bool
                or (receipt.amount is not None and
                    (type(receipt.amount) is not int or not 0 <= receipt.amount <= self.cap))):
            raise DispatchDenied("invalid synthetic accounting receipt")
        prior = self._receipts.get(receipt.receipt_id)
        if prior is not None:
            if prior != receipt:
                raise DispatchDenied("contradictory receipt replay")
            return
        if self._closed or (self._amount is not None and receipt.amount != self._amount):
            raise DispatchDenied("contradictory or late receipt")
        self._receipts[receipt.receipt_id] = receipt
        if receipt.final and receipt.amount is not None:
            self._amount = receipt.amount
            self._closed = True
        # Cancellation is not evidence of zero use; unknown remains reserved.

    def checkpoint(self) -> tuple[SyntheticAccountingReceipt, ...]:
        return tuple(self._receipts.values())

    @classmethod
    def recover(
        cls, operation_id: str, cap: int, worst_case: int,
        receipts: tuple[SyntheticAccountingReceipt, ...],
    ) -> "SyntheticLiabilityBook":
        book = cls(operation_id, cap, worst_case)
        for receipt in receipts:
            book.intake(receipt)
        return book
