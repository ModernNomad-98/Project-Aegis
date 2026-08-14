"""WP-2B-3 execution gates (BER-DEC-008 decisions 19, 26, 34-35; task
sections 16-17).

The hard Stage-A1 gate: NO provider judgment call may happen while
OWNER_LABEL_APPROVAL is PENDING. Claude cannot self-certify labels as
human-approved — only an explicit owner approval artifact whose hashes bind
the exact dataset, split map, and labeling guide unlocks the DEVELOPMENT
stage, and the sealed holdout additionally requires the later owner
freeze state (decision 19 OWNER_WAIT gate). Authorization objects can be
constructed ONLY through the gate functions here.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping

from ..enums import StrictEnum
from ..errors import SchemaValidationError
from .calibration_errors import (
    CalibrationAuthorizationError,
    CalibrationStopError,
    CalibrationStopReason,
    HoldoutAccessError,
)
from .calibration_transport import (
    HOLDOUT_MAX_OUTPUT_TOKENS_RANGE,
    REASONING_EFFORT,
)

_HEX = set("0123456789abcdef")


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise SchemaValidationError(message)


def _require_sha256(value: Any, where: str) -> str:
    _require(
        isinstance(value, str) and len(value) == 64 and set(value) <= _HEX,
        f"{where} must be a 64-hex SHA-256",
    )
    return value


class ExecutionStage(StrictEnum):
    DEVELOPMENT = "DEVELOPMENT"
    OWNER_WAIT = "OWNER_WAIT"
    SEALED_HOLDOUT = "SEALED_HOLDOUT"


class OwnerApprovalStatus(StrictEnum):
    PENDING = "PENDING"
    APPROVED = "APPROVED"


@dataclass(frozen=True, slots=True)
class DatasetIdentity:
    """The hash-bound identity the approval artifact must match exactly."""

    dataset_id: str
    dataset_version: str
    dataset_sha256: str
    split_map_sha256: str
    labeling_guide_sha256: str

    def validate(self) -> None:
        for name in ("dataset_id", "dataset_version"):
            value = getattr(self, name)
            _require(isinstance(value, str) and bool(value), f"{name} required")
        for name in ("dataset_sha256", "split_map_sha256",
                     "labeling_guide_sha256"):
            _require_sha256(getattr(self, name), name)


@dataclass(frozen=True, slots=True)
class OwnerLabelApproval:
    """The owner label-approval artifact (BER-DEC-008 decision 34).

    Stage A1 always carries status PENDING; only Peter Nguyen's explicit
    future approval — hash-bound to the exact dataset — flips it.
    """

    status: OwnerApprovalStatus
    approved_by: str
    approval_statement: str
    approval_date: str
    dataset_id: str
    dataset_version: str
    dataset_sha256: str
    split_map_sha256: str
    labeling_guide_sha256: str

    def validate(self) -> None:
        _require(
            isinstance(self.status, OwnerApprovalStatus),
            "status must be OwnerApprovalStatus",
        )
        for name in ("approved_by", "approval_statement", "approval_date",
                     "dataset_id", "dataset_version"):
            value = getattr(self, name)
            _require(isinstance(value, str) and bool(value), f"{name} required")
        for name in ("dataset_sha256", "split_map_sha256",
                     "labeling_guide_sha256"):
            _require_sha256(getattr(self, name), name)

    @classmethod
    def pending(cls, identity: DatasetIdentity) -> "OwnerLabelApproval":
        identity.validate()
        return cls(
            status=OwnerApprovalStatus.PENDING,
            approved_by="PENDING — no human approval exists",
            approval_statement=(
                "OWNER_LABEL_APPROVAL: PENDING — candidate labels are "
                "Claude/AI-proposed and are NOT human labels"
            ),
            approval_date="PENDING",
            dataset_id=identity.dataset_id,
            dataset_version=identity.dataset_version,
            dataset_sha256=identity.dataset_sha256,
            split_map_sha256=identity.split_map_sha256,
            labeling_guide_sha256=identity.labeling_guide_sha256,
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "status": self.status.value,
            "approved_by": self.approved_by,
            "approval_statement": self.approval_statement,
            "approval_date": self.approval_date,
            "dataset_id": self.dataset_id,
            "dataset_version": self.dataset_version,
            "dataset_sha256": self.dataset_sha256,
            "split_map_sha256": self.split_map_sha256,
            "labeling_guide_sha256": self.labeling_guide_sha256,
        }

    _KEYS = frozenset(
        {
            "status",
            "approved_by",
            "approval_statement",
            "approval_date",
            "dataset_id",
            "dataset_version",
            "dataset_sha256",
            "split_map_sha256",
            "labeling_guide_sha256",
        }
    )

    @classmethod
    def from_dict(cls, payload: Mapping[str, Any]) -> "OwnerLabelApproval":
        unknown = set(payload) - cls._KEYS
        _require(not unknown,
                 f"OwnerLabelApproval: unknown keys {sorted(unknown)}")
        missing = cls._KEYS - set(payload)
        _require(not missing,
                 f"OwnerLabelApproval: missing keys {sorted(missing)}")
        approval = cls(
            status=OwnerApprovalStatus.parse(payload.get("status")),
            approved_by=payload.get("approved_by", ""),
            approval_statement=payload.get("approval_statement", ""),
            approval_date=payload.get("approval_date", ""),
            dataset_id=payload.get("dataset_id", ""),
            dataset_version=payload.get("dataset_version", ""),
            dataset_sha256=payload.get("dataset_sha256", ""),
            split_map_sha256=payload.get("split_map_sha256", ""),
            labeling_guide_sha256=payload.get("labeling_guide_sha256", ""),
        )
        approval.validate()
        return approval


# ----------------------------------------------- dispatch authorization
_AUTHORIZATION_KEY = object()


class CalibrationDispatchAuthorization:
    """Proof that the gates passed. Constructible ONLY by
    ``authorize_calibration_dispatch`` — direct construction fails.

    ``authorized_request_ids`` is the CLOSED set of judgment request ids
    this authorization may dispatch, derived by the gate itself from the
    hash-bound dataset (DEVELOPMENT items only) — a sealed-holdout request
    id is never a member, so the provider refuses it mechanically."""

    __slots__ = (
        "stage",
        "dataset_sha256",
        "approval_statement",
        "authorized_request_ids",
    )

    def __init__(
        self,
        *,
        stage: ExecutionStage,
        dataset_sha256: str,
        approval_statement: str,
        authorized_request_ids: frozenset[str] = frozenset(),
        _key: object | None = None,
    ) -> None:
        if _key is not _AUTHORIZATION_KEY:
            raise CalibrationAuthorizationError(
                "CalibrationDispatchAuthorization is issued only by "
                "authorize_calibration_dispatch after the owner-approval "
                "gate passes; direct construction is refused"
            )
        self.stage = stage
        self.dataset_sha256 = dataset_sha256
        self.approval_statement = approval_statement
        self.authorized_request_ids = frozenset(authorized_request_ids)


def authorize_calibration_dispatch(
    *,
    approval: OwnerLabelApproval | None,
    dataset_identity: DatasetIdentity,
    dataset: Any,
    stage: ExecutionStage,
) -> CalibrationDispatchAuthorization:
    """The Stage-A1 hard gate: PENDING (or absent) owner approval blocks
    every provider judgment call; the sealed holdout is never unlocked here.

    The hash-bound ``dataset`` object is REQUIRED so the gate itself derives
    the authorized (development-only) request-id set — callers cannot supply
    their own item list."""
    dataset_identity.validate()
    if not isinstance(stage, ExecutionStage):
        raise SchemaValidationError("stage must be ExecutionStage")
    if approval is None or not isinstance(approval, OwnerLabelApproval):
        raise CalibrationStopError(
            CalibrationStopReason.OWNER_APPROVAL_PENDING,
            "no owner label-approval artifact exists; provider execution is "
            "mechanically blocked while OWNER_LABEL_APPROVAL is PENDING",
        )
    approval.validate()
    if approval.status is not OwnerApprovalStatus.APPROVED:
        raise CalibrationStopError(
            CalibrationStopReason.OWNER_APPROVAL_PENDING,
            "OWNER_LABEL_APPROVAL is PENDING; Claude cannot self-certify "
            "labels as human-approved — explicit owner approval is required "
            "before any provider judgment call",
        )
    if (
        approval.dataset_id != dataset_identity.dataset_id
        or approval.dataset_version != dataset_identity.dataset_version
        or approval.dataset_sha256 != dataset_identity.dataset_sha256
        or approval.split_map_sha256 != dataset_identity.split_map_sha256
        or approval.labeling_guide_sha256
        != dataset_identity.labeling_guide_sha256
    ):
        raise CalibrationStopError(
            CalibrationStopReason.DATASET_INTEGRITY_MISMATCH,
            "the owner approval does not hash-bind THIS dataset/split/"
            "labeling-guide version; a changed artifact requires a new "
            "owner approval",
        )
    if stage is ExecutionStage.OWNER_WAIT:
        raise CalibrationStopError(
            CalibrationStopReason.UNAUTHORIZED_EXECUTION_STAGE,
            "OWNER_WAIT permits no provider execution (BER-DEC-008 "
            "decision 19)",
        )
    if stage is ExecutionStage.SEALED_HOLDOUT:
        raise CalibrationStopError(
            CalibrationStopReason.HOLDOUT_NOT_FROZEN,
            "sealed-holdout execution requires the owner freeze state "
            "(decision 35); this gate can authorize DEVELOPMENT only",
        )
    from .calibration_dataset import (  # local: no import cycle
        CandidateDataset,
        CandidateSplit,
        calibration_request_id,
        split_map_sha256,
    )

    if not isinstance(dataset, CandidateDataset):
        raise SchemaValidationError(
            "authorize_calibration_dispatch requires the hash-bound "
            "CandidateDataset object to derive the authorized item set"
        )
    if (
        dataset.dataset_sha256() != dataset_identity.dataset_sha256
        or split_map_sha256(dataset) != dataset_identity.split_map_sha256
    ):
        raise CalibrationStopError(
            CalibrationStopReason.DATASET_INTEGRITY_MISMATCH,
            "the supplied dataset object does not hash-match the approved "
            "dataset identity; no authorization is issued",
        )
    authorized_request_ids = frozenset(
        calibration_request_id(item.item_id)
        for item in dataset.items
        if item.split is CandidateSplit.DEVELOPMENT
    )
    return CalibrationDispatchAuthorization(
        stage=stage,
        dataset_sha256=dataset_identity.dataset_sha256,
        approval_statement=approval.approval_statement,
        authorized_request_ids=authorized_request_ids,
        _key=_AUTHORIZATION_KEY,
    )


# ----------------------------------------------------- holdout freeze gate
#: Decision-35 artifacts that must be frozen AND hashed before unsealing.
FREEZE_HASH_FIELDS = (
    "model_snapshot",
    "endpoint",
    "sdk_transport_version",
    "system_policy",
    "rubric_contracts",
    "verdict_schema",
    "dataset",
    "split_map",
    "labels",
    "thresholds",
    "retry_policy",
    "call_token_dollar_caps",
    "retention_settings",
)


@dataclass(frozen=True, slots=True)
class HoldoutFreezeArtifact:
    """The owner freeze record required before the ONE-PASS holdout."""

    owner_freeze_statement: str
    frozen_date: str
    holdout_max_output_tokens: int
    reasoning_effort: str
    frozen_sha256: Mapping[str, str]

    def validate(self) -> None:
        _require(
            isinstance(self.owner_freeze_statement, str)
            and bool(self.owner_freeze_statement.strip()),
            "owner_freeze_statement required (an explicit owner decision)",
        )
        _require(
            isinstance(self.frozen_date, str) and bool(self.frozen_date),
            "frozen_date required",
        )
        low, high = HOLDOUT_MAX_OUTPUT_TOKENS_RANGE
        _require(
            isinstance(self.holdout_max_output_tokens, int)
            and not isinstance(self.holdout_max_output_tokens, bool)
            and low <= self.holdout_max_output_tokens <= high,
            f"holdout_max_output_tokens must be within [{low}, {high}] "
            "(BER-DEC-008 decision 19)",
        )
        _require(
            self.reasoning_effort == REASONING_EFFORT,
            f"reasoning_effort must be {REASONING_EFFORT!r}",
        )
        _require(
            isinstance(self.frozen_sha256, Mapping),
            "frozen_sha256 must be a mapping",
        )
        missing = set(FREEZE_HASH_FIELDS) - set(self.frozen_sha256)
        _require(
            not missing,
            f"freeze artifact missing decision-35 hashes: {sorted(missing)}",
        )
        unknown = set(self.frozen_sha256) - set(FREEZE_HASH_FIELDS)
        _require(
            not unknown,
            f"freeze artifact carries unknown hash fields: {sorted(unknown)}",
        )
        for name in FREEZE_HASH_FIELDS:
            _require_sha256(self.frozen_sha256[name], f"frozen_sha256.{name}")

    _KEYS = frozenset(
        {
            "owner_freeze_statement",
            "frozen_date",
            "holdout_max_output_tokens",
            "reasoning_effort",
            "frozen_sha256",
        }
    )

    @classmethod
    def from_dict(cls, payload: Mapping[str, Any]) -> "HoldoutFreezeArtifact":
        unknown = set(payload) - cls._KEYS
        _require(not unknown,
                 f"HoldoutFreezeArtifact: unknown keys {sorted(unknown)}")
        missing = cls._KEYS - set(payload)
        _require(not missing,
                 f"HoldoutFreezeArtifact: missing keys {sorted(missing)}")
        artifact = cls(
            owner_freeze_statement=payload.get("owner_freeze_statement", ""),
            frozen_date=payload.get("frozen_date", ""),
            holdout_max_output_tokens=payload.get(
                "holdout_max_output_tokens", 0
            ),
            reasoning_effort=payload.get("reasoning_effort", ""),
            frozen_sha256=dict(payload.get("frozen_sha256", {})),
        )
        artifact.validate()
        return artifact

    @classmethod
    def example_dict(cls) -> dict[str, Any]:
        """A syntactically valid EXAMPLE for tests and documentation only —
        it is NOT an owner decision and never exists as evidence."""
        return {
            "owner_freeze_statement": (
                "EXAMPLE ONLY — NOT AN OWNER DECISION; a real freeze is "
                "written by Peter Nguyen after development characterization"
            ),
            "frozen_date": "EXAMPLE",
            "holdout_max_output_tokens": 16384,
            "reasoning_effort": REASONING_EFFORT,
            "frozen_sha256": {name: "0" * 64 for name in FREEZE_HASH_FIELDS},
        }


class HoldoutFreezeAuthorization:
    """Proof the holdout freeze gate passed; issued only by
    ``authorize_holdout_access``."""

    __slots__ = ("artifact",)

    def __init__(
        self,
        *,
        artifact: HoldoutFreezeArtifact,
        _key: object | None = None,
    ) -> None:
        if _key is not _AUTHORIZATION_KEY:
            raise CalibrationAuthorizationError(
                "HoldoutFreezeAuthorization is issued only by "
                "authorize_holdout_access"
            )
        self.artifact = artifact


def authorize_holdout_access(
    *, freeze_artifact: HoldoutFreezeArtifact | None
) -> HoldoutFreezeAuthorization:
    """Sealed-holdout access exists ONLY behind a valid owner freeze."""
    if freeze_artifact is None or not isinstance(
        freeze_artifact, HoldoutFreezeArtifact
    ):
        raise HoldoutAccessError(
            "no owner freeze artifact: the sealed holdout stays sealed "
            "(BER-DEC-008 decisions 19, 35)"
        )
    freeze_artifact.validate()
    return HoldoutFreezeAuthorization(
        artifact=freeze_artifact, _key=_AUTHORIZATION_KEY
    )
