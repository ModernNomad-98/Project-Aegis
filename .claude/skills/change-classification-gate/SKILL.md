---
name: change-classification-gate
description: Classify a requested change before starting work — docs-only, UI/style, frontend logic, backend/API, schema/migration, RLS/security, cloud/IaC, AI/agentic behavior, QA/test-only, refactor, bug fix, or release — and map the class to its required validation level and approval path. Locks scope to the approved class and file set; mid-task scope growth forces reclassification. Use when starting any non-trivial change, when a task mixes change types, or when work is drifting beyond what was asked.
---

# Change Classification Gate

## Purpose

Decide HOW MUCH rigor a change needs before any of it is written. This skill
assigns every requested change one or more classes, maps each class to a
minimum validation level and approval path, and locks the task to that scope —
so "fix a typo" cannot silently become "alter the schema". It is the routing
layer between a request and the discipline the request deserves.

## Use When

- Use when: starting any non-trivial change (more than a trivial single-file
  text edit).
- Use when: a task appears to mix classes (docs + security, bug fix + refactor).
- Use when: mid-task, the work is about to touch a file or layer outside the
  declared scope.
- Do NOT use when: the human is asking conceptually what kind of change
  something is.
- Do NOT use when: the question is whether a specific risky action may proceed —
  that is `human-approval-boundary` (this gate decides the route; that one is
  the stop sign).
- Do NOT use when: shaping an in-progress diff — that is
  `reviewable-diff-discipline`.

## Inputs to Inspect

1. The request itself — every deliverable it names or implies.
2. The files and directories the change will plausibly touch (search before
   classifying; wording alone under-classifies).
3. Repo signals that raise a class: migration dirs, RLS/policy files, IaC dirs
   (`terraform/`, `.github/workflows/`), agent-instruction files,
   billing/payment code paths.
4. Repo policy that defines validation gates (CI config, contribution standards).
5. Any approval already granted in the current conversation, and its exact scope.

## Workflow

1. Decompose the request into concrete deliverables.
2. Assign each deliverable a class from the table below (a task may hold several).
3. The **highest-risk class governs the task's approval path**; per-deliverable
   validation floors still apply per class.
4. Declare the scope contract — classes + expected file set + validation plan —
   and state it to the human before implementing whenever an approval-class is
   present.
5. Route approval-required classes through `human-approval-boundary` BEFORE
   touching them.
6. **Scope lock:** during implementation, any file or layer outside the contract
   triggers reclassification (return to step 2) — do not keep coding into the
   new class.
7. At completion, the validation actually run must meet or exceed each class
   floor; any shortfall is disclosed in the closeout, not absorbed.

Class → validation floor (full matrix with examples:
[references/classification-matrix.md](references/classification-matrix.md)):

| Class | Validation floor | Human approval? |
| --- | --- | --- |
| docs-only | links/rendering sanity + review | no |
| ui-style | build + visual check | no |
| frontend-logic | unit tests + build | no |
| backend-api | unit/integration tests | no |
| schema-migration | migration plan + rollback + data-loss note | **yes** |
| rls-security | negative tests + security review | **yes** |
| cloud-iac | plan/diff reviewed before apply | **yes** |
| ai-agentic | eval cases + guardrail review | **yes** when behavior or tool grants change |
| qa-test-only | test run proving intent | no |
| refactor | behavior-preservation proof (tests before/after) | broad/multi-module: **yes** |
| bug-fix | failing case reproduced → passing | no |
| release-deploy | full gate: CI green + evidence + rollback plan | **yes** |

## Output Format

```
CHANGE CLASSIFICATION
Deliverables:    <list>
Classes:         <class per deliverable>
Governing class: <highest-risk class present>
Approval path:   <none | human-approval-boundary for X>
Validation plan: <per class: the floor + anything extra>
Scope contract:  <expected files/dirs>
```

## Validation Checklist

- [ ] Every deliverable classified; none classified from the request's wording
      alone (target files actually inspected).
- [ ] Mixed tasks use the highest-risk class for the approval path.
- [ ] Approval-required classes routed to `human-approval-boundary` before work.
- [ ] Scope contract stated with an explicit file set.
- [ ] Validation plan meets every class floor, or the gap is escalated.

## Gotchas

- "Quick fix" prompts routinely hide schema or security surface — inspect the
  files before classifying, not after.
- A docs task that edits agent-instruction files (CLAUDE.md and kin) is NOT
  docs-only: instruction files steer future automated behavior. Treat as
  ai-agentic.
- Test-only changes can still change effective behavior (snapshot regeneration,
  fixture edits that mask regressions).
- Refactors advertised as behavior-preserving need proof, not assertion.
- The gate is cheap; re-running it on scope growth is the point. Skipping
  reclassification because "we're almost done" is the exact failure mode this
  skill exists to stop.

## Stop Conditions

- Mid-task scope growth into a new class → stop, reclassify, obtain the new
  approval before proceeding.
- The change cannot be confidently classified (unclear which layers it touches)
  → stop and ask.
- A class's validation floor cannot be met (e.g., no test runner available for
  a backend change) → stop and surface the gap instead of shipping below floor.

## Supporting Files

- [references/classification-matrix.md](references/classification-matrix.md) —
  full matrix: per-class definitions, examples, validation detail, common
  misclassifications.
- `evals/evals.json` — trigger + behavior cases.
- `evals/trigger-evals.json` — discrimination within the change-governance
  cluster (`human-approval-boundary`, `reviewable-diff-discipline`).
