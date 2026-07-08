# ADR Corpus Sheet

Detail for `adr-sequencer`. Read on demand.

## Index / log format

A single navigable list — the front page of the decision history:

```
| # | Title | Date | Status | Supersedes | Superseded by |
|---|-------|------|--------|-----------|---------------|
| 0001 | Use modular monolith | 2026-01 | Accepted | — | — |
| 0012 | Cache with Redis | 2026-03 | Superseded | — | 0045 |
| 0045 | Cache with in-process LRU | 2026-06 | Accepted | 0012 | — |
```

Keep it current; it's the difference between a corpus and a landfill.

## Status lifecycle

```
Proposed ──► Accepted ──► Deprecated
    │            │
    └► Rejected  └► Superseded (by newer ADR)
```

- **Proposed** — under discussion.
- **Accepted** — the current decision.
- **Rejected** — considered and declined (kept as record).
- **Deprecated** — no longer recommended, no direct replacement.
- **Superseded** — replaced by a specific newer ADR (link it).

Every ADR has exactly one current status. Superseded/rejected records
STAY in the corpus.

## Superseding links (bidirectional)

- New ADR: "Supersedes ADR-0012".
- Old ADR: status → Superseded; "Superseded by ADR-0045".
- Chains preserved: 0012 → 0045 → 0061 reads as an evolution, not a
  mystery.

## New ADR vs amendment

| Change | Action |
|---|---|
| Decision itself changes | NEW ADR that supersedes the old |
| Consequence/tradeoff materially changes | NEW ADR (or amend with dated note if minor) |
| Typo, broken link, formatting | Amend in place, dated note |
| Clarification that doesn't change meaning | Amend in place, dated note |

Never disguise a material decision change as an "amendment" — it makes
the history lie.

## Append-only principle

An ADR records what was decided and WHY, at a point in time. Editing it to
change the decision erases that. Supersede; don't overwrite. Delete
nothing that was ever accepted or rejected.

## Contradiction scan

1. List currently-Accepted ADRs.
2. Look for pairs whose decisions can't both hold now (same topic,
   opposite calls).
3. For each: is one actually superseded (fix the link) or is there a real
   live conflict?
4. Resolve a live conflict with a new superseding/reconciling ADR
   (authored via `adr-writer`). Contested facts → `source-of-truth-reconciler`;
   a genuinely new decision → `architecture-designer`.
