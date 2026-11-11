"""Closed schema for the aegis.evidence-reuse/1 record.

This module owns the field vocabulary and the shape checks (RU-01).  The
semantic rules RU-02..RU-12 live in validate.py; the companion JSON Schema at
docs/conformance/evidence-reuse-v1.schema.json mirrors this vocabulary and a
test compares the two so they cannot drift silently.

The record is a *decision record*, not an approval.  It preserves the original
evidence identity, binds source and target heads, and names the independent
qualifier.  No field in this schema can waive required CI or a mandatory
finding.
"""

from __future__ import annotations

import hashlib
import json
import typing

SCHEMA_VERSION = "aegis.evidence-reuse/1"
VALIDATION_SCHEMA_VERSION = "aegis.evidence-reuse-validation/v1"

DELTA_CLASSES = (
    "DOCS_TEXT_ONLY",
    "DOCSTRING_COMMENT_TEXT_ONLY_CODE",
    "TEST_CHANGE",
    "CONFIG_WORKFLOW_POLICY_GENERATED_DEPENDENCY",
    "BEHAVIOR_CHANGE",
    "OTHER",
)
DECISIONS = ("PROPOSED", "VALID", "INVALID", "STALE")
AUTHORITY_KINDS = ("REGISTER_ENTRY", "OWNER_LINE_RECORD", "UNKNOWN")
CHECK_KINDS = ("DIFF_SCOPE", "REQUIRED_CI", "AFFECTED_INPUTS", "REVIEWED_DIFF")
CHECK_RESULTS = ("PASS", "FAIL", "UNRUN")
# The four non-claims a VALID decision must explicitly exclude.  The list is
# closed: a decision that does not exclude all four is INVALID under RU-10.
EXCLUDED_CLAIMS = ("APPROVAL", "BEHAVIORAL_EQUIVALENCE", "CI_WAIVER", "COPIED_PASS")
INVALIDATION_EVENTS = ("TARGET_HEAD_MOVE", "SOURCE_EVIDENCE_CHANGE", "POLICY_CHANGE")

TOP_LEVEL_FIELDS = (
    "schema_version",
    "reuse_id",
    "subject",
    "source",
    "target",
    "delta_class",
    "affected_inputs",
    "full_diff",
    "comparison",
    "excluded_claims",
    "target_delta_checks",
    "independence",
    "decision",
    "decision_authority",
    "invalid_after",
    "provenance",
)

SUBJECT_FIELDS = ("repo", "change_id")
REPO_FIELDS = ("owner", "name")
SOURCE_FIELDS = (
    "evidence_ids",
    "source_head",
    "source_tree",
    "source_base",
    "source_records_sha256",
    "requirement_ids",
)
TARGET_FIELDS = ("target_head", "target_tree", "target_base")
FULL_DIFF_FIELDS = ("name_only_ref", "name_only_sha256", "file_count")
COMPARISON_FIELDS = ("method", "tool", "tool_version", "ast_stripped", "ast_equality_sha256")
CHECK_FIELDS = ("check_id", "kind", "result", "evidence_ref")
INDEPENDENCE_FIELDS = ("qualifier_identity_ref", "class", "attestation_ref")
AUTHORITY_FIELDS = ("authority_kind", "authority_ref_id", "authority_ref_sha256")
PROVENANCE_FIELDS = (
    "source_ref",
    "as_of",
    "producer_role",
    "producer_identity_ref",
    "declared_payload_sha256",
    "declared_payload_bytes",
)

HEX40 = 40
HEX64 = 64


class Violation(typing.NamedTuple):
    """One rule violation, named by its RU id and a stable machine code."""

    rule_id: str
    code: str
    detail: str

    def as_dict(self) -> typing.Dict[str, str]:
        return {"rule_id": self.rule_id, "code": self.code, "detail": self.detail}


def canonical_bytes(value: object) -> bytes:
    """Deterministic JSON bytes: sorted keys, no whitespace, UTF-8."""

    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def digest(value: object) -> str:
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def payload_of(record: typing.Mapping[str, object]) -> typing.Dict[str, object]:
    """The record payload covered by provenance (the record minus provenance)."""

    return {key: value for key, value in record.items() if key != "provenance"}


def payload_digest(record: typing.Mapping[str, object]) -> str:
    return digest(payload_of(record))


def payload_bytes(record: typing.Mapping[str, object]) -> int:
    return len(canonical_bytes(payload_of(record)))


def is_hex(value: object, length: int) -> bool:
    if not isinstance(value, str) or len(value) != length:
        return False
    return all(character in "0123456789abcdef" for character in value)


def _is_plain_int(value: object) -> bool:
    return isinstance(value, int) and not isinstance(value, bool)


def _is_string_list(value: object) -> bool:
    return isinstance(value, list) and all(isinstance(item, str) and item for item in value)


def _check_object(
    value: object,
    path: str,
    required: typing.Sequence[str],
    allowed: typing.Sequence[str],
    issues: typing.List[Violation],
) -> typing.Optional[typing.Dict[str, object]]:
    if not isinstance(value, dict):
        issues.append(Violation("RU-01", "RU-01_NOT_OBJECT", "%s is not an object" % path))
        return None
    for key in required:
        if key not in value:
            issues.append(
                Violation("RU-01", "RU-01_MISSING_FIELD", "%s.%s is missing" % (path, key))
            )
    for key in sorted(set(value) - set(allowed)):
        issues.append(
            Violation("RU-01", "RU-01_UNKNOWN_FIELD", "%s.%s is not in the closed schema" % (path, key))
        )
    return value


def _require_type(
    container: typing.Mapping[str, object],
    key: str,
    path: str,
    expected: type,
    issues: typing.List[Violation],
    nullable: bool = False,
) -> None:
    value = container.get(key)
    if value is None and nullable:
        return
    if expected is int:
        if not _is_plain_int(value):
            issues.append(
                Violation("RU-01", "RU-01_TYPE_MISMATCH", "%s.%s must be an integer" % (path, key))
            )
        return
    if not isinstance(value, expected) or (expected is str and not value):
        issues.append(
            Violation(
                "RU-01",
                "RU-01_TYPE_MISMATCH",
                "%s.%s must be a non-empty %s" % (path, key, expected.__name__),
            )
        )


def validate_shape(document: object) -> typing.List[Violation]:
    """RU-01: closed schema.  Returns every shape violation it can see."""

    issues: typing.List[Violation] = []
    record = _check_object(document, "record", TOP_LEVEL_FIELDS, TOP_LEVEL_FIELDS, issues)
    if record is None:
        return issues
    if record.get("schema_version") != SCHEMA_VERSION:
        issues.append(
            Violation(
                "RU-01",
                "RU-01_SCHEMA_VERSION",
                "schema_version must be %r" % SCHEMA_VERSION,
            )
        )
    _require_type(record, "reuse_id", "record", str, issues)

    subject = _check_object(record.get("subject"), "record.subject", SUBJECT_FIELDS, SUBJECT_FIELDS, issues)
    if subject is not None:
        repo = _check_object(subject.get("repo"), "record.subject.repo", REPO_FIELDS, REPO_FIELDS, issues)
        if repo is not None:
            _require_type(repo, "owner", "record.subject.repo", str, issues)
            _require_type(repo, "name", "record.subject.repo", str, issues)
        change_id = subject.get("change_id")
        if not (isinstance(change_id, str) and change_id) and not _is_plain_int(change_id):
            issues.append(
                Violation(
                    "RU-01",
                    "RU-01_TYPE_MISMATCH",
                    "record.subject.change_id must be a non-empty string or an integer",
                )
            )

    source = _check_object(record.get("source"), "record.source", SOURCE_FIELDS, SOURCE_FIELDS, issues)
    if source is not None:
        for key in ("evidence_ids", "source_records_sha256", "requirement_ids"):
            if not _is_string_list(source.get(key)) or not source.get(key):
                issues.append(
                    Violation(
                        "RU-01",
                        "RU-01_TYPE_MISMATCH",
                        "record.source.%s must be a non-empty list of non-empty strings" % key,
                    )
                )
        for key in ("source_head", "source_tree", "source_base"):
            _require_type(source, key, "record.source", str, issues)

    target = _check_object(record.get("target"), "record.target", TARGET_FIELDS, TARGET_FIELDS, issues)
    if target is not None:
        for key in TARGET_FIELDS:
            _require_type(target, key, "record.target", str, issues)

    if record.get("delta_class") not in DELTA_CLASSES:
        issues.append(
            Violation(
                "RU-01",
                "RU-01_INVALID_ENUM",
                "record.delta_class must be one of %s" % ", ".join(DELTA_CLASSES),
            )
        )
    if not _is_string_list(record.get("affected_inputs")):
        issues.append(
            Violation("RU-01", "RU-01_TYPE_MISMATCH", "record.affected_inputs must be a list of strings")
        )

    full_diff = _check_object(record.get("full_diff"), "record.full_diff", FULL_DIFF_FIELDS, FULL_DIFF_FIELDS, issues)
    if full_diff is not None:
        _require_type(full_diff, "name_only_ref", "record.full_diff", str, issues)
        _require_type(full_diff, "name_only_sha256", "record.full_diff", str, issues)
        _require_type(full_diff, "file_count", "record.full_diff", int, issues)

    comparison = _check_object(
        record.get("comparison"), "record.comparison", COMPARISON_FIELDS, COMPARISON_FIELDS, issues
    )
    if comparison is not None:
        for key in ("method", "tool", "tool_version"):
            _require_type(comparison, key, "record.comparison", str, issues)
        if not isinstance(comparison.get("ast_stripped"), bool):
            issues.append(
                Violation(
                    "RU-01",
                    "RU-01_TYPE_MISMATCH",
                    "record.comparison.ast_stripped must be a boolean",
                )
            )
        ast_digest = comparison.get("ast_equality_sha256")
        if ast_digest is not None and not isinstance(ast_digest, str):
            issues.append(
                Violation(
                    "RU-01",
                    "RU-01_TYPE_MISMATCH",
                    "record.comparison.ast_equality_sha256 must be a string or null",
                )
            )

    excluded = record.get("excluded_claims")
    if not _is_string_list(excluded):
        issues.append(
            Violation("RU-01", "RU-01_TYPE_MISMATCH", "record.excluded_claims must be a list of strings")
        )
    elif len(set(excluded)) != len(excluded):
        issues.append(
            Violation("RU-01", "RU-01_DUPLICATE_VALUE", "record.excluded_claims contains a duplicate")
        )
    elif any(item not in EXCLUDED_CLAIMS for item in excluded):
        issues.append(
            Violation(
                "RU-01",
                "RU-01_INVALID_ENUM",
                "record.excluded_claims may only carry %s" % ", ".join(EXCLUDED_CLAIMS),
            )
        )

    checks = record.get("target_delta_checks")
    if not isinstance(checks, list):
        issues.append(
            Violation("RU-01", "RU-01_TYPE_MISMATCH", "record.target_delta_checks must be a list")
        )
    else:
        for index, entry in enumerate(checks):
            path = "record.target_delta_checks[%d]" % index
            check = _check_object(entry, path, CHECK_FIELDS, CHECK_FIELDS, issues)
            if check is None:
                continue
            _require_type(check, "check_id", path, str, issues)
            _require_type(check, "evidence_ref", path, str, issues)
            if check.get("kind") not in CHECK_KINDS:
                issues.append(
                    Violation("RU-01", "RU-01_INVALID_ENUM", "%s.kind is not a closed vocabulary value" % path)
                )
            if check.get("result") not in CHECK_RESULTS:
                issues.append(
                    Violation("RU-01", "RU-01_INVALID_ENUM", "%s.result is not a closed vocabulary value" % path)
                )

    independence = _check_object(
        record.get("independence"),
        "record.independence",
        INDEPENDENCE_FIELDS,
        INDEPENDENCE_FIELDS,
        issues,
    )
    if independence is not None:
        for key in ("qualifier_identity_ref", "class", "attestation_ref"):
            _require_type(independence, key, "record.independence", str, issues)

    if record.get("decision") not in DECISIONS:
        issues.append(
            Violation(
                "RU-01",
                "RU-01_INVALID_ENUM",
                "record.decision must be one of %s" % ", ".join(DECISIONS),
            )
        )

    authority = _check_object(
        record.get("decision_authority"),
        "record.decision_authority",
        AUTHORITY_FIELDS,
        AUTHORITY_FIELDS,
        issues,
    )
    if authority is not None:
        if authority.get("authority_kind") not in AUTHORITY_KINDS:
            issues.append(
                Violation(
                    "RU-01",
                    "RU-01_INVALID_ENUM",
                    "record.decision_authority.authority_kind is not a closed vocabulary value",
                )
            )
        for key in ("authority_ref_id", "authority_ref_sha256"):
            value = authority.get(key)
            if value is not None and not isinstance(value, str):
                issues.append(
                    Violation(
                        "RU-01",
                        "RU-01_TYPE_MISMATCH",
                        "record.decision_authority.%s must be a string or null" % key,
                    )
                )

    invalid_after = record.get("invalid_after")
    if not _is_string_list(invalid_after):
        issues.append(
            Violation("RU-01", "RU-01_TYPE_MISMATCH", "record.invalid_after must be a list of strings")
        )
    elif any(item not in INVALIDATION_EVENTS for item in invalid_after):
        issues.append(
            Violation(
                "RU-01",
                "RU-01_INVALID_ENUM",
                "record.invalid_after may only carry %s" % ", ".join(INVALIDATION_EVENTS),
            )
        )

    provenance = _check_object(
        record.get("provenance"), "record.provenance", PROVENANCE_FIELDS, PROVENANCE_FIELDS, issues
    )
    if provenance is not None:
        for key in ("source_ref", "as_of", "producer_role"):
            _require_type(provenance, key, "record.provenance", str, issues)
        identity = provenance.get("producer_identity_ref")
        if identity is not None and not isinstance(identity, str):
            issues.append(
                Violation(
                    "RU-01",
                    "RU-01_TYPE_MISMATCH",
                    "record.provenance.producer_identity_ref must be a string or null",
                )
            )
        _require_type(provenance, "declared_payload_sha256", "record.provenance", str, issues)
        _require_type(provenance, "declared_payload_bytes", "record.provenance", int, issues)

    return issues


def sample_record() -> typing.Dict[str, object]:
    """A synthetic, schema-conformant docs-text-only record for --self-test.

    The identities are obviously synthetic; the record asserts no real reuse.
    """

    record: typing.Dict[str, object] = {
        "schema_version": SCHEMA_VERSION,
        "reuse_id": "REUSE-SELFTEST-0001",
        "subject": {"repo": {"owner": "example-org", "name": "example-repo"}, "change_id": 42},
        "source": {
            "evidence_ids": ["EV-SELFTEST-1"],
            "source_head": "a" * 40,
            "source_tree": "b" * 40,
            "source_base": "c" * 40,
            "source_records_sha256": ["1" * 64],
            "requirement_ids": ["MG1"],
        },
        "target": {"target_head": "d" * 40, "target_tree": "e" * 40, "target_base": "f" * 40},
        "delta_class": "DOCS_TEXT_ONLY",
        "affected_inputs": ["docs/example.md"],
        "full_diff": {"name_only_ref": "diff-selftest-0001", "name_only_sha256": "2" * 64, "file_count": 1},
        "comparison": {
            "method": "name-only-diff",
            "tool": "git",
            "tool_version": "2.x",
            "ast_stripped": False,
            "ast_equality_sha256": None,
        },
        "excluded_claims": list(EXCLUDED_CLAIMS),
        "target_delta_checks": [
            {
                "check_id": "CI-REQUIRED",
                "kind": "REQUIRED_CI",
                "result": "PASS",
                "evidence_ref": "EV-SELFTEST-CI",
            }
        ],
        "independence": {
            "qualifier_identity_ref": "role-e-selftest",
            "class": "INDEPENDENT",
            "attestation_ref": "ATT-SELFTEST-0001",
        },
        "decision": "VALID",
        "decision_authority": {
            "authority_kind": "OWNER_LINE_RECORD",
            "authority_ref_id": "OWNER-LINE-SELFTEST-0001",
            "authority_ref_sha256": "3" * 64,
        },
        "invalid_after": ["TARGET_HEAD_MOVE", "SOURCE_EVIDENCE_CHANGE"],
        "provenance": {
            "source_ref": "selftest:evidence-reuse",
            "as_of": "2026-11-11T00:00:00Z",
            "producer_role": "evidence-lineage-steward",
            "producer_identity_ref": None,
            "declared_payload_sha256": "",
            "declared_payload_bytes": 0,
        },
    }
    provenance = typing.cast(typing.Dict[str, object], record["provenance"])
    provenance["declared_payload_sha256"] = payload_digest(record)
    provenance["declared_payload_bytes"] = payload_bytes(record)
    return record


def self_test() -> typing.Dict[str, object]:
    record = sample_record()
    issues = validate_shape(record)
    first = canonical_bytes(record)
    second = canonical_bytes(record)
    digest_value = payload_digest(record)
    return {
        "ok": not issues and first == second and len(digest_value) == 64,
        "schema_version": SCHEMA_VERSION,
        "sample_payload_sha256": digest_value,
        "sample_payload_bytes": payload_bytes(record),
        "violations": [issue.as_dict() for issue in issues],
    }
