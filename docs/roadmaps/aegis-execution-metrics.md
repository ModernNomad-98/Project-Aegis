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
| Calibration replacement candidate packet | 2026-09-23 11:47 | 4–8 hours active work | In progress | Pending | None recorded | Private repository created and verified; branch from exact BER-DEC-010 merge |

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

Append later observations and final actuals in the relevant PR. Keep provider
or model token/credit usage as unknown when the runtime does not expose it.
