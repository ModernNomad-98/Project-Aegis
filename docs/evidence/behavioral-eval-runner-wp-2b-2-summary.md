# Behavioral Eval Runner — WP-2B-2 Scenario A Grading Stack: sanitized implementation summary

**Scope: the authorized NON-LIVE Scenario A Grading Stack — deterministic graders over
recorded synthetic evidence, the non-live semantic-judge scaffold, and the
deterministic/mock calibration harness. ZERO runner-generated, grading-stack-generated, or
test-harness-generated model/provider dispatches; ZERO actual judge/provider calls; NO
measured calibration; NO live Scenario A; NO generic corpus; NO CI wiring.**

This file is repository-safe: it contains no personal username, no personal path, no
secret, no environment dump, no raw test log, and no private machine detail. Full build
evidence (RED/GREEN test logs, validation logs, census outputs, timing) is retained
externally under the BER-DEC-007 build-evidence root and is not committed.

## 1. Authorization

| Item | Value |
| --- | --- |
| Authorization record | BER-DEC-007 |
| Authorization PR | [#84](https://github.com/ModernNomad-98/Project-Aegis/pull/84) — MERGED |
| Authorization merge SHA | `1145cb75d79bc6ab13876438527235c93320278b` |
| Authorization merge tree SHA | `47a013fe4de3820f828887dc857dc441edc50272` |
| Authorized work package | WP-2B-2 — Scenario A Grading Stack (non-live) |
| Implementation branch | `feat/behavioral-eval-runner-2b-2-scenario-a-grading-stack` |
| Implementation base SHA | `1145cb75d79bc6ab13876438527235c93320278b` |
| Implementation base tree SHA | `47a013fe4de3820f828887dc857dc441edc50272` |
| Authoritative design | `docs/design/behavioral-eval-runner-v1-fast-track-successor.md` (§3–§4) over `docs/design/behavioral-eval-runner-v1.md` (§5c, §5d, §6, §7, §8, §9, §13, §18) |
| Authoritative continuation register | `docs/roadmaps/behavioral-eval-runner-backlog.md` (BER-DEC-007, §13) |

The implementation branch was created directly from the authorization squash-merge commit
and tree, never from a later moving `main`.

## 2. Delivered modules and schemas

All new code is Python standard library only — no dependency file, no package
installation, no network library, no provider SDK, no native FFI.

### Deterministic graders — `tools/behavioral_eval_runner/graders/`

| Module | Delivers |
| --- | --- |
| `contract.py` | The versioned Scenario A control A–Q classification contract (17 controls, each with source section, requirement, disposition, evidence contract, oracle/rubric refs, failure reason codes, fail-closed ambiguity behavior, D9 owner-sign-off flag, anchoring cases, non-claims); canonical contract hash |
| `records.py` | Typed, hash-bound `GraderResult` records (closed result states PASS/FAIL/ERROR; closed 41-value grading reason-code set reusing the WP-2B-1 vocabulary where applicable; content-bound `output_sha256`; no free-form reasoning field) |
| `_base.py` | Shared fail-closed grading envelope (malformed evidence ⇒ ERROR/EVIDENCE_MALFORMED, never a verdict) |
| `state_machine.py` | State/transition grading over the pinned STEP_00…STEP_08 states and design §9 turn classes: prior/next-state validation, permitted successors, answer-bank membership, mechanically provable repeated-loop detection, completion-state handling, broken-chain ⇒ ERROR |
| `approval.py` | Approval-boundary grading: approval present, approver identity represented, action-never-before-approval, preview→approve→append recording boundary, owner-gate-checked stage advancement, ambiguous/declined approval fails closed |
| `mutation.py` | CONTROL-SCOPED prohibited-action checks over the shared recorded evidence contract (J: unapproved file mutations + out-of-scope actions; K: package installs; L: network egress; M: git mutations; N: deploys + migrations; the full category set must be present — a missing key fails closed — and cross-category observations stay visible in the reproduction) plus the fail-closed zero-commit oracle (ports `Test-ZeroCommitCount`: a broken git check is ERROR, never a certified zero) |
| `append_only.py` | Append-only/recording checks porting the mechanical harness's content-agnostic oracles (section/row extraction, prefix property, placeholder preservation, expected-ID census, PS-006-before-PS-007 and owners-before-SS-002 ordering gates, SS-003 forbidden); run-local normalized-LF hashing only |
| `hashing.py` | Run-local preview-versus-created hashing (CRLF/CR→LF canonicalization; equality/mismatch; the API cannot accept a fixture-pinned digest and rejects one smuggled into evidence) |
| `activation.py` | Typed target/invocation-mode grading (skill never satisfies subagent expectation and vice versa; explicit mode required; Tier-1/promoted-Tier-2-with-ref identifying; unpromoted Tier-2 corroborating only; prose-only/conflicting/insufficient ⇒ ERROR/AMBIGUOUS_ACTIVATION, never a verdict) |
| `controls.py` | Control A/B/H deterministic-half oracles, runner-provided P/Q capture oracles, and the control dispatcher (`grade_control`): ERROR > FAIL precedence; a COMPOSITE/SEMANTIC control can never PASS from deterministic evidence — its non-FAIL outcome is SEMANTIC_PENDING |

### Semantic judge scaffold — `tools/behavioral_eval_runner/judge/` (NON-LIVE)

| Module | Delivers |
| --- | --- |
| `interface.py` | Judge interface: pinned `JudgeIdentity` (model/provider fields DATA ONLY), `JudgeRequest`/`JudgeResponse` identities, closed `TransportOutcome` set, abstract `JudgeClient`, and `DisabledJudgeProvider` — the only "provider", denying every dispatch with `LIVE_DISPATCH_DISABLED` |
| `policy.py` | Versioned, hashed injection-resistant system policy (untrusted-data rule, never-follow-transcript-instructions, no tools, no network, no file access, no policy reveal, no fabrication, schema-only output, abstain/JUDGE_ERROR on insufficiency) |
| `envelope.py` | Delimited untrusted-data envelope: built ONLY from stage-A input-manifest-verified artifacts via `JudgeInputGate`; base64 canonical-JSON transport encoding (delimiter text in data cannot break framing); policy text never inside; closed least-context evidence-key set (no expected-answer/answer-bank channel representable) |
| `rubric.py` | The coherent-topic rubric contract preserving the accepted rule EXACTLY ("ONE COHERENT DISCOVERY TOPIC PER TURN. / Related supporting details within that topic are allowed."); the generic control-semantics rubric for the other non-mechanical Scenario A assertions; a CLOSED rubric registry; no counting oracle of any kind |
| `mock.py` | Recorded-fixture mock judge client (returns pre-recorded responses only; zero model calls by construction) |
| `verdict.py` | Schema-validated `StructuredVerdict` (no confidence field — unauthorized by the parent design; no chain-of-thought; `offending_span` hard-capped at 500 chars) and fail-closed `parse_judge_output`: malformed/refused/timed-out/transport-failed/schema-invalid/mismatched/contradictory output ⇒ JUDGE_ERROR, never PASS or FAIL |
| `calibration.py` | The minimum versioned calibration-dataset contract (labeler as ROLE only; SYNTHETIC_MOCK provenance in this phase); deterministic metrics over recorded mock verdicts (confusion matrix, agreement, false-PASS, false-FAIL, abstention, JUDGE_ERROR, separate CRITICAL false-PASS; explicit denominators; null on zero denominator); explicit thresholds whose ONLY representable status is MOCK_UNRATIFIED (no RATIFIED value exists); threshold enforcement (under-threshold rejected, missing thresholds rejected, indeterminate metrics rejected, `baseline_eligible` always false); drift triggers (judge model/version, policy, rubric, rubric-derivation, dataset, dataset-label, verdict-schema changes) that invalidate prior mock state |

### Schemas — `tools/behavioral_eval_runner/schemas/` (6 new, `1.0.0-wp2b2`)

`grader-result.schema.json`, `judge-request.schema.json`, `judge-verdict.schema.json`,
`calibration-dataset.schema.json`, `calibration-report.schema.json`,
`scenario-a-grading-contract.schema.json` — draft-07, `additionalProperties: false`,
enum sets cross-checked against the code enums by tests and `self-check`.

### Fixtures — `tools/behavioral_eval_runner/fixtures/scenario_a/` (9 recorded synthetic files)

`append_only.json`, `transitions.json`, `approvals.json`, `mutations.json`,
`activation.json`, `controls_misc.json`, `injection_suite.json`, `mock_verdicts.json`,
`calibration_mock.json` — all marked SYNTHETIC_MOCK; none is live output, none is the
future owner-approved measured dataset, and no fixture pins are ever applied to live
output.

### Integration files modified (authorized §14.B, only as necessary)

- `tools/behavioral_eval_runner/__init__.py` — additive WP-2B-2 constants
  (`GRADING_STACK_VERSION`, `GRADING_SCHEMA_VERSION`, BER-DEC-007 identifiers); WP-2B-1
  identifiers unchanged.
- `tools/behavioral_eval_runner/cli.py` — six offline subcommands
  (`validate-grading-contract`, `grade-fixture`, `build-judge-envelope`,
  `validate-judge-verdict`, `mock-calibration`, `grading-capabilities`; no live verb
  exists) and seven new self-check items.
- `tools/behavioral_eval_runner/README.md` — grading-stack documentation.

No other existing repository file was modified. The read-only core boundary files
(`materialize.py`, `pathsafe.py`, `containment.py`, `process_control.py`, `budget.py`,
`scheduler.py`, `adapters/**`, the WP-2B-1 census artifact), the structural validator,
workflows, skills, evals, the Scenario A runbook and mechanical harness, design docs, and
the backlog are untouched.

## 3. Control A–Q classification and accounting

Every Scenario A control A–Q is accounted for exactly once in the versioned contract
(`graders/contract.py`, mirrored by `scenario-a-grading-contract.schema.json`), with the
dispositions transcribed from design §9's own grading column:

| Controls | Disposition | Deterministic oracle | Semantic component |
| --- | --- | --- | --- |
| E, F, K, L, M, P, Q | DETERMINISTIC | implemented | — |
| A, B, D, H, J, N, O | COMPOSITE | implemented (deterministic half) | SCAFFOLDED → judge scaffold; D9 sign-off flagged |
| C, G, I | SEMANTIC | — | SCAFFOLDED → judge scaffold; D9 sign-off flagged |

- No control is classified UNJUDGEABLE_AS_WRITTEN, EVIDENCE_UNAVAILABLE, or
  OUT_OF_SCOPE_FOR_WP2B2; no unjudgeable control is silently treated as PASS.
- Control F carries the explicit R1 caveat: real-host activation evidence remains
  UNAVAILABLE/UNKNOWN; the grader grades recorded synthetic typed evidence only, and
  prose-only or ambiguous evidence yields ERROR/AMBIGUOUS_ACTIVATION.
- Controls K/L/M/N (and J) carry the explicit R4 non-claim: recorded-evidence
  verification only, never host-containment proof.
- The dispatcher enforces that COMPOSITE/SEMANTIC controls never PASS deterministically
  (their non-FAIL outcome is SEMANTIC_PENDING).
- **D9 owner sign-off (Peter Nguyen) is flagged, not performed**: the coherent-topic
  grading contract and the semantic halves of A, B, C, D, H, I, J, N, O await owner
  sign-off at implementation review.

## 4. Tests and validation (actual results)

Local runner tests are developer-machine evidence — GitHub CI validates only the
repository gates (gate-guard, validator self-tests, validate-skills, DCO) and does not
run the runner suite.

- Full runner suite: `python -m unittest discover -s tools/behavioral_eval_runner/tests -p "test_*.py"`
  ⇒ **618 tests, 0 failures, 0 errors, 4 skipped (POSIX-only, pre-existing)** —
  377 baseline WP-2B-1 tests plus **241 new WP-2B-2 tests** in 16 new test modules
  (contract census/serialization + oracle/reason-code agreement; grader-record integrity
  incl. case-scoped assertion identity; per-grader good/bad fixture truth tables;
  state-transition truth table; approval boundaries incl. type-confusion fail-closed;
  control-scoped prohibited mutations + fail-closed zero-commit + dispatcher round trips
  for J/K/L/M/N; append-only/ordering gates incl. shadow-section and untyped-semantics
  fail-closed; run-local hashing incl. the no-fixture-pin guards; typed-target/mode
  activation incl. prose-only ⇒ ERROR; control dispatch incl. composite-never-passes;
  judge scaffold (policy/interface/mock/rubric/verdict incl. bounded verdict_id);
  envelope construction + stage-A gate enforcement incl. duck-typed-gate rejection; the
  12-class injection suite; mock calibration metrics/thresholds/drift incl. mandatory
  schema_version; schema/code agreement; runtime no-network import probe for the grading
  stack; CLI and self-check).
- RED-first discipline: every component group was demonstrated RED against the
  unimplemented behavior before implementation; RED and GREEN logs are retained under the
  external evidence root.
- Runner self-check ⇒ **PASS (15/15 checks)** — the 8 WP-2B-1 checks plus:
  grading enum closure, grading schema/code agreement, contract completeness,
  deterministic fixture reproducibility, judge-provider absence/denial, judge-envelope
  security invariants, and mock-calibration threshold behavior.
- Census reproducibility: two regenerations over the pinned snapshot
  (`--ref fc98ee6…`) ⇒ byte-identical, canonical hash
  `674017e9344c0afa2ff26539221a9ea185753ceef5bfe8c9040514a54004a22a`, byte-equal to the
  committed census blob (`git hash-object` match). No corpus change.
- Validator self-tests ⇒ **91 PASS** (untouched).
- `validate-skills` ⇒ **184 valid, 0 warnings** (untouched).
- Static safety (AST-based, extended automatically over the new packages): no forbidden
  import (network/ctypes/asyncio), no `shell=True`, no dynamic exec, no install-command
  literal, subprocess only in the pre-existing allowlisted modules; no provider SDK; no
  live-session launch path; no generic-corpus execution path.
- Whitespace (`git diff --check`) clean; no `.pyc`/`__pycache__` residue; only
  authorized paths changed.

## 5. Model and spend accounting

- runner-generated model/provider dispatches: **0**
- grading-stack-generated dispatches: **0**
- test-harness-generated dispatches: **0**
- actual judge/provider calls: **0**
- runner-generated live Claude Code sessions: **0**
- external model/API spend: **USD $0**
- package installations: **0**
- network use: none except the read-only Git/GitHub operations required to clone, verify
  authorization state, push, and open the PR.

Implementation-session AI activity (distinct from runner dispatch, per BER-DEC-007): the
authoring Claude Code session plus **4 bounded read-only review agents** (three finding
lenses — Scenario A semantics/A–Q completeness, injection resistance/fail-closed
behavior, schema-integration/scope compliance — and one refutation/consolidation
reviewer). This activity is not Behavioral Eval Runner dispatch, is not counted against
the runner's zero-dispatch budget, and constitutes no behavioral or calibration
evidence.

## 5a. Bounded adversarial review and remediation

Before commit, a bounded exact-code review ran per the authorization's review protocol:
three read-only finding reviewers (Scenario A semantics/A–Q completeness; injection
resistance/evidence integrity/fail-closed behavior; schema-runtime integration/
determinism/phase-scope compliance) and one read-only refutation/consolidation reviewer —
four review agents total, implementation clone only, no evidence-root or memory access.

Confirmed findings, all remediated test-first with the full suite re-run green:

1. **(Blocker)** The shared mutation oracle stamped every result as control K while the
   contract declared it for J/K/L/M/N — controls J/L/N were ungradable through their
   declared oracle. Fixed by making `grade_mutations` control-scoped (per-control
   category map, results carry the graded control's identity, dispatcher round-trip
   tests added for J/K/L/M/N).
2. **(Blocker)** A duplicate section header matching a graded section could shadow the
   real section in the append-only extractor (tampered history could pass). Fixed:
   duplicate matching headers now fail closed as EVIDENCE_MALFORMED.
3. **(Blocker)** `semantics` values were key-checked but not type-checked; a string
   `forbidden_snapshot_ids` iterated as characters and silently disabled the
   forbidden-snapshot gate. Fixed: full type validation of semantics and
   `expected_final_ids` values (fail closed).
4. Non-string `approval_id`/`owner_gate_record_ids` crashed instead of failing closed —
   now EVIDENCE_MALFORMED.
5. `verdict_id` was an unbounded free-form field — now a bounded identifier
   (1–128 chars, `[A-Za-z0-9._:-]`) in code and schema.
6. `CalibrationDataset.from_dict` silently defaulted a missing `schema_version` — now
   rejected; the mock fixture carries it explicitly.
7. `GraderResult.assertion_uid` was not bound to the record's own `case_uid` — now
   enforced.
8. Contract `failure_reason_codes` disagreed with the codes the named oracles can raise
   (controls E, O, P; unreachable codes declared; state-machine oracle unregistered) —
   contract corrected, two unreachable enum members removed, and a new
   oracle/reason-code agreement test pins the mapping both directions.
9. The envelope gate was duck-typed and base64 decoding unvalidated — now an
   `isinstance` contract on `JudgeInputGate` and validated base64/UTF-8 decoding.
10. A runtime no-network import probe was added for the grading-stack modules
    (mirroring the WP-2B-1 probe).

Reviewer observations assessed and NOT adopted (recorded dispositions): binding
`JudgeRequest`→envelope verification inside `parse_judge_output` and artifact-role-scoped
envelope keys (future WP-2B-4 integration hardening; the stage-A gate and closed key set
remain the enforced boundary — noted in §7); a mandatory final-version Stage-3 snapshot
check (partial recorded sequences are valid grading evidence; the ordering gates and
append-only prefix already reject dishonest sequences); calibration TRAIN/HOLDOUT split
breakdown in metrics (the split is represented per the contract; per-split metrics belong
to the future measured gate).

## 6. Non-claims and boundaries (binding)

- **No measured judge calibration exists or is claimed.** The calibration harness proves
  metric computation and threshold enforcement over recorded deterministic inputs only.
- **OD-1 remains OPEN**; no threshold is ratified; the only representable threshold
  status is MOCK_UNRATIFIED; nothing can be baseline-eligible.
- **R1** remains UNAVAILABLE/UNKNOWN (activation grading is over recorded synthetic
  evidence; prose is never activation). **R2** remains BLOCKED (no judge pinned, no
  provider adapter exists). **R4** remains INCOMPLETE/BLOCKED (mutation grading verifies
  recorded evidence contracts, never host containment). **R5** remains
  INCOMPLETE/BLOCKED (unchanged by this work).
- **WP-2B-3 (Measured Judge Calibration and OD-1 Ratification Gate) is not started** and
  remains BLOCKED. **WP-2B-4 (live suite) and WP-2B-5 (generic corpus) are not started.**
- No live dispatch: every dispatch path is absent or denies with
  `LIVE_DISPATCH_DISABLED`; no live Scenario A execution occurred; no generic corpus was
  executed; no CI/workflow integration was made.
- The Scenario A runbook, mechanical harness, skills, evals, validator, and gates are
  unchanged; fixture-manifest digests are never applied to live output.
- This summary does not mark WP-2B-2 DONE in the durable backlog; that status change
  belongs to a later reviewed governance closeout.

## 7. Known limitations

- The semantic halves of controls A, B, C, D, G, H, I, J, N, O are SCAFFOLDED contracts:
  they can be graded only when a future, separately authorized measured-calibration gate
  (WP-2B-3) and live phase (WP-2B-4) exist. In this phase they yield SEMANTIC_PENDING —
  never a verdict.
- The activation grader's PASS results apply to recorded synthetic Tier-1/promoted-Tier-2
  evidence only; no real-host activation signal exists (R1).
- The questionnaire-dump deterministic screen (control H) is a conservative mechanical
  proxy (enumerated question lines); topic coherence itself remains semantic.
- The mock calibration fixtures are synthetic; their metrics say nothing about any real
  judge.
- `parse_judge_output` validates verdict↔request self-consistency and verdict evidence
  references against the caller-supplied envelope key set; hash-binding the request to
  the rendered envelope object end-to-end is a WP-2B-4 integration step, recorded as a
  limitation, not claimed here.
- The JSON Schemas remain the portable specification; the runtime contract is enforced by
  the dataclass validators (consistent with WP-2B-1's recorded decision; no dependency
  was added).
- The WP-2B-1 Windows residuals (owner findings B/C/E — ambiguity-inventory binding,
  Windows reparse/TOCTOU write race, Windows descendant cleanup) are unchanged and remain
  OPEN owner decisions; nothing here claims them solved.

## 8. Owner decisions required at implementation review

- **D9 sign-off (Peter Nguyen):** the Scenario-A-scoped grading contracts — the
  coherent-topic rubric contract (`rubric.scenario_a.coherent_topic.v1`, rule preserved
  exactly) and the generic control-semantics rubric for the other non-mechanical
  Scenario A assertions — plus the control A–Q classification table itself
  (`graders/contract.py`).
- Accept or reject the WP-2B-2 schema shapes (`1.0.0-wp2b2` set).
- Accept the recorded-evidence contracts used by the deterministic graders (the fixture
  evidence shapes in §2) as the Scenario A grading-evidence interface for the future
  WP-2B-4 live suite.
- Accept or reject this implementation as satisfying the BER-DEC-007 non-live scope.

## 9. Evidence root

External build-evidence root (BER-DEC-007 terms): created before implementation with the
ownership marker binding BER-DEC-007/WP-2B-2/branch/base SHA + tree, a 30-day expiration,
ACL inheritance disabled, access restricted to the owner's authorized Windows account and
SYSTEM (no Everyone/Users/Authenticated Users), no reparse point in the validated path
chain, and the root outside every Git repository. It holds the baseline and final
validation logs, RED/GREEN cycle logs, census reproduction outputs, and timing records.
Cleanup is not authorized in this pass; evidence is preserved for owner review within the
retention window. No personal username or profile path appears in repository-safe output.
