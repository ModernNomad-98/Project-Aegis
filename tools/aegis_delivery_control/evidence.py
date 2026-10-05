"""Canonical evidence helpers for synthetic kernel records."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Mapping

from .contracts import DispatchDenied


def canonical_bytes(record: Mapping[str, object]) -> bytes:
    return json.dumps(
        record,
        ensure_ascii=True,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("ascii")


def write_new_evidence(path: Path, record: Mapping[str, object]) -> str:
    """Create one immutable synthetic evidence file and return its SHA-256."""
    payload = canonical_bytes(record)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("xb") as stream:
        stream.write(payload)
        stream.flush()
    return hashlib.sha256(payload).hexdigest()


def verify_synthetic_evidence(
    original: bytes, *, expected_hash: str, expected_binding: str,
    expected_writer: str, expected_stage: str,
) -> dict[str, object]:
    """Verify original bytes and the one closed synthetic fixture payload."""
    try:
        if any(type(value) is not str or not value.strip() for value in (
            expected_binding, expected_writer, expected_stage,
        )):
            raise ValueError("invalid synthetic evidence identity")
        record = json.loads(original.decode("ascii"))
        if not isinstance(record, dict) or canonical_bytes(record) != original:
            raise ValueError("noncanonical evidence")
        if (set(record) != {"version", "binding", "writer", "stage", "payload"}
                or type(record["version"]) is not int or record["version"] != 1
                or record["binding"] != expected_binding
                or record["writer"] != expected_writer
                or record["stage"] != expected_stage
                or record["payload"] != {"receipt": "synthetic"}):
            raise ValueError("unverifiable or sensitive evidence")
        if hashlib.sha256(original).hexdigest() != expected_hash:
            raise ValueError("evidence hash mismatch")
    except (UnicodeError, json.JSONDecodeError, TypeError, ValueError) as error:
        raise DispatchDenied("synthetic evidence verification failed") from error
    return record


# ---------------------------------------------------------------------------
# ZT-P1 — versioned evidence envelope (ZT-01 §4.8(1))
# ---------------------------------------------------------------------------
# The full §4.8(1) envelope: one record binding repository · task ·
# plan revision · head · base · tested merge tree · policy version ·
# environment · coverage declaration · stage identity · predecessor verdict ·
# verdict · artifact digests.  Canonical serialization reuses canonical_bytes.
# Malformed and duplicate envelopes are rejected, not merged or ignored.
# The envelope carries the contract version so it satisfies acceptance A1.
# ---------------------------------------------------------------------------

EVIDENCE_ENVELOPE_FIELDS: tuple[str, ...] = (
    "contract_version",
    "repository",
    "task",
    "plan_revision",
    "head",
    "base",
    "tested_merge_tree",
    "policy_version",
    "environment",
    "coverage_declaration",
    "stage_identity",
    "predecessor_verdict",
    "verdict",
    "artifact_digests",
)


def build_versioned_evidence_envelope(
    *,
    contract_version: int,
    repository: str,
    task: str,
    plan_revision: str,
    head: str,
    base: str,
    tested_merge_tree: str,
    policy_version: str,
    environment: str,
    coverage_declaration: str,
    stage_identity: str,
    predecessor_verdict: str | None,
    verdict: str,
    artifact_digests: tuple[str, ...],
) -> dict[str, object]:
    """Build the canonical versioned evidence envelope of ZT-01 §4.8(1)."""
    from .contracts import ZT_P1_CONTRACT_VERSION

    if contract_version != ZT_P1_CONTRACT_VERSION:
        raise DispatchDenied(
            "evidence envelope contract version "
            f"{contract_version!r} != {ZT_P1_CONTRACT_VERSION!r}"
        )
    envelope: dict[str, object] = {
        "contract_version": contract_version,
        "repository": repository,
        "task": task,
        "plan_revision": plan_revision,
        "head": head,
        "base": base,
        "tested_merge_tree": tested_merge_tree,
        "policy_version": policy_version,
        "environment": environment,
        "coverage_declaration": coverage_declaration,
        "stage_identity": stage_identity,
        "predecessor_verdict": predecessor_verdict,
        "verdict": verdict,
        "artifact_digests": list(artifact_digests),
    }
    if set(envelope) != set(EVIDENCE_ENVELOPE_FIELDS):
        raise DispatchDenied("evidence envelope has an unexpected field set")
    return envelope


def verify_versioned_evidence_envelope(
    original: bytes,
    *,
    seen_identities: set[tuple[str, str, str]] | None = None,
) -> dict[str, object]:
    """Reject a malformed or duplicate versioned envelope; return the record.

    A second envelope with the same (repository, stage_identity, head)
    identity is a duplicate and is rejected, never merged or ignored.
    """
    from .contracts import ZT_P1_CONTRACT_VERSION

    try:
        record = json.loads(original.decode("ascii"))
        if not isinstance(record, dict):
            raise ValueError("envelope is not an object")
        if set(record) != set(EVIDENCE_ENVELOPE_FIELDS):
            raise ValueError("envelope has unexpected or missing fields")
        if canonical_bytes(record) != original:
            raise ValueError("envelope is not canonical")
        if type(record["contract_version"]) is not int:
            raise ValueError("envelope contract_version must be an int")
        if record["contract_version"] != ZT_P1_CONTRACT_VERSION:
            raise ValueError("envelope has an unknown contract version")
        for field in EVIDENCE_ENVELOPE_FIELDS:
            value = record[field]
            if field == "contract_version":
                continue
            if field == "artifact_digests":
                if not isinstance(value, list) or not value or not all(
                    isinstance(item, str) and item for item in value
                ):
                    raise ValueError(
                        "artifact_digests must be a non-empty list of strings"
                    )
            elif field == "predecessor_verdict":
                if value is not None and (not isinstance(value, str) or not value):
                    raise ValueError("predecessor_verdict must be a string or null")
            elif not isinstance(value, str) or not value:
                raise ValueError(f"{field} must be a non-empty string")
        identity = (
            record["repository"],
            record["stage_identity"],
            record["head"],
        )
        if seen_identities is not None:
            if identity in seen_identities:
                raise ValueError("duplicate evidence envelope identity")
            seen_identities.add(identity)
    except (UnicodeError, json.JSONDecodeError, TypeError, ValueError) as error:
        raise DispatchDenied(f"versioned evidence envelope rejected: {error}") from error
    return record
