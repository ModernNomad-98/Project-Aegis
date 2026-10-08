# Brief — CIFIX-1 "Fix the Errno 39 race in scripts/tests/test_offline_ci.py" (third PR, all seven stages)

Owner: Peter Nguyen. Repository: /home/user/Project-Aegis (Role A, source library). Base: origin/main (re-verify; c060a7cb
at brief time, but FU-1 #680 or FU-2 #679 may merge first). Branch: claude/sharp-lovelace-urgxpz-ci-fix (new; create from
latest origin/main). Coordinator: parent session (does not author/commit/merge).

## Owner instruction (verbatim, AskUserQuestion answer in this session, 2026-10-08)
Chosen label: "Yes, one-time exception (Recommended)". Option text, verbatim:
"A third PR touching only that test file, on a third branch, through all seven stages. It merges once gate-guard's red is
covered by your one-time exception for that exact commit, recorded in the register, with every other check green. Admin
merge allowed."
Earlier standing failure-handling texts (verbatim, rcf/BRIEF-COMMON.md): "I approve for you to merge once all checks are
green. Including admin merge" / "if a check fails, diagnose and fix the issue and try to merge again. Do not stop until it is merged".

## Binding rules
Same as …/scratchpad/rcf/BRIEF-COMMON.md items 1–7 (read it), except: this PR edits ONLY scripts/tests/test_offline_ci.py
(a gate-guard PROTECTED path; gate-guard will be red by design). The one-time exception must be recorded in
docs/approvals/APPROVAL_REGISTER.md bound to the EXACT head commit. The planner must decide, from the register's preamble
and precedents (e.g. AEGIS-APR-047 and other gate-guard exceptions; grep the register), HOW the exception is recorded
given that the exact head is only known after the fix commit exists — e.g. a register entry in a separate register-only
PR, or whatever the register's own rules and precedent require — WITHOUT adding a second file to this PR unless the
precedent requires it and the owner text allows it ("touching only that test file" — treat it as binding; flag any
conflict to the coordinator instead of resolving it yourself).
Register ID coordination: FU-2 (#679, open) adds AEGIS-APR-119. Take the next free ID at the time of writing (re-check at
merge). Never write the Codex trigger phrase. No reserved-scope work. Never skip/disable/quarantine a test.

## Inputs
Diagnosis: …/scratchpad/ci-diag/DIAGNOSIS.md (root cause: Git 2.55 detached geometric auto-maintenance `git repack`
races TemporaryDirectory cleanup in run_guard; runs 36695924676 and 37713171379). Proposed fix: …/ci-diag/proposed-fix.diff
(disable maintenance.auto and gc.auto in the fixture repo after `git init`). The planner must independently verify the
diagnosis and whether the fix covers every git call path in the test (fetch in the guard, other fixtures in the file).

Merge terms: as quoted above. Merge agent must confirm gate-guard is the ONLY non-green check, that it is red solely for
the protected-path reason, and that the recorded exception names that exact head.
Recorded by coordinator at 2026-10-08T15:28:53Z (date -u).

## Owner answers to plan open questions Q2/Q3/Q4 (AskUserQuestion in this session, 2026-10-08; labels chosen verbatim)
- Q2 "The exception has to name the fix PR's exact commit, which only exists once the fix is written. The last one-time
  exception (AEGIS-APR-106) handled this with a separate small PR that changes only the approval register, merged just
  before the protected PR. That's a fourth PR your instruction didn't name. May the team open and merge it on the same
  terms (all seven stages, all checks green, admin merge allowed)?" -> "Yes, same terms (Recommended)" — option text:
  "Follows the precedent. The fix PR stays one file, and the exception is in the register, approved and pinned to the
  exact commit, before the fix merges. About 30–45 extra minutes."
- Q3 (consumption record) -> "Batch it later (Recommended)" — option text: "Recorded in the next register PR, which will
  also record FU-2's grant as used up. One PR instead of two, with no loss of safety, since a one-time exception for an
  exact commit can't be reused anyway."
- Q4 (fix head moves after the exception is recorded) -> "Ask me again (Recommended)" — option text: "Matches the
  AEGIS-APR-032→034 precedent. Each exception stays tied to a commit you approved. Costs a short wait for your answer if
  it happens, which is unlikely because the fix is small."
Coordinator procedural positions (not owner decisions): Q1 skipped path-scoped jobs recorded as skipped (as #677/#678);
Q5 keep the regression test; Q6 #679 merges first.
Recorded by coordinator at 2026-10-08T16:01:16Z (date -u).

## Answers to Stage B RC6 / RC3 (coordinator, from the session transcript's own AskUserQuestion call)
The question the owner answered with "Yes, one-time exception (Recommended)", verbatim (header "CI test fix"):
"main's CI failure was a rare race in one CI test: Git 2.55 starts a background clean-up job in a throwaway test folder, and the test deletes the folder while that job is still writing. The one re-run passed, so main is green again, and the same race has happened once before (2026-09-30). The proposed fix adds two lines to scripts/tests/test_offline_ci.py telling Git not to run that background job in the test's folder. scripts/ is protected, so a fix PR's protected-file guard (gate-guard) will be red until you grant a one-time exception for that exact PR commit. Do you want the fix?"
The chosen option's text, on ONE line exactly as the owner saw it (the brief above only wraps it):
"A third PR touching only that test file, on a third branch, through all seven stages. It merges once gate-guard's red is covered by your one-time exception for that exact commit, recorded in the register, with every other check green. Admin merge allowed."
Other options offered (not chosen): "Yes, but ask me before merging" — "Same PR. It waits for you to look at the exact commit before the exception is used."; "Not now, backlog it" — "Leave it as a known intermittent failure (about 1 in 750 runs by the diagnosis) and record it as a backlog item."
RC3 reading: coordinator reads "recorded in the register" as "merged on main" (the register on the default branch is the authority per AGENTS.md). Coordinator is telling the owner of this reading.
Recorded by coordinator at 2026-10-08T16:10:40Z (date -u).

## OQ-A answer (coordinator)
The exact one-line question texts and option texts of Q2/Q3/Q4, as the owner saw them, are in
$S/cifix/owner-q2-q4-verbatim.json (extracted programmatically from the session transcript's own AskUserQuestion call;
sha256 74c8cd5a559b1398fe411d6d75f4da1be23fe788b0845cdb59dcfb09bc82f1c2). JSON strings = the exact text; the wrapped
versions above are line-wrapped copies of the same text.
## OQ-B (coordinator)
The coordinator has told the owner that the fix head adds about 28 lines (the 2 config lines, a comment, an import and a
regression test), not just 2. The owner's chosen option scopes by FILE ("touching only that test file"); the entry
states the real size.
Recorded by coordinator at 2026-10-08T16:20:07Z (date -u).

## Owner instruction (verbatim, direct chat in this session, 2026-10-08) — binds every recommendation
"always audit and scrutinize your recommendations. Do not make any assumptions on your recommendation, if you are unsure, look for evidence or research it first."
Coordinator application: every recommendation (batch choice, overlap verdict, estimate, MANUAL-ONLY call, procedure
choice) must carry its evidence (file:line, command output, PR/commit) or be researched until it does; anything still
unproven is labelled "unverified" and is NOT used as a basis for the recommendation. Each recommendation section ends
with a self-scrutiny note: the strongest counter-argument and what evidence would change it. The coordinator's own
earlier expectation that the batch "lean towards QA Tier 2 or Phase 3" was an unverified guess and carries no weight.
Recorded by coordinator at 2026-10-08T17:10:06Z (date -u).

## OQ-C closed: owner answer (AskUserQuestion, this session, 2026-10-08; verbatim)
Q: "For the CI test fix, your answer says the exception must be \"recorded in the register\". I read that as: the register entry has to be merged on main (not just written in an open PR) before the fix can merge. Is that right?"
-> "Yes, merged on main (Recommended)" — option text: "The safest reading. The register on main is what the repo treats as authority, so the exception only counts once that small register PR has merged."
OQ-B status: the coordinator told the owner at ~16:20Z that the fix adds about 28 lines incl. a regression test; the owner
did not object. This is a disclosure, NOT owner approval of the size; the owner's option scopes by file.
Recorded by coordinator at 2026-10-08T17:52:07Z (date -u).
