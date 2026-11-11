"""C1-C13 fail-closed gate, blocker classes and the readiness predicate.

Semantics consumed by reference from aegis.verdict-bound/v2.1 (C03-M1 delta
section 2.7 as corrected by the v2.1 errata sections 2.3-2.5, 3.3 and 4.3):

  C1 completeness / closed schema / conditionals
  C2 bound hash and sub-hashes
  C3 verdict record integrity and affirmative F verdict
  C4 reviewer authenticity and independence
  C5 repository/change/merge-target identity
  C6 exact current head/tree/base
  C7 policy/plan/revision and review-head budget
  C8 required stage evidence and affirmative stage verdicts
  C9 canonical triage
  C10 evidence binding/reuse
  C11 skills/security/witness
  C12 owner line / merge authority
  C13 readiness predicate

Checks run in order and fail closed on the first failing check.  Readiness is
true only when every term holds; it is not merge authority and a recorded
bypass never becomes green.  No network, no provider SDK, standard library
only.
"""

from __future__ import annotations

import dataclasses
import re
import typing
from pathlib import Path

from . import canonical, catalogue, inputs, records
from .records import Issue

MANDATORY = "MANDATORY"
LIMIT = "LIMIT"
WAIT = "WAIT"

BLOCKER_CLASSES: typing.Dict[str, str] = {
    "OPEN_BLOCKING_FINDING": MANDATORY,
    "MISSING_INDEPENDENT_APPROVAL": MANDATORY,
    "MISSING_REQUIRED_REVIEW_OR_DISPOSITION": MANDATORY,
    "VERDICT_STALE_OR_UNVERIFIED": MANDATORY,
    "CANONICAL_FIELD_MISSING_OR_MISMATCH": MANDATORY,
    "HEAD_MOVED_OR_BASE_INVALIDATED": MANDATORY,
    "EVIDENCE_REUSE_INVALID": MANDATORY,
    "AUTHORITY_ABSENT": MANDATORY,
    "STATE_TAMPER_SUSPECTED": MANDATORY,
    "OWNER_DECISION_BLOCKING": MANDATORY,
    "POST_F_BLOCKER": MANDATORY,
    "REQUIRED_INPUT_UNAVAILABLE": MANDATORY,
    "VERDICT_NOT_AFFIRMATIVE": MANDATORY,
    "STAGE_VERDICT_NOT_ACCEPTED": MANDATORY,
    "SECURITY_FLAG_SET": MANDATORY,
    "REVIEW_BUDGET_EXHAUSTED": LIMIT,
    "ADVISORY_REVIEW_PENDING": WAIT,
    "SCHEDULED_EXTERNAL_WAIT": WAIT,
    "OWNER_DECISION_NON_BLOCKING": WAIT,
}

PERMITTED_ACTION: typing.Dict[str, typing.Dict[str, str]] = {
    "VERDICT_NOT_AFFIRMATIVE": {
        "action": "A3_FIX_AND_REAUDIT_AT_NEW_HEAD",
        "actor_role": "implementer",
        "authority_ref": "R3/R4 blocking-fix budget (plan section 2.1)",
    },
    "STAGE_VERDICT_NOT_ACCEPTED": {
        "action": "A3_FIX_AND_REAUDIT_AFFECTED_STAGES",
        "actor_role": "implementer",
        "authority_ref": "R3/R4 blocking-fix budget (plan section 2.1)",
    },
    "SECURITY_FLAG_SET": {
        "action": "A3_REMOVE_SECRET_EXPOSURE_AT_NEW_HEAD",
        "actor_role": "implementer",
        "authority_ref": "R3 blocking (a) credential/secret exposure; no exception clears readiness",
    },
    "VERDICT_STALE_OR_UNVERIFIED": {
        "action": "A7_REBIND_VERDICT_OR_A8_AWAIT_AUTHORITY",
        "actor_role": "record-holder",
        "authority_ref": "contract section 6.5 authentication gap (T6 open)",
    },
    "CANONICAL_FIELD_MISSING_OR_MISMATCH": {
        "action": "A7_REBIND_OR_CORRECT_RECORD",
        "actor_role": "record-holder",
        "authority_ref": "contract VB-I01 and closed-schema rule",
    },
    "HEAD_MOVED_OR_BASE_INVALIDATED": {
        "action": "A3_CONTROLLED_REPAIR_UNDER_EXCEPTION",
        "actor_role": "implementer",
        "authority_ref": "R3 blocking (c); new head under the R4 budget",
    },
    "EVIDENCE_REUSE_INVALID": {
        "action": "RERUN_AFFECTED_CHECKS_NO_COPY",
        "actor_role": "evidence-lineage-steward",
        "authority_ref": "contract C10",
    },
    "AUTHORITY_ABSENT": {
        "action": "A8_AWAIT_OWNER_DECISION",
        "actor_role": "owner",
        "authority_ref": "missing owner/exception/merge authority record",
    },
    "STATE_TAMPER_SUSPECTED": {
        "action": "A8_AWAIT_AUTHORITY_AND_RECORD_EVIDENCE",
        "actor_role": "records-steward",
        "authority_ref": "append-only record policy",
    },
    "OWNER_DECISION_BLOCKING": {
        "action": "A8_AWAIT_OWNER_DECISION",
        "actor_role": "owner",
        "authority_ref": "open owner decision gating readiness",
    },
    "POST_F_BLOCKER": {
        "action": "A7_CONTROLLED_REPAIR_UNDER_EXCEPTION",
        "actor_role": "implementer",
        "authority_ref": "post-F suspension (plan section 10.5)",
    },
    "REQUIRED_INPUT_UNAVAILABLE": {
        "action": "SUPPLY_THE_NAMED_REQUIRED_INPUT",
        "actor_role": "record-holder",
        "authority_ref": "contract C13 / plan section 6 required inputs",
    },
    "REVIEW_BUDGET_EXHAUSTED": {
        "action": "A5_REQUEST_SCOPED_EXCEPTION_OR_A6_PARK",
        "actor_role": "owner",
        "authority_ref": "R4 3-head budget; T7 authority undefined",
    },
    "OPEN_BLOCKING_FINDING": {
        "action": "A3_BATCHED_FIX_OR_A5_EXCEPTION_OR_A6_PARK",
        "actor_role": "implementer",
        "authority_ref": "R3 blocking (c)",
    },
    "MISSING_INDEPENDENT_APPROVAL": {
        "action": "A8_AWAIT_INDEPENDENT_APPROVAL",
        "actor_role": "reviewer-coordinator",
        "authority_ref": "AUTH-REVIEWERS (distinct reviewer required)",
    },
    "MISSING_REQUIRED_REVIEW_OR_DISPOSITION": {
        "action": "A4_SETTLE_REVIEW_OR_A8_AWAIT_DISPOSITION",
        "actor_role": "reviewer-coordinator",
        "authority_ref": "T7 unavailable-review disposition authority (undefined)",
    },
    # WAIT codes never block readiness; they still carry a permitted action so
    # that a displayed blocker is never a KeyError (the class map is total).
    "ADVISORY_REVIEW_PENDING": {
        "action": "WAIT_FOR_THE_ADVISORY_REVIEW",
        "actor_role": "reviewer-coordinator",
        "authority_ref": "advisory review is not a readiness term",
    },
    "SCHEDULED_EXTERNAL_WAIT": {
        "action": "WAIT_FOR_THE_SCHEDULED_EXTERNAL_EVENT",
        "actor_role": "record-holder",
        "authority_ref": "scheduled external wait is not a readiness term",
    },
    "OWNER_DECISION_NON_BLOCKING": {
        "action": "WAIT_FOR_THE_NON_BLOCKING_OWNER_DECISION",
        "actor_role": "owner",
        "authority_ref": "non-blocking owner decision",
    },
}

READY_ACTION = {
    "action": "PROCEED_TO_STAGE_G_MERGE_AUTHORITY",
    "actor_role": "authorized merger",
    "authority_ref": "G merge authority (separate; readiness is not merge authority)",
}

NOT_VERIFIABLE = (
    "T6: no supported authentication method is declared, so production readiness cannot be true",
    "live PR identity/head/base revalidation needs provider events (C1.1b)",
    "store provenance re-check covers presence and bytes of the cited authority record only",
    "mounted host coverage is UNKNOWN (T5 out of scope)",
)

HEX40 = re.compile(r"\b[0-9a-f]{40}\b")
HEX64 = re.compile(r"^[0-9a-f]{64}$")

STAGE_BY_STAGE = ("B", "D", "E")

TYPE_RULES: typing.Dict[str, typing.Tuple[type, ...]] = {
    "repo.owner": (str,),
    "repo.name": (str,),
    "change.type": (str,),
    "change.id": (int, str),
    "change.url": (str,),
    "merge_target.ref": (str,),
    "candidate_id": (str,),
    "contract_schema_version": (str,),
    "bound_set_id": (str,),
    "bound_set_version": (str,),
    "canonicalization_version": (str,),
    "conditionals_applied": (list,),
    "head_sha": (str,),
    "tree_sha": (str,),
    "base_sha": (str,),
    "parents": (list,),
    "policy_ref": (str,),
    "policy_sha256": (str,),
    "plan.sha256": (str,),
    "plan.revision_count": (int,),
    "plan.basis_ref": (str,),
    "revision_state_sha256": (str,),
    "review_heads.used": (int,),
    "review_heads.exception_id": (str,),
    "evidence_inputs_sha256": (str,),
    "stage_records": (list,),
    "plan_audit_applies": (bool,),
    "plan_audit_waiver_ref": (str,),
    "triage.schema_version": (str,),
    "triage.sha256": (str,),
    "triage.open_blocking": (int,),
    "triage.residual_accepted_count": (int,),
    "reviewer.identity_ref": (str,),
    "reviewer.role": (str,),
    "reviewer.auth_method": (str,),
    "reviewer.auth_verified": (bool,),
    "reviewer.independence.class": (str,),
    "reviewer.independence.distinct_from": (list,),
    "reviewer.independence.attestation_ref": (str,),
    "verdict.stage": (str,),
    "verdict.value": (str,),
    "verdict.record_id": (str,),
    "verdict.record_sha256": (str,),
    "verdict.posted_at": (str,),
    "verdict.posted_after_last_commit": (bool,),
    "verdict.edit_state": (dict,),
    "verdict.event_ref": (str,),
    "owner_line.id": (str,),
    "owner_line.register_sha256": (str,),
    "merge_authority_ref": (str,),
    "skills.rows": (list,),
    "skills.none_reason": (str,),
    "skills.sha256": (str,),
    "security.surfaces_touched": (list,),
    "security.mitigations": (list,),
    "security.residual": (list,),
    "security.secret_read_or_logged": (bool,),
    "security.sha256": (str,),
    "witness.diff_name_only": (list,),
    "witness.probes": (list,),
    "witness.sha256": (str,),
    "bound_fields_sha256": (str,),
}

CONDITIONAL_IDS = ("VB-C03", "VB-C05", "VB-C08", "VB-D03", "VB-G03", "VB-H02")


@dataclasses.dataclass(frozen=True)
class Blocker:
    code: str
    detail: str

    @property
    def classification(self) -> str:
        return BLOCKER_CLASSES[self.code]

    def as_dict(self) -> typing.Dict[str, str]:
        return {
            "code": self.code,
            "class": self.classification,
            "detail": self.detail,
            "recovery": PERMITTED_ACTION[self.code]["action"],
        }


@dataclasses.dataclass
class GateResult:
    readiness: bool
    blockers: typing.List[Blocker]
    checks: typing.List[typing.Dict[str, typing.List[str]]]
    derived_counts: typing.Dict[str, object]
    revision_state_sha256: str
    store_digest: str
    inputs_sha256: typing.Dict[str, object]
    permitted_next_action: typing.Dict[str, str]
    assurance: typing.Dict[str, str]
    not_verifiable: typing.List[str]

    @property
    def reason_codes(self) -> typing.List[str]:
        seen: typing.List[str] = []
        for blocker in self.blockers:
            if blocker.code not in seen:
                seen.append(blocker.code)
        return seen

    def as_dict(self) -> typing.Dict[str, object]:
        return {
            "schema_version": "aegis.verdict-gate-output/v1",
            "bound_set_id": catalogue.BOUND_SET_ID,
            "bound_set_version": catalogue.BOUND_SET_VERSION,
            "readiness": self.readiness,
            "blockers": [blocker.as_dict() for blocker in self.blockers],
            "reason_codes": self.reason_codes,
            "derived_counts": self.derived_counts,
            "revision_state_sha256": self.revision_state_sha256,
            "store_digest": self.store_digest,
            "inputs_sha256": self.inputs_sha256,
            "permitted_next_action": self.permitted_next_action,
            "assurance": self.assurance,
            "not_verifiable": self.not_verifiable,
            "checks": self.checks,
        }


@dataclasses.dataclass
class Context:
    repo_root: Path
    doc: typing.Dict[str, object]
    record: typing.Dict[str, object]
    store: records.StoreResult
    freeze: inputs.FreezeResult
    settlement: inputs.SettlementResult
    history: inputs.HeadHistory
    heads: records.ReviewHeads
    stages: inputs.StageResult
    declarations: typing.Dict[str, typing.Dict[str, object]]
    supported_auth_methods: typing.Tuple[str, ...]
    candidate_head: str
    fixture_mode: bool

    def get(self, path: str) -> typing.Tuple[bool, object]:
        return catalogue.get_path(self.doc, path)

    def text(self, path: str) -> str:
        present, value = self.get(path)
        return value if present and isinstance(value, str) else ""


def _issue(code: str, detail: str) -> Issue:
    if code not in BLOCKER_CLASSES:
        raise ValueError("unknown blocker code %r" % code)
    return Issue(code, detail)


def _record(doc: typing.Mapping[str, object]) -> typing.Dict[str, object]:
    record = doc.get("record")
    return typing.cast(typing.Dict[str, object], record) if isinstance(record, dict) else {}


# ---------------------------------------------------------------------------
# C1 completeness, closed schema, conditionals
# ---------------------------------------------------------------------------


def _schema_issues(value: typing.Any, node: typing.Dict[str, typing.Any], prefix: str) -> typing.List[Issue]:
    """Walk the closed-schema tree and report unexpected members."""

    issues: typing.List[Issue] = []
    if not isinstance(value, dict):
        return [_issue("CANONICAL_FIELD_MISSING_OR_MISMATCH", "field group %r is not an object" % prefix)]
    for key, child in value.items():
        path = "%s.%s" % (prefix, key) if prefix else str(key)
        if key not in node:
            issues.append(_issue("CANONICAL_FIELD_MISSING_OR_MISMATCH", "unexpected field %s" % path))
            continue
        subtree = node[key]
        if not subtree:
            allowed_types = TYPE_RULES.get(path, ())
            if isinstance(child, dict) and dict not in allowed_types:
                issues.append(
                    _issue("CANONICAL_FIELD_MISSING_OR_MISMATCH", "scalar field %s is an object" % path)
                )
            continue
        issues.extend(_schema_issues(child, subtree, path))
    return issues


def check_c1(ctx: Context) -> typing.List[Issue]:
    issues: typing.List[Issue] = []
    doc = ctx.doc
    schema = catalogue.allowed_schema()
    for key, value in doc.items():
        if key in catalogue.declared_metadata_keys():
            continue
        if key not in schema:
            issues.append(_issue("CANONICAL_FIELD_MISSING_OR_MISMATCH", "unexpected field %r" % key))
            continue
        issues.extend(_schema_issues(value, schema[key], str(key)) if schema[key] else [])
        if not schema[key] and isinstance(value, dict) and dict not in TYPE_RULES.get(str(key), ()):
            issues.append(
                _issue("CANONICAL_FIELD_MISSING_OR_MISMATCH", "scalar field %r is an object" % key)
            )
    for entry in catalogue.hashed_entries():
        present, value = catalogue.get_path(doc, entry.path)
        if not present or value is None:
            if entry.requiredness == catalogue.REQUIRED:
                code = "CANONICAL_FIELD_MISSING_OR_MISMATCH"
                issues.append(_issue(code, "required field %s (%s) is missing" % (entry.path, entry.entry_id)))
                if entry.group == "F":
                    issues.append(
                        _issue(
                            "VERDICT_STALE_OR_UNVERIFIED",
                            "the verdict record cannot be verified without %s" % entry.entry_id,
                        )
                    )
            continue
        expected = TYPE_RULES.get(entry.path)
        if expected and not isinstance(value, expected):
            issues.append(
                _issue(
                    "CANONICAL_FIELD_MISSING_OR_MISMATCH",
                    "field %s has the wrong type" % entry.path,
                )
            )
        if isinstance(value, str) and not value and entry.requiredness == catalogue.REQUIRED:
            issues.append(_issue("CANONICAL_FIELD_MISSING_OR_MISMATCH", "field %s is empty" % entry.path))
    if issues:
        return issues
    issues.extend(_conditional_issues(ctx))
    return issues


def _conditional_issues(ctx: Context) -> typing.List[Issue]:
    issues: typing.List[Issue] = []
    applied_raw = ctx.get("conditionals_applied")[1]
    applied: typing.Dict[str, typing.Dict[str, object]] = {}
    if not isinstance(applied_raw, list):
        return [_issue("CANONICAL_FIELD_MISSING_OR_MISMATCH", "conditionals_applied is not a list")]
    order: typing.List[str] = []
    for entry in applied_raw:
        if not isinstance(entry, dict):
            issues.append(_issue("CANONICAL_FIELD_MISSING_OR_MISMATCH", "conditionals_applied entry is not an object"))
            continue
        condition_id = entry.get("condition_id")
        if condition_id not in CONDITIONAL_IDS:
            issues.append(
                _issue("CANONICAL_FIELD_MISSING_OR_MISMATCH", "unknown condition_id %r" % (condition_id,))
            )
            continue
        if not isinstance(entry.get("applied"), bool) or not entry.get("basis_ref"):
            issues.append(
                _issue("CANONICAL_FIELD_MISSING_OR_MISMATCH", "condition %s needs applied and basis_ref" % condition_id)
            )
        order.append(typing.cast(str, condition_id))
        applied[typing.cast(str, condition_id)] = entry
    if order != sorted(order):
        issues.append(_issue("CANONICAL_FIELD_MISSING_OR_MISMATCH", "conditionals_applied is not in canonical order"))
    plan_sha_present = ctx.get("plan.sha256")[0] and ctx.get("plan.sha256")[1] is not None
    plan_basis_present = ctx.get("plan.basis_ref")[0] and bool(ctx.get("plan.basis_ref")[1])
    if not plan_sha_present and not plan_basis_present:
        issues.append(
            _issue(
                "CANONICAL_FIELD_MISSING_OR_MISMATCH",
                "VB-C03 is null and VB-C05 plan.basis_ref is absent (no plan-of-record basis)",
            )
        )
    waiver_present = ctx.get("plan_audit_waiver_ref")[0] and bool(ctx.get("plan_audit_waiver_ref")[1])
    if ctx.get("plan_audit_applies")[1] is False and not waiver_present:
        issues.append(
            _issue(
                "CANONICAL_FIELD_MISSING_OR_MISMATCH",
                "plan_audit_applies is false without a VB-D03 waiver",
            )
        )
    rows = ctx.get("skills.rows")[1]
    none_reason = ctx.get("skills.none_reason")[1]
    if isinstance(rows, list) and not rows and not none_reason:
        issues.append(
            _issue("CANONICAL_FIELD_MISSING_OR_MISMATCH", "VB-H01 is empty and VB-H02 none_reason is absent")
        )
    # VB-C08 is deliberately NOT enforced here: the budget term, its threshold
    # and the unnecessary-exception rule belong to C7 so that an exhausted
    # budget reports the LIMIT blocker REVIEW_BUDGET_EXHAUSTED rather than a
    # generic completeness failure.
    if not ctx.get("merge_authority_ref")[0] or ctx.get("merge_authority_ref")[1] is None:
        entry = applied.get("VB-G03")
        if not entry or entry.get("applied") is not False:
            issues.append(
                _issue(
                    "CANONICAL_FIELD_MISSING_OR_MISMATCH",
                    "VB-G03 merge_authority_ref is absent without a recorded not-applied condition",
                )
            )
    for condition_id in applied:
        if condition_id not in CONDITIONAL_IDS:
            issues.append(_issue("CANONICAL_FIELD_MISSING_OR_MISMATCH", "unrecorded condition %s" % condition_id))
    return issues


# ---------------------------------------------------------------------------
# C2 bound hash and sub-hashes
# ---------------------------------------------------------------------------


def _sub_hash_object(value: typing.Any, keys: typing.Sequence[str]) -> typing.Dict[str, object]:
    if not isinstance(value, dict):
        return {}
    return {key: value[key] for key in keys if key in value}


def check_c2(ctx: Context) -> typing.List[Issue]:
    issues: typing.List[Issue] = []
    if ctx.text("bound_set_id") != catalogue.BOUND_SET_ID:
        issues.append(
            _issue(
                "CANONICAL_FIELD_MISSING_OR_MISMATCH",
                "bound_set_id is not %s (v2 or lower is INVALID for a v2.1 gate)" % catalogue.BOUND_SET_ID,
            )
        )
    if ctx.text("bound_set_version") != catalogue.BOUND_SET_VERSION:
        issues.append(
            _issue(
                "CANONICAL_FIELD_MISSING_OR_MISMATCH",
                "bound_set_version is not 2.1 (v2 or lower is INVALID for a v2.1 gate)",
            )
        )
    if ctx.text("canonicalization_version") != catalogue.CANONICALIZATION_VERSION:
        issues.append(
            _issue("CANONICAL_FIELD_MISSING_OR_MISMATCH", "canonicalization_version is not JCS-RFC8785-v1")
        )
    recomputed = canonical.bound_fields_sha256(ctx.doc)
    if recomputed != ctx.get("bound_fields_sha256")[1]:
        issues.append(
            _issue("CANONICAL_FIELD_MISSING_OR_MISMATCH", "bound_fields_sha256 does not recompute")
        )
    rows = ctx.record.get("triage_rows")
    if not isinstance(rows, list):
        issues.append(_issue("REQUIRED_INPUT_UNAVAILABLE", "record.triage_rows is missing; E02 cannot be recomputed"))
    else:
        triage_object = {"schema_version": catalogue.TRIAGE_SCHEMA, "rows": sorted(
            [row for row in rows if isinstance(row, dict)],
            key=lambda row: (str(row.get("finding_id")), str(row.get("candidate_head"))),
        )}
        if canonical.digest(triage_object) != ctx.get("triage.sha256")[1]:
            issues.append(_issue("CANONICAL_FIELD_MISSING_OR_MISMATCH", "VB-E02 triage.sha256 does not recompute"))
    skills_hash = canonical.digest(_sub_hash_object(ctx.get("skills")[1], ("rows", "none_reason")))
    if skills_hash != ctx.get("skills.sha256")[1]:
        issues.append(_issue("CANONICAL_FIELD_MISSING_OR_MISMATCH", "VB-H03 skills.sha256 does not recompute"))
    security_hash = canonical.digest(
        _sub_hash_object(
            ctx.get("security")[1],
            ("surfaces_touched", "mitigations", "residual", "secret_read_or_logged"),
        )
    )
    if security_hash != ctx.get("security.sha256")[1]:
        issues.append(_issue("CANONICAL_FIELD_MISSING_OR_MISMATCH", "VB-H08 security.sha256 does not recompute"))
    witness_hash = canonical.digest(_sub_hash_object(ctx.get("witness")[1], ("diff_name_only", "probes")))
    if witness_hash != ctx.get("witness.sha256")[1]:
        issues.append(_issue("CANONICAL_FIELD_MISSING_OR_MISMATCH", "VB-H11 witness.sha256 does not recompute"))
    return issues


# ---------------------------------------------------------------------------
# C3 verdict record integrity and affirmative F verdict
# ---------------------------------------------------------------------------


def _verdict_records(ctx: Context) -> typing.List[typing.Dict[str, object]]:
    value = ctx.record.get("verdict_records")
    if not isinstance(value, list):
        return []
    return [item for item in value if isinstance(item, dict)]


def check_c3(ctx: Context) -> typing.List[Issue]:
    issues: typing.List[Issue] = []
    body = ctx.record.get("body_text")
    head = ctx.candidate_head
    if not isinstance(body, str) or not body.strip():
        issues.append(_issue("VERDICT_NOT_AFFIRMATIVE", "the verdict record has no body text"))
    else:
        first_line = body.splitlines()[0] if body.splitlines() else ""
        if not HEX40.search(first_line) or head not in first_line:
            issues.append(
                _issue(
                    "VERDICT_NOT_AFFIRMATIVE",
                    "the verdict first line does not name the exact 40-character head",
                )
            )
        if canonical.sha256_hex(body.encode("utf-8")) != ctx.get("verdict.record_sha256")[1]:
            issues.append(_issue("CANONICAL_FIELD_MISSING_OR_MISMATCH", "VB-F11 verdict body hash does not recompute"))
    edit_state = ctx.get("verdict.edit_state")[1]
    if isinstance(edit_state, dict):
        if edit_state.get("post_post_edits") != 0:
            issues.append(_issue("VERDICT_STALE_OR_UNVERIFIED", "verdict has post-post content edits"))
        if edit_state.get("deleted") is not False:
            issues.append(_issue("VERDICT_STALE_OR_UNVERIFIED", "verdict record is deleted or deleted is not false"))
        if edit_state.get("body_hash_match") is not True:
            issues.append(_issue("VERDICT_STALE_OR_UNVERIFIED", "verdict body hash does not match the posted body"))
    if ctx.get("verdict.posted_after_last_commit")[1] is not True:
        issues.append(_issue("VERDICT_STALE_OR_UNVERIFIED", "verdict was not posted after the last commit"))
    active = [record for record in _verdict_records(ctx) if record.get("active") is True]
    bound = [record for record in active if record.get("head_sha") == head]
    if len(bound) != 1:
        issues.append(
            _issue(
                "VERDICT_NOT_AFFIRMATIVE",
                "exactly one active F verdict must be bound to the evaluated head (found %d)" % len(bound),
            )
        )
    for record in active:
        if record.get("head_sha") == head and record.get("value") != "PASS":
            issues.append(
                _issue(
                    "VERDICT_NOT_AFFIRMATIVE",
                    "an active F verdict at this head is %r, not PASS" % (record.get("value"),),
                )
            )
    if bound and bound[0].get("record_id") != ctx.get("verdict.record_id")[1]:
        issues.append(
            _issue("CANONICAL_FIELD_MISSING_OR_MISMATCH", "the bound F record id does not match VB-F10")
        )
    if ctx.text("verdict.value") != "PASS":
        issues.append(
            _issue(
                "VERDICT_NOT_AFFIRMATIVE",
                "VB-F09 verdict.value is %r; readiness requires an explicit PASS" % (ctx.get("verdict.value")[1],),
            )
        )
    if ctx.text("verdict.stage") != "F":
        issues.append(_issue("CANONICAL_FIELD_MISSING_OR_MISMATCH", "VB-F08 verdict.stage is not F"))
    return issues


# ---------------------------------------------------------------------------
# C4 reviewer authenticity and independence
# ---------------------------------------------------------------------------


def check_c4(ctx: Context) -> typing.List[Issue]:
    issues: typing.List[Issue] = []
    if ctx.text("reviewer.role") != "F":
        issues.append(_issue("CANONICAL_FIELD_MISSING_OR_MISMATCH", "VB-F02 reviewer.role is not F"))
    if ctx.supported_auth_methods and not ctx.fixture_mode:
        # A supported method is a fixture-only affordance.  If one ever arrives
        # outside fixture mode this term fails closed rather than lending the
        # record an authentication it does not have (T6 undecided).
        issues.append(
            _issue(
                "VERDICT_STALE_OR_UNVERIFIED",
                "supported authentication methods are refused outside fixture mode (T6 undecided)",
            )
        )
    method = ctx.text("reviewer.auth_method")
    if method not in ctx.supported_auth_methods:
        issues.append(
            _issue(
                "VERDICT_STALE_OR_UNVERIFIED",
                "reviewer.auth_method %r is not a supported method (T6 undecided; default empty list)" % method,
            )
        )
    if ctx.get("reviewer.auth_verified")[1] is not True:
        issues.append(_issue("VERDICT_STALE_OR_UNVERIFIED", "reviewer.auth_verified is not true"))
    if ctx.text("reviewer.independence.class") != "INDEPENDENT":
        issues.append(_issue("MISSING_INDEPENDENT_APPROVAL", "reviewer independence class is not INDEPENDENT"))
    distinct = ctx.get("reviewer.independence.distinct_from")[1]
    if not isinstance(distinct, list) or not distinct:
        issues.append(_issue("MISSING_INDEPENDENT_APPROVAL", "reviewer distinct_from is empty"))
    else:
        distinct_values = [str(value) for value in distinct]
        # VB-F06/C4: distinct_from must cover the PR author, the implementing
        # identity and every declared commit author on the candidate.  The roles
        # are required tokens; declared commit-author identities must appear too.
        required_roles = {"implementer", "pr-author"}
        declared_commit_authors: typing.List[str] = []
        payload = ctx.record if isinstance(ctx.record, dict) else {}
        raw_commit_authors = payload.get("commit_authors")
        if raw_commit_authors is None and isinstance(payload.get("change"), dict):
            raw_commit_authors = typing.cast(typing.Dict[str, object], payload["change"]).get("commit_authors")
        if raw_commit_authors is None:
            reviewer = payload.get("reviewer")
            if isinstance(reviewer, dict) and isinstance(reviewer.get("independence"), dict):
                raw_commit_authors = typing.cast(typing.Dict[str, object], reviewer["independence"]).get("commit_authors")
        if isinstance(raw_commit_authors, list):
            declared_commit_authors = [str(value) for value in raw_commit_authors]
            required_roles.update(declared_commit_authors)
        missing_roles = sorted(required_roles.difference(distinct_values))
        if missing_roles:
            issues.append(
                _issue(
                    "MISSING_INDEPENDENT_APPROVAL",
                    "reviewer distinct_from does not exclude required role(s)/identity(ies): %s"
                    % ", ".join(missing_roles),
                )
            )
        identity = ctx.text("reviewer.identity_ref")
        if identity in distinct_values or identity in required_roles:
            issues.append(
                _issue("MISSING_INDEPENDENT_APPROVAL", "reviewer identity appears in its own distinct_from list")
            )
    if not ctx.text("reviewer.independence.attestation_ref"):
        issues.append(_issue("MISSING_INDEPENDENT_APPROVAL", "reviewer independence attestation_ref is missing"))
    return issues


# ---------------------------------------------------------------------------
# C5 repository/change/merge-target identity
# ---------------------------------------------------------------------------


def check_c5(ctx: Context) -> typing.List[Issue]:
    issues: typing.List[Issue] = []
    if ctx.text("change.type") not in ("PR", "RECORD"):
        issues.append(_issue("CANONICAL_FIELD_MISSING_OR_MISMATCH", "change.type is not PR or RECORD"))
    merge_ref = ctx.text("merge_target.ref")
    if not merge_ref.startswith("refs/heads/"):
        issues.append(_issue("CANONICAL_FIELD_MISSING_OR_MISMATCH", "merge_target.ref is not a full ref"))
    attestation = ctx.record.get("identity_attestation")
    if isinstance(attestation, dict):
        repo = attestation.get("repo") if isinstance(attestation.get("repo"), dict) else {}
        change = attestation.get("change") if isinstance(attestation.get("change"), dict) else {}
        if repo.get("owner") != ctx.text("repo.owner") or repo.get("name") != ctx.text("repo.name"):
            issues.append(
                _issue("CANONICAL_FIELD_MISSING_OR_MISMATCH", "repo identity does not match the supplied attestation")
            )
        if change.get("type") != ctx.text("change.type") or change.get("id") != ctx.get("change.id")[1]:
            issues.append(
                _issue("CANONICAL_FIELD_MISSING_OR_MISMATCH", "change identity does not match the supplied attestation")
            )
    return issues


# ---------------------------------------------------------------------------
# C6 exact current head/tree/base
# ---------------------------------------------------------------------------


def check_c6(ctx: Context) -> typing.List[Issue]:
    issues: typing.List[Issue] = []
    for issue in ctx.freeze.issues:
        if issue.code == "HEAD_MOVED_OR_BASE_INVALIDATED":
            issues.append(_issue(issue.code, issue.detail))
    if ctx.history.status == "VERIFIED":
        heads = [head.get("head_sha") for head in ctx.history.heads]
        if ctx.candidate_head in heads and heads[-1] != ctx.candidate_head:
            issues.append(
                _issue("HEAD_MOVED_OR_BASE_INVALIDATED", "a newer published head exists in the head history")
            )
    return issues


# ---------------------------------------------------------------------------
# C7 policy/plan/revision/budget
# ---------------------------------------------------------------------------


def _register_text(ctx: Context) -> typing.Tuple[str, typing.Optional[Issue]]:
    """Read the approval register the verdict cites (VB-G02), never a copy.

    Returns (text, issue).  An absent register or a register whose bytes do not
    match VB-G02 yields an issue and no text: the G group is resolved at gate
    time from the hashed register, so a missing or edited register can never be
    read as ACTIVE authority.
    """

    register_path = ctx.repo_root / records.REGISTER_RELATIVE_PATH
    if not register_path.is_file():
        return ("", _issue("REQUIRED_INPUT_UNAVAILABLE", "the approval register is absent"))
    raw = register_path.read_bytes()
    if canonical.sha256_hex(raw) != ctx.text("owner_line.register_sha256"):
        return (
            "",
            _issue(
                "CANONICAL_FIELD_MISSING_OR_MISMATCH",
                "VB-G02 register hash does not match the register bytes",
            ),
        )
    return (raw.decode("utf-8", "replace"), None)


def check_c7(ctx: Context) -> typing.List[Issue]:
    issues: typing.List[Issue] = []
    if not HEX64.match(ctx.text("policy_sha256")):
        issues.append(_issue("CANONICAL_FIELD_MISSING_OR_MISMATCH", "policy_sha256 is not 64 lowercase hex"))
    plan_sha = ctx.get("plan.sha256")[1]
    if isinstance(plan_sha, str) and not HEX64.match(plan_sha):
        issues.append(_issue("CANONICAL_FIELD_MISSING_OR_MISMATCH", "plan.sha256 is not 64 lowercase hex"))
    if ctx.text("revision_state_sha256") != ctx.store.revision_state_sha256():
        issues.append(
            _issue(
                "STATE_TAMPER_SUSPECTED",
                "VB-C06 revision_state_sha256 does not match the derived record",
            )
        )
    for issue in ctx.history.issues:
        # The export's own binding findings (wrong change/head, unverified
        # provenance) are contract blockers, never dropped on the floor.
        issues.append(_issue(issue.code, issue.detail))
    if ctx.history.status != "VERIFIED":
        issues.append(
            _issue("REQUIRED_INPUT_UNAVAILABLE", "the authoritative head-history export is not VERIFIED")
        )
        return issues
    if issues:
        return issues
    for issue in ctx.heads.issues:
        issues.append(_issue("STATE_TAMPER_SUSPECTED", issue.detail))
    if issues:
        return issues
    used = ctx.get("review_heads.used")[1]
    if used != ctx.heads.used:
        issues.append(
            _issue(
                "STATE_TAMPER_SUSPECTED",
                "VB-C07 review_heads.used %r does not equal the derived exclusive count %d"
                % (used, ctx.heads.used),
            )
        )
        return issues
    exception_id = ctx.get("review_heads.exception_id")[1]
    if ctx.heads.used >= 3:
        exception = ctx.record.get("review_head_exception")
        if not isinstance(exception, dict) or not exception_id or exception.get("exception_id") != exception_id:
            issues.append(
                _issue(
                    "REVIEW_BUDGET_EXHAUSTED",
                    "used=%d with no ACTIVE scoped exception covering this change/head" % ctx.heads.used,
                )
            )
            return issues
        # The exception is validated against the register identity at gate
        # time, never self-granted by the record that cites it.
        text, register_issue = _register_text(ctx)
        if register_issue is not None:
            issues.append(register_issue)
            return issues
        entry_id = typing.cast(str, exception_id)
        entry = records.resolve_register_entry(text, entry_id)
        authority = exception.get("authority_ref")
        granted = (
            records.resolve_register_entry(text, str(authority))
            if isinstance(authority, str) and authority
            else None
        )
        repo_ref = "%s/%s" % (ctx.text("repo.owner"), ctx.text("repo.name"))
        scope = exception.get("scope") if isinstance(exception.get("scope"), dict) else {}
        valid = (
            entry is not None
            and entry.status == "ACTIVE"
            and entry.scope_present
            and entry.covers(repo_ref, ctx.get("change.id")[1], ctx.candidate_head, ctx.text("merge_target.ref"))
            and granted is not None
            and granted.status == "ACTIVE"
        )
        if not valid:
            issues.append(
                _issue(
                    "REVIEW_BUDGET_EXHAUSTED",
                    "used=%d with no ACTIVE, register-resolved, scope-covering exception for %s"
                    % (ctx.heads.used, entry_id),
                )
            )
            return issues
        # The record may not claim a state or scope the register does not hold.
        if exception.get("state") != entry.status:
            issues.append(
                _issue(
                    "STATE_TAMPER_SUSPECTED",
                    "the supplied exception claims state %r but the register's effective status is %r"
                    % (exception.get("state"), entry.status),
                )
            )
        for key in records.GATE_SCOPE_FIELDS:
            if str(scope.get(key, "")) != str(entry.scope.get(key, "")):
                issues.append(
                    _issue(
                        "STATE_TAMPER_SUSPECTED",
                        "the supplied exception claims scope %s=%r but the register says %r"
                        % (key, scope.get(key), entry.scope.get(key)),
                    )
                )
    elif exception_id:
        issues.append(
            _issue("STATE_TAMPER_SUSPECTED", "an exception is recorded below the used >= 3 threshold")
        )
    return issues


# ---------------------------------------------------------------------------
# C8 required stage evidence and affirmative stage verdicts
# ---------------------------------------------------------------------------


def check_c8(ctx: Context) -> typing.List[Issue]:
    issues: typing.List[Issue] = []
    if ctx.get("plan_audit_applies")[1] is False and not ctx.text("plan_audit_waiver_ref"):
        issues.append(_issue("AUTHORITY_ABSENT", "no plan-audit waiver authority for a skipped B stage"))
    declared = ctx.get("stage_records")[1]
    declared_by_stage: typing.Dict[str, typing.Dict[str, object]] = {}
    if isinstance(declared, list):
        for entry in declared:
            if isinstance(entry, dict) and entry.get("stage") in STAGE_BY_STAGE:
                declared_by_stage[typing.cast(str, entry.get("stage"))] = entry
    for stage, declaration in sorted(ctx.declarations.items()):
        hashed = declared_by_stage.get(stage)
        if not isinstance(hashed, dict):
            issues.append(
                _issue("CANONICAL_FIELD_MISSING_OR_MISMATCH", "VB-D01 does not bind the %s stage record" % stage)
            )
            continue
        for key in ("record_id", "record_path", "bytes", "sha256", "head_sha", "verdict"):
            if hashed.get(key) != declaration.get(key):
                issues.append(
                    _issue(
                        "CANONICAL_FIELD_MISSING_OR_MISMATCH",
                        "VB-D01 and the %s stage declaration disagree on %s" % (stage, key),
                    )
                )
    issues.extend(ctx.stages.issues)
    return issues


# ---------------------------------------------------------------------------
# C9 canonical triage
# ---------------------------------------------------------------------------


def _triage_rows(ctx: Context) -> typing.List[typing.Dict[str, object]]:
    rows = ctx.record.get("triage_rows")
    if not isinstance(rows, list):
        return []
    return [row for row in rows if isinstance(row, dict)]


def check_c9(ctx: Context) -> typing.List[Issue]:
    issues: typing.List[Issue] = []
    if ctx.text("triage.schema_version") != catalogue.TRIAGE_SCHEMA:
        issues.append(_issue("CANONICAL_FIELD_MISSING_OR_MISMATCH", "VB-E01 triage schema is not aegis.triage/v1"))
    rows = _triage_rows(ctx)
    required_columns = (
        "finding_id",
        "source",
        "round",
        "candidate_head",
        "class",
        "disposition",
        "decided_by",
        "authority_ref",
        "evidence_ref",
        "decided_at",
    )
    open_blocking = 0
    for row in rows:
        for column in required_columns:
            if column not in row:
                issues.append(
                    _issue(
                        "CANONICAL_FIELD_MISSING_OR_MISMATCH",
                        "triage row %r is missing %s" % (row.get("finding_id"), column),
                    )
                )
        if row.get("candidate_head") != ctx.candidate_head:
            issues.append(
                _issue("CANONICAL_FIELD_MISSING_OR_MISMATCH", "triage row is bound to a different head")
            )
        if row.get("class") not in ("BLOCKING", "RESIDUAL", "NIT"):
            issues.append(_issue("CANONICAL_FIELD_MISSING_OR_MISMATCH", "triage row has an unknown class"))
        if row.get("disposition") not in ("FIXED", "RESIDUAL_ACCEPTED", "NIT_ACCEPTED", "REJECTED", "UNRUN"):
            issues.append(_issue("CANONICAL_FIELD_MISSING_OR_MISMATCH", "triage row has an unknown disposition"))
        decided_by = row.get("decided_by")
        if not isinstance(decided_by, dict) or not decided_by.get("role") or not decided_by.get("identity_ref"):
            issues.append(_issue("CANONICAL_FIELD_MISSING_OR_MISMATCH", "triage decided_by is incomplete"))
        if row.get("class") == "BLOCKING" and row.get("disposition") != "FIXED":
            open_blocking += 1
    declared_open = ctx.get("triage.open_blocking")[1]
    if declared_open != open_blocking:
        issues.append(
            _issue(
                "CANONICAL_FIELD_MISSING_OR_MISMATCH",
                "VB-E03 open_blocking %r does not equal the re-derived %d" % (declared_open, open_blocking),
            )
        )
    elif open_blocking > 0:
        issues.append(
            _issue("OPEN_BLOCKING_FINDING", "%d blocking triage finding(s) without a validated fix" % open_blocking)
        )
    return issues


# ---------------------------------------------------------------------------
# C10 evidence binding/reuse
# ---------------------------------------------------------------------------


def check_c10(ctx: Context) -> typing.List[Issue]:
    issues: typing.List[Issue] = list(inputs.check_evidence_set(ctx.record, ctx.doc))
    reuse = ctx.record.get("evidence_reuse")
    if isinstance(reuse, dict):
        if reuse.get("decision") != "VALID":
            issues.append(_issue("EVIDENCE_REUSE_INVALID", "the evidence-reuse decision is not VALID"))
        if reuse.get("target_head") != ctx.candidate_head:
            issues.append(_issue("EVIDENCE_REUSE_INVALID", "the reuse decision targets a different head"))
        if reuse.get("copies_pass") is True:
            issues.append(_issue("EVIDENCE_REUSE_INVALID", "the reuse decision copies a PASS"))
        if reuse.get("independence") != "INDEPENDENT":
            issues.append(_issue("EVIDENCE_REUSE_INVALID", "the reuse decision is not independent"))
    return issues


# ---------------------------------------------------------------------------
# C11 skills/security/witness
# ---------------------------------------------------------------------------


def check_c11(ctx: Context) -> typing.List[Issue]:
    issues: typing.List[Issue] = []
    flag = ctx.get("security.secret_read_or_logged")[1]
    if flag is True:
        issues.append(
            _issue(
                "SECURITY_FLAG_SET",
                "security.secret_read_or_logged is true; no exception path clears this",
            )
        )
    elif flag is not False:
        issues.append(
            _issue("CANONICAL_FIELD_MISSING_OR_MISMATCH", "security.secret_read_or_logged is absent or not boolean")
        )
    rows = ctx.get("skills.rows")[1]
    none_reason = ctx.get("skills.none_reason")[1]
    if isinstance(rows, list) and not rows and not none_reason:
        issues.append(_issue("CANONICAL_FIELD_MISSING_OR_MISMATCH", "skills rows are empty without none_reason"))
    probes = ctx.get("witness.probes")[1]
    if isinstance(probes, list):
        for probe in probes:
            if not isinstance(probe, dict) or not probe.get("probe_id"):
                issues.append(_issue("CANONICAL_FIELD_MISSING_OR_MISMATCH", "witness probe is malformed"))
    diff = ctx.get("witness.diff_name_only")[1]
    if isinstance(diff, list) and diff != sorted(str(path) for path in diff):
        issues.append(_issue("CANONICAL_FIELD_MISSING_OR_MISMATCH", "witness.diff_name_only is not in canonical order"))
    return issues


# ---------------------------------------------------------------------------
# C12 owner line / merge authority
# ---------------------------------------------------------------------------


def check_c12(ctx: Context) -> typing.List[Issue]:
    """Owner line: resolved from the register, never from the record's own claim.

    The supplied gate-time resolution is audit/display material.  It must agree
    with what the hashed register says; a forged ACTIVE status or a forged
    covering scope is refused even when the resolution record is otherwise
    well formed.
    """

    issues: typing.List[Issue] = []
    resolution = ctx.record.get("owner_line_resolution")
    if not isinstance(resolution, dict):
        return [_issue("AUTHORITY_ABSENT", "no owner-line resolution record is supplied")]
    entry_id = ctx.text("owner_line.id")
    if resolution.get("entry_id") != entry_id:
        issues.append(_issue("CANONICAL_FIELD_MISSING_OR_MISMATCH", "the resolution entry id does not match VB-G01"))
        return issues
    text, register_issue = _register_text(ctx)
    if register_issue is not None:
        return [register_issue]
    if resolution.get("register_sha256") != ctx.text("owner_line.register_sha256"):
        issues.append(
            _issue("CANONICAL_FIELD_MISSING_OR_MISMATCH", "the resolution register hash does not match the register")
        )
        return issues
    entry = records.resolve_register_entry(text, entry_id)
    if entry is None:
        issues.append(
            _issue("AUTHORITY_ABSENT", "the cited owner-line entry %r is absent from the register" % entry_id)
        )
        return issues
    if entry.status != "ACTIVE":
        issues.append(
            _issue(
                "AUTHORITY_ABSENT",
                "the register's effective status for %s is %s, not ACTIVE" % (entry_id, entry.status),
            )
        )
        return issues
    if not entry.scope_present:
        issues.append(
            _issue(
                "AUTHORITY_ABSENT",
                "the register entry %s carries no machine-checkable gate scope" % entry_id,
            )
        )
        return issues
    repo_ref = "%s/%s" % (ctx.text("repo.owner"), ctx.text("repo.name"))
    if not entry.covers(repo_ref, ctx.get("change.id")[1], ctx.candidate_head, ctx.text("merge_target.ref")):
        issues.append(
            _issue(
                "AUTHORITY_ABSENT",
                "the register entry %s does not cover this repo/change/head/merge target" % entry_id,
            )
        )
        return issues
    declared_status = resolution.get("effective_status")
    if declared_status != entry.status:
        issues.append(
            _issue(
                "STATE_TAMPER_SUSPECTED",
                "the supplied resolution claims effective_status %r but the register says %r"
                % (declared_status, entry.status),
            )
        )
    scope = resolution.get("scope") if isinstance(resolution.get("scope"), dict) else {}
    for key in records.GATE_SCOPE_FIELDS:
        if str(scope.get(key, "")) != str(entry.scope.get(key, "")):
            issues.append(
                _issue(
                    "STATE_TAMPER_SUSPECTED",
                    "the supplied resolution claims scope %s=%r but the register says %r"
                    % (key, scope.get(key), entry.scope.get(key)),
                )
            )
    return issues


# ---------------------------------------------------------------------------
# C13 readiness predicate
# ---------------------------------------------------------------------------


def check_c13(ctx: Context) -> typing.List[Issue]:
    issues: typing.List[Issue] = []
    post_f = ctx.record.get("post_f_state")
    if post_f is None:
        issues.append(_issue("REQUIRED_INPUT_UNAVAILABLE", "record.post_f_state is missing"))
    elif post_f == "SUSPENDED":
        issues.append(_issue("POST_F_BLOCKER", "the post-F state is SUSPENDED"))
    elif post_f != "ACTIVE":
        issues.append(_issue("CANONICAL_FIELD_MISSING_OR_MISMATCH", "record.post_f_state is not ACTIVE/SUSPENDED"))
    decisions = ctx.record.get("owner_decisions")
    if isinstance(decisions, list):
        for decision in decisions:
            if not isinstance(decision, dict):
                issues.append(_issue("CANONICAL_FIELD_MISSING_OR_MISMATCH", "owner decision entry is not an object"))
                continue
            if decision.get("state") == "OPEN" and decision.get("gates_readiness") is True:
                issues.append(
                    _issue(
                        "OWNER_DECISION_BLOCKING",
                        "open owner decision %r gates readiness" % (decision.get("decision_id"),),
                    )
                )
    if ctx.store.binding_status != "VERIFIED":
        issues.append(
            _issue(
                "REQUIRED_INPUT_UNAVAILABLE",
                "the record store provenance binding is %s: %s" % (ctx.store.binding_status, ctx.store.binding_detail),
            )
        )
    if not ctx.freeze.valid:
        issues.append(_issue("REQUIRED_INPUT_UNAVAILABLE", "freeze.valid is false or underivable"))
    if not ctx.settlement.settled:
        issues.append(
            _issue(
                "MISSING_REQUIRED_REVIEW_OR_DISPOSITION",
                "settlement.settled is false: a required review source is not settled or disposed",
            )
        )
    return issues


CHECKS: typing.Tuple[typing.Tuple[str, typing.Callable[[Context], typing.List[Issue]]], ...] = (
    ("C1", check_c1),
    ("C2", check_c2),
    ("C3", check_c3),
    ("C4", check_c4),
    ("C5", check_c5),
    ("C6", check_c6),
    ("C7", check_c7),
    ("C8", check_c8),
    ("C9", check_c9),
    ("C10", check_c10),
    ("C11", check_c11),
    ("C12", check_c12),
    ("C13", check_c13),
)


def _load_stage_declarations(
    directory: Path,
) -> typing.Tuple[typing.Dict[str, typing.Dict[str, object]], typing.List[Issue]]:
    """Load the required B/D/E declaration envelopes, fail closed.

    --stage-records-dir is a required input: an absent/unreadable directory, an
    empty directory, an unusable or malformed envelope, a non-B/D/E stage or a
    duplicate stage is a finding, never a silent omission.  The declarations
    are cross-checked against VB-D01 in C8 and the records themselves are
    re-hashed by inputs.validate_stage_records.
    """

    declarations: typing.Dict[str, typing.Dict[str, object]] = {}
    issues: typing.List[Issue] = []
    if not directory.is_dir():
        return (
            declarations,
            [
                _issue(
                    "REQUIRED_INPUT_UNAVAILABLE",
                    "required --stage-records-dir is absent or not a directory: %s" % directory,
                )
            ],
        )
    paths = sorted(directory.glob("*.json"))
    if not paths:
        return (
            declarations,
            [
                _issue(
                    "REQUIRED_INPUT_UNAVAILABLE",
                    "--stage-records-dir holds no stage declaration envelope: %s" % directory,
                )
            ],
        )
    for path in paths:
        try:
            envelope = inputs.load_envelope(path)
        except inputs.InputError as error:
            issues.append(
                _issue(error.code, "stage declaration %s is unusable: %s" % (path.name, error.detail))
            )
            continue
        if envelope.issues:
            issues.append(
                _issue(
                    envelope.issues[0].code,
                    "stage declaration %s is not verifiable: %s" % (path.name, envelope.issues[0].detail),
                )
            )
            continue
        stage = envelope.payload.get("stage")
        if not isinstance(stage, str) or stage not in STAGE_BY_STAGE:
            issues.append(
                _issue(
                    "CANONICAL_FIELD_MISSING_OR_MISMATCH",
                    "stage declaration %s declares no B/D/E stage" % path.name,
                )
            )
            continue
        if stage in declarations:
            issues.append(
                _issue(
                    "CANONICAL_FIELD_MISSING_OR_MISMATCH",
                    "more than one %s stage declaration envelope in --stage-records-dir" % stage,
                )
            )
            continue
        declarations[stage] = envelope.payload
    return (declarations, issues)


def _empty_result(
    code: str,
    detail: str,
    inputs_sha: typing.Dict[str, object],
    fixture_mode: bool = False,
) -> GateResult:
    blockers = [Blocker(code, detail)]
    return GateResult(
        readiness=False,
        blockers=blockers,
        checks=[{"check": "INPUTS", "status": "FAIL", "codes": [code]}],
        derived_counts={},
        revision_state_sha256="",
        store_digest="",
        inputs_sha256=inputs_sha,
        permitted_next_action=PERMITTED_ACTION[code],
        assurance=_assurance(fixture_mode),
        not_verifiable=list(NOT_VERIFIABLE),
    )


def _assurance(fixture_mode: bool) -> typing.Dict[str, str]:
    return {
        "claim": "AUDITABLE",
        "mounted_coverage": "UNKNOWN",
        "mode": "FIXTURE" if fixture_mode else "PRODUCTION",
    }


def evaluate(
    *,
    repo_root: typing.Union[str, Path],
    verdict_path: typing.Union[str, Path],
    freeze_path: typing.Union[str, Path],
    settlement_path: typing.Union[str, Path],
    head_history_path: typing.Union[str, Path],
    stage_records_dir: typing.Union[str, Path],
    records_dir: str = "docs/approvals/revision-state",
    candidate_head: typing.Optional[str] = None,
    supported_auth_methods: typing.Sequence[str] = (),
    base_ref: str = "origin/main",
    fixture_mode: bool = False,
) -> GateResult:
    """Run C1-C13 in order and return a deterministic result.  Read-only.

    supported_auth_methods is a fixture-only affordance: outside fixture_mode a
    non-empty list is refused before any record is read, so a production run
    has no path to readiness=true while owner decision T6 is undecided.
    """

    root = Path(repo_root).resolve()
    inputs_sha: typing.Dict[str, object] = {}
    if supported_auth_methods and not fixture_mode:
        return _empty_result(
            "VERDICT_STALE_OR_UNVERIFIED",
            "supported authentication methods are refused outside fixture mode: T6 is undecided, so "
            "production has no path to readiness=true",
            inputs_sha,
        )
    store = records.load_store(root, records_dir, base_ref)
    inputs_sha["store"] = {
        "manifest_sha256": canonical.sha256_hex((store.records_dir / "manifest.json").read_bytes())
        if (store.records_dir / "manifest.json").is_file()
        else "",
        "files": len(store.files),
        "git_base": store.git_base,
        "prefix_checks": store.prefix_checks,
    }
    if store.issues:
        code = store.issues[0].code
        detail = "; ".join(issue.detail for issue in store.issues)
        result = _empty_result(code, detail, inputs_sha, fixture_mode)
        result.store_digest = store.recomputed_store_digest
        return result

    loaded: typing.Dict[str, inputs.Envelope] = {}
    for name, path in (
        ("verdict", verdict_path),
        ("freeze", freeze_path),
        ("settlement", settlement_path),
        ("head_history", head_history_path),
    ):
        try:
            envelope = inputs.load_envelope(path)
        except inputs.InputError as error:
            if error.fatal:
                raise
            return _empty_result(error.code, "%s: %s" % (name, error.detail), inputs_sha, fixture_mode)
        loaded[name] = envelope
        inputs_sha[name] = envelope.report()
        if envelope.issues:
            code = envelope.issues[0].code
            detail = "; ".join(issue.detail for issue in envelope.issues)
            return _empty_result(code, "%s: %s" % (name, detail), inputs_sha, fixture_mode)

    doc = typing.cast(typing.Dict[str, object], loaded["verdict"].payload)
    record = _record(doc)
    verdict_head = doc.get("head_sha")
    resolved_head = str(verdict_head) if isinstance(verdict_head, str) else ""
    if candidate_head is not None and candidate_head != resolved_head:
        return _empty_result(
            "HEAD_MOVED_OR_BASE_INVALIDATED",
            "--candidate-head does not equal VB-B01",
            inputs_sha,
            fixture_mode,
        )

    freeze = inputs.derive_freeze(loaded["freeze"], doc)
    settlement = inputs.derive_settlement(loaded["settlement"], doc, root)
    history = inputs.validate_head_history(loaded["head_history"], doc)
    declarations, declaration_issues = _load_stage_declarations(Path(stage_records_dir))
    inputs_sha["stage_records"] = {
        stage: {
            "stage": stage,
            "record_id": declaration.get("record_id"),
            "record_path": declaration.get("record_path"),
            "sha256": declaration.get("sha256"),
            "bytes": declaration.get("bytes"),
        }
        for stage, declaration in sorted(declarations.items())
    }
    if declaration_issues:
        return _empty_result(
            declaration_issues[0].code,
            "; ".join(issue.detail for issue in declaration_issues),
            inputs_sha,
            fixture_mode,
        )
    plan_audit_applies = doc.get("plan_audit_applies") is True
    applicable_stages = ["D", "E"] + (["B"] if plan_audit_applies else [])
    missing_stages = [stage for stage in applicable_stages if stage not in declarations]
    if missing_stages:
        return _empty_result(
            "REQUIRED_INPUT_UNAVAILABLE",
            "--stage-records-dir is missing required stage declaration(s): %s"
            % ", ".join(missing_stages),
            inputs_sha,
            fixture_mode,
        )
    stages = inputs.validate_stage_records(root, doc.get("stage_records"), resolved_head, plan_audit_applies)
    heads = records.derive_review_heads(store.change_events, history.heads, resolved_head)
    ctx = Context(
        repo_root=root,
        doc=doc,
        record=record,
        store=store,
        freeze=freeze,
        settlement=settlement,
        history=history,
        heads=heads,
        stages=stages,
        declarations=declarations,
        supported_auth_methods=tuple(supported_auth_methods),
        candidate_head=resolved_head,
        fixture_mode=fixture_mode,
    )

    checks: typing.List[typing.Dict[str, typing.List[str]]] = []
    blockers: typing.List[Blocker] = []
    for name, check in CHECKS:
        issues = check(ctx)
        codes = sorted({issue.code for issue in issues})
        checks.append({"check": name, "status": "FAIL" if issues else "PASS", "codes": codes})
        if issues:
            for issue in issues:
                blockers.append(Blocker(issue.code, issue.detail))
            break
    readiness = not blockers
    if readiness and not fixture_mode:
        # Structural invariant, not a policy override: readiness needs a
        # supported authentication method and no method exists while T6 is
        # undecided, so a production run can never be ready.
        blockers.append(
            Blocker(
                "VERDICT_STALE_OR_UNVERIFIED",
                "production readiness is unreachable while owner decision T6 is undecided "
                "(a supported method is fixture mode only)",
            )
        )
        readiness = False
    first_code = blockers[0].code if blockers else None
    return GateResult(
        readiness=readiness,
        blockers=blockers,
        checks=checks,
        derived_counts={
            "items": [store.items[key].as_derived() for key in sorted(store.items)],
            "review_heads_used": heads.used,
            "derived_ordinal": heads.ordinal,
            "ledger_heads": heads.ledger_count,
        },
        revision_state_sha256=store.revision_state_sha256(),
        store_digest=store.recomputed_store_digest,
        inputs_sha256=inputs_sha,
        permitted_next_action=READY_ACTION if readiness else PERMITTED_ACTION[first_code],
        assurance=_assurance(fixture_mode),
        not_verifiable=list(NOT_VERIFIABLE),
    )
