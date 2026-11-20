#!/usr/bin/env python3
"""Manual pre-push check: is the manifest source revision an ancestor of HEAD?

This is a MANUAL pre-push check. It is NOT a git hook and is NOT a CI gate:
nothing runs it automatically. Run it by hand before pushing:

    python -P scripts/check-manifest-ancestry.py
    python -P scripts/check-manifest-ancestry.py --json

WHAT IT PROVES
    tools/skills-manifest.json records, in "source_revision", the commit whose
    skill content the manifest hashes describe. This checker proves whether
    that commit is an ancestor of the repository's current HEAD. PASS means
    git merge-base --is-ancestor <source_revision> HEAD exited 0.

    It does not prove that the manifest hashes still match the working tree;
    that is a separate check. It answers only the provenance question: is the
    recorded revision part of this branch's history?

EXIT CODES
    0 PASS: source_revision is an ancestor of HEAD.
    1 FAIL: source_revision is not an ancestor of HEAD, or is not a commit in
      this repository.
    2 ERROR: the question could not be answered - a missing, unreadable or
      invalid manifest; an invalid source_revision; an unresolvable HEAD; a
      git failure; or shallow history. argparse usage errors also exit 2.

SHALLOW HISTORY
    A shallow clone cannot prove ancestry: a revision absent from truncated
    history is indistinguishable from one that never existed. The checker
    therefore reports ERROR, never PASS or FAIL, when Git reports
    rev-parse --is-shallow-repository as true.

SAFETY
    No network, no shell, no writes. Git is invoked as an argument list with
    shell=False; the manifest is only read. Only exit 0 from
    git merge-base --is-ancestor can produce PASS.
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

ZERO_REVISION = "0" * 40
REVISION_RE = re.compile(r"^[0-9a-f]{40}$")
MANIFEST_SCHEMA = "aegis.skills-manifest/1"

GIT_TIMEOUT_SECONDS = 30
EXIT_PASS = 0
EXIT_FAIL = 1
EXIT_ERROR = 2


class AncestryError(RuntimeError):
    """Git could not be started, or did not finish, for a reason we surface.

    A nonzero Git exit is normally data for this checker: cat-file and
    merge-base use their exit status to answer the question. This exception
    is reserved for the cases where no answer exists at all (missing executable,
    timeout, or another operating-system error).
    """


def _git(repo_root: Path, *args: str) -> subprocess.CompletedProcess[str]:
    """Run one Git command against repo_root, without a shell."""
    try:
        return subprocess.run(
            ["git", "-C", str(repo_root), *args],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=GIT_TIMEOUT_SECONDS,
            shell=False,
        )
    except FileNotFoundError as exc:
        raise AncestryError("git executable not found") from exc
    except subprocess.TimeoutExpired as exc:
        raise AncestryError(
            f"git {' '.join(args)} timed out after {GIT_TIMEOUT_SECONDS} seconds"
        ) from exc
    except OSError as exc:
        raise AncestryError(f"git {' '.join(args)} could not be run: {exc}") from exc


def _result(
    status: str,
    *,
    reason: str,
    source_revision: str | None = None,
    head: str | None = None,
) -> dict[str, object]:
    """Build the one result shape every caller receives."""
    return {
        "status": status,
        "source_revision": source_revision,
        "head": head,
        "reason": reason,
    }


def _git_detail(proc: subprocess.CompletedProcess[str]) -> str:
    """Return the most useful short detail from a failed Git call."""
    detail = (proc.stderr or proc.stdout or "").strip()
    return detail[:400]


def check_manifest_ancestry(
    repo_root: str | Path,
    manifest: str = "tools/skills-manifest.json",
) -> dict[str, object]:
    """Return PASS, FAIL or ERROR for the manifest's recorded revision.

    repo_root is resolved first. manifest must be relative to that root and
    must not contain a ".." component. Every early failure is ERROR: the
    checker never reports FAIL for a question it could not ask.
    """
    root = Path(repo_root).resolve()

    manifest_path = Path(manifest)
    if manifest_path.is_absolute():
        return _result(
            "ERROR",
            reason="manifest path must be relative to the repository root",
        )
    if any(part == ".." for part in manifest_path.parts):
        return _result(
            "ERROR",
            reason='manifest path must not contain a ".." component',
        )

    path = root / manifest_path
    if not path.is_file():
        return _result(
            "ERROR",
            reason=f"manifest file not found: {manifest}",
        )
    try:
        raw = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as exc:
        return _result(
            "ERROR",
            reason=f"manifest file is not readable as UTF-8: {exc}",
        )

    try:
        data = json.loads(raw)
    except json.JSONDecodeError as exc:
        return _result("ERROR", reason=f"manifest is not valid JSON: {exc}")
    if not isinstance(data, dict):
        return _result("ERROR", reason="manifest root must be a JSON object")
    if data.get("schema") != MANIFEST_SCHEMA:
        return _result(
            "ERROR",
            reason=f"manifest schema must be {MANIFEST_SCHEMA!r}",
        )

    revision = data.get("source_revision")
    if not isinstance(revision, str):
        return _result("ERROR", reason="source_revision must be a string")
    if REVISION_RE.fullmatch(revision) is None:
        return _result(
            "ERROR",
            source_revision=revision,
            reason="source_revision must be 40 lowercase hexadecimal characters",
        )
    if revision == ZERO_REVISION:
        return _result(
            "ERROR",
            source_revision=revision,
            reason="source_revision must not be all zeros",
        )

    try:
        head_proc = _git(root, "rev-parse", "HEAD")
    except AncestryError as exc:
        return _result("ERROR", source_revision=revision, reason=str(exc))
    if head_proc.returncode != 0:
        detail = _git_detail(head_proc)
        reason = "cannot resolve HEAD"
        if detail:
            reason = f"{reason}: {detail}"
        return _result("ERROR", source_revision=revision, reason=reason)
    head = head_proc.stdout.strip()

    try:
        shallow_proc = _git(root, "rev-parse", "--is-shallow-repository")
    except AncestryError as exc:
        return _result(
            "ERROR",
            source_revision=revision,
            head=head,
            reason=str(exc),
        )
    if shallow_proc.returncode != 0:
        detail = _git_detail(shallow_proc)
        reason = "cannot determine whether history is shallow"
        if detail:
            reason = f"{reason}: {detail}"
        return _result(
            "ERROR",
            source_revision=revision,
            head=head,
            reason=reason,
        )
    if shallow_proc.stdout.strip() == "true":
        return _result(
            "ERROR",
            source_revision=revision,
            head=head,
            reason="history is shallow; ancestry cannot be proven",
        )

    try:
        commit_proc = _git(root, "cat-file", "-e", f"{revision}^{{commit}}")
    except AncestryError as exc:
        return _result(
            "ERROR",
            source_revision=revision,
            head=head,
            reason=str(exc),
        )
    if commit_proc.returncode != 0:
        return _result(
            "FAIL",
            source_revision=revision,
            head=head,
            reason="source_revision is not a commit in this repository",
        )

    try:
        ancestry_proc = _git(root, "merge-base", "--is-ancestor", revision, "HEAD")
    except AncestryError as exc:
        return _result(
            "ERROR",
            source_revision=revision,
            head=head,
            reason=str(exc),
        )
    if ancestry_proc.returncode == 0:
        return _result(
            "PASS",
            source_revision=revision,
            head=head,
            reason="source_revision is an ancestor of HEAD",
        )
    if ancestry_proc.returncode == 1:
        return _result(
            "FAIL",
            source_revision=revision,
            head=head,
            reason="source_revision is not an ancestor of HEAD",
        )
    detail = _git_detail(ancestry_proc)
    reason = f"git merge-base exited {ancestry_proc.returncode}"
    if detail:
        reason = f"{reason}: {detail}"
    return _result(
        "ERROR",
        source_revision=revision,
        head=head,
        reason=reason,
    )


def _human_line(result: dict[str, object]) -> str:
    """Render one readable line from a result dict."""
    fields = [str(result["status"])]
    if result["source_revision"]:
        fields.append(f"source_revision={result['source_revision']}")
    if result["head"]:
        fields.append(f"head={result['head']}")
    return " ".join(fields) + ": " + str(result["reason"])


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Manually check that the skills manifest source_revision is an "
            "ancestor of HEAD."
        ),
        epilog=(
            "Manual pre-push check; no git hook and no CI gate. "
            "Exit 0 PASS, 1 FAIL, 2 ERROR."
        ),
    )
    parser.add_argument(
        "--repo-root",
        default=".",
        help="repository root to inspect (default: .)",
    )
    parser.add_argument(
        "--manifest",
        default="tools/skills-manifest.json",
        help=(
            "manifest path relative to --repo-root "
            "(default: tools/skills-manifest.json)"
        ),
    )
    parser.add_argument(
        "--json",
        dest="as_json",
        action="store_true",
        help="print the result as JSON instead of one human-readable line",
    )
    args = parser.parse_args(argv)

    result = check_manifest_ancestry(args.repo_root, args.manifest)
    if args.as_json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print(_human_line(result))

    status = str(result["status"])
    if status == "PASS":
        return EXIT_PASS
    if status == "FAIL":
        return EXIT_FAIL
    return EXIT_ERROR


if __name__ == "__main__":
    sys.exit(main())
