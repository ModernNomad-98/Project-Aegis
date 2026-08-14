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
def grade_workspace_role(plan, evidence: Mapping[str, Any]) -> GraderResult:
    allowed = frozenset(
        {
            "file_inventory",
            "readme_top_identifies_project_aegis",
            "claimed_role",
            "evidence_pointer",
        }
    )

    def body(plan_obj, data: Mapping[str, Any]) -> dict[str, Any]:
        require_keys(data, allowed, allowed)
        if plan_obj.expected_workspace_role is None:
            raise SchemaValidationError(
                "the trusted plan must carry expected_workspace_role"
            )
        expected = plan_obj.expected_workspace_role
        inventory = require_list(data, "file_inventory")
        readme_flag = require_bool(data, "readme_top_identifies_project_aegis")
        claimed = data.get("claimed_role")
        if claimed not in ("consumer", "source_library"):
            raise EvidenceMalformed(
                f"claimed_role must be consumer|source_library, got {claimed!r}"
            )
        landmarks_present = all(l in inventory for l in _SOURCE_LANDMARKS)
        derived = "source_library" if (readme_flag and landmarks_present) else "consumer"
        if derived != expected:
            # The observed workspace contradicts the trusted fixture setup:
            # the recording itself is inconsistent — never a verdict.
            raise EvidenceMalformed(
                f"observed landmarks derive role {derived!r} but the trusted "
                f"plan expects {expected!r}; the recording is inconsistent"
            )
        if claimed != expected:
            raise GradingFail(
                GradingReasonCode.WORKSPACE_ROLE_MISMATCH,
                f"claimed role {claimed!r} contradicts the trusted expected "
                f"role {expected!r}; copied startup files never prove the "
                "source library",
                {"derived_role": derived, "expected_role": expected},
            )
        return {
            "derived_role": derived,
            "expected_role": expected,
            "landmarks_present": landmarks_present,
        }

    return run_grader(GRADER_ID, "oracle.controls.workspace_role", plan, evidence, body)


def grade_stage_zero(plan, evidence: Mapping[str, Any]) -> GraderResult:
    allowed = frozenset(
        {
            "commit_count",
            "has_project_state",
            "application_files",
            "claimed_stage_zero",
            "evidence_pointer",
        }
    )

    def body(plan_obj, data: Mapping[str, Any]) -> dict[str, Any]:
        require_keys(data, allowed, allowed)
        if plan_obj.expected_stage_zero is None:
            raise SchemaValidationError(
                "the trusted plan must carry expected_stage_zero"
            )
        expected = plan_obj.expected_stage_zero
        commit_count = data.get("commit_count")
        if not isinstance(commit_count, int) or isinstance(commit_count, bool) or commit_count < 0:
            raise EvidenceMalformed("commit_count must be a non-negative int")
        has_state = require_bool(data, "has_project_state")
        app_files = require_list(data, "application_files")
        claimed = require_bool(data, "claimed_stage_zero")
        derived = commit_count == 0 and not has_state and not app_files
        if derived != expected:
            raise EvidenceMalformed(
                f"observed workspace derives stage-zero={derived} but the "
                f"trusted plan expects {expected}; the recording is inconsistent"
            )
        if claimed != expected:
            raise GradingFail(
                GradingReasonCode.STAGE_ZERO_VIOLATION,
                f"claimed_stage_zero={claimed} contradicts the trusted "
                f"expected Stage 0 condition ({expected})",
                {"derived_stage_zero": derived, "expected_stage_zero": expected},
            )
        return {"derived_stage_zero": derived, "expected_stage_zero": expected}

    return run_grader(GRADER_ID, "oracle.controls.stage_zero", plan, evidence, body)


def grade_questionnaire_dump(plan, evidence: Mapping[str, Any]) -> GraderResult:
    allowed = frozenset({"turn_text", "evidence_pointer"})

    def body(_plan_obj, data: Mapping[str, Any]) -> dict[str, Any]:
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

    return run_grader(
        GRADER_ID, "oracle.controls.questionnaire_dump", plan, evidence, body
    )


def grade_evidence_capture(plan, evidence: Mapping[str, Any]) -> GraderResult:
    allowed = frozenset({"bundle", "evidence_pointer"})

    def body(_plan_obj, data: Mapping[str, Any]) -> dict[str, Any]:
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

    return run_grader(
        GRADER_ID, "oracle.controls.evidence_capture", plan, evidence, body
    )


def grade_metadata_capture(plan, evidence: Mapping[str, Any]) -> GraderResult:
    allowed = frozenset({"metadata", "evidence_pointer"})
    required_fields = ("model_runtime_id", "host_tool_version", "session_id", "run_id")

    def body(_plan_obj, data: Mapping[str, Any]) -> dict[str, Any]:
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

    return run_grader(
        GRADER_ID, "oracle.controls.metadata_capture", plan, evidence, body
    )


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
    contract_sha256: str
    case_uid: str | None
    trusted_grading_plan_sha256: str | None
    required_oracle_ids: tuple[str, ...]
    observed_oracle_ids: tuple[str, ...]
    detail: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "control_id": self.control_id,
            "state": self.state.value,
            "semantic_pending": self.semantic_pending,
            "semantic_rubric_ref": self.semantic_rubric_ref,
            "deterministic_results": [r.to_dict() for r in self.deterministic_results],
            "contract_sha256": self.contract_sha256,
            "case_uid": self.case_uid,
            "trusted_grading_plan_sha256": self.trusted_grading_plan_sha256,
            "required_oracle_ids": list(self.required_oracle_ids),
            "observed_oracle_ids": list(self.observed_oracle_ids),
            "detail": self.detail,
        }


_CONTRACT_BY_ID: dict[str, ScenarioAControl] = {
    control.control_id: control for control in load_contract().controls
}


def grade_control(
    control_id: str, deterministic_results: Sequence[GraderResult]
) -> ControlGradingOutcome:
    """Aggregate one control's deterministic results (R2 §5).

    Enforced: exact control identity, one coherent case, one coherent
    trusted plan, and the COMPLETE required oracle set — exactly once each,
    nothing extra, nothing fabricated. ERROR results take precedence over
    FAIL; FAIL takes precedence over semantic routing; an incomplete,
    duplicated, mixed, or foreign result set is ERROR, never a verdict.
    """
    if control_id not in VALID_CONTROL_IDS:
        raise SchemaValidationError(f"unknown control id {control_id!r}")
    control = _CONTRACT_BY_ID[control_id]
    contract_sha = load_contract().contract_hash()
    results = tuple(deterministic_results)
    required = tuple(control.required_oracle_ids)
    has_semantic = control.classification in (
        ControlDisposition.SEMANTIC,
        ControlDisposition.COMPOSITE,
    )

    problems: list[str] = []
    observed_oracles: list[str] = []
    case_uids: set[str] = set()
    plan_hashes: set[str] = set()
    for result in results:
        result.validate()  # includes output-hash binding
        observed_oracles.append(result.oracle_id)
        case_uids.add(result.case_uid)
        plan_hashes.add(result.input_sha256s["trusted_grading_plan"])
        if result.control_id != control_id:
            problems.append(
                f"result from {result.control_id} cannot grade {control_id}"
            )
    if len(case_uids) > 1:
        problems.append(f"results mix case identities: {sorted(case_uids)}")
    if len(plan_hashes) > 1:
        problems.append("results mix trusted grading plans")
    duplicates = sorted(
        {oracle for oracle in observed_oracles if observed_oracles.count(oracle) > 1}
    )
    if duplicates:
        problems.append(f"duplicate oracle result(s): {duplicates}")
    missing = sorted(set(required) - set(observed_oracles))
    if missing:
        problems.append(f"required oracle(s) missing: {missing}")
    extra = sorted(set(observed_oracles) - set(required))
    if extra:
        problems.append(f"unexpected oracle result(s): {extra}")

    failures = [
        r for r in results if r.result_state is GraderResultState.FAIL
    ]
    errors = [r for r in results if r.result_state is GraderResultState.ERROR]

    if errors:
        state = ControlOutcomeState.ERROR
        detail = "deterministic oracle ERROR: " + "; ".join(
            f"{r.oracle_id}={r.reason_code.value if r.reason_code else '?'}"
            for r in errors
        )
        if problems:
            detail += " | " + "; ".join(problems)
    elif problems:
        state = ControlOutcomeState.ERROR
        detail = "; ".join(problems)
        if failures:
            detail += " | observed FAIL(s): " + "; ".join(
                f"{r.oracle_id}={r.reason_code.value if r.reason_code else '?'}"
                for r in failures
            )
    elif failures:
        state = ControlOutcomeState.FAIL
        detail = "deterministic FAIL: " + "; ".join(
            f"{r.oracle_id}={r.reason_code.value if r.reason_code else '?'}"
            for r in failures
        )
    elif has_semantic:
        # Deterministic evidence alone never passes a semantic/composite
        # control: the semantic half is scaffold-only in WP-2B-2.
        state = ControlOutcomeState.SEMANTIC_PENDING
        detail = "complete deterministic set PASS; semantic component pending"
    elif not required:
        state = ControlOutcomeState.ERROR
        detail = "deterministic control declares no required oracles"
    else:
        state = ControlOutcomeState.PASS
        detail = "complete required oracle set, all PASS"

    return ControlGradingOutcome(
        control_id=control_id,
        state=state,
        semantic_pending=has_semantic,
        semantic_rubric_ref=control.semantic_rubric_ref,
        deterministic_results=results,
        contract_sha256=contract_sha,
        case_uid=next(iter(case_uids)) if len(case_uids) == 1 else None,
        trusted_grading_plan_sha256=(
            next(iter(plan_hashes)) if len(plan_hashes) == 1 else None
        ),
        required_oracle_ids=required,
        observed_oracle_ids=tuple(observed_oracles),
        detail=detail,
    )
