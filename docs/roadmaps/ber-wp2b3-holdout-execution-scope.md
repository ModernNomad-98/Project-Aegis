# Behavioral Eval Runner holdout execution support: work package 2B-3

> **Current reading, checked 2026-09-23:** This remains an offline
> implementation proposal, not a grant to unseal private cases or call a
> provider. Work package 2B-3 (WP-2B-3) is authorized under decision
> BER-DEC-008 but incomplete; the
> proposed holdout code needs its own reviewed amendment. The
> [BER backlog](behavioral-eval-runner-backlog.md#start-here-status-and-routes)
> holds the current gates and the [private-input summary](../evidence/ber-replacement-candidate-1-summary.md)
> records the candidate packet without exposing its contents.

**Reading key for delivery terms:** Developer Certificate of Origin (DCO)
sign-off applies to commits; quality assurance (QA) is independent test review;
software development kit (SDK) identifies the pinned provider interface;
command-line interface (CLI) is the user-facing command surface. `OWNER_WAIT`
is the stop before a human holdout freeze; `JUDGE_ERROR` is an unsuccessful
judge outcome, not a passing verdict.

This document proposes the allowed files, behavior, tests, and decision gates
for building an offline holdout execution path. It helps reviewers decide what
the implementation may do. It does not approve reading private cases or calling
the model provider. In this document, **Behavioral Eval Runner (BER)** is the
evaluation tool, **WP-2B-3** is its numbered calibration work package, and
**BER-DEC-008** and **BER-DEC-010** are entries in the linked decision log.

Prepared 2026-09-23 from public `main` at
`f3d3e07cd623a1cd69413d0d28e15b75df4c5a49`. This is the drafting
baseline; the proposal was reconciled with later `main` before merge.
**Proposal only.**
WP-2B-3 remains AUTHORIZED under BER-DEC-008 but incomplete. Its surviving
`calibration_development_driver.py` is explicitly development-only; the
[replacement plan](../evidence/ber-recovery-2026-09-11/replacement-plan.md)
requires a separately reviewed holdout implementation. BER-DEC-010 moved
replacement inputs to the owner-only private repository without changing the
original measured-execution branch or source baseline. The private candidate
packet remains PENDING human label review. This proposal grants no changed
source baseline, provider request, holdout unseal or OD-1 result.

## Proposed next decision

Approve one **offline implementation branch** for the holdout execution seam
described below. The amendment would be appended to the BER decision log through
a reviewed governance PR and become effective only on its merge. Start the new
`feat/ber-wp2b3-holdout-offline-support` branch directly from that exact grant
merge commit; record its head/tree, reconcile intervening BER normative changes,
and keep the BER-DEC-008 model, SDK, thresholds, budget, deadlines, retry policy,
evidence root and one-pass rules intact. The original BER-DEC-008 measured-
execution branch and clone remain unchanged. This offline branch does **not**
become an authorized live execution source or establish any remaining spending
allowance. The old development-only driver and PR #88 closeout stay historical.

| Boundary | Proposed offline implementation scope |
| --- | --- |
| Repository and base | `ModernNomad-98/Project-Aegis`, source-library Role A; create only `feat/ber-wp2b3-holdout-offline-support` from the exact merged grant commit. Do not repoint, replace or silently supersede BER-DEC-008's `feat/behavioral-eval-runner-2b-3-measured-judge-calibration` branch/clone or its original source baseline. No history rewrite. |
| Code paths | New `tools/behavioral_eval_runner/judge/calibration_holdout_driver.py`; existing `tools/behavioral_eval_runner/judge/calibration_development_driver.py`, `tools/behavioral_eval_runner/judge/calibration_gates.py`, `tools/behavioral_eval_runner/judge/calibration_ledger.py`, `tools/behavioral_eval_runner/judge/calibration_provider.py`, `tools/behavioral_eval_runner/judge/calibration_dataset.py`; existing `tools/behavioral_eval_runner/tests/test_calibration_development_driver.py`, `tools/behavioral_eval_runner/tests/test_calibration_gates.py`, `tools/behavioral_eval_runner/tests/test_calibration_ledger.py`, `tools/behavioral_eval_runner/tests/test_calibration_provider.py`; new `tools/behavioral_eval_runner/tests/test_calibration_holdout_driver.py`. |
| Documentation paths | `tools/behavioral_eval_runner/README.md`, `docs/roadmaps/behavioral-eval-runner-backlog.md`, and one sanitized `docs/evidence/ber-wp2b3-holdout-offline-review.md`. The separate governance-grant PR edits only the BER decision log and its measurement record. |
| Time and size | Maximum 16 active implementation hours and 2,000 added code/test lines; stop for a reviewed scope change if either is exceeded. The current remaining execution-support forecast is 8–16 active hours. |
| Data and spend | Synthetic temporary fixtures only; no access to the 120 private holdout transcripts or labels during this offline implementation, no credential, metadata/model/provider call, dependency install or task-controlled external spend. |
| Delivery | One DCO-signed code PR with explicit-path staging, focused and full BER offline tests, independent security/recovery/QA review, and all exact-head GitHub Actions green. Protected-file guard failure needs its own documented owner disposition; PR #104's exception does not transfer. |

## Reuse and negative acceptance

The new seam composes the existing canonical ledger, verified external-root
contract, provider transport, authorization, freeze artifact and dataset
mapping. It must not clone a second accounting ledger, widen the generic BER
CLI, or weaken the development-only path. Existing code may be changed only
where the shared stage contract needs a typed holdout path; keep all source
changes within the exact allowlist.

- An unapproved or wrong-hash dataset, absent independently pinned owner freeze,
  invalid selected output cap, changed source/head/tree, failed root check,
  unresolved historical usage or wrong stage denies before any provider
  contact. Synthetic tests may use example freeze structures but cannot record
  them as actual owner approval.
- The holdout path sees only the 120 frozen holdout items after the gate; no
  expected answer or gold label enters the judge envelope. Development items
  and public candidate data cannot be substituted for the holdout.
- One durable run/segment and one authoritative ledger count the metadata
  request, both stages, retries, token/spend reserve and settlements. A crash,
  lost acknowledgement or unknown outcome cannot trigger an automatic second
  holdout pass or refill a consumed allowance.
- Every incomplete/refusal/transport/schema outcome is `JUDGE_ERROR` under
  the existing stop and retry rules. Preserve raw outcomes and usage evidence;
  no retry-until-green or selective rerun of failed cases. The result reports
  the full confusion matrix and all six BER-DEC-008 thresholds without
  claiming OD-1 ratification.
- Local Windows and pinned Linux tests use fake transports and temporary
  fixtures. They prove denial and accounting behavior only, not provider
  availability, private-input approval, selected-host readiness or a measured
  calibration result.

## Gates after offline code

1. Peter reviews and approves exact private dataset, split, guide and hashes;
   any case changes create a new version. A separate owner-reviewed BER-DEC
   amendment must select the exact audited code head/tree and any execution-
   branch/clone change before a provider request; the offline PR does not make
   that selection. Reconcile private-repository visibility and access. The
   public PR contains only opaque identities and sanitized evidence.
2. Resolve historical usage and remaining allowance from authoritative
   evidence; verify actual host, credential custody, provider project, SDK,
   model and pricing. Run the BER-DEC-008 preflight on an exact audited source
   revision. An absent file is never evidence of zero prior spend.
3. Only then may a separately authorized development stage make requests.
   Development ends at OWNER_WAIT. Peter reviews its distribution and freezes
   the exact holdout output cap and hashes before one holdout execution.
   Present the measured result for OD-1; a passing synthetic test or source
   merge cannot ratify it.

No approval of this proposal alone starts implementation or contacts a
provider. If the owner declines the offline-branch grant, the existing
BER-DEC-008 authority remains as recorded and this proposed new path is not
used.
