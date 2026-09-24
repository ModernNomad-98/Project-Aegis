---
name: agent-startup-context-gate
description: Run at the start of any repository or coding task, before reading or writing code. Verifies the working directory and workspace role from available evidence, reads project instructions and status docs, and separates verified facts from assumptions and missing information. A fresh product repository may have no remote, commits, application files, or project-state document. Use when starting work in a repo, when told to cd into a path and build something there, or when resuming a session whose context may be stale. Ask when the intended location or role is genuinely ambiguous — a path that exists is not proof it is the right repo.
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

1. **Location identity:** working directory path, task-named workspace, and
   available `git remote -v`, `git status`, branch, and recent history. A fresh
   zero-commit product repository may have no remote or history.
2. **Landmark files:** README title and purpose statement; expected top-level
   directories; project manifest (`package.json`, `pyproject.toml`, `.sln`, …).
3. **Agent instructions:** `CLAUDE.md` (root and nested), `AGENTS.md`, and any
   tool-specific instruction files the repo carries.
4. **Canonical status docs:** whatever the repo designates as current
   (reconciliation records, roadmap, catalog, architecture docs).
5. **Task-referenced files:** every file or doc the task prompt names.

## Workflow

1. **Verify location and role before task writes or skill selection.** Reading
   local instructions and source landmarks is part of this verification. Confirm
   that the current path is the task's intended workspace using available
   independent signals, such as a matching remote and project landmarks in an
   established repository. For Project Aegis source-library work, require the
   four source-package landmarks in `AGENTS.md`; copied startup files alone
   do not establish source-library role. Classify as consumer/product when
   task and local evidence support it; otherwise ask one role question. A fresh
   Stage 0 product repository can have zero commits, no remote, no application
   files and no `docs/project-state.md`. Use the task-named current workspace
   and its instructions to classify it as the product repository. "The path
   exists" alone is zero signals.
2. **On genuine identity ambiguity or contradiction, stop.** A missing target,
   a remote pointing to a different named project, or conflicting project
   landmarks needs one found-versus-expected clarification before writing.
   A missing remote, history, application file or source-library landmark in
   a fresh product repository is not by itself a failure. Do not redirect a
   fresh product into a sibling folder. Never initialize or scaffold a
   genuinely unverified location (see Gotchas).
3. **Check working-tree state.** Note the branch, whether it is behind origin,
   and any uncommitted changes the task did not mention. Fetch if currency
   matters to the task.
4. **Finish the governing-instruction and status pass** after the initial
   role check. Read the relevant CLAUDE.md / AGENTS.md / repo standards in
   full, then the canonical status docs, in the precedence order of
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
  Expected: <task-named workspace and role>
  Found:    <available remote, branch, landmarks and instructions>
  Signals:  <independent location/role evidence used; missing fresh-repo signals identified>
Working tree: <branch, ahead/behind, dirty files if any>
Instructions read: <files, in order>
Facts:        <each with file:line or command evidence>
Assumptions:  <each with risk-if-wrong>
Missing info: <blocking> / <non-blocking>
Verdict: PROCEED | HALTED — <question for the human>
```

## Validation Checklist

- [ ] Location and role verified from available independent evidence; absent
      remote/history is not treated as failure in a fresh product repository.
- [ ] Every fact cites its evidence (file:line or command output).
- [ ] No assumption silently promoted to fact.
- [ ] Every task-referenced file confirmed present, or flagged missing.
- [ ] Blocking unknowns escalated to the human, not guessed around.

## Gotchas

- **A path that exists is not the right path.** In an established-repository
  task, an empty directory with no matching project evidence is ambiguous;
  do not scaffold it. A task that names a fresh Stage 0 product repository
  with copied startup instructions is different: absent commits, remote and
  application files can be its expected state. Work in that current workspace
  after reading its instructions and confirming the intended role.
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
- An established repository's expected identity evidence is missing, or the
  intended role remains genuinely ambiguous after reading instructions →
  stop, report found versus expected, and ask one clarification. A fresh
  product repository may legitimately lack commits, a remote, application
  files and source-library landmarks.
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
