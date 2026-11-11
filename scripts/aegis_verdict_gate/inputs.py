"""Readers, validators and derivations for the required gate inputs.

Every required input is a JSON envelope:

    {"payload": {...record content...},
     "provenance": {"source_ref", "as_of", "producer_role",
                    "producer_identity_ref", "declared_payload_sha256",
                    "declared_payload_bytes", "status"?}}

The declared payload hash covers the canonical serialization of the payload,
so the binding is not circular and the checker can always re-derive it.  The
checker re-hashes every file and reports file bytes/sha256 in inputs_sha256;
a declared hash is never trusted when the file can be re-hashed.

No predicate term defaults to true.  An absent, unparseable, tampered or
unverifiable input becomes a fail-closed finding (REQUIRED_INPUT_UNAVAILABLE
or a more specific contract code); absence is never read as valid, settled or
frozen.  No network, no provider SDK, standard library only.
"""

from __future__ import annotations

import dataclasses
import json
import typing
from pathlib import Path

from . import canonical, catalogue
from .records import Issue

CODE_CANONICAL = "CANONICAL_FIELD_MISSING_OR_MISMATCH"
CODE_REQUIRED_INPUT = "REQUIRED_INPUT_UNAVAILABLE"
CODE_STAGE_VERDICT = "STAGE_VERDICT_NOT_ACCEPTED"
CODE_MISSING_REVIEW = "MISSING_REQUIRED_REVIEW_OR_DISPOSITION"
CODE_HEAD_MOVED = "HEAD_MOVED_OR_BASE_INVALIDATED"

PRE_AUDIT_STATES = ("pass", "fail", "neutral", "unrun", "bypassed")
REVIEW_SOURCE_STATES = ("SETTLED", "PENDING", "UNAVAILABLE_DISPOSITIONED")
STAGE_VERDICT_VOCABULARY = {"B": ("ACCEPT", "REVISE"), "D": ("ACCEPT", "REVISE"), "E": ("PASS", "FAIL")}
AFFIRMATIVE_STAGE = {"B": "ACCEPT", "D": "ACCEPT", "E": "PASS"}
INPUT_STATUSES = ("VERIFIED", "UNVERIFIED", "ABSENT")

# The verified authority record a real unavailable-review disposition needs.
# The disposition authority (owner decision T7) is undefined, so v1 can only
# honour a disposition whose authority record is present, closed-schema,
# ACTIVE, and scoped to this exact change/head/merge target.  Anything else -
# including arbitrary strings in the settlement payload - is blocked.
DISPOSITION_AUTHORITY_SCHEMA = "aegis.disposition-authority/v1"
DISPOSITION_DECISION = "UNAVAILABLE_REVIEW"
DISPOSITION_SCOPE_FIELDS = ("repo", "change_id", "head_sha", "merge_target_ref")


class InputError(ValueError):
    """The input file itself is unusable (missing, unparseable, wrong shape).

    fatal is true when the file cannot be parsed at all (usage/parse failure,
    exit code 2); a merely absent input is a gate condition (exit code 1).
    """

    def __init__(self, code: str, detail: str, fatal: bool = False) -> None:
        super().__init__(detail)
        self.code = code
        self.detail = detail
        self.fatal = fatal


@dataclasses.dataclass
class Envelope:
    path: str
    payload: typing.Dict[str, object]
    file_bytes: int
    file_sha256: str
    provenance: typing.Dict[str, object]
    issues: typing.List[Issue]

    def report(self) -> typing.Dict[str, object]:
        return {
            "path": self.path,
            "bytes": self.file_bytes,
            "sha256": self.file_sha256,
            "source_ref": self.provenance.get("source_ref"),
            "as_of": self.provenance.get("as_of"),
            "producer_role": self.provenance.get("producer_role"),
        }


@dataclasses.dataclass
class FreezeResult:
    present: bool
    valid: bool
    immutable_inputs_sha256: str
    issues: typing.List[Issue]

    @property
    def code(self) -> str:
        for issue in self.issues:
            if issue.code == CODE_HEAD_MOVED:
                return CODE_HEAD_MOVED
        return CODE_REQUIRED_INPUT


@dataclasses.dataclass
class SettlementResult:
    present: bool
    settled: bool
    issues: typing.List[Issue]


@dataclasses.dataclass
class StageResult:
    present_by_stage: typing.Dict[str, typing.Dict[str, object]]
    issues: typing.List[Issue]


@dataclasses.dataclass
class HeadHistory:
    present: bool
    status: str
    heads: typing.List[typing.Dict[str, object]]
    issues: typing.List[Issue]


def load_envelope(path: typing.Union[str, Path], require_provenance: bool = True) -> Envelope:
    """Load one input envelope and validate its provenance binding."""

    file_path = Path(path)
    issues: typing.List[Issue] = []
    if not file_path.is_file():
        raise InputError(CODE_REQUIRED_INPUT, "required input is absent: %s" % file_path)
    raw = file_path.read_bytes()
    try:
        document = json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, ValueError) as error:
        raise InputError(CODE_CANONICAL, "input is not valid UTF-8 JSON: %s (%s)" % (file_path, error), fatal=True)
    if not isinstance(document, dict) or not isinstance(document.get("payload"), dict):
        raise InputError(CODE_CANONICAL, "input envelope has no payload object: %s" % file_path, fatal=True)
    payload = typing.cast(typing.Dict[str, object], document["payload"])
    provenance = document.get("provenance")
    if not isinstance(provenance, dict):
        if require_provenance:
            issues.append(Issue(CODE_REQUIRED_INPUT, "input has no provenance block: %s" % file_path))
        provenance = {}
    if require_provenance:
        for key, expected in (
            ("source_ref", str),
            ("as_of", str),
            ("producer_role", str),
            ("declared_payload_sha256", str),
            ("declared_payload_bytes", int),
        ):
            value = provenance.get(key)
            if not isinstance(value, expected) or (expected is str and not value):
                issues.append(Issue(CODE_REQUIRED_INPUT, "provenance.%s is missing or invalid: %s" % (key, file_path)))
        declared_sha = provenance.get("declared_payload_sha256")
        declared_bytes = provenance.get("declared_payload_bytes")
        recomputed_sha = canonical.digest(payload)
        recomputed_bytes = len(canonical.canonical_bytes(payload))
        if isinstance(declared_sha, str) and declared_sha != recomputed_sha:
            issues.append(
                Issue(CODE_CANONICAL, "declared payload hash does not match the payload: %s" % file_path)
            )
        if isinstance(declared_bytes, int) and declared_bytes != recomputed_bytes:
            issues.append(
                Issue(CODE_CANONICAL, "declared payload bytes do not match the payload: %s" % file_path)
            )
    return Envelope(
        path=str(file_path),
        payload=payload,
        file_bytes=len(raw),
        file_sha256=canonical.sha256_hex(raw),
        provenance=provenance,
        issues=issues,
    )


def _require(payload: typing.Mapping[str, object], key: str, kind: type) -> typing.Tuple[bool, object]:
    value = payload.get(key)
    if not isinstance(value, kind) or (kind is str and not value):
        return (False, None)
    return (True, value)


def derive_freeze(freeze: Envelope, verdict: typing.Mapping[str, object]) -> FreezeResult:
    """Derive freeze.valid from the freeze record (never defaulted true)."""

    payload = freeze.payload
    issues: typing.List[Issue] = list(freeze.issues)
    for key, kind in (
        ("freeze_id", str),
        ("candidate_id", str),
        ("head_sha", str),
        ("tree_sha", str),
        ("base_sha", str),
        ("frozen_at", str),
        ("immutable_inputs_sha256", str),
        ("settlement_ref", str),
    ):
        ok, _ = _require(payload, key, kind)
        if not ok:
            issues.append(Issue(CODE_REQUIRED_INPUT, "freeze.%s is missing or invalid" % key))
    if payload.get("valid") is False:
        issues.append(Issue(CODE_REQUIRED_INPUT, "freeze record declares valid=false"))
    policy_sha = verdict.get("policy_sha256")
    plan = verdict.get("plan") if isinstance(verdict.get("plan"), dict) else {}
    plan_sha = plan.get("sha256")
    evidence_sha = verdict.get("evidence_inputs_sha256")
    recomputed = canonical.digest(
        {
            "head": payload.get("head_sha"),
            "tree": payload.get("tree_sha"),
            "base": payload.get("base_sha"),
            "policy_sha256": policy_sha,
            "plan_sha256": plan_sha,
            "evidence_inputs_sha256": evidence_sha,
        }
    )
    declared = payload.get("immutable_inputs_sha256")
    if declared != recomputed:
        issues.append(
            Issue(CODE_REQUIRED_INPUT, "freeze.immutable_inputs_sha256 does not recompute")
        )
    for key, verdict_key in (("head_sha", "head_sha"), ("tree_sha", "tree_sha"), ("base_sha", "base_sha")):
        if payload.get(key) != verdict.get(verdict_key):
            issues.append(
                Issue(CODE_HEAD_MOVED, "freeze.%s does not equal the verdict %s" % (key, verdict_key))
            )
    if payload.get("candidate_id") != verdict.get("candidate_id"):
        issues.append(Issue(CODE_REQUIRED_INPUT, "freeze.candidate_id does not equal VB-A07"))
    mutations = payload.get("mutation_events")
    if not isinstance(mutations, list):
        issues.append(Issue(CODE_REQUIRED_INPUT, "freeze.mutation_events is missing"))
    elif mutations:
        issues.append(Issue(CODE_HEAD_MOVED, "freeze.mutation_events is not empty after frozen_at"))
    return FreezeResult(
        present=True,
        valid=not issues,
        immutable_inputs_sha256=recomputed,
        issues=issues,
    )


def _disposition_scope_matches(scope: typing.Any, verdict: typing.Mapping[str, object]) -> bool:
    if not isinstance(scope, dict):
        return False
    change = verdict.get("change") if isinstance(verdict.get("change"), dict) else {}
    expected = {
        "repo": "%s/%s" % (verdict.get("repo", {}).get("owner"), verdict.get("repo", {}).get("name"))
        if isinstance(verdict.get("repo"), dict)
        else "",
        "change_id": change.get("id"),
        "head_sha": verdict.get("head_sha"),
        "merge_target_ref": verdict.get("merge_target", {}).get("ref")
        if isinstance(verdict.get("merge_target"), dict)
        else "",
    }
    for key in DISPOSITION_SCOPE_FIELDS:
        if str(scope.get(key, "")) != str(expected[key]):
            return False
    return True


def verify_disposition_authority(
    repo_root: typing.Optional[Path],
    verdict: typing.Optional[typing.Mapping[str, object]],
    source: typing.Mapping[str, object],
) -> typing.Tuple[bool, str]:
    """Verify a policy-authorised unavailable-review disposition.

    Returns (ok, detail).  ok is true only when the cited authority record is
    present in the repository at the cited sha256, is a closed-schema
    disposition authority, is ACTIVE, decides UNAVAILABLE_REVIEW, is not
    time-bounded (an offline checker cannot evaluate an expiry), and covers
    this exact repo/change/head/merge target.  A truthy string is never enough.
    """

    authority = source.get("disposition_authority_ref")
    if not isinstance(authority, str) or not authority:
        return (False, "no disposition authority is cited")
    if verdict is None or repo_root is None:
        return (False, "the disposition authority cannot be resolved without the evaluated change")
    declared_sha = source.get("disposition_authority_sha256")
    if not isinstance(declared_sha, str) or len(declared_sha) != 64 or set(declared_sha) - set("0123456789abcdef"):
        return (False, "the disposition authority cites no 64-hex sha256")
    scope = source.get("disposition_scope")
    if not _disposition_scope_matches(scope, verdict):
        return (False, "the disposition scope does not cover this repo/change/head/merge target")
    if source.get("expires") not in (None, ""):
        return (False, "a time-bounded disposition authority cannot be evaluated offline (status must govern)")
    path = (Path(repo_root) / authority).resolve()
    try:
        path.relative_to(Path(repo_root).resolve())
    except ValueError:
        return (False, "the disposition authority path escapes the repository")
    if not path.is_file():
        return (False, "the disposition authority record is absent: %s" % authority)
    raw = path.read_bytes()
    if canonical.sha256_hex(raw) != declared_sha:
        return (False, "the disposition authority bytes do not match the cited sha256")
    try:
        document = json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, ValueError):
        return (False, "the disposition authority is not UTF-8 JSON")
    if not isinstance(document, dict):
        return (False, "the disposition authority is not a JSON object")
    if document.get("schema_version") != DISPOSITION_AUTHORITY_SCHEMA:
        return (False, "the disposition authority does not declare schema %s" % DISPOSITION_AUTHORITY_SCHEMA)
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
    if not _disposition_scope_matches(document.get("scope"), verdict):
        return (False, "the disposition authority's own scope does not cover this change")
    return (True, "disposition authority %s resolves ACTIVE at the cited sha256" % authority)


def derive_settlement(
    settlement: Envelope,
    verdict: typing.Optional[typing.Mapping[str, object]] = None,
    repo_root: typing.Optional[Path] = None,
) -> SettlementResult:
    """Re-derive settlement.settled from checks and review sources."""

    payload = settlement.payload
    issues: typing.List[Issue] = list(settlement.issues)
    checks = payload.get("pre_audit_checks")
    if not isinstance(checks, list):
        issues.append(Issue(CODE_REQUIRED_INPUT, "settlement.pre_audit_checks is missing"))
        checks = []
    for check in checks:
        if not isinstance(check, dict):
            issues.append(Issue(CODE_CANONICAL, "settlement pre-audit check is not an object"))
            continue
        if not check.get("check_id"):
            issues.append(Issue(CODE_CANONICAL, "settlement pre-audit check has no check_id"))
        if check.get("state") not in PRE_AUDIT_STATES:
            issues.append(
                Issue(CODE_CANONICAL, "settlement pre-audit check %r has no recorded outcome" % check.get("check_id"))
            )
        if not check.get("evidence_ref"):
            issues.append(Issue(CODE_CANONICAL, "settlement pre-audit check %r has no evidence_ref" % check.get("check_id")))
    sources = payload.get("review_sources")
    if not isinstance(sources, list):
        issues.append(Issue(CODE_REQUIRED_INPUT, "settlement.review_sources is missing"))
        sources = []
    derived_settled = True
    for source in sources:
        if not isinstance(source, dict):
            issues.append(Issue(CODE_CANONICAL, "settlement review source is not an object"))
            derived_settled = False
            continue
        state = source.get("state")
        if state == "PENDING":
            derived_settled = False
            issues.append(
                Issue(CODE_MISSING_REVIEW, "review source %r is PENDING (not settled)" % source.get("source_id"))
            )
        elif state == "UNAVAILABLE_DISPOSITIONED":
            verified, detail = verify_disposition_authority(repo_root, verdict, source)
            if not verified:
                derived_settled = False
                issues.append(
                    Issue(
                        CODE_MISSING_REVIEW,
                        "review source %r has no policy-authorised unavailable disposition: %s"
                        % (source.get("source_id"), detail),
                    )
                )
        elif state != "SETTLED":
            derived_settled = False
            issues.append(
                Issue(CODE_CANONICAL, "review source %r has an invalid state %r" % (source.get("source_id"), state))
            )
    if issues and derived_settled:
        derived_settled = False
    declared = payload.get("settled")
    if not isinstance(declared, bool):
        issues.append(Issue(CODE_REQUIRED_INPUT, "settlement.settled is missing"))
    elif declared != derived_settled:
        derived_settled = False
        issues.append(
            Issue(CODE_CANONICAL, "declared settlement.settled disagrees with the re-derivation")
        )
    return SettlementResult(present=True, settled=derived_settled, issues=issues)


def validate_stage_records(
    repo_root: Path,
    stage_records: typing.Any,
    candidate_head: str,
    plan_audit_applies: bool,
) -> StageResult:
    """Re-hash and validate the supplied B/D/E stage records."""

    issues: typing.List[Issue] = []
    by_stage: typing.Dict[str, typing.Dict[str, object]] = {}
    if not isinstance(stage_records, list):
        return StageResult(
            present_by_stage=by_stage,
            issues=[Issue(CODE_REQUIRED_INPUT, "VB-D01 stage_records is not a list")],
        )
    for record in stage_records:
        if not isinstance(record, dict):
            issues.append(Issue(CODE_CANONICAL, "stage record is not an object"))
            continue
        stage = str(record.get("stage", ""))
        if stage not in STAGE_VERDICT_VOCABULARY:
            issues.append(Issue(CODE_CANONICAL, "stage record has an unknown stage %r" % stage))
            continue
        if stage in by_stage:
            issues.append(Issue(CODE_CANONICAL, "more than one %s stage record is bound" % stage))
            continue
        by_stage[stage] = record
        record_path = record.get("record_path")
        if not isinstance(record_path, str) or not record_path:
            issues.append(Issue(CODE_REQUIRED_INPUT, "%s stage record has no record_path" % stage))
            continue
        path = (Path(repo_root) / record_path).resolve()
        try:
            path.relative_to(Path(repo_root).resolve())
        except ValueError:
            issues.append(Issue(CODE_CANONICAL, "%s stage record path escapes the repository" % stage))
            continue
        if not path.is_file():
            issues.append(Issue(CODE_REQUIRED_INPUT, "%s stage record file is absent: %s" % (stage, record_path)))
            continue
        raw = path.read_bytes()
        if record.get("bytes") != len(raw):
            issues.append(Issue(CODE_CANONICAL, "%s stage record bytes do not recompute" % stage))
        if record.get("sha256") != canonical.sha256_hex(raw):
            issues.append(Issue(CODE_CANONICAL, "%s stage record sha256 does not recompute" % stage))
        if record.get("head_sha") != candidate_head:
            issues.append(Issue(CODE_STAGE_VERDICT, "%s stage record is not bound to the frozen head" % stage))
        if record.get("independence_class") != "INDEPENDENT":
            issues.append(Issue(CODE_STAGE_VERDICT, "%s stage record is not INDEPENDENT" % stage))
        if not record.get("snapshot_identity"):
            issues.append(Issue(CODE_STAGE_VERDICT, "%s stage record has no snapshot_identity" % stage))
        if not record.get("holder_identity_ref"):
            issues.append(Issue(CODE_STAGE_VERDICT, "%s stage record has no holder_identity_ref" % stage))
        verdict = record.get("verdict")
        if verdict not in STAGE_VERDICT_VOCABULARY[stage]:
            issues.append(
                Issue(CODE_STAGE_VERDICT, "%s stage record verdict %r is not in the stage vocabulary" % (stage, verdict))
            )
        elif verdict != AFFIRMATIVE_STAGE[stage]:
            issues.append(
                Issue(CODE_STAGE_VERDICT, "%s stage verdict %r is not affirmative" % (stage, verdict))
            )
    required = ["D", "E"] + (["B"] if plan_audit_applies else [])
    for stage in required:
        if stage not in by_stage:
            issues.append(Issue(CODE_REQUIRED_INPUT, "required %s stage record is missing" % stage))
    return StageResult(present_by_stage=by_stage, issues=issues)


def validate_head_history(
    head_history: Envelope,
    verdict: typing.Optional[typing.Mapping[str, object]] = None,
) -> HeadHistory:
    """Validate the authoritative published-head export, its provenance and its binding.

    The export is authoritative only if its provenance status is VERIFIED *for
    the evaluated change/head*: the payload must declare the change id and the
    candidate head it was captured for, and both must match the evaluated
    record.  A VERIFIED string on a foreign or earlier export therefore cannot
    drive the review-head budget.
    """

    issues: typing.List[Issue] = list(head_history.issues)
    status = head_history.provenance.get("status")
    if status not in INPUT_STATUSES:
        issues.append(Issue(CODE_REQUIRED_INPUT, "head-history provenance.status is missing or invalid"))
        return HeadHistory(present=True, status="UNVERIFIED", heads=[], issues=issues)
    heads = head_history.payload.get("heads")
    if not isinstance(heads, list):
        issues.append(Issue(CODE_REQUIRED_INPUT, "head-history payload has no heads list"))
        heads = []
    if status != "VERIFIED":
        issues.append(
            Issue(CODE_REQUIRED_INPUT, "head-history provenance.status is %s, not VERIFIED" % status)
        )
    declared_change = head_history.payload.get("change_id")
    declared_head = head_history.payload.get("candidate_head")
    if verdict is not None:
        change = verdict.get("change") if isinstance(verdict.get("change"), dict) else {}
        expected_change = change.get("id")
        expected_head = verdict.get("head_sha")
        if declared_change is None:
            issues.append(
                Issue(
                    CODE_REQUIRED_INPUT,
                    "head-history payload declares no change_id; the export cannot be bound to the evaluated change",
                )
            )
        elif expected_change is not None and str(declared_change) != str(expected_change):
            issues.append(
                Issue(
                    CODE_REQUIRED_INPUT,
                    "head-history export is for change %r, not the evaluated change %r"
                    % (declared_change, expected_change),
                )
            )
        if declared_head is None:
            issues.append(
                Issue(
                    CODE_REQUIRED_INPUT,
                    "head-history payload declares no candidate_head; the export cannot be bound to the evaluated head",
                )
            )
        elif expected_head and str(declared_head) != str(expected_head):
            issues.append(
                Issue(
                    CODE_REQUIRED_INPUT,
                    "head-history export is captured for head %r, not the evaluated head %r"
                    % (declared_head, expected_head),
                )
            )
    for head in heads:
        if not isinstance(head, dict):
            issues.append(Issue(CODE_CANONICAL, "head-history entry is not an object"))
    return HeadHistory(present=True, status=typing.cast(str, status), heads=typing.cast(typing.List[typing.Dict[str, object]], heads), issues=issues)


def check_evidence_set(record: typing.Mapping[str, object], verdict: typing.Mapping[str, object]) -> typing.List[Issue]:
    """Re-derive VB-C09 from the supplied evidence set."""

    issues: typing.List[Issue] = []
    evidence = record.get("evidence_set")
    if not isinstance(evidence, list):
        return [Issue(CODE_REQUIRED_INPUT, "record.evidence_set is missing")]
    normalised = []
    for item in evidence:
        if not isinstance(item, dict):
            issues.append(Issue(CODE_CANONICAL, "evidence_set entry is not an object"))
            continue
        normalised.append(
            {
                "evidence_id": item.get("evidence_id"),
                "sha256": item.get("sha256"),
                "head": item.get("head"),
            }
        )
    recomputed = canonical.digest(normalised)
    if recomputed != verdict.get("evidence_inputs_sha256"):
        issues.append(Issue(CODE_CANONICAL, "VB-C09 evidence_inputs_sha256 does not recompute"))
    return issues
