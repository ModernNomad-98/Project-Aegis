# Canonical semantics - R8 owner work order item 1

Status: canonical, merged before any normative skill-text change (the only SKILL.md edits in R8-A are pointer citations). This file is the single authoritative statement for the canonical IDs below; affected skills and evals cite it and do not restate it. This PR (R8-A) adds this file and pointer citations only; it implements no deferred item and changes no rule text outside the citations.

Source: owner standing work order item 1 (recorded date 2026-10-23, same session date as this PR), base main b231011f; read-only basis evidence: PR-1/PR-2/UX-follow-up merge records, R6 DECISION.md, R6 C7-DEFER record, R6 E6 recurrence evidence, review 5623617542, and the current merged skills.

## 0. Principles (normative; apply to every canonical ID)

P1 Fail-safe: an absent, unrecorded, unparseable or corrupted value selects the restrictive case. It is never treated as permission, never inferred, and never called impossible; the record names the missing/corrupt value and the human remediation path.
P2 Deny-by-default ordering: FORBIDDEN is checked first and is never downgraded. CONFIRM is the default for every non-FORBIDDEN action that does not satisfy the explicit AUTONOMOUS gate. AUTONOMOUS is only the remainder after that gate. 'Apply in order' means first matching class wins; the canonical order is FORBIDDEN -> CONFIRM default -> AUTONOMOUS remainder, where CONFIRM's match condition is 'not FORBIDDEN and not AUTONOMOUS-gated'. A literal unconditional CONFIRM row before an AUTONOMOUS row would make AUTONOMOUS unreachable and is invalid.
P3 One canonical name per quantity or subject. The names in this file are the operative names. Other spellings are deprecated (removal is an implementation-wave edit), not aliased in operative text; this file's mapping and deprecation tables are the only place old names may appear.
P4 Formula terms are explicit: every formula enumerates its included terms; every term named in a formula appears in the section-4 registry and is asserted by at least one named eval case (a formula's full term set may span the named cases; the registry maps each term to at least one asserting case). The term registry in section 4 is normative.
P5 Every claimed check is executable exactly as written: a concrete command or a concrete closure with a stated expected result. A compound exit-status form that cannot be run as written is not a check, and a check without its expected result is not a check.

## 1. Canonical ID map (old aliases -> canonical IDs)

### 1a. UX convergence items (UX CONV-1..8)

| Old ID | Canonical ID | Subject | Status at base b231011f |
|---|---|---|---|
| UX CONV-1 | R8-UX-1 | mockup/pass matrix and direction-conditional mockup count | satisfied by merged #892 (SKILL 1.2) |
| UX CONV-2 | R8-UX-2 | two-question design-entry discipline | satisfied by merged #892 (Workflow step 1) |
| UX CONV-3 | R8-UX-3 | reference schema/readiness/Supporting Files sync | partly satisfied; remaining schema/readiness sync is UX item-3 |
| UX CONV-4 | R8-UX-4 | clickthrough lifecycle and post-implementation record | plain offered/declined/UNRUN satisfied; detailed lifecycle and the post-implementation clickthrough record field are UX item-3 (never part of the pre-implementation selection record) |
| UX CONV-5 | R8-UX-5 | E18 complete pre-design digest case | satisfied by merged #892 (E18 present) |
| UX CONV-6 | R8-UX-6 | guided-premium HARD-vs-residual labels and E25 residual | satisfied by merged #892 (E25 present; residual wording) |
| UX CONV-7 | R8-UX-7 | no-repository-change vs committed-copy sha256/byte-size conflict | satisfied by merged #892 (host-provided binding; skill writes nothing) |
| UX CONV-8 | R8-UX-8 | settled-direction one-mockup vs creative-options 2-4 conflict | satisfied by merged #892 (single SKILL 1.2 rule) |

UX item-3 remaining work (this PR does not implement it): E19 (E4-B6/E5-B1), E30 (reference-restatement issue), and the post-implementation clickthrough record field clickthrough_offer_decision (never part of the pre-implementation selection record). The canonical rules for those items are fixed in R8-UX-3/R8-UX-4 below; only the later skill/eval edits remain.

### 1b. R8 deferred R6 items (R6 CONV-1..5)

| Old ID / source | Canonical ID | Subject |
|---|---|---|
| R6 CONV-1 / R5D-3 / DECISION C / records E4-3, D4-3, D5-1 | R8-CONV-1 | standing grant effective-deadline and state model |
| R6 CONV-2 / R5D-2 / DECISION B / records E2-2, E3-1, D2-2, D5-3 | R8-CONV-2 | latency retry-spend model |
| R6 CONV-3 / R6-C4 / record E4-5 | R8-CONV-3 | memory merge-base exit-status and content-vs-reachability guidance |
| R6 CONV-4 / R5D-1 / DECISION A / records E4-1, E4-2, E4-7 | R8-CONV-4 | HITL class ordering and judgeability |
| R6 CONV-5 | R8-CONV-5 | standing eval/catalog alignment |

### 1c. Review 5623617542 recurrence map and carried advisories

| Review item subject | Canonical ID |
|---|---|
| latency retry-spend/downstream probability weighting and step-6 wording | R8-CONV-2 |
| standing effective-deadline prose/eval/absent-deadline note | R8-CONV-1 and R8-CONV-5 |
| memory executable exit-status and content-vs-reachability | R8-CONV-3 |
| HITL class-ordering/judgeability/bounded multi-record conditions | R8-CONV-4 |

Carried non-AC advisories remain advisory-only and create no operative rule: R8-ADV-1 (R6-C1 database-backup drill; delivered, advisory record only), R8-ADV-2 (R6-C2 secrets role/carve-out; delivered), R8-ADV-3 (R6-C3 background queue-depth evidence; delivered), R8-ADV-4 (R6-C4 memory completion-anchor split; deferred and now folded into R8-CONV-3 scope), R8-ADV-5 (R6-C5 ledger consumer pointer; delivered). No operative text cites an advisory as authority.

### 1d. Term deprecation map (P3)

| Old term | Canonical term / status |
|---|---|
| expected_total_hop_spend | total_expected_hop_cost |
| retry_cost (P(retry)*(backoff_total+own+downstream)) | deleted - no canonical term; the expression is not a term and must not be used |

## 2. UX semantics

### R8-UX-1 mockup/pass matrix
Concepts are non-cosmetic candidate flows; mockups are exercisable artifacts of a chosen concept or direction. Defaults: one to four concepts and one to four mockups, configurable with a recorded reason. At least one concept is required whenever the iteration runs; zero concepts only when iteration is not-applicable/justified N/A with a recorded reason. A recorded reason may reduce within the direction bounds but never permits more than four and never contradicts the direction minima. Four is the hard maximum for concepts and for mockups and is never exceeded. Direction override: 1a guided premium and 1c follow-my-existing-design permit exactly one mockup (one required and permitted, never a second); 1b creative options require at least two mockups, each for a distinct non-cosmetic concept or direction. Cosmetic variants never count as concepts or mockups. Every evaluation pass counts. The SKILL 1.2 text is the merged implementation of this rule; this canonical file is the audit reference.

### R8-UX-2 question discipline
At design entry, ask at most TWO questions in total: the A/B choice and, only when context does not settle it, the direction/mockup choice. Zero questions is valid when context settles both. Never ask a third design-entry question; record remaining decisions as open items or UNKNOWNs for later. The cap excludes the post-implementation clickthrough question and the proof-set question, which are offered only after implementation.

### R8-UX-3 reference schema/readiness/Supporting Files sync
The canonical selection record has five pre-implementation fields: design_direction, mockup_budget, ui_lock, pre_design_binding and authority_conflict. pre_design_binding is always present: not-applicable when 1c is not used; under 1c the binding or a named UNKNOWN(reason) when not bindable. authority_conflict is ONE mapping: not-applicable when no pre-design/1c is in use; none when 1c applies with no conflict; the recorded resolution when 1c conflicts; a named UNKNOWN/open item when unresolved. Its scope is pre-design-vs-in-code authority only, never UI-lock element conflicts. The readiness rules and Supporting Files must cite this file rather than restating these fields; remaining sync edits are UX item-3.

### R8-UX-4 clickthrough lifecycle
Clickthrough is offered after implementation and is never required. Post-implementation status is exactly one of: offered, declined, UNRUN. declined is a recorded user answer (the user explicitly declines at the offer) and is not a run outcome; it carries no defect classes and is never a pass. UNRUN is a run outcome used only when the clickthrough could not be run (an attempted/impossible run), naming the unobservable state-hydration/transition defect classes; readiness may still be declared but the record shows it was not run and the clickthrough is never a pass. A user decline is never converted into UNRUN. The clickthrough_offer_decision field is post-implementation and belongs in the iteration/post-implementation record, never in the pre-implementation selection record (SKILL 1.3; PR-2 B2'). Detailed lifecycle state names beyond this status are UX item-3; the canonical status set and placement are fixed here.

### R8-UX-5 E18 complete pre-design digest
A complete pre-design is bound by file name, version, byte size and full 64-hex sha256; its presence is recorded as a complete binding, not as a pre_design_binding UNKNOWN. Unspecified items remain UNKNOWNs and are never invented. E18 is the asserting case and is present in merged #892.

### R8-UX-6 guided-premium HARD-vs-residual labels
Heuristics that are labels/rules (one primary action per screen, one dominant element per view) are HARD findings. Under UI lock, a heuristic the existing UI cannot meet with its current vocabulary is recorded as a named residual, not forced and not silently dropped. E25 asserts the finding/residual treatment; it is present in merged #892.

### R8-UX-7 no-repository-change vs committed-copy binding
The skill never writes the repository: prototype/mockup/proof writing is delegated to the host/user. An approved mockup is bound by sha256 and byte size when the host provides it; when the host commits the copy, the implementation record compares the committed copy to that binding. 'No repository change' refers to the skill's own actions, not to the host's committed copy; the two statements are not in conflict.

### R8-UX-8 settled direction vs creative options
A settled direction implies one mockup only under 1a/1c. Under 1b, at least two distinct non-cosmetic mockups are still required even when the user believes the direction is settled. There is one rule: R8-UX-1. This resolves the settled-direction/1b conflict; no second mockup-count sentence is permitted.

## 3. R8 core semantics

### R8-CONV-1 standing grants: effective deadline, states, transitions
Definitions (all recorded, never inferred): attestation_deadline (re-attestation due date); review_deadline (scheduled policy-review date); effective_deadline = min(recorded attestation_deadline, recorded review_deadline) when both are recorded, otherwise the sole recorded deadline. recorded_expiry_or_use_limit is nullable: a recorded explicit null means no expiry date (a one-use/consumption limit may still expire it); an absent, unrecorded, unparseable or corrupt value is BLOCKED fail-safe with a named reason and human remediation, never 'no expiry' by inference (P1). recorded_consumption_or_one_use is the recorded consumption state/one-use count; a one-use grant is consumed exactly when its recorded use occurs. grandfathered is the recorded valid-at-adoption flag (recorded for every grant; unrecorded/ambiguous is BLOCKED fail-safe, never inferred). armed is the recorded auto-advance enable flag, defined for every non-EXPIRED state (for GRANDFATHERED it is recorded but does not bypass GRANDFATHERED precedence); a recorded, non-expired, non-blocked, non-grandfathered grant that is not armed is INACTIVE (no auto-advance; a human must arm it). transition trigger = a recorded external event named in the grant record that invalidates the grant (for example a policy-tier or scope change); it is never inferred. If a recorded consumption value is unrecorded/ambiguous for a one-use grant, the grant is BLOCKED with a named fail-safe reason and human remediation, never ACTIVE/GRANDFATHERED by inference. Likewise, unrecorded or ambiguous armed/grandfathered values on a grant that needs them are BLOCKED fail-safe (never inferred true/false).
Fail-safe: if neither deadline is recorded, or a recorded value is unparseable/corrupt, the grant is BLOCKED with a named fail-safe reason and a human remediation path; it is never called impossible and never permitted by inference.
State precedence: first, if recorded_expiry_or_use_limit has passed OR the grant is recorded as consumed/one-use-consumed, the grant is EXPIRED (terminal; no agent or in-scope manual authority; a new grant is required; consumption cannot be reset by re-attestation or a new use). Otherwise BLOCKED > GRANDFATHERED > ACTIVE > INACTIVE, first match wins. ACTIVE requires a future effective_deadline, armed=true, not blocked, not expired, not consumed, and grandfathered=false. GRANDFATHERED requires grandfathered=true recorded, not blocked, future effective_deadline, not expired, not consumed armed may be true or false but is inert for GRANDFATHERED - only ACTIVE auto-advances, GRANDFATHERED never auto-advances and needs recorded clearance plus re-attestation to reach ACTIVE). effective_deadline = min(attestation_deadline, review_deadline): re-attestation records a new attestation_deadline and does not move review_deadline; clearing a passed review_deadline requires a recorded review/clearance action that records a new future review_deadline (re-attestation alone never clears it). INACTIVE is the remaining recorded valid grant with a future effective_deadline, not blocked/expired/consumed, grandfathered=false and armed=false (no auto-advance; the human must record armed=true to reach ACTIVE). BLOCKED applies on a reviewer block, a passed effective_deadline, a transition trigger, recorded consumption is ambiguous/unrecorded for a one-use grant, a recorded expiry is absent/corrupt, or the fail-safe missing/corrupt deadline case.
Transitions (all edges reachable; each requires the recorded fields named): ACTIVE->BLOCKED, GRANDFATHERED->BLOCKED or INACTIVE->BLOCKED on reviewer block, passed effective_deadline, or a recorded transition trigger; BLOCKED->ACTIVE with recorded re-attestation, future effective_deadline, block cleared, recorded_expiry_or_use_limit not passed, armed=true, grandfathered=false, not consumed; BLOCKED->GRANDFATHERED with recorded valid-at-adoption grandfathered=true, block cleared, future effective_deadline, recorded_expiry_or_use_limit not passed, not consumed; GRANDFATHERED->ACTIVE only when the grant record is updated with grandfathered=false (a recorded clearance) plus recorded re-attestation, future effective_deadline, recorded_expiry_or_use_limit not passed, armed=true, not consumed; INACTIVE->ACTIVE with recorded armed=true, future effective_deadline, not blocked/expired/consumed; any non-EXPIRED state->EXPIRED when recorded_expiry_or_use_limit passes or a one-use grant is recorded consumed; EXPIRED has no transition out. Expiry passing and recorded consumption are EXPIRED, never BLOCKED. A passed/absent deadline is never a source condition for ACTIVE/GRANDFATHERED.
Effects: BLOCKED halts every agent-initiated action immediately and waits for the named human; only in-scope human/manual remediation proceeds; GRANDFATHERED never bypasses a reviewer block; the recorded expiry keeps running. No eligible reviewer -> the grant is BLOCKED (one state, not FORBIDDEN by reviewer absence alone) with a named eligible-reviewer/owner escalation and human remediation path recorded; the action never proceeds silently. FORBIDDEN remains only for actions the R8-CONV-4 decision procedure classifies FORBIDDEN.
Canonical names: effective_deadline, attestation_deadline, review_deadline, recorded_expiry_or_use_limit, recorded_consumption_or_one_use, consumed, armed, grandfathered, BLOCKED, GRANDFATHERED, ACTIVE, INACTIVE, EXPIRED. The old attestation-only assertions will be superseded when the implementation wave updates that eval; eval positive-standing-grant-state-precedence must assert effective_deadline and consumed=>EXPIRED, and the fail-safe missing-deadline case must assert BLOCKED with a human path.

### R8-CONV-2 latency retry-spend model
Definitions (all milliseconds unless stated): k=0 is the initial attempt, k=1..R the retries numbered in order of occurrence; wait_k = inter-attempt wait before retry k (that is, before attempt k+1), defined for k=1..R; there is no retry wait before the initial attempt; wait_0 is the separate pre-first-attempt queue/dispatch overhead, counted once and not a retry wait. R=1 worked example: the sole retry is attempt 2, and its wait is wait_1, so upstream_own_expected_cost = wait_0 + (1+p)*own_attempt_work + p*wait_1; no wait for an attempt 3 exists. own_attempt_work = the hop's own processing/serialization work per attempt, excluding queue/dispatch wait; wait_0 = pre-first-attempt queue/dispatch wait owned by the hop, counted once; wait_k = inter-attempt wait before attempt k+1; p in [0,1] = recorded probability that an attempt fails and a retry is attempted; R = recorded retry cap. upstream_timeout = the hop's recorded timeout budget (an input constant used by the cascade checks; not derived from the other terms). downstream_expected_critical_path = SERIAL sum of downstream expected costs plus, at each parallel join, the EXPECTED MAXIMUM over the branches' total expected costs (expected value of the maximum), not the maximum of the branches' means; it includes each downstream hop's retry_overhead and is already probability-weighted.
Formulas (canonical, terms explicit):
upstream_own_expected_cost = wait_0 + SUM(k=0..R) p^k * own_attempt_work + SUM(k=1..R) p^k * wait_k   # wait_k is the wait before retry k (before attempt k+1); R=1 -> wait_1 only
total_expected_hop_cost = upstream_own_expected_cost + SUM(k=0..R) p^k * downstream_expected_critical_path
retry_overhead = total_expected_hop_cost - (wait_0 + own_attempt_work + downstream_expected_critical_path) = SUM(k=1..R) p^k * (own_attempt_work + wait_k + downstream_expected_critical_path)
backoff_total = SUM(k=1..R) wait_k (deterministic schedule sum; never a flat additive expected cost; the weighted term uses SUM(k=1..R) p^k * wait_k)
expected-mode cascade check: upstream_timeout > total_expected_hop_cost + epsilon, where total_expected_hop_cost already includes the probability-weighted downstream critical path, retry work and weighted waits; do not add downstream_expected_critical_path a second time. hard-mode cascade check: upstream_timeout > upstream_own_hard_bound + downstream_hard_bound + epsilon. In both modes epsilon is recorded once and never doubled; no aggregate backoff_total is added as a second term.
Independence: p^k is valid only for independent attempts. For nested/correlated retries record the joint/nested expectation or a conservative bound; never multiply marginal p across nested layers and call it exact. Exactly one retry layer is named.
If p is unknown, use the conservative p=1 bound and say so; if p=1 the weighted wait sum equals backoff_total. Deprecated terms are listed in section 1d. Step-6 wording must use the probability-weighted model: retrying a 50ms hop does not flat-add 50ms plus backoff.
Eval terms asserted (list is NON-EXHAUSTIVE; the normative full registry is section 4, which also includes wait_0_bound, own_attempt_work_hard_bound, branch_hard_bound and retry_allowance_bound): upstream_own_expected_cost, total_expected_hop_cost, retry_overhead, backoff_total, wait_0, wait_k, own_attempt_work, p, R, upstream_timeout, downstream_expected_critical_path, epsilon, upstream_own_hard_bound, downstream_hard_bound, expected_maximum_at_joins, recorded_percentile - see section 4.

Hard-timeout mode (second explicit mode): for every term use a recorded conservative/worst-case bound or a recorded percentile (not the expected mean); parallel joins use the MAX of branch BOUNDS, not an expected maximum; the retry wait uses backoff_total (deterministic schedule sum) and R only; the hard cascade is upstream_timeout > upstream_own_hard_bound + downstream_hard_bound + epsilon, with epsilon recorded once and every term stating its bound/percentile source. Never mix an expected-mean term with a hard bound in the same comparison. If a term has no recorded hard bound/percentile, that mode is UNVERIFIED and cannot pass.
Hard-mode composition formulas (explicit, same term treatment as expected mode): upstream_own_hard_bound = wait_0_bound + (R+1) * own_attempt_work_hard_bound + backoff_total, where wait_0_bound is the recorded hard bound of the pre-first-attempt wait, own_attempt_work_hard_bound is the recorded hard bound of one attempt's own work, and backoff_total is the deterministic schedule wait sum; downstream_hard_bound = SERIAL sum over downstream hops of (branch_hard_bound + retry_allowance_bound) plus, at each parallel join, MAX over that join branches of their SERIAL hard bounds; serial hops ADD (A then B contributes branch_hard_bound_A + branch_hard_bound_B), MAX applies only at parallel joins. Hard cascade (downstream-retry aggregation factor DEFERRED to the R8 wave, E6-B1; no correctness claim here): upstream_timeout > upstream_own_hard_bound + downstream_hard_bound + epsilon; downstream retries for R>0 attempts are not modelled in this formula. Every hard-mode term is a recorded conservative/worst-case bound or percentile, never an expected mean.
Expected-mode rule: expected retry-spend uses p weighting and the EXPECTED MAXIMUM at every parallel join (not MAX of means); hard-timeout mode uses MAX of branch BOUNDS. Both modes name the same term names and record which mode is in use.

### R8-CONV-3 memory merge-base exit status and content proof
Ancestry and content are different questions and need different checks; neither proves the other. The canonical exit-status form is a tested, errexit-safe POSIX script (run at this head):

```
#!/bin/sh
: "${BASE:?BASE required}"
: "${HEAD:?HEAD required}"
if [ -z "${TARGET_PATH:-}" ]; then echo "content_match_status=UNVERIFIED reason=empty_TARGET_PATH"; exit 2; fi
set +e
git merge-base --is-ancestor "$BASE" "$HEAD"; anc_rc=$?
GIT_LITERAL_PATHSPECS=1 git diff --no-textconv --no-ext-diff --quiet "$BASE" "$HEAD" -- "$TARGET_PATH"; content_rc=$?
base_oid=$(git rev-parse --verify --quiet "$BASE:$TARGET_PATH"); base_oid_rc=$?
head_oid=$(git rev-parse --verify --quiet "$HEAD:$TARGET_PATH"); head_oid_rc=$?
set -e
case "$anc_rc" in 0) ancestry_status=ancestor_or_equal ;; 1) ancestry_status=not_ancestor ;; *) ancestry_status=UNVERIFIED ;; esac
case "$content_rc" in 0) content_match_status=same ;; 1) content_match_status=differs ;; *) content_match_status=UNVERIFIED ;; esac
if [ "$base_oid_rc" -eq 0 ] && [ "$head_oid_rc" -eq 0 ]; then
  if [ "$base_oid" = "$head_oid" ]; then oid_match_status=same; else oid_match_status=differs; fi
else oid_match_status=UNVERIFIED; fi
echo "ancestry_status=$ancestry_status ancestry_rc=$anc_rc"
echo "content_match_status=$content_match_status content_rc=$content_rc"
echo "blob_oid base=$base_oid head=$head_oid oid_match_status=$oid_match_status"
if [ "$ancestry_status" = UNVERIFIED ] || [ "$content_match_status" = UNVERIFIED ] || [ "$oid_match_status" = UNVERIFIED ]; then exit 3; fi
exit 0
```

Measured test evidence at this head:

```
TEST1 rc=3
ancestry_status=ancestor_or_equal ancestry_rc=0
content_match_status=differs content_rc=1
blob_oid base= head=cc80c45bf71d953a9f94d44cc9e4d407f190ce21 oid_match_status=UNVERIFIED
TEST2 rc=2
content_match_status=UNVERIFIED reason=empty_TARGET_PATH
TEST3 rc=0
ancestry_status=ancestor_or_equal ancestry_rc=0
content_match_status=differs content_rc=1
blob_oid base=93ccdd7df1d138ddfde5bdbabd2fb9bff53fdef5 head=cb7ef362fe27d5d41c7f06516d0b641c303e60a0 oid_match_status=differs
```

Exit-code contract: 0 = check completed/recorded (NOT passed - a negative outcome such as TEST3 content-differs still exits 0); 2 = empty TARGET_PATH UNVERIFIED (explicit exception); 3 = any other UNVERIFIED status (ancestry/content/blob-OID). Gating-safe interpretation of these exit codes is DEFERRED to the R8 wave (E6-B2); no gating-safe claim is made. TARGET_PATH must be non-empty; an UNVERIFIED status is never a pass; a defined result exits 0 and records both rcs. GIT_LITERAL_PATHSPECS=1 makes the pathspec literal; --no-textconv --no-ext-diff disable textconv/external drivers; the if/then and explicit rc capture are errexit-safe (verified with bash -e above). The blob-OID variant uses git rev-parse --verify on BASE:TARGET_PATH and HEAD:TARGET_PATH and records oid_match_status (same/differs/UNVERIFIED). Reachability is not content proof; the exact SHA is the long-lived binding.

### R8-CONV-4 HITL class ordering and judgeability
Decision procedure (deny-by-default): (1) If the action is inherently FORBIDDEN - no person may perform it, cross-tenant, irreversible or non-compensable, inherently unjudgeable by any eligible person, barred by written policy/risk tier, or an aggregate one eligible reviewer cannot judge - it is FORBIDDEN; never downgraded by approval, reviewer availability or policy silence. An unavailable/ineligible reviewer or missing evidence is recorded as an open escalation under P1 (classification DEFERRED to the R8 implementation wave, E3-B2/E4-B2), never silently downgraded. (2) Otherwise, check the explicit AUTONOMOUS gate: risk tier allows, reversible AND compensable, blast radius one record/user, watch-and-undo controls exist, written policy explicitly permits autonomy, and an eligible reviewer can judge it. If satisfied -> AUTONOMOUS. (3) Otherwise -> CONFIRM, the default for a non-FORBIDDEN action. Policy silence or explicit permission without an autonomy clause keeps CONFIRM; it never makes the action FORBIDDEN and never AUTONOMOUS. Blast-radius boundary: the AUTONOMOUS gate requires exactly one record or one user; a multi-record batch is never AUTONOMOUS. The wide blast radius definition is DEFERRED to the R8 implementation wave (E3-B6/E4-B3); no operative wide-blast rule is stated in this PR.
Judgeability and reviewer eligibility: judgeable = one eligible reviewer can evaluate the evidence and consequence of the exact action without specialist escalation or missing evidence. Eligible reviewer = holds active, unexpired, in-scope authority to perform the action themselves in that tenant, is not the requesting/triggering identity, and is not the AI/service account. If the available reviewer is ineligible, hold at CONFIRM and escalate to a named eligible reviewer/owner. If NO eligible reviewer exists at all, the action is not judgeable by one reviewer: it is recorded as a named eligible-reviewer/owner escalation with a human remediation path (P1); it never proceeds silently and is never a pass. Classification of this case is DEFERRED to the R8 implementation wave (E3-B2/E4-B2); FORBIDDEN remains for actions the decision procedure classifies FORBIDDEN.
Fail-safe: if the undo window or compensation bound is absent/unrecorded, the action is non-reversible/non-compensable and therefore FORBIDDEN until both are recorded.
Bounded multi-record boundary (canonical): a multi-record batch is never AUTONOMOUS. With every action in the batch reversible AND compensable AND judgeable, with written policy explicitly permitting the batch, and with an eligible reviewer able to judge the aggregate, the batch may be approved as CONFIRM (one recorded confirmation for the batch); otherwise it remains CONFIRM only if no action is FORBIDDEN; if any action in it is FORBIDDEN, the batch is FORBIDDEN. A FORBIDDEN condition is never downgraded by this exception.
Canonical names: FORBIDDEN, CONFIRM, AUTONOMOUS, reversible, compensable, judgeable, eligible_reviewer. Risk-tier routing: the recorded risk tier routes through this same order; a tier never skips FORBIDDEN. Eval cases refund-confirm-happy-path, tags-stay-advisory-only, account-deletion-forbidden, self-approval-refused and no-risk-tier-stops assert these classes; the canonical ordering/judgeability assertions must be added at implementation.

### R8-CONV-5 standing eval/catalog alignment
Canonical standing terms are the R8-CONV-1 names. After the standing implementation wave, the standing eval case positive-standing-grant-state-precedence and the policy reference must use effective_deadline (not attestation-only wording), and the fail-safe missing-deadline case must use BLOCKED with a human remediation path and never say impossible. Catalog alignment: after that wave every standing term in docs/skills-catalog.md must use the canonical names; stale-term checks for drift-proof/legal-failure/refresh/environmentMatchGlobs remain clean and are not a substitute for this check. Eval/catalog references are pointers/assertions to this file; no alias is allowed in operative text.

## 4. Formula term registry (R8-CONV-2) and eval assertion mapping

| Term | Meaning | Asserting eval case(s) at implementation |
|---|---|---|
| wait_0 | pre-first-attempt queue/dispatch wait, counted once | latency-budget-architect positive-decompose-journey-target |
| wait_0_bound | recorded hard bound of the pre-first-attempt wait | positive-timeout-folklore-cleanup |
| branch_hard_bound | recorded hard bound of one downstream serial hop | edge-fan-out-tail-math |
| retry_allowance_bound | recorded retry-allowance bound used in hard-mode composition | positive-timeout-folklore-cleanup |
| wait_k | inter-attempt wait before attempt k+1 | edge-fan-out-tail-math |
| own_attempt_work | per-attempt own work excluding wait | positive-timeout-folklore-cleanup |
| p | recorded retry probability | edge-fan-out-tail-math |
| R | recorded retry cap | positive-timeout-folklore-cleanup |
| upstream_own_expected_cost | expected own-hop cost before downstream (wait_0 + probability-weighted own work and wait) | positive-decompose-journey-target |
| upstream_own_hard_bound | hard bound/percentile of the upstream own-hop cost | positive-timeout-folklore-cleanup |
| downstream_hard_bound | serial downstream hard bounds ADD; MAX only at parallel joins | edge-fan-out-tail-math |
| expected_maximum_at_joins | expected maximum at parallel joins (expected mode), not MAX of means | edge-fan-out-tail-math |
| recorded_percentile | percentile used for hard-mode terms | positive-timeout-folklore-cleanup |
| upstream_timeout | recorded hop timeout budget (input constant used by both cascade checks) | edge-fan-out-tail-math |
| own_attempt_work_hard_bound | recorded hard bound of one attempt's own work (hard-mode composition) | positive-timeout-folklore-cleanup |
| total_expected_hop_cost | canonical total cost | positive-decompose-journey-target and edge-fan-out-tail-math |
| retry_overhead | total minus initial own+wait+downstream baseline | positive-timeout-folklore-cleanup |
| backoff_total | deterministic schedule wait sum | edge-fan-out-tail-math |
| downstream_expected_critical_path | probability-weighted downstream critical path incl. downstream retry_overhead | edge-fan-out-tail-math |
| epsilon | recorded one-time safety margin | positive-timeout-folklore-cleanup |

Every term above must appear in at least the named eval assertion when the implementation wave updates that eval. R8-A does not run or claim those eval updates.

## 5. Executable check registry

All commands are run from the repository root. R8-IMPL implementation checks verified: the canonical-file integrity check and the per-line implementation checks below were run at this head with their actual results recorded (hit counts / exit code); every claimed pass is backed by the measured result and every line states its expected result (P5). Every check states its expected result (P5); checks are discriminating: they name terms that are absent from the base rule text and must be present after the owning wave implements. BLOCKED-dependent checks are removed together with the deferred P2/CONV-4 constructs; no BLOCKED claim remains for those deferred constructs. R8-CONV-1 standing-grant states (including its base-consistent BLOCKED rule) are retained unchanged.

Canonical-file integrity (R8-A; falsifiable: required sections/terms present, no placeholder text):
```
python -P -c "from pathlib import Path; t=Path('docs/semantics/canonical-semantics.md').read_text(encoding='utf-8'); required=['## 4. Formula term registry','## 5. Executable check registry','P1 Fail-safe','P5 Every claimed check','upstream_timeout','upstream_own_hard_bound','total_expected_hop_cost','effective_deadline']; ids=['R8-UX-'+str(i) for i in range(1,9)]+['R8-CONV-'+str(i) for i in range(1,6)]; assert all(x in t for x in required+ids) and 'PLACE'+'HOLDER' not in t and 'TO'+'DO' not in t"   # measured at this head: rc=0 (expect 0)
```
Implementation-wave checks (each term has its own line; no combined alternation; every line states its expected result). Classification (measured at this head): canonical-file integrity check PASSES rc0. Implementation-wave checks at this head: measured results are recorded per line; all previously expect-to-fail terms are now present after implementation and the integrity check exits 0. Each deferred subject is implemented once under its canonical ID; the resolved status is recorded in section 6.
```
git grep -n 'recorded_expiry_or_use_limit' -- .claude/skills/standing-approval-and-auto-advance   # measured at this head: 1 hit(s), rc=0 (expect >=1 hit)
git grep -n effective_deadline -- .claude/skills/standing-approval-and-auto-advance   # measured at this head: 7 hit(s), rc=0 (expect >=1 hit)
python -P -c "import json; d=json.load(open('.claude/skills/standing-approval-and-auto-advance/evals/evals.json',encoding='utf-8')); cs=[c for c in d.get('cases',[]) if c.get('id')=='positive-standing-grant-state-precedence']; assert len(cs)==1; a=cs[0].get('expect',{}).get('assertions',[]); assert any('consumed' in s and 'EXPIRED' in s for s in a) and any('effective_deadline' in s for s in a)"   # measured at this head: rc=0 (expect 0)
git grep -n 'wait_k' -- .claude/skills/latency-budget-architect   # measured at this head: 4 hit(s), rc=0 (expect >=1 hit)
git grep -n 'upstream_timeout' -- .claude/skills/latency-budget-architect   # measured at this head: 4 hit(s), rc=0 (expect >=1 hit)
git grep -n 'upstream_own_hard_bound' -- .claude/skills/latency-budget-architect   # measured at this head: 4 hit(s), rc=0 (expect >=1 hit)
git grep -n 'expected_maximum_at_joins' -- .claude/skills/latency-budget-architect   # measured at this head: 2 hit(s), rc=0 (expect >=1 hit)
git grep -n 'retry_overhead' -- .claude/skills/latency-budget-architect   # measured at this head: 3 hit(s), rc=0 (expect >=1 hit)
git grep -n 'downstream_expected_critical_path' -- .claude/skills/latency-budget-architect   # measured at this head: 3 hit(s), rc=0 (expect >=1 hit)
git grep -n 'downstream_hard_bound' -- .claude/skills/latency-budget-architect   # measured at this head: 4 hit(s), rc=0 (expect >=1 hit)
git grep -n 'recorded_percentile' -- .claude/skills/latency-budget-architect   # measured at this head: 2 hit(s), rc=0 (expect >=1 hit)
git grep -n total_expected_hop_cost -- .claude/skills/latency-budget-architect   # measured at this head: 3 hit(s), rc=0 (expect >=1 hit)
git grep -n 'ancestry_status' -- .claude/skills/agent-memory-governance   # measured at this head: 1 hit(s), rc=0 (expect >=1 hit)
git grep -n -- '--no-textconv --no-ext-diff' -- .claude/skills/agent-memory-governance   # measured at this head: 1 hit(s), rc=0 (expect >=1 hit)
git grep -n 'TARGET_PATH' -- .claude/skills/agent-memory-governance   # measured at this head: 1 hit(s), rc=0 (expect >=1 hit)
git grep -n 'judgeable' -- .claude/skills/ai-human-in-the-loop-designer   # measured at this head: 15 hit(s), rc=0 (expect >=1 hit)
git grep -n 'eligible_reviewer' -- .claude/skills/ai-human-in-the-loop-designer   # measured at this head: 2 hit(s), rc=0 (expect >=1 hit)
git grep -n 'effective_deadline' -- docs/skills-catalog.md   # measured at this head: 1 hit(s), rc=0 (expect >=1 hit)
```
Python snippets require Python >= 3.11 for -P and use explicit UTF-8 reading; every case access is defensive (.get) so a missing expect/assertions fails the assertion rather than raising KeyError. Every expected result above is exit 0 or at least one hit. A check that cannot run as written is deprecated, not reworded.

## 6. Citation, ownership and change control
All affected SKILL.md files, evals and the agent-memory-governance reference cite this file as a pointer. Citations scope themselves to the rules covered by the named IDs ("the rules covered by R8-CONV-2 are resolved by this file"), do not claim to resolve unrelated rules in the same file, and from the implementation waves onward do not restate a rule; existing merged rule text is not rewritten by this R8-A PR. Eval top-level canonical_semantics.covers arrays list individual canonical IDs; covers means the file is the authoritative resolution for the named IDs, not that every named ID is already asserted by a case (deferred E19/E30 are covered for resolution, not claimed asserted); the JSON path is repository-root-relative, while SKILL one-line citations are document-relative, and citation lines are wrapped for readability (no Markdown-lint claim is made). The top-level eval key canonical_semantics is an additive extension explicitly authorised by the owner work order item 1 (approved extension) and accepted by the repo validator/contract at this head; external eval-schema additionalProperties behavior is not verified from this repository and is recorded as an owner-approved extension, re-checked by the owner at merge. Audits check operative text against this file. Changes to this file require the owner's recorded instruction; this file is merged before any normative skill-text change and R8 implementation waves implement each canonical ID once at its named canonical location. No advisory row (R8-ADV-*), review item, or old alias is authority in operative text. RESOLVED IN R8 IMPLEMENTATION. R8-IMPL RESOLUTION (replaces the prior deferral section; no remaining R4/R5 deferred rows; no deferred subject ID remains; R8-IMPL implementation checks verified):

- P2-BLOCKED ordering (E3-B2/E4-B1): apply P2 class decision first (FORBIDDEN, then the AUTONOMOUS gate, else CONFIRM). A standing-grant state gate applies after class: EXPIRED and BLOCKED halt every agent-initiated action before any CONFIRM/AUTONOMOUS execution; BLOCKED/EXPIRED never reclassify the action and never downgrade FORBIDDEN. CONFIRM human remediation may proceed only under its own authority; no agent action runs while BLOCKED/EXPIRED.
- reviewer classification (E3-B2/E4-B2): if NO eligible reviewer exists at evaluation time, classify the action FORBIDDEN (not judgeable) because it is not judgeable by one eligible reviewer (P1 restrictive); record the named owner escalation and human remediation. An available but ineligible reviewer leaves the action at CONFIRM pending escalation; never AUTONOMOUS and never silently proceeds. Reviewer availability never moves a FORBIDDEN action down a class.
- wide_blast_radius definition (E3-B6/E4-B3): any action whose potential affected records/users exceeds one, any aggregate or batch selected by one action, any cross-tenant scope, or any blast radius that is unrecorded/unbounded is wide_blast_radius (P1 fail-safe treats unrecorded as wide). A wide action is never AUTONOMOUS. If it is inherently FORBIDDEN (cross-tenant, irreversible, non-compensable, or not judgeable by one eligible reviewer), it is FORBIDDEN. Otherwise a single wide action may be CONFIRM only after the design records an explicit scope reduction to exactly one record/user plus all CONFIRM conditions; if that reduction cannot be recorded, it is FORBIDDEN. Explicit batch exception: a multi-record batch is not AUTONOMOUS but is CONFIRM (not FORBIDDEN for wideness alone) only when all four conditions hold: (1) every action reversible AND compensable AND judgeable; (2) written policy explicitly permits the batch; (3) an eligible reviewer can judge the aggregate; (4) one recorded aggregate confirmation. Any FORBIDDEN action makes the batch FORBIDDEN; failure of any condition is recorded and never downgraded.
- External eval-schema additionalProperties (E3-B8/E4-B4): the canonical_semantics top-level field is an owner-approved additive extension; repo validator and contract audit accept it. The external eval-schema check cannot be run from this repository and is recorded UNRUN, never a pass; no external compatibility claim.
- Hard-mode downstream retry (E6-B1): downstream_hard_bound = downstream_retry_allowance_bound aggregation = serial SUM over downstream hops of branch_hard_bound + retry_allowance_bound, with each parallel join taking MAX of the branch serial hard bounds. Per-hop downstream variables: downstream_own_attempt_work_hard_bound (one downstream re-execution's hard own-work bound) and downstream_backoff_total (recorded downstream retry-wait schedule sum). retry_allowance_bound = R_down * downstream_own_attempt_work_hard_bound + (R_down>0 ? downstream_backoff_total : 0), so R_down=0 => retry_allowance_bound=0 exactly; upstream backoff_total is never charged to a hop with no downstream retry. No deferred qualifier. The hard cascade is upstream_timeout > upstream_own_hard_bound + downstream_hard_bound + epsilon; every term states its bound/percentile source (recorded_percentile) and mixing expected and hard terms in one comparison is invalid. expected_maximum_at_joins is the expected-mode join term.
- Gating-safe exit (E6-B2): CONV-3 exit 0 means the check completed with a defined result, NOT passed; a gate may pass only when ancestry_status=ancestor_or_equal AND content_match_status=same AND oid_match_status=same. Exit 2 (empty TARGET_PATH) and exit 3 (other UNVERIFIED) block the gate; any differs/UNVERIFIED status blocks; a gate must never infer pass from exit 0 alone.
- bounded multi-record rule (E6-B4): a multi-record batch is CONFIRM only, never AUTONOMOUS. Four conditions: (1) every action reversible AND compensable AND judgeable; (2) written policy explicitly permits the batch; (3) an eligible reviewer can judge the aggregate; (4) one recorded aggregate confirmation is required. If any condition fails the batch is not approved; if any action is FORBIDDEN the whole batch is FORBIDDEN. Failure of any condition is recorded and never downgraded.
- No deferred-subject ID remains. R8-CONV-1..5 and review 5623617542 items are implemented once under their canonical IDs; R8-ADV-1..5 stay advisory-only and create no operative rule. No remaining R4/R5 deferred rows were found beyond the R6/R8-A inventory; if a later record names one, it is a scope change, not a silent implementation.
