"""Deterministic report generator with honest coverage accounting (Phase 19).

Every report carries the complete coverage metrics, the three §13 field
groups, scheduling/budget/materialization evidence, and author-facing
findings. HONESTY GUARDS:

- no report may state an eval passed unless actual executed attempts produced
  quorum (enforced structurally by AggregateRecord and re-checked here);
- because WP-2B-1 runs no behavioral attempts, its demonstration reports keep
  every attempt UNRUN and every aggregate INCONCLUSIVE with a blocker;
- assertion ACCOUNTING coverage and assertions ACTUALLY GRADED coverage are
  distinct metrics, never conflated.
"""

from __future__ import annotations

from typing import Any, Iterable, Mapping

from . import RUNNER_VERSION, SCHEMA_VERSION
from .enums import (
    AggregateBlocker,
    AggregateVerdict,
    AttemptState,
    ReasonCode,
    RiskClass,
)
from .errors import DishonestReportError
from .models import (
    AggregateRecord,
    AttemptRecord,
    CoverageMetrics,
    default_unselected_aggregate,
    planned_unrun_attempt,
)
from .preflight import PreflightResult


def compute_coverage(
    authored_units_total: int,
    selected_case_uids: Iterable[str],
    preflight_results: Iterable[PreflightResult],
    attempts: Iterable[AttemptRecord],
    aggregates: Iterable[AggregateRecord],
    assertions_selected_total: int,
    assertions_accounted_total: int,
    assertions_actually_graded_total: int,
    critical_case_uids: Iterable[str] = (),
) -> CoverageMetrics:
    """Compute the honest coverage metrics from the run's actual records."""
    selected = sorted(set(selected_case_uids))
    preflight_by_case = {result.case_uid: result for result in preflight_results}
    attempts_by_case: dict[str, list[AttemptRecord]] = {}
    for attempt in attempts:
        attempts_by_case.setdefault(attempt.case_uid, []).append(attempt)

    runnable = [
        uid
        for uid in selected
        if uid in preflight_by_case
        and preflight_by_case[uid].outcome.value == "RUNNABLE"
    ]
    attempted = [
        uid
        for uid in runnable
        if any(
            a.attempt_state is not AttemptState.UNRUN
            for a in attempts_by_case.get(uid, [])
        )
    ]
    completed = [
        uid
        for uid in attempted
        if attempts_by_case.get(uid)
        and all(
            a.attempt_state is not AttemptState.UNRUN
            for a in attempts_by_case[uid]
        )
    ]
    critical = sorted(set(critical_case_uids))
    critical_runnable = [uid for uid in critical if uid in set(runnable)]
    critical_executed = [uid for uid in critical_runnable if uid in set(attempted)]

    unrun_totals: dict[str, int] = {}
    for case_attempts in attempts_by_case.values():
        for attempt in case_attempts:
            if attempt.attempt_state is AttemptState.UNRUN:
                key = (
                    attempt.error_reason_code.value
                    if attempt.error_reason_code
                    else ReasonCode.NOT_SELECTED.value
                )
                unrun_totals[key] = unrun_totals.get(key, 0) + 1

    excluded_totals: dict[str, int] = {}
    for aggregate in aggregates:
        if aggregate.aggregate_blocker in (
            AggregateBlocker.PRECHECK_EXCLUDED,
            AggregateBlocker.BUDGET_EXHAUSTED,
        ):
            key = aggregate.aggregate_blocker.value
            excluded_totals[key] = excluded_totals.get(key, 0) + 1

    metrics = CoverageMetrics(
        authored_units_total=authored_units_total,
        selected_units_total=len(selected),
        preflight_accounted_total=len(
            [uid for uid in selected if uid in preflight_by_case]
        ),
        runnable_units_total=len(runnable),
        attempted_units_total=len(attempted),
        completed_units_total=len(completed),
        assertions_selected_total=assertions_selected_total,
        assertions_accounted_total=assertions_accounted_total,
        assertions_actually_graded_total=assertions_actually_graded_total,
        critical_runnable_total=len(critical_runnable),
        critical_executed_total=len(critical_executed),
        unrun_totals_by_reason=dict(sorted(unrun_totals.items())),
        excluded_totals_by_reason=dict(sorted(excluded_totals.items())),
    )
    metrics.validate()
    return metrics


def _enforce_honesty(
    attempts: list[AttemptRecord], aggregates: list[AggregateRecord]
) -> None:
    executed_by_case: dict[str, int] = {}
    for attempt in attempts:
        if attempt.attempt_state in (AttemptState.PASS, AttemptState.FAIL):
            executed_by_case[attempt.case_uid] = (
                executed_by_case.get(attempt.case_uid, 0) + 1
            )
    for aggregate in aggregates:
        aggregate.validate()
        if aggregate.aggregate_verdict in (
            AggregateVerdict.PASS,
            AggregateVerdict.FAIL,
        ):
            executed = executed_by_case.get(aggregate.case_uid, 0)
            if executed < aggregate.wins or executed == 0:
                raise DishonestReportError(
                    f"{aggregate.case_uid}: verdict "
                    f"{aggregate.aggregate_verdict.value} without matching "
                    "executed attempts — a report may never state an eval "
                    "passed unless actual executed attempts produced quorum"
                )


def _validate_report_records(
    run_id: str,
    attempts_list: list[AttemptRecord],
    aggregates_list: list[AggregateRecord],
) -> None:
    """A2: enforce attempt-identity and aggregate-completeness before a report.

    Rejects cross-run attempts, duplicate repetitions, out-of-range repetition
    numbers, duplicate aggregates, attempts for a case without an aggregate,
    and an aggregate missing exactly its planned attempt identities. Duplicate
    or cross-run attempts can never count as evidence.
    """
    aggregate_by_case: dict[str, AggregateRecord] = {}
    for aggregate in aggregates_list:
        if aggregate.case_uid in aggregate_by_case:
            raise DishonestReportError(
                f"duplicate aggregate for case {aggregate.case_uid}"
            )
        aggregate_by_case[aggregate.case_uid] = aggregate

    reps_by_case: dict[str, set[int]] = {}
    for attempt in attempts_list:
        if attempt.run_id != run_id:
            raise DishonestReportError(
                f"attempt {attempt.identity} belongs to a different run than "
                f"the report ({run_id})"
            )
        aggregate = aggregate_by_case.get(attempt.case_uid)
        if aggregate is None:
            raise DishonestReportError(
                f"attempt for case {attempt.case_uid} has no aggregate"
            )
        if not (1 <= attempt.repetition_number <= aggregate.attempts_planned):
            raise DishonestReportError(
                f"attempt repetition {attempt.repetition_number} for "
                f"{attempt.case_uid} outside 1..{aggregate.attempts_planned}"
            )
        seen = reps_by_case.setdefault(attempt.case_uid, set())
        if attempt.repetition_number in seen:
            raise DishonestReportError(
                f"duplicate attempt repetition {attempt.repetition_number} for "
                f"{attempt.case_uid} — duplicates never count as evidence"
            )
        seen.add(attempt.repetition_number)

    attempts_by_case: dict[str, list[AttemptRecord]] = {}
    for attempt in attempts_list:
        attempts_by_case.setdefault(attempt.case_uid, []).append(attempt)

    for case_uid, aggregate in aggregate_by_case.items():
        present = reps_by_case.get(case_uid, set())
        expected = set(range(1, aggregate.attempts_planned + 1))
        if present != expected:
            raise DishonestReportError(
                f"aggregate {case_uid} expects planned attempts {sorted(expected)} "
                f"but the report carries {sorted(present)}"
            )
        case_attempts = attempts_by_case.get(case_uid, [])
        executed = sum(
            1 for a in case_attempts if a.attempt_state is not AttemptState.UNRUN
        )
        if aggregate.attempts_run != executed:
            raise DishonestReportError(
                f"aggregate {case_uid} claims attempts_run={aggregate.attempts_run} "
                f"but {executed} of its attempts actually executed"
            )
        if aggregate.aggregate_verdict is AggregateVerdict.PASS:
            actual_wins = sum(
                1 for a in case_attempts if a.attempt_state is AttemptState.PASS
            )
        elif aggregate.aggregate_verdict is AggregateVerdict.FAIL:
            actual_wins = sum(
                1 for a in case_attempts if a.attempt_state is AttemptState.FAIL
            )
        else:
            actual_wins = 0
        if aggregate.wins != actual_wins:
            raise DishonestReportError(
                f"aggregate {case_uid} claims wins={aggregate.wins} but "
                f"{actual_wins} attempts actually won"
            )


def build_run_report(
    run_id: str,
    baseline_identity: Mapping[str, Any],
    run_provenance: Mapping[str, Any],
    input_evidence_manifest_sha256: str | None,
    attempts: Iterable[AttemptRecord],
    aggregates: Iterable[AggregateRecord],
    coverage: CoverageMetrics,
    scheduling_evidence: Mapping[str, Any] | None = None,
    budget_totals: Mapping[str, Any] | None = None,
    materialization: Mapping[str, Any] | None = None,
    execution_profile: Mapping[str, Any] | None = None,
    findings: Iterable[Mapping[str, Any]] = (),
    risk_classes: Mapping[str, str] | None = None,
    *,
    selected_case_uids: Iterable[str] = (),
    preflight_results: Iterable[PreflightResult] = (),
    critical_case_uids: Iterable[str] = (),
    assertions_selected_total: int = 0,
    assertions_accounted_total: int = 0,
    assertions_actually_graded_total: int = 0,
) -> dict[str, Any]:
    """Assemble the deterministic run report (sorted, canonicalizable).

    Coverage is RECOMPUTED from the run's own records and required to equal the
    caller-supplied ``coverage`` (A3): a fabricated coverage — e.g. 100% over an
    empty run — is rejected, never published.
    """
    if not run_id:
        raise DishonestReportError("run_id required")
    attempts_list = sorted(
        attempts, key=lambda a: (a.case_uid, a.repetition_number)
    )
    aggregates_list = sorted(aggregates, key=lambda a: a.case_uid)
    for attempt in attempts_list:
        attempt.validate()
    _validate_report_records(run_id, attempts_list, aggregates_list)
    _enforce_honesty(attempts_list, aggregates_list)
    coverage.validate()

    # A3: derive coverage from the records and reject any caller mismatch.
    recomputed = compute_coverage(
        authored_units_total=coverage.authored_units_total,
        selected_case_uids=selected_case_uids,
        preflight_results=preflight_results,
        attempts=attempts_list,
        aggregates=aggregates_list,
        assertions_selected_total=assertions_selected_total,
        assertions_accounted_total=assertions_accounted_total,
        assertions_actually_graded_total=assertions_actually_graded_total,
        critical_case_uids=critical_case_uids,
    )
    if recomputed.to_dict() != coverage.to_dict():
        raise DishonestReportError(
            "supplied coverage metrics do not match the coverage recomputed "
            "from selection/preflight/attempts/aggregates — coverage is "
            "evidence, not a caller assertion"
        )

    quarantine_inventory = [
        {
            "case_uid": aggregate.case_uid,
            "quarantine_status": aggregate.quarantine_status.value,
            "quarantine_reason": aggregate.quarantine_reason,
            "quarantine_since": aggregate.quarantine_since,
            "latest_aggregate_verdict": (
                aggregate.latest_aggregate_verdict.value
                if aggregate.latest_aggregate_verdict
                else None
            ),
            "latest_aggregate_blocker": (
                aggregate.latest_aggregate_blocker.value
                if aggregate.latest_aggregate_blocker
                else None
            ),
            "waiver_ref": aggregate.waiver_ref,
            "risk_class": (
                (risk_classes or {}).get(aggregate.case_uid, RiskClass.STANDARD.value)
            ),
        }
        for aggregate in aggregates_list
        if aggregate.quarantine_status.value == "ACTIVE"
    ]

    report: dict[str, Any] = {
        "report_kind": "behavioral_eval_run_report",
        "schema_version": SCHEMA_VERSION,
        "runner_version": RUNNER_VERSION,
        "run_id": run_id,
        "baseline_identity": dict(baseline_identity),
        "run_provenance": dict(run_provenance),
        "run_evidence_binding": (
            {"input_evidence_manifest_sha256": input_evidence_manifest_sha256}
            if input_evidence_manifest_sha256
            else {"input_evidence_manifest_sha256": None, "status": "UNFINALIZED"}
        ),
        "coverage_metrics": coverage.to_dict(),
        "scheduling": dict(scheduling_evidence or {}),
        "budget_totals": dict(
            budget_totals
            or {"reserved": {}, "actual": {}, "released": {}, "monetary_spend": "UNKNOWN"}
        ),
        "materialization": dict(materialization or {}),
        "execution_profile": dict(execution_profile or {}),
        "risk_class_governance": (
            "risk classes are PROPOSED / NOT OWNER-RATIFIED (OD-3) and control "
            "no live behavior or promotion in WP-2B-1"
        ),
        "aggregates": [a.to_dict() for a in aggregates_list],
        "attempts": [a.to_dict() for a in attempts_list],
        "quarantine_inventory": quarantine_inventory,
        "author_facing_findings": sorted(
            (dict(f) for f in findings),
            key=lambda f: (str(f.get("finding_kind", "")), str(f.get("case_uid", ""))),
        ),
        "non_claims": [
            "no live behavioral attempt was executed by WP-2B-1",
            "no eval is claimed to pass",
            "real-host capabilities remain UNAVAILABLE/UNKNOWN (R1-R5)",
        ],
    }
    return report


def build_demonstration_report(
    run_id: str,
    case_uids: Iterable[str],
    authored_units_total: int,
    attempts_planned_per_case: int = 3,
) -> dict[str, Any]:
    """The WP-2B-1 demonstration report: everything honestly UNRUN.

    Attempts stay UNRUN, aggregates stay INCONCLUSIVE with NOT_SELECTED —
    the report shape itself proves nothing ran.
    """
    uids = sorted(set(case_uids))
    attempts: list[AttemptRecord] = []
    aggregates: list[AggregateRecord] = []
    for uid in uids:
        for repetition in range(1, attempts_planned_per_case + 1):
            attempts.append(
                planned_unrun_attempt(run_id, uid, repetition, ReasonCode.NOT_SELECTED)
            )
        aggregates.append(
            default_unselected_aggregate(uid, attempts_planned=attempts_planned_per_case)
        )
    coverage = compute_coverage(
        authored_units_total=authored_units_total,
        selected_case_uids=[],
        preflight_results=[],
        attempts=attempts,
        aggregates=aggregates,
        assertions_selected_total=0,
        assertions_accounted_total=0,
        assertions_actually_graded_total=0,
    )
    return build_run_report(
        run_id=run_id,
        baseline_identity={
            "runner_version": RUNNER_VERSION,
            "schema_version": SCHEMA_VERSION,
            "note": "demonstration report; no system under test exists in WP-2B-1",
        },
        run_provenance={"selection": "none", "demonstration_only": True},
        input_evidence_manifest_sha256=None,
        attempts=attempts,
        aggregates=aggregates,
        coverage=coverage,
    )
