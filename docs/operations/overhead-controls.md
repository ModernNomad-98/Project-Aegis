# C3.1 overhead controls: events, settlement, idle release and durable resume

**Scope.** C3.1 reduces avoidable CI/review overhead by consuming the existing
GitHub event set and the merged C1.1a store/checker. It adds no polling loop,
no scheduler and no second store.

## Event catalogue and duplicate semantics

The closed catalogue is `aegis.ops-event-catalogue/v1`. A row maps an existing
`(event_name, action)` pair to a stage action, a deterministic check, the
authority role, the state update and one duplicate rule:

| Duplicate rule | Meaning |
| --- | --- |
| `NO_OP` | A repeated delivery is recorded and performs no action |
| `RESTART_NOT_ALLOWED` | A repeated delivery cannot restart a stage; it is refused |
| `INVALID` | The event is refused |

Unknown event/action pairs are refused. An out-of-order delivery (a sequence
that does not strictly increase) is refused. A pull-request `edited` delivery
maps to `NO_STAGE_ACTION`: the body is checked by the structural bound-field
step, and a body edit does not re-run the whole pipeline. Duplicate no-ops are
visible in the report; they are not silently dropped.

Run:

```
python -m tools.aegis_ops validate --input tools/aegis_ops/tests/fixtures/event-catalogue-valid.json
python -m tools.aegis_ops validate --input tools/aegis_ops/tests/fixtures/duplicate-event-noop.json
python -m tools.aegis_ops validate --input tools/aegis_ops/tests/fixtures/out-of-order-event.json
```

## Bounded settlement

`aegis.ops-settlement/v1` records:

- `pre_audit_checks[]`: `check_id`, `state` (`pass`, `fail`, `neutral`,
  `unrun`, `bypassed`), `evidence_ref` and an explicit `deadline`;
- `review_sources[]`: `source_id` and `state` (`SETTLED`, `PENDING`,
  `UNAVAILABLE_DISPOSITIONED`), plus disposition-authority fields only when a
  real unavailable-review disposition is cited;
- `bounded_wait`: `deadline`, `max_attempts` and `observed_attempts`;
- `settled`: the **declared** value, which must equal the derivation, and
  `blockers[]`.

Derivation rules:

1. any required `PENDING` review source means `settled=false`;
2. an `UNAVAILABLE_DISPOSITIONED` source is BLOCKED while T7 is open, even
   when a citation is supplied - this slice does not invent the missing
   authority;
3. a declared-vs-derived mismatch is refused, never silently corrected;
4. `observed_attempts >= max_attempts` names `BOUNDED_WAIT_EXHAUSTED`;
5. a failed/unrun/bypassed pre-audit check is recorded and named as a blocker,
   but it does not by itself prevent a fully recorded settlement. Settlement is
   **not** readiness.

The deadline and attempts are inputs. The tool reads no clock and never loops.

## Merged-checker envelope

`python -m tools.aegis_ops settle --input PATH` prints the merged checker's
`--settlement` envelope. The merged checker at
[`scripts/aegis_verdict_gate/`](../../scripts/aegis_verdict_gate/README.md)
remains authoritative. The expected round-trip at this Stage C is **exit 1**
with named blockers, not a green result:

- T6 has no supported authentication method, so `VERDICT_STALE_OR_UNVERIFIED`
  or an equivalent blocker is expected;
- T24 leaves the revision-state store UNVERIFIED, so
  `REQUIRED_INPUT_UNAVAILABLE`/store blockers are expected;
- the result's `assurance.claim` is `AUDITABLE` and mounted coverage is
  `UNKNOWN`; `readiness` must not be reported as true.

The round-trip command is recorded in
[qualification-and-pilot-metrics.md](qualification-and-pilot-metrics.md) and in
the Stage C evidence record. A failed or blocked checker result is reported as
blocked, never as approval or green.

## Idle release and durable resume

A waiting agent is released with a recorded state bundle, not a prose promise.
The canonical bundle is the C3.4 context bundle
([stage-holders-and-replacement.md](stage-holders-and-replacement.md)):
candidate, stage, head/tree/base, frozen scope, active-holder refs, verdict
refs, triage ref, remaining UNRUNs, deadline, next action and a
`context_bundle_sha256`. Resume reads that bundle and the merged store/checker;
it does not rely on chat memory, a new store or idle supervision.

Validation: `python -m tools.aegis_ops holders --input ...` checks the bundle
hash and the one-active-holder rule. A missing or mismatched bundle fails
closed. No new store entry is appended; a real store extension would need
AUTH-STORE/T24 and is out of this slice.

## Authority honesty

- **T6 UNVERIFIED+BLOCKED** is displayed, never promoted.
- **T24 UNVERIFIED** is displayed; no verified-provenance count is claimed.
- **T7 OPEN** means a real unavailable-review disposition is BLOCKED; the
  one-time PR #1016 T7-equivalent exception is consumed and is not reused.
- **No enforcement/readiness/green claim** is made by the tooling or this
  procedure.

## UNRUN at this slice

Real event deliveries against a live PR, a real settlement/freeze/head-history
set and a real idle release/resume remain **UNRUN** until the dependency and
authority gates supply them. Synthetic fixtures are not production evidence.
