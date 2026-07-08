# Evolution Stage Playbook

Detail for the three stages, the compatibility matrix, the backfill handoff
contract, and the deprecation register. `SKILL.md` owns the workflow; this
file owns the tables and templates.

## Compatibility matrix (state per stage)

For each stage, fill all four cells — a stage ships only when every cell is
"works":

| | old schema shape | new schema shape |
|---|---|---|
| **old code version** | baseline | must not error (expand: ignores new objects; migrate: never sees new-only rows) |
| **new code version** | must read/write correctly (null-tolerant reads, defaults) | target behavior |

A cell that cannot be made to work forces a stage split, not a caveat.

## Stage templates

### Expand
- DDL: new column (nullable or defaulted) / new table / new index — never a
  mutation of an existing object.
- Forbidden here: NOT NULL on existing rows, type narrowing, dropping,
  renaming in place, retroactive constraint enforcement.
- Gate evidence: schema object present in the target environment; error
  rates flat while old code runs against it.

### Migrate
- Application dual-write lands every mutation in both shapes; note where the
  write happens (model layer, trigger, or service) and who owns turning it
  on and off.
- Backfill covers pre-existing rows. This plan states: batch intent,
  parity definition (row counts per range, checksums over normalized
  values, or sampled field equality), and the read-switch mechanism (flag,
  config, deploy). Operational sizing, throttling, and the verification
  queries themselves belong to `data-migration-runbook-author`.
- Gate evidence: parity check passes over the FULL keyspace (not a sample
  alone); reads verifiably served from the new shape; dual-write error rate
  zero over a stated window.

### Contract
- Stop dual-writes (code change), enter the old shape in the deprecation
  register, tighten constraints that expand had to defer (NOT NULL, type,
  FK), and schedule — not execute — the physical drop.
- Gate evidence before the drop ships: zero readers of the old shape over a
  stated observation window, from query statistics or log scan; the
  register entry's earliest-drop release reached.

## Deprecation register format

One row per logically-dead-but-physically-present object:

| Object | Replaced by | Deprecated in (release/date) | Earliest drop | Evidence required before drop | Owner |
|---|---|---|---|---|---|
| `<table.column>` | `<new shape>` | `<release>` | `<release>` | zero reads over `<window>` via `<source>` | `<role>` |

Rules: no entry without an earliest-drop value and an owner; the drop
migration cites the row and its evidence; the register lives with the
migration directory so it is versioned with the schema.

## Backfill handoff contract (to data-migration-runbook-author)

The plan hands over, at minimum: source and target shapes; keyspace and
row-count estimate; parity definition; batching intent (by key range, with
the write-rate caveat); abort condition (parity failure ⇒ stop, never
"skip and continue"); and the read-switch that must NOT flip until parity
evidence exists. The runbook owns everything operational beyond that.

## Gate evidence examples (tool-agnostic)

- Zero-reader proof: the store's query-statistics view filtered on the old
  object over the window, or application log scan for the deprecated
  accessor — state which, and the window.
- Parity proof: per-range `count(*)` equality plus a checksum/aggregate
  over normalized values of migrated columns; sampled row-by-row equality
  as a spot check, never the sole proof.
- Read-switch proof: a marker in the read path (log line, metric tag)
  showing the new shape serves production reads.
