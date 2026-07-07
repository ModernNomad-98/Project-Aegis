---
name: cloud-architecture-decider
description: Decide cloud platform and deployment posture cloud-neutrally — gather requirements and constraints FIRST (compliance/residency, latency and regions, availability, cost envelope, team operational maturity, existing estate), shape the provider-neutral logical architecture, THEN decide provider (Azure, AWS, stay, multi- or hybrid-cloud) and per-capability managed-vs-self-hosted posture with named tradeoffs, exit costs, and an ADR handoff. Cloud choices must tie to tenant isolation, cost, and operational maturity — never to fashion. Use when asked which cloud or provider to use, whether to migrate clouds, managed-vs-self-hosted decisions, single-vs-multi-cloud, or when a greenfield SaaS needs a cloud decision. Do NOT use for mapping a decided provider to services (azure-saas-architect / aws-saas-architect), system structure (architecture-designer), tenancy structure (saas-platform-architect), or IaC review (iac-reviewer).
---

# Cloud Architecture Decider

## Purpose

Produce a defensible cloud platform decision: a requirements-and-constraints
record, a provider-neutral logical architecture, a scored provider/deployment
decision with honest tradeoffs and exit costs, and per-capability
managed-vs-self-hosted calls. The discipline is decision-before-services:
naming a provider's products before the constraints and logical shape are
written produces architecture-by-brochure. The output is the input
`azure-saas-architect` or `aws-saas-architect` maps, and the decision record
is handed to `adr-writer`.

## Use When

- Use when: asked which cloud provider a product should run on, or whether
  to stay, migrate, go multi-cloud, or go hybrid.
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

## Workflow

1. **Write the requirements-and-constraints record** across nine axes:
   compliance/residency, latency/regions, availability target, cost
   envelope, operational maturity, existing estate, integration gravity
   (what the product must talk to), scale trajectory, and exit-cost
   tolerance. Mark each entry verified (with source) or assumed. Missing
   answers on compliance, residency, or availability are Stop Conditions,
   not guesses.
2. **Shape the provider-neutral logical architecture**: identity boundary,
   network zones, data stores by kind (relational/object/cache/search),
   compute shape (long-running services, jobs, functions), messaging needs,
   observability requirements — in capability language ("managed relational
   DB with per-tenant isolation option"), never product names.
3. **Derive hard filters from tenant isolation and compliance**: which
   deployment models the tenancy design permits (a database-per-tenant silo
   needs cheap DB instances or schema automation; residency needs the right
   regions), and which providers/regions satisfy the compliance set. Filters
   eliminate options before scoring starts.
4. **Score the surviving options** against the record: provider(s) ×
   deployment posture (single provider, multi-cloud, hybrid, stay-as-is).
   Score cost (marginal per-tenant cost under the tenancy model, committed
   spend, egress), operational fit (can THIS team run it — a k8s-everywhere
   answer for a two-engineer team fails here), integration gravity, region
   coverage, and exit cost. Multi-cloud gets scored for its real costs
   (duplicated expertise, lowest-common-denominator services) — it must earn
   its place, not be a default hedge.
5. **Decide managed-vs-self-hosted per capability**: default managed;
   self-hosting requires a named reason (cost at proven scale, capability
   gap, residency) plus the operational bill (patching, backup, on-call) the
   team accepts. Record each as capability → posture → reason.
6. **Name the tradeoffs and exit costs honestly**: what the decision gives
   up, which services create lock-in and what leaving would cost, and the
   trigger conditions that would reopen the decision (price change, region
   gap, acquisition, compliance change).
7. **Hand off**: the decision record to `adr-writer` (with the rollback/
   reversal plan an ADR requires), service mapping to `azure-saas-architect`
   or `aws-saas-architect`, and per-tenant cost modeling of the chosen
   posture to `saas-cost-architect`.

## Output Format

```
CLOUD ARCHITECTURE DECISION — <product/scope>
Requirements & constraints: <nine axes, each verified(source)/assumed>
Logical architecture: <capability-language shape: identity, network zones,
  data, compute, messaging, observability>
Hard filters applied: <isolation/compliance/region filters → options
  eliminated, with the filter that killed each>
Options scored: <option — cost / operational fit / integration / regions /
  exit cost — score rationale per axis>
Decision: <provider + deployment posture — the one-paragraph why>
Managed vs self-hosted: <capability → posture → named reason → operational
  bill accepted>
Tradeoffs & exit costs: <what is given up; lock-in services; cost to leave;
  reopen triggers>
Handoffs: <adr-writer record; azure-/aws-saas-architect mapping;
  saas-cost-architect model>
Assumptions & open questions: <each with risk-if-wrong / who answers>
```

## Validation Checklist

- [ ] Requirements record complete across all nine axes; every entry marked
      verified (with source) or assumed — no silent guesses on compliance,
      residency, or availability.
- [ ] Logical architecture contains zero provider product names.
- [ ] Tenant isolation and compliance produced explicit hard filters before
      any scoring.
- [ ] Scoring includes operational maturity ("can this team run it") and
      exit cost — not just feature/price comparison.
- [ ] Multi-cloud, if chosen, carries its duplicated-expertise and
      lowest-common-denominator costs in writing; if rejected, the rejection
      is recorded.
- [ ] Every self-hosted call names its reason and its operational bill.
- [ ] Tradeoffs, lock-in, exit costs, and reopen triggers are written down.
- [ ] Handoffs to `adr-writer` and the provider architect skill are stated.

## Gotchas

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
  template, hard-filter derivation table, and scoring rubric.
- `evals/evals.json` — trigger + behavior cases.
- `evals/trigger-evals.json` — discrimination within the cloud cluster
  (`azure-saas-architect`, `aws-saas-architect`, `iac-reviewer`) and against
  shipped `architecture-designer` / `saas-platform-architect`.
