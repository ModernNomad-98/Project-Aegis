# Review Severity Rubric & Pass Checklists

Supporting detail for `code-reviewer`. Read on demand.

The owning [code review skill](../SKILL.md) defines the verdict process.
Authz means authorization, authn authentication, SSRF server-side request
forgery, N+1 one query per item after an initial query, CI continuous
integration, and ADR architecture decision record.

## Severity definitions

| Severity | Definition | Boundary examples |
| --- | --- | --- |
| **BLOCKER** | Merging causes incorrect behavior, data loss/corruption, a security hole, or an unrecoverable operational state on a plausible path. | Missing authz on a new endpoint; migration drops a column still read by deployed code; unhandled rejection crashes the worker loop. |
| **MAJOR** | A real defect or serious risk, but on an edge path, recoverable, or currently unreachable — will bite later if not now. | Race on concurrent update of the same row; retry without idempotency on a payment call; N+1 that's fine at 10 rows and fatal at 10k; failing tests marked skipped so the change goes green; a user interface component querying the database directly against an ADR that requires the service layer. |
| **MINOR** | Worth fixing, does not threaten correctness or safety. | Missing test for an error branch; misleading function name; duplicated constant. |
| **NIT** | Style/preference; the author may reasonably decline. | Ordering of imports; comment phrasing; `map` vs loop taste. |

Escalation rules: a MINOR in security-adjacent code escalates one level.
Weakened validation (tests deleted or skipped, assertions loosened, timeouts
or retries raised, CI steps removed) is at least MAJOR unless the stated
intent explains it. Drift from a recorded ADR or documented layering rule is
MAJOR and cites the ADR; convention drift with no recorded decision stays
MINOR or NIT.
A pattern repeated across the diff is one finding at the pattern's severity,
listing occurrences — not N duplicate findings.

## Severity is impact, not certainty

Certainty is expressed separately: a suspected BLOCKER you couldn't verify is
written as `[BLOCKER?] needs verification: <what would confirm it>` — never
silently downgraded to MINOR because you weren't sure.

## Pass checklists (expanded)

**Correctness:** inverted/short-circuited conditions; off-by-one at loop and
pagination boundaries; null/undefined/empty/zero/NaN handling; error paths
that swallow or double-handle; float money math; timezone-naive datetimes;
mutation of shared references; async ordering assumptions; missing `await`.

**Security:** input validation at every new boundary; authz (not just authn)
on new routes/queries — object-level, not just role-level; parameterized
queries; template/HTML escaping; secrets or tokens in diffs, configs, logs,
or test fixtures; unsafe deserialization/dynamic eval; tenant scope on every
new data access; SSRF on new outbound fetches with user-influenced URLs.

**Reliability:** timeout on every new network call; retry with backoff and a
cap, idempotent or guarded; partial-failure behavior of multi-step
operations; resource cleanup on error paths (connections, files, locks);
queue/stream consumers that can't poison-loop.

**Performance:** queries inside loops; missing index for the new query shape
(check the migration!); payloads that grow with data volume; hot-path
allocations; caches without eviction or with cross-tenant keys.

**Tests:** the revert test — would the suite fail if the diff's behavior
change were undone? New error paths exercised, not just happy paths;
assertions on behavior rather than snapshots-of-everything; fixtures that
don't encode the bug being fixed.

**Validation integrity:** tests deleted, skipped, marked as expected to
fail, or narrowed with a focus marker such as `.only` so the rest never run;
assertions loosened (exact value to "truthy", fewer fields checked, wider
tolerance); snapshots regenerated without a reason; timeouts or retry counts
raised; CI steps, linters or coverage gates removed or made non-blocking.
Deleting a test together with the feature it covered is not a finding when
the stated intent says so. A removed or disabled security scan is also a
security finding; recommend `security-pr-reviewer` for that part.

**Architecture decisions:** the ADRs and layering rules that cover the
changed files; calls that skip a required layer; a dependency direction the
ADR forbids; a pattern the ADR superseded. Cite the ADR and the line that
breaks it.

**Migrations:** forward-only safety while old code still runs (add-then-use,
never rename-in-place); rollback statement or explicit "irreversible because";
long-running table locks on large tables; deploy-order dependency stated.

## Anti-noise rules

- Max one style/convention comment per pattern; link the convention.
- Do not restate what the diff does — findings only.
- "Consider…" without a reason is deleted; every suggestion carries its why.
- Praise is allowed and specific ("the retry guard on L84 closes the old
  double-charge window") — it teaches as much as criticism.
