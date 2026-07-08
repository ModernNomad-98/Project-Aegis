# Approval Register — Format, Lifecycle, Placement

Companion to `scoped-approval-register`. Everything here is product-agnostic;
identifiers are placeholders (`<owner>/<repo>`, `<tenant-id>`) per house rule.

## Entry template

```markdown
### APR-<NNN>: <short imperative title>

- **Status:** ACTIVE
- **Date / Grantor:** <YYYY-MM-DD> / <named human or role, e.g. "repo owner">
- **Reason:** <the need this authorization answers — one or two sentences>
- **Scope allowed:** <exact actions, files/paths, branches, environments,
  tenants covered — in or quoting the grantor's wording>
- **Scope FORBIDDEN:** <explicit adjacent actions this grant does NOT cover>
- **Evidence:** <link to the grant: PR comment URL, issue reply, dated chat
  record committed to the repo, commit SHA>
- **Expiry:** <YYYY-MM-DD | "one-time" | "until <condition>" | "until superseded">
```

## Field semantics

| Field | Rule |
| --- | --- |
| Status | One of `ACTIVE`, `SUPERSEDED by APR-<NNN>`, `EXPIRED <date>`, `REVOKED <date, by whom>`. The only field ever edited in place — and only to flip state. |
| Date / Grantor | A NAMED human or role. "The team" cannot be cited; a person or accountable role can. |
| Reason | Why the authorization exists. Lets a future reader judge whether the reason still holds before leaning on the entry. |
| Scope allowed | The grantor's wording governs. If the wording and the recorded scope differ, the wording wins and the entry is defective. |
| Scope FORBIDDEN | Mandatory and non-empty. Name the adjacent actions a future agent would plausibly stretch this grant to cover (the next environment up, the neighboring table, the protected branch). |
| Evidence | A retrievable pointer. An entry without evidence records a claim, not a grant. |
| Expiry | One-time grants die on use — flip to `EXPIRED` when consumed. Phase-scoped grants name the phase. Durable grants say `until superseded`. |

## Lifecycle rules

1. **Append-only history.** New authorization = new entry. Never rewrite an
   old entry's scope; never delete an entry. The register's value under audit
   is that its history is trustworthy.
2. **Supersede, don't edit.** Widening/narrowing scope: write APR-042, flip
   APR-017 to `SUPERSEDED by APR-042`. Both remain readable.
3. **Revocation is a state, not a deletion.** `REVOKED 2026-07-07, by <role>`
   preserves both the grant and its withdrawal.
4. **Consumed one-time grants are flipped promptly** — an ACTIVE one-time
   entry that already fired is a phantom authorization.
5. **Expiry sweep:** whenever the register is touched, flip any entry whose
   expiry has passed. Stale-ACTIVE is the register lying.

## Citation rule (state at the top of every register)

> An action is authorized by this register only if an **ACTIVE** entry's
> **Scope allowed** covers it as worded. Absence from any FORBIDDEN list is
> not permission — deny-by-default holds. FORBIDDEN beats allowed on
> conflict, within and across entries.

## Placement options

| Option | When |
| --- | --- |
| Dedicated `docs/approvals/APPROVAL_REGISTER.md` | Default. One file, append-style, easy to link. |
| Exceptions section inside the repo's context map | House pattern observed in a production multi-agent repo (Repo A): ~60 "narrow exception" blocks with exactly these fields, co-located with the context the exceptions modify. Valid when a context map is already the governance hub — pairs with `context-co-update-ci-gate`. |
| Per-phase blocks inside stage/phase docs | Acceptable for phase-scoped grants; add a pointer line to the central register so citation stays one-hop. |

Never two authoritative registers. If both a dedicated file and a context-map
section exist, one must declare itself a pointer to the other.

## Worked example

```markdown
### APR-013: Backfill script may run against the staging tenant

- **Status:** ACTIVE
- **Date / Grantor:** 2026-07-07 / repo owner
- **Reason:** Orders backfill (issue #88) needs one supervised run before the
  migration PR can be validated end-to-end.
- **Scope allowed:** Run `scripts/backfill-orders.ts` in validate-only AND
  apply mode against tenant `<staging-tenant-id>` on the staging environment,
  during the issue-#88 work only.
- **Scope FORBIDDEN:** Any production tenant or environment; any other
  script; schema changes; re-running after issue #88 closes without a new
  grant.
- **Evidence:** PR #91 review comment (link) — "approved for staging tenant
  only, one issue's duration".
- **Expiry:** until issue #88 closes.
```

## Anti-patterns

- **The optimistic paraphrase** — "sure" recorded as approval of the whole
  plan. Record what the "sure" answered.
- **The empty FORBIDDEN field** — an entry that closes no doors decides
  nothing; disputes always arrive at the adjacent action.
- **The evidence-free entry** — "approved verbally" with no committed record.
  If the grant only exists in ephemeral chat, commit the dated quote first
  (`chat-backlog-reconciliation` is the cadenced version of this move).
- **The self-service widening** — an agent extending its own entry's scope
  because the new action is "basically the same". Widening is a new grant.
- **Registering policy instead of grants** — standing authority rules (what
  agents may EVER do) belong to `agent-authorization-matrix`; a designed
  standing-approval loop belongs to `standing-approval-and-auto-advance`.
  The register records that a specific grant happened, including — as one
  entry — the human's adoption of such a policy.
