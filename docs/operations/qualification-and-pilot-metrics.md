# C4 qualification and the five-change pilot

**Scope.** C4.1 publishes a truthful support matrix; C4.2 measures the
**existing** five-change pilot; C4.3 is an independent final review. The
reports are programme records outside this repository. This page defines the
formats and the rules; it adds no product behaviour, telemetry, dashboard,
ledger, data plane or separate pilot.

**Audience and reading key.** For Project Aegis maintainers and reviewers of C4 qualification. **aegis.ops-support-matrix/v1** is the support-matrix schema; **aegis.ops-pilot-metrics/v1** is the pilot metrics schema; **QUALIFIED** means independently exercised; **UNQUALIFIED** means evidence failed; **T5** is mounted coverage; **T6** authentication; **T7** exception authority; **T15–T19** are E3 item-2 outcome rows; **AUTH-REVIEWERS** is the named reviewer authority; **AC** is acceptance criterion; **E4.1/E4.2/E2.4/E3** are programme evidence items; **bounded_shortfall** is fewer than five eligible cases; **T5-gated** means requiring mounted coverage; **fourth-head** is the register-scoped exception; **B/D/E/F** are workflow stages.

**Status.** Formats and the offline analyser are implemented. C4.1 real-host cells, C4.2 arrivals/reports and C4.3 independent review are **UNRUN**.

## C4.1 support matrix

`aegis.ops-support-matrix/v1` rows are configurations/claims:

| Configuration | Required cell |
| --- | --- |
| mode A one-agent/no-inbox | claim, prerequisites, evidence identity, assurance class, independence, limitations, permitted next action |
| optional subagent | same |
| bounded real multi-platform handoff | same |
| selected inbox when authorised | same |
| inbox-disabled zero activity | same |
| recovery/status states | same |

The assurance class is one of **QUALIFIED**, **UNQUALIFIED**, **UNRUN** or
**UNKNOWN**. A QUALIFIED cell needs a real evidence identity and an
independence statement; a cell cannot be both UNRUN and cite evidence. A
simulated host is **never** counted. `simulated_host_counted` must be false.
T5 mounted coverage is **not assumed**; any mounted claim needs a separate
T5-gated slice. Unavailable/unauthorised paths stay UNRUN with their delivery
impact. The matrix feeds E4.1 compatibility and E2/E4 presentation, and it is
bounded by the E3 item-2 outcome (T15-T19); it does not assume accepted
consumer proof.

## C4.2 existing five-change pilot

There is **one** pilot, the existing C4.2 pilot. It is not the retrospective
efficiency-review sample and not the separate docs/instrumentation
workflow-outcomes pilot. The first three eligible cases are the
baseline/checkpoint; all five are the final comparison. Arrivals are external
waits. Fewer than five is a **bounded shortfall** result, never filled with
invented cases or dates.

`aegis.ops-pilot-metrics/v1` per case records:

- `change_id`, `case_ordinal`, `eligible`, `candidate_heads[]` and any
  fourth-head exception (exception ref, blocking-finding ref, authority ref);
- `review_rounds` for B/D/E/F plus `automated_submissions`;
- `stage_elapsed` per stage (minutes or `UNKNOWN`);
- `active_vs_wait`: `active` is `UNKNOWN` unless `active_instrumented=true`;
  wall wait is recorded separately; owner latency is `UNKNOWN` unless
  instrumented;
- `audit_suite_minutes`: value, declared definition and source;
- `reuse_events[]`, `exceptions_bypasses[]`, `owner_touches`, `defects[]`,
  `triage_categories`, `unrun[]`, `dispositions[]`;
- an optional `measured_cost` only with amount, currency and invoice ref.

Rules:

1. every number names its source, query and as-of; denominators are defined;
2. active/owner time may stay UNKNOWN; it is not guessed;
3. a dollar figure is refused unless actually measured on an invoice; the
   field `dollars` (or `dollar_savings`, `hours_saved`, `delay_hours`) is
   forbidden;
4. no hours-to-delay conversion, no cap tuning and no aggregate rate presented
   as a programme-completion claim;
5. the rubric may be tuned later; the caps may not;
6. a distinct reviewer can re-derive a sample from the recorded identities.

The analyser is deterministic and offline; run from the repository root:

```
python -m tools.aegis_ops pilot-metrics --input tools/aegis_ops/tests/fixtures/pilot-metrics-valid.json
python -m tools.aegis_ops pilot-metrics --input tools/aegis_ops/tests/fixtures/pilot-metrics-dollar-invented.json
python -m tools.aegis_ops pilot-metrics --input tools/aegis_ops/tests/fixtures/pilot-metrics-missing-unknown.json
```

Expected: valid exits 0 and states bounded_shortfall; the dollar-invented and
missing-unknown fixtures exit 1. C4.1 matrix production is the programme C4.1 support-matrix record (2,095 B /
`30cb6bf933afa494d9f067caf4c8f5279aea0a82d833ac7bef306d58e87a056b`); the C4.3
record is the independent-review request (2,369 B /
`a3f92a64e87f3cd1dd5c8292a96ac4adfd4b28fe2efaac04473130f920dce07d`).
Neither is produced by this page.

The output states `bounded_shortfall` and the eligible/required counts. A
shortfall exits 0 only when the record is otherwise valid; it is a result, not
a defect.

## C4.3 independent final review

The C4.3 record is an **independent** review of C4.1/C4.2: reviewer identity,
inputs and exact identities, method, exclusions, AC-by-AC result, a
re-derivation sample, accepted changes/compatibility/costs (minutes; dollars
only if measured), limitations and a remaining backlog with real identities.
The reviewer must not be the author, implementer or C4.2 analyst; no
self-approval. T6 authentication is **UNVERIFIED**; T7 exception authority is
**UNKNOWN**. Both are stated so the review cannot imply otherwise. The review feeds E4.1/E4.2 and claims no
merge authority.

In this Stage C slice the C4.3 review is **UNRUN**: no independent reviewer is
named under AUTH-REVIEWERS, so the implementer neither performs nor
self-approves it. The record format and the independence rule are the
deliverable; the verdict itself waits for the named reviewer.

## No new telemetry or data plane

The analyser reads a read-only copy/citation of existing PR, commit, review,
comment, check-run, action-run, stage-record or merge-receipt metadata (see the
fixtures and tests). No prompt/model output/source content is copied. The
analyser performs no network call; its tests assert this. The docs/instrumentation pilot is not enrolled and
[`tools/aegis_usage/`](../../tools/aegis_usage/README.md) is not repurposed:
the analyser fixtures/tests under `tools/aegis_ops/tests/` neither reference
nor modify that usage directory.

## UNRUN

C4.1 real-host qualification and the E2.4 exercise, C4.2 pilot arrivals and
reports, and C4.3 independent review are **UNRUN**. The formats and the
analyser are implemented; the external evidence is not manufactured.
