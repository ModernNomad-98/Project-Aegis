"""Append-only and recording checks over recorded version sequences
(WP-2B-2; prompt 10.D).

Ports the mechanical harness's CONTENT-AGNOSTIC oracles to recorded
synthetic evidence: section/row extraction (``Get-ImmutableRows``), the
append-only prefix property (``Test-AppendOnly``), placeholder preservation,
expected-record presence, and the semantic ordering gates
(``Test-SemanticGates``). Hashing is run-local (normalized-LF SHA-256 per
version); the fixture manifest's pinned digests are never applied here."""

from __future__ import annotations

from typing import Any, Mapping

from ..errors import SchemaValidationError
from .records import GraderResult, GradingReasonCode
from .hashing import run_local_hash
from ._base import (
    EvidenceMalformed,
    GradingFail,
    require_keys,
    require_str,
    run_grader,
)

GRADER_ID = "graders.append_only"
CONTROL_ID = "SCENARIO_A_CONTROL_O"

SECTION_KEYS = ("State snapshots", "Decision log", "Approvals", "Deviations")
ID_SECTION_KEYS = ("State snapshots", "Decision log", "Approvals")

ORACLE_ID = "oracle.append_only.version_sequence"

#: Observed evidence carries ONLY the recorded versions; the semantic gates
#: and expected final IDs are trusted-plan data.
_ALLOWED = frozenset({"versions", "evidence_pointer"})
_REQUIRED = _ALLOWED


def _is_separator_row(line: str) -> bool:
    stripped = line.strip()
    if not (stripped.startswith("|") and stripped.endswith("|")):
        return False
    inner = stripped.strip("|")
    return bool(inner) and set(inner) <= set(" :-|") and "-" in inner


def extract_immutable_rows(content: str) -> dict[str, list[str]]:
    """Ordered immutable rows per section (port of Get-ImmutableRows).

    Fail closed on a DUPLICATE matching section header: a second header
    matching the same section key (e.g. a trailing "## State snapshots
    (audit copy)") could otherwise shadow the real section and hide a
    tampered history from the prefix check.
    """
    lines = content.split("\n")
    raw_by_section: dict[str, list[str]] = {}
    current: str | None = None
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("## "):
            header = stripped[3:].strip()
            current = None
            for key in SECTION_KEYS:
                if header.startswith(key):
                    if key in raw_by_section:
                        raise EvidenceMalformed(
                            f"duplicate section header matching {key!r}: a "
                            "shadow section cannot replace the graded one"
                        )
                    current = key
                    raw_by_section[key] = []
                    break
            continue
        if current is not None:
            raw_by_section[current].append(line)

    result: dict[str, list[str]] = {}
    for key in SECTION_KEYS:
        rows: list[str] = []
        raw_lines = raw_by_section.get(key, [])
        separator_index = -1
        for index, line in enumerate(raw_lines):
            if _is_separator_row(line):
                separator_index = index
                break
        for index, line in enumerate(raw_lines):
            if not line.strip():
                continue
            if line.lstrip().startswith("<!--"):
                continue
            if separator_index >= 0:
                if index <= separator_index:
                    continue
                if not line.lstrip().startswith("|"):
                    continue
                rows.append(line.strip())
            else:
                if line.lstrip().startswith("- "):
                    rows.append(line.strip())
                elif rows:
                    rows[-1] = rows[-1] + " " + line.strip()
        result[key] = rows
    return result


def _row_id(row: str) -> str:
    """First cell of a pipe row (the immutable ID column)."""
    if not row.startswith("|"):
        return row
    cells = [cell.strip() for cell in row.strip("|").split("|")]
    return cells[0] if cells else ""


def extract_section_ids(content: str) -> dict[str, list[str]]:
    rows = extract_immutable_rows(content)
    return {key: [_row_id(row) for row in rows[key]] for key in ID_SECTION_KEYS}


def _is_placeholder(row: str) -> bool:
    return "(none yet)" in row or "(none recorded" in row


def _check_prefix(prev: Mapping[str, list[str]], cur: Mapping[str, list[str]]) -> None:
    for key in SECTION_KEYS:
        prev_rows = prev[key]
        cur_rows = cur[key]
        removed_placeholder = any(
            _is_placeholder(row) and row not in cur_rows for row in prev_rows
        )
        if len(cur_rows) < len(prev_rows):
            if removed_placeholder:
                raise GradingFail(
                    GradingReasonCode.PLACEHOLDER_REMOVED,
                    f"[{key}] a preserved empty-state placeholder row was removed",
                )
            raise GradingFail(
                GradingReasonCode.APPEND_ONLY_VIOLATION,
                f"[{key}] an immutable row was deleted "
                f"({len(prev_rows)} -> {len(cur_rows)})",
            )
        for index in range(len(prev_rows)):
            if cur_rows[index] != prev_rows[index]:
                if removed_placeholder:
                    raise GradingFail(
                        GradingReasonCode.PLACEHOLDER_REMOVED,
                        f"[{key}] a preserved empty-state placeholder row was "
                        "replaced instead of appended after",
                    )
                raise GradingFail(
                    GradingReasonCode.APPEND_ONLY_VIOLATION,
                    f"[{key}] immutable row #{index + 1} was edited, "
                    "reordered, or replaced",
                )


def _first_step_index(per_version_ids: list[dict[str, list[str]]],
                      section: str, wanted: str) -> int:
    for index, ids in enumerate(per_version_ids):
        if wanted in ids[section]:
            return index
    return -1


def _check_gates(
    per_version_ids: list[dict[str, list[str]]], semantics: Mapping[str, Any]
) -> None:
    forbidden = [str(v) for v in semantics["forbidden_snapshot_ids"]]
    for ids in per_version_ids:
        hit = [f for f in forbidden if f in ids["State snapshots"]]
        if hit:
            raise GradingFail(
                GradingReasonCode.FORBIDDEN_SNAPSHOT,
                f"forbidden snapshot id(s) appear in the sequence: {hit}",
            )

    stage3 = str(semantics["stage3_snapshot_id"])
    stage3_index = _first_step_index(per_version_ids, "State snapshots", stage3)
    if stage3_index >= 0:
        if stage3_index < 1:
            raise GradingFail(
                GradingReasonCode.ORDERING_GATE_VIOLATION,
                f"the Stage 3 snapshot {stage3} appears in the first recorded "
                "version; it must follow the recorded owner gate",
            )
        prior_decisions = per_version_ids[stage3_index - 1]["Decision log"]
        missing = [
            str(owner)
            for owner in semantics["stage2_owner_ids"]
            if str(owner) not in prior_decisions
        ]
        if missing:
            raise GradingFail(
                GradingReasonCode.ORDERING_GATE_VIOLATION,
                f"Stage 2 owner record(s) {missing} are not recorded before "
                f"the Stage 3 snapshot {stage3}",
            )

    acceptance = str(semantics["spec_acceptance_id"])
    completion = str(semantics["spec_owner_completion_id"])
    acceptance_index = _first_step_index(per_version_ids, "Decision log", acceptance)
    completion_index = _first_step_index(per_version_ids, "Decision log", completion)
    if completion_index >= 0 and not (
        acceptance_index >= 0 and completion_index > acceptance_index
    ):
        raise GradingFail(
            GradingReasonCode.ORDERING_GATE_VIOLATION,
            f"owner completion {completion} (version index {completion_index}) "
            f"must be recorded after the user's spec acceptance {acceptance} "
            f"(version index {acceptance_index})",
        )


def grade_version_sequence(plan, evidence: Mapping[str, Any]) -> GraderResult:
    def body(plan_obj, data: Mapping[str, Any]) -> dict[str, Any]:
        require_keys(data, _ALLOWED, _REQUIRED)
        versions = data.get("versions")
        if not isinstance(versions, list) or not versions:
            raise EvidenceMalformed("versions must be a non-empty list")
        if plan_obj.semantic_gates is None:
            raise SchemaValidationError(
                "the trusted plan must carry the semantic gates for "
                "append-only grading"
            )
        semantics = plan_obj.semantic_gates
        parsed: list[dict[str, list[str]]] = []
        id_census: list[dict[str, list[str]]] = []
        hashes: list[dict[str, str]] = []
        for version in versions:
            if not isinstance(version, Mapping):
                raise EvidenceMalformed("every version must be a mapping")
            version_id = require_str(version, "version_id")
            content = require_str(version, "content")
            rows = extract_immutable_rows(content)
            parsed.append(rows)
            id_census.append(
                {key: [_row_id(row) for row in rows[key]] for key in ID_SECTION_KEYS}
            )
            hashes.append(
                {
                    "version_id": version_id,
                    "normalized_sha256": run_local_hash(content),
                }
            )

        added_rows: list[str] = []
        for index in range(1, len(parsed)):
            _check_prefix(parsed[index - 1], parsed[index])
            for key in SECTION_KEYS:
                for row in parsed[index][key][len(parsed[index - 1][key]):]:
                    added_rows.append(f"[{key}] +{row}")

        _check_gates(id_census, semantics)

        expected = plan_obj.expected_final_ids
        if expected is not None:
            final_ids = id_census[-1]
            for section, wanted in expected.items():
                actual = final_ids[section]
                if list(wanted) != actual:
                    raise GradingFail(
                        GradingReasonCode.EXPECTED_RECORD_MISSING,
                        f"[{section}] final immutable IDs {actual} do not "
                        f"match the required IDs {list(wanted)}",
                    )

        return {
            "version_sha256s": hashes,
            "added_rows": added_rows,
            "hashing": "run-local normalized-LF SHA-256; fixture-manifest pins "
                       "are never applied to this evidence",
        }

    return run_grader(GRADER_ID, ORACLE_ID, plan, evidence, body)
