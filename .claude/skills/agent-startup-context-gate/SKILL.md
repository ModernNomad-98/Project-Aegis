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


## Startup authority and effective Git identity

Startup identity and hook inspection is READ-ONLY: inspect the current Git identity,
effective author/committer values and hook state without mutating configuration or
installing/replacing hooks. Configure the agent identity or install/replace a local
hook only when an actual applicable authority covers that exact action; otherwise
report the missing setup and stop. Do not copy the repository owner identity from
existing commits, and do not invent a new approval when a valid grant already covers
the action.

Run and record the inspection. It reports missing setup and the effective hook path
without mutating configuration or hook files:

```bash
MISSING=0
AGENT_NAME=$(git config --get user.name 2>/dev/null || true)
AGENT_EMAIL=$(git config --get user.email 2>/dev/null || true)
LOCAL_NAME=$(git config --local --get user.name 2>/dev/null || true)
LOCAL_EMAIL=$(git config --local --get user.email 2>/dev/null || true)
EXPLICIT=0
[ -n "$LOCAL_NAME" ] && [ -n "$LOCAL_EMAIL" ] && EXPLICIT=1
[ -n "${GIT_AUTHOR_NAME:-}" ] && [ -n "${GIT_AUTHOR_EMAIL:-}" ] && [ -n "${GIT_COMMITTER_NAME:-}" ] && [ -n "${GIT_COMMITTER_EMAIL:-}" ] && EXPLICIT=1
if [ "$EXPLICIT" -eq 0 ]; then echo "STARTUP: identity source not explicit (local config or env required)"; MISSING=1; fi
[ -n "$AGENT_NAME" ] || echo "STARTUP: configured agent user.name absent; effective identity used"
[ -n "$AGENT_EMAIL" ] || echo "STARTUP: configured agent user.email absent; effective identity used"
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
case "$AUTHOR_NAME" in *"|"*) echo "STARTUP: effective author name has extra separators"; MISSING=1 ;; esac
case "$AUTHOR_EMAIL" in *"|"*) echo "STARTUP: effective author email has extra separators"; MISSING=1 ;; esac
if [ -z "$AUTHOR_NAME" ] || [ -z "$AUTHOR_EMAIL" ] || [ -z "$COMMITTER_NAME" ] || [ -z "$COMMITTER_EMAIL" ]; then echo "STARTUP: effective author/committer identity empty or malformed"; MISSING=1; fi
if [ -n "$OWNER_NAME" ] || [ -n "$OWNER_EMAIL" ]; then
  if { [ -n "$AGENT_NAME" ] && [ "$AGENT_NAME" = "$OWNER_NAME" ]; } || { [ -n "$AGENT_EMAIL" ] && [ "$AGENT_EMAIL" = "$OWNER_EMAIL" ]; } || [ "$AUTHOR_NAME" = "$OWNER_NAME" ] || [ "$AUTHOR_EMAIL" = "$OWNER_EMAIL" ] || [ "$COMMITTER_NAME" = "$OWNER_NAME" ] || [ "$COMMITTER_EMAIL" = "$OWNER_EMAIL" ]; then
    echo "STARTUP: effective author/committer identity matches the recorded owner identity"; MISSING=1
  fi
fi
HOOKS_PATH=$(git config --get core.hooksPath 2>/dev/null || true)
if [ -n "$HOOKS_PATH" ]; then
  case "$HOOKS_PATH" in
    /*) HOOK_BASE="$HOOKS_PATH" ;;
    "~/"*) HOOK_BASE="${HOME%/}/${HOOKS_PATH#~/}" ;;
    *) HOOK_BASE="$(git rev-parse --show-toplevel 2>/dev/null || pwd)/$HOOKS_PATH" ;;
  esac
else
  HOOK_BASE=$(git rev-parse --git-path hooks 2>/dev/null || true)
fi
if [ -n "$HOOK_BASE" ]; then
  HOOK_PATH="${HOOK_BASE%/}/pre-commit"
  echo "STARTUP: effective hook path=$HOOK_PATH"
  if [ ! -f "$HOOK_PATH" ] || [ ! -x "$HOOK_PATH" ]; then echo "STARTUP: hook missing or not executable at effective path"; MISSING=1; fi
else
  echo "STARTUP: effective hook path unavailable"; MISSING=1
fi
[ "$MISSING" -eq 0 ] || exit 1
echo "STARTUP: effective author/committer identity available and distinct from the recorded owner"
```

Supported model: Linux with POSIX sh/coreutils. Windows and non-Linux POSIX lock/readiness scenarios are explicit SKIP/UNRUN, never PASS.

Identity policy: the effective `git var` identity is authoritative; configured values are also checked when present and must not be the owner. A command-level `git -c user.name=...` override intentionally changes the configured view (and is accepted only when the resulting effective identity is non-owner); the actual commit remains the oracle. Minimum Git: 2.20 (git var/config behavior); command-level `-c` visibility in hooks depends on Git exporting GIT_CONFIG_PARAMETERS/GIT_CONFIG_COUNT, so set those explicitly on older Git; the effective `git var` check remains authoritative.

Effective author AND committer identities matter, not only the configured defaults:
environment (`GIT_AUTHOR_*`, `GIT_COMMITTER_*`) can change the identity that is
recorded. A command override such as `git commit --author` can also change the
recorded author, but Git applies `--author` after the pre-commit hook, so the local
hook cannot reliably catch it. The resulting ACTUAL commit is the final oracle:
inspect `%an <%ae>` and `%cn <%ce>` on the resulting commit. If either effective
identity is missing, empty or still the recorded owner identity, do not push; amend
or recreate the local commit before push, or STOP and report the mismatch. A pre-commit
hook may have exited 0 because `--author` was applied after it, so the actual-commit
inspection is mandatory.

The owner identity is recorded by an explicitly authorized setup action below, not
by the read-only startup inspection; perform it only when an applicable authority
covers the action. It comes from local-only config (never committed):

```bash
# AUTHORIZED SETUP (not read-only inspection): record the repository owner identity
# only under the applicable authority.
git config --local aegis.ownerName "<owner name>"
git config --local aegis.ownerEmail "<owner email>"
```

The complete executable pre-commit hook below reads the recorded owner identity and
validates the EFFECTIVE author and committer through `git var GIT_AUTHOR_IDENT` /
`git var GIT_COMMITTER_IDENT`. It exits nonzero for missing owner identity, missing/
invalid effective identity, or effective owner identity in either position. Install at
the EFFECTIVE hook path reported by inspection (resolved through `core.hooksPath` /
`git rev-parse --git-path hooks/pre-commit`; normally `.git/hooks/pre-commit` only when
`core.hooksPath` is unset), executable, never committed. Hook-file presence is not authenticity: inspect the file contents/owner/expected hash before trusting it:

```sh
#!/bin/sh
set -u
OWNER_NAME=$(git config --local --get aegis.ownerName || true)
OWNER_EMAIL=$(git config --local --get aegis.ownerEmail || true)
if [ -z "$OWNER_NAME" ] || [ -z "$OWNER_EMAIL" ]; then
  echo "STOP: recorded owner identity missing; set git config --local aegis.ownerName and aegis.ownerEmail" >&2
  exit 1
fi
LOCAL_NAME=$(git config --local --get user.name || true)
LOCAL_EMAIL=$(git config --local --get user.email || true)
EXPLICIT=0
[ -n "$LOCAL_NAME" ] && [ -n "$LOCAL_EMAIL" ] && EXPLICIT=1
[ -n "${GIT_AUTHOR_NAME:-}" ] && [ -n "${GIT_AUTHOR_EMAIL:-}" ] && [ -n "${GIT_COMMITTER_NAME:-}" ] && [ -n "${GIT_COMMITTER_EMAIL:-}" ] && EXPLICIT=1
if [ "$EXPLICIT" -eq 0 ]; then echo "STOP: identity source not explicit (local config or env required)" >&2; exit 1; fi
CONFIG_NAME=$(git config --get user.name || true)
CONFIG_EMAIL=$(git config --get user.email || true)
if { [ -n "$CONFIG_NAME" ] && [ "$CONFIG_NAME" = "$OWNER_NAME" ]; } || { [ -n "$CONFIG_EMAIL" ] && [ "$CONFIG_EMAIL" = "$OWNER_EMAIL" ]; }; then
  echo "Refusing commit: configured Git identity is the repository owner identity" >&2
  exit 1
fi
AUTHOR_IDENT=$(git var GIT_AUTHOR_IDENT) || { echo "STOP: effective Git author identity unavailable" >&2; exit 1; }
COMMITTER_IDENT=$(git var GIT_COMMITTER_IDENT) || { echo "STOP: effective Git committer identity unavailable" >&2; exit 1; }
AUTHOR_NAME=$(printf "%s\n" "$AUTHOR_IDENT" | sed -n "s/^\(.*\) <\([^>]*\)>.*$/\1/p")
AUTHOR_EMAIL=$(printf "%s\n" "$AUTHOR_IDENT" | sed -n "s/^\(.*\) <\([^>]*\)>.*$/\2/p")
COMMITTER_NAME=$(printf "%s\n" "$COMMITTER_IDENT" | sed -n "s/^\(.*\) <\([^>]*\)>.*$/\1/p")
COMMITTER_EMAIL=$(printf "%s\n" "$COMMITTER_IDENT" | sed -n "s/^\(.*\) <\([^>]*\)>.*$/\2/p")
if [ -z "$AUTHOR_NAME" ] || [ -z "$AUTHOR_EMAIL" ] || [ -z "$COMMITTER_NAME" ] || [ -z "$COMMITTER_EMAIL" ]; then
  echo "STOP: effective Git author/committer identity is missing, empty or malformed" >&2
  exit 1
fi
if [ "$AUTHOR_NAME" = "$OWNER_NAME" ] || [ "$AUTHOR_EMAIL" = "$OWNER_EMAIL" ] || [ "$COMMITTER_NAME" = "$OWNER_NAME" ] || [ "$COMMITTER_EMAIL" = "$OWNER_EMAIL" ]; then
  echo "Refusing commit: effective Git author/committer identity is the repository owner identity" >&2
  exit 1
fi
exit 0
```

Expected behavior: valid agent author+committer -> exit 0 and the commit proceeds;
missing owner/effective identity or effective owner identity in EITHER author or
committer position -> exit 1 with the exact STOP/refusal message; environment overrides
are validated against the effective identity. A command override such as
`git commit --author` is **not reliably caught** by a pre-commit hook because Git
applies it after the hook. A pre-commit hook cannot remediate this; after inspecting
the ACTUAL resulting commit, amend/recreate it with a valid identity before push, or
stop and report. Invoke the hook directly to prove the unit behavior, then inspect the
actual commit as the oracle. Local hooks are not a
security boundary: `git commit --no-verify` can bypass a local pre-commit hook, and no
global hook, host setting, remote identity service or unbypassable guarantee is
promised. This is a local guard and disclosure boundary only.

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
- Configured Git identity equals the recorded owner identity, or owner/agent identity is
  missing → STOP before committing; report the mismatch and ask the human to fix it,
  never commit as the owner (see Git Identity Gate and the pre-commit hook).

## Supporting Files

- [references/context-source-checklist.md](references/context-source-checklist.md) —
  identity-signal table and reading precedence, per repo type.
- `evals/evals.json` — trigger + behavior cases, including the
  exists-but-wrong-repo halt.
- `evals/trigger-evals.json` — discrimination against `source-of-truth-reconciler`
  and the change-governance gates.
