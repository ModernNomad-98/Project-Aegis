# CP-WP-003 offline capability-proof authorization proposal

Prepared 2026-09-23 from public `main` at
`32144083bc86412e30d70873f877d4e7c051b6e0`. **Proposal only.**
CP-WP-003 remains BLOCKED in the [control-plane backlog](resumable-control-plane-backlog.md).
The local committed [design](../design/resumable-control-plane-v1.md),
[CP-WP-002 closeout](../evidence/control-plane/cp-wp-002-codex-handoff.md),
and [owner-decision index](aegis-open-decisions-2026-09-23.md) are the
source boundaries. The unrelated uncommitted local design draft is not part
of this proposal or a new normative base.

## What is ready and what is missing

CP-WP-002 delivered a synthetic-only SQLite recovery kernel with 28/28
transition, 9/9 crash and 22/22 acceptance-family rows independently accepted,
543 passing offline tests on each of Windows and Linux (with three expected
platform skips), and three green hosted jobs.
Its synthetic issuer, capability and adapter prove local contract behavior,
not a real external authorization or effect. The kernel still lacks a real
source-atomic approval claim shared with manual/other-host consumers, a
verified independent monotonic anchor or complete current-source
reconciliation, selected-host process containment/fencing, a real evidence
writer/access policy, and bounded-liability settlement backed by the chosen
operation's actual receipts and billing source. CP-WP-004 has no chosen target.

The first useful CP-WP-003 increment is an **offline proof harness and
fail-closed interface contract**, called CP-WP-003A here. It can expose
incompatible or missing host/source guarantees before selecting a real
operation. It cannot satisfy CP-WP-003's real-source/host gate by itself.

## Proposed owner decision

Authorize CP-WP-003A only, under the following bounded contract. This
decision would permit its implementation after the exact approval is recorded
in the source-library approval register and merged from a reviewed governance
branch. Acceptance of this proposal PR alone does not grant that authority.

| Boundary | Proposed CP-WP-003A grant |
| --- | --- |
| Repository and base | `ModernNomad-98/Project-Aegis`, Role A; implementation branch starts at the exact merged grant commit. If main advances, reconcile changed normative CP files before code. |
| Purpose | Define and falsify source, freshness, containment, owned-path, evidence and accounting capabilities using synthetic issuers, targets and temporary fixtures. Unknown/unavailable capabilities deny real dispatch. |
| Allowed implementation | Python standard library only in the exact files below; closed capability declarations and checked read-only probes; synthetic adversarial authority-source and receipt/billing fakes; a fail-closed capability gate at the existing dispatch boundary; focused tests and CP package README/backlog/evidence updates. Keep the public CLI synthetic-only. |
| Exact proposed implementation paths | `tools/aegis_delivery_control/capabilities.py` (new); `tools/aegis_delivery_control/authority.py`; `tools/aegis_delivery_control/adapters.py`; `tools/aegis_delivery_control/dispatch.py`; `tools/aegis_delivery_control/evidence.py`; `tools/aegis_delivery_control/owned_paths.py`; `tools/aegis_delivery_control/README.md`; `tools/aegis_delivery_control/tests/test_capabilities.py` (new); `tools/aegis_delivery_control/tests/test_dispatch.py`; `tools/aegis_delivery_control/tests/test_platform.py`; `tools/aegis_delivery_control/tests/test_recovery.py`; `docs/roadmaps/resumable-control-plane-backlog.md`; `docs/evidence/control-plane/cp-wp-003a-review.md` (new). The separate merged grant must repeat this list exactly before implementation. No other path is authorized by this proposal. |
| Time and size | Proposed ceiling: 10 active implementation hours, excluding owner/CI wait; no more than 2,000 added code/test lines. Stop and re-scope if a proof needs more. These ceilings are for the proposed first increment; the backlog's revised 12–24-hour total CP-WP-003 forecast remains provisional. |
| Spend and data | USD $0 task-controlled spend; no dependency install, credential, production/customer data, sealed holdout, external provider call, deployment or real mutation. Existing approved Codex session and repository CI only. |
| Delivery | One focused DCO-signed PR, explicit-path staging, local Windows and pinned Linux CP suite plus applicable BER regressions when a shared contract changes, independent architecture/security/QA review, exact-head hosted checks, owner-approved merge under existing AEGIS-APR-002. No automatic phase advance. |

The proposed fixture location is temporary directories created by the existing
Python tests under the operating system's temporary root. No fixture bytes go
into the repository or the unrelated local `artifacts/` directories. The
implementation may edit only the paths in the exact list after the owner grants
this scope and the grant is merged. `contracts.py`, `engine.py`, `storage.py`,
the CLI, dependencies, CI, BER, startup and the local design draft stay outside
this first increment. If a required invariant needs one of those files, or the
10-hour/2,000-line ceiling cannot cover the negative proofs, stop and seek a
revised reviewed scope before touching it. The existing synthetic dispatch
behavior must remain usable; the new capability gate denies any unproven
real-target route rather than treating a synthetic pass as real readiness.
If no safe synthetic probe can represent a source requirement, record
`UNPROVEN` and keep the gate shut; do not replace the source with a mock and
call the real guarantee verified.

### Required negative proofs

| Capability | Offline falsifier / acceptance evidence | Real gate left open |
| --- | --- | --- |
| Source-atomic one-use approval | Race two synthetic consumers, including a simulated manual consumer, for one token; exactly one claim/redemption wins. Revoke/expire/supersede before contact and replay a lost acknowledgement. A copied local SQLite claim cannot satisfy a distinct source. | Select a real source and prove the same atomic operation spans every authorized consumer; source outage denies dispatch. |
| Freshness/rollback | Restore an older internally valid checkpoint after a later synthetic effect/charge; independent anchor or complete current-source ledger rejects it. Stale, unavailable and contradictory proof deny. | Name a real independent anchor or complete reconciliation source, its custody and failure semantics. |
| Containment/fencing | Inject descendant escape, leader exit with child alive, process timeout, path swap, reparse/hardlink and ownership/ACL failures. An unsupported host denies dispatch with a recorded unsupported-capability reason; a check-before-open alone is insufficient. | Probe selected host and operation boundary; demonstrate prevention/termination/fencing before any real dispatch. |
| Evidence | Tamper binding, hash, version, writer identity or stage transition; verify original bytes and an independently checkable report. Reject unverifiable or sensitive evidence publication. | Approve actual evidence root, readers, encryption, retention and cleanup before real output. CP does not inherit BER policy automatically. |
| Receipt and bounded liability | Duplicate, delayed, contradictory, lost and post-cancel receipts; unknown bill amount retains worst-case liability and slot/fence. Crash/replay never refunds uncertainty or exceeds cap. | Pin actual operation receipt and billing authority, cap and dispute/reconciliation route. |

Every proof names a fixture, invariant, expected denial, observed command and
exit, platform, reviewer, and exact candidate commit. Passing a synthetic
probe is evidence about the interface, not a production capability claim.
Windows and pinned Linux results are recorded separately; a skipped or
unavailable platform capability remains unproven.

## Follow-on decision gates

1. **CP-WP-003A closeout:** prove the negative families above and document
   missing guarantees. Keep CP-WP-003 BLOCKED if any real prerequisite is
   unselected or unverified. No real connector/authority enters CP-WP-003A.
2. **Selected source and host:** owner chooses a specific authorization source,
   independent freshness/ledger design, host and allowed operation. Prepare a
   separate exact-source/host plan with immutable pins, source-atomic/manual
   consumption, containment and evidence proof; obtain a separate grant before
   contacting it. A host capability matrix may be shared with BER, but CP and
   BER approvals, data and runtime contracts remain separate.
3. **CP-WP-004:** after CP-WP-003's real prerequisites are accepted, compare a
   draft GitHub PR target with local artifact export. Select one operation with
   idempotency, receipt, rollback, approval, evidence and bounded spending
   specified. No delivery target or provider call is selected by this proposal.

This split keeps the existing complete offline kernel useful and makes the
missing guarantees measurable without reusing BER's live grant or rebuilding
CP-WP-002. No synthetic pass may be promoted to a live-readiness claim.
