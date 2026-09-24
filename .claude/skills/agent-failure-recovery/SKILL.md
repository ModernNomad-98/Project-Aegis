---
name: agent-failure-recovery
description: MANUAL-ONLY; never auto-invoke. Recover from a broken working state — failed or interrupted runs, dirty or conflicted trees, partial or wrong commits, broken branches, blocked permissions — without losing work. Invoke explicitly when an agent session ended badly or git state looks wrong. Diagnoses read-only first, inventories ignored as well as untracked files, and verifies a rescue ref, stash or safe copy covers every valuable path before changing anything. A normal stash with -u does not include ignored files. Never run destructive cleanup (reset --hard, clean, force-push, branch -D) without a verified backup and explicit approval. Manual-only, because recovery itself mutates git state.
disable-model-invocation: true
---

# Agent Failure Recovery

## Purpose

Return a damaged working state to a known-good, verified condition while
preserving every byte of potentially valuable work. The order is fixed:
diagnose (read-only) → preserve → recover → verify → report. The skill treats
"clean slate" as a human decision, never an agent convenience.

## Use When

- Use when (explicitly invoked by a human): a previous run failed or was
  interrupted mid-operation (rebase/merge/cherry-pick in progress), the tree is
  unexpectedly dirty or conflicted, a commit captured the wrong files, a branch
  is broken or mis-based, or a permission block left an operation half done.
- Do NOT use when: tests fail for code reasons — that is debugging, not state
  recovery.
- Do NOT use when: the tree is dirty because of expected in-progress work.
- Never auto-invoked: recovery mutates git state, so a human must consciously
  start it (`disable-model-invocation: true`).

## Inputs to Inspect

All read-only, before ANY mutation:

1. `git status` (full, including untracked), current branch, `git branch -vv`.
2. In-progress operation markers: `.git/MERGE_HEAD`, `.git/rebase-merge/`,
   `.git/rebase-apply/`, `.git/CHERRY_PICK_HEAD`.
3. `git stash list`, `git log --oneline -10`, `git reflog -15`.
4. Untracked **and ignored** files that exist only in the working tree.
   Inspect `git status --ignored` and identify valuable generated artifacts;
   neither class is recoverable from Git history unless separately saved.
5. What the failed run was TRYING to do (task context, partial outputs).

## Workflow

1. **Diagnose read-only.** Collect the full picture from Inputs to Inspect.
   Classify the failure: failed-tests-mid-change | dirty/conflicted tree |
   interrupted operation | partial/wrong commit | broken branch | blocked
   permission.
2. **Preserve before touching.** Create a rescue ref — `git branch
   rescue/<date>-<context>` at HEAD — and/or `git stash push -u -m "<context>"`
   for tracked and non-ignored untracked work. The `-u` option does **not**
   preserve ignored files. Copy valuable ignored or other non-Git artifacts
   to a safe scratch location, verify the copies against their sources, and
   record every ref, stash and path created before any recovery mutation.
3. **Recover minimally**, using the matching playbook in
   [references/recovery-playbooks.md](references/recovery-playbooks.md).
   Prefer additive, reversible operations (new branch, `stash apply`,
   `git restore --staged`, `rebase --abort` / `--continue`) over history surgery.
4. **Verify.** `git status` matches the intended end state; build/tests run if
   the state claims to be working; the preserved refs still exist.
5. **Report** using the Output Format — including exactly where the preserved
   work lives.

## Output Format

```
RECOVERY REPORT
Found:      <failure classification + evidence>
Preserved:  <rescue branch / stash ref / scratch paths — exact names>
Actions:    <ordered list of commands run>
State now:  <branch, cleanliness, verification result>
Follow-ups: <e.g., secret rotation, force-push decision awaiting approval>
```

## Validation Checklist

- [ ] No mutating command ran before the preservation step completed.
- [ ] Untracked and ignored files inventoried; each valuable path preserved
      by the appropriate stash or verified copy, or explicitly marked absent.
- [ ] Every destructive command either avoided, or run only with a verified
      backup ref AND fresh explicit approval.
- [ ] Recovered state verified, not assumed (status + build/tests where
      applicable).
- [ ] Report names the exact rescue refs so the human can find the preserved
      work later.

## Gotchas

- The reflog is a recovery source, not a safety net: untracked and ignored
  files never enter it. A normal `stash -u` also omits ignored files. Inventory
  and verify their safe copies before relying on a clean working tree.
- `git checkout -- <path>` and `git restore <path>` silently discard
  working-tree edits — they belong to the destructive set even though they
  look mild.
- `git stash pop` onto a dirty or conflicted tree can create a second-order
  mess; prefer `git stash apply` (keeps the stash) until the result is verified.
- A wrong commit containing a secret is two incidents: state recovery AND
  credential exposure. Flag rotation as a follow-up — and treat it as urgent if
  the commit was pushed.
- Blocked-permission failures leave half-written files that LOOK committed;
  diff before trusting the tree.

## Stop Conditions

The destructive set — each item requires a verified backup ref AND fresh,
explicit, per-command human approval:

- `git reset --hard`
- `git checkout -- <path>` / `git restore <path>` (working-tree discard)
- `git clean -f` / `-fd`
- `git push --force` (any variant, including `--force-with-lease`)
- `git branch -D`, `git stash drop`, `git stash clear`
- any history rewrite of commits that were already pushed

Also stop when: the failure involves possibly-pushed secrets (rotation is a
human decision); two recovery paths would each lose different work (the human
picks); or the diagnosis cannot confidently classify the state.

## Supporting Files

- [references/recovery-playbooks.md](references/recovery-playbooks.md) —
  per-failure-mode playbooks (diagnose → preserve → recover → verify).
- `evals/evals.json` — behavior cases, including the never-auto-invoke rule.
- Manual-only invocation prevents trigger overlap, so no trigger-evals file.
