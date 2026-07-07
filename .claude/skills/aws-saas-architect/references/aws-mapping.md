# AWS Mapping Reference

Detail file for `aws-saas-architect`. Loaded on demand. Service names are
stable AWS primitives; anything quota-, instance-type-, price-, or
region-specific is a verification item against current AWS docs, never
asserted from here.

## Capability → AWS service mapping

| Capability | Default | Alternatives (when) |
| --- | --- | --- |
| Org guardrails | AWS Organizations + SCPs | Control Tower (managed landing zone) |
| Workforce identity | IAM Identity Center / external IdP | — |
| Customer identity | Cognito | external IdP (existing estate, feature needs) |
| Service-to-service auth | IAM roles (assumed) | — (avoid long-lived keys) |
| CI/CD → cloud auth | OIDC federation to IAM roles | — (avoid stored access keys) |
| Secrets | Secrets Manager | SSM Parameter Store (simple/cheap tiers) |
| Encryption keys | KMS (per-workload keys + key policies) | — |
| Global ingress + CDN + WAF | CloudFront + AWS WAF | — |
| Regional L7 ingress | ALB | API Gateway (managed API features) |
| Private service access | VPC endpoints / PrivateLink | NAT egress (pays per GB; justify) |
| Relational data | Aurora (PostgreSQL/MySQL) | RDS engines (feature/cost preference) |
| Document/KV | DynamoDB | — |
| Object storage | S3 | — |
| Cache | ElastiCache (Redis) | — |
| Container compute | ECS on Fargate | EKS (named reason only), EC2 (special cases) |
| Event/job compute | Lambda | ECS scheduled tasks (long-running jobs) |
| Queues | SQS (+ DLQs) | — |
| Fan-out | SNS | — |
| Event routing | EventBridge | — |
| Telemetry | CloudWatch + X-Ray | — |
| Audit trail (control plane) | CloudTrail → log-archive account | — |
| Posture | Security Hub + GuardDuty + Config | — |
| IaC | Terraform | CDK (TS-native teams), CloudFormation |

## Tenant-isolation options per store

| Store | Pooled mechanism | Silo mechanism | Watch for |
| --- | --- | --- | --- |
| Aurora/RDS | tenant-key rows + app/RLS scoping | schema- or DB-per-tenant | connection fan-out per silo; pool exhaustion |
| DynamoDB | tenant-prefixed partition keys (+ IAM leading-key conditions) | table-per-tenant | hot tenant = hot partition; wildcard IAM conditions |
| S3 | tenant-prefixed keys + policy conditions | bucket-per-tenant | client-minted presigned URLs; bucket quota per account |
| ElastiCache | key prefix per tenant | instance per tenant | SCAN across prefixes; eviction mixing tenants |
| CloudWatch | tenant dimension on metrics/logs | log group per tenant (heavy) | support queries crossing tenants unaudited |

Mechanism detail and propagation contract: `multi-tenant-data-architect`.
IAM-enforced isolation claims pair with negative tests
(`multi-tenant-security-tester`).

## Account topology pattern (minimum viable)

```
Organizations root
├── OU: security      → log-archive acct, security-tooling acct
├── OU: workloads
│   ├── prod-<workload> acct
│   └── nonprod-<workload> acct
└── OU: sandbox
SCPs at OU level: deny region drift, deny CloudTrail disable,
deny root access keys, require encryption defaults.
Tags everywhere: env, workload, cost-center, tenant (where applicable);
activate cost allocation tags at landing-zone time.
```

## Standing verification items (always emit when relevant)

- Service quotas for the promised tenant count (DB instances per account,
  buckets, log groups, IAM policy size when tenant-scoped).
- Regional availability of every selected service in required regions.
- CloudWatch ingestion/retention economics for expected telemetry volume.
- PrivateLink/VPC-endpoint support for each selected service in scope.
