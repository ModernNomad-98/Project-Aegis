# Brief — FU-1 "Follow-ups after PR #678" (one PR, two parts, built by a team of agents)

Owner: Peter Nguyen. Repository: /home/user/Project-Aegis (Role A, source library). Base: origin/main c060a7cb (re-verify;
PR #678 merged at 2026-10-08T01:29:19Z). Designated branch: claude/sharp-lovelace-urgxpz (its last PR #678 is MERGED,
so restart it from latest origin/main with `git checkout --no-track -B claude/sharp-lovelace-urgxpz origin/main` and push
with --force-with-lease against the current remote value — the remote holds only already-merged history).
Coordinator: parent session (does not author/commit/merge).

## Owner request (verbatim, direct chat in this session, 2026-10-08)
The owner selected these two items from the coordinator's list:
> "* Small dated corrections for the four minor points the reviewers left open. One small docs PR would cover them.
> * Adding the six tagged-field markers to the PR template. That file is protected, so it needs your owner exception. It would stop the description fix rounds that happened on both PRs."
and then: "use multiple agents".
CORRECTION by coordinator (verified 2026-10-08T14:06Z): `.github/pull_request_template.md` is NOT gate-guard protected —
the gate_pattern in .github/workflows/validate-skills.yml:528 does not match it, and scripts/tests/test_offline_ci.py:298
lists it explicitly as a near-miss that must NOT match. No owner exception is needed. It IS inside `.github/`, which
CONTRIBUTING.md:238 lists as a security-relevant surface (security review applies to OUTSIDE contributions only).

## Binding rules
Same as …/scratchpad/rcf/BRIEF-COMMON.md items 1–7 (read it). Forward-dated notes only; merged dated text and register
entries are never rewritten (register lifecycle events are appended, per its preamble). No reserved-scope work (paused
evaluation/VM/Stage 4B/BER calibration). The OPT1 program stays paused: nothing here resumes, repairs or switches it.
Never write the Codex trigger phrase (the word codex prefixed with @) in any file, comment or PR text unless the
coordinator's brief explicitly asks you to request a review.

## Part A — dated corrections (the four minor points left open on PR #678)
Sources: …/scratchpad/opt1-pr1/IMPL-AUDIT-3.md (m-1, m-2, n-1) and …/scratchpad/opt1-pr1/FINAL-REVIEW-1.md (F-1, F-2,
n-a, n-b) and the merge receipt …/scratchpad/opt1-pr1/MERGE-RECEIPT.md. The four the coordinator reported to the owner:
 1. D73 row 2 item (e) rejection rule should say it applies per event kind (lost-commit and withdrawal rows) — m-1.
 2. The "targeted-review row may be withdrawn?" Open item is missing from D73's / APR-113's "not decided" lists — m-2.
 3. The ledger note leaves preservation of the side-branch-only commit e6fc8d24 implicit (still open under D73 row 8) — F-2.
 4. PR #678's skills table lacks rows for the round-3 D/E agents and Stage F — F-1 (the merge receipt points to them).
Decide per item the correct forward vehicle (a dated note in the decision log / ledger / open-decisions, an appended
register lifecycle note only if the register's own rules allow it, or "no repo change needed — already recorded in the
merge receipt"), and say why. Include the nits n-1/n-a/n-b only if cheap and correct.

## Part B — bound-field sentinels in the PR template
Add the six whole-line sentinels that docs/delivery-workflow.md "The bound fields" defines (witness, skills, security
pairs) to .github/pull_request_template.md, placed so a PR author who fills the template gets parseable bound fields.
Model the placement on merged PR bodies #676/#677/#678 (read via GitHub MCP tools). Check every rule/test that reads the
template (scripts/tests/test_offline_ci.py, docs/delivery-workflow.md, CONTRIBUTING.md, readability rules) and whether
delivery-workflow.md or CONTRIBUTING.md should gain a one-line pointer.

## Merge authority
NOT yet granted for this PR (earlier grants were scoped to PR #677 and the OPT1 program). The coordinator is asking the
owner; agents must not assume it.

Scratch folder: /tmp/claude-0/-home-user-Project-Aegis/0168d1d5-9af4-5a74-a8dd-9a35339e53ab/scratchpad/fu1/

## Owner answers (recorded by coordinator 2026-10-08T14:09:13Z; AskUserQuestion in this session, labels verbatim)
- Q: "Which backlog item should the team take next? ..." -> "Stale CI docs (Recommended)" — option text: "Since PR #676,
  docs/offline-ci.md still says PRs have no path filter and to wait for all five jobs, and the PR template still asks for
  the Windows jobs to be checked. Docs PRs now skip those jobs. About 0.5–1 hour; folded into the current PR as Part C."
- Q: "May the team merge this follow-up PR (dated corrections, PR template markers, plus whatever you pick above) on the
  same terms as before: every stage passed, all checks green, admin merge allowed, fix and retry on failure?" ->
  "Yes, same terms (Recommended)". This is the merge authority for FU-1 (replaces the "NOT yet granted" note above).

## Part C — stale CI docs since PR #676 (owner-selected)
Verified at origin/main c060a7cb: docs/offline-ci.md:12-15 ("wait for all five jobs") and :28 ("Pull requests have no
path filter"); .github/pull_request_template.md:33-34 ("both Ubuntu and Windows verification jobs checked"). Since #676
the advisory jobs are path-scoped and skip on docs-only PRs. Correct these to match .github/workflows/validate-skills.yml
(read its `changes` job and its jobs' `if:` conditions) and the flake policy #676 documented. Part C's template edit overlaps Part
B's file: the Part B planner owns all template edits and must include Part C's template line; the Part A/C planner owns
docs/offline-ci.md. offline-ci.md: check whether it is dated-snapshot text (forward note) or living how-to text (edit in
place), per its own conventions.

## Coordination with FU-2 (parallel PR on branch claude/sharp-lovelace-urgxpz-fu2, owner-approved)
FU-2 (audit baseline refresh + library-diff-reviewer description) adds a register GRANT. FU-1 must NOT add register
entries: if a Part A item would need one, choose another forward vehicle or flag it to the coordinator.
Neither PR touches docs/roadmaps/aegis-backlog-forecast.md unless the plan proves it necessary (flag it).
