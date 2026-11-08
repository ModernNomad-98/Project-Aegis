# Live-evaluation admission, binding and uncertain-exposure recovery - v1 design

**Item (readable name):** Outcome 7 Live-Evaluation Admission, Binding and Uncertain-Exposure Recovery Design Slice. Plain English: this page writes down, before anyone is allowed to spend money on a live model evaluation, what must be true first, how one exact code candidate is bound to a run, what budget ceiling applies, how unclear or expired evidence is counted rather than guessed, and how to recover when the shipped code and the candidate disagree.
**Row / lane:** plan row P-14, lane L7 (Aegis Maturity Package completion plan, captured revision `5ca5eab04b15b3bed7de2f0986f3ed053ee8616d267bc1608b8cabc70feaf7ff`).
**Record type:** repository design page. **Design evidence only.** It changes no code, performs no live or paid run, contacts no provider, reads no credential, changes no setting or retention policy, dispatches no workflow, posts nothing, and claims no CI, review, audit, merge or qualification result.
**Base:** `e99fa451cbd214a3155e07330436b3c87907e78a`, tree `f83e3153b6a107a38cae5f068b8c17690e084745`.
**Author:** Aegis L7 Agent (DeepSeek Harness); configured route `deepseek-flash`; serving model not observable. No human wrote, reviewed or approved this page.
**Status of the rules below:** proposed design rules for a future, separately authorized live evaluation. They are **not implemented by this page**, **not approved**, and grant nothing. Every rule is either grounded in code observable at the base above or is explicitly labelled as a proposed requirement.

## 1. Purpose and scope

A live evaluation is the one activity in this program that can spend real money, contact an external model provider, and produce evidence a reader could mistake for qualification. The merged code at the base already enforces a gated, fail-closed admission path for it (`tools/behavioral_eval_runner/live/`), and it already carries one bounded exception for two historical smoke "proof" artifacts whose platform retention is expiring. What the repository does not yet have is a single page that states:

1. what admission means and what must be bound to a run before a provider call may happen (section 5);
2. what budget, ceiling and run-count limits apply, and what the recorded-hash acceptance does and does not permit (section 6);
3. how ambiguous, expired or unselected evidence is detected and accounted as uncertain exposure instead of being guessed, zeroed or silently dropped (section 7);
4. how to recover when the candidate state and the shipped state disagree, including the specific #992 candidate-versus-shipped reconciliation (section 8);
5. what evidence a future admission must record, and which decisions remain the owner's (sections 9 and 10).

**In scope:** the rules, the present-behaviour description they depend on, the evidence checklist, and the recovery procedure. **Out of scope:** implementing any of it.

## 2. Non-goals and explicit non-claims

- **No live or paid execution.** No provider was called, no key was read, no budget was reserved, no spend occurred. `LIVE_ENABLED_BY_DEFAULT = False`, `LIVE_GATE_REQUIRED = True` and `LIVE_CAPABILITY_STATE = "GATED"` remain the observable state of the package (`tools/behavioral_eval_runner/live/__init__.py`, lines 27-33).
- **No provider call, no credentials, no network.** Nothing in this page constructs a transport object or resolves a credential.
- **No settings, retention or workflow change.** The 14-day artifact-retention recurrence described in section 12 (line 273) is documented, not fixed; changing it is a separate owner/provider settings action.
- **No code change.** No file under `tools/behavioral_eval_runner/` is edited by this page. That directory is a protected surface: any code change inside `tools/behavioral_eval_runner/live/` requires the owner-authorized manual-review route.
- **No CI claim.** This page asserts no workflow result, no check-run colour and no test outcome. Local checks actually run for the lane that added this page are recorded in that lane's receipt, not here.
- **No approval, review, audit, merge, delivery or publication claim.** This is a local candidate document; it is not on any remote branch and has no reviewer.
- **No new recorded-hash acceptance, no retention exception, no broader exception.** The existing bounded acceptance is described, never extended.
- **No measurement claim beyond the numbers the cited records carry.** Where this page gives a byte count or digest, it was read at the base and is named in section 11.

## 3. Plain-English terms

| Term | Meaning in this page |
| --- | --- |
| **Admission** | The decision, made before any paid call, that this exact run on this exact candidate may proceed and that its worst-case cost fits inside the remaining allowance. |
| **Binding** | Tying a run to exact identities - commit, tree, dataset revision and digest, model identifiers, gate record, config template, run attempt - so that a later change to any of them invalidates the evidence instead of quietly reusing it. |
| **Ceiling** | The maximum total spend the owner has allowed for the allowance. |
| **Cap** | A second, provider-side or gate-side upper bound; the effective ceiling is the smallest applicable bound (section 5.6). |
| **Reservation** | A booking, written before a spend-bearing dispatch, that reserves worst-case cost so the next admission counts it as used even if the run is cancelled or interrupted. |
| **True-up** | Replacing a reservation with the spend that actually happened, once recorded evidence exists. |
| **Exposure** | Money already spent plus money reserved but not yet trued up. |
| **UNKNOWN** | Evidence that could not be established. It is never converted to zero, to a pass, or to an estimate. |
| **Recorded-hash acceptance** | The bounded, documented exception that books a fixed recorded spend for one exact historical run whose proof artifact is gone, using the recorded proof length and digest instead of the artifact. It is weaker than verifying the artifact. |
| **Expired listing** | A platform artifact-listing record with `expired: true`. The merged code treats it as absent; it is not proof of when or whether the bytes were deleted. |

## 4. Verified present state at the base

Everything in this section was read from the base tree, not recalled. Module identities (bytes / SHA-256) are in section 11.

### 4.1 The live package is gated and ships zero dispatches

`tools/behavioral_eval_runner/live/__init__.py` states the contract this design builds on: no live verb runs without a committed/gated owner record; credentials come only from named environment variables and a missing key fails closed; a served model that differs from its pinned identifier halts the run; the cross-vendor judge is reachable only through the owner allowlist and must never share the subject vendor; and **every call is preceded by a reservation against the configured ceiling, with a denied reservation halting dispatch so remaining cases are recorded `UNRUN/BUDGET_CAP` and never `PASS`** (lines 8-18).

### 4.2 The owner gate record is the admission instrument

`live/gate.py` defines the record every live verb must present. Its fields (lines 80-94) are: `gate_id`, `owner_decision_ref`, `fact_origin` (`SYNTHETIC` or `REAL_HOST`), `dataset_revision` (40-hex commit), `dataset_path` (repository-relative, no parent traversal), `dataset_sha256` (64-hex), `case_count`, `subject_models`, `judge_models`, `model_terms` (acknowledgment flag, reference, date), `spend_ceiling_cents`, `provider_cap_cents`, `created_at`, `expires_at` and `schema_version` (line 94, defaulted to the live schema version and checked at line 98).

`require_live_gate` (lines 340-377) refuses when the gate is absent (351-355), when its `fact_origin` is not in the allowed set (360-365), when it was created in the future (366-370), and when it has expired (371-375). It validates the record again on every use rather than trusting a directly built object (line 356).

**The committed gate at the base cannot authorize anything.** `live/gates/pilot-a-apr161.json` records `spend.ceiling_cents = 12000`, `spend.provider_cap_cents = 12000`, `created_at = 2026-10-30T17:50:00Z` and `expires_at = 2026-11-06T17:50:00Z` (lines 34-39). The expiry instant is in the past, so `require_live_gate` refuses. This agrees with the recorded owner-decision request ROD-13 ("the earlier live gate expired 2026-11-06T17:50Z and was not renewed"). A second observation: the same record's `dataset.revision` is forty zeros (line 8) - a placeholder that satisfies the 40-hex shape without binding a real dataset commit.

### 4.3 The effective ceiling is the smallest applicable bound

`OwnerGateRecord.effective_ceiling_cents` returns the minimum of the configured spend ceiling, the gate's ceiling and the gate's provider cap (lines 179-185). The package-level owner bounds are `OWNER_PILOT_CEILING_CENTS = 15000` and `OWNER_PROVIDER_CAP_CENTS = 12000` (`live/config.py`, lines 29-30), and a configuration ceiling above the owner ceiling is refused (lines 140-147). The committed live configuration sets `spend_ceiling_cents = 12000`, `max_output_tokens = 16384` and `runs_per_case = 3` (`live/config/pilot-a-live-config.json`, lines 3-5).

### 4.4 Spend is metered cumulatively, not per workflow

`live/cumulative.py` records the owner decision of 2026-10-31: smoke and trial spend **one** cumulative allowance of 12,000c that includes preserved prior spend, and separate workflow ledgers must not create separate allowances (lines 3-7). The remaining allowance is the ceiling minus prior ledger spend minus cumulative smoke spend (lines 183-189). `admit_paid_call` returns `admitted = remaining_cents >= 0` over a snapshot whose combined exposure is prior ledger plus smoke plus outstanding reservations plus the new reservation (lines 365-393 and 396-420).

### 4.5 Reservations are the exposure primitive

`live/workflow_runtime.py` documents the reservation contract at lines 780-785: a reservation is written atomically **before** a spend-bearing dispatch and survives cancellation or interruption, so the **next admission must count it as outstanding exposure**; a true-up moves the reserved amount into ledger plus specific spend and clears the outstanding amount. A state whose status is `TRUE_UP` must have zero outstanding reservations (lines 832-833). Reservation states are `RESERVED`, `TRUE_UP` and `CANCELLED` (lines 798-800).

### 4.6 Smoke-proof admission and the expiry-only path

`collect_smoke_proof_spends` (`live/workflow_runtime.py`, lines 536-637) walks every ended run of the smoke workflow and books each run's spend. The fail-closed details this design depends on are:

- the artifact listing must reconcile against its declared `total_count` before any expiry handling, or it refuses as incomplete (lines 258-280);
- more than one same-name proof record on one run - duplicate live records, an expired/live mix, or several expired records - refuses, and the refusal names every record id and expired flag, because the available download is name-based and cannot be constrained to one artifact id (lines 601-611);
- a non-boolean `expired` flag is a malformed listing and refuses (lines 595-600);
- a single record is unambiguous: `expired: true` is treated as absent and takes the exact-match registry path, otherwise the one live artifact is downloaded and validated (lines 612-636);
- a run with no proof artifact and no registry entry fails as `UNKNOWN, not zero` (lines 439-440 and 617-618);
- the run's own attempt is part of the paid-attempt identity, so a missing or invalid attempt fails closed and is never defaulted (lines 88-91, 462-473 and 518-529).

The two exact-match registries are `SMOKE_RUNS_WITHOUT_PROOF` (lines 103-125: runs 41167546138 at 6c and 42134872074 at 0c, both recorded failures with attempt 1) and `SMOKE_RUNS_WITH_EXPIRED_PROOF` (lines 174-201: runs 41213566873 and 41179846875, 6c each, heads `1bfdf4a9...` and `cef6e91c...`, attempt 1, proof 2,253 B with digests `d1b18fe2...` and `a202b4ac...`).

The fixture README states the same semantics in prose and names the boundary plainly: retention is an ongoing 14-day workflow property; the registry is a **bounded two-run exception, not a retention fix**; the expired path does **not** receive provenance/tamper validation and is **weaker than verifying the artifact**; an unregistered artifactless run stays `UNKNOWN` and admission stays blocked; adding a future run is a reviewed code change with the same exact-match bounds, not a wildcard (`tools/behavioral_eval_runner/tests/fixtures/live/smoke-proof/README.md`, lines 59-99).

### 4.7 Credentials and model pins

`live/credentials.py` reads each secret from exactly one environment variable, masks it in `repr` and `str`, records only the variable name and presence, never puts the value in an exception message, and fails closed **before** any transport object is constructed (lines 1-7, 30-40, 81-96). `live/providers.py` pins the subject vendors and their prices: `claude-sonnet-5-5` at 200/1000 cents per million tokens (line 57) and `gpt-6-astra` at 1000/5000 (line 59), with cross-vendor judge routes (lines 65-70). These are the shipped pins; the held #992 candidate pins 300/1500 for `claude-sonnet-5-5` and is not shipped (section 8).

## 5. Admission and binding rules for a future live evaluation

Each rule below is a proposed requirement (R-AB), grounded in the code cited. None is implemented by this page.

**R-AB-1 - One exact candidate, named by commit and tree.** A live admission binds exactly one 40-hex commit and that commit's tree, both recorded in the admission evidence. A rebase, merge, retarget, force-push, amend or any other move of the head after admission voids the binding; the evidence is re-derived at the new head, never re-pointed at it. This follows the repository's standing void-on-move rule for head-bound evidence.

**R-AB-2 - A real dataset commit, not a placeholder.** The gate's `dataset_revision` must name a real 40-hex commit (the committed gate's forty zeros satisfy the shape but bind nothing), `dataset_sha256` must be the digest of the exact dataset bytes, and `case_count` must equal the number of cases actually present. Shape validation alone is not evidence of content.

**R-AB-3 - An owner grant is required, and it must be the right kind.** `owner_decision_ref` must name a recorded owner line, and `fact_origin` must be `REAL_HOST` for any real live call; a `SYNTHETIC` record may only exercise a dry run. "The plan allows it" is not a grant; only the owner's recorded words are.

**R-AB-4 - The gate must be current at the instant of the call.** Created-at must not be in the future and now must be strictly before `expires_at`, evaluated per call rather than once per run. The committed gate expires 2026-11-06T17:50:00Z, so no live verb is admissible at the base.

**R-AB-5 - Model pins are exact and a mismatch halts.** Subject and judge models must equal the pinned identifiers; a served-model string that differs halts the run with a structured mismatch error and no silent substitution. The judge route must not share the subject vendor.

**R-AB-6 - Model terms must be acknowledged** with a reference and an ISO-8601 date; an unacknowledged gate refuses.

**R-AB-7 - The ceiling is the smallest applicable bound.** `min(config ceiling, gate ceiling, provider cap)`; none of the three may exceed its owner bound (15,000c and 12,000c at the base).

**R-AB-8 - The attempt number is part of the identity.** Admission records the run id and the attempt; a re-run that increments the attempt is a different paid attempt and does not inherit an earlier decision or an earlier recorded-hash booking.

**R-AB-9 - The configuration template identity is bound.** A proof's `config_template_sha256` must appear in the registered pin map; a new or changed template requires a reviewed change to that map, and the offline drift guard is what detects a mismatch. A committed configuration change that is not reflected in the registry makes the proof inadmissible.

**R-AB-10 - Required recorded evidence at admission.** The admission record must carry, at minimum: gate id and owner reference; commit and tree; dataset revision, digest and case count; the exact model pin set and judge routes; terms reference and date; configured ceiling, gate ceiling, provider cap and the effective ceiling; the reservation record (amount, identity, status); the run ids and attempts; the configuration and gate template identities; the per-call outcomes; and the true-up or explicit outstanding remainder. An item that cannot be produced blocks admission; it is never filled with a plausible value.

**R-AB-11 - Provider and credential boundary.** Credentials come only from the pinned environment variables; a missing value fails closed before any transport object exists; no credential value appears in any record, log, exception or evidence file. No provider object is constructed before admission succeeds, and a denied reservation must not resolve keys or dispatch.

**R-AB-12 - Fail-closed catalogue.** Admission refuses, and records the refusal, when: the gate is absent; the gate is synthetic for a live verb; the gate is expired or future-dated; a model pin mismatches; terms are unacknowledged; the dataset revision or digest is malformed (the merged gate checks only the 40-hex/64-hex shape at `gate.py:102`, so the committed forty-zero placeholder is accepted today; rejecting a placeholder is the proposed strengthening covered by R-AB-2, not current behaviour); the reservation is denied or would overrun the ceiling; the run attempt is missing or invalid; a same-name artifact listing is ambiguous; an artifact listing is incomplete against its declared total; an expired flag is not boolean; a prior history or manifest is absent where history is required; observed smoke history is below the preserved floor. Each refusal names the exact failing condition and the record ids involved; none is converted to zero, to a pass, or to an estimate, and no dispatch follows a refusal in the same decision.

**R-AB-13 - No admission by inference.** Silence, an expired gate, a synthetic gate, an unrecorded attempt, a missing artifact, a missing prior record, or another agent's summary never yields admission. Only a recorded owner grant plus a passing, evidenced admission decision does.

## 6. Budget, ceiling and run-count rules

**R-BC-1 - One shared allowance.** Smoke and trial spend one cumulative allowance of 12,000c that includes preserved prior spend. A second workflow, a fresh workflow run id, or a per-workflow ledger does not create a second allowance.

**R-BC-2 - Remaining is computed, never clamped.** Remaining = ceiling - prior ledger spend - cumulative smoke spend. A negative remainder stays negative and is reported as such; clamping it to zero would hide an overrun.

**R-BC-3 - Reserve worst case before dispatch.** The reservation is computed from enforced limits, not from a guess: the request's actual UTF-8 byte count (a token cannot encode fewer than one byte) and the configured output cap, with no bytes-per-output-token factor. A reservation is written atomically before the call.

**R-BC-4 - Admit only when the post-reservation remainder is non-negative.** The decision is over combined exposure: prior ledger plus smoke plus outstanding reservations plus the new reservation, against the effective ceiling.

**R-BC-5 - A denied reservation halts.** Remaining cases are recorded `UNRUN/BUDGET_CAP` and are never recorded as `PASS`. The run stops; it does not silently continue with cheaper settings.

**R-BC-6 - Bounded run counts, stated in the grant.** The grant must state the case count, the runs per case and the maximum number of paid attempts, and no run may exceed the stated number. The recorded values at the base are 20 cases in the committed gate and `runs_per_case = 3` in the committed live configuration; those are recorded configuration facts, not an authorization, and a future grant must restate its own numbers.

**R-BC-7 - Recorded-hash acceptance is exact-match and bounded.** It applies only to the two registered run ids. At runtime the registry matches run id (by key), conclusion, full 40-hex head and attempt against the committed record, and any mismatch refuses. The recorded proof length and digest are **not** re-validated at runtime, because the artifact is absent: they are audit-only, and the committed-fixture drift guard enforces them offline (`workflow_runtime.py:506-509`; `tests/test_live_workflow_runtime.py:1123`, 1693-1723). It is not a wildcard, not a general compatibility rule, and not a retention fix. Adding a run is a reviewed code change with the same bounds plus a new owner risk acceptance.

**R-BC-8 - The A3 expiry boundary is 2026-11-13 23:15:44 PST.** That instant is 2026-11-14T07:15:44Z, the earliest platform-declared expiry of the two proof artifacts (artifact 13034581056; the second, 13046737982, expires 2026-11-14T15:10:59Z). At and after it the merged code treats an `expired: true` listing and an absent listing identically. The recorded default is **no change / fail-closed** (option A): the two registered runs continue on their recorded identities, and every unregistered, ambiguous or mismatched case still refuses. Nothing happens automatically at the boundary, and exact platform deletion timing remains unknown.

**R-BC-9 - No automatic re-run.** A GitHub re-run keeps the run id and head and increments the attempt, so a re-run does not inherit the earlier booking or the earlier admission; it is a new paid attempt that needs its own decision and reservation. A failed or denied call is not retried automatically.

**R-BC-10 - No unrecorded spend.** Any dispatch without a preceding reservation record is a defect, not a rounding error. A reservation that cannot be trued up stays outstanding and is counted by the next admission; it is never released on the assumption that the call did not happen.

**R-BC-11 - No agent raises a ceiling.** Ceilings and caps are owner-set values carried by the gate and the configuration; a configuration value above the owner bound is refused. An agent may lower a ceiling, never raise one.

**R-BC-12 - Floor integrity.** The identified historical smoke spend must not fall below the preserved 18c smoke floor, and the preserved ledger floor is 222c. The two floors are applied differently. Observed smoke history strictly between 0c and 18c refuses, because it cannot be deduplicated without double counting (`workflow_runtime.py:723-727`); a recorded 0c instead books the preserved 18c (lines 719-722). The ledger floor is not a refusal: the ledger is booked at `max(ledger_spend_cents, PRESERVED_HISTORICAL_LEDGER_CENTS)`, i.e. 222c (`workflow_runtime.py:689`, 730-731). "Below the floor refuses" therefore holds for the effective floor enforced by refusal - the 18c smoke floor - while a sub-222c ledger is raised to 222c, not refused. A shortfall is not repaired by lowering either floor.

## 7. Uncertain-exposure accounting

**R-UE-1 - Detection.** The states below are detected by the merged code and must be reported as states, not resolved by choice:

| Detected state | Where it is detected | Required outcome |
| --- | --- | --- |
| Artifact absent and run unregistered | `collect_smoke_proof_spends` | `UNKNOWN` refusal; admission blocked |
| Listing marked `expired: true` | same | treated as absent; registry path only for exact-match registered runs |
| Two or more same-name proof records | same, lines 601-611 | refusal naming every record id and expired flag |
| Expired/live mix on one run | same | refusal; no name-only selection |
| Non-boolean `expired` flag | same, lines 595-600 | refusal as a malformed listing |
| Listing shorter than its declared total | `list_run_artifacts`, lines 258-280 | refusal as an incomplete listing |
| Missing or invalid run attempt | registry helpers, lines 518-529 | refusal; never defaulted to 1 |
| Conclusion or head mismatch against the registry | registry helpers | refusal |
| Multiple independent trial manifests with different totals | `collect_latest_trial_spend` | refusal as ambiguous aggregation |
| Prior history absent where history is required | `restore_smoke_spend` | refusal; missing is not zero |
| Observed smoke history below the preserved floor | `collect_allowance_history` | refusal |

**R-UE-2 - UNKNOWN is never converted.** It is not zero, not a pass, not an estimate, and not a "probably fine". It blocks admission until recorded evidence resolves it.

**R-UE-3 - What counts as exposure.** Prior ledger spend, booked smoke spend, outstanding reservations (including reservations left behind by a cancelled or interrupted run), and the new reservation being decided. An UNKNOWN does not add a number; it blocks the decision, which is the stronger handling.

**R-UE-4 - What is explicitly not counted.** Local fixture copies of historical proofs, captured screenshots, documentation, cached manifests, provider capacity, pricing predictions, and any hypothetical or modelled spend. These are evidence or context, never exposure.

**R-UE-5 - What is explicitly not inferred.** No inference that an artifact was untampered while it existed (the recorded-hash path cannot prove it); no inference about when or whether the platform deletes expired bytes; no inference that the held #992 implementation is functionally equivalent to the merged helpers (that comparison was never executed); no inference that recorded-hash booking equals artifact verification; no inference that a missing artifact means zero spend; no inference that a documented 0c is a measured bill; no inference that the existing A3 acceptance covers a new run, a new head or a retention change; no inference about provider capacity, model availability or price stability.

**R-UE-6 - Ambiguity is named, not summarized.** A refusal lists the record ids and flags that made the selection ambiguous, so the next reader can resolve the specific conflict without re-deriving the whole listing.

**R-UE-7 - The recorded hash is audit-only at runtime.** The recorded byte count and digest are not re-validated at runtime because the artifact is absent; a committed-fixture drift guard enforces them offline. The registry remains a mutable module-level mapping (both limits are recorded deferrals, P3-1 and P3-2), so the exception is bounded by review, not by runtime proof.

**R-UE-8 - An expired listing is not proof of deletion.** It is a platform statement about availability. Treating it as absent is a policy choice already merged; it is not knowledge of the artifact's history.

**R-UE-9 - A reservation survives the run.** Cancellation or interruption does not clear it; the next admission counts it. Only a recorded true-up clears an outstanding amount, and a true-up state with a non-zero outstanding amount is refused.

**R-UE-10 - Reservations are not merged or netted.** Two reservations for the same case are two exposures. There is no "netting" rule that lets a later, smaller reservation release an earlier one.

**R-UE-11 - A negative remainder halts.** It is reported, not clamped, and no further dispatch follows from a negative remainder.

**R-UE-12 - Recovery accounting is derived from recorded state.** It is recomputed from the reservation record, the manifests and the recorded spend - never from an agent's recollection of what a run did.

## 8. Recovery procedures

**R-RC-1 - Reconcile candidate against shipped before any admission.** The reference record is `RECORDS/PR992-CANDIDATE-VS-SHIPPED-RECONCILIATION.md` - 12,784 B, SHA-256 `ff7003a33f33aec3dabd86c32e851afc401c27e0d1e694f270f6f1edcdae0870` (plan row P-05; closure CL-25 recorded UNVERIFIED (DF-48) - presence only, not closure). Its finding is the operative one: at the capture, all ten changed files differed from main, the candidate head `fe2d05a2...` was 5 ahead and 32 behind main `e99fa451...`, the four functions it adds are absent from main, and main implements the same admission/expiry surface with different symbols. The verdict is that the Pilot-A change is **not merged, not textually shipped, and not superseded by absorption**: it cannot be applied as-is and any future attempt is a rebase-and-re-derive that voids the existing head-bound evidence and needs fresh checks and a fresh review at the new head.

**R-RC-2 - Decide which side is "is" and which is "should".** For a question about current behaviour, the shipped code at the bound commit wins; the held candidate is a proposal, not current behaviour. A divergence is recorded as a finding, not silently resolved by applying the candidate patch.

**R-RC-3 - Re-derive, do not re-point.** After any head, base, body or protection move, the earlier bindings and reviews are void. A recovery that "reuses" a green result from a previous head is not a recovery.

**R-RC-4 - Escalation path.** When recovery cannot settle the state from recorded evidence: stop the affected work; record the state as `UNKNOWN` or `UNRUN` with the exact unresolved question; check the owner-decision records (ROD-13 for live and paid, ROD-10 for the held pull requests including #992's H4, ROD-11 for A3 expiry handling); and if no recorded line answers it, escalate to the owner. No agent may infer an owner answer, and a live/paid answer and a held-PR paid answer must agree - one does not answer the other.

**R-RC-5 - Recovery after a refusal.** Read the refusal's named condition, resolve only that condition with recorded evidence, and take a fresh admission decision. Do not retry on the assumption that the refusal was transient.

**R-RC-6 - Recovery after an interruption.** Count the surviving reservation as exposure; true up only from recorded evidence; if the evidence cannot be produced, leave the reservation outstanding and record why. Never clear an outstanding amount by assumption.

**R-RC-7 - Recovery at and after the A3 boundary.** The four recorded handlings are A (no change, fail-closed - the default), B (retention or settings change - not authorized, separate owner/provider route), C (a broader recorded-hash acceptance - not authorized, requires code change, a new owner risk acceptance, review and tests), and D (another bounded course the owner specifies). Nothing is executed automatically, and silence keeps A.

**R-RC-8 - What remains UNRUN after any recovery.** Any run not actually executed stays UNRUN; a re-run is a new result and the earlier UNRUN stays on the record. A recovery record that converts an UNRUN into a pass by rewriting it is invalid.

## 9. Required evidence checklist for a future live admission

| # | Item | Why it is required | If absent |
| --- | --- | --- | --- |
| 1 | Owner grant: recorded line, scope, budget, ceiling, cap, expiry, stop conditions | Authorization cannot be inferred | Refuse; no admission |
| 2 | Gate record with id, owner reference, `REAL_HOST` origin | The only accepted admission instrument | Refuse |
| 3 | Candidate commit and tree (40-hex each) | Binds the run to one code state | Refuse |
| 4 | Dataset revision (real commit), digest and case count | Binds inputs; a placeholder binds nothing | Refuse |
| 5 | Exact subject and judge model pins and routes | Prevents silent substitution | Refuse; halt on mismatch |
| 6 | Model-terms acknowledgment with reference and date | Required by the gate schema | Refuse |
| 7 | Configured ceiling, gate ceiling, provider cap, effective ceiling | Makes the binding budget explicit | Refuse |
| 8 | Reservation record: amount, identity, status, timestamp | Exposure must be booked before dispatch | Refuse; do not dispatch |
| 9 | Run ids and attempt numbers | Attempt is part of paid identity | Refuse |
| 10 | Configuration and gate template identities | A drifted template is not the recorded configuration | Refuse |
| 11 | Per-call outcomes, including refusals and `BUDGET_CAP` | A refusal is evidence, not an absence | Record as refused/UNRUN |
| 12 | True-up record, or an explicit outstanding remainder | Closes or carries the exposure | Carry as outstanding |
| 13 | The post-run reconciliation of any held candidate against shipped code | Prevents shipping a divergent patch | Record divergence; do not apply as-is |
| 14 | An explicit statement of what was not run | Keeps UNRUN visible | Add it before closeout |

## 10. Residual owner decisions and their safe defaults

All three are **UNDECIDED** at the time of writing. The defaults below are the recorded ones; none is an agent's choice.

| Decision (readable name) | What it asks | Safe default while undecided | What it blocks |
| --- | --- | --- | --- |
| **ROD-13 - Live/paid evaluation decision** (residual owner decision 13 of 15) | Whether any live or paid evaluation run, or any provider contact, is authorized, and under what budget, ceiling, expiry and stop conditions | **Live off; no provider contact.** Outcome 7 stays design and evidence only, with no live claim and no budget-recovery claim | Plan row P-26 (CL-27). Also the paid half of #992's H4 |
| **ROD-10 - Held pull-request gates: #995, #993, #996 and #992** (residual owner decision 10 of 15) | Per-item choices for four held pull requests, all with zero counted approving reviews; for #992 specifically, keep H4 deferred or authorize a bounded paid run with a named gate, budget, cap, ceiling and stop conditions | **Hold all:** nothing merged, no administrator bypass, no provider retry, no paid run, no counted approval created or borrowed, a failed required check stays failed | Plan rows P-31, P-32, P-33 (CL-36, CL-37, CL-38); #992 stays open, conflicted and owner-gated |
| **ROD-11 - A3 artifact-expiry handling before 2026-11-13 23:15:44 PST** (residual owner decision 11 of 15) | Which expiry handling applies at and after the boundary: A (no change, fail-closed), B (retention change), C (broader recorded-hash acceptance) or D (another bounded course) | **Option A - no change; fail-closed stays in force.** The merged two-run exception and the fail-closed selection stay exactly as merged; no retention, settings, provider, live, spend or publication action | Plan row P-35 (CL-40). Silence keeps A and creates no record |

Two further recorded facts belong beside those decisions. First, the owner's head-exact confirmation of the existing bounded A3 acceptance at `e99fa451` is recorded (`evidence/inbox/OWNER-A3-RISK-ACCEPTANCE-HEAD-CONFIRMATION-2026-11-08.md`, 3,847 B, SHA-256 `9a7cf4349211e0c566f17058c4e3fa1c8f9255ce462cfbf9ec84ca313e6a0aff`): it confirms coverage at the hardened head for exactly runs 41179846875 and 41213566873 and explicitly does **not** authorize retention or settings changes, a broader acceptance, provider or live actions, consumer qualification or publication. Second, that confirmation is not an answer to ROD-11 and does not extend to any new run.

## 11. Evidence identities read for this page

All values below were measured locally at the base. Records outside the repository are named by their path under the root that actually holds them: `RECORDS/`, `PLAN/` and `OWNER-DECISIONS/` under `_A/strengthening-program-2026-11-04/COMMANDER-DECISION-PACKET-2026-11-06/AEGIS-COMPLETION-2026-11-08/`; `GATES-PREP-2026-11-08/` and `A3-EXPIRY-DECISION-PREP-2026-11-08/` under `_A/strengthening-program-2026-11-04/COMMANDER-DECISION-PACKET-2026-11-06/`; and `evidence/inbox/` under `_A/strengthening-program-2026-11-04/`.

| Record or module | Bytes | SHA-256 |
| --- | ---: | --- |
| `RECORDS/PR992-CANDIDATE-VS-SHIPPED-RECONCILIATION.md` | 12,784 | `ff7003a33f33aec3dabd86c32e851afc401c27e0d1e694f270f6f1edcdae0870` |
| `RECORDS/DEFERRALS-AND-FINDINGS-REGISTER.md` | 34,448 | `a7c4fefd17b59cca680c01bb72fae4b9bc34eaa08e29651897f8e6f0fa2cabad` |
| `RECORDS/PLAN-REAUDIT4-STAGE-B.md` (ACCEPT at the captured revision) | 42,060 | `426f5fc331dba74903e8dbf338afa291d2793b71c6b828bb6e5c9cc74857bdaf` |
| `PLAN/PLAN.md` (captured revision) | 39,942 | `5ca5eab04b15b3bed7de2f0986f3ed053ee8616d267bc1608b8cabc70feaf7ff` |
| `PLAN/A-ROWS.json` | 58,167 | `920b019d8f0d2068276c8bba36ea31b3e92b9c25024e1dbaee192c2a0730affe` |
| `GATES-PREP-2026-11-08/GATES-PREP-2026-11-08.md` | 34,162 | `bbd5a52860377f7b388c87800270648fe0d7738afc667bb86591a7941d6e2848` |
| `A3-EXPIRY-DECISION-PREP-2026-11-08/A3-EXPIRY-DECISION-PREP-2026-11-08.md` | 32,590 | `7b07fbe11f96957e2b38d49e1dba13e11cf574fb18444100c8cd735a445a28b0` |
| `OWNER-DECISIONS/ROD-10-HELD-PR-GATES.md` | 7,960 | `cb7c772a1d053c68a0c327ff8d0d0b7a56de1912d92cc216a8d3d4c2220ef5d9` |
| `OWNER-DECISIONS/ROD-11-A3-ARTIFACT-EXPIRY-HANDLING.md` | 7,651 | `c2fad8bc43155090072e08ab38adfece988013050a6ed22d9e1dbfe980a90991` |
| `OWNER-DECISIONS/ROD-13-LIVE-PAID-EVALUATION.md` | 5,258 | `9511e2078a9f0153cf6639751a326c637e743a73860f2618fe0626f5af043dd3` |
| `evidence/inbox/OWNER-A3-RISK-ACCEPTANCE-HEAD-CONFIRMATION-2026-11-08.md` | 3,847 | `9a7cf4349211e0c566f17058c4e3fa1c8f9255ce462cfbf9ec84ca313e6a0aff` |
| `tools/behavioral_eval_runner/live/workflow_runtime.py` | 43,999 | `1797f0ee121172dc54a6bae81be74dba65bed4ddf3dd342591eb6a639978dc2c` |
| `tools/behavioral_eval_runner/live/cumulative.py` | 17,064 | `476e549f13fea4258edb5b3519e7803b09665bb49755907e0a1634caf886ee09` |
| `tools/behavioral_eval_runner/live/gate.py` | 15,999 | `cbdb52d774fb89064c43b4133a1c7885f4fdfdd976fceaa484154ca372326317` |
| `tools/behavioral_eval_runner/live/config.py` | 12,395 | `a1c3b5b8e5bdc6e12dcf0cfde6ebd762b870bfa7ca21ef1891a0d90a6852de5e` |
| `tools/behavioral_eval_runner/live/credentials.py` | 3,385 | `27bd3431e65a0be0b2f90febc7e658a43f1523ee06dd75b24413671ab93fae3d` |
| `tools/behavioral_eval_runner/live/providers.py` | 16,092 | `a13fa5a25dbec828605e208b64def23127d6dded7bf0d7e13e17af36db9e7d30` |
| `tools/behavioral_eval_runner/live/__init__.py` | 1,910 | `dd00f73a9c91d2373c6df66d610f14435abf33e60b2b90b5f4ce3148569701bf` |
| `tools/behavioral_eval_runner/tests/fixtures/live/smoke-proof/README.md` | 6,047 | `8846043701aaeb41227cf6574e304ef8bfcbaabba7606297f84f8e33bc043092` |

The two committed JSON inputs cited in section 4 are read as content, not hashed here: `live/gates/pilot-a-apr161.json` (1,342 B) and `live/config/pilot-a-live-config.json` (433 B).

## 12. UNRUN and limitations

- **No live run, no provider call, no paid execution, no credentials, no budget reservation.** Nothing in this page was exercised against a provider.
- **Post-expiry platform behaviour is unobserved.** Only `expired=false` was observed before the boundary; whether GitHub omits or flags the artifacts, and exactly when it deletes them, is unknown. The merged code handles both likely forms, but that handling has not been verified at expiry.
- **Recorded-hash booking is not artifact verification** and cannot prove the artifact was untampered while it existed.
- **The retention recurrence is unresolved.** Every future successful smoke proof older than the 14-day window becomes artifactless and unregistered, so admission stays blocked; fixing it needs a retention/settings change (ROD-11 option B) or a broader acceptance (option C), neither of which is authorized.
- **#992 functional equivalence is unverified.** Whether the held candidate's four functions cover the same threat as the merged helpers was never tested; no code was executed in the reconciliation.
- **No rebase was trialled** for #992; the conflict is asserted from the provider's mergeable state and the reconciliation record, not from a local conflict enumeration.
- **This page is a proposal.** None of R-AB, R-BC, R-UE or R-RC is implemented; a future implementation needs its own plan, its own protected-surface route for any code under `tools/behavioral_eval_runner/live/`, and its own review.
- **No CI, review, audit or merge evidence exists for this page.** It was written and committed locally on one Windows host; no workflow ran, and no independent reader has checked it.
- **Host scope.** All local measurements are from one Windows host and one local clone; no macOS or Linux behaviour was observed.

## 13. Change discipline and traceability

This page is documentation only. A change to a rule here is a new document revision with a new captured identity; rules are never edited silently to match a changed code path. If the merged admission behaviour changes, this page becomes stale and must be re-derived against the new base rather than patched from memory.

| Required design element | Section |
| --- | --- |
| (a) Purpose and scope; explicit non-goals | 1, 2 |
| (b) Admission and binding rules; owner grant; provider/credential boundary; fail-closed behaviour | 5 |
| (c) Budget and ceiling rules; bounded run counts; recorded-hash acceptance; A3 expiry boundary; no automatic re-run; no unrecorded spend | 6 |
| (d) Uncertain-exposure accounting; detection; what counts; what is not inferred | 7 |
| (e) Recovery procedures; candidate-versus-shipped reconciliation (#992); escalation; what remains UNRUN | 8, 12 |
| (f) Required evidence checklist; residual owner decisions and safe defaults | 9, 10 |
| (g) UNRUN and limitations | 12 |

**Authority:** this page records no decision, grants no authority, and changes no gate, budget, ceiling, acceptance or merge condition. The owner decisions named in section 10 remain the owner's alone.
