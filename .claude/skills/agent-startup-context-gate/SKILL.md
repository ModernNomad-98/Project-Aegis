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
   four source-package landmarks named in `AGENTS.md` — a `README.md` whose
   top identifies the repository as `# Project Aegis`, `docs/skills-catalog.md`,
   `scripts/validate-skills.py`, and the
   `artifacts/audits/skill-contract-audit-baseline.json` baseline — copied
   startup files alone do not establish source-library role. Classify as
   consumer/product when task and local evidence support it; otherwise ask one
   role question. A fresh Stage 0 (nothing started yet) product repository can
   have zero commits, no remote, no application files and no
   `docs/project-state.md`. Use the task-named current workspace
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


## Git Identity Gate (before the first commit)

**Status: REQUIRED behavior; not automatically enforced.** Run this gate before
the first commit of a work session, and re-run it after any repository/config/
environment change or before any commit whose identity source or mode may have
changed. The gate has two mandatory parts: (1) the presence/owner check below,
and (2) the mandatory manual provenance step below. This repository includes
illustrative optional example snippets (including the hook example), but they
are NOT installed or activated and provide no automatic enforcement. The
attempted explicit-source enforcement implementation was withdrawn after
independent review; implementation work is queued as backlog item **DS-R1b**.
The gate is REQUIRED behavior, not optional, and is not a security boundary,
verified identity, or unbypassable control. No automatic-enforcement,
complete-enforcement, verified-identity, readiness or CI-green claim is made.

Effective-identity policy (single source of truth): the identity reported by
`git var GIT_AUTHOR_IDENT` / `git var GIT_COMMITTER_IDENT` is authoritative. A valid
non-owner author AND committer exit 0 regardless of whether that identity comes from
local config, global config, explicit environment (GIT_AUTHOR_* / GIT_COMMITTER_*),
`GIT_CONFIG_COUNT`/GIT_CONFIG_KEY_* or a command-level `git -c`. Configured owner
values are NOT separately rejected when the effective identity is a valid non-owner
(the actual commit remains the oracle). Owner-match is intentionally strict: matching
the owner on EITHER the name OR the email is treated as owner; an agent sharing
only the owner name or only the owner email must change that field. A missing/empty
effective identity, or an
effective owner in EITHER author or committer position, exits nonzero. Inspect and
record the effective values; never copy the repository owner identity.

Record the owner identity from local-only config (never committed), and inspect the
effective author and committer without mutating configuration or hooks:

Record owner identity under the applicable authority (local-only, never committed):

```bash
git config --local aegis.ownerName "<owner name>"
git config --local aegis.ownerEmail "<owner email>"
```

Inspect effective identity; initialize MISSING before any check:

```bash
MISSING=0
OWNER_NAME=$(git config --local --get aegis.ownerName 2>/dev/null || true)
OWNER_EMAIL=$(git config --local --get aegis.ownerEmail 2>/dev/null || true)
[ -n "$OWNER_NAME" ] || { echo "STARTUP: recorded owner name missing"; MISSING=1; }
[ -n "$OWNER_EMAIL" ] || { echo "STARTUP: recorded owner email missing"; MISSING=1; }
AUTHOR_IDENT=$(git var GIT_AUTHOR_IDENT 2>/dev/null) || { echo "STARTUP: effective author identity unavailable"; MISSING=1; }
COMMITTER_IDENT=$(git var GIT_COMMITTER_IDENT 2>/dev/null) || { echo "STARTUP: effective committer identity unavailable"; MISSING=1; }
AUTHOR_NAME=$(printf "%s\n" "${AUTHOR_IDENT:-}" | sed -n "s/^\(.*\) <\([^>]*\)>.*$/\1/p")
AUTHOR_EMAIL=$(printf "%s\n" "${AUTHOR_IDENT:-}" | sed -n "s/^\(.*\) <\([^>]*\)>.*$/\2/p")
COMMITTER_NAME=$(printf "%s\n" "${COMMITTER_IDENT:-}" | sed -n "s/^\(.*\) <\([^>]*\)>.*$/\1/p")
COMMITTER_EMAIL=$(printf "%s\n" "${COMMITTER_IDENT:-}" | sed -n "s/^\(.*\) <\([^>]*\)>.*$/\2/p")
if [ -z "$AUTHOR_NAME" ] || [ -z "$AUTHOR_EMAIL" ] || [ -z "$COMMITTER_NAME" ] || [ -z "$COMMITTER_EMAIL" ]; then echo "STARTUP: effective author/committer identity missing or empty"; MISSING=1; fi
if [ "$AUTHOR_NAME" = "$OWNER_NAME" ] || [ "$AUTHOR_EMAIL" = "$OWNER_EMAIL" ] || [ "$COMMITTER_NAME" = "$OWNER_NAME" ] || [ "$COMMITTER_EMAIL" = "$OWNER_EMAIL" ]; then echo "STARTUP: effective author/committer identity matches the recorded owner"; MISSING=1; fi
[ "$MISSING" -eq 0 ] || exit 1
echo "STARTUP: presence/owner OK; mandatory manual provenance step still required (see below)"
echo "STARTUP: effective author=$AUTHOR_NAME <$AUTHOR_EMAIL> committer=$COMMITTER_NAME <$COMMITTER_EMAIL>"
```

### Mandatory manual provenance step (required; not automated)

The check above verifies only that the effective identity is present and does
not match the recorded owner. It does **not** prove that the identity has an
acceptable explicit source, and it does not implement the explicit-source
matrix. Before committing, the agent MUST perform this provenance step manually:

    git config --show-scope --show-origin --get-all user.name
    git config --show-scope --show-origin --get-all user.email
    env | grep -E '^(GIT_AUTHOR|GIT_COMMITTER)_(NAME|EMAIL|DATE)=' || true
    # Also inspect the ACTUAL commit command: a -c value used only for the check
    # does not count unless it is present on the commit itself.

Decide and record:
- ACCEPT only when the effective identity is supplied by one of: a full
  same-scope local/command config user.name+user.email pair matching the
  effective author pair or the effective committer pair; a full caller
  author+committer environment (both fields) with clean fallbacks; a single
  differing caller env override over a resolvable fallback; or a field-specific
  caller author OR committer override.
- STOP when the effective identity comes only from inherited global/system/
  auto-detected configuration or otherwise has no acceptable explicit source,
  or when a command-scope value is present only on the check command and not
  on the actual commit. Do not commit.
- Record the provenance source and the decision in the run report. A
  presence/owner check success is NOT a full gate pass; provenance is still
  required.

The illustrative hook below does NOT perform this provenance step.

The executable pre-commit hook example below automates only the presence/owner
check. It is an illustrative optional example: this repository includes it but
does NOT install or activate it, and its presence is not evidence of automatic
enforcement. If you choose to install a local hook, it reads the owner identity
from local-only config, requires a non-empty effective author AND committer from
git var, and refuses when the effective author or committer equals the recorded
owner or when that effective identity is missing or empty. It does NOT implement
the explicit-source provenance step above; strict raw/malformed validation and
provenance remain DS-R1b requirements. Installing the hook is optional; the
manual presence/owner check and the mandatory provenance step are required.
Install it at the effective hook path. Resolve core.hooksPath FIRST: a relative value resolves from the
repository top level and a leading tilde expands to HOME; use git rev-parse
--git-path hooks/pre-commit ONLY when core.hooksPath is unset. Verify the chosen path
is executable, and treat hook-file presence as presence, not authenticity (inspect
contents/owner/hash).

```sh
#!/bin/sh
# AI-R02 effective-identity hook (unique marker; exactly one block)
set -u
OWNER_NAME=$(git config --local --get aegis.ownerName || true)
OWNER_EMAIL=$(git config --local --get aegis.ownerEmail || true)
if [ -z "$OWNER_NAME" ] || [ -z "$OWNER_EMAIL" ]; then
  echo "STOP: recorded owner identity missing; set git config --local aegis.ownerName and aegis.ownerEmail" >&2
  exit 1
fi
AUTHOR_IDENT=$(git var GIT_AUTHOR_IDENT) || { echo "STOP: effective Git author identity unavailable" >&2; exit 1; }
COMMITTER_IDENT=$(git var GIT_COMMITTER_IDENT) || { echo "STOP: effective Git committer identity unavailable" >&2; exit 1; }
AUTHOR_NAME=$(printf "%s\n" "$AUTHOR_IDENT" | sed -n "s/^\(.*\) <\([^>]*\)>.*$/\1/p")
AUTHOR_EMAIL=$(printf "%s\n" "$AUTHOR_IDENT" | sed -n "s/^\(.*\) <\([^>]*\)>.*$/\2/p")
COMMITTER_NAME=$(printf "%s\n" "$COMMITTER_IDENT" | sed -n "s/^\(.*\) <\([^>]*\)>.*$/\1/p")
COMMITTER_EMAIL=$(printf "%s\n" "$COMMITTER_IDENT" | sed -n "s/^\(.*\) <\([^>]*\)>.*$/\2/p")
if [ -z "$AUTHOR_NAME" ] || [ -z "$AUTHOR_EMAIL" ] || [ -z "$COMMITTER_NAME" ] || [ -z "$COMMITTER_EMAIL" ]; then
  echo "STOP: effective Git author/committer identity is missing or empty" >&2
  exit 1
fi
if [ "$AUTHOR_NAME" = "$OWNER_NAME" ] || [ "$AUTHOR_EMAIL" = "$OWNER_EMAIL" ] || [ "$COMMITTER_NAME" = "$OWNER_NAME" ] || [ "$COMMITTER_EMAIL" = "$OWNER_EMAIL" ]; then
  echo "Refusing commit: effective Git author/committer identity is the repository owner identity" >&2
  exit 1
fi
exit 0
```

Expected behavior: any valid non-owner effective author+committer -> exit 0 and the
commit proceeds, including identities supplied only via global config, environment,
`GIT_CONFIG_COUNT` or `git -c`; missing owner/effective identity or effective owner in
EITHER position -> exit 1. A configured owner with a valid non-owner env/command
override is accepted because the effective identity is authoritative, not silently
treated as a different policy. The resulting ACTUAL commit is the final oracle; a
command `--author` is applied after the pre-commit hook, so inspect the commit and
amend/recreate before push or stop and report. Local hooks are not a security boundary:
`git commit --no-verify` bypasses them. No global hook, host setting or remote identity
service is promised.

## Shared Local Lock Before E2E/Validation

When parallel agents could share a local stack, port, database, lock directory or fixture
set, coordinate ownership before any E2E or validation run. Use the atomic lock-directory
protocol in references/shared-local-resource-coordination.md:

- Create the lock with mkdir as the single atomic primitive; never steal or delete a
  foreign, tokenless or successor lock. Existing lock with a different readable token is
  contention (exit 1, inspect and wait/escalate); an unreadable token fails closed.
- Write owner, run id, acquisition time and ttl into the lock, and release only after the
  full stored token matches this run. Traps make ONE cleanup attempt: set trap '' INT TERM
  in the handler before cleanup, reset reentrancy/stop flags on failure, and never claim
  the lock was retained or released when it was not.
- Own and stop only the direct child workload with bounded TERM then KILL waits and
  zombie reaping. Do not depend on POSIX-undefined process-group signalling or on GNU-only
  mv -T. If the child is genuinely alive after the bounded stop window, retain ownership
  and report INCOMPLETE; never report the resource free.
- Fixture cleanup removes only this run's unique mktemp directory under a literal prefix,
  rejects symlinked bases/dirs, prints the exact rm -rf command and target paths before
  removal, and reports failure. Broad delete/reset is always a stop.
- Platform honesty: Linux is the required POSIX lane (OK, required); macOS is local/UNRUN
  with no readiness claim; Windows is SKIP/UNRUN with a nonzero required skip; unsupported
  shell/tool capability is UNRUN. SKIP/UNRUN is never PASS and no all-skip success counts.

The shared-resource reference also carries the effective hook-path resolver: core.hooksPath
(relative resolved from the repository top level; tilde expanded) takes precedence, and
git rev-parse --git-path hooks/pre-commit is only the fallback when core.hooksPath is unset.

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
- [ ] Shared local resources use the mkdir lock with an owner token, a single-attempt trap release, bounded direct-child TERM/KILL, foreign/tokenless/successor preservation and a fail-closed unreadable-token path; unsupported platforms are SKIP/UNRUN, never PASS.
- [ ] Effective hook path resolves core.hooksPath first (relative/tilde handled) before the git rev-parse --git-path fallback, and hook presence is not claimed as authenticity.

## Gotchas

- **A path that exists is not the right path.** In an established-repository
  task, an empty directory with no matching project evidence is ambiguous;
  do not scaffold it. A task that names a fresh Stage 0 (nothing started yet)
  product repository with copied startup instructions is different: absent
  commits, remote and application files can be its expected state. Work in
  that current workspace after reading its instructions and confirming the
  intended role.
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
- Effective author or committer identity equals the recorded owner identity, is
  missing or empty, or the mandatory manual provenance step cannot establish an
  acceptable explicit source (full same-scope local/command config user.name+user.email
  pair matching the effective author pair or the effective committer pair; full
  caller author+committer environment, both fields, with clean fallbacks; a single
  differing caller env override over a resolvable fallback; or a field-specific
  caller author OR committer override) → STOP before committing. This includes
  inherited global/system/auto-detected-only identities and command-scope values
  present only on the check command, not the actual commit; report the mismatch and
  ask the human to fix it, never commit as the owner (see Git Identity Gate and its
  reference matrix). A presence/owner check success is not a full gate pass; strict
  raw/malformed validation remains a DS-R1b requirement.

## Supporting Files

- references/shared-local-resource-coordination.md - exclusive local-resource lock, owner token, bounded child stop, fixture cleanup and effective hook-path resolution.
- [references/context-source-checklist.md](references/context-source-checklist.md) —
  identity-signal table and reading precedence, per repo type.
- `evals/evals.json` — trigger + behavior cases, including the
  exists-but-wrong-repo halt.
- `evals/trigger-evals.json` — discrimination against `source-of-truth-reconciler`
  and the change-governance gates.
