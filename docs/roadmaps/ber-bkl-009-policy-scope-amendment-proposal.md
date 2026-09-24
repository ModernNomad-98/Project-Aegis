# BER-BKL-009: remaining evidence-policy implementation scope proposal

Prepared 2026-09-24 for the Project Aegis owner. **OWNER DECISION PROPOSAL ONLY.**
This page is not an approval, a decision-log amendment, or permission to run,
publish, contact a provider, inspect private inputs, change a host, or delete
evidence. Behavioral Eval Runner (BER) backlog item 009 remains **PARTIALLY
DELIVERED**. An Aegis approval-register entry (APR-009) records the owner's
selection of the [30-day complete-bundle policy](../approvals/APPROVAL_REGISTER.md#aegis-apr-009-behavioral-eval-runner-evidence-policy-selection).
It expressly requires a separate reviewed implementation grant.

## Current boundary and proposed increment

The input-evidence stage (Stage A) is the hash-bound input bundle. The
final-evidence stage (Stage B) is the final result and verification chain.
[Pull request (PR) #139](https://github.com/ModernNomad-98/Project-Aegis/pull/139)
delivered the bounded synthetic proof authorized by BER decision-log entry
011 (BER-DEC-011). Its `OfflinePolicyWriter` requires an explicit
classification decision for every input and the final report; the receipts
bind one first-writer timestamp and a 30-day bundle review date through the
Stage A manifest, Stage B manifest, final report and detached finalization
marker.
Expired, failed and incomplete bundles are preserved. The [offline review](../evidence/ber-bkl-009a-offline-review.md)
records the tests and limits. Existing `expiration_at` fields still mean each
artifact's own expiry; they are not the complete-bundle review date. The
published `1.0.0-wp2b1` byte shape remains unchanged.

The proof does not establish a real host's access-control list (ACL), disk
encryption, recovery-key custody, actual redaction, or an operator cleanup
procedure. A citable classification reference does not prove content is safe
to publish. The current [backlog](behavioral-eval-runner-backlog.md#ber-bkl-009--evidence-retention-access-encryption-redaction-and-deletion-policy)
and [policy target](ber-bkl-009-evidence-policy-decision.md) require those
controls before item 009 can close. Older pages that call PR #139 open are
historical checkpoints; the merged code and PR history decide the current
implementation state.

The goal of this increment is to make the selected complete-bundle policy
usable by an explicitly opted-in local caller while preserving accepted
receipt bytes and refusing unknown host facts. Its non-goals are real-host
attestation, production driver integration, publication clearance and evidence
deletion. Keeping the current metadata defaults would allow a caller to
mistake implicit classification for review; changing the published evidence
schema would require a separate versioned decision; and implementing real-host
controls now would require a named host and its own authority. Those options
are outside this proposal.

**Proposed owner choice:** authorize one follow-up **offline, synthetic-only**
implementation package to make the selected policy usable by explicitly
approved local callers and operators, on an opt-in basis, without enabling a
live run. Production driver wiring is outside the ten proposed paths. Work
would begin only from the exact
merge commit of a separate reviewed BER decision-log amendment that records
the owner's approval. This proposal itself makes no change to the decision log
or approval register. The package would be capped at **16 active implementation
hours**, **1,500 added code/test lines**, and **$0 task-controlled external
spend**. If the complete safe implementation does not fit, stop and return a
new scope instead of silently widening it.

| Exact proposed path | Permitted work after a separate owner grant |
| --- | --- |
| `tools/behavioral_eval_runner/evidence_policy.py` | Add a fail-closed, local policy entry point for complete-bundle eligibility and classification verification. Preserve the shipped receipt and manifest byte contract. |
| `tools/behavioral_eval_runner/evidence.py` | Route opted-in local writer/verifier calls through the selected policy and reject implicit metadata defaults where a policy-bound artifact is required. No unversioned schema change. |
| `tools/behavioral_eval_runner/evidence_policy_preflight.py` (new) | Produce a read-only, structured preflight result from synthetic host facts supplied by the caller; unknown ACL, encryption, path ownership or recovery-key status must be `STOP`, never assumed verified. Any passing result must be explicitly marked `SIMULATION_ONLY`, never host attestation. It must not inspect or alter a real host. |
| `tools/behavioral_eval_runner/tests/test_evidence_policy.py` | Cover the expanded policy entry point, exact first-evidence clock, complete bundle, classification and refusal cases using owned synthetic directories. |
| `tools/behavioral_eval_runner/tests/test_evidence.py` | Guard the existing Stage A/B hash chain, marker binding and legacy byte compatibility. |
| `tools/behavioral_eval_runner/tests/test_evidence_policy_preflight.py` (new) | Test missing, false, conflicting and simulated passing host facts without querying the operating system. |
| `tools/behavioral_eval_runner/README.md` | Explain the opt-in local application programming interface (API), stop states and the difference between synthetic proof and host verification. |
| `docs/roadmaps/ber-bkl-009-operator-policy-runbook.md` (new) | Document the owner-review procedure: inventory and verify a bundle, determine review eligibility, preserve failed/incomplete bundles, inspect proposed cleanup targets and record a sanitized decision. It may describe future manual deletion prerequisites but contain no executable deletion command. |
| `docs/roadmaps/behavioral-eval-runner-backlog.md` | Append the owner-approved decision and an accurate dated implementation checkpoint only after the owner grants it; retain PARTIALLY DELIVERED until later host gates pass. |
| `docs/evidence/ber-bkl-009-policy-integration-review.md` (new) | Record exact source revision, changed paths and line count, synthetic commands/results, independent review, and unresolved host/privacy/cleanup gates. |

No other code, schema, workflow, dependency, private-repository or configuration
path is proposed. The new preflight module is a testable contract for a later
host adapter. Even a synthetic `PASS` means `SIMULATION_ONLY`; it cannot attest
that any selected host passed. No production
driver wiring, provider adapter change, automatic timer or deletion routine is
included.

The proposed rollout would be opt-in at the local writer/verifier interface;
existing callers and the published `1.0.0-wp2b1` byte contract must remain
valid. New runs could return to the legacy path, while an already policy-bound
bundle would stay on its policy verification path and be preserved. Historical
legacy evidence would need no schema migration. Structured stop reasons and a
sanitized review record would provide observability without raw transcripts or
host identifiers. Synthetic tests would cover refusal and compatibility; the
later host adapter, privacy review and cleanup procedure remain open questions
for the owner and independent security reviewer.

## Acceptance and delivery gates

1. A synthetic caller cannot write or treat a policy-bound bundle as trusted
   using default `INTERNAL`/`sanitized_by_construction` metadata. Every input
   and report must carry an explicit, versioned access-policy reference and a
   content-specific classification decision. Actual redaction remains a human
   content-review gate before publication.
2. The writer/verifier preserve one first-evidence clock and one 30-day review
   date across both stages and the detached marker. A later report cannot
   extend the date. A missing, forged, expired, conflicting or incomplete chain
   fails closed and leaves its files in place. Existing per-artifact
   `expiration_at` semantics, published hashes and accepted bytes remain
   unchanged. Any required schema or byte change stops for a separate versioned
   decision.
3. The synthetic preflight rejects missing or contradictory ownership, exact
   path, ACL, inheritance, encryption and recovery-key facts. It never turns a
   caller assertion or simulated `PASS` into a real-host verification claim;
   passing output must carry an explicit `SIMULATION_ONLY` status. The runbook requires
   hash/marker checks, an explicit owner review and an inventory before any
   future cleanup request; expiration alone does not authorize deletion.
4. Focused policy/evidence tests, the full offline BER suite, skill validation,
   whitespace and path-scope checks, independent architecture/security review,
   and exact-head Linux and Windows continuous integration (CI) checks pass.
   The implementation PR
   carries a Developer Certificate of Origin sign-off. A protected gate-guard
   failure needs its own owner disposition; it is not a green check.
5. The evidence review records the observed results and remaining limits
   without raw transcript, private labels, credentials, provider output or
   unsanitized host identifiers in the public repository or CI artifacts.

## Boundaries and later owner gates

The proposed grant, if approved, would cover only the synthetic package above. It
would authorize **no** real or selected host access, ACL or BitLocker change,
recovery-key handling, service principal, private calibration source, sealed
holdout, credential use, provider call, live run, public release of raw content,
or operator cleanup. Preserve any failed/incomplete bundle. No automatic or
manual deletion is authorized by a review-eligibility date or this proposal.

The later real-host package must name the exact source and execution host,
prove owner-plus-SYSTEM (the Windows built-in service account) access with
inheritance disabled on the Windows work
package 2B-3 (WP-2B-3) root or obtain a separately approved reader matrix,
verify encryption
on that host and recovery-key custody, bind actual creation sites and driver
wiring to the policy, independently review privacy before publishing any
derivative, and test a marker-gated cleanup plan. Any actual deletion requires
a separate explicit owner action after inventory, hash and path checks. A
different host or access principal needs its own recorded mechanism and
decision. BER-BKL-009 can be marked DONE only after the policy, runtime wiring,
host proof, operator procedure and reviewed completion evidence exist.

## Decision for the owner

Approve or decline **only** the proposed 16-hour, 1,500-added-line, $0
synthetic implementation scope and exact ten paths above. Approval should be
transcribed into a separate BER decision-log amendment and reviewed/merged
before an implementation branch begins. It would not approve the later
real-host or cleanup gates. The current forecast assigns **8–16 active hours**
to the whole remaining BER-BKL-009 item. If this proposed grant is approved,
that whole-item range is superseded: the proposed offline package alone has a
16-hour cap, while residual real-host/runtime/privacy/cleanup effort remains
**TBD pending host selection**. The selected backlog total after PR #250 of
**87–178 active hours** must then be recomputed; this proposal assigns no
invented hours to the residual work. This offline package closes none of the
selected-host proof or cleanup work. A later host package needs a separate forecast row and estimate
when its host and scope are selected.
