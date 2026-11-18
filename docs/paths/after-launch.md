# After launch — keep it healthy, learn from incidents, plan what's next

*This path names who acts and in what order — each skill owns its own how.*

**Who this is for:** your product is live and you want to learn from an incident, run a routine health check, plan the next version, or retire a feature, an API or a customer — without knowing which skill to name.

**How to run it:** open your project in your agent tool (Claude Code, OpenAI's Codex command-line interface (CLI), or any Agent Skills tool) and describe the situation in one plain sentence. Advisory specialists can be selected automatically; a specialist marked **manual-only** must be named explicitly by you before it runs — for a starter consumer, a valid trigger-scoped override recorded in the consumer-local register must cover it before use; naming alone is not authorization. Example: **"My app is live — help me do a routine health check and tell me what evidence I need."** Auto-selection quality varies by tool; see the source-only Aegis README's tools section.

**Source-only links.** Links to skills or pages outside the starter package are source-repository links; in a consumer copy they do not resolve — copy the skill first (starter sections 4.1–4.2).

**Before you start — what a starter install has.** The starter package installs none of these 10 specialists (see the source-only starter-package page; manual-only skills are not installed). Copy each skill you need with the **selected-skills allow-list** route in the source-only `README.md` section "Using the skills in your own project": copy that skill's `.claude/skills/<name>/` folder into your repository, then check it is present at use time in `.claude/skills/<name>/`, `.agents/skills/<name>/` or `~/.agents/skills/<name>/`. For a starter consumer, record the extension as a DECISION in `docs/project-state.md` before first use (the starter package's section 4.2 rule). If a skill is absent, name it and copy it — never substitute. Every handoff named in a row below is optional/conditional: copy the handoff skill first; if it is absent and you do not copy it, that route is unavailable and you can stop here. No auto-install claim; the starter package does not change for this page.

## The situation map

### Something is wrong right now

**If the product is broken right now, this page adds no steps.** Use the symptom map in [Something's broken](something-is-broken.md): a live incident, live diagnosis and a live status determination stay with the specialists named there — `systematic-debugger` is **manual-only** as named there, and a live status determination is `observability-operator` (**manual-only**; see Routine health check below) — and this page never diagnoses, reports live health or runs a probe.

### Learn from an incident

| The situation, in plain words | Who owns it (and its rules) |
|---|---|
| "We had an incident; I want the next one handled better and the lessons acted on." | [`incident-response-runbook`](../../.claude/skills/incident-response-runbook/SKILL.md) — designs the postmortem process; it does not write the postmortem itself. A live incident → stop authoring and report it to the human incident owner; root cause stays with [`systematic-debugger`](../../.claude/skills/systematic-debugger/SKILL.md) **manual-only — name it explicitly**. Quote: "An incident is live NOW … stop authoring; report it to the human incident owner." |
| "We have CI history and want the incident's regression tests promoted." | [`regression-suite-curator`](../../.claude/skills/regression-suite-curator/SKILL.md) — **conditional**: applies only when CI history and runtimes are accessible; otherwise reduce scope to the quarantine registry. Quote: "No CI history/runtimes are accessible → … reduce scope to the quarantine registry." |
| "Targets may need revisiting after the incident." | [`slo-reliability-architect`](../../.claude/skills/slo-reliability-architect/SKILL.md) — **conditional**: only when targets need revisiting; with no baseline data, provisional targets only. Quote: "No baseline data exists and none can be gathered → provisional targets only." |
| "An attack was visible in the logs but no alert fired — or the alert fired and no one owned it." | [`security-logging-alerting-architect`](../../.claude/skills/security-logging-alerting-architect/SKILL.md) — **conditional**: only when a threat model or statable attack concerns exist; no incident-response path is surfaced as the blocking gap. Quote: "The organization has no incident-response path at all (no owner, no severity ladder) … surface this as the blocking gap." |

### Routine health check

| The situation, in plain words | Who owns it (and its rules) |
|---|---|
| "Is the live product healthy right now?" | [`production-safe-smoke-tester`](../../.claude/skills/production-safe-smoke-tester/SKILL.md) — designs read-only probes; a person runs them. A live health determination is [`observability-operator`](../../.claude/skills/observability-operator/SKILL.md) **manual-only — name it explicitly**, and live-failure diagnosis is [`systematic-debugger`](../../.claude/skills/systematic-debugger/SKILL.md) **manual-only — name it explicitly**; executing probes is refused. Quote: "The user asks for a live post-deploy health determination … route the live determination to observability-operator (manual-only) and live-failure diagnosis to systematic-debugger." |
| "We need evidence the backups would actually restore before a risky change." | [`database-backup-verifier`](../../.claude/skills/database-backup-verifier/SKILL.md) **manual-only — name it explicitly** — **conditional** on a recorded RPO/RTO; without one it stops and the gap goes to [`resilience-architecture-reviewer`](../../.claude/skills/resilience-architecture-reviewer/SKILL.md). Quote: "A store in scope has no recorded RPO or RTO → stop before judging it and hand the gap to resilience-architecture-reviewer." |
| "We do not have recorded recovery targets, or the disaster-recovery design has never been reviewed." | [`resilience-architecture-reviewer`](../../.claude/skills/resilience-architecture-reviewer/SKILL.md) — **conditional**: only when targets are missing or the DR design needs review; it never lists or restores real backups. Quote: "No RTO or RPO is recorded for a service or store in scope → stop the DR part of the review for it and ask the owner one question." |
| "Security controls may have silently drifted from the recorded baseline." | [`security-drift-detector`](../../.claude/skills/security-drift-detector/SKILL.md) — **conditional**: a recorded baseline and supplied evidence exist; missing evidence is marked UNVERIFIED, never invented. Quote: "Required evidence is unavailable: state what is missing and mark the artifact UNVERIFIED instead of inventing facts." |
| "Is the cloud account configured safely against a baseline?" | [`cloud-security-baseline-reviewer`](../../.claude/skills/cloud-security-baseline-reviewer/SKILL.md) — **conditional**: you supply exports or screenshots; with no evidence it stops and lists the exports needed, and it refuses to run CLI commands or sign in. Quote: "No evidence supplied → stop and list the exports needed for the named baseline." |
| "Staging and production differ; it works in one and fails in the other." | [`environment-parity-reviewer`](../../.claude/skills/environment-parity-reviewer/SKILL.md) — **conditional**: exports for at least two environments exist; it compares by name and presence only and never prints secret values. Quote: "No evidence exists for any environment beyond one → stop; a parity review needs at least two environments." |
| "Bad, stale or missing data keeps reaching users or reports." | [`data-quality-monitor-designer`](../../.claude/skills/data-quality-monitor-designer/SKILL.md) — **conditional**: production data pipelines exist; silent auto-repair is refused. Quote: "Asked to design checks that auto-repair failing data → refuse silent correction." |
| "We have no external probes and learn about outages from customers." | [`synthetic-monitoring-architect`](../../.claude/skills/synthetic-monitoring-architect/SKILL.md) — **conditional**: no external probes exist yet; running probes against production needs human approval and a validated safety contract, and SLO targets come from [`slo-reliability-architect`](../../.claude/skills/slo-reliability-architect/SKILL.md) first. Quote: "Executing probes against production is requested (not just designing them) → STOP." |

### Plan the next version

| The situation, in plain words | Who owns it (and its rules) |
|---|---|
| "What should we build next?" | [`project-orchestrator`](../../.claude/skills/project-orchestrator/SKILL.md) — handoff only: the project's own stage route owns the next slice. This page writes no plan, runs no prioritization frame and names no prioritization skill. |
| "Decisions or bugs exist only in chat and the repo does not record them." | [`chat-backlog-reconciliation`](../../.claude/skills/chat-backlog-reconciliation/SKILL.md) — **optional input**: a chat claim of "done" is refused without evidence; the audit against evidence is the skill. Quote: "Asked to mark items completed from chat claims without evidence … → refuse; the audit against evidence is the skill." |
| "How many people get from sign-up to paying?" | [`funnel-definition-designer`](../../.claude/skills/funnel-definition-designer/SKILL.md) — **optional input**: the events for the steps must exist first. Quote: "The events needed for the steps don't exist". |
| "Did this change actually help?" | [`ab-test-designer`](../../.claude/skills/ab-test-designer/SKILL.md) — **optional input**: the metric must be rigorously defined, and funnel definition comes first when it is not. Quote: "The metric to be tested isn't rigorously defined → route to funnel-definition-designer first." |

### Retire a feature, an API or a customer

| The situation, in plain words | Who owns it (and its rules) |
|---|---|
| "We are going to retire a feature or an API." | [`sunset-deprecation-communicator`](../../.claude/skills/sunset-deprecation-communicator/SKILL.md) — **conditional**: the sunset is already decided; if it is still debated, that is a product/business call and this skill stops. Quote: "The sunset itself is not actually decided (still debating whether to kill it) → stop; the decision is a product/business call." |
| "A customer or tenant is leaving." | [`saas-offboarding-architect`](../../.claude/skills/saas-offboarding-architect/SKILL.md) — designs the exit workflow and refuses execution; missing state/data/policy evidence is reported as UNKNOWN and asked for, not invented. Quote: "The caller wants this skill to implement, provision or execute the design: refuse." |
| "Deletion or retention reaches personal data." | [`pii-lifecycle-designer`](../../.claude/skills/pii-lifecycle-designer/SKILL.md) — **conditional**: deletion or retention applies; an "anonymized" label without a re-identification check is refused. Quote: "Asked to label a dataset 'anonymized' to skip retention/erasure obligations … → refuse the label." |
| "Data must move as part of the change." | [`data-migration-runbook-author`](../../.claude/skills/data-migration-runbook-author/SKILL.md) — **conditional**: data must move; an approved plan, a safety-review verdict and a verified backup are prerequisites. Quote: "No approved plan, no safety-review verdict, or no verified backup → stop; name the missing prerequisite." |
| "The change needs a backout plan." | [`rollback-runbook-author`](../../.claude/skills/rollback-runbook-author/SKILL.md) — **conditional**: the change needs a backout; an irreversible migration stage is a release-blocking finding. Quote: "Asked to execute the rollback now → stop; authoring and executing are different authorities." |

## What this is — and isn't

This is a guided map, not a guarantee. Each specialist owns its own how, its own preconditions and its own stop conditions; several are design or advisory only and execute nothing. **Manual-only** specialists are named explicitly and never auto-applied. The starter package installs none of the 10 specialists above, so a missing skill is copied through the selected-skills route or the step stops — it is never silently substituted.

There is no readiness claim, no coverage-percentage claim, no host-support claim, no eval-detection claim and **no live-health-status claim** here: where evidence is missing the page says **UNKNOWN**, and nothing on this page fixes, probes or diagnoses anything. The after-launch conductor is parked and not built: nothing here is a conductor, and the whole journey stays with `project-orchestrator`.

For a live symptom use [Something's broken](something-is-broken.md); for a single situation outside this page use [Find a specialist](find-a-specialist.md).
