---
name: azure-saas-architect
description: Map a DECIDED logical architecture onto provider-idiomatic Azure for a multi-tenant SaaS — subscription layout, identity (Entra ID, managed identities, OIDC federation), network (VNets, Private Link, Front Door), Key Vault, data with an explicit tenant-isolation strategy per store (Azure SQL, Cosmos DB, Blob), compute chosen by team maturity (App Service, Container Apps, AKS, Functions), messaging (Service Bus, Event Grid), Azure Monitor observability, Azure Policy + Defender for Cloud/Sentinel posture, Bicep/Terraform IaC, and tag-keyed cost controls. Every choice ties to tenant isolation, cost, and operational maturity; SKU/quota/price claims become verification items, never asserted from memory. Use when asked to design or review Azure architecture for a SaaS, lay out a landing zone, or choose between Azure options. Do NOT use to decide WHETHER Azure (cloud-architecture-decider), for AWS (aws-saas-architect), tenancy semantics (saas-platform-architect), or IaC diffs (iac-reviewer).
---

# Azure SaaS Architect

## Purpose

Produce an Azure service architecture for a multi-tenant SaaS that a team
can build and operate: per-capability service selections with rationale,
tenant-isolation strategy per data store, identity and network topology,
CI/CD and security posture, IaC strategy, and cost controls. The discipline
is provider-idiomatic-without-invention: use Azure's native primitives the
way Azure documents them, name services and capabilities — and leave SKU
tiers, quotas, regional availability, and prices as verification items
against current Azure docs, never asserted from memory.

Terms used below: **SaaS** means software as a service, **IaC** infrastructure
as code, **CI/CD** continuous integration and continuous delivery, and **SKU**
stock keeping unit (an offered service tier or configuration). For identity,
**ID** means identity, **OIDC** OpenID Connect, and **RBAC** role-based access
control. For network and compute, **VNet** means virtual network, **WAF** web
application firewall, **CDN** content delivery network, **AKS** Azure Kubernetes
Service, and **SQL** Structured Query Language. Security terms are **CSPM**
(cloud security posture management), **CWPP** (cloud workload protection
platform), **SIEM** (security information and event management), **SOAR**
(security orchestration, automation and response), and **CASB** (cloud access
security broker). **GA** means general availability and **L7** means layer 7
(the application layer) of the network model. These terms identify what
to evaluate; they do not verify a current Azure offering, limit or price.

## Use When

- Use when: a cloud decision landed on Azure and the logical architecture
  needs mapping to concrete Azure services.
- Use when: asked to design an Azure landing zone / subscription layout for
  a SaaS, or to place identity, network, data, compute, messaging, and
  observability on Azure.
- Use when: choosing between Azure options for one capability (App Service
  vs Container Apps vs AKS; Azure SQL vs Cosmos DB; Service Bus vs Event
  Grid) with SaaS tenancy in play.
- Use when: reviewing an existing Azure architecture against SaaS isolation,
  cost, and operability expectations.
- Do NOT use when: the provider question is still open —
  `cloud-architecture-decider` first.
- Do NOT use when: the platform is AWS — `aws-saas-architect`.
- Do NOT use when: defining tenancy semantics or pooled/siloed structure —
  `tenant-modeler` / `saas-platform-architect` (their outputs are inputs
  here).
- Do NOT use when: reviewing a Bicep/Terraform change — `iac-reviewer`.

## Inputs to Inspect

1. The cloud decision record (`cloud-architecture-decider` output): the
   constraints, hard filters, and managed-vs-self-hosted posture already
   decided.
2. The logical architecture and tenancy model: `architecture-designer`
   components, `saas-platform-architect` pooled/siloed decisions per
   component, `tenant-modeler` lifecycle.
3. Compliance/residency obligations and required regions.
4. Existing Azure estate if any: subscriptions, Entra tenant layout,
   networking, IaC in repo, deployed services.
5. Team operational maturity: AKS is a different operational bill than App
   Service — what has the team run?
6. Current Azure documentation for any capability where the design depends
   on a specific limit, SKU, or regional feature — these are verified, not
   recalled.

## Workflow

1. **Lay out the management structure**: management groups, subscriptions
   (at minimum: production / non-production separation; per-environment or
   per-workload subscriptions as scale warrants), resource-group
   conventions, and the tagging standard (tenant, environment, workload,
   cost center) that cost controls and Azure Policy will key on.
2. **Design identity first**: Microsoft Entra ID as the identity plane —
   workforce vs customer identity (External ID) separation, managed
   identities for service-to-service auth (no connection-string culture),
   workload identity federation (OIDC) for CI/CD instead of long-lived
   service principals with secrets, RBAC role assignments at the narrowest
   scope that works.
3. **Design the network**: VNet topology (hub-spoke when multiple workloads/
   environments warrant it), private endpoints via Private Link for data
   services, public ingress through Front Door or Application Gateway (WAF
   at the edge), egress control, and the rule that data stores are not
   publicly reachable.
4. **Map data stores with a tenant-isolation strategy per store**: Azure
   SQL (elastic pools for database-per-tenant silos; row-level scoping in
   pooled models), Cosmos DB (partition-key-per-tenant in pooled containers;
   database/container-per-tenant for silos), Blob Storage (tenant-prefixed
   paths or per-tenant containers), cache/search equivalents — each store
   carries: service, isolation mechanism, and the reason it satisfies the
   tenancy model. Delegate mechanism design detail to
   `multi-tenant-data-architect`.
5. **Choose compute per workload shape**: App Service (web workloads, low
   ops), Azure Container Apps (containers without cluster ops), AKS (only
   with a named reason and the operational bill accepted), Functions
   (event-driven/jobs) — biased by the team-maturity input, not resume
   ambition.
6. **Map messaging**: Service Bus for commands/queues with ordering and
   dead-lettering, Event Grid for event distribution/fan-out, Event Hubs
   for streaming volumes — with tenant context carried in messages and
   consumer-side tenant scoping stated.
7. **Wire observability and secrets**: Application Insights + Azure Monitor
   + Log Analytics with tenant-tagged telemetry (design detail per
   `observability-operator` / `slo-reliability-architect`), Key Vault per
   environment for secrets/keys/certs with rotation posture, diagnostic
   settings shipped to Log Analytics by default.
8. **Set the CI/CD and security posture**: deployment via GitHub Actions or
   Azure DevOps using OIDC federation to Entra (no stored cloud
   credentials), Azure Policy for guardrails (deny public storage, require
   tags, require private endpoints), activity logs retained — then place
   the security suite deliberately:
   - Microsoft Defender for Cloud: CSPM baseline org-wide, plus
     per-workload CWPP plans (Servers, Containers, SQL, Storage, Key
     Vault, App Service, APIs) for the services THIS design deploys — each
     plan is a per-resource cost meter (coverage/pricing are verification
     items; enable-all-by-default is a cost trap, not a posture win).
   - Microsoft Sentinel: SIEM/SOAR when the team has (or is hiring) a
     detection-and-response practice; it ingests via Log Analytics, so the
     Log Analytics cost gotcha applies to security telemetry too, and
     Sentinel without a triage practice is shelfware (a maturity call,
     like AKS). Detection-rule/alert design belongs to
     `security-logging-alerting-architect`; operating the stack to
     `observability-operator`.
   - Defender for Cloud Apps (CASB) + Entra ID Protection + Conditional
     Access (risk-based sign-on on the step-2 identity plane):
     name-and-place for enterprise estates — these govern
     workforce/operator access to the estate, NOT the product's end-user
     authorization.
   - Current shape: Microsoft consolidates these in the unified Defender
     portal (Sentinel now GA there); portal packaging and tier names are
     verification items against current Azure docs.
   The mapper NAMES and PLACES these services and ties them to isolation,
   cost, and maturity; deep threat modeling belongs to `threat-modeler` /
   `ai-threat-modeler`. Pipeline design itself belongs to
   `ci-pipeline-architect`.
9. **Declare the IaC strategy**: Bicep (Azure-native) or Terraform (mixed
   estates) — one primary tool, state/environment layout, module
   conventions; review discipline per `iac-reviewer`.
10. **Attach cost controls**: budgets with alerts per subscription/
    workload, Cost Management views keyed on the tagging standard,
    tenant-attributable usage feeding `saas-cost-architect`, and the
    top 3 cost risks of the chosen design named (egress, per-tenant DB
    floors, log ingestion).
11. **Emit verification items**: every claim that depends on a SKU, quota,
    regional availability, or price is listed as "verify against current
    Azure docs" — the design says WHAT must hold, verification says whether
    it does today.

## Output Format

```
AZURE SAAS ARCHITECTURE — <product/scope>
Management & tagging: <mgmt groups, subscriptions, resource-group + tag standard>
Identity: <Entra layout, workforce/customer split, managed identities, OIDC federation, RBAC scopes>
Network: <VNet topology, Private Link coverage, ingress/WAF, egress posture>
Data (per store): <store — service — tenant-isolation mechanism — why it fits the tenancy model>
Compute (per workload): <workload — service — rationale incl. operational bill>
Messaging: <needs → Service Bus / Event Grid / Event Hubs, tenant context propagation>
Observability & secrets: <Monitor/App Insights/Log Analytics wiring, Key Vault layout, rotation>
Delivery pipeline and security controls: <OIDC deploy path, Azure Policy guardrails, Defender for Cloud plans, Sentinel (if detection-and-response practice), CASB / ID Protection placements>
Infrastructure-as-code strategy: <tool, state/environment layout, module conventions>
Cost controls: <budgets, views, attribution feed, top-3 cost risks>
Verification items: <each SKU/limit/region/price-dependent claim → verify against current Azure docs>
Assumptions & open questions: <each with risk-if-wrong / who answers>
```

## Validation Checklist

- [ ] Every data store names its tenant-isolation mechanism and ties it to
      the tenancy model — no store ships isolation-unspecified.
- [ ] No SKU tier, quota, price, or regional-availability claim is asserted
      from memory — all such dependencies sit in Verification items.
- [ ] Identity design uses managed identities and OIDC federation; any
      long-lived credential is flagged, not normalized.
- [ ] Data services sit behind private endpoints; every public exposure is
      justified in writing.
- [ ] Compute choices cite the team-maturity input; AKS (if chosen) carries
      a named reason and its operational bill.
- [ ] Security-suite choices tie to team maturity and carry their cost
      meters; no plan/tier claim is asserted from memory.
- [ ] Cost controls key on the tagging standard and name the top cost risks
      of this specific design.
- [ ] Tenancy semantics, pipeline internals, and IaC diff review were
      delegated (`saas-platform-architect`/`multi-tenant-data-architect`,
      `ci-pipeline-architect`, `iac-reviewer`), not restated.

## Gotchas

- Per-tenant Azure SQL databases without elastic pools price like a
  separate server per tenant; pools are the silo-model default — verify
  current pool limits before promising tenant counts.
- Cosmos DB partition-key-per-tenant pools hit noisy-neighbor throughput
  sharing; heavy tenants may need their own containers — design the
  promotion path now.
- Front Door and Application Gateway overlap on ingress: global anycast +
  CDN vs regional L7; picking by acronym rather than traffic shape is a
  recurring miss.
- Managed identities do not cross the Entra tenant boundary trivially;
  customer-facing auth (External ID) and workforce auth are different
  designs — do not conflate them.
- Log Analytics ingestion is a routine surprise top-3 cost line in SaaS
  telemetry designs; set daily caps/table plans as part of the design, not
  after the first bill.
- Defender for Cloud plans meter per resource and Sentinel rides the Log
  Analytics meter — the security suite is a routine surprise top-3 cost
  line; scope plans to the workloads this design deploys and cap security
  telemetry like any other Log Analytics table.
- Azure Policy guardrails applied after workloads exist produce a
  remediation backlog; ship policy with the landing zone, not as cleanup.

## Stop Conditions

- No cloud decision record exists and the provider choice is actually
  contested → `cloud-architecture-decider` first; this skill does not
  arbitrate providers.
- The tenancy model (pooled/siloed per component) is undefined → run
  `saas-platform-architect`; per-store isolation cannot be mapped without it.
- A design constraint hinges on a SKU/limit/region fact that cannot be
  verified against current docs in this session → mark it blocking in
  Verification items and say so; do not design on a recalled number.
- The request shifts from designing to APPLYING changes to a live Azure
  estate → stop; this skill designs. Route execution through
  `human-approval-boundary` and the IaC/change process.

## Supporting Files

- `references/azure-mapping.md` — capability → Azure service mapping table,
  tenancy-isolation options per store, landing-zone layout patterns.
- `evals/evals.json` — trigger + behavior cases.
- `evals/trigger-evals.json` — discrimination within the cloud cluster
  (`cloud-architecture-decider`, `aws-saas-architect`, `iac-reviewer`) and
  against shipped `saas-platform-architect` / `architecture-designer`.
