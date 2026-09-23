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
