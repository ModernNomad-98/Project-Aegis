# Project Aegis execution measurements

Record an estimate when each new work package starts. In its PR, record the
estimated active time, actual active time, review and CI time, owner waiting,
and meaningful progress checkpoints. Use observed timestamps rather than
reconstructed precision. A range is an estimate, not a delivery promise.

After every five merged PRs following #106, re-estimate each open work item
and the total in the [backlog forecast](aegis-backlog-forecast.md) from these
measurements and the corresponding PR records. Record the five merge commits,
scope changes and uncertainty. A material owner decision also triggers an
earlier forecast update.

| Work package | First recorded checkpoint (UTC) | Estimated active work | Actual active work | Review / CI | Owner waiting | Status |
| --- | --- | --- | --- | --- | --- | --- |
| BER-BKL-007 authorization (WP-2B-1A governance) | 2026-09-23 10:52 | 20–30 minutes remaining at checkpoint; earlier start was not timed | At least 5m14s observed wall time to PR #103 merge; earlier active time unknown | Independent review and all three Actions passed | None recorded | PR #103 merged at 10:57:14 UTC |
| BER-BKL-007 implementation | 2026-09-23 10:57 | 3–5 hours active work after authorization merge | Active-only total unavailable; about 28 minutes observed wall time to first final-candidate CI | Independent audit passed after corrections; PR #104 Linux and Windows pass, protected-file guard fails under recorded narrow exception | Awaiting owner schema-shape decision | PR #104 open; BKL-007 not DONE |
| Calibration replacement storage proposal | 2026-09-23 11:26 | 30–45 minutes active work | Exact active total unavailable; 12m50s observed wall time to merge at 11:38:50 | Independent review passed; final Actions green (Linux 1m24s, Windows 3m11s, guard 5s) | About 1 minute before owner chose A | PR #105 merged; choice A recorded |
| Private input storage amendment (BER-DEC-010) | 2026-09-23 11:39 | 20–40 minutes active work to review and merge-ready PR | Exact active total unavailable; 8m21s observed wall time to merge at 11:47:21 | Independent audit passed after correction; final Actions guard 4s, Linux 1m18s, Windows 2m55s | None recorded | PR #106 merged |
| Calibration replacement candidate packet | 2026-09-23 11:47 | 4–8 hours active work | 33m20s observed wall time to public PR #107 merge; active-only total unavailable | Private PR #1 open; local contract/restore checks passed; public PR #107 independent audit and all Actions passed | Owner semantic review pending | Private packet PENDING; public checkpoint merged |
| Cross-stream owner decision packet | 2026-09-23 12:20 | 2–4 hours active work | 13m38s observed wall time to PR #108 merge; active-only time unavailable | Independent read-only audit passed; all three Actions green | BKL-009 owner selection pending after merge | PR #108 merged at 12:33:38 UTC; BKL-009 remains PARTIAL |
| Issue #101 package 1 design | 2026-09-23 12:34 | 4–8 hours active work | 9m40s observed wall time to PR #109 merge; active-only time unavailable | Independent read-only audit passed; all three Actions green | No runtime authorization requested | PR #109 merged at 12:43:40 UTC; planning only |
| CP-WP-003A offline proof scope proposal | 2026-09-23 12:44 | 2–4 hours active work | 8m58s observed wall time to PR #110 merge; active-only time unavailable | Independent read-only audit passed after terminology correction; all three Actions green | Owner authorization needed before code | PR #110 merged at 12:52:58 UTC; CP-WP-003 BLOCKED |
| BER R4/R5 selected-host decision packet | 2026-09-23 12:53 | 2–4 hours active work | In progress | Pending | Host choice and later probe grant pending | Proposal only; no host probe or live dispatch |

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

Append later observations and final actuals in the relevant PR. Keep provider
or model token/credit usage as unknown when the runtime does not expose it.
