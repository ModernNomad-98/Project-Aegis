---
name: architecture-spike-planner
description: 'Plan timeboxed architecture spikes: question, hypotheses, timebox, evidence, exit criteria and the resulting decision.'
---

# Architecture Spike Planner

Terms: **family 3** - core architecture & engineering (README roster family 3; docs/skills-catalog.md Phase 2 pack). **Advisory/design-only:** produces the named artifact and records; never edits code, runs commands, uses the network or grants production authority.

## Purpose

Charter time-boxed spikes: hypothesis, success criteria, artifacts, decision output, and what is thrown away.

**Output artifact:** spike charter with question, hypotheses, timebox, evidence and exit criteria. The skill is auto-invocable and advisory: it composes the named neighbouring owners instead of duplicating them, and it returns the artifact plus open questions for the authorized implementer.

## Use When

- The request needs spike charter with question, hypotheses, timebox, evidence and exit criteria for a real system.
- The design is implicit/disputed or about to harden an assumption.
- A spec or review must record the artifact fields and boundaries explicitly.
- Implementation is about to start and the record it builds against is missing.

**Do not use when** the request belongs to a named neighbouring owner in Stop Conditions, or when the evidence needed for the artifact is unavailable.

## Inputs to Inspect

- Question the spike must answer
- Hypotheses and disconfirming evidence
- Timebox and stop rule
- Evidence to collect and how
- Exit criteria and decision record
- Threats to validity

## Workflow

1. State the decision the spike informs.
2. List hypotheses and disconfirming evidence.
3. Set timebox and stop rule.
4. Define the evidence collection method.
5. Write exit criteria before starting.
6. Plan the decision record and owner.
7. Mark artifacts throwaway vs durable.

## Output Format

Return, in this order:

1. Scope, evidence inventory and what could not be inspected.
2. Spike charter with question, hypotheses, timebox, evidence and exit criteria, with the fields listed in Inputs to Inspect.
3. Edge/failure cases and the chosen handling.
4. Boundary/handoff note naming the neighbouring owners (including the eval-only list below).
5. Verified facts, assumptions, UNKNOWN/UNVERIFIED items and the validation/test plan.

## Validation Checklist

- Question is decision-relevant
- Hypotheses are falsifiable
- Timebox and stop rule are explicit
- Evidence method is credible
- Exit criteria exist before the spike
- Decision and owner are recorded

## Gotchas

- A spike without a question becomes a prototype
- No stop rule means scope creep
- A spike whose artifacts become production code was not a spike

## Stop Conditions

- roadmap under uncertainty planner requests route to `roadmap-under-uncertainty-planner`; this skill owns a different artifact.
- ai task decomposer requests route to `ai-task-decomposer`; this skill owns a different artifact.
- exploratory charter designer requests route to `exploratory-charter-designer`; this skill owns a different artifact.
- The caller wants implementation, execution or approval: refuse; return the artifact for the authorized owner.
- Required evidence is unavailable: mark the artifact UNVERIFIED and state what is missing instead of inventing facts.
- **Eval-only discrimination set** (from `evals/trigger-evals.json` overlaps_with; eval-only, not a routing contract): `adr-writer`, `ai-task-decomposer`, `architecture-designer`, `change-classification-gate`, `code-reviewer`, `design-review-facilitator`, `exploratory-charter-designer`, `human-approval-boundary`, `observability-by-design`, `release-readiness-reviewer`, `roadmap-under-uncertainty-planner`, `rollback-runbook-author`, `security-pr-reviewer`, `tech-spec-writer`.

## Supporting Files

- [spike-charter](references/spike-charter.md) - the concrete spike charter with question, hypotheses, timebox, evidence and exit criteria fields, construction method, checks and a worked table.
- [evals/evals.json](evals/evals.json) - six domain-specific behaviour cases.
- [evals/trigger-evals.json](evals/trigger-evals.json) - 22 trigger-discrimination cases (8 positive / 14 negative) against real manifest owners

**Source:** docs/skills-catalog.md Phase 2 core architecture & engineering pack (Batch 4/D112); coverage cat 01 rows #54. Description is trigger-first (capability front-loaded for truncated listings).
