#!/usr/bin/env python3
"""Deterministic read-only host capability record checker (stdlib only, offline).

Validates synthetic host capability records and the offline fixture set against
the program-internal aegis.host-capability-record/1 contract. It reads files,
recomputes the declared config digest, compares the fixture manifest and the
expected-findings table, and emits a deterministic findings report. It never
writes the repository, never spawns a process, never reaches a remote service,
never reads a credential and never probes a host.

Exit codes: 0 clean (fixture-set expectations met or record clean);
1 findings; 2 usage/input/refused-path/over-cap/bad JSON; 3 internal error.
Program-internal tooling only; not a host, consumer or production qualification.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

SCHEMA_ID = "aegis.host-capability-record/1"
MANIFEST_SCHEMA_ID = "aegis.host-record-fixture-manifest/1"
EXPECTED_SCHEMA_ID = "aegis.host-record-expected-findings/1"
REPORT_SCHEMA_ID = "aegis.host-record-check-report/1"
TOOL = "check_host_record"

MAX_RECORD_BYTES = 65536
MAX_MANIFEST_BYTES = 262144
MAX_RECORDS = 64
MAX_CAPABILITIES = 50
MIN_CAPABILITIES = 7  # v1 schema minItems: one entry per capability
MIN_SOURCE_EVIDENCE = 1  # v1 schema minItems: at least one cited payload
MAX_STRING_CHARS = 2000
FIXTURE_RECORD_COUNT = 6  # this fixture set is pinned at six record entries

MANIFEST_TOP_FIELDS = ("schema", "fixture_version", "entries")
MANIFEST_ENTRY_FIELDS = ("path", "bytes", "sha256", "kind", "expected_exit")
EXPECTED_TOP_FIELDS = ("schema", "fixture_version", "entries")
EXPECTED_ENTRY_FIELDS = ("fixture", "contract_negative", "expected_findings", "expected_exit", "expected_absent_fields")
VALID_EXITS = (0, 1)

RECORD_ID_RE = re.compile(r"^HCR-[A-Z0-9-]{1,40}$")
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
SECRET_RE = re.compile(r"(password|token|secret|api[_-]?key|credential|private[_-]?key)")
PERSONAL_RE = re.compile(r"(email|phone|address|account[_-]?id|full[_-]?name)")

CAPABILITIES = [
    "discovery",
    "explicit-invocation",
    "automatic-invocation-restriction",
    "reference-loading",
    "tool-permission",
    "interruption-resume",
    "evidence-collection",
]
DISPOSITIONS = ["VERIFIED", "UNSUPPORTED", "UNKNOWN", "NOT_RUN"]
INVOCATION_MODES = ["discovery", "explicit-invocation", "manual-invocation", "automatic-invocation"]
AGGREGATE_KEYS = ("aggregate", "aggregate_ok")
FORBIDDEN_KEYS = (
    "pass",
    "qualified",
    "approved",
    "authorized",
    "host_qualified",
    "consumer_qualified",
    "authority",
    "status",
    "self_sha256",
    "self_hash",
    "self_digest",
    "own_hash",
    "own_digest",
)
REQUIRED_TOP = [
    "schema",
    "record_id",
    "synthetic",
    "preparation_only",
    "source_evidence",
    "host",
    "config_digest",
    "package_binding",
    "capabilities",
    "limits",
    "non_claims",
]
REQUIRED_HOST = ["product", "version", "os_name", "os_version", "invocation_mode"]
REQUIRED_CONFIG = ["algorithm", "input_names", "input_values", "digest"]
REQUIRED_PACKAGE = ["package_manifest_sha256", "profile_id"]
REQUIRED_CAPABILITY = ["capability", "disposition", "reason", "evidence_refs"]


class UsageError(Exception):
    """Usage or input error mapped to exit code 2."""


def repo_root_for(script_path):
    return Path(script_path).resolve().parents[2]


def canonical_json(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def sha256_bytes(raw):
    return hashlib.sha256(raw).hexdigest()


def is_int_not_bool(value):
    """A JSON integer only: JSON true/false are bool, an int subclass, so 1 == True."""
    return isinstance(value, int) and not isinstance(value, bool)


def is_string_list(value):
    """A JSON array whose every element is a string."""
    return isinstance(value, list) and all(isinstance(item, str) for item in value)


def has_control_characters(text):
    """Reject NUL and every other C0/DEL control character in a path string."""
    return any(ord(char) < 32 or ord(char) == 127 for char in text)


def normalise_relative(text):
    """Collapse empty and '.' segments so path comparisons are canonical."""
    return "/".join(part for part in text.split("/") if part not in ("", "."))


def is_safe_relative(text):
    if not isinstance(text, str) or not text:
        return False
    if has_control_characters(text):
        return False
    if text.startswith("/") or text.startswith("\\"):
        return False
    if re.match(r"^[A-Za-z]:", text):
        return False
    if "\\" in text:
        return False
    parts = [part for part in text.split("/") if part not in ("", ".")]
    if any(part == ".." for part in parts):
        return False
    return True


def resolve_under_repo(repo, relative):
    if not is_safe_relative(relative):
        raise UsageError("UNSAFE-PATH: refusing unsafe input path: " + repr(relative))
    try:
        candidate = (repo / relative).resolve()
        root = repo.resolve()
    except (OSError, RuntimeError, ValueError) as exc:
        raise UsageError("UNSAFE-PATH: input path cannot be resolved") from exc
    try:
        candidate.relative_to(root)
    except ValueError as exc:
        raise UsageError("UNSAFE-PATH: path escapes the repository") from exc
    return candidate


def walk_strings(value):
    """Yield every string in the document, including object field names."""
    if isinstance(value, str):
        yield value
    elif isinstance(value, dict):
        for name, child in value.items():
            yield str(name)
            yield from walk_strings(child)
    elif isinstance(value, list):
        for child in value:
            yield from walk_strings(child)


def enforce_input_caps(record):
    """Apply the input-class caps that must fail closed before any report.

    The byte caps are enforced by load_json; the string-length cap and the
    capability-count cap are enforced here so an over-cap record exits 2 with no
    report, matching the README's fail-closed statement.
    """
    if not isinstance(record, dict):
        return
    for text in walk_strings(record):
        if len(text) > MAX_STRING_CHARS:
            raise UsageError("INPUT-TOO-LARGE: a record string exceeds the " + str(MAX_STRING_CHARS) + "-character cap")
    capabilities = record.get("capabilities")
    if isinstance(capabilities, list) and len(capabilities) > MAX_CAPABILITIES:
        raise UsageError("INPUT-TOO-LARGE: capability count " + str(len(capabilities)) + " exceeds the cap of " + str(MAX_CAPABILITIES))


def load_json(path, max_bytes):
    """Read one JSON file, refusing an over-cap file from stat() before reading it."""
    try:
        size = path.stat().st_size
    except OSError as exc:
        raise UsageError("UNKNOWN-FIXTURE: input file cannot be stat()ed") from exc
    if size > max_bytes:
        raise UsageError("INPUT-TOO-LARGE: " + str(path.name) + " exceeds the byte cap")
    raw = path.read_bytes()
    if len(raw) > max_bytes:
        raise UsageError("INPUT-TOO-LARGE: " + str(path.name) + " exceeds the byte cap")
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise UsageError("BAD-JSON: file is not valid UTF-8") from exc
    try:
        document = json.loads(text)
    except json.JSONDecodeError as exc:
        raise UsageError("BAD-JSON: file is not valid JSON") from exc
    return document, raw


def add(findings, code, location, evidence):
    findings.append({"code": code, "path": location, "evidence": evidence})


def key_class(name):
    low = str(name).lower()
    if low in AGGREGATE_KEYS:
        return "AGGREGATE-CAPABILITY"
    if SECRET_RE.search(low):
        return "SECRET-LIKE-FIELD"
    if PERSONAL_RE.search(low):
        return "PERSONAL-DATA-FIELD"
    if low in FORBIDDEN_KEYS:
        return "UNKNOWN-FIELD"
    return None


def join(parent, name):
    return parent + "/" + str(name) if parent else str(name)


def walk_keys(value, location, findings):
    if isinstance(value, dict):
        for name, child in value.items():
            child_location = join(location, name)
            code = key_class(name)
            if code is not None:
                add(findings, code, child_location, "forbidden field family in a host record")
            walk_keys(child, child_location, findings)
    elif isinstance(value, list):
        for index, child in enumerate(value):
            walk_keys(child, location + "[" + str(index) + "]", findings)


def field_names(value):
    """Every object field name in the document, lower-cased, at any depth."""
    names = set()
    if isinstance(value, dict):
        for name, child in value.items():
            names.add(str(name).casefold())
            names |= field_names(child)
    elif isinstance(value, list):
        for child in value:
            names |= field_names(child)
    return names


def config_digest_of(input_names, input_values):
    payload = canonical_json({"input_names": input_names, "input_values": input_values})
    return sha256_bytes(payload.encode("utf-8"))


def validate_record(record, record_relative, findings, record_sha256=None):
    if not isinstance(record, dict):
        add(findings, "SCHEMA", "", "record root is not a JSON object")
        return 0
    for name in record:
        if name in REQUIRED_TOP or key_class(name) is not None:
            continue
        add(findings, "UNKNOWN-FIELD", str(name), "field is not in the v1 contract")
    for name in REQUIRED_TOP:
        if name not in record:
            add(findings, "MISSING-FIELD", str(name), "required v1 field is missing")
    walk_keys(record, "", findings)
    if record.get("schema") != SCHEMA_ID:
        add(findings, "SCHEMA", "schema", "record schema id is not the supported v1 id")
    record_id = record.get("record_id")
    if not isinstance(record_id, str) or RECORD_ID_RE.match(record_id) is None:
        add(findings, "BAD-RECORD-ID", "record_id", "record id is not HCR-[A-Z0-9-]{1,40}")
    if record.get("synthetic") is not True or record.get("preparation_only") is not True:
        add(findings, "UNSYNTHETIC-REAL-CLAIM", "", "synthetic and preparation_only must both be true")
    source_evidence = record.get("source_evidence")
    if "source_evidence" in record and not isinstance(source_evidence, list):
        add(findings, "SCHEMA", "source_evidence", "source evidence must be an array of evidence entries")
    if isinstance(source_evidence, list):
        if len(source_evidence) < MIN_SOURCE_EVIDENCE:
            add(findings, "SOURCE-EVIDENCE-EMPTY", "source_evidence", "source evidence count " + str(len(source_evidence)) + " is below the v1 minimum of " + str(MIN_SOURCE_EVIDENCE))
        for index, item in enumerate(source_evidence):
            base = "source_evidence[" + str(index) + "]"
            if not isinstance(item, dict):
                add(findings, "SCHEMA", base, "source evidence entry is not an object")
                continue
            for name in item:
                if name not in ("path", "bytes", "sha256", "note") and key_class(name) is None:
                    add(findings, "UNKNOWN-FIELD", base + "/" + str(name), "source evidence field is not in the v1 contract")
            for name in ("path", "bytes", "sha256", "note"):
                if name not in item:
                    add(findings, "MISSING-FIELD", base + "/" + name, "source evidence field is missing")
            path = item.get("path")
            if not isinstance(path, str) or not is_safe_relative(path):
                add(findings, "UNSAFE-PATH", base + "/path", "source evidence path is unsafe")
            elif normalise_relative(path).casefold() == normalise_relative(record_relative).casefold():
                add(findings, "UNSAFE-PATH", base + "/path", "record may not cite itself")
            digest = item.get("sha256")
            if not isinstance(digest, str) or SHA256_RE.match(digest) is None:
                add(findings, "SCHEMA", base + "/sha256", "source evidence digest is not sha256 hex")
            byte_count = item.get("bytes")
            if not isinstance(byte_count, int) or isinstance(byte_count, bool) or byte_count < 0:
                add(findings, "SCHEMA", base + "/bytes", "source evidence byte count is not a non-negative integer")
            note = item.get("note")
            if not isinstance(note, str) or len(note) < 3:
                add(findings, "SCHEMA", base + "/note", "source evidence note is missing or too short")
    host = record.get("host")
    if "host" in record and not isinstance(host, dict):
        add(findings, "SCHEMA", "host", "host must be a JSON object")
    if isinstance(host, dict):
        for name in REQUIRED_HOST:
            if name not in host:
                add(findings, "MISSING-FIELD", "host/" + name, "host field is missing")
        for name in host:
            if name not in REQUIRED_HOST and key_class(name) is None:
                add(findings, "UNKNOWN-FIELD", "host/" + str(name), "host field is not in the v1 contract")
        if host.get("invocation_mode") not in INVOCATION_MODES:
            add(findings, "SCHEMA", "host/invocation_mode", "invocation mode is not a v1 enum value")
    config = record.get("config_digest")
    if "config_digest" in record and not isinstance(config, dict):
        add(findings, "SCHEMA", "config_digest", "config digest must be a JSON object")
    if isinstance(config, dict):
        for name in REQUIRED_CONFIG:
            if name not in config:
                add(findings, "MISSING-FIELD", "config_digest/" + name, "config digest field is missing")
        for name in config:
            if name not in REQUIRED_CONFIG and key_class(name) is None:
                add(findings, "UNKNOWN-FIELD", "config_digest/" + str(name), "config digest field is not in the v1 contract")
        names = config.get("input_names")
        values = config.get("input_values")
        digest = config.get("digest")
        if config.get("algorithm") != "sha256":
            add(findings, "BAD-CONFIG-DIGEST", "config_digest/algorithm", "algorithm must be sha256")
        if not isinstance(names, list) or not isinstance(values, dict):
            add(findings, "BAD-CONFIG-DIGEST", "config_digest", "input names and values are malformed")
        else:
            try:
                expected_digest = config_digest_of(names, values)
            except (TypeError, ValueError):
                add(findings, "BAD-CONFIG-DIGEST", "config_digest", "digest inputs are not canonicalisable")
            else:
                if not isinstance(digest, str) or digest != expected_digest:
                    add(findings, "BAD-CONFIG-DIGEST", "config_digest/digest", "declared digest does not recompute from the declared inputs")
    binding = record.get("package_binding")
    if "package_binding" in record and not isinstance(binding, dict):
        add(findings, "SCHEMA", "package_binding", "package binding must be a JSON object")
    if isinstance(binding, dict):
        for name in REQUIRED_PACKAGE:
            if name not in binding:
                add(findings, "MISSING-FIELD", "package_binding/" + name, "package binding field is missing")
        for name in binding:
            if name not in REQUIRED_PACKAGE and key_class(name) is None:
                add(findings, "UNKNOWN-FIELD", "package_binding/" + str(name), "package binding field is not in the v1 contract")
        manifest_digest = binding.get("package_manifest_sha256")
        profile = binding.get("profile_id")
        if not isinstance(manifest_digest, str) or SHA256_RE.match(manifest_digest) is None:
            add(findings, "BAD-PACKAGE-BINDING", "package_binding/package_manifest_sha256", "package manifest digest is not sha256 hex")
        elif record_sha256 is not None and manifest_digest == record_sha256:
            add(findings, "BAD-PACKAGE-BINDING", "package_binding/package_manifest_sha256", "package manifest digest may not be the record's own digest")
        if not isinstance(profile, str) or len(profile.strip()) < 3:
            add(findings, "BAD-PACKAGE-BINDING", "package_binding/profile_id", "profile id is missing or too short")
    capabilities = record.get("capabilities")
    capability_count = 0
    if isinstance(capabilities, list):
        capability_count = len(capabilities)
        if len(capabilities) < MIN_CAPABILITIES:
            add(findings, "CAPABILITY-COUNT", "capabilities", "capability count " + str(len(capabilities)) + " is below the v1 minimum of " + str(MIN_CAPABILITIES) + " (one entry per capability)")
        seen = set()
        for index, item in enumerate(capabilities):
            base = "capabilities[" + str(index) + "]"
            if not isinstance(item, dict):
                add(findings, "SCHEMA", base, "capability entry is not an object")
                continue
            for name in item:
                if name in REQUIRED_CAPABILITY or name == "remaining_action" or key_class(name) is not None:
                    continue
                add(findings, "UNKNOWN-FIELD", base + "/" + str(name), "capability field is not in the v1 contract")
            for name in ("capability", "disposition", "reason", "evidence_refs"):
                if name not in item and name != "disposition":
                    add(findings, "MISSING-FIELD", base + "/" + name, "capability field is missing")
            if "disposition" not in item:
                add(findings, "MISSING-DISPOSITION", base, "capability has no disposition")
            capability_name = item.get("capability")
            if capability_name not in CAPABILITIES:
                add(findings, "SCHEMA", base + "/capability", "capability name is not a v1 enum value")
            elif capability_name in seen:
                add(findings, "DUPLICATE-CAPABILITY", base + "/capability", "capability is duplicated")
            else:
                seen.add(capability_name)
            disposition = item.get("disposition")
            if "disposition" in item and disposition not in DISPOSITIONS:
                add(findings, "BAD-DISPOSITION", base + "/disposition", "disposition is not a v1 enum value")
            elif disposition == "VERIFIED":
                refs = item.get("evidence_refs")
                if not isinstance(refs, list) or len(refs) == 0:
                    add(findings, "VERIFIED-WITHOUT-EVIDENCE", base, "VERIFIED requires at least one evidence reference")
            elif disposition in ("UNKNOWN", "NOT_RUN"):
                reason = item.get("reason")
                action = item.get("remaining_action")
                if not isinstance(reason, str) or len(reason.strip()) < 3 or not isinstance(action, str) or len(action.strip()) < 3:
                    add(findings, "UNKNOWN-WITHOUT-REASON", base, "UNKNOWN/NOT_RUN requires a named reason and remaining action")
            reason = item.get("reason")
            if "reason" in item and (not isinstance(reason, str) or len(reason) < 3):
                add(findings, "SCHEMA", base + "/reason", "capability reason is missing or too short")
            refs = item.get("evidence_refs")
            if "evidence_refs" in item and not isinstance(refs, list):
                add(findings, "SCHEMA", base + "/evidence_refs", "evidence refs must be an array")
            if isinstance(refs, list):
                for ref_index, ref in enumerate(refs):
                    ref_location = base + "/evidence_refs[" + str(ref_index) + "]"
                    if not isinstance(ref, str) or not is_safe_relative(ref):
                        add(findings, "UNSAFE-PATH", ref_location, "evidence reference is unsafe")
                    elif normalise_relative(ref).casefold() == normalise_relative(record_relative).casefold():
                        add(findings, "UNSAFE-PATH", ref_location, "evidence reference may not cite the record itself")
    else:
        add(findings, "AGGREGATE-CAPABILITY", "capabilities", "capabilities must be a separate-entry array, not an aggregate value")
    for name in ("limits", "non_claims"):
        value = record.get(name)
        if not isinstance(value, list) or len(value) == 0:
            add(findings, "MISSING-FIELD", name, "required list field is absent or empty")
            continue
        for index, item in enumerate(value):
            if not isinstance(item, str) or len(item) < 3:
                add(findings, "SCHEMA", name + "[" + str(index) + "]", "list entry is not a string of at least three characters")
    non_claims = record.get("non_claims")
    if isinstance(non_claims, list) and 0 < len(non_claims) < 3:
        add(findings, "SCHEMA", "non_claims", "non_claims must carry at least three entries")
    if isinstance(non_claims, list):
        required_claims = [
            "not host/consumer qualification",
            "not a portability claim",
            "not live/production behaviour",
        ]
        for claim in required_claims:
            if claim not in non_claims:
                add(findings, "MISSING-FIELD", "non_claims", "required non-claim is missing: " + claim)
    return capability_count


def validate_expectation_entry(entry, location, findings):
    """Validate one expectation entry's metadata; every defect is a finding, never a raise."""
    for name in entry:
        if name not in EXPECTED_ENTRY_FIELDS:
            add(findings, "EXPECTED-FINDINGS-MISMATCH", location + "/" + str(name), "expectation field is not in the v1 contract")
    if "expected_findings" not in entry:
        add(findings, "EXPECTED-FINDINGS-MISMATCH", location, "expectation findings list is missing")
    elif not is_string_list(entry.get("expected_findings")):
        add(findings, "EXPECTED-FINDINGS-MISMATCH", location + "/expected_findings", "expected findings must be a list of strings")
    if "expected_exit" not in entry:
        add(findings, "EXPECTED-FINDINGS-MISMATCH", location + "/expected_exit", "expectation exit code is missing")
    elif not is_int_not_bool(entry.get("expected_exit")) or entry.get("expected_exit") not in VALID_EXITS:
        add(findings, "EXPECTED-FINDINGS-MISMATCH", location + "/expected_exit", "expected exit code must be the integer 0 or 1")
    if "expected_absent_fields" in entry and not is_string_list(entry.get("expected_absent_fields")):
        add(findings, "EXPECTED-FINDINGS-MISMATCH", location + "/expected_absent_fields", "expected absent fields must be a list of strings")
    if "contract_negative" in entry and not isinstance(entry.get("contract_negative"), bool):
        add(findings, "EXPECTED-FINDINGS-MISMATCH", location + "/contract_negative", "contract_negative must be a boolean")


def validate_expected_table(expected, findings):
    for name in expected:
        if name not in EXPECTED_TOP_FIELDS:
            add(findings, "EXPECTED-FINDINGS-MISMATCH", str(name), "expected-findings field is not in the v1 contract")
    if expected.get("fixture_version") != "v1":
        add(findings, "EXPECTED-FINDINGS-MISMATCH", "fixture_version", "expected-findings fixture version is not the current v1")
    entries = expected.get("entries")
    if not isinstance(entries, list):
        add(findings, "EXPECTED-FINDINGS-MISMATCH", "entries", "expected-findings table has no entries list")
        return {}, []
    real = {}
    contract = []
    seen = set()
    declared_paths = []
    for index, entry in enumerate(entries):
        location = "entries[" + str(index) + "]"
        if not isinstance(entry, dict):
            add(findings, "EXPECTED-FINDINGS-MISMATCH", location, "expectation entry is not an object")
            continue
        validate_expectation_entry(entry, location, findings)
        fixture = entry.get("fixture")
        if not isinstance(fixture, str) or not is_safe_relative(fixture):
            add(findings, "EXPECTED-FINDINGS-MISMATCH", location, "expectation fixture path is missing or unsafe")
            continue
        clean = normalise_relative(fixture)
        declared_paths.append(clean)
        if clean in seen:
            add(findings, "EXPECTED-FINDINGS-MISMATCH", clean, "duplicate expectation path; only the first entry counts")
            continue
        seen.add(clean)
        if entry.get("contract_negative") is True:
            contract.append(entry)
            continue
        real[clean] = entry
    if len(entries) != 8:
        add(findings, "EXPECTED-FINDINGS-MISMATCH", "entries", "expected-findings must have exactly eight entries")
    expected_contract_codes = sorted(["MANIFEST-STALE", "EXPECTED-FINDINGS-MISMATCH"])
    actual_contract_codes = sorted(
        code
        for entry in contract
        if is_string_list(entry.get("expected_findings"))
        for code in entry.get("expected_findings")
    )
    if len(contract) != 2 or actual_contract_codes != expected_contract_codes:
        add(findings, "EXPECTED-FINDINGS-MISMATCH", "entries", "contract-negative expectations must be exactly two with the pinned codes")
    if declared_paths != sorted(declared_paths):
        add(findings, "EXPECTED-FINDINGS-MISMATCH", "entries", "expectation fixture paths must be sorted")
    return real, contract


def compare_expectation(record, record_relative, actual_codes, expectation, findings):
    expected_codes = expectation.get("expected_findings")
    expected_exit = expectation.get("expected_exit")
    if not is_string_list(expected_codes) or not is_int_not_bool(expected_exit) or expected_exit not in VALID_EXITS:
        add(findings, "EXPECTED-FINDINGS-MISMATCH", record_relative, "expectation metadata is malformed")
        return
    actual_exit = 0 if len(actual_codes) == 0 else 1
    if actual_exit != expected_exit or sorted(actual_codes) != sorted(expected_codes):
        add(findings, "EXPECTED-FINDINGS-MISMATCH", record_relative, "observed codes/exit differ from the expected-findings table")
    absent = expectation.get("expected_absent_fields")
    if is_string_list(absent) and absent:
        present = sorted(field_names(record) & {item.casefold() for item in absent})
        if present:
            add(findings, "EXPECTED-FINDINGS-MISMATCH", record_relative, "record carries a field the expectation requires absent: " + ", ".join(present))


def resolve_manifest_entry(repo, relative, findings, root=None):
    """Resolve one manifest entry, refusing any path that escapes the boundary.

    The boundary is the repository root by default and the supplied fixtures
    directory for a fixture-set check. A safe-looking relative string can still
    resolve outside the boundary through a symlink or junction; that is a
    deterministic finding, not a read.
    """
    boundary = repo if root is None else root
    try:
        candidate = (repo / relative).resolve()
        boundary_resolved = boundary.resolve()
    except (OSError, RuntimeError, ValueError):
        add(findings, "UNSAFE-PATH", relative, "manifest entry path cannot be resolved")
        return None
    try:
        candidate.relative_to(boundary_resolved)
    except ValueError:
        message = "manifest entry resolves outside the repository" if root is None else "manifest entry resolves outside the fixtures directory"
        add(findings, "UNSAFE-PATH", relative, message)
        return None
    return candidate


def validate_fixture_set(repo, fixtures_relative):
    fixtures_rel = normalise_relative(fixtures_relative)
    fixtures_dir = resolve_under_repo(repo, fixtures_relative)
    if not fixtures_dir.is_dir():
        raise UsageError("UNKNOWN-FIXTURE: fixtures directory is missing")
    manifest_rel = fixtures_rel + "/FIXTURE-MANIFEST.v1.json"
    expected_rel = fixtures_rel + "/expected-findings.v1.json"
    manifest_path = resolve_under_repo(repo, manifest_rel)
    expected_path = resolve_under_repo(repo, expected_rel)
    if not manifest_path.is_file() or not expected_path.is_file():
        raise UsageError("UNKNOWN-FIXTURE: manifest or expected-findings file is missing")
    manifest, manifest_raw = load_json(manifest_path, MAX_MANIFEST_BYTES)
    expected, expected_raw = load_json(expected_path, MAX_MANIFEST_BYTES)
    if not isinstance(manifest, dict) or manifest.get("schema") != MANIFEST_SCHEMA_ID:
        raise UsageError("UNKNOWN-FIXTURE: fixture-manifest schema is not supported")
    if not isinstance(expected, dict) or expected.get("schema") != EXPECTED_SCHEMA_ID:
        raise UsageError("UNKNOWN-FIXTURE: expected-findings schema is not supported")
    findings = []
    for name in manifest:
        if name not in MANIFEST_TOP_FIELDS:
            add(findings, "MANIFEST-STALE", str(name), "manifest field is not in the v1 contract")
    if manifest.get("fixture_version") != "v1":
        add(findings, "MANIFEST-STALE", manifest_rel, "manifest fixture version is not the current v1")
    entries = manifest.get("entries")
    if not isinstance(entries, list) or len(entries) == 0:
        raise UsageError("UNKNOWN-FIXTURE: fixture-manifest entries are malformed")
    if manifest.get("fixture_version") is None:
        add(findings, "MANIFEST-STALE", manifest_rel, "manifest fixture version is missing")
    declared_records = sum(1 for entry in entries if isinstance(entry, dict) and entry.get("kind") == "record")
    if declared_records > MAX_RECORDS:
        raise UsageError("INPUT-TOO-LARGE: manifest declares " + str(declared_records) + " record entries, above the cap of " + str(MAX_RECORDS))
    expected_real, expected_contract = validate_expected_table(expected, findings)
    if expected.get("fixture_version") is not None and expected.get("fixture_version") != manifest.get("fixture_version"):
        add(findings, "MANIFEST-STALE", "fixture_version", "manifest and expected-findings fixture versions differ")
    manifest_paths = []
    records = 0
    capabilities = 0
    seen_paths = set()
    declared_paths = []
    entry_by_path = {}
    for index, entry in enumerate(entries):
        base = "entries[" + str(index) + "]"
        if not isinstance(entry, dict):
            add(findings, "MANIFEST-STALE", base, "manifest entry is not an object")
            continue
        for name in entry:
            if name not in MANIFEST_ENTRY_FIELDS:
                add(findings, "MANIFEST-STALE", base + "/" + str(name), "manifest entry field is not in the v1 contract")
        path = entry.get("path")
        if not isinstance(path, str) or not is_safe_relative(path):
            add(findings, "UNSAFE-PATH", base + "/path", "manifest entry path is unsafe")
            continue
        clean = normalise_relative(path)
        declared_paths.append(clean)
        if clean == manifest_rel:
            add(findings, "MANIFEST-STALE", base, "manifest may not include itself")
            continue
        if clean in seen_paths:
            add(findings, "MANIFEST-STALE", clean, "duplicate manifest path; only the first entry counts")
            continue
        seen_paths.add(clean)
        kind = entry.get("kind")
        if kind not in ("record", "expectations"):
            add(findings, "MANIFEST-STALE", base + "/kind", "manifest entry kind is not record or expectations")
        expected_exit = entry.get("expected_exit")
        if not is_int_not_bool(expected_exit) or expected_exit not in VALID_EXITS:
            add(findings, "MANIFEST-STALE", base + "/expected_exit", "manifest expected exit code must be the integer 0 or 1")
        byte_count = entry.get("bytes")
        if not is_int_not_bool(byte_count) or byte_count < 0:
            add(findings, "MANIFEST-STALE", base + "/bytes", "manifest byte count must be a non-negative integer")
        declared_digest = entry.get("sha256")
        if not isinstance(declared_digest, str) or SHA256_RE.match(declared_digest) is None:
            add(findings, "MANIFEST-STALE", base + "/sha256", "manifest digest is not sha256 hex")
        manifest_paths.append(clean)
        entry_by_path[clean] = entry
        resolved = resolve_manifest_entry(repo, clean, findings, fixtures_dir)
        if resolved is None:
            continue
        if not resolved.is_file():
            add(findings, "MANIFEST-MISSING-FIXTURE", clean, "manifest entry file is missing")
            continue
        try:
            declared_size = resolved.stat().st_size
        except OSError as exc:
            raise UsageError("UNKNOWN-FIXTURE: a fixture file cannot be stat()ed") from exc
        if kind == "record" and declared_size > MAX_RECORD_BYTES:
            raise UsageError("INPUT-TOO-LARGE: " + resolved.name + " exceeds the record byte cap")
        if kind == "expectations" and declared_size > MAX_MANIFEST_BYTES:
            raise UsageError("INPUT-TOO-LARGE: " + resolved.name + " exceeds the manifest byte cap")
        raw = resolved.read_bytes()
        digest = sha256_bytes(raw)
        if not is_int_not_bool(entry.get("bytes")) or entry.get("bytes") != len(raw):
            add(findings, "MANIFEST-BYTE-MISMATCH", clean, "manifest byte count does not match the fixture")
        if entry.get("sha256") != digest:
            add(findings, "MANIFEST-BYTE-MISMATCH", clean, "manifest digest does not match the fixture")
        if kind == "record":
            records += 1
            try:
                record, _ = load_json(resolved, MAX_RECORD_BYTES)
            except UsageError as exc:
                raise UsageError("UNKNOWN-FIXTURE: fixture record is unreadable: " + str(exc)) from exc
            enforce_input_caps(record)
            record_findings = []
            capabilities += validate_record(record, clean, record_findings, digest)
            actual_codes = sorted({finding["code"] for finding in record_findings})
            expectation = expected_real.get(clean)
            if expectation is None:
                add(findings, "EXPECTED-FINDINGS-MISMATCH", clean, "no expected-findings entry for this record")
            else:
                if is_int_not_bool(expected_exit) and expected_exit != expectation.get("expected_exit"):
                    add(findings, "EXPECTED-FINDINGS-MISMATCH", clean, "manifest and expected-findings exit codes differ")
                compare_expectation(record, clean, actual_codes, expectation, findings)
        elif kind == "expectations":
            if clean != expected_rel:
                add(findings, "EXPECTED-FINDINGS-MISMATCH", clean, "expectations entry does not point at expected-findings")
    if declared_paths != sorted(declared_paths):
        add(findings, "MANIFEST-STALE", "entries", "manifest entries must be sorted by canonical path")
    file_set = set()
    for candidate in fixtures_dir.rglob("*"):
        if candidate.is_file():
            try:
                relative = candidate.resolve().relative_to(repo.resolve()).as_posix()
            except (OSError, RuntimeError, ValueError):
                add(findings, "UNSAFE-PATH", fixtures_rel, "fixture file resolves outside the repository")
                continue
            if relative != manifest_rel:
                file_set.add(relative)
    for path in sorted(file_set - set(path for path in manifest_paths if isinstance(path, str))):
        add(findings, "MANIFEST-MISSING-FIXTURE", path, "fixture file is not inventoried in the manifest")
    for fixture in sorted(expected_real):
        if not fixture.startswith(fixtures_rel + "/"):
            add(findings, "UNSAFE-PATH", fixture, "expectation fixture path is outside the fixtures directory")
            continue
        if resolve_manifest_entry(repo, fixture, findings, fixtures_dir) is None:
            continue
        if fixture not in entry_by_path:
            add(findings, "MANIFEST-MISSING-FIXTURE", fixture, "expected record fixture is not in the manifest")
    if records != FIXTURE_RECORD_COUNT:
        add(findings, "MANIFEST-STALE", "entries", "manifest record count " + str(records) + " does not match the pinned fixture count " + str(FIXTURE_RECORD_COUNT))
    expected_findings_total = sum(
        len(entry["expected_findings"])
        for entry in expected_real.values()
        if is_string_list(entry.get("expected_findings"))
    )
    manifest_identity = {"path": manifest_rel, "bytes": len(manifest_raw), "sha256": sha256_bytes(manifest_raw)}
    expectations = {
        "expected_findings": expected_findings_total,
        "contract_negatives": len(expected_contract),
        "expected_file": expected_rel,
        "expected_sha256": sha256_bytes(expected_raw),
    }
    findings.sort(key=lambda item: (item["code"], item["path"], item["evidence"]))
    return findings, {"records": records, "capabilities": capabilities}, manifest_identity, expectations


def build_report(manifest_identity, checked_record, findings, counts, limits, expectations=None):
    summary = {
        "findings": len(findings),
        "errors": len(findings),
        "warnings": 0,
        "records": int(counts.get("records", 0)),
        "capabilities": int(counts.get("capabilities", 0)),
    }
    if expectations is not None:
        summary["expected_findings"] = expectations.get("expected_findings", 0)
        summary["contract_negatives"] = expectations.get("contract_negatives", 0)
    report = {
        "schema": REPORT_SCHEMA_ID,
        "tool": TOOL,
        "fixture_manifest": manifest_identity,
        "checked_record": checked_record,
        "findings": findings,
        "summary": summary,
        "limits": limits,
        "non_claims": [
            "not host/consumer qualification",
            "not a portability claim",
            "not live/production behaviour",
        ],
        "result": "FINDINGS" if findings else "CLEAN",
    }
    if expectations is not None:
        report["expected_findings_table"] = expectations
    return report


def write_report(repo, report, out_arg):
    path = Path(out_arg)
    try:
        path = (Path.cwd() / path).resolve() if not path.is_absolute() else path.resolve()
        repo_root = repo.resolve()
    except (OSError, RuntimeError, ValueError):
        print("REFUSED: --out path cannot be resolved", file=sys.stderr)
        return 2
    try:
        path.relative_to(repo_root)
    except ValueError:
        pass
    else:
        print("REFUSED: --out must resolve outside the repository", file=sys.stderr)
        return 2
    payload = json.dumps(report, indent=2, sort_keys=True, ensure_ascii=True) + "\n"
    path.write_bytes(payload.encode("utf-8"))
    return 0


def main(argv=None):
    parser = argparse.ArgumentParser(prog="check_host_record.py", description="deterministic read-only host capability record checker")
    parser.add_argument("--record", metavar="RECORD", help="one host capability record to validate")
    parser.add_argument("--fixtures", metavar="DIR", help="offline fixture directory to validate")
    parser.add_argument("--json", action="store_true", help="emit a deterministic JSON report")
    parser.add_argument("--out", metavar="PATH", help="write the report outside the repository")
    parser.add_argument("--quiet", action="store_true", help="print only the summary line")
    args = parser.parse_args(argv)
    if args.record and args.fixtures:
        print("usage error: --record and --fixtures are mutually exclusive", file=sys.stderr)
        return 2
    if not args.record and not args.fixtures:
        print("usage error: --record or --fixtures is required", file=sys.stderr)
        return 2
    repo = repo_root_for(Path(__file__))
    limits = [
        "record byte cap " + str(MAX_RECORD_BYTES),
        "manifest byte cap " + str(MAX_MANIFEST_BYTES),
        "record count cap " + str(MAX_RECORDS) + " (input-class)",
        "capability count cap " + str(MAX_CAPABILITIES) + " (input-class)",
        "capability count minimum " + str(MIN_CAPABILITIES),
        "source evidence minimum " + str(MIN_SOURCE_EVIDENCE),
        "string character cap " + str(MAX_STRING_CHARS) + " (input-class)",
        "pinned fixture record count " + str(FIXTURE_RECORD_COUNT),
        "read-only, offline, stdlib-only, no host probe",
    ]
    try:
        findings = []
        counts = {"records": 0, "capabilities": 0}
        manifest_identity = None
        checked_record = None
        expectations = None
        code = 0
        if args.record:
            record_path = resolve_under_repo(repo, args.record)
            if not record_path.is_file():
                raise UsageError("UNKNOWN-FIXTURE: record file is missing")
            record, raw = load_json(record_path, MAX_RECORD_BYTES)
            if not isinstance(record, dict):
                raise UsageError("UNKNOWN-FIXTURE: record root is not an object")
            if record.get("schema") != SCHEMA_ID:
                raise UsageError("UNKNOWN-FIXTURE: record schema is not the supported v1 id")
            record_relative = record_path.resolve().relative_to(repo.resolve()).as_posix()
            enforce_input_caps(record)
            record_findings = []
            counts["capabilities"] = validate_record(record, record_relative, record_findings, sha256_bytes(raw))
            counts["records"] = 1
            findings.extend(record_findings)
            checked_record = {"path": record_relative, "bytes": len(raw), "sha256": sha256_bytes(raw)}
            findings.sort(key=lambda item: (item["code"], item["path"], item["evidence"]))
            code = 1 if findings else 0
        if args.fixtures:
            fixtures_findings, fixture_counts, manifest_identity, expectations = validate_fixture_set(repo, args.fixtures)
            findings.extend(fixtures_findings)
            findings.sort(key=lambda item: (item["code"], item["path"], item["evidence"]))
            counts = fixture_counts
            code = 1 if findings else 0
        report = build_report(manifest_identity, checked_record, findings, counts, limits, expectations)
        payload = json.dumps(report, indent=2, sort_keys=True, ensure_ascii=True) + "\n"
        if args.out:
            out_code = write_report(repo, report, args.out)
            if out_code != 0:
                return out_code
        if args.json:
            sys.stdout.write(payload)
        elif args.quiet:
            print("findings: " + str(len(findings)) + "; records: " + str(counts["records"]) + "; capabilities: " + str(counts["capabilities"]))
        else:
            print(TOOL + " report")
            print("findings: " + str(len(findings)))
            for finding in findings:
                print("  [" + finding["code"] + "] " + finding["path"] + ": " + finding["evidence"])
            print("RESULT: " + ("FINDINGS" if findings else "CLEAN"))
        return code
    except UsageError as exc:
        print(str(exc), file=sys.stderr)
        return 2
    except Exception as exc:  # defensive fail-closed mapping
        print("internal error: " + type(exc).__name__, file=sys.stderr)
        return 3


if __name__ == "__main__":
    sys.exit(main())
