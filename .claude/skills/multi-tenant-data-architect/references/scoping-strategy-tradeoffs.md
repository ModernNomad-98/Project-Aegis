# Scoping Strategy Tradeoffs & Migration Patterns

Use this comparison with the [multi-tenant data architect](../SKILL.md) to
choose per-store isolation and plan a tenant-scoping retrofit. **DB** means
database, **ORM** means object-relational mapper, and **API** means application
programming interface. The uppercase `DELETE` and `DROP` entries are database
operations to plan and verify, not instructions to run from this reference.

## Scoping strategy tradeoff table (per store)

| | Pooled (tenant key) | Schema-per-tenant | Database-per-tenant |
| --- | --- | --- | --- |
| Isolation enforcement | Code/policy-enforced every query | Connection/search-path routing | Connection routing |
| Migration cost | One migration | × tenant count | × tenant count |
| Noisy neighbor | Shared everything; needs quotas | Shared instance resources | Depends on physical compute and I/O isolation; separate DB alone may still share resources |
| Cost floor per tenant | ~zero | Low | Instance/DB minimum |
| Tenant purge | DELETE + verify everywhere | DROP SCHEMA | DROP DATABASE |
| Fits | Many small tenants | Mid-count, moderate isolation optics | Few large/regulated tenants |
| Classic failure | One missing WHERE clause | Search-path bug routes to wrong schema | Fleet drift; forgotten tenant DB on old version |

Mixed is the common real answer: pooled default, database-per-tenant for the
few tenants whose contracts or size demand it, with a tenant→home routing
table that is itself treated as an isolation control.

## Tenant-context propagation mechanisms

| Mechanism | Where it binds | Watch for |
| --- | --- | --- |
| Middleware + scoped repository | Request middleware → repo constructor | Escape hatches: raw query access bypassing the repo |
| ORM default scope / global filter | Model layer | Code that disables the scope "temporarily"; bulk ops that skip hooks |
| DB session variable (+ policy) | Per-connection/session | Connection pooling resetting or leaking the variable across requests |
| Job context envelope | Queue message carries tenant id explicitly | Fan-out jobs that iterate tenants inside one context |

Whichever is chosen: one trusted binding point. A data-path API may accept
a tenant selector only after server-side membership and operation-scope
validation; raw client input never becomes query context. Enumerate escape
hatches in the design.

## Retrofit migration pattern (expand → contract)

1. **Expand** — add nullable tenant key columns; no behavior change. Rollback:
   drop columns.
2. **Backfill** — derive tenant ownership; write keys in batches. Rollback:
   keep the old read path active and stop the backfill; do not promise to
   undo writes by re-running it. Correct or quarantine bad assignments with
   a separately verified plan before switching reads.
3. **Verify** — per-tenant row counts vs expected ownership; spot checksums on
   the ambiguous tables; unresolved rows go to a quarantine report, not a
   default tenant.
4. **Enforce** — scoped reads/writes behind a flag; dual-read comparison in
   shadow mode first. Rollback: flip the flag.
5. **Contract** — make keys NOT NULL only after enforcement has soaked;
   retain the old path through the rollback window. Drop it in a later
   irreversible cleanup after evidence and approval. Rollback before that
   cleanup: redeploy the retained path and flip the flag; a dropped path
   cannot be restored by a flag alone.

The verification gate (step 3) is the difference between a migration and a
mass mis-assignment of customer data.
