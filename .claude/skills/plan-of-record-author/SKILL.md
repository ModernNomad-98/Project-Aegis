---
name: plan-of-record-author
description: 'Turn a request or owner directive into ONE plan-of-record artifact package before implementation: what/why, blast radius and paths, five-question necessity/reuse, scope plus protected-path/authority map, proportionate acceptance criteria, executable fail-before/pass-after closures, residual owner decisions surfaced not decided, verification and re-base plan, and non-circular evidence bindings. Never approves its own plan; hands the captured revision to an independent plan auditor. Use when a non-trivial change in the Project Aegis source library (Role A) or a consumer/product repository that copied the skills (Role B) needs a plan-of-record; Role B writes the package only under the documentation-write rule (Exception 1), within the consumer''s own approvals. Do NOT use to audit a plan (plan-audit-reviewer), split a broad goal (ai-task-decomposer), request risky-action approval (human-approval-boundary), or check acceptance criteria only (acceptance-criteria-reviewer).'
---

# Plan of Record Author

**Reading key:** a plan of record (PoR) is the single written plan an agent and its reviewers treat as authoritative for one change. A closure is an executable check that must fail before the change and pass after it. A protected path is a file a gate or approval rule controls. An owner decision is a choice only the human owner may make. **Role A** is the Project Aegis source library; **Role B** is a consumer/product repository that copied the Aegis skills.

## Purpose

Non-trivial changes fail in review when the plan is scattered across chat, guesses and a partial checklist. In either role, this skill writes ONE plan-of-record package before any implementation: the objective and why, blast radius and exact paths, the five-question necessity/reuse answers, scope and the protected-path/authority map, proportionate acceptance criteria, executable fail-before/pass-after closures, the owner decisions surfaced (never decided by the agent), the verification and re-base plan, and evidence bindings. In Role B the package is written in the consumer repository's own authorized evidence path under the documentation-write rule (Exception 1), within the consumer's own approvals and human merge gate; Role A keeps the source-library path. It never implements and never approves its own plan; the captured revision goes to an independent plan auditor.

## Use When

- Use when: a non-trivial change in the Project Aegis source library (**Role A**) needs a written plan before implementation.
- Use when: a non-trivial change in a consumer/product repository that copied the Aegis skills (**Role B**) needs the same plan-of-record package before implementation; the package is written in that repository's own authorized evidence path, under Exception 1, and the consumer's own approvals and human merge gate govern.
- Use when: a wave or lane starts and the coordinator needs the Role A plan artifact package (PLAN, SPECS-ANNEX, A-ROWS, IMPACT, plan-binding, INDEX).
- Use when: an owner directive must become a reviewable plan without the agent inventing authority.
- Do NOT use when: auditing a plan (plan-audit-reviewer), splitting a broad goal into ordered tasks (ai-task-decomposer), requesting approval for a risky action (human-approval-boundary), or reviewing only acceptance criteria (acceptance-criteria-reviewer).

## Inputs to Inspect

**Both roles:** the owner directive or queue item, quoted verbatim with its source and timestamp; the current default-branch head and tree (read-only checkout) plus any worktree actually used; and the repository's own role evidence (AGENTS.md Role A/Role B landmarks), because the role decides the authority route.

**Role A (Project Aegis source library) — as today:**
- The registries the change touches: README markers/roster, docs/skills-catalog.md, tools/skills-manifest.json, docs/skills/coverage-map.json/.md, validator count pins, test literals, audit baselines.
- The gate-guard pattern and protected-path list, the delivery workflow's stage rules, the approval register entries and the owner decision table.
- The existing plan package format and its binding rules (INDEX and final verification pinned non-circularly).

**Role B (consumer/product repository):**
- The consumer repository's own identity/role evidence and the claimed base head/tree; the approved product specification/requirements and acceptance criteria for this change.
- The consumer's `docs/project-state.md` and its recorded design/build authority and decisions.
- The consumer's own approvals and authority records — `human-approval-boundary` and `scoped-approval-register` are always installed in the starter package and are used under the consumer's own approval route; the consumer's own validation and closure checks for this change.
- Explicit: the source library's registries, read-only command allowlist and approval register are **not required and not assumed** in Role B.
- The change's recorded class from the consumer's `change-classification-gate` (from the consumer's own recorded class); a plan that cannot record a real class is not written — route it through the consumer's change classification or stop and hand the decision over; "unclassified" is never accepted as a class.

## Workflow

1. **Detect the role from repository evidence** (AGENTS.md Role A/Role B landmarks, path, project files). If the role is genuinely ambiguous, ask one question and do not write; never guess a role to unlock a write.
2. Read the directive and the working base; record the exact commit/tree and worktree cleanliness.
3. Inventory every surface the change touches. Role A: the source counts that must move, measured with commands. Role B: the product surfaces and the consumer repository's own checks; never claim or require source-only registries.
4. Draft the plan package: objective, five-question necessity/reuse answers, scope, non-goals, blast radius, exact file list, count/route deltas (Role A) or repository-check deltas (Role B), and gate expectations; record the change's classification — Role A from `change-classification-gate` (delivery-workflow Stage A rule), Role B the consumer's own classification from the consumer's own recorded class; if classification cannot be completed, stop and hand the decision over — do not write an unclassified plan.
5. Write acceptance criteria and executable closures that genuinely fail before the change; record base results. The package also records the verification and re-base plan: what to re-measure, and how to re-base (and what to re-audit) if the base moves before the implementation head. Before executing any closure command, apply the same safety preflight as the auditor: execute only closures whose provenance you can verify as read-only; record networked, privileged, state-changing, secret-accessing or unverifiable closures as UNRUN and require the `human-approval-boundary` instead — never mutate a database, download dependencies, rewrite snapshots or touch a live service merely to author a plan.
6. Surface each residual owner decision with its default and consequences; in Role A that is the source owner's decision, in Role B the consumer's own. Never decide an owner decision yourself.
7. Bind the artifacts (bytes/LF/sha256) non-circularly; the INDEX may list the final-verification identity and the binding may list both, but neither may embed its own or the binding hash.
8. **Write-authority step for the package:** with the package complete — including the acceptance criteria and closures, owner decisions and the artifact binding — show the exact target path and the complete final content, then apply the documentation-write rule (Exception 1: a current-session instruction that already authorizes this bounded documentary recording, or content-specific single-use approval). Any content added or changed after approval must be shown and covered by the grant before it is written. Role A: the source `_A/evidence/<item>/` path defined by the delivery workflow. Role B: only the consumer repository's own authorized evidence path; no arbitrary path. If the path/content is not authorized, hand the complete package content over in the conversation and ask, or hand the recording decision to `project-orchestrator` — never write anyway.
9. Hand the captured revision (hash of the exact text) to an independent plan auditor; no self-approval. Stop at Stage A; do not implement, push or merge.

## Output Format

A plan-of-record package whose files (PLAN.md, SPECS-ANNEX.md where applicable, A-ROWS.json, IMPACT.md, plan-binding.json, INDEX.md, captures/, final-verification.txt) are the same in both roles; the directory is **relative to the working repository**: Role A `_A/evidence/<item>/` (the delivery-workflow Stage A artifact, L106-108); Role B the consumer repository's own `_A/evidence/<item>/`, with the exact path and complete content shown and authorized under Exception 1 before any write. A Role B change with no skill-spec annex may omit SPECS-ANNEX only if the package says so; do not invent an annex. The package records the change's classification (Role A from `change-classification-gate`; Role B from the consumer's own recorded class; a plan without a real class is not accepted). Plus a one-paragraph handoff naming the captured revision hash.

## Validation Checklist

- [ ] The role (Role A source library or Role B consumer/product repository) was detected from repository evidence, or one question was asked and nothing was written.
- [ ] Base head/tree measured this turn and the worktree state recorded.
- [ ] Role A: source counts and gate expectations are evidence-based, with the command that measured them. Role B: the consumer repository's own checks and authority are named; no source-only registry, allowlist or approval register is claimed or required.
- [ ] The package write path and complete content were shown and authorized under Exception 1, or nothing was written and the decision was handed over.
- [ ] Closures are executable and fail before the change (captured), and the expected after-state is explicit.
- [ ] The plan records the change's classification for its role (Role A from change-classification-gate; Role B the consumer's real recorded class; an unclassified plan is not accepted).
- [ ] The package records the verification and re-base plan, and step 8's complete-content approval covers it.
- [ ] Protected paths and approval/authority routes are named for the correct role; no source approval is claimed in Role B; no approval or merge authority is claimed.
- [ ] Owner decisions are surfaced with defaults, never decided; in Role B they are the consumer's decisions.
- [ ] Artifact identities are measured and bound non-circularly.
- [ ] The plan contains no implementation and no self-approval; the handoff names the exact captured revision hash.

## Gotchas

- A plan that quotes stale counts or line anchors will be rejected by the independent auditor; re-measure at the current head.
- Do not claim closure results that were not executed; record fail-before evidence and defer pass-after to the implementation head.
- Never move the "owner ratification" claim from the owner's words to an agent's inference.
- Do not re-freeze artifacts after measuring only some of them; all identities must be measured after the last edit.
- Do not carry a source-only assumption into Role B: the source approval register and the source read-only allowlist do not exist in a consumer repository and are not inherited.

## Stop Conditions

- The role is genuinely ambiguous after reading the repository evidence → ask one question and write nothing.
- Surface a required owner decision as an OPEN owner decision (options, defaults, consequences) and keep drafting the rest of the package; stop only when the next step would require choosing without a recorded default, and never choose the owner's decision yourself.
- Role B has no authorized evidence path/content → stop and hand the write decision to the human/`project-orchestrator`; never write anyway, and never write source-library state, registries, catalog, manifest, coverage or approval files in Role B.
- Never claim a Role A approval or protected-path authority in Role B; Role B uses the consumer's own approvals and the human remains the merge gate.
- Stop when the working base is dirty or cannot be verified.
- Stop when a proposed closure cannot genuinely fail before the change (it proves nothing).
- Never implement, push, merge or approve; hand off instead.

## Supporting Files

- references/plan-of-record-package.md
