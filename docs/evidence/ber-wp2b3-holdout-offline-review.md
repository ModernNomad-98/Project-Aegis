# Behavioral Eval Runner offline holdout-support review

**Current reading, 2026-09-24:** This is an in-progress synthetic implementation
record. No measured calibration or private sealed holdout has run. Four focused
offline suites and the full unsandboxed Windows suite pass locally. Independent
security, recovery and quality review is complete with corrections applied.
Pinned Linux, the exact implementation head, and hosted checks remain pending.

Behavioral Eval Runner (BER) work package 2B-3 (WP-2B-3) measures a semantic
judge against an owner-approved dataset. Owner decision one (OD-1) is the later
human disposition of measured results. Decision BER-DEC-012 grants a bounded
offline implementation seam; it does not grant a provider request. The
[decision](../roadmaps/behavioral-eval-runner-backlog.md#ber-dec-012-bounded-offline-holdout-support-implementation-grant--owner-approved)
and [scope packet](../roadmaps/ber-wp2b3-holdout-execution-scope.md) govern this
record.

## Source and allowed scope

The implementation branch is `feat/ber-wp2b3-holdout-offline-support`, created
directly from grant merge `0196fe5b4eb30ca72c4bd61d51bedc9489a62115`.
Its audited execution head and tree remain **unselected**. The original
BER-DEC-008 measured-execution branch and source baseline are not replaced by
this offline branch. The grant allows 11 named code/test paths and these three
documentation paths, at most 16 active implementation hours and 2,000 added
code/test lines. It permits synthetic temporary fixtures, no private inputs,
credentials, provider or metadata calls, dependency installs, or task spend.

The implemented seam composes the existing dataset, authorization, provider and
ledger contracts. A holdout dispatch binds the approved dataset and split,
an independently pinned owner freeze, the audited source head and tree, and a
frozen output cap before transport. The same durable ledger records the
development stop at `OWNER_WAIT` and one transition to sealed holdout. The
driver requires a pinned, read-only development result summary matching its
durable 40 outcomes before that transition. An interrupted or uncertain run
does not start a second pass. Only the 120 holdout item identities may reach a
future authorized dispatch, and judge envelopes omit expected labels.

The production freeze, audited holdout source head/tree, original development
source head/tree, and development manifest/summary digest pins are all `None`.
Tests replace them inside synthetic fixtures only. The driver cannot dispatch
from this source checkout without separate reviewed selections and the other
recorded gates. A completed synthetic one-pass fixture made 120 fake software
development kit (SDK) calls, produced all six pre-registered threshold fields,
and refused a second transition. If a process stops after the durable pass
closes but before its result summary is written, `recover_summary()` reads the
verified chain and outcomes and writes only the missing summary. It creates no
SDK client or new provider attempt and refuses an incomplete or stopped pass.
Independent review of the candidate found issues that were corrected before
this checkpoint. Final full-suite and hosted results remain pending.

## Verification ledger

| Check | Result at this checkpoint |
| --- | --- |
| Exact implementation head and tree | Pending final implementation commit. |
| Added code/test lines and active time | Final scope audit: 1,659 added code/test lines against the 2,000-line cap, within the exact allowed paths. From the grant merge at 2026-09-24 16:16:48 UTC through 17:18 UTC, less than 62 minutes elapsed. At most seven agent slots, including root, were available. Even counting every slot active throughout gives a conservative aggregate upper bound below 7 hours 14 minutes, within the 16-hour grant; actual active time was not measured. |
| Focused synthetic tests | Gates: 29 pass; ledger: 49 pass; provider: 48 pass; holdout driver: 7 pass. All use local synthetic fixtures and fake SDK transport. |
| Full offline BER suite on Windows and pinned Linux | Unsandboxed Windows: `python -B -m unittest discover -s tools/behavioral_eval_runner/tests -p test_*.py -q` ran 1,050 tests in 330.679 seconds: OK, 14 expected skips. An earlier sandbox run of 1,050 tests had 12 environment errors and no assertion failures; its targeted unsandboxed watchdog check passes. Pinned Linux remains pending. |
| Skill validator and diff whitespace check | 185 skills valid, zero warnings; diff check clean. |
| Independent security, recovery, and quality review | Completed on the current candidate; findings were corrected. Final integration evidence remains pending. |
| Exact-head GitHub Actions | Pending pull request. |

## Gates still required

The owner must review the exact private dataset, split, labels, guide and
hashes. A later owner-reviewed decision must select the audited execution
head/tree and any execution-branch change. Historical usage and remaining
allowance, private-repository visibility, selected-host evidence, credential
custody, pinned provider terms and actual root protections must pass their
preflight before measured development. Development stops at `OWNER_WAIT` for
owner review and a separately pinned holdout freeze. One authorized measured
holdout pass and OD-1 review then remain. Offline tests, this record and a
source merge satisfy none of those gates.
