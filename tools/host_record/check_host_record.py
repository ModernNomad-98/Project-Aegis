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


class InternalError(Exception):
    """Unexpected state mapped to exit code 3."""


def repo_root_for(script_path):
    return Path(script_path).resolve().parents[2]


def canonical_json(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def sha256_bytes(raw):
    return hashlib.sha256(raw).hexdigest()


def is_safe_relative(text):
    if not isinstance(text, str) or not text:
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
    candidate = (repo / relative).resolve()
    try:
        candidate.relative_to(repo.resolve())
    except ValueError as exc:
        raise UsageError("UNSAFE-PATH: path escapes the repository") from exc
    return candidate


def load_json(path, max_bytes):
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


def config_digest_of(input_names, input_values):
    payload = canonical_json({"input_names": input_names, "input_values": input_values})
    return sha256_bytes(payload.encode("utf-8"))


def validate_record(record, record_relative, findings):
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
    if isinstance(source_evidence, list):
        if len(source_evidence) < MIN_SOURCE_EVIDENCE:
            add(findings, "SOURCE-EVIDENCE-EMPTY", "source_evidence", "source evidence count " + str(len(source_evidence)) + " is below the v1 minimum of " + str(MIN_SOURCE_EVIDENCE))
        for index, item in enumerate(source_evidence):
            base = "source_evidence[" + str(index) + "]"
            if not isinstance(item, dict):
                add(findings, "SCHEMA", base, "source evidence entry is not an object")
                continue
            for name in ("path", "bytes", "sha256", "note"):
                if name not in item:
                    add(findings, "MISSING-FIELD", base + "/" + name, "source evidence field is missing")
            path = item.get("path")
            if not isinstance(path, str) or not is_safe_relative(path):
                add(findings, "UNSAFE-PATH", base + "/path", "source evidence path is unsafe")
            elif path == record_relative:
                add(findings, "UNSAFE-PATH", base + "/path", "record may not cite itself")
            digest = item.get("sha256")
            if not isinstance(digest, str) or SHA256_RE.match(digest) is None:
                add(findings, "SCHEMA", base + "/sha256", "source evidence digest is not sha256 hex")
    host = record.get("host")
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
        if not isinstance(profile, str) or len(profile.strip()) < 3:
            add(findings, "BAD-PACKAGE-BINDING", "package_binding/profile_id", "profile id is missing or too short")
    capabilities = record.get("capabilities")
    capability_count = 0
    if isinstance(capabilities, list):
        capability_count = len(capabilities)
        if len(capabilities) > MAX_CAPABILITIES:
            add(findings, "SCHEMA", "capabilities", "capability count exceeds the v1 cap")
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
            refs = item.get("evidence_refs")
            if isinstance(refs, list):
                for ref_index, ref in enumerate(refs):
                    if not isinstance(ref, str) or not is_safe_relative(ref):
                        add(findings, "UNSAFE-PATH", base + "/evidence_refs[" + str(ref_index) + "]", "evidence reference is unsafe")
    else:
        add(findings, "AGGREGATE-CAPABILITY", "capabilities", "capabilities must be a separate-entry array, not an aggregate value")
    for name in ("limits", "non_claims"):
        value = record.get(name)
        if not isinstance(value, list) or len(value) == 0:
            add(findings, "MISSING-FIELD", name, "required list field is absent or empty")
    non_claims = record.get("non_claims")
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


def normalise_record_for_tamper(record):
    return json.loads(json.dumps(record))


def validate_expected_table(expected, findings):
    entries = expected.get("entries")
    if not isinstance(entries, list):
        add(findings, "EXPECTED-FINDINGS-MISMATCH", "entries", "expected-findings table has no entries list")
        return {}, []
    real = {}
    contract = []
    for index, entry in enumerate(entries):
        if not isinstance(entry, dict):
            add(findings, "EXPECTED-FINDINGS-MISMATCH", "entries[" + str(index) + "]", "expectation entry is not an object")
            continue
        fixture = entry.get("fixture")
        if entry.get("contract_negative") is True:
            contract.append(entry)
            continue
        if not isinstance(fixture, str):
            add(findings, "EXPECTED-FINDINGS-MISMATCH", "entries[" + str(index) + "]", "expectation fixture path is missing")
            continue
        real[fixture] = entry
    if len(entries) != 8:
        add(findings, "EXPECTED-FINDINGS-MISMATCH", "entries", "expected-findings must have exactly eight entries")
    expected_contract_codes = sorted(["MANIFEST-STALE", "EXPECTED-FINDINGS-MISMATCH"])
    actual_contract_codes = sorted(
        code
        for entry in contract
        for code in (entry.get("expected_findings") or [])
        if isinstance(code, str)
    )
    if len(contract) != 2 or actual_contract_codes != expected_contract_codes:
        add(findings, "EXPECTED-FINDINGS-MISMATCH", "entries", "contract-negative expectations must be exactly two with the pinned codes")
    return real, contract


def compare_expectation(record_relative, actual_codes, capability_count, expectation, findings):
    expected_codes = expectation.get("expected_findings")
    expected_exit = expectation.get("expected_exit")
    if not isinstance(expected_codes, list):
        add(findings, "EXPECTED-FINDINGS-MISMATCH", record_relative, "expectation findings list is missing")
        return
    actual_exit = 0 if len(actual_codes) == 0 else 1
    if actual_exit != expected_exit or sorted(actual_codes) != sorted(expected_codes):
        add(findings, "EXPECTED-FINDINGS-MISMATCH", record_relative, "observed codes/exit differ from the expected-findings table")


def validate_fixture_set(repo, fixtures_relative):
    fixtures_dir = resolve_under_repo(repo, fixtures_relative)
    if not fixtures_dir.is_dir():
        raise UsageError("UNKNOWN-FIXTURE: fixtures directory is missing")
    manifest_path = fixtures_dir / "FIXTURE-MANIFEST.v1.json"
    expected_path = fixtures_dir / "expected-findings.v1.json"
    if not manifest_path.is_file() or not expected_path.is_file():
        raise UsageError("UNKNOWN-FIXTURE: manifest or expected-findings file is missing")
    manifest, manifest_raw = load_json(manifest_path, MAX_MANIFEST_BYTES)
    expected, expected_raw = load_json(expected_path, MAX_MANIFEST_BYTES)
    if not isinstance(manifest, dict) or manifest.get("schema") != MANIFEST_SCHEMA_ID:
        raise UsageError("UNKNOWN-FIXTURE: fixture-manifest schema is not supported")
    if not isinstance(expected, dict) or expected.get("schema") != EXPECTED_SCHEMA_ID:
        raise UsageError("UNKNOWN-FIXTURE: expected-findings schema is not supported")
    findings = []
    if manifest.get("fixture_version") != "v1":
        add(findings, "MANIFEST-STALE", fixtures_relative + "/FIXTURE-MANIFEST.v1.json", "manifest fixture version is not the current v1")
    entries = manifest.get("entries")
    if not isinstance(entries, list) or len(entries) == 0:
        raise UsageError("UNKNOWN-FIXTURE: fixture-manifest entries are malformed")
    if manifest.get("fixture_version") is None:
        add(findings, "MANIFEST-STALE", fixtures_relative + "/FIXTURE-MANIFEST.v1.json", "manifest fixture version is missing")
    expected_real, expected_contract = validate_expected_table(expected, findings)
    manifest_rel = fixtures_relative.rstrip("/") + "/FIXTURE-MANIFEST.v1.json"
    expected_rel = fixtures_relative.rstrip("/") + "/expected-findings.v1.json"
    manifest_paths = []
    records = 0
    capabilities = 0
    expected_findings_total = sum(len(entry.get("expected_findings") or []) for entry in expected_real.values())
    entry_by_path = {}
    for index, entry in enumerate(entries):
        base = "entries[" + str(index) + "]"
        if not isinstance(entry, dict):
            add(findings, "MANIFEST-STALE", base, "manifest entry is not an object")
            continue
        path = entry.get("path")
        if not isinstance(path, str) or not is_safe_relative(path):
            add(findings, "UNSAFE-PATH", base + "/path", "manifest entry path is unsafe")
            continue
        if path == manifest_rel:
            add(findings, "MANIFEST-STALE", base, "manifest may not include itself")
        manifest_paths.append(path)
        entry_by_path[path] = entry
        resolved = (repo / path).resolve()
        if not resolved.is_file():
            add(findings, "MANIFEST-MISSING-FIXTURE", path, "manifest entry file is missing")
            continue
        raw = resolved.read_bytes()
        digest = sha256_bytes(raw)
        if entry.get("bytes") != len(raw):
            add(findings, "MANIFEST-BYTE-MISMATCH", path, "manifest byte count does not match the fixture")
        if entry.get("sha256") != digest:
            add(findings, "MANIFEST-BYTE-MISMATCH", path, "manifest digest does not match the fixture")
        kind = entry.get("kind")
        if kind == "record":
            records += 1
            try:
                record, _ = load_json(resolved, MAX_RECORD_BYTES)
            except UsageError as exc:
                raise UsageError("UNKNOWN-FIXTURE: fixture record is unreadable: " + str(exc)) from exc
            record_findings = []
            capabilities += validate_record(record, path, record_findings)
            actual_codes = sorted({finding["code"] for finding in record_findings})
            expectation = expected_real.get(path)
            if expectation is None:
                add(findings, "EXPECTED-FINDINGS-MISMATCH", path, "no expected-findings entry for this record")
            else:
                compare_expectation(path, actual_codes, capabilities, expectation, findings)
        elif kind == "expectations":
            if path != expected_rel:
                add(findings, "EXPECTED-FINDINGS-MISMATCH", path, "expectations entry does not point at expected-findings")
        else:
            add(findings, "MANIFEST-STALE", base + "/kind", "manifest entry kind is not record or expectations")
    if any(chr(92) in str(path) for path in manifest_paths):
        add(findings, "UNSAFE-PATH", "entries", "manifest paths must use forward slashes")
    file_set = set()
    for candidate in fixtures_dir.rglob("*"):
        if candidate.is_file():
            relative = candidate.resolve().relative_to(repo.resolve()).as_posix()
            if relative != manifest_rel:
                file_set.add(relative)
    for path in sorted(file_set - set(path for path in manifest_paths if isinstance(path, str))):
        add(findings, "MANIFEST-MISSING-FIXTURE", path, "fixture file is not inventoried in the manifest")
    for fixture in sorted(expected_real):
        if fixture not in entry_by_path:
            add(findings, "MANIFEST-MISSING-FIXTURE", fixture, "expected record fixture is not in the manifest")
    if records != MAX_RECORDS and records != 6:
        add(findings, "MANIFEST-STALE", "entries", "manifest record count does not match the fixture set")
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
    if not path.is_absolute():
        path = (Path.cwd() / path).resolve()
    else:
        path = path.resolve()
    try:
        path.relative_to(repo.resolve())
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
    if not args.record and not args.fixtures:
        print("usage error: --record or --fixtures is required", file=sys.stderr)
        return 2
    repo = repo_root_for(Path(__file__))
    limits = [
        "record byte cap " + str(MAX_RECORD_BYTES),
        "manifest byte cap " + str(MAX_MANIFEST_BYTES),
        "record count cap " + str(MAX_RECORDS),
        "capability count cap " + str(MAX_CAPABILITIES),
        "capability count minimum " + str(MIN_CAPABILITIES),
        "source evidence minimum " + str(MIN_SOURCE_EVIDENCE),
        "string character cap " + str(MAX_STRING_CHARS),
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
            record_findings = []
            counts["capabilities"] = validate_record(record, record_relative, record_findings)
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
    except InternalError as exc:
        print("internal error: " + str(exc), file=sys.stderr)
        return 3
    except Exception as exc:  # defensive fail-closed mapping
        print("internal error: " + type(exc).__name__, file=sys.stderr)
        return 3


if __name__ == "__main__":
    sys.exit(main())
