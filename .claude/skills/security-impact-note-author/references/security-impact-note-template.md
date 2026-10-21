# Security impact note template and approval evidence

Reference for the security-impact-note-author skill. It is method and record guidance only: it never directs the skill to edit code, run commands, use the network or claim production authority.

## 1. Core model

- Sections: scope, change class, assets/data, impact classification, threats, mitigations, tests/evidence, rollback, monitoring, approvals, residual risk.
- Evidence rule: every mitigation maps to a test/observation or is labeled UNRUN.
- Verified vs assumed: separate columns/lists; assumptions need owners.
- Rollback: data can/cannot be restored; blast radius; monitoring window.
- Approval: required register entry, sign-off owner, what is not granted.
- Residual risk and smallest decision for the approver.

## 2. When this applies

- A change touches authentication, authorization, secrets, tenancy, payments, production data or trust boundaries.
- A reviewer or governance path needs a written impact note before approval.
- Mitigations exist but are scattered across the diff, tests and design docs.
- Rollback and approval needs must be explicit before deployment.

## 3. Output and evidence rules

1. Scope/asset/impact classification.
2. Risk-mitigation-evidence table with residual risk and owners.
3. Verified vs assumed separation and known gaps.
4. Tests, rollback and monitoring evidence.
5. Approval requirements, sign-off owner and required decisions.

Every claim in the returned record is backed by inspected evidence or explicitly labeled **assumption**, **UNKNOWN** or **UNRUN**. An empty or unrun check is never a PASS. The skill does not edit files or execute commands; delegated actions go to the host/user or the existing implementation owner under existing authority.

## 4. Boundaries

- Inputs inspected: see the SKILL.md Inputs to Inspect section.
- Stop and route out when the request matches another owner; see Stop Conditions.
- No production, deployment, spending or approval authority is granted by this reference.

## 5. Validation before returning

- Scope, change class and assets explicit.
- Risks mapped to mitigations, tests and residual risk.
- Verified facts separated from assumptions; UNRUN items named.
- Rollback and monitoring evidence recorded.
- Approval requirements and owner stated; no self-approval claimed.
- Residual risk visible for the sign-off decision.
