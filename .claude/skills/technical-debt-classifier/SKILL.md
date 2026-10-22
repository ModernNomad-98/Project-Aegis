---
name: technical-debt-classifier
description: 'Classify technical debt with a ledger: type, evidence, interest, principal, owner, priority and reversal cost, ranked for decisions.'
---

# Technical Debt Classifier

Terms: **family 3** - core architecture & engineering (README roster family 3; docs/skills-catalog.md Phase 2 pack). **Advisory/design-only:** produces the named artifact and records; never edits code, runs commands, uses the network or grants production authority.

## Purpose

Classify debt by risk, owner, impact, payoff and whether it blocks future architecture; produce a ledger, not a wish list.

**Output artifact:** technical-debt ledger with interest, cost, owner and priority. The skill is auto-invocable and advisory: it composes the named neighbouring owners instead of duplicating them, and it returns the artifact plus open questions for the authorized implementer.

## Use When

- The request needs technical-debt ledger with interest, cost, owner and priority for a real system.
- The design is implicit/disputed or about to harden an assumption.
- A spec or review must record the artifact fields and boundaries explicitly.
- Implementation is about to start and the record it builds against is missing.

**Do not use when** the request belongs to a named neighbouring owner in Stop Conditions, or when the evidence needed for the artifact is unavailable.

## Inputs to Inspect

- Debt type taxonomy (code, design, test, doc, infra, data)
- Evidence per item with file/link
- Interest: what worsens if deferred
- Principal/reversal cost estimate
- Owner and decision route
- Priority ranking and rationale

## Workflow

1. Collect candidate debt items from evidence, not opinion.
2. Classify each item with the taxonomy.
3. Attach evidence and affected components.
4. Estimate interest and reversal cost.
5. Assign owner and decision route.
6. Rank with an explicit frame.
7. Define ledger cadence and retirement rule.

## Output Format

Return, in this order:

1. Scope, evidence inventory and what could not be inspected.
2. Technical-debt ledger with interest, cost, owner and priority, with the fields listed in Inputs to Inspect.
3. Edge/failure cases and the chosen handling.
4. Boundary/handoff note naming the neighbouring owners (including the eval-only list below).
5. Verified facts, assumptions, UNKNOWN/UNVERIFIED items and the validation/test plan.

## Validation Checklist

- Every item has evidence and a type
- Interest and cost estimates are separate
- Owner and decision route are named
- Ranking is explained not asserted
- Retired items are removed or marked

## Gotchas

- Debt without evidence is a wish list
- Interest and principal conflated produce wrong priorities
- A ledger nobody reviews becomes stale in one quarter

## Stop Conditions

- principal code analyst requests route to `principal-code-analyst`; this skill owns a different artifact.
- full codebase auditor requests route to `full-codebase-auditor`; this skill owns a different artifact.
- staff scope selector requests route to `staff-scope-selector`; this skill owns a different artifact.
- The caller wants implementation, execution or approval: refuse; return the artifact for the authorized owner.
- Required evidence is unavailable: mark the artifact UNVERIFIED and state what is missing instead of inventing facts.
- **Eval-only discrimination set** (from `evals/trigger-evals.json` overlaps_with; eval-only, not a routing contract): `adr-writer`, `architecture-designer`, `change-classification-gate`, `code-reviewer`, `design-review-facilitator`, `full-codebase-auditor`, `human-approval-boundary`, `principal-code-analyst`, `prioritization-frame-picker`, `release-readiness-reviewer`, `roadmap-under-uncertainty-planner`, `rollback-runbook-author`, `staff-scope-selector`, `tech-spec-writer`.

## Supporting Files

- [debt-ledger-template](references/debt-ledger-template.md) - the concrete technical-debt ledger with interest, cost, owner and priority fields, construction method, checks and a worked table.
- [evals/evals.json](evals/evals.json) - six domain-specific behaviour cases.
- [evals/trigger-evals.json](evals/trigger-evals.json) - 22 trigger-discrimination cases (8 positive / 14 negative) against real manifest owners

**Source:** docs/skills-catalog.md Phase 2 core architecture & engineering pack (Batch 4/D112); coverage cat 01 rows #43. Description is trigger-first (capability front-loaded for truncated listings).
