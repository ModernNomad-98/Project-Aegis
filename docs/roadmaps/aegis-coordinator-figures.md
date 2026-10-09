# Project Aegis coordinator figures — tracked home, and the check-duration baseline

**This page is the tracked home for the coordinator's figures** (`PROC-12`) and
carries **the maintained baseline table of check durations** (`PROC-11`) as its
first landed figure set. Both rules are recorded in the
[process issues and prevention register](../evidence/documentation/process-issues-and-prevention-2026-10-02.md);
this page is the artifact that discharges them.

**Reading key.** A **job** is one named unit of work inside a continuous
integration (CI) run; a **workflow** is the whole run that contains the jobs. A
**runner** is the machine that executes a job. **UTC** is Coordinated Universal
Time, and every timestamp and duration on this page is UTC compared with UTC. A
**percentile** is the value at or below which a given share of samples fall;
**p90** is the 90th percentile and **p95** the 95th. **Dependabot** is GitHub's
dependency-update bot. `PROC-11` and `PROC-12` are stable rule identifiers from
the register above.

**Measurement status, 2026-10-08.** The 296-run table and its decision rule
below describe a historical pre-#676 workflow. Section 3.5 records a separately
measured, historical pre-CIFIX job-duration window after #676. Neither window
is an accepted current post-CIFIX baseline or a new alert rule. Post-CIFIX
performance is **NOT SAMPLED** here.

---

## 1. Why this page exists

Two register rules were owed a tracked artifact, and one artifact discharges
both.

- **`PROC-12` — the coordinator's own estimates are the least reliable input.**
  A coordinator's figures live in a briefing, and a briefing is session state.
  When one of those figures turns out to be wrong there is no artifact to
  correct and no page that owns it, so the same wrong figure is repeated in the
  next session. The remedy is a **tracked home**: a page in the repository that
  a coordinator's figure must be landed in before anyone may rely on it.
- **`PROC-11` — never call a duration anomalous without a measured baseline.**
  The trigger instance was a false "stalled job" alarm raised on
  `tools-tests-windows`, judged from one or two samples because no normal
  duration had ever been measured. A baseline had never been needed, so it had
  never been taken.

Read as a pair: **the home holds the figures, and the rule for entering it is
that a figure is re-derived before it is trusted.**

## 2. How a figure gets into this page (the `PROC-12` rule)

A figure supplied in a briefing, a chat message, a plan or a summary is a
**claim**, not evidence. It enters this page only through this gate:

1. **Re-derive it.** Run your own query against the repository or the API. A
   figure restated from the briefing is not re-derived.
2. **Land the measured value, not the briefed value.** Where the two disagree,
   this page carries the measurement and says so explicitly.
3. **Record the command, the revision and the date** beside the figure, so a
   later reader re-runs the query instead of trusting this page.
4. **If it cannot be re-derived, record it as `unknown`** with what would
   resolve it. Do not upgrade it to "probably fine" and do not delete it; a
   figure that is absent from this page cannot be cited by the next session.
5. **Never land a figure on the strength of a briefing alone**, and never edit
   a landed figure without re-running its command.

This is why every table below names the level it measured, the percentile
method it used, the sample size and the regeneration command. A figure without
those four things is not maintainable, and a page that cannot be maintained
becomes the next stale briefing.

## 3. `PROC-11` — the measured check-duration baseline

### 3.1 What is measured, exactly — two quantities that are not interchangeable

| Quantity | Definition | Includes runner queue time? | Used here |
| --- | --- | --- | --- |
| **Job-level duration** | `job.completed_at` − `job.started_at`, both UTC | **No** — starts when the runner begins executing the job | **Yes — this is the baseline table** |
| Workflow-level duration | `run.updatedAt` − `run.createdAt`, both UTC | **Yes** — includes waiting for a runner and the fan-out across all five jobs | Reference only, §4 warning 4 |

All five jobs live in the single workflow file [`.github/workflows/validate-skills.yml`](../../.github/workflows/validate-skills.yml).
Job declarations and their declared limits, read from that file:

| Job | Runner | Declared limit | Gate condition |
| --- | --- | --- | --- |
| `validate-skills` | `ubuntu-latest` | 900 s (15 min) | — |
| `windows-offline-checks` | `windows-latest` | 1200 s (20 min) | — |
| `tools-tests-linux` | `ubuntu-latest` | 900 s (15 min) | — |
| `tools-tests-windows` | `windows-latest` | 1200 s (20 min) | — |
| `gate-guard` | `ubuntu-latest` | 300 s (5 min) | `if: github.event_name == 'pull_request'` |

**Dated note, 2026-10-08: the workflow changed after this window.**
Re-derived with step 4 of [§6](#6-regeneration--exact-commands) against
`origin/main` at `c060a7cb` on 2026-10-08: the workflow now declares **six**
jobs. Pull request #676 (merged 2026-10-06T01:29:57Z, after this baseline's
pinned window ended) added `changes` (`ubuntu-latest`, 300 s / 5 min), which
reads a pull request's changed paths. `windows-offline-checks` now carries
`needs: [changes]` and
`if: github.event_name == 'push' || needs.changes.outputs.offline == 'true'`;
`tools-tests-linux` and `tools-tests-windows` carry `needs: [changes]` and
`if: github.event_name == 'push' || needs.changes.outputs.tools == 'true'`.
The table above, "five jobs" in §3.1 and §3.3, and warning 4's "The five
jobs also run in parallel" describe the workflow during the pinned window and
stay as measured. A later window differs in two ways: a skipped job is
excluded from the sample (step 2), so those three jobs have fewer samples;
and when they run, they start only after `changes` finishes, so their path
through the run includes that job and a second wait for a runner. That
second point is read from the workflow, not measured, and this note lands no
duration figure. The [CI guide](../offline-ci.md) states when each job runs.

### 3.2 The historical baseline table (job level, seconds)

Primary sample: every non-`skipped` job with both timestamps, success **and**
failure, all events.

| Job | n | min | **median** | p90 | p95 | max | mean |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `validate-skills` | 296 | 18 † | **104** | 114 | 119 | 164 | 102.8 |
| `windows-offline-checks` | 296 | 129 | **220** | 238 | 245 | 412 | 211.8 |
| `tools-tests-linux` | 296 | 89 | **148** | 162 | 213 | 379 | 151.8 |
| `tools-tests-windows` | 296 | 120 | **222** | 239 | 245 | 277 | 212.2 |
| `gate-guard` | 191 ‡ | 4 | **6** | 8 | 8 | 45 | 6.5 |

† **The 18 s minimum is not a healthy floor.** It is the single **failed**
`validate-skills` job, which aborted early. Success-only, that job's minimum is
**62 s**, and 62 s is the healthy floor to quote. Every other row's min and max
are unchanged when failures are excluded, and the `gate-guard` maximum of 45 s
is a **successful** run, not a failure artifact.

‡ `gate-guard` has `n = 191` because 105 of the 296 runs report it as `skipped`.
See warning 2 in §4.

Sample window: run ids `36620909745` → `37090194553`; dates
`2026-09-29T19:40:27Z` → `2026-10-03T02:33:04Z` (3.3 days). The window is the
300 most recent runs the API returns, minus 4 unrelated `Dependabot Updates`
runs, leaving 296 `validate-skills` runs and 1,480 job records
(1,370 `success`, 5 `failure`, 105 `skipped`).

### 3.3 Percentile method — stated, not implied

**Nearest-rank, no interpolation.** For ascending-sorted values `x[0 .. n−1]`:

```text
p-th percentile = x[ ceil(p/100 × n) − 1 ]        # 1-based rank, clamped to n
```

For even `n` the median is therefore the **lower-middle** element, not the
average of the two middle elements. Cross-check: the standard interpolated
median agreed exactly with the nearest-rank median for all five jobs, so the
choice of definition changes no headline figure here. Ranks used: `n = 296`
gives median rank 148 and p90 rank 267; `n = 191` gives median rank 96 and p90
rank 172.

**Dated wording correction, 2026-10-08.** The earlier "upper-middle" wording
contradicted the unchanged formula: rank 148 of 296 is the lower of the two
middle observations. The percentile rank is one-based; `x[rank - 1]` is a
zero-based array subscript (147 for rank 148). This corrects the explanation,
not the historical figures. Their raw observations were not re-read for this
wording change.

### 3.4 The historical decision rule this baseline supported

**Historical only:** this rule was derived for the 296-run pre-#676 sample. It
has not been recalibrated from the small §3.5 window and must not be applied as
a current post-CIFIX threshold.

| Job | Normal (do not comment) | Slow but expected | Worth a look | Job dies at |
| --- | --- | --- | --- | --- |
| `validate-skills` | ≤ 119 s (p95) | 120–164 s | > 164 s | 900 s |
| `windows-offline-checks` | ≤ 245 s (p95) | 246–412 s | > 412 s | 1200 s |
| `tools-tests-linux` | ≤ 213 s (p95) | 214–379 s | > 379 s | 900 s |
| `tools-tests-windows` | ≤ 245 s (p95) | 246–277 s | > 277 s | 1200 s |
| `gate-guard` | ≤ 8 s (p95) | 9–45 s | > 45 s | 300 s |

Read it as: **only a duration beyond the observed maximum of this 296-run
window is a candidate anomaly.** p95 is the routine-noise ceiling. A green job
anywhere in the first two columns is normal, and citing it as a stall is the
error this page exists to prevent.

### 3.5 Historical pre-CIFIX window after #676 (job execution, seconds)

**Status and use.** These are source-verified historical figures for maintainers
reconciling the workflow change, not an accepted operating baseline or evidence
that #676 improved durations. Fresh read-only GitHub Actions metadata were
retrieved on 2026-10-09 UTC and checked against all 27 request receipts and the
frozen source pins. A separate independent implementation audit remains pending.
The Stage C implementer authored the fixed GET-only collector; the coordinator
executed that unchanged script after direct owner approval and automatic review
acceptance, and the implementer verified and adopted its responses. This
execution split departed from `AGENTS.md`'s Role A coordinator-only rule and
is disclosed as a stage-handoff deviation, not counted as an independent Stage D
collection.
The [normalized attachment](../evidence/metrics/metrics-1-ci-duration-2026-10-08.json)
preserves the source operands, all run and job records, original timestamps,
cutoff witnesses, exclusions, request receipts, sums and percentile ranks.
Its SHA-256 is `0a592b341f04814ed272b3a5510e5ff1b747a74fbdfef1b0e58fdefbb5f30f8d`.

The frozen half-open run creation window is
`2026-10-06T01:29:57Z <= created_at < 2026-10-08T19:36:00Z`.
The primary population is **attempt 1 of main pushes** whose head lies from
#676's merge `03c93c77` through pinned main `52289779` and matches the pinned
workflow and offline-test blobs. The five qualifying runs are 37399467224,
37672991237, 37713171379, 37804698446 and 37807051981. The fresh API
retrieval returned 12 workflow runs in two matching one-page censuses: five
main pushes and seven pull-request diagnostics, with no other exclusions.
All 72 unique attempt-1 job records are retained. This is a census of the
**API-retrievable** rows at that retrieval time; it cannot establish whether
any historical run had already been deleted.

Only success or failure jobs from a terminal attempt before the cutoff, with
valid start and completion timestamps before it, enter a primary duration
vector. Duration is `completed_at - started_at`; runner queue time and whole-run
elapsed time are outside this table. Skipped jobs have **no duration**, even
when the API reports placeholder timestamps. A retry contributes nothing to
attempt 1. This differs from the older all-event, "non-skipped" sample, whose
attempt semantics were not specified; the two tables are not a controlled
before-and-after comparison.

| Main-push job | n | success/failure | min | median | p90 | p95 | max | exact sum | mean |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `changes` | 5 | 5/0 | 4 | 5 | 8 | 8 | 8 | 27 | 5.4 |
| `validate-skills` | 5 | 4/1 | 20 † | 95 | 108 | 108 | 108 | 392 | 78.4 |
| `windows-offline-checks` | 5 | 5/0 | 137 | 179 | 250 | 250 | 250 | 947 | 189.4 |
| `tools-tests-linux` | 5 | 5/0 | 98 | 149 | 157 | 157 | 157 | 701 | 140.2 |
| `tools-tests-windows` | 5 | 5/0 | 163 | 215 | 238 | 238 | 238 | 1051 | 210.2 |
| `gate-guard` | 0 | 0/0; 5 skipped | NOT MEASURED | — | — | — | — | — | — |

† Attempt 1 of [run 37713171379](https://github.com/ModernNomad-98/Project-Aegis/actions/runs/37713171379)
failed after 20 seconds in `validate-skills`; its later successful attempt does
not erase this observation. A success-only companion for that job has `n=4`,
min 71, median 95, p90 108, p95 108, max 108, sum 372 and mean 93.0 seconds.
For the other four executed jobs, all five observations succeeded, so their
success-only figures equal their rows above. The failed 20-second minimum is
not a healthy floor.

The rows use the unchanged nearest-rank method in §3.3: rank
`min(n, max(1, (p*n+99)//100))`, with a one-based rank and zero-based array
subscript. For each `n=5` row, p50 rank is 3 and p90/p95 rank is 5. Means are
exact sum divided by `n`, displayed to one decimal with decimal half-even
rounding. For `n=0`, values are **NOT MEASURED**; with one observation all
quantiles would equal that observation.

The main-push denominator is 30 jobs: 24 successful measured, one failed
measured and five skipped `gate-guard` jobs. The five skips are supported by
the pinned workflow's pull-request-only condition. No main-push job had a
cancelled, timed-out, neutral, invalid-timestamp or cutoff-unresolved
disposition. For the seven PR diagnostics, the later retrieval recorded 21
successes and 21 advisory skips; their durations do **not** enter these
quantiles. Six PR attempts had terminal evidence before the cutoff. The
seventh, [run 37833100150](https://github.com/ModernNomad-98/Project-Aegis/actions/runs/37833100150),
was created at 19:35:31Z and its validation job completed at 19:37:25Z, after
the cutoff, so the attempt is **cutoff-unresolved** for this window. All 21 PR
advisory skip causes remain **unknown**: these metadata lack the actual runtime
filter outputs and proven PR checkout/workflow revision. `changes` success
alone does not establish a path-skip cause.

This short window cannot characterize weekends, later runner images, all PR
workloads or tail behavior; with `n=5`, p90 and p95 both select the maximum.
Post-CIFIX performance is **NOT SAMPLED**. No new timeout, anomaly threshold,
cost saving, CI improvement, or time-to-green forecast follows from this sample.

## 4. Warnings this page exists to carry

### Warning 1 — the `tools-tests-windows` false alarm, and why it is false by construction

A previous coordinator raised a **false "stalled job" alarm** on
`tools-tests-windows`, on the belief that this job legitimately takes 149–240 s
and that something above it was wrong. Measured, `n = 296`:

| Statistic | Value |
| --- | --- |
| min | 120 s |
| p05 | 150 s |
| p25 | 192 s |
| **median** | **222 s** |
| p75 | 230 s |
| p90 | 239 s |
| p95 | 245 s |
| max | 277 s |
| samples inside the claimed 149–240 s band | **260 / 296 = 87.8 %** |
| samples above 240 s | 23 / 296 = 7.8 %, all still ≤ 277 s |
| samples below 149 s | 13 / 296 = 4.4 % |

**The claimed band contains the median.** An alarm that fires inside
149–240 s will fire on roughly half of all healthy runs, so it is **false by
construction** — not merely imprecise. Against the job's declared 1200 s limit,
even the slowest observed run used 23 % of its budget.

> **Nothing below 277 s may be called slow.** The observed maximum of the
> window is the floor of defensibility, and a useful investigation threshold
> sits well above it.

### Warning 2 — `gate-guard` reporting `skipped` on a push to `main` is EXPECTED

- **105 of 296** sample runs report `gate-guard` as `skipped`.
- The skipped set is **exactly** the set of `push` runs, and every one of those
  pushes was to `main`: skipped = push set is true, the push-branch set is
  `{main: 105}`, and **zero** pull-request runs skip it.
- Root cause is in the workflow source: the job carries
  `if: github.event_name == 'pull_request'`, so it is by design not applicable
  to a `main` push.

**Do not count a skipped `gate-guard` as a pass or as a failure.** It is "not
applicable to this event". These 105 runs are excluded from the duration sample
— a skipped job has no honest duration — which is the only reason its row reads
`n = 191` rather than 296.

### Warning 3 — a 3.3-day window; min and max are window extremes, not bounds

The sample is the **whole population of that window**, not a random sample and
not a season: 296 runs covering **Tuesday to Saturday UTC**
(`2026-09-29T19:40:27Z` → `2026-10-03T02:33:04Z`, 3 days 6 h 52 m 37 s), taken
at roughly 90 runs per day. Two consequences:

- `min` and `max` are the observed extremes **of this window**. A later run can
  and eventually will fall outside them; that is not by itself a regression.
- Weekend and night-time runner-availability behaviour is **effectively
  unsampled**. The window enters Saturday UTC only for its first
  **2 h 33 m 04 s** (`2026-10-03T00:00:00Z` → `2026-10-03T02:33:04Z`) and
  contains no Sunday at all, so the "weekend" case rests on one partial day.
  The `windows-*` jobs are the queue-sensitive ones, so their figures are the
  least transferable part of this table.

Re-measure when the workflow file changes, when a step is added or removed, or
when GitHub rotates the `ubuntu-latest` or `windows-latest` image. Also re-read
limit 7 and re-run its check whenever `scripts/ci/check-markdown-links.py`
changes: a different tool revision can invalidate that limit without touching
the workflow, and already did once (see limit 7).

### Warning 4 — workflow-level duration is a DIFFERENT quantity and is queue-dominated

For the same 296 runs, `run.updatedAt − run.createdAt`:

| n | min | median | p90 | max | mean |
| --- | --- | --- | --- | --- | --- |
| 296 | 154 s | 232 s | 258 s | **26,679 s** | 322.9 s |

Excluding the single worst run, the workflow-level maximum falls to **420 s**.

**Why the 26,679 s outlier exists.** Run `36695924676` (conclusion `success`):

| Job | `started_at` | `completed_at` | Duration |
| --- | --- | --- | --- |
| `gate-guard` | 09:24:38Z | 09:24:45Z | 7 s |
| `tools-tests-linux` | 09:24:38Z | 09:30:57Z | 379 s |
| `windows-offline-checks` | 09:24:39Z | 09:28:42Z | 243 s |
| `tools-tests-windows` | 09:24:39Z | 09:27:59Z | 200 s |
| `validate-skills` | **16:47:22Z** | 16:49:13Z | 111 s |

Four jobs started immediately and finished within 6½ minutes. The
`validate-skills` job waited **7 h 22 m 44 s for a runner** and then ran in a
perfectly normal 111 s. Workflow-level duration was 7 h 24 m 39 s while **no
job was ever slow**.

**Workflow-level duration is dominated by runner queueing and must not be used
to judge whether a job is stalled.** The five jobs also run in parallel, so
workflow-level is approximately `max(job) + queue`, never the sum of the jobs.

## 5. Independent re-derivation of this table

Every figure above was re-derived from scratch on **2026-10-03** by a second
agent, with its own `gh` queries against its own cache — not read from the
first measurement's intermediate results. Result: **all five job rows, the
87.8 % band count, the 105-of-296 skip count, the run-id and date ranges, and
the healthy 62 s floor agree exactly.**

One figure disagreed, and the measurement is what this page carries:

| Figure | First measurement's report | First measurement's own machine output | This page (re-derived) |
| --- | --- | --- | --- |
| Workflow-level p90 | 257 s (prose, §6 of its report) | **258 s** (`baseline.json`) | **258 s** |

The discrepancy is a 1-second transcription error in the earlier report's
prose, not in its computation, and it lies in the workflow-level contrast row
that §4's warning 4 already forbids using to judge job stalls. It is recorded
here rather than silently repaired, because the value of this page is that its
figures are traceable.

## 6. Regeneration — exact commands

All commands are read-only. **`gh` must run from inside a git repository** or
carry an explicit `-R`; a bare workspace directory is not one. `gh api` does
**not** accept `-R`, so put `owner/repo` in the endpoint path and run from a
real checkout.

```powershell
# ---- 1) Run-level window -------------------------------------------------------------
# This baseline's window is PINNED, not "the most recent": run ids 36620909745 to
# 37090194553, created 2026-09-29T19:40:27Z to 2026-10-03T02:33:04Z, 296 runs of
# the `validate-skills` workflow. The command below fetches whatever is most
# recent AT THE MOMENT YOU RUN IT, so it does NOT reproduce §3.2 - it yields a
# NEW baseline over a different window (breaking this page's own §2 rule 3 if it
# is then read as the table above). To reproduce §3.2, keep only runs whose
# databaseId lies inside the pinned id range above.
gh run list --limit 300 -R ModernNomad-98/Project-Aegis `
  --json databaseId,headBranch,event,conclusion,createdAt,updatedAt,workflowName,status `
  | Out-File -FilePath 'runs-300.json' -Encoding utf8
# Use Out-File -Encoding utf8, NOT `>`. Windows PowerShell 5.1 `>` writes UTF-16LE,
# which no JSON reader will parse; read it back with encoding='utf-8-sig'.

# ---- 2) Job-level records, one call per run id --------------------------------------
gh api "/repos/ModernNomad-98/Project-Aegis/actions/runs/<RUN_ID>/jobs" --paginate
#   -> duration = completed_at - started_at, both UTC.
#   -> rows with 'conclusion': 'skipped' are EXCLUDED from the duration sample.

# ---- 3) One-run human-readable sanity check -----------------------------------------
gh api "/repos/ModernNomad-98/Project-Aegis/actions/runs/<RUN_ID>/jobs" `
  --jq '.jobs[] | {name, started_at, completed_at, conclusion}'

# ---- 4) The workflow's job list, declared limits and gate conditions ----------------
git show origin/main:.github/workflows/validate-skills.yml

# ---- 5) Workflow-level duration (the DIFFERENT quantity, §3.1) ----------------------
# Same moving-window caveat as step 1: pin the ids if you need §4 warning 4's row.
gh run list --limit 300 -R ModernNomad-98/Project-Aegis `
  --json databaseId,createdAt,updatedAt     # duration = updatedAt - createdAt
```

Then apply §3.3's percentile method to the collected values. `--paginate`
concatenates JSON objects, so decode with a streaming JSON decoder rather than
a single `json.loads`.

## 7. Honest limits of this page

1. **It owns one figure set, not every figure.** `PROC-12` asks for a home for
   the coordinator's figures; this page is that home, and the check-duration
   baseline is the first set landed in it. Other kinds of coordinator figure
   are not here yet, and their absence is a gap rather than a clean bill.
2. **It cannot make anyone re-derive a figure.** §2 is a rule an agent follows,
   not a gate that fails. A figure landed here without its command is a defect a
   reader has to catch.
3. **The baseline decays.** It is pinned to a 3.3-day window, a runner image and
   a workflow revision. Nothing regenerates it automatically, so the
   re-measurement trigger in warning 3 is the only thing keeping it true.
4. **Job-level duration excludes queue time**, which makes it the right basis
   for judging a job and the wrong basis for predicting time-to-green for a
   pull request; add queue time for that, and note that queue time is unbounded.
5. **Failures are included in the primary sample** (5 records: 4 `gate-guard`,
   1 `validate-skills`). §3.2's footnote gives the success-only correction; no
   headline median or p90 moves.
6. **This page has had no independent full-page re-read.** It is a new tracked
   page and starts `pending`, because the repository's targeted-edit rule
   retains an acceptance and cannot confer one.
7. **A line-wrapped link was silently unchecked — FIXED on `main`, revision
   pinned.** When this page was written, the repository's link checker
   `scripts/ci/check-markdown-links.py` was blob
   `bb1e40073a0f379e893218cdbb8f5a8aefbfb65b` (revision `9f5dc6b3`). Its
   `LINK` pattern forbade a newline, so a link whose text or destination
   wrapped to the next line was not counted at all rather than reported as
   broken — the behaviour the register's `7.3` proves, and the reason this
   page's own links were unwrapped. **That is no longer true of the current
   checker.** PR #648 (`20fadd48`, "count markdown links that wrap across a
   line break") replaced the pattern; at blob
   `efa65c95f5444e50867e832a688c8351cd332d2c` (revision `25cc0e7a`) the wrapped
   fixture and its unwrapped twin produce **identical** counts —
   `scripts/tests/fixtures/markdown-links/wrapped/README.md` and
   `unwrapped-twin.md` each report `checked 7, anchors 4, broken 0, dead 0,
   external 1`, exit 0. Keeping a link on one line is now prose style, not a
   correctness requirement. **Re-run that comparison whenever the checker's
   blob changes**, and still compare `links checked` rather than `broken: 0`
   alone, because a link the scan never reaches is invisible in both numbers.

## 8. Provenance

**Measurement.** Source of truth is the GitHub Actions run history of
`ModernNomad-98/Project-Aegis`, read live through `gh`. The measurement wrote
nothing to this repository. Base revision at measurement:
`origin/main` = `279ac94d07f95140814e279ff8b04f7661cb15fd`. The figures were
re-derived independently on 2026-10-03 (§5) and landed by the pull request that
created this page.

**Registration.** The discharge of `PROC-11` and `PROC-12` is recorded as a
dated note in the [process issues and prevention register](../evidence/documentation/process-issues-and-prevention-2026-10-02.md),
which is append-only in practice.

**Skill applied.** `chat-backlog-reconciliation`, for the discipline this page
encodes: move claims out of session state into a dated tracked document, and
audit every one of them against repository evidence — a claim of "done", or a
figure, caps at `unknown` until evidence upgrades it. Its sibling
`ci-failure-classifier` is the consumer of §3.4, because its duration findings
require exactly the comparison point this table supplies.
