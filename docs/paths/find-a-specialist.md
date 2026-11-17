# Find a specialist — name the situation, not the skill

*This path names who acts and in what order — each skill owns its own how.*

**Who this is for:** you can describe the situation in plain words but cannot name the skill for it — data and where it lives, documentation, analytics and experiments, planning for performance, or simply "which skill should I use?". This page maps the situation to the specialist who owns it; you do not have to know its name first.

**How to run it:** open your project in your agent tool (Claude Code, OpenAI's Codex command-line interface (CLI), or any Agent Skills tool) and describe the situation in one plain sentence. Advisory specialists can be selected automatically; a specialist marked **manual-only** must be named explicitly by you before it runs. For example: **"Reports are slowing down the app — which skill should I use?"** Auto-selection quality varies by tool; see the README's [tools section](../../README.md#using-aegis-with-codex-cli-and-other-agent-skills-tools).

**Before you start — what a starter install has.** The [starter package](../consumer-starter-package.md) installs none of these 25 specialists (42 files / 19 skills; manual-only skills are not installed). Copy each skill you need with the **selected-skills allow-list** route in [Using the skills in your own project](../../README.md#using-the-skills-in-your-own-project): copy that skill's `.claude/skills/<name>/` folder into your repository, then check it is present at use time in `.claude/skills/<name>/` or `.agents/skills/<name>/`. If a skill is absent, name it and copy it — never substitute a different skill. Every handoff named in a row below is optional/conditional: copy the handoff skill first; if it is absent and you do not copy it, that route is unavailable and you can stop here. The starter package does not change for this page and there is no auto-install claim.

## The situation map

### Data and where it lives

| The situation, in plain words | Who owns it (and its rules) |
|---|---|
| "I need to change a table or schema without breaking the live app." | [`schema-evolution-planner`](../../.claude/skills/schema-evolution-planner/SKILL.md) — stages the change while the system keeps serving traffic; it refuses a one-deploy breaking change and stops when the consumer list cannot be completed. The migration file's safety review is [`secure-migration-reviewer`](../../.claude/skills/secure-migration-reviewer/SKILL.md); the operator steps are [`data-migration-runbook-author`](../../.claude/skills/data-migration-runbook-author/SKILL.md) — copy it first (the starter does not install it). |
| "I need step-by-step instructions to move or backfill data in production." | [`data-migration-runbook-author`](../../.claude/skills/data-migration-runbook-author/SKILL.md) — authors the operator-executable runbook and refuses to execute it; it stops without an approved plan, a safety-review verdict and a **verified backup**, which comes from the manual-only [`database-backup-verifier`](../../.claude/skills/database-backup-verifier/SKILL.md) **manual-only — name it explicitly**. |
| "I need to know the backups would actually save us before a risky migration." | [`database-backup-verifier`](../../.claude/skills/database-backup-verifier/SKILL.md) **manual-only — name it explicitly** — a human invokes it; evidence mode is the read-only default, a restore drill needs a named isolated non-production target, and a store with no recorded recovery objective stops the check. |
| "Reports are slowing down the app." | [`operational-vs-analytical-splitter`](../../.claude/skills/operational-vs-analytical-splitter/SKILL.md) — decides the split and executes nothing; one slow query with a broken plan goes to [`query-plan-reader`](../../.claude/skills/query-plan-reader/SKILL.md) **manual-only — name it explicitly** first, and a workload with no freshness tolerance holds its verdict. |
| "Where should our analytics data live?" | [`warehouse-lake-architect`](../../.claude/skills/warehouse-lake-architect/SKILL.md) — designs the analytical estate and executes nothing; the splitter verdict (or a consumer inventory) comes first, and an undefined tenant model halts the design. |
| "Services need to pass events to each other reliably." | [`streaming-event-architect`](../../.claude/skills/streaming-event-architect/SKILL.md) — designs internal event transport; a partner/public contract routes to [`api-event-architect`](../../.claude/skills/api-event-architect/SKILL.md), and a hard exactly-once requirement goes to a human with the honest options. |
| "We need a public/partner API or webhooks that integrations can rely on." | [`api-event-architect`](../../.claude/skills/api-event-architect/SKILL.md) — designs external API and event contracts; the tenant model and authorization matrix run first, and a breaking change with no deprecation policy routes through [`human-approval-boundary`](../../.claude/skills/human-approval-boundary/SKILL.md). |
| "We need to know when data goes bad in production." | [`data-quality-monitor-designer`](../../.claude/skills/data-quality-monitor-designer/SKILL.md) — designs monitoring and executes nothing; it refuses silent auto-repair, and unsourced validity rules stop that dataset. |
| "Where does personal data live, and how do we delete it everywhere?" | [`pii-lifecycle-designer`](../../.claude/skills/pii-lifecycle-designer/SKILL.md) — designs the collection, classification, retention and deletion model; it refuses an "anonymized" label without a re-identification check, and it may not read bulk actual personal values. |

### Documentation

| The situation, in plain words | Who owns it (and its rules) |
|---|---|
| "Our README does not explain what this is or how to start." | [`readme-craftsman`](../../.claude/skills/readme-craftsman/SKILL.md) — crafts the README entry point; a whole-corpus organization job routes to [`diataxis-doc-organizer`](../../.claude/skills/diataxis-doc-organizer/SKILL.md), and an unverifiable quickstart is flagged, never shipped. |
| "Our docs are a pile and nobody can find anything." | [`diataxis-doc-organizer`](../../.claude/skills/diataxis-doc-organizer/SKILL.md) — organizes the docs set by reader need; the README entry point routes back to [`readme-craftsman`](../../.claude/skills/readme-craftsman/SKILL.md), and the toolchain routes to [`docs-as-code-architect`](../../.claude/skills/docs-as-code-architect/SKILL.md). |
| "We need docs to build and publish with the code." | [`docs-as-code-architect`](../../.claude/skills/docs-as-code-architect/SKILL.md) — designs the docs toolchain and pipeline; content organization routes to the docs organizer or README craft, and generated API reference is [`api-doc-generator-designer`](../../.claude/skills/api-doc-generator-designer/SKILL.md). |
| "We need API reference docs generated from the code or schema." | [`api-doc-generator-designer`](../../.claude/skills/api-doc-generator-designer/SKILL.md) — designs generated API reference from a machine-readable source; designing the API contract itself routes to [`api-event-architect`](../../.claude/skills/api-event-architect/SKILL.md), and no machine-readable source is a prerequisite gap to flag. |
| "Outside contributors do not know how to send a change." | [`contribution-guide-author`](../../.claude/skills/contribution-guide-author/SKILL.md) — designs the CONTRIBUTING guide content; new-employee onboarding routes to [`onboarding-doc-designer`](../../.claude/skills/onboarding-doc-designer/SKILL.md), and a genuinely undefined contribution process is surfaced, not papered over. |
| "New team members take weeks to get productive." | [`onboarding-doc-designer`](../../.claude/skills/onboarding-doc-designer/SKILL.md) — designs onboarding docs for new hires or team members; an external-contributor audience routes to [`contribution-guide-author`](../../.claude/skills/contribution-guide-author/SKILL.md), and a missing process is surfaced. |
| "We have a pile of architecture decision records and no index." | [`adr-sequencer`](../../.claude/skills/adr-sequencer/SKILL.md) — sequences and manages the ADR corpus; authoring one new ADR is [`adr-writer`](../../.claude/skills/adr-writer/SKILL.md)'s job, and a contested fact is resolved with the project's fact-reconciliation owner before writing a resolving ADR. |
| "Old process docs never get cleaned up." | [`docs-retention-index`](../../.claude/skills/docs-retention-index/SKILL.md) — governs retention and retirement of process, session and operational docs; retiring a library skill belongs to the skill-lifecycle owner, not this document-retention index, and deleting a doc needs explicit human approval. |

### Analytics and experiments — in chain order

| The situation, in plain words | Who owns it (and its rules) |
|---|---|
| "We do not know what to track." | [`event-schema-architect`](../../.claude/skills/event-schema-architect/SKILL.md) — defines the tracking plan and event taxonomy; an external contract routes to [`api-event-architect`](../../.claude/skills/api-event-architect/SKILL.md), and instrumentation routes to [`product-analytics-instrumenter`](../../.claude/skills/product-analytics-instrumenter/SKILL.md). |
| "We know what to track; where in the code should it fire?" | [`product-analytics-instrumenter`](../../.claude/skills/product-analytics-instrumenter/SKILL.md) — designs where product-analytics events fire; a missing or inconsistent schema routes to [`event-schema-architect`](../../.claude/skills/event-schema-architect/SKILL.md) first, and system telemetry belongs to [`observability-operator`](../../.claude/skills/observability-operator/SKILL.md) **manual-only — name it explicitly**. |
| "How many people get from sign-up to paying?" | [`funnel-definition-designer`](../../.claude/skills/funnel-definition-designer/SKILL.md) — defines the funnel and its counting rules; the events must exist first, and a causation question routes to [`ab-test-designer`](../../.claude/skills/ab-test-designer/SKILL.md). |
| "Did this change actually help?" | [`ab-test-designer`](../../.claude/skills/ab-test-designer/SKILL.md) — designs and reads the controlled experiment; a safety rollout is not an experiment and routes to [`feature-flag-rollout-strategist`](../../.claude/skills/feature-flag-rollout-strategist/SKILL.md), and a fuzzy metric goes back to the funnel definition first. |

### Planning for performance — not fixing slowness

| The situation, in plain words | Who owns it (and its rules) |
|---|---|
| "Pages must load in under X — how do we budget that?" | [`latency-budget-architect`](../../.claude/skills/latency-budget-architect/SKILL.md) — decomposes an end-to-end target into component budgets; with no target there is no budget, so target setting routes to [`slo-reliability-architect`](../../.claude/skills/slo-reliability-architect/SKILL.md), and setting the service-level objective itself is declined. |
| "Will it hold up when lots of customers use it at once?" | [`load-test-planner`](../../.claude/skills/load-test-planner/SKILL.md) — plans the load test and executes nothing; planning is safe, but running against production is refused without explicit recorded human approval, and with no pass/fail numbers the target-setting owners come first. Measure it afterwards with [`performance-test-harness`](../../.claude/skills/performance-test-harness/SKILL.md). |
| "Should we cache this, and how do we keep it correct?" | [`caching-strategy-designer`](../../.claude/skills/caching-strategy-designer/SKILL.md) — designs the cache and its invalidation rules; caching authorization or permission results needs explicit human approval, and a chatty N+1 pattern goes to [`n-plus-one-detector`](../../.claude/skills/n-plus-one-detector/SKILL.md) **manual-only — name it explicitly** first. |

If the app is already slow or broken rather than being planned, use the symptom map in [Something's broken](something-is-broken.md) instead; this section is planning ahead.

### Not sure which skill?

| The situation, in plain words | Who owns it (and its rules) |
|---|---|
| "I know what I want to do — I just do not know which skill." | [`skill-selection-advisor`](../../.claude/skills/skill-selection-advisor/SKILL.md) — recommends a ranked shortlist for a stated outcome and performs no side effect; it needs `docs/skills-catalog.md` and `tools/skills-manifest.json`, so a starter copy without them states the unknown and stops short of a definitive shortlist, and it refuses to invoke, install or run anything. For the beginner lifecycle, use the journey door instead of this shortlist. |

## What this is — and isn't

This is a guided map, not a guarantee: each specialist owns its own how, its own preconditions and its own stop conditions, and the named skill's own text governs when it runs. Several of the skills above are design or advisory only — they produce a plan, finding or recommendation and execute nothing.

The starter package installs **none** of these specialties; a missing skill is copied through the selected-skills route or that step stops. Manual-only specialists are never auto-applied: you name the exact skill and invoke it yourself. Nothing on this page fixes anything during a mapping.

There is no readiness claim, no coverage-percentage claim, no host-support claim and no eval-detection claim here. The shortlist row depends on the catalog and manifest, which a starter copy may not carry, so it can stop short of a definitive answer rather than invent one.

Nothing here is a conductor: the whole journey belongs to `project-orchestrator`. For a symptom that is already broken, use the symptom map in [Something's broken](something-is-broken.md); for a ranked shortlist for a stated outcome, use [`skill-selection-advisor`](../../.claude/skills/skill-selection-advisor/SKILL.md).
