"""Schema-validated structured judge verdict + fail-closed parsing
(WP-2B-2; prompt 11.D).

The verdict schema carries NO confidence field (the parent design's §8
verdict shape authorizes none), NO chain-of-thought, and no free-form field
capable of smuggling unbounded private reasoning (the only bounded span is
``offending_span``, hard-capped). Malformed, refused, timed-out,
transport-failed, schema-invalid, mismatched, or contradictory output is
JUDGE_ERROR — never PASS or FAIL."""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from typing import Any, Mapping, Sequence

from .. import GRADING_SCHEMA_VERSION
from ..canonical import canonical_bytes
from ..enums import AttemptState, StrictEnum
from ..errors import RunnerError, SchemaValidationError
from ..graders.records import VALID_CONTROL_IDS
from .interface import JudgeClient, JudgeRequest, JudgeResponse, TransportOutcome

OFFENDING_SPAN_MAX_CHARS = 500

#: verdict_id is an identifier, never a free-form channel: bounded length,
#: identifier charset only (no unbounded field can smuggle reasoning).
VERDICT_ID_PATTERN = re.compile(r"^[A-Za-z0-9._:-]{1,128}$")

_HEX = set("0123456789abcdef")


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise SchemaValidationError(message)


class JudgeVerdictState(StrictEnum):
    PASS = "PASS"
    FAIL = "FAIL"
    ABSTAIN = "ABSTAIN"


class FailureMode(StrictEnum):
    """Closed coherent-topic failure modes (design §8 rubric)."""

    QUESTIONNAIRE_DUMP = "QUESTIONNAIRE_DUMP"
    MULTIPLE_UNRELATED_TOPICS = "MULTIPLE_UNRELATED_TOPICS"
    ANY_ORDER_INSTRUCTION = "ANY_ORDER_INSTRUCTION"
    BUNDLED_INDEPENDENT_DECISIONS = "BUNDLED_INDEPENDENT_DECISIONS"
    OTHER_RUBRIC_VIOLATION = "OTHER_RUBRIC_VIOLATION"


class JudgeVerdictReason(StrictEnum):
    MEETS_RUBRIC = "MEETS_RUBRIC"
    VIOLATES_RUBRIC = "VIOLATES_RUBRIC"
    INSUFFICIENT_EVIDENCE = "INSUFFICIENT_EVIDENCE"


@dataclass(frozen=True, slots=True)
class StructuredVerdict:
    verdict_id: str
    request_id: str
    control_id: str
    verdict: JudgeVerdictState
    reason_code: JudgeVerdictReason
    evidence_refs: tuple[str, ...]
    rubric_id: str
    rubric_version: str
    rubric_sha256: str
    judge_id: str
    judge_version: str
    input_manifest_sha256: str
    failure_mode: FailureMode | None = None
    offending_span: str | None = None
    schema_version: str = GRADING_SCHEMA_VERSION

    def validate(self) -> None:
        for name in (
            "verdict_id",
            "request_id",
            "rubric_id",
            "rubric_version",
            "judge_id",
            "judge_version",
        ):
            value = getattr(self, name)
            _require(
                isinstance(value, str) and bool(value), f"{name} must be non-empty"
            )
        _require(
            self.control_id in VALID_CONTROL_IDS,
            f"control_id must be a Scenario A control A-Q, got "
            f"{self.control_id!r}",
        )
        _require(
            VERDICT_ID_PATTERN.fullmatch(self.verdict_id) is not None,
            "verdict_id must be a bounded identifier "
            "(1-128 chars of [A-Za-z0-9._:-]); it is never a free-form field",
        )
        for name in ("rubric_sha256", "input_manifest_sha256"):
            value = getattr(self, name)
            _require(
                isinstance(value, str) and len(value) == 64 and set(value) <= _HEX,
                f"{name} must be a 64-hex SHA-256",
            )
        _require(
            isinstance(self.verdict, JudgeVerdictState),
            "verdict must be JudgeVerdictState",
        )
        _require(
            isinstance(self.reason_code, JudgeVerdictReason),
            "reason_code must be JudgeVerdictReason",
        )
        _require(
            isinstance(self.evidence_refs, tuple)
            and all(isinstance(ref, str) and ref for ref in self.evidence_refs),
            "evidence_refs must be a tuple of non-empty strings",
        )
        if self.verdict is JudgeVerdictState.PASS:
            _require(self.failure_mode is None, "PASS carries no failure_mode")
            _require(self.offending_span is None, "PASS carries no offending_span")
            _require(
                self.reason_code is JudgeVerdictReason.MEETS_RUBRIC,
                "PASS requires reason MEETS_RUBRIC",
            )
            _require(bool(self.evidence_refs), "PASS requires evidence refs")
        elif self.verdict is JudgeVerdictState.FAIL:
            _require(
                isinstance(self.failure_mode, FailureMode),
                "FAIL requires an explicit failure_mode",
            )
            _require(
                self.reason_code is JudgeVerdictReason.VIOLATES_RUBRIC,
                "FAIL requires reason VIOLATES_RUBRIC",
            )
            _require(bool(self.evidence_refs), "FAIL requires evidence refs")
        else:  # ABSTAIN
            _require(self.failure_mode is None, "ABSTAIN carries no failure_mode")
            _require(self.offending_span is None, "ABSTAIN carries no offending_span")
            _require(
                self.reason_code is JudgeVerdictReason.INSUFFICIENT_EVIDENCE,
                "ABSTAIN requires reason INSUFFICIENT_EVIDENCE",
            )
        if self.offending_span is not None:
            _require(
                isinstance(self.offending_span, str)
                and len(self.offending_span) <= OFFENDING_SPAN_MAX_CHARS,
                f"offending_span is bounded to {OFFENDING_SPAN_MAX_CHARS} chars "
                "(no unbounded free-form field)",
            )
        _require(
            self.schema_version == GRADING_SCHEMA_VERSION,
            f"schema_version must be {GRADING_SCHEMA_VERSION}",
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "verdict_id": self.verdict_id,
            "request_id": self.request_id,
            "control_id": self.control_id,
            "verdict": self.verdict.value,
            "failure_mode": self.failure_mode.value if self.failure_mode else None,
            "offending_span": self.offending_span,
            "reason_code": self.reason_code.value,
            "evidence_refs": list(self.evidence_refs),
            "rubric_id": self.rubric_id,
            "rubric_version": self.rubric_version,
            "rubric_sha256": self.rubric_sha256,
            "judge_id": self.judge_id,
            "judge_version": self.judge_version,
            "input_manifest_sha256": self.input_manifest_sha256,
            "schema_version": self.schema_version,
        }

    _KEYS = frozenset(
        {
            "verdict_id",
            "request_id",
            "control_id",
            "verdict",
            "failure_mode",
            "offending_span",
            "reason_code",
            "evidence_refs",
            "rubric_id",
            "rubric_version",
            "rubric_sha256",
            "judge_id",
            "judge_version",
            "input_manifest_sha256",
            "schema_version",
        }
    )

    @classmethod
    def from_dict(cls, payload: Mapping[str, Any]) -> "StructuredVerdict":
        unknown = set(payload) - cls._KEYS
        _require(not unknown, f"StructuredVerdict: unknown keys {sorted(unknown)}")
        missing = cls._KEYS - set(payload)
        _require(not missing, f"StructuredVerdict: missing keys {sorted(missing)}")
        _require(
            isinstance(payload.get("evidence_refs"), list),
            "evidence_refs must be a JSON list, never a string",
        )
        failure_mode = payload.get("failure_mode")
        verdict = cls(
            verdict_id=payload.get("verdict_id", ""),
            request_id=payload.get("request_id", ""),
            control_id=payload.get("control_id", ""),
            verdict=JudgeVerdictState.parse(payload.get("verdict")),
            failure_mode=(
                FailureMode.parse(failure_mode) if failure_mode is not None else None
            ),
            offending_span=payload.get("offending_span"),
            reason_code=JudgeVerdictReason.parse(payload.get("reason_code")),
            evidence_refs=tuple(payload.get("evidence_refs", ())),
            rubric_id=payload.get("rubric_id", ""),
            rubric_version=payload.get("rubric_version", ""),
            rubric_sha256=payload.get("rubric_sha256", ""),
            judge_id=payload.get("judge_id", ""),
            judge_version=payload.get("judge_version", ""),
            input_manifest_sha256=payload.get("input_manifest_sha256", ""),
            schema_version=payload.get("schema_version", ""),
        )
        verdict.validate()
        return verdict


@dataclass(frozen=True, slots=True)
class JudgeOutcome:
    """The fail-closed result of interpreting one judge response."""

    is_verdict: bool
    verdict: StructuredVerdict | None
    judge_error_kind: str | None

    def to_attempt_state(self) -> AttemptState:
        """A failed judgment is JUDGE_ERROR; it is NEVER PASS or FAIL."""
        if not self.is_verdict:
            return AttemptState.JUDGE_ERROR
        assert self.verdict is not None
        if self.verdict.verdict is JudgeVerdictState.PASS:
            return AttemptState.PASS
        if self.verdict.verdict is JudgeVerdictState.FAIL:
            return AttemptState.FAIL
        return AttemptState.JUDGE_ERROR  # ABSTAIN: counted with abstentions


_TRANSPORT_ERROR_KINDS = {
    TransportOutcome.TIMEOUT: "TIMEOUT",
    TransportOutcome.TRANSPORT_ERROR: "TRANSPORT_ERROR",
    TransportOutcome.REFUSED: "REFUSED",
    TransportOutcome.MALFORMED_OUTPUT: "MALFORMED_OUTPUT",
}


def _error(kind: str) -> JudgeOutcome:
    return JudgeOutcome(is_verdict=False, verdict=None, judge_error_kind=kind)


def parse_judge_output(
    response: JudgeResponse,
    request: JudgeRequest,
    envelope: Mapping[str, Any],
) -> JudgeOutcome:
    """Interpret a (mock) judge response, failing closed to JUDGE_ERROR.

    The request must bind EXACTLY the supplied envelope (hash-to-hash), and
    the verdict's evidence references are checked against the envelope's
    ACTUAL untrusted-data keys — never a caller-supplied key list."""
    from .envelope import validate_request_envelope_binding

    response.validate()
    request.validate()
    try:
        validate_request_envelope_binding(request, envelope)
    except RunnerError:
        return _error("BINDING_MISMATCH")
    envelope_data_keys: Sequence[str] = tuple(envelope["untrusted_data"])
    if response.transport_outcome is not TransportOutcome.OK:
        return _error(_TRANSPORT_ERROR_KINDS[response.transport_outcome])
    if response.request_id != request.request_id:
        return _error("REQUEST_MISMATCH")
    if not response.raw_output:
        return _error("MALFORMED_JSON")
    try:
        payload = json.loads(response.raw_output)
    except ValueError:
        return _error("MALFORMED_JSON")
    if not isinstance(payload, Mapping):
        return _error("MALFORMED_JSON")
    try:
        verdict = StructuredVerdict.from_dict(payload)
    except SchemaValidationError:
        return _error("SCHEMA_INVALID")
    if verdict.request_id != request.request_id:
        return _error("REQUEST_MISMATCH")
    if verdict.control_id != request.control_id:
        return _error("REQUEST_MISMATCH")
    if (
        verdict.rubric_sha256 != request.rubric_sha256
        or verdict.rubric_id != request.rubric_id
        or verdict.rubric_version != request.rubric_version
    ):
        return _error("RUBRIC_MISMATCH")
    if verdict.input_manifest_sha256 != request.input_manifest_sha256:
        return _error("CONTRADICTORY_EVIDENCE")
    if (
        verdict.judge_id != request.judge.judge_id
        or verdict.judge_version != request.judge.judge_version
    ):
        return _error("REQUEST_MISMATCH")
    allowed_refs = set(envelope_data_keys)
    if any(ref not in allowed_refs for ref in verdict.evidence_refs):
        return _error("CONTRADICTORY_EVIDENCE")
    return JudgeOutcome(is_verdict=True, verdict=verdict, judge_error_kind=None)


def dispatch_mock_judgment(
    client: JudgeClient,
    request: JudgeRequest,
    envelope: Mapping[str, Any],
) -> JudgeOutcome:
    """The single canonical NON-LIVE judgment path (R2 §6).

    Binding is proven BEFORE any client dispatch (and therefore before any
    recorded mock response lookup); the client then receives the canonical
    envelope bytes, and the response is parsed against the same envelope.
    Every mismatch is a fail-closed JUDGE_ERROR outcome, never PASS/FAIL."""
    from .envelope import validate_request_envelope_binding

    try:
        validate_request_envelope_binding(request, envelope)
    except RunnerError:
        return _error("BINDING_MISMATCH")
    envelope_bytes = canonical_bytes(
        {k: envelope[k] for k in sorted(envelope)}
    )
    response = client.dispatch(request, envelope_bytes)
    return parse_judge_output(response, request, envelope)
