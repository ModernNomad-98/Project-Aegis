---
name: cloud-architecture-decider
description: Decide cloud platform, deployment pattern, and operational posture cloud-neutrally — gather requirements FIRST (compliance/residency, latency/regions, availability, cost, team maturity, existing estate), shape the provider-neutral logical architecture, THEN compare compatible infrastructure, managed application, data, and function options by operational burden and verified constraints, select providers, and decide per-capability managed-vs-self-hosted posture — with tradeoffs, exit costs, and an ADR handoff. A hyperscaler is a provider catalog, not automatically the highest abstraction. Ties to isolation, cost, and ops maturity, never fashion. Use when asked which cloud, provider, or platform tier to use, whether to migrate, managed-vs-self-hosted, or single-vs-multi-cloud. Do NOT use to MAP a decided provider to services (aws-/azure-saas-architect), system structure (architecture-designer), tenancy (saas-platform-architect), or IaC review (iac-reviewer).
---

# Cloud Architecture Decider

**Reading key:** VPS means virtual private server; IaaS means infrastructure
as a service; PaaS means platform as a service; SSR means server-side
rendering; BaaS means backend as a service; ADR means architecture decision
record; IAM means identity and access management; SaaS means software as a
service. Define other provider or product abbreviations when they drive a
decision.
Here p95 means the 95th percentile; SOC 2 and ISO 27001 are named security
assurance standards. OS means operating system; DB means database; VM means
virtual machine; API means application programming interface; SKU means a
provider's product or pricing unit; RLS means row-level security; k8s means
Kubernetes. AWS is Amazon Web Services and GCP is Google Cloud Platform.

## Purpose

Produce a defensible cloud platform decision: a requirements-and-constraints
record, a provider-neutral logical architecture, an explicit **deployment-pattern**
choice (how much operational surface the team should own for each workload
component), a scored pattern/provider/deployment decision with
honest tradeoffs and exit costs, and per-capability managed-vs-self-hosted calls.
The discipline is decision-before-services and operational-fit-before-provider:
choose compatible managed patterns that meet verified constraints, then a
provider for each. Naming a provider's products before the constraints,
logical shape, and pattern are written produces architecture-by-brochure.
For a hyperscaler the output is the
input `aws-saas-architect` or `azure-saas-architect` maps; for the modern
managed-platform tier the platform absorbs most of that mapping, so the decision
record plus the concrete provider is often enough to start. The decision record
is handed to `adr-writer`.

## Use When

- Use when: asked which cloud provider a product should run on, or whether
  to stay, migrate, go multi-cloud, or go hybrid.
- Use when: choosing how much operational surface to own for each workload
  component (raw VPS/IaaS, container-PaaS, managed-Jamstack/SSR host,
  Postgres-BaaS, edge/serverless, or a hyperscaler service) — not just which provider.
- Use when: a greenfield SaaS needs its cloud/deployment posture decided.
- Use when: deciding managed-vs-self-hosted per capability (database, queue,
  search, k8s vs PaaS) — on any provider.
- Use when: an existing cloud bill, compliance obligation, or team-capacity
  problem reopens the platform question.
- Do NOT use when: the provider is already decided and the task is mapping
  to concrete services — `azure-saas-architect` / `aws-saas-architect`.
- Do NOT use when: designing component boundaries and data ownership —
  `architecture-designer` (its output is an input here).
- Do NOT use when: deciding pooled/siloed tenancy or control-plane/data-plane
  structure — `saas-platform-architect` (its isolation decisions constrain
  the cloud decision, not vice versa).
- Do NOT use when: reviewing a Terraform/Bicep diff — `iac-reviewer`.

## Inputs to Inspect

1. The logical/system architecture if one exists (`architecture-designer`
   output, ADRs, diagrams) — the decision maps THIS, not a blank slate.
2. Tenancy decisions: `saas-platform-architect` pooled/siloed choices and
   `tenant-modeler` semantics — isolation requirements rule providers and
   deployment models in or out.
3. Compliance and residency obligations: certifications required by
   customers (SOC 2, ISO 27001), data-residency clauses, regulated-industry
   constraints — from contracts and security questionnaires, not memory.
4. Cost reality: current bills, `saas-cost-architect` model if present,
   funding stage, committed-spend contracts and credits with expiry dates.
5. Team operational maturity: who is on call, what the team has run in
   production before (k8s? managed PaaS only?), hiring plans.
6. Existing estate: current provider footprint, IaC, CI/CD, identity
   provider, and every integration with provider-specific services.
7. Latency/region needs: where users are, acceptable p95, offline/edge needs.
8. Workload shape per service: static/SSR, long-running/stateful, or bursty/
   event-driven — this rules out some patterns (a stateful long-running
   process does not fit a pure edge runtime; a static frontend + API fits a
   managed-Jamstack host), so inspect it before choosing a pattern.

## Workflow

1. **Write the requirements-and-constraints record** across nine axes:
   compliance/residency, latency/regions, availability target, cost
   envelope, operational maturity, existing estate, integration gravity
   (what the product must talk to), scale trajectory, and exit-cost
   tolerance. Mark each entry verified (with source) or assumed. Missing
   answers on compliance, residency, or availability are Stop Conditions,
   not guesses. These axes drive pattern selection in step 4:
   operational maturity and workload shape set how much ops the team should
   own; residency and compliance can rule out a pattern; cost sets the model.
2. **Shape the provider-neutral logical architecture**: identity boundary,
   network zones, data stores by kind (relational/object/cache/search),
   compute shape (long-running services, jobs, functions), messaging needs,
   observability requirements — in capability language ("managed relational
   DB with per-tenant isolation option"), never product names. Concrete
   providers and platform brands are deferred to steps 4–5; nothing here
   names a product.
3. **Derive hard filters from tenant isolation and compliance**: which
   deployment models the tenancy design permits (a database-per-tenant silo
   needs cheap DB instances or schema automation; residency needs the right
   regions), and which providers/regions satisfy the compliance set. Filters
   eliminate options — and can eliminate whole patterns (strict residency or a
   heavy compliance set can rule the modern managed-platform tier out and
   require a hyperscaler option; a stateful long-running service rules out a
   pure edge runtime) — before scoring starts.
4. **Compare compatible deployment patterns** — decide how much operational
   surface the team should own for each component before naming a provider.
   These options overlap and are not a single low-to-high ladder:
   - **IaaS / VPS** — you run the OS, patching, and runtime (hyperscaler VMs;
     e.g. DigitalOcean Droplets, Linode). Most control, most ops.
   - **Container PaaS** — "just deploy my app + DB," the platform runs the
     host and scaling (e.g. Render, Railway, Fly.io).
   - **Managed Jamstack / SSR host** — frontend + serverless functions, the
     platform owns build/CDN/deploy (e.g. Vercel, Netlify, Cloudflare Pages).
   - **Managed data / Postgres-BaaS** — managed DB plus auth and storage
     (e.g. Supabase, Neon).
   - **Edge / serverless functions** — global, per-invocation compute (e.g.
     Cloudflare Workers, Fly.io).
   - **Hyperscaler managed services** — a broad catalog for deep compliance,
     scale, and integration (AWS, Azure, GCP); operational burden varies by
     service and configuration.
   Prefer a compatible option with the **least operational burden** that meets
   verified constraints. A frontend host, managed data service and serverless
   functions can be combined; each needs its own fit check. Choose more
   operational control only for a named reason (cost at proven scale,
   residency, or a capability gap). Decide on the durable axes — operational
   abstraction, team maturity, workload shape (static/SSR vs
   long-running/stateful vs edge/event), cost
   model (per-invocation vs per-VM vs bandwidth/egress), compliance/residency,
   and lock-in/exit cost — and treat the named brands as **current examples of
   each category, not the decision**: their pricing, free-tier limits, and
   runtime constraints are VOLATILE verification items, never asserted from
   memory (the same rule the skill applies to hyperscaler SKUs and regions).
5. **Score the surviving options** against the record across **deployment
   pattern × provider × deployment posture** (single provider, multi-cloud,
   hybrid, stay-as-is) — not provider × posture alone. Score cost (the cost
   model of the pattern: per-invocation vs per-VM vs bandwidth/egress, marginal
   per-tenant cost under the tenancy model, committed spend), operational fit
   (can THIS team run it — a k8s-everywhere answer for a two-engineer team
   fails here, and so does a raw-VPS answer when a managed platform would
   carry the ops), integration gravity, region coverage, and exit cost.
   Multi-cloud gets scored for its real costs (duplicated expertise,
   lowest-common-denominator services) — it must earn its place, not be a
   default hedge.
   When a provider, deployment pattern, or posture is a user-facing choice,
   define unfamiliar terms and why each option survived. Explain each one's
   pros and cons, verified or estimated money cost, setup and delivery time,
   and continuing upkeep before requesting a choice. A $0 software tier can
   still consume team time; mark unknown prices instead of guessing. End the
   choice presentation with one clear owner decision question; do not decide
   silently.
6. **Decide managed-vs-self-hosted per capability** — the per-capability
   refinement of the pattern choice: default managed; self-hosting requires a
   named reason (cost at proven scale, capability gap, residency) plus the
   operational bill (patching, backup, on-call) the team accepts. Record each
   as capability → posture → reason. Managed application and data platforms
   settle more of this by default; it bites most on IaaS and mixed hyperscaler
   stacks, where each capability is a separate managed-or-not call.
7. **Name the tradeoffs and exit costs honestly**: what the decision gives
   up, which services create lock-in and what leaving would cost, and the
   trigger conditions that would reopen the decision (price change, region
   gap, acquisition, compliance change, outgrowing the pattern). Each pattern
   has its own
   exit profile — a managed platform trades control for speed and can hit a
   ceiling (pricing, runtime limits, a capability gap) that forces a change in
   the selected pattern; name that ceiling and the migration it would trigger
   rather
   than meeting it in production.
8. **Hand off**: the decision record to `adr-writer` (with the rollback/
   reversal plan an ADR requires) and per-tenant cost modeling of the chosen
   posture to `saas-cost-architect`. Service mapping depends on the pattern:
   - **Hyperscaler option** → `aws-saas-architect` or `azure-saas-architect`
     maps account topology, IAM, network, and service SKUs. (GCP is a
     decide-able hyperscaler here but has no mapping skill yet — a banked
     future item; the decision can still land on GCP.)
   - **Modern managed-platform tier** (container-PaaS / Jamstack / Postgres-
     BaaS / edge) → there is no dedicated mapping skill; the platform may
     absorb parts of account topology, IAM, network, and patching, so verify
     the remaining responsibilities. The decision record plus
     the concrete provider is usually enough to start. Route the parts that
     still need design to their owners: tenancy to `saas-platform-architect`,
     `tenant-modeler`, and `multi-tenant-data-architect`; Postgres-BaaS
     row-level isolation to `rls-policy-auditor`; and the push-to-deploy flow
     to `merge-is-deploy-governance` when push-to-deploy is enabled, because
     merge then becomes a deployment trigger.

## Output Format

```
CLOUD ARCHITECTURE DECISION — <product/scope>
Requirements & constraints: <nine axes, each verified(source)/assumed>
Logical architecture: <capability-language shape: identity, network zones,
  data, compute, messaging, observability>
Hard filters applied: <isolation/compliance/region filters → options and
  options eliminated, with the filter that killed each>
Deployment patterns: <compatible pattern for each component + why; options
  ruled out and by what (workload shape / residency / compliance)>
Options scored: <plain-language meaning + why each pattern × provider × posture
  is considered; pros/cons; money, setup, delivery-time and upkeep costs;
  operational fit / integration / regions / exit cost — rationale per axis>
Decision: <patterns + providers + deployment posture — why this fits best>
Managed vs self-hosted: <capability → posture → named reason → operational
  bill accepted>
Tradeoffs & exit costs: <what is given up; lock-in services; cost to leave;
  reopen triggers incl. outgrowing the pattern>
Handoffs: <adr-writer record; hyperscaler → aws-/azure-saas-architect mapping,
  OR modern tier → saas-platform-architect/tenant-modeler/multi-tenant-data-
  architect + rls-policy-auditor + merge-is-deploy-governance;
  saas-cost-architect model>
Assumptions & open questions: <each with risk-if-wrong / who answers>
```

## Validation Checklist

- [ ] Requirements record complete across all nine axes; every entry marked
      verified (with source) or assumed — no silent guesses on compliance,
      residency, or availability.
- [ ] Logical architecture contains zero provider product names.
- [ ] Concrete provider/platform brand names appear only in the abstraction-
      pattern explanation and the options/scoring output, as current examples —
      never in the logical architecture, which stays capability-language.
- [ ] Tenant isolation and compliance produced explicit hard filters before
      any scoring.
- [ ] Deployment patterns are chosen per component and justified by verified
      fit and operational burden; rejected options are recorded with the reason
      (workload shape, residency, compliance).
- [ ] Scoring is pattern × provider × posture and includes operational maturity
      ("can this team run it") and exit cost — not just feature/price
      comparison, and not provider × posture alone.
- [ ] Before a user-facing build choice, terms, reasons, pros/cons, and
      money/time/setup/upkeep costs are clear; current prices and free tiers
      are verified or labeled unknown, and the recommendation explains fit.
- [ ] Multi-cloud, if chosen, carries its duplicated-expertise and
      lowest-common-denominator costs in writing; if rejected, the rejection
      is recorded.
- [ ] Every self-hosted call names its reason and its operational bill.
- [ ] Tradeoffs, lock-in, exit costs, and reopen triggers are written down.
- [ ] Handoffs are stated and pattern-appropriate: `adr-writer` always;
      hyperscaler → the provider architect skill; modern managed-platform tier
      → the tenancy, RLS, and deploy owners.

## Gotchas

- The enterprise-default trap: reaching for a hyperscaler (AWS/Azure/GCP)
  for a small team or greenfield product usually over-buys operational
  surface. Compatible managed frontend, data, or container platforms can hand
  patching, account topology, and identity plumbing to the platform. Choose
  a more operationally demanding option for a named reason; "everyone uses
  AWS" is fashion, not a requirement.
- The named platforms (Vercel, Netlify, Cloudflare, Render, Railway, Fly,
  Supabase, Neon, …) are current market examples of each pattern, not
  endorsements; their free tiers, pricing, and runtime limits move
  quarterly — verify them at decision time, never assert from memory (the
  same discipline the skill applies to hyperscaler SKUs and regions). Note
  engine heritage precisely when it drives a decision (a Postgres-BaaS is not
  interchangeable with a MySQL/Vitess-heritage platform).
- Committed-spend contracts and startup credits decide more real cloud
  choices than architecture does — surface them in the cost axis instead of
  letting them operate invisibly.
- "Multi-cloud for resilience" usually buys correlated complexity, not
  resilience; region-level redundancy on one provider is the cheaper first
  answer. Multi-cloud earns its place via residency, acquisition risk, or
  customer mandate.
- Integration gravity is underweighted: an estate already deep in one
  provider's identity, queues, and IAM makes "better database elsewhere"
  a net loss after integration cost.
- Team maturity is the axis people lie about; score what the team has
  RUN in production, not what it wants to run.
- The tenancy model changes provider economics (thousands of silo DBs vs
  one pooled cluster price out differently) — decide with
  `saas-platform-architect` output in hand, not after.
- A "temporary" second provider from an acquisition becomes permanent;
  write the consolidation trigger into the decision or accept hybrid as
  the real posture.

## Stop Conditions

- Compliance, data-residency, or availability requirements cannot be
  verified from any source → stop; a cloud decision on guessed compliance
  is unshippable. Route to `human-approval-boundary` with what is missing.
- Tenancy decisions do not exist yet → run `saas-platform-architect` first;
  the deployment model is an input, not an afterthought.
- The scored options land within noise of each other → present the tie with
  the tie-breaking question (usually exit cost or team maturity) to the
  human instead of manufacturing a winner.
- The decision would trigger a migration of a live production estate →
  decision record only; migration planning is separate, approval-gated work.

## Supporting Files

- `references/decision-inputs.md` — the nine-axis requirements record
  template, the deployment patterns with current example providers,
  the hard-filter derivation table, and the scoring rubric.
- `evals/evals.json` — trigger + behavior cases.
- `evals/trigger-evals.json` — discrimination within the cloud cluster
  (`azure-saas-architect`, `aws-saas-architect`, `iac-reviewer`) and against
  shipped `architecture-designer` / `saas-platform-architect`.
