"""Shared plumbing for the WP-2B-2 deterministic graders.

Every grader takes ONE recorded-evidence mapping and returns a hash-bound
``GraderResult``. Malformed evidence becomes result_state=ERROR with
reason_code=EVIDENCE_MALFORMED (fail closed) — never an unhandled exception
for recorded-data problems, and never a verdict. Graders may raise
``GradingError`` with a specific error reason (e.g. AMBIGUOUS_ACTIVATION).
"""

from __future__ import annotations

from typing import Any, Callable, Mapping

from ..canonical import sha256_of_obj
from ..errors import SchemaValidationError
from .records import (
    GraderResult,
    GraderResultState,
    GradingReasonCode,
    make_grader_result,
)


class GradingError(Exception):
    """Raised inside a grader body for a fail-closed ERROR (non-verdict)."""

    def __init__(
        self,
        reason: GradingReasonCode,
        detail: str,
        extra: Mapping[str, Any] | None = None,
    ) -> None:
        super().__init__(detail)
        self.reason = reason
        self.detail = detail
        self.extra = dict(extra or {})


class EvidenceMalformed(GradingError):
    """Recorded evidence is malformed: ERROR / EVIDENCE_MALFORMED."""

    def __init__(self, detail: str, extra: Mapping[str, Any] | None = None) -> None:
        super().__init__(GradingReasonCode.EVIDENCE_MALFORMED, detail, extra)


class GradingFail(Exception):
    """Raised inside a grader body to report a deterministic FAIL."""

    def __init__(
        self,
        reason: GradingReasonCode,
        detail: str,
        extra: Mapping[str, Any] | None = None,
    ) -> None:
        super().__init__(detail)
        self.reason = reason
        self.detail = detail
        self.extra = dict(extra or {})


def require_keys(
    evidence: Mapping[str, Any], allowed: frozenset[str], required: frozenset[str]
) -> None:
    unknown = set(evidence) - set(allowed)
    if unknown:
        raise EvidenceMalformed(f"unknown evidence keys {sorted(unknown)}")
    missing = set(required) - set(evidence)
    if missing:
        raise EvidenceMalformed(f"missing evidence keys {sorted(missing)}")


def require_str(container: Mapping[str, Any], key: str) -> str:
    value = container.get(key)
    if not isinstance(value, str) or not value:
        # Report the key and TYPE only — never echo malformed content (which
        # may be transcript text) into diagnostics or results.
        raise EvidenceMalformed(
            f"{key} must be a non-empty string, got {type(value).__name__}"
        )
    return value


def require_bool(container: Mapping[str, Any], key: str) -> bool:
    value = container.get(key)
    if not isinstance(value, bool):
        raise EvidenceMalformed(f"{key} must be a boolean, got {value!r}")
    return value


def require_list(container: Mapping[str, Any], key: str) -> list[Any]:
    value = container.get(key)
    if not isinstance(value, list):
        raise EvidenceMalformed(f"{key} must be a list, got {value!r}")
    return value


def run_grader(
    grader_id: str,
    oracle_id: str,
    plan: "TrustedGradingPlan",
    evidence: Mapping[str, Any],
    body: Callable[["TrustedGradingPlan", Mapping[str, Any]], dict[str, Any]],
) -> GraderResult:
    """Execute a grader body with the shared fail-closed envelope.

    The TRUSTED grading plan and the OBSERVED evidence arrive as separate,
    mechanically distinct inputs: the plan must be a validated
    ``TrustedGradingPlan`` (a raw mapping is refused), the case identity and
    grading criteria come only from the plan, and the result binds
    ``trusted_grading_plan`` and ``observed_evidence`` hashes separately.

    ``body`` returns the PASS reproduction payload, raises ``GradingFail``
    for a deterministic FAIL, or raises ``GradingError`` (including
    ``EvidenceMalformed``) for a non-verdict ERROR.
    """
    from .plan import TrustedGradingPlan  # local import: avoids module cycle

    if not isinstance(plan, TrustedGradingPlan):
        raise SchemaValidationError(
            "the trusted grading plan must be a TrustedGradingPlan instance; "
            "a raw mapping cannot carry grading criteria"
        )
    plan.validate()
    if oracle_id not in plan.required_oracle_ids:
        raise SchemaValidationError(
            f"oracle {oracle_id!r} is not in the plan's required oracle set "
            f"for {plan.control_id}: {list(plan.required_oracle_ids)}"
        )
    if not isinstance(evidence, Mapping):
        raise SchemaValidationError("observed evidence must be a mapping")
    pointer = evidence.get("evidence_pointer")
    if not isinstance(pointer, str) or not pointer:
        raise SchemaValidationError("evidence.evidence_pointer is required")
    observed_hash = sha256_of_obj({k: evidence[k] for k in sorted(evidence)})

    state = GraderResultState.PASS
    reason: GradingReasonCode | None = None
    reproduction: dict[str, Any]
    try:
        reproduction = body(plan, evidence)
    except GradingFail as fail:
        state = GraderResultState.FAIL
        reason = fail.reason
        reproduction = {"failure_detail": fail.detail, **fail.extra}
    except GradingError as error:
        state = GraderResultState.ERROR
        reason = error.reason
        reproduction = {"error_detail": error.detail, **error.extra}

    return make_grader_result(
        grader_id=grader_id,
        oracle_id=oracle_id,
        control_id=plan.control_id,
        case_uid=plan.case_uid,
        result_state=state,
        reason_code=reason,
        evidence_pointers=(pointer,),
        input_sha256s={
            "trusted_grading_plan": plan.plan_sha256,
            "observed_evidence": observed_hash,
        },
        reproduction=reproduction,
    )
