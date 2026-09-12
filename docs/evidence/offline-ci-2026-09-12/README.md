# Offline CI implementation verification

Implementation tested: `b483d4e0b98d76b64c8053c99397eb5a296c7705`.
Base: PR #90 merge `82dfebee7dadb68207bead5cb10fa3c562f21c1e`.
This checkpoint records local results before hosted verification; it is not a
claim that the CI follow-up has merged.

The subsequent [hosted verification and fix record](HOSTED.md) records successful
Linux and Windows jobs at `0444f46`, including both PowerShell editions on Windows.

## Preflight and reviewed plan

Existing unittest, validator and PowerShell runners cover the intended layers;
introducing another test framework or replacing those runners was unnecessary.
The workflow invokes each once through a small output/status recorder. Independent
read-only reviews covered workflow behavior, evidence preservation and enforcement
boundaries. Findings repaired before this checkpoint: invalid job-level runner
context use, and an omitted parent Python import path in the protected-file guard.

Full Git history is required by historical authorization fixtures. Both platforms
install the reviewed SDK and fail a precheck if its mocked-test dependencies are
absent. Fixture temporary directories stay outside the checkout. Windows Desktop
and Core acceptance runs are sequential; the two OS jobs are independent.
There are no automatic retries, new credentials, live provider requests, new
runner infrastructure, or branch-protection changes.

The required Ubuntu job gains contract, BER and acceptance checks. Windows adds
visible coverage without becoming a newly required branch-protection context.
Both jobs must pass before delivery closeout. The protected-file guard expands
to the new enforcement dependencies and reads filenames without quoting/rename
bypasses. Its deliberate failure on this CI PR requires the existing manual merge
route. The plan is to publish, fix hosted/review findings, then verify the merged
tree on main. Full operating details are in [offline-ci.md](../../offline-ci.md).

## Observed local results

| Check | Result |
| --- | --- |
| Windows Python 3.14.7 / installed SDK precheck | PASS; dependency inventory recorded |
| CI helper tests on Windows | 8 tests, 4 Linux guard cases skipped |
| Validator self-tests / skill validation | 91 assertions; 184 valid skills, 0 warnings |
| Contract-audit self-tests / BER self-check | 63 assertions; 21 self-checks passed |
| Full Windows BER suite | 987 tests, 14 capability skips; PASS |
| Windows PowerShell 5.1 Scenario A acceptance | 113 checks; PASS |
| Linux CI recorder and actual guard regression tests | 8 tests; PASS, no skips |
| DCO / whitespace / actionlint v1.7.12 | PASS |
| Local PowerShell Core | UNRUN: shell not installed |

The Windows mirror read commands from the actual workflow and verified an
unchanged, clean checkout before and after execution. The Linux fixture run used
the exact implementation commit, Python 3.12.3 and an unprivileged network-disabled
container; it establishes guard/helper behavior only. Hosted Linux Python 3.14,
installed SDK coverage and both hosted Core acceptance runs remain to be observed.
Skip reasons are preserved in raw output and must be assessed per host.

`windows/` contains the recorder's raw logs, metadata and driver summary;
`linux-guard.json` records the container invocation and full output.
`SHA256SUMS.json` hashes the retained evidence files. Historical local paths in
records identify where commands ran; they are not portability requirements.

This automation does not close measured calibration, approved input/label work,
OD1, sealed-holdout execution, or the blocked WP-2B-4 phase.
