# Project Aegis execution measurements

Record an estimate when each new work package starts. In its PR, record the
estimated active time, actual active time, review and CI time, owner waiting,
and meaningful progress checkpoints. Use observed timestamps rather than
reconstructed precision. A range is an estimate, not a delivery promise.

| Work package | First recorded checkpoint (UTC) | Estimated active work | Actual active work | Review / CI | Owner waiting | Status |
| --- | --- | --- | --- | --- | --- | --- |
| BER-BKL-007 authorization (WP-2B-1A governance) | 2026-09-23 10:52 | 20–30 minutes remaining at checkpoint; earlier start was not timed | At least 5 minutes 14 seconds from first timed checkpoint to merge; earlier active time unknown | Independent review passed; Linux 1m24s, Windows 3m14s, guard 4s | 0 during PR | Merged PR #103 at 10:57:14 UTC |
| BER-BKL-007 implementation | 2026-09-23 10:57 | 3–5 hours active work | Pending | Pending | 0 so far | In progress |

## Progress checkpoints

- **2026-09-23 10:52 UTC — authorization:** The scope record was drafted,
  independently reviewed and corrected; structural validation passed. The
  governance branch was committed and pushed. This is the first timed
  checkpoint; the preceding work has no measured start timestamp.
- **2026-09-23 10:57 UTC — authorization merged:** PR #103 was green and
  independently reviewed, then merged at `f82a4bc`. Its PR comment records
  the lower-bound elapsed time and per-job CI durations.
- **2026-09-23 11:05 UTC — BER-BKL-007 implementation:** The implementation
  branch is based on that exact merge. Regressions reproduced the missing and
  unknown-version gaps; focused tests pass after changes. The first full BER
  suite reached 994 tests but had 12 sandbox-environment errors (nested Git
  ownership and a synthetic child-process kill). A command-scoped trust and
  unsandboxed rerun are pending. Independent implementation audit is underway.
- **2026-09-23 11:14 UTC — final local suites:** After the independent audit's
  checkpoint and nested-report findings were fixed, the final BER suite passed
  997 tests (14 skips). The unchanged control-plane suite passed 543 tests.
  Structural validation and BER self-check passed. Active time since the
  10:57 UTC implementation checkpoint is about 17 minutes; local acceptance,
  PR review and CI remain.
- **2026-09-23 11:15 UTC — local acceptance:** Windows PowerShell Desktop
  acceptance passed all 113 checks. PowerShell Core is unavailable locally;
  the hosted Windows Actions job will provide that coverage.
- **2026-09-23 11:20 UTC — PR #104 first candidate checks:** From the 10:57
  implementation checkpoint to the hosted result, about 23 minutes elapsed.
  Linux passed in 1m23s and Windows in 2m52s; the protected-file guard failed
  in 5s on its documented manual-review condition. Engineering and local
  verification overlapped, so exact active-only minutes are not available.
  Owner waiting began for schema-shape acceptance and the guard exception.
- **2026-09-23 11:21 UTC — partial owner decision:** Peter Nguyen permitted
  the narrow PR #104 guard exception. Final schema-shape acceptance remains
  pending. The decision is recorded as AEGIS-APR-005.

Append later observations and final actuals in the relevant PR. Keep provider
or model token/credit usage as unknown when the runtime does not expose it.
