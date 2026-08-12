"""Deterministic capability/fixture preflight (design §5b; prompt Phase 11).

Preflight runs BEFORE any session spawn and decides, per case, whether the
case can honestly run. Missing setup NEVER becomes a behavioral FAIL:

- unavailable prerequisite  -> UNRUN attempts, INCONCLUSIVE + PRECHECK_EXCLUDED,
  reason MISSING_PREREQUISITE;
- missing fixture           -> same, reason MISSING_FIXTURE;
- setup failure             -> attempt ERROR, reason FIXTURE_SETUP_FAILED;
- MANUAL-ONLY positive without authorized explicit invocation
                            -> UNRUN, PRECHECK_EXCLUDED, INCOMPATIBLE_INVOCATION_MODE;
- required unjudgeable assertion
                            -> UNRUN, PRECHECK_EXCLUDED, UNJUDGEABLE_ASSERTION.

Every exclusion produces an author-facing finding.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from .enums import (
    AggregateBlocker,
    AggregateVerdict,
    AttemptState,
    InvocationMode,
    PreflightOutcome,
    ReasonCode,
)
from .errors import PreflightError
from .models import CaseManifestRecord
from .pathsafe import UnsafePathError, normalize_relative_path


@dataclass(frozen=True, slots=True)
class PreflightEnvironment:
    """The deterministic capability surface available to a run."""

    available_language_runtimes: frozenset[str] = frozenset()
    available_frameworks: frozenset[str] = frozenset()
    available_commands: frozenset[str] = frozenset()
    reachable_services: frozenset[str] = frozenset()
    available_databases: frozenset[str] = frozenset()
    available_credential_classes: frozenset[str] = frozenset({"none"})
    available_fixtures: frozenset[str] = frozenset({"empty-consumer"})
    available_network_postures: frozenset[str] = frozenset({"none"})
    unjudgeable_assertion_uids: frozenset[str] = frozenset()
    #: Fixture-relative files present in the product-fixture overlay.
    available_fixture_files: frozenset[str] = frozenset()
    #: Tool permissions the sandbox allowlist grants.
    available_tool_permissions: frozenset[str] = frozenset()


@dataclass(frozen=True, slots=True)
class AuthorFacingFinding:
    finding_kind: str
    case_uid: str
    owner: str
    detail: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "finding_kind": self.finding_kind,
            "case_uid": self.case_uid,
            "owner": self.owner,
            "detail": self.detail,
        }


@dataclass(frozen=True, slots=True)
class PreflightResult:
    case_uid: str
    outcome: PreflightOutcome
    reason_code: ReasonCode | None
    planned_attempt_state: AttemptState
    aggregate_verdict: AggregateVerdict | None
    aggregate_blocker: AggregateBlocker | None
    findings: tuple[AuthorFacingFinding, ...] = field(default_factory=tuple)

    def to_dict(self) -> dict[str, Any]:
        return {
            "case_uid": self.case_uid,
            "outcome": self.outcome.value,
            "reason_code": self.reason_code.value if self.reason_code else None,
            "planned_attempt_state": self.planned_attempt_state.value,
            "aggregate_verdict": (
                self.aggregate_verdict.value if self.aggregate_verdict else None
            ),
            "aggregate_blocker": (
                self.aggregate_blocker.value if self.aggregate_blocker else None
            ),
            "findings": [finding.to_dict() for finding in self.findings],
        }


def _excluded(
    case: CaseManifestRecord,
    reason: ReasonCode,
    finding_kind: str,
    detail: str,
) -> PreflightResult:
    finding = AuthorFacingFinding(
        finding_kind=finding_kind,
        case_uid=case.case_uid,
        owner=case.owner,
        detail=detail,
    )
    return PreflightResult(
        case_uid=case.case_uid,
        outcome=PreflightOutcome.PRECHECK_EXCLUDED,
        reason_code=reason,
        planned_attempt_state=AttemptState.UNRUN,
        aggregate_verdict=AggregateVerdict.INCONCLUSIVE,
        aggregate_blocker=AggregateBlocker.PRECHECK_EXCLUDED,
        findings=(finding,),
    )


def evaluate_case(
    case: CaseManifestRecord, environment: PreflightEnvironment
) -> PreflightResult:
    """Deterministic preflight for one case. Never dispatches anything."""
    case.validate()

    # 1. MANUAL-ONLY invocation-mode compatibility (design §5c). Negative cases
    #    still run; a positive expectation on a MANUAL-ONLY target is
    #    dispatchable only when explicit invocation is genuinely authorized by
    #    the authored case.
    positive_expectation = case.case_type.value in (
        "should_trigger",
        "should_not_do",
        "discrimination",
        "discrimination_empty_neighbor",
    )
    if (
        case.manual_only_target
        and positive_expectation
        and case.activation_mode_expected is InvocationMode.MODEL_SELECTED
    ):
        return _excluded(
            case,
            ReasonCode.INCOMPATIBLE_INVOCATION_MODE,
            "manual_only_incompatible_positive",
            "MANUAL-ONLY target cannot be model-selected; the case neither "
            "names nor authorizes explicit invocation",
        )
    if (
        case.manual_only_target
        and positive_expectation
        and case.activation_mode_expected is InvocationMode.EXPLICIT_SKILL_INVOCATION
        and not case.explicit_invocation_authorized
    ):
        return _excluded(
            case,
            ReasonCode.INCOMPATIBLE_INVOCATION_MODE,
            "manual_only_unauthorized_explicit_invocation",
            "explicit invocation is not authorized by the authored case text",
        )

    # 2. Required unjudgeable assertion blocks full PASS -> not dispatched.
    for assertion in case.assertions:
        if assertion.assertion_uid in environment.unjudgeable_assertion_uids:
            return _excluded(
                case,
                ReasonCode.UNJUDGEABLE_ASSERTION,
                "unjudgeable_required_assertion",
                f"required assertion {assertion.index} is unjudgeable as "
                "written; the runner never rewrites assertions",
            )

    # 3. Fixture availability.
    if case.workspace_fixture_id not in environment.available_fixtures:
        return _excluded(
            case,
            ReasonCode.MISSING_FIXTURE,
            "missing_fixture",
            f"fixture {case.workspace_fixture_id!r} (version "
            f"{case.fixture_version!r}) is not available",
        )

    # 4. Capability prerequisites.
    requirement_checks: tuple[tuple[str, tuple[str, ...], frozenset[str]], ...] = (
        (
            "language runtime",
            case.required_language_runtime,
            environment.available_language_runtimes,
        ),
        ("framework", case.required_framework, environment.available_frameworks),
        ("command", case.required_commands, environment.available_commands),
        ("service", case.required_services, environment.reachable_services),
        ("database", case.required_database, environment.available_databases),
    )
    for label, required, available in requirement_checks:
        missing = sorted(set(required) - set(available))
        if missing:
            return _excluded(
                case,
                ReasonCode.MISSING_PREREQUISITE,
                "missing_prerequisite",
                f"required {label}(s) unavailable: {missing}",
            )

    # Group B: required fixture-relative files must be present in the overlay.
    normalized_required: list[str] = []
    for raw in case.required_files:
        try:
            normalized_required.append(normalize_relative_path(raw))
        except UnsafePathError as exc:
            return _excluded(
                case,
                ReasonCode.MISSING_PREREQUISITE,
                "unsafe_required_file_path",
                f"required file path {raw!r} is unsafe: {exc}",
            )
    available_files = {
        normalize_relative_path(p) for p in environment.available_fixture_files
    }
    missing_files = sorted(set(normalized_required) - available_files)
    if missing_files:
        return _excluded(
            case,
            ReasonCode.MISSING_PREREQUISITE,
            "missing_required_file",
            f"required file(s) absent from the fixture: {missing_files}",
        )

    # Group B: required tool permissions must be granted by the sandbox.
    missing_permissions = sorted(
        set(case.required_tool_permissions) - set(environment.available_tool_permissions)
    )
    if missing_permissions:
        return _excluded(
            case,
            ReasonCode.MISSING_PREREQUISITE,
            "missing_tool_permission",
            f"required tool permission(s) not granted: {missing_permissions}",
        )

    if case.required_network_posture not in environment.available_network_postures:
        return _excluded(
            case,
            ReasonCode.MISSING_PREREQUISITE,
            "missing_prerequisite",
            f"required network posture {case.required_network_posture!r} "
            "unavailable (egress is deny-by-default)",
        )
    if (
        case.required_credentials_class != "none"
        and case.required_credentials_class
        not in environment.available_credential_classes
    ):
        return _excluded(
            case,
            ReasonCode.MISSING_PREREQUISITE,
            "missing_prerequisite",
            f"required credentials class {case.required_credentials_class!r} "
            "unavailable (production credentials are never supplied)",
        )

    return PreflightResult(
        case_uid=case.case_uid,
        outcome=PreflightOutcome.RUNNABLE,
        reason_code=None,
        planned_attempt_state=AttemptState.UNRUN,  # honest default until dispatched
        aggregate_verdict=None,
        aggregate_blocker=None,
        findings=(),
    )


def fixture_setup_failure(case: CaseManifestRecord, detail: str) -> PreflightResult:
    """A fixture/setup ATTEMPT failed during materialization: attempt ERROR.

    This is an execution-time infrastructure failure, never a behavioral FAIL.
    """
    if not detail:
        raise PreflightError("fixture_setup_failure requires a detail message")
    finding = AuthorFacingFinding(
        finding_kind="fixture_setup_failed",
        case_uid=case.case_uid,
        owner=case.owner,
        detail=detail,
    )
    return PreflightResult(
        case_uid=case.case_uid,
        outcome=PreflightOutcome.FIXTURE_SETUP_FAILED,
        reason_code=ReasonCode.FIXTURE_SETUP_FAILED,
        planned_attempt_state=AttemptState.ERROR,
        aggregate_verdict=None,  # aggregate follows §10 precedence over attempts
        aggregate_blocker=None,
        findings=(finding,),
    )
