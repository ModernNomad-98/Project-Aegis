# Feature-flag system skill (`feature-flag-architect`): scope proposal

> **Status:** Accepted by the owner 2026-09-26 (chat); implementation in
> progress; this page grants no authority beyond the standing delivery
> approvals ([AEGIS-APR-039](../approvals/APPROVAL_REGISTER.md#aegis-apr-039-reaffirmation-of-ongoing-backlog-delivery-approval)).

Prepared 2026-09-26 from `ModernNomad-98/Project-Aegis` `origin/main` at
`eadf1fd3934ca196b70178681dfb07ef7c264020`. The owner asked for a new
feature-flag skill on 2026-09-26, accepted this scope in chat at about
15:20 Pacific Daylight Time (PDT) the same day, and said to build it now.

This page is for maintainers and reviewers who build or review the new skill,
and for the owner checking that the delivered work matches what was accepted.
It records **what was proposed and accepted**. It is not a delivery record:
nothing below was built, validated or merged when this page was written. The
pull requests (PRs) that deliver the skill will carry their own evidence.

## Terms used on this page

- A **feature flag** is a named switch the running product reads to decide
  whether a piece of behavior is on, and for whom, without shipping new code.
- A **kill switch** is a flag used to turn a feature off quickly when it
  misbehaves.
- **Flag debt** is the growing pile of flags nobody removed after they stopped
  being useful, and the dead code paths they keep alive.
- A **software development kit (SDK)** is the library a product imports to
  talk to a service, here the library that reads flag values.
- **Targeting** decides which tenants (customer accounts), users, plans,
  roles or environments see a flag's "on" value. **Sticky targeting** means
  the same user or tenant keeps getting the same answer from one request to
  the next.
- A **fail-safe** is what the product does when the flag service cannot be
  reached: it falls back to a known safe value instead of failing.
- **General availability (GA)** means a feature is on for everyone. A
  **canary** or percentage ramp turns it on for a small share first.
- A skill is **auto-invocable** when the assistant may choose it on its own
  from its description. A **manual-only** skill runs only when a person names
  it, because it has side effects.
- A **trigger-eval** is a test prompt that checks which skill the assistant
  picks, so that two skills with similar topics do not steal each other's
  requests.
- **ROUTE-002** is a finding in the skill-contract audit
  (`scripts/audit-skill-contracts.py`). It flags a skill that says "do not use
  me for X, use skill B" when skill B never points back.
- A **D-row** is a numbered decision in the
  [reconciliation and decision log](../reconciliation/step-0-reconciliation-v4.md).
  The existing flag skill came from decision D12.5.
- **Checks 1–7** are the seven judgment checks run by the
  [`skill-quality-reviewer`](../../.claude/skills/skill-quality-reviewer/SKILL.md)
  skill: trigger quality, collision with other skills, duplication versus
  extension, evaluation integrity, section substance, scope discipline and
  invocation posture.

## Decision in one read

**Build one new skill, `feature-flag-architect`, that designs the flag
system itself. Do not build a second "rollout by tenant" skill.** Make a small
matching wording edit to the existing
[`feature-flag-rollout-strategist`](../../.claude/skills/feature-flag-rollout-strategist/SKILL.md)
in the same PR. Add the beginner-route change to `project-orchestrator` in a
separate, smaller PR.

| Item | Accepted proposal | State when this page was written |
| --- | --- | --- |
| New skill `feature-flag-architect` | One auto-invocable design skill; writes nothing, installs nothing | Not built |
| Strategist wording edit | Reciprocal exclusion, one Use-When bullet, one Stop Condition hand-off, trigger-eval cases | Not built |
| Orchestrator route | Stage 3 route plus an optional Stage 9 route, in its own PR | Not built |
| Estimate | 2.75–5.5 active hours across both PRs, provisional | Not measured |

## Why a new skill and not an extension

### What already exists

The shipped strategist (decision D12.5, auto-invocable, description 999 of
the 1,024 allowed characters) plans the rollout of **one change**. It
classifies the flag, plans stages (internal, then canary or percentage, then
cohorts, then GA), sets sticky targeting and guardrails with automatic
rollback, requires a kill-switch test before ramping, picks the safe value
**for that flag** if the flag service is down, and schedules the flag's
removal. Its trigger-evals separate it from `plan-entitlement-architect`,
`authorization-matrix-designer` and `ab-test-designer`.

Nothing in the library designs the **flag system**: where flags are stored,
whether to build or buy that store, where the SDK sits, where flags are
evaluated, the targeting data model, the mechanism that makes a fail-safe
actually happen, how fast a kill switch takes effect and who may flip it, the
audit trail of flag changes, and tooling that exposes flag debt. Today
`saas-platform-architect` only lists feature flags as a capability that is
present, partial or missing. `ci-pipeline-architect` only decides whether a
pipeline needs a flag-gated deploy route. `tenant-isolation-reviewer` reviews
flags as one possible cross-tenant leak.

### Extending the strategist was considered and rejected

Arguments for extending: both skills deal with flags, fail-safes, kill
switches, targeting and flag debt, and one skill is less to maintain. Earlier
supply-chain threat additions (the LLM03 and ASI04 risk identifiers) landed
as extensions of `supply-chain-security-reviewer`.

Arguments against, which decided it:

1. **Different jobs at different times.** The strategist runs once per risky
   change, at release time. The new job runs once per system, at design time
   (orchestrator Stage 3), and returns only when the platform changes. A
   merged skill would fail check 6 (scope discipline): it would both pick a
   flag vendor and plan next week's canary.
2. **Different inputs.** The strategist reads one change's blast radius and
   metrics. The new job reads the rendering model (server, client, edge,
   static), service count, latency budget, tenancy model, existing
   configuration and admin screens, and budget.
3. **Only the new job has an owner build choice.** Building or buying the
   flag store costs money, setup time and upkeep, so the standard's rule on
   [explaining build choices to the user](../skill-generation-standard.md#explaining-build-choices-to-the-user)
   applies. Adding that choice to the strategist would change its posture and
   its test surface.
4. **No description space left.** At 999 of 1,024 characters, an extension
   would force a rewrite that drops trigger phrases, which risks unseen
   routing regressions.
5. **The precedent does not fit.** The supply-chain extensions added a new
   threat class to the same review job. This would add a new job.

### Where the two skills meet

Each row becomes a pair of trigger-evals, one in each direction.

| Topic | Strategist (one change) | New skill (whole system) |
| --- | --- | --- |
| Fail-safe | Picks the safe **value** for this flag, usually the old behavior | Designs the **mechanism** that delivers it: code defaults, last-known-good cache, bootstrap values, evaluation timeout, start-up with no cache |
| Kill switch | Decides one is needed, with its test and evidence | Designs how a flip reaches every running instance (streaming or polling, with a time bound), who may flip, and the audit record |
| Targeting | Chooses segments and order for this ramp; sticky by a stable ID | Designs the evaluation context (tenant, plan, role, cohort, environment, region), where each attribute comes from, and tenant-safe caching of per-tenant overrides |
| Flag debt | Owner and removal trigger for this flag; deletes the flag and dead code | Builds the hooks: a registry with owner and expiry, a stale-flag report or check, code-reference search |

### One skill, not two roadmap skills

The roadmap lists two related entries:

- [Software architecture roadmap](../skills/01-software-architecture-engineering.md)
  row #27, "Feature Flag Architecture": design safe rollout, kill switches,
  experiments, tenant scopes and phased migrations.
- [SaaS platform roadmap](../skills/02-saas-platform-architecture.md)
  row #65, "Feature Flag Rollout by Tenant": roll out capabilities by tenant,
  role, plan, cohort, environment or kill switch.

Split by who already owns each part:

- #27: safe rollout belongs to the strategist; experiments to
  `ab-test-designer`; phased migrations to `schema-evolution-planner` and
  `rollback-runbook-author`. Kill switches and tenant scopes **as system
  capabilities** go to the new skill.
- #65: rolling out one capability by tenant or cohort belongs to the
  strategist. The **model** that makes targeting by tenant, role, plan, cohort
  or environment possible goes to the new skill.

What remains is one coherent job. A separate "rollout by tenant" skill would
collide with the strategist on the ramp, with the new skill on the targeting
model, and with `plan-entitlement-architect` on "by plan". That fails check 2
(collision).

### Name

`feature-flag-architect` matches the roadmap's "Feature Flag Architecture",
and `-architect` is the library's suffix for system-design skills (for
example `plan-entitlement-architect` and `audit-log-architect`).
`feature-flag-platform-architect` was rejected: it is longer and "platform"
is easily confused with `saas-platform-architect`. The shared `feature-flag-`
prefix with the strategist is deliberate. It helps discovery, the suffixes
state which job each does, and the pair is pinned in both directions.

## Draft descriptions

The description is the text the assistant reads when choosing a skill. Both
drafts below are one line of strict YAML, single-quoted so an apostrophe can
be doubled, as elsewhere in the library. Lengths were measured with Python's
`yaml.safe_load` on the proposal draft; recheck them when building.

**New skill, 990 characters (limit 1,024).** The first 92 or so characters,
which is all some assistants read when selecting, say what it does.

```yaml
description: 'Design the feature-flag SYSTEM a product runs on — flag store build-vs-buy (an owner choice, taught with costs), SDK and config placement, where flags evaluate (server per request, client, edge, build time), the targeting context (tenant, plan, role, cohort, environment) with tenant-safe caching, the fail-safe mechanism when the flag service is down (code defaults, last-known-good cache, timeouts), kill-switch propagation and who may flip it, a flag-change audit trail, and flag-debt hooks (owner/expiry registry, stale-flag report). Designs; writes nothing. Use when choosing or building a flag service, wiring flags into a codebase, or when flags evaluate inconsistently across surfaces or tenants. Do NOT use for one change''s staged rollout, guardrails or flag removal (feature-flag-rollout-strategist), plan entitlements (plan-entitlement-architect), role permissions (authorization-matrix-designer), experiment design (ab-test-designer), or deploy strategy (ci-pipeline-architect).'
```

**Strategist replacement, 943 characters.** ROUTE-002 would report the new
skill's exclusion toward the strategist unless the strategist names it back.
The only change is that one redundant sentence about entitlements and
experiments becomes a short one, and the new exclusion is added. Every
existing "Use when" phrase and "Do NOT use" neighbor stays.

```yaml
description: 'Design the ROLLOUT STRATEGY for a change behind a flag — classify the flag by purpose (release, ops/kill-switch, experiment, permission — release flags stay separate from permanent entitlements), plan progressive delivery (internal → canary/% → cohorts → GA), define sticky targeting, set guardrail metrics with auto-rollback criteria and a pre-ramp kill-switch test gate, choose the fail-safe default when the flag service is down, and manage the lifecycle so release flags are removed after GA (flag debt). Owns HOW one change is de-risked, on whatever flag system exists. Use when planning a staged rollout, a canary or percentage ramp, a kill switch, or flag cleanup. Do NOT use to design the flag system itself — store, SDK, evaluation, change audit (feature-flag-architect) — model plan/feature entitlements (plan-entitlement-architect), role permissions (authorization-matrix-designer), or design/analyze an A/B test (ab-test-designer).'
```

The strategist also gains one Use-When bullet, one Stop Condition hand-off
and reverse trigger-eval cases. Check 1 (trigger quality) passed on the draft:
it names situations and near-misses, and its symptom trigger ("flags evaluate
inconsistently") follows the `authority-invalidation-architect` pattern of
matching a bug report as well as a design request.

## What the skill designs

The workflow has about nine steps:

1. **Inventory.** Find existing flags: environment variables, config files,
   hard-coded tenant checks, database toggles and vendor SDKs. Record the
   rendering model, service count, tenancy model and latency budget, reusing
   output from `tenant-modeler`, `saas-platform-architect` or
   `latency-budget-architect` when it exists. Route flags that really grant
   plan features or permissions to their owners now.
2. **Flag store: build or buy, an owner choice.** Options: flags in the
   repository's config (changes need a release), a flag table in the product's
   own database with an admin screen, a self-hosted open-source flag service,
   or a hosted vendor. Teach, recommend one and ask exactly one question (see
   [Owner choice](#owner-choice)). Vendor names live in the skill's
   `references/` folder, marked volatile, with prices to verify.
3. **SDK and config placement.** One internal flag interface wraps the chosen
   store, so application code never imports the vendor directly. Each flag
   has a typed definition and a registry entry. Server keys stay on the
   server; the browser receives only the flags it needs.
4. **Where flags evaluate.** Per request on the server (the default for
   anything security- or tenant-sensitive), on the client (screen changes
   only, never the only enforcement), at the edge, or at build time (static
   sites; changes need a rebuild). State the staleness, latency and flicker
   cost of each and pick one per kind of flag. This is internal mechanics:
   the skill decides and explains; the owner is not asked.
5. **Targeting context.** Which attributes exist, where each is read from
   (identity or the tenant record, never the client's own claim), the order
   of precedence (kill switch, then per-tenant override, then rule, then
   default), and cache keys that include the tenant. Plan-based targeting
   reads the entitlement system rather than copying it.
6. **Fail-safe mechanism.** A code default at every call site, a
   last-known-good cache or start-up snapshot, an evaluation timeout that
   never blocks a request or page, and defined behavior when starting with no
   cache. The safe value per flag comes from the strategist.
7. **Kill-switch wiring.** How a flip reaches every instance, with a stated
   upper bound in seconds; who may flip in each environment (roles defined by
   `authorization-matrix-designer`); an off-hours emergency path; and a local
   override that works when the flag service itself is down.
8. **Audit of flag changes.** Every create, flip, rule edit and delete records
   who, which flag, which environment, before and after, reason and time. The
   audit store itself belongs to `audit-log-architect`.
9. **Flag-debt hooks.** Registry fields (owner, type, created date, expiry or
   review date), a stale-flag report or non-blocking check, code-reference
   search and an alert on an expired release flag. Removing a given flag is
   the strategist's job.

The output states what was chosen, why, and the main rejected alternative
for the store, evaluation placement, fail-safe and kill-switch path, plus a
hand-off list.

### Hand-offs

| Concern | Goes to |
| --- | --- |
| One change's stages, guardrails, auto-rollback, safe value, removal plan | `feature-flag-rollout-strategist` |
| What a plan includes, limits, quotas; "flag permanently on for Pro" | `plan-entitlement-architect` |
| Which roles may do what, including who may flip flags | `authorization-matrix-designer` |
| Experiment hypothesis, sample size, readout | `ab-test-designer` |
| Deploy strategy and pipeline gates | `ci-pipeline-architect` (manual-only; the user invokes it by name) |
| Where the flag service sits among platform capabilities | `saas-platform-architect` |
| Audit store, retention, integrity | `audit-log-architect` |
| Flag screen inside the admin console, emergency elevation | `admin-console-architect` |
| General caching beyond flag evaluation | `caching-strategy-designer` |
| Reviewing an existing flag system for cross-tenant leaks | `tenant-isolation-reviewer` |
| Recording the store choice as a decision | `adr-writer` |

### What it refuses

The skill refuses to install an SDK, sign up for or pay a vendor, create
flags in a live service, flip a production flag, or edit config or
continuous integration (CI) files. It designs; any live change follows
`human-approval-boundary`. It also refuses to model a permanent plan feature
as a flag and routes that request to `plan-entitlement-architect`.

## Invocation posture

The skill is **auto-invocable**; it does not set `disable-model-invocation`.
Under [section 5 of the standard](../skill-generation-standard.md#5-least-privilege--side-effects),
a skill that only reads and reports needs neither the manual-only marker nor
wider tool permissions. This skill reads the repository and answers in the
conversation. It writes no files, runs no state-changing command, makes no
network call, spends nothing and deploys nothing. It sets no `allowed-tools`
field. If the owner wants the design saved, that goes through `adr-writer` or
the standard's documentation exception, with its own approval of the shown
content. No execution route is proposed. A later revision that added "then
wire the SDK" would make it side-effecting and manual-only, so its Stop
Conditions state that execution is refused. Its neighbors (the strategist,
`plan-entitlement-architect`, `caching-strategy-designer` and
`audit-log-architect`) are also auto-invocable design skills.

## Owner choice

### Required: where flags live

Workflow step 2 teaches before it asks. Draft wording:

> If the owner must choose where flags live, teach it before asking. In plain
> language, define: flags in the repository's config (on/off changes need a
> new release), a small flag table in your own database with an admin screen,
> a self-hosted open-source flag service, and a hosted flag vendor. For each
> viable option give: why it could fit this product, what it can and cannot
> do (runtime and per-customer switches, instant off, audit, experiments), and
> its money, setup-time and upkeep cost. Mark vendor pricing as volatile or
> unknown and verify it when exact prices matter. Recommend the simplest
> option that meets the recorded need, say why and what fact would change the
> recommendation, and ask exactly one owner question. Choosing a vendor is a
> preference, not approval: signing up, installing or paying still needs
> explicit human approval, and this skill does none of it.

Typical recommendation logic, for the skill's reference sheet: one app, one
team and no experiments suggests an own-database table plus code defaults.
Several services or teams, experiments, or non-engineers flipping flags
suggests a self-hosted service or vendor. A static site alone suggests
build-time config, with its limits stated.

### Optional: who may flip production flags

Asked only when evidence calls for it. Whether only engineers, on-call staff
or support staff may flip flags is a business question. The skill explains
the risk and audit trade-off; `authorization-matrix-designer` defines the
roles.

### Planned evaluation cases

One behavior test (in the skill's `evals/evals.json`) covers the owner
choice. A two-person team with one Next.js app and about 40 business
customers wants early access for a few customers and a fast off switch, and
lists the four store options without checked vendor prices. The expected
answer defines the four options, says config flags need a release to change,
gives fit, limits and cost for each while marking vendor pricing unknown,
recommends one option with the fact that would change it, asks one owner
question, installs and signs up for nothing, and leaves the ramp plan to the
strategist.

Other planned cases: a multi-service product needing a flag system; an SDK
that blocks page render for three seconds when the flag service is down; a
near miss that belongs to the strategist ("ramp the billing page from 1% to
GA"); a refusal ("add the vendor SDK and turn the flag on in production");
and a permanent Enterprise-plan flag that routes to
`plan-entitlement-architect`.

## Trigger-eval seams

The new skill lists these neighbors as overlaps:
`feature-flag-rollout-strategist`, `plan-entitlement-architect`,
`authorization-matrix-designer`, `ab-test-designer`, `ci-pipeline-architect`,
`saas-platform-architect` and `tenant-isolation-reviewer`. Planned pairs:

| # | Neighbor | Direction | Prompt sketch | Expected skill |
| --- | --- | --- | --- | --- |
| 1 | Strategist | Forward | Build or buy a flag store, where flags evaluate, what happens when it is unreachable | New skill |
| 2 | Strategist | Reverse | Ramp the billing page from 1% to GA with auto-rollback and a flag deletion date | Strategist |
| 3 | Strategist | Hard edge (mechanism) | Flag SDK blocks page render for three seconds when the service is down | New skill |
| 4 | Strategist | Hard edge (value) | Should the checkout flag fall back to old or new checkout when the service is down? | Strategist |
| 5 | Plan entitlements | Forward | Early access for specific enterprise tenants through per-tenant overrides until GA | New skill |
| 6 | Plan entitlements | Reverse (hard) | Single sign-on should be permanently part of the Pro plan; a flag turns it on per account today | `plan-entitlement-architect` |
| 7 | Authorization | Forward | Only on-call engineers can toggle production kill switches, and every toggle is recorded | New skill (uses authorization for role definitions) |
| 8 | Authorization | Reverse | Which roles can view, edit and export tenant data, deny by default | `authorization-matrix-designer` |
| 9 | Experiments | Forward | Experiments and flags use two SDKs that assign users differently; unify evaluation | New skill |
| 10 | Experiments | Reverse | Sample size and duration to detect a 2% lift | `ab-test-designer` |
| 11 | CI pipeline | Forward | Static marketing site plus app: flags at build time or fetched at runtime? | New skill |
| 12 | CI pipeline | Reverse | Add a canary deploy stage with automatic abort and a named-human promotion gate | `ci-pipeline-architect` |
| 13 | SaaS platform | Reverse | What belongs in the control plane versus the data plane? | `saas-platform-architect` |
| 14 | Tenant isolation | Reverse | Review existing flag overrides and SDK payloads for cross-tenant leakage | `tenant-isolation-reviewer` |

The strategist's own trigger-evals gain cases 1 and 2 and list the new skill
as an overlap. Deliberately not pinned: `edge-state-ux-designer` (client
flicker is handled in the evaluation-placement step, and its triggers do not
contest flag requests), `caching-strategy-designer` and `audit-log-architect`
(composition hand-offs, not competing triggers).

## Orchestrator route: a separate PR

`project-orchestrator` is the beginner entry point, and its changes get their
own review, so this route ships in a second, smaller PR.

**Where:** Stage 3, "Design how it's built", as a route taken when evidence
calls for it, next to `saas-platform-architect`. The evidence is the product
spec's rollout intent (which `product-spec-writer` already captures) or the
owner's answer to the question below. Not Stage 2, whose exit gate is four
fixed owner rows; not Stage 8, by which time the code would already need the
flag interface.

**The one question**, asked only when the spec does not already answer it,
the product has more than a handful of users or customers, and the Stage 3
discussion reaches it, after a plain explanation and a recommendation:

> "When you add a new feature later, do you want to be able to turn it on for
> a few customers first — and switch it off within minutes without releasing
> new code — or is turning each feature on for everyone at once good enough?"

- "A few first / switch off fast" routes to `feature-flag-architect`, which
  asks its own store question on a later turn: one decision per turn.
- "Everyone at once" records the decision with what it was chosen over. No
  route.

The PR changes about 6–10 lines plus one test:

1. A Stage 3 route to `feature-flag-architect` on evidence of a need to
   release to some customers first or switch a feature off without a release.
2. A recommended Stage 9 route to `feature-flag-rollout-strategist` on
   evidence of a risky change, which the owner could strike. The orchestrator
   routes to no flag or rollout skill today.
3. One test: a Stage 3 project whose spec says "early access for pilot
   customers". The orchestrator routes to `feature-flag-architect` by name,
   asks no store question itself and records nothing without its recording
   gate.

## Estimate and review path

All estimates are **provisional**. Active hours count only active work,
excluding review waits, CI queue time and owner waiting. Wall time is
reported separately and never converted.

| Work item | Active hours (provisional) |
| --- | ---: |
| PR 1: new skill (entry file of about 250–320 lines, a reference sheet, 6–7 behavior tests, 14 trigger-evals, catalog and README rows, skill count 185 to 186, decision-log row) | 2–4 |
| PR 1 add-on: strategist description, Use-When bullet, Stop Condition hand-off, 2 trigger-evals | 0.25–0.5 |
| PR 2: orchestrator Stage 3 route, optional Stage 9 route, 1 test | 0.5–1 |
| **Total** | **2.75–5.5, provisional** |

This work sits **outside** the bounded selected planning subtotal (75–154
active hours) in the [backlog forecast](aegis-backlog-forecast.md), like other
skill-maintenance lines, unless the owner selects it into that subtotal.

**Review path for PR 1:**

1. `python scripts/validate-skills.py`: structure, lengths, required
   sections, test files, catalog and README registration, and the new skill
   count. A pass is the entry ticket, not proof of quality.
2. `skill-quality-reviewer` checks 1–7 on the new skill in a fresh session,
   plus check 2 again on the edited strategist.
3. Reciprocity census: run `python scripts/audit-skill-contracts.py` and
   compare ROUTE-002 findings before and after. Expected: the new skill and
   the strategist point at each other. The four one-way exclusions toward
   `plan-entitlement-architect`, `authorization-matrix-designer`,
   `ab-test-designer` and `ci-pipeline-architect` remain as census data,
   because those are widely referenced hub skills that cannot name everyone.
   The frozen audit baseline is not regenerated, and the audit script is a
   protected path that this work does not touch.
4. `library-diff-reviewer` on the whole PR: CI on the exact head, catalog
   integrity and the decision-log row.
5. The owner merges, as the accepted proposal states for both PRs.

**Review path for PR 2:** the validator, a `skill-quality-reviewer` spot
re-review of `project-orchestrator` (checks 2 and 5), `library-diff-reviewer`,
then the owner merges.

**Verify at build time:** the catalog section (proposed: the SaaS
architecture table beside `plan-entitlement-architect`, with a cross-reference
in the D12.5 paragraph), the README family row (the family count should stay
at 23), and the next free decision number (D60 was the highest seen on
`main`).

## What this page does not do

Acceptance of this proposal and this page are not a new grant. Delivery of
the two PRs relies on the standing delivery approvals in
[AEGIS-APR-039](../approvals/APPROVAL_REGISTER.md#aegis-apr-039-reaffirmation-of-ongoing-backlog-delivery-approval)
and the conditions they carry, including passing checks on the exact head.
This page does not waive a protected `gate-guard` check, authorize a change
to `scripts/audit-skill-contracts.py` or its frozen baseline, or permit any
install, vendor sign-up, spending, live flag change or deployment.

Not inspected when the proposal was written: any branch-local backlog wording
for this item (no feature-flag backlog row existed on `main`; only roadmap
rows #27 and #65), the orchestrator's stage-gate map in
`ai-sdlc-operating-model` (a route is not a gate, so no edit is expected;
confirm at build), the neighbors' reference files and the quality-review
checklist. The validator and contract audit were not run for the proposal.
