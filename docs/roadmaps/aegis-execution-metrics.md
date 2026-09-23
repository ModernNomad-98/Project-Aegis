# Project Aegis execution measurements

Record an estimate when each new work package starts. In its PR, record the
estimated active time, actual active time, review and CI time, owner waiting,
and meaningful progress checkpoints. Use observed timestamps rather than
reconstructed precision. A range is an estimate, not a delivery promise.

| Work package | First recorded checkpoint (UTC) | Estimated active work | Actual active work | Review / CI | Owner waiting | Status |
| --- | --- | --- | --- | --- | --- | --- |
| BER-BKL-007 authorization (WP-2B-1A governance) | 2026-09-23 10:52 | 20–30 minutes remaining at checkpoint; earlier start was not timed | Pending; earlier active time unknown | Pending | Pending | PR preparation |
| BER-BKL-007 implementation | Not started | 3–5 hours active work after authorization merge | Pending | Pending | Pending | Gated by authorization merge |
| Calibration replacement storage proposal | 2026-09-23 11:26 | 30–45 minutes active work | Pending | Pending | Pending | Drafting owner decision |
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

Append later observations and final actuals in the relevant PR. Keep provider
or model token/credit usage as unknown when the runtime does not expose it.
