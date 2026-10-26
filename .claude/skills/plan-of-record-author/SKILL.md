---
name: plan-of-record-author
description: 'Turn a request or owner directive into ONE plan-of-record artifact package before implementation: what/why, blast radius and paths, five-question necessity/reuse, scope plus protected-path/authority map, proportionate acceptance criteria, executable fail-before/pass-after closures, residual owner decisions surfaced not decided, verification and re-base plan, and non-circular evidence bindings. Never approves its own plan; hands the captured revision to an independent plan auditor. Use when a non-trivial Role A change needs a plan-of-record. Do NOT use to audit a plan (plan-audit-reviewer), split a broad goal (ai-task-decomposer), request risky-action approval (human-approval-boundary), or check acceptance criteria only (acceptance-criteria-reviewer).'
---

# Plan of Record Author

**Reading key:** a plan of record (PoR) is the single written plan an agent and its reviewers treat as authoritative for one change. A closure is an executable check that must fail before the change and pass after it. A protected path is a file a gate or approval rule controls. An owner decision is a choice only the human owner may make.

## Purpose

Non-trivial changes fail in review when the plan is scattered across chat, guesses and a partial checklist. This skill writes ONE plan-of-record package before any implementation: the objective and why, blast radius and exact paths, the five-question necessity/reuse answers, scope and the protected-path/authority map, proportionate acceptance criteria, executable fail-before/pass-after closures, the owner decisions surfaced (never decided by the agent), the verification and re-base plan, and evidence bindings. It never implements and never approves its own plan; the captured revision goes to an independent plan auditor.

## Use When

- Use when: a non-trivial change in the Project Aegis source library needs a written plan before implementation.
- Use when: a wave or lane starts and the coordinator needs the plan artifact package (PLAN, SPECS-ANNEX, A-ROWS, IMPACT, plan-binding, INDEX).
- Use when: an owner directive must become a reviewable plan without the agent inventing authority.
- Do NOT use when: auditing a plan (plan-audit-reviewer), splitting a broad goal into ordered tasks (ai-task-decomposer), requesting approval for a risky action (human-approval-boundary), or reviewing only acceptance criteria (acceptance-criteria-reviewer).

## Inputs to Inspect

- The owner directive or queue item, quoted verbatim with its source and timestamp.
- The current default-branch head and tree (read-only checkout), plus any worktree actually used.
- The registries the change touches: README markers/roster, docs/skills-catalog.md, tools/skills-manifest.json, docs/skills/coverage-map.json/.md, validator count pins, test literals, audit baselines.
- The gate-guard pattern and protected-path list, the delivery workflow's stage rules, the approval register entries and the owner decision table.
- The existing plan package format and its binding rules (INDEX and final verification pinned non-circularly).

## Workflow

1. Read the directive and the working base; record the exact commit/tree and worktree cleanliness.
2. Inventory every surface the change touches and the counts that must move; measure them with commands, not from memory.
3. Draft the plan package: objective, five-question necessity/reuse answers, scope, non-goals, blast radius, exact file list, count deltas and gate expectations.
4. Write acceptance criteria and executable closures that genuinely fail before the change; record base results.
5. Surface each residual owner decision with its default and consequences; never decide an owner decision yourself.
6. Bind the artifacts (bytes/LF/sha256) non-circularly; the INDEX may list the final-verification identity and the binding may list both, but neither may embed its own or the binding hash.
7. Hand the captured revision (hash of the exact text) to an independent plan auditor; no self-approval.
8. Record the re-base rule and stop at Stage A; do not implement, push or merge.

## Output Format

A plan-of-record package under the evidence item directory: PLAN.md (concise, size-capped), SPECS-ANNEX.md (inventory, supersession, skill specs, counts, matrix), A-ROWS.json (acceptance rows and executable closures), IMPACT.md, plan-binding.json (non-circular bindings), INDEX.md, captures/, and final-verification.txt. Plus a one-paragraph handoff naming the captured revision hash.

## Validation Checklist

- [ ] Base head/tree measured this turn and the worktree state recorded.
- [ ] Every count and gate expectation is evidence-based, with the command that measured it.
- [ ] Closures are executable and fail before the change (captured), and the expected after-state is explicit.
- [ ] Protected paths and approval/authority routes are named; no approval or merge authority is claimed.
- [ ] Owner decisions are surfaced with defaults, never decided.
- [ ] Artifact identities are measured and bound non-circularly.
- [ ] The plan contains no implementation and no self-approval.
- [ ] The handoff names the exact captured revision hash.

## Gotchas

- A plan that quotes stale counts or line anchors will be rejected by the independent auditor; re-measure at the current head.
- Do not claim closure results that were not executed; record fail-before evidence and defer pass-after to the implementation head.
- Never move the "owner ratification" claim from the owner's words to an agent's inference.
- Do not re-freeze artifacts after measuring only some of them; all identities must be measured after the last edit.

## Stop Conditions

- Surface a required owner decision as an OPEN owner decision (options, defaults, consequences) and keep drafting the rest of the package; stop only when the next step would require choosing without a recorded default, and never choose the owner's decision yourself.
- Stop when the working base is dirty or cannot be verified.
- Stop when a proposed closure cannot genuinely fail before the change (it proves nothing).
- Never implement, push, merge or approve; hand off instead.

## Supporting Files

- references/plan-of-record-package.md
