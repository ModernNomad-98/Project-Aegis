---
name: defect-triage-facilitator
description: 'Use when defects need a consistent report or a prioritization decision: author the bug report (repro, expected vs actual, environment, logs, suspected area) and run triage by severity, frequency, customer impact, security and release risk with one owner and next action per defect. Do NOT use for CI log failure classification (ci-failure-classifier) or root-cause debugging (systematic-debugger); this skill authors reports and triage decisions and fixes nothing.'
---

# Defect Triage Facilitator

Terms: **family 6** - QA, E2E & evidence (README roster family 6; docs/skills-catalog.md Phase 5 QA, E2E and evidence pack); **advisory/design-only** means this skill produces guidance and records and never edits code, runs commands or grants production authority.

## Purpose

Facilitate consistent defect reporting and triage: complete the bug report (repro steps, expected vs actual, environment, evidence, suspected area), rank defects by severity, frequency, customer impact, security and release risk with explicit rationale, assign one owner and next action per decision, and route security/release-risk findings; refuses invented facts and fixes.

The skill is **auto-invocable and advisory/design-only**. It produces the named artifact below with evidence and open questions; it does not edit code, run commands, use the network or grant production authority. Implementation and approval are delegated host/user actions. It composes the named neighbouring owners instead of duplicating them.

## Use When

- The request is to facilitate consistent defect reporting and triage: complete the bug report (repro steps, expected vs actual, environment, evidence, suspected area), rank defects by severity, frequency, customer impact, security and release risk with explicit rationale, assign one owner and next action per decision, and route security/release-risk findings; refuses invented facts and fixes..
- The named artifact is missing, disputed or about to be built against a wrong assumption.
- A review/spec must record the artifact, its edge cases and the boundary owners explicitly.
- An implementation is about to start and the ask is for the artifact it must build against.

**Do not use when:** the request belongs to a named neighbouring owner (the complete routing list is in Stop Conditions) or when no evidence exists and the answer would be invention.

## Inputs to Inspect

- Defect or bug report text, reproduction steps, logs, screenshots and affected environment/build info.
- Impact data: frequency, affected tenants/users, customer reports and revenue/support signal.
- Release plan and current release risk context; quality bar and known issues.
- Component ownership map and security/release escalation contacts.

## Workflow

1. Complete the bug report: repro steps, expected vs actual, environment, evidence, suspected area; mark missing fields as UNKNOWN.
2. Classify the defect (functional/security/data/release-blocking/regression) and check duplicates.
3. Triage on the axes: severity, frequency, customer impact, security and release risk with rationale.
4. Assign one owner and one next action per decision; record assumptions and unknowns explicitly.
5. Route security-flagged or release-risk findings to their owners and produce the triage agenda/decision list.

## Output Format

Return, in this order:

1. Completed bug report with missing fields marked.
2. Triage table: defect, axes, rationale, owner, next action, assumptions.
3. Duplicate/security/release-risk flags and routing.
4. Triage agenda and ranked decision list.

## Validation Checklist

- [ ] Report has repro, expected/actual, environment and evidence, or explicit UNKNOWN fields.
- [ ] Each triage decision cites its axes and rationale.
- [ ] One owner and one next action per defect; no invented fixes or release dates.
- [ ] Security and release risk are routed, not buried in severity.
- [ ] Assumptions and unknowns are recorded.

## Gotchas

- Promising a fix or release date the triage cannot authorize.
- Ranking only by severity while ignoring frequency or customer impact.
- Inventing reproduction steps when the report is incomplete.
- Treating a duplicate as a new defect and inflating the queue.

## Stop Conditions

Route a request to its real owner when it is that owner's deliverable (the complete expected-owner routing list exercised by trigger-evals):

- ci-failure-classifier work -> `ci-failure-classifier`.
- systematic-debugger work -> `systematic-debugger`.
- regression-suite-curator work -> `regression-suite-curator`.
- release-readiness-reviewer work -> `release-readiness-reviewer`.
- clickthrough-test-engineer work -> `clickthrough-test-engineer`.
- manual-test-case-creator work -> `manual-test-case-creator`.
- acceptance-criteria-reviewer work -> `acceptance-criteria-reviewer`.
- exploratory-charter-designer work -> `exploratory-charter-designer`.
- test-plan-designer work -> `test-plan-designer`.
- screenshot-evidence-planner work -> `screenshot-evidence-planner`.
- flaky-test-detective work -> `flaky-test-detective`.
- qa-strategy-architect work -> `qa-strategy-architect`.
- test-coverage-mapper work -> `test-coverage-mapper`.
- ai-closeout-reporter work -> `ai-closeout-reporter`.
- The caller wants this skill to implement, run or approve the change: refuse; return the artifact for the authorized owner.
- Required evidence is unavailable: state what is missing and mark the artifact UNVERIFIED instead of inventing facts.

## Supporting Files

- [bug-report-and-triage-template](references/bug-report-and-triage-template.md) - the named artifact, tables and completion checklist for this skill.
- [evals/evals.json](evals/evals.json) - the 6 behaviour cases for this skill.
- [evals/trigger-evals.json](evals/trigger-evals.json) - the 22 trigger-discrimination cases (8 positive / 14 negative) against real manifest owners.

**Source:** docs/skills-catalog.md - Phase 5 QA, E2E and evidence pack (Batch 5/D113); coverage: roadmap rows #224, #225. The trigger description is the frontmatter description above; keep it under 1,024 parsed characters, concrete and trigger-oriented.
