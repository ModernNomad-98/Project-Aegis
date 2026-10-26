---
name: plan-audit-reviewer
description: 'Independently audit a captured plan-of-record revision: completeness, feasibility, authority/boundary, count/protected-path coherence, acceptance observability, closure fail-before validity and owner-decision disclosure. Return CONFIRM or REVISE/REJECT with a minimal fix list bound to the exact captured revision hash. Never authors or self-approves; audit findings are backlog input only after dedupe and owner-ordered queueing. Use when a plan-of-record revision needs an independent verdict before implementation. Do NOT use to write or fix the plan (plan-of-record-author), implement the change, or prioritize the backlog.'
---

# Plan Audit Reviewer

**Reading key:** a captured revision is the exact plan text identified by its content hash. A backlog input is evidence for a future queue decision, never an execution order. CONFIRM means the plan is internally sound and evidence-based; REVISE/REJECT names the minimal fixes without prescribing implementation.

## Purpose

A plan written by the implementing agent cannot approve itself. This skill independently audits a captured plan-of-record revision against the repository and the owner's directives: completeness, feasibility, authority and boundary statements, count/protected-path coherence, acceptance observability, closure fail-before validity and owner-decision disclosure. It returns CONFIRM or REVISE/REJECT with a minimal fix list bound to the exact captured revision; it never approves (or implements) the plan it audits. Its findings are backlog input only: dedupe into the existing backlog, owner-ordered, never a second queue.

## Use When

- Use when: a Stage A plan-of-record revision must be independently audited before implementation.
- Use when: a re-audit is requested after a REVISE, bound to the new captured hash.
- Do NOT use when: writing or fixing the plan (plan-of-record-author), implementing the change, reviewing implementation diffs (code-reviewer), or prioritizing queue work.

## Inputs to Inspect

- The captured revision hash and the full plan package.
- The live repository at the claimed base head/tree and the clean worktree state.
- The count/gate/registry surfaces the plan claims to change, the gate-guard protected-path pattern, the approval register and the owner decision table.
- The closure definitions and the captured fail-before results.
- The owner directive quoted in the plan, including its source and timestamp.

## Workflow

1. Verify the captured revision hash matches the package and that no post-capture edit exists; a mismatch voids the audit.
2. Read the whole package; check the five-question answers, scope, non-goals, inventory and count delta feasibility against the live repo.
3. Re-run each claimed closure on the clean base and confirm it genuinely fails; check that after-state expectations are precise.
4. Check that every count and gate number is measured, not assumed; re-measure the base values yourself.
5. Check authority: no self-approval, no invented owner ratification, protected paths and approval routes named.
6. Check that acceptance criteria are observable and that owner decisions are surfaced, not decided.
7. Issue the verdict with a minimal fix list bound to the captured hash; route findings as backlog input only.
8. Record what could not be verified as UNRUN; unavailable evidence is never a pass.

## Output Format

A verdict block: role/identity, captured revision hash and base, verdict (CONFIRM or REVISE/REJECT), per-finding results with commands and observed output, minimal fix list, and a flat JSON object with role, verdict, commit/plan hash and findings. Findings are backlog input only.

## Validation Checklist

- [ ] Captured hash verified against the package; no post-capture edit.
- [ ] Base head/tree independently re-measured and clean.
- [ ] Every claimed closure re-run and confirmed fail-before; after-state expectations precise.
- [ ] Counts/gate numbers independently measured, not trusted from the plan.
- [ ] Authority and protected-path statements correct; no self-approval or invented ratification.
- [ ] Acceptance criteria observable; owner decisions surfaced not decided.
- [ ] Unverifiable items marked UNRUN, never passed.
- [ ] Verdict and minimal fix list bound to the captured hash; findings routed as backlog input only.

## Gotchas

- Do not audit the working tree instead of the captured revision, and do not re-freeze the plan yourself.
- A plan can pass on presence while failing on substance; re-run the checks rather than trusting wording.
- Do not treat an advisory review or an agent's assertion as an owner decision.
- Do not prescribe implementation inside the minimal fix list; name the defect and the acceptance condition.

## Stop Conditions

- Stop when the captured hash cannot be verified; the audit cannot bind.
- Stop when the base cannot be reconstructed cleanly; report UNRUN.
- Never author, fix, implement, approve or merge; report only.

## Supporting Files

- references/plan-audit-checklist.md
