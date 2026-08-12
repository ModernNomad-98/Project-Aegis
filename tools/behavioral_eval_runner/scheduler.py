"""Deterministic risk-aware, budget-aware scheduler (design §11a; Phase 16).

The queue is a pure function of (policy version, selection, seed): filesystem,
API, and dictionary iteration order can never influence it. Within one
priority, ordering is canonical by ``case_uid`` — or an explicitly seeded
deterministic rotation (SHA-256 of seed+case_uid, never ``random``). Under a
budget cap, the dispatched prefix is exactly reproducible; every case records
its priority, queue position, reservation result, and inclusion/exclusion
reason. No automatic reprioritization exists.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Iterable, Mapping

from . import SCHEDULING_POLICY_VERSION
from .canonical import sha256_hex_text, sha256_of_obj
from .enums import InclusionReason, ReasonCode, SchedulingPriority
from .errors import ReservationDeniedError, SchedulerError
from .budget import BudgetLedger
from .identity import parse_case_uid


@dataclass(frozen=True, slots=True)
class SchedulingPolicy:
    """Versioned scheduling policy. The priority order is the design §11a order."""

    policy_version: str = SCHEDULING_POLICY_VERSION
    priority_order: tuple[int, ...] = tuple(int(p) for p in SchedulingPriority)
    within_priority_ordering: str = "canonical_case_uid"  # or "seeded_rotation"
    seed: str | None = None

    def validate(self) -> None:
        if self.within_priority_ordering not in ("canonical_case_uid", "seeded_rotation"):
            raise SchedulerError(
                f"unknown within-priority ordering {self.within_priority_ordering!r}"
            )
        if self.within_priority_ordering == "seeded_rotation" and not self.seed:
            raise SchedulerError("seeded_rotation requires an explicit recorded seed")
        if self.priority_order != tuple(int(p) for p in SchedulingPriority):
            raise SchedulerError(
                "the v1 policy priority order is fixed by design §11a; "
                "no automatic reprioritization exists"
            )

    def to_dict(self) -> dict[str, Any]:
        return {
            "policy_version": self.policy_version,
            "priority_order": list(self.priority_order),
            "within_priority_ordering": self.within_priority_ordering,
            "seed": self.seed,
        }

    @property
    def policy_hash(self) -> str:
        return sha256_of_obj(self.to_dict())


@dataclass(frozen=True, slots=True)
class SelectionItem:
    """One selected case entering the scheduler."""

    case_uid: str
    priority: SchedulingPriority
    inclusion_reason: InclusionReason
    reservation_request: Mapping[str, int] = field(default_factory=dict)

    def validate(self) -> None:
        parse_case_uid(self.case_uid)
        if not isinstance(self.priority, SchedulingPriority):
            raise SchedulerError("priority must be a SchedulingPriority")
        if not isinstance(self.inclusion_reason, InclusionReason):
            raise SchedulerError("inclusion_reason must be an InclusionReason")


@dataclass(frozen=True, slots=True)
class QueueEntry:
    case_uid: str
    priority: int
    queue_position: int
    inclusion_reason: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "case_uid": self.case_uid,
            "priority": self.priority,
            "queue_position": self.queue_position,
            "inclusion_reason": self.inclusion_reason,
        }


def _within_priority_key(policy: SchedulingPolicy, case_uid: str) -> str:
    if policy.within_priority_ordering == "seeded_rotation":
        assert policy.seed is not None  # validated
        return sha256_hex_text(f"{policy.seed}::{case_uid}")
    return case_uid


def build_queue(
    policy: SchedulingPolicy, selection: Iterable[SelectionItem]
) -> list[QueueEntry]:
    """Build the deterministic queue. Input iteration order is irrelevant."""
    policy.validate()
    items = list(selection)
    seen: set[str] = set()
    for item in items:
        item.validate()
        if item.case_uid in seen:
            raise SchedulerError(f"duplicate case in selection: {item.case_uid}")
        seen.add(item.case_uid)
    ordered = sorted(
        items,
        key=lambda item: (
            int(item.priority),
            _within_priority_key(policy, item.case_uid),
            item.case_uid,
        ),
    )
    return [
        QueueEntry(
            case_uid=item.case_uid,
            priority=int(item.priority),
            queue_position=position,
            inclusion_reason=item.inclusion_reason.value,
        )
        for position, item in enumerate(ordered)
    ]


@dataclass(frozen=True, slots=True)
class DispatchDecision:
    """Per-case scheduling evidence (design §11a/§13)."""

    case_uid: str
    priority: int
    queue_position: int
    inclusion_reason: str
    reservation_result: str  # "reserved" | "denied"
    reservation_id: str | None
    denial_detail: str | None
    unrun_reason_code: str | None

    def to_dict(self) -> dict[str, Any]:
        return {
            "case_uid": self.case_uid,
            "priority": self.priority,
            "queue_position": self.queue_position,
            "inclusion_reason": self.inclusion_reason,
            "reservation_result": self.reservation_result,
            "reservation_id": self.reservation_id,
            "denial_detail": self.denial_detail,
            "unrun_reason_code": self.unrun_reason_code,
        }


@dataclass(frozen=True, slots=True)
class ScheduleEvidence:
    scheduling_policy_version: str
    scheduling_policy_hash: str
    seed: str | None
    queue: tuple[QueueEntry, ...]
    decisions: tuple[DispatchDecision, ...]

    def to_dict(self) -> dict[str, Any]:
        return {
            "scheduling_policy_version": self.scheduling_policy_version,
            "scheduling_policy_hash": self.scheduling_policy_hash,
            "seed": self.seed,
            "queue": [entry.to_dict() for entry in self.queue],
            "decisions": [decision.to_dict() for decision in self.decisions],
        }


def schedule_with_reservation(
    policy: SchedulingPolicy,
    selection: Iterable[SelectionItem],
    ledger: BudgetLedger,
) -> ScheduleEvidence:
    """Walk the deterministic queue, reserving before every would-be dispatch.

    A denied reservation leaves the case UNRUN with reason BUDGET_CAP. Nothing
    is dispatched here — WP-2B-1 has no dispatch path — this produces the
    scheduling + reservation evidence only. The walk models the conservative
    sequential (concurrency-1) prefix: each granted reservation is immediately
    reconciled at its conservative maximum, so the dispatched prefix is a pure
    function of policy + selection + seed + caps.
    """
    materialized = list(selection)
    # build_queue is the single duplicate-selection gate; run it on the raw
    # list BEFORE indexing so a repeated case_uid is refused, never silently
    # collapsed last-wins (which would make dispatch input-order dependent).
    queue = build_queue(policy, materialized)
    items = {item.case_uid: item for item in materialized}
    decisions: list[DispatchDecision] = []
    for entry in queue:
        item = items[entry.case_uid]
        try:
            reservation = ledger.reserve(entry.case_uid, item.reservation_request)
            ledger.reconcile(reservation, dict(reservation.amounts))
        except ReservationDeniedError as denial:
            decisions.append(
                DispatchDecision(
                    case_uid=entry.case_uid,
                    priority=entry.priority,
                    queue_position=entry.queue_position,
                    inclusion_reason=entry.inclusion_reason,
                    reservation_result="denied",
                    reservation_id=None,
                    denial_detail=str(denial),
                    unrun_reason_code=ReasonCode.BUDGET_CAP.value,
                )
            )
            continue
        decisions.append(
            DispatchDecision(
                case_uid=entry.case_uid,
                priority=entry.priority,
                queue_position=entry.queue_position,
                inclusion_reason=entry.inclusion_reason,
                reservation_result="reserved",
                reservation_id=reservation.reservation_id,
                denial_detail=None,
                unrun_reason_code=None,
            )
        )
    return ScheduleEvidence(
        scheduling_policy_version=policy.policy_version,
        scheduling_policy_hash=policy.policy_hash,
        seed=policy.seed,
        queue=tuple(queue),
        decisions=tuple(decisions),
    )


def build_selection_with_reverse_edges(
    changed_skills: Iterable[str],
    own_cases: Mapping[str, list[str]],
    reverse_index: Mapping[str, list[str]],
    priority_for_own: SchedulingPriority = SchedulingPriority.CHANGED_SKILL,
) -> list[SelectionItem]:
    """PR-tier selection helper: own cases PLUS every incoming reverse edge.

    ``own_cases`` maps skill -> its case_uids; ``reverse_index`` maps
    skill -> case_uids elsewhere in the corpus that name it (the §12 reverse
    negative-neighbor index). Symmetry is never assumed.
    """
    selected: dict[str, SelectionItem] = {}
    for skill in sorted(set(changed_skills)):
        for case_uid in sorted(own_cases.get(skill, ())):
            selected[case_uid] = SelectionItem(
                case_uid=case_uid,
                priority=priority_for_own,
                inclusion_reason=InclusionReason.OWN_CASE,
            )
        for case_uid in sorted(reverse_index.get(skill, ())):
            if case_uid not in selected:
                selected[case_uid] = SelectionItem(
                    case_uid=case_uid,
                    priority=SchedulingPriority.REVERSE_NEIGHBOR_EDGE,
                    inclusion_reason=InclusionReason.REVERSE_EDGE,
                )
    return sorted(selected.values(), key=lambda item: item.case_uid)
