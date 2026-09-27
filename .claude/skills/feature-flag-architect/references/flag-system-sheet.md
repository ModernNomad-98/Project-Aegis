# Flag system sheet

Lookup material for the [feature-flag-architect](../SKILL.md) skill, read
on demand from its Workflow steps 2, 4 and 6–9. Nothing here authorizes signing up,
paying, adding an SDK (software development kit: the client library a flag
service ships), or changing a live system. **TTL** (time to live) is how
long a cached value is kept before it is refreshed; **UI** means user
interface. **Edge** means servers at the network edge, close to the user,
rather than your application servers. **First paint** is the moment a
browser first draws the page. **Data residency** is a requirement that data
stay in a named country or region. A **break-glass** change is an audited
emergency action taken outside the normal approval path.

**Volatility notice.** Flag products, open-source projects and their prices
change often. This sheet names categories, not products, on purpose. Verify
current products and prices at decision time; where a price is not
verified, say "unknown" in the owner-facing comparison.

## 1. Flag store options (step 2)

| Option | Can do | Cannot do (or costs extra effort) | Money | Setup time | Upkeep |
| --- | --- | --- | --- | --- | --- |
| Config in the repository | Simple on/off per environment; reviewed like code | Per-customer targeting; instant off (every change is a release); change audit beyond version history | None beyond existing hosting | Hours | Low, but every flip costs a release |
| Flag table in your own database + small admin screen | Per-tenant overrides; instant off within the cache TTL; audit through your own event | Percentage bucketing, experiments and streaming propagation unless you build them | Existing database; no license | Days | You own the code, the admin screen and its access control |
| Self-hosted open-source flag server | Targeting rules, percentages, SDKs for several languages, often an admin UI | Only what the chosen project supports; you run, patch and back it up | Hosting cost (unknown until sized); no license for most projects — verify | Days to a couple of weeks | Patching, upgrades, availability of one more service |
| Hosted flag vendor | Rich targeting, streaming updates, audit, experiments, non-engineer UI | Nothing major technically; data leaves your infrastructure; cost grows with seats, usage or monthly active users | Subscription — volatile; verify current pricing | Hours to days | Low operationally; ongoing bill and vendor dependency |

### Recommendation patterns (starting points, not rules)

- One app, one small team, a handful of per-customer switches, no
  experiments, only engineers flip flags → **own database table + code
  defaults**. Changes that would flip it: several services needing the same
  flags, planned experiments, or non-engineers who must flip flags safely.
- Several services or teams, planned experiments, or support / product
  staff flipping flags → **self-hosted server or hosted vendor**. Choose
  between them on who will run it (ops capacity) versus budget and data
  residency.
- Static site only, no runtime server → **build-time config**, stated with
  its limit: every change needs a rebuild and publish.
- Regulated data or strict data residency → prefer a store inside your own
  infrastructure unless a vendor's terms are verified to fit.

Always name the single fact that would move the recommendation, and ask
only for that fact first if it is missing.

## 2. Evaluation placement (step 4)

| Placement | Good for | Staleness | Latency | Flicker | Never use for |
| --- | --- | --- | --- | --- | --- |
| Server, per request | Anything tenant- or security-sensitive; default | Cache TTL or stream lag | One in-process lookup when cached | None | — |
| Client | Presentation-only variation | Until the next fetch or stream event | Network on first load unless bootstrapped | Yes, unless bootstrapped from the server render | Sole enforcement of access or limits |
| Edge | Cached pages varying by a coarse attribute | Edge config propagation | Low | None | Per-user or per-tenant sensitive decisions without verified identity |
| Build time | Static pages | Until the next build | None | None | Anything needing instant off |

Bootstrapping: the server renders the evaluated client flags into the page
so the client starts with correct values and avoids a flash of the wrong
variant.

## 3. Fail-safe mechanism checklist (step 6)

The safe VALUE per flag comes from `feature-flag-rollout-strategist`. The
mechanism guarantees the system reaches it.

- [ ] Every call site passes a code-level default equal to the flag's safe
      value.
- [ ] A last-known-good cache (in memory, optionally persisted) or a
      bootstrap snapshot serves values when the flag service is unreachable.
- [ ] Evaluation has a timeout stated in milliseconds and never blocks a
      request or first paint; on timeout the cached or default value wins.
- [ ] Cold start with no cache and no service returns the code default and
      emits a metric.
- [ ] The fallback is exercised in a non-production environment by making
      the flag service unreachable, and the observed behavior matches the
      design.
- [ ] Fallback use is observable: a metric or log line when the system is
      serving cached or default values.

## 4. Kill-switch propagation (step 7)

| Option | Reach bound | Cost | Notes |
| --- | --- | --- | --- |
| Streaming (server push) | Seconds | Persistent connections; reconnect logic | Best for kill switches; needs a polling fallback |
| Polling | Poll interval + cache TTL | Simple; load grows with instances × frequency | State the bound as interval + TTL, not "instant" |
| Local override | Next config read | Needs a config channel independent of the flag service | Must work when the flag service is down |

Flip authority: name the roles per environment (production normally
narrower than staging); the role definitions come from
`authorization-matrix-designer`; the console that enforces them belongs
with `admin-console-architect` when it lives in the ops console.

## 5. Audit event fields (step 8)

`actor`, `actor_type` (human, service, break-glass), `flag_key`,
`environment`, `change_kind` (new, flip, rule change, override change,
removal), `value_before`, `value_after`, `targeting_before`,
`targeting_after`, `tenant_scope` (when the change is a per-tenant
override), `reason`, `timestamp`. The storage, integrity and retention
design belongs to `audit-log-architect`.

## 6. Registry fields (step 9)

`flag_key`, `type` (release, operational, experiment), `owner`,
`date_added`, `expiry_or_review_date`, `safe_value` (from the strategist's
plan), `evaluation_placement`, `tenant_sensitive` (yes/no),
`linked_change` (ticket or spec). A release flag past its expiry date
raises an alert; removing it is planned by `feature-flag-rollout-strategist`.
