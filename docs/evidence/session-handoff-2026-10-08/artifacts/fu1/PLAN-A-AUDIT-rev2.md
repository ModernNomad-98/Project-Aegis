# FU-1 Parts A and C — Stage B INDEPENDENT PLAN AUDIT, round 2

**`SD-B: ACCEPT`** on `PLAN-A-rev2.md`, sha256
`0eff1f77e3d395ff90eeb22becb32a590242fa5a377b9e4c03eb5769c768b17f`. The hash was the same when I
started (2026-10-08T15:05:45Z) and before I wrote this verdict (15:10:05Z). Editing the plan
afterwards voids this ACCEPT.

**The verdict binds these inputs.** Each sha256 below was recomputed by me:

- `plan-a-text-rev2/`:
  - E1 `62f6c381…33bd1`, E2 `d41453ae…b30a4`, E3 `71e27df3…852c5a` and E4 `ef3f9ad9…69ac`. Each is `cmp`-identical to its rev1 file.
  - E6 `81cfb03d…84f5`, which is new.
- `tools-local/apply_plan_a_rev2.py` `30d21143…ed3d`.
- `plan-a-rev2-dryrun.diff` `fc979b84…1e8b`.
- Part B's accepted text, `planB/template.proposed.rev2.md` `cfc26e12…1346`. It is the file that
  `PLAN-B-AUDIT-rev2.md`'s `SD-B: ACCEPT` names. `PLAN-B-rev2.patch` (`dfe9af12…0e9c`) passes
  `git apply --check` at the base.

**Auditor and scope.** I am the same Stage B agent as round 1. I did not write, implement,
validate, review or merge this change. **Base:** `git ls-remote origin refs/heads/main` →
`c060a7cb09758fa2f4f6b67ab00094f01d7c6a46`.

## 0. Aegis skills used (Stage B, round 2)

| Skill | Stage / agent | How applied | Result |
| --- | --- | --- | --- |
| [`acceptance-criteria-reviewer`](https://github.com/ModernNomad-98/Project-Aegis/blob/main/.claude/skills/acceptance-criteria-reviewer/SKILL.md) (partial fit, per `docs/delivery-workflow.md`'s stage map) | B / Part A+C plan auditor | I re-checked AC-9 and AC-11 and the new K19 and K20 for outcome, threshold and evidence. | AC-9 is now TESTABLE. All 15 criteria are TESTABLE, and the four that cannot run yet are declared not verifiable at this head, with reasons. There are no gaps and no contradictions. |
| [`source-of-truth-reconciler`](https://github.com/ModernNomad-98/Project-Aegis/blob/main/.claude/skills/source-of-truth-reconciler/SKILL.md) | B / Part A+C plan auditor | I re-read the platform rule at its source (W9, C10). I checked the new Part C clauses against the workflow, which wins under precedence rule 2 for IS-questions. | Correct. Live state still matches. |

No MANUAL-ONLY skill was used. The plan-level verdict is procedural, because no skill owns it.

## 1. B-1, W9, AC-9 and K20

- **The GitHub rule, which I re-read today with WebFetch:**
  - Workflow syntax, `jobs.<job_id>.needs`: "If a job fails or is skipped, all jobs that need it
    are skipped unless the jobs use a conditional expression that causes the job to continue." The
    same section says: "If you would like a job to run even if a job it is dependent on did not
    succeed, use the `always()` conditional expression in `jobs.<job_id>.if`."
  - Expressions, status check functions: "A default status check of `success()` is applied unless
    you include one of these functions."
  - W9 quotes all three correctly.
- **K20 against the workflow**, read with `git show origin/main:…validate-skills.yml`. This file is
  identical to my round-1 copy (`cmp`).
  - The three job-level `if:` lines (`:275`, `:363`, `:413`) contain no status function, and each
    job has `needs: [changes]` (`:274`, `:362`, `:412`).
  - The only `always()` hits are at `:263`, `:347`, `:403` and `:459`. All four are step-level,
    indented 8 spaces.
- **B-1 is resolved.** The new C-7 row tells the reader to check `changes` first and names both
  causes of a skip. It keeps "record a skipped job as skipped, not as passed". Changing "runs it"
  to "selects it" is the more exact claim under W9.
- **AC-9's trace now covers W1–W9.** K15 includes rev1's cause-only wording, which is now 0 at the head.

## 2. All seven changed Part C hunks and E6, re-read

| Hunk | Verdict | Check |
| --- | --- | --- |
| C-1 | Correct | It states B-3's sentence S1 verbatim. "runs only when …" states a necessary condition, so it stays true under W9. "The pull request's latest commit (its head)" matches the next sentence, "A later push starts new checks". |
| C-2 | Correct | The selection rules match the regexes at `:94` and `:99`. "Against `main`" fixes N-7. The added dependency sentence matches W9, and the [Reading a failure](#reading-a-failure) anchor resolves (K4). |
| C-3 | Correct | The new cell matches W9. The row has 4 cells (pipe count 5). |
| C-4 | Correct | It now carries S2. "runs every job except … `gate-guard`" describes the design on a push (`:85-86`, `:476`). The push run 37713171379 confirms it. |
| C-5 | Correct | "whenever they run" no longer names a single cause. |
| C-7 | Correct | See §1. The row has 2 cells (pipe count 3). |
| C-8 (README) | Correct | It carries S1 and S2 verbatim. The `docs/offline-ci.md#reading-a-failure` link resolves. The row has 2 cells. |
| E6 | Correct | N-1: "their path through the run includes that job and a second wait for a runner". This claims only what the workflow implies. N-2: "Pull request #676"; the page's first "PR" is still the existing one at `:349`. The longest line is 77 characters. |

**Verbatim alignment with Part B (K19).** I collapsed whitespace and counted three sentences: S1
(the job-condition sentence taken from the template itself), S2 ("Record a skipped job as skipped,
not as passed.") and S3 ("the pull request's latest commit (its head)").

| File | S1 | S2 | S2, lower-case | S3 |
| --- | --- | --- | --- | --- |
| template | 1 | 1 | 0 | 1 |
| `offline-ci.md` | 1 | 2 | 1 | 1 |
| `README.md` | 1 | 1 | 0 | 0 |

These counts are exactly the ones the plan states.

## 3. N-1 to N-8 dispositions

| Finding | Status | Evidence |
| --- | --- | --- |
| N-1, N-2 | Fixed | See the E6 row in §2. |
| N-3 | Fixed | K12 now records 77. I measured 77 too. |
| N-4 | Fixed | With YAML comment markers stripped, the W7 quote count is 1. |
| N-5 | Fixed | R-7 now gives the three reasons and drops the #638/#649 precedent. |
| N-6 | Fixed | §1: the combined pull request takes Part B's ai-agentic class. |
| N-7 | Fixed | C-2 now says "against `main`". |
| N-8 | Recorded honestly | The plan again records that no ETA was stated at the start. |

The plan also records O-A as R-10 and O-6, and O-B as O-7. The plan is right not to act on either.
Run 37713171379 still reads `run_attempt 1`, `completed`, `failure` at 15:09Z.

## 4. Nothing else changed

- **Plan text.** I diffed rev1 against rev2. Every changed line falls under an item in rev2's
  finding table, or is a figure refreshed from the rev2 dry run. Those figures are:
  - `offline-ci.md` numstat: 36/8 in this change, and 41/12 since `640f87b9`;
  - dry-run totals: +111/−8;
  - K4 anchors: 874;
  - K14: re-measured.
- **Apply scripts.** `diff` between the rev1 and rev2 scripts shows only the C-1, C-2, C-3, C-4,
  C-5, C-7 and C-8 strings and the docstring. E1–E4 and the C-6 string are unchanged.
- **Dry run.** My own apply in fresh worktrees reproduces `plan-a-rev2-dryrun.diff` byte for byte
  (`cmp`, sha256 `fc979b84…`). The Part A hunks (decision log, ledger, open-decisions) are
  byte-identical to rev1's dry run. Every embedded `~~~~text` block matches its file. Each C-block's
  old text occurs once at the base and its new text once at the head.

## 5. Re-run checks (Python 3.13.16, my scratch worktrees)

- **K11** (`build_index.py --candidates`):
  - exit 0 and empty stderr, at base and head;
  - both outputs are byte-identical to my round-1 outputs (base `6c0648d3…`, head `960c7b8c…`,
    the hashes the plan states);
  - (a) counts identical, (b) identical after normalisation, (c) 0 of 56 references fall in lines 111–135.
- **K12:** every pattern 0, 0 table rows, longest line 77.
- **Local suite:** K1, K2, K3, K5 and K6 return their expected summaries, all exit 0.
- **K4:** 619 files, 3223 links, 874 anchors, broken 0, dead 0.
- **K8:** 0 of 6 paths match.
- **K13:** every count as the plan states, and W7 is 1.
- **K14** (15:09Z): both refs hold `e6fc8d24…`. `git merge-base --is-ancestor` exits 1.
- **K15:** all five strings 0. No heading added. The job table has 6 rows, with timeouts 5/15/20/5/15/20.
- **Other checks:** K16 exit 0. K17 0. AC-15 0. No CR bytes.

## 6. Non-blocking nits

Stage C must not apply these, because the plan text is exact.

- C-2's "The three selected jobs need `changes`" would read more clearly as "The three advisory
  jobs". The meaning is clear in context.
- C-4 and C-8 describe the post-merge run by design ("runs every job except `gate-guard`"), while
  C-7 uses the more exact "selects". C-2's dependency sentence covers the difference.

## 7. Not done

- I made no repository edit, commit, push or GitHub write.
- I did not audit Part B's template beyond checking it against B-3.
- The scratch worktrees `…/fu1/auditA2/wt-base` and `wt-head` are removed after this file is written.

## 8. Timing

- **Item:** FU-1 Parts A+C, Stage B round 2.
- **ETA:** I stated none at the start, which is a gap. The plan estimated this stage at 10–20 minutes.
- **Start:** 2026-10-08T15:05:45Z (`date -u`). The finish time and measured wall time are in the
  hand-off report.
- Active time was not measured separately.
