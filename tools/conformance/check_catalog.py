#!/usr/bin/env python3
"""Deterministic read-only checker for the Aegis requirements-to-evidence conformance catalog.

Purpose: validate docs/conformance/requirements.v1.json by standard-library structural validation
that matches the normative schema (no JSON-Schema engine is loaded; the schema file is normative
documentation and a drift test checks selected constants), resolve every requirement/mechanism/
evidence anchor against the captured source bytes, enforce and report the first-profile completeness
rule (declared range and observed count), and (optionally) check an evidence binding for
non-circular, exact-head-bound claims. It reports only. It never repairs, writes inside the repository, executes catalog/evidence
text or treats any string as a command.

CLI
  python tools/conformance/check_catalog.py --catalog docs/conformance/requirements.v1.json
      [--evidence PATH] [--profile PROFILE_ID] [--json] [--out PATH] [--quiet]

Exit codes
  0  clean (structurally valid catalog, all anchors resolve, completeness satisfied)
  1  findings (see finding codes; no finding ever renders as a passing result)
  2  usage/input error: missing or unreadable input, unsupported catalog major, input over the
     declared caps, unsafe/refused --out path
  3  internal error

Determinism: findings sorted by (code, path, record_id, evidence); JSON sort_keys=True; no
timestamps, hostnames, usernames or absolute home paths; two runs on identical inputs are
byte-identical. Standard library only: argparse, hashlib, json, os, pathlib, re, sys.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
import tempfile
from pathlib import Path

TOOL_NAME = "aegis-conformance-catalog-checker"
TOOL_VERSION = "1"
REPORT_SCHEMA = "aegis.conformance-report/1"
EVIDENCE_SCHEMA = "aegis.evidence-binding/1"
CATALOG_SCHEMA = "aegis.conformance-catalog/1"
SUPPORTED_MAJOR = 1
MAX_CATALOG_BYTES = 512 * 1024
MAX_EVIDENCE_BYTES = 1024 * 1024
MAX_REQUIREMENTS = 500
MAX_EVIDENCE_RECORDS = 1000
MAX_STRING = 2000

SEED_FAMILIES = {
    "F1": ["SD-A", "SD-B", "SD-C", "SD-D", "SD-E", "SD-F", "SD-G"],
    "F2": ["MG1", "MG2", "MG3", "MG4", "MG5"],
    "F3": ["AEGIS-REQ-PRES-01"],
    "F4": ["AEGIS-REQ-SKILL-01", "AEGIS-REQ-SKILL-02", "AEGIS-REQ-SKILL-03",
           "AEGIS-REQ-SKILL-04", "AEGIS-REQ-SKILL-05", "AEGIS-REQ-SKILL-06"],
    "F5": ["AEGIS-REQ-MECH-01", "AEGIS-REQ-MECH-02"],
    "F6": ["AEGIS-REQ-EVID-01", "AEGIS-REQ-EVID-02"],
}
SEED_IDS = [item for family in SEED_FAMILIES.values() for item in family]


def enum_value(value, allowed):
    """Membership helper that treats non-string values as invalid, never crashes."""
    return isinstance(value, str) and value in allowed
DECLARED_COUNT_MIN = 23
DECLARED_COUNT_MAX = 27
FIRST_PROFILE = "source-library-change"

ID_RE = re.compile(r"^(?:SD-[A-G]|MG[1-5]|AEGIS-REQ-[A-Z0-9]{2,8}-[0-9]{2})$")
SEMVER_RE = re.compile(r"^([0-9]+)\.([0-9]+)\.([0-9]+)$")
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
GIT_SHA_RE = re.compile(r"^[0-9a-f]{40}$")
PROFILE_RE = re.compile(r"^[a-z0-9][a-z0-9-]{1,40}$")
REL_PATH_RE = re.compile(r"^[A-Za-z0-9_.-]+(?:/[A-Za-z0-9_.-]+)*$")
AC_RE = re.compile(r"^AC-[0-9]{2}$")

MECH_KINDS = {"machine-check", "independent-review", "manual-attestation", "procedural-none"}
VERIF_METHODS = {"deterministic-check", "independent-review", "execution-evidence",
                 "manual-attestation", "none"}
EVID_KINDS = {"console-log", "json-record", "review-verdict", "artifact-digest",
              "host-observation", "none"}
REASON_CODES = {"production-only", "outside-first-profile-scope", "not-yet-enforced",
                "host-specific"}
ANCHOR_KINDS = {"heading", "line-span", "symbol"}
ID_KINDS = {"existing-authoritative", "catalog-minted"}
CLASSIFICATIONS = {"EXECUTED", "PLANNED-UNRUN", "UNRUN"}
FORBIDDEN_KEYS = {"status", "observed", "pass", "result", "evidence_status", "authority",
                  "approval", "permission", "granted", "self_sha256", "self_digest",
                  "own_sha256", "binding_sha256", "catalog_sha256"}
EVIDENCE_PRESENT = "EVIDENCE-PRESENT"
NO_EVIDENCE = "NO-EVIDENCE"
UNRUN_LISTED = "UNRUN-LISTED"
LIMITS_SENTENCE = ("Structural checks do not establish semantic correctness, behavioural "
                   "efficacy, live-host behaviour or authority.")


class InputError(Exception):
    """Usage or input error -> exit 2."""


class InternalError(Exception):
    """Internal error -> exit 3."""


class UnsupportedMajor(InputError):
    """Refused catalog major -> exit 2."""


def findings_sorted(findings):
    return sorted(findings, key=lambda f: (f.get("code") or "", f.get("path") or "",
                                           f.get("record_id") or "", f.get("evidence") or ""))


def esc(value, limit=300):
    text = "" if value is None else str(value)
    text = text.encode("unicode_escape", "backslashreplace").decode("ascii")
    return text[:limit]


def detect_suspicious(value):
    if not isinstance(value, str):
        return None
    if len(value) > MAX_STRING:
        return "string over %d characters" % MAX_STRING
    controls = [ch for ch in value if ord(ch) < 32 and ch not in "\n\t"]
    if controls:
        return "control character U+%04X" % ord(controls[0])
    if "\u202e" in value or "\u202d" in value:
        return "bidirectional override character"
    patterns = ["$(", "__import__", "os." + "system", "eval" + "(", "exec" + "(", "sub" + "process",
                chr(96), "\\?\\", "#!/"]
    for pat in patterns:
        if pat and pat in value:
            return "payload-like token %r" % pat
    return None


def walk_strings(node, path=""):
    if isinstance(node, dict):
        for key, value in node.items():
            yield from walk_strings(value, path + "." + str(key))
    elif isinstance(node, list):
        for index, value in enumerate(node):
            yield from walk_strings(value, path + "[%d]" % index)
    elif isinstance(node, str):
        yield path, node


def walk_keys(node, path=""):
    if isinstance(node, dict):
        for key, value in node.items():
            yield path + "." + str(key), str(key)
            yield from walk_keys(value, path + "." + str(key))
    elif isinstance(node, list):
        for index, value in enumerate(node):
            yield from walk_keys(value, path + "[%d]" % index)


def is_safe_relpath(value):
    return (isinstance(value, str) and bool(REL_PATH_RE.match(value))
            and not value.startswith("/") and not re.match(r"^[A-Za-z]:", value)
            and ".." not in value.split("/") and "\\" not in value)


def resolve_repo_path(repo_root, relpath):
    full = (repo_root / relpath).resolve()
    try:
        common = os.path.commonpath([str(full), str(repo_root.resolve())])
    except ValueError:
        return None
    if os.path.normcase(common) != os.path.normcase(str(repo_root.resolve())):
        return None
    return full


def sha256_file(path):
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def read_text(path):
    with open(path, "r", encoding="utf-8", errors="strict") as handle:
        return handle.read()


def load_json_checked(path, max_bytes, label):
    if not os.path.isfile(path):
        raise InputError("%s not found: %s" % (label, path))
    size = os.path.getsize(path)
    if size > max_bytes:
        raise InputError("INPUT-TOO-LARGE: %s is %d bytes (cap %d)" % (label, size, max_bytes))
    try:
        return json.loads(read_text(path))
    except (OSError, UnicodeDecodeError) as exc:
        raise InputError("%s unreadable: %s" % (label, exc))
    except ValueError as exc:
        raise InputError("%s is not valid JSON: %s" % (label, exc))


def parse_version(value):
    match = SEMVER_RE.match(value) if isinstance(value, str) else None
    if not match:
        return None
    return tuple(int(part) for part in match.groups())


def catalog_file_identity(path, repo_root):
    full = Path(path).resolve()
    rel = os.path.relpath(str(full), str(repo_root.resolve())).replace("\\", "/")
    return {"path": rel, "bytes": os.path.getsize(full), "sha256": sha256_file(full)}


def add(finding_list, code, path, record_id, evidence):
    finding_list.append({"code": code, "severity": "ERROR", "path": path,
                         "record_id": record_id, "evidence": esc(evidence)})


def check_structure(catalog, findings):
    def fail(path, record, message):
        add(findings, "SCHEMA", path, record, message)

    if not isinstance(catalog, dict):
        fail("$", None, "catalog must be a JSON object")
        return None
    allowed = {"schema", "catalog_version", "source_baseline", "profiles", "sources",
               "requirements"}
    for key in catalog:
        if key not in allowed:
            fail("$." + key, None, "unknown top-level field")
    for key in sorted(allowed):
        if key not in catalog:
            fail("$", None, "missing required top-level field %r" % key)
    if catalog.get("schema") != CATALOG_SCHEMA:
        fail("$.schema", None, "schema must be %r" % CATALOG_SCHEMA)
    version = catalog.get("catalog_version")
    parsed = parse_version(version)
    if parsed is None:
        add(findings, "BAD-VERSION", "$.catalog_version", None,
            "catalog_version is not SemVer: %r" % (version,))
    elif parsed[0] != SUPPORTED_MAJOR:
        raise UnsupportedMajor("UNSUPPORTED-MAJOR: catalog major %d is not supported"
                               % parsed[0])
    baseline = catalog.get("source_baseline")
    if not isinstance(baseline, dict):
        fail("$.source_baseline", None, "source_baseline must be an object")
    else:
        for key in ("repository", "revision", "tree"):
            if key not in baseline:
                fail("$.source_baseline", None, "missing required field %r" % key)
        for key in ("revision", "tree"):
            value = baseline.get(key)
            if key in baseline and not (isinstance(value, str) and GIT_SHA_RE.match(value)):
                fail("$.source_baseline." + key, None, "%s must be a 40-character lowercase git SHA" % key)
    profiles = catalog.get("profiles")
    if not isinstance(profiles, list) or not profiles:
        fail("$.profiles", None, "profiles must be a non-empty array")
        profiles = []
    profile_ids = set()
    for index, profile in enumerate(profiles):
        where = "$.profiles[%d]" % index
        if not isinstance(profile, dict):
            fail(where, None, "profile must be an object")
            continue
        for key in ("profile_id", "readable_name", "description", "scope_statement",
                    "mandatory_requirement_ids", "maintains_full_catalog", "owner"):
            if key not in profile:
                fail(where, None, "missing required profile field %r" % key)
        pid = profile.get("profile_id")
        if not (isinstance(pid, str) and PROFILE_RE.match(pid)):
            fail(where + ".profile_id", None, "invalid profile_id")
        elif pid in profile_ids:
            add(findings, "BAD-PROFILE", where, None, "duplicate profile_id %r" % pid)
        else:
            profile_ids.add(pid)
        if profile.get("maintains_full_catalog") is not True:
            add(findings, "BAD-PROFILE", where, None,
                "maintains_full_catalog must be true; a profile may not hide catalog records")
        mandatory = profile.get("mandatory_requirement_ids")
        if not isinstance(mandatory, list) or not mandatory:
            fail(where + ".mandatory_requirement_ids", None, "must be a non-empty array")
        else:
            for rid in mandatory:
                if not (isinstance(rid, str) and ID_RE.match(rid)):
                    fail(where + ".mandatory_requirement_ids", None, "invalid id %r" % (rid,))
        owner = profile.get("owner")
        if not isinstance(owner, dict) or not owner.get("role") or not owner.get("maintainer"):
            fail(where + ".owner", None, "owner requires role and maintainer")
    sources = catalog.get("sources")
    if not isinstance(sources, list) or not sources:
        fail("$.sources", None, "sources must be a non-empty array")
        sources = []
    source_paths = set()
    for index, source in enumerate(sources):
        where = "$.sources[%d]" % index
        if not isinstance(source, dict):
            fail(where, None, "source must be an object")
            continue
        path = source.get("path")
        if not is_safe_relpath(path):
            add(findings, "UNSAFE-PATH" if isinstance(path, str) else "SCHEMA", where,
                None, "unsafe or invalid source path %r" % (path,))
        elif path in source_paths:
            add(findings, "SCHEMA", where, None, "duplicate source path %r" % path)
        else:
            source_paths.add(path)
        digest = source.get("sha256")
        if not (isinstance(digest, str) and SHA256_RE.match(digest)):
            fail(where + ".sha256", None, "sha256 must be 64 lowercase hex")
        if not (isinstance(source.get("bytes"), int) and source["bytes"] >= 0):
            fail(where + ".bytes", None, "bytes must be a non-negative integer")
    requirements = catalog.get("requirements")
    if not isinstance(requirements, list):
        fail("$.requirements", None, "requirements must be an array")
        requirements = []
    if len(requirements) > MAX_REQUIREMENTS:
        raise InputError("INPUT-TOO-LARGE: %d requirements exceeds cap %d"
                         % (len(requirements), MAX_REQUIREMENTS))
    seen_ids = set()
    for index, record in enumerate(requirements):
        where = "$.requirements[%d]" % index
        if not isinstance(record, dict):
            fail(where, None, "requirement record must be an object")
            continue
        rid = record.get("requirement_id")
        if not (isinstance(rid, str) and ID_RE.match(rid)):
            add(findings, "BAD-ID" if isinstance(rid, str) else "SCHEMA", where, rid,
                "invalid requirement_id %r" % (rid,))
        elif rid in seen_ids:
            add(findings, "DUP-ID", where, rid, "duplicate requirement_id %r" % rid)
        else:
            seen_ids.add(rid)
        for key in ("requirement_id", "id_kind", "readable_name", "source_ref",
                    "applicability", "mechanism", "verification", "evidence_requirement",
                    "owner"):
            if key not in record:
                fail(where, rid, "missing required record field %r" % key)
        if not enum_value(record.get("id_kind"), ID_KINDS):
            fail(where + ".id_kind", rid, "invalid id_kind")
        name = record.get("readable_name")
        if not (isinstance(name, str) and 3 <= len(name) <= 160):
            fail(where + ".readable_name", rid, "readable_name length 3..160 required")
        sections = [
            ("source_ref", ("path", "anchor_kind", "anchor")),
            ("applicability", ("profiles", "inapplicability")),
            ("mechanism", ("kind", "refs", "limits")),
            ("verification", ("method", "check", "expected_result")),
            ("evidence_requirement", ("kind", "description")),
            ("owner", ("role", "maintainer")),
        ]
        for section, keys in sections:
            value = record.get(section)
            if not isinstance(value, dict):
                fail(where + "." + section, rid, "%s must be an object" % section)
                continue
            for key in keys:
                if key not in value:
                    fail(where + "." + section, rid, "missing %r" % key)
        source_ref = record.get("source_ref") or {}
        if isinstance(source_ref, dict):
            path = source_ref.get("path")
            if not is_safe_relpath(path):
                add(findings, "UNSAFE-PATH" if isinstance(path, str) else "SCHEMA",
                    where + ".source_ref.path", rid, "unsafe or invalid source path %r" % (path,))
            if not enum_value(source_ref.get("anchor_kind"), ANCHOR_KINDS):
                fail(where + ".source_ref.anchor_kind", rid, "invalid anchor_kind")
            anchor = source_ref.get("anchor")
            if not (isinstance(anchor, str) and 1 <= len(anchor) <= 300):
                fail(where + ".source_ref.anchor", rid, "anchor length 1..300 required")
        applicability = record.get("applicability") or {}
        if isinstance(applicability, dict):
            if not isinstance(applicability.get("profiles"), list):
                fail(where + ".applicability.profiles", rid, "profiles must be an array")
            if not isinstance(applicability.get("inapplicability"), list):
                fail(where + ".applicability.inapplicability", rid,
                     "inapplicability must be an array")
        mechanism = record.get("mechanism") or {}
        if isinstance(mechanism, dict):
            if not enum_value(mechanism.get("kind"), MECH_KINDS):
                add(findings, "BAD-MECHANISM", where + ".mechanism.kind", rid,
                    "invalid mechanism kind %r" % (mechanism.get("kind"),))
            refs = mechanism.get("refs")
            if not isinstance(refs, list):
                fail(where + ".mechanism.refs", rid, "refs must be an array")
            else:
                for rindex, ref in enumerate(refs):
                    if not isinstance(ref, dict) or not is_safe_relpath(ref.get("path")):
                        add(findings, "BAD-MECHANISM" if isinstance(ref, dict) else "SCHEMA",
                            where + ".mechanism.refs[%d]" % rindex, rid,
                            "mechanism ref needs a safe repository-relative path")
            limits = mechanism.get("limits")
            if not (isinstance(limits, str) and 20 <= len(limits) <= 1000):
                fail(where + ".mechanism.limits", rid, "mechanism.limits length 20..1000 required")
        verification = record.get("verification") or {}
        if isinstance(verification, dict):
            method = verification.get("method")
            if not enum_value(method, VERIF_METHODS):
                add(findings, "BAD-VERIFICATION", where + ".verification.method", rid,
                    "invalid verification method %r" % (method,))
            for key in ("check", "expected_result"):
                value = verification.get(key)
                if not (isinstance(value, str) and len(value) >= 3):
                    fail(where + ".verification." + key, rid, "%s is required" % key)
            if method == "none" and not (isinstance(verification.get("limits"), str)
                                         and len(verification["limits"]) >= 20):
                add(findings, "BAD-VERIFICATION", where + ".verification", rid,
                    "method 'none' requires an explicit limits statement")
        evidence_requirement = record.get("evidence_requirement") or {}
        if isinstance(evidence_requirement, dict):
            if not enum_value(evidence_requirement.get("kind"), EVID_KINDS):
                add(findings, "BAD-EVIDENCE-REQUIREMENT",
                    where + ".evidence_requirement.kind", rid,
                    "invalid evidence kind %r" % (evidence_requirement.get("kind"),))
            description = evidence_requirement.get("description")
            if not (isinstance(description, str) and len(description) >= 4):
                fail(where + ".evidence_requirement.description", rid,
                     "evidence description is required")
        owner = record.get("owner")
        if not isinstance(owner, dict) or not owner.get("role") or not owner.get("maintainer"):
            fail(where + ".owner", rid, "owner requires role and maintainer")
        for key in ("supersedes", "superseded_by", "related"):
            if key in record:
                values = record[key]
                if not isinstance(values, list) or any(
                        not (isinstance(v, str) and ID_RE.match(v)) for v in values):
                    fail(where + "." + key, rid, "%s must be an array of requirement ids" % key)
        if "negative_case_ids" in record:
            values = record["negative_case_ids"]
            if not isinstance(values, list) or any(
                    not (isinstance(v, str) and AC_RE.match(v)) for v in values):
                fail(where + ".negative_case_ids", rid, "must be AC-NN ids")
    return {"ids": seen_ids, "source_paths": source_paths, "requirements": requirements}


def check_sources(catalog, repo_root, findings):
    source_paths = {}
    for index, source in enumerate(catalog.get("sources") or []):
        if not isinstance(source, dict):
            continue
        path = source.get("path")
        if not is_safe_relpath(path):
            continue
        full = resolve_repo_path(repo_root, path)
        if full is None:
            add(findings, "UNSAFE-PATH", "$.sources[%d]" % index, None,
                "source path escapes the repository: %r" % path)
            continue
        if not os.path.isfile(full):
            add(findings, "MISSING-SOURCE", "$.sources[%d]" % index, None,
                "source path does not exist: %r" % path)
            continue
        actual_bytes = os.path.getsize(full)
        actual_sha = sha256_file(full)
        if source.get("bytes") != actual_bytes or source.get("sha256") != actual_sha:
            add(findings, "STALE-SOURCE", "$.sources[%d]" % index, None,
                "pinned source identity does not match current bytes for %r" % path)
            continue
        source_paths[path] = {"full": full, "text": None}
    return source_paths


def source_text(source_paths, path):
    entry = source_paths.get(path)
    if entry is None:
        return None
    if entry["text"] is None:
        try:
            entry["text"] = read_text(entry["full"])
        except (OSError, UnicodeDecodeError):
            entry["text"] = ""
    return entry["text"]


def anchor_resolves(text, anchor_kind, anchor):
    lines = text.splitlines()
    if anchor_kind == "heading":
        normalized = anchor.strip().lower()
        for line in lines:
            if re.match(r"^\s*#{1,6}\s+", line):
                heading = re.sub(r"^\s*#{1,6}\s+", "", line).strip().lower()
                heading = heading.rstrip("#").strip()
                if heading == normalized:
                    return True
        return False
    if anchor_kind == "line-span":
        match = re.match(r"^([0-9]+)(?:\s*-\s*([0-9]+))?$", anchor.strip())
        if not match:
            return False
        start = int(match.group(1))
        end = int(match.group(2) or start)
        return 1 <= start <= end <= len(lines)
    if anchor_kind == "symbol":
        return bool(anchor.strip()) and anchor.strip() in text
    return False


def check_requirements(catalog, repo_root, source_paths, findings):
    requirements = [r for r in (catalog.get("requirements") or []) if isinstance(r, dict)]
    by_id = {}
    for index, record in enumerate(requirements):
        rid = record.get("requirement_id")
        if isinstance(rid, str) and rid not in by_id:
            by_id[rid] = (index, record)
    profile_ids = {p.get("profile_id") for p in (catalog.get("profiles") or [])
                   if isinstance(p, dict)}
    declared_paths = {s.get("path") for s in (catalog.get("sources") or [])
                      if isinstance(s, dict)}
    for index, record in enumerate(requirements):
        rid = record.get("requirement_id")
        where = "$.requirements[%d]" % index
        if isinstance(rid, str):
            expected_kind = ("existing-authoritative"
                             if re.match(r"^(?:SD-[A-G]|MG[1-5])$", rid)
                             else "catalog-minted")
            if record.get("id_kind") != expected_kind:
                add(findings, "BAD-ID", where + ".id_kind", rid,
                    "id_kind %r is inconsistent with identifier family (expected %r)"
                    % (record.get("id_kind"), expected_kind))
        source_ref = record.get("source_ref") or {}
        path = source_ref.get("path")
        if is_safe_relpath(path):
            if path not in declared_paths:
                add(findings, "MISSING-SOURCE", where + ".source_ref", rid,
                    "source_ref path is not declared in sources: %r" % path)
            else:
                full = resolve_repo_path(repo_root, path)
                if full is None or not os.path.isfile(full):
                    add(findings, "MISSING-SOURCE", where + ".source_ref", rid,
                        "source_ref file missing or escapes the repository: %r" % path)
                else:
                    text = source_text(source_paths, path)
                    if text is None:
                        try:
                            text = read_text(full)
                        except (OSError, UnicodeDecodeError):
                            text = ""
                    if not anchor_resolves(text, source_ref.get("anchor_kind"),
                                           source_ref.get("anchor") or ""):
                        add(findings, "MISSING-ANCHOR", where + ".source_ref", rid,
                            "anchor does not resolve in %r: kind=%r anchor=%r"
                            % (path, source_ref.get("anchor_kind"), source_ref.get("anchor")))
                    quoted = source_ref.get("quoted_phrase")
                    if isinstance(quoted, str) and quoted and quoted not in text:
                        add(findings, "MISSING-ANCHOR", where + ".source_ref", rid,
                            "quoted_phrase not present in %r" % path)
        applicability = record.get("applicability") or {}
        profiles = applicability.get("profiles") if isinstance(applicability, dict) else []
        inapplicability = (applicability.get("inapplicability")
                           if isinstance(applicability, dict) else []) or []
        valid_profiles = []
        for pid in profiles if isinstance(profiles, list) else []:
            if not isinstance(pid, str) or pid not in profile_ids:
                add(findings, "UNKNOWN-REF", where + ".applicability", rid,
                    "applicability names unknown profile %r" % (pid,))
            else:
                valid_profiles.append(pid)
        for claim in inapplicability:
            if not isinstance(claim, dict):
                add(findings, "BAD-INAPPLICABILITY", where + ".applicability", rid,
                    "inapplicability entry must be an object")
                continue
            pid = claim.get("profile_id")
            if not isinstance(pid, str) or pid not in profile_ids:
                add(findings, "BAD-INAPPLICABILITY", where + ".applicability", rid,
                    "inapplicability names unknown profile %r" % (pid,))
            if not enum_value(claim.get("reason_code"), REASON_CODES):
                add(findings, "BAD-INAPPLICABILITY", where + ".applicability", rid,
                    "inapplicability reason_code is not allowlisted: %r"
                    % (claim.get("reason_code"),))
            justification = claim.get("justification")
            if not (isinstance(justification, str) and len(justification) >= 20):
                add(findings, "BAD-INAPPLICABILITY", where + ".applicability", rid,
                    "inapplicability justification must be at least 20 characters")
        if not valid_profiles and not inapplicability:
            add(findings, "BAD-INAPPLICABILITY", where + ".applicability", rid,
                "requirement has no valid applicability profile and no inapplicability claim")
        mechanism = record.get("mechanism") or {}
        for rindex, ref in enumerate(mechanism.get("refs") or []):
            if not isinstance(ref, dict):
                continue
            path = ref.get("path")
            if not is_safe_relpath(path):
                continue
            full = resolve_repo_path(repo_root, path)
            if full is None:
                add(findings, "UNSAFE-PATH", where + ".mechanism.refs", rid,
                    "mechanism ref escapes the repository: %r" % path)
            elif not (os.path.isfile(full) or os.path.isdir(full)):
                add(findings, "MISSING-SOURCE", where + ".mechanism.refs", rid,
                    "mechanism ref does not exist: %r" % path)
    edges = {}
    for rid, (index, record) in by_id.items():
        related = []
        for key in ("supersedes", "superseded_by", "related"):
            for other in record.get(key) or []:
                if other not in by_id:
                    add(findings, "UNKNOWN-REF", "$.requirements[%d]" % index, rid,
                        "%s names unknown requirement %r" % (key, other))
                else:
                    related.append(other)
                if other == rid:
                    add(findings, "CIRCULAR-BINDING", "$.requirements[%d]" % index, rid,
                        "%s contains the record itself" % key)
        edges[rid] = [r for r in related if r in by_id]
    visiting, done = set(), set()

    def visit(node):
        if node in done:
            return False
        if node in visiting:
            return True
        visiting.add(node)
        for target in edges.get(node, []):
            if visit(target):
                return True
        visiting.discard(node)
        done.add(node)
        return False

    for rid in sorted(edges):
        if visit(rid):
            add(findings, "CIRCULAR-DEPENDENCY", "$.requirements", rid,
                "supersession/relation graph contains a cycle involving %r" % rid)
            break
    return by_id


def check_observation_fields(catalog, findings):
    for path, key in walk_keys(catalog, "$"):
        if key in FORBIDDEN_KEYS:
            add(findings, "OBSERVATION-FIELD", path, None,
                "field name %r stores or implies an observation, authority or self-digest; "
                "the catalog stores no observations and grants no authority" % key)
    for path, value in walk_strings(catalog, "$"):
        reason = detect_suspicious(value)
        if reason:
            add(findings, "SUSPICIOUS-DATA", path, None,
                "untrusted data treated as data only (not executed): " + reason)


def check_completeness(catalog, findings):
    all_profiles = [p for p in (catalog.get("profiles") or []) if isinstance(p, dict)]
    profiles = [p for p in all_profiles if p.get("profile_id") == FIRST_PROFILE]
    requirements = [r for r in (catalog.get("requirements") or []) if isinstance(r, dict)]
    by_id = {}
    for record in requirements:
        rid = record.get("requirement_id")
        if isinstance(rid, str):
            by_id.setdefault(rid, record)

    def gap(message, record=None):
        add(findings, "COMPLETENESS-GAP", "$.requirements", record, message)

    mandatory = []
    mandatory_set = set()
    if len(all_profiles) != 1:
        gap("v1 requires exactly one profile; catalog declares %d" % len(all_profiles))
    if not profiles:
        gap("first profile %r is missing" % FIRST_PROFILE)
    else:
        mandatory = profiles[0].get("mandatory_requirement_ids")
        mandatory = mandatory if isinstance(mandatory, list) else []
        mandatory_set = set(m for m in mandatory if isinstance(m, str))
        for family, ids in SEED_FAMILIES.items():
            present = [rid for rid in ids if rid in mandatory_set and rid in by_id]
            if len(present) != len(ids):
                missing = [rid for rid in ids if rid not in present]
                gap("family %s is incomplete; missing mandatory seeds: %s"
                    % (family, ", ".join(missing)))
        if mandatory_set != set(SEED_IDS) or mandatory_set != set(by_id):
            gap("mandatory_requirement_ids must equal the declared seed inventory and every catalog record")
        for rid in SEED_IDS:
            record = by_id.get(rid)
            if record is None:
                gap("mandatory seed record is missing", rid)
                continue
            for section, keys in (("source_ref", ("path", "anchor_kind", "anchor")),
                                  ("mechanism", ("kind", "limits")),
                                  ("verification", ("method", "check", "expected_result")),
                                  ("evidence_requirement", ("kind", "description"))):
                value = record.get(section)
                if not isinstance(value, dict) or not all(value.get(key) for key in keys):
                    gap("mandatory record lacks required %s evidence" % section, rid)
    observed = len(requirements)
    if observed < DECLARED_COUNT_MIN or observed > DECLARED_COUNT_MAX:
        gap("declared first-profile record range is %d-%d but the catalog has %d records"
            % (DECLARED_COUNT_MIN, DECLARED_COUNT_MAX, observed))
    unknown_mandatory = sorted(mandatory_set - set(by_id))
    for rid in unknown_mandatory:
        gap("mandatory_requirement_ids names a record that does not exist", rid)
    uncovered = sorted(set(by_id) - mandatory_set)
    if uncovered:
        gap("catalog records omitted from first-profile mandatory_requirement_ids: %s"
            % ", ".join(uncovered))


def build_completeness(catalog):
    """Deterministic completeness report block (AC-29: declared range + observed count)."""
    requirements = [r for r in (catalog.get("requirements") or []) if isinstance(r, dict)]
    by_id = {}
    for record in requirements:
        rid = record.get("requirement_id")
        if isinstance(rid, str):
            by_id.setdefault(rid, record)
    profile = None
    for candidate in catalog.get("profiles") or []:
        if isinstance(candidate, dict) and candidate.get("profile_id") == FIRST_PROFILE:
            profile = candidate
            break
    mandatory = set()
    if profile is not None:
        mandatory = set(m for m in (profile.get("mandatory_requirement_ids") or [])
                        if isinstance(m, str))
    families = {}
    missing_seed_ids = []
    for family in sorted(SEED_FAMILIES):
        ids = SEED_FAMILIES[family]
        present = [rid for rid in ids if rid in by_id and rid in mandatory]
        families[family] = {"expected": len(ids), "present": len(present)}
        missing_seed_ids.extend(rid for rid in ids if rid not in present)
    observed = len(requirements)
    return {
        "declared_min": DECLARED_COUNT_MIN,
        "declared_max": DECLARED_COUNT_MAX,
        "observed_requirements": observed,
        "expected_families": len(SEED_FAMILIES),
        "expected_requirements": len(SEED_IDS),
        "families": families,
        "first_profile": FIRST_PROFILE,
        "in_declared_range": DECLARED_COUNT_MIN <= observed <= DECLARED_COUNT_MAX,
        "missing_seed_ids": sorted(set(missing_seed_ids)),
    }


def load_evidence_binding(path, catalog_identity, repo_root, findings, catalog_revision):
    binding = load_json_checked(path, MAX_EVIDENCE_BYTES, "evidence binding")
    if not isinstance(binding, dict):
        add(findings, "BAD-EVIDENCE-BINDING", path, None, "binding must be a JSON object")
        return None
    if binding.get("schema") != EVIDENCE_SCHEMA:
        add(findings, "BAD-EVIDENCE-BINDING", path, None,
            "binding schema must be %r" % EVIDENCE_SCHEMA)
        return None
    for path_key, key in walk_keys(binding, "$"):
        if key in FORBIDDEN_KEYS:
            add(findings, "CIRCULAR-BINDING", path_key, None,
                "evidence binding carries a self-referential/observation field %r" % key)
    for path_key, value in walk_strings(binding, "$"):
        reason = detect_suspicious(value)
        if reason:
            add(findings, "SUSPICIOUS-DATA", path_key, None,
                "untrusted evidence data treated as data only: " + reason)
    recorded_catalog = binding.get("catalog") if isinstance(binding.get("catalog"), dict) else {}
    stale = []
    if recorded_catalog.get("sha256") != catalog_identity.get("sha256"):
        stale.append("catalog sha256 expected %s observed %s"
                     % (recorded_catalog.get("sha256"), catalog_identity.get("sha256")))
    if recorded_catalog.get("bytes") != catalog_identity.get("bytes"):
        stale.append("catalog bytes expected %s observed %s"
                     % (recorded_catalog.get("bytes"), catalog_identity.get("bytes")))
    source_revision = binding.get("source_revision")
    if not (isinstance(source_revision, str) and GIT_SHA_RE.match(source_revision)):
        stale.append("source_revision is not a 40-character lowercase git SHA")
    elif source_revision != catalog_revision:
        stale.append("source_revision does not match the catalog source baseline")
    if stale:
        for message in stale:
            add(findings, "STALE-BINDING", path, None, "STALE-BINDING: " + message)
        return None
    records = binding.get("records")
    if not isinstance(records, list):
        add(findings, "BAD-EVIDENCE-BINDING", path, None, "records must be an array")
        return None
    if len(records) > MAX_EVIDENCE_RECORDS:
        raise InputError("INPUT-TOO-LARGE: %d evidence records exceeds cap %d"
                         % (len(records), MAX_EVIDENCE_RECORDS))
    parsed = []
    binding_dir = os.path.dirname(os.path.abspath(path))
    for index, record in enumerate(records):
        where = path + " records[%d]" % index
        if not isinstance(record, dict):
            add(findings, "BAD-EVIDENCE-BINDING", where, None, "record must be an object")
            continue
        classification = record.get("classification")
        if not enum_value(classification, CLASSIFICATIONS):
            add(findings, "UNKNOWN-OUTCOME", where, record.get("evidence_id"),
                "classification %r is not one of %s" % (classification, sorted(CLASSIFICATIONS)))
            continue
        requirement_ids = record.get("requirement_ids")
        if not isinstance(requirement_ids, list) or not requirement_ids:
            add(findings, "BAD-EVIDENCE-BINDING", where, record.get("evidence_id"),
                "requirement_ids must be a non-empty array")
            requirement_ids = []
        payload_ok = True
        if classification == "EXECUTED":
            payload_path = record.get("stdout_path")
            unsafe = (not isinstance(payload_path, str) or not payload_path
                      or ".." in payload_path.split("/") or "\\" in payload_path
                      or re.match(r"^[A-Za-z]:", payload_path) or payload_path.startswith("/"))
            if unsafe:
                add(findings, "BAD-EVIDENCE-BINDING", where, record.get("evidence_id"),
                    "executed record needs a safe relative payload path")
                payload_ok = False
            else:
                payload_full = os.path.join(binding_dir, payload_path)
                if not os.path.isfile(payload_full):
                    add(findings, "EVIDENCE-PAYLOAD", where, record.get("evidence_id"),
                        "declared payload file is absent")
                    payload_ok = False
                else:
                    actual_bytes = os.path.getsize(payload_full)
                    actual_sha = sha256_file(payload_full)
                    if (record.get("stdout_bytes") != actual_bytes
                            or record.get("stdout_sha256") != actual_sha):
                        add(findings, "EVIDENCE-PAYLOAD", where, record.get("evidence_id"),
                            "payload digest does not match the declared evidence")
                        payload_ok = False
        parsed.append({"record": record, "classification": classification,
                       "requirement_ids": [r for r in requirement_ids if isinstance(r, str)],
                       "payload_ok": payload_ok})
    return {"path": path, "records": parsed,
            "identity": {"path": os.path.basename(path), "bytes": os.path.getsize(path),
                         "sha256": sha256_file(path)}}


def evaluate_evidence(by_id, evidence, findings):
    evidence_present = set()
    unrun = set()
    if not evidence:
        return evidence_present, unrun
    for entry in evidence["records"]:
        for rid in entry["requirement_ids"]:
            if rid not in by_id:
                add(findings, "UNKNOWN-REF", evidence["path"], None,
                    "evidence record names unknown requirement %r" % rid)
                continue
            if entry["classification"] == "EXECUTED" and entry["payload_ok"]:
                evidence_present.add(rid)
            elif entry["classification"] in ("PLANNED-UNRUN", "UNRUN"):
                unrun.add(rid)
    return evidence_present, unrun


def build_report(catalog, catalog_identity, repo_root, evidence_path, profile_arg, findings):
    by_id = {}
    for record in catalog.get("requirements") or []:
        if isinstance(record, dict) and isinstance(record.get("requirement_id"), str):
            by_id.setdefault(record["requirement_id"], record)
    profiles = [p for p in (catalog.get("profiles") or []) if isinstance(p, dict)]
    selected = None
    if profile_arg:
        matches = [p for p in profiles if p.get("profile_id") == profile_arg]
        if not matches:
            raise InputError("profile %r not found in the catalog" % profile_arg)
        selected = matches[0]
    elif len(profiles) == 1:
        selected = profiles[0]
    mandatory = set()
    if selected is not None:
        mandatory = set(m for m in (selected.get("mandatory_requirement_ids") or [])
                        if isinstance(m, str))
    evidence = None
    if evidence_path:
        raw_baseline = catalog.get("source_baseline")
        catalog_revision = (raw_baseline.get("revision")
                            if isinstance(raw_baseline, dict) else None)
        evidence = load_evidence_binding(evidence_path, catalog_identity, repo_root, findings,
                                         catalog_revision)
    evidence_present, unrun = evaluate_evidence(by_id, evidence, findings)
    rows = []
    for rid in sorted(by_id):
        record = by_id[rid]
        if selected is not None and mandatory and rid not in mandatory:
            continue
        raw_mechanism = record.get("mechanism")
        mechanism = raw_mechanism if isinstance(raw_mechanism, dict) else {}
        raw_verification = record.get("verification")
        verification = raw_verification if isinstance(raw_verification, dict) else {}
        raw_evidence = record.get("evidence_requirement")
        evidence_requirement = raw_evidence if isinstance(raw_evidence, dict) else {}
        if rid in evidence_present:
            status = EVIDENCE_PRESENT
        elif rid in unrun:
            status = UNRUN_LISTED
        else:
            status = NO_EVIDENCE
        rows.append({
            "requirement_id": rid,
            "readable_name": record.get("readable_name"),
            "mechanism_kind": mechanism.get("kind"),
            "mechanism_limits": mechanism.get("limits"),
            "verification_method": verification.get("method"),
            "evidence_requirement_kind": evidence_requirement.get("kind"),
            "evidence_status": status,
            "procedural_not_machine_enforced": mechanism.get("kind") != "machine-check",
        })
    unrun_entries = []
    for rid in sorted(unrun):
        unrun_entries.append({"requirement_id": rid,
                              "reason": "an evidence record declares this check planned/unrun; "
                                        "it is never counted as present evidence"})
    findings = findings_sorted(findings)
    completeness = build_completeness(catalog)
    summary = {
        "requirements": len(rows),
        "observed_requirements": completeness["observed_requirements"],
        "findings": len(findings),
        "errors": sum(1 for f in findings if f["severity"] == "ERROR"),
        "warnings": sum(1 for f in findings if f["severity"] == "WARNING"),
        "evidence_present": sum(1 for row in rows if row["evidence_status"] == EVIDENCE_PRESENT),
        "no_evidence": sum(1 for row in rows if row["evidence_status"] == NO_EVIDENCE),
        "unrun_listed": len(unrun_entries),
        "circular_rejected": sum(1 for f in findings
                                 if f["code"] == "CIRCULAR-BINDING"),
    }
    return {
        "schema": REPORT_SCHEMA,
        "tool": {"name": TOOL_NAME, "version": TOOL_VERSION,
                 "sha256": sha256_file(os.path.abspath(__file__))},
        "catalog": catalog_identity,
        "completeness": completeness,
        "evidence_binding": evidence["identity"] if evidence else None,
        "profile": ({"profile_id": selected.get("profile_id"),
                     "readable_name": selected.get("readable_name")}
                    if selected is not None else None),
        "requirements": rows,
        "findings": findings,
        "summary": summary,
        "unrun": unrun_entries,
        "limits": [
            LIMITS_SENTENCE,
            "The catalog is an index over existing normative sources; it replaces no normative "
            "document, validator, audit or delivery workflow.",
            "No status in this report is an approval, a merge authorization or a claim of live "
            "or production behaviour.",
        ],
    }


def human_summary(report):
    lines = []
    lines.append("conformance catalog check: %s" % report["catalog"]["path"])
    lines.append("catalog bytes=%s sha256=%s" % (report["catalog"]["bytes"],
                                                 report["catalog"]["sha256"]))
    if report.get("profile"):
        lines.append("profile: %s (%s)" % (report["profile"]["profile_id"],
                                           report["profile"]["readable_name"]))
    for finding in report["findings"]:
        lines.append("  %-24s %s %s" % (finding["code"], finding["path"],
                                        esc(finding["evidence"], 200)))
    summary = report["summary"]
    lines.append("SUMMARY: requirements=%d findings=%d errors=%d warnings=%d "
                 "evidence_present=%d no_evidence=%d unrun_listed=%d" % (
                     summary["requirements"], summary["findings"], summary["errors"],
                     summary["warnings"], summary["evidence_present"],
                     summary["no_evidence"], summary["unrun_listed"]))
    completeness = report["completeness"]
    lines.append("COMPLETENESS: declared_min=%d declared_max=%d observed_requirements=%d "
                 "expected_families=%d expected_requirements=%d in_declared_range=%s"
                 % (completeness["declared_min"], completeness["declared_max"],
                    completeness["observed_requirements"], completeness["expected_families"],
                    completeness["expected_requirements"],
                    "YES" if completeness["in_declared_range"] else "NO"))
    lines.append("LIMITS: " + LIMITS_SENTENCE)
    return "\n".join(lines)


def write_out(path, report, repo_root, input_paths=()):
    full = Path(path).resolve()
    if full.exists() and not full.is_file():
        raise InputError("--out destination must be a regular file")
    for input_path in input_paths:
        if full == Path(input_path).resolve():
            raise InputError("--out must not overwrite an input file")
    try:
        common = os.path.commonpath([str(full), str(repo_root.resolve())])
    except ValueError:
        common = ""
    if os.path.normcase(common) == os.path.normcase(str(repo_root.resolve())):
        raise InputError("--out must resolve outside the repository root")
    directory = str(full.parent)
    if not os.path.isdir(directory):
        raise InputError("--out directory does not exist")
    payload = json.dumps(report, sort_keys=True, indent=2, ensure_ascii=True) + "\n"
    handle = tempfile.NamedTemporaryFile(prefix=".conformance-", dir=directory, delete=False)
    try:
        with handle:
            handle.write(payload.encode("utf-8"))
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(handle.name, str(full))
    finally:
        if os.path.exists(handle.name):
            try:
                os.unlink(handle.name)
            except OSError:
                pass


def parse_args(argv):
    parser = argparse.ArgumentParser(
        prog="check_catalog.py",
        description="Read-only deterministic checker for the Aegis conformance catalog; "
                    "report-only, no repair, no CI wiring.")
    parser.add_argument("--catalog", required=True)
    parser.add_argument("--evidence", default=None)
    parser.add_argument("--profile", default=None)
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--out", default=None)
    parser.add_argument("--quiet", action="store_true")
    return parser.parse_args(argv)


def main(argv=None):
    args = parse_args(argv)
    repo_root = Path.cwd().resolve()
    try:
        catalog = load_json_checked(args.catalog, MAX_CATALOG_BYTES, "catalog")
        catalog_identity = catalog_file_identity(args.catalog, repo_root)
        if not isinstance(catalog, dict):
            raise InputError("catalog must be a JSON object")
        findings = []
        structure = check_structure(catalog, findings)
        if structure is not None and not any(f.get("code") == "SCHEMA" for f in findings):
            source_paths = check_sources(catalog, repo_root, findings)
            check_requirements(catalog, repo_root, source_paths, findings)
            check_observation_fields(catalog, findings)
            check_completeness(catalog, findings)
        report = build_report(catalog, catalog_identity, repo_root, args.evidence,
                              args.profile, findings)
        report["exit_code"] = 1 if report["findings"] else 0
        payload = json.dumps(report, sort_keys=True, indent=2, ensure_ascii=True) + "\n"
        if args.out:
            write_out(args.out, report, repo_root,
                      [args.catalog] + ([args.evidence] if args.evidence else []))
        if args.json:
            sys.stdout.write(payload)
        elif not args.quiet:
            print(human_summary(report))
        if args.quiet and not args.json:
            print("SUMMARY: findings=%d" % len(report["findings"]))
        if report["findings"]:
            sys.stderr.write("findings=%d\n" % len(report["findings"]))
        return report["exit_code"]
    except UnsupportedMajor as exc:
        sys.stderr.write("ERROR (exit 2): " + str(exc) + "\n")
        return 2
    except InputError as exc:
        sys.stderr.write("ERROR (exit 2): " + str(exc) + "\n")
        return 2
    except InternalError as exc:
        sys.stderr.write("ERROR (exit 3): " + str(exc) + "\n")
        return 3
    except Exception as exc:
        sys.stderr.write("ERROR (exit 3): %s: %s\n" % (type(exc).__name__, exc))
        return 3


if __name__ == "__main__":
    sys.exit(main())
