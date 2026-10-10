# Coverage Mapping Method

Detail file for `test-coverage-mapper`. Loaded on demand.

## Surface inventory recipe

Enumerate before judging. Typical sources:

| Surface kind | Where to find it |
| --- | --- |
| Routes/pages | router config, pages/app directory |
| API endpoints | route handlers, OpenAPI spec, controller files |
| Commands/services | command handlers, service classes, use-case modules |
| Schema | migrations, table definitions (row-level security (RLS) tables flagged) |
| Background jobs | queue/cron definitions |
| Integrations | webhook handlers, provider clients |

Record each with a stable ID so the map is diffable across audits. For
example, `route:tenant-invoice-read` can map to
`tests/invoices.test.ts:42`, layer `integration`, bucket `covered` only when
that assertion verifies the authorized response and tenant boundary.

## Verifying vs theater rubric

A test VERIFIES a surface when it asserts observable behavior a user or
consumer depends on. Theater signals:

- No assertion, or assertions that cannot fail (`expect(true).toBe(true)`).
  `expect(result).toBeDefined()` on a constructor result usually proves only
  construction, not required behavior.
- Render-only component tests (mounts, asserts nothing about behavior).
- Snapshot-everything tests nobody reviews on update.
- Asserting against the mock itself (mock called with X, where X is the only
  thing the test set up — circular).
- Integration tests where every boundary is mocked: reclassify to unit at
  best; the boundary is NOT covered.

When in doubt, ask: "what real bug would make this test fail?" No answer →
theater.

## Gap-ranking worksheet

For each uncovered/theater surface:

1. Impact if broken: data loss / money / security / journey blocked / cosmetic.
2. Likelihood: change frequency (git churn), complexity, incident history.
3. Detection without a test: would anything else catch it before users?

Rank = impact-first, likelihood as tiebreaker, low-detectability promotes.
Security-relevant gaps (tenant/authorization) are always reported, with specification
delegated to `multi-tenant-security-tester`.

## Mutation-report rubric

When a mutation-testing report is supplied, read it into the map:

- **Killed** mutants: the suite already distinguishes the behavior — no gap.
- **Survived** mutants: no test distinguishes the mutated behavior — gap
  evidence; map each actionable survivor to the surface it exposes.
- **Equivalent** mutants: the mutation changed nothing observable (renamed
  variable, dead branch) — no test CAN distinguish it; exclude with a
  written reason, never count as a gap.

A mutation score is a lead, not a verdict: triage survivors into
"equivalent (excluded)" and "actionable (mapped)" before any gap claim.
Running the mutation tool or writing killing tests stays with the engineer
skills; this method consumes reports and maps gaps.

## Coverage statement discipline

Report four buckets with counts: covered / theater / uncovered /
not-inspected. "Not-inspected" is honest scope-cutting; omitting it converts
a partial audit into a false whole-scope claim.
