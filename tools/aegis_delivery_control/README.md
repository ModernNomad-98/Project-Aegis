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
- Accepted plans now pin a complete per-check terminal policy inside the signed
  acceptance payload and complete-policy digest. A late FAIL after authoritative
  all-descendant cessation creates the unapplied observation, irreversible
  terminal-policy obligation and fence atomically; exact immediate T19 stop
  fulfillment binds every open obligation, terminal-late intake never reopens
  the run, and dependent adoptions are fenced transitively.
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
  rewriting immutable event bodies. The reviewed T08 source now supplies the
  public clean-VALIDATING resume path; full T14 remains unverified while its
  other ordered source families remain outstanding.
- T05 now accepts an authenticated pause command for the exact repository slot
  owner in either the committed-intent/pre-launch or launched/pre-contact
  window. One transaction records a discriminated `PAUSE_REQUESTED`, an
  item/effect fence, full signed operator evidence and `RUNNING -> PAUSING`
  while retaining the attempt, reservation, permission use and cursor. A
  contacted attempt is denied to T06. This synthetic path performs no
  cancel/drain side effect and never treats parent exit or a pause request as
  cessation evidence.
- T06 now accepts an authenticated pause command only for the exact contacted
  external-mutation attempt. A durable contact without an intaken receipt is
  treated as bounded uncertainty: one transaction worst-case-charges a still
  reserved budget, records an `EXTERNAL_MUTATION` pause fence and enters
  `RECONCILIATION_REQUIRED` while retaining the slot and cursor. Existing
  accounting is retained by exact historical-prefix reference. The route makes
  no observe/cancel/retry call; later known or unknown receipts use T23 and do
  not reopen dispatch. Recovery verifies the full contact body/order and
  prefix-derived settlement head.
- T07 now settles the exact T05 local pause only after the same reservation's
  authoritative T25 `NONDISPATCH_PROVEN` release proves zero liability, no
  uncertainty or contradiction, and every obligation settled without releasing
  the operation slot. The atomic `PAUSE_SETTLED` event retains the pause fence,
  slot and `operation-recovery` cursor while advancing `PAUSING -> PAUSED`.
  Recovery independently derives the latest pre-T07 settlement, so intervening
  non-accounting facts remain valid. Its distinct T14 activity-resume route
  clears only that pause fence and returns to `BLOCKED`, retaining the exact
  slot generation, recovery cursor and every other blocker. It also accepts
  authenticated active-validator RESULT/INTERRUPTION/NONLAUNCH sources only
  after exact cessation or full nonexecution evidence and authoritative closed
  accounting. Result preserves the intent/application path; interruption and
  nonlaunch require a separate exact T16 successor authorization.
- T08 now accepts a typed, issuer-authenticated pause-validation request bound
  to one exact shared runtime/recovery checkpoint. Idle work, or a matching
  RESULT observation with known accounting and authoritative validator
  cessation, enters PAUSED. Uncontacted unresolved work retains RESERVED
  accounting; contacted unresolved work atomically settles a still-RESERVED
  budget as `UNKNOWN_WORST_CASE_CHARGED`; both enter
  `RECONCILIATION_REQUIRED`. Pause performs no adapter call or cancellation and
  retains the repository slot, cursor and application obligation. T14 can clear
  only this exact T08 fence and return a clean eligible checkpoint to
  VALIDATING; unresolved checkpoints cannot resume through T14.
- The active-validator T08 route adds an issuer-signed activity attestation for
  the exact durable contact and containment, records `VALIDATING -> PAUSING`,
  and retains slot, reservation and cursor. T07 closes only exact result plus
  cessation, interruption plus cessation, or complete T25 nonlaunch evidence.
  T14 returns the result path to VALIDATING and interruption/nonlaunch to
  BLOCKED; the latter consume one exact signed T16 recovery before a successor
  validator intent. Strict recovery rejects self-consistent source/cursor
  rewrites. The tranche received independent `APPROVE` with no blocker/major.
- The reviewed T17 validator-result route binds one exact observation,
  authoritative cessation, adjusted settlement and uncertainty set. Runtime and
  recovery use the same global-writer-epoch prefix reducer, reject superseded
  validator attempts, retain the typed validation-application cursor and route
  remaining same-run pauses to PAUSED while treating applicable cross-run
  fences as blockers. Its distinct versioned T14 request authenticates both the
  immutable T09/T17 sources and the independently current run head. Sequential
  resumes clear only their named T09 fences: the first stays PAUSED while a
  second remains, and the final clean resume returns to VALIDATING. Historical
  replay recognizes those exact clearances.
- The reviewed T17 operation-uncertainty foundation uses one canonical
  runtime/migration/recovery derivation. T06 records separate outcome, activity
  and source/control uncertainty and adds billing only for unknown accounting.
  Receipt intake requires typed issuer-authenticated source/control evidence;
  known historical accounting is not downgraded by missing telemetry. The
  version-0-to-1 semantic migration is atomic, rejects malformed or disguised
  legacy rows and validates settlement projections against immutable history;
  version 1 verifies exact rows/fences without healing.
- The reviewed T17 verified-receipt route records a closed, MAC-bound
  query/time/source/response envelope with mandatory `KNOWN` classification.
  It binds the exact durable receipt, accepted plan, repository slot and heads,
  proves every billing uncertainty through the complete settlement ancestry,
  and atomically records the reconciliation event, exact resolutions, fence
  deletions, action projection and next typed cursor. Same-run pauses route to
  `PAUSED`, remaining recovery/finalization blockers route to `BLOCKED`, and a
  clean prefix routes to `VALIDATING`; replay precedes mutable freshness and
  state guards. Semantic version 2, recovery and reopen validate the exact
  route-specific projection without rewriting legacy validator history.
- The local T17 proof-free disposition route accepts only separately
  authenticated one-use `REPORT_ONLY`, `STOPPED` or `FAILED_FINAL` owner
  commands. It binds the accepted plan, descriptor, exact repository/run heads,
  cursor, retained slot and complete unresolved operation-uncertainty set.
  Every branch preserves unknown outcome and historical accounting; report-only
  stays in reconciliation, while terminal branches add a permanent scoped fence
  without releasing the slot or manufacturing success/nonexecution. Semantic
  version 7 creates its projection atomically, rejects partial/missing schema,
  and reconstructs the exact accounting prefix and action from immutable
  history. Independent implementation review returned `APPROVE` after the
  accepted-plan issuer boundary and denial matrix were corrected; committed
  exact-head evidence is still pending.
- T22 exposes a separate read-only terminal-restart report. It opens existing
  main and auxiliary SQLite ledgers with `mode=ro` plus `query_only`, performs
  no initialization, migration, repair or lock-file creation, and separates
  local integrity from independent freshness and caller-anchor matching. Only
  a current, fully verified terminal entry invokes the T22 same-state guard;
  stale status remains non-authorizing and integrity/schema failure is reported
  unverified with dispatch closed. The route never resets budget/caps, releases
  a slot or authorizes T23/T26 reconciliation.
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

- Windows: the OS-known LocalAppData folder returned by
  `SHGetKnownFolderPath`, then
  `ProjectAegis/control-plane/<repo-id-hash>/state.sqlite3`; environment
  variables are not authority
- Linux: `${XDG_STATE_HOME:-$HOME/.local/state}/project-aegis/control-plane/<repo-id-hash>/state.sqlite3`

The stable `writer.lock` supplies cooperative OS-backed writer exclusion. It is
never deleted to take ownership, its initialized identity is required by every
later store mutation, and it does not replace the durable outstanding operation
slot. Checked paths reject lexical escapes, links, unsafe ownership/ACLs,
hardlinks, WAL/SHM and unsafe rollback journals. Windows retains the fixed-
volume/known-folder and managed-descendant handles for each connection/lock
scope. POSIX uses descriptor-relative no-follow traversal, but the current
checkpoint has no POSIX runtime receipt and does not claim one.

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

The 2026-09-22 checkpoint is implementation work in progress, not a deployable
controller. The complete local package suite ran 485 tests successfully, and
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
run-scoped active-validator recovery. T14 remains aggregate `UNVERIFIED`
pending committed-head trace refresh. Its active-validator sources are now
independently accepted: preserved results return to VALIDATING, while
interruption and nonlaunch return to BLOCKED until one exact T16 successor
authorization is consumed.
T05 local-execution pause received independent implementation `APPROVE` after
the initial plan was corrected for the pre-launch window, durable capability
authenticity and T04/T05 schema separation, and the implementation was corrected
to bind its retained cursor to the recovered historical predecessor.
T06 contacted external-mutation pause received independent implementation
`APPROVE` after the plan was corrected to route bare contact through
worst-case reconciliation and the implementation was corrected to verify the
complete historical contact body/order and prefix-derived accounting head.
It performs no adapter observe/cancel/retry and does not claim T07 settlement.
The reviewed T07 paths retain the slot and fence in PAUSED. In addition to the
exact T05/T25 local source, active-validator settlement now accepts only exact
RESULT/INTERRUPTION cessation or complete T25 nonlaunch evidence with
authoritative closed accounting. Result application is preserved; the retry
paths require exact T16. Runtime/recovery source and cursor derivation,
self-consistent rewrite rejection and one-use consumption received independent
`APPROVE`.
The reviewed T08 slice uses one exact checkpoint across runtime, T14 and
recovery. Its initial implementation review found two MAJOR gaps: a RESULT
checkpoint could omit authoritative cessation, and deterministic pause/contact
and pause/result races were not tested. Exact cessation ordering, serialized
verified reads and the two race regressions closed both; corrected independent
review returned `APPROVE`. The authenticated contacted active-validator drain
is now also implemented and accepted without claiming adapter cancellation.
T08 remains aggregate `UNVERIFIED` only until committed-head trace refresh.
T09 reconciliation pause received independent implementation `APPROVE` after
its first review identified one future-clearance schema defect. The corrected
route binds a typed one-use PAUSE capability to the exact current
`RECONCILIATION_REQUIRED` head, records a durable stacked fence without changing
the continuation cursor, accounting, outstanding slot or prior evidence, and
supports idempotent replay plus strict recovery. Its immutable action history
does not foreign-key the live fence, so later exact fence clearance can preserve
that history. T09 performs no adapter call and does not clear uncertainty.
The reviewed T17 validator-result slice and its distinct T14 T09-resume route
also received independent `APPROVE` after two correction rounds closed
repository-prefix scope, legacy-contract separation, stacked-fence chaining,
historical fence replay and full source rebinding. Two exact T09 fences now
clear sequentially without losing the typed validation-application cursor.
The reviewed operation-uncertainty foundation now adds typed source/control
evidence, conditional operation uncertainty, an atomic semantic migration and
exact-set recovery without promoting T17. The reviewed verified-receipt slice
adds proof-bound operation clearance, full accounting ancestry, typed routing
and exact replay/recovery. The authoritative-nonexecution and safe-retry slice
adds exact all-path seals, a typed T14/T16 recovery chain, one-use
generation-bound operation retry and generation-aware T10/T23/T27/T11/T12/
T16/T26 recovery. Safe-retry authorization requires and retains the exact
active T06 pause, ends PAUSED, and leaves outcome/activity uncertainty intact;
only separate effective one-use T14 RESUME authority clears that pause.
Stacked/new fences remain and prevent PLANNED, while expiry is rechecked through
target contact. Its corrected migrations preserve proof-time uncertainty
prefixes, newer fences, existing rows and foreign keys. The final F02
implementation review returned `APPROVE` with no BLOCKER or MAJOR finding.
T22 terminal-restart reporting received independent implementation `APPROVE`
after a write-capable auxiliary proof-ledger handle and an escaping structural
JSON error were corrected. Its 11 focused tests cover terminal/nonterminal,
freshness, corruption, trust, retained accounting/slot, concurrent snapshots
and byte-preserving main/auxiliary reads. T28/F01 verified-effect adoption also
received independent implementation `APPROVE`: it binds completed root and
immediate provenance, the current plan/check set and exact synthetic source
terms, consumes one adoption grant without redispatch or reused validation/
charge, persists transitive dependencies, and conservatively fences dependents
on contrary T23 evidence. Canonical relationship authority and source-history
recovery fail closed on rebinding, stale lifecycle, use-window or use-limit
violations. Cross-family F05/F06/F13/F20 now also has independent implementation
`APPROVE`: complete-vector freshness guards new one-use source consumption,
repository-wide slot tests cover lifecycle and generation boundaries, contrary
receipts are recovered across exact durable states, and validator containment
is typed, bounded, authority-bound and strictly reconstructed. Filesystem
ownership/reparse/path-swap protection now also has independent implementation
`APPROVE`: Windows actual junction/replacement and same-volume known-folder
rebound probes pass, the stable lock identity is pinned, and unsafe sidecars and
hardlinks fail closed. POSIX runtime remains `UNVERIFIED`. The broader exact
T/C/F trace and final reviews remain, so this checkpoint is
not merge-ready and does not authorize real authority, external calls, provider
integration, release, or deployment.

The selected-check foundation is independently accepted. New plan acceptance
uses authenticated v2 declarations for every check's dependencies and launch
gates, binds a deterministic topological order, persists normalized projections
and reconstructs them from event history. Legacy v1 plans fail closed at T27,
dependency order is enforced before validator intent, and authenticated
monotonic PASS/FAIL/UNKNOWN gate facts feed a signed complete launch snapshot.
Every v2 launch, including a zero-gate plan, now requires that current READY
snapshot and acquires an unclaimed validator grant inside the writer operation;
the production preclaimed entrypoints were removed. T11 atomically records an
exact signed next-check route, T16 resolves its bound blocked route after fresh
prerequisites pass, and contact rechecks either replay an existing contact or
durably disable stale initiation for exact T25 settlement and later T16 resume.
Crash rollback, lost acknowledgement, stale/rebound evidence, migration and
strict projection recovery are covered, and the corrected increment received
independent `APPROVE` with no findings. T11, T27, F11 and F17 remain
`UNVERIFIED` pending committed exact-head trace review. The local proof-free
T17/F18 branch is implemented and independently accepted but remains aggregate
`UNVERIFIED` pending committed exact-head evidence; remaining canonical gaps
are still open.

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
tests do not establish the remaining complete T/C/F families.
The backlog remains the source of truth for acceptance cases not yet implemented,
including complete transition application and final exact-head trace/review.
