# Session checkpoint — 2026-09-27

> **Why this page exists:** On 2026-09-27 the owner, Peter Nguyen, paused work
> and asked for all progress to be saved in the repository. When he says
> "continue", a new session resumes from this page. It records state only. It
> grants no implementation, host or provider authority. Verify every fact below
> against the live repository before acting on it.

Terms used here: a pull request (PR) is a proposed change on GitHub. A commit
hash (SHA) identifies one exact commit. An approval-register entry (APR) records
a scoped owner decision in the [approval register](../approvals/APPROVAL_REGISTER.md).
The Behavioral Eval Runner (BER) is the repository's behavioral test tool.
Control-plane work packages (CP-WP) are tracked in the
[control-plane backlog](resumable-control-plane-backlog.md). ROUTE-002 is the
audit rule that flags a routing exclusion one skill states but the other skill
does not repeat. Codex is the automated GitHub code reviewer. OWASP is the
Open Worldwide Application Security Project; LLM08 is a risk in its Top 10 for
Large Language Model (LLM) applications. D-numbered decisions such as D65 and
D67 are in the [step-0 reconciliation log](../reconciliation/step-0-reconciliation-v4.md).

## Where things stand

| Item | Value at pause |
| --- | --- |
| `main` head | `3c51fb2f6f4a22c6120b38d2a7e9f0074b6bf69c` (merge of PR #441) |
| Shipped skills | 186 |
| Skill-contract audit | 316 findings, 232 of them ROUTE-002, with audit engine v1.13.2 (regenerated in PR #441) |

All times and dates are Coordinated Universal Time (UTC).

## Merged this session

The merge commit is the `main` commit that each PR created.

| PR | Merge commit | What it did |
| --- | --- | --- |
| [#397](https://github.com/ModernNomad-98/Project-Aegis/pull/397) | `4a68acef7d7d0bfc4d60755c81c544fc88923e0f` | Recorded what was decided for each ROUTE-002 routing note |
| [#403](https://github.com/ModernNomad-98/Project-Aegis/pull/403) | `f42e3f0f6469d7c1d4cc3fabb5c208383efdc01d` | Recorded final acceptance of the feature-flag-architect pages |
| [#409](https://github.com/ModernNomad-98/Project-Aegis/pull/409) | `4416c6d96d7701f449758223ad2d1240fe773207` | Extended and renamed the LLM08 skill to `hidden-context-exposure-reviewer` |
| [#410](https://github.com/ModernNomad-98/Project-Aegis/pull/410) | `b553d91d064370c18227d837ea4d31bca204b0a3` | Full-page re-read fixes to four skill pages |
| [#411](https://github.com/ModernNomad-98/Project-Aegis/pull/411) | `7693c26d120f29ec1cfd0c761c45315b4cd5515d` | Re-read fixes to the skills catalog and `cloud-architecture-decider` |
| [#412](https://github.com/ModernNomad-98/Project-Aegis/pull/412) | `2219ac81937d2a533bc32451edc8a9709fc53bfa` | README re-read fixes |
| [#413](https://github.com/ModernNomad-98/Project-Aegis/pull/413) | `fa1e34444ce834e6b40ea612a070a93adff32c8b` | Corrected the master-prompt section citation |
| [#414](https://github.com/ModernNomad-98/Project-Aegis/pull/414) | `3a1e9da434dc1fe91811e56c8fb8bf9c80e247dd` | Re-read fixes to the instruction map, decision inputs and reconciliation log |
| [#415](https://github.com/ModernNomad-98/Project-Aegis/pull/415) | `f4defa2c156d4e8e416461084156b1a65038e43d` | Re-read fixes to the OWASP security pages |
| [#416](https://github.com/ModernNomad-98/Project-Aegis/pull/416) | `da2636d049db25a4fc367c025e44636c9de66e6d` | Re-read fixes to the ROUTE-002 record and the AEGIS-060+ register |
| [#417](https://github.com/ModernNomad-98/Project-Aegis/pull/417) | `dcec7f22292e9cd45e5f7507e5ee7cfaddf832c2` | Mirrored description hand-backs in "Use When" (batch B) |
| [#418](https://github.com/ModernNomad-98/Project-Aegis/pull/418) | `02f054c0816d0a244063ae03aeb5ebd06fca5339` | Same, batch C |
| [#419](https://github.com/ModernNomad-98/Project-Aegis/pull/419) | `9033e7c70327420cdc3d4196f3b97ce7a9e880da` | Same, batch A |
| [#420](https://github.com/ModernNomad-98/Project-Aegis/pull/420) | `dfb0cac85a3e486955afae94b672a607958cf286` | Recorded owner decisions: live routing test grant and security-review scope |
| [#421](https://github.com/ModernNomad-98/Project-Aegis/pull/421) | `4b205a7a56b6ba3cfa56f13e7e7d70d0c7d36944` | Required the security line on every PR; kept the checklist advisory |
| [#422](https://github.com/ModernNomad-98/Project-Aegis/pull/422) | `5d91fa5c1b3b7d0f0e0335c362e9cacf99d03cf5` | Re-read fixes to `hidden-context-exposure-reviewer` and `agent-tool-safety-guard` |
| [#423](https://github.com/ModernNomad-98/Project-Aegis/pull/423) | `656194426e2ea3358fa29fcf19e05f0278d9c270` | Added D67, the after-the-fact decision record for `aegis-setup` |
| [#424](https://github.com/ModernNomad-98/Project-Aegis/pull/424) | `5711ddfc875a1866485c8feceac83490b656fa6c` | Extended `llm-output-safety-reviewer` to artificial intelligence (AI)-generated code |
| [#425](https://github.com/ModernNomad-98/Project-Aegis/pull/425) | `7b8884133fe92da8adae6b929c5440e05c1ed10b` | Dated the BER README's pinned census counts |
| [#426](https://github.com/ModernNomad-98/Project-Aegis/pull/426) | `a06f815b602705f2ca75bad3ccea520c24fa429e` | Recorded #410 and #412–#419 in the readability ledger |
| [#427](https://github.com/ModernNomad-98/Project-Aegis/pull/427) | `0030e73f3616c46be3393813ea403c262d96a823` | Extended `prompt-injection-defender` to multimodal injection |
| [#428](https://github.com/ModernNomad-98/Project-Aegis/pull/428) | `0cb07776923d1899002b2cb4624c742652bde8ed` | Extended `supply-chain-security-reviewer` to promoted model artifacts |
| [#429](https://github.com/ModernNomad-98/Project-Aegis/pull/429) | `169e8be44d80f08938b7728000251dcfce2223bb` | Made the ROUTE-002 audit rule match whole skill names |
| [#430](https://github.com/ModernNomad-98/Project-Aegis/pull/430) | `6712ebbc73897dc93fa47cdcfaca95efbef0f74a` | Added a glossary for the README reference tables |
| [#431](https://github.com/ModernNomad-98/Project-Aegis/pull/431) | `dfbcf0f4b8e0b52516c90cb9d2c7ec5d16335ba0` | Recorded three more owner decisions |
| [#432](https://github.com/ModernNomad-98/Project-Aegis/pull/432) | `7894567d49d301f82f40cb6445b668581d5799ac` | Regenerated the skill-contract audit baselines |
| [#433](https://github.com/ModernNomad-98/Project-Aegis/pull/433) | `9104cff1f676b7aef310ec83c0f0966020ec85d5` | Recorded the live startup-routing acceptance run |
| [#434](https://github.com/ModernNomad-98/Project-Aegis/pull/434) | `b7dc0601b03643d947b91de785cfc21ff2f01432` | Routed file-content injection to `prompt-injection-defender` |
| [#435](https://github.com/ModernNomad-98/Project-Aegis/pull/435) | `a96b902e90478af4951137559b7c28df8da77745` | Made the orchestrator point setup requests to `/aegis-setup` |
| [#436](https://github.com/ModernNomad-98/Project-Aegis/pull/436) | `862dd90853806d7f0a4d1bf51158c8d1fb1679c8` | Recorded that engine v1.13.2 removed the ROUTE-002 false positive |
| [#437](https://github.com/ModernNomad-98/Project-Aegis/pull/437) | `96cf65acd80bd68a43edeba59fce70991e84004e` | Cited the live startup-routing run in the README |
| [#438](https://github.com/ModernNomad-98/Project-Aegis/pull/438) | `5dbf7bc9e958d932bd0c5b093ebecfe61be41840` | Recorded grant lifecycle events and three more owner decisions |
| [#439](https://github.com/ModernNomad-98/Project-Aegis/pull/439) | `d2d9b05e948c82b32cc34200d64d48ce0afd0347` | Closed D65's open gaps and fixed first-use terms in the log |
| [#440](https://github.com/ModernNomad-98/Project-Aegis/pull/440) | `adf54d98ef3454efb5cdf8dd9266fc71f9031c57` | Recorded #420–#439 in the readability ledger |
| [#441](https://github.com/ModernNomad-98/Project-Aegis/pull/441) | `3c51fb2f6f4a22c6120b38d2a7e9f0074b6bf69c` | Regenerated the audit baselines with engine v1.13.2 (APR-065) |

A search for PRs merged on 2026-09-27 also returns #371, #375–#379,
#381–#396, #398–#402 and #404–#408. They merged earlier the same day and are
not part of this list.

## Owner decisions made on 2026-09-27

The decisions are recorded in
[Decided on 2026-09-27](aegis-open-decisions-2026-09-23.md#decided-on-2026-09-27)
and in register entries
[APR-057](../approvals/APPROVAL_REGISTER.md#aegis-apr-057-live-startup-routing-acceptance-test-re-run)
through
[APR-065](../approvals/APPROVAL_REGISTER.md#aegis-apr-065-regenerate-the-audit-baselines-once-more-with-engine-v1132).
Those records hold the scope and authority; this page does not restate them.

## Open items at the pause

1. **APR-065 consumption.** Done in the PR that adds this page:
   [APR-066](../approvals/APPROVAL_REGISTER.md#aegis-apr-066-consumption-of-the-engine-v1132-baseline-regeneration-grant)
   records that PR #441 used the grant.
2. **Readability ledger.** PR #440 left these pages pending a full-page
   re-read: the approval register, the open-decisions index, the PR template,
   the skills catalog, the AEGIS-060+ register, the audit baseline report, the
   live-acceptance record, the `api-event-architect` skill page,
   `llm-top10-threat-catalog.md` and `poisoning-controls.md`. The next ledger
   update must record #438, #441 and the PR that adds this page.
3. **Owner questions from the ledger review.** Peter has not answered these:
   - Do edits made before the 10-line rule existed count toward it for the
     `project-orchestrator` skill page?
   - May PRs #420, #421 and #423, which had targeted edits but no posted
     review, keep their acceptance?
   - Do generated reports, such as the audit baseline report, need their own
     ledger class?
4. **Notes, no action needed.**
   - The trigger test separating `supply-chain-security-reviewer` from
     `release-readiness-reviewer` shipped in PR #428.
   - D65's open gaps were closed by PR #439.
   - The BER census baseline stays pinned at 184 skills by design
     (`EXPECTED_PINNED_BASELINE` in `tools/behavioral_eval_runner/census.py`).
     It is a historical baseline, not the current count.
5. **Still waiting on the owner** (see [Still open for the owner](aegis-open-decisions-2026-09-23.md#still-open-for-the-owner)): the Stage 4B actual-host proof, the private
   BER labels, CP-WP-003 and CP-WP-004, and the paused VirtualBox virtual
   machine.

## How to resume

1. Read this page, then do the workspace role check in `AGENTS.md`, then read
   the [approval register](../approvals/APPROVAL_REGISTER.md).
2. Check live state with `git fetch` and `gh`: the `main` head and the open
   PRs, including the PR that adds this page.
3. Follow these process rules:
   - An independent reviewer checks each PR. A separate check confirms any
     fixes.
   - Merge only when the checks on the exact head commit are green; Codex
     has reviewed that head, or posted a usage-limit notice after it; and
     every Codex finding on that head has a fix or a reasoned reply.
   - Merge with `gh pr merge <number> --merge --admin --match-head-commit <head SHA>`.
   - Sign off every commit with `git commit -s`, because CI checks the
     Developer Certificate of Origin (DCO). Stage files by exact path only.
   - Make each change in its own worktree, branched from a fresh `origin/main`.
   - A PR that changes a protected path needs a one-time owner exception for
     its exact head.
   - Reviewers post their verdicts as PR comments.
   - Follow the 10-line rule in the
     [readability ledger](aegis-documentation-readability-backlog.md): a
     reviewed targeted edit of at most 10 changed lines on a page, counted
     since its last full-page acceptance, keeps acceptance; a larger change
     needs a full-page re-read.
   - Every PR description answers the security line.
   - Use PowerShell for `git` when Bash `git` hangs.

> **Later clarification — 2026-10-01.** Nothing above is changed. The
> sign-off rule under [How to resume](#how-to-resume) has an unnamed
> exception. The check requires a `Signed-off-by:` trailer on every
> commit in the pull request's range, except two machine authors that
> cannot sign off — `dependabot[bot]` and `github-actions[bot]` — per
> [D60](../reconciliation/step-0-reconciliation-v4.md#5-recorded-decisions).
> That exemption is deliberately **not an authentication boundary**.
