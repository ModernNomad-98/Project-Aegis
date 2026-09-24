# Project Aegis execution measurements

## Start here — current measurements

This page is for maintainers and coding agents tracking Project Aegis work.
**ETA** means estimated time to complete a work item; **PR** means pull
request; **CI** means continuous integration; and **UTC** means Coordinated
Universal Time. Codes such as **BER-BKL-007** (Behavioral Eval Runner backlog
item 007), **WP-2B-1A** (work package 2B-1A), and **OD-1** (owner decision 1)
identify records in the [runner backlog](behavioral-eval-runner-backlog.md),
where their scope and gates are explained. The codes are identifiers, not
independent permission to start work. **CP-WP-003A** means control-plane
work package 003A; its scope is in the [control-plane backlog](resumable-control-plane-backlog.md).
**AEGIS-APR-005** means Project Aegis approval-register entry 005; read the
[owner approval register](../approvals/APPROVAL_REGISTER.md) for its exact
grant and later lifecycle events. The shorter `BKL-009` in older entries
means the same runner backlog item as `BER-BKL-009`, the evidence-policy
work; it is not a separate package.

The latest [five-merge checkpoint after pull request #238](#checkpoint-after-pull-request-238--2026-09-24)
reconsiders every open work item and links the [current remaining-work
forecast](aegis-backlog-forecast.md#five-merge-checkpoint--2026-09-24-after-pull-request-238).
The table and dated checkpoints below preserve their original estimates and
observed intervals; older pending or in-progress cells are historical, not
current work status. Active-work estimates and observed wall time are different
measurements. Use the owning backlogs and approval register for current gates.

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

## Checkpoint after pull request #238 — 2026-09-24

The five merges since #232 were #233, #234, #236, #237 and #238. Their exact
merge commits and original package estimates are below. The interval column
uses GitHub `mergedAt` receipts, not Git commit timestamps: #232
06:46:49, #233 06:59:20, #234 07:51:54, #236 08:30:44, #237 08:39:50 and
#238 09:14:07 UTC. It measures from the preceding merge to this merge and
includes unrelated work,
review, CI and queue time and is not a measure of active labor or a sum of
task durations.

| Merged request and scope | Exact merge commit | Original active-work estimate | Prior-merge wall interval |
| --- | --- | ---: | ---: |
| [#233](https://github.com/ModernNomad-98/Project-Aegis/pull/233): forecast and status update | `b545d07591f1508b197d708b33cfd2991d50db58` | 1–2 h | 12m31s |
| [#234](https://github.com/ModernNomad-98/Project-Aegis/pull/234): 40-page acceptance | `5c46c7b3e61712674051eb734fa7d099a10aae4f` | 6–12 h | 52m34s |
| [#236](https://github.com/ModernNomad-98/Project-Aegis/pull/236): 18-page acceptance | `39361bad7537b2140e601fe9fd7d6314d8540c7f` | 3–6 h | 38m50s |
| [#237](https://github.com/ModernNomad-98/Project-Aegis/pull/237): Issue #101 host preparation proposal | `8ed59cd761d156b85bf80b16246131d84159cbda` | 1–2 h | 9m06s |
| [#238](https://github.com/ModernNomad-98/Project-Aegis/pull/238): remaining-page review | `a092f8e07429c75cdc06d46befe084cb84a35d13` | 25–105 h | 34m17s |

The five intervals span **06:46:49–09:14:07 UTC**, totaling **2h27m18s**.
PR #238 work overlapped #237; its separately documented first-work-to-merge
upper bound is **43m23s**. PR #234's documented task interval is
**39m51s–52m34s**. Active-only and review/CI/queue splits remain unavailable.
The [forecast checkpoint](aegis-backlog-forecast.md#five-merge-checkpoint--2026-09-24-after-pull-request-238)
reassesses all 14 selected and seven optional rows. It reduces documentation
from **30–115** to **1–3 active hours** and the selected total from
**125–309** to **96–197**, based on accepted pages and one pending README,
not on the wall intervals. Subsequent #240–#243 merges corrected already
delivered setup and offline control-plane defects; they did not close the
remaining owner, real-host or provider gates. Four merges followed #238 before
this checkpoint; its accepted merge would be the fifth.

## Proposed BER-DEC-012 holdout-support grant — 2026-09-24

The first recorded preparation checkpoint is 08:02 UTC on 2026-09-24, from
`main` at `5c46c7b3e61712674051eb734fa7d099a10aae4f` after PR #234.
The previous execution-support estimate was **8–16 active hours**. This
separate governance proposal is estimated at **1–2 active hours**; it does not
reduce the implementation estimate until an owner decision and delivery change
the scope. The selected remaining backlog was **120–304 active hours** at the
PR #234 checkpoint, of which documentation was **25–110** and other selected
work **95–194**; the full optional adoption backlog had no finite total.
Actual active time, review/CI time and owner waiting are not yet measured.
The [proposed decision](behavioral-eval-runner-backlog.md#ber-dec-012-proposed-offline-holdout-support-implementation-grant--pending)
is **PENDING** and creates no implementation, private-input, provider or
spending authority. Record the observed wall interval and separate known
review, CI and owner waiting after the governance PR reaches a disposition.

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

## Checkpoint after pull request #173 — 2026-09-23

Five requests merged after #169, in order #177, #175, #171, #172 and #173.
The merge clock is GitHub's pull-request `mergedAt` event. All times below
are September 23, 2026, in Coordinated Universal Time (UTC). Duration
notation uses **m** for minutes and **s** for seconds.

| Pull request and bounded package | Previous and new estimates | First work checkpoint (UTC) | Merge event (UTC) | Observed wall time |
| --- | --- | --- | --- | ---: |
| [#177 — previous five-merge forecast](https://github.com/ModernNomad-98/Project-Aegis/pull/177) | Previous and new checkpoint estimates: 1–2 active hours | 21:05:58, first preparation | 21:15:07 | 9m09s |
| [#175 — scoped human merge-grant clarification](https://github.com/ModernNomad-98/Project-Aegis/pull/175) | No previous item estimate recorded; new correction estimate: 1–3 active hours | 20:52:28, first preparation | 21:16:02 | 23m34s |
| [#171 — sixth reference screen, four corrected pages](https://github.com/ModernNomad-98/Project-Aegis/pull/171) | Previous fifth-screen half-batch estimate: 1–3 active hours; new sixth-screen estimate: 2–4 active hours | 20:41:22, first preparation | 21:16:49 | 35m27s |
| [#172 — seventh reference screen, six corrected pages](https://github.com/ModernNomad-98/Project-Aegis/pull/172) | Previous sixth-screen estimate: 2–4 active hours; new seventh-screen estimate: 2–4 active hours | 20:43:13, first preparation | 21:17:35 | 34m22s |
| [#173 — final 16-reference screen, five corrected pages](https://github.com/ModernNomad-98/Project-Aegis/pull/173) | Previous seventh-screen estimate: 2–4 active hours; new final-screen estimate: 1–3 active hours | 20:44:33, first preparation | 21:18:19 | 33m46s |

The earlier ranges for #171–#173 describe different page sets. #175 was a
newly identified correction with no previous item estimate. Every package
started with a selected backlog estimate of **175–394 active hours**.
All five final revisions passed their Linux, Windows and protected-file
checks, and the changed documents received independent review.

These starts include read-only preparation. Editing began later: #177 at
21:07:20 UTC, #175 at 20:54:08, #171 at 20:43:34, #172 at 20:45:58 and #173 at
20:51:45. The observed intervals must not be presented as continuous editing
time. They overlap and include waiting, review, integration and checks.
Active effort, waiting and rework were not separately instrumented, so these
intervals must not be summed as active labor or extrapolated into a coding
or full-sweep review rate. Pull request bodies and timing comments provide
the estimates and starts; observed merge events provide the endpoints.

The [new every-item snapshot](aegis-backlog-forecast.md#five-merge-checkpoint--2026-09-23-after-pull-request-173)
records the five merge commits and reconsiders all **14 selected rows and
seven optional rows**. Previous and revised selected totals are both
**175–394 active hours**: **95–194** for non-documentation work plus
**80–200** for documentation. Both optional issue #101 helpers add **16–40
hours**, giving **191–434 active hours**. The full all-options backlog remains
unbounded. No selected implementation row closed, and no optional quantity or
package was selected.

The exact #173 merge tree contains **536 tracked Markdown files**, compared
with 533 after #169. The three reference screens add **15 corrections**,
bringing cumulative screen-batch corrections to **49 reference pages**.
All **156 sorted reference paths** now have bounded screening coverage.
This completes the screening pass, not full page acceptance or the wider
documentation sweep. Earlier entrypoint coverage remains **186 `SKILL.md`
paths**, comprising 185 shipped skills and one template, with 28 corrected
pages in those screen batches.

Separately, #175 clarifies existing grant handling in two skill instructions,
two reference pages and two evaluation files. It adds no Markdown file and
creates no grant or repository-setting change. Shared-ledger integration
remains pending. At the **21:20:04 UTC** preparation checkpoint, #176, #178
and #179 remained open and are excluded. #139 also remained open with its
documented protected-file guard failure and separate owner disposition
pending. Owner waits, GitHub queues, provider execution and host provisioning
remain outside the active-hour estimates.

### Preparation and editing time for this checkpoint

Previous and new checkpoint estimates are both **1–2 active hours**; the
selected backlog estimate at start is **175–394 active hours**. Read-only
preparation ran from **21:19:16 to 21:20:04 UTC**, an observed **48 seconds**.
Editing began at **2026-09-23 21:20:55 UTC** in an isolated worktree at the
exact #173 merge. Active-only effort is not instrumented. Local checks
completed at **21:25:09 UTC**, an observed **4m14s** from the editing start:
185 skills valid with zero warnings, all 76 relative links and heading anchors
across the two records resolved, all row counts, durations and arithmetic
checked, and the whitespace check passed. Historical snapshots remain intact;
only the current first-screen navigation links were updated. Independent
review and the eventual pull request closeout remain pending.

## Checkpoint after pull request #181 — 2026-09-23

Five requests merged after #173, in order #180, #176, #178, #179 and #181.
The merge clock is GitHub's pull-request `mergedAt` event, confirmed for each
request; all times are September 23, 2026, in Coordinated Universal Time
(UTC). **h**, **m** and **s** mean hours, minutes and seconds.

| Pull request and bounded package | Previous estimate | New package estimate | First audit/preparation (UTC) | Merge event (UTC) | Observed wall time |
| --- | ---: | ---: | ---: | ---: | ---: |
| [#180 — previous five-merge forecast](https://github.com/ModernNomad-98/Project-Aegis/pull/180) | 1–2 h | 1–2 h | 21:19:16 | 21:29:50 | 10m34s |
| [#176 — changelog and startup routing](https://github.com/ModernNomad-98/Project-Aegis/pull/176) | 2–4 h guide batch | 1–3 h bounded correction | 21:00:06 | 21:33:11 | 33m05s |
| [#178 — seven operational guides](https://github.com/ModernNomad-98/Project-Aegis/pull/178) | 2–4 h smaller screen | 4–8 h seven-page correction | 21:04:03 | 21:33:58 | 29m55s |
| [#179 — five authorization proposals](https://github.com/ModernNomad-98/Project-Aegis/pull/179) | 2–4 h smaller guide batch | 2–4 h bounded correction | 21:03:56 | 21:34:31 | 30m35s |
| [#181 — seven legacy plans and research pages](https://github.com/ModernNomad-98/Project-Aegis/pull/181) | 4–8 h 15-page audit | 4–8 h seven-page correction | 21:19:43 | 21:35:10 | 15m27s |
| **Five-merge cycle** | No single combined active-work ETA published | Five separately scoped package estimates above | **21:00:06**, earliest audit | **21:35:10**, last merge | **35m04s** |

The earlier ranges for #176–#181 describe preceding or differently bounded
screens. All five packages began with a selected remaining-backlog estimate of
**175–394 active hours**. Their intervals overlap and include read-only
preparation, editing, independent review, integration, checks and waiting.
Active effort and waits were not separately instrumented; these values cannot
be summed as labor or used to infer a full-sweep rate. The merge commit object's
clock is one second earlier than GitHub's merge event for #176 and #178; this
table consistently uses the GitHub event.

All five exact-head pull-request checks and their main-branch checks passed.
The four delivered documentation corrections added four
dated evidence notes. The exact #181 merge tree contains **540 tracked
Markdown files**, versus 536 after #173. They improved startup routing,
operational status pointers and historical plan labels; they did not close
the full documentation acceptance or a selected implementation item.

The [every-item snapshot](aegis-backlog-forecast.md#five-merge-checkpoint--2026-09-23-after-pull-request-181)
reconsiders all **14 selected** and **seven optional** rows. Previous and
revised selected totals both remain **175–394 active hours**, split into
**95–194** non-documentation and **80–200** documentation hours. The two
optional issue #101 helpers add **16–40 hours** if selected, giving
**191–434 active hours**. The all-options backlog remains unbounded. No
optional package or quantity was selected. Owner waiting, GitHub queues,
provider execution and host provisioning are outside these active-hour
estimates. This checkpoint restarts the five-merge counter after #181.

### Preparation and editing time for this checkpoint

The previous and new forecast-packet estimates are both **1–2 active hours**.
The selected backlog estimate at start was **175–394 active hours**. Read-only
preparation began at **21:35:39 UTC**; the isolated worktree was created from
the exact #181 merge before editing. Active-only time is not instrumented.
Local checks completed and the draft froze at **21:41:06 UTC**, an observed
**5m27s** after the first preparation checkpoint. The validator reported 185
valid skills with zero warnings; 78 relative file links and two same-page
heading anchors resolved (80 internal links total), all 14 selected
and seven optional rows and totals were checked, and `git diff --check`
passed. Historical forecast and metrics text was preserved. Independent
read-only review remains pending at this draft checkpoint.

## Checkpoint after pull request #186 — 2026-09-23

Five requests merged after #181, in order #185, #182, #183, #184 and #186.
All times below are September 23, 2026, in Coordinated Universal Time (UTC).
**h**, **m** and **s** mean hours, minutes and seconds. The merge endpoints
are GitHub pull-request `mergedAt` events recorded by the coordinator;
local Git history confirms the merge identities and delivered scope.

| Pull request and bounded package | Previous estimate | New package estimate | First audit/preparation (UTC) | Merge event (UTC) | Observed wall time |
| --- | ---: | ---: | ---: | ---: | ---: |
| [#185 — previous five-merge forecast](https://github.com/ModernNomad-98/Project-Aegis/pull/185) | 1–2 h | 1–2 h | 21:35:39 | 21:49:17 | 13m38s |
| [#182 — documentation batch ledger](https://github.com/ModernNomad-98/Project-Aegis/pull/182) | None recorded for this integration | 1–3 h | 20:59:26 | 21:50:02 | 50m36s |
| [#183 — three roadmap and audit reading keys](https://github.com/ModernNomad-98/Project-Aegis/pull/183) | 4–8 h wider screen | 1–3 h bounded correction | 21:27:21 | 21:50:43 | 23m22s |
| [#184 — evidence index and seven dated banners](https://github.com/ModernNomad-98/Project-Aegis/pull/184) | 2–4 h evidence inventory | 4–8 h bounded correction | 21:37:27 | 21:51:20 | 13m53s |
| [#186 — five candidate and hosted-evidence reading notes](https://github.com/ModernNomad-98/Project-Aegis/pull/186) | 2–4 h evidence inventory | 2–4 h five-page correction | 21:47:36 | 21:57:03 | 9m27s |
| **Five-merge cycle** | No single combined active-work estimate published | Separately scoped package estimates above | **20:59:26**, earliest preparation | **21:57:03**, last merge | **57m37s** |

The earlier ranges for #183–#186 describe preceding or differently bounded
screens. Every package began with a selected backlog estimate of
**175–394 active hours**. The original estimates, starts and completion
intervals are recorded in the linked pull requests and their timing comments.
The prior forecast records #185's preparation start; the ledger records
#182's original integration estimate. The [three-page evidence note](../evidence/documentation/remaining-active-docs-readability-2026-09-23.md)
records #183's later editing start at 21:29:03 and its terminology corrections.
The [five-page follow-up note](../evidence/documentation/evidence-followup-current-reading-2026-09-23.md)
records #186's 21:47:36 start and independent review. These local notes and the
[evidence index](../evidence/README.md) retain the bounded scope and historical
status of the pages concerned.

These intervals overlap and include read-only preparation, editing, review,
integration, checks and waiting. Active effort, waits and rework were not
separately instrumented. Do not sum these wall intervals as labor, treat a
first-audit timestamp as an editing start, or infer a full-sweep or coding
rate from them. The Git merge-commit clocks for #185 and #184 are one second
earlier than the observed GitHub events; this table uses the events consistently.

All five final pull-request revisions passed their Linux, Windows and
protected-file checks, as verified by the coordinator at the exact merge
heads. All five main-branch runs also passed. The #186 main run was still in
progress at the 21:58 UTC observation; [run 35925522295](https://github.com/ModernNomad-98/Project-Aegis/actions/runs/35925522295)
subsequently completed successfully at the exact merge before this draft froze.

The exact #186 merge `d5b007b0a3cc2bd43806a16970f19c84be9a86b0`
contains **543 tracked Markdown files**, compared with 540 after #181.
#182 adds no file, #183 adds one dated evidence note, #184 adds one evidence
index and #186 adds one dated evidence note. The documentation ledger now
includes the completed screen batches through #173 and the separate
owning-skill corrections: 186 entrypoint paths (185 shipped skills plus one
template), with 28 screen-batch corrections, and 156 reference paths, with
49 screen-batch corrections. This is a ledger closeout of earlier bounded
screens, not full page acceptance or a second set of delivered corrections.
The evidence index covers 15 selected records; the five follow-up reading
notes preserve earlier failures and candidate-only results.

The [every-item snapshot](aegis-backlog-forecast.md#five-merge-checkpoint--2026-09-23-after-pull-request-186)
reconsiders all **14 selected** and **seven optional** rows. Previous and
revised selected totals remain **175–394 active hours**: **95–194** for
non-documentation work plus **80–200** for documentation. Both optional
issue #101 helpers add **16–40 hours**, giving **191–434 active hours**.
The all-options backlog has no finite estimate. No implementation gate
closed and no optional package or quantity was selected. Pull request #139
remains outside this merged tree pending its separate protected-file guard
disposition; no exception is inferred from these documentation merges.
Owner waiting, GitHub queues, provider execution and host provisioning are
outside the active-hour estimates. Restart the five-merge counter after #186.

### Preparation and editing time for this checkpoint

Previous and new forecast-package estimates are both **1–2 active hours**;
the selected backlog estimate at start is **175–394 active hours**.
Read-only preparation ran from **21:56:26 to 21:57:52 UTC**, an observed
**1m26s**. Editing began at **21:58:10 UTC** in an isolated worktree at the
exact #186 merge. Active-only effort is not instrumented. Local checks
completed at **22:02:01 UTC**, an observed **3m51s** after editing began:
185 skills valid with zero warnings; all 91 local relative links and heading
anchors resolved; all selected/optional rows, totals, five merge identities,
durations and the 543-file Markdown count checked; and `git diff --check`
passed. Historical snapshots remain intact; only current first-screen
navigation was updated. Independent read-only review and the eventual
pull-request closeout remain pending at this draft checkpoint.

## Checkpoint after pull request #191 — 2026-09-23

Five requests merged after #186, in order #189, #187, #188, #190 and #191.
All times below are September 23, 2026, in Coordinated Universal Time (UTC).
**h**, **m** and **s** mean hours, minutes and seconds. Merge endpoints use
GitHub pull-request `mergedAt` events recorded by the coordinator.
Local Git history confirms each merge identity and delivered file scope.

| Pull request and bounded package | Previous estimate | New package estimate | First audit/preparation (UTC) | Merge event (UTC) | Observed wall time |
| --- | ---: | ---: | ---: | ---: | ---: |
| [#189 — previous five-merge forecast](https://github.com/ModernNomad-98/Project-Aegis/pull/189) | 1–2 h | 1–2 h | 21:56:26 | 22:08:40 | 12m14s |
| [#187 — root maintainer reading route](https://github.com/ModernNomad-98/Project-Aegis/pull/187) | 2–4 h inventory | 1–3 h bounded correction | 21:48:24 | 22:09:42 | 21m18s |
| [#188 — four historical documentation notes](https://github.com/ModernNomad-98/Project-Aegis/pull/188) | 2–4 h preceding screen | 1–3 h bounded correction | 22:00:49 | 22:11:11 | 10m22s |
| [#190 — seven agent and contributor pages](https://github.com/ModernNomad-98/Project-Aegis/pull/190) | 2–4 h preceding 15-page screen | 2–4 h seven-page correction | 22:01:17 | 22:14:38 | 13m21s |
| [#191 — ledger through #186](https://github.com/ModernNomad-98/Project-Aegis/pull/191) | 1–3 h | 1–3 h | 22:06:41 | 22:16:49 | 10m08s |
| **Five-merge cycle** | No single combined active-work estimate published | Separately scoped package estimates above | **21:48:24**, earliest preparation | **22:16:49**, last merge | **28m25s** |

The previous ranges for #187, #188 and #190 describe preceding or differently
bounded screens. Every package began with a selected remaining-backlog
estimate of **175–394 active hours**. The linked pull requests and their
timing comments record the original estimates and starts; local evidence
records identify later editing checkpoints where available. #189 editing
began at 21:58:10, after its first preparation, and #191 editing began at
22:08:40, after its 22:06:41 preparation. The [agent/contributor evidence note](../evidence/documentation/agent-contributor-docs-readability-2026-09-23.md)
records #190's 22:01:17 editing start and the terminology and sign-off
corrections made during independent review.

These overlapping intervals include preparation, editing, independent
review, integration, checks and waits. Active effort, waiting and rework
were not separately instrumented. Do not sum the intervals as labor or
derive a full-sweep or coding rate from them. The merge-commit clocks are
one second earlier than GitHub's merge events for #187, #190 and #191, and
two seconds earlier for #188; the table consistently uses the GitHub events.

All five final pull-request revisions passed their Linux, Windows and
protected-file checks, as verified by the coordinator at the exact merge
heads. All five main-branch runs also passed. The last two,
[#190 main run 35927233158](https://github.com/ModernNomad-98/Project-Aegis/actions/runs/35927233158)
and [#191 main run 35927442963](https://github.com/ModernNomad-98/Project-Aegis/actions/runs/35927442963),
were still in progress at about 22:17 UTC and were confirmed successful at
their exact merges before this draft froze.

The exact #191 merge `761915207f7974b3d4cab7fb099216188ef3e968`
contains **544 tracked Markdown files**, compared with 543 after #186.
Only #190 added a Markdown file, its dated evidence note. #187 revised the
root maintainer route, #188 dated four historical documentation notes,
#190 clarified seven existing agent/contributor pages, and #191 integrated
seven previously delivered batches in the [documentation ledger](aegis-documentation-readability-backlog.md#ledger-checkpoint-through-pull-request-186--2026-09-23).
The ledger's 543-file count belongs to #186. Its completed skill/reference
screens and this cycle's guide corrections remain bounded evidence, not
full page acceptance or proof of agent/provider behavior. Agent names,
tools, models and permissions were not changed by the terminology edits.

The [every-item snapshot](aegis-backlog-forecast.md#five-merge-checkpoint--2026-09-23-after-pull-request-191)
reconsiders all **14 selected** and **seven optional** rows. Previous and
revised selected totals remain **175–394 active hours**, comprising
**95–194** non-documentation and **80–200** documentation hours.
Both optional issue #101 helpers add **16–40 hours**, giving
**191–434 active hours**. The all-options backlog remains unbounded.
No selected implementation gate closed and no optional package or quantity
was selected. Pull request #139 remains unmerged and its separate guard
disposition is still pending. Owner waits, GitHub queues, provider execution
and host provisioning are outside the active-hour estimates. Restart the
five-merge counter after #191.

### Preparation and editing time for this checkpoint

Previous and new forecast-package estimates are both **1–2 active hours**;
the selected backlog estimate at start is **175–394 active hours**.
Read-only preparation began at **22:17:50 UTC**. Editing began at
**22:18:05 UTC** in an isolated worktree at the exact #191 merge.
Active-only effort is not instrumented. Local checks completed at
**22:22:02 UTC**, an observed **3m57s** after editing began: 185 skills valid
with zero warnings; all 100 local relative links and heading anchors
resolved; all row counts, totals, five merge identities and wall intervals
checked; the 544-file Markdown count verified; and `git diff --check`
passed. Historical snapshots remain intact, with only current first-screen
navigation changed. Independent read-only review and the eventual
pull-request closeout remain pending at this draft checkpoint.

## Checkpoint after pull request #196 — 2026-09-23

Five requests merged after #191, in order #194, #192, #193, #195 and #196.
All times below are September 23, 2026, in Coordinated Universal Time (UTC).
**h**, **m** and **s** mean hours, minutes and seconds. Merge endpoints are
GitHub pull-request `mergedAt` events; the first-work timestamps come from
the pull-request bodies and merge-time comments. The exact #196 merge is
`437e73a7967d908b30fe9d919365ec2cf2ed035b`.

| Pull request and bounded package | Previous estimate | New package estimate (original ETA) | First work (UTC) | Merge event (UTC) | Observed wall time |
| --- | ---: | ---: | ---: | ---: | ---: |
| [#194 — preceding forecast](https://github.com/ModernNomad-98/Project-Aegis/pull/194) | 1–2 h | 1–2 h | 22:17:50 | 22:27:42 | 9m52s |
| [#192 — category and application path](https://github.com/ModernNomad-98/Project-Aegis/pull/192) | 2–4 h screen | 1–3 h correction | 22:16:34 | 22:28:10 | 11m36s |
| [#193 — historical runner design and roadmap](https://github.com/ModernNomad-98/Project-Aegis/pull/193) | 2–4 h screen | 1–3 h correction | 22:16:19 | 22:29:03 | 12m44s |
| [#195 — stable forecast links](https://github.com/ModernNomad-98/Project-Aegis/pull/195) | 2–4 h screen | 1–2 h correction | 22:24:37 | 22:34:17 | 9m40s |
| [#196 — control-plane verification guide](https://github.com/ModernNomad-98/Project-Aegis/pull/196) | 2–4 h screen | 1–3 h correction | 22:24:45 | 22:35:54 | 11m09s |
| **Five-merge cycle** | No single combined active-work estimate | Separately scoped estimates above | **22:16:19**, earliest work | **22:35:54**, fifth merge | **19m35s** |

The intervals overlap, and the previous screen estimates cover different
scope from the correction estimates. They include editing, independent audit,
GitHub checks and queue time. Active effort and waits were not separately
instrumented. Do not sum these intervals as labor or extrapolate them into a
full documentation-sweep rate. Every package began with a selected-backlog
estimate of **175–394 active hours**.

The exact #196 tree has **547 tracked Markdown files**, compared with 544
after #191. Three dated evidence notes were added by #193, #195 and #196.
The category and path guidance, historical runner design, stable forecast
routes and control-plane verification guide were corrected; the wider
documentation acceptance inventory remains open. None of the five PRs
closed a selected implementation or provider/host gate.

All five final PR heads passed Linux, Windows and protected-file checks
before their merges. Their exact-main runs also succeeded: #194
[35928468606](https://github.com/ModernNomad-98/Project-Aegis/actions/runs/35928468606),
#192 [35928508247](https://github.com/ModernNomad-98/Project-Aegis/actions/runs/35928508247),
#193 [35928586186](https://github.com/ModernNomad-98/Project-Aegis/actions/runs/35928586186),
#195 [35929071102](https://github.com/ModernNomad-98/Project-Aegis/actions/runs/35929071102),
and #196 [35929217637](https://github.com/ModernNomad-98/Project-Aegis/actions/runs/35929217637).

The [every-item forecast](aegis-backlog-forecast.md#five-merge-checkpoint--2026-09-23-after-pull-request-196)
reassesses all **14 selected** and **seven optional** open rows. The selected
remaining total stays **175–394 active hours**: **95–194** non-documentation
plus **80–200** documentation. Both optional issue #101 helpers would add
**16–40 hours**, for a bounded **191–434** selected-plus-both total. The
all-options backlog has no finite estimate. The separate protected-path
decision for #139 and any future exception for #197 are outside these five
merges.

### Preparation and editing time for this checkpoint

Previous and new forecast-package estimates are both **1–2 active hours**;
the selected backlog estimate at start is **175–394 active hours**.
Read-only preparation began at **22:35:25 UTC**. Editing began after the
#196 merge in an isolated worktree based on that exact commit. Active-only
effort is not instrumented. Draft review completed at **22:41:54 UTC**,
**6m29s observed wall time** after preparation began. The independent
read-only audit checked all 21 open rows, arithmetic, five merge identities
and intervals, 547 tracked Markdown files, 103 local links and anchors,
historical preservation and section order. `python -B scripts/validate-skills.py`
reported 185 valid skills with zero warnings; `git diff --check` passed.
The forecast pull request records its final first-work-to-merge interval.

## Checkpoint after pull request #202 — 2026-09-23

Five requests merged after #196, in order #198, #199, #200, #201 and #202.
All times are September 23, 2026, in Coordinated Universal Time (UTC).
**ETA** means estimated time to complete a bounded package; **m** and **s**
mean minutes and seconds. Merge endpoints are GitHub pull-request `mergedAt`
events; first-work checkpoints come from the request body or timing comment.
The exact #202 merge is `867a4225cbeb72a2c06139adf7b1f7a2e19910b6`.

| Pull request and bounded package | Original ETA | First work (UTC) | Merge event (UTC) | Observed first-work-to-merge wall time |
| --- | ---: | ---: | ---: | ---: |
| [#198 — preceding forecast](https://github.com/ModernNomad-98/Project-Aegis/pull/198) | 1–2 active hours | 22:35:25 | 22:47:49 | 12m24s |
| [#199 — contributor merge guidance](https://github.com/ModernNomad-98/Project-Aegis/pull/199) | 1–3 active hours | Approximately 22:44 | 22:56:09 | About 12 minutes |
| [#200 — documentation backlog reading](https://github.com/ModernNomad-98/Project-Aegis/pull/200) | 1–2 active hours | 22:48:46 | 22:59:39 | 10m53s |
| [#201 — roadmap status and terms](https://github.com/ModernNomad-98/Project-Aegis/pull/201) | 1–3 active hours | Approximately 23:00 | 23:11:03 | About 11 minutes |
| [#202 — historical control-plane citations](https://github.com/ModernNomad-98/Project-Aegis/pull/202) | 2–4 active hours | 23:00:28 | 23:13:26 | 12m58s |
| **Five-merge cycle** | **No single combined active ETA** | **22:35:25 earliest work** | **23:13:26 last merge** | **38m01s overlapping span** |

The #199 and #201 preparation starts were recorded only to minute precision;
their observed intervals are therefore approximate. The five package intervals
overlap and include preparation, editing, independent review, checks,
integration and waits. Active effort and wait were not separately instrumented.
Do not sum the intervals as labor or use them to predict full-page documentation
or runtime implementation speed. Every package started with a selected-backlog
estimate of **175–394 active hours**.

The exact #202 tree has **551 tracked Markdown files**, four more than #196.
The four added files are dated evidence notes in #199–#202. The delivered
guidance corrected contributor approval reading, the documentation ledger,
roadmap status and terminology, and historical control-plane citations.
#201's status correction described the existing #134 grant; it did not grant
new authority. No selected implementation, private-label, provider or host
gate closed. #139 and #197 remain separate pending protected-path decisions.

All five final PR heads passed Linux, Windows and protected-file checks before
merge. Exact-main runs passed for #198
[35930285500](https://github.com/ModernNomad-98/Project-Aegis/actions/runs/35930285500),
#199 [35931009849](https://github.com/ModernNomad-98/Project-Aegis/actions/runs/35931009849),
#200 [35931291622](https://github.com/ModernNomad-98/Project-Aegis/actions/runs/35931291622),
and #201 [35932292490](https://github.com/ModernNomad-98/Project-Aegis/actions/runs/35932292490).
The #202 [main run 35932500973](https://github.com/ModernNomad-98/Project-Aegis/actions/runs/35932500973)
also completed successfully before this checkpoint was committed.

The [every-item forecast](aegis-backlog-forecast.md#five-merge-checkpoint--2026-09-23-after-pull-request-202)
reassesses all **14 selected** and **seven optional** rows. The selected
remaining total stays **175–394 active hours**: **95–194** non-documentation
plus **80–200** documentation. Both optional issue #101 helpers would add
**16–40 hours**, giving **191–434** selected-plus-both. All-options scope
remains unbounded. No estimate was narrowed from these short document PRs.

### Preparation and editing time for this checkpoint

Previous and new forecast-package estimates are both **1–2 active hours**;
the selected backlog at start is **175–394 active hours**. Preparation began
at about **23:14 UTC**, after #202 merged, and this isolated worktree was
created from that exact merge. Active-only effort is not instrumented.
Local checks, independent audit, pull-request checks and the final observed
first-work-to-merge interval will be recorded by the forecast pull request.

## Checkpoint after pull request #207 — 2026-09-23

Five requests merged after #202, in order #204, #203, #205, #206 and #207.
All times are September 23, 2026, in Coordinated Universal Time (UTC).
**ETA** means estimated time to complete a bounded package; **m** and **s**
mean minutes and seconds. Endpoints are GitHub pull-request `mergedAt`
events; preparation starts come from the request body or timing comment.
The exact #207 merge is `69c055bdb862f305b511fcef5a0120a1af8918c4`.

| Pull request and bounded package | Original ETA | First work (UTC) | Merge event (UTC) | Observed first-work-to-merge wall time |
| --- | ---: | ---: | ---: | ---: |
| [#204 — preceding five-merge forecast](https://github.com/ModernNomad-98/Project-Aegis/pull/204) | 1–2 active hours | Approximately 23:14 | 23:23:32 | About 9½ minutes |
| [#203 — user paths and acceptance runbook](https://github.com/ModernNomad-98/Project-Aegis/pull/203) | 1–2 active hours | Approximately 23:06 | 23:24:23 | About 18 minutes |
| [#205 — historical evidence reading](https://github.com/ModernNomad-98/Project-Aegis/pull/205) | 2–4 active hours | Approximately 23:20 | 23:28:26 | About 8½ minutes |
| [#206 — documentation progress accounting and batching](https://github.com/ModernNomad-98/Project-Aegis/pull/206) | 2–4 combined active hours | Approximately 23:24 | 23:39:23 | About 15 minutes |
| [#207 — nine-page full-checklist sample](https://github.com/ModernNomad-98/Project-Aegis/pull/207) | 2–4 active hours initially; 4–8 before page review | 23:35:27 | 23:56:59 | 21m32s |
| **Five-merge cycle** | **No single combined active ETA** | **Approximately 23:06 earliest work** | **23:56:59 last merge** | **About 51 minutes overlapping span** |

Four starts have minute-level precision, so their wall intervals and the
cycle span are approximate. The five intervals overlap and include page
selection, edits, independent review, GitHub checks and waits. Active-only
labor and queue time were not separately instrumented; do not add these
intervals as labor or extrapolate them to runtime work. Every package began
with a selected-backlog estimate of **175–394 active hours**.

At the exact #207 tree, **554 tracked Markdown files** exist. Pull requests
#203 and #205 corrected specific pages; #206 reconciled the 553-file
inventory and created a larger-batch workflow; #207 independently accepted
nine corrected pages against the documentation checklist. The
[nine-page evidence](../evidence/documentation/full-page-readability-sample-2026-09-23.md)
records disjoint reviewer intervals and limits. The other pages are not
implicitly accepted. None of the five PRs closed a non-documentation
implementation, private-label, provider or selected-host gate.

All five final PR heads passed Linux, Windows and protected-file checks before
merge. Exact-main runs passed for #204
[35933367116](https://github.com/ModernNomad-98/Project-Aegis/actions/runs/35933367116),
#203 [35933438019](https://github.com/ModernNomad-98/Project-Aegis/actions/runs/35933438019),
#205 [35933773787](https://github.com/ModernNomad-98/Project-Aegis/actions/runs/35933773787),
and #206 [35934669429](https://github.com/ModernNomad-98/Project-Aegis/actions/runs/35934669429).
The #207 [main run 35936082668](https://github.com/ModernNomad-98/Project-Aegis/actions/runs/35936082668)
also passed at the exact merge commit.

The [every-item forecast](aegis-backlog-forecast.md#five-merge-checkpoint--2026-09-23-after-pull-request-207)
reassesses all **14 selected** and **seven optional** rows. The
non-documentation subtotal remains **95–194 active hours**. The
documentation estimate is provisionally **55–200 active hours**, so the
selected total is **150–394 active hours**. These are scope-based estimates,
not a measured per-page throughput rate. The forecast states the residual
model and uncertainty; the full all-options
backlog remains unbounded. The separate owner decisions for #139, #197 and
the offline holdout grant are not counted as delivered implementation.

### Preparation and editing time for this checkpoint

Previous and new checkpoint estimates are both **1–2 active hours**. The
selected backlog estimate at start was **175–394 active hours**. Preparation
began after the #207 merge at approximately **23:57 UTC** in an isolated
worktree at that exact merge. The eventual forecast pull request will record
its final first-work-to-merge wall interval; active-only effort remains
separate and uninstrumented.

## Checkpoint after pull request #212 — 2026-09-24

Five requests merged after #207 in order #208, #209, #210, #211 and #212.
The exact #212 merge is `ba24016d209be6e49171be52332887558db16ab2`.
Times below are first-work-to-merge wall intervals recorded with those PRs;
they include review and GitHub waiting and are not active-work measurements.

| Pull request and bounded package | Merge commit | Original ETA | Observed wall time |
| --- | --- | ---: | ---: |
| [#208 — preceding forecast](https://github.com/ModernNomad-98/Project-Aegis/pull/208) | `754fc7a02f85c1f05dc32b4bbd70c1b616979b50` | 1–2 active hours | About 11m27s |
| [#209 — 21-page acceptance batch](https://github.com/ModernNomad-98/Project-Aegis/pull/209) | `f1bfaece5b68551f75e910470becd17ed61ccb7e` | 3–6 active hours | About 19m31s |
| [#210 — 20-page acceptance batch](https://github.com/ModernNomad-98/Project-Aegis/pull/210) | `80fbdbb4b6319dc1e7cafc9a57235a77360f9763` | 3–6 active hours | About 25m24s |
| [#211 — retry correction](https://github.com/ModernNomad-98/Project-Aegis/pull/211) | `2efae405d555815383abc1d9f713f3e4549eef84` | 1–2 active hours | About 10m29s |
| [#212 — 20-page acceptance batch](https://github.com/ModernNomad-98/Project-Aegis/pull/212) | `ba24016d209be6e49171be52332887558db16ab2` | 3–6 active hours | About 16m10s |

All exact-head Linux, Windows and protected-file checks passed. The #212
[exact-main run](https://github.com/ModernNomad-98/Project-Aegis/actions/runs/35942609209)
passed at the merge commit. The exact tree has **558 tracked Markdown pages**,
of which **71 existing pages** have recorded full-page acceptance and **487**
remain. The [every-item forecast](aegis-backlog-forecast.md#five-merge-checkpoint--2026-09-24-after-pull-request-212)
revisits all 14 selected and seven optional rows. Non-documentation remains
**95–194 active hours** because its implementation and authority gates did not
close. Documentation changes **55–200 → 50–175**, selected work **150–394 →
145–369**, and selected work plus both optional issue #101 helpers **166–434
→ 161–409 active hours**. The full all-options backlog remains unbounded.
PR #139 and #197 guard dispositions and the separate Behavioral Eval Runner
offline holdout implementation grant remain pending.

### Preparation and editing time for this checkpoint

The forecast-checkpoint item previously and currently estimates **1–2 active
hours**. Preparation began approximately **01:27 UTC** after verification of
the exact #212 main run. Active-only effort, review time and GitHub wait are
not separately instrumented; the checkpoint PR records the final observed
first-work-to-merge wall interval beside its original estimate.

## Documentation batch after pull request #213 — 2026-09-24

At approximately **01:37 UTC**, the next 20-page full-checklist batch began
from the exact #213 merge. Its comparable prior batch ETA and new item ETA
are both **3–6 active hours**. The selected backlog at start was **145–369
active hours**, including **50–175** for documentation. Two read-only agents
audited disjoint ten-page sets and independently reviewed corrections. The
[page-level evidence](../evidence/documentation/full-page-readability-batch-after-213-2026-09-24.md)
records 20 accepted existing pages and the scope limits. The interim
[forecast](aegis-backlog-forecast.md#documentation-batch-estimate--2026-09-24-after-pull-request-213)
is **140–364 selected active hours** after that candidate batch. Active-only,
review, CI and queue durations are not separately instrumented; the batch PR
will report observed first-work-to-merge wall time against the original ETA.

## Documentation batch after pull request #231 — 2026-09-24

The next 20-page full-checklist batch began from the exact #231 merge
`65384f04696c699881b2ff0294b6ce63711c85cf`. Its comparable prior
batch ETA and new item ETA are both **3–6 active hours**. Selected backlog
at start was **125–314 active hours**, including **30–120** for
documentation. Two read-only agents audited disjoint ten-page sets and
reviewed corrected pages. The
[page-level record](../evidence/documentation/full-page-readability-batch-after-231-2026-09-24.md)
records 20 existing-page outcomes and supporting entrypoint alignment. The
interim [forecast](aegis-backlog-forecast.md#documentation-batch-estimate--2026-09-24-after-pull-request-231)
narrows to **125–309 selected active hours**, with **30–115** for
documentation. Active-only, review, CI and queue durations are not
separately instrumented; the batch PR will report observed available wall
time against its original ETA. Independent corrected-candidate review,
exact-head Actions and merge remain required. This is the fifth merge
after #227 if merged; a full per-item checkpoint follows its exact tree.

## Documentation batch after pull request #230 — 2026-09-24

The next 20-page full-checklist batch began from the exact #230 merge
`275678c96f934aecb85c0b9e3c9fbce2b1490c23`. Its comparable prior
batch ETA and new item ETA are both **3–6 active hours**. Selected backlog
at start was **125–319 active hours**, including **30–125** for
documentation. Two read-only agents audited disjoint ten-page sets and
reviewed corrected pages. The
[page-level record](../evidence/documentation/full-page-readability-batch-after-230-2026-09-24.md)
records 20 existing-page outcomes and supporting reference alignment. The
interim [forecast](aegis-backlog-forecast.md#documentation-batch-estimate--2026-09-24-after-pull-request-230)
narrows to **125–314 selected active hours**, with **30–120** for
documentation. Active-only, review, CI and queue durations are not
separately instrumented; the batch PR will report observed available wall
time against its original ETA. Independent corrected-candidate review,
exact-head Actions and merge remain required. This is the fourth merge
after #227 if merged; the next full per-item checkpoint follows one more.

## Documentation batch after pull request #229 — 2026-09-24

The next 20-page full-checklist batch began from the exact #229 merge
`b949422c1c4aca65ecf809cc48ff2d9c78aeede6`. Its comparable prior
batch ETA and new item ETA are both **3–6 active hours**. Selected backlog
at start was **125–319 active hours**, including **30–125** for
documentation. Two read-only agents audited disjoint ten-page sets and
reviewed corrected pages. The
[page-level record](../evidence/documentation/full-page-readability-batch-after-229-2026-09-24.md)
records 20 existing-page outcomes and supporting reference alignment. The
interim [forecast](aegis-backlog-forecast.md#documentation-batch-estimate--2026-09-24-after-pull-request-229)
remains **125–319 selected active hours**, with **30–125** for
documentation. Active-only, review, CI and queue durations are not
separately instrumented; the batch PR will report observed available wall
time against its original ETA. Independent corrected-candidate review,
exact-head Actions and merge remain required. This is the third merge
after #227 if merged; the next full per-item checkpoint follows two more.

## Documentation batch after pull request #228 — 2026-09-24

The next 20-page full-checklist batch began from the exact #228 merge
`0bc4a8fcae32ccaab009ae9e0e23390ce4342f6a`. Its comparable prior
batch ETA and new item ETA are both **3–6 active hours**. Selected backlog
at start was **130–324 active hours**, including **35–130** for
documentation. Two read-only agents audited disjoint ten-page sets and
reviewed corrected pages. The
[page-level record](../evidence/documentation/full-page-readability-batch-after-228-2026-09-24.md)
records 20 existing-page outcomes and supporting reference alignment. The
interim [forecast](aegis-backlog-forecast.md#documentation-batch-estimate--2026-09-24-after-pull-request-228)
narrows to **125–319 selected active hours**, with **30–125** for
documentation. Active-only, review, CI and queue durations are not
separately instrumented; the batch PR will report observed available wall
time against its original ETA. Independent corrected-candidate review,
exact-head Actions and merge remain required. This is the second merge
after #227 if merged; the next full per-item checkpoint follows three more.

## Documentation batch after pull request #226 — 2026-09-24

The next 20-page full-checklist batch began from the exact #226 merge
`777f439327f6d9e3e602f1b42f25cd8a2cb7e7ac`. Its comparable prior
batch ETA and new item ETA are both **3–6 active hours**. Selected backlog
at start was **130–329 active hours**, including **35–135** for
documentation. Two read-only agents audited disjoint ten-page sets and
reviewed corrected pages. The
[page-level record](../evidence/documentation/full-page-readability-batch-after-226-2026-09-24.md)
records 20 existing-page outcomes and supporting reference alignment. The
interim [forecast](aegis-backlog-forecast.md#documentation-batch-estimate--2026-09-24-after-pull-request-226)
narrows to **130–324 selected active hours**, with **35–130** for
documentation. Active-only, review, CI and queue durations are not
separately instrumented; the batch PR will report observed available wall
time against its original ETA. Independent corrected-candidate review,
exact-head Actions and merge remain required. This is the fifth merge
after #222 if merged; the full per-item checkpoint follows its exact tree.

## Documentation batch after pull request #225 — 2026-09-24

The next 20-page full-checklist batch began from the exact #225 merge
`bc9e48b070fe99085757ce1d9cb0b791640e0d42`. Its comparable prior
batch ETA and new item ETA are both **3–6 active hours**. Selected backlog
at start was **130–334 active hours**, including **35–140** for
documentation. Two read-only agents audited disjoint ten-page sets and
reviewed corrected pages. The
[page-level record](../evidence/documentation/full-page-readability-batch-after-225-2026-09-24.md)
records 20 existing-page outcomes and supporting reference alignment. The
interim [forecast](aegis-backlog-forecast.md#documentation-batch-estimate--2026-09-24-after-pull-request-225)
narrows to **130–329 selected active hours**, with **35–135** for
documentation. Active-only, review, CI and queue durations are not
separately instrumented; the batch PR will report observed first-work-to-merge
wall time against its original ETA. Independent corrected-candidate review,
exact-head Actions and merge remain required.

## Documentation batch after pull request #224 — 2026-09-24

At approximately **04:31 UTC**, the next 20-page full-checklist batch began
from the exact #224 merge
`cf19639335158ffa09c02247d5d7b400f14fb522`. Its comparable prior
batch ETA and new item ETA are both **3–6 active hours**. Selected backlog
at start was **130–334 active hours**, including **35–140** for
documentation. Two read-only agents audited disjoint ten-page sets;
one previously accepted entrypoint was excluded and replaced before
acceptance counting. The
[page-level record](../evidence/documentation/full-page-readability-batch-after-224-2026-09-24.md)
records 20 existing-page outcomes and supporting reference/evaluation
alignment. The interim [forecast](aegis-backlog-forecast.md#documentation-batch-estimate--2026-09-24-after-pull-request-224)
remains **130–334 selected active hours**, with **35–140** for
documentation after outward rounding. Active-only, review, CI and queue
durations are not separately instrumented; the batch PR will report
observed wall time against its original ETA. Independent corrected-candidate
review, exact-head Actions and merge remain required.

## Documentation batch after pull request #223 — 2026-09-24

At approximately **04:12 UTC**, the next 20-page full-checklist batch began
from the exact #223 merge
`6ccf20a8d5cbcd355d27b4ebf38980d6724959ba`. Its comparable prior
batch ETA and new item ETA are both **3–6 active hours**. Selected backlog
at start was **135–339 active hours**, including **40–145** for
documentation. Two read-only agents audited disjoint ten-page sets;
two previously accepted references were excluded and replaced before
acceptance counting. The
[page-level record](../evidence/documentation/full-page-readability-batch-after-223-2026-09-24.md)
records 20 existing-page outcomes plus a supporting reference and owning
skill correction.
The interim [forecast](aegis-backlog-forecast.md#documentation-batch-estimate--2026-09-24-after-pull-request-223)
narrows to **130–334 selected active hours**, with **35–140** for
documentation. Active-only, review, CI and queue durations are not
separately instrumented; the batch PR will report observed wall time
against its original ETA. Independent corrected-candidate review,
exact-head Actions and merge remain required.

## Checkpoint after pull request #232 — 2026-09-24

The five-merge forecast checkpoint began from the exact #232 merge
`970aad27524bccc8a3f342bc990215904253be53`. The preceding checkpoint
and this bounded item each estimate **1–2 active hours**. The selected
remaining forecast at start and after the checkpoint is **125–309 active
hours**; the #227 checkpoint was **130–324**. The
[every-item forecast](aegis-backlog-forecast.md#five-merge-checkpoint--2026-09-24-after-pull-request-232)
reassesses 14 selected and seven optional rows. The exact merge tree has
**574 tracked Markdown pages**, **391** with recorded full-page acceptance
and **183** pending. Documentation is **30–115**; the unchanged other 13
selected rows total **95–194 active hours**. Independent read-only agents
checked the tree, category arithmetic, row estimates and authority gates.

| Merged PR | Original package ETA | Observed available wall interval | Exact-main Actions |
| --- | ---: | ---: | --- |
| [#228](https://github.com/ModernNomad-98/Project-Aegis/pull/228) | 1–2 active hours | 8m50s prior merge to merge; first-work start unavailable | [Passed](https://github.com/ModernNomad-98/Project-Aegis/actions/runs/35960351056) |
| [#229](https://github.com/ModernNomad-98/Project-Aegis/pull/229) | 3–6 active hours | 19m12s prior merge to merge; first-work start unavailable | [Passed](https://github.com/ModernNomad-98/Project-Aegis/actions/runs/35961765170) |
| [#230](https://github.com/ModernNomad-98/Project-Aegis/pull/230) | 3–6 active hours | 18m45s prior merge to merge; first-work start unavailable | [Passed](https://github.com/ModernNomad-98/Project-Aegis/actions/runs/35963177961) |
| [#231](https://github.com/ModernNomad-98/Project-Aegis/pull/231) | 3–6 active hours | 18m36s prior merge to merge; first-work start unavailable | [Passed](https://github.com/ModernNomad-98/Project-Aegis/actions/runs/35964645740) |
| [#232](https://github.com/ModernNomad-98/Project-Aegis/pull/232) | 3–6 active hours | 18m30s prior merge to merge; first-work start unavailable | [Passed](https://github.com/ModernNomad-98/Project-Aegis/actions/runs/35966166419) |

All five exact-head Linux, Windows and protected-file checks passed. The
five available intervals sum to **1h23m53s**, using GitHub `mergedAt`
receipts and the PR comments. They include work, review, CI and merge wait;
active labor, review, CI, queue and owner-wait splits were not separately
instrumented. They are not a throughput sample. No non-documentation
implementation or separate owner gate closed. PR #139 and #197 remain open
with failed protected-file guards, each requiring its own disposition. The
Behavioral Eval Runner holdout-executor implementation grant remains
separate; live/provider execution has further gates. This checkpoint PR
will report its observed available wall interval beside the original ETA
at merge.

## Checkpoint after pull request #227 — 2026-09-24

The five-merge forecast checkpoint began from the exact #227 merge
`88cc83fc547495b4f4d10eb5af76a4879c05af15`. The preceding checkpoint
and this bounded item each estimate **1–2 active hours**. The selected
remaining forecast at start and after the checkpoint is **130–324 active
hours**; the #222 checkpoint was **135–339**. The
[every-item forecast](aegis-backlog-forecast.md#five-merge-checkpoint--2026-09-24-after-pull-request-227)
reassesses 14 selected and seven optional rows. The exact merge tree has
**570 tracked Markdown pages**, **311** with recorded full-page acceptance
and **259** pending. Documentation is **35–130**; the unchanged other 13
selected rows total **95–194 active hours**. Independent read-only agents
checked the tree, category arithmetic, row estimates and authority gates.

| Merged PR | Original package ETA | Observed available wall interval | Exact-main Actions |
| --- | ---: | ---: | --- |
| [#223](https://github.com/ModernNomad-98/Project-Aegis/pull/223) | 1–2 active hours | About 9m27s first work to merge | [Passed](https://github.com/ModernNomad-98/Project-Aegis/actions/runs/35954390925) |
| [#224](https://github.com/ModernNomad-98/Project-Aegis/pull/224) | 3–6 active hours | About 19m15s first work to merge | [Passed](https://github.com/ModernNomad-98/Project-Aegis/actions/runs/35955760887) |
| [#225](https://github.com/ModernNomad-98/Project-Aegis/pull/225) | 3–6 active hours | About 20m20s first work to merge | [Passed](https://github.com/ModernNomad-98/Project-Aegis/actions/runs/35957203119) |
| [#226](https://github.com/ModernNomad-98/Project-Aegis/pull/226) | 3–6 active hours | 16m44s prior merge to merge; first-work start unavailable | [Passed](https://github.com/ModernNomad-98/Project-Aegis/actions/runs/35958384698) |
| [#227](https://github.com/ModernNomad-98/Project-Aegis/pull/227) | 3–6 active hours | 17m54s prior merge to merge; first-work start unavailable | [Passed](https://github.com/ModernNomad-98/Project-Aegis/actions/runs/35959689686) |

All five exact-head Linux, Windows and protected-file checks passed. The
five available intervals sum to **1h23m40s**, mixing three observed
first-work-to-merge intervals with two prior-merge-to-merge intervals.
They include review, CI and merge wait, and are neither active labor nor a
comparable throughput sample. No non-documentation implementation or
separate owner gate closed. PR #139 and #197 remain open with failed
protected-file guards, each requiring its own disposition. The Behavioral
Eval Runner holdout-executor implementation grant remains separate;
live/provider execution has further gates. Active-only effort, review, CI
and queue durations were not separately instrumented for this checkpoint;
the checkpoint PR will report its observed available wall interval beside
the original ETA at merge.

## Checkpoint after pull request #222 — 2026-09-24

At approximately **04:00 UTC**, the five-merge forecast checkpoint began
from the exact #222 merge
`7a913818c49bd0d5ee4a07faee6cb75bc0b524de`. The preceding checkpoint
and this bounded item each estimate **1–2 active hours**. The selected
remaining forecast at start and after the checkpoint is **135–339 active
hours**; the #217 checkpoint was **135–354**. The
[every-item forecast](aegis-backlog-forecast.md#five-merge-checkpoint--2026-09-24-after-pull-request-222)
reassesses 14 selected and seven optional rows. The exact merge tree has
**566 tracked Markdown pages**, **231** with recorded full-page acceptance
and **335** pending. Documentation is **40–145**; the unchanged other 13
selected rows total **95–194 active hours**. Independent read-only agents
checked the tree, category arithmetic, row estimates and authority gates.

| Merged PR | Original package ETA | Observed first-work-to-merge wall time | Exact-main Actions |
| --- | ---: | ---: | --- |
| [#218](https://github.com/ModernNomad-98/Project-Aegis/pull/218) | 1–2 active hours | About 6m41s | [Passed](https://github.com/ModernNomad-98/Project-Aegis/actions/runs/35949023976) |
| [#219](https://github.com/ModernNomad-98/Project-Aegis/pull/219) | 3–6 active hours | About 14m57s | [Passed](https://github.com/ModernNomad-98/Project-Aegis/actions/runs/35950164559) |
| [#220](https://github.com/ModernNomad-98/Project-Aegis/pull/220) | 3–6 active hours | About 15m48s | [Passed](https://github.com/ModernNomad-98/Project-Aegis/actions/runs/35951339362) |
| [#221](https://github.com/ModernNomad-98/Project-Aegis/pull/221) | 3–6 active hours | About 17m27s | [Passed](https://github.com/ModernNomad-98/Project-Aegis/actions/runs/35952498930) |
| [#222](https://github.com/ModernNomad-98/Project-Aegis/pull/222) | 3–6 active hours | About 17m49s | [Passed](https://github.com/ModernNomad-98/Project-Aegis/actions/runs/35953714246) |

All five exact-head Linux, Windows and protected-file checks and all five
exact-main runs passed. The
five reported wall intervals total about **1h12m42s** of package wall time;
they include review, CI and merge wait and are not active labor or a
throughput estimate. No non-documentation implementation or separate owner
gate closed. PR #139 and #197 remain open with failed protected-file
guards, each requiring its own disposition. The Behavioral Eval Runner
holdout-executor implementation grant remains separate; live/provider
execution has further gates. Active-only effort, review, CI and queue
durations were not separately instrumented for the current checkpoint;
the checkpoint PR will report its observed wall interval beside the
original ETA at merge.

## Documentation batch after pull request #221 — 2026-09-24

At approximately **03:42 UTC**, the next 20-page full-checklist batch began
from the exact #221 merge
`c0a3d1d4de64ce9f7307c22d2dbddaaf149c6239`. Its comparable prior
batch ETA and new item ETA are both **3–6 active hours**. Selected backlog
at start was **135–344 active hours**, including **40–150** for
documentation. Two read-only agents audited disjoint ten-page sets. The
[page-level record](../evidence/documentation/full-page-readability-batch-after-221-2026-09-24.md)
records 20 existing-page outcomes and fixture exclusion. The interim
[forecast](aegis-backlog-forecast.md#documentation-batch-estimate--2026-09-24-after-pull-request-221)
narrows to **135–339 selected active hours**, with **40–145** for
documentation. Active-only, review, CI and queue durations are not
separately instrumented; the batch PR will report observed wall time against
its original ETA. Independent corrected-candidate review, exact-head Actions
and merge are pending. The next full forecast checkpoint follows this batch
if it becomes the fifth completed merge after #217.

## Documentation batch after pull request #220 — 2026-09-24

At approximately **03:24 UTC**, the next 20-page full-checklist batch began
from the exact #220 merge
`afe5f456ccf20cba8a8cf3e168fdfd547dd1b80c`. Its comparable prior
batch ETA and new item ETA are both **3–6 active hours**. Selected backlog
at start was **135–349 active hours**, including **40–155** for
documentation. Two read-only agents audited disjoint ten-page sets. The
[page-level record](../evidence/documentation/full-page-readability-batch-after-220-2026-09-24.md)
records 20 existing-page outcomes and scope limits. The interim
[forecast](aegis-backlog-forecast.md#documentation-batch-estimate--2026-09-24-after-pull-request-220)
narrows to **135–344 selected active hours**, with **40–150** for
documentation. Active-only, review, CI and queue durations are not
separately instrumented; the batch PR will report observed wall time against
its original ETA. Independent corrected-candidate review, exact-head Actions
and merge are pending.

## Documentation batch after pull request #219 — 2026-09-24

At approximately **03:09 UTC**, the next 20-page full-checklist batch began
from the exact #219 merge
`dbad6c25c11179489c6c8f78aca387a3b768995c`. Its comparable prior
batch ETA and new item ETA are both **3–6 active hours**. Selected backlog
at start was **135–349 active hours**, including **40–155** for
documentation. Two read-only agents audited disjoint ten-page sets. The
[page-level record](../evidence/documentation/full-page-readability-batch-after-219-2026-09-24.md)
records 20 existing-page outcomes and scope limits. The interim
[forecast](aegis-backlog-forecast.md#documentation-batch-estimate--2026-09-24-after-pull-request-219)
remains **135–349 selected active hours**, with **40–155** for documentation.
Active-only, review, CI and queue durations are not separately instrumented;
the batch PR will report observed wall time against its original ETA.
Independent corrected-candidate review, exact-head Actions and merge are
pending.

## Documentation batch after pull request #218 — 2026-09-24

At approximately **02:53 UTC**, the next 20-page full-checklist batch
began from the exact #218 merge
`694333c0b7ebc697272b03705700c845fcc6462a`. Its comparable
prior batch ETA and new item ETA are both **3–6 active hours**.
Selected backlog at start was **135–354 active hours**, including
**40–160** for documentation. Two read-only agents audited disjoint
ten-page sets. The
[page-level record](../evidence/documentation/full-page-readability-batch-after-218-2026-09-24.md)
records 20 existing-page outcomes and scope limits. The interim
[forecast](aegis-backlog-forecast.md#documentation-batch-estimate--2026-09-24-after-pull-request-218)
narrows to **135–349 selected active hours**, with **40–155** for
documentation. Active-only, review, CI and queue durations are not
separately instrumented; the batch PR will report observed wall time
against its original ETA. Independent corrected-candidate review,
exact-head Actions and merge are pending.

## Checkpoint after pull request #217 — 2026-09-24

At approximately **02:45 UTC**, the five-merge checkpoint began from the
exact #217 merge
`f6a05e97b68108a9de0c81f37ce48b8ffe55d78c`. The preceding
checkpoint and this bounded item were each estimated at **1–2 active
hours**. Selected remaining work before and after the checkpoint is
**135–354 active hours**; the earlier #212 checkpoint was **145–369**.
The [every-item forecast](aegis-backlog-forecast.md#five-merge-checkpoint--2026-09-24-after-pull-request-217)
reassesses 14 selected and seven optional rows. The #217 merge tree has
**562 tracked Markdown pages**, **151** with recorded full-page
acceptance and **411** pending. The documentation model is **40–160**,
and the unchanged other 13 selected rows total **95–194**. Two
independent read-only agents checked tree arithmetic and merge receipts.

| Merged PR | Original package ETA | Observed first-work-to-merge wall time | Exact-main Actions |
| --- | ---: | ---: | --- |
| [#213](https://github.com/ModernNomad-98/Project-Aegis/pull/213) | 1–2 active hours | About 9m48s | [Passed](https://github.com/ModernNomad-98/Project-Aegis/actions/runs/35943696676) |
| [#214](https://github.com/ModernNomad-98/Project-Aegis/pull/214) | 3–6 active hours | About 17m50s | [Passed](https://github.com/ModernNomad-98/Project-Aegis/actions/runs/35944985873) |
| [#215](https://github.com/ModernNomad-98/Project-Aegis/pull/215) | 3–6 active hours | About 12m50s | [Passed](https://github.com/ModernNomad-98/Project-Aegis/actions/runs/35945938499) |
| [#216](https://github.com/ModernNomad-98/Project-Aegis/pull/216) | 3–6 active hours | About 15m04s | [Passed](https://github.com/ModernNomad-98/Project-Aegis/actions/runs/35947300449) |
| [#217](https://github.com/ModernNomad-98/Project-Aegis/pull/217) | 3–6 active hours | About 16m07s | [Passed](https://github.com/ModernNomad-98/Project-Aegis/actions/runs/35948498380) |

All five exact-head Linux, Windows and protected-file checks passed.
The five observed intervals total about **1h11m39s** of package wall
time; do not treat that sum as active labor or a throughput estimate.
No non-documentation implementation or separate owner gate closed.
PR #139 and #197 remain open with failed protected-file guards; each
needs its separate owner disposition. The Behavioral Eval Runner
holdout-executor implementation grant remains separate; live/provider
execution has further gates. The checkpoint PR will report
its own observed wall interval at merge.

## Documentation batch after pull request #216 — 2026-09-24

At approximately **02:28 UTC**, the next 20-page full-checklist batch began
from the exact #216 merge
`d759f26527017574154a23c0748e659a75ef8b71`. Its comparable prior
batch ETA and new item ETA are both **3–6 active hours**. Selected backlog
at start was **140–359 active hours**, including **45–165** for
documentation. Two read-only agents audited disjoint ten-page sets. The
[page-level record](../evidence/documentation/full-page-readability-batch-after-216-2026-09-24.md)
records 20 existing-page outcomes and scope limits. The interim
[forecast](aegis-backlog-forecast.md#documentation-batch-estimate--2026-09-24-after-pull-request-216)
narrows to **135–354 selected active hours**, with **40–160** for
documentation. Active-only, review, CI and queue durations are not
separately instrumented; the batch PR will report observed wall time
against its original ETA. Independent corrected-candidate review,
exact-head Actions and merge are pending.

## Documentation batch after pull request #215 — 2026-09-24

At approximately **02:12 UTC**, the next 20-page full-checklist batch began
from the exact #215 merge
`4e09c54b511a43672c282bc75c41061ec4f2f878`. Its comparable prior
batch ETA and new item ETA are both **3–6 active hours**. Selected backlog
at start was **140–364 active hours**, including **45–170** for
documentation. Two read-only agents audited disjoint ten-page sets. The
[page-level record](../evidence/documentation/full-page-readability-batch-after-215-2026-09-24.md)
records 20 existing-page outcomes and scope limits. The interim
[forecast](aegis-backlog-forecast.md#documentation-batch-estimate--2026-09-24-after-pull-request-215)
narrows to **140–359 selected active hours**, with **45–165** for
documentation. Active-only, review, CI and queue durations are not
separately instrumented; the batch PR will report observed wall time
against its original ETA. Independent corrected-candidate review,
exact-head Actions and merge are pending.

## Documentation batch after pull request #214 — 2026-09-24

At approximately **01:55 UTC**, the next 20-page full-checklist batch began
from the exact #214 merge. Its comparable prior batch ETA and new item ETA
are both **3–6 active hours**. Selected backlog at start was **140–364
active hours**, including **45–170** for documentation. Two read-only agents
audited disjoint ten-page sets and independently reviewed corrections.
The [page-level record](../evidence/documentation/full-page-readability-batch-after-214-2026-09-24.md)
records 20 accepted existing pages and the scope limits. The interim
[forecast](aegis-backlog-forecast.md#documentation-batch-estimate--2026-09-24-after-pull-request-214)
remains **140–364 selected active hours** after outward rounding; the raw
documentation model narrowed from 48.35–168.85 to 47.15–165.1 hours.
Active-only, review, CI and queue durations are not separately instrumented;
the batch PR will report observed first-work-to-merge wall time against its
original ETA.
