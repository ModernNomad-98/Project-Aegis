# Gated Deployment Prompt — Template Skeleton & History Index

Companion to `gated-deployment-prompt-template`. Everything below is
product-agnostic; `<angle-bracket>` values are filled by the OPERATOR at run
time. Credentials appear as environment-variable names only.

## Operator prompt skeleton

```markdown
# <OPERATION CLASS> RUN — <YYYY-MM-DD>

## Fill before starting (all placeholders mandatory)
- Repo / environment:   <owner>/<repo> / <environment>
- Target:               <tenant-id> | <database/schema> | <surface>
- Unit:                 <migration-id | grant-id | backfill script + version>
- Migration review:     <link to secure-migration-reviewer verdict>   [required input]
- Rollback artifact:    <link to rollback runbook for this change>    [required input]
- Approval:             <register entry APR-<NNN> covering this run>  [required input]
- Backup id (filled in step B1): <backup-id>
- Report path:          docs/deployments/<YYYY-MM-DD>-<operation>.md
- Credentials:          via env vars <ENV_VAR_NAME_1>, <ENV_VAR_NAME_2> — never pasted

## Hard rules (every run of this class)
1. Required inputs above present and current, or the run does not start.
2. Validate-only mode first wherever the tooling has one; apply only after
   validate-only output matches expectations.
3. Scope = the named unit. Anything else discovered mid-run is a NEW run.
4. Every claim in the report cites its evidence (command output, query
   result); any uncited operational claim is labeled
   "unverified — recommend confirming".
5. On ANY stop condition: halt, leave the state described, report — do not
   improvise recovery beyond the rollback artifact.

## Stop conditions (halt + safe state)
- Backup cannot be taken OR cannot be verified → halt BEFORE any change;
  state: untouched.
- Pre-checks (phase 0 smoke) fail → halt; state: untouched.
- Mid-run deltas differ from expected → halt; state: document exactly what
  applied; invoke rollback artifact decision point.
- Post-phase smoke fails → halt; same as above.
- Ambiguity about WHICH tenant/environment is being touched → halt
  immediately; state: untouched if pre-apply, else as documented.

## Phases
### B1 — Backup, then VERIFY the backup
- Take: <backup command/procedure — evidence: backup id + size/rowcount>
- Verify: <readability/restorability check — a backup unverified is not a gate>
- ETA: <range> (anchor: index rows <ids>)

### P0 — Pre-checks (smoke before touching anything)
- <query/endpoint> → expected: <value>
- ETA: <range> (anchor: <ids>)

### P1 — Apply (validate-only → apply)
- Validate-only: <command> → expected output: <shape/counts>
- Apply: <command> → expected deltas: <rows affected / objects created>
- ETA: <range> (anchor: <ids>)

### P2 — Post-verification (expected deltas, not absence-of-error)
- <query> → expected: <exact expected value/delta>
- <smoke endpoint/flow> → expected: <status>
- ETA: <range> (anchor: <ids>)

## Report (required, at the report path)
- Placeholders as filled (minus secrets), phase timings (expected vs
  observed), verification outcomes with evidence, deviations from this
  template (each flagged), stop conditions hit (if any), final state.
- Add one row to the deployment-history index (below). No report → the run
  never calibrates anything → the next operator inherits folklore.
```

## Deployment-history index format

```markdown
# Deployment History Index — <operation class>

| # | date | operation/unit | phase durations (observed) | outcome | report |
|---|------|----------------|------------------------------|---------|--------|
| 7 | 2026-07-01 | migration <id-class> | B1 4m / P0 1m / P1 6m / P2 3m | success | [report](…) |
| 6 | 2026-06-14 | migration <id-class> | B1 5m / P0 1m / P1 9m (lock retry) / P2 3m | success w/ deviation | [report](…) |
```

**ETA-anchor rule:** a template ETA range cites the index rows it derives
from — e.g. `P1 ETA: 6–10m (anchors: #6, #7)`. Anchors must be actual prior
reports of the SAME operation class. When history is empty or too thin, the
ETA is written as `unverified — recommend confirming (no comparable prior
run)` — never a confident invented range. When a new run's observed duration
falls outside the cited range, the next template revision re-derives the
range and cites the new row.

## Identifier hygiene (source-evidence lesson)

The production docs this pattern was extracted from embedded a live tenant
UUID inside the deployment prompt itself. Do not inherit that: the template
carries `<tenant-id>`; the run report records which tenant was touched
(that's evidence, in a governed doc); an optional per-environment VALUES
note may exist under the repo's secret-handling conventions, separate from
the template. Credentials never appear as values anywhere in this system —
env-var names only.

## Relationship to neighbors (quick router)

| Need | Skill |
| --- | --- |
| Is this migration itself safe (locks, reversibility, data loss)? | `secure-migration-reviewer` — its verdict is a required input above |
| The executable rollback steps referenced by the stop conditions | `rollback-runbook-author` |
| Production is broken NOW | `incident-response-runbook` |
| What does merging auto-deploy, and who owns branch protection? | `merge-is-deploy-governance` — the operator-applied remainder it identifies is what this template gates |
| May an agent run any of this at all? | `agent-authorization-matrix` floors + the approval register entry |
