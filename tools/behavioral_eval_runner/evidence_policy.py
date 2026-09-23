"""Opt-in, synthetic-only proof of the 30-day complete-bundle policy.

The versioned policy receipts are ordinary artifacts in existing manifests.
Their deadline is a bundle review date; legacy per-artifact expiration fields
retain their original meaning. No cleanup or host-security action exists here.
"""

from __future__ import annotations

import datetime as dt
import os
import re
from dataclasses import dataclass
from typing import Any, Mapping

from .canonical import canonical_bytes, sha256_hex
from .enums import RedactionState, RetentionClass, Sensitivity
from .errors import EvidenceError, EvidenceIntegrityError
from .evidence import (
    ArtifactMetadata,
    EvidenceArtifact,
    EvidenceWriter,
    FINAL_MANIFEST_NAME,
    FINAL_REPORT_NAME,
    INPUT_MANIFEST_NAME,
    MARKER_NAME,
    _claim_policy_receipt,
    _load_json_bytes,
    _validate_artifact_path,
    verify_final_bundle,
    verify_input_evidence,
)

POLICY_VERSION = "BER-BKL-009A-offline-v1"
STAGE_A_POLICY = "policy/stage-a.json"
STAGE_B_POLICY = "policy/stage-b.json"
_POLICY_ACCESS = "BER-DEC-011@v1"
_POLICY_DECISION = "BER-DEC-011:synthetic-policy-record"
_REF = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:/#@-]{3,}$")
_ACCESS = re.compile(r"^[A-Za-z0-9._:/#-]+@v[1-9][0-9]*$")


def _identity(path: str) -> str:
    """Conservative identity for Windows case aliases across policy stages."""
    return os.path.normcase(path).casefold()


def _now() -> str:
    return dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _parse_time(value: Any) -> dt.datetime:
    if not isinstance(value, str):
        raise EvidenceIntegrityError("policy timestamp is missing or not a string")
    try:
        parsed = dt.datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise EvidenceIntegrityError("policy timestamp is malformed") from exc
    if parsed.tzinfo is None:
        raise EvidenceIntegrityError("policy timestamp has no timezone")
    return parsed.astimezone(dt.timezone.utc)


def _iso(value: dt.datetime) -> str:
    return value.astimezone(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


@dataclass(frozen=True, slots=True)
class ClassificationDecision:
    sensitivity: Sensitivity
    redaction_state: RedactionState
    access_policy_ref: str
    decision_ref: str

    def validate(self) -> None:
        if not isinstance(self.sensitivity, Sensitivity):
            raise EvidenceError("explicit sensitivity is required")
        if not isinstance(self.redaction_state, RedactionState):
            raise EvidenceError("explicit redaction state is required")
        if not isinstance(self.access_policy_ref, str) or not _ACCESS.fullmatch(self.access_policy_ref):
            raise EvidenceError("a versioned access-policy reference is required")
        if not isinstance(self.decision_ref, str) or not _REF.fullmatch(self.decision_ref):
            raise EvidenceError("a citable content-classification decision is required")


@dataclass(frozen=True, slots=True)
class ClassifiedArtifact:
    relative_path: str
    content: bytes
    decision: ClassificationDecision


def _metadata(decision: ClassificationDecision, created_at: str | None = None) -> ArtifactMetadata:
    return ArtifactMetadata(
        sensitivity=decision.sensitivity,
        redaction_state=decision.redaction_state,
        retention_class=RetentionClass.DAYS_30,
        access_policy_ref=decision.access_policy_ref,
        preserve_on_failure=True,
        created_at=created_at,
    )


def _policy_artifact(path: str, content: bytes, created_at: str | None = None) -> EvidenceArtifact:
    return EvidenceArtifact(
        path,
        content,
        _metadata(ClassificationDecision(
            Sensitivity.INTERNAL,
            RedactionState.SANITIZED_BY_CONSTRUCTION,
            _POLICY_ACCESS,
            _POLICY_DECISION,
        ), created_at),
    )


def _decision_record(artifact: ClassifiedArtifact) -> dict[str, str]:
    if not isinstance(artifact, ClassifiedArtifact) or not isinstance(artifact.content, bytes):
        raise EvidenceError("policy requires explicit classified byte artifacts")
    if not isinstance(artifact.decision, ClassificationDecision):
        raise EvidenceError("policy requires an explicit classification decision")
    artifact.decision.validate()
    path = _validate_artifact_path(
        artifact.relative_path, allow_final_report=artifact.relative_path == FINAL_REPORT_NAME
    )
    if _identity(path) in {_identity(STAGE_A_POLICY), _identity(STAGE_B_POLICY)}:
        raise EvidenceError("policy receipt path is reserved")
    return {
        "path": path,
        "sha256": sha256_hex(artifact.content),
        "sensitivity": artifact.decision.sensitivity.value,
        "redaction_state": artifact.decision.redaction_state.value,
        "access_policy_ref": artifact.decision.access_policy_ref,
        "decision_ref": artifact.decision.decision_ref,
    }


def _records(artifacts: list[ClassifiedArtifact]) -> list[dict[str, str]]:
    records = [_decision_record(item) for item in artifacts]
    paths = [record["path"] for record in records]
    identities = [_identity(path) for path in paths]
    if _identity(FINAL_REPORT_NAME) in identities or len(identities) != len(set(identities)):
        raise EvidenceError("duplicate policy artifact path")
    return sorted(records, key=lambda record: record["path"])


def _receipt(stage: str, run_id: str, first: str, records: list[dict[str, str]],
             input_sha: str | None = None) -> bytes:
    first_time = _parse_time(first)
    payload: dict[str, Any] = {
        "policy_version": POLICY_VERSION,
        "stage": stage,
        "run_id": run_id,
        "first_created_at": _iso(first_time),
        "bundle_review_at": _iso(first_time + dt.timedelta(days=30)),
        "classification_decisions": records,
        "receipt_decision_ref": _POLICY_DECISION,
    }
    if input_sha is not None:
        payload["input_evidence_manifest_sha256"] = input_sha
    return canonical_bytes(payload)


class OfflinePolicyWriter:
    """Opt-in writer for synthetic fixtures; no legacy method is changed."""

    def __init__(self, root: str, run_id: str) -> None:
        self.writer = EvidenceWriter(root, run_id)

    def finalize_input(self, artifacts: list[ClassifiedArtifact]):
        if not artifacts:
            raise EvidenceError("policy Stage A needs a first input artifact")
        records = _records(artifacts)  # validate before first evidence write
        if os.listdir(self.writer.root):
            raise EvidenceError("policy Stage A requires an empty root; existing evidence is preserved")
        first = _iso(_parse_time(_now()))  # writer clock, normalized before first write
        receipt = _policy_artifact(
            STAGE_A_POLICY,
            _receipt("stage_a", self.writer.run_id, first, records),
            created_at=first,
        )
        _claim_policy_receipt(self.writer.root, STAGE_A_POLICY, receipt.content)
        inputs = [receipt] + [
            EvidenceArtifact(a.relative_path, a.content, _metadata(a.decision))
            for a in artifacts
        ]
        result = self.writer.finalize_input_evidence(
            inputs, _prewritten=frozenset({STAGE_A_POLICY})
        )
        verify_policy_input(self.writer.root)
        return result

    def finalize_final(self, final_report: Mapping[str, Any],
                       artifacts: list[ClassifiedArtifact],
                       report_decision: ClassificationDecision, final_status: str):
        if not isinstance(report_decision, ClassificationDecision):
            raise EvidenceError("final report needs an explicit classification decision")
        report_decision.validate()
        if not isinstance(final_report, Mapping):
            raise EvidenceError("final report must be an object")
        stage_a = verify_policy_input(self.writer.root)
        records = _records(artifacts)
        stage_a_manifest, stage_a_bytes = _load_json_bytes(self.writer.root, INPUT_MANIFEST_NAME)
        if sha256_hex(stage_a_bytes) != stage_a["input_evidence_manifest_sha256"]:
            raise EvidenceIntegrityError("Stage A changed before finalization preflight")
        prior_paths = {_identity(entry["path"]) for entry in stage_a_manifest["artifacts"]}
        if any(_identity(record["path"]) in prior_paths for record in records):
            raise EvidenceError("final artifact would overwrite Stage A evidence")
        if any(os.path.lexists(os.path.join(self.writer.root, *record["path"].split("/")))
               for record in records):
            raise EvidenceError("final artifact target already exists; preserving prior bytes")
        if any(os.path.lexists(os.path.join(self.writer.root, name)) for name in (
            FINAL_REPORT_NAME, FINAL_MANIFEST_NAME, MARKER_NAME, STAGE_B_POLICY,
        )):
            raise EvidenceError("final bundle already exists; existing evidence is preserved")
        if any(record["path"] == FINAL_REPORT_NAME for record in records):
            raise EvidenceError("final report path is reserved")
        report_content = canonical_bytes(dict(final_report))
        records.append(_decision_record(ClassifiedArtifact(
            FINAL_REPORT_NAME, report_content, report_decision,
        )))
        records.sort(key=lambda record: record["path"])
        claimed_at = _iso(_parse_time(_now()))
        receipt = _policy_artifact(STAGE_B_POLICY, _receipt(
            "stage_b", self.writer.run_id, stage_a["first_created_at"],
            records, stage_a["input_evidence_manifest_sha256"],
        ), created_at=claimed_at)
        _claim_policy_receipt(self.writer.root, STAGE_B_POLICY, receipt.content)
        outputs = [
            EvidenceArtifact(a.relative_path, a.content, _metadata(a.decision))
            for a in artifacts
        ] + [receipt]
        result = self.writer.finalize_final_bundle(
            final_report, outputs, stage_a["input_evidence_manifest_sha256"],
            final_status, report_metadata=_metadata(report_decision),
            _prewritten=frozenset({STAGE_B_POLICY}),
        )
        verify_policy_bundle(self.writer.root)
        return result


def _load_receipt(root: str, path: str, stage: str,
                  expected_entry: Mapping[str, Any]) -> dict[str, Any]:
    record, raw = _load_json_bytes(root, path)
    if sha256_hex(raw) != expected_entry.get("sha256") or len(raw) != expected_entry.get("bytes"):
        raise EvidenceIntegrityError("policy receipt changed after manifest verification")
    if canonical_bytes(record) != raw:
        raise EvidenceIntegrityError("policy receipt is not canonical JSON")
    expected = {"policy_version", "stage", "run_id", "first_created_at",
                "bundle_review_at", "classification_decisions", "receipt_decision_ref"}
    if stage == "stage_b":
        expected.add("input_evidence_manifest_sha256")
    if set(record) != expected or record.get("policy_version") != POLICY_VERSION or record.get("stage") != stage:
        raise EvidenceIntegrityError("unsupported or incomplete policy receipt")
    if record["receipt_decision_ref"] != _POLICY_DECISION:
        raise EvidenceIntegrityError("policy receipt decision is missing")
    first = _parse_time(record["first_created_at"])
    if record["first_created_at"] != _iso(first) or record["bundle_review_at"] != _iso(first + dt.timedelta(days=30)):
        raise EvidenceIntegrityError("bundle deadline differs from first writer event")
    return record


def _check_entries(manifest: Mapping[str, Any], receipt: Mapping[str, Any],
                   receipt_path: str) -> None:
    entries = manifest.get("artifacts")
    if not isinstance(entries, list):
        raise EvidenceIntegrityError("policy manifest has no artifact list")
    by_path = {entry.get("path"): entry for entry in entries if isinstance(entry, dict)}
    if len(by_path) != len(entries) or receipt_path not in by_path:
        raise EvidenceIntegrityError("policy receipt absent or duplicate paths")
    if len({_identity(path) for path in by_path}) != len(by_path):
        raise EvidenceIntegrityError("policy manifest contains filesystem path aliases")
    first = _parse_time(receipt["first_created_at"])
    policy_entry = by_path[receipt_path]
    if (policy_entry.get("sensitivity") != Sensitivity.INTERNAL.value
            or policy_entry.get("redaction_state") != RedactionState.SANITIZED_BY_CONSTRUCTION.value
            or policy_entry.get("access_policy_ref") != _POLICY_ACCESS):
        raise EvidenceIntegrityError("policy receipt classification differs")
    if receipt_path == STAGE_A_POLICY and policy_entry.get("created_at") != receipt["first_created_at"]:
        raise EvidenceIntegrityError("first timestamp is not bound to first writer artifact")
    decisions = receipt.get("classification_decisions")
    if not isinstance(decisions, list):
        raise EvidenceIntegrityError("classification decisions are missing")
    if receipt_path == STAGE_A_POLICY and not decisions:
        raise EvidenceIntegrityError("policy Stage A has no real input artifact")
    if receipt_path == STAGE_A_POLICY and STAGE_B_POLICY in by_path:
        raise EvidenceIntegrityError("Stage B policy receipt cannot satisfy Stage A input")
    if receipt_path == STAGE_B_POLICY and FINAL_REPORT_NAME not in by_path:
        raise EvidenceIntegrityError("policy Stage B does not include the final report")
    if receipt_path == STAGE_B_POLICY and STAGE_A_POLICY in by_path:
        raise EvidenceIntegrityError("Stage A policy receipt cannot be repeated in Stage B")
    decision_paths: set[str] = set()
    for decision in decisions:
        if not isinstance(decision, dict) or set(decision) != {
            "path", "sha256", "sensitivity", "redaction_state", "access_policy_ref", "decision_ref",
        }:
            raise EvidenceIntegrityError("classification decision has wrong shape")
        path = decision["path"]
        if not isinstance(path, str) or path in decision_paths or path not in by_path:
            raise EvidenceIntegrityError("classification decision path missing or repeated")
        decision_paths.add(path)
        entry = by_path[path]
        for key in ("sha256", "sensitivity", "redaction_state", "access_policy_ref"):
            if decision[key] != entry.get(key):
                raise EvidenceIntegrityError(f"classification decision {path!r} differs in {key}")
        if (entry.get("sensitivity") not in Sensitivity.values()
                or entry.get("redaction_state") not in RedactionState.values()):
            raise EvidenceIntegrityError("unknown sensitivity or redaction state")
        if not isinstance(decision["decision_ref"], str) or not _REF.fullmatch(decision["decision_ref"]):
            raise EvidenceIntegrityError("content-classification citation is missing")
        if not _ACCESS.fullmatch(str(entry.get("access_policy_ref", ""))):
            raise EvidenceIntegrityError("access policy reference is not versioned")
    if decision_paths != set(by_path) - {receipt_path}:
        raise EvidenceIntegrityError("classification decisions do not cover all content")
    for entry in entries:
        if (entry.get("retention_class") != RetentionClass.DAYS_30.value
                or entry.get("preserve_on_failure") is not True):
            raise EvidenceIntegrityError("mixed retention or failure cleanup is forbidden")
        created = _parse_time(entry.get("created_at"))
        if created < first:
            raise EvidenceIntegrityError("artifact predates first writer event")
        if entry.get("expiration_at") != _iso(created + dt.timedelta(days=30)):
            raise EvidenceIntegrityError("legacy per-artifact expiration metadata differs")


def verify_policy_input(root: str) -> dict[str, str]:
    """Check opt-in Stage A policy; never accept empty or legacy Stage A."""
    input_sha = verify_input_evidence(root)
    manifest, manifest_bytes = _load_json_bytes(root, INPUT_MANIFEST_NAME)
    if sha256_hex(manifest_bytes) != input_sha:
        raise EvidenceIntegrityError("input manifest changed after verification")
    receipt_entry = next((entry for entry in manifest["artifacts"]
                          if entry.get("path") == STAGE_A_POLICY), None)
    if receipt_entry is None:
        raise EvidenceIntegrityError("Stage A policy receipt is missing")
    receipt = _load_receipt(root, STAGE_A_POLICY, "stage_a", receipt_entry)
    if receipt["run_id"] != manifest.get("run_id"):
        raise EvidenceIntegrityError("Stage A policy run identity differs")
    _check_entries(manifest, receipt, STAGE_A_POLICY)
    return {
        "first_created_at": receipt["first_created_at"],
        "bundle_review_at": receipt["bundle_review_at"],
        "input_evidence_manifest_sha256": input_sha,
    }


def verify_policy_bundle(root: str) -> dict[str, str]:
    """Verify complete synthetic chain and its single review deadline.

    Expiration means review eligibility, never permission to delete. At or
    after the deadline this checker refuses an active-bundle acceptance claim.
    """
    stage_a = verify_policy_input(root)
    hashes = verify_final_bundle(root)  # includes detached marker binding
    if hashes["input_evidence_manifest_sha256"] != stage_a["input_evidence_manifest_sha256"]:
        raise EvidenceIntegrityError("Stage A changed during complete-bundle verification")
    manifest, manifest_bytes = _load_json_bytes(root, FINAL_MANIFEST_NAME)
    if sha256_hex(manifest_bytes) != hashes["final_evidence_manifest_sha256"]:
        raise EvidenceIntegrityError("final manifest changed after verification")
    receipt_entry = next((entry for entry in manifest["artifacts"]
                          if entry.get("path") == STAGE_B_POLICY), None)
    if receipt_entry is None:
        raise EvidenceIntegrityError("Stage B policy receipt is missing")
    receipt = _load_receipt(root, STAGE_B_POLICY, "stage_b", receipt_entry)
    if (receipt["run_id"] != manifest.get("run_id")
            or receipt["input_evidence_manifest_sha256"] != stage_a["input_evidence_manifest_sha256"]
            or receipt["first_created_at"] != stage_a["first_created_at"]
            or receipt["bundle_review_at"] != stage_a["bundle_review_at"]):
        raise EvidenceIntegrityError("Stage B policy is not bound to Stage A")
    _check_entries(manifest, receipt, STAGE_B_POLICY)
    _, report_bytes = _load_json_bytes(root, FINAL_REPORT_NAME)
    if sha256_hex(report_bytes) != hashes["final_report_sha256"]:
        raise EvidenceIntegrityError("final report changed after verification")
    marker, marker_bytes = _load_json_bytes(root, MARKER_NAME)
    if sha256_hex(marker_bytes) != hashes["finalization_marker_sha256"]:
        raise EvidenceIntegrityError("marker changed after verification")
    finalized = _parse_time(marker.get("finalized_at"))
    input_manifest, input_bytes = _load_json_bytes(root, INPUT_MANIFEST_NAME)
    if sha256_hex(input_bytes) != stage_a["input_evidence_manifest_sha256"]:
        raise EvidenceIntegrityError("input manifest changed after final verification")
    latest_artifact = max(
        _parse_time(entry["created_at"])
        for entry in input_manifest["artifacts"] + manifest["artifacts"]
    )
    verification_time = _parse_time(_now())
    if (finalized < latest_artifact or finalized > verification_time
            or _parse_time(stage_a["first_created_at"]) > verification_time):
        raise EvidenceIntegrityError("policy chronology is not writer/verifier ordered")
    deadline = _parse_time(stage_a["bundle_review_at"])
    if finalized >= deadline or verification_time >= deadline:
        raise EvidenceIntegrityError("complete bundle reached review deadline; preserve for owner review")
    return {**stage_a, **hashes}
