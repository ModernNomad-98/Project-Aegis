# Memory Governance — rule sets, entry format, live checks

Follow the owning [Agent Memory Governance skill](../SKILL.md) and its
manual-only boundary. A pull request (PR) proposes a repository change;
personally identifiable information (PII) can identify a person. This page
is a review aid: memory changes require the human approval described by
the owning skill.

## WRITE rules (what may enter memory)

1. Confirmed durable facts only. Test: "can a single routine command make this
   false tomorrow?" If yes (PR state, branch tips, CI status, who is on-call),
   it is a snapshot — record the decision/lesson instead, or nothing.
2. Provenance mandatory: when written, based on what evidence.
3. Absolute dates only. Convert "yesterday"/"last Tuesday" at write time.
4. One fact per entry; entries link related entries rather than bundling.
5. Never: secrets, credentials, tokens, connection strings, PII. No
   exceptions clause — "just the staging password" is still a credential in a
   plaintext file that outlives the session.
6. Not what the repo records: code structure, git history, merged content.
   Store the pointer (`see docs/reconciliation/step-0-...md §3`), not a copy
   that will drift.
7. Update only when a confirmed fact CHANGES. Corrections replace the stale
   text and note the change (`was X until 2026-07-06, now Y per <evidence>`);
   never append a contradiction beneath the old claim.
8. Completion-baseline anchors are the durable form of "done". Pin finished
   work as `<work> is complete; do not treat as pending — PR #<n> merged,
   <merge SHA>, migration <id> applied, <YYYY-MM-DD>` so later sessions do
   not re-open or redo it; the merge SHA (Secure Hash Algorithm) is the hash
   that identifies the merge commit. Merged and applied are immutable, unlike
   "PR #10 is open"; an anchor without that evidence fails WRITE 1 and 2. An
   anchor is still a lead: its TRUST check runs before it stops any work.

## TRUST rules (before acting on memory)

Memory is a lead, not truth. Before any action premised on remembered state:

| Remembered claim | Verify with |
|---|---|
| PR open / merged / identity ("#11 is the docs PR") | `gh pr view <n> --json state,title,mergedAt,headRefName` |
| Branch exists / current branch | `git branch -a`, `git branch --show-current` |
| What merged to main / repo baseline | `git log --oneline -20 origin/main`, validator output |
| File / flag / command still exists | direct check before recommending it |
| Completion anchor ("X complete, PR #n, SHA") | See the completion-anchor verification list below the table. |
| Auto-merge / protection posture | `gh pr view <n> --json autoMergeRequest`, repo settings |

**Completion-anchor verification (every check preserved):**
- (a) Claimed artifacts present in the current tree (direct check).
- (b) ANCHOR_SHA reachable from origin/main and containing the claimed artifacts: `git merge-base --is-ancestor ANCHOR_SHA origin/main` (it emits NO output: exit 0 = yes, exit 1 = no, any other/non-zero = UNVERIFIED; record the echoed result), plus a content check such as `git ls-tree -r --name-only ANCHOR_SHA -- <paths>` or `git show ANCHOR_SHA:<path>`; command errors mean UNVERIFIED, not "no".
- (c) If a commit on origin/main reverts the anchor change set, the claim fails unless the revert was itself reverted: name ANCHOR_SHA, REVERT_SHA and RE_REVERT_SHA; check `git merge-base --is-ancestor REVERT_SHA RE_REVERT_SHA` AND `git merge-base --is-ancestor RE_REVERT_SHA origin/main`; inspect full content proofs with `git show REVERT_SHA`, `git show RE_REVERT_SHA` and `git diff REVERT_SHA RE_REVERT_SHA`, and record the outputs.
- (d) Each cited migration id shown as applied by the migration tool read-only status (`migrate status` or equivalent) and recorded.
- (e) When a PR is cited, `gh pr view <n> --json state,mergeCommit` shows merged and its mergeCommit is reachable from origin/main (`git merge-base --is-ancestor <mergeCommit> origin/main`).
- Fetch `origin` first; use SHA-based checks, never names; record ANCHOR_SHA/REVERT_SHA/RE_REVERT_SHA and the exact command output as evidence; editing memory files stops for approval.

On divergence: live state wins, act on it, queue the memory correction. If the
divergence changes what the CURRENT task should do, route that conflict to
`source-of-truth-reconciler` (memory sits at the bottom of its precedence
order); only the memory fix returns here.

## HYGIENE classifications and dispositions

| Classification | Meaning | Default disposition |
|---|---|---|
| verified-current | live check confirms it | keep |
| stale | true when written; reality moved | correct (replace, with change provenance) |
| wrong-when-written | never true | correct or delete, with reason |
| duplicate | same fact elsewhere | merge-into the canonical entry |
| forbidden-content | secret/credential/PII | delete + **URGENT rotation recommendation** |
| unverifiable | no provenance, no way to check | delete or mark suspect — never silently trust |

All dispositions are proposed, human-approved, then applied exactly; the index
is updated and re-verified against the files afterwards.

## Case study — the stale-memory incident

Two sessions ran in parallel against one repo. Session A read memory: "PR #10
is open and needs merging" — true when written, but a colleague had already
merged it; A attempted a re-merge. Session B read memory describing PR #11's
purpose — the numbering had shifted as PRs opened and closed, and B pushed
work against the wrong PR. Neither entry was a lie; both were snapshots of
in-flight state trusted after they expired.

The rules this incident wrote: in-flight state does not enter memory (WRITE 1);
remembered PR state is verified with `gh` before any action (TRUST); and
parallel sessions assume memory is stale between write and read — the cost of
one `gh pr view` is always smaller than the cost of acting on a dead snapshot.
