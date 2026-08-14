"""Run-local preview-versus-created hashing (WP-2B-2; prompt 10.E).

RUN-LOCAL ONLY. The grader compares a run's own preview bytes to the same
run's created bytes after newline canonicalization (CRLF/CR -> LF, mirroring
the mechanical harness's normalized hashing). There is NO parameter and NO
evidence field through which a fixture-pinned expected digest can be
injected: live output is never compared against fixture-manifest pins
(design sections 7 and 9)."""

from __future__ import annotations

from typing import Any, Mapping

from ..canonical import sha256_hex_text
from .records import GraderResult, GradingReasonCode
from ._base import EvidenceMalformed, GradingFail, require_keys, require_str, run_grader

GRADER_ID = "graders.hashing"
ORACLE_ID = "oracle.hashing.preview_vs_created"

_ALLOWED = frozenset({"preview_text", "created_text", "evidence_pointer"})
_REQUIRED = _ALLOWED


def normalize_newlines(text: str) -> str:
    """Canonicalize CRLF and lone CR to LF."""
    return text.replace("\r\n", "\n").replace("\r", "\n")


def run_local_hash(text: str) -> str:
    """SHA-256 over the newline-normalized UTF-8 text (run-local only)."""
    return sha256_hex_text(normalize_newlines(text))


def grade_preview_vs_created(plan, evidence: Mapping[str, Any]) -> GraderResult:
    def body(_plan_obj, data: Mapping[str, Any]) -> dict[str, Any]:
        require_keys(data, _ALLOWED, _REQUIRED)
        preview = require_str(data, "preview_text")
        created = data.get("created_text")
        if not isinstance(created, str) or not created:
            raise EvidenceMalformed(
                "created_text must be the non-empty recorded created bytes"
            )
        preview_sha = run_local_hash(preview)
        created_sha = run_local_hash(created)
        payload = {
            "preview_sha256": preview_sha,
            "created_sha256": created_sha,
            "canonicalization": "CRLF/CR->LF then UTF-8 SHA-256 (run-local)",
        }
        if preview_sha != created_sha:
            raise GradingFail(
                GradingReasonCode.PREVIEW_MISMATCH,
                "created content does not equal the approved preview for this run",
                payload,
            )
        return payload

    return run_grader(GRADER_ID, ORACLE_ID, plan, evidence, body)
