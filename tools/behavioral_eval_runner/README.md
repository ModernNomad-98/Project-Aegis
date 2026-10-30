# Behavioral Eval Runner

The **Behavioral Eval Runner (BER)** is Project Aegis's evaluation harness. It helps
maintainers find out whether an Aegis skill or agent behaves as intended on a
test case. The skills library tells an assistant how to work; this runner
inventories test cases, prepares reproducible inputs, grades recorded behavior,
and reports coverage and uncertainty. It is maintainer infrastructure, not an
application feature installed with the skills.

**Current state:** General runner and Scenario A grading commands (Scenario A
is the first control family in the design; see
[Terms and limits](#terms-and-limits)) operate on
offline or recorded synthetic data. They do not start a live assistant or
send a model request. A separate gated calibration development driver exists,
and the synthetic offline holdout-support increment was delivered in
[pull request (PR) #249](https://github.com/ModernNomad-98/Project-Aegis/pull/249).
Measured calibration has not started: replacement labels still need owner
review. No live Scenario A or general corpus run is available. The
[active backlog](../../docs/roadmaps/behavioral-eval-runner-backlog.md) records
current gates; the [design](../../docs/design/behavioral-eval-runner-v1.md)
contains the complete contract.

A **gated live-adapter enablement package** now exists under `live/` (2026-10-29,
build-only). It is **GATED, not enabled by default**: it ships the subject and
cross-vendor judge adapters, a spend ceiling with a proven hard halt, an owner
gate for real-host facts, and the `live-preflight`, `live-dry-run` and
`live-run` verbs. No live provider request has been made, no key was used and
the build spent $0; see [Live adapters are gated](#live-adapters-are-gated-not-enabled-by-default).

In this guide, a **manifest** lists prepared files or test cases and their
expected properties. A **hash** is a fingerprint calculated from file or
record bytes to detect changes; a matching hash does not approve the content.
A **fixture** is prepared test data or a recorded observation used for an
offline check. **JavaScript Object Notation (JSON)** is the file format used
for the structured examples and command inputs below.

## A normal offline workflow

1. **Inventory cases.** `census` reads a pinned Git revision and counts skill
   and trigger test cases. A pinned revision makes results reproducible.
2. **Prepare inputs.** `materialize` copies approved Git objects into separate
   test surfaces and writes hash manifests. `preflight` checks prerequisites;
   missing setup is reported as missing setup, not a behavioral failure.
3. **Plan and grade.** `schedule` makes a deterministic queue. For Scenario A,
   `grade-fixture` compares a trusted grading plan with recorded observations.
   A semantic assertion that needs a model cannot silently pass a deterministic
   grader.
4. **Verify and report.** `verify-evidence` checks the input and final bundles
   for structural integrity only; it does not accept a policy-bound bundle.
   For an opted-in policy bundle, use the Python
   `verify_local_bundle(root, require_policy=True)` entry point described
   below. Aggregation and reporting preserve unrun, uncertain and blocked
   outcomes.

For example, these safe commands report the installed version and available
capabilities, then check offline invariants. They do not run a case or contact
a model provider:

```bash
python -m tools.behavioral_eval_runner version
python -m tools.behavioral_eval_runner capabilities
python -m tools.behavioral_eval_runner self-check
```

To inventory a source revision, use a full Git commit identifier. This example
pins the 2026-09-23 owner-grant merge; use another full identifier for another
revision:

```bash
python -m tools.behavioral_eval_runner census --repo . --ref 1af342712d27d5e6ea482b3f451106b4dccaf125 --out census.json --canonical
```

This command **creates or replaces `census.json` in the current directory**.
Choose an output path deliberately, especially when working in the source
checkout. Omit `--out` to print the result without creating that file.
`--canonical` selects a stable JSON representation so the same input produces
the same serialized bytes and hash.

The main workflow commands have these input and output effects. None starts a
live assistant or sends a request to a model provider:

| Command | Reads | Writes or prints |
| --- | --- | --- |
| `census` | Skills and cases at `--ref` in `--repo`. | Prints the full census JSON without `--out`. With `--out`, creates or replaces that JSON file and prints output metadata. |
| `materialize` | Objects at the requested Git commit and expected tree, with a selected profile and workspace role. It verifies the supplied identities; it does not establish owner approval. | Copies inputs and writes three manifests under required `--dest`, which must be fresh or empty; prints a preparation record. |
| `preflight` | A required `--manifest` JSON list of case requirements and optional `--env` JSON declaring available capabilities. | Compares the declarations and prints `RUNNABLE` (eligible under those declarations) or `PRECHECK_EXCLUDED` (excluded before execution) per case, with reasons. It does not probe the host or approve a run. |
| `schedule` | Required `--selection` JSON and optional work and cost caps. | Prints a deterministic queue and budget accounting; it does not dispatch the queue. |
| `grade-fixture` | A required `--grader` selector, trusted grading `--plan`, and recorded `--evidence`. | Prints one deterministic Scenario A grader result. |
| `verify-evidence` | Bundles below required `--root`; optional `--stage` selects input, final, or both reports. Final verification also checks the linked input bundle. | Prints integrity results for the supplied evidence; it does not execute cases. |
| `live-preflight` | A live configuration, an owner gate record, and committed case data. | Prints the gate/dataset/model/ceiling/allowlist/key-presence report. **No network call and no credential value read.** |
| `live-dry-run` | The same inputs plus an empty evidence root and a cost-ledger path. | Runs the whole pipeline over mock adapters, writes the evidence bundle and cost ledger, and marks every result MOCK / SYNTHETIC_NOT_CITABLE. Zero network calls. |
| `live-run` | The same inputs, a **REAL_HOST** gate record and the two credential environment variables. | Refuses without the gate or keys. When authorized, dispatches through the vendor software development kit and halts on a model-pin mismatch or a spend-ceiling denial. |

The optional `--verify-baseline` flag checks one pinned historical census (882
behavioral cases and 858 trigger cases), counted from commit `e2f1da0` and set on
2026-08-13 in commit `72e74af`. A later revision may legitimately have different
counts. For current counts, run the `census` example above with the full commit
identifier you need and read `behavior_cases` and `discrimination_cases` (trigger
cases) under `totals`. Run each command with `--help` for required file shapes
and options.

## What each part does

| Area | Purpose and result |
| --- | --- |
| `census.py`, `materialize.py`, `preflight.py`, `runtime_surface.py` | Count cases from a pinned revision, copy required files, classify runtime files, and report missing or ambiguous prerequisites before grading. |
| `models.py`, `enums.py`, `schemas/`, `identity.py`, `canonical.py` | Define versioned record shapes, stable identities and canonical hashes. Reject invalid or unexpected fields. |
| `pathsafe.py`, `execution_profile.py`, `containment.py`, `process_control.py` | Keep paths within intended roots, describe host capabilities honestly, and expose process-control interfaces. Synthetic tests do not prove real-host containment. |
| `budget.py`, `scheduler.py` | Reserve bounded work before dispatch and build a deterministic queue. Unknown costs, absent caps or deadline violations close the gate. |
| `aggregation.py`, `reporting.py`, `evidence.py`, `evidence_policy.py`, `evidence_policy_preflight.py` | Combine attempts without an unearned pass, report coverage, write and verify a two-stage evidence chain, and optionally check its synthetic complete-bundle policy and caller-supplied host facts. |
| `graders/`, `judge/` | Grade recorded Scenario A controls against trusted plans. Deterministic graders cannot decide semantic assertions; the generic judge provider denies live dispatch. |
| `live/` | Gated live enablement: strict subject pins, the cross-vendor judge adapter behind the owner allowlist, the cost meter with a hard ceiling halt, the owner gate and the preflight/dry-run/run pipeline. All of it refuses without the gate; the default transport denies dispatch. |
| `cli.py` | Expose offline inventory, preparation, grading, evidence and status commands, plus the three gated live verbs. No live verb runs without an owner gate record. |

The command-line interface also offers `validate-record`, `aggregate-fixture`,
`validate-grading-contract`, `build-judge-envelope`,
`validate-judge-verdict`, `mock-calibration`, `grading-capabilities`,
`validate-calibration-dataset`, and `calibration-status`. These commands check
records, combine recorded attempts, check grading inputs and outputs, exercise
mock calibration, report capabilities, validate synthetic candidate data, and
report authorization status. The envelope command prints repository-safe
metadata rather than private raw content.

## Offline complete-bundle policy integration

`evidence_policy.py` provides an **opt-in Python application programming
interface (API) for synthetic fixtures and local callers**. Use
`OfflinePolicyWriter` only when every caller input and the final report has an
explicit `ClassificationDecision` with a versioned access-policy reference
and a content-specific decision reference. The ordinary `EvidenceWriter`
keeps its legacy serialization for unbound bundles; it must not complete an
already policy-bound Stage A (hash-verified input) bundle through implicit
metadata defaults.
`OfflinePolicyWriter.finalize_input` requires at least one explicitly classified
input and stamps its first evidence time from the writer's Coordinated Universal
Time (UTC) clock; callers
cannot supply a creation timestamp. `finalize_final` requires an explicit
classification decision for the report and each other final artifact.
`verify_policy_bundle` checks the existing Stage A input and Stage B
final-report hashes and detached
marker, then the content-bound decisions and one deadline: first writer-stamped
creation time plus 30 consecutive 24-hour periods. At that deadline the
checker refuses an active-bundle acceptance claim and preserves all files for
owner review. It never deletes or publishes a bundle.

For a local verification entry point, `evidence.verify_local_bundle(root,
require_policy=True)` insists on the policy path and refuses missing policy
claims; its default mode recognizes a policy-bound Stage A claim and routes to
the policy verifier. The lower-level `verify_final_bundle` remains an
integrity-only verifier for legacy callers. A policy claim must never be
silently treated as an ordinary legacy bundle.

`evidence_policy_preflight.evaluate_synthetic_host_facts` accepts a
`SyntheticHostFacts` record supplied by the caller. It does not query the
operating system. The proposed root must be a matching, normalized absolute
Portable Operating System Interface (POSIX) or Windows drive path supplied
by the caller; relative, ambiguous or
volume-root paths stop. Missing, false, contradictory or malformed assertions
about that exact path, ownership, access-control list (ACL), inheritance,
encryption or recovery-key custody return `STOP` with sanitized reason codes.
Complete, consistent assertions return `SIMULATION_ONLY`, which is **not**
real-host attestation or permission to run. The
[operator review runbook](../../docs/roadmaps/ber-bkl-009-operator-policy-runbook.md)
describes inventory, verification and owner review without deletion.

The two versioned policy receipts (`policy/stage-a.json` and
`policy/stage-b.json`) are **ordinary artifacts** in their respective
manifests. The final manifest hashes the Stage B receipt; the detached marker
hashes that manifest and the final report. The marker is not a manifest entry.
Existing `expiration_at` fields still describe **each artifact's own**
creation time plus its retention class. The opt-in receipt's
`bundle_review_at` is the distinct, controlling complete-bundle review date;
a later report does not extend it. Legacy evidence writer calls keep their
previous serialized bytes and hashes.

Run the local synthetic checks with:

```bash
python -B -m unittest tools.behavioral_eval_runner.tests.test_evidence_policy tools.behavioral_eval_runner.tests.test_evidence tools.behavioral_eval_runner.tests.test_evidence_policy_preflight
```

This checker proves internal consistency and the writer API's timestamp
source, not independent clock attestation against someone able to rewrite the
entire bundle. A cited classification decision is required and hash-bound to
content; metadata cannot prove redaction or public-release safety. Real-host
access controls, encryption, privacy review, cleanup and provider execution
remain separate gates in the [policy backlog](../../docs/roadmaps/behavioral-eval-runner-backlog.md).

## Calibration is a separate gated workflow

**Work package 2B-3** is the numbered effort to measure the semantic judge's
quality. Decision identifiers such as `BER-DEC-008` refer to owner decisions
in the [runner backlog and decision record](../../docs/roadmaps/behavioral-eval-runner-backlog.md).
Offline-tested dataset, request, accounting, credential and authorization
controls live under `judge/calibration_*.py`. The existing
`calibration_development_driver.py` remains development-only. Its default
description command reports the contract without sending a request:

```bash
python -m tools.behavioral_eval_runner.judge.calibration_development_driver --describe
```

The original approved input bytes are unavailable here. Replacement inputs
are versioned in an owner-only private repository; proposed labels still
await human review. Hidden holdout transcripts and labels must stay out of
this public repository and judge requests. See the
[replacement plan](../../docs/evidence/ber-recovery-2026-09-11/replacement-plan.md)
and [offline holdout support scope](../../docs/roadmaps/ber-wp2b3-holdout-execution-scope.md).
BER-DEC-012 authorized the bounded implementation delivered in PR #249 using
synthetic temporary fixtures only. The holdout driver uses the same durable
ledger and refuses a
second pass after its one-way transition. It can rebuild a missing result
summary from a fully closed, verified pass without another provider request.
The production freeze, audited source and development evidence pins remain
unset. The [offline review record](../../docs/evidence/ber-wp2b3-holdout-offline-review.md)
records focused and full Windows tests, independent review, and exact-head
Linux and Windows checks for that merged synthetic package. It is not an
approved live execution revision. The general
runner command-line interface
has no holdout command, and a later measured holdout still needs its separate
gates.

Before any provider request, the owner-approved dataset and exact source
revision, historical usage and remaining allowance, evidence root, host,
credential custody and model terms must pass the recorded gate. Development
would use only its 40 development cases. The 120 holdout cases stay sealed
until the owner reviews development results and freezes the output cap. An
offline test cannot approve labels, establish spending allowance or ratify a
measured result.

## Terms and limits

- **Offline** here means the general commands use local records and fakes.
  Installing dependencies is a separate networked setup step.
- **Scenario A** is the first control family in the design. Its controls are
  labeled A through Q; those letters identify tests, not success grades.
- **Stage A** is the hash-verified input bundle. **Stage B** is the final
  report and verification bundle. A detached marker binds finalization.
- **PASS**, **FAIL**, **UNRUN** and **JUDGE_ERROR** are result states. An unrun
  case or a judge error is neither a behavioral failure nor a pass.
- **SHA-256** is the hash algorithm that binds file and record bytes. A
  matching hash proves integrity against a pinned value, not owner approval.
- Real-host activation, cost observation, containment and execution-profile
  isolation still require separate evidence. Consult `capabilities` before
  making a claim about them.

## Live adapters are gated (not enabled by default)

The `live/` subpackage is the enablement surface for pilot A. **Live capability
state is GATED**: importing the package starts nothing, the default transport
denies every dispatch, and every live verb requires an owner gate record.

**Strict model pinning.** The subject pins are `claude-sonnet-5-5` (Anthropic)
and `gpt-6-astra` (OpenAI). The adapter requests exactly that string and records
the exact `served_model` string the provider returns. A mismatch — including a
missing served-model field — is a HALT with a structured `MODEL_PIN_MISMATCH`
error: the response is discarded, nothing is retried and no alternative model is
substituted. The same rule applies to the judge.

**Credentials.** `ANTHROPIC_API_KEY` and `OPENAI_API_KEY` are read from the
environment only. A missing value fails closed with `CREDENTIAL_MISSING` before
any transport object is built. Values are never logged: structured records carry
the variable name and presence, and `repr`/`str` mask the value.

**Cross-vendor judge.** The judge route is pinned by subject: an Anthropic
subject is judged by `gpt-6-astra` and an OpenAI subject by
`claude-sonnet-5-5`. A judge that shares the subject vendor is refused
structurally. Judge dispatch also requires the judge model to be listed in the
owner allowlist (`judge_allowlist` in the live configuration); an empty
allowlist authorizes no judgment. The judge's rubric input comes only from
committed case data, and every verdict must echo the rubric and response SHA-256
values or it is recorded as `JUDGE_ERROR`.

**Cost meter and hard halt.** Every call reserves a conservative integer-cent
upper bound before dispatch and is reconciled against provider-reported usage
afterwards. When the next reservation would exceed the effective ceiling, the
meter refuses, records the halt and raises `BUDGET_CAP`. The caller marks every
remaining case `UNRUN` with reason `BUDGET_CAP` and never PASS, stops
dispatching, writes `halt.json`, and finalizes the bundle with status
`HALTED`. The proof — simulated usage reaching the ceiling, the refused
reservation, the dispatched-call count and the UNRUN tail — is
`tests/test_live_cost_meter.py`; the work-package record cites it as the
pilot-A required evidence.

**Owner gate and fact provenance.** A live verb needs a committed/gated owner
record with the dataset revision and digest, the pinned model identifiers, the
model-terms acknowledgment, the spend ceiling and a `fact_origin`. `SYNTHETIC`
records can exercise `live-dry-run` only; `live-run` requires `REAL_HOST`.
Synthetic and real results are labeled differently (`SYNTHETIC_NOT_CITABLE` vs
`REAL_HOST`), and the evidence bundle carries its provenance.

**Deterministic graders are primary.** A committed case may carry
`must_include`/`must_not_include` checks. A deterministic failure is recorded
as FAIL even when the semantic judge returns PASS; the judge cannot overrule a
deterministic grader.

**Pilot A run plan (owner pre-granted; subject to a fresh PASS review and the
pilot keys/gate).** 20 skills, 3 runs per case, with and without baseline,
ceiling $150 subject to the owner's $120 provider cap, structured publication,
no raw transcripts. The build itself used no keys and made no provider call.
The live path **defers to the owner allowlist and the cost meter**: enablement is
a recorded owner decision, not a code default.

## Tests and further reading

The [offline continuous-integration guide](../../docs/offline-ci.md) gives the
pinned Python environment and prerequisites. Its runner suite command is:

```bash
python -m unittest discover -s tools/behavioral_eval_runner/tests -p "test_*.py" -v
```

The gated live package has its own offline suite (mock transports and fake
environment values only; no network call and no real key):

```bash
python -B -m unittest tools.behavioral_eval_runner.tests.test_live_adapters tools.behavioral_eval_runner.tests.test_live_cost_meter tools.behavioral_eval_runner.tests.test_live_gate tools.behavioral_eval_runner.tests.test_live_pipeline
```

Tests use synthetic fixtures, local Git and temporary directories. Some need
permission to create and stop synthetic child processes. Record platform
skips and the exact tested revision. The
[Scenario A design](../../docs/design/behavioral-eval-runner-v1-fast-track-successor.md),
[work package 2B-3 evidence summary](../../docs/evidence/behavioral-eval-runner-wp-2b-3-summary.md),
[recovery record](../../docs/evidence/ber-pr88-closeout-2026-09-12/README.md)
and [backlog](../../docs/roadmaps/behavioral-eval-runner-backlog.md) preserve
the transport and ledger limits, thresholds, decisions, historical corrections
and remaining work.
