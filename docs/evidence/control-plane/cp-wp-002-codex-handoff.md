# CP-WP-002 Codex continuation handoff

Date: 2026-09-21
Repository: `ModernNomad-98/Project-Aegis` (Role A source library)
Branch: `feat/cp-wp-002-offline-kernel`
Base: `main` at `497a4529b84ec223245e001213271a9266514f62`
Implementation checkpoint: `ba133941a5ae897b6202fa9788b183da28b3f12a`
First handoff checkpoint: `8456a369b64dc3f6ef87e4423a8e877ed0525316`
Latest pushed checkpoint: `ad9b1d149b6c361a72e8650654d395f3114a7f9b`
Draft PR: [#99](https://github.com/ModernNomad-98/Project-Aegis/pull/99)
Status: **IN PROGRESS - NOT MERGE-READY - IMPLEMENTED SLICES AND FILESYSTEM DIFF `APPROVE`; EXACT COMMITTED-HEAD/HOSTED AND FINAL TRACE GATES OPEN**

This is the continuation authority and evidence record for the current
CP-WP-002 work. It does not create authority. The current user instructions,
[approval register](../../approvals/APPROVAL_REGISTER.md), and canonical
[design](../../design/resumable-control-plane-v1.md) remain controlling sources.

## 1. Cold-start preflight

Run these checks before editing:

```powershell
git fetch origin
git switch feat/cp-wp-002-offline-kernel
git pull --ff-only
git rev-parse HEAD
git rev-parse origin/feat/cp-wp-002-offline-kernel
git status --short --untracked-files=normal
gh pr view 99 --repo ModernNomad-98/Project-Aegis --json state,isDraft,headRefName,headRefOid,baseRefName,url,mergeStateStatus,statusCheckRollup
```

The implementation checkpoint is `ba13394`. This handoff is committed after
that checkpoint, so the PR head should be a descendant of `ba13394`, not
necessarily that exact SHA. Stop and reconcile before editing if:

- the checkout is not the Project Aegis source repository;
- the branch or PR differs;
- `ba13394` is not an ancestor of the checked-out head;
- tracked changes are present that PR #99 does not explain; or
- an approval lifecycle event has revoked, expired, consumed or superseded an
  authority listed below.

Expected preserved untracked paths at handoff time:

```text
artifacts/recovery/
artifacts/reviews/
tools/aegis_delivery_control/__pycache__/
tools/aegis_delivery_control/tests/__pycache__/
tools/behavioral_eval_runner/__pycache__/
tools/behavioral_eval_runner/adapters/__pycache__/
tools/behavioral_eval_runner/graders/__pycache__/
tools/behavioral_eval_runner/judge/__pycache__/
tools/behavioral_eval_runner/tests/__pycache__/
```

Stage 5's local validator invocation also generated these untracked cache paths;
they are preserved and must likewise not be staged or deleted:

```text
scripts/__pycache__/
scripts/ci/__pycache__/
scripts/tests/__pycache__/
```

Do not stage, delete, broadly inspect or add ignore rules for the artifact
directories. The cache directories are generated local state and were not added
to the checkpoint. No further cleanup or deletion, including cache removal, is
authorized by this handoff; do not stage or delete them.

## 2. Source precedence

Apply precedence by domain:

- **Authority:** the user's current direct instruction, then the effective
  lifecycle in the approval register. This handoff, design and backlog create no
  authority.
- **Requirements and scope:** current direct scope, the canonical design, then
  the durable backlog. A checkpoint record cannot weaken a canonical acceptance
  requirement.
- **Observed state:** live Git/GitHub state and current code/tests, then this
  handoff's dated evidence, then merged history. Old chat, summaries and memory
  are context only where labeled.

Any contradiction across these domains stops work for explicit source
reconciliation. Do not resolve it merely by selecting whichever source is higher
in a single global list.

Code and passing tests establish current behavior, not acceptance. The design
establishes required behavior, not implementation. A transition registry row is
not proof that the transition has a request, transaction, recovery path or tests.

## 3. Authority and delivery state

No revocation, expiry, consumption or supersession event affecting the grants
below existed in the approval register when this handoff was prepared.

| Authority | Active scope carried forward | Does not authorize |
| --- | --- | --- |
| AEGIS-APR-001 | Read-only Project Aegis agents without repeated approval | Writes or unrelated work |
| AEGIS-APR-002 | Administrator merges for otherwise authorized Project Aegis delivery | Starting unrelated work, changing settings, bypassing substantive readiness |
| AEGIS-APR-003 | Updating Project Aegis pull requests as needed | Unrelated work outside the applicable task |
| AEGIS-APR-004 | CP-WP-002 under `tools/aegis_delivery_control/`; standard-library SQLite, stable OS lock, one outstanding synthetic operation, synthetic authority/adapters, complete T01-T28/C01-C09/F01-F21 tests, package README and backlog updates | BER, dependencies, CI changes, production data, providers/external calls, releases, deployment, kernel Git mutation, artifact changes, credentials, real authority or real adapters |
| Direct user instruction, prior session `fccf4968-b86b-44d4-9371-8ef2ce8fe1ba`, turn 2118 | "implement the exact order, run pre-flight. For each item, plan first, the audit and scrutinize that plan, once that is done, implment. Pre-approve for commit/push/administrative merge. Loop until backlogs are completely cleared" | Waiving scope, validation, independent review, release safety or deployment authorization |
| Current user instruction | Continue the durable backlog in order; commit/push/merge are pre-approved, and repeat correction/review loops until the backlog is complete | Bypassing scope, validation, independent review, readiness gates, release safety or deployment authority |

Delivery state at handoff preparation:

- checkpoint commit `ba13394` is pushed to the branch above;
- first handoff commit `8456a36` is pushed to the same branch;
- PR #99 was updated with both commit identifiers, the linked handoff, local
  validation receipts and all three blocking stop findings;
- a public PR-page read after that update confirmed PR #99 was open and draft,
  listed both commits, and identified `8456a36` as the latest head at that time;
- no CP-WP-002 commit is on `main`;
- on 2026-09-21 the GitHub deployments API returned `[]`;
- on 2026-09-21 `gh release list` returned `no releases found`;
- no software deployment or release occurred; and
- administrator-merge pre-approval is carried forward but must not be exercised
  while the independent gate is `REVISE` or required checks are unresolved.

The commit containing the final audit corrections to this handoff necessarily
cannot self-record its own SHA. Treat PR #99's latest head and check rollup as
the live delivery record and re-query them during cold-start preflight.

## 4. Binding decision register

All canonical decisions remain binding. None was superseded in this checkpoint.

| ID | Binding decision | Source | Status |
| --- | --- | --- | --- |
| CP-D01 | Keep delivery control independent; BER remains unchanged | Design section 3 | Binding |
| CP-D02 | One host/owner and one repository-wide outstanding synthetic operation, guarded atomically and independently of the writer lock | Design section 3 | Binding |
| CP-D03 | Authority and state transitions are deterministic; workers are untrusted | Design section 3 | Binding |
| CP-D04 | Unknown effects do not dispatch; proof-free owner disposition permits only stop, final-fail or report | Design section 3 | Binding |
| CP-D05 | The storage interface and selected crash model govern implementation | Design section 3; AEGIS-APR-004 | Binding |
| CP-D06 | Terminal states never reopen; late evidence settles obligations without advancing lifecycle | Design section 3 | Binding |
| CP-D07 | Imported state requires independent freshness or complete authoritative reconciliation before dispatch | Design section 3 | Binding |
| CP-D08 | Logical-effect deduplication survives item, run, source, plan and policy revisions | Design section 3 | Binding |
| CP-D09 | External one-use grants require trusted-source atomic claim/consume; local reservation is not authority | Design section 3 | Binding |
| CP-D10 | Versioned budget settlements retain actual use and worst-case uncertainty across terminals and restarts | Design section 3 | Binding |
| CP-H01 | T01-T28 are canonical transition identifiers, not separate tasks recreated on each pass | Design transition table | Binding |
| CP-H02 | Every next item follows preflight -> plan -> independent plan audit -> implementation -> focused validation -> independent implementation review | Direct user instruction | Binding |
| CP-H03 | Passing tests do not override an independent `REVISE` verdict | Current checkpoint evidence | Binding |
| CP-H04 | "Removal of the project" is limited to the accidental dashboard identified in the immediately preceding exchange | Current user context and explicit dashboard discussion | Binding; broader deletion forbidden |
| CP-H05 | PR #99 is a recoverable work checkpoint, not a release or deployment | Current user pause instruction | Binding |

## 5. Stage 1 - implementation checkpoint

### Changed files in `ba13394`

Implementation and tests:

- `tools/aegis_delivery_control/adapters.py`
- `tools/aegis_delivery_control/authority.py`
- `tools/aegis_delivery_control/cli.py`
- `tools/aegis_delivery_control/contracts.py`
- `tools/aegis_delivery_control/dispatch.py`
- `tools/aegis_delivery_control/storage.py`
- `tools/aegis_delivery_control/tests/test_dispatch.py`
- `tools/aegis_delivery_control/tests/test_engine.py`
- `tools/aegis_delivery_control/tests/test_platform.py`
- `tools/aegis_delivery_control/tests/test_recovery.py`
- `tools/aegis_delivery_control/tests/test_storage.py`

Status documentation synchronized with the checkpoint:

- `README.md`
- `docs/README.md`
- `docs/roadmaps/resumable-control-plane-backlog.md`
- `tools/aegis_delivery_control/README.md`

The commit contains 19,000 insertions and 2,811 deletions across those 15 files.
It is one accumulated CP-WP-002 checkpoint, not a claim that every included
transition or acceptance family has passed independent review.

### Current implemented surface

- Standard-library Python/SQLite synthetic offline kernel.
- Immutable event history and deterministic projections.
- Repository-global `writer_epoch` historical transaction cutoff.
- One repository-wide outstanding operation slot.
- Synthetic HMAC-bound authority, execution and validation evidence only.
- T01 plan/check registration; mediated T03 dispatch; effect receipt and
  validation-intent/result/application paths; recovery/freshness, accounting,
  slot and fence logic; terminal evidence intake; and broad fault tests.
- Typed T18 graceful and T19 immediate stop requests and persistence, including
  permanent stop fencing, retained cursor/slot obligations, replay/recovery and
  late-evidence interaction tests.

This inventory is descriptive, not an independent acceptance verdict.

### Intentionally not touched

- `docs/design/resumable-control-plane-v1.md`: canonical design unchanged.
- `docs/approvals/APPROVAL_REGISTER.md`: no new grant or lifecycle event created.
- `.github/`, workflows, requirements and dependency files: outside
  AEGIS-APR-004.
- BER code/docs: CP-D01 and AEGIS-APR-004 prohibit this coupling.
- `artifacts/recovery/` and `artifacts/reviews/`: preserved untracked.
- Production data, providers, credentials, external integrations, real authority,
  real execution adapters, releases and deployments: absent and unauthorized.

## 6. Stage 2 - first handoff checkpoint

### Changed files in `8456a36`

- `docs/evidence/control-plane/cp-wp-002-codex-handoff.md`: created the Codex
  continuation record.

### Intentionally not touched

- All kernel source and tests: the user requested pause, not another stop fix.
- Canonical design and approval register: no decision or authority changed.
- Artifact/cache paths and every prohibited AEGIS-APR-004 surface.

### Proven delivery

- `git push` advanced the remote branch from `ba13394` to `8456a36`.
- `gh pr edit 99 ...` returned PR #99's URL after replacing the provisional body
  with the actual handoff link, commit identities, validation and blockers.
- A public PR read confirmed two commits, draft state and head `8456a36` at that
  time. Its latest-head checks were not all terminal yet.

### Open item

Independent review of this first handoff returned `REVISE`; Stage 3 corrects the
specific findings below without resuming kernel implementation.

## 7. Stage 3 - handoff audit corrections

### Changed files

- `docs/evidence/control-plane/cp-wp-002-codex-handoff.md`: corrected precedence,
  remote evidence, stage inventory, cleanup boundaries and T/C/F status mapping.
- `docs/README.md`: changed the incomplete two-grant approval summary to require
  reading the complete grant/lifecycle register.

### Intentionally not touched

- All kernel source/tests and the three unresolved stop findings.
- Canonical design, approval register, BER, CI/dependencies and artifact/cache
  paths.
- PR draft state, merge state, releases and deployments.

### Commit identity

This stage is the commit containing this revised handoff. Its SHA is deliberately
not embedded in itself. The final PR #99 head and a post-push PR record identify
it without a self-referential commit claim.

Independent read-only re-review verdict: `APPROVE`, with no blocker, major,
minor or nit findings. The reviewer confirmed all six first-review findings were
closed and that the three implementation stop defects remain correctly blocking.

### Stage 4 - R-STOP-01 terminal slot closure

The initial implementation plan audit returned `REVISE` because the typed
application source, PASS/FAIL mapping, four T18/T19 predecessor routes, exact
SQLite migration and C05/C09 assertions were underspecified. The corrected plan
received independent `APPROVE` with no findings before any implementation edit.

Changed files:

- `tools/aegis_delivery_control/contracts.py`: added the typed
  `VALIDATION_APPLICATION` T26 source and closed disposition/field validation.
- `tools/aegis_delivery_control/storage.py`: added exact application binding,
  terminal closure, recovery validation and an atomic legacy-table migration.
- `tools/aegis_delivery_control/tests/test_storage.py`: added the four stop/state
  routes, closure/dispatch, crash/replay, migration, accounting, latest-attempt
  and tamper regressions.
- `README.md`, `docs/README.md`,
  `tools/aegis_delivery_control/README.md`, the durable backlog and this handoff:
  synchronized only the observed R-STOP-01 result and remaining blockers.

Intentionally untouched: canonical design, approval register, BER, CI,
dependencies, adapters, artifact/cache paths, real authority/execution surfaces,
releases and deployments. R-STOP-02 and R-STOP-03 received no implementation
change.

The first focused test failed on the unsupported application source, then passed
after the narrow implementation. The storage module passed 168 tests; the full
package passed 209. Independent implementation review returned `APPROVE` with no
blocker, major, minor or nit finding and independently ran nine focused tests.
The accepted trace is limited to the R-STOP-01 slices of T18/T19/T26, C05/C09 and
F06/F09/F14/F18; complete rows/families remain `UNVERIFIED`.

Commit `a60cdd7b0340123a37473bdd8b57887a2b317072` contains this reviewed stage and
is pushed to the existing branch. PR #99 remains open, draft and blocked; all
three hosted checks passed on that exact head.

### Stage 5 - R-STOP-02 graceful-stop escalation

The initial plan audit returned `REVISE`: it required atomic conversion of every
ambiguous reserved obligation, historical-prefix validation, an exact drain
predicate and an honest authority route. The corrected plan received independent
`APPROVE` before editing. It selected the canonical synthetic operator route;
no approved-rule deadline scheduler is implemented or claimed.

Changed files:

- `tools/aegis_delivery_control/contracts.py`: added typed escalation and
  per-reservation settlement requests.
- `tools/aegis_delivery_control/authority.py`: added the synthetic
  `STOP_ESCALATE` operator action.
- `tools/aegis_delivery_control/dispatch.py`: added the coordinator T20 route.
- `tools/aegis_delivery_control/storage.py`: added the atomic escalation,
  ordinary versioned UNKNOWN settlements, event/projection/recovery validation,
  injected UTC deadline check and historical obligation/accounting proof.
- `tools/aegis_delivery_control/tests/test_dispatch.py` and
  `test_storage.py`: added coordinator, deadline, coverage, crash/replay, later
  adjustment/release/restart and self-consistent tamper regressions.
- Root/package routing docs, the durable backlog and this handoff: synchronized
  only observed R-STOP-02 evidence and the remaining R-STOP-03 blocker.

Intentionally untouched: canonical design, approval register, BER, CI,
dependencies, adapters, artifact/cache paths, real authority/execution surfaces,
releases and deployments. R-STOP-03 received no implementation change.

The first focused coordinator test failed because `escalate_stop` did not exist,
then passed after the narrow implementation. The storage module passed 177 tests
and the full package passed 219. The initial implementation review returned
`REVISE` for a self-consistent escalation item-retarget recovery gap. Recovery
now binds item/effect to the exact source stop and accepted plan/run, and the
projection persists item/effect/slot identity. The corrected independent review
returned `APPROVE` with no findings; its 10 focused tests passed and its former
retarget probe failed closed with `StorageIntegrityError`.

The accepted trace is T20's operator route and its C06/C09/F04b slices. Complete
cross-family trace remains as shown below, and R-STOP-03 keeps the aggregate stop
gate at `REVISE`. Commit/push evidence for Stage 5 remains pending until this
reviewed and validated stage is committed.

### Stage 6 - R-STOP-03 post-contact immediate-stop accounting

The initial plan audit returned `REVISE` for underspecified compatibility,
settlement identity, historical predicates and exact-set/crash coverage. A
corrected plan still proposed an infeasible event-envelope schema v2 and returned
`REVISE`; retaining envelope schema 1 with an exact nested uncertainty snapshot
version received `APPROVE` before editing.

Changed files: `storage.py` adds the atomic contact-bound UNKNOWN settlement and
historical recovery proof; `test_storage.py` adds effect/validator, pre-contact,
crash/replay, late-adjustment/restart, tamper and cross-run alias regressions.
Status docs were synchronized only after implementation approval. Contracts,
adapters, canonical design, approval register, BER, CI, dependencies,
artifact/cache paths and real integrations were intentionally untouched.

The first focused test failed with the contacted reservation still `RESERVED`.
After implementation, seven focused tests, 184 storage tests and 226 package tests
passed. Initial implementation review returned `REVISE` because effect resolution
used attempt ID alone; the reviewer reproduced a cross-run/effect alias. The fix
binds repository/run/item/effect/attempt, its regression passes, and corrected
review returned `APPROVE` with no blocker or major finding.

All three stop findings and the aggregate stop gate are now `APPROVE`. This does
not make the PR merge-ready: exact-head T/C/F backlog work and final independent
architecture/security/QA gates remain. Stage 6 was committed and pushed as
`5cd844bb65813efd798e41ab52ff9003ff23366f`; its three hosted checks passed.

### Stage 7 - T13 authority lifecycle intake

The T13 plan required three audit corrections before `APPROVE`: an exact
fact-kind/order table, grant-wide durable authority state, retained unknown
claims, typed supersession, generation-exact correction and deterministic
lifecycle routing. The first focused test failed because the store had no
`record_authority_fact`; the completed route now uses issuer-authenticated
synthetic evidence and one atomic `AUTHORITY_EVALUATED` transition.

Changed files: `contracts.py` adds typed fact/order/request contracts;
`authority.py` signs and verifies bound synthetic lifecycle evidence;
`dispatch.py` exposes the engine-authorized T13 coordinator route; `storage.py`
persists facts, typed supersession graphs, effective generations, fences and
recovery proofs while rechecking every grant consumer/contact; `test_storage.py`
adds 16 focused decision, consumer, crash/replay, recovery and tamper tests.
Canonical design, approvals, BER, CI, dependencies, artifacts/caches and real
authority/adapters were intentionally untouched.

Implementation review initially returned `REVISE` for stacked correction loss,
cross-kind unknown-claim binding and non-graph supersession checks. Subsequent
re-reviews found typed-graph namespacing and exact own-consumption continuation
gaps. Each was corrected and regression-tested. Final review returned `APPROVE`
with no remaining blocker or major and independently passed all 16 focused tests.
The complete package passed 242 tests; skill validation reported 184 valid and
zero warnings; validator self-tests passed 91 assertions; diff-check was clean
apart from line-ending notices.

T13 is `YES/YES/YES`. Only its C08/F03 slices are accepted; complete cross-family
C08/F03 traceability remains `UNVERIFIED`. T13 was committed and pushed as
`7114bc79b0f960d94c8a78b093781268532ebd41`; all three hosted checks passed on
that exact head.

### Stage 8 - T15 immutable binding mismatch

The T15 plan required two `REVISE` audits before `APPROVE`. Corrections added an
explicit source-tree pin rather than overloading revision identity, strict
all-or-none source/item/schema/reducer pins for every new acceptance, complete
semantic-plan and policy identities, issuer-authenticated current-head
observations, exact SOURCE/ITEM/PLAN/POLICY mapping, store-owned fence identity,
an atomic legacy-schema migration and narrow F01 non-mutation boundaries. The
first focused tests proved the prior gaps: unpinned plans were accepted and the
store had no typed `record_binding_mismatch` route.

Changed production files: `contracts.py` adds typed mismatch kinds/requests and
the four acceptance pins; `authority.py` signs and verifies exact synthetic
observations; `dispatch.py` exposes the engine-authorized T15 route; `storage.py`
adds compatible plan migration, semantic/policy derivation, atomic mismatch
persistence/fencing/routing and historical recovery. `test_storage.py`,
`test_dispatch.py` and `test_recovery.py` provide pinned synthetic builders and
14 focused acceptance, mapping, migration, crash/replay, lifecycle, F01-boundary,
recovery and tamper tests. The three status READMEs, backlog and this handoff are
the only documentation changes. Canonical design, approvals, BER, CI,
dependencies, artifacts/caches and real authority/adapters were intentionally
untouched.

Initial implementation review returned `REVISE`: a BLOCKED/FINALIZING run that
still owned the repository slot was incorrectly treated as idle. Routing now
derives active/uncertain status transactionally from the historical prefix and
obligation-bearing cursor, persists it, and recomputes it during recovery. The
reviewer's exact reproduction now enters `RECONCILIATION_REQUIRED` while
retaining cursor and slot; corrected review returned `APPROVE` with no remaining
blocker or major and independently passed all 14 focused tests.

The complete package passed 256 tests; skill validation reported 184 valid and
zero warnings; validator self-tests passed 91 assertions; diff-check was clean
apart from line-ending notices. T15 is `YES/YES/YES`. Its narrow F01 controls
prove that mismatch handling does not change the effect identity/descriptor,
accepted plan/revision, outstanding slot or accounting projections and cannot
re-enable readiness. Full F01 remains `UNVERIFIED` for T28. The reviewed stage
was committed with DCO sign-off and pushed as
`2de362612f43c125829ff8c73e22bcdcfa6147c0`; `gate-guard`, `validate-skills` and
`windows-offline-checks` passed on that exact head. PR #99 remained open, draft
and blocked as intended.

### Stage 9 - T14 pause-source resume slice

The T14 plan required two `REVISE` audits before `APPROVE`. The corrected plan
bound resume to the exact durable pause source and complete current run-head
vector, required full signed capability/request evidence, derived routing from
the historical prefix, cleared only the source pause fence and preserved every
other blocker, slot and accounting fact. It also selected a compatibility-safe
legacy projection migration and explicitly deferred the public clean-VALIDATING
integration to the ordered T08 work rather than fabricating T08 history.

Changed production files: `contracts.py` adds the typed `ResumeRequest` and
history-derived optional pause cursor; `authority.py` signs/verifies exact
synthetic resume evidence and supports the RESUME operator action; `dispatch.py`
adds the engine-authorized coordinator route; `storage.py` adds exact schema and
legacy migration, atomic persistence/fence clearance, blocker routing, replay,
full-prefix recovery and projection verification. `test_storage.py` and
`test_dispatch.py` provide 21 focused contract, evidence, routing, migration,
crash/replay, recovery and self-consistent-tamper tests. The status READMEs,
durable backlog and this handoff are the only documentation changes. Canonical
design, approval register, BER, dependencies, CI, CLI, artifacts/caches and real
authority/adapters were intentionally untouched.

The first implementation review returned `REVISE` with four MAJOR findings and
no blocker: recovery accepted surplus resume fields, reconstructed a non-null
cursor from the wrong field, disagreed with true pre-T14 cursor migration and
treated an unrelated run's active validator as owned activity. Exact resume
schema/type/nested-shape validation, resume-specific cursor replay, shared legacy
prefix derivation with transactional rollback and run-scoped validator history
closed those findings. Corrected review returned `APPROVE` with no remaining
blocker or major and independently passed all 21 focused tests.

The focused T14 slice passed 21 tests in 0.957 seconds; the affected storage and
dispatch modules passed 255 tests in 21.039 seconds; the complete package passed
277 tests in 22.194 seconds. Reviewer-focused validation passed 21 tests in
0.982 seconds; skill validation reported 184 valid with zero warnings; validator
self-tests passed 91 assertions; and diff-check was clean apart from line-ending notices. T14
remains `UNVERIFIED/UNVERIFIED/UNVERIFIED` as a complete transition because the
exact public-path clean VALIDATING route depends on T08. C06/C07 and
F03/F05/F06/F12/F14/F21 also remain `UNVERIFIED`; only their narrow interactions
with this reviewed slice were exercised. The reviewed implementation was
committed with DCO sign-off and pushed as
`c3c94bf3d367380d1ff60835fb72cb300e69c3e4`. On that exact head, `gate-guard`
passed in 3 seconds, `validate-skills` in 1m18s and `windows-offline-checks` in
3m23s. PR #99 remained open, draft and blocked as intended.

### Stage 10 - T05 local-execution pause

The exact cold-start preflight matched at `52e73db`: local, remote and PR heads
agreed; `ba13394` remained an ancestor; PR #99 was open, draft and blocked;
tracked state was clean; preserved untracked paths matched; and no applicable
approval was revoked, expired, consumed or superseded.

The initial plan audit returned `REVISE` with three MAJOR findings. The corrected
plan accepts both committed-intent/pre-launch and launched/pre-contact RUNNING
histories, persists the complete signed operator capability, uses a closed
`LOCAL_EXECUTION` discriminator distinct from T04 and binds the exact intent,
attempt and slot generation. Re-audit returned `APPROVE` before edits.

TDD first established missing typed-contract, state-owner and coordinator
routes. The implementation now atomically records `PAUSE_REQUESTED`, an
item/effect fence, full operator evidence/redemption and RUNNING to PAUSING while
retaining the outstanding attempt, permission use, reservation, launch and
cursor. Contacted attempts deny to T06. The request-only synthetic path performs
no cancellation/drain contact and makes no child-cessation inference.

The initial implementation review returned `REVISE` for one MAJOR: a
self-consistently rehashed retained cursor was not bound to the historical
predecessor. Ordered replay now compares both predecessor lifecycle and cursor
before applying T05; its tamper regression fails closed. Final independent
review returned `APPROVE` with no remaining blocker or major.

Reviewed code commit `13bda54b9bc63e962a3900ac16640fd2bb18d304` is
DCO-signed and pushed. Its 17 focused tests, 272 affected storage/dispatch tests,
294 complete package tests, 184-skill validator and 91 validator self-test
assertions passed. Exact-head hosted checks passed: `gate-guard` 4s,
`validate-skills` 1m18s and `windows-offline-checks` 3m22s. PR #99 remained
open, draft and blocked. T05 is `YES/YES/YES`; the narrower C06/F06 evidence does
not promote those complete families. T06 is next.

### Stage 11 - T06 contacted external-mutation pause

The approved T06 route begins only after the exact `EFFECT` adapter contact is
durably claimed and before a control-plane receipt is recorded. Bare contact is
bounded uncertainty, not trustworthy proof that the mutation remains active or
drainable. `PauseExternalMutationRequest` therefore binds the exact intent,
operation launch, adapter contact, canonical target digest and slot generation,
and the implemented route advances `RUNNING` directly to
`RECONCILIATION_REQUIRED` rather than inventing an ordinary PAUSING state.

The same atomic transaction writes a normal versioned
`UNKNOWN_WORST_CASE_CHARGED` settlement at W for a still-reserved attempt, then
records the closed `EXTERNAL_MUTATION` pause event, item/effect fence, complete
signed operator evidence/redemption and command outcome. Existing accounting is
retained only by exact prefix-head reference. The outstanding slot, effect key,
intent/launch/contact evidence and cursor remain. No adapter observe, cancel,
rollback, retry, cessation inference or new mutation occurs. A later known or
unknown receipt uses T23 from reconciliation, adjusts or retains the charge
without reopening dispatch and preserves the fence/slot.

The initial plan audit returned `REVISE` because it treated lost-receipt contact
as ordinary PAUSING, omitted mandatory worst-case accounting and routed the
later receipt through T10. The corrected plan received `APPROVE`. The initial
implementation review then found two MAJOR recovery gaps: incomplete contact
body/order verification and a retained-settlement snapshot that was not derived
from the historical prefix. Recovery now round-trips the full contact body,
checks strict pre-pause order and derives the exact pre-transaction settlement
head/disposition. Full self-consistent contact-retarget and settlement-head-
retarget regressions fail closed. Final independent review returned `APPROVE`
with no remaining blocker/major and independently passed 14 focused tests.

Reviewed code commit `39b3268adc984e3d0b10e55a42fe37a172229e60`
is DCO-signed and pushed. Local evidence is 14 focused T06 tests, 285 affected
storage/dispatch tests, 307 complete package tests, 184 valid skills with zero
warnings, 91 validator self-test assertions, compileall and clean diff checks.
Exact-head hosted checks passed: `gate-guard` in 7s, `validate-skills` in 1m20s
and `windows-offline-checks` in 2m49s. PR #99 remains open, draft and blocked.
T06 is `YES/YES/YES`; narrow C03/C06/F06/F07/F08 evidence does not promote
those complete families. T07 is next.

### Stage 12 - T07 local nonexecution settlement slice

The T07 plan required three `REVISE` audits before `APPROVE`. Corrections
removed any invented operator-authority cessation proof, included the prior
T25/T17/T14 interaction matrix, separated the new activity settlement from
legacy T04 projections and preserved the signed bytes of historical
`ResumeRequest` records by using a distinct versioned T14 activity route.

Changed production files: `contracts.py` adds typed T07 settlement and activity
resume requests; `authority.py` signs/verifies the distinct resume evidence;
`dispatch.py` exposes the coordinator routes; `storage.py` adds closed schemas,
atomic event/projection transactions, exact T05/T25/slot/fence binding,
BLOCKED-only activity resume and historical recovery. `test_storage.py` and
`test_dispatch.py` add contract/coordinator, crash/replay, accounting, late
receipt, tamper, recovery and resume regressions. Status READMEs, the durable
backlog and this handoff are the only documentation changes.

The accepted slice requires the exact T05 local pause and the same
reservation's latest authoritative T25 `NONDISPATCH_PROVEN` settlement:
`RELEASED`, zero liability, all obligations settled, no uncertainty or
contradiction and no slot release. T07 atomically records a distinct
`ACTIVITY_SETTLEMENT` `PAUSE_SETTLED`, advances `PAUSING -> PAUSED`, and retains
the pause fence, outstanding slot, accounting head and operation-recovery
cursor. The separate T14 activity route clears only that pause fence and moves
to `BLOCKED`, retaining the cursor, slot and every unrelated blocker/fence.

Initial implementation review returned `REVISE` with two MAJOR findings.
Recovery incorrectly required the T07 journal predecessor to equal the T25
settlement hash, rejecting a valid intervening non-accounting event; T14 also
hardcoded slot generation 1. Recovery now independently derives the latest
pre-T07 reservation settlement, while normal event-chain verification governs
the journal predecessor. Runtime and recovery share an exact T07
event/projection generation binding. A real intervening T13
`SOURCE_UNAVAILABLE/UNKNOWN` regression retains both fences and survives
verified reload; a non-1 generation regression prevents reintroduction of the
constant. Corrected independent review returned `APPROVE` with no remaining
blocker or major and independently passed the three correction tests.

Local evidence is 296 affected storage/dispatch tests, 318 complete package
tests, 184 valid skills with zero warnings, 8 script tests with 4 expected
skips, 91 gate self-test assertions, compileall and clean diff checks apart from
line-ending notices. Commit,
push and exact-head hosted-check evidence remain pending until this reviewed
stage is committed. Canonical design, approval register, BER, dependencies, CI,
CLI, adapters, artifact/cache paths, real authority/adapters and external
systems were intentionally untouched.

T07 remains `UNVERIFIED/UNVERIFIED/UNVERIFIED` as a complete transition because
this checkpoint establishes only the T05-local/T25-authoritative nonexecution
source. T08, T24 and other source families remain outstanding; full T14 also
remains `UNVERIFIED`. Narrow C06/F06/F12 interactions do not promote those
complete families. T08 is next and PR #99 remains open, draft and blocked.

### Stage 13 - T08 validation-pause checkpoint

The T08 plan initially received `REVISE` for three checkpoint, cessation and
race-definition gaps. The corrected plan received independent `APPROVE` before
editing. It required one exact runtime/recovery/T14 checkpoint, authoritative
cessation for the settled-result PAUSED route, reconciliation for unresolved
work, atomic worst-case accounting after contact, and deterministic contact and
result-intake races.

Changed production files: `contracts.py` adds the distinct typed
`PauseValidationRequest`; `dispatch.py` exposes the engine-authorized route;
`storage.py` adds closed pause events/projections, shared checkpoint derivation,
atomic state/fence/accounting writes, T14 integration, verified recovery and
writer-serialized verifier reads. `test_dispatch.py` adds 13 contract,
coordinator, crash/replay, accounting, cessation, tamper, recovery and race
tests; `test_storage.py` updates the closed table inventory. Status READMEs, the
durable backlog and this handoff are the only documentation changes.

`IDLE`, or an exact RESULT observation with known accounting and authoritative
cessation after observation, enters `PAUSED`. Uncontacted unresolved work keeps
RESERVED accounting; contacted unresolved work atomically records one
`UNKNOWN_WORST_CASE_CHARGED` settlement. Both unresolved forms enter
`RECONCILIATION_REQUIRED`. All routes retain the repository slot, validation
cursor and result-application obligation. No adapter observe/cancel/retry call
occurs. T14 accepts only the exact clean T08 PAUSED source, clears only that
fence and returns to `VALIDATING`.

Initial implementation review returned `REVISE` with two MAJOR findings: the
eligible-result predicate permitted zero cessation records, and deterministic
pause/contact plus pause/result races were absent. The shared predicate now
requires exactly one matching authoritative cessation ordered after the RESULT
observation. Both races use a fail-closed retry around writer-serialized
verified reads and prove one slot, fence, observation and settlement. Corrected
independent review returned `APPROVE` with no remaining blocker or major and
independently passed all 13 focused tests in 2.479 seconds.

Local evidence is 13 focused tests in 2.536 seconds, three repeated passes of
the two race tests, 40 dispatch tests, 331 complete package tests, 184 valid
skills with zero warnings, 8 script tests with 4 expected skips, 91 gate
self-test assertions, compileall and clean diff checks apart from line-ending
notices. Reviewed code was committed with DCO sign-off and pushed as
`a0d27bbdd64d7d86bf080355ca933d28760244ab`. On that exact head,
`gate-guard` passed in 5 seconds, `validate-skills` in 1m19s and
`windows-offline-checks` in 2m58s. PR #99 remained open, draft and blocked.
Canonical design, approval register, BER,
dependencies, CI, CLI, adapters, preserved artifact/cache paths, real
authority/adapters and external systems were intentionally untouched. The
validator run added `scripts/ci/__pycache__/` to the preserved untracked cache
set; it was neither deleted nor staged.

T08 remains `UNVERIFIED/UNVERIFIED/UNVERIFIED` as a complete transition because
active drain/cancel and broader T17/T24 cessation sources remain ordered work.
The clean VALIDATING T14 slice is independently accepted, but complete T14 and
the implicated C/F families remain `UNVERIFIED`. T09 is next and PR #99 remains
open, draft and blocked.

### Stage 14 - T09 reconciliation-required pause fence

The T09 plan bound one typed, signed, one-use PAUSE request to the exact current
`RECONCILIATION_REQUIRED` source event, accepted plan and preserved cursor. It
received independent `APPROVE` before editing. The plan deliberately kept T14
fence clearance with later T17 and allowed T09 itself to become
`YES/YES/YES` without promoting the complete C06, F06 or F21 families.

Changed production files: `contracts.py` adds `PauseReconciliationRequest`;
`dispatch.py` adds the engine-authorized coordinator route; `storage.py` adds the
closed event/projection schema, atomic writer-serialized transition, historical
activity reconstruction and strict recovery. `test_dispatch.py` adds 8 typed
contract, exact-head, stacked-fence, no-adapter, crash/replay, tamper, recovery,
race and future-clearance tests; `test_storage.py` updates the closed table
inventory. Status READMEs, the durable backlog and this handoff are the only
documentation changes.

The transaction authenticates and redeems the PAUSE capability, appends
`PAUSE_FENCE_RECORDED`, inserts its fence and immutable action projection and
advances the run and catalog heads. It does not change lifecycle, cursor,
accounting, outstanding-slot ownership, prior evidence or prior fences and does
not call an adapter. Replay is idempotent, stale-source commands fail closed and
a command deliberately rebound to the new exact head may stack another fence.

Initial implementation review returned `REVISE` with one MAJOR finding: the new
immutable action projection foreign-keyed its live fence and would prevent later
T17/T14 exact fence clearance from preserving history. The correction removed
only that T09 dependency, restored the pre-existing external-pause constraint
unchanged and added a foreign-key-enabled deletion/retention regression.
Corrected independent review returned `APPROVE` with no findings and passed all
8 focused tests in 1.453 seconds.

Local evidence is 8 focused tests in 1.580 seconds, 48 dispatch tests in 6.715
seconds, 339 complete package tests in 30.792 seconds, 184 valid skills with zero
warnings, 8 script tests with 4 expected skips, 91 gate self-test assertions,
compileall and clean diff checks apart from line-ending notices. Reviewed code
was committed with DCO sign-off and pushed as
`9599bcb748f2290f328561704c860f5cb3b9c4c3`. On that exact head, `gate-guard`
passed in 7 seconds, `validate-skills` in 1m18s and `windows-offline-checks` in
2m47s. Live PR #99 remained open, draft and blocked at that exact head.
Canonical design, approval register, BER, dependencies, CI, CLI,
adapters, preserved artifact/cache paths, real authority/adapters and external
systems were intentionally untouched.

T09 is `YES/YES/YES`. Its narrow C06 crash/replay, F06 slot-retention and F21
uncertainty/fence-persistence evidence does not promote those complete families,
which remain `UNVERIFIED`. T17 with F02/F11/F12/F21 is next; PR #99 remains open,
draft and blocked.

### Stage 15 - T17 validator-result reconciliation and exact T09 resume

The reviewed slice binds validator reconciliation to one immutable RESULT
observation, authoritative cessation, versioned accounting settlement, exact
uncertainty set, accepted plan, repository slot and unsuperseded validator
attempt. Runtime and recovery use the same repository-prefix reducer bounded by
global `writer_epoch` plus sequence. The reducer resolves only the named
uncertainty instances and their exact fences, ignores later history, preserves
a same-run pause, treats an applicable cross-run pause as a blocker and retains
the typed validation-application cursor for the unapplied result.

The paired T14 route uses a distinct versioned
`ReconciliationPauseResumeRequest` and domain-separated issuer evidence instead
of broadening legacy resume semantics. It independently binds the immutable T09
pause and T17 reconciliation sources, complete catalog/run-head vector and
current run head. One transaction clears exactly the named T09 fence, redeems
the one-use RESUME capability, records the closed event/action projections and
advances both heads. Two stacked T09 fences clear sequentially: the first resume
remains `PAUSED`, the second chains from the first resume head and returns the
eligible result to `VALIDATING`. Both historical reducers replay the exact
clearances, so later routing and recovery do not resurrect a deleted fence.

Changed production files: `contracts.py`, `authority.py`, `dispatch.py`,
`engine.py` and `storage.py`. `test_dispatch.py` covers validator settlement,
repository-prefix ordering, cross-run before/after boundaries, two-stage T09
clearance, crash rollback/replay and semantic tamper; `test_storage.py` updates
the exact closed table inventory and preserves T06 uncertainty regressions.
Root/package routing docs, the durable backlog and this handoff record only the
observed slice. Canonical design, approval register, BER, dependencies, CI, CLI,
adapters, artifact/cache contents, real authority/adapters and external systems
remain intentionally untouched.

Independent review returned two `REVISE` verdicts before final acceptance. The
first required repository-wide applicable item/effect scope and a distinct T14
contract rather than inferred legacy resume behavior. The second found that a
second stacked T09 fence would be stranded, the historical reducers would
resurrect a cleared fence, and recovery incompletely rebound the T09 source.
Signed current-head binding, `PAUSED` preservation, exact clearance replay and
full repository/run/item/effect/plan/revision source binding closed every
finding. Final independent verdict: `APPROVE`, with no remaining blocker or
major.

Focused regressions passed after each correction. The affected dispatch/storage
modules passed 330 tests before the final current-head correction, and the full
delivery-control package passed 352 tests in 41.590 seconds afterward.
Repository validation found 184 valid skills with zero warnings, 8 script tests
passed with 4 expected skips, all 91 gate self-test assertions passed and
compileall passed. `git diff --check` exited 0 with Windows line-ending notices
only. Signed-off commit `2bd6112215d78937bb23d694aa933eebf8d417e2`
was pushed to the existing branch; PR #99 remained open, draft and blocked, and
`gate-guard`, `validate-skills` and `windows-offline-checks` all passed on that
exact head.

This stage accepts only the validator-result T17 route and the exact T09-source
T14 route. Complete T17 remains `UNVERIFIED/UNVERIFIED/UNVERIFIED`: effect
operation uncertainty backfill, complete T06 uncertainty categories,
receipt/nonexecution reconciliation and authenticated safe retry remain ordered
T17 work. F02, F11, F12 and F21 gain narrow evidence but remain `UNVERIFIED` as
complete families. PR #99 remains open, draft and blocked.

### Stage 16 - T17 operation-uncertainty foundation

The reviewed foundation introduces one closed operation-uncertainty derivation
shared by T06 runtime, receipt intake, semantic migration and recovery. T06
always creates distinct `OUTCOME`, `ACTIVITY` and `SOURCE_CONTROL` instances and
adds `BILLING` only when the complete accounting history is unknown. Receipt
intake carries a typed, domain-separated issuer MAC over the exact
repository/run/item/effect/attempt, claim, receipt, payload, usage and
`KNOWN`/`UNKNOWN` classification. `SOURCE_CONTROL` exists only for authenticated
`UNKNOWN`; missing receipt telemetry cannot downgrade an already authoritative
`CONSUMED` or `ADJUSTED` settlement.

`PRAGMA user_version=1` now marks the semantic projection boundary. Version 0
performs reconciliation backfill, the complete legacy operation-origin audit,
canonical row/fence insertion, foreign-key validation and the version advance
inside one `BEGIN IMMEDIATE`. It rejects malformed or disguised operation rows
regardless of their claimed `check_id`, and verifies settlement projection
fields against immutable event body/hash plus reservation and event scope before
derivation. Version 1 validates exact rows and fences and never recreates a
deleted row. Evidence-bearing v2 observations require the bound issuer and MAC
during recovery; immutable legacy observations preserve their v1 digest shape.

The narrow plan received independent `APPROVE` before editing. The first
implementation review returned `REVISE` for four MAJOR gaps: evidence-free new
writes, optional recovery MAC verification, a split semantic transaction and
legacy-row healing. After correction, a second `REVISE` found a disguised
validator-shaped operation-row escape and pre-verification use of settlement
projection classifications. Exact-set expansion, immutable settlement binding
and two rollback regressions closed those findings. Final independent verdict:
`APPROVE`, with no remaining blocker or major; the reviewer independently passed
the two final migration regressions.

Changed production files are `authority.py`, `contracts.py`, `dispatch.py` and
`storage.py`; `test_dispatch.py` and `test_storage.py` add the category matrix,
typed-evidence, migration, exact-set, crash/replay and tamper coverage. Status
READMEs, the durable backlog and this handoff record only observed evidence.
Canonical design, approval register, BER, dependencies, CI, CLI, adapters,
preserved artifact/cache contents, real authority/adapters and external systems
remain intentionally untouched.

The affected storage/dispatch modules passed 342 tests in 43.910 seconds. The
complete delivery-control package passed 364 tests in 44.034 seconds. Repository
validation found 184 valid skills with zero warnings, 8 script tests passed with
4 expected skips, all 91 gate self-test assertions passed, compileall passed and
`git diff --check` exited 0 with Windows line-ending notices only. This commit
cannot self-identify its final SHA; the exact delivery head, push result, live PR
status and hosted-check conclusions belong in PR #99 and the final response as
required by the handoff contract below.

This foundation adds narrow evidence to T17 and F02/F04a/F07/F11/F12/F21 but
does not promote any complete family. T17 remains
`UNVERIFIED/UNVERIFIED/UNVERIFIED`; verified-receipt reconciliation,
authoritative nonexecution resolution and authenticated concurrent-safe
same-effect retry remain next in the canonical order. PR #99 remains open,
draft and blocked.

### Stage 17 - T17 verified-receipt reconciliation

The reviewed `VERIFIED_RECEIPT` slice binds one durable effect receipt to the
accepted plan/revision, exact repository slot and current catalog/run heads. Its
synthetic read-only lookup evidence is a domain-separated MAC over a canonical
timezone-aware query time, governed query-after event ID/hash, derived source
identity, response ID/digest, mandatory `KNOWN` result and sorted exact prior
`SOURCE_CONTROL` bindings. Runtime and recovery derive the expected source,
response and ordering from immutable receipt and uncertainty history rather
than trusting caller labels.

The request must name every applicable unresolved operation uncertainty for the
same repository/run/item/effect/attempt. Each billing resolution proves the full
settlement ancestry from its recorded uncertain head to the current
authoritative `CONSUMED` or `ADJUSTED` head. A single transaction records the
event, action, exact resolutions and command outcome, deletes only the covered
uncertainty fences and advances the run/catalog heads. The server-derived
`operation-validation:v1` cursor routes an uncovered reconciliation obligation
to `RECONCILIATION_REQUIRED`, a retained same-run pause to `PAUSED`, other
recovery/finalization blockers to `BLOCKED`, and a clean prefix to
`VALIDATING`. Exact replay follows request/evidence and projection-integrity
verification but precedes mutable freshness, head, lifecycle, slot and
uncertainty guards.

Semantic version 2 adds a distinct exact
`verified_receipt_reconciliation_actions` projection. The v1-to-v2 migration
does not rewrite validator reconciliation events, hashes or rows; missing,
partial or incompatible v2 state fails closed. Reopen recognizes only exact
verified-receipt event/action/resolution pairs before excluding their cleared
fences, and complete recovery re-verifies the lookup MAC, order, settlement
ancestry, route and exact projections.

The initial implementation review returned `REVISE` for two MAJOR gaps: the
lookup proof lacked explicit query/time/source/response/result bindings, and
exact replay followed the mutable freshness gate. The closed typed lookup
envelope, derived order/source/response checks and replay reordering corrected
both. Final independent verdict: `APPROVE`, no remaining blocker or major; the
reviewer independently passed the three core focused tests.

Changed production files are `authority.py`, `contracts.py`, `dispatch.py` and
`storage.py`; `test_dispatch.py` and `test_storage.py` add schema inventory,
migration, typed-evidence, settlement-ancestry, routing, denial, crash/replay,
reopen and tamper coverage. Status READMEs, the durable backlog and this handoff
record only observed evidence. Canonical design, approval register, BER,
dependencies, CI, CLI, adapters, preserved artifact/cache contents, real
authority/adapters and external systems remain intentionally untouched.

The complete delivery-control package passed 368 tests in 45.506 seconds.
Repository validation found 184 valid skills with zero warnings, 8 script tests
passed with 4 expected skips, all 91 gate self-test assertions passed,
compileall passed and `git diff --check` exited 0 with Windows line-ending
notices only.

This stage adds narrow evidence to T17, C03/C04/C06 and
F02/F04a/F07/F11/F12/F21 without promoting any complete family. T17 remains
`UNVERIFIED/UNVERIFIED/UNVERIFIED`; authoritative `PROVEN_NONEXECUTION` is next,
then authenticated concurrent-safe `SAFE_SAME_EFFECT_RETRY`. The existing
validator-only T09-after-T17 T14 projection is intentionally unchanged, so
operation-sourced T14 clearance remains deferred. PR #99 remains open, draft
and blocked.

### Stage 18 - T17 authoritative nonexecution and safe retry

The reviewed slice closes the remaining ordered T17 implementation work for
synthetic operation nonexecution. T25 requires an issuer-authenticated canonical
target-ledger seal for every `INTENT_ONLY`, `LAUNCHED` or `CONTACTED` operation
routed to recovery. It records the exact action, clears only proof-prefix
uncertainty instances and retains newer or independent fences. The typed T14
route clears only its exact pause and remains PAUSED under another prefix-active
pause. T16 records a one-use recovery authorization; the exact successor T03
intent atomically consumes it and transfers the repository slot to generation 2.

Recovered generation and authorization binding propagate through operation
launch/contact, T10/T23, T27 validator intent/contact, T11/T12, T16 and T26.
Pre-commit rollback and post-commit acknowledgement-loss replay are exact;
generation/authorization substitution fails closed; ordinary generation-1
event shapes remain unchanged. A stopped contacted retry retains its slot until
the missing authoritative effect outcome is settled.

The initial implementation review returned `REVISE` for three findings: the
generation-2 path stopped at operation contact, INTENT_ONLY T25 recovery lacked
its canonical action/seal, and T14 replay counted cleared historical pauses as
active. After those corrections, two migration-only BLOCKERs were found and
closed. Terminal-settlement migration now recognizes both committed generation-1
schemas and preserves populated rows and foreign keys. V2-to-v3 T25 backfill now
uses the exact proof-event prefix, preserves newer uncertainty/fences and
atomically rejects incompatible later resolution ownership. Final independent
verdict: `APPROVE`, no remaining blocker or major; the reviewer independently
passed both migration probes.

Changed production files are `authority.py`, `contracts.py`, `dispatch.py` and
`storage.py`; `test_dispatch.py` and `test_storage.py` add typed routes,
generation propagation, all-path seal, stacked-pause, crash/replay, restart,
tamper, compatibility and migration coverage. Status READMEs, the durable
backlog and this handoff record observed evidence. Canonical design, approval
register, BER, dependencies, CI, CLI, adapters, preserved artifact/cache
contents, real authority/adapters and external systems remain intentionally
untouched.

The storage module passed 279 tests in 32.924 seconds and the complete
delivery-control package passed 373 tests in 47.700 seconds. Repository
validation found 184 valid skills with zero warnings, 8 script tests passed with
4 expected skips, all 91 gate self-test assertions passed and compileall passed.
Signed-off commit `a6b2d8624400d7af3be2cb309db01864d6e8e472`
was pushed to the existing branch. On that exact head, `gate-guard` passed in 5
seconds, `validate-skills` in 1m7s and `windows-offline-checks` in 3m1s. PR #99
remained open, draft and blocked.

This stage adds accepted slice evidence to T14/T16/T17/T25 and generation-aware
T10/T11/T12/T23/T26/T27 behavior, plus C03/C04/C06 and
F02/F04a/F06/F07/F11/F12/F19/F21. Complete T/C/F families remain conservatively
`UNVERIFIED` pending an accumulated exact-head audit. The succeeding T22
checkpoint is recorded below. PR #99 remains open, draft and blocked.

### 7.19 T22 terminal restart reporting

T22 now exposes a typed, non-authorizing restart/resume report for terminal
`COMPLETED`, `FAILED_FINAL` and `STOPPED` runs. A dedicated read facade opens
only existing main and auxiliary SQLite ledgers with URI `mode=ro` and
`query_only`. It creates no state directory or writer lock and performs no
initialization, migration, backfill, repair or hot-journal recovery. Trusted
synthetic authority is injected independently of stored fingerprints. The
reader verifies the complete local history/projections, derives the unique
terminal-entry event server-side and invokes the T22 same-state engine guard
only when independent complete-vector freshness and optional caller anchors
also match.

Verification and request disposition are separate. Current nonterminal state is
reported as `NONTERMINAL` without evaluating ordinary dispatch guards. Locally
intact but stale/unavailable freshness is explicitly non-authorizing with
dispatch closed. Integrity, schema or trusted-verifier failure returns an
unverified, dispatch-closed report and no authoritative terminal-event claim.
Caller anchors are assertions, not freshness proof. T22 never appends an event,
consumes authority, clears a fence, changes lifecycle, resets budget/caps or
releases a slot. T23/T26 remain separate guarded routes and are not authorized
by the report.

The plan required three correction rounds before independent `APPROVE`: local
integrity had to remain reportable without freshness; the path had to be truly
read-only rather than using state-owner initialization; and verification,
caller matching, restart denial and global dispatch posture had to be orthogonal.
The first implementation review returned `REVISE` for two MAJOR findings. A
proven-nonexecution recovery audit still opened its auxiliary target ledger with
a write-capable handle, and valid JSON with a non-object shape could escape the
typed failure result. Shared read-only auxiliary connections, a non-inheriting
read facade and verifier-boundary structural exception normalization closed both.
Corrected independent review returned `APPROVE`, no remaining blocker or major,
and independently passed all 11 focused tests.

Changed production files are `contracts.py`, `dispatch.py` and `storage.py`;
`test_storage.py` covers all terminal states, verified nonterminal status,
stale/raising freshness, mismatched anchors/authority, missing/corrupt/legacy
state, retained accounting/slot, repeated reads, concurrent writer snapshots,
non-object event bodies and byte-preserving main/auxiliary proof reads. Status
READMEs, the durable backlog and this handoff record the evidence. Canonical
design, approval register, BER, dependencies, CI, CLI, adapters, preserved
artifact/cache contents, real authority/adapters and external systems remain
intentionally untouched.

The complete delivery-control package passed 384 tests in 53.243 seconds after
review corrections. Repository validation found 184 valid skills with zero
warnings, 8 script tests passed with 4 expected skips, all 91 gate self-test
assertions passed, compileall passed and `git diff --check` exited 0 with Windows
line-ending notices only. Signed implementation commit
`39ad374a172122c14d06070f65c1e033da3b5c83` was pushed to the existing branch;
exact-head hosted checks passed (`gate-guard` in 4s, `validate-skills` in 1m24s
and `windows-offline-checks` in 2m14s). Local and remote heads matched, `ba13394`
remained an ancestor and live PR #99 remained open, draft and blocked.

T22 is implemented, tested and independently accepted. C07 and F04b receive
narrow accepted evidence but remain conservatively `UNVERIFIED` as complete
families. The succeeding T28/F01 checkpoint is recorded below. PR #99 remains
open, draft and blocked.

### 7.20 T28 verified-effect adoption and F01 identity

T28 now adopts a fully settled completed effect into a new accepted plan and
validation-check set without contacting an execution adapter, repeating the
effect, reusing validation results or charging it again. One dedicated synthetic
adoption grant is consumed exactly once. The signed adoption identity binds the
root attempt/observation/finalization, immediate execution-or-adoption edge,
current check-set digest, accepted plan/effect and source ID/version/terms/scope.
Readiness, source use, slot ownership, origin and transitive dependency edges are
committed atomically and replayed from immutable history.

F01 now persists canonical effect definitions plus explicitly authorized
`REPEAT_OF`, `DIFFERENT_FROM` and `COMPENSATES` relationships. Their authority
keys bind the new canonical material and defining plan, predecessor descriptor
and defining history, relationship source terms and grant. Every relationship
kind must have a settled, unfenced predecessor before T03. Exact lost-ack T01
replay precedes mutable freshness, returns the original outcome and verifies the
supplied capability against the recorded source-use event without spending it
again.

The v4 schema boundary verifies exact table DDL, foreign keys and canonical
projections without healing deletion or surplus data. Recovery reduces the
synthetic source journal sequentially, so registration must precede use, every
capability must match its grant, time windows and use limits must hold, and a
prior effective revocation/expiry/supersession/unknown state denies the use.
Post-use expiry remains valid. T23 contrary evidence places every dependent
adoption into durable reconciliation with a typed integrity fence. T13
correction clears only authority-owned dependent fences; an authority fact ID
collision cannot clear a contrary-receipt fence.

The implementation review initially returned `REVISE` for under-bound
adoption/relationship authority, incomplete source-history reduction, replay
ordering and silent T23 fence deletion. Corrections retained the contrary fence,
bound complete root/immediate/check/source materials and added sequential source
verification. A second `REVISE` found missing adoption source terms and a
cross-domain correction-owner collision. Complete source-term replay binding
and provenance-scoped correction closed both. Final independent review returned
`APPROVE` with no remaining blocker or major.

The final focused set passed four tests. The complete delivery-control package
passed 391 tests in 60.210 seconds. Repository validation found 184 valid skills
with zero warnings, 8 script tests passed with 4 expected skips, all 91 gate
self-test assertions passed, compileall passed and `git diff --check` exited 0
with Windows line-ending notices only. Signed implementation commit
`bbc96cffc31b8d1c82ba8877309d14674f133ff5` was pushed to the existing branch.
Exact-head hosted checks were pending when this evidence commit was written.

Changed implementation files are `authority.py`, `contracts.py`, `dispatch.py`,
`storage.py`, `test_dispatch.py`, `test_storage.py` and `_legacy_schema.py`.
Canonical design, approval register, BER, dependencies, CI, CLI, real authority/
adapters, external systems and preserved artifact/cache paths were intentionally
untouched. T28/F01 receive accepted slice evidence but remain conservatively
`UNVERIFIED` as accumulated matrix rows pending exact-head trace. At that
checkpoint, cross-family F05/F06/F13/F20 was next; PR #99 remained open, draft
and blocked.

### 7.21 Cross-family F05/F06/F13/F20

F05 now requires an exact independently supplied catalog/run/source-head vector
at every dispatch-capable storage boundary. Exact idempotent replay remains
available before mutable freshness checks, but a stale copied database cannot
spend a new HOST or MANUAL one-use source grant; denial leaves the database
byte-identical. Source, run and effect rollback vectors, missing or surplus
members and independent-current mismatch all fail closed.

F06 exercises one repository-wide outstanding-operation slot across runs,
items, lifecycle states, known and unknown accounting and generation-bound
same-effect retry. F13 records late proof-first contrary receipts with exact
known or worst-case accounting against PLANNED, RUNNING, PAUSING, PAUSED,
BLOCKED, VALIDATING, RECONCILIATION_REQUIRED and terminal successors. Tests
assert each actual pre-receipt state; PAUSING is created lawfully through T05
before adapter contact. Terminal successors remain terminal, while nonterminal
successors retain slot ownership and enter reconciliation.

F20 adds a typed validator containment specification bound into validator
grants, capabilities, intent, contact, observation and recovery. It enforces
pairwise-disjoint canonical roots, a fixed standard-library-only action set,
internally derived canonical output byte size with a hard bound, and a pure
checker that denies path escape, mutation, descendant tools and network access.
The v5 migration verifies exact validator-intent/event schemas and unique/partial
indexes without healing drift; legacy active intent without containment cannot
launch.

The plan audit returned `REVISE` twice before the third audit returned `APPROVE`,
expanding the mutation inventory and the F06/F13 state matrices and making F20
containment and recovery exact. Implementation review then required three correction rounds:
caller-asserted output bounds, nested roots, optional recovery authority,
schema/event drift and incomplete F05/F06/F13 coverage were corrected first;
the final two findings added freshness to new one-use source consumption and
replaced a mislabeled PAUSING fixture with a lawful T05 transition. Final
independent review returned `APPROVE` with no remaining blocker or major.

The final focused three-test set passed in 2.143 seconds. The complete
delivery-control package passed 413 tests in 67.555 seconds. Repository
validation found 184 valid skills with zero warnings, 8 script tests passed with
4 expected skips, all 91 gate self-test assertions passed and compileall passed.
`git diff --check` exited 0 with Windows line-ending notices only. Changed
implementation files are `adapters.py`, `authority.py`, `contracts.py`,
`dispatch.py`, `storage.py`,
`test_dispatch.py` and `test_storage.py`. Canonical design, approval register,
BER, dependencies, CI, CLI, real authority/adapters, external systems and
preserved artifact/cache paths were intentionally untouched.

DCO-signed implementation commit
`cf09be260bbffcb78dc44847b317d6c4a0de8237` was pushed to the existing branch
after fetched remote head `676c4e2bc366290f28802721cd1dd99467a71707`
matched its parent. Exact-head hosted checks passed: `gate-guard` in 6 seconds,
`validate-skills` in 1m19s and `windows-offline-checks` in 1m55s. Local and
remote heads matched, `ba13394` remained an ancestor, tracked state was clean,
preserved untracked paths remained untouched, and PR #99 remained open, draft
and blocked.

F05/F06/F13/F20 receive independently accepted evidence but remain
conservatively `UNVERIFIED` as accumulated matrix rows until the final exact-head
trace. The next documented slice was filesystem ownership/reparse/path-swap
protection.

### Filesystem ownership/reparse/path-swap checkpoint

The checked-path layer now covers the controller database, both synthetic
adapter ledgers, the stable writer lock, CLI status and read-only terminal
reporting. Windows binds the OS-known LocalAppData result to retained fixed-
volume and known-folder handles, a normalized handle-verified lexical path and every
managed descendant identity. It denies junctions, same-volume known-folder
rebinding, leaf/ancestor replacement, hardlinks, unsafe ACLs, WAL/SHM sidecars
and unsafe rollback journals. Every later store mutation requires the original
`writer.lock` identity, preventing replacement from splitting serialization.

The POSIX path uses descriptor-relative `O_NOFOLLOW`, rejects mount transitions
and untrusted ancestor owners, and requires an owner-private child after sticky
directories. Its policy tests pass, but no POSIX runtime evidence exists, so the
platform result remains `UNVERIFIED`. Windows can prevent untrusted-principal
swaps while checked handles are live; same-owner replacement is detected at the
next identity-pinned connection. No continuity across a new process is claimed
beyond the protected root plus durable journal/freshness checks.

The final focused platform module passed 27 tests. The complete delivery-control
package passed 433 tests in 78.889 seconds on the final reviewed diff. Repository validation found 184
valid skills with zero warnings, 8 script tests passed with 4 expected skips,
all 91 gate self-test assertions passed, compileall passed and `git diff --check`
exited 0 with Windows line-ending notices only. Independent implementation
review corrected full Windows ancestor/anchor binding, persistent lock identity,
POSIX ownership/sticky semantics, error cleanup and same-volume path rebinding;
its final verdict was `APPROVE` with no remaining blocker or major.

Changed implementation files are new `owned_paths.py`, `storage.py`,
`adapters.py`, `cli.py`, `test_platform.py`, and narrow isolation/canonical-path
fixtures in `test_dispatch.py`, `test_recovery.py` and `test_storage.py`. This
handoff, the backlog and status READMEs record the evidence. Canonical design,
approval register, BER, dependencies, CI workflows, real authority/adapters,
external systems and preserved artifact/cache paths remain intentionally
untouched. The current sandbox principal does not own its OS-returned
LocalAppData directory, so a real default-root smoke run is correctly
`UNAVAILABLE`; tests use the checked known-folder seam.

The filesystem slice is independently accepted, but accumulated T/C/F rows
remain conservatively `UNVERIFIED` until the final exact-head trace. PR #99
remains open, draft and blocked; documentation and final architecture/security/
QA review gates remain, and this checkpoint authorizes no release or deployment.

## 8. Proven invocations

| Command | Tell-tale result |
| --- | --- |
| `git branch --show-current; git rev-parse HEAD; git rev-parse --verify origin/main; git remote -v` before branching | `main`; local and `origin/main` both `497a4529...`; origin `https://github.com/ModernNomad-98/Project-Aegis.git` |
| `python -m unittest discover -s tools/aegis_delivery_control/tests -v` before documentation edits | `Ran 198 tests in 16.659s`; `OK` |
| `git diff --check` before documentation edits | Exit 0; no output |
| `python -m unittest discover -s tools/aegis_delivery_control/tests` immediately before commit | `Ran 198 tests in 15.955s`; `OK` |
| `git diff --check` immediately before commit | Exit 0; no output |
| `git commit -s -m "feat(control-plane): checkpoint offline kernel"` | Commit `ba13394`; signed-off; 15 files, 19,000 insertions, 2,811 deletions |
| `git push -u origin feat/cp-wp-002-offline-kernel` | New remote branch created and upstream configured |
| `gh pr create --draft ...` | Draft PR `https://github.com/ModernNomad-98/Project-Aegis/pull/99` |
| `git push` after `8456a36` | Remote branch advanced `ba13394..8456a36` |
| `gh pr edit 99 ...` | PR #99 URL returned after body synchronization |
| Public read of PR #99 after update | Draft; two commits; latest head `8456a36`; implementation commit showed 3/3 checks, handoff head checks still running |
| `gh api "repos/ModernNomad-98/Project-Aegis/deployments?per_page=100"` | `[]` |
| `gh release list --repo ModernNomad-98/Project-Aegis --limit 20` | `no releases found` |
| Dashboard cleanup verification | `Test-Path tools/aegis_delivery_control/dashboard` returned `False`; dashboard absent from `git status` |
| Local-link audit over the five updated Markdown files | 103 local Markdown links checked; all targets exist |
| T/C/F matrix row-count check | T=28, C=9, F=22 (F04a and F04b are separate canonical rows) |
| `python -B scripts/validate-skills.py` | `OK: 184 skill(s) valid, 0 warning(s)` |
| `python -B scripts/tests/test_validator.py` | `OK: 91 gate self-test assertion(s) passed.` |
| Independent corrected-handoff re-review | `APPROVE`; no blocker, major, minor or nit findings |
| R-STOP-01 focused first test | Failed on unsupported `VALIDATION_APPLICATION`; passed after the narrow contract/storage change |
| `python -m unittest tools.aegis_delivery_control.tests.test_storage` | `Ran 168 tests in 14.231s`; `OK` |
| `python -m unittest discover -s tools/aegis_delivery_control/tests -v` | `Ran 209 tests in 16.666s`; `OK` |
| Independent R-STOP-01 implementation review | `APPROVE`; no findings; independent 9-test focused run passed |
| R-STOP-02 initial / corrected plan audits | `REVISE`, then `APPROVE`; operator route selected and deadline scheduler omitted honestly |
| R-STOP-02 focused first test | Failed because coordinator `escalate_stop` was absent; passed after implementation |
| R-STOP-02 focused suite after review correction | `Ran 10 tests`; `OK` |
| `python -m unittest tools.aegis_delivery_control.tests.test_storage` after R-STOP-02 | `Ran 177 tests in 14.474s`; `OK` |
| `python -m unittest discover -s tools/aegis_delivery_control/tests -p 'test_*.py'` after R-STOP-02 | `Ran 219 tests in 19.387s`; `OK` |
| R-STOP-02 initial / corrected implementation reviews | `REVISE` for item-retarget recovery gap, then `APPROVE`; reviewer independently passed 10 focused tests and the former probe failed closed |
| T13 focused first falsification | Failed because `record_authority_fact` was absent; passed after the typed durable route |
| T13 complete delivery-control package | `Ran 242 tests in 21.120s`; `OK` |
| T13 repository validators | 184 skills valid with zero warnings; 91 gate self-test assertions passed |
| Independent T13 implementation review | Initial and intermediate `REVISE` findings corrected; final `APPROVE`, no remaining blocker/major; 16 focused tests passed independently |
| T15 focused first falsifications | Unpinned plan acceptance failed to reject; typed mismatch failed because `record_binding_mismatch` was absent; both passed after the narrow implementation |
| T15 focused suite | `Ran 14 tests`; `OK` |
| T15 complete delivery-control package | `Ran 256 tests in 19.733s`; `OK` |
| T15 repository validators | 184 skills valid with zero warnings; 91 gate self-test assertions passed; `git diff --check` exit 0 with line-ending notices only |
| Independent T15 implementation review | Initial `REVISE` for active BLOCKED routing; corrected final `APPROVE`, no remaining blocker/major; 14 focused tests passed independently |
| `git commit -s -m "feat(control-plane): fence immutable binding mismatches"` | Commit `2de362612f43c125829ff8c73e22bcdcfa6147c0`; signed-off; 12 files changed |
| `git push origin feat/cp-wp-002-offline-kernel` after T15 | Remote branch advanced `7114bc7..2de3626` |
| Live PR #99 read on T15 implementation head | OPEN; DRAFT; BLOCKED; head `2de362612f43c125829ff8c73e22bcdcfa6147c0` |
| Hosted checks on exact T15 implementation head | `gate-guard` passed in 5s; `validate-skills` passed in 1m24s; `windows-offline-checks` passed in 2m59s |
| T14 plan audits | Two `REVISE` rounds, then `APPROVE`; exact source/current bindings, compatibility migration, prefix route, MAC evidence and deferred T08 integration were explicit |
| T14 focused suite after corrections | `Ran 21 tests in 0.957s`; `OK` |
| T14 affected storage/dispatch modules | `Ran 255 tests in 21.039s`; `OK` |
| T14 complete delivery-control package | `Ran 277 tests in 22.194s`; `OK` |
| T14 repository validators | 184 skills valid with zero warnings; 91 gate self-test assertions passed; `git diff --check` exit 0 with line-ending notices only |
| Independent T14 implementation review | Initial `REVISE` with four MAJOR recovery findings; corrected `APPROVE`, no remaining blocker/major; reviewer independently ran 21 tests in 0.982s |
| `git commit -s -m "feat(control-plane): add pause-source resume recovery"` | Commit `c3c94bf3d367380d1ff60835fb72cb300e69c3e4`; signed-off; 11 files changed |
| `git push origin feat/cp-wp-002-offline-kernel` after T14 | Remote branch advanced `384b3eb..c3c94bf` |
| Live PR #99 read before T14 delivery | OPEN; DRAFT; BLOCKED; head `384b3eb5b7e9880dd920477cb1bd98e90e6a29c6`; prior three checks successful |
| Hosted checks on exact T14 implementation head | `gate-guard` passed in 3s; `validate-skills` passed in 1m18s; `windows-offline-checks` passed in 3m23s |
| T05 initial / corrected plan audits | `REVISE` for three MAJOR pre-launch/authenticity/schema gaps, then `APPROVE`; no remaining blocker/major |
| T05 focused first falsifications | Missing typed contract, state-owner method and coordinator route failed before their narrow implementations |
| T05 focused suite after review correction | `Ran 17 tests in 0.675s`; `OK` |
| T05 affected storage/dispatch modules | `Ran 272 tests in 22.140s`; `OK` |
| T05 complete delivery-control package | `Ran 294 tests in 23.893s`; `OK` |
| T05 repository validators | 184 skills valid with zero warnings; 91 gate self-test assertions passed; `git diff --check` exit 0 with line-ending notices only |
| Independent T05 implementation review | Initial `REVISE` for one MAJOR predecessor-cursor recovery gap; corrected `APPROVE`, no remaining blocker/major; reviewer independently ran 17 focused tests in 0.743s |
| `git commit -s -m "feat(control-plane): add local execution pause fence"` | Commit `13bda54b9bc63e962a3900ac16640fd2bb18d304`; signed-off; 5 files changed |
| `git push origin feat/cp-wp-002-offline-kernel` after T05 | Remote branch advanced `52e73db..13bda54` |
| Hosted checks on exact T05 implementation head | `gate-guard` passed in 4s; `validate-skills` passed in 1m18s; `windows-offline-checks` passed in 3m22s |
| T06 initial / corrected plan audits | `REVISE` for one BLOCKER and two MAJOR state/accounting/receipt-route gaps, then `APPROVE`; no remaining blocker/major |
| T06 focused first falsification | Import failed because the typed external-pause request was absent; the narrow implementation made the contacted/no-receipt test pass |
| T06 focused suite after review corrections | `Ran 14 tests in 0.923s`; `OK` |
| T06 affected storage/dispatch modules | `Ran 285 tests in 23.229s`; `OK` |
| T06 complete delivery-control package | `Ran 307 tests in 23.939s`; `OK` |
| T06 repository validators | 184 skills valid with zero warnings; 91 gate self-test assertions passed; compileall passed; `git diff --check` exit 0 with line-ending notices only |
| Independent T06 implementation review | Initial `REVISE` for two MAJOR contact-history and prefix-accounting recovery gaps; corrected `APPROVE`, no remaining blocker/major; reviewer independently ran 14 focused tests in 0.824s |
| `git commit -s -m "feat(control-plane): fence contacted pause uncertainty"` | Commit `39b3268adc984e3d0b10e55a42fe37a172229e60`; signed-off; 5 files changed |
| `git push origin feat/cp-wp-002-offline-kernel` after T06 | Remote branch advanced `0cdb6d1..39b3268` |
| Hosted checks on exact T06 implementation head | `gate-guard` passed in 7s; `validate-skills` passed in 1m20s; `windows-offline-checks` passed in 2m49s |
| T07 plan audits | Three `REVISE` rounds, then `APPROVE`; cessation authority, T25/T17/T14 interactions, projection separation and legacy signed-request compatibility were made explicit |
| T07 correction-focused suite | `Ran 3 tests in 0.197s`; `OK` |
| T07 affected storage/dispatch modules | `Ran 296 tests in 24.830s`; `OK` |
| T07 complete delivery-control package | `Ran 318 tests in 25.638s`; `OK` |
| T07 repository validators | 184 skills valid with zero warnings; 8 script tests passed with 4 expected skips; 91 gate self-test assertions passed; compileall passed; `git diff --check` exit 0 with line-ending notices only |
| Independent T07 implementation reviews | Initial `REVISE` for two MAJOR settlement-prefix and slot-generation recovery defects; corrected `APPROVE`, no remaining blocker/major; reviewer independently ran 3 correction tests in 0.194s |
| T08 plan audit | Initial `REVISE` for three checkpoint/cessation/race gaps; corrected `APPROVE` before editing |
| T08 focused suite | `Ran 13 tests in 2.536s`; `OK`; two race tests also passed in three repeated runs |
| T08 dispatch module | `Ran 40 tests in 4.925s`; `OK` |
| T08 complete delivery-control package | `Ran 331 tests in 28.693s`; `OK` |
| T08 repository validators | 184 skills valid with zero warnings; 8 script tests passed with 4 expected skips; 91 gate self-test assertions passed; compileall passed; `git diff --check` exit 0 with line-ending notices only |
| Independent T08 implementation review | Initial `REVISE` for two MAJOR cessation/race gaps; corrected `APPROVE`, no remaining blocker/major; reviewer independently ran 13 focused tests in 2.479s |
| `git commit -s -m "feat(control-plane): checkpoint validation pause"` | Commit `a0d27bbdd64d7d86bf080355ca933d28760244ab`; signed-off; 10 files changed |
| `git push origin feat/cp-wp-002-offline-kernel` after T08 | Remote branch advanced `511f590..a0d27bb` |
| Hosted checks on exact T08 implementation head | `gate-guard` passed in 5s; `validate-skills` passed in 1m19s; `windows-offline-checks` passed in 2m58s |
| T09 plan audit | `APPROVE` before editing; exact source/head/cursor, typed one-use PAUSE capability, stacked fences and deferred T17/T14 clearance were explicit |
| T09 focused suite after review correction | `Ran 8 tests in 1.580s`; `OK` |
| T09 dispatch module | `Ran 48 tests in 6.715s`; `OK` |
| T09 complete delivery-control package | `Ran 339 tests in 30.792s`; `OK` |
| T09 repository validators | 184 skills valid with zero warnings; 8 script tests passed with 4 expected skips; 91 gate self-test assertions passed; compileall passed; `git diff --check` exit 0 with line-ending notices only |
| Independent T09 implementation review | Initial `REVISE` for one MAJOR future-clearance foreign-key defect; corrected `APPROVE`, no findings; reviewer independently ran 8 focused tests in 1.453s |
| `git commit -s -m "feat(control-plane): fence reconciliation pauses"` | Commit `9599bcb748f2290f328561704c860f5cb3b9c4c3`; signed-off; 10 files changed |
| `git push origin feat/cp-wp-002-offline-kernel` after T09 | Remote branch advanced `9b4cc6f..9599bcb` |
| Hosted checks on exact T09 implementation head | `gate-guard` passed in 7s; `validate-skills` passed in 1m18s; `windows-offline-checks` passed in 2m47s |
| Live PR #99 on exact T09 implementation head | OPEN; DRAFT; BLOCKED; head `9599bcb748f2290f328561704c860f5cb3b9c4c3` |
| T17/T14 focused stacked-fence regression after final corrections | Two T09 fences cleared sequentially; first resume remained PAUSED, second returned VALIDATING; rollback/replay and semantic tamper checks passed |
| T17/T14 affected dispatch/storage modules before final correction | `Ran 330 tests in 40.735s`; `OK` |
| `python -m unittest discover -s tools/aegis_delivery_control/tests -p "test_*.py"` after final T17/T14 corrections | `Ran 352 tests in 41.590s`; `OK` |
| T17/T14 repository validators | 184 skills valid with zero warnings; 8 script tests passed with 4 expected skips; 91 gate self-test assertions passed; compileall passed |
| `git diff --check` after final T17/T14 corrections | Exit 0; Windows line-ending notices only |
| Independent T17/T14 implementation review | Two `REVISE` rounds closed repository scope/distinct contract and stacked-head/reducer/source-binding defects; final `APPROVE`, no remaining blocker or major |
| T17/T14 delivery preflight | Local and remote head `637b2caf026ae638ae5ba34af93a788a2c3d6512`; `ba13394` ancestor; PR #99 OPEN/DRAFT/BLOCKED with all three checks successful; approvals active; owner confirmed preservation of the additional `scripts/ci/__pycache__/` path |
| T17 operation-uncertainty plan audit | Corrected narrow runtime/migration/recovery/accounting plan received `APPROVE` before editing |
| T17 operation-uncertainty focused final migration regressions | Disguised validator-shaped operation row and projection-only settlement tamper both denied; rollback retained semantic version 0 and the original tampered rows; `Ran 2 tests`; `OK` independently |
| T17 operation-uncertainty affected storage/dispatch modules | `Ran 342 tests in 43.910s`; `OK` |
| T17 operation-uncertainty complete delivery-control package | `Ran 364 tests in 44.034s`; `OK` |
| T17 operation-uncertainty repository validators | 184 skills valid with zero warnings; 8 script tests passed with 4 expected skips; 91 gate self-test assertions passed; compileall passed |
| `git diff --check` after final operation-uncertainty corrections | Exit 0; Windows line-ending notices only |
| Independent T17 operation-uncertainty implementation review | Two `REVISE` rounds closed six MAJOR evidence/MAC/atomicity/legacy-audit/settlement-projection findings; final `APPROVE`, no remaining blocker or major |
| T17 verified-receipt focused falsification | Four-category T06 late receipt retained the operator pause and routed to typed `PAUSED`; observation-only billing ancestry routed cleanly to `VALIDATING`; stale order, wrong source/response, `UNKNOWN`, missing/surplus schema, stale slot, forged MAC, crash and projection tamper probes denied or replayed exactly as required |
| `python -m unittest discover -s tools/aegis_delivery_control/tests -p "test_*.py"` after verified-receipt review corrections | `Ran 368 tests in 45.506s`; `OK` |
| T17 verified-receipt repository validators | 184 skills valid with zero warnings; 8 script tests passed with 4 expected skips; 91 gate self-test assertions passed; compileall passed; `git diff --check` exited 0 with Windows line-ending notices only |
| Independent T17 verified-receipt implementation review | Initial `REVISE` closed two MAJOR typed lookup-envelope and replay-order findings; corrected review `APPROVE`, no remaining blocker or major; reviewer independently passed 3 focused tests |
| T17 nonexecution/safe-retry focused regression | Generation-2 T10/T27/T11/T12/T16/T23/T26, INTENT_ONLY/LAUNCHED/CONTACTED T25 seals, stacked T14 pauses, crash/replay/restart, tamper and generation-1 compatibility passed |
| T17 nonexecution/safe-retry storage module | `Ran 279 tests in 32.924s`; `OK` |
| T17 nonexecution/safe-retry complete delivery-control package | `Ran 373 tests in 47.700s`; `OK` |
| T17 nonexecution/safe-retry repository validators | 184 skills valid with zero warnings; 8 script tests passed with 4 expected skips; 91 gate self-test assertions passed; compileall passed |
| Independent T17 nonexecution/safe-retry implementation review | Initial `REVISE` closed three generation/action/pause-replay findings; two later migration BLOCKERs corrected exact-HEAD terminal schema and proof-prefix T25 backfill. Final `APPROVE`, no remaining blocker or major; reviewer independently passed both migration probes |
| T17 nonexecution/safe-retry delivery | Signed-off commit `a6b2d8624400d7af3be2cb309db01864d6e8e472` pushed; exact-head `gate-guard` passed in 5s, `validate-skills` in 1m7s and `windows-offline-checks` in 3m1s; PR #99 remained OPEN/DRAFT/BLOCKED |
| T22 cold-start preflight | Local and remote head `3406e3e22f80f461e35f529900c289c7b93c46ac`; `ba13394` ancestor; source landmarks present; tracked state clean; preserved untracked inventory matched; PR #99 OPEN/DRAFT/BLOCKED with all three checks successful; approvals active |
| T22 plan audit | Three `REVISE` rounds corrected freshness/reporting, true read-only access, trusted verifier injection, request/verification axes and nonterminal dispatch posture; final `APPROVE` before editing |
| T22 focused regression after implementation corrections | `Ran 11 tests in 1.106s`; `OK`; independent rerun passed 11 tests in 1.038s |
| T22 complete delivery-control package | `Ran 384 tests in 53.243s`; `OK` |
| T22 repository validators | 184 skills valid with zero warnings; 8 script tests passed with 4 expected skips; 91 gate self-test assertions passed; compileall passed |
| Independent T22 implementation review | Initial `REVISE` found two MAJOR read-only auxiliary-ledger and structural-JSON failure gaps; corrected `APPROVE`, no remaining blocker or major |
| `git diff --check` after T22 corrections | Exit 0; Windows line-ending notices only |
| T22 commit, push and hosted checks | Signed implementation commit `39ad374a172122c14d06070f65c1e033da3b5c83` pushed; local and remote heads matched; `ba13394` remained an ancestor; exact-head `gate-guard`, `validate-skills` and `windows-offline-checks` passed; PR #99 remained OPEN/DRAFT/BLOCKED |
| T28/F01 focused regressions | Root/immediate/check/source adoption-key changes, relationship material/history/source rebinding, occupied slot, spent one-use grant, v4 no-heal, source window/use-limit/revoke recovery, terminal settlement and T13/T23 collision ownership passed |
| T28/F01 complete delivery-control package | `Ran 391 tests in 60.210s`; `OK` |
| T28/F01 repository validators | 184 skills valid with zero warnings; 8 script tests passed with 4 expected skips; 91 gate self-test assertions passed; compileall passed |
| Independent T28/F01 implementation review | Correction rounds closed all authority-binding, sequential-source, replay and typed dependent-fence findings; final `APPROVE`, no remaining blocker or major |
| T28/F01 implementation delivery | Signed implementation commit `bbc96cffc31b8d1c82ba8877309d14674f133ff5` pushed after remote head `8ac0c342b7648b4eb5b8697e260271480af64244` matched its parent; PR #99 remained OPEN/DRAFT at pre-push verification; hosted exact-head checks pending |
| Cross-family F05/F06/F13/F20 focused regressions | Final three-test set passed in 2.143s: source-use replay/stale-copy non-mutation, dispatch-boundary guard inventory and exact PAUSING contrary-receipt recovery |
| Cross-family F05/F06/F13/F20 complete delivery-control package | `Ran 413 tests in 67.555s`; `OK` |
| Cross-family F05/F06/F13/F20 repository validators | 184 skills valid with zero warnings; 8 script tests passed with 4 expected skips; 91 gate self-test assertions passed; compileall passed |
| Independent cross-family F05/F06/F13/F20 implementation review | Three correction rounds closed all output-bound/root/authority/schema/matrix/freshness/fixture findings; final `APPROVE`, no remaining blocker or major |
| Cross-family F05/F06/F13/F20 delivery | DCO-signed implementation commit `cf09be260bbffcb78dc44847b317d6c4a0de8237` pushed after remote head `676c4e2bc366290f28802721cd1dd99467a71707` matched its parent; exact-head `gate-guard`, `validate-skills` and `windows-offline-checks` passed; PR #99 remained OPEN/DRAFT/BLOCKED |
| Filesystem plan audit | Two `REVISE` rounds corrected exact anchors, prevention/detection limits, rollback-journal handling and noncreating read-only access; final `APPROVE` before editing |
| Filesystem focused platform module | Initial `Ran 22 tests`; `OK`; independent falsifier-plus-module rerun passed 23/23; final-review corrections expanded the module to 27 passing tests |
| Filesystem complete delivery-control package | `Ran 433 tests in 78.889s`; `OK` on the final reviewed diff |
| Filesystem repository validators | 184 skills valid with zero warnings; 8 script tests passed with 4 expected skips; 91 gate self-test assertions passed; compileall passed |
| Filesystem diff validation | `git diff --check` exit 0 with Windows line-ending notices only |
| Independent filesystem implementation review | `REVISE` rounds closed Windows ancestor/known-folder binding, stable-lock identity, POSIX owner/sticky checks, cleanup leaks and same-volume rebinding; final `APPROVE`, no remaining blocker or major |
| Final-review correction pass | Architecture `REVISE` found premature canonical-root discovery affecting `capabilities`, typed `status` and explicit-path stores; QA `REVISE` required hostile Windows ACL and valid-status nonmutation regressions; security initially `APPROVE` with wording/test/flag notes. Corrections pass the 27-test platform module and 433-test package; architecture, security and QA re-reviews all returned `APPROVE` with no blocker or major |

The first handoff audit returned `REVISE`: one precedence blocker, three major
evidence/inventory/backlog findings and two minor cleanup/index findings. Stage 3
addresses those findings and requires re-review before closeout.

The independent stop reviewer was read-only and did not execute tests. Its
findings are code-review evidence, not an executable test receipt.

## 9. Independent stop gate - aggregate `APPROVE`

R-STOP-01, R-STOP-02 and R-STOP-03 are accepted. The aggregate stop gate is
`APPROVE`; later backlog and final review gates still block merge.

### R-STOP-01 - RESOLVED - independent `APPROVE`

STOP can be entered from `BLOCKED/FINALIZING` or recoverable validation-failure
state while retaining the repository slot. T16 is unavailable after `STOPPED`,
and T26 rejects an already-settled validator intent. New intents remain denied
while the slot exists.

Review anchors:

- [`contracts.py`](../../../tools/aegis_delivery_control/contracts.py#L493)
- [`engine.py`](../../../tools/aegis_delivery_control/engine.py#L49)
- [`storage.py`](../../../tools/aegis_delivery_control/storage.py#L4962)
- [`storage.py`](../../../tools/aegis_delivery_control/storage.py#L9079)
- [`storage.py`](../../../tools/aegis_delivery_control/storage.py#L9770)
- [`storage.py`](../../../tools/aegis_delivery_control/storage.py#L10260)
- [`storage.py`](../../../tools/aegis_delivery_control/storage.py#L12891)

Resolution: T26 accepts a typed `VALIDATION_APPLICATION` reference to the exact
already-applied observation/application and latest validator attempt. It preserves
terminal lifecycle and prior cursor history, performs no reapplication, and
atomically releases the slot only after every validation and accounting obligation
closes. Tests cover T18 and T19 from both affected predecessor states, denial of
unrelated dispatch before closure, dispatch after closure, C05/C09 crash/replay,
legacy migration, superseded attempts and tampering. Independent plan and
implementation reviews both ended `APPROVE`; the aggregate stop gate remains
`APPROVE` after the later R-STOP-02 and R-STOP-03 corrections.

### R-STOP-02 - RESOLVED - independent `APPROVE`

T20 has a typed request, operator-authorized coordinator route and an atomic,
idempotent storage transaction bound to the exact graceful stop/deadline,
accepted plan/run identity, retained slot and complete unresolved obligation
snapshot. Ambiguous reservations become versioned
`UNKNOWN_WORST_CASE_CHARGED` settlements before the same transaction records
`STOP_ESCALATED`; known accounting, lifecycle, fence, cursor and slot are
preserved. Recovery validates the historical prefix and remains valid after
later authoritative correction and terminal release.

Review anchors:

- [`engine.py`](../../../tools/aegis_delivery_control/engine.py#L51)
- [`contracts.py`](../../../tools/aegis_delivery_control/contracts.py#L715)
- [`storage.py`](../../../tools/aegis_delivery_control/storage.py#L5317)
- [canonical T20](../../design/resumable-control-plane-v1.md#L447)

Resolution: the plan audit reconciled the transient exclusion note against the
canonical design and AEGIS-APR-004, selecting the canonical O route while
explicitly omitting an unapproved deadline-rule scheduler. Focused coverage
includes deadline and drain predicates, exact settlement coverage, C06/C09
commit boundaries, replay, later T23/T26 correction/release/restart, projection
and historical tamper. The initial implementation review's item-retarget finding
was corrected; re-review returned `APPROVE` with no findings.

### R-STOP-03 - RESOLVED - independent `APPROVE`

Adapter contact is durably claimed before target execution, creating a window in
which effect outcome and billing are unknown. The corrected immediate-stop path
now classifies that bounded exposure atomically as
`UNKNOWN_WORST_CASE_CHARGED`.

Review anchors:

- [`adapters.py`](../../../tools/aegis_delivery_control/adapters.py#L455)
- [`storage.py`](../../../tools/aegis_delivery_control/storage.py#L1831)
- [`storage.py`](../../../tools/aegis_delivery_control/storage.py#L4962)
- [`storage.py`](../../../tools/aegis_delivery_control/storage.py#L6668)
- [canonical T19](../../design/resumable-control-plane-v1.md#L446)

Resolution: T19 atomically converts exact contacted, unresolved reserved effect
or validator liability to `UNKNOWN_WORST_CASE_CHARGED`, retains pre-contact and
known accounting, and persists a strict contact/reservation/settlement snapshot.
Crash/replay, late adjustment/restart, tamper and cross-run reused-attempt tests
pass. The initial alias finding was corrected and re-review returned `APPROVE`.

## 10. Backlog state

Canonical obligations remain T01-T28, C01-C09 and F01-F21. Do not infer a family
complete from the 384 passing tests, a registry entry or an earlier milestone
paragraph. No complete exact-head traceability audit was performed at this
checkpoint.

Status legend: `YES` means directly established at this checkpoint;
`NO` means a verified absence or failed gate; `UNVERIFIED` means the exact-head
implementation-to-test-to-requirement trace has not been audited. `UNVERIFIED`
is not a failure and must never be upgraded from filenames, test counts or a
transition registry entry.

### T01-T28 transition matrix

Canonical rows: [design transition table](../../design/resumable-control-plane-v1.md#L420-L455).

| ID | Implemented | Tested | Independently accepted | Current disposition / evidence |
| --- | --- | --- | --- | --- |
| T01 | UNVERIFIED | UNVERIFIED | UNVERIFIED | Code/test names exist; exact-head trace required |
| T02 | UNVERIFIED | UNVERIFIED | UNVERIFIED | Historical readiness work exists; exact-head trace required |
| T03 | UNVERIFIED | UNVERIFIED | UNVERIFIED | Historical focused evidence only |
| T04 | UNVERIFIED | UNVERIFIED | UNVERIFIED | Exact-head trace required |
| T05 | YES | YES | YES | Exact owned pre-launch/launched-before-contact local pause, durable fence/authenticity, crash/replay and recovery independently accepted; no cancel/drain side effect claimed |
| T06 | YES | YES | YES | Exact contacted/no-receipt route, atomic worst-case accounting/fence, T23 late-receipt behavior, crash/replay and prefix-derived recovery independently accepted; no unauthenticated PAUSING/cancel claim |
| T07 | UNVERIFIED | UNVERIFIED | UNVERIFIED | T05-local/T25-authoritative nonexecution settlement and BLOCKED-only T14 recovery slice independently accepted; T08/T24/other source families remain |
| T08 | UNVERIFIED | UNVERIFIED | UNVERIFIED | Idle/exact-settled-result pause, unresolved reconciliation, contacted worst-case accounting and clean VALIDATING T14 slice independently accepted; active drain/cancel and broader cessation sources remain |
| T09 | YES | YES | YES | Exact current-head reconciliation fence, one-use authority, idempotent replay, stacked fence, no-adapter invariants and strict recovery independently accepted |
| T10 | UNVERIFIED | UNVERIFIED | UNVERIFIED | Exact-head trace required |
| T11 | UNVERIFIED | UNVERIFIED | UNVERIFIED | Historical validation work only |
| T12 | UNVERIFIED | UNVERIFIED | UNVERIFIED | Historical validation work only |
| T13 | YES | YES | YES | Typed lifecycle facts, grant-wide denial, exact own-use continuation, typed supersession and correction independently accepted |
| T14 | UNVERIFIED | UNVERIFIED | UNVERIFIED | PLANNED/BLOCKED, T07 activity recovery, T08 clean recovery, sequential T09 clearance and operation-nonexecution stacked-pause slices independently accepted; other source families remain |
| T15 | YES | YES | YES | Immutable source/item/plan/policy pins, authenticated mismatch evidence, atomic scoped fence and historical activity routing independently accepted |
| T16 | UNVERIFIED | UNVERIFIED | UNVERIFIED | R-STOP-01 terminal closure plus typed operation-recovery authorization/finalization slices accepted; full T16 trace remains |
| T17 | UNVERIFIED | UNVERIFIED | UNVERIFIED | Validator-result, operation-uncertainty, verified-receipt, authoritative-nonexecution and generation-bound safe-retry slices independently accepted; accumulated exact-head trace remains |
| T18 | YES | YES | YES | Graceful-stop and terminal-closure slices independently accepted |
| T19 | YES | YES | YES | Terminal closure and post-contact uncertainty slices independently accepted |
| T20 | YES | YES | YES | Operator escalation route independently accepted; no deadline-rule scheduler claimed |
| T21 | UNVERIFIED | UNVERIFIED | UNVERIFIED | Exact-head trace required |
| T22 | YES | YES | YES | Typed strictly read-only terminal restart denial, local/current/unverified reporting, unique terminal-entry derivation, no budget/slot mutation and concurrent snapshot behavior independently accepted |
| T23 | UNVERIFIED | UNVERIFIED | UNVERIFIED | Stop interaction plus generation-2 late-receipt/retry-invalidation slice independently accepted; full trace remains |
| T24 | UNVERIFIED | UNVERIFIED | UNVERIFIED | Stop interaction inspected, not independently accepted |
| T25 | UNVERIFIED | UNVERIFIED | UNVERIFIED | INTENT_ONLY/LAUNCHED/CONTACTED canonical-seal, exact proof-prefix clearance and operation-recovery slices independently accepted; full all-state/contradiction trace remains |
| T26 | UNVERIFIED | UNVERIFIED | UNVERIFIED | Applied-evidence closure and generation-2 terminal-settlement migration/replay slices accepted; full T26 trace remains |
| T27 | UNVERIFIED | UNVERIFIED | UNVERIFIED | Generation-2 parent binding, validator contact and recovery/replay slices independently accepted; full trace remains |
| T28 | UNVERIFIED | UNVERIFIED | UNVERIFIED | Verified-effect adoption slice independently accepted; accumulated exact-head trace remains |

### C01-C09 crash-boundary matrix

Canonical rows: [design crash boundaries](../../design/resumable-control-plane-v1.md#L599-L607).

| ID | Implemented | Tested | Independently accepted | Current disposition / evidence |
| --- | --- | --- | --- | --- |
| C01 | UNVERIFIED | UNVERIFIED | UNVERIFIED | Exact-head trace required |
| C02 | UNVERIFIED | UNVERIFIED | UNVERIFIED | Exact-head trace required |
| C03 | UNVERIFIED | UNVERIFIED | UNVERIFIED | T06 plus generation-bound same-effect retry preserve original effect/slot/accounting through missing-receipt reconciliation; complete family trace remains |
| C04 | UNVERIFIED | UNVERIFIED | UNVERIFIED | Earlier receipt slice plus generation-2 receipt/replay evidence accepted; accumulated exact head not re-audited |
| C05 | UNVERIFIED | UNVERIFIED | UNVERIFIED | Earlier slice accepted; accumulated exact head not re-audited |
| C06 | UNVERIFIED | UNVERIFIED | UNVERIFIED | T05/T06/T07/T09 and T17/T25/T14/T16 recovery pre/post-commit rollback/replay, atomic settlement and durable-fence slices accepted; full crash family remains unverified |
| C07 | UNVERIFIED | UNVERIFIED | UNVERIFIED | T22 read-only local status versus independent-current freshness and closed stale/unverified reporting accepted; broader restore/export family remains |
| C08 | UNVERIFIED | UNVERIFIED | UNVERIFIED | T13 lifecycle/unknown-claim slice accepted; complete atomic-claim trace remains |
| C09 | UNVERIFIED | UNVERIFIED | UNVERIFIED | Earlier slice evidence exists; accumulated exact head not re-audited |

### F01-F21 acceptance-family matrix

Canonical rows: [design acceptance families](../../design/resumable-control-plane-v1.md#L939-L960).

| ID | Implemented | Tested | Independently accepted | Current disposition / evidence |
| --- | --- | --- | --- | --- |
| F01 | UNVERIFIED | UNVERIFIED | UNVERIFIED | T15 non-mutation plus canonical relationship/T28 adoption slices independently accepted; accumulated exact-head trace remains |
| F02 | UNVERIFIED | UNVERIFIED | UNVERIFIED | T17 proof-free denial, exact nonexecution proof and generation-bound same-effect retry slices accepted; complete family trace remains |
| F03 | UNVERIFIED | UNVERIFIED | UNVERIFIED | T13 lifecycle/supersession/correction slice accepted; full family trace remains |
| F04a | UNVERIFIED | UNVERIFIED | UNVERIFIED | T17 verified-receipt ancestry, conditional billing and canonical nonexecution zero-liability release slices accepted; complete family trace remains |
| F04b | UNVERIFIED | UNVERIFIED | UNVERIFIED | Stop accounting plus T22 repeated terminal-read no-reset/no-release evidence accepted; full family trace remains |
| F05 | UNVERIFIED | UNVERIFIED | UNVERIFIED | Complete-vector mutation inventory, source/run/effect rollback and stale one-use source denial independently accepted; final exact-head trace remains |
| F06 | UNVERIFIED | UNVERIFIED | UNVERIFIED | Repository-wide lifecycle/accounting matrix and generation-bound same-effect retry independently accepted; final exact-head trace remains |
| F07 | UNVERIFIED | UNVERIFIED | UNVERIFIED | T06 unknown late-receipt retention plus T17 typed source/control settlement and verified-receipt clearance accepted; complete family remains |
| F08 | UNVERIFIED | UNVERIFIED | UNVERIFIED | R-STOP-03 and T06 post-contact/late-adjustment slices accepted; full family trace remains |
| F09 | UNVERIFIED | UNVERIFIED | UNVERIFIED | R-STOP-01 terminal-closure slice accepted; full family trace remains |
| F10 | UNVERIFIED | UNVERIFIED | UNVERIFIED | Exact-head trace required |
| F11 | UNVERIFIED | UNVERIFIED | UNVERIFIED | T17 typed query/time/source/response settlement, repository-prefix, exact-origin ordering and operation-proof prefix accepted; complete claim-settlement family remains |
| F12 | UNVERIFIED | UNVERIFIED | UNVERIFIED | T07 local-nonexecution plus T17 validator/receipt/operation PAUSED-to-BLOCKED recovery slices and semantic migrations accepted; complete family trace remains |
| F13 | UNVERIFIED | UNVERIFIED | UNVERIFIED | Known/unknown proof-first contrary receipts across exact nonterminal and terminal lifecycle states independently accepted; final exact-head trace remains |
| F14 | UNVERIFIED | UNVERIFIED | UNVERIFIED | R-STOP-01 recoverable-failure stop slice accepted; full trace remains |
| F15 | UNVERIFIED | UNVERIFIED | UNVERIFIED | Exact-head trace required |
| F16 | UNVERIFIED | UNVERIFIED | UNVERIFIED | Exact-head trace required |
| F17 | UNVERIFIED | UNVERIFIED | UNVERIFIED | Exact-head trace required |
| F18 | UNVERIFIED | UNVERIFIED | UNVERIFIED | R-STOP-01 terminal closure slice accepted; full family trace remains |
| F19 | UNVERIFIED | UNVERIFIED | UNVERIFIED | T25 exact all-path nonexecution seal and operation recovery slice accepted; complete before/after-handoff and contradiction trace remains |
| F20 | UNVERIFIED | UNVERIFIED | UNVERIFIED | Typed bounded validator containment, authority binding, pure checking and strict migration/recovery independently accepted; final exact-head trace remains |
| F21 | UNVERIFIED | UNVERIFIED | UNVERIFIED | T09 persistence plus T17 exact derivation, receipt/nonexecution clearance, stacked-pause recovery and one-use retry accepted; complete family trace remains |

Immediate order:

1. R-STOP-01 terminal slot closure - complete; independent `APPROVE`.
2. R-STOP-02 T20 graceful-stop escalation - complete; independent `APPROVE`.
3. R-STOP-03 post-contact worst-case accounting - complete; independent
   `APPROVE`.
4. Aggregate stop gate - complete; independent `APPROVE`.

Current durable order after the accepted T17 work is:

1. T15, T05, T06 and T09 complete and independently accepted; T07 local-nonexecution, T08 validation-pause and T14 core slices accepted with the complete transitions still UNVERIFIED pending T17/T24 and other source families.
2. The ordered T17 validator-result, operation-uncertainty, verified-receipt, authoritative-nonexecution and authenticated safe-retry slices are complete and independently accepted; the accumulated matrix row remains UNVERIFIED pending exact-head trace.
3. T22 complete and independently accepted.
4. T28 with F01 complete and independently accepted; accumulated rows remain `UNVERIFIED` pending exact-head trace.
5. Cross-family F05/F06/F13/F20 complete and independently accepted; accumulated rows remain `UNVERIFIED` pending the final exact-head trace.
6. Filesystem ownership/reparse/path-swap protection complete and independently accepted; POSIX runtime remains `UNVERIFIED`.
7. Documentation refresh in progress in this checkpoint.
8. Full local repository validation complete; exact-head hosted validation remains pending commit/push.
9. Independent pre-commit architecture, security and QA reviews complete with `APPROVE`; exact committed-head/hosted confirmation remains.
10. Commit, push, PR update and administrator merge only after all gates pass.

This later order is recovered session context, not a superseding design record.
Before each item, compare it with the current backlog, design and actual diff.
Any mismatch triggers source reconciliation, not silent reordering. Earlier
milestones C04, C05 and C09 have historical focused evidence in the backlog, but
the accumulated exact-head implementation still requires final cross-family
review. Complete transition/acceptance mapping and final exact-head reviews
remain open until proven otherwise.

CP-WP-003, CP-WP-004 and CP-FUT-001 remain blocked. Do not begin them under
AEGIS-APR-004.

## 11. Continuation protocol

For every remaining item:

1. Run the cold-start preflight and inspect the current PR/check/review state.
2. Name one falsifiable local hypothesis and one focused check that can disprove
   it.
3. Write the item plan, including exact files, behavior, tests and scope limits.
4. Obtain an independent read-only audit of the plan. Revise until accepted.
5. Make the smallest grounded edit.
6. Immediately run the focused test that discriminates the hypothesis.
7. Repair locally and rerun that test before widening scope.
8. Run the affected suite, then the full package suite.
9. Update the package README, root/docs routing text and durable backlog only
   with results actually observed.
10. Obtain independent implementation review. A `REVISE` result blocks the next
    item.
11. Commit with DCO sign-off, push the existing branch and update PR #99 under
    the carried approvals. Keep the PR draft until all gates are green.

Do not merge merely because administrator merge is pre-approved. Merge is the
last step after scope, tests, independent reviews, documentation and GitHub
checks all pass. Merge does not authorize a release or deployment.

## 12. Cleanup and removal contract

The accidental dashboard was an unauthorized scope deviation. It was mocked,
untracked and disconnected from the kernel. These files were deleted before the
checkpoint and the empty directory was removed:

```text
tools/aegis_delivery_control/dashboard/index.html
tools/aegis_delivery_control/dashboard/styles.css
tools/aegis_delivery_control/dashboard/app.js
tools/aegis_delivery_control/dashboard/
```

The phrase "cleanup and removal of the project" has no broader verified target
in the conversation. Dashboard removal is complete. No further deletion or
cleanup is authorized, including deletion of cache directories. Do not delete
Project Aegis, `tools/aegis_delivery_control/`, tracked implementation files,
the preserved artifact directories, caches or any remote branch/PR. Ask the
owner before interpreting it more broadly.

## 13. Deviations

- **Unauthorized frontend deviation:** a dashboard was created after accidental
  frontend exploration was mistaken for an active request. This violated the
  resume summary, scope lock and AEGIS-APR-004. It was never connected, staged,
  committed or pushed and has now been removed.
- **Documentation lag:** the docs index still said CP-WP-002 was blocked and the
  package/root status described only earlier C04/C05 milestones. The checkpoint
  commit corrected those statements and records the current `REVISE` gate.
- **Historical pause after final review:** the three stop findings were initially
  preserved rather than patched without a new plan audit because the user
  requested a pause and handoff. Stages 4 and 5 subsequently corrected
  R-STOP-01 and R-STOP-02 only after their plan audits returned `APPROVE`.
- **Validation-command correction:** the first custom Markdown link audit used
  an empty parent path for root-level files and emitted PowerShell `Join-Path`/
  `Test-Path` errors. No pass was claimed from it; the corrected command checked
  103 local links successfully after the final audit corrections.
- **Unavailable generic test runner:** a Stage 5 attempt to invoke
  `python -m pytest scripts/tests -q` failed because `pytest` is not installed.
  No dependency was added. The repository-native
  `python scripts/tests/test_validator.py` completed all 91 self-test assertions,
  and the delivery-control suite uses `unittest` as recorded above.
- **Large accumulated diff:** `ba13394` is a 15-file checkpoint of work developed
  across prior stages. It is intentionally a draft recovery point, not an ideal
  review-sized completion commit.

## 14. Intentionally not done / omitted

- R-STOP-01, R-STOP-02, R-STOP-03, T13, T15, T05, T06, T09, T28/F01,
  cross-family F05/F06/F13/F20, the narrow T07
  local-nonexecution slice, T08 validation-pause slice, T14 core/T09-source
  slices, and all ordered T17 validator-result, operation-uncertainty,
  verified-receipt, authoritative-nonexecution and safe-retry slices are
  independently accepted as recorded in Stages 4-18. Complete T07/T08/T14 and
  the accumulated T17 row remain UNVERIFIED pending T24/other source families
  or their exact-head trace, and later final review gates remain.
- T05 performs no cancel/drain contact. T06 performs no observe/cancel/retry and
  treats bare contact as reconciliation uncertainty. T07 accepts only an exact
  T05 plus authoritative T25 nonexecution source; it is not inferred from a
  pause request. T08 adds no adapter cancellation or drain side effect. T09
  retains reconciliation uncertainty and performs no adapter call. The T17
  foundation derives and preserves uncertainty; the verified-receipt route now
  resolves only its exact proof-covered set. The authoritative-nonexecution and
  safe-retry slice adds no real adapter, authority or provider integration.
- No complete T01-T28/C01-C09/F01-F21 exact-head mapping was claimed.
- No full platform matrix or final hosted check result is claimed in this
  document unless PR #99 later records it.
- No independent final architecture, security or QA approval exists for the
  accumulated checkpoint.
- No merge, release, deployment, provider call, production-data operation,
  external integration or real authority/adapter work was performed.

## 15. Next entry criterion

Codex may continue only after each cold-start preflight matches this handoff and
the next backlog item's narrow plan has independently passed review. All three
stop findings, T13, T15, T05, T06 and the reviewed T07/T08/T14 slices are accepted.
T09 and the narrow T17 validator-result/T14 T09-source slice are also
independently accepted, as are the T17 operation-uncertainty foundation and
verified-receipt route and the authoritative-nonexecution/safe-retry slice. The
T22 terminal-restart report, T28/F01 verified-effect adoption and cross-family
F05/F06/F13/F20 are also independently accepted. Filesystem ownership/reparse/
path-swap protection is independently accepted on Windows; POSIX runtime remains
`UNVERIFIED`. The corrected pre-commit diff has independent architecture,
security and QA `APPROVE`. The next gates are exact committed-head/hosted
confirmation and the final trace. Keep PR
#99 draft until every remaining backlog and final review gate passes; no merge
or deployment decision is currently due.
