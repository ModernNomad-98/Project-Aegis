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

## Abstraction ladder (rung selection)

Pick the **highest rung the workload tolerates**, then a provider within it — a
higher rung hands more operational surface (OS patching, account topology, IAM,
network) to the platform, the right default for a small team. Reach DOWN the
ladder only for a named reason (control, cost at proven scale, residency, a
capability the platform lacks). Named providers are **current market examples of
each category, not recommendations** — pricing, free tiers, and runtime limits
are volatile verification items, checked at decision time, never asserted.

| Rung (low→high abstraction) | You own vs the platform | Example providers | Fits when | Ceiling that forces a step |
| --- | --- | --- | --- | --- |
| IaaS / VPS | You: OS, patching, runtime. Platform: hardware. | Hyperscaler VMs, DigitalOcean Droplets, Linode | Full control; custom kernels/daemons; lift-and-shift | Ops burden exceeds team capacity |
| Container PaaS | You: the container. Platform: host, scaling, deploy. | Render, Railway, Fly.io | "Just deploy my app + DB"; long-running services | Pricing/scale limits; a service the platform lacks |
| Managed Jamstack / SSR host | You: frontend + functions. Platform: build, CDN, deploy. | Vercel, Netlify, Cloudflare Pages | Static/SSR frontend + serverless API; push-to-deploy | Long-running/stateful backend that won't fit functions |
| Managed data / Postgres-BaaS | You: schema + policies. Platform: DB, auth, storage, backups. | Supabase, Neon | Managed relational DB + auth/storage without DBA ops | Extreme scale/tuning; an engine the BaaS doesn't offer |
| Edge / serverless functions | You: function code. Platform: global runtime, per-call scaling. | Cloudflare Workers, Fly.io | Global low-latency; bursty/event compute; stateless | Stateful/long-running work; runtime/time limits |
| Hyperscaler managed services | You: choose per-service managed-vs-self. Platform: the catalog. | AWS, Azure, GCP | Deep compliance/scale/integration; broad service needs | (the floor — most control, most ops) |

Notes:

- **Engine heritage matters — state it precisely.** Supabase and Neon are
  Postgres-native. PlanetScale is Vitess/MySQL-heritage that added Postgres
  support only recently — do not conflate it with the Postgres-native BaaS
  options; name the engine when it drives a decision.
- **Rungs are not mutually exclusive per system.** A common modern shape is a
  Jamstack/SSR host for the frontend + a Postgres-BaaS for data + edge functions
  for global paths — score each surface on its own rung.
- **Cost model differs by rung:** per-invocation (edge/serverless),
  per-VM/per-container (IaaS/PaaS), or bandwidth/egress (Jamstack/CDN) — a
  workload cheap on one rung can be punitive on another.

Durable decision axes (these age slowly; brands do not): abstraction rung · ops
maturity · workload shape (static/SSR vs long-running/stateful vs edge/event) ·
cost model · compliance/residency · lock-in / exit cost. Decide on these; the
brand names are refreshable examples a future update swaps without touching the
logic.

## Scoring rubric (surviving options only)

Score each surviving option 1–5 per axis across **abstraction rung × provider ×
deployment posture** (not provider × posture alone), with a one-line written
rationale per cell — the rationale is the deliverable, the number is a summary:

| Axis | 5 looks like | 1 looks like |
| --- | --- | --- |
| Cost | Marginal per-tenant cost fits envelope incl. egress; credits usable | Punitive pricing under the chosen tenancy model |
| Operational fit | Team has run this shape in production | New paradigm + no hiring plan |
| Integration gravity | Estate already there / trivial adapters | Deep rework of identity, queues, IAM |
| Region coverage | All required regions, all required services | Gaps needing workarounds |
| Exit cost | Portable primitives, standard APIs | Proprietary services at the core |

The rung is chosen first (highest the workload tolerates, see § Abstraction
ladder); providers are then scored within it and, where the choice is close,
across adjacent rungs. Deployment postures to score alongside providers:
single-provider, multi-cloud (score its duplicated-expertise cost explicitly),
hybrid (on-prem + cloud), stay-as-is (always score the incumbent — migration
cost counts against challengers, not the incumbent).

## Managed-vs-self-hosted decision table

This is the per-capability refinement WITHIN the chosen rung (see § Abstraction
ladder). On the higher rungs most rows are settled by the platform (a
Postgres-BaaS or Jamstack host is managed by definition); the table bites most
on the IaaS and hyperscaler rungs, where each capability is a separate call.

| Capability | Default | Self-host only when | Operational bill to accept |
| --- | --- | --- | --- |
| Relational DB | managed | proven cost at scale / capability gap | backups, HA, patching, upgrades, on-call |
| Object storage | managed | almost never | durability engineering |
| Queue/stream | managed | exotic semantics needed | broker ops, partition rebalancing |
| Search | managed | index size pricing / plugin needs | cluster ops, reindex windows |
| Kubernetes | managed control plane | regulatory/edge | node ops, upgrades, CNI/CSI debugging |
| Observability stack | managed | data-volume pricing at scale | storage, retention, query performance |

Every self-hosted row in the output must fill all three columns.
