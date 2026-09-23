# Software as a service (SaaS) security and row-level security (RLS)

Security skills for tenant isolation, RLS, authorization, secrets, storage, and auditability.

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

Terms in the table: SaaS means software as a service; RLS means row-level
security; MFA means multifactor authentication; SSO means single sign-on; CSRF
means cross-site request forgery; XSS means cross-site scripting; SQL means
Structured Query Language; URL means web address; API means application
programming interface; IP means Internet Protocol address; CSP means Content
Security Policy; HTTP means Hypertext Transfer Protocol; HSTS means HTTP
Strict Transport Security; CI means continuous integration; PII means
personally identifiable information. `SECURITY DEFINER` is a PostgreSQL
function privilege mode; `tenant_id` and `owner_id` are record identifiers.
SELECT, INSERT, UPDATE and DELETE are database read, create, change and
removal operations; RPC means remote procedure call; auth means
authentication.

| # | Skill | Priority | Usage |
|---:|---|---|---|
| 91 | Threat Modeling Facilitation | P0 | Identify assets, actors, trust boundaries, abuse paths, mitigations, and validation tests. |
| 92 | Abuse Case Development | P0 | Turn likely attacker behavior into concrete negative tests and security requirements. |
| 93 | Tenant Isolation Review | P0 | Inspect every path where tenant data can leak across queries, storage, logs, caches, or integrations. |
| 94 | RLS Policy Authoring | P0 | Write precise SELECT, INSERT, UPDATE, and DELETE policies using tenant, membership, role, and resource checks. |
| 95 | RLS Negative Test Design | P0 | Prove unauthorized reads and writes fail for wrong tenant, wrong role, wrong user, and missing auth. |
| 96 | RLS Recursion Avoidance | P0 | Design helper functions and policies that avoid recursive table access and runtime policy failures. |
| 97 | SECURITY DEFINER Helper Design | P0 | Build safe Postgres helpers with fixed search paths, least privilege, and predictable semantics. |
| 98 | Deny-by-Default Policy Review | P0 | Confirm data remains inaccessible unless an explicit, tested policy allows access. |
| 99 | Tenant ID Enforcement | P0 | Require tenant-owned records to carry trusted tenant scope or document an approved alternate model. |
| 100 | Server-Derived Scope Enforcement | P0 | Reject frontend-provided actor, tenant, role, project, or resource hints when untrusted. |
| 101 | Protected Write Path Design | P0 | Require sensitive writes to go through server-side command or service paths. |
| 102 | Service Role Containment | P0 | Keep service-role keys in server-only runtime and prevent exposure through frontend, logs, or tests. |
| 103 | Secret Management Design | P0 | Define where secrets live, how they load, who can access them, and how they rotate. |
| 104 | Credential Encryption Design | P0 | Use appropriate encryption, hashing, key derivation, and rotation for stored credentials. |
| 105 | Sensitive Column Masking | P0 | Prevent exposure of private fields such as credentials, tokens, phone numbers, emails, and internal notes. |
| 106 | Authorization Matrix Design | P0 | Map roles and permissions to actions, resources, screens, commands, reports, and data fields. |
| 107 | Privilege Escalation Review | P0 | Test whether users can upgrade roles, access admin actions, modify ownership, or bypass approvals. |
| 108 | Authentication Flow Review | P0 | Review login, logout, reset, MFA, SSO, session refresh, device trust, and profile resolution. |
| 109 | Session Handling Security | P0 | Validate token storage, refresh behavior, expiration, revocation, and cross-tab/device behavior. |
| 110 | CSRF and Browser Boundary Review | P1 | Assess browser-side mutation paths, cookies, headers, origins, and cross-site risks. |
| 111 | XSS Defense Review | P0 | Review rendering, markdown, rich text, user content, third-party widgets, and escaping boundaries. |
| 112 | SQL Injection Defense Review | P0 | Check dynamic SQL, filters, RPCs, search, sorting, and migration scripts for injection risks. |
| 113 | Mass Assignment Defense | P1 | Ensure clients cannot submit restricted fields such as role, tenant_id, owner_id, status, or billing fields. |
| 114 | Insecure Direct Object Reference Review | P0 | Verify every resource access checks ownership, tenant, membership, and action-specific authority. |
| 115 | Storage Access Policy Review | P0 | Validate bucket policies, signed URL expiry, path naming, ownership checks, and public asset boundaries. |
| 116 | Webhook Security Design | P1 | Validate signatures, replay protection, idempotency, tenant mapping, and safe error handling for webhooks. |
| 117 | API Rate Limit Design | P1 | Apply rate limits by actor, tenant, IP, token, endpoint, feature, and abuse category. |
| 118 | Audit Log Security Review | P0 | Ensure security-relevant events are logged without storing secrets or unsafe payloads. |
| 119 | Security Error Response Design | P0 | Return safe errors that do not reveal record existence, user existence, tenant membership, or secret state. |
| 120 | Security Header Review | P1 | Review CSP, HSTS, frame, referrer, permissions, and content type headers for browser apps. |
| 121 | Dependency Vulnerability Review | P1 | Assess package vulnerabilities, exploitability, upgrade risk, lockfile integrity, and compensating controls. |
| 122 | Supply Chain Risk Review | P1 | Review build steps, scripts, GitHub Actions, packages, artifacts, and external downloads for compromise paths. |
| 123 | Environment Variable Exposure Review | P0 | Classify public, server-only, CI-only, local-only, and deployment-only environment variables. |
| 124 | Logging Redaction Review | P0 | Ensure logs redact credentials, tokens, PII, provider payloads, tenant secrets, and private data. |
| 125 | Security Regression Harness | P0 | Create permanent tests for every fixed security bug or access-control gap. |
| 126 | Secure Migration Review | P0 | Review migrations for privilege changes, policy gaps, unsafe defaults, broad grants, and destructive operations. |
| 127 | Security Impact Note Authoring | P0 | Document impact, risks, mitigations, tests, rollback, and approval needs for security-sensitive changes. |
| 128 | Compliance Evidence Mapping | P1 | Map controls to evidence such as logs, approvals, tests, policies, and change history. |
| 129 | Privacy-by-Design Review | P1 | Minimize data collection, define purpose, restrict access, support deletion, and document retention. |
| 130 | Security Drift Detection | P0 | Compare code, policies, tests, and docs to catch weakened or undocumented security behavior. |

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
