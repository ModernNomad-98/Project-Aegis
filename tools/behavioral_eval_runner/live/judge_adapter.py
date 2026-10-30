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

LIVE_JUDGE_POLICY_VERSION = "1.0.0-ber-live"
JUDGE_ADDENDUM = (
    "\nLIVE ADAPTER ADDENDUM (v1.0.0-ber-live)\n"
    "10. The rubric and the candidate response are committed case data supplied "
    "in the data envelope. Both carry SHA-256 values that your output MUST echo "
    "unchanged; a mismatch invalidates the judgment.\n"
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
    served_model: str
    response_sha256: str
    usage: ProviderUsage
    verdict: LiveVerdict | None
    judge_error_kind: str | None

    @property
    def is_verdict(self) -> bool:
        return self.verdict is not None

    def to_record(self) -> dict[str, Any]:
        record: dict[str, Any] = {
            "request_id": self.request_id,
            "served_model": self.served_model,
            "response_sha256": self.response_sha256,
            "usage": self.usage.to_dict(),
        }
        if self.verdict is not None:
            record["verdict"] = self.verdict.to_dict()
        else:
            record["judge_error_kind"] = self.judge_error_kind or "UNKNOWN"
        return record


def parse_live_verdict(
    raw_output: str,
    *,
    rubric_sha256: str,
    response_sha256: str,
    judge_model: str,
) -> tuple[LiveVerdict | None, str | None]:
    """Interpret judge output, failing closed to a judge error (never PASS)."""
    if not isinstance(raw_output, str) or not raw_output.strip():
        return None, "EMPTY_OUTPUT"
    try:
        payload = json.loads(raw_output)
    except ValueError:
        return None, "MALFORMED_JSON"
    if not isinstance(payload, Mapping):
        return None, "MALFORMED_JSON"
    if set(payload) != _ERROR_KEYS:
        return None, "SCHEMA_INVALID"
    try:
        verdict = JudgeVerdictState(payload["verdict"])
        reason = JudgeVerdictReason(payload["reason_code"])
        failure_mode = (
            FailureMode(payload["failure_mode"]) if payload["failure_mode"] is not None else None
        )
    except ValueError:
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
        payload = {
            "case_id": case.case_id,
            "arm": arm,
            "subject_vendor": subject_vendor,
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
        response = self.transport.complete(request)
        response.validate()
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
        return JudgeResult(
            request_id=request.request_id,
            served_model=response.served_model,
            response_sha256=sha256_hex_text(response.text),
            usage=response.usage,
            verdict=verdict,
            judge_error_kind=error_kind,
        )

    def capability_report(self) -> Mapping[str, Any]:
        return {
            "vendor": self.pin.vendor,
            "pinned_model": self.pin.model,
            "cross_vendor_enforced": True,
            "allowlist_required": True,
            "policy_version": LIVE_JUDGE_POLICY_VERSION,
            "policy_sha256": LIVE_JUDGE_POLICY_SHA256,
            "rubric_source": "committed case data only",
        }
