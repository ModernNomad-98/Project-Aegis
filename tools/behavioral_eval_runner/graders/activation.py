"""Typed target and invocation-mode grading over recorded activation
evidence (WP-2B-2; prompt 10.F; design sections 5c, 5d, 6).

- A skill node NEVER satisfies a subagent expectation (and vice versa).
- Invocation mode must be represented explicitly.
- Activation-identifying evidence is a recorded synthetic Tier-1 event, or a
  Tier-2 signature explicitly recorded as promoted WITH its owner-approval
  reference. Unpromoted Tier-2 is corroborating only; Tier-3 prose is never
  activation. Ambiguity yields ERROR / AMBIGUOUS_ACTIVATION — never PASS,
  never FAIL.
- R1 remains UNAVAILABLE/UNKNOWN on the real host: only source
  RECORDED_SYNTHETIC evidence is representable here, and nothing graded here
  is live evidence."""

from __future__ import annotations

from typing import Any, Mapping

from ..enums import InvocationMode, TargetKind
from ..errors import SchemaValidationError, UnknownEnumValueError
from .records import GraderResult, GradingReasonCode
from ._base import EvidenceMalformed, GradingError, GradingFail, require_keys, run_grader

GRADER_ID = "graders.activation"
ORACLE_ID = "oracle.activation.typed_target"

TIER1 = "TIER1_STRUCTURED_EVENT"
TIER2 = "TIER2_OUTPUT_SIGNATURE"
TIER3 = "TIER3_PROSE"
EVIDENCE_TIERS = (TIER1, TIER2, TIER3)

RECORDED_SYNTHETIC = "RECORDED_SYNTHETIC"

#: Observed evidence carries ONLY the recorded activation graph; the
#: expected target is trusted-plan data.
_ALLOWED = frozenset({"observed_nodes", "evidence_pointer"})
_REQUIRED = _ALLOWED
_NODE_ALLOWED_KEYS = frozenset(
    {
        "target_kind",
        "target_name",
        "evidence_tier",
        "invocation_mode",
        "source",
        "tier2_promoted",
        "promotion_ref",
        "children",
        "note",
    }
)


def _ambiguous(kind: str, detail: str) -> GradingError:
    return GradingError(
        GradingReasonCode.AMBIGUOUS_ACTIVATION, detail, {"ambiguity_kind": kind}
    )


def _validate_node(node: Any, path: str) -> dict[str, Any]:
    if not isinstance(node, Mapping):
        raise EvidenceMalformed(f"{path} must be a mapping")
    unknown = set(node) - _NODE_ALLOWED_KEYS
    if unknown:
        raise EvidenceMalformed(f"{path}: unknown keys {sorted(unknown)}")
    try:
        TargetKind.parse(node.get("target_kind"))
    except UnknownEnumValueError as exc:
        raise EvidenceMalformed(f"{path}: {exc}") from exc
    name = node.get("target_name")
    if not isinstance(name, str) or not name:
        raise EvidenceMalformed(f"{path}: target_name required")
    if node.get("evidence_tier") not in EVIDENCE_TIERS:
        raise EvidenceMalformed(
            f"{path}: unknown evidence tier {node.get('evidence_tier')!r}"
        )
    if node.get("source") != RECORDED_SYNTHETIC:
        raise EvidenceMalformed(
            f"{path}: evidence source must be {RECORDED_SYNTHETIC} in this "
            f"non-live phase, got {node.get('source')!r}"
        )
    mode = node.get("invocation_mode")
    if mode is not None:
        try:
            InvocationMode.parse(mode)
        except UnknownEnumValueError as exc:
            raise EvidenceMalformed(f"{path}: {exc}") from exc
    promoted = node.get("tier2_promoted", False)
    if not isinstance(promoted, bool):
        raise EvidenceMalformed(f"{path}: tier2_promoted must be a boolean")
    validated = dict(node)
    children = node.get("children", [])
    if children:
        if not isinstance(children, list):
            raise EvidenceMalformed(f"{path}: children must be a list")
        validated["children"] = [
            _validate_node(child, f"{path}.children[{index}]")
            for index, child in enumerate(children)
        ]
    return validated


def _flatten(nodes: list[dict[str, Any]]) -> list[dict[str, Any]]:
    flat: list[dict[str, Any]] = []
    for node in nodes:
        flat.append(node)
        flat.extend(_flatten(node.get("children", [])))
    return flat


def _is_identifying(node: Mapping[str, Any]) -> bool:
    if node["evidence_tier"] == TIER1:
        return True
    if node["evidence_tier"] == TIER2 and node.get("tier2_promoted", False):
        # Promotion is only real with its owner-approval reference; a bare
        # promoted flag is an ambiguous claim, handled by the caller.
        return bool(node.get("promotion_ref"))
    return False


def grade_activation(plan, evidence: Mapping[str, Any]) -> GraderResult:
    def body(plan_obj, data: Mapping[str, Any]) -> dict[str, Any]:
        require_keys(data, _ALLOWED, _REQUIRED)
        if plan_obj.expected_target is None:
            raise SchemaValidationError(
                "the trusted plan must carry the expected activation target"
            )
        expected_kind = TargetKind.parse(plan_obj.expected_target["target_kind"])
        expected_mode = InvocationMode.parse(
            plan_obj.expected_target["invocation_mode"]
        )
        expected_name = plan_obj.expected_target["target_name"]

        raw_nodes = data.get("observed_nodes")
        if not isinstance(raw_nodes, list):
            raise EvidenceMalformed("observed_nodes must be a list")
        nodes = [
            _validate_node(node, f"observed_nodes[{index}]")
            for index, node in enumerate(raw_nodes)
        ]
        flat = _flatten(nodes)

        for node in flat:
            if (
                node["evidence_tier"] == TIER2
                and node.get("tier2_promoted", False)
                and not node.get("promotion_ref")
            ):
                raise _ambiguous(
                    "unproven_promotion_claim",
                    "a Tier-2 signature claims promotion without its "
                    "owner-approval reference; the claim is not usable",
                )

        identifying = [node for node in flat if _is_identifying(node)]
        if not identifying:
            if flat and all(node["evidence_tier"] == TIER3 for node in flat):
                raise _ambiguous(
                    "prose_only",
                    "only Tier-3 prose evidence exists; prose is a claim, "
                    "never activation-identifying",
                )
            raise _ambiguous(
                "insufficient_evidence",
                "no activation-identifying signal exists (no Tier-1 event, "
                "no promoted Tier-2 signature)",
            )

        for node in identifying:
            if node.get("invocation_mode") is None:
                raise _ambiguous(
                    "mode_unrepresented",
                    f"identifying node {node['target_name']!r} does not "
                    "represent its invocation mode explicitly",
                )

        by_identity: dict[tuple[str, str], set[str]] = {}
        for node in identifying:
            key = (node["target_kind"], node["target_name"])
            by_identity.setdefault(key, set()).add(node["invocation_mode"])
        for key, modes in by_identity.items():
            if len(modes) > 1:
                raise _ambiguous(
                    "conflicting_signals",
                    f"identifying signals for {key} disagree on invocation "
                    f"mode: {sorted(modes)}",
                )

        name_matches = [
            node for node in identifying if node["target_name"] == expected_name
        ]
        if not name_matches:
            raise GradingFail(
                GradingReasonCode.TARGET_NAME_MISMATCH,
                f"no activation-identifying evidence for expected target "
                f"{expected_name!r}",
            )
        full_matches = [
            node
            for node in name_matches
            if node["target_kind"] == expected_kind.value
        ]
        if not full_matches:
            raise GradingFail(
                GradingReasonCode.TARGET_KIND_MISMATCH,
                f"a {name_matches[0]['target_kind']} activation never "
                f"satisfies a {expected_kind.value} expectation, even for the "
                f"same name {expected_name!r}",
            )
        matched = full_matches[0]
        if matched["invocation_mode"] != expected_mode.value:
            raise GradingFail(
                GradingReasonCode.INVOCATION_MODE_MISMATCH,
                f"observed invocation mode {matched['invocation_mode']!r} "
                f"does not satisfy expected {expected_mode.value!r}",
            )
        return {
            "observed_nodes": nodes,
            "matched_node": {
                "target_kind": matched["target_kind"],
                "target_name": matched["target_name"],
                "evidence_tier": matched["evidence_tier"],
                "invocation_mode": matched["invocation_mode"],
            },
            "r1_non_claim": (
                "Recorded synthetic evidence only; R1 real-host activation "
                "observability remains UNAVAILABLE/UNKNOWN"
            ),
        }

    return run_grader(GRADER_ID, ORACLE_ID, plan, evidence, body)
