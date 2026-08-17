"""WP-2B-3 calibration error taxonomy (BER-DEC-008).

Every WP-2B-3 failure mode is typed so callers fail closed on the exact
boundary that broke. A STOP condition carries its closed reason; nothing
here ever maps a failure into a PASS/FAIL verdict.
"""

from __future__ import annotations

from ..enums import StrictEnum
from ..errors import RunnerError


class CalibrationStopReason(StrictEnum):
    """Closed BER-DEC-008 stop conditions (decision 26 and related terms)."""

    MODEL_IDENTITY_MISMATCH = "MODEL_IDENTITY_MISMATCH"
    BUDGET_TELEMETRY_UNAVAILABLE = "BUDGET_TELEMETRY_UNAVAILABLE"
    CAP_WOULD_BE_EXCEEDED = "CAP_WOULD_BE_EXCEEDED"
    CREDENTIAL_MISSING = "CREDENTIAL_MISSING"
    PROVIDER_AUTH_REJECTED = "PROVIDER_AUTH_REJECTED"
    PROXY_ENV_PRESENT = "PROXY_ENV_PRESENT"
    TLS_ENV_OVERRIDE_PRESENT = "TLS_ENV_OVERRIDE_PRESENT"
    BASE_URL_ENV_OVERRIDE_PRESENT = "BASE_URL_ENV_OVERRIDE_PRESENT"
    BASE_URL_MISMATCH = "BASE_URL_MISMATCH"
    SDK_VERSION_MISMATCH = "SDK_VERSION_MISMATCH"
    SDK_RETRY_CONFIG_INVALID = "SDK_RETRY_CONFIG_INVALID"
    REQUEST_SETTINGS_VIOLATION = "REQUEST_SETTINGS_VIOLATION"
    OWNER_APPROVAL_PENDING = "OWNER_APPROVAL_PENDING"
    HOLDOUT_NOT_FROZEN = "HOLDOUT_NOT_FROZEN"
    UNAUTHORIZED_EXECUTION_STAGE = "UNAUTHORIZED_EXECUTION_STAGE"
    DATASET_INTEGRITY_MISMATCH = "DATASET_INTEGRITY_MISMATCH"
    DEADLINE_EXCEEDED = "DEADLINE_EXCEEDED"
    CONCURRENCY_VIOLATION = "CONCURRENCY_VIOLATION"
    UNCLASSIFIED_TRANSPORT_ERROR = "UNCLASSIFIED_TRANSPORT_ERROR"


class CalibrationError(RunnerError):
    """Base class for every WP-2B-3 calibration failure."""


class CalibrationStopError(CalibrationError):
    """A BER-DEC-008 STOP condition: no further provider dispatch may occur.

    The stop is fail-closed and carries a closed ``CalibrationStopReason``.
    """

    def __init__(self, reason: CalibrationStopReason, message: str) -> None:
        if not isinstance(reason, CalibrationStopReason):
            raise TypeError("reason must be CalibrationStopReason")
        super().__init__(f"{reason.value}: {message}")
        self.stop_reason = reason


class CalibrationAuthorizationError(CalibrationError):
    """The calibration execution surface was invoked without a gate-issued
    authorization (or with a forged/mismatched one)."""


class LabelLeakError(CalibrationError):
    """Expected-label material tried to enter a judge-facing surface."""


class HoldoutAccessError(CalibrationError):
    """Sealed-holdout content was requested without the owner freeze state."""


class CalibrationLedgerError(CalibrationError):
    """Calibration accounting-ledger integrity or usage failure."""


class CalibrationReservationDenied(CalibrationLedgerError):
    """A pre-dispatch reservation was denied; the request must not begin."""

    reason_code = "BUDGET_CAP"
