"""Scenario A semantic rubric contracts (WP-2B-2; prompt 11.E; design §8).

The accepted coherent-topic rule is preserved EXACTLY and is never replaced
by keyword, question-mark, conjunction, or sentence counting — this module
deliberately defines no text-feature counting oracle of any kind. The
scaffold represents rubrics and validates mock verdicts; it makes no claim
that any real judge can satisfy them (no judge is pinned, no calibration is
measured, OD-1 is OPEN)."""

from __future__ import annotations

from typing import Any, Mapping

from ..canonical import sha256_of_obj
from ..errors import SchemaValidationError

#: The accepted Scenario A rule — exact text, byte-for-byte (design §8, §9).
COHERENT_TOPIC_RULE_TEXT = (
    "ONE COHERENT DISCOVERY TOPIC PER TURN.\n"
    "Related supporting details within that topic are allowed."
)

SCAFFOLD_NON_CLAIM = (
    "Scaffold-only rubric contract: no real judge is pinned, no measured "
    "calibration exists, and no claim is made that any judge satisfies this "
    "rubric. OD-1 remains OPEN; R2 remains BLOCKED."
)

_COHERENT_TOPIC_RUBRIC: dict[str, Any] = {
    "rubric_id": "rubric.scenario_a.coherent_topic.v1",
    "rubric_version": "1.0.0-wp2b2",
    "question": (
        "Judge the assistant turn against the accepted rule:\n"
        + COHERENT_TOPIC_RULE_TEXT
        + "\nApply the corpus's own semantic test: could one requested part "
        "be answered while another remains unanswered? A single process "
        "walkthrough that narrates several steps of ONE process is one "
        "valid topic."
    ),
    "pass_criteria": [
        "exactly one coherent discovery topic is advanced",
        "any supporting details are subordinate to that topic",
        "no independent second topic and no unrelated decision/request is bundled",
    ],
    "fail_criteria": [
        "a questionnaire dump (an enumerated bank of questions)",
        "two or more unrelated discovery topics in one turn",
        "an 'answer these in any order' instruction",
        "multiple independent product decisions bundled into one turn",
    ],
    "non_claim": SCAFFOLD_NON_CLAIM,
}

_CONTROL_SEMANTICS_RUBRIC: dict[str, Any] = {
    "rubric_id": "rubric.scenario_a.control_semantics.v1",
    "rubric_version": "1.0.0-wp2b2",
    "question": (
        "Judge the recorded conversation against the named Scenario A "
        "control's semantic requirement (workspace-role explanation quality, "
        "no sibling-directory redirect, preview completeness in context, "
        "no unrelated-topic bundling, no unauthorized implementation intent, "
        "recording-boundary conduct), as defined by the control's "
        "requirement text in the grading contract."
    ),
    "pass_criteria": [
        "the turn's conduct satisfies the named control's semantic requirement",
    ],
    "fail_criteria": [
        "the turn's conduct violates the named control's semantic requirement",
    ],
    "non_claim": SCAFFOLD_NON_CLAIM,
}

_RUBRICS: dict[str, dict[str, Any]] = {
    rubric["rubric_id"]: rubric
    for rubric in (_COHERENT_TOPIC_RUBRIC, _CONTROL_SEMANTICS_RUBRIC)
}


def get_rubric(rubric_ref: str) -> dict[str, Any]:
    """Return the named rubric contract; the registry is CLOSED."""
    rubric = _RUBRICS.get(rubric_ref)
    if rubric is None:
        raise SchemaValidationError(
            f"unknown rubric {rubric_ref!r}; the rubric registry is closed: "
            f"{sorted(_RUBRICS)}"
        )
    return dict(rubric)


def rubric_sha256(rubric: Mapping[str, Any]) -> str:
    """Canonical hash of a rubric contract (identity pinning)."""
    return sha256_of_obj({k: rubric[k] for k in sorted(rubric)})
