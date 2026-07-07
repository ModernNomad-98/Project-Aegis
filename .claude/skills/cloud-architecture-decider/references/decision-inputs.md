# Decision Inputs Reference

Detail file for `cloud-architecture-decider`. Loaded on demand.

## Nine-axis requirements record template

| Axis | Question to answer | Typical source | Verified/Assumed |
| --- | --- | --- | --- |
| Compliance & residency | Which certifications do customers demand? Where must data live? | Contracts, security questionnaires, DPAs | |
| Latency & regions | Where are users? Acceptable p95? Edge/offline needs? | Analytics, contracts, product | |
| Availability target | What outage length is survivable commercially? | SLAs sold, `slo-reliability-architect` output | |
| Cost envelope | Monthly ceiling? Committed spend/credits + expiry? | Bills, finance, contracts | |
| Operational maturity | What has THIS team run in production? On-call depth? | Team history, incident record | |
| Existing estate | Current provider footprint, IaC, CI/CD, IdP? | Repos, bills, console inventory | |
| Integration gravity | What provider-specific services does the product already depend on? | Code, IaC, vendor list | |
| Scale trajectory | Tenants/traffic in 12–24 months? Spiky or steady? | Funnel data, sales pipeline | |
| Exit-cost tolerance | How bad is being stuck? Acquisition/customer-mandate risk? | Leadership, board constraints | |

## Hard-filter derivation

Filters eliminate options before scoring. Derive from:

- **Tenancy model** (`saas-platform-architect`): database-per-tenant silo →
  needs cheap per-DB pricing or schema automation; pooled → needs strong
  row-level isolation primitives. A model the provider prices punitively is
  a filter, not a scoring penalty.
- **Residency**: required regions/sovereign clouds the provider must offer
  today (verify region service availability, not just region existence).
- **Compliance**: certifications the provider holds for the services in
  scope, in the regions in scope.
- **Non-negotiable integrations**: services the product cannot leave
  (existing IdP, marketplace commitments, customer VPC peering).

## Scoring rubric (surviving options only)

Score each option 1–5 per axis, with a one-line written rationale per cell —
the rationale is the deliverable, the number is a summary:

| Axis | 5 looks like | 1 looks like |
| --- | --- | --- |
| Cost | Marginal per-tenant cost fits envelope incl. egress; credits usable | Punitive pricing under the chosen tenancy model |
| Operational fit | Team has run this shape in production | New paradigm + no hiring plan |
| Integration gravity | Estate already there / trivial adapters | Deep rework of identity, queues, IAM |
| Region coverage | All required regions, all required services | Gaps needing workarounds |
| Exit cost | Portable primitives, standard APIs | Proprietary services at the core |

Deployment postures to score alongside providers: single-provider,
multi-cloud (score its duplicated-expertise cost explicitly), hybrid
(on-prem + cloud), stay-as-is (always score the incumbent — migration cost
counts against challengers, not the incumbent).

## Managed-vs-self-hosted decision table

| Capability | Default | Self-host only when | Operational bill to accept |
| --- | --- | --- | --- |
| Relational DB | managed | proven cost at scale / capability gap | backups, HA, patching, upgrades, on-call |
| Object storage | managed | almost never | durability engineering |
| Queue/stream | managed | exotic semantics needed | broker ops, partition rebalancing |
| Search | managed | index size pricing / plugin needs | cluster ops, reindex windows |
| Kubernetes | managed control plane | regulatory/edge | node ops, upgrades, CNI/CSI debugging |
| Observability stack | managed | data-volume pricing at scale | storage, retention, query performance |

Every self-hosted row in the output must fill all three columns.
