---
name: data-quality-monitor-designer
description: Design data-quality monitoring for production pipelines and stores — checks across the six dimensions (freshness, completeness/volume, uniqueness, validity, consistency/referential integrity, distribution drift), placed at the right pipeline stage (ingest, transform, serving), each with severity, an owner, and a failure action (block, quarantine to a reviewable location, or alert-and-pass — never silent auto-fix), plus per-dataset quality SLAs and incident routing. Produces the monitor spec and quarantine policy as design; alert/dashboard wiring is observability-operator and user-journey SLO targets stay with slo-reliability-architect. Use when bad, stale, or missing data keeps reaching users or models, when a warehouse/pipeline needs quality gates, or when nobody can say whether a dataset is trustworthy. Do NOT use for TEST data design (test-data-architect), system telemetry (observability-operator), or LLM output shape (structured-output-validator).
---

# Data Quality Monitor Designer

## Purpose

Systems monitor their services and stay blind to their data: the pipeline
runs green while a third of yesterday's rows never arrived, a join
silently fans out duplicates, and a upstream format change poisons every
downstream report. This skill designs the data-quality monitoring layer —
which checks, on which datasets, at which pipeline stage, with what
severity, owner, and failure action — so data problems surface as typed,
routed incidents instead of being discovered by the user who trusted the
number. It produces the monitor SPEC and the quarantine policy; it does
not wire alerts (that is `observability-operator`'s implementation
surface) and it never designs checks that silently "fix" data.

## Use When

- Use when: bad, stale, duplicated, or missing data keeps reaching users,
  reports, or models, and detection is currently "someone notices".
- Use when: a pipeline, warehouse, or critical dataset needs quality gates
  and nobody can enumerate what is checked today.
- Use when: defining per-dataset quality SLAs (freshness by 06:00, ≥99.5%
  rows with valid foreign keys) and what happens when they are missed.
- Use when: a data incident post-mortem asks "what monitor would have
  caught this?" and the answer needs designing, not guessing.
- Do NOT use when: the data in question is TEST data — deterministic
  fixtures, factories, and seed hygiene are `test-data-architect`; this
  skill watches production data.
- Do NOT use when: the signals are system telemetry — latency, errors,
  saturation, health checks are `observability-operator` (implementation)
  and `slo-reliability-architect` (targets); this skill owns checks on the
  DATA CONTENT itself.
- Do NOT use when: validating an LLM's response shape against a schema —
  that is `structured-output-validator`.
- Do NOT use when: the failing thing is a migration's correctness during a
  planned data move — one-time verification gates belong to
  `data-migration-runbook-author`'s runbook; this skill owns the STANDING
  monitors that outlive the move.

## Inputs to Inspect

1. The dataset inventory in scope: tables/topics/files, their producers,
   their downstream consumers (reports, features, models, exports), and
   which consumers make decisions on them.
2. The pipeline topology: ingest points, transform stages, serving
   surfaces — where a check can physically run and how early a defect is
   catchable.
3. Incident history: past data incidents (silent loss, duplication, drift,
   late arrival) — each one is a candidate check with a known severity.
4. Existing checks and their gaps: constraint definitions in the store,
   ad-hoc assertion scripts, pipeline-native tests already present.
5. Contract sources for validity rules: schema definitions, enum
   registries, business rules docs — what "valid" even means per field.
6. The tenant dimension: whether quality must be judged per tenant (one
   tenant's feed failing while the aggregate looks fine).

## Workflow

1. **Rank datasets by blast radius.** For each dataset: who consumes it,
   what decision or feature breaks when it is wrong, and how long a defect
   goes unnoticed today. Monitor design effort follows this ranking —
   full six-dimension coverage for the critical few, freshness+volume
   floors for the long tail.
2. **Design checks per dimension, per dataset.** For each critical
   dataset, work the six dimensions and state each check concretely:
   - *Freshness:* latest event/partition age vs an expected-by deadline.
   - *Completeness/volume:* row/event counts vs a seasonal-aware
     expectation band, plus required-field null rates.
   - *Uniqueness:* duplicate rate on declared keys (joins and replays are
     the usual injectors).
   - *Validity:* type/format/enum/range conformance per field, sourced
     from the contract inputs, not invented.
   - *Consistency:* referential integrity across stores, aggregate
     reconciliation (sum of parts vs reported total), cross-system counts.
   - *Drift:* distribution shift on fields where meaning matters
     (categorical mix, numeric distribution) — flag, never auto-correct.
3. **Place each check at the earliest viable stage.** Ingest-time checks
   stop poison at the door (schema/validity), transform-time checks catch
   what only exists post-join (uniqueness, consistency), serving-time
   checks guard what users actually read (freshness, reconciliation).
   State the placement and why.
4. **Assign severity and failure action per check.** The action vocabulary
   is exactly three: **block** (pipeline stops; defect cannot pass),
   **quarantine** (offending rows diverted to a reviewable location with
   provenance; healthy rows proceed; quarantine has an owner and a drain
   SLA — mirroring DLQ discipline), **alert-and-pass** (data flows,
   humans notified). Silent correction — coercing, defaulting, dropping
   without a record — is not in the vocabulary.
5. **Define per-dataset quality SLAs.** The consumer-facing promise:
   freshness deadline, completeness floor, validity floor — each derived
   from what the top consumer can tolerate, stated with its measurement
   window. Where a journey-level SLO exists (`slo-reliability-architect`),
   the data SLA feeds it rather than duplicating it.
6. **Route incidents.** Per dataset: who owns a red check (a named role,
   not a channel), what the first diagnostic step is (the check's own
   evidence: failing rows sample, expected-vs-actual counts), and where
   quarantined data is reviewed. Alert wiring, dedup, and dashboards are
   handed to `observability-operator` as an implementation package.
7. **Design the monitor-as-code shape.** Checks live versioned next to the
   pipeline they guard (declarative where the stack allows), with the
   convention stated: adding a dataset of class X requires its floor
   checks in the same change — a review-time rule, not tooling magic.
8. **Deliver the spec** in the Output Format with coverage honestly
   stated: which datasets got full coverage, which got floors, which got
   nothing yet — an explicit residual list, not an implied "all".

Check catalogs per dimension, expectation-band guidance, and the
quarantine-policy template:
[references/quality-dimension-catalog.md](references/quality-dimension-catalog.md).

## Output Format

```
DATA QUALITY MONITOR SPEC — <scope>
Datasets ranked: <N, by blast radius; coverage tier per dataset>
Per-dataset card:
  <dataset>: consumers=<top consumers/decisions>
  checks: <dimension → check, placement (ingest|transform|serving),
           severity, action (block|quarantine|alert-and-pass)>
  SLA: freshness=<deadline> completeness=<floor> validity=<floor> (window=<w>)
  incident: owner=<role> first-diagnostic=<evidence the check emits>
Quarantine policy: <location, provenance fields, owner, drain SLA>
Tenant dimension: <per-tenant checks where aggregate masks single-tenant failure | n/a + why>
Handoffs: alert/dashboard wiring → observability-operator;
          journey SLO targets → slo-reliability-architect (consumed, not set here)
Residual: <datasets/dimensions deliberately not covered yet>
```

## Validation Checklist

- [ ] Every check names its dataset, dimension, placement, severity,
      owner, and one of the three failure actions — no check "just logs".
- [ ] No check silently mutates data: quarantine preserves offending rows
      with provenance; nothing coerces, defaults, or drops unrecorded.
- [ ] Validity rules cite a contract source (schema, enum registry,
      business rule) — none invented from sample data alone.
- [ ] Volume/drift checks use expectation bands aware of seasonality, not
      naive fixed thresholds guaranteed to false-positive.
- [ ] Quarantine has an owner and a drain SLA — it is not a write-only
      graveyard.
- [ ] Per-tenant blindness considered: aggregate-level checks that a
      single tenant's failure cannot trip are named as such.
- [ ] Coverage residual is explicit — datasets left unmonitored are
      listed, not implied covered.
- [ ] The spec hands wiring to observability-operator rather than
      embedding alert-platform configuration.

## Gotchas

- Green pipelines, rotten data: orchestration success says the job ran,
  not that the data is right. Quality checks assert on CONTENT — never
  accept "the DAG succeeded" as a quality signal.
- Fixed thresholds rot: "alert if rows < 10,000" false-positives every
  holiday and misses a 30% drop on the biggest day. Bands come from
  history with seasonality, and get reviewed like code.
- Silent coercion is data loss with better manners: a transform that
  defaults bad values to zero destroys the evidence AND the number.
  Quarantine exists so correction is a reviewed decision.
- Aggregate checks mask per-tenant failure: total volume looks fine while
  one integration's feed died. The tenant dimension check exists for the
  datasets where that matters.
- Duplicates arrive at joins and replays, not ingest: uniqueness checked
  only at the door misses fan-out introduced mid-pipeline. Placement
  follows where the defect is created.
- Drift checks on the wrong fields alarm-fatigue everyone: monitor
  distribution only where shift changes meaning (model features, pricing
  inputs), not every column.
- Reconciliation needs a lag budget: comparing system A to system B
  before B's sync window closes manufactures false mismatches — state the
  comparison point, not just the comparison.
- Quality SLAs without consumers are decoration: a freshness deadline
  nobody depends on will be ignored the first week it is red. Every SLA
  cites the consumer that needs it.

## Stop Conditions

- Asked to design checks that auto-repair failing data (coerce, default,
  drop, "clean up") as the failure action → refuse silent correction;
  offer quarantine + reviewed repair, and record any human decision to
  auto-correct a specific field as an explicit, logged transform, not a
  monitor behavior.
- Validity rules cannot be sourced — no schema, no contract, and the
  owner cannot say what valid means for a critical field → stop for that
  dataset; checks invented from sampled data enshrine today's defects as
  the standard.
- The request is really "make the pipeline stop failing" (orchestration
  reliability, retries, infra) → route to the pipeline/reliability
  surface; adding quality checks will not fix a broken scheduler.
- Monitoring would require reading data classified as restricted (PII
  fields under minimization rules from `pii-lifecycle-designer`) and no
  privacy-preserving check form exists (counts, hashes, null rates) →
  halt and surface the conflict rather than designing checks that widen
  access.
- Asked to also wire the alerts/dashboards live → decline that slice;
  hand the implementation package to `observability-operator` (which is
  manual-invocation for live config).

## Supporting Files

- [references/quality-dimension-catalog.md](references/quality-dimension-catalog.md)
  — per-dimension check catalog with concrete forms, expectation-band
  guidance, placement table, and the quarantine-policy template.
- `evals/evals.json` — behavior cases including the seasonality-band edge
  and the silent-auto-fix refusal.
- `evals/trigger-evals.json` — discrimination against
  `observability-operator`, `test-data-architect`,
  `structured-output-validator`, and `data-migration-runbook-author`.
