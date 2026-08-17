"""WP-2B-3 calibration envelope construction (BER-DEC-008 decision 4; task
section 17).

Produces envelopes of EXACTLY the WP-2B-2 shape — same version, same policy
identity layer, same TRUSTED contract-derived control context, same closed
untrusted-data encoding — so ``validate_request_envelope_binding`` and
``parse_judge_output`` apply unchanged. The input side accepts ONLY the
label-free ``CalibrationItemContent`` projection: expected labels are
structurally unavailable to this builder.
"""

from __future__ import annotations

import base64
from typing import Any, Mapping

from .. import CALIBRATION_SCHEMA_VERSION, GRADING_SCHEMA_VERSION
from ..canonical import sha256_hex_text, sha256_of_obj
from ..errors import SchemaValidationError
from ..graders.contract import load_contract
from . import policy as judge_policy
from . import rubric as judge_rubric
from .calibration_dataset import CalibrationItemContent, calibration_request_id
from .calibration_errors import LabelLeakError
from .calibration_transport import (
    AUTHORIZED_MODEL_SNAPSHOT,
    AUTHORIZED_PROVIDER,
)
from .envelope import ENVELOPE_VERSION, envelope_sha256
from .interface import JudgeIdentity, JudgeRequest

CALIBRATION_JUDGE_ID = "judge.wp2b3.measured-calibration"
CALIBRATION_JUDGE_VERSION = "1.0.0-wp2b3"


def calibration_judge_identity() -> JudgeIdentity:
    """The pinned WP-2B-3 judge identity (model/provider as exact data)."""
    return JudgeIdentity(
        judge_id=CALIBRATION_JUDGE_ID,
        judge_version=CALIBRATION_JUDGE_VERSION,
        model_identifier=AUTHORIZED_MODEL_SNAPSHOT,
        provider_identifier=AUTHORIZED_PROVIDER,
        policy_version=judge_policy.JUDGE_POLICY_VERSION,
        policy_sha256=judge_policy.policy_sha256(),
    )


def calibration_item_manifest(content: CalibrationItemContent) -> dict[str, Any]:
    """The stage-A-equivalent input manifest for ONE calibration item: it
    binds the exact untrusted transcript bytes, never any label."""
    content.validate()
    return {
        "manifest_kind": "aegis_calibration_item_manifest",
        "schema_version": CALIBRATION_SCHEMA_VERSION,
        "item_id": content.item_id,
        "control_id": content.control_id,
        "transcript_sha256": sha256_hex_text(content.transcript),
    }


def build_calibration_envelope(content: CalibrationItemContent) -> dict[str, Any]:
    """Build the canonical judge envelope for one calibration item."""
    if not isinstance(content, CalibrationItemContent):
        raise LabelLeakError(
            "build_calibration_envelope accepts only the label-free "
            "CalibrationItemContent projection (use from_item/from_mapping)"
        )
    content.validate()
    contract = load_contract()
    control = next(
        (c for c in contract.controls if c.control_id == content.control_id),
        None,
    )
    if control is None or control.semantic_rubric_ref is None:
        raise SchemaValidationError(
            f"{content.control_id!r} has no semantic component; no "
            "calibration envelope exists for it"
        )
    rubric = judge_rubric.get_rubric(control.semantic_rubric_ref)
    rubric_hash = judge_rubric.rubric_sha256(rubric)
    return {
        "envelope_kind": "aegis_judge_envelope",
        "envelope_version": ENVELOPE_VERSION,
        "policy_version": judge_policy.JUDGE_POLICY_VERSION,
        "policy_sha256": judge_policy.policy_sha256(),
        "control_context": {
            "control_id": control.control_id,
            "requirement": control.requirement,
            "classification": control.classification.value,
            "semantic_rubric_ref": control.semantic_rubric_ref,
            "contract_version": contract.contract_version,
            "contract_sha256": contract.contract_hash(),
            "owner_signoff_required": control.owner_signoff_required,
            "d9_signoff_state": "PENDING_OWNER_DECISION",
        },
        "rubric": {
            "rubric_id": rubric["rubric_id"],
            "rubric_version": rubric["rubric_version"],
            "rubric_sha256": rubric_hash,
            "question": rubric["question"],
            "pass_criteria": list(rubric["pass_criteria"]),
            "fail_criteria": list(rubric["fail_criteria"]),
        },
        "untrusted_data": {
            "transcript": {
                "encoding": "utf-8",
                "content_b64": base64.b64encode(
                    content.transcript.encode("utf-8")
                ).decode("ascii"),
            }
        },
        "input_manifest_sha256": sha256_of_obj(
            calibration_item_manifest(content)
        ),
    }


def build_calibration_judge_request(
    *,
    content: CalibrationItemContent,
    envelope: Mapping[str, Any],
    dataset_id: str,
    dataset_version: str,
    dataset_sha256: str,
) -> JudgeRequest:
    """Bind one calibration judgment request to EXACTLY this envelope and
    the candidate dataset identity (labels never enter the request)."""
    content.validate()
    rubric = envelope.get("rubric")
    if not isinstance(rubric, Mapping):
        raise SchemaValidationError("envelope has no rubric section")
    request = JudgeRequest(
        request_id=calibration_request_id(content.item_id, dataset_sha256),
        control_id=content.control_id,
        judge=calibration_judge_identity(),
        rubric_id=rubric["rubric_id"],
        rubric_version=rubric["rubric_version"],
        rubric_sha256=rubric["rubric_sha256"],
        envelope_sha256=envelope_sha256(envelope),
        input_manifest_sha256=envelope["input_manifest_sha256"],
        calibration_dataset_id=dataset_id,
        calibration_dataset_version=dataset_version,
        calibration_dataset_sha256=dataset_sha256,
        schema_version=GRADING_SCHEMA_VERSION,
    )
    request.validate()
    return request
