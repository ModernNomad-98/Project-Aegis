"""Read-only verification of a distributed-payload target against a manifest.

Guarantees enforced here:
  * the target tree is opened read-only; this module contains no write, delete,
    move, rename or chmod operation against the target;
  * the manifest is validated fail-closed before the target is read;
  * findings are reported with relative package paths only and are never
    repaired, deleted or overwritten;
  * an explicit report path must be a regular-file destination outside the
    target and outside the declared package directories; without it nothing is
    written at all;
  * output is deterministic (no timestamps, durations, host names or absolute
    paths) so two runs on identical inputs produce identical bytes.

Exit codes are findings, not authority: 0 clean, 1 findings, 2 usage/invalid/
unsafe input, 3 internal error. The report never contains an approved,
qualified or verdict field.
"""
from __future__ import annotations

import json
import os
import tempfile
from pathlib import Path

from .manifest import (
    ManifestError,
    payload_directory_prefixes,
    sha256_normalized,
    sha256_raw,
    validate_manifest,
)

REPORT_SCHEMA = "aegis.distributed-payload-verify-report/1"
IDENTITY_SCHEMA = "aegis.distributed-payload-manifest-identity/1"

EXIT_CLEAN = 0
EXIT_FINDINGS = 1
EXIT_USAGE = 2
EXIT_INTERNAL = 3

FINDING_CLASSES = ("ABSENT", "CHANGED", "CHANGED_TYPE", "UNRECOGNIZED")


def load_manifest_document(manifest_path: Path) -> tuple[dict, bytes]:
    path = Path(manifest_path)
    try:
        data = path.read_bytes()
    except OSError as exc:
        raise ManifestError("manifest_unreadable", f"cannot read manifest: {exc}") from exc
    try:
        document = json.loads(data.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ManifestError("manifest_invalid_json", f"manifest does not parse: {exc}") from exc
    validate_manifest(document)
    return document, data


def _detect_reparse(path: Path) -> bool:
    if path.is_symlink():
        return True
    is_junction = getattr(os.path, "isjunction", None)
    try:
        return bool(callable(is_junction) and is_junction(path))
    except OSError:
        return False


def _containment_preflight(target: Path) -> list[str]:
    """Refuse unsafe targets; return host limitations that remain UNRUN."""
    limitations = []
    if _detect_reparse(target):
        raise ManifestError("unsafe_target", "target root is a symlink/reparse point; refusing")
    # Check every ancestor of the supplied path (absolute form) and every ancestor of
    # the resolved target, so a relative target reached through a symlinked parent
    # cannot bypass containment preflight.
    for parent in Path(os.path.abspath(str(target))).parents:
        if _detect_reparse(parent):
            raise ManifestError("unsafe_target",
                                "target path chain contains a symlink/reparse point; refusing")
    resolved_target = target.resolve()
    for parent in resolved_target.parents:
        if _detect_reparse(parent):
            raise ManifestError("unsafe_target",
                                "resolved target path chain contains a symlink/reparse point; refusing")
    if not callable(getattr(os.path, "isjunction", None)):
        limitations.append(
            "junction/reparse detection is unavailable on this host (os.path.isjunction absent); "
            "symlink detection only - deep reparse-point containment is UNRUN")
    return limitations


def _entry_parent_reparse(target_root: Path, relative: str):
    """Return the first symlinked/reparse parent component of an entry, else None."""
    current = target_root
    parts = Path(relative).parts
    for part in parts[:-1]:
        current = current / part
        if _detect_reparse(current):
            return current
    return None


def _read_target_file(path: Path) -> bytes:
    with open(path, "rb") as handle:
        return handle.read()


def _plan_report_path(report_out: Path, target: Path, manifest: dict) -> Path:
    resolved = Path(report_out).resolve()
    target_root = target.resolve()
    try:
        resolved.relative_to(target_root)
    except ValueError:
        pass
    else:
        raise ManifestError("unsafe_report_path", "report path must be outside the target root")
    for prefix in payload_directory_prefixes(manifest):
        candidate = (target_root / prefix).resolve()
        try:
            resolved.relative_to(candidate)
        except ValueError:
            continue
        raise ManifestError("unsafe_report_path",
                            "report path must be outside the declared package directories")
    if resolved.exists():
        if not resolved.is_file():
            raise ManifestError("unsafe_report_path", "report destination must be a regular file")
    parent = resolved.parent
    if not parent.is_dir():
        raise ManifestError("unsafe_report_path", "report destination directory does not exist")
    return resolved


def _write_report(report_out: Path, report: dict) -> None:
    data = (json.dumps(report, indent=2, sort_keys=True) + "\n").encode("utf-8")
    handle = tempfile.NamedTemporaryFile(
        prefix=".verify-report-", dir=str(report_out.parent), delete=False)
    temp_path = Path(handle.name)
    try:
        with handle:
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
        temp_path.replace(report_out)
    finally:
        if temp_path.exists():
            temp_path.unlink()


def verify_target(manifest_path: Path, target_root: Path,
                  report_out: Path | None = None) -> tuple[dict, int]:
    """Read-only verification. Returns (report, exit_code)."""
    manifest, manifest_bytes = load_manifest_document(manifest_path)
    target = Path(target_root)
    if not target.exists():
        raise ManifestError("target_missing", "target root does not exist")
    if not target.is_dir():
        raise ManifestError("target_not_directory", "target root is not a directory")
    limitations = _containment_preflight(target)
    if any("mode" in entry for entry in manifest.get("entries", []) if isinstance(entry, dict)):
        limitations.append(
            "declared file mode is accepted in the manifest but mode comparison is not "
            "implemented on this host; mode verification is UNRUN (never checked)")
    planned_report = None
    if report_out is not None:
        planned_report = _plan_report_path(report_out, target, manifest)
        if planned_report == Path(manifest_path).resolve():
            raise ManifestError("unsafe_report_path",
                                "report path must not overwrite the manifest input")
    resolved_manifest = Path(manifest_path).resolve()
    target_root_resolved = target.resolve()
    entry_paths = [entry["path"] for entry in manifest["entries"]]
    entry_set = set(entry_paths)
    try:
        manifest_relative = resolved_manifest.relative_to(target_root_resolved).as_posix()
    except ValueError:
        manifest_relative = None
    if manifest_relative is not None and manifest_relative in entry_set:
        raise ManifestError("manifest_self_reference",
                            "the manifest file lies inside the target and is listed as an entry")

    findings = []
    ok_count = 0
    for entry in manifest["entries"]:
        relative = entry["path"]
        candidate = target / Path(relative)
        if _entry_parent_reparse(target, relative) is not None:
            findings.append({"class": "CHANGED_TYPE", "path": relative,
                             "detail": "target entry path component is a symlink/reparse point (not followed)"})
            continue
        if _detect_reparse(candidate):
            findings.append({"class": "CHANGED_TYPE", "path": relative,
                             "detail": "target entry is a symlink/reparse point (not followed)"})
            continue
        try:
            candidate.resolve().relative_to(target_root_resolved)
        except ValueError as exc:
            raise ManifestError("unsafe_target_entry",
                                "entry path resolves outside the target root", relative) from exc
        if not candidate.exists():
            findings.append({"class": "ABSENT", "path": relative})
            continue
        if not candidate.is_file():
            findings.append({"class": "CHANGED_TYPE", "path": relative,
                             "detail": "target entry is not a regular file"})
            continue
        try:
            payload = _read_target_file(candidate)
        except OSError as exc:
            raise ManifestError("target_unreadable",
                                f"cannot read target entry: {exc}", relative) from exc
        actual = {
            "bytes": len(payload),
            "lf": payload.count(b"\n"),
            "sha256_raw": sha256_raw(payload),
            "sha256_normalized": sha256_normalized(payload),
        }
        differences = {}
        for field, expected_value in (
            ("bytes", entry["bytes"]),
            ("lf", entry["lf"]),
            ("sha256_raw", entry["sha256_raw"]),
            ("sha256_normalized", entry["sha256_normalized"]),
        ):
            if actual[field] != expected_value:
                differences[field] = {"expected": expected_value, "actual": actual[field]}
        if differences:
            findings.append({"class": "CHANGED", "path": relative, "fields": differences})
        else:
            ok_count += 1

    # Unrecognized content inside declared package directories only.
    payload_prefixes = payload_directory_prefixes(manifest)
    # Never claim ownership of the whole target: scan only declared package directories.
    roots = [target / prefix for prefix in payload_prefixes]
    for root in roots:
        if _detect_reparse(root):
            findings.append({"class": "UNRECOGNIZED", "path": root.relative_to(target).as_posix(),
                             "detail": "declared package directory is a symlink/reparse point; not followed"})
            continue
        if not root.is_dir():
            continue
        for dirpath, dirnames, filenames in os.walk(root, followlinks=False):
            dirnames.sort()
            for dirname in list(dirnames):
                directory_path = Path(dirpath) / dirname
                if _detect_reparse(directory_path):
                    try:
                        relative_dir = directory_path.relative_to(target).as_posix()
                    except ValueError:
                        relative_dir = None
                    if relative_dir is not None and relative_dir not in entry_set:
                        findings.append({"class": "UNRECOGNIZED", "path": relative_dir,
                                         "detail": "undeclared directory symlink/reparse point; not followed"})
                    dirnames.remove(dirname)
            for filename in sorted(filenames):
                file_path = Path(dirpath) / filename
                try:
                    relative = file_path.relative_to(target).as_posix()
                except ValueError:
                    continue
                if _detect_reparse(file_path):
                    if relative not in entry_set:
                        findings.append({"class": "UNRECOGNIZED", "path": relative,
                                         "detail": "undeclared symlink/reparse point; not followed"})
                    continue
                if relative in entry_set:
                    continue
                findings.append({"class": "UNRECOGNIZED", "path": relative,
                                 "detail": "not declared in the manifest; reported, never deleted or overwritten"})

    findings.sort(key=lambda finding: (finding["class"], finding["path"]))
    summary = {
        "entries": len(manifest["entries"]),
        "ok": ok_count,
        "absent": sum(1 for finding in findings if finding["class"] == "ABSENT"),
        "changed": sum(1 for finding in findings if finding["class"] == "CHANGED"),
        "changed_type": sum(1 for finding in findings if finding["class"] == "CHANGED_TYPE"),
        "unrecognized": sum(1 for finding in findings if finding["class"] == "UNRECOGNIZED"),
        "findings": len(findings),
    }
    report = {
        "schema": REPORT_SCHEMA,
        "manifest": {"sha256": sha256_raw(manifest_bytes), "bytes": len(manifest_bytes)},
        "package": {"profile_id": manifest["package"]["profile_id"],
                    "profile_version": manifest["package"]["profile_version"]},
        "source": {key: manifest["source"][key] for key in ("repository", "commit", "tree")},
        "source_note": ("source identity is a declared claim recorded from the manifest; optional "
                        "source.note and package.label are untrusted free text and are not emitted "
                        "in this report; verification checks payload bytes only and does not prove "
                        "authorship or approval"),
        "target": ".",
        "mode": "read-only",
        "findings": findings,
        "summary": summary,
        "host_limitations": limitations,
        "repair_available": False,
    }
    if planned_report is not None:
        _write_report(planned_report, report)
    return report, (EXIT_FINDINGS if findings else EXIT_CLEAN)


def check_manifest(manifest_path: Path) -> dict:
    """Validate a manifest and return its detached identity (never acceptance)."""
    document, data = load_manifest_document(manifest_path)
    validate_manifest(document)
    return {
        "schema": IDENTITY_SCHEMA,
        "manifest_schema": document["schema"],
        "bytes": len(data),
        "sha256": sha256_raw(data),
        "package": {key: document["package"][key]
                    for key in ("profile_id", "profile_version")},
        "source": {key: document["source"][key] for key in ("repository", "commit", "tree")},
        "note": ("this is a content identity, not an approval or a proof of authorship; optional "
                 "source.note and package.label free text are untrusted and are not emitted; "
                 "acceptance belongs to a detached binding's consumer"),
    }