"""Distributed-payload manifest contract and deterministic builder.

Schema: aegis.distributed-payload-manifest/1 (see docs/design/distributed-payload-manifest-v1.md).

Design rules this module enforces:
  * raw on-disk bytes are the authoritative identity; a CRLF->LF normalized
    digest is recorded as a diagnostic only and never proves raw-byte identity;
  * the manifest never carries its own hash (no manifest_identity field); a
    detached binding records manifest identity instead;
  * serialization is deterministic (UTF-8 without BOM, LF only, two-space
    indent, sort_keys, one trailing LF) and independent of enumeration order;
  * path, dependency and schema validation fails closed before any write.

This module writes nothing itself except through write_manifest_atomic(), which
is used only for the explicit --out path supplied by the operator.
"""
from __future__ import annotations

import hashlib
import json
import os
import re
import tempfile
from pathlib import Path

SCHEMA = "aegis.distributed-payload-manifest/1"
BINDING_SCHEMA = "aegis.distributed-payload-binding/1"
TOOL_NAME = "aegis-distributed-payload"
TOOL_VERSION = "1.0.0"

HASH_CONTRACT = {
    "path_encoding": "UTF-8, POSIX '/' separators, relative, no leading './'",
    "sort": "ordinal byte order of the UTF-8 path",
    "bytes": "decimal count of on-disk file bytes",
    "lf": "decimal count of 0x0A bytes",
    "raw_sha256": "SHA-256 over exact on-disk bytes, line endings included",
    "normalized_sha256": "SHA-256 over bytes with every CRLF replaced by LF; this is the only normalization",
    "equality_rule": ("raw equality is authoritative; normalized equality is diagnostic and "
                      "never proves raw-byte identity"),
}

DEPENDENCY_CLASSES = ("required", "conditional", "optional", "maintainer-only")

TOP_LEVEL_FIELDS = (
    "schema", "package", "source", "hash_contract", "entries", "dependencies",
    "generator", "host_configuration",
)

HEX40_RE = re.compile(r"^[0-9a-f]{40}$")
HEX64_RE = re.compile(r"^[0-9a-f]{64}$")
PROFILE_ID_RE = re.compile(r"^[a-z0-9][a-z0-9._-]{0,63}$")
PROFILE_VERSION_RE = re.compile(r"^[A-Za-z0-9._-]{1,64}$")
REPOSITORY_RE = re.compile(r"^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$")


class ManifestError(ValueError):
    """Fail-closed validation error with a stable code for diagnostics."""

    def __init__(self, code: str, message: str, path: str | None = None):
        self.code = code
        self.path = path
        detail = f"{code}: {message}"
        if path is not None:
            detail = f"{code} [{path}]: {message}"
        super().__init__(detail)


def sha256_raw(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_normalized(data: bytes) -> str:
    return hashlib.sha256(data.replace(b"\r\n", b"\n")).hexdigest()


def count_lf(data: bytes) -> int:
    return data.count(b"\n")


def validate_payload_path(path: str) -> None:
    """Validate one POSIX relative payload path or raise ManifestError."""
    if not isinstance(path, str) or path == "":
        raise ManifestError("empty_path", "path must be a non-empty string")
    if "\\" in path:
        raise ManifestError("backslash_path", "paths must use '/' separators", path)
    if path.startswith("/"):
        raise ManifestError("absolute_path", "absolute paths are not allowed", path)
    if re.match(r"^[A-Za-z]:", path):
        raise ManifestError("drive_letter_path", "drive-letter paths are not allowed", path)
    if path.startswith("//") or path.startswith("\\\\"):
        raise ManifestError("unc_path", "UNC paths are not allowed", path)
    if "\x00" in path:
        raise ManifestError("nul_character", "NUL characters are not allowed", path)
    if any(ord(character) < 32 or ord(character) == 127 for character in path):
        raise ManifestError("control_character", "control characters are not allowed", path)
    segments = path.split("/")
    if any(segment == "" for segment in segments):
        raise ManifestError("empty_segment", "empty path segment (relative form)", path)
    if any(segment in (".", "..") for segment in segments):
        raise ManifestError("dot_segment", "'.' or '..' segments are not allowed", path)
    for segment in segments:
        if ":" in segment:
            raise ManifestError("alternate_data_stream",
                                "':' alternate-data-stream segments are not allowed", path)
        if segment.endswith(".") or segment.endswith(" "):
            raise ManifestError("trailing_dot_or_space",
                                "Windows-normalized trailing dot/space segments are not allowed", path)
        stem = segment.split(".", 1)[0].upper()
        if stem in WINDOWS_RESERVED_NAMES:
            raise ManifestError("windows_reserved_name",
                                "Windows reserved device names are not allowed", path)


def payload_directory_prefixes(manifest: dict) -> list[str]:
    """Top-level directories containing at least one payload entry (for scope)."""
    prefixes = set()
    for entry in manifest.get("entries", []):
        parts = entry["path"].split("/")
        if len(parts) > 1:
            prefixes.add(parts[0])
    return sorted(prefixes)


WINDOWS_RESERVED_NAMES = frozenset(
    ["CON", "PRN", "AUX", "NUL", "CLOCK$", "CONIN$", "CONOUT$"]
    + ["COM%d" % number for number in range(1, 10)]
    + ["LPT%d" % number for number in range(1, 10)]
)


def _is_reparse_point(path: Path) -> bool:
    try:
        if path.is_symlink():
            return True
        is_junction = getattr(os.path, "isjunction", None)
        if callable(is_junction) and is_junction(path):
            return True
    except OSError:
        return False
    return False


def _reject_symlink(path: Path, relative: str) -> None:
    if _is_reparse_point(path):
        kind = "symlink_payload" if path.is_symlink() else "reparse_point"
        raise ManifestError(kind, "symlinks and junction/reparse points are not supported in v1", relative)
    try:
        stat_result = path.stat()
    except OSError as exc:
        raise ManifestError("unreadable_file", f"cannot stat file: {exc}", relative) from exc
    if not (os.path.isfile(path)):
        raise ManifestError("unexpected_file_type", "only regular files are supported in v1", relative)
    if getattr(stat_result, "st_nlink", 1) > 1:
        raise ManifestError("hard_link", "hard-linked payload files are not supported in v1", relative)


def collect_entries(payload_root: Path) -> list[dict]:
    """Walk payload_root and return sorted, validated entries."""
    original_root = Path(payload_root)
    if _is_reparse_point(original_root):
        kind = "symlink_payload" if original_root.is_symlink() else "reparse_point"
        raise ManifestError(kind, "payload root symlinks and junction/reparse points are not supported in v1")
    root = payload_root.resolve()
    if not root.is_dir():
        raise ManifestError("payload_root", f"payload root is not a directory: {payload_root}")
    collected = []
    seen = {}
    for dirpath, dirnames, filenames in os.walk(root, followlinks=False):
        dirnames.sort()
        for dirname in list(dirnames):
            directory_path = Path(dirpath) / dirname
            if _is_reparse_point(directory_path):
                relative_dir = directory_path.relative_to(root).as_posix()
                kind = "symlink_payload" if directory_path.is_symlink() else "reparse_point"
                raise ManifestError(kind, "directory symlinks and junction/reparse points are not supported in v1", relative_dir)
        for filename in sorted(filenames):
            file_path = Path(dirpath) / filename
            relative = file_path.relative_to(root).as_posix()
            validate_payload_path(relative)
            _reject_symlink(file_path, relative)
            try:
                data = file_path.read_bytes()
            except OSError as exc:
                raise ManifestError("unreadable_file", f"cannot read file: {exc}", relative) from exc
            folded = relative.casefold()
            if folded in seen:
                raise ManifestError(
                    "duplicate_path",
                    f"case-insensitive collision with '{seen[folded]}'", relative)
            seen[folded] = relative
            collected.append({
                "path": relative,
                "type": "file",
                "bytes": len(data),
                "lf": count_lf(data),
                "sha256_raw": sha256_raw(data),
                "sha256_normalized": sha256_normalized(data),
            })
    collected.sort(key=lambda entry: entry["path"].encode("utf-8"))
    return collected


def load_source_identity(source_path: Path) -> dict:
    """Load and validate a declared source identity JSON file."""
    try:
        source = json.loads(source_path.read_text(encoding="utf-8"))
    except OSError as exc:
        raise ManifestError("source_unreadable", f"cannot read source JSON: {exc}") from exc
    except UnicodeDecodeError as exc:
        raise ManifestError("source_encoding", f"source JSON is not valid UTF-8: {exc}") from exc
    except json.JSONDecodeError as exc:
        raise ManifestError("source_invalid_json", f"source JSON does not parse: {exc}") from exc
    if not isinstance(source, dict):
        raise ManifestError("source_invalid", "source JSON must be an object")
    allowed = {"repository", "commit", "tree", "note"}
    extra = sorted(set(source) - allowed)
    if extra:
        raise ManifestError("source_unknown_field", f"unknown source field(s): {', '.join(extra)}")
    repository = source.get("repository")
    if not isinstance(repository, str) or not REPOSITORY_RE.match(repository):
        raise ManifestError("source_repository", "repository must be owner/name form")
    commit = source.get("commit")
    if not isinstance(commit, str) or not HEX40_RE.match(commit):
        raise ManifestError("source_commit", "commit must be 40 lowercase hex characters")
    tree = source.get("tree")
    if not isinstance(tree, str) or not HEX40_RE.match(tree):
        raise ManifestError("source_tree", "tree must be 40 lowercase hex characters")
    note = source.get("note")
    if note is not None and not isinstance(note, str):
        raise ManifestError("source_note", "note must be a string when present")
    result = {"repository": repository, "commit": commit, "tree": tree}
    if note:
        result["note"] = note
    return result


def _validate_package(package) -> None:
    if not isinstance(package, dict):
        raise ManifestError("package_invalid", "package must be an object")
    extra = sorted(set(package) - {"profile_id", "profile_version", "label"})
    if extra:
        raise ManifestError("package_unknown_field", f"unknown package field(s): {', '.join(extra)}")
    profile_id = package.get("profile_id")
    if not isinstance(profile_id, str) or not PROFILE_ID_RE.match(profile_id):
        raise ManifestError("package_profile_id",
                            "profile_id must be 1-64 lowercase ASCII identifier characters")
    profile_version = package.get("profile_version")
    if not isinstance(profile_version, str) or not PROFILE_VERSION_RE.match(profile_version):
        raise ManifestError("package_profile_version",
                            "profile_version must be 1-64 letters/digits/./_/- characters")
    label = package.get("label")
    if label is not None and (not isinstance(label, str) or not label.strip()):
        raise ManifestError("package_label", "label must be a non-empty string when present")


def _validate_source(source) -> None:
    if not isinstance(source, dict):
        raise ManifestError("source_invalid", "source must be an object")
    extra = sorted(set(source) - {"repository", "commit", "tree", "note"})
    if extra:
        raise ManifestError("source_unknown_field", f"unknown source field(s): {', '.join(extra)}")
    if not isinstance(source.get("repository"), str) or not REPOSITORY_RE.match(source["repository"]):
        raise ManifestError("source_repository", "repository must be owner/name form")
    for key in ("commit", "tree"):
        value = source.get(key)
        if not isinstance(value, str) or not HEX40_RE.match(value):
            raise ManifestError("source_" + key, f"{key} must be 40 lowercase hex characters")
    if "note" in source and not isinstance(source["note"], str):
        raise ManifestError("source_note", "note must be a string when present")


def _validate_hash_contract(hash_contract) -> None:
    if not isinstance(hash_contract, dict):
        raise ManifestError("hash_contract_invalid", "hash_contract must be an object")
    if hash_contract != HASH_CONTRACT:
        raise ManifestError("hash_contract_mismatch",
                            "hash_contract must exactly match the documented v1 contract")


def _validate_entry(entry, position: int) -> None:
    if not isinstance(entry, dict):
        raise ManifestError("entry_invalid", f"entry {position} must be an object")
    allowed = {"path", "type", "bytes", "lf", "sha256_raw", "sha256_normalized", "mode"}
    extra = sorted(set(entry) - allowed)
    if extra:
        raise ManifestError("entry_unknown_field", f"unknown entry field(s): {', '.join(extra)}")
    path = entry.get("path")
    validate_payload_path(path)
    if entry.get("type") != "file":
        raise ManifestError("entry_type", "v1 supports only type 'file'", path)
    for key in ("bytes", "lf"):
        value = entry.get(key)
        if not isinstance(value, int) or isinstance(value, bool) or value < 0:
            raise ManifestError("entry_" + key, f"{key} must be a non-negative integer", path)
    if entry["lf"] > entry["bytes"]:
        raise ManifestError("entry_lf", "lf count cannot exceed byte count", path)
    for key in ("sha256_raw", "sha256_normalized"):
        value = entry.get(key)
        if not isinstance(value, str) or not HEX64_RE.match(value):
            raise ManifestError("entry_digest", f"{key} must be 64 lowercase hex characters", path)
    if "mode" in entry and not re.match(r"^[0-7]{6}$", str(entry["mode"])):
        raise ManifestError("entry_mode", "mode must be a 6-character POSIX mode string", path)


def _validate_dependencies(dependencies, entry_paths: set[str]) -> None:
    if not isinstance(dependencies, list):
        raise ManifestError("dependencies_invalid", "dependencies must be an array")
    for position, dependency in enumerate(dependencies):
        if not isinstance(dependency, dict):
            raise ManifestError("dependency_invalid", f"dependency {position} must be an object")
        allowed = {"from", "to", "class", "rule"}
        extra = sorted(set(dependency) - allowed)
        if extra:
            raise ManifestError("dependency_unknown_field",
                                f"unknown dependency field(s): {', '.join(extra)}")
        source_path = dependency.get("from")
        target_path = dependency.get("to")
        dependency_class = dependency.get("class")
        if not isinstance(source_path, str) or not isinstance(target_path, str):
            raise ManifestError("dependency_invalid", "from/to must be strings")
        if dependency_class not in DEPENDENCY_CLASSES:
            raise ManifestError("dependency_class", "unknown dependency class", source_path)
        if "rule" in dependency and dependency_class != "conditional":
            raise ManifestError("dependency_unexpected_rule",
                                "rule is allowed only for conditional dependencies", source_path)
        if dependency_class == "conditional":
            rule = dependency.get("rule")
            if not isinstance(rule, str) or not rule.strip():
                raise ManifestError("dependency_missing_rule",
                                    "conditional dependency requires a named activation rule",
                                    source_path)
        if source_path not in entry_paths:
            raise ManifestError("dependency_from_missing",
                                "dependency 'from' must be a payload entry path", source_path)
        if dependency_class != "maintainer-only" and target_path not in entry_paths:
            raise ManifestError("dependency_target_missing",
                                "declared dependency target is not a payload entry path "
                                "(required/conditional/optional edges must resolve inside entries)",
                                target_path)


def _validate_generator(generator) -> None:
    if not isinstance(generator, dict):
        raise ManifestError("generator_invalid", "generator must be an object")
    extra = sorted(set(generator) - {"tool", "version"})
    if extra:
        raise ManifestError("generator_unknown_field", f"unknown generator field(s): {', '.join(extra)}")
    if not isinstance(generator.get("tool"), str) or not generator["tool"].strip():
        raise ManifestError("generator_tool", "generator.tool must be a non-empty string")
    if not isinstance(generator.get("version"), str) or not generator["version"].strip():
        raise ManifestError("generator_version", "generator.version must be a non-empty string")


def _validate_host_configuration(host_configuration) -> None:
    if not isinstance(host_configuration, dict):
        raise ManifestError("host_configuration_invalid", "host_configuration must be an object")
    extra = sorted(set(host_configuration) - {"digest", "note"})
    if extra:
        raise ManifestError("host_configuration_unknown_field",
                            f"unknown host_configuration field(s): {', '.join(extra)}")
    digest = host_configuration.get("digest")
    if not isinstance(digest, str) or not HEX64_RE.match(digest):
        raise ManifestError("host_configuration_digest",
                            "host_configuration.digest must be 64 lowercase hex characters")
    if "note" in host_configuration and not isinstance(host_configuration["note"], str):
        raise ManifestError("host_configuration_note", "note must be a string when present")


def validate_manifest(manifest: dict) -> dict:
    """Fail-closed validation of a parsed manifest document (no filesystem reads)."""
    if not isinstance(manifest, dict):
        raise ManifestError("manifest_invalid", "manifest must be a JSON object")
    if "manifest_identity" in manifest:
        raise ManifestError("manifest_self_reference",
                            "a manifest must not carry its own identity; use a detached binding")
    extra = sorted(set(manifest) - set(TOP_LEVEL_FIELDS))
    if extra:
        raise ManifestError("manifest_unknown_field",
                            f"unknown top-level field(s): {', '.join(extra)}")
    missing = [field for field in ("schema", "package", "source", "hash_contract",
                                   "entries", "dependencies", "generator") if field not in manifest]
    if missing:
        raise ManifestError("manifest_missing_field", f"missing required field(s): {', '.join(missing)}")
    if manifest.get("schema") != SCHEMA:
        raise ManifestError("schema_unsupported",
                            f"schema must be exactly '{SCHEMA}'")
    _validate_package(manifest["package"])
    _validate_source(manifest["source"])
    _validate_hash_contract(manifest["hash_contract"])
    entries = manifest["entries"]
    if not isinstance(entries, list):
        raise ManifestError("entries_invalid", "entries must be an array")
    entry_paths = set()
    last_key = None
    for position, entry in enumerate(entries):
        _validate_entry(entry, position)
        path = entry["path"]
        if path in entry_paths:
            raise ManifestError("duplicate_path", "duplicate entry path", path)
        folded = path.casefold()
        if any(existing.casefold() == folded for existing in entry_paths):
            raise ManifestError("duplicate_path", "case-insensitive duplicate entry path", path)
        entry_paths.add(path)
        sort_key = path.encode("utf-8")
        if last_key is not None and sort_key <= last_key:
            raise ManifestError("entries_not_sorted",
                                "entries must be sorted by ordinal UTF-8 path bytes", path)
        last_key = sort_key
    _validate_dependencies(manifest["dependencies"], entry_paths)
    _validate_generator(manifest["generator"])
    if "host_configuration" in manifest:
        _validate_host_configuration(manifest["host_configuration"])
    return manifest


def build_manifest(payload_root: Path, package_id: str, package_version: str,
                   source: dict, label: str | None = None,
                   dependencies: list | None = None) -> dict:
    """Build a validated manifest document for a payload tree.

    dependencies is an optional array of dependency edges using the documented
    schema contract ({from, to, class[, rule]}); it is validated by
    validate_manifest against the collected entry paths.
    """
    for value, pattern, field in (
        (package_id, PROFILE_ID_RE, "package id"),
        (package_version, PROFILE_VERSION_RE, "package version"),
    ):
        if not isinstance(value, str) or not pattern.match(value):
            raise ManifestError("package_invalid", f"invalid {field}: {value!r}")
    entries = collect_entries(payload_root)
    package = {"profile_id": package_id, "profile_version": package_version}
    if label is not None:
        if not isinstance(label, str) or not label.strip():
            raise ManifestError("package_label", "label must be a non-empty string")
        package["label"] = label
    manifest = {
        "schema": SCHEMA,
        "package": package,
        "source": source,
        "hash_contract": dict(HASH_CONTRACT),
        "entries": entries,
        "dependencies": [] if dependencies is None else dependencies,
        "generator": {"tool": TOOL_NAME, "version": TOOL_VERSION},
    }
    return validate_manifest(manifest)


def serialize_manifest(manifest: dict) -> bytes:
    """Deterministic LF JSON bytes for a validated manifest."""
    text = json.dumps(manifest, indent=2, sort_keys=True, ensure_ascii=False)
    return (text + "\n").encode("utf-8")


def write_manifest_atomic(manifest: dict, out_path: Path) -> Path:
    """Write a validated manifest to out_path atomically (temp file + os.replace)."""
    data = serialize_manifest(manifest)
    validate_manifest(manifest)
    target = Path(out_path)
    parent = target.parent
    if not parent.exists():
        raise ManifestError("out_parent_missing", f"output directory does not exist: {parent}")
    descriptor, temp_name = tempfile.mkstemp(prefix=".manifest-", suffix=".tmp", dir=parent)
    try:
        with os.fdopen(descriptor, "wb") as handle:
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temp_name, target)
    except BaseException:
        try:
            os.unlink(temp_name)
        except OSError:
            pass
        raise
    return target


def manifest_identity(manifest_path: Path) -> dict:
    """Detached identity of a manifest file (never embedded inside the manifest)."""
    data = Path(manifest_path).read_bytes()
    return {"schema": SCHEMA, "bytes": len(data), "sha256": sha256_raw(data)}


def create_binding(manifest_path: Path, source: dict, verify_command: str,
                   verify_exit_code: int, evidence_utc: str) -> dict:
    """Detached binding over manifest identity + source claim + verify outcome.

    Acyclic by construction: it references the manifest, never the reverse, and
    it never references an artifact that contains it.
    """
    identity = manifest_identity(manifest_path)
    manifest = json.loads(Path(manifest_path).read_text(encoding="utf-8"))
    validate_manifest(manifest)
    manifest_source = manifest.get("source")
    if not isinstance(manifest_source, dict):
        raise ManifestError("binding_source_mismatch",
                            "manifest source is missing or not an object")
    if dict(source) != manifest_source:
        raise ManifestError("binding_source_mismatch",
                            "binding source must equal the manifest source")
    return {
        "schema": BINDING_SCHEMA,
        "manifest": {"path": Path(manifest_path).name, "bytes": identity["bytes"],
                     "sha256": identity["sha256"]},
        "source": dict(manifest_source),
        "generator": {"tool": TOOL_NAME, "version": TOOL_VERSION},
        "verify": {"command": verify_command, "exit_code": int(verify_exit_code)},
        "evidence_utc": evidence_utc,
    }
