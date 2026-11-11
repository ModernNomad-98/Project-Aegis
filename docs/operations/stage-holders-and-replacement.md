# C3.4 stage holders, replacement and context transfer

**Scope.** C3.4 makes reviewer unavailability and replacement explicit and
checkable over existing state. It validates **declared** records; it does not
append to the merged revision-state store (that needs AUTH-STORE/T24), create a
second ledger, name reviewers or grant authority.

## Record set

`aegis.ops-stage-holders/v1` bundles:

| Record | Required fields |
| --- | --- |
| Stage holder | `holder_id`, `candidate_id`, `stage` (B/D/E/F), `holder_identity_ref`, `holder_role`, `activation_event_ref`, `authority_ref`, `independence_class`, `snapshot_identity`, `activated_at`, `bounded_wait_ref`, `deadline`, `state` (ACTIVE/REPLACED/SUPERSEDED/COMPLETED/DECLINED) |
| Replacement | `replacement_id`, `candidate_id`, `stage`, `old_holder_ref`, `new_holder_ref`, `reason_class` (INVALID/INCOMPLETE/UNAVAILABLE/CONFLICT/STALE), `finding_refs[]`, `authority_ref`, `authority_role`, `independence_attestation`, `snapshot_identity`, `context_bundle_sha256`, `created_at`, `status` |
| Unavailability | `unavailability_id`, `candidate_id`, `stage`, `source_ref`, `scope`, `evidence_ref`, `bounded_wait_ref`, `deadline`, `disposition` (WAIT_BOUNDED/REPLACE_EXPLICITLY/BLOCKED), `t7_ref` |
| Context bundle | `bundle_id`, `candidate_id`, `stage`, `head_sha`, `tree_sha`, `base_sha`, `frozen_scope`, `active_holder_refs[]`, `verdict_refs[]`, `triage_ref`, `unrun[]`, `deadline`, `next_action`, `prior_holder_separation`, `context_bundle_sha256` |

The bundle hash covers the canonical object without the hash field. A missing
or mismatched hash fails closed. The bundle is a record reference, not chat
history.

## Rules

1. **One active holder per stage/candidate.** Two simultaneous `ACTIVE`
   holders for the same stage are `DUPLICATE_ACTIVE_HOLDER`. A replacement
   first marks the old holder `REPLACED` or `SUPERSEDED`; there is no
   side-by-side lane.
2. **Replacement completeness and authority.** Missing reason, authority,
   old/new identity, independence, snapshot or bundle hash is refused. An
   implementer/PR-author role cannot authorise its own replacement.
3. **Independence.** The new holder must differ from the implementer, PR
   author, every commit author and the old holder. A self-approved replacement
   is `REPLACEMENT_SELF_APPROVAL`.
4. **Bounded unavailability.** Wait only to the recorded deadline, then
   explicit replacement or BLOCKED. No polling, unbounded retry or self-written
   exception. While T7 is OPEN, a real unavailable-review disposition is
   BLOCKED; the one-time PR #1016 exception is consumed.
5. **Invalidation/rebind.** A head/base/policy/evidence move suspends the
   active holder and requires a recorded rebind; stale bindings never continue
   silently.
6. **No duplicate lanes or hidden head churn.** At most one active D and one
   active E per frozen head; a replacement does not reset the review-head
   budget. A fourth head needs a recorded scoped exception with its R3 blocking
   basis.
7. **One component owner.** A replacement changes only the stage holder. The
   component owner and governance path stay single and unchanged;
   `component_owner_after` must equal `component_owner`.
8. **Status honesty.** Status shows active/replaced/unavailable/blocked and the
   permitted next action. `BLOCKED` wins; there is no authority inference.
9. **No new store.** A real stage-holder/replacement record appended to the
   existing store would need AUTH-STORE/T24; this slice emits normalized,
   hash-addressed programme-record JSON only.

## Recovery and durable resume

The context bundle is the resume state for C3.1-3: candidate, stage,
head/tree/base, frozen scope, verdict refs, triage, UNRUN, deadline and next
action. Resume does not rely on chat memory or a new store. A missing or
mismatched bundle blocks the act.

## Commands

```
python -m tools.aegis_ops holders --input tools/aegis_ops/tests/fixtures/holder-valid.json
python -m tools.aegis_ops holders --input tools/aegis_ops/tests/fixtures/holder-duplicate-active.json
python -m tools.aegis_ops holders --input tools/aegis_ops/tests/fixtures/replacement-valid.json
python -m tools.aegis_ops holders --input tools/aegis_ops/tests/fixtures/unavailability-no-t7-blocked.json
```

Expected: the duplicate-active, missing-authority, self-approve and
bundle-mismatch fixtures fail closed; the no-T7 unavailability record is
structurally valid but **blocked**, and the CLI exits 1.

## UNRUN

Real reviewer replacement, real unavailability disposition and a real store
append are **UNRUN**. T7 must be defined and AUTH-STORE/T24 resolved before
those records can exist. This page claims no enforcement and no approval.
