---
name: docs-retention-index
description: Design the numbered retention index governing every workflow/process doc's LIFECYCLE — each doc gets a retention category, a reason-to-keep, a superseded-by pointer, and a cleanup rule, mirrored by per-doc retention frontmatter, so doc retirement becomes an explicit, approvable operation instead of silent rot or hoarding. Runs the reverse-reference sweep before retiring a doc, stages retirement (mark → redirect → remove) with human approval for deletion, and keeps the index the source of truth for what's kept, why, and until when. The DOC-lifecycle counterpart to skill-deprecation-planner (which retires a library SKILL) — pinned both ways. Use when governing doc retention/retirement, building a doc index with lifecycle metadata, or deciding which docs to keep, supersede, or delete. Do NOT use to retire a library SKILL (skill-deprecation-planner), sunset a PRODUCT feature/API to users (sunset-deprecation-communicator), or organize docs by type (diataxis-doc-organizer).
---

# Docs Retention Index

## Purpose

Workflow and process docs accumulate in two failure modes at once: rot
(stale session reports, superseded plans, and dead runbooks nobody
removes because nobody's sure it's safe) and hoarding (keep everything
forever, just in case, until the folder is archaeology). Both come from
the same gap — no doc ever declared how long it should live or why. This
skill designs the numbered retention index that closes it: every governed
doc gets a retention category, a reason-to-keep, a superseded-by pointer,
and a cleanup rule, mirrored by per-doc frontmatter so each doc declares
its own lifecycle. Retirement becomes an explicit, approvable operation —
a reverse-reference sweep, then mark → redirect → remove, with deletion
human-approved. It is the DOC-lifecycle counterpart to
`skill-deprecation-planner`, which retires a library SKILL; the two are
pinned against each other in both directions.

## Use When

- Use when: governing the retention/retirement of workflow, process,
  session, or operational docs — deciding what to keep, supersede, or
  delete, and why.
- Use when: building a doc index with lifecycle metadata (retention
  category, reason-to-keep, review date, superseded-by).
- Use when: docs have rotted (stale/superseded docs nobody removed) or
  been hoarded (keep-everything with no reason), and retention needs a
  governing rule.
- Use when: a doc is being retired and needs the reverse-reference sweep
  and a staged, approvable removal.
- Do NOT use when: the object being retired is a library SKILL (its
  mark→redirect→remove lifecycle, neighbor trigger-eval sweep, catalog/
  README rows) — that is `skill-deprecation-planner`; different object,
  and it already references this seam.
- Do NOT use when: the task is communicating a PRODUCT feature/API sunset
  to external users (migration path, timeline, comms) — that is
  `sunset-deprecation-communicator`.
- Do NOT use when: the task is organizing docs by TYPE (tutorials/how-to/
  reference/explanation) — that is `diataxis-doc-organizer`; this governs
  lifecycle, not taxonomy.

## Inputs to Inspect

1. The doc corpus in scope: the workflow/process/session/operational docs
   this index governs, where they live, and their age/last-touched dates.
2. Existing lifecycle signals: any current index, frontmatter, or naming
   convention indicating retention or supersession (usually none — that's
   the gap).
3. Supersession relationships: docs clearly replaced by newer ones but
   never marked/removed, and canonical source-of-truth docs everything
   else defers to.
4. The reverse-reference graph: what links to each doc — other docs, code,
   READMEs, decision logs — so retiring one doesn't create dangling
   references.
5. The repo's removal mechanics and approval path: how deletions are made
   and approved (and the squash-merge revert convention, per D19), so
   retirement rollback is correct.

## Workflow

1. **Define retention categories.** A small, clear set — e.g. permanent/
   canonical (source of truth, never auto-cleaned), reference-until-
   superseded, time-boxed (expires after a stated date/event), and
   transient/disposable (safe to remove after its purpose). Every governed
   doc gets exactly one.
2. **Assign per-doc lifecycle fields.** For each doc: retention category,
   a REASON-TO-KEEP (not "just in case" — a concrete why), superseded-by
   (if any), a cleanup rule, and a review/expiry date where applicable.
   Retention without a reason is hoarding; a reason makes keep-or-remove
   decidable.
3. **Mirror it in per-doc frontmatter.** Each doc declares its own
   lifecycle in frontmatter so the metadata travels with the doc and the
   index can be regenerated/checked against it. The doc and the index
   agree; drift between them is a finding.
4. **Build the numbered index.** A single numbered index listing every
   governed doc with its retention fields — the source of truth for what's
   kept, why, and until when. New docs are entered on creation.
5. **Make retirement an approvable operation.** Before retiring a doc, run
   the REVERSE-REFERENCE sweep (everything that links to it) and give each
   a disposition (relink, redirect, or accept removal). Then stage: mark
   (superseded/expired, successor named) → redirect for a grace window →
   remove. DELETION is human-approved — this skill plans and recommends;
   it does not delete.
6. **Detect rot AND hoarding.** Flag docs past their review/expiry,
   superseded-but-present, and orphaned; equally, flag "permanent" docs
   with no reason-to-keep (hoarding by default). Push both toward an
   explicit decision.
7. **Specify rollback.** Retiring a doc must be reversible: in a
   squash-merge repo, a removal reverts as one ordinary commit (honor the
   D19 convention). State the rollback per retirement.
8. **Deliver** the index, the frontmatter convention, and the per-doc
   dispositions in the Output Format — with deletions flagged for human
   approval.

Retention-category definitions, the per-doc frontmatter schema, the
reverse-reference sweep checklist, and the mark→redirect→remove staging:
[references/retention-index-sheet.md](references/retention-index-sheet.md).

## Output Format

```
DOCS RETENTION INDEX — <scope: workflow/process docs>
Categories:    permanent/canonical | reference-until-superseded | time-boxed | transient
Index (numbered):
  <NN | doc path | category | reason-to-keep | superseded-by | cleanup rule | review/expiry>
Frontmatter:   per-doc retention fields (mirrors the index; drift = finding)
Retirements (recommended):
  <doc>: reverse-ref sweep result; disposition (relink/redirect/remove);
         stage=mark→redirect→remove; rollback=<one-commit revert>; DELETION = human-approved
Findings:      rotted (past expiry / superseded-present / orphan); hoarded (permanent, no reason)
Boundaries:    SKILL retirement → skill-deprecation-planner; product sunset →
               sunset-deprecation-communicator; corpus-by-type → diataxis-doc-organizer
```

## Validation Checklist

- [ ] A small, clear set of retention categories is defined; every
      governed doc has exactly one.
- [ ] Each doc has a concrete reason-to-keep (not "just in case"),
      superseded-by, cleanup rule, and review/expiry where applicable.
- [ ] Per-doc frontmatter mirrors the index; drift between them is flagged.
- [ ] A single numbered index is the source of truth for what's kept, why,
      and until when.
- [ ] Retirement runs a reverse-reference sweep and stages mark → redirect
      → remove; DELETION is human-approved, not executed here.
- [ ] Both rot (stale/superseded/orphan) and hoarding (permanent without a
      reason) are surfaced.
- [ ] Rollback is stated per retirement (one-commit revert in a
      squash-merge repo).
- [ ] SKILL-retirement, product-sunset, and corpus-by-type concerns are
      handed to their owning skills.

## Gotchas

- Rot and hoarding are the same disease: no doc ever said how long it
  should live. The reason-to-keep field is the cure for both — it makes
  "keep" a decision, not a default.
- "Permanent" with no reason is hoarding wearing a badge. Canonical
  source-of-truth docs earn permanence; a session report from last year
  doesn't. Demand the reason.
- Deleting a doc without the reverse-reference sweep breaks every link
  into it — a dead cross-reference in the README, a decision log pointing
  at nothing. Sweep first, disposition each reference, then remove.
- Retiring by editing history in place (or hard-deleting a superseded doc
  that others cite) destroys traceability. Mark and redirect through a
  grace window; supersede visibly.
- This skill plans retirement; it does not delete. Executing a deletion is
  a human-approved operation — quietly removing docs is exactly the silent
  behavior the index exists to prevent.
- Retiring a DOC is not retiring a SKILL. A skill's retirement sweeps
  neighbor trigger-evals and catalog rows and is `skill-deprecation-planner`'s
  job; conflating them applies the wrong reverse-link graph.
- An index that drifts from the docs' own frontmatter is two sources of
  truth. Mirror them and treat divergence as a finding, or the governance
  rots like the docs it governs.

## Stop Conditions

- The object being retired is a library SKILL → route to
  `skill-deprecation-planner` (it owns the skill lifecycle and already
  pins this seam from its side).
- The task is communicating a PRODUCT feature/API sunset to external users
  → route to `sunset-deprecation-communicator`.
- The task is organizing docs by type → route to `diataxis-doc-organizer`.
- A retirement recommendation would DELETE a doc → stop at the recommend
  stage and require explicit human approval for the deletion; this skill
  governs and plans, it does not execute removals.

## Supporting Files

- [references/retention-index-sheet.md](references/retention-index-sheet.md)
  — retention-category definitions, the per-doc frontmatter schema, the
  reverse-reference sweep checklist, and the mark→redirect→remove staging
  with rollback.
- `evals/evals.json` — behavior cases including the reason-to-keep
  discipline, the reverse-reference sweep, and the human-approved-deletion
  refusal.
- `evals/trigger-evals.json` — discrimination against `skill-deprecation-planner`
  (DOC vs SKILL — the pinned seam), `sunset-deprecation-communicator`, and
  `diataxis-doc-organizer`.
