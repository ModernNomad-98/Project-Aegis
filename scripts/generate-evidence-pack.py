#!/usr/bin/env python3
"""Generate a deterministic pack of mechanical change facts for auditors.

The recurring facts in an evidence trail are mechanical: which commits a change
runs between, which files it touches and how large they are, what the skills
manifest records, and which changed paths match the caller's gate patterns.
This script measures them once and writes them as JSON.

WHAT IT RECORDS
    schema, status, the resolved base and head commits, their merge base,
    each changed path's status/mode/addition and deletion counts and (for
    regular blobs) sha256/bytes/line count, the manifest's working-tree sha256
    and the reused ancestry result, the caller's gate patterns verbatim with
    the paths each matched, and an optional --plan file's sha256/bytes/lines.

SAFETY
    No network, no shell, and no writes except --out. Git runs only as an
    argument list with shell=False and a 60 second timeout; no repository
    hooks or scripts are launched as subprocesses. The manifest ancestry fact
    is produced by importing the repository's scripts/check-manifest-ancestry.py
    in-process and calling check_manifest_ancestry (that module runs its own
    Git calls). Blobs are read as bytes with "git cat-file blob", never
    through a text conversion or textconv. The manifest is only read.

DETERMINISM
    No timestamps, run ids or absolute repository paths are recorded, and the
    output is json.dump(indent=2, sort_keys=True) plus one newline. The same
    inputs produce byte-identical packs.

EXIT CODES
    0 the pack was written, even when the recorded ancestry result is FAIL or
      ERROR (the pack reports facts; it does not gate).
    2 the pack could not be generated: an unresolvable ref, a --head that is
      not the working tree's HEAD, no common ancestor, an invalid gate
      pattern, an unreadable manifest/plan, a refused or unwritable --out, or
      a Git failure. argparse usage errors also exit 2.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import os
import re
import subprocess
import sys
from pathlib import Path

SCHEMA = "aegis.evidence-pack/1"
GIT_TIMEOUT_SECONDS = 60
EXIT_OK = 0
EXIT_ERROR = 2


class PackError(RuntimeError):
    """The pack could not be generated; the message names the cause."""


def _failure(args: tuple[str, ...], proc: subprocess.CompletedProcess) -> str:
    """Render a nonzero Git exit with the stderr Git produced."""
    stderr = proc.stderr or b""
    if isinstance(stderr, bytes):
        stderr = stderr.decode("utf-8", "replace")
    detail = stderr.strip()
    command = "git " + " ".join(args)
    if detail:
        return f"{command} exited {proc.returncode}: {detail}"
    return f"{command} exited {proc.returncode}"


def _run(repo_root: str | Path, args: tuple[str, ...], *, text: bool):
    """Run one Git command against repo_root, without a shell."""
    command = ["git", "-C", str(repo_root), *args]
    kwargs = {
        "capture_output": True,
        "timeout": GIT_TIMEOUT_SECONDS,
        "shell": False,
    }
    if text:
        kwargs.update(text=True, encoding="utf-8", errors="replace")
    try:
        return subprocess.run(command, **kwargs)
    except FileNotFoundError as exc:
        raise PackError("git executable not found") from exc
    except subprocess.TimeoutExpired as exc:
        raise PackError(
            f"git {' '.join(args)} timed out after {GIT_TIMEOUT_SECONDS} seconds"
        ) from exc
    except OSError as exc:
        raise PackError(f"git {' '.join(args)} could not be run: {exc}") from exc


def _git(repo_root: str | Path, *args: str) -> str:
    """Return stdout text, or raise PackError for any failure."""
    proc = _run(repo_root, args, text=True)
    if proc.returncode != 0:
        raise PackError(_failure(args, proc))
    return proc.stdout


def _git_bytes(repo_root: str | Path, *args: str) -> bytes:
    """Return stdout bytes, or raise PackError for any failure."""
    proc = _run(repo_root, args, text=False)
    if proc.returncode != 0:
        raise PackError(_failure(args, proc))
    return proc.stdout


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _line_count(data: bytes) -> int:
    """Count lines without decoding: complete newlines plus a final fragment."""
    if not data:
        return 0
    return data.count(b"\n") + (0 if data.endswith(b"\n") else 1)


def _facts(data: bytes) -> dict[str, object]:
    return {"sha256": _sha256(data), "bytes": len(data), "lines": _line_count(data)}


def _split_nul(stdout: str) -> list[str]:
    fields = stdout.split("\0")
    while fields and fields[-1] == "":
        fields.pop()
    return fields


def _parse_name_status(stdout: str) -> list[tuple[str, str]]:
    """Parse "git diff --name-status -z" pairs of status and path."""
    fields = _split_nul(stdout)
    if len(fields) % 2 != 0:
        raise PackError("unexpected git diff --name-status output")
    return [(fields[i + 1], fields[i]) for i in range(0, len(fields), 2)]


def _parse_numstat(stdout: str) -> dict[str, tuple[int | None, int | None]]:
    """Parse "git diff --numstat -z" records; "-" means binary (null)."""
    counts: dict[str, tuple[int | None, int | None]] = {}
    for record in _split_nul(stdout):
        parts = record.split("\t", 2)
        if len(parts) != 3:
            raise PackError("unexpected git diff --numstat output")
        added, deleted, path = parts
        counts[path] = (
            None if added == "-" else int(added),
            None if deleted == "-" else int(deleted),
        )
    return counts


def _parse_raw(stdout: str) -> dict[str, tuple[str, str]]:
    """Parse "git diff --raw -z": :oldmode newmode oldsha newsha status NUL path."""
    entries: dict[str, tuple[str, str]] = {}
    fields = _split_nul(stdout)
    if len(fields) % 2 != 0:
        raise PackError("unexpected git diff --raw output")
    for index in range(0, len(fields), 2):
        meta, path = fields[index], fields[index + 1]
        if not meta.startswith(":"):
            raise PackError("unexpected git diff --raw record")
        parts = meta[1:].split(" ")
        if len(parts) != 5:
            raise PackError("unexpected git diff --raw metadata")
        old_mode, new_mode, _old_sha, _new_sha, status = parts
        mode = old_mode if status == "D" else new_mode
        entries[path] = (mode, status)
    return entries


def _resolve_commit(repo_root: Path, ref: str) -> str:
    """Resolve one ref to a full commit id, or raise PackError."""
    return _git(repo_root, "rev-parse", "--verify", f"{ref}^{{commit}}").strip()


def _load_ancestry_checker(repo_root: Path):
    """Load the hyphenated ancestry checker by path, never by module name."""
    candidates = [
        repo_root / "scripts" / "check-manifest-ancestry.py",
        Path(__file__).resolve().parent / "check-manifest-ancestry.py",
    ]
    for candidate in candidates:
        if not candidate.is_file():
            continue
        spec = importlib.util.spec_from_file_location(
            "aegis_manifest_ancestry_under_evidence_pack", candidate
        )
        if spec is None or spec.loader is None:
            raise PackError(f"cannot load ancestry checker: {candidate.name}")
        module = importlib.util.module_from_spec(spec)
        try:
            spec.loader.exec_module(module)
        except Exception as exc:  # noqa: BLE001 - surface any load failure
            raise PackError(
                f"cannot load ancestry checker {candidate.name}: {exc}"
            ) from exc
        return module
    raise PackError(
        "ancestry checker not found: scripts/check-manifest-ancestry.py"
    )


def _inside(path: str, root: str) -> bool:
    """True when path is root or below it; case-insensitive on Windows."""
    candidate = os.path.normcase(path)
    resolved_root = os.path.normcase(root).rstrip(os.sep)
    return candidate == resolved_root or candidate.startswith(
        resolved_root + os.sep
    )


def _resolve_output(out: str, repo_root: Path, force: bool) -> str:
    """Resolve and vet --out; it must be outside the repository."""
    target = os.path.realpath(os.path.abspath(out))
    root = os.path.realpath(str(repo_root))
    if _inside(target, root):
        raise PackError("--out must be outside the repository")
    parent = os.path.dirname(target)
    if not os.path.isdir(parent):
        raise PackError(f"output directory does not exist: {parent}")
    if os.path.exists(target):
        if os.path.isdir(target):
            raise PackError(f"--out is a directory: {target}")
        if not force:
            raise PackError("--out already exists; pass --force to replace it")
    return target


def _read_file(path: Path, label: str) -> bytes:
    try:
        return path.read_bytes()
    except OSError as exc:
        raise PackError(f"{label} could not be read: {exc}") from exc


def _changed_entries(
    repo_root: Path, base: str, head: str
) -> list[dict[str, object]]:
    """Measure every path the three-dot diff reports, sorted by path."""
    name_status = _parse_name_status(
        _git(repo_root, "diff", "--name-status", "-z", "--no-renames",
             f"{base}...{head}")
    )
    numstat = _parse_numstat(
        _git(repo_root, "diff", "--numstat", "-z", "--no-renames",
             f"{base}...{head}")
    )
    raw = _parse_raw(
        _git(repo_root, "diff", "--raw", "-z", "--no-renames",
             f"{base}...{head}")
    )

    entries: list[dict[str, object]] = []
    for path, status in sorted(name_status):
        if path not in numstat or path not in raw:
            raise PackError(f"incomplete diff data for path: {path!r}")
        if raw[path][1] != status:
            raise PackError(f"inconsistent diff status for path: {path!r}")
        additions, deletions = numstat[path]
        mode = raw[path][0]
        entry: dict[str, object] = {
            "path": path,
            "status": status,
            "mode": mode,
            "additions": additions,
            "deletions": deletions,
            "sha256": None,
            "bytes": None,
            "lines": None,
        }
        measurable = (
            status not in {"D", "T"}
            and mode in {"100644", "100755"}
        )
        if measurable:
            blob = _git_bytes(repo_root, "cat-file", "blob", f"{head}:{path}")
            entry.update(_facts(blob))
        entries.append(entry)
    return entries


def build_pack(args: argparse.Namespace) -> dict[str, object]:
    """Measure every fact and return the pack object."""
    repo_root = Path(args.repo_root)
    if not repo_root.is_dir():
        raise PackError(f"--repo-root is not a directory: {args.repo_root}")
    _resolve_output(args.out, repo_root, args.force)

    base = _resolve_commit(repo_root, args.base)
    head = _resolve_commit(repo_root, args.head)
    working_head = _git(repo_root, "rev-parse", "HEAD").strip()
    if head != working_head:
        raise PackError(
            "the working tree does not match --head: "
            f"--head resolves to {head}, HEAD is {working_head}"
        )
    merge_base = _git(repo_root, "merge-base", base, head).strip()

    patterns = list(args.gate_pattern or [])
    compiled = []
    for pattern in patterns:
        try:
            compiled.append((pattern, re.compile(pattern)))
        except re.error as exc:
            raise PackError(f"invalid gate pattern {pattern!r}: {exc}") from exc

    changed = _changed_entries(repo_root, base, head)

    matches = [
        {"path": entry["path"], "pattern": pattern}
        for entry in changed
        for pattern, expression in compiled
        if expression.search(str(entry["path"]))
    ]
    matches.sort(key=lambda item: (str(item["path"]), str(item["pattern"])))

    manifest_arg = args.manifest
    manifest_path = Path(manifest_arg)
    if manifest_path.is_absolute():
        raise PackError("manifest path must be relative to the repository root")
    if any(part == ".." for part in manifest_path.parts):
        raise PackError('manifest path must not contain a ".." component')
    manifest_bytes = _read_file(repo_root / manifest_path, "manifest")
    checker = _load_ancestry_checker(repo_root)
    ancestry = checker.check_manifest_ancestry(str(repo_root), args.manifest)
    if not isinstance(ancestry, dict):
        raise PackError("ancestry checker returned an unexpected result")
    manifest = {
        "path": manifest_arg,
        "sha256": _sha256(manifest_bytes),
        "bytes": len(manifest_bytes),
        "ancestry": ancestry,
    }

    plan = None
    if args.plan:
        plan_path = Path(args.plan)
        recorded_plan = args.plan
        if plan_path.is_absolute():
            try:
                recorded_plan = Path(os.path.relpath(
                    os.path.realpath(str(plan_path)),
                    os.path.realpath(str(repo_root)),
                )).as_posix()
            except ValueError as exc:
                raise PackError(
                    "plan path cannot be expressed relative to the "
                    f"repository root: {exc}"
                ) from exc
        else:
            plan_path = repo_root / plan_path
        plan_bytes = _read_file(plan_path, "plan")
        plan = {"path": recorded_plan, **_facts(plan_bytes)}

    return {
        "schema": SCHEMA,
        "status": "OK",
        "base": base,
        "head": head,
        "merge_base": merge_base,
        "changed": changed,
        "gate": {"patterns": patterns, "matches": matches},
        "manifest": manifest,
        "plan": plan,
    }


def write_pack(target: str, pack: dict[str, object]) -> None:
    """Write the pack as deterministic JSON plus one trailing newline."""
    try:
        with open(target, "w", encoding="utf-8", newline="\n") as handle:
            json.dump(pack, handle, indent=2, sort_keys=True)
            handle.write("\n")
    except OSError as exc:
        raise PackError(f"--out could not be written: {exc}") from exc


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Generate a deterministic JSON evidence pack of mechanical facts "
            "for the given base and head commits."
        ),
        epilog=(
            "Facts only: a FAIL/ERROR ancestry result is recorded and the pack "
            "is still written (exit 0). Generation errors exit 2."
        ),
    )
    parser.add_argument("--repo-root", default=".",
                        help="repository root to inspect (default: .)")
    parser.add_argument("--base", required=True,
                        help="base revision; resolved with rev-parse --verify")
    parser.add_argument("--head", default="HEAD",
                        help="head revision; must be the working tree HEAD "
                             "(default: HEAD)")
    parser.add_argument("--manifest", default="tools/skills-manifest.json",
                        help="manifest path relative to --repo-root; an "
                             "absolute path or one containing '..' is "
                             "rejected (default: tools/skills-manifest.json)")
    parser.add_argument("--plan",
                        help="optional plan file, relative to --repo-root, "
                             "to hash as sha256/bytes/lines; an absolute path "
                             "is recorded relative to the repository root")
    parser.add_argument("--gate-pattern", action="append", default=[],
                        metavar="REGEX",
                        help="repeatable regex recorded verbatim; matched "
                             "against each changed path")
    parser.add_argument("--out", required=True,
                        help="output JSON file; must be outside the repository")
    parser.add_argument("--force", action="store_true",
                        help="replace an existing --out file")
    args = parser.parse_args(argv)

    try:
        pack = build_pack(args)
        target = _resolve_output(args.out, Path(args.repo_root), args.force)
        write_pack(target, pack)
    except PackError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return EXIT_ERROR
    except Exception as exc:  # noqa: BLE001 - report, never traceback
        detail = " ".join(str(exc).split()) or "no detail"
        print(
            f"ERROR: unexpected {type(exc).__name__}: {detail}",
            file=sys.stderr,
        )
        return EXIT_ERROR
    return EXIT_OK


if __name__ == "__main__":
    sys.exit(main())
