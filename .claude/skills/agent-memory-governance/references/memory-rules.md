# Memory Governance — rule sets, entry format, live checks

Canonical semantics: the merge-base and content-proof rules covered by R8-CONV-3 are resolved by
[canonical semantics](../../../../docs/semantics/canonical-semantics.md); that file is authoritative for conflicts and this reference cites the covered ID.

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

## Canonical memory merge-base/content checks (R8-CONV-3)

Canonical check invocation (no new repo file): the canonical wrapper is the complete fenced POSIX script in docs/semantics/canonical-semantics.md section 3; extract that block verbatim into a temporary file and execute it as TARGET_PATH=<repo-relative path> BASE=<sha> HEAD=<sha> sh /tmp/canonical-wrapper.sh (the block is executable as-is; there is no placeholder body). It emits ancestry_status/content_match_status/oid_match_status and exit codes: 0 = completed/defined (NOT passed), 2 = empty TARGET_PATH UNVERIFIED, 3 = any UNVERIFIED. Merge-base rc0=ancestor_or_equal, rc1=not_ancestor, rc>=2=UNVERIFIED; content diff rc0=same, rc1=differs, rc>=2=UNVERIFIED with GIT_LITERAL_PATHSPECS=1 and --no-textconv --no-ext-diff; blob-OID equal=same, different=differs, absent/error=UNVERIFIED. A gate passes only when ancestry_status=ancestor_or_equal AND content_match_status=same AND oid_match_status=same; raw git diff exit 0 is only same, and wrapper exit 0 is completed-only, never a pass. Exit 2 empty TARGET_PATH and exit 3 other UNVERIFIED block the gate; any differs/UNVERIFIED blocks; never infer pass from exit 0 alone. Reachability is not content proof; record command, rc and stdout statuses; missing/empty TARGET_PATH is UNVERIFIED, never no.

### Legacy boolean shortcut - forbidden

A boolean shortcut is **forbidden** (it must not be used and must not be reintroduced), including any mapping of Git rc>=2/error 128 to `no`/exit 0 or any direct `|| echo no` fallback around an ancestry/content command. A Git error is **UNVERIFIED**, which blocks the gate; it is never `no` and never a pass. Route ancestry + content + OID checks through the canonical wrapper above, keep the three statuses distinct (`ancestor_or_equal` / `not_ancestor` / `UNVERIFIED`; `same` / `differs` / `UNVERIFIED`), and treat wrapper exit 0 as completed-only. This reference contains no executable duplicate shortcut; the normative rule is the prohibition, not a claim that historical code was deleted.

## TRUST rules (before acting on memory)

Memory is a lead, not truth. Before any action premised on remembered state:

| Remembered claim | Verify with |
|---|---|
| PR open / merged / identity ("#11 is the docs PR") | `gh pr view <n> --json state,title,mergedAt,headRefName` |
| Branch exists / current branch | `git branch -a`, `git branch --show-current` |
| What merged to main / repo baseline | `git log --oneline -20 origin/main`, validator output |
| File / flag / command still exists | direct check before recommending it |
| Completion anchor ("X complete, PR #n, SHA") | A completion claim is verified by: (a) the claimed artifacts present in the current tree; (b) ANCHOR_SHA reachable from origin/main containing them: `git merge-base --is-ancestor ANCHOR_SHA origin/main`; (c) if a commit on origin/main reverts the anchor change set the claim fails unless the revert was itself reverted - inspect `git show --stat REVERT_SHA` and `git merge-base --is-ancestor REVERT_SHA origin/main`, name REVERT_SHA and RE_REVERT_SHA when present, check `git merge-base --is-ancestor REVERT_SHA RE_REVERT_SHA` AND `git merge-base --is-ancestor RE_REVERT_SHA origin/main` (a local/unmerged re-revert cannot pass), inspect the full content proofs `git show REVERT_SHA`, `git show RE_REVERT_SHA` and `git diff REVERT_SHA RE_REVERT_SHA` (show --stat alone is not proof) and record all outputs; (d) each cited migration id shown as applied by the migration tool read-only status (`migrate status` or equivalent) and recorded; (e) when a PR is cited, `gh pr view <n> --json state,mergeCommit` shows merged and its mergeCommit is reachable from origin/main (`git merge-base --is-ancestor <mergeCommit> origin/main`). Use SHA-based checks, never names; run `git fetch origin` first, then record ANCHOR_SHA/REVERT_SHA/RE_REVERT_SHA plus the canonical wrapper's exit status and its three emitted statuses as evidence. Run the canonical wrapper from [Canonical memory merge-base/content checks (R8-CONV-3)](#canonical-memory-merge-basecontent-checks-r8-conv-3) for the ancestry, content and blob-OID checks: it prints `ancestry_status`, `content_match_status` and `oid_match_status`; its exit 0 means completed (never passed), exit 2 (empty TARGET_PATH) and exit 3 (any UNVERIFIED) block, and a Git error is UNVERIFIED - never `no`, never a pass. The completion claim is verified only when `ancestry_status=ancestor_or_equal` AND `content_match_status=same` AND `oid_match_status=same` and the evidence in (a)-(e) above is recorded; a defined difference or an UNVERIFIED status blocks, and neither is a pass. Editing memory files stops for approval. |
| Auto-merge / protection posture | `gh pr view <n> --json autoMergeRequest`, repo settings |

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
