"""Closed, versioned enum sets for the WP-2B-1 runner schemas.

Every set is CLOSED: parsing an unknown value raises UnknownEnumValueError.
New members are added only through a versioned schema change, never free text.
"""

from __future__ import annotations

import enum

from .errors import UnknownEnumValueError


class StrictEnum(enum.Enum):
    """Enum base with strict, closed parsing."""

    @classmethod
    def parse(cls, value: object) -> "StrictEnum":
        if isinstance(value, cls):
            return value
        if isinstance(value, str):
            for member in cls:
                if member.value == value:
                    return member
        raise UnknownEnumValueError(
            f"{cls.__name__}: unknown value {value!r}; allowed: "
            f"{sorted(m.value for m in cls)}"
        )

    @classmethod
    def values(cls) -> list[str]:
        return [m.value for m in cls]

    def __str__(self) -> str:  # pragma: no cover - convenience
        return str(self.value)


class AttemptState(StrictEnum):
    """Per-attempt state. UNRUN means exactly 'this planned attempt was NOT run'."""

    PASS = "PASS"
    FAIL = "FAIL"
    ERROR = "ERROR"
    JUDGE_ERROR = "JUDGE_ERROR"
    UNRUN = "UNRUN"


class AggregateVerdict(StrictEnum):
    """Case-level verdict; the only three values."""

    PASS = "PASS"
    FAIL = "FAIL"
    INCONCLUSIVE = "INCONCLUSIVE"


class AggregateBlocker(StrictEnum):
    """Why an INCONCLUSIVE case is inconclusive (NONE on PASS/FAIL)."""

    NONE = "NONE"
    ERROR = "ERROR"
    JUDGE_ERROR = "JUDGE_ERROR"
    INSUFFICIENT_ATTEMPTS = "INSUFFICIENT_ATTEMPTS"
    PRECHECK_EXCLUDED = "PRECHECK_EXCLUDED"
    BUDGET_EXHAUSTED = "BUDGET_EXHAUSTED"
    NOT_SELECTED = "NOT_SELECTED"


#: Precedence order for assigning the blocker of a no-quorum case (design §10).
BLOCKER_PRECEDENCE = (
    AggregateBlocker.ERROR,
    AggregateBlocker.JUDGE_ERROR,
    AggregateBlocker.INSUFFICIENT_ATTEMPTS,
    AggregateBlocker.PRECHECK_EXCLUDED,
    AggregateBlocker.BUDGET_EXHAUSTED,
    AggregateBlocker.NOT_SELECTED,
)


class QuarantineStatus(StrictEnum):
    """Orthogonal quarantine metadata; never erases the latest aggregate verdict."""

    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"


class RiskClass(StrictEnum):
    """Case risk class. Census-produced values remain PROPOSED until OD-3."""

    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    STANDARD = "STANDARD"


class ClaimScope(StrictEnum):
    FULL_LIBRARY = "full_library"
    PARTIAL_INSTALL = "partial_install"


class RuntimeClassification(StrictEnum):
    """Per-file runtime-surface classification; ambiguity fails closed."""

    RUNTIME_REQUIRED = "runtime_required"
    CONTROL_PLANE_ONLY = "control_plane_only"
    AMBIGUOUS_NEEDS_OWNER_REVIEW = "ambiguous_needs_owner_review"


class PreflightOutcome(StrictEnum):
    RUNNABLE = "RUNNABLE"
    PRECHECK_EXCLUDED = "PRECHECK_EXCLUDED"
    FIXTURE_SETUP_FAILED = "FIXTURE_SETUP_FAILED"


class ReasonCode(StrictEnum):
    """Versioned reason codes carried by attempts/aggregates/errors."""

    AMBIGUOUS_ACTIVATION = "AMBIGUOUS_ACTIVATION"
    MISSING_PREREQUISITE = "MISSING_PREREQUISITE"
    MISSING_FIXTURE = "MISSING_FIXTURE"
    FIXTURE_SETUP_FAILED = "FIXTURE_SETUP_FAILED"
    INCOMPATIBLE_INVOCATION_MODE = "INCOMPATIBLE_INVOCATION_MODE"
    UNJUDGEABLE_ASSERTION = "UNJUDGEABLE_ASSERTION"
    BUDGET_CAP = "BUDGET_CAP"
    EVIDENCE_INTEGRITY_FAILURE = "EVIDENCE_INTEGRITY_FAILURE"
    LIVE_DISPATCH_DISABLED = "LIVE_DISPATCH_DISABLED"
    NOT_SELECTED = "NOT_SELECTED"


#: Reason codes that mark a preflight exclusion (aggregate PRECHECK_EXCLUDED).
PRECHECK_REASON_CODES = frozenset(
    {
        ReasonCode.MISSING_PREREQUISITE,
        ReasonCode.MISSING_FIXTURE,
        ReasonCode.INCOMPATIBLE_INVOCATION_MODE,
        ReasonCode.UNJUDGEABLE_ASSERTION,
    }
)


class CapabilityState(StrictEnum):
    """Truthful capability disposition; unproven capabilities never claim more."""

    AVAILABLE = "AVAILABLE"
    UNAVAILABLE = "UNAVAILABLE"
    UNKNOWN = "UNKNOWN"
    DISABLED = "DISABLED"


class MaterializationProfile(StrictEnum):
    CONSUMER_SKILLS_ONLY = "consumer_skills_only"
    CONSUMER_WITH_STARTUP_ROUTING = "consumer_with_startup_routing"
    CONSUMER_WITH_SUBAGENTS = "consumer_with_subagents"
    SOURCE_LIBRARY = "source_library"
    CONSUMER_PARTIAL_INSTALL = "consumer_partial_install"


class WorkspaceRole(StrictEnum):
    CONSUMER = "consumer"
    SOURCE_LIBRARY = "source_library"


class TargetKind(StrictEnum):
    SKILL = "skill"
    SUBAGENT = "subagent"


class EvalFileKind(StrictEnum):
    BEHAVIOR_EVAL = "behavior_eval"
    TRIGGER_EVAL = "trigger_eval"
    CONVERSATION_SUITE = "conversation_suite"


class CaseType(StrictEnum):
    """Authored case types as found in the corpus, plus runner-typed variants."""

    SHOULD_TRIGGER = "should_trigger"
    SHOULD_NOT_TRIGGER = "should_not_trigger"
    SHOULD_NOT_DO = "should_not_do"
    DISCRIMINATION = "discrimination"
    DISCRIMINATION_EMPTY_NEIGHBOR = "discrimination_empty_neighbor"
    CONVERSATION_SUITE = "conversation_suite"


class InvocationMode(StrictEnum):
    MODEL_SELECTED = "model_selected"
    EXPLICIT_SKILL_INVOCATION = "explicit_skill_invocation"
    DELEGATED_SUBAGENT = "delegated_subagent"


class Tier(StrictEnum):
    PR = "pr"
    CADENCE = "cadence"
    FULL = "full"


class SchedulingPriority(enum.IntEnum):
    """Versioned risk-aware scheduling priorities (design §11a; lower runs first)."""

    CRITICAL_REGRESSION = 1
    CRITICAL_SAFETY = 2
    CANONICAL_REGRESSION_SUITE = 3
    CHANGED_SKILL = 4
    REVERSE_NEIGHBOR_EDGE = 5
    NAMED_NEIGHBOR = 6
    HIGH_RISK = 7
    STANDARD_CHANGED_SCOPE = 8
    CADENCE_ONLY = 9

    @classmethod
    def parse(cls, value: object) -> "SchedulingPriority":
        if isinstance(value, cls):
            return value
        if isinstance(value, int) and not isinstance(value, bool):
            for member in cls:
                if member.value == value:
                    return member
        raise UnknownEnumValueError(
            f"SchedulingPriority: unknown value {value!r}; allowed: "
            f"{[int(m) for m in cls]}"
        )


class InclusionReason(StrictEnum):
    OWN_CASE = "own_case"
    NAMED_NEIGHBOR = "named_neighbor"
    REVERSE_EDGE = "reverse_edge"
    REGRESSION_MAPPED = "regression_mapped"
    CADENCE_SLOT = "cadence_slot"
    FULL_CORPUS = "full_corpus"


class RetentionClass(StrictEnum):
    DAYS_30 = "days_30"
    DAYS_90 = "days_90"
    DAYS_365 = "days_365"


class Sensitivity(StrictEnum):
    PUBLIC_SAFE = "PUBLIC_SAFE"
    INTERNAL = "INTERNAL"
    CONFIDENTIAL = "CONFIDENTIAL"
    SYNTHETIC = "SYNTHETIC"


class RedactionState(StrictEnum):
    SANITIZED_BY_CONSTRUCTION = "sanitized_by_construction"
    REDACTED = "redacted"
    UNREDACTED_INTERNAL_ONLY = "unredacted_internal_only"


class AssertionClassification(StrictEnum):
    """WP-2B-1 proposes candidates only; ratification is OD/owner work."""

    DETERMINISTIC_CANDIDATE = "deterministic_candidate"
    SEMANTIC_CANDIDATE = "semantic_candidate"
    UNJUDGEABLE_CANDIDATE = "unjudgeable_candidate"
