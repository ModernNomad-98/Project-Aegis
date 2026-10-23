# Canonical semantics - R8 owner work order item 1

Status: canonical, merged before any R8 skill-text change. This file is the single authoritative statement for the canonical IDs below; affected skills and evals cite it and do not restate it. This PR (R8-A) adds this file and pointer citations only; it implements no deferred item and changes no rule text outside the citations.

Source: owner standing work order item 1 (2026-10-23), base main b231011f; read-only basis evidence: PR-1/PR-2/UX-follow-up merge records, R6 DECISION.md, R6 C7-DEFER record, R6 E6 recurrence evidence, review 5623617542, and the current merged skills.

## 0. Principles (normative; apply to every canonical ID)

P1 Fail-safe: an absent, unrecorded, unparseable or corrupted value selects the restrictive case. It is never treated as permission, never inferred, and never called impossible; the record names the missing/corrupt value and the human remediation path.
P2 Deny-by-default ordering: FORBIDDEN is checked first and is never downgraded. CONFIRM is the default for every non-FORBIDDEN action that does not satisfy the explicit AUTONOMOUS gate. AUTONOMOUS is only the remainder after that gate. 'Apply in order' means first matching class wins; the canonical order is FORBIDDEN -> CONFIRM default -> AUTONOMOUS remainder, where CONFIRM's match condition is 'not FORBIDDEN and not AUTONOMOUS-gated'. A literal unconditional CONFIRM row before an AUTONOMOUS row would make AUTONOMOUS unreachable and is invalid.
P3 One canonical name per quantity or subject. The names in this file are the operative names. Other spellings are deleted, not aliased in operative text; this file's mapping and deprecation tables are the only place old names may appear.
P4 Formula terms are explicit: every formula enumerates its included terms, and every term named in a formula appears in the eval assertion that asserts it. The term registry in section 4 is normative.
P5 Every claimed check is executable exactly as written: a concrete command or a concrete closure with a stated expected result. A compound exit-status form that cannot be run as written is not a check, and a check without its expected result is not a check.

## 1. Canonical ID map (old aliases -> canonical IDs)

### 1a. UX convergence items (UX CONV-1..8)

| Old ID | Canonical ID | Subject | Status at base b231011f |
|---|---|---|---|
| UX CONV-1 | R8-UX-1 | mockup/pass matrix and direction-conditional mockup count | satisfied by merged #892 (SKILL 1.2) |
| UX CONV-2 | R8-UX-2 | two-question design-entry discipline | satisfied by merged #892 (Workflow step 1) |
| UX CONV-3 | R8-UX-3 | reference schema/readiness/Supporting Files sync | partly satisfied; remaining schema/readiness sync is UX item-3 |
| UX CONV-4 | R8-UX-4 | clickthrough lifecycle and post-implementation record | plain offered/declined/UNRUN status satisfied; detailed lifecycle + sixth selection-record field is UX item-3 |
| UX CONV-5 | R8-UX-5 | E18 complete pre-design digest case | satisfied by merged #892 (E18 present) |
| UX CONV-6 | R8-UX-6 | guided-premium HARD-vs-residual labels and E25 residual | satisfied by merged #892 (E25 present; residual wording) |
| UX CONV-7 | R8-UX-7 | no-repository-change vs committed-copy sha256/byte-size conflict | satisfied by merged #892 (host-provided binding; skill writes nothing) |
| UX CONV-8 | R8-UX-8 | settled-direction one-mockup vs creative-options 2-4 conflict | satisfied by merged #892 (single SKILL 1.2 rule) |

UX item-3 remaining work (this PR does not implement it): E19 (E4-B6/E5-B1), E30 (reference-restatement issue), and the sixth selection-record field clickthrough_offer_decision with post-implementation placement. The canonical rules for those items are fixed in R8-UX-3/R8-UX-4 below; only the later skill/eval edits remain.

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

## 2. UX semantics

### R8-UX-1 mockup/pass matrix
Concepts are non-cosmetic candidate flows; mockups are exercisable artifacts of a chosen concept or direction. Defaults: one to four concepts and one to four mockups, configurable with a recorded reason. At least one concept is required whenever the iteration runs; zero concepts only when iteration is not-applicable/justified N/A with a recorded reason. A recorded reason may reduce within the direction bounds but never permits more than four and never contradicts the direction minima. Four is the hard maximum for concepts and for mockups and is never exceeded. Direction override: 1a guided premium and 1c follow-my-existing-design permit exactly one mockup (one required and permitted, never a second); 1b creative options require at least two mockups, each for a distinct non-cosmetic concept or direction. Cosmetic variants never count as concepts or mockups. Every evaluation pass counts. The SKILL 1.2 text is the merged implementation of this rule; this canonical file is the audit reference.

### R8-UX-2 question discipline
At design entry, ask at most TWO questions in total: the A/B choice and, only when context does not settle it, the direction/mockup choice. Zero questions is valid when context settles both. Never ask a third design-entry question; record remaining decisions as open items or UNKNOWNs for later. The cap excludes the post-implementation clickthrough question and the proof-set question, which are offered only after implementation.

### R8-UX-3 reference schema/readiness/Supporting Files sync
The canonical selection record has five pre-implementation fields: design_direction, mockup_budget, ui_lock, pre_design_binding and authority_conflict. pre_design_binding is always present: not-applicable when 1c is not used; under 1c the binding or a named UNKNOWN(reason) when not bindable. authority_conflict is ONE mapping: not-applicable when no pre-design/1c is in use; none when 1c applies with no conflict; the recorded resolution when 1c conflicts; a named UNKNOWN/open item when unresolved. Its scope is pre-design-vs-in-code authority only, never UI-lock element conflicts. The readiness rules and Supporting Files must cite this file rather than restating these fields; remaining sync edits are UX item-3.

### R8-UX-4 clickthrough lifecycle
Clickthrough is offered after implementation and is never required. Post-implementation status is exactly one of: offered, declined, UNRUN. A decline or impossible run is recorded as UNRUN naming the unobservable state-hydration/transition defect classes; readiness may still be declared but the record shows it was not run and the clickthrough is never a pass. The clickthrough_offer_decision field is post-implementation and belongs in the iteration/post-implementation record, never in the pre-implementation selection record (SKILL 1.3; PR-2 B2'). Detailed lifecycle state names beyond this status are UX item-3; the canonical status set and placement are fixed here.

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
Definitions (all recorded, never inferred): attestation_deadline (re-attestation due date); review_deadline (scheduled policy-review date); effective_deadline = min(recorded attestation_deadline, recorded review_deadline) when both are recorded, otherwise the sole recorded deadline. recorded_expiry_or_use_limit is nullable: a recorded explicit null means no expiry date (a one-use/consumption limit may still expire it); an absent, unrecorded, unparseable or corrupt value is BLOCKED fail-safe with a named reason and human remediation, never 'no expiry' by inference (P1). recorded_consumption_or_one_use is the recorded consumption state/one-use count; a one-use grant is consumed exactly when its recorded use occurs. grandfathered is the recorded valid-at-adoption flag. armed is the recorded auto-advance enable flag; a recorded, non-expired, non-blocked, non-grandfathered grant that is not armed is INACTIVE (no auto-advance; a human must arm it). If a recorded consumption value is unrecorded/ambiguous for a one-use grant, the grant is BLOCKED with a named fail-safe reason and human remediation, never ACTIVE/GRANDFATHERED by inference.
Fail-safe: if neither deadline is recorded, or a recorded value is unparseable/corrupt, the grant is BLOCKED with a named fail-safe reason and a human remediation path; it is never called impossible and never permitted by inference.
State precedence: first, if recorded_expiry_or_use_limit has passed OR the grant is recorded as consumed/one-use-consumed, the grant is EXPIRED (terminal; no agent or in-scope manual authority; a new grant is required; consumption cannot be reset by re-attestation or a new use). Otherwise BLOCKED > GRANDFATHERED > ACTIVE > INACTIVE, first match wins. ACTIVE requires a future effective_deadline, armed, not blocked, not expired, not consumed. GRANDFATHERED requires valid-at-adoption, recorded, not blocked, future effective_deadline, not expired, not consumed. INACTIVE is the remaining recorded valid grant with a future effective_deadline, not blocked/expired/consumed/grandfathered and armed=false (no auto-advance; the human must record armed=true to reach ACTIVE). BLOCKED applies on a reviewer block, a passed effective_deadline, a transition trigger, recorded consumption is ambiguous/unrecorded for a one-use grant, a recorded expiry is absent/corrupt, or the fail-safe missing/corrupt deadline case.
Transitions: ACTIVE->BLOCKED or GRANDFATHERED->BLOCKED on reviewer block, passed effective_deadline, or trigger; BLOCKED->ACTIVE only with recorded re-attestation, future effective_deadline, block cleared, recorded_expiry_or_use_limit not passed, armed=true, and not consumed; BLOCKED->GRANDFATHERED only with valid-at-adoption, recorded grandfathered, block cleared, future effective_deadline, recorded_expiry_or_use_limit not passed, and not consumed; GRANDFATHERED->ACTIVE on recorded re-attestation with future effective_deadline, recorded_expiry_or_use_limit not passed, armed=true, and not consumed; any non-EXPIRED state->EXPIRED when recorded_expiry passes or a one-use grant is recorded consumed; EXPIRED has no transition out. Expiry passing and recorded consumption are EXPIRED, never BLOCKED. A passed/absent deadline is never a source condition for ACTIVE/GRANDFATHERED.
Effects: BLOCKED halts every agent-initiated action immediately and waits for the named human; only in-scope human/manual remediation proceeds; GRANDFATHERED never bypasses a reviewer block; the recorded expiry keeps running. No eligible reviewer -> the action is not judgeable and the grant stays BLOCKED/FORBIDDEN per R8-CONV-4 semantics; the human remediation path is named and recorded.
Canonical names: effective_deadline, attestation_deadline, review_deadline, recorded_expiry_or_use_limit, recorded_consumption_or_one_use, consumed, armed, grandfathered, BLOCKED, GRANDFATHERED, ACTIVE, INACTIVE, EXPIRED. The old attestation-only assertions are superseded; eval positive-standing-grant-state-precedence must assert effective_deadline and consumed=>EXPIRED, and the fail-safe missing-deadline case must assert BLOCKED with a human path.

### R8-CONV-2 latency retry-spend model
Definitions (all milliseconds unless stated): k=0 is the initial attempt, k=1..R the retries numbered in order of occurrence; wait_k = inter-attempt wait before retry k (that is, before attempt k+1), defined for k=1..R; there is no wait before the initial attempt. R=1 worked example: the sole retry is attempt 2, and its wait is wait_1, so upstream_own_expected_cost = wait_0 + (1+p)*own_attempt_work + p*wait_1; no wait for an attempt 3 exists. own_attempt_work = the hop's own processing/serialization work per attempt, excluding queue/dispatch wait; wait_0 = pre-first-attempt queue/dispatch wait owned by the hop, counted once; wait_k = inter-attempt wait before attempt k+1; p in [0,1] = recorded probability that an attempt fails and a retry is attempted; R = recorded retry cap. upstream_timeout = the hop's recorded timeout budget (an input constant used by the cascade checks; not derived from the other terms). downstream_expected_critical_path = SERIAL sum of downstream expected costs plus, at each parallel join, the EXPECTED MAXIMUM over the branches' total expected costs (expected value of the maximum), not the maximum of the branches' means; it includes each downstream hop's retry_overhead and is already probability-weighted.
Formulas (canonical, terms explicit):
upstream_own_expected_cost = wait_0 + SUM(k=0..R) p^k * own_attempt_work + SUM(k=1..R) p^k * wait_k   # wait_k is the wait before retry k (before attempt k+1); R=1 -> wait_1 only
total_expected_hop_cost = upstream_own_expected_cost + SUM(k=0..R) p^k * downstream_expected_critical_path
retry_overhead = total_expected_hop_cost - (wait_0 + own_attempt_work + downstream_expected_critical_path) = SUM(k=1..R) p^k * (own_attempt_work + wait_k + downstream_expected_critical_path)
backoff_total = SUM(k=1..R) wait_k (deterministic schedule sum; never a flat additive expected cost; the weighted term uses SUM(k=1..R) p^k * wait_k)
expected-mode cascade check: upstream_timeout > total_expected_hop_cost + epsilon, where total_expected_hop_cost already includes the probability-weighted downstream critical path, retry work and weighted waits; do not add downstream_expected_critical_path a second time. hard-mode cascade check: upstream_timeout > upstream_own_hard_bound + downstream_hard_bound + epsilon. In both modes epsilon is recorded once and never doubled; no aggregate backoff_total is added as a second term.
Independence: p^k is valid only for independent attempts. For nested/correlated retries record the joint/nested expectation or a conservative bound; never multiply marginal p across nested layers and call it exact. Exactly one retry layer is named.
If p is unknown, use the conservative p=1 bound and say so; if p=1 the weighted wait sum equals backoff_total. Deprecated names: expected_total_hop_spend -> total_expected_hop_cost; retry_cost = P(retry)*(backoff_total+own+downstream) -> deleted. Step-6 wording must use the probability-weighted model: retrying a 50ms hop does not flat-add 50ms plus backoff.
Eval terms asserted: upstream_own_expected_cost, total_expected_hop_cost, retry_overhead, backoff_total, wait_0, wait_k, own_attempt_work, p, R, upstream_timeout, downstream_expected_critical_path, epsilon, upstream_own_hard_bound, downstream_hard_bound, expected_maximum_at_joins, recorded_percentile - see section 4.

Hard-timeout mode (second explicit mode): for every term use a recorded conservative/worst-case bound or a recorded percentile (not the expected mean); parallel joins use the MAX of branch BOUNDS, not an expected maximum; the retry wait uses backoff_total (deterministic schedule sum) and R only; the hard cascade is upstream_timeout > upstream_own_hard_bound + downstream_hard_bound + epsilon, with epsilon recorded once and every term stating its bound/percentile source. Never mix an expected-mean term with a hard bound in the same comparison. If a term has no recorded hard bound/percentile, that mode is UNVERIFIED and cannot pass.
Expected-mode rule: expected retry-spend uses p weighting and the EXPECTED MAXIMUM at every parallel join (not MAX of means); hard-timeout mode uses MAX of branch BOUNDS. Both modes name the same term names and record which mode is in use.

### R8-CONV-3 memory merge-base exit status and content proof
Ancestry and content are different questions and need different checks; neither proves the other. The canonical exit-status form is:
```
git merge-base --is-ancestor "$BASE" "$HEAD"
rc=$?
case "$rc" in
  0) ancestry_status=ancestor_or_equal ;;
  1) ancestry_status=not_ancestor ;;
  *) ancestry_status=UNVERIFIED ;;
esac
git -c diff.noprefix=false diff --no-textconv --no-ext-diff --quiet "$BASE" "$HEAD" -- "$PATH"
content_rc=$?   # expected: rc=0 same, rc=1 differs, rc>=2 UNVERIFIED (textconv/external drivers disabled)
case "$content_rc" in
  0) content_match_status=same ;;
  1) content_match_status=differs ;;
  *) content_match_status=UNVERIFIED ;;
esac
```
Record the command, rc and status; rc>=2 is UNVERIFIED, never no. An if/then form that maps command errors to no is not executable as written and is deleted. Reachability (ancestry) is not content proof; content identity requires the separate content check or blob equality (git rev-parse "$BASE:$PATH" vs git rev-parse "$HEAD:$PATH"; expected: equal OIDs=same, different=differs, command error/absent path=UNVERIFIED) and the exact SHA. The content check runs with --no-textconv --no-ext-diff so textconv/external diff drivers cannot turn a differing blob into a clean diff. Item (b) of the memory guidance is split into these two checks.

### R8-CONV-4 HITL class ordering and judgeability
Decision procedure (deny-by-default): (1) If the action is FORBIDDEN - no person may perform it, cross-tenant, irreversible or non-compensable, wide blast radius, not judgeable by one eligible reviewer, or barred by written policy/risk tier - it is FORBIDDEN; never downgraded by approval, reviewer availability or policy silence. (2) Otherwise, check the explicit AUTONOMOUS gate: risk tier allows, reversible AND compensable, blast radius one record/user, watch-and-undo controls exist, written policy explicitly permits autonomy, and an eligible reviewer can judge it. If satisfied -> AUTONOMOUS. (3) Otherwise -> CONFIRM, the default for a non-FORBIDDEN action. Policy silence or explicit permission without an autonomy clause keeps CONFIRM; it never makes the action FORBIDDEN and never AUTONOMOUS. CONFIRM is limited to single-record/one-user blast radius.
Judgeability and reviewer eligibility: judgeable = one eligible reviewer can evaluate the evidence and consequence of the exact action without specialist escalation or missing evidence. Eligible reviewer = holds active, unexpired, in-scope authority to perform the action themselves in that tenant, is not the requesting/triggering identity, and is not the AI/service account. If the available reviewer is ineligible, hold at CONFIRM and escalate to a named eligible reviewer/owner. If NO eligible reviewer exists at all, the action is not judgeable by one reviewer and is FORBIDDEN; record the boundary and never proceed silently.
Fail-safe: if the undo window or compensation bound is absent/unrecorded, the action is non-reversible/non-compensable and therefore FORBIDDEN until both are recorded.
Bounded multi-record exception (canonical): a multi-record batch is not AUTONOMOUS unless every action in it is reversible AND compensable AND judgeable, written policy explicitly permits the batch, and an eligible reviewer can judge the aggregate. Otherwise the batch defaults to CONFIRM (or FORBIDDEN if any action cannot meet those conditions).
Canonical names: FORBIDDEN, CONFIRM, AUTONOMOUS, reversible, compensable, judgeable, eligible_reviewer. Eval cases refund-confirm-happy-path, tags-stay-advisory-only, account-deletion-forbidden, self-approval-refused and no-risk-tier-stops assert these classes; the canonical ordering/judgeability assertions must be added at implementation.

### R8-CONV-5 standing eval/catalog alignment
Canonical standing terms are the R8-CONV-1 names. The standing eval case positive-standing-grant-state-precedence and the policy reference use effective_deadline, not attestation-only wording; the fail-safe missing-deadline case uses BLOCKED with a human remediation path and never says impossible. Catalog alignment: every standing term in docs/skills-catalog.md uses the canonical names; stale-term checks for drift-proof/legal-failure/refresh/environmentMatchGlobs remain clean and are not a substitute for this check. Eval/catalog references are pointers/assertions to this file; no alias is allowed in operative text.

## 4. Formula term registry (R8-CONV-2) and eval assertion mapping

| Term | Meaning | Asserting eval case(s) at implementation |
|---|---|---|
| wait_0 | pre-first-attempt queue/dispatch wait, counted once | latency-budget-architect positive-decompose-journey-target |
| wait_k | inter-attempt wait before attempt k+1 | edge-fan-out-tail-math |
| own_attempt_work | per-attempt own work excluding wait | positive-timeout-folklore-cleanup |
| p | recorded retry probability | edge-fan-out-tail-math |
| R | recorded retry cap | positive-timeout-folklore-cleanup |
| upstream_own_expected_cost | expected own-hop cost before downstream (wait_0 + probability-weighted own work and wait) | positive-decompose-journey-target |
| upstream_own_hard_bound | hard bound/percentile of the upstream own-hop cost | positive-timeout-folklore-cleanup |
| downstream_hard_bound | MAX of branch bounds for downstream hard mode | edge-fan-out-tail-math |
| expected_maximum_at_joins | expected maximum at parallel joins (expected mode), not MAX of means | edge-fan-out-tail-math |
| recorded_percentile | percentile used for hard-mode terms | positive-timeout-folklore-cleanup |
| total_expected_hop_cost | canonical total cost | positive-decompose-journey-target and edge-fan-out-tail-math |
| retry_overhead | total minus initial own+wait+downstream baseline | positive-timeout-folklore-cleanup |
| backoff_total | deterministic schedule wait sum | edge-fan-out-tail-math |
| downstream_expected_critical_path | probability-weighted downstream critical path incl. downstream retry_overhead | edge-fan-out-tail-math |
| epsilon | recorded one-time safety margin | positive-timeout-folklore-cleanup |

Every term above must appear in at least the named eval assertion when the implementation wave updates that eval. R8-A does not run or claim those eval updates.

## 5. Executable check registry

All commands are run from the repository root. R8-A itself runs only the canonical-file integrity checks; the implementation-wave checks are specified now and are run/passed only when the owning wave implements the rule (this PR makes no pass claim for them). Every check states its expected result (P5); checks are discriminating: they name terms that are absent from the base rule text and must be present after the owning wave implements.

Canonical-file integrity (R8-A):
```
python -P -c "from pathlib import Path; t=Path('docs/semantics/canonical-semantics.md').read_text(encoding='utf-8'); ids=['R8-UX-'+str(i) for i in range(1,9)]+['R8-CONV-'+str(i) for i in range(1,6)]; assert all(x in t for x in ids+['P1','P5','total_expected_hop_cost','effective_deadline'])}"   # expected: exit 0 (all 13 canonical IDs and the named terms are present)
```
Implementation-wave checks:
```
git grep -n 'recorded_expiry_or_use_limit' -- .claude/skills/standing-approval-and-auto-advance   # expected: at least one hit AFTER the standing wave implements R8-CONV-1 (term absent from base rule text -> discriminating)
git grep -nE 'wait_k|upstream_timeout|expected_maximum_at_joins|retry_overhead' -- .claude/skills/latency-budget-architect   # expected: at least one hit for each named term AFTER the latency wave implements R8-CONV-2 (adds the missing hard/expected terms -> discriminating)
git grep -n -- '--no-textconv --no-ext-diff' -- .claude/skills/agent-memory-governance   # expected: at least one hit AFTER the memory wave implements R8-CONV-3 (hardened executable content check -> discriminating)
git grep -nE 'judgeable|eligible_reviewer' -- .claude/skills/ai-human-in-the-loop-designer   # expected: at least one hit for each term AFTER the HITL wave implements R8-CONV-4 (FORBIDDEN alone already matches base text and is not discriminating)
python -P -c "import json; d=json.load(open('.claude/skills/standing-approval-and-auto-advance/evals/evals.json')); assert any('effective_deadline' in ' '.join(c['expect']['assertions']) for c in d['cases'])   # expected: exit 0 (assertion holds)
```
Expected results are stated per owning wave; a check that cannot run as written is deleted, not reworded.

## 6. Citation, ownership and change control
All affected SKILL.md files, evals and the agent-memory-governance reference cite this file as a pointer. Citations name the canonical IDs they cover and, from the implementation waves onward, do not restate a rule; existing merged rule text is not rewritten by this R8-A PR. Eval top-level canonical_semantics.covers arrays list individual canonical IDs (range strings are not used, so exact-match consumers see each ID); the JSON path is repository-root-relative, while SKILL one-line citations are document-relative. The eval top-level canonical_semantics key schema additionalProperties is not verified from this repository (repo validator/contract pass); external schema compatibility remains unverified. Audits check operative text against this file. Changes to this file require the owner's recorded instruction; this file is merged before any skill-text change and R8 implementation waves implement each canonical ID once at its named canonical location. No advisory row (R8-ADV-*), review item, or old alias is authority in operative text.
