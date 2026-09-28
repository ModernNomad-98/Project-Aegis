# Runbook Skeleton & Worksheets

Templates backing the workflow. Purpose-first commands; exact invocations
only where platform-stable. Placeholders (`<table>`, `<tenant-id>`)
throughout — never live identifiers.
The owning [data migration runbook skill](../SKILL.md) defines the
document-only scope and the authorization needed to execute a live run.
Here, **p99** means the 99th-percentile response time on the primary path.

## Target confirmation (step 1 of every runbook)

A read-only fingerprint, compared with expected values written down BEFORE
the run by the plan or the environment's owner:

```
Fingerprint:  database name = <expected>; host = <expected>;
              sentinel row <table>.<key> = <expected value only this environment holds>
Run as:       read-only query from the session that will do the writes
EXPECTED:     all three match exactly
ON MISMATCH:  stop; nothing below runs; record what was seen in the log
```

An expected value copied from the session being checked proves nothing:
it must come from outside that session.

## Batching-rationale worksheet

```
Batch key:     <monotonic id | date partition | tenant bucket>
Batch size:    <n rows> — rationale: <rows × width vs lock/undo/redo budget;
               target batch duration ≤ <s> so locks/transactions stay short>
Throttle:      <sleep ms | rate> tuned by: <replication lag > <t> ⇒ back off;
               primary p99 > <t> ⇒ pause>
Concurrency:   1 unless partition-disjoint proof: <proof or "n/a">
Progress:      marker=<last completed batch key> stored in <OUTSIDE the moving data>
Resume:        idempotent because <keyed upsert | range replace> — re-running
               the marker batch is harmless
Window:        <quiet hours; days of elevated attention after cutover>
```

## Verification-query patterns (intent + expected shape)

- **Batch count parity:** count rows in source range vs target range —
  EXPECTED: exact equality; any diff ⇒ batch FAIL (abort path, not retry-
  and-hope).
- **Checksum/aggregate parity:** checksum or sum/hash over normalized
  migrated columns for the range — EXPECTED: equal values. Normalize
  first (trim, case, precision) or the checksum manufactures mismatches.
- **Sampled row equality:** N known entities (include edge rows: nulls,
  max-length, oldest) compared field-by-field — EXPECTED: zero diffs;
  spot-check only, never the sole gate.
- **Full-keyspace stage gate:** the plan's parity definition over the
  ENTIRE keyspace before any read-switch — EXPECTED: stated by the plan.
- **Serving-path check post-switch:** the read path demonstrably serving
  from the new store (marker log/metric) + error rate flat — EXPECTED:
  markers present, errors ≤ baseline.

Where each runs: primary vs replica stated per check, with the lag the
check must tolerate.

## Abort triggers → safe halt states (examples)

The runbook's **A1** abort uses the first row's stop-loop, old-path-serving
halt when a dual-write, batch, or full-keyspace verification fails before the
read switch. Its **A4** abort uses the fourth row's switch-reads-back halt
after the read switch. Replace the example thresholds with plan-approved values.

| Trigger (numeric) | Action | Safe halt state |
|---|---|---|
| A1 — Batch parity mismatch > 0 | stop loop immediately; do NOT revert schema | old path serving; partial new data inert; resumable after diagnosis |
| Replication lag > <t> for > <d> | pause loop; resume when < <t/2> | mid-move pause; marker intact |
| Primary p99 > <t> during batches | pause; halve batch size on resume (recorded deviation) | as above |
| A4 — Serving errors > baseline post-switch | switch reads BACK (dual-writes still on) | old path serving; new store still converging |
| Batch duration 2× baseline trend | finish current batch; stop; investigate | clean marker boundary |

Never in the abort path: dropping the new schema/store, disabling
dual-writes before reads are back on the old path, or "clean up" deletes
without their own reviewed step.

## Smoke-check patterns (after apply or read switch)

- **Known record renders:** a named record that touches the changed
  tables is read through the application — EXPECTED: the stated fields,
  no error.
- **Write path works:** one reversible test write through the application
  on a marked test entity — EXPECTED: success, and the row has the new
  shape.
- **Error rate:** the serving path's error rate for <n> minutes after the
  change — EXPECTED: at or below the pre-change baseline.

A failed smoke check points to an abort row, never to "watch and see".

## Runbook skeleton

```
DATA MIGRATION RUNBOOK — <move> vN <date>
0 PREREQUISITES (all cited, none assumed)
  plan=<schema-evolution-planner ref> review=<secure-migration-reviewer verdict ref>
  backup=<evidence: last successful backup/restore-test + restore-time bound>
  rehearsal=<staging run of THIS runbook: date/result | waived by <human> because <reason>>
1 PRECONDITIONS (pass/fail gates)
  1.1 backup evidence current … EXPECTED: <artifact/timestamp>
  1.2 dry-run parity on <sample keyspace> … EXPECTED: <result>  (evidences syntax+mechanics, NOT volume behavior)
  1.3 headroom: disk/undo/lag baseline … EXPECTED: <numbers>
  1.4 window announced to <stakeholders> … EXPECTED: ack
2 EXECUTION — Stage <n> <name>
  2.1 [APPROVAL REQUIRED] enable dual-writes … VERIFY <both shapes written> EXPECTED <sample shows both> ON FAIL <abort A1>
  2.2 backfill loop per batching worksheet … VERIFY per-batch parity EXPECTED equality ON FAIL <abort A1>
  2.3 stage gate: full-keyspace parity … EXPECTED <plan's definition> ON FAIL <abort A1>
  2.4 [APPROVAL REQUIRED] switch reads … VERIFY serving-path check EXPECTED markers+flat errors ON FAIL <abort A4: switch back>
3 ABORT CRITERIA (per table above; each names its halt state)
4 ROLLBACK per stage (rollback-runbook-author conventions; time-boxed
  roll-back-vs-fix-forward; one observable verification per step)
  NO-RETURN: <decommission/contract step> — requires <named human sign-off> +
  zero-reader evidence <ref>; after this, rollback = restore-grade event
5 EXECUTION LOG (fill during run)
  <timestamp> <step> <batch range> <verification output> <deviation + reason>
6 CLOSEOUT RECORD
  fingerprint seen, backup evidence used, end state, smoke-check results, residuals
POSTURE: this document executes nothing; operators run steps; [APPROVAL
REQUIRED] steps proceed only with the marked human approval recorded.
```

Step 1 target confirmation (above) precedes section 0 in every runbook.

## Schema-migration deploy skeleton

```
MIGRATION DEPLOY RUNBOOK — <migration id> to <environment> vN <date>
1 TARGET CONFIRMATION … EXPECTED <fingerprint values> ON MISMATCH <stop>
2 PREREQUISITES  review=<secure-migration-reviewer verdict> backup=<evidence + restore-time bound>
3 [APPROVAL REQUIRED] apply <migration id> … EXPECTED <tool reports applied; lock time ≤ <s>>
                                              ON FAIL <abort: stop; do not re-run blind>
4 SCHEMA VERIFICATION … EXPECTED <migration recorded as applied; tables/columns/indexes as reviewed>
5 SMOKE CHECKS (patterns above) … EXPECTED <each check's result> ON FAIL <rollback ref>
6 ROLLBACK REFERENCE  <the migration's rollback plan from rollback-runbook-author>
7 EXECUTION LOG and CLOSEOUT RECORD (as above)
POSTURE: this document executes nothing; operators run steps.
```

## Execution-log discipline

The log is the move's evidence: verification OUTPUTS pasted (not "ok"),
deviations recorded at decision time with who approved them, and the
final entry stating end state + residuals (inert copies kept/cleaned).
Feeds the closeout and any later governance audit.
