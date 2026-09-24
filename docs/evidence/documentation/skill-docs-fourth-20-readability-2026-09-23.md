# Fourth 20 skill documents: bounded readability correction — 2026-09-23

## Current reading

This is dated delivery evidence. Its original base commit, estimates, counts,
and pending-review language describe that historical batch. For current
acceptance totals and remaining work, use the [documentation ledger](../../roadmaps/aegis-documentation-readability-backlog.md) and [forecast](../../roadmaps/aegis-backlog-forecast.md); follow the linked owning skill or reference for current guidance. This note does not grant implementation or merge authority.

## Scope and timing

A read-only sweep of the 20 skill guides after `data-quality-monitor-designer`
identified three unexplained terms in documentation and execution guidance.
This batch changes only [Docs-First Implementer](../../../.claude/skills/docs-first-implementer/SKILL.md),
[Docs Retention Index](../../../.claude/skills/docs-retention-index/SKILL.md),
[Gated Deployment Prompt Template](../../../.claude/skills/gated-deployment-prompt-template/SKILL.md),
and this note. It began in an isolated worktree at
**2026-09-23 19:52:03 UTC** (Coordinated Universal Time) from `origin/main`
`4343d8c6322f974b2eb62c1d5b1529d85d6a9c7d`, after pull request #152.

The previous estimate for this batch was **2–4 active hours**, and the new
bounded estimate remains **2–4 active hours**. The selected backlog total is
**175–394 active hours**. These are planning ranges; active labor was not
instrumented. The first local checkpoint at **19:54:27 UTC** was **2 minutes
24 seconds** after the recorded start.

## Reader path and changes

Use the skill's Purpose and Use When to select the task, then follow its
Workflow and Output Format. The docs-first guide now defines
Task-Authorized Local Implementation (TALI) and links to the governing
[skill-generation standard](../../skill-generation-standard.md#5-least-privilege--side-effects).
The text retains the rule that explicit invocation of this manual-only skill
does not activate TALI; the separate route still needs its own classification
and activation.

The retention guide states the squash-merge rollback rule directly, in place
of an unexplained historical decision code, and spells out the output's row
number placeholder. It still requires a reverse-reference sweep and human
approval for deletion. The deployment template identifies “Repo B” as an
anonymized source in the [workflow extraction report](../../research/aegis-workflow-extraction-report.md),
defines estimated time-to-complete (ETA) on first use, and labels the operator
placeholders and estimated run duration clearly. It still authors a template
and index without executing an operation.

The three skill frontmatter blocks, invocation posture, trigger and behavior
evaluation fixtures, technical criteria, and approval boundaries are unchanged.
No manual-only skill was invoked and no operation was run.

## Verification

- `python -B scripts/validate-skills.py`: **185 valid skills, 0 warnings**.
- The six existing trigger and behavior evaluation files remain unchanged;
  their authority and output expectations were inspected for wording impact.
- All **12 local relative links** in the four scoped pages resolve, including
  the skill-generation standard's section 5 anchor; `git diff --check` passes.
- Independent read-only review reported **no blocker** at
  **2026-09-23 19:55:47 UTC**, before the Developer Certificate of Origin
  (DCO) signed commit. No push or pull request is part of this writer batch.
