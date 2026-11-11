"""Producer-side derivation and fail-closed checks for change-state records.

Every function here derives a value; none of them accepts a declared value on
trust and none of them returns a readiness verdict.  Readiness remains the
merged checker's job (tools/aegis_verdict_gate/): this module only proves that
the records it produced are internally consistent, bound to one frozen head,
and fail closed under the adversarial conditions C1.3 exercises.

Codes are the merged checker's blocker codes where a term maps to one.  Where
this producer is stricter than the merged checker (an UNRUN pre-audit outcome
cannot settle; a second freeze never wins) the README states the divergence and
the merged checker stays authoritative for readiness.
"""

from __future__ import annotations

import typing
from pathlib import Path

from . import ASSURANCE, NOT_VERIFIABLE
from .schema import (
    AFFIRMATIVE_STAGE,
    CODE_AUTHORITY_ABSENT,
    CODE_BUDGET,
    CODE_CANONICAL,
    CODE_HEAD_MOVED,
    CODE_MISSING_REVIEW,
    CODE_REQUIRED_INPUT,
    CODE_STAGE,
    CODE_TAMPER,
    DISPOSITION_AUTHORITY_SCHEMA,
    DISPOSITION_DECISION,
    DISPOSITION_SCOPE_FIELDS,
    INDEPENDENCE_CLASSES,
    PRE_AUDIT_STATES,
    REVIEW_SOURCE_STATES,
    STAGE_VERDICTS,
    STAGES,
    Issue,
    build_envelope,
    digest,
    envelope_issues,
    immutable_inputs_digest,
    is_hex,
    payload_issues,
    sha256_hex,
    stage_record_consistency_issues,
)


def _document_issues(document: object, kind: str, label: str) -> typing.Tuple[typing.Dict[str, object], typing.List[Issue]]:
    """Validate one envelope and return (payload, issues)."""

    issues = envelope_issues(document, label)
    payload = document.get("payload") if isinstance(document, dict) else None
    if not isinstance(payload, dict):
        return ({}, issues + [Issue(CODE_CANONICAL, "%s has no payload" % label)])
    issues.extend(payload_issues(kind, payload))
    return (payload, issues)


def derive_freeze(payload: typing.Mapping[str, object]) -> typing.Dict[str, object]:
    """Return the *derived* freeze terms (never the declared ones)."""

    immutable = payload.get("immutable_inputs") if isinstance(payload.get("immutable_inputs"), dict) else {}
    return {
        "immutable_inputs_sha256": immutable_inputs_digest(immutable),
        "head_sha": payload.get("head_sha"),
        "tree_sha": payload.get("tree_sha"),
        "base_sha": payload.get("base_sha"),
        "candidate_id": payload.get("candidate_id"),
        "mutation_events": len(payload.get("mutation_events") or []),
    }


def freeze_issues(
    document: object,
    *,
    identity: typing.Optional[typing.Mapping[str, object]] = None,
    label: str = "freeze",
) -> typing.Tuple[typing.List[Issue], typing.Dict[str, object]]:
    """Re-derive freeze validity: immutable hash, moves and mutation events."""

    payload, issues = _document_issues(document, "freeze", label)
    if not payload:
        return (issues, {"valid": False})
    derived = derive_freeze(payload)
    immutable = payload.get("immutable_inputs") if isinstance(payload.get("immutable_inputs"), dict) else {}
    if immutable:
        if payload.get("immutable_inputs_sha256") != derived["immutable_inputs_sha256"]:
            issues.append(Issue(CODE_REQUIRED_INPUT, "freeze.immutable_inputs_sha256 does not recompute"))
        for key in ("head_sha", "tree_sha", "base_sha"):
            if immutable.get(key) != payload.get(key):
                issues.append(
                    Issue(CODE_HEAD_MOVED, "freeze.%s does not equal its own immutable input %s" % (key, key))
                )
    if derived["mutation_events"]:
        issues.append(Issue(CODE_HEAD_MOVED, "freeze.mutation_events is not empty after frozen_at"))
    if identity:
        for key in ("head_sha", "tree_sha", "base_sha"):
            if identity.get(key) is not None and payload.get(key) != identity.get(key):
                issues.append(Issue(CODE_HEAD_MOVED, "freeze.%s has moved from the evaluated %s" % (key, key)))
        if identity.get("candidate_id") is not None and payload.get("candidate_id") != identity.get("candidate_id"):
            issues.append(Issue(CODE_REQUIRED_INPUT, "freeze.candidate_id does not equal the evaluated candidate"))
    valid = not issues
    if payload.get("valid") is False:
        issues.append(Issue(CODE_REQUIRED_INPUT, "freeze record declares valid=false"))
        valid = False
    elif payload.get("valid") is True and not valid:
        issues.append(Issue(CODE_CANONICAL, "freeze declares valid=true but the record does not validate"))
    return (issues, {"valid": valid, **derived})


def freeze_set_issues(documents: typing.Sequence[object]) -> typing.Tuple[typing.List[Issue], typing.List[typing.Dict[str, object]]]:
    """At most one authoritative freeze per candidate; a re-freeze never wins."""

    issues: typing.List[Issue] = []
    payloads: typing.List[typing.Dict[str, object]] = []
    for document in documents:
        payload, item_issues = _document_issues(document, "freeze", "freeze")
        issues.extend(item_issues)
        payloads.append(payload)
    by_candidate: typing.Dict[str, typing.List[typing.Dict[str, object]]] = {}
    for payload in payloads:
        by_candidate.setdefault(str(payload.get("candidate_id")), []).append(payload)
    for candidate, records in sorted(by_candidate.items()):
        if len(records) > 1:
            issues.append(
                Issue(
                    CODE_TAMPER,
                    "candidate %r has %d freeze records; a second/racing freeze is INVALID and never "
                    "silently replaces the first" % (candidate, len(records)),
                )
            )
    return (issues, payloads)


def _scope_matches(scope: object, identity: typing.Mapping[str, object]) -> bool:
    if not isinstance(scope, dict):
        return False
    for key in DISPOSITION_SCOPE_FIELDS:
        if str(scope.get(key, "")) != str(identity.get(key, "")):
            return False
    return True


def verify_disposition_authority(
    authority_root: typing.Optional[typing.Union[str, Path]],
    identity: typing.Optional[typing.Mapping[str, object]],
    source: typing.Mapping[str, object],
) -> typing.Tuple[bool, str]:
    """Structurally verify a cited aegis.disposition-authority/v1 record.

    Owner decision T7 (general fourth-head / unavailable-review authority) is
    undefined, so no such record can legitimately be produced by this slice;
    the structural route below exists because the merged checker defines it,
    and a record is only honoured when it is present, ACTIVE, decided, not
    time-bounded and scoped to this exact change/head/merge target.
    """

    authority = source.get("disposition_authority_ref")
    if not isinstance(authority, str) or not authority:
        return (False, "no disposition authority is cited (owner decision T7 is undefined)")
    if authority_root is None or identity is None:
        return (False, "the disposition authority cannot be resolved without the evaluated change")
    declared_sha = source.get("disposition_authority_sha256")
    if not is_hex(declared_sha, 64):
        return (False, "the disposition authority cites no 64-hex sha256")
    if not _scope_matches(source.get("disposition_scope"), identity):
        return (False, "the disposition scope does not cover this repo/change/head/merge target")
    if source.get("expires") not in (None, ""):
        return (False, "a time-bounded disposition authority cannot be evaluated offline")
    root = Path(authority_root).resolve()
    path = (root / authority).resolve()
    try:
        path.relative_to(root)
    except ValueError:
        return (False, "the disposition authority path escapes the repository")
    if not path.is_file():
        return (False, "the disposition authority record is absent: %s" % authority)
    raw = path.read_bytes()
    if sha256_hex(raw) != declared_sha:
        return (False, "the disposition authority bytes do not match the cited sha256")
    try:
        import json

        document = json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, ValueError):
        return (False, "the disposition authority is not UTF-8 JSON")
    if not isinstance(document, dict):
        return (False, "the disposition authority is not a JSON object")
    if document.get("schema_version") != DISPOSITION_AUTHORITY_SCHEMA:
        return (False, "the disposition authority does not declare %s" % DISPOSITION_AUTHORITY_SCHEMA)
    record_id = document.get("authority_id")
    if not isinstance(record_id, str) or not record_id:
        return (False, "the disposition authority declares no authority_id")
    cited_id = source.get("disposition_authority_id")
    if isinstance(cited_id, str) and cited_id and cited_id != record_id:
        return (False, "the disposition authority declares a different authority_id")
    if document.get("status") != "ACTIVE":
        return (False, "the disposition authority is not ACTIVE")
    if document.get("decision") != DISPOSITION_DECISION:
        return (False, "the disposition authority did not decide UNAVAILABLE_REVIEW")
    if not _scope_matches(document.get("scope"), identity):
        return (False, "the disposition authority's own scope does not cover this change")
    return (True, "disposition authority %s resolves ACTIVE at the cited sha256" % authority)


def settlement_issues(
    document: object,
    *,
    authority_root: typing.Optional[typing.Union[str, Path]] = None,
    identity: typing.Optional[typing.Mapping[str, object]] = None,
    freeze: typing.Optional[typing.Mapping[str, object]] = None,
    label: str = "settlement",
) -> typing.Tuple[typing.List[Issue], typing.Dict[str, object]]:
    """Re-derive settlement.settled from recorded checks and review sources."""

    payload, issues = _document_issues(document, "settlement", label)
    derived: typing.Dict[str, object] = {"settled": False, "pre_audit_checks": 0, "review_sources": 0}
    if not payload:
        return (issues, derived)
    checks = payload.get("pre_audit_checks") if isinstance(payload.get("pre_audit_checks"), list) else []
    sources = payload.get("review_sources") if isinstance(payload.get("review_sources"), list) else []
    derived["pre_audit_checks"] = len(checks)
    derived["review_sources"] = len(sources)
    settled = True
    for check in checks:
        if not isinstance(check, dict):
            settled = False
            continue
        state = check.get("state")
        if state == "unrun":
            settled = False
            issues.append(
                Issue(
                    CODE_MISSING_REVIEW,
                    "pre-audit check %r is UNRUN; a settlement cannot be recorded before every check has an "
                    "outcome" % (check.get("check_id"),),
                )
            )
        elif state not in PRE_AUDIT_STATES:
            settled = False
            issues.append(Issue(CODE_CANONICAL, "pre-audit check %r has no recorded outcome" % (check.get("check_id"),)))
    for source in sources:
        if not isinstance(source, dict):
            settled = False
            continue
        state = source.get("state")
        if state == "PENDING":
            settled = False
            issues.append(
                Issue(
                    CODE_MISSING_REVIEW,
                    "review source %r is PENDING (not settled)" % (source.get("source_id"),),
                )
            )
        elif state == "UNAVAILABLE_DISPOSITIONED":
            verified, detail = verify_disposition_authority(authority_root, identity, source)
            if not verified:
                settled = False
                issues.append(
                    Issue(
                        CODE_MISSING_REVIEW,
                        "review source %r has no policy-authorised unavailable disposition: %s"
                        % (source.get("source_id"), detail),
                    )
                )
        elif state != "SETTLED":
            settled = False
            issues.append(Issue(CODE_CANONICAL, "review source %r has an invalid state %r" % (source.get("source_id"), state)))
    if isinstance(freeze, dict):
        frozen_at = freeze.get("frozen_at")
        as_of = payload.get("as_of")
        if isinstance(frozen_at, str) and isinstance(as_of, str) and as_of < frozen_at:
            settled = False
            issues.append(
                Issue(CODE_MISSING_REVIEW, "settlement as_of precedes the freeze; the record is premature")
            )
    if issues:
        settled = False
    declared = payload.get("settled")
    if isinstance(declared, bool) and declared != settled:
        issues.append(Issue(CODE_CANONICAL, "declared settlement.settled disagrees with the re-derivation"))
        settled = False
    derived["settled"] = settled
    return (issues, derived)


def stage_issues(
    documents: typing.Sequence[object],
    *,
    root: typing.Union[str, Path],
    frozen_head: typing.Optional[str] = None,
    plan_audit_applies: bool = True,
    snapshot_ids: typing.Optional[typing.Sequence[str]] = None,
    change_id: typing.Optional[str] = None,
) -> typing.Tuple[typing.List[Issue], typing.Dict[str, object]]:
    """Exactly one B/D/E declaration per applicable stage, bound to one head.

    Re-hashes each record, refuses duplicates, stage substitution (E offered as
    D), a non-affirmative verdict, a non-independent holder, a snapshot that is
    not one of this head's snapshots and a record bound to another head.
    """

    issues: typing.List[Issue] = []
    by_stage: typing.Dict[str, typing.Dict[str, object]] = {}
    bodies: typing.Dict[str, typing.Dict[str, object]] = {}
    root_path = Path(root).resolve()
    for index, document in enumerate(documents):
        payload, item_issues = _document_issues(document, "stage", "stage[%d]" % index)
        issues.extend(item_issues)
        stage = payload.get("stage")
        if not isinstance(stage, str) or stage not in STAGES:
            continue
        if stage in by_stage:
            issues.append(
                Issue(CODE_CANONICAL, "more than one %s stage declaration is bound (duplicate lane)" % stage)
            )
            continue
        by_stage[stage] = payload
    for stage in ("D", "E"):
        if stage not in by_stage:
            issues.append(Issue(CODE_REQUIRED_INPUT, "required %s stage declaration is missing" % stage))
    if plan_audit_applies and "B" not in by_stage:
        issues.append(Issue(CODE_REQUIRED_INPUT, "required B stage declaration is missing"))
    for stage, payload in sorted(by_stage.items()):
        if plan_audit_applies and stage == "B" and payload.get("applicability") == "WAIVED":
            issues.append(Issue(CODE_STAGE, "B is WAIVED but plan_audit_applies is true"))
        if payload.get("applicability") == "WAIVED" and not payload.get("waiver_ref"):
            issues.append(Issue(CODE_STAGE, "a WAIVED stage declaration cites no waiver_ref"))
        if change_id is not None and payload.get("change_id") != change_id:
            issues.append(Issue(CODE_CANONICAL, "%s declaration is for another change" % stage))
        record_path = payload.get("record_path")
        if not isinstance(record_path, str) or not record_path:
            continue
        candidate = Path(record_path)
        if candidate.is_absolute():
            issues.append(Issue(CODE_CANONICAL, "%s record_path is absolute" % stage))
            continue
        resolved = (root_path / candidate).resolve()
        try:
            resolved.relative_to(root_path)
        except ValueError:
            issues.append(Issue(CODE_CANONICAL, "%s record_path escapes the bundle" % stage))
            continue
        if not resolved.is_file():
            issues.append(Issue(CODE_REQUIRED_INPUT, "%s stage record file is absent: %s" % (stage, record_path)))
            continue
        raw = resolved.read_bytes()
        if payload.get("bytes") != len(raw):
            issues.append(Issue(CODE_CANONICAL, "%s stage record bytes do not recompute" % stage))
        if payload.get("sha256") != sha256_hex(raw):
            issues.append(Issue(CODE_CANONICAL, "%s stage record sha256 does not recompute" % stage))
        if frozen_head is not None and payload.get("head_sha") != frozen_head:
            issues.append(Issue(CODE_STAGE, "%s stage record is not bound to the frozen head" % stage))
        if payload.get("independence_class") != "INDEPENDENT":
            issues.append(Issue(CODE_STAGE, "%s stage record is not INDEPENDENT" % stage))
        snapshot_identity = payload.get("snapshot_identity")
        if not isinstance(snapshot_identity, str) or not snapshot_identity:
            issues.append(Issue(CODE_STAGE, "%s stage record has no snapshot identity" % stage))
        elif snapshot_ids is not None and snapshot_identity not in snapshot_ids:
            issues.append(
                Issue(CODE_STAGE, "%s stage record names a snapshot that does not belong to this head" % stage)
            )
        verdict = payload.get("verdict")
        if verdict not in STAGE_VERDICTS[stage]:
            issues.append(Issue(CODE_STAGE, "%s verdict %r is not in the stage vocabulary" % (stage, verdict)))
        elif verdict != AFFIRMATIVE_STAGE[stage]:
            issues.append(Issue(CODE_STAGE, "%s verdict %r is not affirmative" % (stage, verdict)))
        try:
            import json

            body = json.loads(raw.decode("utf-8"))
        except (UnicodeDecodeError, ValueError):
            body = None
        if isinstance(body, dict) and "stage" in body:
            issues.extend(payload_issues("stage_record", body))
            issues.extend(stage_record_consistency_issues(payload, body))
            bodies[stage] = body
    derived: typing.Dict[str, object] = {
        "stages": {stage: payload.get("verdict") for stage, payload in sorted(by_stage.items())},
        "declared": len(documents),
        "active_holders": {
            stage: payload.get("holder_identity_ref") for stage, payload in sorted(by_stage.items())
        },
        "bodies_checked": sorted(bodies),
        "plan_audit_applies": plan_audit_applies,
    }
    return (issues, derived)


def head_history_issues(
    document: object,
    *,
    change_id: typing.Optional[str],
    candidate_head: typing.Optional[str],
    ledger_events: typing.Optional[typing.Sequence[typing.Mapping[str, object]]] = None,
    exception_resolved: bool = False,
    label: str = "head-history",
) -> typing.Tuple[typing.List[Issue], typing.Dict[str, object]]:
    """Bind the export to this change/head and re-derive the exclusive budget."""

    payload, issues = _document_issues(document, "head_history", label)
    derived: typing.Dict[str, object] = {"used": 0, "ordinal": 1, "head_count": 0, "exception_required": False}
    if not payload:
        return (issues, derived)
    status = document.get("provenance", {}).get("status") if isinstance(document, dict) else None
    if status != "VERIFIED":
        issues.append(
            Issue(
                CODE_REQUIRED_INPUT,
                "head-history provenance.status is %r, not VERIFIED: the export cannot drive the budget"
                % (status,),
            )
        )
    if change_id is not None and str(payload.get("change_id")) != str(change_id):
        issues.append(Issue(CODE_REQUIRED_INPUT, "head-history export is for another change"))
    if candidate_head is not None and str(payload.get("candidate_head")) != str(candidate_head):
        issues.append(Issue(CODE_REQUIRED_INPUT, "head-history export is captured for another head"))
    heads = payload.get("heads") if isinstance(payload.get("heads"), list) else []
    export_heads: typing.List[str] = []
    exception_heads: typing.List[str] = []
    for head in heads:
        if not isinstance(head, dict):
            continue
        head_sha = head.get("head_sha")
        if is_hex(head_sha, 40):
            export_heads.append(str(head_sha))
            if head.get("exception_ref"):
                exception_heads.append(str(head_sha))
    seqs = [head.get("seq") for head in heads if isinstance(head, dict)]
    if seqs != list(range(1, len(seqs) + 1)):
        issues.append(Issue(CODE_TAMPER, "head-history ordinals are not contiguous from 1"))
    if len(set(export_heads)) != len(export_heads):
        issues.append(Issue(CODE_TAMPER, "head-history contains a duplicate head"))
    if candidate_head is not None and candidate_head in export_heads:
        if export_heads[-1] != candidate_head:
            issues.append(Issue(CODE_TAMPER, "the candidate head is not the last published head"))
    used = sum(1 for head in export_heads if head != candidate_head)
    derived["used"] = used
    derived["ordinal"] = used + 1
    derived["head_count"] = len(export_heads)
    if ledger_events is not None:
        ledger_heads = [
            str(event.get("head_sha"))
            for event in ledger_events
            if isinstance(event, dict) and is_hex(event.get("head_sha"), 40)
        ]
        if len(set(ledger_heads)) != len(ledger_heads):
            issues.append(Issue(CODE_TAMPER, "the change ledger repeats a head"))
        if candidate_head is not None and candidate_head in ledger_heads:
            issues.append(Issue(CODE_TAMPER, "the change ledger records the candidate head as published"))
        prior_export = [head for head in export_heads if head != candidate_head]
        if ledger_heads != prior_export:
            issues.append(
                Issue(
                    CODE_TAMPER,
                    "the change ledger must mirror all %d previously published head(s) exactly (it records %d); "
                    "a truncated or extra ledger is tamper" % (len(prior_export), len(ledger_heads)),
                )
            )
    if used >= 3:
        derived["exception_required"] = True
        if not exception_heads:
            issues.append(
                Issue(
                    CODE_BUDGET,
                    "used=%d reaches the fourth head without a scoped exception" % used,
                )
            )
        elif not exception_resolved:
            issues.append(
                Issue(
                    CODE_AUTHORITY_ABSENT,
                    "the cited fourth-head exception does not resolve ACTIVE in the approval register; a "
                    "self-written exception is not an approval (owner decision T7 is undefined)",
                )
            )
    return (issues, derived)


def _relative(root: Path, path: typing.Union[str, Path]) -> str:
    try:
        return Path(path).resolve().relative_to(root).as_posix()
    except ValueError:
        return Path(path).name


def validate_bundle(
    root: typing.Union[str, Path],
    *,
    identity: typing.Optional[typing.Mapping[str, object]] = None,
    base_ref: typing.Optional[str] = None,
    plan_audit_applies: bool = True,
    snapshot_repo: typing.Optional[typing.Union[str, Path]] = None,
    exception_resolved: bool = False,
) -> typing.Dict[str, object]:
    """Validate one complete change-state bundle; never computes readiness."""

    from . import records, snapshot

    root_path = Path(root).resolve()
    discovered = records.discover_bundle(root_path)
    blockers: typing.List[Issue] = []
    records_report: typing.Dict[str, typing.Dict[str, object]] = {}
    derived: typing.Dict[str, object] = {}

    def load(paths: typing.Sequence[str], label: str) -> typing.List[object]:
        documents: typing.List[object] = []
        for path in paths:
            try:
                documents.append(__import__("json").loads(Path(path).read_bytes().decode("utf-8")))
            except (OSError, UnicodeDecodeError, ValueError) as error:
                blockers.append(Issue(CODE_REQUIRED_INPUT, "%s is unusable: %s (%s)" % (label, path, error)))
        return documents

    freeze_documents = load(discovered["freeze"], "freeze")
    if not freeze_documents:
        blockers.append(Issue(CODE_REQUIRED_INPUT, "required freeze input is absent"))
    freeze_payload: typing.Dict[str, object] = {}
    if freeze_documents:
        freeze_set, freeze_payloads = freeze_set_issues(freeze_documents)
        blockers.extend(freeze_set)
        freeze_payload = freeze_payloads[0] if freeze_payloads else {}
        if freeze_payload:
            item_issues, derived_freeze = freeze_issues(freeze_documents[0], identity=identity)
            blockers.extend(item_issues)
            derived["freeze"] = derived_freeze
            frozen_head = str(freeze_payload.get("head_sha")) if freeze_payload.get("head_sha") else None
            change_id = str(freeze_payload.get("change_id")) if freeze_payload.get("change_id") else None
        else:
            frozen_head, change_id = None, None
    else:
        frozen_head, change_id = None, None

    settlement_documents = load(discovered["settlement"], "settlement")
    if not settlement_documents:
        blockers.append(Issue(CODE_REQUIRED_INPUT, "required settlement input is absent"))
    elif len(settlement_documents) > 1:
        blockers.append(Issue(CODE_TAMPER, "more than one settlement record is bound"))
    if settlement_documents:
        item_issues, derived_settlement = settlement_issues(
            settlement_documents[0],
            authority_root=root_path if settlement_documents else None,
            identity=identity,
            freeze=freeze_payload or None,
        )
        blockers.extend(item_issues)
        derived["settlement"] = derived_settlement

    snapshot_ids: typing.List[str] = []
    for path in discovered["snapshots"]:
        try:
            document = __import__("json").loads(Path(path).read_bytes().decode("utf-8"))
        except (OSError, UnicodeDecodeError, ValueError) as error:
            blockers.append(Issue(CODE_REQUIRED_INPUT, "snapshot manifest is unusable: %s (%s)" % (path, error)))
            continue
        payload = document.get("payload") if isinstance(document, dict) else None
        if not isinstance(payload, dict):
            blockers.append(Issue(CODE_CANONICAL, "snapshot manifest has no payload: %s" % path))
            continue
        blockers.extend(envelope_issues(document, "snapshot"))
        blockers.extend(payload_issues("snapshot", payload))
        blockers.extend(snapshot.retention_issues(payload))
        if freeze_payload:
            blockers.extend(snapshot.binding_issues(payload, freeze_payload))
        if snapshot_repo is not None:
            blockers.extend(snapshot.verify_manifest(snapshot_repo, payload))
        if isinstance(payload.get("snapshot_id"), str):
            snapshot_ids.append(str(payload["snapshot_id"]))
        derived.setdefault("snapshots", []).append(
            {
                "snapshot_id": payload.get("snapshot_id"),
                "commit": payload.get("commit"),
                "archive_sha256": payload.get("archive_sha256"),
                "file_count": payload.get("file_count"),
            }
        )
    if not snapshot_ids:
        blockers.append(Issue(CODE_REQUIRED_INPUT, "no per-head snapshot manifest is present"))

    stage_documents = load(discovered["stage-records"], "stage declaration")
    if not stage_documents:
        blockers.append(Issue(CODE_REQUIRED_INPUT, "no stage declaration envelope is present"))
    stage_result, derived_stage = stage_issues(
        stage_documents,
        root=root_path,
        frozen_head=frozen_head,
        plan_audit_applies=plan_audit_applies,
        snapshot_ids=snapshot_ids or None,
        change_id=change_id,
    )
    blockers.extend(stage_result)
    derived["stage_records"] = derived_stage

    head_documents = load(discovered["head-history"], "head-history")
    if not head_documents:
        blockers.append(Issue(CODE_REQUIRED_INPUT, "required head-history input is absent"))
    elif len(head_documents) > 1:
        blockers.append(Issue(CODE_TAMPER, "more than one head-history export is bound"))
    ledger_events: typing.List[typing.Dict[str, object]] = []
    for path in discovered["ledger"]:
        events, lines, ledger_issues = records.read_jsonl(path)
        blockers.extend(ledger_issues)
        blockers.extend(records.validate_chain(events, lines))
        ledger_events.extend(events)
    if head_documents:
        item_issues, derived_heads = head_history_issues(
            head_documents[0],
            change_id=change_id,
            candidate_head=frozen_head,
            ledger_events=ledger_events if discovered["ledger"] else None,
            exception_resolved=exception_resolved,
        )
        blockers.extend(item_issues)
        derived["review_heads"] = derived_heads
    if not discovered["ledger"]:
        blockers.append(Issue(CODE_REQUIRED_INPUT, "no change ledger is present"))

    manifest_path = Path(discovered["manifest"][0]) if discovered["manifest"] else None
    if manifest_path is None:
        blockers.append(Issue(CODE_REQUIRED_INPUT, "no change-state manifest is present"))
    else:
        manifest = load([str(manifest_path)], "manifest")
        if manifest:
            blockers.extend(records.validate_manifest(root_path, manifest[0]))
            if isinstance(manifest[0], dict):
                blockers.extend(assurance_issues(manifest[0]))
            if change_id is not None and isinstance(manifest[0], dict) and manifest[0].get("change_id") != change_id:
                blockers.append(Issue(CODE_CANONICAL, "manifest change_id disagrees with the freeze"))
            if base_ref is not None:
                paths = [
                    entry.get("path")
                    for entry in manifest[0].get("files", [])
                    if isinstance(entry, dict) and isinstance(entry.get("path"), str)
                ] if isinstance(manifest[0], dict) else []
                derived["prefix_checks"] = records.prefix_check(root_path, paths, base_ref)

    for key, paths in sorted(discovered.items()):
        for path in paths:
            raw = Path(path).read_bytes()
            records_report[_relative(root_path, path)] = {"bytes": len(raw), "sha256": sha256_hex(raw)}
            derived.setdefault("record_kinds", {})[key] = derived.get("record_kinds", {}).get(key, 0) + 1

    return {
        "ok": not blockers,
        "blockers": [issue.as_dict() for issue in blockers],
        "derived": derived,
        "records": records_report,
        "assurance": {
            "claim": ASSURANCE["claim"],
            "mounted_coverage": ASSURANCE["mounted_coverage"],
            "enforced": "BLOCKED",
        },
        "readiness": "NOT_COMPUTED",
        "not_verifiable": list(NOT_VERIFIABLE),
    }


def assurance_issues(manifest: typing.Mapping[str, object]) -> typing.List[Issue]:
    """A producer record may not claim enforcement, coverage or readiness."""

    issues: typing.List[Issue] = []
    claim = manifest.get("assurance_claim")
    if claim not in ("NONE", "AUDITABLE"):
        issues.append(
            Issue(CODE_CANONICAL, "assurance claim %r is not NONE/AUDITABLE" % (claim,))
        )
    coverage = manifest.get("mounted_coverage")
    if coverage != "UNKNOWN":
        issues.append(
            Issue(
                CODE_CANONICAL,
                "mounted coverage %r is claimed without a T5 export (it must stay UNKNOWN)" % (coverage,),
            )
        )
    for key in ("readiness", "ready", "green"):
        if key in manifest:
            issues.append(
                Issue(
                    CODE_AUTHORITY_ABSENT,
                    "a producer record asserts %r; readiness is only ever derived by the merged checker" % key,
                )
            )
    return issues
