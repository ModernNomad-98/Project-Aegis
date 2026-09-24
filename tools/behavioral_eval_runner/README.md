# Behavioral Eval Runner

The **Behavioral Eval Runner** is Project Aegis's evaluation harness. It helps
maintainers find out whether an Aegis skill or agent behaves as intended on a
test case. The skills library tells an assistant how to work; this runner
inventories test cases, prepares reproducible inputs, grades recorded behavior,
and reports coverage and uncertainty. It is maintainer infrastructure, not an
application feature installed with the skills.

**Current state:** General runner and Scenario A grading commands operate on
offline or recorded synthetic data. They do not start a live assistant or
send a model request. A separate gated calibration development driver exists,
but measured calibration has not started: replacement labels still need owner
review. No live Scenario A or general corpus run is available. The
[active backlog](../../docs/roadmaps/behavioral-eval-runner-backlog.md) records
current gates; the [design](../../docs/design/behavioral-eval-runner-v1.md)
contains the complete contract.

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
4. **Verify and report.** `verify-evidence` checks the input and final bundles.
   Aggregation and reporting preserve unrun, uncertain and blocked outcomes.

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

The optional `--verify-baseline` flag checks one pinned historical census (882
behavioral cases and 858 trigger cases). A later revision may legitimately
have different counts. Run each command with `--help` for required file shapes
and options.

## What each part does

| Area | Purpose and result |
| --- | --- |
| `census.py`, `materialize.py`, `preflight.py`, `runtime_surface.py` | Count cases from a pinned revision, copy required files, classify runtime files, and report missing or ambiguous prerequisites before grading. |
| `models.py`, `enums.py`, `schemas/`, `identity.py`, `canonical.py` | Define versioned record shapes, stable identities and canonical hashes. Reject invalid or unexpected fields. |
| `pathsafe.py`, `execution_profile.py`, `containment.py`, `process_control.py` | Keep paths within intended roots, describe host capabilities honestly, and expose process-control interfaces. Synthetic tests do not prove real-host containment. |
| `budget.py`, `scheduler.py` | Reserve bounded work before dispatch and build a deterministic queue. Unknown costs, absent caps or deadline violations close the gate. |
| `aggregation.py`, `reporting.py`, `evidence.py`, `evidence_policy.py` | Combine attempts without an unearned pass, report coverage, write and verify a two-stage evidence chain, and optionally check its synthetic complete-bundle policy. |
| `graders/`, `judge/` | Grade recorded Scenario A controls against trusted plans. Deterministic graders cannot decide semantic assertions; the generic judge provider denies live dispatch. |
| `cli.py` | Expose offline inventory, preparation, grading, evidence and status commands. There is no general live-run command. |

The command-line interface also offers `validate-record`, `aggregate-fixture`,
`validate-grading-contract`, `build-judge-envelope`,
`validate-judge-verdict`, `mock-calibration`, `grading-capabilities`,
`validate-calibration-dataset`, and `calibration-status`. These commands check
records, combine recorded attempts, check grading inputs and outputs, exercise
mock calibration, report capabilities, validate synthetic candidate data, and
report authorization status. The envelope command prints repository-safe
metadata rather than private raw content.

## Offline complete-bundle policy proof

`evidence_policy.py` provides an **opt-in Python application programming
interface (API) for synthetic fixtures**.
`OfflinePolicyWriter.finalize_input` requires at least one explicitly classified
input and stamps its first evidence time from the writer's Coordinated Universal
Time (UTC) clock; callers
cannot supply a creation timestamp. `finalize_final` requires an explicit
classification decision for the report and each other final artifact.
`verify_policy_bundle` checks the existing Stage A/B hashes and detached
marker, then the content-bound decisions and one deadline: first writer-stamped
creation time plus 30 consecutive 24-hour periods. At that deadline the
checker refuses an active-bundle acceptance claim and preserves all files for
owner review. It never deletes or publishes a bundle.

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
python -B -m unittest tools.behavioral_eval_runner.tests.test_evidence_policy tools.behavioral_eval_runner.tests.test_evidence
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
controls live under `judge/calibration_*.py`. The current
`calibration_development_driver.py` is development-only. Its default
description command reports the contract without sending a request:

```bash
python -m tools.behavioral_eval_runner.judge.calibration_development_driver --describe
```

The original approved input bytes are unavailable here. Replacement inputs
are versioned in an owner-only private repository; proposed labels still
await human review. Hidden holdout transcripts and labels must stay out of
this public repository and judge requests. See the
[replacement plan](../../docs/evidence/ber-recovery-2026-09-11/replacement-plan.md)
and [offline holdout support proposal](../../docs/roadmaps/ber-wp2b3-holdout-execution-scope.md).
That proposal does not complete a holdout driver or authorize a live run.

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

## Tests and further reading

The [offline continuous-integration guide](../../docs/offline-ci.md) gives the
pinned Python environment and prerequisites. Its runner suite command is:

```bash
python -m unittest discover -s tools/behavioral_eval_runner/tests -p "test_*.py" -v
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
