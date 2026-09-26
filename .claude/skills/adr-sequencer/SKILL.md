---
name: adr-sequencer
description: 'Manage a CORPUS of Architecture Decision Records over time — the longitudinal discipline atop adr-writer (which authors ONE ADR): numbering and the ADR index/log, the status lifecycle (proposed → accepted → deprecated → superseded), bidirectional superseding links so a new decision points at the one it replaces and vice versa, detecting and resolving contradictions between ADRs, deciding when a change is a NEW ADR vs an amendment, and keeping the decision history navigable and trustworthy as append-only. Composes adr-writer for single-record authoring; owns the collection. Use when standing up or curating an ADR log, superseding/deprecating a past decision, reconciling conflicting ADRs, or when the ADR folder has become an unnavigable pile. Do NOT use to author ONE ADR''s content (adr-writer), organize the whole docs corpus by type (diataxis-doc-organizer), or design the docs pipeline/toolchain (docs-as-code-architect).'
---

# ADR Sequencer

## Purpose

A single ADR is a decision written down; a hundred ADRs with no
management is a landfill you can't navigate — nobody knows which
decisions still hold, two "accepted" records quietly contradict each
other, and someone edits a three-year-old ADR in place, destroying the
history it existed to preserve. This skill manages the ADR CORPUS over
time: the index/log, sequential numbering, the status lifecycle, the
bidirectional superseding graph that lets a reader trace how a decision
evolved, contradiction detection, and the rule that keeps the record
trustworthy — ADRs are append-only history; you supersede, you don't
overwrite. It composes `adr-writer` for authoring any individual record
and owns everything about the collection: its order, its status, and its
navigability.

## Use When

- Use when: standing up an ADR log/index for a project, or curating one
  that's grown into an unnavigable pile.
- Use when: a past decision is being superseded or deprecated and the old
  and new ADRs need correct bidirectional links and statuses.
- Use when: two ADRs appear to contradict and the conflict must be
  surfaced and resolved.
- Use when: deciding whether a change warrants a NEW ADR (a material
  decision change) or an amendment (a clarification).
- Do NOT use when: the task is authoring ONE ADR's content — context,
  decision, alternatives, consequences, rollback — that is `adr-writer`,
  which this skill composes and does not replace.
- Do NOT use when: the task is organizing the whole documentation corpus
  by type (tutorials/how-to/reference/explanation) — that is
  `diataxis-doc-organizer`.
- Do NOT use when: the task is the docs toolchain/pipeline (generator,
  build, deploy, CI) — that is `docs-as-code-architect`.

## Inputs to Inspect

1. The existing ADR corpus: how many, their numbers, dates, current
   statuses, and where they live — plus the gaps (missing numbers,
   status-less records).
2. The index/log if any: whether a single navigable list of decisions
   exists, and how stale it is.
3. Superseding relationships already implied: decisions that clearly
   replace earlier ones but aren't linked, and any in-place edits that
   overwrote history.
4. Apparent contradictions: pairs of "accepted" ADRs whose decisions
   can't both hold now.
5. The team's ADR conventions: template in use (so new records match),
   numbering scheme, and where ADRs are expected to be referenced from
   (code, docs, PRs).

## Workflow

This automatic phase reads the corpus and produces proposed index/status/link
changes in the conversation. It does not renumber, amend, overwrite, or move
existing records. Their application requires the separately authorized manual
mutation route. Ordinary new ADR drafts go to `adr-writer` and its bounded
document-persistence contract; a proposed graph is not evidence of a file edit.

1. **Inventory and index.** List every ADR with its number, title, date,
   and current status in a single index/log — the navigable front page of
   the decision history. Propose missing numbers and statuses; label any
   unresolved human decision instead of inventing acceptance.
2. **Propose the status lifecycle mapping.** Each ADR is proposed, accepted,
   rejected, deprecated, or superseded — never ambiguous. A superseded ADR
   stays in the record (it's history) with its status and a pointer to
   its successor; it is not deleted.
3. **Propose the superseding graph both ways.** When a new decision replaces
   an old one, the NEW ADR names what it supersedes, and the proposed OLD ADR update is
   marked "superseded by <new>". Bidirectional links let a reader walk the
   evolution in either direction. Preserve the chain, don't collapse it.
4. **Enforce append-only history.** A decided ADR is not edited in place
   to change its decision — that erases the reasoning that was true when
   it was made. A changed decision is a NEW ADR that supersedes; propose
   typo/clarity amendments separately, dated and explicitly authorized before application.
5. **Draw the new-vs-amend line.** Material change to the decision or its
   consequences → new superseding ADR. Clarification, formatting, a fixed
   link → amendment with a dated note. State which and why. When the facts
   leave a genuine owner choice, explain that an amendment clarifies the
   existing record while a new ADR preserves it and records a changed
   decision. Compare only viable paths: why each fits, what history it
   preserves or risks obscuring, review/setup effort, ongoing upkeep and
   any money cost or unknowns. Recommend the path that keeps the decision
   history accurate, explain why and what evidence could change that call,
   then ask one decision question. Do not treat the answer as authority to
   edit existing records through this automatic phase.
6. **Detect contradictions and propose resolutions.** Scan for two current decisions
   that conflict; surface each pair and propose its resolution — usually a new ADR
   that supersedes one or reconciles both — rather than leaving the corpus
   self-contradictory. Contested FACTS behind a conflict go to
   `source-of-truth-reconciler` first.
7. **Propose navigation and references.** Draft area tags, related-ADR links,
   and code/doc pointers to the governing ADR. The log's job
   is that anyone can find the current decision on a topic and its
   history.
8. **Author via adr-writer.** Any individual ADR (new, or the superseding
   record) is drafted by `adr-writer`; this skill proposes its position,
   statuses and links. Deliver the corpus plan/index
   in the Output Format.

The ADR index format, the status lifecycle diagram, superseding-link
conventions, and the new-vs-amend decision guide:
[references/adr-corpus-sheet.md](references/adr-corpus-sheet.md).

## Output Format

```
ADR CORPUS PLAN — <project>
Index:         numbered list — <NNNN | title | date | status | supersedes/superseded-by>
Status plan:   evidenced current statuses; proposed updates and unresolved decisions labeled
Superseding:   bidirectional links proposed (new names old; old → superseded-by new)
Append-only:   history preserved; changed decisions = new superseding ADRs, not in-place edits
New-vs-amend:  <classification and reasons; if owner choice remains: plain
                terms, viable paths and reasons, history pros/cons, review/
                setup/upkeep and money cost or unknowns, recommendation and
                why, one decision question>
Contradictions:<conflicting pairs surfaced + resolution (superseding/reconciling ADR)>
Navigation:    grouping/tags; related-ADR links; code/docs → governing ADR
Authoring:     individual records → adr-writer
Boundaries:    corpus-by-type → diataxis-doc-organizer; pipeline → docs-as-code-architect
```

## Validation Checklist

- [ ] A single index/log lists every ADR with number, title, date, and
      status.
- [ ] Current statuses are evidenced; proposed statuses and unresolved human decisions are labeled.
- [ ] Proposed superseding links are bidirectional (new names old; old points to
      its successor).
- [ ] History is append-only — no decided ADR was edited in place to
      change its decision; changes are new superseding records.
- [ ] The new-ADR-vs-amendment line is applied with stated reasons.
- [ ] An unresolved owner-facing new-vs-amend choice explains terms,
      preservation tradeoffs, costs or unknowns, and a recommendation
      before one question; the automatic phase does not apply file edits.
- [ ] Contradictions are surfaced with proposed resolutions, not silently decided.
- [ ] Navigation and governing-ADR pointers are proposed; application claims require separate evidence.
- [ ] Individual-record authoring is delegated to `adr-writer`, not
      duplicated here.

## Gotchas

- Editing a decided ADR in place to "update" it destroys the very thing
  an ADR is for: the reasoning that was true at decision time. Supersede
  with a new record; never overwrite history.
- An ADR folder with no index is write-only memory — decisions go in and
  are never found again. The log is what makes the corpus usable.
- Superseding links that only point forward (or only back) leave readers
  stranded: from an old ADR they can't find what replaced it. Wire both
  directions.
- Two "accepted" ADRs that contradict each other are worse than no ADRs —
  they give false confidence in opposite directions. Detecting these is a
  primary job, not a nicety.
- Deleting a superseded ADR erases the trail. A superseded decision is
  still history; mark it, don't remove it.
- Confusing amendment with supersession blurs the record: a material
  decision change hidden as an "amendment" makes the history lie. Keep the
  line sharp.
- This skill doesn't rewrite `adr-writer`. Re-authoring single-ADR content
  here duplicates a neighbor; compose it.

## Stop Conditions

- The task is authoring ONE ADR's content (context/decision/alternatives/
  consequences/rollback) → route to `adr-writer`; this skill sequences and
  manages, it doesn't re-implement single-record authoring.
- A contradiction between ADRs rests on a contested FACT (which config/
  number/state is actually current) → route to `source-of-truth-reconciler`
  before writing a resolving ADR.
- Resolving a contradiction requires MAKING a new architecture decision
  (not just recording sequence) → the decision itself is
  `architecture-designer`'s; this skill wires the resulting ADR into the
  corpus once decided.
- The task is corpus-by-type organization or the docs pipeline → route to
  `diataxis-doc-organizer` or `docs-as-code-architect`.

## Supporting Files

- [references/adr-corpus-sheet.md](references/adr-corpus-sheet.md) — the
  ADR index format, the status lifecycle, superseding-link conventions,
  the new-vs-amend decision guide, and a contradiction-scan checklist.
- `evals/evals.json` — behavior cases including the supersede-not-overwrite
  discipline, the contradiction resolution, and the new-vs-amend call.
- `evals/trigger-evals.json` — discrimination against `adr-writer` (single
  vs corpus — the compose seam), `diataxis-doc-organizer`, and
  `docs-as-code-architect`.
