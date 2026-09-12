"""WP-2B-3 process-scoped credential boundary (BER-DEC-008 decisions 23, 32).

Stage A1 implements but never exercises credential loading: no real secret is
accessed, and tests use obvious dummy sentinels only. The future mechanism is
process-scoped ephemeral secret injection into the single authorized
calibration process — never a persistent user/machine environment variable,
CLI argument, file, log, evidence artifact, crash dump, or PR body.
"""

from __future__ import annotations

import os
from typing import MutableMapping

from .calibration_errors import CalibrationStopError, CalibrationStopReason

#: The process-scoped injection variable the single authorized calibration
#: process consumes. It must be injected ephemerally into that process only
#: and is removed from the process environment on first read (consume-once).
CREDENTIAL_ENV_VAR = "AEGIS_WP2B3_JUDGE_CREDENTIAL"

_REDACTED = "CalibrationCredential(REDACTED)"


class CalibrationCredential:
    """An opaque credential handle whose value can never be printed.

    ``repr``/``str`` are redacted; the value is reachable only through the
    deliberately alarming ``reveal_for_transport_use_only`` accessor, whose
    sole legitimate caller is the transport client factory.
    """

    __slots__ = ("_value",)

    def __init__(self, value: str) -> None:
        if not isinstance(value, str) or not value:
            raise CalibrationStopError(
                CalibrationStopReason.CREDENTIAL_MISSING,
                "credential value must be a non-empty string",
            )
        self._value = value

    def __repr__(self) -> str:  # never the value
        return _REDACTED

    def __str__(self) -> str:  # never the value
        return _REDACTED

    def reveal_for_transport_use_only(self) -> str:
        """Return the raw value for SDK client construction ONLY."""
        return self._value

    def redact_from_text(self, text: str) -> str:
        """Defensively strip the value from any outbound text."""
        if not isinstance(text, str):
            return text
        return text.replace(self._value, "[REDACTED]")


def consume_process_scoped_credential(
    environ: MutableMapping[str, str] | None = None,
) -> CalibrationCredential:
    """Read AND remove the credential from the process environment.

    Consume-once: after this call the variable is gone from ``environ``, so
    child processes cannot inherit it and later environment dumps cannot
    contain it. A missing credential is a STOP condition, never a workaround
    (BER-DEC-008 decision 23). The default target is the REAL process
    environment — passing a copy would silently defeat consume-once, so
    callers should omit the argument outside tests.
    """
    if environ is None:
        environ = os.environ
    value = environ.get(CREDENTIAL_ENV_VAR)
    if not value:
        raise CalibrationStopError(
            CalibrationStopReason.CREDENTIAL_MISSING,
            f"{CREDENTIAL_ENV_VAR} is not present in the process environment; "
            "a missing credential is a STOP condition",
        )
    credential = CalibrationCredential(value)
    try:
        del environ[CREDENTIAL_ENV_VAR]
    except KeyError:  # pragma: no cover - defensive
        pass
    return credential
