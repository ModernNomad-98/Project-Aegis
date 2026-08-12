"""Versioned, strictly validated runner records (design §10, §13).

Records are frozen dataclasses with closed field sets. ``from_dict`` rejects
unknown keys and unknown enum values; ``validate`` enforces the honesty
invariants (UNRUN default, no defaulted PASS/FAIL, blocker discipline).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping

from . import SCHEMA_VERSION
from .enums import (
    AggregateBlocker,
    AggregateVerdict,
    AssertionClassification,
    AttemptState,
    CaseType,
    ClaimScope,
    EvalFileKind,
    InvocationMode,
    MaterializationProfile,
    QuarantineStatus,
    ReasonCode,
    RiskClass,
    TargetKind,
    WorkspaceRole,
)
from .errors import SchemaValidationError
from .identity import parse_case_uid

MONETARY_UNKNOWN = "UNKNOWN"


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise SchemaValidationError(message)


def _check_keys(payload: Mapping[str, Any], allowed: frozenset[str], where: str) -> None:
    unknown = set(payload) - set(allowed)
    _require(not unknown, f"{where}: unknown keys {sorted(unknown)}")


def _non_negative_int(value: Any, where: str) -> int:
    _require(
        isinstance(value, int) and not isinstance(value, bool) and value >= 0,
        f"{where} must be a non-negative int, got {value!r}",
    )
    return value


def _str_tuple(value: Any, where: str) -> tuple[str, ...]:
    _require(
        isinstance(value, (list, tuple))
        and all(isinstance(item, str) for item in value),
        f"{where} must be a list of strings, got {value!r}",
    )
    return tuple(value)


@dataclass(frozen=True, slots=True)
class TypedTarget:
    """Typed activation target (design §5d): skill vs subagent, never collapsed."""

    target_kind: TargetKind
    target_name: str
    target_annotation: str | None = None

    def validate(self) -> None:
        _require(isinstance(self.target_kind, TargetKind), "target_kind must be TargetKind")
        _require(
            isinstance(self.target_name, str) and bool(self.target_name),
            "target_name must be a non-empty string",
        )
        if self.target_annotation is not None:
            _require(
                isinstance(self.target_annotation, str),
                "target_annotation must be a string or None",
            )

    def to_dict(self) -> dict[str, Any]:
        return {
            "target_kind": self.target_kind.value,
            "target_name": self.target_name,
            "target_annotation": self.target_annotation,
        }

    _KEYS = frozenset({"target_kind", "target_name", "target_annotation"})

    @classmethod
    def from_dict(cls, payload: Mapping[str, Any]) -> "TypedTarget":
        _check_keys(payload, cls._KEYS, "TypedTarget")
        target = cls(
            target_kind=TargetKind.parse(payload.get("target_kind")),
            target_name=payload.get("target_name", ""),
            target_annotation=payload.get("target_annotation"),
        )
        target.validate()
        return target


def parse_target(raw_expected: str) -> TypedTarget:
    """Parse an authored target string, honoring the ``(subagent)`` annotation."""
    _require(
        isinstance(raw_expected, str) and bool(raw_expected.strip()),
        f"expected target must be a non-empty string, got {raw_expected!r}",
    )
    text = raw_expected.strip()
    marker = "(subagent)"
    if text.endswith(marker):
        name = text[: -len(marker)].strip()
        _require(bool(name), f"subagent target has no name: {raw_expected!r}")
        return TypedTarget(TargetKind.SUBAGENT, name, marker)
    return TypedTarget(TargetKind.SKILL, text, None)


@dataclass(frozen=True, slots=True)
class AssertionRecord:
    assertion_uid: str
    index: int
    text: str
    proposed_classification: AssertionClassification | None = None

    def validate(self) -> None:
        _require(
            isinstance(self.assertion_uid, str) and self.assertion_uid.count("::") >= 5,
            "assertion_uid must be a case_uid-scoped identity",
        )
        _non_negative_int(self.index, "AssertionRecord.index")
        _require(
            isinstance(self.text, str) and bool(self.text),
            "assertion text must be non-empty",
        )
        if self.proposed_classification is not None:
            _require(
                isinstance(self.proposed_classification, AssertionClassification),
                "proposed_classification must be AssertionClassification or None",
            )

    def to_dict(self) -> dict[str, Any]:
        return {
            "assertion_uid": self.assertion_uid,
            "index": self.index,
            "text": self.text,
            "proposed_classification": (
                self.proposed_classification.value
                if self.proposed_classification is not None
                else None
            ),
        }

    _KEYS = frozenset({"assertion_uid", "index", "text", "proposed_classification"})

    @classmethod
    def from_dict(cls, payload: Mapping[str, Any]) -> "AssertionRecord":
        _check_keys(payload, cls._KEYS, "AssertionRecord")
        classification = payload.get("proposed_classification")
        record = cls(
            assertion_uid=payload.get("assertion_uid", ""),
            index=payload.get("index", -1),
            text=payload.get("text", ""),
            proposed_classification=(
                AssertionClassification.parse(classification)
                if classification is not None
                else None
            ),
        )
        record.validate()
        return record


@dataclass(frozen=True, slots=True)
class CostUsage:
    """Reserved-vs-actual accounting; monetary may be honestly UNKNOWN."""

    reserved_max: Mapping[str, int] = field(default_factory=dict)
    actual: Mapping[str, int] = field(default_factory=dict)
    released: Mapping[str, int] = field(default_factory=dict)
    monetary: str | int = MONETARY_UNKNOWN

    def validate(self) -> None:
        for name, bucket in (
            ("reserved_max", self.reserved_max),
            ("actual", self.actual),
            ("released", self.released),
        ):
            _require(isinstance(bucket, Mapping), f"CostUsage.{name} must be a mapping")
            for key, value in bucket.items():
                _require(isinstance(key, str), f"CostUsage.{name} keys must be strings")
                _non_negative_int(value, f"CostUsage.{name}[{key}]")
        if isinstance(self.monetary, str):
            _require(
                self.monetary == MONETARY_UNKNOWN,
                f"monetary string must be {MONETARY_UNKNOWN!r}, got {self.monetary!r}",
            )
        else:
            _non_negative_int(self.monetary, "CostUsage.monetary")

    def to_dict(self) -> dict[str, Any]:
        return {
            "reserved_max": dict(self.reserved_max),
            "actual": dict(self.actual),
            "released": dict(self.released),
            "monetary": self.monetary,
        }

    _KEYS = frozenset({"reserved_max", "actual", "released", "monetary"})

    @classmethod
    def from_dict(cls, payload: Mapping[str, Any]) -> "CostUsage":
        _check_keys(payload, cls._KEYS, "CostUsage")
        usage = cls(
            reserved_max=dict(payload.get("reserved_max", {})),
            actual=dict(payload.get("actual", {})),
            released=dict(payload.get("released", {})),
            monetary=payload.get("monetary", MONETARY_UNKNOWN),
        )
        usage.validate()
        return usage


#: States that represent an executed attempt reaching a verdict.
VERDICT_ATTEMPT_STATES = frozenset({AttemptState.PASS, AttemptState.FAIL})
#: States that are terminal but carry no verdict.
NON_VERDICT_TERMINAL_STATES = frozenset(
    {AttemptState.ERROR, AttemptState.JUDGE_ERROR}
)


@dataclass(frozen=True, slots=True)
class AttemptRecord:
    """Immutable per-attempt record; identity = (run_id, case_uid, repetition_number)."""

    run_id: str
    case_uid: str
    repetition_number: int
    attempt_state: AttemptState
    error_reason_code: ReasonCode | None = None
    model_runtime_id: str | None = None
    activation_evidence: Mapping[str, Any] | None = None
    assertion_results: tuple[Mapping[str, Any], ...] = ()
    cost_usage: CostUsage = field(default_factory=CostUsage)
    duration_seconds: float | None = None
    evidence_pointer: str | None = None
    schema_version: str = SCHEMA_VERSION

    def validate(self) -> None:
        _require(isinstance(self.run_id, str) and bool(self.run_id), "run_id required")
        parse_case_uid(self.case_uid)
        _require(
            isinstance(self.repetition_number, int)
            and not isinstance(self.repetition_number, bool)
            and self.repetition_number >= 1,
            "repetition_number must be >= 1",
        )
        _require(
            isinstance(self.attempt_state, AttemptState),
            "attempt_state must be AttemptState",
        )
        if self.error_reason_code is not None:
            _require(
                isinstance(self.error_reason_code, ReasonCode),
                "error_reason_code must be ReasonCode or None",
            )
        if self.attempt_state is AttemptState.UNRUN:
            _require(
                not self.assertion_results,
                "an UNRUN attempt cannot carry assertion results (it never ran)",
            )
            _require(
                self.error_reason_code is not None,
                "an UNRUN attempt must carry the reason it was not run",
            )
        if self.attempt_state in VERDICT_ATTEMPT_STATES:
            _require(
                self.error_reason_code is None,
                "a PASS/FAIL attempt must not carry an error reason code",
            )
        if self.attempt_state in NON_VERDICT_TERMINAL_STATES:
            _require(
                self.error_reason_code is not None or self.attempt_state
                is AttemptState.JUDGE_ERROR,
                "an ERROR attempt must carry a reason code",
            )
        self.cost_usage.validate()
        if self.duration_seconds is not None:
            _require(
                isinstance(self.duration_seconds, (int, float))
                and not isinstance(self.duration_seconds, bool)
                and self.duration_seconds >= 0,
                "duration_seconds must be >= 0",
            )
        _require(
            self.schema_version == SCHEMA_VERSION,
            f"schema_version must be {SCHEMA_VERSION}",
        )

    @property
    def identity(self) -> tuple[str, str, int]:
        return (self.run_id, self.case_uid, self.repetition_number)

    def to_dict(self) -> dict[str, Any]:
        return {
            "run_id": self.run_id,
            "case_uid": self.case_uid,
            "repetition_number": self.repetition_number,
            "attempt_state": self.attempt_state.value,
            "error_reason_code": (
                self.error_reason_code.value if self.error_reason_code else None
            ),
            "model_runtime_id": self.model_runtime_id,
            "activation_evidence": (
                dict(self.activation_evidence)
                if self.activation_evidence is not None
                else None
            ),
            "assertion_results": [dict(r) for r in self.assertion_results],
            "cost_usage": self.cost_usage.to_dict(),
            "duration_seconds": self.duration_seconds,
            "evidence_pointer": self.evidence_pointer,
            "schema_version": self.schema_version,
        }

    _KEYS = frozenset(
        {
            "run_id",
            "case_uid",
            "repetition_number",
            "attempt_state",
            "error_reason_code",
            "model_runtime_id",
            "activation_evidence",
            "assertion_results",
            "cost_usage",
            "duration_seconds",
            "evidence_pointer",
            "schema_version",
        }
    )

    @classmethod
    def from_dict(cls, payload: Mapping[str, Any]) -> "AttemptRecord":
        _check_keys(payload, cls._KEYS, "AttemptRecord")
        reason = payload.get("error_reason_code")
        record = cls(
            run_id=payload.get("run_id", ""),
            case_uid=payload.get("case_uid", ""),
            repetition_number=payload.get("repetition_number", 0),
            attempt_state=AttemptState.parse(payload.get("attempt_state")),
            error_reason_code=ReasonCode.parse(reason) if reason is not None else None,
            model_runtime_id=payload.get("model_runtime_id"),
            activation_evidence=payload.get("activation_evidence"),
            assertion_results=tuple(payload.get("assertion_results", ())),
            cost_usage=CostUsage.from_dict(payload.get("cost_usage", {})),
            duration_seconds=payload.get("duration_seconds"),
            evidence_pointer=payload.get("evidence_pointer"),
            schema_version=payload.get("schema_version", SCHEMA_VERSION),
        )
        record.validate()
        return record


def planned_unrun_attempt(
    run_id: str,
    case_uid: str,
    repetition_number: int,
    reason: ReasonCode = ReasonCode.NOT_SELECTED,
) -> AttemptRecord:
    """The DEFAULT state of every planned attempt: UNRUN with an explicit reason."""
    record = AttemptRecord(
        run_id=run_id,
        case_uid=case_uid,
        repetition_number=repetition_number,
        attempt_state=AttemptState.UNRUN,
        error_reason_code=reason,
    )
    record.validate()
    return record


@dataclass(frozen=True, slots=True)
class AggregateRecord:
    """Case-level aggregate (verdict + blocker + orthogonal quarantine)."""

    case_uid: str
    aggregate_verdict: AggregateVerdict
    aggregate_blocker: AggregateBlocker
    execution_degraded: bool = False
    reason_code: ReasonCode | None = None
    wins: int = 0
    attempts_planned: int = 0
    attempts_run: int = 0
    derived_from_executed_quorum: bool = False
    quarantine_status: QuarantineStatus = QuarantineStatus.INACTIVE
    latest_aggregate_verdict: AggregateVerdict | None = None
    latest_aggregate_blocker: AggregateBlocker | None = None
    quarantine_reason: str | None = None
    quarantine_since: str | None = None
    waiver_ref: str | None = None
    schema_version: str = SCHEMA_VERSION

    def validate(self) -> None:
        parse_case_uid(self.case_uid)
        _require(
            isinstance(self.aggregate_verdict, AggregateVerdict),
            "aggregate_verdict must be AggregateVerdict",
        )
        _require(
            isinstance(self.aggregate_blocker, AggregateBlocker),
            "aggregate_blocker must be AggregateBlocker",
        )
        if self.aggregate_verdict in (AggregateVerdict.PASS, AggregateVerdict.FAIL):
            _require(
                self.aggregate_blocker is AggregateBlocker.NONE,
                "PASS/FAIL aggregates carry blocker NONE",
            )
            _require(
                self.derived_from_executed_quorum,
                "a PASS/FAIL aggregate requires an executed quorum; "
                "no code path may default an unexecuted case to PASS or FAIL",
            )
            _require(self.wins >= 1, "a PASS/FAIL aggregate requires executed wins")
            _require(
                self.attempts_run >= self.wins,
                "attempts_run must cover the winning attempts",
            )
        else:
            _require(
                self.aggregate_blocker is not AggregateBlocker.NONE,
                "an INCONCLUSIVE aggregate must carry a non-NONE blocker",
            )
        _non_negative_int(self.wins, "wins")
        _non_negative_int(self.attempts_planned, "attempts_planned")
        _non_negative_int(self.attempts_run, "attempts_run")
        _require(
            self.attempts_run <= self.attempts_planned,
            "attempts_run cannot exceed attempts_planned",
        )
        if self.reason_code is not None:
            _require(
                isinstance(self.reason_code, ReasonCode),
                "reason_code must be ReasonCode or None",
            )
        _require(
            isinstance(self.quarantine_status, QuarantineStatus),
            "quarantine_status must be QuarantineStatus",
        )
        if self.quarantine_status is QuarantineStatus.ACTIVE:
            _require(
                self.quarantine_reason is not None and self.quarantine_since is not None,
                "an ACTIVE quarantine must carry a dated reason",
            )
            _require(
                self.latest_aggregate_verdict is not None,
                "quarantine never erases latest_aggregate_verdict",
            )
        _require(
            self.schema_version == SCHEMA_VERSION,
            f"schema_version must be {SCHEMA_VERSION}",
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "case_uid": self.case_uid,
            "aggregate_verdict": self.aggregate_verdict.value,
            "aggregate_blocker": self.aggregate_blocker.value,
            "execution_degraded": self.execution_degraded,
            "reason_code": self.reason_code.value if self.reason_code else None,
            "wins": self.wins,
            "attempts_planned": self.attempts_planned,
            "attempts_run": self.attempts_run,
            "derived_from_executed_quorum": self.derived_from_executed_quorum,
            "quarantine_status": self.quarantine_status.value,
            "latest_aggregate_verdict": (
                self.latest_aggregate_verdict.value
                if self.latest_aggregate_verdict
                else None
            ),
            "latest_aggregate_blocker": (
                self.latest_aggregate_blocker.value
                if self.latest_aggregate_blocker
                else None
            ),
            "quarantine_reason": self.quarantine_reason,
            "quarantine_since": self.quarantine_since,
            "waiver_ref": self.waiver_ref,
            "schema_version": self.schema_version,
        }

    _KEYS = frozenset(
        {
            "case_uid",
            "aggregate_verdict",
            "aggregate_blocker",
            "execution_degraded",
            "reason_code",
            "wins",
            "attempts_planned",
            "attempts_run",
            "derived_from_executed_quorum",
            "quarantine_status",
            "latest_aggregate_verdict",
            "latest_aggregate_blocker",
            "quarantine_reason",
            "quarantine_since",
            "waiver_ref",
            "schema_version",
        }
    )

    @classmethod
    def from_dict(cls, payload: Mapping[str, Any]) -> "AggregateRecord":
        _check_keys(payload, cls._KEYS, "AggregateRecord")

        def _opt(parser, key):
            value = payload.get(key)
            return parser(value) if value is not None else None

        record = cls(
            case_uid=payload.get("case_uid", ""),
            aggregate_verdict=AggregateVerdict.parse(payload.get("aggregate_verdict")),
            aggregate_blocker=AggregateBlocker.parse(payload.get("aggregate_blocker")),
            execution_degraded=bool(payload.get("execution_degraded", False)),
            reason_code=_opt(ReasonCode.parse, "reason_code"),
            wins=payload.get("wins", 0),
            attempts_planned=payload.get("attempts_planned", 0),
            attempts_run=payload.get("attempts_run", 0),
            derived_from_executed_quorum=bool(
                payload.get("derived_from_executed_quorum", False)
            ),
            quarantine_status=QuarantineStatus.parse(
                payload.get("quarantine_status", QuarantineStatus.INACTIVE.value)
            ),
            latest_aggregate_verdict=_opt(
                AggregateVerdict.parse, "latest_aggregate_verdict"
            ),
            latest_aggregate_blocker=_opt(
                AggregateBlocker.parse, "latest_aggregate_blocker"
            ),
            quarantine_reason=payload.get("quarantine_reason"),
            quarantine_since=payload.get("quarantine_since"),
            waiver_ref=payload.get("waiver_ref"),
            schema_version=payload.get("schema_version", SCHEMA_VERSION),
        )
        record.validate()
        return record


def default_unselected_aggregate(case_uid: str) -> AggregateRecord:
    """The DEFAULT aggregate of every authored case outside a run's selection."""
    record = AggregateRecord(
        case_uid=case_uid,
        aggregate_verdict=AggregateVerdict.INCONCLUSIVE,
        aggregate_blocker=AggregateBlocker.NOT_SELECTED,
        reason_code=ReasonCode.NOT_SELECTED,
    )
    record.validate()
    return record


@dataclass(frozen=True, slots=True)
class CaseManifestRecord:
    """Control-plane case manifest entry (design §5b; surface A, never agent-visible)."""

    case_uid: str
    case_id: str
    owner: str
    eval_file_kind: EvalFileKind
    case_type: CaseType
    prompt_sha256: str
    target: TypedTarget
    risk_class: RiskClass
    risk_class_ratified: bool
    claim_scope: ClaimScope
    workspace_role: WorkspaceRole
    materialization_profile_id: MaterializationProfile
    activation_mode_expected: InvocationMode
    workspace_fixture_id: str = "empty-consumer"
    fixture_version: str = "1"
    required_files: tuple[str, ...] = ()
    required_language_runtime: tuple[str, ...] = ()
    required_framework: tuple[str, ...] = ()
    required_commands: tuple[str, ...] = ()
    required_services: tuple[str, ...] = ()
    required_database: tuple[str, ...] = ()
    required_network_posture: str = "none"
    required_credentials_class: str = "none"
    required_tool_permissions: tuple[str, ...] = ()
    setup_provenance: str | None = None
    setup_hash: str | None = None
    assertions: tuple[AssertionRecord, ...] = ()
    should_not_trigger: tuple[str, ...] = ()
    overlaps_with: tuple[str, ...] = ()
    manual_only_target: bool = False
    explicit_invocation_authorized: bool = False
    schema_version: str = SCHEMA_VERSION

    def validate(self) -> None:
        parse_case_uid(self.case_uid)
        _require(bool(self.case_id), "case_id required")
        _require(bool(self.owner), "owner required")
        _require(isinstance(self.eval_file_kind, EvalFileKind), "eval_file_kind enum")
        _require(isinstance(self.case_type, CaseType), "case_type enum")
        _require(
            isinstance(self.prompt_sha256, str) and len(self.prompt_sha256) == 64,
            "prompt_sha256 must be 64 hex chars",
        )
        self.target.validate()
        _require(isinstance(self.risk_class, RiskClass), "risk_class enum")
        _require(
            self.risk_class_ratified is False,
            "WP-2B-1 risk classes are PROPOSED / NOT OWNER-RATIFIED; "
            "ratification is OD-3 owner work",
        )
        _require(isinstance(self.claim_scope, ClaimScope), "claim_scope enum")
        _require(isinstance(self.workspace_role, WorkspaceRole), "workspace_role enum")
        _require(
            isinstance(self.materialization_profile_id, MaterializationProfile),
            "materialization_profile_id enum",
        )
        _require(
            isinstance(self.activation_mode_expected, InvocationMode),
            "activation_mode_expected enum",
        )
        _require(
            self.required_network_posture in ("none", "loopback-fixture-only"),
            f"required_network_posture invalid: {self.required_network_posture!r} "
            "(open egress is never permitted)",
        )
        _require(
            self.required_credentials_class in ("none", "synthetic-test-only"),
            f"required_credentials_class invalid: {self.required_credentials_class!r} "
            "(production credentials are never permitted)",
        )
        if self.claim_scope is ClaimScope.PARTIAL_INSTALL:
            _require(
                self.materialization_profile_id
                is MaterializationProfile.CONSUMER_PARTIAL_INSTALL,
                "partial_install claims require the consumer_partial_install profile",
            )
        if (
            self.materialization_profile_id
            is MaterializationProfile.CONSUMER_PARTIAL_INSTALL
        ):
            _require(
                self.claim_scope is ClaimScope.PARTIAL_INSTALL,
                "the consumer_partial_install profile requires claim_scope "
                "partial_install",
            )
        for assertion in self.assertions:
            assertion.validate()
        _require(
            self.schema_version == SCHEMA_VERSION,
            f"schema_version must be {SCHEMA_VERSION}",
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "case_uid": self.case_uid,
            "case_id": self.case_id,
            "owner": self.owner,
            "eval_file_kind": self.eval_file_kind.value,
            "case_type": self.case_type.value,
            "prompt_sha256": self.prompt_sha256,
            "target": self.target.to_dict(),
            "risk_class": self.risk_class.value,
            "risk_class_ratified": self.risk_class_ratified,
            "claim_scope": self.claim_scope.value,
            "workspace_role": self.workspace_role.value,
            "materialization_profile_id": self.materialization_profile_id.value,
            "activation_mode_expected": self.activation_mode_expected.value,
            "workspace_fixture_id": self.workspace_fixture_id,
            "fixture_version": self.fixture_version,
            "required_files": list(self.required_files),
            "required_language_runtime": list(self.required_language_runtime),
            "required_framework": list(self.required_framework),
            "required_commands": list(self.required_commands),
            "required_services": list(self.required_services),
            "required_database": list(self.required_database),
            "required_network_posture": self.required_network_posture,
            "required_credentials_class": self.required_credentials_class,
            "required_tool_permissions": list(self.required_tool_permissions),
            "setup_provenance": self.setup_provenance,
            "setup_hash": self.setup_hash,
            "assertions": [a.to_dict() for a in self.assertions],
            "should_not_trigger": list(self.should_not_trigger),
            "overlaps_with": list(self.overlaps_with),
            "manual_only_target": self.manual_only_target,
            "explicit_invocation_authorized": self.explicit_invocation_authorized,
            "schema_version": self.schema_version,
        }

    _KEYS = frozenset(
        {
            "case_uid",
            "case_id",
            "owner",
            "eval_file_kind",
            "case_type",
            "prompt_sha256",
            "target",
            "risk_class",
            "risk_class_ratified",
            "claim_scope",
            "workspace_role",
            "materialization_profile_id",
            "activation_mode_expected",
            "workspace_fixture_id",
            "fixture_version",
            "required_files",
            "required_language_runtime",
            "required_framework",
            "required_commands",
            "required_services",
            "required_database",
            "required_network_posture",
            "required_credentials_class",
            "required_tool_permissions",
            "setup_provenance",
            "setup_hash",
            "assertions",
            "should_not_trigger",
            "overlaps_with",
            "manual_only_target",
            "explicit_invocation_authorized",
            "schema_version",
        }
    )

    @classmethod
    def from_dict(cls, payload: Mapping[str, Any]) -> "CaseManifestRecord":
        _check_keys(payload, cls._KEYS, "CaseManifestRecord")
        record = cls(
            case_uid=payload.get("case_uid", ""),
            case_id=payload.get("case_id", ""),
            owner=payload.get("owner", ""),
            eval_file_kind=EvalFileKind.parse(payload.get("eval_file_kind")),
            case_type=CaseType.parse(payload.get("case_type")),
            prompt_sha256=payload.get("prompt_sha256", ""),
            target=TypedTarget.from_dict(payload.get("target", {})),
            risk_class=RiskClass.parse(payload.get("risk_class")),
            risk_class_ratified=bool(payload.get("risk_class_ratified", False)),
            claim_scope=ClaimScope.parse(payload.get("claim_scope")),
            workspace_role=WorkspaceRole.parse(payload.get("workspace_role")),
            materialization_profile_id=MaterializationProfile.parse(
                payload.get("materialization_profile_id")
            ),
            activation_mode_expected=InvocationMode.parse(
                payload.get("activation_mode_expected")
            ),
            workspace_fixture_id=payload.get("workspace_fixture_id", "empty-consumer"),
            fixture_version=payload.get("fixture_version", "1"),
            required_files=_str_tuple(payload.get("required_files", ()), "required_files"),
            required_language_runtime=_str_tuple(
                payload.get("required_language_runtime", ()), "required_language_runtime"
            ),
            required_framework=_str_tuple(
                payload.get("required_framework", ()), "required_framework"
            ),
            required_commands=_str_tuple(
                payload.get("required_commands", ()), "required_commands"
            ),
            required_services=_str_tuple(
                payload.get("required_services", ()), "required_services"
            ),
            required_database=_str_tuple(
                payload.get("required_database", ()), "required_database"
            ),
            required_network_posture=payload.get("required_network_posture", "none"),
            required_credentials_class=payload.get(
                "required_credentials_class", "none"
            ),
            required_tool_permissions=_str_tuple(
                payload.get("required_tool_permissions", ()), "required_tool_permissions"
            ),
            setup_provenance=payload.get("setup_provenance"),
            setup_hash=payload.get("setup_hash"),
            assertions=tuple(
                AssertionRecord.from_dict(a) for a in payload.get("assertions", ())
            ),
            should_not_trigger=_str_tuple(
                payload.get("should_not_trigger", ()), "should_not_trigger"
            ),
            overlaps_with=_str_tuple(payload.get("overlaps_with", ()), "overlaps_with"),
            manual_only_target=bool(payload.get("manual_only_target", False)),
            explicit_invocation_authorized=bool(
                payload.get("explicit_invocation_authorized", False)
            ),
            schema_version=payload.get("schema_version", SCHEMA_VERSION),
        )
        record.validate()
        return record


#: The exact coverage-metric field names required in every report (Phase 19).
COVERAGE_METRIC_FIELDS = (
    "authored_units_total",
    "selected_units_total",
    "preflight_accounted_total",
    "runnable_units_total",
    "attempted_units_total",
    "completed_units_total",
    "authored_coverage",
    "selected_coverage",
    "runnable_coverage",
    "execution_coverage",
    "assertion_accounting_coverage",
    "assertions_actually_graded_coverage",
    "critical_case_coverage",
    "unrun_totals_by_reason",
    "excluded_totals_by_reason",
)


def _ratio(numerator: int, denominator: int) -> float:
    if denominator <= 0:
        return 0.0
    return round(numerator / denominator, 6)


@dataclass(frozen=True, slots=True)
class CoverageMetrics:
    """Honest run coverage accounting (design §13; prompt Phase 19)."""

    authored_units_total: int
    selected_units_total: int
    preflight_accounted_total: int
    runnable_units_total: int
    attempted_units_total: int
    completed_units_total: int
    assertions_selected_total: int
    assertions_accounted_total: int
    assertions_actually_graded_total: int
    critical_runnable_total: int = 0
    critical_executed_total: int = 0
    unrun_totals_by_reason: Mapping[str, int] = field(default_factory=dict)
    excluded_totals_by_reason: Mapping[str, int] = field(default_factory=dict)
    schema_version: str = SCHEMA_VERSION

    def validate(self) -> None:
        for name in (
            "authored_units_total",
            "selected_units_total",
            "preflight_accounted_total",
            "runnable_units_total",
            "attempted_units_total",
            "completed_units_total",
            "assertions_selected_total",
            "assertions_accounted_total",
            "assertions_actually_graded_total",
            "critical_runnable_total",
            "critical_executed_total",
        ):
            _non_negative_int(getattr(self, name), f"CoverageMetrics.{name}")
        _require(
            self.selected_units_total <= self.authored_units_total,
            "selected cannot exceed authored",
        )
        _require(
            self.preflight_accounted_total <= self.selected_units_total,
            "preflight-accounted cannot exceed selected",
        )
        _require(
            self.runnable_units_total <= self.preflight_accounted_total,
            "runnable cannot exceed preflight-accounted",
        )
        _require(
            self.attempted_units_total <= self.runnable_units_total,
            "attempted cannot exceed runnable",
        )
        _require(
            self.completed_units_total <= self.attempted_units_total,
            "completed cannot exceed attempted",
        )
        _require(
            self.assertions_accounted_total <= self.assertions_selected_total,
            "accounted assertions cannot exceed selected assertions",
        )
        _require(
            self.assertions_actually_graded_total <= self.assertions_accounted_total,
            "graded assertions cannot exceed accounted assertions "
            "(accounting is not grading)",
        )
        _require(
            self.critical_executed_total <= self.critical_runnable_total,
            "executed critical cannot exceed runnable critical",
        )
        for name, bucket in (
            ("unrun_totals_by_reason", self.unrun_totals_by_reason),
            ("excluded_totals_by_reason", self.excluded_totals_by_reason),
        ):
            _require(isinstance(bucket, Mapping), f"{name} must be a mapping")
            for key, value in bucket.items():
                _require(isinstance(key, str), f"{name} keys must be strings")
                if name == "unrun_totals_by_reason":
                    ReasonCode.parse(key)  # unrun buckets key by versioned reason code
                _non_negative_int(value, f"{name}[{key}]")

    def to_dict(self) -> dict[str, Any]:
        return {
            "authored_units_total": self.authored_units_total,
            "selected_units_total": self.selected_units_total,
            "preflight_accounted_total": self.preflight_accounted_total,
            "runnable_units_total": self.runnable_units_total,
            "attempted_units_total": self.attempted_units_total,
            "completed_units_total": self.completed_units_total,
            "authored_coverage": _ratio(
                self.attempted_units_total, self.authored_units_total
            ),
            "selected_coverage": _ratio(
                self.selected_units_total, self.authored_units_total
            ),
            "runnable_coverage": _ratio(
                self.runnable_units_total, self.selected_units_total
            ),
            "execution_coverage": _ratio(
                self.attempted_units_total, self.runnable_units_total
            ),
            "assertion_accounting_coverage": _ratio(
                self.assertions_accounted_total, self.assertions_selected_total
            ),
            "assertions_actually_graded_coverage": _ratio(
                self.assertions_actually_graded_total, self.assertions_selected_total
            ),
            "critical_case_coverage": _ratio(
                self.critical_executed_total, self.critical_runnable_total
            ),
            "unrun_totals_by_reason": dict(self.unrun_totals_by_reason),
            "excluded_totals_by_reason": dict(self.excluded_totals_by_reason),
            "schema_version": self.schema_version,
        }
