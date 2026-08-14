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
| `graders/` (WP-2B-2) | Scenario A control A–Q classification contract (`contract.py`); typed hash-bound results (`records.py`); deterministic graders over recorded synthetic evidence: state/transitions (`state_machine.py`), approval boundaries (`approval.py`), prohibited mutations + fail-closed zero-commit (`mutation.py`), append-only/ordering gates (`append_only.py`), run-local preview-vs-created hashing (`hashing.py`; never fixture pins), typed target/invocation-mode activation (`activation.py`), role/stage/questionnaire/capture oracles + control dispatch (`controls.py`; composite/semantic controls never PASS deterministically) |
| `judge/` (WP-2B-2) | NON-LIVE judge scaffold: pinned-identity interface with a deny-all provider placeholder (`interface.py`), versioned injection-resistant system policy (`policy.py`), delimited base64 untrusted-data envelope built only from stage-A-verified artifacts (`envelope.py`), the exact coherent-topic rubric contract (`rubric.py`), recorded-fixture mock client (`mock.py`), schema-validated verdicts with fail-closed `JUDGE_ERROR` (`verdict.py`), deterministic/mock calibration harness with MOCK/UNRATIFIED thresholds and drift invalidation (`calibration.py`) |
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

## Tests

```bash
python -m unittest discover -s tools/behavioral_eval_runner/tests -p "test_*.py" -v
```

All tests are deterministic and offline: mocks, synthetic fixtures, local
subprocesses for timeout/kill tests only, temp directories under the
process-local TMP/TEMP. No network, no package installation, no model calls.
