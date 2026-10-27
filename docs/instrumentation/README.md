# Workflow outcomes instrumentation

This directory documents and binds the **opt-in, offline workflow-outcomes
reporter** for Project Aegis. It exists so that maintainers can learn whether
observed, consenting workflows reach delivery, without inspecting anyone's
project, prompts, output or code.

**Status: offline implementation and synthetic tests only.** No real data has
been collected, no workflow has been enrolled, no export of real data has been
made, and no pilot has been authorised. Writing a runbook here is documentation,
not permission to launch anything.

## Default off, opt in per workflow

- Capture is **off by default**. A fresh local store records nothing.
- One workflow at a time is enabled by an explicit local `opt-in` action that
  records the start day, the applicable stages, the frozen-criteria flag and a
  random criteria-contract reference.
- `opt-out` stops capture for that workflow and drops its unsent export queue;
  retained history is unchanged.
- Local history deletion is a separate, deliberate action:
  `local_report.py delete-local --workflow-ref W --confirm` (or `--all
  --confirm`) irreversibly removes that workflow's history and opt-in from the
  local store. It is local only and never contacts the steward. The store file
  remains if other workflows still use it.
- An export is written only after the **exact bytes** were previewed and the
  preview handle (SHA-256) was confirmed. There is no background upload and no
  reconnect retry; the tool imports no networking module.

## What is collected

Every exported value is an allowlisted enum, a day-precision date or a random
reference generated for that workflow alone:

| Group | Examples |
| --- | --- |
| Envelope | schema epoch, shipped library revision, capture tier `self_report`, consent policy version, 30-day horizon, random `admission_ref` |
| Workflow identity | random `workflow_ref`, monotonic `revision`, random `export_ref` |
| Timing | `start_day`, `last_observed_day`, `report_due_day` (start + 30 days) |
| Stages | fixed `discover`, `plan`, `build`, `validate`, `deliver` with allowlisted status values |
| Outcome | `ongoing`, `delivered`, `failed`, `abandoned`, `unknown` |
| Acceptance | assessment enum, participant-supplied local evidence category (default `none`), delivery and acceptance days |
| History | at most 256 transitions, each with a random `event_ref`, a fixed kind, an effective day and an enum value |

One value per event kind (and per stage, for stage events) per effective day is
allowed. The recorder and the importer reject a same-day conflicting value for
correction instead of guessing which event came last.

## Stage vocabulary and project-orchestrator stages

The contract fixes five stage names. They are a coarse record vocabulary, not a
gate or a quality score. [project-orchestrator](../../.claude/skills/project-orchestrator/SKILL.md)
uses nine finer stages; this is the correspondence a participant should use when
recording.

| Contract stage | Corresponding project-orchestrator stages |
| --- | --- |
| `discover` | Stage 1 — Understand the need (Stage 0 before any work starts) |
| `plan` | Stages 2–3 and 5 — define the product, design how it is built, plan the work |
| `build` | Stage 6 — build it one slice at a time |
| `validate` | Stages 4 and 7 — make it safe, prove it works |
| `deliver` | Stages 8–9 — get it ready to run, decide to release |

Later stages never imply that skipped stages are complete. Record only the
stages that actually happened; inapplicable stages are chosen at start.

## What is never collected

No names, accounts, email addresses or other identities. No prompts, model
output, source code or file content. No project, repository, directory or file
names. No URLs, host, device or IP identifiers. No content hashes or other
content fingerprints. No free-text reasons, notes or comments. Correlation is
**pseudonymous, not anonymous**: a random workflow reference links one
workflow's exports over time, and transport metadata (sender address, IP) is
outside this contract and must be disclosed before any real transfer.

## Data planes

- **Workflow outcomes** — this directory and `tools/aegis_usage/`. A separate
  versioned dataset, `workflow-outcomes-v1`.
- **Skill usage** — unchanged. The existing skill-usage epoch 2 contract in the
  shipped manifest and catalog is not modified by this work; a skill completion
  hint is not a quality score.
- **GitHub attention** — not part of this slice. No scheduled acquisition, no
  joins to workflow data.

## Read next

- [privacy-and-consent.md](privacy-and-consent.md) — allowlist, pseudonymity
  limits, consent, withdrawal and deletion.
- [metrics.md](metrics.md) — cohort, horizon, denominators, suppression.
- [workflow-outcomes-v1.schema.json](workflow-outcomes-v1.schema.json) — the
  strict versioned contract.
- [pilot-runbook.md](pilot-runbook.md) — documentation-only operating procedure.
- [tools/aegis_usage/README.md](../../tools/aegis_usage/README.md) — CLI usage
  with synthetic examples.

## Authority boundary

Implementing or testing this reporter does not authorise real collection,
enrolment, hosting, a pilot, exports of real data, host hooks, scheduled GitHub
acquisition, paid services or deployment. Each of those remains a separate owner
decision with its own privacy and security review.
