# Common brief — work item RCF-1 "Readability pending-count reconciliation"

Owner: Peter Nguyen. Owner selected this item on 2026-10-07 (current-turn instruction, chat).
Repository: /home/user/Project-Aegis (Project Aegis SOURCE LIBRARY, Role A — the four landmarks are present).
Base: origin/main = 03c93c77a05e89d082f93c91b23dffabb332373c. Working branch: claude/sharp-lovelace-urgxpz (currently == main).
Coordinator: the parent Claude session. The coordinator does not author, edit, commit, push or merge.

## Binding rules for every agent in this item
1. Read /home/user/Project-Aegis/AGENTS.md, CLAUDE.md and docs/delivery-workflow.md first. Follow them. In Role A you must
   identify and read the matching Aegis skill under .claude/skills/ before doing your stage, and name it in your report
   (dogfood rule). MANUAL-ONLY skills are never used unless the owner names them.
2. "Audit your own state": every factual claim carries the command + observed output, or is labelled "unverified".
   Count with commands. Never fabricate. "unknown / not derivable" is an acceptable answer.
3. Separation of duty: you perform ONLY your assigned stage. Do not perform another stage's work.
4. NO push, NO PR creation, NO merge, NO GitHub writes, NO issue comments. Local work only unless your stage brief says otherwise.
5. Reserved scope — read-only context at most, never modify or execute: anything about the paused Aegis evaluation /
   rehearsal package / VirtualBox / VMs / ISO / Stage 4B / issue #101 execution / BER calibration / provider spend /
   execution flags. Do not change the evaluation's recorded source pin [evaluation-source-pin]. Protected paths and gate-guard rules in
   CONTRIBUTING.md and .github/ apply; do not edit .github/ or the approval register (docs/approvals/) unless the plan
   explicitly justifies it AND the audit accepts it — default is: don't.
6. The ledger's rule: dated text is corrected forward by a dated note, never rewritten. Respect AEGIS-APR-101 (ledger keeper
   role: keeper must be a different agent from the page author and accepting reviewer; coordinator may not hold it).
   This item must NOT accept any page or grant any acceptance; it reconciles the COUNT and its premises only.
7. Report at the end: skill(s) used, what you did, what you did not do, evidence, open questions, start/finish timestamps
   (`date -u`), measured wall time.

## The problem (coordinator's observation, re-verify it yourself)
- docs/roadmaps/aegis-documentation-readability-backlog.md "Start here — current reading" states 16 pending pages
  (656 tracked; later 657 after PR #577), dated snapshots.
- A "Premises correction — appended 2026-10-03, measured at c3527560" section in that ledger corrects three premises,
  including that the canonical acceptance index exists (tools/readability_acceptance/).
- Running `python3 -I tools/readability_acceptance/check_index.py` at 03c93c77 reports: reader_pages_in_index 602,
  provably_pending 212, no_recorded_acceptance 159, recorded_acceptance_within_10_lines 224, cannot_decide 7
  (unreachable acceptance revisions — this clone is SHALLOW, 50 commits; `git fetch --unshallow origin` is permitted and
  may resolve some of them), exact_pending_count "NOT DERIVABLE from this procedure".
- The docs/roadmaps/aegis-backlog-forecast.md also quotes readability figures (16 pending etc.).
So the repository's stated pending count (16) and its own instrument's lower bound (>=212) disagree. Goal: make the
repository's current-state statements truthful and consistent with the instrument, by forward-dated notes, without
accepting pages, rewriting dated snapshots, or claiming an exact number the procedure says is not derivable.

Scratch folder for artifacts: /tmp/claude-0/-home-user-Project-Aegis/0168d1d5-9af4-5a74-a8dd-9a35339e53ab/scratchpad/rcf/

## Owner merge instruction (verbatim, recorded by coordinator at 2026-10-07T17:36:13Z)
Source: owner Peter Nguyen, direct chat message in this Claude Code session, 2026-10-07:
> "I approve for you to merge once all checks are green. Including admin merge"
Scope as read by the coordinator: RCF-1's pull request only; merge only after every required stage (plan audit,
implementation audit, validate, final independent PR review) is affirmative at the exact head, and ALL checks on that
head are green (not only branch-protection-required ones). Admin merge is permitted under that condition. It grants
nothing else (no deploy, no reserved-scope work, no register edits). The merge is performed by a separate merge agent
that re-derives every gate itself; it is not performed by the author, any reviewer, or the coordinator.

## Owner failure-handling instruction (verbatim, recorded 2026-10-07T17:37:14Z)
> "if a check fails, diagnose and fix the issue and try to merge again. Do not stop until it is merged"
Coordinator reading: a failing check is diagnosed (ci-failure-classifier) and fixed by an implementer agent, then the fix
goes back through implementation audit, validate and final review at the new head before any merge attempt. It never
authorizes skipping/disabling tests, waiving a failed check, bypassing a required review, or touching reserved scope.
