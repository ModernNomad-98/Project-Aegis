"""Committed case data for the gated live pipeline.

A case is committed JSON: the prompt, the semantic rubric and the deterministic
checks, plus a SHA-256 that binds the rubric sub-object. The judge adapter may
only receive rubric input loaded here; there is no command-line rubric argument.
"""

from __future__ import annotations

import json
import os
from dataclasses import dataclass
from typing import Any, Mapping, Sequence

from ..canonical import canonical_bytes, sha256_hex
from . import LIVE_SCHEMA_VERSION
from .errors import LiveDatasetError

CASE_FILE_NAME = "case.json"


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise LiveDatasetError(message)


def _sha256_hex(value: str) -> bool:
    return len(value) == 64 and set(value) <= set("0123456789abcdef")


@dataclass(frozen=True, slots=True)
class LiveCase:
    """One committed case: prompt, rubric and deterministic checks."""

    case_id: str
    skill: str
    prompt: str
    baseline_prompt: str
    skill_instructions: str
    rubric: Mapping[str, Any]
    rubric_sha256: str
    deterministic_checks: Mapping[str, tuple[str, ...]]
    record_sha256: str
    source_path: str
    raw: Mapping[str, Any]

    def to_record(self) -> dict[str, Any]:
        return {
            "case_id": self.case_id,
            "skill": self.skill,
            "rubric_sha256": self.rubric_sha256,
            "record_sha256": self.record_sha256,
            "source_path": self.source_path,
        }


def rubric_sha256(rubric: Mapping[str, Any]) -> str:
    return sha256_hex(canonical_bytes(dict(rubric)))


def load_case(path: str) -> LiveCase:
    """Load and validate one committed case file (fail closed on any gap)."""
    if not os.path.isfile(path):
        raise LiveDatasetError(
            f"case file not found: {path}", context={"path": path}
        )
    with open(path, "rb") as handle:
        raw = handle.read()
    try:
        payload = json.loads(raw.decode("utf-8"))
    except (ValueError, UnicodeDecodeError) as exc:
        raise LiveDatasetError(
            f"unparsable case file: {path}: {exc}", context={"path": path}
        ) from exc
    _require(isinstance(payload, Mapping), "case file must contain an object")
    unknown = set(payload) - {
        "schema_version",
        "case_id",
        "skill",
        "prompt",
        "baseline_prompt",
        "skill_instructions",
        "rubric",
        "rubric_sha256",
        "deterministic_checks",
    }
    _require(not unknown, f"case file has unknown keys {sorted(unknown)}")
    _require(
        payload.get("schema_version") == LIVE_SCHEMA_VERSION,
        f"case schema_version must be {LIVE_SCHEMA_VERSION}",
    )
    case_id = payload.get("case_id")
    skill = payload.get("skill")
    prompt = payload.get("prompt")
    baseline_prompt = payload.get("baseline_prompt")
    skill_instructions = payload.get("skill_instructions")
    rubric = payload.get("rubric")
    declared = payload.get("rubric_sha256")
    checks = payload.get("deterministic_checks", {})
    _require(isinstance(case_id, str) and bool(case_id), "case_id must be non-empty")
    _require(isinstance(skill, str) and bool(skill), "skill must be non-empty")
    _require(isinstance(prompt, str) and bool(prompt), "prompt must be non-empty")
    _require(
        isinstance(baseline_prompt, str) and bool(baseline_prompt),
        "baseline_prompt must be non-empty (the without-baseline arm is explicit)",
    )
    _require(
        isinstance(skill_instructions, str) and bool(skill_instructions),
        "skill_instructions must be non-empty (the WITH_SKILL arm loads it)",
    )
    _require(isinstance(rubric, Mapping) and bool(rubric), "rubric must be an object")
    _require(
        isinstance(declared, str) and _sha256_hex(declared),
        "rubric_sha256 must be a 64-hex SHA-256",
    )
    _require(isinstance(checks, Mapping), "deterministic_checks must be an object")
    _require(
        not (set(checks) - {"must_include", "must_not_include"}),
        "deterministic_checks supports only must_include / must_not_include",
    )
    normalized: dict[str, tuple[str, ...]] = {}
    for key, values in checks.items():
        _require(
            isinstance(values, Sequence) and not isinstance(values, (str, bytes)),
            f"deterministic_checks.{key} must be a list",
        )
        items = tuple(values)
        _require(
            all(isinstance(item, str) and item for item in items),
            f"deterministic_checks.{key} entries must be non-empty strings",
        )
        normalized[key] = items
    computed = rubric_sha256(rubric)
    _require(
        computed == declared,
        f"rubric_sha256 mismatch for {case_id}: declared {declared}, computed {computed}",
    )
    return LiveCase(
        case_id=case_id,
        skill=skill,
        prompt=prompt,
        baseline_prompt=baseline_prompt,
        skill_instructions=skill_instructions,
        rubric=dict(rubric),
        rubric_sha256=declared,
        deterministic_checks=normalized,
        record_sha256=sha256_hex(raw),
        source_path=os.path.basename(os.path.dirname(path)) + "/" + CASE_FILE_NAME,
        raw=dict(payload),
    )


def load_cases(cases_root: str) -> list[LiveCase]:
    """Load every committed case under a dataset root, ordered by case_id."""
    if not os.path.isdir(cases_root):
        raise LiveDatasetError(
            f"cases root not found: {cases_root}", context={"path": cases_root}
        )
    cases: list[LiveCase] = []
    for name in sorted(os.listdir(cases_root)):
        directory = os.path.join(cases_root, name)
        if not os.path.isdir(directory):
            continue
        path = os.path.join(directory, CASE_FILE_NAME)
        if not os.path.isfile(path):
            continue
        cases.append(load_case(path))
    if not cases:
        raise LiveDatasetError(
            f"no committed cases under {cases_root}", context={"path": cases_root}
        )
    ids = [case.case_id for case in cases]
    if len(set(ids)) != len(ids):
        raise LiveDatasetError("duplicate case_id in the committed dataset")
    return sorted(cases, key=lambda case: case.case_id)


def dataset_digest(cases: Sequence[LiveCase]) -> str:
    """Digest of the ordered (case_id, record_sha256) set: binds the dataset."""
    payload = [{"case_id": case.case_id, "sha256": case.record_sha256} for case in cases]
    return sha256_hex(canonical_bytes(payload))


def evaluate_deterministic(case: LiveCase, text: str) -> dict[str, Any]:
    """Deterministic checks FIRST; a semantic judge cannot overrule them."""
    failures: list[dict[str, str]] = []
    checked = 0
    lowered = text.lower()
    for fragment in case.deterministic_checks.get("must_include", ()):
        checked += 1
        if fragment.lower() not in lowered:
            failures.append({"check": "must_include", "fragment": fragment})
    for fragment in case.deterministic_checks.get("must_not_include", ()):
        checked += 1
        if fragment.lower() in lowered:
            failures.append({"check": "must_not_include", "fragment": fragment})
    if checked == 0:
        return {"status": "NOT_APPLICABLE", "checks": 0, "failures": []}
    return {
        "status": "FAIL" if failures else "PASS",
        "checks": checked,
        "failures": failures,
    }
