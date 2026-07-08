---
name: sunset-deprecation-communicator
description: Plan and communicate the sunset or deprecation of a PRODUCT feature or public API to the USERS and integrators who depend on it — establish the (already-made) decision's rationale, assess impact (who uses it, what breaks), define the migration path to the replacement, set a timeline with a deprecation window and a firm sunset date, and build the multi-channel escalating communication plan (announcement, in-app, docs, reminder emails; for APIs deprecation/sunset headers + changelog), plus grandfathering and transition support. The center of gravity is USER communication and migration. This is NOT the retirement of a library SKILL (mark→redirect→remove, reverse-link sweep, catalog rows) — that is skill-deprecation-planner. Use when sunsetting a feature, deprecating an API version/endpoint, or announcing an end-of-life to customers. Do NOT use to retire a skill in THIS library (skill-deprecation-planner) or set the standing API deprecation POLICY (api-event-architect).
---

# Sunset & Deprecation Communicator

## Purpose

Killing a feature is easy; killing it without burning the users who
depend on it is the actual work. The failure modes are familiar: a
silent removal that greets integrators with a 404 on Monday morning, a
"deprecated" banner nobody reads followed by a sunset with no migration
path, or a public API version pulled on a date that was mentioned once in
a changelog. This skill plans the humane sunset: the rationale users will
be told, an honest impact assessment of who breaks and how badly, a
concrete migration path to the replacement, a timeline with a real
deprecation window and a firm date, and a multi-channel, escalating
communication plan that reaches people before it's too late — plus
grandfathering and support for the hardest-hit. Its center of gravity is
COMMUNICATION and MIGRATION for external users. It is deliberately not
`skill-deprecation-planner`, which retires an internal library skill.

## Use When

- Use when: sunsetting or deprecating a product FEATURE and its users
  need a migration path and warning.
- Use when: deprecating a public API version, endpoint, or field that
  integrators depend on, with a compatibility/sunset window.
- Use when: announcing an end-of-life to customers and you need the
  timeline, channels, and messaging planned.
- Use when: a heavy-usage or contractual customer needs grandfathering,
  exceptions, or extended-support handling during a sunset.
- Do NOT use when: the thing being retired is a SKILL in this library —
  the mark→redirect→remove lifecycle, the reverse-link sweep across
  neighbor descriptions/trigger-evals, and the catalog/README rows are
  `skill-deprecation-planner`. Different object (a library skill, not a
  product feature), different work (registration mechanics, not user
  comms).
- Do NOT use when: the task is the STANDING deprecation POLICY — how long
  API versions are supported by default, sunset-header conventions,
  versioning rules — that is `api-event-architect`; this skill executes a
  specific sunset within that policy.
- Do NOT use when: the task is building the notification delivery SYSTEM
  (preference center, channels, in-app notification center) — that is
  `notification-webhook-ux-designer`; this skill plans the sunset MESSAGING
  that rides on it.

## Inputs to Inspect

1. The decision and its rationale: what is being sunset and WHY (low
   usage, replaced, cost, security, strategy) — confirmed as decided;
   this skill communicates it, it does not make the call.
2. The dependency map: who uses the feature/endpoint — segments,
   integrators, volume, revenue, and any contractual commitments naming
   it.
3. The replacement: the alternative users should move to, whether it's at
   parity, and how hard the migration is (from `api-event-architect` /
   `schema-evolution-planner` outputs where relevant).
4. The standing deprecation policy: default support windows, sunset-header
   conventions, and changelog practices this sunset must follow
   (`api-event-architect`).
5. The available communication channels and their reach:
   announcement/blog, in-app, docs, email, and (for APIs) response
   headers — the delivery system owned by `notification-webhook-ux-designer`.

## Workflow

1. **Anchor the rationale and confirm it's decided.** Capture WHY in
   terms users will accept. If the sunset itself is still in question,
   stop — deciding it is a product call, not this skill's; this skill
   plans the communication of a made decision.
2. **Assess impact honestly.** Who depends on it, how many, how heavily,
   and what breaks for them. Identify the hardest-hit (deep integrations,
   contractual users) — they drive the window length and the outreach
   plan. No replacement at parity is itself a finding to surface, not
   hide.
3. **Define the migration path.** The concrete alternative and a
   migration guide with effort estimate; automated migration or tooling
   where feasible. If there is genuinely no replacement, say so plainly
   and give users the honest options.
4. **Set the timeline.** Announcement → deprecation period (still works,
   discouraged, warnings emitted) → firm sunset date (removed). Length
   proportional to impact and migration effort, and at least the standing
   policy's minimum. Dates are firm and stated once, everywhere the same.
5. **Build the escalating communication plan.** Multi-channel and
   repeated, not a single post: initial announcement (changelog/blog/
   email), in-app notices, docs marked deprecated with the migration
   link, reminder emails escalating as the date nears, and targeted
   outreach to heavy/contractual users. For APIs: `Deprecation`/`Sunset`
   response headers, versioned docs, and changelog entries. Each message
   says what, why, when, what to do, and where to get help.
6. **Plan grandfathering, exceptions, and support.** Who (if anyone) gets
   an extension or extended support, the escalation path for stuck users,
   and readiness of support/success teams for the transition wave.
7. **Design the post-sunset behavior.** The removal, and a clear
   tombstone — an explanatory error/redirect pointing to the replacement,
   never a silent 404 — plus monitoring for stragglers still calling the
   dead surface.
8. **Name boundaries and deliver.** Standing policy/versioning →
   `api-event-architect`; the notification delivery system →
   `notification-webhook-ux-designer`; a LIBRARY skill's retirement →
   `skill-deprecation-planner`. Produce the sunset plan in the Output
   Format.

The impact-assessment checklist, window-length guidance, the escalating-
comms schedule, and API deprecation-header conventions:
[references/sunset-comms-sheet.md](references/sunset-comms-sheet.md).

## Output Format

```
SUNSET PLAN — <feature / API surface>
Rationale:     <why, in user-acceptable terms; confirmed decided>
Impact:        <who depends, volume, revenue, contractual; hardest-hit named>
Migration:     <replacement + guide + effort; tooling; "no parity" stated if true>
Timeline:      announce <date> → deprecation window <len> → SUNSET <firm date>
Comms plan:    channels × schedule (announcement, in-app, docs, escalating email,
               targeted outreach; API: Deprecation/Sunset headers + changelog)
Message content: what / why / when / what-to-do / where-to-get-help
Grandfathering: exceptions, extended support, escalation path
Post-sunset:   tombstone (explanatory error/redirect → replacement, NOT silent 404);
               straggler monitoring
Boundaries:    policy/versioning → api-event-architect; delivery system →
               notification-webhook-ux-designer; SKILL retirement → skill-deprecation-planner
```

## Validation Checklist

- [ ] The rationale is captured and the decision confirmed made — this
      skill communicates, it doesn't decide the sunset.
- [ ] Impact names who breaks, how badly, and the hardest-hit
      (contractual/deep-integration) users.
- [ ] A concrete migration path exists, or the lack of a parity
      replacement is stated plainly.
- [ ] The timeline has a real deprecation window and a firm sunset date
      meeting at least the standing policy minimum.
- [ ] Communication is multi-channel and ESCALATING, not a single notice;
      each message covers what/why/when/what-to-do/help.
- [ ] Grandfathering/exceptions and a support/escalation path are defined.
- [ ] Post-sunset leaves an explanatory tombstone, not a silent 404, and
      monitors stragglers.
- [ ] Standing policy, the delivery system, and library-skill retirement
      are handed to their owning skills.

## Gotchas

- A deprecation banner is not a communication plan. People don't read
  banners; they hit the wall on sunset day. Escalating, multi-channel,
  and targeted-to-heavy-users is what actually reaches them.
- Sunsetting without a migration path is an eviction. If there's no
  replacement at parity, that's a decision to reconsider or to state
  honestly — not something to paper over with a cheerful announcement.
- A silent 404 on sunset day tells the integrator nothing; a tombstone
  that says "this was retired on X, use Y" turns a mystery outage into a
  guided migration. Design the after-state.
- Moving the sunset date because users weren't ready teaches everyone the
  date is negotiable, and the next deprecation is ignored. Set a window
  long enough to be firm, then hold it (with grandfathering as the
  pressure valve, not date-slipping).
- The heaviest users are the quietest until it breaks — they've automated
  around your feature. Targeted outreach to top consumers beats hoping
  they saw the blog post.
- This is not retiring a library skill. If the object is a skill in
  `.claude/skills/` with neighbor trigger-evals and catalog rows, the
  reverse-link sweep and mark→redirect→remove lifecycle are
  `skill-deprecation-planner`'s — a completely different mechanism.

## Stop Conditions

- The object being retired is a LIBRARY SKILL (its lifecycle, reverse-
  link sweep, catalog/README rows) → route to `skill-deprecation-planner`;
  this skill handles product features and APIs for external users.
- The sunset itself is not actually decided (still debating whether to
  kill it) → stop; the decision is a product/business call. This skill
  communicates a made decision, it doesn't make it.
- There is no replacement at parity and users have no viable path off the
  feature → surface this to a human as a reason to reconsider the sunset
  or its timing, not to communicate around.
- A contractual commitment names the feature/endpoint being sunset →
  halt and route to the commitment owner; sunsetting contracted
  functionality is a legal/commercial decision, not a comms plan.

## Supporting Files

- [references/sunset-comms-sheet.md](references/sunset-comms-sheet.md) —
  the impact-assessment checklist, window-length guidance by impact, the
  escalating-communication schedule, and API `Deprecation`/`Sunset`
  header conventions.
- `evals/evals.json` — behavior cases including the API-version sunset,
  the no-migration-path refusal, and the escalating-comms plan.
- `evals/trigger-evals.json` — discrimination against `skill-deprecation-planner`
  (THE seam: product feature vs library skill), `api-event-architect`
  (standing policy), and `notification-webhook-ux-designer` (delivery system).
