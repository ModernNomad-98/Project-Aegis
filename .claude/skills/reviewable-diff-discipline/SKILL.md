---
name: reviewable-diff-discipline
description: Keep a change small, scoped, and reviewable while implementing it — one intent per branch or PR, no drive-by edits, no opportunistic refactors, no generated noise or secrets staged. Stages only the intended files by explicit path and verifies the staged set matches the declared intent before commit. Use when implementing any code change, preparing a commit or PR, or when a working diff has grown beyond its stated purpose.
---

# Reviewable Diff Discipline

## Purpose

Produce diffs a human can actually review: every hunk traceable to the stated
intent, every staged file expected, nothing smuggled. The discipline runs
DURING implementation, not only at the end, so scope drift is caught when it
starts — and the final `git diff --cached` equals the intent, no more, no less.

## Use When

- Use when: implementing any change that will become a commit or PR.
- Use when: preparing to stage or commit work, or writing the PR description.
- Use when: the working diff has visibly outgrown the stated task.
- Do NOT use when: reviewing someone else's diff for bugs — that is code review.
- Do NOT use when: deciding a change's risk class or validation — that is
  `change-classification-gate`.
- Do NOT use when: writing the final task report — that is
  `ai-closeout-reporter` (this skill's parked items feed it).

## Inputs to Inspect

1. The declared intent and scope contract (from `change-classification-gate`
   when one exists).
2. `git status` and `git diff` — the full working-tree state, before staging.
3. `.gitignore` and repo conventions for generated artifacts.
4. The expected file set for the intent.

## Workflow

1. **Declare intent + expected file set before editing** — one sentence plus a
   file list.
2. **While editing, touch only files the intent requires.** On discovering an
   unrelated problem, record it for the closeout or a separate task — do not
   fix it inline.
3. **Before staging, self-review `git diff` against the intent, hunk by hunk.**
   Park anything out of scope (labeled stash or a noted follow-up) — never
   silently discard work, and never silently keep it either.
4. **Stage by explicit path:** `git add <file> <file>` — never `git add .`,
   `-A`, or `-u` from a tree containing anything beyond the task.
5. **Verify staged == intended:** `git diff --cached --stat` must match the
   declared file set; investigate any surprise before continuing.
6. **Scan the staged diff** for secrets/credentials, `.env` files, generated
   bundles, lockfile churn unrelated to the intent, editor/backup files, and
   leftover debug output.
7. **Write the commit/PR description:** the intent in one sentence, a rationale
   for any file a reviewer would not expect, and a note listing parked
   out-of-scope items.

## Output Format

- A staged change where `git diff --cached --stat` equals the declared file set.
- A commit/PR description containing: intent (one sentence); file-by-file
  rationale for anything surprising; and a "parked / out of scope" note listing
  what was deliberately NOT included and where it lives (stash label, follow-up
  task).

## Validation Checklist

- [ ] Every hunk in `git diff --cached` traces to the stated intent.
- [ ] Staged file set equals the declared file set — verified via `--stat`,
      not memory.
- [ ] No secrets, env files, generated artifacts, or debug leftovers staged.
- [ ] Unrelated discoveries recorded, not fixed inline.
- [ ] Formatting-only churn absent, or isolated into its own commit.
- [ ] Parked items are listed somewhere a human will see (PR note / closeout).

## Gotchas

- `git add .` in a dirty tree is how unrelated edits, junk files, and secrets
  ship. Explicit paths are non-negotiable whenever the tree holds anything
  beyond the task.
- Auto-formatters can rewrite whole files on save, drowning the real change —
  scope formatter output to edited regions or commit it separately.
- "While I'm here" refactors double review cost and hide the actual fix.
- Lockfile changes with no dependency change in the intent are a red flag —
  investigate, don't stage.
- Parked work is easy to lose: every parked item must resurface in the PR note
  or the closeout report, with its stash label or follow-up reference.

## Stop Conditions

- A secret, credential, or `.env` file appears in the staged set → halt,
  unstage it, and confirm handling with the human (its presence may itself be
  an incident).
- The intent genuinely requires many more files than declared → stop; return to
  `change-classification-gate` and re-contract the scope.
- Keeping the diff clean would require discarding (not parking) someone's work
  → confirm with the human before deleting anything.

## Supporting Files

- `evals/evals.json` — trigger + behavior cases.
- `evals/trigger-evals.json` — discrimination within the change-governance
  cluster (`change-classification-gate`, `human-approval-boundary`).
- Self-contained otherwise.
