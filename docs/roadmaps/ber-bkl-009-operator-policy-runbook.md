# BER-BKL-009 synthetic evidence-policy operator review

## Scope and authority

This runbook supports the opt-in offline policy package authorized by
[BER-DEC-013](behavioral-eval-runner-backlog.md#ber-dec-013-bounded-synthetic-evidence-policy-integration--owner-approved)
and [APR-023](../approvals/APPROVAL_REGISTER.md#aegis-apr-023-bounded-synthetic-evidence-policy-integration).
It describes a **review procedure**, not a host attestation, live-run
procedure, publication clearance or deletion authorization. Use only owned
synthetic bundles. A `SIMULATION_ONLY` preflight result records that supplied
facts were internally consistent; it says nothing about an actual machine.

The input-evidence stage (Stage A) contains the classified inputs and its
policy receipt. The final-evidence stage (Stage B) contains the final report
and policy receipt; a detached finalization marker binds the final manifest
and report. The complete-bundle review date is
the first writer-stamped evidence time plus 30 consecutive 24-hour periods.
Each artifact's `expiration_at` retains its separate per-artifact meaning.
Neither date authorizes deletion.

## Review a synthetic bundle

1. **Record the request.** Record the owner of the synthetic test root, the
   exact root identifier, reason for review, source revision, reviewer and
   Coordinated Universal Time (UTC) of review in a local sanitized record.
   Keep raw evidence, private labels, credentials and host identifiers out of
   this repository and continuous integration (CI) artifacts. If ownership
   or scope is unclear, stop.
2. **Inventory without changing files.** Enumerate the expected Stage A and
   Stage B manifests, both policy receipts, final report, detached marker and
   referenced artifacts. Record relative paths, lengths and hashes. Notice
   missing, extra, aliased or conflicting paths; do not repair them in place.
   Preserve failed and incomplete bundles exactly as found.
3. **Verify the chain.** Run the offline policy verifier against a read-only
   view of the synthetic bundle. It must check each manifest and receipt,
   the report and detached marker, explicit input/report classification
   decisions, one first-evidence clock and the same 30-day review date across
   both stages. Treat any missing, tampered, expired, inconsistent or incomplete
   chain as `STOP`; preserve the bundle and record the reason for owner review
   or investigation.
   A successful hash check alone does not establish truthful classification
   or redaction, nor independent authenticity against a coordinated rewrite.
4. **Inspect the proposed action.** If the review date has arrived, the policy
   verifier returns `STOP` and does not issue an accepted-bundle result. Keep
   that state. A separate read-only inventory may recompute hashes solely to
   list exact proposed targets for owner review; label them inventory values,
   **not** verified policy acceptance. Include failed/incomplete bundles in
   the preservation inventory. Have the owner review the classification
   references, privacy implications and any later
   real-host controls separately. The owner must make an explicit decision;
   elapsed time cannot stand in for that decision.
5. **Record the outcome.** Record only sanitized identifiers, verifier result,
   review date, owner decision or `PENDING`, reviewer and remaining gates.
   A `PENDING` or `STOP` outcome leaves all evidence in place. An owner
   decision to consider future cleanup is a proposal for a separate authorized
   procedure, not permission to remove anything under this runbook.

## Stop and escalation conditions

Stop when facts are missing or contradictory, a hash or marker fails, a
policy-bound bundle is presented through a legacy path, the review date has
arrived,
the bundle is incomplete, or the proposed action would touch a real host,
private input, provider, credential, production driver or publication surface.
Preserve the bundle and return a sanitized account to the owner and security
reviewer. Do not rewrite receipts or reset a clock to make a bundle pass.

Real-host access control, inheritance, disk encryption, recovery-key custody,
actual redaction, runtime binding and cleanup remain separate BER-BKL-009
gates. Any future deletion requires its own owner authorization after an exact
path and hash inventory, independent host/privacy review and a separately
reviewed marker-gated procedure. This document contains no deletion command.
