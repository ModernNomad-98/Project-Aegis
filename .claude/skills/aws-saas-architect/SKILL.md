---
name: aws-saas-architect
description: Map a decided logical architecture onto Amazon Web Services (AWS) for multi-tenant software as a service (SaaS). Design account, identity, network, data isolation, compute, messaging, observability, security, infrastructure-as-code, and cost choices tied to team maturity. Treat quotas, regional availability, instance types, and prices as current-documentation verification items. Use for AWS architecture and account layout. Do NOT use to choose the provider (cloud-architecture-decider), define tenancy semantics (saas-platform-architect), or review infrastructure-as-code changes (iac-reviewer).
---

# AWS SaaS Architect

## Purpose

Produce an AWS service architecture for a multi-tenant SaaS that a team can
build and operate: account topology, per-capability service selections with
rationale, tenant-isolation strategy per data store, identity and network
topology, security posture, infrastructure as code (IaC) strategy, and cost
controls. The discipline
is provider-idiomatic-without-invention: use AWS primitives the way AWS
documents them — IAM-first isolation, multi-account boundaries, tag-based
attribution — and leave instance types, quotas, regional availability, and
prices as verification items against current AWS docs, never asserted from
memory.

Terms used below: **AWS** is Amazon Web Services, **SaaS** is software as a
service, **IaC** is infrastructure as code, and **CI/CD** is continuous
integration and continuous delivery. For accounts and identity, **OU** means
organizational unit, **SCP** service control policy, **IAM** Identity and Access
Management, **IdP** identity provider, and **OIDC** OpenID Connect. For network
controls, **VPC** means virtual private cloud, **ALB** Application Load
Balancer, **WAF** web application firewall, **CDN** content delivery network,
and **NAT** network address translation. Data and compute names are **RDS**
(Relational Database Service), **S3** (Simple Storage Service), **ECS** (Elastic
Container Service), and **EKS** (Elastic Kubernetes Service); **SQS** (Simple
Queue Service) and **SNS** (Simple Notification Service) are messaging services.
**KMS** means Key Management Service and **CDK** Cloud Development Kit. Security
terms are **PII** (personally identifiable information), **CSPM** (cloud
security posture management), **SOC** (security operations center), **SIEM**
(security information and event management), and **OCSF** (Open Cybersecurity
Schema Framework). **EC2** and **ECR** name Elastic Compute Cloud and Elastic
Container Registry. These names explain the output fields; they do not select
services or assert their availability in a region.

## Use When

- Use when: a cloud decision landed on AWS and the logical architecture
  needs mapping to concrete AWS services.
- Use when: asked to design the AWS account/organization layout for a SaaS,
  or to place identity, network, data, compute, messaging, and
  observability on AWS.
- Use when: choosing between AWS options for one capability (ECS vs EKS vs
  Lambda; Aurora vs DynamoDB; SQS vs EventBridge) with SaaS tenancy in play.
- Use when: reviewing an existing AWS architecture against SaaS isolation,
  cost, and operability expectations.
- Do NOT use when: the provider question is still open —
  `cloud-architecture-decider` first.
- Do NOT use when: the platform is Azure — `azure-saas-architect`.
- Do NOT use when: defining tenancy semantics or pooled/siloed structure —
  `tenant-modeler` / `saas-platform-architect` (their outputs are inputs
  here).
- Do NOT use when: reviewing a Terraform/CDK change — `iac-reviewer`.

## Inputs to Inspect

1. The cloud decision record (`cloud-architecture-decider` output):
   constraints, hard filters, managed-vs-self-hosted posture.
2. The logical architecture and tenancy model: `architecture-designer`
   components, `saas-platform-architect` pooled/siloed decisions,
   `tenant-modeler` lifecycle.
3. Compliance/residency obligations and required regions.
4. Existing AWS estate if any: accounts, Organizations layout, VPCs, IaC in
   repo, deployed services, IdP integration.
5. Team operational maturity: EKS is a different operational bill than
   Fargate or Lambda — what has the team run?
6. Current AWS documentation for any capability where the design depends on
   a quota, instance type, or regional feature — verified, not recalled.

## Workflow

1. **Lay out the account topology**: AWS Organizations with organizational
   units separating production from non-production (and workload/security/
   log-archive accounts as scale warrants), Service Control Policies as
   organization-level guardrails (deny root access keys, restrict regions,
   protect logging), and the tagging standard (tenant, environment,
   workload, cost center) that cost attribution and policy will key on.
2. **Design identity first**: IAM roles over users everywhere,
   least-privilege policies scoped to resources and conditions (tenant tags
   in IAM condition keys where the isolation model uses them), Cognito or
   an external IdP for customer identity (workforce and customer identity
   kept separate), OIDC federation for CI/CD (no long-lived access keys in
   pipelines), and role-assumption paths that carry tenant scoping for
   runtime isolation where the design uses IAM-enforced tenancy.
3. **Design the network**: VPC layout per environment/account, private
   subnets for data and compute, PrivateLink/VPC endpoints for AWS service
   access without internet egress, ingress through ALB (regional) and/or
   CloudFront (global edge/CDN) with AWS WAF, egress control (NAT posture),
   and the rule that data stores are not publicly reachable.
4. **Map data stores with a tenant-isolation strategy per store**:
   Aurora/RDS (schema- or database-per-tenant silos vs pooled tenant-keyed
   rows), DynamoDB (tenant-prefixed partition keys in pooled tables vs
   table-per-tenant; IAM leading-key conditions where used), S3
   (tenant-prefixed keys with policy conditions vs bucket-per-tenant),
   cache/search equivalents — each store carries: service, isolation
   mechanism, and why it satisfies the tenancy model. Delegate mechanism
   detail to `multi-tenant-data-architect`.
5. **Choose compute per workload shape**: ECS on Fargate (containers, low
   ops default), Lambda (event-driven/jobs/spiky), EKS (only with a named
   reason and the operational bill accepted), biased by the team-maturity
   input.
6. **Map messaging**: SQS for queues/commands with dead-letter queues, SNS
   for fan-out, EventBridge for event routing/integration — with tenant
   context carried in messages and consumer-side tenant scoping stated.
7. **Wire observability and secrets**: CloudWatch logs/metrics/alarms with
   tenant-tagged telemetry (design detail per `observability-operator` /
   `slo-reliability-architect`), X-Ray tracing, CloudTrail on in every
   account shipped to a log-archive account, Secrets Manager + KMS with
   rotation posture and key policies scoped per workload.
8. **Set the CI/CD and security posture**: deployments assume IAM roles via
   OIDC federation, Security Hub + GuardDuty enabled organization-wide,
   SCP guardrails, AWS Config rules for drift-prone settings — then
   complete the suite:
   - Inspector: vulnerability management for the computes chosen (EC2, ECR
     images, Lambda functions); volume-priced (verification item).
   - Macie: S3 data/PII discovery scoped to the buckets holding tenant
     data (pairs with the tenant-prefixed S3 isolation strategy); scan
     scope is a cost decision, not default-on.
   - Detective: investigation graph over GuardDuty findings — only with a
     team that runs investigations (maturity-tied).
   - IAM Access Analyzer: external- and unused-access findings — the
     org-wide check on the IAM-first isolation discipline this design
     depends on.
   - Current shape: AWS splits Security Hub CSPM (posture aggregation)
     from broader Security Hub (threat correlation) — packaging/naming are
     verification items. Where findings feed an external SOC/SIEM, Amazon
     Security Lake (OCSF) is the first-class export path; Verified
     Permissions is the managed fine-grained-authz option at the app layer
     (the matrix itself belongs to `authorization-matrix-designer`).
   The mapper NAMES and PLACES these services and ties them to isolation,
   cost, and maturity; deep threat modeling belongs to `threat-modeler` /
   `ai-threat-modeler`; detection-rule design to
   `security-logging-alerting-architect`; operating the SIEM to
   `observability-operator`. Pipeline design itself belongs to
   `ci-pipeline-architect`.
9. **Declare the IaC strategy**: Terraform (mixed estates, most common),
   CDK (TypeScript-native teams), or CloudFormation — one primary tool,
   state/environment layout, module conventions; review discipline per
   `iac-reviewer`.
10. **Attach cost controls**: AWS Budgets with alerts per account/workload,
    Cost Explorer views keyed on the tagging standard (activate cost
    allocation tags), tenant-attributable usage feeding
    `saas-cost-architect`, and the top 3 cost risks of the chosen design
    named (NAT/egress, per-tenant DB floors, CloudWatch ingestion).
11. **Emit verification items**: every claim that depends on a quota,
    instance type, regional availability, or price is listed as "verify
    against current AWS docs".
12. **Teach consequential choices before requesting one.** For each service
    or topology choice the team must make, define unfamiliar terms in plain
    language, state the workload and tenancy reason, compare practical pros
    and cons, and recommend one option with its reason. Include money,
    setup time, and ongoing operations; call out a $0 incremental charge
    only when verified, and put unverified prices in Verification items.

## Output Format

```
AWS SAAS ARCHITECTURE — <product/scope>
Accounts & tagging: <Organizations/OU layout, SCP guardrails, tag standard>
Identity: <IAM role model, customer IdP, OIDC federation, tenant-scoped conditions>
Network: <VPC layout, PrivateLink coverage, ingress/WAF, egress posture>
Data (per store): <store — service — tenant-isolation mechanism — why it fits the tenancy model>
Compute (per workload): <workload — service — rationale incl. operational bill>
Messaging: <needs → SQS / SNS / EventBridge, tenant context propagation>
Observability & secrets: <CloudWatch/X-Ray/CloudTrail wiring, Secrets Manager + KMS layout>
Security controls and delivery pipeline: <Security Hub (CSPM/threat split), GuardDuty, Inspector/Macie/Detective/Access Analyzer placements, SCPs/Config, OIDC deploy path>
Infrastructure-as-code strategy: <tool, state/environment layout, module conventions>
Cost controls: <budgets, views, attribution feed, top-3 cost risks>
Choice guide: <for each owner choice: terms, reason, money/setup/ongoing cost,
  pros and cons, recommended option and why>
Verification items: <each quota/type/region/price-dependent claim → verify against current AWS docs>
Assumptions & open questions: <each with risk-if-wrong / who answers>
```

## Validation Checklist

- [ ] Every data store names its tenant-isolation mechanism and ties it to
      the tenancy model — no store ships isolation-unspecified.
- [ ] No quota, instance type, price, or regional-availability claim is
      asserted from memory — all such dependencies sit in Verification items.
- [ ] Identity uses roles + OIDC federation; long-lived access keys are
      flagged, not normalized; workforce and customer identity are separate.
- [ ] Data stores sit in private subnets / behind endpoints; every public
      exposure is justified in writing.
- [ ] Compute choices cite the team-maturity input; EKS (if chosen) carries
      a named reason and its operational bill.
- [ ] CloudTrail and posture services are organization-wide, not
      per-account afterthoughts.
- [ ] Cost controls key on activated cost-allocation tags and name this
      design's top cost risks.
- [ ] Choices shown to a human explain terms, reasons, money/time/setup and
      upkeep costs, pros/cons, and a justified recommendation; unverified
      price claims remain verification items.
- [ ] Tenancy semantics, pipeline internals, and IaC diff review were
      delegated, not restated.

## Gotchas

- IAM condition-key tenancy (leading-key/tag conditions) is powerful but
  subtle: one wildcard or missing condition silently pools tenants — pair
  every IAM-enforced isolation claim with a negative test
  (`multi-tenant-security-tester`).
- NAT gateway data processing is a classic surprise bill in
  private-subnet-everything designs; route AWS service traffic over VPC
  endpoints and say which traffic still pays NAT.
- DynamoDB single-table-with-tenant-prefix designs concentrate hot tenants
  onto hot partitions; design the heavy-tenant promotion path now.
- Lambda-per-everything architectures trade infrastructure ops for
  distributed-systems debugging; score against team maturity honestly.
- Cost allocation tags do not attribute retroactively — activate them at
  landing-zone time or lose the history.
- CloudWatch log ingestion and retention is a routine top-3 SaaS cost line;
  set retention and export posture in the design, not after the bill.
- GuardDuty, Inspector, and Macie meter by volume analyzed; Macie run
  estate-wide over data-heavy buckets is a classic surprise bill — scope
  it to tenant-data stores and list every scan meter as a verification
  item.

## Stop Conditions

- No cloud decision record exists and the provider choice is actually
  contested → `cloud-architecture-decider` first; this skill does not
  arbitrate providers.
- The tenancy model (pooled/siloed per component) is undefined → run
  `saas-platform-architect`; per-store isolation cannot be mapped without it.
- A design constraint hinges on a quota/type/region fact that cannot be
  verified against current docs in this session → mark it blocking in
  Verification items; do not design on a recalled number.
- The request shifts from designing to APPLYING changes to a live AWS
  estate → stop; this skill designs. Route execution through
  `human-approval-boundary` and the IaC/change process.

## Supporting Files

- `references/aws-mapping.md` — capability → AWS service mapping table,
  tenancy-isolation options per store, account-topology patterns.
- `evals/evals.json` — trigger + behavior cases.
- `evals/trigger-evals.json` — discrimination within the cloud cluster
  (`cloud-architecture-decider`, `azure-saas-architect`, `iac-reviewer`)
  and against shipped `saas-platform-architect` / `architecture-designer`.
