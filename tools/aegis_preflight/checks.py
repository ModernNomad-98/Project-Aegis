"""PF-01..PF-10 preflight checks (read-only, fail closed).

The preflight composes exactly two read-only tools — the merged C1.1a checker
(PF-07) and the C2.3 evidence-reuse validator (PF-08) — plus read-only git
plumbing in the checker itself.  It does not invoke, wrap or duplicate the
existing DCO / PR-body / record-check / environment / link checks.

Every check returns PASS, FAIL, BLOCKED or UNRUN.  A missing, unparseable or
tampered required input can never default to PASS, and a checker BLOCKED result
is reported as BLOCKED, never converted to PASS.
"""

from __future__ import annotations

import ast
import dataclasses
import json
import subprocess
import sys
import typing
from pathlib import Path

from . import models

FORBIDDEN_NETWORK_MODULES = (
    "aiohttp",
    "ftplib",
    "http",
    "httpx",
    "requests",
    "smtplib",
    "socket",
    "ssl",
    "telnetlib",
    "urllib",
    "urllib3",
)
FORBIDDEN_WRITE_CALLS = (
    "os.system",
    "os.popen",
    "subprocess.Popen",
    "subprocess.call",
    "subprocess.check_call",
    "subprocess.check_output",
)
FORBIDDEN_WRITE_METHODS = ("write_text", "write_bytes", "unlink", "mkdir", "rename", "rmdir")


@dataclasses.dataclass
class Context:
    bundle: models.Bundle
    repo_root: Path
    fixture_mode: bool
    code_root: Path
    supported_auth_methods: typing.Sequence[str] = ()
    checker_result: typing.Optional[typing.Dict[str, object]] = None
    checker_exit: typing.Optional[int] = None
    checker_raw: str = ""
    reuse_results: typing.List[typing.Dict[str, object]] = dataclasses.field(default_factory=list)
    reuse_valid_count: int = 0


def _result(
    check_id: str,
    status: str,
    reason_code: str,
    message: str,
    evidence_ref: str = "",
) -> typing.Dict[str, object]:
    return models.check_record(check_id, status, reason_code, message, evidence_ref)


def _issues_message(issues: typing.Sequence[str], limit: int = 6) -> str:
    if not issues:
        return ""
    shown = list(issues[:limit])
    if len(issues) > limit:
        shown.append("(+%d more)" % (len(issues) - limit))
    return "; ".join(shown)


def _envelope(bundle: models.Bundle, key: str) -> typing.Tuple[typing.Optional[typing.Dict[str, object]], str]:
    value = bundle.value("inputs", key)
    if not models.is_nonempty_string(value):
        return None, "inputs.%s is not an explicit path" % key
    path = bundle.resolve(str(value))
    return models.read_envelope(path)


def _payload(bundle: models.Bundle, key: str) -> typing.Tuple[typing.Optional[typing.Dict[str, object]], str]:
    envelope, error = _envelope(bundle, key)
    if envelope is None:
        return None, error
    payload = envelope.get("payload")
    return typing.cast(typing.Dict[str, object], payload), ""


# ---------------------------------------------------------------------------
# PF-01 - required fields present and correctly typed
# ---------------------------------------------------------------------------


def check_pf01(ctx: Context) -> typing.Dict[str, object]:
    bundle = ctx.bundle
    document = bundle.document
    issues: typing.List[str] = []
    if document.get("schema_version") != models.SCHEMA_VERSION:
        issues.append("schema_version is not %r" % models.SCHEMA_VERSION)
    unknown = sorted(set(document) - {"schema_version", "subject", "inputs", "declared", "provenance"})
    for key in unknown:
        issues.append("unknown top-level field %r" % key)

    subject = document.get("subject")
    if not isinstance(subject, dict):
        issues.append("subject is missing or not an object")
    else:
        repo = subject.get("repo")
        if not isinstance(repo, dict):
            issues.append("subject.repo is missing or not an object")
        else:
            for key in ("owner", "name"):
                if not models.is_nonempty_string(repo.get(key)):
                    issues.append("subject.repo.%s is missing" % key)
        change_id = subject.get("change_id")
        if not (models.is_nonempty_string(change_id) or models.is_plain_int(change_id)):
            issues.append("subject.change_id must be a non-empty string or an integer")
        candidate = subject.get("candidate")
        if not isinstance(candidate, dict):
            issues.append("subject.candidate is missing or not an object")
        else:
            for key in ("head_sha", "tree_sha", "base_sha"):
                if not models.is_nonempty_string(candidate.get(key)):
                    issues.append("subject.candidate.%s is missing" % key)

    inputs = document.get("inputs")
    if not isinstance(inputs, dict):
        issues.append("inputs is missing or not an object")
    else:
        for key in ("verdict", "freeze", "settlement", "head_history"):
            if not models.is_nonempty_string(inputs.get(key)):
                issues.append("inputs.%s must be an explicit path" % key)
        for key in ("stage_records", "evidence", "reuse_decisions"):
            if not isinstance(inputs.get(key), list):
                issues.append("inputs.%s must be a list" % key)
        if isinstance(inputs.get("stage_records"), list) and len(inputs.get("stage_records")) != 3:
            issues.append("inputs.stage_records must list exactly three B/D/E declaration files")
        triage = inputs.get("triage")
        if not isinstance(triage, dict):
            issues.append("inputs.triage is missing or not an object")
        else:
            for key in ("schema_version", "findings"):
                if key not in triage:
                    issues.append("inputs.triage.%s is missing" % key)
            if not isinstance(triage.get("findings"), list):
                issues.append("inputs.triage.findings must be a list")
            for key in ("open_blocking", "residual_accepted_count"):
                if not models.is_plain_int(triage.get(key)):
                    issues.append("inputs.triage.%s must be an integer" % key)
        gate_status = inputs.get("gate_status")
        if gate_status is not None:
            if not isinstance(gate_status, dict):
                issues.append("inputs.gate_status must be an object when present")
            else:
                for key in ("MG1", "MG2", "MG3", "MG4", "MG5"):
                    if key in gate_status and not models.is_nonempty_string(gate_status.get(key)):
                        issues.append("inputs.gate_status.%s must be a string" % key)

    declared = document.get("declared")
    if not isinstance(declared, dict):
        issues.append("declared is missing or not an object")
    else:
        for key in ("claim", "generated_by", "as_of"):
            if not models.is_nonempty_string(declared.get(key)):
                issues.append("declared.%s is missing" % key)
        if declared.get("claim") not in models.CLAIMS:
            issues.append("declared.claim is not %s" % ", ".join(models.CLAIMS))

    provenance = document.get("provenance")
    if not isinstance(provenance, dict):
        issues.append("provenance is missing or not an object")
    else:
        for key in ("source_ref", "as_of", "producer_role"):
            if not models.is_nonempty_string(provenance.get(key)):
                issues.append("provenance.%s is missing" % key)
        identity = provenance.get("producer_identity_ref")
        if identity is not None and not isinstance(identity, str):
            issues.append("provenance.producer_identity_ref must be a string or null")
        if not models.is_hex64(provenance.get("declared_payload_sha256")):
            issues.append("provenance.declared_payload_sha256 is not a 64-hex digest")
        if not models.is_plain_int(provenance.get("declared_payload_bytes")):
            issues.append("provenance.declared_payload_bytes is not an integer")
        status = provenance.get("status")
        if status is not None and status not in ("UNVERIFIED", "VERIFIED"):
            issues.append("provenance.status must be UNVERIFIED or VERIFIED when present")
        if not issues and models.is_hex64(provenance.get("declared_payload_sha256")):
            if provenance.get("declared_payload_sha256") != models.digest(models.bundle_payload(bundle)):
                issues.append("provenance.declared_payload_sha256 does not match the bundle payload")
            if provenance.get("declared_payload_bytes") != len(models.canonical_bytes(models.bundle_payload(bundle))):
                issues.append("provenance.declared_payload_bytes does not match the bundle payload")

    if issues:
        return _result("PF-01", "FAIL", "PF01_REQUIRED_FIELD", _issues_message(issues), str(bundle.path))
    return _result("PF-01", "PASS", "OK", "bundle fields present, correctly typed and provenance re-hashed", str(bundle.path))


# ---------------------------------------------------------------------------
# PF-02 - references resolve
# ---------------------------------------------------------------------------


def check_pf02(ctx: Context) -> typing.Dict[str, object]:
    bundle = ctx.bundle
    issues: typing.List[str] = []
    subject = bundle.section("subject") or {}
    candidate = subject.get("candidate") if isinstance(subject.get("candidate"), dict) else {}
    candidate_head = str(candidate.get("head_sha") or "")
    for key in ("head_sha", "tree_sha", "base_sha"):
        if not models.is_hex40(candidate.get(key)):
            issues.append("subject.candidate.%s is not 40-hex" % key)

    verdict, error = _payload(bundle, "verdict")
    if verdict is None:
        issues.append(error)
    else:
        if verdict.get("head_sha") != candidate_head:
            issues.append("verdict head does not equal subject.candidate.head_sha")
        repo = subject.get("repo") if isinstance(subject.get("repo"), dict) else {}
        verdict_repo = verdict.get("repo") if isinstance(verdict.get("repo"), dict) else {}
        if repo and verdict_repo and (repo.get("owner"), repo.get("name")) != (
            verdict_repo.get("owner"),
            verdict_repo.get("name"),
        ):
            issues.append("verdict repo does not equal subject.repo")
        change = verdict.get("change") if isinstance(verdict.get("change"), dict) else {}
        if change and subject.get("change_id") is not None:
            if str(change.get("id")) != str(subject.get("change_id")):
                issues.append("verdict change id does not equal subject.change_id")
        freeze, freeze_error = _payload(bundle, "freeze")
        if freeze is None:
            issues.append(freeze_error)
        else:
            for key in ("head_sha", "tree_sha", "base_sha"):
                if freeze.get(key) and freeze.get(key) != candidate.get(key):
                    issues.append("freeze %s does not equal subject.candidate.%s" % (key, key))
            settlement, settlement_error = _payload(bundle, "settlement")
            if settlement is None:
                issues.append(settlement_error)
            elif freeze.get("settlement_ref") and settlement.get("settlement_id") != freeze.get("settlement_ref"):
                issues.append("settlement id does not equal freeze.settlement_ref")
        history, history_error = _payload(bundle, "head_history")
        if history is None:
            issues.append(history_error)
        else:
            heads = history.get("heads")
            if not isinstance(heads, list):
                issues.append("head_history.heads is not a list")
            else:
                sequences = [entry.get("seq") for entry in heads if isinstance(entry, dict)]
                if sequences != list(range(1, len(sequences) + 1)):
                    issues.append("head_history head ordinals are not contiguous from 1")
                if history.get("candidate_head") not in (None, candidate_head):
                    issues.append("head_history.candidate_head does not equal the candidate head")

    stage_values = bundle.value("inputs", "stage_records")
    stages_seen: typing.Dict[str, str] = {}
    record_ids: typing.List[str] = []
    if not isinstance(stage_values, list):
        issues.append("inputs.stage_records is not a list")
    else:
        for value in stage_values:
            if not isinstance(value, str):
                issues.append("inputs.stage_records entry is not a path")
                continue
            envelope, stage_error = models.read_envelope(bundle.resolve(value))
            if envelope is None:
                issues.append(stage_error)
                continue
            payload = typing.cast(typing.Dict[str, object], envelope["payload"])
            stage = payload.get("stage")
            if stage not in ("B", "D", "E"):
                issues.append("stage declaration %s declares no B/D/E stage" % value)
                continue
            if stage in stages_seen:
                issues.append("duplicate stage declaration for %s" % stage)
            stages_seen[str(stage)] = value
            record_id = payload.get("record_id")
            if not models.is_nonempty_string(record_id):
                issues.append("stage declaration %s has no record_id" % value)
            else:
                record_ids.append(str(record_id))
    if sorted(stages_seen) != ["B", "D", "E"]:
        issues.append("stage declarations are not exactly one B, D and E")
    if len(set(record_ids)) != len(record_ids):
        issues.append("stage record ids are not unique")

    triage = bundle.section("inputs", "triage") or {}
    findings = triage.get("findings") if isinstance(triage.get("findings"), list) else []
    finding_ids: typing.List[str] = []
    for row in findings:
        if not isinstance(row, dict):
            issues.append("a triage finding is not an object")
            continue
        finding_id = row.get("finding_id")
        if not models.is_nonempty_string(finding_id):
            issues.append("a triage finding has no finding_id")
        else:
            finding_ids.append(str(finding_id))
    if len(set(finding_ids)) != len(finding_ids):
        issues.append("triage finding ids are not unique")

    evidence = bundle.value("inputs", "evidence")
    evidence_ids: typing.List[str] = []
    if not isinstance(evidence, list):
        issues.append("inputs.evidence is not a list")
        evidence = []
    for entry in evidence:
        if not isinstance(entry, dict):
            issues.append("an evidence entry is not an object")
            continue
        evidence_id = entry.get("evidence_id")
        if not models.is_nonempty_string(evidence_id):
            issues.append("an evidence entry has no evidence_id")
        else:
            evidence_ids.append(str(evidence_id))
    if len(set(evidence_ids)) != len(evidence_ids):
        issues.append("evidence ids are not unique")
    known_evidence = set(evidence_ids)
    for row in findings:
        if isinstance(row, dict) and row.get("evidence_ref") not in (None, "") and str(row.get("evidence_ref")) not in known_evidence:
            issues.append("triage finding %s cites unresolved evidence %s" % (row.get("finding_id"), row.get("evidence_ref")))
    if verdict is not None:
        record = verdict.get("record") if isinstance(verdict.get("record"), dict) else {}
        for entry in record.get("evidence_set") or []:
            if isinstance(entry, dict) and str(entry.get("evidence_id")) not in known_evidence:
                issues.append("verdict evidence_set cites unresolved evidence %s" % entry.get("evidence_id"))

    requirement_catalog = _requirement_ids(ctx.repo_root)
    reuse_values = bundle.value("inputs", "reuse_decisions")
    if isinstance(reuse_values, list):
        for value in reuse_values:
            if not isinstance(value, str):
                issues.append("inputs.reuse_decisions entry is not a path")
                continue
            try:
                record = models.read_json(bundle.resolve(value))
            except models.ModelError as error:
                issues.append(str(error))
                continue
            if not isinstance(record, dict):
                issues.append("reuse record is not an object: %s" % value)
                continue
            if requirement_catalog is not None:
                source = record.get("source") if isinstance(record.get("source"), dict) else {}
                for requirement_id in source.get("requirement_ids") or []:
                    if str(requirement_id) not in requirement_catalog:
                        issues.append("reuse record cites unresolved requirement %s" % requirement_id)

    if issues:
        return _result("PF-02", "FAIL", "PF02_UNRESOLVED_REFERENCE", _issues_message(issues), str(bundle.path))
    return _result("PF-02", "PASS", "OK", "record ids, evidence ids, stage acts and requirement ids resolve", str(bundle.path))


def _requirement_ids(repo_root: Path) -> typing.Optional[typing.Set[str]]:
    try:
        document = models.read_json(repo_root / "docs" / "conformance" / "requirements.v1.json")
    except models.ModelError:
        return None
    requirements = document.get("requirements") if isinstance(document, dict) else None
    if not isinstance(requirements, list):
        return None
    return {
        str(entry.get("requirement_id"))
        for entry in requirements
        if isinstance(entry, dict) and entry.get("requirement_id")
    }


# ---------------------------------------------------------------------------
# PF-03 - status vocabularies
# ---------------------------------------------------------------------------


def check_pf03(ctx: Context) -> typing.Dict[str, object]:
    bundle = ctx.bundle
    issues: typing.List[str] = []
    stage_values = bundle.value("inputs", "stage_records")
    if isinstance(stage_values, list):
        for value in stage_values:
            if not isinstance(value, str):
                continue
            envelope, _ = models.read_envelope(bundle.resolve(value))
            if envelope is None:
                continue
            payload = typing.cast(typing.Dict[str, object], envelope["payload"])
            stage = str(payload.get("stage"))
            verdict = payload.get("verdict")
            allowed = models.STAGE_VERDICTS.get(stage, ())
            if verdict not in allowed:
                issues.append("stage %s verdict %r is not in %s" % (stage, verdict, ", ".join(allowed)))
    triage = bundle.section("inputs", "triage") or {}
    for row in triage.get("findings") or []:
        if not isinstance(row, dict):
            continue
        if row.get("class") not in models.TRIAGE_CLASSES:
            issues.append("triage class %r is not a closed vocabulary value" % row.get("class"))
        if row.get("disposition") not in models.TRIAGE_DISPOSITIONS:
            issues.append("triage disposition %r is not a closed vocabulary value" % row.get("disposition"))
    for entry in bundle.value("inputs", "evidence") or []:
        if not isinstance(entry, dict):
            continue
        if entry.get("result") not in models.EVIDENCE_RESULTS:
            issues.append("evidence result %r is not a closed vocabulary value" % entry.get("result"))
        if entry.get("assurance") not in models.EVIDENCE_ASSURANCES:
            issues.append("evidence assurance %r is not a closed vocabulary value" % entry.get("assurance"))
    gate_status = bundle.section("inputs", "gate_status")
    if gate_status:
        for key, value in sorted(gate_status.items()):
            if value not in models.GATE_STATUSES:
                issues.append("gate status %s=%r is not a closed vocabulary value" % (key, value))
    if issues:
        return _result("PF-03", "FAIL", "PF03_INVALID_STATUS", _issues_message(issues), str(bundle.path))
    return _result("PF-03", "PASS", "OK", "SD/MG/triage/evidence/assurance vocabularies are valid", str(bundle.path))


# ---------------------------------------------------------------------------
# PF-04 - arithmetic
# ---------------------------------------------------------------------------


def check_pf04(ctx: Context) -> typing.Dict[str, object]:
    bundle = ctx.bundle
    issues: typing.List[str] = []
    triage = bundle.section("inputs", "triage") or {}
    findings = triage.get("findings") if isinstance(triage.get("findings"), list) else []
    open_blocking = sum(
        1
        for row in findings
        if isinstance(row, dict) and row.get("class") == "BLOCKING" and row.get("disposition") != "FIXED"
    )
    residual_accepted = sum(
        1
        for row in findings
        if isinstance(row, dict) and row.get("disposition") == "RESIDUAL_ACCEPTED"
    )
    if triage.get("open_blocking") != open_blocking:
        issues.append("triage.open_blocking %r does not equal the re-derived %d" % (triage.get("open_blocking"), open_blocking))
    if triage.get("residual_accepted_count") != residual_accepted:
        issues.append(
            "triage.residual_accepted_count %r does not equal the re-derived %d"
            % (triage.get("residual_accepted_count"), residual_accepted)
        )
    history, _ = _payload(bundle, "head_history")
    verdict, _ = _payload(bundle, "verdict")
    candidate_head = str((bundle.section("subject") or {}).get("candidate", {}).get("head_sha") or "")
    if history is not None and verdict is not None and isinstance(history.get("heads"), list):
        published = [
            entry
            for entry in history["heads"]
            if isinstance(entry, dict) and entry.get("head_sha") != candidate_head
        ]
        review_heads = verdict.get("review_heads") if isinstance(verdict.get("review_heads"), dict) else {}
        if review_heads.get("used") != len(published):
            issues.append(
                "verdict review_heads.used %r does not equal the %d previously published head(s)"
                % (review_heads.get("used"), len(published))
            )
    record = verdict.get("record") if isinstance(verdict, dict) and isinstance(verdict.get("record"), dict) else {}
    evidence = bundle.value("inputs", "evidence")
    evidence_set = record.get("evidence_set") if isinstance(record.get("evidence_set"), list) else []
    if isinstance(evidence, list) and len(evidence) != len(evidence_set):
        issues.append("evidence denominator mismatch: %d supplied, %d in the verdict set" % (len(evidence), len(evidence_set)))
    plan = verdict.get("plan") if isinstance(verdict, dict) and isinstance(verdict.get("plan"), dict) else {}
    revision_count = plan.get("revision_count")
    if revision_count is not None and (not models.is_plain_int(revision_count) or revision_count < 0):
        issues.append("verdict plan.revision_count is not a non-negative integer")
    if issues:
        return _result("PF-04", "FAIL", "PF04_ARITHMETIC_MISMATCH", _issues_message(issues), str(bundle.path))
    return _result("PF-04", "PASS", "OK", "triage, review-head and evidence denominators recompute", str(bundle.path))


# ---------------------------------------------------------------------------
# PF-05 - evidence completeness
# ---------------------------------------------------------------------------


def check_pf05(ctx: Context) -> typing.Dict[str, object]:
    bundle = ctx.bundle
    issues: typing.List[str] = []
    evidence = bundle.value("inputs", "evidence")
    if not isinstance(evidence, list) or not evidence:
        issues.append("inputs.evidence is empty or not a list")
        evidence = []
    for index, entry in enumerate(evidence):
        if not isinstance(entry, dict):
            issues.append("evidence[%d] is not an object" % index)
            continue
        label = "evidence[%d]" % index
        for field in models.EVIDENCE_REQUIRED_FIELDS:
            if field not in entry:
                issues.append("%s is missing %s" % (label, field))
        if not models.is_nonempty_string(entry.get("evidence_id")):
            issues.append("%s.evidence_id is missing" % label)
        if not models.is_nonempty_string(entry.get("kind")):
            issues.append("%s.kind is missing" % label)
        if not models.is_plain_int(entry.get("bytes")) or entry.get("bytes", -1) < 0:
            issues.append("%s.bytes is not a non-negative integer" % label)
        if not models.is_hex64(entry.get("sha256")):
            issues.append("%s.sha256 is not a 64-hex digest" % label)
        if not (models.is_nonempty_string(entry.get("scope")) or models.is_string_list(entry.get("scope"))):
            issues.append("%s.scope is missing" % label)
        if not models.is_hex40(entry.get("source_head")):
            issues.append("%s.source_head is not 40-hex" % label)
        for field in ("method", "environment", "retention", "invalidation"):
            if not models.is_nonempty_string(entry.get(field)):
                issues.append("%s.%s is missing" % (label, field))
        if entry.get("result") == "UNRUN" and not models.is_nonempty_string(entry.get("unrun_reason")):
            issues.append("%s is UNRUN without a named unrun_reason" % label)
        if entry.get("result") == "PASS" and not models.is_nonempty_string(entry.get("evidence_ref")):
            # PASS evidence needs a retrievable reference; the id itself is not proof.
            issues.append("%s is PASS without an evidence_ref" % label)
        if entry.get("assurance") == "VERIFIED" and not models.is_nonempty_string(entry.get("verification_ref")):
            issues.append("%s claims VERIFIED assurance without a verification_ref" % label)
    if issues:
        return _result("PF-05", "FAIL", "PF05_EVIDENCE_INCOMPLETE", _issues_message(issues), str(bundle.path))
    return _result("PF-05", "PASS", "OK", "%d evidence record(s) complete; every UNRUN is named" % len(evidence), str(bundle.path))

# ---------------------------------------------------------------------------
# PF-06 - stale generated records
# ---------------------------------------------------------------------------


def check_pf06(ctx: Context) -> typing.Dict[str, object]:
    bundle = ctx.bundle
    issues: typing.List[str] = []
    store_dir = ctx.repo_root / "docs" / "approvals" / "revision-state"
    manifest_path = store_dir / "manifest.json"
    declared_digest = ""
    store_provenance_status = ""
    if not manifest_path.is_file():
        issues.append("revision-state manifest is absent: %s" % manifest_path)
    else:
        try:
            manifest = models.read_json(manifest_path)
        except models.ModelError as error:
            issues.append(str(error))
            manifest = None
        if isinstance(manifest, dict):
            for volatile in ("generated_at", "as_of", "timestamp"):
                if volatile in manifest:
                    issues.append("manifest carries volatile field %r (deterministic bytes required)" % volatile)
            files = manifest.get("files")
            if not isinstance(files, list):
                issues.append("manifest files[] is missing")
                files = []
            listed: typing.Dict[str, typing.Dict[str, object]] = {}
            for entry in files:
                if not isinstance(entry, dict) or not models.is_nonempty_string(entry.get("path")):
                    issues.append("manifest files[] entry has no path")
                    continue
                listed[str(entry["path"])] = entry
            expected = set()
            for pattern in ("items/*.jsonl", "changes/*.jsonl"):
                expected.update(path.relative_to(store_dir).as_posix() for path in store_dir.glob(pattern))
            if set(listed) != expected:
                missing = sorted(expected - set(listed))
                extra = sorted(set(listed) - expected)
                if missing:
                    issues.append("record file not listed in the manifest: %s" % ", ".join(missing))
                if extra:
                    issues.append("manifest lists a record file that does not exist: %s" % ", ".join(extra))
            for relative_path in sorted(listed):
                entry = listed[relative_path]
                file_path = store_dir / relative_path
                if not file_path.is_file():
                    continue
                raw = file_path.read_bytes()
                if entry.get("bytes") != len(raw):
                    issues.append("manifest bytes mismatch for %s" % relative_path)
                if entry.get("sha256") != models.sha256_bytes(raw):
                    issues.append("manifest sha256 mismatch for %s" % relative_path)
                if entry.get("event_count") != len(raw.splitlines()):
                    issues.append("manifest event_count mismatch for %s" % relative_path)
            digest_value = manifest.get("store_digest")
            if not models.is_hex64(digest_value):
                issues.append("manifest store_digest is not a 64-hex digest")
            else:
                declared_digest = str(digest_value)
            provenance_binding = manifest.get("provenance_binding")
            if not isinstance(provenance_binding, dict):
                store_provenance_status = "ABSENT"
            else:
                store_provenance_status = str(provenance_binding.get("binding_status") or "ABSENT")
        elif manifest is not None:
            issues.append("manifest is not a JSON object")

    checker_digest = ""
    if isinstance(ctx.checker_result, dict):
        checker_digest = str(ctx.checker_result.get("store_digest") or "")
    digest_unverified = False
    if declared_digest and checker_digest:
        if declared_digest != checker_digest:
            issues.append("manifest store_digest does not equal the checker's recomputed store_digest")
    elif declared_digest:
        digest_unverified = True

    binding_path = ctx.repo_root / "docs" / "conformance" / "evidence-binding-v1.json"
    if not binding_path.is_file():
        issues.append("evidence-binding catalog is absent: %s" % binding_path)
    else:
        try:
            binding = models.read_json(binding_path)
        except models.ModelError as error:
            issues.append(str(error))
            binding = None
        if isinstance(binding, dict):
            if binding.get("schema") != "aegis.evidence-binding/1":
                issues.append("evidence-binding schema is not aegis.evidence-binding/1")
            catalog = binding.get("catalog")
            if not isinstance(catalog, dict):
                issues.append("evidence-binding catalog block is missing")
            else:
                catalog_path = ctx.repo_root / str(catalog.get("path"))
                if not catalog_path.is_file():
                    issues.append("evidence-binding catalog path does not resolve: %s" % catalog.get("path"))
                else:
                    raw = catalog_path.read_bytes()
                    if catalog.get("bytes") != len(raw):
                        issues.append("evidence-binding catalog bytes do not match")
                    if catalog.get("sha256") != models.sha256_bytes(raw):
                        issues.append("evidence-binding catalog sha256 does not match")
            requirement_ids = _requirement_ids(ctx.repo_root) or set()
            records = binding.get("records")
            if not isinstance(records, list):
                issues.append("evidence-binding records[] is missing")
                records = []
            binding_ids: typing.List[str] = []
            for entry in records:
                if not isinstance(entry, dict):
                    issues.append("evidence-binding record is not an object")
                    continue
                evidence_id = entry.get("evidence_id")
                if not models.is_nonempty_string(evidence_id):
                    issues.append("evidence-binding record has no evidence_id")
                else:
                    binding_ids.append(str(evidence_id))
                for requirement_id in entry.get("requirement_ids") or []:
                    if str(requirement_id) not in requirement_ids:
                        issues.append("evidence-binding record cites unknown requirement %s" % requirement_id)
                classification = entry.get("classification")
                if classification not in ("EXECUTED", "UNRUN", "PLANNED-UNRUN"):
                    issues.append("evidence-binding classification %r is not a closed vocabulary value" % classification)
                if classification == "EXECUTED":
                    payload_path = binding_path.parent / str(entry.get("stdout_path"))
                    if not entry.get("stdout_path") or not payload_path.is_file():
                        issues.append("EXECUTED binding payload is absent: %s" % entry.get("stdout_path"))
                    else:
                        raw = payload_path.read_bytes()
                        if entry.get("stdout_bytes") != len(raw):
                            issues.append("EXECUTED binding payload bytes do not match: %s" % entry.get("stdout_path"))
                        if entry.get("stdout_sha256") != models.sha256_bytes(raw):
                            issues.append("EXECUTED binding payload sha256 does not match: %s" % entry.get("stdout_path"))
            if len(set(binding_ids)) != len(binding_ids):
                issues.append("evidence-binding evidence ids are not unique")

    if issues:
        return _result("PF-06", "FAIL", "PF06_STALE_GENERATED_RECORD", _issues_message(issues), str(bundle.path))
    if digest_unverified:
        return _result(
            "PF-06",
            "BLOCKED",
            "PF06_STORE_DIGEST_UNVERIFIED",
            "manifest store_digest cannot be reconciled: no checker recomputation is available",
            str(bundle.path),
        )
    if store_provenance_status != "VERIFIED":
        return _result(
            "PF-06",
            "BLOCKED",
            "PF06_STORE_PROVENANCE_UNVERIFIED",
            "revision-state store provenance is %s (T24 unresolved); treated as REQUIRED_INPUT_UNAVAILABLE"
            % (store_provenance_status or "ABSENT"),
            str(bundle.path),
        )
    return _result("PF-06", "PASS", "OK", "manifest files/digest/provenance and the evidence-binding catalog are current", str(bundle.path))


# ---------------------------------------------------------------------------
# PF-07 - merged-checker composition
# ---------------------------------------------------------------------------


def _stage_directory(bundle: models.Bundle) -> typing.Tuple[typing.Optional[Path], str]:
    values = bundle.value("inputs", "stage_records")
    if not isinstance(values, list) or len(values) != 3 or not all(isinstance(item, str) for item in values):
        return None, "inputs.stage_records must list exactly three B/D/E declaration files"
    paths = [bundle.resolve(item) for item in values]
    parents = {path.parent for path in paths}
    if len(parents) != 1:
        return None, "the three stage declarations must share one directory (the checker takes a directory)"
    directory = parents.pop()
    if not directory.is_dir():
        return None, "the stage-records directory does not exist: %s" % directory
    actual = {path.name for path in directory.glob("*.json")}
    listed = {path.name for path in paths}
    if actual != listed:
        return None, "the stage-records directory holds files not listed in the bundle: %s" % ", ".join(sorted(actual ^ listed))
    return directory, ""


def _checker_command(ctx: Context, stage_dir: Path) -> typing.List[str]:
    bundle = ctx.bundle
    command = [
        sys.executable,
        "-P",
        "scripts/aegis_verdict_gate/run.py",
        "check",
        "--repo-root",
        str(ctx.repo_root),
        "--verdict",
        str(bundle.resolve(str(bundle.value("inputs", "verdict")))),
        "--freeze",
        str(bundle.resolve(str(bundle.value("inputs", "freeze")))),
        "--settlement",
        str(bundle.resolve(str(bundle.value("inputs", "settlement")))),
        "--head-history",
        str(bundle.resolve(str(bundle.value("inputs", "head_history")))),
        "--stage-records-dir",
        str(stage_dir),
        "--json",
    ]
    candidate_head = str((bundle.section("subject") or {}).get("candidate", {}).get("head_sha") or "")
    if models.is_hex40(candidate_head):
        command.extend(["--candidate-head", candidate_head])
    if ctx.fixture_mode:
        command.append("--fixture-mode")
        for method in ctx.supported_auth_methods:
            command.extend(["--supported-auth-method", method])
    return command


def _run(
    command: typing.Sequence[str],
    *,
    cwd: Path,
    input_text: typing.Optional[str] = None,
    timeout: int = 180,
) -> typing.Tuple[int, str, str]:
    completed = subprocess.run(
        list(command),
        cwd=str(cwd),
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        input=input_text,
        timeout=timeout,
        check=False,
    )
    return completed.returncode, completed.stdout, completed.stderr


def check_pf07(
    ctx: Context,
    runner: typing.Optional[typing.Callable[[typing.Sequence[str], Path], typing.Tuple[int, str, str]]] = None,
) -> typing.Dict[str, object]:
    bundle = ctx.bundle
    stage_dir, stage_error = _stage_directory(bundle)
    required = {}
    for key in ("verdict", "freeze", "settlement", "head_history"):
        value = bundle.value("inputs", key)
        path = bundle.resolve(str(value)) if isinstance(value, str) else None
        if path is None or not path.is_file():
            return _result(
                "PF-07",
                "BLOCKED",
                "PF07_REQUIRED_INPUT_UNAVAILABLE",
                "checker input %s is absent or not a file" % key,
                str(bundle.path),
            )
        required[key] = path
    if stage_dir is None:
        return _result("PF-07", "FAIL", "PF07_STAGE_RECORDS_INVALID", stage_error, str(bundle.path))

    command = _checker_command(ctx, stage_dir)
    try:
        exit_code, stdout, stderr = (runner or (lambda cmd, cwd: _run(cmd, cwd=cwd)))(command, ctx.code_root)
    except (OSError, subprocess.SubprocessError) as error:
        return _result("PF-07", "FAIL", "PF07_CHECKER_NOT_RUNNABLE", "the merged checker could not be run: %s" % error, str(bundle.path))
    ctx.checker_exit = exit_code
    ctx.checker_raw = stdout
    try:
        result = json.loads(stdout)
    except ValueError:
        detail = (stderr or stdout).strip().splitlines()
        return _result(
            "PF-07",
            "FAIL",
            "PF07_CHECKER_OUTPUT_UNPARSEABLE",
            "the merged checker returned no parseable JSON (exit %d): %s" % (exit_code, detail[-1] if detail else ""),
            str(bundle.path),
        )
    if not isinstance(result, dict) or result.get("schema_version") != "aegis.verdict-gate-output/v1":
        return _result("PF-07", "FAIL", "PF07_CHECKER_OUTPUT_INVALID", "checker output schema is not aegis.verdict-gate-output/v1", str(bundle.path))
    ctx.checker_result = result

    if exit_code == 2:
        return _result("PF-07", "FAIL", "PF07_CHECKER_INVALID_INPUT", "the merged checker rejected an input (exit 2)", str(bundle.path))
    if exit_code == 3:
        return _result("PF-07", "FAIL", "PF07_CHECKER_INTERNAL_ERROR", "the merged checker reported an internal error (exit 3)", str(bundle.path))
    if exit_code not in (0, 1):
        return _result("PF-07", "FAIL", "PF07_CHECKER_UNEXPECTED_EXIT", "unexpected checker exit code %d" % exit_code, str(bundle.path))

    assurance = result.get("assurance") if isinstance(result.get("assurance"), dict) else {}
    if assurance.get("claim") != "AUDITABLE" or assurance.get("mounted_coverage") != "UNKNOWN":
        return _result("PF-07", "FAIL", "PF07_ASSURANCE_MISMATCH", "the checker did not report AUDITABLE/UNKNOWN assurance", str(bundle.path))

    readiness = result.get("readiness") is True
    mode = assurance.get("mode")
    if readiness and mode != "FIXTURE":
        return _result("PF-07", "FAIL", "PF07_FALSE_PRODUCTION_READINESS", "a production checker run reported readiness true", str(bundle.path))

    reported = result.get("inputs_sha256") if isinstance(result.get("inputs_sha256"), dict) else {}
    mismatches: typing.List[str] = []
    missing: typing.List[str] = []
    for key, path in required.items():
        entry = reported.get(key)
        actual_bytes, actual_sha = models.file_report(path)
        if not isinstance(entry, dict):
            missing.append(key)
            continue
        if entry.get("bytes") != actual_bytes or entry.get("sha256") != actual_sha:
            mismatches.append(key)
    if mismatches:
        return _result(
            "PF-07",
            "FAIL",
            "PF07_INPUT_HASH_MISMATCH",
            "the checker consumed different bytes than the bundle declares: %s" % ", ".join(mismatches),
            str(bundle.path),
        )
    if exit_code == 0 and missing:
        return _result(
            "PF-07",
            "FAIL",
            "PF07_CHECKER_OUTPUT_INCOMPLETE",
            "the checker reported readiness without reporting input hashes: %s" % ", ".join(missing),
            str(bundle.path),
        )

    reason_codes = [str(code) for code in result.get("reason_codes") or [] if isinstance(code, str)]
    if exit_code == 0 and readiness:
        return _result(
            "PF-07",
            "PASS",
            "OK",
            "merged checker ready in fixture mode; input hashes reconciled (%d input(s), %d previously published head(s))"
            % (len(required), (result.get("derived_counts") or {}).get("review_heads_used", 0)),
            str(bundle.path),
        )
    if exit_code == 0 and not readiness:
        return _result("PF-07", "FAIL", "PF07_CHECKER_INCONSISTENT", "exit 0 did not carry readiness true", str(bundle.path))
    summary = ", ".join(reason_codes[:8]) if reason_codes else "no reason code"
    if missing:
        summary += "; checker stopped before consuming %s" % ", ".join(missing)
    return _result(
        "PF-07",
        "BLOCKED",
        "PF07_CHECKER_BLOCKED",
        "merged checker blocked (exit 1): %s" % summary,
        str(bundle.path),
    )


# ---------------------------------------------------------------------------
# PF-08 - evidence-reuse composition
# ---------------------------------------------------------------------------


def check_pf08(ctx: Context) -> typing.Dict[str, object]:
    bundle = ctx.bundle
    values = bundle.value("inputs", "reuse_decisions")
    if not isinstance(values, list):
        return _result("PF-08", "FAIL", "PF08_INPUT_INVALID", "inputs.reuse_decisions is not a list", str(bundle.path))
    if not values:
        return _result("PF-08", "PASS", "OK", "no reuse decisions were supplied; nothing to reuse", str(bundle.path))
    candidate_head = str((bundle.section("subject") or {}).get("candidate", {}).get("head_sha") or "")
    if not models.is_hex40(candidate_head):
        return _result("PF-08", "BLOCKED", "PF08_TARGET_UNAVAILABLE", "no candidate head is available to bind the reuse decisions", str(bundle.path))
    evidence = bundle.value("inputs", "evidence")
    if not isinstance(evidence, list):
        evidence = []
    evidence_set = [
        {
            "evidence_id": entry.get("evidence_id"),
            "sha256": entry.get("sha256"),
            "head": entry.get("source_head") or entry.get("head"),
            "kind": entry.get("kind"),
        }
        for entry in evidence
        if isinstance(entry, dict)
    ]
    change_id = (bundle.section("subject") or {}).get("change_id")
    problems: typing.List[str] = []
    blocked: typing.List[str] = []
    for value in values:
        if not isinstance(value, str):
            problems.append("a reuse decision entry is not a path")
            continue
        path = bundle.resolve(value)
        command = [
            sys.executable,
            "-m",
            "tools.aegis_evidence_reuse",
            "validate",
            "--record",
            str(path),
            "--target-head",
            candidate_head,
            "--evidence",
            "-",
            "--json",
        ]
        if change_id is not None:
            command.extend(["--change-id", str(change_id)])
        try:
            exit_code, stdout, _ = _run(command, cwd=ctx.code_root, input_text=json.dumps(evidence_set, sort_keys=True))
        except (OSError, subprocess.SubprocessError) as error:
            problems.append("reuse validator could not be run for %s: %s" % (value, error))
            continue
        try:
            result = json.loads(stdout)
        except ValueError:
            problems.append("reuse validator returned no parseable JSON for %s" % value)
            continue
        if not isinstance(result, dict) or result.get("schema_version") != "aegis.evidence-reuse-validation/v1":
            problems.append("reuse validator output schema is invalid for %s" % value)
            continue
        ctx.reuse_results.append(result)
        if exit_code == 0 and result.get("valid") is True and result.get("effective_decision") == "VALID":
            ctx.reuse_valid_count += 1
        elif exit_code == 1:
            codes = sorted(
                {
                    str(item.get("code"))
                    for item in result.get("violations") or []
                    if isinstance(item, dict) and item.get("code")
                }
            )
            blocked.append("%s: %s" % (value, ", ".join(codes) if codes else str(result.get("effective_decision"))))
        else:
            problems.append("reuse validator exited %d for %s" % (exit_code, value))
    if problems:
        return _result("PF-08", "FAIL", "PF08_VALIDATOR_ERROR", _issues_message(problems), str(bundle.path))
    if blocked:
        return _result("PF-08", "BLOCKED", "PF08_REUSE_NOT_VALID", _issues_message(blocked), str(bundle.path))
    return _result("PF-08", "PASS", "OK", "%d reuse decision(s) validated VALID at the candidate head" % ctx.reuse_valid_count, str(bundle.path))


# ---------------------------------------------------------------------------
# PF-09 - truthfulness
# ---------------------------------------------------------------------------


def check_pf09(ctx: Context) -> typing.Dict[str, object]:
    bundle = ctx.bundle
    issues: typing.List[str] = []
    if bundle.value("declared", "claim") not in models.CLAIMS:
        issues.append("declared.claim is not a mechanical-checks-only claim")
    verdict, _ = _payload(bundle, "verdict")
    record = verdict.get("record") if isinstance(verdict, dict) and isinstance(verdict.get("record"), dict) else {}
    for entry in record.get("bypasses") or []:
        if not isinstance(entry, dict):
            issues.append("a bypass entry is not an object")
            continue
        if entry.get("displayed_as") != "BYPASS":
            issues.append("bypass %r is not displayed as a bypass" % entry.get("bypass_id"))
        if str(entry.get("status", "")).upper() in ("GREEN", "PASS"):
            issues.append("bypass %r is displayed green or passing" % entry.get("bypass_id"))
    reuse = record.get("evidence_reuse")
    if isinstance(reuse, dict):
        if reuse.get("copies_pass") is True:
            issues.append("the verdict record claims a copied PASS")
        if reuse.get("decision") == "VALID" and ctx.reuse_valid_count == 0:
            issues.append("the verdict claims VALID evidence reuse with no validated reuse record")
    for entry in bundle.value("inputs", "evidence") or []:
        if isinstance(entry, dict) and entry.get("result") == "UNRUN" and not models.is_nonempty_string(entry.get("unrun_reason")):
            issues.append("an UNRUN evidence record is not named with an unrun_reason")
    if ctx.checker_result is not None:
        assurance = ctx.checker_result.get("assurance") if isinstance(ctx.checker_result.get("assurance"), dict) else {}
        if assurance.get("claim") != "AUDITABLE":
            issues.append("the checker's assurance claim is not AUDITABLE")
        if ctx.checker_result.get("readiness") is True and assurance.get("mode") != "FIXTURE":
            issues.append("a production readiness=true was accepted as verified")
    triage = bundle.section("inputs", "triage") or {}
    for row in triage.get("findings") or []:
        if isinstance(row, dict) and row.get("class") == "BLOCKING" and row.get("disposition") != "FIXED":
            issues.append("blocking finding %s is not fixed" % row.get("finding_id"))
    provenance = bundle.section("provenance") or {}
    if provenance.get("status") == "VERIFIED" and not provenance.get("producer_identity_ref"):
        issues.append("a VERIFIED provenance status is claimed without a producer identity")
    if issues:
        return _result("PF-09", "FAIL", "PF09_UNTRUTHFUL_OUTPUT", _issues_message(issues), str(bundle.path))
    return _result("PF-09", "PASS", "OK", "bypasses are bypasses, UNRUN is named and no aggregate green is claimed", str(bundle.path))


# ---------------------------------------------------------------------------
# PF-10 - determinism / read-only / offline self-audit
# ---------------------------------------------------------------------------


def scan_source(root: Path) -> typing.List[str]:
    """Statically scan production Python sources for network/write behaviour."""

    issues: typing.List[str] = []
    for path in sorted(root.rglob("*.py")):
        if "tests" in path.parts:
            continue
        try:
            tree = ast.parse(path.read_text(encoding="utf-8"))
        except (OSError, SyntaxError) as error:
            issues.append("cannot parse %s: %s" % (path, error))
            continue
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    if alias.name.split(".")[0] in FORBIDDEN_NETWORK_MODULES:
                        issues.append("network import %s in %s" % (alias.name, path.name))
            elif isinstance(node, ast.ImportFrom):
                module = (node.module or "").split(".")[0]
                if module in FORBIDDEN_NETWORK_MODULES:
                    issues.append("network import %s in %s" % (node.module, path.name))
            elif isinstance(node, ast.Call):
                name = _dotted_name(node.func)
                if name in FORBIDDEN_WRITE_CALLS:
                    issues.append("write/execute call %s in %s" % (name, path.name))
                elif name == "open" and len(node.args) >= 2 and isinstance(node.args[1], ast.Constant):
                    mode = str(node.args[1].value)
                    if any(character in mode for character in "wax+"):
                        issues.append("file opened for writing in %s" % path.name)
                elif name.startswith("subprocess.") or name == "subprocess.run":
                    for keyword in node.keywords:
                        if keyword.arg == "shell" and isinstance(keyword.value, ast.Constant) and keyword.value.value is True:
                            issues.append("subprocess shell=True in %s" % path.name)
                elif isinstance(node.func, ast.Attribute) and node.func.attr in FORBIDDEN_WRITE_METHODS:
                    issues.append("filesystem write method .%s in %s" % (node.func.attr, path.name))
    return issues


def _dotted_name(node: ast.AST) -> str:
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        prefix = _dotted_name(node.value)
        return "%s.%s" % (prefix, node.attr) if prefix else node.attr
    return ""


def check_pf10(ctx: Context, source_root: typing.Optional[Path] = None) -> typing.Dict[str, object]:
    issues: typing.List[str] = []
    first = models.canonical_bytes(ctx.bundle.document)
    second = models.canonical_bytes(ctx.bundle.document)
    if first != second:
        issues.append("canonical serialization is not byte-identical across two runs")
    if models.SUBPROCESS_MODULES != ("scripts/aegis_verdict_gate/run.py", "tools.aegis_evidence_reuse"):
        issues.append("the subprocess allowlist is not exactly the merged checker and the reuse validator")
    if models.GIT_SUBCOMMANDS != ("rev-parse", "cat-file", "log", "merge-base"):
        issues.append("the git allowlist is not the read-only plumbing set")
    scan_root = source_root if source_root is not None else Path(__file__).resolve().parent
    issues.extend(scan_source(scan_root))
    if issues:
        return _result("PF-10", "FAIL", "PF10_SELF_AUDIT_FAILED", _issues_message(issues), str(scan_root))
    return _result("PF-10", "PASS", "OK", "deterministic encoding; no network or write path in the production sources", str(scan_root))


# ---------------------------------------------------------------------------
# Runner
# ---------------------------------------------------------------------------


def run_all(
    bundle: models.Bundle,
    repo_root: Path,
    *,
    fixture_mode: bool = False,
    code_root: typing.Optional[Path] = None,
    supported_auth_methods: typing.Sequence[str] = (),
    checker_runner: typing.Optional[typing.Callable[[typing.Sequence[str], Path], typing.Tuple[int, str, str]]] = None,
    source_root: typing.Optional[Path] = None,
) -> typing.List[typing.Dict[str, object]]:
    context = Context(
        bundle=bundle,
        repo_root=Path(repo_root).resolve(),
        fixture_mode=fixture_mode,
        code_root=(code_root or Path(__file__).resolve().parents[2]).resolve(),
        supported_auth_methods=supported_auth_methods,
    )
    results = [
        check_pf01(context),
        check_pf02(context),
        check_pf03(context),
        check_pf04(context),
        check_pf05(context),
        check_pf07(context, runner=checker_runner),
        check_pf06(context),
        check_pf08(context),
        check_pf09(context),
        check_pf10(context, source_root=source_root),
    ]
    by_id = {str(item["check_id"]): item for item in results}
    return [by_id[check_id] for check_id in models.CHECK_IDS]


def self_test() -> typing.Dict[str, object]:
    model_report = models.self_test()
    source_report = scan_source(Path(__file__).resolve().parent)
    return {
        "ok": bool(model_report["ok"]) and not source_report,
        "schema_version": models.SCHEMA_VERSION,
        "check_ids": list(models.CHECK_IDS),
        "canonical_sample_sha256": model_report["canonical_sample_sha256"],
        "source_scan_findings": source_report,
    }
