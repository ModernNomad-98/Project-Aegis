# Tenant Lifecycle & Membership Catalog

Supporting detail for `tenant-modeler`. Read on demand.

## Lifecycle state/posture table (starter)

| State | User access | Data | Billing | Background jobs |
| --- | --- | --- | --- | --- |
| Provisioning | None (or admin-only setup) | Seeding | Not started / trial clock pending | Setup jobs only |
| Active | Full per role | Read/write | Charging per plan | All |
| Suspended | Blocked (or read-only — pick one and say why) | Intact, frozen writes | Paused or payment recovery | Stopped except billing/retention |
| Offboarding | Export-only for owners | Read-only, export available | Final invoice | Export + retention jobs only |
| Purged | None | Destroyed (backups per retention policy) | Closed | None |

Transitions worth defining explicitly: payment-failure → suspended (after what
grace?), suspended → active (restore is instant?), offboarding → purged (after
what window? who can cancel it?), each eligible non-purged state → offboarding
(which states permit it, and who may trigger it?). `Purged` has no transition
back to offboarding or an active state.
Purge is irreversible: it requires an approval gate and an audit event.
For each allowed transition, record its trigger, side effects, reversibility,
and actor. For example, an active tenant suspended after an expired payment
grace period may have jobs and writes stopped, then regain access through an
authorized billing recovery action. The actual policy must choose the grace
period and actor.

## Membership patterns

| Pattern | Model consequence |
| --- | --- |
| Single-tenant user | Simplest; still model membership as an entity so it can evolve |
| Multi-tenant user | One user identity, one membership per tenant; role/status per membership; active-tenant selection is session state, not identity state |
| Guest / external member | Membership with restricted role + expiry; counted or not counted as a seat (decide) |
| Service account | Membership owned by the tenant, not a person; credentials rotate; never inherits a human's role |
| Domain capture | Users signing up with a verified email domain auto-join or request membership in that tenant; explicit tenant opt-in required |

## Invitation state machine

From `draft`, send an invitation. From `sent`, exactly one terminal outcome
applies: `accepted`, `expired`, or `revoked`.

- `sent → accepted`: creates the membership atomically; an invitation is not a
  membership.
- `sent → expired`: time-boxed; re-invite creates a new invitation (audit trail
  keeps both).
- `sent → revoked`: revocation wins over a concurrent acceptance — decide the
  race explicitly.
- Invitations carry the role they grant; changing the role after acceptance is
  a membership operation, not an invitation edit.
- Who may invite is a permission (feeds `authorization-matrix-designer`), and
  invite volume is a plan limit candidate (feeds `plan-entitlement-architect`).
