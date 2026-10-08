# FU-1 Parts A and C — Stage B INDEPENDENT PLAN AUDIT, rev1

**`SD-B: REVISE`** on `PLAN-A-rev1.md`, sha256
`9cd43efeee0c8a66c9059e69c3dc00af48f0517f402344468d578e8013cd1f98`. I read the hash at
2026-10-08T14:34:01Z, before reading the plan, and again at 14:49:16Z after the audit. Both reads gave the same value.

There is one blocking finding (B-1). It is a one-clause correctness fix in the new "Reading a
failure" row C-7, plus a supporting fact row. Everything else in the plan held up when I checked it
adversarially. A rev2 that changes only what B-1 asks for, and optionally the listed nits, needs
only a short re-audit of those changes.

**Auditor:** the FU-1 Part A/C plan-audit agent. I did not write this plan, and I will not
implement, validate, review or merge FU-1. I audited Parts A and C only. Part B (the PR template)
belongs to the parallel auditor. I checked only that Part B's B-3 conditions agree with this plan
and with the workflow.
**Base:** `git ls-remote origin refs/heads/main` → `c060a7cb09758fa2f4f6b67ab00094f01d7c6a46` at
14:49Z, the same as the plan's base.
**Bound inputs, recomputed (`sha256sum`):** E1 `62f6c381…33bd1`, E2 `d41453ae…b30a4`,
E3 `71e27df3…852c5a`, E4 `ef3f9ad9…69ac`, E6 `adcd867d…4a10`; `apply_plan_a.py`
`551a1edd…f8505`; `plan-a-dryrun.diff` `9f647e33…3ea80`. All match the plan.
**Brief:** `BRIEF.md` `584ca29a…21ec9`. `PLAN-B-rev1.md` `55e40d5d…8cda` was read only for the
B-3 cross-check.

## 0. Aegis skills used (Stage B)

| Skill | Stage / agent | Scope check and how applied | Result |
| --- | --- | --- | --- |
| [`acceptance-criteria-reviewer`](https://github.com/ModernNomad-98/Project-Aegis/blob/main/.claude/skills/acceptance-criteria-reviewer/SKILL.md) (partial fit) | B / Part A+C plan auditor | `docs/delivery-workflow.md` names it as a partial fit for Stage B only. It gives one verdict per criterion and "never decides whether work is done". I used its three-part test: outcome, threshold, evidence. I also used its gap and contradiction steps on AC-1 to AC-15. The ACCEPT/REVISE verdict and the hash binding are procedural. | §4: 14 TESTABLE, 1 NEEDS-REWRITE (AC-9, through B-1). Gaps: one. |
| [`source-of-truth-reconciler`](https://github.com/ModernNomad-98/Project-Aegis/blob/main/.claude/skills/source-of-truth-reconciler/SKILL.md) | B / Part A+C plan auditor | Used to check the plan's nine conflict verdicts (C1–C9). I re-read each source and applied the skill's default precedence: live repository state wins IS-questions, and canonical records win SHOULD-questions. | All nine verdicts are correct. I found one IS-conflict the plan missed: the advisory jobs' `needs` semantics (B-1). |

No MANUAL-ONLY skill was used. No skill owns a plan-level verdict, so this stage is procedurally
enforced.

## 1. Blocking finding

### B-1 — C-7 states only one cause for a skipped advisory job; `needs: [changes]` adds a second

- **Plan text (C-7, §6.5):** "| An advisory job is skipped | The path filter did not select it for
  this pull request. It did not run, so record it as skipped, not as passed; the post-merge run on
  `main` runs it. |"
- **The workflow:** all three advisory jobs declare `needs: [changes]` (`validate-skills.yml:274`,
  `:362`, `:412`). Their `if:` expressions (`:275`, `:363`, `:413`) contain no status-check
  function.
- **GitHub Actions rule:** read today from
  `https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax`
  (`jobs.<job_id>.needs`): "If a job fails or is skipped, all jobs that need it are skipped unless
  the jobs use a conditional expression that causes the job to continue."
- **Consequence:** if the `changes` job fails, times out or is cancelled, all three advisory jobs
  show as skipped. This happens on a `tools/` pull request and on a push to `main` too. The C-7
  row would then send the reader to the wrong cause, the path filter.
- **Why this matters here:**
  - `docs/offline-ci.md:5` says the guide exists to explain "how to interpret a failure or skip".
  - C-7 is a new row in that guide's interpretation table.
  - AC-9 requires every new factual clause to trace to the workflow. This clause traces only in part.
  - The safety rule ("record it as skipped, not as passed") still holds, so the defect is in the
    stated cause, not in the handling.
  - The plan fixes the exact text, and Stage C applies it exactly. So the fix belongs in the plan,
    not at Stage C.
- **Required in rev2:**
  1. Reword C-7 so that a reader checks `changes` first. Suggested text, which the planner may adapt:
     "| An advisory job is skipped | Check the `changes` job first. If it failed or was cancelled,
     every job that needs it is skipped too, and that failure is the finding to fix. Otherwise the
     path filter did not select the job for this pull request. Either way it did not run: record it
     as skipped, not as passed. The post-merge run on `main` runs it. |"
  2. Add a W9 row to §4.1 with this rule and its source.
  3. Extend AC-9's trace to cover W9.
  4. C-2 and C-4 may stay as written. They describe selection, not the cause of a skip.
  5. The README row (C-8) and Part B's B-3 state no cause, so they are unaffected.

## 2. Non-blocking findings and nits

The planner may fold these into rev2. None of them blocks on its own.

- **N-1, E6 overstates the duration effect (MINOR).** E6 says the three jobs "start only after
  `changes` finishes, so a run's workflow-level duration is no longer approximately the slowest
  single job plus queue".
  - On a docs-only pull request, the usual case, all three are skipped. The approximation still
    holds there.
  - When they do run, the change is that the slowest path now begins with `changes` and can wait
    for a runner twice.
  - Suggested wording: "when they run, they start only after `changes` finishes, which adds that
    job and a second runner wait to the run's longest path."
  - The rest of E6 is accurate: six jobs, the conditions, the merge time, the window end, step 4
    and the skipped-row exclusion. I checked each item against the workflow at `c060a7cb`, the
    GitHub API (`merged_at` `2026-10-06T01:29:57Z`) and figures `:267`, `:282`.
- **N-2, the first use of "PR" in E6 is not expanded (NIT, `CONTRIBUTING.md` readability rule 2).**
  - `grep -n -i 'pull request (PR)'` over the figures page finds nothing, and the only existing
    "PR" is at `:330`.
  - E6's "PR #676" would become the page's first use.
  - Suggested fix: "Pull request #676".
- **N-3, K12's recorded maximum line length is off by one (NIT).**
  - Measured by `python3`: the longest E3 line is 77 characters and 77 bytes ("nothing. Like the
    notes above, it moves…").
  - The plan records 78.
  - The ≤ 80 bound still holds.
- **N-4, K13's W7 item fails under the stated method (NIT).**
  - Collapsing whitespace alone does not join the workflow comment across its `#` line break. My
    run of K13 returned 0 for W7 and the expected count for every other quotation.
  - W7 is not quoted in any E-text: C-6 paraphrases it. So AC-8 is unaffected.
  - Fix: strip comment markers for W7, or drop W7 from K13.
- **N-5, R-7's precedent does not fit (NIT).**
  - #638 (3/2) and #649 (2/2) total 9 changed lines since `640f87b9`
    (`git diff --numstat 640f87b9 c060a7cb -- docs/offline-ci.md` → `5 4`). That is under the
    10-line rule, so neither PR changed the page's status.
  - FU-1 alone is 32/8 and does change it.
  - Not recording the change in the ledger is still defensible, for three reasons:
    - The ledger declares its own count a stale floor (`:42-48`).
    - The pull request body's disclosure meets `CONTRIBUTING.md` rule 6.
    - Writing the page path into the ledger would need harvester-safe wording.
  - Restate the reason; the precedent is the wrong one.
- **N-6, the combined pull request's class is not stated (NIT).**
  - `PLAN-B-rev1.md` §2 sets Part B's governing class to ai-agentic.
  - Stage E selects validation depth from the class of the combined pull request, which is the
    riskier one.
  - One sentence in §1 saying so would make `SD-A`'s classification complete for the combined
    pull request.
- **N-7, "since it left `main`" in C-2 (optional).**
  - On a `pull_request` event the job diffs the checked-out test-merge commit against the freshly
    fetched base. `origin/${BASE_REF}...HEAD` is at `:93`.
  - "The paths the pull request changes against `main`" is slightly more exact.
- **N-8, the brief asked for ETA reporting (process).** The plan says its own ETA was not stated
  at start. It records that gap honestly.

## 3. Checks the brief asked for

| Item | Result | Evidence (command and output) |
| --- | --- | --- |
| Item 1 problem real | **Yes** | D73 row 2 (`step-0…:3815`): (e) rejects "any row whose offline checks (commit, blob ID, identifiers) fail"; (d) allows a lost commit "as an event of its own kind". IMPL-AUDIT-3 m-1 quotes the same text. |
| Item 2 problem real | **Yes** | D73 "Not decided here" (`:3851-3856`) lists 3 items; row 2 (c) and its Source cell say "Open (withdrawing a targeted-review row)". AEGIS-APR-113 "Not decided by this entry" (`APPROVAL_REGISTER.md:4797-4804`) lists 3. |
| Item 3 problem real | **Yes** | Ledger `:92-96` lists "Both deserve an owner ruling…" as answered. The answer covers only point (1) of `:3391-3398`. D73 row 8 leaves the preservation mechanism open. |
| Item 4 problem real | **Yes** | PR #678 body (GitHub MCP `pull_request_read get`): D rows for rounds 1–2 only, E rows for rounds 1–2 only, no F row. |
| Vehicle, items 1–2 (D73) | **Sound** | D73's rule for Audit-labelled conditions (`:3805-3806`): "a later plan changes it only by a dated note here". The inline-correction convention has 5 precedents (`grep -c 'Correction (appended'` → 5; D34 `:1534`, D57 `:2808`). §6 is newest-first (`:24-25`). E1 is a clarification compatible with both readings IMPL-AUDIT-3 m-1 allowed. It binds nothing if the tool-repair plan records lost commits in the report instead. |
| No register note (item 2) | **Sound** | Preamble `:8-10`: "do not edit old entries". The AEGIS-APR-086 correction block was made under the AEGIS-APR-099 grant. The FU-2 rule also says FU-1 adds no entry. Both reviewers called the register optional. |
| Vehicle, item 3 (ledger) | **Sound** | The ledger's Correction precedent, "**Correction (appended 2026-10-03).**" (`:3400`), sits at the end of the note it corrects, as E3 does. The 2026-10-07 note's 92 lines (19–110) stay contiguous and byte-identical. Diff hunk: `@@ -110,0 +111,25 @@`. |
| New fact about `e6fc8d24` | **Verified, complete** | `git ls-remote origin refs/heads/docs/readability-batch-b 'refs/pull/625/head'` → both `e6fc8d24…08e` (14:37Z). `git merge-base --is-ancestor … origin/main` → exit 1. Containment over all refs: local branches equal the remote (634 = 634, `diff` empty), and `for-each-ref --contains` gives only `origin/docs/readability-batch-b`. I fetched all 677 `refs/pull/*/head` into a separate scratch bare repository (main repository objects as alternates; nothing written to the main repository): `--contains` gives only `refs/pull/625/head`. There are no tags. So "can be fetched only while one of those references exists" is true today. It agrees with D73 row 5: "A commit still held by a pull-request head is not lost". |
| Item 4 "no repo change" | **Sound** | Merge receipt comment 6050309870 (`created_at` = `updated_at` = 01:30:25Z) has "### Aegis skills used" pointing to 6049874529 (D3), 6049912717 (E3) and 6050266060 (F) with their skills. `delivery-workflow.md:484-485` says merge-stage usage goes in the merge receipt. Editing the merged body would void the receipt's recorded hash `995807705e5a6a59`. |
| Nits n-1 / n-a / n-b | **Sound** | n-1 is excluded because rewrapping deletes dated text. n-a: the quote is inside AEGIS-APR-113 (heading `:4558`, quote `:4680`). n-b: "four rows" appears three times at base (banner, `:237`, `:239`). The table had 4 rows at `5c806348`, `d10f6319` and `7d1d05e8` (`git show` + `awk`). |
| Part C against the workflow | **Correct except B-1** | Read `git show origin/main:.github/workflows/validate-skills.yml`. W1–W8 match: jobs at `:56/105/271/361/411/467`; `needs`/`if:` at `:274-275/362-363/412-413`; `gate-guard` `if:` at `:476`; DCO step PR-only at `:254`; timeouts 5/15/20/15/20/5; flake comment at `:64-65`. Required checks via `gh api …/branches/main` → `gate-guard`, `validate-skills` only, so C-3's "Not registered as required" is right. Live run 37709031628 (PR #678): `changes`, `gate-guard` and `validate-skills` success; the three advisory jobs skipped. Push run 37713171379 (main at `c060a7cb`): `gate-guard` skipped and all other jobs ran, which confirms C-2's and C-4's push statements. |
| In-place or dated note, per page | **Right on all four** | `offline-ci.md` is living text: no dated banners, and in-place corrections by #638 and #649 (`git log`). The figures page is a pinned window (`:266-267`), and its rule 5 gives the dated note. The control-plane backlog `:257` is under "## 4. Historical validation and delivery protocol" (`:218`), written in `9e3db619` on 2026-09-12, so it is left unchanged. The README is living. |
| Part B B-3 consistency | **Consistent** | B-3's template text and the plan's C-1, C-2, C-8 state the same four rules: `validate-skills`/`gate-guard` on every pull request to `main`; Windows on `tools/` or either lock file; tools tests on `tools/`; skipped is not passed. On a push, this plan says "every job except `gate-guard`" (correct, `:476`). Part B's R5 says "everything on a push to `main`", which is loose, but that sentence is in Part B's plan, not its template text. |
| Harvester safety (K11/K12 re-run) | **Holds** | `build_index.py --repo <wt> --ref HEAD --candidates` in my own base and head worktrees: exit 0, empty stderr. (a) Counts identical (675/1/65/609/609/437/172/3/489/433/43/13). (b) Identical after normalising the ledger line numbers. (c) 0 of 56 ledger references fall in 111–135. The 43 tracker references shift by +25. The 13 stated-acceptance labels stay unchanged, as E3's Self-cost says. K12: ACCEPT 0, RETENTION 0, BARE_SHA 0, SHA 0, MD_LINK 0, backticked `.md` 0, table rows 0; max 77. The harvester reads only the ledger and `docs/evidence/documentation/` (`build_index.py` constants), so the other five files cannot harvest. |
| Readability cost disclosed | **Yes** | `offline-ci.md`: `git diff --numstat 640f87b9` at the dry-run head → `37 12`, more than 10, so it returns to pending. No added heading (`grep -c '^+#'` → 0). The index rows for the six pages agree with the plan's §4.3 (`acceptance-index.json`). README `f1bfaece..c060a7cb` → `520 131`; decision log `6488eaa0..c060a7cb` → `892 24`. AC-14 discloses this. |
| Readability rules for new text | **Met except N-2** | Codes are explained (m-1, m-2, D73). Counts name their method (E3 Self-cost, E6 step 4). Every dated note carries date and revision. Table cell counts are correct (pipe count 3/5/3/3 for 2/4/2/2 columns). |
| No owner attribution | **Met** | Every added line mentioning the owner either quotes repository text ("deserve an owner ruling") or restates D73 row 8. No owner words are invented, and nobody is named. |
| AC/K mechanical | **Yes** | See §4 and §5. |
| FU-2 overlap | **None** | Plan paths: `README.md`, `docs/offline-ci.md`, decision log, coordinator figures, ledger, open-decisions. FU-2's declared paths: register, `docs/audits/*`, `artifacts/audits/*`, `library-diff-reviewer/evals/trigger-evals.json`. No path is shared. FU-2's branch is not on the remote yet: `git ls-remote origin 'refs/heads/claude/sharp-lovelace-urgxpz*'` shows only the merged head `3797739c`. E1, E3 and E4 cite no register line numbers, so register appends cannot stale them. P-1 covers a moved base. |
| Codex trigger phrase | **0** | `grep -c -i` with the needle built by concatenation, over the plan, E-files and dry-run diff → 0 each. This file contains none. |

## 4. Acceptance criteria (`acceptance-criteria-reviewer`)

| AC | Verdict | Note |
| --- | --- | --- |
| AC-1 to AC-8 | TESTABLE | Each names its outcome, threshold and command (K9, K11–K14, K18). |
| AC-9 | **NEEDS-REWRITE** | It becomes TESTABLE once W9 is in the trace (B-1). |
| AC-10 | TESTABLE (declared UNRUN until Stage E, with reason) | It names the expected skipped set. It is restated if FU-1 touches `tools/` or a lock file. |
| AC-11 to AC-15 | TESTABLE | AC-13's live leg is declared for Stage D/F. |

- **Gap, error class:** no criterion checks that the C-texts cover a non-filter skip. B-1 closes
  this.
- **Contradictions:** none.
- **Declarations:** every criterion that cannot be checked at this head is declared, with its
  reason, as `SD-A` requires.

## 5. Re-run results (my own worktrees at `c060a7cb`, dry run applied with the plan's script)

- **Dry run reproduces:** `cmp` of my diff with `plan-a-dryrun.diff` → identical, sha256
  `9f647e33…`. Numstat: `1 0`, `32 8`, `28 0`, `19 0`, `25 0`, `2 0`.
- **Embedded copies:** the E1–E4 and E6 blocks are byte-identical to their files. Each C-block's
  old text occurs once at the base and its new text once at the head.
- **Local suite, Python 3.13.16:**
  - K1: `OK: 195 skill(s) valid, 0 warning(s)`.
  - K2: `OK: 181 gate self-test assertion(s) passed.`
  - K3: `OK`.
  - K5: `OK (skipped=1)`.
  - K6: `OK: 76 contract-audit self-test assertion(s) passed.`
  - All exit 0.
- **K4 link check:** base 619 / 3221 / 871 / broken 0 / dead 0; head 619 / 3223 / 872 / 0 / 0.
- **K8 guard pattern:** 0 of 6 paths match. Controls behave as expected: `tools/__init__.py`,
  `.github/workflows/x.yml` and `scripts/a.md` match; `.github/pull_request_template.md`,
  `docs/x.py`, `README.md` and `docs/offline-ci.md` do not.
- **Other checks:** K16 `git diff --check` exit 0. AC-15 grep → 0. CR bytes in added lines → 0.
- **K10 at base:** `check_index.py --json --ref c060a7cb…` → 602 / 436 / 212 / 159 / 224 / 7,
  "NOT DERIVABLE from this procedure". The head leg needs Stage C's commit.

## 6. Observations for the coordinator (outside this plan; no change requested here)

- **O-A, main's push run at `c060a7cb` is red.**
  - Run 37713171379 (push, attempt 1, `conclusion: failure`): `validate-skills` failed in "Check
    CI evidence and protected-path handling".
  - The error was `test_offline_ci.py` → `OSError: [Errno 39] Directory not empty:
    '/home/runner/work/_temp/aegis-ci-guard-…/repo'`, raised in `TemporaryDirectory` cleanup
    (job log 113103554440).
  - The same tree `0c5a2400…` passed on the pull-request run 37709031628, so the failure is
    non-deterministic.
  - No second attempt exists (`/attempts/2` → 404).
  - FU-1's own run executes the same test. A `ci-failure-classifier` pass and a re-run decision
    belong to the coordinator, not to this stage. This is not the flake signature C-6 documents.
- **O-B, the auto-merge policy may conflict with path scoping.**
  - `docs/reconciliation/auto-merge-policy.md:23-24`, the dated owner-policy reading of 2026-09-23,
    requires "passing Linux and Windows jobs" for a guard-failure exception.
  - Since #676, a pull request that fails `gate-guard` only through `scripts/` or `.github/`
    skips the Windows job, so that condition cannot be met as written.
  - This is dated owner policy. It is not FU-1's to edit, and I suggest adding it to the plan's
    O-list for the owner.

## 7. Not done, and limits

- No repository edit, commit, push, pull-request action, comment or GitHub write.
- Local work was confined to scratch worktrees `…/fu1/auditA/wt-base`, `wt-head` and a scratch bare
  repository `…/fu1/auditA/probe.git`. The probe uses the main repository's object store as an
  alternate and holds the fetched pull-request refs. The main checkout stayed clean
  (`git status --short | wc -l` → 0).
- I did not audit Part B's template text beyond the B-3 cross-check.
- The CI-only Python 3.14 leg is not run here.

## 8. Timing

- **Item:** FU-1 Parts A+C, Stage B plan audit, rev1.
- **ETA:** I stated none at start, which is a gap. The plan estimated this stage at 20–35 minutes.
- **Start:** 2026-10-08T14:34:01Z (`date -u`). Finish and measured wall time are in the hand-off
  report.
- Active time was not measured separately.
