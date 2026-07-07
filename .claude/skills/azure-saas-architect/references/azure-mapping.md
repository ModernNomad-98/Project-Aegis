# Azure Mapping Reference

Detail file for `azure-saas-architect`. Loaded on demand. Service names are
stable Azure primitives; anything SKU-, quota-, price-, or region-specific is
a verification item against current Azure docs, never asserted from here.

## Capability → Azure service mapping

| Capability | Default | Alternatives (when) |
| --- | --- | --- |
| Workforce identity | Microsoft Entra ID | — |
| Customer identity | Microsoft Entra External ID | third-party IdP (existing estate) |
| Service-to-service auth | Managed identities | — (avoid secret-bearing service principals) |
| CI/CD → cloud auth | Workload identity federation (OIDC) | — (avoid stored credentials) |
| Secrets/keys/certs | Key Vault (per environment) | Managed HSM (regulatory) |
| Global ingress + CDN + WAF | Front Door | Application Gateway (regional-only L7) |
| Private data-plane access | Private Link / private endpoints | service firewalls (weaker; justify) |
| Relational data | Azure SQL Database | PostgreSQL flexible server (engine preference) |
| Silo relational tenancy | Azure SQL elastic pools | database-per-tenant unpooled (verify economics) |
| Document/NoSQL | Cosmos DB | — |
| Object storage | Blob Storage | — |
| Cache | Azure Cache for Redis | — |
| Web compute | App Service | Container Apps (containers), AKS (named reason only) |
| Jobs/event compute | Functions | Container Apps jobs |
| Commands/queues | Service Bus | Storage queues (simple, low-volume) |
| Event distribution | Event Grid | — |
| Streaming | Event Hubs | — |
| Telemetry | Application Insights + Azure Monitor + Log Analytics | — |
| Policy guardrails | Azure Policy | — |
| Posture monitoring | Microsoft Defender for Cloud | — |
| IaC | Bicep (Azure-native) | Terraform (mixed estate) |

## Tenant-isolation options per store

| Store | Pooled mechanism | Silo mechanism | Watch for |
| --- | --- | --- | --- |
| Azure SQL | tenant-key rows + app/DB-level scoping | DB-per-tenant in elastic pools | pool DTU/vCore sharing = noisy neighbor; verify pool limits |
| Cosmos DB | partition key = tenant id | container/DB per tenant | cross-partition queries leaking scope; RU sharing |
| Blob | tenant-prefixed paths + scoped SAS/RBAC | container per tenant | SAS tokens minted client-side; list-scope leaks |
| Redis | key prefix per tenant | DB/instance per tenant | SCAN across prefixes; eviction mixing tenants |
| Log Analytics | tenant dimension on telemetry | workspace per tenant (heavy) | support queries crossing tenants unaudited |

Mechanism detail and propagation contract: `multi-tenant-data-architect`.

## Landing-zone layout pattern (minimum viable)

```
Management group: <org>
├── platform (shared: connectivity, identity, management)
├── landing zones
│   ├── prod-<workload>      # subscription
│   └── nonprod-<workload>   # subscription
└── sandbox
Tags everywhere: env, workload, cost-center, tenant (where applicable)
Policy at MG level: require tags, deny public storage endpoints,
require private endpoints for data services, allowed regions.
```

## Standing verification items (always emit when relevant)

- Elastic pool / Cosmos RU / App Service plan limits for the promised tenant
  count and traffic.
- Regional availability of every selected service in required regions.
- Log Analytics pricing tier / daily-cap behavior for expected telemetry volume.
- Private Link support for each selected service in scope.
