"""Required-governance contract: deterministic render, validation, resolver, receipts, admission.

P0-GOV C1 implementation (plan of record r3 sections 5-7, 9.2).  This module is the
second verb family of tools/aegis_preflight: a read-only, offline, stdlib-only
resolver/validator for the versioned governance contract and its four schemas.
It adds GR-01..GR-12 governance checks and leaves PF-01..PF-10 semantics
unchanged.

Assurance: AUDITABLE TOOLING, NOT ENFORCEMENT.  Nothing here denies a host tool
call, proves reading or obedience, or creates approval.  The render verbs write
nothing: they print canonical JSON bytes to stdout for the operator to redirect
into the committed artifacts; the test suite proves the committed artifacts are
byte-identical to the render output.

CLI (from the repository root)::

    python -m tools.aegis_preflight governance validate --contract docs/governance/payload/required-governance-contract.v1.json --repo-root .
    python -m tools.aegis_preflight governance resolve --role source-library --route source-checkout --repo-root . [--adoption PATH] [--json]
    python -m tools.aegis_preflight governance receipt --role consumer --route copied-starter --observation-type fresh-start --repo-root . ...
    python -m tools.aegis_preflight governance admit --receipt receipt.json --operation-class commit --repo-root . ...
    python -m tools.aegis_preflight governance render --artifact contract|projection|governance-dependencies --repo-root .

Exit codes: 0 pass/allow, 1 findings or blocked/deny, 2 invalid input/usage, 3
internal error (never 0).
"""
from __future__ import annotations

import hashlib
import json
import re
import sys
import typing
from pathlib import Path

from . import models

# ---------------------------------------------------------------------------
# Locations and identities
# ---------------------------------------------------------------------------

GOVERNANCE_DIR = "docs/governance"
PAYLOAD_DIR = "docs/governance/payload"
CONTRACT_RELPATH = "docs/governance/payload/required-governance-contract.v1.json"
PROJECTION_RELPATH = "docs/governance/payload/rule-projection.v1.json"
SCHEMA_RELPATHS = {
    "contract": "docs/governance/payload/schemas/governance-contract-v1.schema.json",
    "receipt": "docs/governance/payload/schemas/context-receipt-v1.schema.json",
    "adoption": "docs/governance/payload/schemas/adoption-record-v1.schema.json",
    "admission": "docs/governance/payload/schemas/admission-decision-v1.schema.json",
}
SOURCE_RELPATH = "docs/governance/governance-payload.source.json"
DEPENDENCIES_RELPATH = "docs/governance/governance-payload.dependencies.json"
MANIFEST_RELPATH = "docs/governance/governance-payload.manifest.json"
INVENTORY_RELPATH = "docs/governance/inputs/governance-inventory.json"
GOVERNANCE_DEPENDENCIES_RELPATH = "tools/governance-dependencies.json"
SKILLS_DIR = ".claude/skills"
SKILL_ENTRYPOINT_NAME = "SKILL.md"
SKILL_TEMPLATE_DIR = "_template"

CONTRACT_SCHEMA_ID = "aegis.governance-contract/1"
CONTRACT_ID = "aegis.required-governance"
CONTRACT_VERSION = "1.0.0"
RECEIPT_SCHEMA_ID = "aegis.context-receipt/1"
ADOPTION_SCHEMA_ID = "aegis.governance-adoption/1"
ADMISSION_SCHEMA_ID = "aegis.admission-decision/1"
RULE_PROJECTION_SCHEMA_ID = "aegis.rule-projection/1"
GOVERNANCE_DEPENDENCIES_SCHEMA_ID = "aegis.governance-dependencies/1"
OUTPUT_SCHEMA_ID = models.GOVERNANCE_SCHEMA_VERSION
TOOL_NAME = "aegis-governance"
TOOL_VERSION = "1.0.0"

# Task-33 inventory identity (the governed generation input).  The repository
# stores the inventory LF-normalized because the repository's .gitattributes
# policy (text=auto eol=lf) normalizes text files on commit; the raw task-33
# source identity is recorded beside it so the conversion is explicit, not a
# silent byte change.  The JSON semantics are identical.  Any change to the
# committed bytes is refused by the build: a new inventory requires a deliberate
# projection/contract regeneration under review.
INVENTORY_PATH = "docs/governance/inputs/governance-inventory.json"
INVENTORY_BYTES = 465578
INVENTORY_LF = 8008
INVENTORY_SHA256 = "FCDC04B3AFF8FC117BCF5EC3451A4539D99C4AC0B181DABC9695200199FFEDBC"
INVENTORY_SOURCE_RAW = {
    "bytes": 473586,
    "lf": 8008,
    "cr": 8008,
    "sha256": "902E443A33C677BDA0A761B2F91F59FC37CF8CC8F0D55D3F6B2B8516C057C3C3",
    "encoding": "UTF-8 with CRLF line endings as produced by task-33",
}
INVENTORY_NORMALIZATION = "CRLF->LF only (repository text policy); JSON semantics unchanged"

HEX40_RE = re.compile(r"^[0-9a-f]{40}$")
HEX64_UPPER_RE = re.compile(r"^[0-9A-F]{64}$")
SEMVER_RE = re.compile(r"^[0-9]+\.[0-9]+\.[0-9]+$")
ROUTE_ID_SET = frozenset(models.ROUTE_IDS)
ROUTE_FAMILY_SET = frozenset(models.ROUTE_FAMILIES)
OBSERVATION_TYPE_SET = frozenset(models.OBSERVATION_TYPES)
OPERATION_CLASS_SET = frozenset(models.OPERATION_CLASSES)
ENFORCEMENT_CLASS_SET = frozenset(models.ENFORCEMENT_CLASSES)
DEPENDENCY_CLASS_SET = frozenset(models.DEPENDENCY_CLASSES)
CONDITION_RULE_SET = frozenset(models.CONDITION_RULES)
ROLE_SET = frozenset(models.ROLE_IDS)
ACTIVE_RULE_LIFECYCLES = frozenset(models.RULE_LIFECYCLE_ACTIVE)

EXIT_PASS = 0
EXIT_FINDINGS = 1
EXIT_USAGE = 2
EXIT_INTERNAL = 3

MAX_SEVERITY = {"PASS": 0, "UNRUN": 1, "BLOCKED": 2, "FAIL": 3}

# ---------------------------------------------------------------------------
# Authored contract content (deterministic; the rule_applicability fields and
# the document identities are the only generated parts)
# ---------------------------------------------------------------------------

SUMMARY = (
    "A versioned, machine-readable statement of which Aegis documents and rules govern a "
    "source-library (Role A) or consumer (Role B) work item, how the governance dependency is "
    "resolved for five entry-route families, what a context receipt must record, and what this "
    "repository can and cannot enforce on the observed host. It binds authoritative documents "
    "and rules by identity and declares applicability, lifecycle and local adoption; it neither "
    "replaces any authoritative document nor creates approval, and it does not enforce at "
    "runtime."
)

# role_scope: which repository roles the document is in scope for.  Consumer-copied
# startup files, the consumer manual-only policy family and the consumer-adoption
# pages are in scope for both roles; every other document is source-library only.
DOCUMENT_ROLE_SCOPE = {
    "AGENTS": ("source-library", "consumer"),
    "CLAUDE": ("source-library", "consumer"),
    "CONTRIBUTING": ("source-library",),
    "DW": ("source-library",),
    "REGISTER": ("source-library",),
    "MANUAL-ONLY-POLICY": ("source-library", "consumer"),
    "CONSUMER-MANUAL-ONLY": ("source-library", "consumer"),
    "STARTER": ("source-library", "consumer"),
    "STATUS-PRESENTATION": ("source-library", "consumer"),
    "READINESS-GUIDE": ("source-library", "consumer"),
    "COMPATIBILITY-MATRIX": ("source-library", "consumer"),
    "SUPPORT-CLAIMS": ("source-library", "consumer"),
    "OPEN-DECISIONS": ("source-library",),
    "OWNER-DECISIONS": ("source-library",),
    "RECONCILIATION": ("source-library",),
    "AUTO-MERGE-POLICY": ("source-library",),
    "MATURITY-PACKAGE": ("source-library",),
    "EXECUTION-METRICS": ("source-library",),
    "READABILITY-BACKLOG": ("source-library",),
    "APPROVAL-LIFECYCLE-GRADING": ("source-library",),
    "SKILL-GENERATION-STANDARD": ("source-library",),
    "ZERO-TRUST-DISCIPLINE": ("source-library",),
    "OFFLINE-CI": ("source-library",),
    "PR-TEMPLATE": ("source-library",),
    "CODEOWNERS": ("source-library",),
    "VALIDATE-SKILLS-WORKFLOW": ("source-library",),
    "SECURITY": ("source-library",),
}

DOCUMENT_AUTHORITY_CLASS = {
    "AGENTS": "owner-instruction",
    "CLAUDE": "owner-instruction",
    "CONTRIBUTING": "policy",
    "DW": "policy",
    "REGISTER": "record",
    "MANUAL-ONLY-POLICY": "policy",
    "CONSUMER-MANUAL-ONLY": "policy",
    "STARTER": "policy",
    "STATUS-PRESENTATION": "policy",
    "READINESS-GUIDE": "evidence",
    "COMPATIBILITY-MATRIX": "evidence",
    "SUPPORT-CLAIMS": "evidence",
    "OPEN-DECISIONS": "record",
    "OWNER-DECISIONS": "record",
    "RECONCILIATION": "record",
    "AUTO-MERGE-POLICY": "record",
    "MATURITY-PACKAGE": "record",
    "EXECUTION-METRICS": "record",
    "READABILITY-BACKLOG": "record",
    "APPROVAL-LIFECYCLE-GRADING": "method",
    "SKILL-GENERATION-STANDARD": "policy",
    "ZERO-TRUST-DISCIPLINE": "method",
    "OFFLINE-CI": "record",
    "PR-TEMPLATE": "policy",
    "CODEOWNERS": "enforcement-surface",
    "VALIDATE-SKILLS-WORKFLOW": "enforcement-surface",
    "SECURITY": "policy",
}

DOCUMENT_EFFECTIVE_FROM = "2026-11-14"
CONTRACT_REVIEW_DATE = "2026-12-15"

# Role profiles (plan section 7.1-7.2).  Required documents are the normative
# Tier 1 set for the source role (tier + normative flag in the authoritative set)
# or the copied/consumer-local set for the consumer role.  Conditional documents
# are resolved only when the named condition holds; exclusions are recorded with
# a reason and never silently dropped.
ROLE_PROFILES = {
    "source-library": {
        "role_id": "source-library",
        "required_documents": [
            "AGENTS",
            "CLAUDE",
            "CONSUMER-MANUAL-ONLY",
            "CONTRIBUTING",
            "DW",
            "MANUAL-ONLY-POLICY",
            "PR-TEMPLATE",
            "REGISTER",
            "SKILL-GENERATION-STANDARD",
            "STARTER",
        ],
        "conditional_documents": [
            {"doc_id": "APPROVAL-LIFECYCLE-GRADING", "condition": "prior-review-artifact"},
            {"doc_id": "AUTO-MERGE-POLICY", "condition": "delivery-stage-work"},
            {"doc_id": "COMPATIBILITY-MATRIX", "condition": "consumer-adoption-work"},
            {"doc_id": "EXECUTION-METRICS", "condition": "delivery-stage-work"},
            {"doc_id": "MATURITY-PACKAGE", "condition": "delivery-stage-work"},
            {"doc_id": "OFFLINE-CI", "condition": "protected-operation"},
            {"doc_id": "OPEN-DECISIONS", "condition": "delivery-stage-work"},
            {"doc_id": "OWNER-DECISIONS", "condition": "delivery-stage-work"},
            {"doc_id": "READABILITY-BACKLOG", "condition": "delivery-stage-work"},
            {"doc_id": "READINESS-GUIDE", "condition": "consumer-adoption-work"},
            {"doc_id": "RECONCILIATION", "condition": "delivery-stage-work"},
            {"doc_id": "STATUS-PRESENTATION", "condition": "consumer-adoption-work"},
            {"doc_id": "SUPPORT-CLAIMS", "condition": "consumer-adoption-work"},
            {"doc_id": "ZERO-TRUST-DISCIPLINE", "condition": "delivery-stage-work"},
        ],
        "exclusions": [
            {"doc_id": "CODEOWNERS", "reason": "enforcement surface: recorded, not a rule source (Tier 3)"},
            {"doc_id": "SECURITY", "reason": "enforcement surface: recorded, not a rule source (Tier 3)"},
            {"doc_id": "VALIDATE-SKILLS-WORKFLOW", "reason": "enforcement surface: recorded, not a rule source (Tier 3)"},
        ],
        "adoption_required": False,
        "role_entry_routes": ["compaction", "handoff", "resume", "source-checkout"],
    },
    "consumer": {
        "role_id": "consumer",
        "required_documents": [
            "AGENTS",
            "CLAUDE",
            "CONSUMER-MANUAL-ONLY",
            "MANUAL-ONLY-POLICY",
            "STARTER",
        ],
        "conditional_documents": [
            {"doc_id": "COMPATIBILITY-MATRIX", "condition": "consumer-adoption-work"},
            {"doc_id": "READINESS-GUIDE", "condition": "consumer-adoption-work"},
            {"doc_id": "STATUS-PRESENTATION", "condition": "consumer-adoption-work"},
            {"doc_id": "SUPPORT-CLAIMS", "condition": "consumer-adoption-work"},
        ],
        "exclusions": [
            {"doc_id": "APPROVAL-LIFECYCLE-GRADING", "reason": "source-library document; Role B does not inherit the source process by copying"},
            {"doc_id": "AUTO-MERGE-POLICY", "reason": "source-library document; Role B does not inherit the source process by copying"},
            {"doc_id": "CODEOWNERS", "reason": "source-library enforcement surface; not distributed to consumers"},
            {"doc_id": "CONTRIBUTING", "reason": "source-library document; Role B does not inherit the source process by copying"},
            {"doc_id": "DW", "reason": "source-library document; Role B does not inherit the source process by copying"},
            {"doc_id": "EXECUTION-METRICS", "reason": "source-library document; Role B does not inherit the source process by copying"},
            {"doc_id": "MATURITY-PACKAGE", "reason": "source-library document; Role B does not inherit the source process by copying"},
            {"doc_id": "OFFLINE-CI", "reason": "source-library document; Role B does not inherit the source process by copying"},
            {"doc_id": "OPEN-DECISIONS", "reason": "source-library document; Role B does not inherit the source process by copying"},
            {"doc_id": "OWNER-DECISIONS", "reason": "source-library document; Role B does not inherit the source process by copying"},
            {"doc_id": "PR-TEMPLATE", "reason": "source-library document; Role B does not inherit the source process by copying"},
            {"doc_id": "READABILITY-BACKLOG", "reason": "source-library document; Role B does not inherit the source process by copying"},
            {"doc_id": "RECONCILIATION", "reason": "source-library document; Role B does not inherit the source process by copying"},
            {"doc_id": "REGISTER", "reason": "source-library document; Role B does not inherit the source process by copying"},
            {"doc_id": "SECURITY", "reason": "source-library enforcement surface; not distributed to consumers"},
            {"doc_id": "SKILL-GENERATION-STANDARD", "reason": "source-library document; Role B does not inherit the source process by copying"},
            {"doc_id": "VALIDATE-SKILLS-WORKFLOW", "reason": "source-library enforcement surface; not distributed to consumers"},
            {"doc_id": "ZERO-TRUST-DISCIPLINE", "reason": "source-library document; Role B does not inherit the source process by copying"},
        ],
        "adoption_required": True,
        "role_entry_routes": ["compaction", "copied-starter", "external-skill", "handoff", "resume", "standalone-export"],
    },
}

ENTRY_ROUTES = [
    {
        "route_family": "source-checkout",
        "route_ids": ["source-checkout"],
        "triggers": [
            "an agent works in a checkout whose four source-library landmarks are present",
        ],
        "resolution_inputs": ["target_root", "role_evidence", "host_session_facts"],
        "required": True,
        "fail_closed_behavior": (
            "block dependent work and name the missing or changed document; diagnostic reads "
            "remain allowed with the missing source named"
        ),
        "evidence_required": [
            "resolved document identities (bytes/sha256 re-derived in-turn)",
            "context receipt",
            "admission decision record for the protected class",
        ],
        "supported_host_scope": {
            "scope": "repository content and local auditable tooling",
            "claim_label": "GUIDANCE-ONLY",
            "host_evidence_ref": "none",
            "limitations": ["no runtime enforcement on the observed host"],
        },
    },
    {
        "route_family": "copied-starter",
        "route_ids": ["copied-starter"],
        "triggers": [
            "a consumer repository contains the copied startup files and installed skills without the source landmarks",
        ],
        "resolution_inputs": ["target_root", "role_evidence", "adoption_record"],
        "required": True,
        "fail_closed_behavior": (
            "an absent, malformed, mismatched or revoked adoption record means not-adopted and "
            "dependent work blocks; a gate-owning skill outside the installed set stops and names "
            "the install"
        ),
        "evidence_required": [
            "consumer context receipt",
            "adoption record identity",
            "excluded source documents with reasons",
        ],
        "supported_host_scope": {
            "scope": "repository content; live starter install is a separate governed outcome (O12)",
            "claim_label": "GUIDANCE-ONLY",
            "host_evidence_ref": "none",
            "limitations": ["live starter install is UNRUN; case 02 evidence is synthetic-only in P0"],
        },
    },
    {
        "route_family": "external-skill",
        "route_ids": ["external-skill"],
        "triggers": ["a skill is opened from outside the target root"],
        "resolution_inputs": [
            "target_root",
            "role_evidence",
            "skill_packaging_metadata",
            "approved_upstream_pin",
        ],
        "required": True,
        "fail_closed_behavior": (
            "a pin or contract mismatch between the skill's expected dependency and the target "
            "blocks with both versions named"
        ),
        "evidence_required": [
            "declared skill dependency (tools/governance-dependencies.json)",
            "target adoption state",
            "pin comparison",
        ],
        "supported_host_scope": {
            "scope": "packaging metadata and resolver tooling",
            "claim_label": "GUIDANCE-ONLY",
            "host_evidence_ref": "none",
            "limitations": ["the live OpsFlow-shaped route is UNRUN; no OpsFlow edit is performed"],
        },
    },
    {
        "route_family": "standalone-export",
        "route_ids": ["standalone-export"],
        "triggers": ["a single skill is copied or exported without the rest of the library"],
        "resolution_inputs": ["target_root", "skill_packaging_metadata", "adoption_record"],
        "required": True,
        "fail_closed_behavior": (
            "the export is rejected when a required governance dependency edge is missing; the "
            "resolver never treats an absent dependency as none"
        ),
        "evidence_required": [
            "distributed-payload closure report (verify --check-dependencies)",
            "governance dependency declaration",
        ],
        "supported_host_scope": {
            "scope": "structural packaging check, not runtime enforcement",
            "claim_label": "CI-STRUCTURAL",
            "host_evidence_ref": "none",
            "limitations": ["the closure check runs locally/read-only and is not a required context"],
        },
    },
    {
        "route_family": "session-boundary",
        "route_ids": ["resume", "compaction", "handoff"],
        "triggers": [
            "a session continues across a boundary: resume after interruption, context compaction, or handoff to a replacement agent",
        ],
        "resolution_inputs": ["host_session_facts", "target_root", "role_evidence"],
        "required": True,
        "fail_closed_behavior": (
            "re-establish the current context before the next protected operation; a receipt "
            "observed before the boundary cannot authorize it"
        ),
        "evidence_required": [
            "resume/compaction/handoff receipt with the typed observation",
            "fresh admission recheck before the next protected class",
        ],
        "supported_host_scope": {
            "scope": "session-boundary logic tested synthetically",
            "claim_label": "GUIDANCE-ONLY",
            "host_evidence_ref": "none",
            "limitations": [
                "no handoff primitive on the observed host; live resume/compaction evidence is UNRUN",
            ],
        },
    },
]

DEPENDENCY_GRAPH = [
    {"from_node": "doc:AGENTS", "to_doc_id": "REGISTER", "class": "conditional", "rule": "source-role-register-read", "reason": "a source-role agent reads the grant register before relying on any grant"},
    {"from_node": "doc:DW", "to_doc_id": "PR-TEMPLATE", "class": "required", "rule": None, "reason": "the PR-body obligations are defined by the canonical workflow"},
    {"from_node": "doc:DW", "to_doc_id": "REGISTER", "class": "required", "rule": None, "reason": "the workflow's gates cite register entries that are not imported into the contract"},
    {"from_node": "doc:STARTER", "to_doc_id": "CONSUMER-MANUAL-ONLY", "class": "conditional", "rule": "consumer-adoption-work", "reason": "consumer route resolves the consumer manual-only contract only while adopting"},
    {"from_node": "doc:STARTER", "to_doc_id": "MANUAL-ONLY-POLICY", "class": "required", "rule": None, "reason": "the starter installs the manual-only policy reference"},
    {"from_node": "route:copied-starter", "to_doc_id": "AGENTS", "class": "required", "rule": None, "reason": "the copied startup file is the consumer's instruction entry"},
    {"from_node": "route:copied-starter", "to_doc_id": "CLAUDE", "class": "required", "rule": None, "reason": "the copied startup file is the consumer's instruction entry"},
    {"from_node": "route:copied-starter", "to_doc_id": "CONSUMER-MANUAL-ONLY", "class": "required", "rule": None, "reason": "consumer manual-only obligations are normative for adopters"},
    {"from_node": "route:copied-starter", "to_doc_id": "MANUAL-ONLY-POLICY", "class": "required", "rule": None, "reason": "manual-only policy reference installed by the starter"},
    {"from_node": "route:external-skill", "to_doc_id": "CONSUMER-MANUAL-ONLY", "class": "conditional", "rule": "consumer-adoption-work", "reason": "external skill work resolves the target's consumer obligations only while adopting"},
    {"from_node": "route:external-skill", "to_doc_id": "MANUAL-ONLY-POLICY", "class": "required", "rule": None, "reason": "an external skill may not auto-apply a manual-only step"},
    {"from_node": "route:source-checkout", "to_doc_id": "AGENTS", "class": "required", "rule": None, "reason": "the startup instruction is the source entry pointer"},
    {"from_node": "route:source-checkout", "to_doc_id": "DW", "class": "required", "rule": None, "reason": "source work resolves the canonical seven-stage workflow"},
    {"from_node": "route:source-checkout", "to_doc_id": "REGISTER", "class": "required", "rule": None, "reason": "source authority is derived only from the register/owner lines"},
    {"from_node": "route:standalone-export", "to_doc_id": "MANUAL-ONLY-POLICY", "class": "required", "rule": None, "reason": "an exported skill may not auto-apply a manual-only step"},
    {"from_node": "route_family:session-boundary", "to_doc_id": "AGENTS", "class": "required", "rule": None, "reason": "re-establish the startup instruction before the next protected operation"},
    {"from_node": "route_family:session-boundary", "to_doc_id": "DW", "class": "conditional", "rule": "protected-operation", "reason": "a session boundary before a protected operation resolves the workflow"},
    {"from_node": "skill:agent-startup-context-gate", "to_doc_id": "AGENTS", "class": "required", "rule": None, "reason": "the startup gate verifies the instruction source"},
    {"from_node": "skill:agent-startup-context-gate", "to_doc_id": "DW", "class": "conditional", "rule": "protected-operation", "reason": "the startup gate feeds protected operations that need the workflow"},
    {"from_node": "skill:plan-audit-reviewer", "to_doc_id": "APPROVAL-LIFECYCLE-GRADING", "class": "conditional", "rule": "prior-review-artifact", "reason": "an audit of recorded lifecycle evidence needs the grading semantics"},
    {"from_node": "skill:plan-audit-reviewer", "to_doc_id": "DW", "class": "required", "rule": None, "reason": "the independent audit contract is the canonical workflow's stage rule"},
    {"from_node": "skill:plan-of-record-author", "to_doc_id": "DW", "class": "required", "rule": None, "reason": "the plan-of-record contract is the canonical workflow's stage rule"},
    {"from_node": "skill:project-orchestrator", "to_doc_id": "AGENTS", "class": "required", "rule": None, "reason": "routing resolves the startup instruction"},
    {"from_node": "skill:project-orchestrator", "to_doc_id": "DW", "class": "conditional", "rule": "delivery-stage-work", "reason": "routing delivery-stage work needs the workflow"},
    {"from_node": "skill:release-readiness-reviewer", "to_doc_id": "COMPATIBILITY-MATRIX", "class": "required", "rule": None, "reason": "a readiness claim cites the compatibility matrix"},
    {"from_node": "skill:release-readiness-reviewer", "to_doc_id": "SUPPORT-CLAIMS", "class": "required", "rule": None, "reason": "a readiness claim cites the support-claims ledger"},
]

LIFECYCLE = {
    "status": "proposed",
    "review_date": CONTRACT_REVIEW_DATE,
    "supersedes": None,
    "migration_rule": (
        "A consumer adopts a new contract by recording the new contract id/version/sha256 in its "
        "adoption record; a source edit to any bound document requires re-generation, a "
        "contract_version bump and a re-derived manifest; receipts observed under an older "
        "contract remain old observations and are never upgraded."
    ),
    "rollback_rule": (
        "Roll back by restoring the previous committed payload bytes and manifest and superseding "
        "the new contract version in the record; never restore revoked authority and never "
        "silently delete consumer-local policy files. Triggers: a false admission, a broken "
        "install, an unusable restoration, or the owner's withdrawal."
    ),
}

LOCAL_ADOPTION = {
    "schema": ADOPTION_SCHEMA_ID,
    "required_for_consumer": True,
    "record_paths": ["docs/aegis-adoption.json", "docs/project-state.md (A-* rows)"],
    "required_fields": [
        "schema",
        "target_repo",
        "adopter_role",
        "authority",
        "contract",
        "adoption",
        "manual_only_overrides_ref",
        "installation",
        "effective_at_utc",
        "revoked_at_utc",
        "revocation_authority",
        "supersedes",
        "next_review_date",
        "limitations",
    ],
    "invalidation_inputs": [
        "contract bytes/version",
        "any required document hash",
        "the approved upstream pin",
        "the target repository or role",
        "the adoption record content (including a withdrawal or re-pin)",
        "any nested/local policy file hash",
        "the host build/profile digest or session boundary",
        "the task/authority reference",
    ],
}

HOST_BOUNDARY = {
    "supported_hosts": [
        {
            "host_product": "DeepSeek Harness Desktop",
            "host_version": "0.2.2-rc.1",
            "host_build_sha256": "5FA8A6B21BCEB8F3E99E30EFA2270EFD0CC773A11E42AA0488F804A64B34E637",
            "claim": "OBSERVED-IDENTITY-ONLY",
            "evidence_refs": [
                "task-34 host capability record: HOST-CAPABILITY.md sha256 AD096DA6330763D7502143E22B3DD7D958918440BF431B21A9F001DB5C935D03",
            ],
            "limitations": [
                "no repository-installable hook or interception facility was observed; no host gate is active",
                "the served model is unobservable; only the requested route can be recorded",
                "case 25 cannot pass on this host without a separately provisioned host-profile gate (owner choice O15)",
            ],
        },
    ],
    "unsupported_host_behavior": (
        "fail closed on any claimed enforcement; diagnostic reads remain allowed with the missing "
        "host evidence named"
    ),
    "data_exit_disclosures": [
        {"channel": "DSH session-log upload", "state": "DEFAULT-ON", "ref": "task-34 observed delivery events"},
        {"channel": "DSH plugin inventory", "state": "DOCUMENTED", "ref": "task-34"},
        {"channel": "DSH telemetry", "state": "DEFAULT-FEEDBACK-ONLY", "ref": "task-34"},
    ],
}

ENFORCEMENT_CLAIMS = {
    "claim": "GUIDANCE-ONLY",
    "claim_scope": (
        "all repository content in this change and the auditable tools it adds; no host gate is "
        "active on the observed installation"
    ),
    "named_surfaces": [
        {
            "surface": "validate-skills (configured as a required context; live registration DOCUMENTED-BUT-UNVERIFIED)",
            "class": "CI-REQUIRED",
            "evidence_ref": ".github/workflows/validate-skills.yml",
        },
        {
            "surface": "gate-guard (configured as a required context; live registration DOCUMENTED-BUT-UNVERIFIED)",
            "class": "CI-REQUIRED",
            "evidence_ref": ".github/workflows/validate-skills.yml",
        },
        {
            "surface": "aegis_preflight and distributed_payload (auditable local checks; not wired into CI)",
            "class": "CI-STRUCTURAL",
            "evidence_ref": "tools/aegis_preflight, tools/distributed_payload",
        },
    ],
    "host_plugin": None,
    "bypass_routes": [
        "direct Node effects inside run_code (inner tool calls are gated; direct fs/network/subprocess effects are not)",
        "alternate launchers and CLI profiles composing user-controlled policy",
        "GUI/remote bridges and ACP external backends with their own permission systems",
        "host-user configuration edits (bundle list, profile patch, --patch overlays)",
        "subprocess effects under the harness process authority",
        "local mutation of receipts and session logs by a sufficiently privileged actor",
        "default-on provider upload of session content",
    ],
    "unrun": [
        "live required-context registration and branch protection (DOCUMENTED-BUT-UNVERIFIED from this seat)",
        "live resume/compaction/handoff boundary evidence",
        "live bypass suite",
        "host-profile plugin absence (owner choice O15)",
        "served-model attestation",
        "live OpsFlow adoption route",
    ],
}

TRUST = {
    "authoritative_inputs": [
        "the target git tree bytes at a revision",
        "the contract bytes in the payload",
        "the register bytes for the source role",
        "the consumer's adoption record and local policy hashes",
        "host-exposed session facts where available",
    ],
    "not_authoritative": [
        "self-written receipts and JSON",
        "task-board prose",
        "another agent's assertion",
        "a provider model name",
    ],
    "verification_rule": (
        "every claim is re-derived in-turn against an authoritative input; a self-asserted "
        "receipt is evidence, never authority"
    ),
}

NON_CLAIMS = [
    "this contract is not an approval, a grant or a permission",
    "this contract does not enforce at runtime; on the observed host it is guidance-only and the auditable tools are local checks",
    "no serving-model attestation is made or possible from repository content",
    "no instruction-load or reading-comprehension guarantee is made",
    "no consumer readiness, support commitment or host qualification is claimed",
    "this contract is not a second policy, register, backlog or compliance scorecard",
    "reading this contract in a consumer repository does not make that repository a source-library seat",
]

CURRENT_CONTEXT_CONTRACT = (
    "receipts are self-asserted observations of the applicable context; admission re-derives the "
    "bound inputs and a stale or forged receipt blocks dependent work while diagnostic reads stay allowed"
)


# ---------------------------------------------------------------------------
# Errors and small helpers
# ---------------------------------------------------------------------------


class GovernanceError(ValueError):
    """A fail-closed governance error with a stable diagnostic code."""

    def __init__(self, code: str, message: str, ref: str = ""):
        self.code = code
        self.ref = ref
        detail = "%s: %s" % (code, message)
        if ref:
            detail = "%s [%s]: %s" % (code, ref, message)
        super().__init__(detail)


def canonical_bytes(value: object) -> bytes:
    """Deterministic artifact bytes: UTF-8, two-space indent, sorted keys, one trailing LF."""
    return (json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n").encode("utf-8")


def canonical_digest(value: object) -> str:
    """SHA-256 over a compact canonical JSON serialization (for digests, not artifacts)."""
    compact = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return hashlib.sha256(compact.encode("utf-8")).hexdigest()


def sha256_raw(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_upper(data: bytes) -> str:
    return sha256_raw(data).upper()


def count_lf(data: bytes) -> int:
    return data.count(b"\n")


def _relpath_parts(relpath: str) -> typing.Tuple[str, ...]:
    if not isinstance(relpath, str) or not relpath:
        raise GovernanceError("invalid_relpath", "path must be a non-empty relative string")
    normalized = relpath.replace("\\", "/")
    if normalized.startswith("/") or re.match(r"^[A-Za-z]:", normalized):
        raise GovernanceError("invalid_relpath", "absolute or drive-letter path is not allowed", relpath)
    parts = normalized.split("/")
    if any(part in ("", ".", "..") for part in parts):
        raise GovernanceError("invalid_relpath", "empty or dot path segment is not allowed", relpath)
    return tuple(parts)


def repo_path(repo_root: Path, relpath: str) -> Path:
    """Resolve a repository-relative path fail-closed (no escape outside the root)."""
    root = Path(repo_root).resolve()
    candidate = root.joinpath(*_relpath_parts(relpath)).resolve()
    try:
        candidate.relative_to(root)
    except ValueError as error:
        raise GovernanceError("path_escape", "path escapes the repository root", relpath) from error
    return candidate


def read_repo_bytes(repo_root: Path, relpath: str) -> bytes:
    path = repo_path(repo_root, relpath)
    try:
        return path.read_bytes()
    except OSError as error:
        raise GovernanceError("unreadable_file", "cannot read required file: %s" % error, relpath) from error


def read_repo_json(repo_root: Path, relpath: str) -> object:
    data = read_repo_bytes(repo_root, relpath)
    try:
        return json.loads(data.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise GovernanceError("invalid_json", "file is not valid UTF-8 JSON: %s" % error, relpath) from error


def file_identity(repo_root: Path, relpath: str) -> typing.Dict[str, object]:
    data = read_repo_bytes(repo_root, relpath)
    return {"path": relpath, "bytes": len(data), "lf": count_lf(data), "sha256": sha256_upper(data)}


def compare_semver(left: str, right: str) -> int:
    """Return -1/0/1 comparing two x.y.z versions; invalid versions raise."""
    for value in (left, right):
        if not isinstance(value, str) or not SEMVER_RE.match(value):
            raise GovernanceError("invalid_semver", "contract_version must be x.y.z numeric")
    left_parts = tuple(int(part) for part in left.split("."))
    right_parts = tuple(int(part) for part in right.split("."))
    if left_parts < right_parts:
        return -1
    if left_parts > right_parts:
        return 1
    return 0


# ---------------------------------------------------------------------------
# Minimal strict JSON-Schema subset validator
# ---------------------------------------------------------------------------

_SUPPORTED_SCHEMA_KEYWORDS = frozenset(
    {
        "$schema", "$id", "title", "description", "definitions",
        "$ref", "type", "required", "properties", "additionalProperties",
        "items", "enum", "const", "pattern", "minLength", "maxLength",
        "minItems", "maxItems", "uniqueItems", "minimum", "maximum",
        "oneOf", "anyOf", "allOf",
    }
)


class SchemaUnsupported(GovernanceError):
    def __init__(self, keyword: str, ref: str):
        super().__init__("schema_keyword_unsupported", "unsupported schema keyword %r" % keyword, ref)


def _json_type_matches(value: object, expected: str) -> bool:
    if expected == "object":
        return isinstance(value, dict)
    if expected == "array":
        return isinstance(value, list)
    if expected == "string":
        return isinstance(value, str)
    if expected == "integer":
        return isinstance(value, int) and not isinstance(value, bool)
    if expected == "number":
        return isinstance(value, (int, float)) and not isinstance(value, bool)
    if expected == "boolean":
        return isinstance(value, bool)
    if expected == "null":
        return value is None
    raise SchemaUnsupported("type", "unknown JSON type %r" % expected)


def validate_json_schema(
    instance: object,
    schema: object,
    *,
    root_schema: typing.Optional[object] = None,
    pointer: str = "$",
) -> typing.List[str]:
    """Validate instance against the documented JSON-Schema subset.

    Returns a list of human-readable findings (empty means valid).  Unsupported
    schema keywords raise SchemaUnsupported so a schema can never silently weaken
    (fail closed).  Format is deliberately not enforced; types are.
    """
    root = root_schema if root_schema is not None else schema
    findings: typing.List[str] = []

    def fail(message: str) -> None:
        findings.append("%s: %s" % (pointer, message))

    if not isinstance(schema, dict):
        raise SchemaUnsupported("schema", "schema node is not an object at %s" % pointer)
    for keyword in schema:
        if keyword not in _SUPPORTED_SCHEMA_KEYWORDS:
            raise SchemaUnsupported(keyword, pointer)

    if "$ref" in schema:
        reference = schema["$ref"]
        if not isinstance(reference, str) or not reference.startswith("#/definitions/"):
            raise SchemaUnsupported("$ref", "only #/definitions/<name> references are supported")
        name = reference[len("#/definitions/"):]
        definitions = root.get("definitions") if isinstance(root, dict) else None
        if not isinstance(definitions, dict) or name not in definitions:
            raise GovernanceError("schema_ref_missing", "unresolved schema reference %r" % reference, pointer)
        findings.extend(validate_json_schema(instance, definitions[name], root_schema=root, pointer=pointer))
        # A $ref may stand beside no other validation keywords in this subset.
        return findings

    if "oneOf" in schema:
        matches = 0
        branch_findings: typing.List[typing.List[str]] = []
        for branch in schema["oneOf"]:
            branch_result = validate_json_schema(instance, branch, root_schema=root, pointer=pointer)
            branch_findings.append(branch_result)
            if not branch_result:
                matches += 1
        if matches != 1:
            fail("value must match exactly one oneOf branch (matched %d)" % matches)
            return findings
        return findings

    if "anyOf" in schema:
        for branch in schema["anyOf"]:
            if not validate_json_schema(instance, branch, root_schema=root, pointer=pointer):
                return findings
        fail("value must match at least one anyOf branch")
        return findings

    if "allOf" in schema:
        for branch in schema["allOf"]:
            findings.extend(validate_json_schema(instance, branch, root_schema=root, pointer=pointer))
        return findings

    if "type" in schema:
        expected = schema["type"]
        expected_types = [expected] if isinstance(expected, str) else list(expected)
        if not any(_json_type_matches(instance, item) for item in expected_types):
            fail("expected type %s" % expected_types)
            return findings
    if "const" in schema and instance != schema["const"]:
        fail("expected const %r" % (schema["const"],))
        return findings
    if "enum" in schema and instance not in schema["enum"]:
        fail("value %r not in enum" % (instance,))
        return findings
    if isinstance(instance, str):
        pattern = schema.get("pattern")
        if isinstance(pattern, str) and re.search(pattern, instance) is None:
            fail("value %r does not match pattern %r" % (instance, pattern))
        if "minLength" in schema and len(instance) < int(schema["minLength"]):
            fail("string shorter than minLength %s" % schema["minLength"])
        if "maxLength" in schema and len(instance) > int(schema["maxLength"]):
            fail("string longer than maxLength %s" % schema["maxLength"])
    if isinstance(instance, (int, float)) and not isinstance(instance, bool):
        if "minimum" in schema and instance < schema["minimum"]:
            fail("number below minimum %s" % schema["minimum"])
        if "maximum" in schema and instance > schema["maximum"]:
            fail("number above maximum %s" % schema["maximum"])
    if isinstance(instance, list):
        if "minItems" in schema and len(instance) < int(schema["minItems"]):
            fail("array shorter than minItems %s" % schema["minItems"])
        if "maxItems" in schema and len(instance) > int(schema["maxItems"]):
            fail("array longer than maxItems %s" % schema["maxItems"])
        if schema.get("uniqueItems") is True:
            seen: typing.Set[str] = set()
            for item in instance:
                key = json.dumps(item, sort_keys=True, ensure_ascii=False)
                if key in seen:
                    fail("array items are not unique")
                    break
                seen.add(key)
        if "items" in schema:
            for index, item in enumerate(instance):
                findings.extend(
                    validate_json_schema(item, schema["items"], root_schema=root, pointer="%s[%d]" % (pointer, index))
                )
    if isinstance(instance, dict):
        required = schema.get("required", [])
        for name in required:
            if name not in instance:
                fail("missing required property %r" % name)
        properties = schema.get("properties", {})
        additional = schema.get("additionalProperties", True)
        for name, value in instance.items():
            child_pointer = "%s.%s" % (pointer, name)
            if isinstance(properties, dict) and name in properties:
                findings.extend(
                    validate_json_schema(value, properties[name], root_schema=root, pointer=child_pointer)
                )
            elif additional is False:
                fail("unknown property %r" % name)
            elif isinstance(additional, dict):
                findings.extend(validate_json_schema(value, additional, root_schema=root, pointer=child_pointer))
    return findings


# ---------------------------------------------------------------------------
# Artifact loading
# ---------------------------------------------------------------------------


def load_schemas(repo_root: Path) -> typing.Dict[str, typing.Dict[str, object]]:
    schemas: typing.Dict[str, typing.Dict[str, object]] = {}
    for kind, relpath in SCHEMA_RELPATHS.items():
        document = read_repo_json(repo_root, relpath)
        if not isinstance(document, dict):
            raise GovernanceError("invalid_schema", "schema file is not a JSON object", relpath)
        for keyword in ("$schema", "$id", "title", "description", "type", "definitions", "properties"):
            if keyword not in document:
                raise GovernanceError("invalid_schema", "schema is missing %r" % keyword, relpath)
        schemas[kind] = document
    return schemas


def load_inventory(repo_root: Path) -> typing.Dict[str, object]:
    data = read_repo_bytes(repo_root, INVENTORY_RELPATH)
    if len(data) != INVENTORY_BYTES:
        raise GovernanceError("inventory_bytes_mismatch", "inventory bytes changed: %d" % len(data), INVENTORY_RELPATH)
    if sha256_upper(data) != INVENTORY_SHA256:
        raise GovernanceError("inventory_sha256_mismatch", "inventory SHA-256 changed", INVENTORY_RELPATH)
    if count_lf(data) != INVENTORY_LF:
        raise GovernanceError("inventory_lf_mismatch", "inventory LF count changed", INVENTORY_RELPATH)
    document = json.loads(data.decode("utf-8"))
    if not isinstance(document, dict):
        raise GovernanceError("invalid_inventory", "inventory is not a JSON object", INVENTORY_RELPATH)
    return typing.cast(typing.Dict[str, object], document)


def load_projection(repo_root: Path) -> typing.Dict[str, object]:
    document = read_repo_json(repo_root, PROJECTION_RELPATH)
    if not isinstance(document, dict):
        raise GovernanceError("invalid_projection", "rule projection is not a JSON object", PROJECTION_RELPATH)
    return typing.cast(typing.Dict[str, object], document)


def load_contract(repo_root: Path) -> typing.Tuple[typing.Dict[str, object], bytes]:
    data = read_repo_bytes(repo_root, CONTRACT_RELPATH)
    try:
        document = json.loads(data.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise GovernanceError("invalid_contract_json", "contract is not valid UTF-8 JSON: %s" % error, CONTRACT_RELPATH) from error
    if not isinstance(document, dict):
        raise GovernanceError("invalid_contract", "contract is not a JSON object", CONTRACT_RELPATH)
    return typing.cast(typing.Dict[str, object], document), data


def load_source_identity(repo_root: Path) -> typing.Dict[str, object]:
    source = read_repo_json(repo_root, SOURCE_RELPATH)
    if not isinstance(source, dict):
        raise GovernanceError("invalid_source", "source identity is not a JSON object", SOURCE_RELPATH)
    extra = sorted(set(source) - {"repository", "commit", "tree", "note"})
    if extra:
        raise GovernanceError("source_unknown_field", "unknown source field(s): %s" % ", ".join(extra))
    repository = source.get("repository")
    if not isinstance(repository, str) or not re.match(r"^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$", repository):
        raise GovernanceError("source_repository", "repository must be owner/name form")
    for key in ("commit", "tree"):
        value = source.get(key)
        if not isinstance(value, str) or not HEX40_RE.match(value):
            raise GovernanceError("source_" + key, "%s must be 40 lowercase hex characters" % key)
    if "note" in source and not isinstance(source["note"], str):
        raise GovernanceError("source_note", "note must be a string when present")
    result: typing.Dict[str, object] = {
        "repository": repository,
        "commit": source["commit"],
        "tree": source["tree"],
    }
    if source.get("note"):
        result["note"] = source["note"]
    return result


def load_dependencies_input(repo_root: Path) -> typing.List[typing.Dict[str, object]]:
    document = read_repo_json(repo_root, DEPENDENCIES_RELPATH)
    if not isinstance(document, list):
        raise GovernanceError("dependencies_invalid", "governance dependency input must be an array")
    for position, edge in enumerate(document):
        if not isinstance(edge, dict):
            raise GovernanceError("dependency_invalid", "dependency %d is not an object" % position)
        allowed = {"from", "to", "class", "rule"}
        extra = sorted(set(edge) - allowed)
        if extra:
            raise GovernanceError("dependency_unknown_field", "unknown dependency field(s): %s" % ", ".join(extra))
        if edge.get("class") not in DEPENDENCY_CLASS_SET:
            raise GovernanceError("dependency_class", "unknown dependency class", str(edge.get("from")))
    return typing.cast(typing.List[typing.Dict[str, object]], document)


def load_manifest_binding(repo_root: Path) -> typing.Dict[str, object]:
    """Digest of the committed packaging manifest (identity only; never approval)."""
    data = read_repo_bytes(repo_root, MANIFEST_RELPATH)
    return {
        "manifest_path": MANIFEST_RELPATH,
        "manifest_bytes": len(data),
        "manifest_lf": count_lf(data),
        "manifest_sha256": sha256_upper(data),
    }


# ---------------------------------------------------------------------------
# Rule projection: derivation, validation and deterministic render
# ---------------------------------------------------------------------------


def _doc_id_table(projection: typing.Dict[str, object]) -> typing.Dict[str, str]:
    table: typing.Dict[str, str] = {}
    for row in typing.cast(typing.List[typing.Dict[str, object]], projection.get("document_ids") or []):
        if not isinstance(row, dict) or set(row) != {"path", "doc_id"}:
            raise GovernanceError("invalid_projection", "document_ids rows are {path, doc_id}")
        path = row["path"]
        doc_id = row["doc_id"]
        if not isinstance(path, str) or not isinstance(doc_id, str):
            raise GovernanceError("invalid_projection", "document_ids rows must be strings")
        if path in table:
            raise GovernanceError("duplicate_document_path", "duplicate document path", path)
        table[path] = doc_id
    return table


def _source_table(projection: typing.Dict[str, object]) -> typing.Dict[str, typing.Dict[str, typing.List[str]]]:
    source_table = projection.get("source_to_doc_id")
    if not isinstance(source_table, dict):
        raise GovernanceError("invalid_projection", "source_to_doc_id must be an object")
    return typing.cast(typing.Dict[str, typing.Dict[str, typing.List[str]]], source_table)


def source_document_of(rule: typing.Dict[str, object], projection: typing.Dict[str, object]) -> str:
    source = rule.get("source")
    if not isinstance(source, str):
        raise GovernanceError("invalid_inventory_rule", "rule source is not a string", str(rule.get("id")))
    entry = _source_table(projection).get(source)
    if not isinstance(entry, dict) or "primary" not in entry:
        raise GovernanceError(
            "unmapped_rule_source",
            "no committed source_to_doc_id mapping for this inventory source (no default is applied)",
            source,
        )
    primary = entry["primary"]
    if not isinstance(primary, str):
        raise GovernanceError("invalid_projection", "primary must be a doc_id string", source)
    return primary


def all_doc_ids_of(rule: typing.Dict[str, object], projection: typing.Dict[str, object]) -> typing.List[str]:
    source = rule.get("source")
    entry = _source_table(projection).get(typing.cast(str, source))
    if not isinstance(entry, dict):
        raise GovernanceError("unmapped_rule_source", "no committed source mapping", str(source))
    values = entry.get("all")
    if not isinstance(values, list) or not values:
        raise GovernanceError("invalid_projection", "source mapping needs a non-empty 'all' list", str(source))
    return typing.cast(typing.List[str], values)


def applies_to_roles_of(rule: typing.Dict[str, object], projection: typing.Dict[str, object]) -> typing.List[str]:
    role_mapping = projection.get("role_mapping")
    if not isinstance(role_mapping, dict):
        raise GovernanceError("invalid_projection", "role_mapping must be an object")
    base_by_class = role_mapping.get("base_by_class")
    overrides = role_mapping.get("overrides") or {}
    if not isinstance(base_by_class, dict) or not isinstance(overrides, dict):
        raise GovernanceError("invalid_projection", "role_mapping needs base_by_class and overrides objects")
    rule_class = rule.get("cls")
    if not isinstance(rule_class, str) or rule_class not in base_by_class:
        raise GovernanceError(
            "unmapped_role_combination",
            "no committed role mapping for this class (an unmapped combination fails the build)",
            str(rule.get("id")),
        )
    roles = overrides.get(typing.cast(str, rule.get("id")), base_by_class[rule_class])
    if not isinstance(roles, list) or not roles or any(role not in ROLE_SET for role in roles):
        raise GovernanceError("invalid_projection", "invalid applies_to_roles value", str(rule.get("id")))
    return typing.cast(typing.List[str], list(roles))


def authority_action_of(rule: typing.Dict[str, object]) -> bool:
    return rule.get("cls") == "action-permission"


def _enforcement_spec(projection: typing.Dict[str, object]) -> typing.Dict[str, object]:
    classifier = projection.get("enforcement_classifier")
    if not isinstance(classifier, dict):
        raise GovernanceError("invalid_projection", "enforcement_classifier must be an object")
    for key in (
        "version",
        "classes",
        "guidance_prefixes",
        "required_keywords",
        "host_keywords",
        "structural_keywords",
        "default_class",
        "guidance_ref",
        "unnamed_ref",
        "surface_patterns",
    ):
        if key not in classifier:
            raise GovernanceError("invalid_projection", "enforcement_classifier is missing %r" % key)
    if not isinstance(classifier["classes"], list) or set(classifier["classes"]) != ENFORCEMENT_CLASS_SET:
        raise GovernanceError("invalid_projection", "classifier classes must be the closed enforcement class set")
    if classifier["default_class"] not in ENFORCEMENT_CLASS_SET:
        raise GovernanceError("invalid_projection", "classifier default_class is not a closed class")
    return classifier


def classify_enforcement(
    enforce_text: object,
    projection: typing.Dict[str, object],
) -> typing.Tuple[str, str]:
    """Deterministic closed classifier over the inventory's Enforcement text.

    Precedence (documented in the design page): a leading procedural/negative
    marker means GUIDANCE-ONLY; then required-context language means CI-REQUIRED;
    then host-enforcement language means HOST-ENFORCED; then structural-check
    language means CI-STRUCTURAL; otherwise GUIDANCE-ONLY.  The classification is
    descriptive of the inventory's own text and is not a complete-enforcement
    claim.
    """
    classifier = _enforcement_spec(projection)
    text = enforce_text if isinstance(enforce_text, str) else ""
    lowered = text.lower()
    overrides = projection.get("enforcement_overrides") or []
    if isinstance(overrides, list):
        for override in overrides:
            if not isinstance(override, dict):
                raise GovernanceError("invalid_projection", "enforcement override must be an object")
            rule_id = override.get("rule_id")
            if rule_id is None:
                continue
            # Overrides are applied by the caller (rule_id-aware); unreachable here.
            del rule_id
    prefixes = [str(prefix).lower() for prefix in typing.cast(typing.List[object], classifier["guidance_prefixes"])]
    for prefix in prefixes:
        if lowered.lstrip().startswith(prefix):
            return classifier["default_class"], classifier["guidance_ref"]
    for keyword in typing.cast(typing.List[str], classifier["required_keywords"]):
        if str(keyword).lower() in lowered:
            return "CI-REQUIRED", _surface_ref(text, classifier, required=True)
    for keyword in typing.cast(typing.List[str], classifier["host_keywords"]):
        if str(keyword).lower() in lowered:
            return "HOST-ENFORCED", _surface_ref(text, classifier, required=False)
    for keyword in typing.cast(typing.List[str], classifier["structural_keywords"]):
        if str(keyword).lower() in lowered:
            return "CI-STRUCTURAL", _surface_ref(text, classifier, required=False)
    return classifier["default_class"], classifier["guidance_ref"]


def _surface_ref(text: str, classifier: typing.Dict[str, object], *, required: bool) -> str:
    del required
    lowered = text.lower()
    for row in typing.cast(typing.List[typing.Dict[str, object]], classifier["surface_patterns"]):
        token = row.get("token")
        ref = row.get("ref")
        if isinstance(token, str) and isinstance(ref, str) and token.lower() in lowered:
            return ref
    return typing.cast(str, classifier["unnamed_ref"])


def derive_rule_fields(
    rule: typing.Dict[str, object],
    projection: typing.Dict[str, object],
) -> typing.Dict[str, object]:
    enforcement_class, enforcement_ref = classify_enforcement(rule.get("enforce"), projection)
    overrides = projection.get("enforcement_overrides") or []
    if isinstance(overrides, list):
        for override in overrides:
            if isinstance(override, dict) and override.get("rule_id") == rule.get("id"):
                enforcement_class = override.get("class")
                enforcement_ref = override.get("ref")
                break
    if enforcement_class not in ENFORCEMENT_CLASS_SET:
        raise GovernanceError("invalid_projection", "override produced an unknown enforcement class", str(rule.get("id")))
    if not isinstance(enforcement_ref, str) or not enforcement_ref:
        raise GovernanceError("invalid_projection", "enforcement_ref must be a non-empty string", str(rule.get("id")))
    return {
        "source_document": source_document_of(rule, projection),
        "applies_to_roles": applies_to_roles_of(rule, projection),
        "authority_action": authority_action_of(rule),
        "enforcement_class": enforcement_class,
        "enforcement_ref": enforcement_ref,
    }


def derive_projection_output(
    inventory: typing.Dict[str, object],
    projection: typing.Dict[str, object],
) -> typing.Dict[str, object]:
    """Compute the committed derived output for every inventory rule."""
    rules = inventory.get("rules")
    if not isinstance(rules, list) or len(rules) != 187:
        raise GovernanceError("invalid_inventory", "inventory rules must be an array of 187 records")
    derived_rules: typing.Dict[str, typing.Dict[str, object]] = {}
    for rule in rules:
        if not isinstance(rule, dict):
            raise GovernanceError("invalid_inventory", "inventory rule is not an object")
        rule_id = rule.get("id")
        if not isinstance(rule_id, str):
            raise GovernanceError("invalid_inventory", "inventory rule has no id")
        if rule_id in derived_rules:
            raise GovernanceError("duplicate_rule_id", "duplicate inventory rule id", rule_id)
        derived_rules[rule_id] = derive_rule_fields(rule, projection)
    return {
        "classifier_version": typing.cast(typing.Dict[str, object], projection["enforcement_classifier"])["version"],
        "rules": {rule_id: derived_rules[rule_id] for rule_id in sorted(derived_rules)},
    }


def validate_projection_document(
    projection: typing.Dict[str, object],
    inventory: typing.Dict[str, object],
) -> typing.List[str]:
    findings: typing.List[str] = []
    if projection.get("schema") != RULE_PROJECTION_SCHEMA_ID:
        findings.append("schema must be exactly %r" % RULE_PROJECTION_SCHEMA_ID)
    if projection.get("contract_id") != CONTRACT_ID:
        findings.append("contract_id must be exactly %r" % CONTRACT_ID)
    if not isinstance(projection.get("projection_version"), str) or not SEMVER_RE.match(
        typing.cast(str, projection.get("projection_version"))
    ):
        findings.append("projection_version must be SemVer")
    document_ids = _doc_id_table(projection)
    authoritative_paths = {
        row["path"]
        for row in typing.cast(typing.List[typing.Dict[str, object]], inventory.get("authoritative_set") or [])
        if isinstance(row, dict) and isinstance(row.get("path"), str)
    }
    if set(document_ids) != authoritative_paths:
        missing = sorted(authoritative_paths - set(document_ids))
        extra = sorted(set(document_ids) - authoritative_paths)
        findings.append("document_ids must be a total mapping over the authoritative set; missing=%s extra=%s" % (missing, extra))
    inventory_record = projection.get("inventory")
    if not isinstance(inventory_record, dict):
        findings.append("inventory identity record is missing")
    else:
        if inventory_record.get("sha256") != INVENTORY_SHA256:
            findings.append("projection inventory sha256 does not match the pinned committed identity")
        if inventory_record.get("bytes") != INVENTORY_BYTES:
            findings.append("projection inventory bytes does not match the pinned committed identity")
        if inventory_record.get("lf") != INVENTORY_LF:
            findings.append("projection inventory lf does not match the pinned committed identity")
        if inventory_record.get("path") != INVENTORY_RELPATH:
            findings.append("projection inventory path must be %r" % INVENTORY_RELPATH)
        source_raw = inventory_record.get("source_raw")
        if not isinstance(source_raw, dict):
            findings.append("projection must record the raw task-33 source identity beside the committed identity")
        else:
            for key in ("bytes", "lf", "cr", "sha256"):
                if source_raw.get(key) != INVENTORY_SOURCE_RAW[key]:
                    findings.append("projection inventory source_raw.%s does not match the recorded task-33 identity" % key)
        if inventory_record.get("normalization") != INVENTORY_NORMALIZATION:
            findings.append("projection inventory normalization note is missing or wrong")
    rules = typing.cast(typing.List[typing.Dict[str, object]], inventory.get("rules") or [])
    inventory_sources = sorted({str(rule.get("source")) for rule in rules if isinstance(rule, dict)})
    source_table = _source_table(projection)
    mapped_sources = sorted(source_table)
    if inventory_sources != mapped_sources:
        findings.append(
            "source_to_doc_id must be a total, no-default mapping over the inventory sources; "
            "missing=%s extra=%s"
            % (sorted(set(inventory_sources) - set(mapped_sources)), sorted(set(mapped_sources) - set(inventory_sources)))
        )
    known_doc_ids = set(document_ids.values())
    for source, entry in source_table.items():
        if not isinstance(entry, dict) or not isinstance(entry.get("all"), list) or not entry["all"]:
            findings.append("source mapping %r needs a non-empty all list" % source)
            continue
        for doc_id in entry["all"]:
            if doc_id not in known_doc_ids:
                findings.append("source mapping %r names unknown doc_id %r" % (source, doc_id))
        if entry.get("primary") != entry["all"][0]:
            findings.append("source mapping %r primary must be the first listed document" % source)
    rules_by_id = {str(rule.get("id")): rule for rule in rules if isinstance(rule, dict)}
    role_mapping = projection.get("role_mapping")
    if not isinstance(role_mapping, dict) or not isinstance(role_mapping.get("base_by_class"), dict):
        findings.append("role_mapping.base_by_class is missing")
    else:
        base_by_class = typing.cast(typing.Dict[str, object], role_mapping["base_by_class"])
        overrides = role_mapping.get("overrides") or {}
        if isinstance(overrides, dict):
            for rule_id in overrides:
                if rule_id not in rules_by_id:
                    findings.append("role override names unknown rule %r" % rule_id)
        for rule in rules:
            if isinstance(rule, dict) and rule.get("cls") not in base_by_class:
                findings.append("role_mapping has no base class %r (unmapped combination)" % rule.get("cls"))
                break
    classifier = projection.get("enforcement_classifier")
    if not isinstance(classifier, dict):
        findings.append("enforcement_classifier is missing")
    else:
        try:
            _enforcement_spec(projection)
        except GovernanceError as error:
            findings.append(str(error))
    conflicts = projection.get("conflict_rule_ids")
    if not isinstance(conflicts, dict):
        findings.append("conflict_rule_ids must be an object")
    else:
        inventory_conflicts = {
            str(conflict.get("id"))
            for conflict in typing.cast(typing.List[typing.Dict[str, object]], inventory.get("conflicts") or [])
            if isinstance(conflict, dict)
        }
        if set(conflicts) != inventory_conflicts:
            findings.append("conflict_rule_ids must map exactly the inventory conflicts")
        for conflict_id, rule_ids in conflicts.items():
            if not isinstance(rule_ids, list):
                findings.append("conflict_rule_ids[%r] must be an array" % conflict_id)
                continue
            for rule_id in rule_ids:
                if rule_id not in rules_by_id:
                    findings.append("conflict %r names unknown rule %r" % (conflict_id, rule_id))
    derived = projection.get("derived")
    expected = derive_projection_output(inventory, projection)
    if derived != expected:
        findings.append("committed derived projection output is not byte-equal to a fresh re-derivation")
    return findings


def render_projection_bytes(repo_root: Path) -> bytes:
    inventory = load_inventory(repo_root)
    projection = load_projection(repo_root)
    document = dict(projection)
    document["derived"] = derive_projection_output(inventory, projection)
    findings = validate_projection_document(document, inventory)
    if findings:
        raise GovernanceError("projection_invalid", "; ".join(findings))
    return canonical_bytes(document)


# ---------------------------------------------------------------------------
# Documents, conflicts and the contract document
# ---------------------------------------------------------------------------


def _authoritative_set(inventory: typing.Dict[str, object]) -> typing.List[typing.Dict[str, object]]:
    rows = inventory.get("authoritative_set")
    if not isinstance(rows, list):
        raise GovernanceError("invalid_inventory", "authoritative_set must be an array")
    return [typing.cast(typing.Dict[str, object], row) for row in rows if isinstance(row, dict)]


def _inventory_identities(inventory: typing.Dict[str, object]) -> typing.Dict[str, typing.Dict[str, object]]:
    rows = inventory.get("identities")
    if not isinstance(rows, list):
        raise GovernanceError("invalid_inventory", "identities must be an array")
    table: typing.Dict[str, typing.Dict[str, object]] = {}
    for row in rows:
        if isinstance(row, dict) and isinstance(row.get("path"), str):
            table[typing.cast(str, row["path"])] = typing.cast(typing.Dict[str, object], row)
    return table


def build_documents(
    inventory: typing.Dict[str, object],
    projection: typing.Dict[str, object],
    repo_root: Path,
) -> typing.List[typing.Dict[str, object]]:
    """Build the document records: identities verified against the checkout.

    Bytes/LF/SHA-256 are direct inventory fields (the inventory measured the same
    base); the build re-derives them from the checkout so a drift is refused, not
    silently re-bound.
    """
    path_to_doc = _doc_id_table(projection)
    identities = _inventory_identities(inventory)
    citations: typing.Dict[str, typing.Set[str]] = {doc_id: set() for doc_id in path_to_doc.values()}
    rules = typing.cast(typing.List[typing.Dict[str, object]], inventory.get("rules") or [])
    for rule in rules:
        if not isinstance(rule, dict):
            continue
        rule_id = str(rule.get("id"))
        for doc_id in all_doc_ids_of(rule, projection):
            if doc_id not in citations:
                raise GovernanceError("invalid_projection", "source mapping names unknown doc_id", doc_id)
            citations[doc_id].add(rule_id)
    authoritative = _authoritative_set(inventory)
    if len(authoritative) != 27:
        raise GovernanceError("invalid_inventory", "authoritative_set must contain exactly 27 documents")
    documents: typing.List[typing.Dict[str, object]] = []
    for row in sorted(authoritative, key=lambda item: path_to_doc.get(str(item.get("path")), "")):
        path = row.get("path")
        tier = row.get("tier")
        if not isinstance(path, str) or tier not in ("T1", "T2", "T3"):
            raise GovernanceError("invalid_inventory", "authoritative-set row is malformed")
        if path not in path_to_doc:
            raise GovernanceError("invalid_projection", "authoritative-set path has no doc_id", path)
        doc_id = path_to_doc[path]
        if doc_id not in DOCUMENT_ROLE_SCOPE or doc_id not in DOCUMENT_AUTHORITY_CLASS:
            raise GovernanceError("missing_document_metadata", "no committed metadata for doc_id", doc_id)
        identity = identities.get(path)
        if identity is None:
            raise GovernanceError("invalid_inventory", "no measured identity for authoritative document", path)
        actual = file_identity(repo_root, path)
        for field in ("bytes", "lf"):
            if identity.get(field) != actual[field]:
                raise GovernanceError(
                    "document_identity_mismatch",
                    "inventory %s for %s is %r but the checkout has %r" % (field, path, identity.get(field), actual[field]),
                    path,
                )
        expected_sha = identity.get("sha256")
        if not isinstance(expected_sha, str) or expected_sha.lower() != actual["sha256"].lower():
            raise GovernanceError(
                "document_identity_mismatch",
                "inventory sha256 for %s does not match the checkout bytes" % path,
                path,
            )
        documents.append(
            {
                "doc_id": doc_id,
                "path": path,
                "role_scope": list(DOCUMENT_ROLE_SCOPE[doc_id]),
                "tier": tier,
                "bytes": actual["bytes"],
                "lf": actual["lf"],
                "sha256": typing.cast(str, actual["sha256"]),
                "authority_class": DOCUMENT_AUTHORITY_CLASS[doc_id],
                "lifecycle": {
                    "state": "effective",
                    "effective_from": DOCUMENT_EFFECTIVE_FROM,
                    "superseded_by": None,
                },
                "read_depth": "full",
                "citations": sorted(citations[doc_id]),
            }
        )
    documents.sort(key=lambda item: str(item["doc_id"]))
    if len(documents) != 27:
        raise GovernanceError("invalid_inventory", "document set is not 27 records")
    return documents


_DOC_EVIDENCE_PATH_RE = re.compile(r"([A-Za-z0-9_][A-Za-z0-9_./-]*\.(?:md|yml|yaml|json|txt))(?=:[0-9])")


def build_conflicts(
    inventory: typing.Dict[str, object],
    projection: typing.Dict[str, object],
) -> typing.List[typing.Dict[str, object]]:
    """Document-level conflict records derived from the inventory.

    The inventory attributes conflicts to documents/anchors, not to rules, so a
    committed conflict records the documents it names and an empty rule_ids list
    unless the projection's conflict_rule_ids attaches rules (it attaches none in
    v1).  A rule-level conflict, when supplied, blocks resolution deterministically.
    """
    path_to_doc = _doc_id_table(projection)
    conflict_rule_ids = projection.get("conflict_rule_ids") or {}
    if not isinstance(conflict_rule_ids, dict):
        raise GovernanceError("invalid_projection", "conflict_rule_ids must be an object")
    rules = typing.cast(typing.List[typing.Dict[str, object]], inventory.get("rules") or [])
    known_rule_ids = {str(rule.get("id")) for rule in rules if isinstance(rule, dict)}
    conflicts: typing.List[typing.Dict[str, object]] = []
    inventory_conflicts = inventory.get("conflicts")
    if not isinstance(inventory_conflicts, list):
        raise GovernanceError("invalid_inventory", "conflicts must be an array")
    for conflict in inventory_conflicts:
        if not isinstance(conflict, dict):
            raise GovernanceError("invalid_inventory", "conflict is not an object")
        conflict_id = str(conflict.get("id"))
        raw_status = str(conflict.get("status") or "")
        if raw_status.upper().startswith("UNRUN"):
            status = "UNRUN"
        elif raw_status.upper().startswith("UNRESOLVED"):
            status = "UNRESOLVED"
        else:
            raise GovernanceError("unsupported_conflict_status", "unrecognized inventory conflict status", conflict_id)
        documents: typing.Set[str] = set()
        for evidence in typing.cast(typing.List[object], conflict.get("evidence") or []):
            if not isinstance(evidence, str):
                continue
            for match in _DOC_EVIDENCE_PATH_RE.findall(evidence):
                candidate = match.replace("\\", "/")
                if candidate in path_to_doc:
                    documents.add(path_to_doc[candidate])
        rule_ids = conflict_rule_ids.get(conflict_id, [])
        if not isinstance(rule_ids, list):
            raise GovernanceError("invalid_projection", "conflict_rule_ids value must be an array", conflict_id)
        for rule_id in rule_ids:
            if rule_id not in known_rule_ids:
                raise GovernanceError("invalid_projection", "conflict names unknown rule", str(rule_id))
        conflicts.append(
            {
                "conflict_id": conflict_id,
                "title": str(conflict.get("title")),
                "status": status,
                "documents": sorted(documents),
                "rule_ids": sorted(str(rule_id) for rule_id in rule_ids),
                "resolution_owner": str(conflict.get("resolution_owner")),
            }
        )
    conflicts.sort(key=lambda item: (len(str(item["conflict_id"])), str(item["conflict_id"])))
    return conflicts


def build_rule_applicability(
    inventory: typing.Dict[str, object],
    projection: typing.Dict[str, object],
) -> typing.List[typing.Dict[str, object]]:
    derived = derive_projection_output(inventory, projection)["rules"]
    records: typing.List[typing.Dict[str, object]] = []
    for rule in sorted(
        typing.cast(typing.List[typing.Dict[str, object]], inventory["rules"]),
        key=lambda item: str(item.get("id")),
    ):
        if not isinstance(rule, dict):
            raise GovernanceError("invalid_inventory", "inventory rule is not an object")
        rule_id = str(rule["id"])
        consumer = rule.get("consumer")
        if not isinstance(consumer, dict):
            raise GovernanceError("invalid_inventory", "rule has no consumer object", rule_id)
        fields = derived[rule_id]
        records.append(
            {
                "rule_id": rule_id,
                "anchor": str(rule["anchor"]),
                "class": str(rule["cls"]),
                "dimension": str(rule["dim"]),
                "lifecycle": str(rule["lifecycle"]),
                "adoption_status": str(consumer["adoption_status"]),
                "consumer_effect": str(consumer.get("effect") or ""),
                "source_document": fields["source_document"],
                "applies_to_roles": list(fields["applies_to_roles"]),
                "authority_action": bool(fields["authority_action"]),
                "enforcement_class": fields["enforcement_class"],
                "enforcement_ref": fields["enforcement_ref"],
            }
        )
    return records


def build_contract_document(
    repo_root: Path,
    *,
    inventory: typing.Optional[typing.Dict[str, object]] = None,
    projection: typing.Optional[typing.Dict[str, object]] = None,
    source: typing.Optional[typing.Dict[str, object]] = None,
    previous_contract: typing.Optional[typing.Dict[str, object]] = None,
) -> typing.Dict[str, object]:
    inventory = inventory if inventory is not None else load_inventory(repo_root)
    projection = projection if projection is not None else load_projection(repo_root)
    source = source if source is not None else load_source_identity(repo_root)
    projection_findings = validate_projection_document(projection, inventory)
    if projection_findings:
        raise GovernanceError("projection_invalid", "; ".join(projection_findings))
    documents = build_documents(inventory, projection, repo_root)
    if previous_contract is not None:
        previous_version = previous_contract.get("contract_version")
        if not isinstance(previous_version, str):
            raise GovernanceError("invalid_previous_contract", "previous contract has no contract_version")
        if documents != previous_contract.get("documents"):
            if compare_semver(CONTRACT_VERSION, previous_version) <= 0:
                raise GovernanceError(
                    "contract_version_bump_required",
                    "a bound document changed but contract_version did not increase "
                    "(re-generation requires a contract_version bump)",
                    CONTRACT_RELPATH,
                )
    contract: typing.Dict[str, object] = {
        "schema": CONTRACT_SCHEMA_ID,
        "contract_id": CONTRACT_ID,
        "contract_version": CONTRACT_VERSION,
        "source": {
            "repository": source["repository"],
            "commit": source["commit"],
            "tree": source["tree"],
            "generated_by": {"tool": TOOL_NAME, "version": TOOL_VERSION},
        },
        "summary": SUMMARY,
        "roles": {role_id: dict(profile) for role_id, profile in ROLE_PROFILES.items()},
        "documents": documents,
        "entry_routes": [dict(route) for route in ENTRY_ROUTES],
        "dependency_graph": [dict(edge) for edge in DEPENDENCY_GRAPH],
        "rule_applicability": build_rule_applicability(inventory, projection),
        "conflicts": build_conflicts(inventory, projection),
        "lifecycle": dict(LIFECYCLE),
        "local_adoption": dict(LOCAL_ADOPTION),
        "host_boundary": json.loads(json.dumps(HOST_BOUNDARY)),
        "enforcement_claims": json.loads(json.dumps(ENFORCEMENT_CLAIMS)),
        "trust": dict(TRUST),
        "non_claims": list(NON_CLAIMS),
    }
    schemas = load_schemas(repo_root)
    findings = validate_json_schema(contract, schemas["contract"], root_schema=schemas["contract"])
    if findings:
        raise GovernanceError("contract_schema_invalid", "; ".join(findings[:10]))
    return contract


def render_contract_bytes(repo_root: Path) -> bytes:
    previous: typing.Optional[typing.Dict[str, object]] = None
    try:
        previous, _ = load_contract(repo_root)
    except GovernanceError:
        previous = None
    contract = build_contract_document(repo_root, previous_contract=previous)
    return canonical_bytes(contract)


# ---------------------------------------------------------------------------
# Skill packaging metadata (tools/governance-dependencies.json)
# ---------------------------------------------------------------------------

_MANUAL_ONLY_DESCRIPTION_PREFIX = "MANUAL-ONLY"


def scan_skill_entrypoints(repo_root: Path) -> typing.List[typing.Dict[str, object]]:
    """Scan the shipped skill entrypoints deterministically (directory order).

    The template directory is not a shipped skill.  The manual-only marker is the
    skill's own description prefix, the repository's established convention; it is
    read, never inferred from a list.
    """
    skills_root = repo_path(repo_root, SKILLS_DIR)
    if not skills_root.is_dir():
        raise GovernanceError("skills_root_missing", "skill directory is missing", SKILLS_DIR)
    entries: typing.List[typing.Dict[str, object]] = []
    for directory in sorted(skills_root.iterdir(), key=lambda item: item.name):
        if not directory.is_dir() or directory.name == SKILL_TEMPLATE_DIR:
            continue
        entrypoint = directory / SKILL_ENTRYPOINT_NAME
        if not entrypoint.is_file():
            continue
        data = entrypoint.read_bytes()
        manual_only = _skill_manual_only(data)
        entries.append(
            {
                "name": directory.name,
                "path": "%s/%s/%s" % (SKILLS_DIR, directory.name, SKILL_ENTRYPOINT_NAME),
                "manual_only": manual_only,
            }
        )
    names = [entry["name"] for entry in entries]
    if len(set(names)) != len(names):
        raise GovernanceError("duplicate_skill_name", "duplicate shipped skill name")
    return entries


def _skill_manual_only(data: bytes) -> bool:
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError:
        return False
    lines = text.splitlines()[:40]
    for index, line in enumerate(lines):
        if line.strip() != "---":
            continue
        for body_line in lines[index + 1:]:
            stripped = body_line.strip()
            if stripped == "---":
                return False
            if stripped.lower().startswith("description:"):
                value = stripped[len("description:"):].strip().strip("'\"")
                return value.upper().startswith(_MANUAL_ONLY_DESCRIPTION_PREFIX)
        return False
    return False


def build_governance_dependencies_document(
    repo_root: Path,
    contract_document: typing.Dict[str, object],
) -> typing.Dict[str, object]:
    contract_bytes = canonical_bytes(contract_document)
    contract_sha = sha256_upper(contract_bytes)
    skills = scan_skill_entrypoints(repo_root)
    required_skill_ids = sorted(
        {
            edge["from_node"].split(":", 1)[1]
            for edge in DEPENDENCY_GRAPH
            if edge["from_node"].startswith("skill:")
        }
    )
    entrypoints: typing.List[typing.Dict[str, object]] = []
    for skill in skills:
        required = skill["name"] in required_skill_ids
        entrypoints.append(
            {
                "name": skill["name"],
                "path": skill["path"],
                "dependency_class": "required" if required else "optional",
                "manual_only": bool(skill["manual_only"]),
                "contract": {
                    "id": CONTRACT_ID,
                    "accepted_versions": [CONTRACT_VERSION],
                    "expected_sha256_when_bundled": contract_sha,
                },
                "export_closure_rule": (
                    "required: a standalone export must include the contract and the role-scoped "
                    "required documents and pass the distributed-payload closure check; an export "
                    "missing a required governance edge is rejected"
                    if required
                    else "optional: the export may omit the contract only if it makes no governance "
                    "coverage claim; an absent dependency may never be reported as none"
                ),
            }
        )
    document: typing.Dict[str, object] = {
        "schema": GOVERNANCE_DEPENDENCIES_SCHEMA_ID,
        "contract": {"id": CONTRACT_ID, "version": CONTRACT_VERSION, "sha256": contract_sha},
        "generator": {"tool": TOOL_NAME, "version": TOOL_VERSION},
        "declared_rule": (
            "generated deterministically by tools.aegis_preflight.governance from the shipped skill "
            "entrypoints (directory scan, sorted) and the contract bytes; no timestamps; the "
            "manual_only flag is the skill description's own MANUAL-ONLY marker; dependency_class "
            "is 'required' exactly for skill entrypoints named in the contract dependency graph"
        ),
        "entrypoints": entrypoints,
        "non_claims": [
            "this declaration is packaging metadata, not a second policy or a gate",
            "an 'optional' declaration does not mean the contract is irrelevant; it means the export is not rejected without it while the skill makes no governance-coverage claim",
            "the expected contract sha256 binds the declaration to one contract build; a different contract version requires a new declaration",
        ],
    }
    validate_governance_dependencies_document(document, contract_document)
    return document


def validate_governance_dependencies_document(
    document: typing.Dict[str, object],
    contract_document: typing.Dict[str, object],
) -> typing.List[str]:
    findings: typing.List[str] = []
    if document.get("schema") != GOVERNANCE_DEPENDENCIES_SCHEMA_ID:
        findings.append("schema must be exactly %r" % GOVERNANCE_DEPENDENCIES_SCHEMA_ID)
    contract = document.get("contract")
    if not isinstance(contract, dict):
        findings.append("contract binding is missing")
    else:
        if contract.get("id") != CONTRACT_ID:
            findings.append("contract.id mismatch")
        if contract.get("version") != contract_document.get("contract_version"):
            findings.append("contract.version does not match the contract document")
        expected_sha = sha256_upper(canonical_bytes(contract_document))
        if contract.get("sha256") != expected_sha:
            findings.append("contract.sha256 does not match the contract bytes")
    entrypoints = document.get("entrypoints")
    if not isinstance(entrypoints, list):
        findings.append("entrypoints must be an array")
        return findings
    if not entrypoints:
        findings.append("entrypoints must not be empty")
    names: typing.Set[str] = set()
    for entry in entrypoints:
        if not isinstance(entry, dict):
            findings.append("entrypoint is not an object")
            continue
        name = entry.get("name")
        if not isinstance(name, str) or not name:
            findings.append("entrypoint name is missing")
            continue
        if name in names:
            findings.append("duplicate entrypoint name %r" % name)
        names.add(name)
        path = entry.get("path")
        if not isinstance(path, str) or not path.endswith("/" + SKILL_ENTRYPOINT_NAME):
            findings.append("entrypoint path must end with %r (name %r)" % (SKILL_ENTRYPOINT_NAME, name))
        if entry.get("dependency_class") not in ("required", "optional"):
            findings.append("entrypoint %r has no valid dependency_class" % name)
        if not isinstance(entry.get("manual_only"), bool):
            findings.append("entrypoint %r has no boolean manual_only" % name)
        contract_entry = entry.get("contract")
        if not isinstance(contract_entry, dict):
            findings.append("entrypoint %r has no contract binding" % name)
            continue
        if contract_entry.get("expected_sha256_when_bundled") != (contract.get("sha256") if isinstance(contract, dict) else None):
            findings.append("entrypoint %r expected contract sha256 mismatch" % name)
        if contract_entry.get("accepted_versions") != [contract_document.get("contract_version")]:
            findings.append("entrypoint %r accepted_versions mismatch" % name)
    return findings


def render_governance_dependencies_bytes(repo_root: Path) -> bytes:
    contract = build_contract_document(repo_root)
    document = build_governance_dependencies_document(repo_root, contract)
    return canonical_bytes(document)


# ---------------------------------------------------------------------------
# Contract validation: GR-01..GR-12
# ---------------------------------------------------------------------------


def _document_table(contract: typing.Dict[str, object]) -> typing.Dict[str, typing.Dict[str, object]]:
    table: typing.Dict[str, typing.Dict[str, object]] = {}
    documents = contract.get("documents")
    if isinstance(documents, list):
        for document in documents:
            if isinstance(document, dict) and isinstance(document.get("doc_id"), str):
                table[typing.cast(str, document["doc_id"])] = typing.cast(typing.Dict[str, object], document)
    return table


def _rule_table(contract: typing.Dict[str, object]) -> typing.Dict[str, typing.Dict[str, object]]:
    table: typing.Dict[str, typing.Dict[str, object]] = {}
    rules = contract.get("rule_applicability")
    if isinstance(rules, list):
        for rule in rules:
            if isinstance(rule, dict) and isinstance(rule.get("rule_id"), str):
                table[typing.cast(str, rule["rule_id"])] = typing.cast(typing.Dict[str, object], rule)
    return table


def _graph_nodes(contract: typing.Dict[str, object]) -> typing.Dict[str, typing.List[str]]:
    adjacency: typing.Dict[str, typing.List[str]] = {}
    edges = contract.get("dependency_graph")
    if isinstance(edges, list):
        for edge in edges:
            if not isinstance(edge, dict):
                continue
            source = edge.get("from_node")
            target = edge.get("to_doc_id")
            if isinstance(source, str) and isinstance(target, str):
                adjacency.setdefault(source, []).append(target)
    for node in list(adjacency):
        adjacency[node] = sorted(adjacency[node])
    return adjacency


def _find_cycle(adjacency: typing.Dict[str, typing.List[str]]) -> typing.Optional[typing.List[str]]:
    WHITE, GREY, BLACK = 0, 1, 2
    color: typing.Dict[str, int] = {node: WHITE for node in adjacency}
    stack: typing.List[str] = []

    def visit(node: str) -> typing.Optional[typing.List[str]]:
        color[node] = GREY
        stack.append(node)
        for neighbour in adjacency.get(node, []):
            if neighbour not in color:
                color[neighbour] = WHITE
            if color[neighbour] == GREY:
                start = stack.index(neighbour)
                return stack[start:] + [neighbour]
            if color[neighbour] == WHITE:
                found = visit(neighbour)
                if found:
                    return found
        stack.pop()
        color[node] = BLACK
        return None

    for node in sorted(adjacency):
        if color[node] == WHITE:
            found = visit(node)
            if found:
                return found
    return None


def _validate_documents(
    contract: typing.Dict[str, object],
    repo_root: typing.Optional[Path],
    verify_hashes: bool,
) -> typing.List[models.GovernanceFinding]:
    findings: typing.List[models.GovernanceFinding] = []
    documents = contract.get("documents")
    if not isinstance(documents, list) or len(documents) != 27:
        findings.append(models.GovernanceFinding("GR-03", "FAIL", "documents must be an array of 27 records"))
        return findings
    seen_ids: typing.Set[str] = set()
    seen_paths: typing.Set[str] = set()
    for document in documents:
        if not isinstance(document, dict):
            findings.append(models.GovernanceFinding("GR-03", "FAIL", "a document record is not an object"))
            continue
        doc_id = document.get("doc_id")
        path = document.get("path")
        if not isinstance(doc_id, str) or not isinstance(path, str):
            findings.append(models.GovernanceFinding("GR-03", "FAIL", "a document record has no doc_id/path"))
            continue
        if doc_id in seen_ids:
            findings.append(models.GovernanceFinding("GR-03", "FAIL", "duplicate document id", doc_id))
        seen_ids.add(doc_id)
        if path in seen_paths:
            findings.append(models.GovernanceFinding("GR-03", "FAIL", "duplicate document path", path))
        seen_paths.add(path)
        try:
            _relpath_parts(path)
        except GovernanceError:
            findings.append(models.GovernanceFinding("GR-03", "FAIL", "document path is not a safe relative path", path))
        sha = document.get("sha256")
        if not isinstance(sha, str) or not HEX64_UPPER_RE.match(sha):
            findings.append(models.GovernanceFinding("GR-03", "FAIL", "document sha256 must be uppercase 64-hex", path))
        lifecycle = document.get("lifecycle")
        if not isinstance(lifecycle, dict) or lifecycle.get("state") not in models.LIFECYCLE_STATES:
            findings.append(models.GovernanceFinding("GR-03", "FAIL", "document lifecycle state is not closed", path))
        if not isinstance(document.get("role_scope"), list) or not document["role_scope"]:
            findings.append(models.GovernanceFinding("GR-03", "FAIL", "document role_scope is empty", path))
        elif any(role not in ROLE_SET for role in document["role_scope"]):
            findings.append(models.GovernanceFinding("GR-03", "FAIL", "document role_scope is not closed", path))
        if verify_hashes and repo_root is not None:
            try:
                actual = file_identity(repo_root, path)
            except GovernanceError as error:
                findings.append(models.GovernanceFinding("GR-03", "FAIL", str(error), path))
                continue
            for field in ("bytes", "lf"):
                if document.get(field) != actual[field]:
                    findings.append(
                        models.GovernanceFinding(
                            "GR-03", "FAIL", "document %s does not match the checkout" % field, path
                        )
                    )
            if str(document.get("sha256")).lower() != str(actual["sha256"]).lower():
                findings.append(
                    models.GovernanceFinding("GR-03", "FAIL", "document sha256 does not match the checkout bytes", path)
                )
    return findings


def _validate_roles(contract: typing.Dict[str, object], documents: typing.Dict[str, typing.Dict[str, object]]) -> typing.List[models.GovernanceFinding]:
    findings: typing.List[models.GovernanceFinding] = []
    roles = contract.get("roles")
    if not isinstance(roles, dict) or set(roles) != ROLE_SET:
        return [models.GovernanceFinding("GR-04", "FAIL", "roles must be exactly source-library and consumer")]
    for role_id, profile in roles.items():
        if not isinstance(profile, dict):
            findings.append(models.GovernanceFinding("GR-04", "FAIL", "a role profile is not an object", role_id))
            continue
        if profile.get("role_id") != role_id:
            findings.append(models.GovernanceFinding("GR-04", "FAIL", "role_id does not match its key", role_id))
        required = profile.get("required_documents")
        conditional = profile.get("conditional_documents")
        exclusions = profile.get("exclusions")
        if not isinstance(required, list) or not isinstance(conditional, list) or not isinstance(exclusions, list):
            findings.append(models.GovernanceFinding("GR-04", "FAIL", "role lists are malformed", role_id))
            continue
        required_set = set()
        for doc_id in required:
            if doc_id not in documents:
                findings.append(models.GovernanceFinding("GR-04", "FAIL", "required document is not documented", str(doc_id)))
            required_set.add(doc_id)
            if doc_id in documents and role_id not in documents[doc_id].get("role_scope", []):
                findings.append(
                    models.GovernanceFinding("GR-04", "FAIL", "role requires a document outside its role_scope", str(doc_id))
                )
        conditional_set = set()
        for entry in conditional:
            if not isinstance(entry, dict) or not isinstance(entry.get("doc_id"), str):
                findings.append(models.GovernanceFinding("GR-04", "FAIL", "conditional document is malformed", role_id))
                continue
            doc_id = entry["doc_id"]
            conditional_set.add(doc_id)
            if doc_id not in documents:
                findings.append(models.GovernanceFinding("GR-04", "FAIL", "conditional document is not documented", doc_id))
            if entry.get("condition") not in CONDITION_RULE_SET:
                findings.append(models.GovernanceFinding("GR-04", "FAIL", "conditional rule is not closed", doc_id))
            if doc_id in documents and role_id not in documents[doc_id].get("role_scope", []):
                findings.append(
                    models.GovernanceFinding("GR-04", "FAIL", "conditional document is outside its role_scope", doc_id)
                )
        excluded_set = set()
        for entry in exclusions:
            if not isinstance(entry, dict) or not isinstance(entry.get("doc_id"), str):
                findings.append(models.GovernanceFinding("GR-04", "FAIL", "exclusion is malformed", role_id))
                continue
            excluded_set.add(entry["doc_id"])
            if entry["doc_id"] not in documents:
                findings.append(models.GovernanceFinding("GR-04", "FAIL", "excluded document is not documented", entry["doc_id"]))
        overlap = (required_set & conditional_set) | (required_set & excluded_set) | (conditional_set & excluded_set)
        if overlap:
            findings.append(
                models.GovernanceFinding("GR-04", "FAIL", "a document is both required/conditional/excluded", ", ".join(sorted(overlap)))
            )
        if profile.get("adoption_required") is True and role_id != "consumer":
            findings.append(models.GovernanceFinding("GR-04", "FAIL", "adoption_required belongs to the consumer role only"))
        if role_id == "consumer" and profile.get("adoption_required") is not True:
            findings.append(models.GovernanceFinding("GR-04", "FAIL", "the consumer role must require local adoption"))
        routes = profile.get("role_entry_routes")
        if not isinstance(routes, list) or not routes or any(route not in ROUTE_ID_SET for route in routes):
            findings.append(models.GovernanceFinding("GR-04", "FAIL", "role_entry_routes is empty or not closed", role_id))
    return findings


def _validate_routes(contract: typing.Dict[str, object]) -> typing.List[models.GovernanceFinding]:
    findings: typing.List[models.GovernanceFinding] = []
    routes = contract.get("entry_routes")
    if not isinstance(routes, list) or len(routes) != 5:
        return [models.GovernanceFinding("GR-05", "FAIL", "entry_routes must be exactly five family records")]
    families = set()
    seen_route_ids: typing.Set[str] = set()
    for route in routes:
        if not isinstance(route, dict):
            findings.append(models.GovernanceFinding("GR-05", "FAIL", "an entry route record is not an object"))
            continue
        family = route.get("route_family")
        if family not in ROUTE_FAMILY_SET:
            findings.append(models.GovernanceFinding("GR-05", "FAIL", "route family is not closed", str(family)))
            continue
        families.add(family)
        route_ids = route.get("route_ids")
        if not isinstance(route_ids, list) or not route_ids:
            findings.append(models.GovernanceFinding("GR-05", "FAIL", "route_ids is empty", str(family)))
            continue
        for route_id in route_ids:
            if route_id not in ROUTE_ID_SET or models.ROUTE_FAMILY_OF.get(route_id) != family:
                findings.append(
                    models.GovernanceFinding("GR-05", "FAIL", "route id does not belong to its family", str(route_id))
                )
            seen_route_ids.add(str(route_id))
        if not isinstance(route.get("triggers"), list) or not route["triggers"]:
            findings.append(models.GovernanceFinding("GR-05", "FAIL", "route triggers are empty", str(family)))
        if not isinstance(route.get("fail_closed_behavior"), str) or not route["fail_closed_behavior"]:
            findings.append(models.GovernanceFinding("GR-05", "FAIL", "route has no fail-closed behaviour", str(family)))
        host_scope = route.get("supported_host_scope")
        if not isinstance(host_scope, dict) or host_scope.get("claim_label") not in (
            "GUIDANCE-ONLY",
            "CI-STRUCTURAL",
            "HOST-ENFORCED",
        ):
            findings.append(models.GovernanceFinding("GR-05", "FAIL", "route host scope claim label is not closed", str(family)))
    if families != ROUTE_FAMILY_SET:
        findings.append(models.GovernanceFinding("GR-05", "FAIL", "the five route families are not all present"))
    if seen_route_ids != ROUTE_ID_SET:
        findings.append(
            models.GovernanceFinding(
                "GR-05",
                "FAIL",
                "the seven route ids are not all present; missing=%s"
                % ", ".join(sorted(ROUTE_ID_SET - seen_route_ids)),
            )
        )
    return findings


def _validate_graph(
    contract: typing.Dict[str, object],
    documents: typing.Dict[str, typing.Dict[str, object]],
    repo_root: typing.Optional[Path],
) -> typing.List[models.GovernanceFinding]:
    findings: typing.List[models.GovernanceFinding] = []
    edges = contract.get("dependency_graph")
    if not isinstance(edges, list) or not edges:
        return [models.GovernanceFinding("GR-06", "FAIL", "dependency_graph must be a non-empty array")]
    skill_ids: typing.Optional[typing.Set[str]] = None
    if repo_root is not None:
        skill_ids = {entry["name"] for entry in scan_skill_entrypoints(repo_root)}
    seen_edges: typing.Set[typing.Tuple[str, str]] = set()
    adjacency: typing.Dict[str, typing.List[str]] = {}
    for edge in edges:
        if not isinstance(edge, dict):
            findings.append(models.GovernanceFinding("GR-06", "FAIL", "a graph edge is not an object"))
            continue
        source = edge.get("from_node")
        target = edge.get("to_doc_id")
        edge_class = edge.get("class")
        rule = edge.get("rule")
        reason = edge.get("reason")
        if not isinstance(source, str) or not re.match(r"^(doc|route|route_family|skill):[A-Za-z0-9_.-]+$", source):
            findings.append(models.GovernanceFinding("GR-06", "FAIL", "graph from_node is not a known node kind", str(source)))
            continue
        kind, name = source.split(":", 1)
        if kind == "doc" and name not in documents:
            findings.append(models.GovernanceFinding("GR-06", "FAIL", "graph source doc is not documented", source))
        elif kind == "route" and name not in ROUTE_ID_SET:
            findings.append(models.GovernanceFinding("GR-06", "FAIL", "graph source route id is not known", source))
        elif kind == "route_family" and name not in ROUTE_FAMILY_SET:
            findings.append(models.GovernanceFinding("GR-06", "FAIL", "graph source route family is not known", source))
        elif kind == "skill" and skill_ids is not None and name not in skill_ids:
            findings.append(models.GovernanceFinding("GR-06", "FAIL", "graph source skill is not a shipped skill", source))
        if not isinstance(target, str) or target not in documents:
            findings.append(
                models.GovernanceFinding("GR-06", "FAIL", "a required/unresolvable edge target is not a documented node", str(target))
            )
            continue
        if edge_class not in DEPENDENCY_CLASS_SET:
            findings.append(models.GovernanceFinding("GR-06", "FAIL", "graph edge class is not closed", source))
        if edge_class == "conditional":
            if rule not in CONDITION_RULE_SET:
                findings.append(models.GovernanceFinding("GR-06", "FAIL", "conditional edge rule is not closed", source))
        elif rule is not None:
            findings.append(models.GovernanceFinding("GR-06", "FAIL", "only conditional edges carry a rule", source))
        if not isinstance(reason, str) or not reason:
            findings.append(models.GovernanceFinding("GR-06", "FAIL", "graph edge has no reason", source))
        key = (source, target)
        if key in seen_edges:
            findings.append(models.GovernanceFinding("GR-06", "FAIL", "duplicate graph edge", "%s->%s" % key))
        seen_edges.add(key)
        adjacency.setdefault(source, []).append("doc:" + target)
        lifecycle = documents[target].get("lifecycle")
        if isinstance(lifecycle, dict) and lifecycle.get("state") != "effective" and edge_class == "required":
            findings.append(
                models.GovernanceFinding("GR-06", "FAIL", "a required edge resolves only to a non-effective document", target)
            )
    cycle = _find_cycle(adjacency)
    if cycle is not None:
        findings.append(models.GovernanceFinding("GR-06", "FAIL", "dependency_graph contains a cycle: %s" % " -> ".join(cycle)))
    return findings


def _validate_rules(
    contract: typing.Dict[str, object],
    inventory: typing.Dict[str, object],
) -> typing.List[models.GovernanceFinding]:
    findings: typing.List[models.GovernanceFinding] = []
    rules = contract.get("rule_applicability")
    if not isinstance(rules, list) or len(rules) != 187:
        return [models.GovernanceFinding("GR-07", "FAIL", "rule_applicability must be an array of 187 records")]
    inventory_rules = {
        str(rule.get("id")): rule
        for rule in typing.cast(typing.List[typing.Dict[str, object]], inventory.get("rules") or [])
        if isinstance(rule, dict)
    }
    seen: typing.Set[str] = set()
    last_id: typing.Optional[str] = None
    documents = _document_table(contract)
    for rule in rules:
        if not isinstance(rule, dict):
            findings.append(models.GovernanceFinding("GR-07", "FAIL", "a rule record is not an object"))
            continue
        rule_id = rule.get("rule_id")
        if not isinstance(rule_id, str) or rule_id not in inventory_rules:
            findings.append(models.GovernanceFinding("GR-07", "FAIL", "rule is not in the inventory", str(rule_id)))
            continue
        if rule_id in seen:
            findings.append(models.GovernanceFinding("GR-07", "FAIL", "duplicate rule id", rule_id))
        seen.add(rule_id)
        if last_id is not None and rule_id <= last_id:
            findings.append(models.GovernanceFinding("GR-07", "FAIL", "rules are not sorted by id", rule_id))
        last_id = rule_id
        if rule.get("source_document") not in documents:
            findings.append(models.GovernanceFinding("GR-07", "FAIL", "rule source_document is not documented", rule_id))
        if not isinstance(rule.get("applies_to_roles"), list) or not rule["applies_to_roles"] or any(
            role not in ROLE_SET for role in rule["applies_to_roles"]
        ):
            findings.append(models.GovernanceFinding("GR-07", "FAIL", "rule applies_to_roles is empty or not closed", rule_id))
        if rule.get("authority_action") is not (rule.get("class") == "action-permission"):
            findings.append(models.GovernanceFinding("GR-07", "FAIL", "authority_action is not the mechanical class test", rule_id))
        if rule.get("enforcement_class") not in ENFORCEMENT_CLASS_SET:
            findings.append(models.GovernanceFinding("GR-07", "FAIL", "enforcement_class is not closed", rule_id))
        if not isinstance(rule.get("enforcement_ref"), str) or not rule["enforcement_ref"]:
            findings.append(models.GovernanceFinding("GR-07", "FAIL", "enforcement_ref is empty", rule_id))
    if seen != set(inventory_rules):
        findings.append(
            models.GovernanceFinding(
                "GR-07",
                "FAIL",
                "rule set differs from the inventory; missing=%s"
                % ", ".join(sorted(set(inventory_rules) - seen)),
            )
        )
    return findings


def _validate_projection_consistency(
    contract: typing.Dict[str, object],
    inventory: typing.Dict[str, object],
    projection: typing.Dict[str, object],
) -> typing.List[models.GovernanceFinding]:
    findings: typing.List[models.GovernanceFinding] = []
    projection_findings = validate_projection_document(projection, inventory)
    for message in projection_findings:
        findings.append(models.GovernanceFinding("GR-08", "FAIL", message))
    derived = derive_projection_output(inventory, projection)["rules"]
    inventory_rules = {
        str(rule.get("id")): rule
        for rule in typing.cast(typing.List[typing.Dict[str, object]], inventory.get("rules") or [])
        if isinstance(rule, dict)
    }
    direct_fields = {
        "anchor": "anchor",
        "class": "cls",
        "dimension": "dim",
        "lifecycle": "lifecycle",
    }
    for rule in typing.cast(typing.List[typing.Dict[str, object]], contract.get("rule_applicability") or []):
        if not isinstance(rule, dict):
            continue
        rule_id = str(rule.get("rule_id"))
        inventory_rule = inventory_rules.get(rule_id)
        if inventory_rule is None:
            continue
        consumer = inventory_rule.get("consumer") or {}
        for field, source_key in direct_fields.items():
            if rule.get(field) != inventory_rule.get(source_key):
                findings.append(
                    models.GovernanceFinding("GR-08", "FAIL", "direct field %r is not byte-equal to the inventory" % field, rule_id)
                )
        if rule.get("adoption_status") != typing.cast(typing.Dict[str, object], consumer).get("adoption_status"):
            findings.append(models.GovernanceFinding("GR-08", "FAIL", "adoption_status is not equal to the inventory", rule_id))
        if rule.get("consumer_effect") != (typing.cast(typing.Dict[str, object], consumer).get("effect") or ""):
            findings.append(models.GovernanceFinding("GR-08", "FAIL", "consumer_effect is not equal to the inventory", rule_id))
        expected = derived.get(rule_id)
        if expected is None:
            continue
        for field in ("source_document", "applies_to_roles", "authority_action", "enforcement_class", "enforcement_ref"):
            if rule.get(field) != expected.get(field):
                findings.append(
                    models.GovernanceFinding("GR-08", "FAIL", "derived field %r is not the committed projection value" % field, rule_id)
                )
    return findings


def _validate_host_and_enforcement(contract: typing.Dict[str, object]) -> typing.List[models.GovernanceFinding]:
    findings: typing.List[models.GovernanceFinding] = []
    host_boundary = contract.get("host_boundary")
    if not isinstance(host_boundary, dict):
        return [models.GovernanceFinding("GR-11", "FAIL", "host_boundary is missing")]
    hosts = host_boundary.get("supported_hosts")
    if not isinstance(hosts, list) or not hosts:
        findings.append(models.GovernanceFinding("GR-11", "FAIL", "supported_hosts is empty"))
    else:
        for host in hosts:
            if not isinstance(host, dict):
                findings.append(models.GovernanceFinding("GR-11", "FAIL", "a supported-host record is not an object"))
                continue
            claim = host.get("claim")
            if claim not in models.HOST_CLAIM_LABELS:
                findings.append(models.GovernanceFinding("GR-11", "FAIL", "host claim label is not closed", str(claim)))
                continue
            evidence_refs = host.get("evidence_refs")
            if claim in ("OBSERVED-TESTED", "OBSERVED-IDENTITY-ONLY") and (
                not isinstance(evidence_refs, list) or not evidence_refs
            ):
                findings.append(
                    models.GovernanceFinding("GR-11", "FAIL", "an observed host claim requires evidence refs", str(claim))
                )
            if claim == "OBSERVED-TESTED" and not isinstance(host.get("limitations"), list):
                findings.append(models.GovernanceFinding("GR-11", "FAIL", "an observed-tested claim needs limitations"))
    behavior = host_boundary.get("unsupported_host_behavior")
    if not isinstance(behavior, str) or "fail closed" not in behavior:
        findings.append(models.GovernanceFinding("GR-11", "FAIL", "unsupported-host behaviour is not fail-closed"))
    claims = contract.get("enforcement_claims")
    if not isinstance(claims, dict):
        return findings + [models.GovernanceFinding("GR-10", "FAIL", "enforcement_claims is missing")]
    claim = claims.get("claim")
    if claim not in ("GUIDANCE-ONLY", "CI-STRUCTURAL", "HOST-PLUGIN"):
        findings.append(models.GovernanceFinding("GR-10", "FAIL", "enforcement claim value is not closed", str(claim)))
    if claim == "HOST-PLUGIN":
        host_plugin = claims.get("host_plugin")
        if (
            not isinstance(host_plugin, dict)
            or not isinstance(host_plugin.get("composition_sha256"), str)
            or not HEX64_UPPER_RE.match(host_plugin["composition_sha256"])
            or not host_plugin.get("evidence_refs")
        ):
            findings.append(
                models.GovernanceFinding("GR-10", "FAIL", "a HOST-PLUGIN claim requires a composition hash and evidence")
            )
    if not isinstance(claims.get("bypass_routes"), list) or not claims["bypass_routes"]:
        findings.append(models.GovernanceFinding("GR-10", "FAIL", "the bypass analysis is empty"))
    for surface in typing.cast(typing.List[object], claims.get("named_surfaces") or []):
        if not isinstance(surface, dict) or surface.get("class") not in ("CI-REQUIRED", "CI-STRUCTURAL", "HOST-ENFORCED"):
            findings.append(models.GovernanceFinding("GR-10", "FAIL", "a named surface has no closed enforcement class"))
            continue
        if surface["class"] == "HOST-ENFORCED" and claim != "HOST-PLUGIN":
            findings.append(models.GovernanceFinding("GR-10", "FAIL", "a HOST-ENFORCED surface claim needs a host plugin"))
    return findings


def _validate_identity_and_nongoals(
    contract: typing.Dict[str, object],
    raw_bytes: typing.Optional[bytes],
) -> typing.List[models.GovernanceFinding]:
    findings: typing.List[models.GovernanceFinding] = []
    if contract.get("schema") != CONTRACT_SCHEMA_ID:
        findings.append(models.GovernanceFinding("GR-02", "FAIL", "schema is not %r" % CONTRACT_SCHEMA_ID))
    if contract.get("contract_id") != CONTRACT_ID:
        findings.append(models.GovernanceFinding("GR-02", "FAIL", "contract_id is not %r" % CONTRACT_ID))
    version = contract.get("contract_version")
    if not isinstance(version, str) or not SEMVER_RE.match(version):
        findings.append(models.GovernanceFinding("GR-02", "FAIL", "contract_version must be SemVer"))
    source = contract.get("source")
    if not isinstance(source, dict):
        findings.append(models.GovernanceFinding("GR-02", "FAIL", "source identity is missing"))
    else:
        if not isinstance(source.get("repository"), str):
            findings.append(models.GovernanceFinding("GR-02", "FAIL", "source.repository is missing"))
        for key in ("commit", "tree"):
            if not isinstance(source.get(key), str) or not HEX40_RE.match(typing.cast(str, source.get(key))):
                findings.append(models.GovernanceFinding("GR-02", "FAIL", "source.%s must be 40 lowercase hex" % key))
        generated_by = source.get("generated_by")
        if not isinstance(generated_by, dict) or not isinstance(generated_by.get("tool"), str):
            findings.append(models.GovernanceFinding("GR-02", "FAIL", "source.generated_by is missing"))
    # No self hash and no manifest hash may be embedded in the contract.
    if raw_bytes is not None:
        contract_sha = sha256_upper(raw_bytes)
        if contract_sha in raw_bytes.decode("utf-8", "replace"):
            findings.append(models.GovernanceFinding("GR-02", "FAIL", "the contract embeds its own sha256"))
    serialized = canonical_bytes(contract).decode("utf-8", "replace")
    if re.search(r"[A-Za-z]:\\", serialized) or re.search(r"/(?:home|Users)/", serialized):
        findings.append(models.GovernanceFinding("GR-02", "FAIL", "the contract embeds an absolute host path"))
    if re.search(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}", serialized):
        findings.append(models.GovernanceFinding("GR-02", "FAIL", "the contract embeds a capture timestamp"))
    lifecycle = contract.get("lifecycle")
    if not isinstance(lifecycle, dict) or lifecycle.get("status") not in ("proposed", "effective"):
        findings.append(models.GovernanceFinding("GR-02", "FAIL", "contract lifecycle status is not closed"))
    elif not isinstance(lifecycle.get("migration_rule"), str) or not isinstance(lifecycle.get("rollback_rule"), str):
        findings.append(models.GovernanceFinding("GR-02", "FAIL", "contract lifecycle lacks migration/rollback rules"))
    non_claims = contract.get("non_claims")
    if not isinstance(non_claims, list) or len(non_claims) < 3:
        findings.append(models.GovernanceFinding("GR-02", "FAIL", "non_claims must name at least three non-claims"))
    trust = contract.get("trust")
    if not isinstance(trust, dict) or not isinstance(trust.get("verification_rule"), str):
        findings.append(models.GovernanceFinding("GR-02", "FAIL", "trust.verification_rule is missing"))
    adoption = contract.get("local_adoption")
    if not isinstance(adoption, dict) or adoption.get("schema") != ADOPTION_SCHEMA_ID:
        findings.append(models.GovernanceFinding("GR-09", "FAIL", "local_adoption schema is missing or wrong"))
    elif not adoption.get("required_for_consumer") is True:
        findings.append(models.GovernanceFinding("GR-09", "FAIL", "consumer adoption must be required explicitly"))
    if "enforcement_summary" in contract or "enforcement_counts" in contract:
        findings.append(models.GovernanceFinding("GR-02", "FAIL", "the contract publishes an aggregate enforcement tally"))
    return findings


def validate_contract_document(
    contract: typing.Dict[str, object],
    schemas: typing.Dict[str, typing.Dict[str, object]],
    *,
    repo_root: typing.Optional[Path] = None,
    inventory: typing.Optional[typing.Dict[str, object]] = None,
    projection: typing.Optional[typing.Dict[str, object]] = None,
    raw_bytes: typing.Optional[bytes] = None,
) -> typing.List[models.GovernanceFinding]:
    """Validate a contract document against schema + GR-01..GR-12.

    Returns findings only; callers decide the exit status.  A validation PASS is
    a structural observation, never approval.
    """
    findings: typing.List[models.GovernanceFinding] = []
    schema_findings = validate_json_schema(contract, schemas["contract"], root_schema=schemas["contract"])
    for message in schema_findings:
        findings.append(models.GovernanceFinding("GR-01", "FAIL", message))
    if inventory is None:
        try:
            inventory = load_inventory(repo_root) if repo_root is not None else None
        except GovernanceError as error:
            findings.append(models.GovernanceFinding("GR-08", "BLOCKED", str(error)))
    if projection is None:
        try:
            projection = load_projection(repo_root) if repo_root is not None else None
        except GovernanceError as error:
            findings.append(models.GovernanceFinding("GR-08", "BLOCKED", str(error)))
    findings.extend(_validate_identity_and_nongoals(contract, raw_bytes))
    documents = _document_table(contract)
    findings.extend(_validate_documents(contract, repo_root, verify_hashes=repo_root is not None))
    findings.extend(_validate_roles(contract, documents))
    findings.extend(_validate_routes(contract))
    findings.extend(_validate_graph(contract, documents, repo_root))
    if inventory is not None:
        findings.extend(_validate_rules(contract, inventory))
        if projection is not None:
            findings.extend(_validate_projection_consistency(contract, inventory, projection))
    findings.extend(_validate_host_and_enforcement(contract))
    # Deterministic serialization round-trip: the committed bytes must equal the
    # canonical rendering of the parsed document.
    if raw_bytes is not None and canonical_bytes(contract) != raw_bytes:
        findings.append(models.GovernanceFinding("GR-12", "FAIL", "committed contract bytes are not canonical JSON"))
    return findings


def validate_contract_at_repo(
    repo_root: Path,
) -> typing.Tuple[typing.Dict[str, object], bytes, typing.List[models.GovernanceFinding]]:
    schemas = load_schemas(repo_root)
    contract, raw_bytes = load_contract(repo_root)
    inventory = load_inventory(repo_root)
    projection = load_projection(repo_root)
    findings = validate_contract_document(
        contract,
        schemas,
        repo_root=repo_root,
        inventory=inventory,
        projection=projection,
        raw_bytes=raw_bytes,
    )
    return contract, raw_bytes, findings


# ---------------------------------------------------------------------------
# Resolution of the role/route applicability graph
# ---------------------------------------------------------------------------


def _condition_holds(condition: str, conditions: typing.Optional[typing.Mapping[str, bool]]) -> bool:
    if condition not in CONDITION_RULE_SET:
        raise GovernanceError("unknown_condition", "condition is not in the closed vocabulary", condition)
    if not conditions:
        return False
    return bool(conditions.get(condition, False))


def _doc_lifecycle(document: typing.Dict[str, object]) -> str:
    lifecycle = document.get("lifecycle")
    if isinstance(lifecycle, dict):
        return str(lifecycle.get("state") or "effective")
    return "effective"


def _edge_closure(
    contract: typing.Dict[str, object],
    start_nodes: typing.Sequence[str],
    conditions: typing.Optional[typing.Mapping[str, bool]],
) -> typing.Tuple[typing.List[str], typing.List[typing.Dict[str, str]], typing.List[typing.Dict[str, str]]]:
    """Traverse the resolution graph from the route nodes.

    Returns (required_doc_ids, conditional_records, advisory_records).  Required
    edges add targets; conditional edges add only when their closed rule holds;
    optional edges are recorded as advisory; maintainer-only targets are never
    added (not consumer-distributed).  Unresolvable required edges are a hard
    failure (the caller receives them in the missing list).
    """
    edges = contract.get("dependency_graph")
    if not isinstance(edges, list):
        raise GovernanceError("invalid_contract", "dependency_graph is not an array")
    adjacency: typing.Dict[str, typing.List[typing.Dict[str, object]]] = {}
    for edge in edges:
        if not isinstance(edge, dict):
            raise GovernanceError("invalid_contract", "dependency_graph edge is not an object")
        source = str(edge.get("from_node"))
        adjacency.setdefault(source, []).append(edge)
    for source in adjacency:
        adjacency[source] = sorted(adjacency[source], key=lambda item: (str(item.get("to_doc_id")), str(item.get("class"))))
    visited_nodes: typing.Set[str] = set()
    queue: typing.List[str] = list(start_nodes)
    required: typing.List[str] = []
    conditional_records: typing.List[typing.Dict[str, str]] = []
    advisory_records: typing.List[typing.Dict[str, str]] = []
    while queue:
        node = queue.pop(0)
        if node in visited_nodes:
            continue
        visited_nodes.add(node)
        for edge in adjacency.get(node, []):
            target = str(edge.get("to_doc_id"))
            edge_class = str(edge.get("class"))
            if edge_class == "required":
                if target not in required:
                    required.append(target)
                queue.append("doc:" + target)
            elif edge_class == "conditional":
                rule = edge.get("rule")
                holds = _condition_holds(str(rule), conditions)
                record = {"from_node": node, "to_doc_id": target, "rule": str(rule), "satisfied": "yes" if holds else "no"}
                conditional_records.append(record)
                if holds:
                    queue.append("doc:" + target)
            elif edge_class == "optional":
                advisory_records.append({"from_node": node, "to_doc_id": target, "class": "optional"})
            elif edge_class == "maintainer-only":
                advisory_records.append({"from_node": node, "to_doc_id": target, "class": "maintainer-only"})
    return required, conditional_records, advisory_records


def _exclusion_reason(reason_text: str) -> str:
    lowered = reason_text.lower()
    if "enforcement surface" in lowered:
        return "enforcement-surface"
    return "role-excluded"


def resolve(
    contract: typing.Dict[str, object],
    *,
    role: str,
    route_id: str,
    repo_root: Path,
    conditions: typing.Optional[typing.Mapping[str, bool]] = None,
    adoption: typing.Optional[typing.Dict[str, object]] = None,
    adoption_ref: typing.Optional[str] = None,
    adoption_sha256: typing.Optional[str] = None,
    nested_policies: typing.Optional[typing.Sequence[str]] = None,
    target: typing.Optional[typing.Dict[str, object]] = None,
    host_facts: typing.Optional[typing.Dict[str, object]] = None,
    operation_class: str = "read-only-diagnostic",
    schemas: typing.Optional[typing.Dict[str, typing.Dict[str, object]]] = None,
) -> models.ResolutionResult:
    """Resolve the applicable document/rule set for one role and route.

    Fail-closed: any missing required document, hash mismatch, superseded target,
    cycle, unresolved required edge, absent/withdrawn adoption or unresolved
    rule-level conflict makes status BLOCKED with the exact inputs named.
    """
    if role not in ROLE_SET:
        raise GovernanceError("unknown_role", "role must be one of %s" % (models.ROLE_IDS,))
    if route_id not in ROUTE_ID_SET:
        raise GovernanceError("unknown_route", "route_id must be one of the seven route ids")
    if operation_class not in OPERATION_CLASS_SET:
        raise GovernanceError("unknown_operation_class", "operation_class is not in the closed vocabulary")
    route_family = models.ROUTE_FAMILY_OF[route_id]
    schemas = schemas if schemas is not None else load_schemas(repo_root)
    findings: typing.List[models.GovernanceFinding] = []
    exclusions: typing.List[typing.Dict[str, object]] = []
    excluded_documents: typing.List[typing.Dict[str, object]] = []
    resolved_documents: typing.List[models.ResolvedDocument] = []
    resolved_rules: typing.List[typing.Dict[str, object]] = []
    conflicts: typing.List[typing.Dict[str, object]] = []
    labels: typing.List[str] = []
    roles = contract.get("roles")
    if not isinstance(roles, dict) or role not in roles:
        raise GovernanceError("invalid_contract", "contract has no role profile for %r" % role)
    profile = typing.cast(typing.Dict[str, object], roles[role])
    documents = _document_table(contract)
    # Structural validation (schema + roles/routes/graph) before resolving: a
    # cycle or malformed graph is a hard failure, never silently traversed.
    for message in validate_json_schema(contract, schemas["contract"], root_schema=schemas["contract"]):
        findings.append(models.GovernanceFinding("GR-01", "BLOCKED", "contract schema: " + message))
    for finding in _validate_roles(contract, documents) + _validate_routes(contract) + _validate_graph(contract, documents, None):
        findings.append(models.GovernanceFinding(finding.code, "BLOCKED", "contract validation: " + finding.message, finding.ref))
    if route_id not in typing.cast(typing.List[str], profile.get("role_entry_routes") or []):
        findings.append(
            models.GovernanceFinding("GR-05", "BLOCKED", "route id is not permitted for this role", "%s/%s" % (role, route_id))
        )
    # Role-profile documents.
    required_doc_ids: typing.List[str] = []
    conditional_doc_ids: typing.List[typing.Tuple[str, str]] = []
    for doc_id in typing.cast(typing.List[object], profile.get("required_documents") or []):
        if isinstance(doc_id, str):
            required_doc_ids.append(doc_id)
    for entry in typing.cast(typing.List[object], profile.get("conditional_documents") or []):
        if not isinstance(entry, dict):
            continue
        condition = str(entry.get("condition"))
        if _condition_holds(condition, conditions):
            conditional_doc_ids.append((str(entry.get("doc_id")), condition))
        else:
            exclusions.append({"ref": str(entry.get("doc_id")), "reason": "out-of-scope"})
    for entry in typing.cast(typing.List[object], profile.get("exclusions") or []):
        if isinstance(entry, dict):
            exclusions.append({"ref": str(entry.get("doc_id")), "reason": _exclusion_reason(str(entry.get("reason")))})
            excluded_documents.append(
                {"doc_id": str(entry.get("doc_id")), "path": str(documents.get(str(entry.get("doc_id")), {}).get("path")), "reason": _exclusion_reason(str(entry.get("reason"))), "detail": str(entry.get("reason"))}
            )
    # Resolution graph traversal from the route nodes.
    graph_required, graph_conditional, graph_advisory = _edge_closure(
        contract,
        ["route:" + route_id, "route_family:" + route_family],
        conditions,
    )
    for doc_id in graph_required:
        if doc_id not in required_doc_ids:
            required_doc_ids.append(doc_id)
    for record in graph_conditional:
        if record["satisfied"] == "yes":
            conditional_doc_ids.append((record["to_doc_id"], record["rule"]))
    for record in graph_advisory:
        exclusions.append({"ref": record["to_doc_id"], "reason": "out-of-scope"})
    for doc_id in sorted(set(required_doc_ids) | {doc_id for doc_id, _ in conditional_doc_ids}):
        document = documents.get(doc_id)
        if document is None:
            findings.append(models.GovernanceFinding("GR-06", "BLOCKED", "a required dependency does not resolve to a documented node", doc_id))
            excluded_documents.append({"doc_id": doc_id, "path": "", "reason": "missing", "detail": "not documented in the contract"})
            continue
        path = str(document.get("path"))
        lifecycle = _doc_lifecycle(document)
        if lifecycle in ("superseded", "withdrawn"):
            findings.append(
                models.GovernanceFinding("GR-06", "BLOCKED", "a required dependency resolves only to a %s document" % lifecycle, doc_id)
            )
            excluded_documents.append({"doc_id": doc_id, "path": path, "reason": lifecycle, "detail": "lifecycle excludes the target"})
            continue
        try:
            data = read_repo_bytes(repo_root, path)
        except GovernanceError as error:
            findings.append(models.GovernanceFinding("GR-03", "BLOCKED", str(error), path))
            excluded_documents.append({"doc_id": doc_id, "path": path, "reason": "missing", "detail": str(error)})
            continue
        sha = sha256_upper(data)
        if len(data) != document.get("bytes") or sha != document.get("sha256"):
            findings.append(
                models.GovernanceFinding(
                    "GR-03", "BLOCKED", "required document bytes/hash do not match the contract", path
                )
            )
            resolved_documents.append(
                models.ResolvedDocument(
                    doc_id=doc_id,
                    path=path,
                    bytes=len(data),
                    sha256=sha,
                    role_scope=typing.cast(typing.List[str], document.get("role_scope") or []),
                    lifecycle=lifecycle,
                    read_status="hash-mismatch",
                    adoption_provenance=None,
                )
            )
            continue
        resolved_documents.append(
            models.ResolvedDocument(
                doc_id=doc_id,
                path=path,
                bytes=len(data),
                sha256=sha,
                role_scope=typing.cast(typing.List[str], document.get("role_scope") or []),
                lifecycle=lifecycle,
                read_status="read-verified",
                adoption_provenance=None,
            )
        )
    resolved_documents.sort(key=lambda item: item.doc_id)
    resolved_doc_ids = {item.doc_id for item in resolved_documents if item.read_status == "read-verified"}
    # Local adoption (consumer role only; the source role is its own authoritative set).
    adoption_state = "unknown"
    adoption_authority_ref = None
    adopted_rule_ids: typing.Set[str] = set()
    installation_pin: typing.Optional[typing.Dict[str, object]] = None
    if profile.get("adoption_required") is True:
        if adoption is None:
            adoption_state = "not-adopted"
            findings.append(
                models.GovernanceFinding(
                    "GR-09", "BLOCKED", "no consumer adoption record resolves; portable defaults are not auto-adopted", "local_adoption"
                )
            )
        else:
            adoption_findings = validate_json_schema(adoption, schemas["adoption"], root_schema=schemas["adoption"])
            if adoption_findings:
                adoption_state = "unknown"
                findings.append(
                    models.GovernanceFinding("GR-09", "BLOCKED", "adoption record is malformed: %s" % "; ".join(adoption_findings[:5]), "local_adoption")
                )
            else:
                revoked = adoption.get("revoked_at_utc")
                installation = adoption.get("installation") if isinstance(adoption.get("installation"), dict) else {}
                installation_pin = {
                    "commit": installation.get("aegis_pin_commit"),
                    "tree": installation.get("aegis_pin_tree"),
                    "package_manifest_sha256": installation.get("payload_manifest_sha256"),
                }
                authority = adoption.get("authority") if isinstance(adoption.get("authority"), dict) else {}
                adoption_authority_ref = str(authority.get("ref") or "")
                contract_binding = adoption.get("contract") if isinstance(adoption.get("contract"), dict) else {}
                expected_contract_sha = sha256_upper(canonical_bytes(contract))
                if revoked is not None:
                    adoption_state = "withdrawn"
                    findings.append(
                        models.GovernanceFinding("GR-09", "BLOCKED", "local adoption was withdrawn by a recorded revocation", "local_adoption")
                    )
                elif contract_binding.get("sha256") != expected_contract_sha:
                    adoption_state = "unknown"
                    findings.append(
                        models.GovernanceFinding("GR-09", "BLOCKED", "adoption record binds a different contract sha256", "local_adoption")
                    )
                else:
                    adoption_state = "adopted"
                    adoption_block = adoption.get("adoption") if isinstance(adoption.get("adoption"), dict) else {}
                    for rule_id in typing.cast(typing.List[object], adoption_block.get("adopted_rule_ids") or []):
                        adopted_rule_ids.add(str(rule_id))
                if target is not None and target.get("target_repo") and adoption.get("target_repo") != target.get("target_repo"):
                    findings.append(
                        models.GovernanceFinding("GR-09", "BLOCKED", "adoption record target_repo does not match the resolution target", "role_target_mismatch")
                    )
    # Rule applicability.
    rules = typing.cast(typing.List[typing.Dict[str, object]], contract.get("rule_applicability") or [])
    for rule in rules:
        rule_id = str(rule.get("rule_id"))
        rule_roles = typing.cast(typing.List[str], rule.get("applies_to_roles") or [])
        if role not in rule_roles:
            exclusions.append({"ref": rule_id, "reason": "role-excluded"})
            continue
        lifecycle = str(rule.get("lifecycle"))
        if lifecycle in models.RULE_LIFECYCLE_EXCLUDED:
            exclusions.append({"ref": rule_id, "reason": models.RULE_LIFECYCLE_EXCLUDED[lifecycle]})
            continue
        if str(rule.get("source_document")) not in resolved_doc_ids:
            exclusions.append({"ref": rule_id, "reason": "out-of-scope"})
            continue
        if role == "consumer":
            adoption_status = str(rule.get("adoption_status"))
            explicitly_adopted = rule_id in adopted_rule_ids
            if adoption_status == "adopted-by-copy":
                explicitly_adopted = True
            if adoption_state != "adopted" or not explicitly_adopted:
                exclusions.append({"ref": rule_id, "reason": "not-adopted"})
                continue
        resolved_rules.append(
            {
                "rule_id": rule_id,
                "source_document": str(rule.get("source_document")),
                "applicability": "yes",
                "adoption_status": str(rule.get("adoption_status")),
                "enforcement_class": str(rule.get("enforcement_class")),
                "authority_action": bool(rule.get("authority_action")),
            }
        )
    resolved_rule_ids = {rule["rule_id"] for rule in resolved_rules}
    resolved_rule_table = _rule_table(contract)
    # Unresolved rule-level conflicts block; document-level conflicts are surfaced.
    for conflict in typing.cast(typing.List[typing.Dict[str, object]], contract.get("conflicts") or []):
        rule_ids = set(typing.cast(typing.List[str], conflict.get("rule_ids") or []))
        conflict_documents = set(typing.cast(typing.List[str], conflict.get("documents") or []))
        if len(rule_ids & resolved_rule_ids) >= 2:
            anchors = {rule_id: str(resolved_rule_table.get(rule_id, {}).get("anchor")) for rule_id in sorted(rule_ids & resolved_rule_ids)}
            conflicts.append(
                {
                    "conflict_id": conflict.get("conflict_id"),
                    "status": conflict.get("status"),
                    "rule_ids": sorted(rule_ids & resolved_rule_ids),
                    "anchors": anchors,
                    "resolved_by_resolver": False,
                }
            )
            findings.append(
                models.GovernanceFinding(
                    "GR-06",
                    "BLOCKED",
                    "unresolved rule conflict %s affects resolved rules %s; the resolver never picks a winner"
                    % (conflict.get("conflict_id"), sorted(rule_ids & resolved_rule_ids)),
                    str(conflict.get("conflict_id")),
                )
            )
        elif conflict_documents & resolved_doc_ids:
            conflicts.append(
                {
                    "conflict_id": conflict.get("conflict_id"),
                    "status": conflict.get("status"),
                    "documents": sorted(conflict_documents & resolved_doc_ids),
                    "rule_ids": sorted(rule_ids),
                    "resolved_by_resolver": False,
                }
            )
    # Nested/local policy files supplied explicitly by the caller.
    nested_records: typing.List[typing.Dict[str, object]] = []
    for relpath in nested_policies or []:
        try:
            identity = file_identity(repo_root, relpath)
        except GovernanceError as error:
            findings.append(models.GovernanceFinding("GR-03", "BLOCKED", "nested/local policy is unreadable: %s" % error, relpath))
            continue
        nested_records.append(
            {"path": identity["path"], "bytes": identity["bytes"], "sha256": identity["sha256"], "applies_to": target.get("target_repo") if target else "target"}
        )
    # Enforcement/host labels.
    enforcement_claims = contract.get("enforcement_claims") if isinstance(contract.get("enforcement_claims"), dict) else {}
    enforcement_claim = str(typing.cast(typing.Dict[str, object], enforcement_claims).get("claim") or "GUIDANCE-ONLY")
    gates_active = "none"
    if host_facts and host_facts.get("gates_active") not in (None, "none"):
        gates_active = str(host_facts.get("gates_active"))
    lifecycle = contract.get("lifecycle") if isinstance(contract.get("lifecycle"), dict) else {}
    if typing.cast(typing.Dict[str, object], lifecycle).get("status") == "proposed":
        labels.append("PROPOSED-CONTRACT")
    if installation_pin is not None and contract.get("source") and installation_pin.get("commit") != typing.cast(typing.Dict[str, object], contract["source"]).get("commit"):
        labels.append("HISTORICAL-UNMIGRATED")
    if enforcement_claim == "GUIDANCE-ONLY":
        labels.append("GUIDANCE-ONLY")
    if adoption_state == "not-adopted":
        labels.append("NOT-ADOPTED")
    blocking = [finding.status for finding in findings if finding.status in ("FAIL", "BLOCKED")]
    status = "BLOCKED" if blocking else "RESOLVED"
    resolved_set_digest = canonical_digest(
        {
            "role": role,
            "route_id": route_id,
            "documents": [[item.doc_id, item.sha256] for item in resolved_documents],
            "rules": sorted(resolved_rule_ids),
        }
    )
    result = models.ResolutionResult(
        status=status,
        role=role,
        route_id=route_id,
        route_family=route_family,
        resolved_documents=resolved_documents,
        conditional_documents=[
            {"doc_id": doc_id, "condition": condition} for doc_id, condition in sorted(set(conditional_doc_ids))
        ],
        excluded_documents=excluded_documents,
        resolved_rules=resolved_rules,
        exclusions=exclusions,
        conflicts=conflicts,
        findings=findings,
        enforcement_claim=enforcement_claim,
        gates_active=gates_active,
        labels=labels,
        resolved_set_digest=resolved_set_digest,
    )
    result.nested_local_policy = nested_records  # type: ignore[attr-defined]
    result.adoption_state = adoption_state  # type: ignore[attr-defined]
    result.adoption_authority_ref = adoption_authority_ref  # type: ignore[attr-defined]
    result.adoption_ref = adoption_ref  # type: ignore[attr-defined]
    result.adoption_sha256 = adoption_sha256  # type: ignore[attr-defined]
    result.installation_pin = installation_pin  # type: ignore[attr-defined]
    return result


# ---------------------------------------------------------------------------
# Context receipts
# ---------------------------------------------------------------------------


def _normalize_inputs(inputs: typing.Sequence[typing.Mapping[str, object]]) -> typing.List[typing.Dict[str, object]]:
    normalized = []
    for item in inputs:
        normalized.append(
            {
                "kind": str(item.get("kind")),
                "path": str(item.get("path")),
                "bytes": int(typing.cast(int, item.get("bytes"))),
                "sha256": str(item.get("sha256")),
            }
        )
    normalized.sort(key=lambda item: (item["kind"], item["path"], item["sha256"]))
    return normalized


def invalidation_digest(inputs: typing.Sequence[typing.Mapping[str, object]]) -> str:
    return canonical_digest(_normalize_inputs(inputs))


def _resolution_invalidation_inputs(
    contract_raw: bytes,
    resolution: models.ResolutionResult,
    *,
    adoption: typing.Optional[typing.Dict[str, object]] = None,
    adoption_ref: typing.Optional[str] = None,
    adoption_sha256: typing.Optional[str] = None,
    target: typing.Optional[typing.Dict[str, object]] = None,
    host_session: typing.Optional[typing.Dict[str, object]] = None,
    task_authority_ref: typing.Optional[str] = None,
) -> typing.List[typing.Dict[str, object]]:
    inputs: typing.List[typing.Dict[str, object]] = [
        {
            "kind": "contract",
            "path": CONTRACT_RELPATH,
            "bytes": len(contract_raw),
            "sha256": sha256_upper(contract_raw),
        }
    ]
    for document in resolution.resolved_documents:
        inputs.append({"kind": "document", "path": document.path, "bytes": document.bytes, "sha256": document.sha256})
    if adoption is not None:
        adoption_bytes = canonical_bytes(adoption)
        inputs.append(
            {
                "kind": "adoption-record",
                "path": adoption_ref or "local_adoption",
                "bytes": len(adoption_bytes),
                "sha256": sha256_upper(adoption_bytes),
            }
        )
    for record in getattr(resolution, "nested_local_policy", []) or []:
        inputs.append(
            {
                "kind": "nested-local-policy",
                "path": str(record["path"]),
                "bytes": int(typing.cast(int, record["bytes"])),
                "sha256": str(record["sha256"]),
            }
        )
    if target is not None:
        role_evidence = typing.cast(typing.List[object], target.get("role_evidence") or [])
        evidence_bytes = canonical_bytes(role_evidence)
        inputs.append(
            {
                "kind": "role-evidence",
                "path": "role-evidence:%s:%s" % (target.get("target_repo"), target.get("workspace_role")),
                "bytes": len(evidence_bytes),
                "sha256": sha256_upper(evidence_bytes),
            }
        )
    if host_session is not None and host_session.get("profile_digest"):
        inputs.append(
            {
                "kind": "host-profile",
                "path": "host-profile:%s" % host_session.get("host_build_sha256"),
                "bytes": len(str(host_session.get("profile_digest"))),
                "sha256": sha256_upper(str(host_session.get("profile_digest")).encode("utf-8")),
            }
        )
    if task_authority_ref:
        encoded = task_authority_ref.encode("utf-8")
        inputs.append(
            {
                "kind": "task-authority",
                "path": "task-authority",
                "bytes": len(encoded),
                "sha256": sha256_upper(encoded),
            }
        )
    return inputs


_INVALIDATION_KINDS = (
    "contract",
    "document",
    "adoption-record",
    "nested-local-policy",
    "instruction-baseline",
    "role-evidence",
    "host-profile",
    "task-authority",
)


def build_packaging_binding(
    repo_root: Path,
    *,
    detached_binding_evidence_ref: str,
    detached_binding_sha256: str,
    commands: typing.Sequence[typing.Mapping[str, object]],
    stage_a_feasibility_ref: str,
    c1_dependency_consumption_used: bool,
    dependency_closure_verified: bool,
) -> typing.Dict[str, object]:
    identity = load_manifest_binding(repo_root)
    binding = {
        "manifest_bytes": identity["manifest_bytes"],
        "manifest_lf": identity["manifest_lf"],
        "manifest_sha256": identity["manifest_sha256"],
        "manifest_path": identity["manifest_path"],
        "detached_binding_evidence_ref": detached_binding_evidence_ref,
        "detached_binding_sha256": detached_binding_sha256,
        "commands": [dict(command) for command in commands],
        "stage_a_feasibility_ref": stage_a_feasibility_ref,
        "c1_dependency_consumption_used": c1_dependency_consumption_used,
        "dependency_closure_verified": dependency_closure_verified,
    }
    return binding


_RECEIPT_NON_CLAIMS = [
    "a receipt is evidence of an observation, never authority, approval or permission",
    "a receipt does not prove reading comprehension or obedience",
    "a receipt is not valid past the next invalidating change; old receipts remain evidence of the old observation only",
]


def receipt_sha256(receipt: typing.Dict[str, object]) -> str:
    """Detached receipt identity (lowercase hex over canonical bytes)."""
    return sha256_raw(canonical_bytes(receipt))


def validate_receipt_document(
    receipt: typing.Dict[str, object],
    schemas: typing.Dict[str, typing.Dict[str, object]],
    *,
    repo_root: typing.Optional[Path] = None,
    contract: typing.Optional[typing.Dict[str, object]] = None,
    contract_raw: typing.Optional[bytes] = None,
) -> typing.List[models.GovernanceFinding]:
    """Validate one context receipt: shape, observation typing and authoritative re-reads."""
    findings: typing.List[models.GovernanceFinding] = []
    schema_findings = validate_json_schema(receipt, schemas["receipt"], root_schema=schemas["receipt"])
    for message in schema_findings:
        findings.append(models.GovernanceFinding("GR-09", "FAIL", message))
    if schema_findings:
        return findings
    route_id = receipt.get("route_id")
    route_family = receipt.get("route_family")
    observation_type = receipt.get("observation_type")
    if models.ROUTE_FAMILY_OF.get(str(route_id)) != route_family:
        findings.append(models.GovernanceFinding("GR-09", "FAIL", "route_family does not match route_id"))
    if route_id in models.BOUNDARY_OBSERVATION_OF:
        if observation_type != models.BOUNDARY_OBSERVATION_OF[typing.cast(str, route_id)]:
            findings.append(
                models.GovernanceFinding(
                    "GR-09", "FAIL", "a session-boundary receipt must keep its matching observation type", str(route_id)
                )
            )
    elif observation_type not in ("fresh-start", "protected-operation"):
        findings.append(models.GovernanceFinding("GR-09", "FAIL", "non-boundary receipt observation type is invalid"))
    digest_record = receipt.get("invalidation_inputs_digest")
    if isinstance(digest_record, dict):
        declared = _normalize_inputs(typing.cast(typing.List[typing.Mapping[str, object]], digest_record.get("inputs") or []))
        if not declared:
            findings.append(models.GovernanceFinding("GR-09", "FAIL", "the invalidation digest has no inputs"))
        else:
            if invalidation_digest(declared) != digest_record.get("digest"):
                findings.append(models.GovernanceFinding("GR-09", "FAIL", "the declared digest is not over the declared inputs"))
            for item in declared:
                if item["kind"] not in _INVALIDATION_KINDS:
                    findings.append(models.GovernanceFinding("GR-09", "FAIL", "invalidation input kind is not closed", item["kind"]))
    else:
        findings.append(models.GovernanceFinding("GR-09", "FAIL", "invalidation_inputs_digest is missing"))
    integrity = receipt.get("integrity")
    if isinstance(integrity, dict) and integrity.get("verification_status") not in (
        "UNVERIFIED",
        "RECONCILED-AGAINST-AUTHORITATIVE-INPUTS",
        "MISMATCH",
    ):
        findings.append(models.GovernanceFinding("GR-09", "FAIL", "receipt verification_status is not closed"))
    if contract is not None and contract_raw is not None:
        expected_contract_sha = sha256_upper(contract_raw)
        contract_block = receipt.get("contract")
        if not isinstance(contract_block, dict) or contract_block.get("contract_sha256") != expected_contract_sha:
            findings.append(models.GovernanceFinding("GR-09", "FAIL", "receipt does not bind the current contract sha256"))
        if contract_block.get("contract_version") != contract.get("contract_version"):
            findings.append(models.GovernanceFinding("GR-09", "FAIL", "receipt contract version mismatch"))
    # Authoritative re-read of every required document (a receipt cannot assert bytes).
    required = receipt.get("required_documents")
    if isinstance(required, list):
        for document in required:
            if not isinstance(document, dict):
                continue
            path = document.get("path")
            if not isinstance(path, str) or repo_root is None:
                continue
            try:
                data = read_repo_bytes(repo_root, path)
            except GovernanceError as error:
                findings.append(models.GovernanceFinding("GR-09", "FAIL", "required document is unreadable: %s" % error, path))
                continue
            if len(data) != document.get("bytes") or sha256_upper(data) != document.get("sha256"):
                findings.append(
                    models.GovernanceFinding("GR-09", "FAIL", "required document hash does not match authoritative bytes", path)
                )
            if document.get("read_status") != "read-verified":
                findings.append(models.GovernanceFinding("GR-09", "FAIL", "a required document is not read-verified", path))
    return findings


def _recompute_input(
    item: typing.Dict[str, object],
    repo_root: Path,
    *,
    current_target: typing.Optional[typing.Dict[str, object]],
    current_host_session: typing.Optional[typing.Dict[str, object]],
    current_authority_ref: typing.Optional[str],
) -> typing.Dict[str, object]:
    kind = str(item["kind"])
    if kind in ("contract", "document", "adoption-record", "nested-local-policy", "instruction-baseline"):
        try:
            data = read_repo_bytes(repo_root, str(item["path"]))
        except GovernanceError:
            return {**item, "bytes": -1, "sha256": "", "actual_present": False}
        return {"kind": kind, "path": str(item["path"]), "bytes": len(data), "sha256": sha256_upper(data)}
    if kind == "role-evidence" and current_target is not None:
        evidence = canonical_bytes(typing.cast(typing.List[object], current_target.get("role_evidence") or []))
        return {
            "kind": kind,
            "path": "role-evidence:%s:%s" % (current_target.get("target_repo"), current_target.get("workspace_role")),
            "bytes": len(evidence),
            "sha256": sha256_upper(evidence),
        }
    if kind == "host-profile" and current_host_session is not None and current_host_session.get("profile_digest"):
        profile = str(current_host_session.get("profile_digest"))
        return {
            "kind": kind,
            "path": "host-profile:%s" % current_host_session.get("host_build_sha256"),
            "bytes": len(profile),
            "sha256": sha256_upper(profile.encode("utf-8")),
        }
    if kind == "task-authority" and current_authority_ref:
        encoded = current_authority_ref.encode("utf-8")
        return {"kind": kind, "path": "task-authority", "bytes": len(encoded), "sha256": sha256_upper(encoded)}
    return dict(item)


def compute_current_digest(
    receipt: typing.Dict[str, object],
    repo_root: Path,
    *,
    current_target: typing.Optional[typing.Dict[str, object]] = None,
    current_host_session: typing.Optional[typing.Dict[str, object]] = None,
    current_authority_ref: typing.Optional[str] = None,
) -> typing.Tuple[str, typing.List[typing.Dict[str, object]]]:
    """Re-read every bound input at admission time and report differing inputs."""
    digest_record = receipt.get("invalidation_inputs_digest")
    declared_inputs = []
    if isinstance(digest_record, dict):
        declared_inputs = _normalize_inputs(typing.cast(typing.List[typing.Mapping[str, object]], digest_record.get("inputs") or []))
    current_inputs = [
        _recompute_input(
            item,
            repo_root,
            current_target=current_target,
            current_host_session=current_host_session,
            current_authority_ref=current_authority_ref,
        )
        for item in declared_inputs
    ]
    differing: typing.List[typing.Dict[str, object]] = []
    for declared, current in zip(declared_inputs, current_inputs):
        if declared.get("sha256") != current.get("sha256") or current.get("bytes") == -1:
            differing.append(
                {
                    "kind": declared["kind"],
                    "path": declared["path"],
                    "expected_sha256": declared["sha256"] or None,
                    "actual_sha256": (current.get("sha256") or None),
                }
            )
    current_inputs = [item for item in current_inputs if item.get("bytes") != -1]
    return invalidation_digest(current_inputs), differing


def admit(
    contract: typing.Dict[str, object],
    contract_raw: bytes,
    receipt: typing.Optional[typing.Dict[str, object]],
    schemas: typing.Dict[str, typing.Dict[str, object]],
    *,
    repo_root: Path,
    operation_class: str,
    decision_id: str,
    requested_at_utc: str,
    operation_ref: typing.Dict[str, object],
    authority_ref: str,
    current_target: typing.Optional[typing.Dict[str, object]] = None,
    current_role: typing.Optional[str] = None,
    current_repo: typing.Optional[str] = None,
    current_pin: typing.Optional[typing.Dict[str, object]] = None,
    session_boundary_utc: typing.Optional[str] = None,
    current_authority_ref: typing.Optional[str] = None,
    current_host_session: typing.Optional[typing.Dict[str, object]] = None,
    current_adoption: typing.Optional[typing.Dict[str, object]] = None,
    limitations: typing.Optional[typing.Sequence[str]] = None,
) -> models.AdmissionOutcome:
    """Admission recheck for one protected operation class.

    A record, not a prompt: ALLOW is only after a fresh authoritative re-read; a
    missing/stale/forged receipt, a role/target move, a pin change, a boundary
    before the observation, a withdrawn adoption or an unresolved conflict
    DENIES/BLOCKS dependent work while diagnostic reads remain allowed.
    """
    if operation_class not in OPERATION_CLASS_SET:
        raise GovernanceError("unknown_operation_class", "operation_class is not in the closed vocabulary")
    recheck: typing.Dict[str, object] = {
        "inputs_rehashed": False,
        "digest_before": None,
        "digest_after": None,
        "differing_inputs": [],
        "role_rechecked": False,
        "adoption_rechecked": True,
    }
    decision_limitations = list(limitations or [])
    if operation_class == "read-only-diagnostic":
        return _admission_outcome(
            schemas,
            decision_id=decision_id,
            operation_class=operation_class,
            decision="ALLOW",
            reason_code="READ_ONLY_DIAGNOSTIC_PERMITTED",
            requested_at_utc=requested_at_utc,
            operation_ref=operation_ref,
            receipt=receipt,
            recheck=recheck,
            authority_ref=authority_ref,
            limitations=decision_limitations + ["diagnostic reads remain allowed with the missing/stale source named"],
        )
    if receipt is None:
        return _admission_outcome(
            schemas,
            decision_id=decision_id,
            operation_class=operation_class,
            decision="DENY",
            reason_code="RECEIPT_INVALID",
            requested_at_utc=requested_at_utc,
            operation_ref=operation_ref,
            receipt=None,
            recheck=recheck,
            authority_ref=authority_ref,
            limitations=decision_limitations + ["no receipt was supplied for a protected operation class"],
        )
    # Shape/typing/digest-self-consistency: a malformed or contradicted receipt is DENIED.
    receipt_findings = validate_receipt_document(receipt, schemas, repo_root=None, contract=contract, contract_raw=contract_raw)
    if receipt_findings:
        return _admission_outcome(
            schemas,
            decision_id=decision_id,
            operation_class=operation_class,
            decision="DENY",
            reason_code="RECEIPT_INVALID",
            requested_at_utc=requested_at_utc,
            operation_ref=operation_ref,
            receipt=receipt,
            recheck=recheck,
            authority_ref=authority_ref,
            limitations=decision_limitations + [finding.message for finding in receipt_findings[:5]],
        )
    target = receipt.get("target") if isinstance(receipt.get("target"), dict) else {}
    task = receipt.get("task") if isinstance(receipt.get("task"), dict) else {}
    contract_block = receipt.get("contract") if isinstance(receipt.get("contract"), dict) else {}
    # Role / target identity recheck.
    recheck["role_rechecked"] = True
    if current_role is not None and current_role != target.get("workspace_role"):
        return _admission_outcome(
            schemas,
            decision_id=decision_id,
            operation_class=operation_class,
            decision="DENY",
            reason_code="ROLE_TARGET_MISMATCH",
            requested_at_utc=requested_at_utc,
            operation_ref=operation_ref,
            receipt=receipt,
            recheck=recheck,
            authority_ref=authority_ref,
            limitations=decision_limitations + ["the current workspace role differs from the receipt's target role"],
        )
    if current_repo is not None and current_repo != target.get("target_repo"):
        return _admission_outcome(
            schemas,
            decision_id=decision_id,
            operation_class=operation_class,
            decision="DENY",
            reason_code="ROLE_TARGET_MISMATCH",
            requested_at_utc=requested_at_utc,
            operation_ref=operation_ref,
            receipt=receipt,
            recheck=recheck,
            authority_ref=authority_ref,
            limitations=decision_limitations + ["the current target repository differs from the receipt's target"],
        )
    # Authority isolation: a source-library grant never authorizes consumer work.
    consumer_authority = str(task.get("task_authority_ref") or "")
    if target.get("workspace_role") == "consumer" and re.search(r"(AEGIS-APR-\d{3}|^APR-\d{3})", consumer_authority):
        return _admission_outcome(
            schemas,
            decision_id=decision_id,
            operation_class=operation_class,
            decision="DENY",
            reason_code="AUTHORITY_ISOLATION_VIOLATION",
            requested_at_utc=requested_at_utc,
            operation_ref=operation_ref,
            receipt=receipt,
            recheck=recheck,
            authority_ref=authority_ref,
            limitations=decision_limitations + ["a source-library register entry cannot authorize consumer-repository work"],
        )
    if contract_block.get("contract_sha256") != sha256_upper(contract_raw):
        return _admission_outcome(
            schemas,
            decision_id=decision_id,
            operation_class=operation_class,
            decision="DENY",
            reason_code="RECEIPT_CONTRACT_MISMATCH",
            requested_at_utc=requested_at_utc,
            operation_ref=operation_ref,
            receipt=receipt,
            recheck=recheck,
            authority_ref=authority_ref,
            limitations=decision_limitations + ["the receipt binds a different contract sha256 than the current bytes"],
        )
    if current_pin is not None:
        declared_pin = contract_block.get("approved_upstream_pin") if isinstance(contract_block.get("approved_upstream_pin"), dict) else {}
        if declared_pin.get("commit") != current_pin.get("commit") or declared_pin.get("tree") != current_pin.get("tree"):
            return _admission_outcome(
                schemas,
                decision_id=decision_id,
                operation_class=operation_class,
                decision="BLOCKED",
                reason_code="PIN_CHANGED",
                requested_at_utc=requested_at_utc,
                operation_ref=operation_ref,
                receipt=receipt,
                recheck=recheck,
                authority_ref=authority_ref,
                limitations=decision_limitations
                + ["approved pin changed: receipt %s -> current %s" % (declared_pin.get("commit"), current_pin.get("commit"))],
            )
    # Session-boundary ordering: a pre-boundary observation cannot authorize the next protected operation.
    if session_boundary_utc is not None and str(receipt.get("observed_at_utc")) <= str(session_boundary_utc):
        return _admission_outcome(
            schemas,
            decision_id=decision_id,
            operation_class=operation_class,
            decision="BLOCKED",
            reason_code="OBSERVATION_PRE_BOUNDARY",
            requested_at_utc=requested_at_utc,
            operation_ref=operation_ref,
            receipt=receipt,
            recheck=recheck,
            authority_ref=authority_ref,
            limitations=decision_limitations + ["the receipt was observed before the session boundary; re-observe"],
        )
    # Adoption recheck for consumer work.
    if target.get("workspace_role") == "consumer":
        if current_adoption is None:
            adoption_state = typing.cast(typing.Dict[str, object], receipt.get("local_adoption") or {}).get("state")
            if adoption_state in ("unknown", "not-adopted"):
                return _admission_outcome(
                    schemas,
                    decision_id=decision_id,
                    operation_class=operation_class,
                    decision="BLOCKED",
                    reason_code="ADOPTION_MISSING",
                    requested_at_utc=requested_at_utc,
                    operation_ref=operation_ref,
                    receipt=receipt,
                    recheck=recheck,
                    authority_ref=authority_ref,
                    limitations=decision_limitations + ["consumer work requires a current local adoption record"],
                )
        else:
            revoked = current_adoption.get("revoked_at_utc")
            if revoked is not None:
                return _admission_outcome(
                    schemas,
                    decision_id=decision_id,
                    operation_class=operation_class,
                    decision="BLOCKED",
                    reason_code="ADOPTION_WITHDRAWN",
                    requested_at_utc=requested_at_utc,
                    operation_ref=operation_ref,
                    receipt=receipt,
                    recheck=recheck,
                    authority_ref=authority_ref,
                    limitations=decision_limitations + ["local adoption revoked at %s" % revoked],
                )
    # Full authoritative re-read: any differing bound input blocks.
    digest_after, differing = compute_current_digest(
        receipt,
        repo_root,
        current_target=current_target,
        current_host_session=current_host_session,
        current_authority_ref=current_authority_ref,
    )
    digest_record = receipt.get("invalidation_inputs_digest") if isinstance(receipt.get("invalidation_inputs_digest"), dict) else {}
    recheck.update(
        {
            "inputs_rehashed": True,
            "digest_before": digest_record.get("digest"),
            "digest_after": digest_after,
            "differing_inputs": differing,
        }
    )
    if differing:
        return _admission_outcome(
            schemas,
            decision_id=decision_id,
            operation_class=operation_class,
            decision="BLOCKED",
            reason_code="OBSERVATION_STALE",
            requested_at_utc=requested_at_utc,
            operation_ref=operation_ref,
            receipt=receipt,
            recheck=recheck,
            authority_ref=authority_ref,
            limitations=decision_limitations
            + ["bound inputs changed after observation: %s" % ", ".join(item["path"] for item in differing[:5])],
        )
    if target.get("workspace_role") == "consumer" and current_adoption is not None:
        adoption_findings = validate_json_schema(current_adoption, schemas["adoption"], root_schema=schemas["adoption"])
        if adoption_findings:
            return _admission_outcome(
                schemas,
                decision_id=decision_id,
                operation_class=operation_class,
                decision="BLOCKED",
                reason_code="ADOPTION_MISSING",
                requested_at_utc=requested_at_utc,
                operation_ref=operation_ref,
                receipt=receipt,
                recheck=recheck,
                authority_ref=authority_ref,
                limitations=decision_limitations + ["the current adoption record is malformed"],
            )
    # Authoritative document re-read: an edited receipt can never satisfy admission.
    authoritative_findings = validate_receipt_document(
        receipt, schemas, repo_root=repo_root, contract=contract, contract_raw=contract_raw
    )
    if authoritative_findings:
        return _admission_outcome(
            schemas,
            decision_id=decision_id,
            operation_class=operation_class,
            decision="DENY",
            reason_code="RECEIPT_INVALID",
            requested_at_utc=requested_at_utc,
            operation_ref=operation_ref,
            receipt=receipt,
            recheck=recheck,
            authority_ref=authority_ref,
            limitations=decision_limitations + [finding.message for finding in authoritative_findings[:5]],
        )
    host_session = receipt.get("host_session") if isinstance(receipt.get("host_session"), dict) else {}
    if host_session.get("gates_active") != "none":
        return _admission_outcome(
            schemas,
            decision_id=decision_id,
            operation_class=operation_class,
            decision="DENY",
            reason_code="HOST_CLAIM_UNSUPPORTED",
            requested_at_utc=requested_at_utc,
            operation_ref=operation_ref,
            receipt=receipt,
            recheck=recheck,
            authority_ref=authority_ref,
            limitations=decision_limitations + ["a claimed active host gate needs composition/profile evidence (none exists here)"],
        )
    return _admission_outcome(
        schemas,
        decision_id=decision_id,
        operation_class=operation_class,
        decision="ALLOW",
        reason_code="FRESH_RECEIPT_REVALIDATED",
        requested_at_utc=requested_at_utc,
        operation_ref=operation_ref,
        receipt=receipt,
        recheck=recheck,
        authority_ref=authority_ref,
        limitations=decision_limitations,
    )


def _admission_outcome(
    schemas: typing.Dict[str, typing.Dict[str, object]],
    *,
    decision_id: str,
    operation_class: str,
    decision: str,
    reason_code: str,
    requested_at_utc: str,
    operation_ref: typing.Dict[str, object],
    receipt: typing.Optional[typing.Dict[str, object]],
    recheck: typing.Dict[str, object],
    authority_ref: str,
    limitations: typing.Sequence[str],
) -> models.AdmissionOutcome:
    record = {
        "schema": ADMISSION_SCHEMA_ID,
        "decision_id": decision_id,
        "operation_class": operation_class,
        "operation_ref": operation_ref,
        "requested_at_utc": requested_at_utc,
        "receipt_id": receipt.get("receipt_id") if isinstance(receipt, dict) else None,
        "receipt_sha256": receipt_sha256(receipt) if isinstance(receipt, dict) else None,
        "recheck": {
            "inputs_rehashed": bool(recheck.get("inputs_rehashed")),
            "digest_before": recheck.get("digest_before"),
            "digest_after": recheck.get("digest_after"),
            "differing_inputs": list(typing.cast(typing.List[object], recheck.get("differing_inputs") or [])),
            "role_rechecked": bool(recheck.get("role_rechecked")),
            "adoption_rechecked": bool(recheck.get("adoption_rechecked")),
        },
        "decision": decision,
        "reason_code": reason_code,
        "authority_ref": authority_ref,
        "evidence_refs": [],
        "limitations": list(limitations),
    }
    schema_findings = validate_json_schema(record, schemas["admission"], root_schema=schemas["admission"])
    if schema_findings:
        raise GovernanceError("admission_schema_invalid", "; ".join(schema_findings[:10]))
    return models.AdmissionOutcome(
        decision=decision,
        reason_code=reason_code,
        recheck=dict(recheck),
        decision_record=record,
    )


# ---------------------------------------------------------------------------
# Supporting determinism, preservation, budget, host-claim, rollback and
# manual-only helpers (used by the acceptance fixtures/tests)
# ---------------------------------------------------------------------------


def preservation_manifest(
    repo_root: Path,
    relpaths: typing.Sequence[str],
) -> typing.Dict[str, object]:
    """Bounded before/after manifest of explicitly supplied paths (case 23)."""
    entries: typing.List[typing.Dict[str, object]] = []
    for relpath in sorted(set(relpaths)):
        identity = file_identity(repo_root, relpath)
        entries.append(identity)
    return {
        "schema": "aegis.preservation-manifest/1",
        "entries": entries,
        "digest": canonical_digest(entries),
    }


def preservation_diff(
    before: typing.Dict[str, object],
    after: typing.Dict[str, object],
) -> typing.List[str]:
    """Return only the changed paths between two preservation manifests."""
    before_entries = {
        str(entry["path"]): entry for entry in typing.cast(typing.List[typing.Dict[str, object]], before.get("entries") or [])
    }
    after_entries = {
        str(entry["path"]): entry for entry in typing.cast(typing.List[typing.Dict[str, object]], after.get("entries") or [])
    }
    changed = []
    for path in sorted(set(before_entries) | set(after_entries)):
        if before_entries.get(path) != after_entries.get(path):
            changed.append(path)
    return changed


def build_budget_record(category: str, item_ref: str, count: int) -> typing.Dict[str, object]:
    """One typed budget event.  Budget categories are never converted into each other."""
    if category not in models.BUDGET_CATEGORIES:
        raise GovernanceError("unknown_budget_category", "budget category is not in the closed vocabulary", category)
    if not isinstance(count, int) or isinstance(count, bool) or count < 0:
        raise GovernanceError("invalid_budget_count", "budget count must be a non-negative integer")
    return {"category": category, "item_ref": item_ref, "count": count}


def sum_budgets(records: typing.Sequence[typing.Mapping[str, object]]) -> typing.Dict[str, int]:
    """Per-category totals; unknown categories raise (no cross-category conversion)."""
    totals = {category: 0 for category in models.BUDGET_CATEGORIES}
    for record in records:
        category = str(record.get("category"))
        if category not in totals:
            raise GovernanceError("unknown_budget_category", "budget category is not in the closed vocabulary", category)
        count = record.get("count")
        if not isinstance(count, int) or isinstance(count, bool) or count < 0:
            raise GovernanceError("invalid_budget_count", "budget count must be a non-negative integer")
        totals[category] += count
    return totals


def validate_host_claim(host: typing.Mapping[str, object]) -> typing.List[models.GovernanceFinding]:
    """Claim discipline: a host claim needs the evidence its label promises (case 25)."""
    findings: typing.List[models.GovernanceFinding] = []
    claim = host.get("claim")
    if claim not in models.HOST_CLAIM_LABELS:
        findings.append(models.GovernanceFinding("GR-11", "FAIL", "host claim label is not closed", str(claim)))
        return findings
    evidence_refs = host.get("evidence_refs")
    if claim in ("OBSERVED-TESTED", "OBSERVED-IDENTITY-ONLY") and (not isinstance(evidence_refs, list) or not evidence_refs):
        findings.append(models.GovernanceFinding("GR-11", "FAIL", "an observed host claim requires evidence refs", str(claim)))
    if claim == "OBSERVED-TESTED":
        if not isinstance(host.get("tested_boundaries"), list) or not host.get("tested_boundaries"):
            findings.append(models.GovernanceFinding("GR-11", "FAIL", "an OBSERVED-TESTED claim requires the tested boundaries"))
        if not isinstance(host.get("limitations"), list):
            findings.append(models.GovernanceFinding("GR-11", "FAIL", "an OBSERVED-TESTED claim requires limitations"))
    return findings


def plan_rollback(
    *,
    current_contract: typing.Dict[str, object],
    target_contract: typing.Dict[str, object],
    target_contract_raw: bytes,
    target_manifest_sha256: str,
    revocation_state: typing.Optional[typing.Dict[str, object]],
    local_policy_paths: typing.Sequence[str] = (),
    triggers: typing.Optional[typing.Sequence[str]] = None,
) -> typing.Dict[str, object]:
    """Deterministic rollback record (case 26).

    Restores the approved package identity without restoring revoked authority or
    deleting local policy: a withdrawal stays withdrawn and local policy files are
    listed as retained, never removed.
    """
    if not HEX64_UPPER_RE.match(target_manifest_sha256):
        raise GovernanceError("invalid_manifest_sha256", "target manifest sha256 must be uppercase 64-hex")
    revoked = None
    if isinstance(revocation_state, dict) and revocation_state.get("revoked_at_utc") is not None:
        revoked = {
            "revoked_at_utc": revocation_state.get("revoked_at_utc"),
            "revocation_authority": revocation_state.get("revocation_authority"),
        }
    return {
        "schema": "aegis.governance-rollback/1",
        "from_contract_version": str(current_contract.get("contract_version")),
        "to_contract_version": str(target_contract.get("contract_version")),
        "to_contract_sha256": sha256_upper(target_contract_raw),
        "to_manifest_sha256": target_manifest_sha256,
        "restores_payload_bytes": True,
        "restores_authority": False,
        "revoked_authority_restored": False,
        "revocation_state": revoked,
        "local_policy_deletions": [],
        "local_policy_retained": sorted(str(path) for path in local_policy_paths),
        "triggers": sorted(
            triggers
            or (
                "a false admission under the new governance dependency",
                "a broken install of the governance payload",
                "an unusable restoration of the previous package",
                "the consumer owner's withdrawal of the adoption record",
            )
        ),
        "non_claims": [
            "a rollback record is a plan, not an executed rollback",
            "rolling back bytes never restores revoked authority",
        ],
    }


def skill_invocation_decision(
    dependencies: typing.Dict[str, object],
    skill_id: str,
    *,
    mode: str = "auto",
    override_ref: typing.Optional[str] = None,
) -> typing.Dict[str, object]:
    """MANUAL-ONLY skills are never auto-applied (case 22).

    Discovery may report a manual-only skill; only a human-initiated invocation
    with a recorded consumer-local authorization may use it.  This is a decision
    record, not a host enforcement.
    """
    entrypoints = dependencies.get("entrypoints")
    if not isinstance(entrypoints, list):
        raise GovernanceError("invalid_governance_dependencies", "entrypoints must be an array")
    entry = None
    for candidate in entrypoints:
        if isinstance(candidate, dict) and candidate.get("name") == skill_id:
            entry = candidate
            break
    if entry is None:
        return {
            "skill_id": skill_id,
            "decision": "DENY",
            "reason_code": "SKILL_NOT_DECLARED",
            "manual_only": None,
            "limitations": ["the skill is not a declared shipped entrypoint; an undeclared skill cannot claim governance coverage"],
        }
    manual_only = bool(entry.get("manual_only"))
    if mode not in ("auto", "discovery", "explicit"):
        raise GovernanceError("unknown_invocation_mode", "invocation mode is not closed", mode)
    if manual_only and mode in ("auto", "discovery"):
        return {
            "skill_id": skill_id,
            "decision": "DENY",
            "reason_code": "MANUAL_ONLY_AUTO_INVOCATION_DENIED",
            "manual_only": True,
            "limitations": ["MANUAL-ONLY skills are never auto-applied; the denial is recorded, not host-enforced"],
        }
    if manual_only and mode == "explicit":
        if not override_ref:
            return {
                "skill_id": skill_id,
                "decision": "DENY",
                "reason_code": "MANUAL_ONLY_OVERRIDE_REQUIRED",
                "manual_only": True,
                "limitations": ["a human-initiated manual-only invocation needs a recorded consumer-local authorization record"],
            }
        return {
            "skill_id": skill_id,
            "decision": "ALLOW",
            "reason_code": "MANUAL_ONLY_EXPLICIT_AUTHORIZED",
            "manual_only": True,
            "limitations": [
                "the override reference is consumer-local; this seat cannot verify the authorization record's content",
                "an explicit invocation is not a host-enforced permission",
            ],
        }
    return {
        "skill_id": skill_id,
        "decision": "ALLOW",
        "reason_code": "DECLARED_ENTRYPOINT",
        "manual_only": False,
        "limitations": ["a declared dependency is packaging metadata, not runtime enforcement"],
    }


def validate_governance_dependencies_at_repo(repo_root: Path) -> typing.List[models.GovernanceFinding]:
    """Validate the committed governance-dependency declaration against the contract."""
    schemas = load_schemas(repo_root)
    contract, contract_raw = load_contract(repo_root)
    contract_findings = validate_contract_document(
        contract,
        schemas,
        repo_root=repo_root,
        inventory=load_inventory(repo_root),
        projection=load_projection(repo_root),
        raw_bytes=contract_raw,
    )
    findings: typing.List[models.GovernanceFinding] = []
    for finding in contract_findings:
        findings.append(models.GovernanceFinding("GR-01", finding.status, "contract: " + finding.message, finding.ref))
    document = read_repo_json(repo_root, GOVERNANCE_DEPENDENCIES_RELPATH)
    if not isinstance(document, dict):
        return findings + [models.GovernanceFinding("GR-07", "FAIL", "governance dependencies are not a JSON object")]
    for message in validate_governance_dependencies_document(typing.cast(typing.Dict[str, object], document), contract):
        findings.append(models.GovernanceFinding("GR-07", "FAIL", message, GOVERNANCE_DEPENDENCIES_RELPATH))
    skills = scan_skill_entrypoints(repo_root)
    if len(typing.cast(typing.List[object], document.get("entrypoints") or [])) != len(skills):
        findings.append(
            models.GovernanceFinding(
                "GR-07",
                "FAIL",
                "the declaration does not cover every shipped skill entrypoint (%d of %d)"
                % (len(typing.cast(typing.List[object], document.get("entrypoints") or [])), len(skills)),
            )
        )
    return findings


def validate_skill_dependency(
    dependencies_document: typing.Dict[str, object],
    skill_id: str,
    contract: typing.Dict[str, object],
    contract_raw: bytes,
) -> typing.List[models.GovernanceFinding]:
    """Resolve one skill's declared governance dependency against a target contract.

    A declared contract sha256/version that does not match the target contract
    blocks with both identities named; an undeclared skill cannot claim coverage.
    """
    findings: typing.List[models.GovernanceFinding] = []
    entrypoints = dependencies_document.get("entrypoints")
    if not isinstance(entrypoints, list):
        return [models.GovernanceFinding("GR-07", "FAIL", "the dependency declaration has no entrypoints")]
    entry = None
    for candidate in entrypoints:
        if isinstance(candidate, dict) and candidate.get("name") == skill_id:
            entry = candidate
            break
    if entry is None:
        return [models.GovernanceFinding("GR-07", "FAIL", "the skill is not a declared entrypoint", skill_id)]
    contract_binding = entry.get("contract") if isinstance(entry.get("contract"), dict) else {}
    target_version = str(contract.get("contract_version"))
    accepted_versions = contract_binding.get("accepted_versions")
    if not isinstance(accepted_versions, list) or target_version not in [str(item) for item in accepted_versions]:
        findings.append(
            models.GovernanceFinding(
                "GR-07",
                "BLOCKED",
                "contract version mismatch: the skill accepts %s but the target contract is %s"
                % (accepted_versions, target_version),
                skill_id,
            )
        )
    expected_sha = contract_binding.get("expected_sha256_when_bundled")
    actual_sha = sha256_upper(contract_raw)
    if expected_sha != actual_sha:
        findings.append(
            models.GovernanceFinding(
                "GR-07",
                "BLOCKED",
                "contract sha256 mismatch: the skill expects %s but the target contract is %s"
                % (expected_sha, actual_sha),
                skill_id,
            )
        )
    return findings


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def _print_json(value: object) -> None:
    sys.stdout.write(json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n")


def _parse_kv_conditions(values: typing.Sequence[str]) -> typing.Dict[str, bool]:
    conditions: typing.Dict[str, bool] = {}
    for value in values:
        if "=" not in value:
            raise GovernanceError("invalid_condition", "conditions use NAME=true|false form", value)
        name, raw = value.split("=", 1)
        if name not in CONDITION_RULE_SET:
            raise GovernanceError("unknown_condition", "condition is not in the closed vocabulary", name)
        conditions[name] = raw.strip().lower() in ("1", "true", "yes")
    return conditions


BINDING_SCHEMA_ID = "aegis.governance-payload-binding/1"


def load_packaging_binding(repo_root: Path, binding_path: Path) -> typing.Dict[str, object]:
    """Load and validate a detached packaging binding for a receipt.

    The binding is evidence outside the payload root; it records the manifest
    identity, the contract identity, the executed commands and their exit codes.
    A receipt cannot be derived without it: the manifest identity is re-checked
    against the committed manifest, never asserted by the receipt alone.
    """
    try:
        binding_bytes = Path(binding_path).read_bytes()
    except OSError as error:
        raise GovernanceError("binding_unreadable", "cannot read the detached binding: %s" % error, str(binding_path))
    try:
        binding = json.loads(binding_bytes.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise GovernanceError("binding_invalid_json", "the detached binding is not valid UTF-8 JSON", str(binding_path))
    if not isinstance(binding, dict) or binding.get("schema") != BINDING_SCHEMA_ID:
        raise GovernanceError("binding_invalid", "the detached binding does not use %r" % BINDING_SCHEMA_ID, str(binding_path))
    identity = load_manifest_binding(repo_root)
    manifest = binding.get("manifest")
    if not isinstance(manifest, dict):
        raise GovernanceError("binding_invalid", "the detached binding has no manifest identity")
    for key in ("bytes", "lf", "sha256"):
        expected = identity["manifest_" + key]
        if key == "sha256":
            if str(manifest.get(key)).upper() != str(expected).upper():
                raise GovernanceError("binding_mismatch", "binding manifest sha256 does not match the committed manifest")
        elif manifest.get(key) != expected:
            raise GovernanceError("binding_mismatch", "binding manifest %s does not match the committed manifest" % key)
    contract_identity = binding.get("contract") if isinstance(binding.get("contract"), dict) else {}
    contract, contract_raw = load_contract(repo_root)
    if contract_identity.get("sha256") != sha256_upper(contract_raw):
        raise GovernanceError("binding_mismatch", "binding contract sha256 does not match the committed contract")
    if contract_identity.get("version") != contract.get("contract_version"):
        raise GovernanceError("binding_mismatch", "binding contract version does not match the committed contract")
    commands = binding.get("commands")
    if not isinstance(commands, list) or len(commands) < 3:
        raise GovernanceError("binding_invalid", "the detached binding must record at least the three packaging commands")
    binding_record = {
        "manifest_bytes": identity["manifest_bytes"],
        "manifest_lf": identity["manifest_lf"],
        "manifest_sha256": identity["manifest_sha256"],
        "manifest_path": identity["manifest_path"],
        "detached_binding_evidence_ref": str(binding_path),
        "detached_binding_sha256": sha256_raw(binding_bytes),
        "commands": [dict(command) for command in commands],
        "stage_a_feasibility_ref": str(binding.get("stage_a_feasibility_ref") or ""),
        "c1_dependency_consumption_used": bool(binding.get("c1_dependency_consumption_used")),
        "dependency_closure_verified": bool(binding.get("dependency_closure_verified")),
    }
    if not binding_record["stage_a_feasibility_ref"]:
        raise GovernanceError("binding_invalid", "the detached binding must name the Stage A feasibility reference")
    return binding_record


def _cli_validate(repo_root: Path, arguments: typing.Sequence[str]) -> int:
    del arguments
    contract, raw_bytes, findings = validate_contract_at_repo(repo_root)
    status = "FAIL" if any(finding.status in ("FAIL", "BLOCKED") for finding in findings) else "PASS"
    _print_json(
        {
            "schema": OUTPUT_SCHEMA_ID,
            "artifact": "contract",
            "status": status,
            "contract_sha256": sha256_upper(raw_bytes),
            "contract_version": contract.get("contract_version"),
            "findings": [finding.as_dict() for finding in findings],
            "non_claims": ["a validate PASS is a structural observation, not approval or enforcement"],
        }
    )
    return EXIT_PASS if status == "PASS" else EXIT_FINDINGS


def _load_adoption(path_argument: typing.Optional[str]) -> typing.Tuple[typing.Optional[typing.Dict[str, object]], typing.Optional[str], typing.Optional[str]]:
    if not path_argument:
        return None, None, None
    path = Path(path_argument)
    try:
        data = path.read_bytes()
    except OSError as error:
        raise GovernanceError("adoption_unreadable", "cannot read the adoption record: %s" % error, path_argument)
    try:
        document = json.loads(data.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise GovernanceError("adoption_invalid_json", "the adoption record is not valid UTF-8 JSON", path_argument)
    if not isinstance(document, dict):
        raise GovernanceError("adoption_invalid", "the adoption record is not a JSON object", path_argument)
    return typing.cast(typing.Dict[str, object], document), path_argument, sha256_raw(data)


def _cli_resolve(repo_root: Path, arguments: typing.Sequence[str]) -> int:
    parser = _sub_parser("resolve")
    parser.add_argument("--role", required=True, choices=list(models.ROLE_IDS))
    parser.add_argument("--route", required=True, choices=list(models.ROUTE_IDS))
    parser.add_argument("--adoption", default=None)
    parser.add_argument("--nested-policy", action="append", default=[])
    parser.add_argument("--condition", action="append", default=[])
    parser.add_argument("--target-repo", default="ModernNomad-98/Project-Aegis")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(list(arguments))
    contract, contract_raw = load_contract(repo_root)
    adoption, adoption_ref, adoption_sha = _load_adoption(args.adoption)
    result = resolve(
        contract,
        role=args.role,
        route_id=args.route,
        repo_root=repo_root,
        conditions=_parse_kv_conditions(args.condition),
        adoption=adoption,
        adoption_ref=adoption_ref,
        adoption_sha256=adoption_sha,
        nested_policies=args.nested_policy,
        target={"target_repo": args.target_repo, "workspace_role": args.role, "role_evidence": ["cli"]},
    )
    payload = {
        "schema": OUTPUT_SCHEMA_ID,
        "contract_sha256": sha256_upper(contract_raw),
        "resolution": result.as_dict(),
        "non_claims": ["a resolved set is an observation, not approval or authority"],
    }
    _print_json(payload)
    del args.json
    return EXIT_PASS if result.status == "RESOLVED" else EXIT_FINDINGS


def _sub_parser(verb: str):
    import argparse

    parser = argparse.ArgumentParser(prog="python -m tools.aegis_preflight governance %s" % verb)
    return parser


def _cli_receipt(repo_root: Path, arguments: typing.Sequence[str]) -> int:
    parser = _sub_parser("receipt")
    parser.add_argument("--role", required=True, choices=list(models.ROLE_IDS))
    parser.add_argument("--route", required=True, choices=list(models.ROUTE_IDS))
    parser.add_argument("--observation-type", required=True, choices=list(models.OBSERVATION_TYPES))
    parser.add_argument("--receipt-id", required=True)
    parser.add_argument("--observed-at", required=True)
    parser.add_argument("--task-id", required=True)
    parser.add_argument("--task-ref", required=True)
    parser.add_argument("--task-authority-ref", required=True)
    parser.add_argument("--binding", required=True,
                        help="detached packaging binding JSON (manifest/contract identity + commands)")
    parser.add_argument("--adoption", default=None)
    parser.add_argument("--condition", action="append", default=[])
    args = parser.parse_args(list(arguments))
    schemas = load_schemas(repo_root)
    contract, contract_raw = load_contract(repo_root)
    adoption, adoption_ref, adoption_sha = _load_adoption(args.adoption)
    resolution = resolve(
        contract,
        role=args.role,
        route_id=args.route,
        repo_root=repo_root,
        conditions=_parse_kv_conditions(args.condition),
        adoption=adoption,
        adoption_ref=adoption_ref,
        adoption_sha256=adoption_sha,
        target={
            "target_repo": "ModernNomad-98/Project-Aegis",
            "target_kind": "source-library-checkout" if args.role == "source-library" else "consumer-copy",
            "workspace_role": args.role,
            "role_evidence": ["cli"],
        },
    )
    receipt = derive_receipt(
        contract,
        contract_raw,
        resolution,
        repo_root=repo_root,
        schemas=schemas,
        receipt_id=args.receipt_id,
        observation_type=args.observation_type,
        observed_at_utc=args.observed_at,
        task={
            "task_id": args.task_id,
            "task_ref": args.task_ref,
            "scope_summary": "cli-derived receipt",
            "task_authority_ref": args.task_authority_ref,
        },
        target={
            "target_repo": "ModernNomad-98/Project-Aegis",
            "target_kind": "source-library-checkout" if args.role == "source-library" else "consumer-copy",
            "workspace_role": args.role,
            "role_evidence": ["cli"],
        },
        host_session=_default_host_session(),
        instructions={"baseline_identity": None, "files": [], "budget_omissions": []},
        packaging_binding=load_packaging_binding(repo_root, Path(args.binding)),
        adoption=adoption,
        adoption_ref=adoption_ref,
        adoption_sha256=adoption_sha,
    )
    _print_json({"schema": OUTPUT_SCHEMA_ID, "receipt_sha256": receipt_sha256(receipt), "receipt": receipt})
    return EXIT_PASS


def _default_host_session() -> typing.Dict[str, object]:
    return {
        "host_product": None,
        "host_version": None,
        "host_build_sha256": None,
        "profile_digest": None,
        "session_id": None,
        "origin": None,
        "delegation_depth": None,
        "agent_preset": None,
        "requested_model_route": None,
        "reported_model_display": None,
        "reasoning_effort": None,
        "permission_preset": None,
        "sandbox_mode": None,
        "approval_policy": None,
        "gates_active": "none",
        "data_exit_paths": [],
    }


def _cli_admit(repo_root: Path, arguments: typing.Sequence[str]) -> int:
    parser = _sub_parser("admit")
    parser.add_argument("--receipt", required=True)
    parser.add_argument("--operation-class", required=True, choices=list(models.OPERATION_CLASSES))
    parser.add_argument("--decision-id", required=True)
    parser.add_argument("--requested-at", required=True)
    parser.add_argument("--authority-ref", required=True)
    parser.add_argument("--current-role", default=None, choices=list(models.ROLE_IDS))
    parser.add_argument("--current-repo", default=None)
    parser.add_argument("--component", default=".")
    args = parser.parse_args(list(arguments))
    schemas = load_schemas(repo_root)
    contract, contract_raw = load_contract(repo_root)
    receipt_path = Path(args.receipt)
    receipt_data = receipt_path.read_bytes()
    receipt = json.loads(receipt_data.decode("utf-8"))
    if not isinstance(receipt, dict):
        raise GovernanceError("invalid_receipt", "the receipt is not a JSON object", args.receipt)
    outcome = admit(
        contract,
        contract_raw,
        typing.cast(typing.Dict[str, object], receipt),
        schemas,
        repo_root=repo_root,
        operation_class=args.operation_class,
        decision_id=args.decision_id,
        requested_at_utc=args.requested_at,
        operation_ref={"kind": "commit", "ref": args.component},
        authority_ref=args.authority_ref,
        current_role=args.current_role,
        current_repo=args.current_repo,
    )
    _print_json({"schema": OUTPUT_SCHEMA_ID, "outcome": outcome.as_dict()})
    return EXIT_PASS if outcome.decision == "ALLOW" else EXIT_FINDINGS


def _cli_render(repo_root: Path, arguments: typing.Sequence[str]) -> int:
    parser = _sub_parser("render")
    parser.add_argument("--artifact", required=True, choices=["contract", "projection", "governance-dependencies"])
    args = parser.parse_args(list(arguments))
    if args.artifact == "contract":
        data = render_contract_bytes(repo_root)
    elif args.artifact == "projection":
        data = render_projection_bytes(repo_root)
    else:
        data = render_governance_dependencies_bytes(repo_root)
    sys.stdout.buffer.write(data)
    sys.stdout.buffer.flush()
    return EXIT_PASS


def main(argv: typing.Optional[typing.Sequence[str]] = None) -> int:
    """CLI entry point for the governance verb family (read-only except stdout)."""
    arguments = list(argv if argv is not None else sys.argv[1:])
    if not arguments or arguments[0] in ("-h", "--help"):
        sys.stdout.write(
            "usage: python -m tools.aegis_preflight governance <validate|resolve|receipt|admit|render> ...\n"
        )
        return EXIT_PASS if arguments else EXIT_USAGE
    verb = arguments[0]
    rest = arguments[1:]
    repo_root = Path(".")
    cleaned: typing.List[str] = []
    index = 0
    while index < len(rest):
        if rest[index] == "--repo-root" and index + 1 < len(rest):
            repo_root = Path(rest[index + 1])
            index += 2
            continue
        cleaned.append(rest[index])
        index += 1
    try:
        if verb == "validate":
            return _cli_validate(repo_root, cleaned)
        if verb == "resolve":
            return _cli_resolve(repo_root, cleaned)
        if verb == "receipt":
            return _cli_receipt(repo_root, cleaned)
        if verb == "admit":
            return _cli_admit(repo_root, cleaned)
        if verb == "render":
            return _cli_render(repo_root, cleaned)
        sys.stderr.write("unknown governance verb %r\n" % verb)
        return EXIT_USAGE
    except GovernanceError as error:
        sys.stderr.write("ERROR: %s\n" % error)
        return EXIT_USAGE
    except OSError as error:
        sys.stderr.write("ERROR: %s: %s\n" % (type(error).__name__, error))
        return EXIT_USAGE
    except Exception as error:  # internal errors are never reported as pass
        sys.stderr.write("INTERNAL ERROR: %s: %s\n" % (type(error).__name__, error))
        return EXIT_INTERNAL


def derive_receipt(
    contract: typing.Dict[str, object],
    contract_raw: bytes,
    resolution: models.ResolutionResult,
    *,
    repo_root: Path,
    schemas: typing.Dict[str, typing.Dict[str, object]],
    receipt_id: str,
    observation_type: str,
    observed_at_utc: str,
    task: typing.Dict[str, object],
    target: typing.Dict[str, object],
    host_session: typing.Dict[str, object],
    instructions: typing.Dict[str, object],
    packaging_binding: typing.Dict[str, object],
    adoption: typing.Optional[typing.Dict[str, object]] = None,
    adoption_ref: typing.Optional[str] = None,
    adoption_sha256: typing.Optional[str] = None,
    prior_receipt: typing.Optional[typing.Dict[str, object]] = None,
) -> typing.Dict[str, object]:
    """Derive a schema-valid context receipt from one resolution.

    The receipt keeps the observation type it was derived with: an old receipt is
    never edited to refresh, and admission never upgrades its type.
    """
    if observation_type not in OBSERVATION_TYPE_SET:
        raise GovernanceError("invalid_observation_type", "observation_type is not closed", observation_type)
    if resolution.route_id in models.BOUNDARY_OBSERVATION_OF:
        if observation_type != models.BOUNDARY_OBSERVATION_OF[resolution.route_id]:
            raise GovernanceError(
                "observation_type_mismatch",
                "a session-boundary route requires its matching observation type",
                "%s/%s" % (resolution.route_id, observation_type),
            )
    elif observation_type not in ("fresh-start", "protected-operation"):
        raise GovernanceError(
            "observation_type_mismatch",
            "a non-boundary route requires fresh-start or protected-operation",
            observation_type,
        )
    inputs = _resolution_invalidation_inputs(
        contract_raw,
        resolution,
        adoption=adoption,
        adoption_ref=adoption_ref,
        adoption_sha256=adoption_sha256,
        target=target,
        host_session=host_session,
        task_authority_ref=str(task.get("task_authority_ref") or ""),
    )
    digest = invalidation_digest(inputs)
    current_pin = getattr(resolution, "installation_pin", None)
    if current_pin is None:
        contract_source = contract.get("source") if isinstance(contract.get("source"), dict) else {}
        current_pin = {
            "commit": contract_source.get("commit"),
            "tree": contract_source.get("tree"),
            "package_manifest_sha256": None,
        }
    limitations = list(getattr(resolution, "limitations", []) or [])
    for finding in resolution.findings:
        if finding.status == "UNRUN":
            limitations.append("%s: %s" % (finding.code, finding.message))
    if prior_receipt is not None:
        prior_pin = typing.cast(typing.Dict[str, object], prior_receipt.get("contract", {})).get("approved_upstream_pin")
        if isinstance(prior_pin, dict) and prior_pin.get("commit") != current_pin.get("commit"):
            limitations.append(
                "PIN_CHANGED from %s to %s; the prior receipt is retained as evidence of the old observation"
                % (prior_pin.get("commit"), current_pin.get("commit"))
            )
    adoption_state = getattr(resolution, "adoption_state", "unknown")
    authority_ref = getattr(resolution, "adoption_authority_ref", None) or str(task.get("task_authority_ref"))
    required_documents = [
        document.as_dict()
        for document in resolution.resolved_documents
        if document.read_status == "read-verified"
    ]
    for document in required_documents:
        document["adoption_provenance"] = (
            "adoption-record:%s" % adoption_sha256 if (adoption is not None and adoption_sha256) else None
        )
    receipt = {
        "schema": RECEIPT_SCHEMA_ID,
        "receipt_id": receipt_id,
        "observation_type": observation_type,
        "route_id": resolution.route_id,
        "route_family": resolution.route_family,
        "observed_at_utc": observed_at_utc,
        "task": {
            "task_id": str(task.get("task_id")),
            "task_ref": str(task.get("task_ref")),
            "scope_summary": str(task.get("scope_summary")),
            "task_authority_ref": str(task.get("task_authority_ref")),
        },
        "target": {
            "target_repo": str(target.get("target_repo")),
            "target_kind": str(target.get("target_kind")),
            "workspace_role": str(target.get("workspace_role")),
            "role_evidence": [str(item) for item in typing.cast(typing.List[object], target.get("role_evidence") or [])],
        },
        "host_session": host_session,
        "instructions": instructions,
        "contract": {
            "contract_id": CONTRACT_ID,
            "contract_version": str(contract.get("contract_version")),
            "contract_sha256": sha256_upper(contract_raw),
            "contract_source_commit": str(typing.cast(typing.Dict[str, object], contract.get("source")).get("commit")),
            "approved_upstream_pin": current_pin,
            "dependency_closure_verified": bool(packaging_binding.get("dependency_closure_verified")),
            "verifier_identity": "tools.aegis_preflight.governance/%s" % TOOL_VERSION,
            "lifecycle_state": str(typing.cast(typing.Dict[str, object], contract.get("lifecycle")).get("status")),
        },
        "packaging_manifest_binding": {
            key: packaging_binding[key]
            for key in (
                "manifest_bytes",
                "manifest_lf",
                "manifest_sha256",
                "manifest_path",
                "detached_binding_evidence_ref",
                "detached_binding_sha256",
                "commands",
                "stage_a_feasibility_ref",
                "c1_dependency_consumption_used",
            )
        },
        "required_documents": required_documents,
        "local_adoption": {
            "state": adoption_state,
            "adoption_record_ref": adoption_ref,
            "adoption_record_sha256": adoption_sha256,
            "adopted_rules_digest": canonical_digest(
                sorted(
                    set(
                        str(rule_id)
                        for rule_id in typing.cast(typing.Dict[str, object], adoption.get("adoption") or {}).get(
                            "adopted_rule_ids", []
                        )
                    )
                )
            )
            if adoption is not None
            else None,
            "overrides": list(typing.cast(typing.List[object], (adoption or {}).get("manual_only_overrides") or [])),
            "authority_ref": authority_ref,
        },
        "nested_local_policy": list(getattr(resolution, "nested_local_policy", []) or []),
        "resolved_rules": resolution.resolved_rules,
        "exclusions": resolution.exclusions,
        "invalidation_inputs_digest": {
            "algorithm": "sha256",
            "inputs": _normalize_inputs(inputs),
            "digest": digest,
        },
        "integrity": {
            "self_asserted": True,
            "verification_status": "RECONCILED-AGAINST-AUTHORITATIVE-INPUTS"
            if resolution.status == "RESOLVED"
            else "UNVERIFIED",
            "evidence_refs": [],
        },
        "limitations": limitations,
        "non_claims": list(_RECEIPT_NON_CLAIMS),
    }
    schema_findings = validate_json_schema(receipt, schemas["receipt"], root_schema=schemas["receipt"])
    if schema_findings:
        raise GovernanceError("receipt_schema_invalid", "; ".join(schema_findings[:10]))
    return receipt


if __name__ == "__main__":
    sys.exit(main())
