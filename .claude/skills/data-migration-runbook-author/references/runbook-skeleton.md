# Runbook Skeleton & Worksheets

Templates backing the workflow. Purpose-first commands; exact invocations
only where platform-stable. Placeholders (`<table>`, `<tenant-id>`)
throughout — never live identifiers.

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

| Trigger (numeric) | Action | Safe halt state |
|---|---|---|
| Batch parity mismatch > 0 | stop loop immediately; do NOT revert schema | old path serving; partial new data inert; resumable after diagnosis |
| Replication lag > <t> for > <d> | pause loop; resume when < <t/2> | mid-move pause; marker intact |
| Primary p99 > <t> during batches | pause; halve batch size on resume (recorded deviation) | as above |
| Serving errors > baseline post-switch | switch reads BACK (dual-writes still on) | old path serving; new store still converging |
| Batch duration 2× baseline trend | finish current batch; stop; investigate | clean marker boundary |

Never in the abort path: dropping the new schema/store, disabling
dual-writes before reads are back on the old path, or "clean up" deletes
without their own reviewed step.

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
POSTURE: this document executes nothing; operators run steps; [APPROVAL
REQUIRED] steps proceed only with the marked human approval recorded.
```

## Execution-log discipline

The log is the move's evidence: verification OUTPUTS pasted (not "ok"),
deviations recorded at decision time with who approved them, and the
final entry stating end state + residuals (inert copies kept/cleaned).
Feeds the closeout and any later governance audit.
