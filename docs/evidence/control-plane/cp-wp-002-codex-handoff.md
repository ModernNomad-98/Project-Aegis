# CP-WP-002 Codex continuation handoff

Date: 2026-09-21
Repository: `ModernNomad-98/Project-Aegis` (Role A source library)
Branch: `feat/cp-wp-002-offline-kernel`
Base: `main` at `497a4529b84ec223245e001213271a9266514f62`
Implementation checkpoint: `ba133941a5ae897b6202fa9788b183da28b3f12a`
First handoff checkpoint: `8456a369b64dc3f6ef87e4423a8e877ed0525316`
Latest reviewed implementation checkpoint: `39b3268adc984e3d0b10e55a42fe37a172229e60`
Draft PR: [#99](https://github.com/ModernNomad-98/Project-Aegis/pull/99)
Status: **IN PROGRESS - NOT MERGE-READY - STOP GATE, T13, T15, T14 CORE SLICE, T05, T06 AND NARROW T07 SLICE `APPROVE`**

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
```

Stage 5's local validator invocation also generated these untracked cache paths;
they are preserved and must likewise not be staged or deleted:

```text
scripts/__pycache__/
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
notices. Commit, push and exact-head hosted-check evidence remain pending until
this reviewed stage is committed. Canonical design, approval register, BER,
dependencies, CI, CLI, adapters, preserved artifact/cache paths, real
authority/adapters and external systems were intentionally untouched. The
validator run added `scripts/ci/__pycache__/` to the preserved untracked cache
set; it was neither deleted nor staged.

T08 remains `UNVERIFIED/UNVERIFIED/UNVERIFIED` as a complete transition because
active drain/cancel and broader T17/T24 cessation sources remain ordered work.
The clean VALIDATING T14 slice is independently accepted, but complete T14 and
the implicated C/F families remain `UNVERIFIED`. T09 is next and PR #99 remains
open, draft and blocked.

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
complete from the 331 passing tests, a registry entry or an earlier milestone
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
| T09 | UNVERIFIED | UNVERIFIED | UNVERIFIED | Later ordered backlog |
| T10 | UNVERIFIED | UNVERIFIED | UNVERIFIED | Exact-head trace required |
| T11 | UNVERIFIED | UNVERIFIED | UNVERIFIED | Historical validation work only |
| T12 | UNVERIFIED | UNVERIFIED | UNVERIFIED | Historical validation work only |
| T13 | YES | YES | YES | Typed lifecycle facts, grant-wide denial, exact own-use continuation, typed supersession and correction independently accepted |
| T14 | UNVERIFIED | UNVERIFIED | UNVERIFIED | PLANNED/BLOCKED, T07 activity-recovery-to-BLOCKED and T08 clean recovery-to-VALIDATING slices independently accepted; other source families remain |
| T15 | YES | YES | YES | Immutable source/item/plan/policy pins, authenticated mismatch evidence, atomic scoped fence and historical activity routing independently accepted |
| T16 | UNVERIFIED | UNVERIFIED | UNVERIFIED | R-STOP-01 no longer blocks terminal closure; full T16 trace remains |
| T17 | UNVERIFIED | UNVERIFIED | UNVERIFIED | Later ordered backlog |
| T18 | YES | YES | YES | Graceful-stop and terminal-closure slices independently accepted |
| T19 | YES | YES | YES | Terminal closure and post-contact uncertainty slices independently accepted |
| T20 | YES | YES | YES | Operator escalation route independently accepted; no deadline-rule scheduler claimed |
| T21 | UNVERIFIED | UNVERIFIED | UNVERIFIED | Exact-head trace required |
| T22 | UNVERIFIED | UNVERIFIED | UNVERIFIED | Later ordered backlog |
| T23 | UNVERIFIED | UNVERIFIED | UNVERIFIED | Stop interaction inspected, not independently accepted |
| T24 | UNVERIFIED | UNVERIFIED | UNVERIFIED | Stop interaction inspected, not independently accepted |
| T25 | UNVERIFIED | UNVERIFIED | UNVERIFIED | Stop interaction inspected, not independently accepted |
| T26 | UNVERIFIED | UNVERIFIED | UNVERIFIED | Applied-evidence closure slice accepted; full T26 trace remains |
| T27 | UNVERIFIED | UNVERIFIED | UNVERIFIED | Exact-head trace required |
| T28 | UNVERIFIED | UNVERIFIED | UNVERIFIED | Later ordered backlog with F01 |

### C01-C09 crash-boundary matrix

Canonical rows: [design crash boundaries](../../design/resumable-control-plane-v1.md#L599-L607).

| ID | Implemented | Tested | Independently accepted | Current disposition / evidence |
| --- | --- | --- | --- | --- |
| C01 | UNVERIFIED | UNVERIFIED | UNVERIFIED | Exact-head trace required |
| C02 | UNVERIFIED | UNVERIFIED | UNVERIFIED | Exact-head trace required |
| C03 | UNVERIFIED | UNVERIFIED | UNVERIFIED | T06 preserves original effect key/slot and worst-case accounting through missing-receipt reconciliation; complete family trace remains |
| C04 | UNVERIFIED | UNVERIFIED | UNVERIFIED | Earlier slice accepted; accumulated exact head not re-audited |
| C05 | UNVERIFIED | UNVERIFIED | UNVERIFIED | Earlier slice accepted; accumulated exact head not re-audited |
| C06 | UNVERIFIED | UNVERIFIED | UNVERIFIED | T05/T06/T07 pre/post-commit rollback/replay, atomic settlement and durable-fence slices accepted; full crash family remains unverified |
| C07 | UNVERIFIED | UNVERIFIED | UNVERIFIED | Exact-head trace required |
| C08 | UNVERIFIED | UNVERIFIED | UNVERIFIED | T13 lifecycle/unknown-claim slice accepted; complete atomic-claim trace remains |
| C09 | UNVERIFIED | UNVERIFIED | UNVERIFIED | Earlier slice evidence exists; accumulated exact head not re-audited |

### F01-F21 acceptance-family matrix

Canonical rows: [design acceptance families](../../design/resumable-control-plane-v1.md#L939-L960).

| ID | Implemented | Tested | Independently accepted | Current disposition / evidence |
| --- | --- | --- | --- | --- |
| F01 | UNVERIFIED | UNVERIFIED | UNVERIFIED | T15 identity/non-mutation boundary slice accepted; full family remains ordered with T28 |
| F02 | UNVERIFIED | UNVERIFIED | UNVERIFIED | Later ordered with T17 |
| F03 | UNVERIFIED | UNVERIFIED | UNVERIFIED | T13 lifecycle/supersession/correction slice accepted; full family trace remains |
| F04a | UNVERIFIED | UNVERIFIED | UNVERIFIED | Exact-head accounting trace required |
| F04b | UNVERIFIED | UNVERIFIED | UNVERIFIED | Stop accounting slices accepted; full family trace remains |
| F05 | UNVERIFIED | UNVERIFIED | UNVERIFIED | Later cross-family backlog |
| F06 | UNVERIFIED | UNVERIFIED | UNVERIFIED | R-STOP-01 plus T05/T06/T07 pause, settlement, slot-retention and serialized contact/receipt slices accepted; full family trace remains |
| F07 | UNVERIFIED | UNVERIFIED | UNVERIFIED | T06 unknown late-receipt retention/worst-case reconciliation slice accepted; full family trace remains |
| F08 | UNVERIFIED | UNVERIFIED | UNVERIFIED | R-STOP-03 and T06 post-contact/late-adjustment slices accepted; full family trace remains |
| F09 | UNVERIFIED | UNVERIFIED | UNVERIFIED | R-STOP-01 terminal-closure slice accepted; full family trace remains |
| F10 | UNVERIFIED | UNVERIFIED | UNVERIFIED | Exact-head trace required |
| F11 | UNVERIFIED | UNVERIFIED | UNVERIFIED | Later ordered with T17 |
| F12 | UNVERIFIED | UNVERIFIED | UNVERIFIED | T07 local-nonexecution PAUSED/recovery slice accepted; validator nonlaunch and T17 completion remain |
| F13 | UNVERIFIED | UNVERIFIED | UNVERIFIED | Later cross-family backlog |
| F14 | UNVERIFIED | UNVERIFIED | UNVERIFIED | R-STOP-01 recoverable-failure stop slice accepted; full trace remains |
| F15 | UNVERIFIED | UNVERIFIED | UNVERIFIED | Exact-head trace required |
| F16 | UNVERIFIED | UNVERIFIED | UNVERIFIED | Exact-head trace required |
| F17 | UNVERIFIED | UNVERIFIED | UNVERIFIED | Exact-head trace required |
| F18 | UNVERIFIED | UNVERIFIED | UNVERIFIED | R-STOP-01 terminal closure slice accepted; full family trace remains |
| F19 | UNVERIFIED | UNVERIFIED | UNVERIFIED | Exact-head trace required |
| F20 | UNVERIFIED | UNVERIFIED | UNVERIFIED | Later cross-family backlog |
| F21 | UNVERIFIED | UNVERIFIED | UNVERIFIED | Later ordered with T17 |

Immediate order:

1. R-STOP-01 terminal slot closure - complete; independent `APPROVE`.
2. R-STOP-02 T20 graceful-stop escalation - complete; independent `APPROVE`.
3. R-STOP-03 post-contact worst-case accounting - complete; independent
   `APPROVE`.
4. Aggregate stop gate - complete; independent `APPROVE`.

Prior-session routing context for work after stop approval was:

1. T15, T05 and T06 complete and independently accepted; T07 local-nonexecution, T08 validation-pause and T14 core slices accepted with the complete transitions still UNVERIFIED pending T17/T24 and other source families.
2. T09 next.
3. T17 with F02/F11/F12/F21.
4. T22.
5. T28 with F01.
6. Cross-family F05/F06/F13/F20.
7. Documentation refresh.
8. Full repository validation.
9. Independent architecture, security and QA reviews.
10. Commit, push, PR update and administrator merge only after all gates pass.

This later order is recovered session context, not a superseding design record.
Before each item, compare it with the current backlog, design and actual diff.
Any mismatch triggers source reconciliation, not silent reordering. Earlier
milestones C04, C05 and C09 have historical focused evidence in the backlog, but
the accumulated exact-head implementation still requires final cross-family
review. Filesystem ownership, reparse/path-swap protection and complete
transition/acceptance mapping remain open until proven otherwise.

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

- R-STOP-01, R-STOP-02, R-STOP-03, T13, T15, T05, T06, the narrow T07
  local-nonexecution slice, T08 validation-pause slice and T14 core slices are
  independently accepted as recorded in Stages 4-13; complete T07/T08/T14
  remain UNVERIFIED pending T17/T24 and other source families, and later exact-head/final
  review gates remain.
- T05 performs no cancel/drain contact. T06 performs no observe/cancel/retry and
  treats bare contact as reconciliation uncertainty. T07 accepts only an exact
  T05 plus authoritative T25 nonexecution source; it is not inferred from a
  pause request. T08 adds no adapter cancellation or drain side effect. T09 is
  the next ordered work.
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
The next code change follows the documented order at T09. Keep PR #99 draft until every remaining backlog
and final review gate passes; no merge or deployment decision is currently due.
