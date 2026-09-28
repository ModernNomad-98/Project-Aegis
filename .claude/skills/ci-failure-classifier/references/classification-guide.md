# CI failure classification guide

Detail for `ci-failure-classifier`. Read on demand when a job's class is not
obvious. The signatures below are examples, not an exhaustive list; the rule
is always "quote the line that decided it".

## Ordering rule

Apply the classes in this order and stop at the first that the evidence
supports. The order exists because earlier classes explain later symptoms:
a missing secret makes tests fail, and a lost runner makes a job time out.

1. `MISSING-SECRET-OR-CONFIG`
2. `INFRASTRUCTURE`
3. `TIMEOUT-ONLY`
4. `SKIPPED-RUNTIME`
5. `TEST-BUG`
6. `PRODUCT-BUG`
7. `INDETERMINATE`

A later class wins over an earlier one only when the log shows the earlier
signal was a consequence, not the cause. Example: a 401 that appears only
after the product's own login endpoint returned the wrong token is a product
symptom, not a missing secret.

## Per-class signatures

| Class | Typical deciding lines | Common false match |
| --- | --- | --- |
| `MISSING-SECRET-OR-CONFIG` | `Error: Input required and not supplied: token`; `environment variable DATABASE_URL is not set`; an empty `***` value where a secret is expected; 401/403 from a registry, cloud provider or third-party API the job reaches with its own credential; secrets unavailable to pull requests from forks | A 401 from the product's own authentication under test |
| `INFRASTRUCTURE` | `The runner has received a shutdown signal`; `lost communication with the server`; `No space left on device`; `ECONNRESET` or domain name system (DNS) failure reaching a package mirror; `429 Too Many Requests` from a registry; image pull failure; service container health check never passing | A product service that crashes on start (that is product code) |
| `TIMEOUT-ONLY` | `The job running on runner ... has exceeded the maximum execution time of 30 minutes`; `Error: The operation was canceled.` at the limit; test runner "timed out waiting" with every earlier test passing | A timeout that follows failed assertions (classify by the assertions) |
| `SKIPPED-RUNTIME` | `0 passing`; `Ran 0 tests`; `No tests found`; a required job shown as skipped because a path filter or condition excluded it; a whole suite marked `skip` by an environment flag; the report step that decides the verdict never ran | A skip that the workflow declares on purpose for a docs-only change (state it; it is not hidden) |
| `TEST-BUG` | locator or fixture not found after a known interface change; expectation that contradicts the written requirement; test depends on order or shared state; failure in `beforeAll` or setup before product code is exercised | A product change that legitimately broke a correct test (that is `PRODUCT-BUG`) |
| `PRODUCT-BUG` | assertion failure with expected and actual values on specified behavior; stack trace whose top frames are in application code; unhandled rejection raised by product code; wrong status code or response body | A stack trace inside the test helper (that is `TEST-BUG`) |
| `INDETERMINATE` | log truncated before the first abnormal line; no log for the job; two classes equally supported | — |

## Hidden markers in green runs

Scan every passing job for these. Any one makes the run
`GREEN-WITH-FINDINGS`.

- Console errors printed by the application or browser during tests
  (`console.error`, `[error]`, React or framework warnings that are errors in
  production).
- `UnhandledPromiseRejection`, `unhandledRejection`, `Uncaught`, `panic`
  lines that did not fail the job.
- Unexpected skips: the skipped count rose against the comparison run, or
  tests were skipped without a written reason.
- Authentication failures swallowed by a retry or a fallback path.
- "0 tests", "no test files found", or a coverage or report file that is
  missing but not required.
- Runner notices that an exit code was ignored (`continue-on-error`,
  `|| true`) on a step that produces a verdict.
- Deprecation notices for a runtime or action version with a known end date.

## Duration heuristics

- **At the limit:** a job whose duration is within a few seconds of its
  configured limit ended because of the limit.
- **Far faster than usual:** a job that took under half its usual time and
  passed is a skip or early-exit suspect; check the test count.
- **Slower than usual but green:** report the drift with both numbers; it
  predicts a future timeout.
- **No comparison run:** state durations as absolute values and do not call
  any of them a regression.

## Worked tie-breaks

1. *Timeout after failures.* A 30-minute job shows 3 failed assertions at
   minute 12 and then hangs until the limit. Class: `PRODUCT-BUG` or
   `TEST-BUG` per the assertions; the hang is noted as a second finding.
2. *Missing secret causing test failures.* Forty integration tests fail with
   connection refused after `DATABASE_URL is not set`. Class:
   `MISSING-SECRET-OR-CONFIG`, not forty product bugs.
3. *Runner lost mid-suite.* The log ends with `lost communication with the
   server` at minute 7 with all earlier tests passing. Class:
   `INFRASTRUCTURE`; the next step is to resume unfinished work, decided by a
   human.
4. *Truncated log.* The log stops at 4 MB with "log truncated" and no failure
   line in view. Class: `INDETERMINATE`; name the full log or the test report
   artifact as the evidence that would settle it.
