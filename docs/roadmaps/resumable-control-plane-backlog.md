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

Peter's current explicit CP-WP-001 authorization permits exactly three documents,
the focused branch, DCO-signed commits, one PR, existing CI and in-scope corrections.
Runtime stays excluded. The 2026-09-13 owner continuation now permits commit/push/merge
of PR #95; AEGIS-APR-001 and standing administrator-merge grant AEGIS-APR-002 apply.
The task authorization source and bounded summary are in the evidence document.
The current correction instruction continues PR #95 on this same branch: address
all original and subsequent GitHub findings, reply/resolve only after pushing evidence, request a fresh
exact-head Codex review and monitor it plus all CI. No second branch or PR is allowed.

Status vocabulary: AUTHORIZED = the human granted the exact package;
READY_FOR_OWNER_REVIEW = scoped delivery evidence exists, acceptance still pending;
BLOCKED = entry conditions/authority absent; DONE = owner disposition and required
delivery evidence recorded. No automatic phase advancement or implicit authorization.
Do not silently delete/relabel history; later dispositions cite evidence and scope.

## 2. CP-WP-001 contract

| Field | Contract |
| --- | --- |
| ID / title | CP-WP-001 — Durable State, Authority and Recovery Contract |
| Status | AUTHORIZED for documentation delivery and merge after required review/CI; no implementation |
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
| Next owner decision | After CP-WP-001 delivery, decide whether to authorize a separately scoped CP-WP-002; no automatic advancement |

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

## 3. CP-WP-001 exact file plan

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

## 4. Validation and delivery protocol

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
| CP-WP-002 — Offline state and recovery kernel | BLOCKED: accepted CP-WP-001, separate explicit authorization naming exact source/files, selected storage/crash model, budget lifecycle, synthetic freshness source and synthetic-only adapters | Independent synthetic T01–T28/C01–C09/F01–F21 tests, including F04a/F04b; complete lifecycle traces, observation/apply identity, slot/replay/budget/freshness and terminal validation evidence; synthetic authority cannot enable a real adapter |
| CP-WP-003 — Authority, evidence and execution capability contracts | BLOCKED: separate scope/approval, source-atomic approval claims/redemption including manual consumers, independent monotonic anchor or complete reconciliation, verified containment/fencing, evidence and bounded-liability accounting | Negative authority/race/rollback/path/process/receipt/billing probes; unavailable guarantees deny real dispatch; no live deployment/provider call without separately named grant |
| CP-WP-004 — One bounded delivery integration | BLOCKED: chosen integration, owner authority, idempotency/receipt/rollback semantics, source/evidence/budget pins and proven CP-WP-003 prerequisites | Exact-operation evidence and reviewed outcome; no automatic promotion to broad delivery or BER execution |
| CP-FUT-001 — Distributed ownership or hosted service | BLOCKED: demonstrated need and separate architecture/security/cost approval | Distributed fencing/failover/identity design and capability proof; local locks/checkpoints never satisfy it |

No later package is authorized by this register or by CP-WP-001 acceptance. BER
integration, if requested, additionally follows BER's current phase/evidence gates.

### 5.1 Provisional offline-kernel file plan

This is a planning estimate, not an authorized file set or storage decision.
All paths are new except the noted backlog update. Logical interfaces can share
modules; do not create services or extract BER just to match a diagram.

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
