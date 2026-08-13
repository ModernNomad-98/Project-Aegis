"""Immutable attempt records and deterministic N/quorum aggregation
(design §10; prompt Phase 17).

- Default N=3, quorum 2-of-3; N configurable, quorum = floor(N/2)+1.
- No replacement attempts, ever: a duplicate (run_id, case_uid,
  repetition_number) is refused; retry-until-green does not exist.
- Blocker precedence for no-quorum cases: ERROR > JUDGE_ERROR >
  INSUFFICIENT_ATTEMPTS > PRECHECK_EXCLUDED > BUDGET_EXHAUSTED > other.
- ``execution_degraded`` is true ONLY when a valid quorum coexists with a
  non-verdict attempt.
- Quarantine is orthogonal metadata and never erases
  latest_aggregate_verdict/latest_aggregate_blocker.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Mapping

from .enums import (
    AggregateBlocker,
    AggregateVerdict,
    AttemptState,
    PRECHECK_REASON_CODES,
    QuarantineStatus,
    ReasonCode,
)
from .errors import AggregationError, DuplicateAttemptError
from .models import AggregateRecord, AttemptRecord


def quorum_for(n_attempts: int) -> int:
    """Majority quorum: k = floor(N/2) + 1."""
    if not isinstance(n_attempts, int) or isinstance(n_attempts, bool) or n_attempts < 1:
        raise AggregationError(f"N must be an int >= 1, got {n_attempts!r}")
    return n_attempts // 2 + 1


@dataclass(frozen=True, slots=True)
class QuarantineMetadata:
    """Orthogonal quarantine inputs to aggregation (design §10)."""

    status: QuarantineStatus = QuarantineStatus.INACTIVE
    reason: str | None = None
    since: str | None = None
    waiver_ref: str | None = None


class AttemptSet:
    """Collects the immutable attempts of ONE case in ONE run.

    Refuses duplicate repetition numbers (no replacement attempts) and
    attempts whose identity does not match the set.
    """

    def __init__(self, run_id: str, case_uid: str, attempts_planned: int) -> None:
        if attempts_planned < 1:
            raise AggregationError("attempts_planned must be >= 1")
        self.run_id = run_id
        self.case_uid = case_uid
        self.attempts_planned = attempts_planned
        self._attempts: dict[int, AttemptRecord] = {}

    def add(self, attempt: AttemptRecord) -> None:
        attempt.validate()
        if attempt.run_id != self.run_id or attempt.case_uid != self.case_uid:
            raise AggregationError(
                f"attempt identity {attempt.identity} does not belong to "
                f"({self.run_id}, {self.case_uid})"
            )
        if attempt.repetition_number > self.attempts_planned:
            raise AggregationError(
                f"repetition {attempt.repetition_number} exceeds planned "
                f"{self.attempts_planned}"
            )
        if attempt.repetition_number in self._attempts:
            raise DuplicateAttemptError(
                f"attempt {attempt.identity} already recorded; replacement "
                "attempts are forbidden (no retry-until-green)"
            )
        self._attempts[attempt.repetition_number] = attempt

    @property
    def attempts(self) -> tuple[AttemptRecord, ...]:
        return tuple(self._attempts[k] for k in sorted(self._attempts))


def _state_counts(attempts: Iterable[AttemptRecord]) -> Mapping[AttemptState, int]:
    counts = {state: 0 for state in AttemptState}
    for attempt in attempts:
        counts[attempt.attempt_state] += 1
    return counts


def aggregate_case(
    attempt_set: AttemptSet,
    n_attempts: int | None = None,
    quarantine: QuarantineMetadata | None = None,
) -> AggregateRecord:
    """Deterministic §10 aggregation over one case's immutable attempts."""
    attempts = attempt_set.attempts
    n = n_attempts if n_attempts is not None else attempt_set.attempts_planned
    if n != attempt_set.attempts_planned:
        raise AggregationError(
            f"N={n} disagrees with attempts_planned={attempt_set.attempts_planned}"
        )
    if len(attempts) != n:
        raise AggregationError(
            f"aggregation requires every planned attempt to be recorded "
            f"({len(attempts)} of {n}); planned-but-unlaunched attempts are "
            "recorded UNRUN, never omitted"
        )
    quarantine = quarantine or QuarantineMetadata()
    quorum = quorum_for(n)
    counts = _state_counts(attempts)
    pass_count = counts[AttemptState.PASS]
    fail_count = counts[AttemptState.FAIL]
    executed_verdicts = pass_count + fail_count
    attempts_run = n - counts[AttemptState.UNRUN]
    non_verdict_present = (
        counts[AttemptState.ERROR] > 0
        or counts[AttemptState.JUDGE_ERROR] > 0
        or counts[AttemptState.UNRUN] > 0
    )

    verdict: AggregateVerdict
    blocker: AggregateBlocker
    reason: ReasonCode | None = None
    degraded = False
    wins = 0
    from_quorum = False

    if pass_count >= quorum:
        verdict, blocker = AggregateVerdict.PASS, AggregateBlocker.NONE
        wins = pass_count
        degraded = non_verdict_present
        from_quorum = True
    elif fail_count >= quorum:
        verdict, blocker = AggregateVerdict.FAIL, AggregateBlocker.NONE
        wins = fail_count
        degraded = non_verdict_present
        from_quorum = True
    else:
        verdict = AggregateVerdict.INCONCLUSIVE
        unrun_reasons = {
            attempt.error_reason_code
            for attempt in attempts
            if attempt.attempt_state is AttemptState.UNRUN
        }
        error_reasons = [
            attempt.error_reason_code
            for attempt in attempts
            if attempt.attempt_state is AttemptState.ERROR
        ]
        if counts[AttemptState.ERROR] > 0:
            blocker = AggregateBlocker.ERROR
            reason = error_reasons[0]
        elif counts[AttemptState.JUDGE_ERROR] > 0:
            blocker = AggregateBlocker.JUDGE_ERROR
        elif executed_verdicts > 0:
            # The case EXECUTED without reaching quorum — never reported as
            # "unrun" (§20a-S21).
            blocker = AggregateBlocker.INSUFFICIENT_ATTEMPTS
        elif unrun_reasons & PRECHECK_REASON_CODES:
            blocker = AggregateBlocker.PRECHECK_EXCLUDED
            precheck = sorted(
                (r for r in unrun_reasons if r in PRECHECK_REASON_CODES),
                key=lambda r: r.value,
            )
            reason = precheck[0]
        elif ReasonCode.BUDGET_CAP in unrun_reasons:
            blocker = AggregateBlocker.BUDGET_EXHAUSTED
            reason = ReasonCode.BUDGET_CAP
        elif unrun_reasons <= {ReasonCode.NOT_SELECTED, None}:
            blocker = AggregateBlocker.NOT_SELECTED
            reason = ReasonCode.NOT_SELECTED
        else:
            # UNRUN attempts carry a reason the blocker precedence does not
            # map (e.g. LIVE_DISPATCH_DISABLED). Fail closed rather than
            # laundering it into NOT_SELECTED, which would destroy the real
            # cause. The verdict stays INCONCLUSIVE; the reason is preserved.
            unmapped = sorted(
                (r for r in unrun_reasons if r is not None),
                key=lambda r: r.value,
            )
            raise AggregationError(
                f"{attempt_set.case_uid}: UNRUN attempts carry unmapped "
                f"reason(s) {[r.value for r in unmapped]}; the blocker "
                "precedence does not classify them, so aggregation fails "
                "closed rather than mislabel the cause"
            )

    record = AggregateRecord(
        case_uid=attempt_set.case_uid,
        aggregate_verdict=verdict,
        aggregate_blocker=blocker,
        execution_degraded=degraded,
        reason_code=reason,
        wins=wins,
        attempts_planned=n,
        attempts_run=attempts_run,
        derived_from_executed_quorum=from_quorum,
        quarantine_status=quarantine.status,
        # Quarantine is orthogonal: the freshly computed aggregate is ALWAYS
        # the latest result and is never displaced by quarantine metadata.
        latest_aggregate_verdict=verdict,
        latest_aggregate_blocker=blocker,
        quarantine_reason=quarantine.reason,
        quarantine_since=quarantine.since,
        waiver_ref=quarantine.waiver_ref,
    )
    record.validate()
    return record
