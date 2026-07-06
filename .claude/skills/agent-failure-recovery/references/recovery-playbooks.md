# Recovery Playbooks

Supporting detail for `agent-failure-recovery`. Every playbook assumes the
skill's fixed order: diagnose (read-only) → preserve → recover → verify.
Preservation (rescue branch / `stash push -u` / scratch copies) has already
happened before any playbook's "recover" steps run.

## 1. Failed tests mid-change

- Diagnose: which tests, since when (`git stash` the change and re-run to see
  if main is green — using `stash push -u -m`, which is also the preservation).
- Recover: this is usually a DEBUGGING problem, not state recovery. If the
  change must be parked: leave it on a labeled stash or WIP branch, restore a
  clean base, and hand off to debugging with the failure output.
- Verify: base branch builds and its tests pass.

## 2. Dirty or conflicted tree

- Diagnose: `git status` — distinguish merge/rebase conflict markers from
  plain uncommitted edits; check operation markers in `.git/`.
- Recover (conflict): resolve file-by-file only if the original operation's
  intent is known; otherwise `--abort` the operation (rebase/merge) — additive
  and safe because the pre-state is preserved.
- Recover (plain dirt): nothing may need recovery — confirm with the human
  whether the edits are wanted work before doing anything at all.
- Verify: status clean or intentionally-dirty; no leftover conflict markers
  (`grep -r '<<<<<<<' --include=*` on changed files).

## 3. Interrupted operation (rebase / merge / cherry-pick in progress)

- Diagnose: `.git/rebase-merge/`, `.git/rebase-apply/`, `MERGE_HEAD`,
  `CHERRY_PICK_HEAD`; `git status` names the operation and the stopped commit.
- Recover: two clean exits only — `--continue` after resolving what stopped
  it, or `--abort` to return to the pre-operation state. Never delete `.git/`
  operation directories by hand.
- Verify: operation markers gone; log shows the expected shape; tree state
  matches the chosen exit.

## 4. Partial or wrong commit (not yet pushed)

- Diagnose: `git show --stat HEAD` — what got in that shouldn't have, or what
  was missed.
- Recover (extra files): `git reset --soft HEAD~1` (keeps everything staged),
  then unstage the wrong files with `git restore --staged <path>` and recommit
  the intended set. `--soft` loses nothing; it only moves the branch pointer.
- Recover (missed files): a follow-up commit is usually better than amending;
  amend only if the commit is definitely unshared.
- Secret in the commit: recover the state, then flag credential rotation as a
  follow-up — urgent if there is any chance it was pushed or mirrored.
- Verify: `git show --stat HEAD` now matches the intent; nothing from the
  working tree disappeared.

## 5. Broken or mis-based branch

- Diagnose: `git log --oneline --graph`, `git branch -vv`, merge-base with the
  intended base.
- Recover: build the CORRECT branch fresh from the right base and
  cherry-pick/apply the intended commits onto it. Leave the broken branch in
  place as its own backup; do not delete or force-rewrite it.
- Verify: new branch contains exactly the intended commits (diff against the
  rescue ref); old branch untouched.

## 6. Blocked permission mid-operation

- Diagnose: what was the operation, how far did it get (half-written files,
  partial staging)? `git status` + diff every touched path.
- Recover: complete or cleanly undo the half-done step ONLY after the human
  re-grants or declines the permission — do not route around a permission
  block; it may have been the point.
- Verify: no half-written files remain; state is either fully pre-op or fully
  post-op, never between.

## Command risk quick-reference

| Safe (additive/reversible) | Destructive (backup + explicit approval) |
| --- | --- |
| `git branch rescue/<x>` | `git reset --hard` |
| `git stash push -u -m` | `git checkout -- <path>` / `git restore <path>` |
| `git stash apply` | `git clean -f` / `-fd` |
| `git reset --soft` | `git push --force[-with-lease]` |
| `git restore --staged <path>` | `git branch -D` / `git stash drop|clear` |
| `rebase/merge --abort` | rewriting pushed history |
