# Authorization Matrix Templates & Negative-Test Catalog

Supporting detail for the owning [Authorization Matrix Designer](../SKILL.md).
Read on demand. User interface (UI) is the visible control surface; an
application programming interface (API) is the server contract; insecure
direct object reference (IDOR) is an object access attempt without the
required authorization check.

## Permission naming convention

`<verb>:<resource>` — e.g. `read:project`, `export:dataset`, `manage:billing`,
`invite:member`. Verbs from a closed set (read, create, update, delete,
export, share, invite, manage, impersonate). No role names inside permission
names; no plan names anywhere (that axis belongs to entitlements).
Assignment permissions use `grant:<role>` — e.g. `grant:member`,
`grant:admin` — the grant axis: who may assign which role.

## Matrix template

| Permission ↓ / Role → | owner | admin | member | guest | support (brokered) | service-account |
| --- | --- | --- | --- | --- | --- | --- |
| read:project | ✓ | ✓ | ✓ | ✓(shared only) | ✓(grant) | ✓(scoped) |
| update:project | ✓ | ✓ | ✓(own) | — | — | — |
| export:dataset | ✓ | ✓ | — | — | — | — |
| manage:billing | ✓ | — | — | — | — | — |
| invite:member | ✓ | ✓ | — | — | — | — |
| impersonate:user | — | — | — | — | ✓(grant, time-boxed) | — |
| grant:member | ✓ | ✓ | — | — | — | — |
| grant:admin | ✓ | — | — | — | — | — |

Empty cell = denied. Parenthetical = object-level rule that further narrows
the allow. Every ✓ in the support column requires an active brokered grant
and emits an audit event.

## Enforcement-point map template

| Surface | Check location | Authoritative? |
| --- | --- | --- |
| UI | Hide/disable controls | No — UX only |
| API | Middleware + shared decision point | Yes |
| Service layer | Object-level rules at repository/service | Yes (object rules) |
| Background jobs | Job context carries actor + tenant; same decision point | Yes |
| Integrations/webhooks | Token scopes mapped to permissions | Yes |
| Admin console | Same shared decision point — no parallel logic | Yes |

## Grant-ceiling table template

| Actor level | May grant roles | Ceiling rule |
| --- | --- | --- |
| owner | all tenant roles | at or below owner |
| admin | member, guest | at or below admin |
| member | — (none) | grants nothing |
| support (brokered) | — (none) | explicit grants only, time-boxed |

The ceiling is structural: an actor may grant only roles at or below their
own level, enforced at the grant path — never advice.

## Custom-role composition template

| Field | Bound |
| --- | --- |
| Name | tenant-scoped, closed vocabulary |
| Permissions | composed from the tenant's template permission set only |
| Ceiling | never exceeds the tenant's own ceiling |
| Inheritance | inherits from at most one built-in parent role |
| Audit | every create/change emits an audit event (schema via audit-log-architect) |

## Negative-test catalog (minimum set)

- **IDOR probe:** member of tenant A requests tenant B's resource by id on
  every resource type → deny/404 per stated policy.
- **Vertical escalation:** member attempts admin-only action (invite, export,
  billing) via direct API call, not UI → denied.
- **Horizontal reach:** member A attempts update on member B's owned object
  where matrix says own-only → denied.
- **Revocation:** remove membership/role, then replay a previously successful
  request with the still-live session and API token → denied.
- **Impersonation expiry:** support acts after grant expiry / without grant →
  denied AND the attempt is audited.
- **Machine actor:** service account attempts an action outside its scoped
  permissions → denied (service accounts don't inherit human roles).
- **Disabled tenant:** any role attempts writes in a suspended tenant →
  denied per lifecycle posture.
- **Self-escalation:** an actor grants themselves a role above their own
  level → denied at the grant path AND audited.
- **Above-ceiling grant:** an actor grants a role above their grant ceiling →
  denied at the grant path AND audited.
- **Custom role out of bounds:** a custom role includes a permission outside
  its tenant-bounded template → rejected at creation/change.
- **Custom-role cross-tenant:** a custom role created in tenant A grants
  anything in tenant B → denied; the role is tenant-scoped.
