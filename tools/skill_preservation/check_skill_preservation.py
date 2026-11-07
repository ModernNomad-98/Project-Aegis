#!/usr/bin/env python3
"""Skill-Preservation Guard - deterministic, offline, read-only library-preservation check.

Compares a candidate tree against a frozen, schema-versioned baseline of the shipped skill
library and reports any reduction, hiding or silent degradation. It reports only: it never
repairs, prunes, deletes, installs or writes inside the scanned tree. It is NOT wired into CI
(the separately owner-gated enforcement slice owns wiring).

Verbs
  baseline --tree PATH --out PATH [--source-revision HEX] [--source-tree HEX] [--base-commit HEX]
      Build a schema-versioned baseline JSON from a clean baseline tree. The output path must
      resolve OUTSIDE the scanned tree; the write is atomic (temp file + replace).
  check --baseline PATH --tree PATH [--report PATH] [--json] [--quiet]
      Compare a candidate tree against the baseline. Read-only: nothing under the tree is
      written. Optional --report must resolve outside the tree. BLOCK findings fail the run;
      WARN/INFO/UNRUN findings are reported but do not fail it.

Exit codes
  0  no BLOCK findings (clean, or warnings/info/unrun only)
  1  at least one BLOCK finding
  2  usage or input error; fail closed (missing/malformed baseline, unknown schema version,
     tampered baseline id, missing/empty candidate tree, output/report path inside the tree,
     symlinked baseline or tree path, duplicate/case-colliding baseline paths)
  3  internal error

Determinism: JSON output is sorted, ASCII-escaped and carries no timestamps or host-dependent
values. Standard library only; no network, no subprocess, no credential access.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
import tempfile

TOOL_NAME = "skill-preservation-guard"
TOOL_VERSION = "1"
BASELINE_SCHEMA = "aegis.skill-preservation-baseline/1"
MANIFEST_SCHEMA = "aegis.skills-manifest/1"
MANIFEST_HASH_INPUT = "SKILL.md bytes, CRLF->LF normalized"
MANUAL_ONLY_SENTINEL = "MANUAL-ONLY; never auto-invoke. "
SKILLS_REL = ".claude/skills"
SKILL_MD = "SKILL.md"
CATALOG_REL = "docs/skills-catalog.md"
README_REL = "README.md"
MANIFEST_REL = "tools/skills-manifest.json"
STARTER_REL = "docs/consumer-starter-package.md"
EXCLUDED_DIR_NAMES = frozenset({".git", "__pycache__", ".pytest_cache", ".mypy_cache", ".worktrees", ".aegis-control-plane"})
EXCLUDED_SUFFIXES = (".pyc",)
SKILL_PATH_RE = re.compile(r"\.claude/skills/([a-z0-9][a-z0-9-]*)/([A-Za-z0-9_./-]+)")
STARTER_STARTUP_RE = re.compile(r"\|\s*`?(AGENTS\.md|CLAUDE\.md)`?\s*\|")
REMOVAL_VERB_RE = re.compile(
    r"(^|[/_.-])(uninstall|un-install|prune|garbage[-_]?collect|cleanup|remove)[-_]?(skill|skills|all)?($|[/_.-])",
    re.IGNORECASE,
)
SEVERITY_ORDER = {"BLOCK": 0, "WARN": 1, "INFO": 2, "UNRUN": 3}


# --------------------------------------------------------------------------- hashing / paths
def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def normalized_sha256_file(path: str) -> str:
    with open(path, "rb") as handle:
        data = handle.read()
    return sha256_bytes(data.replace(b"\r\n", b"\n"))


def safe_relpath(path: str, root: str) -> str:
    """Repo-relative POSIX path; surrogate/undecodable characters are escaped deterministically."""
    rel = os.path.relpath(path, root)
    rel = rel.replace(os.sep, "/")
    try:
        return rel.encode("utf-8", "surrogateescape").decode("utf-8", "backslashreplace")
    except Exception:  # pragma: no cover - defensive
        return rel.encode("ascii", "backslashreplace").decode("ascii")


def iter_repo_files(tree: str):
    """Yield sorted repo-relative file paths, skipping VCS/cache directories."""
    collected = []
    for dirpath, dirnames, filenames in os.walk(tree):
        dirnames[:] = sorted(d for d in dirnames if d not in EXCLUDED_DIR_NAMES)
        for name in sorted(filenames):
            if name.endswith(EXCLUDED_SUFFIXES):
                continue
            full = os.path.join(dirpath, name)
            if os.path.islink(full):
                continue
            collected.append(safe_relpath(full, tree))
    collected.sort()
    return collected


def iter_symlinks_under(tree: str, rel_root: str):
    """Return symlink paths under rel_root without following them."""
    root = os.path.join(tree, *rel_root.split("/"))
    found = []
    if not os.path.isdir(root):
        return found
    for dirpath, dirnames, filenames in os.walk(root, followlinks=False):
        for name in sorted(list(dirnames) + list(filenames)):
            full = os.path.join(dirpath, name)
            if os.path.islink(full):
                found.append(safe_relpath(full, tree))
    return sorted(set(found))


def read_text(path: str) -> str:
    with open(path, "r", encoding="utf-8", errors="replace") as handle:
        return handle.read()


def is_within(path: str, root: str) -> bool:
    try:
        return os.path.commonpath([os.path.realpath(path), os.path.realpath(root)]) == os.path.realpath(root)
    except ValueError:
        return False


# --------------------------------------------------------------------------- frontmatter parsing
def split_frontmatter(text: str):
    """Return (frontmatter_text, body) or (None, text); mirrors the validator's fence rule."""
    if not text.startswith("---"):
        return None, text
    lines = text.splitlines()
    if lines and lines[0].strip() != "---":
        return None, text
    for index in range(1, len(lines)):
        if lines[index].strip() == "---":
            return "\n".join(lines[1:index]), "\n".join(lines[index + 1 :])
    return None, text


def _strip_scalar_comment(value: str) -> str:
    """Strip a YAML inline comment outside quoted scalars."""
    quote = None
    for index, char in enumerate(value):
        if quote:
            if char == quote:
                quote = None
        elif char in ("'", '\"'):
            quote = char
        elif char == "#" and (index == 0 or value[index - 1].isspace()):
            return value[:index].rstrip()
    return value.rstrip()


def _strip_scalar_quotes(value: str) -> str:
    """Remove one layer of surrounding quotes from a simple YAML scalar."""
    if len(value) >= 2 and value[0] == value[-1] and value[0] in ("'", '"'):
        inner = value[1:-1]
        if value[0] == "'":
            inner = inner.replace("''", "'")
        return inner
    return value


def parse_skill_frontmatter(text: str) -> dict:
    """Minimal stdlib line parser for the invariants the guard needs (B5). Never raises."""
    record = {
        "parse_ok": False,
        "name": None,
        "description_present": False,
        "sentinel": False,
        "disable_model_invocation": None,
        "unreadable_reason": None,
    }
    try:
        fm_text, _body = split_frontmatter(text)
        if fm_text is None:
            record["unreadable_reason"] = "no frontmatter block"
            return record
        lines = fm_text.splitlines()
        seen: dict = {}
        index = 0
        while index < len(lines):
            line = lines[index]
            match = re.match(r"^[\"']?([A-Za-z0-9_-]+)[\"']?\s*:\s*(.*)$", line)
            if match:
                key, value = match.group(1), match.group(2)
                if key == "description" and value[:1] in (">", "|"):
                    block = [value]
                    index += 1
                    while index < len(lines) and (lines[index].startswith(" ") or not lines[index].strip()):
                        block.append(lines[index])
                        index += 1
                    seen[key] = "\n".join(block).strip()
                    continue
                seen[key] = _strip_scalar_comment(value.strip())
            index += 1
        name_value = seen.get("name")
        if isinstance(name_value, str) and name_value:
            name_value = _strip_scalar_quotes(name_value.strip())
            record["name"] = name_value
            record["parse_ok"] = True
        description = seen.get("description")
        if isinstance(description, str):
            description = _strip_scalar_quotes(description.strip())
        record["description_present"] = bool(isinstance(description, str) and description.strip())
        sentinel_phrase = MANUAL_ONLY_SENTINEL.rstrip()
        record["sentinel"] = bool(
            (isinstance(description, str) and description.startswith(sentinel_phrase))
            or sentinel_phrase in fm_text)
        dmi = seen.get("disable-model-invocation")
        raw_dmi = re.search(
            r"^[\s-]*[\"']?disable-model-invocation[\"']?\s*:\s*([^#\r\n]+)",
            fm_text, re.MULTILINE | re.IGNORECASE)
        if raw_dmi is None:
            raw_dmi = re.search(
                r"[{,]\s*[\"']?disable-model-invocation[\"']?\s*:\s*([^\s,}\]]+)",
                fm_text, re.IGNORECASE)
        if raw_dmi is not None:
            dmi_token = _strip_scalar_quotes(raw_dmi.group(1).strip()).strip().lower()
            if dmi_token in ("true", "false"):
                record["disable_model_invocation"] = dmi_token == "true"
            else:
                record["disable_model_invocation"] = None
                record["parse_ok"] = False
                record["unreadable_reason"] = "unrecognized disable-model-invocation value"
        elif dmi is None:
            record["disable_model_invocation"] = None
        else:
            dmi_token = _strip_scalar_quotes(str(dmi).strip()).strip().lower()
            if dmi_token in ("true", "false"):
                record["disable_model_invocation"] = dmi_token == "true"
            else:
                record["disable_model_invocation"] = None
                record["parse_ok"] = False
                record["unreadable_reason"] = "unrecognized disable-model-invocation value"
        if not record["parse_ok"] and record["unreadable_reason"] is None:
            record["unreadable_reason"] = "name key missing or unquoted frontmatter unclear"
        return record
    except Exception as exc:  # pragma: no cover - defensive; guard must not crash on a tree
        record["unreadable_reason"] = "guard parser error: " + type(exc).__name__
        return record


# --------------------------------------------------------------------------- inventory builders
def skill_dirs(tree: str):
    """Return sorted skill directory absolute paths (symlinked skill dirs are refused by caller)."""
    root = os.path.join(tree, *SKILLS_REL.split("/"))
    if not os.path.isdir(root):
        return None
    dirs = []
    for name in sorted(os.listdir(root)):
        full = os.path.join(root, name)
        if os.path.isdir(full):
            dirs.append(full)
    return dirs


def skill_record(tree: str, skill_dir: str) -> dict:
    files = []
    for dirpath, dirnames, filenames in os.walk(skill_dir):
        dirnames[:] = sorted(d for d in dirnames if d not in EXCLUDED_DIR_NAMES)
        for name in sorted(filenames):
            if name.endswith(EXCLUDED_SUFFIXES):
                continue
            full = os.path.join(dirpath, name)
            if os.path.islink(full):
                continue
            if not os.path.isfile(full):
                raise InputError("non-regular file inside a skill directory: "
                                 + safe_relpath(full, tree))
            files.append({
                "path": safe_relpath(full, tree),
                "bytes": os.path.getsize(full),
                "sha256": sha256_file(full),
            })
    files.sort(key=lambda item: item["path"])
    skill_md_path = os.path.join(skill_dir, SKILL_MD)
    skill_md = None
    frontmatter = {"parse_ok": False, "name": None, "description_present": False,
                   "sentinel": False, "disable_model_invocation": None,
                   "unreadable_reason": "SKILL.md missing"}
    if os.path.isfile(skill_md_path):
        skill_md = {
            "bytes": os.path.getsize(skill_md_path),
            "raw_sha256": sha256_file(skill_md_path),
            "normalized_sha256": normalized_sha256_file(skill_md_path),
        }
        frontmatter = parse_skill_frontmatter(read_text(skill_md_path))
    has_references = any("/references/" in item["path"] for item in files)
    return {
        "files": files,
        "skill_md": skill_md,
        "has_references": has_references,
        "has_evals": os.path.isfile(os.path.join(skill_dir, "evals", "evals.json")),
        "has_trigger_evals": os.path.isfile(os.path.join(skill_dir, "evals", "trigger-evals.json")),
        "frontmatter": frontmatter,
    }


def build_manifest_surface(tree: str) -> dict:
    path = os.path.join(tree, *MANIFEST_REL.split("/"))
    surface = {"present": False, "schema": None, "hash_input": None,
               "source_revision": None, "entries": {}, "error": None}
    if not os.path.isfile(path):
        surface["error"] = "manifest missing"
        return surface
    try:
        payload = json.loads(read_text(path))
        if not isinstance(payload, dict):
            surface["error"] = "manifest is not a JSON object"
            return surface
        entries = payload.get("skills")
        if not isinstance(entries, list):
            surface["error"] = "manifest skills list missing"
            return surface
        surface["present"] = True
        surface["schema"] = payload.get("schema")
        surface["hash_input"] = payload.get("hash_input")
        surface["source_revision"] = payload.get("source_revision")
        for entry in entries:
            if isinstance(entry, dict) and isinstance(entry.get("name"), str):
                surface["entries"][entry["name"]] = {
                    "path": entry.get("path"),
                    "sha256": entry.get("sha256"),
                }
    except (OSError, ValueError) as exc:
        surface["error"] = "manifest unreadable: " + type(exc).__name__
    return surface


def mentions_skill(text: str, name: str) -> bool:
    """Token-bounded mention so a longer skill id cannot mask a shorter one."""
    if not isinstance(text, str) or not isinstance(name, str) or not name:
        return False
    return re.search(r"(?<![A-Za-z0-9-])" + re.escape(name) + r"(?![A-Za-z0-9-])", text) is not None


def build_discovery_surface(tree: str, skill_ids: list) -> dict:
    catalog_path = os.path.join(tree, *CATALOG_REL.split("/"))
    readme_path = os.path.join(tree, *README_REL.split("/"))
    catalog_text = read_text(catalog_path) if os.path.isfile(catalog_path) else ""
    readme_text = read_text(readme_path) if os.path.isfile(readme_path) else ""
    return {
        "catalog_present": os.path.isfile(catalog_path),
        "readme_present": os.path.isfile(readme_path),
        "catalog_mentions": {name: mentions_skill(catalog_text, name) for name in skill_ids},
        "readme_mentions": {name: mentions_skill(readme_text, name) for name in skill_ids},
    }


def build_starter_surface(tree: str) -> dict:
    path = os.path.join(tree, *STARTER_REL.split("/"))
    surface = {"present": False, "parsed": False, "sha256": None,
               "declared_paths": [], "declared_skills": [], "error": None}
    if not os.path.isfile(path):
        surface["error"] = "starter definition missing"
        return surface
    surface["present"] = True
    surface["sha256"] = sha256_file(path)
    try:
        text = read_text(path)
        declared_paths = set()
        declared_skills = set()
        # Only the normative file-table rows declare install files. Prose citations elsewhere in the
        # page (for example a backticked path quoted in a refusal example) are not declared files.
        for line in text.splitlines():
            if not line.lstrip().startswith("|"):
                continue
            for match in SKILL_PATH_RE.finditer(line):
                skill_id, rest = match.group(1), match.group(2)
                declared_skills.add(skill_id)
                declared_paths.add(".claude/skills/%s/%s" % (skill_id, rest.rstrip(".,;:")))
            for match in STARTER_STARTUP_RE.finditer(line):
                declared_paths.add(match.group(1))
        surface["declared_paths"] = sorted(declared_paths)
        surface["declared_skills"] = sorted(declared_skills)
        surface["parsed"] = bool(declared_skills)
        if not surface["parsed"]:
            surface["error"] = "no declared skill paths found in the starter definition table"
    except Exception as exc:  # pragma: no cover - defensive
        surface["error"] = "starter definition unreadable: " + type(exc).__name__
    return surface


def build_baseline(tree: str, source_revision: str = None, source_tree: str = None,
                   base_commit: str = None) -> dict:
    tree = os.path.realpath(tree)
    dirs = skill_dirs(tree)
    if dirs is None:
        raise InputError("candidate tree has no %s directory" % SKILLS_REL)
    if not dirs:
        raise InputError("candidate tree has an empty %s directory" % SKILLS_REL)
    for full in dirs:
        if os.path.islink(full):
            raise InputError("symlinked skill directory refused: " + safe_relpath(full, tree))
    skills = {}
    seen_casefold = {}
    for full in dirs:
        name = os.path.basename(full)
        key = name.casefold()
        if key in seen_casefold:
            raise InputError("case-colliding skill directories refused: %r and %r" %
                             (seen_casefold[key], name))
        seen_casefold[key] = name
        skills[name] = skill_record(tree, full)
    named = sorted(name for name in skills if name != "_template")
    inventory = iter_repo_files(tree)
    inventory_casefold = {}
    for rel in inventory:
        key = rel.casefold()
        if key in inventory_casefold:
            raise InputError("case-colliding repository paths refused: %r and %r" %
                             (inventory_casefold[key], rel))
        inventory_casefold[key] = rel
    manifest_surface = build_manifest_surface(tree)
    discovery = build_discovery_surface(tree, named)
    starter = build_starter_surface(tree)
    if starter["present"]:
        if not starter["parsed"]:
            raise InputError("starter definition present but no declared file-table rows could be read: "
                             + str(starter.get("error")))
        missing_declared = [rel for rel in starter["declared_paths"]
                            if not os.path.isfile(os.path.join(tree, *rel.split("/")))]
        if missing_declared:
            raise InputError("starter definition declares paths that are missing from the baseline tree: "
                             + ", ".join(missing_declared[:5]))
        missing_skills = [skill_id for skill_id in starter["declared_skills"]
                          if not os.path.isdir(os.path.join(tree, SKILLS_REL, skill_id))]
        if missing_skills:
            raise InputError("starter definition declares skills that are missing from the baseline tree: "
                             + ", ".join(missing_skills[:5]))
    counts = {
        "skill_directories": len(dirs),
        "named_skills": len(named),
        "skill_md_files": sum(1 for record in skills.values() if record["skill_md"]),
        "skill_files_total": sum(len(record["files"]) for record in skills.values()),
        "skills_with_references": sum(1 for record in skills.values() if record["has_references"]),
        "skills_with_evals": sum(1 for record in skills.values() if record["has_evals"]),
        "skills_with_trigger_evals": sum(1 for record in skills.values() if record["has_trigger_evals"]),
        "skills_manual_only": sum(1 for record in skills.values()
                                  if record["frontmatter"].get("disable_model_invocation") is True
                                  or record["frontmatter"].get("sentinel")),
        "manifest_entries": len(manifest_surface["entries"]),
        "starter_declared_files": len(starter["declared_paths"]),
        "starter_declared_skills": len(starter["declared_skills"]),
    }
    payload = {
        "schema": BASELINE_SCHEMA,
        "tool": {"name": TOOL_NAME, "version": TOOL_VERSION},
        "generated_from": {
            "source_revision": source_revision,
            "source_tree": source_tree,
            "base_commit": base_commit,
        },
        "contract": {
            "skills_root": SKILLS_REL,
            "skill_md": SKILL_MD,
            "catalog_path": CATALOG_REL,
            "readme_path": README_REL,
            "manifest_path": MANIFEST_REL,
            "manifest_schema": MANIFEST_SCHEMA,
            "manifest_hash_input": MANIFEST_HASH_INPUT,
            "starter_path": STARTER_REL,
            "manual_only_sentinel": MANUAL_ONLY_SENTINEL,
        },
        "counts": counts,
        "skills": skills,
        "discovery": {
            "catalog_present": discovery["catalog_present"],
            "readme_present": discovery["readme_present"],
            "catalog_mentions": discovery["catalog_mentions"],
            "readme_mentions": discovery["readme_mentions"],
            "manifest": {
                "present": manifest_surface["present"],
                "schema": manifest_surface["schema"],
                "hash_input": manifest_surface["hash_input"],
                "source_revision": manifest_surface["source_revision"],
                "entries": manifest_surface["entries"],
                "error": manifest_surface["error"],
            },
        },
        "starter": starter,
        "file_inventory": inventory,
    }
    payload["baseline_id"] = compute_baseline_id(payload)
    return payload


def compute_baseline_id(payload: dict) -> str:
    body = {key: value for key, value in payload.items() if key != "baseline_id"}
    canonical = json.dumps(body, sort_keys=True, ensure_ascii=True, separators=(",", ":"))
    return sha256_bytes(canonical.encode("utf-8"))


# --------------------------------------------------------------------------- errors / findings
class InputError(Exception):
    """Usage or input error -> exit 2 (fail closed)."""


class InternalError(Exception):
    """Internal error -> exit 3."""


def finding(rule: str, severity: str, message: str, subject: str = None) -> dict:
    item = {"rule": rule, "severity": severity, "message": message}
    if subject is not None:
        item["subject"] = subject
    return item


def _is_hex64(value) -> bool:
    return isinstance(value, str) and re.fullmatch(r"[0-9a-f]{64}", value) is not None


def _validate_baseline_skill(name: str, record) -> None:
    if not isinstance(record, dict):
        raise InputError("baseline skill %r is not an object" % name)
    files = record.get("files")
    if not isinstance(files, list):
        raise InputError("baseline skill %r has no file inventory" % name)
    for file_index, item in enumerate(files):
        if not isinstance(item, dict):
            raise InputError("baseline skill %r file entry %d is not an object" % (name, file_index))
        if not isinstance(item.get("path"), str) or not item["path"]:
            raise InputError("baseline skill %r file entry %d has no path" % (name, file_index))
        if isinstance(item.get("bytes"), bool) or not isinstance(item.get("bytes"), int) or item["bytes"] < 0:
            raise InputError("baseline skill %r file entry %d has invalid bytes" % (name, file_index))
        if not _is_hex64(item.get("sha256")):
            raise InputError("baseline skill %r file entry %d has invalid sha256" % (name, file_index))
    skill_md = record.get("skill_md")
    if skill_md is not None:
        if not isinstance(skill_md, dict):
            raise InputError("baseline skill %r skill_md is not an object" % name)
        if isinstance(skill_md.get("bytes"), bool) or not isinstance(skill_md.get("bytes"), int) \
                or skill_md.get("bytes") < 0:
            raise InputError("baseline skill %r skill_md.bytes is invalid" % name)
        if not _is_hex64(skill_md.get("raw_sha256")) or not _is_hex64(skill_md.get("normalized_sha256")):
            raise InputError("baseline skill %r skill_md digests are invalid" % name)
    frontmatter = record.get("frontmatter")
    if frontmatter is not None:
        if not isinstance(frontmatter, dict):
            raise InputError("baseline skill %r frontmatter is not an object" % name)
        if not isinstance(frontmatter.get("parse_ok"), bool):
            raise InputError("baseline skill %r frontmatter.parse_ok is not a boolean" % name)
        if frontmatter.get("name") is not None and not isinstance(frontmatter.get("name"), str):
            raise InputError("baseline skill %r frontmatter.name is invalid" % name)
        if not isinstance(frontmatter.get("description_present"), bool):
            raise InputError("baseline skill %r frontmatter.description_present is invalid" % name)
        if not isinstance(frontmatter.get("sentinel"), bool):
            raise InputError("baseline skill %r frontmatter.sentinel is invalid" % name)
        if frontmatter.get("disable_model_invocation") is not None \
                and not isinstance(frontmatter.get("disable_model_invocation"), bool):
            raise InputError("baseline skill %r frontmatter.disable_model_invocation is invalid" % name)


def validate_baseline(baseline: dict) -> None:
    if not isinstance(baseline, dict):
        raise InputError("baseline is not a JSON object")
    if baseline.get("schema") != BASELINE_SCHEMA:
        raise InputError("unknown baseline schema: %r" % (baseline.get("schema"),))
    recorded_id = baseline.get("baseline_id")
    if not isinstance(recorded_id, str):
        raise InputError("baseline_id missing")
    if compute_baseline_id(baseline) != recorded_id:
        raise InputError("baseline_id mismatch: baseline is malformed or was edited after generation")
    for key in ("contract", "counts", "skills", "discovery", "starter", "file_inventory"):
        if key not in baseline:
            raise InputError("baseline missing required section: %s" % key)
    if not isinstance(baseline["contract"], dict):
        raise InputError("baseline contract section is not an object")
    generated_from = baseline.get("generated_from")
    if generated_from is not None and not isinstance(generated_from, dict):
        raise InputError("baseline generated_from section is not an object")
    if not isinstance(baseline["counts"], dict):
        raise InputError("baseline counts section is not an object")
    if not isinstance(baseline["discovery"], dict):
        raise InputError("baseline discovery section is not an object")
    if not isinstance(baseline["starter"], dict):
        raise InputError("baseline starter section is not an object")
    if not isinstance(baseline["file_inventory"], list):
        raise InputError("baseline file_inventory section is not a list")
    if not isinstance(baseline["skills"], dict) or not baseline["skills"]:
        raise InputError("baseline skills section empty")
    count_names = ("skill_directories", "named_skills", "skill_md_files",
                   "skill_files_total", "manifest_entries")
    for key in count_names:
        value = baseline["counts"].get(key)
        if isinstance(value, bool) or not isinstance(value, int) or value < 0:
            raise InputError("baseline counts.%s is not a non-negative integer" % key)
    for key in ("catalog_mentions", "readme_mentions"):
        value = baseline["discovery"].get(key)
        if not isinstance(value, dict) or not all(
                isinstance(k, str) and isinstance(v, bool) for k, v in value.items()):
            raise InputError("baseline discovery.%s is not an object of booleans" % key)
    manifest_surface = baseline["discovery"].get("manifest")
    if not isinstance(manifest_surface, dict):
        raise InputError("baseline discovery.manifest is not an object")
    if not isinstance(manifest_surface.get("present"), bool):
        raise InputError("baseline discovery.manifest.present is not a boolean")
    if not isinstance(manifest_surface.get("entries"), dict):
        raise InputError("baseline discovery.manifest.entries is not an object")
    for key in ("declared_paths", "declared_skills"):
        value = baseline["starter"].get(key)
        if not isinstance(value, list) or not all(isinstance(item, str) and item for item in value):
            raise InputError("baseline starter.%s is not a list of non-empty strings" % key)
    for key in ("present", "parsed"):
        if not isinstance(baseline["starter"].get(key), bool):
            raise InputError("baseline starter.%s is not a boolean" % key)
    seen_skills = {}
    for name, record in baseline["skills"].items():
        if not isinstance(name, str) or not name:
            raise InputError("baseline skill id is not a non-empty string")
        key = name.casefold()
        if key in seen_skills:
            raise InputError("baseline duplicate/case-colliding skill id: %r and %r" %
                             (seen_skills[key], name))
        seen_skills[key] = name
        _validate_baseline_skill(name, record)
    inventory_seen = set()
    for index, rel in enumerate(baseline["file_inventory"]):
        if not isinstance(rel, str):
            raise InputError("baseline file_inventory entry %d is not a string" % index)
        folded = rel.casefold()
        if folded in inventory_seen:
            raise InputError("baseline duplicate/case-colliding path: %r" % rel)
        inventory_seen.add(folded)


# --------------------------------------------------------------------------- comparison
def compare(baseline: dict, tree: str) -> dict:
    tree = os.path.realpath(tree)
    skills_root = os.path.join(tree, *SKILLS_REL.split("/"))
    if os.path.islink(skills_root) or (
            callable(getattr(os.path, "isjunction", None)) and os.path.isjunction(skills_root)):
        raise InputError("symlinked/junction skill root refused")
    dirs = skill_dirs(tree)
    if dirs is None or not dirs:
        raise InputError("candidate tree has no non-empty %s directory" % SKILLS_REL)
    for full in dirs:
        if os.path.islink(full):
            raise InputError("symlinked skill directory refused: " + safe_relpath(full, tree))
    candidates = {}
    casefold_seen = {}
    case_collisions = []
    for full in dirs:
        name = os.path.basename(full)
        key = name.casefold()
        if key in casefold_seen:
            case_collisions.append((casefold_seen[key], name))
        casefold_seen[key] = name
        candidates[name] = skill_record(tree, full)
    base_skills = baseline["skills"]
    base_named = sorted(name for name in base_skills if name != "_template")
    cand_named = sorted(name for name in candidates if name != "_template")
    findings = []
    unrun = []
    seen_messages = set()

    def add(rule, severity, message, subject=None):
        key = (rule, severity, message, subject or "")
        if key in seen_messages:
            return
        seen_messages.add(key)
        findings.append(finding(rule, severity, message, subject))

    for rel in iter_symlinks_under(tree, SKILLS_REL):
        add("SYMLINK_IN_SKILL_SURFACE", "BLOCK",
            "candidate contains a symlink under the protected skill surface: %r" % rel, rel)
    for rel in iter_symlinks_under(tree, "tools/skill_preservation"):
        if REMOVAL_VERB_RE.search(rel):
            add("CLEANUP_PATH_ADDITION", "BLOCK",
                "candidate contains a removal-looking symlink inside the guard package: %r" % rel, rel)
    if "_template" in base_skills and "_template" not in candidates:
        add("TEMPLATE_DISAPPEARED", "BLOCK",
            "baseline template skill _template is absent from the candidate tree", "_template")
    base_counts = baseline.get("counts") or {}
    if isinstance(base_counts.get("skill_directories"), int) and len(dirs) < base_counts["skill_directories"]:
        add("SKILL_DIRECTORY_COUNT_REDUCED", "BLOCK",
            "candidate has %d skill directories; baseline has %d" % (len(dirs), base_counts["skill_directories"]))

    if "_template" in base_skills and "_template" in candidates:
        base_template_files = {item["path"] for item in base_skills["_template"].get("files", [])
                               if isinstance(item, dict) and isinstance(item.get("path"), str)}
        cand_template_files = {item["path"] for item in candidates["_template"].get("files", [])
                               if isinstance(item, dict) and isinstance(item.get("path"), str)}
        for missing in sorted(base_template_files - cand_template_files):
            add("MISSING_SUPPORTING_FILE", "BLOCK",
                "candidate template skill is missing baseline file: %r" % missing, missing)
        if base_skills["_template"].get("skill_md") and not candidates["_template"].get("skill_md"):
            add("TEMPLATE_SKILL_MD_MISSING", "BLOCK",
                "candidate template skill has no SKILL.md", "_template")

    if case_collisions:
        for first, second in case_collisions:
            add("CASE_COLLIDING_SKILL_DIRS", "BLOCK",
                "candidate tree has case-colliding skill directories: %r and %r; "
                "case-folded availability is ambiguous" % (first, second), first)

    missing_ids = [name for name in base_named if name not in candidates]
    new_ids = [name for name in cand_named if name not in base_skills]
    renamed = []
    for missing in missing_ids:
        missing_record = base_skills[missing]
        missing_hash = (missing_record.get("skill_md") or {}).get("raw_sha256")
        for candidate_id in list(new_ids):
            candidate_hash = (candidates[candidate_id].get("skill_md") or {}).get("raw_sha256")
            if missing_hash and candidate_hash == missing_hash:
                renamed.append((missing, candidate_id))
                add("RENAMED_OR_HIDDEN_SKILL", "BLOCK",
                    "skill %r disappeared but new skill %r has the identical SKILL.md bytes; "
                    "this is an availability-changing rename/hide" % (missing, candidate_id), missing)
                new_ids.remove(candidate_id)
                break
        if not any(missing == item[0] for item in renamed):
            add("DISAPPEARED_SKILL", "BLOCK",
                "baseline skill %r is absent from the candidate tree" % missing, missing)
    for new_id in new_ids:
        add("ADDED_SKILL", "WARN",
            "candidate adds skill %r (additions are allowed; review discovery and packaging)" % new_id,
            new_id)
    for candidate_id in cand_named:
        base_record = base_skills.get(candidate_id)
        if base_record is None:
            continue
        candidate_record = candidates[candidate_id]
        # missing supporting files inside an existing skill
        base_files = {item["path"] for item in base_record.get("files", [])}
        cand_files = {item["path"] for item in candidate_record.get("files", [])}
        for rel in sorted(base_files - cand_files):
            severe = rel.endswith("/" + SKILL_MD) or rel.endswith("/evals/evals.json")
            add("MISSING_SUPPORTING_FILE", "BLOCK",
                "required skill file missing from candidate: %r%s" %
                (rel, " (severe: SKILL.md or evals asset)" if severe else ""), candidate_id)
        for rel in sorted(cand_files - base_files):
            add("ADDED_SKILL_FILE", "INFO",
                "candidate adds a file inside skill %r: %r" % (candidate_id, rel), candidate_id)
        base_md = base_record.get("skill_md") or {}
        cand_md = candidate_record.get("skill_md") or {}
        if base_md and not cand_md:
            add("MISSING_SUPPORTING_FILE", "BLOCK",
                "SKILL.md missing from candidate skill %r" % candidate_id, candidate_id)
        elif base_md and cand_md:
            if base_md.get("raw_sha256") != cand_md.get("raw_sha256"):
                add("SKILL_MD_CHANGED", "INFO",
                    "SKILL.md bytes changed for skill %r (content change; availability unaffected; "
                    "the validator remains the per-tree strictness gate)" % candidate_id, candidate_id)
        base_fm = base_record.get("frontmatter") or {}
        cand_fm = candidate_record.get("frontmatter") or {}
        if not cand_fm.get("parse_ok") and candidate_record.get("skill_md"):
            add("FRONTMATTER_UNREADABLE_BY_GUARD", "WARN",
                "guard cannot parse frontmatter for skill %r (%s); validator is authoritative"
                % (candidate_id, cand_fm.get("unreadable_reason")), candidate_id)
        was_manual = bool(base_fm.get("disable_model_invocation")) or bool(base_fm.get("sentinel"))
        is_manual = bool(cand_fm.get("disable_model_invocation")) or bool(cand_fm.get("sentinel"))
        if not was_manual and is_manual:
            add("SILENT_DISABLE", "BLOCK",
                "previously active skill %r is now manual-only (disable-model-invocation "
                "and/or MANUAL-ONLY sentinel); this silently removes automatic availability"
                % candidate_id, candidate_id)
        if not cand_fm.get("description_present"):
            add("EMPTY_DESCRIPTION", "BLOCK",
                "skill %r has an empty or missing description" % candidate_id, candidate_id)
        if cand_fm.get("name") != candidate_id:
            add("NAME_DIRECTORY_MISMATCH", "BLOCK",
                "skill %r frontmatter name %r does not equal its directory name"
                % (candidate_id, cand_fm.get("name")), candidate_id)
    # discovery surfaces
    discovery = baseline["discovery"]
    named_all = sorted(set(base_named) | set(cand_named))
    cand_catalog_path = os.path.join(tree, *CATALOG_REL.split("/"))
    cand_readme_path = os.path.join(tree, *README_REL.split("/"))
    cand_catalog = read_text(cand_catalog_path) if os.path.isfile(cand_catalog_path) else None
    cand_readme = read_text(cand_readme_path) if os.path.isfile(cand_readme_path) else None
    if discovery.get("catalog_present") and cand_catalog is None:
        add("DISCOVERY_OMISSION_CATALOG", "BLOCK", "docs/skills-catalog.md is missing from the candidate")
    elif cand_catalog is not None:
        for name in base_named:
            if discovery.get("catalog_mentions", {}).get(name) and not mentions_skill(cand_catalog, name):
                add("DISCOVERY_OMISSION_CATALOG", "BLOCK",
                    "skill %r was listed in docs/skills-catalog.md at baseline and is no longer listed"
                    % name, name)
    if discovery.get("readme_present") and cand_readme is None:
        add("DISCOVERY_OMISSION_README", "BLOCK", "README.md is missing from the candidate")
    elif cand_readme is not None:
        for name in base_named:
            if discovery.get("readme_mentions", {}).get(name) and not mentions_skill(cand_readme, name):
                add("DISCOVERY_OMISSION_README", "BLOCK",
                    "skill %r was listed in README.md at baseline and is no longer listed" % name, name)
    base_manifest = discovery.get("manifest") or {}
    cand_manifest = build_manifest_surface(tree)
    if base_manifest.get("present"):
        if not cand_manifest["present"]:
            add("DISCOVERY_OMISSION_MANIFEST", "BLOCK",
                "tools/skills-manifest.json is missing or unreadable in the candidate"
                + (": " + cand_manifest["error"] if cand_manifest["error"] else ""))
        else:
            if cand_manifest["schema"] != base_manifest.get("schema"):
                add("DISCOVERY_SEMANTICS_CHANGED", "BLOCK",
                    "skills manifest schema changed: %r -> %r"
                    % (base_manifest.get("schema"), cand_manifest["schema"]))
            if cand_manifest["hash_input"] != base_manifest.get("hash_input"):
                add("DISCOVERY_SEMANTICS_CHANGED", "BLOCK",
                    "skills manifest hash_input changed without a decision: %r -> %r"
                    % (base_manifest.get("hash_input"), cand_manifest["hash_input"]))
            for name in sorted(base_manifest.get("entries") or {}):
                if name not in cand_manifest["entries"]:
                    add("DISCOVERY_OMISSION_MANIFEST", "BLOCK",
                        "skills manifest entry %r was present at baseline and is missing" % name, name)
            for name in sorted(cand_manifest["entries"]):
                if name not in (base_manifest.get("entries") or {}):
                    add("MANIFEST_ADDED_ENTRY", "WARN",
                        "skills manifest adds entry %r (allowed addition; review packaging)" % name, name)
    # starter / declared installed set (source-side)
    base_starter = baseline.get("starter") or {}
    cand_starter = build_starter_surface(tree)
    if base_starter.get("present") and not cand_starter["present"]:
        add("INSTALLED_SET_REDUCTION", "BLOCK",
            "docs/consumer-starter-package.md is missing from the candidate; the declared "
            "installed set cannot be verified")
    elif base_starter.get("present") and cand_starter["present"]:
        if base_starter.get("sha256") != cand_starter["sha256"]:
            add("STARTER_DEFINITION_CHANGED", "WARN",
                "the consumer starter-package definition changed since baseline; a reviewed "
                "re-pin decision is required (OD-W04-2 baseline-freeze governance)")
        for rel in base_starter.get("declared_paths", []):
            if not os.path.isfile(os.path.join(tree, *rel.split("/"))):
                add("INSTALLED_SET_REDUCTION", "BLOCK",
                    "declared starter-package file is missing from the candidate: %r" % rel)
        for skill_id in base_starter.get("declared_skills", []):
            if skill_id not in candidates:
                add("INSTALLED_SET_REDUCTION", "BLOCK",
                    "declared starter-package skill is missing from the candidate: %r" % skill_id,
                    skill_id)
    unrun.append({
        "item": "consumer install record",
        "reason": "no consumer install-record format or target is authorized; installed-set "
                  "evidence is UNRUN, never PASS (source-side declared set is checked above)",
    })
    # cleanup-path additions (candidate-added paths only, B8; name/path rule, not content scan)
    base_inventory = set(baseline.get("file_inventory") or [])
    cand_inventory = set(iter_repo_files(tree))
    added_paths = sorted(cand_inventory - base_inventory)
    for rel in added_paths:
        if rel.startswith(SKILLS_REL + "/"):
            parts = rel.split("/")
            added_skill_id = parts[2] if len(parts) >= 3 else ""
            if REMOVAL_VERB_RE.search(rel):
                add("CLEANUP_PATH_ADDITION", "BLOCK",
                    "candidate adds a removal-looking path inside the protected skill surface: "
                    "%r" % rel, rel)
                continue
            if added_skill_id in base_skills:
                add("ADDED_PATH_IN_SKILL_SURFACE", "BLOCK",
                    "candidate adds a file inside an existing baseline skill directory: %r" % rel, rel)
                continue
            add("ADDED_SKILL_FILE", "INFO",
                "candidate adds a file inside a newly added skill %r (additions are allowed; "
                "the added-skill WARN covers discovery/packaging review)" % added_skill_id, rel)
            continue
        if REMOVAL_VERB_RE.search(rel):
            if rel.startswith("tools/skill_preservation/") and re.search(
                    r"(skill|skills)", rel, re.IGNORECASE):
                add("CLEANUP_PATH_ADDITION", "BLOCK",
                    "candidate adds a removal-looking path that names skills inside the guard "
                    "package itself (forbidden): %r" % rel, rel)
            else:
                add("CLEANUP_PATH_ADDITION", "WARN",
                    "candidate adds a path whose name matches a removal-verb pattern: %r "
                    "(name/path rule only; review whether a deletion/cleanup capability is being "
                    "introduced)" % rel, rel)
    # summary
    ordering = sorted(findings, key=lambda item: (SEVERITY_ORDER[item["severity"]],
                                                  item["rule"], item.get("subject") or "",
                                                  item["message"]))
    summary = {
        "BLOCK": sum(1 for item in ordering if item["severity"] == "BLOCK"),
        "WARN": sum(1 for item in ordering if item["severity"] == "WARN"),
        "INFO": sum(1 for item in ordering if item["severity"] == "INFO"),
        "UNRUN": len(unrun),
        "findings_total": len(ordering),
        "result": "BLOCK" if any(item["severity"] == "BLOCK" for item in ordering) else "CLEAN",
    }
    observed = {
        "skill_directories": len(candidates),
        "named_skills": len(cand_named),
        "skill_md_files": sum(1 for record in candidates.values() if record["skill_md"]),
        "skill_files_total": sum(len(record["files"]) for record in candidates.values()),
        "skills_with_references": sum(1 for record in candidates.values() if record["has_references"]),
        "skills_with_evals": sum(1 for record in candidates.values() if record["has_evals"]),
        "skills_with_trigger_evals": sum(1 for record in candidates.values() if record["has_trigger_evals"]),
        "manifest_entries": len(cand_manifest["entries"]),
        "catalog_present": cand_catalog is not None,
        "readme_present": cand_readme is not None,
        "candidate_added_paths": len(added_paths),
    }
    return {
        "tool": {"name": TOOL_NAME, "version": TOOL_VERSION},
        "baseline_id": baseline.get("baseline_id"),
        "generated_from": baseline.get("generated_from"),
        "observed": observed,
        "baseline_counts": baseline.get("counts"),
        "findings": ordering,
        "unrun": unrun,
        "summary": summary,
    }


# --------------------------------------------------------------------------- CLI
def atomic_write_bytes(path: str, data: bytes) -> None:
    if os.path.isdir(path):
        raise InputError("output path is an existing directory")
    directory = os.path.dirname(os.path.abspath(path))
    if directory and not os.path.isdir(directory):
        raise InputError("output directory does not exist: " + directory)
    handle = tempfile.NamedTemporaryFile(prefix=".skill-preservation-", dir=directory,
                                         delete=False)
    try:
        with handle:
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(handle.name, path)
    finally:
        if os.path.exists(handle.name):
            try:
                os.unlink(handle.name)
            except OSError:
                pass


def dump_json(payload) -> str:
    return json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=True) + "\n"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="check_skill_preservation.py",
        description="Skill-Preservation Guard: report-only, offline, read-only skill-library "
                    "preservation check (never repairs, prunes or wires CI).",
    )
    sub = parser.add_subparsers(dest="verb", required=True)
    baseline_cmd = sub.add_parser("baseline", help="build a baseline JSON from a clean tree")
    baseline_cmd.add_argument("--tree", required=True, help="clean baseline tree (read-only)")
    baseline_cmd.add_argument("--out", required=True, help="output baseline JSON outside the tree")
    baseline_cmd.add_argument("--source-revision", default=None,
                              help="declared source revision (40 lowercase hex, optional)")
    baseline_cmd.add_argument("--source-tree", default=None, help="declared source tree hash (optional)")
    baseline_cmd.add_argument("--base-commit", default=None, help="local base commit hash (optional)")
    check_cmd = sub.add_parser("check", help="compare a candidate tree against a baseline")
    check_cmd.add_argument("--baseline", required=True, help="baseline JSON path")
    check_cmd.add_argument("--tree", required=True, help="candidate tree to inspect (read-only)")
    check_cmd.add_argument("--report", default=None, help="optional JSON report path outside the tree")
    check_cmd.add_argument("--json", action="store_true", help="emit deterministic JSON to stdout")
    check_cmd.add_argument("--quiet", action="store_true", help="only print the summary line")
    return parser


def run_baseline(args) -> int:
    tree = os.path.realpath(args.tree)
    if not os.path.isdir(tree):
        raise InputError("baseline tree not found: " + args.tree)
    if os.path.islink(args.tree):
        raise InputError("symlinked baseline tree refused")
    out = os.path.realpath(args.out)
    if is_within(out, tree):
        raise InputError("--out must resolve outside the scanned tree")
    if os.path.islink(args.out):
        raise InputError("symlinked --out path refused")
    payload = build_baseline(tree, args.source_revision, args.source_tree, args.base_commit)
    atomic_write_bytes(out, dump_json(payload).encode("utf-8"))
    print("baseline written: %s (%d skills, %d named, %d skill files, %d repo files, baseline_id=%s)" % (
        args.out, payload["counts"]["skill_directories"], payload["counts"]["named_skills"],
        payload["counts"]["skill_files_total"], len(payload["file_inventory"]),
        payload["baseline_id"]))
    return 0


def run_check(args) -> int:
    tree_raw = args.tree
    tree = os.path.realpath(tree_raw)
    if os.path.islink(tree_raw):
        raise InputError("symlinked candidate tree refused")
    if not os.path.isdir(tree):
        raise InputError("candidate tree not found: " + tree_raw)
    baseline_path = os.path.realpath(args.baseline)
    if os.path.islink(args.baseline):
        raise InputError("symlinked baseline path refused")
    if not os.path.isfile(baseline_path):
        raise InputError("baseline not found: " + args.baseline)
    try:
        baseline = json.loads(read_text(baseline_path))
    except ValueError as exc:
        raise InputError("baseline JSON malformed: " + str(exc))
    validate_baseline(baseline)
    report_path = None
    if args.report is not None:
        report_path = os.path.realpath(args.report)
        if is_within(report_path, tree):
            raise InputError("--report must resolve outside the scanned tree")
        if os.path.islink(args.report):
            raise InputError("symlinked --report path refused")
        if os.path.normcase(report_path) == os.path.normcase(baseline_path):
            raise InputError("--report must not overwrite the baseline input")
    report = compare(baseline, tree)
    payload = dump_json(report).encode("utf-8")
    if report_path is not None:
        atomic_write_bytes(report_path, payload)
    if args.json:
        sys.stdout.write(payload.decode("utf-8"))
    elif args.quiet:
        pass
    else:
        print("skill-preservation check: tree=%s" % tree)
        print("baseline_id=%s source_revision=%s" % (
            report["baseline_id"],
            (report["generated_from"] or {}).get("source_revision")))
        observed = report["observed"]
        baseline_counts = report["baseline_counts"] or {}
        print("observed: %d dirs / %d named / %d SKILL.md / %d skill files / manifest %d" % (
            observed["skill_directories"], observed["named_skills"], observed["skill_md_files"],
            observed["skill_files_total"], observed["manifest_entries"]))
        print("baseline: %d dirs / %d named / %d SKILL.md / %d skill files / manifest %d" % (
            baseline_counts.get("skill_directories", -1), baseline_counts.get("named_skills", -1),
            baseline_counts.get("skill_md_files", -1), baseline_counts.get("skill_files_total", -1),
            baseline_counts.get("manifest_entries", -1)))
        for item in report["findings"]:
            print("  %-5s %-32s %s" % (item["severity"], item["rule"], item["message"]))
        for item in report["unrun"]:
            print("  UNRUN %-32s %s" % (item["item"], item["reason"]))
        summary = report["summary"]
        print("SUMMARY: BLOCK=%d WARN=%d INFO=%d UNRUN=%d RESULT=%s" % (
            summary["BLOCK"], summary["WARN"], summary["INFO"], summary["UNRUN"],
            summary["result"]))
    if args.quiet and not args.json:
        summary = report["summary"]
        print("RESULT: %s BLOCK=%d WARN=%d INFO=%d UNRUN=%d" % (
            summary["result"], summary["BLOCK"], summary["WARN"], summary["INFO"],
            summary["UNRUN"]))
    return 1 if report["summary"]["BLOCK"] else 0


def main(argv=None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        if args.verb == "baseline":
            return run_baseline(args)
        if args.verb == "check":
            return run_check(args)
        parser.error("unknown verb: " + str(args.verb))
    except InputError as exc:
        print("ERROR (fail closed, exit 2): " + str(exc), file=sys.stderr)
        return 2
    except InternalError as exc:
        print("ERROR (internal, exit 3): " + str(exc), file=sys.stderr)
        return 3
    except Exception as exc:  # pragma: no cover - defensive: never crash without a deterministic exit
        print("ERROR (internal, exit 3): %s: %s" % (type(exc).__name__, exc), file=sys.stderr)
        return 3
    return 3


if __name__ == "__main__":
    sys.exit(main())
