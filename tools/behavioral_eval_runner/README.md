# Behavioral Eval Runner — WP-2B-1 offline core + WP-2B-2 grading stack

The NON-LIVE control plane and minimum guardrails of the Project Aegis
Behavioral Eval Runner, authorized by **BER-DEC-006**
(authorization PR #82, squash merge `fc98ee6bf59bb516064be62ed8c5dc8861c92697`),
implementing the 2B-1 row of
[`docs/design/behavioral-eval-runner-v1.md`](../../docs/design/behavioral-eval-runner-v1.md) §19 —
plus the NON-LIVE **WP-2B-2 Scenario A Grading Stack**, authorized by
**BER-DEC-007** (authorization PR #84, squash merge
`1145cb75d79bc6ab13876438527235c93320278b`), implementing the v1.1
fast-track successor
([`docs/design/behavioral-eval-runner-v1-fast-track-successor.md`](../../docs/design/behavioral-eval-runner-v1-fast-track-successor.md)) §3–§4.

## Hard boundaries (Outcome B)

- **0 model/provider dispatches, 0 live Claude Code sessions, USD $0 spend.**
  No dispatch path exists; the Claude Code adapter denies every session with
  `LIVE_DISPATCH_DISABLED`.
- **R1–R5 are NOT technically solved here.** Real-host activation observation
  (R1), judge calibration (R2, BLOCKED; OD-1 OPEN), cost observability (R3),
  containment (R4), and execution-profile isolation (R5) all remain
  UNAVAILABLE/UNKNOWN and are reported that way.
- **No live Scenario A, no generic eval execution, no CI wiring.** Python
  standard library only; no dependencies.
- Census-proposed risk classes are **PROPOSED / NOT OWNER-RATIFIED** (OD-3).
- **WP-2B-2 grading stack is NON-LIVE:** deterministic graders grade RECORDED
  synthetic evidence only; the semantic judge is a scaffold with NO provider
  implementation (the only provider object denies with
  `LIVE_DISPATCH_DISABLED`); calibration is a deterministic/mock harness with
  MOCK/UNRATIFIED thresholds only. Zero runner-, grading-stack-, or
  test-harness-generated model/provider dispatches; zero actual judge calls;
  **no measured calibration; OD-1 OPEN; R2 BLOCKED; WP-2B-3/2B-4 not started.**

## What is here

| Module | Delivers |
| --- | --- |
| `enums.py`, `models.py`, `schemas/` | Versioned closed enum sets and strict records (`attempt_state` incl. honest `UNRUN` default; `aggregate_verdict` + `aggregate_blocker`; coverage metrics) |
| `canonical.py`, `identity.py` | Canonical JSON + SHA-256; globally unique `case_uid`/`assertion_uid`/attempt identities |
| `census.py` | Implementation-time corpus census from the pinned Git snapshot (design §3 items a–k) |
| `runtime_surface.py` | Fail-closed runtime-file classification (`runtime_required` / `control_plane_only` / `ambiguous_needs_owner_review`) |
| `pathsafe.py` | Shared strict relative-path validation (traversal / drive / ADS / device-name / trailing-dot) and reparse-safe joins used by the materializer and evidence writer |
| `materialize.py` | Immutable Git-object materializer: two separated surfaces + product fixture, three hashed manifests, full-shipped-corpus rule, partial-install scoping. Git calls resolve the binary, disable remote protocols and system/global config, require hex SHAs, and pass `--end-of-options` |
| `preflight.py` | Capability/fixture preflight — missing setup never becomes behavioral FAIL |
| `execution_profile.py` | §5e profile representation; real host honestly UNAVAILABLE/UNKNOWN; baseline-eligibility marking |
| `containment.py`, `process_control.py` | Fail-closed containment interfaces, mock/synthetic test boundary, timeout + process-tree emergency kill |
| `budget.py`, `scheduler.py` | Pre-dispatch reservation ledger (hash-chained + checkpoint-anchored, restart-safe, empty/uncapped-dimension denial, atomic reconcile with drift fail-safe, enforced wall-clock deadline, kill switch) + deterministic risk-aware, prefix-exhaustion-safe scheduler with typed reverse edges |
| `aggregation.py` | Immutable attempts, N/quorum truth table, blocker precedence, orthogonal quarantine |
| `evidence.py` | Two-stage finalization with detached marker; fail-closed integrity verification |
| `reporting.py` | Deterministic reports with complete coverage metrics and no-unearned-PASS enforcement |
| `adapters/` | Host-adapter interface + the non-live Claude Code adapter |
| `cli.py` | `census`, `validate-record`, `materialize`, `preflight`, `schedule`, `aggregate-fixture`, `verify-evidence`, `capabilities`, `version`, `self-check`, plus the offline WP-2B-2 commands `validate-grading-contract`, `grade-fixture`, `build-judge-envelope`, `validate-judge-verdict`, `mock-calibration`, `grading-capabilities` — no live-run command exists |
| `graders/` (WP-2B-2) | Scenario A control A–Q classification contract with structured required-oracle sets (`contract.py`); TRUSTED hash-bound grading plans, mechanically separated from observed evidence (`plan.py`); typed hash-bound results carrying closed oracle identities and separate plan/evidence input hashes (`records.py`); deterministic graders over recorded synthetic evidence: state/transitions (`state_machine.py`), approval boundaries with ID+target-bound approvals (`approval.py`), plan-scoped prohibited mutations + fail-closed zero-commit (`mutation.py`), append-only/ordering gates with duplicate-header fail-closed extraction (`append_only.py`), run-local preview-vs-created hashing (`hashing.py`; never fixture pins), typed target/invocation-mode activation (`activation.py`), role/stage/questionnaire/capture oracles + the control dispatcher enforcing the COMPLETE required oracle set per control (`controls.py`; composite/semantic controls never PASS deterministically; incomplete/duplicate/foreign result sets are ERROR) |
| `judge/` (WP-2B-2) | NON-LIVE judge scaffold: pinned-identity interface with a deny-all provider placeholder (`interface.py`), versioned injection-resistant system policy (`policy.py`), delimited base64 untrusted-data envelope built only from stage-A-verified artifacts and carrying the TRUSTED contract-derived control context (`envelope.py`), the exact coherent-topic rubric contract (`rubric.py`), recorded-fixture mock client that verifies the envelope bytes hash-bind the request before any lookup (`mock.py`), schema-validated verdicts with fail-closed `JUDGE_ERROR` and full request↔envelope binding via `dispatch_mock_judgment`/`parse_judge_output` (`verdict.py`), deterministic/mock calibration harness with MOCK/UNRATIFIED thresholds and drift invalidation (`calibration.py`). The `build-judge-envelope` CLI emits repository-safe metadata only — no raw envelope content is printed or persisted |
| `fixtures/scenario_a/` (WP-2B-2) | Recorded SYNTHETIC good/bad grading fixtures, the injection-defense suite, mock verdicts, and the synthetic/mock calibration dataset |

Note on the final bundle: the stage-A input manifest is bound through the
final report's `run_evidence_binding.input_evidence_manifest_sha256`; the
final manifest lists the final artifacts (including the final report) and
never lists itself or the detached marker.

## Usage (offline, deterministic)

```bash
python -m tools.behavioral_eval_runner version
python -m tools.behavioral_eval_runner capabilities
python -m tools.behavioral_eval_runner self-check
python -m tools.behavioral_eval_runner census --repo . --ref <sha> --verify-baseline --out census.json --canonical
```

## WP-2B-3 Stage A1 — measured-calibration controls (BER-DEC-008; OFFLINE)

Authorized by **BER-DEC-008** (authorization PR #87, squash merge
`1c3e4931329179d9a3f9cc9ec1bb93020378c043`): the OFFLINE implementation of
the Measured Judge Calibration controls. **Stage A1 makes ZERO
provider/model/metadata calls, accesses ZERO credentials, and spends
USD $0** — every element below is exercised with fakes only.

| Module | Delivers |
| --- | --- |
| `judge/calibration_errors.py` | Typed WP-2B-3 failure taxonomy with the closed BER-DEC-008 stop-reason set |
| `judge/calibration_credential.py` | Process-scoped consume-once credential handle (redacted repr; missing ⇒ STOP; never exercised with a real secret in Stage A1) |
| `judge/calibration_transport.py` | Pinned provider terms (OpenAI Responses API, exact snapshot `gpt-5.5-2026-04-23`, SDK `openai==3.0.0` with recorded wheel/sdist SHA-256); lazy-import client factory with SDK retries pinned to ZERO, connect 15 s / total 300 s, exact `https://api.openai.com/v1`, `trust_env=False`, proxy/TLS/base-URL environment fail-closed; the CLOSED request-kwargs set (no tools/functions/search/code/conversation state; `store:false`; `background:false`; reasoning medium; default sampling); strict structured-output verdict schema; conservative 8,000-input-token gate |
| `judge/calibration_ledger.py` | Append-only hash-chained accounting in integer nano-USD; pre-dispatch reservations enforcing 200 judgment attempts / 1 metadata request / 201 total, USD $175 total and single-day ceilings (stop BEFORE any cap; worst permitted token path USD $158), per-judgment 2-attempt maximum, missing-usage-telemetry ⇒ recorded worst-case charge + STOP; 90 min / 4 h / 6 h active-execution deadlines with OWNER_WAIT excluded |
| `judge/calibration_dataset.py` | The SYNTHETIC CANDIDATE dataset contract (160 items; 16 per semantic-bearing control A,B,C,D,G,H,I,J,N,O; 40 dev 2P/2F; 120 sealed holdout 6P/6F; ≥40 CRITICAL expected-FAIL; ≥40 adversarial with ≥20/≥20; overlap reported); split-map hashing; holdout access impossible without the owner freeze; the label-free `CalibrationItemContent` judge-facing projection (expected labels structurally unrepresentable) |
| `judge/calibration_envelope.py` | Calibration envelopes of the EXACT WP-2B-2 shape (same version/policy/trusted control context), bound through the existing `validate_request_envelope_binding`; label-bearing inputs rejected |
| `judge/calibration_gates.py` | The hard Stage-A1 gate: OWNER_LABEL_APPROVAL=PENDING mechanically blocks every dispatch; gate-issued-only authorization objects; the decision-35 holdout freeze artifact contract (cap frozen in [8,192, 25,000]) |
| `judge/calibration_provider.py` | The calibration-only judge client (constructible ONLY with a gate-issued authorization): one runner-owned transport retry maximum (attempts uniquely ledgered and linked; semantic FAIL / malformed / refusal / incomplete NEVER retry); returned-model mismatch ⇒ STOP; incomplete ⇒ `JUDGE_ERROR`, never parsed; concurrency 1; the single authorized metadata request surface (capped at exactly one; not called in Stage A1) |
| `schemas/calibration-*.schema.json` | Candidate-dataset, owner-approval, and ledger-entry schema mirrors (`1.0.0-wp2b3`) |
| CLI | `validate-calibration-dataset` and `calibration-status` (repository-safe hashes/counts/status only) plus six new self-check items |

The generic denial boundary is UNCHANGED: `DisabledJudgeProvider` still
denies every dispatch with `LIVE_DISPATCH_DISABLED`, no Scenario A or
generic-corpus execution path exists, and the runtime "openai" fragment is
allowlisted for exactly the two calibration adapter modules. The candidate
160-item dataset, labeling guide, and owner label-review packet live ONLY
under the authorized external evidence root; **OWNER_LABEL_APPROVAL is
PENDING, the development calibration has NOT started, the sealed holdout is
NOT opened, OD-1 remains OPEN, and WP-2B-4 remains BLOCKED.**

## Tests

```bash
python -m unittest discover -s tools/behavioral_eval_runner/tests -p "test_*.py" -v
```

All tests are deterministic and offline: mocks, synthetic fixtures, local
subprocesses for timeout/kill tests only, temp directories under the
process-local TMP/TEMP. No network, no package installation, no model calls.
The WP-2B-3 SDK-configuration tests run only where the pinned SDK is
installed (the isolated WP-2B-3 venv) and are honestly SKIPPED elsewhere —
they still perform no network call anywhere.
