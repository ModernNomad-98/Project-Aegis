# Session checkpoint — 2026-09-28

> **Why this page exists:** This page records the 2026-09-28 session so that a
> new session can resume from it when the owner, Peter Nguyen, says
> "continue". It records state only. It grants no implementation, host or
> provider authority. Verify every fact below against the live repository
> before acting on it.

Terms used here: a pull request (PR) is a proposed change on GitHub. A commit
hash (SHA) identifies one exact commit. An approval-register entry (APR) records
a scoped owner decision in the [approval register](../approvals/APPROVAL_REGISTER.md).
The Behavioral Eval Runner (BER) is the repository's behavioral test tool.
Control-plane work packages (CP-WP) are tracked in the
[control-plane backlog](resumable-control-plane-backlog.md). ROUTE-002 is the
audit rule that flags a routing exclusion one skill states but the other skill
does not repeat. Codex is the automated GitHub code reviewer. `gate-guard` is
the continuous integration (CI) check that fails when a PR changes a protected
path. Artificial intelligence (AI) is spelled out here because a decision below
is about that abbreviation. A virtual machine (VM) is a simulated computer.
A manual-only skill runs only when the user names it; the *(manual-only)*
marker flags it where a page hands off to it. Dependabot is GitHub's automated
dependency-update bot. D15 is a 2026-07-07 decision in the
[reconciliation log](../reconciliation/step-0-reconciliation-v4.md) that
recorded enrichments for four skills.

## Where things stand

| Item | Value at recording |
| --- | --- |
| `main` head | `ecd1e59e80d95dab483b14b14a9c448edb94e9a3` (merge of PR #483) |
| Shipped skills | 186 |
| Skill-contract audit | 316 findings, 232 of them ROUTE-002; report format from audit engine v1.13.3 (PR #461), findings unchanged |
| Open PRs | [#484](https://github.com/ModernNomad-98/Project-Aegis/pull/484) at head `2f5858c`: shortens the `project-orchestrator` manual-only labels and adds `local-ci-mirror-preflight` to the stage-gate map; [#486](https://github.com/ModernNomad-98/Project-Aegis/pull/486) at head `8459ac7`: spells out "artificial intelligence (AI)" at first use. Both open at recording. |

All times and dates are Coordinated Universal Time (UTC).

## Merged this session

The merge commit is the `main` commit that each PR created. Forty PRs merged
in this session.

| PR | Merge commit | What it did |
| --- | --- | --- |
| [#443](https://github.com/ModernNomad-98/Project-Aegis/pull/443) | `e251c5146f627ec31b7d2f750f0dbabe0bca7ede` | Dependabot bump of `actions/setup-node` from 4.4.0 to 7.0.0 (one-time exception, APR-071) |
| [#445](https://github.com/ModernNomad-98/Project-Aegis/pull/445) | `8c52960b16493577af813f602d8d02281140bb96` | Re-read readability fixes to three skill pages |
| [#446](https://github.com/ModernNomad-98/Project-Aegis/pull/446) | `7005cdacdce225cb1318196a31a22a7dbb734022` | Recorded #438–#442 and the owner's 2026-09-28 rules in the readability ledger |
| [#447](https://github.com/ModernNomad-98/Project-Aegis/pull/447) | `484d10476eca116f117258c0f96245a97ba3eaca` | Re-read fixes to the open-decisions index and PR template; recorded the first 2026-09-28 owner decisions |
| [#448](https://github.com/ModernNomad-98/Project-Aegis/pull/448) | `2bcbfe6358903081faca9da9e06cea37826344e0` | Added a reading aid to the approval register |
| [#449](https://github.com/ModernNomad-98/Project-Aegis/pull/449) | `bb7ed711bd566e106b91ac986b97774b1a5e16c6` | Clarified the audit register, baseline preface and routing evidence |
| [#450](https://github.com/ModernNomad-98/Project-Aegis/pull/450) | `bb3b117d34955f665553c3b75130e4c4144d758a` | Recorded closeout events for four spent grants (APR-067 to APR-070) |
| [#451](https://github.com/ModernNomad-98/Project-Aegis/pull/451) | `0d4b093fdd36bafa8367eab2e68d318e31c58a72` | Added a grouped abbreviation glossary to the skills catalog |
| [#452](https://github.com/ModernNomad-98/Project-Aegis/pull/452) | `419ad2313a60cd39b33dbb572115f42bec6fa870` | Spelled out abbreviations at first use in `project-orchestrator` |
| [#453](https://github.com/ModernNomad-98/Project-Aegis/pull/453) | `4226d293a965fe595be4a6f941bd074f6db942a9` | Recorded the PR #443 exception and the engine v1.13.3 report grant (APR-071 to APR-073) |
| [#454](https://github.com/ModernNomad-98/Project-Aegis/pull/454) | `5bd21fbd88e08e9eda89d252a008d804b90a4644` | Marked the Stage 6 manual-only enforcers in `project-orchestrator` |
| [#455](https://github.com/ModernNomad-98/Project-Aegis/pull/455) | `c789f582bd608ad8cb6fb9636dde1563f5cdad90` | Applied the D15 enrichment deltas to four shipped skills |
| [#456](https://github.com/ModernNomad-98/Project-Aegis/pull/456) | `072a1b0a8c160d904d5e2072fb02491c17d14152` | Re-read fixes to `tenant-modeler` and `source-of-truth-reconciler` |
| [#457](https://github.com/ModernNomad-98/Project-Aegis/pull/457) | `4920686388138c295d4172ebcae31646dbe5916b` | Backlog forecast checkpoint after #454 |
| [#458](https://github.com/ModernNomad-98/Project-Aegis/pull/458) | `ec8cf3e0939bec23802673967b0eda9aca6b732c` | Recorded #443 to #454 in the readability ledger |
| [#459](https://github.com/ModernNomad-98/Project-Aegis/pull/459) | `da4336273ab44c124439fff82c6c94e70def1db1` | Re-read fixes to the cost-guardrail and streaming skills |
| [#460](https://github.com/ModernNomad-98/Project-Aegis/pull/460) | `61763d8f2ccf66c58a6467eecb4ba3a1ba3a2e00` | Recorded the later 2026-09-28 owner decisions in the open-decisions index |
| [#461](https://github.com/ModernNomad-98/Project-Aegis/pull/461) | `dc3c767dc91d936cc8cc70589137ca33e6f44b7c` | Made the audit report readable on its own (engine v1.13.3, APR-073) |
| [#462](https://github.com/ModernNomad-98/Project-Aegis/pull/462) | `ad5c0538d122e68a47b65c98879c3efc21f171ad` | Re-read fixes to the `ai-closeout-reporter` pages |
| [#463](https://github.com/ModernNomad-98/Project-Aegis/pull/463) | `2f61f9707d3ca58a3dedd6cbb05eebdd23fbe0f4` | Re-read readability fixes to `ai-sdlc-operating-model` |
| [#464](https://github.com/ModernNomad-98/Project-Aegis/pull/464) | `c857e56ff34592e678c35447cb1a5531bbb5f397` | Reading-aid fixes from the approval register re-read |
| [#465](https://github.com/ModernNomad-98/Project-Aegis/pull/465) | `5bff21d53eac39571c239caa421ace6e0ddbc634` | Recorded APR-074 to APR-076 for the PR #461 merge |
| [#466](https://github.com/ModernNomad-98/Project-Aegis/pull/466) | `adea71e0c1a6a0c3f9f23cfb55098665ed16f196` | Readability sweep, batch 1 |
| [#467](https://github.com/ModernNomad-98/Project-Aegis/pull/467) | `164bea8dd621dd3023c8caf1f398791d1cdac0d8` | Readability sweep, batch 4 |
| [#468](https://github.com/ModernNomad-98/Project-Aegis/pull/468) | `45b6118cbc3d76eea064fa4a203261956d326d1e` | Readability sweep, batch 9 |
| [#469](https://github.com/ModernNomad-98/Project-Aegis/pull/469) | `29435b3cfced222ef3dc28574bbb0b374fec43f0` | Readability sweep, batch 8 |
| [#470](https://github.com/ModernNomad-98/Project-Aegis/pull/470) | `d9bc77400c51e3a29b3f4fee268c3bdf4fc0ff52` | Readability sweep, batch 7 |
| [#471](https://github.com/ModernNomad-98/Project-Aegis/pull/471) | `4b448403b4ecddcc4e3152bfadce39da9e1faca5` | Readability sweep, batch 2 |
| [#472](https://github.com/ModernNomad-98/Project-Aegis/pull/472) | `f31d665616bde8bef6d3446b7758d34182ab9842` | Readability sweep, batch 6 |
| [#473](https://github.com/ModernNomad-98/Project-Aegis/pull/473) | `08470871f1f9ea0560253481263e6353dfa71895` | Readability sweep, batch 3 |
| [#474](https://github.com/ModernNomad-98/Project-Aegis/pull/474) | `2be0a77f59a21fad9cd478e83113fb89105703d1` | Readability sweep, batch 5 |
| [#475](https://github.com/ModernNomad-98/Project-Aegis/pull/475) | `59b2fb7cbc5dbc27ff33a1d2bf59792d5e865ccc` | Readability edits to the BER README (one-time exception, APR-077) |
| [#476](https://github.com/ModernNomad-98/Project-Aegis/pull/476) | `8f3d369d12962496d25c25a88f29aa885850c2b2` | Recorded the paused VM setup and defined terms on the BER host pages |
| [#477](https://github.com/ModernNomad-98/Project-Aegis/pull/477) | `6d2b2f6c9c59a5bad4b83a8ab65e3809f2e98de9` | Recorded #453, #455 to #474 and the sweep in the readability ledger |
| [#478](https://github.com/ModernNomad-98/Project-Aegis/pull/478) | `3ac0c2f48a46b762b7e40cc906079f2a902e350a` | Backlog forecast checkpoint after #474 |
| [#479](https://github.com/ModernNomad-98/Project-Aegis/pull/479) | `5d0fa769c37cad32ff543a0c7dd2b9f571b1fd85` | Recorded the PR #475 exception and its consumption (APR-077 and APR-078) |
| [#480](https://github.com/ModernNomad-98/Project-Aegis/pull/480) | `19d26a941d0d55eab3ad9fe805732c7917387dfb` | Fixes from the small-edit reviews to eleven pages |
| [#481](https://github.com/ModernNomad-98/Project-Aegis/pull/481) | `6567fba78dd1ed3d3acb4f31ab554a8c198d276e` | Clarified two approval register reading aids |
| [#482](https://github.com/ModernNomad-98/Project-Aegis/pull/482) | `7c8dbf64af2d97b6c99dca4f89dc71ae133fde6a` | `adr-writer` readability fixes and the `code-reviewer` routing wording |
| [#483](https://github.com/ModernNomad-98/Project-Aegis/pull/483) | `ecd1e59e80d95dab483b14b14a9c448edb94e9a3` | Four reviewer follow-ups from 2026-09-28 |

A search for PRs merged on 2026-09-28 also returns #442, which added the
[2026-09-27 checkpoint](session-checkpoint-2026-09-27.md) at 00:04 UTC and
belongs to that session. Dependabot PR #444 was closed without merging, as
the owner decided.

## Owner decisions made on 2026-09-28

Most decisions are recorded in
[Decided on 2026-09-28](aegis-open-decisions-2026-09-23.md#decided-on-2026-09-28)
(PRs #447 and #460) and in register entries
[APR-067](../approvals/APPROVAL_REGISTER.md#aegis-apr-067-consumption-of-the-cp-wp-002-kernel-grant)
through
[APR-078](../approvals/APPROVAL_REGISTER.md#aegis-apr-078-consumption-of-the-pr-475-exception).
Those records hold the scope and authority; this page does not restate them.

The owner made these later decisions in chat by choosing an option from the
coordinator's multiple-choice questions. None of them was recorded in the
open-decisions index at this recording; a separate PR is adding them.

| Topic | Chosen option | Status |
| --- | --- | --- |
| Spell out "AI" as "artificial intelligence (AI)" at first use, across the library | "Spell it out everywhere" | Open at recording as PR #486 (head `8459ac7`) |
| Add `local-ci-mirror-preflight` to the stage-gate map | "Add it to the map (Recommended)" | In PR #484 |
| Use the short *(manual-only)* marker everywhere | "Use the short form everywhere (Recommended)" | In PR #484 |
| `code-reviewer` description: send skill-library PRs to `library-diff-reviewer` | "Apply it (Recommended)" | Delivered by PR #482 |
| BER README readability edits (PR #475) and their one-time `gate-guard` exception at head `acdcdad` | "Prepare it (Recommended)", then "Approve for acdcdad only (Recommended)" | Merged; recorded as APR-077 and APR-078 |
| Which skill mentions get a *(manual-only)* marker | "Mark real handoffs only (Recommended)": mark a manual-only skill wherever a page tells the reader or agent to go to it or hand off to it (running text, "Do NOT use" lines and Stop Conditions); skip bare mentions in templates, checklists and eval lists | Applied in #480 and #483 |

## Open items at recording

1. **Approval register re-read.** PR #479 added 51 lines (APR-077 and
   APR-078) to the approval register. That is over the 10-line rule, so the
   page needs an independent full-page re-read before the readability ledger
   can accept it again.
2. **Readability ledger.** The next ledger update must record #475 to #483,
   any later merges, and the PR that adds this page.
3. **`library-diff-reviewer` frontmatter.** Its description still says
   "library-changing PR", while the body, catalog, README and `code-reviewer`
   now say "skill-library PR". PR #483 left it alone on purpose because it is
   frontmatter, which affects routing. The owner may choose to align it.
4. **Audit report format.** The one-time readability review of the audit
   report's output format (engine v1.13.3) is still pending. Under the
   generated-reports decision, it is judged once on the generator's format.
5. **Still waiting on the owner** (see
   [Still open for the owner](aegis-open-decisions-2026-09-23.md#still-open-for-the-owner)):
   the issue #101 Stage 4B proof on a real host, the semantic review of the
   private BER candidate labels,
   CP-WP-003 and CP-WP-004, and the paused VirtualBox VM. The choice of
   which backlog item to unblock first is deferred.
6. **Open-decisions index.** The six later decisions above are not yet
   recorded in
   [Decided on 2026-09-28](aegis-open-decisions-2026-09-23.md#decided-on-2026-09-28)
   at this recording; a separate PR is adding them. The "Spell it out
   everywhere" work is open at recording as PR #486 (head `8459ac7`, in
   review), and PR #484 is open at recording, in its final check.

## How to resume

1. Read this page, then do the workspace role check in `AGENTS.md`, then read
   the [approval register](../approvals/APPROVAL_REGISTER.md).
2. Check live state with `git fetch` and `gh`: the `main` head and the open
   PRs, including #484, #486 and the PR that adds this page.
3. Follow these process rules:
   - An independent reviewer checks each PR. A separate check confirms any
     fixes.
   - Merge only when the checks on the exact head commit are green; Codex
     has reviewed that head, or posted a usage-limit notice after it; and
     every Codex finding on that head has a fix or a reasoned reply. Codex
     was out of quota all day on 2026-09-28; a usage-limit notice posted
     after the head counts as Codex being unavailable under
     [APR-050](../approvals/APPROVAL_REGISTER.md#aegis-apr-050-merges-wait-for-the-automated-codex-review).
   - Merge with `gh pr merge <number> --merge --admin --match-head-commit <head SHA>`.
   - The owner's standing chat instruction pre-approves commits, pushes and
     merges that pass local tests and are green on GitHub Actions. It does
     not waive a failed `gate-guard` check, the independent-review loop or
     APR-050.
   - The Claude Code permission check sometimes blocks a merge or a worker
     agent's GitHub write. When that happens, ask the owner to name the PR
     and its head commit.
   - Worker agents are `aegis-worker` agents (Opus 5.5, medium effort).
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
