"""WP-2B-3 candidate calibration-dataset contract (BER-DEC-008 decisions
5-10, 34-35; task sections 14, 16, 17).

CANDIDATE means NOT HUMAN-APPROVED: every label in this contract is a
``candidate_expected_label`` proposed by the implementation session, carried
with ``owner_label_status = PENDING`` until Peter Nguyen's explicit
approval. Nothing here may be described as a human label, and the assembled
160-item dataset itself lives ONLY under the external evidence root — the
repository carries this contract, its validators, and hashes.

The label-leak boundary is structural: the ONLY judge-facing projection of
an item is ``CalibrationItemContent`` (item id, control id, transcript), a
shape on which expected labels are unrepresentable.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping

from .. import CALIBRATION_SCHEMA_VERSION
from ..canonical import sha256_hex_text, sha256_of_obj
from ..enums import RiskClass, StrictEnum
from ..errors import SchemaValidationError
from .calibration_errors import HoldoutAccessError, LabelLeakError

#: The ten semantic-bearing Scenario A controls (BER-DEC-008 decision 6),
#: cross-checked against the grading contract by tests.
SEMANTIC_BEARING_CONTROL_IDS: tuple[str, ...] = tuple(
    f"SCENARIO_A_CONTROL_{letter}" for letter in "ABCDGHIJNO"
)

#: Candidate provenance: explicitly NOT a human-approved dataset.
CANDIDATE_PROVENANCE = "SYNTHETIC_CANDIDATE_NOT_HUMAN_APPROVED"

_ITEM_ID_MAX = 64
_HEX = set("0123456789abcdef")


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise SchemaValidationError(message)


class CandidateSplit(StrictEnum):
    DEVELOPMENT = "DEVELOPMENT"
    SEALED_HOLDOUT = "SEALED_HOLDOUT"


class CandidateLabel(StrictEnum):
    """Candidate expected labels are PASS/FAIL only (60/60 and 2/2 balances);
    ABSTAIN is an observed judge outcome, never an expected label."""

    PASS = "PASS"
    FAIL = "FAIL"


class OwnerLabelStatus(StrictEnum):
    PENDING = "PENDING"
    APPROVED = "APPROVED"


class AdversarialKind(StrictEnum):
    PROMPT_INJECTION = "PROMPT_INJECTION"
    ROLE_CONFUSION = "ROLE_CONFUSION"


@dataclass(frozen=True, slots=True)
class CandidateItem:
    item_id: str
    control_id: str
    split: CandidateSplit
    risk_class: RiskClass
    adversarial: bool
    adversarial_kind: AdversarialKind | None
    candidate_expected_label: CandidateLabel
    candidate_rationale: str
    owner_label_status: OwnerLabelStatus
    transcript: str

    def validate(self) -> None:
        _require(
            isinstance(self.item_id, str)
            and 0 < len(self.item_id) <= _ITEM_ID_MAX
            and all(c.isalnum() or c in "._-" for c in self.item_id),
            f"item_id must be a bounded identifier, got {self.item_id!r}",
        )
        _require(
            self.control_id in SEMANTIC_BEARING_CONTROL_IDS,
            f"control_id must be one of the ten semantic-bearing controls, "
            f"got {self.control_id!r}",
        )
        _require(isinstance(self.split, CandidateSplit), "split enum required")
        _require(isinstance(self.risk_class, RiskClass),
                 "risk_class enum required")
        _require(isinstance(self.adversarial, bool), "adversarial must be bool")
        if self.adversarial:
            _require(
                isinstance(self.adversarial_kind, AdversarialKind),
                f"{self.item_id}: adversarial items require an "
                "adversarial_kind (PROMPT_INJECTION or ROLE_CONFUSION)",
            )
        else:
            _require(
                self.adversarial_kind is None,
                f"{self.item_id}: non-adversarial items carry no "
                "adversarial_kind",
            )
        _require(
            isinstance(self.candidate_expected_label, CandidateLabel),
            "candidate_expected_label enum required",
        )
        _require(
            isinstance(self.candidate_rationale, str)
            and bool(self.candidate_rationale.strip()),
            f"{self.item_id}: every candidate label carries a concise "
            "rationale",
        )
        _require(
            isinstance(self.owner_label_status, OwnerLabelStatus),
            "owner_label_status enum required",
        )
        _require(
            isinstance(self.transcript, str) and bool(self.transcript.strip()),
            f"{self.item_id}: transcript must be non-empty synthetic content",
        )

    def transcript_sha256(self) -> str:
        return sha256_hex_text(self.transcript)

    def to_dict(self) -> dict[str, Any]:
        return {
            "item_id": self.item_id,
            "control_id": self.control_id,
            "split": self.split.value,
            "risk_class": self.risk_class.value,
            "adversarial": self.adversarial,
            "adversarial_kind": (
                self.adversarial_kind.value if self.adversarial_kind else None
            ),
            "candidate_expected_label": self.candidate_expected_label.value,
            "candidate_rationale": self.candidate_rationale,
            "owner_label_status": self.owner_label_status.value,
            "transcript": self.transcript,
        }

    _KEYS = frozenset(
        {
            "item_id",
            "control_id",
            "split",
            "risk_class",
            "adversarial",
            "adversarial_kind",
            "candidate_expected_label",
            "candidate_rationale",
            "owner_label_status",
            "transcript",
        }
    )

    @classmethod
    def from_dict(cls, payload: Mapping[str, Any]) -> "CandidateItem":
        unknown = set(payload) - cls._KEYS
        _require(not unknown, f"CandidateItem: unknown keys {sorted(unknown)}")
        missing = cls._KEYS - set(payload)
        _require(not missing, f"CandidateItem: missing keys {sorted(missing)}")
        kind = payload.get("adversarial_kind")
        item = cls(
            item_id=payload.get("item_id", ""),
            control_id=payload.get("control_id", ""),
            split=CandidateSplit.parse(payload.get("split")),
            risk_class=RiskClass.parse(payload.get("risk_class")),
            adversarial=bool(payload.get("adversarial")),
            adversarial_kind=(
                AdversarialKind.parse(kind) if kind is not None else None
            ),
            candidate_expected_label=CandidateLabel.parse(
                payload.get("candidate_expected_label")
            ),
            candidate_rationale=payload.get("candidate_rationale", ""),
            owner_label_status=OwnerLabelStatus.parse(
                payload.get("owner_label_status")
            ),
            transcript=payload.get("transcript", ""),
        )
        item.validate()
        return item


@dataclass(frozen=True, slots=True)
class CandidateDataset:
    dataset_id: str
    version: str
    labeler_role: str
    provenance: str
    owner_label_status: OwnerLabelStatus
    items: tuple[CandidateItem, ...]
    schema_version: str = CALIBRATION_SCHEMA_VERSION

    def validate(self) -> None:
        for name in ("dataset_id", "version", "labeler_role"):
            value = getattr(self, name)
            _require(
                isinstance(value, str) and bool(value), f"{name} required"
            )
        _require(
            self.provenance == CANDIDATE_PROVENANCE,
            f"provenance must be {CANDIDATE_PROVENANCE!r}: candidate labels "
            "are never human labels",
        )
        _require(
            isinstance(self.owner_label_status, OwnerLabelStatus),
            "owner_label_status enum required",
        )
        _require(
            isinstance(self.items, tuple) and len(self.items) > 0,
            "items must be non-empty",
        )
        _require(
            self.schema_version == CALIBRATION_SCHEMA_VERSION,
            f"schema_version must be {CALIBRATION_SCHEMA_VERSION}",
        )
        seen_ids: set[str] = set()
        seen_transcripts: set[str] = set()
        for item in self.items:
            item.validate()
            _require(
                item.item_id not in seen_ids,
                f"duplicate item_id {item.item_id!r}",
            )
            seen_ids.add(item.item_id)
            digest = item.transcript_sha256()
            _require(
                digest not in seen_transcripts,
                f"{item.item_id}: transcript duplicates another item — the "
                "dataset must contain DISTINCT items",
            )
            seen_transcripts.add(digest)
            _require(
                item.owner_label_status is self.owner_label_status,
                f"{item.item_id}: item owner_label_status must match the "
                "dataset-level status",
            )

    def dataset_sha256(self) -> str:
        return sha256_of_obj(self.to_dict())

    def to_dict(self) -> dict[str, Any]:
        return {
            "dataset_id": self.dataset_id,
            "version": self.version,
            "labeler_role": self.labeler_role,
            "provenance": self.provenance,
            "owner_label_status": self.owner_label_status.value,
            "items": [item.to_dict() for item in self.items],
            "schema_version": self.schema_version,
        }

    _KEYS = frozenset(
        {
            "dataset_id",
            "version",
            "labeler_role",
            "provenance",
            "owner_label_status",
            "items",
            "schema_version",
        }
    )

    @classmethod
    def from_dict(cls, payload: Mapping[str, Any]) -> "CandidateDataset":
        unknown = set(payload) - cls._KEYS
        _require(not unknown, f"CandidateDataset: unknown keys {sorted(unknown)}")
        _require(
            "schema_version" in payload,
            "CandidateDataset requires an explicit schema_version",
        )
        _require(
            isinstance(payload.get("items", []), list),
            "items must be a JSON list",
        )
        dataset = cls(
            dataset_id=payload.get("dataset_id", ""),
            version=payload.get("version", ""),
            labeler_role=payload.get("labeler_role", ""),
            provenance=payload.get("provenance", ""),
            owner_label_status=OwnerLabelStatus.parse(
                payload.get("owner_label_status")
            ),
            items=tuple(
                CandidateItem.from_dict(item)
                for item in payload.get("items", ())
            ),
            schema_version=payload.get("schema_version", ""),
        )
        dataset.validate()
        return dataset


# ------------------------------------------------- authorized composition
_PER_CONTROL_TOTAL = 16
_PER_CONTROL_DEV_PASS = 2
_PER_CONTROL_DEV_FAIL = 2
_PER_CONTROL_HOLDOUT_PASS = 6
_PER_CONTROL_HOLDOUT_FAIL = 6
_TOTAL_ITEMS = 160
_DEV_TOTAL = 40
_HOLDOUT_TOTAL = 120
_MIN_CRITICAL_EXPECTED_FAIL = 40
_MIN_ADVERSARIAL = 40
_MIN_ADVERSARIAL_PASS = 20
_MIN_ADVERSARIAL_FAIL = 20


def validate_authorized_composition(dataset: CandidateDataset) -> dict[str, Any]:
    """Enforce the EXACT BER-DEC-008 dataset composition; return the
    distribution report (with the CRITICAL/adversarial overlap reported
    separately and no double-counting of the 120 distinct holdout items)."""
    dataset.validate()
    items = dataset.items
    _require(
        len(items) == _TOTAL_ITEMS,
        f"dataset must contain exactly {_TOTAL_ITEMS} distinct items, "
        f"got {len(items)}",
    )
    per_control: dict[str, dict[str, int]] = {}
    for control in SEMANTIC_BEARING_CONTROL_IDS:
        control_items = [i for i in items if i.control_id == control]
        dev = [i for i in control_items
               if i.split is CandidateSplit.DEVELOPMENT]
        holdout = [i for i in control_items
                   if i.split is CandidateSplit.SEALED_HOLDOUT]
        counts = {
            "total": len(control_items),
            "development_pass": sum(
                1 for i in dev
                if i.candidate_expected_label is CandidateLabel.PASS
            ),
            "development_fail": sum(
                1 for i in dev
                if i.candidate_expected_label is CandidateLabel.FAIL
            ),
            "holdout_pass": sum(
                1 for i in holdout
                if i.candidate_expected_label is CandidateLabel.PASS
            ),
            "holdout_fail": sum(
                1 for i in holdout
                if i.candidate_expected_label is CandidateLabel.FAIL
            ),
        }
        per_control[control] = counts
        _require(
            counts["total"] == _PER_CONTROL_TOTAL
            and counts["development_pass"] == _PER_CONTROL_DEV_PASS
            and counts["development_fail"] == _PER_CONTROL_DEV_FAIL
            and counts["holdout_pass"] == _PER_CONTROL_HOLDOUT_PASS
            and counts["holdout_fail"] == _PER_CONTROL_HOLDOUT_FAIL,
            f"{control}: per-control composition must be exactly "
            f"{_PER_CONTROL_TOTAL} items (dev {_PER_CONTROL_DEV_PASS}P/"
            f"{_PER_CONTROL_DEV_FAIL}F; holdout {_PER_CONTROL_HOLDOUT_PASS}P/"
            f"{_PER_CONTROL_HOLDOUT_FAIL}F), got {counts}",
        )

    development = [i for i in items if i.split is CandidateSplit.DEVELOPMENT]
    holdout = [i for i in items if i.split is CandidateSplit.SEALED_HOLDOUT]
    _require(len(development) == _DEV_TOTAL, "development split must be 40")
    _require(len(holdout) == _HOLDOUT_TOTAL, "sealed holdout must be 120")

    holdout_pass = [i for i in holdout
                    if i.candidate_expected_label is CandidateLabel.PASS]
    holdout_fail = [i for i in holdout
                    if i.candidate_expected_label is CandidateLabel.FAIL]
    critical_fail = [i for i in holdout_fail
                     if i.risk_class is RiskClass.CRITICAL]
    adversarial = [i for i in holdout if i.adversarial]
    adversarial_pass = [
        i for i in adversarial
        if i.candidate_expected_label is CandidateLabel.PASS
    ]
    adversarial_fail = [
        i for i in adversarial
        if i.candidate_expected_label is CandidateLabel.FAIL
    ]
    overlap = [i for i in adversarial_fail
               if i.risk_class is RiskClass.CRITICAL]
    _require(
        len(critical_fail) >= _MIN_CRITICAL_EXPECTED_FAIL,
        f"at least {_MIN_CRITICAL_EXPECTED_FAIL} holdout items must carry "
        f"risk_class=CRITICAL with candidate_expected_label=FAIL, got "
        f"{len(critical_fail)}",
    )
    _require(
        len(adversarial) >= _MIN_ADVERSARIAL
        and len(adversarial_pass) >= _MIN_ADVERSARIAL_PASS
        and len(adversarial_fail) >= _MIN_ADVERSARIAL_FAIL,
        "the sealed holdout must contain at least "
        f"{_MIN_ADVERSARIAL} injection/role-confusion items "
        f"(>= {_MIN_ADVERSARIAL_PASS} candidate PASS and >= "
        f"{_MIN_ADVERSARIAL_FAIL} candidate FAIL); got "
        f"{len(adversarial)} ({len(adversarial_pass)}P/"
        f"{len(adversarial_fail)}F)",
    )
    by_kind: dict[str, int] = {kind.value: 0 for kind in AdversarialKind}
    for item in adversarial:
        assert item.adversarial_kind is not None
        by_kind[item.adversarial_kind.value] += 1
    return {
        "total_items": len(items),
        "development_total": len(development),
        "holdout_total": len(holdout),
        "holdout_expected_pass": len(holdout_pass),
        "holdout_expected_fail": len(holdout_fail),
        "holdout_critical_expected_fail": len(critical_fail),
        "holdout_adversarial_total": len(adversarial),
        "holdout_adversarial_expected_pass": len(adversarial_pass),
        "holdout_adversarial_expected_fail": len(adversarial_fail),
        "holdout_adversarial_by_kind": by_kind,
        "critical_adversarial_overlap": len(overlap),
        "per_control": per_control,
    }


def require_stage_a1_pending(dataset: CandidateDataset) -> None:
    """Stage A1: candidate labels are explicitly NOT human-approved."""
    _require(
        dataset.owner_label_status is OwnerLabelStatus.PENDING,
        "Stage A1 requires owner_label_status=PENDING — Claude/AI-generated "
        "labels are candidates, never human approvals",
    )


# ------------------------------------------------------ split map / access
def split_map(dataset: CandidateDataset) -> dict[str, str]:
    return {item.item_id: item.split.value for item in dataset.items}


def split_map_sha256(dataset: CandidateDataset) -> str:
    return sha256_of_obj(split_map(dataset))


#: Opaque request-id namespace (audit family A): judge-visible request ids
#: carry NO raw item id, split marker, PASS/FAIL marker, control position,
#: label, or rationale — item ids like ``A-dev-p1`` would otherwise leak
#: the gold label through their ``-p``/``-f`` suffix.
OPAQUE_REQUEST_ID_PREFIX = "wp2b3-r-"
_OPAQUE_REQUEST_ID_HEX_CHARS = 32


def calibration_request_id(item_id: str, dataset_sha256: str) -> str:
    """The canonical LABEL-OPAQUE judgment request id for one item (single
    derivation shared by the envelope builder, the authorization gate, and
    the development driver).

    Deterministic and collision-free across the approved dataset: the id is
    a truncated SHA-256 over the dataset's semantic identity plus the item
    id, so accounting and owner summaries can re-derive the mapping while
    nothing judge-visible encodes the item, its split, or its label."""
    _require(
        isinstance(item_id, str) and bool(item_id), "item_id required"
    )
    _require(
        isinstance(dataset_sha256, str)
        and len(dataset_sha256) == 64
        and set(dataset_sha256) <= _HEX,
        "dataset_sha256 must be a 64-hex semantic dataset identity",
    )
    digest = sha256_hex_text(f"{dataset_sha256}:{item_id}")
    return OPAQUE_REQUEST_ID_PREFIX + digest[:_OPAQUE_REQUEST_ID_HEX_CHARS]


def development_items(dataset: CandidateDataset) -> tuple[CandidateItem, ...]:
    """The ONLY split reachable without the owner freeze state."""
    return tuple(
        item for item in dataset.items
        if item.split is CandidateSplit.DEVELOPMENT
    )


def holdout_items(dataset: CandidateDataset, freeze: Any) -> tuple[CandidateItem, ...]:
    """Sealed-holdout access requires the owner freeze authorization
    (BER-DEC-008 decisions 19, 35); anything else fails closed."""
    from .calibration_gates import HoldoutFreezeAuthorization  # local: no cycle

    if not isinstance(freeze, HoldoutFreezeAuthorization):
        raise HoldoutAccessError(
            "sealed-holdout items are inaccessible without the owner "
            "freeze authorization; development execution cannot iterate "
            "the holdout"
        )
    return tuple(
        item for item in dataset.items
        if item.split is CandidateSplit.SEALED_HOLDOUT
    )


# -------------------------------------------------- judge-facing projection
#: Keys that may NEVER reach the judge-facing content surface.
FORBIDDEN_CONTENT_KEYS = frozenset(
    {
        "candidate_expected_label",
        "expected_label",
        "proposed_gold_label",
        "gold_label",
        "label",
        "labels",
        "owner_label_status",
        "candidate_rationale",
        "rationale",
        "risk_class",
        "split",
        "adversarial",
        "adversarial_kind",
    }
)

_CONTENT_KEYS = frozenset({"item_id", "control_id", "transcript"})


@dataclass(frozen=True, slots=True)
class CalibrationItemContent:
    """The judge-facing projection of one item: labels are UNREPRESENTABLE
    on this shape, so the envelope builder is structurally label-free."""

    item_id: str
    control_id: str
    transcript: str

    def validate(self) -> None:
        _require(
            isinstance(self.item_id, str) and bool(self.item_id),
            "item_id required",
        )
        _require(
            self.control_id in SEMANTIC_BEARING_CONTROL_IDS,
            f"control_id must be semantic-bearing, got {self.control_id!r}",
        )
        _require(
            isinstance(self.transcript, str) and bool(self.transcript.strip()),
            "transcript required",
        )

    def to_dict(self) -> dict[str, str]:
        return {
            "item_id": self.item_id,
            "control_id": self.control_id,
            "transcript": self.transcript,
        }

    @classmethod
    def from_item(
        cls,
        item: CandidateItem,
        *,
        holdout_authorization: Any = None,
    ) -> "CalibrationItemContent":
        """Project one item onto the judge-facing shape.

        SEALED_HOLDOUT items are refused unless a gate-issued
        ``HoldoutFreezeAuthorization`` is presented — iterating
        ``dataset.items`` can never yield a dispatchable holdout content
        without the owner freeze (BER-DEC-008 decisions 19, 35).
        """
        item.validate()
        if item.split is CandidateSplit.SEALED_HOLDOUT:
            from .calibration_gates import (  # local: no import cycle
                HoldoutFreezeAuthorization,
            )

            if not isinstance(holdout_authorization, HoldoutFreezeAuthorization):
                raise HoldoutAccessError(
                    f"{item.item_id} is a SEALED_HOLDOUT item: its "
                    "judge-facing projection requires the owner freeze "
                    "authorization; the sealed holdout stays sealed"
                )
        content = cls(
            item_id=item.item_id,
            control_id=item.control_id,
            transcript=item.transcript,
        )
        content.validate()
        return content

    @classmethod
    def from_mapping(cls, payload: Mapping[str, Any]) -> "CalibrationItemContent":
        keys = set(payload)
        leaked = keys & FORBIDDEN_CONTENT_KEYS
        if leaked:
            raise LabelLeakError(
                f"label-bearing keys {sorted(leaked)} may never reach the "
                "judge-facing content surface"
            )
        unknown = keys - _CONTENT_KEYS
        if unknown:
            raise LabelLeakError(
                f"unknown keys {sorted(unknown)} rejected: the judge-facing "
                f"content surface is closed to {sorted(_CONTENT_KEYS)}"
            )
        missing = _CONTENT_KEYS - keys
        _require(not missing, f"content missing keys {sorted(missing)}")
        content = cls(
            item_id=payload["item_id"],
            control_id=payload["control_id"],
            transcript=payload["transcript"],
        )
        content.validate()
        return content
