---
name: aws-saas-architect
description: Map a DECIDED logical architecture onto provider-idiomatic AWS for a multi-tenant SaaS — account topology (Organizations, SCPs), identity (IAM roles, Cognito, OIDC federation), network (VPCs, PrivateLink, ALB/CloudFront with WAF), Secrets Manager/KMS, data with an explicit tenant-isolation strategy per store (Aurora/RDS, DynamoDB, S3), compute chosen by team maturity (ECS/Fargate, EKS, Lambda), messaging (SQS, SNS, EventBridge), CloudWatch/CloudTrail observability, Security Hub/GuardDuty posture, Terraform/CDK IaC, and cost-allocation-tag cost controls. Every choice ties to tenant isolation, cost, and operational maturity; quota/instance-type/price claims become verification items, never asserted from memory. Use when asked to design or review AWS architecture for a SaaS, lay out AWS accounts, or choose between AWS options. Do NOT use to decide WHETHER AWS (cloud-architecture-decider), for Azure (azure-saas-architect), tenancy semantics (saas-platform-architect), or IaC diffs (iac-reviewer).
---

# AWS SaaS Architect

## Purpose

Produce an AWS service architecture for a multi-tenant SaaS that a team can
build and operate: account topology, per-capability service selections with
rationale, tenant-isolation strategy per data store, identity and network
topology, security posture, IaC strategy, and cost controls. The discipline
is provider-idiomatic-without-invention: use AWS primitives the way AWS
documents them — IAM-first isolation, multi-account boundaries, tag-based
attribution — and leave instance types, quotas, regional availability, and
prices as verification items against current AWS docs, never asserted from
memory.

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
   SCP guardrails, AWS Config rules for drift-prone settings. Pipeline
   design itself belongs to `ci-pipeline-architect`.
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
Security posture & CI/CD: <Security Hub/GuardDuty/SCPs/Config, OIDC deploy path>
IaC strategy: <tool, state/environment layout, module conventions>
Cost controls: <budgets, views, attribution feed, top-3 cost risks>
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
