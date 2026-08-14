"""Typed deterministic grader results (WP-2B-2; prompt section 10.H).

A ``GraderResult`` is the only shape a deterministic grader may emit:

- versioned (``GRADING_SCHEMA_VERSION``), with grader identity/version;
- control/assertion identifier and case/suite identity;
- a CLOSED result state (PASS / FAIL / ERROR) — never a silent default;
- a CLOSED grading reason-code set (FAIL and ERROR always carry one);
- evidence pointers and validated input hashes;
- deterministic reproduction data;
- an output hash computed over the record WITHOUT the hash itself
  (no self-referential hash; tampering is caught on parse);
- no private chain-of-thought and no free-form reasoning field.

Unknown enum or field values fail closed (``SchemaValidationError``).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from types import MappingProxyType
from typing import Any, Mapping

from .. import GRADING_SCHEMA_VERSION, GRADING_STACK_VERSION
from ..canonical import sha256_of_obj
from ..enums import StrictEnum
from ..errors import SchemaValidationError
from ..identity import parse_case_uid

GRADER_VERSION = GRADING_STACK_VERSION

_HEX = set("0123456789abcdef")

#: Valid Scenario A control identifiers (A-Q).
CONTROL_ID_PREFIX = "SCENARIO_A_CONTROL_"
CONTROL_LETTERS = "ABCDEFGHIJKLMNOPQ"
VALID_CONTROL_IDS = frozenset(f"{CONTROL_ID_PREFIX}{c}" for c in CONTROL_LETTERS)


class GraderResultState(StrictEnum):
    """Closed deterministic result states. There is no silent pass."""

    PASS = "PASS"
    FAIL = "FAIL"
    ERROR = "ERROR"


class GradingReasonCode(StrictEnum):
    """Closed, versioned grading reason codes.

    Names shared with the WP-2B-1 ``ReasonCode`` vocabulary keep identical
    values (prompt section 13: reuse where applicable); the remainder are
    grading-specific deterministic codes.
    """

    # Reused WP-2B-1 vocabulary (values must match enums.ReasonCode).
    AMBIGUOUS_ACTIVATION = "AMBIGUOUS_ACTIVATION"
    EVIDENCE_INTEGRITY_FAILURE = "EVIDENCE_INTEGRITY_FAILURE"
    UNJUDGEABLE_ASSERTION = "UNJUDGEABLE_ASSERTION"
    INCOMPATIBLE_INVOCATION_MODE = "INCOMPATIBLE_INVOCATION_MODE"
    # State and transition grading (10.A).
    INVALID_PRIOR_STATE = "INVALID_PRIOR_STATE"
    INVALID_TURN_CLASS = "INVALID_TURN_CLASS"
    UNKNOWN_ANSWER_ID = "UNKNOWN_ANSWER_ID"
    PROHIBITED_TRANSITION = "PROHIBITED_TRANSITION"
    REPEATED_LOOP = "REPEATED_LOOP"
    COMPLETION_VIOLATION = "COMPLETION_VIOLATION"
    FORBIDDEN_SNAPSHOT = "FORBIDDEN_SNAPSHOT"
    ORDERING_GATE_VIOLATION = "ORDERING_GATE_VIOLATION"
    # Authorization and approval boundaries (10.B).
    APPROVAL_MISSING = "APPROVAL_MISSING"
    APPROVAL_AMBIGUOUS = "APPROVAL_AMBIGUOUS"
    APPROVAL_IDENTITY_MISSING = "APPROVAL_IDENTITY_MISSING"
    ACTION_BEFORE_APPROVAL = "ACTION_BEFORE_APPROVAL"
    RECORDING_BOUNDARY_VIOLATION = "RECORDING_BOUNDARY_VIOLATION"
    SILENT_STAGE_ADVANCE = "SILENT_STAGE_ADVANCE"
    # Prohibited action / mutation checks (10.C).
    NETWORK_EGRESS_OBSERVED = "NETWORK_EGRESS_OBSERVED"
    PACKAGE_INSTALL_OBSERVED = "PACKAGE_INSTALL_OBSERVED"
    GIT_MUTATION_OBSERVED = "GIT_MUTATION_OBSERVED"
    DEPLOY_OBSERVED = "DEPLOY_OBSERVED"
    MIGRATION_OBSERVED = "MIGRATION_OBSERVED"
    UNAPPROVED_FILE_MUTATION = "UNAPPROVED_FILE_MUTATION"
    OUT_OF_SCOPE_ACTION = "OUT_OF_SCOPE_ACTION"
    # Append-only and recording checks (10.D).
    APPEND_ONLY_VIOLATION = "APPEND_ONLY_VIOLATION"
    PLACEHOLDER_REMOVED = "PLACEHOLDER_REMOVED"
    EXPECTED_RECORD_MISSING = "EXPECTED_RECORD_MISSING"
    # Preview-versus-created hashing (10.E).
    PREVIEW_MISMATCH = "PREVIEW_MISMATCH"
    # Typed target and invocation mode (10.F).
    TARGET_KIND_MISMATCH = "TARGET_KIND_MISMATCH"
    TARGET_NAME_MISMATCH = "TARGET_NAME_MISMATCH"
    INVOCATION_MODE_MISMATCH = "INVOCATION_MODE_MISMATCH"
    # Workspace-role / stage recognition (controls A-B deterministic halves).
    WORKSPACE_ROLE_MISMATCH = "WORKSPACE_ROLE_MISMATCH"
    STAGE_ZERO_VIOLATION = "STAGE_ZERO_VIOLATION"
    # Questionnaire-dump deterministic screen (control H deterministic half).
    QUESTIONNAIRE_DUMP_DETECTED = "QUESTIONNAIRE_DUMP_DETECTED"
    # Runner-provided capture controls (P-Q).
    EVIDENCE_CAPTURE_MISSING = "EVIDENCE_CAPTURE_MISSING"
    METADATA_CAPTURE_MISSING = "METADATA_CAPTURE_MISSING"
    # Evidence-shape failures (any grader).
    EVIDENCE_MALFORMED = "EVIDENCE_MALFORMED"
    # Non-verdict routing for semantic components (never a PASS).
    SEMANTIC_REQUIRED = "SEMANTIC_REQUIRED"


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise SchemaValidationError(message)


def _require_sha256(value: Any, where: str) -> str:
    _require(
        isinstance(value, str) and len(value) == 64 and set(value) <= _HEX,
        f"{where} must be a 64-char lowercase hex SHA-256, got {value!r}",
    )
    return value


def _deep_freeze(obj: Any) -> Any:
    if isinstance(obj, Mapping):
        return MappingProxyType({str(k): _deep_freeze(v) for k, v in obj.items()})
    if isinstance(obj, (list, tuple)):
        return tuple(_deep_freeze(v) for v in obj)
    return obj


def _to_plain(obj: Any) -> Any:
    if isinstance(obj, Mapping):
        return {k: _to_plain(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [_to_plain(v) for v in obj]
    return obj


@dataclass(frozen=True, slots=True)
class GraderResult:
    """Immutable deterministic grading result (see module docstring)."""

    grader_id: str
    control_id: str
    case_uid: str
    result_state: GraderResultState
    evidence_pointers: tuple[str, ...]
    input_sha256s: Mapping[str, str]
    reproduction: Mapping[str, Any]
    output_sha256: str
    assertion_uid: str | None = None
    reason_code: GradingReasonCode | None = None
    grader_version: str = GRADER_VERSION
    schema_version: str = GRADING_SCHEMA_VERSION

    def __post_init__(self) -> None:
        object.__setattr__(self, "input_sha256s", _deep_freeze(self.input_sha256s))
        object.__setattr__(self, "reproduction", _deep_freeze(self.reproduction))
        object.__setattr__(
            self, "evidence_pointers", tuple(self.evidence_pointers)
        )

    # ---------------------------------------------------------------- content
    def _content_dict(self) -> dict[str, Any]:
        """The hashed content: everything EXCEPT output_sha256."""
        return {
            "grader_id": self.grader_id,
            "grader_version": self.grader_version,
            "control_id": self.control_id,
            "case_uid": self.case_uid,
            "assertion_uid": self.assertion_uid,
            "result_state": self.result_state.value,
            "reason_code": self.reason_code.value if self.reason_code else None,
            "evidence_pointers": list(self.evidence_pointers),
            "input_sha256s": _to_plain(self.input_sha256s),
            "reproduction": _to_plain(self.reproduction),
            "schema_version": self.schema_version,
        }

    def validate(self) -> None:
        _require(
            isinstance(self.grader_id, str) and bool(self.grader_id),
            "grader_id must be a non-empty string",
        )
        _require(
            isinstance(self.grader_version, str) and bool(self.grader_version),
            "grader_version must be a non-empty string",
        )
        _require(
            self.control_id in VALID_CONTROL_IDS,
            f"control_id must be one of the Scenario A controls A-Q, got "
            f"{self.control_id!r}",
        )
        parse_case_uid(self.case_uid)
        if self.assertion_uid is not None:
            _require(
                isinstance(self.assertion_uid, str)
                and self.assertion_uid.count("::") >= 5
                and self.assertion_uid.startswith(self.case_uid + "::"),
                "assertion_uid must be scoped to THIS record's case_uid",
            )
        _require(
            isinstance(self.result_state, GraderResultState),
            "result_state must be GraderResultState",
        )
        if self.reason_code is not None:
            _require(
                isinstance(self.reason_code, GradingReasonCode),
                "reason_code must be GradingReasonCode or None",
            )
        if self.result_state is GraderResultState.PASS:
            _require(
                self.reason_code is None,
                "a PASS result must not carry a failure/error reason code",
            )
        else:
            _require(
                self.reason_code is not None,
                f"a {self.result_state.value} result must carry a reason code",
            )
        _require(
            isinstance(self.evidence_pointers, tuple) and len(self.evidence_pointers) > 0,
            "evidence_pointers must be a non-empty tuple",
        )
        for pointer in self.evidence_pointers:
            _require(
                isinstance(pointer, str) and bool(pointer),
                "every evidence pointer must be a non-empty string",
            )
        _require(
            isinstance(self.input_sha256s, Mapping) and len(self.input_sha256s) > 0,
            "input_sha256s must be a non-empty mapping",
        )
        for key, value in self.input_sha256s.items():
            _require(isinstance(key, str) and bool(key), "input hash keys must be strings")
            _require_sha256(value, f"input_sha256s[{key}]")
        _require(
            isinstance(self.reproduction, Mapping),
            "reproduction must be a mapping of deterministic repro data",
        )
        _require(
            self.schema_version == GRADING_SCHEMA_VERSION,
            f"schema_version must be {GRADING_SCHEMA_VERSION}",
        )
        expected = sha256_of_obj(self._content_dict())
        _require(
            self.output_sha256 == expected,
            "output_sha256 does not match the record content "
            "(tampered or mis-built result)",
        )

    def to_dict(self) -> dict[str, Any]:
        payload = self._content_dict()
        payload["output_sha256"] = self.output_sha256
        return payload

    _KEYS = frozenset(
        {
            "grader_id",
            "grader_version",
            "control_id",
            "case_uid",
            "assertion_uid",
            "result_state",
            "reason_code",
            "evidence_pointers",
            "input_sha256s",
            "reproduction",
            "schema_version",
            "output_sha256",
        }
    )

    @classmethod
    def from_dict(cls, payload: Mapping[str, Any]) -> "GraderResult":
        unknown = set(payload) - cls._KEYS
        _require(not unknown, f"GraderResult: unknown keys {sorted(unknown)}")
        reason = payload.get("reason_code")
        result = cls(
            grader_id=payload.get("grader_id", ""),
            grader_version=payload.get("grader_version", ""),
            control_id=payload.get("control_id", ""),
            case_uid=payload.get("case_uid", ""),
            assertion_uid=payload.get("assertion_uid"),
            result_state=GraderResultState.parse(payload.get("result_state")),
            reason_code=(
                GradingReasonCode.parse(reason) if reason is not None else None
            ),
            evidence_pointers=tuple(payload.get("evidence_pointers", ())),
            input_sha256s=dict(payload.get("input_sha256s", {})),
            reproduction=dict(payload.get("reproduction", {})),
            schema_version=payload.get("schema_version", ""),
            output_sha256=payload.get("output_sha256", ""),
        )
        result.validate()
        return result


def make_grader_result(
    grader_id: str,
    control_id: str,
    case_uid: str,
    result_state: GraderResultState,
    evidence_pointers: tuple[str, ...],
    input_sha256s: Mapping[str, str],
    reproduction: Mapping[str, Any],
    assertion_uid: str | None = None,
    reason_code: GradingReasonCode | None = None,
) -> GraderResult:
    """Build, hash-bind, and validate a deterministic grader result."""
    provisional = GraderResult(
        grader_id=grader_id,
        control_id=control_id,
        case_uid=case_uid,
        assertion_uid=assertion_uid,
        result_state=result_state,
        reason_code=reason_code,
        evidence_pointers=tuple(evidence_pointers),
        input_sha256s=dict(input_sha256s),
        reproduction=dict(reproduction),
        output_sha256="0" * 64,
    )
    bound = GraderResult(
        grader_id=provisional.grader_id,
        grader_version=provisional.grader_version,
        control_id=provisional.control_id,
        case_uid=provisional.case_uid,
        assertion_uid=provisional.assertion_uid,
        result_state=provisional.result_state,
        reason_code=provisional.reason_code,
        evidence_pointers=provisional.evidence_pointers,
        input_sha256s=dict(provisional.input_sha256s),
        reproduction=dict(_to_plain(provisional.reproduction)),
        schema_version=provisional.schema_version,
        output_sha256=sha256_of_obj(provisional._content_dict()),
    )
    bound.validate()
    return bound
