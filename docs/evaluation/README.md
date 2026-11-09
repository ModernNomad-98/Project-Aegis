# Offline evaluation qualification slice

**Item (readable name):** Offline evaluation qualification slice (ITEM-2 /
L6-OFFLINE-EVAL). Plain English: a versioned, data-only set of ten evaluation
cases, their expected observations, and a recorded offline run log — with no
runner code change and no provider contact.

**Status:** data-only. The case set exists and a synthetic, mock-adapter pipeline
run is recorded in [run-log-2026-11-09.md](run-log-2026-11-09.md). The
**provider-backed judge and any citable qualification result are UNRUN**. No case
is marked passed, no score is claimed and no effectiveness claim is made.

## What is here

| Path | What it is |
| --- | --- |
| [qualification-set.v1.json](qualification-set.v1.json) | Versioned index: 10 cases over four kinds, each with its oracle and expected terminal state. |
| [cases/](cases/) | Ten `case.json` bodies in the existing Behavioral Eval Runner (BER) live-case schema, so an existing offline entry can load them with no code change. |
| [fixtures/](fixtures/) | Ten hand-written expected-observation fixtures (synthetic; not model output). |
| [case-set-gate.synthetic.json](case-set-gate.synthetic.json) | Synthetic dry-run gate that pins the case-set digest, count and base revision. It grants no live authority. |
| [run-log-2026-11-09.md](run-log-2026-11-09.md) | The executed mock/offline command, exit code, counts, evidence identity, and what remains UNRUN. |

## Four case kinds

The set is deliberately balanced so a refusal-only run cannot look successful:

- **positive** (3) — the response must complete the correct action;
- **negative** (3) — the response must avoid a specific wrong action;
- **refusal** (2) — the request itself must be refused;
- **interruption** (2) — a mid-task instruction must not waive a required step.

## Feasibility gate (checked before authoring)

The plan's gate asked whether an existing offline entry can read an external
fixture directory with no code change. It can: the merged Behavioral Eval Runner
exposes `live-dry-run`, which loads a `--cases` directory in the committed
`case.json` schema and runs the whole pipeline over mock adapters with zero
network calls. A two-case probe against a directory outside the runner's bundled
`live/cases` returned exit 0. The ten cases in this slice use the same schema, so
no runner or script change was needed; **no `.py` file is changed by this item**.

## Boundaries and non-claims

- No live, paid or provider call; no credential; no spend.
- No judge verdict, pass, score or qualification result is claimed. Mock results
  are marked `SYNTHETIC_NOT_CITABLE` by the runner and are not evidence of case
  behaviour.
- No runner, script, workflow or skill is changed or added.
- The case bodies and fixtures are synthetic; they contain no personal data.
- Selection of the judge, thresholds and the consumer-outcome scope remain owner
  decisions (`ROD-06`); this slice does not decide them.
