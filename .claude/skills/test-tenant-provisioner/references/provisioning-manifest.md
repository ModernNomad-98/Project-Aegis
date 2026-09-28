# Provisioning manifest, markers, drift classes and lint rules

Detail for [`test-tenant-provisioner`](../SKILL.md). Read on demand. RLS is
row-level security; E2E is end-to-end; CI is continuous integration; API is
application programming interface.

## 1. Desired-state manifest

The manifest is derived from the persona catalog that `test-data-architect`
produces. It never adds a persona the catalog does not name. Keep it in the
repository next to the catalog so a reviewer can diff it.

```yaml
environment: staging-eu          # the named non-production target
marker:
  field: test_fixture             # column, metadata key or identity-provider tag
  value_format: "ttp:<suite>:<catalog-id>"
tenants:
  - id: tenant-a                  # stable catalog id
    slug: acme-test
    marker: "ttp:e2e:tenant-a"
users:
  - id: tenant-a-owner
    email: owner.tenant-a@example.test   # reserved test domain, never a real one
    tenant: tenant-a
    role: owner
    credential_env: TTP_TENANT_A_OWNER_PASSWORD   # NAME only, never the value
    marker: "ttp:e2e:tenant-a-owner"
memberships:
  - user: tenant-a-member
    tenant: tenant-b              # deliberate cross-tenant membership, if the catalog says so
    role: viewer
grants:
  - id: grant-support-flag
    subject: tenant-a-admin
    capability: support_access
    backup: required
```

Rules:

- One row per catalog identity. Stable ids come from the catalog, not from the
  environment's generated primary keys.
- Emails and domains use reserved test domains (`example.test`,
  `example.com` subaddresses or the product's documented test domain).
- `credential_env` holds the variable NAME. The manifest, report and logs
  never hold a value.

## 2. Marker conventions

Choose the most structural marker the platform supports, in this order:

1. A dedicated column or metadata field (`test_fixture`) set at creation.
2. An identity-provider user attribute or app-metadata tag.
3. A tenant-level flag (for example `is_test_tenant = true`) plus a per-row
   field for users and memberships.
4. Naming only (prefix or reserved domain) is the weakest option. Use it only
   when nothing else exists, and say so in the report, because a person can
   hand-create a row with the same name.

Scope the marker value by suite or owner (`ttp:<suite>:<id>`) in shared
environments so one team's run never classifies another team's rows as its
own orphans.

## 3. Drift classes

| Class | Meaning | Validate-only | Apply mode |
| --- | --- | --- | --- |
| OK | Marked row matches the manifest | report | no action |
| MISSING | No row for a catalog identity | report | create with marker |
| DRIFTED | Marked row differs (role, tenant, membership, grant) | report the difference | repair the marked row |
| ORPHANED | Marked row with no catalog identity | report | delete only on an explicit, separate request |
| BLOCKED | UNMARKED row collides with a catalog identity | report | never touched; human decides |
| UNVERIFIED | No read path to the current state | report | apply refused until state can be read |

## 4. Capability grants: backup first, rollback beside

A capability grant is any change to what a principal may do: a role, a
permission row, an elevated flag, a support or impersonation capability.

For each grant, the plan shows three lines together:

```
Grant grant-support-flag: tenant-a-admin gains support_access
  Backup: export of current grants for tenant-a-admin → <reference id>
  Rollback: revoke support_access from tenant-a-admin; restore <reference id>
```

If the backup cannot be taken, or the rollback cannot be stated as one exact
step, the grant is skipped and reported. The backup reference is recorded in
the report so a later reader can undo the grant without this conversation.

## 5. Production-reach lint rules

Static and read-only. Inputs: the declared production hosts, project or
database identifiers, and account or tenant ids.

Flag, with file and line:

- A test runner base URL, API host or web socket host equal to a production
  host (for example a Playwright `baseURL`).
- A connection string or database identifier that names a production
  project or host.
- An environment-variable fallback default that points at production, such as
  `process.env.API_URL ?? "https://app.example.com"`.
- A CI job that runs test or seed commands with production secrets or a
  production environment name.
- A seed or provisioning script without an environment guard that refuses
  production.

The lint compares declared values. It does not resolve DNS or call hosts
unless that network access is separately authorized; when a host is an
alias whose target is unknown, report it as UNRESOLVED rather than clean.
