# Managed Platform Tier Reference

Detail file for `cloud-architecture-decider`. Loaded on demand when a managed
platform is a candidate, or when the user names one.

The owning [cloud architecture skill](../SKILL.md) defines the decision,
teaching and authority boundary. This sheet supplies the category comparison,
the trade-offs to check, the graduation path and a presentation template.

**Reading key:** a **managed platform** is a service that runs servers,
scaling, patching and deploys for you, so the team ships code instead of
operating infrastructure. A **hyperscaler** is a very large general cloud
provider with hundreds of services (AWS, Azure, Google Cloud (GCP)), where the
team chooses and governs each service. **BaaS** (backend as a service) bundles
a database, sign-in, file storage and often serverless functions behind one
account.
**PaaS** (platform as a service) runs your own application code or container
without you managing servers. **Egress** is data sent out of a provider,
often billed per gigabyte. **Lock-in** is the cost and effort of leaving a
provider. **RLS** (row-level security) is a database rule that limits which
rows each signed-in user or tenant can read or change. **SLA** means
service-level agreement; **DPA** data processing agreement; **BAA** business
associate agreement (a United States health-data contract); **SSR**
server-side rendering; **CDN** content delivery network; **OIDC** OpenID
Connect, a standard sign-in protocol.

## How this sheet names vendors

Every vendor name, price, free-tier limit and runtime limit below is
**volatile: examples only; verify current offerings, pricing and limits at
decision time.** Never quote a price or limit from memory; mark it unknown
until checked against the provider's current documentation.

This follows the skill's existing house style (Aegis library decision 45,
D45): a durable **category** carries the decision and brands appear only as
"e.g." examples inside it, the same treatment given to hyperscaler SKUs
(specific service or instance types) and regions. Some Aegis sheets name no
vendor at all (the feature-flag system sheet compares "hosted flag vendor" as
one category, because vendor choice there is a downstream detail). This skill
names examples because users ask by brand ("Vercel plus Supabase, or AWS?"),
and mapping a named brand to its category is part of answering them. Brands
never appear in the logical architecture, and a future update swaps the
example list without touching the logic.

## Category comparison

| Category | What the platform runs for you | What you still own | Examples (volatile; verify) | Fits when | Watch for |
| --- | --- | --- | --- | --- | --- |
| Frontend / edge hosting | Builds, CDN, preview deploys, SSR and short serverless functions | Frontend code, function code, environment secrets | Vercel, Netlify, Cloudflare Pages | Web frontend with SSR or static pages and a light API | Function time and memory limits; bandwidth and invocation pricing; no persistent workers |
| Postgres-based BaaS | Managed Postgres, sign-in, file storage, often realtime and functions | Schema, RLS policies, migrations, data model | Supabase; Neon (serverless Postgres; check which extras it bundles) | Standard web SaaS needing Postgres + sign-in quickly | RLS is the tenant barrier when clients query the database directly; proprietary sign-in and function layers add lock-in |
| Document-store BaaS | Managed document database, sign-in, storage, functions | Data model, security rules | Firebase (document-database heritage; check current SQL options) | Mobile-first or realtime apps with document-shaped data | Not relational: joins, reporting and migration to SQL cost more; security rules replace RLS |
| App platform / PaaS | Runs your container or app process, scaling, managed add-on databases | Application code, container image, background workers | Render, Railway, Fly.io, Heroku | Long-running API, background workers, cron jobs | Scale and price steps; region list; private networking and static outbound IPs may need higher plans |
| Edge / serverless functions | Global per-request runtime | Stateless function code | Cloudflare Workers | Low-latency global reads; bursty stateless work | Execution limits; a single-region database behind global compute adds latency |
| Hyperscaler managed services | Service-by-service operations across a very large catalog | Choosing, wiring, securing and governing each service | AWS, Azure, GCP | Regulated data, strict residency, private networking, deep integration, large proven scale | Setup and upkeep need cloud skills; more configuration surface to secure |

These categories combine. A common small-team shape is a frontend host, a
Postgres BaaS and an app platform for workers. Fit-check each component on its
own; one component that cannot fit does not force the whole product off the
tier.

## Trade-offs to check before recommending the tier

Answer each for THIS case. Mark every answer verified (with source), estimated,
or unknown.

| Trade-off | Question to answer | Why it matters |
| --- | --- | --- |
| Lock-in and migration path | Which parts are standard (plain Postgres, a container, OIDC sign-in) and which are proprietary (platform sign-in, functions runtime, realtime API, security rules)? Can the full database be exported? | Standard parts move in days; proprietary parts need rewrites. The exit plan is part of the recommendation. |
| Cost curve at scale | What is the monthly cost at today's usage, at 10x and at 100x? Which meter grows (seats, bandwidth, invocations, database size, compute hours)? | Low entry cost can climb steeply with bandwidth or invocations; a hyperscaler can be cheaper at large steady load but costs more team time. |
| Compliance and residency | Does the platform offer the required regions and certifications, and sign a DPA or BAA, on the plan the budget allows? | These are often available only on higher plans or not at all; a hard requirement can eliminate the tier (the hard-filter step). |
| Multi-tenant isolation | Pooled with Postgres RLS, schema per tenant, or project per tenant? Does the browser or mobile client query the database directly? | With direct client access, RLS is the only barrier between tenants and must be audited (`rls-policy-auditor`). Project-per-tenant silos hit project limits and cost. |
| Background jobs and long-running compute | Do jobs exceed function time limits, need retries and schedules, or hold connections? | Frontend hosts do not run persistent workers; add an app platform worker or a queue service (`background-job-orchestration-architect`). |
| Egress and data transfer | How much data leaves each provider, and does traffic cross providers or regions? | Bandwidth overages and cross-provider calls add cost and latency. |
| Vendor maturity | What SLA does the chosen plan give? Is there a status history, support tier and incident transparency? How long has the service run in production at this scale? | A missed availability target or a vendor change lands on the product. |
| Networking and access | Are private networking, static outbound IPs or customer network peering required? | Enterprise customers may allowlist IPs or demand private links that managed plans lack. |

## Hybrid paths and graduation

Start on the managed tier when it fits, and keep the exit cheap:

- Keep portable seams: standard Postgres features, the backend packaged as a
  container, sign-in through a standard protocol or behind one internal
  interface, and configuration kept in the repository.
- Graduate piece by piece, not all at once. Typical order: move workers or a
  heavy API to a container service first; move the database to a hyperscaler
  managed Postgres when size, compliance or networking demands it; keep the
  frontend host while it still fits.
- Write measurable **exit criteria** into the decision record, for example:
  the managed bill exceeds an estimated hyperscaler cost plus the added team
  time for a set number of months; a signed customer contract needs a region,
  certification or private network the platform cannot provide; jobs
  routinely exceed runtime limits; the availability target exceeds the plan's
  SLA; the team gains operations capacity and a named reason to use it.

## Deciding facts: ask only what is missing

Ask for a fact only when the prompt, repository and prior decisions do not
supply it and the answer could change the recommendation. Ask one per turn,
in this order, because earlier facts can eliminate whole categories:

1. Compliance, regulated data and data residency.
2. Workload shape: long-running jobs, stateful services, heavy realtime.
3. Team size and what it has operated in production.
4. Expected scale in the next 12 to 24 months.
5. Budget ceiling, credits and their expiry.
6. Existing stack or estate that must be reused.

## Presentation template

Use this shape when the owner must choose, and only once every deciding fact
above is known; a turn that asks for a missing fact carries no recommendation.
Include every option that survived the hard filters; when both survive,
include at least the strongest managed platform option and the strongest
hyperscaler option.

```
TERMS: <plain definitions of the terms the options use>
| Option | What it is | Why it fits this case | Pros (this case) | Cons (this case) | Money | Setup time | Upkeep | Exit path |
| <managed platform combo> | ... | ... | ... | ... | <verified / estimate / unknown> | ... | ... | ... |
| <hyperscaler option>     | ... | ... | ... | ... | ... | ... | ... | ... |
RECOMMENDATION: <one option> because <case-specific reason>.
WOULD CHANGE IF: <the fact or event that flips it>.
QUESTION: <one atomic owner question>
NOTE: your answer records a preference; creating accounts, paying, or
releasing anything still needs separate explicit approval.
```
