# Deprecation stage playbook

Companion to [../SKILL.md](../SKILL.md). Checklists and formats for the
staged retirement of a library skill. Everything here is PLAN material —
execution of any stage is a separate, human-approved operation.

## Reverse-link sweep procedure

Purpose: find every inbound reference so none dangles after removal.

1. Full-text search the repository for the skill's exact name (it is a
   kebab-case token — matches are high-precision). Surfaces to cover:
   - every other skill's `SKILL.md` (yield clauses in Use When,
     description "Do NOT use" lists, Supporting Files notes),
   - every `evals/trigger-evals.json` (`expected_skill`,
     `should_not_trigger`, `overlaps_with`, case `note`/`reason` text),
   - every `evals/evals.json` (assertion text naming the skill),
   - the catalog and README (rows, cluster notes, narrative),
   - agent definitions (subagents composing the skill),
   - CI/config files and templates.
2. One row per hit in the disposition table. A hit with no row blocks the
   plan.

## Disposition table format

```
| Reference (file:line) | Kind | Disposition | New target / new text |
| --- | --- | --- | --- |
| <neighbor>/SKILL.md:<n> | yield clause | repoint | "…that is <successor>" |
| <neighbor>/evals/trigger-evals.json:<case-id> | discrimination case | rewrite | case re-targeted to <successor> or removed with reason |
| docs/<catalog>:<n> | registration row | move | retired record entry |
| docs/<decision-log>:<n> | historical entry | annotate-historical | untouched — true when written |
```

Dispositions: **repoint** (successor takes the reference), **rewrite** (the
seam/clause no longer needs to exist), **move** (registration → retired
record), **annotate-historical** (provenance text stays; optionally gains a
"(retired <date>)" note where the convention allows).

## Stage 1 — MARK checklist

- [ ] Description gains the deprecation notice as its FIRST clause:
      `DEPRECATED (<date>) — superseded by <successor>; new requests go there.`
      (The description still triggers — that is intentional: it catches
      requests and redirects them during the window.)
- [ ] Catalog and README rows annotated deprecated + successor.
- [ ] NEW dated decision-log entry: trigger, evidence, successor, window
      end date, planned removal.
- [ ] Neighbors NOT yet edited (they still legitimately reference a
      present skill).
- Rollback: revert the marking commit(s); no other artifact moved.

## Stage 2 — REDIRECT window

- [ ] Window has an explicit end date recorded in the decision-log entry —
      open-ended deprecation is deprecation-by-neglect.
- [ ] Straggler monitoring named: instrumented invocation signal
      (`skill-usage-instrumenter` tier 1) if it exists, else tier-2
      self-report review at window end.
- [ ] New inbound references to the deprecated skill are review findings
      (the library-diff review of any PR in the window should flag them).
- Rollback: un-mark (revert stage 1) and record the reversal as a new
  decision-log entry; the window simply closes unexecuted.

## Stage 3 — REMOVE checklist

- [ ] Skill directory deleted in a dedicated PR whose intent declares the
      retirement and links this plan.
- [ ] Every disposition-table row executed in the SAME PR: repoints,
      rewrites, registration moves — neighbor trigger-evals updated here,
      not as a follow-up.
- [ ] Registration rows MOVED to the retired record (see below); count
      arithmetic decremented at every site a count appears (reuse the
      library's count-site list from its diff-review checklist).
- [ ] Final decision-log entry: removed, date, where the retired record
      lives.
- [ ] The PR reviewed by `library-diff-reviewer` against this plan —
      deviations are findings.
- Rollback: on a squash-merge platform the removal lands as ONE ordinary
  commit; `git revert <squash-sha>` restores the directory, registration
  rows, and neighbor edits in one step. On merge-commit platforms the
  revert needs the mainline-parent selection — state which platform
  applies. Rollback is itself a PR with the same review path.

## Retired-record conventions

- The catalog keeps a **Retired** section: skill name, dates (shipped →
  retired), trigger (superseded-by / absorbed-into / disuse / defect), and
  the decision-log entries that bracket its life.
- The README's shipped list drops the skill; the README does not need a
  retired section (the catalog is the record).
- Git history remains the full-content archive — the retired record is a
  pointer, not a copy of the skill body.

## Point-of-no-return honesty

The plan's rollback restores THIS repository. It cannot recall:

- external copies (consumers who vendored the skill directory),
- downstream libraries that imported the pattern,
- muscle memory (users who invoke the skill by name will get nothing —
  the stage-2 window exists to retrain that path while it still redirects).

State these limits in the plan rather than implying total reversibility.
