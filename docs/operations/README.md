# Operations: C3 overhead reduction and C4 qualification

This directory holds the procedures and record formats for C3.1-C3.5 and
C4.1-C4.3. It is documentation plus a read-only validator
([`tools/aegis_ops/`](../../tools/aegis_ops/README.md)); it is not a service,
store, scheduler, dashboard or second policy file.

**Assurance status.** AUDITABLE, mounted coverage UNKNOWN. T6 is
UNVERIFIED+BLOCKED; T24 is UNVERIFIED; T7 is OPEN, so real unavailable-review
dispositions are BLOCKED; T5 is not assumed, so C4.1 is configuration/evidence
only; T4 is declined, so no settings or required-context change is made. No
production-readiness, enforcement, green, conformance or dollar claim is made
or implied.

## Index

| Document | Covers |
| --- | --- |
| [overhead-controls.md](overhead-controls.md) | C3.1 event catalogue, bounded settlement, idle release, durable resume |
| [ci-routing-matrix.md](ci-routing-matrix.md) | C3.2 routing matrix, required-check invariant, E1 edit and bypass accounting |
| [advisory-trigger-findings-policy.md](advisory-trigger-findings-policy.md) | C3.3 advisory-trigger/findings policy proposal and preservation inventory |
| [stage-holders-and-replacement.md](stage-holders-and-replacement.md) | C3.4 holder/replacement/unavailability/context bundle |
| [inbox-zero-activity.md](inbox-zero-activity.md) | C3.5 inbox configuration and disabled zero-activity verification |
| [qualification-and-pilot-metrics.md](qualification-and-pilot-metrics.md) | C4.1 support matrix, C4.2 five-change pilot, C4.3 independent review |

## What is deliberately absent

- no new store, ledger, database, queue, dashboard, service or background job;
- no second policy file and no second finding-triage rubric - the R3 rubric
  stays in [docs/delivery-workflow.md](../delivery-workflow.md#r3-finding-triage-rubric);
- no new telemetry, provider call, network call or paid action;
- no settings, branch-protection, required-context, identity, label or
  repository-visibility change;
- no real reviewer replacement, inbox configuration, pilot case or snapshot.

## Commands

Run from the repository root:

```
python -m tools.aegis_ops --self-test
python -m unittest discover -s tools/aegis_ops/tests -v
python -m scripts.aegis_verdict_gate --self-test
```

The merged checker self-test is pinned to **560 UTF-8 bytes /
098ad54886568bbc7e9103839d5ceda9a573d01f7d234d58a8747913e331bd5d**. C1.1b
moved the checker from `tools/aegis_verdict_gate/` to
`scripts/aegis_verdict_gate/`; the Stage C commands use the live merged path
and the pin is unchanged.

## Format rules

Every record is a closed JSON object with a `schema_version` from
`aegis.ops-*/v1`. Unknown fields are refused rather than ignored. JSON is
canonical for hashing: sorted keys, no insignificant whitespace, UTF-8.
Reports carry the assurance block and never display a blocked condition as
green.

## Limits

This slice proves deterministic validation, not operational adoption. Real
settlements, stage records, inbox runs, reviewer replacements and pilot cases
remain UNRUN until the applicable authority and external arrivals exist. The
tooling can validate synthetic fixtures today; it cannot manufacture the
evidence.
