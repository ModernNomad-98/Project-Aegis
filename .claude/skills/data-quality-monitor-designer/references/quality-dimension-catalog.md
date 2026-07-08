# Quality Dimension Catalog

Concrete check forms per dimension, expectation-band guidance, placement
table, and the quarantine template. `SKILL.md` owns the workflow; this file
owns the catalogs. All forms are stack-agnostic — express them in your
pipeline's assertion tooling.

## Check forms per dimension

### Freshness
- `max(event_time | partition_date)` age vs expected-by deadline, per
  dataset AND per critical source within it.
- Watermark lag for streaming datasets (consumed-up-to vs now).
- Trap: freshness of the LOAD, not the DATA — a job that runs on time but
  loads yesterday's file twice is "fresh" and wrong; pair with volume.

### Completeness / volume
- Row/event count vs expectation band (see bands below), per period.
- Required-field null rate ≤ floor, per field that consumers key on.
- Source-complete check where the producer publishes a manifest/count.

### Uniqueness
- Duplicate rate on the declared business key ≤ floor (state the key).
- Post-join fan-out check: output rows ÷ input rows within expected ratio.

### Validity
- Type/format conformance (parseable dates, numeric ranges, id shapes —
  placeholders like `<tenant-id>` format rules, never live values).
- Enum membership against the registry the contract names.
- Cross-field rules (end ≥ start; refund ≤ original amount).

### Consistency / referential
- Orphan rate: foreign keys resolving nowhere ≤ floor.
- Reconciliation: aggregate here vs source-of-truth there, compared AFTER
  the stated sync lag (the lag budget is part of the check).
- Cross-store counts for dual-written data during migrations (standing
  version of the runbook's one-time parity gate).

### Drift (flag-only; never auto-correct)
- Categorical mix shift vs trailing window (top-k share change).
- Numeric distribution shift (quantile deltas) on decision-bearing fields.
- New-category appearance on supposedly closed enums.

## Expectation bands

- Derive from trailing history (e.g., same weekday over N weeks), not a
  single fixed number; widen for known seasonality; version band changes.
- A band that has false-positived twice without a data defect is a defect
  in the band — tune it via review, not by muting the alert.
- New datasets get provisional wide bands + alert-and-pass until history
  accumulates; say so in the spec.

## Placement table

| Placement | Catches | Typical dimensions |
|---|---|---|
| Ingest | Poison at the door; producer contract breaks | validity, schema shape, source-complete |
| Transform | Defects created mid-pipeline | uniqueness (post-join), consistency, volume deltas per stage |
| Serving | What consumers actually read | freshness, reconciliation, SLA floors |

Earliest viable placement wins; a defect catchable at ingest but checked
at serving costs a full pipeline run per incident.

## Failure-action vocabulary

| Action | Semantics | Requirements |
|---|---|---|
| block | Pipeline halts; nothing passes | Only where bad data is worse than late data — state that judgment |
| quarantine | Offending rows diverted with provenance; healthy rows flow | Location, provenance fields, owner, drain SLA (below) |
| alert-and-pass | Data flows; humans notified | Named owner; acceptable only where consumers tolerate the defect class |

Silent correction (coerce/default/drop without record) is NOT an action.
A deliberate, human-approved correction is a logged transform with its own
review — outside the monitor's authority.

## Quarantine policy template

```
QUARANTINE — <dataset>
Location:    <table/topic/prefix reserved for quarantined rows>
Provenance:  original row + check id + check evidence + captured-at + source batch/offset
Owner:       <role> — reviews within <drain SLA>
Dispositions: repair-and-replay (via the pipeline, idempotent) | discard-with-record | accept-upstream-fix
Escalation:  quarantine size > <threshold> or age > <limit> ⇒ incident to <route>
```

## Incident routing card

```
<dataset> RED on <check> ⇒ owner=<role>
First diagnostic: <the check's own evidence — failing-row sample, expected-vs-actual counts, band history>
Consumer notice: <who is told their data is suspect, and how quickly>
```
