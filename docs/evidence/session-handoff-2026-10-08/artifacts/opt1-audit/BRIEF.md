# Common brief — OPT1-AUDIT: "Would Option 1 slow development or break a process?"

Owner: Peter Nguyen. Request (verbatim, 2026-10-07): "please audit the entire repository, there are a lot of workflows,
rules, skills, and dependencies. I want to make sure your recommendation does not slow down development or break a process"

Repository: /home/user/Project-Aegis — Project Aegis SOURCE LIBRARY (Role A). Checkout is detached at origin/main
7d1d05e8170254ae60e8deb175c74e244a284a80 (full history available). READ-ONLY audit.

## The recommendation under audit ("Option 1, with conditions")
Today the repository's count of documentation pages "pending" readability review is stated by hand in the ledger
`docs/roadmaps/aegis-documentation-readability-backlog.md` (~3,950 lines). A script-based acceptance index exists at
`tools/readability_acceptance/` (build_index.py builds acceptance-index.json by harvesting the ledger + evidence records;
check_index.py applies the ">10 changed lines or new section returns a page to pending" rule). PR #677 (merged today)
recorded that the index over-counts by >=6 because of four harvester blind spots (wrapped sentences, table cells,
unresolved short names/`../` links, ledger-keeper rows carrying no verdict word).
Option 1 = once the harvester is repaired and independently reviewed, the INDEX becomes the official pending count,
under these conditions:
  C1 the index reads ledger-keeper rows; C2 the ledger keeper (AEGIS-APR-101) keeps recording in the ledger, unchanged;
  C3 a named role regenerates the index (build_index.py --write) through the normal delivery stages;
  C4 acceptance commits the index depends on are preserved (e.g. tagged) — some are only reachable from side branches,
     two are already lost (65bacc7, d3dcb62);
  C5 no switch until an independent review passes the repaired tool.
Possible later extension the coordinator mentioned: run the index check in CI to flag drift.
Option 2 = ledger stays official; index advisory.

## Rules for every audit agent
1. Read AGENTS.md, CLAUDE.md, docs/delivery-workflow.md first. Role A dogfood rule: identify and read the matching Aegis
   skill(s) under .claude/skills/ for your work, apply them, and name them in your report. Never use a MANUAL-ONLY skill.
2. READ-ONLY. No file edits in the repo, no commits, pushes, PRs, comments, GitHub writes, `--write` runs, branch changes,
   or dependency installs. Write only inside the scratch folder below. You may run read-only commands and the repo's
   read-only scripts/tests (use a scratch TMPDIR; use `python -B` to avoid __pycache__).
3. Evidence over assumption: every finding cites file:line or a command + observed output, or is labelled "unverified".
   Count with commands. "unknown" is acceptable; fabrication is not.
4. Reserved scope — never touch or run: the paused Aegis evaluation / rehearsal / VirtualBox / VM / ISO / Stage 4B /
   issue #101 execution / BER calibration / provider spend. Reading docs that mention them is fine.
5. Judge both directions: list what Option 1 would BREAK or SLOW, and what it would FIX or SPEED UP, and what Option 2
   costs. Rate each finding: BREAKS (a process stops working), SLOWS (measurable added time/steps), RISK (could break
   under a plausible condition), NEUTRAL, or HELPS. Say which condition (C1–C5) mitigates it, or propose a new condition.
6. Report: skills used, findings table, evidence, what you did not check, start/finish timestamps (`date -u`).

Scratch folder: /tmp/claude-0/-home-user-Project-Aegis/0168d1d5-9af4-5a74-a8dd-9a35339e53ab/scratchpad/opt1-audit/

## Owner decisions (recorded by coordinator 2026-10-07T20:51:30Z; source: owner Peter Nguyen, direct chat in this session, 2026-10-07)
- After hearing the recommendation (Option 1, gated; no CI gate; repair first; one source of truth) the owner wrote verbatim:
  > "ok go with your recommendation"
- Answers to the coordinator's three follow-up questions (AskUserQuestion, verbatim option labels chosen):
  Q "159 pages have never had a review recorded... how should they be treated?" -> "Count as pending (Recommended)"
  Q "When should the index be regenerated?" -> "On demand + keeper (Recommended)" (rebuild after the ledger keeper records an
    acceptance, or when someone needs a fresh official count)
  Q "May the team merge these PRs on the same terms (every stage passed and all checks green, admin merge allowed, fix and
    retry on failure)?" -> "Yes, same terms (Recommended)" — scope: the OPT1 program PRs (decision record, tool repair, switch).
