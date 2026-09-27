---
name: feature-flag-architect
description: 'Design the feature-flag SYSTEM a product runs on — flag store build-vs-buy (an owner choice), SDK and config placement, where flags evaluate (server, client, edge, build time), targeting context (tenant, plan, role, cohort, environment) with tenant-safe caching, the fail-safe mechanism for a flag-service outage (code defaults, last-known-good cache, timeouts), kill-switch propagation and who may flip it, flag-change audit trail, and flag-debt hooks (owner/expiry registry, stale-flag report). Designs; writes nothing. Use when choosing or building a flag service, wiring flags into code, or when flags evaluate inconsistently across surfaces or tenants. Do NOT use for one change''s staged rollout, guardrails or flag removal (feature-flag-rollout-strategist), plan entitlements (plan-entitlement-architect), role permissions (authorization-matrix-designer), experiment design (ab-test-designer), deploy strategy (ci-pipeline-architect), or reviewing existing flags for cross-tenant leaks (tenant-isolation-reviewer).'
---

# Feature Flag Architect

Terms: a **feature flag** is a named on/off (or multi-value) switch the code
checks at run time. An **SDK** (software development kit) is the client
library a flag service ships for your code to call. **Evaluation** is the
moment a flag's value is worked out for one request or user. A **kill
switch** is a long-lived flag that turns a feature off fast. **CI** means
continuous integration; **GA** means general availability; **TTL** means
time to live; **SSR** means server-side rendering.

## Purpose

Most flag trouble is not one bad rollout — it is a flag SYSTEM nobody
designed. Flags live in three places at once (environment variables, a
database column, a vendor dashboard); the SDK blocks page render when the
flag service is slow; per-tenant overrides are cached under the flag name
alone, so one customer sees another's setting; a kill switch takes ten
minutes to reach every instance and anyone with dashboard access can pull
it; nobody can say who flipped what; and dead flags pile up because nothing
makes them visible. This skill designs the system every rollout then runs
on: where flags are stored (a build-vs-buy choice the owner makes, taught
before asking), how the code reaches them through one internal interface,
where each class of flag is evaluated, the targeting context and its
sources of truth, the fail-safe mechanism that guarantees each flag falls
back to its safe value, how a kill switch propagates and who may pull it,
the flag-change audit event, and the hooks that expose flag debt. It
designs and explains; it installs, signs up for, pays for, and flips
nothing.

## Use When

- Use when: choosing where flags should live — config in the repository,
  a flag table in the product's own database, a self-hosted open-source
  flag server, or a hosted flag vendor — and the owner needs the choice
  explained.
- Use when: wiring flags into a codebase for the first time, or
  consolidating flags scattered across environment variables, database
  toggles, hard-coded tenant checks and a vendor SDK.
- Use when: flags evaluate inconsistently — different answers on server
  and client, between surfaces, between instances, or between tenants.
- Use when: the flag SDK slows or blocks requests or page render, or the
  app misbehaves whenever the flag service is unreachable (the fallback
  MECHANISM is missing).
- Use when: designing how fast a kill switch reaches every instance, who
  may pull it in each environment, and how flag changes are audited.
- Use when: flag debt needs system-wide visibility — a registry with
  owners and expiry dates, a stale-flag report, code-reference search.
- Do NOT use when: planning ONE change's rollout — its stages, guardrail
  metrics, auto-rollback, the safe value for that flag, or removing that
  flag after GA. That is `feature-flag-rollout-strategist`, which runs on
  whatever flag system exists.
- Do NOT use when: deciding what a plan includes — "Pro gets SSO",
  limits, quotas, or "leave this flag on permanently for Enterprise".
  That is a permanent entitlement: `plan-entitlement-architect`.
- Do NOT use when: defining which roles may do what — including the role
  definition behind "who may flip production flags". That is
  `authorization-matrix-designer`; this skill consumes its roles.
- Do NOT use when: designing or reading an experiment — hypothesis,
  sample size, significance. That is `ab-test-designer`; this skill only
  guarantees consistent assignment.
- Do NOT use when: designing the deploy strategy (canary deploy,
  blue/green) or pipeline gates. That is `ci-pipeline-architect`, a
  manual-only skill: name it to the user, who invokes it.
- Do NOT use when: reviewing an existing flag setup for cross-tenant
  leakage — that is `tenant-isolation-reviewer` — or placing the flag
  service among control-plane capabilities, which is
  `saas-platform-architect`.
- Do NOT use when: designing a general cache layer, TTLs or invalidation
  beyond flag evaluation — that is `caching-strategy-designer`. This skill
  owns only how evaluated flag values are cached and keyed.
- Do NOT use when: an access change — a revoked role, a membership
  removal, a plan downgrade — did not take effect and old authority is
  still honored somewhere. That is `authority-invalidation-architect`;
  this skill owns how FLAG changes reach every instance.

## Inputs to Inspect

1. Every existing flag mechanism: environment variables and config files
   that act as switches, database toggles, hard-coded tenant or user-ID
   checks, and any flag or experiment SDK already present.
2. The rendering and runtime model: server-rendered pages, SSR, a
   single-page app, static or edge-hosted pages, mobile clients — and how
   many services and instances run.
3. The tenancy model and identity source (from `tenant-modeler` or
   `saas-platform-architect` output where it exists): where tenant, plan
   and role are authoritatively read on the server.
4. The entitlement resolution point, if `plan-entitlement-architect` has
   defined one — plan-derived targeting must read it, not copy it.
5. The latency budget (from `latency-budget-architect` where it exists)
   and any render-blocking or request-blocking flag calls today.
6. Existing admin or ops console surfaces, audit log platform, and cache
   layers the flag system would share.
7. The recorded owner context: team size, who is expected to flip flags,
   whether experiments are planned, budget stance, and any recorded store
   decision (in `docs/project-state.md` or an ADR).

## Workflow

1. **Inventory before designing.** List every existing flag mechanism
   from Inputs 1–2 with its location, who can change it, and how a change
   takes effect. Mark flags that are really permanent entitlements or
   permissions and route them out now (Stop Conditions). Record the
   rendering model, service and instance count, tenancy model and latency
   budget; each constrains a later step.
2. **Flag store — an owner choice; teach it before asking.** If the owner
   has already recorded a store decision, design on it and skip the
   question. Otherwise define, in plain language, the viable stores:
   **config in the repository** (values ship with the code, so a change
   needs a new release and there is no per-customer or instant-off switch
   at run time), **a flag table in your own database** with a small admin
   screen (you own the code and its upkeep), **a self-hosted open-source
   flag server** (existing software you run and patch on your own
   infrastructure), and **a hosted flag vendor** (a paid service that
   stores and serves flags for you). For each viable option give why it
   could fit this product; what it can and cannot do here (per-customer
   targeting, instant off, change audit, consistent experiment
   assignment); its pros and cons; and its money, setup-time and upkeep
   cost — mark vendor and hosting prices as unknown or volatile unless
   verified at decision time, never invented. Recommend one option, say
   why it fits the recorded needs, and name the fact that would change the
   recommendation. If a deciding fact is missing, ask only for that fact
   first. Then ask exactly one atomic owner question. The answer is a
   design preference and grants no authority: signing up, paying, or
   adding an SDK stays with the human approval path, and this skill does
   none of it. Recommendation patterns:
   [references/flag-system-sheet.md](references/flag-system-sheet.md).
3. **One internal flag interface.** Call sites use one internal flag
   interface (an adapter) that wraps the chosen store, so no call site
   imports a vendor SDK directly and a later store change touches one
   module. Flag definitions are typed, and each has a registry entry
   (step 9). Server-side SDK keys and client-safe keys stay separate: a
   server key never ships to client code, and a client receives only the
   evaluated values of the flags it needs — never the targeting rules or
   other tenants' overrides.
4. **Decide where each flag class evaluates.** Per request on the server
   is the default, and mandatory for anything tenant- or
   security-sensitive. Client-side evaluation is for presentation only and
   is never the sole enforcement. Edge evaluation suits cached pages that
   vary by a coarse attribute. Build-time flags suit static pages, and a
   change needs a rebuild. State what each placement costs in staleness,
   latency and flicker, and pick one per flag class. This is internal
   mechanics: decide it and explain it; do not turn it into an owner
   question.
5. **Targeting context model.** Name the attributes (tenant, plan, role,
   cohort, environment, region), the server-side source of truth for each
   (identity or the tenant record — never a value the client asserts), and
   the precedence: kill switch > per-tenant override > targeting rule >
   default. Plan-derived targeting READS the entitlement resolution point
   and never duplicates it. Percentage and cohort bucketing hash a stable
   identifier, and flags and experiments share one bucketing function so
   assignment stays consistent. Every cached per-tenant value is keyed by
   tenant as well as flag; a cache key without the tenant is a
   cross-tenant leak.
6. **Fail-safe mechanism.** The strategist picks each flag's safe value;
   this skill designs the mechanism that falls back to it. Specify: a
   code-level default at every call site (set to the strategist's safe
   value); a last-known-good cache or bootstrap snapshot served when the
   flag service is unreachable; an evaluation timeout, stated in
   milliseconds, that never blocks a request or a page render; cold-start
   behavior with no cache (serve the code default and emit a metric, so
   fallback use is visible); and how the fallback is
   exercised in a non-production environment by making the flag service
   unreachable. A flag that fails open into unfinished code is the defect
   this step exists to prevent.
7. **Kill-switch propagation and authority.** Choose streaming or polling
   and state the upper bound, in seconds, for a flip to reach every
   instance and client. Name who may flip in each environment — the role
   definitions come from `authorization-matrix-designer`, and the flag
   console enforces them. Design a break-glass path for off-hours, and a
   local override that still works when the flag service itself is down.
8. **Flag-change audit event.** Specify the event every new flag, flip,
   rule change and removal emits: actor, flag, environment, value before
   and after, targeting change, reason and timestamp. This skill defines
   the event; the audit platform — append-only storage, retention, scoped
   reads — is `audit-log-architect`'s.
9. **Flag-debt hooks.** Registry metadata per flag: owner, type (release,
   operational, experiment), date added, an expiry or review date, and the
   safe value (recorded from the strategist's choice, so the code default
   and the registry agree). Add
   a stale-flag report or a non-blocking CI check (its pipeline wiring is
   `ci-pipeline-architect`'s, invoked by the user), code-reference search
   so every flag's call sites can be found, and an alert when a release
   flag passes its expiry. Removing a given flag is the strategist's job;
   this step makes debt visible across the whole system.

Every design ends with the hand-off list (Output Format) naming the owner
of each routed concern. Live execution — adding an SDK, signing up,
creating flags in a live service, flipping a flag — is never part of this
workflow.

## Output Format

```
FEATURE FLAG SYSTEM DESIGN — <product>
Inventory:     <existing mechanisms, where, who changes them, how fast>;
               routed out: <entitlement/permission "flags" → owner>
Flag store:    CHOSEN <option> — why; REJECTED <main alternative> — why
  Choice guide (only when the owner has not decided):
               terms; per option: why it fits, can/cannot do, pros/cons,
               money / setup / upkeep (unknown where unverified);
               recommendation + the fact that would change it;
               ONE owner question (or the one missing fact, asked first);
               "the answer is a preference and authorizes nothing"
Interface:     internal adapter; typed definitions; key separation;
               client payload = evaluated values only
Evaluation:    per flag class → server | client (presentation only) | edge |
               build time; staleness / latency / flicker cost; rejected placement
Targeting:     attributes + server-side source of truth each; precedence;
               stable-ID bucketing shared with experiments;
               tenant-qualified cache keys
Fail-safe:     code default (= strategist's safe value) | last-known-good /
               bootstrap | timeout <N ms> | cold start | how it is exercised;
               rejected alternative
Kill switch:   streaming | polling, reach bound <N s>; who may flip per
               environment (roles ← authorization-matrix-designer);
               break-glass; local override when the service is down
Audit event:   fields; platform → audit-log-architect
Flag debt:     registry fields; stale-flag report / CI check; code search;
               expiry alert
Hand-offs:     rollout per change → feature-flag-rollout-strategist;
               entitlements → plan-entitlement-architect;
               roles → authorization-matrix-designer;
               experiments → ab-test-designer;
               deploy strategy / pipeline → ci-pipeline-architect (user invokes);
               flag console UI → admin-console-architect;
               audit platform → audit-log-architect;
               live execution → human-approval-boundary
Not decided:   <open owner questions, unverified prices, missing facts>
```

## Validation Checklist

- [ ] The inventory came first, and entitlement or permission "flags"
      were routed out rather than designed as flags.
- [ ] A store choice put to the owner defines terms, gives every viable
      option its fit, capabilities, pros, cons and money / setup / upkeep
      cost (unknown where unverified), recommends one with the fact that
      would change it, and asks exactly one atomic question — or asks only
      for a missing deciding fact first.
- [ ] The design states that the owner's answer grants no authority to
      sign up, pay, add an SDK, or change a live system.
- [ ] Call sites reach flags through one internal interface; no server
      key reaches client code; clients get evaluated values only.
- [ ] Every flag class has an evaluation placement with its staleness,
      latency and flicker cost; tenant- or security-sensitive flags are
      evaluated on the server.
- [ ] Targeting attributes come from server-side sources of truth; every
      per-tenant cached value has a tenant-qualified key.
- [ ] The fail-safe mechanism covers code defaults, last-known-good
      cache, a non-blocking timeout and cold start — and the safe value
      itself is left to `feature-flag-rollout-strategist`.
- [ ] The kill switch has a stated reach bound in seconds, named flip
      authority per environment, and a path that works with the flag
      service down.
- [ ] The audit event and flag-debt hooks are specified, with the audit
      platform and the pipeline wiring handed to their owners.
- [ ] Each major decision states what was chosen, why, and the main
      rejected alternative.

## Gotchas

- The render-blocking SDK: a flag call awaited before first paint turns
  every flag-service blip into a blank page. Evaluation must time out
  into the fallback, never wait on the network.
- The tenant-blind cache: caching an evaluated flag under its name alone
  serves tenant A's override to tenant B. The key is flag + tenant (+ any
  other targeting attribute that changes the answer).
- Client-asserted targeting: reading plan or role from a client-sent
  header or local storage lets any user grant themselves a beta feature.
  Targeting attributes come from the server's identity and tenant record.
- Two bucketing functions: a flag SDK and an experiment SDK that hash
  users differently put the same user in different groups, corrupting
  both the rollout and the experiment readout.
- The kill switch that depends on what it protects: if pulling the
  switch requires the flag service, it fails exactly when the service is
  the problem. Design the local override.
- Config-in-repository flags look free until someone needs to turn a
  feature off at 2 a.m.: every change is a release. Say so plainly when
  teaching the store choice.
- The permanent flag: a flag left on forever for one plan is an
  entitlement with no billing link — it drifts from the plan and billing
  source of truth, and turning it off would remove a paid feature from a
  paying customer. Route it before it hardens.
- Vendor lock-in through call sites: importing a vendor SDK in hundreds
  of files makes the store choice irreversible in practice. The adapter
  keeps it cheap to change.

## Stop Conditions

- Asked to add or upgrade an SDK, sign up for or pay a flag vendor,
  create flags in a live flag service, flip a flag in production, or edit
  configuration or CI files → refuse the execution and explain why: this
  skill designs and writes nothing. Offer the design, and route any live
  change through `human-approval-boundary`; the pipeline itself belongs
  to `ci-pipeline-architect`, which the user invokes by name.
- A store decision is needed and the owner has not made it → do not
  present a store-specific design as final. Teach the choice and ask the
  one question; the store-independent parts (interface, fail-safe,
  targeting, audit event) may proceed.
- A fact that decides the store recommendation is missing (for example
  team size, number of services, whether experiments are planned, or who
  will flip flags) → ask only for that fact first, then continue.
- The "flag" is a permanent plan entitlement ("leave it on for
  Enterprise", "Pro includes this") → refuse to design it as a flag and
  route it to `plan-entitlement-architect`.
- The request is one change's ramp, guardrails, auto-rollback, safe value
  or removal → route to `feature-flag-rollout-strategist`.
- The ask is who may flip flags as a role model → the role definitions
  go to `authorization-matrix-designer`; this skill only states where the
  flag console enforces them.
- An existing flag system appears to leak one tenant's overrides or
  targeting data to another → redesign the flag keying and targeting, but
  do not treat the redesign as proof nothing else leaks; report the
  observed evidence and route a full review to `tenant-isolation-reviewer`.

## Supporting Files

- [references/flag-system-sheet.md](references/flag-system-sheet.md) —
  the store comparison and recommendation patterns (with volatile-cost
  notes), the evaluation-placement table, the fail-safe mechanism
  checklist, kill-switch propagation options, and the audit-event and
  registry field lists.
- `evals/evals.json` — behavior cases: the multi-service system design,
  the render-blocking SDK edge, the tenant-blind override cache, the
  owner flag-store choice (`edge-owner-flag-store-choice`), the
  entitlement-as-flag routing refusal, the install-and-flip refusal, the
  vendor sign-up refusal, and the single-change ramp near miss.
- `evals/trigger-evals.json` — discrimination against
  `feature-flag-rollout-strategist` (system vs one rollout, including the
  fail-safe mechanism-vs-value seam), `plan-entitlement-architect`,
  `authorization-matrix-designer`, `ab-test-designer`,
  `ci-pipeline-architect`, `saas-platform-architect`,
  `tenant-isolation-reviewer`, `caching-strategy-designer` (flag-value
  caching vs general cache design), `authority-invalidation-architect`
  (flag-change propagation vs a revoked access change still honored), and
  `frontend-perf-engineer` (a render-blocking flag SDK vs general page
  performance).
