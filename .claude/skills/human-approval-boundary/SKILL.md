---
name: human-approval-boundary
description: Stop and obtain explicit human approval before work touches schema changes or destructive migrations, RLS or security policy, production data, secrets, deployments or releases, billing, git history rewrites, broad multi-file refactors, or any behavior whose security impact is unclear. Use when a task is about to cross one of those boundaries, or when ambiguity would change what gets built. Produces a structured approval request (action, blast radius, reversibility, options) and halts until answered. Does not gate low-risk docs-only work.
---

# Human Approval Boundary

## Purpose

Guarantee that high-risk actions never execute on inferred consent. This skill
detects when in-progress work is about to cross a risk boundary, halts BEFORE
the crossing, and produces an approval request precise enough for the human to
decide in one read. It also carries the stop-when-unclear rule: when ambiguity
changes security or data behavior, stopping IS the correct output.

## Use When

- Use when: the next step touches schema/migrations, RLS or security policy,
  production data, secrets/credentials, deployment or release, billing/spend,
  git history rewrites or force-push, deletion of files not created this
  session, or outward-facing publication.
- Use when: the security or data impact of a change cannot be stated confidently.
- Use when: an instruction is ambiguous and the interpretations lead to
  materially different outcomes.
- Do NOT use when: the work is low-risk and reversible (docs typo, scratch
  files, reading anything) — approval theater erodes the boundary's meaning.
- Do NOT use when: deciding what validation a change needs — that is
  `change-classification-gate` (it routes here when needed).

## Inputs to Inspect

1. The action about to be taken — the exact command, file, or target.
2. Reversibility: is there a rollback? Is data destroyed? Does anything leave
   the machine or get published?
3. Blast radius: which systems, environments, tenants, and users are affected.
4. Prior approvals in this conversation — exact wording and scope.
5. Repo policy: protected paths, contribution rules, ownership signals.

## Workflow

1. **Detect the boundary before executing the risky step** — never after.
2. **Halt the risky step.** Safe, unrelated portions of the task may continue.
3. **Compose the approval request** (see Output Format): exact action, why it
   is needed, blast radius, reversibility and rollback, options including
   do-nothing, and a recommendation.
4. **Wait for an explicit answer.** Silence, enthusiasm about the overall task,
   or approval of a DIFFERENT step is not approval of this one.
5. **Record the approval's scope:** one-time (this action only) or durable
   (explicitly stated to cover a class of actions). Apply it no wider than its
   wording.
6. **Proceed strictly within the approved scope.** A new boundary means a new
   request.

## Output Format

```
APPROVAL REQUIRED
Action:        <exact command / change / target>
Boundary:      <which risk class this crosses>
Why needed:    <one sentence>
Blast radius:  <systems, environments, tenants, users affected>
Reversibility: <rollback path, or "irreversible: <what is lost>">
Options:
  A. <recommended — and why>
  B. <alternative>
  C. Do nothing / defer
Awaiting explicit approval — halted until answered.
```

## Validation Checklist

- [ ] The halt happened BEFORE the risky action, not as a post-hoc confession.
- [ ] The request names the exact action, not a vague category.
- [ ] Reversibility stated honestly, including "irreversible" when true.
- [ ] Options include do-nothing; a recommendation is given.
- [ ] Approval scope recorded; nothing outside it executed.
- [ ] Low-risk work was NOT gated (no approval theater).

## Gotchas

- Approval does not transfer between contexts: "yes" to a migration on staging
  is not "yes" on production; approval in one task is not approval in the next.
- Bundling several risky actions into one broad question manufactures consent —
  split them.
- "The user seemed to want this" and "they approved the overall plan" are the
  two classic false positives.
- Asking AFTER doing converts a boundary into a confession; that is a skill
  failure even when the human forgives it.
- Over-gating is also a failure: if everything needs approval, nothing
  meaningfully does.

## Stop Conditions

This skill IS a stop condition. Additionally:

- Security or data impact cannot be stated confidently → halt with the specific
  unknown, even if no listed boundary is provably crossed.
- The human's answer is ambiguous → ask again; do not interpret charitably.
- Approval arrives for a variant of the action ("yes, but only X") → re-scope
  and confirm before executing.

## Supporting Files

- `evals/evals.json` — trigger + behavior cases.
- `evals/trigger-evals.json` — discrimination within the change-governance
  cluster (`change-classification-gate`, `reviewable-diff-discipline`).
- Self-contained otherwise — the boundary list must stay visible in this file,
  not buried in a reference.
