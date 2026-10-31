# Clickthrough Route Catalog

Detail file for `clickthrough-test-engineer`. Loaded on demand.

The owning [clickthrough test skill](../SKILL.md) defines execution scope.
ESC means the Escape key, CTA call to action, and QA quality assurance.
Viewport means the browser display dimensions used for the check.

## Per-route interaction checklist

Apply the rows that exist on the route; mark N/A explicitly.

| Item | What to do | Common failures |
| --- | --- | --- |
| Direct navigation | hit the URL cold (new tab) | guard missing, infinite spinner, crash on no-state |
| In-app navigation | reach via menus/links | dead links, wrong active state |
| Forms — valid | submit realistic valid input | silent failure, no feedback, double-submit duplicates |
| Forms — invalid | empty required, over-length, wrong format, paste junk | no validation, cryptic errors, data loss on error |
| Dialogs/modals | open, ESC, backdrop click, cancel, confirm | focus lost, background scroll, state leak after cancel |
| Permission gates | try controls per persona (member vs admin) | hidden-but-callable actions, visible-but-broken controls |
| Empty states | route with zero data | raw "undefined", broken layout, no CTA |
| Loading states | throttle/first load | layout shift, spinner forever on error |
| Error states | trigger a failing action where safe | blank screen, unhandled rejection in console |
| Destructive actions | delete/remove on session fixtures ONLY | no confirmation, confirmation deletes wrong thing |
| Back/refresh | browser back after submit; F5 mid-flow | resubmission, lost state, auth loop |
| Console | check on every route | errors/warnings on "working" pages |

## Table interactions (sorting, filtering, result sets)

Apply this section whenever a route shows a data table or a sortable/filterable
list. Each result set is checked against an independent expected answer derived
from the fixture data, never against what the screen currently shows.

| Check | What to do | Common failures |
| --- | --- | --- |
| Sort — whole-list order | derive the expected order of EVERY row from the fixture (date and number columns), then compare the rendered order row-by-row | only first/last row checked, sampled rows, order trusted from the view |
| Sort — both directions | exercise ascending AND descending, and re-derive the expected list for each | one direction untested, direction silently ignored |
| Sort — fixture shape | use a deliberately unsorted/mixed fixture; an already-sorted fixture cannot prove the comparator runs | sorted fixture masks a broken/absent sort |
| Sort — nulls and ties | apply the product's stated null rule (first/last/excluded) and tie rule (deterministic tie-break, or explicitly documented undefined order) with at least one null and one tie case | nulls crash or land inconsistently, ties reorder between renders |
| Filter — membership and count | for each filter derive the expected member set and count independently; assert no stale rows remain after changing filters | stale rows, wrong count, filter silently ignored |
| Filter + sort composition | apply a filter after sorting (and the reverse) and assert both semantics hold | one control resets the other |
| Pagination/total count | where pagination exists, check the count and boundary behavior of filtered/sorted sets | count reflects unfiltered data, boundary duplicates/omissions |
| Empty-result recovery | trigger a filter with zero matches; confirm the empty state explains the result, filter/query state stays visible or is clearly reset, and a recovery path (clear/reset) exists | blank page, crash, filter cannot be cleared, state lost |

## Viewport set

Default: desktop 1280×800 + one mobile width (375×812) on customer-facing
routes. Deep responsive QA is its own effort; here mobile only needs to be
usable on the critical routes.

## Session evidence defaults

Used when no `screenshot-evidence-planner` policy exists:
- Name: `<route>--<step>--<pass|defect>--<yyyymmdd-hhmm>.png`
- Mask: emails, names, tokens, ids that look real — before storage.
- Store: the session's report directory, referenced from the defect table.
- Metadata: build id + persona + viewport in the report row, not burned into
  the filename beyond the pattern above.

## Severity rubric

- **Blocker:** journey cannot proceed / data loss / security-relevant.
- **Major:** feature broken with no workaround.
- **Minor:** broken with workaround, or wrong-but-recoverable.
- **Cosmetic:** visual/copy issues.

Security-relevant observations (cross-tenant data visible, hidden admin
control callable) are filed as blockers AND routed to the security skills —
never sat on until the report is done.
