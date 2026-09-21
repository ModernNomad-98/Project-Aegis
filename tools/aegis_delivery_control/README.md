# Aegis delivery control kernel

This package is the CP-WP-002 offline state and recovery kernel. It provides a
deterministic transition authority, a repository-scoped SQLite state owner,
durable effect/use/budget/slot invariants, and a durable synthetic target
fixture. It is not a delivery integration.

## Boundary

- Only `SyntheticAuthority`, `SyntheticExecutionAdapter` and
  `SyntheticValidatorAdapter` exist.
- No network, provider, credential, shell, subprocess, Git mutation,
  deployment, production-data or real execution interface exists.
- The CLI is read-only. Lifecycle mutations are not exposed as commands.
- `SyntheticDispatchCoordinator` is the supported dispatch path: it authorizes
  T03, commits intent and capability redemption, then contacts the synthetic
  target. A committed intent is never silently redispatched after a crash.
- `SyntheticValidationCoordinator` commits a distinct T27 validator sub-intent
  before contacting the synthetic validator ledger. T24 intake reconstructs a
  final result from that canonical ledger and records it once. T11 application
  then consumes only that stored RESULT; intake never applies it implicitly.
- T01 atomically registers the accepted revision and its non-empty validation
  check set. T27 rejects checks outside that durable set.
- C04 admits effect receipts only through the canonical coordinator. Receipts
  carry repository, run, item, effect, attempt, claim, payload and receipt
  identity. Intake atomically appends receipt-backed budget settlement and
  observation events, retains the operation slot, and replays an identical
  command without duplicate accounting.
- C05 implements exactly-once PASS and classified FAIL application. An immutable
  application event marks the observation applied and settles its validator
  intent. PASS remains `VALIDATING` for pending checks or moves to `BLOCKED` for
  distinct T16 finalization. Issuer-verified `RECOVERABLE` failure moves to
  `BLOCKED` with the slot retained; `FINAL` moves to `FAILED_FINAL`, installs a
  permanent item/effect fence, and releases the slot only when no independent
  validation obligation remains. Committed applications replay from durable
  state without resupplying classification evidence. Plan acceptance durably
  pins the synthetic classification issuer, and every mutating path verifies
  raw event sequence, predecessor, body hash and row bindings before projections.
- The current worktree includes typed T18 graceful and T19 immediate stop requests.
  Stop commits `STOPPED`, a permanent scoped dispatch fence, the retained cursor,
  and synthetic grant redemption atomically while preserving existing slot and
  accounting obligations. T26 now accepts an exact already-applied T11/T12
  application as terminal closure evidence, without reapplying validation or
  reopening lifecycle, and releases the slot only after every check and accounting
  obligation is closed. T20 now escalates an expired graceful drain through a
  typed synthetic operator route, atomically classifies every ambiguous reserved
  obligation as `UNKNOWN_WORST_CASE_CHARGED`, records `STOP_ESCALATED`, and
  retains terminal lifecycle, fence, cursor and slot. Recovery binds the exact
  stop, plan, item, effect, slot and historical accounting snapshot. R-STOP-01
  and R-STOP-02 are independently accepted. Immediate T19 stop now also charges
  exact contacted, unresolved effect or validator liability at worst case in the
  same transaction. All three stop findings are independently accepted.
- T13 now ingests issuer-authenticated synthetic expiry, revocation,
  supersession, consumption, availability, unknown-claim and exact correction
  facts. A durable grant-wide effective-authority index is checked by effect,
  validator and operator consumers and again before adapter contact. Ordered
  historical disputes fence the affected provenance without changing terminal
  lifecycle; lawful own consumption permits only its exact in-flight action to
  continue while denying later reuse. Recovery reconstructs typed supersession
  graphs, stacked prohibitions and exact correction generations.
- T15 now pins the accepted source tree, item definition, plan schema and
  reducer, and derives domain-separated semantic-plan and complete-policy
  digests. Issuer-signed current-head SOURCE/ITEM/PLAN/POLICY mismatch
  observations atomically append `BINDING_MISMATCH`, a store-derived scoped
  fence and the deterministic lifecycle result. Idle work blocks, paused work
  stays paused, and active or uncertain work enters reconciliation without
  changing the accepted effect identity, plan, slot or accounting projections.
  Legacy unpinned plan events remain readable but cannot accept a new T15 fact.
- T14 now accepts an issuer-authenticated, exact-head resume request only from a
  durable pause source. The atomic `RESUME_ACCEPTED` transaction clears exactly
  that pause fence, retains every other fence, slot and accounting obligation,
  and routes clean PLANNED work back to PLANNED while retaining readiness,
  recovery and FINALIZING blockers in BLOCKED. Recovery verifies the complete
  run-head vector, signed request/capability evidence, exact event schema and
  historical route. Pre-T14 pause projections migrate transactionally without
  rewriting immutable event bodies. A public-path clean VALIDATING resume still
  depends on the ordered T08 pause-validation work and remains unverified.
- T05 now accepts an authenticated pause command for the exact repository slot
  owner in either the committed-intent/pre-launch or launched/pre-contact
  window. One transaction records a discriminated `PAUSE_REQUESTED`, an
  item/effect fence, full signed operator evidence and `RUNNING -> PAUSING`
  while retaining the attempt, reservation, permission use and cursor. A
  contacted attempt is denied to T06. This synthetic path performs no
  cancel/drain side effect and never treats parent exit or a pause request as
  cessation evidence.
- A local permission-use reservation is accounting, not real human authority.
- Recovery requires an independently obtained repository identity, catalog
  head, and complete run-id/head vector. A self-consistent SQLite file is not
  freshness proof, and an omitted or additional run fails verification.

## Storage and crash model

The state owner uses one standard-library SQLite database with foreign keys,
rollback-journal mode and `synchronous=FULL`. Each intent transaction commits
the event, effect index, synthetic permission use, budget reservation, command
outcome and repository-wide outstanding slot together. Budget settlement and
slot release are similarly atomic and append to the same run/catalog event
chain, so the independently supplied freshness vector advances with accounting.
Supported dispatch opens both controller and target ledgers only at the
repository-derived canonical state root; alternate roots are rejected.

The synthetic target uses a separate SQLite ledger. Its accepted effect and
receipt survive a controller restart, allowing a fresh adapter instance to
reconcile a lost receipt without contacting the target again.
The synthetic validator uses another repository-scoped SQLite ledger. Writes
require the exact issued validator capability, and a lost final result can be
reconciled without rerunning validation. Validator reservations are subordinate
to the existing operation slot; an active validator prevents slot release.

Tests establish process-crash and transaction-rollback behavior. They do not
establish power-loss durability for a filesystem, disk controller or host.
Unsupported or uncertain guarantees close dispatch.

The default database location is outside the checkout:

- Windows: `%LOCALAPPDATA%/ProjectAegis/control-plane/<repo-id-hash>/state.sqlite3`
- Linux: `${XDG_STATE_HOME:-$HOME/.local/state}/project-aegis/control-plane/<repo-id-hash>/state.sqlite3`

The stable `writer.lock` supplies cooperative OS-backed writer exclusion. It is
never deleted to take ownership and does not replace the durable outstanding
operation slot.

## Commands

```powershell
python -m tools.aegis_delivery_control --repository-id <id> capabilities
python -m tools.aegis_delivery_control --repository-id <id> status
python -m tools.aegis_delivery_control --repository-id <id> verify --expected-vector <json-file>
```

`status` reports stored facts without verifying freshness. `verify` requires a
JSON object containing exactly `repository_id`, `catalog_head`, and `run_heads`
obtained independently of the database; any identity, inventory, or head
difference fails closed.

## Current draft checkpoint

The 2026-09-21 checkpoint is implementation work in progress, not a deployable
controller. The complete local package suite ran 294 tests successfully, and
`git diff --check` passed. R-STOP-01 and R-STOP-02 received independent
implementation `APPROVE` after focused route, migration, accounting,
crash/replay, recovery and tamper validation:

1. stopping from `BLOCKED/FINALIZING` or a recoverable validation-failure state
  can now use T26 to bind the already-applied validation evidence and release the
  repository-wide slot atomically after every obligation closes; and
2. expired graceful drains can now use the typed T20 operator route to classify
  ambiguous reservations at worst case and durably record an idempotent
  escalation without releasing the outstanding slot.

R-STOP-03 now atomically classifies post-contact/pre-receipt uncertainty as
`UNKNOWN_WORST_CASE_CHARGED`, with exact historical recovery, crash/replay,
late-adjustment and alias/tamper coverage. The aggregate stop gate is `APPROVE`.
T13 authority lifecycle intake also received independent implementation
`APPROVE` after stacked-correction, typed supersession, cross-kind redemption,
own-consumption continuation, crash/replay, recovery and tamper review.
T15 binding-mismatch handling received independent implementation `APPROVE`
after its initial active-`BLOCKED` routing finding was corrected and re-tested
against idle, paused, active, uncertain and terminal cases.
The T14 PLANNED/BLOCKED resume slice received independent implementation
`APPROVE` after four recovery findings were corrected: exact event-schema
validation, non-null cursor reconstruction, true legacy cursor migration and
run-scoped active-validator recovery. T14 remains `UNVERIFIED` as a complete
transition until T08 supplies the public clean-VALIDATING pause/resume path.
T05 local-execution pause received independent implementation `APPROVE` after
the initial plan was corrected for the pre-launch window, durable capability
authenticity and T04/T05 schema separation, and the implementation was corrected
to bind its retained cursor to the recovered historical predecessor.
The broader exact T/C/F backlog and final reviews remain, so this checkpoint is
not merge-ready and does not authorize real authority, external calls, provider
integration, release, or deployment.

## Validation

```powershell
python -m unittest discover -s tools/aegis_delivery_control/tests -v
```

The tests cover the T01-T28 transition registry and deny-by-default behavior,
atomic intent rollback and replay, mediated T03 dispatch, durable cross-instance
claim redemption in one state database, budget uncertainty/release rules,
settlement-tail freshness, projection tamper rejection, restart-safe lost-receipt
reconciliation, atomic C04 settlement and observation rollback, post-commit
reopen and replay, complete receipt-provenance substitution denial, conflicting
identity and observation-projection tamper rejection, pre-commit settlement
rollback, post-commit settlement replay
without duplicate slot release, T27 validator-intent crash/replay and guard
behavior, T24 canonical result intake without application, unknown-accounting
reconciliation, T01 plan/check registration and tamper detection, exactly-once
C05 PASS/recoverable/final application, signed full-binding classification,
scoped terminal fencing, crash/restart replay, rebound denial, conditional slot
release, active-validator slot retention, cross-process writer exclusion, and
T18/T19 stop request, persistence, recovery, replay, late-evidence and fencing
behavior, plus T26 closure by exact already-applied PASS/recoverable-failure
evidence across T18/T19, crash/replay, migration and tamper boundaries. Passing
tests do not cover the two unresolved checkpoint findings.
The backlog remains the source of truth for acceptance cases not yet implemented,
including complete transition application, the unresolved stop cases above, and
filesystem ownership/reparse/path-swap enforcement.
