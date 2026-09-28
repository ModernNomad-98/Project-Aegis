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
batch of testing skills from the roadmap. The artificial intelligence
(AI)-assisted software development lifecycle (SDLC) batch, the AI-SDLC batch,
covers skills for that lifecycle. The "tools test suites" are the Python tests under
`tools/aegis_setup/tests` and `tools/aegis_delivery_control/tests`. The
code-health audit of 2026-09-28 numbered its findings by priority: P1 is
high, P2 is medium. A manual-only skill runs only when the user names it.
LF is the Unix line ending; `umask` is the Unix setting that decides the
default permissions of new files. A PR's head is its latest commit. To
rebase a PR is to replay its commits onto the current `main`. Frontmatter is
the settings block at the top of a skill or agent file.

## Where things stand

| Item | Value at recording |
| --- | --- |
| Recorded at | 2026-09-28 22:30 Coordinated Universal Time (UTC) |
| Updated at | 2026-09-28 23:10 UTC, after #498, #500 and #508 merged and the owner decided D69 to D71 |
| `main` head | `d932d2cd7a82e0a5f6af8a1aa423e4db4f7dd29f` (merge of PR #508) |
| Shipped skills | 188: PR #499 added `acceptance-criteria-reviewer` (187) and PR #500 added `test-tenant-provisioner` (188) |
| Skill-contract audit | 316 findings, 232 of them informational ROUTE-002 routing notes; report format from audit engine v1.13.4 (PR #503), findings unchanged |
| Open PRs | Nine besides this page's PR #509: #502, #505, #507, #510, #511, #512, #513, #514 and #515. See [Open PRs at recording](#open-prs-at-recording). |

All times and dates are UTC.

## Merged since the morning checkpoint

The merge commit is the `main` commit that each PR created. Nineteen PRs merged
after #485, listed below in merge order (from
`git log --first-parent`). PR #487, which recorded the morning's later owner
decisions, merged just before #485 and is not repeated here. Of the numbers
#486 to #508, #487 is covered above and the three not listed (#502, #505 and
#507) are still open.

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
| [#498](https://github.com/ModernNomad-98/Project-Aegis/pull/498) | `04fb8aa54e965c41fe7c02260745708ccb26575c` | Added a per-surface negative-path matrix to `test-plan-designer` (D68 extension); merged at head `2be50520` |
| [#500](https://github.com/ModernNomad-98/Project-Aegis/pull/500) | `53f3cf2f86d112f29e8b8130047b33156154737a` | Added the manual-only `test-tenant-provisioner` skill under D68 (187 to 188); merged at head `f8122455` |
| [#508](https://github.com/ModernNomad-98/Project-Aegis/pull/508) | `d932d2cd7a82e0a5f6af8a1aa423e4db4f7dd29f` | Recorded the #501 exception as APR-080 and APR-081, and applied approval register re-read edits E1 to E4; merged at head `3ccac339` |

## Owner decisions made on 2026-09-28 after the morning checkpoint

The owner made these decisions in chat by choosing an option from the
coordinator's multiple-choice questions. The quoted text is his exact answer.
Only D68 has its own permanent record so far (PR #493). Open PR #510 records
D69, D70 and D71. The others live in chat and in the PR descriptions named
below.

| Topic | Exact chat answer | Where it stands |
| --- | --- | --- |
| Build the QA Tier 1 skill batch as proposed in PR #492 | "Build it as recommended (Recommended)" | Recorded as D68 (#493). Delivers three new skills and one extension (186 to 189). `acceptance-criteria-reviewer` (#499), the `test-plan-designer` extension (#498) and `test-tenant-provisioner` (#500) merged; `ci-failure-classifier` is open as #502. |
| Commit, push and open the PR for audit engine v1.13.4 | "Commit, push, open PR (Recommended)" | Merged as #503 |
| The tools test suites never ran in CI (finding P2-1) | "Fix and add to CI (Recommended)" | Open as #507 |
| Add a root `.gitattributes` (finding P2-7) | "Add it (Recommended)" | Merged as #504 |
| Agent files can run commands (finding P2-3) | "Validator + gate both (Recommended)" | Open as #505 |
| Merge PR #492 | "Merge #492 at 930493c5 (Recommended)" | Merged at that head |
| One-time `gate-guard` exception for PR #501 | "Approve exception, merge (Recommended)" | Merged; #508, since merged, records it as APR-080 and APR-081 |
| A JavaScript test (`node --test`) ran unguarded, PR-controlled code inside a required gate job (the second P1 finding) | "Separate CI job (Recommended)" | Open as #507, which moves it into its own tools jobs |
| The #505 agent-frontmatter allow-list | "Keep it as is (Recommended)" | #505 keeps its eight allowed keys |
| Merge seven ready PRs | "Merge all seven (Recommended)" | Merged: #493, #490, #497, #494, #495, #506 and #504 |
| One-time `gate-guard` exception for PR #503 | "Approve exception, merge (Recommended)" | Merged at head `52269aab`; not yet in the approval register |
| Delivery-control tests fail on the Windows CI runner because each file's owner is not the current user | "Fix the test fixtures (Recommended)" | Open as the tests-only PR #512 (head `a5274ba`). The Windows tools job in #507 fails until it merges. |
| Build the AI-SDLC skill batch as proposed in PR #494 | "Build it as recommended (Recommended)" | D69. Open PR #510 records it. Builds open: the `ai-closeout-reporter` per-deliverable trace (#511) and the `code-reviewer` checks (#515). |
| Build the Phase 7 AI engineering skill batch as proposed in PR #495 | "Build it as recommended (Recommended)" | D70. Open PR #510 records it. Build open: the `ai-router-architect` extension (#513). |
| Build the Phase 6 reliability skill batch as proposed in PR #496 | "Build all, backup verifier first (Recommended)" | D71. Open PR #510 records it; builds in progress. |
| Record the #503 exception in the approval register | "Confirm, record it (Recommended)" | Not yet delivered at the update; no register PR was open. |
| Guard more Claude Code configuration files than #505 covers | "Do it as proposed (Recommended)" | Not yet delivered at the update. |

**Standing instruction.** The owner also said: "I already pre-approved all
admin merges for PRs as long as local tests and Github Actions are green. Do
not ask me again". Admin merges of PRs whose local tests and GitHub Actions
checks are green therefore need no new question. A failed `gate-guard` check
is not green, so a protected-path PR still needs its one-time exact-head
exception.

## Open PRs at recording

Codex was out of quota all day. Every Codex request today got a usage-limit
notice instead of a review. This table was brought up to date at the 23:10 UTC
update.

| PR | Head | What it does | State at recording |
| --- | --- | --- | --- |
| [#502](https://github.com/ModernNomad-98/Project-Aegis/pull/502) | `288e9cd3e07a03e598f0e423f8461e1a403f99eb` | Adds the `ci-failure-classifier` skill (D68) | Rebased onto `main` and renumbered to 188 to 189 (its title still says 186 to 187). CI green. The independent check said SHIP on the earlier head `08f5502`; the new head needs a check. |
| [#505](https://github.com/ModernNomad-98/Project-Aegis/pull/505) | `ccb28a21ea7b2e13ac9e366ae87056c58c04d79e` | Forbids command-running keys in agent frontmatter and adds `.claude/agents` to `gate-guard` (P2-3) | Revised after a REVISE review; the revision needs its check. `gate-guard` fails by design; merging needs a one-time exact-head exception. |
| [#507](https://github.com/ModernNomad-98/Project-Aegis/pull/507) | `3f9c8f1b5c96958866971a1090857d0e63087163` | Runs the tools test suites in separate CI jobs, outside the gates (P2-1 and the second P1) | The security review said SHIP on the earlier head `b9b0d29`. Newer commits `892a93d` and `3f9c8f1` stop the Windows gate jobs from running programs found in the repository root (the executable-search fix). A last hardening round is in progress; the final head needs a check. `tools-tests-linux` passes; `tools-tests-windows` fails until #512 merges. `gate-guard` fails by design and needs a one-time exact-head exception. |
| [#510](https://github.com/ModernNomad-98/Project-Aegis/pull/510) | `93f6e940fb58001a3c60b3532e0eb29d8e821d0f` | Records D69, D70 and D71 in the reconciliation log and the open-decisions page | CI green; waiting for its independent review. |
| [#511](https://github.com/ModernNomad-98/Project-Aegis/pull/511) | `81b4234c1f87a4bd4cc2fdaa437ac36ffa091d76` | Adds a per-deliverable trace to `ai-closeout-reporter` (D69; folds in backlog candidates #267 and #273) | CI green; waiting for its independent review. |
| [#512](https://github.com/ModernNomad-98/Project-Aegis/pull/512) | `a5274ba682b343582d61e3ada9633a6b5d776e1a` | Tests only: makes the delivery-control Windows fixtures owned by the current user | CI green; waiting for its independent review. Unblocks the Windows tools job in #507. |
| [#513](https://github.com/ModernNomad-98/Project-Aegis/pull/513) | `232e4d4d64c88469aa5874d4cd89fb5601fc6c6b` | Extends `ai-router-architect` with per-provider adapters, a capability matrix and conformance tests (D70; folds in backlog candidate #282) | CI green; waiting for its independent review. |
| [#514](https://github.com/ModernNomad-98/Project-Aegis/pull/514) | `5b0e59b635cf5368d54e12c3f055620f9ad657ef` | Records #489 to #508 in the readability ledger | CI green; waiting for its independent review. |
| [#515](https://github.com/ModernNomad-98/Project-Aegis/pull/515) | `1b4638f5f99cdde5fda2ed39a887a918b6487829` | Adds weakened-validation and architecture decision record (ADR) drift checks to `code-reviewer` (D69; folds in backlog candidate #277) | CI green; waiting for its independent review. |

## Decisions still waiting on the owner

1. **Code-health findings P2-2, P2-4 and P2-6.** P2-2 is that the CI
   requirements pin direct packages but not the packages they pull in. P2-4
   and P2-6 are described in the code-health audit report in chat; they are
   not yet written down in the repository.
2. **Required checks.** Whether to make the new tools jobs from #507
   required checks in branch protection. They are not required today.
3. **Leftover-journal handling.** How to handle leftover journal files. The
   question was raised in chat; its details are not yet written down in the
   repository.
4. **Carried over from the morning** (see
   [Still open for the owner](aegis-open-decisions-2026-09-23.md#still-open-for-the-owner)):
   the issue #101 Stage 4B proof on a real host, the semantic review of the
   private Behavioral Eval Runner (BER) candidate labels, CP-WP-003 and
   CP-WP-004 (control-plane work packages), and the paused VirtualBox virtual
   machine.

## Next steps

1. Review #512 and merge it when green. Then re-check #507 at its final head
   and merge it with its one-time exact-head `gate-guard` exception.
2. Check #502 at its new head `288e9cd`, correct its title to 188 to 189, and
   merge it when green.
3. Finish the #505 revision check. Merge it after #507 with its one-time
   exact-head `gate-guard` exception.
4. Review #510 (D69, D70 and D71) and merge it when green.
5. Build the D69, D70 and D71 batches (Phase 6: backup verifier first).
   Review and merge each build, starting with #511, #513 and #515.
6. Record the #503 exception (head `52269aab`) in the approval register, as
   the owner confirmed, in the same way #508 records #501. Also record the
   #505 and #507 exceptions once they are used.
7. Build the extra configuration-file guards the owner approved.
8. Record today's other later chat decisions, from the table above, in
   [Decided on 2026-09-28](aegis-open-decisions-2026-09-23.md#decided-on-2026-09-28)
   (#510 adds D69, D70 and D71 there).
9. Review and merge the readability ledger update (#514). Then record the
   later merges, including this page, and run the next backlog forecast
   checkpoint.
10. Ask the owner the pending decisions above, one at a time.

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
