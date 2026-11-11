"""C3.4 stage-holder, replacement, unavailability and context-bundle checks.

This module validates declared records against the single-holder rule and the
one-accountable-owner rule.  It validates records; it does not append to the
merged revision-state store (that would need AUTH-STORE/T24), create a second
ledger, or grant authority.  A real unavailable-review disposition is BLOCKED
while T7 is open, and a replacement can never be self-approved.
"""

from __future__ import annotations

import typing

from . import schema

STAGES = ("B", "D", "E", "F")
HOLDER_FIELDS = (
    "holder_id",
    "candidate_id",
    "stage",
    "holder_identity_ref",
    "holder_role",
    "activation_event_ref",
    "authority_ref",
    "independence_class",
    "snapshot_identity",
    "activated_at",
    "bounded_wait_ref",
    "deadline",
    "state",
)
REPLACEMENT_FIELDS = (
    "replacement_id",
    "candidate_id",
    "stage",
    "old_holder_ref",
    "new_holder_ref",
    "reason_class",
    "finding_refs",
    "authority_ref",
    "authority_role",
    "independence_attestation",
    "snapshot_identity",
    "context_bundle_sha256",
    "created_at",
    "status",
)
INDEPENDENCE_FIELDS = (
    "new_holder_identity_ref",
    "old_holder_identity_ref",
    "implementer_identity_ref",
    "pr_author_identity_ref",
    "commit_author_identity_refs",
)
UNAVAILABILITY_FIELDS = (
    "unavailability_id",
    "candidate_id",
    "stage",
    "source_ref",
    "scope",
    "evidence_ref",
    "bounded_wait_ref",
    "deadline",
    "disposition",
    "t7_ref",
)
BUNDLE_FIELDS = (
    "bundle_id",
    "candidate_id",
    "stage",
    "head_sha",
    "tree_sha",
    "base_sha",
    "frozen_scope",
    "active_holder_refs",
    "verdict_refs",
    "triage_ref",
    "unrun",
    "deadline",
    "next_action",
    "prior_holder_separation",
    "context_bundle_sha256",
)
OWNER_FIELDS = ("component", "owner_identity_ref", "governance_path_ref")
TOP_FIELDS = (
    "schema_version",
    "candidate_id",
    "stage",
    "frozen_head",
    "component_owner",
    "holders",
    "replacements",
    "unavailabilities",
    "context_bundles",
    "head_budget",
    "invalidation",
)
TOP_OPTIONAL = ("component_owner_after",)


def _context_payload(bundle: typing.Mapping[str, object]) -> typing.Dict[str, object]:
    return {key: value for key, value in bundle.items() if key != "context_bundle_sha256"}


def _check_bundle(
    bundle: typing.Any, report: schema.Report, position: int
) -> typing.Optional[typing.Dict[str, object]]:
    where = "context_bundles[%d]" % position
    checked = schema.check_object(bundle, where, BUNDLE_FIELDS, (), report)
    if checked is None:
        return None
    schema.check_string(checked.get("bundle_id"), where + ".bundle_id", report)
    schema.check_string(checked.get("candidate_id"), where + ".candidate_id", report)
    schema.check_enum(checked.get("stage"), where + ".stage", STAGES, report)
    schema.check_hex40(checked.get("head_sha"), where + ".head_sha", report)
    schema.check_hex40(checked.get("tree_sha"), where + ".tree_sha", report)
    schema.check_hex40(checked.get("base_sha"), where + ".base_sha", report)
    schema.check_string(checked.get("frozen_scope"), where + ".frozen_scope", report)
    for field in ("active_holder_refs", "verdict_refs", "unrun"):
        value = checked.get(field)
        if not isinstance(value, list) or any(not isinstance(item, str) or not item for item in value):
            report.add("BUNDLE_LIST_INVALID", "%s.%s must be a string list" % (where, field))
    schema.check_string(checked.get("triage_ref"), where + ".triage_ref", report)
    schema.check_iso(checked.get("deadline"), where + ".deadline", report)
    schema.check_string(checked.get("next_action"), where + ".next_action", report)
    schema.check_string(
        checked.get("prior_holder_separation"),
        where + ".prior_holder_separation",
        report,
    )
    declared = checked.get("context_bundle_sha256")
    if not schema.is_nonempty_str(declared):
        report.add("BUNDLE_HASH_MISSING", "%s.context_bundle_sha256 is required" % where)
        return checked
    computed = schema.digest(_context_payload(checked))
    if computed != declared:
        report.add(
            "BUNDLE_HASH_MISMATCH",
            "%s context hash does not recompute (declared %s... computed %s...)"
            % (where, str(declared)[:12], computed[:12]),
        )
    return checked


def _check_independence(
    attestation: typing.Any, where: str, report: schema.Report
) -> typing.Optional[typing.Dict[str, object]]:
    checked = schema.check_object(
        attestation, where, INDEPENDENCE_FIELDS, (), report
    )
    if checked is None:
        return None
    for field in (
        "new_holder_identity_ref",
        "old_holder_identity_ref",
        "implementer_identity_ref",
        "pr_author_identity_ref",
    ):
        schema.check_string(checked.get(field), where + "." + field, report)
    authors = checked.get("commit_author_identity_refs")
    if not isinstance(authors, list) or any(not isinstance(item, str) for item in authors):
        report.add("REPLACEMENT_AUTHORS_INVALID", "%s.commit_author_identity_refs must be a string list" % where)
        authors = []
    new_holder = checked.get("new_holder_identity_ref")
    conflicts = set()
    for label, value in (
        ("implementer", checked.get("implementer_identity_ref")),
        ("PR author", checked.get("pr_author_identity_ref")),
        ("old holder", checked.get("old_holder_identity_ref")),
    ):
        if new_holder and new_holder == value:
            conflicts.add(label)
    if new_holder in authors:
        conflicts.add("commit author")
    if conflicts:
        report.add(
            "REPLACEMENT_SELF_APPROVAL",
            "%s new holder is the %s; a replacement must be independent"
            % (where, ", ".join(sorted(conflicts))),
        )
        return checked
    if checked.get("implementer_identity_ref") == new_holder:
        report.add("REPLACEMENT_SELF_APPROVAL", "%s is self-approved" % where)
    return checked


def validate_records(document: typing.Mapping[str, object]) -> typing.Dict[str, object]:
    report = schema.Report()
    schema.check_schema_version(document, schema.SCHEMA_HOLDERS, report)
    schema.check_object(
        document, "stage-holder record set", TOP_FIELDS, TOP_OPTIONAL, report
    )
    schema.check_string(document.get("candidate_id"), "candidate_id", report)
    schema.check_enum(document.get("stage"), "stage", STAGES, report)
    schema.check_hex40(document.get("frozen_head"), "frozen_head", report)
    owner = schema.check_object(
        document.get("component_owner"), "component_owner", OWNER_FIELDS, (), report
    )
    if owner is not None:
        for field in OWNER_FIELDS:
            schema.check_string(owner.get(field), "component_owner." + field, report)
    after = document.get("component_owner_after")
    if after is not None:
        if after != owner:
            report.add(
                "COMPONENT_OWNER_CHANGED",
                "a replacement may not change the component owner or governance path",
            )
    holders: typing.List[typing.Dict[str, object]] = []
    raw_holders = document.get("holders")
    if not isinstance(raw_holders, list) or not raw_holders:
        report.add("HOLDERS_MISSING", "holders must be a non-empty list")
        raw_holders = []
    for position, holder in enumerate(raw_holders):
        where = "holders[%d]" % position
        checked = schema.check_object(holder, where, HOLDER_FIELDS, (), report)
        if checked is None:
            continue
        for field in (
            "holder_id",
            "candidate_id",
            "holder_identity_ref",
            "holder_role",
            "activation_event_ref",
            "authority_ref",
            "independence_class",
            "snapshot_identity",
            "bounded_wait_ref",
        ):
            schema.check_string(checked.get(field), where + "." + field, report)
        schema.check_enum(checked.get("stage"), where + ".stage", STAGES, report)
        schema.check_iso(checked.get("activated_at"), where + ".activated_at", report)
        schema.check_iso(checked.get("deadline"), where + ".deadline", report)
        schema.check_enum(checked.get("state"), where + ".state", schema.HOLDER_STATES, report)
        holders.append(checked)
    active_by_stage: typing.Dict[str, typing.List[str]] = {}
    for holder in holders:
        if holder.get("state") == "ACTIVE":
            active_by_stage.setdefault(str(holder.get("stage")), []).append(
                str(holder.get("holder_id"))
            )
    for stage, active in sorted(active_by_stage.items()):
        if len(active) > 1:
            report.add(
                "DUPLICATE_ACTIVE_HOLDER",
                "stage %s has more than one ACTIVE holder: %s"
                % (stage, ", ".join(sorted(active))),
            )
    by_id = {str(holder.get("holder_id")): holder for holder in holders}
    bundles = document.get("context_bundles")
    bundle_list: typing.List[typing.Dict[str, object]] = []
    if not isinstance(bundles, list):
        report.add("BUNDLES_MISSING", "context_bundles must be a list")
        bundles = []
    for position, bundle in enumerate(bundles):
        checked = _check_bundle(bundle, report, position)
        if checked is not None:
            bundle_list.append(checked)
    bundle_hashes = {str(bundle.get("context_bundle_sha256")) for bundle in bundle_list}
    replacements = document.get("replacements")
    if not isinstance(replacements, list):
        report.add("REPLACEMENTS_MISSING", "replacements must be a list")
        replacements = []
    for position, replacement in enumerate(replacements):
        where = "replacements[%d]" % position
        checked = schema.check_object(
            replacement, where, REPLACEMENT_FIELDS, (), report
        )
        if checked is None:
            continue
        for field in ("replacement_id", "candidate_id", "snapshot_identity", "created_at"):
            schema.check_string(checked.get(field), where + "." + field, report)
        schema.check_enum(checked.get("stage"), where + ".stage", STAGES, report)
        schema.check_enum(
            checked.get("reason_class"),
            where + ".reason_class",
            schema.REPLACEMENT_REASONS,
            report,
        )
        findings = checked.get("finding_refs")
        if not isinstance(findings, list) or any(not isinstance(item, str) or not item for item in findings):
            report.add("REPLACEMENT_FINDINGS_INVALID", "%s.finding_refs must be a string list" % where)
        old_ref = checked.get("old_holder_ref")
        new_ref = checked.get("new_holder_ref")
        old = by_id.get(str(old_ref))
        new = by_id.get(str(new_ref))
        if old is None:
            report.add("REPLACEMENT_OLD_MISSING", "%s.old_holder_ref does not resolve" % where)
        elif old.get("state") not in ("REPLACED", "SUPERSEDED"):
            report.add(
                "REPLACEMENT_OLD_NOT_MARKED",
                "%s old holder is %r, not REPLACED/SUPERSEDED"
                % (where, old.get("state")),
            )
        if new is None:
            report.add("REPLACEMENT_NEW_MISSING", "%s.new_holder_ref does not resolve" % where)
        elif new.get("state") != "ACTIVE":
            report.add("REPLACEMENT_NEW_NOT_ACTIVE", "%s new holder is not ACTIVE" % where)
        authority = checked.get("authority_ref")
        role = checked.get("authority_role")
        schema.check_string(authority, where + ".authority_ref", report)
        schema.check_string(role, where + ".authority_role", report)
        if role in ("IMPLEMENTER", "SELF", "PR_AUTHOR"):
            report.add(
                "REPLACEMENT_AUTHORITY_INVALID",
                "%s authority_role %r cannot authorise its own replacement" % (where, role),
            )
        _check_independence(
            checked.get("independence_attestation"),
            where + ".independence_attestation",
            report,
        )
        bundle_hash = checked.get("context_bundle_sha256")
        schema.check_hex64(bundle_hash, where + ".context_bundle_sha256", report)
        if bundle_hash not in bundle_hashes:
            report.add(
                "REPLACEMENT_BUNDLE_UNBOUND",
                "%s.context_bundle_sha256 does not match a supplied context bundle" % where,
            )
    unavailabilities = document.get("unavailabilities")
    if not isinstance(unavailabilities, list):
        report.add("UNAVAILABILITIES_MISSING", "unavailabilities must be a list")
        unavailabilities = []
    blocked_reasons: typing.List[str] = []
    for position, entry in enumerate(unavailabilities):
        where = "unavailabilities[%d]" % position
        checked = schema.check_object(entry, where, UNAVAILABILITY_FIELDS, (), report)
        if checked is None:
            continue
        for field in (
            "unavailability_id",
            "candidate_id",
            "source_ref",
            "scope",
            "evidence_ref",
            "bounded_wait_ref",
        ):
            schema.check_string(checked.get(field), where + "." + field, report)
        if checked.get("t7_ref") is not None:
            schema.check_string(checked.get("t7_ref"), where + ".t7_ref", report)
        schema.check_iso(checked.get("deadline"), where + ".deadline", report)
        route = schema.check_enum(
            checked.get("disposition"),
            where + ".disposition",
            schema.UNAVAILABILITY_ROUTES,
            report,
        )
        t7_ref = checked.get("t7_ref")
        if route in ("WAIT_BOUNDED", "REPLACE_EXPLICITLY") and not schema.is_nonempty_str(t7_ref):
            blocked_reasons.append(
                "UNAVAILABLE_REVIEW_T7_OPEN:%s" % checked.get("unavailability_id")
            )
        if route == "REPLACE_EXPLICITLY":
            linked = [
                replacement
                for replacement in replacements
                if isinstance(replacement, dict)
                and replacement.get("reason_class") == "UNAVAILABLE"
                and replacement.get("stage") == checked.get("stage")
            ]
            if not linked:
                report.add(
                    "REPLACEMENT_REQUIRED_MISSING",
                    "%s declares REPLACE_EXPLICITLY but no UNAVAILABLE replacement is recorded"
                    % where,
                )
    head_budget = document.get("head_budget")
    if not isinstance(head_budget, dict):
        report.add("HEAD_BUDGET_MISSING", "head_budget must be an object")
        head_budget = {}
    used = head_budget.get("heads_used")
    limit = head_budget.get("limit", 3)
    exception = head_budget.get("exception_ref")
    basis = head_budget.get("exception_basis")
    if not schema.is_int(used) or used < 0:
        report.add("HEAD_BUDGET_USED_INVALID", "head_budget.heads_used must be an integer >= 0")
    if not schema.is_int(limit) or limit < 1:
        report.add("HEAD_BUDGET_LIMIT_INVALID", "head_budget.limit must be an integer >= 1")
    elif schema.is_int(used) and used > limit:
        if not schema.is_nonempty_str(exception) or not schema.is_nonempty_str(basis):
            report.add(
                "HEAD_BUDGET_EXCEPTION_MISSING",
                "a fourth head needs a recorded scoped exception and its R3 blocking basis",
            )
    invalidation = document.get("invalidation")
    if invalidation is not None:
        checked_invalidation = schema.check_object(
            invalidation,
            "invalidation",
            ("head_moved", "base_moved", "policy_moved", "evidence_moved", "rebind_ref"),
            (),
            report,
        )
        if checked_invalidation is not None:
            for field in ("head_moved", "base_moved", "policy_moved", "evidence_moved"):
                if not schema.is_bool(checked_invalidation.get(field)):
                    report.add("INVALIDATION_FLAG_INVALID", "invalidation.%s must be a boolean" % field)
            moved = any(
                checked_invalidation.get(field) is True
                for field in ("head_moved", "base_moved", "policy_moved", "evidence_moved")
            )
            if moved and not schema.is_nonempty_str(checked_invalidation.get("rebind_ref")):
                report.add(
                    "INVALIDATION_REBIND_MISSING",
                    "a moved head/base/policy/evidence requires a recorded rebind",
                )
            if moved and active_by_stage:
                report.add(
                    "HOLDER_STALE_AFTER_MOVE",
                    "an ACTIVE holder cannot continue across an invalidating move",
                )
    status_entries = []
    for holder in holders:
        status_entries.append(
            {
                "holder_id": holder.get("holder_id"),
                "stage": holder.get("stage"),
                "state": holder.get("state"),
                "provenance": holder.get("authority_ref"),
                "next_action": "NONE" if holder.get("state") in ("COMPLETED", "DECLINED") else "REVIEW_OR_REPLACE",
            }
        )
    blocked = bool(report.issues or blocked_reasons)
    overall = "BLOCKED" if blocked else "ACTIVE" if active_by_stage else "IDLE"
    return {
        **schema.base_report(schema.SCHEMA_HOLDERS),
        "valid": report.valid,
        "blocked": blocked,
        "overall_state": overall,
        "active_holders": {
            stage: sorted(active) for stage, active in sorted(active_by_stage.items())
        },
        "status": status_entries,
        "blockers": sorted(blocked_reasons),
        "component_owner": owner,
        "issues": [issue.as_dict() for issue in report.issues],
        "not_verifiable": list(schema.NOT_VERIFIABLE),
    }


def validate(document: typing.Mapping[str, object]) -> typing.Dict[str, object]:
    return validate_records(document)
