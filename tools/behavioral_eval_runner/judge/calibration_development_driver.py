"""WP-2B-3 Stage A2 dedicated DEVELOPMENT execution driver (BER-DEC-008).

This module is the ONLY WP-2B-3 execution driver, and it is deliberately
narrow: WP-2B-3, BER-DEC-008, the DEVELOPMENT stage, the owner-approved
candidate dataset ``1.0.0-wp2b3-candidate.2``, and the pinned judge
snapshot only. It is NOT a general Scenario A, generic-corpus, holdout, or
production dispatch surface, and it is intentionally NOT wired into the
generic Behavioral Eval Runner CLI (which continues to expose no live
model/provider-dispatch command).

Controls this driver adds on top of the Stage A1 machinery it composes:

- ONE canonical ledger path and ONE canonical run-manifest path, derived
  exclusively from the marker-verified evidence root — no caller-selected
  ledger path exists anywhere on this surface (task section 8);
- GENESIS exactly once: creating the fresh work-package accounting history
  requires the explicit first-segment declaration AND is refused whenever
  the canonical ledger or manifest already exists; later sessions REOPEN
  the same file and must re-prove every manifest binding (head/tree,
  approval hash, dataset hashes, model, SDK, caps) before resuming;
- a persistent, durably verified DEVELOPMENT active segment is mandatory
  before ANY external interaction (metadata or judgment), and the
  90-minute development / 6-hour whole-run deadlines therefore govern
  every attempt including the single runner-owned retry (task section 9);
- deterministic development-only execution: exactly the 40 approved
  DEVELOPMENT items in sorted item-id order; sealed-holdout items are
  structurally unreachable (never projected, never authorized);
- restart safety without retry-until-green: items with a durable terminal
  semantic outcome are never dispatched again; an orphaned STARTED attempt
  or an open (crashed) active segment blocks resume pending owner review;
- process-scoped consume-once credential handling; the credential value
  can never reach the ledger, the manifest, or any summary.

Stage A2 preflight runs everything here with fakes only: ZERO provider,
model, or metadata calls; ZERO credential access; the REAL canonical
ledger is NOT created by this preflight.
"""

from __future__ import annotations

import argparse
import json
import math
import os
import stat as stat_module
import statistics
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Callable, Mapping, MutableMapping

from .. import (
    WP2B3_AUTHORIZATION_ID,
    WP2B3_AUTHORIZATION_MERGE_SHA,
    WP2B3_AUTHORIZATION_TREE_SHA,
    WP2B3_WORK_PACKAGE,
)
from ..canonical import canonical_bytes, sha256_hex
from ..errors import SchemaValidationError
from .calibration_credential import (
    CalibrationCredential,
    consume_process_scoped_credential,
)
from .calibration_dataset import (
    CalibrationItemContent,
    CandidateDataset,
    CandidateItem,
    CandidateLabel,
    calibration_request_id,
    development_items,
    split_map_sha256,
    validate_authorized_composition,
)
from .calibration_envelope import (
    build_calibration_envelope,
    build_calibration_judge_request,
)
from .calibration_errors import (
    CalibrationAuthorizationError,
    CalibrationLedgerError,
    CalibrationStopError,
    CalibrationStopReason,
)
from .calibration_gates import (
    CalibrationDispatchAuthorization,
    DatasetIdentity,
    ExecutionStage,
    OwnerLabelApproval,
    authorize_calibration_dispatch,
)
from .calibration_ledger import (
    DEV_STAGE_DEADLINE_SECONDS,
    MAX_JUDGMENT_ATTEMPTS,
    MAX_METADATA_REQUESTS,
    MAX_SINGLE_DAY_SPEND_NANOUSD,
    MAX_TOTAL_EXTERNAL_REQUESTS,
    MAX_TOTAL_SPEND_NANOUSD,
    RUN_STATE_OWNER_WAIT,
    RUN_STATE_PAUSED,
    RUN_STATE_STOPPED,
    TOTAL_RUN_DEADLINE_SECONDS,
    CalibrationLedger,
    RequestKind,
)
from .calibration_provider import (
    OpenAICalibrationJudgeClient,
    TransportExceptionTypes,
    dispatch_calibration_judgment,
)
from .calibration_transport import (
    AUTHORIZED_MODEL_SNAPSHOT,
    AUTHORIZED_SDK_VERSION,
    DEV_MAX_OUTPUT_TOKENS,
    MAX_INPUT_TOKENS_PER_JUDGMENT,
    build_judge_client,
    verify_sdk_available,
    verify_sdk_version,
)

# ------------------------------------------------------- authorized surface
#: BER-DEC-008 decision 24: the ONE authorized external evidence root.
AUTHORIZED_EVIDENCE_ROOT = (
    r"C:\temp\Project-Aegis-BER-WP-2B-3-Measured-Judge-Calibration-Evidence"
)
IMPLEMENTATION_BRANCH = (
    "feat/behavioral-eval-runner-2b-3-measured-judge-calibration"
)
IMPLEMENTATION_PULL_REQUEST = 88

#: The ONE canonical ledger and run manifest (task section 8). These names
#: are constants of the driver — no API accepts a caller-selected path.
CANONICAL_LEDGER_RELPATH = "runs/wp2b3-development-ledger-v1.jsonl"
CANONICAL_MANIFEST_RELPATH = "runs/wp2b3-development-run-manifest-v1.json"
DEVELOPMENT_RESULT_SUMMARY_RELPATH = (
    "runs/wp2b3-development-result-summary-v1.json"
)

MARKER_RELPATH = "ownership-marker.json"
APPROVAL_ARTIFACT_RELPATH = "approvals/wp2b3-owner-label-approval-v2.json"
DATASET_RELPATH = "dataset/wp2b3-candidate-dataset-v2.json"
LABELING_GUIDE_RELPATH = "dataset/wp2b3-labeling-guide-v2-copy.md"
OWNER_BUNDLE_RELPATH = "wp2b3-owner-label-review-bundle-v2.zip"

EXPECTED_DEVELOPMENT_ITEMS = 40
EXPECTED_DEVELOPMENT_PASS = 20
EXPECTED_DEVELOPMENT_FAIL = 20

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


def _require_sha1_hex(value: Any, where: str) -> str:
    _require(
        isinstance(value, str) and len(value) == 40 and set(value) <= _HEX,
        f"{where} must be a 40-hex Git object id",
    )
    return value


def _sha256_file(path: str) -> str:
    with open(path, "rb") as handle:
        return sha256_hex(handle.read())


def _utc_day() -> str:
    return datetime.now(timezone.utc).date().isoformat()


def _recorded_sdk_version() -> str:
    available, version = verify_sdk_available()
    if available and version:
        return version
    return f"pinned-{AUTHORIZED_SDK_VERSION}-not-imported-offline"


@dataclass(frozen=True, slots=True)
class ApprovedArtifactIdentity:
    """The owner-approved artifact identity the driver enforces.

    ``PRODUCTION_APPROVED_ARTIFACTS`` (the BER-DEC-008 / owner-approval
    values) is the only identity the live surface ever uses; offline tests
    substitute a synthetic identity for their synthetic roots.
    """

    dataset_id: str
    dataset_version: str
    dataset_semantic_sha256: str
    dataset_file_sha256: str
    split_map_sha256: str
    labeling_guide_sha256: str
    owner_review_bundle_sha256: str
    #: The SHA-256 of the owner-approval artifact FILE itself (focused-review
    #: blocker remediation): the five binding hashes above are repository
    #: constants, so without this pin a well-formed APPROVED artifact could
    #: be reconstructed by any evidence-root writer. Pinning the artifact
    #: hash in the audited tree moves the trust anchor into the exact-head
    #: audit, like every other binding.
    approval_artifact_sha256: str

    def validate(self) -> None:
        for name in ("dataset_id", "dataset_version"):
            value = getattr(self, name)
            _require(isinstance(value, str) and bool(value), f"{name} required")
        for name in (
            "dataset_semantic_sha256",
            "dataset_file_sha256",
            "split_map_sha256",
            "labeling_guide_sha256",
            "owner_review_bundle_sha256",
            "approval_artifact_sha256",
        ):
            _require_sha256(getattr(self, name), name)

    def gate_identity(self) -> DatasetIdentity:
        return DatasetIdentity(
            dataset_id=self.dataset_id,
            dataset_version=self.dataset_version,
            dataset_sha256=self.dataset_semantic_sha256,
            split_map_sha256=self.split_map_sha256,
            labeling_guide_sha256=self.labeling_guide_sha256,
        )


#: The owner-approved v2 artifact identity (BER-DEC-008 decision 34; owner
#: approval of 2026-08-14). These are the ONLY values the live path accepts.
PRODUCTION_APPROVED_ARTIFACTS = ApprovedArtifactIdentity(
    dataset_id="calibration.scenario_a.wp2b3-candidate",
    dataset_version="1.0.0-wp2b3-candidate.2",
    dataset_semantic_sha256=(
        "b73c8d855fdf9ff304e18d2964d266fef3e97f42050443d52c872bd54ebaa5bf"
    ),
    dataset_file_sha256=(
        "c212c1c50d1bfd25f3de496acc542d9bd3e2fc258c51eb81ba9fd7c95d11ac56"
    ),
    split_map_sha256=(
        "08078227408b9a560afb2e5614019ef0280edda353f9d233c95adfaf4d099fca"
    ),
    labeling_guide_sha256=(
        "05708c4052ca2a7f4a173b196dd553237741710bd09db9ff21bc7e835f9fbc2d"
    ),
    owner_review_bundle_sha256=(
        "355fc2c42db6cb38c3672e940a46d4c1d6488a3b74beca56aa284641c937645a"
    ),
    approval_artifact_sha256=(
        "b04b5aa3b0854aacf9d9e53f1e9e399062e2ac5805d6b5b6b8b052e9f9dbb675"
    ),
)


# ------------------------------------------------------ evidence-root gate
@dataclass(frozen=True, slots=True)
class VerifiedEvidenceRoot:
    """Proof that an evidence root carries the exact BER-DEC-008 ownership
    marker. Canonical paths derive ONLY from this object."""

    root: str
    marker: Mapping[str, Any]
    marker_sha256: str


#: Marker fields that must equal these exact authorization facts.
_MARKER_BINDINGS: Mapping[str, Any] = {
    "marker_kind": "aegis-evidence-ownership-marker",
    "authorization_id": WP2B3_AUTHORIZATION_ID,
    "work_package": WP2B3_WORK_PACKAGE,
    "repository": "ModernNomad-98/Project-Aegis",
    "implementation_branch": IMPLEMENTATION_BRANCH,
    "authorization_merge_sha": WP2B3_AUTHORIZATION_MERGE_SHA,
    "authorization_tree_sha": WP2B3_AUTHORIZATION_TREE_SHA,
    "provider": "OpenAI API",
    "judge_model_snapshot": AUTHORIZED_MODEL_SNAPSHOT,
}


def _refuse_reparse_ancestors(root: str) -> None:
    """Refuse a reparse point anywhere on the evidence-root path chain
    (BER-DEC-008 decision 24)."""
    flag = getattr(stat_module, "FILE_ATTRIBUTE_REPARSE_POINT", None)
    if flag is None:  # non-Windows platforms carry no reparse attribute
        return
    path = os.path.abspath(root)
    while True:
        try:
            attributes = os.lstat(path).st_file_attributes
        except OSError:
            attributes = 0
        if attributes & flag:
            raise CalibrationAuthorizationError(
                f"evidence-root path chain contains a reparse point: {path}"
            )
        parent = os.path.dirname(path)
        if parent == path:
            return
        path = parent


def verify_evidence_root(root: str) -> VerifiedEvidenceRoot:
    """Verify the ownership marker binds this root to BER-DEC-008 exactly.

    An arbitrary directory — even one containing a ledger-shaped file — is
    rejected; only a root carrying the exact authorization marker (with the
    encrypted-volume gate recorded verified) is usable."""
    if not isinstance(root, str) or not root:
        raise CalibrationAuthorizationError("evidence root path required")
    if not os.path.isdir(root):
        raise CalibrationAuthorizationError(
            f"evidence root does not exist: {root}"
        )
    _refuse_reparse_ancestors(root)
    marker_path = os.path.join(root, MARKER_RELPATH)
    if not os.path.isfile(marker_path):
        raise CalibrationAuthorizationError(
            "evidence root carries no ownership marker; an unmarked root is "
            "never usable (BER-DEC-008 decision 24)"
        )
    with open(marker_path, encoding="utf-8") as handle:
        marker = json.load(handle)
    for key, expected in _MARKER_BINDINGS.items():
        found = marker.get(key)
        if found != expected:
            raise CalibrationAuthorizationError(
                f"ownership marker field {key!r} is {found!r}, expected "
                f"{expected!r}; this root is not the authorized BER-DEC-008 "
                "evidence root"
            )
    encryption = marker.get("encryption_verification")
    if not isinstance(encryption, Mapping) or encryption.get("verified") is not True:
        raise CalibrationAuthorizationError(
            "the encrypted-volume gate is not recorded verified in the "
            "ownership marker; STOP before provider execution "
            "(BER-DEC-008 decision 24)"
        )
    return VerifiedEvidenceRoot(
        root=root, marker=marker, marker_sha256=_sha256_file(marker_path)
    )


def _canonical_path(verified: VerifiedEvidenceRoot, relpath: str) -> str:
    if not isinstance(verified, VerifiedEvidenceRoot):
        raise CalibrationAuthorizationError(
            "canonical paths derive only from a marker-verified evidence "
            "root; arbitrary paths are refused (task section 8)"
        )
    return os.path.join(verified.root, *relpath.split("/"))


def canonical_ledger_path(verified: VerifiedEvidenceRoot) -> str:
    """The ONE canonical development ledger path."""
    return _canonical_path(verified, CANONICAL_LEDGER_RELPATH)


def canonical_manifest_path(verified: VerifiedEvidenceRoot) -> str:
    """The ONE canonical development run-manifest path."""
    return _canonical_path(verified, CANONICAL_MANIFEST_RELPATH)


# ------------------------------------------------- approved-artifact loads
def load_approved_dataset(
    verified: VerifiedEvidenceRoot,
    expected: ApprovedArtifactIdentity = PRODUCTION_APPROVED_ARTIFACTS,
) -> CandidateDataset:
    """Load the approved dataset, enforcing byte identity (file hash),
    semantic identity, split map, composition, and the guide/bundle hashes."""
    expected.validate()
    dataset_path = _canonical_path(verified, DATASET_RELPATH)
    if not os.path.isfile(dataset_path):
        raise CalibrationStopError(
            CalibrationStopReason.DATASET_INTEGRITY_MISMATCH,
            f"approved dataset artifact missing: {DATASET_RELPATH}",
        )
    if _sha256_file(dataset_path) != expected.dataset_file_sha256:
        raise CalibrationStopError(
            CalibrationStopReason.DATASET_INTEGRITY_MISMATCH,
            "the dataset file is not byte-identical to the owner-approved "
            "artifact; a changed dataset requires a new owner approval",
        )
    with open(dataset_path, encoding="utf-8") as handle:
        dataset = CandidateDataset.from_dict(json.load(handle))
    if (
        dataset.dataset_id != expected.dataset_id
        or dataset.version != expected.dataset_version
        or dataset.dataset_sha256() != expected.dataset_semantic_sha256
        or split_map_sha256(dataset) != expected.split_map_sha256
    ):
        raise CalibrationStopError(
            CalibrationStopReason.DATASET_INTEGRITY_MISMATCH,
            "the dataset does not match the owner-approved identity "
            "(id/version/semantic hash/split map)",
        )
    validate_authorized_composition(dataset)
    guide_path = _canonical_path(verified, LABELING_GUIDE_RELPATH)
    if (
        not os.path.isfile(guide_path)
        or _sha256_file(guide_path) != expected.labeling_guide_sha256
    ):
        raise CalibrationStopError(
            CalibrationStopReason.DATASET_INTEGRITY_MISMATCH,
            "the labeling guide is missing or does not hash-match the "
            "owner-approved guide",
        )
    bundle_path = _canonical_path(verified, OWNER_BUNDLE_RELPATH)
    if (
        not os.path.isfile(bundle_path)
        or _sha256_file(bundle_path) != expected.owner_review_bundle_sha256
    ):
        raise CalibrationStopError(
            CalibrationStopReason.DATASET_INTEGRITY_MISMATCH,
            "the owner-review bundle is missing or does not hash-match the "
            "owner-approved bundle",
        )
    return dataset


def load_owner_approval(
    verified: VerifiedEvidenceRoot,
    expected: ApprovedArtifactIdentity = PRODUCTION_APPROVED_ARTIFACTS,
) -> OwnerLabelApproval:
    """Load the owner label-approval artifact; absence blocks exactly like
    a PENDING approval (the gate itself re-verifies status and binding)."""
    expected.validate()
    approval_path = _canonical_path(verified, APPROVAL_ARTIFACT_RELPATH)
    if not os.path.isfile(approval_path):
        raise CalibrationStopError(
            CalibrationStopReason.OWNER_APPROVAL_PENDING,
            "no owner label-approval artifact exists under the evidence "
            "root; OWNER_LABEL_APPROVAL is PENDING and provider execution "
            "is mechanically blocked",
        )
    if _sha256_file(approval_path) != expected.approval_artifact_sha256:
        raise CalibrationStopError(
            CalibrationStopReason.OWNER_APPROVAL_PENDING,
            "the approval artifact on disk does not hash-match the "
            "owner-recorded approval artifact; a reconstructed or altered "
            "artifact is NOT an owner approval — OWNER_LABEL_APPROVAL is "
            "treated as PENDING",
        )
    with open(approval_path, encoding="utf-8") as handle:
        approval = OwnerLabelApproval.from_dict(json.load(handle))
    return approval


def approval_artifact_sha256(verified: VerifiedEvidenceRoot) -> str:
    return _sha256_file(_canonical_path(verified, APPROVAL_ARTIFACT_RELPATH))


def authorize_development_dispatch(
    *,
    approval: OwnerLabelApproval,
    expected: ApprovedArtifactIdentity,
    dataset: CandidateDataset,
    stage: ExecutionStage = ExecutionStage.DEVELOPMENT,
) -> CalibrationDispatchAuthorization:
    """Issue the gate authorization for the expected identity; the gate
    derives the closed DEVELOPMENT-only request-id set itself."""
    return authorize_calibration_dispatch(
        approval=approval,
        dataset_identity=expected.gate_identity(),
        dataset=dataset,
        stage=stage,
    )


# ---------------------------------------------- owner-freeze distributions
def nearest_rank_percentile(values, percentile: int):
    """Deterministic nearest-rank percentile (audit family D): the k-th
    smallest value with k = ceil(percentile/100 * n). No interpolation, so
    the result is always an observed sample value."""
    if not values:
        raise SchemaValidationError("percentile of an empty sample")
    ordered = sorted(values)
    k = max(1, math.ceil(percentile / 100.0 * len(ordered)))
    return ordered[k - 1]


def _distribution(values) -> dict[str, Any]:
    """The complete owner-freeze evidence for one token dimension."""
    ordered = sorted(values)
    if not ordered:
        return {
            "sample_count": 0,
            "minimum": None,
            "maximum": None,
            "mean": None,
            "median": None,
            "p95": None,
            "percentile_definition": (
                "nearest-rank: k-th smallest, k = ceil(p/100 * n)"
            ),
            "values_sorted": [],
        }
    return {
        "sample_count": len(ordered),
        "minimum": ordered[0],
        "maximum": ordered[-1],
        "mean": statistics.fmean(ordered),
        "median": statistics.median(ordered),
        "p95": nearest_rank_percentile(ordered, 95),
        "percentile_definition": (
            "nearest-rank: k-th smallest, k = ceil(p/100 * n)"
        ),
        "values_sorted": ordered,
    }


# -------------------------------------------------- deterministic item set
def development_run_order(dataset: CandidateDataset) -> tuple[CandidateItem, ...]:
    """The EXACT deterministic development execution order: the 40
    DEVELOPMENT items sorted by item id (BER-DEC-008 decisions 5-10)."""
    items = tuple(sorted(development_items(dataset), key=lambda i: i.item_id))
    _require(
        len(items) == EXPECTED_DEVELOPMENT_ITEMS,
        f"development split must contain exactly "
        f"{EXPECTED_DEVELOPMENT_ITEMS} items, got {len(items)}",
    )
    passes = sum(
        1 for i in items
        if i.candidate_expected_label is CandidateLabel.PASS
    )
    _require(
        passes == EXPECTED_DEVELOPMENT_PASS
        and len(items) - passes == EXPECTED_DEVELOPMENT_FAIL,
        "development gold labels must be exactly "
        f"{EXPECTED_DEVELOPMENT_PASS} PASS / {EXPECTED_DEVELOPMENT_FAIL} "
        "FAIL",
    )
    return items


def build_item_envelope_bytes(item: CandidateItem) -> bytes:
    """The canonical envelope bytes for one DEVELOPMENT item (label-free by
    construction: holdout items raise inside the projection)."""
    content = CalibrationItemContent.from_item(item)
    envelope = build_calibration_envelope(content)
    return canonical_bytes({k: envelope[k] for k in sorted(envelope)})


def build_item_request(item: CandidateItem, expected: ApprovedArtifactIdentity):
    """The canonical judge request for one DEVELOPMENT item."""
    content = CalibrationItemContent.from_item(item)
    envelope = build_calibration_envelope(content)
    return build_calibration_judge_request(
        content=content,
        envelope=envelope,
        dataset_id=expected.dataset_id,
        dataset_version=expected.dataset_version,
        dataset_sha256=expected.dataset_semantic_sha256,
    )


# ------------------------------------------------------------ run manifest
_MANIFEST_KEYS = frozenset(
    {
        "manifest_kind",
        "authorization_id",
        "authorization_merge_sha",
        "authorization_tree_sha",
        "pull_request",
        "execution_branch",
        "audited_execution_head_sha",
        "audited_execution_tree_sha",
        "evidence_marker_sha256",
        "approval_artifact_sha256",
        "dataset_id",
        "dataset_version",
        "dataset_semantic_sha256",
        "dataset_file_sha256",
        "split_map_sha256",
        "labeling_guide_sha256",
        "owner_review_bundle_sha256",
        "model_snapshot",
        "sdk_version",
        "canonical_ledger_relpath",
        "active_stage",
        "started_utc",
        "caps",
    }
)

_MANIFEST_KIND = "wp2b3-development-run-manifest"

#: Manifest fields that must match EXACTLY for a later segment to resume
#: (started_utc is the genesis timestamp and is preserved, not re-matched).
_MANIFEST_BINDING_KEYS = tuple(sorted(_MANIFEST_KEYS - {"started_utc"}))


def _caps_dict() -> dict[str, int]:
    return {
        "max_judgment_attempts": MAX_JUDGMENT_ATTEMPTS,
        "max_metadata_requests": MAX_METADATA_REQUESTS,
        "max_total_external_requests": MAX_TOTAL_EXTERNAL_REQUESTS,
        "max_total_spend_nanousd": MAX_TOTAL_SPEND_NANOUSD,
        "max_single_day_spend_nanousd": MAX_SINGLE_DAY_SPEND_NANOUSD,
        "max_input_tokens_per_judgment": MAX_INPUT_TOKENS_PER_JUDGMENT,
        "development_max_output_tokens": DEV_MAX_OUTPUT_TOKENS,
        "development_stage_deadline_seconds": DEV_STAGE_DEADLINE_SECONDS,
        "total_run_deadline_seconds": TOTAL_RUN_DEADLINE_SECONDS,
    }


def build_run_manifest(
    *,
    verified: VerifiedEvidenceRoot,
    expected: ApprovedArtifactIdentity,
    audited_head_sha: str,
    audited_tree_sha: str,
    started_utc: str,
) -> dict[str, Any]:
    """The canonical run manifest binding every task-section-8 fact."""
    expected.validate()
    return {
        "manifest_kind": _MANIFEST_KIND,
        "authorization_id": WP2B3_AUTHORIZATION_ID,
        "authorization_merge_sha": WP2B3_AUTHORIZATION_MERGE_SHA,
        "authorization_tree_sha": WP2B3_AUTHORIZATION_TREE_SHA,
        "pull_request": IMPLEMENTATION_PULL_REQUEST,
        "execution_branch": IMPLEMENTATION_BRANCH,
        "audited_execution_head_sha": audited_head_sha,
        "audited_execution_tree_sha": audited_tree_sha,
        "evidence_marker_sha256": verified.marker_sha256,
        "approval_artifact_sha256": approval_artifact_sha256(verified),
        "dataset_id": expected.dataset_id,
        "dataset_version": expected.dataset_version,
        "dataset_semantic_sha256": expected.dataset_semantic_sha256,
        "dataset_file_sha256": expected.dataset_file_sha256,
        "split_map_sha256": expected.split_map_sha256,
        "labeling_guide_sha256": expected.labeling_guide_sha256,
        "owner_review_bundle_sha256": expected.owner_review_bundle_sha256,
        "model_snapshot": AUTHORIZED_MODEL_SNAPSHOT,
        "sdk_version": _recorded_sdk_version(),
        "canonical_ledger_relpath": CANONICAL_LEDGER_RELPATH,
        "active_stage": "DEVELOPMENT",
        "started_utc": started_utc,
        "caps": _caps_dict(),
    }


# ------------------------------------------------------------- the driver
class Wp2b3DevelopmentDriver:
    """The Stage A2 DEVELOPMENT driver: composes the Stage A1 gate, ledger,
    and provider machinery under the section 8-11 controls."""

    def __init__(
        self,
        *,
        verified_root: VerifiedEvidenceRoot,
        expected_artifacts: ApprovedArtifactIdentity = (
            PRODUCTION_APPROVED_ARTIFACTS
        ),
        audited_head_sha: str,
        audited_tree_sha: str,
        current_head_sha: str,
        current_tree_sha: str,
        time_source: Callable[[], float] = time.time,
        day_provider: Callable[[], str] = _utc_day,
    ) -> None:
        if not isinstance(verified_root, VerifiedEvidenceRoot):
            raise CalibrationAuthorizationError(
                "the driver requires a marker-verified evidence root"
            )
        expected_artifacts.validate()
        for name, value in (
            ("audited_head_sha", audited_head_sha),
            ("audited_tree_sha", audited_tree_sha),
            ("current_head_sha", current_head_sha),
            ("current_tree_sha", current_tree_sha),
        ):
            _require_sha1_hex(value, name)
        if (
            current_head_sha != audited_head_sha
            or current_tree_sha != audited_tree_sha
        ):
            raise CalibrationAuthorizationError(
                "the current repository head/tree does not equal the "
                "audited execution head/tree; the GENESIS/resume "
                "precondition (exact-head ChatGPT audit) is not satisfied"
            )
        self.verified_root = verified_root
        self.expected_artifacts = expected_artifacts
        self.audited_head_sha = audited_head_sha
        self.audited_tree_sha = audited_tree_sha
        self._time_source = time_source
        self._day_provider = day_provider
        self.dataset: CandidateDataset | None = None
        self.approval: OwnerLabelApproval | None = None
        self.authorization: CalibrationDispatchAuthorization | None = None
        self.ledger: CalibrationLedger | None = None
        self._segment_open_verified = False
        self.state = "READY"

    def _request_id(self, item: CandidateItem) -> str:
        """The label-opaque request id for one approved item (family A)."""
        return calibration_request_id(
            item.item_id, self.expected_artifacts.dataset_semantic_sha256
        )

    # ------------------------------------------------------------- gates
    def prepare(self) -> None:
        """Section 10 steps 3-4: verify the approved artifacts and load the
        APPROVED owner artifact through the hard gate."""
        self.dataset = load_approved_dataset(
            self.verified_root, self.expected_artifacts
        )
        self.approval = load_owner_approval(
            self.verified_root, self.expected_artifacts
        )
        self.authorization = authorize_development_dispatch(
            approval=self.approval,
            expected=self.expected_artifacts,
            dataset=self.dataset,
            stage=ExecutionStage.DEVELOPMENT,
        )

    def _require_prepared(self) -> None:
        if (
            self.dataset is None
            or self.approval is None
            or self.authorization is None
        ):
            raise CalibrationAuthorizationError(
                "the approval/dataset gates have not passed; call prepare() "
                "first — no ledger or provider interaction exists before "
                "the gates"
            )

    # -------------------------------------------------- genesis / reopen
    def create_genesis(self, *, started_utc: str) -> None:
        """Create the canonical run manifest and the ledger GENESIS —
        refused whenever either already exists (one genesis, ever)."""
        self._require_prepared()
        _require(
            isinstance(started_utc, str) and bool(started_utc),
            "started_utc required",
        )
        ledger_path = canonical_ledger_path(self.verified_root)
        manifest_path = canonical_manifest_path(self.verified_root)
        if os.path.exists(ledger_path):
            raise CalibrationLedgerError(
                "the canonical work-package ledger already exists; a second "
                "GENESIS (a fresh accounting history) is mechanically "
                "refused — reopen the existing ledger instead"
            )
        if os.path.exists(manifest_path):
            raise CalibrationLedgerError(
                "the canonical run manifest already exists; a second "
                "GENESIS is refused"
            )
        manifest = build_run_manifest(
            verified=self.verified_root,
            expected=self.expected_artifacts,
            audited_head_sha=self.audited_head_sha,
            audited_tree_sha=self.audited_tree_sha,
            started_utc=started_utc,
        )
        os.makedirs(os.path.dirname(manifest_path), exist_ok=True)
        with open(manifest_path, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(json.dumps(manifest, sort_keys=True, indent=2) + "\n")
            fh.flush()
            os.fsync(fh.fileno())
        self.ledger = CalibrationLedger(
            ledger_path, declare_first_segment=True
        )

    def reopen(self) -> None:
        """Reopen the ONE canonical ledger: verify the chain, re-prove every
        manifest binding, and fail closed on orphans or a crashed-open
        active segment (sections 8 and 11)."""
        self._require_prepared()
        ledger_path = canonical_ledger_path(self.verified_root)
        manifest_path = canonical_manifest_path(self.verified_root)
        if not os.path.exists(ledger_path):
            raise CalibrationLedgerError(
                "no canonical ledger exists; a first segment requires the "
                "explicit GENESIS declaration"
            )
        if not os.path.exists(manifest_path):
            raise CalibrationAuthorizationError(
                "the canonical run manifest is missing; resume is refused"
            )
        with open(manifest_path, encoding="utf-8") as handle:
            recorded = json.load(handle)
        unknown = set(recorded) - _MANIFEST_KEYS
        missing = _MANIFEST_KEYS - set(recorded)
        if unknown or missing:
            raise CalibrationAuthorizationError(
                f"run manifest shape mismatch (unknown {sorted(unknown)}, "
                f"missing {sorted(missing)}); resume is refused"
            )
        expected_now = build_run_manifest(
            verified=self.verified_root,
            expected=self.expected_artifacts,
            audited_head_sha=self.audited_head_sha,
            audited_tree_sha=self.audited_tree_sha,
            started_utc=recorded.get("started_utc", ""),
        )
        for key in _MANIFEST_BINDING_KEYS:
            if recorded.get(key) != expected_now.get(key):
                raise CalibrationAuthorizationError(
                    f"run-manifest binding {key!r} does not match the "
                    "current verified state (recorded "
                    f"{recorded.get(key)!r}, expected "
                    f"{expected_now.get(key)!r}); a model/dataset/approval/"
                    "code-head/settings/manifest mismatch prevents resume"
                )
        ledger = CalibrationLedger(ledger_path)
        if ledger.orphaned_attempt_ids:
            raise CalibrationStopError(
                CalibrationStopReason.BUDGET_TELEMETRY_UNAVAILABLE,
                "the ledger records STARTED attempts with no terminal event "
                f"(orphans: {list(ledger.orphaned_attempt_ids)}); their "
                "billing is unknown and resume is refused pending owner "
                "review — an orphan is never silently retried",
            )
        if self._has_unclosed_segment(ledger_path):
            raise CalibrationAuthorizationError(
                "the durable chain records an OPEN ACTIVE SEGMENT from a "
                "prior run (an uncontrolled crash is preserved honestly); "
                "resume is refused pending owner review"
            )
        # Family C: persisted failure/terminal run states are authoritative
        # across restarts — RUN_STOPPED and OWNER_WAIT can never be
        # silently resumed; only a clean RUN_PAUSED run may continue.
        run_state = ledger.current_run_state()
        if run_state == RUN_STATE_STOPPED:
            raise CalibrationStopError(
                CalibrationStopReason.UNAUTHORIZED_EXECUTION_STAGE,
                "the durable ledger records RUN_STOPPED (a fail-closed "
                "provider/auth/model/cap/telemetry/metadata stop); "
                "automatic resume is prohibited and no request may be "
                "repeated — this run returns to Peter Nguyen for a "
                "separate disposition",
            )
        if run_state == RUN_STATE_OWNER_WAIT:
            raise CalibrationStopError(
                CalibrationStopReason.UNAUTHORIZED_EXECUTION_STAGE,
                "the durable ledger records OWNER_WAIT: all 40 development "
                "outcomes are terminal and the summary is written; every "
                "further provider interaction is prohibited",
            )
        if os.path.exists(
            _canonical_path(self.verified_root,
                            DEVELOPMENT_RESULT_SUMMARY_RELPATH)
        ):
            raise CalibrationStopError(
                CalibrationStopReason.UNAUTHORIZED_EXECUTION_STAGE,
                "the development result summary already exists; the "
                "development stage is complete and cannot be re-entered",
            )
        self.ledger = ledger

    # ----------------------------------------------------- event reading
    @staticmethod
    def _read_events(ledger_path: str) -> list[dict[str, Any]]:
        events: list[dict[str, Any]] = []
        with open(ledger_path, encoding="utf-8") as handle:
            for line in handle:
                line = line.strip()
                if line:
                    events.append(json.loads(line))
        return events

    @classmethod
    def _has_unclosed_segment(cls, ledger_path: str) -> bool:
        depth = 0
        for event in cls._read_events(ledger_path):
            if event.get("event_kind") == "ACTIVE_SEGMENT_BEGIN":
                depth += 1
            elif event.get("event_kind") == "ACTIVE_SEGMENT_END":
                depth -= 1
        return depth > 0

    def _terminal_request_ids(self) -> set[str]:
        """Logical judgment ids with a durable terminal SEMANTIC_OUTCOME."""
        ledger_path = canonical_ledger_path(self.verified_root)
        if not os.path.exists(ledger_path):
            return set()
        attempt_to_logical: dict[str, str] = {}
        terminal: set[str] = set()
        for event in self._read_events(ledger_path):
            kind = event.get("event_kind")
            if kind == "ATTEMPT_STARTED":
                logical = event.get("logical_judgment_id")
                if logical:
                    attempt_to_logical[event["attempt_id"]] = logical
            elif kind == "ATTEMPT_TERMINAL":
                logical = event.get("logical_judgment_id")
                if logical:
                    attempt_to_logical[event["internal_request_id"]] = logical
            elif kind == "SEMANTIC_OUTCOME":
                logical = attempt_to_logical.get(
                    event.get("internal_request_id", "")
                )
                if logical:
                    terminal.add(logical)
        return terminal

    # --------------------------------------------------- active segment
    def open_development_segment(self) -> None:
        """Open the persistent DEVELOPMENT active segment and verify it is
        DURABLY present before any external interaction (section 9)."""
        self._require_prepared()
        if self.ledger is None:
            raise CalibrationAuthorizationError(
                "no ledger is open; create the genesis or reopen first"
            )
        self.ledger.begin_active_segment(
            "DEVELOPMENT", self._time_source()
        )
        ledger_path = canonical_ledger_path(self.verified_root)
        events = self._read_events(ledger_path)
        if (
            not events
            or events[-1].get("event_kind") != "ACTIVE_SEGMENT_BEGIN"
            or events[-1].get("stage") != "DEVELOPMENT"
            or not self._has_unclosed_segment(ledger_path)
        ):
            raise CalibrationLedgerError(
                "the DEVELOPMENT active segment is not durably present in "
                "the canonical ledger; external interaction is refused"
            )
        self._segment_open_verified = True

    def close_development_segment(self) -> None:
        """Controlled close of the active segment (controlled stops always
        close; an uncontrolled crash leaves the open segment preserved)."""
        if self.ledger is None:
            raise CalibrationAuthorizationError("no ledger is open")
        self.ledger.end_active_segment(self._time_source())
        self._segment_open_verified = False

    def _require_open_segment(self) -> None:
        if self.state == "OWNER_WAIT":
            raise CalibrationStopError(
                CalibrationStopReason.UNAUTHORIZED_EXECUTION_STAGE,
                "OWNER_WAIT permits no provider interaction "
                "(BER-DEC-008 decision 19)",
            )
        if self.ledger is None or not self._segment_open_verified:
            raise CalibrationStopError(
                CalibrationStopReason.UNAUTHORIZED_EXECUTION_STAGE,
                "no verified DEVELOPMENT active segment is open; every "
                "external interaction is refused (task section 9)",
            )

    # ------------------------------------------------------ interaction
    def make_client(
        self,
        sdk_client: Any,
        exception_types: TransportExceptionTypes | None = None,
    ) -> OpenAICalibrationJudgeClient:
        # A live-capable client exists ONLY under a verified open
        # DEVELOPMENT segment, so deadline clocks bind every possible use.
        self._require_open_segment()
        self._require_prepared()
        assert self.authorization is not None
        if self.ledger is None:
            raise CalibrationAuthorizationError("no ledger is open")
        return OpenAICalibrationJudgeClient(
            authorization=self.authorization,
            ledger=self.ledger,
            sdk_client=sdk_client,
            exception_types=exception_types,
            day_provider=self._day_provider,
            time_source=self._time_source,
        )

    def run_metadata_probe(
        self,
        *,
        sdk_client: Any,
        exception_types: TransportExceptionTypes | None = None,
    ) -> Any:
        """The single authorized read-only availability request — refused
        without the verified open DEVELOPMENT segment."""
        self._require_open_segment()
        client = self.make_client(sdk_client, exception_types)
        return client.request_model_availability_metadata()

    def run_development_judgments(
        self,
        *,
        sdk_client: Any,
        exception_types: TransportExceptionTypes | None = None,
        owner_stop_after_items: int | None = None,
    ) -> int:
        """Dispatch the remaining development items in deterministic order;
        items with a durable terminal outcome are NEVER dispatched again."""
        self._require_open_segment()
        assert self.dataset is not None
        client = self.make_client(sdk_client, exception_types)
        dispatched = 0
        for item in development_run_order(self.dataset):
            request_id = self._request_id(item)
            if request_id in self._terminal_request_ids():
                continue
            self._dispatch_one(client, item)
            dispatched += 1
            if (
                owner_stop_after_items is not None
                and dispatched >= owner_stop_after_items
            ):
                break
        return dispatched

    def _dispatch_one(
        self, client: OpenAICalibrationJudgeClient, item: CandidateItem
    ) -> None:
        content = CalibrationItemContent.from_item(item)
        envelope = build_calibration_envelope(content)
        request = build_calibration_judge_request(
            content=content,
            envelope=envelope,
            dataset_id=self.expected_artifacts.dataset_id,
            dataset_version=self.expected_artifacts.dataset_version,
            dataset_sha256=self.expected_artifacts.dataset_semantic_sha256,
        )
        outcome = dispatch_calibration_judgment(client, request, envelope)
        if not outcome.is_verdict:
            self._ensure_error_terminal(request.request_id, outcome)

    def _ensure_error_terminal(self, request_id: str, outcome: Any) -> None:
        """Guarantee a durable terminal semantic event for a JUDGE_ERROR
        outcome whose attempt produced no unvalidated output (e.g. an
        incomplete response) — a development JUDGE_ERROR is terminal and is
        never semantically retried (BER-DEC-008 decision 19)."""
        assert self.ledger is not None
        entries = [
            entry
            for entry in self.ledger.entries()
            if entry.logical_judgment_id == request_id
            and entry.request_kind == RequestKind.JUDGMENT_ATTEMPT.value
        ]
        if not entries:
            return  # nothing external ever started (fail-closed earlier)
        if any(
            entry.outcome_kind == "OUTPUT_RECEIVED_UNVALIDATED"
            for entry in entries
        ):
            return  # the provider path already appended the semantic event
        kind = getattr(outcome, "judge_error_kind", None) or "UNCLASSIFIED"
        self.ledger.record_semantic_outcome(
            entries[-1].internal_request_id,
            f"JUDGE_ERROR_{kind}",
            detail=request_id,
        )

    # -------------------------------------------------------- completion
    def _outcome_by_item(self) -> dict[str, str]:
        """Latest durable semantic outcome per logical judgment id."""
        ledger_path = canonical_ledger_path(self.verified_root)
        attempt_to_logical: dict[str, str] = {}
        outcomes: dict[str, str] = {}
        for event in self._read_events(ledger_path):
            kind = event.get("event_kind")
            if kind in ("ATTEMPT_STARTED", "ATTEMPT_TERMINAL"):
                logical = event.get("logical_judgment_id")
                attempt_id = event.get("attempt_id") or event.get(
                    "internal_request_id"
                )
                if logical and attempt_id:
                    attempt_to_logical[attempt_id] = logical
            elif kind == "SEMANTIC_OUTCOME":
                logical = attempt_to_logical.get(
                    event.get("internal_request_id", "")
                )
                if logical:
                    outcomes[logical] = event.get("outcome", "")
        return outcomes

    def finalize(self) -> dict[str, Any]:
        """Close the segment, compute the repository-safe development
        summary, write it once, and enter OWNER_WAIT (section 10 steps
        16-20). Refused until ALL 40 outcomes are terminal."""
        self._require_prepared()
        assert self.dataset is not None
        order = development_run_order(self.dataset)
        outcomes = self._outcome_by_item()
        missing = [
            item.item_id for item in order
            if self._request_id(item) not in outcomes
        ]
        if missing:
            raise CalibrationAuthorizationError(
                "OWNER_WAIT requires ALL 40 development outcomes terminal "
                f"and reconciled; missing: {missing[:5]}{'...' if len(missing) > 5 else ''}"
            )
        if self._segment_open_verified:
            self.close_development_segment()
        summary = self._build_summary(order, outcomes)
        summary_path = _canonical_path(
            self.verified_root, DEVELOPMENT_RESULT_SUMMARY_RELPATH
        )
        if os.path.exists(summary_path):
            raise CalibrationLedgerError(
                "the development result summary already exists; it is "
                "append-only and never overwritten"
            )
        with open(summary_path, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(json.dumps(summary, sort_keys=True, indent=2) + "\n")
            fh.flush()
            os.fsync(fh.fileno())
        # Family C: OWNER_WAIT is durable — the transition is an
        # append-only chain event that survives restarts and blocks every
        # further external interaction.
        assert self.ledger is not None
        self.ledger.record_run_state(
            RUN_STATE_OWNER_WAIT,
            reason="all-40-development-outcomes-terminal",
        )
        self.state = "OWNER_WAIT"
        return summary

    def _build_summary(
        self, order: tuple[CandidateItem, ...], outcomes: dict[str, str]
    ) -> dict[str, Any]:
        assert self.ledger is not None
        agree = 0
        false_pass = 0
        false_fail = 0
        abstention = 0
        judge_error = 0
        per_item: list[dict[str, str]] = []
        matrix = {
            "expected_pass": 0,
            "expected_fail": 0,
            "true_pass": 0,
            "true_fail": 0,
            "false_pass": 0,
            "false_fail": 0,
            "abstain": 0,
            "judge_error": 0,
        }
        for item in order:
            gold = item.candidate_expected_label.value
            outcome = outcomes[self._request_id(item)]
            matrix["expected_pass" if gold == "PASS" else "expected_fail"] += 1
            if outcome.startswith("JUDGE_ERROR"):
                judge_error += 1
                matrix["judge_error"] += 1
            elif outcome == "VALIDATED_ABSTAIN":
                abstention += 1
                matrix["abstain"] += 1
            elif outcome == "VALIDATED_PASS":
                if gold == "PASS":
                    agree += 1
                    matrix["true_pass"] += 1
                else:
                    false_pass += 1
                    matrix["false_pass"] += 1
            elif outcome == "VALIDATED_FAIL":
                if gold == "FAIL":
                    agree += 1
                    matrix["true_fail"] += 1
                else:
                    false_fail += 1
                    matrix["false_fail"] += 1
            per_item.append({
                "item_id": item.item_id,
                "request_id": self._request_id(item),  # the opaque mapping
                "outcome": outcome,
            })

        events = self._read_events(
            canonical_ledger_path(self.verified_root)
        )
        judgment_terminals = [
            e for e in events
            if e.get("event_kind") == "ATTEMPT_TERMINAL"
            and e.get("request_kind") == RequestKind.JUDGMENT_ATTEMPT.value
        ]
        retries = sum(
            1 for e in judgment_terminals if e.get("attempt_number") == 2
        )
        # Distribution basis: attempts that produced provider telemetry
        # (completed or incomplete responses). Zero-token transport-failure
        # terminals would dilute the means the owner reads for the holdout
        # max_output_tokens freeze.
        usable = [
            e for e in judgment_terminals
            if e.get("response_status") in ("completed", "incomplete")
        ]
        latencies = [int(e.get("latency_ms", 0)) for e in usable]
        inputs = [int(e.get("input_tokens", 0)) for e in usable]
        outputs = [int(e.get("output_tokens", 0)) for e in usable]
        reasonings = [int(e.get("reasoning_tokens", 0)) for e in usable]
        incomplete = [
            {
                "request_id": e.get("logical_judgment_id"),
                "reason": e.get("incomplete_details_reason"),
            }
            for e in judgment_terminals
            if e.get("response_status") == "incomplete"
        ]
        cumulative = self.ledger.cumulative()
        total = len(order)
        return {
            "summary_kind": "wp2b3-development-result-summary",
            "work_package": WP2B3_WORK_PACKAGE,
            "authorization_id": WP2B3_AUTHORIZATION_ID,
            "stage": "DEVELOPMENT",
            "state": "OWNER_WAIT",
            "items_total": total,
            "agreement": agree / total,
            "agreement_count": agree,
            "false_pass_count": false_pass,
            "false_fail_count": false_fail,
            "abstention_count": abstention,
            "judge_error_count": judge_error,
            "confusion_matrix": matrix,
            "per_item_outcomes": per_item,
            "incomplete_responses": incomplete,
            "token_distribution": {
                "input_tokens_total": cumulative.input_tokens_total,
                "output_tokens_total": cumulative.output_tokens_total,
                "reasoning_tokens_total": cumulative.reasoning_tokens_total,
                "cached_input_tokens_total": (
                    cumulative.cached_input_tokens_total
                ),
                "per_judgment_output_max": max(outputs, default=0),
                "per_judgment_output_mean": (
                    statistics.fmean(outputs) if outputs else 0.0
                ),
            },
            # Family D: the complete owner-freeze evidence — per-judgment
            # distributions over telemetry-bearing attempts only (transport
            # failures without token telemetry are excluded here but remain
            # counted in attempts/retries/failures/spend accounting).
            "distributions": {
                "input_tokens": _distribution(inputs),
                "output_tokens": _distribution(outputs),
                "reasoning_tokens": _distribution(reasonings),
            },
            "accounting": {
                "judgment_attempts": cumulative.attempts_total,
                "metadata_requests": cumulative.metadata_requests,
                "total_external_requests": (
                    cumulative.total_external_requests
                ),
                "retries": retries,
                "spend_nanousd_total": cumulative.spend_nanousd_total,
                "latency_ms_max": max(latencies, default=0),
                "latency_ms_mean": (
                    statistics.fmean(latencies) if latencies else 0.0
                ),
            },
            "gold_labels": {
                "expected_pass": EXPECTED_DEVELOPMENT_PASS,
                "expected_fail": EXPECTED_DEVELOPMENT_FAIL,
            },
        }

    # ------------------------------------------------------ orchestration
    def execute_development(
        self,
        *,
        sdk_client: Any,
        exception_types: TransportExceptionTypes | None = None,
        declare_first_segment: bool,
        started_utc: str,
        owner_stop_after_items: int | None = None,
    ) -> dict[str, Any]:
        """The future DEVELOPMENT run in the exact section-10 order. Stage
        A2 preflight exercises this with fakes only."""
        if self.authorization is None:
            self.prepare()
        if declare_first_segment:
            self.create_genesis(started_utc=started_utc)
        else:
            self.reopen()
        self.open_development_segment()
        assert self.ledger is not None
        try:
            # Family C: judgments require one durable metadata SUCCESS
            # (METADATA_OK for the exact snapshot) — a metadata attempt
            # COUNT never suffices, and the single authorized request is
            # never repeated.
            if not self.ledger.metadata_success_recorded():
                if self.ledger.cumulative().metadata_requests >= 1:
                    raise CalibrationStopError(
                        CalibrationStopReason.UNAUTHORIZED_EXECUTION_STAGE,
                        "the single authorized metadata availability "
                        "request was consumed without a durable "
                        "METADATA_OK success; no judgment may proceed and "
                        "no metadata retry exists — owner disposition "
                        "required",
                    )
                self.run_metadata_probe(
                    sdk_client=sdk_client, exception_types=exception_types
                )
            dispatched = self.run_development_judgments(
                sdk_client=sdk_client,
                exception_types=exception_types,
                owner_stop_after_items=owner_stop_after_items,
            )
        except CalibrationStopError as exc:
            # Section 9.6 + family C: a typed stop persists the fail-closed
            # RUN_STOPPED state FIRST and then closes the active segment —
            # if storage fails between the two appends, the surviving state
            # is the (already resume-blocking) open segment, never a
            # silently resumable run. Automatic resume after restart is
            # impossible; the run returns to the owner. Only an
            # uncontrolled crash leaves a segment open.
            self.ledger.record_run_state(
                RUN_STATE_STOPPED, reason=exc.stop_reason.value
            )
            if self._segment_open_verified:
                self.close_development_segment()
            self.state = "RUN_STOPPED"
            raise
        assert self.dataset is not None
        terminal = self._terminal_request_ids()
        all_ids = {
            self._request_id(item)
            for item in development_run_order(self.dataset)
        }
        if all_ids <= terminal:
            return self.finalize()
        # Family C: the deliberate owner-controlled partial pause is
        # durably RUN_PAUSED (no provider failure implied); a clean
        # RUN_PAUSED run may lawfully resume from the same ledger.
        self.close_development_segment()
        self.ledger.record_run_state(
            RUN_STATE_PAUSED, reason="owner_stop_after_items"
        )
        self.state = "RUN_PAUSED"
        return {
            "state": "RUN_PAUSED",
            "stopped_after_items": dispatched,
            "terminal_total": len(all_ids & terminal),
            "items_total": len(all_ids),
        }


# --------------------------------------------------------- live execution
def consume_credential(
    environ: MutableMapping[str, str] | None = None,
) -> CalibrationCredential:
    """Consume-once credential read (BER-DEC-008 decisions 23, 32). The
    Stage A2 preflight only ever passes DUMMY test mappings here."""
    return consume_process_scoped_credential(environ)


def _resolve_repo_identity(repo_root: str) -> tuple[str, str]:
    """Resolve the CURRENT repository head and tree via the materializer's
    confined Git runner (subprocess stays confined to materialize.py)."""
    from ..materialize import _run_git  # local import: live path only

    head = _run_git(repo_root, ["rev-parse", "--verify", "HEAD"]).decode(
        "ascii"
    ).strip()
    tree = _run_git(
        repo_root, ["rev-parse", "--verify", "HEAD^{tree}"]
    ).decode("ascii").strip()
    status = _run_git(repo_root, ["status", "--porcelain"]).decode(
        "utf-8", "replace"
    ).strip()
    if status:
        raise CalibrationAuthorizationError(
            "the implementation clone working tree is not clean; live "
            "execution requires the exact audited state"
        )
    return head, tree


def execute_development_live(
    *,
    audited_head_sha: str,
    audited_tree_sha: str,
    declare_first_segment: bool,
    current_head_sha: str | None = None,
    current_tree_sha: str | None = None,
    environ: MutableMapping[str, str] | None = None,
    owner_stop_after_items: int | None = None,
    repo_root: str | None = None,
    _root_override_for_offline_tests: str | None = None,
    _expected_artifacts_override_for_offline_tests: (
        ApprovedArtifactIdentity | None
    ) = None,
) -> dict[str, Any]:
    """The FUTURE live entry: section 10 steps 1-8 in order, then the run.

    Never invoked in the Stage A2 preflight. The evidence root is the
    hard-pinned ``AUTHORIZED_EVIDENCE_ROOT``; the underscore overrides
    exist for OFFLINE TESTS ONLY and never carry a live credential.
    """
    # 1. exact repository head/tree and authorization state
    if current_head_sha is None or current_tree_sha is None:
        if repo_root is None:
            repo_root = os.path.abspath(
                os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             "..", "..", "..")
            )
        current_head_sha, current_tree_sha = _resolve_repo_identity(repo_root)
    # 2. evidence root marker / ACL / encryption / retention surface
    root = _root_override_for_offline_tests or AUTHORIZED_EVIDENCE_ROOT
    verified = verify_evidence_root(root)
    expected = (
        _expected_artifacts_override_for_offline_tests
        or PRODUCTION_APPROVED_ARTIFACTS
    )
    driver = Wp2b3DevelopmentDriver(
        verified_root=verified,
        expected_artifacts=expected,
        audited_head_sha=audited_head_sha,
        audited_tree_sha=audited_tree_sha,
        current_head_sha=current_head_sha,
        current_tree_sha=current_tree_sha,
    )
    # 3-4. approved dataset/split/guide/bundle hashes + APPROVED artifact
    driver.prepare()
    # 5. exact SDK pin
    verify_sdk_version()
    # 6. consume the dedicated process-scoped credential ONCE
    credential = consume_credential(environ)
    # (client construction re-checks env interference and invariants)
    sdk_client = build_judge_client(credential, environ)
    # 7-20. manifest/genesis or reopen, active segment, metadata, the 40
    # development judgments, summary, OWNER_WAIT.
    started_utc = datetime.now(timezone.utc).isoformat()
    return driver.execute_development(
        sdk_client=sdk_client,
        declare_first_segment=declare_first_segment,
        started_utc=started_utc,
        owner_stop_after_items=owner_stop_after_items,
    )


# ------------------------------------------------------------ module CLI
def _describe() -> dict[str, Any]:
    """The offline description of this driver (no side effects)."""
    return {
        "driver": "wp2b3-development-driver",
        "work_package": WP2B3_WORK_PACKAGE,
        "authorization_id": WP2B3_AUTHORIZATION_ID,
        "stage": "DEVELOPMENT",
        "model_snapshot": AUTHORIZED_MODEL_SNAPSHOT,
        "sdk_pin": f"openai=={AUTHORIZED_SDK_VERSION}",
        "authorized_evidence_root": AUTHORIZED_EVIDENCE_ROOT,
        "canonical_ledger_relpath": CANONICAL_LEDGER_RELPATH,
        "canonical_manifest_relpath": CANONICAL_MANIFEST_RELPATH,
        "development_items": EXPECTED_DEVELOPMENT_ITEMS,
        "development_gold_balance": (
            f"{EXPECTED_DEVELOPMENT_PASS} PASS / "
            f"{EXPECTED_DEVELOPMENT_FAIL} FAIL"
        ),
        "caps": _caps_dict(),
        "boundaries": [
            "OWNER_LABEL_APPROVAL artifact required (hash-bound, APPROVED)",
            "one canonical ledger; second genesis mechanically refused",
            "verified DEVELOPMENT active segment required before any "
            "external interaction",
            "sealed holdout structurally unreachable (owner freeze gate)",
            "OWNER_WAIT after all 40 terminal outcomes; no further calls",
        ],
        "provider_calls_made_by_this_command": 0,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="calibration_development_driver",
        description=(
            "WP-2B-3 dedicated DEVELOPMENT driver (BER-DEC-008). The "
            "default surface is the OFFLINE --describe report; live "
            "execution requires the audited head/tree and every "
            "BER-DEC-008 gate."
        ),
    )
    parser.add_argument("--describe", action="store_true",
                        help="print the offline driver contract (default)")
    parser.add_argument("--execute-development", action="store_true",
                        help="run the authorized live DEVELOPMENT stage")
    parser.add_argument("--audited-head", default=None,
                        help="the ChatGPT-audited execution head SHA")
    parser.add_argument("--audited-tree", default=None,
                        help="the ChatGPT-audited execution tree SHA")
    parser.add_argument("--declare-first-segment", action="store_true",
                        help="declare the FIRST ledger segment (genesis)")
    args = parser.parse_args(argv)

    if not args.execute_development:
        print(json.dumps(_describe(), indent=2, sort_keys=True))
        return 0
    if not args.audited_head or not args.audited_tree:
        parser.error(
            "--execute-development requires --audited-head and "
            "--audited-tree (the exact-head audit precondition)"
        )
    result = execute_development_live(
        audited_head_sha=args.audited_head,
        audited_tree_sha=args.audited_tree,
        declare_first_segment=bool(args.declare_first_segment),
    )
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
