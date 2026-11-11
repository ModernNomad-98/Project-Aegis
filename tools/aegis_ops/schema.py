"""Closed schemas and deterministic primitives for the read-only C3/C4 ops tooling.

This module is the only schema home in `tools/aegis_ops/`.  It defines the
`aegis.ops-*/v1` record family, canonical JSON serialisation, and small
structural validators shared by the feature modules.  It does not restate the
merged checker's verdict field list: the merged bound-verdict schema (version
2.1) remains owned
by `scripts/aegis_verdict_gate/catalogue.py` and is consumed by version.

The package is standard-library only.  Nothing here writes a file, opens a
socket, starts a subprocess or reads the wall clock; callers pass the bytes or
the facts they want checked.
"""

from __future__ import annotations

import hashlib
import json
import re
import typing

PACKAGE_VERSION = "1.0.0"
RECORD_FAMILY = "aegis.ops/v1"

# Assurance vocabulary is deliberately fixed.  It is displayed by every report
# and is never promoted by this tooling.
ASSURANCE_CLAIM = "AUDITABLE"
MOUNTED_COVERAGE = "UNKNOWN"
AUTHORITY_STATUS = {
    "T4": "DECLINED",
    "T5": "NOT_ASSUMED",
    "T6": "UNVERIFIED+BLOCKED",
    "T7": "OPEN",
    "T24": "UNVERIFIED",
}
NOT_VERIFIABLE = (
    "production readiness (T6 UNVERIFIED+BLOCKED)",
    "store provenance (T24 UNVERIFIED)",
    "unavailable-review dispositions (T7 OPEN)",
    "mounted host coverage (T5 NOT_ASSUMED)",
)

SCHEMA_EVENT = "aegis.ops-event-catalogue/v1"
SCHEMA_SETTLEMENT = "aegis.ops-settlement/v1"
SCHEMA_ROUTING = "aegis.ops-routing/v1"
SCHEMA_HOLDERS = "aegis.ops-stage-holders/v1"
SCHEMA_INBOX = "aegis.ops-inbox/v1"
SCHEMA_PILOT_METRICS = "aegis.ops-pilot-metrics/v1"
SCHEMA_SUPPORT_MATRIX = "aegis.ops-support-matrix/v1"

KNOWN_SCHEMAS = (
    SCHEMA_EVENT,
    SCHEMA_SETTLEMENT,
    SCHEMA_ROUTING,
    SCHEMA_HOLDERS,
    SCHEMA_INBOX,
    SCHEMA_PILOT_METRICS,
    SCHEMA_SUPPORT_MATRIX,
)

PRE_AUDIT_STATES = ("pass", "fail", "neutral", "unrun", "bypassed")
REVIEW_SOURCE_STATES = ("SETTLED", "PENDING", "UNAVAILABLE_DISPOSITIONED")
DUPLICATE_SEMANTICS = ("NO_OP", "RESTART_NOT_ALLOWED", "INVALID")
HOLDER_STATES = ("ACTIVE", "REPLACED", "SUPERSEDED", "COMPLETED", "DECLINED")
REPLACEMENT_REASONS = ("INVALID", "INCOMPLETE", "UNAVAILABLE", "CONFLICT", "STALE")
UNAVAILABILITY_ROUTES = ("WAIT_BOUNDED", "REPLACE_EXPLICITLY", "BLOCKED")
ASSURANCE_CLASSES = ("QUALIFIED", "UNQUALIFIED", "UNRUN", "UNKNOWN")

HEX40_RE = re.compile(r"^[0-9a-f]{40}$")
HEX64_RE = re.compile(r"^[0-9a-f]{64}$")
ISO_INSTANT_RE = re.compile(r"^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z$")


class Issue(typing.NamedTuple):
    """One deterministic defect or blocked condition."""

    code: str
    detail: str

    def as_dict(self) -> typing.Dict[str, str]:
        return {"code": self.code, "detail": self.detail}


class Report:
    """An ordered, deterministic validation report."""

    def __init__(self) -> None:
        self.issues: typing.List[Issue] = []

    def add(self, code: str, detail: str) -> None:
        self.issues.append(Issue(code, detail))

    def extend(self, issues: typing.Iterable[Issue]) -> None:
        self.issues.extend(issues)

    @property
    def valid(self) -> bool:
        return not self.issues

    def codes(self) -> typing.List[str]:
        return sorted({issue.code for issue in self.issues})

    def as_dict(self) -> typing.Dict[str, object]:
        return {
            "valid": self.valid,
            "issues": [issue.as_dict() for issue in self.issues],
            "codes": self.codes(),
        }


def canonical_bytes(value: object) -> bytes:
    """Canonical JSON bytes: sorted keys, no insignificant whitespace."""

    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    ).encode("utf-8")


def sha256_hex(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def digest(value: object) -> str:
    return sha256_hex(canonical_bytes(value))


def is_nonempty_str(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def is_bool(value: object) -> bool:
    return isinstance(value, bool)


def is_int(value: object) -> bool:
    return isinstance(value, int) and not isinstance(value, bool)


def is_number(value: object) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool)


def is_iso_instant(value: object) -> bool:
    return isinstance(value, str) and bool(ISO_INSTANT_RE.match(value))


def check_object(
    value: object,
    where: str,
    required: typing.Sequence[str],
    optional: typing.Sequence[str],
    report: Report,
) -> typing.Optional[typing.Dict[str, object]]:
    """Reject a non-object and any field outside the closed shape."""

    if not isinstance(value, dict):
        report.add("SCHEMA_NOT_OBJECT", "%s must be an object" % where)
        return None
    allowed = set(required) | set(optional)
    unknown = sorted(set(value) - allowed)
    if unknown:
        report.add(
            "SCHEMA_UNKNOWN_FIELD",
            "%s has field(s) outside the closed schema: %s" % (where, ", ".join(unknown)),
        )
    missing = [key for key in required if key not in value]
    if missing:
        report.add(
            "SCHEMA_MISSING_FIELD",
            "%s is missing required field(s): %s" % (where, ", ".join(missing)),
        )
    return value


def check_string(
    value: object, where: str, report: Report, allow_empty: bool = False
) -> typing.Optional[str]:
    if not isinstance(value, str):
        report.add("SCHEMA_NOT_STRING", "%s must be a string" % where)
        return None
    if not allow_empty and not value.strip():
        report.add("SCHEMA_EMPTY_STRING", "%s must be non-empty" % where)
        return None
    return value


def check_hex40(value: object, where: str, report: Report) -> typing.Optional[str]:
    text = check_string(value, where, report)
    if text is not None and not HEX40_RE.match(text):
        report.add("SCHEMA_NOT_HEX40", "%s must be a 40-hex commit/tree id" % where)
        return None
    return text


def check_hex64(value: object, where: str, report: Report) -> typing.Optional[str]:
    text = check_string(value, where, report)
    if text is not None and not HEX64_RE.match(text):
        report.add("SCHEMA_NOT_HEX64", "%s must be a 64-hex sha256" % where)
        return None
    return text


def check_iso(value: object, where: str, report: Report) -> typing.Optional[str]:
    text = check_string(value, where, report)
    if text is not None and not is_iso_instant(text):
        report.add(
            "SCHEMA_NOT_ISO_INSTANT",
            "%s must be an ISO-8601 UTC instant (YYYY-MM-DDTHH:MM:SSZ)" % where,
        )
        return None
    return text


def check_enum(
    value: object,
    where: str,
    allowed: typing.Sequence[str],
    report: Report,
) -> typing.Optional[str]:
    text = check_string(value, where, report)
    if text is not None and text not in allowed:
        report.add(
            "SCHEMA_NOT_IN_VOCABULARY",
            "%s value %r is not in %s" % (where, text, ", ".join(allowed)),
        )
        return None
    return text


def check_schema_version(
    document: typing.Mapping[str, object],
    expected: str,
    report: Report,
) -> None:
    version = document.get("schema_version")
    if version != expected:
        report.add(
            "SCHEMA_VERSION_MISMATCH",
            "schema_version must be %r, not %r" % (expected, version),
        )


def classify_docs_skills(paths: typing.Iterable[str]) -> bool:
    """The closed E1 `docs_skills` predicate.

    True only for a non-empty changed-path set in which every path is under
    `docs/` or `.claude/skills/`.  "Other non-code paths" is not guessed:
    the predicate is enumerated, so an unmapped path is never silently
    classified as documentation.
    """

    materialised = [path for path in paths if isinstance(path, str) and path]
    if not materialised:
        return False
    return all(
        path.startswith("docs/") or path.startswith(".claude/skills/")
        for path in materialised
    )


def base_report(schema: str) -> typing.Dict[str, object]:
    return {
        "schema_version": schema,
        "assurance": {
            "claim": ASSURANCE_CLAIM,
            "mounted_coverage": MOUNTED_COVERAGE,
            "authority": dict(AUTHORITY_STATUS),
            "not_verifiable": list(NOT_VERIFIABLE),
        },
    }


def self_test() -> typing.Dict[str, object]:
    """Built-in schema and determinism checks (no I/O, no clock)."""

    checks: typing.List[typing.Dict[str, object]] = []

    vector = {"a": 1, "b": [2, 3]}
    expected = "efbd0040190fb0871831e606c581f8a66db79d8e2bb836745a70051306956070"
    checks.append(
        {
            "check": "canonical_digest_vector",
            "ok": digest(vector) == expected,
            "expected": expected,
            "actual": digest(vector),
        }
    )
    checks.append(
        {
            "check": "deterministic_key_order",
            "ok": canonical_bytes({"z": 1, "a": 2}) == canonical_bytes({"a": 2, "z": 1}),
        }
    )
    checks.append(
        {
            "check": "docs_skills_closed_predicate",
            "ok": classify_docs_skills(["docs/operations/README.md"])
            and classify_docs_skills([".claude/skills/x/SKILL.md"])
            and not classify_docs_skills(["docs/operations/README.md", "tools/aegis_ops/__init__.py"])
            and not classify_docs_skills([]),
        }
    )
    checks.append(
        {
            "check": "closed_schema_family_count",
            "ok": len(KNOWN_SCHEMAS) == 7,
            "count": len(KNOWN_SCHEMAS),
        }
    )
    return {
        "schema_version": "aegis.ops-self-test/v1",
        "ok": all(check["ok"] for check in checks),
        "checks": checks,
        "package_version": PACKAGE_VERSION,
    }
