# Brief — OPT1-PR1 "Record the owner's Option 1 decision" (first PR of the OPT1 program)

Owner: Peter Nguyen. Repository: /home/user/Project-Aegis (Role A, source library). Base: origin/main 7d1d05e8 (re-verify).
Designated branch: claude/sharp-lovelace-urgxpz. Its PR #677 is already MERGED (squash), so this is a fresh change: restart
the branch from latest origin/main (`git checkout -B claude/sharp-lovelace-urgxpz origin/main`). DISCLOSURE: the
coordinator's shell accidentally already ran exactly that command at 2026-10-07T21:13:28Z (unquoted heredoc). Effect: local
branch reset to origin/main 7d1d05e8 and its upstream set to origin/main; remote branch untouched at ccf3fc22 (only
already-merged content). UPDATE 21:14:16Z: coordinator restored the local branch to origin/claude/sharp-lovelace-urgxpz
(ccf3fc22, upstream = that remote branch), i.e. the pre-accident state; the implementer performs the restart itself. Re-verify, set the push upstream to origin/claude/sharp-lovelace-urgxpz, and push with
--force-with-lease (permitted: the remote branch holds only already-merged history). Coordinator: parent session (does not author/commit/merge).

## Binding rules
Same rules as /tmp/claude-0/-home-user-Project-Aegis/0168d1d5-9af4-5a74-a8dd-9a35339e53ab/scratchpad/rcf/BRIEF-COMMON.md items 1–7 (read it), with these differences: this item MAY edit
docs/approvals/APPROVAL_REGISTER.md and the decision log, because recording the owner's decision there is its purpose.
Never edit .github/, scripts/, tools/ or skills in this PR. No reserved-scope content. The tool repair and the switch are
LATER PRs — out of scope here.

## Owner decisions to record (verbatim sources; all direct chat in this session, 2026-10-07)
1. "ok go with your recommendation" — Option 1: the acceptance index becomes the official readability pending count, gated:
   no switch until the repaired tool passes independent review; no blocking CI gate (informational-only CI job at most,
   later); one source of truth after the switch (the ledger stops publishing its own count and cites the index).
2. AskUserQuestion answers (labels chosen verbatim):
   - pages with no recorded acceptance in the (repaired) index -> "Count as pending (Recommended)".
     NOTE coordinator correction disclosed to owner: the question said "never had a review recorded"; the 159 are pages the
     UNREPAIRED tool could not match. The rule applies to the repaired index's records, not today's 159.
   - regeneration trigger -> "On demand + keeper (Recommended)".
   - merges of the OPT1 program PRs (decision record, tool repair, switch) -> "Yes, same terms (Recommended)".
   - repair path -> "B: structured table (Recommended)": the ledger keeper records each acceptance as one row in a
     fixed-format table INSIDE the ledger (page, full 40-char commit, file blob ID); the index reads only that table, after a
     one-time reviewed backfill whose rows must quote verifiable ledger/evidence text. AEGIS-APR-101 unchanged (it fixes no format).
   - post-switch routine rebuild PRs -> "Yes, standing approval (Recommended)": standing grant for index-rebuild PRs only,
     same terms (all stages passed, all checks green, admin merge allowed, fix and retry), revocable.
3. Coordinator defaults the owner was told of and did not object to: edits of <=10 changed lines and no new section keep a
   page accepted (ledger's existing written rule); lost/undecidable acceptance records count as pending; rebuilds are done by
   a delivery-stage coding agent, never the coordinator or the read-only reviewer agents; rebuild only from a full clone with
   PR heads fetched (never shallow).
Merge authority for THIS PR = decision 2 "same terms" (verbatim instruction texts are in /tmp/claude-0/-home-user-Project-Aegis/0168d1d5-9af4-5a74-a8dd-9a35339e53ab/scratchpad/rcf/BRIEF-COMMON.md, owner merge
and failure-handling instructions; their scope now extended by the "Yes, same terms" answer to the OPT1 program PRs).

## Inputs
Audit + verification: /tmp/claude-0/-home-user-Project-Aegis/0168d1d5-9af4-5a74-a8dd-9a35339e53ab/scratchpad/opt1-audit/ (BRIEF.md, L1–L4 reports, VERIFY.md — the reconciled condition set lives in VERIFY.md).
