---
name: security-drift-detector
description: 'Use when security posture may have silently drifted from a recorded baseline: compare code, policy, tests and docs against the baseline and report weakened, undocumented or expired controls with evidence and an owner/action.'
---

# Security Drift Detector

Terms: **family 5** - Security, RLS & supply chain (README roster family 5; docs/skills-catalog.md Phase 4 security, RLS & supply-chain pack); **advisory/design-only** means this skill produces guidance and records and never edits code, runs commands or grants production authority.

## Purpose

Detect security drift against a recorded baseline: select and record the baseline, compare control by control, classify weakening (removed, narrowed, default-changed, unowned), detect undocumented changes and expiry/staleness, attach evidence and an owner/action per finding, and recommend re-baselining; read-only, no live probing.

The skill is **auto-invocable and advisory/design-only**. It produces a design/decision record with evidence and open questions; it does not edit code, run commands, use the network or grant production authority. Implementation and approval are delegated host/user actions. It composes the named neighbouring owners instead of duplicating them.

## Use When

- The request is to detect security drift against a recorded baseline.
- The current design or evidence is implicit, disputed or about to harden a wrong assumption.
- A spec/review must record the decision, the edge/failure cases and the boundary owners explicitly.
- An implementation is about to start and the ask is for the record it must build against.

**Do not use when:** the request belongs to a named neighbouring owner (see Stop Conditions) or when no evidence exists and the answer would be invention.

## Inputs to Inspect

- The design/spec/configuration under discussion and the decision it must support.
- Existing code/config/tests/diagrams and the observed behaviour they encode.
- Related standards, runbooks, baselines and recorded decisions (D-records, ADRs) that constrain the answer.
- Known incidents, review findings and open questions attached to this area.

## Workflow

1. State the question, scope and what will not be inspected; list evidence actually available.
2. Build the primary artifact for security drift detector from inspected evidence (not from assumptions).
3. Enumerate the edge, failure and refusal cases the artifact must survive.
4. Name the boundary owners from Stop Conditions and what each one owns.
5. Separate verified facts, assumptions and open questions; mark unverified items explicitly.
6. Define the validation/test plan that would prove the artifact correct.
7. Return the artifact and records; do not edit code or claim an execution you did not perform.

## Output Format

Return, in this order:

1. Scope/question and evidence inventory.
2. Primary design/decision record for this skill.
3. Edge/failure table and the chosen handling.
4. Boundary/handoff note naming the neighbouring owners.
5. Open questions, assumptions and unverified items, with the verification plan.

## Validation Checklist

- Scope and inputs are stated; no claim of inspection or execution that did not happen.
- The primary artifact is complete enough for another engineer to implement against.
- Edge/failure cases are enumerated with a chosen handling, not hand-waved.
- Boundary owners are named and this skill does not take over their work.
- Facts, assumptions and open questions are separated; UNKNOWN is not presented as a decision.
- A concrete validation/test plan is included.

## Gotchas

- A design record built on assumed evidence becomes a false contract.
- Skipping the edge/failure table moves the surprise into implementation.
- Taking over a neighbouring owner deliverable duplicates authority and hides the boundary.
- An artifact with no open questions usually means the inspection was shallow.

## Stop Conditions

- The request is security pr reviewer work: route to `security-pr-reviewer`; this skill owns a different deliverable.
- The request is rls policy auditor work: route to `rls-policy-auditor`; this skill owns a different deliverable.
- The request is agent governance audit work: route to `agent-governance-audit`; this skill owns a different deliverable.
- The caller wants this skill to implement, run or approve the change: refuse; return the design/record for the authorized owner.
- Required evidence is unavailable: state what is missing and mark the artifact UNVERIFIED instead of inventing facts.

## Supporting Files

- [security-baseline-checklist](references/security-baseline-checklist.md) - method and record guidance for this skill.
- [evals/evals.json](evals/evals.json) - the 6 behaviour cases for this skill.
- [evals/trigger-evals.json](evals/trigger-evals.json) - the 22 trigger-discrimination cases (8 positive / 14 negative) against real manifest owners.

**Source:** docs/skills-catalog.md - Phase 4 security, RLS & supply-chain pack (Batch 5/D113); coverage roadmap rows #130. The trigger description is the frontmatter description above; keep it under 1,024 parsed characters, concrete and trigger-oriented.
