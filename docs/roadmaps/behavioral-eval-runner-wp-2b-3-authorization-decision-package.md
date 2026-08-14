# Behavioral Eval Runner — WP-2B-3 Measured Judge Calibration Authorization Decision Package

**Status:** PROPOSAL / OWNER DECISION PACKAGE — **NOT AUTHORIZATION.**
**Prepared:** 2026-08-14.
**Owner and sole decision authority:** Peter Nguyen.
**Repository:** ModernNomad-98/Project-Aegis.
**Work package:** WP-2B-3 — Measured Judge Calibration and OD-1 Ratification Gate
([`behavioral-eval-runner-backlog.md`](behavioral-eval-runner-backlog.md) §7).
**Governing design:** merged design
[`behavioral-eval-runner-v1.md`](../design/behavioral-eval-runner-v1.md) (§8, §13, §17
criterion 9, §17a item 9, §20 D1/D9/OD-1/R2) as partially superseded by the v1.1
fast-track successor
[`behavioral-eval-runner-v1-fast-track-successor.md`](../design/behavioral-eval-runner-v1-fast-track-successor.md)
(§6).

This document exists so Peter Nguyen can make the exact, itemized decisions a future
WP-2B-3 authorization must record. It must be read with the following standing facts:

- **BER-DEC-008 has not been issued.** The governance log of
  [`behavioral-eval-runner-backlog.md`](behavioral-eval-runner-backlog.md) (§13) ends at
  BER-DEC-007.
- **WP-2B-3 remains BLOCKED and unauthorized.** This package does not change that status
  and cannot: execution authority attaches only to a reviewed and manually merged BER-DEC
  entry (backlog §2 work-package authorization protocol).
- **No provider call is authorized by this document.** Zero judge/provider/model calls
  may be made under it, including "just to check availability."
- **No model or API credential may be used** under this document — not read, not tested,
  not printed, not stored.
- **No implementation branch, implementation clone, or external evidence root may be
  created yet.** The names proposed below are reservations on paper only.
- **Every "recommended" or "proposed" value below is a control-layer proposal, not
  Peter's decision.** Nothing in this file may be quoted as owner approval.

---

## A. Completed prerequisite (what already exists)

- **WP-2B-2 is complete.** The Scenario A Grading Stack was implemented NON-LIVE and
  merged through [PR #85](https://github.com/ModernNomad-98/Project-Aegis/pull/85)
  (final reviewed head `5d16bace5fec9f7c394ad7f3b4147ac9d4ad74f2`, squash merge
  `b84e43ad9f42a793c6f68c2f5aebf0abfad2b8ed`, tree
  `81404d350a26e8349d3c869209ae04f8628e0a95`), and Peter Nguyen's **D9 contract/schema
  approval was recorded in the final PR #85 body, scoped to the WP-2B-2 non-live
  contract shapes only**.
- **The non-live scaffold this gate will exercise exists:** the provider-denial judge
  interface (`DisabledJudgeProvider`, `LIVE_DISPATCH_DISABLED`; no provider
  implementation exists), the injection-resistant system policy, the delimited base64
  untrusted-data envelope with trusted contract-derived control context, the
  coherent-topic and control-semantics rubric contracts, the versioned schemas
  (`1.0.0-wp2b2`), the recorded-fixture mock harness, and the deterministic
  confusion-matrix/agreement/false-PASS/false-FAIL/abstention/`JUDGE_ERROR` metrics with
  the separate CRITICAL false-PASS rate — thresholds representable only as
  `MOCK_UNRATIFIED`.
- **No measured calibration exists.** Every calibration result to date is
  deterministic/mock and says nothing about any real judge.
- **OD-1 remains OPEN** (backlog §9): no numeric threshold is ratified, and no
  baseline-eligible semantic verdict can exist before a measured result meets
  owner-ratified thresholds.

## B. Exact owner decisions required

WP-2B-3 cannot be authorized until Peter Nguyen decides every row below. Each decision
must be recorded verbatim in the future authorization entry; the control-layer
recommendations for each row live in §C and are proposals only.

| # | Decision Peter Nguyen must make |
| --- | --- |
| 1 | Judge provider |
| 2 | Exact immutable judge model/snapshot identity |
| 3 | API endpoint |
| 4 | Reasoning/settings profile (tools, output mode, reasoning effort, sampling posture) |
| 5 | Human-labeled calibration dataset size |
| 6 | Per-control distribution across the semantic-bearing controls |
| 7 | Expected PASS/FAIL balance |
| 8 | CRITICAL-risk representation (count and composition) |
| 9 | Adversarial injection and role-confusion representation |
| 10 | Development vs sealed-holdout split |
| 11 | Overall agreement threshold |
| 12 | False-PASS threshold |
| 13 | CRITICAL false-PASS threshold |
| 14 | False-FAIL threshold |
| 15 | Abstention threshold |
| 16 | `JUDGE_ERROR` threshold |
| 17 | Maximum provider calls |
| 18 | Maximum input tokens per call |
| 19 | Maximum output tokens per call |
| 20 | Maximum dollar spend |
| 21 | Retry policy |
| 22 | Concurrency |
| 23 | Credential source and handling |
| 24 | External evidence root |
| 25 | Evidence retention |
| 26 | Stop conditions |
| 27 | What constitutes WP-2B-3 DONE |
| 28 | What happens when thresholds are missed (failure disposition) |

## C. Control-layer recommended package — NOT YET APPROVED

Everything in this section is a recommendation prepared for owner review. **None of it is
approved, and none of it authorizes anything.**

### C.1 Provider and pinned judge (decisions 1–2)

- **INDEPENDENT PROVIDER (recommended):** OpenAI API.
- **RECOMMENDED PINNED JUDGE:** `gpt-5.5-2026-04-23` (a dated snapshot identifier).
- **RATIONALE:**
  - the provider is independent from the Claude system under test (design §8 / D1
    independence);
  - a dated snapshot is preferable to a moving alias for a reproducible calibration
    identity;
  - structured output is supported, matching the schema-validated verdict contract;
  - **verification status: NOT verified in this task.** No provider call, availability
    check, or documentation lookup was performed here. The recommendation **must be
    reverified immediately before BER-DEC-008 is finalized and again during
    implementation preflight.**
- **Unavailability rule:** if the `gpt-5.5-2026-04-23` snapshot is unavailable at
  verification time, the authorization **returns to Peter Nguyen** for a new decision.
  It must **not** be silently replaced with another model, alias, or "closest
  equivalent."
- **ALTERNATIVE:** `gpt-5.6-terra` may be considered **only after a dated immutable
  snapshot of it is verified**. The moving alias alone is not a sufficient reproducible
  calibration identity.

### C.2 Endpoint and settings profile (decisions 3–4)

- **PROPOSED ENDPOINT:** OpenAI Responses API.
- **PROPOSED SETTINGS:**
  - no tools;
  - no web search;
  - no file search;
  - no code execution;
  - no conversation persistence (every judgment is an independent, least-context call);
  - structured JSON-schema output only (the existing judge-verdict schema contract);
  - reasoning effort: medium;
  - maximum output tokens per judgment: 512;
  - temperature or sampling controls left at the pinned model's supported, documented
    deterministic/default posture (no undocumented sampling claims);
  - concurrency: 1.

### C.3 Dataset options (decisions 5–10)

All options are human-approved, human-labeled datasets over the ten semantic-bearing
Scenario A controls (composite A, B, D, H, J, N, O + semantic C, G, I per the merged A–Q
contract), versioned and hashed per design §8, with the sealed holdout inaccessible
during rubric development.

- **FAST:** 120 human-approved labeled items; 12 per semantic-bearing control; balanced
  expected PASS/FAIL; stratified development and sealed-holdout split.
- **RECOMMENDED (control-layer recommendation, not Peter's decision):** 160
  human-approved labeled items; 16 per semantic-bearing control; 40-item development
  set; 120-item sealed holdout; balanced expected PASS/FAIL per control; at least 40
  CRITICAL examples; at least 40 adversarial injection or role-confusion examples; no
  customer or personal data; no private chain-of-thought.
- **STRONGER:** 240 human-approved labeled items; the same stratification with a larger
  holdout.

### C.4 Pre-registered thresholds (decisions 11–16)

Proposed for pre-registration **before** any measured run, measured **on the sealed
holdout only**:

- overall agreement: at least 95%;
- false-PASS rate: at most 2%;
- CRITICAL false-PASS rate: exactly 0%;
- false-FAIL rate: at most 5%;
- abstention rate: at most 5%;
- `JUDGE_ERROR` rate: at most 1%;
- every semantic-bearing control represented in the holdout;
- **no threshold may be relaxed after results are seen** without a new explicit owner
  decision and a newly versioned calibration attempt.

These are recommendations only; OD-1's numbers are Peter Nguyen's to set.

### C.5 Budget (decisions 17–22)

- maximum provider calls: 200;
- maximum retry: one retry for transport failure only;
- no retry for a semantic disagreement or a failed verdict (never retry-until-green;
  backlog BER-PROH-001);
- maximum input tokens per call: 8,000;
- maximum output tokens per call: 512;
- concurrency: 1;
- maximum total external API spend: USD $15;
- maximum single-day spend: USD $15;
- stop before exceeding any cap;
- record actual tokens, calls, and spend;
- if monetary telemetry is unavailable, stop rather than estimate success.

### C.6 Future implementation surfaces (decisions 24–25; reservations on paper only)

- **PROPOSED FUTURE IMPLEMENTATION BRANCH:**
  `feat/behavioral-eval-runner-2b-3-measured-judge-calibration`
- **PROPOSED FUTURE IMPLEMENTATION CLONE:**
  `C:\src\Project-Aegis-BER-WP-2B-3-Measured-Judge-Calibration-Implementation`
- **PROPOSED FUTURE EVIDENCE ROOT:**
  `C:\temp\Project-Aegis-BER-WP-2B-3-Measured-Judge-Calibration-Evidence`
- **PROPOSED RETENTION:** 30 calendar days from first evidence creation.

None of these may be created before a reviewed and manually merged BER-DEC-008.

### C.7 Credential handling (decision 23)

- API credential supplied only through an owner-managed environment variable;
- never committed;
- never written to the evidence root;
- never printed;
- never included in environment dumps;
- presence checked without revealing its value;
- no credential copying or persistence by the runner;
- a missing credential is a STOP condition, never a workaround.

## D. Proposed WP-2B-3 DONE criteria (decision 27)

Recommend that WP-2B-3 reaches DONE only when ALL of the following hold:

- the exact provider/model snapshot is verified (at authorization finalization and again
  at implementation preflight);
- the human-approved calibration dataset version and hash are recorded;
- the sealed holdout remained inaccessible during rubric development;
- every authorized calibration call is accounted for (calls, tokens, spend);
- the confusion matrix and all required rates are calculated with explicit denominators;
- the injection/role-confusion subset is reported separately;
- the pre-registered thresholds are evaluated mechanically against the sealed-holdout
  result;
- no evidence-integrity failure occurred;
- Peter Nguyen reviews the measured result;
- Peter Nguyen explicitly ratifies or declines OD-1 on that measured result;
- no Scenario A system-under-test execution occurred;
- no WP-2B-4 work occurred;
- a repository-safe summary and an external evidence inventory exist.

## E. Proposed failure disposition (decision 28)

Recommend that a threshold miss is handled as follows:

- a threshold miss does **not** trigger retry-until-green;
- the result is recorded as **calibration NOT ACCEPTED**;
- OD-1 remains OPEN;
- no baseline-eligible semantic verdict exists;
- any rubric, judge-model, or dataset change creates a **new version and a new measured
  attempt** (with re-calibration per design §8);
- WP-2B-4 remains blocked.

## F. Owner response block

Peter Nguyen may approve, edit, or replace any row. A row left PENDING is undecided. No
row below records an approval, and nothing in this package may be treated as one.

| # | Item | Control-layer proposal (not approved) | Owner decision |
| --- | --- | --- | --- |
| 1 | Provider | OpenAI API | PENDING |
| 2 | Immutable model/snapshot | `gpt-5.5-2026-04-23` (reverify; return to owner if unavailable) | PENDING |
| 3 | API endpoint | OpenAI Responses API | PENDING |
| 4 | Settings profile | §C.2 (no tools/search/code/persistence; JSON-schema output; medium reasoning; 512 output tokens; documented default sampling posture) | PENDING |
| 5 | Dataset size | 160 items (FAST 120 / STRONGER 240 alternatives) | PENDING |
| 6 | Per-control distribution | 16 per semantic-bearing control (A, B, C, D, G, H, I, J, N, O) | PENDING |
| 7 | PASS/FAIL balance | balanced per control | PENDING |
| 8 | CRITICAL representation | at least 40 CRITICAL examples | PENDING |
| 9 | Injection/role-confusion representation | at least 40 adversarial examples | PENDING |
| 10 | Dev vs sealed-holdout split | 40 development / 120 sealed holdout | PENDING |
| 11 | Overall agreement threshold | ≥ 95% (sealed holdout only) | PENDING |
| 12 | False-PASS threshold | ≤ 2% | PENDING |
| 13 | CRITICAL false-PASS threshold | exactly 0% | PENDING |
| 14 | False-FAIL threshold | ≤ 5% | PENDING |
| 15 | Abstention threshold | ≤ 5% | PENDING |
| 16 | `JUDGE_ERROR` threshold | ≤ 1% | PENDING |
| 17 | Maximum provider calls | 200 | PENDING |
| 18 | Maximum input tokens per call | 8,000 | PENDING |
| 19 | Maximum output tokens per call | 512 | PENDING |
| 20 | Maximum dollar spend | USD $15 total; USD $15 single-day | PENDING |
| 21 | Retry policy | one transport-failure retry only; never on semantic disagreement or failed verdict | PENDING |
| 22 | Concurrency | 1 | PENDING |
| 23 | Credential source/handling | §C.7 (owner-managed environment variable; never committed/printed/stored; missing ⇒ STOP) | PENDING |
| 24 | External evidence root | `C:\temp\Project-Aegis-BER-WP-2B-3-Measured-Judge-Calibration-Evidence` | PENDING |
| 25 | Retention | 30 calendar days from first evidence creation | PENDING |
| 26 | Stop conditions | budget/credential/identity/evidence-integrity stops per §C.5, §C.7, and the backlog §2 protocol | PENDING |
| 27 | WP-2B-3 DONE definition | §D | PENDING |
| 28 | Threshold-miss disposition | §E (calibration NOT ACCEPTED; OD-1 stays OPEN; new version for any change) | PENDING |

```
OWNER DECISION:
PENDING

BER-DEC-008:
NOT ISSUED
```

Only after Peter Nguyen records his decisions and a reviewed PR is **manually merged**
appending a BER-DEC-008 entry that captures those exact terms does WP-2B-3 become
authorized. Until then, WP-2B-3 stays BLOCKED, no provider call or credential use is
permitted, and no implementation surface may be created.
