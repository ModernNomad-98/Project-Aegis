# Project Aegis execution measurements

At the start of **every** new work package, state together: (1) its previously
published remaining ETA, or "none" if it is new; (2) its new active-work ETA;
and (3) the current **entire backlog** ETA. Give the bounded selected total,
the conditional total when useful, and say explicitly when the full adoption
backlog has no finite total because quantities/decisions are open. Repeat these
figures in its PR with progress and actual time. Record actual active time,
review and CI time, owner waiting, and meaningful checkpoints when the runtime
exposes them; otherwise mark the split unavailable and give measured wall time.
Use observed timestamps rather than reconstructed precision. A range is an
estimate, not a delivery promise.

After every five merged PRs following #106, re-estimate each open work item
and the total in the [backlog forecast](aegis-backlog-forecast.md) from these
measurements and the corresponding PR records. Record the five merge commits,
scope changes and uncertainty. A material owner decision also triggers an
earlier forecast update.

| Work package | First recorded checkpoint (UTC) | Estimated active work | Actual active work | Review / CI | Owner waiting | Status |
| --- | --- | --- | --- | --- | --- | --- |
| BER-BKL-007 authorization (WP-2B-1A governance) | 2026-09-23 10:52 | 20–30 minutes remaining at checkpoint; earlier start was not timed | At least 5m14s observed wall time to PR #103 merge; earlier active time unknown | Independent review and all three Actions passed | None recorded | PR #103 merged at 10:57:14 UTC |
| BER-BKL-007 implementation | 2026-09-23 10:57 | 3–5 hours active work after authorization merge | 4h42m26s observed wall time through PR #104 merge, including owner wait and main-drift reconciliation; active-only unavailable | Independent audit, 997 local BER tests, Linux and Windows passed; guard's documented manual-review failure covered by PR-specific exception | Owner accepted schema shapes on 2026-09-23 | PR #104 merged at 15:39:26 UTC; BKL-007 DONE |
| Calibration replacement storage proposal | 2026-09-23 11:26 | 30–45 minutes active work | Exact active total unavailable; 12m50s observed wall time to merge at 11:38:50 | Independent review passed; final Actions green (Linux 1m24s, Windows 3m11s, guard 5s) | About 1 minute before owner chose A | PR #105 merged; choice A recorded |
| Private input storage amendment (BER-DEC-010) | 2026-09-23 11:39 | 20–40 minutes active work to review and merge-ready PR | Exact active total unavailable; 8m21s observed wall time to merge at 11:47:21 | Independent audit passed after correction; final Actions guard 4s, Linux 1m18s, Windows 2m55s | None recorded | PR #106 merged |
| Calibration replacement candidate packet | 2026-09-23 11:47 | 4–8 hours active work | 33m20s observed wall time to public PR #107 merge; active-only total unavailable | Private PR #1 open; local contract/restore checks passed; public PR #107 independent audit and all Actions passed | Owner semantic review pending | Private packet PENDING; public checkpoint merged |
| Cross-stream owner decision packet | 2026-09-23 12:20 | 2–4 hours active work | 13m38s observed wall time to PR #108 merge; active-only time unavailable | Independent read-only audit passed; all three Actions green | BKL-009 owner selection pending after merge | PR #108 merged at 12:33:38 UTC; BKL-009 remains PARTIAL |
| Issue #101 package 1 design | 2026-09-23 12:34 | 4–8 hours active work | 9m40s observed wall time to PR #109 merge; active-only time unavailable | Independent read-only audit passed; all three Actions green | No runtime authorization requested | PR #109 merged at 12:43:40 UTC; planning only |
| CP-WP-003A offline proof scope proposal | 2026-09-23 12:44 | 2–4 hours active work | 8m58s observed wall time to PR #110 merge; active-only time unavailable | Independent read-only audit passed after terminology correction; all three Actions green | Owner authorization needed before code | PR #110 merged at 12:52:58 UTC; CP-WP-003 BLOCKED |
| BER R4/R5 selected-host decision packet | 2026-09-23 12:53 | 2–4 hours active work | 8m19s observed wall time to PR #111 merge; active-only time unavailable | Independent read-only audit passed after CI/host distinction correction; all three Actions green | Host choice and later probe grant pending | PR #111 merged at 13:01:19 UTC; no host probe or live dispatch |
| Five-merge backlog re-estimate | 2026-09-23 13:02 | 1–2 hours active work; no earlier item estimate | 9m13s observed wall time to PR #112 merge; active-only time unavailable | Independent read-only audit passed; all three Actions green | None needed for arithmetic; owner choices remain gates for execution | PR #112 merged at 13:11:13 UTC; selected total 112–228 h; all optional adoption unbounded |
| Issue #101 package-2 authorization proposal | 2026-09-23 13:12 | Prior package-2 delivery ETA 6–12 h; new scope-packet ETA 1–2 h active | 11m21s observed wall time to PR #113 merge; active-only unavailable | Independent audit and all three Actions passed | Exact owner implementation grant pending | PR #113 merged at 13:23:21 UTC; selected total 112–228 h; both helpers 128–268 h; all options unbounded |
| CP-WP-003A exact-file authorization packet | 2026-09-23 13:24 | Prior CP-WP-003 delivery ETA 12–24 h; prior separate packet ETA none; new packet ETA 1–2 h active | 8m35s observed wall time to PR #114 merge; active-only unavailable | Independent audit and all three Actions passed | Owner implementation grant pending | PR #114 merged at 13:32:35 UTC; selected backlog 112–228 h; both optional helpers 128–268 h; full all-options backlog has no finite ETA |
| Issue #101 package-3 offline-contract scope packet | 2026-09-23 13:33 | Prior package-3 delivery ETA 6–12 h; prior separate packet ETA none; new packet ETA 1–2 h active | 7m15s observed wall time to PR #115 merge; active-only unavailable | Independent audit and all three Actions passed | Owner later approved exact scope; grant transcription/implementation pending | PR #115 merged at 13:40:15 UTC; selected backlog was 112–228 h before new documentation scope |
| Five-merge forecast and documentation backlog | 2026-09-23 15:40 | Prior forecast-packet ETA 1–2 h; new packet ETA 1–2 h active. New documentation item previously 4–8 h, then 24–60 h, now 80–200 h after inventory | 12m43s observed wall time to PR #117 merge; active-only unavailable | Independent audit and all three Actions passed | Owner approved several scopes and required repository-wide documentation readability | PR #117 merged at 15:52:43 UTC; revised selected backlog 191–426 h, optional helpers 207–466 h, all options unbounded |
| BER WP-2B-3 holdout execution-support scope packet | 2026-09-23 15:21 | Prior execution-support delivery estimate 8–16 active hours; prior separate packet estimate none; new packet estimate 1–2 active hours | 39m21s observed wall time to PR #116 merge; active-only unavailable | Independent audit and all three Actions passed | Offline-branch grant, later exact execution-source amendment and input-label review pending | PR #116 merged at 16:00:21 UTC; selected backlog 191–426 active hours, optional helpers 207–466 hours, all options unbounded |
| Owner-approved scope transcription | 2026-09-23 16:01 | No earlier estimate for this grant packet; new estimate 1–2 active hours | 10m42s observed wall time to PR #118 merge; active-only unavailable | Independent audit and all three exact-head Actions passed | Exact grants became effective on merge | PR #118 merged at 16:11:42 UTC; selected backlog 191–426 active hours, optional helpers 207–466 hours, all options unbounded |
| Component-guide readability, first batch | 2026-09-23 16:12 | Prior full documentation item estimate 80–200 active hours; new first-batch estimate 4–8 active hours | In progress | Local command examples and independent audit pending | None for offline documentation | Selected backlog 191–426 active hours; optional helpers 207–466 hours; all options unbounded |

## Progress checkpoints

- **2026-09-23 10:52 UTC — authorization:** The scope record was drafted,
  independently reviewed and corrected; structural validation passed. The
  governance branch was committed and pushed. This is the first timed
  checkpoint; the preceding work has no measured start timestamp.
- **2026-09-23 10:57:14 UTC — authorization merged:** PR #103 merged at
  `f82a4bce770c173df6d4ddc6b920a7b35a6a63e7`. At least 5m14s elapsed
  after the first recorded checkpoint; earlier preparation was not timed.
- **2026-09-23 11:25 UTC — schema implementation candidate:** PR #104 has
  tested schema-integrity code, policy and an independent audit. Linux and
  Windows verification passed. The protected-file guard failure has a
  PR-specific owner exception recorded as AEGIS-APR-005. Final schema-shape
  acceptance remains pending, so no DONE or merge is claimed.
- **2026-09-23 11:27 UTC — calibration storage proposal:** The public source
  repository's visibility was verified on GitHub. A separate private GitHub
  input repository is proposed to preserve holdout confidentiality; the
  existing external execution-evidence root remains distinct. No candidate
  dataset, repository or provider request has been created.
- **2026-09-23 11:34 UTC — storage choice:** Peter Nguyen selected the
  recommended private GitHub input repository after PR #105's first green
  Actions run. The branch now records that answer; a BER-DEC amendment and
  another final-revision check are pending before publication of inputs.
- **2026-09-23 11:38:50 UTC — storage proposal merged:** PR #105 merged at
  `c6fa54ac0fd42342976c6e89a70fd02b390783b0` after its final three
  Actions checks passed. The observed wall interval since the first recorded
  checkpoint was 12m50s; active-only time was not instrumented.
- **2026-09-23 11:39 UTC — amendment started:** BER-DEC-010 preparation began
  from the exact PR #105 merge, with a 20–40 minute active-work estimate.
- **2026-09-23 11:47:21 UTC — amendment merged:** PR #106 merged at
  `14e3f17c380dd26ddba1f27c7e041b6064509ba4` after independent review
  and three green Actions checks. Observed wall time from the 11:39 checkpoint
  was 8m21s; exact active-only time was unavailable. Final measurement was
  recorded in the PR.
- **2026-09-23 11:49 UTC — candidate preparation:** Created
  `ModernNomad-98/Project-Aegis-Calibration-Inputs`, verified PRIVATE with
  only the owner account listed as collaborator, and disabled GitHub Actions
  in that repository. No calibration input was pushed. Candidate branch
  `feat/ber-wp2b3-replacement-candidates` starts at the exact BER-DEC-010
  merge commit. Estimate: 4–8 active hours.
- **2026-09-23 12:13 UTC — first private candidate:** 160 synthetic PENDING
  records were built and validated offline. The exact packet was committed to
  the owner-only private repository at `6beba11e83e5e8a1655f33302e40959ecc6067e5`
  and private PR #1 opened. Composition and manifest restoration passed; no
  provider call or human label approval occurred. Approximately 26 minutes
  elapsed since the candidate work checkpoint, including the requested
  five-merge forecast baseline work; active-only time was not measured.
- **2026-09-23 12:20:20 UTC — candidate public checkpoint merged:** PR #107
  merged at `911fe25f7a5297113890512aaecc38694bda3e8a` with three green
  Actions checks and an independent public-diff audit. Its observed wall
  interval from the 11:47 candidate start was 33m20s; exact active-only
  time is unknown. This is one of five merges after the #106 forecast anchor.
- **2026-09-23 12:20 UTC — owner decision packet started:** Estimated 2–4
  active hours to prepare BKL-009's concrete policy options and the distinct
  remaining BER/CP/#101 decision boundaries.
- **2026-09-23 12:33:38 UTC — owner decision packet merged:** PR #108 merged at
  `2b13be9fac1169bf8f6cd0cfcbe4da0c5b8bf926` after independent read-only
  audit and three green Actions. Observed wall time since the 12:20 checkpoint:
  13m38s; active-only time was not instrumented. This is merge 2 of 5 after
  the #106 forecast anchor. BKL-009 policy selection remains pending.
- **2026-09-23 12:34 UTC — issue #101 package 1 started:** Estimated 4–8 active
  hours for offline design, candidate screening and a paired evaluation plan.
- **2026-09-23 12:43:40 UTC — issue #101 package 1 plan merged:** PR #109 merged
  at `32144083bc86412e30d70873f877d4e7c051b6e0` after independent
  read-only audit and three green Actions. Observed wall time from 12:34 was
  9m40s; active-only time is unavailable. This is merge 3 of 5 after #106.
- **2026-09-23 12:44 UTC — CP-WP-003A scope proposal started:** Estimated 2–4
  active hours to prepare synthetic capability-proof authorization; no code or
  real CP action is authorized by drafting it.
- **2026-09-23 12:52:58 UTC — CP-WP-003A proposal merged:** PR #110 merged at
  `75d1e6e662ed48f0ec9f6b04c4c52e6f39ead319` after independent audit,
  correction and three green Actions. Observed wall time from 12:44 was
  8m58s; active-only time is unavailable. This is merge 4 of 5 after #106.
- **2026-09-23 12:53 UTC — BER selected-host decision packet started:**
  Estimated 2–4 active hours to prepare the R4/R5 host choice and bounded
  offline proof boundary. No host or provider probe is authorized by drafting.
- **2026-09-23 13:01:19 UTC — BER host packet merged:** PR #111 merged at
  `8e6971d806e257097c76159ac0875b4fef8baf0b` after the independent
  audit corrected a stale POSIX `UNRUN` claim and all three Actions passed.
  Observed wall time from 12:53 was 8m19s; active-only time is unavailable.
  This is merge 5 of 5 after #106.
- **2026-09-23 13:02 UTC — five-merge re-estimate started:** Prior item ETA:
  none. New item ETA: 1–2 active hours. Prior selected backlog total:
  106–214 active hours; revised draft selected total: 112–228 active hours;
  conditional both-helper total: 128–268 active hours; full all-options
  backlog: no finite bound while adoption/quantity choices remain open.
- **2026-09-23 13:11:13 UTC — five-merge forecast merged:** PR #112 merged at
  `fa79092f1c0fb1984b75245d8bce6a41982e5419` after independent audit
  and three green Actions. Observed wall time from 13:02 was 9m13s; active-only
  time is unavailable. This is merge 1 of the next five after #111.
- **2026-09-23 13:12 UTC — issue #101 package-2 scope started:** Prior delivery
  ETA 6–12 active hours, no prior scope-packet ETA; new scope-packet ETA
  1–2 active hours. Current bounded selected total 112–228 active hours,
  both-helper conditional total 128–268, full all-options backlog unbounded.
- **2026-09-23 13:23:21 UTC — issue #101 package-2 scope merged:** PR #113 merged
  at `5a2452a0e0a6cec974d142e14a66641cd51f2c5d` after independent audit
  and three green Actions. Observed wall time from 13:12 was 11m21s; active-only
  time is unavailable. This is merge 2 of five after #111. Owner authorization
  for implementation remains pending.
- **2026-09-23 13:24 UTC — CP-WP-003A exact-file packet started:** Prior
  CP-WP-003 delivery ETA 12–24 active hours; prior separate packet ETA none;
  new packet ETA 1–2 active hours. Selected backlog 112–228 active hours,
  both optional helpers 128–268; full all-options backlog has no finite ETA.
- **2026-09-23 13:32:35 UTC — CP-WP-003A exact-file packet merged:** PR #114
  merged at `d187849287e5047fc821f7a1070b0c59cc5b32b9` after independent
  audit and three green Actions. Observed wall time from 13:24 was 8m35s;
  active-only time is unavailable. This is merge 3 of five after #111.
  Owner authorization for implementation remains pending.
- **2026-09-23 13:33 UTC — issue #101 package-3 scope started:** Prior
  package-3 delivery ETA 6–12 active hours; prior separate scope-packet ETA
  none; new packet ETA 1–2 active hours. Selected backlog 112–228 active
  hours, both optional helpers 128–268; full all-options backlog has no finite
  ETA while adoption quantities and decisions remain open.

- **2026-09-23 owner schema decision — PR #104:** Peter Nguyen accepted the
  recommendation to approve the tested schema shapes and merge the PR. The
  earlier PR-specific guard exception remains recorded separately as
  AEGIS-APR-005. A conflict with later main in this measurement log was
  resolved by retaining the later main entries; BER code is unchanged from
  the previously reviewed PR head. Revised exact-head checks remain pending.
- **2026-09-23 15:39:26 UTC — schema integrity merged:** PR #104 merged at
  `c83a0601d9b7945ad407b6fa81bd2563ab501475` after its updated head
  passed local BER tests and Linux/Windows Actions. The protected-file guard
  failed only on its documented review condition under AEGIS-APR-005.
  Observed wall time since 10:57 was 4h42m26s, including owner and base-drift
  waiting; active-only time is unavailable. This is merge 5 of five after #111.
- **2026-09-23 15:40 UTC — five-merge and documentation checkpoint:** The
  previous selected backlog was 112–228 active hours, or 128–268 with both
  optional issue #101 helpers. Closing the 1–2-hour schema row and adding
  the owner-requested repository-wide documentation sweep at 80–200 hours
  yields a new selected estimate of 191–426 hours, or 207–466 with both
  helpers. The full all-options backlog remains without a finite estimate.
  The documentation item was earlier estimated at 4–8 hours for two guides,
  then 24–60 hours provisionally; an inventory of 845 Markdown files widened
  the provisional full-sweep estimate to 80–200 hours. A tracked-file inventory
  then found 491 Markdown files, including 344 skill docs and 84 under `docs/`;
  the initial 845 count had included unrelated untracked local artifacts and
  omitted hidden tracked skill files, so it was not the repository inventory.

- **2026-09-23 15:52:43 UTC — five-merge and documentation packet merged:**
  PR #117 merged at `a7c0724c86cce3f59b4dacfe0db7502ac148b49a` after
  independent audit and all three Actions passed. Observed wall time from the
  approximate 15:40 start was 12m43s; active-only time is unavailable. This is
  merge 1 of the next five after PR #104. The selected backlog is 191–426
  active hours; optional issue #101 helpers raise that to 207–466 hours.
- **2026-09-23 15:21 UTC — BER WP-2B-3 holdout scope checkpoint:** The prior
  execution-support estimate was 8–16 active hours. This separate proposal
  had no prior estimate and was estimated at 1–2 active hours. It describes an
  offline implementation boundary only; owner approval and a reviewed grant
  remain required before code. The selected total is now 191–426 active hours.

- **2026-09-23 16:00:21 UTC — offline holdout scope proposal merged:**
  PR #116 merged at `2755fb6b59c64290a4cef2e4f9bcac204699fe76` after
  independent audit and all three exact-head Actions passed. Its 15:21 start
  to merge interval was 39m21s observed wall time; active-only time was not
  separately captured. This is merge 2 of five after PR #104. The proposal
  did not grant offline implementation, private-input access or provider calls.
- **2026-09-23 16:01 UTC — owner-grant transcription started:** This separate
  governance packet had no earlier estimate and is estimated at 1–2 active
  hours. The selected backlog remains 191–426 active hours, or 207–466 if
  both optional issue #101 helpers are selected. The full all-options backlog
  has no finite estimate.

- **2026-09-23 16:11:42 UTC — owner grants merged:** PR #118 merged at
  `1af342712d27d5e6ea482b3f451106b4dccaf125` after independent audit
  and three green Actions. Observed wall time from the approximate 16:01
  checkpoint was 10m42s; active-only time was not separately measured. This
  is merge 3 of five after PR #104.
- **2026-09-23 16:12 UTC — first documentation batch started:** The prior
  full-sweep estimate is 80–200 active hours; the first component-guide batch
  is estimated at 4–8 active hours. The selected remaining total stays
  191–426 active hours, or 207–466 with both optional issue #101 helpers.
  The root README is outside this batch. The unrelated local control-plane
  design edit remains unstaged.

Append later observations and final actuals in the relevant PR. Keep provider
or model token/credit usage as unknown when the runtime does not expose it.

## Checkpoint after pull request #121 — 2026-09-23

The following merged requests complete the five-merge cadence after #104.
Each request's body or closeout comment carries its own item estimate and
progress. These intervals are wall time from the first captured checkpoint,
not measured active labor, and some work began before that checkpoint.

| Pull request | Merge time (Coordinated Universal Time) | Observed wall interval | Progress |
| --- | --- | ---: | --- |
| [#117](https://github.com/ModernNomad-98/Project-Aegis/pull/117) | 15:52:43 | 12m43s | Documentation inventory and prior forecast |
| [#116](https://github.com/ModernNomad-98/Project-Aegis/pull/116) | 16:00:21 | 39m21s | Offline holdout executor proposal only |
| [#118](https://github.com/ModernNomad-98/Project-Aegis/pull/118) | 16:11:42 | 10m42s | Three exact implementation grants and one evidence-policy choice |
| [#120](https://github.com/ModernNomad-98/Project-Aegis/pull/120) | 16:29:59 | 6m59s | Root documentation entry point and writing standard |
| [#121](https://github.com/ModernNomad-98/Project-Aegis/pull/121) | 16:42:21 | At least 10m39s | Offline advisory routing contract; one independent review finding corrected |

Every open row was reconsidered in the [dated forecast snapshot](aegis-backlog-forecast.md#five-merge-checkpoint--2026-09-23-after-pull-request-121).
The prior selected total was **191–426 active hours**; the revised selected
total is **185–414 active hours**, solely because issue #101 package 3 closed
its 6–12-hour remaining row. The conditional total with both optional issue
#101 helpers moved from **207–466** to **201–454 active hours**. The
repository-wide documentation estimate remains 80–200 active hours until
audited batches give meaningful evidence. Owner waits, GitHub queue time,
provider runs and host provisioning remain outside these active-hour ranges.

## Checkpoint after pull request #126 — 2026-09-23

Five further requests merged after #121. Each pull request's own body or
closeout comment records its estimate, progress and final observed duration.
The intervals below overlap and include waiting or concurrent work; active
labor was not separately instrumented.

| Pull request | Merge time (Coordinated Universal Time) | Observed wall interval | Progress |
| --- | --- | ---: | --- |
| [#123](https://github.com/ModernNomad-98/Project-Aegis/pull/123) | 16:49:28 | 19m29s | Synthetic control-plane capability falsifiers; real route still denied |
| [#122](https://github.com/ModernNomad-98/Project-Aegis/pull/122) | 16:50:19 | At least 11m25s | Three active maintainer guides |
| [#124](https://github.com/ModernNomad-98/Project-Aegis/pull/124) | 16:54:59 | About 19m59s | Manual Aegis-only Windows setup; helper paths unavailable |
| [#125](https://github.com/ModernNomad-98/Project-Aegis/pull/125) | 16:55:48 | 13m27s | Previous five-merge forecast |
| [#126](https://github.com/ModernNomad-98/Project-Aegis/pull/126) | 17:05:32 | 14m46s | Two technical guides and review record |

The [new every-item snapshot](aegis-backlog-forecast.md#five-merge-checkpoint--2026-09-23-after-pull-request-126)
reduces the selected remaining estimate from **185–414** to **175–394 active
hours**: issue #101 package 2 closed its 6–12-hour row, and the delivered
synthetic control-plane increment narrows package 003 from 12–24 to 8–16
hours. This reduction is based on completed scope, not a rate extrapolated
from short wall intervals. If both optional issue #101 helpers are chosen,
the bounded total moves from **201–454** to **191–434 active hours**. The
full all-options backlog remains unbounded. The documentation estimate stays
80–200 hours because most of the inventory remains unreviewed. The #117
baseline counted 491 tracked Markdown files; the merged #126 tree contains
501 tracked Markdown files, counted with `git ls-files`.

## Checkpoint after pull request #141 — 2026-09-23

This record closes the next five-merge interval after #135. The intervening
checkpoints remain in the forecast: [after #130](aegis-backlog-forecast.md#five-merge-checkpoint--2026-09-23-after-pull-request-130)
and [after #135](aegis-backlog-forecast.md#five-merge-checkpoint--2026-09-23-after-pull-request-135).
Their associated requests retain individual estimates and closeout comments;
this later summary does not reconstruct unavailable active-time measurements.
Here, a pull request is a proposed repository change, and Coordinated
Universal Time (UTC) is the time standard used for all timestamps below.

| Pull request and bounded package | Prior estimate and package estimate | First work checkpoint (UTC) | GitHub merge event (`mergedAt`, UTC) | Observed wall time to merge |
| --- | --- | --- | --- | ---: |
| [#136 — evaluation shortlist](https://github.com/ModernNomad-98/Project-Aegis/pull/136) | Prior package-4 delivery: 8–16 active hours; this roadmap update: 30–60 active minutes | About 17:45 | 17:51:29 | About 6m29s |
| [#137 — previous forecast](https://github.com/ModernNomad-98/Project-Aegis/pull/137) | Previous and new forecast-package estimate: 1–2 active hours | About 17:49 | 17:56:56 | About 7m56s |
| [#138 — offline setup guide](https://github.com/ModernNomad-98/Project-Aegis/pull/138) | Prior documentation sweep: 80–200 active hours; this batch: 1–3 active hours | 17:58:19 | 18:11:25 | 13m06s |
| [#140 — three user guides](https://github.com/ModernNomad-98/Project-Aegis/pull/140) | Prior documentation sweep: 80–200 active hours; this batch: 1–3 active hours | 18:10:57 | 18:24:35 | 13m38s |
| [#141 — setup routing plan](https://github.com/ModernNomad-98/Project-Aegis/pull/141) | Prior documentation sweep: 80–200 active hours; this batch: 1–3 active hours | 18:25:36 | 18:36:31 | 10m55s |

All dates in that table are September 23, 2026. Merge times use GitHub pull
request `mergedAt` events; the #136 and #141 commit-object timestamps are one
second earlier. The first two starts are
rounded checkpoints, so their derived durations are approximate. Every
package began with a selected backlog estimate of **175–394 active hours**.
Some intervals overlap; their sum would not measure project elapsed time or
active effort. All five received independent
review and their final Linux, Windows and protected-file checks passed.

Pull request #138 initially failed because its commit lacked a Developer
Certificate of Origin (DCO) sign-off. The signed replacement revision passed
all checks before merge. Its 13m06s interval includes that correction,
independent review and the repeated checks. Pull request #140 also required
corrections after independent review found contract and readability claims
that needed narrowing. Review, queue, rework and active effort were not
separately instrumented. These short, bounded documentation packages cannot
support a coding-rate multiplier or a repository-wide review-rate estimate.

[Pull request #139](https://github.com/ModernNomad-98/Project-Aegis/pull/139)
remains open at `8928383f0838e2d99ee3a89c44b98b7aba7f1c9b` in this snapshot.
Its full evidence-policy estimate was **8–16 active hours** and its bounded
offline increment was estimated at **4–8 hours**, capped at eight. The first
captured file timestamp was **17:41:37 UTC** and the local completion
checkpoint was **18:13:55 UTC**, a **32m18s observed wall interval**. Earlier
preparation and active-only effort were not measured. Local checks and
independent adversarial review passed after corrections; Linux and Windows
Actions passed. The protected-file `gate-guard` check failed, and a separate
owner disposition remains pending. No merge time, completed implementation
row or completed real-host proof is claimed for that candidate.

The [new every-item forecast](aegis-backlog-forecast.md#five-merge-checkpoint--2026-09-23-after-pull-request-141)
reconsiders all 14 selected rows and all seven optional rows. The previous
and revised selected totals are both **175–394 active hours**; selecting both
optional issue #101 helpers gives **191–434 active hours**. Non-documentation
work remains **95–194 hours**, and the full documentation sweep remains
**80–200 hours**. The source tree for #141 contains **509 tracked Markdown
files**, compared with 506 at the prior checkpoint. The full all-options
backlog remains unbounded. Owner waits, GitHub queues, provider execution and
host provisioning remain outside the active-work estimates.

### Preparation time for this checkpoint

This checkpoint had no estimate before preparation; its new estimate was
**1–2 active hours**. Read-only preparation ran from **18:27:20 to 18:29:34
UTC**, an observed **2m14s**. Editing these two records began at **18:37:29
UTC**, after the fifth merge was confirmed. The earlier preparation overlaps
other packages and is included only as a separately observed segment.
Local validation and link checks completed at **18:42:52 UTC**, an observed
**5m23s** from the editing start. The validator reported 185 valid skills and
zero warnings; all eight new relative links and heading anchors resolved,
the arithmetic checks passed, and prior snapshots were preserved exactly.
Active-only effort is not instrumented. Independent read-only review from
**18:43:59 to 18:45:17 UTC** (1m18s observed wall) found no blocker. The
reviewer verified the five merges, all 14 selected and seven optional rows,
the inventory, links and two-file scope. It prompted the explicit `mergedAt`
clock label above. The eventual start-to-merge interval belongs in the pull
request closeout record.

## Checkpoint after pull request #146 — 2026-09-23

Five requests merged after #141, in order #142, #143, #144, #145 and #146.
Their original active-hour estimates and observed start-to-merge wall times
are shown side by side below. The merge-event times come from GitHub pull
request `mergedAt` fields in Coordinated Universal Time (UTC). The intervals
overlap, and active-only work was not instrumented. They include review,
continuous integration and any rework.
Pull request #146 required a reviewed merge-conflict resolution after #145
added an adjacent documentation-ledger row; its interval includes a second
complete set of exact-head Actions.

| Pull request and bounded package | Original ETA | Merge event (UTC) | Observed wall time |
| --- | ---: | --- | ---: |
| [#142 — skill category maps 08–09](https://github.com/ModernNomad-98/Project-Aegis/pull/142) | 1–3 active hours | 18:44:39 | 15m47s |
| [#143 — prior forecast](https://github.com/ModernNomad-98/Project-Aegis/pull/143) | 1–2 active hours | 18:52:10 | 24m50s from first preparation; 14m41s from edit start |
| [#144 — skill category maps 01–07](https://github.com/ModernNomad-98/Project-Aegis/pull/144) | 2–4 active hours, revised from 1–3 | 18:55:43 | 16m44s |
| [#145 — control-plane backlog guide](https://github.com/ModernNomad-98/Project-Aegis/pull/145) | 2–4 active hours | 19:04:34 | About 8m34s; start recorded only to the minute |
| [#146 — current owner-decision index](https://github.com/ModernNomad-98/Project-Aegis/pull/146) | 1–3 active hours | 19:11:10 | 14m16s |

Every selected and optional item was re-estimated in the
[new forecast snapshot](aegis-backlog-forecast.md#five-merge-checkpoint--2026-09-23-after-pull-request-146).
The selected total remains **175–394 active hours**, including **80–200**
for repository-wide documentation and **95–194** for other selected work.
Selecting both optional issue #101 helpers would give **191–434 active
hours**; the all-options scope remains unbounded. The merged #146 tree has
**513 tracked Markdown files**, compared with 509 at #141. These bounded
documentation batches closed no selected implementation row. PR #139's
evidence-policy candidate was still open at this checkpoint and has not
reduced its row. Owner waits, GitHub queues, provider execution and host
provisioning remain outside active-hour estimates.

Preparation for this checkpoint had a prior and new package estimate of
**1–2 active hours**. Independent read-only forecast preparation ran from
**19:05:59 to 19:07:45 UTC** (1m46s observed wall), while the fifth merge
was still pending. Editing started after that merge, about **19:11 UTC**.
The eventual start-to-merge interval belongs in the forecast pull request's
closeout comment. The preparation and editing intervals overlap other work;
they must not be summed as active labor.

## Checkpoint after pull request #151 — 2026-09-23

Five requests merged after #146, in order #148, #147, #149, #150 and #151.
The merge clock is GitHub's pull-request `mergedAt` event. All times below
are September 23, 2026, in Coordinated Universal Time (UTC). The previous
estimate and the estimate for each bounded package are recorded beside its
observed start-to-merge interval.

| Pull request and bounded package | Previous and new estimates | First work checkpoint (UTC) | Merge event (UTC) | Observed wall time |
| --- | --- | --- | --- | ---: |
| [#148 — previous forecast](https://github.com/ModernNomad-98/Project-Aegis/pull/148) | Previous and new: 1–2 active hours | 19:05:59, first preparation | 19:21:11 | 15m12s |
| [#147 — Behavioral Eval Runner backlog guide](https://github.com/ModernNomad-98/Project-Aegis/pull/147) | Previous and new: 2–4 active hours | 19:05:27 | 19:21:59 | 16m32s |
| [#149 — execution handoff](https://github.com/ModernNomad-98/Project-Aegis/pull/149) | Previous page estimate: none; new: 1–3 active hours | 19:18:33 | 19:29:36 | 11m03s |
| [#150 — control-plane design](https://github.com/ModernNomad-98/Project-Aegis/pull/150) | Previous page estimate: none; new: 2–4 active hours | About 19:18 | 19:36:02 | About 18m02s |
| [#151 — forecast navigation](https://github.com/ModernNomad-98/Project-Aegis/pull/151) | Previous page estimate: none; new: 1–3 active hours | 19:26:04 | 19:42:13 | 16m09s |

Every package started with a selected backlog estimate of **175–394 active
hours**. The documentation sweep was estimated at **80–200 active hours**.
All five final revisions passed independent review and all three GitHub
Actions. Their intervals overlap and include review, integration and checks;
active effort, waiting and rework were not separately measured. In particular,
#148 began with preparation overlapping other work and #150's rounded start
cannot support an exact duration. The intervals must not be summed as active
labor or treated as an implementation or full-inventory review rate.

The [new every-item snapshot](aegis-backlog-forecast.md#five-merge-checkpoint--2026-09-23-after-pull-request-151)
reconsiders all **14 selected rows and seven optional rows**. Previous and
revised selected totals are both **175–394 active hours**, comprising
**95–194** for non-documentation work and **80–200** for documentation.
Both optional issue #101 helpers would add **16–40 hours**, giving
**191–434 active hours**. The full all-options backlog remains unbounded.
The merged #151 tree contains **517 tracked Markdown files**, up from 513
after #146. These four readability batches and the prior forecast close no
selected implementation row. The offline policy candidate in pull request
#139 remains open; real-host, owner-label and provider gates remain separate.
Owner waits, GitHub queues, provider execution and host provisioning remain
outside the active-hour estimates.

### Preparation and editing time for this checkpoint

Previous and new checkpoint estimates are both **1–2 active hours**; the
selected backlog estimate at start is **175–394 active hours**. Read-only
preparation ran from **19:38:57 to 19:40:21 UTC**, an observed **1m24s**.
Editing began at **2026-09-23 19:45:33 UTC**, after the fifth merge was
confirmed and an isolated worktree was created. Active-only effort is not
instrumented. Local checks completed at **19:46:40 UTC**, an observed
**1m07s** from the editing start: 185 skills valid with zero warnings, all
31 relative links and heading anchors across the two records resolved,
all row counts and arithmetic checked, and the whitespace check passed.
Prior snapshots remain intact; only the current first-screen navigation
links were updated. Independent read-only review completed at **19:47:46
UTC** with no blocker. GitHub Actions on the exact committed revision and
the eventual start-to-merge interval remain pull request closeout gates.

## Checkpoint after pull request #156 — 2026-09-23

Five requests merged after #151, in order #152, #153, #154, #155 and #156.
The merge clock is GitHub's pull-request `mergedAt` event. All times below
are September 23, 2026, in Coordinated Universal Time (UTC). Duration
notation uses **m** for minutes and **s** for seconds.

| Pull request and bounded package | Previous and new estimates | First work checkpoint (UTC) | Merge event (UTC) | Observed wall time |
| --- | --- | --- | --- | ---: |
| [#152 — first skill screen](https://github.com/ModernNomad-98/Project-Aegis/pull/152) | Pull request records previous and new batch estimates of 2–4 active hours; see the scope note below | 19:31:24 | 19:49:02 | 17m38s |
| [#153 — previous forecast](https://github.com/ModernNomad-98/Project-Aegis/pull/153) | Previous and new checkpoint estimates: 1–2 active hours | 19:38:57, first preparation | 19:53:58 | 15m01s |
| [#154 — cloud skill screen](https://github.com/ModernNomad-98/Project-Aegis/pull/154) | Previous and new batch estimates: 2–4 active hours | 19:34:25 | 19:57:41 | 23m16s |
| [#155 — third skill screen](https://github.com/ModernNomad-98/Project-Aegis/pull/155) | Previous and new batch estimates: 2–4 active hours | 19:44:38 | 20:07:31 | 22m53s |
| [#156 — fifth skill screen](https://github.com/ModernNomad-98/Project-Aegis/pull/156) | Previous fourth-batch estimate: 2–4 active hours; new fifth-batch estimate: 2–4 active hours | 19:57:30 | 20:09:10 | 11m40s |

The [first batch's writer record](../evidence/documentation/skill-docs-first-20-readability-2026-09-23.md)
states that its correction item had no prior estimate, while #152's
pull request records a previous batch estimate of 2–4 active hours. Both
sources record a new bounded estimate of 2–4 hours. This summary preserves
the different scope labels instead of silently choosing one prior-estimate
claim. For #156, the earlier range belongs to a different batch; it does not
establish that batch 4 was delivered.

Every package started with a selected backlog estimate of **175–394 active
hours**. All five final revisions passed their Linux, Windows and
protected-file checks, and the changed documents received independent review.
The intervals overlap and include integration, review corrections and checks.
Active effort, waiting and rework were not separately measured. The #153
interval starts with preparation before editing began. These intervals must
not be summed as active labor or extrapolated into a coding or full-sweep
review rate.

The [new every-item snapshot](aegis-backlog-forecast.md#five-merge-checkpoint--2026-09-23-after-pull-request-156)
reconsiders all **14 selected rows and seven optional rows**. Previous and
revised selected totals are both **175–394 active hours**: **95–194** for
non-documentation work plus **80–200** for documentation. Both optional
issue #101 helpers add **16–40 hours**, giving **191–434 active hours**.
The full all-options backlog remains unbounded.

The exact #156 merge tree contains **521 tracked Markdown files**, compared
with 517 after #151. Four 20-page entrypoint screens corrected 11 skill
pages, but do not close the full documentation sweep. Batch 4 and the fifth
batch's shared-ledger integration are outside this checkpoint. No selected
implementation row closed, and pull request #139's policy candidate remains
open. Owner waits, GitHub queues, provider execution and host provisioning
remain outside the active-hour estimates.

### Preparation and editing time for this checkpoint

Previous and new checkpoint estimates are both **1–2 active hours**; the
selected backlog estimate at start is **175–394 active hours**. Read-only
preparation ran from **20:10:11 to 20:11:59 UTC**, an observed **1m48s**.
Editing began at **2026-09-23 20:15:36 UTC** in an isolated worktree at
the exact #156 merge. Active-only effort is not instrumented. Local checks
completed at **20:16:40 UTC**, an observed **1m04s** from the editing start:
185 skills valid with zero warnings, all 41 relative links and heading anchors
across the two records resolved, all row counts and arithmetic checked, and
the whitespace check passed. Historical snapshots remain intact; only the
current first-screen navigation links were updated. Independent coordinator
review completed at **20:17:42 UTC** with no blocker. GitHub Actions on the
exact committed revision and the eventual start-to-merge interval remain
pull request closeout gates.

## Checkpoint after pull request #160 — 2026-09-23

Five requests merged after #156, in order #162, #157, #158, #159 and #160.
The merge clock is GitHub's pull-request `mergedAt` event. All times below
are September 23, 2026, in Coordinated Universal Time (UTC). Duration
notation uses **m** for minutes and **s** for seconds.

| Pull request and bounded package | Previous and new estimates | First work checkpoint (UTC) | Merge event (UTC) | Observed wall time |
| --- | --- | --- | --- | ---: |
| [#162 — previous forecast](https://github.com/ModernNomad-98/Project-Aegis/pull/162) | Previous and new checkpoint estimates: 1–2 active hours | 20:10:11, first preparation | 20:23:21 | 13m10s |
| [#157 — fourth skill screen](https://github.com/ModernNomad-98/Project-Aegis/pull/157) | Previous and new batch estimates: 2–4 active hours | 19:52:03 | 20:25:05 | 33m02s |
| [#158 — sixth skill screen](https://github.com/ModernNomad-98/Project-Aegis/pull/158) | Previous fifth-batch estimate: 2–4 active hours; new sixth-batch estimate: 2–4 active hours | 20:00:36 | 20:26:31 | 25m55s |
| [#159 — seventh skill screen](https://github.com/ModernNomad-98/Project-Aegis/pull/159) | Previous sixth-batch estimate: 2–4 active hours; new seventh-batch estimate: 2–4 active hours | 20:03:28 | 20:32:16 | 28m48s |
| [#160 — eighth skill screen](https://github.com/ModernNomad-98/Project-Aegis/pull/160) | Previous seventh-batch estimate: 2–4 active hours; new eighth-batch estimate: 2–4 active hours | 20:06:57 | 20:33:17 | 26m20s |

The previous ranges for #158–#160 describe earlier batches, not earlier
measurements of the same page set. Every package started with a selected
backlog estimate of **175–394 active hours**. All five final revisions passed
their Linux, Windows and protected-file checks. The changed documents received
independent review; integration and review corrections are included in the
wall intervals. The #162 interval begins with preparation; its editing start
was 20:15:36 UTC, giving a separate edit-to-merge interval of **7m45s**.

These overlapping intervals include waiting and checks. Active effort,
waiting and rework were not separately instrumented, so they must not be
summed as active labor or extrapolated into a coding or full-sweep review
rate. The pull request bodies and post-merge comments provide the original
estimates and observed clocks; the
[new every-item snapshot](aegis-backlog-forecast.md#five-merge-checkpoint--2026-09-23-after-pull-request-160)
records the five merge commits and reconsiders all **14 selected rows and
seven optional rows**.

Previous and revised selected totals are both **175–394 active hours**:
**95–194** for non-documentation work plus **80–200** for documentation.
Both optional issue #101 helpers add **16–40 hours**, giving **191–434 active
hours**. The full all-options backlog remains unbounded. No selected
implementation row closed, and no optional quantity or package was selected.

The exact #160 merge tree contains **525 tracked Markdown files**, compared
with 521 after #156. This interval delivered four 20-page entrypoint screens
and corrected 14 skill pages. Cumulative batches 1–8 screened **160
entrypoints** and corrected **25 skill pages**; this records bounded
terminology and output review, not full page acceptance. Shared documentation
ledger rows for batches 5–8 remain pending at this checkpoint. Supporting
references and the wider documentation sweep remain open.

At the **20:37:49 UTC** observation, pull request #139 remained open with its
protected-file check failure and separate owner disposition pending. Requests
#161, #163, #164 and #165 were also unmerged; their work is excluded from this
checkpoint. Owner waits, GitHub queues, provider execution and host provisioning
remain outside the active-hour estimates.

### Preparation and editing time for this checkpoint

Previous and new checkpoint estimates are both **1–2 active hours**; the
selected backlog estimate at start is **175–394 active hours**. Read-only
preparation ran from **20:36:56 to 20:38:05 UTC**, an observed **1m09s**.
Editing began at **2026-09-23 20:38:59 UTC** in an isolated worktree at the
exact #160 merge. Active-only effort is not instrumented. Local checks
completed at **20:41:48 UTC**, an observed **2m49s** from the editing start:
185 skills valid with zero warnings, all 50 relative links and heading anchors
across the two records resolved, all row counts and arithmetic checked, and
the whitespace check passed. Historical snapshots remain intact; only the
current first-screen navigation links were updated. Independent review and
the eventual pull request closeout remain pending.

## Checkpoint after pull request #164 — 2026-09-23

Five requests merged after #160, in order #170, #165, #161, #163 and #164.
The merge clock is GitHub's pull-request `mergedAt` event. All times below
are September 23, 2026, in Coordinated Universal Time (UTC). Duration
notation uses **m** for minutes and **s** for seconds.

| Pull request and bounded package | Previous and new estimates | First work checkpoint (UTC) | Merge event (UTC) | Observed wall time |
| --- | --- | --- | --- | ---: |
| [#170 — previous forecast](https://github.com/ModernNomad-98/Project-Aegis/pull/170) | Previous and new checkpoint estimates: 1–2 active hours | 20:36:56, first preparation | 20:46:46 | 9m50s |
| [#165 — owning-skill correction](https://github.com/ModernNomad-98/Project-Aegis/pull/165) | Previous and new bounded correction estimates: 1–3 active hours | 20:28:26 | 20:47:57 | 19m31s |
| [#161 — final entrypoint screen](https://github.com/ModernNomad-98/Project-Aegis/pull/161) | Previous eighth-batch estimate: 2–4 active hours; new final-screen estimate: 2–4 active hours | 20:07:21 | 20:48:39 | 41m18s |
| [#163 — first reference batch](https://github.com/ModernNomad-98/Project-Aegis/pull/163) | Previous final-screen estimate: 2–4 active hours; new first-reference-batch estimate: 2–4 active hours | 20:14:24 | 20:49:42 | 35m18s |
| [#164 — second reference batch](https://github.com/ModernNomad-98/Project-Aegis/pull/164) | Previous first-reference-batch estimate: 2–4 active hours; new second-reference-batch estimate: 2–4 active hours | 20:14:27 | 20:50:33 | 36m06s |

The previous ranges for #161, #163 and #164 describe earlier batches, not
earlier measurements of the same page set. Every package started with a
selected backlog estimate of **175–394 active hours**. All five final
revisions passed their Linux, Windows and protected-file checks. The changed
documents received independent review. The #165 audit found and cleared an
outdated output template and evaluation assertion before the final revision.

The #170 interval begins with preparation; its editing start was 20:38:59 UTC,
giving a separate edit-to-merge interval of **7m47s**. These overlapping wall
intervals include waiting, review corrections, integration and checks. Active
effort, waiting and rework were not separately instrumented, so the intervals
must not be summed as active labor or extrapolated into a coding or full-sweep
review rate. The pull request bodies provide the original estimates and start
clocks; the observed merge events provide the interval endpoints.

The [new every-item snapshot](aegis-backlog-forecast.md#five-merge-checkpoint--2026-09-23-after-pull-request-164)
records the five merge commits and reconsiders all **14 selected rows and
seven optional rows**. Previous and revised selected totals are both
**175–394 active hours**: **95–194** for non-documentation work plus
**80–200** for documentation. Both optional issue #101 helpers add **16–40
hours**, giving **191–434 active hours**. The full all-options backlog remains
unbounded. No selected implementation row closed, and no optional quantity or
package was selected.

The exact #164 merge tree contains **529 tracked Markdown files**, compared
with 525 after #160. The final entrypoint screen adds **26 paths and three
corrected guides**. Cumulatively, the sorted pass covered **186 `SKILL.md`
paths and corrected 28 entrypoint pages**. The 186 paths include **185
shipped skills and one authoring template**; the validator excludes
`.claude/skills/_template/SKILL.md`. These counts describe bounded screens,
not full readability acceptance.

Separately, #165 corrects two owning-skill instructions and one behavior
evaluation; #163 and #164 correct seven reference pages. Remaining supporting
references and full page acceptance keep the wider documentation sweep open.
Shared-ledger integration for entrypoint batches 5 through the final screen,
the reference batches and the owning-skill correction remains pending here.
Pull request #139 remains open with its protected-file guard failure and
separate owner disposition pending. Unmerged work and requests outside this
five-merge checkpoint are excluded from delivery claims. Owner waits, GitHub
queues, provider execution and host provisioning remain outside the active-hour
estimates.

### Preparation and editing time for this checkpoint

Previous and new checkpoint estimates are both **1–2 active hours**; the
selected backlog estimate at start is **175–394 active hours**. Read-only
preparation ran from **20:51:28 to 20:52:23 UTC**, an observed **55 seconds**.
Editing began at **2026-09-23 20:53:14 UTC** in an isolated worktree at the
exact #164 merge. Active-only effort is not instrumented. Local checks
completed at **20:56:17 UTC**, an observed **3m03s** from the editing start:
185 skills valid with zero warnings, all 59 relative links and heading anchors
across the two records resolved, all row counts, duration calculations and
arithmetic checked, and the whitespace check passed. Historical snapshots
remain intact; only the current first-screen navigation links were updated.
Independent review and the eventual pull request closeout remain pending.

## Checkpoint after pull request #169 — 2026-09-23

Five requests merged after #164, in order #174, #166, #167, #168 and #169.
The merge clock is GitHub's pull-request `mergedAt` event. All times below
are September 23, 2026, in Coordinated Universal Time (UTC). Duration
notation uses **m** for minutes and **s** for seconds.

| Pull request and bounded package | Previous and new estimates | First work checkpoint (UTC) | Merge event (UTC) | Observed wall time |
| --- | --- | --- | --- | ---: |
| [#174 — previous forecast](https://github.com/ModernNomad-98/Project-Aegis/pull/174) | Previous and new checkpoint estimates: 1–2 active hours | 20:51:28, first preparation | 21:01:09 | 9m41s |
| [#166 — third reference batch](https://github.com/ModernNomad-98/Project-Aegis/pull/166) | Previous second-reference-batch estimate: 2–4 active hours; new third-reference-batch estimate: 2–4 active hours | 20:21:41 | 21:02:08 | 40m27s |
| [#167 — fourth reference batch](https://github.com/ModernNomad-98/Project-Aegis/pull/167) | Previous third-reference-batch estimate: 2–4 active hours; new fourth-reference-batch estimate: 2–4 active hours | 20:21:54 | 21:03:14 | 41m20s |
| [#168 — fifth screen, first half](https://github.com/ModernNomad-98/Project-Aegis/pull/168) | Previous whole-screen estimate: 2–4 active hours; new first-half estimate: 1–3 active hours | 20:27:55 | 21:04:15 | 36m20s |
| [#169 — fifth screen, second half](https://github.com/ModernNomad-98/Project-Aegis/pull/169) | Previous whole-screen estimate: 2–4 active hours; new second-half estimate: 1–3 active hours | 20:28:01 | 21:05:02 | 37m01s |

The earlier batch ranges for #166 and #167 describe different page sets.
For #168 and #169, the prior whole-screen range and new half-screen ranges
also describe different scopes; neither half was originally estimated at
2–4 hours. Every package started with a selected backlog estimate of
**175–394 active hours**. All five final revisions passed their Linux,
Windows and protected-file checks. The changed documents received independent
review, including corrections to incident-authoring wording, mainline-parent
selection and first-use terms before the final revisions.

The #174 interval begins with preparation; its editing start was 20:53:14 UTC,
giving a separate edit-to-merge interval of **7m55s**. These overlapping wall
intervals include waiting, review corrections, integration and checks. Active
effort, waiting and rework were not separately instrumented, so the intervals
must not be summed as active labor or extrapolated into a coding or full-sweep
review rate. Pull request bodies and timing comments supply the original
estimates and starts; observed merge events provide the interval endpoints.

The [new every-item snapshot](aegis-backlog-forecast.md#five-merge-checkpoint--2026-09-23-after-pull-request-169)
records the five merge commits and reconsiders all **14 selected rows and
seven optional rows**. Previous and revised selected totals are both
**175–394 active hours**: **95–194** for non-documentation work plus
**80–200** for documentation. Both optional issue #101 helpers add **16–40
hours**, giving **191–434 active hours**. The full all-options backlog remains
unbounded. No selected implementation row closed, and no optional quantity or
package was selected.

The exact #169 merge tree contains **533 tracked Markdown files**, compared
with 529 after #164. This interval corrects **27 reference pages**, giving
**34 cumulative delivered reference corrections**. Bounded reference screens
now reach sorted positions **1–100 of 156**. This is terminology, navigation
and specific technical-guidance review, not full page acceptance. Earlier
entrypoint coverage remains **186 `SKILL.md` paths**, comprising 185 shipped
skills and one template, with 28 corrected pages in those screen batches.

At the **21:06:39 UTC** preparation checkpoint, reference requests #171–#173
remained open; their 56-reference screen scope is excluded here. Requests
#175 and #139 were also open, and #139's documented protected-file guard
failure and separate owner disposition remained pending. Shared-ledger
integration and the wider documentation sweep remain open. Unmerged work and
requests outside this five-merge checkpoint are excluded from delivery
claims. Owner waits, GitHub queues, provider execution and host provisioning
remain outside the active-hour estimates.

### Preparation and editing time for this checkpoint

Previous and new checkpoint estimates are both **1–2 active hours**; the
selected backlog estimate at start is **175–394 active hours**. Read-only
preparation ran from **21:05:58 to 21:06:39 UTC**, an observed **41 seconds**.
Editing began at **2026-09-23 21:07:20 UTC** in an isolated worktree at the
exact #169 merge. Active-only effort is not instrumented. Local checks
completed at **21:10:28 UTC**, an observed **3m08s** from the editing start:
185 skills valid with zero warnings, all 68 relative links and heading anchors
across the two records resolved, all row counts, duration calculations and
arithmetic checked, and the whitespace check passed. Historical snapshots
remain intact; only the current first-screen navigation links were updated.
Independent review and the eventual pull request closeout remain pending.
