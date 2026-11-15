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

# The only subprocess entrypoints the preflight may invoke.  git plumbing is
# restricted to read-only subcommands.
SUBPROCESS_MODULES = ("scripts/aegis_verdict_gate/run.py", "tools.aegis_evidence_reuse")
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


# --- Governance resolver vocabulary and result records (P0-GOV C1) ----------
# The resolver/validator lives in governance.py; these are the shared closed
# vocabularies and the typed result records it returns.  They add a second verb
# family to this package and do not change PF-01..PF-10 semantics.

GOVERNANCE_SCHEMA_VERSION = "aegis.governance-output/v1"
GOVERNANCE_CHECK_IDS = (
    "GR-01", "GR-02", "GR-03", "GR-04", "GR-05", "GR-06",
    "GR-07", "GR-08", "GR-09", "GR-10", "GR-11", "GR-12",
)
GOVERNANCE_STATUSES = ("PASS", "FAIL", "BLOCKED", "UNRUN")
GOVERNANCE_DECISIONS = ("ALLOW", "DENY", "BLOCKED")
ROLE_IDS = ("source-library", "consumer")
ROUTE_IDS = (
    "source-checkout",
    "copied-starter",
    "external-skill",
    "standalone-export",
    "resume",
    "compaction",
    "handoff",
)
ROUTE_FAMILIES = (
    "source-checkout",
    "copied-starter",
    "external-skill",
    "standalone-export",
    "session-boundary",
)
ROUTE_FAMILY_OF = {
    "source-checkout": "source-checkout",
    "copied-starter": "copied-starter",
    "external-skill": "external-skill",
    "standalone-export": "standalone-export",
    "resume": "session-boundary",
    "compaction": "session-boundary",
    "handoff": "session-boundary",
}
# The observation typing of the session-boundary route ids.  An old receipt
# keeps its old observation type; admission never upgrades it.
BOUNDARY_OBSERVATION_OF = {
    "resume": "resume",
    "compaction": "compaction",
    "handoff": "handoff",
}
OBSERVATION_TYPES = ("fresh-start", "resume", "compaction", "handoff", "protected-operation")
OPERATION_CLASSES = (
    "read-only-diagnostic",
    "design-plan-write",
    "protected-write",
    "commit",
    "push",
    "pr-create-update",
    "merge",
    "deploy-publish",
    "provider-call-spend",
    "settings-branch-protection-change",
    "consumer-repository-write",
    "manual-only-invocation",
)
ENFORCEMENT_CLASSES = ("HOST-ENFORCED", "CI-REQUIRED", "CI-STRUCTURAL", "GUIDANCE-ONLY")
DEPENDENCY_CLASSES = ("required", "conditional", "optional", "maintainer-only")
CONDITION_RULES = (
    "delivery-stage-work",
    "protected-operation",
    "consumer-adoption-work",
    "prior-review-artifact",
    "manual-only-invocation",
    "source-role-register-read",
)
BUDGET_CATEGORIES = (
    "planning-revision",
    "code-review-round",
    "review-head",
    "host-evidence",
)
LIFECYCLE_STATES = ("effective", "superseded", "withdrawn")
RULE_LIFECYCLE_ACTIVE = ("effective", "effective-conditional", "evidence-only", "program", "recording")
RULE_LIFECYCLE_EXCLUDED = {
    "historical": "historical",
    "proposed": "proposed-not-in-force",
    "ambiguous": "ambiguous-classification",
}
AUTHORITY_KINDS = ("OWNER_LINE", "A_ROW", "DECISION")
ADOPTION_STATES = ("adopted", "not-adopted", "withdrawn", "unknown")
HOST_CLAIM_LABELS = ("OBSERVED-TESTED", "OBSERVED-IDENTITY-ONLY", "UNSUPPORTED-UNVERIFIED")


@dataclasses.dataclass
class GovernanceFinding:
    """One GR-* finding (never a verdict, never an approval)."""

    code: str
    status: str
    message: str
    ref: str = ""

    def as_dict(self) -> typing.Dict[str, object]:
        return {"code": self.code, "status": self.status, "message": self.message, "ref": self.ref}


@dataclasses.dataclass
class ResolvedDocument:
    """One document in a resolved set, with the identity that was re-derived."""

    doc_id: str
    path: str
    bytes: int
    sha256: str
    role_scope: typing.Sequence[str]
    lifecycle: str
    read_status: str
    adoption_provenance: typing.Optional[str] = None

    def as_dict(self) -> typing.Dict[str, object]:
        return {
            "doc_id": self.doc_id,
            "path": self.path,
            "bytes": self.bytes,
            "sha256": self.sha256,
            "role_scope": list(self.role_scope),
            "lifecycle": self.lifecycle,
            "read_status": self.read_status,
            "adoption_provenance": self.adoption_provenance,
        }


@dataclasses.dataclass
class ResolutionResult:
    """Result of resolving one role/route against one contract.

    status is RESOLVED or BLOCKED; BLOCKED is fail-closed and always names the
    missing/changed/hard-failure inputs in findings and exclusions.  No field
    here is authority: the resolution is an observation.
    """

    status: str
    role: str
    route_id: str
    route_family: str
    resolved_documents: typing.List[ResolvedDocument]
    conditional_documents: typing.List[typing.Dict[str, object]]
    excluded_documents: typing.List[typing.Dict[str, object]]
    resolved_rules: typing.List[typing.Dict[str, object]]
    exclusions: typing.List[typing.Dict[str, object]]
    conflicts: typing.List[typing.Dict[str, object]]
    findings: typing.List[GovernanceFinding]
    enforcement_claim: str
    gates_active: str
    labels: typing.List[str]
    resolved_set_digest: str
    nested_local_policy: typing.List[typing.Dict[str, object]] = dataclasses.field(default_factory=list)
    adoption_state: str = "unknown"
    adoption_authority_ref: typing.Optional[str] = None
    adoption_ref: typing.Optional[str] = None
    adoption_sha256: typing.Optional[str] = None
    installation_pin: typing.Optional[typing.Dict[str, object]] = None
    limitations: typing.List[str] = dataclasses.field(default_factory=list)

    def as_dict(self) -> typing.Dict[str, object]:
        return {
            "status": self.status,
            "role": self.role,
            "route_id": self.route_id,
            "route_family": self.route_family,
            "resolved_documents": [document.as_dict() for document in self.resolved_documents],
            "conditional_documents": list(self.conditional_documents),
            "excluded_documents": list(self.excluded_documents),
            "resolved_rules": list(self.resolved_rules),
            "exclusions": list(self.exclusions),
            "conflicts": list(self.conflicts),
            "findings": [finding.as_dict() for finding in self.findings],
            "enforcement_claim": self.enforcement_claim,
            "gates_active": self.gates_active,
            "labels": list(self.labels),
            "resolved_set_digest": self.resolved_set_digest,
            "nested_local_policy": list(self.nested_local_policy),
            "adoption_state": self.adoption_state,
            "adoption_authority_ref": self.adoption_authority_ref,
            "adoption_ref": self.adoption_ref,
            "adoption_sha256": self.adoption_sha256,
            "installation_pin": self.installation_pin,
            "limitations": list(self.limitations),
        }


@dataclasses.dataclass
class AdmissionOutcome:
    """One protected-operation admission decision record (never a permission)."""

    decision: str
    reason_code: str
    recheck: typing.Dict[str, object]
    decision_record: typing.Dict[str, object]

    def as_dict(self) -> typing.Dict[str, object]:
        return {
            "decision": self.decision,
            "reason_code": self.reason_code,
            "recheck": dict(self.recheck),
            "decision_record": dict(self.decision_record),
        }
