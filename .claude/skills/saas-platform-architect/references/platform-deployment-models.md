# Platform Deployment Models & Control-Plane Catalog

Use this reference with the [SaaS Platform Architect](../SKILL.md). Read on
demand.

## Deployment model catalog (decided per component)

| Model | What it means | Isolation mechanism to name | Costs to name |
| --- | --- | --- | --- |
| Pooled | All tenants share the instance/store | Row scoping (tenant key + enforced filter/RLS), tenant-scoped cache keys, per-tenant queue partitions | Noisy neighbor, blast radius = all tenants, isolation is code-enforced |
| Siloed | Dedicated instance/store per tenant | Physical separation | Provisioning automation, per-tenant upgrades/migrations, fleet drift, cost floor per tenant |
| Bridge / mixed | Pooled default with siloed exceptions | Both of the above + routing layer that maps tenant → home | Routing correctness becomes an isolation control; two operational paths to maintain |

Decision drivers, in the order they usually dominate: compliance/residency
mandates → largest-tenant blast radius and noisy-neighbor exposure → per-tenant
cost floor → operational capacity to run a fleet.

## Control-plane capability checklist

Every platform needs an answer (present / partial / missing / deferred) for:

- Tenant management: provision, suspend, offboard, purge.
- Identity: IdP integration, token/session shape, where tenant context is bound.
- Membership & invitations (semantics from `tenant-modeler`).
- Entitlements & plan resolution (design via `plan-entitlement-architect`).
- Billing integration and its reconciliation path.
- Platform audit log (design via `audit-log-architect`).
- Support tooling: brokered, scoped, audited access — never raw DB access.
- Feature flags with tenant/plan/cohort targeting.
- Analytics: tenant-tagged, aggregation rules that don't leak small cohorts.

Control-plane capabilities may be pooled, siloed, or mixed. Choose the model
per capability and document tenant routing, authority boundaries, residency,
and the operational cost of the selected model.

## Single-tenant → multi-tenant conversion patterns

1. **Identity first** — introduce tenant context into authentication and
   session/token shape while everything else stays single-tenant.
2. **Data scoping second** — add tenant keys and scoping to stores (design
   with `multi-tenant-data-architect`); backfill with the single existing
   tenant; verify counts.
3. **Enforcement third** — make scoped reads and writes fail closed, and run
   dual-read verification before cutting over. A flag may control rollout
   timing but must never bypass tenant authorization.
4. **Onboard tenant #2 last** — only after effective tenant scoping is
   enforced and negative tests prove tenant #1 cannot be reached from the
   new tenant's context
   (`tenant-isolation-reviewer`).

Each step ships alone and rolls back alone. The rollback for step N must not
require rolling back step N-1.
