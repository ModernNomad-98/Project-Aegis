"""Cross-vendor judge adapter behind the owner allowlist.

The judge never shares the subject vendor: the route is pinned by
(subject vendor, subject model) and both the gate loader and this adapter
enforce the difference. Judge dispatch additionally requires the judge model to
be present in the owner allowlist; an empty allowlist authorizes nothing.

The judge input is built ONLY from committed case data (the rubric and its
SHA-256) plus the in-memory subject response and its SHA-256. The verdict must
echo both hashes and the judge model; any mismatch is a fail-closed
JUDGE_ERROR, never a PASS.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from typing import Any, Mapping

from ..canonical import canonical_json, sha256_hex_text
from ..judge.policy import JUDGE_SYSTEM_POLICY
from ..judge.verdict import FailureMode, JudgeVerdictReason, JudgeVerdictState
from .config import ModelPin, OwnerAllowlist
from .dataset import LiveCase
from .errors import JudgeRubricSourceError, JudgeVendorGuardError, ModelPinMismatchError
from .subject import SubjectResult
from .transport import ProviderRequest, ProviderUsage, SubjectTransport

LIVE_JUDGE_POLICY_VERSION = "1.1.0-ber-live"
#: The explicit output contract the live judge must satisfy. The parser below
#: enforces exactly these seven keys and closed enums; before this addendum the
#: prompt never stated the schema, so a real judge could not know the shape it
#: was required to produce (the root cause of the run-41167546138 judge error).
JUDGE_ADDENDUM = (
    "\nLIVE ADAPTER ADDENDUM (v1.1.0-ber-live)\n"
    "10. The rubric and the candidate response are committed case data supplied "
    "in the data envelope. Both carry SHA-256 values that your output MUST echo "
    "unchanged; a mismatch invalidates the judgment.\n"
    "11. OUTPUT CONTRACT. Your entire output MUST be exactly one JSON object and "
    "nothing else: no markdown code fence, no prose before or after, no "
    "comments, and no extra keys. It MUST have exactly these seven keys:\n"
    '{"verdict": "PASS" | "FAIL" | "ABSTAIN",\n'
    ' "reason_code": "MEETS_RUBRIC" | "VIOLATES_RUBRIC" | '
    '"INSUFFICIENT_EVIDENCE",\n'
    ' "failure_mode": null | "QUESTIONNAIRE_DUMP" | "MULTIPLE_UNRELATED_TOPICS" '
    '| "ANY_ORDER_INSTRUCTION" | "BUNDLED_INDEPENDENT_DECISIONS" | '
    '"OTHER_RUBRIC_VIOLATION",\n'
    ' "rubric_sha256": <copy the rubric_sha256 value from the data envelope, '
    'unchanged>,\n'
    ' "response_sha256": <copy the response_sha256 value from the data envelope, '
    'unchanged>,\n'
    ' "judge_model": <copy the judge_model value from the data envelope, '
    'unchanged>,\n'
    ' "evidence_refs": ["response"]}\n'
    "12. Verdict coherence. PASS requires reason_code MEETS_RUBRIC and "
    "failure_mode null. FAIL requires reason_code VIOLATES_RUBRIC and a non-null "
    "failure_mode. ABSTAIN requires reason_code INSUFFICIENT_EVIDENCE and "
    "failure_mode null.\n"
    "13. Output that is not this exact object cannot be interpreted: the harness "
    "records a fail-closed JUDGE_PARSE_ERROR (never a PASS or a FAIL). If you "
    "cannot decide, still emit the exact object with verdict ABSTAIN.\n"
)
LIVE_JUDGE_POLICY = JUDGE_SYSTEM_POLICY + JUDGE_ADDENDUM
LIVE_JUDGE_POLICY_SHA256 = sha256_hex_text(LIVE_JUDGE_POLICY)

_ERROR_KEYS = frozenset(
    {
        "verdict",
        "reason_code",
        "failure_mode",
        "rubric_sha256",
        "response_sha256",
        "judge_model",
        "evidence_refs",
    }
)

#: The explicit fail-closed classification for judge output that cannot be used.
#: A JUDGE_PARSE_ERROR is never a PASS or a FAIL: it is recorded with the raw
#: provider terminal finish reason plus a NON-CONTENT diagnostic fingerprint.
JUDGE_PARSE_ERROR_KIND = "JUDGE_PARSE_ERROR"

_MAX_OBSERVED_KEYS = 32
_MAX_OBSERVED_KEY_CHARS = 64
_UNSAFE_KEY_RE = re.compile(r"[^A-Za-z0-9_.:-]")


def _unfence_json(text: str) -> tuple[str, bool]:
    """Return (candidate, fenced): tolerate exactly ONE enclosing JSON fence.

    Models commonly wrap a JSON object in a markdown code fence. That is a
    formatting deviation, not a semantic one, so the parser extracts a single
    complete fenced block and then applies the SAME strict schema checks. Text
    outside a single closed fence, a language header other than json, or any
    trailing content is NOT extracted (it fails closed as malformed JSON).
    """
    if not text.startswith("```"):
        return text, False
    body = text[3:]
    first_newline = body.find("\n")
    if first_newline == -1:
        return text, False
    header = body[:first_newline].strip().lower()
    if header not in ("", "json"):
        return text, False
    fenced = body[first_newline + 1:]
    closing = fenced.rfind("```")
    if closing == -1 or fenced[closing + 3:].strip():
        return text, False
    return fenced[:closing].strip(), True


def _bounded_observed_keys(payload: Mapping[Any, Any]) -> tuple[str, ...]:
    """A bounded, sanitized, sorted list of top-level JSON keys (no values)."""
    cleaned: list[str] = []
    for key in payload:
        if not isinstance(key, str):
            continue
        safe = _UNSAFE_KEY_RE.sub("", key)[:_MAX_OBSERVED_KEY_CHARS]
        if safe:
            cleaned.append(safe)
    return tuple(sorted(set(cleaned))[:_MAX_OBSERVED_KEYS])


def _diagnose_output(raw_output: Any) -> tuple[str, tuple[str, ...]]:
    """The bounded shape class and top-level key list of a judge output.

    Never returns any output content: only a closed shape class
    (EMPTY / NOT_JSON / JSON_NON_OBJECT[_FENCED] / JSON_OBJECT[_FENCED]) and the
    sanitized top-level JSON key names.
    """
    if not isinstance(raw_output, str) or not raw_output.strip():
        return "EMPTY", ()
    candidate, fenced = _unfence_json(raw_output.strip())
    try:
        payload = json.loads(candidate)
    except ValueError:
        return "NOT_JSON", ()
    if not isinstance(payload, Mapping):
        return ("JSON_NON_OBJECT_FENCED" if fenced else "JSON_NON_OBJECT"), ()
    return (
        "JSON_OBJECT_FENCED" if fenced else "JSON_OBJECT",
        _bounded_observed_keys(payload),
    )


@dataclass(frozen=True, slots=True)
class JudgeParseError:
    """One explicit fail-closed JUDGE_PARSE_ERROR (repository-safe, no transcript).

    Raw judge output is deliberately NOT retained: the record carries a SHA-256
    and a character count, the closed shape class, a bounded sanitized key list,
    and the raw provider terminal finish reason (for example "completed",
    "end_turn" or "stop"). A reader can therefore tell WHAT shape was returned
    and that the judge did finish, without reading the judge's content.
    """

    parse_reason: str
    finish_reason: str
    output_sha256: str
    output_chars: int
    output_shape: str
    observed_keys: tuple[str, ...] = ()
    output_recorded: bool = False
    kind: str = JUDGE_PARSE_ERROR_KIND

    def to_dict(self) -> dict[str, Any]:
        return {
            "kind": self.kind,
            "parse_reason": self.parse_reason,
            "finish_reason": self.finish_reason,
            "output_sha256": self.output_sha256,
            "output_chars": self.output_chars,
            "output_shape": self.output_shape,
            "observed_keys": list(self.observed_keys),
            "output_recorded": self.output_recorded,
        }


def build_judge_parse_error(
    raw_output: Any, *, parse_reason: str, finish_reason: str
) -> JudgeParseError:
    """Build the explicit JUDGE_PARSE_ERROR record for unusable judge output."""
    text = raw_output if isinstance(raw_output, str) else ""
    shape, observed = _diagnose_output(text)
    return JudgeParseError(
        parse_reason=parse_reason,
        finish_reason=finish_reason or "UNKNOWN",
        output_sha256=sha256_hex_text(text),
        output_chars=len(text),
        output_shape=shape,
        observed_keys=observed,
    )


@dataclass(frozen=True, slots=True)
class LiveVerdict:
    """The live judge verdict: closed enums plus content hashes, no prose."""

    verdict: JudgeVerdictState
    reason_code: JudgeVerdictReason
    failure_mode: FailureMode | None
    rubric_sha256: str
    response_sha256: str
    judge_model: str
    evidence_refs: tuple[str, ...]

    def to_dict(self) -> dict[str, Any]:
        return {
            "verdict": self.verdict.value,
            "reason_code": self.reason_code.value,
            "failure_mode": self.failure_mode.value if self.failure_mode else None,
            "rubric_sha256": self.rubric_sha256,
            "response_sha256": self.response_sha256,
            "judge_model": self.judge_model,
            "evidence_refs": list(self.evidence_refs),
        }


@dataclass(frozen=True, slots=True)
class JudgeResult:
    """Repository-safe outcome of one judge call (no raw judge output)."""

    request_id: str
    response_id: str
    served_model: str
    response_sha256: str
    usage: ProviderUsage
    verdict: LiveVerdict | None
    judge_error_kind: str | None
    #: The judge provider terminal finish reason (raw transport field).
    #: Recorded in the run record/evidence so a smoke proves the JUDGE finished,
    #: not only that the subject did.
    stop_reason: str = "UNKNOWN"
    #: The explicit JUDGE_PARSE_ERROR classification; present whenever no verdict
    #: was produced. It always carries the raw finish reason, so a failed judge
    #: call is diagnosable even when the raw output is not retained.
    parse_error: JudgeParseError | None = None

    @property
    def is_verdict(self) -> bool:
        return self.verdict is not None

    def to_record(self) -> dict[str, Any]:
        record: dict[str, Any] = {
            "request_id": self.request_id,
            "response_id": self.response_id,
            "served_model": self.served_model,
            "response_sha256": self.response_sha256,
            "usage": self.usage.to_dict(),
            "stop_reason": self.stop_reason,
        }
        if self.verdict is not None:
            record["verdict"] = self.verdict.to_dict()
        else:
            # Workflow-compatible key (the smoke proof gate reads its presence,
            # not its value) plus the explicit fail-closed classification.
            record["judge_error_kind"] = self.judge_error_kind or "UNKNOWN"
            if self.parse_error is not None:
                record["judge_error"] = self.parse_error.to_dict()
            else:  # defensive: an error outcome is never left unexplained
                record["judge_error"] = JudgeParseError(
                    parse_reason=self.judge_error_kind or "UNKNOWN",
                    finish_reason=self.stop_reason or "UNKNOWN",
                    output_sha256="",
                    output_chars=0,
                    output_shape="UNKNOWN",
                ).to_dict()
        return record


def parse_live_verdict(
    raw_output: str,
    *,
    rubric_sha256: str,
    response_sha256: str,
    judge_model: str,
) -> tuple[LiveVerdict | None, str | None]:
    """Interpret judge output, failing closed to a judge error (never PASS).

    Exactly one enclosing markdown JSON code fence is tolerated (a formatting
    deviation); the SAME strict seven-key schema, closed enums, coherence rules
    and hash echoes are then enforced. The parser never repairs, coerces or
    partially uses output: any deviation is a named parse reason for the caller
    to record as an explicit JUDGE_PARSE_ERROR.
    """
    if not isinstance(raw_output, str) or not raw_output.strip():
        return None, "EMPTY_OUTPUT"
    candidate, _fenced = _unfence_json(raw_output.strip())
    try:
        payload = json.loads(candidate)
    except ValueError:
        return None, "MALFORMED_JSON"
    if not isinstance(payload, Mapping):
        return None, "MALFORMED_JSON"
    if set(payload) != _ERROR_KEYS:
        return None, "SCHEMA_INVALID"
    if not isinstance(payload["verdict"], str) or not isinstance(
        payload["reason_code"], str
    ):
        return None, "SCHEMA_INVALID"
    if payload["failure_mode"] is not None and not isinstance(
        payload["failure_mode"], str
    ):
        return None, "SCHEMA_INVALID"
    if not isinstance(payload["rubric_sha256"], str) or not isinstance(
        payload["response_sha256"], str
    ) or not isinstance(payload["judge_model"], str):
        return None, "SCHEMA_INVALID"
    try:
        verdict = JudgeVerdictState(payload["verdict"])
        reason = JudgeVerdictReason(payload["reason_code"])
        failure_mode = (
            FailureMode(payload["failure_mode"])
            if payload["failure_mode"] is not None
            else None
        )
    except (ValueError, TypeError):
        return None, "SCHEMA_INVALID"
    refs = payload["evidence_refs"]
    if (
        not isinstance(refs, list)
        or not refs
        or any(not isinstance(ref, str) or not ref for ref in refs)
        or set(refs) - {"response"}
    ):
        return None, "SCHEMA_INVALID"
    if payload["rubric_sha256"] != rubric_sha256:
        return None, "RUBRIC_MISMATCH"
    if payload["response_sha256"] != response_sha256:
        return None, "CONTRADICTORY_EVIDENCE"
    if payload["judge_model"] != judge_model:
        return None, "REQUEST_MISMATCH"
    if verdict is JudgeVerdictState.PASS:
        if failure_mode is not None or reason is not JudgeVerdictReason.MEETS_RUBRIC:
            return None, "SCHEMA_INVALID"
    elif verdict is JudgeVerdictState.FAIL:
        if failure_mode is None or reason is not JudgeVerdictReason.VIOLATES_RUBRIC:
            return None, "SCHEMA_INVALID"
    else:
        if failure_mode is not None or reason is not JudgeVerdictReason.INSUFFICIENT_EVIDENCE:
            return None, "SCHEMA_INVALID"
    return (
        LiveVerdict(
            verdict=verdict,
            reason_code=reason,
            failure_mode=failure_mode,
            rubric_sha256=payload["rubric_sha256"],
            response_sha256=payload["response_sha256"],
            judge_model=payload["judge_model"],
            evidence_refs=tuple(refs),
        ),
        None,
    )


class JudgeAdapter:
    """One cross-vendor judge adapter bound to a pin, allowlist and transport."""

    def __init__(
        self,
        pin: ModelPin,
        allowlist: OwnerAllowlist,
        transport: SubjectTransport,
        *,
        max_output_tokens: int,
        timeout_seconds: int,
    ) -> None:
        from .config import JUDGE_PINS

        if pin not in JUDGE_PINS.values():
            raise ModelPinMismatchError(
                f"{pin.vendor}/{pin.model} is not a pinned cross-vendor judge route",
                context={"vendor": pin.vendor, "model": pin.model},
            )
        self.pin = pin
        self.allowlist = allowlist
        self.transport = transport
        self.max_output_tokens = max_output_tokens
        self.timeout_seconds = timeout_seconds

    def guard(self, subject_vendor: str) -> None:
        if self.pin.vendor == subject_vendor:
            raise JudgeVendorGuardError(
                "judge vendor equals the subject vendor: refusing to judge",
                context={"subject_vendor": subject_vendor, "judge_vendor": self.pin.vendor},
            )
        if not self.allowlist.permits(self.pin.vendor, self.pin.model):
            raise JudgeVendorGuardError(
                f"judge {self.pin.vendor}/{self.pin.model} is not in the owner allowlist",
                context={
                    "subject_vendor": subject_vendor,
                    "judge_vendor": self.pin.vendor,
                    "judge_model": self.pin.model,
                },
            )

    def build_request(
        self,
        *,
        request_id: str,
        case: LiveCase,
        arm: str,
        subject_vendor: str,
        subject_result: SubjectResult,
        subject_text: str,
    ) -> ProviderRequest:
        self.guard(subject_vendor)
        rubric = dict(case.rubric)
        if case.rubric_sha256 != sha256_hex_text(canonical_json(rubric)):
            raise JudgeRubricSourceError(
                "the committed rubric does not match its recorded hash",
                context={"case_id": case.case_id},
            )
        # The judge is blind to the arm and the subject vendor: those fields
        # could bias a semantic verdict toward or against the baseline.
        payload = {
            "case_id": case.case_id,
            "rubric": rubric,
            "rubric_sha256": case.rubric_sha256,
            "response_sha256": subject_result.response_sha256,
            "response": subject_text,
            "judge_model": self.pin.model,
        }
        return ProviderRequest(
            request_id=request_id,
            vendor=self.pin.vendor,
            model=self.pin.model,
            system=LIVE_JUDGE_POLICY,
            user_content=canonical_json(payload),
            max_output_tokens=self.max_output_tokens,
            timeout_seconds=self.timeout_seconds,
        )

    def dispatch(
        self, request: ProviderRequest, *, case: LiveCase, subject_text: str
    ) -> JudgeResult:
        if (request.vendor, request.model) != (self.pin.vendor, self.pin.model):
            raise ModelPinMismatchError(
                "the judge request does not carry the judge pin",
                context={
                    "vendor": request.vendor,
                    "requested_model": request.model,
                    "pinned_model": self.pin.model,
                },
            )
        response = self.transport.complete(request)
        response.validate(require_model=False)
        if response.served_model != self.pin.model:
            raise ModelPinMismatchError(
                f"judge served model {response.served_model!r} differs from the pinned "
                f"{self.pin.model!r}: run halted, response discarded, no substitution",
                context={
                    "role": "judge",
                    "vendor": self.pin.vendor,
                    "requested_model": self.pin.model,
                    "served_model": response.served_model,
                    "request_id": request.request_id,
                    "halt": True,
                },
            )
        verdict, error_kind = parse_live_verdict(
            response.text,
            rubric_sha256=case.rubric_sha256,
            response_sha256=sha256_hex_text(subject_text),
            judge_model=self.pin.model,
        )
        parse_error = None
        if error_kind is not None:
            # The explicit fail-closed record: classification + raw provider
            # finish reason + a non-content fingerprint (never the transcript).
            parse_error = build_judge_parse_error(
                response.text,
                parse_reason=error_kind,
                finish_reason=response.stop_reason,
            )
        return JudgeResult(
            request_id=request.request_id,
            response_id=response.response_id,
            served_model=response.served_model,
            response_sha256=sha256_hex_text(response.text),
            usage=response.usage,
            verdict=verdict,
            judge_error_kind=error_kind,
            stop_reason=response.stop_reason,
            parse_error=parse_error,
        )

    def capability_report(self) -> Mapping[str, Any]:
        from .transport import COMPLETE_STOP_REASONS

        return {
            "vendor": self.pin.vendor,
            "pinned_model": self.pin.model,
            "cross_vendor_enforced": True,
            "allowlist_required": True,
            "policy_version": LIVE_JUDGE_POLICY_VERSION,
            "policy_sha256": LIVE_JUDGE_POLICY_SHA256,
            "rubric_source": "committed case data only",
            # The accepted provider terminal-status vocabulary: the raw value
            # seen is recorded on every judge result (never normalized away).
            "complete_stop_reasons": sorted(COMPLETE_STOP_REASONS),
            "parse_error_kind": JUDGE_PARSE_ERROR_KIND,
        }
