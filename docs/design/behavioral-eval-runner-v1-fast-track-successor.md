# Behavioral Eval Runner v1.1 — Fast-Track Successor (Scenario A Grading Stack)

**Status:** DESIGN / SPECIFICATION SUCCESSOR — **partial supersession** of
[`behavioral-eval-runner-v1.md`](behavioral-eval-runner-v1.md). Nothing here is built,
wired, or executed.
**Owning skill:** [`eval-runner-designer`](../../.claude/skills/eval-runner-designer/SKILL.md).
**Design baseline (main HEAD):** `72e74af6f0183fef25e353ec2bf3a851d83b5df6` — the merged
WP-2B-1 offline runner core ([PR #83](https://github.com/ModernNomad-98/Project-Aegis/pull/83)).
**Prepared:** 2026-08-13.
**Owner:** Peter Nguyen.
**Repository:** ModernNomad-98/Project-Aegis.
**Governing authorization:** BER-DEC-007, appended to the append-only governance log of
[`docs/roadmaps/behavioral-eval-runner-backlog.md`](../roadmaps/behavioral-eval-runner-backlog.md)
(§13); effective **only after** its governance PR is reviewed and manually merged.

---

## 1. Purpose and authority scope

This successor changes **only the phase structure and directly dependent scope** of the
merged [Behavioral Eval Runner v1 design](behavioral-eval-runner-v1.md). It is authoritative
for that change and for nothing else:

- The **parent v1 design remains authoritative** for architecture, controls, evidence
  rules, containment, and every requirement it defines. Where this successor is silent, v1
  governs unchanged (v1 §1–§6, §10–§18, §20–§24, and the untouched portions of §7–§9 and
  §19).
- This successor is authoritative for the **revised phase map** (§2), the combined
  **WP-2B-2 "Scenario A Grading Stack"** definition and its **non-live** scope (§3–§4), the
  **redefinition of WP-2B-3 as the blocked Measured Judge Calibration and OD-1 Ratification
  Gate** — only its former NON-LIVE scaffold scope is superseded and absorbed by WP-2B-2
  (§6) — the **redefinition of WP-2B-4 as a separate, blocked limited-scope live suite**
  (§7), and the **deferral of generic grading/judging breadth to WP-2B-5** (§8).
- **No claim of solving R1, R2, R4, or R5** is made here. **OD-1 is not ratified.** **No
  live execution, measured calibration, generic-corpus execution, or CI integration is
  authorized.**
- A conflict between this successor and the parent design is a **STOP condition** surfaced
  to the owner, never resolved silently in either direction.

## 2. Revised phase map (fast-track)

The fast track is achieved by **changing the phase design and scope**, not by granting
authorization across blocked phase boundaries. Each phase still begins only with its own
merged owner authorization (backlog §2 work-package authorization protocol); no arrow is
crossed by momentum, and no later phase may erase an earlier phase's evidence boundary
(parent §19).

| Phase | Name | Status under this successor |
| --- | --- | --- |
| WP-2B-1 | Offline runner core and minimum guardrails | **DONE** — completion evidence [PR #83](https://github.com/ModernNomad-98/Project-Aegis/pull/83), merge commit `72e74af6f0183fef25e353ec2bf3a851d83b5df6` |
| WP-2B-2 | **Scenario A Grading Stack** — combined NON-LIVE deterministic + semantic grading | **AUTHORIZED by BER-DEC-007**, effective only after its governance PR is manually merged |
| WP-2B-3 | **Measured Judge Calibration and OD-1 Ratification Gate** (redefined; former title: Independent injection-resistant semantic judge) | **BLOCKED** — NOT authorized by BER-DEC-007; requires its own future, separate, reviewed and merged BER-DEC authorization (§6). Only the former WP-2B-3 **NON-LIVE scaffold scope** is superseded and absorbed by WP-2B-2; no former generic/non-live judge implementation remains separately scheduled; historical record retained |
| WP-2B-4 | **Scenario A Limited-Scope Live Suite** | Separate first-live phase — **BLOCKED**, **NOT authorized** by BER-DEC-007 |
| WP-2B-5 | Generic corpus execution | **BACKLOG** — receives the generic grader/judge breadth deferred by the fast track |

WP-2B-6 (advanced cadence / analytics / cost refinement) and WP-2B-7 (advisory CI) continue
unchanged per the parent design §19 and the backlog §7 register. **WP-2B-7 remains the sole
owner of actual advisory CI integration and operator workflow** (§8).

This phase compression **does not** claim R1, R2, R4, or R5 is solved; **does not** ratify
OD-1; **does not** authorize WP-2B-3 measured-calibration work; and **does not** authorize
live execution.

## 3. WP-2B-2 — Scenario A Grading Stack (Deterministic + Semantic, Non-Live)

The revised WP-2B-2 combines, as a single **non-live** implementation and test work package:

- **A. The Scenario-A-required subset of the former WP-2B-2 deterministic graders** (parent
  design §7).
- **B. The NON-LIVE implementation and test-harness subset of the former WP-2B-3 semantic
  judge** (parent design §8).

It **does NOT** combine or authorize any of:

- real judge/model/provider calls;
- measured judge calibration;
- OD-1 ratification;
- Scenario A live execution;
- WP-2B-4 implementation;
- generic corpus execution;
- CI integration.

The actual R2 measured calibration and OD-1 ratification (parent §8, §17a; backlog OD-1)
are **owned by the redefined WP-2B-3 gate** (§6) and **remain required before WP-2B-4 may be
authorized**. This work package builds the judge **scaffold and its deterministic harness
only** — every judge-facing behavior is exercised with deterministic mocks and recorded
fixtures; the grading stack and its test harness generate no model, provider, or judge
dispatch.

## 4. WP-2B-2 authorized non-live scope

BER-DEC-007 authorizes the following NON-LIVE scope only.

### Deterministic Scenario A graders (parent design §7, §9, §5c–§5d)

- stage-transition validation;
- authorization and approval-boundary validation;
- prohibited-action and mutation checks;
- append-only evidence checks;
- preview-versus-created hashing (run-local only; never fixture-pin digests on live output);
- recording-state checks;
- typed skill/subagent target handling (§5d);
- invocation-mode validation when supported by available evidence (§5c);
- deterministic Scenario A controls A–Q (the deterministic subset of §9);
- versioned deterministic reason codes;
- evidence pointers;
- deterministic recorded good/bad fixtures;
- unit, integration, and schema tests.

The activation matcher is built **only on the mechanism Phase 2B-0 proved real**; where the
mechanism is unproven or the evidence is prose-only, the grader yields `ERROR` /
`AMBIGUOUS_ACTIVATION`, never a manufactured verdict. No R1 "solved" claim is made.

### Semantic Scenario A grading scaffolding (parent design §8)

- an independent judge interface;
- pinned judge-identity representation;
- injection-resistant system policy;
- transcript treated as delimited untrusted data;
- no judge tools;
- least-context input envelope;
- schema-validated structured verdict;
- `JUDGE_ERROR` fail-closed behavior;
- coherent-topic grading contract (the accepted Scenario A rule, preserved exactly);
- other Scenario A assertions that cannot be mechanically graded;
- minimum versioned human-labeled calibration-dataset structure;
- deterministic/mock calibration harness;
- threshold-enforcement logic using recorded/mock results;
- drift/recalibration trigger representation;
- unit, integration, injection-defense, and schema tests.

The semantic scaffold must be **testable with deterministic mocks and recorded fixtures
only**. **No runner-generated, grading-stack-generated, or test-harness-generated
model/provider dispatch and no actual judge/provider call is authorized. No measured
calibration result may be claimed.**

**Implementation-session activity is distinct from runner dispatch.** WP-2B-2 will be
implemented in an AI-assisted session (e.g., Claude Code). Model calls made by that
implementation session — or by read-only review agents — to author or inspect code and docs
are implementation-session activity: they are not Behavioral Eval Runner dispatches, they
are not counted against the runner's 0-dispatch budget, they must be disclosed separately
in the implementation closeout, and they constitute no Behavioral Eval Runner execution or
calibration evidence.

The accepted Scenario A semantic rule is preserved exactly (parent §8, §9):

> **ONE COHERENT DISCOVERY TOPIC PER TURN.**
> **Related supporting details within that topic are allowed.**

## 5. What remains required before WP-2B-4

This successor moves **no** live gate. Before WP-2B-4 (the first live phase) may be
authorized, all of the following still must exist (parent §8, §9, §17a, §19; backlog
WP-2B-4, OD-1, R1/R2/R4/R5):

- WP-2B-2 DONE;
- **WP-2B-3 DONE** — the Measured Judge Calibration and OD-1 Ratification Gate (§6), itself
  requiring its own future, separate, reviewed and merged authorization, delivering:
  - actual **measured** judge calibration against the versioned human-labeled dataset;
  - **OD-1 ratified** by Peter Nguyen (numeric acceptance thresholds, including the separate
    critical false-PASS threshold);
- an owner-approved **selected-host R4 disposition** (effective per-tool-path confinement);
- an owner-approved **selected-profile R5 disposition** (execution-profile
  observability/isolation);
- any residual **R1** dependency either supported or expressly excluded from the bounded
  claim;
- a **separate reviewed and merged WP-2B-4 authorization**, with a live-token budget, a live
  external evidence root, evidence-handling and retention terms, and live stop conditions.

BER-DEC-007 grants none of those permissions.

## 6. WP-2B-3 — redefined: Measured Judge Calibration and OD-1 Ratification Gate

The former WP-2B-3 (independent injection-resistant semantic judge) is **redefined, not
erased**: only its **NON-LIVE scaffold scope is superseded and absorbed by WP-2B-2** (§4),
its historical record is retained in the backlog §7 register, its design substance remains
in parent design §8, and **WP-2B-3 itself continues as the narrow Measured Judge
Calibration and OD-1 Ratification Gate**. No former generic/non-live judge implementation
remains separately scheduled.

**Status: BLOCKED.** WP-2B-3 is **NOT authorized by BER-DEC-007.** It requires a future,
separate, reviewed and merged BER-DEC authorization recording its own exact branch, its
actual judge/provider-call budget, its external evidence root, its evidence-handling terms,
its retention, its stop conditions, and its owner review.

**WP-2B-3 owns:**

- actual pinned-judge selection or confirmation;
- execution against the versioned human-labeled calibration dataset;
- confusion-matrix measurement;
- aggregate agreement/accuracy measurement;
- false-PASS measurement;
- false-FAIL measurement;
- abstention/`JUDGE_ERROR` measurement;
- separate CRITICAL false-PASS measurement;
- measured adversarial injection and role-confusion calibration;
- presentation of the measured result to Peter Nguyen;
- OD-1 numeric-threshold and measured-result ratification.

**WP-2B-3 must not:**

- run the Scenario A system under test;
- authorize WP-2B-4;
- produce a baseline-eligible semantic verdict before OD-1 is ratified.

## 7. WP-2B-4 — Scenario A Limited-Scope Live Suite (separate, BLOCKED, documented only)

WP-2B-4 becomes the **Scenario A Limited-Scope Live Suite** — the separate first-live phase.
This successor may **document** its future bounded claim scope but **may not authorize or
implement it**.

The future **initial claim scope** is limited to:

- Scenario A only;
- explicit invocation of `project-orchestrator`;
- one pinned Project Aegis version;
- one pinned execution profile;
- one selected host configuration;
- one approved synthetic answer set;
- Scenario A controls A–Q;
- **no** claim that the model independently selected `project-orchestrator`;
- **no** general model-selected routing claim;
- **no** generic corpus claim;
- **no** baseline claim;
- **no** stability-window claim;
- **no** promotion claim;
- **no** production-readiness claim.

**Explicit invocation proves only that the named target was intentionally invoked. It does
not prove independent routing selection.**

WP-2B-4 remains **BLOCKED** until every item in §5 exists, including a separate reviewed and
merged WP-2B-4 authorization. BER-DEC-007 grants none of them.

## 8. Generic breadth deferred to WP-2B-5

The following generic-breadth items are moved out of the pre-Scenario-A path and into
WP-2B-5 (generic corpus execution), which **remains BACKLOG and is not authorized here**:

- generic deterministic grader mappings for the complete authored corpus;
- generic semantic rubric mappings;
- generic corpus judge configuration;
- generic activation-observer breadth;
- generic fixture-library breadth;
- integration with all 1,740 authored single-prompt cases (runnable units remain the
  per-run preflight output, never an assumed 1,740 — parent §5, §5b, §19);
- corpus-wide execution;
- corpus-wide calibration where separately authorized;
- generic-corpus evidence runs;
- reports and output contracts suitable for later CI consumption.

WP-2B-5 does **NOT** own: GitHub Actions workflow creation or modification; advisory CI
wiring; scheduled CI cadence; CI permissions; CI artifact-retention wiring; PR advisory
check integration; or the operator CI workflow. **WP-2B-7 remains the sole owner of actual
advisory CI integration and operator workflow** (parent §16, §19; backlog WP-2B-7).

## 9. Relationship to the parent design (partial-supersession pointers)

| Parent design section | Effect under this successor |
| --- | --- |
| §7 Deterministic grading | Its **Scenario-A-required subset** is delivered (non-live) by WP-2B-2 (§4). Generic breadth → WP-2B-5 (§8). |
| §8 Semantic judging | Its **non-live scaffold + deterministic/mock calibration harness** is delivered by WP-2B-2 (§4). Measured calibration and OD-1 ratification are owned by the redefined WP-2B-3 gate (§6); live use remains gated ahead of WP-2B-4 (§5). |
| §9 Scenario A behavioral suite | Its **deterministic + semantic grading** is built (non-live) in WP-2B-2; the **live adaptive suite** is WP-2B-4, blocked (§7). |
| §19 Implementation phases | Phase rows 2B-2 / 2B-3 / 2B-4 / 2B-5 are re-mapped per §2; the hard live-phase precondition and the evidence-boundary rules stand unchanged. |

All other parent-design sections stand unchanged.

## 10. Non-claims

This successor and BER-DEC-007 do **not** claim or authorize:

- that R1, R2, R4, or R5 is solved;
- any measured judge-calibration result;
- OD-1 ratification;
- any Scenario A live execution or generic-corpus execution;
- any baseline, stability-window, routing, promotion, or production-readiness claim;
- any runner-generated, grading-stack-generated, or test-harness-generated model/provider
  dispatch, or any actual judge/provider call;
- WP-2B-3 measured-calibration or OD-1-ratification work;
- any CI/workflow wiring, deployment, package installation, or merge.

Authority attaches only to the merged governance PR that contains BER-DEC-007, and only for
the non-live WP-2B-2 scope defined above.
