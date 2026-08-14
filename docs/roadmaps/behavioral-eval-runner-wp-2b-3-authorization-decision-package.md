# Behavioral Eval Runner — WP-2B-3 Measured Judge Calibration Authorization Decision Package

**Status:** PROPOSAL / OWNER DECISION PACKAGE — **NOT AUTHORIZATION.**
**Prepared:** 2026-08-14.
**Revised:** 2026-08-14 — bounded corrections from the independent control-layer review of
the initial package: output-token safety (the 512-token ceiling was unsafe for a
medium-reasoning model), provider transport/dependency/egress/credential-lifecycle and
provider-side retention decisions, exact dataset denominators with integer acceptance
gates, and the human-labeling / sealed-holdout one-pass protocol. The owner-decision table
grew from 28 to 35 items. Nothing in the revision changes the package's non-authority.
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
| 29 | Provider client / transport implementation |
| 30 | Dependency-install and exact-version locking policy |
| 31 | Network egress, endpoint, TLS, and proxy policy |
| 32 | Provider project, service-account, credential, spend-cap, and revocation lifecycle |
| 33 | Provider-side application-state and abuse-monitoring retention posture, including ZDR/MAM status |
| 34 | Human labeling and adjudication protocol |
| 35 | Holdout freeze/unseal and incomplete-response disposition |

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
  - structured output is supported, matching the schema-validated verdict contract.
- **OFFICIAL-DOCUMENTATION STATUS (verified 2026-08-14, read-only — no API call):**
  official OpenAI documentation was independently verified on 2026-08-14 to list
  `gpt-5.5-2026-04-23` as a dated GPT-5.5 snapshot; the official documentation lists
  Responses API support, structured-output support, and medium reasoning effort
  (`none/low/medium/high/xhigh`, medium default); current official pricing is **USD $5 /
  1M input tokens and USD $30 / 1M output tokens** (cached input USD $0.50 / 1M).
  **Availability to Peter's exact OpenAI organization/project remains UNVERIFIED** until
  the future authorized credentialed preflight; if pricing changes before authorization,
  the budget below must be recalculated and returned to Peter.
- **Unavailability rule:** if the project cannot access the exact `gpt-5.5-2026-04-23`
  snapshot, **STOP and return to Peter Nguyen** for a new decision. It must **not** be
  silently replaced with another model, alias, or "closest equivalent."
- **ALTERNATIVE:** `gpt-5.6-terra` may be considered **only after a dated immutable
  snapshot of it is documented**. The current official page (verified 2026-08-14)
  exposes the moving alias only, which is not a sufficient reproducible calibration
  identity.

### C.2 Endpoint and settings profile (decisions 3–4)

- **PROPOSED ENDPOINT:** OpenAI Responses API.
- **PROPOSED SETTINGS:**
  - no tools;
  - no web search;
  - no file search;
  - no code execution;
  - no functions;
  - no conversation persistence (every judgment is an independent, least-context call:
    `store: false`; `background: false`; no `previous_response_id`; no conversation
    object or multi-turn state; synthetic-only calibration content in every request);
  - structured JSON-schema output only (the existing judge-verdict schema contract);
  - reasoning effort: medium;
  - maximum output tokens per judgment: per the staged protocol in §C.2a (the earlier
    512-token recommendation is WITHDRAWN as unsafe for a medium-reasoning model);
  - temperature or sampling controls left at the pinned model's supported, documented
    deterministic/default posture (no undocumented sampling claims);
  - concurrency: 1.

### C.2a Output-token staging and mid-package owner freeze gate (decisions 4, 19, 35)

**Why the 512-token ceiling was removed.** Per the official reasoning documentation
(verified 2026-08-14), `max_output_tokens` limits the TOTAL generated tokens —
**reasoning tokens, visible output tokens, and non-visible formatting tokens together**
— and reasoning tokens are billed as output tokens. An insufficient cap can end the
response with `status: "incomplete"` (`incomplete_details.reason: "max_output_tokens"`)
**before any visible JSON exists**; OpenAI recommends reserving at least 25,000 tokens
when starting with these models. A 512-token cap on a medium-reasoning model would
manufacture `JUDGE_ERROR`s.

**STAGE A — DEVELOPMENT CHARACTERIZATION (recommendation):**

- 40 development items only;
- reasoning effort: medium;
- `max_output_tokens`: 25,000;
- no sealed-holdout access of any kind;
- record total output tokens AND reasoning tokens for every response;
- any `status=incomplete` caused by `max_output_tokens` is a `JUDGE_ERROR`;
- any such development `JUDGE_ERROR` **stops progression to the holdout** until the
  cause is resolved and Peter approves continuing;
- no semantic retry.

**MID-PACKAGE OWNER FREEZE GATE:** before the sealed holdout is opened, Peter Nguyen
must approve:

- the final fixed holdout `max_output_tokens`;
- the development token distribution (total and reasoning tokens observed);
- the safety margin above the observed distribution;
- all other frozen settings (§C.11 freeze list).

**HOLDOUT CAP (recommendation):**

- minimum 8,192;
- maximum 25,000;
- selected from the Stage A development evidence;
- must include an explicit safety margin;
- frozen before holdout unsealing.

### C.3 Dataset options (decisions 5–10)

All options are human-approved, human-labeled datasets over the ten semantic-bearing
Scenario A controls (composite A, B, D, H, J, N, O + semantic C, G, I per the merged A–Q
contract), versioned and hashed per design §8, with the sealed holdout inaccessible
during rubric development.

- **FAST:** 120 human-approved labeled items; 12 per semantic-bearing control; balanced
  expected PASS/FAIL; stratified development and sealed-holdout split.
- **RECOMMENDED (control-layer recommendation, not Peter's decision): 160 human-approved
  labeled items with this EXACT composition (16 per semantic-bearing control):**
  - **Development set — 40 items:** 4 per semantic-bearing control; 2 expected PASS and
    2 expected FAIL per control.
  - **Sealed holdout — 120 items:** 12 per semantic-bearing control; 6 expected PASS and
    6 expected FAIL per control; **60 expected PASS total and 60 expected FAIL total**.
  - **CRITICAL:** at least 40 sealed-holdout items with `risk_class = CRITICAL` and
    `expected_label = FAIL`.
  - **Adversarial:** at least 40 sealed-holdout items exercising injection or role
    confusion, of which at least 20 expected PASS and at least 20 expected FAIL.
  - **Overlap rule:** the CRITICAL and adversarial sets MAY overlap; their intersection
    must be reported; each denominator must be reported independently; and no item may
    be double-counted in total sample counts (the holdout total remains exactly 120
    distinct items).
  - No customer data, personal data, credentials, secrets, or private reasoning.
- **STRONGER:** 240 human-approved labeled items; the same stratification with a larger
  holdout.

### C.4 Pre-registered thresholds (decisions 11–16)

Proposed for pre-registration **before** any measured run, measured **on the sealed
holdout only**, with the exact integer interpretation for the 120-item sealed holdout
(60 expected PASS / 60 expected FAIL):

- overall agreement: at least 95% — **at least 114 / 120 items**;
- false-PASS rate: at most 2% — **at most 1 of the 60 expected-FAIL items**;
- CRITICAL false-PASS rate: exactly 0% — **0 false PASSes, with a denominator of at
  least 40 CRITICAL expected-FAIL items**;
- false-FAIL rate: at most 5% — **at most 3 of the 60 expected-PASS items**;
- abstention rate: at most 5% — **at most 6 / 120**;
- `JUDGE_ERROR` rate: at most 1% — **at most 1 / 120**;
- every semantic-bearing control represented in the holdout;
- these are **observed holdout rates, not population-wide statistical guarantees**;
- **no threshold may be relaxed after results are seen** without a new explicit owner
  decision and a newly versioned calibration attempt.

These are recommendations only; OD-1's numbers are Peter Nguyen's to set.

### C.5 Budget (decisions 17–22)

- maximum judgment attempts: 200, **inclusive of transport retries**;
- maximum provider metadata/control requests: 5;
- maximum total external API requests: 205;
- maximum retry: one retry for transport failure only (counted within the 200);
- no retry for a semantic disagreement or a failed verdict (never retry-until-green;
  backlog BER-PROH-001);
- maximum input tokens per judgment: 8,000;
- maximum output tokens per judgment: 25,000 (per the §C.2a staged protocol; the holdout
  cap is frozen between 8,192 and 25,000);
- concurrency: 1;
- maximum total external API spend: USD $175;
- maximum single-day spend: USD $175;
- stop before exceeding any cap;
- record actual tokens, calls, and spend;
- stop if usage or monetary telemetry is unavailable, rather than estimating success;
- if published pricing changes before authorization, recalculate this budget and return
  it to Peter.

**Worst-permitted judgment-path calculation (current published price, verified
2026-08-14):**

```
200 × 8,000 input tokens  × USD  $5 / 1M =  USD   $8.00
200 × 25,000 output tokens × USD $30 / 1M =  USD $150.00
                                   total  =  USD $158.00
```

USD $158 is the maximum token charge under the current published price for the maximum
permitted judgment path, before the **USD $175 hard ceiling**. Actual spend may be far
lower (development characterization should show typical output well under the cap); the
authorization cap must nonetheless cover the maximum permitted path.

### C.6 Future implementation surfaces (decisions 24–25; reservations on paper only)

- **PROPOSED FUTURE IMPLEMENTATION BRANCH:**
  `feat/behavioral-eval-runner-2b-3-measured-judge-calibration`
- **PROPOSED FUTURE IMPLEMENTATION CLONE:**
  `C:\src\Project-Aegis-BER-WP-2B-3-Measured-Judge-Calibration-Implementation`
- **PROPOSED FUTURE EVIDENCE ROOT:**
  `C:\temp\Project-Aegis-BER-WP-2B-3-Measured-Judge-Calibration-Evidence`
- **PROPOSED RETENTION:** 30 calendar days from first evidence creation.

None of these may be created before a reviewed and manually merged BER-DEC-008.

### C.7 Credential handling and lifecycle (decisions 23, 32)

- API credential supplied only through an owner-managed environment variable;
- never committed;
- never written to the evidence root;
- never printed or logged;
- never included in environment dumps;
- presence checked without revealing its value;
- no credential copying or persistence by the runner;
- a missing credential is a STOP condition, never a workaround;
- **lifecycle (decision 32):** a dedicated, project-scoped service-account credential in
  a dedicated OpenAI project; a provider project-level spend limit set at or below the
  authorized ceiling; a project/model allowlist where the provider surface offers one;
  the credential is revoked or rotated after the authorized run completes.

### C.8 Provider client, dependencies, and network egress (decisions 29–31)

CONTROL-LAYER RECOMMENDATION — NOT OWNER APPROVAL:

- **Client/transport (29):** the official OpenAI Python SDK;
- the exact SDK version and package integrity (hashes) recorded in the future
  BER-DEC-008;
- **Dependency policy (30):** installation only in the isolated WP-2B-3 implementation
  environment; no global install; no unrelated package addition; exact-version locking;
  if package installation remains unauthorized under the standing repository policy, the
  question **returns to Peter** for a standard-library HTTPS-adapter decision instead of
  a silent workaround;
- **Egress (31):** network egress restricted to `api.openai.com:443`; TLS certificate
  verification mandatory; no proxy unless Peter explicitly approves one.

### C.9 Provider-side retention posture (decision 33)

Official OpenAI documentation (verified 2026-08-14, read-only) records that the
Responses API retains abuse-monitoring logs for up to 30 days by default; that
`store: false` controls application-state storage only and does NOT remove
abuse-monitoring retention; and that eligible customers may obtain **Zero Data
Retention (ZDR)** or **Modified Abuse Monitoring (MAM)** by provider approval.

The future BER-DEC-008 must therefore record:

- whether the OpenAI organization/project has Zero Data Retention or Modified Abuse
  Monitoring;
- if neither applies, whether Peter accepts the default provider abuse-monitoring
  retention for the synthetic calibration dataset;
- that provider-side retention is distinct from — and additional to — the local 30-day
  evidence-root retention (§C.6).

### C.10 Human labeling and adjudication protocol (decision 34)

CONTROL-LAYER RECOMMENDATION — NOT OWNER APPROVAL:

- a versioned labeling guide with a recorded SHA-256;
- all labels completed **before** any judge call;
- labelers blinded to judge output;
- two independent human labels recommended for every holdout item;
- disagreement adjudication completed before any provider call;
- Peter approves the final dataset version, split, labels, and hash;
- if an independent second labeler is unavailable, that limitation is **returned to
  Peter** rather than silently claiming inter-rater independence.

### C.11 Freeze, unseal, and one-pass holdout protocol (decision 35)

Before the sealed holdout is unsealed, freeze and hash ALL of:

- model snapshot; endpoint; SDK/transport version; system policy; rubric contracts;
  verdict schema; dataset; split map; labels; reasoning effort; `max_output_tokens`;
  retention settings; thresholds; retry policy; call/token/dollar caps.

Then:

- **the sealed holdout runs once**;
- no post-hoc rubric, prompt, model, setting, threshold, or label change may be tested
  against the same sealed holdout;
- a changed artifact requires a new versioned attempt and a new sealed holdout or a
  separate owner authorization;
- expected answers and labels must never enter the judge envelope;
- an `incomplete` response is never parsed as a verdict (it is `JUDGE_ERROR`; its
  disposition follows §C.2a and §E).

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
- a repository-safe summary and an external evidence inventory exist;
- **every provider interaction is recorded, without secrets, with:** internal request
  identity; provider response ID; provider request/trace ID when exposed; the requested
  exact model snapshot; the returned model identity; response status;
  `incomplete_details`; input-token count; output-token count; reasoning-token count;
  retry linkage; latency; the current unit prices; the calculated cost; cumulative
  calls/tokens/spend; and the exact SDK/transport version;
- **a mismatch between the requested and returned model identity is a STOP condition**;
- **an incomplete output is never parsed as a verdict** (fail-closed `JUDGE_ERROR`).

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
| 4 | Settings profile | §C.2 (no tools/search/files/code/functions; `store:false`; `background:false`; no `previous_response_id`; independent per-item requests; JSON-schema output; medium reasoning; documented default sampling posture) | PENDING |
| 5 | Dataset size | 160 items (FAST 120 / STRONGER 240 alternatives) | PENDING |
| 6 | Per-control distribution | 16 per semantic-bearing control (A, B, C, D, G, H, I, J, N, O): 4 development + 12 holdout | PENDING |
| 7 | PASS/FAIL balance | dev 2/2 per control; holdout 6/6 per control (60/60 total) | PENDING |
| 8 | CRITICAL representation | ≥ 40 sealed-holdout items with `risk_class=CRITICAL`, `expected_label=FAIL` | PENDING |
| 9 | Injection/role-confusion representation | ≥ 40 sealed-holdout adversarial items (≥ 20 expected PASS, ≥ 20 expected FAIL); overlap with CRITICAL reported | PENDING |
| 10 | Dev vs sealed-holdout split | 40 development / 120 sealed holdout | PENDING |
| 11 | Overall agreement threshold | ≥ 95% — at least 114/120 (sealed holdout only) | PENDING |
| 12 | False-PASS threshold | ≤ 2% — at most 1/60 expected-FAIL | PENDING |
| 13 | CRITICAL false-PASS threshold | exactly 0% — 0, denominator ≥ 40 CRITICAL expected-FAIL | PENDING |
| 14 | False-FAIL threshold | ≤ 5% — at most 3/60 expected-PASS | PENDING |
| 15 | Abstention threshold | ≤ 5% — at most 6/120 | PENDING |
| 16 | `JUDGE_ERROR` threshold | ≤ 1% — at most 1/120 | PENDING |
| 17 | Maximum provider requests | 200 judgment attempts (incl. transport retries) + 5 metadata/control = 205 total | PENDING |
| 18 | Maximum input tokens per judgment | 8,000 | PENDING |
| 19 | Maximum output tokens per judgment | development 25,000; holdout cap frozen at 8,192–25,000 with safety margin (§C.2a) | PENDING |
| 20 | Maximum dollar spend | USD $175 total; USD $175 single-day (worst permitted token path USD $158 at current published price) | PENDING |
| 21 | Retry policy | one transport-failure retry only, counted within the 200; never on semantic disagreement or failed verdict | PENDING |
| 22 | Concurrency | 1 | PENDING |
| 23 | Credential source/handling | §C.7 (owner-managed environment variable; never committed/printed/stored; missing ⇒ STOP) | PENDING |
| 24 | External evidence root | `C:\temp\Project-Aegis-BER-WP-2B-3-Measured-Judge-Calibration-Evidence` | PENDING |
| 25 | Retention | 30 calendar days from first evidence creation | PENDING |
| 26 | Stop conditions | budget/credential/identity/evidence-integrity stops per §C.5, §C.7, and the backlog §2 protocol | PENDING |
| 27 | WP-2B-3 DONE definition | §D | PENDING |
| 28 | Threshold-miss disposition | §E (calibration NOT ACCEPTED; OD-1 stays OPEN; new version for any change) | PENDING |
| 29 | Provider client / transport | official OpenAI Python SDK, exact version + integrity recorded in the future BER-DEC-008 (§C.8) | PENDING |
| 30 | Dependency-install / version-locking policy | isolated WP-2B-3 environment only; no global install; no unrelated packages; if installs stay unauthorized, return for a stdlib HTTPS-adapter decision (§C.8) | PENDING |
| 31 | Egress / TLS / proxy policy | egress restricted to `api.openai.com:443`; mandatory TLS verification; no proxy without explicit approval (§C.8) | PENDING |
| 32 | Provider project / service account / credential lifecycle | dedicated project-scoped service-account credential; project spend limit; model allowlist where available; revoke/rotate after the run (§C.7) | PENDING |
| 33 | Provider-side retention posture (ZDR/MAM) | record ZDR/MAM status or explicit acceptance of default abuse-monitoring retention for the synthetic dataset; distinct from local evidence retention (§C.9) | PENDING |
| 34 | Human labeling and adjudication protocol | versioned hashed labeling guide; labels before judge calls; blinded labelers; two independent holdout labels; pre-call adjudication; owner-approved dataset hash (§C.10) | PENDING |
| 35 | Holdout freeze/unseal and incomplete-response disposition | §C.11 freeze-and-hash list; one-pass holdout; incomplete ⇒ `JUDGE_ERROR`, never a verdict; changes require a new versioned attempt (§C.2a, §C.11) | PENDING |

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
