"""Exception hierarchy for the WP-2B-1 offline runner core.

Every failure mode has a typed exception so callers can fail closed on the
exact boundary that broke. Reason codes reference the versioned reason-code
set in enums.py; exceptions never map an error into a PASS/FAIL verdict.
"""

from __future__ import annotations


class RunnerError(Exception):
    """Base class for every runner-raised error."""

    reason_code: str | None = None

    def __init__(self, message: str, *, reason_code: str | None = None) -> None:
        super().__init__(message)
        if reason_code is not None:
            self.reason_code = reason_code


class CanonicalizationError(RunnerError):
    """An object cannot be represented in canonical JSON."""


class SchemaValidationError(RunnerError):
    """A record violates its versioned schema contract."""


class UnknownEnumValueError(SchemaValidationError):
    """A value outside a closed, versioned enum set was rejected."""


class IdentityError(RunnerError):
    """A canonical identity (case_uid / assertion_uid / attempt id) is invalid."""


class CensusError(RunnerError):
    """The implementation-time corpus census failed."""


class CensusBaselineMismatchError(CensusError):
    """The pinned corpus does not match the expected baseline (STOP condition)."""


class ClassificationError(RunnerError):
    """Runtime-surface classification failed closed."""


class MaterializationError(RunnerError):
    """Workspace materialization failed closed."""


class SnapshotVerificationError(MaterializationError):
    """Commit/tree verification of the immutable source snapshot failed."""


class PathEscapeError(MaterializationError):
    """A path escaped its containment root (absolute, '..', or resolution escape)."""


class ReparsePointError(MaterializationError):
    """A symlink/junction/mount/other reparse point was refused."""


class ControlPlaneLeakageError(MaterializationError):
    """A control-plane file would become agent-visible."""


class PartialSurfaceViolationError(MaterializationError):
    """A reduced skill surface was used for a full-library claim."""


class RoleMismatchError(MaterializationError):
    """Workspace role and materialization profile are inconsistent."""


class PreflightError(RunnerError):
    """Capability/fixture preflight could not be evaluated."""


class ProfileError(RunnerError):
    """Execution-profile capture or validation failed."""


class ContainmentError(RunnerError):
    """Containment boundary failure (base)."""


class ContainmentUnavailableError(ContainmentError):
    """The real-host containment capability is UNAVAILABLE/UNKNOWN: fail closed."""


class ContainmentViolationError(ContainmentError):
    """An operation violated the (mock/synthetic) containment boundary."""


class ProcessControlError(RunnerError):
    """Timeout / process-tree kill machinery failure."""


class BudgetError(RunnerError):
    """Budget/reservation machinery failure (base)."""


class ReservationDeniedError(BudgetError):
    """A pre-dispatch reservation was denied; the attempt must stay UNRUN."""

    reason_code = "BUDGET_CAP"


class LedgerIntegrityError(BudgetError):
    """The append-only budget ledger is inconsistent or would be silently reset."""


class SchedulerError(RunnerError):
    """Deterministic scheduling failure."""


class AggregationError(RunnerError):
    """Attempt/quorum aggregation failure."""


class DuplicateAttemptError(AggregationError):
    """A second attempt record for the same (run_id, case_uid, repetition_number)."""


class ImmutableRecordError(AggregationError):
    """An attempt record mutation was refused."""


class EvidenceError(RunnerError):
    """Evidence finalization/verification failure (base)."""


class EvidenceIntegrityError(EvidenceError):
    """Corrupt, missing, truncated, or mismatched evidence: fail closed.

    Maps to attempt_state=ERROR with reason_code=EVIDENCE_INTEGRITY_FAILURE;
    it is never a verdict.
    """

    reason_code = "EVIDENCE_INTEGRITY_FAILURE"


class CircularEvidenceError(EvidenceIntegrityError):
    """An artifact directly or indirectly hashes itself."""


class ReportError(RunnerError):
    """Report generation failure."""


class DishonestReportError(ReportError):
    """A report claimed more than its evidence supports (e.g. PASS without quorum)."""


class AdapterError(RunnerError):
    """Host-adapter failure (base)."""


class LiveDispatchDisabledError(AdapterError):
    """Every live dispatch path is disabled in WP-2B-1 (BER-DEC-006).

    Raised deterministically by the non-live Claude Code adapter for every
    attempt to spawn a session or reach a provider.
    """

    reason_code = "LIVE_DISPATCH_DISABLED"


class CliError(RunnerError):
    """CLI usage or execution failure."""
