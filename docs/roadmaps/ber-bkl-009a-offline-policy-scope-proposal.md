# Behavioral Eval Runner evidence policy: offline first-increment proposal

**Reader key:** This page is for the owner and reviewers of the bounded
Behavioral Eval Runner (BER) offline proof. `AEGIS-APR` identifies an owner
approval-register entry; `BER-DEC` identifies a runner decision-log entry;
`BER-BKL-009A` is the offline increment of backlog item 009. A pull request
(PR) proposes a repository change, and continuous integration (CI) runs
automated checks. The original proposal below remains historical; its linked
approval and decision record set the current scope.

> **Current status, 2026-09-23:** The owner approved this bounded synthetic
> offline proof in [AEGIS-APR-012](../approvals/APPROVAL_REGISTER.md#aegis-apr-012-offline-behavioral-eval-runner-evidence-policy-proof)
> and the merged [BER-DEC-011 decision](behavioral-eval-runner-backlog.md#ber-dec-011-bounded-offline-evidence-policy-proof).
> The owner had already selected the 30-day complete-bundle policy in
> [AEGIS-APR-009](../approvals/APPROVAL_REGISTER.md#aegis-apr-009-behavioral-eval-runner-evidence-policy-selection).
> [PR #139](https://github.com/ModernNomad-98/Project-Aegis/pull/139) is not
> merged into this checkout; the [backlog](behavioral-eval-runner-backlog.md#wp-2b-1b--offline-evidence-policy-proof)
> records it as open at its checkpoint. Recheck its live state before acting.
> No real-host run, private input, provider call or cleanup follows from this
> grant. The options below preserve the pre-approval proposal as history.

**Historical authorization proposal follows.**

Prepared 2026-09-23 for the Project Aegis owner. **Proposal only.** Merging
this page would record a reviewable scope, not grant implementation or change
the state of Behavioral Eval Runner (BER) backlog item 009. The owner selected
the [30-day complete-bundle policy](ber-bkl-009-evidence-policy-decision.md)
in [approval APR-009](../approvals/APPROVAL_REGISTER.md); that record expressly
requires a separate reviewed decision-log amendment before code or an
operator action is authorized.

## What problem the first increment would solve

The shipped evidence writer records hashes and per-artifact metadata. It
currently calculates expiration from each artifact's own creation time, so
the input manifest, final report and detached marker do not yet share a
verified deadline from the first evidence creation. The writer's default
classification can also label content as already sanitized without a
content-specific decision. Neither behavior proves the selected runtime
policy. A complete bundle must remain together for 30 calendar days from its
first evidence creation, and failed or incomplete runs must be preserved for
owner review.

For example, if the first input is created on October 1 and the final report
is created on October 2, both belong to one bundle whose review-eligibility
date is October 31. The October 2 report must not quietly gain an extra day.
Expiration makes a bundle eligible for review; it does not authorize deletion.

## Recommended authorization: BER-BKL-009A

Authorize one **offline, synthetic-only** implementation increment, capped at
**8 active hours**, **1,000 added code/test lines** and **zero task-controlled
external spend**. Start from the exact merged grant commit. The intended
deliverable is a policy checker and negative tests for a complete bundle.

| Exact implementation path | Allowed purpose |
| --- | --- |
| `tools/behavioral_eval_runner/evidence_policy.py` (new) | Represent the selected policy and check one trusted first-evidence clock, complete-bundle deadline, explicit classification and artifact binding. |
| `tools/behavioral_eval_runner/evidence.py` | Add an opt-in writer/verifier seam that mints or verifies policy facts without changing the legacy path's accepted bytes or behavior. |
| `tools/behavioral_eval_runner/tests/test_evidence_policy.py` (new) | Synthetic positive and negative policy tests. |
| `tools/behavioral_eval_runner/tests/test_evidence.py` | Regression checks for existing Stage A and Stage B serialization and verification. |
| `tools/behavioral_eval_runner/README.md` | Explain the offline checker, its use and its limits. |
| `docs/roadmaps/behavioral-eval-runner-backlog.md` | Append the owner-approved decision and a dated status checkpoint only after the owner actually grants this scope. |
| `docs/evidence/ber-bkl-009a-offline-review.md` (new) | Record exact revision, commands, results, independent audit and remaining real-host gates. |

Here **Stage A** means the input evidence manifest and its bound artifacts;
**Stage B** means the final report, final manifest and detached finalization
marker. The marker stays outside the manifest it names, so the checker must
bind it through the existing non-circular hash chain. It must not claim the
marker is a manifest entry.

The policy path must get the first creation time from a trusted writer event,
not a caller-supplied timestamp or a later finalization time. It may use the
current serialized fields only if they can truthfully carry and verify that
fact. **If a new published field, changed field meaning or accepted-byte
shape is necessary, stop for a separate versioned schema decision** under
the [schema compatibility policy](../behavioral-eval-runner-schema-compatibility.md).
Do not silently change version `1.0.0-wp2b1` or historical evidence.
The opt-in path must stamp the creation time itself and reject a caller's
`created_at` override. An empty Stage A input has no first artifact creation;
reject it in this path unless a separately approved versioned record supplies
a trustworthy first-evidence event. For this proposal, a deadline means the
first trusted timestamp normalized to Coordinated Universal Time (UTC) plus
30 consecutive 24-hour periods. A later report cannot reset that timestamp.

## Acceptance evidence before this increment can close

1. Synthetic tests prove one exact 30-calendar-day deadline across the
   input and final evidence chain, including the detached marker's binding.
   A later Stage B finalization cannot extend the deadline.
2. Missing, caller-forged or contradictory first-creation times fail closed.
   Tests include different time zones, a month boundary, and an already
   expired bundle.
3. The policy path requires an explicit sensitivity, redaction state and
   versioned access-policy reference at each creation site. Raw evidence
   cannot pass with the existing sanitized-by-construction default. Mixed
   90/365-day retention inside a 30-day runtime bundle is rejected. The
   creation site must also supply a citable content-classification decision;
   metadata alone cannot prove that content was actually redacted. The
   synthetic checker enforces the decision record's presence and binding,
   while any public release still needs separate human content review.
4. Hash changes, a substituted run identity, altered policy bytes and an
   unbound or missing marker fail closed. Existing non-policy evidence tests
   and serialized hashes remain compatible.
5. Failed and incomplete runs are preserved. The implementation has no
   cleanup, publication, provider, private-input or real-host side effect;
   tests assert those absences where mechanically checkable.
6. Focused tests, the full relevant offline BER suite, skill validation,
   independent architecture/security review and exact-head Linux and
   Windows Actions must pass. The protected-file guard will flag BER code
   and README changes; a separate explicit owner disposition is required
   before merging any PR with that check failed. A failed guard is not green.

## Boundaries and later gates

This increment cannot use real credentials, customer data, private calibration
inputs, sealed holdouts, provider calls, a live run, an external evidence
root, real deletion or a service principal. It does not verify operating-system
access control lists (ACLs), volume encryption or BitLocker recovery-key
custody. It does not assign a real host or alter the approved 30-day policy.

A later decision must name the selected source and host, exact live writer and
driver wiring, owner-plus-SYSTEM access with inheritance disabled on the
Windows root, actual encryption verification and recovery-key custody,
privacy review for any public derivative, and a marker-gated operator cleanup
procedure. The owner must separately approve any real deletion or additional
reader. The existing [backlog](behavioral-eval-runner-backlog.md) remains
**PARTIALLY DELIVERED** until those controls are implemented and evidenced.

## Owner options

| Choice | Effect |
| --- | --- |
| **A. Approve the bounded offline increment (recommended)** | Create a separate, reviewed BER decision-log grant for only the seven paths and limits above. It proves the policy contract without claiming host readiness. |
| B. Design the complete real-host implementation first | Requires a named host, access and encryption proof, and a broader reviewed scope before code. It delays the offline falsifiers. |
| C. Defer | Keep the selected policy and partial-delivery status; no new code is authorized. |

Approval of option A would authorize the bounded code work only after the
exact grant is recorded and merged. It would **not** itself approve a future
protected-file guard exception, private data access, provider run or cleanup.

The previously stated full evidence-policy implementation estimate is
**8–16 active hours**. Preparing this scope proposal is estimated at **1–2
active hours**. The selected backlog estimate when this proposal began was
**175–394 active hours**, pending merge of its forecast PR. The full
all-options backlog has no finite ETA while optional host and product counts
remain undecided.
