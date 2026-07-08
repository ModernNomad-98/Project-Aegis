---
name: schema-evolution-planner
description: Plan how a live store's schema changes without breaking deployed readers and writers — the expand → migrate → contract sequence (additive first, dual-read/dual-write windows, backfill, contraction only after verified cutover), per-stage compatibility guarantees (old code × new schema, new code × old schema), consumer impact across ORM models, event payloads, and analytics extracts, a deprecation register for columns still physically present, and verification gates per stage. Produces the staged evolution PLAN; the operator runbook is data-migration-runbook-author and safety review of a written migration is secure-migration-reviewer. Use when renaming/splitting/retyping columns or tables on a live system, coordinating schema change with rolling deploys, or sequencing a multi-release evolution. Do NOT use for tenant-scoping design (multi-tenant-data-architect) or event-schema compatibility (streaming-event-architect).
---

# Schema Evolution Planner

## Purpose

A schema change on a live system is a distributed-systems problem disguised
as DDL: at every moment during the rollout, some deployed code version is
reading and writing the store, and a "simple rename" breaks whichever side
moved second. This skill produces the staged evolution plan — expand,
migrate, contract — in which every stage keeps BOTH the previous and the
next code version working, every stage has a verification gate before the
next begins, and nothing is dropped until evidence shows nothing still
reads it. The deliverable is a plan a team can execute across releases; it
is not the migration file, not the operator runbook, and not a safety
review of DDL someone already wrote.

## Use When

- Use when: a column or table must be renamed, split, merged, retyped, or
  moved while the system keeps serving traffic.
- Use when: a schema change must coordinate with rolling deploys — old and
  new application versions overlap and both must keep working.
- Use when: sequencing a multi-release evolution (deprecate now, remove two
  releases later) and the team needs the stages, gates, and compatibility
  contract written down.
- Use when: a proposed one-shot migration ("just rename it in one deploy")
  needs to be decomposed into compatible stages.
- Do NOT use when: the question is HOW tenant data is scoped, partitioned,
  or migrated between isolation models — that data-model design is
  `multi-tenant-data-architect`; this skill sequences changes to an agreed
  model.
- Do NOT use when: reviewing a written migration file for privilege, RLS,
  lock, or destructive-operation risk — that is `secure-migration-reviewer`;
  each stage's migration from this plan still goes through it.
- Do NOT use when: authoring the operator-executable runbook for the data
  move itself (batching, verification queries, cutover timing) — that is
  `data-migration-runbook-author`, which consumes this plan.
- Do NOT use when: the evolving schema is an EVENT or stream payload —
  compatibility rules for event consumers live with
  `streaming-event-architect` (internal streams) or `api-event-architect`
  (external contracts).

## Inputs to Inspect

1. The current schema of the affected store: table/column definitions,
   constraints, indexes, and which of them the change touches.
2. Every reader and writer of the affected objects: application models/ORM
   mappings, raw queries, background jobs, event producers serializing the
   fields, analytics extracts (CDC, warehouse sync), and reporting queries.
3. The deploy model: rolling vs blue/green, how long old and new code
   versions overlap, and whether a migration can be ordered relative to a
   deploy (this determines the compatibility window each stage must survive).
4. Data volume and write rate of the affected tables — backfill duration
   and lock behavior scale with them.
5. Prior evolution history in the repo (migration directory conventions,
   any existing deprecation register or schema changelog).

## Workflow

1. **Classify the change.** Additive (new nullable column, new table) —
   safe in one stage. Mutating (rename, split, retype, constraint
   tightening) — requires the full expand→migrate→contract sequence.
   Destructive (drop) — only ever the LAST stage of a sequence, never the
   first.
2. **Enumerate consumers.** For each affected object, list every reader and
   writer found in the inputs, including the non-obvious ones: event
   payload serializers, analytics extracts, ad-hoc reporting. Each consumer
   is a row that must be dispositioned across the stages.
3. **Design the expand stage.** Introduce the new shape alongside the old —
   new column/table, nullable or defaulted, no old object touched.
   Compatibility guarantee to state: old code ignores the new shape
   entirely; new code can read old rows (null-tolerant reads).
4. **Design the migrate stage.** Dual-write from application code (writes
   land in both shapes), backfill existing rows in batches, then move reads
   to the new shape behind a verifiable switch. State the guarantee both
   directions: either code version produces rows the other can read. The
   backfill's operational execution is handed to
   `data-migration-runbook-author`; this plan states WHAT must be true
   after it (row parity, checksum match).
5. **Design the contract stage.** Stop dual-writes, mark the old shape in
   the deprecation register (object, replaced-by, earliest-drop release,
   evidence required), and only schedule the physical drop after the gate
   in step 6 passes. Constraint tightening (NOT NULL, narrowed type)
   belongs here, never in expand.
6. **Define per-stage verification gates.** Each stage ends with an
   observable check before the next starts: expand — schema present, no
   errors from old code; migrate — parity evidence (counts/checksums, reads
   served from new shape); contract — proof of zero readers of the old
   shape over a stated window (query stats, log scan) before any drop.
7. **Map each stage to release boundaries.** State which stage rides which
   deploy, what the rollback of each stage is (expand and dual-write stages
   roll back by reverting code; post-contract rollback requires the
   deprecation register's restore note), and where the point of no return
   is — the physical drop.
8. **Hand off.** Each stage's migration file → `secure-migration-reviewer`
   before it ships; the backfill/cutover execution →
   `data-migration-runbook-author`; the finished plan is recorded per the
   repo's decision conventions.

Stage-design details, the compatibility matrix, and the deprecation
register format:
[references/evolution-stage-playbook.md](references/evolution-stage-playbook.md).

## Output Format

```
SCHEMA EVOLUTION PLAN — <object(s)>
Change class:   additive | mutating | destructive-terminal
Consumers:      <N readers / M writers enumerated, incl. events + analytics>
Stage 1 EXPAND:   <DDL intent> — compat: <old×new guarantee> — gate: <check>
Stage 2 MIGRATE:  <dual-write + backfill + read-switch> — compat: <both directions> — gate: <parity evidence>
Stage 3 CONTRACT: <stop dual-write; deprecation-register entry; drop schedule> — gate: <zero-reader evidence over window>
Release mapping:  <stage → deploy/release boundary>
Rollback:         <per stage; point of no return = physical drop>
Handoffs:         migrations → secure-migration-reviewer; execution → data-migration-runbook-author
Not covered:      <explicitly out of scope for this plan>
```

## Validation Checklist

- [ ] Every stage keeps both adjacent code versions working, and the
      guarantee is stated per stage in both directions.
- [ ] No stage both introduces and removes a shape; drops appear only in
      contract, after a zero-reader gate.
- [ ] The consumer enumeration includes event serializers and analytics
      extracts, not just application code.
- [ ] Every stage has an observable verification gate; none is "wait and
      hope".
- [ ] Backfill execution is handed off, not embedded as shell commands here.
- [ ] The deprecation register entry exists for anything left physically
      present but logically dead.
- [ ] Rollback is stated per stage and the point of no return is explicit.

## Gotchas

- Renames are never renames: a true in-place rename breaks whichever side
  deploys second. It is always add-new → dual-write → switch reads → drop
  old, even when the tooling offers a one-line rename.
- The forgotten readers are analytics and events: the application compiles,
  but the warehouse extract or an event payload still serializes the old
  column. Consumer enumeration exists because of these two.
- Constraint tightening is a contract-stage move: adding NOT NULL or
  narrowing a type during expand fails on rows old code keeps writing.
- Long-running backfills on hot tables can hold locks or bloat the store —
  the plan states batching intent and hands sizing to the runbook; a plan
  that says "UPDATE all rows" has not engaged with volume.
- Dual-write drift: without a parity check, the two shapes silently
  diverge and the read-switch flips onto wrong data. The migrate gate is
  parity evidence, not elapsed time.
- Deprecation registers rot: an old column kept "temporarily" with no
  earliest-drop release and no owner is permanent. Register entries carry
  both.
- ORM default eagerness: some data layers SELECT every column, so "no code
  references it" is false until the model definition drops the field too.

## Stop Conditions

- Asked to plan a one-deploy breaking change ("rename it tonight, deploy
  everything together") → refuse the single-stage form; present the staged
  plan and state what the one-shot version breaks during the deploy
  overlap. A human may still choose downtime — that choice is theirs,
  recorded, not the planner's default.
- Consumer enumeration cannot be completed (unknown readers, no query
  visibility, opaque integrations) → stop and say which consumers are
  unverifiable; a plan gated on "probably nobody reads it" is not a plan.
- The change is destructive FIRST (drop now, fix consumers later) → refuse
  and re-sequence; data loss cannot be staged around after the fact.
- The affected store's tenant-scoping model is itself in question (the
  change alters isolation, not just shape) → halt and route the isolation
  design to `multi-tenant-data-architect` before sequencing anything.
- Asked to also produce the operator runbook or run the backfill → decline
  that slice; hand to `data-migration-runbook-author` (authoring) and a
  human-approved execution.

## Supporting Files

- [references/evolution-stage-playbook.md](references/evolution-stage-playbook.md)
  — per-stage design details, the old×new compatibility matrix, backfill
  handoff contract, deprecation-register format, and gate evidence examples.
- `evals/evals.json` — behavior cases including the live-rename edge and
  the one-deploy-breaking-change refusal.
- `evals/trigger-evals.json` — discrimination against
  `secure-migration-reviewer`, `data-migration-runbook-author`,
  `multi-tenant-data-architect`, and `streaming-event-architect`.
