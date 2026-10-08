# Brief — FU-2 "Audit baseline refresh + library-diff-reviewer description alignment"

Owner: Peter Nguyen. Repository: /home/user/Project-Aegis (Role A). Base: origin/main c060a7cb (re-verify).
A separate PR (FU-1: dated corrections, PR template markers, stale CI docs) is being planned in parallel by other agents
and will use branch claude/sharp-lovelace-urgxpz first; FU-2 delivery branch is decided by the coordinator later. Do not
touch FU-1's files: docs/reconciliation/step-0-reconciliation-v4.md, docs/roadmaps/aegis-documentation-readability-backlog.md,
docs/roadmaps/aegis-open-decisions-2026-09-23.md, docs/offline-ci.md, .github/pull_request_template.md (if you must,
say so — the coordinator sequences it).
Coordinator: parent session (does not author/commit/merge).

## Owner request (verbatim, direct chat in this session, 2026-10-08)
> "also work on these:
> Skill contract-audit baseline refresh (186 skills / 316 findings frozen vs 339 today)
> Aligning library-diff-reviewer's description with its "skill-library PR" wording"
(The two lines are the coordinator's own descriptions, which the owner copied. The owner's instruction is to do the work;
the figures are the coordinator's unverified-at-this-turn claims — re-derive them.)

## Binding rules
Same as …/scratchpad/rcf/BRIEF-COMMON.md items 1–7 (read it). Register entries are append-only; record any new owner
grant as a NEW entry quoting the owner verbatim from this brief. No reserved-scope work. Never write the Codex trigger
phrase (the word codex prefixed with @). Read AEGIS-APR-065/066 (and any later baseline-regeneration entries, e.g.
APR-073, APR-079) for the precedent: they named an exact engine version, an exact path allow-list and one PR, and APR-066
says "Any further regeneration needs a new grant". The library-diff-reviewer item is listed in
docs/roadmaps/aegis-backlog-forecast.md:360 as "it changes routing, so it waits for the owner" — the owner has now asked.

Scratch folder: /tmp/claude-0/-home-user-Project-Aegis/0168d1d5-9af4-5a74-a8dd-9a35339e53ab/scratchpad/fu2/
2026-10-08T14:13:30Z

## Owner answers (AskUserQuestion, labels verbatim)
- Q: "How should the two new items (audit baseline refresh, library-diff-reviewer wording) ship? They're separate from
  FU-1, and my session is set up to push to one branch." -> "Second branch, in parallel" — option text: "You allow one
  extra branch so FU-2 is built and reviewed alongside FU-1. Faster, but two PRs are open at once."
  => FU-2 branch: claude/sharp-lovelace-urgxpz-fu2 (created from origin/main by the FU-2 implementer).
- Q: "May FU-2 merge on the same terms (every stage passed, all checks green, admin merge allowed, fix and retry)? Your
  request to do the baseline refresh will also be recorded as a new approval register grant, quoted word for word,
  because the register says any further regeneration needs a new grant." -> "Yes, same terms (Recommended)".

## Coordination with FU-1 (parallel PR)
- Register: FU-2 adds the new baseline GRANT (and later its consumption). FU-1 must NOT add register entries; if FU-1
  needs one, the coordinator sequences it. Whichever PR merges second re-checks the next free AEGIS-APR ID at merge time.
- The forecast (docs/roadmaps/aegis-backlog-forecast.md) is touched by neither unless a plan proves it necessary; if both
  need it, the coordinator sequences them.
recorded 2026-10-08T14:15:33Z

## Coordinator decisions (2026-10-08, after Stage A plans)
- Part E: option E1 (one-line fix in .claude/skills/library-diff-reviewer/evals/trigger-evals.json:3). The owner's
  request repeated an item already delivered by PR #542; E1 finishes the residual wording. The other skill's eval line is
  NOT edited (it would change a paused BER case ID).
- Part D: register entry variant A (Part D only; Part E needs no grant). Order inside the PR: E1 commit first, then D.
- Part D merge method: prefer a merge commit (preserves the scanned commit S on main's history, as #432/#441/#461/#503
  did); the merge agent verifies the repository allows it and otherwise records the provenance consequence.
- Grant consumption: recorded by a later register-only PR after merge, per precedent (APR-066/084).
- Skipped path-filtered CI jobs: recorded as skipped, not green, as on #677/#678.
