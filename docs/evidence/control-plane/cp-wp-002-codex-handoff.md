# CP-WP-002 Codex continuation handoff

Date: 2026-09-21
Repository: `ModernNomad-98/Project-Aegis` (Role A source library)
Branch: `feat/cp-wp-002-offline-kernel`
Base: `main` at `497a4529b84ec223245e001213271a9266514f62`
Implementation checkpoint: `ba133941a5ae897b6202fa9788b183da28b3f12a`
Draft PR: [#99](https://github.com/ModernNomad-98/Project-Aegis/pull/99)
Status: **PAUSED - NOT MERGE-READY - INDEPENDENT REVIEW VERDICT `REVISE`**

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

Do not stage, delete, broadly inspect or add ignore rules for the artifact
directories. The cache directories are generated local state and were not added
to the checkpoint; do not stage them.

## 2. Source precedence

Use this order when sources disagree:

1. the user's current direct instruction;
2. the effective lifecycle in the approval register;
3. this handoff for the exact paused checkpoint and deviations;
4. the canonical design for required CP-D/T/C/F behavior;
5. the durable backlog for work-package status and completion gates;
6. current code and tests for what is implemented now;
7. merged history;
8. old chat, summaries and memory only as labeled context.

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
- PR #99 is open, draft and blocked;
- no CP-WP-002 commit is on `main`;
- the GitHub deployments API returned `[]`;
- `gh release list` returned `no releases found`;
- no software deployment or release occurred; and
- administrator-merge pre-approval is carried forward but must not be exercised
  while the independent gate is `REVISE` or required checks are unresolved.

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

## 6. Proven invocations

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
| `gh api "repos/ModernNomad-98/Project-Aegis/deployments?per_page=100"` | `[]` |
| `gh release list --repo ModernNomad-98/Project-Aegis --limit 20` | `no releases found` |
| Dashboard cleanup verification | `Test-Path tools/aegis_delivery_control/dashboard` returned `False`; dashboard absent from `git status` |
| Local-link audit over the five updated Markdown files | 100 local Markdown links checked; all targets exist |
| `python -B scripts/validate-skills.py` | `OK: 184 skill(s) valid, 0 warning(s)` |
| `python -B scripts/tests/test_validator.py` | `OK: 91 gate self-test assertion(s) passed.` |

The independent stop reviewer was read-only and did not execute tests. Its
findings are code-review evidence, not an executable test receipt.

## 7. Independent stop gate - `REVISE`

The stop gate must be corrected before any later backlog slice or merge.

### R-STOP-01 - BLOCKER - terminal slot can be stranded

STOP can be entered from `BLOCKED/FINALIZING` or recoverable validation-failure
state while retaining the repository slot. T16 is unavailable after `STOPPED`,
and T26 rejects an already-settled validator intent. New intents remain denied
while the slot exists.

Review anchors:

- [`storage.py`](../../../tools/aegis_delivery_control/storage.py#L409)
- [`engine.py`](../../../tools/aegis_delivery_control/engine.py#L49)
- [`storage.py`](../../../tools/aegis_delivery_control/storage.py#L4248)
- [`storage.py`](../../../tools/aegis_delivery_control/storage.py#L7842)
- [`storage.py`](../../../tools/aegis_delivery_control/storage.py#L8384)
- [`storage.py`](../../../tools/aegis_delivery_control/storage.py#L8833)

Required correction: add a T26-compatible terminal closure by reference to
already-applied validation evidence. Release the slot atomically only after all
accounting and check obligations are closed. Test both predecessor states,
crash/replay and unrelated-run dispatch after closure.

### R-STOP-02 - MAJOR - T20 is declaration-only

T20 exists in the registry but has no typed escalation request,
coordinator/storage operation, registered `STOP_ESCALATED` event,
projection/recovery validation or tests. A persisted graceful deadline cannot
currently produce the canonical auditable escalation.

Review anchors:

- [`engine.py`](../../../tools/aegis_delivery_control/engine.py#L51)
- [`contracts.py`](../../../tools/aegis_delivery_control/contracts.py#L681)
- [`storage.py`](../../../tools/aegis_delivery_control/storage.py#L4263)
- [canonical T20](../../design/resumable-control-plane-v1.md#L447)

Required correction: implement a typed, idempotent T20 transaction bound to the
original graceful stop and deadline, with outstanding-obligation and deadline
checks, recovery validation, tamper tests and both commit-boundary crash tests.

Source conflict to resolve explicitly before editing: one prior transient session
note said "T20 remains excluded", while the canonical design, AEGIS-APR-004's
complete T01-T28 scope and the current independent stop gate require T20. The
durable sources authorize T20, but do not silently decide its sequencing. Record
the plan-audit resolution; do not treat the old note as a superseding decision.

### R-STOP-03 - MAJOR - post-contact uncertainty is underclassified

Adapter contact is durably claimed before target execution, creating a window in
which effect outcome and billing are unknown. Immediate stop currently records
stop/fence/state but does not atomically classify that bounded exposure as
`UNKNOWN_WORST_CASE_CHARGED`.

Review anchors:

- [`adapters.py`](../../../tools/aegis_delivery_control/adapters.py#L448)
- [`storage.py`](../../../tools/aegis_delivery_control/storage.py#L4218)
- [canonical T19](../../design/resumable-control-plane-v1.md#L446)

Required correction: atomically preserve the obligation and worst-case charge
when stop observes post-contact/pre-receipt uncertainty. Add late authoritative
usage correction, replay, tamper and crash-boundary tests.

## 8. Backlog state

Canonical obligations remain T01-T28, C01-C09 and F01-F21. Do not infer a family
complete from the 198 passing tests, a registry entry or an earlier milestone
paragraph. No complete exact-head traceability audit was performed at this
checkpoint.

Immediate order:

1. R-STOP-01 terminal slot closure.
2. R-STOP-02 T20 scope/sequence reconciliation, then implementation if the
   plan audit confirms the durable-source reading above.
3. R-STOP-03 post-contact worst-case accounting.
4. Focused stop tests, complete 198-test package suite, integrity diagnostics and
   a fresh independent stop review.
5. Do not proceed until that reviewer returns `APPROVE` with no blocker/major
   finding.

Prior-session routing context for work after stop approval was:

1. T13/T15/T14.
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

## 9. Continuation protocol

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

## 10. Cleanup and removal contract

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
in the conversation. Do not delete Project Aegis, `tools/aegis_delivery_control/`,
tracked implementation files, the preserved artifact directories or any remote
branch/PR. Ask the owner before interpreting it more broadly.

## 11. Deviations

- **Unauthorized frontend deviation:** a dashboard was created after accidental
  frontend exploration was mistaken for an active request. This violated the
  resume summary, scope lock and AEGIS-APR-004. It was never connected, staged,
  committed or pushed and has now been removed.
- **Documentation lag:** the docs index still said CP-WP-002 was blocked and the
  package/root status described only earlier C04/C05 milestones. The checkpoint
  commit corrected those statements and records the current `REVISE` gate.
- **No implementation correction after final review:** the three stop findings
  were preserved rather than patched without a new plan audit because the user
  requested a pause and handoff.
- **Validation-command correction:** the first custom Markdown link audit used
  an empty parent path for root-level files and emitted PowerShell `Join-Path`/
  `Test-Path` errors. No pass was claimed from it; the corrected command checked
  100 local links successfully.
- **Large accumulated diff:** `ba13394` is a 15-file checkpoint of work developed
  across prior stages. It is intentionally a draft recovery point, not an ideal
  review-sized completion commit.

## 12. Intentionally not done / omitted

- The three stop findings were not fixed after the user requested pause.
- No complete T01-T28/C01-C09/F01-F21 exact-head mapping was claimed.
- No full platform matrix or final hosted check result is claimed in this
  document unless PR #99 later records it.
- No independent final architecture, security or QA approval exists for the
  accumulated checkpoint.
- No merge, release, deployment, provider call, production-data operation,
  external integration or real authority/adapter work was performed.

## 13. Next entry criterion

Codex may resume implementation only after the cold-start preflight matches this
handoff and the first stop-fix plan has been independently audited. The next code
change is R-STOP-01, not dashboard work and not a later T/C/F family. The next
delivery decision is to keep PR #99 draft until the stop review returns
`APPROVE`; no merge or deployment decision is currently due.