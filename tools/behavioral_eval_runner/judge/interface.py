"""NON-LIVE judge interface (WP-2B-2; prompt 11.A).

Represents pinned judge identity, model/provider identity AS DATA ONLY,
rubric and calibration identities, request/response identity, and
timeout/error representation. There is NO provider implementation: the only
concrete clients are ``DisabledJudgeProvider`` (denies with
LIVE_DISPATCH_DISABLED) and the recorded-fixture mock in ``mock.py``."""

from __future__ import annotations

import abc
from dataclasses import dataclass
from typing import Any, Mapping

from .. import GRADING_SCHEMA_VERSION
from ..enums import StrictEnum
from ..errors import LiveDispatchDisabledError, SchemaValidationError
from ..graders.records import VALID_CONTROL_IDS

_HEX = set("0123456789abcdef")


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise SchemaValidationError(message)


def _require_str(value: Any, where: str) -> str:
    _require(isinstance(value, str) and bool(value), f"{where} must be non-empty")
    return value


def _require_sha256(value: Any, where: str) -> str:
    _require(
        isinstance(value, str) and len(value) == 64 and set(value) <= _HEX,
        f"{where} must be a 64-hex SHA-256",
    )
    return value


class TransportOutcome(StrictEnum):
    """Closed transport-level outcomes of a (mock) judge dispatch."""

    OK = "OK"
    TIMEOUT = "TIMEOUT"
    TRANSPORT_ERROR = "TRANSPORT_ERROR"
    REFUSED = "REFUSED"
    MALFORMED_OUTPUT = "MALFORMED_OUTPUT"


@dataclass(frozen=True, slots=True)
class JudgeIdentity:
    """Pinned judge identity; model/provider fields are DATA ONLY here."""

    judge_id: str
    judge_version: str
    model_identifier: str
    provider_identifier: str
    policy_version: str
    policy_sha256: str

    def validate(self) -> None:
        _require_str(self.judge_id, "judge_id")
        _require_str(self.judge_version, "judge_version")
        _require_str(self.model_identifier, "model_identifier")
        _require_str(self.provider_identifier, "provider_identifier")
        _require_str(self.policy_version, "policy_version")
        _require_sha256(self.policy_sha256, "policy_sha256")

    def to_dict(self) -> dict[str, Any]:
        return {
            "judge_id": self.judge_id,
            "judge_version": self.judge_version,
            "model_identifier": self.model_identifier,
            "provider_identifier": self.provider_identifier,
            "policy_version": self.policy_version,
            "policy_sha256": self.policy_sha256,
        }

    _KEYS = frozenset(
        {
            "judge_id",
            "judge_version",
            "model_identifier",
            "provider_identifier",
            "policy_version",
            "policy_sha256",
        }
    )

    @classmethod
    def from_dict(cls, payload: Mapping[str, Any]) -> "JudgeIdentity":
        unknown = set(payload) - cls._KEYS
        _require(not unknown, f"JudgeIdentity: unknown keys {sorted(unknown)}")
        identity = cls(
            judge_id=payload.get("judge_id", ""),
            judge_version=payload.get("judge_version", ""),
            model_identifier=payload.get("model_identifier", ""),
            provider_identifier=payload.get("provider_identifier", ""),
            policy_version=payload.get("policy_version", ""),
            policy_sha256=payload.get("policy_sha256", ""),
        )
        identity.validate()
        return identity


@dataclass(frozen=True, slots=True)
class JudgeRequest:
    """One judgment request's identity (no transcript content lives here)."""

    request_id: str
    control_id: str
    judge: JudgeIdentity
    rubric_id: str
    rubric_version: str
    rubric_sha256: str
    envelope_sha256: str
    input_manifest_sha256: str
    assertion_uid: str | None = None
    calibration_dataset_id: str | None = None
    calibration_dataset_version: str | None = None
    calibration_dataset_sha256: str | None = None
    schema_version: str = GRADING_SCHEMA_VERSION

    def validate(self) -> None:
        _require_str(self.request_id, "request_id")
        _require(
            self.control_id in VALID_CONTROL_IDS,
            f"control_id must be a Scenario A control A-Q, got "
            f"{self.control_id!r}",
        )
        _require(isinstance(self.judge, JudgeIdentity), "judge must be JudgeIdentity")
        self.judge.validate()
        _require_str(self.rubric_id, "rubric_id")
        _require_str(self.rubric_version, "rubric_version")
        _require_sha256(self.rubric_sha256, "rubric_sha256")
        _require_sha256(self.envelope_sha256, "envelope_sha256")
        _require_sha256(self.input_manifest_sha256, "input_manifest_sha256")
        if self.assertion_uid is not None:
            _require_str(self.assertion_uid, "assertion_uid")
        dataset_fields = (
            self.calibration_dataset_id,
            self.calibration_dataset_version,
            self.calibration_dataset_sha256,
        )
        if any(field is not None for field in dataset_fields):
            _require(
                all(field is not None for field in dataset_fields),
                "calibration dataset identity must be complete or absent",
            )
            _require_sha256(
                self.calibration_dataset_sha256, "calibration_dataset_sha256"
            )
        _require(
            self.schema_version == GRADING_SCHEMA_VERSION,
            f"schema_version must be {GRADING_SCHEMA_VERSION}",
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "request_id": self.request_id,
            "control_id": self.control_id,
            "assertion_uid": self.assertion_uid,
            "judge": self.judge.to_dict(),
            "rubric_id": self.rubric_id,
            "rubric_version": self.rubric_version,
            "rubric_sha256": self.rubric_sha256,
            "envelope_sha256": self.envelope_sha256,
            "input_manifest_sha256": self.input_manifest_sha256,
            "calibration_dataset_id": self.calibration_dataset_id,
            "calibration_dataset_version": self.calibration_dataset_version,
            "calibration_dataset_sha256": self.calibration_dataset_sha256,
            "schema_version": self.schema_version,
        }

    _KEYS = frozenset(
        {
            "request_id",
            "control_id",
            "assertion_uid",
            "judge",
            "rubric_id",
            "rubric_version",
            "rubric_sha256",
            "envelope_sha256",
            "input_manifest_sha256",
            "calibration_dataset_id",
            "calibration_dataset_version",
            "calibration_dataset_sha256",
            "schema_version",
        }
    )

    @classmethod
    def from_dict(cls, payload: Mapping[str, Any]) -> "JudgeRequest":
        unknown = set(payload) - cls._KEYS
        _require(not unknown, f"JudgeRequest: unknown keys {sorted(unknown)}")
        request = cls(
            request_id=payload.get("request_id", ""),
            control_id=payload.get("control_id", ""),
            assertion_uid=payload.get("assertion_uid"),
            judge=JudgeIdentity.from_dict(payload.get("judge", {})),
            rubric_id=payload.get("rubric_id", ""),
            rubric_version=payload.get("rubric_version", ""),
            rubric_sha256=payload.get("rubric_sha256", ""),
            envelope_sha256=payload.get("envelope_sha256", ""),
            input_manifest_sha256=payload.get("input_manifest_sha256", ""),
            calibration_dataset_id=payload.get("calibration_dataset_id"),
            calibration_dataset_version=payload.get("calibration_dataset_version"),
            calibration_dataset_sha256=payload.get("calibration_dataset_sha256"),
            schema_version=payload.get("schema_version", ""),
        )
        request.validate()
        return request


@dataclass(frozen=True, slots=True)
class JudgeResponse:
    """A (mock) judge dispatch's transport result and raw output."""

    request_id: str
    response_id: str
    transport_outcome: TransportOutcome
    raw_output: str | None

    def validate(self) -> None:
        _require_str(self.request_id, "request_id")
        _require_str(self.response_id, "response_id")
        _require(
            isinstance(self.transport_outcome, TransportOutcome),
            "transport_outcome must be TransportOutcome",
        )
        if self.raw_output is not None:
            _require(isinstance(self.raw_output, str), "raw_output must be str|None")


class JudgeClient(abc.ABC):
    """Abstract judge dispatch boundary. No live implementation exists."""

    @abc.abstractmethod
    def dispatch(self, request: JudgeRequest, envelope_bytes: bytes) -> JudgeResponse:
        """Dispatch one judgment request; NON-LIVE in this phase."""


class DisabledJudgeProvider(JudgeClient):
    """The real provider adapter's place-holder: it DENIES every dispatch.

    WP-2B-2 authorizes zero actual judge/provider calls; this class is the
    fail-closed representation of that budget.
    """

    def __init__(self) -> None:
        self.dispatch_count = 0  # stays 0 forever: denial precedes counting

    def dispatch(self, request: JudgeRequest, envelope_bytes: bytes) -> JudgeResponse:
        raise LiveDispatchDisabledError(
            "actual judge/provider dispatch is not authorized in WP-2B-2 "
            "(BER-DEC-007: zero judge/provider calls; OD-1 OPEN; R2 BLOCKED)"
        )
