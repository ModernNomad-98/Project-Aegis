# Resumable Aegis delivery control plane — separate work-package register

Owner: Peter Nguyen. Repository: ModernNomad-98/Project-Aegis.
Prepared: 2026-09-12. Base: `57e6928d2849aa5377daf52c723b85736292585d`.

This register records this delivery-control stream only. It does not alter the
[BER backlog](behavioral-eval-runner-backlog.md), BER authority or the existing
[owner approval register](../approvals/APPROVAL_REGISTER.md). A backlog entry or
approved design is not implementation authority. No runtime is delivered here.

## 1. Authority and continuation rules

The [design proposal](../design/resumable-control-plane-v1.md) owns proposed
architecture/state semantics; this file owns work-package scope and continuation.
The [review evidence](../evidence/control-plane/cp-wp-001-review.md) records actual
checks and review dispositions. Equal-authority contradictions stop dependent work.
Current direct human instructions govern before transcription; these records do
not create grants or replace the repository's one approval register.

Peter authorized CP-WP-001 as exactly three documents, a focused branch,
DCO-signed commits, one PR, existing CI and in-scope corrections. Runtime remained
excluded. PR #95 delivered that package and merged as
`32cbb2dff8265b2c2aaff38f2ace198417ef1646` on 2026-09-13. The task authority,
correction cycle and bounded delivery evidence remain in the evidence document
and PR history; they are historical instructions, not authority to reopen the
merged branch or begin another package.

Status vocabulary: AUTHORIZED = the human granted the exact package;
READY_FOR_OWNER_REVIEW = scoped delivery evidence exists, acceptance still pending;
BLOCKED = entry conditions/authority absent; DONE = owner disposition and required
delivery evidence recorded. No automatic phase advancement or implicit authorization.
Do not silently delete/relabel history; later dispositions cite evidence and scope.

## 2. CP-WP-001 contract

| Field | Contract |
| --- | --- |
| ID / title | CP-WP-001 — Durable State, Authority and Recovery Contract |
| Status | DONE — documentation-only contract merged in [PR #95](https://github.com/ModernNomad-98/Project-Aegis/pull/95) as `32cbb2dff8265b2c2aaff38f2ace198417ef1646`; no implementation |
| Owner | Peter Nguyen |
| Purpose | Make safe continuation decidable from durable identity, authority, events and evidence |
| Allowed scope | Create/correct exactly the three declarative Markdown files in section 3; reviewed design, separate backlog and sanitized evidence |
| Branch | `docs/cp-wp-001-durable-state-authority-recovery` |
| Reviewed/reconciled base | `57e6928d2849aa5377daf52c723b85736292585d`; fetched/live main matched at startup |
| Base-revision rule | Reverify live main; if advanced, read-only comparison may adopt only nonconflicting main with recorded reconciliation; material design/authority/evidence/scope conflict stops |
| Time | Maximum four active hours, excluding CI/owner waiting; stop/report rather than extend |
| File/change budget | Exactly three new Markdown files; maximum 1,500 added lines total; no other tracked changes |
| Spend | USD $0 task-controlled external spend; ordinary existing Codex session, approved read-only reviewers and existing GitHub CI excluded; no paid provisioning/API calls |
| Evidence | `docs/evidence/control-plane/cp-wp-001-review.md`; final head/tree/PR/exact-head CI in PR body and final handoff to avoid self-reference |
| Reviewers | Independent read-only architecture/recovery review and security/authority review; Peter for acceptance |
| Permitted delivery | Focused branch, explicit-path staging, DCO-signed commits, normal push, exactly one PR to main, all-check monitoring, in-scope corrections and owner-approved merge |
| Forbidden | Auto-merge/force-push/history rewrite; other PR/issues/releases/tags/deployments/settings; runtime/code/schema/policy/dependency/CI/BER/database/credential/holdout/provider actions |
| Non-goals | Offline kernel, physical extraction/wrappers, actual execution/containment, distribution, dashboard, BER advancement |
| Completion | Three-file bounded diff, local validation, independent re-reviews of all findings, evidence-backed resolution of all original/new threads, fresh exact-head Codex review with no blocking finding and all exact-head CI successful; merge only the verified reviewed head under the 2026-09-13 approval; auto-merge disabled |
| Next owner decision | Decide whether to authorize a separately scoped CP-WP-002; it remains BLOCKED and there is no automatic advancement |

### 2.1 Required evidence handling

Only sanitized repository facts, source links, commands/exits, hashes, review
findings/dispositions and explicit skips enter the evidence file. No credentials,
secrets, raw provider evidence, environment dumps, sealed holdouts or unrelated
untracked contents. Published documentation is permanent repository-safe history.
No active-state storage, raw evidence creation or deletion policy is executed here.

### 2.2 Acceptance and stop conditions

Acceptance requires: Role A/remote/base/grant reconciliation; explicit product/BER
boundaries; every required reuse primitive classified; all eleven logical components
and their authority limits; normative T01–T28 and C01–C09 coverage; identity,
idempotency, atomicity, pause/stop, corruption/schema/receipt handling; seven storage
classes and checkpoint transfer; platform limits/threats/tests; blocked later work;
reviewable three-file diff and actual validation evidence.

The corrected contract must cover CP-D01–CP-D10 and the negative families in
[design section 10.1](../design/resumable-control-plane-v1.md#101-finding-specific-negative-acceptance-families):
F01 stable cross-revision/run effect identity and durable approved distinctions;
F02 proof-free dispositions remain non-dispatching and cannot certify success;
F03 source-atomic one-use claims across all consumers with synthetic isolation;
F04a/F04b intent-owned versioned budget settlement for every receipt/non-dispatch/
cancellation/uncertainty/terminal/restart route; F05 independently fresh checkpoint
recovery; F06 atomic repository-wide outstanding slot across items/runs. Independent
review must verify transitions, storage/crash rules and negative cases agree; adding
prose or passing CI alone does not close a finding. The fresh-review follow-ups
add F07 receipt retention with UNKNOWN billing in reconciliation, F08 terminal
receipt admission with classified usage, and F09 T26 non-advancing terminal validation
settlement backed by T27 pre-launch intent. No-start proof cannot be inferred from
missing results; no terminal settlement may waive independent slot-release evidence.
F10–F17 trace independent multi-check application, initial unknown claims, consistent
non-launch recovery, contradictory receipts in every state, retained recoverable-failure
slots, delayed results after cancellation, exactly-once observation application and
selected-check prerequisites before launch. Reviewers must trace complete success,
failure, pause/stop and restart sequences across these rules, not just clause presence.
Include readiness/pause/reconciliation detours around recovery blockers, and a final
check applied before its aggregate gate clears: distinct finalization must release once.
F18-F21 require atomic final-failure fencing/settlement, proven nonexecution after
handoff, non-mutating contained validation and identity-bound uncertainty-fence clearance.
F01/F09/F19/F21 also require validation-only T28 adoption with its own free slot/current
checks, typed ceased-validator recovery, all-state contrary nonexecution intake and T25
exact-instance fence clearance, receipt-versus-retry serialization, source-atomic adoption approval use,
and terminal late authority facts. Independent review evidence names final design/backlog hashes;
historical hashes cannot attest changed normative bytes.

Stop on pre-existing tracked/staged changes, role/repository ambiguity, unrelated
target-branch work, material base conflict, additional file or line/time budget,
sensitive evidence, unresolved authority conflict, inconsistent design, forbidden
correction, another external resource/PR or merge without passing gates. Preserve unrelated
work. Green CI never supplies implementation or merge permission.

## 3. CP-WP-001 delivered file plan

| Action / file | Purpose / necessity | Protected gate surface at base |
| --- | --- | --- |
| Create `docs/design/resumable-control-plane-v1.md` | Single proposed architecture/state/durability/storage/threat/test contract | No current guard match; CODEOWNERS still applies |
| Create `docs/roadmaps/resumable-control-plane-backlog.md` | Independent scope, phase/authority and continuation record | No current guard match; CODEOWNERS still applies |
| Create `docs/evidence/control-plane/cp-wp-001-review.md` | Reconciliation, checks, review dispositions and evidence boundaries | No current guard match; CODEOWNERS still applies |

Everything else remains unchanged, especially `tools/`, `scripts/`, `.github/`,
`.claude/`, `.agents/`, `.codex/`, AGENTS.md, CLAUDE.md, README.md, approval register,
BER documents/evidence/runtime/tests/schemas, dependencies and `.gitignore`.
`artifacts/recovery/` and `artifacts/reviews/` remain completely untouched and
unstaged; do not inspect contents or add ignore rules for them. No index/catalog
edit is required; these three documents cross-link each other.

## 4. Historical validation and delivery protocol

This section preserves the protocol that governed PR #95. It is delivery
history, not an instruction to reopen that PR, recreate its branch or perform
another work package.

Before staging run `git diff --check`; inspect the complete correction diff and
all resulting three-file content. Inspect Markdown heading/table/fence
structure, local links/anchors and scenario coverage. Check only allowed paths.
Stage the three explicit paths. Run `git diff --cached --check` before each commit
and inspect the complete staged diff. Commit with DCO sign-off.

After committing run:

```text
git diff --check 57e6928d2849aa5377daf52c723b85736292585d...HEAD
git diff --no-renames --name-status 57e6928d2849aa5377daf52c723b85736292585d...HEAD
git status --short --untracked-files=normal
```

The committed name-status must contain exactly the three added files, and numstat
must remain within 1,500 additions. Use the reconciled base if it was legitimately
updated, and record that fact. Run existing safe applicable repository checks with
available dependencies only; disclose unavailable checks rather than installing.
Markdown/link checking is separate from skill validation; do not claim the latter
validates arbitrary documentation.

After a new DCO-signed correction commit, push normally to the existing branch and
update only [PR #95](https://github.com/ModernNomad-98/Project-Aegis/pull/95). Body
includes exact base/head/tree, file/line count, corrections, validation/reviews,
limitations and no-auto-merge. Reply separately to every finding with disposition,
corrected contract location and pushed commit; only then resolve its thread.
Request fresh Codex review explicitly naming that head. Monitor all review threads,
the new review and every attached CI check to terminal status. `validate-skills`,
`gate-guard` and `windows-offline-checks` must succeed on that head; old-head results
are historical. New findings require the same in-scope correction/review cycle.
Merge readiness requires no unresolved thread and no blocking fresh-review finding.
Merge the verified head under current owner approval; exceeding scope/budget stops.

[Existing CI](../offline-ci.md) runs without PR path filters and already performs
dependency setup, synthetic tests and evidence upload. It may run unchanged under
this task's express authorization; no local installation or CI modification follows.
All paths are maintainer-owned. The protected-file regex additionally guards BER,
CI/scripts/requirements and parent import files; absence of a guard match is not
permission for runtime work.

## 5. Separate future work packages — all blocked

| ID / purpose | Status / entry criteria | Proposed evidence / stop point |
| --- | --- | --- |
| CP-WP-002 — Offline state and recovery kernel | IN_PROGRESS under AEGIS-APR-004: standard-library SQLite rollback journal with `synchronous=FULL`; process-crash claims only; injected complete-vector freshness; versioned absolute budget settlements; synthetic-only authority/adapters | Current kernel demonstrates atomic intent rollback/replay, coordinator-owned T03 dispatch with durable PLANNED→RUNNING state, canonical supported controller/target roots, durable claim redemption, C04 canonical full-provenance receipt intake, and C05 exactly-once PASS/recoverable/final validation application. C05 uses store-bound issuer verification, full observation binding, item/effect-scoped permanent failure fences, crash/restart replay, and conditional slot release. It also proves event-anchored settlement/fence/slot facts, worst-case unknown charging, proof-bound release and OS writer exclusion. Filesystem ownership/reparse/path-swap protection and complete T01–T28/C06–C09/F01–F21 application remain blocking; do not promote to DONE |
| CP-WP-003 — Authority, evidence and execution capability contracts | BLOCKED: separate scope/approval, source-atomic approval claims/redemption including manual consumers, independent monotonic anchor or complete reconciliation, verified containment/fencing, evidence and bounded-liability accounting | Negative authority/race/rollback/path/process/receipt/billing probes; unavailable guarantees deny real dispatch; no live deployment/provider call without separately named grant |
| CP-WP-004 — One bounded delivery integration | BLOCKED: chosen integration, owner authority, idempotency/receipt/rollback semantics, source/evidence/budget pins and proven CP-WP-003 prerequisites | Exact-operation evidence and reviewed outcome; no automatic promotion to broad delivery or BER execution |
| CP-FUT-001 — Distributed ownership or hosted service | BLOCKED: demonstrated need and separate architecture/security/cost approval | Distributed fencing/failover/identity design and capability proof; local locks/checkpoints never satisfy it |

No later package is authorized by this register or by CP-WP-001 acceptance. BER
integration, if requested, additionally follows BER's current phase/evidence gates.

### 5.1 Authorized offline-kernel file plan

AEGIS-APR-004 authorized this file set and selected the storage/crash model on
2026-09-17. All paths are new except this backlog update. Logical interfaces can
share modules; do not create services or extract BER just to match a diagram.

| Action / file | Purpose / why needed | Protected gate surface at base |
| --- | --- | --- |
| Create `tools/aegis_delivery_control/__init__.py` | Package/version identity | No current match |
| Create `tools/aegis_delivery_control/__main__.py` | Existing module-command convention | No |
| Create `tools/aegis_delivery_control/cli.py` | Bounded synthetic plan/status/pause/resume/stop/recovery interface | No |
| Create `tools/aegis_delivery_control/contracts.py` | Typed records/identity and interfaces | No |
| Create `tools/aegis_delivery_control/engine.py` | Deterministic transitions and policy evaluation | No |
| Create `tools/aegis_delivery_control/authority.py` | Synthetic authority only, no real-adapter grant path | No |
| Create `tools/aegis_delivery_control/storage.py` | Selected journal, owner, projection and effect-index reconstruction | No |
| Create `tools/aegis_delivery_control/adapters.py` | Synthetic execution/receipt/reconciliation only | No |
| Create `tools/aegis_delivery_control/evidence.py` | Independent synthetic evidence/export contract | No |
| Create `tools/aegis_delivery_control/README.md` | Commands, limitations and capability requirements | No |
| Create `tools/aegis_delivery_control/tests/test_engine.py` | State/authority negative cases | No |
| Create `tools/aegis_delivery_control/tests/test_storage.py` | Corruption, interruption and writer exclusion | No |
| Create `tools/aegis_delivery_control/tests/test_recovery.py` | Receipt ambiguity, checkpoints and terminal restart | No |
| Create `tools/aegis_delivery_control/tests/test_platform.py` | Paths, locks and shell/platform acceptance | No |
| Create `.gitignore` | Narrow future scratch/cache rules only | No |
| Modify `docs/roadmaps/resumable-control-plane-backlog.md` | Record separately approved scope and evidence disposition | No |

No parent `tools/__init__.py`, requirements, runtime schema file or CI edit is
assumed. Such additions need their own explicit future scope; parent imports, BER
and CI changes would touch current protected surfaces. Future test plans are in
[design section 10](../design/resumable-control-plane-v1.md#10-future-tests-and-acceptance).

### 5.2 CP-WP-002 implementation evidence and remaining gate

The current implementation is deliberately not marked complete. Its read-only
CLI exposes no lifecycle mutation, network, provider, credential, shell, Git,
deployment, production-data or real-adapter path. SQLite stores immutable
hash-chained intent events and event-derived effect, permission-use, budget and
slot projections in one transaction. Recovery rejects projection divergence
before independent freshness can pass. Synthetic capabilities and settlement
proofs are issuer-verifiable. One state database atomically records claim
redemption with intent, and a separate durable synthetic target ledger preserves
accepted effects and receipts across adapter instances. These facts do not
establish protection against filesystem path replacement/permission attacks or
real source-atomic authority consumption.

Focused local evidence through 2026-09-19 includes the package `unittest` suite
on Windows and an actual second-process writer-lock denial. This evidence covers
important portions of T03/T21/T22/T23, C01-C04/C07-C09 and F03-F07. C04 now
admits only a canonical receipt carrying the complete repository/run/item/effect/
attempt/source binding, then writes its budget settlement and observation in one
transaction without releasing the operation slot. Injected failure between those
writes rolls both back; lost acknowledgement survives reopening, verifies from
immutable history and replays without duplicate events or accounting. Conflicting
durable identities and tampered observation projections fail closed. The focused
suite passed 63 tests, and independent QA and security rereviews accepted C04
without a remaining major finding. C05 now atomically applies stored validator
observations exactly once: PASS routes through T11; signed full-binding
recoverable/final classifications route through T12. Recoverable failures retain
the slot in `BLOCKED`; final failures enter `FAILED_FINAL`, install a permanent
item/effect fence, and release only when no independent check obligation remains.
Committed failure applications replay after restart without resupplying evidence;
rebound identities, forged evidence, unsupported policies and projection tampering
fail closed. The accepted plan durably pins the classification issuer fingerprint,
and every mutation verifies raw event-chain integrity before trusting projections.
Unrelated item/effect work remains eligible after a fully settled final failure.
The package suite passed 81 tests locally. Independent QA and security rereviews
accepted C05 with no remaining implementation finding; CI wiring remains the
documented, separately authorized follow-up below. C09
now
includes injected failure after settlement/slot writes before commit and after
commit before acknowledgement: the former rolls back fully and retries to one
exact charge/release, while the latter replays the same event without duplicate
accounting or slot release. This does
not yet establish the complete normative rows. Before DONE, complete executable
finalization records and crash replay for C06; then
cover the remaining F01-F21 families, especially multi-check validation,
stop/late-receipt ordering, adoption, exact fence clearance and complete
transition application. Add filesystem ownership/reparse/path-swap protections
and durable application paths for the remaining lifecycle rows. Re-run independent
architecture, security and QA reviews against the resulting exact head. Power-loss
durability and any real authority/execution capability remain unavailable, not
inferred from these process-level tests.
The delivery-control suite is not yet wired into repository CI; AEGIS-APR-004
does not authorize workflow changes, so CI gating remains a declared follow-up
rather than a silent scope expansion.

### 5.3 Paused CP-WP-002 checkpoint — 2026-09-21

The current checkpoint is based on `497a4529b84ec223245e001213271a9266514f62`
on `main`, which matched `origin/main` before checkpoint delivery. The working
tree contained 11 modified tracked delivery-control source/test files. The
accidental untracked `tools/aegis_delivery_control/dashboard/` detour was outside
AEGIS-APR-004, disconnected from the kernel and removed before checkpointing.
Existing untracked `artifacts/recovery/`, `artifacts/reviews/` and bytecode cache
directories were not added to the work package.

Fresh local evidence at this checkpoint:

| Command | Result |
| --- | --- |
| `python -m unittest discover -s tools/aegis_delivery_control/tests -v` | Exit 0; 198 tests ran in 16.659 seconds; `OK` |
| `git diff --check` | Exit 0; no whitespace errors |
| `git status --short --untracked-files=normal` | The 11 tracked delivery-control files remained modified; the dashboard no longer appeared; preserved artifact/cache directories remained untracked |
| `gh pr list --repo ModernNomad-98/Project-Aegis --state open ...` | Only unrelated Dependabot PR #98 was open; no CP-WP-002 PR or deployment existed |

Passing tests do not close the current independent gate. A read-only
`principal-architecture-reviewer` re-audit of T18/T19 and their required
T20/T23-T26 interactions returned `REVISE`:

1. **BLOCKER — terminal slot can be stranded.** STOP from
	`BLOCKED/FINALIZING` or recoverable validation failure can retain a slot that
	neither T16 nor T26 can later close. Add a T26-compatible terminal closure by
	reference to already-applied validation evidence, with crash/replay and
	unrelated-run dispatch tests.
2. **MAJOR — T20 is declaration-only.** Add a typed, idempotent escalation bound
	to the original graceful stop/deadline, the coordinator/storage transaction,
	`STOP_ESCALATED` event and recovery/projection validation, plus deadline,
	tamper and commit-boundary tests.
3. **MAJOR — post-contact immediate-stop uncertainty is underclassified.** When
	adapter contact is durably claimed but no receipt exists, T19 must atomically
	preserve the obligation and classify bounded liability as
	`UNKNOWN_WORST_CASE_CHARGED`, with late authoritative correction and replay
	tests.

No software was deployed. No release, production data, provider call, external
integration, real authority, credential, real adapter, BER, dependency, CI or
artifact-directory change is authorized by this checkpoint. CP-WP-003,
CP-WP-004 and CP-FUT-001 remain blocked. The exact continuation rules, current
file inventory, approval boundaries and ordered backlog are recorded in the
[Codex handoff](../evidence/control-plane/cp-wp-002-codex-handoff.md).

### 5.4 R-STOP-01 terminal slot closure checkpoint

R-STOP-01 is corrected and independently accepted. T26 now has a typed
`VALIDATION_APPLICATION` source that binds the exact prior T11/T12 application,
its observation, current validator attempt and complete plan/run/item/effect/check
identity. `PASS` maps only to `PASSED`; `FAIL` maps only to `FAILED`. The terminal
transaction never reapplies validation, changes classification or reopens the
run. It releases the repository-wide slot atomically only when
`_validation_checks_settled` and `_accounting_closure_error` establish closure of
every check, effect, validator and budget obligation.

The SQLite table constraint is upgraded by an atomic, exact-schema migration.
Historical rows, event bodies and hashes are preserved. Incompatible schema,
foreign-key divergence, source/application tampering and superseded attempts fail
closed. Focused coverage exercises both T18 and T19 from applied PASS
`BLOCKED/FINALIZING` and applied recoverable FAIL `BLOCKED/VALIDATING`, denial of
unrelated dispatch before closure, dispatch after closure, C05/C09 rollback and
lost-acknowledgement replay, populated legacy migration and self-consistent tamper
attempts.

| Evidence | Result |
| --- | --- |
| Initial plan audit | `REVISE`: typed mapping, four-route matrix, exact migration and crash assertions needed clarification |
| Corrected plan re-audit | `APPROVE`; no findings |
| Focused first falsification | Failed on unsupported `VALIDATION_APPLICATION`, then passed after the narrow implementation |
| `python -m unittest tools.aegis_delivery_control.tests.test_storage` | Exit 0; 168 tests ran in 14.231 seconds; `OK` |
| `python -m unittest discover -s tools/aegis_delivery_control/tests -v` | Exit 0; 209 tests ran in 16.666 seconds; `OK` |
| Independent implementation review | `APPROVE`; no blocker, major, minor or nit findings; reviewer independently ran 9 focused tests |

This checkpoint establishes only the R-STOP-01 slices of T18/T19/T26, C05/C09
and F06/F09/F14/F18. Full-row and full-family traceability remain `UNVERIFIED`.
R-STOP-02 and R-STOP-03 remain major blockers; the aggregate stop gate remains
`REVISE`, PR #99 remains draft, and no merge, release or deployment is ready.

### 5.5 R-STOP-02 graceful-stop escalation checkpoint

R-STOP-02 is corrected and independently accepted. T20 now has a typed
`StopEscalationRequest`, a synthetic operator-only coordinator route, and one
idempotent SQLite transaction bound to the exact graceful stop, persisted drain
deadline, accepted plan/run/item/effect, retained slot attempt/generation and
complete unresolved drain snapshot. The store's injected UTC clock must reach
the recorded deadline; the caller's deadline is binding evidence, not authority.

At escalation, every ambiguous `RESERVED` obligation in the snapshot is
atomically classified `UNKNOWN_WORST_CASE_CHARGED` through ordinary versioned
budget-settlement events. Known and already-unknown settlements are retained.
The transaction then records `STOP_ESCALATED`, operator redemption, command
outcome and projection without changing the terminal lifecycle, fence, cursor or
repository-wide slot. Recovery reconstructs the historical prefix, validates
the source/plan/slot identities and exact obligation/accounting snapshots, and
continues to accept later authoritative adjustments and terminal slot release.

| Evidence | Result |
| --- | --- |
| Initial plan audit | `REVISE`: exact ambiguous-reservation conversion, historical-prefix validation, drain predicate and operator route required clarification |
| Corrected plan re-audit | `APPROVE`; no findings; synthetic operator route accepted, approved-rule scheduler explicitly omitted |
| Focused first falsification | Failed because the coordinator lacked `escalate_stop`, then passed after the narrow implementation |
| Focused T20 suite after review correction | Exit 0; 10 tests ran; `OK` |
| `python -m unittest tools.aegis_delivery_control.tests.test_storage` | Exit 0; 177 tests ran in 14.474 seconds; `OK` |
| `python -m unittest discover -s tools/aegis_delivery_control/tests -p 'test_*.py'` | Exit 0; 219 tests ran in 19.387 seconds; `OK` |
| `python scripts/validate-skills.py` | `OK: 184 skill(s) valid, 0 warning(s)` |
| `python scripts/tests/test_validator.py` | `OK: 91 gate self-test assertion(s) passed` |
| Independent implementation review | Initial `REVISE` for self-consistent item retargeting; corrected re-review `APPROVE`, no findings; reviewer independently passed 10 focused tests and reproduced fail-closed retarget recovery |

This checkpoint establishes T20's operator route and its C06/C09/F04b slices.
It does not claim an approved deadline-rule scheduler. R-STOP-03 remains a major
blocker, so the aggregate stop gate remains `REVISE`, PR #99 remains draft, and
no merge, release or deployment is ready.

### 5.6 R-STOP-03 post-contact immediate-stop checkpoint

R-STOP-03 is corrected and independently accepted. Every new immediate T19 stop
records an exact nested uncertainty snapshot while preserving the legacy event
envelope and historical stop bodies. A contacted effect or validator reservation
with no exact receipt/observation/cessation/nonexecution resolution is atomically
settled from `RESERVED` to `UNKNOWN_WORST_CASE_CHARGED` before `STOP_RECORDED` in
the same writer epoch. Pre-contact reservations remain reserved and known
accounting is never downgraded.

Settlement identities are domain-separated hashes of the stop, exact reservation,
contact identity/hash and predecessor head. Recovery reconstructs the historical
prefix and rejects omitted, added, retargeted or aliased contact classifications
while allowing later authoritative adjustment without reopening the terminal run.

| Evidence | Result |
| --- | --- |
| Initial plan audit | `REVISE`: exact legacy compatibility, durable identity, per-contact historical predicates and exact-set/crash coverage required |
| Corrected plan re-audits | `REVISE` for infeasible event-envelope v2, then `APPROVE` after retaining envelope schema 1 with exact nested snapshot version 1 |
| Focused first falsification | Failed with contacted reservation still `RESERVED`; passed after atomic T19 settlement |
| Focused R-STOP-03 suite | Exit 0; 7 tests; `OK` |
| Storage module | Exit 0; 184 tests; `OK` |
| Complete delivery-control package | Exit 0; 226 tests; `OK` |
| Independent implementation review | Initial `REVISE` for cross-run/effect attempt-ID alias; corrected re-review `APPROVE`, no remaining blocker/major; reviewer independently passed 7 focused tests and reproduced the corrected probe |

This establishes the R-STOP-03 slices of T19, C09, F04b and F08. All three
stop findings are independently accepted and the aggregate stop gate is
`APPROVE`. Full-row/family traceability remains unclaimed where the matrix says
`UNVERIFIED`; PR #99 remains draft and not merge-ready for the remaining backlog.

### 5.7 T13 authority lifecycle checkpoint

T13 is implemented and independently accepted. Typed, issuer-authenticated
synthetic lifecycle facts cover expiry, revocation, supersession, foreign and
own consumption, source unavailability, unknown local claim status and exact
correction. One atomic event records the governed boundary/order, durable
grant-wide effective-authority generation, scoped provenance fence and
deterministic lifecycle result. Effect, validator and operator consumers consult
the index, with a second exact check before adapter contact.

Corrections rematerialize the newest remaining uncorrected prohibition rather
than erasing stacked facts. Typed supersession graphs admit independent acyclic
chains by issuer/kind/action/scope, reject conflicts and reachability cycles, and
remove only an exactly corrected edge. Lawful own consumption remains a durable
future-use denial while allowing only its exact already-committed intent to
continue through launch/contact. Terminal lifecycle never reopens.

| Evidence | Result |
| --- | --- |
| Plan audit | Initial `REVISE` rounds clarified the fact/order table, claim-status retention, typed graph, exact correction and lifecycle routes; corrected plan `APPROVE` |
| Focused first falsification | Failed because `record_authority_fact` was absent; passed after the typed durable route |
| Complete delivery-control package | Exit 0; 242 tests; `OK` |
| `python scripts/validate-skills.py` | `OK: 184 skill(s) valid, 0 warning(s)` |
| `python scripts/tests/test_validator.py` | `OK: 91 gate self-test assertion(s) passed` |
| Independent implementation review | `REVISE` findings for stacked correction, claim-kind binding, graph reachability/namespacing and own-use continuation were corrected; final `APPROVE`, no remaining blocker/major; reviewer passed 16 focused tests |

This promotes T13 itself to `YES/YES/YES`. It establishes the T13 slices of C08
and F03 only; full cross-family C08/F03 traceability remains `UNVERIFIED`. T15 is
the next ordered item, followed by T14. PR #99 remains draft and not merge-ready.

### 5.8 T15 immutable binding-mismatch checkpoint

T15 is implemented and independently accepted. New plan acceptance requires
explicit source-tree, item-definition, plan-schema and reducer pins. Acceptance
persists a domain-separated semantic-plan digest and a complete-policy digest
covering permission/budget policy, checks/gates, failure-classification policy
and issuer, finalization policy and issuer, schema and reducer. Historical
unpinned plan events remain readable with NULL derived fields, but cannot accept
a new mismatch fact.

Typed SOURCE, ITEM, PLAN and POLICY mismatch requests carry an issuer-signed,
current-head synthetic observation. Storage rederives the accepted value, owns
the deterministic reason-keyed fence identity and atomically records the event,
fresh observation, projection, fence, command outcome, catalog/run heads and
lifecycle. PAUSED retains its state and fence; truly idle work becomes BLOCKED;
active or uncertain work, including BLOCKED/FINALIZING with the outstanding
slot, becomes RECONCILIATION_REQUIRED. Terminal states reject T15. Recovery
recomputes the plan/policy digests, evidence MAC, historical activity predicate,
route, fence and full projection/fence union.

| Evidence | Result |
| --- | --- |
| Plan audit | Two `REVISE` rounds added explicit source pins, authenticated/store-derived observations, complete policy identity, strict legacy migration, exact kind mapping and narrow F01 boundaries; corrected plan `APPROVE` |
| Focused first falsifications | Unpinned plan was initially accepted; the first typed mismatch then failed because `record_binding_mismatch` was absent; both became green through the narrow implementation path |
| Focused T15 suite | Exit 0; 14 tests; `OK` |
| Complete delivery-control package | Exit 0; 256 tests; `OK` |
| `python scripts/validate-skills.py` | `OK: 184 skill(s) valid, 0 warning(s)` |
| `python scripts/tests/test_validator.py` | `OK: 91 gate self-test assertion(s) passed` |
| Independent implementation review | Initial `REVISE` found active BLOCKED work incorrectly treated as idle; historical-prefix activity routing and regression coverage corrected it; final `APPROVE`, no remaining blocker/major; reviewer passed 14 focused tests |
| Commit/push and hosted checks | Signed-off commit `2de362612f43c125829ff8c73e22bcdcfa6147c0` pushed to the existing branch; `gate-guard`, `validate-skills` and `windows-offline-checks` passed on that exact head; PR #99 remained open, draft and blocked |

This promotes T15 itself to `YES/YES/YES`. The narrow F01 non-mutation controls
show that T15 does not change an existing effect key/descriptor, accepted plan,
slot or accounting state, but full F01 remains `UNVERIFIED` for the later T28
work. T14 is the next ordered item. PR #99 remains draft and not merge-ready.

### 5.9 T14 pause-source resume checkpoint

The reviewed T14 slice adds a typed resume request, issuer-authenticated exact
request evidence and a coordinator-owned route from durable PAUSED history. The
state owner verifies the current catalog and complete run-head vector, accepted
plan/revision, exact pause settlement and active pause fence. One transaction
appends `RESUME_ACCEPTED`, clears only the source pause fence, redeems the
operator grant and updates the run/catalog heads. Other fences, readiness
blockers, the repository-wide slot, accounting and intervening facts survive.
Unresolved activity owned by the resumed run still requires T17; unrelated-run
activity yields BLOCKED without making the committed resume unrecoverable.

Recovery verifies the exact event and nested evidence schemas, issuer MACs,
full historical prefix, route, cursor and projections. A compatibility-safe
migration adds preserved lifecycle/cursor columns to the legacy pause projection,
derives their values from verified pre-pause history and does not rewrite legacy
event bodies. Partial schemas and malformed prefixes fail transactionally.

| Evidence | Result |
| --- | --- |
| Plan audit | Two `REVISE` rounds closed source-pause/current-vector, legacy migration, route, capability-MAC and public VALIDATING-path scope gaps; corrected plan `APPROVE` |
| Focused first falsifications | Typed request, coordinator route, signed evidence, authority action, durable route and recovery tests failed before their narrow implementations; the later review probes reproduced four additional recovery gaps before correction |
| Focused T14 suite | Exit 0; 21 tests in 0.957 seconds; `OK` |
| Affected storage/dispatch modules | Exit 0; 255 tests in 21.039 seconds; `OK` |
| Complete delivery-control package | Exit 0; 277 tests in 22.194 seconds; `OK` |
| Repository validators | 184 skills valid with zero warnings; 91 gate self-test assertions passed; `git diff --check` exit 0 with line-ending notices only |
| Independent implementation review | Initial `REVISE` found surplus-schema acceptance, non-null cursor replay, true-legacy projection and cross-run validator divergences; corrected final `APPROVE`, no remaining blocker/major; reviewer passed 21 focused tests in 0.982 seconds |
| Commit/push and hosted checks | Signed-off commit `c3c94bf3d367380d1ff60835fb72cb300e69c3e4` pushed to the existing branch; `gate-guard` passed in 3s, `validate-skills` in 1m18s and `windows-offline-checks` in 3m23s; PR #99 remained open, draft and blocked |
| Intentionally untouched | Canonical design, approval register, BER, dependencies, CI, CLI, artifacts/caches, real authority/adapters and external systems |

T14 remains `UNVERIFIED/UNVERIFIED/UNVERIFIED` as a complete transition. The
reviewed PLANNED/BLOCKED resume slice and narrow C06/C07 and F03/F05/F06/F12/F14/F21
interactions do not establish those complete families. Exact public-path clean
VALIDATING resume is intentionally deferred to the ordered T08 work. At this
checkpoint T05-T09 was next; section 5.10 records the completed T05 successor.
PR #99 remains draft and not merge-ready.

### 5.10 T05 local-execution pause checkpoint

T05 is implemented and independently accepted for the synthetic request-only
local-execution boundary. `PauseLocalExecutionRequest` binds the exact committed
intent event/hash, repository slot owner and generation. The store admits both
valid RUNNING windows: committed intent before launch and a launch with no
adapter contact. A contacted attempt is denied to the ordered T06 route.

The single atomic transaction appends a closed-schema, explicitly
`LOCAL_EXECUTION` `PAUSE_REQUESTED`, installs an item/effect fence, persists the
full signed operator capability and redemption, advances RUNNING to PAUSING and
retains the outstanding slot, permission use, budget reservation, launch and
continuation cursor. The coordinator performs no cancel/drain contact: this
offline kernel has no trusted local-child cancellation adapter, so neither a
pause request nor parent exit is represented as cessation proof. Contact and
pause serialize under the repository writer boundary; only the committed
contact or committed fence can win.

Recovery reconstructs and verifies the exact intent and historical slot,
issuer MAC, closed T05/T04-discriminated event shape, projection/redemption/fence
union, predecessor lifecycle and predecessor-derived continuation cursor.
Self-consistent event/projection/head rewrites of capability fields, cursor or
surplus schema fail closed.

| Evidence | Result |
| --- | --- |
| Plan audit | Initial `REVISE` found three MAJOR gaps: launch was over-required, the capability MAC was not durably recoverable and T05 was not separated from T04 history; corrected plan `APPROVE` with no remaining blocker/major |
| Focused first falsifications | Typed contract failed because it was absent; store route failed because `pause_local_execution` was absent; coordinator route failed because it was absent; each passed after its narrow implementation |
| Focused T05 suite | Exit 0; 17 tests in 0.675 seconds; `OK` |
| Affected storage/dispatch modules | Exit 0; 272 tests in 22.140 seconds; `OK` |
| Complete delivery-control package | Exit 0; 294 tests in 23.893 seconds; `OK` |
| Repository validators | 184 skills valid with zero warnings; 91 gate self-test assertions passed; `git diff --check` exit 0 with line-ending notices only |
| Independent implementation review | Initial `REVISE` found a forgeable retained cursor; prefix-derived cursor validation and a self-consistent tamper regression corrected it; final `APPROVE`, no remaining blocker/major; reviewer independently passed 17 focused tests in 0.743 seconds |
| Commit/push and hosted checks | Signed-off commit `13bda54b9bc63e962a3900ac16640fd2bb18d304` pushed to the existing branch; `gate-guard` passed in 4s, `validate-skills` in 1m18s and `windows-offline-checks` in 3m22s; PR #99 remained open, draft and blocked |
| Files changed | `contracts.py`, `dispatch.py`, `storage.py`, `test_dispatch.py`, `test_storage.py` |
| Intentionally untouched | Canonical design, approval register, BER, dependencies, CI, CLI, artifacts/caches, real authority/adapters and external systems |

This promotes T05 itself to `YES/YES/YES`. Its accepted crash/replay and
repository-slot-retention slices inform C06 and F06, but both complete families
remain `UNVERIFIED`. No cancel/drain adapter or T07 settlement is claimed. T06
through T09 are next in their documented order; PR #99 remains draft and not
merge-ready.

### 5.11 T06 contacted external-mutation pause checkpoint

T06 is implemented and independently accepted for the synthetic contacted,
no-control-plane-receipt boundary. `PauseExternalMutationRequest` binds the exact
committed intent, operation launch, durable `EFFECT` adapter contact, canonical
target digest, repository slot owner and generation. Bare contact is not treated
as proof that the mutation remains active or drainable. The only implemented T06
outcome is therefore `RUNNING -> RECONCILIATION_REQUIRED`; no unauthenticated
`PAUSING` branch is claimed.

One writer transaction converts a still-`RESERVED` reservation to a normal,
versioned `UNKNOWN_WORST_CASE_CHARGED` settlement at W, appends the closed-schema
`EXTERNAL_MUTATION` `PAUSE_REQUESTED`, installs the item/effect fence and redeems
the signed operator grant. Existing known or unknown accounting is retained by
exact prefix-head reference without downgrade or duplicate charge. The slot,
effect identity, intent/launch/contact evidence and continuation cursor remain.
The route performs no adapter observe, cancel, rollback, retry or new mutation
and never infers cessation. A later receipt enters through T23: known use adjusts
the prior worst-case charge while unknown use retains it; both remain in
reconciliation with the fence and slot intact.

Recovery round-trips the complete contact event body and independently verifies
its repository/run/item/effect/attempt/kind/source/target/hash and strict
pre-pause order. It derives the reservation disposition and settlement head from
the pre-transaction writer-epoch prefix rather than trusting the pause snapshot.
Self-consistent contact retarget, settlement-head retarget, snapshot, projection,
schema and cursor/history tampering fail closed.

| Evidence | Result |
| --- | --- |
| Plan audit | Initial `REVISE` found one BLOCKER and two MAJOR gaps: bare contact was incorrectly treated as ordinary PAUSING, worst-case accounting was omitted and later receipt routing incorrectly used T10; corrected plan `APPROVE` with no remaining blocker/major |
| Focused first falsification | The coordinator test failed at import because `PauseExternalMutationRequest` was absent; the narrow typed route then made the contacted/no-receipt worst-case behavior pass |
| Focused T06 suite | Exit 0; 14 tests in 0.923 seconds; `OK` |
| Affected storage/dispatch modules | Exit 0; 285 tests in 23.229 seconds; `OK` |
| Complete delivery-control package | Exit 0; 307 tests in 23.939 seconds; `OK` |
| Repository validators | 184 skills valid with zero warnings; 91 gate self-test assertions passed; compileall passed; `git diff --check` exit 0 with line-ending notices only |
| Independent implementation review | Initial `REVISE` found two MAJOR recovery gaps in exact contact-body/order verification and prefix-derived retained accounting; both were corrected with self-consistent tamper regressions; final `APPROVE`, no remaining blocker/major; reviewer independently passed 14 focused tests in 0.824 seconds |
| Commit/push and hosted checks | Signed-off commit `39b3268adc984e3d0b10e55a42fe37a172229e60` pushed to the existing branch; `gate-guard` passed in 7s, `validate-skills` in 1m20s and `windows-offline-checks` in 2m49s; PR #99 remained open, draft and blocked |
| Files changed | `contracts.py`, `dispatch.py`, `storage.py`, `test_dispatch.py`, `test_storage.py` |
| Intentionally untouched | Canonical design, approval register, BER, dependencies, CI, CLI, artifacts/caches, real authority/adapters and external systems |

This promotes T06 itself to `YES/YES/YES`. Its accepted contact uncertainty,
crash/replay, late-receipt and slot-retention slices inform C03, C06, F06, F07
and F08, but those complete families remain `UNVERIFIED`. No authenticated
active/drainable PAUSING route or T07 settlement is claimed. T07 through T09 are
next in their documented order; PR #99 remains draft and not merge-ready.

### 5.12 T07 local nonexecution settlement checkpoint

The reviewed T07 slice settles only an exact T05 local-execution pause whose
same attempt and reservation have an authoritative T25 `NONDISPATCH_PROVEN`
settlement. That proof must be the reservation's latest pre-T07 accounting
head, `RELEASED`, zero-liability, non-uncertain, non-contradictory and complete,
with `release_slot=false`. One transaction appends the distinct
`ACTIVITY_SETTLEMENT` `PAUSE_SETTLED` event and projection, advances
`PAUSING -> PAUSED`, and retains the pause fence, outstanding slot, T25
accounting and `operation-recovery:<attempt>` cursor.

The associated versioned T14 activity-resume route uses a distinct typed
request/evidence/projection so legacy T04 signed bytes remain unchanged. It
clears only the exact T05 fence and returns `PAUSED -> BLOCKED`, retaining the
recovery cursor, outstanding slot and every non-pause fence/blocker. Runtime and
recovery bind the slot generation to the exact T07 projection/event pair rather
than assuming generation 1. Recovery derives the latest reservation settlement
from the historical prefix independently of journal chaining, so a legitimate
intervening T13 non-accounting fact remains recoverable.

| Evidence | Result |
| --- | --- |
| Plan audit | Three `REVISE` rounds closed authority/cessation overclaim, missing T25/T17/T14 interactions, projection separation and legacy signed-request compatibility; corrected plan `APPROVE` with no remaining blocker/major |
| Focused falsification and correction tests | Initial typed-contract/coordinator tests failed before implementation; final correction suite passed 3 tests in 0.197 seconds |
| Affected storage/dispatch modules | Exit 0; 296 tests in 24.830 seconds; `OK` |
| Complete delivery-control package | Exit 0; 318 tests in 25.638 seconds; `OK` |
| Repository validators | 184 skills valid with zero warnings; 8 script tests passed with 4 expected skips; 91 gate self-test assertions passed; compileall passed; `git diff --check` exit 0 with line-ending notices only |
| Independent implementation review | Initial `REVISE` found two MAJOR recovery defects: journal predecessor was incorrectly equated with T25 head and T14 assumed slot generation 1. Prefix-derived accounting and exact T07 generation binding, with intervening-T13 and non-1 regressions, closed both. Final `APPROVE`, no remaining blocker/major; reviewer independently passed 3 correction tests in 0.194 seconds |
| Commit/push and hosted checks | Signed-off commit `a0d27bbdd64d7d86bf080355ca933d28760244ab` pushed to the existing branch; `gate-guard` passed in 5s, `validate-skills` in 1m19s and `windows-offline-checks` in 2m58s; PR #99 remained open, draft and blocked |
| Files changed | `contracts.py`, `authority.py`, `dispatch.py`, `storage.py`, `test_dispatch.py`, `test_storage.py`, plus status README/backlog/handoff synchronization |
| Intentionally untouched | Canonical design, approval register, BER, dependencies, CI, CLI, adapters, artifacts/caches, real authority/adapters and external systems |

T07 remains `UNVERIFIED/UNVERIFIED/UNVERIFIED` as a complete transition: this
checkpoint proves only the T05-local/T25-authoritative nonexecution source. T08
validation-pause and T24/other source families remain ordered work, so full T14
also remains `UNVERIFIED`. The accepted slice informs C06 and F06/F12 but does
not promote those complete families. The T08 slice below is next; PR #99 remains draft and not
merge-ready.

### 5.13 T08 validation-pause checkpoint

The reviewed T08 slice introduces a distinct typed pause-validation request and
one exact checkpoint shared by runtime, T14 and recovery. `IDLE` and an
`ELIGIBLE_RESULT_SETTLED` checkpoint with an exact RESULT observation, known
accounting and authoritative validator cessation enter `PAUSED`. Unresolved
work enters `RECONCILIATION_REQUIRED`: uncontacted work retains its RESERVED
budget, while contacted work atomically settles a still-RESERVED budget as
`UNKNOWN_WORST_CASE_CHARGED`. The transaction retains the repository-wide slot,
validation cursor and result-application obligation, and performs no adapter
observe, cancel or retry call.

The associated T14 route accepts only the exact clean T08 PAUSED source, clears
only its pause fence and resumes `VALIDATING`. It rejects unresolved T08
checkpoints. Recovery independently derives the same checkpoint from the
historical prefix, validates the full signed operator capability and closed
event/projection schemas, and verifies the deterministic uncertainty settlement.
Repository writer serialization prevents a verifier from accepting a mixed
projection/event snapshot while contact or result intake commits.

| Evidence | Result |
| --- | --- |
| Plan audit | Initial `REVISE` identified three checkpoint/cessation/race gaps; the corrected narrow plan received `APPROVE` before editing |
| Focused falsification and race tests | 13 T08 tests passed locally in 2.536 seconds; the two deterministic race tests passed in three repeated runs |
| Affected dispatch module | 40 tests passed in 4.925 seconds |
| Complete delivery-control package | 331 tests passed in 28.693 seconds |
| Repository validators | 184 skills valid with zero warnings; 8 script tests passed with 4 expected skips; 91 gate self-test assertions passed; compileall passed; `git diff --check` exit 0 with line-ending notices only |
| Independent implementation review | Initial `REVISE` found two MAJOR gaps: zero cessation was accepted as eligible and pause/contact plus pause/result races lacked deterministic coverage. Both were corrected; final `APPROVE`, no remaining blocker/major; reviewer independently passed 13 focused tests in 2.479 seconds |
| Commit/push and hosted checks | Reviewed implementation commit `a0d27bbdd64d7d86bf080355ca933d28760244ab` and evidence commit `9b4cc6ff0d656409b071e16ed6a81ec06a692e5a` were pushed; all three hosted checks passed on both exact heads; PR #99 remained open, draft and blocked |
| Files changed | `contracts.py`, `dispatch.py`, `storage.py`, `test_dispatch.py`, `test_storage.py`, plus status README/backlog/handoff synchronization |
| Intentionally untouched | Canonical design, approval register, BER, dependencies, CI, CLI, adapters, preserved artifacts/caches, real authority/adapters and external systems |

T08 remains `UNVERIFIED/UNVERIFIED/UNVERIFIED` as a complete transition. This
slice proves the synthetic idle, exact settled-result, uncontacted uncertainty
and contacted worst-case branches plus the clean VALIDATING T14 route; it does
not claim authenticated active drain/cancel or every T17/T24 cessation source.
T14 and the implicated C/F families likewise remain `UNVERIFIED`. T09 follows;
PR #99 remains draft and not merge-ready.

### 5.14 T09 reconciliation-required pause checkpoint

T09 now has a distinct typed operator request and coordinator/state-owner route
for an already durable `RECONCILIATION_REQUIRED` run. The request binds the
repository, run, item, logical effect, accepted plan and revision, exact current
source event ID/hash, preserved continuation cursor, new event and fence IDs,
reason and signed one-use PAUSE capability. Under the repository writer lock and
one `BEGIN IMMEDIATE` transaction, the route verifies the current head, cursor,
plan and authority, appends `PAUSE_FENCE_RECORDED`, inserts the fence and immutable
action projection, redeems the capability and advances both durable heads.

The lifecycle remains `RECONCILIATION_REQUIRED`. The route leaves accounting,
the repository-wide outstanding slot, continuation cursor, prior evidence and
prior fences unchanged, performs no adapter call and does not hide or clear
uncertainty. Same-command replay is idempotent; a distinct stale-source command
is denied, while a deliberate new command bound to the new exact head can stack
another fence. Recovery reconstructs and authenticates the complete event,
source, plan, projection, redemption and fence history and fails closed on
schema or self-consistent source retarget tamper.

| Evidence | Result |
| --- | --- |
| Plan audit | The narrow plan received independent `APPROVE` before editing; T14 clearance remained deferred to T17 |
| Focused first falsification | Typed contract import failed before implementation; the narrow route made the contract/coordinator test pass |
| Focused T09 suite | 8 tests passed in 1.580 seconds |
| Affected dispatch module | 48 tests passed in 6.715 seconds |
| Complete delivery-control package | 339 tests passed in 30.792 seconds |
| Repository validators | 184 skills valid with zero warnings; 8 script tests passed with 4 expected skips; 91 gate self-test assertions passed; compileall passed; `git diff --check` exit 0 with line-ending notices only |
| Independent implementation review | Initial `REVISE` found one MAJOR future-clearance foreign-key defect; removing only the T09 action-to-live-fence dependency and adding its regression produced final `APPROVE`, no findings; reviewer independently passed 8 focused tests in 1.453 seconds |
| Commit/push and hosted checks | Signed-off commit `9599bcb748f2290f328561704c860f5cb3b9c4c3` pushed to the existing branch; `gate-guard` passed in 7s, `validate-skills` in 1m18s and `windows-offline-checks` in 2m47s on that exact head; PR #99 remained open, draft and blocked |
| Files changed | `contracts.py`, `dispatch.py`, `storage.py`, `test_dispatch.py`, `test_storage.py`, plus status README/backlog/handoff synchronization |
| Intentionally untouched | Canonical design, approval register, BER, dependencies, CI, CLI, adapters, preserved artifacts/caches, real authority/adapters and external systems |

T09 is `YES/YES/YES`. Its crash/replay, slot-retention and uncertainty/fence
persistence tests are narrow evidence for C06, F06 and F21; those complete
families remain `UNVERIFIED`. T17 with F02/F11/F12/F21 is next. PR #99 remains
draft and not merge-ready.

### 5.15 T17 validator-result reconciliation and T09-resume checkpoint

The reviewed T17 slice reconciles one exact ceased validator RESULT from its
immutable observation, cessation, accounting settlement and uncertainty set.
Runtime and recovery share one repository-prefix reducer bounded by the global
writer epoch. It rejects a superseded validator attempt, resolves only the
named uncertainty instances and exact associated fences, and derives the
remaining route from applicable item/effect history. A same-run pause preserves
`PAUSED`; an applicable cross-run pause is a blocker; later history cannot
retroactively alter the recorded route. The typed validation-application cursor
is retained for the still-unapplied result.

The associated versioned T14 route is distinct from legacy `ResumeRequest`.
Its signed request binds the immutable T09 pause and T17 reconciliation sources,
the independently current catalog/run-head vector and current run head. One
transaction clears only the named T09 fence, redeems the one-use operator
capability and advances the run chain. If another same-run T09 fence remains,
the first resume remains `PAUSED`; a later independently signed resume chains
from that new head and may return the eligible result to `VALIDATING`. Historical
reducers replay both exact clearances so a removed fence is not resurrected.

| Evidence | Result |
| --- | --- |
| Focused falsification and correction tests | T17 validator reconciliation, cross-run prefix ordering, T09/T17 stacking, two-stage exact fence clearance, rollback/replay and recovery tamper tests passed |
| Affected dispatch/storage modules | 330 tests passed in 40.735 seconds before the final current-head binding correction; focused two-stage regression passed afterward |
| Complete delivery-control package | 352 tests passed in 41.590 seconds after all corrections |
| Repository validators | 184 skills valid with zero warnings; 8 script tests passed with 4 expected skips; 91 gate self-test assertions passed; compileall passed |
| Diff validation | `git diff --check` exit 0 with Windows line-ending notices only |
| Independent implementation review | First `REVISE` required repository-wide applicable scope and a distinct T14 contract. Second `REVISE` found stranded stacked fences, historical fence resurrection and incomplete recovery rebinding. Current-head signing, PAUSED preservation, both historical reducers and full source bindings closed the findings; final `APPROVE`, no remaining blocker or major |
| Commit/push and hosted checks | Signed-off commit `2bd6112215d78937bb23d694aa933eebf8d417e2` pushed to the existing branch; `gate-guard`, `validate-skills` and `windows-offline-checks` passed on that exact head; PR #99 remained open, draft and blocked |
| Files changed | `contracts.py`, `authority.py`, `dispatch.py`, `engine.py`, `storage.py`, `test_dispatch.py`, `test_storage.py`, plus status README/backlog/handoff synchronization |
| Intentionally untouched | Canonical design, approval register, BER, dependencies, CI, CLI, adapters, preserved artifacts/caches, real authority/adapters and external systems |

This checkpoint accepts only the validator-result T17 route and the exact T09
pause-source T14 route. T17 remains `UNVERIFIED/UNVERIFIED/UNVERIFIED` as a
complete transition: effect-operation uncertainty backfill, the complete T06
uncertainty categories, operation receipt/nonexecution reconciliation and safe
retry remain ordered T17 work. F02, F11, F12 and F21 receive narrow evidence but
remain `UNVERIFIED` as complete families. PR #99 remains draft and not
merge-ready.

### 5.16 T17 operation-uncertainty foundation checkpoint

The reviewed foundation gives operation uncertainty one canonical derivation
used by runtime, semantic migration and recovery. T06 now records distinct
`OUTCOME`, `ACTIVITY` and `SOURCE_CONTROL` instances and records `BILLING` only
when the complete settlement history is genuinely unknown. Effect receipts use
typed, issuer-authenticated source/control classification: `SOURCE_CONTROL` is
created only for authenticated `UNKNOWN`, while known `CONSUMED` or `ADJUSTED`
accounting is never downgraded merely because the incoming receipt omits usage.
The operator pause fence remains separate from these uncertainty fences.

SQLite `PRAGMA user_version=1` is the semantic boundary. Version 0 performs the
reconciliation backfill, exact legacy-operation audit, canonical operation-row
derivation and version advance in one `BEGIN IMMEDIATE` transaction. Version 1
validates the exact row/fence set and never heals deletion or surplus data.
Migration rejects disguised validator-shaped operation rows and verifies every
settlement projection against its immutable event body, hash and scope before
classification. New evidence-bearing receipt history requires the bound issuer
and MAC during recovery; immutable legacy receipt bodies retain their original
digest semantics.

| Evidence | Result |
| --- | --- |
| Plan and independent audit | The narrow T17 foundation plan tied runtime, migration, recovery and the accounting matrix to T06/T10/T17 and F02/F04a/F07/F11/F12/F21; corrected plan received `APPROVE` before editing |
| Cheapest falsification and regressions | Evidence omission, v2 authority/MAC recovery, conditional T06/receipt category matrices, exact legacy migration, atomic rollback, repeated reopen, deletion/surplus/tamper and crash/replay cases passed; the final disguised-row and settlement-projection rollback probes passed 2 tests independently |
| Affected storage/dispatch modules | 342 tests passed in 43.910 seconds after the final migration corrections |
| Complete delivery-control package | 364 tests passed in 44.034 seconds |
| Repository validators | 184 skills valid with zero warnings; 8 script tests passed with 4 expected skips; 91 gate self-test assertions passed; compileall passed |
| Diff validation | `git diff --check` exit 0 with Windows line-ending notices only |
| Independent implementation review | Initial `REVISE` found four MAJOR evidence, recovery-MAC, transaction-boundary and legacy-row-healing gaps. A second `REVISE` found disguised operation rows and unverified settlement projections at migration. Both correction rounds were regression-tested; final `APPROVE`, no remaining blocker or major |
| Files changed | `authority.py`, `contracts.py`, `dispatch.py`, `storage.py`, `test_dispatch.py`, `test_storage.py`, plus status README/backlog/handoff synchronization |
| Intentionally untouched | Canonical design, approval register, BER, dependencies, CI, CLI, adapters, preserved artifacts/caches, real authority/adapters and external systems |

This checkpoint adds narrow evidence to T17 and F02/F04a/F07/F11/F12/F21 but
does not promote any complete family. T17 remains
`UNVERIFIED/UNVERIFIED/UNVERIFIED`: verified-receipt reconciliation,
authoritative nonexecution resolution and authenticated concurrent-safe
same-effect retry remain next in their documented order. PR #99 remains draft
and not merge-ready.

## 6. Handoff contract

A new session verifies role, repository, current branch/head/remote and complete
approval lifecycle before any work. Read design, this register and evidence.
Carry CP-D01–CP-D10 with explicit supersession/deviation records; preserve previous
decisions unless the owner accepts a change. Each stage records changed files,
intentional untouched paths, actual commands and distinctive results, reviewers,
unresolved obligations, authority source and exact next entry criteria.

No self-referential final SHA inside its own commit: final commit/tree, PR URL,
all exact-head check conclusions and owner handoff live in the PR body/final response.
Existing CI logs have finite retention; repository evidence records sanitized
durable summaries and links, not an assertion that raw hosted logs last forever.
After gated owner-approved merge, report its SHA and leave every later package blocked.
