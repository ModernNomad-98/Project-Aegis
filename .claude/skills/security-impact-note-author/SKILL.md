---
name: security-impact-note-author
description: 'Use when a security-sensitive change needs a reviewable impact note: document affected assets, risks, mitigations, tests, rollback and approval needs, separating verified facts from assumptions. Authoring-only; it does not review diffs, approve changes, or replace threat modeling.'
---

# Security Impact Note Author

Terms: **family 5** - the discipline family in README.md and docs/skills-catalog.md; **read-only** means this skill inspects and returns guidance/records and never edits code or runs production actions.

## Purpose

Author a reviewable security impact note for a sensitive change: establish scope and assets, classify impact, record mitigations, tests and rollback, separate verified from assumed, and require approval sign-off.

The skill is **advisory and auto-invocable**. It produces guidance, records and review structure only; it does not edit code, run commands, use the network or grant production authority. Any implementation, execution or approval is a delegated host/user action under existing authority. It composes the nearest owners rather than duplicating them.

## Use When

- A change touches authentication, authorization, secrets, tenancy, payments, production data or trust boundaries.
- A reviewer or governance path needs a written impact note before approval.
- Mitigations exist but are scattered across the diff, tests and design docs.
- Rollback and approval needs must be explicit before deployment.

**Do not use when:** the request belongs to a named neighbouring owner (see Stop Conditions), or when inspection evidence is unavailable and the question would have to be answered by guessing.

## Inputs to Inspect

- The change, its diff and design context, plus the classification/approval record.
- Threat model or security review findings for the affected surface.
- Tests, evidence and rollback plan that actually exist.
- Asset/data inventory and classification.
- The applicable approval register and sign-off owner.

## Workflow

1. State scope, change class and the assets/data affected.
2. Classify impact and threat scenarios; separate verified facts from assumptions.
3. Map each risk to mitigation, evidence/test, residual risk and owner.
4. Record rollback/recovery and what cannot be rolled back.
5. List required approvals and the sign-off owner; state what approval is not granted.
6. Flag any mitigation or test that is UNRUN/missing; never inflate coverage.
7. Return the impact note; do not approve the change yourself.

## Output Format

Return, in this order:

1. Scope/asset/impact classification.
2. Risk-mitigation-evidence table with residual risk and owners.
3. Verified vs assumed separation and known gaps.
4. Tests, rollback and monitoring evidence.
5. Approval requirements, sign-off owner and required decisions.

## Validation Checklist

- Scope, change class and assets explicit.
- Risks mapped to mitigations, tests and residual risk.
- Verified facts separated from assumptions; UNRUN items named.
- Rollback and monitoring evidence recorded.
- Approval requirements and owner stated; no self-approval claimed.
- Residual risk visible for the sign-off decision.

## Gotchas

- An impact note that lists mitigations without evidence is a wish list.
- Self-approval by the author converts a review artifact into theatre.
- Rollback that cannot restore data must be stated, not implied.
- Assumed threat coverage presented as verified corrupts the approval decision.
- Silent residual risk is the most dangerous omission.

## Stop Conditions

- The request is reviewing a security diff: route to security-pr-reviewer.
- The request is threat modeling: route to threat-modeler.
- The request is governance/process audit: route to agent-governance-audit.
- The request is human approval/sign-off authority: route to human-approval-boundary.
- The request is change classification: route to change-classification-gate.
- Never reproduce secrets, tokens or PII in the note; use classification labels and compose with sensitive-disclosure-guard.
- The caller asks this skill to approve the change: refuse and record that approval needs the recorded sign-off.
- Impact cannot be classified from available evidence: state assumptions and required facts or UNRUN.

## Supporting Files

- [security-impact-note-template](references/security-impact-note-template.md) - Security impact note template and approval evidence.
- [evals/evals.json](evals/evals.json) - the 4 behaviour cases for this skill.
- [evals/trigger-evals.json](evals/trigger-evals.json) - 8 positive and 14 negative trigger-discrimination cases against the nearest owners.

**Source:** docs/skills-catalog.md - cat 03 #127 (Security Impact Note Authoring); coverage roadmap #127. The trigger description is the frontmatter description above; keep it under 1,024 parsed characters, concrete and trigger-oriented.
