---
name: agent-authorization-matrix
description: MANUAL-ONLY; never auto-invoke. Define a deny-by-default authorization matrix for AI agents across actions and contexts. Protected-branch merge requires an explicit human decision, which may be a still-active, scoped standing grant; green checks alone are never approval. Arming auto-merge is forbidden to agents by default and is a separate action from merging. Deploys, releases, production data, secrets, and history rewrites require their own decisions. Invoke explicitly to design or revise agent authority, after an autonomy incident, or to write an agent-permissions policy. Proposal-first; edit governance artifacts after approval. Do not use for end-user permissions (authorization-matrix-designer) or an in-flight stop (human-approval-boundary).
disable-model-invocation: true
---

# Agent Authorization Matrix

**Reading key:** A pull request (PR) proposes a repository change;
continuous integration (CI) runs automated checks; a command-line interface
(CLI) is a terminal tool. This skill writes an authority policy and is
manual-only; it does not grant permission to merge or deploy.

## Purpose

Make agent authority explicit instead of inferred. This skill produces the
standing, deny-by-default matrix of what an AI agent may do on its own
authority, what requires a named human decision, and what is forbidden — per
action class and execution context. It is the governance control for merge and
deploy authority: `human-approval-boundary` halts at a boundary in-flight; this
matrix IS the boundary definition it enforces. Its non-negotiable floor exists
because of a real incident class: auto-merge armed in one session fired in a
later one, merging a security-relevant PR with zero human review.

## Use When

- Use when (explicitly invoked by a human): defining or revising what an agent
  may plan, edit, test, commit, push, PR, merge, or deploy without further
  approval — for a repo, team, or agent fleet.
- Use when: granting or revoking a specific agent authority, or onboarding
  agents to a repo that has no written permission policy.
- Use when: after an autonomy incident — an agent merged, deployed, or
  destroyed something nobody approved — to codify the corrected authority.
- Do NOT use when: a risky action is imminent mid-task — that halt is
  `human-approval-boundary` (it enforces this matrix; it does not define it).
- Do NOT use when: designing roles × permissions for end users or tenants of a
  product — that is `authorization-matrix-designer`. This skill governs the
  AGENTS building the product, not the product's users.
- Do NOT use when: defining the overall workflow stages — that is
  `ai-sdlc-operating-model`, which cites this matrix for its authority column.
- Never auto-invoked: the matrix is a behavior-steering governance artifact —
  supply-chain-sensitive, human-initiated only (`disable-model-invocation: true`).

## Inputs to Inspect

1. Branch protection and merge settings: required reviews and checks, who may
   merge, whether auto-merge is enabled repo-wide
   (`gh api repos/{owner}/{repo}` → `allow_auto_merge`, branch protection).
2. Existing permission statements scattered across `CLAUDE.md`, `AGENTS.md`,
   contribution docs, and any auto-merge policy doc — the fragments the matrix
   consolidates.
3. Incident history: every past case of an agent exceeding intended authority,
   and which missing rule allowed it.
4. Deploy/release pipelines: what a push, tag, or merge actually triggers —
   a "commit" that auto-deploys is a deploy authority question, not a commit.
5. The agent surfaces in use (CLI sessions, CI bots, scheduled agents) — each
   context the matrix must cover.
6. An existing matrix, if any: this run revises it, never forks a second one.

## Workflow

1. **Inventory agent-reachable actions** using the taxonomy in
   [references/matrix-template.md](references/matrix-template.md): read/plan,
   edit, test, commit, push (feature branch), open PR, comment/review, merge,
   arm/disarm auto-merge, tag/release, deploy, production data, secrets,
   memory and instruction-file edits, history rewrites.
2. **Inventory contexts:** scratch/worktree, feature branch, protected branch,
   CI, staging, production. A cell is action × context.
3. **Fill the matrix deny-by-default.** Every cell gets AUTONOMOUS,
   APPROVAL-REQUIRED, or FORBIDDEN plus a one-line rationale. Any action not
   listed is APPROVAL-REQUIRED by definition.
4. **Apply the non-negotiable floor** (weakening any of these requires an
   explicit, recorded human decision in the artifact itself):
   - Merging to a protected branch: APPROVAL-REQUIRED, always. Without an
     applicable explicit human decision, the terminal action is open PR and
     stop. A scoped, still-active durable human grant can satisfy this cell;
     verify repository identity, grant history, action scope, and later owner
     instructions before relying on it. Do not infer approval from green CI.
   - Arming auto-merge: FORBIDDEN for agents. Arming is merge authority
     exercised early — it outlives the session and fires on future green CI.
     Agents also RE-CHECK for armed auto-merge on their PRs after every push
     (`gh pr view <n> --json autoMergeRequest`) and treat an armed state not
     traceable to a recorded human decision as a hazard: disarm and flag.
   - Deploys, production data, secrets, history rewrites: APPROVAL-REQUIRED.
5. **Define approval semantics:** one-time vs durable, exact scope wording,
   expiry, and where approvals are recorded — composing the scope rules of
   `human-approval-boundary`, not redefining them.
6. **Propose the artifact** (location per repo convention, e.g.
   `docs/governance/agent-authorization-matrix.md`), including how the matrix
   itself is protected from agent self-modification. **STOP for approval.**
7. **Apply after approval** — exactly the approved matrix, nothing more; set a
   review date; record the approving human in the artifact.

## Output Format

```
AGENT AUTHORIZATION MATRIX
Scope:      <repo / team / fleet>   Approved by: <human>   Review: <date>
Matrix:     <action × context → AUTONOMOUS | APPROVAL-REQUIRED | FORBIDDEN, rationale>
Floor:      <the non-negotiable rows, stated in full>
Approvals:  <one-time vs durable semantics, recording location>
Self-protection: <how agents are prevented from editing this artifact silently>
Status:     AWAITING APPROVAL | APPLIED (approved by <human>, <date>)
```

## Validation Checklist

- [ ] Deny-by-default holds: unlisted action = APPROVAL-REQUIRED.
- [ ] Merge-to-protected, arm-auto-merge, deploy, production-data, secrets,
      and history-rewrite cells are approval-required or forbidden. Any
      exception has an explicit human decision recorded in the applicable
      repository, with scope and later instructions checked.
- [ ] Every AUTONOMOUS cell has a rationale; none granted by omission.
- [ ] Approval semantics (scope, durability, expiry, recording) are defined.
- [ ] No governance file edited before explicit approval.
- [ ] The matrix documents its own protection against agent self-modification.

## Gotchas

- Auto-merge is the classic authority leak: armed while checks were red, it
  merges the moment CI goes green — in a later session, with nobody watching.
  The incident that motivated this skill merged a security PR to main exactly
  that way. Arming is therefore treated as the merge decision itself.
- CI green is validation, not authorization. A matrix cell must never read
  "AUTONOMOUS if checks pass" for merge-class actions. A grant for the merge
  method does not automatically waive a later all-checks-green instruction.
- Approval of a plan is not approval of the merge; approval on staging is not
  approval on production. Durable approvals apply no wider than their wording
  and do not transfer to another repository when skills are copied.
- A "commit" that a pipeline auto-deploys is a deploy. Classify cells by what
  the action TRIGGERS, not what the git verb is called.
- A matrix agents can silently edit is self-granted authority; store it where
  changes are reviewed (protected path, gate-guard-style check).
- Over-restriction backfires: if agents need approval to run tests, humans
  start rubber-stamping, and the meaningful gates drown in noise.

## Stop Conditions

- Proposal complete → full stop until explicit human approval. Applying an
  unapproved authorization matrix is this skill's defining failure.
- Asked to grant agents merge, deploy, or auto-merge-arming authority without
  an applicable explicit human decision → halt and route through
  `human-approval-boundary`. A standing human grant can satisfy a particular
  approval-required action; it does not silently change another action or a
  later owner constraint. Record new grants with their accepted risk.
- An armed auto-merge or standing permission is discovered that no recorded
  human decision explains → halt, disarm/flag, and report before continuing.
- The matrix's storage location cannot be protected from silent agent edits →
  flag the gap and get an explicit decision before publishing the artifact.

## Supporting Files

- [references/matrix-template.md](references/matrix-template.md) — action
  taxonomy, context list, copyable matrix template with the default floor
  pre-filled, and the auto-merge incident case study.
- `evals/evals.json` — behavior cases, including the auto-merge incident
  (positive: open PR and stop; negative: never merge on own authority).
- `evals/trigger-evals.json` — discrimination against `human-approval-boundary`,
  `authorization-matrix-designer`, and the Phase 1.5 siblings.
