# Project Aegis

**Project Aegis — Shield of the agent fleet**

*Discipline before code. Evidence before merge.*

Project Aegis is an operating system for engineering software with AI — a reusable
Claude engineering shield: a library of skills, subagents, validation gates, and
safety patterns, governed by Zero-Trust Engineering Discipline, that turns Claude
into a disciplined senior/principal engineering partner for architecture, SaaS,
security, QA, audit, troubleshooting, and AI safety.

## About

Project Aegis is a reusable Claude engineering operating system built to protect, guide,
and sharpen AI-assisted software development. It combines reusable Claude Code skills,
read-only specialist subagents, validation gates, eval conventions, and disciplined
engineering workflows so Claude operates like a senior/principal engineering partner.
The name carries three layers: the divine shield of Zeus and Athena; the Navy's Aegis,
shield of the fleet — fitting for a veteran-founded project whose operating model is a
fleet of agents; and a shield proven in use — several skills' eval cases are drawn from
real incidents this project absorbed during its own construction (an unauthorized
auto-merge, stale-memory session collisions, an empty-directory build). The goal is not
prompt bloat; it is a protected execution framework where Claude models before coding,
reads docs before implementation, tests before changes, keeps diffs small, respects
human approval boundaries, and produces evidence before closeout.

The repo is built in **phases**. **Phase 0** established the foundation — authoring
standard, templates, eval convention, validator, catalog, the seven read-only reviewer
subagents, and the Step 0 reconciliation of the two earlier planning tracks. **Phase 1**
shipped the first real skills: the 8-skill AI engineering **operating-discipline pack**
(reconciled decision D4). **Phase 2** shipped the 10-skill **core architecture &
engineering pack**. **Phase 3** shipped the 9-skill **SaaS & tenant isolation pack**.
**Phase 4** shipped the 9-skill **security, RLS & supply-chain pack**. **Phase 5**
shipped the 16-skill **QA, E2E, manual QA & evidence pack** (the 13 canonical Phase 5
skills plus 3 pulled forward from the QA backlog: roadmap #184/#185/#204). **Phase 1.5**
shipped the 4-skill **AI-SDLC governance completion** (roadmap #261/#268/#279/#280),
completing the category-08 governance layer Phase 1 started. **Phase 6** shipped the
10-skill **cloud, DevOps, reliability & release pack**. **Phase 7** shipped the
14-skill **AI security & LLM systems pack** (v4's 10 plus 4 OWASP LLM Top 10 gap
additions, D6). **Phase 7.5** shipped the **agentic AI security pack** (OWASP
Agentic Top 10 for 2026, D7: 6 new skills + 3 extensions of existing skills;
ASI08+ASI10 merged into one containment reviewer). The **Compliance &
Governance batch** (D9) ships the 9-skill **compliance pack** — ISO
27001:2022 + ISO 42001:2023 + SOC 2 with NIST AI RMF as companion: one
shared control foundation + framework projections + a crosswalk, mapping
controls that largely already exist and producing auditor-grade evidence on
top. The first **D13 library-meta pull** (D18) ships `skill-quality-reviewer`
— the judgment layer atop the mechanical validator, so the library now
reviews its own additions — see [Skills (shipped)](#skills-shipped) below.

## What this is

Aegis is not just a collection of skills; it is an **operating system for engineering
software with AI**. It combines (a) a library of ready-to-use skills an AI coding
assistant follows, (b) read-only specialist reviewers that give independent second
opinions, (c) validation gates and eval conventions that check the work mechanically,
and (d) — governing all of it — **Zero-Trust Engineering Discipline**, the doctrine
that decides how everything above is allowed to operate.

The discipline's essence in one line: **"Never trust, always verify — every step of the
lifecycle. Assume drift. Demand evidence. Track everything."** It is documented at
[docs/ZERO_TRUST_ENGINEERING_DISCIPLINE.md](docs/ZERO_TRUST_ENGINEERING_DISCIPLINE.md)
and deliberately extends the Zero Trust security principle from network access to the
whole development lifecycle. The problem it solves: AI assistants confidently act on
stale memory, claim done-when-not-done, and let docs drift away from the code — this
system replaces that risk with enforced evidence at every step.

## How to use this

**Point an AI coding assistant at the repo.** The skills live under
[`.claude/skills/`](.claude/skills/); point the assistant at this repository (or copy
the skill directories into your own project) and it picks them up from there. Skills
are invoked by their trigger descriptions — each skill's frontmatter states when it
applies, so the assistant selects the right procedure from the task itself.
[`docs/skill-generation-standard.md`](docs/skill-generation-standard.md) defines the
format.

**Run the core loop.** Every change, large or small, follows the same rhythm:

1. **Classify the change** — what kind of change is this, and what validation and
   approval path does that class require?
2. **Verify against evidence** — run the checks; never assume state from memory.
3. **Keep the diff small and reviewable** — one intent, exact files, nothing smuggled in.
4. **A human approves the merge** — the assistant proposes; a person decides.
5. **Record the decision** — a dated entry in the planning record, so history never
   drifts.

This loop is not overhead layered on top of the discipline; it **is** the discipline in
practice.

**Follow the non-negotiable operating rules** (full text with rationales in
[CONTRIBUTING.md](CONTRIBUTING.md)): evidence before merge; one session per repo at a
time; no auto-merge — the human is the gate; and every decision tracked as a dated
entry in the reconciliation doc.

**What a change looks like.** One realistic pass through the loop:

> A developer asks for a new feature. The assistant classifies the change and locks the
> scope, then composes the relevant shipped skills — say, domain modeling, test-first
> implementation, and a security review matching the change class. It produces a small
> diff with passing tests as evidence and opens a pull request, which the validator
> gates in CI. A human reviews and merges. The decision lands as a dated entry in the
> planning record.

## Map of the system

- **Skills** ([`.claude/skills/`](.claude/skills/)) — the ~96 shipped procedures,
  grouped by the phase categories in the catalog: operating discipline, AI-SDLC
  governance, core architecture & engineering, SaaS & tenant isolation, security &
  supply chain, QA & evidence, cloud & reliability & release, AI/LLM security, agentic
  AI security, compliance & governance, and library meta (self-application). Full
  list in [Skills (shipped)](#skills-shipped) below.
- **Subagents** — seven read-only specialist reviewers, one per lens; see
  [Subagents (read-only reviewers)](#subagents-read-only-reviewers).
- **The planning record**
  ([`docs/reconciliation/step-0-reconciliation-v4.md`](docs/reconciliation/step-0-reconciliation-v4.md))
  — the dated decisions (D1–D18) in §5 are the project's immutable decision log; the
  D12/D13/D14/D12.8 candidate scopes recorded there are banked-but-not-built future
  work.
- **The doctrine**
  ([docs/ZERO_TRUST_ENGINEERING_DISCIPLINE.md](docs/ZERO_TRUST_ENGINEERING_DISCIPLINE.md))
  and **the operating rules** ([CONTRIBUTING.md](CONTRIBUTING.md)) — why the system
  works this way, and the eight enforceable rules every session follows.
- **Validation + CI** — the local structural gate ([Validation](#validation)) and the
  merge gate ([CI (merge gate)](#ci-merge-gate)).

## Start here (canonical reading order)

1. [`docs/reconciliation/step-0-reconciliation-v4.md`](docs/reconciliation/step-0-reconciliation-v4.md) — what was reconciled and why (read first).
2. [`docs/research/claude-skills-architecture-audit-findings-v4.md`](docs/research/claude-skills-architecture-audit-findings-v4.md) — canonical architecture audit.
3. [`docs/prompts/claude-skills-master-generation-prompts-v4.md`](docs/prompts/claude-skills-master-generation-prompts-v4.md) — canonical master + phase prompts.
4. [`docs/300-repeatable-software-saas-skills-roadmap.md`](docs/300-repeatable-software-saas-skills-roadmap.md) — the strategic backlog / capability map (the original 300; per the D12 standing rule a 300+ target backlog — ship on demand and framework coverage, not count).
5. [`docs/skills/`](docs/skills/) — category-level backlogs.
6. [`docs/skills-catalog.md`](docs/skills-catalog.md) — implemented vs. backlog, priorities, skills-vs-agents.
7. [`docs/skill-generation-standard.md`](docs/skill-generation-standard.md) — the authoring standard the validator enforces.

**Historical / reference inputs** (superseded by the v4 pair + reconciliation; retained for provenance):

- [`docs/prompts/senior-principal-claude-skills-execution-plan.md`](docs/prompts/senior-principal-claude-skills-execution-plan.md) — earlier combined execution plan (now historical).
- `docs/research/claude-skills-principal-architecture-findings.md`
- `docs/prompts/master-claude-skills-and-agents-development-prompt.md`
- `docs/prompts/phased-claude-skills-prompts.md`
- `docs/roadmaps/product-agnostic-skill-and-agent-roadmap.md`
- `docs/150-claude-skills-roadmap.md` (superseded by the original 300-skill roadmap — per the D12 standing rule a 300+ target backlog, not a cap)

## Reconciled phase plan (single source of truth)

The v4 phase structure is canonical. See [the reconciliation doc](docs/reconciliation/step-0-reconciliation-v4.md) §3
for the per-phase skill lists and how the older execution-plan names merge in.

| Phase | Pack | Priority | Status |
|---:|---|---|---|
| 0 | Foundation: standard, templates, eval convention, validator, catalog, README, 7 subagents, `_template` | P0 | ✅ merged |
| 1 | AI engineering **operating-discipline** pack (8 skills) | P0 | ✅ merged |
| 1.5 | AI-SDLC **governance completion** (4 skills: roadmap #261/#268/#279/#280) | P0/P1 | ✅ merged |
| 2 | Core architecture & engineering (10) | P0 | ✅ merged |
| 3 | SaaS & tenant isolation (9) | P0/P1 | ✅ merged |
| 4 | Security, RLS & supply chain (9) | P0/P1 | ✅ merged |
| 5 | QA, E2E, manual QA & evidence (16 = 13 canonical + 3 pulled forward from the QA backlog: roadmap #184/#185/#204) | P0/P1 | ✅ merged |
| 6 | Cloud, DevOps, reliability & release (10) | P1 | ✅ merged |
| 7 | AI security & LLM systems (14 = v4's 10 + 4 OWASP LLM Top 10 additions, D6) | P1 | ✅ merged |
| 7.5 | Agentic AI security (OWASP Agentic Top 10, D7: 6 new + 3 extensions) | P1 | ✅ merged |
| D9 | Compliance & Governance batch (9 = 3 shared foundation + 3 framework projections + 3 cross-cutting; ISO 27001 + ISO 42001 + SOC 2, NIST AI RMF companion) | P1 | ✅ this branch |
| D13 (pull 1) | Library meta / self-application: `skill-quality-reviewer` — the judgment layer atop the mechanical validator (D18); other 4 D13 candidates stay banked | P1 | ✅ shipped (D18) |
| 8 | Backlog expansion in ≤20-skill validated batches | P2 | backlog |

## Subagents (read-only reviewers)

Real project subagents live under `.claude/agents/<name>.md` (reconciled decision D2),
read-only by default. Each maps to a v4 orchestrator role (see reconciliation §5):

| Subagent | Lens |
|---|---|
| `principal-architecture-reviewer` | Architecture boundaries, coupling, data ownership, scalability. |
| `secure-saas-reviewer` | Tenant isolation, RLS, authz, secrets, cross-tenant leakage. |
| `qa-automation-lead` | Test strategy, coverage gaps, flake risk, release evidence. |
| `full-codebase-auditor` | Whole-repo inventory, evidence-based risk, debt map. |
| `senior-troubleshooting-lead` | Reproduction, hypothesis ranking, root cause. |
| `ai-security-red-team-reviewer` | Prompt injection, tool/RAG abuse, data exfil. |
| `release-readiness-reviewer` | CI/build/test evidence, migrations, rollback, go/no-go. |

## Skills (shipped)

Phase 1 — AI engineering operating-discipline pack, under `.claude/skills/<name>/`
(full detail: [`docs/skills-catalog.md`](docs/skills-catalog.md)):

| Skill | What it does | Invocation |
|---|---|---|
| `agent-startup-context-gate` | Verifies repo identity and loads governing context before any work; halts when the location can't be verified (a path that exists is not proof it's the right repo). | auto + manual |
| `source-of-truth-reconciler` | Resolves conflicts between instructions, docs, code, tests, and memory by evidence-cited precedence; surfaces every assumption. | auto + manual |
| `change-classification-gate` | Classifies a change before work → validation floor + approval path; locks scope to the approved class. | auto + manual |
| `human-approval-boundary` | Halts for explicit approval before schema, RLS/security, prod-data, secrets, deploy, billing, or destructive work; stops when security impact is unclear. | auto + manual |
| `reviewable-diff-discipline` | Keeps diffs small and intentional; stages exact files only; staged set must equal declared intent. | auto + manual |
| `ai-closeout-reporter` | Terminal closeout report with a mandatory "intentionally not done / omitted" section — scope reductions are never silent. | auto + manual |
| `agent-failure-recovery` | Preserve-first recovery from broken git/tree state; destructive cleanup only with backup + explicit approval. | **manual only** |
| `agent-instruction-consolidator` | Aligns CLAUDE.md / AGENTS.md / Cursor / Copilot instruction files to one canonical source with rule-preservation proof. | **manual only** |

Phase 1.5 — AI-SDLC governance completion (roadmap #261/#268/#279/#280; completes the
category-08 layer Phase 1 started — composes the Phase 1 skills, never restates them):

| Skill | What it does | Invocation |
|---|---|---|
| `ai-sdlc-operating-model` | End-to-end human+agent lifecycle contract: named stages with entry/exit gates, per-stage authority (human / agent / agent-with-approval), enforcing skill per stage, failure routing, learning loop; grounded in observed PR practice with a gap list. | auto + manual |
| `agent-authorization-matrix` | Deny-by-default action × context matrix of standing agent authority — merge to protected branches requires a named human always; auto-merge arming is forbidden to agents (armed state re-checked after every push); approval scope/expiry semantics; proposal-first. | **manual only** |
| `agent-memory-governance` | Persistent-memory WRITE/TRUST/HYGIENE rules: confirmed durable facts with provenance and absolute dates, never secrets; remembered repo/PR state verified against live git/gh before acting; disposition-approved cleanups. | **manual only** |
| `agent-governance-audit` | Audits one AI-assisted change's process compliance from primary evidence (PR timeline incl. who armed auto-merge, commits, CI runs): per-control PASS/FAIL/UNVERIFIABLE verdicts; closeout claims cross-checked; missing evidence is never a PASS. | auto + manual |

Phase 2 — core architecture & engineering pack:

| Skill | What it does | Invocation |
|---|---|---|
| `domain-modeler` | Domain model from requirements/code — language, bounded contexts, aggregates with invariants; hard "do not code yet" gate at the end. | auto + manual |
| `architecture-designer` | Inspects the CURRENT architecture first, then component/dependency/data-ownership maps, tradeoffs, ADR draft, and an incremental migration plan. | auto + manual |
| `adr-writer` | Architecture Decision Records with honest alternatives, consequences, operational impact, mandatory rollback/reversal plan and review date. | auto + manual |
| `docs-first-implementer` | Pins the exact installed library version (lockfile), reads version-matching docs before coding, verifies with real commands; declares uncertainty instead of guessing. | auto + manual |
| `tdd-engineer` | Strict red-green-refactor: confirms each test fails for the intended reason before the minimal implementation; reports exact commands and results. | auto + manual |
| `systematic-debugger` | Reproduce → reduce → isolate → fix one thing → verify → prevent; prediction-tested hypotheses, single-variable fixes, regression test kept. | auto + manual |
| `code-reviewer` | Reviews actual diffs only — severity-ranked findings with file:line evidence and remediation; no diff, no review. | auto + manual |
| `code-simplifier` | Behavior-preserving simplification with the suite green before and after every move; coverage gate; restraint ("not done" list) is a deliverable. | **manual only** |
| `principal-code-analyst` | Subsystem-level strategic analysis laddering code findings to architecture, security, cost; risk register + small-step remediation with validation signals. | auto + manual |
| `full-codebase-auditor` | Whole-repo audit with inventory-first coverage; findings filed as confirmed / likely / hypotheses / missing information. (Skill = procedure; same-named subagent composes it.) | auto + manual |

Phase 3 — SaaS & tenant isolation pack:

| Skill | What it does | Invocation |
|---|---|---|
| `saas-platform-architect` | Platform structure: per-component pooled/siloed/bridge decisions with named isolation mechanisms, control-plane/data-plane split, capability inventory, rollout plan with per-step rollback. | auto + manual |
| `tenant-modeler` | Tenant semantics: definition, hierarchy, membership-as-entity (roles on membership), invitations, ownership, and a lifecycle state machine with per-state access/data/billing/jobs posture. | auto + manual |
| `tenant-isolation-reviewer` | Reviews real systems for cross-tenant leakage across all 15 surfaces (identity → audit, incl. AI retrieval); evidence-cited findings, isolation test matrix, negative tests, honest not-inspected list. | auto + manual |
| `multi-tenant-data-architect` | Per-store tenant scoping decisions (incl. caches, search, vector stores), server-derived tenant-context propagation, ownership map, expand→contract migration with verification and rollback. | auto + manual |
| `authorization-matrix-designer` | Deny-by-default roles × permissions × resources matrix, object-level rules, enforcement-point map, brokered support access, negative tests, additive role migration. | auto + manual |
| `plan-entitlement-architect` | Plan × entitlement matrix with one resolution point enforced uniformly on every surface; metering hooks; plan transitions with no silent data loss; grandfathering + rollback. | auto + manual |
| `audit-log-architect` | Audit event taxonomy, versioned record schema, append-only integrity with explicit write-failure policy, retention/redaction, tenant-scoped access, negative tests. | auto + manual |
| `saas-cost-architect` | Bill-grounded cost drivers, per-tenant attribution (or admitted overhead), distribution-based unit economics vs revenue, exposure math, guardrails with observe-first rollout. | auto + manual |
| `api-event-architect` | External API/event contracts: credential-derived tenant context, idempotency, per-tenant/plan rate limits, versioning with dual-run deprecation, tenant-scoped signed webhooks. | auto + manual |

Phase 4 — security, RLS & supply-chain pack:

| Skill | What it does | Invocation |
|---|---|---|
| `threat-modeler` | Design-time threat model: assets/actors/trust-boundaries, STRIDE per boundary, abuse cases, exploit-path-gated severity, mitigations mapped to negative tests; consumes tenant/authz outputs instead of re-deriving them. | auto + manual |
| `appsec-implementer` | Implements one NAMED security control test-first — negative test red→green, minimal server-side control, scoped diff, residual risk stated. | **manual only** |
| `multi-tenant-security-tester` | Executable cross-tenant/authorization negative suite: two-tenant fixtures, forbidden-action-denied assertions, positive controls, IDOR/list/mass-assignment/exports/jobs, honest coverage. | auto + manual |
| `rls-policy-auditor` | Per-command RLS audit/authoring (merges rls-policy-author + rls-negative-test-designer): recursion, unsafe SECURITY DEFINER, broad grants, missing tenant scope, service-role leakage, frontend-derived scope; mandatory negative-test plan; policies delivered as a migration, never run live. | auto + manual |
| `secrets-identity-hardener` | Env classification (catches VITE_/NEXT_PUBLIC_ leaks), moves secrets server-side with a client-bundle-absence proof, rotates leaked credentials, least-privilege service accounts, session/token flags. | **manual only** |
| `supply-chain-security-reviewer` | SLSA-style: lockfile-based dependency set, reachability triage of scanner output, install/build-script and CI compromise paths, SHA pinning, compromise-path-gated severity. | auto + manual |
| `security-pr-reviewer` | Security lens on an actual diff: authz/object-level/tenant-scope, injection, secrets, SSRF, control-weakening detection; exploit-path-gated findings; no diff, no review. | auto + manual |
| `secure-migration-reviewer` | Whole-migration deploy safety: RLS/policy gaps, GRANT widening, unsafe defaults, destructive/irreversible ops, tenant-scoped backfills, lock risk, expand→contract deploy order, rollback; delegates policy text to `rls-policy-auditor`. | auto + manual |
| `static-analysis-reviewer` | Triages SAST/CodeQL/SARIF on first-party code: dedup, confirm-against-code disposition (TP/FP/dup/accepted), five-axis ranking (reachability/exploitability/asset/tenant/business), written suppression policy. | auto + manual |

Phase 5 — QA, E2E, manual QA & evidence pack (13 canonical + 3 pulled forward from the
QA backlog, roadmap #184/#185/#204):

| Skill | What it does | Invocation |
|---|---|---|
| `qa-strategy-architect` | Product-level QA strategy: ranked risk inventory → cheapest-reliable-layer decisions, explicit automation/manual split, evidence per change class, CI gates, ownership. | auto + manual |
| `test-plan-designer` | Per-change test plan: risk-traced items with layer/data/environment, objective entry/exit criteria, named artifacts and CI placement, explicit out-of-scope list. | auto + manual |
| `test-coverage-mapper` | Coverage audit: surface inventory first, maps tests by reading assertions (theater ≠ coverage), risk-ranked gaps with cheapest fill layer, honest not-inspected list. | auto + manual |
| `qa-automation-architect` | Automation blueprint: tools per layer with rationale, structure/fixtures/auth-state, parallel-safe isolation, CI tiers with bounded logged retries, flake policy, migration steps. | auto + manual |
| `playwright-e2e-engineer` | Critical-journey Playwright specs: role/label locators, web-first assertions, zero sleeps/networkidle, storageState per persona, failure traces, honest run reports. | **manual only** |
| `clickthrough-test-engineer` | Pre-planned interactive walkthrough of a running app (forms with invalid input, dialogs, permissions, states, console), severity-rated defects with masked evidence, honest coverage. | **manual only** |
| `manual-test-case-creator` | Stranger-executable manual cases: exact data/roles/environment, one observable expected result per step, screenshot checkpoints, verdict rules, cleanup. | auto + manual |
| `screenshot-evidence-planner` | Evidence policy: risk-justified checkpoints, deterministic naming, mandatory pre-storage masking, metadata, storage/retention classes, case/PR/closeout linkage. | auto + manual |
| `vitest-unit-component-engineer` | Vitest unit/component tests: intentional node-vs-DOM environment per file, owned-seam mocks, Testing Library queries, determinism, real run output. | **manual only** |
| `vite-build-qa-engineer` | Build-artifact QA: `VITE_` env classification, dist-level secret proof, build/preview parity (base, deep links, modes), bundle budgets, sourcemap policy. | **manual only** |
| `flaky-test-detective` | Classify → reproduce with counts → fix ONE cause → prove stability; no retries/sleeps/weakened assertions; product races routed as product bugs; quarantine with owner/ticket/expiry. | auto + manual |
| `test-data-architect` | Test-data design: read-only persona/baseline catalog, per-layer sources, determinism, worker-scoped isolation, synthetic-only PII posture, cleanup + seed evolution. | auto + manual |
| `regression-suite-curator` | Evidence-based promote/retain/demote/retire with written rationale, protected security regressions, enforced quarantine registry, tier-budget fit. | auto + manual |
| `integration-test-designer` | (pulled forward, #184) The layer between unit and E2E: real service/command/DB/auth/permission boundaries, named faked seams, persisted-state assertions, no browser. | auto + manual |
| `api-contract-test-designer` | (pulled forward, #185) Contract verification: provider/consumer roles, schema + error-envelope validation, additive-vs-breaking CI gate, version coverage; design stays with `api-event-architect`. | auto + manual |
| `accessibility-test-harness` | (pulled forward, #204) WCAG-pinned a11y harness: automated scans (baseline+ratchet) AND manual keyboard/focus/contrast/screen-reader checklists; honest about automation limits. | auto + manual |

Phase 6 — cloud, DevOps, reliability & release pack (`rollback-strategy-designer`
merged into `rollback-runbook-author` per reconciliation §3):

| Skill | What it does | Invocation |
|---|---|---|
| `cloud-architecture-decider` | Cloud-neutral platform decision: nine-axis requirements record, provider-neutral logical architecture, isolation/compliance hard filters before scoring, managed-vs-self-hosted with the operational bill, exit costs and reopen triggers. | auto + manual |
| `azure-saas-architect` | Maps a decided logical architecture to provider-idiomatic Azure: Entra ID/managed identities/OIDC, VNets + Private Link, per-store tenant isolation, compute by team maturity, Azure Policy/Defender posture, Bicep/Terraform, tag-keyed cost controls; SKU/limit/price claims become verification items. | auto + manual |
| `aws-saas-architect` | Maps a decided logical architecture to provider-idiomatic AWS: Organizations/SCPs, IAM roles + OIDC, VPC/PrivateLink, per-store tenant isolation, compute by team maturity, Security Hub/GuardDuty posture, Terraform/CDK, cost-allocation tags; quota/type/price claims become verification items. | auto + manual |
| `iac-reviewer` | Review-only IaC audit with blast radius first: destructive replaces, public exposure, IAM width deltas, secrets in code and state, tenant-isolation impact, drift, pinning, cost flags; never applies or runs plan against live backends. | auto + manual |
| `ci-pipeline-architect` | Pipeline stage graph with blocking semantics and a latency budget, CI secret governance (OIDC over stored keys, fork-PR posture), artifact provenance, promotion gates with named humans, branch-protection alignment; composes qa-automation-architect tiers. | **manual only** |
| `release-readiness-reviewer` | Evidence-based ship/no-ship gate: every dimension cites a verifiable artifact or is MISSING; CI evidence pinned to the release SHA; unknown = No-Go with the evidence that flips it. (Skill = procedure; same-named subagent composes it.) | auto + manual |
| `rollback-runbook-author` | Rollback strategy + stranger-executable runbook in one artifact: decision criteria with time-box, per-layer primitives in order, bad-window data repair, rehearsal log and staleness triggers; authors only, never executes. | auto + manual |
| `observability-operator` | Hands-on observability: structured redacted instrumentation, truthful health checks, alerts with severity/owner/runbook-link/justified threshold, query-verified claims, silences only with owner+expiry. | **manual only** |
| `slo-reliability-architect` | Journey-derived SLOs: symptom-based SLIs with measurement points, error budgets in user units, burn-rate paging with cause-alert demotion, budget policy with consequences, per-tenant reliability views. | auto + manual |
| `incident-response-runbook` | Incident machinery: one-minute severity ladder, IC/comms/ops roles, triage to decision points, containment invoking the rollback artifact by reference, tenant-aware comms, blameless postmortem where every finding lands as a test/alert/fix or owned risk. | auto + manual |

Phase 7 — AI security & LLM systems pack (14 = v4's 10 + 4 OWASP LLM Top 10 gap
additions, D6). Anchored to the OWASP Top 10 for LLM Applications (2025); these
skills **compose** the shipped tenant/security/cost/governance packs rather than
re-deriving them. **LLM03** is extend-existing (the shipped
`supply-chain-security-reviewer` was extended to models/datasets/adapters);
**LLM10** DoS/denial-of-wallet is baked into `ai-cost-guardrail-designer`;
`ai-evaluation-harness` absorbs the AI security test harness:

| Skill | What it does | Invocation |
|---|---|---|
| `ai-threat-modeler` | AI-specific threat model: AI assets + trust boundaries (all untrusted content), per-boundary threats anchored to the OWASP LLM Top 10, abuse cases, exploit-path-gated severity, each mitigation mapped to an owning skill + red-team case; composes `threat-modeler` for the classic surface. | auto + manual |
| `prompt-injection-defender` | Layered injection defense (LLM01): trust zones, the untrusted-content invariant, content/instruction separation, and the primary layer — deterministic action authorization OUTSIDE the model; direct + indirect payloads; red-team suite with SAFE-outcome assertions. | **manual only** |
| `rag-security-architect` | RAG/vector-store security (LLM08): authorization AT RETRIEVAL TIME (never post-filter), per-tenant index scoping, document-ACL propagation, embedding risks (inversion/membership/poisoning/stale-permission); composes `tenant-isolation-reviewer` + `multi-tenant-data-architect`. | auto + manual |
| `agent-tool-safety-guard` | Least-privilege tool access (LLM06): per-tool blast-radius matrix, calling-user authority (no service-account confused deputy), argument validation before execution, approval gates on irreversible actions, tool-chain abuse; composes `human-approval-boundary` + `agent-authorization-matrix`. | auto + manual |
| `llm-output-safety-reviewer` | Output-handling review (LLM05): model output as untrusted data to render/execute/URL/tool/store sinks (XSS/RCE/SSRF/injection/second-order), context-correct encoding, generated-code sandboxing; exploit-flow-gated findings. | auto + manual |
| `ai-evaluation-harness` | Versioned eval dataset (representative + adversarial/red-team + regression), per-dimension graders + thresholds (quality/schema/safety/grounding/injection/latency/cost), CI regression gate; absorbs the AI security test harness; honest real-run reporting. | **manual only** |
| `ai-cost-guardrail-designer` | Consumption guardrails (LLM10 DoS/denial-of-wallet): per-request token caps, tenant-scoped budgets/rate limits, agent loop/recursion bounds, fail-safe degraded mode + kill switch, burn-rate alerts before exhaustion; composes `saas-cost-architect` + `observability-operator`. | auto + manual |
| `ai-governance-risk-reviewer` | AI governance/risk posture: impact-based risk tiering, oversight-to-tier matching, accountable ownership, AI disclosure/consent, model/feature card, obligation→control mapping (EU AI Act tiers, NIST AI RMF) without asserting legal conclusions. | auto + manual |
| `ai-router-architect` | Centralized model-routing layer: one interface, server-side-only credentials, task/cost routing, choke-point cost enforcement, per-call telemetry, resilient fallback + circuit breaker + no-deploy kill switch, idempotent retries; composes `secrets-identity-hardener` + `observability-operator`. | **manual only** |
| `structured-output-validator` | Output-shape contract (LLM05 companion): schema (fields/types/enums/ranges), validate-before-use, semantic checks beyond shape (tenant-scoped ids), bounded failure handling; shape-is-not-safety handoffs to `llm-output-safety-reviewer` + `agent-tool-safety-guard`. | auto + manual |
| `sensitive-disclosure-guard` | (NEW, LLM02) Disclosure defense: data-minimization + pre-model redaction of secrets/PII/other-tenant data, output-path echo/bleed checks, log redaction at emission, provider retention/training posture; composes `tenant-isolation-reviewer` + `secrets-identity-hardener`. | auto + manual |
| `model-poisoning-reviewer` | (NEW, LLM04) Training/feedback/ingestion integrity: contributor-trust assessment, poisoning paths, feedback-loop Sybil defense, ingestion-as-truth integrity, provenance/holdout controls; acquire-vs-ingest boundary with `supply-chain-security-reviewer`. | auto + manual |
| `system-prompt-leakage-reviewer` | (NEW, LLM07) Two axes: no secrets in the prompt AND no security dependence on prompt secrecy — **system prompts are NOT security controls**; enforcement is deterministic and lives OUTSIDE the LLM; extraction-is-harmless framing. | auto + manual |
| `ai-misinformation-guard` | (NEW, LLM09) Grounding in retrieved sources (not memory), citation-to-claim verification, calibrated uncertainty/refusal, fact validation before action, package/API hallucination (slopsquatting) checks, overreliance-aware UX. | auto + manual |

Phase 7.5 — agentic AI security pack (6 new + 3 extensions). Anchored to the
OWASP Top 10 for Agentic Applications (2026), ASI01–ASI10, per reconciliation
§3 (D7). The Agentic Top 10 **extends** the LLM Top 10: agent systems inherit
every Phase 7 risk; this pack adds autonomy, tool, identity, memory, and
multi-agent risks on top. **ASI08+ASI10 merged** into one
`agent-containment-reviewer` (D7). **Extensions (scoped diffs, not new
skills):** `agent-tool-safety-guard` extended for ASI02 + the tool-side slice
of ASI05 (tool misuse, side-effect limits, code-execution tool class);
`llm-output-safety-reviewer` extended for ASI05 (autonomous generate-and-run
loops, ephemeral sandboxes, NL-to-execution paths);
`supply-chain-security-reviewer` extended again (after D6/LLM03) for ASI04
(MCP servers/manifests, tool/skill registries, plugins, A2A dependencies):

| Skill | What it does | Invocation |
|---|---|---|
| `agent-goal-hijack-defender` | (ASI01) Goal/plan integrity for multi-step agents: pinned goal record outside the model context, principal-only mutation channel, per-step tracing, deviation detection, drift response, per-channel hijack red-team suite; builds on `prompt-injection-defender` (LLM01 owns the vector). | **manual only** |
| `agent-identity-privilege-reviewer` | (ASI03) Agent identity architecture: distinct least-privilege identity per agent, task/time-scoped credentials, delegation chains that attenuate (never amplify), confused-deputy closure, dual attribution (principal + agent); complements `secrets-identity-hardener`. | auto + manual |
| `memory-context-poisoning-reviewer` | (ASI06) Persistent memory poisoning review: write-path trust, validation-before-write, provenance, tenant/user/session scoping at write AND recall, TTL + purge with rollback, recalled memory as data never instructions; distinct from `model-poisoning-reviewer` (LLM04) and `rag-security-architect` (LLM08). | auto + manual |
| `inter-agent-comms-reviewer` | (ASI07) A2A/MCP message security: per-edge mutual authn, end-to-end integrity, replay bounds, confidentiality, topology allowlists, spoofed results; authenticated ≠ trusted — peer messages never re-task or assert authority. | auto + manual |
| `agent-containment-reviewer` | (ASI08+ASI10 merged) Cascade half: blast-radius isolation, bounded upstream trust, circuit breakers, checkpoints/rollback, retry-storm limits. Rogue half: drift baselines, agent inventory/lifecycle, kill switches that SEVER AUTHORITY (credentials revoked, not processes killed); composes `ai-cost-guardrail-designer` + `incident-response-runbook`. | auto + manual |
| `human-agent-trust-reviewer` | (ASI09) Adversarial review of the approval layer: consent fatigue (rate/latency signals), self-reported summaries vs system-verified facts, bundling, urgency manipulation, automation-bias controls; counterpart to `human-approval-boundary`. | auto + manual |

Compliance & Governance batch (D9) — ISO 27001:2022 + ISO 42001:2023 + SOC 2,
with NIST AI RMF 1.0 as voluntary companion. Architecture: **one shared
control foundation + framework projections + a crosswalk** — not three
parallel skill sets. The batch **maps controls that largely already exist**
(Phases 3/4 technical controls, the Phase 5 evidence pack, Phase 1.5 +
Phase 7 AI governance) and produces auditor-grade evidence on top. Every
skill encodes the D9 precision flags (SOC 2 = AICPA **attestation**, never
certification; Annex A counts secondary-sourced/conflicting — verify before
citing; ~60–80% overlap = industry estimate) in a Compliance Precision
Rules section:

| Skill | What it does | Invocation |
|---|---|---|
| `compliance-control-foundation` | One framework-agnostic control catalog (access control, crypto, change mgmt, logging/monitoring, incident response, vendor mgmt, risk assessment + AI governance): each control written once with objective, owner, mechanism mapped by name to shipped skills, evidence hook, honest status. | auto + manual |
| `compliance-evidence-collector` | Operating-effectiveness evidence OVER TIME (SOC 2 Type 2's core demand, reused for ISO surveillance): per-control cadence matched to operating frequency, populations for sampling, retention/integrity, window-coverage matrix with holes; never mutates a live evidence store. | auto + manual |
| `statement-of-applicability-author` | The ISO-mandatory SoA serving both 27001 and 42001: per-control include/exclude justified by 6.1.3 risk-treatment traces, controlled-document diffs, licensed-Annex-A-only rows — never reconstructed from memory. | auto + manual |
| `iso-27001-isms-architect` | ISMS clauses 4–10 (incl. Amd 1:2024 climate-relevance check), four-theme Annex A selection via the foundation; headline net-new = risk register, internal audit program, management review cadence; readiness plan, never a certification claim. | auto + manual |
| `iso-42001-aims-architect` | AIMS clauses 4–10 + AI risk assessment (6.1.2/8.2), AI risk treatment (6.1.3/8.3), AI system impact assessment (6.1.4/8.4 — individuals/societies); maps the Phase 1.5 governance pack as operational mechanisms; Annex A counts never stated (sources conflict). | auto + manual |
| `soc2-trust-criteria-mapper` | SOC 2 scoping as ATTESTATION (never certification): system boundary, commitment-driven TSC category selection (Security baseline + optional four), Type 1 vs Type 2 with window feasibility, subservice carve-outs; Type definitions flagged CPA-firm-sourced. | auto + manual |
| `multi-framework-crosswalk` | One control → 27001 Annex A + SOC 2 TSC + 42001 Annex A (+ AI RMF function): edition-pinned, text-in-hand cells only, FULL/PARTIAL(residue) honesty, explicit joint sets — the do-the-work-once engine. | auto + manual |
| `compliance-gap-auditor` | ONE parameterized gap audit vs chosen framework(s): MET/PARTIAL/GAP/UNVERIFIABLE per requirement from cited evidence (missing evidence is never MET), blockers-first remediation order; readiness assessment, never an audit opinion. | auto + manual |
| `ai-lifecycle-risk-manager` | NIST AI RMF GOVERN/MAP/MEASURE/MANAGE operationalized across the AI lifecycle with owners, triggers, and a risk register; voluntary and under revision — never a certification target; companion to `iso-42001-aims-architect`. | auto + manual |

D13 pull 1 — library meta / self-application (D18): the library starts
applying its own discipline to itself. Pure review skill (verdict report
only, edits nothing) → model-invocable. It **composes**
`scripts/validate-skills.py` — runs it first as the entry gate, never
re-implements its mechanical checks — and leaves the whole
skill-adding-PR audit to `library-diff-reviewer` (D13 candidate, not
built; the seam is pinned in trigger-evals). The other four D13
candidates remain banked in the reconciliation doc §3:

| Skill | What it does | Invocation |
|---|---|---|
| `skill-quality-reviewer` | The judgment layer above the mechanical validator: validator-first gate, then the seven checks it cannot script — trigger quality (trigger-oriented vs merely descriptive), trigger collision against the full shipped corpus (colliding skills NAMED), duplication/extension (the LLM03/ASI04 precedent), eval integrity (boundary cases vs hollow filler), section substance (Stop Conditions that actually refuse), scope discipline, invocation posture. Per-check PASS/CONCERN/FAIL with quoted evidence → ship / revise / reject / make-it-an-extension. | auto + manual |

## Authoring a new skill

1. Read [`docs/skill-generation-standard.md`](docs/skill-generation-standard.md).
2. Copy `.claude/skills/_template/` to `.claude/skills/<your-skill-name>/`.
3. Set frontmatter `name` to match the new directory exactly.
4. Fill in all required sections; keep `SKILL.md` under 500 lines (push detail to `references/`).
5. Add `evals/evals.json` (and `evals/trigger-evals.json` if the trigger overlaps another skill).
6. List the skill in [`docs/skills-catalog.md`](docs/skills-catalog.md) **and** this README.
7. Run the validator until it passes.

Side-effecting skills (writes, network, deploy, spend) MUST set `disable-model-invocation: true`
and document the irreversible step under **Stop Conditions**.

## Validation

Run from the repo root:

```bash
python scripts/validate-skills.py
```

Checks: `name` matches directory; `description` present and < 1024 chars; no broad
`allowed-tools`; `SKILL.md` < 500 lines; all required sections present; `evals/evals.json`
exists and parses (structural only — no runner yet); `evals/trigger-evals.json` parses when
present; catalog integrity (every skill listed in catalog + README, none claimed that don't
exist); bundled-name collision and duplicate-name checks.

Behavior: `_template` is ignored. When `_template` is the only skill directory, the validator
prints a "no skills found" status and exits `0`. Exit `0` = clean (warnings allowed); non-zero
= at least one error. Run it before every commit that touches `.claude/skills/`.

## CI (merge gate)

Every pull request targeting `main` runs
[`.github/workflows/validate-skills.yml`](.github/workflows/validate-skills.yml), which
provides two required status checks:

| Check | What it does |
| --- | --- |
| `validate-skills` | Runs `python scripts/validate-skills.py` on the PR (latest Python 3.x). Fails on any validator error — same checks as running it locally. |
| `gate-guard` | Diffs the PR against its base and **fails if the PR touches the merge gate itself** (anything under `.github/workflows/` or `scripts/validate-skills.py`). Such PRs print `This PR modifies the merge gate itself and requires manual review and merge.` and must be reviewed and merged manually by a human. |

Notes:

- Both job names are registered as required status checks — do not rename them (and keep
  them unique across all workflows) without updating branch protection.
- A `gate-guard` failure is not a defect; it is the intended signal that the change needs
  human eyes. Fixing the gate to "make CI green" defeats its purpose.
- The gate uses only `actions/checkout` and `actions/setup-python` — no third-party actions.
- Auto-merge is enabled per-phase via `gh pr merge --auto --squash` — never for changes
  touching the merge gate itself (see
  [`docs/reconciliation/auto-merge-policy.md`](docs/reconciliation/auto-merge-policy.md)).

## Target repository layout

```text
.claude/
  agents/                 # real read-only reviewer subagents
    <agent-name>.md
  skills/
    _template/            # reference template (ignored by validator)
    <skill-name>/
      SKILL.md
      references/
      assets/
      evals/
        evals.json
        trigger-evals.json   # when trigger overlaps another skill

docs/
  reconciliation/  research/  prompts/  roadmaps/  skills/  templates/
  skill-generation-standard.md
  skills-catalog.md

scripts/
  validate-skills.py
```

## Core rules

- Skills are reusable procedures, not essays. Agents are isolated read-only specialists.
- Build in waves. Do not create the backlog at once (the original 300-skill roadmap, per the D12 standing rule a 300+ target backlog — ship on demand and framework coverage, not count; roadmap = backlog, not a batch command).
- Start with standards, templates, eval convention, and validators (Phase 0).
- Every skill needs `SKILL.md` with clear frontmatter, concise workflow, output format,
  validation checklist, gotchas, stop conditions, and `evals/evals.json`.
- Avoid broad `allowed-tools`; use `disable-model-invocation: true` for side-effect workflows.
- Use read-only exploration first for audits, architecture, code, security, and QA review.
- Treat security, tenant isolation, QA evidence, and verification as first-class requirements.
- Keep product-specific skills out of this reusable foundation.

## Safety note

Claude Code Skills and subagents can influence future code, tests, reviews, and tool usage.
Review every generated skill and agent before trusting it. A reusable skill library is useful
only if it is specific, testable, constrained, maintained, and validated.
