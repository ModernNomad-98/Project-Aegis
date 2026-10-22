---
name: branching-strategy-designer
description: 'Use when a repo''s branching, protection, review and release flow is undefined or inconsistent: choose trunk-based or branch/release branching and record naming, protection, review, merge strategy, hotfix and release flow with migration risks. Do NOT use to edit repository settings or pipeline YAML (ci-pipeline-architect) or to review an actual diff (reviewable-diff-discipline); this skill records a branching decision only.'
---

# Branching Strategy Designer

Terms: **family 7** - Cloud, DevOps, reliability & release (README roster family 7; docs/skills-catalog.md Phase 6 cloud, DevOps, reliability and release pack); **advisory/design-only** means this skill produces guidance and records and never edits code, runs commands or grants production authority.

## Purpose

Design and record a repository branching and release flow: choose trunk-based or branch/release branching with alternatives and rejected options, define branch naming/protection/review rules, merge method and queue, release and hotfix flow, migrate from the current model with safe defaults and risks; refuses to change repository settings or invent team constraints.

The skill is **auto-invocable and advisory/design-only**. It produces the named artifact below with evidence and open questions; it does not edit code, run commands, use the network or grant production authority. Implementation and approval are delegated host/user actions. It composes the named neighbouring owners instead of duplicating them.

## Use When

- A concrete request like: Our branching and release flow is undefined - choose and record a strategy.
- The named artifact is missing, disputed or about to be built against a wrong assumption.
- A review/spec must record the artifact, its edge cases and the boundary owners explicitly.
- An implementation is about to start and the ask is for the artifact it must build against.

**Do not use when:** the request belongs to a named neighbouring owner (the complete routing list is in Stop Conditions) or when no evidence exists and the answer would be invention.

## Inputs to Inspect

- Current branch inventory, protection rules and merge queue configuration (as supplied; do not change settings).
- Team size, review capacity, release cadence, hotfix expectations and environment/CI gate facts.
- Existing contribution guide, merge policy and rollback/release procedures.
- Migration constraints (open branches, release trains, compliance freezes) and known pain points.

## Workflow

1. Record the decision context: team size, cadence, release model and current pain points with evidence.
2. Choose trunk-based vs branch/release (or a hybrid) with alternatives and rejected options.
3. Define branch naming/protection/review/merge rules and the merge queue/hotfix path.
4. Design migration from the current model in safe steps, including open-branch handling and rollback of the process change.
5. Record risks, unresolved team constraints and the decision record; edit no repository settings.

## Output Format

Return, in this order:

1. Branching decision record with context, alternatives and rejected options.
2. Branch/protection/review/merge rule table.
3. Release/hotfix flow and migration/rollout plan.
4. Risks and open team constraints.

## Validation Checklist

- [ ] Decision context and constraints are recorded with evidence.
- [ ] Alternatives and rejected options are stated, not just the chosen model.
- [ ] Rules cover naming, protection, review, merge method and hotfix/release path.
- [ ] Migration keeps existing open work safe and has a rollback.
- [ ] No repository settings were changed by this skill.

## Gotchas

- Choosing a model without the team/release constraints and then declaring it "best practice".
- Ignoring open long-lived branches during migration.
- Assuming the merge queue is safe without review/protection rules.
- Editing protection settings instead of recording the decision.

## Stop Conditions

Route a request to its real owner when it is that owner's deliverable (the complete expected-owner routing list exercised by trigger-evals):

- ci-pipeline-architect work -> `ci-pipeline-architect`.
- contribution-guide-author work -> `contribution-guide-author`.
- merge-is-deploy-governance work -> `merge-is-deploy-governance`.
- release-readiness-reviewer work -> `release-readiness-reviewer`.
- ai-sdlc-operating-model work -> `ai-sdlc-operating-model`.
- local-ci-mirror-preflight work -> `local-ci-mirror-preflight`.
- change-classification-gate work -> `change-classification-gate`.
- reviewable-diff-discipline work -> `reviewable-diff-discipline`.
- rollback-runbook-author work -> `rollback-runbook-author`.
- phased-work-handoff-designer work -> `phased-work-handoff-designer`.
- environment-parity-reviewer work -> `environment-parity-reviewer`.
- code-reviewer work -> `code-reviewer`.
- human-approval-boundary work -> `human-approval-boundary`.
- scoped-approval-register work -> `scoped-approval-register`.
- The caller wants this skill to implement, run or approve the change: refuse; return the artifact for the authorized owner.
- Required evidence is unavailable: state what is missing and mark the artifact UNVERIFIED instead of inventing facts.

## Supporting Files

- [branching-decision-model](references/branching-decision-model.md) - the named artifact, tables and completion checklist for this skill.
- [evals/evals.json](evals/evals.json) - the 6 behaviour cases for this skill.
- [evals/trigger-evals.json](evals/trigger-evals.json) - the 22 trigger-discrimination cases (8 positive / 14 negative) against real manifest owners.

**Source:** docs/skills-catalog.md - Phase 6 cloud, DevOps, reliability and release pack (Batch 5/D113); coverage: roadmap rows #236. The trigger description is the frontmatter description above; keep it under 1,024 parsed characters, concrete and trigger-oriented.
