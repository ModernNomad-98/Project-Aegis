# Behavioral Eval Runner — Durable Backlog and Phase Register

Prepared: 2026-08-10.
Purpose: the durable, repository-resident continuation and deferred-work register for the
Behavioral Eval Runner, required before Phase 2B-0 may begin. This file replaces every
non-repository continuation source (conversation memory, temporary review exports, closeout
summaries, owner recollection) as the authoritative record of what remains, why, and under
what authority.

---

## 1. Status and authority

- **Status:** ACTIVE DURABLE BACKLOG
- **Created:** 2026-08-10
- **Owner:** Peter Nguyen
- **Repository:** ModernNomad-98/Project-Aegis
- **Authoritative design:**
  [`docs/design/behavioral-eval-runner-v1.md`](../design/behavioral-eval-runner-v1.md)
- **Authoritative design successor (partial — WP-2B-2 grading-stack fast track):**
  [`docs/design/behavioral-eval-runner-v1-fast-track-successor.md`](../design/behavioral-eval-runner-v1-fast-track-successor.md)
  — authoritative for the revised phase structure and the directly dependent §7–§9/§19 scope
  under BER-DEC-007 (2026-08-13); the v1 design remains authoritative for everything it does
  not change.
- **Design merge source:** [PR #78](https://github.com/ModernNomad-98/Project-Aegis/pull/78)
- **Design merge commit:** `c61aca84554dbc38d08b8acb2bc3b0b428f3bf01`
- **Reviewed design blob:** `94ba583a92b2150036ab3efc35e8fa838ecba4da`

Authority relationships (binding):

- The merged design is **authoritative for architecture and controls**. Every requirement,
  state model, containment rule, evidence rule, and phase definition referenced below is
  defined there; this backlog records work status against it, never a competing definition.
- This backlog is **authoritative for continuation and deferred work**: what remains, which
  phase owns it, what evidence and approval each item needs, and what may not begin yet.
- **Conversation memory is not an authoritative source.** No chat transcript, AI session
  memory, or assistant recollection carries design or authorization authority.
- **Temporary review exports are evidence history, not the continuation record.** Local
  export directories used during the PR #78 review cycle document how findings were reached;
  they are not authoritative sources and are cited nowhere in this register as authority.
- **A conflict between this backlog and the merged design is a STOP condition.** Work halts
  and the conflict is surfaced to the owner; it is never resolved silently in either
  direction.
- **The merged design wins** until a reviewed design successor explicitly supersedes it
  through the repository's normal review-and-merge process.

Retention posture (per the `docs-retention-index` discipline, recorded in prose because the
repository instantiates no retention index and design decision D10 made no retention/index
change): this file is **permanent/canonical** — reason-to-keep: it is the single durable
register of Behavioral Eval Runner continuation work and owner decisions; superseded-by:
none; cleanup rule: never silently deleted, superseded only by an explicit reviewed
successor that names this file.

## 2. Governance rules

These rules bind every use of this register:

1. A backlog entry is **not implementation authority**.
2. Work may begin only after **explicit, phase-specific owner authorization**, made
   durable per the work-package authorization protocol below.
3. Every implementation phase uses a **separate branch and reviewed PR**.
4. **No entry may be silently deleted.**
5. Completed, rejected, or replaced work remains visible with: final status; evidence;
   date; owner; and the superseding item where applicable.
6. **Status changes require repository review** (a reviewed PR that edits this file).
7. **No automatic reprioritization by an agent.**
8. **No automatic scope expansion.**
9. **Human merge authority remains required.**
10. **Actual PR content must be reviewed before any merge recommendation.**
11. **Auto-merge remains prohibited** unless separately and explicitly authorized.
12. **Phase 2B-0 must not begin until this backlog is merged.**

### Work-package authorization protocol (binding)

1. **The work-package record (§7 of this file) is the governing execution-authority
   record.** Execution authority attaches to work packages and to nothing else in this
   register.
2. **Before any phase work begins, a reviewed and merged repository change must:**
   append an immutable BER-DEC authorization entry to the governance log (§13 of this
   file); identify the authorizing owner; record the exact scope; record the
   repository; record the branch; record the budget and its enforceable units; record
   the evidence path; record the evidence-handling terms (for WP-2B-0, the minimum
   spike-evidence-handling terms below); record the stop conditions; and change the
   governing work-package record from BLOCKED or BACKLOG to AUTHORIZED.
3. **A chat message, assistant memory, temporary file, or unmerged branch is not
   sufficient implementation authority.** Authority exists only once the authorization
   change is merged.
4. **Child evidence and backlog records do NOT independently move to AUTHORIZED.**
   R1–R5 remain EVIDENCE_REQUIRED until their dispositions are recorded; BER-BKL
   records remain BACKLOG until their own normal lifecycle changes them; both may be
   worked only when explicitly included in the recorded scope of an AUTHORIZED work
   package.
5. **"Only AUTHORIZED work may proceed" means:** the governing work package must be
   AUTHORIZED; child records may be executed only within that authorization's recorded
   scope; a child record's own status never grants authority.
6. **After the authorization is merged, implementation may begin** — on the separately
   named phase branch the authorization records, and nowhere else.
7. **Completion, rejection, or supersession is recorded through a later reviewed
   backlog update.** Prior BER-DEC authorization history is never edited (§13
   append-only rules of this file).

### Minimum Phase 2B-0 spike-evidence-handling terms (mandatory authorization content)

WP-2B-0 will create potentially sensitive evidence about configuration scopes,
managed/user instructions, hooks/plugins/MCP servers, auto-memory, filesystem and tool
confinement, provider/cost observability, activation event streams, and judge
calibration prompts and outputs. A minimum temporary spike-evidence policy is therefore
mandatory content of the WP-2B-0 authorization itself and must be in force before any
probe or model call runs. The authorization's recorded terms must fix:

1. the exact external evidence root;
2. the authorized evidence readers;
3. the sensitivity / data classification of the spike evidence;
4. an explicit prohibition on storing provider credentials, access tokens, passwords,
   private keys, unrestricted environment dumps, or any real secret;
5. the redaction and sanitization rules;
6. whether encryption at rest is required for the spike evidence;
7. the retention or expiration date;
8. the deletion and cleanup procedure;
9. the preserve-on-failure rule;
10. the ownership-marker and verified-cleanup requirements;
11. the repository-safe summary, evidence manifest, and hashes that must be committed
    after the spike;
12. how evidence integrity is checked before owner review.

Phase split (binding): these terms are temporary and specific to the authorized spike —
mandatory before WP-2B-0 work, and never a substitute for the final policy. BER-BKL-009
delivers the final production-grade retention / access / encryption / redaction /
deletion policy and its evidence-writer integration in Phase 2B-1. This register fixes
no permanent retention periods, access groups, or encryption technology here; those
remain the owner decisions recorded in §9 of this file.

## 3. Status vocabulary

Every record in this register carries exactly one status:

- **EVIDENCE_REQUIRED** — a Phase 2B-0 gate item: its disposition can only be produced by
  host evidence gathered under an authorized spike, never by assumption. It is not
  startable work in itself; it is resolved inside WP-2B-0 once WP-2B-0 is AUTHORIZED. An
  R record retains EVIDENCE_REQUIRED while it is investigated inside AUTHORIZED WP-2B-0
  scope; it never independently becomes AUTHORIZED (work-package authorization protocol,
  §2 of this file).
- **BACKLOG** — recorded and traceable, but neither ready for owner review nor authorized.
  The default state of future work. A BER-BKL record never moves to AUTHORIZED; while it
  is included within the recorded scope of an AUTHORIZED work package, reviewed lifecycle
  updates may move it to another applicable non-authority status such as IN_PROGRESS,
  READY_FOR_OWNER_REVIEW, DONE, REJECTED, or SUPERSEDED. No child-record status grants
  execution authority; authority remains with the governing work package.
- **READY_FOR_OWNER_REVIEW** — the item's deliverable or decision package exists and awaits
  owner review or ratification.
- **AUTHORIZED** — the owner has explicitly authorized this item with a stated scope.
  **Only the owner (Peter Nguyen) may move an item to AUTHORIZED**, and only through the
  work-package authorization protocol (§2 of this file): a reviewed and **merged**
  repository change that appends the immutable BER-DEC authorization entry and moves the
  governing work-package record to AUTHORIZED. Execution authority attaches to
  work-package records only; a chat message, assistant memory, temporary file, or
  unmerged branch is never sufficient implementation authority.
- **IN_PROGRESS** — authorized work actively underway on its own branch.
- **BLOCKED** — the item may not begin or continue: a named dependency, gate, or required
  authorization is missing. BLOCKED records why work cannot proceed; it does not imply any
  authorization exists.
- **DONE** — completed with completion evidence recorded (reviewed PR, committed report, or
  registered owner decision). Never claimed without evidence.
- **REJECTED** — the owner declined the item; it stays visible with the rationale.
- **SUPERSEDED** — replaced by a successor item; the record names its successor and remains
  visible.
- **PROHIBITED** — a standing prohibition (see the prohibited-pattern register, §11): never
  scheduled, never implemented; recorded so it cannot be mistaken for deferred work.

## 4. Priority vocabulary

- **GATE** — blocks a phase boundary. The item must reach an evidence-backed disposition
  before its dependent phase may be authorized or (for broad execution) proceed.
- **REQUIRED** — necessary for the v1 runner as designed; its owning phase is incomplete
  without it.
- **IMPORTANT** — materially improves its phase's outcome and is planned within it, but its
  absence does not block the phase boundary.
- **FUTURE** — explicitly deferred beyond v1. Never blocks any v1 phase unless the merged
  design names it a gate (it names none).
- **PROHIBITED** — never implemented; an anti-feature recorded to prevent it.

This register deliberately does **not** use P0/P1/P2: those labels already carry meanings
elsewhere in Project Aegis (roadmap phase priorities in
[`docs/roadmaps/product-agnostic-skill-and-agent-roadmap.md`](product-agnostic-skill-and-agent-roadmap.md)
and finding/severity language in the audit corpus), and reusing them here would collide
with that vocabulary.

## 5. Backlog-record schema

Every record in §6 (evidence gates), §7 (work packages), §8 (backlog inventory), and §11
(prohibited patterns) carries all of the following fields, none empty:

- **ID**
- **Title**
- **Phase**
- **Priority**
- **Status**
- **Source / evidence**
- **Why it matters**
- **Dependencies**
- **Trigger to begin**
- **Expected deliverable**
- **Acceptance criteria**
- **Owner decision required**
- **Explicit non-goals**
- **Related design sections**
- **Completion evidence**
- **Supersedes / superseded by**

Prohibited-pattern records populate the same fields with standing-prohibition semantics
(e.g. *Trigger to begin: none — never scheduled*), so a reader can never mistake a
prohibition for schedulable work. Prohibited-pattern records may populate the shared
Phase, Priority, Status, Dependencies, Trigger to begin, Owner decision required,
Completion evidence, and Supersedes / superseded by fields through the explicit
shared-field declaration in §11 of this file; those inherited values count as populated
required fields. The owner-decision register (§9), future-consideration
register (§10), and append-only governance log (§13) use the explicit field sets defined
in their own sections.

Section references of the form §N below refer to sections of the merged design
([`docs/design/behavioral-eval-runner-v1.md`](../design/behavioral-eval-runner-v1.md))
unless the text says otherwise.

---

## 6. Phase 2B-0 evidence gates — R1–R5

The merged design defers exactly five items to Phase 2B-0 as evidence-required (design
§20 "Remaining — DEFERRED TO 2B-0 — EVIDENCE REQUIRED"). Their identifiers and meanings
are preserved here exactly. For every R record: Phase = 2B-0; Priority = GATE; the
Status preserves the record's final evidence-backed post-2B-0 state under Outcome B /
Limited Scope ([PR #81](https://github.com/ModernNomad-98/Project-Aegis/pull/81)).
DONE means the authorized WP-2B-0 evidence task reached a complete, owner-accepted
disposition — NOT that the underlying host capability is proven or technically solved.
BLOCKED means the required technical gate remains unmet even though the 2B-0 evidence
attempt and its evidence are closed. The recorded limitations remain binding on later
phases, and **no status grants implementation authority — none is implied by a
record's existence**.

### R1 — Activation-observation mechanism and truthful v1 claim scope

- **ID:** R1
- **Title:** Activation-observation mechanism and the truthful scope of v1's claims
- **Phase:** 2B-0
- **Priority:** GATE
- **Status:** DONE — WP-2B-0 evidence disposition accepted as UNAVAILABLE / UNKNOWN under
  Outcome B. Activation-identifying evidence was not proven. Activation-dependent
  implementation and live-routing claims remain blocked pending later evidence.
- **Source / evidence:** Merged design §6 (evidence tiers; ambiguity ⇒ `ERROR` /
  `AMBIGUOUS_ACTIVATION`), §17a items 1–5, §20 R1. Carried into this register by the
  owner's backlog-creation directive of 2026-08-10.
- **Why it matters:** Determining what skill actually activated is the design's central
  hard problem. Model prose such as `→ invokes X` is a claim, not proof. Without a proven
  activation-identifying mechanism, no positive or negative routing verdict is truthful,
  in either direction.
- **Dependencies:** This backlog merged; WP-2B-0 DONE under Outcome B / Limited Scope —
  the owner accepted R1's disposition with PR #81; BER-DEC-005 is executed and closed.
- **Trigger to begin:** CLOSED — no further WP-2B-0 work is authorized by BER-DEC-005;
  the R1 evidence task is complete. Any follow-up activation probe requires a new
  reviewed and merged authorization.
- **Expected deliverable:** An activation observability report that determines, by evidence
  on the real host, whether Claude Code exposes a reliable, structured,
  activation-identifying signal (Tier 1), and/or whether any specific Tier-2 output
  signature passes the design's full promotion proof (uniqueness against the collision
  set, base-model-imitation resistance, other-skill-emission resistance, fresh-session
  stability, measured false-positive/false-negative rates, explicit owner approval of the
  claim scope).
- **Acceptance criteria:** R1 ends in exactly one activation-specific disposition:
  (1) an activation-identifying mechanism proven with a bounded, evidence-backed claim
  scope; or (2) an owner-approved Tier-2 signature claim scope after the full §6
  signature-promotion proof; or (3) activation-identifying evidence recorded as
  unavailable/unknown, with the limitation recorded. R1's disposition alone does NOT
  establish WP-2B-0 outcome A or B: outcome A/B is decided only by WP-2B-0 after R1–R5
  all have evidence-backed dispositions, and outcome A requires the activation
  mechanism plus the isolation boundary and per-tool-path confinement (R4) and
  execution-profile observability/isolation (R5), as defined in the merged design
  (§17a item 10). Broad general-corpus execution remains blocked. No Claude Code API,
  event stream, hook, or telemetry source is assumed; ambiguous evidence remains
  `ERROR` / `AMBIGUOUS_ACTIVATION`, never a verdict.
- **Owner decision required:** RESOLVED for WP-2B-0 — the owner accepted R1's
  disposition 3 (limitation recorded: activation-identifying evidence UNAVAILABLE /
  UNKNOWN) together with the Outcome B / Limited Scope decision. Any later
  activation-mechanism proof, Tier-2 signature promotion, or narrower claim-scope
  approval remains a separate future owner decision.
- **Explicit non-goals:** No runner construction; no broad corpus execution; no invented
  host telemetry; no treatment of routing prose or name mentions as activation evidence.
- **Related design sections:** §6, §17a (items 1–5, 10), §19 (2B-0 row), §20 R1, §22
  (activation risk row), §24.
- **Completion evidence:** [PR #81](https://github.com/ModernNomad-98/Project-Aegis/pull/81)
  (merge commit `55b0c4b4f5c0cba9bbf70f63cd0ebf8212f8eae5`); the repository-safe summary
  [`docs/evidence/behavioral-eval-runner-wp-2b-0-summary.md`](../evidence/behavioral-eval-runner-wp-2b-0-summary.md);
  the evidence manifest
  [`artifacts/evidence/behavioral-eval-runner-wp-2b-0-manifest.json`](../../artifacts/evidence/behavioral-eval-runner-wp-2b-0-manifest.json);
  the detached finalization marker
  [`artifacts/evidence/behavioral-eval-runner-wp-2b-0-finalization.json`](../../artifacts/evidence/behavioral-eval-runner-wp-2b-0-finalization.json);
  and the owner-side integrity gate PASS.
- **Supersedes / superseded by:** None.

### R2 — Exact judge model/version and measured calibration result

- **ID:** R2
- **Title:** Exact pinned judge model/version and its measured calibration result
- **Phase:** 2B-0
- **Priority:** GATE
- **Status:** BLOCKED — WP-2B-0 ended under Outcome B / Limited Scope without the
  measured judge calibration required by the merged design. No judge was pinned, no
  calibration dataset was executed, and OD-1 remains OPEN. The WP-2B-0 evidence attempt
  is complete, but the R2 technical gate is not.
- **Source / evidence:** Merged design §8 (measurable judge calibration; §20a-S28), §17a
  item 9, §20 D1 and R2, OD-1. Carried into this register by the owner's backlog-creation
  directive of 2026-08-10.
- **Why it matters:** The judge policy is decided (D1: pinned, independent,
  injection-defended), but an unmeasured calibration cannot be accepted, compared, or
  re-verified. Until a concrete judge identity produces a measured result that meets
  owner-ratified thresholds, no baseline-eligible semantic verdict may exist — and
  critical safety assertions carry a separately approved critical false-PASS bound.
- **Dependencies:** The WP-2B-0 evidence attempt and owner disposition are complete
  through [PR #81](https://github.com/ModernNomad-98/Project-Aegis/pull/81); measured
  calibration remains absent; OD-1 remains open; any future R2 work requires a new
  reviewed and merged authorization.
- **Trigger to begin:** BLOCKED — no further work is authorized by BER-DEC-005. A new
  phase-specific authorization must provide the calibration scope, model budget,
  evidence terms, and stop conditions before R2 work resumes.
- **Expected deliverable:** A pinned judge identity (model/version); a versioned,
  human-labeled calibration dataset (`calibration_dataset_version/hash`); and a measured
  calibration report containing the full confusion matrix, accuracy/agreement, false-PASS
  rate, false-FAIL rate, abstention/`JUDGE_ERROR` rate, and the critical-vs-standard
  split, including the adversarial injection subset results.
- **Acceptance criteria:** The measured result is presented for owner ratification against
  OD-1 numeric thresholds, including the separate critical false-PASS threshold; the
  judge produces no baseline-eligible semantic verdict before the ratified thresholds are
  met; judge failure paths resolve to `JUDGE_ERROR`, never PASS/FAIL; any later judge,
  rubric-derivation, or dataset change is recorded as requiring re-calibration and
  behavioral re-baselining.
- **Owner decision required:** The owner accepted the incomplete/blocked WP-2B-0
  disposition. The required judge identity, measured calibration, and OD-1 ratification
  remain open; no baseline-eligible semantic judging is permitted.
- **Explicit non-goals:** No invented threshold numbers (the design deliberately invents
  none); no production semantic judging; no hard-coded model name in the design.
- **Related design sections:** §8, §13 (calibration-dataset identity in
  `baseline_identity`), §17 criterion 9, §17a item 9, §20 D1/OD-1/R2, §22 (judge risk
  rows).
- **Completion evidence:** [PR #81](https://github.com/ModernNomad-98/Project-Aegis/pull/81)
  (merge commit `55b0c4b4f5c0cba9bbf70f63cd0ebf8212f8eae5`) records the completed 2B-0
  attempt and its blocked R2 result via the repository-safe summary
  [`docs/evidence/behavioral-eval-runner-wp-2b-0-summary.md`](../evidence/behavioral-eval-runner-wp-2b-0-summary.md),
  the evidence manifest
  [`artifacts/evidence/behavioral-eval-runner-wp-2b-0-manifest.json`](../../artifacts/evidence/behavioral-eval-runner-wp-2b-0-manifest.json),
  and the detached finalization marker
  [`artifacts/evidence/behavioral-eval-runner-wp-2b-0-finalization.json`](../../artifacts/evidence/behavioral-eval-runner-wp-2b-0-finalization.json).
  The required measured-calibration deliverable is NOT completed, and no completion of
  it is claimed here.
- **Supersedes / superseded by:** None.

### R3 — Monetary-cost observability versus enforceable proxies

- **ID:** R3
- **Title:** Monetary-cost observability versus enforceable proxy reservation
- **Phase:** 2B-0
- **Priority:** GATE
- **Status:** DONE — WP-2B-0 evidence disposition accepted as UNAVAILABLE / UNKNOWN under
  Outcome B. The ordinary Claude Code control session did not prove direct monetary
  reservation or a complete pre-dispatch proxy envelope. WP-2B-1 may build and
  deterministically test runner-owned enforcement, but no live enforcement claim is
  authorized.
- **Source / evidence:** Merged design §11 (pre-dispatch reservation; monetary-`UNKNOWN`
  fallback), §17a (closing constraint), §20 D3 (as corrected by §20a-S3) and R3. Carried
  into this register by the owner's backlog-creation directive of 2026-08-10.
- **Why it matters:** The owner-ratified ceilings (PR ≤ $5/run; daily ≤ $20; cadence ≤
  $20/run; full corpus disabled by default) are enforceable only if reservation happens
  before dispatch in units the provider surface actually exposes. Whether monetary cost is
  observable — or only token/call/turn/session proxies are — is a host-evidence question,
  and fabricated dollar accounting is prohibited.
- **Dependencies:** This backlog merged; WP-2B-0 DONE under Outcome B / Limited Scope —
  the owner accepted R3's disposition with PR #81; BER-DEC-005 is executed and closed.
- **Trigger to begin:** CLOSED — no further WP-2B-0 work is authorized by BER-DEC-005;
  the R3 evidence task is complete (zero dispatches; envelope not provable in-session).
  Any follow-up cost probe requires a new reviewed and merged authorization.
- **Expected deliverable:** A cost-observability report establishing whether cost can be
  enforced through direct monetary reservation, or must be enforced through
  provider-enforced token/call/turn/session ceilings with monetary cost reported
  `UNKNOWN`.
- **Acceptance criteria:** The report names the enforceable reservation unit(s) proven on
  the real host; every enforcement claim traces to evidence; if monetary data is
  unavailable, the recorded disposition adopts the design's decided fallback (proxy
  reservation + monetary `UNKNOWN` + stop at the enforceable cap) with no fabricated
  dollar figures anywhere.
- **Owner decision required:** RESOLVED for WP-2B-0 — the owner accepted R3's
  UNAVAILABLE / UNKNOWN disposition as the basis for WP-2B-1's non-live, runner-owned
  reservation implementation. No live host/provider enforcement claim is authorized;
  later live phases require their own evidence and authorization.
- **Explicit non-goals:** No spend beyond WP-2B-0's own approved spike budget; no
  reservation implementation (that is WP-2B-1); no cost prediction presented as fact.
- **Related design sections:** §11, §11a, §13 (cost accounting fields), §17a, §20 D3/R3,
  §22 (cost risk rows).
- **Completion evidence:** [PR #81](https://github.com/ModernNomad-98/Project-Aegis/pull/81)
  (merge commit `55b0c4b4f5c0cba9bbf70f63cd0ebf8212f8eae5`); the repository-safe summary
  [`docs/evidence/behavioral-eval-runner-wp-2b-0-summary.md`](../evidence/behavioral-eval-runner-wp-2b-0-summary.md);
  the evidence manifest
  [`artifacts/evidence/behavioral-eval-runner-wp-2b-0-manifest.json`](../../artifacts/evidence/behavioral-eval-runner-wp-2b-0-manifest.json);
  the detached finalization marker
  [`artifacts/evidence/behavioral-eval-runner-wp-2b-0-finalization.json`](../../artifacts/evidence/behavioral-eval-runner-wp-2b-0-finalization.json);
  and the owner-side integrity gate PASS.
- **Supersedes / superseded by:** None.

### R4 — OS/host isolation and per-tool-path confinement

- **ID:** R4
- **Title:** OS/host isolation mechanism and per-tool-path confinement evidence
- **Phase:** 2B-0
- **Priority:** GATE
- **Status:** DONE — WP-2B-0 evidence disposition accepted as INCOMPLETE / BLOCKED under
  Outcome B. Effective per-tool-path confinement was not proven. Live execution remains
  blocked pending later evidence.
- **Source / evidence:** Merged design §15 (containment-first model; eleven enumerated
  tool paths; §20a-S13/S20), §5a (control-plane inaccessibility), §17a items 6–7, §18
  (benchmark-contamination probes), §20 R4. Carried into this register by the owner's
  backlog-creation directive of 2026-08-10.
- **Why it matters:** The runner executes an agent. Path checks and ownership markers
  protect the runner's cleanup; they are not an agent sandbox. Without an OS/host-enforced
  boundary proven per tool path, live behavioral execution cannot be contained, and the
  control-plane eval corpus (case definitions, expectations, rubrics, answer banks) cannot
  be proven unreachable from the system under test.
- **Dependencies:** This backlog merged; WP-2B-0 DONE under Outcome B / Limited Scope —
  the owner accepted R4's disposition with PR #81; BER-DEC-005 is executed and closed.
- **Trigger to begin:** CLOSED — no further WP-2B-0 work is authorized by BER-DEC-005;
  the R4 evidence task is complete (effective per-tool-path probes did not run under the
  envelope gate). Any follow-up containment probe requires a new reviewed and merged
  authorization.
- **Expected deliverable:** A containment capability report proving, by probe against the
  real host (never config inspection alone), effective confinement for every design-
  enumerated path: shell/subprocess execution; built-in Read; built-in Edit/Write;
  WebFetch/network-fetch tools; MCP tools; plugin-provided tools; hook execution;
  subagent tool permissions; unsandboxed-command escape behavior; excluded/exempted
  commands; and the merged effective permission rules after all configuration scopes
  combine — plus control-plane eval-corpus inaccessibility through every path.
- **Acceptance criteria:** Each path receives an evidence-backed confinement verdict; the
  §15 boundary contract items (workspace-only writes, read-only corpus, caller-directory
  inaccessibility, no provider credentials in the sandbox, deny-by-default egress, bounded
  process lifetime, tree-wide emergency kill) are proven or explicitly recorded as
  unavailable; benchmark-contamination probes fail closed; an unconfinable path blocks
  broad execution or the host adapter entirely, with owner approval required for any
  narrower claim.
- **Owner decision required:** RESOLVED for WP-2B-0 — the owner accepted R4's
  INCOMPLETE / BLOCKED disposition. Approval of any narrower v1 claim scope remains a
  later owner decision, available only when live evidence exists; no such approval is
  granted here.
- **Explicit non-goals:** No assumption that a sandboxed shell confines non-shell tool
  paths; no invented sandbox feature; no broad live execution while any relevant path is
  unproven.
- **Related design sections:** §5a, §15, §17a items 6–7, §18 (containment and
  contamination tests), §20 R4, §22 (containment risk rows).
- **Completion evidence:** [PR #81](https://github.com/ModernNomad-98/Project-Aegis/pull/81)
  (merge commit `55b0c4b4f5c0cba9bbf70f63cd0ebf8212f8eae5`); the repository-safe summary
  [`docs/evidence/behavioral-eval-runner-wp-2b-0-summary.md`](../evidence/behavioral-eval-runner-wp-2b-0-summary.md);
  the evidence manifest
  [`artifacts/evidence/behavioral-eval-runner-wp-2b-0-manifest.json`](../../artifacts/evidence/behavioral-eval-runner-wp-2b-0-manifest.json);
  the detached finalization marker
  [`artifacts/evidence/behavioral-eval-runner-wp-2b-0-finalization.json`](../../artifacts/evidence/behavioral-eval-runner-wp-2b-0-finalization.json);
  and the owner-side integrity gate PASS.
- **Supersedes / superseded by:** None.

### R5 — Execution-profile observability and isolation

- **ID:** R5
- **Title:** Execution-profile observability and isolation
- **Phase:** 2B-0
- **Priority:** GATE
- **Status:** DONE — WP-2B-0 evidence disposition accepted as INCOMPLETE / BLOCKED under
  Outcome B. Execution-profile isolation was not proven. Baseline eligibility and live
  execution remain blocked pending later evidence.
- **Source / evidence:** Merged design §5e (pinned execution-profile contract; §20a-S19),
  §13 (`baseline_identity` includes the execution profile), §17a item 8, §20 R5. Carried
  into this register by the owner's backlog-creation directive of 2026-08-10.
- **Why it matters:** A fresh session is not automatically a clean system under test:
  managed/user/project/local settings, user-level `CLAUDE.md`, auto-memory, user-scope
  skills and subagents, plugins, hooks, and MCP servers can load from outside the
  materialized workspace and silently change behavior. Runs whose configuration surface
  cannot be observed and isolated are non-baseline-eligible by design.
- **Dependencies:** This backlog merged; WP-2B-0 DONE under Outcome B / Limited Scope —
  the owner accepted R5's disposition with PR #81; BER-DEC-005 is executed and closed.
- **Trigger to begin:** CLOSED — no further WP-2B-0 work is authorized by BER-DEC-005;
  the R5 evidence task is complete (partial existence-level observability recorded;
  isolation not proven). Any follow-up profile probe requires a new reviewed and merged
  authorization.
- **Expected deliverable:** An execution-profile isolation report establishing, for the
  real host, whether each element of the configuration surface can be controlled or
  accurately observed: configuration scopes (managed/user/project/local settings);
  `CLAUDE.md` scopes; auto-memory; user- and project-scope skills; subagents; plugins;
  hooks; MCP servers; permission, sandbox, and tool policy; and runtime version /
  auto-update state.
- **Acceptance criteria:** Every §5e candidate control is verified on the real host or
  recorded as a limitation; whatever cannot be observed or isolated is classified
  unavailable/unknown — never assumed — and affected runs are marked
  non-baseline-eligible, excluded from stability windows and promotion accounting. No
  configuration-isolation flag is invented.
- **Owner decision required:** RESOLVED for WP-2B-0 — the owner accepted R5's
  INCOMPLETE / BLOCKED disposition and its baseline-eligibility consequences (affected
  runs remain non-baseline-eligible until isolation is proven by later evidence).
- **Explicit non-goals:** No assumption of any Claude Code isolation switch; no silent
  inheritance of developer-personal configuration into recorded baselines.
- **Related design sections:** §5e, §13, §17 criterion 1, §17a item 8, §18
  (execution-profile tests), §20 R5, §22 (hidden-configuration risk row).
- **Completion evidence:** [PR #81](https://github.com/ModernNomad-98/Project-Aegis/pull/81)
  (merge commit `55b0c4b4f5c0cba9bbf70f63cd0ebf8212f8eae5`); the repository-safe summary
  [`docs/evidence/behavioral-eval-runner-wp-2b-0-summary.md`](../evidence/behavioral-eval-runner-wp-2b-0-summary.md);
  the evidence manifest
  [`artifacts/evidence/behavioral-eval-runner-wp-2b-0-manifest.json`](../../artifacts/evidence/behavioral-eval-runner-wp-2b-0-manifest.json);
  the detached finalization marker
  [`artifacts/evidence/behavioral-eval-runner-wp-2b-0-finalization.json`](../../artifacts/evidence/behavioral-eval-runner-wp-2b-0-finalization.json);
  and the owner-side integrity gate PASS.
- **Supersedes / superseded by:** None.

---

## 7. Phase work-package register — WP-2B-0 … WP-2B-7

One work package per merged-design implementation phase (design §19). Dependencies follow
the design's corrected implementation order (§20a-S7): every minimum guardrail lands in
2B-1, before any live phase; no later phase may erase an earlier phase's evidence
boundary. Statuses: WP-2B-0 is DONE — Outcome B / Limited Scope accepted (BER-DEC-005
executed; evidence and owner decision merged through
[PR #81](https://github.com/ModernNomad-98/Project-Aegis/pull/81)); WP-2B-1 is DONE —
authorized by BER-DEC-006 ([PR #82](https://github.com/ModernNomad-98/Project-Aegis/pull/82))
and completed through the merged offline runner core
([PR #83](https://github.com/ModernNomad-98/Project-Aegis/pull/83), merge commit
`72e74af6f0183fef25e353ec2bf3a851d83b5df6`); WP-2B-2 is the revised **Scenario A Grading
Stack** (combined non-live deterministic + semantic grading), AUTHORIZED by BER-DEC-007 (§13
of this file), effective only after the governance PR containing BER-DEC-007 is reviewed and
merged; WP-2B-3 is SUPERSEDED BY WP-2B-2 (historical record retained); WP-2B-4 is the
separate, BLOCKED Scenario A Limited-Scope Live Suite; and WP-2B-5 through WP-2B-7 remain
BACKLOG.

### WP-2B-0 — Capability and evidence spike

- **ID:** WP-2B-0
- **Title:** Activation observability + host & isolation capability spike (implementation
  gate)
- **Phase:** 2B-0
- **Priority:** GATE
- **Status:** DONE — Outcome B / Limited Scope accepted by Peter Nguyen. The capability
  spike and evidence package are complete. R1/R3 remain unavailable/unknown; R2/R4/R5
  remain incomplete/blocked. Outcome A is not claimed. Live behavioral execution
  remains blocked. This administrative phase closure does not claim that R2's measured
  judge-calibration requirement was fulfilled — R2 remains a BLOCKED technical gate
  carried forward.
- **Source / evidence:** Merged design §17a and §19 (2B-0 row); §20 R1–R5; owner
  backlog-creation directive of 2026-08-10.
- **Why it matters:** The design forbids building a runner around assumed telemetry, an
  assumed sandbox, an assumed configuration-isolation switch, or an unmeasured judge. The
  spike converts each assumption into evidence or an owner-approved limitation before any
  general construction or broad execution.
- **Dependencies:** SATISFIED for WP-2B-0 completion through
  [PR #81](https://github.com/ModernNomad-98/Project-Aegis/pull/81) and the owner
  integrity gate.
- **Trigger to begin:** CLOSED — no additional work is authorized under BER-DEC-005.
  Any follow-up probe requires a new reviewed and merged authorization.
- **Expected deliverable:** The activation observability report (R1); the containment
  capability report (R4); the execution-profile isolation report (R5); the
  cost-observability report (R3); the measured judge-calibration report (R2); and an
  owner go / no-go / limited-scope decision recording 2B-0's outcome (A or B).
- **Acceptance criteria:** R1–R5 each receive an evidence-backed disposition; unknowns
  remain explicitly unknown (classified proven / owner-approved limitation /
  unavailable-unknown); no broad corpus execution occurs; no host capability is invented;
  spike spend stays within its authorized budget and stop conditions; every probe and
  model call runs under the authorization's minimum spike-evidence-handling terms, and
  all spike evidence is created, stored, redacted, retained, and cleaned up per those
  terms.
- **Owner decision required:** RESOLVED for the WP-2B-0 aggregate outcome: Outcome B /
  Limited Scope accepted. OD-1 remains OPEN.
- **Explicit non-goals:** No runner core construction; no Scenario A or corpus execution;
  no CI wiring; no judge production use; no modification of skills, evals, the validator,
  or the merged design.
- **Related design sections:** §6, §8, §11, §15, §5e, §17a, §19 (2B-0), §20 (OD-1,
  R1–R5).
- **Completion evidence:** [PR #81](https://github.com/ModernNomad-98/Project-Aegis/pull/81);
  merge commit `55b0c4b4f5c0cba9bbf70f63cd0ebf8212f8eae5`; the three merged evidence
  files ([`docs/evidence/behavioral-eval-runner-wp-2b-0-summary.md`](../evidence/behavioral-eval-runner-wp-2b-0-summary.md),
  [`artifacts/evidence/behavioral-eval-runner-wp-2b-0-manifest.json`](../../artifacts/evidence/behavioral-eval-runner-wp-2b-0-manifest.json),
  [`artifacts/evidence/behavioral-eval-runner-wp-2b-0-finalization.json`](../../artifacts/evidence/behavioral-eval-runner-wp-2b-0-finalization.json));
  and the owner-side integrity-gate verification record below. This reviewed
  repository record — not conversation memory — is the durable record of the owner
  verification:
  - **Verification owner:** Peter Nguyen
  - **Verification date:** 2026-08-11
  - **Verification result:** PASS
  - **Repository-safe summary SHA-256:**
    `a18b18899272a96826fa6d1bb4af1908782c3fb03bd591afefdd83bd21816374`
  - **Evidence manifest SHA-256:**
    `f304b889477a4c72f55c1462c9079f02efa9ede87d7cc5c3376d542376dd3969`
  - **Detached finalization marker SHA-256:**
    `c33bd26edac562c12578ff1b2231c440718d2bbbd1b19ad7e365f60b862b543c`
  - **External-artifact result:** all 12 manifest-listed external artifacts matched
    their recorded byte counts and SHA-256 values.
  - **Path-safety result:** no reparse point was found in the validated path chains.
  - **Verification mode:** independent owner-run, read-only PowerShell integrity gate.
- **Supersedes / superseded by:** None.

### WP-2B-1 — Runner core and versioned contracts

- **ID:** WP-2B-1
- **Title:** Runner core, minimum guardrails, and versioned contracts
- **Phase:** 2B-1
- **Priority:** REQUIRED
- **Status:** DONE — authorized by BER-DEC-006 (merged via
  [PR #82](https://github.com/ModernNomad-98/Project-Aegis/pull/82)) and completed through the
  reviewed and merged offline runner core
  ([PR #83](https://github.com/ModernNomad-98/Project-Aegis/pull/83), merge commit
  `72e74af6f0183fef25e353ec2bf3a851d83b5df6`). Scope was limited to the non-live runner core
  and minimum guardrails recorded by BER-DEC-006; no live dispatch, no Scenario A, no
  graders, no semantic judge.
- **Source / evidence:** Merged design §19 (2B-1 row) and the sections it delivers (§3
  census items a–k, §5, §5a, §5b, §5e, §10, §11, §11a, §13, §14, §15); owner
  backlog-creation directive of 2026-08-10.
- **Why it matters:** Per §20a-S7, every minimum guardrail must exist and be tested before
  any live phase: containment, timeouts, emergency kill, budget reservation, attempt
  recording, aggregate semantics, and bounded concurrency. 2B-1 is where the runner's
  honest result model and evidence machinery become code.
- **Dependencies:** WP-2B-0 is DONE under Outcome B / Limited Scope;
  [PR #81](https://github.com/ModernNomad-98/Project-Aegis/pull/81) evidence and the
  owner decision are merged; R1–R5 limitations remain binding; BER-DEC-006 is the
  governing authorization.
- **Trigger to begin:** This governance PR (the reviewed PR containing BER-DEC-006) is
  manually merged; implementation occurs only on `feat/behavioral-eval-runner-2b-1`;
  the implementation branch starts from this governance PR's exact squash-merge commit
  and tree; the build-evidence root is absent or validly owned; all implementation
  remains offline and non-live; and no package installation is required.
- **Expected deliverable:** The runner core entry point; versioned attempt/aggregate/run
  schemas (`attempt_state`; `aggregate_verdict` + `aggregate_blocker`; coverage metrics);
  case and fixture manifest schemas (capability/fixture fields of §5b, keyed by
  `case_uid`/`assertion_uid`); the workspace materializer (immutable Git-object snapshot,
  two-surface separation, three separately-hashed manifests, materialization profiles,
  landmark exclusion); the sanitized runtime-surface builder with the runtime-file
  classification census; the capability preflight; containment delivered as
  fail-closed containment interfaces, contracts, adapters, and guards — with a
  deterministic mock/synthetic containment implementation used only by offline tests, a
  real-host implementation state of unavailable/unknown unless later evidence supplies
  an R4-proven boundary, no real-host containment integration claim, and no live path
  becoming enabled; timeouts and emergency kill (process-tree-wide); bounded
  concurrency; budget and reservation delivered as runner-owned reservation,
  reconciliation, concurrency, timeout, deadline, and kill state machines — with
  deterministic tests using configured synthetic/mock call, turn, token, session, and
  monetary units, the real Claude Code/provider adapter reporting reservation
  capability unavailable/unknown and denying live dispatch until later R3 evidence
  identifies enforceable units, and no host/provider enforcement claim; the
  deterministic budget-aware scheduler (§11a); evidence finalization (two-stage bundles + detached
  marker); the N/quorum attempt controller; the host-adapter interface with the Claude
  Code adapter; the report generator (attempt-level `UNRUN` default; coverage metrics in
  every report); and the machine-generated corpus census (BER-BKL-008).
- **Acceptance criteria:** Design §23 build-acceptance items applicable to 2B-1 hold under
  the §18 test strategy with zero runner-generated model/provider dispatches, zero live
  Claude Code sessions, and no live behavioral execution in this phase; all tests use
  mocks, recorded synthetic fixtures, or local deterministic harnesses; any future live
  smoke requires a separate reviewed authorization outside WP-2B-1; every §5b concept
  remains addressed in the final schemas; the structural validator remains
  untouched. Outcome B constraint: WP-2B-1 passes only when its code and tests honestly
  represent unproven capabilities as unavailable/unknown and keep every live-dispatch
  path disabled. Unit tests may prove runner-owned control logic; they do not prove
  host/provider enforcement or containment.
- **Owner decision required:** WP-2B-1 authorization is recorded by BER-DEC-006. Final
  schema-shape acceptance (BER-BKL-007) and OD-3 risk-class ratification remain owner
  decisions at implementation review. No later phase is authorized.
- **Explicit non-goals:** No semantic judging in production; no Scenario A live suite; no
  generic corpus execution; no CI integration; no relaxation of any 2B-0 evidence
  boundary.
- **Related design sections:** §3, §5, §5a–§5e, §10, §11, §11a, §13, §14, §15, §18, §19
  (2B-1).
- **Completion evidence:** [PR #83](https://github.com/ModernNomad-98/Project-Aegis/pull/83)
  (merge commit `72e74af6f0183fef25e353ec2bf3a851d83b5df6`) — the reviewed and merged offline
  runner core with passing runner self-tests; sanitized summary at
  [`docs/evidence/behavioral-eval-runner-wp-2b-1-summary.md`](../evidence/behavioral-eval-runner-wp-2b-1-summary.md)
  (post-merge record appended, §14). Status updated here through this reviewed governance PR.
- **Supersedes / superseded by:** None.

### WP-2B-2 — Scenario A Grading Stack (deterministic + semantic, non-live)

- **ID:** WP-2B-2
- **Title:** Scenario A Grading Stack — combined non-live deterministic + semantic grading
- **Phase:** 2B-2
- **Priority:** REQUIRED
- **Status:** AUTHORIZED — authorized by BER-DEC-007 (§13 of this file), effective only after
  the governance PR containing BER-DEC-007 is reviewed and manually merged. Scope is limited
  to the non-live deterministic + semantic grading recorded by BER-DEC-007 and the v1.1
  fast-track successor.
- **Source / evidence:** The v1.1 fast-track successor
  [`docs/design/behavioral-eval-runner-v1-fast-track-successor.md`](../design/behavioral-eval-runner-v1-fast-track-successor.md)
  (authoritative for this revised scope); merged design §5c, §5d, §6, §7, §8, §9, §13, §18,
  §19 (2B-2/2B-3 rows); owner clarification of 2026-08-13.
- **Why it matters:** The fast track combines everything gradable for Scenario A — the
  Scenario-A-required deterministic graders and the NON-LIVE semantic-judge scaffold — into a
  single reviewed work package, so Scenario A grading is built and tested offline before any
  live phase, while the measured calibration and live judge use stay gated ahead of WP-2B-4.
- **Dependencies:** WP-2B-1 DONE ([PR #83](https://github.com/ModernNomad-98/Project-Aegis/pull/83));
  R1 disposition (the activation matcher is built only on the 2B-0-proven mechanism, else
  `ERROR` / `AMBIGUOUS_ACTIVATION`); owner authorization for WP-2B-2 (BER-DEC-007).
- **Trigger to begin:** The governance PR containing BER-DEC-007 is manually merged;
  implementation occurs only on `feat/behavioral-eval-runner-2b-2-scenario-a-grading-stack`;
  the implementation branch starts from that governance PR's exact squash-merge commit and
  tree; the build-evidence root is absent or validly owned; all implementation remains
  offline and non-live; and no package installation is required.
- **Expected deliverable:** (A) the Scenario-A-required deterministic graders —
  stage-transition validation; authorization/approval-boundary validation; prohibited-action
  and mutation checks (no network egress, no package install, no git mutation, no
  deploy/migration — verified from the contained sandbox); append-only evidence checks;
  run-local preview-versus-created hashing (never fixture-pin digests on live output);
  recording-state checks; typed skill/subagent target handling (§5d); invocation-mode
  validation where evidence supports it (§5c); deterministic Scenario A controls A–Q;
  versioned deterministic reason codes; evidence pointers; deterministic recorded good/bad
  fixtures; and unit/integration/schema tests. (B) the NON-LIVE semantic grading scaffold —
  an independent judge interface; pinned judge-identity representation; injection-resistant
  system policy; transcript treated as delimited untrusted data; no judge tools;
  least-context input envelope; schema-validated structured verdict; `JUDGE_ERROR`
  fail-closed behavior; the coherent-topic grading contract; the other Scenario A assertions
  that cannot be mechanically graded; a minimum versioned human-labeled calibration-dataset
  structure; a deterministic/mock calibration harness; threshold-enforcement logic over
  recorded/mock results; a drift/recalibration trigger representation; and
  unit/integration/injection-defense/schema tests. All semantic behavior is exercised with
  deterministic mocks and recorded fixtures only.
- **Acceptance criteria:** §18 grader tests pass over recorded good/bad fixture transcripts;
  a skill node never satisfies a subagent expectation; prose-only activation evidence yields
  `ERROR`, never a verdict; fixture-pin comparison against live output is provably absent; the
  semantic scaffold passes with a mock judge (injection-defense probes; threshold enforcement
  rejecting an under-threshold mock result) and its contracts consume only stage-A
  input-manifest-verified artifacts (§13); zero model/provider/judge dispatch occurs; no
  measured calibration result is produced or claimed; results carry evidence pointers and are
  reproducible from the same transcript. Non-live constraint: WP-2B-2 passes only when its
  code and tests keep every live-dispatch path disabled and represent measured calibration
  and R1/R2/R4/R5 as unproven.
- **Owner decision required:** Phase authorization (BER-DEC-007). Assertion-classification
  sign-off (D9 authority, Peter Nguyen) applies to the rubric-derivation contracts at
  implementation review. No later phase is authorized; OD-1 is not ratified here.
- **Explicit non-goals:** No actual model/provider/judge call; no measured judge calibration;
  no OD-1 ratification; no Scenario A live execution; no WP-2B-4 implementation; no generic
  corpus execution or generic grader/judge breadth (deferred to WP-2B-5); no CI integration;
  no weakening of the mechanical Scenario A harness (which stays unchanged); no
  skill/eval/validator/gate/design modification beyond the four authorized governance docs.
- **Related design sections:** §5c, §5d, §6, §7, §8, §9, §13, §18, §19 (2B-2/2B-3); v1.1
  fast-track successor §3–§6.
- **Completion evidence:** Reviewed and merged WP-2B-2 PR(s) with passing grader and
  mock-judge harness tests; status updated here through a reviewed PR.
- **Supersedes / superseded by:** Supersedes the former WP-2B-3 (semantic judge) by absorbing
  its non-live scaffold; the measured-calibration and live portion of the former WP-2B-3
  remains a future requirement gated ahead of WP-2B-4.

### WP-2B-3 — Semantic judge (SUPERSEDED BY WP-2B-2)

- **ID:** WP-2B-3
- **Title:** Independent injection-resistant semantic judge
- **Phase:** 2B-3
- **Priority:** REQUIRED
- **Status:** SUPERSEDED BY WP-2B-2 (v1.1 fast-track successor; BER-DEC-007, 2026-08-13) —
  historical record retained (governance rule 5). The NON-LIVE injection-resistant judge
  scaffold, calibration-harness structure, threshold-enforcement logic, and `JUDGE_ERROR`
  handling are delivered inside WP-2B-2 (non-live; mock/recorded only). The measured
  calibration, OD-1 ratification, and any live judge use remain a future requirement gated
  ahead of WP-2B-4. No separate WP-2B-3 implementation is scheduled.
- **Source / evidence:** Merged design §19 (2B-3 row), §8, §13 (stage-A input-manifest
  verification); §20 D1/D9, OD-1; owner backlog-creation directive of 2026-08-10.
- **Why it matters:** Semantic assertions ("one coherent discovery topic per turn",
  refusal quality) cannot be regex-graded. The judge must be pinned, independent, and
  injection-defended, and may produce baseline-eligible verdicts only under the
  owner-ratified measured calibration (R2/OD-1).
- **Dependencies (historical, superseded):** WP-2B-1 and WP-2B-2 DONE; R2 disposition with
  OD-1 ratified; owner authorization for WP-2B-3.
- **Trigger to begin:** SUPERSEDED — no separate WP-2B-3 authorization is scheduled. The
  non-live scaffold is delivered under WP-2B-2 (BER-DEC-007); measured calibration and OD-1
  ratification are required before WP-2B-4 and are not authorized by BER-DEC-007.
- **Expected deliverable:** The injection-resistant judge interface (separate system-level
  judge policy; delimited data envelope; no judge tools; least-context input; structured
  schema-validated verdicts; no private chain-of-thought in evidence); the versioned
  human-labeled calibration dataset operationalized in a calibration harness that
  enforces the owner-approved thresholds (including the separate critical false-PASS
  gate); drift detection via re-calibration triggers (any judge model/version, rubric-
  derivation, or dataset change forces re-calibration and behavioral re-baselining, with
  dataset identity pinned in `baseline_identity`); the documented re-calibration process;
  rubric derivation with the unjudgeable-as-written census (assertion classification
  keyed by `assertion_uid`, approval authority Peter Nguyen per D9); and structured judge
  evidence with `JUDGE_ERROR` handling (malformed/refusal/timeout/transport ⇒
  `JUDGE_ERROR`, never PASS/FAIL).
- **Acceptance criteria:** §18 judge-harness and calibration-harness tests pass (mock
  judge; injection-defense probes; threshold enforcement rejecting an under-threshold
  judge); the judge consumes only stage-A input-manifest-verified artifacts; no
  baseline-eligible semantic verdict is produced below the ratified thresholds.
- **Owner decision required:** Phase authorization; assertion-classification sign-off
  (D9 authority); any re-ratification OD-1 requires after judge/dataset change.
- **Explicit non-goals:** No judge choice outside the R2-pinned identity without
  re-calibration; no exposure of expected answers beyond the rubric; no multi-judge
  arbitration (a FUTURE consideration, BER-BKL-011).
- **Related design sections:** §8, §13, §17 criterion 9, §18, §19 (2B-3), §20 D1/D9/OD-1.
- **Completion evidence:** SUPERSEDED BY WP-2B-2. The non-live scaffold's completion evidence
  is WP-2B-2's reviewed and merged PR(s); the measured-calibration gate remains a future
  requirement recorded against WP-2B-4 and BER-BKL-005/011.
- **Supersedes / superseded by:** SUPERSEDED BY WP-2B-2 (v1.1 fast-track successor;
  BER-DEC-007). Historical record retained per governance rule 5.

### WP-2B-4 — Scenario A Limited-Scope Live Suite

- **ID:** WP-2B-4
- **Title:** Scenario A Limited-Scope Live Suite (separate first-live phase)
- **Phase:** 2B-4
- **Priority:** REQUIRED
- **Status:** BLOCKED — separate first-live phase; NOT authorized by BER-DEC-007. Unblocks
  only when every dependency below exists, including a separate reviewed and merged WP-2B-4
  authorization with a live-token budget, a live external evidence root, evidence-handling and
  retention terms, and live stop conditions.
- **Source / evidence:** Merged design §19 (2B-4 row), §9 (state machine; controls A–Q;
  live behavioral manifest), §8 (coherent-topic rubric);
  [`docs/acceptance/scenario-a-runbook.md`](../acceptance/scenario-a-runbook.md)
  (Control I); owner backlog-creation directive of 2026-08-10.
- **Why it matters:** Scenario A is the first canonical multi-turn behavioral suite and
  the runner's own first end-to-end self-proof. It automates the currently-manual
  fresh-session acceptance while complementing — never replacing — the mechanical
  evidence harness.
- **Dependencies:** ALL of: (1) WP-2B-1 and WP-2B-2 DONE (the former WP-2B-3 is superseded by
  WP-2B-2; this is the first live phase: the §19 hard precondition requires containment,
  timeouts, emergency kill, budget reservation, attempt recording, aggregate semantics, and
  bounded concurrency implemented and tested first, and the Scenario A grading stack built
  non-live in WP-2B-2); (2) a truthful R1 activation-identifying mechanism or an explicitly
  owner-approved bounded activation claim scope sufficient for Scenario A's claims; (3) R2
  measured calibration completed and OD-1 ratified through the required measured-calibration
  gate (formerly WP-2B-3; now a future requirement ahead of WP-2B-4, not authorized by
  BER-DEC-007); (4) R4 effective per-tool-path confinement proven for the selected live host,
  including control-plane corpus inaccessibility; (5) R5 execution-profile observability and
  isolation proven for the selected live host, or an explicit owner-approved narrower live
  claim scope that defines exactly what remains unobservable and excludes affected runs from
  baseline claims; and (6) a separate reviewed and merged WP-2B-4 authorization with
  live-token budget, live external evidence root, evidence terms, and stop conditions.
- **Trigger to begin:** Owner authorizes WP-2B-4 with its live-token budget, evidence
  terms, and stop conditions. WP-2B-4 may not be authorized while R1, R2/OD-1, R4, or
  R5 remains unresolved for the selected live execution profile.
- **Future initial claim scope (documented by the v1.1 successor; NOT authorized here):**
  Scenario A only; explicit invocation of `project-orchestrator`; one pinned Project Aegis
  version; one pinned execution profile; one selected host configuration; one approved
  synthetic answer set; Scenario A controls A–Q; NO claim that the model independently
  selected `project-orchestrator`; NO general model-selected routing claim; NO generic corpus
  claim; NO baseline claim; NO stability-window claim; NO promotion claim; NO
  production-readiness claim. Explicit invocation proves only that the named target was
  intentionally invoked; it does not prove independent routing selection. See
  [`docs/design/behavioral-eval-runner-v1-fast-track-successor.md`](../design/behavioral-eval-runner-v1-fast-track-successor.md)
  §7.
- **Expected deliverable:** A versioned live Scenario A behavioral manifest (run-local
  hashes only; never fixture-pin comparison on live output); the adaptive conversation
  state machine; the turn/topic classifier; the canonical synthetic answer bank (trusted
  control-plane material, never agent-visible); controls A–Q graded per the design's
  anchoring corpus cases; support for valid alternative topic orderings; detection of
  questionnaire dumps, unrelated-topic bundling, repeated looping without progress, and
  unauthorized stage transitions; and the per-run evidence report with every transition
  recorded (`prior_state`, `observed_turn_class`, `selected_answer_id`, `next_state`).
- **Acceptance criteria:** Design §23 item 11 holds: the suite passes its own self-proof
  via the adaptive driver, covering controls A–Q against the live behavioral manifest,
  with the coherent-topic rule graded semantically. The mechanical PS1 harness remains
  unmodified. The accepted Scenario A rule is preserved exactly:

  > **ONE COHERENT DISCOVERY TOPIC PER TURN.**
  > **Related supporting details within that topic are allowed.**

- **Owner decision required:** Phase authorization with live budget; acceptance of the
  suite's first self-proof evidence.
- **Explicit non-goals:** No modification of Scenario A behavior, the runbook, existing
  eval assertions, or the mechanical harness; no keyword/question-mark/conjunction
  counting as a topic-atomicity oracle; no generic corpus execution.
- **Related design sections:** §5, §8, §9, §18 (conversation-driver tests), §19 (2B-4),
  §23 item 11.
- **Completion evidence:** Reviewed and merged WP-2B-4 PR(s); the first self-proof run's
  evidence bundle at its authorized evidence path; status updated here through a
  reviewed PR.
- **Supersedes / superseded by:** None.

### WP-2B-5 — Generic corpus execution

- **ID:** WP-2B-5
- **Title:** Generic `evals.json` + `trigger-evals.json` execution
- **Phase:** 2B-5
- **Priority:** REQUIRED
- **Status:** BACKLOG
- **Source / evidence:** Merged design §19 (2B-5 row), §5 (case semantics), §5b
  (preflight), §5c (MANUAL-ONLY), §5d (typed targets), §5a (binding full-surface rule);
  owner backlog-creation directive of 2026-08-10.
- **Why it matters:** This phase makes the 1,740 authored single-prompt cases executable
  as designed — honestly: runnable units are the per-run preflight output, never an
  assumed 1,740, and every exclusion carries a reason code and an author-facing finding.
- **Receives generic breadth deferred by the WP-2B-2 fast track (BER-DEC-007):** generic
  deterministic grader mappings for the complete authored corpus; generic semantic rubric
  mappings; generic corpus judge configuration; generic activation-observer breadth; generic
  fixture-library breadth; integration with all 1,740 authored single-prompt cases (runnable
  units remain the per-run preflight output, never an assumed 1,740); corpus-wide execution;
  corpus-wide calibration; generic-corpus evidence runs; and CI integration. None of these is
  authorized here; WP-2B-5 remains BACKLOG and separately owner-authorized.
- **Dependencies:** WP-2B-4 DONE; the 2B-0 gate resolved to outcome A or an
  owner-approved limitation (broad general-corpus execution precondition, §19); owner
  authorization for WP-2B-5.
- **Trigger to begin:** Owner authorizes WP-2B-5 within the decided tier ceilings.
- **Expected deliverable:** Execution of `evals.json` behavior cases and
  `trigger-evals.json` discrimination cases under §5 semantics; MANUAL-ONLY handling per
  §5c (incompatible positives not dispatched — `UNRUN` + `PRECHECK_EXCLUDED` /
  `INCOMPATIBLE_INVOCATION_MODE` with a corpus warning; negatives still run); typed
  subagent handling per §5d; the fixture library for fixture-dependent cases (no silent
  fixture manufacture that changes what an authored prompt means); the runnability
  census kept current against BER-BKL-008; author-facing findings for outliers,
  degenerate cases, and preflight exclusions; and full-library selection-surface
  enforcement (every full-library routing execution materializes the complete shipped
  corpus; `partial_install` separately scoped and never baseline evidence).
- **Acceptance criteria:** Design §23 items 3–6 and 13 hold for the executed scope; every
  corpus case type discovered by the census has a working execution path or an honest
  preflight exclusion; no MANUAL-ONLY contract is violated; reports publish complete
  coverage metrics with `UNRUN`/excluded totals by reason.
- **Owner decision required:** Phase authorization; tier selection scope for early runs;
  full-corpus runs remain separately owner-authorized events (D3).
- **Explicit non-goals:** No claim that all potential units are runnable; no retyping or
  rewriting of authored cases (findings only, D8); no promotion of the CI lane.
- **Related design sections:** §3, §5, §5a–§5d, §10, §11, §12, §13, §19 (2B-5), §23.
- **Completion evidence:** Reviewed and merged WP-2B-5 PR(s); first generic-run evidence
  bundles at their authorized paths; status updated here through a reviewed PR.
- **Supersedes / superseded by:** None.

### WP-2B-6 — Scheduling, cost, quarantine, and cadence operations

- **ID:** WP-2B-6
- **Title:** Scheduling, cost, quarantine, and cadence operations (beyond the 2B-1
  minimums)
- **Phase:** 2B-6
- **Priority:** REQUIRED
- **Status:** BACKLOG
- **Source / evidence:** Merged design §19 (2B-6 row: advanced cadence + analytics + cost
  refinement), §10–§12, §13; owner backlog-creation directive of 2026-08-10.
- **Why it matters:** The minimum guardrails (reservation, scheduler, N/quorum
  controller) land in 2B-1 by design; sustained operation needs the mature layer —
  rotation that provably covers the corpus, quarantine governance with waiver
  operations, budget accounting over time, and stable identity-matched windows.
- **Dependencies:** WP-2B-5 DONE; owner authorization for WP-2B-6.
- **Trigger to begin:** Owner authorizes WP-2B-6.
- **Expected deliverable:** Operational maturity over the 2B-1 minimums, never relaxing
  them: deterministic scheduling refinements under the versioned §11a policy; the
  reverse negative-neighbor index maintained and versioned for PR-tier selection (§12);
  risk-class-aware operations over the owner-ratified `CRITICAL`/`HIGH`/`STANDARD`
  classes (OD-3); critical-quarantine waiver operations (complete, expiring,
  human-issued waivers only); a budget ledger view over reserved/actual/released spend
  (monetary or `UNKNOWN` + proxy units) across runs; weekly rotating stratified ~10%
  cadence with rotation-coverage reporting (D4); coverage accounting across runs against
  §13 metrics; identity-matched stability windows (segment/reset on any
  `baseline_identity` change); and the release-candidate execution profile (explicitly
  configured N=5 for RC/disputed/high-risk cases, per D2).
- **Acceptance criteria:** §18 scheduler and aggregator tests keep passing; two runs with
  the same policy version, selection, and seed produce the same queue; quarantine never
  erases `latest_aggregate_verdict`; no unwaived ACTIVE CRITICAL quarantine can be
  silently excluded from promotion accounting; cadence rotation demonstrably reaches the
  whole shipped corpus over its window.
- **Owner decision required:** Phase authorization; OD-3 ratification if still pending;
  any waiver issuance (each waiver is a recorded owner artifact).
- **Explicit non-goals:** No relaxation of 2B-1 guardrails; no automatic waivers; no
  automatic reprioritization; no promotion of the CI lane.
- **Related design sections:** §10, §11, §11a, §12, §13, §17 (window/threshold inputs),
  §19 (2B-6), §20 D2/D3/D4/OD-3.
- **Completion evidence:** Reviewed and merged WP-2B-6 PR(s); recorded operational
  evidence (rotation coverage, ledger, window reports); status updated here through a
  reviewed PR.
- **Supersedes / superseded by:** None.

### WP-2B-7 — Advisory CI and operator workflow

- **ID:** WP-2B-7
- **Title:** Advisory CI integration and operator workflow
- **Phase:** 2B-7
- **Priority:** REQUIRED
- **Status:** BACKLOG
- **Source / evidence:** Merged design §19 (2B-7 row), §16 (CI posture; protected-surface
  governance), §17 (promotion-to-gate criteria — DECIDED and binding; promotion itself
  remains a separate later owner decision); the live merge gate
  [`.github/workflows/validate-skills.yml`](../../.github/workflows/validate-skills.yml)
  (gate-guard protected-surface path); owner backlog-creation directive of 2026-08-10.
- **Why it matters:** The behavioral lane must attach to CI as advisory/non-blocking
  without ever mutating enforcement surfaces at runtime, and the wiring change itself
  must go through gate-guard's protected-surface manual-review path — human review and
  human merge, exactly as that gate intends.
- **Dependencies:** WP-2B-6 DONE; owner authorization for WP-2B-7.
- **Trigger to begin:** Owner authorizes WP-2B-7.
- **Expected deliverable:** A reviewed GitHub Actions workflow implementing the advisory
  lane; gate-guard protected-surface handling (the 2B-7 PR is expected to trigger the
  manual-review path and is merged only by a human); explicit workflow permissions
  (least privilege); evidence retention wiring for CI-produced run artifacts per the
  BER-BKL-009 policy; concurrency and cancellation semantics; the scheduled cadence
  trigger; manual full-corpus dispatch that still requires the owner's per-run
  authorization and run-level cap (D3); advisory PR reporting (informs, never gates);
  the operator runbook; and rollback and escalation procedures.
- **Acceptance criteria:** The lane is non-blocking; `validate-skills` and `gate-guard`
  remain required and independent; the runner runtime provably never edits workflows,
  CODEOWNERS, the validator, or gate scripts; the §17 promotion criteria are DECIDED,
  binding prerequisites that the 2B-7 implementation team may not reopen; OD-2's numeric
  minimum coverage threshold and the final durable human promotion approval remain
  pending; meeting the criteria does not itself authorize promotion — WP-2B-7 implements
  advisory CI only, and a separate later owner decision is still required to promote the
  lane; nothing in this phase activates blocking CI.
- **Owner decision required:** Phase authorization; review/merge of the protected-surface
  workflow PR; and the separate later promotion decision — pending OD-2 ratification and
  the durable human promotion approval under the DECIDED §17 criteria, which meeting the
  criteria never self-authorizes.
- **Explicit non-goals:** No blocking CI; no auto-merge; no weakening or replacement of
  the structural validator; no automatic full-corpus scheduling.
- **Related design sections:** §16, §17, §19 (2B-7), §20 D5.
- **Completion evidence:** The reviewed, human-merged workflow PR; the operator runbook in
  the repository; status updated here through a reviewed PR.
- **Supersedes / superseded by:** None.

---

## 8. Canonical BER backlog inventory — BER-BKL-001 … BER-BKL-015

Inventory records preserve their IDs durably. Where an item overlaps an R gate or a work
package, the record cross-references the authoritative record instead of duplicating (and
risking forking) its requirements.

### BER-BKL-001 — Split assertion-accounting coverage from assertions-actually-graded coverage

- **ID:** BER-BKL-001
- **Title:** Split assertion-accounting coverage from assertions-actually-graded coverage
- **Phase:** 2B-1
- **Priority:** IMPORTANT
- **Status:** BACKLOG
- **Source / evidence:** Merged design §13 defines `assertion_coverage` as a composite
  (selected assertions graded OR explicitly unjudgeable-with-finding OR excluded by an
  approved reason); §17 condition 7 consumes it. Refinement recorded as a deferred
  finding from the PR #78 review cycle, carried into this register by the owner's
  backlog-creation directive of 2026-08-10.
- **Why it matters:** A single composite number can look identical for a run that graded
  95% of assertions and a run that graded 60% while classifying 35% unjudgeable. Separate
  metrics (accounted-for vs actually graded) keep the honesty property the coverage
  metrics exist for.
- **Dependencies:** WP-2B-1 schema work (BER-BKL-007).
- **Trigger to begin:** WP-2B-1 AUTHORIZED and its report-schema implementation underway.
- **Expected deliverable:** Two explicitly named metrics in the run report schema — an
  assertion-accounting coverage (every selected assertion has a recorded disposition) and
  an assertions-actually-graded coverage (graded assertions only, excluding unjudgeable
  and approved-excluded) — with the §17 promotion input mapping stated.
- **Acceptance criteria:** Both metrics appear in every run report; report-schema tests
  cover them; the composite behavior required by the merged design remains derivable, and
  nothing weakens §17 condition 7.
- **Owner decision required:** None beyond WP-2B-1 authorization and normal PR review
  (OD-2 later consumes the resulting denominators).
- **Explicit non-goals:** No change to the merged design document in this backlog task; no
  weakening of any §17 coverage condition.
- **Related design sections:** §8, §13 (coverage metrics), §17 (conditions 7–8).
- **Completion evidence:** Merged WP-2B-1 schema PR implementing both metrics; status
  updated here through a reviewed PR.
- **Supersedes / superseded by:** None.

### BER-BKL-002 — Normalize remaining prose/schema naming

- **ID:** BER-BKL-002
- **Title:** Normalize remaining prose/schema naming (exemplar: `JUDGE-ERROR` versus
  `JUDGE_ERROR`)
- **Phase:** 2B-1
- **Priority:** IMPORTANT
- **Status:** BACKLOG
- **Source / evidence:** Deferred normalization finding from the PR #78 review cycle,
  carried into this register by the owner's backlog-creation directive of 2026-08-10.
  Verification note (2026-08-10): the merged design at blob `94ba583…` uses the
  underscore form `JUDGE_ERROR` consistently — a text search finds zero hyphenated
  instances — so this item governs naming discipline in the runner-facing schemas, code,
  and prose written from 2B-1 onward, plus any residual variance actually found at
  implementation time.
- **Why it matters:** Schema identifiers become machine keys (§13 versioned schemas).
  Prose/identifier drift (`JUDGE-ERROR` vs `JUDGE_ERROR` and any similar pair) produces
  parsers and reports that disagree about the same concept.
- **Dependencies:** WP-2B-1 schema work (BER-BKL-007).
- **Trigger to begin:** WP-2B-1 AUTHORIZED.
- **Expected deliverable:** A naming-normalization sweep over the runner's schemas, code,
  and docs as they are authored: one canonical spelling per identifier (the design's
  underscore enum forms), a recorded mapping for any variance found, and a lint/test
  guard where practical.
- **Acceptance criteria:** Runner schemas and reports use exactly one spelling per
  identifier; any discovered variance is either normalized in the new artifacts or
  recorded as a finding; **the merged design document is not edited by this item** — if a
  genuine design-text defect is ever found, it routes to a reviewed design successor, not
  a silent edit.
- **Owner decision required:** None beyond WP-2B-1 authorization and normal PR review.
- **Explicit non-goals:** No modification of the merged design in this task or under this
  item; no semantic changes disguised as renames.
- **Related design sections:** §10, §13 (versioned enums and schemas).
- **Completion evidence:** Merged WP-2B-1 PR(s) showing the canonical identifiers and any
  guard; status updated here through a reviewed PR.
- **Supersedes / superseded by:** None.

### BER-BKL-003 — Activation-observability evidence and claim-scope implementation

- **ID:** BER-BKL-003
- **Title:** Activation-observability evidence and claim-scope implementation
- **Phase:** 2B-0 / 2B-2
- **Priority:** GATE
- **Status:** BLOCKED — R1's WP-2B-0 disposition is accepted as unavailable/unknown.
  Activation-observer implementation cannot proceed until the later phase has a truthful
  mechanism or separately accepted limitation. WP-2B-2 remains unauthorized.
- **Source / evidence:** Cross-reference: **R1** (authoritative record, §6 of this file).
  Merged design §6, §17a, §20 R1.
- **Why it matters:** Inventory visibility for the R1 gate; see R1.
- **Dependencies:** The gate half is DONE — R1's disposition (unavailable/unknown) is
  recorded and owner-accepted under Outcome B via
  [PR #81](https://github.com/ModernNomad-98/Project-Aegis/pull/81). The implementation
  half requires WP-2B-2 AUTHORIZED plus a truthful activation mechanism or a separately
  accepted limitation.
- **Trigger to begin:** Gate half CLOSED — no further WP-2B-0 work is authorized by
  BER-DEC-005. The implementation half awaits WP-2B-2 authorization; it remains BLOCKED
  until a truthful mechanism or separately accepted limitation exists.
- **Expected deliverable:** R1's activation observability report — evidence/report work
  occurring only inside AUTHORIZED WP-2B-0 scope — then the 2B-2 activation observer —
  implemented only inside AUTHORIZED WP-2B-2 scope — built only on the proven mechanism
  within the recorded claim scope.
- **Acceptance criteria:** As R1 (disposition recorded and accepted); the future
  implementation additionally satisfies design §23 item 6 and never treats R1 as
  technically solved.
- **Owner decision required:** As R1.
- **Explicit non-goals:** As R1; this record adds no requirement beyond R1 and WP-2B-2.
- **Related design sections:** §6, §17a, §19, §20 R1, §23 item 6.
- **Completion evidence:** Gate half: as R1 —
  [PR #81](https://github.com/ModernNomad-98/Project-Aegis/pull/81) (merge commit
  `55b0c4b4f5c0cba9bbf70f63cd0ebf8212f8eae5`) and this reviewed status update.
  Implementation half: the future merged WP-2B-2 activation-observer implementation PR
  (still required).
- **Supersedes / superseded by:** None (tracks R1; R1's record is authoritative for the
  gate's requirements).

### BER-BKL-004 — Configuration isolation and effective per-tool confinement

- **ID:** BER-BKL-004
- **Title:** Configuration isolation and effective per-tool-path confinement
- **Phase:** 2B-0 / 2B-1
- **Priority:** GATE
- **Status:** BACKLOG — WP-2B-0 recorded R4/R5 as incomplete/blocked. The non-live
  containment and execution-profile scaffolding may be built inside authorized WP-2B-1,
  but no effective-containment or baseline-eligibility claim is allowed until later
  evidence proves it.
- **Source / evidence:** Cross-reference: **R4 and R5** (authoritative records, §6 of this
  file). Merged design §5e, §15, §17a items 6–8.
- **Why it matters:** Inventory visibility for the containment and configuration gates;
  see R4 and R5.
- **Dependencies:** The gate half is DONE — R4/R5 dispositions (incomplete/blocked) are
  recorded and owner-accepted under Outcome B via
  [PR #81](https://github.com/ModernNomad-98/Project-Aegis/pull/81). The non-live
  scaffolding half requires WP-2B-1's BER-DEC-006 authorization to be effective (the
  governance PR containing BER-DEC-006 merged); effective-containment evidence remains
  a later-phase requirement.
- **Trigger to begin:** Gate half CLOSED — no further WP-2B-0 work is authorized by
  BER-DEC-005. The non-live scaffolding half begins only after the governance PR
  containing BER-DEC-006 is merged, on `feat/behavioral-eval-runner-2b-1`.
- **Expected deliverable:** R4's containment capability report and R5's execution-profile
  isolation report — evidence work that occurred only inside AUTHORIZED WP-2B-0 scope
  and is now recorded incomplete/blocked — then the 2B-1 fail-closed, non-live
  containment and execution-profile scaffolding: interfaces, contracts, adapters,
  guards, and profile capture, with deterministic mock/synthetic implementations used
  only by offline tests, implemented only inside AUTHORIZED WP-2B-1 scope, and with the
  real-host implementation state reported unavailable/unknown until later evidence
  supplies the proven mechanisms.
- **Acceptance criteria:** As R4 and R5 (dispositions recorded and accepted); the
  WP-2B-1 scaffolding is fail-closed and non-live — deterministic mock/synthetic tests
  only, with real-host containment and profile-isolation capability reported
  unavailable/unknown and live paths denied — satisfies the non-live, deterministically
  tested subset of design §23 items 12 and 15, and makes no effective-containment or
  baseline-eligibility claim until later evidence proves it.
- **Owner decision required:** As R4/R5 (including any narrower-claim approval).
- **Explicit non-goals:** As R4/R5; this record adds no requirement beyond them and
  WP-2B-1.
- **Related design sections:** §5a, §5e, §13, §15, §17a, §18, §20 R4/R5, §23 items 12/15.
- **Completion evidence:** Gate half: as R4/R5 —
  [PR #81](https://github.com/ModernNomad-98/Project-Aegis/pull/81) (merge commit
  `55b0c4b4f5c0cba9bbf70f63cd0ebf8212f8eae5`) and this reviewed status update.
  Scaffolding half: the future merged WP-2B-1 containment/profile scaffolding PRs
  (non-live; still required).
- **Supersedes / superseded by:** None (tracks R4/R5; their records are authoritative).

### BER-BKL-005 — Judge selection, measurable calibration, and owner thresholds

- **ID:** BER-BKL-005
- **Title:** Judge selection, measurable calibration, and owner thresholds
- **Phase:** 2B-0 / 2B-2 (non-live scaffold) / pre-2B-4 (measured calibration)
- **Priority:** GATE
- **Status:** BLOCKED — R2 remains incomplete/blocked and OD-1 remains open. The former
  WP-2B-3 is SUPERSEDED BY WP-2B-2: the NON-LIVE judge/calibration scaffold and
  threshold-enforcement logic move into WP-2B-2 (BER-DEC-007; mock/recorded only), while the
  MEASURED calibration and OD-1 ratification remain unauthorized and required ahead of
  WP-2B-4.
- **Source / evidence:** Cross-reference: **R2** (authoritative record, §6 of this file)
  and OD-1 (§9 of this file). Merged design §8, §17a item 9, §20 D1/OD-1/R2; v1.1 fast-track
  successor §4–§5.
- **Why it matters:** Inventory visibility for the judge gate; see R2. WP-2B-2 delivers the
  non-live calibration harness and threshold-enforcement logic (mock/recorded only); the
  ratified thresholds are then applied once the measured calibration is completed and OD-1 is
  ratified ahead of WP-2B-4.
- **Dependencies:** The WP-2B-0 evidence half is DONE — R2's disposition
  (incomplete/blocked) is recorded and owner-accepted under Outcome B via
  [PR #81](https://github.com/ModernNomad-98/Project-Aegis/pull/81); no judge was pinned
  and no calibration exists. The non-live scaffold half is delivered by WP-2B-2
  (BER-DEC-007). The measured-calibration half requires a new reviewed and merged
  authorization ahead of WP-2B-4 (the former separate WP-2B-3 authorization is superseded).
- **Trigger to begin:** Spike half CLOSED — no further WP-2B-0 work is authorized by
  BER-DEC-005. The non-live scaffold is delivered under WP-2B-2 (BER-DEC-007). Otherwise
  BLOCKED: measured judge selection and calibration require a new reviewed and merged
  authorization ahead of WP-2B-4, and OD-1 remains open.
- **Expected deliverable:** the WP-2B-2 non-live calibration-harness scaffold and
  threshold-enforcement logic (mock/recorded); then, ahead of WP-2B-4, R2's pinned judge
  identity + measured calibration report enforcing the OD-1-ratified thresholds.
- **Acceptance criteria:** As R2, WP-2B-2 (non-live scaffold), and the future
  measured-calibration gate; design §23 items 7 and 19 hold.
- **Owner decision required:** WP-2B-2 phase authorization (BER-DEC-007) for the non-live
  scaffold; OD-1 (measured calibration, ahead of WP-2B-4).
- **Explicit non-goals:** No invented thresholds; no baseline-eligible semantic verdict
  before ratification; no measured calibration under WP-2B-2 (non-live only).
- **Related design sections:** §8, §13, §17 criterion 9, §17a item 9, §20 D1/OD-1/R2,
  §23 items 7/19.
- **Completion evidence:** Evidence half: as R2 —
  [PR #81](https://github.com/ModernNomad-98/Project-Aegis/pull/81) (merge commit
  `55b0c4b4f5c0cba9bbf70f63cd0ebf8212f8eae5`) and this reviewed status update. The non-live
  scaffold's evidence is WP-2B-2's merged PR(s); the measured calibration result and OD-1
  ratification (formerly WP-2B-3) remain future requirements ahead of WP-2B-4.
- **Supersedes / superseded by:** None (tracks R2 + WP-2B-2 non-live scaffold + the future
  measured-calibration gate; those records are authoritative).

### BER-BKL-006 — Cost observability and enforceable reservation units

- **ID:** BER-BKL-006
- **Title:** Cost observability and enforceable reservation units
- **Phase:** 2B-0 / 2B-1
- **Priority:** GATE
- **Status:** BACKLOG — R3's limitation is accepted. Authorized WP-2B-1 may build and
  deterministically test runner-owned reservation and budget enforcement, but no live
  host/provider enforcement claim is allowed.
- **Source / evidence:** Cross-reference: **R3** (authoritative record, §6 of this file).
  Merged design §11, §11a, §20 D3/R3.
- **Why it matters:** Inventory visibility for the cost gate; see R3. WP-2B-1 then
  implements pre-dispatch reservation in the proven units.
- **Dependencies:** The gate half is DONE — R3's disposition (unavailable/unknown) is
  recorded and owner-accepted under Outcome B via
  [PR #81](https://github.com/ModernNomad-98/Project-Aegis/pull/81). The runner-owned,
  non-live implementation half requires WP-2B-1's BER-DEC-006 authorization to be
  effective (the governance PR containing BER-DEC-006 merged).
- **Trigger to begin:** Spike half CLOSED — no further WP-2B-0 work is authorized by
  BER-DEC-005. The runner-owned reservation half begins only after the governance PR
  containing BER-DEC-006 is merged, on `feat/behavioral-eval-runner-2b-1`.
- **Expected deliverable:** R3's cost-observability report (disposition recorded
  unavailable/unknown); then WP-2B-1's runner-owned reservation, bounded concurrency,
  reconciliation, and kill-switch state machines exercised with configured
  synthetic/mock call, turn, token, session, and monetary units in deterministic
  offline tests, while the real Claude Code/provider adapter reports reservation
  capability unavailable/unknown and denies live dispatch until later R3 evidence
  identifies enforceable units.
- **Acceptance criteria:** As R3 (disposition recorded and accepted) and WP-2B-1; the
  non-live, deterministically tested subset of design §23 item 10 holds over
  synthetic/mock units; the real adapter reports reservation capability
  unavailable/unknown and denies live dispatch; no fabricated dollar accounting
  anywhere; and no live host/provider enforcement claim is made until later evidence
  proves it.
- **Owner decision required:** As R3; WP-2B-1 authorization.
- **Explicit non-goals:** As R3; no spend outside approved budgets.
- **Related design sections:** §11, §11a, §13, §17a, §20 D3/R3, §23 item 10.
- **Completion evidence:** Gate half: as R3 —
  [PR #81](https://github.com/ModernNomad-98/Project-Aegis/pull/81) (merge commit
  `55b0c4b4f5c0cba9bbf70f63cd0ebf8212f8eae5`) and this reviewed status update.
  Implementation half: the future merged WP-2B-1 budget-guard PR (non-live; still
  required).
- **Supersedes / superseded by:** None (tracks R3; R3's record is authoritative).

### BER-BKL-007 — Final production JSON/YAML schemas and schema-migration policy

- **ID:** BER-BKL-007
- **Title:** Final production JSON/YAML schemas and schema-migration policy
- **Phase:** 2B-1
- **Priority:** REQUIRED
- **Status:** BACKLOG
- **Source / evidence:** Merged design §13 (every report carries `schema_version` /
  `runner_version`; versioned blocker/reason enums; canonical identities) and §5b ("the
  exact field names may be refined at build time into a better coherent schema, but every
  concept above must remain addressed"); owner backlog-creation directive of 2026-08-10.
- **Why it matters:** The design deliberately specifies concepts, not final serialized
  shapes. Production schemas need exact field names, types, enum registries, and a
  migration policy so later schema versions never silently reinterpret stored evidence.
- **Dependencies:** WP-2B-1 AUTHORIZED.
- **Trigger to begin:** WP-2B-1 schema implementation begins.
- **Expected deliverable:** Versioned JSON/YAML schemas for attempt records, case
  aggregates, run reports (three field groups), case/fixture manifests, materialization
  and execution profiles, and evidence manifests; a schema-migration policy (how
  `schema_version` increments, what compatibility is promised, how old evidence is read);
  and validation tooling in the runner's tests.
- **Acceptance criteria:** Every §5b concept and every §13 field group remains addressed;
  dropping a concept is treated as reopening the "all-cases-runnable" fiction and is
  refused; enum sets are closed and versioned; report-schema tests enforce the shapes.
- **Owner decision required:** Acceptance of the final shapes at WP-2B-1 review (none
  earlier).
- **Explicit non-goals:** No change to the merged design's concepts; no free-text reason
  codes; no unversioned enums.
- **Related design sections:** §5b, §10, §13, §18 (report-schema tests).
- **Completion evidence:** Merged WP-2B-1 schema PR(s) with tests; status updated here
  through a reviewed PR.
- **Supersedes / superseded by:** None.

### BER-BKL-008 — Machine-generated corpus census

- **ID:** BER-BKL-008
- **Title:** Machine-generated, kept-current corpus census
- **Phase:** 2B-1
- **Priority:** REQUIRED
- **Status:** BACKLOG
- **Source / evidence:** Merged design §3 (implementation-time corpus census, items a–k;
  the design-time census is evidence, not a completeness proof); owner backlog-creation
  directive of 2026-08-10.
- **Why it matters:** Runnability, MANUAL-ONLY handling, risk classes, and OD-2's honest
  denominator all depend on a machine-produced census that stays current with the
  corpus — never on the design-time snapshot or hard-coded assumptions.
- **Dependencies:** WP-2B-1 AUTHORIZED.
- **Trigger to begin:** WP-2B-1 begins.
- **Expected deliverable:** A machine-generated census covering: runtime-file
  classification (`runtime_required` / `control_plane_only` /
  `ambiguous_needs_owner_review`, ambiguous failing closed); runnability (cases runnable
  in an empty consumer workspace); MANUAL-ONLY-sentinel skills (parsed from frontmatter)
  and their positive cases; subagent-target cases; fixture-dependent cases;
  service/network-dependent cases; credential-dependent cases; source-role cases; cases
  with unjudgeable-as-written assertions; and proposed per-case risk classes
  (`CRITICAL`/`HIGH`/`STANDARD`) for owner ratification — plus the honest runnable
  denominator feeding OD-2.
- **Acceptance criteria:** The census is reproducible from the pinned corpus SHA; sentinel
  detection is parsed, never a hard-coded name list; ambiguous classifications are never
  exposed to the agent-visible surface until a human reclassifies; census output feeds
  the §5b manifests and the OD-2/OD-3 decision packages.
- **Owner decision required:** OD-3 ratification of proposed risk classes; human
  reclassification of any `ambiguous_needs_owner_review` file.
- **Explicit non-goals:** No hand-maintained counts; no assumption that the design-time
  variances are the only variances.
- **Related design sections:** §3 (items a–k), §5a, §5b, §5c, §8, §10, §17 (OD-2 input).
- **Completion evidence:** Merged WP-2B-1 census PR with generated output and tests;
  status updated here through a reviewed PR.
- **Supersedes / superseded by:** None.

### BER-BKL-009 — Evidence retention, access, encryption, redaction, and deletion policy

- **ID:** BER-BKL-009
- **Title:** Evidence retention, access, encryption, redaction, and deletion policy
- **Phase:** 2B-1
- **Priority:** REQUIRED
- **Status:** BACKLOG
- **Source / evidence:** Merged design §13 ("Access, retention, redaction": least-
  privilege readers; access-controlled evidence root; encryption-at-rest where
  sensitivity requires; per-artifact retention class with a defined retention period and
  deletion/expiration procedure; redaction before judge exposure or external sharing);
  §20 D6; owner backlog-creation directive of 2026-08-10.
- **Why it matters:** External never means ungoverned. The design requires the classes
  and procedures to exist but deliberately does not fix the exact periods, access
  groups, or encryption mechanism — those are owner decisions that must be recorded
  before evidence accumulates at scale. Phase split: WP-2B-0 runs under the minimum
  temporary spike-evidence-handling terms fixed in its authorization (§2 of this file) —
  mandatory before any probe or model call; this item delivers the final
  production-grade policy in 2B-1, and the spike terms never substitute for it.
- **Dependencies:** WP-2B-1 AUTHORIZED (the evidence writer implements the classes).
- **Trigger to begin:** WP-2B-1 evidence-writer implementation begins.
- **Expected deliverable:** A written evidence-governance policy fixing: retention
  periods per retention class; access groups and the least-privilege read matrix;
  the encryption-at-rest mechanism and its key custody; redaction/sanitization rules
  (including what the judge may ever see); and the deletion/expiration procedure —
  wired into the evidence writer and the operator runbook.
- **Acceptance criteria:** Every artifact class in the §13 bundle contract maps to a
  retention class with a concrete period and procedure; preserve-on-failure behavior is
  retained; raw transcripts remain external and never auto-committed (D6); the policy is
  reviewable in the repository; and the final policy explicitly reviews the WP-2B-0
  spike-evidence-handling terms and absorbs or retires them.
- **Owner decision required:** The exact retention periods, access groups, and encryption
  mechanism (owner-decision register §9, unnumbered item; deliberately not invented in
  the design or here).
- **Explicit non-goals:** No cryptographic signing or immutable external store (that is
  BER-BKL-010 / OD-4); no committing of raw transcripts.
- **Related design sections:** §13 (evidence-bundle contract; access/retention/
  redaction), §15 (preserve-on-failure), §20 D6.
- **Completion evidence:** Merged policy + evidence-writer PR(s); the owner's recorded
  parameter decisions; status updated here through a reviewed PR.
- **Supersedes / superseded by:** None.

### BER-BKL-010 — Evidence signing or immutable external storage beyond SHA-256

- **ID:** BER-BKL-010
- **Title:** Evidence signing or immutable external storage beyond SHA-256 tamper
  evidence
- **Phase:** FUTURE SECURITY
- **Priority:** FUTURE
- **Status:** BACKLOG
- **Source / evidence:** Merged design §13 "Honest limits" and §20 OD-4: SHA-256 provides
  tamper evidence after finalization, not authenticity against a malicious or
  compromised control plane; stronger authenticity is a later owner/security decision
  recorded as out of v1 scope. Owner backlog-creation directive of 2026-08-10.
- **Why it matters:** Without a separately protected signing key or an external
  immutable/append-only store, the process that writes the hashes could rewrite them.
  v1 says this plainly instead of overclaiming; the upgrade path must stay visible.
- **Dependencies:** OD-4 (owner/security decision); BER-BKL-009 policy in place.
- **Trigger to begin:** The owner adopts OD-4's stronger-authenticity direction.
- **Expected deliverable:** If adopted: a signing design (key custody separate from the
  control plane) and/or an external immutable storage design, integrated with the
  two-stage bundle contract without introducing self-referential hashing.
- **Acceptance criteria:** The chosen mechanism demonstrably protects against
  control-plane rewrite within its stated threat model; the detached-marker protocol's
  non-circularity properties are preserved; claims stay within what the mechanism
  proves.
- **Owner decision required:** OD-4 itself.
- **Explicit non-goals:** Not required for v1; never blocks Phase 2B-0 or any v1 phase;
  no authenticity overclaim while unadopted.
- **Related design sections:** §13 (honest limits), §20 OD-4.
- **Completion evidence:** A merged design/implementation PR for the adopted mechanism;
  status updated here through a reviewed PR.
- **Supersedes / superseded by:** None.

### BER-BKL-011 — Judge dataset operations, agreement measurement, drift monitoring, multi-judge arbitration

- **ID:** BER-BKL-011
- **Title:** Judge dataset operations, agreement measurement, drift monitoring, and
  possible multi-judge arbitration
- **Phase:** 2B-2 (non-live trigger representation) / FUTURE (measured operation)
- **Priority:** IMPORTANT
- **Status:** BACKLOG
- **Source / evidence:** Merged design §8 (calibration dataset versioning; re-calibration
  on any judge/rubric/dataset change; human label owner) and §13 (calibration-dataset
  identity pinned in `baseline_identity`); multi-judge arbitration appears in no design
  section and is therefore strictly a future consideration. Owner backlog-creation
  directive of 2026-08-10; v1.1 fast-track successor §4.
- **Why it matters:** A calibrated judge decays: datasets grow, models change, agreement
  drifts. Ongoing dataset operations and measured agreement keep OD-1's ratified
  thresholds meaningful over time.
- **Dependencies:** WP-2B-2 DONE for the non-live drift/recalibration-trigger representation
  and dataset-structure half (the former WP-2B-3 is superseded by WP-2B-2); the measured
  dataset-operations half requires the future measured-calibration authorization ahead of
  WP-2B-4; a reviewed design successor for any multi-judge arbitration (it would extend §8).
- **Trigger to begin:** WP-2B-2 delivers the non-live drift/recalibration trigger
  representation and calibration-dataset structure; measured dataset operations begin after
  the future measured-calibration authorization; an owner-approved design successor
  (arbitration half).
- **Expected deliverable:** Dataset-operations procedures (labeling, versioning, growth,
  re-baselining triggers); periodic agreement measurement against the ratified
  thresholds; drift monitoring with recorded re-calibration events; and — only if the
  owner later adopts it through a design successor — a multi-judge arbitration design.
- **Acceptance criteria:** Every dataset change produces a new
  `calibration_dataset_version/hash` and a re-calibration record; drift beyond thresholds
  removes baseline eligibility until re-ratification; no arbitration mechanism ships
  without a reviewed design successor.
- **Owner decision required:** Re-ratification after any re-calibration (OD-1 authority);
  a separate owner decision for multi-judge arbitration.
- **Explicit non-goals:** No silent dataset edits; no arbitration in v1; no threshold
  changes without owner ratification.
- **Related design sections:** §8, §13, §17 criterion 9, §20 D1/OD-1.
- **Completion evidence:** Merged operational procedures + monitoring PR(s); recorded
  re-calibration events; status updated here through a reviewed PR.
- **Supersedes / superseded by:** None.

### BER-BKL-012 — Exact scheduler weights, fairness policy, and advanced cost estimation

- **ID:** BER-BKL-012
- **Title:** Exact scheduler weights, fairness policy, and advanced cost estimation
- **Phase:** 2B-6
- **Priority:** IMPORTANT
- **Status:** BACKLOG
- **Source / evidence:** Merged design §11a (versioned deterministic risk-aware priority
  policy; within-priority canonical or seeded ordering) and §11 (reservation estimates);
  the exact numeric weights and estimation models are deliberately implementation-time
  detail. Owner backlog-creation directive of 2026-08-10.
- **Why it matters:** The v1 priority order is fixed by §11a, but sustained operation
  needs tuned within-class behavior (fairness across skills/families over time) and
  reservation estimates accurate enough that caps neither starve work nor overshoot.
- **Dependencies:** WP-2B-6 AUTHORIZED; operational data from WP-2B-5 runs.
- **Trigger to begin:** WP-2B-6 begins.
- **Expected deliverable:** A versioned scheduling-policy revision recording exact
  weights/fairness rules (still deterministic and seed-reproducible); improved
  per-case/per-tier reservation estimation with reconciliation feedback; and updated
  scheduler tests.
- **Acceptance criteria:** Determinism invariants hold (same policy version + selection +
  seed ⇒ same queue); priority order never demotes CRITICAL work below the §11a v1
  order; `scheduling_policy_version` and `scheduling_policy_hash` are direct
  `baseline_identity` fields (§13); every scheduling-policy change segments or resets
  the stability window; runs from different scheduling-policy identities are never
  combined in one stability window; and re-baselining occurs where the merged design
  requires it (§13, §17).
- **Owner decision required:** None beyond WP-2B-6 authorization and normal PR review.
- **Explicit non-goals:** No nondeterministic ordering; no silent policy drift (every
  change is a versioned artifact).
- **Related design sections:** §11, §11a, §13 (scheduling provenance), §18 (scheduler
  tests).
- **Completion evidence:** Merged policy-revision PR(s) with tests; status updated here
  through a reviewed PR.
- **Supersedes / superseded by:** None.

### BER-BKL-013 — Exact CI workflow, artifact retention, permissions, and operator runbook

- **ID:** BER-BKL-013
- **Title:** Exact CI workflow, artifact retention, permissions, and operator runbook
- **Phase:** 2B-7
- **Priority:** REQUIRED
- **Status:** BACKLOG
- **Source / evidence:** Cross-reference: **WP-2B-7** (authoritative record for the
  phase). Merged design §16, §19 (2B-7). Owner backlog-creation directive of 2026-08-10.
- **Why it matters:** Inventory visibility for the concrete CI artifacts WP-2B-7 must
  produce: the workflow file itself, artifact-retention wiring, least-privilege
  permissions, and the operator runbook.
- **Dependencies:** As WP-2B-7.
- **Trigger to begin:** As WP-2B-7.
- **Expected deliverable:** As WP-2B-7's deliverable list (reviewed workflow; permissions;
  evidence retention; concurrency/cancellation; cadence trigger; owner-gated full-corpus
  dispatch; advisory reporting; runbook; rollback/escalation).
- **Acceptance criteria:** As WP-2B-7.
- **Owner decision required:** As WP-2B-7.
- **Explicit non-goals:** As WP-2B-7 (no blocking CI; no validator replacement).
- **Related design sections:** §16, §17, §19 (2B-7), §20 D5.
- **Completion evidence:** As WP-2B-7.
- **Supersedes / superseded by:** None (tracks WP-2B-7; that record is authoritative).

### BER-BKL-014 — Additional host adapters

- **ID:** BER-BKL-014
- **Title:** Additional host adapters (OpenAI Codex, Gemini CLI, Cursor, GitHub Copilot
  coding agent, local models, other future providers)
- **Phase:** FUTURE
- **Priority:** FUTURE
- **Status:** BACKLOG
- **Source / evidence:** Merged design §14 (host-adapter interface; Claude Code is the
  first supported adapter per D7), §21 ("no fabricated cross-provider parity"); owner
  backlog-creation directive of 2026-08-10.
- **Why it matters:** The adapter boundary keeps Project Aegis from being permanently
  tied to one vendor — but only honestly: **no cross-provider parity claim exists until
  an adapter is implemented and behaviorally verified** against the same
  activation-observation contract (§6) on its real host.
- **Dependencies:** v1 complete on the Claude Code adapter; a per-host capability spike
  equivalent to the R1/R3/R4/R5 evidence for that host — including the host's own
  monetary-cost observability or enforceable token/call/turn/session proxy reservation
  units; owner authorization per adapter.
- **Trigger to begin:** An explicit owner decision to target a specific additional host.
- **Expected deliverable:** Per adopted host: an adapter implementing
  `spawn_fresh_session` / `stream_events` / `capability_report`; host-evidence reports
  equivalent to the 2B-0 gates for that host, including an R3-equivalent per-host
  cost-observability disposition (direct monetary reservation, or enforceable
  token/call/turn/session proxy units with monetary cost reported `UNKNOWN` where
  unavailable); and behaviorally verified execution before any claim is made.
- **Acceptance criteria:** No parity or support claim for any host before its adapter is
  implemented and behaviorally verified; capability reports deny by default on unknown;
  every host-specific limitation is recorded exactly as the Claude Code limitations
  were; no live case executes on a host until its pre-dispatch reservation units are
  evidence-backed; and no cross-provider cost or safety parity is assumed.
- **Owner decision required:** Per-host adoption decision and budget.
- **Explicit non-goals:** Never blocks any v1 phase; no speculative compatibility
  matrices; no invented host capabilities.
- **Related design sections:** §14, §20 D7, §21, §24.
- **Completion evidence:** Merged adapter PR(s) plus the host's evidence reports; status
  updated here through a reviewed PR.
- **Supersedes / superseded by:** None.

### BER-BKL-015 — Optional operational products

- **ID:** BER-BKL-015
- **Title:** Optional operational products (dashboard, trends, issue automation,
  scorecards, telemetry integration)
- **Phase:** FUTURE
- **Priority:** FUTURE
- **Status:** BACKLOG
- **Source / evidence:** Future-consideration register (§10 of this file); none of these
  products appears as a v1 requirement in the merged design. Owner backlog-creation
  directive of 2026-08-10.
- **Why it matters:** Once runs exist, their value compounds through visibility — but
  every one of these is a consumer of runner evidence, not a precondition for producing
  it.
- **Dependencies:** Stable WP-2B-5/2B-6 operation producing evidence worth visualizing;
  owner adoption decision per product.
- **Trigger to begin:** An explicit owner decision to build a specific product.
- **Expected deliverable:** Per adopted product: a behavioral dashboard; historical trend
  views; automatic issue creation for confirmed regressions; behavioral release
  scorecards; and/or live skill-usage telemetry integration — each specified and
  reviewed on its own branch.
- **Acceptance criteria:** Products consume finalized, integrity-verified evidence only;
  no product gains merge/gate authority (advisory posture persists unless a separate
  owner decision changes it); no product mutates runner evidence.
- **Owner decision required:** Per-product adoption decision.
- **Explicit non-goals:** Never blocks any v1 phase; no automatic merges or gate
  activation from any product.
- **Related design sections:** §13 (evidence consumers), §16–§17 (advisory posture).
- **Completion evidence:** Merged per-product PR(s); status updated here through a
  reviewed PR.
- **Supersedes / superseded by:** None.

---

## 9. Owner-decision register

Extracted from the merged design. Identifiers and meanings are preserved exactly; nothing
here reopens decisions the design already settled (D1–D10 stand, as amended only where
§20a records a specific supersession, S1–S32). None of these decisions is made by this
backlog.

### Pending numbered owner decisions (design §20)

- **OD-1 — Judge-calibration numeric thresholds.** OWNER DECISION REQUIRED **DURING
  2B-0**. Peter Nguyen approves the initial acceptance thresholds (accuracy/agreement,
  false-PASS rate, false-FAIL rate, abstention rate) **and the separate critical
  false-PASS threshold**, together with the measured calibration result, before the judge
  produces any baseline-eligible semantic verdict (design §8, §17a). The design invents
  no numbers; so does this backlog. Tracked by: R2, BER-BKL-005, WP-2B-0, WP-2B-2 (non-live
  scaffold), and the future measured-calibration gate (formerly WP-2B-3).
  **Post-2B-0 status (2026-08-11): OPEN — not completed during 2B-0.** The design's
  during-2B-0 timing requirement above is preserved as written, not rewritten; it was
  not met because the BER-DEC-005 model-dispatch envelope denied the calibration calls
  (zero dispatches), so no measured calibration input exists. OD-1 remains OPEN, and
  semantic judging, WP-2B-3 completion, and WP-2B-4 semantic use remain blocked until a
  later reviewed and merged authorization completes the measured calibration and owner
  ratification. **Post-supersession note (2026-08-13):** the former WP-2B-3 is SUPERSEDED BY
  WP-2B-2 (BER-DEC-007); its NON-LIVE judge/calibration scaffold is delivered inside WP-2B-2,
  while the measured calibration and OD-1 ratification remain the future gate ahead of
  WP-2B-4. OD-1 stays OPEN; BER-DEC-007 does not ratify it.
- **OD-2 — Minimum promotion coverage threshold.** OWNER DECISION REQUIRED **BEFORE CI
  PROMOTION**. After the implementation-time census (BER-BKL-008) establishes the honest
  runnable denominator, Peter Nguyen ratifies the minimum authored execution/assertion
  coverage threshold; CI promotion stays blocked until the threshold is ratified and met
  (design §17). The design invents no percentage; so does this backlog. Tracked by:
  WP-2B-7's non-goals and any future promotion decision.
- **OD-3 — Risk-class ratification.** The census-proposed `CRITICAL`/`HIGH`/`STANDARD`
  assignments (design §3 item j) and the CRITICAL category list (design §10) require
  owner ratification before they gate promotion (design §10, §17). Tracked by:
  BER-BKL-008, WP-2B-1, WP-2B-6.
- **OD-4 — Evidence authenticity beyond tamper evidence.** LATER owner/security decision:
  whether to add a separately protected signing key and/or external immutable storage
  for evidence bundles (design §13). v1 claims tamper evidence after finalization only.
  Tracked by: BER-BKL-010.

### Required owner decisions without a design OD number

- **Exact evidence retention periods, access groups, and encryption mechanism.** Design
  §13 requires retention classes with defined periods, access control, and
  encryption-at-rest where sensitivity requires, but deliberately fixes none of the
  parameters. The owner sets them before evidence accumulates at scale. No OD number
  exists in the design for this item and none is invented here. Tracked by: BER-BKL-009.
- **Stronger evidence authenticity mechanism, if adopted.** The concrete mechanism choice
  under OD-4 (signing key custody, immutable store, or both), if the owner adopts one.
  Tracked by: BER-BKL-010.

### Standing approval gates (recorded in the design; recurring, not one-time)

- WP-2B-0 authorization itself, and the 2B-0 **go / no-go / limited-scope** outcome
  decision (design §17a item 10: outcome A or B).
- The **minimum Phase 2B-0 spike-evidence-handling terms** (§2 of this file): mandatory
  content of the WP-2B-0 authorization, in force before any probe or model call runs;
  temporary and spike-specific, superseded for later phases by the final BER-BKL-009
  policy delivered in 2B-1.
- Explicit owner approval of any **Tier-2 signature promotion** and its claim scope
  (design §6).
- Owner approval of any **narrower containment/claim scope** when the host cannot provide
  the full §15 boundary (design §15, §17a).
- **Full-corpus tier runs**: each requires explicit owner authorization plus a specific
  run-level spend cap (design §11, D3).
- **Critical-quarantine waivers**: each is a complete, expiring, human-issued artifact;
  no automatic and no indefinite waivers (design §10, §17).
- **Human reclassification** of any `ambiguous_needs_owner_review` runtime file before it
  can ever be agent-visible (design §5a).
- **Assertion-classification sign-off** authority: Peter Nguyen (design D9 — the
  authority is settled; the approvals recur at implementation time).
- **Promotion criterion 11**: a durable, explicit human-owner approval recorded in the
  repository before any promotion (design §17) — in addition to OD-2.

---

## 10. Future-consideration register

Recorded as FUTURE. None of these is required for v1, and **no future item may block
Phase 2B-0 or any v1 phase unless the merged design names it a gate — and the merged
design names none of them as gates.**

| Future consideration | Tracked by | Note |
| --- | --- | --- |
| Additional provider adapters (Codex, Gemini CLI, Cursor, Copilot coding agent, local models, others) | BER-BKL-014 | No parity claim until implemented and behaviorally verified |
| Cryptographically signed evidence | BER-BKL-010 / OD-4 | v1 = tamper evidence only |
| Immutable external evidence storage | BER-BKL-010 / OD-4 | Same decision family as signing |
| Long-term archival | BER-BKL-009 (policy) + BER-BKL-010 | Beyond the v1 retention classes |
| Enterprise key management | BER-BKL-009 / BER-BKL-010 | Key custody beyond v1 encryption-at-rest |
| Multi-judge consensus / arbitration | BER-BKL-011 | Requires a reviewed design successor to §8 |
| Statistical-power work beyond N=3 (beyond the decided N=5 RC escalation) | BER-BKL-011 / WP-2B-6 | D2 fixes v1 at N=3, quorum 2-of-3 |
| Human-reviewed assisted fixture generation | WP-2B-5 fixture library | D6 allows only curated, sanitized, synthetic fixtures via reviewed changes |
| Organization-wide behavioral dashboards | BER-BKL-015 | Evidence consumer, not precondition |
| Historical trend visualization | BER-BKL-015 | Evidence consumer |
| Automated issue creation | BER-BKL-015 | Evidence consumer |
| Release scorecards | BER-BKL-015 | Evidence consumer |
| Live skill-use telemetry integration | BER-BKL-015 | Evidence consumer |

---

## 11. Prohibited-pattern register — BER-PROH-001 … BER-PROH-014

These are **standing prohibitions, not backlog features**. Every record uses the §5
schema with prohibition semantics: Phase = all phases; Priority = PROHIBITED; Status =
PROHIBITED; Trigger to begin = none (never scheduled). A prohibition can change only
through an explicit, owner-approved, reviewed design successor — never through
implementation convenience. Shared fields, stated once and incorporated by reference
into each record below: **Phase:** all phases (standing prohibition). **Priority:**
PROHIBITED. **Status:** PROHIBITED. **Dependencies:** none — always in force.
**Trigger to begin:** none — never scheduled. **Owner decision required:** only an
explicit owner-approved reviewed design successor could ever alter the prohibition.
**Completion evidence:** not applicable — a prohibition is never "completed"; §18-style
tests and review keep proving its absence. **Supersedes / superseded by:** none.

### BER-PROH-001 — Retry until green

- **ID:** BER-PROH-001. **Title:** Retry until green.
- **Source / evidence:** Design §10 (no replacement attempts; never retry-until-green),
  §21, D2.
- **Why it matters:** Re-rolling stochastic attempts until one passes manufactures
  verdicts and destroys the meaning of quorum.
- **Expected deliverable / Acceptance criteria:** None to build; §18 aggregator tests
  assert replacement attempts and retry-until-green are absent.
- **Explicit non-goals:** The N planned attempts are the N reported attempts — always.
- **Related design sections:** §10, §18, §21, §20 D2.

### BER-PROH-002 — Automatically remove, disable, or prune failing cases

- **ID:** BER-PROH-002. **Title:** Automatically remove, disable, or prune failing cases.
- **Source / evidence:** Design §10 (forbidden: auto-pruning failing cases), §21.
- **Why it matters:** Deleting the evidence of failure is result laundering; failing
  cases are findings for authors, not noise for the runner to erase.
- **Expected deliverable / Acceptance criteria:** None to build; §18 tests assert
  auto-prune is absent; reports never exclude cases.
- **Explicit non-goals:** Case retirement is a human, reviewed corpus change — never a
  runner behavior.
- **Related design sections:** §10, §18, §21.

### BER-PROH-003 — Silently hide quarantined cases or erase their latest verdict

- **ID:** BER-PROH-003. **Title:** Silently hide quarantined cases or erase their latest
  verdict.
- **Source / evidence:** Design §10 and §20a-S1/S2/S23: quarantine is orthogonal
  metadata; `latest_aggregate_verdict` is never erased; CRITICAL quarantine never
  silently leaves promotion accounting.
- **Why it matters:** Quarantine manages instability; hiding it converts an honesty
  mechanism into a laundering mechanism, worst of all for critical safety evidence.
- **Expected deliverable / Acceptance criteria:** None to build; §18 tests assert
  quarantine never mutates the latest verdict and reports never exclude quarantined
  cases.
- **Explicit non-goals:** Gate exclusion for HIGH/STANDARD is advisory-layer only and
  always visible; CRITICAL requires a complete, unexpired, human-issued waiver.
- **Related design sections:** §10, §13, §17, §18, §20a S1/S2/S23.

### BER-PROH-004 — Automatically rewrite skill contracts, prompts, fixtures, or eval assertions to manufacture a pass

- **ID:** BER-PROH-004. **Title:** Automatically rewrite skill contracts, prompts,
  fixtures, or eval assertions to manufacture a pass.
- **Source / evidence:** Design §3 (outliers recorded, never silently normalized), §5
  (the runner never rewrites an assertion to make it judgeable), §5c (no case
  rewriting), §21, D8.
- **Why it matters:** The corpus is the contract under test. A runner that edits the test
  to fit the behavior measures nothing.
- **Expected deliverable / Acceptance criteria:** None to build; divergences produce
  author-facing findings; any corpus change is a separate reviewed change by humans.
- **Explicit non-goals:** No auto-retyping of `should_not_do`; no silent fixture edits;
  no assertion weakening.
- **Related design sections:** §3, §5, §5b, §5c, §21, §20 D8.

### BER-PROH-005 — Convert infrastructure errors into behavioral failures

- **ID:** BER-PROH-005. **Title:** Convert infrastructure errors into behavioral
  failures.
- **Source / evidence:** Design §5 ("errors are not verdicts"), §5b (missing setup never
  becomes behavioral FAIL), N4 honesty invariants.
- **Why it matters:** A case that could not honestly run tells us nothing about the
  skill; laundering it into FAIL (or PASS) poisons every rollup built on top.
- **Expected deliverable / Acceptance criteria:** None to build; §18 tests assert
  `ERROR`/`UNRUN` paths never collapse into PASS/FAIL.
- **Explicit non-goals:** Ambiguous activation stays `ERROR` + `AMBIGUOUS_ACTIVATION`;
  fixture failures stay `ERROR` + `FIXTURE_SETUP_FAILED`.
- **Related design sections:** §4 N4, §5, §5b, §10, §18.

### BER-PROH-006 — Convert judge errors into PASS or FAIL

- **ID:** BER-PROH-006. **Title:** Convert judge errors into PASS or FAIL.
- **Source / evidence:** Design §8 and D1: judge failure (malformed verdict, refusal,
  timeout, transport error) ⇒ `JUDGE_ERROR`, counted separately, never mapped to
  PASS/FAIL.
- **Why it matters:** A failed judgment is missing evidence, not evidence; mapping it to
  a verdict fabricates a result no one produced.
- **Expected deliverable / Acceptance criteria:** None to build; §18 judge-harness tests
  assert the mapping never happens.
- **Explicit non-goals:** `JUDGE_ERROR` rate is a first-class reported metric and a
  promotion input, never a hidden bucket.
- **Related design sections:** §8, §10, §13, §17, §18, §20 D1.

### BER-PROH-007 — Expose expected answers, negative neighbors, rubrics, or answer banks to the agent under test

- **ID:** BER-PROH-007. **Title:** Expose expected answers, negative neighbors, rubrics,
  or answer banks to the agent under test.
- **Source / evidence:** Design §5a (two separated surfaces; §20a-S18), §15
  (control-plane inaccessibility), §18 (benchmark-contamination probes).
- **Why it matters:** Leaking the benchmark to the benchmark-taker invalidates every
  routing and behavior claim the runner exists to make.
- **Expected deliverable / Acceptance criteria:** None to build beyond the designed
  separation; contamination probes must pass through every tool path before broad
  execution.
- **Explicit non-goals:** No eval file, case manifest, expectation, rubric, or answer
  bank is ever agent-visible; ambiguous runtime files fail closed.
- **Related design sections:** §5a, §15, §18, §20a S18.

### BER-PROH-008 — Claim that unexecuted evals passed

- **ID:** BER-PROH-008. **Title:** Claim that unexecuted evals passed.
- **Source / evidence:** Design D3 lineage (structural-only convention), §13 (defaults:
  `UNRUN` attempts; `INCONCLUSIVE` aggregates until real executed attempts reach
  quorum), §24 non-claims;
  [`docs/skill-generation-standard.md`](../skill-generation-standard.md) §6.
- **Why it matters:** This is the founding honesty rule of the whole corpus: structural
  validity is never behavioral proof.
- **Expected deliverable / Acceptance criteria:** None to build; the report shape itself
  proves nothing ran until something did.
- **Explicit non-goals:** No "pass" language for present-and-well-formed evals, in any
  artifact, ever.
- **Related design sections:** §2, §13, §24.

### BER-PROH-009 — Replace or weaken the structural validator

- **ID:** BER-PROH-009. **Title:** Replace or weaken the structural validator.
- **Source / evidence:** Design §16 ("weakening or removing the validator 'because the
  runner covers it' is refused"), §17 (validator stays independently mandatory even
  after promotion), N2.
- **Why it matters:** The validator is the required floor the behavioral ceiling stands
  on; removing the floor because a ceiling exists inverts the architecture.
- **Expected deliverable / Acceptance criteria:** None to build;
  [`scripts/validate-skills.py`](../../scripts/validate-skills.py) and its self-tests
  remain required, independent, and untouched by runner work.
- **Explicit non-goals:** The behavioral lane never absorbs, replaces, or gates the
  structural checks.
- **Related design sections:** §4 N2, §16, §17, §21.

### BER-PROH-010 — Automatically merge based on behavioral results

- **ID:** BER-PROH-010. **Title:** Automatically merge based on behavioral results.
- **Source / evidence:** Design §21 ("no merge automation; no enabling of auto-merge; no
  blocking CI in this phase"), §16–§17 (advisory posture; promotion requires OD-2 +
  durable human approval); governance rules 9–11 of this file.
- **Why it matters:** Merge authority is human. A behavioral lane that merges (or arms
  auto-merge) on its own results is an authority escalation, not a feature.
- **Expected deliverable / Acceptance criteria:** None to build; the advisory lane
  informs and never gates; auto-merge stays prohibited unless separately and explicitly
  authorized by the owner.
- **Explicit non-goals:** No agent-armed auto-merge under any result, green or red.
- **Related design sections:** §16, §17, §21.

### BER-PROH-011 — Spend money or launch model work without enforceable owner-approved caps

- **ID:** BER-PROH-011. **Title:** Spend money or launch model work without enforceable
  owner-approved caps.
- **Source / evidence:** Design §11 (pre-dispatch reservation against hard ceilings;
  D3), §21 ("no autonomous spend without the owner-defined guardrails; no session
  dispatch without a budget reservation; no full-corpus run without explicit owner
  authorization").
- **Why it matters:** A limit is "hard" only if enforced before dispatch; anything else
  is an alert after the money is gone.
- **Expected deliverable / Acceptance criteria:** None to build beyond WP-2B-1's
  reservation machinery; a call that cannot reserve never launches.
- **Explicit non-goals:** No fabricated dollar accounting (monetary `UNKNOWN` + proxy
  units when the surface cannot expose cost, per R3).
- **Related design sections:** §11, §11a, §17a, §21, §20 D3.

### BER-PROH-012 — Invent unsupported host telemetry, activation events, cost reporting, or security guarantees

- **ID:** BER-PROH-012. **Title:** Invent unsupported host telemetry, activation events,
  cost reporting, or security guarantees.
- **Source / evidence:** Design N5 (host-honest), §6 (no fabricated stream), §15 (no
  claimed sandbox mechanism until proven), §17a constraint ("the spike does not invent a
  Claude Code API, event stream, hook, sandbox feature, configuration-isolation flag,
  cost API, or telemetry source"), §24.
- **Why it matters:** Every 2B-0 gate exists because assumed capabilities produce
  untruthful claims; inventing one re-creates the exact failure the gates prevent.
- **Expected deliverable / Acceptance criteria:** None to build; every candidate
  capability is classified proven / owner-approved limitation / unavailable-unknown.
- **Explicit non-goals:** No assumed activation API, isolation flag, or cost surface —
  the runner is built only on what 2B-0 establishes.
- **Related design sections:** §4 N5, §6, §15, §17a, §24.

### BER-PROH-013 — Use a partial skill surface to claim full-library routing evidence

- **ID:** BER-PROH-013. **Title:** Use a partial skill surface to claim full-library
  routing evidence.
- **Source / evidence:** Design §5a binding full-surface rule (§20a-S32): every
  baseline-eligible routing execution materializes the full shipped corpus;
  `partial_install` is separately scoped, separately reported, and never baseline,
  stability, coverage, or promotion evidence (§17).
- **Why it matters:** Removing rival skills makes routing artificially easy and can
  manufacture a false full-library behavioral PASS.
- **Expected deliverable / Acceptance criteria:** None to build beyond the designed rule;
  §18 materializer tests reject reduced surfaces for full-library claims.
- **Explicit non-goals:** No handpicked skill subsets for ordinary routing claims, in any
  tier.
- **Related design sections:** §5a, §5b, §12, §13, §17, §18, §20a S32.

### BER-PROH-014 — Begin broad live execution before the Phase 2B-0 gates and minimum controls are proven

- **ID:** BER-PROH-014. **Title:** Begin broad live execution before Phase 2B-0 gates and
  minimum containment, timeout, kill, evidence, and budget controls are proven.
- **Source / evidence:** Design §17a item 10 and §19 hard precondition: no live model
  phase before containment, timeouts, emergency kill, budget reservation, attempt
  recording, aggregate semantics, and bounded concurrency are implemented AND tested;
  broad general-corpus execution additionally requires 2B-0 outcome A or B.
- **Why it matters:** Running the general corpus on hope is not an option the design
  permits; the ordering exists so no live phase ever runs without its guardrails.
- **Expected deliverable / Acceptance criteria:** None to build; phase sequencing in §7
  of this file enforces the ordering, and BER-DEC-002 blocks even 2B-0 until this
  backlog merges.
- **Explicit non-goals:** No "small quick run" exception — the smallest live execution
  outside an authorized spike budget is still a live phase.
- **Related design sections:** §15, §17a, §19, §23 item 1.

---

## 12. Dependency and sequence map

```
PR #78 merged design (main @ c61aca8) — MERGED
        |
        v
Durable backlog merged (this file, via reviewed PR #79) — MERGED   <-- Phase 2B-0 may not begin before this
        |
        v
Owner authorization for WP-2B-0 merged per the work-package authorization protocol
(immutable BER-DEC entry: owner, scope, budget + units, evidence path,
evidence-handling terms, stop conditions; WP-2B-0 -> AUTHORIZED)
— MERGED: BER-DEC-005 via PR #80
        |
        v
R1-R5 evidence dispositions (WP-2B-0 reports)
— MERGED: PR #81 WP-2B-0 evidence + Outcome B
        |
        v
Owner go / no-go / limited-scope decision (design 17a outcome A or B)
— DONE: WP-2B-0 closed as Outcome B / Limited Scope
        |
        v
WP-2B-1  runner core + minimum guardrails
— DONE: PR #83 merged (main @ 72e74af); authorized by BER-DEC-006 (PR #82)
        |
        v
WP-2B-2  Scenario A Grading Stack (non-live deterministic + semantic scaffold)
— AUTHORIZED by BER-DEC-007, effective after the governance PR containing
  BER-DEC-007 is merged; combines the former WP-2B-2 + non-live WP-2B-3 scope
        |
        v
WP-2B-3  SUPERSEDED BY WP-2B-2 (non-live judge scaffold absorbed; historical
  record retained; measured calibration + OD-1 remain future, ahead of WP-2B-4)
        |
        v
WP-2B-4  Scenario A Limited-Scope Live Suite (first live phase; BLOCKED and NOT
authorized by BER-DEC-007; requires WP-2B-2 DONE, measured calibration, OD-1
ratified, selected-host R4, selected-profile R5, residual R1 disposition, and a
separate merged WP-2B-4 authorization with live budget/evidence/stop terms)
        |
        v
WP-2B-5  generic corpus execution (requires 2B-0 outcome A or B)
        |
        v
WP-2B-6  scheduling / cost / quarantine / cadence operations
        |
        v
WP-2B-7  advisory CI (reviewed workflow through gate-guard's manual-review path)
        |
        v
Separate future decision on blocking promotion (OD-2 + design 17 criteria + durable
human approval) — NOT part of v1, NOT scheduled by this backlog
```

Explicit statements about this map:

- **Merging this backlog does not authorize WP-2B-0.** It only removes one named blocker
  (governance rule 12); the owner's explicit authorization remains a separate act —
  itself a reviewed and merged change per the work-package authorization protocol (§2 of
  this file).
- **Merging a phase PR does not authorize the next phase.** Every phase begins only with
  its own merged owner authorization (§2 protocol of this file) on its own branch.
- **Each arrow requires its own evidence and its own owner decision.** No arrow is
  crossed by momentum, and no later phase may erase an earlier phase's evidence boundary
  (design §19).
- **Current state (recorded 2026-08-11):** PR #78 (design), PR #79 (backlog), PR #80
  (WP-2B-0 authorization), and PR #81 (WP-2B-0 evidence + Outcome B) are MERGED;
  WP-2B-0 is DONE — Outcome B / Limited Scope; WP-2B-1 is AUTHORIZED by BER-DEC-006,
  effective only after the governance PR containing BER-DEC-006 is merged. WP-2B-2
  through WP-2B-7 remain governed by their existing dependencies and separate
  authorization requirements — merging the WP-2B-1 authorization does not authorize
  WP-2B-2, completing WP-2B-1 does not authorize WP-2B-2, and live phases remain
  blocked pending their own evidence and owner authorization.
- **Current state (recorded 2026-08-13):** PR #82 (WP-2B-1 authorization / BER-DEC-006) and
  PR #83 (WP-2B-1 offline runner core) are MERGED; `main` is at
  `72e74af6f0183fef25e353ec2bf3a851d83b5df6`; WP-2B-1 is DONE. Under the v1.1 fast-track
  successor and BER-DEC-007 (this governance PR, pending review and manual merge): WP-2B-2 is
  redefined as the non-live **Scenario A Grading Stack** and AUTHORIZED (effective only after
  this PR is merged); the former WP-2B-3 is SUPERSEDED BY WP-2B-2 with its historical record
  retained; WP-2B-4 is the separate, BLOCKED Scenario A Limited-Scope Live Suite; and WP-2B-5
  through WP-2B-7 remain governed by their existing dependencies and separate authorization
  requirements. No arrow is crossed by momentum: measured judge calibration, OD-1
  ratification, and every live phase remain blocked pending their own evidence and owner
  authorization; BER-DEC-007 authorizes WP-2B-2 only.

---

## 13. Append-only governance log

Rules for this log: entries are **never edited or deleted**; corrections append a
superseding entry that names the entry it supersedes; mutable backlog status elsewhere in
this file may change through reviewed PRs, but historical decisions below remain visible
verbatim.

### BER-DEC-001

- **Date:** 2026-08-10
- **Decision:** The repository backlog, not conversation memory, is the authoritative
  continuation record for Behavioral Eval Runner work.
- **Owner:** Peter Nguyen
- **Evidence:** PR #78 merge commit `c61aca84554dbc38d08b8acb2bc3b0b428f3bf01`.

### BER-DEC-002

- **Date:** 2026-08-10
- **Decision:** Phase 2B-0 must not begin until this backlog is reviewed and merged.
- **Owner:** Peter Nguyen

### BER-DEC-003

- **Date:** 2026-08-10
- **Decision:** A backlog entry, status, priority, or dependency does not itself grant
  implementation authority.
- **Owner:** Peter Nguyen

### BER-DEC-004

- **Date:** 2026-08-10
- **Decision:** Actual PR content must be reviewed before any merge recommendation.
- **Owner:** Peter Nguyen

### BER-DEC-005

- **Date:** 2026-08-11
- **Decision:** Authorize WP-2B-0 — the Behavioral Eval Runner capability and
  evidence spike — under the exact scope, budget, evidence policy, and stop
  conditions below. This authorization becomes effective only when the PR
  containing this entry is reviewed and merged.
- **Owner:** Peter Nguyen
- **Repository:** `ModernNomad-98/Project-Aegis`
- **Authorized work package:** `WP-2B-0`
- **Authorized execution branch:** `spike/behavioral-eval-runner-2b-0`
- **Authorization PR:** `#80`
- **Authorized source baseline:** the immutable GitHub merge commit recorded
  for PR #80 after its manual merge, plus that commit's Git tree SHA. Binding
  baseline rules:
  1. the execution session must resolve PR #80's GitHub `merge_commit_sha`;
  2. it must verify that PR #80 is merged and that the merge commit contains
     this reviewed authorization;
  3. it must create `spike/behavioral-eval-runner-2b-0` directly from that
     exact merge commit — not from a later moving `main`;
  4. it must record in the ownership marker and repository-safe summary: the
     authorization PR number; the authorization merge SHA; the authorization
     merge tree SHA; the execution branch base SHA; and the execution branch
     base tree SHA;
  5. all five SHA/tree values must agree where applicable before any evidence
     collection;
  6. if a later main commit is desired, a new reviewed and merged
     authorization is required — the execution session may not silently adopt
     it.
- **Authorized scope:**
  - R1 activation-observation evidence and truthful claim-scope report;
  - R2 pinned-judge selection and bounded calibration evidence;
  - R3 monetary-cost or enforceable proxy-reservation evidence;
  - R4 OS/host isolation and per-tool-path confinement evidence;
  - R5 execution-profile observability and isolation evidence;
  - an evidence-backed owner decision package for WP-2B-0 outcome A, outcome B,
    no-go, or incomplete/blocked.
- **Explicitly forbidden scope:**
  - runner-core implementation;
  - production schemas;
  - deterministic-grader implementation;
  - semantic-judge implementation;
  - Scenario A live-suite implementation or execution;
  - generic corpus execution;
  - skill or eval modification;
  - workflow or CI modification;
  - package installation without a separately reviewed authorization;
  - broad environment collection;
  - production deployment;
  - authorization of WP-2B-1 or any later work package.
- **External evidence root:**
  `C:\temp\Project-Aegis-BER-WP-2B-0-Evidence`
- **Repository-safe closeout artifacts required after the spike (exactly
  these):**
  - `docs/evidence/behavioral-eval-runner-wp-2b-0-summary.md`
  - `artifacts/evidence/behavioral-eval-runner-wp-2b-0-manifest.json`
  - `artifacts/evidence/behavioral-eval-runner-wp-2b-0-finalization.json`
- **Budget and enforceable units — monetary rule:**
  - owner monetary ceiling: USD `$5.00` total;
  - USD `$5.00` may be called a HARD monetary ceiling only if R3 proves
    direct, pre-dispatch monetary reservation;
  - if direct monetary reservation is unavailable: monetary spend is reported
    `UNKNOWN`; no statement may claim that USD $5 was technically enforced;
    and model work may proceed only under the complete enforceable proxy
    envelope below.
- **Budget and enforceable units — mandatory pre-dispatch proxy envelope:**
  before any model call, prove that ALL of the following are enforceable:
  - maximum model dispatches: `20`;
  - maximum assistant turns: `60`;
  - maximum concurrency: `1`;
  - maximum session duration: `15 minutes`;
  - maximum total authorization wall-clock duration: `4 hours`;
  - and either direct monetary reservation within USD `$5.00`, or enforceable
    input/output token ceilings (maximum observable input tokens: `400000`;
    maximum observable output tokens: `80000`) plus the call/turn/session
    limits above;
  - a control that is only observable after use is not a hard cap;
  - if the complete applicable envelope cannot be enforced before dispatch: no
    model call is authorized; R3 is recorded unavailable/unknown; and WP-2B-0
    stops with a bounded non-model report.
- **Budget and enforceable units — cumulative authorization ledger:**
  - required ledger, created before any model call:
    `C:\temp\Project-Aegis-BER-WP-2B-0-Evidence\budget-ledger.json`;
  - the ledger must record: authorization ID; authorization merge SHA;
    execution-session ID; started_at; the absolute wall-clock deadline;
    monetary reservation status; monetary reserved / actual / released /
    `UNKNOWN`; dispatches reserved and consumed; assistant turns consumed;
    input/output tokens reserved and consumed where available; current
    in-flight reservations; remaining authorized units; and every denial
    caused by a cap;
  - the ledger is cumulative for BER-DEC-005 and may never reset;
  - exactly one Claude Code control session is authorized under BER-DEC-005;
    the ownership marker must record that execution-session ID and the
    budget-ledger path;
  - if that control session terminates before closeout: evidence is preserved;
    the spike stops incomplete/blocked; no second session or refreshed budget
    is authorized; and resumption requires another reviewed and merged
    authorization.
- **Execution order:**
  1. establish and validate the evidence root, ownership marker, physical-path
     controls, evidence-handling controls, and the cumulative budget ledger;
  2. perform non-model, read-only R3 capability inspection;
  3. perform non-model R4/R5 configuration and capability inspection;
  4. only after R3's complete pre-dispatch envelope is proven, and only inside
     a disposable synthetic probe workspace, conduct bounded model-driven R4
     per-tool-path probes and R5 effective-profile probes where non-model
     inspection cannot prove actual behavior;
  5. conduct the bounded R1 activation-observation work only if the
     established boundary safely supports it;
  6. conduct the bounded R2 calibration work only if all preceding
     prerequisites remain satisfied;
  7. stop and prepare the repository-safe owner-decision package.
- **Bounded model-driven R4/R5 probe constraints:** the model-driven R4/R5
  probes must:
  - use synthetic canaries only;
  - never target real credentials, user files, private repositories, or
    unrestricted directories;
  - be ledger-reserved before dispatch;
  - run under concurrency `1` and all existing call/token/turn/session/time
    limits;
  - stop on the first unsafe, escaped, or ambiguous tool path;
  - record unavailable/unknown rather than bypassing an unprovable boundary;
  - never become Scenario A or corpus execution.
- **Stop conditions:**
  - PR #80 is not merged;
  - PR #80's merge SHA or merge tree SHA cannot be resolved;
  - the execution branch base differs from PR #80's merge SHA/tree;
  - the repository or execution branch differs from BER-DEC-005;
  - evidence root exists without the correct ownership marker;
  - evidence-handling terms cannot be enforced;
  - encryption-at-rest requirements cannot be met for sensitive raw evidence;
  - any secret, token, password, credential, private key, or unrestricted
    environment dump would be collected;
  - the complete applicable pre-dispatch budget envelope (monetary or proxy)
    cannot be enforced before dispatch;
  - the cumulative budget ledger is absent, unwritable, or would be reset;
  - the single authorized control session has terminated before closeout;
  - budget, token, dispatch, turn, concurrency, session, or wall-clock cap is
    reached;
  - any relevant tool path cannot be contained;
  - the control-plane eval corpus cannot be proven inaccessible;
  - an unauthorized repository file would be modified;
  - a package install, broad corpus execution, deployment, or later-phase task
    would be required;
  - evidence integrity cannot be verified;
  - finalization evidence is circular, incomplete, mismatched, or
    unverifiable;
  - any unexpected condition makes a claim uncertain.
- **Authority boundary:** This authorization grants WP-2B-0 only after merge.
  It does not authorize WP-2B-1, runner implementation, corpus execution, CI
  wiring, deployment, or any automatic merge.
- **Supersedes / superseded by:** None.

#### BER-DEC-005 — minimum spike-evidence-handling terms (binding)

These terms are recorded as part of the BER-DEC-005 authorization, satisfying
the minimum Phase 2B-0 spike-evidence-handling terms required by §2 of this
file. They carry no separate backlog ID, and they bind every WP-2B-0 probe,
model call, and evidence artifact.

1. **Evidence root:** `C:\temp\Project-Aegis-BER-WP-2B-0-Evidence`.
2. **Ownership marker:**
   `C:\temp\Project-Aegis-BER-WP-2B-0-Evidence\.aegis-owned-evidence.json` —
   the marker must record: authorization ID (`BER-DEC-005`); work package
   (`WP-2B-0`); owner (Peter Nguyen); repository; execution branch; creation
   timestamp; the exact evidence root; the expiration timestamp; the
   authorization PR number (`#80`); the authorization merge SHA; the
   authorization merge tree SHA; the execution branch base SHA; the execution
   branch base tree SHA; the single authorized execution-session ID; and the
   budget-ledger path.
3. **Evidence recipients (three explicit classes; no wider access):**
   - **A. Raw/confidential evidence readers:** only Peter Nguyen and the
     single authorized local Claude Code control session identified in the
     ownership marker. No plugin, MCP server, hook, cloud-sync process,
     unrelated service, or other person may read raw/confidential evidence.
   - **B. Narrow model/provider recipients:** the system-under-test
     provider/model used for R1 and for the bounded model-driven R4/R5
     capability probes, and the separately configured independent judge
     provider/model used for R2, may receive ONLY the minimum synthetic or
     redacted prompt/evidence envelope required for that specific call, after
     redaction and sanitization, with no credential, no token, no private
     key, no raw configuration dump, no private path, no unrelated evidence,
     and no private chain-of-thought. For every provider call the evidence
     manifest must record: purpose (exactly one of `R1`, `R2`, `R4`, `R5`);
     provider; model/version where observable; system-under-test versus judge
     role; payload SHA-256; payload byte count; redaction status; dispatch
     timestamp; response artifact reference; and the budget-ledger
     reservation reference. For every R4/R5 probe call the manifest must
     additionally record: the tool path or execution-profile property under
     test; the synthetic canary ID; the expected boundary; the observed
     result; the response artifact reference; and the budget-ledger
     reservation reference. The R2 judge must remain a separate, independent,
     minimum-context, no-tools call/session and receive only the minimum
     verified calibration envelope. Provider receipt of the minimum sanitized
     payload does not authorize provider access to the external evidence
     root.
   - **C. Repository/public readers:** only after owner review may the public
     repository receive the sanitized summary, the sanitized evidence
     manifest, and hashes and dispositions — no raw transcript, no
     confidential artifact, no personal path, and no secret or credential.
     The repository-safe closeout files are intentionally public-safe
     outputs, not raw/confidential evidence.
4. **Data classification:** CONFIDENTIAL — INTERNAL TECHNICAL EVIDENCE.
5. **Forbidden evidence content:** credentials; access tokens; passwords;
   private keys; authentication cookies; complete environment-variable dumps;
   unrestricted filesystem listings; real customer or patient data; private
   source content unrelated to Project Aegis; personal email addresses or
   user-profile paths in repository-safe outputs.
6. **Redaction:** before writing or sharing evidence, replace personal
   usernames, user-profile paths, personal email addresses, machine IDs,
   device serials, internal hostnames, private URLs, and tokens or
   secret-like values with explicit placeholders.
7. **Encryption at rest:** raw or confidential evidence may be stored only on
   a locally encrypted volume; before collecting such evidence, verify
   BitLocker or equivalent protection. If encryption cannot be verified, STOP
   before collecting confidential evidence.
8. **Retention:** 30 calendar days from first evidence creation; the exact
   expiration timestamp must be written into the ownership marker; no
   extension is allowed without another reviewed and merged authorization
   update.
9. **Preserve on failure:** failed or partial evidence is preserved for owner
   review, but remains subject to the same expiration unless a reviewed
   extension is merged.
10. **Cleanup:** cleanup may target only the exact marked evidence root.
    Before deletion: verify the marker; verify the authorization ID; verify
    the physical path; and verify the root contains no repository checkout.
    After deletion: verify the evidence root no longer exists; and record the
    cleanup result in the repository-safe closeout summary. Do not use broad
    `git clean`, wildcard deletion, or deletion outside the marked root.
11. **Repository-safe closeout:** the closeout PR after WP-2B-0 must contain:
    the sanitized summary; the evidence manifest; the detached finalization
    marker
    (`artifacts/evidence/behavioral-eval-runner-wp-2b-0-finalization.json`);
    SHA-256 hashes of retained evidence artifacts; R1–R5 dispositions; the
    owner decision package; the resulting WP-2B-0 outcome; no raw transcript;
    no credential; no personal path; and no unrestricted configuration dump.
    The repository-safe closeout artifacts are exactly the three files named
    in BER-DEC-005.
12. **Integrity — binding finalization protocol (non-circular):**
    1. finalize the sanitized summary first;
    2. create the canonical evidence manifest over: every retained
       raw/confidential evidence artifact, listed by sanitized relative
       identifier; every retained sanitized evidence artifact; and the
       repository-safe summary — each entry carrying byte count, SHA-256,
       sensitivity, redaction state, and creation timestamp;
    3. the evidence manifest MUST NOT list itself, and MUST NOT list the
       detached finalization marker;
    4. hash the finalized summary and the finalized manifest;
    5. write the detached finalization marker
       (`artifacts/evidence/behavioral-eval-runner-wp-2b-0-finalization.json`)
       containing: authorization ID; authorization PR number; authorization
       merge SHA; execution-session ID; evidence-manifest SHA-256;
       repository-safe summary SHA-256; final spike status; and the
       finalized_at timestamp;
    6. the detached marker is not included in the evidence manifest;
    7. the repository-safe summary must not contain the final manifest hash
       or the finalization-marker hash;
    8. no artifact may directly or indirectly contain a hash computed over
       itself;
    9. owner review must independently verify every manifest-listed artifact,
       the manifest hash, the summary hash, and the detached marker;
    10. the marker's own SHA-256 is recorded externally by the consuming
        review record or Git repository object, never inside the marker or
        the manifest. SHA-256 provides tamper evidence after finalization
        only; no cryptographic authenticity beyond that is claimed.
13. **Reparse-safe physical-path validation (binding):** before evidence-root
    creation, before every evidence read, every evidence write, and every
    evidence hash, and again before cleanup:
    1. resolve every existing path component from the volume root through
       `C:\temp`, the evidence root, and the exact target path;
    2. reject any symlink, junction, mount, or other reparse point anywhere
       in that path chain;
    3. fail closed if any path component cannot be resolved unambiguously;
    4. verify the resolved evidence root is physically beneath the resolved
       `C:\temp` directory;
    5. verify the evidence root is outside every Project Aegis checkout, the
       source repository, the execution repository, and any Git repository;
    6. verify every target remains physically beneath the validated evidence
       root;
    7. reject any child path that introduces a reparse point after root
       creation;
    8. repeat the complete physical-path validation immediately before
       deletion;
    9. stop if: the resolved physical path changes; a reparse point appears;
       the root resolves outside `C:\temp`; the root or target resolves
       inside a repository; or physical-path verification becomes
       unavailable or ambiguous.
    Cleanup still targets only the exact ownership-marker-bound root; all
    existing marker, retention, encryption, and deletion rules remain in
    force.

### BER-DEC-006

- **Date:** 2026-08-11
- **Decision:** Close WP-2B-0 under the owner-accepted Outcome B / Limited
  Scope and authorize WP-2B-1 to build the non-live Behavioral Eval Runner
  control plane and minimum guardrails under the exact limitations, scope,
  evidence terms, and stop conditions below. Authorization becomes effective
  only after the reviewed PR containing BER-DEC-006 is manually merged.
- **Owner:** Peter Nguyen
- **Repository:** `ModernNomad-98/Project-Aegis`
- **Evidence basis:**
  - PR #81;
  - merge commit
    `55b0c4b4f5c0cba9bbf70f63cd0ebf8212f8eae5`;
  - owner-accepted Outcome B / Limited Scope;
  - the owner-side integrity-gate verification record — this reviewed repository
    record, not conversation memory, is the durable record of the owner verification:
    - **Verification owner:** Peter Nguyen
    - **Verification date:** 2026-08-11
    - **Verification result:** PASS
    - **Repository-safe summary SHA-256:**
      `a18b18899272a96826fa6d1bb4af1908782c3fb03bd591afefdd83bd21816374`
    - **Evidence manifest SHA-256:**
      `f304b889477a4c72f55c1462c9079f02efa9ede87d7cc5c3376d542376dd3969`
    - **Detached finalization marker SHA-256:**
      `c33bd26edac562c12578ff1b2231c440718d2bbbd1b19ad7e365f60b862b543c`
    - **External-artifact result:** all 12 manifest-listed external artifacts
      matched their recorded byte counts and SHA-256 values.
    - **Path-safety result:** no reparse point was found in the validated path
      chains.
    - **Verification mode:** independent owner-run, read-only PowerShell integrity
      gate;
  - detached-marker SHA-256
    `c33bd26edac562c12578ff1b2231c440718d2bbbd1b19ad7e365f60b862b543c`.
- **Closed work package:** `WP-2B-0`
- **Authorized work package:** `WP-2B-1`
- **Authorized implementation branch:**
  `feat/behavioral-eval-runner-2b-1`
- **Authorized source baseline:** the immutable GitHub squash-merge commit of
  the reviewed PR containing BER-DEC-006. The future implementation session
  must resolve that merge SHA and tree and create the implementation branch
  directly from them, never from a later moving `main`.
- **Authorized scope:**
  - non-live runner core;
  - versioned attempt, aggregate, run, case, fixture, materialization,
    execution-profile, and evidence schemas;
  - immutable workspace materializer;
  - separation of agent-visible runtime and control-plane surfaces;
  - sanitized runtime-surface builder;
  - implementation-time corpus census;
  - capability and fixture preflight;
  - fail-closed containment interfaces and guards;
  - timeout and process-tree emergency-kill controls;
  - bounded concurrency machinery;
  - runner-owned pre-dispatch dispatch/call/turn/token/session reservation
    machinery;
  - deterministic budget-aware scheduler;
  - evidence writer and non-circular finalization machinery;
  - attempt and N/quorum controller;
  - host-adapter interface;
  - non-live Claude Code adapter scaffolding that denies unavailable or
    unproven capabilities;
  - report generator with honest UNRUN/ERROR/default states and complete
    coverage metrics;
  - deterministic unit, integration, schema, scheduler, evidence, and
    containment tests using mocks and synthetic fixtures;
  - a sanitized WP-2B-1 implementation closeout summary.
- **Outcome B constraints:**
  - no implementation may claim R1, R2, R3, R4, or R5 is technically solved;
  - live dispatch remains disabled by default;
  - all unproven host capabilities deny or report unavailable/unknown;
  - the Claude Code adapter must not expose a live-dispatch path in this phase;
  - no baseline, routing, containment, semantic-judge, or promotion claim may
    result from WP-2B-1;
  - R2 and OD-1 remain blocked/open;
  - WP-2B-1 neither selects nor calibrates a judge;
  - WP-2B-1 does not satisfy R2;
  - later live phases require their own evidence and authorization.
- **Explicitly forbidden scope:**
  - model/provider dispatch by the new runner;
  - live Claude Code session spawning by the runner;
  - Scenario A execution;
  - generic eval execution;
  - deterministic grader implementation owned by WP-2B-2;
  - semantic judge implementation owned by WP-2B-3;
  - CI/workflow wiring;
  - skill or eval modification;
  - validator or gate modification;
  - deployment;
  - package installation or dependency addition without another reviewed
    authorization;
  - authorization of WP-2B-2 or any later work package.
- **Model and spend budget:**
  - runner-generated model/provider dispatches: `0`;
  - runner-generated live sessions: `0`;
  - external model/API spend: USD `$0`;
  - package installations: `0`;
  - no network use except Git/GitHub operations required for the reviewed PR;
  - all tests must use mocks, recorded synthetic fixtures, or local
    deterministic harnesses.
- **External build-evidence root:**
  `C:\temp\Project-Aegis-BER-WP-2B-1-Implementation-Evidence`
- **Build-evidence handling:**
  - classification: INTERNAL TECHNICAL BUILD EVIDENCE;
  - permitted content: test logs, schema-validation results, local coverage
    summaries, timing records, validator output, DCO output;
  - forbidden content: credentials, tokens, passwords, private keys, personal
    paths, unrestricted environment/configuration dumps, raw model
    transcripts, real customer/patient data;
  - retention: 30 calendar days from first creation;
  - an ownership marker must bind the root to BER-DEC-006 and the exact
    implementation branch/base;
  - cleanup must be marker-gated and physically reparse-safe;
  - repository-safe outputs may contain only sanitized implementation evidence;
  - authorized readers/writers (least privilege, binding): Peter Nguyen through the
    Windows account running the authorized WP-2B-1 implementation session; Windows
    SYSTEM only where required for normal local filesystem operation; and no other
    local user, service account, plugin, MCP server, hook, cloud-sync process, or
    network service;
  - before the first build-evidence write: (1) resolve the physical path from the
    volume root through `C:\temp` and the exact evidence root; (2) reject symlinks,
    junctions, mounts, and other reparse points; (3) verify the evidence root is
    outside every Git repository and Project Aegis checkout; (4) create or configure
    the evidence root with ACL inheritance disabled; (5) verify no broad read/write
    principal remains, including Everyone, Users, and Authenticated Users; (6) verify
    only the authorized Windows account and SYSTEM retain required access; (7) record
    a sanitized ACL-verification result in the external ownership marker or
    build-evidence log, recording no personal username or profile path in
    repository-safe output; (8) reverify physical containment and ACLs before every
    cleanup operation;
  - if the ACL or physical-path boundary cannot be established and verified: STOP
    before writing build evidence.
- **Stop conditions:**
  - repository, authorization merge SHA/tree, branch base, or scope differs;
  - any runner/model/provider dispatch would occur;
  - a package installation or dependency addition is required;
  - an existing skill, eval, workflow, validator, gate, design, or unrelated
    roadmap would need modification;
  - a capability would need to be claimed without evidence;
  - a test cannot remain deterministic and offline;
  - an unauthorized file path would be changed;
  - structural validation fails;
  - the build-evidence root's least-privilege ACL or physical-path boundary cannot
    be established and verified;
  - an unexpected condition makes a claim uncertain.
- **Authority boundary:** This authorizes WP-2B-1 only after merge. It does not
  authorize WP-2B-2, live execution, Scenario A, corpus execution, CI
  promotion, deployment, auto-merge, or merge.
- **Supersedes / superseded by:** None.

### BER-DEC-007

- **Date:** 2026-08-13
- **Decision:** Adopt the Behavioral Eval Runner **v1.1 fast-track successor**
  ([`docs/design/behavioral-eval-runner-v1-fast-track-successor.md`](../design/behavioral-eval-runner-v1-fast-track-successor.md)).
  Combine the NON-LIVE implementation scope of the former WP-2B-2 (deterministic graders) and
  the former WP-2B-3 (semantic judge) into the revised **WP-2B-2 — Scenario A Grading Stack**.
  Mark the former WP-2B-3 **SUPERSEDED BY WP-2B-2** (historical record retained). **Authorize
  WP-2B-2 only.** Keep **WP-2B-4 BLOCKED and unauthorized.** This authorization becomes
  effective only after the reviewed PR containing BER-DEC-007 is manually merged.
- **Owner:** Peter Nguyen
- **Repository:** `ModernNomad-98/Project-Aegis`
- **Authorization PR:** AUTHORIZATION_PR_PENDING
- **Evidence basis:**
  - WP-2B-1 DONE — [PR #83](https://github.com/ModernNomad-98/Project-Aegis/pull/83), merge
    commit `72e74af6f0183fef25e353ec2bf3a851d83b5df6` (offline runner core + minimum
    guardrails);
  - WP-2B-1 authorization — [PR #82](https://github.com/ModernNomad-98/Project-Aegis/pull/82),
    BER-DEC-006, merge commit `fc98ee6bf59bb516064be62ed8c5dc8861c92697`;
  - the v1.1 fast-track successor design (this governance PR).
- **Closed / updated work packages:** WP-2B-1 → DONE; former WP-2B-3 → SUPERSEDED BY WP-2B-2.
- **Authorized work package:** `WP-2B-2` (Scenario A Grading Stack — non-live).
- **Authorized implementation branch:**
  `feat/behavioral-eval-runner-2b-2-scenario-a-grading-stack`
- **Authorized source baseline:** the future exact manual merge/squash commit and Git tree of
  this governance PR. The implementation session must resolve and verify those values before
  creating or using the implementation branch, and never branch from a later moving `main`.
- **Authorized scope (NON-LIVE only — v1.1 successor §4):**
  - **Deterministic Scenario A graders:** stage-transition validation; authorization and
    approval-boundary validation; prohibited-action and mutation checks; append-only evidence
    checks; preview-versus-created hashing (run-local only); recording-state checks; typed
    skill/subagent target handling; invocation-mode validation when supported by available
    evidence; deterministic Scenario A controls A–Q; versioned deterministic reason codes;
    evidence pointers; deterministic recorded good/bad fixtures; unit, integration, and schema
    tests.
  - **Semantic Scenario A grading scaffolding:** an independent judge interface; pinned
    judge-identity representation; injection-resistant system policy; transcript treated as
    delimited untrusted data; no judge tools; least-context input envelope; schema-validated
    structured verdict; `JUDGE_ERROR` fail-closed behavior; the coherent-topic grading
    contract; other Scenario A assertions that cannot be mechanically graded; a minimum
    versioned human-labeled calibration-dataset structure; a deterministic/mock calibration
    harness; threshold-enforcement logic using recorded/mock results; a drift/recalibration
    trigger representation; unit, integration, injection-defense, and schema tests.
  - The semantic scaffold must be testable with deterministic mocks and recorded fixtures
    only. **No actual model or provider call is authorized. No measured calibration result
    may be claimed.**
- **Model and spend budget:**
  - runner-generated model/provider dispatches: `0`;
  - runner-generated live sessions: `0`;
  - actual judge/provider calls: `0`;
  - external model/API spend: USD `$0`;
  - package installations: `0`.
- **External build-evidence root:**
  `C:\temp\Project-Aegis-BER-WP-2B-2-Scenario-A-Grading-Stack-Evidence`
- **Evidence classification:** INTERNAL TECHNICAL BUILD EVIDENCE.
- **Permitted evidence:** test logs; deterministic fixture outputs; schema-validation
  results; mock judge results; recorded human-labeled calibration fixtures; mock
  calibration-harness output; timing; validator output; DCO output; scope verification;
  static/security scans.
- **Forbidden evidence:** credentials; tokens; passwords; private keys; unrestricted
  environment dumps; private source unrelated to Project Aegis; real user/customer/patient
  data; actual live judge responses; actual provider transcripts; personal paths in
  repository-safe outputs; private chain-of-thought.
- **Retention:** 30 calendar days from first evidence creation unless another reviewed and
  merged authorization changes it.
- **Ownership and ACL (same least-privilege principles recorded by BER-DEC-006):**
  - an ownership marker binding the root to BER-DEC-007, WP-2B-2, the implementation branch,
    the base SHA, and the expiration;
  - ACL inheritance disabled;
  - only Peter Nguyen's authorized Windows account and SYSTEM retain required access;
  - no Everyone, Users, or Authenticated Users broad access;
  - evidence root outside every Git repository and Project Aegis checkout;
  - fail closed on symlink, junction, mount, reparse, identity, or ACL ambiguity;
  - marker-gated, physically reparse-safe cleanup.
- **Explicitly forbidden scope:**
  - actual model/provider/judge dispatch;
  - measured judge calibration;
  - OD-1 ratification by an agent;
  - live Claude Code session spawning by the runner;
  - Scenario A live execution;
  - generic corpus execution;
  - WP-2B-4 implementation;
  - WP-2B-5 implementation;
  - CI/workflow wiring;
  - skill modification;
  - authored-eval modification;
  - validator or gate modification;
  - deployment;
  - package or dependency installation;
  - native FFI;
  - automatic authorization of later phases;
  - merge or auto-merge.
- **Stop conditions:** Stop if —
  - repository, base, branch, authorization, or scope differs;
  - the source baseline cannot be verified;
  - any model/provider/judge call would occur;
  - a package or dependency is required;
  - a skill, eval, workflow, validator, gate, or unrelated design file must change;
  - the evidence root cannot satisfy its marker, ACL, path, or retention terms;
  - a test cannot remain deterministic and offline;
  - an unauthorized repository path must change;
  - generic corpus or live Scenario A work becomes necessary;
  - WP-2B-4 work becomes necessary;
  - a capability would have to be claimed without evidence;
  - DCO, validation, scope, or evidence integrity fails;
  - force-push, reset, rebase, amend, auto-merge, or merge is required;
  - an unexpected condition makes a claim uncertain.
- **Authority boundary:** BER-DEC-007 becomes effective only after its governance PR is
  reviewed and manually merged. It authorizes **WP-2B-2 only**. It does not authorize:
  actual calibration; OD-1 ratification; WP-2B-4; live execution; WP-2B-5; generic corpus
  execution; CI; deployment; promotion; or merge of an implementation PR.
- **Supersedes / superseded by:** Supersedes the former WP-2B-3 (semantic judge) by absorbing
  its NON-LIVE scaffold into the revised WP-2B-2 (via the v1.1 fast-track successor).
  BER-DEC-001 through BER-DEC-006 are unchanged. Superseded by: None.

---

## 14. Continuation instructions for a brand-new session

A future session (human or AI) resuming Behavioral Eval Runner work follows these steps
before doing anything else:

1. **Read [`AGENTS.md`](../../AGENTS.md) and [`CLAUDE.md`](../../CLAUDE.md)** and follow
   their workspace-role and skill-routing rules.
2. **Verify the repository, branch, HEAD, and clean working tree** with read-only Git
   commands before any write.
3. **Read the merged Behavioral Eval Runner design**
   ([`docs/design/behavioral-eval-runner-v1.md`](../design/behavioral-eval-runner-v1.md))
   — it is authoritative for architecture and controls.
4. **Read this backlog** — it is authoritative for continuation and deferred work.
5. **Determine whether the requested item is authorized**: find its record here, check
   its Status, and check the owner-decision register. Only AUTHORIZED work may proceed —
   meaning the governing WORK-PACKAGE record is AUTHORIZED through the work-package
   authorization protocol's merged BER-DEC entry (§2 of this file), and the requested
   item is either that work package or a child record explicitly inside its recorded
   scope. A child record's own status never grants authority.
6. **Do not infer authorization from an item being present.** Presence in this register
   is a record, not a grant (BER-DEC-003). A chat message, assistant memory, temporary
   file, or unmerged branch is never sufficient implementation authority.
7. **Do not begin Phase 2B-0 unless ALL of the following hold:** this backlog is merged
   (BER-DEC-002); a WP-2B-0 authorization is merged per the work-package authorization
   protocol (§2 of this file), appending its immutable BER-DEC entry and moving WP-2B-0
   to AUTHORIZED; and that authorization records the exact scope, repository, branch,
   budget with enforceable units, evidence path, minimum Phase 2B-0
   spike-evidence-handling terms, and stop conditions.
8. **Record all phase outcomes durably** through reviewed repository artifacts — evidence
   reports at their authorized paths and reviewed PRs updating this register — never
   through conversation memory alone.
