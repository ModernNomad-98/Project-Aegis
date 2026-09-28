# Session checkpoint — 2026-09-28 evening

> **Why this page exists:** This page records the end of the 2026-09-28
> session so that a new session can resume from it when the owner, Peter
> Nguyen, says "continue". It follows the
> [morning checkpoint for the same day](session-checkpoint-2026-09-28.md),
> which PR #485 added. It records state only. It grants no implementation,
> host or provider authority. Verify every fact below against the live
> repository before acting on it.

Terms used here: a pull request (PR) is a proposed change on GitHub. A commit
hash (SHA) identifies one exact commit. An approval-register entry (APR)
records a scoped owner decision in the
[approval register](../approvals/APPROVAL_REGISTER.md). A decision number such
as D68 is an entry in the
[reconciliation log](../reconciliation/step-0-reconciliation-v4.md).
Continuous integration (CI) is the automated check run on each PR; GitHub
Actions runs it. `gate-guard` is the CI check that fails when a PR changes a
protected path, such as the workflow files or the validator. Codex is the
automated GitHub code reviewer. Quality assurance (QA) Tier 1 is the first
batch of testing skills from the roadmap. The AI-SDLC batch covers skills for
the artificial intelligence (AI)-assisted software development lifecycle
(SDLC). The "tools test suites" are the Python tests under
`tools/aegis_setup/tests` and `tools/aegis_delivery_control/tests`. The
code-health audit of 2026-09-28 numbered its findings by priority: P1 is
high, P2 is medium. A manual-only skill runs only when the user names it.
LF is the Unix line ending; `umask` is the Unix setting that decides the
default permissions of new files.

## Where things stand

| Item | Value at recording |
| --- | --- |
| Recorded at | 2026-09-28 22:30 Coordinated Universal Time (UTC) |
| `main` head | `76b399b11e8068ca26171dbd6d715f161757f35e` (merge of PR #496) |
| Shipped skills | 187: PR #499 added `acceptance-criteria-reviewer` |
| Skill-contract audit | 316 findings, 232 of them informational ROUTE-002 routing notes; report format from audit engine v1.13.4 (PR #503), findings unchanged |
| Open PRs | Six: #498, #500, #502, #505, #507 and #508. See [Open PRs at recording](#open-prs-at-recording). |

All times and dates are UTC.

## Merged since the morning checkpoint

The merge commit is the `main` commit that each PR created. Sixteen PRs merged
after #485, listed below in merge order (from
`git log --first-parent`). PR #487, which recorded the morning's later owner
decisions, merged just before #485 and is not repeated here. Of the numbers
#486 to #506, the four not listed (#498, #500, #502 and #505) are still open.

| PR | Merge commit | What it did |
| --- | --- | --- |
| [#486](https://github.com/ModernNomad-98/Project-Aegis/pull/486) | `2a411fd47cd2c9edbdb3092674367bb41d9e1183` | Spelled out "artificial intelligence (AI)" at first use in the body of each page |
| [#488](https://github.com/ModernNomad-98/Project-Aegis/pull/488) | `ebf210c63cfb0428434b3d7be967d17775c808ab` | Marked manual-only handoffs and defined terms in `ai-evaluation-harness` |
| [#489](https://github.com/ModernNomad-98/Project-Aegis/pull/489) | `80d9dfe71decf6aa6772bf48577395b8b4453f1f` | Repointed a renamed leakage-checks link in the reference evidence |
| [#491](https://github.com/ModernNomad-98/Project-Aegis/pull/491) | `5f581a3b0f213fc327308c8bb399e23f321856db` | Recorded the audit engine v1.13.4 report-format grant as APR-079 |
| [#492](https://github.com/ModernNomad-98/Project-Aegis/pull/492) | `e0f1d244d4dd2fa71505e6fedd05a65b5adf4a01` | Proposed the scope of the QA Tier 1 skill batch (merged at head `930493c5`) |
| [#501](https://github.com/ModernNomad-98/Project-Aegis/pull/501) | `c17a567185d4c7f75036c444d07ee6990905317d` | Stopped new modules from shadowing imports in the gate checks (the first P1 finding); merged at head `9ca82d53` under a one-time `gate-guard` exception |
| [#493](https://github.com/ModernNomad-98/Project-Aegis/pull/493) | `051770035105162a27d588fb46292afdb90b6d5e` | Recorded D68, the owner's QA Tier 1 build decision |
| [#490](https://github.com/ModernNomad-98/Project-Aegis/pull/490) | `cc4da2cd3a9a2672404d480f0877a06ad20dbe90` | Recorded #475 to #488 and the net-difference rule in the readability ledger |
| [#497](https://github.com/ModernNomad-98/Project-Aegis/pull/497) | `654ca2d1495773cad08d1ccefb657458c43577d1` | Catch-up backlog forecast checkpoint after #491 |
| [#494](https://github.com/ModernNomad-98/Project-Aegis/pull/494) | `4ee21152297c1943ae3ad7c3522b9f24ddd507a8` | Proposed the scope of the AI-SDLC skill batch |
| [#495](https://github.com/ModernNomad-98/Project-Aegis/pull/495) | `e77403ccc3199d1a99d17acb2d6e222f1c633d8a` | Proposed the scope of the Phase 7 AI engineering skill batch |
| [#506](https://github.com/ModernNomad-98/Project-Aegis/pull/506) | `862d07c749525f092672880c713ca4b68d596037` | Made the delivery-control test fixtures private to their owner under any `umask` |
| [#504](https://github.com/ModernNomad-98/Project-Aegis/pull/504) | `6fe634ecc129b0d6d7731c6ad78435344b2c4e34` | Added a root `.gitattributes` that forces LF line endings (code-health finding P2-7) |
| [#503](https://github.com/ModernNomad-98/Project-Aegis/pull/503) | `c14338d254bde3fd7fb9b8060033299cde5d5197` | Extended the audit report key (engine v1.13.4, APR-079); merged under a one-time `gate-guard` exception |
| [#499](https://github.com/ModernNomad-98/Project-Aegis/pull/499) | `f0c4b24294514e12790e559a98806d3d9b56b28e` | Added the `acceptance-criteria-reviewer` skill under D68 (186 to 187) |
| [#496](https://github.com/ModernNomad-98/Project-Aegis/pull/496) | `76b399b11e8068ca26171dbd6d715f161757f35e` | Proposed the scope of the Phase 6 reliability skill batch |

## Owner decisions made on 2026-09-28 after the morning checkpoint

The owner made these decisions in chat by choosing an option from the
coordinator's multiple-choice questions. The quoted text is his exact answer.
Only D68 has its own permanent record so far (PR #493); the others live in
chat and in the PR descriptions named below.

| Topic | Exact chat answer | Where it stands |
| --- | --- | --- |
| Build the QA Tier 1 skill batch as proposed in PR #492 | "Build it as recommended (Recommended)" | Recorded as D68 (#493). Delivers three new skills and one extension (186 to 189). `acceptance-criteria-reviewer` merged (#499); the other three are open as #498, #500 and #502. |
| Commit, push and open the PR for audit engine v1.13.4 | "Commit, push, open PR (Recommended)" | Merged as #503 |
| The tools test suites never ran in CI (finding P2-1) | "Fix and add to CI (Recommended)" | Open as #507 |
| Add a root `.gitattributes` (finding P2-7) | "Add it (Recommended)" | Merged as #504 |
| Agent files can run commands (finding P2-3) | "Validator + gate both (Recommended)" | Open as #505 |
| Merge PR #492 | "Merge #492 at 930493c5 (Recommended)" | Merged at that head |
| One-time `gate-guard` exception for PR #501 | "Approve exception, merge (Recommended)" | Merged; open PR #508 records it as APR-080 and APR-081 |
| A JavaScript test (`node --test`) ran unguarded, PR-controlled code inside a required gate job (the second P1 finding) | "Separate CI job (Recommended)" | Open as #507, which moves it into its own tools jobs |
| The #505 agent-frontmatter allow-list | "Keep it as is (Recommended)" | #505 keeps its eight allowed keys |
| Merge seven ready PRs | "Merge all seven (Recommended)" | Merged: #493, #490, #497, #494, #495, #506 and #504 |
| One-time `gate-guard` exception for PR #503 | "Approve exception, merge (Recommended)" | Merged at head `52269aab`; not yet in the approval register |
| Delivery-control tests fail on the Windows CI runner because each file's owner is not the current user | "Fix the test fixtures (Recommended)" | Not yet delivered at recording. The Windows tools job in #507 fails until it is. |

**Standing instruction.** The owner also said: "I already pre-approved all
admin merges for PRs as long as local tests and Github Actions are green. Do
not ask me again". Admin merges of PRs whose local tests and GitHub Actions
checks are green therefore need no new question. A failed `gate-guard` check
is not green, so a protected-path PR still needs its one-time exact-head
exception.

## Open PRs at recording

Codex was out of quota all day. Every Codex request today got a usage-limit
notice instead of a review. "Blocked" and "conflict" are GitHub's merge states.

| PR | Head | What it does | State at recording |
| --- | --- | --- | --- |
| [#498](https://github.com/ModernNomad-98/Project-Aegis/pull/498) | `2be5052023e6c53c150138fd937209e13b55458a` | Adds a per-surface negative-path matrix to `test-plan-designer` (D68 extension) | Rebased onto `main` at 22:09. The independent check said SHIP on the earlier head `e9cce7d`; the new head needs a check and green CI. Blocked. |
| [#500](https://github.com/ModernNomad-98/Project-Aegis/pull/500) | `f8122455baa9aed2f110696d0d701312b6825585` | Adds the manual-only `test-tenant-provisioner` skill (D68) | Rebased and renumbered to 187 to 188 after #499. The independent check said SHIP on the earlier head `77319f8`; the new head needs a check and green CI. Blocked. |
| [#502](https://github.com/ModernNomad-98/Project-Aegis/pull/502) | `08f550263d21c5d7de19b86bb84f910b22435198` | Adds the `ci-failure-classifier` skill (D68) | Independent check said SHIP on this head. Now in conflict with `main` after #499; needs a rebase, then a check of the new head. |
| [#505](https://github.com/ModernNomad-98/Project-Aegis/pull/505) | `ccb28a21ea7b2e13ac9e366ae87056c58c04d79e` | Forbids command-running keys in agent frontmatter and adds `.claude/agents` to `gate-guard` (P2-3) | Revised after a REVISE review; the revision needs its check. `gate-guard` fails by design; merging needs a one-time exact-head exception. |
| [#507](https://github.com/ModernNomad-98/Project-Aegis/pull/507) | `892a93d35b5dab3f5c9c8aec0bc7917f02694a5c` | Runs the tools test suites in separate CI jobs, outside the gates (P2-1 and the second P1) | The security review said SHIP on the earlier head `b9b0d29`. Two newer commits stop the Windows gate jobs from running programs found in the repository root; the new head needs a check. Its Windows tools job still fails until the fixture fix lands. `gate-guard` fails by design and needs a one-time exact-head exception. |
| [#508](https://github.com/ModernNomad-98/Project-Aegis/pull/508) | `3ccac3390a86fca08eee4e26a23dc1cc5a9d1fd0` | Records the #501 exception as APR-080 and APR-081, and applies approval register re-read edits E1 to E4 | CI green; waiting for its independent review. |

A new worktree, `record-d69`, appeared at recording. It suggests a D69 record
PR is being prepared; check `gh pr list` for it.

## Decisions still waiting on the owner

1. **Build approvals for three batch proposals.** Each proposal is merged and
   builds nothing until the owner decides:
   [AI-SDLC](ai-sdlc-skill-batch-proposal.md) (#494),
   [Phase 7 AI engineering](phase7-ai-engineering-skill-batch-proposal.md)
   (#495) and
   [Phase 6 reliability](phase6-reliability-skill-batch-proposal.md) (#496).
2. **Code-health findings P2-2, P2-4 and P2-6.** P2-2 is that the CI
   requirements pin direct packages but not the packages they pull in. P2-4
   and P2-6 are described in the code-health audit report in chat; they are
   not yet written down in the repository.
3. **Extra configuration guards.** Whether to guard more Claude Code
   configuration locations and keys than #505 covers. The #505 review found
   that Claude Code loads agent settings from more places than the PR checks.
4. **Required checks.** Whether to make the new tools jobs from #507
   required checks in branch protection. They are not required today.
5. **Leftover-journal handling.** How to handle leftover journal files. The
   question was raised in chat; its details are not yet written down in the
   repository.
6. **Carried over from the morning** (see
   [Still open for the owner](aegis-open-decisions-2026-09-23.md#still-open-for-the-owner)):
   the issue #101 Stage 4B proof on a real host, the semantic review of the
   private Behavioral Eval Runner (BER) candidate labels, CP-WP-003 and
   CP-WP-004 (control-plane work packages), and the paused VirtualBox virtual
   machine.

## Next steps

1. Re-check the new heads of #498 and #500. Merge each one when its CI is
   green and the check says SHIP.
2. Deliver the Windows test-fixture fix the owner chose, so the Windows tools
   job in #507 passes. Then re-check #507 and merge it with its one-time
   exact-head `gate-guard` exception.
3. Rebase #502 onto `main`, renumber its skill count, check the new head and
   merge when green.
4. Finish the #505 revision check. Merge it after #507 with its one-time
   exact-head `gate-guard` exception.
5. Get the independent review of #508 and merge it when green.
6. Record the #503 exception (head `52269aab`) in the approval register, in
   the same way #508 records #501. Also record the #505 and #507 exceptions
   once they are used.
7. Record today's later chat decisions, from the table above, in
   [Decided on 2026-09-28](aegis-open-decisions-2026-09-23.md#decided-on-2026-09-28).
8. Update the readability ledger for #489 onward, including this page, and
   run the next backlog forecast checkpoint.
9. Ask the owner the pending decisions above, one at a time.

## How to resume

1. Read this page, then do the workspace role check in `AGENTS.md`, then read
   the [approval register](../approvals/APPROVAL_REGISTER.md).
2. Check live state with `git fetch` and `gh`: the `main` head and the open
   PRs, including the PR that adds this page.
3. Follow the process rules in
   [How to resume](session-checkpoint-2026-09-28.md#how-to-resume) on the
   morning checkpoint. One change since then: under the owner's standing
   instruction above, an admin merge of a PR with green local tests and green
   GitHub Actions needs no new question. It does not waive a failed
   `gate-guard` check, the independent-review loop or the Codex wait rule in
   [APR-050](../approvals/APPROVAL_REGISTER.md#aegis-apr-050-merges-wait-for-the-automated-codex-review).
