# Consumer status and assurance presentation - v1 (PROPOSED; docs-only)

**Status:** PROPOSED documentation, 2026-11-11. This is not a contract, a contract-conformance claim, an acceptance, a delivery, an implementation or a plan revision. It is display-only consumer guidance: no renderer, application, service, dashboard or status feed is created. The contract basis (T2) is open; authenticated verdicts are UNVERIFIED/BLOCKED until T6; mounted coverage (T5) is UNKNOWN; no enforcement claim is made.

**Authority and ownership.** The proposal sits under the owner Fast Lane B authority recorded for docs-only E2/E4 work (E2-E4-IMPLEMENTATION-AUTHORITY-2026-11-11) and the owner autonomy decision of 2026-11-11 (docs-only status/claims, WCAG 2.2 AA accessibility target, no publication/delivery claim until T9, consumer audience, display-only request records). C&C/C0 own the contract, policy, authority and evidence semantics; Experience presents them. The UI cannot grant authority. Nothing here is an approval or a closure.

**Reading key:** a **state** is what the authoritative record currently says; an **assurance class** says how strongly it is known; a **permitted next action** is the one action the record authorises for the consumer; **UNRUN** means not executed and is never a pass.

## 1. What this document covers

- The six consumer-facing governance states from the plan (frozen, awaiting review, budget exhausted, blocked, residual accepted, evidence reused) and the actual permitted next action.
- The assurance and evidence labels a consumer sees: VERIFIED, REPORTED, UNKNOWN, UNRUN, FAIL, bypass-recorded, and the local / hosted / independently-verified distinction.
- The two separate budgets (plan revisions and review heads) and the correct reading of each.
- The fixed rules that keep a display from granting authority, optimism or approval.

It does not define policy, authority or evidence semantics, and it does not promise that a live status value exists today.

## 2. Current programme state referenced by this proposal (2026-11-11)

The following is the state this document was written against. It is a point-in-time record; re-measure before relying on it.

- Merged / delivered on the reviewed lineage: C1.1a (verdict-gate checker and seeded revision-state store), C2 (governance/evidence reuse), C1.2-C1.4 (freeze/snapshot/stage and qualification work), C1.1b (required-context design work, staged), C3 (overhead controls), C4 (qualification/economics work), E1.4 and E1.5 (current-head containment and transition evidence).
- Open / UNRUN: E1.6 integrated independent verification; historical Stage-B gaps on E1 items 3/4/8 (T12); programme closure of E1 items 3/4 (T13); item-5 05-G source link (05-D/05-G not met); item-8 acceptance row P3-08-01 hosted proof; C4 external cells; and the contract design basis T2.
- Never inferred from merge status: a merged control has no consumer status view by itself, and a merged PR is not an approval, acceptance or enforcement. T5 mounted coverage is UNKNOWN, T6 authenticated verdicts are UNVERIFIED/BLOCKED, and the relevant owner decisions (T7 exception authority, T8/T8a-c/T21 item-5, T14 item-8, T15-T20 item-2) remain open unless separately recorded.

## 3. Modes, capabilities, optional components, burden and costs

The consumer must be able to see, for the chosen configuration, what is actually supported and what it will cost in effort and attention. The display follows the shared definitions; it does not invent a capability, a support claim or a number.

- **Supported modes are explicit, never inferred.** Mode A is one agent without subagents; Mode B is one platform with subagents; Mode C is multiple platforms. The selected configuration is displayed after setup and must equal the recorded value; an invalid, empty or padded mode statement is refused with a reason (the starter package's P2 gate remains the install-side source of truth).
- **Capabilities are shown with their actual state and reason.** Each capability is available, gated or unavailable, with the owning workstream and its support limit; no capability is implied by a repository file existing. Optional subagents, additional providers and the inbox are marked optional and must never be a prerequisite for the simplest configuration. No Nemesis dependency and no mandatory source-programme staffing is implied.
- **Inbox disabled means zero associated activity.** A disabled inbox shows no polling, handshake or external reporting, and the disabled state is visible. Enabling it is a consumer choice with its own prerequisites, costs and assurance limits.
- **Setup burden is stated as a checklist, not a promise.** Prerequisites and their MET/UNMET/UNRUN states come from the consumer page (section 6 there); a prerequisite that was not observed is UNRUN with the remaining action, never a pass. Agent time and owner attention are real costs even when no billing data exists.
- **Known costs are shown with their source; unknown costs stay UNKNOWN.** This proposal claims no dollar or elapsed-time figure. Where a cost is known it is cited; where it is not, the display says UNKNOWN or REPORTED and names what would resolve it. No mandatory subscription, vendor or hosted service is implied for the simplest supported configuration, and additional dependency requirements are explained only where they apply to the chosen configuration.

## 4. The six consumer states and the permitted next action

Every state has the same four obligations: **show** the state and its cause; **show one actual permitted next action** with actor, authority, precondition and record reference (or none, with the responsible authority); **never imply** something the record does not say; and **fail closed** to UNKNOWN/STALE when the record is missing, stale or unreadable. The state is a projection of the authoritative record, not a client-side calculation.

| State | What it means for the consumer | Must show | Must never imply | Typical permitted next action |
| --- | --- | --- | --- | --- |
| **frozen** | A candidate is pinned at an exact head while independent review and validation run. | Candidate identity (item, exact 40-character head, tree/base, snapshot identity), freeze time, which evidence is bound to that head. | Approval, merge readiness, a verdict, enforcement, or that later findings cannot appear. | Wait for the bound stages; do not move the head; a blocker still suspends readiness. |
| **awaiting review** | A required independent stage/reviewer act is outstanding. | Which stage/role is outstanding, request time, the applicable bounded-wait policy, current evidence state, and whether the reviewer is independent. | A pass in progress, an automatic advance, or that indefinite polling is expected. | Wait within the applicable bounded policy, or replace a failed/incomplete reviewer explicitly under authority. |
| **budget exhausted** | The published review-head budget (default 3 candidate heads per change) has been used. | The head count and lineage across agents/renames/restarts, the applicable cap, and any recorded scoped exception with its authority and duration. | That defective work is accepted, that a fourth head is allowed, or that a restart/rename resets the count. | Stop the next candidate cycle until a valid scoped exception exists; a written finding is not authority by itself. |
| **blocked** | A mandatory acceptance, authorization, security, evidence-integrity or required-validation condition is unmet (including a missing mandatory independent approval). | The specific unmet condition and the authority who can resolve it. | That the work failed, that time or a UI action clears it, or that CI/advisory UI acknowledgment substitutes for approval. | Obtain the named missing evidence or authority; remain blocked meanwhile. |
| **residual accepted** | A finding was independently dispositioned as an accepted residual; the head did not move. | Finding identity, candidate/head, requirement or threat boundary, supporting evidence, classification, authorized decision-maker, outcome and rationale. | That the finding was fixed, that a mandatory defect is waived, that aggregate assurance is green, or that readiness is implied. | Proceed only where all blocking gates independent of that finding are satisfied; a residual acceptance is not a pass. |
| **evidence reused** | Prior valid evidence is reused for a target head only through an independently checked applicability record. | Original evidence identity (head, scope, method, environment, result) and the new applicability record: source and target 40-character heads, affected inputs, comparison method, excluded claims, target-head delta checks, and required CI retained. | That an old PASS was copied to a new head, that AST equality alone proves equivalence, that mandatory CI was waived, or that reuse equals approval. | Run the recorded narrow delta audit; rerun affected checks not covered by the reuse record. |
| **actual permitted next action** | The single action the authoritative record authorises now. | Actor/authority, precondition, one bounded step and the record reference that permits it. | A generic recommendation, an inferred authority, or any authority the consumer does not hold. | Perform that action only; if it is unavailable, display BLOCKED with the reason. |

**Extension labels (derived presentations, not new guarantees):** no-candidate, suspended, ready-for-gate and closed/parked are presentation labels derived from the record; stale, invalidated, unknown, bypass-recorded and audit-only are overlays. They do not add acceptance, enforcement or a new contract term.

## 5. Assurance, evidence and UNRUN

- **Assurance classes are shown with their meaning:** VERIFIED (re-derived from a primary source), REPORTED (asserted by a record not re-executed), UNKNOWN (not derivable; a resolver is named), UNRUN (not executed; named remaining action), FAIL (recorded failure). A class is never silently upgraded.
- **Local, hosted and independently verified are distinct.** A local acceptance pass is not a hosted run and is not an independent verification. One host's evidence is bounded to that host.
- **No aggregate green.** Named UNRUNs, frozen denominators and counts must be visible where a claim depends on them; the CP-01..CP-22 consumer-proof ledger currently records 18 PASS / 3 FAIL / 1 UNRUN out of 22 and is not accepted, and the item-5 evidence remains not independently retrievable (05-D) and not source-linked (05-G).
- **Bypasses are shown as bypasses.** An administrator bypass or a red required check is never displayed as green or approval; it is recorded with its authority and disposition.
- **Enforcement is not claimed.** Current enforcement status is AUDITABLE, not ENFORCED: mounted coverage is UNKNOWN and custody preconditions are not met. A display may not imply otherwise.

## 6. The two budgets

- **Plan revisions (APR-139(i), per item):** a plan revision count at or above 4 stops planning on that item; one counted lean reopen is available per item; no reopen resets the count and no second reopen is allowed. WAITING-ON-OWNER / park-unmerged is the limit state.
- **Review heads (per change, default 3):** the published candidate-head count is tracked including resyncs/fix heads across agents and renames; a fourth head requires the applicable scoped exception, and budget exhaustion never converts a mandatory finding into acceptance.
- The two counters are displayed separately and never converted into each other, into assurance, or into an approval. The review-head exception/unavailable-review authority is currently UNKNOWN and displays as such.

## 7. Rules that keep the display honest

1. **Read-only projection.** Every displayed state names its authoritative record and as_of/freshness; missing, stale or contradictory data shows UNKNOWN/STALE/INVALID with a resolver, never a last-known green.
2. **One permitted action.** Exactly one action with actor/authority/precondition/reference, or none with reason and responsible authority. No invented option lists.
3. **The UI cannot grant authority.** The display cannot create/clear/advance/suspend/reopen a state, approve, merge, waive, accept risk or clear a block, and it does not derive authority from a label, SHA, CI result, fix commit, timestamp or merge.
4. **No optimistic transitions.** A state changes only when the authoritative record changes, and the change names its record reference.
5. **No delivery or conformance claim.** This is documentation; no publication, delivery, install, release or enforcement authority is implied, and no contract conformance is claimed before T2.
6. **Display-only request records (owner decision 2026-11-11).** This version does not create durable request records; consumers are shown what is permitted, not given an approval control.

## 8. Accessibility and audience

- **Accessibility target:** WCAG 2.2 AA (owner-selected default for E2/E4 docs-only work). States are conveyed by visible text, never colour or icon alone; badges/state labels have accessible names and descriptions; state changes use an appropriate live region; keyboard and screen-reader use is supported; every code has a plain-English gloss.
- **Audience:** consumer-facing documentation, public where the source documentation is public, with metadata minimisation: no plan-forbidden product names, PR numbers or personal names in public metadata. Publication is not claimed or performed by this document.

## 9. Non-claims and next steps

- No live governance status value is claimed to exist or to be verified by this document. The merged controls provide records and checks, not a consumer status view.
- T2 remains open: this is requirements-level presentation, not contract-conformance evidence. T5 mounted coverage is UNKNOWN; T6 authenticated verdicts are UNVERIFIED/BLOCKED; T7 exception/unavailable-review authority is UNKNOWN; item-5 05-G, item-8 P3-08-01, E1.6/T12/T13 and C4 external cells remain open/UNRUN.
- **Next:** independent E2.4 exercise against the implemented documentation surfaces, then Stage D/E/F review under the programme route. A separate reviewer - not the author - must disposition this document and the E2.4 exercise; a REVISE grants nothing.

Proposed by e0-requirements-envoy (DeepSeek Harness; route deepseek-flash; serving model not observable), 2026-11-11. Docs-only proposal; no code, publication, delivery, settings, host or approval action.
