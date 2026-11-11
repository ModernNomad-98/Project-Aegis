# Consumer status presentation v1 (CS-0..CS-7 display requirements)

**Status: PROPOSED display requirements for E2.2/E2.3 - not a contract, not an
implementation, not a renderer, not an acceptance, not delivery or publication
authority.** This page states how a read-only consumer status view presents the
authoritative record. It creates no status service, UI, dashboard, vocabulary,
ledger or policy, and it claims no live status value: the merged change-state
producers are auditable tooling, the verdict gate is not wired, and T2/T6
remain open.

**Source design.** E2/E4 consumer status presentation design, 59,936 B /
`4a878d2599bf578c72a2879fe465c404655d79816f2bfa59e23a5974e421fa88`.
E2/E4 Stage A plan, 55,297 B /
`84c41f7ee9ce4a7b26230e82cd4e178925802274d6f66c26284f3ec1cc9cccab`;
capture, 1,047 B / `94812fd32e9aae89ae7441e7141052f43c31982f360aacb741bdb898a0d3b1da`;
Stage B audit ACCEPT, 20,719 B /
`a11b572ea24aac496d0c8e6ca3bc1afad181b2c1e977c10fd9152633de703448`;
implementation authority, 1,815 B /
`c96eb16aaec39bbcf7be6d4d1e1174206200a8a1f49a9379c54241b308ac6401`.
**Base:** origin/main `c5fe3adf7b64f3f583bd6ee12591afe36176d2da` / tree
`9d7f214c63d78721c463d972336dc1bacf0ba514`.

**Display-map version:** `cs-map/1` (candidate; not an accepted contract
version). **T2 is open**, so this page makes no contract-conformance claim and
labels every contract identifier as proposed.

**Labels.** `VERIFIED` = re-derived from a primary source; `REPORTED` = asserted
by a named record, not recomputed here; `UNKNOWN` = not derivable, resolver
named; `UNRUN` = not executed, never PASS; `STALE` = superseded record.

---

## 1. Purpose, scope and ownership

This page turns the E2.2 capability/assurance/burden obligation and the E2.3
stop/approval/recovery obligation into display requirements for one read-only
consumer status view. It consumes the E2/E4 presentation design and the
corrected contract semantics by reference; it does not re-encode contract
fields.

C&C/C0 own the contract, policy, authority and evidence semantics and the
authoritative record values. Experience presents them. The view never defines
policy, grants authority, approves a disposition, clears a blocked state or
recomputes an authoritative value.

**Not in this document:** a renderer, HTML/CSS/JS, an application, a status
service, a dashboard, a ledger, a second vocabulary, a plan revision, an
acceptance, a delivery/publication/install/release claim, or an E2/E4 closure
claim. E2.4 independent exercise and E4.1 compatibility evidence remain UNRUN.

**How it is used.** Any future consumer status surface - a page, template or
read-only view - is checked against sections 2-10. E2.4 exercises these rules
against fixtures and real entry-path refusals; it does not present fixture
output as live status. E4.1 checks that the display map version in section 9
still matches the contract version it consumes.

---

## 2. The view is a read-only projection

Every status view SHALL render one view composed of these blocks. The view SHALL
NOT compute, infer, aggregate or optimistic-update any block.

| Block | Required content | Honesty rule |
| --- | --- | --- |
| P1 Provenance | record id/type, bytes, sha256, as_of, freshness (CURRENT/STALE/UNKNOWN), producer role, contract schema version, bound-set version where a verdict is displayed | A value without an authoritative record reference is UNKNOWN, not a default |
| P2 Headline state | consumer label (frozen, awaiting review, budget exhausted, blocked, residual accepted, evidence reused) and every derived-true attribute | Multiple attributes may be true; the headline is precedence-selected; badges are not collapsed |
| P3 Reason and code | every active reason/blocker code with class MANDATORY/LIMIT/WAIT and a plain-English gloss; no bare code | A code label never replaces the reason or the authority |
| P4 Candidate identity | work-item stable id and readable name; exact 40-character head, tree and base; candidate id; freeze record and snapshot identity; observation time | Renaming a file, item or agent does not mint a new id or reset a count |
| P5 Budget panel | plan-revision count per item (limit 4, reopen used true/false, stop state) and review-head count (exclusive used, default limit 3, candidate ordinal, published-head list, exception id/status/authority/scope/expiry) | The two counters are separate; one never implies anything about the other |
| P6 Stage and settlement | required stages B/D/E/F with state, verdict value, independence class, snapshot identity, requested_at and bounded-wait reference, settlement state, review sources (SETTLED/PENDING/UNAVAILABLE_DISPOSITIONED), missing-mandatory-review flag; v2.1 affirmative rules shown as affirmative or non-affirmative | A REVISE/BLOCKED/FAIL/UNRUN displayed as such is never converted to a pass by the view |
| P7 Assurance and evidence | assurance class per item (VERIFIED/REPORTED/UNKNOWN) and its meaning; named UNRUN list; frozen denominator and counts; retention class; evidence-reuse applicability record; required versus advisory CI; bypasses; enforcement claim and mounted-coverage state | No aggregate green or score; UNRUN stays UNRUN; a bypass is a bypass; enforcement is NONE/AUDITABLE unless proved |
| P8 One permitted next action | exactly one action from section 5 with actor role, authority reference, precondition, bounded step and record reference; or "none" with reason and responsible authority | The view displays it; it never executes it as a transition or infers a different one |
| P9 Limits and UNKNOWN | every UNKNOWN with its resolver; mounted coverage UNKNOWN; consumer support limits; explicit statement that the view grants no authority or approval | Missing data displays UNKNOWN plus resolver, never an optimistic default |

**Headline precedence.** blocked > review budget exhausted > suspended >
awaiting settlement > frozen candidate > awaiting final review > residual
accepted (badge, not readiness) > ready for gate. Every derived-true badge
remains visible; the view never collapses multiple states into one green or
neutral badge that hides a blocking state. "Ready for gate" is a readiness
statement, not merge authority.

**Fail-closed projection.** If the contract is missing, stale or internally
contradictory, display BLOCKED or UNKNOWN with the reason code and
REFRESH_FROM_AUTHORITY (A10). Never display a default "ready" or "green". A
stale head/base/policy/evidence or an invalidated verdict displays
INVALIDATED/STALE with A10, never the last-good green.

**No client-side derivation.** The view may format and label only. Readiness,
counts, budgets, assurance, approval, enforcement and verdicts come from the
authoritative record; the view does not derive them.

---

## 3. Consumer labels CS-0..CS-7

### CS-0 - general projection (applies to every state)

- **Display SHALL:** read-only projection of the durable authoritative record;
  provenance with as_of and freshness; the applicable state and every
  derived-true attribute as its own badge; reason codes with class and
  plain-English gloss; exactly one permitted next action with actor, authority,
  precondition and record reference.
- **SHALL NEVER imply:** authority, approval, a pass, a completed review or
  enforcement; that the view can create, clear, advance, suspend or reopen a
  state; that a SHA-bearing comment, fix commit, freeze label, green CI or merge
  is approval; that a label, nit or theoretical classification converts a
  mandatory finding.
- **One permitted action:** CS-7 rules. "None" only with reason and responsible
  authority. Unknown data shows UNKNOWN plus resolver, never a default.
- **Assurance:** UNRUN shown as UNRUN; FAIL shown as FAIL; a bypass shown as a
  bypass; no aggregate green; the two budgets separate; consumer choice
  preserved; a REVISE grants nothing.

### CS-1 - frozen

- **Display SHALL:** candidate identity (work item, exact 40-character head,
  tree/base), freeze record id and time, pinned snapshot identity, settlement
  state, which B/D/E/F evidence is bound to that head, what is still
  outstanding, and the plain statement "frozen is not approved".
- **SHALL NEVER imply:** approval, merge readiness, a verdict, that findings
  cannot appear, that a later blocker is suppressed, or that a freeze label is
  enforcement.
- **One permitted action:** exactly one of A1 WAIT_BOUNDED, A2 COMMISSION_STAGE
  or A10 REFRESH_FROM_AUTHORITY, selected by the authoritative record; if F has
  started, no head move.
- **Assurance:** show which evidence is bound to the frozen head and which is
  still UNRUN. A previous-head PASS is not bound to this head unless an
  evidence-reuse record says VALID.

### CS-2 - awaiting review

- **Display SHALL:** which required stage or reviewer role is outstanding,
  requested_at attributed to the record, the applicable bounded-wait limit or
  "limit UNKNOWN/unconfigured", current evidence state, independence status,
  and the settlement checklist with each source's state.
- **SHALL NEVER imply:** a pass in progress, an automatic advance, that
  indefinite polling is expected, that silence is settlement, or that a Stage-B
  plan audit substitutes for implementation review.
- **One permitted action:** exactly one of A1 WAIT_BOUNDED, A2 COMMISSION_STAGE,
  A4 RECORD_UNAVAILABLE_DISPOSITION (only where the authority permits) or A8
  AWAIT_OWNER_DECISION (where authority is UNKNOWN). Missing mandatory review
  remains BLOCKED and is displayed as such.
- **Assurance:** show each required source separately; automated-only
  completion is not settlement; UNRUN or pending shown truthfully; required CI
  included in the wait.

### CS-3 - budget exhausted

- **Display SHALL:** published candidate-head list with seq, head and kind;
  exclusive used count against the default cap 3; candidate ordinal (used + 1);
  the separate plan-revision count with reopen consumption and its own limit;
  any recorded scoped exception (id, status ACTIVE/EXPIRED/REVOKED, authority
  line, scope, duration/expiry); and the plain statement "a written blocking
  finding is an exception request, not authority".
- **SHALL NEVER imply:** that defective work is accepted; that a fourth head is
  authorised without an ACTIVE scoped exception; that counting resets on
  rename, agent, restart or retitle; that budget exhaustion is an assurance
  class or acceptance; that one counter's state implies anything about the
  other.
- **One permitted action:** A5 REQUEST_SCOPED_EXCEPTION only with the
  policy-defined authority (unknown authority displays UNKNOWN and stays
  blocked), or A6 PARK_UNMERGED. No "continue anyway".
- **Assurance:** do not show the head budget as a quality or assurance label;
  show the exception as an exception, never as approval or green.

### CS-4 - blocked

- **Display SHALL:** the specific unmet mandatory condition and its class/code;
  supporting evidence; the authority or role who can unblock, or UNKNOWN with
  the resolver; the missing mandatory independent approval state; and preserved
  work.
- **SHALL NEVER imply:** that the work failed; that time, a retry or a view
  action can clear it; that a substitute approval exists; that mandatory
  approval is advisory; or that blocked is terminal.
- **One permitted action:** A8 AWAIT_OWNER_DECISION for owner-gated conditions;
  A4 only if policy permits an unavailable disposition; A10 if stale; otherwise
  the named evidence or authority acquisition. "None" requires reason and
  responsible authority.
- **Assurance:** missing mandatory review stays BLOCKED and is never settled by
  silence; stale, forged or edited verdict evidence displays INVALID or STALE
  with the reason, not blocked-with-hope.

### CS-5 - residual accepted

- **Display SHALL:** finding identity; candidate and head; requirement or
  threat boundary; supporting evidence; classification RESIDUAL or NIT; the
  authorised decision-maker and outcome/rationale; the fact that the head did
  not move; and a clear "not a pass, not readiness" statement.
- **SHALL NEVER imply:** that the finding was fixed or waived where mandatory;
  that the head moved; that aggregate assurance is green; that residual
  acceptance is permanent immunity; or that it applies to a different head.
- **One permitted action:** the applicable A-action; proceed only when all
  blocking gates independent of that finding are satisfied (A9 only under valid
  readiness); later evidence affecting the residual re-triggers triage.
- **Assurance:** residual acceptance is a badge or distinct disposition, never
  a PASS. Security, authorization, acceptance and required-validation defects
  are never labelled residual.

### CS-6 - evidence reused

- **Display SHALL:** original evidence id, head, scope, method, environment and
  result; the applicability record with source and target 40-character heads,
  affected inputs, comparison method (AST equality only as supporting
  evidence), excluded claims, target-head delta checks, independence record,
  decision VALID/INVALID/STALE, and required CI retained.
- **SHALL NEVER imply:** that an old PASS was copied to the new head; that AST
  equality alone proves equivalence; that reuse equals approval; or that
  required CI can be waived through reuse.
- **One permitted action:** run the recorded narrow delta audit and any affected
  checks not covered by the reuse record; no waiver of mandatory CI; if the
  decision is INVALID or STALE, show that with the resolver.
- **Assurance:** show the assurance class of the source evidence and that it is
  reused, not fresh; required CI retained; target D/E/F still bind the actual
  target head.

### CS-7 - actual permitted next action

- **Display SHALL:** exactly one action with label, actor role, actual authority
  reference (or UNKNOWN plus resolver), precondition, one bounded next step and
  the record reference that permits it. Where no action is permitted, "none"
  with reason and responsible authority.
- **SHALL NEVER imply:** a generic recommendation; an inference from a label or
  timestamp; authority the consumer does not hold; that the view can execute
  the transition; or that "contact the owner" is an authority. Unknown
  authority is displayed as UNKNOWN.
- **One permitted action:** mapped directly to A1-A11 in section 5. The view may
  link to or copy the record reference; a request path records a request, not
  an approval.
- **Assurance:** the action display never implies approval or readiness; A9
  appears only under valid readiness and still says the merge decision is
  separate.

---

## 4. Presentation extension states and overlays

These labels are derived from the recorded contract states. They are not new
contractual guarantees and are not separate plan items.

### CS-P0 - no active candidate

Display "No active candidate for this work item"; show the work item's separate
revision/reopen/stop state and its permitted next action. Never imply "all
good", "nothing wrong" or "approved", and never invent a candidate. The
permitted action is A11 NO_ACTION with a reason, or the authorised new-candidate
path where the policy records one.

### CS-P1 - awaiting settlement versus awaiting final review

Both use the "awaiting review" headline; the sub-status distinguishes pre-audit
settlement (S1) from a final-review wait (S3). Never imply either is a pass in
progress.

### CS-P2 - suspended

Display "suspended - final readiness not valid"; the trigger (new blocking
finding during or after F, head/base/policy/evidence invalidation, or a stale
verdict); the stage where it occurred; that work is preserved and prior
evidence retained but its bindings may be stale; and the controlled
repair/rebinding path. The permitted action is A7 REBIND_CANDIDATE under
authorised rebind authority, or A3/A8 as applicable. Never imply failed/final,
that evidence vanished, that a merge may proceed, that a freeze label
suppresses the blocker, or that rebinding is automatic. No "resume" or
"unblock" control.

### CS-P3 - ready for gate

Display "readiness satisfied for the exact current head; the merge decision
remains with the authorised G holder - readiness is not merge authority"; show
the F verdict value, exact head, bound-fields hash, required stage evidence,
budget/exception state, freeze and settlement. Never imply approved, merged,
green, that readiness authorises anyone, or that a recorded bypass counts. The
permitted action is A9 AWAIT_G_MERGE_AUTHORITY for the G role only. No merge
button.

### CS-P4 - closed / parked

Display the terminal disposition: MERGED with merge receipt identity (head,
receipt id) and every bypass recorded as a bypass, never green; or
PARKED_UNMERGED with the owner line reference. State that reopen requires an
explicit authorised new-candidate event and counts in the line. Never imply
accepted/secure by itself, a silent reopen, that merged equals independently
verified, or that parked equals failure. The permitted action is A11 NO_ACTION
with a reason, or the counted authorised new-candidate path. No reopen control.

### Overlays (apply to any display)

- **STALE/INVALIDATED:** show the reason and A10; never the last-good green.
- **UNKNOWN:** show the resolver; never an optimistic default.
- **BYPASS RECORDED:** show the owner line reference and "not green, not
  approval".
- **ENFORCEMENT NONE/AUDITABLE_GATE:** mounted coverage is UNKNOWN; an ENFORCED
  claim requires the recorded evidence.

---

## 5. One permitted next action (A1-A11)

Exactly one action is displayed. Several candidate actions may be defined for a
state, but the authoritative record selects one; the view never presents them as
equally permitted and never hides one that is present.

| Action | Consumer-facing label | Actor / authority to display | Must not imply |
| --- | --- | --- | --- |
| A1 WAIT_BOUNDED | Wait within the recorded review or settlement limit | supervising holder; policy wait bound or UNKNOWN | that waiting is approval or that indefinite polling is expected |
| A2 COMMISSION_STAGE | Request an independent stage review | authorised stage commissioner; one active holder per stage | that the view can commission, or that a stage is committed or approved |
| A3 FIX_ONE_BATCHED_BLOCKING_SET | Fix the recorded blocking set once, then re-audit affected stages | implementer; budget/exception check | that a fix commit is proof of repair or approval |
| A4 RECORD_UNAVAILABLE_DISPOSITION | Record a policy-authorised unavailable-review disposition | policy authority, or UNKNOWN which stays blocked | that silence or unavailability is a pass |
| A5 REQUEST_SCOPED_EXCEPTION | Request the scoped head or exception authority | named authority defined by policy; UNKNOWN stays blocked | that a written finding or the request itself grants anything |
| A6 PARK_UNMERGED | Park the candidate unmerged | owner | that parked is accepted, failed or final for all time |
| A7 REBIND_CANDIDATE | Controlled repair or rebind to a new head | authorised rebind authority | that rebinding is silent, free or resets counters |
| A8 AWAIT_OWNER_DECISION | Wait on a named owner decision | the pending decision's authority holder | that an agent, the view or time can decide it |
| A9 AWAIT_G_MERGE_AUTHORITY | Wait for the authorised G merge decision | G role only; readiness valid | that readiness is merge authority or that the view may merge |
| A10 REFRESH_FROM_AUTHORITY | Re-read PR, CI, policy and evidence from authoritative events | any holder (read-only) | that retrying a stale value makes it current |
| A11 NO_ACTION | Nothing is permitted; terminal | none, with reason and responsible authority | blank screen, "done" or "all clear" |

**Forbidden renderings:** "Approve", "Merge", "Waive", "Override", "Clear
blocked", "Accept risk", "Mark reviewed" or "Fix it" controls that execute a
transition; "Contact admin" without an authority; an action derived from a label
or timestamp; multiple actions presented as equally permitted; an action hidden
when present. A request control must state "records a request; does not
approve".

---

## 6. Assurance, UNRUN, bypass and dual-budget display

| ID | Requirement |
| --- | --- |
| A-1 | Every evidence item displays its assurance class and meaning: VERIFIED (re-derived from a primary source), REPORTED (asserted, not recomputed), UNKNOWN (with resolver). No number or status is promoted by the view. |
| A-2 | UNRUN is displayed as UNRUN with its count, ids, expected resolver and owner; it is never counted as PASS, omitted or hidden by a total. FAIL is displayed as FAIL. Counts sum to the frozen denominator. |
| A-3 | Retention and durability class is displayed with consumer meaning: DURABLE, LOCAL_SINGLE_COPY, TRANSIENT or UNKNOWN. No display implies an evidence set is retrievable, publication-classified or independently verified when it is not. |
| A-4 | Local acceptance, hosted and independently verified are separate labels; "LOCAL ACCEPTANCE PASS" is not hosted and not independently verified. Native acceptance REPORTED or UNRUN stays labelled as such. |
| A-5 | CI is explainable: which suite was selected for the change class, which checks are required versus advisory, and their provenance. A missing required check is blocked; required CI is never waived through evidence reuse. |
| A-6 | Bypasses display as "BYPASS RECORDED (not green)" with the owner line and authority, never as approval, pass or waiver; a red-by-design check displays as failed with its authorised disposition. |
| A-7 | The enforcement claim displays as NONE or AUDITABLE_GATE only while custody and coverage are unproved, with mounted coverage UNKNOWN and the named uncovered bypasses. An ENFORCED claim requires the recorded evidence. |
| A-8 | Every value carries as_of and CURRENT/STALE/UNKNOWN; stale or invalidated values are not displayed as current, and readiness built on them is visibly invalidated. |
| A-9 | Conflicts and GAPs are displayed, not averaged; an open NOT MET item is shown as open, never resolved by presentation. |
| A-10 | No aggregate green, score, percentage, health or traffic-light converts any of the above into a pass. Any visual token carries a text label and is not green for a non-affirmative state. |
| A-11 | Display vocabulary is version-pinned: contract schema `aegis.capability-status/v2` (proposed) and bound set `aegis.verdict-bound/v2.1` (design of record). A v2-or-lower verdict record is displayed INVALID, never current. |

**Dual budget.** Display the two counters separately and in this form:

- **Plan-revision count per item:** APR-139(i) limit 4; reopen used true/false;
  stop state. Exhaustion is never acceptance.
- **Review-head count:** exclusive used count (initial 0, second 1, third 2,
  fourth 3); default limit 3; candidate ordinal = used + 1; published-head list;
  exception id/status/authority/scope/expiry; exception required exactly when
  used >= 3; resync and fix heads count; rename, agent and restart do not reset;
  a decrease or an unnecessary exception is INVALID; a fourth head without an
  ACTIVE scoped exception displays LIMIT REVIEW_BUDGET_EXHAUSTED.
- One counter's state never implies anything about the other. Neither counter is
  an assurance class or an approval.

**Gaps carried visibly.** The E0 item-5 set remains PARTIAL with 05-G NOT MET and
no durable-custody claim; E3 item-2 remains 18 PASS / 3 FAIL / 1 UNRUN, not
accepted. Where an E2 view cites either, it cites the record identity and the
limitation; it does not turn the counts into a green total. These are assurance
precedents, not E2 evidence.

---

## 7. Fail-closed, stale and UNKNOWN behavior

1. **Missing contract or record:** display BLOCKED or UNKNOWN with the reason
   code and REFRESH_FROM_AUTHORITY (A10); never a default "ready" or "green".
2. **Stale head, base, policy or evidence:** display STALE/INVALIDATED with the
   stale term and A10; never the last-good green or a silently reused verdict.
3. **Contradictory record:** display BLOCKED with the conflict named; do not
   choose the optimistic reading and do not average the two values.
4. **Unknown value:** display UNKNOWN plus the resolver and owner; do not
   substitute zero, false, "none" or an inferred default.
5. **Invalid or lower-version verdict record:** display INVALID and the version
   rule; never current, never silently accepted.
6. **Authentication:** while T6 is UNVERIFIED and BLOCKED, an "authenticated
   verdict" display reads UNVERIFIED/BLOCKED with its resolver. No UI workaround
   may display it as verified.
7. **No authoritative record at all:** the simplest correct display is
   BLOCKED/UNKNOWN with the missing record named, not a neutral "not yet
   available" state that could read as green.

The view never recovers a stale value by retrying it, by reading a cached copy
as current, or by treating the absence of an error as a pass.

---

## 8. Modes, capabilities, burden and known cost (E2.2)

- **Selected configuration is displayed explicitly, never inferred.** The
  display names the mode and the optional components the consumer selected; it
  does not infer them from identity values, a default, a label, elapsed time or
  the absence of a setting. Invalid, whitespace-padded or missing mode values
  are refused before comparison, with the reason and the valid tokens.
- **Supported v1 configuration.** One measured Windows host, PowerShell 7, Git,
  a POSIX `sh` and one host agent; single agent; no inbox; the 41-file package.
  Subagents, additional providers and the inbox are optional. No Nemesis
  dependency and no source-programme staffing requirement is displayed or
  implied.
- **Capabilities.** Each capability displays available, gated or unavailable,
  with its reason, owning workstream and support limit. The capability fields
  are consumed from the shared contract by reference; this page does not
  re-encode them and adds no second field list.
- **Inbox disabled.** Display exactly "inbox disabled - zero associated
  activity". It is a supported state, not progress, not approval and not an
  implication of hidden activity.
- **Assurance differences.** Local acceptance, hosted and independently verified
  are separate labels. The current package claims local acceptance on one
  measured host only; hosted and independent verification are UNRUN. A missing
  mandatory independent approval displays BLOCKED and is never substituted by a
  CI pass, an advisory review or a view acknowledgement.
- **Setup burden.** The burden is the section 6 checklist and the P0-P9 steps in
  the [consumer starter package](consumer-starter-package.md). macOS and Linux
  remain unvalidated; a second host is UNRUN.
- **Known cost.** The package requires no vendor, subscription, inbox, subagent
  or additional provider. A dollar figure is UNKNOWN, not zero and not invented.
  Agent time and owner attention are costs even when no price is attached.

---

## 9. Version pin and display map `cs-map/1`

`cs-map/1` is the candidate display-map version for this page. It pins the
following display elements so a contract change cannot silently change labels:

| Pinned element | Value at `cs-map/1` |
| --- | --- |
| Contract schema | `aegis.capability-status/v2` (proposed; T2 open) |
| Bound set | `aegis.verdict-bound/v2.1` (design of record) |
| Consumer labels | frozen, awaiting review, budget exhausted, blocked, residual accepted, evidence reused, actual permitted next action |
| Presentation extensions | CS-P0 no active candidate, CS-P1 settlement/final split, CS-P2 suspended, CS-P3 ready for gate, CS-P4 closed/parked |
| Action set | A1-A11 with the section 5 labels |
| Assurance tokens | VERIFIED, REPORTED, UNKNOWN, UNRUN, FAIL, BYPASS RECORDED, NONE/AUDITABLE_GATE, VALID, INVALID, STALE |
| Projection blocks | P1-P9 in the section 2 order |
| Precedence | the section 2 order |
| Fail-closed rules | section 7 |

Rules:

1. `cs-map/1` is a **candidate**. It becomes accepted only with the contract
   acceptance and owner direction; until then it supports review and E4.1
   compatibility checking only. It is not a contract-conformance claim.
2. A change to any pinned element requires a new map identifier (`cs-map/2` or
   later); no silent relabeling or reordering. E4.1 re-checks the affected
   compatibility cells only, against the new map and the contract version.
3. A v2-or-lower bound-set verdict record is INVALID for a v2.1 gate. The view
   displays INVALID, never "current".
4. The map does not encode contract fields. C03 and its errata own them; this
   page cites them by identity.

---

## 10. The view cannot grant authority

Binding rules for every mode, every accessible name, every live-region
announcement, every tooltip and every exported report:

1. **Read-only projection.** The view displays authoritative record values; it
   cannot create, edit, clear, advance, suspend or reopen a state, and cannot
   write a verdict, disposition, exception, approval or merge.
2. **No client-side derivation.** The view does not compute readiness, counts,
   budgets, assurance, approval, enforcement or a verdict.
3. **No optimistic transitions.** A status never advances before the
   authoritative record exists; a failed read reverts with an explicit error,
   never a silent green.
4. **No authority inference.** Approval, repair or enforcement is never inferred
   from a SHA-bearing comment, freeze label, green CI, later fix commit, merge,
   elapsed time, absence of errors or a click.
5. **Attribution.** Every state change names the authoritative record and actor;
   a view event is never authority evidence.
6. **Action labels.** No control may be labelled or read by assistive
   technology as approve, merge, waive, accept-risk or clear-blocked. A request
   control says it records a request and does not approve.
7. **Consumer independence.** The consumer is never shown authority it does not
   hold; missing mandatory independent approval displays BLOCKED; the source
   programme's reviewer identities or staffing are not implied to exist in the
   consumer's environment.
8. **Access.** The same prohibitions apply in every mode, single-agent and
   no-inbox configuration, and in accessible names, live announcements, tooltips
   and exports.

---

## 11. Current state at this revision (2026-11-11)

This section records state; it is not evidence of E2 work and not a verdict.

| Item | State at this revision | Effect on this page |
| --- | --- | --- |
| C1.1a checker/store | MERGED `701ebc7c` (checker and seeded revision-state store only) | consumed by reference; no live status value |
| C2 preflight/policy | MERGED `b90e756c` and policy fix `96b13887` | no effect; cited as merged |
| C1.2-C1.4 change-state producers | MERGED `91ac3f97`; auditable tooling, readiness NOT_COMPUTED, not wired | record formats consumed; no enforcement or live value |
| C1.1b Stage 1/2 | MERGED `27981d22`; Stage 3 BLOCKED on T4/T6/T24/T7; verdict gate NOT WIRED | no authenticated or live verdict display claimed |
| C3/C4 ops package | MERGED `c5fe3adf`; C4 external cells UNRUN | no C4.1 compatibility evidence for E4.1 |
| E1.4/E1.5 evidence | MERGED `544928a5` at their recorded base | cited as historical evidence; no re-run |
| E1.6 integrated verification | UNRUN | E2 closure is not claimed |
| E1.2/E1.3 closure | UNRUN; delivered-not-closed | no E1 closure claim |
| T12/T13 | UNRUN; owner-held | no programme disposition claim |
| Item-8 P3-08-01 | UNRUN | shown honestly where item-8 status appears |
| Item-5 05-G | NOT MET; item-5 PARTIAL; no durable-custody claim | shown honestly if cited |
| T2 design-basis acceptance | OPEN | no contract-conformance claim |
| T6 authentication | UNVERIFIED and BLOCKED | authenticated verdict displays are not claimed |
| T5 mounted coverage / B1 | mounted coverage UNKNOWN; B1 auditable-only | enforcement displays NONE/AUDITABLE_GATE |
| E2.4 independent exercise | UNRUN; request recorded separately | no exercise result is claimed here |
| E3 item-2 | 18 PASS / 3 FAIL / 1 UNRUN, not accepted | assurance precedent only |
| E4.1/E4.2/E4.3 | not this slice; UNRUN | no compatibility or delivery claim |

Merge commits are read from `git log` at base `c5fe3adf`; the closure and UNRUN
state follows the implementation authority (1,815 B / `c96eb16a...`) and the
2026-11-11 implementation-wave status (5,917 B / `dd87b20c...`). No state is
re-derived beyond that base.

**No live status value is displayed or claimed.** The merged pieces are
checker/store tooling and evidence records, not a consumer status service. Until
an authoritative record exists for a work item, the correct display is
BLOCKED/UNKNOWN with the missing record named, not a green or neutral default.

---

## 12. Non-claims and change control

This page is **PROPOSED display requirements**. It does not claim:

- E2.1-E2.4 completion, E1 closure, E3 acceptance or E4 readiness;
- contract conformance or owner acceptance (T2 open);
- enforcement, mounted coverage, authenticated verdicts or merge authority;
- delivery, publication, installation or release;
- a renderer, application, service, dashboard, ledger, policy or second status
  vocabulary;
- any PASS for an UNRUN item, and any aggregate green.

A change to this page follows the E2 docs route: exact-head diff, link and
render checks, independent review, and no self-approval. A change to the
contract, a consumer label, an action, an assurance token or the block order
also requires the C0/T2 path and a new display-map identifier. The current map
is `cs-map/1`; it is not accepted merely because this page exists.
