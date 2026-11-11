"""C3.1 bounded settlement derivation and merged-checker envelope emission.

The record family is `aegis.ops-settlement/v1`.  Settlement is derived from
recorded pre-audit and review-source facts with an explicit deadline and
attempt bound.  A pending required source, an unavailable disposition without
a T7 authority, or a declared-vs-derived mismatch means the record is not
settled (or is invalid, for a mismatch).  The deadline and attempts are inputs;
this module never reads the clock and never polls.

`build_envelope()` emits the merged C1.1a checker's `--settlement` input
envelope (`payload` + `provenance`).  The merged checker remains authoritative
for re-derivation; this module uses its field names and vocabulary so the
output round-trips unchanged.
"""

from __future__ import annotations

import typing

from . import schema

PRE_AUDIT_FIELDS = ("check_id", "state", "evidence_ref", "deadline")
REVIEW_FIELDS = ("source_id", "state")
REVIEW_OPTIONAL = (
    "disposition_authority_ref",
    "disposition_authority_sha256",
    "disposition_scope",
    "expires",
)
WAIT_FIELDS = ("deadline", "max_attempts", "observed_attempts")
RECORD_FIELDS = (
    "schema_version",
    "change_id",
    "candidate_head",
    "source_ref",
    "as_of",
    "settled",
    "pre_audit_checks",
    "review_sources",
    "bounded_wait",
    "blockers",
)


def _check_review_source(
    source: typing.Mapping[str, object], where: str, report: schema.Report
) -> typing.Optional[str]:
    checked = schema.check_object(
        source, where, REVIEW_FIELDS, REVIEW_OPTIONAL, report
    )
    if checked is None:
        return None
    schema.check_string(checked.get("source_id"), where + ".source_id", report)
    state = schema.check_enum(
        checked.get("state"), where + ".state", schema.REVIEW_SOURCE_STATES, report
    )
    if state == "UNAVAILABLE_DISPOSITIONED":
        authority = checked.get("disposition_authority_ref")
        if authority is not None:
            schema.check_string(
                authority, where + ".disposition_authority_ref", report
            )
        declared_sha = checked.get("disposition_authority_sha256")
        if declared_sha is not None:
            schema.check_hex64(
                declared_sha, where + ".disposition_authority_sha256", report
            )
        if checked.get("expires") not in (None, ""):
            report.add(
                "DISPOSITION_TIME_BOUND",
                "%s cites a time-bounded disposition; an offline checker cannot evaluate it"
                % where,
            )
    return state


def derive(document: typing.Mapping[str, object]) -> typing.Dict[str, object]:
    """Validate and derive settlement without emitting an envelope."""

    report = schema.Report()
    schema.check_schema_version(document, schema.SCHEMA_SETTLEMENT, report)
    schema.check_object(
        document,
        "settlement record",
        required=RECORD_FIELDS,
        optional=(),
        report=report,
    )
    schema.check_string(document.get("change_id"), "change_id", report)
    schema.check_hex40(document.get("candidate_head"), "candidate_head", report)
    schema.check_string(document.get("source_ref"), "source_ref", report)
    schema.check_iso(document.get("as_of"), "as_of", report)
    declared_settled = document.get("settled")
    if not schema.is_bool(declared_settled):
        report.add("SETTLEMENT_DECLARED_NOT_BOOL", "settled must be a boolean")
        declared_settled = None
    blockers: typing.List[str] = []
    declared_blockers = document.get("blockers")
    if not isinstance(declared_blockers, list) or any(
        not isinstance(entry, str) or not entry.strip() for entry in declared_blockers
    ):
        report.add("SETTLEMENT_BLOCKERS_INVALID", "blockers must be a list of non-empty strings")
        declared_blockers = []
    else:
        blockers.extend(declared_blockers)

    checks = document.get("pre_audit_checks")
    if not isinstance(checks, list) or not checks:
        report.add("SETTLEMENT_CHECKS_MISSING", "pre_audit_checks must be a non-empty list")
        checks = []
    for position, check in enumerate(checks):
        where = "pre_audit_checks[%d]" % position
        checked = schema.check_object(check, where, PRE_AUDIT_FIELDS, (), report)
        if checked is None:
            continue
        schema.check_string(checked.get("check_id"), where + ".check_id", report)
        state = schema.check_enum(
            checked.get("state"), where + ".state", schema.PRE_AUDIT_STATES, report
        )
        schema.check_string(checked.get("evidence_ref"), where + ".evidence_ref", report)
        schema.check_iso(checked.get("deadline"), where + ".deadline", report)
        if state in ("fail", "unrun", "bypassed"):
            blockers.append(
                "PRE_AUDIT_CHECK_NOT_PASSING:%s:%s" % (checked.get("check_id"), state)
            )

    sources = document.get("review_sources")
    if not isinstance(sources, list) or not sources:
        report.add("SETTLEMENT_REVIEWS_MISSING", "review_sources must be a non-empty list")
        sources = []
    pending: typing.List[str] = []
    unavailable: typing.List[str] = []
    for position, source in enumerate(sources):
        where = "review_sources[%d]" % position
        state = _check_review_source(source, where, report)
        if state == "PENDING":
            pending.append(str(source.get("source_id")))
            blockers.append("REVIEW_SOURCE_PENDING:%s" % source.get("source_id"))
        elif state == "UNAVAILABLE_DISPOSITIONED":
            unavailable.append(str(source.get("source_id")))
            blockers.append(
                "UNAVAILABLE_REVIEW_DISPOSITION_T7_OPEN:%s" % source.get("source_id")
            )
    derived_settled = not pending and not unavailable
    if report.issues:
        derived_settled = False
    if declared_settled is not None and declared_settled != derived_settled:
        report.add(
            "DECLARED_SETTLED_MISMATCH",
            "declared settled=%r but the recorded facts derive settled=%r"
            % (declared_settled, derived_settled),
        )
        derived_settled = False

    wait = document.get("bounded_wait")
    checked_wait = schema.check_object(wait, "bounded_wait", WAIT_FIELDS, (), report)
    deadline = None
    max_attempts = None
    observed = None
    if checked_wait is not None:
        deadline = schema.check_iso(checked_wait.get("deadline"), "bounded_wait.deadline", report)
        max_attempts = checked_wait.get("max_attempts")
        observed = checked_wait.get("observed_attempts")
        if not schema.is_int(max_attempts) or max_attempts < 1:
            report.add("BOUNDED_WAIT_MAX_INVALID", "bounded_wait.max_attempts must be an integer >= 1")
        if not schema.is_int(observed) or observed < 0:
            report.add("BOUNDED_WAIT_OBSERVED_INVALID", "bounded_wait.observed_attempts must be an integer >= 0")
        elif schema.is_int(max_attempts) and observed >= max_attempts:
            blockers.append("BOUNDED_WAIT_EXHAUSTED:%d/%d" % (observed, max_attempts))
    # A blocker is a readiness condition, not a settlement defect: a failed
    # pre-audit check can be fully recorded (settled) while still blocking the
    # act.  The separation is deliberate and is what C3.1-4 requires.
    unique_blockers = sorted(set(blockers))
    return {
        "report": report,
        "settled": derived_settled,
        "blockers": unique_blockers,
        "blocked": bool(unique_blockers) or not derived_settled,
        "deadline": deadline,
        "max_attempts": max_attempts,
        "observed_attempts": observed,
    }


def build_envelope(
    document: typing.Mapping[str, object], derived: typing.Mapping[str, object]
) -> typing.Dict[str, object]:
    """Emit the merged checker's settlement envelope from the supplied record."""

    payload = {
        "schema_version": schema.SCHEMA_SETTLEMENT,
        "change_id": document.get("change_id"),
        "candidate_head": document.get("candidate_head"),
        "settled": bool(derived["settled"]),
        "pre_audit_checks": document.get("pre_audit_checks"),
        "review_sources": document.get("review_sources"),
        "bounded_wait": document.get("bounded_wait"),
        "blockers": list(derived["blockers"]),
    }
    provenance = {
        "source_ref": document.get("source_ref"),
        "as_of": document.get("as_of"),
        "producer_role": "tools/aegis_ops",
        "producer_identity_ref": "tools/aegis_ops/settlement.py",
        "declared_payload_sha256": schema.digest(payload),
        "declared_payload_bytes": len(schema.canonical_bytes(payload)),
        "status": "UNVERIFIED",
    }
    return {"payload": payload, "provenance": provenance}


def settle(document: typing.Mapping[str, object]) -> typing.Dict[str, object]:
    derived = derive(document)
    report: schema.Report = derived["report"]  # type: ignore[assignment]
    result = {
        **schema.base_report(schema.SCHEMA_SETTLEMENT),
        "valid": report.valid,
        "blocked": derived["blocked"],
        "settled": derived["settled"],
        "blockers": derived["blockers"],
        "issues": [issue.as_dict() for issue in report.issues],
        "not_verifiable": list(schema.NOT_VERIFIABLE),
    }
    if report.valid:
        result["envelope"] = build_envelope(document, derived)
    return result


def validate(document: typing.Mapping[str, object]) -> typing.Dict[str, object]:
    return settle(document)
