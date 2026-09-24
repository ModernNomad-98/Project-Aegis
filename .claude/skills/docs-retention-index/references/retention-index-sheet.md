# Retention Index Sheet

Detail for `docs-retention-index`. Read on demand.

The owning [docs retention skill](../SKILL.md) defines the lifecycle decision.
YAML is the structured metadata format; frontmatter is the YAML block at the
start of a document; expiry is the date or event that triggers retention review.

## Retention categories

| Category | Meaning | Cleanup |
|---|---|---|
| Permanent / canonical | Source of truth; earns permanence | Never auto-cleaned; reason required |
| Reference-until-superseded | Useful until a successor replaces it | Retire when superseded-by is set |
| Time-boxed | Valid until a date/event | Review/retire at expiry |
| Transient / disposable | Served a one-time purpose | Remove after purpose met |

Every governed doc gets exactly one. "Permanent" must be EARNED by a
reason, not chosen by default.

## Per-doc frontmatter schema

```yaml
retention:
  category: reference-until-superseded   # one of the four
  reason: "canonical decision log for X"  # concrete why — never "just in case"
  superseded_by: null                     # path/id of successor, if any
  cleanup: "retire when superseded_by set"
  review: 2026-12-01                      # date/event, if time-boxed
```

The doc carries a copy of its lifecycle fields; the numbered index governs
the retention decision. Drift between frontmatter and index is a finding.

## Numbered index format

```
| # | Doc | Category | Reason-to-keep | Superseded-by | Cleanup | Review/expiry |
|---|-----|----------|----------------|---------------|---------|---------------|
| 01 | reconciliation.md | permanent | canonical plan | — | never | — |
| 07 | session-2026-05.md | transient | one session report | — | remove after 90d | 2026-08 |
```

The source of truth for what's kept, why, and until when. Each document's
frontmatter mirrors these fields so its metadata travels with it. Enter
new docs on creation and flag any index/frontmatter drift for correction.

## Reverse-reference sweep (before retiring)

1. Find everything that links to the doc: other docs, README, code
   comments, decision logs, indexes.
2. Disposition each reference: relink to successor / redirect / accept
   removal.
3. Only after the graph is clean do you stage removal.

Deleting without the sweep leaves dangling references.

## Retirement staging (mark → redirect → remove)

| Stage | Action | Reversible? |
|---|---|---|
| Mark | Set status superseded/expired; name successor | Trivially |
| Redirect | Grace window; point readers to successor | Trivially |
| Remove | Delete the doc within applicable human authorization, including any active grant | Revert only an isolated retirement commit; otherwise restore the targeted doc and references |

This skill plans/recommends; it does NOT execute deletions. Removal is a
operation governed by the applicable human authorization.

## Rot vs hoarding findings

- **Rot:** past review/expiry; superseded but still present; orphaned (no
  inbound references and no reason).
- **Hoarding:** "permanent" with no reason-to-keep; keep-everything with
  no category.

Both push toward an explicit keep-or-retire decision.
