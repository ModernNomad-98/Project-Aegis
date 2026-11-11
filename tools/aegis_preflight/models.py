"""Models and parsing helpers for the C2.2 preflight bundle.

The bundle is a supplied, explicit-path description of the records a preflight
run may read.  This module owns the vocabulary, canonical serialization and
small file helpers; checks.py owns PF-01..PF-10.  Nothing here writes, calls a
network or trusts a declared hash without recomputing it.
"""

from __future__ import annotations

import dataclasses
import hashlib
import json
import typing
from pathlib import Path

SCHEMA_VERSION = "aegis.preflight/v1"
OUTPUT_SCHEMA_VERSION = "aegis.preflight-output/v1"
TOOL_NAME = "aegis-preflight"
TOOL_VERSION = "1.0.0"

CHECK_IDS = (
    "PF-01",
    "PF-02",
    "PF-03",
    "PF-04",
    "PF-05",
    "PF-06",
    "PF-07",
    "PF-08",
    "PF-09",
    "PF-10",
)

STATUSES = ("PASS", "FAIL", "BLOCKED", "UNRUN")
CLAIMS = ("MECHANICAL_CHECKS_ONLY",)
GATE_STATUSES = ("present", "absent", "not applicable")
STAGE_VERDICTS = {
    "B": ("ACCEPT", "REVISE"),
    "D": ("ACCEPT", "REVISE"),
    "E": ("PASS", "INCOMPLETE", "FAIL"),
}
TRIAGE_CLASSES = ("BLOCKING", "RESIDUAL", "NIT")
TRIAGE_DISPOSITIONS = ("FIXED", "RESIDUAL_ACCEPTED", "NIT_ACCEPTED", "REJECTED", "UNRUN")
EVIDENCE_RESULTS = ("PASS", "FAIL", "UNRUN", "BLOCKED")
EVIDENCE_ASSURANCES = ("NONE", "AUDITABLE", "VERIFIED")
EVIDENCE_REQUIRED_FIELDS = (
    "evidence_id",
    "kind",
    "bytes",
    "sha256",
    "scope",
    "source_head",
    "method",
    "environment",
    "result",
    "retention",
    "assurance",
    "invalidation",
)

# The only subprocess modules the preflight may invoke.  git plumbing is
# restricted to read-only subcommands.
SUBPROCESS_MODULES = ("tools.aegis_verdict_gate", "tools.aegis_evidence_reuse")
GIT_SUBCOMMANDS = ("rev-parse", "cat-file", "log", "merge-base")

NON_CLAIMS = (
    "auditable tooling, not enforcement",
    "not a required status context and not wired into CI",
    "no settings, branch-protection, identity or label change",
    "an exit 0 means mechanical checks passed, not approval, readiness or merge permission",
    "production readiness remains unreachable while owner decision T6 is undecided",
    "the revision-state store remains UNVERIFIED under T24",
    "mounted coverage is UNKNOWN",
    "no UNRUN, UNKNOWN or BLOCKED result is converted to PASS",
)


class ModelError(Exception):
    """A fatal bundle/file error (the CLI maps it to exit 2)."""


def canonical_bytes(value: object) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def digest(value: object) -> str:
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def sha256_bytes(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def is_hex(value: object, length: int) -> bool:
    if not isinstance(value, str) or len(value) != length:
        return False
    return all(character in "0123456789abcdef" for character in value)


def is_hex40(value: object) -> bool:
    return is_hex(value, 40)


def is_hex64(value: object) -> bool:
    return is_hex(value, 64)


def is_plain_int(value: object) -> bool:
    return isinstance(value, int) and not isinstance(value, bool)


def is_nonempty_string(value: object) -> bool:
    return isinstance(value, str) and bool(value)


def is_string_list(value: object) -> bool:
    return isinstance(value, list) and all(isinstance(item, str) and item for item in value)


def read_json(path: Path) -> object:
    try:
        raw = path.read_bytes()
    except OSError as error:
        raise ModelError("required file is unreadable: %s (%s)" % (path, error)) from error
    try:
        return json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, ValueError) as error:
        raise ModelError("required file is not valid UTF-8 JSON: %s (%s)" % (path, error)) from error


def read_envelope(path: Path) -> typing.Tuple[typing.Optional[typing.Dict[str, object]], str]:
    """Read a C1.1a input/stage-declaration envelope without trusting it."""

    try:
        document = read_json(path)
    except ModelError as error:
        return None, str(error)
    if not isinstance(document, dict) or not isinstance(document.get("payload"), dict):
        return None, "envelope has no payload object: %s" % path
    return document, ""


@dataclasses.dataclass
class Bundle:
    """One loaded preflight bundle plus its resolution base directory."""

    path: Path
    document: typing.Dict[str, object]

    @property
    def base_dir(self) -> Path:
        return self.path.parent

    def resolve(self, value: str) -> Path:
        candidate = Path(value)
        if candidate.is_absolute():
            return candidate
        return (self.base_dir / candidate).resolve()

    def section(self, *keys: str) -> typing.Optional[typing.Dict[str, object]]:
        current: object = self.document
        for key in keys:
            if not isinstance(current, dict):
                return None
            current = current.get(key)
        return typing.cast(typing.Dict[str, object], current) if isinstance(current, dict) else None

    def value(self, *keys: str) -> object:
        current: object = self.document
        for key in keys:
            if not isinstance(current, dict):
                return None
            current = current.get(key)
        return current


def load_bundle(path: Path) -> Bundle:
    document = read_json(path)
    if not isinstance(document, dict):
        raise ModelError("preflight bundle is not a JSON object: %s" % path)
    return Bundle(path=path.resolve(), document=document)


def bundle_payload(bundle: Bundle) -> typing.Dict[str, object]:
    return {key: value for key, value in bundle.document.items() if key != "provenance"}


def file_report(path: Path) -> typing.Tuple[int, str]:
    raw = path.read_bytes()
    return len(raw), sha256_bytes(raw)


def check_record(check_id: str, status: str, reason_code: str, message: str, evidence_ref: str = "") -> typing.Dict[str, object]:
    if check_id not in CHECK_IDS:
        raise ValueError("unknown preflight check id %r" % check_id)
    if status not in STATUSES:
        raise ValueError("unknown preflight status %r" % status)
    return {
        "check_id": check_id,
        "status": status,
        "reason_code": reason_code,
        "message": message,
        "evidence_ref": evidence_ref,
    }


def build_output(
    subject: object,
    checks: typing.Sequence[typing.Mapping[str, object]],
    fixture_mode: bool,
) -> typing.Dict[str, object]:
    by_id = {str(item["check_id"]): item for item in checks}
    ordered = [dict(by_id[check_id]) for check_id in CHECK_IDS if check_id in by_id]
    totals = {"pass": 0, "fail": 0, "blocked": 0, "unrun": 0}
    for item in ordered:
        key = str(item["status"]).lower()
        totals[key] = totals.get(key, 0) + 1
    exit_code = 0 if totals["fail"] == 0 and totals["blocked"] == 0 and totals["unrun"] == 0 else 1
    return {
        "schema_version": OUTPUT_SCHEMA_VERSION,
        "subject": subject,
        "checks": ordered,
        "totals": totals,
        "exit_code": exit_code,
        "assurance": {
            "claim": "AUDITABLE",
            "mounted_coverage": "UNKNOWN",
            "mode": "FIXTURE" if fixture_mode else "PRODUCTION",
        },
        "non_claims": list(NON_CLAIMS),
    }


def self_test() -> typing.Dict[str, object]:
    sample = {"b": 2, "a": 1}
    return {
        "ok": canonical_bytes(sample) == b'{"a":1,"b":2}' and digest(sample) == digest({"a": 1, "b": 2}),
        "schema_version": SCHEMA_VERSION,
        "check_ids": list(CHECK_IDS),
        "canonical_sample_sha256": digest(sample),
    }
