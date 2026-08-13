"""Fail-closed runtime-surface classification (design §5a; prompt Phase 9).

Every file in a shipped skill package gets exactly one classification:

- ``control_plane_only``  — never agent-visible (all of ``evals/**`` categorically,
  every ``evals.json`` / ``trigger-evals.json``, expected-answer data, rubrics,
  case manifests, selection data, result expectations);
- ``runtime_required``    — legitimately part of the agent-visible runtime surface
  (``SKILL.md``, runtime ``references/**``, templates, checklists, examples,
  helper ``scripts/**``, ``assets/**``);
- ``ambiguous_needs_owner_review`` — everything unrecognized; ambiguity FAILS
  CLOSED on the control-plane side and is never agent-visible until a human
  reclassifies it.

No decision is based solely on a file extension: rules combine the directory
context, the file's role inside the package, and its name.
"""

from __future__ import annotations

from dataclasses import dataclass

from .enums import RuntimeClassification
from .errors import ClassificationError

#: Directory names (within a skill package) whose content is runtime material.
_RUNTIME_DIRS = frozenset({"references", "assets", "scripts"})

#: Eval-file names that are categorically control-plane wherever they appear.
_CONTROL_PLANE_FILENAMES = frozenset({"evals.json", "trigger-evals.json"})

#: Name fragments that mark control-plane content (expected answers, rubrics,
#: case manifests, selection data, result expectations) regardless of location.
_CONTROL_PLANE_NAME_FRAGMENTS = (
    "expected-answer",
    "expected_answers",
    "answer-bank",
    "answer_bank",
    "rubric",
    "case-manifest",
    "case_manifest",
    "selection-manifest",
    "selection_manifest",
    "result-expectation",
    "result_expectations",
    "grading-key",
    "grading_key",
)

#: Runtime-shaped document/script suffixes accepted inside runtime dirs. The
#: suffix alone never decides: it only applies to files already inside a
#: recognized runtime directory of a skill package.
_RUNTIME_SUFFIXES = (
    ".md",
    ".txt",
    ".json",
    ".yaml",
    ".yml",
    ".csv",
    ".py",
    ".ps1",
    ".sh",
    ".sql",
    ".html",
    ".css",
    ".js",
    ".ts",
    ".svg",
    ".png",
    ".template",
)


@dataclass(frozen=True, slots=True)
class ClassifiedFile:
    relative_path: str
    classification: RuntimeClassification
    rule: str


def _normalize(relative_path: str) -> tuple[str, ...]:
    if not isinstance(relative_path, str) or not relative_path:
        raise ClassificationError(f"invalid path: {relative_path!r}")
    normalized = relative_path.replace("\\", "/").strip("/")
    parts = tuple(part for part in normalized.split("/") if part)
    if not parts:
        raise ClassificationError(f"empty path: {relative_path!r}")
    for part in parts:
        if part in (".", ".."):
            raise ClassificationError(f"path traversal segment in {relative_path!r}")
    return parts


def classify_skill_file(relative_path: str) -> ClassifiedFile:
    """Classify one file path RELATIVE TO its skill package root.

    Example inputs: ``SKILL.md``, ``evals/evals.json``,
    ``references/blueprint.md``, ``notes/scratch.bin``.
    """
    parts = _normalize(relative_path)
    lower_parts = tuple(part.lower() for part in parts)
    filename = lower_parts[-1]

    # Rule 1: all of evals/** is control-plane, categorically.
    if "evals" in lower_parts[:-1]:
        return ClassifiedFile(
            relative_path,
            RuntimeClassification.CONTROL_PLANE_ONLY,
            "evals-directory-content",
        )

    # Rule 2: eval files are control-plane wherever they appear.
    if filename in _CONTROL_PLANE_FILENAMES:
        return ClassifiedFile(
            relative_path,
            RuntimeClassification.CONTROL_PLANE_ONLY,
            "eval-file-name",
        )

    # Rule 3: expected-answer/rubric/manifest/selection/expectation content is
    # control-plane regardless of directory — matched across the FULL relative
    # path (C4), so `references/rubric/criteria.md` or `assets/answer-bank/x.json`
    # can never leak through a directory name.
    for segment in lower_parts:
        for fragment in _CONTROL_PLANE_NAME_FRAGMENTS:
            if fragment in segment:
                return ClassifiedFile(
                    relative_path,
                    RuntimeClassification.CONTROL_PLANE_ONLY,
                    f"control-plane-path-fragment:{fragment}",
                )

    # Rule 4: SKILL.md at the package root is the runtime entry point.
    if len(parts) == 1 and parts[0] == "SKILL.md":
        return ClassifiedFile(
            relative_path, RuntimeClassification.RUNTIME_REQUIRED, "skill-entry-point"
        )

    # Rule 5: recognized runtime directories carry runtime material, judged by
    # directory role plus a recognized document/script shape (never suffix alone).
    if lower_parts[0] in _RUNTIME_DIRS and len(parts) >= 2:
        if any(filename.endswith(suffix) for suffix in _RUNTIME_SUFFIXES):
            return ClassifiedFile(
                relative_path,
                RuntimeClassification.RUNTIME_REQUIRED,
                f"runtime-directory:{lower_parts[0]}",
            )
        return ClassifiedFile(
            relative_path,
            RuntimeClassification.AMBIGUOUS_NEEDS_OWNER_REVIEW,
            "unrecognized-shape-in-runtime-directory",
        )

    # Fail closed: anything else needs a human decision and is never exposed.
    return ClassifiedFile(
        relative_path,
        RuntimeClassification.AMBIGUOUS_NEEDS_OWNER_REVIEW,
        "unrecognized-supporting-file",
    )


def classify_skill_package(
    relative_paths: list[str] | tuple[str, ...],
) -> list[ClassifiedFile]:
    """Classify every file of one skill package, deterministically ordered."""
    classified = [classify_skill_file(path) for path in relative_paths]
    classified.sort(key=lambda item: item.relative_path)
    return classified


def agent_visible(classification: RuntimeClassification) -> bool:
    """Only ``runtime_required`` files may ever become agent-visible."""
    return classification is RuntimeClassification.RUNTIME_REQUIRED
