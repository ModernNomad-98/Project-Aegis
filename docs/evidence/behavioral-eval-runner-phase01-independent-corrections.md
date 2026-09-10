# Phase 0/1 independent-review corrections

2026-09-10. Independent read-only review of local commit
`40bfabc91b60d46f201a575911d0f2a9edac2a2e` (tree
`a9e12ad61aafb0434bf36e256553fdf634c58053`) requested changes. The reviewer
inspected all 12 PR88 findings, four PR87 reconciliation rows and 35 decision
mappings, and independently passed 153 offline tests with one skip.

## Confirmed findings and corrections

1. Malformed usage escaped typed stopping. Negative counts could discard a
   pending reservation before accounting; strings could raise conversion
   exceptions; booleans/fractions could be silently coerced. Raw token values
   now receive strict validation. Unusable usage follows the existing missing
   telemetry path: worst-case reserved charge, terminal evidence and durable
   BUDGET_TELEMETRY_UNAVAILABLE / RUN_STOPPED. Reservation consumption and
   in-memory terminal accounting occur only after successful durable append.
2. The SDK's `Timeout(300, connect=15)` limits individual I/O operations, not
   total request time required by the approved package section F, decision 4.
   The same pinned official SDK now uses its asynchronous client through a
   synchronous facade with an owned event loop and a 300-second total I/O
   deadline. Cancellation unwinds and closes the response before control
   returns to the accounting/retry owner. The live driver closes the client
   and event loop on exit. No request is abandoned in a worker thread.
3. Preliminary review caught a completed-response edge case in the deadline
   correction. Completion after the deadline preserves the received response
   and actual usage, records DEADLINE_EXCEEDED / RUN_STOPPED and never retries.
   Late metadata is accounted for but cannot establish METADATA_OK.

The static scanner permits `asyncio` only in the calibration transport and its
two named test modules. Tests prove sibling/suffix paths and other forbidden
imports remain denied. Provider/model/SDK pins, dependencies, request settings,
credential mechanism, budgets and thresholds are unchanged. The transport
implementation changes intentionally supersede the earlier no-transport-change
observation; no historical authorization text is rewritten.

## Test-first evidence

Commands run from the implementation worktree. `<sdk-python>` denotes the
existing isolated `../phase01-sdk-venv/Scripts/python.exe`.

- `python -B ../run_phase01_checks.py focused`: telemetry RED, 154 tests,
  14 failures / 17 errors / one skip. Failures included `CalibrationStopError
  not raised`, negative-count validation, and string/nonfinite conversion
  errors. After strict validation, GREEN: 154 tests, one skip.
- `python -B -m unittest tools.behavioral_eval_runner.tests.test_calibration_ledger.TestTerminalAccounting`:
  RED: both validation and fsync regressions reported `True is not false` for
  consumed reservation. GREEN: two tests passed after moving consumption.
- `<sdk-python> -B -m unittest tools.behavioral_eval_runner.tests.test_calibration_transport.TestPinnedSdkClientConfiguration.test_total_deadline_cancels_slow_body_before_returning`:
  RED: metadata and judgment slow bodies failed with `APITimeoutError not raised`.
  GREEN: six SDK configuration/deadline tests passed after adding cancellation.
- Completed-late-response and narrow static-allowlist regressions were RED
  before their corrections. GREEN: retry/configuration/static subset passed
  25 tests; metadata/calibration-static subset passed 14 tests.
- Real pinned-SDK tests use synthetic in-memory HTTP responses, including a
  stalled body. They prove cancellation cleanup precedes the accounted retry.
  No socket or provider request is needed.

Final full verification passed:

- Windows with pinned SDK: 961 tests, 13 skips, 192.621 seconds.
- Unprivileged network-disabled POSIX container: 961 tests, 11 skips, 28.219
  seconds; container exit code 0 captured directly by the host harness.
- Validator self-tests: 91 assertions; 184 skills valid with zero warnings;
  contract self-tests: 50 assertions; runner self-check: 21/21; diff check clean.

An earlier full POSIX attempt exposed the missing narrow asyncio scanner
exception; it passed after the correction. The concurrent Windows attempt was
interrupted once that failure was known, then rerun to completion above.
PowerShell initially translated passing POSIX unittest stderr into a misleading
host failure; direct subprocess capture established the final container status.
Final exact-commit independent review remains a separate gate.

Independent review of `c6822e1c3fd0dd2b8195c3909c1cf57faeab6607` approved with
one minor evidence-fidelity finding; 20 independently run pinned-SDK tests
passed without skips. The final follow-up preserves `incomplete_details.reason`
on late incomplete responses. Its regression first failed with
`None != 'max_output_tokens'`, then passed with the complete provider,
transport, ledger and calibration-static suites: 127 tests, no skips,
42.007 seconds. Command: `<sdk-python> -B -m unittest
tools.behavioral_eval_runner.tests.test_calibration_provider
tools.behavioral_eval_runner.tests.test_calibration_transport
tools.behavioral_eval_runner.tests.test_calibration_ledger
tools.behavioral_eval_runner.tests.test_static_safety_calibration`.
The full platform results above apply to c6822e1; this final small field
preservation change was verified with the targeted suite rather than repeating
unaffected full-suite checks. Final follow-up exact-head review is pending.

## Scope of the evidence

The deadline covers cooperative asynchronous SDK/network I/O and rejects late
completed responses. It does not forcibly interrupt arbitrary blocking Python
or native code, or certify whole-process containment. Real evidence-root ACLs,
encryption, live SDK/provider behavior, credential injection and measured
calibration remain future execution gates. No real credential, dataset/holdout,
provider call, push, merge, publication or remote comment occurred. WP-2B-3 is
not DONE; OD-1 remains OPEN and WP-2B-4 remains BLOCKED.
