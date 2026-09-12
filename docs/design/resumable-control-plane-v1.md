# Resumable Aegis delivery control plane — v1 contract

Status: DESIGN PROPOSAL FOR OWNER REVIEW; CP-WP-001 documentation only.
Owner: Peter Nguyen. Repository: ModernNomad-98/Project-Aegis.
Inspected base: `57e6928d2849aa5377daf52c723b85736292585d` (2026-09-12).

This document specifies future behavior; no controller, runtime schema, policy,
adapter or execution authority is delivered. MUST and MUST NOT express proposed
acceptance requirements, not instructions to execute them. Approval to author or
merge this document does not authorize implementation or any delivery action.

Continuation: [separate backlog](../roadmaps/resumable-control-plane-backlog.md).
Verification: [CP-WP-001 evidence](../evidence/control-plane/cp-wp-001-review.md).

## 1. Purpose, boundaries and authority

The future product coordinates governed software delivery that can pause and
continue across process restarts without losing decisions, repeating uncertain
effects or treating stale approvals as current. Its first implementation target
would be an offline, single-host kernel with synthetic adapters only.

Forces, in order: preserve authority and evidence; prevent duplicate effects;
make recovery decisions explicit; keep the first increment reviewable; defer
distribution and optimization until demonstrated demand.

### 1.1 Role A and Role B

Apply [AGENTS.md](../../AGENTS.md) before acting. Role A requires the README title,
catalog, validator and audit-baseline landmarks, not copied startup files alone.
This checkout meets those requirements. Role B is a consumer/product repository
using copied Aegis skills. Its work, owners, approvals, evidence and repository
identity are separate; source-library grants never transfer by copying files.
A future controller must bind each target repository explicitly and reject
cross-project work/approval/receipt substitutions. No consumer repository is
created or selected by this work package.

### 1.2 Separation from BER

The [BER parent design](behavioral-eval-runner-v1.md) owns BER architecture,
controls and evidence. Its [successor](behavioral-eval-runner-v1-fast-track-successor.md)
supersedes only its stated scope. The [BER backlog](../roadmaps/behavioral-eval-runner-backlog.md)
owns BER continuation, including current WP-2B-3 authorization and unfinished
measured acceptance. Current notices supersede historical statements that no
implementation exists or that BER-DEC-008 has not yet taken effect.

At this base, BER engineering and offline CI are delivered; original calibration
inputs are missing, replacement approvals and measured calibration remain open,
OD-1 is unratified and WP-2B-4 is blocked. No result here advances those gates.
BER's own use of "control plane" does not establish a delivery controller.
BER-BKL-015 describes optional BER evidence consumers, not ownership of this stream.
Any future BER adapter must respect BER's own authority and consume verified
evidence without changing it. This stream never edits the BER backlog implicitly.

### 1.3 Approval sources

The complete [owner register](../approvals/APPROVAL_REGISTER.md) currently contains
active AEGIS-APR-001 (read-only agents) and AEGIS-APR-002 (administrator merges),
with no later lifecycle entries. Neither starts unrelated implementation.
The current direct CP-WP-001 instruction authorizes three documents and one PR,
and explicitly stops before merge. That narrower boundary governs this task.
The register remains the one documentary approval register; these documents link
to it and record task evidence, not a competing source of general grants.

### 1.4 Non-goals

No executable controller, schemas, policy, model dispatch, credential handling,
real execution adapter, CI wiring, dependency, database, deployment, release,
tag, automatic merge, multi-host execution, dashboard or BER behavior change.
No claim of live containment, measured calibration or exactly-once external effects.

## 2. Current implementation and reuse dispositions

Paths in this table are under `tools/behavioral_eval_runner/`; tests are under its
`tests/`. Each primitive has exactly one disposition for the stated proposed use.
All reuse, wrapping and corrections are later work. None occurs in CP-WP-001.
No physical extraction is justified now; an interface can precede extraction.

| Primitive / current responsibility | Classification | Proposed use / seam | Coupling and platform limits | Protecting tests / change ownership |
| --- | --- | --- | --- | --- |
| [canonical.py](../../tools/behavioral_eval_runner/canonical.py): deterministic JSON and SHA-256 | REUSE AS-IS | Import unchanged byte/hash functions behind a versioned Python serialization contract; new identities use integers/strings | BER exception; finite floats accepted, not a cross-language numeric-normalization standard; file hashing has no containment | `test_canonical.py`; add controller golden-byte tests in CP-WP-002; no BER change |
| [identity.py](../../tools/behavioral_eval_runner/identity.py): case/assertion/repetition IDs | BER-SPECIFIC — DO NOT REUSE | New project/item/run/effect identity contract | BER kinds, assertion positions and repetition semantics; no OS dependence identified | `test_identity.py` retained; new controller tests; BER modification nowhere |
| [pathsafe.py](../../tools/behavioral_eval_runner/pathsafe.py): lexical paths and separate reparse checks | WRAP BEHIND A NEW INTERFACE | Future owned-path checked-I/O interface | `safe_join` does not invoke reparse checkers despite its docstring; check-before-open races remain; Windows ADS/device rules are useful | `test_pathsafe.py`; add ancestor/swap/capability tests in CP-WP-002; no BER edit |
| [preflight.py](../../tools/behavioral_eval_runner/preflight.py): eval prerequisites | BER-SPECIFIC — DO NOT REUSE | Borrow honest missing-prerequisite blocking, build independent readiness | Case/fixture/invocation/verdict coupling; declared capabilities are not host proof | `test_preflight.py` retained; new readiness tests; BER modification nowhere |
| [process_control.py](../../tools/behavioral_eval_runner/process_control.py): timeouts and process cleanup | WRAP BEHIND A NEW INTERFACE | Later execution adapter exposes measured cleanup capability | Windows post-leader descendant reaping unavailable; termination does not revoke grants or cancel remote effects | `test_process_control.py`; CP-WP-003 capability probes before real use |
| [scheduler.py](../../tools/behavioral_eval_runner/scheduler.py): deterministic BER ordering | BER-SPECIFIC — DO NOT REUSE | Initially follow explicit dependency order; no priority scheduler | Case risk/identity/reverse-edge coupling; scheduler produces evidence, not dispatch | `test_scheduler.py` retained; independent dependency tests; modification nowhere |
| [budget.py](../../tools/behavioral_eval_runner/budget.py): reservation/replay/kill state | REQUIRES CORRECTION BEFORE REUSE | Accounting invariants only until integrated with one atomic intent transaction | Thread lock, separate fsynced ledger and checkpoint replacement; intervening crash can block replay; joint rewrite defeats authenticity | `test_budget.py`; CP-WP-003 accounting decision/correction or separate implementation; no direct kernel dependency |
| [calibration_ledger.py](../../tools/behavioral_eval_runner/judge/calibration_ledger.py): durable calibration accounting | BER-SPECIFIC — DO NOT REUSE | Precedent for durable intent and orphan refusal | BER authorization/model/SDK/prices/caps/stages pinned; local file/lock assumptions | `test_calibration_ledger.py`, `test_calibration_first_live_corrections.py`; new journal tests in CP-WP-002; no BER modification |
| [calibration_development_driver.py](../../tools/behavioral_eval_runner/judge/calibration_development_driver.py): bound calibration orchestration | BER-SPECIFIC — DO NOT REUSE | Reference exact-identity resume and terminal/orphan gates | Dataset/model/approval/provider coupling; cooperative single-host lock | `test_calibration_development_driver.py`; independent engine in CP-WP-002; no BER modification |
| [calibration_io.py](../../tools/behavioral_eval_runner/judge/calibration_io.py): checked I/O and process lock | WRAP BEHIND A NEW INTERFACE | Owned storage/lease interface | BER errors; local cooperative lock, not distributed fencing; checked paths alone do not prove every race prevented | `test_calibration_phase01.py`, driver tests; new multiprocess/platform tests in CP-WP-002 |
| [evidence.py](../../tools/behavioral_eval_runner/evidence.py): manifests and finalization | REQUIRES CORRECTION BEFORE REUSE | Controller evidence contract first; generalized writer only after review | Hardcoded BER schema, access policy and final-report 30-day retention; Windows swap protection detection-only; not a journal | `test_evidence.py`, `test_group_bcde.py`, `test_hardening.py`; CP-WP-003 correction or independent writer |
| [approval_lifecycle.py](../../tools/behavioral_eval_runner/graders/approval_lifecycle.py): grades recorded approvals | BER-SPECIFIC — DO NOT REUSE | Borrow lifecycle rules and abuse cases | Explicitly not an authorization service/consent authenticator | `test_approval_lifecycle.py`; independent verifier; BER modification nowhere |
| Materializer, runtime surface, execution profile, containment | BER-SPECIFIC — DO NOT REUSE | Reference safety requirements for later adapter design | BER corpus/fixtures/profiles; live host guarantees not proven by code presence | Corresponding materialize/runtime/profile/containment suites retained; CP-WP-003 independent capability work |
| Models, enums, aggregation, reporting | BER-SPECIFIC — DO NOT REUSE | New delivery states and reports | BER attempt/quorum/coverage meanings are not delivery completion | Existing model/aggregation/report suites retained; new controller records; modification nowhere |
| [schemas](../../tools/behavioral_eval_runner/schemas): run, attempt, case, profile, materialization, evidence, grading and calibration | BER-SPECIFIC — DO NOT REUSE | Closed/versioned-record precedents only | BER namespace and meanings; schemas cannot authenticate grants, ensure durability or enforce paths | `test_grading_schemas.py` and procedural evidence/calibration tests; new runtime schemas only under later authorization |
| Existing BER automated suites | REUSE AS-IS | Unchanged regression coverage if pure helpers are later imported | BER fixtures/history/platform prerequisites; skips remain gaps | Existing CI owns execution; no CP-WP-001 edits or claims that controller tests ran |
| BER fixtures and test helpers | BER-SPECIFIC — DO NOT REUSE | Independent synthetic controller fixtures | BER expected outcomes/approval assumptions; sealed holdouts inaccessible | New CP-WP-002 fixtures only; BER modification nowhere |

The [runner README](../../tools/behavioral_eval_runner/README.md) distinguishes
offline implementation from unavailable/unknown real-host R1–R5 evidence.
Fail-closed restart refusal is useful precedent, not automatic workflow recovery.

## 3. Names, alternatives and decision register

No exact tracked collision was found for the four candidates at the inspected base.
This is not a public package-name reservation.

| Candidate | Assessment |
| --- | --- |
| `tools/aegis_control_plane` | Architectural fit, but "control plane" already names BER internals |
| `tools/aegis_controller` | Vague delivery scope; suggests one controller rather than bounded interfaces |
| `tools/aegis_runner` | Confusing with Behavioral Eval Runner; understates authority and recovery |
| `tools/aegis_delivery_control` | Recommended separate governed-delivery namespace |

Eventual command: `python -m tools.aegis_delivery_control`, following BER's module
entry convention. No installed console script or packaging dependency is implied.

| Decision | Proposed rule | Reversal condition |
| --- | --- | --- |
| CP-D01 | Independent stream and namespace; BER unchanged | Explicit owner-reviewed integration design |
| CP-D02 | One host/owner and one repository-wide outstanding synthetic operation; atomic slot guard across items/runs, independent of lock | Demonstrated need plus separately approved multi-operation/distributed design |
| CP-D03 | Authority and state transitions deterministic; workers untrusted | Not relaxable by worker output or implementation convenience |
| CP-D04 | Unknown effects remain non-dispatching; proof-free owner disposition can only stop/final-fail/report | Authoritative nonexecution proof or separately reviewed safe retry using the original effect identity; never owner risk acceptance alone |
| CP-D05 | Storage interface before selecting implementation | CP-WP-002 authorization must name selected storage and crash model |
| CP-D06 | Terminal state never reopens; later evidence may settle obligations | New explicitly authorized run/item revision, preserving predecessor history |
| CP-D07 | Imported state needs independent monotonic freshness proof or complete authoritative reconciliation before dispatch | No self-consistent chain or inactive-host exception |
| CP-D08 | Effect dedup key excludes item/run/source/plan/policy revisions; immutable logical-effect binding survives them | Different/repeated/compensating effect needs explicit new-ID approval and durable predecessor disposition |
| CP-D09 | External one-use grants require atomic claim/consume at the trusted source; local reservation is not authority | Real dispatch denied when source or any consuming path cannot enforce it |
| CP-D10 | Versioned budget settlements retain honest usage and worst-case uncertainty across terminals/restarts | Only authoritative settlement evidence changes held/charged totals; no implicit refund/reset |

These IDs are proposal decisions, not granted execution permissions. A later
accepted change names superseded decisions and reasons rather than silently
rewriting the continuation assumptions.

Contract-first adds no runtime cost and keeps reversal to document edits. An
immediate offline kernel gives executable evidence sooner but commits to storage
before recovery semantics are reviewed. A hosted workflow service adds deployment,
identity, cost and operational scope. Choose contract-first; revisit only after
owner acceptance. Then ship independently reviewable offline, capability and
integration packages, each with its own stop point in the separate backlog.

## 4. Components, ownership and trust boundaries

These are logical interfaces, not eleven services. Only the durable-state owner
writes authoritative events. Other writes below are immutable evidence or disposable
projections. Requests to append are validated by the engine and state owner.

| Component | Trusted/untrusted inputs | Reads | Writes | May request | Cannot possess | Failure behavior / evidence |
| --- | --- | --- | --- | --- | --- | --- |
| Operator interface | Authenticated identity; command payload still untrusted | Sanitized status/proposals | No direct authoritative writes | Accept plan, pause, resume, stop, review | A CLI flag cannot create consent | Reject invalid identity/payload; command ID, actor proof reference, disposition |
| Deterministic transition/authority engine | Validated commands; untrusted observations | Verified state, item, policy, verifier result | Event transactions through owner | Allowed transition and bounded operation | Cannot invent grants or remove gates | Deny unknowns; record predicates, versions and reasons |
| Single durable-state owner | Typed transactions with expected head | Project catalog, outstanding slot, journals and accounting | Authoritative catalog/journals/slot and budget/use records | Atomic intent/settlement acknowledgement | Cannot turn local use reservation into an external atomic claim | Project lock/I/O/integrity/freshness failure closes dispatch; committed sequence/hash receipt |
| Work-item repository | Proposed content untrusted until accepted/pinned | Immutable definitions/dependencies | New revisions through owner | Acceptance/supersession review | Cannot approve its proposals or dispatch | Reject cycles/mismatch; definition digest/provenance |
| Approval verifier | Human evidence and atomic-claim receipt from trusted source; text untrusted | Full lifecycle, source claims/uses, scope/time facts | Decisions/nonsecret claim references through owner, never grants | Fresh verification and source-atomic claim/consume after write-ahead intent | Cannot replace external claim with a local lock/read | Expired/revoked/consumed/unknown/unreachable source denies; evidence binds claim to effect |
| Execution adapter interface | Exact request and trusted-boundary one-shot permission | Approved snapshot and allowed workspace | Only named authorized effect targets | Execute/cancel original effect; retry only under separately verified contract | Cannot expand paths, choose fresh keys, retry itself or certify completion | Refuse mismatch/expiry/redeemed capability; bound effect/usage receipts and uncertainty |
| Evidence writer | Raw output untrusted; validated metadata | Explicit artifacts | New immutable evidence | Record artifact references | Cannot rewrite history or authenticate itself | Preserve failure; manifests/classification/redaction/finalization |
| Reconciliation adapter | Approved lookup and pending effect identity | Bounded external status or synthetic equivalent | Observation artifacts | Read-only lookup/disposition proposal | Cannot resend mutation | Unknown stays unresolved; query/target/freshness/receipt evidence |
| Materialized-state projector | Verified ordered events only | Journal | Disposable cache | Rebuild | Cannot authorize from cache or repair history | Reject gaps/versions; projection version and source head |
| Policy evaluator | Approved pinned policy; other content untrusted | Gates, caps, paths, dependencies | No policy/history changes | Deterministic decision | Cannot accept worker policy changes | Missing/unsupported rule denies; policy hash and evaluated predicates |
| Read-only reporting interface | Validated query | Verified sanitized view/evidence | No authoritative state | Read/export preview | Cannot advance/repair/approve | Label stale/unverified data; report source head and coverage |

Dependency direction: operator -> engine -> verifier/policy -> state owner ->
bounded adapter request. Adapter -> evidence/verification -> engine -> state owner.
Projector/reporting consume verified state; no reverse authority edge exists.

| Boundary | Assets and trust change |
| --- | --- |
| B1 operator -> authority | Authentic human consent versus text claiming approval |
| B2 definitions -> engine | Repository/item/policy identity and required gates |
| B3 engine -> durable owner | Ordered atomic intent/accounting and history |
| B4 engine -> worker/adapter | Narrow capabilities; AI worker is untrusted |
| B5 observations -> verification | Receipts/evidence versus established completion |
| B6 checkpoint -> recovery | Provenance, completeness and exclusive ownership |

The AI worker cannot approve work, alter required gates, rewrite historical events,
change its own allowed paths or establish its own completion. A proposed plan or
patch is untrusted input requiring the same acceptance path as any other input.
Workers cannot directly access controller state, approval sources or raw evidence.

## 5. Identity, authority and deterministic dispatch

### 5.1 Stable logical-effect identity

Bind an explicit repository UID to the canonical repository and owner-approved
target configuration; a folder name is insufficient. Run UID survives restart;
writer epoch changes with verified exclusive reacquisition. Item UID plus immutable
definition digest binds inputs, dependency IDs, targets and required gates.
Pin source commit/tree, plan digest, policy digest and schema/reducer versions.
Input changes require a new revision and explicit acceptance; old evidence retains
the old binding. Moving `main` never changes a running work item's identity.

The deduplication key is a domain-separated hash of repository UID and accepted
logical-effect ID ONLY. Item/revision/run/source/plan/policy/validation versions,
target and semantic-input hashes are not alternate key generators. An immutable
EFFECT_DEFINED record binds that ID to action, target and canonical semantic inputs.
All references must match that descriptor; changed metadata or a renamed/revised
item cannot create a new effect or bypass its history. The catalog records each
item revision's effect references and predecessor/equivalence relationships.
Equivalent effects across revisions/runs reuse the same ID and dedup key.

A legitimately different semantic effect requires an explicit approval binding a
new logical-effect ID, full descriptor and DIFFERENT_FROM predecessor relationship.
Intentional repetition similarly requires approved REPEAT_OF; compensation requires
approved COMPENSATES. These are new effects, not rewriting the predecessor. Changing
inputs, target, source, plan, policy or validation alone never grants repetition.
Unclassified equivalence or a missing predecessor history blocks dispatch. An alias
of a completed or unknown predecessor cannot redispatch it. A known completed
effect can only be intentionally repeated as the separately approved new effect;
an unknown predecessor cannot be repeated on risk acceptance, even under a new ID.
Safe recovery of that original effect follows section 7.4 with the SAME key.
Compensation does not prove the original outcome and cannot bypass CP-D02's slot.
The verified project effect index spans every item revision and run; incomplete
catalog, equivalence or freshness evidence denies dispatch.

### 5.2 Approval lifecycle and authoritative one-use claims

Approval verification matches genuine human source, repository, work package,
action/target/paths, revision scope, time, budgets and actual use limits. Missing
permission is not permission; absence of prohibition is not a grant. Read the full
lifecycle: expiry (even without a recorded EXPIRED event), revocation, supersession
and consumption apply. Revoking a successor never revives its predecessor.
Effective time is distinct from recorded order; late facts remain visible.
Unknown one-use consumption reserves the use until resolved, never resets it.
Malformed/duplicate grant IDs, missing targets, supersession cycles or conflicting
lifecycle evidence make affected authority unresolved; they cannot authorize dispatch.
Recurring grants are not converted into one-use grants. Direct current human
instructions remain evidence before register transcription; recording is not granting.

Real approval authentication/freshness is an unresolved live-adapter design gate.
The offline kernel can use only explicitly synthetic authority, structurally unable
to enable real adapters. No Markdown parser or worker text becomes a trusted human.
Recheck all authority at each dispatch using trustworthy time and a fresh source;
clock rollback never extends a grant. Specify/prove maximum proof age and revocation
propagation before a real adapter is enabled; accepted invalidation wins before
dispatch. Source-claim contact also obeys the current local dispatch fence.
Fresh reads and repository-local serialization do not prevent another host,
controller or manual path from spending the same external one-use grant. Real use
MUST atomically claim/consume it at the trusted approval source using CAS, exclusive
lease, nonce redemption or an equivalent one-shot capability. The atomic claim binds
repository, work package, action, target, logical-effect ID/key, intent/attempt,
descriptor digest and expiration. Every consumer, including manual paths, must use
that authoritative mechanism; a bypass path makes the grant unsupported for real
dispatch. Expired, revoked, superseded, consumed, ambiguous or unreachable authority
denies. No atomic source semantics means no real one-use dispatch.

After durable local intent, the source claim is idempotently identified by that
intent. Persist its nonsecret receipt before dispatch. The trusted dispatch boundary
redeems the capability once, checking binding, current expiry/revocation and final
fence. The source/broker integration must enforce that linearization across all
consumers; a claim followed by an unprotected fresh read is insufficient. If the
claim/redemption result is lost, query its original identity and retain uncertainty;
never mint another claim or assume no use. A lost lease/expired token cannot renew
authority automatically. No claim of instantaneous cancellation of an already
accepted external effect is made. Synthetic claim receipts have a distinct type
and cannot satisfy a real adapter's construction or dispatch requirements.

Permission-use records have RESERVED, CONSUMED and RELEASED dispositions, bound to
grant ID, logical effect key and owning attempt/intent. The final authority check
may recognize that intent's own reservation; any other intent is denied that use.
It must still check expiry, revocation, supersession and changed scope. Definite
non-dispatch permits release only on recorded proof and under the original grant's
use terms (a grant consumed by intent creation is not restored by cancellation).
Uncertain initiation retains the reservation. Normal consumption by the authorized
in-flight action prevents later uses; it does not itself revoke that same action.
For an external source these local records are accounting/provenance only. Release
also requires authoritative source disposition under original grant terms; a local
RELEASED record cannot make a spent external grant available. Reservation, consumption
and release are serialized across repository runs but do not replace source atomicity.

### 5.3 Atomic dispatch and one outstanding operation

Under one repository owner, T03 atomically checks the verified outstanding-effect
index and acquires its sole operation slot with intent, local permission-use and
budget reservations and attempt identity. A writer lock alone is NOT the slot guard.
When CP-D02 is active, any OTHER operation that is initiated, unsettled, uncertain,
reconciling, cancelling, draining or awaiting validation denies new dispatch across
all runs/items, even for sequential commands in the same process under the same owner.
Paused or terminal lifecycle does not free unresolved obligations. Slot reconstruction
includes committed-but-unacknowledged intents. BOTH slot-release routes require all
source-claim/control-contact/budget obligations resolved, plus either proven
non-dispatch or verified final effect and validation disposition. A terminal
cancellation may close validation as cancelled, never as passed. Proven no effect
with unknown claim/control billing still holds the slot and denies another operation.

Receipt collection, validation, pause/stop and read-only reconciliation of the owned
operation are permitted without allocating another slot. A section 7.4-approved retry
of the SAME logical effect may retain/transfer that slot to a new attempt; it is not
a new operation and keeps the original uncertain attempt/accounting. Another effect,
including compensation, cannot use that exception. T03 rechecks slot ownership and
retry proof atomically; simply labelling a command "retry" never bypasses the guard.

The adapter initiates only after durable intent, any required authoritative claim
receipt and final serialized fence/authority/slot check. Serialize local pause/stop
and dispatch initiation so a committed fence wins; use section 5.2 for source-atomic
external authority. Do not wait for operation completion while holding the command
loop hostage: receipts arrive separately. No adapter retries or spends a capability
twice on its own. Claim requests and other potentially chargeable control interactions
must be declared/bounded/accounted as part of the owned operation before contact.

### 5.4 Durable budget settlement

Budget records are separate from permission-use records. Version 1 dispositions
are RESERVED, CONSUMED, ADJUSTED, RELEASED and UNKNOWN_WORST_CASE_CHARGED. Each
reservation ID is owned by exactly one INTENT_COMMITTED, atomically binding repository,
work package, effect key, attempt, budget-policy/cap snapshot and reserved vector R.
Use integer enforceable units per dimension; no negative/nonfinite value or float
money. Require a defensible maximum liability W before contact (R covers W); an
unbounded or unobservable dimension cannot be silently uncapped. Synthetic W may be
zero; that says nothing about real billing. Account every attempt/control interaction.

| Event/disposition | Required evidence and atomic accounting effect |
| --- | --- |
| BUDGET_RESERVED / RESERVED | In the intent transaction: held=R, charged=0; deny if aggregate held+charged would exceed caps |
| BUDGET_CONSUMED / CONSUMED | Bound authoritative final usage A: held=0, charged=A; commit with receipt/settlement reference; semantic pass/fail is irrelevant to billing |
| BUDGET_ADJUSTED / ADJUSTED | Authoritative correction/reconciliation of actual A, including refund: replace prior absolute held/charged with verified values; never apply a blind delta twice |
| BUDGET_RELEASED / RELEASED | Proven non-dispatch AND zero liability for the reservation: held=0, charged=0; source claim/control costs must already be accounted separately |
| BUDGET_UNKNOWN / UNKNOWN_WORST_CASE_CHARGED | Missing telemetry, ambiguous billing/dispatch or cancellation without final evidence: held=0, charged=W, uncertainty=true; no assumed zero/refund |

Every settlement includes schema/event ID, expected prior reservation-event hash,
original intent/effect/attempt, evidence references, new absolute amounts and reason.
Commit settlement with its receipt/reconciliation/accounting observation so replay
cannot see an outcome with missing accounting. Repeated event ID/payload is an
idempotent observation; conflicting/stale predecessor or a second release denies.
RELEASED cannot be released again. A later contradictory authoritative bill produces
ADJUSTED with true actual usage plus an integrity exception/dispatch fence atomically;
the original release remains history, never a reason to discard or undercount a bill.
CONSUMED/ADJUSTED/UNKNOWN may receive an evidence-backed ADJUSTED record; none resets
historical caps or removes attempts. Totals are sums of current held+charged per
reservation over complete history, checked for nonnegative amounts and no double use.

If A exceeds R/W or remaining cap, durably record actual A and a breach/dispatch
fence in the same transaction; never reject the bill, understate usage or increase
the cap to make it fit. Missing telemetry charges W and blocks further dispatch
pending reconciliation. Uncertainty can be removed only by authoritative final
usage or non-dispatch/zero-liability proof; only the latter permits full release.
A cancellation request, process death, stop, owner acceptance or item revision is
not release evidence. Known cancellation charges are consumed/adjusted; unknown
ones remain worst-case charged. Never release while uncertainty still exists.
Terminal states retain accounting; late receipts settle through T23 without reopening.
On restart reconstruct every reservation/disposition, cap and breach before dispatch.
An external-source outage or an unavailable budget bound closes dispatch, not the ledger.

## 6. Normative state model

### 6.1 Vocabulary and invariants

| State | Meaning |
| --- | --- |
| PLANNED | Accepted definition; next declared step has not dispatched |
| RUNNING | Committed intent; initiated or awaiting immediate result |
| PAUSING | Dispatch fence committed; existing activity being accounted for |
| PAUSED | Fence retained; no unaccounted active execution; cursor preserved |
| VALIDATING | Recorded result awaits deterministic validation/required review |
| RECONCILIATION_REQUIRED | Effect, ownership or integrity cannot safely be inferred |
| BLOCKED | Known unmet prerequisite, approval, capability or recoverable failure |
| FAILED_FINAL | Final failure established under accepted policy |
| COMPLETED | All required evidence/gates establish completion |
| STOPPED | Permanent execution fence for this run/item |

READY is a derived predicate, not durable permission. WAITING_FOR_APPROVAL is
BLOCKED with APPROVAL_REQUIRED. FAILED_RECOVERABLE is BLOCKED with explicit
recovery conditions. No state is added merely because it has a UI label.

Keep durable dispatch fence (open/paused/stopped), continuation cursor,
blocking reasons, identity bindings and outstanding-effect dispositions separate
from lifecycle. A PAUSED item may lose approval while staying paused. Unknown
effects cannot hide behind PAUSED. Terminal states never reopen; non-advancing
late receipts may settle obligations while preserving the terminal disposition.
Run-level stop fences every nonterminal item. A run is COMPLETED only if all
required items, gates and effect obligations are complete; reporting cannot infer
completion from a majority or from a worker's prose.

### 6.2 Transition table

Actors: O = verified operator; E = deterministic engine; S = state owner;
V = authorized independent validator; R = bounded reconciliation adapter.
Every record below is a proposed versioned event, not an executable schema.
Every unspecified state/event pair is denied. Commit failure means no durable
acknowledgement, no new effect, and closed dispatch until storage is verified.

| ID / current state | Event | Authorized actor | Preconditions | Durable record | Permitted side effect | Resulting state | Interruption result | Forbidden alternatives |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| T01 absent | Accept definition | O -> E/S | Valid role/repo/definition/dependencies | PLAN_ACCEPTED with bindings | None | PLANNED | No acknowledgement if commit fails | Dispatch unrecorded plan |
| T02 PLANNED/BLOCKED | Evaluate prerequisites | E/S | Verified history and current inputs | READINESS_EVALUATED | None | PLANNED if ready; otherwise BLOCKED | Unknowns block | Permanent cached ready permission |
| T03 PLANNED | Initiate operation | E/S | Ready, no fence, fresh verified catalog, current authority; atomic repository slot check: no OTHER outstanding operation (5.3); original key/descriptor and any same-effect retry proof valid | Atomic INTENT_COMMITTED, slot ownership, budget/use reservations and attempt/effect key | Named effect only after durable intent, required source-atomic claim/receipt/redemption and final checks | RUNNING | C02/C03/C08 reconciliation retains slot, source claim and accounting | Revision generates fresh key; local lock/read substitutes for source claim or one-operation guard |
| T04 PLANNED/BLOCKED | Pause before dispatch | O -> E/S | Authentic command | PAUSE_REQUESTED and PAUSE_SETTLED atomically | None | PAUSED | Fence only acknowledged after commit | Dispatch after fence |
| T05 RUNNING | Pause local execution | O -> E/S | Authentic command; owned attempt | PAUSE_REQUESTED, fence, outstanding attempt | Approved bounded cancel/drain only | PAUSING | Unknown child/result -> RECONCILIATION_REQUIRED, fence retained | Claiming child termination from parent exit |
| T06 RUNNING | Pause external mutation | O -> E/S | Authentic command; effect key retained | PAUSE_REQUESTED and outstanding effect | Permitted observe/cancel, never new mutation | PAUSING | Missing/ambiguous receipt -> RECONCILIATION_REQUIRED | Retry, implicit rollback, cancellation assumed successful |
| T07 PAUSING | Activity settled | E/S from checked observations | No unaccounted active work; receipts/checkpoints bound | PAUSE_SETTLED with continuation cursor | None | PAUSED | Unknown activity remains reconciliation-required | Settled acknowledgement without proof |
| T08 VALIDATING | Pause validation | O -> E/S | Authentic command | Fence and validation checkpoint | Settle/cancel existing validation only | PAUSING until settled, then PAUSED | Unknown validator activity -> reconciliation | Starting new validation while paused |
| T09 RECONCILIATION_REQUIRED | Pause | O -> E/S | Authentic command | Pause fence | Permitted read-only reconciliation | RECONCILIATION_REQUIRED | Uncertainty and fence persist | Hiding uncertainty as PAUSED |
| T10 RUNNING/PAUSING | Receive result | Adapter observation -> E/S | Request/effect/target/input binding verified; usage evidence classified | RECEIPT_RECORDED and 5.4 CONSUMED/ADJUSTED or UNKNOWN settlement atomically; preserve slot through validation | Preserve evidence | Known budget/result -> VALIDATING or PAUSING to T07; unknown billing -> reconciliation; breach fences dispatch | Conflicting receipt/uncertain settlement retains obligations and slot | Receipt equals success; free capacity from missing telemetry; late result bypasses fence |
| T11 VALIDATING | Required validation passes | V -> E/S | Exact result, settled accounting and all named gates verified | VALIDATION_PASSED and next/final disposition; close operation slot only when 5.3 satisfied | None | COMPLETED only if all gates met; else PLANNED next step or BLOCKED | Uncommitted validation retains slot | Worker self-certifies; skip gates; drop outstanding accounting |
| T12 VALIDATING | Validation fails | V -> E/S | Verified failure and classification | VALIDATION_FAILED, reasons/recovery conditions; retain usage and effect outcome; close slot only under 5.3 | None | BLOCKED if recoverable; FAILED_FINAL only under final-failure rule | Interrupted check retains slot | Retry-until-green; repeat completed mutation to repair validation; erase usage |
| T13 any nonterminal | Approval expires/revokes/supersedes or becomes unavailable through another use | Verifier -> E/S | Effective lifecycle/use facts; own reservation/normal consumption follows section 5 | AUTHORITY_INVALIDATED or evaluated denial; fence | Account for existing activity only | PAUSED stays PAUSED with blocker; idle -> BLOCKED; active -> PAUSING or reconciliation | Unknown freshness denies | Revive old grant; assume unknown use unused; treat own reservation as a foreign use |
| T14 PAUSED | Resume | O -> E/S | Fresh authority/identities, independently verified recovery freshness (8.1), complete effect/use/budget indexes, exclusive owner; unresolved owned effect uses T17 instead | RESUME_ACCEPTED with cursor; retain owned slot until 5.3 closure | None; later T03 enforces global slot and source claim | PLANNED or VALIDATING | Denial leaves PAUSED with reason | Self-consistent stale checkpoint enables dispatch; resume itself dispatches |
| T15 any nonterminal | Source/plan/policy/item binding mismatch | E/S | Mismatch detected | BINDING_MISMATCH and fence | Account for existing work only | PAUSED retains fence/blocker; idle -> BLOCKED; active/uncertain -> reconciliation | Preserve old bindings | Silently follow moving main or changed inputs |
| T16 BLOCKED | Remediation accepted | O -> E/S | Evidence and explicit recovery/revision disposition; 5.1 predecessor and 7.4 replay restrictions still hold | BLOCKER_RESOLVED without replacing effect/use/budget history | None | PLANNED/VALIDATING only if evidence permits; PAUSED if fence retained | Unresolved conditions stay BLOCKED | Revision or owner command erases completed/unknown predecessor |
| T17 RECONCILIATION_REQUIRED | Resolve outcome | R evidence + O where policy requires -> E/S | Exactly one 7.4 evidence route: bound final receipt; authoritative nonexecution; reviewed safe same-key retry; or proof-free non-dispatching disposition | RECONCILIATION_RECORDED with route/proof, 5.4 settlement and slot disposition; original history retained | None in this transition | Receipt -> VALIDATING; nonexecution or safe-retry proof -> PLANNED with original key (PAUSED if fence); proof-free -> STOPPED/FAILED_FINAL or report-only reconciliation, never runnable | Missing proof/telemetry/source leaves uncertainty and slot; terminal obligations persist | Risk acceptance establishes nonexecution/success; fresh key or compensating action rewrites predecessor |
| T18 every nonterminal state | Graceful stop | O or E under approved stop rule -> S | Authentic command/rule | STOP_RECORDED, permanent fence, drain deadline and 5.4 known settlement or retained reserve/worst-case charge | Bounded already-approved drain; no new steps | STOPPED immediately; effects, accounting and slot pending until proven settled | Timeout -> T20; uncertain outcome remains worst-case charged | Stop releases budget/use/slot; business workflow advances |
| T19 every nonterminal state | Immediate stop | O or E under approved stop rule -> S | Authentic command/rule | STOP_RECORDED, permanent fence, obligations and 5.4 uncertainty/known settlement | Best-effort allowed cancellation/kill and observation | STOPPED | Unknown outcomes/billing retain worst-case charge and slot | Cancellation means zero bill; erase accounting or promise reversal |
| T20 STOPPED with graceful drain | Escalate immediate stop | O or approved deadline rule -> E/S | Outstanding drain/cancel obligations | STOP_ESCALATED plus evidence-backed 5.4 settlement or UNKNOWN; no automatic refund | Permitted cancellation only | STOPPED | Unknown obligations, charge and slot remain | Reopen work; refund on deadline |
| T21 any state | Competing resume | Second process | Owner lock unavailable | No competing journal write; local denial result | None | Canonical state unchanged | Bounded refuse/wait | Unlink lock, PID/mtime takeover |
| T22 COMPLETED/FAILED_FINAL/STOPPED | Restart/resume request | O/read interface; E denies advancement | Verified terminal event | No advancing event; optional non-authorizing observation | Reporting and separately allowed receipt reconciliation | Same terminal state | Integrity failure makes status unverified, dispatch closed | Reopen terminal run or reset budget |
| T23 any state, including terminal | Late bound receipt/accounting evidence | R -> E/S | Existing recorded intent/effect/reservation identity, including settled/RELEASED; authoritative binding/integrity/usage verified | LATE_RECEIPT_RECORDED and 5.4 settlement atomically; contradictory release -> true-usage ADJUSTED plus integrity exception/fence; slot closes only under 5.3 | Evidence preservation only | Same lifecycle, no advancement; terminal never reopens; active work obeys any new fence | Conflicting/unknown usage retains accounting uncertainty | Ignore bill after obligation closed; reset cap; convert stopped/failed to completed |
| T24 PAUSING | Existing validator returns | V observation -> E/S | Check began before fence; result and input bindings verified | VALIDATOR_OBSERVATION_RECORDED with pass/fail and cursor | Evidence preservation only | PAUSING until T07 accounts for activity, then PAUSED | Unknown validator activity -> reconciliation | Finalize/advance on late pass; start another check |
| T25 RUNNING/PAUSING/STOPPED with outstanding never-handed intent | Final check denies or pause/stop fence wins | E/S | Authoritative non-dispatch proof; source claim/control-contact disposition and billing separately classified as known or unknown | NONDISPATCH_PROVEN independently of source/local use disposition; 5.4 RELEASED only for proven zero liability, otherwise CONSUMED/UNKNOWN; every unknown retains slot/accounting | None | BLOCKED/PAUSED if obligations resolved; otherwise reconciliation; STOPPED unchanged with obligations | Lost claim/control bill or unproven non-dispatch retains slot/accounting | Local release reactivates external grant; zero effect means zero control cost; reopen STOPPED |

After T24/T07, resume restores VALIDATING and applies the still-valid bound pass/fail
observation through T11/T12. A prior failure remains binding until explicit
remediation and a newly authorized validation attempt; resume does not rerun until
green. Success still requires all current completion gates. If observation validity
is uncertain, block for disposition rather than discard it. No paused observation
itself finalizes work.

All stop modes close future dispatch at the same serialized fence. Graceful stop
allows only the already-authorized operation to settle within a declared deadline;
it cannot launch its next step. Immediate stop requests bounded cancellation now.
Neither guarantees reversal of accepted external mutations. A stop acknowledgement
means the fence is durable, not that cessation is verified. If persistence is
unavailable, reject the durable acknowledgement, disable dispatch in process and
attempt only permitted emergency containment; recovery must expose the uncertainty.

### 6.3 Crash and acknowledgement table

| ID / crash boundary | Reconstructed fact | Required action / forbidden inference |
| --- | --- | --- |
| C01 before intent recording | No committed permission, budget reservation or slot to contact source/adapter | No effect/claim was permitted; reevaluate authority, stable effect key and global slot; never assume cached readiness |
| C02 after intent but before dispatch | Intent, slot and reservations exist; source claim or dispatch may be uncertain | RECONCILIATION_REQUIRED unless non-dispatch/source claim independently proven; no automatic release or fresh key |
| C03 after dispatch without receipt | Outcome/billing unknown; original key, claimed use and slot retained | Query original effect/source claim; apply 5.4 worst-case accounting; proof-free owner command cannot resend |
| C04 after receipt before verification | Receipt and corresponding budget settlement committed together | Validate same receipt; no redispatch; fences/slot/usage survive; missing usage remains reconciliation-required |
| C05 after validation commit before acknowledgement | Result already committed | Same command returns recorded disposition; never duplicate next-step initiation |
| C06 before/after pause or stop commit | Only committed fence can be acknowledged | Replay fence first; unacknowledged command retried by same ID; unknown activity exposed |
| C07 during export, projection or restore of an older valid chain | Internal consistency does not establish latest effect/use/budget state | Read-only until 8.1 freshness proof/complete authoritative reconciliation; no history or cap reset |
| C08 source claim/redemption before local receipt commit | One-use source may already have reserved/consumed grant | Query original claim identity; do not re-claim, release, assume zero billing or dispatch without verified receipt; retain slot |
| C09 during budget settlement/slot release | Outcome and accounting/slot transaction may be committed but unacknowledged | Verify/replay same event IDs and predecessor; no duplicate credit, dropped charge or extra outstanding operation |

## 7. Durable events, atomicity and recovery

### 7.1 Event and storage contract

One run journal has strictly increasing sequence assigned by S, unique immutable
event ID and command ID, writer epoch, run/item/repository bindings, schema version,
event kind, recorded timestamp, effective-time facts where relevant and previous
event hash. Hash canonical body excluding its own hash; genesis binds format and
initial identities. No object directly or indirectly hashes itself. A repository-
scoped durable catalog names every run history and its identity; registration is
committed before a run may receive intents. The catalog and all event mutations
share repository-scoped writer exclusion. Verified complete histories reconstruct
both logical-effect outcomes and grant-use reservations across runs. A missing,
rolled-back or unverifiable catalog/history denies all affected dispatch, not just
the run that happened to notice it. The outstanding-operation slot and all 5.4
budget settlements are reconstructed, not inferred from lifecycle or process locks.
Catalog/registration crash consistency is part
of the storage selection and fault-injection contract, never an assumed second store.

The proposed storage interface is `acquire_writer`, `load_verified`,
`commit(expected_head, transaction)`, `read_verified` and `export_checkpoint`.
These names are prose only. Storage selection is a CP-WP-002 entry decision.
A single framed append-only local journal is a candidate; a local transactional
store is another. Compare crash recovery, platform sync guarantees, dependency
cost, auditability and rollback before selection; neither is implemented here.

Atomicity means all or none of intent/reservations/identity/operation slot becomes committed to a
reader. A successful acknowledgement follows a verified write/flush/fsync barrier
and required directory/metadata durability for the selected storage and filesystem.
An ordinary JSON line, flush alone or atomic rename alone proves none of the full
contract. Unsupported guarantees must be reported as unavailable and refuse the
affected capability. Power-loss durability needs its own platform evidence; process
crash tests are not that proof. Once storage reports uncertain commit, do not keep
using optimistic in-memory state: close dispatch and reload/reconcile.

Acknowledgements distinguish command committed, intent committed, receipt committed,
validation committed, pause requested, pause settled and stop fence committed.
An operation timeout after commit is not proof that the command failed.

### 7.2 Exclusion and stale ownership

Use one repository-scoped OS-backed exclusive local ownership primitive on a
verified owned path, covering the complete run catalog, all run journals, effect
index and approval-use index. Per-run locks alone are insufficient. All runs for
that repository resolve the same verified root; an alternate root/clone cannot
initialize an independent authority while another execution history exists.
Keep lock object identity stable; do not unlink/recreate it to break contention.
PID, file age or timeout is not authority to steal ownership. Reacquisition requires
the OS lock, new writer epoch, verified journal and reconciliation of old attempts.
The lock is cooperative; filesystem ACLs/checked handles protect against untrusted
writers. Old children and remote effects may survive the owner; a new epoch alone
does not fence them. Until adapter-level fencing/cessation is proven, no new effect.
Only the future synthetic adapter is eligible for initial offline kernel execution.

### 7.3 Reconstruction, corruption and schema evolution

Rebuild materialized state, outstanding slot and project effect/use/budget indexes from verified committed events
using a pinned reducer. Each cache carries source sequence/head and reducer version;
reporting labels stale caches, while dispatch never trusts them independently.
Only one repository owner writes the project effect/approval-use indexes, and they
are reconstructible, not second mutable authorities. Missing catalog entries or
referenced histories block dispatch. Replay covers cross-run one-use consumption,
including outstanding reservations, rather than only the run being resumed. Replay
preserves effect equivalence across revisions and reconstructs every reservation's
held/charged/uncertainty fields. Old valid history cannot dispatch merely because it
replays: recovery freshness must pass section 8.1. A missing/stale proof closes dispatch.

Same command ID and payload returns the prior outcome. Same ID/different payload
is an integrity error. Physical duplicate events, reordered sequences, gaps or
predecessor mismatch fail verification; never sort or silently deduplicate history.
Unknown schema/reducer versions prevent advancement. Compatibility/migration must
be explicit, deterministic and tested, preserving original bytes and provenance;
new interpretation cannot manufacture old permission or erase failure.

A corrupt/torn tail preserves original bytes and blocks advancement. Diagnose
uncommitted tail versus committed corruption; never silently truncate/skip bytes.
An owner-authorized successor segment may name the preserved original digest,
verified prefix, unresolved reservations and recovery rationale. It is not a reset
of authority, budgets, keys or terminal states. Stronger evidence may be required
before any side effect can be reconciled; operator enthusiasm is not receipt proof.

SHA-256 is tamper evidence relative to a trusted head, not writer authenticity.
An unanchored valid suffix rollback can self-verify. An attacker able to rewrite
both data and local anchors can fabricate consistency. Independently protected
head/provenance, authentic operator identity, authorization and storage permissions
are separate controls. No malicious-writer authenticity claim is made by this v1.
Section 8.1 turns this limitation into a dispatch gate: restored self-consistent
history alone is read-only and never a basis for fresh effect or approval use.

### 7.4 External receipt reconciliation

Persist original effect key/descriptor, attempt, source-claim and budget reservation
identities. Lookup is bounded/read-only and records query/time/source/response
bindings. T17 classifies one of these routes; every route records evidence and
accounting and retains the original history:

| Route | Permitted disposition / required proof |
| --- | --- |
| VERIFIED_RECEIPT | Bound authoritative final effect/usage receipt -> VALIDATING (or PAUSED if fenced); unresolved billing/claim state remains reconciliation-required; no success before independent validation |
| PROVEN_NONEXECUTION | Authoritative proof covering the original request and every relevant dispatch path -> PLANNED with same key only after source-claim and budget disposition; original grant terms still apply |
| SAFE_SAME_EFFECT_RETRY | Separately reviewed/approved contract proves repeated/concurrent submission cannot produce another mutation; original key/descriptor and effect-outcome uncertainty retained; prior claims/billing resolved, eligible retry authority/source and budget verified -> PLANNED owning the same slot; new attempt claim/receipt/redemption occurs only in T03 after its durable intent |
| OWNER_NONDISPATCHING_DISPOSITION | Without either proof above, owner may choose STOPPED, FAILED_FINAL or report-only RECONCILIATION_REQUIRED; original unknown effect, charges, claims and slot remain; never PLANNED, runnable PAUSED, VALIDATING-success or COMPLETED |

Human risk acceptance is not nonexecution evidence. No owner command converts
uncertainty to success, releases unknown liability or restores spent permission.
"Not found" is proof only if the external contract guarantees complete, current
nonexecution for that operation; empty/stale searches do not qualify. Safe retry
must cover target idempotency retention/expiry, concurrent old attempts, original
key lookup and every reachable mutation path. Missing or expired protection denies.
Reconciliation never performs the retry itself; T03 rechecks all current gates.
Safe effect retry cannot bypass 5.4: unknown billing must first be authoritatively
settled, and every retained/new attempt remains charged/reserved under the same caps.
External one-use claims consumed by an earlier attempt are not revived: retry needs
authority whose actual terms permit it plus the required authoritative claim.

Compensation is a new explicitly approved COMPENSATES effect with a new ID and
descriptor, durable predecessor link and independent authority/budget. It neither
erases nor proves the unknown predecessor. Under CP-D02 that unknown predecessor
still blocks any different operation, including compensation; execution would need
resolution or a separately approved profile, never an undocumented exception.
No external lookup or mutation is part of CP-WP-001 or the synthetic kernel.

## 8. Storage and cross-computer checkpoint contract

All locations below are future proposals, not files created by CP-WP-001.

| Class | Proposed location | Handling |
| --- | --- | --- |
| Tracked declarative configuration | `control-plane/project.json`, `control-plane/work-items/*.json` if authorized later | Nonsecret definitions only; reviewed/pinned; not consent or active state |
| Tracked policy/schema | `control-plane/policy/`, `tools/aegis_delivery_control/schemas/` if later justified | Closed versioned contracts; none executable/created now |
| Local active runtime state | Windows `%LOCALAPPDATA%/ProjectAegis/control-plane/<repo-id>/`; Linux `${XDG_STATE_HOME:-$HOME/.local/state}/project-aegis/control-plane/<repo-id>/` | Outside checkout; one root lock/catalog, journals, effect/use/budget indexes and outstanding slot; restore needs independent freshness, not local consistency |
| Sensitive/raw evidence | External sibling `raw-evidence/<run-id>/` | Worker inaccessible; classification-required encryption; never credentials |
| Sanitized exportable evidence | External `exports/<run-id>/<export-id>/` | Immutable manifest; preview/redaction/integrity review before publication |
| Cross-computer checkpoint | Intentional `docs/evidence/control-plane/checkpoints/<run-id>/<checkpoint-id>/` export only with later explicit approval | Sanitized snapshot with source/export heads and freshness proof; read-only until 8.1 passes, never automatic runtime commit |
| Forbidden Git content | No allowed path | Credentials, unrestricted env dumps, sealed holdouts, raw sensitive transcripts/receipts, active journals/locks, live permission tokens |

Authoritative catalogs, journals and effect/approval-use facts required for future
deduplication MUST NOT be deleted by routine retention. A separately accepted
history-compaction contract must preserve those facts before any retirement.
Disposable projections/artifacts may be reviewed for deletion 30 days after terminal
disposition and all effects settle. Raw evidence has a 30-day review date, with
preserve-on-failure/incident holds. A review date is not automatic deletion.
Cleanup needs owned-path verification and applicable authorization. Sanitized
published evidence is permanent history; exclude sensitive content before publication.
Evidence metadata includes path, bytes, digest, classification, readers, redaction,
retention/review date, creation time, policy reference and preserve-on-failure status.

Root `.gitignore` is absent at this base. Recommend only in later authorized work:

```text
/.aegis-control-plane/
/tools/aegis_delivery_control/**/__pycache__/
/tools/aegis_delivery_control/**/*.py[cod]
```

The scratch path is reserved defensively, not permission to store sensitive state
inside the checkout. Ignore rules are not security controls and cannot prevent
forced staging. Never blanket-ignore or modify existing `artifacts/recovery/` or
`artifacts/reviews/`; their contents are unrelated user property.

Checkpoint export requires a stable verified head, complete decision-bearing
history, repository/source/item/policy/schema identities, approvals and lifecycle
references, effect keys/receipts/obligations, export provenance and transfer terms.
Include the complete project catalog and all history dependencies needed to rebuild
cross-revision/run effect, approval-use and budget indexes plus outstanding slot;
a standalone run dump is insufficient. Include source head (project-catalog head
and complete run-head vector), export head (sanitized representation's manifest
digest), authoritative source inventory and freshness/monotonicity proof references.
Redaction produces a new representation and manifest/hash chain explicitly mapped
to the original head; it must not claim original hashes still cover changed bytes.
If necessary recovery facts cannot be exported safely, mark REPORT_ONLY rather
than resumable. Never include credentials or sealed holdouts.

On another computer: verify clean-clone source/export provenance; import read-only;
verify completeness; rebuild; satisfy 8.1 freshness and reconcile later effect/use/
budget facts; refresh/atomically claim authority when appropriate; establish exclusive
ownership. Old-host inactivity proves neither latest history nor absence of later
manual/other-host activity. If old-host fencing or freshness cannot be established,
execution remains blocked. An offline simulation may test these gates, not bypass them.
Git is a transport for an intentional reviewed checkpoint, not a transactional
runtime database, distributed lock or proof of exclusive execution ownership.

### 8.1 Mandatory recovery freshness gate

Every import/restore/recovered history must obtain one of these complete proofs
before dispatch (synthetic proof only in CP-WP-002):

1. Independently protected monotonic authoritative head: read the current project
   catalog/run-head vector and monotonic epoch from a trusted source that the local
   journal/checkpoint writer cannot roll back. Verify authentic binding, freshness
   and nondecreasing sequence against source_head. Equal numbers with different
   hashes are contradictions; older valid chains are rollback. Fetch and verify all
   missing later events before enabling dispatch; an anchor mismatch is not cured
   by declaring the old host inactive. The source must advance durably with protected
   effect/use/budget commits or an unresolved write-ahead pending marker; anchoring
   only at export leaves an unsafe gap. Its commit/recovery protocol is a later
   implementation gate, not an assumed service or local sidecar.
2. Complete authoritative reconciliation: use an independently current source
   inventory, not just the old checkpoint's list, to account for all registered runs,
   effects/receipts, outstanding operations, budget liabilities and approval claim/
   consumption sources, including other hosts/manual paths. Each source supplies a
   complete current watermark or equivalent proof of absence/additions. Record the
   recovered head/vector and proofs; reconcile later events before dispatch. Partial
   lookup or an operator assertion of completeness does not qualify.

In the selected mode, unavailable, stale or contradictory proof denies dispatch.
Do not silently downgrade a failed anchor check to partial reconciliation; mode 2
must independently satisfy every requirement. Without either complete proof, import
stays read-only/report-only or RECONCILIATION_REQUIRED. No self-consistent chain,
Git SHA, local head file, old-host inactivity or human risk acceptance substitutes.
The proof must be current at dispatch and tied to the verified reconstruction;
later observed events invalidate it until reconciled. Actual atomic one-use claims
still apply even after freshness succeeds; checkpoint freshness is not a spend lock.

Evidence finalization follows the useful BER separation: immutable inputs before
verification, final artifacts afterwards, detached marker outside the manifest it
names. Controller policy metadata must be independent of BER. Hashes do not replace
authentic evidence source or independent completion verification.

## 9. Threat model and operational limitations

Scope: the proposed single-host contract and future adapter boundaries. Assets:
human authority, target repository, effect identity, budgets, journal and evidence.
Actors: verified operator, untrusted worker, lower-trust local process, compromised
adapter/evidence writer and malicious checkpoint supplier. No public/tenant-facing
API exists in this proposal; SaaS tenant routes are out of scope. Repository and
object-level authorization still apply at every state/effect/evidence boundary.
Risks below describe attack paths against a future incorrect implementation, not
claims of current exploitation. No residual live risk is accepted by this document.

| Threat / boundary / priority | Abuse path | Required mitigation / owner | Negative proof |
| --- | --- | --- | --- |
| Forged authority / B1,B4 / high | Worker emits "owner approved" and seeks privileged dispatch | Authentic source verifier, deterministic scope checks; security reviewer/CP-WP-003 | Synthetic prose grant cannot authorize |
| Stale authority / B1,B2 / high | Paused run resumes with revoked/consumed grant | Fresh lifecycle/time evaluation and serialized invalidation; engine owner | Expiry/revocation/supersession/consumption denies |
| Duplicate effect / B2,B3,B4 / high | Revised item/new run generates a fresh key for the same completed/unknown mutation | CP-D08 immutable logical-effect identity, durable equivalence and explicit new-effect approval; kernel owner | F01 revisions/aliases cannot evade predecessor dedup |
| Proof-free disposition / B1,B4,B5 / high | Owner accepts uncertainty and requests retry/success or disguises it as compensation | T17/7.4 proof routes, original key, non-dispatching risk disposition; engine owner | F02 risk acceptance/new-ID compensation cannot clear unknown outcome |
| External approval race / B1,B4 / high | Other host/manual consumer spends one-use grant after local check | Source-atomic claim/redemption across every consumer; unsupported source denies; authority owner | F03 one winner; lost/expired claim and synthetic token cannot dispatch |
| Accounting loss / B3,B5 / high | Stop, cancellation, duplicate settlement or crash refunds uncertain usage | Versioned intent-owned 5.4 lifecycle; honest actual/worst-case charges; accounting owner | F04a/F04b routes replay without free capacity, negative totals or cap reset |
| Checkpoint rollback / B3,B6 / high | Older valid chain omits newer effect/use, even after old host stops | Mandatory independent freshness or complete current-source reconciliation (8.1); recovery owner | F05 older valid effect/use histories and unavailable/stale/contradictory proof deny |
| Multiple operations / B3,B4 / high | Same writer starts different item while first awaits settlement/validation | Atomic repository-wide outstanding slot independent of writer lock; kernel owner | F06 sequential same-owner/different-item/run intent denied before and after crash |
| Cross-project substitution / B2,B5,B6 / high | Valid foreign grant/receipt/checkpoint reused for this target | Bind repository and object identity everywhere; engine owner | Foreign identity rejected |
| Prompt injection / B2,B4,B5 / high | Worker artifact asks to remove gates, expand paths or certify itself | Treat output as data; closed contract and independent validation; security reviewer | Injected plan/evidence cannot affect authority |
| Path escape / B3,B5 / high | Local adversary swaps ancestor to redirect evidence write | Owned ACL/checked-handle capability; unsupported guarantees refuse; platform owner | Symlink/reparse swap probe with prevention versus detection recorded |
| Writer compromise / B3,B5,B6 / high | Writer replaces content and hashes to fabricate success | State trust assumption explicitly; independent authenticity before claiming resistance; owner/security | Demonstrate limits of rewritten chain; no authenticity claim from hashes |
| Lost/counterfeit receipts / B5 / high | Adapter fabricates success or drops accepted-effect receipt | Bound independent receipt verification; unknown outcome blocks; adapter owner | Conflicting/missing receipt cannot complete |
| Schema reinterpretation / B3,B6 / medium | New reducer interprets old denial as grant | Version pin, explicit migration and golden replay; kernel owner | Unknown version and unsafe migration reject |
| Availability/cost exhaustion / B2,B4 / medium | Huge input or endless retry consumes storage/time/budget | Bounded record/input sizes, attempts/deadlines and no autonomous retries; policy owner | Oversize/cap/deadline denies before effect |

Future AI-specific scope: injection/output handling/excessive agency/fabricated
completion map to rows above; sensitive disclosure maps to evidence/path controls;
unbounded consumption maps to caps. Model supply chain, training poisoning, prompt
secrecy and retrieval/vector isolation have no active surface in the synthetic
kernel and need a fresh model before any corresponding integration. No provider,
retrieval store or model credentials are selected here.

Windows evidence code currently documents detection-only mid-operation swap
handling; process cleanup cannot prove post-leader descendant reaping. Those facts
block stronger future guarantees, not documentation. Linux implementation presence
also is not platform evidence: run actual capability probes in a separately
authorized package. Distributed leases/fencing, real authority authentication,
external idempotency and immutable signing/storage remain open implementation gates.

## 10. Future tests and acceptance

These are planned assertions, not executed controller tests. Use independent
synthetic fixtures and owned temporary storage outside checkout. Record source SHA,
OS, Python/shell versions, command, exit, skips, capability outcome and evidence head.

| Test family / covered contract | Expected assertion | Layer |
| --- | --- | --- |
| State table T01–T25 | Allowed transitions meet guards; every unspecified pair denies | Unit/table-driven |
| Reconstruction | Same complete catalog/journals yield states, budget/use dispositions, fences, stable effect index and outstanding slot | Unit/integration |
| Tamper/rollback | Altered/gapped/reordered/conflicting duplicate events reject; internally valid older chain cannot dispatch without 8.1 proof | Unit/fault injection |
| Interrupted transaction | Partial record never enables dispatch; bytes preserved, no silent repair | Fault injection |
| Idempotency | Same command returns prior outcome; effect key stable across item/source/plan/policy revisions and runs; see F01 | Unit/integration |
| Writer exclusion | Two different-run processes sharing an effect or one-use grant cannot advance concurrently; no lock-file deletion takeover | Multiprocess integration |
| Pause T04–T10,T14,T24 | Fence precedes acknowledgement; pause-then-result and paused validation pass/fail are recorded without advancement; restart preserves fence | Integration/fault injection |
| Graceful/immediate stop T18–T20 | No new step after fence; drain deadline/cancel obligations retained | Integration/fault injection |
| Crashes C01–C09 | Inject immediately before/after every commit/acknowledgement, source claim/redemption and budget/slot settlement; no duplicate effect/use/credit | Fault injection |
| Lost external receipt C03,T17 | Synthetic accepted effect plus missing receipt stays unresolved | Integration/fault injection |
| Approval T13 | Expiry/revocation/supersession/consumption and late effective facts deny; predecessor never revives | Unit |
| Concurrent one-use consumption | Local reservation is accounting only; atomic trusted-source claim and redemption are required; F03 includes other-host/manual races | Integration |
| Identity T15 | Changed source/plan/policy/item or foreign repo fails; new run cannot evade effect index | Unit/integration |
| Paths | Traversal/absolute/UNC/drive/ADS/device names reject | Unit |
| Symlinks/reparse | Ancestor/leaf swaps prevented where claimed; otherwise capability unavailable | Platform capability/fault injection |
| Evidence integrity | Missing/altered/cross-run/unfinalized artifacts cannot establish completion | Unit/integration |
| Terminal restart T22,T23 | No reopen; late effect/usage receipts settle obligations and accounting atomically, never reset caps | Unit/integration |
| PowerShell 5.1 | Desktop quoting, Unicode/spaced paths, exit codes and module invocation correct | Windows acceptance |
| PowerShell Core | Same command contract on Windows/Linux; native exit preserved | Acceptance |
| Linux | Actual lock/sync/no-follow behavior measured; no inferred power-loss proof | Platform capability/integration |
| Windows | Actual path/exclusion/cleanup behavior; detection never called prevention | Platform capability/integration |
| Clean-clone recovery | Complete catalog/histories plus 8.1 independent freshness rebuild all cross-run effect/use/budget/slot decisions; inactive old host is insufficient; see F05 | Acceptance |
| Injection | Worker-proposed approval, paths, gate removal and completion cannot authorize | Adversarial unit/integration |
| Schema evolution | Unknown versions block; supported conversion preserves source bytes/provenance | Unit/migration fault injection |
| Retention safety | Routine cleanup cannot remove catalog/journals/effect-use facts needed for replay; absent dependencies block | Integration |
| Read-only reporting | Status/export preview cannot append/advance/repair | Integration |

### 10.1 Six finding-specific negative acceptance families

F01–F06 are required future synthetic tests, not executed runtime evidence. A
positive control must show the narrowly permitted route alongside each denial.

| ID / contract locations | Required cases and expected result |
| --- | --- |
| F01 / CP-D08, 5.1, T03/T15/T16 | Completed and unknown effect reused by another item revision/run has the same key and cannot dispatch. Change source/plan/policy/validation only: no new effect. New-ID alias, missing equivalence/predecessor history and changed descriptor under old ID deny. Explicitly approved genuinely different/repeated effect retains its relationship; unknown predecessor still blocks repetition/global slot |
| F02 / CP-D04, 7.4, T17 | Risk acceptance, "assume failed", stop/report and new-ID compensation cannot cause resend, success or history erasure. Nonexecution proof permits only original-key recovery with other gates met. Reviewed concurrent-safe same-key retry contract permits only its bounded route; missing proof, fresh key or unsettled billing denies. A late verified receipt still needs validation; terminal disposition never reopens |
| F03 / CP-D09, 5.2, C08 | Interleave two hosts/controllers and a manual consumer after identical fresh reads: exactly one authoritative claim/redemption succeeds. Local-only reservation, bypass consumer, unsupported CAS/lease, wrong binding, expired/revoked/consumed grant, unreachable/ambiguous source, lost claim receipt, clock rollback and replayed redemption all deny dispatch. Synthetic claim cannot construct/enable real adapter; own valid claim passes only its exact intent |
| F04a / CP-D10, 5.4, T10/T17/T25 | Receipt A below/equal/above R settles true A once; overrun records breach/fence. Proven non-dispatch plus zero liability releases; non-dispatch with claim/control cost consumes that cost; unknown claim/control billing retains slot and blocks another item/run. Unknown dispatch/billing or missing telemetry charges W and blocks; no known bound denies before contact. Later authoritative final usage adjusts absolute amounts; uncertainty cannot release without nonexecution AND zero-liability proof |
| F04b / 5.4, T18–T20/T23, C09 | Cancel requested/confirmed without final usage does not refund; known cancellation bill settles; graceful stop, immediate stop and drain timeout preserve reserve or worst-case charge. Late terminal bill/refund adjusts without reopen; receipt validation failure retains cost. Crash before/after settlement, duplicate/stale release, conflicting event ID, negative values, restart/new run/revision/cap reset attempts cannot drop/double-credit usage; contradictory post-release bill adjusts to true usage, preserves release history and fences dispatch |
| F05 / CP-D07, 7.3, 8.1, C07 | Restore older valid checkpoint after newer effect receipt and separately after newer one-use consumption: detect via independent current head/inventory and reconcile later facts before dispatch. Source/export heads cannot substitute for each other. Unavailable/stale/contradictory anchor, source rollback, omitted source/run, incomplete watermark, newer pending commit, rewritten local anchor or inactive old host gives no freshness proof. Without complete independent proof, remain read-only/report-only/reconciliation-required |
| F06 / CP-D02, 5.3, T03, C02/C09 | Same process/owner sequentially attempts another item, then another run, while original is initiated/unsettled/uncertain/reconciling/cancelling/draining/awaiting validation: atomic intent denied for every disposition. Pause/stop, completed lock acquisition and crash/restart cannot clear slot. Proven no effect plus unknown claim/control billing still blocks another item/run. Proven final settlement/validation frees it once; approved same-effect retry retains original slot and uncertain attempt, never authorizes another effect |

CP-WP-001 acceptance is document consistency, link/structure review, complete
scenario coverage and independent architecture/security review. Existing repository
checks remain regression evidence, not proof of this future runtime. See the
[work-package contract](../roadmaps/resumable-control-plane-backlog.md#2-cp-wp-001-contract)
for scope, validation and stop-before-merge requirements.
