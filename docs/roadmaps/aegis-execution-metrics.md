# Project Aegis execution measurements

Record an estimate when each new work package starts. In its PR, record the
estimated active time, actual active time, review and CI time, owner waiting,
and meaningful progress checkpoints. Use observed timestamps rather than
reconstructed precision. A range is an estimate, not a delivery promise.

| Work package | First recorded checkpoint (UTC) | Estimated active work | Actual active work | Review / CI | Owner waiting | Status |
| --- | --- | --- | --- | --- | --- | --- |
| BER-BKL-007 authorization (WP-2B-1A governance) | 2026-09-23 10:52 | 20–30 minutes remaining at checkpoint; earlier start was not timed | Pending; earlier active time unknown | Pending | Pending | PR preparation |
| BER-BKL-007 implementation | Not started | 3–5 hours active work after authorization merge | Pending | Pending | Pending | Gated by authorization merge |
| Calibration replacement storage proposal | 2026-09-23 11:26 | 30–45 minutes active work | Exact active total unavailable; 12m50s observed wall time to merge at 11:38:50 | Independent review passed; final Actions green (Linux 1m24s, Windows 3m11s, guard 5s) | About 1 minute before owner chose A | PR #105 merged; choice A recorded |
| Private input storage amendment (BER-DEC-010) | 2026-09-23 11:39 | 20–40 minutes active work to review and merge-ready PR | In progress | Pending | None recorded | Governance branch from exact PR #105 merge |
| Calibration replacement candidate packet | Not started; contract inspected 2026-09-23 11:20 | TBD when storage and input authority are settled; prior 4–8 hour forecast withdrawn | Pending | Pending | Pending | Input publication gated by storage decision |

## Progress checkpoints

- **2026-09-23 10:52 UTC — authorization:** The scope record was drafted,
  independently reviewed and corrected; structural validation passed. The
  governance branch was committed and pushed. This is the first timed
  checkpoint; the preceding work has no measured start timestamp.
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

Append later observations and final actuals in the relevant PR. Keep provider
or model token/credit usage as unknown when the runtime does not expose it.
