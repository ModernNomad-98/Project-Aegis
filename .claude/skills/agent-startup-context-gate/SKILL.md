---
name: agent-startup-context-gate
description: Run at the start of any repository or coding task, before reading or writing code. Verifies the working directory is the intended repo (git remote, landmark files), reads project instructions, status, and architecture docs, and separates verified facts from assumptions and missing information. Use when starting work in a repo, when told to cd into a path and build something there, or when resuming a session whose context may be stale. Halts and asks instead of building when the location or repo identity cannot be verified — a path that exists is not proof it is the right repo.
---

# Agent Startup Context Gate

## Purpose

Establish verified context before any work begins. This skill produces a Startup
Context Report proving the agent is in the intended repository, has read the
governing instructions and status docs, and has explicitly separated what it
knows (facts), what it is guessing (assumptions), and what it cannot know yet
(missing information). It exists to prevent the most expensive startup failure:
confidently building in the wrong place or against stale context.

## Use When

- Use when: starting any task that will read or modify a repository.
- Use when: instructed to `cd` into a path (or open a project) and do work there.
- Use when: resuming after an interruption, context compaction, or handoff, or
  when the conversation references repo state not verified in this session.
- Do NOT use when: continuing mid-task in a session where this gate already
  passed and neither the location nor the task scope has changed.
- Do NOT use when: answering a conceptual question with no repo action (plain
  response, not a gated startup).
- Do NOT use when: the problem is two sources contradicting each other — that is
  `source-of-truth-reconciler`.

## Inputs to Inspect

1. **Location identity:** working directory path; `git remote -v`; `git status`;
   current branch; `git log --oneline -5`.
2. **Landmark files:** README title and purpose statement; expected top-level
   directories; project manifest (`package.json`, `pyproject.toml`, `.sln`, …).
3. **Agent instructions:** `CLAUDE.md` (root and nested), `AGENTS.md`, and any
   tool-specific instruction files the repo carries.
4. **Canonical status docs:** whatever the repo designates as current
   (reconciliation records, roadmap, catalog, architecture docs).
5. **Task-referenced files:** every file or doc the task prompt names.

## Workflow

1. **Verify location identity first — before any other read or write.** Confirm
   the path exists, is a git repository, and matches the repo the task names.
   Require at least TWO independent signals: e.g. `git remote -v` matches the
   expected repo URL/name, AND a landmark file (README title, expected
   directory) matches. "The path exists" is zero signals.
2. **On any identity failure, stop.** If the path is missing, empty, not a git
   repo, has a different remote, or lacks the expected landmarks: halt, report
   exactly what was found versus what was expected, and ask. Never `git init`,
   scaffold, or start the task in an unverified location (see Gotchas).
3. **Check working-tree state.** Note the branch, whether it is behind origin,
   and any uncommitted changes the task did not mention. Fetch if currency
   matters to the task.
4. **Read the governing instructions** (CLAUDE.md / AGENTS.md / repo standards),
   then the canonical status docs, in the precedence order of
   [references/context-source-checklist.md](references/context-source-checklist.md).
5. **Confirm every task-referenced file exists** and skim each for relevance. A
   referenced-but-missing file is a blocker to surface, not to improvise around.
6. **Build the three-way inventory:** facts (verified, each with a source),
   assumptions (unverified, each with the risk if wrong), and missing
   information (split into blocking vs non-blocking).
7. **Emit the Startup Context Report** (see Output Format) and proceed only when
   location is verified and no blocking unknowns remain; otherwise ask.

## Output Format

A Startup Context Report, delivered in the conversation (or as a file if the
task asks for one):

```
STARTUP CONTEXT REPORT
Location: <path> — VERIFIED | FAILED
  Expected: <repo/remote the task implies>
  Found:    <remote, branch, landmarks actually observed>
  Signals:  <the ≥2 independent signals used>
Working tree: <branch, ahead/behind, dirty files if any>
Instructions read: <files, in order>
Facts:        <each with file:line or command evidence>
Assumptions:  <each with risk-if-wrong>
Missing info: <blocking> / <non-blocking>
Verdict: PROCEED | HALTED — <question for the human>
```

## Validation Checklist

- [ ] Location verified with at least two independent signals, not just path existence.
- [ ] Every fact cites its evidence (file:line or command output).
- [ ] No assumption silently promoted to fact.
- [ ] Every task-referenced file confirmed present, or flagged missing.
- [ ] Blocking unknowns escalated to the human, not guessed around.

## Gotchas

- **A path that exists is not the right path.** Real incident: the target
  directory existed but was empty — not the expected git repo at all — and the
  agent scaffolded a brand-new project inside it instead of stopping. Emptiness
  or missing landmarks is an identity FAILURE, not an invitation to build.
- Multiple clones or worktrees of the same repo can coexist on one machine; the
  remote matches in all of them, so also check branch and recent commits.
- Windows paths differ by case and spacing; near-miss directory names look right
  at a glance.
- A verified location can still hold stale content: local main may be behind
  origin. Verified WHERE is not verified CURRENT.
- The README's process claims may be superseded by a doc the repo marks
  canonical — read the instruction files before trusting the README.

## Stop Conditions

- Target path does not exist → stop and ask.
- Target path exists but is empty, is not a git repository, or lacks the
  expected remote/landmarks → stop, report found-vs-expected, ask. Do not init,
  scaffold, or build there.
- `git remote` points at a different repository than the task names → stop.
- Uncommitted changes or an unexpected branch the task does not account for →
  stop and ask before touching the tree.
- A file the task depends on does not exist → stop and surface it.

## Supporting Files

- [references/context-source-checklist.md](references/context-source-checklist.md) —
  identity-signal table and reading precedence, per repo type.
- `evals/evals.json` — trigger + behavior cases, including the
  exists-but-wrong-repo halt.
- `evals/trigger-evals.json` — discrimination against `source-of-truth-reconciler`
  and the change-governance gates.
