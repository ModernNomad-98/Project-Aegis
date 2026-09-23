# Software as a service (SaaS) platform architecture

Repeatable SaaS platform skills for tenants, roles, billing, imports, storage, admin, and operations.

These numbered rows are historical candidates from the [original 300-skill
roadmap](../300-repeatable-software-saas-skills-roadmap.md). They are not an
installed-skill inventory: a capability may have shipped under a reconciled
name, been combined with another, or remain unbuilt. Use the [current
catalog](../skills-catalog.md) to find shipped names, then open
`.claude/skills/<skill-name>/SKILL.md` for trigger and invocation rules. The
row numbers are original candidate identifiers (IDs), not executable skill
names or authorization.

Priority labels are original planning tiers: **P0** is foundation, **P1** is
high-value follow-on work, and **P2** is later expansion. A priority does not
state whether a row shipped.

Terms in the table: SaaS means software as a service; API means application
programming interface; AI means artificial intelligence; UI means user
interface; SMS means Short Message Service (text messaging); RLS means
row-level security; URL means web address.

| # | Skill | Priority | Usage |
|---:|---|---|---|
| 56 | Tenant Model Design | P0 | Define tenant, workspace, organization, membership, ownership, and lifecycle semantics. |
| 57 | Tenant Provisioning Workflow | P0 | Design tenant creation, initial admin setup, defaults, seed data, and post-provision verification. |
| 58 | Membership and Invitation Design | P0 | Handle invites, acceptance, expiration, revocation, role assignment, and auditability. |
| 59 | Role and Permission Architecture | P0 | Design roles, permissions, assignment tables, inheritance rules, and least-privilege checks. |
| 60 | Entitlement Model Design | P0 | Map plan, tenant, user, and feature entitlements into enforceable limits. |
| 61 | Subscription Lifecycle Design | P1 | Model trials, upgrades, downgrades, cancellations, renewals, payment failure, and grace periods. |
| 62 | Usage Metering Architecture | P1 | Measure feature usage, API calls, storage, AI tokens, seats, and billable events. |
| 63 | Billing Reconciliation Design | P1 | Reconcile provider totals, internal ledger entries, invoices, rollups, adjustments, and anomalies. |
| 64 | Plan Limit Enforcement | P0 | Apply limits consistently in UI, API, command paths, background jobs, and integrations. |
| 65 | Feature Flag Rollout by Tenant | P1 | Roll out capabilities by tenant, role, plan, cohort, environment, or kill switch. |
| 66 | Tenant Settings Architecture | P1 | Separate tenant-level settings from user preferences, platform defaults, and environment config. |
| 67 | User Preference Architecture | P1 | Design per-user settings that safely override defaults without breaking tenant policy. |
| 68 | Admin Console Architecture | P1 | Design platform, tenant, support, audit, billing, usage, and configuration admin surfaces. |
| 69 | Supportability Architecture | P1 | Provide safe diagnostics, correlation lookup, tenant-aware support views, and no unsafe impersonation. |
| 70 | Audit Log Platform | P0 | Create a durable cross-module audit system for critical actions, access changes, and security events. |
| 71 | Notification Platform Design | P1 | Use an in-app source of truth with optional email, push, SMS, digest, and webhook delivery. |
| 72 | Digest and Scheduled Communication Design | P2 | Aggregate notifications, alerts, reports, and summaries with user preferences and delivery windows. |
| 73 | Search Architecture for SaaS | P1 | Design permission-aware search, scoped indexing, ranking, redaction, and result explainability. |
| 74 | File Storage Architecture | P0 | Separate public assets, private files, signed URLs, storage policies, ownership, and retention. |
| 75 | Import Pipeline Architecture | P1 | Process files through upload, inspect, map, preview, review, confirm, write, and audit stages. |
| 76 | Export Pipeline Architecture | P2 | Export tenant data with authorization, status tracking, redaction, expiration, and audit evidence. |
| 77 | Soft Delete and Archive Design | P1 | Model delete, archive, restore, purge, retention, legal hold, and historical references. |
| 78 | Data Retention Architecture | P1 | Define retention periods, deletion jobs, preservation exceptions, backups, and user-facing policy. |
| 79 | Multi-Environment SaaS Design | P0 | Separate local, preview, staging, test, demo, and production configuration and data. |
| 80 | Demo Tenant Safety Design | P1 | Prevent demos from creating unsafe data, leaking real data, or bypassing security assumptions. |
| 81 | Test Tenant Architecture | P0 | Create isolated tenants and users for integration, RLS, and E2E validation. |
| 82 | SaaS Onboarding Architecture | P2 | Design first-run experience, tenant setup checklist, invitations, guidance, and first value path. |
| 83 | SaaS Offboarding Architecture | P1 | Handle user removal, tenant cancellation, exports, retention, billing, and access revocation. |
| 84 | Tenant Migration Strategy | P1 | Move tenants, settings, storage, billing, and users across environments or plans safely. |
| 85 | SaaS Data Residency Planning | P2 | Plan regional data boundaries, storage choices, replication, and compliance implications. |
| 86 | SaaS Localization Architecture | P2 | Design locale, currency, date/time, language, and content localization boundaries. |
| 87 | SaaS Timezone Architecture | P1 | Handle tenant timezones, user timezones, scheduled jobs, reminders, and reporting boundaries. |
| 88 | SaaS Audit Readiness Design | P1 | Collect evidence for access, change control, security reviews, approvals, and operational actions. |
| 89 | SaaS Cost Observability | P1 | Track infrastructure, AI, storage, provider, integration, and tenant-level cost drivers. |
| 90 | SaaS Incident Blast Radius Mapping | P1 | Determine affected tenants, users, data, integrations, and workflows during incidents. |

## Historical implementation checklist

This is the original candidate-conversion checklist. For a new or changed
executable skill, follow the [current skill generation
standard](../skill-generation-standard.md) and its required validation. The
checklist called for:

- Purpose
- When to use
- Required inputs
- Step-by-step workflow
- Expected outputs
- Validation checklist
- Anti-patterns / stop conditions
