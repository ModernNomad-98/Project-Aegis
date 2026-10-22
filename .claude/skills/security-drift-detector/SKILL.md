---
name: security-drift-detector
description: 'Use when security posture may have silently drifted from a recorded baseline: compare code, policy, tests and docs against the baseline and report weakened, undocumented or expired controls with evidence and an owner/action. Do NOT use for a live cloud-account baseline check (cloud-security-baseline-reviewer) or a remediation implementation; this skill compares supplied evidence to a recorded baseline and changes nothing.'
---

# Security Drift Detector

Terms: **family 5** - Security, RLS & supply chain (README roster family 5; docs/skills-catalog.md Phase 4 security, RLS and supply-chain pack); **advisory/design-only** means this skill produces guidance and records and never edits code, runs commands or grants production authority.

## Purpose

Detect security drift against a recorded baseline: select and record the baseline, compare control by control, classify weakening (removed, narrowed, default-changed, unowned), detect undocumented changes and expiry/staleness, attach evidence and an owner/action per finding, and recommend re-baselining; read-only, no live probing.

The skill is **auto-invocable and advisory/design-only**. It produces the named artifact below with evidence and open questions; it does not edit code, run commands, use the network or grant production authority. Implementation and approval are delegated host/user actions. It composes the named neighbouring owners instead of duplicating them.

## Use When

- The request is to detect security drift against a recorded baseline: select and record the baseline, compare control by control, classify weakening (removed, narrowed, default-changed, unowned), detect undocumented changes and expiry/staleness, attach evidence and an owner/action per finding, and recommend re-baselining; read-only, no live probing..
- The named artifact is missing, disputed or about to be built against a wrong assumption.
- A review/spec must record the artifact, its edge cases and the boundary owners explicitly.
- An implementation is about to start and the ask is for the artifact it must build against.

**Do not use when:** the request belongs to a named neighbouring owner (the complete routing list is in Stop Conditions) or when no evidence exists and the answer would be invention.

## Inputs to Inspect

- Recorded baseline: audit report, prior security review, control set, configuration snapshot or policy version with its date and scope.
- Current evidence: config/code excerpts, tests, docs, policies, schema/RLS definitions, CI security jobs - whatever the caller supplies (read-only).
- Change history since the baseline where available (commits, change records, tickets) and known exceptions.
- Owner map for the affected controls and the re-baseline authority.

## Workflow

1. Select and record the baseline: source, date, scope and what it covers; state what it does not cover.
2. Compare control by control: expected state vs current state, with evidence for each side.
3. Classify each difference: removed, narrowed, default-changed, undocumented, expired/stale.
4. Separate drift from planned changes (cite the change record); flag unowned controls and stale evidence.
5. Rank findings by control criticality and assign an owner/action and re-baseline recommendation.

## Output Format

Return, in this order:

1. Baseline record: source, date, scope, evidence pointers.
2. Control comparison table: control, expected, current, classification, evidence, owner/action.
3. Weakening list (removed/narrowed/default-changed) and undocumented-change list.
4. Staleness/expiry list and re-baseline recommendation.

## Validation Checklist

- [ ] Baseline is recorded with source/date/scope; unsupplied areas are UNVERIFIED.
- [ ] Each difference has evidence for both expected and current state.
- [ ] Weakening classes are applied consistently (removed/narrowed/default-changed).
- [ ] Planned changes are distinguished from drift by citing the change record.
- [ ] Unowned and expired controls are surfaced, not silently accepted.

## Gotchas

- Treating a newer config as drift when a valid change record explains it.
- Comparing against a baseline that is itself unverified or stale.
- Reporting only removals while missing narrowed defaults and unowned controls.
- Running live scans or probing instead of reading supplied evidence.

## Stop Conditions

Route a request to its real owner when it is that owner's deliverable (the complete expected-owner routing list exercised by trigger-evals):

- security-pr-reviewer work -> `security-pr-reviewer`.
- rls-policy-auditor work -> `rls-policy-auditor`.
- agent-governance-audit work -> `agent-governance-audit`.
- compliance-evidence-collector work -> `compliance-evidence-collector`.
- iac-reviewer work -> `iac-reviewer`.
- cloud-security-baseline-reviewer work -> `cloud-security-baseline-reviewer`.
- code-reviewer work -> `code-reviewer`.
- change-classification-gate work -> `change-classification-gate`.
- source-of-truth-reconciler work -> `source-of-truth-reconciler`.
- audit-log-architect work -> `audit-log-architect`.
- agent-memory-governance work -> `agent-memory-governance`.
- local-ci-mirror-preflight work -> `local-ci-mirror-preflight`.
- secure-migration-reviewer work -> `secure-migration-reviewer`.
- threat-modeler work -> `threat-modeler`.
- The caller wants this skill to implement, run or approve the change: refuse; return the artifact for the authorized owner.
- Required evidence is unavailable: state what is missing and mark the artifact UNVERIFIED instead of inventing facts.

## Supporting Files

- [security-baseline-checklist](references/security-baseline-checklist.md) - the named artifact, tables and completion checklist for this skill.
- [evals/evals.json](evals/evals.json) - the 6 behaviour cases for this skill.
- [evals/trigger-evals.json](evals/trigger-evals.json) - the 22 trigger-discrimination cases (8 positive / 14 negative) against real manifest owners.

**Source:** docs/skills-catalog.md - Phase 4 security, RLS and supply-chain pack (Batch 5/D113); coverage: roadmap rows #130. The trigger description is the frontmatter description above; keep it under 1,024 parsed characters, concrete and trigger-oriented.
