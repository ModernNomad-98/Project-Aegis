"""Semantic rules RU-01..RU-12 for the aegis.evidence-reuse/1 record.

RU-01 is delegated to schema.validate_shape (closed schema); this module owns
RU-02..RU-12.  The validator is read-only and standard-library only.  It never
accepts a declaration at face value: heads are re-checked, cited evidence is
resolved against a supplied set, the target is compared with the current
authoritative target, and the provenance envelope is re-hashed.

A VALID decision is still only a record.  It cannot waive required CI, cannot
clear a mandatory finding, and is not an approval or a merge permission.
"""

from __future__ import annotations

import typing

from . import schema

RULE_IDS = tuple("RU-%02d" % index for index in range(1, 13))

NON_CLAIMS = (
    "auditable tooling, not enforcement",
    "no required context, settings or CI change",
    "a VALID decision is a record, not an approval or merge permission",
    "no required CI or mandatory finding can be waived",
    "no automatic acceptance: the decision is reviewed where policy requires it",
    "mounted coverage is UNKNOWN",
)


def _check(
    rule_id: str,
    status: str,
    detail: str,
    applicable: bool = True,
) -> typing.Dict[str, object]:
    return {"rule_id": rule_id, "status": status, "detail": detail, "applicable": applicable}


def _fail(violations: typing.List[schema.Violation], rule: str, code: str, detail: str) -> None:
    violations.append(schema.Violation(rule, code, detail))


def _check_entries(
    record: typing.Mapping[str, object],
) -> typing.Dict[str, typing.Dict[str, object]]:
    entries = record.get("target_delta_checks")
    if not isinstance(entries, list):
        return {}
    return {
        str(entry.get("kind")): typing.cast(typing.Dict[str, object], entry)
        for entry in entries
        if isinstance(entry, dict)
    }


def _has_ci_pass(record: typing.Mapping[str, object]) -> bool:
    for entry in record.get("target_delta_checks", []):
        if isinstance(entry, dict) and entry.get("kind") == "REQUIRED_CI" and entry.get("result") == "PASS":
            return True
    return False


def validate_record(
    document: object,
    *,
    target_head: typing.Optional[str],
    change_id: typing.Optional[typing.Union[str, int]] = None,
    evidence_records: typing.Sequence[typing.Mapping[str, object]] = (),
    requirement_ids: typing.Optional[typing.Iterable[str]] = None,
) -> typing.Dict[str, object]:
    """Validate one reuse record and return a deterministic result mapping."""

    violations: typing.List[schema.Violation] = []
    checks: typing.Dict[str, typing.Dict[str, object]] = {}
    record: typing.Dict[str, object] = {}
    shape_issues: typing.List[schema.Violation] = []

    if not isinstance(document, dict):
        _fail(violations, "RU-01", "RU-01_NOT_OBJECT", "the record is not a JSON object")
        checks["RU-01"] = _check("RU-01", "FAIL", "the record is not a JSON object")
        for rule_id in RULE_IDS[1:]:
            checks[rule_id] = _check(rule_id, "UNRUN", "not evaluated: the record is not an object")
        return _result(document, violations, checks, "INVALID", False)

    record = document
    shape_issues = schema.validate_shape(record)
    violations.extend(shape_issues)
    if shape_issues:
        checks["RU-01"] = _check(
            "RU-01", "FAIL", "%d closed-schema violation(s)" % len(shape_issues)
        )
        for rule_id in RULE_IDS[1:]:
            checks[rule_id] = _check(rule_id, "UNRUN", "not evaluated: the closed schema failed")
        return _result(record, violations, checks, "INVALID", False)

    checks["RU-01"] = _check("RU-01", "PASS", "closed aegis.evidence-reuse/1 schema")

    # RU-02: 40-hex heads/trees/bases, 64-hex digests.
    hex_issues: typing.List[str] = []
    source = typing.cast(typing.Mapping[str, object], record["source"])
    target = typing.cast(typing.Mapping[str, object], record["target"])
    for key in ("source_head", "source_tree", "source_base"):
        if not schema.is_hex(source.get(key), schema.HEX40):
            hex_issues.append("source.%s" % key)
    for key in ("target_head", "target_tree", "target_base"):
        if not schema.is_hex(target.get(key), schema.HEX40):
            hex_issues.append("target.%s" % key)
    for index, value in enumerate(source.get("source_records_sha256", [])):
        if not schema.is_hex(value, schema.HEX64):
            hex_issues.append("source.source_records_sha256[%d]" % index)
    full_diff = typing.cast(typing.Mapping[str, object], record["full_diff"])
    if not schema.is_hex(full_diff.get("name_only_sha256"), schema.HEX64):
        hex_issues.append("full_diff.name_only_sha256")
    comparison = typing.cast(typing.Mapping[str, object], record["comparison"])
    ast_digest = comparison.get("ast_equality_sha256")
    if ast_digest is not None and not schema.is_hex(ast_digest, schema.HEX64):
        hex_issues.append("comparison.ast_equality_sha256")
    authority = typing.cast(typing.Mapping[str, object], record["decision_authority"])
    authority_digest = authority.get("authority_ref_sha256")
    if authority_digest is not None and not schema.is_hex(authority_digest, schema.HEX64):
        hex_issues.append("decision_authority.authority_ref_sha256")
    provenance = typing.cast(typing.Mapping[str, object], record["provenance"])
    if not schema.is_hex(provenance.get("declared_payload_sha256"), schema.HEX64):
        hex_issues.append("provenance.declared_payload_sha256")
    if hex_issues:
        for field in hex_issues:
            _fail(violations, "RU-02", "RU-02_INVALID_IDENTITY", "%s is not a valid hexadecimal identity" % field)
        checks["RU-02"] = _check("RU-02", "FAIL", ", ".join(hex_issues))
    else:
        checks["RU-02"] = _check("RU-02", "PASS", "40-hex heads/trees/bases and 64-hex digests")

    # RU-03: source evidence identity resolved and preserved.
    evidence_by_id: typing.Dict[str, typing.Mapping[str, object]] = {}
    duplicate_evidence: typing.List[str] = []
    malformed_evidence: typing.List[str] = []
    for entry in evidence_records:
        if not isinstance(entry, dict):
            malformed_evidence.append("<non-object>")
            continue
        evidence_id = entry.get("evidence_id")
        if not isinstance(evidence_id, str) or not evidence_id:
            malformed_evidence.append("<missing evidence_id>")
            continue
        if evidence_id in evidence_by_id:
            duplicate_evidence.append(evidence_id)
        evidence_by_id[evidence_id] = entry
    supplied_digests = {
        entry.get("sha256") for entry in evidence_by_id.values() if isinstance(entry.get("sha256"), str)
    }
    evidence_issues: typing.List[str] = []
    if malformed_evidence:
        _fail(violations, "RU-03", "RU-03_MALFORMED_EVIDENCE", "supplied evidence record is malformed: %s" % ", ".join(malformed_evidence))
        evidence_issues.append("malformed evidence")
    if duplicate_evidence:
        _fail(violations, "RU-03", "RU-03_DUPLICATE_EVIDENCE", "duplicate supplied evidence id(s): %s" % ", ".join(sorted(set(duplicate_evidence))))
        evidence_issues.append("duplicate evidence")
    cited_ids = [str(item) for item in source.get("evidence_ids", [])]
    for evidence_id in cited_ids:
        entry = evidence_by_id.get(evidence_id)
        if entry is None:
            _fail(violations, "RU-03", "RU-03_EVIDENCE_UNRESOLVED", "cited evidence %s is not in the supplied evidence set" % evidence_id)
            evidence_issues.append("unresolved evidence")
            continue
        if entry.get("sha256") not in set(source.get("source_records_sha256", [])):
            _fail(violations, "RU-03", "RU-03_SOURCE_RECORD_MISMATCH", "evidence %s does not match a declared source record digest" % evidence_id)
            evidence_issues.append("source record mismatch")
        if entry.get("head") != source.get("source_head"):
            _fail(violations, "RU-03", "RU-03_SOURCE_HEAD_MISMATCH", "evidence %s is bound to a different source head" % evidence_id)
            evidence_issues.append("source head mismatch")
    if not set(source.get("source_records_sha256", [])).issubset(supplied_digests):
        _fail(violations, "RU-03", "RU-03_SOURCE_RECORD_UNSUPPLIED", "a declared source record digest is not present in the supplied evidence set")
        evidence_issues.append("unsupplied source record")
    if evidence_issues:
        checks["RU-03"] = _check("RU-03", "FAIL", ", ".join(sorted(set(evidence_issues))))
    else:
        checks["RU-03"] = _check("RU-03", "PASS", "%d cited evidence record(s) resolved and preserved" % len(cited_ids))

    # RU-04: target-head currency.  A moved or unverifiable target is STALE.
    target_moved = False
    decision = str(record.get("decision"))
    if decision == "VALID":
        if not target_head:
            _fail(violations, "RU-04", "RU-04_TARGET_UNVERIFIED", "no current authoritative target head was supplied")
            checks["RU-04"] = _check("RU-04", "FAIL", "no current authoritative target head was supplied")
        elif target.get("target_head") != target_head:
            target_moved = True
            _fail(violations, "RU-04", "RU-04_TARGET_MOVED", "the target head is not the current authoritative target")
            checks["RU-04"] = _check("RU-04", "FAIL", "the decision targets a superseded head")
        elif change_id is not None and str(typing.cast(typing.Mapping[str, object], record["subject"]).get("change_id")) != str(change_id):
            _fail(violations, "RU-04", "RU-04_CHANGE_MISMATCH", "the decision is bound to a different change")
            checks["RU-04"] = _check("RU-04", "FAIL", "the decision is bound to a different change")
        else:
            checks["RU-04"] = _check("RU-04", "PASS", "target head equals the current authoritative target")
    else:
        checks["RU-04"] = _check("RU-04", "PASS", "not applicable: the decision is %s" % decision, applicable=False)

    # RU-05..RU-09: delta-class scope rules.
    delta_class = str(record.get("delta_class"))
    class_checks = _check_entries(record)
    if decision != "VALID":
        for rule_id in ("RU-05", "RU-06", "RU-07", "RU-08", "RU-09"):
            checks[rule_id] = _check(rule_id, "PASS", "not applicable: the decision is %s" % decision, applicable=False)
    else:
        if delta_class == "DOCS_TEXT_ONLY":
            if not _has_ci_pass(record):
                _fail(violations, "RU-05", "RU-05_REQUIRED_CI_NOT_RUN", "docs-text-only reuse requires a recorded required-CI pass; CI is never waived")
                checks["RU-05"] = _check("RU-05", "FAIL", "required CI is not recorded as run and passing")
            else:
                checks["RU-05"] = _check("RU-05", "PASS", "docs-text-only reuse after a narrow audit with required CI still run")
        else:
            checks["RU-05"] = _check("RU-05", "PASS", "not applicable: the delta class is %s" % delta_class, applicable=False)
        if delta_class == "DOCSTRING_COMMENT_TEXT_ONLY_CODE":
            problems: typing.List[str] = []
            if comparison.get("ast_stripped") is not True:
                problems.append("ast_stripped is not true")
            if ast_digest is None:
                problems.append("ast_equality_sha256 is absent")
            if not _has_ci_pass(record):
                problems.append("required CI is not recorded as passing")
            for kind in ("AFFECTED_INPUTS", "REVIEWED_DIFF"):
                entry = class_checks.get(kind)
                if not entry or entry.get("result") != "PASS":
                    problems.append("%s check is not recorded as passing" % kind)
            if "BEHAVIORAL_EQUIVALENCE" not in record.get("excluded_claims", []):
                problems.append("BEHAVIORAL_EQUIVALENCE is not explicitly excluded")
            if problems:
                for problem in problems:
                    _fail(violations, "RU-06", "RU-06_AST_EVIDENCE_INCOMPLETE", problem)
                checks["RU-06"] = _check("RU-06", "FAIL", "; ".join(problems))
            else:
                checks["RU-06"] = _check("RU-06", "PASS", "docstring/comment-text-only code reuse with recorded AST-stripped equality (supporting only)")
        else:
            checks["RU-06"] = _check("RU-06", "PASS", "not applicable: the delta class is %s" % delta_class, applicable=False)
        if delta_class == "TEST_CHANGE":
            _fail(violations, "RU-07", "RU-07_TEST_CHANGE_NEVER_REUSES", "a test change never reuses a code-identical claim")
            checks["RU-07"] = _check("RU-07", "FAIL", "test changes never reuse")
        else:
            checks["RU-07"] = _check("RU-07", "PASS", "not applicable: the delta class is %s" % delta_class, applicable=False)
        if delta_class == "CONFIG_WORKFLOW_POLICY_GENERATED_DEPENDENCY":
            _fail(violations, "RU-08", "RU-08_CONFIG_NEVER_REUSES", "config/workflow/policy/generated/dependency changes never reuse a code-identical claim")
            checks["RU-08"] = _check("RU-08", "FAIL", "config/workflow/policy/generated/dependency changes never reuse")
        else:
            checks["RU-08"] = _check("RU-08", "PASS", "not applicable: the delta class is %s" % delta_class, applicable=False)
        if delta_class == "BEHAVIOR_CHANGE":
            _fail(violations, "RU-09", "RU-09_BEHAVIOR_NEVER_REUSES", "a behaviour change never reuses prior evidence")
            checks["RU-09"] = _check("RU-09", "FAIL", "behaviour changes never reuse")
        else:
            checks["RU-09"] = _check("RU-09", "PASS", "not applicable: the delta class is %s" % delta_class, applicable=False)

    # RU-10: incomplete decision material is INVALID.
    if decision == "VALID":
        problems = []
        for claim in schema.EXCLUDED_CLAIMS:
            if claim not in record.get("excluded_claims", []):
                problems.append("missing excluded claim %s" % claim)
        if not record.get("target_delta_checks"):
            problems.append("target_delta_checks is empty")
        independence = typing.cast(typing.Mapping[str, object], record["independence"])
        if independence.get("class") != "INDEPENDENT":
            problems.append("independence.class is not INDEPENDENT")
        if not independence.get("qualifier_identity_ref") or not independence.get("attestation_ref"):
            problems.append("independence references are incomplete")
        if authority.get("authority_kind") == "UNKNOWN":
            problems.append("decision authority is UNKNOWN")
        elif not authority.get("authority_ref_id") or not authority.get("authority_ref_sha256"):
            problems.append("decision authority reference is incomplete")
        if "TARGET_HEAD_MOVE" not in record.get("invalid_after", []):
            problems.append("invalid_after does not name TARGET_HEAD_MOVE")
        if delta_class in ("DOCSTRING_COMMENT_TEXT_ONLY_CODE", "TEST_CHANGE", "CONFIG_WORKFLOW_POLICY_GENERATED_DEPENDENCY", "BEHAVIOR_CHANGE") and not record.get("affected_inputs"):
            problems.append("affected_inputs is empty for a code-bearing delta class")
        if delta_class == "OTHER":
            problems.append("delta_class OTHER never authorises reuse")
        if requirement_ids is not None:
            missing = sorted(set(record.get("source", {}).get("requirement_ids", [])) - set(requirement_ids))
            if missing:
                problems.append("requirement id(s) do not resolve: %s" % ", ".join(missing))
        if problems:
            for problem in problems:
                _fail(violations, "RU-10", "RU-10_INCOMPLETE_DECISION", problem)
            checks["RU-10"] = _check("RU-10", "FAIL", "; ".join(problems))
        else:
            checks["RU-10"] = _check("RU-10", "PASS", "excluded claims, delta checks, independence and authority present")
    else:
        checks["RU-10"] = _check("RU-10", "PASS", "not applicable: the decision is %s" % decision, applicable=False)

    # RU-11: a VALID decision cannot waive required CI or carry a failed/unrun check.
    if decision == "VALID":
        problems = []
        for entry in record.get("target_delta_checks", []):
            if not isinstance(entry, dict):
                continue
            if entry.get("result") == "UNRUN":
                problems.append("check %s is UNRUN" % entry.get("check_id"))
            elif entry.get("result") == "FAIL":
                problems.append("check %s FAILED" % entry.get("check_id"))
        if problems:
            for problem in problems:
                _fail(violations, "RU-11", "RU-11_UNRUN_OR_FAIL_NOT_WAIVED", problem)
            checks["RU-11"] = _check("RU-11", "FAIL", "; ".join(problems))
        else:
            checks["RU-11"] = _check("RU-11", "PASS", "no required CI or mandatory check is waived")
    else:
        checks["RU-11"] = _check("RU-11", "PASS", "not applicable: the decision is %s" % decision, applicable=False)

    # RU-12: provenance re-hashed, never trusted from a declaration.
    recomputed_digest = schema.payload_digest(record)
    recomputed_bytes = schema.payload_bytes(record)
    provenance_problems = []
    if provenance.get("declared_payload_sha256") != recomputed_digest:
        provenance_problems.append("declared_payload_sha256 does not match the record payload")
        _fail(violations, "RU-12", "RU-12_PROVENANCE_HASH_MISMATCH", "declared_payload_sha256 does not match the record payload")
    if provenance.get("declared_payload_bytes") != recomputed_bytes:
        provenance_problems.append("declared_payload_bytes does not match the record payload")
        _fail(violations, "RU-12", "RU-12_PROVENANCE_BYTES_MISMATCH", "declared_payload_bytes does not match the record payload")
    if not provenance.get("producer_role"):
        provenance_problems.append("producer_role is missing")
        _fail(violations, "RU-12", "RU-12_PRODUCER_MISSING", "provenance.producer_role is missing")
    if provenance_problems:
        checks["RU-12"] = _check("RU-12", "FAIL", "; ".join(provenance_problems))
    else:
        checks["RU-12"] = _check("RU-12", "PASS", "provenance re-hashed over the record payload")

    if target_moved:
        effective = "STALE"
    elif decision != "VALID":
        effective = decision
    elif violations:
        effective = "INVALID"
    else:
        effective = "VALID"
    return _result(
        record,
        violations,
        checks,
        effective,
        not [issue for issue in violations if issue.rule_id != "RU-01"] and not shape_issues,
    )


def _result(
    record: object,
    violations: typing.Sequence[schema.Violation],
    checks: typing.Mapping[str, typing.Mapping[str, object]],
    effective_decision: str,
    schema_valid: bool,
) -> typing.Dict[str, object]:
    record_mapping = record if isinstance(record, dict) else {}
    ordered_checks = [dict(checks[rule_id]) for rule_id in RULE_IDS if rule_id in checks]
    return {
        "schema_version": schema.VALIDATION_SCHEMA_VERSION,
        "record_id": str(record_mapping.get("reuse_id") or ""),
        "effective_decision": effective_decision,
        "schema_valid": bool(schema_valid),
        "valid": effective_decision == "VALID",
        "violations": [
            issue.as_dict()
            for issue in sorted(violations, key=lambda item: (item.rule_id, item.code, item.detail))
        ],
        "checks": ordered_checks,
        "assurance": {"claim": "AUDITABLE", "mounted_coverage": "UNKNOWN"},
        "non_claims": list(NON_CLAIMS),
    }
