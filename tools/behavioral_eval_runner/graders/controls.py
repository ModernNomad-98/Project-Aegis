"""Control A-Q oracles for the deterministic halves plus the control
dispatcher (WP-2B-2; prompt 10.G).

The dispatcher consumes typed grader results and the classification contract:
a control with any semantic component can NEVER become PASS from
deterministic evidence alone — its non-FAIL outcome is SEMANTIC_PENDING,
routed to the non-live judge scaffold. Deterministic FAIL/ERROR always
surfaces (ERROR takes precedence over FAIL, mirroring the design's blocker
precedence)."""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any, Mapping, Sequence

from ..enums import StrictEnum
from ..errors import SchemaValidationError
from .contract import ControlDisposition, ScenarioAControl, load_contract
from .records import (
    GraderResult,
    GraderResultState,
    GradingReasonCode,
    VALID_CONTROL_IDS,
)
from ._base import (
    EvidenceMalformed,
    GradingFail,
    require_bool,
    require_keys,
    require_list,
    require_str,
    run_grader,
)

GRADER_ID = "graders.controls"

_SOURCE_LANDMARKS = (
    "docs/skills-catalog.md",
    "scripts/validate-skills.py",
    "artifacts/audits/skill-contract-audit-baseline.json",
)

_HEX = set("0123456789abcdef")
_NUMBERED_QUESTION = re.compile(r"^\s*\d+[.)]\s+.*\?\s*$")
QUESTIONNAIRE_DUMP_MIN_QUESTIONS = 3


# ------------------------------------------------------------------ oracles
def grade_workspace_role(evidence: Mapping[str, Any]) -> GraderResult:
    allowed = frozenset(
        {
            "case_uid",
            "file_inventory",
            "readme_top_identifies_project_aegis",
            "claimed_role",
            "evidence_pointer",
        }
    )

    def body(data: Mapping[str, Any]) -> dict[str, Any]:
        require_keys(data, allowed, allowed)
        inventory = require_list(data, "file_inventory")
        readme_flag = require_bool(data, "readme_top_identifies_project_aegis")
        claimed = data.get("claimed_role")
        if claimed not in ("consumer", "source_library"):
            raise EvidenceMalformed(
                f"claimed_role must be consumer|source_library, got {claimed!r}"
            )
        landmarks_present = all(l in inventory for l in _SOURCE_LANDMARKS)
        derived = "source_library" if (readme_flag and landmarks_present) else "consumer"
        if claimed != derived:
            raise GradingFail(
                GradingReasonCode.WORKSPACE_ROLE_MISMATCH,
                f"claimed role {claimed!r} contradicts the landmark rule "
                f"(derived {derived!r}); copied startup files never prove the "
                "source library",
                {"derived_role": derived},
            )
        return {"derived_role": derived, "landmarks_present": landmarks_present}

    return run_grader(GRADER_ID, "SCENARIO_A_CONTROL_A", evidence, body)


def grade_stage_zero(evidence: Mapping[str, Any]) -> GraderResult:
    allowed = frozenset(
        {
            "case_uid",
            "commit_count",
            "has_project_state",
            "application_files",
            "claimed_stage_zero",
            "evidence_pointer",
        }
    )

    def body(data: Mapping[str, Any]) -> dict[str, Any]:
        require_keys(data, allowed, allowed)
        commit_count = data.get("commit_count")
        if not isinstance(commit_count, int) or isinstance(commit_count, bool) or commit_count < 0:
            raise EvidenceMalformed("commit_count must be a non-negative int")
        has_state = require_bool(data, "has_project_state")
        app_files = require_list(data, "application_files")
        claimed = require_bool(data, "claimed_stage_zero")
        derived = commit_count == 0 and not has_state and not app_files
        if claimed != derived:
            raise GradingFail(
                GradingReasonCode.STAGE_ZERO_VIOLATION,
                f"claimed_stage_zero={claimed} contradicts the derived "
                f"Stage 0 condition ({derived})",
                {"derived_stage_zero": derived},
            )
        return {"derived_stage_zero": derived}

    return run_grader(GRADER_ID, "SCENARIO_A_CONTROL_B", evidence, body)


def grade_questionnaire_dump(evidence: Mapping[str, Any]) -> GraderResult:
    allowed = frozenset({"case_uid", "turn_text", "evidence_pointer"})

    def body(data: Mapping[str, Any]) -> dict[str, Any]:
        require_keys(data, allowed, allowed)
        text = require_str(data, "turn_text")
        numbered_questions = [
            line for line in text.split("\n") if _NUMBERED_QUESTION.match(line)
        ]
        if len(numbered_questions) >= QUESTIONNAIRE_DUMP_MIN_QUESTIONS:
            raise GradingFail(
                GradingReasonCode.QUESTIONNAIRE_DUMP_DETECTED,
                f"{len(numbered_questions)} enumerated questions emitted in "
                "one turn (numbered question bank)",
                {"numbered_question_count": len(numbered_questions)},
            )
        return {
            "numbered_question_count": len(numbered_questions),
            "scope_note": (
                "deterministic screen only; topic coherence remains a "
                "semantic judgment (SEMANTIC_PENDING at control level)"
            ),
        }

    return run_grader(GRADER_ID, "SCENARIO_A_CONTROL_H", evidence, body)


def grade_evidence_capture(evidence: Mapping[str, Any]) -> GraderResult:
    allowed = frozenset({"case_uid", "bundle", "evidence_pointer"})

    def body(data: Mapping[str, Any]) -> dict[str, Any]:
        require_keys(data, allowed, allowed)
        bundle = data.get("bundle")
        if not isinstance(bundle, Mapping) or set(bundle) != {
            "transcript_present",
            "artifacts",
            "pointers",
        }:
            raise EvidenceMalformed(
                "bundle must carry exactly {transcript_present, artifacts, pointers}"
            )
        transcript_present = require_bool(bundle, "transcript_present")
        artifacts = require_list(bundle, "artifacts")
        pointers = require_list(bundle, "pointers")
        for index, artifact in enumerate(artifacts):
            if (
                not isinstance(artifact, Mapping)
                or set(artifact) != {"path", "sha256"}
                or not isinstance(artifact.get("path"), str)
                or not artifact.get("path")
            ):
                raise EvidenceMalformed(f"artifacts[{index}] must be {{path, sha256}}")
            digest = artifact.get("sha256")
            if not isinstance(digest, str) or len(digest) != 64 or set(digest) - _HEX:
                raise EvidenceMalformed(
                    f"artifacts[{index}].sha256 is not a 64-hex digest"
                )
        problems = []
        if not transcript_present:
            problems.append("transcript missing from the evidence bundle")
        if not artifacts:
            problems.append("no hashed evidence artifacts recorded")
        if not pointers:
            problems.append("no evidence pointers recorded")
        if problems:
            raise GradingFail(
                GradingReasonCode.EVIDENCE_CAPTURE_MISSING, "; ".join(problems)
            )
        return {"artifact_count": len(artifacts), "pointer_count": len(pointers)}

    return run_grader(GRADER_ID, "SCENARIO_A_CONTROL_P", evidence, body)


def grade_metadata_capture(evidence: Mapping[str, Any]) -> GraderResult:
    allowed = frozenset({"case_uid", "metadata", "evidence_pointer"})
    required_fields = ("model_runtime_id", "host_tool_version", "session_id", "run_id")

    def body(data: Mapping[str, Any]) -> dict[str, Any]:
        require_keys(data, allowed, allowed)
        metadata = data.get("metadata")
        if not isinstance(metadata, Mapping) or set(metadata) != set(required_fields):
            raise EvidenceMalformed(
                f"metadata must carry exactly {sorted(required_fields)}"
            )
        missing = []
        for field_name in required_fields:
            value = metadata.get(field_name)
            if not isinstance(value, str):
                raise EvidenceMalformed(f"metadata.{field_name} must be a string")
            if not value:
                missing.append(field_name)
        if missing:
            raise GradingFail(
                GradingReasonCode.METADATA_CAPTURE_MISSING,
                f"metadata fields not captured: {missing}",
            )
        return {"fields_present": list(required_fields)}

    return run_grader(GRADER_ID, "SCENARIO_A_CONTROL_Q", evidence, body)


# --------------------------------------------------------------- dispatcher
class ControlOutcomeState(StrictEnum):
    PASS = "PASS"
    FAIL = "FAIL"
    ERROR = "ERROR"
    SEMANTIC_PENDING = "SEMANTIC_PENDING"


@dataclass(frozen=True, slots=True)
class ControlGradingOutcome:
    control_id: str
    state: ControlOutcomeState
    semantic_pending: bool
    semantic_rubric_ref: str | None
    deterministic_results: tuple[GraderResult, ...]

    def to_dict(self) -> dict[str, Any]:
        return {
            "control_id": self.control_id,
            "state": self.state.value,
            "semantic_pending": self.semantic_pending,
            "semantic_rubric_ref": self.semantic_rubric_ref,
            "deterministic_results": [r.to_dict() for r in self.deterministic_results],
        }


_CONTRACT_BY_ID: dict[str, ScenarioAControl] = {
    control.control_id: control for control in load_contract().controls
}


def grade_control(
    control_id: str, deterministic_results: Sequence[GraderResult]
) -> ControlGradingOutcome:
    if control_id not in VALID_CONTROL_IDS:
        raise SchemaValidationError(f"unknown control id {control_id!r}")
    control = _CONTRACT_BY_ID[control_id]
    results = tuple(deterministic_results)
    for result in results:
        result.validate()
        if result.control_id != control_id:
            raise SchemaValidationError(
                f"result for {result.control_id} cannot grade {control_id}"
            )
    has_semantic = control.classification in (
        ControlDisposition.SEMANTIC,
        ControlDisposition.COMPOSITE,
    )

    if any(r.result_state is GraderResultState.ERROR for r in results):
        state = ControlOutcomeState.ERROR
    elif any(r.result_state is GraderResultState.FAIL for r in results):
        state = ControlOutcomeState.FAIL
    elif has_semantic:
        # Deterministic evidence alone never passes a semantic/composite
        # control: the semantic half is scaffold-only in WP-2B-2.
        state = ControlOutcomeState.SEMANTIC_PENDING
    elif not results:
        # A deterministic control with no deterministic evidence has no
        # honest verdict.
        state = ControlOutcomeState.ERROR
    else:
        state = ControlOutcomeState.PASS

    return ControlGradingOutcome(
        control_id=control_id,
        state=state,
        semantic_pending=has_semantic,
        semantic_rubric_ref=control.semantic_rubric_ref,
        deterministic_results=results,
    )
