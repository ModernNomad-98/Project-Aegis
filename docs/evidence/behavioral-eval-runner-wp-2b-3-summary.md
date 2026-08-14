# Behavioral Eval Runner — WP-2B-3 Stage A1: sanitized implementation summary

**Scope: the OFFLINE Stage A1 slice of WP-2B-3 (Measured Judge Calibration and OD-1
Ratification Gate) under BER-DEC-008 — the calibration-only provider transport,
request/token/cost accounting, owner-label approval gate, holdout freeze gate, and the
SYNTHETIC CANDIDATE dataset/labeling/review artifacts. ZERO provider/model/metadata
calls; ZERO credential access; USD $0 external provider spend; the 40-item development
calibration has NOT started; the sealed holdout is NOT opened; OWNER_LABEL_APPROVAL is
PENDING; OD-1 remains OPEN; WP-2B-4 remains BLOCKED.**

This file is repository-safe: no personal username, no personal path, no secret, no
environment dump, no raw dataset content. The candidate dataset, labeling guide, owner
label-review packet, and full build/validation logs are retained ONLY under the
BER-DEC-008 external evidence root and are not committed.

## 1. Authorization

| Item | Value |
| --- | --- |
| Authorization record | BER-DEC-008 |
| Authorization PR | [#87](https://github.com/ModernNomad-98/Project-Aegis/pull/87) — MERGED (manual owner squash merge; GitHub signature verified) |
| Authorization merge SHA | `1c3e4931329179d9a3f9cc9ec1bb93020378c043` |
| Authorization tree SHA | `feb7cf261d8efa624c18363c9928e7f0cbdfed4c` |
| Authorized work package | WP-2B-3 — Measured Judge Calibration and OD-1 Ratification Gate (Stage A1 offline slice) |
| Implementation branch | `feat/behavioral-eval-runner-2b-3-measured-judge-calibration` |
| Implementation PR | [#88](https://github.com/ModernNomad-98/Project-Aegis/pull/88) — DRAFT (Stage A1 stopping point; not ready, no reviewer requested, no auto-merge, no merge) |
| Implementation base | the exact authorization merge commit above (never a later moving `main`; `main` was verified identical to it at branch creation) |
| Authoritative design | `docs/design/behavioral-eval-runner-v1-fast-track-successor.md` §6 over `docs/design/behavioral-eval-runner-v1.md` (§8, §13, §17/§17a, §20) |
| Authoritative terms | BER-DEC-008 (backlog §13) transcribing all 35 owner-approved decisions of `docs/roadmaps/behavioral-eval-runner-wp-2b-3-authorization-decision-package.md` |

## 2. Delivered modules, schemas, and CLI (all OFFLINE)

New runtime modules under `tools/behavioral_eval_runner/judge/`:

| Module | Delivers |
| --- | --- |
| `calibration_errors.py` | Typed WP-2B-3 error taxonomy; closed `CalibrationStopReason` set covering the BER-DEC-008 stop conditions (model-identity mismatch, telemetry unavailable, credential missing, proxy/TLS/base-URL interference, SDK pin/retry violations, owner-approval pending, holdout not frozen, deadline exceeded, concurrency violation) |
| `calibration_credential.py` | Process-scoped consume-once credential handle: redacted `repr`/`str`, removal from the process environment on first read, missing ⇒ STOP; implemented but NEVER exercised with a real secret in Stage A1 (dummy sentinels only in tests) |
| `calibration_transport.py` | Pinned terms as code: OpenAI Responses API; exact snapshot `gpt-5.5-2026-04-23`; SDK `openai==3.0.0` with the BER-DEC-008 wheel/sdist SHA-256; egress `api.openai.com:443`; connect 15 s / total 300 s; SDK-owned retries pinned to ZERO. Lazy SDK import (importing the module loads no network machinery); client factory fails closed on proxy/TLS/base-URL environment interference BEFORE construction, builds the inner HTTP client with `trust_env=False`, and verifies `max_retries == 0` and the exact base URL after construction. The CLOSED request-kwargs set (exactly `model/instructions/input/text/reasoning/store/background/max_output_tokens`; every tool/function/search/code/conversation/sampling/cache/service channel is a named FORBIDDEN key), the strict structured-output verdict schema mirroring `StructuredVerdict`, and the PROVEN pre-dispatch 8,000-input-token ceiling: a byte-based upper bound over the COMPLETE serialized request surface (instructions + rendered input + the canonical `text`/schema block + model + reasoning) resting on the byte-level-BPE property token_count ≤ UTF-8 bytes, plus a documented 64-token framing margin — dispatch above 8,000 is impossible, conservative false rejection is permitted (measured: all 40 development items bound at 4,744–5,402 tokens) |
| `calibration_ledger.py` | EVENT-SOURCED, SINGLE-FILE durable work-package ledger with integer nano-USD money (input 5,000 / output 30,000 / cached input 500 nano-USD per token; price-verification date recorded). One append-only hash chain holds GENESIS / SEGMENT_OPENED / ATTEMPT_STARTED / ATTEMPT_TERMINAL / ACTIVE_SEGMENT_BEGIN·END / SEMANTIC_OUTCOME / DEADLINE_STOP events. Every reservation durably appends a write-ahead STARTED event BEFORE any transport use; a later execution segment REOPENS the same file, verifies the complete chain, and continues every total (creating a fresh file requires an explicit, durably recorded first-segment declaration — silent resets are impossible). STARTED-without-terminal orphans are detected on reopen, counted against every ceiling at reserved worst case with billing UNKNOWN, their identities never reused, and further reservation STOPS pending owner review. Attempt ids are run-prefixed and globally unique across segments; retry linkage is durable. Pre-dispatch reservations enforce: 200 judgment attempts (inclusive of transport retries), 1 metadata request, 201 total, 2 attempts per logical judgment, 8,000 input / 25,000 development output tokens, USD $175 total AND single-day ceilings with stop-BEFORE-cap worst-case projection (worst permitted token path USD $158). Missing usage telemetry writes a worst-case-charged `telemetry_missing` entry and STOPS; boundary-uncertain failures are `billing_unknown` at reserved worst case — NEVER known zero; provider-reported input-token overshoot, output tokens above the reserved ceiling, and an actual charge breaching a hard ceiling each record honestly and STOP. Active-execution deadlines (90 min development / 4 h holdout / 6 h whole-run; OWNER_WAIT contributes zero) are persisted in the same chain and survive restarts |
| `calibration_dataset.py` | The SYNTHETIC CANDIDATE dataset contract: exactly 160 distinct items over the ten semantic-bearing controls (A, B, C, D, G, H, I, J, N, O); 16 per control (4 development = 2 PASS + 2 FAIL; 12 sealed holdout = 6 + 6); ≥40 holdout CRITICAL expected-FAIL; ≥40 holdout injection/role-confusion items with ≥20/≥20; CRITICAL/adversarial overlap reported separately with no double-counting; distinct-transcript enforcement; `candidate_expected_label` vocabulary with `owner_label_status = PENDING` (candidate labels are explicitly NOT human labels); hash-bound split map; development-only selection; holdout items unreachable without the owner freeze authorization; the label-free `CalibrationItemContent` judge-facing projection on which expected labels are structurally unrepresentable (label-bearing keys raise) |
| `calibration_envelope.py` | Calibration envelopes of the EXACT WP-2B-2 envelope shape (same version, policy identity, TRUSTED contract-derived control context, base64 canonical-JSON untrusted `transcript` channel, item-manifest input binding) — the existing `validate_request_envelope_binding` and `parse_judge_output` apply unchanged |
| `calibration_gates.py` | The hard Stage-A1 gate: a missing or PENDING owner label-approval artifact mechanically blocks every provider judgment call; APPROVED artifacts must hash-bind the exact dataset, split map, and labeling guide; authorization objects are constructible ONLY through the gate functions; OWNER_WAIT authorizes nothing; sealed-holdout execution additionally requires the decision-35 freeze artifact (all frozen-artifact hashes present; holdout `max_output_tokens` within [8,192, 25,000]) |
| `calibration_provider.py` | The calibration-only judge client: constructible only with a gate-issued authorization AND the DURABLE work-package ledger (an in-memory ledger is refused — no unaccounted dispatch path exists); no optional clock — the persistent stage and whole-run deadlines are checked from the ledger's durable active-time state before EVERY external attempt including the runner retry; refuses requests without the authorized candidate-dataset identity or outside the gate-derived development item set; envelope bytes must hash-bind the request BEFORE any reservation or provider interaction; concurrency 1; per-attempt durable STARTED → dispatch → terminal record; the Aegis runner owns EXACTLY ONE connection/transport retry, each attempt uniquely ledgered with durable retry linkage; semantic FAIL verdicts, malformed output, refusals, and incomplete responses NEVER retry; returned-model mismatch ⇒ recorded entry + STOP (no silent alias normalization; also enforced on the metadata response); HTTP 401/403 ⇒ STOP; unclassified transport exceptions ⇒ recorded `billing_unknown` attempt + typed STOP; incomplete ⇒ `JUDGE_ERROR`, never parsed; a completed usable output is durably recorded as `OUTPUT_RECEIVED_UNVALIDATED` and the VALIDATED_PASS/FAIL/ABSTAIN (or `JUDGE_ERROR_*`) terminal semantic event is appended ONLY after the canonical `parse_judge_output` + full request/envelope binding validation; the single authorized read-only metadata surface uses the same durable lifecycle, ledger-capped at exactly one, NOT called in Stage A1 |

Schemas (`1.0.0-wp2b3`, draft-07, `additionalProperties: false`):
`calibration-candidate-dataset.schema.json`, `calibration-owner-approval.schema.json`,
`calibration-ledger-entry.schema.json` — enum sets cross-checked against the code by
tests and `self-check`.

Integration files modified (authorized scope only): `__init__.py` (additive WP-2B-3
constants), `cli.py` (offline `validate-calibration-dataset` and `calibration-status`
commands — repository-safe hashes/counts/status output only — plus six new self-check
items), `tests/test_static_safety.py` (the ONE narrow boundary change: the runtime
"openai" fragment ban now carries an exact-path allowlist for
`judge/calibration_transport.py` and `judge/calibration_provider.py` ONLY, and asserts
those files exist), `README.md` (WP-2B-3 section). No other existing repository file
was modified; skills, evals, workflows, gate-guard, the validator, the Scenario A
runbook, design docs, the backlog/governance log, and all prior evidence summaries are
untouched.

## 3. Pinned SDK environment (isolated; no provider call)

- PyPI release metadata for `openai` 3.0.0 was re-verified before installation: wheel
  SHA-256 `8d32ac3a6647a66910d6cb8a64f0fa5a6c823604b6e82db83d9d055c6709bd51` and sdist
  SHA-256 `ffd00ef1678d70957e1f1ed98d5bfcf1d661f41ea4482f22e7d0144a66435a49` — EXACT
  matches to BER-DEC-008 decision 29.
- The wheel was downloaded, hash-verified against the authorized value, and installed
  OFFLINE from the verified local artifact set into an isolated implementation-local
  virtual environment (no global installation; declared runtime dependencies only; a
  full dependency SHA-256 inventory and `pip freeze` lock are retained in the external
  evidence root).
- Package-registry access (pypi.org) for metadata + download is disclosed in
  accounting; it is not a model or provider API call. Requests to `api.openai.com`: 0.
- The pinned SDK source was inspected directly: `DEFAULT_MAX_RETRIES = 2` (hidden
  SDK retries exist by default and are therefore explicitly pinned to 0 in the client
  factory); `max_retries=0` yields exactly one transport attempt
  (`range(max_retries + 1)`); the SDK-configuration tests construct the real client
  with a dummy sentinel and prove `max_retries == 0`, the exact base URL, the 15 s/300 s
  timeouts, and `trust_env=False` — with zero network use.

## 4. Candidate dataset, labeling guide, and owner review packet (EXTERNAL ONLY)

Built by a provenance-preserved script (copy retained in the evidence root), validated
through the repository contract AND independently through the committed
`validate-calibration-dataset` CLI:

| Item | Value |
| --- | --- |
| Dataset | `calibration.scenario_a.wp2b3-candidate` v`1.0.0-wp2b3-candidate.1` — 160 distinct synthetic items |
| Dataset SHA-256 | `f646b4b9ba6f71e3009bbec6b83538dfe0bd9da1c8c56b7174360da3b5d2b160` |
| Split map SHA-256 | `08078227408b9a560afb2e5614019ef0280edda353f9d233c95adfaf4d099fca` |
| Labeling guide | v`1.0.0-wp2b3`, SHA-256 `05708c4052ca2a7f4a173b196dd553237741710bd09db9ff21bc7e835f9fbc2d` — derived ONLY from the approved WP-2B-2 rubric/control contracts (exact rubric text and contract hashes quoted; no rubric changed) |
| Composition | 40 development (2 PASS + 2 FAIL per control) / 120 sealed holdout (6 + 6 per control; 60/60) |
| CRITICAL floor | 40 holdout items with `risk_class=CRITICAL` and candidate FAIL (floor ≥40 met exactly) |
| Adversarial floor | 40 holdout injection/role-confusion items (20 candidate PASS / 20 candidate FAIL; 20 PROMPT_INJECTION / 20 ROLE_CONFUSION) |
| CRITICAL ∩ adversarial | 10 (reported separately; the holdout remains 120 distinct items — no double-counting) |
| Owner label status | **PENDING** — candidate labels are Claude-proposed and are NOT human labels; Peter Nguyen is the sole human gold-label authority per the BER-DEC-008 decision-34 exception |
| Content constraints | synthetic only — no customer/personal/production data, no secrets, no credentials, no private source, no private chain-of-thought |

The owner label-review packet (JSON + human-readable MD) carries the dataset/guide/
split hashes, exact counts and denominators, the complete 160-item inventory with
per-item candidate label + concise rationale + transcript hash, the mechanical
validation results, one explicit design note for owner veto (the 40 development items
are deliberately non-adversarial), and an empty ambiguity-flag list.

## 5. Tests and validation (actual results at the ORIGINAL implementation head)

*(Historical record of the originally pushed head `52805dc4…`; the PR #88
correction pass results at the corrected head are in §5b — 832/0/0.)*

Local runner tests are developer-machine evidence — GitHub CI validates only the
repository gates and does not run the runner suite.

- RED first: all seven new test modules were written and run BEFORE implementation
  (import/attribute failures + allowlist failures recorded); RED and GREEN logs are
  retained under the external evidence root.
- Full runner suite (system Python, SDK absent):
  **794 tests, 0 failures, 0 errors, 9 skipped** (4 pre-existing POSIX-only + 5
  SDK-configuration tests honestly skipped where the SDK is not installed).
- Full runner suite (isolated WP-2B-3 venv, pinned SDK present):
  **794 tests, 0 failures, 0 errors, 4 skipped** (ONLY the pre-existing POSIX skips —
  every SDK-configuration test executed and passed; still zero network).
- New WP-2B-3 tests: **131** across 7 modules (transport/request-closure/input-budget;
  ledger caps/pricing/telemetry/retry-linkage/append-only chain/deadlines/cross-segment
  continuity; dataset composition/distinctness/label-leak/holdout projection boundary;
  gates approval/freeze/authorized-item derivation; provider authorization/fail-closed
  mapping/runner-owned retry/holdout dispatch refusal/metadata cap+identity; static
  safety incl. the lazy-import probe; CLI) — including the 19 blocker-remediation
  regressions of §5a, all demonstrated RED first.
- Runner `self-check` ⇒ **PASS (21/21)** — the 15 prior checks plus: calibration gates
  fail closed, request-settings closure, caps/pricing exactness, dataset-contract
  enforcement, provider-fragment allowlist integrity, and calibration schema/code
  agreement.
- Census regenerated twice over the pinned snapshot ⇒ byte-identical, canonical
  SHA-256 `674017e9344c0afa2ff26539221a9ea185753ceef5bfe8c9040514a54004a22a`
  (unchanged — no corpus change).
- Validator self-tests ⇒ **91 PASS** (untouched). `validate-skills` ⇒ **184 valid,
  0 warnings** (untouched). `git diff --check` clean.
- Static safety: the AST scan (`scan_package_sources`) reports zero violations over
  the whole package including every new module; importing the full calibration stack
  loads no network module AND does not import the SDK (lazy-import probe); the
  "openai" fragment appears in exactly the two allowlisted adapter modules; every
  other provider fragment remains banned everywhere; no `shell=True`, no dynamic
  exec, no install-command literal, no new subprocess/ctypes import, no
  `verify=False`/`trust_env=True` literal, no credential-shaped literal.

## 5a. Bounded adversarial review and remediation

Per the task's review protocol, ONE bounded read-only exact-diff reviewer examined the
full implementation diff across nine lenses (provider boundary; hidden retry/accounting;
credential leakage; model identity; token/cost reservations; label leakage; holdout
leakage; static-safety weakening; unauthorized live/generic execution). It confirmed the
provider boundary, retry/accounting, credential, model-identity, label-leak, and
static-safety dimensions sound, and proposed **two blockers**; both were verified against
the exact code under the seven-point blocker test and **remediated test-first** (19 new
regression tests; full suite re-run green at 794/0/0):

1. **(Blocker) Sealed-holdout reachability.** The holdout seal was enforced only at the
   authorization-stage level and one advisory accessor: `dataset.items` was public,
   `CalibrationItemContent.from_item` accepted any split, and the provider never checked
   item membership — so a DEVELOPMENT authorization could have dispatched all 120 sealed
   items. Fixed structurally at TWO layers: `from_item` now refuses `SEALED_HOLDOUT`
   items without a gate-issued `HoldoutFreezeAuthorization`, and
   `authorize_calibration_dispatch` now REQUIRES the hash-bound dataset object, derives
   the DEVELOPMENT-only request-id set itself, and the provider refuses any request id
   outside that closed set before any reservation or provider interaction.
2. **(Blocker) Cap continuity across execution segments.** Every ledger cap was scoped
   to one in-process `CalibrationLedger`, though the OWNER_WAIT/freeze design mandates
   multiple segments — a later segment would have reset the 200-attempt/201-request/
   USD $175 ceilings to zero. Fixed: `CalibrationLedger(path, prior_ledger_paths=…)`
   verifies every prior segment's hash chain and folds prior attempts, per-judgment
   attempt history, metadata count, total spend, and per-day spend into every
   reservation check and cumulative snapshot (mirroring the WP-2B-1 `BudgetLedger.load`
   "never a reset" contract).

Non-blocking review findings adopted in the same pass: unclassified transport/SDK
exceptions during dispatch or the metadata call are now RECORDED as accounted attempts
and raise a typed `UNCLASSIFIED_TRANSPORT_ERROR` stop (no unrecorded external request,
no untyped crash); the metadata availability response's returned model is now verified
against the exact snapshot (mismatch ⇒ recorded STOP); a provider-REPORTED input-token
count above the 8,000 budget now records the honest charge and stops
(`CAP_WOULD_BE_EXCEEDED`); `consume_process_scoped_credential` defaults to the real
process environment so consume-once cannot be silently defeated by a copied mapping;
bool-vs-int reservation guards tightened.

Non-blocking findings recorded as dispositions, NOT converted into further loops
(future hardening for the Stage A2 authorization): the deadline clock is wired but
optional in the provider constructor (the Stage A2 driver must make it mandatory and
add holdout/total-run deadline checks); the owner-approval artifact is validated
structurally but carries no cryptographic owner signature (the process-scoped
credential remains the effective spend gate; a signed-approval requirement belongs to
the Stage A2 terms); the in-process Python capability-key pattern is bypassable by
trusted in-process code (standard idiom; no untrusted code path exists); the
legacy provider-fragment ban list covers the four historical fragments only
(pre-existing scope).

*(Superseded mechanisms note, recorded by the §5b correction pass: the
`prior_ledger_paths` cross-segment mechanism described above was REPLACED by the
single-file continuously-appendable ledger, and the optional deadline clock was
replaced by mandatory persistent deadlines — see §5b.)*

## 5b. Independent exact-head audit (REQUEST CHANGES) and the PR #88 correction pass

The independent ChatGPT exact-head audit of `52805dc4ea2cd3ccb11a3af79ef557a6d6d32b8d`
returned **REQUEST CHANGES**: four pre-provider-execution blocker families, one
decision-35 freeze-contract defect, and one accounting subcase, all corrected in ONE
bounded test-first pass (38 new RED-first regressions; every family's RED and GREEN
log retained in the external evidence root; the candidate dataset, split map, and
labeling guide remained byte-identical throughout):

1. **Provable pre-dispatch input ceiling.** The `ceil(len/3)` heuristic was removed
   (its names no longer exist). The gate is now `proven_input_token_upper_bound`: the
   sum of UTF-8 byte lengths of EVERY serialized textual member of the closed request
   surface — instructions, rendered envelope input, the canonical `text`/schema
   block, the model identifier, the reasoning block — plus a documented 64-token
   framing margin, resting on the byte-level-BPE property token_count ≤ UTF-8 bytes.
   Dispatch above 8,000 is impossible; the provider-reported input overshoot check
   remains as the second defensive control. Measured against the real candidate
   dataset: all 40 development items bound between 4,744 and 5,402 tokens.
2. **Durable work-package accounting.** The ledger was rebuilt as an event-sourced
   single-file chain: durable write-ahead `ATTEMPT_STARTED` before ANY transport use
   (judgment and metadata); separate append-only terminal events; reopen-and-verify
   continuity with an explicit durably-recorded first-segment declaration (silent
   resets impossible); crash orphans detected, worst-case charged, billing UNKNOWN,
   identities never reused, further reservation stopped pending owner review;
   run-prefixed globally unique attempt ids with durable retry linkage; the
   live-capable provider REJECTS in-memory ledgers. Boundary-uncertain failures
   (timeout / connection error / HTTP status / unclassified exception) are recorded
   `billing_unknown` at the reserved worst case — never known zero; known zero
   remains only for proven-local rejections that never reserve at all.
3. **Mandatory persistent deadlines.** The optional `clock=None` parameter is gone.
   Active-execution segments are events in the durable chain; the provider checks the
   stage limit AND the 6-hour whole-run limit from that persistent state before EVERY
   external attempt, including between attempt 1 and the runner retry; restarts and
   segment transitions preserve active time; OWNER_WAIT contributes zero; a deadline
   denial appends `DEADLINE_STOP` evidence and consumes no external request. The
   4-hour holdout limit is represented and integrity-tested (no holdout execution
   exists in Stage A1).
4. **Validated semantic outcomes.** A completed usable output is durably recorded as
   `OUTPUT_RECEIVED_UNVALIDATED`; the terminal semantic event
   (`VALIDATED_PASS/FAIL/ABSTAIN` or `JUDGE_ERROR_*`) is appended ONLY after the
   canonical `parse_judge_output` plus complete request/envelope binding validation.
   Ten tamper regressions prove a raw `"verdict": "PASS"` with any wrong field
   (request id, control, rubric id/hash, manifest, judge identity, schema version,
   evidence refs, cross-field rules, missing field) never becomes a durable semantic
   PASS and never retries.
5. **Complete freeze integrity (decision 35).** `HoldoutFreezeArtifact` now carries
   `freeze_contract_sha256` — a canonical digest over the COMPLETE artifact binding
   `reasoning_effort` and the owner-selected holdout `max_output_tokens` together
   with all thirteen frozen-artifact hashes; any post-hoc change or missing binding
   invalidates the authorization. Example artifacts remain explicitly non-owner.
6. **Overshoot subcase (folded into family 2).** Provider-reported output tokens
   above the reserved ceiling and an actual recorded charge breaching the total or
   single-day ceiling are each recorded honestly and STOP further execution.

Corrected-head validation: full suite **832 tests, 0 failures, 0 errors** (system
Python: 9 skips = 4 pre-existing POSIX + 5 SDK-absent; pinned-SDK venv: 4 POSIX skips
only — every SDK-dependent correction test executed); `self-check` **PASS 21/21**;
census ×2 byte-identical `674017e9344c0afa2ff26539221a9ea185753ceef5bfe8c9040514a54004a22a`;
validator **91 PASS**; `validate-skills` **184/0**; `git diff --check` clean; the
static-safety allowlist is UNCHANGED (still exactly the two adapter modules); no new
dependency; zero provider/model/metadata calls and zero credential access throughout
the correction. A focused read-only exact-corrective-diff reviewer (ten-dimension
closed scope) ran before commit: **BLOCKERS: 0 — all ten dimensions SOUND**, with
four non-blocking residuals recorded as dispositions (no post-review code change; the
committed corrective diff is byte-identical to the reviewed diff): **F4, the one item
not to drift and a NAMED STAGE A2 PRECONDITION — no production code opens an active
deadline segment yet, so the mandatory 90-minute/6-hour clocks accrue nothing until
the Stage A2 driver opens/refreshes the active segment (or the provider is made to
fail closed when none is open) with epoch-based timestamps; active time does NOT
accrue automatically**; F1 — the durable write-ahead append is flushed but not
fsynced (OS/power-loss window; one-line fix named as a first-live-authorization
precondition); F2 — per-event-kind schema `required` strictness for terminal
accounting fields; F3 — the metadata unclassified-exception path records known-zero
where the invariant's letter says billing-unknown (provably identical money; flag
flip at Stage A2). Full report in the external evidence root.

## 6. Model and spend accounting (Stage A1)

- provider/model judgment calls: **0**
- metadata/control calls: **0** (the single authorized `GET /v1/models/…` remains
  unused)
- credential access (real): **0** (dummy sentinels only in tests)
- external provider spend: **USD $0**
- development judgments executed: **0 of 40** (NOT STARTED)
- sealed-holdout judgments executed: **0 of 120** (NOT OPENED)
- package-registry access (disclosed; not a provider call): PyPI metadata + wheel
  download for the authorized `openai==3.0.0` install into the isolated venv
- implementation-session AI activity (authoring Claude session + bounded read-only
  review agents) is implementation-session activity per the standing BER terms — it is
  not Behavioral Eval Runner dispatch and constitutes no calibration evidence.

## 7. Non-claims and boundaries (binding)

- **No measured calibration exists or is claimed.** Nothing here says anything about
  any real judge's quality.
- **OWNER_LABEL_APPROVAL: PENDING.** No provider judgment call is possible while
  PENDING, and the runner enforces this mechanically; Claude cannot and does not
  certify the candidate labels as human-approved.
- **OD-1 remains OPEN; WP-2B-4 remains BLOCKED**; no baseline-eligible semantic
  verdict exists or can exist from this work.
- The generic/live denial boundary is intact: `DisabledJudgeProvider` denies every
  dispatch; no Scenario A system-under-test execution path, no generic-corpus path,
  no CI/workflow integration, and no deployment exists or was added.
- The sealed holdout was not opened; expected labels are structurally absent from
  every judge-facing surface; holdout execution requires the future owner freeze.
- The next gate is: independent exact-head audit → Peter Nguyen's human label
  approval → the 40-item development calibration → the OWNER_WAIT token-cap freeze.

## 8. External evidence root

Created under the BER-DEC-008 decision-24 terms before implementation: encrypted
volume verified through two independent OS signals; ownership marker binding
BER-DEC-008 / WP-2B-3 / repository / branch / authorization merge SHA + tree /
provider + model snapshot / creation + 30-day expiration / classification
(INTERNAL TECHNICAL CALIBRATION EVIDENCE) / preserve-on-failure / marker-gated
cleanup policy; ACL inheritance disabled with the owner's authorized account and
SYSTEM only; the path chain validated reparse-free; the root outside every Git
repository. It holds the baseline and final validation logs, RED/GREEN logs, SDK
integrity + lock records, the candidate dataset + split map + labeling guide + owner
label-review packet + CLI validation outputs, the builder-script provenance copy,
timing records, and the final SHA-256 evidence inventory. Cleanup is not authorized;
evidence is preserved for owner review within the 30-day retention window. No
credential exists anywhere under the root.
