"""Structured, fail-closed errors for the gated live package.

Every error carries a stable reason code and a structured context mapping so a
caller (or the command-line interface) can halt on the exact boundary that
broke without parsing prose. An error never maps to a PASS.
"""

from __future__ import annotations

from typing import Any, Mapping

from ..errors import RunnerError


class LiveError(RunnerError):
    """Base class for every gated-live error."""

    reason_code = "LIVE_ERROR"

    def __init__(
        self,
        message: str,
        *,
        context: Mapping[str, Any] | None = None,
        reason_code: str | None = None,
    ) -> None:
        super().__init__(message, reason_code=reason_code or self.reason_code)
        self.context: dict[str, Any] = dict(context or {})

    def to_dict(self) -> dict[str, Any]:
        return {
            "error": type(self).__name__,
            "reason_code": self.reason_code,
            "detail": str(self),
            "context": dict(self.context),
        }


class LiveGateRefusedError(LiveError):
    """A live verb was requested without a valid owner gate."""

    reason_code = "LIVE_GATE_REFUSED"


class LiveConfigRefusedError(LiveError):
    """A live verb refused the configuration before any call.

    Used for the two fail-closed live-setting guards: a build-only dry-run
    config source (reason code DRY_RUN_CONFIG_REFUSED) and an output budget
    below the live floor (reason code LIVE_OUTPUT_TOKENS_TOO_LOW). The specific
    reason code is passed by the raiser so the caller can halt on the exact
    boundary that broke.
    """

    reason_code = "LIVE_CONFIG_REFUSED"


class MissingCredentialError(LiveError):
    """A required credential environment variable is absent: fail closed."""

    reason_code = "CREDENTIAL_MISSING"


class ModelPinMismatchError(LiveError):
    """The served model string differs from the pinned identifier: HALT.

    This is a halt, not a retry and not a substitution: the response is
    discarded and the caller dispatches nothing further.
    """

    reason_code = "MODEL_PIN_MISMATCH"


class JudgeVendorGuardError(LiveError):
    """The judge would share the subject vendor, or is outside the allowlist."""

    reason_code = "JUDGE_VENDOR_GUARD"


class JudgeRubricSourceError(LiveError):
    """Judge rubric input did not come from committed case data."""

    reason_code = "JUDGE_RUBRIC_SOURCE"


class CostCeilingHaltError(LiveError):
    """The configured spend ceiling would be exceeded: halt dispatch.

    Callers record the remaining cases UNRUN/BUDGET_CAP; an unrun case is
    never PASS.
    """

    reason_code = "BUDGET_CAP"


class LiveTransportUnavailableError(LiveError):
    """No authorized live transport exists in this environment: fail closed."""

    reason_code = "LIVE_TRANSPORT_UNAVAILABLE"


class LiveDatasetError(LiveError):
    """Committed case data is missing, unparsable, or hash-mismatched."""

    reason_code = "LIVE_DATASET_INVALID"


class ProviderTransportError(LiveError):
    """A provider call failed at the transport boundary (no verdict produced)."""

    reason_code = "TRANSPORT_ERROR"
