---
name: human-approval-boundary
description: Check current task instructions, prior conversation grants and the owner approval register before a risky action. Proceed within an active scoped grant; obtain a new explicit human approval only when the action is not covered or its security impact is unclear. Covers schema changes or destructive migrations, RLS or security policy, production data, secrets, deployments or releases, billing, git history rewrites and broad multi-file refactors. Use when a task approaches one of these boundaries or ambiguity would change what gets built. Produces a precise approval request and halts only for the uncovered action. Does not gate low-risk docs-only work.
---

# Human Approval Boundary

Terms: **RLS** means row-level security.

## Purpose

Guarantee that high-risk actions stay within explicit authority. This skill
checks current instructions and active standing or task-specific grants before
a risk boundary. It proceeds within a matching grant and asks only for an
uncovered or ambiguous action. When needed, the approval request states the
exact action and impact so the human can decide in one read.

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
5. The repository's owner approval register if one exists, including later
   lifecycle events, and repo policy for protected paths and contribution.

## Workflow

1. **Detect the boundary before executing the risky step** — never after.
2. **Check active authority.** Match the exact action to current user
   instructions, conversation grants and the approval register's scope and
   lifecycle. A durable grant applies to later matching actions until changed
   or revoked. Proceed within a matching grant without asking again.
3. **Only if no grant covers the action, prepare it for review.** Continue safe, authorized
   work; halt only the uncovered risky step.
4. **For the uncovered action, compose the approval request** (see Output Format): exact action, why it
   is needed, blast radius, reversibility and rollback, options including
   do-nothing, and a recommendation.
5. **For the uncovered action, wait for an explicit answer.** Silence, enthusiasm about the overall task,
   or approval of a DIFFERENT step is not approval of this one.
6. **Record the approval's scope:** one-time (this action only) or durable
   (explicitly stated to cover a class of actions). Apply it no wider than its
   wording.
7. **Proceed strictly within the approved scope.** Ask again only when the
   next action falls outside active authority.

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

- Approval follows its recorded scope across tasks when durable. "Yes" to
  staging does not cover production unless its wording explicitly does.
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
  to X and proceed within X. Clarify only if X is ambiguous.

## Supporting Files

- `evals/evals.json` — trigger + behavior cases.
- `evals/trigger-evals.json` — discrimination within the change-governance
  cluster (`change-classification-gate`, `reviewable-diff-discipline`).
- Self-contained otherwise — the boundary list must stay visible in this file,
  not buried in a reference.
