# Phase 6 cloud, DevOps and reliability skill batch: scope proposal

> **Status:** Proposal only, waiting for an owner decision. This page grants no
> authority and builds nothing. No skill, evaluation file, catalog row or
> decision-log row was created or changed by the pull request that adds it.

Prepared 2026-09-28 from `ModernNomad-98/Project-Aegis` `origin/main` at
`80d9dfe7`, where the validator reported 186 valid skills.

This page is for the owner, who decides whether and how to build the five
remaining Phase 6 expansion candidates, and for the maintainers and reviewers
who would build them. It follows the
[feature-flag skill proposal](feature-flag-architect-skill-proposal.md) and the
quality assurance (QA) Tier 1 batch proposal in pull request #492 (merged as `e0f1d244`): it
records scope, boundaries and an estimate, and builds nothing.

## Terms used on this page

- **DevOps** means development and operations practices: building, deploying
  and running software. **Continuous integration (CI)** is the automated
  build-and-test run on each change.
- **Infrastructure as code (IaC)** is cloud setup written as files (for
  example Terraform or Bicep) instead of clicked together in a web console.
- **Amazon Web Services (AWS)**, **Microsoft Azure** and **Google Cloud
  Platform (GCP)** are the large cloud providers; **managed platforms** such as
  Vercel and Supabase host an app or database without the team running
  servers.
- **Disaster recovery (DR)** is getting a service back after a major loss.
  The **recovery time objective (RTO)** is how long the service may be down;
  the **recovery point objective (RPO)** is how much recent data may be lost.
- A **service level objective (SLO)** is a reliability target, such as "99.9%
  of checkouts succeed each month".
- **Data definition language (DDL)** is the database commands that change
  table structure. **Change data capture (CDC)** copies database changes as
  they happen.
- **Phase 6** is the cloud, DevOps, reliability and release group of the
  library. Its ten first-pass skills shipped; the five candidates here are its
  **expansion backlog**, listed in the
  [skills catalog, Phase 6 backlog](../skills-catalog.md#phase-6--cloud-devops-reliability--release-p1)
  and the
  [reconciliation log, section 3](../reconciliation/step-0-reconciliation-v4.md#phase-6--cloud-devops-reliability--release-p1).
  A **D-number** (for example D70) is a numbered entry in that log's
  [recorded decisions](../reconciliation/step-0-reconciliation-v4.md#5-recorded-decisions).
- A **skill** is a folder under `.claude/skills/` whose `SKILL.md` tells an artificial intelligence (AI)
  assistant how to do one job. Its **description** is the text the assistant
  reads when choosing a skill; the library caps it at 1,024 characters.
- A **manual-only** skill carries `disable-model-invocation: true`, so the
  assistant never picks it on its own; a person must name it. The
  [skill generation standard, section 5](../skill-generation-standard.md#5-least-privilege--side-effects)
  requires this for any skill that writes, calls a network, deploys or spends.
  A skill that only reads and reports stays **auto-invocable**.
- An **extension** adds a scoped piece of work to an existing skill instead of
  creating a new one.
- **Behavior evals** (`evals/evals.json`) describe prompts and the behavior a
  skill should show. **Trigger evals** (`evals/trigger-evals.json`) check that
  the right skill, and not a neighbor, is chosen for a prompt.
- **ROUTE-002** is a census finding from `scripts/audit-skill-contracts.py`:
  skill A's description says "Do NOT use for X (skill B)", but skill B's
  description never names A. It is information, not a failure; widely used
  "hub" skills cannot name every skill that points at them. To
  **reciprocate** is to add the reverse "Do NOT use" pointer to B's
  description; to **leave it one-way (census)** is to keep the finding as
  recorded census data and edit nothing.
- **Active hours** count only hands-on agent work, excluding review waits, CI
  queue time and time waiting for the owner. They are agent estimates, not
  measurements.

## Decision in one read

Checking each candidate against the 186 shipped skills shows four real gaps
and one candidate that fits best as an extension. None is fully covered today.

| Candidate (roadmap source) | Recommendation | Manual-only? | Active hours (provisional) |
| --- | --- | --- | ---: |
| `cloud-security-baseline-reviewer` (execution-plan extra) | **BUILD** | No, it reads only the evidence it is given | 3–5 |
| `resilience-architecture-reviewer` (execution-plan extra) | **BUILD** | No, review only | 3–4.5 |
| `migration-deployment-runbook` (#254) | **MERGE** into `data-migration-runbook-author` as an extension | not applicable (base stays auto-invocable) | 1–2 |
| `environment-parity-reviewer` (#244, with #246) | **BUILD** (lowest priority; the one to defer if needed) | No, reads files and exports only | 2.5–4 |
| `database-backup-verifier` (#253) | **BUILD** | **Yes**, it calls provider interfaces and restores data | 3–5 |
| Batch overhead (registration, decision row, reciprocity edits, reviews) | — | — | 2–3.5 |
| **Total** | **4 new skills, 1 extension, 0 drops** | | **14.5–24** |

The [backlog forecast](aegis-backlog-forecast.md) carries this group as
"Phase 6 expansion (five skills)" at 10–20 agent-estimated hours. The
recommended set lands above that range because four candidates are real gaps
and two of them (the baseline reviewer and the backup verifier) need
per-provider reference material and refusal cases. Deferring
`environment-parity-reviewer` brings the total to 12–20, inside the forecast.

Roadmap row numbers refer to
[category 07 of the skills roadmap](../skills/07-devops-release-reliability.md).
Two candidates have no numbered row there; they come from the execution
plan's Phase 6 list and the
[product-agnostic roadmap](product-agnostic-skill-and-agent-roadmap.md),
both priority P1 (high-value follow-on work). In category 07, #253 and #254
are P0 (must-have) and #244 and #246 are P1.

## Candidate 1: `cloud-security-baseline-reviewer`

**Roadmap text:** "Review identity, network, secrets, data, logging, policy,
posture, and incident gaps." The reconciliation log's Open Worldwide
Application Security Project (OWASP) Top 10 map also records that "cloud
posture is owed to Phase 6 (`iac-reviewer`, plus
`cloud-security-baseline-reviewer` in the Phase 6 expansion backlog)".

**Purpose.** Given the settings of a cloud account, subscription or managed
platform project as it is actually configured, check each control of a named
security baseline and say, with evidence, which are met and which are not.

**The gap.** The shipped skills design posture or review code, but none
reviews the configured estate control by control:

- [`aws-saas-architect`](../../.claude/skills/aws-saas-architect/SKILL.md) and
  [`azure-saas-architect`](../../.claude/skills/azure-saas-architect/SKILL.md)
  **design** the security posture for a decided provider (guardrail policies,
  posture and threat services, logging). They review an architecture, not a
  configured account, and neither covers GCP or managed platforms.
- [`iac-reviewer`](../../.claude/skills/iac-reviewer/SKILL.md) reviews IaC
  diffs and existing IaC, blast radius first. Settings made in a web console,
  and managed-platform project settings, never appear in IaC.
- [`secrets-identity-hardener`](../../.claude/skills/secrets-identity-hardener/SKILL.md)
  *(manual-only)* moves and rotates application secrets; it does not review
  account-level identity such as owner access or multi-factor sign-in.
- [`security-logging-alerting-architect`](../../.claude/skills/security-logging-alerting-architect/SKILL.md)
  designs detection rules; it does not check that audit logging is switched on
  in every account.
- [`compliance-gap-auditor`](../../.claude/skills/compliance-gap-auditor/SKILL.md)
  audits against a compliance framework (ISO 27001, SOC 2), not a technical
  cloud baseline.
- [`security-scan-orchestrator`](../../.claude/skills/security-scan-orchestrator/SKILL.md)
  runs repository scanners, including IaC scanners; it does not read cloud
  account settings.

| Boundary | Owner |
| --- | --- |
| Control-by-control review of a configured account or platform project | `cloud-security-baseline-reviewer` (new) |
| Designing posture for a decided provider | `aws-saas-architect`, `azure-saas-architect` |
| An IaC change or existing IaC files; IaC-to-runtime drift | `iac-reviewer` |
| Moving or rotating application secrets | `secrets-identity-hardener` |
| What security events must fire alerts | `security-logging-alerting-architect` |
| Readiness against ISO 27001, ISO 42001 or SOC 2 | `compliance-gap-auditor` |
| Cross-tenant leakage in the product | `tenant-isolation-reviewer` |

Extending `iac-reviewer` was considered and rejected: its method is
diff-first, and most baseline failures in small software-as-a-service (SaaS)
teams are console or managed-platform settings with no IaC at all.

**Recommendation: BUILD, auto-invocable.** It reads exported settings,
posture-scanner findings, IaC and screenshots the user supplies, and reports.
It calls no cloud interface and changes nothing, so section 5 of the standard
keeps it auto-invocable. Per-provider reference files (AWS, Azure, GCP,
Vercel, Supabase) list the baseline controls; provider-specific claims become
verification items, never recalled facts. Stop Conditions (the `SKILL.md` section that lists
when the skill must halt or refuse) refuse to mark a
control MET without evidence, refuse to print a secret value found in an
export, and refuse to apply a fix.

**Draft description**, 994 characters measured with Python `yaml.safe_load`
(limit 1,024):

```yaml
description: 'Review the CONFIGURED security baseline of a cloud account, subscription or managed platform project (AWS, Azure, GCP, or hosts like Vercel and Supabase) against a named baseline, control by control: identity and owner access, network exposure, secrets and keys, encryption and public storage, audit logging, guardrail policies, posture services and incident readiness. Each control gets MET, GAP or UNVERIFIED from cited evidence (exported settings, posture-scanner findings, IaC or screenshots the user supplies); missing evidence is never MET. Reads only what it is given, calls no cloud API and changes nothing. Use when asked whether an existing cloud setup is secure, before launch, or after console-made changes. Do NOT use to design a decided provider (aws-saas-architect, azure-saas-architect), review IaC diffs (iac-reviewer), rotate secrets (secrets-identity-hardener), design detection (security-logging-alerting-architect), or audit a compliance framework (compliance-gap-auditor).'
```

**Expected ROUTE-002 reciprocity edits.**

| Excluded neighbor | Current length | Expected edit |
| --- | ---: | --- |
| `aws-saas-architect` | 599 | Reciprocate; room exists |
| `azure-saas-architect` | 999 | Leave one-way (census); no room |
| `iac-reviewer` | 954 | Reciprocate, in one combined rewrite with candidate 4 (see batch summary); needs about 45 characters of rewording |
| `secrets-identity-hardener` | 846 | Leave one-way (census); security hub |
| `security-logging-alerting-architect` | 919 | Reciprocate; room exists |
| `compliance-gap-auditor` | 1,008 | Leave one-way (census); no room |

**Eval plan.**

- Behavior, happy path: an exported account summary with owner multi-factor
  sign-in on, one public storage bucket and audit logging off in one region;
  two GAP findings with the evidence line for each, the rest MET or
  UNVERIFIED.
- Behavior: a Supabase project export with the service key present in a
  client environment file; GAP, the key named by variable only, hand-off to
  `secrets-identity-hardener`.
- Behavior, refusal: "run the AWS command-line tool and fix whatever is open"
  is refused; the skill asks for exported evidence.
- Behavior, edge: no evidence supplied for logging; UNVERIFIED with the export
  that would settle it, never MET.
- Trigger: about 10 cases in both directions against `iac-reviewer` ("review
  this Terraform"), `aws-saas-architect` ("design our AWS security"),
  `compliance-gap-auditor` ("are we SOC 2 ready?") and `security-scan-orchestrator`.
  Because both provider architects also review an existing architecture and
  `iac-reviewer` investigates drift against runtime state, the set includes
  one case in each direction for those seams: "review our existing AWS
  account's security settings" goes to this skill, "review our existing AWS
  architecture" goes to `aws-saas-architect` (and the Azure equivalent to
  `azure-saas-architect`), and "our Terraform and the console disagree" goes
  to `iac-reviewer`.

**Estimate:** 3–5 active hours, driven by the five per-provider reference
files.

## Candidate 2: `resilience-architecture-reviewer`

**Roadmap text:** "Review availability, failover, DR, dependency failure,
backups, chaos tests, and rollback." The D30 note in the reconciliation log
already asked to pull it forward at high priority for "circuit
breakers/bulkheads/timeouts/graceful degradation".

**Purpose.** Answer "what happens when this part fails?" for a system or
design: how each dependency failure is contained, where a single failure
takes everything down, how failover works and whether it was ever tested, and
whether the recovery targets can actually be met.

**The gap.** Failure behavior is touched from several sides, but nobody owns
the whole review, and DR is unowned:

- [`slo-reliability-architect`](../../.claude/skills/slo-reliability-architect/SKILL.md)
  sets reliability targets and walks failure modes to size their impact on the
  targets; findings that need architectural change are routed away ("route to
  `architecture-designer`"). It does not design or review containment,
  failover or DR.
- [`horizontal-scalability-reviewer`](../../.claude/skills/horizontal-scalability-reviewer/SKILL.md)
  reviews scaling out, not failure.
- [`cell-based-architecture-designer`](../../.claude/skills/cell-based-architecture-designer/SKILL.md)
  designs blast-radius cells, a scale-stage option most products never need.
- [`latency-budget-architect`](../../.claude/skills/latency-budget-architect/SKILL.md)
  derives timeouts and retries from latency budgets.
- [`error-handling-security-reviewer`](../../.claude/skills/error-handling-security-reviewer/SKILL.md)
  checks that failures deny access rather than allow it (a security lens).
- [`background-job-orchestration-architect`](../../.claude/skills/background-job-orchestration-architect/SKILL.md)
  owns job retries and dead-letter queues.
- A text search of all 186 skills finds no use of RTO or RPO;
  `data-migration-runbook-author` has only a restore-time gate (restore time
  against the tolerable outage), and no skill designs or reviews DR.

| Boundary | Owner |
| --- | --- |
| Dependency containment, single points of failure, failover, DR targets and fit, fault-injection plan | `resilience-architecture-reviewer` (new) |
| Reliability targets, error budgets and paging | `slo-reliability-architect` |
| Deriving timeout and retry values from a latency budget | `latency-budget-architect` |
| Scaling out to many instances | `horizontal-scalability-reviewer` |
| Blast-radius cells | `cell-based-architecture-designer` |
| Job retries and dead-letter queues | `background-job-orchestration-architect` |
| Whether backups exist and restore (evidence) | `database-backup-verifier` (candidate 5) |
| Rollback steps; incident procedures | `rollback-runbook-author`; `incident-response-runbook` |

**Recommendation: BUILD, auto-invocable.** It reviews designs, code and
configuration it can read, and reports. It runs no fault injection (deliberately breaking a
component to test recovery); a game-day plan (a scheduled, supervised failure
drill) is a document for a person to run. Stop Conditions refuse to call a
failover "tested" without a dated drill record, and stop when no RTO or RPO
exists (ask the owner, explaining both terms, rather than inventing them).

**Draft description**, 975 characters measured with `yaml.safe_load`:

```yaml
description: 'Review how a system survives failure: per dependency, timeouts, retry budgets with backoff, circuit breakers, bulkheads and graceful degradation; single points of failure and zone or region redundancy with a tested failover path; disaster recovery with recovery time and recovery point objectives (RTO, RPO) per service and store and whether the backup strategy can meet them; and a fault-injection or game-day plan to prove it. Severity-ranked findings cite the component, the failure scenario and evidence, with a remediation order; claims without evidence stay UNVERIFIED. Review only; runs no fault injection. Use when asked what happens when a dependency, zone or region fails, or to review failover or DR design. Do NOT use to set SLOs (slo-reliability-architect), assess scale-out (horizontal-scalability-reviewer), allocate timeouts from latency (latency-budget-architect), verify backups (database-backup-verifier), or write rollback steps (rollback-runbook-author).'
```

**Expected ROUTE-002 reciprocity edits.**

| Excluded neighbor | Current length | Expected edit |
| --- | ---: | --- |
| `slo-reliability-architect` | 1,018 | Leave one-way (census); no room |
| `horizontal-scalability-reviewer` | 920 | Reciprocate; room exists |
| `latency-budget-architect` | 963 | Leave one-way (census); little room |
| `database-backup-verifier` | new | Reciprocated by candidate 5's own description |
| `rollback-runbook-author` | 997 | Leave one-way (census); no room |

**Eval plan.**

- Behavior, happy path: a design where checkout calls a payment provider with
  no timeout and a single-zone database; two high findings with the failure
  scenario, and a remediation order.
- Behavior: RPO of 15 minutes but daily backups only; flagged as a DR fit gap,
  with the backup evidence check handed to `database-backup-verifier`.
- Behavior, edge: no RTO or RPO stated; one owner question, no invented
  targets.
- Behavior, refusal: "kill the primary database in production to test
  failover" is refused; a game-day plan is produced instead.
- Trigger: about 10 cases against `slo-reliability-architect` ("what should
  our uptime target be?"), `horizontal-scalability-reviewer` ("can we run
  three instances?"), `latency-budget-architect` and
  `incident-response-runbook` ("write the failover playbook").

**Estimate:** 3–4.5 active hours.

## Candidate 3: `migration-deployment-runbook` (#254)

**Roadmap text:** "Define target confirmation, backup, apply, verify, smoke,
rollback, and documentation steps."

**Purpose as proposed.** A step-by-step procedure for applying a database
migration to a real environment safely.

**What the shipped skills already do.**

- [`data-migration-runbook-author`](../../.claude/skills/data-migration-runbook-author/SKILL.md)
  writes the operator runbook for data moves (backfill, re-shard, cutover,
  tenant move, CDC initial load), already gated on a verified backup and
  dry-run evidence, with per-step verification, abort criteria, per-stage
  rollback and no-return points. Its description already says "write the
  runbook for a backfill/migration/cutover".
- [`gated-deployment-prompt-template`](../../.claude/skills/gated-deployment-prompt-template/SKILL.md)
  writes the reusable template for a **recurring** class of risky operations,
  migrations included, with backup-then-verify gating, per-phase smoke checks
  and a required per-run report.
- [`secure-migration-reviewer`](../../.claude/skills/secure-migration-reviewer/SKILL.md)
  reviews the migration's safety; [`schema-evolution-planner`](../../.claude/skills/schema-evolution-planner/SKILL.md)
  plans the staged sequence;
  [`rollback-runbook-author`](../../.claude/skills/rollback-runbook-author/SKILL.md)
  owns general rollback;
  [`release-readiness-reviewer`](../../.claude/skills/release-readiness-reviewer/SKILL.md)
  gates the release.

**The real gap is small.** Two of #254's seven steps are not explicit
anywhere for a one-off, structure-only migration: **target confirmation**
(proving, before any write, that the connection points at the intended
environment and database, a common and costly mistake) and **post-apply smoke
checks** of the application. The data-move framing of
`data-migration-runbook-author` also makes a plain "apply reviewed DDL to
production" request look out of scope. A standalone skill would collide with
`data-migration-runbook-author` on every "write the migration runbook" prompt.

| Boundary | Owner after the extension |
| --- | --- |
| One-off runbook for a data move or a schema-migration deploy | `data-migration-runbook-author` (extended) |
| Reusable template for a recurring migration class | `gated-deployment-prompt-template` |
| The staged change sequence | `schema-evolution-planner` |
| Safety review of the migration itself | `secure-migration-reviewer` |
| General release rollback | `rollback-runbook-author` |
| The ship or no-ship verdict | `release-readiness-reviewer` |
| Whether the backup the runbook relies on restores | `database-backup-verifier` (candidate 5) |

**Recommendation: MERGE** into `data-migration-runbook-author` as an
extension, the pattern `skill-quality-reviewer` check 3 prefers when content
fits as a scoped addition. The extension:

1. adds a "schema-migration deploy" runbook shape to the workflow and output
   template;
2. makes target confirmation step 1 of every runbook: a read-only
   fingerprint (for example the database name, host and a sentinel row) with
   its expected value, checked before any write;
3. adds post-apply smoke checks with expected output, and a closeout record;
4. updates the description (draft below).

**Manual-only:** no. The skill authors documents only and runs nothing.

**Draft replacement description for `data-migration-runbook-author`**, 1,021
characters measured with `yaml.safe_load`. Both excluded neighbors stay. To fit, it drops the trigger phrase "or to
make a data move operator-safe" and the detail "(counts, checksums, sampled
equality)", so the build must show the existing trigger evals still pass. It
adds the deploy shape, target confirmation, smoke checks
and an exclusion toward `gated-deployment-prompt-template`. "Destructive steps
are human-run" moves from the description into the body, where the same rule
already appears in Stop Conditions.

```yaml
description: 'Author the operator-executable runbook for a DATA move or schema-migration deploy (backfill, re-shard, store cutover, tenant move, CDC initial load, or applying reviewed DDL to a named environment) that a stranger can run under pressure: target confirmed by a read-only fingerprint before any write, preconditions gated on verified backups and dry-run evidence, batching with throttles and pause/resume, per-step verification queries and post-apply smoke checks with expected output, abort criteria naming the safe halt state, per-stage rollback (rollback-runbook-author conventions), and no-return points flagged for human approval. Authors the DOCUMENT only; never executes. Consumes an approved plan (schema-evolution-planner) and safety review (secure-migration-reviewer). Use to write the runbook for a backfill, migration deploy or cutover. Do NOT use for the change SEQUENCE (schema-evolution-planner), recurring templates (gated-deployment-prompt-template), or general release rollbacks (rollback-runbook-author).'
```

**ROUTE-002 edits:** one new one-way finding toward
`gated-deployment-prompt-template` (1,019 characters, no room); leave as
census.

**Eval plan.**

- Behavior: "write the runbook to apply migration 0042 to production"; step 1
  is target confirmation with an expected fingerprint, followed by the backup
  gate, apply, schema verification, smoke checks and rollback reference.
- Behavior, edge: the fingerprint in the plan does not match the named
  environment; the runbook stops at step 1.
- Trigger: two cases pinning a one-off migration deploy to this skill against
  `gated-deployment-prompt-template` ("template our monthly migration
  prompt") and `secure-migration-reviewer` ("is this migration safe?"), plus one case
  pinning "write the rollback plan for migration 0042" to
  `rollback-runbook-author`, whose description triggers on a rollback plan for
  a migration and whose seam the new per-stage rollback wording sits beside.

**Estimate:** 1–2 active hours.

## Candidate 4: `environment-parity-reviewer` (#244, with #246)

**Roadmap text:** #244 "Compare local, CI, staging, preview, and production
environment behavior and config." #246, "Validate required env vars, provider
keys, URLs, modes, and feature flags at startup", is folded in as an output.

**Purpose.** Find the differences between environments that make something
work in one place and fail in another, decide which are intended, and define
the startup checks that catch a missing or wrong setting before users do.

**The gap.** Each shipped neighbor sees one pair of environments or one
layer:

- `iac-reviewer` covers drift between IaC, documentation and the running
  estate (#245), not differences between environments, and not settings held
  outside IaC.
- [`vite-build-qa-engineer`](../../.claude/skills/vite-build-qa-engineer/SKILL.md)
  *(manual-only)* checks build versus preview parity for one front-end build
  tool.
- [`local-ci-mirror-preflight`](../../.claude/skills/local-ci-mirror-preflight/SKILL.md)
  *(manual-only)* mirrors CI checks locally before a push.
- `secrets-identity-hardener` classifies variables as public or server-only;
  [`feature-flag-architect`](../../.claude/skills/feature-flag-architect/SKILL.md)
  designs the flag system.
- A text search of all 186 skills finds no skill that compares environments
  or specifies startup configuration validation.

| Boundary | Owner |
| --- | --- |
| Parity matrix across environments; required-configuration manifest and startup validation | `environment-parity-reviewer` (new) |
| IaC diffs; IaC-to-runtime drift | `iac-reviewer` |
| Build and preview parity of a Vite build | `vite-build-qa-engineer` |
| Running CI checks locally | `local-ci-mirror-preflight` |
| Where secrets live and how they rotate | `secrets-identity-hardener` |
| The feature-flag system and its defaults policy | `feature-flag-architect` |
| Test data per environment | `test-data-architect` |

**Recommendation: BUILD, auto-invocable, lowest priority in the batch.** It
reads repository files (environment templates, lockfiles, container files,
IaC) and exports the user supplies. It reads variable names and non-secret
values only, never secret values, and connects to nothing. The startup
validation is a specification handed to the engineer skills, not code this
skill writes. Stop Conditions refuse to print a secret value and refuse to
call a difference INTENDED without a documented reason.

**Draft description**, 986 characters measured with `yaml.safe_load`:

```yaml
description: 'Review how local, CI, preview, staging and production differ, so "works in staging, fails in production" is caught early: a parity matrix across runtime and dependency versions, environment-variable NAMES and non-secret values, feature-flag defaults, database engine, version and extensions, third-party sandbox versus live modes, auth callbacks, build mode, region, time zone and data shape. Each difference is INTENDED (documented), ACCIDENTAL or UNKNOWN, with evidence and a fix owner; it also drafts the required-configuration manifest and startup validation that fail fast on a missing or wrong setting. Reads repository files and exports it is given, never secret values; connects to nothing. Use when behavior differs between environments, or before promoting to production. Do NOT use for IaC diffs or IaC-to-runtime drift (iac-reviewer), secret handling (secrets-identity-hardener), Vite build checks (vite-build-qa-engineer), or local CI mirroring (local-ci-mirror-preflight).'
```

**Expected ROUTE-002 reciprocity edits.**

| Excluded neighbor | Current length | Expected edit |
| --- | ---: | --- |
| `iac-reviewer` | 954 | Reciprocate in the combined rewrite with candidate 1 |
| `secrets-identity-hardener` | 846 | Leave one-way (census); security hub |
| `vite-build-qa-engineer` | 863 | Reciprocate; room exists |
| `local-ci-mirror-preflight` | 715 | Reciprocate; room exists |

**Eval plan.**

- Behavior, happy path: environment templates for staging and production where
  production lacks one variable and uses a different database extension; two
  ACCIDENTAL findings and a startup-validation entry for the missing variable.
- Behavior: a payment provider in sandbox mode in staging and live mode in
  production is INTENDED only when documented; otherwise UNKNOWN with the
  owner question.
- Behavior, refusal: "paste the production secrets so we can compare them" is
  refused; names only.
- Trigger: about 8 cases against `iac-reviewer` ("our Terraform drifted"),
  `vite-build-qa-engineer` ("works in dev, not in build") and
  `local-ci-mirror-preflight` ("passes locally, fails in CI").

**Estimate:** 2.5–4 active hours.

## Candidate 5: `database-backup-verifier` (#253)

**Roadmap text:** "Verify backups exist, are nonzero, restorable, current, and
outside unsafe commit paths."

**Purpose.** Prove, per database, that a usable backup exists and can be
restored within the agreed time, instead of trusting a "backups enabled"
setting.

**The gap.** Several skills **require** a verified backup; none **produces**
the verification:

- `data-migration-runbook-author` stops without "a VERIFIED backup (not
  'backups are enabled')"; `gated-deployment-prompt-template` gates on
  "verified backup BEFORE"; `rollback-runbook-author` asks that "restore
  points/backups exist". All three consume the evidence.
- [`compliance-evidence-collector`](../../.claude/skills/compliance-evidence-collector/SKILL.md)
  schedules "backup restore test" as periodic audit evidence but never runs
  one.
- [`multi-tenant-data-architect`](../../.claude/skills/multi-tenant-data-architect/SKILL.md)
  and [`pii-lifecycle-designer`](../../.claude/skills/pii-lifecycle-designer/SKILL.md)
  cover retention and deletion in backups, not whether they restore.
- `resilience-architecture-reviewer` (candidate 2) would set the RTO and RPO
  and review whether the backup design can meet them; this skill checks the
  real backups against them.

| Boundary | Owner |
| --- | --- |
| Evidence that each backup exists, is current and restores | `database-backup-verifier` (new) |
| RTO, RPO and DR design | `resilience-architecture-reviewer` (candidate 2) |
| The migration or data-move runbook that needs the backup | `data-migration-runbook-author` |
| A recurring gated operation's template | `gated-deployment-prompt-template` |
| Periodic compliance evidence schedule | `compliance-evidence-collector` |
| Retention and deletion of personal data in backups | `pii-lifecycle-designer` |
| Credentials used to reach the backups | `secrets-identity-hardener` |

Merging into `resilience-architecture-reviewer` was considered and rejected
for the same reason as the QA batch's provisioner: verification calls
provider interfaces and restores data, which would force that review skill to
become manual-only and lose automatic routing.

**Recommendation: BUILD, manual-only.** Evidence mode (the default) runs
read-only listings of backups and their metadata. Drill mode restores only into a named, isolated, non-production target after explicit human approval
that names the drill's cost (a restore spends money on a scratch instance and
its storage, as well as writing data),
compares row counts and checksums with the source snapshot, measures restore
time and removes the scratch copy. Stop Conditions refuse to restore over any
existing database, refuse production as a restore target, refuse to start a drill whose
estimated cost the approval did not state, refuse to print or
store a credential value, and stop when no RTO or RPO is recorded (hand off to
`resilience-architecture-reviewer`). "Outside unsafe commit paths" becomes a
local, read-only check that no database dump sits in the repository or its
history.

**Draft description**, 1,004 characters measured with `yaml.safe_load`:

```yaml
description: 'MANUAL-ONLY; never auto-invoke. Verify database backups would actually save you: per store, a backup exists, is non-empty, is current against the recovery point objective (RPO), is retained and encrypted as required, has an off-account copy, and is RESTORABLE, proven by a restore drill into an isolated scratch target with row-count and checksum parity and a measured restore time against the recovery time objective (RTO). Also flags dump files inside the repository or its history. Evidence mode (the default) runs read-only listings; drill mode restores only to a named non-production target after human approval, never over a source, and names credentials by variable only. CALLS PROVIDER APIS AND RESTORES DATA, so manual invocation only. Use when asked whether backups work or before a risky migration. Do NOT use to design RPO, RTO or DR (resilience-architecture-reviewer), write a migration runbook (data-migration-runbook-author), or design retention for personal data (pii-lifecycle-designer).'
```

**Expected ROUTE-002 reciprocity edits.**

| Excluded neighbor | Current length | Expected edit |
| --- | ---: | --- |
| `resilience-architecture-reviewer` | new (975) | Reciprocated by candidate 2's own description |
| `data-migration-runbook-author` | 982 (1,021 after candidate 3) | Leave one-way (census); no room. Its body names this skill as the source of backup evidence |
| `pii-lifecycle-designer` | 943 | Leave one-way (census) |

**Eval plan.** Every positive prompt names the skill, because the
[standard, section 6](../skill-generation-standard.md#6-evaluations) requires
it for manual-only skills; trigger-eval cases use the prefix
`Explicitly invoke database-backup-verifier. `.

- Behavior, evidence mode: a listing where the newest backup is 30 hours old
  against a 24-hour RPO; reported as a gap, nothing restored.
- Behavior, drill mode: restore to a named scratch target; row-count and
  checksum parity reported with the measured restore time against the RTO,
  and the scratch copy removed.
- Behavior, refusal: "restore last night's backup over production" is refused.
- Behavior, refusal: a zero-byte backup file is never reported as a backup.
- Behavior: a `.sql` dump found in the repository history is flagged, with its
  path and commit, and without printing its contents.
- Behavior, edge: no RTO or RPO recorded; the skill stops and hands off to
  `resilience-architecture-reviewer`.
- Trigger: about 8 cases against `resilience-architecture-reviewer`,
  `data-migration-runbook-author` and `compliance-evidence-collector`, in both
  directions.

**Estimate:** 3–5 active hours. The pull request that builds it will likely
answer "Yes" to the "Security-relevant surface?" question in the
[pull request template](../../.github/pull_request_template.md), because it handles
credentials and restores data.

## Batch summary

**Recommended set:** build `cloud-security-baseline-reviewer`,
`resilience-architecture-reviewer`, `environment-parity-reviewer` and
`database-backup-verifier`; extend `data-migration-runbook-author` with the
schema-migration deploy shape, and retire the `migration-deployment-runbook`
name. The library would go from 186 to 190 skills.

**Suggested pull requests**, so each has one reviewable seam:

1. `resilience-architecture-reviewer`, the `data-migration-runbook-author`
   extension, the `horizontal-scalability-reviewer` reciprocity edit, the
   catalog note recording #254 as merged, the decision row, and a build step
   that repoints the disaster-recovery half of the "uptime/DR commitments"
   route in
   [`soc2-trust-criteria-mapper`'s scoping map](../../.claude/skills/soc2-trust-criteria-mapper/references/tsc-scoping-map.md)
   from `slo-reliability-architect`, which does not do DR, to
   `resilience-architecture-reviewer`.
2. `database-backup-verifier` *(manual-only)*, which completes the
   resilience-backup pair.
3. `cloud-security-baseline-reviewer` and `environment-parity-reviewer`
   together, so the one combined `iac-reviewer` rewrite names both, with the
   `aws-saas-architect`, `security-logging-alerting-architect`,
   `vite-build-qa-engineer` and `local-ci-mirror-preflight` reciprocity edits.
   If the owner defers `environment-parity-reviewer`, this pull request
   carries only the baseline reviewer.

Because #253 and #254 are P0 in category 07, the owner may instead build
`database-backup-verifier` first. That is an ordering choice, not a scope
change: it moves pull request 2 ahead of pull request 1.

Each new skill needs its catalog row (the
[skills catalog](../skills-catalog.md) Phase 6 section), the README counts
inside the validator-checked markers, both eval files, and the registration
steps in [How to add a skill](../../CONTRIBUTING.md#how-to-add-a-skill).

**Total estimate:** 14.5–24 active hours, provisional, including 2–3.5 hours
of batch overhead (registration, decision row, reciprocity edits,
contract-audit comparison and reviews). Deferring `environment-parity-reviewer`
gives 12–20. No route in `project-orchestrator`
(the skill that sequences a project's stages) is proposed; confirm at build time
whether its release stage should name `resilience-architecture-reviewer`.

**Review path per pull request**, as in the feature-flag and QA precedents:
`python -B scripts/validate-skills.py`; `skill-quality-reviewer` checks 1–7 on
each new or extended skill in a fresh session; a ROUTE-002 before-and-after
comparison with `scripts/audit-skill-contracts.py` (a protected script that
this work does not change, and whose frozen baseline is not regenerated);
`library-diff-reviewer` on the whole pull request; then a merge under the
standing conditions of
[AEGIS-APR-048](../approvals/APPROVAL_REGISTER.md#aegis-apr-048-standing-administrator-merge-once-checks-are-green),
[AEGIS-APR-049](../approvals/APPROVAL_REGISTER.md#aegis-apr-049-exact-head-ci-satisfies-the-local-test-condition)
and
[AEGIS-APR-050](../approvals/APPROVAL_REGISTER.md#aegis-apr-050-merges-wait-for-the-automated-codex-review).

**Decision number:** the build would be recorded as **D70**, provisionally.
D67 is the highest decision number in the reconciliation log at `80d9dfe7`.
Open pull request #493 records D68 for the owner's QA Tier 1 build
decision, and open pull request #494 (the AI software-development-lifecycle
batch proposal) claims D69. Open pull request #495 (the Phase 7 batch
proposal) claims only "the next free number". Numbers go to builds in the order they land, so the
real number is the lowest free one when this batch is built; D70 assumes the
QA and AI software-development-lifecycle batches land first. Recheck at build
time.

**Expected ROUTE-002 census after the batch:** ten new one-way findings would
remain: from the baseline reviewer toward `azure-saas-architect`,
`secrets-identity-hardener` and `compliance-gap-auditor`; from the resilience
reviewer toward `slo-reliability-architect`, `latency-budget-architect` and
`rollback-runbook-author`; from the parity reviewer toward
`secrets-identity-hardener`; from the backup verifier toward
`data-migration-runbook-author` and `pii-lifecycle-designer`; and from the
extended `data-migration-runbook-author` toward
`gated-deployment-prompt-template`. Following the D64 owner decision, these
would stay as census data rather than trigger rewrites of full or hub
descriptions.

## What the owner must answer

One reply of "build it as recommended" answers all five with the recommended
option.

1. **Build set.** Approve the recommended set (four new skills, one
   extension)? *Recommended: yes.* Alternative: defer
   `environment-parity-reviewer`, which keeps the batch inside the forecast
   (12–20 hours) and leaves the most self-contained gap for later.
2. **`database-backup-verifier` posture.** Build it manual-only with a
   restore-drill mode? *Recommended: yes*, because "restorable" cannot be
   proven without a restore. Alternative: an auto-invocable reviewer that
   reads supplied backup evidence and writes the drill plan for a person to
   run; it routes automatically but proves nothing by itself.
3. **`cloud-security-baseline-reviewer` posture.** Keep it auto-invocable,
   reading only exported evidence it is given? *Recommended: yes.* The
   alternative, letting it make read-only cloud interface calls itself, is a
   network call and would make it manual-only, so "is our cloud setup secure?"
   would no longer route to it automatically.
4. **`migration-deployment-runbook`.** Merge it into
   `data-migration-runbook-author` rather than build it? *Recommended: yes*,
   to avoid a trigger collision on every "write the migration runbook" prompt.
5. **Census findings.** Accept the ten one-way ROUTE-002 findings listed above
   as census data? *Recommended: yes*, matching D64.

Whether this work counts inside the bounded selected planning subtotal in the
[backlog forecast](aegis-backlog-forecast.md) is not asked; like the
feature-flag and QA work, it stays outside unless the owner selects it.

## What this page does not do

This page grants no authority and builds nothing. It creates no skill,
evaluation, catalog row, README count or decision-log row, and it edits no
shipped skill. An owner "build it" answer would be a new instruction to record;
delivery would then rely on the standing delivery approval in
[AEGIS-APR-039](../approvals/APPROVAL_REGISTER.md#aegis-apr-039-reaffirmation-of-ongoing-backlog-delivery-approval)
and its conditions. Nothing here waives a protected `gate-guard` check (the required CI job
that blocks unapproved changes to the merge gate's own files),
authorizes a change to `scripts/audit-skill-contracts.py` or its frozen
baseline, or permits any cloud call, restore, environment write or deployment.

**Checked for this proposal:** the catalog's Phase 6 implemented and backlog
sections, the reconciliation log's Phase 6 list and D30 pull-forward note,
category 07 rows #244, #245, #246, #253 and #254, the product-agnostic roadmap
rows, the execution plan's Phase 6 list, the descriptions of every neighbor
named above (lengths measured with `yaml.safe_load`), the full bodies of
`iac-reviewer` and the Use When section of `data-migration-runbook-author`,
the relevant body sections of `aws-saas-architect`,
`slo-reliability-architect` and `gated-deployment-prompt-template`, and text
searches of all 186 skills for parity, backup and restore, RTO and RPO,
failover, circuit breakers and bulkheads.

**Not checked:** the neighbors' existing trigger-eval files (the build must
add cases to them where reciprocity edits land), the project-orchestrator
stage map, current provider baseline documents (the build must cite them as
verification items), and `scripts/audit-skill-contracts.py` output; the
expected ROUTE-002 findings above are predicted from the draft descriptions,
not measured. The behavior of the drafted skills is untested; the estimates
are agent estimates, not measurements.
