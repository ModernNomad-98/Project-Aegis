# CP-WP-002 Codex continuation handoff

Date: 2026-09-21
Repository: `ModernNomad-98/Project-Aegis` (Role A source library)
Branch: `feat/cp-wp-002-offline-kernel`
Base: `main` at `497a4529b84ec223245e001213271a9266514f62`
Implementation checkpoint: `ba133941a5ae897b6202fa9788b183da28b3f12a`
First handoff checkpoint: `8456a369b64dc3f6ef87e4423a8e877ed0525316`
Draft PR: [#99](https://github.com/ModernNomad-98/Project-Aegis/pull/99)
Status: **IN PROGRESS - NOT MERGE-READY - R-STOP-01/02/03 AND AGGREGATE STOP GATE `APPROVE`**

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
| Current user instruction | Pause, save progress, synchronize GitHub/documentation, create this Codex handoff, and carry current rules/backlogs/pre-approval without assumption | Deleting the repository or delivery-control package; inventing new authority |

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
C08/F03 traceability remains `UNVERIFIED`. Commit/push and exact-head hosted
evidence remain pending until this reviewed stage is committed.

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
complete from the 242 passing tests, a registry entry or an earlier milestone
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
| T05 | UNVERIFIED | UNVERIFIED | UNVERIFIED | Later ordered backlog |
| T06 | UNVERIFIED | UNVERIFIED | UNVERIFIED | Later ordered backlog |
| T07 | UNVERIFIED | UNVERIFIED | UNVERIFIED | Later ordered backlog |
| T08 | UNVERIFIED | UNVERIFIED | UNVERIFIED | Later ordered backlog |
| T09 | UNVERIFIED | UNVERIFIED | UNVERIFIED | Later ordered backlog |
| T10 | UNVERIFIED | UNVERIFIED | UNVERIFIED | Exact-head trace required |
| T11 | UNVERIFIED | UNVERIFIED | UNVERIFIED | Historical validation work only |
| T12 | UNVERIFIED | UNVERIFIED | UNVERIFIED | Historical validation work only |
| T13 | YES | YES | YES | Typed lifecycle facts, grant-wide denial, exact own-use continuation, typed supersession and correction independently accepted |
| T14 | UNVERIFIED | UNVERIFIED | UNVERIFIED | Later ordered backlog |
| T15 | UNVERIFIED | UNVERIFIED | UNVERIFIED | Later ordered backlog |
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
| C03 | UNVERIFIED | UNVERIFIED | UNVERIFIED | Exact-head trace required |
| C04 | UNVERIFIED | UNVERIFIED | UNVERIFIED | Earlier slice accepted; accumulated exact head not re-audited |
| C05 | UNVERIFIED | UNVERIFIED | UNVERIFIED | Earlier slice accepted; accumulated exact head not re-audited |
| C06 | UNVERIFIED | UNVERIFIED | UNVERIFIED | Exact-head trace required |
| C07 | UNVERIFIED | UNVERIFIED | UNVERIFIED | Exact-head trace required |
| C08 | UNVERIFIED | UNVERIFIED | UNVERIFIED | T13 lifecycle/unknown-claim slice accepted; complete atomic-claim trace remains |
| C09 | UNVERIFIED | UNVERIFIED | UNVERIFIED | Earlier slice evidence exists; accumulated exact head not re-audited |

### F01-F21 acceptance-family matrix

Canonical rows: [design acceptance families](../../design/resumable-control-plane-v1.md#L939-L960).

| ID | Implemented | Tested | Independently accepted | Current disposition / evidence |
| --- | --- | --- | --- | --- |
| F01 | UNVERIFIED | UNVERIFIED | UNVERIFIED | Later ordered with T28 |
| F02 | UNVERIFIED | UNVERIFIED | UNVERIFIED | Later ordered with T17 |
| F03 | UNVERIFIED | UNVERIFIED | UNVERIFIED | T13 lifecycle/supersession/correction slice accepted; full family trace remains |
| F04a | UNVERIFIED | UNVERIFIED | UNVERIFIED | Exact-head accounting trace required |
| F04b | UNVERIFIED | UNVERIFIED | UNVERIFIED | Stop accounting slices accepted; full family trace remains |
| F05 | UNVERIFIED | UNVERIFIED | UNVERIFIED | Later cross-family backlog |
| F06 | UNVERIFIED | UNVERIFIED | UNVERIFIED | R-STOP-01 global-slot slice accepted; full family trace remains |
| F07 | UNVERIFIED | UNVERIFIED | UNVERIFIED | Historical focused evidence only |
| F08 | UNVERIFIED | UNVERIFIED | UNVERIFIED | R-STOP-03 post-contact/late-adjustment slice accepted; full family trace remains |
| F09 | UNVERIFIED | UNVERIFIED | UNVERIFIED | R-STOP-01 terminal-closure slice accepted; full family trace remains |
| F10 | UNVERIFIED | UNVERIFIED | UNVERIFIED | Exact-head trace required |
| F11 | UNVERIFIED | UNVERIFIED | UNVERIFIED | Later ordered with T17 |
| F12 | UNVERIFIED | UNVERIFIED | UNVERIFIED | Later ordered with T17 |
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

1. T15, then T14 (T13 complete and independently accepted).
2. T05-T09.
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

- R-STOP-01, R-STOP-02 and R-STOP-03 are independently accepted as recorded in
  Stages 4-6; later exact-head backlog and final review gates remain.
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
stop findings and T13 are complete. The next code change follows the documented
order at T15, then T14, not dashboard work. Keep PR #99 draft until every remaining backlog
and final review gate passes; no merge or deployment decision is currently due.
