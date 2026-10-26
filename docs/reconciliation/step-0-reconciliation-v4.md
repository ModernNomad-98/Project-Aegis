# Step 0 Reconciliation (v4 canonical)

> **Historical scope — current reading, 2026-09-27.** "Canonical" below names
> the July 2026 choice between two *then-current* generation plans for the
> former `nguyenpv1980-wq/Claude-Skills` repository. It does not make the old
> prompts a current Project Aegis work order. Preserve the numbered decisions
> as historical provenance, including their later appended corrections. For
> current work, first use [AGENTS.md](../../AGENTS.md) to identify the workspace
> role, then the [skills catalog](../skills-catalog.md) and
> [skill authoring standard](../skill-generation-standard.md).
>
> **Later clarification — 2026-10-01.** The reading date above stamps the last
> full-page reading (2026-09-27); material has been appended since. The
> [§6](#6-post-merge-corrections) entry of 2026-09-30 records that pass: a
> full-page audit checked every `path:NNN` / "line NNN" citation in
> [§5](#5-recorded-decisions) against `origin/main` at `2184b54f`. The dated
> corrections of 2026-09-30 and 2026-10-01 were appended inside the affected
> numbered entries rather than in a separate list; the 2026-10-01 one is in
> D60. Those passages are current; the banner above is left as the dated
> scope statement it is.

**How to read this log.** It is still appended as new decisions are made.
Decisions are numbered D1, D2 and so on, oldest first, in
[§5](#5-recorded-decisions). [§6](#6-post-merge-corrections) lists post-merge
corrections newest first; check §6 before relying on a decision. Shorthand used
throughout is expanded here: artificial intelligence (AI), continuous
integration (CI), Developer Certificate of Origin (DCO), end-to-end (E2E),
large language model (LLM), Open Worldwide Application Security Project
(OWASP), pull request (PR), quality assurance (QA), and row-level security
(RLS). Entry-specific shorthand: `cat 01 #27` means item 27 in category 01
([Software Architecture &
Engineering](../skills/01-software-architecture-engineering.md))
of the [300-skill roadmap](../300-repeatable-software-saas-skills-roadmap.md);
ROUTE-002 is the skill contract audit finding for a one-way exclusion, where one
skill routes work away to a neighbour that never names it back; BER means the
Behavioral Eval Runner; WP means work package, the governing delivery unit in
the [BER backlog](../roadmaps/behavioral-eval-runner-backlog.md); OD-1 to OD-3
are owner decisions 1 to 3 in that backlog; AEGIS-APR-007 and similar IDs name
grants in the [owner approval register](../approvals/APPROVAL_REGISTER.md); and
AEGIS-060 is a contract audit finding ID from the
[AEGIS-060+ register](../audits/aegis-060-plus-register.md). "family N" is the
Nth skill family in the README roster. There is no D40 entry; D41 and D42 use
"D40" for a read-only discovery that was never recorded as its own decision.

**Prepared:** 2026-07-06
**Repo:** `nguyenpv1980-wq/Claude-Skills`
**Verified HEAD at reconciliation time:** `5f6f404a8e261c89b8264c3282acd32075f54411` — *"Merge PR #1: 300 repeatable Claude skills roadmap"* on `main`.

This document is the single source of truth for how the two overlapping planning tracks
were reconciled before any skills are generated. It is docs-only. It does not create skills.

---

## 1. Canonicalization

Two planning tracks existed in the repo:

- **v4 track** — [`docs/research/claude-skills-architecture-audit-findings-v4.md`](../research/claude-skills-architecture-audit-findings-v4.md)
  and [`docs/prompts/claude-skills-master-generation-prompts-v4.md`](../prompts/claude-skills-master-generation-prompts-v4.md).
- **Execution-plan track** — [`docs/prompts/senior-principal-claude-skills-execution-plan.md`](../prompts/senior-principal-claude-skills-execution-plan.md).

**Decision D1 — the v4 pair is canonical.** The senior-principal execution plan is
reclassified as **historical/reference input**. Everything unique and still valuable in
it (Phase 8 batch rules, the pre-generation plan table, extra validator checks, several
skill names) is **ported into the v4 pair** so nothing is lost. After this reconciliation,
generation follows the v4 prompts only.

Also historical (unchanged, kept as source inputs):
`docs/research/claude-skills-principal-architecture-findings.md`,
`docs/prompts/master-claude-skills-and-agents-development-prompt.md`,
`docs/prompts/phased-claude-skills-prompts.md`,
`docs/roadmaps/product-agnostic-skill-and-agent-roadmap.md`,
`docs/150-claude-skills-roadmap.md`.

---

## 2. Stale claims removed / corrected

| Stale claim (where) | Reality (2026-07-06) | Action |
|---|---|---|
| "open PR #1", "Continue from or merge PR #1" (v4 audit §2.3, §3 F1, §9) | PR #1 is **merged** into `main` at `5f6f404`. | v4 audit updated to state PR #1 is merged and `main` is the product-agnostic baseline. |
| "`main` is still effectively empty" (execution plan §2.3) | `main` contains the full roadmap, category docs, research, and prompts. | Corrected here; execution plan is now historical so its body is left intact but superseded by this note. |
| Existing work lives on PR branch `docs/300-repeatable-software-saas-skills` (execution plan §2.3) | That branch was fully merged and has been **deleted**. Branch `x` (an older, superseded state) was also fully merged and **deleted**. | Both stale remote branches removed after confirming `git merge-base --is-ancestor` = merged and zero unmerged commits. `main` is the only remaining branch. |

---

## 3. Reconciled phase → executable-skill list (ONE list per phase)

The **v4 phase structure is canonical**. Each row shows the reconciled skill and how the
execution-plan track's names map onto it (merge / move / same). Every skill traces to a
`docs/skills/` category entry where applicable.

### Phase 0 — Foundation (P0) — *this phase*
Standard, templates, eval schema, catalog, validator, README, real subagents, `_template`.
No skills generated. (Both tracks agree.)

### Phase 1 — AI engineering operating-discipline pack (P0)
**Canonical = v4's 8.** The execution plan's Phase 1 mixed operating-discipline with
architecture; the architecture skills are **moved to Phase 2**.

| # | Reconciled skill | Roadmap ref (cat 08) | Merge / move note |
|---|---|---|---|
| 1 | `agent-startup-context-gate` | #262 | same in both tracks |
| 2 | `source-of-truth-reconciler` | #269 | absorbs execution-plan `no-silent-assumptions-protocol` (#270) assumption-surfacing behavior |
| 3 | `change-classification-gate` | #264 | absorbs execution-plan `phase-locked-execution` (#263) scope-lock behavior |
| 4 | `human-approval-boundary` | #265 | new canonical name (v4); also carries the "stop when unclear" half of #270 |
| 5 | `reviewable-diff-discipline` | #271 | absorbs execution-plan `exact-file-staging` intent (#272) |
| 6 | `ai-closeout-reporter` | #274 (+ #267, #273) | same intent both tracks; #267 Prompt-to-Diff Traceability and #273 AI Work Evidence Pack merged into `ai-closeout-reporter` (D69, 2026-09-28) as its per-deliverable trace |
| 7 | `agent-failure-recovery` | #275 | v4 addition |
| 8 | `agent-instruction-consolidator` | #276 | #276 Agent Instruction Consolidation |

**Moved out of Phase 1 → Phase 2:** `adr-writer`, `system-context-mapper`, `domain-modeler`,
`bounded-context-identifier`, `architecture-designer`, `dependency-direction-guard`,
`refactor-safety-planner`.

### Phase 2 — Core architecture & engineering (P0)
**Canonical = v4's 10:** `domain-modeler`, `architecture-designer`, `adr-writer`,
`docs-first-implementer`, `tdd-engineer`, `systematic-debugger`, `code-reviewer`,
`code-simplifier`, `principal-code-analyst`, `full-codebase-auditor`.

Merges/moves from the execution plan: `grill-with-docs` **→ merged into** `docs-first-implementer`
(same skill, v4 name wins). Architecture skills moved from execution-plan Phase 1 land here.
Execution-plan Phase 2 extras (`api-contract-designer` — **✅ built (D79, 2026-10-10) as the #9 extension of `api-event-architect`**,
`idempotency-first-designer` — **✅ built (D79, 2026-10-10) as the #17/#144 extension of `command-gateway-architect` + `product-spec-writer`**,
`validation-boundary-designer`, `observability-by-design`, `operational-runbook-author` —
**dropped (D80, 2026-10-10)**: covered by `incident-response-runbook`,
`rollback-runbook-author`, `data-migration-runbook-author`,
`gated-deployment-prompt-template`, `onboarding-doc-designer`) and
the moved arch skills (`system-context-mapper` — **dropped (D80, 2026-10-10)**:
covered by `architecture-designer` + `threat-modeler`,
`bounded-context-identifier` — **dropped (D80, 2026-10-10)**: covered by
`domain-modeler` step 4,
`dependency-direction-guard`, `refactor-safety-planner`) are **reconciled into the Phase 2
expansion backlog** (built in Phase 8 batches, not the initial Phase 2 pass), keeping the
first pass to v4's 10 for quality.

### Phase 3 — SaaS & tenant isolation (P0/P1)
**Canonical = v4's 9:** `saas-platform-architect`, `tenant-modeler`, `tenant-isolation-reviewer`,
`multi-tenant-data-architect`, `authorization-matrix-designer`, `plan-entitlement-architect`,
`audit-log-architect`, `saas-cost-architect`, `api-event-architect`.
Execution-plan equivalents merged: `rls-policy-author`/`rls-negative-test-designer` →
**deferred to Phase 4** (RLS pack) to avoid duplication; `tenant-provisioning-designer` —
**✅ built (D81, 2026-10-10)**, `membership-invitation-designer` —
**✅ built (D81, 2026-10-10)**, `role-permission-architect` — **✅ built (D78, 2026-10-10) as the #59 extension of `authorization-matrix-designer`**, `security-impact-note-author`
→ Phase 3 expansion backlog.

### Phase 4 — Security, RLS & supply chain (P0/P1)
**Canonical = v4's 9:** `threat-modeler`, `appsec-implementer`, `multi-tenant-security-tester`,
`rls-policy-auditor`, `secrets-identity-hardener`, `supply-chain-security-reviewer`,
`security-pr-reviewer`, `secure-migration-reviewer`, `static-analysis-reviewer`.
Execution-plan `rls-policy-author` + `rls-negative-test-designer` **→ merged into**
`rls-policy-auditor` (which per v4 includes the negative-test plan).

#### OWASP Top 10 (Web Application Security) coverage map

Gap audit (D8) of the nine **shipped** Phase 4 skills against the **OWASP Top 10:2025** for
web application security, A01:2025–A10:2025. Source: <https://owasp.org/www-project-top-ten/>
(verified 2026-07-06 — the project page states the current released edition is the 2025 list,
published at <https://owasp.org/Top10/2025/>). This map records coverage of already-shipped
work and tracks gaps as Phase 8 backlog items; it creates no skills and changes no phase list.

| OWASP Top 10:2025 (web app) | Covering shipped Phase 4 skill(s) | Status |
|---|---|---|
| A01:2025 Broken Access Control | `multi-tenant-security-tester` (IDOR, cross-tenant, privilege escalation), `rls-policy-auditor`, `security-pr-reviewer` (object-level/tenant-scope checks, SSRF hunting in diffs), `appsec-implementer` (authz checks, SSRF/redirect allowlists), `threat-modeler` | covered |
| A02:2025 Security Misconfiguration | `secure-migration-reviewer` (unsafe defaults, over-broad GRANTs, RLS-enablement gaps), `rls-policy-auditor` (deny-by-default posture), `secrets-identity-hardener` (env classification, client-bundle exposure) | partial |
| A03:2025 Software Supply Chain Failures | `supply-chain-security-reviewer` (dependencies, lockfiles, CI/CD, artifact provenance; extended to artificial intelligence (AI) supply chain per D6/LLM03) | covered |
| A04:2025 Cryptographic Failures | `secrets-identity-hardener` (key/credential custody, rotation, exposure), `static-analysis-reviewer` (triage of weak-crypto findings) | partial |
| A05:2025 Injection | `security-pr-reviewer` (injection in diffs), `appsec-implementer` (parameterized queries, input validation, output encoding), `static-analysis-reviewer` (SAST injection triage) | covered |
| A06:2025 Insecure Design | `threat-modeler` (trust boundaries, STRIDE enumeration, abuse cases, mitigations each with a negative test); `appsec-implementer` builds the decided controls | covered |
| A07:2025 Authentication Failures | `secrets-identity-hardener` (session/token expiry, refresh, storage flags, revocation), `security-pr-reviewer` (authn gaps in diffs), `threat-modeler` (auth is a named design surface) | covered |
| A08:2025 Software or Data Integrity Failures | `supply-chain-security-reviewer` (CI/CD integrity, unpinned Actions, artifact provenance), `security-pr-reviewer` (unsafe deserialization) | covered |
| A09:2025 Security Logging and Alerting Failures | `security-logging-alerting-architect` (detection coverage, alerting rules, response wiring — built from the Phase 8 backlog, D28) | covered |
| A10:2025 Mishandling of Exceptional Conditions | `error-handling-security-reviewer` (fail-closed defaults, error-path authorization, exception-driven bypass, leak-free error responses — built from the Phase 8 backlog, D28) | covered |

- **Rubric:** *covered* = the category's core risk is named in at least one shipped Phase 4
  skill contract; *partial* = only a slice is named (residue listed below); *gap* = no
  Phase 4 skill owns it. Honest residue beats optimistic green.
- **A01 / SSRF:** the 2025 edition folds SSRF (A10:2021) into Broken Access Control. SSRF is
  covered at three points (`threat-modeler` enumeration, `appsec-implementer` allowlists,
  `security-pr-reviewer` diff hunting), so no standalone `ssrf-defense-reviewer` backlog item
  is opened.
- **A02 residue:** application/platform configuration — security headers, CORS, XML-parser
  hardening (XXE-class), default accounts, cloud posture — has no Phase 4 owner. Cloud
  posture is owed to Phase 6 (`iac-reviewer`, plus `cloud-security-baseline-reviewer`, built
  by D71 on 2026-09-28 from the Phase 6 expansion backlog); the app-config slice remains
  open residue.
- **A04 residue:** encryption-in-transit/at-rest design and algorithm/library review are
  unowned; coverage today is custody of keys/credentials plus SAST-finding triage only.
- **A09/A10 gaps: CLOSED (D28, 2026-07-08).** Both categories now have an owning skill,
  built from the Phase 8 backlog items D8 recorded: `security-logging-alerting-architect`
  (A09) and `error-handling-security-reviewer` (A10). They are Phase-8-backlog builds, not
  additions to the Phase 4 list — the map cells cite them as D28 builds. Phase 3
  `audit-log-architect` remains the RECORD layer that A09 detection consumes (it records,
  but does not detect or alert).
- **Framework distinction:** this is a third OWASP framework, distinct from the OWASP LLM
  Top 10 (Phase 7 map below, D6) and from the separate OWASP Agentic framework (Phase 7.5
  map below, D7).

### Phase 5 — QA, E2E, manual QA & evidence (P0/P1)
**Canonical = v4's 13:** `qa-strategy-architect`, `test-plan-designer`, `test-coverage-mapper`,
`qa-automation-architect`, `playwright-e2e-engineer`, `clickthrough-test-engineer`,
`manual-test-case-creator`, `screenshot-evidence-planner`, `vitest-unit-component-engineer`,
`vite-build-qa-engineer`, `flaky-test-detective`, `test-data-architect`, `regression-suite-curator`.
Execution-plan extras merged: `acceptance-criteria-tester`,
`e2e-test-architect` — **dropped (D80, 2026-10-10)**: covered by the
`qa-strategy-architect` + `test-plan-designer` + `qa-automation-architect` +
`regression-suite-curator` + `test-data-architect` + `playwright-e2e-engineer`
composition,
`qa-closeout-reporter` — **dropped (D80, 2026-10-10)**: covered by
`ai-closeout-reporter` + `release-readiness-reviewer`
→ Phase 5 expansion backlog (`qa-closeout-reporter` overlaps
`ai-closeout-reporter` + `screenshot-evidence-planner`; keep as backlog to avoid trigger overlap).

> Note: execution-plan ordering placed QA at Phase 4 and audit/troubleshooting at Phase 5.
> v4 ordering (Security at 4, QA at 5) is canonical. Whole-codebase audit / troubleshooting
> skills (`full-codebase-auditor`, `principal-code-analyst`, `senior-troubleshooter`,
> `code-quality-auditor`, `dependency-license-audit-reviewer`, `code-audit-orchestrator`)
> are absorbed into v4 Phase 2 (`full-codebase-auditor`, `principal-code-analyst`) with the
> remainder in the Phase 2/5 expansion backlog.

#### Phase 5 QA expansion backlog — prioritized (D10)

Gap audit (D10, 2026-07-07) of roadmap category 06
([`docs/skills/06-qa-test-engineering.md`](../skills/06-qa-test-engineering.md), scoped to
items #181–#230) against the **16 shipped Phase 5 skills** — the 13 canonical above plus
`integration-test-designer` (#184), `api-contract-test-designer` (#185), and
`accessibility-test-harness` (#204), pulled forward at ship time. Uncovered items land in
three build tiers; **every entry started as (candidate — not built)**, and each row now
carries its own built / merged / dropped marker once a later decision delivers it (D23,
D68). This prioritizes the backlog
only: no skills created, no phases renumbered, validator targets unchanged.

**Already covered — mapped once, not re-listed as candidates:**

| Roadmap # (cat 06) | Owned by shipped skill |
|---|---|
| #181 Test Strategy Authoring | `qa-strategy-architect` (Phase 5) |
| #182 Risk-Based Validation Matrix | `change-classification-gate` (Phase 1) — validation-tier selection lives cross-phase |
| #183 Unit Test Design | `vitest-unit-component-engineer` (Phase 5) |
| #184 Integration Test Design | `integration-test-designer` (Phase 5, pulled forward) |
| #185 Contract Test Design | `api-contract-test-designer` (Phase 5, pulled forward) |
| #186 RLS Test Harness Design | `multi-tenant-security-tester` + `rls-policy-auditor` (Phase 4) — RLS testing lives cross-phase |
| #187 E2E Journey Design | `playwright-e2e-engineer` (Phase 5) |
| #190 Regression-First Bug Fixing | `tdd-engineer` (Phase 2), with `systematic-debugger` (Phase 2) and `regression-suite-curator` (Phase 5) as neighbors — candidate dropped by D68 (2026-09-28) |
| #196 Test Data Isolation / #197 Seed Fixture Governance | `test-data-architect` (Phase 5) |
| #204 Accessibility Test Harness | `accessibility-test-harness` (Phase 5, pulled forward) |
| #209 Flake Detection / #210 Flake Quarantine Governance | `flaky-test-detective` (Phase 5) |
| #221 Manual QA Script Authoring | `manual-test-case-creator` (Phase 5) |
| #222 Clickthrough Testing Protocol | `clickthrough-test-engineer` (Phase 5) |
| #223 Screenshot Evidence Capture | `screenshot-evidence-planner` (Phase 5) |
| #227 Definition of Done Review | `release-readiness-reviewer` (Phase 6), with `ai-closeout-reporter` (Phase 1) and `agent-governance-audit` (Phase 1.5) — split from `acceptance-criteria-tester` by D68 (2026-09-28) |

**Tier 1 — build first when the QA expansion runs** (uncovered roadmap P0s plus the
performance/load headline):

| Candidate *(started as candidate — not built; per-row status below)* | Roadmap ref (cat 06) | Note |
|---|---|---|
| `performance-test-harness` + `load-test-planner` — **✅ both built (D23, 2026-07-07)** | #205 (P1) + #206 (P2) | **Headline gap — now closed:** load/render/query/API/edge-function/background-job performance measurement plus realistic traffic/tenant/data-volume load planning — the largest uncovered risk for a multi-tenant SaaS (noisy neighbors, per-tenant degradation). Built as TWO skills per the D23 pre-generation plan table (instrument vs traffic plan — the sibling seam is pinned in both trigger-evals). Pre-release counterpart to Phase 6 `slo-reliability-architect` (targets/alerting); the designs-vs-measures seam against D12.3 is pinned from both sides. |
| `regression-first-bug-fixer` — **dropped (D68, 2026-09-28)**: covered by `tdd-engineer` (see Already covered above; D68 corrects this row's note) | #190 (P0) | Failing test that reproduces the bug BEFORE the fix. `regression-suite-curator` cites #190 but owns suite membership, not the fix workflow; `tdd-engineer` owns new behavior, not bug reproduction. |
| `negative-path-test-mapper` — **merged into `test-plan-designer` (D68, 2026-09-28)**; no separate skill | #192 (P0) | Now a per-surface negative-path matrix in `test-plan-designer` workflow step 2, its output and its checklist. Original scope: systematic unauthorized/invalid/expired/missing/duplicated/conflicting/out-of-order enumeration per surface. `test-plan-designer`/`test-coverage-mapper` cite #192 as a source but own planning/audit; security negatives stay with Phase 4 `multi-tenant-security-tester`. |
| `test-tenant-provisioner` — **✅ built (D68, 2026-09-28)** | #198 (P0) | Repeatable test tenants/users for auth, RLS, integration, and E2E runs. `test-data-architect` (source range #196–#199) owns the data catalog; provisioning the tenants/users themselves is unowned. (broadened per report P12: test-row marker convention with never-mutate-unmarked rule, validate-only vs apply modes, env-var-name-only credentials, backup-gated capability grants with inline rollback, prod-safe static lint of QA automation) |
| `ci-failure-classifier` — **✅ built (D68, 2026-09-28)** | #214 + #215 (merged; both P0) | ONE skill: hidden runtime-marker scan (console errors, unhandled rejections, skipped tests, auth failures) + failure classification (product bug / test bug / missing secret / timeout-only / infra / skipped runtime). `flaky-test-detective` owns intermittence root-cause; this owns the every-run CI verdict. (per report P14: duration as first-class evidence; TIMEOUT_FAILURE as a distinct class never conflated with regressions; resume-don't-rerun after timeout-only interruptions; no masking real failures by raising timeouts) |
| `acceptance-criteria-tester` — **built as `acceptance-criteria-reviewer`, narrowed to #226 (D68, 2026-09-28)**; #227 is covered (see Already covered above) | #226 + #227 (merged; both P0) | Testability/completeness/ambiguity review of acceptance criteria + definition-of-done check. **Already deferred once** (execution-plan extra → this backlog, note above); the deferral stands — it builds in this tier, not before. |

**Tier 2 — second wave** (roadmap P1 hardening, plus #203 promoted because UI drift is
otherwise invisible to the shipped suite):

| Candidate *(started as candidate — not built; per-row status below)* | Roadmap ref (cat 06) | Note |
|---|---|---|
| `visual-regression-test-designer` — **✅ built (D75, 2026-10-09)** | #203 (P2) | Critical UI states with stable data, deterministic viewport, reviewable diffs. |
| `role-based-qa-matrix` — **✅ built (D76, 2026-10-10)** as `role-coverage-test-designer` | #229 (P1) | Behavior across anonymous/member/manager/admin/owner/support/platform roles; QA counterpart to Phase 3 `authorization-matrix-designer`. |
| `mobile-viewport-qa` — **✅ built (D75, 2026-10-09)** as `mobile-journey-test-designer` | #230 (P1) | Critical journeys on mobile breakpoints, touch interactions, dialogs, navigation. |
| `exploratory-testing-charter` — **✅ built (D75, 2026-10-09)** as `exploratory-charter-designer` | #228 (P1) | Mission/risks/personas/data/paths/timebox charters for exploratory passes. |
| `mock-strategy-designer` — **dropped (D80, 2026-10-10)**: covered by `integration-test-designer` (boundary map + fake pinning), `vitest-unit-component-engineer` (owned seams) and `api-contract-test-designer` (fake-fidelity re-validation) — fresh full-body review, no residual slice | #200 + #201 (merged; both P1) | ONE skill: mock/fake/stub/adapter/recording/live selection + test-double contract review keeping doubles aligned with real provider/DB behavior (`api-contract-test-designer`'s fake-fidelity check is the contract-layer slice of this). |
| `ci-shard-parallel-isolation` — **dropped (D80, 2026-10-10)**: covered by `sharded-validation-with-resume` (shard map/resume) and `qa-automation-architect` (per-worker isolation + CI sharding plan) — fresh full-body review, no residual slice | #211 + #212 (merged; both P1) | ONE skill: shard design (stable shards, run IDs, artifacts) + parallel isolation (no shared users/tenants/records/ports/browser state/queues). Extends `qa-automation-architect`'s blueprint into enforceable rules. |

**Tier 3 — specialized, defer** (all roadmap P2; build on demand only):

| Candidate *(started as candidate — not built; per-row status below)* | Roadmap ref (cat 06) | Note |
|---|---|---|
| `property-based-test-designer` — **✅ built (D77, 2026-10-10)** | #194 (P2) | Generated input combinations for validation, parsing, math, state, transformations. |
| `mutation-testing-reviewer` — **✅ built (D78, 2026-10-10)** as the #195 mutation-report extension of `test-coverage-mapper` | #195 (P2) | Mutation thinking to expose tests that pass without proving behavior. |
| `soak-test-planner` — **dropped (D80, 2026-10-10)**: covered by `load-test-planner` | #207 (P2) | Long-duration runs for leaks, queue buildup, token expiry, degradation. |
| `chaos-test-planner` — **dropped (D80, 2026-10-10)**: covered by `resilience-architecture-reviewer` (fault-injection/game-day plans) | #208 (P2) | Safe injection of service failures, timeouts, retries, partial outages. |

- **Build timing (D10):** after the core phases (7, 7.5) or on demand; nothing here is
  built now.
- Category-06 items neither tiered nor mapped above (#188, #189, #191, #193, #199, #202,
  #213, #216–#220, #224, #225), plus the category tail outside this audit's #181–#230 scope
  (#231–#235), stay unprioritized backlog in the Phase 8 batch flow (D5). Several are already
  partially absorbed via shipped catalog source mappings (#191 → `test-coverage-mapper`,
  #199 → `test-data-architect`, #217 → `vite-build-qa-engineer`,
   #213 → `qa-automation-architect` (D78)) and were counted neither as
  gaps nor as coverage. The execution-plan extras note above (`e2e-test-architect`,
  `qa-closeout-reporter`) is closed by D80 (2026-10-10) — both names are
  marked dropped above.

### Phase 6 — Cloud, DevOps, reliability & release (P1)
**Canonical = v4's 10:** `cloud-architecture-decider`, `azure-saas-architect`, `aws-saas-architect`,
`iac-reviewer`, `ci-pipeline-architect`, `release-readiness-reviewer`, `rollback-runbook-author`,
`observability-operator`, `slo-reliability-architect`, `incident-response-runbook`.
Execution-plan extras (`cloud-security-baseline-reviewer` — **✅ built (D71, 2026-09-28)**, `resilience-architecture-reviewer`,
`rollback-strategy-designer`→merged into `rollback-runbook-author`, `migration-deployment-runbook` (#254)→merged into `data-migration-runbook-author` (D71, 2026-09-28; no separate skill),
`environment-parity-reviewer`, `database-backup-verifier`) → Phase 6 expansion backlog.
`resilience-architecture-reviewer` — **built (D71, 2026-09-28)**, auto-invocable, review
only; it also owns the D30 pull-forward note below (circuit breakers, bulkheads,
timeouts, graceful degradation).

`database-backup-verifier` (category 07 #253, P0) — **✅ built (D71, 2026-09-28)**, manual-only:
read-only backup evidence by default, and restore drills only into a named non-production scratch
target after approval of the exact plan with its estimated cost; it left the expansion backlog.

`environment-parity-reviewer` — **✅ built (D71, 2026-09-28)**, auto-invocable: category 07
#244 Environment Parity Review, with #246 Runtime Configuration Validation folded in as its
required-configuration manifest and startup validation specification. Runtime health checks
(#247) stay with `observability-operator` and `slo-reliability-architect`; IaC-to-runtime
drift (#245) stays with `iac-reviewer`.

### Phase 7 — AI security & LLM systems (P1)
**Canonical = 14 — v4's 10 + 4 OWASP-gap additions (D6):** `ai-threat-modeler`,
`prompt-injection-defender`, `rag-security-architect`, `agent-tool-safety-guard`,
`llm-output-safety-reviewer`, `ai-evaluation-harness`, `ai-cost-guardrail-designer`,
`ai-governance-risk-reviewer`, `ai-router-architect`, `structured-output-validator`,
`sensitive-disclosure-guard` *(NEW)*, `model-poisoning-reviewer` *(NEW)*,
`system-prompt-leakage-reviewer` *(NEW)*, `ai-misinformation-guard` *(NEW)*.
Execution-plan extras (`ai-provider-adapter-designer`→merged into `ai-router-architect` (D70, 2026-09-28), `prompt-contract-designer` (#283)→merged into
`model-context-designer` as its prompt contract record (D70, 2026-09-28),
`ai-human-in-the-loop-designer`→built (D70, 2026-09-28), `ai-autonomy-boundary-designer`→merged into
`ai-human-in-the-loop-designer` (D70, 2026-09-28), `ai-security-test-harness`→merged
into `ai-evaluation-harness`, `ai-feature-kill-switch-designer`→dropped (D70, 2026-09-28)) → Phase 7 expansion backlog.

**Expansion backlog disposition (D70, 2026-09-28)** — roadmap rows in category 09:

| Roadmap # (cat 09) | Disposition |
|---|---|
| #285 AI Human-in-the-Loop Design | built as `ai-human-in-the-loop-designer` (Phase 7) by D70 (2026-09-28) |
| #286 AI Advisory-Only Pattern | merged into `ai-human-in-the-loop-designer` (its advisory-only default) by D70 (2026-09-28) |
| #287 AI Autonomy Boundary Design | candidate `ai-autonomy-boundary-designer` merged into `ai-human-in-the-loop-designer` as its first workflow step (AUTONOMOUS / CONFIRM / FORBIDDEN) by D70 (2026-09-28) |
| #299 AI Feature Kill Switch | candidate `ai-feature-kill-switch-designer` dropped by D70 (2026-09-28): covered by `ai-router-architect` (workflow step 8), with `ai-cost-guardrail-designer` (spend switch), `agent-containment-reviewer` (agent and fleet switches), `feature-flag-architect` and `feature-flag-rollout-strategist` |

#### OWASP LLM Top 10 (2025) coverage map

> **Historical edition.** D65 (2026-09-26) re-anchored Phase 7 to the OWASP Top
> 10 for LLM Applications 2026; this table keeps the 2025 IDs as written. See D65
> in [§5](#5-recorded-decisions).

Phase 7 is anchored to the **OWASP Top 10 for LLM Applications (2025)**, LLM01:2025–LLM10:2025.
Source: <https://genai.owasp.org/llm-top-10/> (verified 2026-07-06). This banks the coverage
target now; the skills themselves are still built at Phase 7, not before.

| OWASP LLM Top 10 (2025) | Covering Phase 7 skill(s) | Status |
|---|---|---|
| LLM01:2025 Prompt Injection | `prompt-injection-defender` | covered |
| LLM02:2025 Sensitive Information Disclosure | `sensitive-disclosure-guard` *(NEW)* | gap |
| LLM03:2025 Supply Chain | Phase 4 `supply-chain-security-reviewer`, **extended** to cover models, datasets, and fine-tuning adapters | extend-existing |
| LLM04:2025 Data and Model Poisoning | `model-poisoning-reviewer` *(NEW)* | gap |
| LLM05:2025 Improper Output Handling | `llm-output-safety-reviewer` + `structured-output-validator` | covered |
| LLM06:2025 Excessive Agency | `agent-tool-safety-guard` | covered |
| LLM07:2025 System Prompt Leakage | `system-prompt-leakage-reviewer` *(NEW)* | gap |
| LLM08:2025 Vector and Embedding Weaknesses | `rag-security-architect`, including cross-tenant vector-store access control | covered |
| LLM09:2025 Misinformation | `ai-misinformation-guard` *(NEW)* — grounding, citation, uncertainty signaling | gap |
| LLM10:2025 Unbounded Consumption | `ai-cost-guardrail-designer`, **extended** to cover denial-of-service and denial-of-wallet | extend-existing |

- `system-prompt-leakage-reviewer` must encode that **system prompts are NOT security
  controls**; enforcement must be deterministic and live outside the LLM.
- `ai-threat-modeler`, `ai-governance-risk-reviewer`, `ai-router-architect`, and
  `ai-evaluation-harness` are cross-cutting glue across all ten categories rather than
  mapped one-to-one.
- The **OWASP Top 10 for Agentic Applications is a separate framework** that the
  LLM Top 10 does not cover; agentic-specific skills are anchored in **Phase 7.5 below**
  (D7) — no longer a Phase 8 follow-on candidate — and are not part of this Phase 7 expansion.

### Phase 7.5 — Agentic AI security (OWASP Agentic Top 10) (P1)

**NEW phase (D7): canonical = 6 new skills + 3 extensions of existing skills.** Anchored to
the **OWASP Top 10 for Agentic Applications (2026)**, ASI01–ASI10. Source:
<https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/> (all ten
designations and names verified 2026-07-06 against the published framework document behind
that page). Rationale (D7): agentic risk builds on top of LLM risk (Phase 7, D6), so this
pack runs immediately after Phase 7; it is too central to this repo's agentic workflows to
defer into the generic Phase 8 backlog. Skills are **built at Phase 7.5, not now** — like
the Phase 7 map above, this banks the coverage target only; today's shipped validator
target (52 skills) is unchanged.

| OWASP Agentic Top 10 (2026) | Covering skill | Status |
|---|---|---|
| ASI01 Agent Goal Hijack | `agent-goal-hijack-defender` *(NEW)* — goal/plan integrity across multi-step runs; builds on `prompt-injection-defender` (LLM01), which owns the injection vector | new |
| ASI02 Tool Misuse and Exploitation | Phase 7 `agent-tool-safety-guard`, **extended** — per-tool authorization, argument validation, side-effect limits, tool-chain abuse paths | extend-existing |
| ASI03 Identity and Privilege Abuse | `agent-identity-privilege-reviewer` *(NEW)* — agent identities, scoped credentials, delegation chains, confused-deputy paths; complements Phase 4 `secrets-identity-hardener` (credential custody) | new |
| ASI04 Agentic Supply Chain Vulnerabilities | Phase 4 `supply-chain-security-reviewer`, **extended** again (after D6/LLM03) to MCP servers and manifests, tool/skill registries, plugin packages, A2A dependencies | extend-existing |
| ASI05 Unexpected Code Execution (RCE) | Phase 7 `llm-output-safety-reviewer` + `agent-tool-safety-guard`, **extended** — execution of agent-generated code, sandbox boundaries, natural-language-driven execution paths | extend-existing |
| ASI06 Memory & Context Poisoning | `memory-context-poisoning-reviewer` *(NEW)* — persistent corruption of stored context/long-term memory, cross-session and cross-tenant contamination; distinct from `model-poisoning-reviewer` (training-time, LLM04) and `rag-security-architect` (retrieval stores, LLM08) | new |
| ASI07 Insecure Inter-Agent Communication | `inter-agent-comms-reviewer` *(NEW)* — authn, integrity, and confidentiality of agent-to-agent messages (MCP/A2A transports); spoofing and replay | new |
| ASI08 Cascading Failures | `agent-containment-reviewer` *(NEW — merged, also owns ASI10)* — fault propagation across agent networks: blast-radius isolation, circuit breakers, checkpoints | new |
| ASI09 Human-Agent Trust Exploitation | `human-agent-trust-reviewer` *(NEW)* — consent fatigue, deceptive or over-polished justifications that mislead human approvers; adversarial counterpart to Phase 1 `human-approval-boundary` | new |
| ASI10 Rogue Agents | `agent-containment-reviewer` *(NEW — merged, same skill as ASI08)* — behavioral-drift detection, agent inventory/lifecycle governance, kill switches | new |

- **Merged overlaps — 6 new skills, not 7+:** ASI08 and ASI10 collapse into one
  `agent-containment-reviewer`. The source's own seam — ASI08 is fault *propagation* across
  interconnected agents, ASI10 is the "containment gap" once behavioral drift begins — makes
  them two halves of a single containment review (same inputs: agent topology, autonomy
  boundaries, kill/rollback paths). It also covers the agentic slice of the Phase 7
  expansion-backlog candidate `ai-feature-kill-switch-designer`. Nothing else collapses: the
  source explicitly distinguishes ASI01 vs ASI06 vs ASI10 (direct goal alteration vs
  stored-memory corruption vs autonomous drift without active attacker control).
- **Coverage counts:** 7 of 10 categories land on new skills (6 skills after the merge);
  3 of 10 are extensions (ASI02, ASI05 extend Phase 7 skills; ASI04 extends Phase 4
  `supply-chain-security-reviewer`); 0 are fully covered by already-planned work.
- **Framework relationship:** the Agentic Top 10 **extends — does not replace — the LLM
  Top 10 (D6)**: the source states agentic apps "will not exist in isolation and will be part
  of developing an LLM App," and its entries cross-reference LLM categories (e.g. ASI09
  builds on LLM06 Excessive Agency and can be caused by LLM01 Prompt Injection). Agent
  systems inherit every Phase 7 LLM-side risk; Phase 7.5 adds the autonomy, tool, identity,
  memory, and multi-agent risks layered on top.

### Compliance & Governance batch (ISO 27001:2022 + ISO 42001:2023 + SOC 2 Type 2)

**SHIPPED batch (D9) — banked 2026-07-06 targeted AFTER Phase 7; implemented 2026-07-07 and
merged via PR #21 (merge commit `2df96f1`) — all 9 skills.** This is
certification/attestation readiness for an AI SaaS vendor selling into US enterprise and EU
markets: SOC 2 is the de-facto US enterprise procurement ask, ISO 27001 is pulled through EU
supply chains by NIS2 obligations on customers, and ISO 42001 is emerging in EU public
procurement for AI vendors (vendor-market rationale, not a standards claim). **Distinct from
Phase 1.5** (operational agent governance — how agents behave inside the SDLC) **and from the
OWASP maps (D6/D7/D8)** (technical attack-surface coverage): this batch maps controls that
largely already exist and produces auditor-grade evidence on top of them.

**The frameworks, from fetched sources (fetched 2026-07-06; full source list + per-item
verification status in D9):**

- **ISO/IEC 27001:2022** — *Information security, cybersecurity and privacy protection —
  Information security management systems — Requirements*, third edition, 2022-10. A
  **certifiable ISMS** standard: management-system clauses 4–10 (Context of the organization,
  Leadership, Planning, Support, Operation, Performance evaluation, Improvement — verified
  against the standard's own TOC) plus **Annex A (normative) "Information security controls
  reference"**, applied through the 6.1.3 risk-treatment process (Statement of Applicability).
  Annex A groups controls into four themes — **A.5 Organizational, A.6 People, A.7 Physical,
  A.8 Technological** — totalling **93 controls (37/8/14/34)**; *counts are from secondary
  controls references, NOT verified against the paywalled Annex A table itself — verify before
  citing.* **ISO/IEC 27001:2022/Amd 1:2024 "Climate action changes"** amends clauses 4.1/4.2
  (the organization must determine whether climate change is relevant; interested parties can
  have climate-related requirements); *amendment existence and title verified from the ISO
  catalog entry; the exact inserted sentences are from secondary summaries.*
- **ISO/IEC 42001:2023** — *Information technology — Artificial intelligence — Management
  system*, first edition, 2023-12. A **certifiable AIMS** standard with the same harmonized
  clauses 4–10 (verified against the standard's TOC), adding AI-specific machinery: AI risk
  assessment (6.1.2/8.2), AI risk treatment (6.1.3/8.3), and **AI system impact assessment
  (6.1.4/8.4)** — plus **Annex A (normative) "Reference control objectives and controls"**,
  Annex B (normative, implementation guidance for AI controls), Annex C/D (informative).
  *Annex A control counts are deliberately NOT stated here: secondary sources conflict ("38
  controls / 9 objectives" vs "42 objectives"); verify against the standard text before using
  any number.*
- **SOC 2** — an **AICPA attestation (a CPA's examination), NOT a certification** — 27001/42001
  certify; SOC 2 attests. It reports on controls at a service organization under the **Trust
  Services Criteria** (2017 TSC with revised Points of Focus 2022, issued by the AICPA
  Assurance Services Executive Committee) across five categories: **Security, Availability,
  Processing Integrity, Confidentiality, Privacy**. **Type 1** = fairness of the system
  description + suitability of control **design as of a specified date**; **Type 2** = the same
  **plus operating effectiveness over a period**. *The five categories, ASEC authorship, and
  "examination" language are verified on AICPA pages; the Type 1/Type 2 definitions and
  "Security is the required common-criteria baseline, the other four are scoped per engagement"
  come from CPA-firm sources — AICPA's fetchable pages do not define them; the defining text is
  the paywalled AICPA SOC 2 guide.*
- **Companion, not a certification target: NIST AI RMF 1.0** (released 2023-01-26; voluntary;
  under revision per NIST). Core = **four functions: GOVERN, MAP, MEASURE, MANAGE**, with
  GOVERN "a cross-cutting function that is infused throughout AI risk management" (verified on
  NIST AIRC). Generative AI Profile NIST-AI-600-1 (2024-07-26). Pairs with 42001 as the risk
  method underneath the management system.

**Architecture (D9): ONE shared control foundation + framework projections + a crosswalk — NOT
three parallel skill sets.** Published crosswalks put cross-framework control overlap at
roughly **60–80%** (industry estimate, not a standard-derived figure): the same access-control,
crypto, change-management, logging, incident-response, vendor-management, and risk-assessment
controls satisfy 27001 Annex A, SOC 2 TSC, and much of 42001's non-AI-specific surface.
Consequence: **build TSC criteria and Annex A mapping together, not sequentially** — the
foundation is written once and projected per framework. The 9 skills below are already the
merged set: evidence collection is ONE skill across all three frameworks (not per-framework),
gap auditing is ONE parameterized skill, and the SoA author serves both ISO standards.

| Skill *(all: implemented — PR #21, 2026-07-07)* | Layer | Purpose |
|---|---|---|
| [`compliance-control-foundation`](../../.claude/skills/compliance-control-foundation/SKILL.md) | Shared foundation | One framework-agnostic common control set — access control, cryptography, change management, logging/monitoring, incident response, vendor management, risk assessment — written once, consumed by the projections |
| [`compliance-evidence-collector`](../../.claude/skills/compliance-evidence-collector/SKILL.md) | Shared foundation | Operating-effectiveness evidence **over time** (cadence, retention, audit-window coverage) — SOC 2 Type 2's core demand, reused for ISO surveillance audits |
| [`statement-of-applicability-author`](../../.claude/skills/statement-of-applicability-author/SKILL.md) | Shared foundation | The ISO-mandatory SoA — per-control inclusion/exclusion justification tied to the 6.1.3 risk-treatment process; the largest net-new ISO artifact SOC 2 lacks |
| [`iso-27001-isms-architect`](../../.claude/skills/iso-27001-isms-architect/SKILL.md) | Framework projection | ISMS per clauses 4–10; four-theme Annex A control selection; internal audit + management review cadence; Amd 1:2024 climate-context check |
| [`iso-42001-aims-architect`](../../.claude/skills/iso-42001-aims-architect/SKILL.md) | Framework projection | AIMS per clauses 4–10; AI risk assessment / treatment and AI system impact assessment; Annex A control-objective selection |
| [`soc2-trust-criteria-mapper`](../../.claude/skills/soc2-trust-criteria-mapper/SKILL.md) | Framework projection | TSC scoping — Security baseline plus which optional categories to attest; Type 1 vs Type 2 decision and audit-window planning |
| [`multi-framework-crosswalk`](../../.claude/skills/multi-framework-crosswalk/SKILL.md) | Cross-cutting | One control → 27001 Annex A + SOC 2 TSC + 42001 Annex A (+ AI RMF function) — the do-the-work-once engine between foundation and projections |
| [`compliance-gap-auditor`](../../.claude/skills/compliance-gap-auditor/SKILL.md) | Cross-cutting | Current state vs chosen framework(s) → prioritized gap list with remediation order and evidence gaps |
| [`ai-lifecycle-risk-manager`](../../.claude/skills/ai-lifecycle-risk-manager/SKILL.md) | Cross-cutting | NIST AI RMF GOVERN/MAP/MEASURE/MANAGE across the AI lifecycle; pairs with `iso-42001-aims-architect` |

**Already covered — the batch MAPS, it does not rebuild:** much of 27001's A.8 Technological
theme and SOC 2's Security category is already implemented by shipped skills — Phase 3
`tenant-isolation-reviewer`, `authorization-matrix-designer`, `audit-log-architect` (access
control, authz, logging substrate); Phase 4 `rls-policy-auditor`,
`multi-tenant-security-tester`, `secrets-identity-hardener` (access control and credential
custody), `secure-migration-reviewer` (change management), `supply-chain-security-reviewer`
(vendor/supply chain), `threat-modeler` (risk-assessment input), `static-analysis-reviewer` +
`security-pr-reviewer` (secure development). Phase 5's evidence pack is the raw material
`compliance-evidence-collector` formalizes into audit-window evidence; Phase 7's planned
`ai-governance-risk-reviewer` and the shipped Phase 1.5 governance pack are what a 42001 / AI
RMF audit points at for AI-specific operational control. The compliance skills produce the
mapping and auditor-consumable evidence on top of these; net-new implementation is mostly
limited to ISO management-system artifacts (SoA, internal audit, management review) and
evidence plumbing.

**Status: implemented (D9 — PR #21).** All 9 skills merged to `main` 2026-07-07 via PR #21
(merge commit `2df96f1`); validator target moved 86 → 95, exit 0. No phases renumbered. The
sequencing left open at banking time resolved as: after Phase 7.5 and the D11 rebrand,
before any Phase 8 batch.

### Engineering discipline expansion (D12) — candidate packs

**BANKED scope (D12, 2026-07-07) — 7 candidate packs, 42 named candidates; banked on-demand.
Built since banking: D12.1 (7 skills) and D12.3 (6 skills), both 2026-07-07 (D23); the
remaining packs stay candidates.** At 95 shipped skills the library covers the technical,
governance, and compliance stacks; this banks the engineering disciplines a senior/principal
engineer would compose alongside them that remain uncovered. **Standing rule recorded here
(D12): the library is NOT capped at 300 skills** — the 300-skill roadmap (D5) is the
strategic backlog the library was audited against, not a ceiling; packs open as coverage or
real engineering need demands, not to hit a count. Every skill below is *(candidate — not
built)*; pull-forward goes through the §4.1 batch rules and the §4.2 pre-generation plan
table like any other batch, and per D13 below, `skill-quality-reviewer` builds first if any
pack is pulled forward.

| Pack | Candidate skills *(all: candidate — not built)* | Pack rationale |
|---|---|---|
| **D12.1 Data engineering (P1) — ✅ all 7 built (D23, 2026-07-07)** | `schema-evolution-planner`, `streaming-event-architect`, `data-quality-monitor-designer`, `operational-vs-analytical-splitter`, `warehouse-lake-architect`, `pii-lifecycle-designer`, `data-migration-runbook-author` | Multi-tenant SaaS operational + analytical data as a first-class discipline. The `streaming-event-architect` ↔ `api-event-architect` internal-pipeline-vs-external-contract seam is pinned in trigger-evals on both directions. |
| **D12.2 Product engineering craft (P1) — ✅ all 5 built (D24, 2026-07-07)** | `pagination-cursor-designer`, `error-taxonomy-designer`, `edge-state-ux-designer`, `notification-webhook-ux-designer`, `mobile-viewport-craft` | API/UX craft distinct from contract design (Phase 3 `api-event-architect` owns the contract; these own the craft inside it). The `api-event-architect` seam is pinned in every skill's trigger-evals; `error-taxonomy-designer` (error MODEL) ↔ `edge-state-ux-designer` (rendering the error STATE) pinned both ways. |
| **D12.3 Performance engineering (P1) — ✅ all 6 built (D23, 2026-07-07)** | `profiling-methodology-designer`, `query-plan-reader`, `n-plus-one-detector`, `caching-strategy-designer`, `latency-budget-architect`, `frontend-perf-engineer` | Performance as an engineering discipline — distinct from the load-testing VALIDATION in D10 Tier 1 (`performance-test-harness` + `load-test-planner`, built in the same D23 batch): D12.3 designs for performance, D10 measures it — the seam is pinned in trigger-evals on BOTH sides. `latency-budget-architect` consumes (never sets) `slo-reliability-architect` targets. |
| **D12.4 Technical writing / docs engineering (P1) — ✅ all 8 built (D25, 2026-07-07)** | `readme-craftsman`, `adr-sequencer` (extends shipped `adr-writer` with longitudinal ADR management), `diataxis-doc-organizer`, `docs-as-code-architect`, `api-doc-generator-designer`, `contribution-guide-author`, `onboarding-doc-designer`, `docs-retention-index` (report P1, added by D15: numbered index governing every workflow doc's lifecycle — retention category, reason-to-keep, superseded-by, cleanup rule — mirrored by per-doc retention frontmatter; documentation retirement as an approvable operation) | Durable documentation as its own discipline. Three seams pinned in trigger-evals: `adr-sequencer` EXTENDS `adr-writer` (composes, no duplicate); `docs-retention-index`↔`skill-deprecation-planner` (DOC vs SKILL retirement, both ways); `api-doc-generator-designer`↔`api-event-architect` (generated reference vs contract). PART A of the D12.4+D12.7+D12.9+D14 two-PR batch. |
| **D12.5 PM / product engineering interface (P2) — ✅ all 6 built (D24, 2026-07-07)** | `requirements-gathering-facilitator`, `product-spec-writer` (a product spec, distinct from an ADR), `roadmap-under-uncertainty-planner`, `prioritization-frame-picker`, `feature-flag-rollout-strategist`, `sunset-deprecation-communicator` | The engineering/PM boundary. Two hard seams pinned both ways in trigger-evals: `product-spec-writer`≠`adr-writer`, and `sunset-deprecation-communicator`≠`skill-deprecation-planner` (product-feature sunset vs library-skill retirement). `feature-flag-rollout-strategist`≠`plan-entitlement-architect`/`authorization-matrix-designer`. |
| **D12.6 Growth / analytics engineering (P2) — ✅ all 4 built (D24, 2026-07-07)** | `event-schema-architect` (analytics counterpart to `api-event-architect`), `funnel-definition-designer`, `ab-test-designer` (design AND reading of results), `product-analytics-instrumenter` | User-facing product analytics, distinct from system-facing observability (Phase 6 `observability-operator` / `slo-reliability-architect`). Two THREE-way seams pinned in trigger-evals: `event-schema-architect`≠`api-event-architect`≠`streaming-event-architect`; `product-analytics-instrumenter`≠`observability-operator`≠`skill-usage-instrumenter`. |
| **D12.7 Staff+ IC craft (P2) — ✅ all 7 built (D26, 2026-07-07)** | `tech-spec-writer` (broader than an ADR), `design-review-facilitator`, `cross-team-dependency-negotiator`, `roadmap-to-commitments-translator`, `staff-scope-selector`, `promotion-packet-writer`, `phased-work-handoff-designer` (multi-stage sequenced work with binding decisions carried forward as evidence — distinct from `ai-closeout-reporter`, which reports ONE turn, and from `ai-sdlc-operating-model`, which frames the whole lifecycle) (build spec substantiated by report P9: decision-ID register carried across stages, changed-files + explicit not-touched lists, proven-invocation-command sections with tell-tale output, deviation flags) | Technical leadership without management authority. |

**D12.8 Operational workflow patterns — evidence-extracted (P1)** *(pack added by D15,
2026-07-07; **all 10 built 2026-07-07, D21** — the concrete, invocable rules of the
Zero Trust AI Engineering Discipline (Zet-AI Engineering for short), D16)*: patterns
extracted from a read-only audit of two
production multi-agent repositories ([`docs/research/aegis-workflow-extraction-report.md`](../research/aegis-workflow-extraction-report.md));
all HIGH confidence (multiple concrete artifacts each); product content stripped at
extraction; live identifiers templated as placeholders per report §6.3. The pack
(each **✅ built (D21)**, with the report pattern ID):

- `scoped-approval-register` (P2) — durable approval records with Status/Reason/Scope
  allowed/Scope FORBIDDEN/Evidence; the record format complementing `human-approval-boundary`
- `standing-approval-and-auto-advance` (P3) — governed anti-approval-fatigue layer: documented
  standing approval for the mechanical delivery loop within named scope, default-on merge
  after green with explicit opt-out phrase (as practiced in the source repos), phase-advance
  rule, reviewer-block path. MUST compose `agent-authorization-matrix` +
  `human-agent-trust-reviewer`; scope limit (house rule): standing approval may thin low-risk
  approvals (phase advance, the pre-merge mechanical loop) but never covers protected-branch
  merge or arming auto-merge — that authority stays human-only per
  `agent-authorization-matrix`, so a built skill must template default-on merge as an explicit
  opt-in deployment-profile choice, never its default; rationale cites the
  ungoverned-auto-merge incident already encoded in `agent-authorization-matrix` evals — the
  governance elements are what separate this pattern from that incident
- `local-ci-mirror-preflight` (P4) — derive local equivalents of every PR-triggered CI check,
  verify on clean mainline first, classify failures (PR-caused / pre-existing / infra /
  cannot-determine); per-commit, distinct from release-scoped review
- `risk-tiered-validation-selector` (P5) — machine classification of changes to VALIDATION
  depth with fail-closed-to-full default; routes validation cost where
  `change-classification-gate` routes approval
- `sharded-validation-with-resume` (P6) — named functional shards, persisted status,
  resume-after-timeout, uncategorized catch-shard, one aggregate required CI check
- `merge-is-deploy-governance` (P7) — standing pipeline governance when the platform
  auto-deploys on merge: PR validation as authoritative gate, branch-protection config
  recorded in-repo, accepted-risk window, revert-PR rollback
- `context-co-update-ci-gate` (P8) — CI fails PRs touching important paths without
  context-map updates; the write-back half of `agent-startup-context-gate`'s read loop
- `lane-authoring-guide` (P10) — pre-work evidence-cited authoring guide per parallel agent
  lane; planner-to-implementer knowledge transfer BEFORE work begins, distinct from handoffs
- `gated-deployment-prompt-template` (P11) — reusable operator prompt for risky operations
  with placeholders, stop conditions, backup-then-verify gating, and ETA ranges calibrated
  from a deployment-history index; uncited operational claims labeled unverified
- `chat-backlog-reconciliation` (P13) — cadenced extraction of chat-only decisions/backlog
  into dated repo docs, then audited against PR/source evidence per item

**Enrichment deltas for shipped skills** (recorded, to apply when each skill is next
touched — report §4 end + P15):

- `ai-closeout-reporter` — per-surface pass/fail + negative-path tables, skip decomposition,
  unqualified-complete only after every gap closed, preflight-evidence block; P15
  completion-baseline anchors — immutable PR/SHA/migration evidence pinned so finished work
  is never re-litigated
- `adr-writer` — certainty labels, status-column index
- `agent-memory-governance` — P15 anchors as memory content rule
- `ai-sdlc-operating-model` — hub-and-spoke vs per-tool-spoke topologies as documented
  options; one-tool-per-surface-per-phase collision rule
- cross-cutting certainty-label convention (confirmed / inferred / unknown /
  unverified-recommend-confirming) as a candidate shared writing rule

**D12.9 Architecture advisory** *(pack added by D20, 2026-07-07; ✅ `architecture-advisor` built (D26, 2026-07-07))*: the library's
`architecture-designer` produces a concrete target architecture and migration plan once the
rough shape is known, and `cloud-architecture-decider` advises on cloud provider/posture —
but nothing advises on the architecture STYLE/PARADIGM itself (monolith vs modular monolith
vs microservices vs event-driven vs serverless vs SOA, and hybrids). This pack fills that
gap:

- `architecture-advisor` *(✅ built — D26, 2026-07-07)* — an ADVISOR that recommends an
  architecture STYLE for what the user is building, with honest tradeoffs and a reasoned
  recommendation — NOT a mechanical selector. Its discipline:
  - Understand the need FIRST: interview for domain, load/traffic shape, team size and
    operational maturity, deployment constraints, scaling and change expectations, and
    consistency/latency needs — before advising.
  - Lay out only the GENUINELY RELEVANT candidate styles for that situation (from monolith,
    modular monolith, microservices, event-driven, serverless, service-oriented, and
    hybrids) — not a textbook dump of all of them.
  - Give pros and cons of each FOR THIS SPECIFIC CASE, not generic pros/cons.
  - Make a CLEAR recommendation WITH its reasoning, and state explicitly what would change
    the recommendation (the decision's sensitivity).
  - CORE NEUTRALITY PRINCIPLE: fit the recommendation to the actual situation; resist
    trend-chasing in BOTH directions — do not default to microservices because it is
    fashionable, nor to monoliths because it is contrarian-safe. Often the honest answer is
    a boring modular monolith, and the skill must be willing to say so.
  - Compose, do NOT overlap: `architecture-advisor` picks and justifies the PARADIGM;
    `architecture-designer` then designs the concrete target WITHIN that paradigm
    (component maps, boundaries, migration plan); `adr-writer` records the decision. Three
    distinct jobs in sequence. The advisor hands its recommendation to
    `architecture-designer`.
  - Likely auto-invocable (pure advisory/analysis, edits nothing) — to be confirmed at
    build time.
  - When built, to be checked by `skill-quality-reviewer` for trigger overlap against
    `architecture-designer`, `cloud-architecture-decider`, `saas-platform-architect`, and
    `domain-modeler`.

**D12.11 SaaS Architecture Depth** *(pack added by D30, 2026-07-08; STRONG
cluster of 10 ✅ built by D31, 2026-07-08 — ahead of the D12.10 SAST/DAST pack
as planned; the 4 LOW-PRIORITY candidates ✅ built by D32, 2026-07-08 (Build B),
pack now COMPLETE)*: net-new architecture-depth gaps surfaced by a private
read-only deep-audit of production multi-tenant SaaS patterns plus general
SaaS-architecture research (product-agnostic — evidenced by production
multi-tenant SaaS patterns; no product/vendor named). Two tiers: a **STRONG
cluster (10, build-first)** carrying strong real-world evidence, and a
**LOW-PRIORITY set (4, scale-stage or possibly-extension)**. Each candidate
records its scope and the exact seam(s) it must pin at build time; three
(`usage-metering-and-cost-attribution-pipeline-designer`,
`intra-tenant-scope-architect`, `share-link-access-architect`) are flagged
standalone-vs-extension for `skill-quality-reviewer` to confirm at build.
**Scheduling: this pack is positioned to build BEFORE the D12.10 SAST/DAST pack
that follows it** — the architecture-depth gaps are foundational product
surfaces, so when packs are pulled the strong cluster here runs first, ahead of
D12.10.

*STRONG cluster (10 — ✅ all built by D31, 2026-07-08):*

- `command-gateway-architect` *(✅ built — D31, 2026-07-08)* — design a single
  server-side-mediated write path (a command bus): a command registry + a
  per-command pipeline (validate → authenticate the actor from the token, never
  from the client → authorize → server-derive tenant/resource scope from trusted
  rows → idempotency → execute → emit audit + domain events → safe error
  envelope), plus the "no direct client writes for protected actions" invariant.
  SEAMS: `api-event-architect` (external contract, NOT internal dispatch),
  `authorization-matrix-designer` (the policy it ENFORCES), `audit-log-architect`
  (the records it emits); backlog components `validation-boundary-designer` /
  `idempotency-first-designer`.
- `realtime-subscription-architect` *(✅ built — D31, 2026-07-08)* — design real-time
  client delivery (WebSocket/SSE/DB-change subscriptions/presence): channel/topic
  model, authorize-at-subscribe-time (the per-tenant + per-user leak boundary),
  fan-out, scaling stateful connections, backpressure, reconnect/replay, presence.
  SEAMS: `streaming-event-architect` (server-internal backbone, NOT client push),
  `api-event-architect` (request/response + outbound webhooks),
  `notification-webhook-ux-designer` (UX, not transport).
- `background-job-orchestration-architect` *(✅ built — D31, 2026-07-08)* — design the
  async job/worker execution model: offload-from-request-path, worker pools,
  scheduled/cron jobs, job idempotency + resumability/checkpointing, retry/backoff,
  job DLQ, visibility timeouts, per-tenant fairness. SEAMS:
  `streaming-event-architect` (transport vs execution — pin hard),
  `performance-test-harness` / `load-test-planner` (they measure it).
- `horizontal-scalability-reviewer` *(✅ built — D31, 2026-07-08)* — review whether a
  system can scale out: statelessness / session externalization, connection
  pooling, sticky-session + in-memory-singleton smells, autoscaling +
  load-balancer config, graceful shutdown/draining. SEAMS:
  `slo-reliability-architect` (targets), `latency-budget-architect` (latency),
  `caching-strategy-designer` (caching).
- `search-architecture-designer` *(✅ built — D31, 2026-07-08)* — design
  search/discovery: full-text (pg `tsvector` / `pg_trgm`) vs external engine,
  indexing pipeline + freshness, relevance/ranking, per-tenant search isolation
  (leak boundary), faceting/pagination seam. SEAMS: `rag-security-architect`
  (AI/vector retrieval), `multi-tenant-data-architect` (data-store scoping),
  `pagination-cursor-designer` (pagination).
- `file-upload-storage-architect` *(✅ built — D31, 2026-07-08)* — design file/object
  storage & upload flows: direct-vs-proxied upload, signed URLs, tenancy by
  bucket/path prefix, size/type/content validation, malware scanning,
  image/derivative processing, retention/lifecycle, CDN, storage-cost posture.
  SEAMS: `pii-lifecycle-designer` (personal-data lifecycle), `rls-policy-auditor`
  (storage RLS).
- `usage-metering-and-cost-attribution-pipeline-designer` *(✅ built — D31,
  2026-07-08; resolved STANDALONE — not an extension of `saas-cost-architect`)* —
  design the metering → pricing → allocation → rollup → reconciliation
  data pipeline: a billing-safe usage-event table (no content), time-bounded rate
  cards, exact/estimated/allocated cost entries with idempotency keys, additive
  daily rollups, budgets + breach alerts, spend forecast, reconciliation. SEAMS:
  `saas-cost-architect` (unit-economics/drivers — NOT the ETL; **pin hard, the
  closest overlap**), `ai-cost-guardrail-designer` (AI budgets/rate-limits/
  kill-switch), `operational-vs-analytical-splitter` (the rollup is an analytical
  projection). **FLAG: standalone-vs-extension-of-`saas-cost-architect` —
  `skill-quality-reviewer` confirms at build time.**
- `synthetic-monitoring-architect` *(✅ built — D31, 2026-07-08)* — design ongoing
  black-box production monitoring: scheduled synthetic journeys/probes against the
  live app + third-party deps, a hard prod-safety contract (probes must not mutate
  prod or leak test fixtures), synthetic SLIs + alert-on-synthetic-failure,
  canary/heartbeat probes, result capture/routing. SEAMS:
  `performance-test-harness` / `load-test-planner` (pre-release measurement),
  `playwright-e2e-engineer` (CI E2E, not prod-safe scheduled probes),
  `slo-reliability-architect` (defines SLOs, not the probes),
  `observability-operator` (white-box instrumentation vs external black-box).
- `offline-first-sync-architect` *(✅ built — D31, 2026-07-08)* — design the client
  offline data layer: write-while-offline queue, optimistic apply + rollback on
  server reject, conflict detection/resolution (LWW/merge/CRDT/manual), local
  persistence, background sync, online↔offline reconciliation + integrity. SEAMS:
  `edge-state-ux-designer` (offline/optimistic-rollback UX STATES, not the sync
  engine), `caching-strategy-designer` (server/distributed cache),
  `realtime-subscription-architect` (live ONLINE push).
- `admin-console-architect` *(✅ built — D31, 2026-07-08; was HIGH PRIORITY
  pull-forward within the strong cluster, the most operationally mature pattern
  in the audited portfolio)* — design the internal ops/support/superadmin
  surface: cross-tenant read/write with mandatory audit, impersonation /
  support-mode-as-user with hard boundaries + audit, least-privilege admin tiers
  (view-ops vs write-ops vs superadmin), break-glass/elevation workflows, and the
  operator control-plane (health dashboards, manual failover/retry, data-repair
  ops). SEAMS: `authorization-matrix-designer` (owns the authz POLICY +
  impersonation policy — this owns the CONSOLE architecture that ENFORCES it),
  `observability-operator` (telemetry vs the action surface),
  `agent-authorization-matrix` (AI-agent authority, not human-admin),
  `incident-response-runbook` (reactive playbook the console's tools serve).

*LOW-PRIORITY set (4 — ✅ all built by D32, 2026-07-08; both standalone-vs-
extension flags resolved STANDALONE at build time):*

- `cell-based-architecture-designer` *(✅ built — D32, 2026-07-08; **LOW** —
  scale-stage only, most SaaS never needs it)* — cell / blast-radius partitioning
  (self-contained stack subset, tenant→cell mapping, thin router, cell-by-cell
  deploy, cross-cell concerns, migration). SEAMS: `saas-platform-architect`
  (per-component isolation, not whole-stack cells), `architecture-advisor` (its
  style menu omits cells — this fills that), `agent-containment-reviewer` (agent
  blast-radius).
- `data-partitioning-sharding-strategist` *(✅ built — D32, 2026-07-08; **LOW** —
  scale-stage, "don't shard prematurely")* — OLTP partitioning/sharding for write
  scale (shard-key selection, range/hash/list partitioning, resharding a hot
  tenant, cross-shard costs, don't-shard-prematurely gate). SEAMS:
  `multi-tenant-data-architect` (isolation scoping, not throughput sharding),
  `warehouse-lake-architect` (analytical partitioning),
  `operational-vs-analytical-splitter`.
- `intra-tenant-scope-architect` *(✅ built — D32, 2026-07-08; **LOW**; **FLAG
  RESOLVED STANDALONE (D32)** — ~60% distinct from `multi-tenant-data-architect`,
  well above the ~40% duplicate threshold)* — a second mandatory data-scoping axis
  below the tenant (location/site/org-unit): per-user scope assignment, an RLS
  predicate on scoped tables, scope-restricted vs tenant-wide roles, propagation,
  and migration to add the axis live. SEAMS: `tenant-modeler` (tenant hierarchy),
  `multi-tenant-data-architect` (`tenant_id` scoping),
  `authorization-matrix-designer` (roles×permissions, not a row-filter dimension).
- `share-link-access-architect` *(✅ built — D32, 2026-07-08; **LOW**; **FLAG
  RESOLVED STANDALONE (D32)** — ~60% distinct from `authorization-matrix-designer`,
  well above the ~40% duplicate threshold)* — guest/public share-link access (opaque
  expiring/revocable tokens, guest sessions, optional password/OTP gating,
  per-link scope, enumeration/abuse defense, audit). SEAMS:
  `authorization-matrix-designer` (member roles, not anyone-with-the-link),
  `api-event-architect` (API credentials/webhook signing).

**Pull-forward priorities (existing backlog, NOT new D12.11 candidates)** — the
same audit gives strong real-world evidence to pull these forward, HIGH priority,
from their existing expansion backlogs (they are prioritization signals here, not
part of the 14 D12.11 candidates): `idempotency-first-designer` (Phase 2 —
"table-stakes for any mutating API"; TOP pull-forward — **✅ built (D79, 2026-10-10)** as the #17/#144 extension), the unnamed
**rate-limit-design** row (Phase 4 — general per-tenant/plan API rate limits +
noisy-neighbor defense; needs a NAME when pulled), and
`resilience-architecture-reviewer` (Phase 6 — circuit
breakers/bulkheads/timeouts/graceful degradation).

**D12.10 Security scanning & orchestration** *(pack added by D27, 2026-07-08; **all 3 BUILT by D44, 2026-07-16** — the LAST banked
capability, built after the library-wide `skill-quality-reviewer` sweep (D33) as planned)*: the library's existing security skills are
JUDGMENT skills — `static-analysis-reviewer` triages scanner findings it is handed,
`supply-chain-security-reviewer` covers dependencies/provenance — but nothing ORCHESTRATES
the scanning itself: running a SAST suite over a repo, dynamic testing against a running
app, or aggregating a whole-repo security scan into one report. This pack fills that gap.
Core principle for all three (per the Zero Trust AI Engineering Discipline, D16, and
`agent-authorization-matrix`): orchestrate-and-REPORT — an AI security scanner may READ a
repo and run scanners, but must never autonomously fix, open PRs, or change settings; every
action is handed to a human.

- `security-scan-orchestrator` *(built — D44)* — guides an assistant to
  clone/access a repo (READ-ONLY) and run the full security-scan suite (SAST +
  dependency/SCA + secret scanning + IaC/config scanning), then AGGREGATE findings into one
  prioritized report. Orchestrates and REPORTS; recommends fixes but NEVER applies them,
  opens no PRs, changes no settings — any action is handed to a human (per Zero Trust AI
  Engineering Discipline / `agent-authorization-matrix`). Composes with
  `static-analysis-reviewer` (which does the true-positive/false-positive judgment on the
  SAST output) and `supply-chain-security-reviewer` (dependency/provenance). Tool-agnostic
  (references scanner CATEGORIES, not one vendor's CLI).
- `sast-orchestration-designer` *(built — D44)* — selects and configures the
  right static-analysis approach for a codebase/language, runs it, and hands findings to
  `static-analysis-reviewer` for triage. Compose-don't-duplicate:
  `static-analysis-reviewer` JUDGES findings; this one PRODUCES them.
- `dast-safety-harness-designer` *(built — D44)* — designs dynamic (running-app)
  security testing with MANDATORY guardrails: only against systems the user owns and has
  WRITTEN authorization to test, never production without explicit human sign-off, scoped
  target allowlists, rate limits, and a documented blast-radius/rollback. DAST sends attack
  traffic at live software — treat it as a side-effecting operation requiring
  authorization; the skill DESIGNS the harness/plan, it does not autonomously attack
  anything. Discriminate from `multi-tenant-security-tester` (which tests tenant-isolation
  specifically).

### Library meta / self-application (D13) — candidate skills

**BANKED scope (D13, 2026-07-07) — 5 candidate skills; SCOPE COMPLETED: `skill-quality-reviewer`
built 2026-07-07 (first pull, D18); the remaining 4 built 2026-07-07 (D22).** The
library validates its own structure (`scripts/validate-skills.py`) but had no skills that
apply its own discipline to itself. These candidates turn the generation standard, the eval
convention (D3), and today's manual PR review flow into reusable skills.
`skill-quality-reviewer` is the highest-leverage candidate: **if any D12 pack is later pulled
forward, `skill-quality-reviewer` builds FIRST** so subsequent additions audit themselves —
satisfied ahead of any D12 pull (built 2026-07-07, D18).

| Candidate skill *(status per row)* | One-line rationale |
|---|---|
| `skill-quality-reviewer` — **✅ built (D18, 2026-07-07)** | Audits a skill against [`docs/skill-generation-standard.md`](../skill-generation-standard.md) as the JUDGMENT layer above the validator (which keeps the mechanical checks: sections, lengths, registration, name collisions): trigger quality, overlap/collision with colliders named, duplication/extension, eval integrity, section substance, scope, invocation posture — so every future addition gets the review the standard demands. |
| `eval-runner-designer` — **✅ built (D22, 2026-07-07)** | Specs what an eval runner should do (inputs, pass criteria, reporting); it does NOT build the runner — closes the design gap D3 left open ("there is no eval runner yet"). |
| `skill-usage-instrumenter` — **✅ built (D22, 2026-07-07)** | Telemetry design: which skills are invoked vs unused, trigger-match rate, false-positive-rate estimation — evidence for pruning and trigger fixes. |
| `skill-deprecation-planner` — **✅ built (D22, 2026-07-07)** | Safe skill sunset — mark deprecated, redirect triggers, remove from catalog — so the library can shrink as deliberately as it grows. |
| `library-diff-reviewer` — **✅ built (D22, 2026-07-07)** | Audits a skill-adding PR the way manual review does today: validator run, cluster-collision check, catalog integrity, incident-eval verification. |

### Framework refresh & source-currency discipline (D14) — candidate skills

**BANKED scope (D14, 2026-07-07) — 3 candidate skills; ✅ all 3 built (D26, 2026-07-07): `framework-edition-tracker`, `framework-mapping-refresher`, `source-currency-auditor`.** The
framework mappings banked and shipped so far (D6/D7/D8 OWASP maps, D9 compliance batch) are
point-in-time snapshots of external standards that revise on their own cadence. These
candidates give the library a refresh discipline so external-truth drift is detected instead
of silent — distinct from D12 (breadth) and D13 (self-quality): D14 governs currency with
EXTERNAL truth.

| Candidate skill *(all: candidate — not built)* | Purpose |
|---|---|
| `framework-edition-tracker` | Pins the editions cited by D6/D7/D8/D9; detects when a new edition ships; produces a delta report WITHOUT auto-updating any mapping. Highest-leverage of the three — pull forward when the first new edition drops. |
| `framework-mapping-refresher` | Given an edition delta, proposes the specific updates to affected skill descriptions, references, and coverage maps; human review required before any change lands. |
| `source-currency-auditor` | Audits skills citing external sources against a known-good source list; flags citations older than N months for re-verification. |

### Phase 8 — Backlog expansion (NEW in v4, ported from execution plan §8)
Convert the remaining backlog — the original 300-skill roadmap, per the D12 standing rule a
300+ target backlog (ship on demand and framework coverage, not count) — into executable
skills **in validated batches** under the batch rules in §4 below. Run only after
Phases 0–7.5 validate cleanly.

**Tracked backlog items — Phase 4 × OWASP Top 10:2025 (web app) gap audit (D8):**

- `security-logging-alerting-architect` *(✅ built, D28, 2026-07-08)* — closes A09:2025 Security
  Logging and Alerting Failures: security-event detection coverage, alerting rules, and
  response wiring; complements Phase 3 `audit-log-architect` (which records, but does not
  detect or alert).
- `error-handling-security-reviewer` *(✅ built, D28, 2026-07-08)* — closes A10:2025 Mishandling
  of Exceptional Conditions: fail-closed defaults, error-path authorization, exception-driven
  logic bypass, leak-free error responses.

Per D8, uncovered web-app categories land here as backlog items — not as a new phase and not
as changes to the shipped Phase 4 list.

---

## 4. Ported from the execution plan into v4

### 4.1 Phase 8 batch rules (now part of canonical v4)
- **Max 20 skills per pass.**
- **Merge** duplicate/overlapping skills instead of creating noisy variants; prefer one
  strong skill over five weak ones.
- **Add `evals/trigger-evals.json`** for any skill whose description overlaps an existing skill.
- **Update README + catalog after each batch; run the validator after each batch.**
- **Create a changelog entry** per batch: the append-only reconciliation D-entry is the per-batch changelog (CHANGELOG.md points readers to it; do not duplicate batch notes in a second log).
- **Stop** if generated skills become repetitive, too long, or weakly differentiated.

### 4.2 Pre-generation plan table (required before writing any skill)
Both tracks require this; it is canonical. Before creating skills in any phase, emit:

| Skill name | Category | Purpose | Trigger description | User-invocable? | Auto-invocable? | Supporting files | Eval cases |
|---|---|---|---|---|---|---|---|

### 4.3 Validator checks (union of both tracks — now enforced by `scripts/validate-skills.py`)
- Each skill dir has `SKILL.md`; frontmatter parses; `name` matches directory.
- `description` present and < 1024 chars.
- `SKILL.md` < 500 lines.
- No broad `allowed-tools`.
- **Catalog integrity:** every real skill is listed in `docs/skills-catalog.md` and `README.md`;
  the catalog/README claim no skills that do not exist.
- **Eval convention:** every real skill has `evals/evals.json` (structural existence + JSON parse).
- **Trigger-evals:** `evals/trigger-evals.json` is validated as JSON when present (Phase 8 requires
  it for overlapping skills).
- Bundled-name collision: no skill name shadows a reserved bundled skill name; no duplicate names.

---

## 5. Recorded decisions

- **D1 — v4 pair is canonical.** Execution plan → historical (§1).
- **D2 — Real subagents live at `.claude/agents/` with a read-only default posture.** This
  supersedes v4's earlier suggestion to store agent prompts in `docs/agents/agent-orchestrator-prompts.md`.
  The seven real subagent files ARE the agent layer; they must **not** duplicate skill bodies —
  they compose skills. Mapping from v4's orchestrator roles to the real subagents:

  | v4 orchestrator role | Real subagent (`.claude/agents/`) |
  |---|---|
  | Principal Claude Architect Agent | `principal-architecture-reviewer` |
  | SaaS Security and Tenant Isolation Agent | `secure-saas-reviewer` |
  | QA Automation and Release Evidence Agent | `qa-automation-lead` |
  | Full Codebase Audit Agent | `full-codebase-auditor` |
  | Senior Troubleshooting Agent | `senior-troubleshooting-lead` |
  | AI Security and LLM Systems Agent | `ai-security-red-team-reviewer` |
  | Release Captain Agent | `release-readiness-reviewer` |

- **D3 — Evals are a repo convention, structurally validated only.** The validator checks that
  `evals/evals.json` exists and parses (and `trigger-evals.json` parses when present). **There is
  no eval runner yet.** Building/using a runner is deferred; do not claim evals "pass," only that
  they are present and well-formed.
- **D4 — Phase 1 is the operating-discipline pack** (the 8 in §3), not the execution plan's
  architecture-heavy Phase 1. Architecture skills move to Phase 2.
- **D5 — 300-skill roadmap is the backlog/capability map, not a batch command.** Executable skills
  are built phase-by-phase; the remainder flows through Phase 8 batches.
- **D6 (2026-07-06) — Phase 7 is anchored to the OWASP Top 10 for LLM Applications (2025).**
  Canonical Phase 7 list expands 10 → 14 (adds `sensitive-disclosure-guard`,
  `model-poisoning-reviewer`, `system-prompt-leakage-reviewer`, `ai-misinformation-guard`).
  Rationale: anchor the AI-security pack to a current published framework rather than an
  ad-hoc list. Source: <https://genai.owasp.org/llm-top-10/>. Coverage map in §3 Phase 7.
- **D7 (2026-07-06) — Phase 7.5 (Agentic AI security) is added after Phase 7, anchored to
  OWASP Agentic Top 10 (ASI01–ASI10); it extends the LLM Top 10 (D6).** Rationale: agentic
  risk builds on top of LLM risk, so the pack runs immediately after Phase 7, and it is too
  central to this repo's agentic workflows to defer into the generic Phase 8 backlog.
  Canonical Phase 7.5 = 6 new skills (ASI08 and ASI10 merge into `agent-containment-reviewer`)
  plus 3 extensions of existing skills, built at Phase 7.5 — not now. Phases 0–8 keep their
  numbers; the shipped validator skill-count target is unchanged. Source:
  <https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/>.
  Coverage map in §3 Phase 7.5.
- **D8 (2026-07-06) — Phase 4 is cross-checked against the OWASP Top 10 for Web Application
  Security; uncovered categories are tracked as Phase 8 backlog.** Audited against the current
  released edition, OWASP Top 10:2025 (A01:2025–A10:2025). Source:
  <https://owasp.org/www-project-top-ten/> (category list: <https://owasp.org/Top10/2025/>).
  Result: 6 covered, 2 partial (A02 Security Misconfiguration, A04 Cryptographic Failures),
  2 gaps (A09 Security Logging and Alerting Failures, A10 Mishandling of Exceptional
  Conditions) — gaps recorded as candidate skills in the §3 Phase 8 backlog
  (`security-logging-alerting-architect`, `error-handling-security-reviewer`). Coverage map
  in §3 Phase 4. This is a gap audit of shipped work: no skills created or changed, no phases
  renumbered, validator target unchanged. Third distinct framework: separate from the OWASP
  Top 10 for LLM Applications (D6) and from the OWASP Agentic Top 10 for 2026 (D7, Phase 7.5).
- **D9 (2026-07-06) — A Compliance & Governance batch (ISO 27001:2022 + ISO 42001:2023 + SOC 2
  Type 2, with NIST AI RMF 1.0 as companion) was banked as a future batch targeted AFTER
  Phase 7; implemented 2026-07-07 via PR #21 (merge commit `2df96f1`).** Subsection in §3,
  after Phase 7.5. Rationale: as an AI SaaS vendor selling into US
  enterprise and EU markets, these converge into procurement requirements (SOC 2 in US
  enterprise sales; 27001 via EU NIS2 supply-chain demand on customers; 42001 emerging in EU
  public procurement) — vendor-market rationale, not a standards claim. Architecture: **one
  shared control foundation + framework-specific projections + a crosswalk** (9 skills,
  already merged — one evidence collector, one gap auditor, one SoA author across
  frameworks), NOT three parallel skill sets; published crosswalks put cross-framework control
  overlap at ~60–80% (industry estimate, not a standard-derived number). The batch is
  substantially a **mapping + evidence layer** over controls already shipped in Phases 3/4
  (and the Phase 5 evidence pack) — it does not rebuild them. Precision: SOC 2 is an AICPA
  **attestation** (CPA examination); 27001/42001 are **certifiable** management-system
  standards. Distinct from Phase 1.5 (operational agent governance) and the OWASP maps
  (D6/D7/D8). All 9 skills built and merged via PR #21 (2026-07-07, merge commit `2df96f1`);
  no phases renumbered; validator target moved 86 → 95, exit 0. Sources fetched 2026-07-06
  (<https://www.iso.org/standard/27001> and
  <https://www.iso.org/standard/42001> returned HTTP 403 to automated fetch, so standard
  structure was verified from official-distributor preview PDFs of the standards themselves):
  - **ISO/IEC 27001:2022 preview PDF** (title page, TOC, Foreword/Introduction):
    <https://cdn.standards.iteh.ai/samples/82875/726bcf58250e43d9a666b4d929c8fbdb/ISO-IEC-27001-2022.pdf>
    — **verified:** third edition 2022-10; ISMS requirements; clauses 4–10; "Annex A
    (normative) Information security controls reference"; third edition replaces 27001:2013.
  - **ISO/IEC 42001:2023 preview PDF**:
    <https://cdn.standards.iteh.ai/samples/81230/4c1911ebc9a641fcb6ee21aa09c28ad3/ISO-IEC-42001-2023.pdf>
    — **verified:** first edition 2023-12; AIMS requirements ("requirements for establishing,
    implementing, maintaining and continually improving an AI management system"); clauses
    4–10 incl. 6.1.2–6.1.4 (AI risk assessment / AI risk treatment / AI system impact
    assessment); "Annex A (normative) Reference control objectives and controls"; Annex B
    (normative) / C, D (informative); drafted by ISO/IEC JTC 1/SC 42.
  - **Amd 1:2024:** ISO catalog entry "ISO/IEC 27001:2022/Amd 1:2024 — … Amendment 1: Climate
    action changes" <https://www.iso.org/standard/88435.html> — **title/existence verified via
    search listing (page itself 403); the exact 4.1/4.2 inserted text is from secondary
    summaries (CompliancePoint, High Table, Iseo Blue) — flagged, not fetched from ISO.**
  - **27001 Annex A counts** (93 = A.5×37 + A.6×8 + A.7×14 + A.8×34):
    <https://www.isms.online/iso-27001/annex-a-2022/> plus corroborating vendor references —
    **flagged: secondary sources; verify against the Annex A table before citing.**
  - **42001 Annex A counts:** secondary sources conflict (38 controls / 9 objectives vs 42
    objectives) — **deliberately not stated; unverified.**
  - **SOC 2 / TSC (AICPA):**
    <https://www.aicpa-cima.com/resources/landing/system-and-organization-controls-soc-suite-of-services>,
    <https://www.aicpa-cima.com/resources/download/2017-trust-services-criteria-with-revised-points-of-focus-2022>,
    <https://www.aicpa-cima.com/topic/audit-assurance/audit-and-assurance-greater-than-soc-2>
    — **verified:** five categories (Security, Availability, Processing Integrity,
    Confidentiality, Privacy); TSC issued by the Assurance Services Executive Committee (2017
    TSC with revised Points of Focus 2022); use in "attestation or consulting engagements";
    SOC 2 titled "Reporting on an Examination of Controls at a Service Organization…".
    **Flagged:** Type 1 vs Type 2 definitions and "Security = required common-criteria
    baseline" are NOT on AICPA's fetchable pages — corroborated via CPA-firm sources
    (Schellman, Linford & Co); the defining text is the paywalled AICPA SOC 2 guide.
  - **NIST AI RMF:** <https://www.nist.gov/itl/ai-risk-management-framework> and
    <https://airc.nist.gov/airmf-resources/airmf/5-sec-core/> — **verified:** AI RMF 1.0
    released 2023-01-26, voluntary; "The Core is composed of four functions: govern, map,
    measure, and manage"; govern is cross-cutting; Generative AI Profile NIST-AI-600-1
    (2024-07-26); NIST notes AI RMF 1.0 is being revised.
  - The **~60–80% overlap** figure is an industry crosswalk estimate — **not a
    standard-derived number.**
- **D10 (2026-07-07) — Phase 5 QA expansion backlog is prioritized in three tiers from a gap
  audit of category 06 vs shipped skills; Tier 1 headlined by performance/load testing as the
  largest uncovered risk for a multi-tenant SaaS. Build timing: after the core phases (7, 7.5)
  or on demand; no skills built now.** Audit baseline: the 16 shipped Phase 5 skills (the 13
  canonical plus `integration-test-designer` #184, `api-contract-test-designer` #185, and
  `accessibility-test-harness` #204, pulled forward at ship time), plus QA coverage living
  cross-phase (#186 RLS testing → Phase 4 `multi-tenant-security-tester` /
  `rls-policy-auditor`; #182 validation-tier selection → Phase 1
  `change-classification-gate`). Overlapping roadmap items are merged, not multiplied:
  #205+#206 (may merge into one skill at build time), #214+#215, #226+#227, #200+#201,
  #211+#212. Items already owned by shipped skills are mapped once in the backlog section,
  not re-listed as candidates; `acceptance-criteria-tester` keeps its existing deferral note.
  Docs-only: no skills created, no phases renumbered, validator skill-count targets
  unchanged. Backlog + coverage mapping in §3 Phase 5.
- **D11 (2026-07-07) — Project identity adopted: "Project Aegis", identity line "Project
  Aegis — Shield of the agent fleet", tagline "Discipline before code. Evidence before
  merge."** The name carries three layers: the divine shield of Zeus and Athena; the Navy's
  Aegis, shield of the fleet — fitting for a veteran-founded project whose operating model
  is a fleet of agents; and a shield proven in use. Several skills' eval cases are drawn
  from real incidents this project absorbed during its own construction (an unauthorized
  auto-merge, stale-memory session collisions, an empty-directory build). Docs-only rebrand:
  README title/intro block, catalog header, and this entry; no skills created or changed; no
  phases renumbered; validator skill count unchanged (86). The GitHub repo rename
  (Claude-Skills → Project-Aegis) is a manual Settings action outside this change; the
  rename was observed already live during this pass (push to the old URL returned "This
  repository moved … Project-Aegis.git" and redirected automatically). README/catalog carry
  no badges or absolute repo URLs (verified); local git remotes still pointing at the old
  URL keep working via redirect but should be updated in a follow-up.
- **D12 (2026-07-07) — Seven engineering-discipline candidate packs (~40 candidate skills)
  are banked as on-demand scope; the library is NOT capped at 300 skills.** All on-demand:
  packs open as coverage or real engineering need demands, not to hit a count. Rationale: at
  95 skills the library covers the technical, governance, and compliance stacks; D12 records
  the engineering domains a senior/principal engineer would compose from that remain
  uncovered — data engineering, product engineering craft, performance engineering,
  technical writing / docs engineering, the PM/engineering interface, growth/analytics
  engineering, and Staff+ IC craft. Docs-only banking: no skills built now, no phases
  renumbered, validator skill-count target unchanged (95). Pack detail and per-pack
  rationales in §3.
- **D13 (2026-07-07) — Five library-meta / self-application candidate skills are banked**
  (`skill-quality-reviewer`, `eval-runner-designer`, `skill-usage-instrumenter`,
  `skill-deprecation-planner`, `library-diff-reviewer`). `skill-quality-reviewer` is the
  highest-leverage candidate; if any D12 pack is later pulled forward, build
  `skill-quality-reviewer` FIRST so subsequent additions audit themselves. Docs-only
  banking: no skills built now; validator skill-count target unchanged (95). Detail in §3.
- **D14 (2026-07-07) — Three candidate skills for framework refresh & source-currency
  discipline are banked** (`framework-edition-tracker`, `framework-mapping-refresher`,
  `source-currency-auditor`). Rationale: the D6–D9 mappings and any future framework skill
  are point-in-time — the underlying standards revise on their own cadence (the OWASP LLM
  Top 10 roughly annually, ISO standards periodically, the EU AI Act still finalizing);
  without a refresh discipline the compliance and security mappings drift silently.
  `framework-edition-tracker` is the highest-leverage candidate — pull it forward when the
  first new edition drops. D14 governs how the library stays current with EXTERNAL truth;
  distinct from D12 (breadth) and D13 (self-quality). Docs-only banking: no skills built
  now; validator skill-count target unchanged (95). Detail in §3.
- **D15 (2026-07-07) — Evidence-extracted operational workflow patterns banked:** 10 new
  candidates as pack D12.8, `docs-retention-index` added to D12.4, and enrichment notes
  recorded against 3 banked candidates and 5 shipped skills. Source: read-only audit of two
  production multi-agent repositories, report committed at
  [`docs/research/aegis-workflow-extraction-report.md`](../research/aegis-workflow-extraction-report.md);
  all extractions HIGH confidence except P15 (MEDIUM, recorded as enrichment not skill);
  product content stripped at extraction; live identifiers in source docs must be templated
  as placeholders in any derived skill (report §6.3). These patterns carry a stronger
  evidence tier than practice-from-memory: each cites concrete repo artifacts. No skills
  built; no shipped skill modified; validator target unchanged.
- **D16 (2026-07-07) — Zero Trust AI Engineering Discipline coined and documented** at
  [`docs/ZERO_TRUST_AI_ENGINEERING_DISCIPLINE.md`](../ZERO_TRUST_AI_ENGINEERING_DISCIPLINE.md).
  Tagline "Never trust, always verify — every step of the lifecycle. / Assume drift. Demand
  evidence. Track everything.", deliberately mirroring the Zero Trust security motto. Applies
  "never trust, always verify" to the whole SDLC to prevent drift and rot; its concrete rules
  are the D12.8 patterns; it is the doctrine Aegis itself operates under. Distinct from
  classic network Zero Trust. No skills built; this is doctrine, not a skill.
- **D17 (2026-07-07) — README reframed to present Aegis as an operating system for
  engineering software with AI, governed by Zero Trust AI Engineering Discipline,** with a
  "How to use this" operator guide and a "Map of the system" navigation section. Additive
  only; all prior README content (skill catalog, phase plan, validation, CI) preserved.
  No skills built.
- **D18 (2026-07-07) — `skill-quality-reviewer` built (first pull from the D13
  library-meta scope);** the judgment layer atop `scripts/validate-skills.py`, auditing
  trigger quality, overlap/collision, duplication, eval integrity, and section substance
  that the mechanical validator cannot check. Composes the manual skill-review discipline
  used across this project into an invocable skill. Pure review skill (verdict report only,
  edits nothing) → model-invocable. The other four D13 candidates
  (`eval-runner-designer`, `skill-usage-instrumenter`, `skill-deprecation-planner`,
  `library-diff-reviewer`) remain candidate — not built; the `library-diff-reviewer` seam
  (whole skill-adding PR vs ONE skill's quality) is pinned in the new skill's
  trigger-evals. 95→96 skills.
- **D19 (2026-07-07) — `agent-governance-audit` retrieval commands fixed and seams
  added,** per the first `skill-quality-reviewer` audit finding live-verified command
  failures in the skill's flagship merge-authority control: `timelineItems` removed
  from the `gh pr view --json` field list, `pulls/<n>/events` → `issues/<n>/timeline`,
  and the armed-auto-merge timeline event documented as strategy-specific
  (`auto_merge_enabled` / `auto_squash_enabled` / `auto_rebase_enabled` — on PR #7,
  the incident this control was built from, the actual event is `auto_squash_enabled`).
  `release-readiness-reviewer` (forward ship/merge gate vs retrospective
  did-it-follow-process verdict) and `agent-authorization-matrix` (audit-what-happened
  vs codify-the-authority-rule) seams added to the description/overlaps/trigger-evals;
  the should-not-soften eval retyped to the `_template` stop-condition convention
  (`should_trigger` / `triggers: true`). All fixed commands live-verified against this
  repo. No new skill; 96 skills unchanged. Neighbor follow-up (`ai-closeout-reporter`
  yield clause + trigger-evals) tracked separately.
- **D20 (2026-07-07) — `architecture-advisor` banked as a D12 candidate (candidate — not
  built):** an advisor that recommends an architecture style/paradigm (monolith / modular
  monolith / microservices / event-driven / serverless / SOA / hybrids) for what the user
  is building, with situation-specific pros/cons and a reasoned, neutrality-disciplined
  recommendation — NOT a mechanical selector. Fills the gap upstream of
  `architecture-designer` (which designs the concrete target within a chosen paradigm) and
  distinct from `cloud-architecture-decider` (provider/posture). Composes advisor →
  designer → adr-writer. Anti-trend-chasing neutrality is a core principle. On-demand; not
  built. Banked as pack D12.9 in §3; docs-only: no skill built, no phases renumbered,
  validator skill-count target unchanged (96).
- **D21 (2026-07-07) — D12.8 operational workflow patterns built:** 10 evidence-extracted
  skills (`scoped-approval-register`, `standing-approval-and-auto-advance`,
  `chat-backlog-reconciliation`, `context-co-update-ci-gate`, `lane-authoring-guide`,
  `local-ci-mirror-preflight`, `risk-tiered-validation-selector`,
  `sharded-validation-with-resume`, `merge-is-deploy-governance`,
  `gated-deployment-prompt-template`) — the concrete, invocable rules of the Zero Trust AI
  Engineering Discipline (D16). Product-agnostic, sourced from
  [`docs/research/aegis-workflow-extraction-report.md`](../research/aegis-workflow-extraction-report.md).
  96→106 skills. Every skill ships `evals/evals.json` + `evals/trigger-evals.json` with
  discriminating cases against its named composed neighbor (and against its in-batch
  siblings for the approval and validation clusters); 9 of 10 model-invocable,
  `standing-approval-and-auto-advance` manual-only (it authors standing autonomy — the
  `agent-authorization-matrix` reasoning); its merge-after-green is templated strictly as
  an opt-in deployment-profile choice per the D15 house rule, rationale citing the
  ungoverned-auto-merge incident. Embedded gh/git commands follow the D19 corrections
  (strategy-specific auto-merge events; squash commits revert as ordinary commits).
  `docs-retention-index` (P1, D12.4) and the enrichment deltas remain separate. To be
  checked by `skill-quality-reviewer` before final trust.
- **D22 (2026-07-07) — D13 library-meta scope completed:** 4 remaining meta-skills built
  (`library-diff-reviewer`, `eval-runner-designer`, `skill-usage-instrumenter`,
  `skill-deprecation-planner`) joining the earlier `skill-quality-reviewer` (D18).
  106→110 skills. These operate ON the skill library itself; product-agnostic (apply to
  any skill library). Seams honored and pinned in trigger-evals on both sides:
  `library-diff-reviewer` owns the whole skill-adding/modifying/retiring PR and composes
  `skill-quality-reviewer` as its single-skill inner loop (the D18 seam, now built);
  `eval-runner-designer` designs eval EXECUTION without claiming a runner exists (the D3
  convention stands until a built runner produces real runs); `skill-usage-instrumenter`
  designs the usage-evidence layer under strict minimization (skill names and coarse enums
  only — never prompt content or user identifiers) with a rare-but-critical exemption;
  `skill-deprecation-planner` stages skill retirement (mark → redirect → remove, rollback
  per stage, squash removal reverts as one ordinary commit per the D19 corrections) and
  pins the SKILL-vs-DOC seam against the still-banked `docs-retention-index` (D12.4). All
  four are pure review/design skills (edit nothing) → model-invocable.
  `skill-quality-reviewer`'s own description/trigger-evals annotations updated in the same
  change ("library-diff-reviewer — not built" would have become false on merge). To be
  checked by `skill-quality-reviewer` before final trust.
- **D23 (2026-07-07) — Data engineering (D12.1, 7 skills), Performance engineering
  (D12.3, 6 skills), and QA Tier 1 performance/load validation (D10, 2 skills) built.**
  110→125 skills, one PR (three pack commits: D12.1, D12.3, D10 — clean split boundaries;
  the batch was NOT split into multiple PRs). D12.1: `schema-evolution-planner`,
  `streaming-event-architect`, `data-quality-monitor-designer`,
  `operational-vs-analytical-splitter`, `warehouse-lake-architect`,
  `pii-lifecycle-designer`, `data-migration-runbook-author`. D12.3:
  `profiling-methodology-designer`, `query-plan-reader`, `n-plus-one-detector`,
  `caching-strategy-designer`, `latency-budget-architect`, `frontend-perf-engineer`.
  D10 Tier 1: `performance-test-harness`, `load-test-planner` — built as TWO skills
  (the §3 row's may-merge option declined at the pre-generation plan table: instrument
  vs traffic plan are different deliverables with a pinned sibling seam). **D12.3
  designs FOR performance; D10 MEASURES it — seam pinned in trigger-evals both sides**
  (harness thresholds are CONSUMED from `latency-budget-architect` /
  `slo-reliability-architect`, never invented). The highest external-collision seam —
  `streaming-event-architect` (internal pipeline) vs `api-event-architect` (external
  contract) — is pinned hard in both skills' trigger-evals. Product-agnostic (perf/data
  tool references kept generic/illustrative — EXPLAIN-style plans, stream platforms,
  load drivers by class, never one product's CLI). All 15 are design/analysis skills
  producing specs/plans/verdicts and editing nothing → model-invocable; the three that
  could touch live systems (profiling, harness, load) carry Stop Conditions forbidding
  execution against production without human approval. Embedded commands follow the D19
  corrections. To be checked by `skill-quality-reviewer` before final trust.
- **D24 (2026-07-07) — Product engineering craft (D12.2, 5 skills),
  PM/product-engineering interface (D12.5, 6 skills), and Growth/analytics
  engineering (D12.6, 4 skills) built.** 125→140 skills, one PR (three pack
  commits: D12.2, D12.5, D12.6 — clean split boundaries; the batch was NOT
  split into multiple PRs). D12.2: `pagination-cursor-designer`,
  `error-taxonomy-designer`, `edge-state-ux-designer`,
  `notification-webhook-ux-designer`, `mobile-viewport-craft` — the API/UX
  craft INSIDE the contract `api-event-architect` owns (pinned in every
  D12.2 trigger-eval). D12.5: `requirements-gathering-facilitator`,
  `product-spec-writer`, `roadmap-under-uncertainty-planner`,
  `prioritization-frame-picker`, `feature-flag-rollout-strategist`,
  `sunset-deprecation-communicator`. D12.6: `event-schema-architect`,
  `funnel-definition-designer`, `ab-test-designer` (design AND result
  reading), `product-analytics-instrumenter`. Key seams pinned in
  trigger-evals: `product-spec-writer`≠`adr-writer` (product spec vs
  architecture decision record);
  `event-schema-architect`≠`api-event-architect`≠`streaming-event-architect`
  (analytics schema vs external contract vs internal pipeline — a three-way
  seam); `product-analytics-instrumenter`≠`observability-operator`≠`skill-usage-instrumenter`
  (product analytics vs system telemetry vs skill-library usage — a
  three-way seam); `sunset-deprecation-communicator`≠`skill-deprecation-planner`
  (product-feature sunset communication vs library-skill retirement);
  `feature-flag-rollout-strategist`≠`plan-entitlement-architect`/`authorization-matrix-designer`
  (rollout vs entitlement/permission). Product-agnostic (no product/company/
  personal names or live identifiers; placeholder paths/ids only). All 15
  are design/facilitation/analysis skills producing specs/plans/verdicts and
  editing nothing → model-invocable (no `disable-model-invocation`); none
  performs side effects. Embedded commands (few — these are design skills)
  follow the D19 squash-merge corrections. The two three-way seams
  (`event-schema-architect`, `product-analytics-instrumenter`) are the
  highest mutual-overlap risks flagged for the reviewer pass. To be checked
  by `skill-quality-reviewer` before final trust.
- **D25 (2026-07-07) — Technical writing / docs engineering (D12.4, 8
  skills) built. PART A of the D12.4+D12.7+D12.9+D14 two-PR batch.**
  140→148 skills. D12.4: `readme-craftsman`, `adr-sequencer`,
  `diataxis-doc-organizer`, `docs-as-code-architect`,
  `api-doc-generator-designer`, `contribution-guide-author`,
  `onboarding-doc-designer`, `docs-retention-index`. Key seams pinned in
  trigger-evals: `adr-sequencer` EXTENDS `adr-writer` (longitudinal ADR
  corpus management — composes single-record authoring, does not duplicate
  it); `docs-retention-index`≠`skill-deprecation-planner` (DOC lifecycle/
  retirement vs library-SKILL retirement — pinned both ways, honoring the
  seam `skill-deprecation-planner` already referenced as "banked, not
  built", now built); `api-doc-generator-designer`≠`api-event-architect`
  (generated reference vs the API contract it documents). Within-pack
  seams pinned across `readme-craftsman`/`diataxis-doc-organizer`/
  `docs-as-code-architect`/`contribution-guide-author`/
  `onboarding-doc-designer` (entry doc vs corpus-by-mode vs pipeline vs
  contributor-guide vs new-hire onboarding). Product-agnostic (no product/
  company/personal names or live identifiers; placeholder paths/ids only —
  `contribution-guide-author` designs contribution guides generically, not
  one repo's CONTRIBUTING.md). All 8 are authoring/design skills producing
  docs/plans and editing nothing → model-invocable; `docs-retention-index`
  gates actual doc DELETION behind human approval (a Stop Condition), like
  `skill-deprecation-planner` for skills. PART B (D12.7 staff-IC 7 + D12.9
  architecture-advisor 1 + D14 framework refresh 3 = 11 skills) is a
  separate PR branched off main-as-it-is; it does not depend on this PR
  merging but should land after it for the count arithmetic. To be checked
  by `skill-quality-reviewer` before final trust.
- **D26 (2026-07-07) — Staff+ IC craft (D12.7, 7 skills), Architecture
  advisory (D12.9, 1 skill), and Framework refresh / source-currency
  (D14, 3 skills) built. PART B of the D12.4+D12.7+D12.9+D14 two-PR
  batch — 148→159 skills.** D12.7: `tech-spec-writer`, `design-review-facilitator`,
  `cross-team-dependency-negotiator`, `roadmap-to-commitments-translator`,
  `staff-scope-selector`, `promotion-packet-writer`,
  `phased-work-handoff-designer`. D12.9: `architecture-advisor` (the
  STYLE/paradigm advisor, per D20 — must discriminate from
  `architecture-designer`/`cloud-architecture-decider`/`saas-platform-architect`/
  `domain-modeler`, pinned all four). D14: `framework-edition-tracker`,
  `framework-mapping-refresher`, `source-currency-auditor` (a
  detect→propose→human-review pipeline; NONE auto-updates a mapping). Key
  seams pinned in trigger-evals: `tech-spec-writer`≠`adr-writer` (whole
  design vs one decision)≠`product-spec-writer`;
  `phased-work-handoff-designer`≠`ai-closeout-reporter` (one turn)≠`ai-sdlc-operating-model`
  (lifecycle); `staff-scope-selector`≠`promotion-packet-writer` (future
  scope vs past impact, both ways); `roadmap-to-commitments-translator`
  inverse of `roadmap-under-uncertainty-planner`;
  `framework-edition-tracker`≠`framework-mapping-refresher`≠`source-currency-auditor`
  (detect vs propose vs broad-staleness). **Build/count note:** built in
  parallel with PART A (D25/D12.4) off main@140, then REBASED onto the
  merged D25 (main@148) with the README/catalog/reconciliation
  pack-block, phase-table, count, and callout regions reconciled to
  include BOTH packs — 148→159 skills, decision log D25 then D26 in order.
  Merge order was PART A (D25) then PART B (D26). Product-agnostic (no product/company/
  personal names or live identifiers; placeholder paths/ids only; edition/
  price/model facts treated as verify-don't-assert per D14). All 11 are
  design/facilitation/advisory skills producing specs/plans/verdicts/
  reports and editing nothing → model-invocable;
  `framework-mapping-refresher` and `docs-retention-index`-style deletion
  is not in scope here, but `framework-edition-tracker`/`-mapping-refresher`/
  `source-currency-auditor` all gate any real change behind human review
  (Stop Conditions). To be checked by `skill-quality-reviewer` before final
  trust.

- **D27 (2026-07-08) — Security scanning & orchestration pack (D12.10)
  banked as candidates (candidate — not built):
  `security-scan-orchestrator`, `sast-orchestration-designer`,
  `dast-safety-harness-designer`.** Fills a real gap (SAST
  tool-running/orchestration, DAST against running apps, whole-repo
  security scan aggregation) distinct from the existing JUDGMENT skills
  (`static-analysis-reviewer` triages findings;
  `supply-chain-security-reviewer` covers deps). Core principle:
  orchestrate-and-REPORT, human approves any action — an AI security
  scanner may READ a repo but must not autonomously fix/PR/configure
  (Zero Trust AI Engineering Discipline). DAST requires written authorization
  + no-prod-without-sign-off guardrails. Build DEFERRED until AFTER the
  library-wide `skill-quality-reviewer` sweep and its corrections are
  complete. Not built.

- **D28 (2026-07-08) — OWASP Web-App Top 10:2025 gap closed:
  `security-logging-alerting-architect` (A09) and
  `error-handling-security-reviewer` (A10) built, the two remaining
  zero-coverage categories from the D8 audit. 159→161.** All 10 OWASP
  web-app categories now have at least one owning skill; A02/A04 remain
  "partial" by the D8 rubric (a slice covered, not the whole category —
  noted, not a gap). OWASP LLM (D6) and Agentic (D7) lists already
  complete. Category definitions per OWASP Top 10:2025 source.
  Product-agnostic. To be checked by `skill-quality-reviewer` in the
  deferred sweep. Seams pinned in trigger-evals:
  `security-logging-alerting-architect` ≠ `audit-log-architect` (records,
  never detects/alerts) ≠ `observability-operator` (system telemetry +
  alert-config implementation) ≠ `slo-reliability-architect` (reliability
  paging) ≠ `incident-response-runbook` (the playbook AFTER the alert this
  skill designs the firing of); `error-handling-security-reviewer` ≠
  `security-pr-reviewer` (broad diff gate vs the error-path lens) ≠
  `appsec-implementer` (builds the fix; the reviewer never edits) ≠
  `static-analysis-reviewer` (judges scanner output, not code directly) ≠
  `error-taxonomy-designer` (the error MODEL vs the security of its
  HANDLING). Both are design/review skills editing nothing →
  model-invocable (no `disable-model-invocation`).

- **D29 (2026-07-08) — `ai-cost-guardrail-designer` extended to cover the
  denial-of-wallet (DoW) + LLMjacking threat model (OWASP LLM10); enhancement,
  not a new skill — count stays 161.** Five evidence-backed defenses woven into
  the existing sections (no new skill, no rename): (1) cost-aware/token-based
  rate limiting — limit on token/cost per window, not request count (one
  request can cost hundreds of times another), with pre-call estimate +
  post-response true-up and per-tenant FIFO queues; (2) FAIL-CLOSED guardrails
  — a cost/rate/budget check that errors, times out, or loses its store DENIES
  the call, and the kill switch ENGAGES on a broken budget-state check; failing
  open turns the limiter into the DoW vector (CWE-636), composing
  `error-handling-security-reviewer` for the general discipline; (3)
  provider-side hard spending caps + billing-anomaly alerting — optional and
  OFF BY DEFAULT, flagged as a verify-at-design-time config action the skill
  flags, not architecture it builds; (4) AI credential-theft (LLMjacking)
  defense — server-side-only custody, short-lived/scoped/per-model keys to
  bound the cost blast radius, and invocation-logging tampering as a compromise
  signal; custody and rotation mechanics defer to `secrets-identity-hardener`,
  this skill owns the AI-spend angle; (5) attribution-under-attack — a DoW
  attacker, a looping agent, and an expensive-but-honest workload look
  identical on the invoice, so per-tenant/user/feature attribution is required
  before judging a spike malicious or benign. Description lightly touched (984
  chars < 1024) to signal the token-based / fail-closed / LLMjacking coverage;
  posture unchanged; product-agnostic (OWASP LLM10 + CWE-636 named by category,
  no vendor/product/incident names). Evals: +2 behavior cases (request-count
  cost-blindness; refuse to label a spike an attack without attribution) and +3
  trigger cases pinning the `secrets-identity-hardener` and
  `error-handling-security-reviewer` seams. Grounded in current DoW/LLMjacking
  research. To be checked by `skill-quality-reviewer` in the deferred sweep.

- **D30 (2026-07-08) — SaaS Architecture Depth pack (D12.11) banked as candidates
  (candidate — not built)**, from a private read-only audit of production
  multi-tenant SaaS patterns + SaaS-architecture research. STRONG cluster (10,
  build-first, scheduled AHEAD of D12.10 SAST/DAST): `command-gateway-architect`,
  `realtime-subscription-architect`, `background-job-orchestration-architect`,
  `horizontal-scalability-reviewer`, `search-architecture-designer`,
  `file-upload-storage-architect`,
  `usage-metering-and-cost-attribution-pipeline-designer`,
  `synthetic-monitoring-architect`, `offline-first-sync-architect`,
  `admin-console-architect` (HIGH/pull-forward). LOW-PRIORITY (4, scale-stage or
  possibly-extension): `cell-based-architecture-designer`,
  `data-partitioning-sharding-strategist`, `intra-tenant-scope-architect` (maybe
  extends `multi-tenant-data-architect`), `share-link-access-architect` (maybe
  extends `authorization-matrix-designer`). Each candidate carries its seam-pins
  for build-time. usage-metering + intra-tenant-scope + share-link flagged
  standalone-vs-extension for `skill-quality-reviewer` to confirm at build. ALSO:
  pull forward (HIGH) from existing backlogs — `idempotency-first-designer`
  (Phase 2, top), rate-limit-design (Phase 4, needs naming),
  `resilience-architecture-reviewer` (Phase 6). All product-agnostic. Build
  DEFERRED — this pack builds after the library-wide `skill-quality-reviewer`
  sweep, ahead of D12.10. Not built.

- **D31 (2026-07-08) — D12.11 SaaS Architecture Depth STRONG cluster built
  (10 skills). 161→171.** Built ahead of the D12.10 SAST/DAST pack as the D30
  schedule specified. The 10:
  `command-gateway-architect`, `realtime-subscription-architect`,
  `background-job-orchestration-architect`, `horizontal-scalability-reviewer`,
  `search-architecture-designer`, `file-upload-storage-architect`,
  `usage-metering-and-cost-attribution-pipeline-designer`,
  `synthetic-monitoring-architect`, `offline-first-sync-architect`,
  `admin-console-architect`.
  **`usage-metering-and-cost-attribution-pipeline-designer` resolved
  STANDALONE** (the build-time flag from D30): it is the metering→rollup→
  reconciliation DATA PIPELINE (event schema, idempotency keys, additive
  rollups, invoice reconciliation) — an ETL/schema deliverable, whereas
  `saas-cost-architect` is the unit-economics MODEL (driver inventory,
  attribution policy, profitability). They compose (the pipeline feeds the
  model); the only overlap is the word "attribution", so the surface is
  ~65% distinct — well above the ~40% duplicate threshold. Not a near-duplicate.
  Seams pinned per the D30 spec, in every skill's `trigger-evals.json` on both
  directions. Highest-overlap pins: usage-metering ≠ `saas-cost-architect`
  (pipeline vs cost model — hard); `background-job-orchestration-architect` ≠
  `streaming-event-architect` (execution vs transport — hard); the in-batch
  `realtime-subscription-architect` ↔ `offline-first-sync-architect` seam
  (live online push vs offline sync) pinned reciprocally both ways;
  `command-gateway-architect` ENFORCES `authorization-matrix-designer`'s policy
  and EMITS into `audit-log-architect`'s schema (not either);
  `admin-console-architect` is the CONSOLE that enforces the authz policy, ≠
  the policy / telemetry / agent-authority / incident-playbook it composes;
  `search-architecture-designer` (lexical) ≠ `rag-security-architect` (vector);
  `synthetic-monitoring-architect` (post-ship prod-safe black-box) ≠
  pre-release/CI/SLO/white-box neighbors. Product-agnostic (no product/company/
  personal names or live identifiers; placeholder paths/ids only; sweep for
  supabase/athena/lovable/aegis/onedrive/personal names/URLs came back clean
  except the standard evals `$schema` URL). All 10 are design/review skills
  producing specs/plans/verdicts and editing nothing → model-invocable (no
  `disable-model-invocation`); the three that DESIGN things that could run
  against live systems (`command-gateway-architect` datastore backstop,
  `synthetic-monitoring-architect` probes, `offline-first-sync-architect`
  reconciliation) carry Stop Conditions forbidding execution against production
  without human approval — they design, they do not run. Embedded commands
  follow the D19 squash-merge posture (few — these are design skills). The 4
  LOW-PRIORITY D12.11 candidates (`cell-based-architecture-designer`,
  `data-partitioning-sharding-strategist`, `intra-tenant-scope-architect`,
  `share-link-access-architect`) remain candidate — not built (Build B). To be
  checked by `skill-quality-reviewer` in the deferred sweep; highest mutual-
  overlap risks flagged for that pass: usage-metering ↔ `saas-cost-architect`
  and realtime ↔ offline-first. Validator: 171 skills, exit 0.

- **D32 (2026-07-08) — D12.11 SaaS Architecture Depth LOW-PRIORITY cluster
  built (4 skills). 171→175.** The deferred Build B, completing the D12.11
  pack. The 4: `cell-based-architecture-designer`,
  `data-partitioning-sharding-strategist`, `intra-tenant-scope-architect`,
  `share-link-access-architect`.
  **Both standalone-vs-extension flags resolved STANDALONE** (same
  author-then-judge circuit-breaker as D31's usage-metering):
  - `intra-tenant-scope-architect` vs `multi-tenant-data-architect`: the
    parent is explicitly SINGLE-AXIS (scoping decided around `tenant_id`,
    per-store pooled/silo strategy + propagation). The new skill adds a
    SUBORDINATE per-user scope axis below the tenant (site/region/org-unit):
    a per-user scope-grant model, a scope-restricted-vs-tenant-wide role
    split, the composite `tenant_id AND scope` row-filter predicate, and a
    live add-axis migration — none of which live in the parent. It
    PRESUPPOSES the tenant layer rather than restating it. Shared surface is
    the server-derived propagation + expand→contract migration pattern
    (~35%); distinct surface ~60% — well above the ~40% duplicate threshold.
    Not a near-duplicate; shipped standalone with the parent seam pinned hard.
  - `share-link-access-architect` vs `authorization-matrix-designer`: the
    parent is IDENTITY/RBAC for authenticated members (roles × permissions ×
    resources, impersonation/support). The new skill is a CAPABILITY model —
    possession of an opaque, unguessable, expiring, revocable token grants a
    fixed narrow scope to anyone-with-the-link, often unauthenticated, with a
    different actor, a different threat surface (token enumeration/leak/expiry,
    guest sessions, abuse defense), and a different lifecycle. The parent's
    one-line "sharing grant" is a MEMBER shared-with grant, not a public
    bearer link. Overlap (~30%: both authorization, both scope+audit+
    deny-by-default) is well below the distinct surface (~60%). Shipped
    standalone with the parent seam pinned hard.
  So both are new skills: 171→175 (not fewer). Seams pinned in every skill's
  `trigger-evals.json`, both directions. Highest-overlap pins: intra-tenant-
  scope ≠ `multi-tenant-data-architect` (subordinate axis vs tenant_id axis)
  and ≠ `command-gateway-architect` (standing read-side axis vs execute-time
  write scope — the D31 bleed guard); share-link ≠ `authorization-matrix-
  designer` (bearer capability vs member RBAC, incl. the member-shared-with-
  grant nuance case); `cell-based-architecture-designer` ≠ `saas-platform-
  architect` (per-component isolation) / `architecture-advisor` (style menu
  omits cells) / `agent-containment-reviewer` (agent blast radius), and its
  too-big-tenant edge routes to `data-partitioning-sharding-strategist`;
  sharding ≠ `multi-tenant-data-architect` (isolation) / `warehouse-lake-
  architect` (analytical) / `operational-vs-analytical-splitter` (what leaves
  OLTP). Product-agnostic (no product/company/personal names or live
  identifiers; placeholder paths/ids only; sweep for supabase/athena/lovable/
  aegis/onedrive/personal names/URLs came back clean except the standard
  evals `$schema` URL and one generic "Postgres" engine reference — neither a
  product/company name nor a live identifier). All 4 are design/review skills
  producing specs/plans/verdicts and editing nothing → model-invocable (no
  `disable-model-invocation`); the three that DESIGN a production-reshaping
  change (`cell-based-architecture-designer` cell migration/rebalancing,
  `data-partitioning-sharding-strategist` reshard, `intra-tenant-scope-
  architect` add-a-scope-axis migration) carry Stop Conditions forbidding
  execution against production without human approval — they design, they do
  not run. `share-link-access-architect` additionally Stop-Conditions
  inventing crypto (specify vetted primitives) and unilateral public exposure
  of regulated data (escalate). Embedded commands follow the D19 squash-merge
  posture (none needed — these are design skills). **D12.11 pack now COMPLETE:
  all 14 candidates resolved (10 strong built D31, 4 low-priority built D32).**
  To be checked by `skill-quality-reviewer` in the deferred sweep; residual
  overlap risks flagged for that pass: intra-tenant-scope ↔ `multi-tenant-
  data-architect` (the closest of the two flag decisions) and share-link ↔
  `authorization-matrix-designer`. Validator: 175 skills, exit 0.

- **D33 (2026-07-08) — Applied `skill-quality-reviewer` sweep corrections
  (19 REVISEs from the completed 8-batch / 80-skill sweep; all nit-level/
  soft, zero FAILs). Count stays 175 — edits only, no skill created/deleted;
  no skill logic/scope/posture changed.** Two mechanical classes:
  - **Built-before-neighbor back-references (Shape A, 8 older hubs):** older
    skills gained `overlaps_with` entries + discriminating trigger-eval
    cases + a one-line Use-When boundary for newer colliders that already
    named them — led by `api-event-architect`'s 6 (`streaming-event-
    architect`, `realtime-subscription-architect`, `command-gateway-
    architect`, `event-schema-architect`, `notification-webhook-ux-designer`,
    `api-doc-generator-designer`). Also `operational-vs-analytical-splitter`
    (stale write-path misroute retargeted from `multi-tenant-data-architect`/
    `architecture-designer` to `data-partitioning-sharding-strategist`,
    isolation-only kept on `multi-tenant-data-architect`; + usage-metering),
    `streaming-event-architect` (+background-job, +realtime),
    `multi-tenant-data-architect` (+sharding, +intra-tenant-scope),
    `saas-cost-architect` (+usage-metering), `architecture-advisor` (+cells),
    `saas-platform-architect` (+cells), `authorization-matrix-designer`
    (+admin-console, +intra-tenant-scope, +share-link).
  - **Eval-completeness nits (Shape A, 8 skills):** `lane-authoring-guide`
    (+scoped-approval-register), `sharded-validation-with-resume`
    (+qa-automation-architect, self-referential Gotcha de-housed),
    `risk-tiered-validation-selector` (+exact-prompt trigger case),
    `intra-tenant-scope-architect` (+share-link), `error-taxonomy-designer`
    (+error-handling-security-reviewer), `command-gateway-architect`
    (+intra-tenant-scope), `standing-approval-and-auto-advance`
    (+merge-is-deploy-governance), `horizontal-scalability-reviewer`
    (+data-partitioning-sharding-strategist).
  - **Staleness (Shape B, 2 skills):** `skill-deprecation-planner` and
    `context-co-update-ci-gate` had "banked / not built / until it ships /
    handled manually" wording about the now-SHIPPED `docs-retention-index`
    and `sunset-deprecation-communicator` replaced with shipped-state
    wording; all SKILL-vs-DOC and library-vs-product-PM discrimination kept
    verbatim.
  The sweep confirmed the library structurally sound — **0 FAIL, 0
  unroutable, 0 escalation** across 80 skills. Product-agnostic (swept
  supabase/athena/lovable/aegis/onedrive/personal names/URLs — clean except
  the standard evals `$schema` URL). Validator: 175 skills, exit 0. **To do
  next: D12.10 SAST/DAST build (deferred by D27).**

- **D34 (2026-07-10) — Documentation accuracy, coined-term rename, auto-merge
  reconciliation, and README readability pass (doc-only; count stays 175,
  validator exit 0; no skill created/edited/renamed/deleted).**
  - **Coined-term rename.** The project's doctrine term gained **"AI"** and
    dropped its hyphen — it now reads **"Zero Trust AI Engineering
    Discipline"** — updated at all 19 verified occurrences across 5 files
    (README, CONTRIBUTING, the catalog, this reconciliation doc, and the
    doctrine doc's H1 + definition). The classic network-security concept
    **"Zero Trust" is deliberately NOT renamed** — README:121, this doc's
    "Zero Trust security motto" / "classic network Zero Trust", the doctrine
    doc's "Distinction from classic Zero Trust" section, and the
    `human-agent-trust-reviewer` "zero trust weight/theater" idiom are all
    left verbatim. The doctrine file was likewise renamed (Option B — full
    consistency) to `docs/ZERO_TRUST_AI_ENGINEERING_DISCIPLINE.md`, with all
    5 inbound links updated (README:120/184/453, CONTRIBUTING:3, this doc's
    D16 entry).
  - **Accuracy fixes.** CONTRIBUTING rule 8's stale "95 skills" reworded to
    "exit 0" (no longer hard-codes a count that keeps going stale);
    CONTRIBUTING "On self-auditing" updated from "banked D13 candidate …
    when built" to the shipped reality (`skill-quality-reviewer`, built
    D18). Catalog Status count chain extended through D31→171 / D32→175
    (current total **175**) and its "Implemented (Phases 0–5)" heading
    relabeled to "Implemented" (the section runs through D32). README About
    paragraph brought current through D33 (was stale at D28). README "Map of
    the system" skills bullet — which omitted 8 shipped packs
    (D12.2/D12.4/D12.5/D12.6/D12.7/D12.9/D14/D28) — superseded by a pointer
    to the new roster. Minor: README "~175" → "175"; the validator
    catalog-integrity claim softened to match actual behavior;
    `secure-saas-reviewer` subagent "a application" → "an".
  - **Auto-merge contradiction reconciled** (owner-confirmed truth: Aegis's
    development used MANUAL merge after green checks; auto-merge is never
    armed as policy). `auto-merge-policy.md` originally specified an opt-in
    per-phase auto-merge-*arming* mechanism (`gh pr merge --auto --squash`)
    that was never adopted; it is corrected forward to describe the actual
    manual-merge process (original text summarized in-doc for provenance,
    not silently deleted). README:701 ("Auto-merge is enabled per-phase …")
    corrected to manual-merge. CONTRIBUTING rule 3 and README:151 were
    already correct and kept. The one time auto-merge fired — PR #7 — was
    the unauthorized incident recorded in §6 and captured as an
    `agent-authorization-matrix` eval; that is the *rationale* for the
    manual-merge rule, not a counterexample to it.
  - **README readability.** The ~80-line About wall-of-text broken into
    digestible paragraphs; a new scannable **"What's in the library"** roster
    of the 19 shipped pack-families (purpose + example skills each),
    surfacing `requirements-gathering-facilitator` as the elicitation entry
    point that feeds `product-spec-writer`; and a concrete **"Getting
    started"** subsection with copy-pasteable git/Claude-Code steps plus the
    Claude.ai / non-CLI path.
  Doc-only: no skill file, validator, or CI config touched — the
  `secure-saas-reviewer` subagent grammar fix is the sole non-doc,
  non-skill file. Validator: 175 skills, exit 0.
  - **Correction (appended, no rewrite of the D34 record; verified
    2026-09-30 against `origin/main` at `2184b54f`).** The inbound doctype
    links named above were correct at `2058b216`'s parent (`72bdf2c3`:
    README **120**, **184**, **453**; CONTRIBUTING **3**, all pointing at
    `docs/ZERO_TRUST_ENGINEERING_DISCIPLINE.md`), but none of those numbers
    resolves to the doctrine link today. The current inbound links are
    README **53**, **150**, **549** and **1106**, and CONTRIBUTING **14**
    (plus CONTRIBUTING **168**, a later addition). The two "Zero Trust"
    occurrences the entry says were deliberately NOT renamed are now README
    **119** ("## The discipline behind it: Zero Trust AI Engineering
    Discipline") and this page's own D34 passage at **1481-1483** (its "Zero
    Trust security motto" / "classic network Zero Trust" wording; the motto
    it mirrors is stated in the D16 entry at page **1040**/**1043**);
    README:121's "Zero Trust security principle" wording no longer exists on
    `main`. README:701's "Auto-merge is enabled per-phase …" and README:151
    are likewise both gone: the current statement is README **1423**
    ("Auto-merge is not armed."), and no line contains the old phrase.
    CONTRIBUTING rule 3 ("merge under human authority; do not arm auto-merge") is still
    rule 3, now at CONTRIBUTING **38**; CONTRIBUTING **168** is an unrelated later
    addition (the 3f zero-trust bullet).

- **D35 (2026-07-10) — Getting Started rewrite: real step-by-step onboarding
  + first-session entry point relocated (doc-only; README.md + this entry;
  count stays 175, validator exit 0; no skill file touched).**
  - **Problem (owner feedback).** The previous "Getting started" stopped at
    `git clone` plus a vague "open this folder in Claude Code" — a capable
    engineer who had never used Claude Code was left guessing. And the
    "Start a project here: `requirements-gathering-facilitator`" journey
    guidance was buried mid-paragraph in the D24 roster family (a catalog
    section) instead of living in Getting Started where a new user looks.
  - **Fix 1 — step-by-step onboarding.** Getting Started rewritten as
    numbered, copy-pasteable steps per environment: Step 1 get-the-repo
    (`git clone` / `cd` / `git pull`, one novice-friendly line each);
    Option 1 Claude Code CLI (install via the official docs at
    code.claude.com/docs — linked, not copied, because install commands
    drift; requires a Claude subscription or Console API access; run
    `claude` from the repo folder; `.claude/` auto-discovery of the 175
    skills + 7 subagents; the previously missing KEY explanation that
    skills are trigger-invoked, not slash-commanded, with two literal
    example prompts; `claude --continue`); Option 2 VS Code / Cursor
    (official Anthropic extension, Open Folder on the repo, Spark-icon
    panel, same engine as the CLI); Option 3 JetBrains plugin, with the
    honest note that Visual Studio (classic) has no native plugin — the
    CLI-in-terminal path is the way; Option 4 Claude.ai / apps kept with
    its honest no-auto-trigger framing; plus a labeled
    "Using the skills in your own project" copy-the-folders step.
    Deliberately NO `npm install -g` instructions (deprecated install
    method; the official page is the single source).
  - **Fix 2 — "Your first session" block added inside Getting Started:**
    start from questions with `requirements-gathering-facilitator`, a
    literal paste-ready first prompt, and the natural chain →
    `product-spec-writer` → architecture/tech-spec skills → build under
    the discipline loop.
  - **Fix 3 — roster cross-reference.** The buried "Start a project here:"
    sentence in the D24 roster family replaced with a one-line pointer to
    *Your first session* in Getting Started; the family still names
    `requirements-gathering-facilitator` as a member skill — only the
    journey instruction moved.
  Doc-only: README.md and this entry are the only files touched.
  Validator: 175 skills, exit 0.

- **D36 (2026-07-10) — Getting Started completion: beginner steps, all
  surfaces, Zero Trust AI Engineering Discipline emphasis (doc-only;
  README.md + this entry; count stays 175, validator exit 0; no skill file
  touched).**
  - **Why.** D35 shipped a good Getting Started rewrite, but an earlier
    draft of its spec ran; this entry completes the final spec. Everything
    is additive or a small in-place edit — D35's structure (Step 1, the
    options, "Your first session", the roster cross-reference) stands.
  - **Beginner-proofing (writing rule: ELI-beginner, never condescending).**
    Step 1 now says how to open a terminal (Windows key / Cmd+Space
    keystrokes) and links git-scm.com/downloads when `git` is missing.
    Version-prone specifics stay linked to code.claude.com/docs, never
    reproduced (the deprecated `npm install -g` method stays banned).
  - **All surfaces.** A "One engine, many surfaces" framing line added
    after Step 1 (terminal / VS Code + forks / JetBrains / Desktop / web,
    linking code.claude.com/docs/en/platforms; the old "Options 1–3 are the
    same engine" intro line trimmed so the two don't repeat). Option 2
    retitled to cover Cursor/Windsurf/VSCodium with the plain distinction
    that the skills are used by Claude Code, not the fork's own AI (Cursor's
    native chat/Composer does not auto-load `.claude/skills/`). Option 3
    (JetBrains) rewritten as numbered steps fixing a real gotcha — the
    plugin does NOT bundle the CLI, so the CLI installs FIRST — plus a
    generalized any-other-editor one-liner (Neovim/Emacs/Sublime/classic
    Visual Studio → run `claude` in a terminal). Two missing surfaces added
    and options renumbered: Option 4 Claude Code Desktop app (no terminal
    at all) and Option 5 Claude Code on the Web (claude.ai/code, zero
    install, honest cloud-copy caveat); Claude.ai manual-paste fallback is
    now Option 6. "Using the skills in your own project" gained one literal
    copy command per OS (PowerShell `Copy-Item -Recurse` / bash `cp -r`),
    each with a one-line explanation.
  - **Discipline emphasis.** New README section "The discipline behind it:
    Zero Trust AI Engineering Discipline" placed immediately after "What
    this is" — a pitch, not a second doctrine doc: two owner-voice
    paragraphs (security's never-trust-by-default lesson vs the blind trust
    AI-assisted development reintroduced; drift + rot and the
    speed-without-silent-decay payoff), six plain-language rules derived
    from the doctrine doc and CONTRIBUTING's operating rules (done-isn't-
    done-until-verified / evidence-not-assertion / assume-drift /
    small-reviewable-changes / human-is-the-gate / track-every-decision),
    the two-tier tagline, and one link to
    docs/ZERO_TRUST_AI_ENGINEERING_DISCIPLINE.md.
  - **Standards placement check (verify-only, no edit).** ISO 27001 /
    ISO 42001 / SOC 2 already appear in the "What's in the library" roster
    family 10 line (Compliance & governance); OWASP appears in family lines
    8 (LLM Top 10), 9 (Agentic Top 10), and 17 (web-app gap closure).
    Confirmed in place; no edit made.
  - README's "Map of the system" decision-log range bumped D35→D36 to match
    this entry.
  Doc-only: README.md and this entry are the only files touched.
  Validator: 175 skills, exit 0.

- **D37 (2026-07-11) — Banked read-only discovery for `project-orchestrator`
  (verbal; no files touched; count stays 175).**
  - Ran a read-only discovery pass before the D38 build: read
    `docs/skill-generation-standard.md`, `scripts/validate-skills.py`,
    `ai-sdlc-operating-model` (SKILL.md + `references/stage-gate-map.md`),
    `requirements-gathering-facilitator`, `phased-work-handoff-designer`,
    `scoped-approval-register`, `human-approval-boundary`,
    `agent-authorization-matrix`, and `change-classification-gate` to fix the
    compose-not-restate boundary before writing anything.
  - **Key finding.** `ai-sdlc-operating-model` OWNS the per-change INNER
    lifecycle (context→classify→…→merge→close) and its stage-gate / authority /
    evidence table; a beginner-facing OUTER product arc (idea→discovery→…→
    release) that DELEGATES the inner loop back to that map is a genuine gap —
    and `ai-sdlc-operating-model` explicitly disclaims in-flight single-project
    navigation ("Do NOT use to enforce a single stage in-flight"). That
    disclaimed gap is what D38 builds.
  - Recorded so the D38 build's "grounded in the D37 read-only discovery"
    reference resolves and the §5 sequence stays gapless (no silent D36→D38
    jump — the Zero Trust AI Engineering Discipline applied to the decision
    log). No files changed in D37; count stays 175.

- **D38 (2026-07-11) — Built `project-orchestrator` — the beginner-facing,
  top-level lifecycle router (175→176; validator exit 0; one new skill).**
  - **What.** The library's front door: takes a non-developer from a vague idea
    to a shipped product via (1) runtime stage detection (reads
    `docs/project-state.md` + inspects the user's repo to locate the project on
    the lifecycle map — a vague prompt with no state file = stage zero →
    discovery; an approved spec but no code = ready for architecture), (2)
    next-skill routing along the library's existing hand-off seams (invokes the
    owning stage skill BY NAME — discovery→`requirements-gathering-facilitator`,
    product-def→`product-spec-writer`…, build-loop→`ai-sdlc-operating-model`'s
    inner lifecycle, release→`release-readiness-reviewer`; conditional skills
    invoked by evidence of the feature, not on the default path), (3)
    plain-language business-question translation (every technical fork surfaces
    as ONE business question about cost/time/risk/customer experience; the user
    answers business questions only, never engineering mechanics), and (4) a
    persistent, append-only, dated `docs/project-state.md` in the USER's product
    repo.
  - **Compose, never restate (the anti-duplication tripwire).** SKILL.md CITES
    `ai-sdlc-operating-model`'s `references/stage-gate-map.md` for the stage
    list / gates / authority model, and `change-classification-gate` for the
    change-rigor matrix — reproducing NEITHER inline (a grep confirms no inline
    stage-gate / authority-level / classification table). The
    `docs/project-state.md` schema COMPOSES `phased-work-handoff-designer`'s
    decision-ID register (still-binding flag; a changed decision is a new
    flagged deviation, never an overwrite) + `scoped-approval-register`'s
    approval-citation pattern (Status / Scope allowed / Scope FORBIDDEN /
    Evidence) + the house decision-log format.
  - **Human gate (composed, never relaxed).** Every irreversible step
    (migration, deploy, auth change, deletion, merge, release) routes through
    `human-approval-boundary` + `change-classification-gate` +
    `agent-authorization-matrix`; presents GO / CONDITIONAL-GO / NO-GO with
    plain-language reasons; the user authorizes. Model-invocable (fires on the
    cold vague prompt) but its output is proposals-and-questions.
  - **Trigger.** Wins the beginner meta-navigation framing ("I have an idea but
    don't know where to start / I'm not a developer / what do I do first / what
    comes next / take me from idea to shipped"). Defers (should_not_trigger
    trigger-evals + Use-When "Do NOT use"): elicitation →
    `requirements-gathering-facilitator` (INVOKED as stage 1), team AI-SDLC
    policy → `ai-sdlc-operating-model`, spec authoring → `product-spec-writer`,
    single-stage request → the owning skill (e.g. `code-reviewer`).
  - **Files.** New `.claude/skills/project-orchestrator/` — SKILL.md (286
    lines; description 941 chars < 1024), `references/project-state-template.md`
    (the one reference file — the state schema, with a generic maintenance-
    company worked example), `evals/evals.json` (happy cold-idea path +
    mid-flight state-file edge + refusals) and `evals/trigger-evals.json` (the 4
    deferrals). Registered in `docs/skills-catalog.md` and `README.md` (surfaced
    as the top-level "Start here" front door). Product-agnostic (generic
    domains only). Grounded in the D37 read-only discovery. To be checked by
    `skill-quality-reviewer` + `library-diff-reviewer` for the compose-not-
    restate condition (does it overlap `ai-sdlc-operating-model` or
    `requirements-gathering-facilitator` anywhere it shouldn't?).
  - Validator: 176 skills, exit 0.

- **D39 (2026-07-11) — README beginner-journey + "the roles Aegis can play" (doc-only;
  count unchanged at 176; validator exit 0; no skill file touched).**
  - **Why.** `project-orchestrator` (D38) shipped the beginner-facing *skill*, but the
    README still had no human-facing section that TELLS a non-developer the idea-to-shipped
    path is real and shows them the on-ramp. D39 adds that section — the repo's most
    important surface for its target audience (founders, non-developer "vibe coders",
    technical leaders evaluating whether the library is real).
  - **ADD 1 — `## From idea to shipped: the no-experience path`.** Placed high, immediately
    after `## The discipline behind it` and BEFORE `## How to use this` (a non-developer hits
    it early); deliberately distinct from and NON-colliding with the engineer-facing `## Start
    here (canonical reading order)` further down (which is untouched). Six parts: (a) the
    promise (you bring the business truth, Aegis brings the engineering discipline; you never
    need a skill name or a technical term); (b) THE paste-ready opening prompt in a quote block
    (the single most important thing on the page — `project-orchestrator` picks it up
    automatically, cross-linked to Getting started); (c) a tight 2–3-exchange worked example
    on the **generic maintenance-company** illustration, showing a technical decision (scoped
    revocable access link) arriving as a plain business question (how long should a customer's
    status link live?); (d) the **nine stages** in plain language (1–2 lines each — understand
    → define → design system → design security → plan build → build slice → test/accept →
    prepare deploy → decide to release), each naming what the USER decides; (e) a **you decide
    (business) vs. Aegis decides (engineering)** two-column table — the trust-building split;
    (f) one honest line on what this is NOT (doesn't remove judgment, doesn't guarantee market
    success, you remain the person who says yes).
  - **ADD 2 — `## The roles Aegis can play`.** Placed right after `## What this is` (the
    positioning hook a CTO/founder scanning the repo hits early). Intro line "In practical
    terms, Aegis can make Claude act as:" then the **16 roles VERBATIM** (owner's words) as a
    3-column table (role | plain-language meaning | 1–2 example skills). Forward-links to ADD 1
    for the non-developer path.
  - **Accuracy gate (Zero Trust — every claim verified against disk).** All 16 roles are
    backed by real shipped skills; every example skill named in the table was confirmed present
    on disk (`.claude/skills/<name>/SKILL.md`) before it was written — 31 distinct skills,
    all OK, zero missing. No role claims a capability the library can't back. Product-agnostic:
    the maintenance-company example is generic (no real product/company names — swept lines
    104–260, clean).
  - **Files.** `README.md` only (two new sections, lightly cross-linked; no existing section
    removed or restructured — Getting started, the discipline section, the roster, the phase
    plan, and canonical reading order all intact) + this §5 entry. No `.claude/skills/**`
    touched.
  - **Six grep confirmations (all pass).** (1) beginner-journey section (line 165) ABOVE
    `## How to use this` (line 261); (2) paste-ready opening prompt present; (3) all nine
    plain-language stages present; (4) the you-decide-vs-Aegis-decides split present; (5) all
    16 verbatim roles present (each ×1); (6) `## Start here (canonical reading order)` (line
    562) still intact and NOT collided with.
  - **Correction (appended, no rewrite of the D39 record; verified 2026-09-30 against
    `origin/main` at `2184b54f`).** All three line numbers in the checklist above are
    stale — **113 commits** touched the README after D39 landed (D51 retitled the
    last heading; D56, D57 and a run of README re-reads reflowed the page). Each
    target is confirmed
    present and the heading order is unchanged, so only the numbers drift: `## From
    idea to shipped: the no-experience path` is now README line **152** (was 165);
    `## How to use this` is now **250** (was 261); and the fourth heading was
    retitled by D51 to `## Canonical reading order (for maintainers)` in the same
    position, then retitled again and moved by later README passes — it is now
    `## Maintainer reading routes` at line **676** (the phrase "canonical
    reading order" no longer appears anywhere on `main`, in the README or in
    this page's live text — only in the two preserved D39/D51 passages above).
    D39's stated facts are
    unaffected (the section still sits above `## How to use this`, and the
    maintainer-facing section is still later in the file). Where the target is a
    heading, prefer the stable anchor over the brittle number: the links
    [From idea to shipped](../../README.md#from-idea-to-shipped-the-no-experience-path)
    and [Maintainer reading routes](../../README.md#maintainer-reading-routes) resolve
    by slug and survive reflow.
  - Validator: 176 skills, exit 0.

- **D41 (2026-07-15) — Doctrine extended with its inward-facing half: CONSTRAIN + CURATE
  pillars + "Zet-AI Engineering" shorthand (doc-only; count unchanged at 176; validator
  exit 0; no skill logic touched).**
  - **Why.** The Zero Trust AI Engineering Discipline's four pillars (TRACK / VERIFY /
    GOVERN / HAND OFF) all govern THE WORK from the outside — records, proof, gates,
    knowledge transfer — and were silent on the AI's own operating environment: the
    harness it runs in, the context it is fed, the loop it executes. Two independent
    real-production implementations, mined in the D40 read-only discovery, converged on
    the same extension — two inward-facing pillars. This closes the "engineering OF AI"
    half the title has always claimed (previously the doctrine governed engineering WITH
    AI only). Evidence-extracted, like the D12.8 patterns — not invented.
  - **ADD 1 — the two inward pillars** in `docs/ZERO_TRUST_AI_ENGINEERING_DISCIPLINE.md`,
    after the four outward pillars, in the existing `### VERB — gloss` format:
    **CONSTRAIN** (build the operating environment so the AI cannot exceed its authority;
    the harness is the contract — authority as a property of the environment, not of
    obedience) citing `agent-harness-architect` (planned — D42), `agentic-loop-designer`
    (planned — D42), and shipped `agent-authorization-matrix`; **CURATE** (control what
    enters and leaves the context; an unverified input is an unverified output; the
    context window is a supply chain — a curated diet, not access) citing
    `model-context-designer` (planned — D42), shipped `structured-output-validator`
    (extended in D42), and shipped `ai-evaluation-harness`. A six-pillar half-framing
    added at the top of "The concrete rules" expresses the industry disciplines in the
    doctrine's voice (harness engineering ⇒ CONSTRAIN; context engineering ⇒ CURATE; the
    loop's bounds/stops ⇒ CONSTRAIN, its observe/validate step ⇒ CURATE) — superset
    framing, not competitors. New cross-cutting principle woven into VERIFY: *a verifier
    that cannot fail is theater with an exit code — every check must be proven able to
    fail before it counts.*
  - **ADD 2 — the "Zet-AI Engineering" shorthand** (pronounced "zet-eye"), introduced
    next to the FIRST occurrence of the full term in all 6 files that name the discipline
    (the doctrine doc's core definition, `README.md`, `CONTRIBUTING.md`, this
    reconciliation doc, `docs/skills-catalog.md`, and `project-orchestrator`'s SKILL.md —
    prose only). Deliberately and partially reverses D34's full-term-only
    standardization: the full term stays CANONICAL; the shorthand is ADDITIVE, placed
    next to the full term so it is repeatable and recognizable. No file renamed; no
    classic-"Zero Trust" security reference touched.
  - **Honesty gate (shipped vs planned).** The three new skills the pillars cite
    (`agent-harness-architect`, `model-context-designer`, `agentic-loop-designer`) are
    NOT built here — they are D42. Marked "(planned — D42)" in the doctrine; NOT added to
    `docs/skills-catalog.md` or README's shipped lists. `structured-output-validator`,
    `agent-authorization-matrix`, and `ai-evaluation-harness` exist on disk and are cited
    as shipped.
  - **Files.** `docs/ZERO_TRUST_AI_ENGINEERING_DISCIPLINE.md` (pillars + framing +
    shorthand + VERIFY principle), `README.md`, `CONTRIBUTING.md`,
    `docs/skills-catalog.md`, `.claude/skills/project-orchestrator/SKILL.md` (the one
    skill file touched — ONLY prose that names the discipline; no logic/workflow/eval
    change), + this §5 entry. Product-agnostic: pillar rules generalized from the D40
    patterns; no product/company names, private paths, or PR numbers.
  - Validator: 176 skills, exit 0.

- **D42 (2026-07-15) — Built the CONSTRAIN/CURATE design skills (176→179).**
  `agent-harness-architect` (CONSTRAIN — the governed operating environment: single
  mediation point, deny-by-default pre-flight ladder, closed registry, server-side
  instruction custody, fail-closed audit), `model-context-designer` (CURATE —
  server-side context assembly under caps, closed schemas, PII/secret minimization,
  designed exclusions, reconstructible context), `agentic-loop-designer` (CONSTRAIN —
  single-shot-vs-agentic decision, clamped iterations, typed retryability with
  policy-stops-terminal, honest empty-set termination), + extended
  `structured-output-validator` (CURATE — type-level policy encoding + banned-content
  scan ladder step). These are the DESIGN skills for harness/context/loop engineering —
  they PRODUCE what the agentic-security cluster REVIEWS (seam: design-not-review,
  yielded explicitly). Threads the "a verifier that cannot fail is theater with an exit
  code" principle. Generalized from a read-only audit of two real production
  implementations (D40). Doctrine's D41 planned markers now shipped. To be checked by
  `skill-quality-reviewer` + `library-diff-reviewer` for the design-vs-review seam.
  - Validator: 179 skills, exit 0.

- **D43 (2026-07-15) — Closed the README presentation-drift ENFORCEMENT gap (the
  discipline applied to its own repo; doc + validator only; count unchanged at 179;
  validator exit 0; no skill logic touched).**
  - **Why.** The library preaches TRACK ("keep the record and reality in sync") and
    "anything caught by hand twice becomes a machine check," yet README presentation-drift
    had been hand-caught repeatedly (stale skill counts, a stale skill name, and an
    auto-merge policy contradiction — corrected around D34 — and now the roles table had
    shipped without the D42 CONSTRAIN/CURATE design capability). Root cause: the validator's
    README enforcement was a SUBSTRING check only — `check_catalog_integrity` verifies each
    skill name appears *somewhere* in README, nothing more. So a skill could ship with stale
    counts, absent from its roster family, or missing from the roles table and still pass
    green. This closes BOTH the current drift AND the mechanism so it cannot silently recur.
  - **Part A — fixed the current drift.** Added the missing **"an AI agent
    operating-environment architect"** role row (the DESIGN side of the D42 CONSTRAIN/CURATE
    pack — `agent-harness-architect`, `model-context-designer`, `agentic-loop-designer`),
    placed adjacent to the AI-security *review* row so design and review read side by side.
    Audited the other presentation surfaces and CONFIRMED current, fixing none that were not
    stale: roster family 20 (CONSTRAIN/CURATE, D42, 3) complete (20 family lines, counts sum
    178 + 1 orchestrator = 179); the About/progression sentence already names the doctrine's
    inward-facing pillars as shipped; the "six rules" discipline summary is an accurate
    OUTWARD per-session summary (not a pillar enumeration, makes no false claim) and was left
    unchanged. Added authoritative `<!-- SKILL-COUNT -->`/`<!-- FAMILY-COUNT -->` markers
    around the counts in the "What's in the library" intro — the human-readable "179 skills"
    text stays; the markers wrap the authoritative instance so the check is unambiguous about
    which number is the current total (historical/aspirational numbers stay unmarked).
  - **Part B — made CONTRIBUTING a complete, followable rule.** Replaced the vague "Register
    the skill in the catalog and the README" with a numbered registration checklist (3a–3f)
    enumerating every surface a new skill must update — catalog; the Skills-(shipped) table;
    the roster family + its `*(Phase/D, N)*` count; the count claims/markers; the roles table
    (a JUDGMENT call, with the D42 pack as the worked "yes, this warranted a new role" example);
    and the doctrine pillar link (judgment) — stating which parts are validator-enforced vs
    judgment. Added a note under "On self-auditing" documenting WHY the checks exist (the
    hand-caught-twice rule).
  - **Part C — added mechanical enforcement to `scripts/validate-skills.py`.**
    `check_readme_counts` (HARD: the marked `SKILL-COUNT` must equal the real skills on disk);
    `check_readme_family_roster` (HARD: sum of family counts + 1 project-orchestrator front
    door == disk, and the number of family lines == the `FAMILY-COUNT` marker; degrades to a
    WARNING if the roster can't be parsed, so a benign format change doesn't hard-block every
    PR); plus WARN-level `check_roster_flagships_exist` (a renamed/removed flagship left stale
    in the roster — the reverse direction the substring check never caught) and
    `check_roles_table_present` (the curated section exists). Curated/judgment surfaces are
    WARN, never HARD, so a check cannot false-fire and get muted — a false-firing check would
    violate the discipline it enforces.
  - **Proof each hard check can fail (Part C6).** Seeded three drifts and confirmed each
    ERRORS (exit 1), then reverted atomically: `SKILL-COUNT` 179→178 (marked != disk);
    family-1 count 8→7 (sum + 1 = 178 != 179 disk); `FAMILY-COUNT` 20→19 (marker != 20 family
    lines). Per *"a verifier that cannot fail is theater with an exit code"* and *"anything
    caught by hand twice becomes a machine check."*
  - **Files.** `README.md` (roles row + count markers), `CONTRIBUTING.md` (registration
    checklist + self-audit note), `scripts/validate-skills.py` (four new checks + wiring +
    docstring), + this §5 entry. No `.claude/skills/**` logic/workflow/eval touched. The map
    is now held to the territory for README counts mechanically, not by memory.
  - Validator: 179 skills, exit 0 (new checks active and passing, 0 warnings).

- **D44 (2026-07-16) — Built the D12.10 Security scanning & orchestration pack
  (179→182), the LAST banked capability (banked D27, deferred until after the
  D33 `skill-quality-reviewer` sweep, now complete).**
  - **What.** Three skills that fill the ORCHESTRATION gap the library's JUDGMENT
    security skills left open (`static-analysis-reviewer` triages the findings it
    is handed; `supply-chain-security-reviewer` covers deps/provenance) — nothing
    RAN or AGGREGATED the scans themselves:
    - `security-scan-orchestrator` — orchestrate a WHOLE-REPO static scan (SAST +
      dependency/SCA + secret + IaC/config) and aggregate it into ONE prioritized
      report (scope, tool-agnostic coordination, cross-tool normalization/dedup,
      severity aggregation, coverage/GAP account).
    - `sast-orchestration-designer` — design HOW a SAST suite is RUN (category-
      level analyzer selection, ruleset/config, baseline + diff-scanning, a GOVERNED
      FP suppression list, incremental-vs-full, fail-closed CI integration).
    - `dast-safety-harness-designer` — design a SAFE DAST harness against a running
      app: written-authorization gate (composes `human-approval-boundary`, classified
      via `change-classification-gate`), staging-only unless prod is explicitly
      authorized, rate/impact limits + abort, no destructive probes without sign-off,
      data-handling; NOT a pen-test playbook (no exploit enumeration).
  - **The hard seam — orchestrate-and-REPORT, human-approves-action.** These skills
    RUN and AGGREGATE; they never fix, act on, or triage findings. Finding TRIAGE is
    yielded to `static-analysis-reviewer` (MANDATORY in the two static skills — pinned
    in Use When + a discriminating trigger-eval); dep/provenance judgment to
    `supply-chain-security-reviewer`; DAST authorization to `human-approval-boundary`.
    The in-batch `security-scan-orchestrator` ↔ `sast-orchestration-designer` seam is
    pinned both ways.
  - **Fail-closed threaded through all three:** a scanner/probe that errors, times out,
    or can't reach its target is a REPORTED GAP, never a silent pass — *a scan that
    cannot run is not a clean scan* — and each ships the designed proof its failure
    path surfaces (*a verifier that cannot fail is theater with an exit code*).
  - **Posture.** All three are DESIGN/orchestration skills producing scan plans/
    aggregated reports and edit nothing → model-invocable (no `disable-model-invocation`);
    Stop Conditions forbid acting on/fixing findings and running DAST without written
    authorization. No NEW doctrine pillar (they APPLY the orchestrate-and-report principle
    of the Zero Trust AI Engineering Discipline / `agent-authorization-matrix`, D16) — no
    doctrine change. Roles table: no new row — the pack is orchestration tooling that
    FEEDS the existing application-security role and whose defining seam is that it does
    NOT do the security JUDGMENT; a new row would blur that (judgment call, CONTRIBUTING 3e).
  - **Registration (D43 enforcement).** Catalog D44 section (+ intro), README
    Skills-(shipped) D44 table, a NEW roster family 21 (Security scanning & orchestration,
    D12.10, 3), phase-plan D44 row, and the count bumps: README `SKILL-COUNT` 179→182 and
    `FAMILY-COUNT` 20→21 (+ the human-readable 182-skills/21-families prose across
    About/roles/map/getting-started, and the D1–D42→D1–D44 decisions range). Banked
    D12.10 candidate block marked BUILT.
  - **Product-agnostic** (swept scanner vendors + supabase/athena/lovable/aegis/onedrive/
    personal/URLs — clean; tool CATEGORIES only). Validator: **182 skills, exit 0**, D43
    count/family checks passing. To be checked by `skill-quality-reviewer` +
    `library-diff-reviewer` for the orchestrate-vs-triage seam.

- **D45 (2026-07-16) — Extended `cloud-architecture-decider` to cover the full
  ABSTRACTION LADDER as a first-class decision axis (rung × provider × posture,
  was provider × posture only), fixing an enterprise-hyperscaler bias that
  mis-steered the repo's non-developer/founder audience. Skill-edit only; count
  stays 182.**
  - **The gap (from the read-only D45 discovery).** The decider is STRUCTURALLY
    provider-neutral (its logical-architecture step forbids product names) but
    CONCRETELY named only AWS/Azure, and its scoring space was provider ×
    deployment-posture {single/multi/hybrid/stay} — WHICH-hyperscaler ×
    HOW-MANY. The abstraction RUNG (IaaS vs container-PaaS vs managed-Jamstack/
    SSR vs Postgres-BaaS vs edge/serverless vs hyperscaler) was not a scoring
    dimension. For the repo's stated non-developer/founder audience (README
    no-experience path, whose on-ramp includes deployment), steering to AWS/
    Azure is the wrong default — the modern 2026 startup default is
    managed-Jamstack + Postgres-BaaS + edge, with container-PaaS between that
    and the hyperscalers.
  - **The fix (Option A from the discovery).** Added the abstraction ladder
    (IaaS/VPS → container-PaaS → managed-Jamstack/SSR → Postgres-BaaS →
    edge/serverless → hyperscaler) as a first-class axis: a new Workflow step 4
    *"Place the workload on the abstraction ladder"* (rule: **pick the highest
    rung the workload tolerates, then a provider within it**), scoring widened
    to **rung × provider × posture**, an Abstraction-rung line added to the
    Output Format, and the managed-vs-self-hosted step reframed as the
    per-capability refinement WITHIN the rung (the ladder generalizes that
    toggle). Named the modern 2026 tier — managed-Jamstack (e.g. Vercel,
    Netlify, Cloudflare Pages), container-PaaS (e.g. Render, Railway, Fly.io),
    Postgres-BaaS (e.g. Supabase, Neon), edge (e.g. Cloudflare Workers) — and
    added **GCP** as a named, decide-able hyperscaler option (was absent).
  - **Brands as refreshable EXAMPLES within durable categories (house style).**
    Every brand is named only as an "e.g." example inside a durable category
    label; the DECISION AXES carry the weight (abstraction rung · ops maturity ·
    workload shape · cost model · compliance/residency · lock-in/exit) and a
    line states brand pricing/free-tiers/runtime-limits are VOLATILE
    verification items, never asserted — the same treatment the skill already
    gives hyperscaler SKUs/regions. Precedent: `merge-is-deploy-governance`
    names `vercel.json`/`netlify.toml`-class files; `rls-policy-auditor`
    already names Supabase as a generic mechanism example. A future update
    swaps the brand list without touching the logic.
  - **Preserved the product-name-free logical architecture.** The concrete
    brands live only in the ladder explanation + options/scoring output;
    Workflow step 2 still bans product names (now says so explicitly), and the
    Validation Checklist keeps *"zero provider product names"* AND adds a check
    that brands appear only in the ladder/scoring, never in the logical
    architecture.
  - **Handoff asymmetry noted, not resolved.** Hyperscaler-rung mapping still
    hands off to `aws-saas-architect`/`azure-saas-architect`; the modern tier
    has NO mapping skill yet, so the handoff notes it is LOWER-TOUCH to map (the
    platform absorbs account topology, IAM, network, patching) and routes the
    parts that still need design to existing owners — tenancy to
    `saas-platform-architect`/`tenant-modeler`/`multi-tenant-data-architect`,
    Postgres-BaaS RLS to `rls-policy-auditor`, and push-to-deploy to
    `merge-is-deploy-governance` (auto-deploy-on-push makes merge==deploy MORE
    central here than on a hyperscaler). No `managed-platform-saas-architect`
    target was invented.
  - **Banked (deferred) future candidates** *(both: candidate — not built)*:
    - `managed-platform-saas-architect` — Option B: a single pattern-named
      mapping skill for the modern managed-platform tier (container-PaaS /
      Jamstack / Postgres-BaaS / edge), the modern-tier peer of the aws/azure
      architects. **Conditional trigger:** build if/when the modern-tier
      handoff asymmetry bites (a decision lands on the modern tier and the
      tenancy/RLS/deploy routing proves insufficient).
    - `gcp-saas-architect` — the parallel hyperscaler mapping skill for GCP
      (GCP is now a decide-able option here but has no mapper), mirroring
      `aws-saas-architect`/`azure-saas-architect`. Separate, lower-priority
      future item. **Banked content (D48) — the GCP security suite, recorded
      for IF this trigger ever fires:** Security Command Center (CSPM +
      threat, now Enterprise tier), Google Security Operations/SecOps
      (SIEM/SOAR, renamed from Chronicle — the rename is the durable fact),
      Cloud Armor (WAF/DDoS), Cloud IDS (network IDS), Sensitive Data
      Protection (formerly Cloud DLP — the Macie slot), Assured Workloads
      (compliance/residency), and AI Protection + Model Armor
      (name-and-place ONLY, design yielded to the AI-security/agent
      cluster — the one GCP item touching the D48 Gap-2 seam). Same
      discipline as the shipped mappers: name + place, tie to
      isolation/cost/maturity, volatile packaging = verification items.
  - **Files.** `.claude/skills/cloud-architecture-decider/SKILL.md` (description
    widened to name the ladder + GCP, still < 1024 chars; Purpose, Use When,
    Inputs #8 workload-shape, Workflow 7→8 steps, Output Format, Validation
    Checklist, Gotchas, Supporting Files) and its
    `references/decision-inputs.md` (new Abstraction-ladder section with the
    rung table + PlanetScale engine-heritage note; scoring rubric widened to
    rung × provider × posture; managed-vs-self-hosted table reframed as per-rung
    refinement). Evals checked — consistent, not edited (out of scope). No
    other skill and no validator/workflow file touched (→ `gate-guard` passes).
  - **Product-agnostic.** Brand names are generic market examples; "supabase"
    (on the standing privacy sweep list — the author's real backend) is named
    ONLY alongside its peer Neon as an industry Postgres-BaaS example, framed
    unambiguously as a market example, never as "our stack" — consistent with
    the existing generic `rls-policy-auditor` Supabase reference; no private
    project/path/URL named.
  - Validator: **182 skills, exit 0** (no skill added/removed; D43 count/family
    markers unchanged at 182/21). To be checked by `skill-quality-reviewer` for
    the decide-vs-map seam and the brands-as-examples framing.

- **D46 (2026-07-18) — Built `authority-invalidation-architect` (182→183), the
  symptom-triggered owner of the "change didn't take effect" access-bug class:
  a removed user still sees the data, a revoked role still works, logout
  doesn't end the session, a plan change still shows the old tier, a deleted
  item stays visible.**
  - **The gap (from the read-only D46 discovery, independently run twice —
    2026-07-17 and re-verified from scratch 2026-07-18, same verdict).** The
    MECHANISM existed as fragments across ≥8 skills — but every fragment is
    design-time, cause-vocabulary, or manual-only, and **no skill triggered on
    the symptom as the victim experiences it** (zero trigger-surface hits
    corpus-wide for "still has access" / "removed but still sees" / "didn't
    propagate"-class language). Three content blocks existed NOWHERE: (1)
    JWT/token-claims staleness — "JWT" appeared in exactly one skill
    (`rls-policy-auditor`, as trusted context source) and
    session-version/epoch/token-denylist had zero auth-context hits; (2)
    client-side state/data-cache purge on authority-change and logout (zero
    client-data-cache vocabulary corpus-wide); (3) the cross-surface verify
    battery for the CHANGED principal (`multi-tenant-security-tester` has no
    formerly-authorized actor class; the corpus DEMANDS the property three
    times — `authorization-matrix-designer`'s "state the mechanism",
    realtime's teardown, a `tenant-isolation-reviewer` reference probe — and
    designs it nowhere). Outcome A (widen existing descriptions) was rejected
    on measured arithmetic — the four candidates sit at 999/970/956/946 chars
    against the 1024 cap — and because N skills widened onto one symptom
    creates N-way routing ambiguity on exactly the attribution the victim
    lacks; Outcome C (adequately covered) was rejected because for the
    README's non-developer audience a fix reachable only through cause
    vocabulary is not coverage.
  - **What.** ONE skill owning the lifecycle CHANGE → PROPAGATE → VERIFY:
    classify the change and direction (deny first — revoked access must
    actually revoke; the removed user reports nothing, which is why the bug
    survives), inventory the eleven surfaces where old authority survives
    (per-surface map in `references/stale-authority-surface-map.md`: server
    sessions, JWT/token claims, client stores/data caches, shared HTTP/CDN
    caches, in-process/distributed caches, DB session context, realtime
    subscriptions, share links, entitlement resolution, search indexes,
    signed URLs), locate the holder by diagnostic tell ("works in incognito"
    → client copy; "fixes at a fixed interval" → token TTL), state an
    owner-confirmed revocation-latency bound (the sibling of
    caching-strategy-designer's consistency envelope, applied to authority),
    design invalidation per surface — OWNED: the token-policy menu
    (short-TTL+refresh vs session-version/epoch vs denylist, tradeoffs and
    resulting latency stated; a stateless token's revocation latency IS its
    access TTL unless a server-side check exists), server-session
    invalidation (replay rejected; clearing the client is presentation, not
    revocation), and client-state purge on logout AND authority-change
    (incl. the next-user-on-shared-device leak) — and verify with the
    deny-direction-first cross-surface battery for the CHANGED principal
    (not a fresh test user), grant direction and positive control included.
  - **The hard seam — compose, never restate (the D38 `project-orchestrator`
    pattern).** Cache mechanics stay with `caching-strategy-designer` — its
    authorization-caching Safety Rule is CITED as governing, never restated
    or re-approved; mid-connection re-auth/teardown with
    `realtime-subscription-architect`; plan resolution + webhook-lag with
    `plan-entitlement-architect`; link revocation with
    `share-link-access-architect`; RLS policy SQL with `rls-policy-auditor`
    (the new skill owns the FRESHNESS of the context feeding policies, plus
    pool reset); custody implementation with `secrets-identity-hardener`
    (manual-only — the new skill produces the named control it requires);
    the generic unknown-cause method with `systematic-debugger` (the new
    skill is the domain differential). Never-worked access routes to the
    correctness owners via the load-bearing discriminator *"did it behave
    correctly before the change?"* — pinned in Use When, Stop Conditions,
    and a trigger-eval. Per the discovery's anti-double-routing rule, NO
    existing skill's description was widened — the new skill is the single
    symptom-layer entry; the mechanism skills keep their cause-language
    triggers.
  - **Posture.** Design/diagnosis only — edits nothing, executes nothing
    against live systems → model-invocable (no `disable-model-invocation`).
    Stop Conditions: live purge/session-kill execution follows the ops
    approval path (`human-approval-boundary`); a proposed authz-result cache
    is never green-lit from here; an active cross-tenant leak routes to the
    isolation path immediately. Ships both eval files (evals + trigger-evals
    discriminating against 8 neighbors).
  - **Registration (D43 enforcement).** Catalog D46 section (+ intro
    narrative), README Skills-(shipped) D46 table, a NEW roster family 22
    (Authority invalidation & propagation, D46, 1), phase-plan D46 row,
    count bumps README `SKILL-COUNT` 182→183 and `FAMILY-COUNT` 21→22 (+ the
    human-readable prose across About/roles/map/getting-started, and the
    D1–D45→D1–D46 decisions range). Roles table: NEW row "an
    access-revocation and stale-authority specialist" (CONTRIBUTING 3e
    judgment, D42-row precedent: a genuinely new user-facing capability the
    table did not name — and the discovery's core finding was precisely this
    symptom's undiscoverability for the README's non-developer audience).
  - **Product-agnostic.** Brands appear only as house-style e.g. examples
    inside durable categories: "managed-auth platforms (e.g. Supabase,
    Firebase)" — Supabase named only alongside a peer, consistent with the
    D45 sweep rule and the existing `rls-policy-auditor` reference — and
    "query/data-cache libraries (e.g. React Query, SWR, Apollo)"
    (`secrets-identity-hardener`'s VITE_/NEXT_PUBLIC_ precedent). No private
    project names, paths, or URLs.
  - Validator: **183 skills, exit 0**; description 1021 chars (< 1024). To
    be checked by `skill-quality-reviewer` + `library-diff-reviewer` for the
    compose-vs-restate seam.

- **D47 (2026-07-18) — Built `superadmin-observability-console-designer`
  (183→184) — designs the cross-tenant superadmin OBSERVABILITY console
  (panel taxonomy + layered IA with restraint; the cross-tenant
  READ-security model: dedicated deny-all-RLS platform-admin registry, no
  self-service grant, three-layer server-side re-check,
  read-only-by-default with privileged-write-only telemetry,
  denied-access-as-metric, break-glass CONTENT-reveal; the server-shaped
  read model; honest-gap typing; the DB/query-perf panel spec;
  posture-as-verification-results + the DB self-monitoring caveat).**
  - Fills a genuinely UNOWNED gap (`admin-console-architect` punts telemetry
    → `observability-operator` operates backends → nobody designed the
    console; the three-way pointer had no owner). COMPOSES ~12 feed/adjacent
    skills rather than restating them.
  - Three seams: SEEING-vs-ACTING (`admin-console-architect` owns
    actions/elevation; this owns the read console + content-reveal
    break-glass), DESIGN-vs-OPERATE (`observability-operator`),
    CONSOLE-vs-FEED (slo / audit / security-logging / synthetic / metering /
    authz owners).
  - Grounded in a read-only discovery mining THREE real production
    implementations that independently converged on the read-security core;
    product-agnostic.
  - Roster: joins family 18 (SaaS architecture depth — strong cluster,
    D31, 10→11 — beside its acting-surface sibling
    `admin-console-architect`) rather than opening a second 1-skill family;
    FAMILY-COUNT stays 22. New roles-table row ("a superadmin console and
    platform-observability designer"). Count markers 183→184. No doctrine
    change.
  - To be checked by `skill-quality-reviewer` + `library-diff-reviewer` for
    the three seams.

- **D48 (2026-07-18) — Extended `aws-saas-architect` + `azure-saas-architect`
  security-posture coverage (skill-EDIT, count stays 184).**
  - **Azure:** added Microsoft Sentinel (SIEM/SOAR), Defender for Cloud CSPM
    + per-workload CWPP plans, Defender for Cloud Apps (CASB), Entra ID
    Protection + Conditional Access — a correctness fix (Azure's security
    suite is a primary enterprise-selection driver yet the mapper was
    weakest there, one posture-only mention).
  - **AWS parity:** added Inspector, Macie, Detective, IAM Access Analyzer,
    the Security Hub CSPM-vs-threat-correlation split, and Security Lake
    (OCSF) + Verified Permissions as first-class options.
  - Each service tied to the existing discipline (tenant isolation + cost +
    team maturity; SKU/tier/price = verification items); seam held
    (name/place services; deep threat-modeling →
    `threat-modeler`/`ai-threat-modeler`, detection-rule design →
    `security-logging-alerting-architect`, SIEM operation →
    `observability-operator`); provider product-naming (not
    brands-as-examples — these are the provider's own service names, the
    same class as Entra/Key Vault/GuardDuty already throughout both
    skills).
  - **Gap 2 (AI agent governance / Microsoft Agent 365): found ALREADY
    COVERED at the content level; no new skill, no agent-skill edits.** The
    Agent-365→skills map: agent registry/shadow detection →
    `agent-containment-reviewer`; agent identity/access/agent-to-agent →
    `agent-identity-privilege-reviewer` + `agent-harness-architect` +
    `agent-authorization-matrix` + `inter-agent-comms-reviewer`; fleet
    observability → `agent-containment-reviewer` (baselines) +
    `ai-cost-guardrail-designer` (spend), surfaced via
    `superadmin-observability-console-designer` (D47); agent data
    governance → `model-context-designer` +
    `memory-context-poisoning-reviewer` + `agent-memory-governance`; agent
    threat protection → the agentic-security cluster
    (`agent-goal-hijack-defender`, `agent-tool-safety-guard`,
    `prompt-injection-defender`, and peers). The agentic cluster +
    CONSTRAIN/CURATE + the D47 console ARE the vendor-neutral agent control
    plane; recorded a doctrine paragraph noting the equivalence
    (optional-b, `docs/ZERO_TRUST_AI_ENGINEERING_DISCIPLINE.md`).
  - GCP security suite recorded as banked content on the D45
    `gcp-saas-architect` banked item above (SCC, Google SecOps née
    Chronicle, Cloud Armor, Cloud IDS, Sensitive Data Protection, Assured
    Workloads, AI Protection/Model Armor) — no skill file created.
  - Grounded in a read-only D48 discovery (verified); Gaps 1 and 2 kept
    strictly separate. Sourced from a 2026 cloud-security-portfolio
    research pass. Validator: **184 skills, exit 0** (edit-only; D43
    count/family markers unchanged at 184/22).

- **D49 (2026-07-18) — Codex/Agent-Skills portability (AGENTS.md
  doc-bridge + MANUAL-ONLY sentinels; skill-EDIT + docs, count stays
  184).**
  - Shipped repo-root `AGENTS.md` (doc-bridge — natively ingested by Codex
    CLI, verified 0.138.0-alpha.7; no hardcoded skill count by D43
    discipline — an unenforced count surface is exactly the drift D43
    exists to prevent).
  - README section "Using Aegis with Codex CLI and other Agent Skills
    tools": out-of-the-box AGENTS.md path recommended; optional native
    `.codex/skills` copy documented user-side only, with four verified
    caveats; no committed copy — drift + silent-drop + truncation +
    ignored manual-only field.
  - MANUAL-ONLY sentinel (`MANUAL-ONLY; never auto-invoke. `, 32 chars)
    prepended to all 18 `disable-model-invocation` skills: Codex ignores
    the field and truncates descriptions to ~92 chars at selection time,
    so the front sentinel is the only guaranteed-visible position
    (A/B-validated in the discovery); 7 descriptions trimmed to fit the
    validator's <1024-char cap (the discovery predicted 6 against Codex's
    ≤1024 cap; this repo's validator is stricter by one character, which
    pulled `agent-goal-hijack-defender` in). Inert in Claude Code (the
    field is enforced there and user /invocation is unaffected),
    protective everywhere else.
  - Grounded in the empirical D49 discovery run in Codex CLI itself.
  - **BANKED FOLLOW-ON (D50 candidate):** strict-YAML normalization of the
    67 out-of-spec descriptions (single-quoting proven Codex-side;
    PRECONDITION: verify Claude Code renders a single-quoted description
    identically before the mass edit) + a HARD strict-YAML parse check in
    `validate-skills.py` so the corpus stays portable (touches the
    validator → gate-guard will fire → D43-style admin-merge expected).
  - Validator: **184 skills, exit 0** (skill-EDIT + docs; D43 count/family
    markers unchanged at 184/22).

- **D50 (2026-07-18) — Portability enforcement (strict-YAML normalization
  ×67 + validator hard checks + portability contract; skill-EDIT +
  validator + docs, count stays 184).**
  - Normalized the 67 strict-YAML-invalid descriptions to single-quoted
    scalars (parsed values byte-identical — pure serialization; precondition
    verified: Claude Code renders quoted descriptions identically, tested on
    `code-reviewer` before the mass edit — and the current build goes
    further: it FALLS BACK to the H1 title for strict-invalid frontmatter,
    so normalization restores description visibility in Claude Code's own
    selection listing too, not just in Codex-class consumers).
  - Validator hardened: strict-YAML frontmatter parse (HARD,
    `check_frontmatter_strict_yaml`), description length measured on the
    PARSED value (matching Codex's counting — quoting chars and doubled
    apostrophes don't count), MANUAL-ONLY sentinel position check for all
    `disable-model-invocation` skills (HARD, `check_manual_only_sentinel`)
    — each proven able to fail on-branch before merge. Requires PyYAML
    (fail-closed; installed in the CI workflow).
  - Portability contract added to skill-generation-standard + `_template`
    (description now models the quoted, front-loaded shape) + CONTRIBUTING;
    README caveat 1 updated (silent-drop fixed; three live caveats remain).
  - The corpus is now portable BY CONSTRUCTION: any future skill either
    satisfies the contract or fails CI. Gate-guard fired by design
    (validator + workflow change); admin-merged after review per D43
    precedent.
  - Validator: **184 skills, exit 0** (D43 count/family markers unchanged
    at 184/22).
  - Post-review hardening (same PR): sentinel check made bidirectional +
    block-scalar descriptions rejected (both proven able to fail); PyYAML
    install documented for local runs; the retroactive D49 annotation
    reverted to keep §5 append-only. Source: Codex-review P2s on PR #59.

- **D51 (2026-07-18) — Guided-paths layer (README "Start here" picker +
  3 path docs; DOCS build, count stays 184).**
  - README "Start here: pick your path" five-door picker replaces the
    one-door pointer after the roles table; D39's idea→shipped section
    unchanged as door 1; door 5 routes to `project-orchestrator` stages
    8–9 — no launch doc, it would restate the orchestrator.
  - Three path docs: `docs/paths/check-your-app.md` (the flagship —
    closes the verified unowned "is my app safe?" cold prompt),
    `docs/paths/add-ai-safely.md` (sequences ~20 owners that had no
    journey), `docs/paths/something-is-broken.md` (the symptom→owner
    table, routing TO the D46 cluster owner).
  - Discriminator: paths name WHO+ORDER+yield+handoff, never HOW (the
    D38/D46 pattern); path docs link `.claude/skills/` directly so
    breakage is click-visible; MANUAL-ONLY skills flagged
    name-it-explicitly, composing the D49/D50 sentinel discipline.
  - Grounded in the read-only D51 discovery (33/33 sequence skills
    verified on disk; goals (i)/(v) deliberately NOT given docs — the
    same test that approved (ii)/(iii)/(iv)). Maintainer "Start here"
    heading retitled "Canonical reading order (for maintainers)" to end
    the phrase collision.
  - BANKED: (1) validator check that `docs/paths/` skill-references
    resolve on disk — implement in the next validator-touching batch
    (gate-guard economy); (2) a payment-processor-integration skill
    candidate (the goal-(v) capability gap: checkout, webhooks, PCI
    posture).
  - Validator: **184 skills, exit 0** (no SKILL.md touched; D43/D50
    markers, roster, and workflows unchanged — normal human merge).

- **D52 (2026-07-19) — External-audit correction batch (skill-EDIT + docs;
  count stays 184).**
  - Source: independent external audit of main at `40a39b9`; the five
    correctness findings selected for this batch were re-verified against
    current main before editing.
  - Fixed:
    1. Replaced the stale `~96` live count in `skill-quality-reviewer` with
       countless full-corpus wording. D43 protects marked README counts, but
       live skill prose had no equivalent protection.
    2. Updated `project-orchestrator` Stage 8 routing to follow the D45
       cloud decider's outcome: AWS/Azure use their shipped mappers; the
       modern managed tier follows the decider's emitted seam-owner
       handoffs; GCP pauses the mapping hop at the missing-mapper boundary
       for human direction (no invented mapper, no silent rerouting);
       `iac-reviewer` is conditional on an actual IaC/config-as-code
       artifact; the remaining stage-8 chain stays unconditional.
    3. Changed project-state recording to propose → exact preview →
       explicit content-specific approval → append, aligned across
       Workflow, Output Format, Validation Checklist, Gotchas, Stop
       Conditions, and evals. Updated the authoring standard (both the
       frontmatter row and §5) and the canonical template with the narrow
       approved-write exception; autonomous and high-authority mutations
       remain manual-only.
    4. Removed the two divergent `docs/templates` files, retained
       `.claude/skills/_template/` as the single canonical template,
       repointed current links (including the template's own back-link),
       and removed both duplicate catalog rows.
    5. Annotated the auto-merge policy's Repo field with the Project-Aegis
       rename while preserving the dated record.
  - BANKED from the same audit for D53 (one gate-touching batch,
    discovery-first, after scope approval): validator fixture tests; strict
    required-section ORDER validation; `.claude/agents/` schema and
    read-only tool validation; `docs/paths/` skill-reference resolution;
    action full-SHA pinning and validator dependency pinning; CODEOWNERS
    and Dependabot; assessment of a live-prose current-count heuristic.
  - OWNER-DECISION items (not AI-selected policy): LICENSE choice;
    SECURITY.md reporting channel; repository-setting auto-merge
    capability.
  - STRATEGIC NEXT ARC: behavioral eval runner — discovery-first,
    advisory-first, piloted on high-blast-radius skills; structural
    validity must not be presented as behavioral proof.
  - Post-review alignment (same correction batch; PR #61 merged
    `dbc6690` before this follow-up landed): skill-quality-reviewer's
    Check 7, description shorthand, and posture reference table updated
    to carry the standard's §5 approved-write exception (all three still
    enforced the pre-D52 absolute rule); README's current-layout line
    dropped the deleted `templates/` directory. Source: second-pass
    external review of the executed batch.
  - Post-merge posture-alignment (D53, PR #63): a classified proximity
    census found the earlier follow-up's sweep understated remaining
    normative surfaces; all (N) surfaces now carry the §5 pointer
    (README.md:1166 authoring rule, README.md:1250 principles bullet,
    docs/skill-generation-standard.md:177 final checklist); Check 7
    aligned to "creates or appends"
    (skill-quality-reviewer/SKILL.md:107); the posture table's excluded
    list completed with agent-instruction, security, identity, and
    authorization files
    (skill-quality-reviewer/references/quality-review-checklist.md:169);
    allowed/forbidden approved-write eval cases added. Sources:
    post-merge automated review of PR #62 + the in-session census.
    *(Re-checked 2026-09-30: all three line numbers in this sentence have
    moved — the README authoring rule is now :1354, the README principles
    bullet is now :1479, and the standard's §8 checklist row is now :593;
    the checklist's posture-table row is now :175 and its text was reworded
    to "Exception 1". The surfaces and the §5 pointer they carry are
    unchanged; the numbers above are kept as the D52/D53-time values.)*

- **D53 (2026-07-19) — Posture-rule alignment (docs + skill-EDIT; count
  stays 184).**
  - Census-driven (PR #63): a classified proximity scan (±6-line windows
    over README, CONTRIBUTING, AGENTS.md, the standard, the catalog,
    `docs/paths/`, `_template`, and skill-quality-reviewer + its
    references) classified every `disable-model-invocation` /
    side-effect-rule occurrence NORMATIVE / DESCRIPTIVE / HISTORICAL;
    only the five (N) surfaces lacking the exception in context were
    edited.
  - Fixed: the §5 pointer (cite-don't-restate — full exception text
    stays only in the standard §5, the frontmatter row, and the posture
    table) on README's authoring rule and principles bullet and the
    standard's final checklist; skill-quality-reviewer Check 7 aligned
    to the standard's "creates or appends a non-executable
    documentation/state file" wording; the posture reference table's
    excluded list completed in substance (agent-instruction /
    behavior-steering files; security, identity, authorization files);
    one ALLOWED eval case (compliant §5 approved-write → Check 7 PASS,
    no posture flip) and one FORBIDDEN eval case (approved-write-shaped
    behavior targeting AGENTS.md / an authorization file → Check 7
    FAIL, manual-only required).
  - Verified-compliant and left unchanged: the standard §5 itself
    (:128/:141-142 governed by its own "with ONE narrow exception,
    next"), the frontmatter row (:39), `_template` (:4-15, :59, :76-80),
    and the checklist's §5 citations (:147, :168); all descriptive
    manual-only listings (catalog, README tables, `docs/paths/`) and
    historical records untouched.
  - NEXT: companion D54 = project-orchestrator correctness (incl. the
    banked explain-the-why edits); the gate-touching batch banked under
    D52 moves to D55.
  - Validator: **184 skills, exit 0**; evals JSON parses (7 cases); no
    `scripts/` or `.github/` files touched — normal merge.
  - **Correction (appended, no rewrite of the D53 record; every citation
    re-verified 2026-09-30 against `origin/main` at `2184b54f`).** The
    Verified-compliant citations above are stale: each cited line number was
    correct when D53 landed at `dd26dab1`, and each target still exists, but
    none of the numbers resolves to the intended text now (the standard was
    rewritten for TALI v3.2.3 in 2026-08-02 and re-read in 2026-09-29; the
    template was reflowed by D54, D56 and #528). Verified target by target:
    - **`:128`** — was the standard §5 rule's `... requires
      `disable-model-invocation: true` ... with ONE narrow exception, next.`
      That phrase no longer exists anywhere in the repo: the D53-era §5
      bullet is now standard lines **254-258**, and §5's approved-write
      exception is now **EXCEPTION 1** at standard lines **272-300** (with
      EXCEPTION 2 / TALI at **302**). What line 128 holds today is unrelated
      portability text (`simply does not exist there.`).
    - **`:141-142`** — was the exception's exclusion list (`or other
      irreversible action. Those remain manual-only and require
      `disable-model-invocation: true`.`). That is now standard lines
      **294-300**; lines 141-142 now carry host listing limits (Claude Code
      1,536 characters; Codex ~2% of the window) inside the Portability
      contract.
    - **`:39`** — the standard's frontmatter row is still a frontmatter row
      in the same table with the same meaning, but it is now line **99**
      (the table grew: §2 now spans lines 91-106). Line 39 now ends
      "invocation commands." Line 99 also carries the current form of the
      exception the row points at (Exception 1, plus the TALI mirror).
    - **`_template` `:4-15`** — the comment block still exists and still
      starts at **line 4**, but it grew from 12 lines to 15, so the intended
      span is now **:4-18**.
    - **`_template` `:59`** — was the Validation Checklist's approved-write
      gate ("Any side-effecting step was gated behind explicit human
      confirmation..."). That gate now lives in the checklist item at
      **:77-82**. Line 59 is now inside the build-choice paragraph
      (`deciding facts are known; never invent a recommendation.`); the
      Validation Checklist now begins at :70.
    - **`_template` `:76-80`** — was the same rule restated in **Stop
      Conditions** ("Before a documentation/project-state append under the
      standard-§5 approved-write exception..."). It is now a substantially
      longer Stop Conditions entry at **:99-111**; the template's Validation
      Checklist item ":76" is now "No **Stop Conditions** were silently
      bypassed." Lines 76-80 no longer contain the cited text.
    - **checklist `:147` / `:168`** — the checklist grew by six lines between
      D53 and now, so both shifted by **+6**, not the two the review
      estimated: the Stop Conditions entry ending `irreversible step here
      (standard §5).` is now **:153-154** (D53-era :147-148), and the Check 7
      posture table's first body row — D53's :168 — is now **:174** (:175 is
      the Exception 1 row the D52 block above cites as :169 at its own
      date). Line 168 today is unrelated Check 6 prose (`grep) is a CONCERN
      the other direction — fold it into its natural parent.`).
    - **Unchanged and still exact:** `skill-quality-reviewer/SKILL.md`
      **:107** (still the "§5 Exception 1 for bounded documentary writes"
      sentence). The README's authoring rule and principles bullet that D52
      and this D53 block cite are no longer at README :1166/:1250 — they are
      now README **:1354** and README **:1479** (both still carry the §5
      pointer, now naming two exceptions), and the checklist's posture-table
      row is now **:175**. D52's follow-up `standard:177` is now **:593**
      (the §8 checklist row).

- **D54 (2026-07-19) — Orchestrator correctness (skill-EDIT + docs;
  count stays 184).**
  - Source: correctness review of `project-orchestrator` after the D52/D53
    posture-alignment batches; five fixes, all in the orchestrator's own
    files plus one sentence in the authoring standard.
  - Fixed:
    1. **Append-only state model.** The state-file template kept mutable
       header fields (`Last updated` / `Current stage` / `Next recommended
       action`) that the §5 create-or-append-never-overwrite contract could
       not legally update. Replaced with a second append-only entry type — a
       dated **STATE SNAPSHOT** (stage + next action) — under the same
       propose → approve → append flow, latest-snapshot-wins; the schema and
       the worked example now model exactly two entry types (DECISION,
       SNAPSHOT), and Capabilities 1-2 read the latest snapshot for current
       stage. No field is ever overwritten.
    2. **Approved-create cold start.** When no `docs/project-state.md`
       exists, the orchestrator now previews the COMPLETE initial document
       (exact path + full initial content, including the first SNAPSHOT),
       asks one explicit approval, and creates only after the yes — the
       create leg of §5's "create or append"; decline/ambiguous creates
       nothing. Cold-start eval updated to assert it.
    3. **Manual-only routing invariant.** Stated ONCE as a general rule:
       before routing to any skill, check its invocation posture; a
       manual-only target (`disable-model-invocation: true`) is never
       invoked on the strength of the orchestrator's own auto-invocation —
       explain the boundary in business terms, STOP the hop, and have the
       USER invoke it by name (the `docs/paths` convention). Noted why it
       matters cross-tool: consumers that ignore the posture field have only
       this text and the description sentinel. The four known routings
       (stage 4 `prompt-injection-defender`, stage 7
       `playwright-e2e-engineer`, stage 8 `ci-pipeline-architect` +
       `observability-operator`) are tagged lightly, citing the invariant.
       One eval added: the stage-8 flow hands manual-only skills to the
       user, never auto-chains them.
    4. **IaC eval scope.** Removed "a deploy workflow config" from the
       IaC-artifact examples in `evals.json` (that is
       `ci-pipeline-architect`'s turf per `iac-reviewer`'s own exclusions);
       kept the Terraform/Bicep/CDK-class examples.
    5. **Required chosen-over rationale** (the banked explain-the-why edits,
       folded from the D46/D52 ledger): every proposed DECISION entry MUST
       carry the "(chosen over …, because …)" clause — the main rejected
       alternative and the plain-language why — surfaced in the propose-step
       preview so the user learns the trade-off at every approval.
       Capabilities 3/4, the template schema + worked example, and the
       preview/approval eval all assert it; plus one sentence in the
       authoring standard's Output Format guidance
       (`docs/skill-generation-standard.md` §4 item 5): decision/design-class
       skills state what was chosen, why, and the main rejected alternative
       in plain language.
  - Clarification (appended, no rewrite of the D52 record): D52's stage-8
    "unconditional" `ci-pipeline-architect` → … → `incident-response-runbook`
    chain meant unconditional-on-INPUTS (it runs regardless of the
    platform/artifact evidence that gates `iac-reviewer` and the provider
    mappers) — NOT unconditional-on-posture. The manual-only members of that
    chain are now routed posture-aware via the D54 invariant: still always
    part of the flow, but handed to the user by name rather than
    auto-invoked. The two facts compose; neither supersedes the other.
  - Frontmatter description left unchanged: a semantic re-read confirmed it
    still accurately describes the skill (front door; detect stage; route by
    name; one plain-language question; record every dated decision; human as
    approval/merge gate) — the D54 fixes refine HOW those hold, not WHAT the
    skill does.
  - NEXT: D55 = the gate-hardening batch banked under D52 (validator fixture
    tests; strict required-section ORDER validation; `.claude/agents/` schema
    + read-only tool validation; `docs/paths/` skill-reference resolution;
    action full-SHA pinning + validator dependency pinning; CODEOWNERS +
    Dependabot; live-prose current-count heuristic) — discovery-first, one
    gate-touching batch after scope approval.
  - Validator: **184 skills, exit 0**; evals JSON parses (10 cases); no
    `scripts/` or `.github/` files touched — normal merge.

- **D55 (2026-07-20) — Gate hardening: the validator's first self-tests, four
  new hard checks, and supply-chain pins (tooling/config only; count stays
  184).**
  - Scope: ONE deliberately gate-touching batch, discovery-first. It edits
    `scripts/validate-skills.py` and `.github/workflows/validate-skills.yml`,
    so the `gate-guard` job fails **by design** (D43 precedent) and a human
    admin merge is required; the `validate-skills` job must be green or the
    batch is not ready. **Zero `.claude/skills/` files touched** — no skill
    content, no README, no CONTRIBUTING.
  - **The meta-gap closed.** The single load-bearing merge gate had no tests at
    all. Every hard check it had grown — the D43 count markers, the D50
    strict-YAML / sentinel / block-scalar trio — was hand-proved once in a pull
    request description and never proved again. `scripts/tests/test_validator.py`
    now re-proves them on every CI run (38 assertions), wired in as a step
    BEFORE the validator step; the `gate-guard` job's logic is untouched.
    Plain-python asserts, NOT pytest: the repo's whole dependency surface is one
    package and the validator fails closed on it, so adding a framework to test
    one script would invert that minimalism. Every bad fixture is paired with
    the error text it must produce, and the suite header documents the one-line
    mutation that turns it red — so "proven able to fail" stays re-checkable
    rather than being a claim in a commit message.
  - INCLUDED (items 1-5 and 7):
    - **Item 1 — validator self-tests + fixtures** (above). Fixtures live
      outside every directory the validator scans, so a normal run never
      discovers them.
    - **Item 2 — section ORDER, not just presence.** `ordered_headers()` (with
      `section_headers()` now its `set()` twin, so the two cannot drift) plus
      `check_section_order()`: required headers in body order, deduped, must
      equal the canonical order restricted to those present — so optional
      sections such as **Safety Rules** interleave freely — and a required
      header written twice is its own error. A skill could previously ship the
      nine required sections scrambled and pass.
    - **Item 3 — `.claude/agents/` schema.** Seven reviewer agents sat wholly
      outside validation, their read-only contract nothing but prose in each
      file. Now: frontmatter strict-parses; `name` equals the filename stem;
      `tools` (the field is `tools`, NOT `allowed-tools`) stays inside
      {Read, Grep, Glob}, with ANY widening an error — the one
      security-relevant check in the batch, since a Write/Edit/Bash grant turns
      a reviewer into an actor; `model`, when present, is recognised.
    - **Item 4 — guided-path link resolution.** Every
      `.claude/skills/<n>/SKILL.md` link in `docs/paths/*.md` and every
      `docs/paths/*.md` link in the README picker must resolve on disk, plus a
      paired-token rule (in ``[`foo`](.../bar/SKILL.md)``, `foo` must equal
      `bar`) that catches drift resolution cannot: the link works, so the doc
      reads as fine, while the reader is named one skill and sent to another.
      This automates the manual "on rename or retire, grep `docs/paths/`" step
      that D51 left as a convention — and conventions that depend on
      remembering are the ones that rot.
      - **Half deliberately NOT built**, recorded in a comment beside the
        check: "every backticked kebab-case token must name a skill". It passes
        today only by luck (0 non-skill tokens exist right now); the first path
        doc to write `read-only` or `fail-closed` in backticks would fail a
        correct sentence, and a verifier that fires on correct prose is worse
        than no verifier.
    - **Item 5 — supply-chain pins, made self-enforcing.**
      `check_workflows_sha_pinned()` was added and watched FAILING against the
      real, still-unpinned workflow (3 errors) before the pins were applied —
      the check is what converts "we pinned once" into "a floating tag cannot
      come back"; abbreviated SHAs are rejected too, local composite actions
      left alone. Tags resolved at build time, not from memory:
      `actions/checkout` v7 → v7.0.0 → `9c091bb2…`, `actions/setup-python`
      v6 → v6.3.0 → `ece7cb06…`, each carrying a `# vX.Y.Z` comment for
      legibility. New `requirements.txt` pins `pyyaml==6.0.3` — the current
      release, verified against PyPI at build time rather than the `6.0.2` the
      discovery report anticipated. Exact rather than a range (the gate depends
      on `safe_load` semantics, so CI should be reproducible rather than merely
      recent) and in a file rather than inline, so dependabot's pip ecosystem
      can see it.
      - Check and pins ship in ONE commit on purpose: splitting them would
        leave a commit on the branch whose validator exits 1, and a red commit
        nobody intends to keep is a trap for `git bisect`. The fixture-first
        ORDER is preserved in the authoring, which is what the discipline is
        actually for.
    - **Item 7 — dependabot** (github-actions + pip, weekly, both at `/`),
      explicitly as item 5's maintenance arm. **The coupling is the point:** a
      SHA pin and an exact version pin freeze the supply chain at review time,
      which is the intent, but a frozen pin with nobody to thaw it silently
      stops receiving upstream security patches. Pins without a bumper rot; a
      bumper without pins has nothing to do — if 5 were out, 7 would be out
      too. `.github/dependabot.yml` is not under `.github/workflows/`, so
      adding it does not itself trip `gate-guard` (verified against the guard's
      own regex); bot PRs that bump a workflow SHA will trip it, which is
      correct — a bot editing the merge gate should not be able to merge
      itself.
  - DROPPED (items 6 and 8), with reasons:
    - **Item 6 — CODEOWNERS.** Solo maintainer: it routes review to self, and
      GitHub does not let you approve your own PR to satisfy a required review,
      so a CODEOWNERS-backed requirement can *block* the admin-merge flow
      rather than aid it. Its one cited upside — documenting protected paths
      for future contributors — is already served, and served with teeth, by
      the `gate-guard` job plus the CONTRIBUTING prose. A CODEOWNERS file with
      no second human to route to is documentation cosplaying as enforcement.
      Revisit only if a second maintainer joins.
    - **Item 8 — live-prose current-count heuristic.** Live and historical
      counts are textually identical: README:76's "175 skills" is a frozen D33
      milestone, README:111's "184 skills" must track disk, and this
      reconciliation log holds roughly forty more legitimate frozen counts. A
      regex over bare `N skills` has no signal to tell them apart, so it would
      either false-positive on every historical entry or, tuned away from that,
      catch nothing. *A verifier that cannot fail correctly is theater with an
      exit code.* The real defense already exists and needs no new check: the
      D43 `SKILL-COUNT` / `FAMILY-COUNT` markers pin the one authoritative live
      count machine-checked, and the countless-full-corpus wording convention
      installed in D52 keeps other prose from asserting a number at all.
  - **The three censuses that made this batch content-free** — each re-run at
    build time rather than trusted from the discovery report, because a census
    gone stale would silently turn a "ships green" check into a skill-content
    edit: section-order **0 offenders across 184** (and 0 duplicate required
    headers); agents **7/7 conform**; `docs/paths` **33 links, 0 unresolved, 3
    picker links, 0 mismatched pairs**. All three held, so all four new checks
    shipped green and no skill file was edited. (One discovery-report nit found
    and not acted on: its agent table transposes the `model` values of
    `release-readiness-reviewer` and `senior-troubleshooting-lead`. Both are in
    the allowed set, so the 7/7 verdict is unaffected.)
  - RESIDUAL, deliberately deferred: README:111's **unmarked** live count
    ("184 skills … 22 discipline families") duplicates the marked line at :523.
    The next count bump will update :523 under D43 and leave :111 stale. It is
    unfixable by a gate check — the same theater problem as item 8 — and
    trivially fixable by a one-line docs edit (reword to drop the bare live
    count, or wrap both numbers in the D43 markers). That is content, so it
    belongs to a future docs pass and is explicitly not part of this gate
    batch.
  - Validator: **184 skills, exit 0, 0 warnings** with all four new checks
    active; self-tests **38/38**. `scripts/validate-skills.py` and
    `.github/workflows/validate-skills.yml` ARE touched — `gate-guard` **red by
    design, human admin merge required**.
  - **Correction (appended, no rewrite of the D55 record; verified
    2026-09-30 against `origin/main` at `2184b54f`).** The RESIDUAL note
    above is preserved as provenance, and the item-8 heuristic claim it rests
    on no longer describes `main`:
    - The live/historical collision it cites no longer exists in that shape.
      README:111's bare "Under the hood, Aegis is a library of 184 skills
      organized into 22 discipline families" line was replaced by README
      **62** ("Under the hood, Aegis is a library of skills organized into
      discipline families — the marked totals in …"), i.e. countless, so
      there is nothing left for the heuristic to distinguish there.
    - README:76's "175 skills" is gone from the README entirely; the historical
      counts now live in `docs/HISTORY.md` (**82** "175 skills", **117** "184
      skills"), moved there by D57.
    - The one governed `SKILL-COUNT`/`FAMILY-COUNT` marker pair is now README
      **557** (not :523), and it reads **195** skills in **23** families.
    - So the RESIDUAL's two options were both effectively taken later: the
      duplicate live count was reworded countless (D56), and the marker pair
      that remains is the single governed one.

- **D56 (2026-07-20) — Multi-agent identity: the README framed for the open
  Agent Skills ecosystem, Claude Code as the reference surface (docs-only;
  count stays 184).**
  - Scope: `README.md`, the three `docs/paths/*.md` guided paths, and this
    entry. No `scripts/`, `.github/`, or `.claude/` files — so `gate-guard`
    passes and both CI checks are green. The skill corpus is untouched; this is
    a framing pass, not a content one.
  - **Why now.** D49/D50 made the corpus Agent-Skills-standard portable and
    proved it in Codex (185/185 native-parse, the `AGENTS.md` bridge, the
    32-char MANUAL-ONLY sentinels). The README's tools section (:418) already
    told that multi-tool truth, but its *identity* — the hero paragraph, the
    About block, the roles intro — still called Aegis "a reusable Claude
    engineering shield." The framing lagged the shipped reality; this closes the
    gap without touching a single skill.
  - **The classified census drove the edits** (D53 pattern — the fix list is
    derived, not guessed). Every Claude-mentioning line in the README and the
    three path docs was classified K / G / T:
    - **G — GENERALIZE (identity/framing that presented Aegis as Claude-only):
      11 sites, all fixed.** The hero identity block; four About-paragraph
      echoes ("reusable Claude engineering operating system", "reusable Claude
      Code skills", "so Claude operates like…", "where Claude models before
      coding"); the roles intro ("make Claude act as"); the picker lead; the
      picker launch door ("tell Claude Code"); and the three `docs/paths` "How
      to run it" leads. Each now names the tool-neutral reality — "your coding
      agent" / "your agent tool (Claude Code, Codex CLI, or any Agent Skills
      tool)" — with Claude Code named first as the reference surface.
    - **T — TOOLS-ANCHOR: 0 pre-existing lines restated the multi-tool content**
      (it was already contained at the tools section), so the anchor work was
      additive — the bold tools lead was promoted to a real `####` heading so it
      finally has a resolvable anchor, and six pointers now cite it: the
      Getting-Started cross-tool lead-in plus the five auto-selection honesty
      clauses.
    - **K — KEEP (Claude-Code-specific FACTS): untouched.** The Getting-Started
      Options 1–6 install walkthroughs with their URLs and `claude` commands,
      the tools-section body, every `.claude/…` path literal, the historical
      `claude-skills-*` doc filenames, the Safety note, and the two
      reference-surface instructions ("Paste this into Claude Code";
      check-your-app.md's "ask Claude Code to explain"). These are correct
      instructions for a real surface, not Claude-only framing.
  - **The asymmetry was preserved, not flattened — the point of the pass.** No
    parity claim was added anywhere. The one true difference stays stated at the
    tools section verbatim: **only Claude Code natively enforces
    `disable-model-invocation`; every other tool relies on the 32-char
    MANUAL-ONLY description sentinel plus the `AGENTS.md` rule, which reduce
    auto-invocation risk but are not enforcement.** The "verified against
    codex-cli 0.138.0-alpha.7 on 2026-07-18" honesty framing is left exactly
    where cross-tool behavior is asserted.
  - **The four instructional leads** (the README picker lead + the three path
    "How to run it" leads) now generalize the "describe it and the right skill
    selects itself" flow to any Agent Skills tool and carry ONE honesty clause
    where auto-selection is implied: selection quality varies by tool — Claude
    Code reads the full descriptions, some tools' native selection reads only a
    short prefix. The full clause is stated once in the README picker lead; the
    path docs cite it rather than restate the caveats.
  - **The :111 residual, deferred by D55, is cleared.** The unmarked live count
    ("184 skills … 22 discipline families") that duplicated the marked line at
    :523 is now itself wrapped in the D43 `<!-- SKILL-COUNT -->` /
    `<!-- FAMILY-COUNT -->` markers, so both numbers are machine-checked against
    disk and the next bump cannot leave :111 stale — the marker option the D55
    residual note anticipated. The frozen historical counts (:76's "175", the
    phase-narrative "184") stay deliberately unmarked.
  - **`AGENTS.md` needed no change** — it was already tool-neutral (it points
    agents into `.claude/skills/` and names no vendor as the owner), so the doc
    bridge and the README framing now agree without editing it.
  - Validator: **184 skills, exit 0, 0 warnings**; self-tests **38/38**. Both
    count-marker pairs (:111 and :523) reconcile against disk; the D55
    guided-path link check stays green (the picker edits touched no path-doc
    link). No `scripts/` or `.github/` files touched — normal merge.
  - **Follow-up (same PR):** the :111 marker pair was reverted to countless
    wording — `check_readme_counts` governs only the FIRST marker instance
    (`.search`), so a second pair leaves one silently ungoverned; exactly one
    governed pair restored. Extended the census fixes to `standard:3` and
    `catalog:93` (identity-class mentions outside the original scope). Source:
    post-build review against the combined prompt. *(Correction appended
    2026-09-30: the `catalog:93` target — the "Skills vs. Agents" table's
    "A reusable *procedure* … Claude loads and executes" row — has since been
    reworded to "…the agent loads and executes" and moved by the catalog's
    2026-09-30 surface edit; it is now `docs/skills-catalog.md:249`. The
    `standard:3` target is the standard's opening sentence, still line 3 but
    rewritten for the open Agent Skills format by D49/D56-era edits. Cited
    line numbers are preserved as provenance; the fixes they name are intact.)*

- **D57 (2026-07-20) — About restructure: the construction history
  relocated to `docs/HISTORY.md`; the README leads with what-it-is and the
  Start-here picker (docs-only; count stays 184).**
  - Scope: `README.md`, the new `docs/HISTORY.md`, and this entry. No
    `scripts/`, `.github/`, or `.claude/` files — `gate-guard` passes and
    both CI checks are green. The skill corpus is untouched; this is a layout
    pass, not a content one.
  - **Why.** The About block ran identity → name story → then a wall of
    construction history (Phase 0 … Phase 7.5, the D12 craft-pack run, the
    per-decision recap through D47/184). Popular-repo READMEs (FastAPI, React,
    LangChain) answer "what is this and why should I care" in seconds and LINK
    the history rather than showing it; the narrative was correct but buried
    the orientation a newcomer needs and pushed the "Start here" picker far
    down the page.
  - **The move (verbatim relocation, append-only spirit).** README lines
    31–86 — the entire phase/decision prose narrative, "The repo is built in
    **phases** …" through "… bringing it to **184 skills** (183→184)." — were
    lifted byte-for-byte into `docs/HISTORY.md` under a three-line intro that
    names the reconciliation log (D1–D56) as the authoritative record and
    links back to the README. Byte-identity proof: the 56-line / 5795-byte
    region hashes identically pre-move (extracted from the README) and
    post-move (the body of `HISTORY.md`, intro excluded) —
    `sha256 b8c16a347fc22b1a187dd4942f664961f327279163753bb1bf8fe9743fcb18ce`.
    Zero content lost; the historical counts inside the narrative (175 through
    184, plus every per-pack size) are preserved untouched — they are history,
    correctly frozen.
  - **The replacement (one new paragraph, countless).** In its place, a short
    "How it's built" paragraph: built in validated phases, every addition
    recorded as an immutable dated decision in the reconciliation log, nothing
    merged without independent audit and a green validator, full story →
    `docs/HISTORY.md` and decision-by-decision record → the reconciliation
    log (both linked). The paragraph carries no counts (countless rule); its
    only digits are the linked filename `step-0-reconciliation-v4.md`.
  - **Result.** README 1272 → 1221 lines (−51). The "Start here: pick your
    path" picker rose from line 139 to line 88 — substantially earlier, the
    point of the pass. Nothing below the About block was reworded; the
    Decision Log table (the structured D1…D47 record, including its own
    "183→184") stays in the README as a separate representation. The one
    governed `SKILL-COUNT`/`FAMILY-COUNT` marker pair (:485 post-move) is
    unmoved and reconciles at 184. No dangling anchors — the moved prose held
    no headings, so nothing anchored into it, and all 8 internal README
    anchors still resolve to their 22 headings.
  - Validator: **184 skills, exit 0, 0 warnings**; self-tests **38/38**. `git
    diff --check` clean; private-name sweep clean on all new and moved-intro
    prose. No `scripts/` or `.github/` files touched — normal merge.
  - **Correction (appended, no rewrite of the D57 record; verified
    2026-09-30 against `origin/main` at `2184b54f`).** Every figure in this
    entry was re-derived and all still hold: the `sha256
    b8c16a347fc22b1a187dd4942f664961f327279163753bb1bf8fe9743fcb18ce`
    byte-identity proof is reproducible (README lines 31-86 at `abecf4e5^`
    and `docs/HISTORY.md` lines 8-63 at `abecf4e5` both hash to exactly that
    value, 5795 bytes, CRLF-joined), the picker did rise from line 139 to
    line 88 at this commit, and the D43 marker pair did sit at README :485.
    Only the *current* numbers have moved since: the picker is now README
    **88-118** ("### Start here: pick your path" at :88), the single governed
    marker pair is now README **557**, and the README carries **26** headings,
    not the 22 recorded then — so "all 8 internal README anchors" is a
    D57-time statement, not a current count (the README now has **12**
    distinct same-page anchor targets, all resolving; the D57-era "22
    headings" figure no longer matches either).
  - **Companion owner actions (outside the repo).** The GitHub "About"
    description and topics are set by the owner to the agreed plain-language
    text, so the repo's own front matter now matches this framing. **Next:
    D58 — the open-source readiness pack — is planned, pending the license
    decision.** _Appended 2026-09-30, verified against `origin/main` at `5c806348`: D58 is no
    longer pending: the pack is delivered. All eleven files in its scope are on `main` —
    `LICENSE` (Apache License 2.0), `NOTICE`, `TRADEMARKS.md`, `SECURITY.md`,
    `CODE_OF_CONDUCT.md`, `.github/CODEOWNERS`, `.github/pull_request_template.md`, the
    `CONTRIBUTING.md` "External contributions" section, the two `README.md` touches (the
    "License & contributing" section and the `ModernNomad-98` clone URL), the
    `auto-merge-policy.md` header annotation and the D58 entry itself. They landed in
    `e18830f8` (PR #70) and `gh api repos/ModernNomad-98/Project-Aegis` reports the licence as
    `Apache-2.0`. The D58 wording above is left as written; the owner-only settings it listed
    are tracked in its own owner-action ledger below._

- **D58 (2026-07-21) — Open-source readiness pack: an Apache-2.0 license,
  trademark and security policies, code-owner review, a code of conduct, and a
  DCO-based contribution model (governance/docs only; count stays 184).**
  - Scope (eleven touches): new `LICENSE`, `NOTICE`, `TRADEMARKS.md`,
    `SECURITY.md`, `CODE_OF_CONDUCT.md`, `.github/CODEOWNERS`, and
    `.github/pull_request_template.md`; a new "External contributions" section
    appended to `CONTRIBUTING.md`; two `README.md` touches (a "License &
    contributing" section and the clone URL); one annotation in
    [`auto-merge-policy.md`](auto-merge-policy.md); and this entry. No `scripts/`,
    no workflow files, no `.claude/`. `.github/CODEOWNERS` and the PR template sit
    outside `.github/workflows/` and match nothing in `gate-guard`'s regex, so
    both CI checks stay green and this merges normally. The skill corpus is
    untouched.
  - **License rationale (Apache-2.0).** Chosen for three properties this library
    needs: §5 licenses inbound contributions under the same terms **without a
    CLA** (contributors sign off with the DCO instead); §6 grants **no trademark
    rights**, which — paired with `TRADEMARKS.md` — lets the material be freely
    forked while the **"Project Aegis"** and **"Zet-AI Engineering"** names stay
    protected; and its explicit patent grant with a termination-on-litigation
    clause gives downstream users patent clarity a bare MIT/BSD notice does not.
  - **Copyright-holder convention.** `NOTICE` attributes copyright to **"The
    Project Aegis Authors"**, a collective holder rather than a named individual,
    so the attribution never needs editing as contributors join — it stays
    correct with zero maintenance.
  - **CODEOWNERS reinstated, reversing D55's drop with cause.** D55's
    gate-hardening batch deliberately dropped a CODEOWNERS file as solo-maintainer
    ceremony: with a single committer it added a review gate that guarded nothing.
    Opening the repository to outside contributions inverts that judgment —
    `* @ModernNomad-98` now makes maintainer review of **every path** structurally
    mandatory (once the owner enables "Require review from Code Owners"), which is
    exactly the enforcement D55 correctly called pointless when no external PRs
    existed. Same artifact, opposite context, opposite decision — recorded here,
    not silently flipped.
  - **DCO, not a CLA.** Every commit carries a `Signed-off-by:` line
    (`git commit -s`) attesting to the [Developer Certificate of
    Origin](https://developercertificate.org). No copyright assignment and no CLA
    bot; Apache-2.0 §5 already fixes the inbound license.
  - **Owner rename recorded.** The canonical repository moved
    `nguyenpv1980-wq` → `ModernNomad-98` (both under `/Project-Aegis`; old URLs
    redirect). A repo-wide census updated the single **live** reference — the
    README clone URL — to `ModernNomad-98`. **Historical records were preserved
    untouched**: the dated `Repo:` headers in the reconciliation docs (this file,
    and `auto-merge-policy.md`, whose header was extended as an annotated rename
    chain rather than overwritten) and the `nguyenpv1980-wq` mentions under
    `docs/prompts/` and `docs/research/`. Zero live `nguyenpv1980` references
    remain outside historical records.
  - **Owner actions required to activate (outside the repo).** The pack wires the
    policy; five owner-only settings bring it live: enable **Private Vulnerability
    Reporting** (the SECURITY.md flow), enable branch protection's **"Require
    review from Code Owners"** (arms CODEOWNERS), set the **auto-merge** repository
    toggle per [`auto-merge-policy.md`](auto-merge-policy.md), paste the agreed
    **About** description/topics, and **park the old `nguyenpv1980-wq` username**
    so the redirects cannot be reclaimed by a third party.
  - Validator: **184 skills, exit 0, 0 warnings**; self-tests **38/38**. `git
    diff --check` clean; private-name sweep clean. No `scripts/` or workflow files
    touched — normal merge; auto-merge left unarmed (this repo's PR-no-merge
    policy).

- **D59 (2026-07-22) — Governance-prose corrections: current-state counts made
  countless outside the one governed surface, a single canonical security-review
  sentence, and the deferred and pending owner items recorded (governance and docs
  only; count stays 184).**
  - **The rule this batch encodes (superseding the earlier blanket phrasing).**
    Current-state **skill totals, family totals, subagent totals, and decision-range
    endpoints** may appear only in a **governed surface** — the README's single
    `<!-- SKILL-COUNT -->` / `<!-- FAMILY-COUNT -->` marker pair, which the validator
    reconciles against the skills actually on disk — or as a **countless pointer** to
    it. Everywhere else the prose says *what kind* of thing exists, never *how many*.
    Historical milestone numbers, per-batch deltas (`183→184`), decision IDs, dates,
    and evidence counts stay legal **when clearly historical**: they describe a past
    state, so they never go stale. A number that must be re-verified on every build is
    a maintenance liability; a number the validator already guards is not. This
    supersedes the earlier blanket phrasing, which banned counts without saying which
    ones or where they were allowed to live.
  - **Prose corrections (eight live surfaces).**
    - [`README.md`](../../README.md) §"Getting started" step 3 — "the 184 skills and 7
      subagents load automatically" became "every skill and subagent loads
      automatically", removing two live totals from the first page a newcomer reads.
    - `README.md` §"Map of the system" — "the 184 shipped procedures: 22 discipline
      families" became "the shipped procedures, organized into discipline families
      (authoritative counts: the marked intro below)". The directional word is
      **below**, not above: "Map of the system" precedes "What's in the library".
    - `README.md` §"Map of the system" — "seven read-only specialist reviewers" became
      "the read-only specialist reviewers". A spelled-out total is still a total; the
      word-versus-digit distinction is an artifact of how counts are *found*, not of
      what the rule governs.
    - `README.md` §"Map of the system" — "the dated decisions (D1–D46) in §5" lost its
      range endpoint, which had long since gone stale.
    - `README.md` §"What's in the library" — "It isn't one of the 22 families" became
      "one of those families", five lines below the marker pair it duplicated.
    - [`docs/HISTORY.md`](../HISTORY.md) intro — the "(D1–D56)" endpoint became a
      countless pointer, **and the document's boundary was made honest**: it now reads
      "curated construction history ... through **D47**", naming the reconciliation log
      as the complete authoritative record. The old intro implied the history covered
      every decision through D56 when its narrative in fact stops at D47. The moved
      narrative body was not touched.
    - [`docs/skills-catalog.md`](../skills-catalog.md) status block — the historical
      delta `(183→184)` was **kept**; the live clause "bringing the library to its
      current **184 skills**" was dropped. One sentence, two classes of number, only
      one of them removed.
    - [`CONTRIBUTING.md`](../../CONTRIBUTING.md) step 3c — "increment the '20 discipline
      families' claims" became "increment the marked `FAMILY-COUNT`". This one was
      **already wrong** (the real total is 22) and contradicted step 3d directly below
      it, which correctly names the markers as authoritative. It was found by the
      census, not by the planned item list — the exact failure mode the rule exists to
      prevent.
  - **One canonical security-review sentence, verbatim in both places.** The README
    claimed "every pull request is security-reviewed before merge", which overstates
    the model: **every** pull request gets maintainer review, and only those touching a
    security-relevant surface get the additional security review. Both surfaces now
    carry the same sentence body — *"Every pull request is reviewed by the maintainer
    before merge; pull requests touching a security-relevant surface receive an
    additional explicit security review"* — with the README closing on a pointer to
    `CONTRIBUTING.md`, and `CONTRIBUTING.md` continuing straight into the surface list
    it owns. `CONTRIBUTING.md`'s prior wording ("peer-reviewed", plus a separate
    paragraph that re-opened the security tier) differed materially enough to align.
  - **Conduct-reporting channel — not yet actionable; owner decision pending.**
    [`CODE_OF_CONDUCT.md`](../../CODE_OF_CONDUCT.md) directs reports "privately to the
    maintainer @ModernNomad-98 via GitHub". **GitHub has no private user-to-user
    messaging**, so as written the channel cannot be used. **The file was deliberately
    left unchanged** rather than patched with a placeholder: a concrete confidential
    intake — an email address or a form — is an owner decision, not an editorial one.
    **Private Vulnerability Reporting is not a substitute**: PVR is scoped to security
    vulnerabilities, not conduct, and its reports land in front of repository
    maintainers under a security workflow — the wrong venue for a complaint that may
    be *about* a maintainer.
    - **Disposition, appended 2026-09-30.** The owner decided this on 2026-09-27: wait until
      outside contributors appear. No private address is published now, `CODE_OF_CONDUCT.md`
      stays unchanged, and the project does not claim confidential intake until a private
      contact and an alternate recipient exist. It is recorded in the [open-decisions
      index](../roadmaps/aegis-open-decisions-2026-09-23.md#decided-on-2026-09-27), which names
      the D59 finding as its source, and restated in that page's current disposition table.
      This bullet's own heading reads "owner decision pending" as of its D59 recording; the
      decision has since been made, and no file changed.
  - **Owner-action ledger, updated.** Of the five owner-only settings D58 listed:
    - **Private Vulnerability Reporting — CONFIRMED ACTIVE** by the owner. Removed from
      pending; the `SECURITY.md` flow is live. **Re-verified 2026-09-30:** `gh api
      repos/ModernNomad-98/Project-Aegis/private-vulnerability-reporting` returns
      `{"enabled":true}`. The other four settings are owner-side or deferred and cannot be
      confirmed from this repository; the CODEOWNERS review requirement has not flipped, as its
      recorded trigger (the first external pull request or added collaborator) has not fired —
      `git log --format='%an' origin/main` lists only the owner's own identities,
      `dependabot[bot]` and `Codex`.
    - **"Require review from Code Owners" — deliberately deferred, with a trigger.**
      During the solo phase `.github/CODEOWNERS` names the only committer, so the gate
      would block the maintainer on the maintainer's own pull requests and buy nothing.
      **Flip it on at the first external pull request or the first added
      collaborator** — that is the moment the enforcement D58 reinstated the file for
      becomes real. Recorded as a deferral with a trigger, not as an omission.
    - **Parking the old `nguyenpv1980-wq` username — verify first, then test.** Park it
      with **no repository named `Project-Aegis` under it**: per GitHub's documentation,
      creating a repository of that name in the old namespace **overrides the
      redirect** — precisely the failure the parking exists to prevent. Note also that
      the old namespace **may already be permanently retired**, since GitHub does not
      release a renamed owner's namespace when the repository met the
      more-than-100-clones-in-the-prior-week threshold at rename time; the parking
      attempt may therefore simply be refused. **Test the redirect after parking**
      either way — parking counts as successful only if the old URLs still resolve.
    - **Repository-level "Allow auto-merge" — owner-verify.** External metadata
      reported the repository toggle still enabled. This is **distinct from per-PR
      arming**, which is verified `null` on every pull request this project opens and
      was verified `null` again here. The repository toggle is a capability, not a
      state; the owner should confirm it matches
      [`auto-merge-policy.md`](auto-merge-policy.md).
    - The **About** description and topics paste was completed at D57.
  - Validator: **184 skills, exit 0, 0 warnings**; self-tests **38/38**. The single
    `<!-- SKILL-COUNT -->` marker pair is unmoved, still appears exactly once, and
    still reconciles. A live-count census across `README.md`, `docs/HISTORY.md`,
    `docs/skills-catalog.md`, `CONTRIBUTING.md`, `AGENTS.md`, and `docs/paths/`
    classified every remaining digit- or word-bearing number as historical, leaving
    **zero live-count survivors** outside the marker pair. `git diff --check` clean;
    private-name sweep clean. No `scripts/`, no `.github/`, no `.claude/` files
    touched — both CI checks green, normal merge; auto-merge left unarmed (this
    repo's PR-no-merge policy).

- **D60 (2026-07-22) — Enforcement batch: commit-level DCO with a named trusted-bot
  exemption, a `push: main` validation lane, a pinned Python minor, and the merge gate
  widened to its enforcement surfaces (CI and `scripts/` only; count stays 184).**
  - **DCO turned from a checklist item into a check.** D58 chose the Developer
    Certificate of Origin over a CLA, and `CONTRIBUTING.md` has asked for
    `git commit -s` ever since — but nothing verified it, and an unverified ask is a
    wish. New [`scripts/check_dco.py`](../../scripts/check_dco.py) requires a
    well-formed `Signed-off-by: Name <email>` trailer on **every commit in the pull
    request's range**, not merely the tip: a branch's second commit is exactly as
    unsigned as its first. A bare `Signed-off-by:` with no identity certifies nobody
    and fails. Failure output names each offending commit by full SHA and prints the
    recovery verbatim — `git commit --amend -s` for one commit,
    `git rebase --signoff origin/main` for several, then `git push --force-with-lease`.
  - **The trusted-bot policy, in full.** Exempt from the trailer requirement:
    **exactly `dependabot[bot]` and `github-actions[bot]`**, matched on their GitHub
    noreply author addresses (an optional numeric-id prefix, the bot name, then
    `@users.noreply.github.com`, anchored at both ends). **Why:** both are machine
    authors with no person able to execute the DCO's certification, and neither can be
    made to add the trailer — so without the exemption every dependency bump would
    arrive permanently red, turning a security-patch pipeline into a nuisance to be
    routed around. The compensating control on the riskiest bot bumps is **cited, not
    restated**: [`.github/dependabot.yml`](../../.github/dependabot.yml) already
    documents that a bump touching the merge gate trips `gate-guard` and therefore
    needs a human admin merge. **Honest limit, recorded:** a commit's author field is
    self-asserted, so this exemption is **not an authentication boundary** and is not
    offered as one. Anyone able to write a commit could claim a bot address and skip
    the trailer — which buys nothing, since adding `-s` is free and the sign-off was
    never the obstacle; what actually gates merge here is human review plus branch
    protection. The list is held to two exact identities on one domain so it cannot
    widen by accident, and a lookalike (`renovate[bot]@users.noreply.github.com`) is
    proved non-exempt in the suite.
  - **Author-identity equality deliberately NOT enforced.** The sign-off email is not
    required to equal the author email. The stricter rule would break the recovery the
    script itself prints: `git rebase --signoff` signs as the person **running** the
    rebase, not as each commit's original author, so a maintainer relaying an outside
    patch would be told to run a command that cannot make the check pass. A gate whose
    own printed remedy fails its own rule is worse than no gate.
  - **Fail-closed on an empty range.** Zero commits is an **error**, not a vacuous
    pass. A pull request always has at least one commit, so an empty range means the
    range was computed wrong — the precise way a green check comes to be examining
    nothing at all. This is the live-surface protection for the real CI invocation,
    matching the "could pass by scanning nothing" guards D55 put on the validator's
    directory-scanning checks.
  - **Merge commits skipped, and the range ends at the real head.** CI passes
    `--no-merges`, and the range ends at `github.event.pull_request.head.sha` rather
    than `HEAD`: on a `pull_request` event `HEAD` is a synthetic merge commit **GitHub
    authored**, which no contributor can sign. Ranging to `HEAD` would have failed
    every pull request on a commit no human made.
  - **The DCO check is a STEP inside `validate-skills`, not a job of its own.** A new
    job name would be advisory until the owner registered it in branch protection; a
    step inside the already-required job makes the contract binding the moment it
    merges, with no owner action required. Cost: that job's checkout now uses
    `fetch-depth: 0` so the commit range can be walked.
  - **`push: main` validation lane.** The workflow now triggers on `pull_request`
    **and** `push` to `main`, deliberately asymmetric:
    - `validate-skills` (self-tests + validator) runs on **both** events.
    - `gate-guard` and the DCO step run on **`pull_request` only**
      (`if: github.event_name == 'pull_request'`). `gate-guard` diffs against
      `github.base_ref`, which a push event does not have — it would fail on a missing
      ref rather than on a real finding. DCO is a **PR-time contract**: squash and
      rebase merges can lawfully rewrite trailers on the way in, so the sign-off is
      asserted against the pull request's own commits, at the only moment they are the
      thing being merged.
    - The lane is a **detection lane, not a gate**: it runs after the merge has already
      happened and cannot block anything. It exists to catch a `main` that went red by
      a route no pull request saw — an admin merge past a red `gate-guard` (which this
      repo performs by design), a direct push, or a clean merge of two individually
      clean branches. Permissions stay `contents: read`.
  - **Python pinned to a minor: `'3.14'`.** `python-version: '3.x'` silently followed
    the runner image to whatever CPython shipped next — the one unpinned input left in
    a workflow that pins its actions to commit SHAs (D55) and PyYAML to an exact
    version. The value was **verified, not guessed**: run `29882666002` (the D59 pull
    request, the last run before this one) logged `Successfully set up CPython (3.14.6)`
    for `3.x` on `ubuntu-latest`, so `'3.14'` **freezes current behaviour rather than
    changing it**. Quoted deliberately — an unquoted `3.10` would parse as the float
    `3.1`. **Dependabot does not bump `python-version`**: it understands SHA-pinned
    actions and pip pins, not this field. That is the point rather than a gap — the
    interpreter the gate runs on now moves only by a deliberate reviewed pull request.
  - **Gate-scope decision: WIDENED to all three candidates** — a recommendation
    adopted, not a violation corrected. `gate-guard`'s protected set grows from
    `.github/workflows/` + `scripts/validate-skills.py` to also cover
    **`.github/CODEOWNERS`**, **`scripts/check_dco.py`**, and **`scripts/tests/`**. The
    four considerations, weighed honestly:
    1. **Always-red cost** — real, but near-zero at the margin. All three are
       rare-edit, and a `scripts/tests/` change almost always accompanies a change to a
       gate script or the workflow, which already tripped the gate. The genuinely new
       red case is a test-only pull request — precisely the change that should not be
       able to merge itself.
    2. **CODEOWNERS has no other control today.** D59 deliberately deferred "Require
       review from Code Owners" until the first external pull request or added
       collaborator. Until that flips, the red gate is the **only** structural control
       on the file that routes review authority — the strongest single argument for
       widening.
    3. **Edit frequency** — bounded. `.github/CODEOWNERS` has been edited once (D58);
       `scripts/check_dco.py` is new and expected to be near-static.
    4. **A separate security-surface job?** Considered and **rejected**: it would
       duplicate the diff-and-match logic, add a second required status check for the
       owner to register, and answer a question the log already answers — `gate-guard`
       prints exactly which files tripped it. Revisit **if** the protected set ever
       spans materially different merge policies (some needing security review, others
       only an admin merge); one gate with one regex is clearer until then.

    The principle recorded: **enforcement surfaces and merge-gate surfaces should
    coincide** — a change able to disarm the gate should not be able to merge itself,
    whichever file it lands in. `.github/dependabot.yml` was considered and left
    **outside** the set: disabling it would stop security patches arriving, which is a
    slow-burn risk rather than a merge-gate bypass.
  - **`CONTRIBUTING.md`, one line added** to External contributions beside the existing
    DCO bullet: *"CI enforces DCO; fix a missing sign-off with `git commit --amend -s`
    or `git rebase --signoff`."* The rule and its remedy now sit together, and match
    what CI prints on failure.
  - **Proofs.** Self-tests **46/46** (38 before, eight added: all-signed passes, one
    unsigned fails naming its hash, an unsigned bot commit passes, a mixed range fails
    on the human commit only, plus a bare trailer, an empty range, an unlisted bot
    address, and record round-tripping). Both gate scripts were proved able to fail by
    seeded mutation and then restored: disarming `check_description_not_block_scalar()`
    in the validator took the suite red at assertion 3, and making `has_signoff()`
    return `True` unconditionally took it red at assertion 39 — a check nobody has
    watched fail is an assertion, not a gate. The widened `gate-guard` regex was
    extracted **verbatim from the workflow** and replayed on-branch:
    `.github/CODEOWNERS`, `scripts/check_dco.py`, `scripts/tests/test_validator.py` and
    a fixture beneath it all trip it, while `README.md`, `CONTRIBUTING.md`,
    `docs/HISTORY.md`, `.github/dependabot.yml` and a `SKILL.md` do not. The workflow
    parses under PyYAML — with YAML 1.1's bare `on` key arriving as the boolean `True`,
    noted rather than fought — and all three `uses:` references remain full 40-hex
    pins, so the edit introduced no floating tag.
  - Validator: **184 skills, exit 0, 0 warnings**; self-tests **46/46**;
    `check_dco.py` green against this pull request's own commit range. `git diff
    --check` clean; private-name sweep clean. This pull request edits
    `.github/workflows/validate-skills.yml` and `scripts/`, so **`gate-guard` is RED by
    design** and the merge is a human admin merge (the D43/D50/D55 precedent);
    `validate-skills` must be green. Auto-merge left unarmed (this repo's PR-no-merge
    policy).
  - **Owner follow-up, one glance.** The push lane's configuration is verified
    on-branch, but its **first live execution cannot be observed until this merges** —
    the event does not exist before then. After merging, check the Actions tab for a
    `validate-skills` run triggered by the `push` to `main`: the `validate-skills` job
    green, `gate-guard` skipped. **Discharged, appended 2026-09-30.** The "cannot be observed
    until this merges" sub-claim resolved the moment D60 merged: the first push-triggered run
    is [run 29886415700](https://github.com/ModernNomad-98/Project-Aegis/actions/runs/29886415700),
    on `main` at `c4990b15` (D60's own merge, PR #72) on 2026-07-22 at 02:40:02 UTC, and it
    shows exactly what this follow-up predicted: `validate-skills` **success**, `gate-guard`
    **skipped**. Every later push run behaves the same, for example [run
    36805748030](https://github.com/ModernNomad-98/Project-Aegis/actions/runs/36805748030) on
    2026-10-01. Nothing further is owed on this row.

- **D61 (2026-07-28) — Claude Code startup bridge: a root `CLAUDE.md` that imports the
  shared `AGENTS.md` contract and adds Claude-Code-specific startup routing, plus a HARD
  validator check that keeps the bridge intact (count stays 184).**
  - **The gap this closes, observed not assumed.** An authentic beginner acceptance test
    run in Claude Code failed: with only `AGENTS.md` at the root, Claude Code loaded no
    startup instructions, never opened `project-orchestrator`, chose a stack, ran
    `npm install`, and scaffolded eighteen files before any requirements work. The cause
    is documented, not mysterious — the Claude Code memory documentation is explicit that
    **Claude Code reads `CLAUDE.md`, not `AGENTS.md`**, at session start. Codex CLI reads
    `AGENTS.md`; the two tools were never reading the same file, and only one of them had
    a file to read.
  - **The fix is the pattern the memory docs themselves prescribe.** A repo-root
    [`CLAUDE.md`](../../CLAUDE.md) whose **first line is the import `@AGENTS.md`** — a
    same-directory import Claude Code resolves at session start (and after compaction)
    with no approval dialog — followed by a short **`## Claude Code — startup routing`**
    section carrying only what the import alone does not make salient: list
    `.claude/skills/` and open the owning `SKILL.md` before acting; route an end-to-end
    or vague request through `project-orchestrator` from Stage 0; use the owning skill
    directly for a scoped single-stage request; never auto-invoke a MANUAL-ONLY skill;
    and, when the matching skill is absent from this copy, say so plainly rather than
    invent or substitute one. One shared contract, two documented entry points.
  - **Honest limit, kept in the wording.** Memory is **context, not enforcement** — the
    bridge makes the routing *salient*, it does not make it deterministic, so no new
    wording claims a mechanical guarantee. The README's beginner promise now reads
    "model-driven behavior enabled by the repo's startup instructions — verified by a
    live acceptance test, not a mechanical guarantee." `CLAUDE.md` is itself **countless**
    — no totals, no ranges — so it never becomes a surface anyone must reconcile.
  - **`AGENTS.md` left byte-identical.** The shared contract did not change; `CLAUDE.md`
    imports it rather than restating it, so the two entry points cannot drift apart.
  - **README, exactly three touches.** (a) The tools-section "Out of the box" bullet
    carried a **false claim** — that `AGENTS.md` is read "as extra context by Claude
    Code" — now corrected to the documented truth (Codex reads `AGENTS.md`; Claude Code
    reads `CLAUDE.md`, which imports it), the verified-against framing kept. (b) The
    beginner "one prompt to start" promise gains the model-driven honesty clause above.
    (c) The "files to copy" guidance now names `CLAUDE.md` (Claude Code's startup file;
    it imports `AGENTS.md`). **Census recorded:** the README had **no** pre-existing
    instruction to copy `AGENTS.md` into a user's own repo — the sole copy-into-your-repo
    region copies individual skill folders — so touch (c) is one addition there, not an
    update to a list that never existed.
  - **The bridge is a HARD check, not a hope**
    ([`check_claude_bridge`](../../scripts/validate-skills.py)). Three conditions, each
    fail-closed: `CLAUDE.md` exists at the root; its first line is exactly `@AGENTS.md`;
    the startup-routing section header is present. It is dependency-injected like the D55
    surface checks (a fixture path for the negatives, the real repo-root file for the
    live pin), so it exercises bad inputs **and** proves the shipped bridge conforms — a
    green check that scanned nothing is the failure mode D55 taught us to guard.
  - **Proofs.** Self-tests **51/51** (46 before, five added: the good bridge passes, a
    non-`@AGENTS.md` first line fails, a missing routing section fails, an absent file
    fails, and the shipped root file conforms). Validator **184 skills, exit 0, 0
    warnings**. Both gate scripts byte-compile; `git diff --check` clean; private-name
    sweep clean. This pull request edits `scripts/validate-skills.py` and adds under
    `scripts/tests/`, so **`gate-guard` is RED by design** and the merge is a human admin
    merge (the D43/D50/D55/D60 precedent); `validate-skills` must be green. Auto-merge
    left unarmed (this repo's PR-no-merge policy).

---

- **D62 (2026-09-11) — Keep recovery continuation in GitHub.** Following the
  loss of the previous computer, the owner clarified that GitHub is the project
  backup location and that the project contains no secret or personal data.
  The owner approved publication of the three reviewed Phase 0/1 commits, then
  directed continuation of committing the useful recovery records and setup
  instructions. Preserve the handoff, missing-input identities, verification
  evidence and runtime dependency lock in the repository, reachable from its
  README and BER backlog. A separate copy of the newly generated local ZIP is
  optional. Historical reports retain their original dates and source bindings;
  no missing calibration input, approval or execution history is reconstructed
  by this decision. See the
  [recovery handoff](../evidence/ber-recovery-2026-09-11/README.md).

- **D63 (2026-09-12) — Reconcile current documentation with delivered work.**
  At the owner's request to update documentation, changelogs and README surfaces,
  record the completed PR #88 calibration-engineering scope, PR #89 audit
  false-positive correction, PR #90 shared skill contracts, PR #91 permanent
  offline CI and PR #93 owner-approval persistence. Their delivery records and
  successful main runs are linked from the new [documentation index](../README.md)
  and [changelog](../../CHANGELOG.md). Update active setup, contributor, CI and
  continuation instructions; label dated design, audit and recovery narratives
  as historical without rewriting their source bindings or prior decisions.
  The [owner register](../approvals/APPROVAL_REGISTER.md) preserves recurring
  read-only-agent and administrator-merge grants for this source repository;
  those direct grants take precedence over generic skill defaults and do not
  transfer to consumer repositories. This is documentation reconciliation,
  not a new skill, release tag or execution authorization. Original calibration
  input bytes remain unavailable, WP-2B-3 measured acceptance is unfinished,
  OD-1 remains OPEN and WP-2B-4 remains BLOCKED. Offline regression CI does not
  complete WP-2B-7's future behavioral advisory integration.

- **D64 (2026-09-26) — Built `feature-flag-architect` (185→186), the
  feature-flag SYSTEM a product runs on, designed once per product.**
  - **Why.** The owner requested a feature-flag architecture skill on
    2026-09-26. Roadmap item cat 01 #27 ("Feature Flag Architecture", P1)
    and the system half of cat 02 #65 had no owner:
    `feature-flag-rollout-strategist` plans how ONE change is de-risked on
    whatever flag system exists, and nothing designed that system — the
    flag store, how code reaches it, where flags evaluate, what happens when
    the flag service is unreachable, how a kill switch propagates, who may
    flip it, and how flag changes are audited.
  - **What.** Inventory first (entitlement or permission "flags" routed
    out); the flag store build-vs-buy taught as an owner choice — terms,
    each viable option's fit, capabilities, pros, cons and money / setup /
    upkeep cost (unknown where unverified), one recommendation with the fact
    that would change it, exactly one atomic question, and the answer
    authorizes no sign-up, payment or SDK change; one internal flag
    interface with server/client key separation; evaluation placement per
    flag class; a targeting model with server-side sources of truth,
    precedence, shared stable-ID bucketing and tenant-qualified cache keys;
    the fail-safe MECHANISM (code defaults, last-known-good cache,
    non-blocking timeout, cold start that serves the code default and emits
    a metric); a kill-switch reach bound and flip authority; the flag-change
    audit event; flag-debt hooks (registry with owner, type, expiry and safe
    value; stale-flag report).
  - **The hard seam — system vs one rollout.** The strategist keeps each
    change's ramp, guardrails, removal and each flag's safe VALUE; this
    skill designs the mechanism that falls back to that value. The
    strategist's body now routes flag-system requests here and consumes
    tenant-qualified caching, change authority and the reach bound from this
    skill (its description names the new neighbour). Further seams pinned in
    trigger-evals: `plan-entitlement-architect`,
    `authorization-matrix-designer`, `ab-test-designer`,
    `ci-pipeline-architect` (manual-only), `saas-platform-architect`,
    `tenant-isolation-reviewer`, `caching-strategy-designer`,
    `authority-invalidation-architect` and `frontend-perf-engineer`. Owner
    decisions of 2026-09-26: the flag-value caching seam with
    `caching-strategy-designer` stays as designed, and the four one-way
    ROUTE-002 hub findings (toward `plan-entitlement-architect`,
    `authorization-matrix-designer`, `ab-test-designer` and
    `ci-pipeline-architect`) stay census data rather than being
    reciprocated. The accepted description's yield to
    `tenant-isolation-reviewer` adds a fifth one-way ROUTE-002 info finding
    (contract audit 347 → 352 on the rebased main); the owner confirmed it is
    likewise left as census data.
  - **Posture.** Design only — installs, signs up for, pays for and flips
    nothing → model-invocable. Live changes route through
    `human-approval-boundary`.
  - **Registration.** Joins the Phase 3 SaaS & tenant isolation pack
    (family 4, 9→10; FAMILY-COUNT stays 23). Catalog Phase 3 row and history
    paragraph, README Phase 3 row, family line and decision-table row; README
    `SKILL-COUNT` 185→186.
  - Validator: **186 skills**; description under the 1024-character cap. To
    be checked by `skill-quality-reviewer` and `library-diff-reviewer` for
    the system-vs-rollout seam.

- **D65 (2026-09-26) — Re-anchored the Phase 7 AI-security pack to the OWASP
  Top 10 for LLM Applications 2026 (v1.0, 2026-08-03).**
  - **Why.** Owner decision 2026-09-26; supersedes D6's edition anchor (2025)
    only — D6's skill set and extend-existing choices stand.
  - **What.** All current LLM IDs renumbered (01→01, 02→02, 03→04, 04→05,
    05→10, 06→03, 07→08 renamed Hidden Context Exposure, 08→09, 09→07,
    10→06); skill pages carry the 2025 ID in brackets; crosswalk in
    `ai-threat-modeler/references/llm-top10-threat-catalog.md`. D6's table
    above keeps its 2025 IDs as the historical record.
  - **Open gaps (owner call).** LLM08 wider hidden context beyond the system
    prompt (owner decided 2026-09-26 to extend and rename the skill —
    follow-up PR); LLM10 generated-code review; LLM04 promoted-artifact
    trust and LLM01 cross-modal injection are catalog-only.

- **D66 (2026-09-26) — Renamed `system-prompt-leakage-reviewer` to
  `hidden-context-exposure-reviewer` and extended it to the full OWASP
  LLM08:2026 scope (count stays 186).**
  - **Why.** The OWASP Top 10 for LLM Applications 2026 (re-anchored in D65)
    replaced 2025's LLM07 System Prompt Leakage with LLM08 Hidden Context
    Exposure, which covers every non-user-facing input the model sees, not
    only the system prompt. The skill reviewed only the system-prompt slice,
    so tool/function schemas, retrieved policy text and gateway-injected
    developer instructions had no owner. The owner chose on 2026-09-26 to
    rename and extend the existing skill rather than add a sibling.
  - **What.** Two axes applied to every hidden source: CONTENTS (no
    credentials, keys, internal endpoints, or role, refusal or workflow
    logic whose disclosure aids an attacker) and DEPENDENCE (no
    authorization, filtering, limit or tool permission relies on hidden
    context staying secret; enforcement is deterministic and outside the
    model). The severity scale follows the official LLM08:2026 wording
    (informational, medium, high, critical). Out of scope, as in the
    official entry: regulated user or training data
    (`sensitive-disclosure-guard`); agentic amplifications — persistent
    memory (`memory-context-poisoning-reviewer`), inter-agent channels
    (`inter-agent-comms-reviewer`), tool configuration persistence and
    multi-step agent compromise; and generic application security —
    client-bundle secrets (`secrets-identity-hardener`, manual-only),
    server-side log leakage and infrastructure-layer side channels
    (`threat-modeler`). A live secret in hidden context is a Stop Condition
    routed to `secrets-identity-hardener` and `incident-response-runbook`.
  - **Seams.** Trigger-evals pin `prompt-injection-defender`,
    `sensitive-disclosure-guard`, `rag-security-architect`,
    `agent-tool-safety-guard`, `secrets-identity-hardener`,
    `memory-context-poisoning-reviewer`, `model-context-designer` and
    `inter-agent-comms-reviewer`. `agent-tool-safety-guard`'s description
    and body now name this skill back for the tool-schema exposure seam.
    Neighbour references in `ai-threat-modeler`,
    `prompt-injection-defender`, `sensitive-disclosure-guard` and
    `ai-evaluation-harness` point to the new name.
  - **Migration.** The catalog records the former name so copied references
    can be updated. Historical evidence, audit snapshots and earlier
    decisions (D6 and the §3 tables) keep the old name as written.
  - **Registration.** Same family and phase (Phase 7 AI security & LLM systems);
    README and catalog rows renamed; `SKILL-COUNT` unchanged at 186.
    Validator: 186 skills, 0 warnings; contract audit shows no new findings.

- **D67 (2026-09-27, retroactive record of 2026-09-23) — Added the manual-only
  `aegis-setup` skill (184 → 185).**
  - **Record type.** This is an after-the-fact record. The owner decided on
    2026-09-27 to add it so every skill-count change has a decision row. The
    decision itself was made and delivered on 2026-09-23.
  - **What shipped.** [PR #124](https://github.com/ModernNomad-98/Project-Aegis/pull/124)
    merged at 2026-09-23T16:54:59Z as
    `d598390f4b7bb367ce79dd1276157f91ae36556b`, under owner grant AEGIS-APR-007
    (Issue #101 package 2), which AEGIS-APR-052 records as consumed. It added
    `aegis-setup`: a manual-only, four-choice setup conversation, run only
    when a person invokes it by name, and an Aegis-only saved selection on
    tested single-user Windows PowerShell. Local and online helpers remain
    unavailable, and a saved choice grants no provider authority. Family 23;
    the library went from 184 to 185 skills.
  - **Why no row existed.** The delivery was authorized and tracked in the
    [owner approval register](../approvals/APPROVAL_REGISTER.md), not in this
    log, and no decision row was written then. PR #389 later added the README row
    and catalog sentence, citing PR #124 and AEGIS-APR-007 instead of a
    decision number.
  - **Numbering.** D67 is the next free number. It is out of time order by
    design: D64 (185 → 186) comes after this change in the skill count but
    has a lower number. Existing numbers are not changed.
  - **What this does NOT change.** No skill, file list or count changes (the
    library stays at 186). AEGIS-APR-007 stays consumed and gains no new use.
    D64, D65 and D66 are not edited or renumbered. README and catalog now cite
    D67 alongside PR #124 and AEGIS-APR-007.

- **D68 (2026-09-28) — Approved the quality assurance (QA) Tier 1 build
  batch: three new skills, one extension and one drop (186 → 189 when
  delivered).**
  - **Why.** The owner, Peter Nguyen, decided on 2026-09-28 in chat with the
    Claude Code coordinator, answering "Build it as recommended
    (Recommended)" to the
    [QA Tier 1 scope proposal](../roadmaps/qa-tier1-skill-batch-proposal.md) (PR #492 at head `930493c`). It settles
    the five remaining D10 Tier 1 candidates.
  - **What.**
    - **Build `test-tenant-provisioner`** (catalog #198), manual-only: it
      writes test tenants and users to a named non-production environment.
    - **Build `ci-failure-classifier`** (#214 + #215), auto-invocable: it
      reads only the logs and reports it is given, and fetches, reruns and
      edits nothing.
    - **Build `acceptance-criteria-reviewer`** (#226), renamed from
      `acceptance-criteria-tester` and narrowed to #226; auto-invocable,
      read-only review. The #227 definition-of-done gate stays with
      `release-readiness-reviewer`, `ai-closeout-reporter` and
      `agent-governance-audit`.
    - **Merge `negative-path-test-mapper`** (#192) into `test-plan-designer`
      as an extension (a per-surface negative-path matrix); the skill stays
      auto-invocable.
    - **Drop `regression-first-bug-fixer`** (#190): `tdd-engineer` already
      owns it, with `systematic-debugger` and `regression-suite-curator` as
      neighbors.
    - **Census.** The eight predicted one-way ROUTE-002 findings (toward
      `tenant-modeler`, `secrets-identity-hardener`, `flaky-test-detective`,
      `sharded-validation-with-resume`, `ci-pipeline-architect`,
      `requirements-gathering-facilitator`, `manual-test-case-creator` and
      `release-readiness-reviewer`) stay census data, following D64. They
      are predicted from draft descriptions, not measured; the build pull
      requests compare the contract audit before and after.
  - **D10 correction.** D10's Tier 1 note that `tdd-engineer` "owns new
    behavior, not bug reproduction" was wrong from the start. `tdd-engineer`
    shipped with the bug-fix trigger in `07049814` (the Phase 2 pack,
    2026-07-06), the day before D10: its description already said "when
    fixing a bug that should get a regression test proving the fix". D10's
    text above is unchanged; this entry is the correction.
    - **The Tier 1 row's Note is itself contradictory and is corrected here
      (verified 2026-09-30 against `git ls-tree -r --name-only origin/main --
      .claude/skills`).** `regression-first-bug-fixer` does **not** exist on
      `main` and D68 dropped it, so the row's "**dropped (D68, 2026-09-28)**"
      marker is TRUE and its trailing Note clause — "`tdd-engineer` owns new
      behavior, not bug reproduction" — is the stale D10 wording this entry
      refutes. Read the row as dropped-covered, not as "built": the skill was
      never built, and the work belongs to `tdd-engineer` (whose bug-fix
      trigger has been in its description since `07049814`, 2026-07-06).
      The row's Note is dated D10 text and is left in place as provenance.
    - **Delivery status of the rest of the batch (verified 2026-09-30).**
      D68's `acceptance-criteria-reviewer` (`89eec69c`),
      `test-tenant-provisioner` (`ebc9225d`), `ci-failure-classifier`
      (`18e8a280`), the `negative-path-test-mapper` → `test-plan-designer`
      extension (`09aa09b7`) and the `regression-first-bug-fixer` drop are all
      on `main`, so the D10 Tier 1 table rows above carry their
      built/merged/dropped markers.
  - **Authority.** This decision authorizes exactly this batch. Its delivery
    relies on the standing delivery approval
    [AEGIS-APR-039](../approvals/APPROVAL_REGISTER.md#aegis-apr-039-reaffirmation-of-ongoing-backlog-delivery-approval)
    and the standing merge conditions
    [AEGIS-APR-048](../approvals/APPROVAL_REGISTER.md#aegis-apr-048-standing-administrator-merge-once-checks-are-green),
    [AEGIS-APR-049](../approvals/APPROVAL_REGISTER.md#aegis-apr-049-exact-head-ci-satisfies-the-local-test-condition)
    and
    [AEGIS-APR-050](../approvals/APPROVAL_REGISTER.md#aegis-apr-050-merges-wait-for-the-automated-codex-review),
    and nothing more. It does not waive `gate-guard`, authorize a change to
    `scripts/audit-skill-contracts.py` or its frozen baseline, or permit any
    environment write, provider call or deployment. Changing the set, for
    example building all five or letting `ci-failure-classifier` fetch logs
    itself, needs a new owner decision.
  - **Status at recording.** Nothing is built; the library stays at 186
    skills. Catalog rows, README counts, eval files and the D10 table rows
    for #190 and #227 land with the build pull requests.

- **D69 (2026-09-28) — Approved the AI-assisted software development
  lifecycle (AI-SDLC) build batch: one new skill, two extensions and one
  drop (189 → 190 when delivered).**
  - **Why.** The owner, Peter Nguyen, decided on 2026-09-28 in chat with the
    Claude Code coordinator, answering "Build it as recommended
    (Recommended)" to the
    [AI-SDLC skill batch proposal](../roadmaps/ai-sdlc-skill-batch-proposal.md)
    (PR #494, merged as `4ee2115`). AI-SDLC is how people and artificial
    intelligence (AI) agents plan, build, check, review, merge and close
    software work together. The decision settles the five remaining
    category 08 candidates (#266, #267, #273, #277 and #278).
  - **What.**
    - **Build `ai-task-decomposer`** (#266), auto-invocable: the assistant
      may choose it without a person naming it, because it only reads and
      plans. It splits a broad goal or approved spec into ordered tasks that
      each fit one pull request, with one intent, an observable done
      criterion, risks and any approval boundary; it starts no work and
      edits nothing. `change-classification-gate`'s description gains a
      reciprocal exclusion naming the new skill.
    - **Wire it into the stage maps.** Add `ai-task-decomposer` to the
      "Plan / approve" row of the `ai-sdlc-operating-model` stage-gate map
      and to `project-orchestrator` Stage 5 ("Plan the work"), between
      `tech-spec-writer` and `phased-work-handoff-designer`. These are body
      edits; neither skill's description changes.
    - **Extend `ai-closeout-reporter`** (#267 + #273) with a
      per-deliverable trace: one row per requested item naming the files
      that serve it, the check that proves it and the evidence, with each
      evidence item tied to its commit SHA or CI run. The skill stays
      auto-invocable.
    - **Extend `code-reviewer`** (#277) with a weakened-validation check
      (tests deleted, skipped or loosened to make a change pass) and a check
      for drift from recorded architecture decisions, both at least MAJOR.
      The skill stays auto-invocable.
    - **Drop #278** (AI Pair Engineering Protocol):
      `ai-sdlc-operating-model` and the skills its stage-gate map names
      already cover each step.
    - **Census.** A one-way ROUTE-002 finding is a contract-audit note that
      a skill's description excludes a neighbor ("Do NOT use for …
      (neighbor)") whose own description does not name it back. The four
      predicted findings, from `ai-task-decomposer` toward
      `tech-spec-writer`, `lane-authoring-guide`,
      `phased-work-handoff-designer` and
      `roadmap-to-commitments-translator`, stay census data: recorded in the
      audit, not fixed. The reason is description room, not D64's reason
      that hub skills cannot name every skill pointing at them: those four
      descriptions have only 8 to 49 characters left under the
      1,024-character limit. The findings are predicted from the draft
      description, not measured; the build pull request compares the
      contract audit before and after.
  - **Authority.** This decision authorizes exactly this batch. Its delivery
    relies on the standing delivery approval
    [AEGIS-APR-039](../approvals/APPROVAL_REGISTER.md#aegis-apr-039-reaffirmation-of-ongoing-backlog-delivery-approval)
    and the standing merge conditions
    [AEGIS-APR-048](../approvals/APPROVAL_REGISTER.md#aegis-apr-048-standing-administrator-merge-once-checks-are-green),
    [AEGIS-APR-049](../approvals/APPROVAL_REGISTER.md#aegis-apr-049-exact-head-ci-satisfies-the-local-test-condition)
    and
    [AEGIS-APR-050](../approvals/APPROVAL_REGISTER.md#aegis-apr-050-merges-wait-for-the-automated-codex-review),
    and nothing more. It does not waive `gate-guard`, authorize a change to
    `scripts/audit-skill-contracts.py` or its frozen baseline, or permit any
    environment write, provider call or deployment. Changing the set, for
    example building all five candidates as separate skills, needs a new
    owner decision.
  - **Status at recording.** Nothing is built. `main` at `76b399b` has 187
    skills: D68's `acceptance-criteria-reviewer` has landed, and its other
    two skills are in open PRs #500 and #502. Once those land the library
    has 189 skills, and this batch makes it 190. Catalog rows, README
    counts, eval files and the catalog note recording #278 as covered land
    with the build pull requests.

- **D70 (2026-09-28) — Approved the Phase 7 artificial intelligence (AI)
  engineering build batch: one new skill, two extensions, one candidate
  folded into the new skill and one drop (one more skill when delivered).**
  - **Why.** The owner, Peter Nguyen, decided on 2026-09-28 in chat with the
    Claude Code coordinator, answering "Build it as recommended
    (Recommended)" to the
    [Phase 7 AI engineering skill batch proposal](../roadmaps/phase7-ai-engineering-skill-batch-proposal.md)
    (PR #495, merged as `e77403c`). It settles the five Phase 7 expansion
    candidates (#282, #283, #285 with #286, #287 and #299).
  - **Numbering.** The
    [Phase 6 reliability batch proposal](../roadmaps/phase6-reliability-skill-batch-proposal.md)
    (PR #496) provisionally claimed D70. Each decision takes the next free
    number when it is recorded, which is not always time order (see D67).
    The owner decided this Phase 7 batch first and it is recorded first, so
    it takes D70; the Phase 6 batch, decided later the same day, takes D71.
  - **What.**
    - **Build `ai-human-in-the-loop-designer`** (#285, with #286),
      auto-invocable (the assistant may choose it without a person naming
      it) and design-only. It designs how an AI feature's output becomes
      product state, by default advisory-only (the AI proposes and a person
      commits), with a review workflow: a pending proposal, a reviewer queue
      showing the exact change, approve, edit, reject and expiry, no
      self-approval, commit through the normal write path, and an audit
      record. #287 is folded in as its first step: each AI action is sorted
      into automatic, confirm or forbidden by risk tier.
      `human-approval-boundary`, `agent-tool-safety-guard` and
      `ai-governance-risk-reviewer` gain reciprocal exclusions naming it.
    - **Extend `ai-router-architect`** (#282) with per-provider adapters, a
      capability matrix that routing and fallback must consult, and adapter
      conformance tests. To fit the 1,024-character limit, two description
      sentences move into the body, which already says both: the one naming
      `secrets-identity-hardener` and `observability-operator` as composed
      skills, and the one explaining why the skill is manual-only. The
      router stays manual-only (a person must name it).
    - **Extend `model-context-designer`** (#283) with a versioned
      prompt-contract record for each model call: the instruction's version
      and owner, declared inputs, a pointer to the output contract, when the
      model must decline, and which prompt changes need an evaluation rerun.
      Its description adds `agent-harness-architect` and
      `structured-output-validator` to its "Distinct from" list; naming
      `agent-harness-architect` clears an existing one-way ROUTE-002
      finding. The proposal also offers an optional reverse exclusion in
      `structured-output-validator` naming the prompt contract. It stays
      auto-invocable.
    - **Drop #299** (AI feature kill switch): already covered by
      `ai-router-architect`'s kill-switch step, with
      `ai-cost-guardrail-designer`, `agent-containment-reviewer` and the
      feature-flag pair.
    - **Census.** The two predicted one-way ROUTE-002 findings (defined in
      D69), from `ai-human-in-the-loop-designer` toward
      `human-agent-trust-reviewer` and `agent-authorization-matrix`, stay
      census data: recorded in the contract audit, not fixed.
      `human-agent-trust-reviewer`'s description has no room (1,018 of
      1,024 characters), and `agent-authorization-matrix` is a manual-only
      governance skill that other governance work depends on. They are
      predicted from the draft description, not measured; the build pull
      request compares the contract audit before and after.
  - **Authority.** This decision authorizes exactly this batch. Its delivery
    relies on the standing delivery approval
    [AEGIS-APR-039](../approvals/APPROVAL_REGISTER.md#aegis-apr-039-reaffirmation-of-ongoing-backlog-delivery-approval)
    and the standing merge conditions
    [AEGIS-APR-048](../approvals/APPROVAL_REGISTER.md#aegis-apr-048-standing-administrator-merge-once-checks-are-green),
    [AEGIS-APR-049](../approvals/APPROVAL_REGISTER.md#aegis-apr-049-exact-head-ci-satisfies-the-local-test-condition)
    and
    [AEGIS-APR-050](../approvals/APPROVAL_REGISTER.md#aegis-apr-050-merges-wait-for-the-automated-codex-review),
    and nothing more. It does not waive `gate-guard`, authorize a change to
    `scripts/audit-skill-contracts.py` or its frozen baseline, or permit any
    environment write, provider call or deployment. Changing the set, for
    example building all five candidates as separate skills or making
    `ai-router-architect` auto-invocable, needs a new owner decision.
  - **Status at recording.** Nothing is built; `main` at `76b399b` has 187
    skills. The batch adds one skill: 190 → 191 if the D68 and D69 builds
    land first. Catalog rows, README counts, eval files and the Phase 7
    backlog note recording #287 and #299 as covered land with the build
    pull requests.

- **D71 (2026-09-28) — Approved the Phase 6 cloud, DevOps and reliability
  build batch: four new skills and one extension, with the backup verifier
  built first (four more skills when delivered).**
  - **Why.** The owner, Peter Nguyen, decided on 2026-09-28 in chat with the
    Claude Code coordinator, answering "Build all, backup verifier first
    (Recommended)" to the
    [Phase 6 reliability skill batch proposal](../roadmaps/phase6-reliability-skill-batch-proposal.md)
    (PR #496, merged as `76b399b`). It settles the five Phase 6 expansion
    candidates (two execution-plan extras, #244 with #246, #253 and #254).
  - **Numbering.** The proposal provisionally claimed D70. Each decision
    takes the next free number when it is recorded; the Phase 7 decision,
    made and recorded first, took D70, so this decision takes D71.
  - **What.**
    - **Build `database-backup-verifier`** (#253) first, because #253 and
      #254 are P0 (must-have) in category 07. It is manual-only (a person
      must name it), because it calls provider interfaces and restores data.
      Evidence mode, the default, runs read-only listings. Drill mode
      restores only into a named, isolated, non-production target after a
      human approval that states the drill's cost, and never over an
      existing database.
    - **Build `cloud-security-baseline-reviewer`**, auto-invocable (the
      assistant may choose it without a person naming it). It reads only the
      exported settings, scanner findings, infrastructure-as-code files and
      screenshots it is given, calls no cloud interface and changes nothing.
    - **Build `resilience-architecture-reviewer`**, auto-invocable and
      review-only: timeouts, retries, single points of failure, failover,
      disaster recovery targets and a fault-injection plan for a person to
      run. It runs no fault injection itself.
    - **Build `environment-parity-reviewer`** (#244, with #246 folded in),
      auto-invocable and the lowest priority in the batch. It compares
      environments and drafts the required-configuration manifest and
      startup validation, reading variable names and non-secret values only.
    - **Merge #254** (`migration-deployment-runbook`) into
      `data-migration-runbook-author` as an extension: a schema-migration
      deploy runbook shape, target confirmation before any write, and
      post-apply smoke checks. The skill stays auto-invocable.
    - **Edits to other shipped skills.** Reciprocal exclusions naming the
      new skills are added to `aws-saas-architect`,
      `security-logging-alerting-architect`,
      `horizontal-scalability-reviewer`, `vite-build-qa-engineer` and
      `local-ci-mirror-preflight`, and to `iac-reviewer` in one combined
      rewrite naming both the baseline and parity reviewers. The
      disaster-recovery half of the "uptime/DR commitments" route in
      `soc2-trust-criteria-mapper`'s scoping map moves from
      `slo-reliability-architect` to `resilience-architecture-reviewer`.
    - **Census.** The ten predicted one-way ROUTE-002 findings (defined in
      D69) stay census data: recorded in the contract audit, not fixed. They
      run from the baseline reviewer toward `azure-saas-architect`,
      `secrets-identity-hardener` and `compliance-gap-auditor`; from the
      resilience reviewer toward `slo-reliability-architect`,
      `latency-budget-architect` and `rollback-runbook-author`; from the
      parity reviewer toward `secrets-identity-hardener`; from the backup
      verifier toward `data-migration-runbook-author` and
      `pii-lifecycle-designer`; and from the extended
      `data-migration-runbook-author` toward
      `gated-deployment-prompt-template`. Seven have little or no
      description room left (963 to 1,021 characters of 1,024); the two
      toward `secrets-identity-hardener` follow D64, because it is a widely
      used security hub; and the proposal leaves the one toward
      `pii-lifecycle-designer` one-way without a separate reason. They are
      predicted from draft descriptions, not measured; the build pull
      requests compare the contract audit before and after.
  - **Authority.** This decision authorizes exactly this batch. Its delivery
    relies on the standing delivery approval
    [AEGIS-APR-039](../approvals/APPROVAL_REGISTER.md#aegis-apr-039-reaffirmation-of-ongoing-backlog-delivery-approval)
    and the standing merge conditions
    [AEGIS-APR-048](../approvals/APPROVAL_REGISTER.md#aegis-apr-048-standing-administrator-merge-once-checks-are-green),
    [AEGIS-APR-049](../approvals/APPROVAL_REGISTER.md#aegis-apr-049-exact-head-ci-satisfies-the-local-test-condition)
    and
    [AEGIS-APR-050](../approvals/APPROVAL_REGISTER.md#aegis-apr-050-merges-wait-for-the-automated-codex-review),
    and nothing more. It does not waive `gate-guard`, authorize a change to
    `scripts/audit-skill-contracts.py` or its frozen baseline, or permit any
    environment write, provider call, cloud call, restore or deployment.
    Building `database-backup-verifier` authorizes no restore drill: each
    drill still needs its own human approval that states its cost. Changing
    the set, for example letting `cloud-security-baseline-reviewer` call
    cloud interfaces itself, needs a new owner decision.
  - **Status at recording.** Nothing is built; `main` at `d932d2c` has 188
    skills. The batch adds four skills: 191 → 195 if the D68, D69 and D70
    builds land first. Catalog rows, README counts, eval files and the
    catalog note recording #254 as merged land with the build pull
    requests.

- **D72 (2026-10-03) — Adopted the seven-stage delivery workflow as standing
  policy for this source repository.**
  - **Why.** The owner's direct instruction asked for one permanent delivery
    workflow that binds any coding agent regardless of model, provider, editor
    or harness, and for it to be recorded rather than remembered: a standing
    rule whose only existence is session state cannot be audited. The repository
    already carried a partial and inconsistent version of it in three places —
    a four-stage arrow in `AGENTS.md`, the merge and evidence rules in
    `CONTRIBUTING.md`, and an advisory skills item in the pull-request template
    — and reconciling those three into one canonical source is what this
    decision settles.
  - **What.** One canonical page, `docs/delivery-workflow.md`, holds the
    normative rule: the seven stages in order — PLAN, INDEPENDENT PLAN AUDIT,
    IMPLEMENT, INDEPENDENT IMPLEMENTATION AUDIT, VALIDATE, FINAL INDEPENDENT PR
    CODE REVIEW, MERGE — each naming its entry evidence and its exit evidence;
    the exact-head invalidation rule, that a moved head **voids** every
    head-bound verdict and that a review dispatched but not posted is
    incomplete; the merge prohibition, that no merge happens before the final PR
    review is posted, accepted and verified against the exact candidate head;
    proportionality, so a small change may carry a short plan and must not
    require a design document; the required four-column "Aegis skills used"
    table; the Role A source-library / Role B consumer-repository scope; and an
    explicit split between what CI and branch protection actually enforce and
    what remains procedural.
    `AGENTS.md` carries a binding summary of the invariant plus a pointer;
    `CONTRIBUTING.md` gains operating rule 9 and a pointer from rule 2; and the
    pull-request template's skills item becomes a required section outside the
    advisory checklist. `CLAUDE.md` and `README.md` are deliberately unchanged —
    `CLAUDE.md` imports `AGENTS.md`, so it inherits, and a second copy would
    drift.
    The page is the **sole normative rendering** of the merge-gate conditions,
    which carry stable IDs `MG1`–`MG5`; every other mention of a condition, in
    any file, is a pointer carrying the ID and **no content**.
  - **Authority.** The owner's current direct instruction, relayed to the
    implementing agents through the coordinating agent's brief and recorded here
    as a transcription rather than as a message an agent can read directly.
    `AGENTS.md` states that "A current-turn owner instruction is itself valid
    evidence and needs no command output", and the approval register's preamble
    states that "Current direct user instructions are valid source evidence
    before transcription and do not need repeated consent". This entry grants
    nothing; it records a process. Its companion register entry is
    `AEGIS-APR-105`, a `POLICY DECISION` that likewise authorizes no work.
  - **Status at recording.** Recorded 2026-10-03 against `origin/main` at
    `c74c78d1`. The library has 195 skills; this decision adds no skill and
    changes no skill file, no workflow file and no protected path. The workflow
    is **documented, not machine-enforced**, and the page says so: its own
    enforcement split records that the stage order, the stage separation, the
    exact-head invalidation rule and proportionality have no mechanical control
    behind them.

- **D73 (2026-10-07) — Decided that the acceptance index will give the
  readability pending count, after a gated repair (Option 1), then paused.**
  - **Why.** One quantity had two figures. The
    [readability ledger](../roadmaps/aegis-documentation-readability-backlog.md)
    states its pending count by hand under an accepted-unless-listed default,
    and its acceptance tool (`tools/readability_acceptance/`) counts on a
    different basis. The ledger's 2026-10-07 current-count reconciliation
    found the exact count not derivable and held the choice for the owner.
    AEGIS-APR-101 had expressly approved no canonical index, no precedence and
    no changed counting rule. An independent audit (OPT1-AUDIT, 2026-10-07:
    four lanes and a verification, coordinator-held session artifacts, not
    repository records) checked whether making the index official would slow
    development or break a process. Its conditions are below.
  - **Decision.** The owner approved the coordinator's recommendation, Option
    1, answered the follow-up questions, and then paused the program after
    this decision record. All of it is recorded verbatim in
    [AEGIS-APR-113](../approvals/APPROVAL_REGISTER.md#aegis-apr-113-readability-pending-count-authority-option-1)
    to AEGIS-APR-118. AEGIS-APR-113 and AEGIS-APR-118 are POLICY DECISIONs;
    AEGIS-APR-114 to AEGIS-APR-117 are GRANTs, and none of the four covers any
    work unless the owner resumes the program. In short:
    1. the index becomes the official pending count only after its repaired
       tool passes an independent review;
    2. a page with no recorded acceptance in the repaired index counts as
       pending;
    3. a page whose recorded acceptance commit no longer exists anywhere, or
       whose change since then cannot be measured for another reason, counts
       as pending until it is re-reviewed;
    4. the ledger keeper records each acceptance as one row of a fixed-format
       table inside the ledger, the index reads only that table, and a
       one-time reviewed backfill seeds it (the schema is condition 2, an
       audit condition);
    5. the index is rebuilt after each keeper recording and on demand, by "a
       coding agent or a human";
    6. there is no continuous integration (CI) gate;
    7. after a switch, the ledger publishes no count of its own;
    8. the tool repair may be split into several pull requests run in
       parallel;
    9. once the fixed-format table exists, the keeper may record targeted
       reviews (AEGIS-APR-116); after a switch, the keeper may append
       withdrawal rows (AEGIS-APR-117);
    10. `tools/readability_acceptance/` is security-relevant "approval/evidence
        tooling" (AEGIS-APR-118, in effect now);
    11. **the program is paused** after this decision record and is a
        low-priority backlog item; until the owner resumes it, the readability
        ledger stays the record.
  - **Alternatives considered.**
    - **Option 2**, the ledger stays official and the index advisory: not
      chosen. The repair is owed under both options, Option 2 keeps the hand
      reconciliation that PR #677 needed, and it keeps the under-counting
      accepted-unless-listed default.
    - **"A: repair the prose reader"** (the option shown to the owner; the
      audit estimated 26–52 active hours, low confidence): not chosen. Every
      later ledger edit would have to stay harvester-safe, and telling positive
      from negative statements would stay heuristic.
    - **Recording in the index itself**, as the
      [conversion note](../evidence/documentation/acceptance-conversion-process-2026-10-02.md)'s
      section (d) proposed: not chosen. The keeper would write outside the
      ledger, which AEGIS-APR-101 does not cover.
    - **The repair variants**, as shown to the owner on 2026-10-07: "V2:
      verifiable only (Recommended)", "V0: full backfill", "V1: no backfill"
      or pausing. The owner chose "Pause the program". The variants, with
      their unmeasured estimates, are kept in the backlog item.
  - **Conditions on the switch.** These are the audit's reconciled set. Each row
    has a source label:
    - **Owner** means the owner's words quoted in AEGIS-APR-113 to
      AEGIS-APR-118, or an owner-approved condition that AEGIS-APR-113 records
      in the coordinator's summary.
    - **Existing rule** means a rule already in force.
    - **Audit** means an acceptance condition this program adopts from the
      independent audit. It is not the owner's words, grants nothing and
      withholds no owner authority; a later plan changes it only by a dated
      note here.
    - **Open** means not decided by this record.

    A **blob ID** is the Git object ID of a file's exact content. It survives a
    squash merge when the content is unchanged.

    | # | Condition | Source |
    | --- | --- | --- |
    | 1 | No switch until the repaired tool passes an independent review. That review uses labelled ground truth: the 18 pages the audit found over-counted, as positive backfill cases; the known misreadings (ledger lines 2569, 2634, 2637 and 2638 as of `d6e48418`; `scoped-approval-register`, `database-backup-verifier`, `file-upload-storage-architect`) as negative cases; refusal of a shallow clone; and a fresh-clone rebuild. The tool's tests run locally, including on Python 3.14, because CI does not run them. | Owner (the gate); Audit (content) |
    | 2 | The index reads only the keeper's table. This record states requirements for that table. The exact schema, field list, validity rules and rejection list are defined by the tool-repair plan and its independent plan audit, if the owner resumes the program. (a) The table keeps the existing keeper table's columns (Page, Acceptance revision, Reviewer, Evidence source, Date, in the first ledger-keeper recording) and adds at least a blob ID, an event kind and a stable identifier for every event. The event kinds include at least a full-page acceptance, a targeted review (AEGIS-APR-116) and a withdrawal (AEGIS-APR-117). (b) Every row carries an evidence pointer to the posted record it rests on: for a backfilled row, the ledger or evidence-record location and revision whose text the row quotes (row 4); for a withdrawal, the evidence that the cancelled event was wrong. The build runs offline, so the recording pull request's independent review checks that the pointer leads to a qualifying record bound to the recorded revision; AEGIS-APR-101 binds each recording "to the exact reviewed revision and its posted evidence". A pull-request comment can still be edited or deleted on GitHub; that residual is recorded, not solved. (c) A withdrawal identifies the specific earlier acceptance event of the same page that it cancels, and cannot cancel a later valid event. A page becomes pending again only when its status rested on the cancelled event, as this record reads AEGIS-APR-117's "The affected page becomes pending again." Whether a targeted-review row may be withdrawn as an "acceptance row" under AEGIS-APR-117 is Open. (d) A lost commit is recorded without binding it, in the backfill's reviewed report or as an event of its own kind, and never counts as an acceptance (rows 5 and 8). (e) The build rejects loudly, and does not count, any malformed row, or any row whose offline checks (commit, blob ID, identifiers) fail. (f) The index never reads the "Candidates examined and NOT recorded" table, `../` links resolve relative to the ledger, and `stated-acceptances.json` stops being an input. | Owner ("the index reads only that table"; AEGIS-APR-116; AEGIS-APR-117, as this record reads it); Existing rule (AEGIS-APR-101's evidence binding); Audit (the requirements); Open (withdrawing a targeted-review row) |
    | 3 | The keeper keeps recording in the ledger under AEGIS-APR-101, unchanged except for the table's format. Two separate grants add to the keeper's role: targeted-review rows once the fixed-format table exists (AEGIS-APR-116), and withdrawal rows after a switch (AEGIS-APR-117). Neither changes AEGIS-APR-101. | Owner (AEGIS-APR-101 unchanged; AEGIS-APR-116 and AEGIS-APR-117) |
    | 4 | Backfill verification. Each backfilled row's quoted text is found verbatim in the cited ledger or evidence record at a stated revision, and that location is the row's evidence pointer. The full commit resolves, and the blob ID equals `git rev-parse <commit>:<path>`. In the backfill from ledger prose, retention, negated, targeted-only and "becomes pending" text never yields a full-page acceptance row. Whether the one-time backfill may transcribe a historical targeted review as a targeted-review row is not decided by this record: AEGIS-APR-116 covers the keeper's recordings, and the owner was not asked about the backfill. A row that cannot be verified is not written as an acceptance, so its page counts as pending. An independent reviewer checks every row, and the build rejects a malformed row loudly. | Owner ("one-time reviewed backfill"); Audit (the verifiable quote and all checks); Open (backfill transcription of targeted reviews) |
    | 5 | A page whose recorded acceptance commit no longer exists anywhere (`65bacc7`, `d3dcb62`, `3c44f4a`, `e9cce7d`, `288d993` and `7f98950` are known) counts as pending until it is re-reviewed. So does a page whose change since its recorded acceptance cannot be measured for any other reason. A commit still held by a pull-request head is not lost (row 8). Such rows are never bound to another commit and never dropped silently. | Owner (AEGIS-APR-113: "Pending until re-reviewed (Recommended)", for lost commits and for other unmeasurable changes); Audit (never re-bound, never dropped silently) |
    | 6 | Reproducible build. Inputs are read at `--ref`, not from the working tree; diff flags are pinned; an unresolved revision is annotated, never dropped; test expectations are derived, not hard-coded; the build refuses a shallow clone and refuses a drop in recorded rows. | Audit |
    | 7 | The page set is derived at `--ref`: new pages start pending, deleted pages drop out, and the JSON output lists the no-record pages. This is what makes rebuilding on demand and after each keeper recording sufficient. | Audit |
    | 8 | Discovery and preservation. Rebuilds run only in a full clone that has fetched `refs/remotes/**` and `refs/pull/*/head`. The build's `--ref` is pinned to the rebuild pull request's base commit on the default branch, named in the pull request, and never to the rebuild's own commit. The reason is that the build records its input ref as `source_revision` in both generated files (`tools/readability_acceptance/build_index.py`), so a run at the candidate head would always differ. The reviewer rebuilds at that same ref and requires a zero diff. If the default branch has moved by merge time, the rebuild is redone at the new tip. A repaired format that records no self-reference is also acceptable, if the tool-repair plan chooses it (row 6). Fetching finds a commit only while some reference still holds it; it does not preserve it. So before the switch, every acceptance commit that a keeper-table row records is held by a durable preservation mechanism that the repaired tool reads; commits already lost are governed by row 5, and no row binds them (row 4). The tool-repair plan names the mechanism, and a new reference namespace, a tag convention or a merge-method rule needs the owner's decision first. The blob ID is a content check: it binds the row to the page's exact bytes at the recorded revision (row 4 verifies it). It is not preservation: under row 5, a page whose commit is lost counts as pending even when its blob survives. Rows 2, 5 and 8 together are how "acceptance commits are preserved" (AEGIS-APR-113) is met. | Owner (approved condition, in the coordinator's summary: "acceptance commits preserved"); Audit (the mechanism) |
    | 9 | "whoever does the rebuild is a coding agent or a human". When a coding agent does it: never the coordinator, never a holder of another stage of that pull request, and the seven stages apply. | Owner (recommendation); Existing rule (agent limits) |
    | 10 | Scope fence: repair and rebuild pull requests touch only `tools/readability_acceptance/**` and `docs/**`, and never `tools/__init__.py`, which is a `gate-guard` path. If the repaired build writes any path other than the two files AEGIS-APR-115 names, the switch plan raises it with the owner before relying on AEGIS-APR-115. | Audit; Owner ("Nothing else is covered.") |
    | 11 | The targeted-edit rule applies as written: "A small edit keeps acceptance only if an independent reviewer checked it". For the index to see that check, it must be recorded as a targeted-review row (row 2's event kind) that identifies the reviewed revision and the retained full-page acceptance it builds on, by its identifier (exact fields: row 2 and the tool-repair plan). A targeted review covers the change from the retained acceptance up to its reviewed revision; a later change needs its own review, as the rule says of any unreviewed edit. The 10-line net difference is still measured from the retained full-page acceptance (the ledger rule). The switch states the resulting count before it takes effect. The keeper may record such rows under AEGIS-APR-116 once the fixed-format table exists. This settles, for the keeper's recordings, the point on which the conversion process's (b)2 and (b)3 differ. | Existing rule; Owner (AEGIS-APR-116: "Yes, explicit grant (Recommended)"); Audit (the recording need and schema) |
    | 12 | One published count. At the switch, dated forward notes go on every surface that states or implies the ledger's count: at least the open-decisions row on edits made before the 10-line rule (with a re-check of the page's opening banner), `tools/readability_acceptance/README.md`, the ledger's count statements, `docs/skill-eval-behavioral-test-procedure.md` ("the stated totals move with it") and the forecast. `CONTRIBUTING.md`'s sentence that the ledger "tracks the full repository sweep and reviewed batches" is re-checked; it does not claim the count, so it stays. After the switch, no page other than the index states the figure. Otherwise rebuild-only pull requests (AEGIS-APR-115) could not keep the other pages current. | Owner (one source of truth); Audit (list and rule) |
    | 13 | There is no CI gate. Any later CI job ("a separate, non-blocking CI job") never fails on drift, fetches full history and pull-request heads, has its own path filter, and needs a one-time owner `gate-guard` exception, because `.github/workflows/` is protected. | Owner (no CI gate; an optional non-blocking job later); Audit (conditions) |
    | 14 | `tools/readability_acceptance/` is security-relevant "approval/evidence tooling under `tools/`" (AEGIS-APR-118, **in effect now**): a pull request that touches it answers the security-relevant-surface question **Yes**, naming it, and an outside contribution that touches it gets the additional security review. This confirms `CONTRIBUTING.md`'s existing wording; that file is unchanged. | Owner (AEGIS-APR-118: "Yes, security-relevant (Recommended)") |
    | 15 | The rule stays out of `SKILL.md` files and `CLAUDE.md`, and no skill cites the ledger, the index or the tool. | Audit |

  - **Consequences.**
    - **Easier:** the count becomes one command. After the switch, ledger prose
      stops being machine input, so ledger edits need no harvester-safe
      wording. A blob ID lets the build and a reviewer check that a row matches
      the page's exact content at its recorded revision.
    - **Harder:** a one-time backfill (option B was shown to the owner at "About
      16–32 agent-hours (estimate)"; later variant estimates are in the backlog
      item). Every rebuild is a full seven-stage `tools/` pull request with
      about 4–5 minutes of CI per head.
    - **Expected:** the official count will rise once the no-record rule, the
      lost-commit rule and the targeted-edit rule's review condition apply.
    - **While paused:** the readability ledger stays the record, and its
      process is unchanged. That answers the owner's question
      "we stopped the program but would that break any of the current ledger process":
      no. Its hand count stays a known-stale floor, and the exact count stays
      not derivable; the ledger's current reading says why. Nothing in
      `tools/` changes.
  - **Reversal.** Before the switch nothing has changed, so there is nothing to
    reverse. After it, a later owner decision can return the count to the
    ledger; the keeper's table stays a valid ledger record, so no record is
    lost. No point of no return was identified.
  - **Not decided here:**
    1. whether and when the program resumes, and which repair to build;
    2. whether the one-time backfill may transcribe historical targeted
       reviews (row 4);
    3. the lighter review path for machine-checked rebuild pull requests,
       which the owner chose to raise at the 2026-10-11 review-cap check-in.

    Whether a program function may be delivered in more than one pull
    request is no longer open for the tool repair: AEGIS-APR-114 records the
    owner's "Parallel repair PRs" choice and its split-PR merge terms.
  - **Authority.** The owner's current direct instructions of 2026-10-07, as
    transcribed by the coordinator from the session chat. The register's
    preamble makes them "valid source evidence before transcription". This
    entry grants nothing. Its register companions are AEGIS-APR-113 and
    AEGIS-APR-118 (POLICY DECISIONs, which grant nothing) and AEGIS-APR-114 to
    AEGIS-APR-117 (GRANTs).
  - **Status at recording.** Recorded 2026-10-07 against `origin/main` at
    `7d1d05e8`. No skill, tool, script, workflow or protected path changes, and
    no count changes; the ledger's current reading stands until the switch.
    The program is paused after this decision record. **Review:** if the
    owner resumes the program, its first plan re-checks each condition above
    against the default branch at that time.
  - **Correction (appended 2026-10-08, no rewrite of the D73 record; verified
    against `origin/main` at `c060a7cb`).** Two points in this entry are
    clarified. No condition, source label, owner decision or count above
    changes.
    1. **Row 2 (e) applies per event kind.** "any row whose offline checks
       (commit, blob ID, identifiers) fail" means the checks that apply to
       that row's event kind. A lost-commit event, which (d) allows, records a
       commit that by definition does not resolve, so the build does not
       reject it for that, and it still never counts as an acceptance. A
       withdrawal is checked against the earlier event it cancels, as (c)
       requires. Which checks apply to each kind stays part of the validity
       rules that the tool-repair plan defines (row 2). This answers minor
       finding m-1 of the round-3 implementation audit on PR #678 (comment
       6049874529).
    2. **"Not decided here" has a fourth item:** 4. whether a targeted-review
       row may be withdrawn as an "acceptance row" under AEGIS-APR-117. Row 2
       (c) and its Source cell already mark it Open, and the list above
       omitted it (finding m-2 of the same audit). AEGIS-APR-113's "Not
       decided by this entry" list is not edited: the register's preamble
       says "do not edit old entries", and the item concerns the scope of
       AEGIS-APR-117, not what AEGIS-APR-113 decides.

- **D74 (2026-10-08) — Exact sourced publication of stage skills rows.**
  The owner selected exact sourced copying of another stage agent's
  self-authored four-column skills row by an already authorized PR editor.
  This resolves the literal "no agent writes another stage's row" ambiguity:
  authorship stays with the stage agent while publication may be delegated as
  an exact copy from a fixed, retrievable source. Preserve agent, round,
  reviewed target and `UNRUN` limits; compare the completed table with those
  sources before the existing bound-field hash. The canonical procedure is
  [Authoring and publishing skills rows](../delivery-workflow.md#authoring-and-publishing-skills-rows),
  and the complete owner question and selected label are in the new
  [approval-register policy record](../approvals/APPROVAL_REGISTER.md).
  The choice grants no new PR edit, stage, merge, tool or reserved-work
  authority and does not rewrite D72 or AEGIS-APR-105. Source capture and
  serialized readback are procedural evidence, not machine enforcement or an
  atomic multiwriter guarantee.

- **D75 (2026-10-09) — QA Tier 2 design batch built (three skills).**
  Decided and built the three G1 BUILD rows of
  [the unselected-expansion proposal](../roadmaps/unselected-expansion-skill-batch-proposal.md)
  (rows 538–540, owner-selected): `visual-regression-test-designer` (roadmap
  #203), `exploratory-charter-designer` (roadmap #228, banked as
  `exploratory-testing-charter`), and `mobile-journey-test-designer` (roadmap
  #230, banked as `mobile-viewport-qa`). All three are read-only QA *design*
  skills — they emit coverage designs and charters in conversation and
  capture, execute and drive nothing — so all three are auto-invocable with
  no `disable-model-invocation` and no MANUAL-ONLY sentinel, per standard §5
  and the proposal's posture note. Each ships `evals/evals.json` and
  `evals/trigger-evals.json` discriminating against its named neighbors.
  Family 6 "QA, E2E & evidence" grows 19 → 22; the library total grows
  195 → 198; FAMILY-COUNT stays 23. The D10 Tier 2 rows for #203/#228/#230
  are marked built above (§3). This entry records the build decision and the
  shipped arithmetic; it grants no new execution, publication or merge
  authority.

- **D76 (2026-10-10) — Role-coverage test design skill built (#229, narrowed).**
  Decided and built the G1 row 541 candidate `role-based-qa-matrix` (#229 P1)
  of [the unselected-expansion proposal](../roadmaps/unselected-expansion-skill-batch-proposal.md),
  owner-selected and narrowed as `role-coverage-test-designer`. The skill is a
  read-only QA *design* skill — it emits the role-coverage design (role ×
  surface allowed-path matrix, interface-consistency deltas, layer-mapped
  coverage) in conversation and edits, executes and drives nothing — so it is
  auto-invocable with no `disable-model-invocation` and no MANUAL-ONLY
  sentinel, per standard §5. It consumes the shipped
  `authorization-matrix-designer` matrix as input (compose, never restate);
  denials stay with `authorization-matrix-designer` step 7 and
  `multi-tenant-security-tester`; custom-role, grant-ceiling and
  role/resource-inheritance coverage is deferred to the unbuilt #59 extension
  (a documented seam, not a build claim). It ships `evals/evals.json` and
  `evals/trigger-evals.json` discriminating against its six named neighbors.
  Family 6 "QA, E2E & evidence" grows 22 → 23; the library total grows
  198 → 199; FAMILY-COUNT stays 23. The D10 Tier 2 row for #229 is marked
  built above (§3). This entry records the build decision and the shipped
  arithmetic; it grants no new execution, publication or merge authority.

- **D77 (2026-10-10) — Batch A design trio built (three skills).**
  Decided and built three owner-selected proposal rows in one batch:
  `validation-boundary-designer` (G3 row 569; roadmap #37 + #38 + #141 +
  #157), `observability-by-design` (G3 row 570; roadmap #22), and
  `property-based-test-designer` (G2 row 554; roadmap #194, D10 Tier 3). All
  three are read-only *design* skills — they emit designs in conversation and
  write, run, edit and drive nothing — so all three are auto-invocable with
  no `disable-model-invocation` and no MANUAL-ONLY sentinel, per standard §5.
  Each ships `evals/evals.json` and `evals/trigger-evals.json` discriminating
  against its named neighbors, including the manual-only ones. Honesty
  caveats from the proposal stand: design-time placement is a research
  hypothesis (row 569), comparative demand needs review (row 570), and
  property-based testing stays on-demand-qualified (row 554); this entry
  records the build decision, not verified demand or effectiveness.
  `validation-boundary-designer` composes the mass-assignment and denial
  coverage of `security-pr-reviewer` and `multi-tenant-security-tester`;
  `observability-by-design` composes `sensitive-disclosure-guard`'s redaction
  rules by reference. Family 3 "Core architecture & engineering" grows
  10 → 12; family 6 "QA, E2E & evidence" grows 23 → 24; the library total
  grows 199 → 202; FAMILY-COUNT stays 23. The D10 Tier 3 row for #194 is
  marked built above (§3). This entry records the build decision and the
  shipped arithmetic; it grants no new execution, publication or merge
  authority.

- **D78 (2026-10-10) — Batch B EXTENDs built (three extensions).**
  Decided and built three owner-selected proposal EXTENDs in one PR:
  #213 per-layer test-timeout policy extended into `qa-automation-architect`
  (G1 row 544; per-suite limits derived from tier budgets, timeout behavior,
  timeout↔retry interaction; finished-run classification stays with
  `ci-failure-classifier`, pipeline job-level limits stay with
  `ci-pipeline-architect`); #59 role-assignment rules with a grant ceiling,
  role/resource inheritance and tenant-defined custom roles extended into
  `authorization-matrix-designer` (G4 row 586; Security Rules, Tenant
  Isolation Rules and Stop Conditions edited — the extension's
  security-relevant surfaces); #195 mutation-report reading extended into
  `test-coverage-mapper` (G2 row 555; survived/killed/equivalent triage as
  coverage-gap evidence; Stop Conditions extended — a security-relevant
  surface). The honesty caveats from the proposal stand: no timeout guidance
  existed (row 544), mutation demand is unmeasured (row 555), and only
  machine actors had assignment/inheritance guidance before this extension
  (row 586); this entry records the build decision, not measured demand.
  Counts are UNCHANGED: no new skills, SKILL-COUNT stays 202, FAMILY-COUNT
  stays 23, family counts stay 12/24. The approved wording-only reciprocity
  edit refreshed `role-coverage-test-designer`'s deferral seams to "the #59
  extension (built by D78)" — its Stop Conditions line ("stop; not designed
  here") was intentionally left unchanged under the lead's constraint and
  remains correct; D76's entry above is immutable and is forward-corrected
  here, not rewritten. The D10 Tier 3 row for #195 and the Phase 3
  `role-permission-architect` row are marked built above (§3). This entry
  records the build decision and the shipped arithmetic; it grants no new
  execution, publication or merge authority.

- **D79 (2026-10-10) — Batch C architecture EXTENDs built (three extensions).**
  Decided and built three owner-selected proposal EXTENDs in one PR:
  #9 per-operation request/response schema conventions extended into
  `api-event-architect` (G3 row 571; typed fields, validation shape,
  per-operation additive-vs-breaking feeding the versioning policy, error
  envelope bound to `error-taxonomy-designer`'s model by citation; the
  extension's scope decision states the skill covers public/partner APIs AND
  first-party client-facing endpoints — the proposal's "unverified"
  first-party question is answered by the extension, not assumed away);
  #17/#144 idempotency outcomes extended into `command-gateway-architect`
  (G3 row 568 item 2; same-key-different-payload and in-flight duplicate
  policies added to step 4 and the Output Idempotency line; description
  unchanged — 944 parsed chars leave too little headroom); #17's spec half
  extended into `product-spec-writer` (item 3; repeated-request outcomes —
  retry / double-submit / second-tab / stale-request / duplicate-events —
  per state-changing action, mechanism routed to `tech-spec-writer` and
  `command-gateway-architect`; description unchanged — 961 parsed chars).
  The honesty caveats stand: the #9 first-party scoping premise was
  unverified at the proposal (row 571); the strongest objection to the
  gateway extension (a one-endpoint product) and D30's recorded "TOP
  pull-forward" remain named design questions; AEGIS-013/AEGIS-028's root
  cause is still recorded "not yet verified" and this extension adds eval
  cases, not a fresh-session regression run (row 568). This entry records
  the build decision, not measured demand or effectiveness. Security:
  **No** — no invocation posture, Security Rules, or Stop Conditions of any
  target skill was edited. Counts are UNCHANGED: no new skills; SKILL-COUNT
  stays 202; FAMILY-COUNT stays 23; families 4/14/18 stay 10/15/11. The
  Phase 2 expansion-list marks for #9 and #17/#144 are recorded above (§3);
  D30/D31/D76/D77/D78 entries are untouched and forward-corrected only by
  this entry's marks. This entry records the build decision and the shipped
  arithmetic; it grants no new execution, publication or merge authority.

- **D80 (2026-10-10) — Batch D: nine DROP closures recorded (docs-only).**
  Decided and recorded nine DROP dispositions from the unselected-expansion
  proposal in one docs-only PR. The two tentative drops were resolved by
  fresh full-body reviews: `mock-strategy-designer` (#200/#201, row 542) —
  DROP confirmed, covered by `integration-test-designer` (boundary map
  REAL/FAKED with per-fake rationale, :70–75; drift-symptom Use When,
  :28–29; fidelity gotcha, :164–167), `vitest-unit-component-engineer`
  (owned-seam mocking + restore, :64–67; mock-boundaries output, :86;
  boundary-crossing refusal, :104/:121–123) and `api-contract-test-designer`
  (fake-fidelity Use When, :33–34; scheduled re-validation, :84–86; plan +
  checklist, :102/:117) — no residual slice; `ci-shard-parallel-isolation`
  (#211/#212, row 543) — DROP confirmed, covered by
  `sharded-validation-with-resume` (named functional shards, :65–68;
  run-id/status semantics, :111–113; resume law, :120–133; aggregate gate,
  :148–152) and `qa-automation-architect` (isolation + parallelization,
  :87–90; CI sharding plan, :94–95) — no residual slice. Plain drops:
  `soak-test-planner` (#207) → `load-test-planner` (soak named in Use When
  :25 and body :227–230; trigger-evals route soak prompts :30–33);
  `chaos-test-planner` (#208) → `resilience-architecture-reviewer`
  (fault-injection/game-day plan :47–48; step 7 writes it :158; execution
  refused :231–233); `operational-runbook-author` (#23) →
  `incident-response-runbook`, `rollback-runbook-author`,
  `data-migration-runbook-author`, `gated-deployment-prompt-template`,
  `onboarding-doc-designer`; `system-context-mapper` (#2) →
  `architecture-designer` step 1 (:57–59) + `threat-modeler` (:70–72, output
  :104–106); `bounded-context-identifier` (#4) → `domain-modeler` step 4
  (:55–58); `e2e-test-architect` → the `qa-strategy-architect` +
  `test-plan-designer` + `qa-automation-architect` +
  `regression-suite-curator` (:126) + `test-data-architect` (:3, :61–63) +
  `playwright-e2e-engineer` (:122) composition; `qa-closeout-reporter` (#235)
  → `ai-closeout-reporter` (:3, :14–19) + `release-readiness-reviewer` (:3,
  :14–21) (the shipped trigger-eval pin's "stays in the backlog" intent —
  `screenshot-evidence-planner` trigger-evals:25 — is now satisfied by this
  drop record). Intentionally NOT
  done: the proposal's optional soak token/session-expiry note (row 556) is
  not taken up — a later `load-test-planner` extension would be its own PR;
  `dependency-direction-guard` (#6/#7) and `refactor-safety-planner` (#11)
  remain DEFER (not closed); #189's PARTIAL/DEFER and all non-DROP proposal
  rows are untouched; the proposal page itself is unchanged (published
  history). Counts are UNCHANGED: no skill added, removed or renamed;
  SKILL-COUNT stays 202; FAMILY-COUNT stays 23. This entry records the
  closure decisions and the shipped arithmetic; it grants no new execution,
  publication or merge authority.

- **D81 (2026-10-10) — Batch E tenant-lifecycle design skills built (two skills).**
  Decided and built two owner-selected proposal rows in one PR:
  `tenant-provisioning-designer` (G4 row 587; roadmap #57) and
  `membership-invitation-designer` (G4 row 588; roadmap #58, built after
  #59). Both are read-only QA/design skills — they emit workflow designs in
  conversation and create, configure, send, generate, and execute nothing —
  so both are auto-invocable with no `disable-model-invocation` and no
  MANUAL-ONLY sentinel, per standard §5. The honesty caveats stand:
  `tenant-modeler` gives lifecycle semantics only (row 587) and models
  invitation states but not token/binding/seat/spam mechanics (row 588);
  this entry records the build decision, not measured demand. Compose,
  never restate (proposal rows 514/518/512): both skills compose
  `command-gateway-architect`'s idempotency contract (including the D79
  different-payload and in-flight policies), `api-event-architect`'s
  rate-limit contract, `plan-entitlement-architect`'s seat pool, and the
  #59-extended `authorization-matrix-designer` grant-ceiling/custom-role
  output as inputs by reference. Each ships `evals/evals.json` and
  `evals/trigger-evals.json` discriminating against its named neighbors,
  including the manual-only ones (test-tenant-provisioner,
  secrets-identity-hardener, multi-tenant-security-tester) with the §6
  prefix. Family 4 "SaaS & tenant isolation" grows 10 → 12; the library
  total grows 202 → 204; FAMILY-COUNT stays 23. The Phase 3 expansion-list
  marks for #57 and #58 are recorded above (§3). This entry records the
  build decision and the shipped arithmetic; it grants no new execution,
  publication or merge authority.

- **D82 (2026-10-10) — Storage-policy handoff narrowed (option R; five files).**
  The owner selected option R — a narrow routing correction, not an
  EXTEND. The shipped overbroad handoff in
  `file-upload-storage-architect` (its description, Use When, workflow,
  output, checklist, supporting-file note, evals, trigger-evals, catalog row
  and README row) claimed `rls-policy-auditor` audits "existing storage
  RLS/bucket policies"; the receiver's contract is database-RLS-only. The
  five-file edit set (P1/P2/P3/P8/P8b) narrows every sender promise to the
  supplied DATABASE RLS policies governing object metadata/access, and
  explicitly states that provider-native bucket permissions, public-serving
  behavior and signed-URL enforcement remain UNVERIFIED unless separately
  scoped. The receiver (`rls-policy-auditor` — SKILL.md, its checklist
  reference, evals.json, trigger-evals.json) is byte-preserved (P4–P7); the
  sender's Stop Conditions and invocation posture are untouched; no
  provider reviewer was invented and no blanket rerouting occurred. The
  mixed trigger case was split: the database-RLS prompt keeps
  `expected_skill: rls-policy-auditor`, and the mixed bucket+RLS prompt's
  reason states the database slice routes there while the bucket/
  public-serving/signing evidence stays unreviewed — no object-store safety
  verdict is claimed. Roadmap #115 remains residual in the catalog's Phase 4
  expansion backlog (catalog "storage-policy review" entry untouched);
  #112 and #127 are out of scope. Counts are UNCHANGED: no skill added or
  renamed; SKILL-COUNT stays 204; FAMILY-COUNT stays 23. This entry records
  the owner's R selection and the shipped correction; it grants no new
  execution, publication or merge authority.

- **D83 (2026-10-10) — role-coverage L108 Stop Conditions refreshed.**
  Origin: the readability sweep fifth batch (PR #707) recorded a named
  follow-up for `role-coverage-test-designer`: L108 (Stop Conditions) read
  "deferred to the unbuilt #59 extension" while the page's own L37/46/78/90/100
  and evals.json:16 read "built by D78" — the internal contradiction the D78
  entry intentionally left, because any L108 refresh is a Stop Conditions
  edit and must be named in the PR's security-answer surfaces. The
  lead/coordinator, the follow-up's recorded owner, decided to proceed under
  exactly that condition. This lane rewords L108 to "deferred to the #59
  extension (built by D78) — compose, never restate; not designed here":
  wording-only, the stop behavior (still refuses to design custom-role,
  grant-ceiling and inheritance coverage) is unchanged, and no frontmatter,
  posture, evals or trigger-evals line changed. The PR's security answer is
  **Yes — the edited skill's Stop Conditions** (the single named surface),
  which is the D78-entry condition honored. D76's entry above keeps its
  historical "unbuilt" text — immutable history, forward-corrected here, not
  rewritten. D82 and earlier entries are byte-untouched; counts are
  UNCHANGED (SKILL-COUNT 204, FAMILY-COUNT 23). This entry records the
  refresh; it grants no new execution, publication or merge authority.

- **D84 (2026-10-10) — Readability index repair + official-count switch.**
  The owner-selected item (AEGIS-APR-113 item 9 / D73) resumed: the repaired
  `build_index.py` reads ONLY the ledger's consolidated keeper table (schema
  v1, the `<!-- acceptance-index-schema: 1 -->` sentinel; columns Stable ID,
  Page, Event kind, Acceptance revision, Blob ID, Quote, Reviewer, Evidence
  source, Date) — the prose harvester and `stated-acceptances.json` are
  retired as inputs; the four prose blind spots are moot by construction and
  pinned as negative regression tests together with the three named
  misreadings. The one-time reviewed backfill transcribed the 12 keeper
  sections' full-page-acceptance rows (the mechanical count is derived by the
  build, never asserted) with per-row verbatim quote, resolving commit, and
  blob ID `git rev-parse <commit>:<path>`; historical targeted reviews were
  NOT transcribed (lead decision 1 — the D73 row-4 Open stays flagged). The
  six named lost commits (65bacc7d6b85, d3dcb62a335d, 3c44f4a, e9cce7d,
  288d993, 7f98950) are recorded as `lost-commit` events — never bound,
  never dropped; their pages count as pending until re-reviewed. Preservation
  is main-containment at build time (lead decision 2); a stronger refs
  namespace/tag convention stays an owner-choice item. `check_index.py` now
  prints the official buckets and the official pending count at the pinned
  ref; the switch PR stated that count at its pinned base before effect, and
  the one-published-count rule moved every counting surface (ledger, tool
  README, open-decisions row, skill-eval procedure, forecast) to cite the
  index — the ledger publishes no count of its own. Lifecycle: this PR
  appends APR-114's CONSUMED event (its own recording step) and APR-115
  becomes ACTIVE from its merge. The repair and the switch were delivered as
  ONE pull request under APR-114's repair scope with the switch's
  requirements embedded. N12/N13 untouched; the "212" frozen-basis figure is
  not reproduced as any current count. Two further recorded acceptances (the
  first keeper recording's `e6fc8d24` setup pages) rest on a revision not
  contained in `refs/remotes/origin/main`; under the owner-selected
  main-containment preservation rule they carry NO acceptance row and their
  pages count pending until re-reviewed. Counts UNCHANGED (SKILL-COUNT 204,
  FAMILY-COUNT 23). This entry records the repair and the switch; it grants
  no new execution, publication or merge authority.

  **Amendment, 2026-10-10 (SD-D REVISE round 2, PR #715).** Two narrow
  fixes, append-only: (1) the APR-114 CONSUMED event's defining ID was
  duplicated; the event now carries its own ID **AEGIS-APR-125** (the
  ID-114 entry keeps its GRANT heading), so the WSL2 lane's planned
  "APR-125 grant" renumbers to **APR-126**; (2) `build_index.py`'s writer
  now pins LF newlines (`newline="\n"`) so a Windows reviewer rebuild is
  byte-identical to the committed JSONs. No content or count change.

- **D85 (2026-10-10) — WSL2 Linux host proposal for the BER Stage A
  candidate (repo phase).** The owner revised the BER R4/R5 Stage A Linux
  capability candidate platform: **WSL2 selected, superseding the VirtualBox
  path** chosen in APR-028's reviewed proposal; the existing VirtualBox VM is
  NOT deleted — deletion requires a separate owner approval plus operator
  confirmation — and stays untouched and unverified. This lane (repo phase
  ONLY — no wsl or host commands) delivered the reviewed proposal page
  (`docs/roadmaps/ber-wsl2-stage-a-setup-proposal.md`), the register's two
  required append-only records — a SUPERSESSION event for APR-028 with its
  own unique ID **AEGIS-APR-127** and the new **AEGIS-APR-126 GRANT** (the
  plan under audit named it APR-125; APR-125 was taken by the index-repair
  lane's APR-114-CONSUMED event, per the D84 amendment) whose scope mirrors
  APR-028 line-by-line with the WSL2 specifics and the deletion rule — and
  this entry. Probe facts are quoted from the lead-run read-only 2026-10-10
  observations (WSL 2.7.12.0, kernel 6.18.33.2-2, WSLg 1.0.73, Windows build
  10.0.26200.9448); the supply-chain statement is honest (Microsoft-signed
  Store AppX, no third-party ISO). Counts UNCHANGED (SKILL-COUNT 204,
  FAMILY-COUNT 23). This entry records the decision and the grant; it grants
  nothing itself and authorizes no host action. D84 and earlier entries are
  byte-untouched.

- **D86 (2026-10-10) — N12 non-hub reciprocal change + folded-in seam fix.**
  The owner selected N12 from the route002 triage (ci-failure-classifier →
  sharded-validation-with-resume, b-high). The source side was already
  complete; this lane closed the one-way gap: sharded's Use When gains the
  Do-NOT boundary (a single stopped CI run's log classification routes to
  `ci-failure-classifier`) and the broad-first-bullet qualifier, its
  Supporting Files names the neighbor, and its trigger-evals gains
  `ci-failure-classifier` in overlaps_with plus one near-miss case
  (expected_skill `ci-failure-classifier`, auto-invocable, no §6 prefix).
  The folded-in batch-2 named follow-up discharged: local-ci-mirror-preflight's
  trigger-evals gains the `ci-failure-classifier` discrimination case and the
  overlaps entry, and its Supporting Files names the neighbor (its
  description/Use When already named it). route002's N12 disposition cell
  reads built (D86, 2026-10-10); line 46, the §N12 note, and every other row
  are byte-untouched. N13 remains an owner-selection item — untouched. No
  posture, Stop Conditions, Security Rules, or description changed anywhere
  (sharded's description is byte-unchanged at 1009 of the 1024-cap parsed
  length — the arithmetic is in the PR body). Counts UNCHANGED (SKILL-COUNT
  204, FAMILY-COUNT 23). This entry records the lane; it grants no new
  execution, publication or merge authority. D85 and earlier entries are
  byte-untouched.

- **D87 (2026-10-10) — N13 non-hub reciprocal change.** The owner selected
  N13 from the route002 triage (cloud-security-baseline-reviewer →
  azure-saas-architect, b-high). The source side was already complete (its
  description names the boundary and its trigger-evals carries both triage
  cases + the overlaps entry; its Security Rules section is untouched); the
  lane closed the one-way gap with zero prior mentions of the neighbor
  anywhere in azure-saas-architect (git grep count 0 before the edit):
  azure-saas-architect's Use When gains the Do-NOT boundary (an EXISTING
  subscription's configured controls vs a named technical baseline routes to
  `cloud-security-baseline-reviewer`) and the :48–49 bullet qualifier, its
  Supporting Files names the neighbor, and its trigger-evals gains
  `cloud-security-baseline-reviewer` in overlaps_with plus one near-miss
  azure-exports case (expected_skill `cloud-security-baseline-reviewer`,
  auto-invocable, no §6 prefix). Its description is byte-unchanged at 999 of
  the 1024-cap parsed length (cap arithmetic in the PR body). route002's N13
  disposition cell reads built (D87, 2026-10-10); line 46, L58, L60–62, the
  N12 row (built (D86)), and every other row are byte-untouched. No posture,
  Stop Conditions, Security Rules, or description changed anywhere. Counts
  UNCHANGED (SKILL-COUNT 204, FAMILY-COUNT 23). This entry records the lane;
  it grants no new execution, publication or merge authority. D86 and earlier
  entries are byte-untouched.

- **D88 (2026-10-10) — Register-transcription housekeeping (gated item 4,
  final).** Mechanical transcription of exactly two entries: APR-121 (the PR
  #682 green-only merge hold) and APR-123 (the exact sourced publication of
  stage skills rows) each relocate their `New authority` bullet from after
  `Evidence` to its canonical slot after the `Decision maker / effective
  order` (Date/Grantor-equivalent) field — the same bullet text, moved only;
  zero word changes (sorted-line byte-equality per entry, and the register's
  B..H diff shows exactly the two relocation hunks: 2 removed lines + 2
  identical added lines). The deviation inventory's exclusions are honored:
  the alternate field labels (`Decision maker / effective order`,
  `Scope FORBIDDEN / boundaries`, `Expiry / future changes`,
  `Related grant / scope`, and the established `Recorded at / by`
  alternates), APR-127's SUPERSESSION wording, and the six
  `Scope allowed (selected policy)` variants are NOT normalized — renaming or
  filling them would change the entries' words, outside the owner's
  no-content-change scope; each is flagged as an owner-choice item. The
  APR-028 no-deletion rule is NOT duplicated: it is already recorded with the
  affected grant ID twice by the WSL2 lane (APR-126 Scope allowed + Scope
  FORBIDDEN; APR-127 Status at recording, whose heading names target grant
  AEGIS-APR-028), satisfying the preamble's append convention — no new event
  added. Counts UNCHANGED (SKILL-COUNT 204, FAMILY-COUNT 23). This entry
  records the transcription; it grants no new execution, publication or merge
  authority. D87 and earlier entries are byte-untouched.

- **D89 (2026-10-10) — BER-DEC grant lane: BER R4/R5 Stage A offline host
  probe authorization (WSL2).** The owner answered "go" to the NEXT step
  after the prepared, verified WSL2 distribution: the offline Stage A host
  probe. The lane (repo phase ONLY — no probe execution, no host actions)
  delivered the three-artifact instrument per the BER-DEC-014/APR-046
  precedent: the **AEGIS-APR-128 GRANT** (scope allowed pinned to the
  WSL2 Ubuntu-24.04 distro only — alias `aegis-ber-stage-a-wsl`, user
  `peternguyen`, scratch root `/home/peternguyen/aegis-stage-a` mode 700 —
  with the exact command list, the five required POSIX test IDs, the bounded
  credential-free `git archive` placement, the sanitized-Git/raw-external
  evidence split, the named time ceiling, and the stop list; scope FORBIDDEN
  mirrors APR-126/028 and locks DELETION under the owner's quoted rule; the
  capability-observation honesty line preserved verbatim), the
  **BER-DEC-016** append-only decision-log entry (the pinned binding), and
  this entry. The probe executes only after this governance PR merges, in a
  separate, later host phase. Counts UNCHANGED (SKILL-COUNT 204,
  FAMILY-COUNT 23). This entry records the decision and the grant; it grants
  nothing itself and authorizes no host action. D88 and earlier entries are
  byte-untouched.

- **D90 (2026-10-10) — BER guard-fix lane: `_POSIX_EVIDENCE_ATOMIC` runtime
  capability probe.** Root cause: the gate required
  `os.replace in os.supports_dir_fd`, but Python 3.12.3 (Ubuntu 24.04, the
  probe host) carries `os.rename` in that set and NOT `os.replace`, so the
  required POSIX test skipped on the host class the grant was meant to
  unlock. The fix measures instead of assuming: a module-level runtime probe
  runs a real `os.replace(src, dst, src_dir_fd=..., dst_dir_fd=...)` against
  two O_DIRECTORY-opened descriptors inside a `TemporaryDirectory`
  (try/except NotImplementedError/OSError/AttributeError → False); the flag
  is `posix + O_NOFOLLOW + O_DIRECTORY + open/mkdir in supports_dir_fd +
  _dirfd_replace_supported()`, where the static membership is only the
  documented fallback when the probe environment cannot be constructed. The
  write path (`_atomic_write`'s dir-fd mechanics, fail-closed checks,
  Windows detection) is byte-unchanged — the fix changes what the gate
  REPORTS and which test RUNS, never how evidence is written. A regression
  test pins the probe on the POSIX host class and the fallback elsewhere.
  This entry records the **one Stage A probe RE-RUN under APR-128's existing
  scope**: the grant's one bounded probe ran to completion with a required
  POSIX skip (NON_BASELINE, proof incomplete), so after this fix merges the
  same pinned probe program re-runs once — same distro, account, scratch
  root, command list, 60-minute ceiling, and receipt discipline. It grants
  nothing new and creates no new APR/BER-DEC. Counts UNCHANGED (SKILL-COUNT
  204, FAMILY-COUNT 23). D89 and earlier entries are byte-untouched.

- **D91 (2026-10-10) — Skills-recording hardening (manifest + skill-usage-ledger
  + one README guidance page).** The owner's REVISED selection ("YES!") is
  delivered as three components: (1) `tools/skills-manifest.json` — the
  validator-generated manifest binding every shipped skill's name to the
  SHA-256 of its `SKILL.md` bytes (CRLF→LF normalized, checkout-independent,
  git-blob reproducible; `_template` and the manifest itself excluded);
  `scripts/validate-skills.py` gains `check_skills_manifest` (drift → the
  validator fails, so every skill PR must carry the refreshed manifest) and
  the `--refresh-skills-manifest` / `--manifest-ref` flags; (2) the
  `skill-usage-ledger` skill (auto-invocable, emits the six-field
  `skill@<manifest-sha256[:12]> / reason / applied / result / incomplete /
  by` record in conversation and writes nothing; evals + trigger-evals with
  the ai-closeout-reporter near-miss) — registered like any skill: catalog
  Phase-1 row, README shipped row, family 1 *(Phase 1, 8 → 9)*, SKILL-COUNT
  204 → 205, FAMILY-COUNT 23 unchanged, roles table and ZERO_TRUST
  unchanged; (3) the ONE README guidance subsection "Using Aegis skills —
  record what you used" with the honesty framing (trivial, verifiable,
  expected; compliance remains the user's); AGENTS.md untouched. Counts
  UNCHANGED as above except the one new skill (SKILL-COUNT 205, FAMILY-COUNT
  23). This entry records the lane; it grants no new execution, publication
  or merge authority. D90 and earlier entries are byte-untouched.

- **D92 (2026-10-11) — dirfd capability-probe repair, published.** The
  owner-queued brief (PLAN-rev1 4985989d…) delivered a LOCAL patch first:
  the probe repair (relative basenames, distinct retained descriptors,
  verified observable outcomes, honest failure categories, static-first
  short circuit) + the regression suite, through local A–F rounds — three
  C/E revise rounds culminating in the AC4 dir_fd-discriminator finding
  (ambient cleanup opens carry dir_fd; the probe's own do not) and the
  round-3 patch fingerprint 7ae0ef34…, SD-F ACCEPT (REVIEW-F-final.md
  9644764c…). This entry records the publication of that patch: the same
  two files (tools/behavioral_eval_runner/evidence.py +
  tools/behavioral_eval_runner/tests/test_evidence.py) now land as a
  reviewed pull request, with the unrun record's resolvers accepted by F
  (the 11 git-dependent tests resolve in CI where .git exists; the 8
  calibration skips need the pinned SDK host; the 4 Windows-only tests need
  a Windows host). Grants nothing new and carries no PR number here; the
  PR's own record is its body and SD-C comment. Counts UNCHANGED
  (SKILL-COUNT 205, FAMILY-COUNT 23). D91 and earlier entries are
  byte-untouched.

- **D93 (2026-10-11) — Q1 PR-body CI structural check (skills-documentation
  enforcement).** The owner-selected queue item: CI enforcement that every
  human/agent PR body carries the template's three bound fields. Delivered:
  `scripts/ci/check_pr_body_skills.py` (structural rules only — whole-line
  sentinel pairs for skills/security/witness; ≥1 four-cell skills data row
  or the no-matching-skill statement; a Row source record naming every
  published data row; bot authors dependabot[bot]/renovate[bot] exempt; no
  hash equality, no content grading), its six ORIGINAL subprocess-level
  fixture
  [count annotation, 2026-10-11 — the suite has grown through nine Codex-review
  revise rounds (rounds 1-10) to 34 tests; the six acceptance fixtures of the
  original delivery are cases (a)-(f), each rule's regression lives beside
  it, and the count above records the original six, not the current suite —
  corrected in place so the durable record does not preserve a stale count]
  tests, and ONE pull_request-only workflow step `pr-body-skills-check` in
  the existing validate-skills job immediately after the DCO step (no new
  job, no branch-protection change). The lane's own PR trips the
  protected-path guard by design; the body records the owner's standing
  blanket pre-approval (APR-100) with its verbatim quote and the
  CONTRIBUTING rule-3 exception route — the gate is not weakened. Counts
  UNCHANGED (SKILL-COUNT 205, FAMILY-COUNT 23). This entry records the
  lane; it grants no new execution, publication or merge authority. D92 and
  earlier entries are byte-untouched.

- **D94 (2026-10-11) — Q2 BER Stage B (model-driven eval) authorization
  record.** The owner selected Q2 with "start on all these" plus the
  standing blanket pre-approval (APR-100: "Pre-aproved all troubleshooting,
  commit, push, and mergs once local and GH chekcs are green. If not, take
  it in thand fry to fix it.") — both quoted verbatim. The lane adds NO
  repository code; this entry is the lane's only repo change. Boundaries
  recorded: ONE bounded run class — three synthetic Scenario-A-shaped
  prompts executed via the session harness's current model route (no new
  provider account, no credentials stored anywhere), on the named distro
  only (alias `aegis-ber-stage-a-wsl`, user `peternguyen`, scratch root
  `/home/peternguyen/aegis-stage-a` mode 700; the placed BER source
  refreshed to the Stage B base pin `26bfc772` by the credential-free
  archive method), a 60-minute ceiling, the runner's NON-LIVE construction
  respected — the live-dispatch gate's deterministic
  `LIVE_DISPATCH_DISABLED` denial is invoked and observed per prompt, never
  worked around — no deletion, no package installs, no network beyond the
  harness provider route. The honesty line every Stage B artifact carries:
  a capability observation ONLY — NOT a production isolation claim, NOT a
  BER baseline result. Stop conditions: harness route unreachable, a
  missing harness credential (never remedied by storing one), the bounded
  class exceeded, or any cap-dec L186–192 stop — a stop is a
  `NON_BASELINE` disposition, never a partial pass. No new APR is created
  (the register preamble L12–13 makes the owner's live instruction the
  grant and this entry its durable transcription); the disposition record
  and raw evidence stay in the lane's evidence tree and the distro's
  protected raw dir — nothing further is published to the repo by this
  lane. Counts UNCHANGED (SKILL-COUNT 205, FAMILY-COUNT 23). This entry
  records the authorization; it grants no new execution, publication or
  merge authority. D93 and earlier entries are byte-untouched.

- **D95 (2026-10-11) — Q3 register normalizations (annotations, never
  rewrites).** The owner selected Q3 — the long-standing normalization
  items. Delivered as FIVE append-only dated annotation blocks, one per
  item, with unique non-colliding IDs in the fixed order A1/A2/B1/C1/D1:
  ANNOT-Q3-001 (APR-121's alternate field labels), ANNOT-Q3-002 (APR-123's
  same labels + lowercase Recorded at / by), ANNOT-Q3-003 (the six entries'
  accepted `Scope allowed (selected policy):` form — APR-009, APR-105,
  APR-113, APR-118, APR-121, APR-123), ANNOT-Q3-004 (APR-127's
  SUPERSESSION event-type wording vs the preamble's four named types),
  ANNOT-Q3-005 (the APR-100 quote divergence: the canonical 2026-09-28
  instruction vs the newer owner blanket wording quoted in the merged
  PR #724 body and D94 — both texts verbatim, recorded not judged). Every
  annotation names its variant in plain words, quotes its binding source,
  and states the original entry text is unchanged; NO new APR IDs (the
  annotations grant nothing and are none of the four lifecycle-event
  types). The register's B..H diff is additions only (+N/−0). Counts
  UNCHANGED (SKILL-COUNT 205, FAMILY-COUNT 23). This entry records the
  lane; it grants no new execution, publication or merge authority. D94 and
  earlier entries are byte-untouched.

- **D96 (2026-10-11) — Q4 durable acceptance refs (pinned official-count
  reference).** The owner selected Q4. The durable record is an APPENDED
  "Official count reference (pinned)" section in
  `tools/readability_acceptance/README.md` (annotate-don't-rewrite;
  additions only): the pinned ref
  `408e4d6a2046b37afe7912e9c8643474df7ab037`, the six labeled numbers
  (reader pages 631 / accepted 50 / provably-pending 4 / no-recorded 564 /
  within-10 7 / cannot-decide 6 → **official pending count 581**), the
  formula, the exact re-derivation command, and the D96 provenance — framed
  as a durable citation point, NOT the live figure (the live figure remains
  `check_index.py` at the current ref; later rebuilds supersede it). The
  re-derivation proof: Stage C re-ran
  `check_index.py --ref 408e4d6a…` in a full clone at the implementation
  base and reproduced all six numbers byte-for-byte. Counts UNCHANGED
  (SKILL-COUNT 205, FAMILY-COUNT 23). This entry records the lane; it
  grants no new execution, publication or merge authority. D95 and earlier
  entries are byte-untouched.

- **D97 (2026-10-11) — Q5 issue #101 status reconciliation.** The owner
  selected Q5 ("start on all these"; APR-100 blanket applies). The
  reconciliation is a dated section appended under the plan doc's own
  "Dated product decisions" convention
  (`docs/roadmaps/aegis-setup-routing-plan.md`, additions only): packages
  1–3 delivered and unchanged (PRs #109/#124/#121); package 4 preparation
  delivered synthetic-only (PRs #271/#286/#281/#319/#329/#335 with
  APR-031/036/040 lifecycle — every fixture case NOT RUN); package 4 live
  evaluation NOT started (the issue's sentence quoted: "Live evaluations
  require explicit inputs, authority, and spending limits"); packages 5/6
  conditional, package 7 pending; no changed decisions; the four
  next-step decision pointers stated, never started; the BER live-dispatch
  gates intact (NON-LIVE, OD-1-gated, unchanged). The same dated section
  is appended to issue #101's body via the gh API AFTER this PR merges
  (the post-merge follow-through, with the byte-preservation proof:
  the original body is a verbatim prefix of the new body). The lane closes
  nothing and grants nothing. Counts UNCHANGED (SKILL-COUNT 205,
  FAMILY-COUNT 23). This entry records the lane; it grants no new
  execution, publication or merge authority. D96 and earlier entries are
  byte-untouched.

- **D98 (2026-10-11) — post-queue 1 readability ledger full-page re-read.**
  The owner's instruction: "go, do not stop until all to-dos are completed"
  (verbatim). The re-read covers the ledger's 8 chunks (its own section
  boundaries, L1–4581 at the reviewed revision `ab7182d8`; the plan anchor
  L4582 overshoots the true EOF by one line) and was performed by TWO
  independent **non-author full-content readers** — pq1-reader-a (chunks 1–4)
  and pq1-reader-b (chunks 5–8) — whose retained records carry a per-chunk
  disposition, a purpose/normal-use restatement and any named follow-up for
  every chunk; the round-1 single-reader deviation (pr-publisher as sole
  reviewer) is superseded. Dispositions: chunks 1, 2, 3, 5, 6 and 7 accepted;
  chunk 4 needs a named follow-up (2: the stale "open PR #633" citation at
  L3238–3243 and the "ten other SHAs" count at L3245–3248); chunk 8 needs a
  named follow-up (1: the stale L-001–L-006 evidence-source anchors at base
  L2574/L2575). Named follow-ups: those 3 plus the self-cost follow-up below.
  No dated snapshot rewritten (the diff is additions only). The official-count
  reconciliation now labels three figures: (a) HISTORICAL — the D96-pinned
  `check_index.py --ref 408e4d6a` in a full clone: reader pages 631 /
  accepted 50 / provably-pending 4 / no-recorded 564 / within-10 7 /
  cannot-decide 6 → **official pending count 581**, labeled historical and NOT
  the live figure (the tool README); (b) LIVE at the reviewed revision
  `ab7182d8` (`check_index.py --ref ab7182d8`, independently re-run in a
  detached worktree at that revision): 633 / 48 / 5 / 566 / 8 / 6 →
  **official pending count 585**; (c) LIVE at the candidate head (this
  entry's commit; `check_index.py --ref <the new head>`): 633 / 48 / 5 /
  566 / 8 / 6 → **585** — the exact head/tree and the verbatim JSON are
  recorded in the PR's Stage C round-2 record, because a commit cannot name
  its own SHA inside its own bytes. The ledger still publishes no count of its
  own and cites the index. SELF-COST: this entry's commit changes the ledger
  by +45/−0 against the base (+21 round 1, +24 round 2), so the ledger is
  provably pending at the new head (197 changed lines against its recorded
  acceptance `2c6b6fc6`, with a new section; it was already pending at the
  base with 152) — the page stays pending until a subsequent full-page
  re-read accepts the resulting head, and D98 accepts only the
  reviewed-revision content, not the new head's state. The tracker tool needs
  NO change. The dated "Full-page re-read — 2026-10-11 (D98)" section is
  appended in the ledger's Start-here area. Counts UNCHANGED (SKILL-COUNT
  205, FAMILY-COUNT 23). This entry records the lane; it grants no new
  execution, publication or merge authority. D97 and earlier entries are
  byte-untouched.

- **D99 (2026-10-11) — post-queue 2 documentation-batch ledger
  reconciliation.** The owner's instruction: "go, do not stop until all
  to-dos are completed" (verbatim). The dated "Documentation-batch
  reconciliation — 2026-10-11 (D99)" section is APPENDED at the end of the
  ledger's "Documentation batches" section: this lane's diff touches ONLY
  its own append range (that section's bytes and this entry), so D98's
  Start-here range — PQ1's PR #730, MERGED FIRST as the merge `279338a9` —
  and every dated entry above are byte-untouched. Round 1 appended the
  section at base `ab7182d8`; round 2 rebuilt its per-batch states after
  Codex P1 finding 4242876575, which was right: an acceptance row records an
  acceptance at a REVISION, not the page's current state. Re-derived with
  the checker: the eleven sweep batches hold **66 acceptance records over 61
  unique pages** (round 1 said 60 — it counted batches 7–11 as 6/4/1/1/1
  against the tables' actual 8/5/2/2/2 rows), and at the pinned `408e4d6a`
  those 61 pages are **50 accepted / 4 provably pending / 7 within-10-lines
  pending** — an accepted row does not make a page accepted (even the first
  batch is 6 accepted + 2 within-10). The official basis is labeled:
  (a) HISTORICAL — the D96-pinned `check_index.py --ref 408e4d6a` re-run in
  a full clone → 631/50/4/564/7/6 → **official pending count 581**,
  reproduced byte-for-byte and NOT the live figure; (b) LIVE at the
  candidate head (this entry's commit; `check_index.py --ref <the new
  head>`) → 633/48/5/566/8/6 → **585** — the exact head/tree and the
  verbatim JSON are recorded in the PR's Stage C round-2 record, because a
  commit cannot name its own SHA inside its own bytes. The dated batch rows
  are annotated at the batch level, never re-scored; the ledger itself stays
  provably pending at the new head (the self-cost paragraph states it, and
  the measured figure is in that PR record). Named follow-ups: none. Counts
  UNCHANGED (SKILL-COUNT 205, FAMILY-COUNT 23). This entry records the lane;
  it grants no new execution, publication or merge authority. D97 and
  earlier entries are byte-untouched.

- **D100 (2026-10-11) — SCIF PR-1 #729 close-out corrections record.** The
  owner's SCIF queue item (received ~17:00 PT) outcome (1): correct the
  #723/#729 close-out record forward. The dated record
  `docs/evidence/scif/scif-closeout-corrections-2026-10-11.md` is ADDED (new
  page), with the evidence index row and this entry as its only other
  touches; `docs/approvals/APPROVAL_REGISTER.md` is byte-untouched. The four
  correction blocks and their verdicts: (a) **MG3 at merge time for #729 —
  NOT MET AT MERGE TIME** — against the rule in force at `c4fbee1d`, neither
  branch existed for the merged head `f356157c`: exactly one review object
  (`5484238846`, `chatgpt-codex-connector[bot]`, 17:30:06Z) names the
  superseded head `8959fd260d`, and no comment carries a Codex result or an
  unavailability notice for `f356157c`; the recorded `MG3 EXACT-HEAD
  PRECEDENT` is cited as a record, never as a waiver, and the triage trail is
  recorded as real without creating satisfaction. (b) **the #729 gate-guard
  authority — NOT ESTABLISHED FROM ACCESSIBLE EVIDENCE** — APR-047's four
  eligible paths exclude #729's two changed files, its Scope FORBIDDEN makes
  such a PR ineligible as a whole, no register or reconciliation entry names
  #729, and APR-100's Scope FORBIDDEN does not waive a protected gate-guard;
  the only accessible authority record is the PR #729 body's verbatim owner
  instruction, whose provenance APR-100 ANNOT-Q3-005 records. (c)
  **HANDOFF-CORRECTION.md dated addenda** — `6104148527`, `6104196189` and
  `6104213124` belong to PR #721 (that lane's SD-D/SD-E/SD-F verdicts), the
  four correct #723 IDs are `6107054131`, `6107118947`, `6107142849` and
  `6107164055`, publisher identity (one account, `ModernNomad-98`) is not
  distinct agent identity, and the 36 (local module), 620 (CI
  tools-tests-linux at #723's head) and 1107 (#729 post-merge BER suite)
  counts are separated by scope. (d) The 36 merged PRs #694..#729 are a
  merge count, not an all-gates-audited claim. The verification base is
  `5a9adea0f2dce00c8ffe4be959ffb7e4a91ad566`; inputs `SCIF-recon.md`
  (above-footer `a3c8a53f…`) and `HANDOFF-CORRECTION.md` (whole-file
  `f508eb4c…`). The D-number was re-derived immediately before this append:
  D99 was the last recorded entry and no D100 existed. This entry records
  the corrections; it grants no new execution, publication or merge
  authority. D99 and earlier entries are byte-untouched.

- **D101 (2026-10-11) — SCIF PR-2 name record, the Stage A/B
  necessity-and-reuse check, and the fitted eval cases.** The SCIF package's
  outcomes (2) and (3). The naming decision as rendered (D1–D4): **Aegis SCIF —
  Secure Compartmented Integrity Framework**, short form **Aegis SCIF**, with
  the plain-language definition and the explanatory line recorded on the new
  page `docs/aegis-scif-naming-and-necessity.md`. The former name has **zero**
  occurrences in the tree and in reachable history (the greps and the
  `git log -S` searches are recorded on the page), so the record is **added,
  not applied to existing prose**; the P0 directive's supervisor wording is
  carried as an **alias** — the same workstream, transcribed in future
  documents under the new name — and the page adds exactly one quotation of the
  historical phrase, to define that alias. The residual-occurrence inventory at
  base `09a5d2b3`: (a) 0, (b) 0, (c) 113 technical identifiers, (d) 29
  unrelated uses, (e) the one deliberate alias quotation; every line is listed
  with file:line and a disposition. Outcome (3): ONE normative subsection added
  inside `## The seven stages` of `docs/delivery-workflow.md` — *Necessity and
  reuse: the five questions owed at Stage A and tested at Stage B* — plus
  pointer-shaped edits to the stage-table rows A/B, the `SD-A`/`SD-B`
  disposition rows and the existing `SD-A`→`SD-B` / `SD-B`→`SD-C` dependency
  rows (no rows added, no new numbered collapse site, site 8
  unchanged-and-verified). The check adds the five questions (necessity /
  reuse / ownership / minimum-safe action / complexity justification), the
  routing dispositions (cite / preserve / smallest change / bounded check), the
  six reuse tests and the never-transfers list, and it adds no new field, gate,
  report or register (D6/D7). The fitted eval assets are five new cases across
  three existing `evals.json` files (`risk-tiered-validation-selector` +2,
  `ai-task-decomposer` +2, `acceptance-criteria-reviewer` +1); no `SKILL.md`
  is edited. The evidence record
  `docs/evidence/scif/scif-eval-assets-and-pilot-census-2026-10-11.md` keeps
  assets, static, deterministic, actual-runs and unrun separate, reports
  scenario #10 as UNRUN, and records the bounded pilot: the read-only offline
  `census` at the pinned base (exit 0, `behavior_cases` 1329,
  `behavior_eval_files` 205) with the candidate-head census's measured delta
  (`behavior_cases` 1334, +5; the three skills 8 / 10 / 9; the head commit and
  tree in the PR's Stage C record, because a commit cannot name its own SHA
  inside its own bytes). Counts UNCHANGED (SKILL-COUNT 205, FAMILY-COUNT 23).
  This entry records the lane; it grants no new execution, publication, review
  or merge authority; the approval register is byte-untouched. D100 and earlier
  entries are byte-untouched.

- **D102 (2026-10-12) — documentation-currency refresh: the two live cutoffs
  advanced, the index routes repaired, and the SCIF page's closing sentence
  corrected forward.** A repository-wide currency change in the
  DOCUMENTATION-CURRENCY REFRESH lane, planned at `DOCS-REFRESH-PLAN-rev3.md`
  (above-Foot prefix sha256 `c779dd18…` over 82,167 bytes) and audited **SD-B
  ACCEPT** (`DOCS-REFRESH-AUDIT-B-rev3.md`, Foot sha256 `329d2fda…`). Fifteen
  files change, docs-only, one commit. `README.md`: the `## CI (merge gate)`
  `validate-skills` row now names the Markdown link-checker corpus step and the
  pull-request body bound-field check; the "What is included" table adds the
  setup-routing and readability-acceptance tools; the delivery-control row adds
  `ci-durations` (#740) and `fast-save` (#741). `docs/README.md`: the evidence
  guide's count 15 → **16**, seven new routing entries, and the feature-flag
  entry notes the delivered banner. `docs/roadmaps/aegis-backlog-forecast.md`
  and `docs/roadmaps/aegis-execution-metrics.md`: the newest reading and
  measurement advance to **M2 = `7fbc2335ee4494ecb8ae6aaea0fe6ecdc297d9f2`,
  assessed through PR #741**, with the #688 and #685 banners kept verbatim.
  `docs/offline-ci.md`: the `validate-skills` coverage cell. Dated forward
  notes on `docs/roadmaps/p0b-fast-save-directive-2026-10-11.md` (**B2 landed
  through its own PR #741, not by that record**; B3 still unscoped),
  `docs/design/fast-save-handoff-protocol-v1.md`,
  `docs/roadmaps/aegis-coordinator-figures.md`,
  `docs/roadmaps/resumable-control-plane-backlog.md`,
  `docs/roadmaps/behavioral-eval-runner-backlog.md`,
  `docs/roadmaps/aegis-ci-baseline-2026-10-11.md`,
  `docs/roadmaps/skill-eval-harness-authorization-request.md` and
  `docs/roadmaps/aegis-open-decisions-2026-09-23.md`; and the SCIF page's
  part-4 closing sentence corrected forward (already **3** old-name lines at its
  own PR #739 head `4d5ccb0b`; **187 / 45 files / 118 / 3 / 16** at both
  `4d5ccb0b` and `7fbc2335`). No historical or evidence file is rewritten:
  every edit is an insertion or a live current-state correction, and D1–D101 are
  byte-untouched. Source: the owner's direct instruction of 2026-10-12 to bring
  all documents, context maps and README files up to date. This entry records
  the lane; **it grants no new execution, publication, review or merge
  authority**; the approval register is byte-untouched.

- **D103 (2026-10-12) — the review-path decision: the broad review-round cap is
  rejected, and a lighter documented review path is adopted for pure-docs pull
  requests only.** The authorizing act is the owner's direct chat message of
  2026-10-12, quoted as relayed: "GO WITH YOUR RECOMMENDATION". By that message
  the owner adopted the recommendation in the coordinator's 2026-10-12
  review-path check-in packet — "REJECT B; adopt C … Revisit in 30 days with the
  next round-cost sample" (the coordinator's wording, not the owner's) — whose
  selected option is the packet's Option C, "NARROW lighter path - cap only
  pure-docs PRs (zero code diff, tier docs-only)". The owner's own words are the
  short message; the option and recommendation wording is the coordinator's. The
  normative rule is ADDED as one new section,
  `## The lighter review path: pure-docs pull requests only`, in
  `docs/delivery-workflow.md` between its `MG` block and its
  `## Pre-authored diffs` section (at base `9c4eb595`: after line 389, before
  line 391). It is scoped exactly to a pull request whose diff is documentation
  only — zero code diff, and the tier `docs-only` from
  `change-classification-gate`. One divergence from the packet is recorded
  deliberately: the packet's "Authorization effect" line says approving C
  permits a lighter path "without mandated repair-re-audit cycles for findings
  that a follow-up docs PR can carry", and the recorded rule declines that
  permission and keeps repair-and-re-audit mandatory for pure-docs pull
  requests. What the section does and does not do is stated there once; this
  entry records the decision and does not restate the rule. The dated row for
  the decision is ADDED as a `### Decided on 2026-10-12` section of
  `docs/roadmaps/aegis-open-decisions-2026-09-23.md`, placed with the page's
  other decided sections, and the open row it replaces (added 2026-10-07, line
  235 at the base) is kept in place with a DECIDED state, a pointer to that
  section, and a dated citation correction. The correction was re-derived at the
  base: the cited commit `4d05c624` exists, resolves
  `.coord/coordinator-cadence.jsonl` (89 lines), and its line 72 IS the tabled
  two-tier proposal the owner declined on 2026-10-04; it is reachable only from
  `origin/coord/idle-check-2026-10-04` and is not an ancestor of `main`
  (`git merge-base --is-ancestor 4d05c624 origin/main` → exit 1). The cited
  **path** is a different matter and is also on `main`: the `main` copy of
  `.coord/coordinator-cadence.jsonl` is 25 lines and contains no such record
  (last written on `main` by `74ee97b0`, 2026-10-03). The coordinator's reported
  2026-10-12 finding that the citation "does not resolve to the tabled proposal"
  was NOT reproduced in this lane; the coordinator's own packet now carries a
  dated correction withdrawing it and attributing the failed check to the wrong
  ref/line, and this entry records that as reported rather than measured. That
  branch has since advanced to `d0a0847c` (2026-10-11), whose line 90 closes the
  check-in and parks the lighter question with the paused readability program;
  the decision recorded here supersedes that parked state for pure-docs pull
  requests only. The rule changes no gate: a pure-docs pull request keeps
  Stages A–G, the stage separation rule, the exact-head invalidation rule,
  `MG1`–`MG5` intact, `APR-100`'s standing pre-approval on its own terms, and
  the auto-merge rules — the lighter path removes no required check, downgrades
  no tier, and widens no scope to make a pass. The revisit date is 2026-11-11
  (30 days), which is separate from this page's own review date of 2026-11-03 in
  `docs/delivery-workflow.md`; the earlier of the two is the page's review, and
  neither date changes the other. The register's two statements that AEGIS-APR-113
  does not decide this review path — its item 8 and its "Not decided by this
  entry" sub-item (3), both on the default branch — are RECORDED HERE, not
  edited: entries are immutable and are corrected by appending a later lifecycle
  event, which is this change's companion register note (see below). This entry
  records the lane; it grants no new execution, publication, review or merge
  authority. Counts UNCHANGED (SKILL-COUNT 205, FAMILY-COUNT 23). D102 and
  earlier entries are byte-untouched.
- **D104 (2026-10-12) — BER host ladder Stage C: the ceiling fix, the Stage A
  disposition, the APR-128 consumption event and the Stage B stop.** The
  owner's instruction, quoted as relayed (the H row,
  `ber-wp2b3-owner-decision-chain.md` L62): "Fix the Stage A host-phase time
  ceiling and disposition Stage A; confirm or stop Stage B"; and the owner's
  acceptance of the probe-is-consumed finding (the 2026-10-12 owner decision
  log, item 8): "records-only lane: ceiling fix as a named §13 log entry,
  Stage A disposition, Stage B stop, APR-128 CONSUMED event". Three paths are
  touched, all additions, in ONE DCO-signed commit:
  `docs/roadmaps/behavioral-eval-runner-backlog.md` gains THREE named entries
  appended at the end of `## 13. Append-only governance log`, after
  BER-DEC-016's last line and before the `## 14` heading — the time-ceiling
  correction, which records **60 minutes** at the point of definition
  (BER-DEC-016's "Time ceiling" bullet, L4026–L4030, states only the rule for
  producing a value); the Stage A host-phase disposition, which records that
  the probe RAN and the grant's one use is CONSUMED; and the owner's stop of
  Stage B. `docs/approvals/APPROVAL_REGISTER.md` gains ONE appended lifecycle
  event, **AEGIS-APR-130** (`CONSUMED; target grant AEGIS-APR-128`, New
  authority: None), because the register still showed APR-128 as unspent
  although its single use was spent. Nothing is edited or deleted:
  BER-DEC-016's block (L3974–L4048) and APR-128's entry are byte-untouched,
  and every backlog change is a new entry appended under §13's own rule
  (L2672–L2675). The Stage A receipts and the pinned source archives live
  outside Git, so the archive hashes are recorded **by reference and by hash**
  and are **not verifiable from a clone** — the publication gap the receipts
  themselves state; publication of the sanitized
  `stage-a-capability-summary/v1` stays an owner decision and was deferred.
  SELF-COST: this entry's commit changes three files by +142/−0 against the
  base (this page +34, the ladder backlog named above +74, and the approval
  register +34), so nothing it adds is a code path, a check or a counted
  artifact, and no acceptance record's review state changes. Counts UNCHANGED
  (SKILL-COUNT 205, FAMILY-COUNT 23). This entry records the lane; it grants
  no new execution, publication or merge authority. D103 and earlier entries
  are byte-untouched.
- **D105 (2026-10-12) — the CP-1 grant record: AEGIS-APR-131 records the owner's bounded
  read-only DynamoDB-first inspection grant.** The authorising act is the owner's dated relay
  **"A"** of 2026-10-12, relayed by the coordinating agent and quoted as relayed: "approving the
  bounded read-only DynamoDB-first inspection", with "[grant] as drafted" the coordinator's gloss
  on that approval and not part of the relayed words — the draft being
  `1351ba260c410f1151df5e598b54f2ccdf6f8993429b8cd5826be6217b5cc5b0`. The four inputs the draft
  left open are resolved and recorded in the register entry, not restated here: authorising words
  = the dated relay "A"; calendar expiry = **none stated** (one use is its own expiry); spend
  ceiling = **USD $0 external**; billing-surface reads = **OUT OF SCOPE**. The register append is
  append-only — no prior entry's bytes change — and carries the exact limits: one account, one
  Region, one table, one strongly consistent verification read path, the named custody and
  configuration reads, read-shaped negative tests only, one sanitized evidence record, 4–8 active
  hours, USD $0 external spend, and the six stop conditions with no discretion and no retry. The
  source identifiers (account, Region, table, incarnation pin), the principals and credential
  custody, the evidence root and retention, and the billing-contract facts are **unselected** and
  are recorded as unselected; the next gate is the owner's AWS credential and identifier
  selection, and **the inspection itself is NOT RUN by this change and is not startable until
  that selection is recorded**. AEGIS-APR-006 is not reused, extended or re-scoped. This entry
  records the lane; it grants no new execution, publication, review or merge authority. D104 and
  earlier entries are byte-untouched.
- **D106 (2026-10-20) — UX/UI open-workflow guided path.** Owner need (2026-10-19): design, build and extend web UI consistently through any chosen workflow, tool, agent or public repository. Demonstrated gap at 9ab6aeac: no guided path sequences the installed UI owners from the user's starting point; no installed skill authors screen structure/visual direction (recorded, not filled). Change (six planned deliverables / seven planned paths / eight touched files, B1): docs/paths/design-and-build-ui.md (deliverable 1); README picker bullet (deliverable 2); project-orchestrator Stage 6 pointer appended to the existing line, 0 added lines (deliverable 3); one should_not_trigger eval case (deliverable 4); evidence page plus docs/evidence/README.md index-row/truthfulness edits — counts 18→19, “Exactly three” → “Exactly four”, fourth-row sentence (deliverable 5); and tools/skills-manifest.json refresh as the authorized **seventh planned path**, required by validator D91, machine-generated consistency only, +2/−2 lines: source_revision bd5d2ff52f063b8854b39e4f216ddbf8aff60530 → a4fecf1aad68bbea62f724cc94e596dcf95f652f, project-orchestrator sha256 487ce822b14ae48b60714cf3abba54e8303a41839a5849ec584cb234d700dd86 → d3ad40ab4f232a54d57f9c43cc2c9027f15279b73320a9519f05f896be7b2bb0; no skill/count/family/catalog change; plan B3 “manifest untouched” superseded for this PR only. Classification: ai-agentic (governing). Baseline proposal sha256 bab99de8d502e2fb008be1e03c0748be48bc72a7724a9e7a6bb83e8c83acb862; plan sha256 b20818316c9b7db7f2c1856c2ace1bfe9a65a20d2f240098e4e1d78f629945ac; review sha256 a93178949164b1c5c5d45a6e0784410e96e55030a94466de2a44768b0e7f0191.
- **D107 (2026-10-21) — coverage triage decision (owner Q1=A/Q2=A/Q3=yes).** Owner decisions: **Q1=A** — `review_pending` counts every non-explicit-id row that still awaits planning-gate confirmation; **Q2=A** — row #254 is COVERED/catalog-decision covering `data-migration-runbook-author` (D71, 2026-09-28; catalog L630-631/L1447-1448; reconciliation R303/R3650-R3652) and row #278 is COVERED/catalog-decision covered by the `ai-sdlc-operating-model` stage map (catalog L1362-1364; reconciliation R3506-R3508); **Q3=yes** — this one append-only D-record. Derivation: the current map has 172 non-explicit-id rows (catalog-decision 14 + capability-review 103 + none 55); the two resolved rows #254/#278 leave the planning-gate pending set, so **review_pending = 172 - 2 = 170** (after reclassification: catalog-decision 16 - 2 resolved = 14 + capability-review 102 + none 54). Row #254's covering set drops `rollback-runbook-author`, but rows 23/242/243 still cover that skill, so the covering union after #254 is unchanged at **124**; row #278 then adds the three previously non-covering enforcers and raises the union **124→127**, so beyond-roadmap moves **83→80** (pinned by the #254-union test assertion). Row #278's source-faithful covering set is **18 names** — `ai-sdlc-operating-model` plus 17 stage-gate-map enforcing skills: `agent-startup-context-gate`, `source-of-truth-reconciler`, `change-classification-gate`, `ai-task-decomposer`, `human-approval-boundary`, `agent-authorization-matrix`, `reviewable-diff-discipline`, `docs-first-implementer`, `tdd-engineer`, `local-ci-mirror-preflight`, `code-reviewer`, `security-pr-reviewer`, `ai-closeout-reporter`, `agent-memory-governance`, `agent-governance-audit`, `agent-failure-recovery`, `agent-instruction-consolidator`; the three enforcers not previously in the covering union (`docs-first-implementer`, `tdd-engineer`, `local-ci-mirror-preflight`) raise **distinct covering 124→127**, so **beyond-roadmap 83→80** and the optionality phrase becomes **"80 of 207"**. Totals before→after: COVERED 54→56, PARTIAL 63→62, GAP 55→54 (SHIPPED 128 unchanged); grades catalog-decision 14→16, capability-review 103→102, none 55→54 (explicit-id 128 unchanged); gap priority P1 35→34 (P0 11 and P2 9 unchanged); **GAP ids 55→54** (row 278 removed; the 11 P0 GAP ids are unchanged); area 07 COVERED 1→2 / PARTIAL 4→3; area 08 COVERED 2→3 / GAP 1→0; entries 300, manifest 207, priority 126/149/25 unchanged; `review_pending` 160→170. Exactly six files change (the five triage files plus the owner-recorded AEGIS-APR-140 pure-append entry in `docs/approvals/APPROVAL_REGISTER.md`): `scripts/validate-skills.py` (planning-gate resolved set, totals, GAP ids, phrase, formula, docstring), `scripts/tests/test_validator.py` (totals/GAP/review-pending fixtures plus row-level, formula and phrase tests; the per-area summary rows are re-derived and validated by the existing summary-row check), `docs/skills/coverage-map.json` (rows #254/#278, totals, phrase), `docs/skills/coverage-map.md` (totals, per-area, GAP list, phrase) this record and the `docs/approvals/APPROVAL_REGISTER.md` append; no `.github`, catalog, README or manifest edit, and no new execution authority is granted beyond the recorded merge exception; the register append records the owner's standing gate-guard exception **AEGIS-APR-140** for `scripts/`-only protected paths, permitting an administrator merge only when conditions (a)-(f) hold at the exact head and never bypassing any other condition. Evidence: PLAN.md sha256 `fa8efcc6d41e6fc05da405a90b649d1f71aefae4a5870e8fd2ea018623209bd3` (13,329 B), AUDIT-B-R2 sha256 `2ce4b2f7b756ce088646a203877d01569a9b8f4a2c3acf6a5c28aec711f49c1b` (4,656 B), A-rows sha256 `31b1bf2ad9282fda8128a1850578c22f991961cc29058b4f2fd3c84c337aaf57` (1,007 B). This entry is append-only; D106 and earlier entries are byte-untouched; if a later follow-up PR lands a D107 before this PR rebases, stop and coordinate rather than renumber silently.
- **D108 (2026-10-21) — Batch 1 P0 gap closures (owner pre-approved).** Owner pre-approval covered this batch under the standing conditional merge conditions; governance basis: the scripts/-only protected changes qualify under the owner-recorded **AEGIS-APR-140** standing gate-guard exception in `docs/approvals/APPROVAL_REGISTER.md` (first use PR #878), and Stage F/G must cite that register entry/standing route explicitly; this entry records the eight deliveries rebased onto main `a568333f3f23071f1197518113b9c00505f2a026` (which already carries #877 hardening plus #878 triage/APR-140). Delivered: **#6** `layered-architecture-enforcer` (family 3, area 01), **#7** `dependency-direction-guard` (family 3, area 01), **#8** `interface-first-designer` (family 3, area 01), **#49** `data-flow-diagrammer` (family 3, area 01), **#125** `security-regression-harness-designer` (family 5, area 03), **#127** `security-impact-note-author` (family 5, area 03), **#155** `concurrency-race-reviewer` (family 3, area 04), **#188** `production-safe-smoke-tester` (family 6, area 06) — each with SKILL.md, trigger-oriented description (<1,024 parsed chars), reference file, behaviour evals (6 cases; #49 has 5) and a 22-case trigger-eval file (8 positive / 14 negative; data-flow-diagrammer is 23 after its added PII-lifecycle negative case). Registration: manifest D91 refreshed **207→215**; **`source_revision` is truthful provenance — it names the content commit that contains all 215 manifest paths and hashes (the content commit immediately before the manifest-provenance commit), not the rebase base; a validator self-test verifies every manifest path exists at the declared source_revision AND its CRLF-normalized sha256 matches the manifest**, so the manifest is verifiable rather than a documented limitation. README SKILL-COUNT **207→215**, FAMILY-COUNT **23 unchanged**, family counts **family 3 12→17 / family 5 9→11 / family 6 24→25** (roster sum 214 + one beginner-facing orchestrator, not counted in a family, = 215); catalog rows added to Phase 2 (5), Phase 4 (2) and Phase 5 (1); no `.github`, catalog-narrative, README-manifest-count or manifest-schema unrelated edits. Coverage map: the eight rows move **GAP/none → SHIPPED/explicit-id** (#6, #7, #8, #49, #125, #127, #155, #188) with the new covering skills and catalog evidence referencing D108; totals before→after on this base: SHIPPED **128→136**, COVERED 56 unchanged, PARTIAL 62 unchanged, GAP **54→46**; grades explicit-id **128→136**, catalog-decision 16 unchanged, capability-review 102 unchanged, none **54→46**; priority 126/149/25 unchanged; gap priority **P0 11→3 / P1 34 unchanged / P2 9 unchanged** (remaining P0 gaps: #161, #162, #164); GAP ids **54→46**; manifest **207→215**; distinct covering **127→135** (the eight new skills, none previously in the union); beyond-roadmap **80 unchanged**; optionality phrase **"80 of 207" → "80 of 215"**; `review_pending` **170→162** under the current planning-gate-resolved semantics (172 non-explicit rows − 2 planning-gate-resolved #254/#278 − 8 newly explicit Batch 1 rows; do not re-mix the pre-triage formula). Per-area status on this base: area 01 SHIPPED **11→15** / GAP **22→18**; area 03 SHIPPED **22→24** / GAP **4→2**; area 04 SHIPPED **3→4** / GAP **6→5**; area 06 SHIPPED **36→37** / GAP **6→5**; area 07 (19/2/3/1) and area 08 (17/3/0/0) are unchanged from the triage merge; entries and other areas unchanged. Validator: COVERAGE_TOTALS, COVERAGE_GAP_IDS, COVERAGE_P0_GAP_IDS and COVERAGE_REQUIRED_PHRASES updated; tests fixtures updated and a Batch 1 delivery regression added; full suite green (248 baseline assertions preserved plus the Batch 1 regressions). Exactly these files change: the eight new `.claude/skills/<name>/` directories, `docs/skills-catalog.md`, `README.md`, `tools/skills-manifest.json`, `docs/skills/coverage-map.json`, `docs/skills/coverage-map.md`, `scripts/validate-skills.py`, `scripts/tests/test_validator.py` and this record; no `.github` change; `scripts/` is protected so the gate-guard refusal applies by design and the owner-conditional merge route is used only at Stage G. Evidence: PLAN.md sha256 `a44b0b3a5c839effcb7259d9882f9f5e27caed9f593dda28706c61e4fded76d0` (15,354 B), AUDIT-B-R2 sha256 `36e5c6216530f67fc9cca4bd8e81df589015bb9d52d02bf864575dc2d9146d60` (5,243 B), A-rows sha256 `a7d99ccf93da09687b64175cefda3547910d80065666550a85011d523cfdffc2` (913 B). Append-only: D107 and earlier entries are byte-untouched; D107 already records the triage decision (this rebase is D108, not a renumber of the old branch's planned D107).
- **D109 (2026-10-21) — Batch 2 SaaS lifecycle skills (seven family-4 deliveries).** Owner pre-approval covered this batch under the standing batch conditions (Batch 1 then Batch 2, strictly sequential; one seven-skill PR). Basis live main `9c05d2954b605fd2c08bcfb6299aa2a20fb18e0e` (Batch 1 PR #879 merge; tree a9188553). Delivered: **#61** `subscription-lifecycle-designer`, **#67** `user-preference-architect`, **#76** `export-pipeline-architect`, **#80** `demo-tenant-safety-designer`, **#83** `saas-offboarding-architect`, **#86** `saas-localization-architect`, **#87** `saas-timezone-architect` (family 4, area 02) — each with SKILL.md, a trigger-oriented description (<1,024 parsed chars), one reference file, six behaviour cases and a 22-case trigger-eval file (8 positive / 14 negative), auto-invocable advisory/design-only, no mandatory scripts. Coverage before->after: SHIPPED 136->143, COVERED 56, PARTIAL 62, GAP 46->39; grades explicit-id 136->143 / catalog-decision 16 / capability-review 102 / none 46->39; priority 126/149/25 unchanged; gap priority P0 3 / P1 34->29 / P2 9->7; GAP ids 46->39 (P0 161/162/164 unchanged); manifest 215->222; distinct covering 135->142; beyond-roadmap 80; phrase "80 of 215"->"80 of 222"; review_pending 162->155 (157 non-explicit rows - 2 planning-gate-resolved #254/#278); area 02 entries 35 -> SHIPPED 14->21 / COVERED 4 / PARTIAL 10 / GAP 7->0; other areas unchanged. README SKILL-COUNT 215->222 and roster family 4 12->19 (roster 221 + one orchestrator = 222; FAMILY-COUNT 23 unchanged); catalog adds seven Implemented Phase 3 rows and the fifth overlap cluster; validator COVERAGE_TOTALS / GAP ids / required phrase updated; tests add T37 Batch-2 delivery regression (T36 length 215->222, provenance checks unchanged); manifest D91 215->222 with truthful `source_revision` = the Batch 2 content commit C (manifest-only provenance commit P immediately after it; T36 verifies 222/222 paths at C in CI mode). Scope: **36 files** (7 new skill dirs x 4 + eight shared registration/coverage/validator/test/reconciliation files); protected paths only `scripts/validate-skills.py` and `scripts/tests/test_validator.py`; no `.github` change; AEGIS-APR-140 rule-1 route applies at Stage G (gate-guard refusal is never a pass; the Stage G receipt records the disclosed admin merge and skipped jobs as never-a-pass). Evidence: PLAN-REV2 `da31b44453f1b8f39d74d8a36d33f69d9f4f1fdc67b7a1f32c8c559ebb8dad74` (15,253 B/57 LF), A-rows `c0ff89ae9b231bc645a0250281fa20c19354da0b5a44ccbd422f386ddcfebda8` (1,315 B/4 LF), independent AUDIT-B-R2 `b0468a656afeb6648cbfa89f6141992c2591921219eb1f863a481027743fc117` (24,124 B/99 LF) ACCEPT; D/E/F/G records follow. D1-D108 are untouched; this record is append-only (+1/-0 vs base).
- **D110 (2026-10-21) — Batch 3 frontend architecture & client-state skills (eight area-05 deliveries).** Owner directed the Lead to start another batch (scope delegated to the Lead under the standing batching rule; disclosed in the plan); this batch closes the eight remaining area-05 frontend GAPs, including all three remaining repo-wide P0 gaps. Basis live main `ce56a754e54b66b4e5276ef96b9ea284b259c432` (Batch 2 PR #880 merge; tree c799bb95). Delivered: **#161** `frontend-architecture-mapper`, **#162** `component-boundary-designer`, **#163** `design-system-token-governor`, **#164** `route-protection-designer`, **#167** `server-state-architect`, **#168** `client-state-boundary-reviewer`, **#169** `url-state-architect`, **#176** `pwa-boundary-reviewer` (family 14, area 05) — each with SKILL.md (nine canonical sections, description <1,024 parsed chars), one reference file, six behaviour cases and a 22-case trigger-eval file (8 positive / 14 negative; real pre-Batch-3 owners plus the batch-internal sibling seams exercised in their trigger-evals, where a Stop-Condition seam (reciprocal SKILL.md routing) and a trigger-eval-pinned seam (a discrimination case) are recorded separately and may be one-way; the server-state <-> client-state seam is a reciprocal Stop-Conditions pair with no trigger-eval case (accepted SD-D residual), and no server-state <-> url-state seam is claimed), auto-invocable advisory design/review-only, no mandatory scripts. Coverage before->after: SHIPPED 143->151, COVERED 56, PARTIAL 62, GAP 39->31; grades explicit-id 143->151 / catalog-decision 16 / capability-review 102 / none 39->31; priority 126/149/25 unchanged; gap priority P0 3->0 / P1 29->25 / P2 7->6; GAP ids 39->31 (P0 set now EMPTY); manifest 222->230; distinct covering 142->150; beyond-roadmap 80; phrase "80 of 222"->"80 of 230"; review_pending 155->147 (149 non-explicit rows - 2 planning-gate-resolved #254/#278); area 05 entries 20 -> SHIPPED 3->11 / COVERED 5 / PARTIAL 4 / GAP 8->0; other areas unchanged. README SKILL-COUNT 222->230 and roster family 14 16->24 (roster 229 + one orchestrator = 230; FAMILY-COUNT 23 unchanged), plus eight shipped D12.2 rows; catalog D12.2 intro now reads 13-skill and adds eight rows and the Batch-3 seam paragraph; validator COVERAGE_TOTALS / GAP ids / empty-P0 pin / required phrase updated; tests add T38 Batch-3 delivery regression (dependent NB-1 fixtures updated: T9b/T12/T13/T32/T33/T35/T36/T37; the pre-Batch-1 "80 of 215"/"83 of 215" rejections stay); manifest D91 222->230 with truthful `source_revision` = the Batch 3 content commit C (manifest-only provenance commit P immediately after it; T36 verifies 230/230 paths at C in CI mode). Scope: **40 files** (8 new skill dirs x 4 + eight shared registration/coverage/validator/test/reconciliation files); protected paths only `scripts/validate-skills.py` and `scripts/tests/test_validator.py`; no `.github` change; AEGIS-APR-140 rule-1 route applies at Stage G (gate-guard refusal never a pass; the receipt records the disclosed admin merge and skipped jobs as never-a-pass). Evidence: PLAN `a55d88cd17ca4c8be50e65be16349e5695546b9174d040518609a5f0327d3044` (15,253 B/53 LF), A-rows `db62deb0a7948dc2139ad9a23612e55f1cfc233aed15f3ad7f33a3b61c45e049` (1,378 B/4 LF), independent AUDIT-B `2f7a4cf515c2b2ba0f3e4539bbd654811de854ebb41a8f5a925075bb675b6ab8` (26,221 B/122 LF) ACCEPT; D/E/F/G records follow. D1-D109 are untouched; this record is append-only (+1/-0 vs base).
- **D111 (2026-10-21) — Step 0 repair &amp; reconcile on the frontend base (PRs #882/#883).** Owner-accepted Step 0 wave: PR-S0-1 (#882, merge `c4bf0fe4`) repaired routing and conventions; PR-S0-2 (this change) applies the coverage hygiene, overlap discrimination, audit-register addition and this record. **R1-R3 repairs:** live-incident routing now reports to the human incident owner (the runbook skill authors procedures only; diagnosis routes to `systematic-debugger`), product approval workflows route to `ai-human-in-the-loop-designer` while `human-approval-boundary` keeps the coding agent's own steps, and live adversarial probing routes to the manual-only `ai-evaluation-harness` with the strict explicit-invocation prefix (three R3 fixtures retargeted; one dependent contract-test expectation updated from 4 to 1 `(subagent)` expectations and disclosed). **0-C convention:** reconciliation section 4.1 now names the append-only reconciliation D-entry as the per-batch changelog, and `CHANGELOG.md` points readers to the D-entries (D108 onward). **0-B coverage hygiene (this record turns the map):** #151 Data Export Backend Design -> COVERED/capability-review covering `export-pipeline-architect`; #231 Timezone QA Strategy -> PARTIAL covering `saas-timezone-architect`; #31 Adapter Pattern Application -> PARTIAL covering `interface-first-designer`; #39 Concurrency Control Design -> PARTIAL covering `concurrency-race-reviewer`; #44 Decision Reversal Planning -> PARTIAL covering `adr-writer` (all capability-review, rationale null, notes `0-B re-triage (D111)`). **Coverage before -> after:** 151/56/62/31 -> **151/57/66/26**; grades 151/16/102/31 -> **151/16/107/26** (the plan-decided alternative #151 catalog-decision would be 151/17/106/26 - not used); priority 126/149/25 unchanged; gap priority 0/25/6 -> **0/21/5** with the P0 key retained at 0 for schema stability (schema_version 1); GAP ids 31 -> **26** (removed 31/39/44/151/231); area 01 55=15/8/17/15, area 04 30=4/12/10/4, area 06 55=37/6/8/4; distinct covering 150, beyond-roadmap 80 and review_pending 147 unchanged; the optionality phrase stays **"80 of 230"**. **0-D overlap:** bounded discrimination cases added to `interface-first-designer` (-> command-gateway-architect), `security-regression-harness-designer` (-> appsec-implementer) and `saas-offboarding-architect` (-> authority-invalidation-architect); `data-flow-diagrammer` already covered both neighbours; no new skills. **Audit registers (owner-accepted default 6):** added `docs/audits/Aegis-Audit-Register-2026-10-20.json` (5,125,392 B, sha b222ad60...) and `docs/audits/Aegis-Coverage-Register-2026-10-20.md` (399,618 B, sha bd3b6e96...) as byte-identical copies, plus `docs/audits/README.md` provenance/limits index and a docs/README pointer; repository delta +5,526,482 B (5,125,392 + 399,618 + 1,472 B README; ~29-31% depending on the size metric) is disclosed, and the coverage register has 0 relative links. **Renamed Batch-1 skills disclosed for D111 closure:** `architecture-enforcement-guard` shipped as **`layered-architecture-enforcer`**; `production-smoke-test-designer` shipped as **`production-safe-smoke-tester`** (owner plan section 4.2). **Planning-gate confirmation policy (Lead plan decision under owner-plan section 6.7 item 7 recommendation):** per-area planning-gate confirmation is recorded as a proposal in this Step 0 wave, not implemented; `review_pending` policy stays D107 Q1=A (rows #254/#278 resolved, remaining non-explicit-id rows counted). **Gates:** validator OK 230/0; self-tests 65 tests normal and CI mode; contract-audit 70; links 811 pages 0 broken/0 dead; DCO signed; T36 230/230 at source_revision `1291b93b` (SKILL.md bytes changed only for the saas-offboarding-architect boundary inventory correction; manifest content+provenance pair refreshed, T36 230/230 at the new content commit); protected `scripts/` paths changed by design under the rule-1 AEGIS-APR-140 route (gate-guard red by design). **Post-D3/E3 corrections:** the new appsec-implementer 0-D case now carries the MANUAL-ONLY strict prefix, the canonical row names are used for #31/#39/#44, the schema_version-1 P0-key shape is restored in coverage totals/validator/tests, and the offboarding boundary inventory now names the authority-invalidation route. D1-D110 are untouched; this record is append-only (+1/-0 vs base).
- **D112 (2026-10-21) — Batch 4 architecture &amp; backend depth (13 merged owner scopes, family 3).** Owner plan section 6.3 accepted merged scopes; 13 new family-3 skills delivered: `state-machine-modeler`, `transaction-scope-designer`, `cqrs-read-model-designer`, `configuration-architect`, `extensibility-boundary-designer`, `application-layer-pattern-advisor`, `technical-debt-classifier`, `modernization-cutover-planner`, `architecture-fitness-function-designer`, `architecture-spike-planner`, `graphql-boundary-reviewer`, `outbound-integration-adapter-designer`, `edge-function-designer`. Each ships nine canonical SKILL.md sections, one reference, six behaviour cases and a 22-case trigger-eval file (8 positive / 14 negative) naming real manifest owners with MANUAL-ONLY strict prefixes (reciprocal/seam-handoff cases raise four skills above the 22-case convention - 23/24/25 cases with 8 positive and 15/16/17 negative as recorded in each SKILL Supporting Files - disclosed); auto-invocable advisory/design-only, no scripts. **Coverage before -> after:** 230 skills, 151/57/66/26 -> **243 skills, 173/57/63/7**; grades 151/16/107/26 -> **173/16/104/7** (Step 0 plan-of-record #151 capability-review default; the catalog-decision alternative would be 173/17/103/7 and is not used); priority 126/149/25 unchanged; gap priority 0/21/5 -> **0/6/1**; GAP ids 26 -> **7 = {110,120,224,225,233,234,236}**; distinct covering 150 -> **163**; beyond-roadmap 80 unchanged; phrase **"80 of 243"**; review_pending 147 -> **125**; areas 01 **32/8/15/0**, 02 **22/4/9/0**, 04 **8/12/10/0**, others unchanged. 22 merged rows delivered: 19 GAP rows -> SHIPPED/explicit-id and the 3 PARTIAL rows #31/#45/#66 upgraded to SHIPPED/explicit-id (#31 application-layer-pattern-advisor, #45 modernization-cutover-planner, #66 configuration-architect). README SKILL-COUNT 230 -> 243, "229 in 23" -> "242 in 23", family 3 17 -> 30, thirteen shipped Phase 2 rows; catalog Phase 2 table thirteen rows and the 30-skill narrative; validator constants / GAP ids / phrase and dependent self-tests updated; new T40 Batch 4 delivery regression (tests 65 -> 66, next free T after T39). Manifest D91 230 -> 243 at truthful source_revision = **C5=93a02703** (final content commit that changed the SKILL.md bytes; the manifest-only provenance commit sets that value and T36 verifies 243/243 paths in CI mode). Protected paths only `scripts/validate-skills.py` and `scripts/tests/test_validator.py` (required registration updates; no check removed or weakened) under the rule-1 AEGIS-APR-140 route; no .github change. **Provenance/evidence (added in correction C5 for D112 parity with D109-D111):** live main **67edd114**; Batch 4 content commit **8c2d598e** with manifest-only provenance **a8f2ff71**; correction rounds C2 **736cbebd**/**8d01bb01**, C3 **46568d72**/**8b265e35**, **C4=a859bc09**/**P4=d018857f**, and final content **C5=93a02703** with manifest-only **P5=head 3e20e6ce** (C5 changed SKILL.md bytes for the seam-handoff cases, so C4 no longer hash-matches all 243 skill files; the manifest source_revision is **C5=93a02703**); evidence hashes: accepted plan **11812652** (15,327 B/61 LF), SPECS-ANNEX **3335f312** (32,656 B/242 LF), Stage B audit **34ec86ab** (37,390 B/120 LF, ACCEPT), A-rows **80a06e49**; gates at this binding: validator **243/0**, self-tests **66 tests / 253 assertions** normal and CI mode, contract-audit **70**, links **837 pages 0 broken/0 dead**, DCO signed, manual-only census **30 skills / 229 expected cases / 0 violations**, **T36 243/243** at the truthful source_revision **C5=93a02703** and the current tree, **T40** delivery regression passing. D1-D111 untouched; this record is append-only (+1/-0 vs base).
- **D113 (2026-10-22) — Batch 5 security / QA / delivery / retrieval (7 new skills + 6 extension-only rows).** Owner plan default (2026-10-21) and Lead scope decision: Batch 5 ships the security/QA/delivery/retrieval remainder. **Seven new skills:** `browser-boundary-reviewer`, `authentication-flow-reviewer`, `security-drift-detector`, `defect-triage-facilitator`, `branching-strategy-designer`, `retrieval-engineering-designer`, `import-pipeline-architect`. Each ships nine canonical SKILL.md sections, one reference, six behaviour cases and a 22-case trigger-eval file (8 positive / 14 negative) naming 14 real manifest owners per skill, with the strict MANUAL-ONLY prompt prefix where an expected negative owner is manual-only; auto-invocable advisory/design-only, no scripts. **Six extension-only roadmap rows, implemented as three extension bundles (E1-E3):** E1 covers rows #231/#232/#233/#234 (four QA rows); `test-plan-designer` +references/qa-scenario-extensions.md (rows #231/#232/#233/#234 scenarios, citing `saas-timezone-architect`, `notification-webhook-ux-designer`, `export-pipeline-architect`, `import-pipeline-architect`); E2 `file-upload-storage-architect` +references/storage-access-policy.md (row #115 bucket policy + signed-URL residual and emergency invalidation); E3 `secrets-identity-hardener` +references/credential-encryption.md (row #104 hash/KDF + migration residual). A bounded reference does not make an owner the material covering skill: #151 stays COVERED and #231 stays PARTIAL (both from Step 0 D111); #104 stays SHIPPED (row #104 is one of the six extension-only rows); #233/#234 stay GAP; no extension coverage status changes in this batch. **Coverage before -> after:** 243 skills, 173/57/63/7 -> **250 skills, 182/57/59/2**; grades 173/16/104/7 -> **182/16/100/2**; priority 126/149/25 unchanged; gap priority 0/6/1 -> **0/1/1**; GAP ids 7 -> **2 = {233,234}**; distinct covering 163 -> **167** (six new covering skills minus two lost owners: #108 `human-agent-trust-reviewer`, #130 `docs-as-code-architect`); beyond-roadmap 80 -> **83**; phrase **"83 of 250"**; review_pending 125 -> **116**; areas 02 **23/4/8/0**, 03 **28/8/4/0**, 04 **9/12/9/0**, 06 **39/6/8/2**, 07 **20/2/3/0**, others unchanged. **Nine roadmap rows delivered:** GAP->SHIPPED/explicit-id #110/#120 (browser-boundary-reviewer), #224/#225 (defect-triage-facilitator), #236 (branching-strategy-designer); PARTIAL->SHIPPED/explicit-id #108 (authentication-flow-reviewer), #130 (security-drift-detector), #75/#150 (import-pipeline-architect). `retrieval-engineering-designer` is a non-roadmap GOV-02 seam (beyond-roadmap +1; no row). README SKILL-COUNT 243 -> 250, "242 in 23" -> "249 in 23", family counts 19/11/25/14/15 -> 20/14/26/15/16, seven shipped rows; catalog Phase 3/4/5/6/7 tables +1/+3/+1/+1/+1 rows; validator constants / GAP ids / phrase and dependent self-tests updated; new T41 Batch 5 delivery regression plus T42 covering-owner assumptions (tests 66 -> 68; next free T after T40). Coverage JSON canonical: nine rows SHIPPED/explicit-id with batch-5 evidence and notes, totals re-derived from entries (no copied numbers), scope_note phrase; coverage MD totals/per-area/GAP section updated. Manifest D91 243 -> 250 at truthful source_revision = the Batch 5 content commit C (manifest-only provenance commit P follows and T36 verifies 250/250 paths in CI mode); G must use a history-preserving two-parent merge so C stays a T36 ancestor. Protected paths only `scripts/validate-skills.py` and `scripts/tests/test_validator.py` (required registration constants, dependent fixtures and an additive T41 regression; no check removed or weakened) under the rule-1 AEGIS-APR-140 route; no .github change. Scope: 7 new skill directories (28 files) + 6 extension files + 8 registration files = 42 planned files; correction C2 adds the `secrets-identity-hardener/evals/evals.json` change needed to make the E3 stored-credential extension reachable from its evals, so the final diff is **43 files** (+3564/-191). Correction C2 (same PR; D1 REVISE 6346640285 / E1 FAIL 6346736127) regenerated the seven skill bodies/references/evals with domain-specific artifacts and complete Stop-Conditions routing, fixed the three extension bundles (E1 row mapping to live #231-#234, E2 signed-URL emergency invalidation, E3 memory-hard KDF + stored-credential wiring), completed the README/catalog descriptions, corrected the README Phase-7 arithmetic, reconciled this D113 extension wording, restored the D107 rationale comment, and added additive T42 covering-owner assertions; final provenance content C2 and manifest-only P2 (source_revision=C2; T36 250/250). D1-D112 untouched; this record is append-only (+1/-0 vs base). Correction C3 (same PR; D2 REVISE 6347216888 / E2 review 5618266672) aligns the #232 owner citations to `notification-webhook-ux-designer`, records the six extension-only rows (including #104) in this record and T41, updates the test count to 66 -> 68 (T41+T42), fixes the browser/auth/defect/retrieval/drift behaviour-eval assertion alignment, the browser E2/E6 conflict split, the stale Batch-2 assertion message, the UNOWNED class definition, the defect severity wording and the Use-When double period; body regenerated truthfully and the G10 advisory-review disclosure is carried in the SD-C C3 record comment (no body edit for advisory reviews, per the owner standing rule). Correction C4 (final correction round; D3 REVISE 6347581003 / E3 6347597360) aligns retrieval E5 assertions to its chunking/embedding prompt, adds the authentication device-trust model and input evidence, adds import export-contract mirroring inputs/table, corrects the HSTS preload threshold and defect-triage completed example, relabels the auth-flow matrix revocation column, fixes the secrets stored-credential wording/numbering, clarifies the retrieval index tenant-scoping handoff, adds security-drift remediation routes, relaxes the brittle T41 exact-text assertions to structural facts while keeping them additive, fixes eval acronym casing, and records in the C4 SD-C comment that the C3 record wording about the body edit (review 5618266672) was inaccurate because body regeneration included its disposition line, plus the C3-head advisory review 5618505139 disclosure (no body edit for advisory reviews, per the owner standing rule). Correction C5 (same PR; D5 REVISE 6349876649) final provenance: content **C5=c2bce45d883ba5f8d32bdf0eedce79c25014b773** and manifest-only **P5=head fbf54a6b35cfd08ed3299bafd017fb3e581393e9** (source_revision=C5; T36 250/250 at C5 and the current tree). The earlier "final provenance content C2 and manifest-only P2 (source_revision=C2; T36 250/250)" sentence describes C2's then-final state and is retained as history. Correction C6 (final correction round under the owner-approved amended convergence limit; D5 REVISE 6349876649) records only this append-only provenance clarification and the regenerated PR body; no other content changes.

## 6. Post-merge corrections

- **D114 (2026-10-24) — #233/#234 regraded SHIPPED/explicit-id after shipping; pointer-only repairs for #2/#4.** The 2026-10-23 standing owner work order authorized building both QA skills; import-qa-strategy-designer (import in PR #897, content commit b4161406, merge 729a25a8) and export-qa-strategy-designer (export in PR #899, content commit 4b4552e9, merge 417235eb) shipped, so #233 Import QA Strategy and #234 Export QA Strategy are regraded **SHIPPED/explicit-id** with those shipped skills as the evidence; the earlier D113 extension-only GAP lines for #233/#234 are **superseded by the shipping** (reference only; D113 is not rewritten). #2 System Context Mapping and #4 Bounded Context Identification keep their status/grade/priority; only their stale catalog pointers are repaired to catalog lines 1478-1479 / skill rows 392,527 (#2) and catalog lines 1480-1481 / skill row 391 (#4). **Convention (owner decision 2026-10-24, DS-2):** the D114 convention applies to a skill newly shipped FOR the row (matching D113's own usage, #108, #110/#120); rows an existing skill merely covers stay COVERED; the owner authorization is not evidence grade. Totals re-derived from rows: SHIPPED 184 / COVERED 57 / PARTIAL 59; explicit-id 184 / catalog-decision 16 / capability-review 100; review_pending 114 (300 entries minus 184 explicit-id leaves 116 non-explicit-id rows; 2 of those carry a recorded planning-gate confirmation; review_pending is therefore 114). The validator fails closed on an unknown skill-shaped token after the phrase and on a malformed/no-token shipped-as phrase (bare, colon-only, punctuation-only, numeric-only, or ordinary prose).

- **2026-10-08 — D73 clarified: per-kind rejection checks and a fourth open
  item.** D73 gained an inline appended correction. Row 2 (e)'s offline checks
  are the ones that apply to each event kind, and the "Not decided here" list
  gains the Open question of whether a targeted-review row may be withdrawn
  under AEGIS-APR-117. No condition, count or register entry changes, and
  D73's dated text above is unchanged. See the D73 entry.

- **2026-09-30 — Line-number citations in §5 re-verified; the stale ones are
  re-pointed.** A full-page audit checked every `path:NNN` / "line NNN"
  citation in this log against `origin/main` at `2184b54f`. The decisions and
  their corrections are append-only, so the dated entries are **not**
  rewritten: each affected entry gained an inline appended correction, listed
  here newest-first per the §6 convention.
  - **D53 — the `Verified-compliant` block (5 of its citation groups stale).**
    `docs/skill-generation-standard.md:128` and `:141-142` and the
    `_template/SKILL.md:59`/`:76-80` targets no longer exist as cited; the
    standard's §5 was rewritten for TALI v3.2.3 and the template was reflowed
    by D54, D56 and #528. D52's `standard:177` also moved (now `:593`). See
    the D53 entry.
  - **D39 — the "Six grep confirmations" block (all three numbers stale).**
    The two README headings it quotes are now lines 152 and 250, and the third
    heading was retitled twice (now `## Maintainer reading routes`, line 676),
    so `## Start here (canonical reading order)` no longer exists in the README (the phrase survives only in the preserved D39/D51 passages and in this correction's own text).
    Heading targets now carry slug anchors so they survive reflow. See the D39
    entry.
  - **D68 — a self-contradicting D10 row Note corrected.** The D10 Tier 1
    `regression-first-bug-fixer` row reads both "dropped (D68)" and "owned by
    `tdd-engineer` … not bug reproduction"; the drop is TRUE
    (`git ls-tree -r --name-only origin/main -- .claude/skills` has no such
    directory) and the trailing Note is the stale D10 wording D68 refutes.
    The row's Note is dated text and stays as provenance. See the D68 entry.
  - **D10 — Tier 1 table header made accurate.** The header claimed every
    entry is "candidate — not built" while three rows already carried
    built/dropped markers and two carried none. The header now states the
    rows carry their own per-row status, and the two unmarked rows
    (`test-tenant-provisioner`, `ci-failure-classifier`) are marked **built
    (D68)**.
  - **D56 / D55 — census and residual citations.** D56's `catalog:93` target
    moved to `docs/skills-catalog.md:249`; D55's RESIDUAL note is preserved but
    the items it names have since been resolved on `main` (the duplicate live
    count was reworded countless, and the surviving marker pair is now README
    :557 reading 195/23).
  - **D34 — inbound links and the auto-merge line.** README:120/184/453,
    CONTRIBUTING:3, README:121, README:701 and README:151 are all stale; the
    current lines are recorded in the D34 entry.
  - **Sweep result.** Every `path:NNN` and "line NNN" citation in the page was
    checked individually, with wrapped lines flattened first so a citation split
    across a line break still counts. No instance count is stated here: the forms
    overlap (a `README.md:1166` also reads as a `README:NNN`), so any single
    number would depend on an arbitrary rule. What is verifiable is the list of
    sites below. The stale groups were refuted and re-pointed — 5 in D53's own
    block plus D52's adjacent `standard:177`, 3 in D39, 2 in D34, D68's D10 row
    Note, D56's `catalog:93`, and D55's RESIDUAL figures. No exact/stale tally is
    stated here either, for the same reason as the total above. What follows are
    those sites, including the
    README:1166/:1250 pair at the D52/D53-time date they were written and the
    `:523`/`:111`/`:76`/`:485` historical notes kept as provenance; the rest
    are D57-time figures that still reproduce (the byte-hash, 139→88, :485).

- **2026-09-27 — D65 amendment: open gaps closed.** All four gaps D65
  listed now have an owning skill (2026 IDs). LLM08, hidden context beyond
  the system prompt: D66, PR #409 (`4416c6d`). LLM01, injection hidden in
  images, audio or other non-text input: PR #427 (`0030e73`) extended
  `prompt-injection-defender`. LLM10, review of AI-generated code: PR #424
  (`5711ddf`) extended `llm-output-safety-reviewer`. LLM04, trust in the model
  artifact promoted to production: PR #428 (`0cb0777`) extended
  `supply-chain-security-reviewer`. No skill was added; the count stays 186.
  D65's text above is unchanged. See the
  [OWASP LLM threat catalog](../../.claude/skills/ai-threat-modeler/references/llm-top10-threat-catalog.md).

- **2026-09-26 — D64 amendment.** PR #395 (`741b29a`) added a reciprocal
  `plan-entitlement-architect` → `feature-flag-architect` yield. The owner
  kept it on 2026-09-26, so four (not five) one-way D64 ROUTE-002 findings
  remain census data: toward `authorization-matrix-designer`,
  `ab-test-designer`, `ci-pipeline-architect` and `tenant-isolation-reviewer`.
  D64's text above is unchanged. See the
  [ROUTE-002 dispositions record](../evidence/route002-dispositions-2026-09-26/README.md).

- **2026-09-12 — Current backlog labels reconciled.** At the owner's request,
  corrected stale completion labels against merged PRs #83/#85/#87/#89 and the
  shipped skill directories. Backlog items BER-BKL-001/-004/-006/-008 are
  complete for their scoped offline deliverables; real-host gates and OD-1/OD-2/OD-3 remain open.
  D12.2/.4/.5/.6/.7 and `docs-retention-index` are implemented. The older
  AEGIS-060 candidate on the calibration branch is explicitly superseded by
  merged main's rejection. Partial schema/policy work remains visible. See the
  [completion crosswalk](../evidence/backlog-status-reconciliation-2026-09-12.md).
  This records status corrections only; it changes no runtime or authorization.

- **2026-07-07 — Phase 4 headline correction.** Squash commit `ee6515c` (PR #7) is titled "Phase 4: security & RLS pack (4 skills)" but actually delivered **all 9** canonical Phase 4 skills (`threat-modeler`, `appsec-implementer`, `multi-tenant-security-tester`, `rls-policy-auditor`, `secrets-identity-hardener`, `supply-chain-security-reviewer`, `security-pr-reviewer`, `secure-migration-reviewer`, `static-analysis-reviewer`); the stale "(4 skills)" headline was captured when auto-merge was armed on the 4-skill branch state, and the remaining 5 skills were pushed before the merge fired. `main` contains all 9 — validator reports 36 skills, exit 0.


- **2026-10-26 - D115: plan-stage skills and A/B ownership supersession (owner D7).** Per owner item 3 (2026-10-25T20:51:26-07:00; OD-6 record sha256 7749905e...) and AD-5/AUTON-1, queue item 5 is delivered: plan-of-record-author owns Stage A plan-of-record writing and plan-audit-reviewer owns the independent Stage B plan-level audit. The 2026-10-21 decision is superseded for stages A and B only; stages C and E remain procedural. Owner D7 wording (verbatim): "D7 = YES - ratify the plan-stage skills wave (plan-of-record-author + plan-audit-reviewer), supersede the 2026-10-21 decision for stages A and B only (C and E stay procedural), and confirm defaults D1, D2, D3, D4, D6 with D5 deferred. The recurring need is demonstrated and the plan should cite it: batch-25 r1-r5, batch-26 r1-r4, pilot block B r1-r4, R4 fourteen rounds, R5 seven, R6 six, the UX extension plan r1-r4, and #913 at fifteen. PR-1's two protected scripts paths are routine count/registration edits under APR-140. Unblock Stage C now." AD-5 D3 keeps the two PRs sequential; this entry is the PR-2 append-only record. Prior entries are unchanged.


- **2026-10-26 - D116: PKG-18 reconciliation close-out (FD-1 cleanup; no parallel machinery).** Final owner-queue item: the external PKG-18 snapshot is stale and is not authority; re-derived from current main, the shipped work remains shipped and the only tracked remainder class is unused module-level validator names. This PR removes exactly four verified-dead module-level names from scripts/validate-skills.py: `COVERAGE_PRIORITIES`, `_coverage_shipped_normalize`, `_coverage_shipped_link_mask`, and the transitively dead regex `COVERAGE_SHIPPED_LINK_MASK_RE` (its only load was inside the removed helper); retained used names are `_coverage_shipped_normalize_tail` and `_coverage_shipped_claims` (plus `_coverage_shipped_scan`), and the adjacent comments now describe the live normalization. No behavior change; no test reference to the removed names; gates unchanged (validator 254/0, validator self-tests 253 exactly 68 defs, contract 71). Shipped statuses recorded: D114 fail-closed/PTR #908; FD-2/FD-3/FD-4 and O-1 #909; FP-10 linear link scanner and pinned scaling tests; FD-1 dead-name cleanup this PR. DS-4b stable anchors shipped (#924) with numeric-anchor MACHINE ENFORCEMENT DEFERRED - open cases: separator chains (e.g. `catalog L/630-631`, `catalog L--630-631`, `catalog lines..1480`) and keyword-internal separators (e.g. `catalog_lines 1480`, `catalog-lines 1480`, `skill_rows 394`) - per coverage-map.md:9 and the DS-4b Stage C reduction record; no rejection claim. DS-7c hands off to the frozen REV-6 plan; its Stage C is blocked on owner DEC-R1. FP-8 remains a disputed carry (D113 protected; no change). F-03/C-01 and the duplicate AC-14 label are evidence-only/process carries with no tracked target. F-to-G receipt consistency remains process/coordinator discipline (no tracked program change; no parallel machinery introduced). Explicit NO PARALLEL MACHINERY: one validator, one contract-audit engine, one Markdown link checker, one behavioral runner; duplicated parsing helpers stay by design and self-test-pinned. Append-only: D113/D114/D115 bytes are unchanged (this entry only appends to the latest D115 tail). No owner decision is required for the dead-name cleanup; OD-1 (DS-7c/DEC-R1) and OD-2 (optional DS-4b enforcement) remain owner choices. 0 human; no merge authority; no CI-green claim.**

- **D117 (2026-10-26) - Owner seven-item decision recorded; transcription confirmation, OD-A one-time grant, and queue dispositions.** Recorded from
  the owner's direct session message 2026-10-26T07:29 PT (14:29Z) and second direct confirmation 2026-10-26T07:49 PT (14:49Z); owner evidence files:
  OWNER-DECISION-2026-10-26T0729Z-SEVEN-ITEMS.md (3,620 B / 36 LF / sha256 344f3cb73c484fa6ea9a65550459f4419e38996b875886cedc22050122fa9529) and
  OWNER-CONFIRMATION-2026-10-26T0749Z.md (1,310 B / 8 LF / sha256 c6acab68d156cb2f757b97fff372b37e3359b2d3bc5dbe24efe760e1037acaf5).
  - **Owner instruction source (seven-item decision):** Source: Peter, typed directly in my session at 7:29 AM PDT. Verbatim excerpt covering the
    acted-on items: item 2 DEC-R1=B; item 3 OD-A grant with conditions (a)-(d); item 4 OD-Q903-2=A / OD-Q903-3=B trigger-scoped standing override /
    OD-Q903-4=A / OD-Q903-5=A; item 5 OD-2 numeric-anchor enforcement deferred; item 6 PKG-09 Wave 2 NOT DERIVABLE/CLOSED and OD-02 resolved by item
    1; #919/#920 dependabot disposal; item 7 later WITHDRAWN by amendment. Full owner words:
    _A/evidence/owner-decisions/OWNER-DECISION-2026-10-26T0729Z-SEVEN-ITEMS.md.
  - **Owner instruction source (second confirmation):** Source: Peter, typed directly in my session at 7:49 AM PDT. Verbatim: "CONFIRMED. All six
    items quoted at #910 comment 6407991132 are my decision, issued by me in the Project Aegis chat on 2026-10-25 at 20:51 PT. The wording was drafted
    for me by Claude, my auditor/planner, and I issued it as written. Every item is mine: (1) #913 narrow-C, (2) #915 covered by standing grants, (3)
    D7 = YES with defaults D1-D4 and D6, D5 deferred, (4) AD-10 ratified, (5) AD-11/AD-12 ratified with the ladder amendment, (6) #912 OD-1 ratified.
    APR-142 and APR-143 are authoritative as of this confirmation. The three administrator merges made under them (#913, #917, #918) stand."
  - **Owner instruction source (item 7 withdrawal):** Source: relayed owner reply #8ld4jznkzn6114218ici in the inbox (comment 6419060793). Relayed
    owner words: "OWNER DECISION: B. Keep the merged #915 text unchanged and WITHDRAW item 7 of my 2026-10-26 07:29 decision. The merged rule is
    correct: a nonce counter stored inside the restorable instance rolls back with a snapshot or backup restore, which re-validates spent nonces and
    allows replay. Anchoring it outside the restorable instance, with fail-closed when unverifiable, is the safe design, and it already admits a
    hardware-backed monotonic counter as the local option. No follow-up PR. Record the withdrawal next to item 7 wherever my seven-item decision is
    transcribed, with this reason. The rest of the seven-item decision stands." Acted on the relayed owner words as written; the brief was drafted by
    Nemesis and approved by the owner at 2026-10-26T14:50:39.839Z.
  - **Owner instruction source (standing provenance rule):** Source: Peter, typed directly in my session at 8:27 AM PDT. Standing provenance rule:
    every owner instruction acted on must state whether it was typed directly or relayed, with the exact session/time or relay doc/comment id and
    verbatim words as required by the owner's two forms.
  - **Owner evidence citation (amended):** Current amended owner evidence: 5,042 B / 44 LF / sha256
    0362eccd2e1ed835ca9b77ae5e36a56ac22fb3db00bed71b95c4f46afc48f344; the original first 3,620 B / 36 LF / sha256
    344f3cb73c484fa6ea9a65550459f4419e38996b875886cedc22050122fa9529 remains preserved as a byte prefix (appended amendment only).
  - **Amendment timestamp disclaimer:** 08:20 PT on 2026-10-26 equals 15:20Z. The amendment evidence filename
    AMENDMENT-2026-10-26T0820Z-ITEM7-WITHDRAWN.md uses the owner's local PT clock with a Z suffix, not UTC; the file name is retained for evidence
    identity, not as a UTC timestamp.
  - **Amended evidence arithmetic:** Amended file named _A/evidence/owner-decisions/OWNER-DECISION-2026-10-26T07:29Z-SEVEN-ITEMS.md is 5,042 B / 44 LF / sha256
    0362eccd2e1ed835ca9b77ae5e36a56ac22fb3db00bed71b95c4f46afc48f344. Original first 3,620 B / 36 LF / sha256 344f3cb7... plus amendment 1,420 B / 7 LF / sha256 6ff7e5bd... = 5,040
    B / 43 LF; the actual amended file is 5,042 B / 44 LF, the 2 extra bytes / 1 LF being the separator blank line between the original transcription block and the appended
    amendment.
- **C5 provenance/arithmetic note:** the compressed seven-item excerpt is a SUMMARY/EXCERPT, NOT verbatim; item 7 was added later by the #915 amendment and was not part of the
  - **Summary/excerpt of the seven-item decision** (not verbatim; item 7 was added later by the #915 amendment).
  - **#919 merge_commit_sha:** GitHub merge_commit_sha field (closed-PR test-merge SHA; not an actual merge commit).
    original 2026-10-26T07:29 message. Exact item-1 owner words source: #910 comment 6418606020, owner typed 2026-10-26T07:29 AM PDT. Amended owner file
    OWNER-DECISION-2026-10-26T0729Z-SEVEN-ITEMS.md is 5,042 B / 44 LF / sha256 0362eccd...; original prefix 3,620 B / 36 LF / sha256 344f3cb7... plus amendment 1,420 B / 7 LF /
    sha256 6ff7e5bd... = 5,040 B / 43 LF; the extra 2 B/1 LF is the separator blank line between original block and appended amendment.
  - **Item 1 (transcription):** #910 comment 6407991132 quotes the 2026-10-25T20:51 six-item decision verbatim; the owner's second direct confirmation
    (2026-10-26T07:49 PT; owner evidence file OWNER-CONFIRMATION-2026-10-26T0749Z.md 1,310/8/sha256
    c6acab68d156cb2f757b97fff372b37e3359b2d3bc5dbe24efe760e1037acaf5) confirms every item is the owner's, with wording drafted by the owner's
    auditor/planner Claude and issued as written; APR-142 and APR-143 are authoritative from this confirmation; the three administrator merges made
    under them (#913 f1bfe44d, #917 fe638bce, #918 f1bacf5b) STAND. Recorded as AEGIS-APR-144; the #921 pending-owner-confirmation limitation is
    satisfied and the old #921 note remains unchanged as historical; APR-142/143 entry text unchanged and no retroactive validation of
    out-of-condition merges.
  - **Item 2 (DEC-R1 = B):** keep DS-7c at 4+1 paths; README SKILL-COUNT/FAMILY-COUNT markers are a separate DS-7c-b follow-up; no README path is
    authorized by this item; smaller diffs converged faster.
  - **Item 3 (OD-A):** one-time grant modeled on APR-119 recorded as AEGIS-APR-145: additive SIDE-005 rule plus TOOL_VERSION bump; exactly the four
    APR-119-named artifacts with the docs preface; conditions (a)-(d), one separate regeneration PR, finding-delta and per-NEW-finding disposition, no
    other regeneration, no reliance on a consumed grant. This recording/maintenance PR is excluded from the one-PR grant and does not consume it;
    consumption attaches to the regeneration PR's merge.
  - **Item 4 (#903 item 1 choices):** OD-Q903-2 = A (any MANUAL-ONLY skill by exact name plus reason); OD-Q903-3 = B trigger-scoped standing override
    bound to a named trigger in the consumer's recorded policy, revocable, re-pinned on every sync - NOT per-invocation; OD-Q903-4 = A (consumer-local
    register; the Aegis register is for Aegis); OD-Q903-5 = A (normative; an advisory contract would not have prevented #903); plan must be revised
    and re-audited before implementation.
  - **Item 5 (OD-2/NFA-1):** numeric-anchor enforcement stays DEFERRED; three fail-open attempts show the predicate is not ready; the resolver detects
    staleness but does not enforce. OD-2 (numeric-anchor enforcement) is KEPT DEFERRED by this owner decision, not carried open for action; NFA-1
    remains deferred. OD-2 is not OD-02.
  - **Item 6 (PKG-09 Wave 2; OD-01 and OD-02):** the external ENG-003/PKG-09 mapping could not be obtained; PKG-09 Wave 2 (OD-01) is recorded NOT
    DERIVABLE and CLOSED and must not be reconstructed. OD-02 (the APR-142 pending-confirmation limitation) is a different item from OD-2 and is
    RESOLVED by item 1 / APR-144. Do not conflate OD-2 with OD-02.
  - **PKG-09 Wave 2 disposition:** NOT DERIVABLE and CLOSED; do not reconstruct.
  - **Item 7 (#915 residuals - WITHDRAWN; owner approval 2026-10-26T14:50:39.839Z = 07:50 PT; amendment recorded 08:20 PT = 15:20Z):**
    2026-10-26T07:29 seven-item decision and its #910 transcription 6418606020. The merged #915 feature-flag-architect text (SKILL.md:168, :260,
    :321-322) STANDS UNCHANGED; NO follow-up PR is opened. Reason (owner verbatim): a nonce counter stored inside the restorable instance rolls back
    with a snapshot or backup restore, which re-validates spent nonces and allows replay; anchoring it outside the restorable instance with
    fail-closed when unverifiable is the safe design, and it already admits a hardware-backed monotonic counter as the local option. SD-VERIFY-915
    (#910 comment 6418631997) is RESOLVED by owner decision B; the earlier contradiction report is superseded/resolved and retained as history only.
    The nonce-anchor principle and offline-residual wording from the withdrawn item are NOT an active owner requirement. Items 1-6 stand unchanged.
    Amendment evidence: _A/evidence/owner-decisions/AMENDMENT-2026-10-26T0820Z-ITEM7-WITHDRAWN.md 1,420 B / 7 LF / sha256
    6ff7e5bd0123a74dcd5292d180b75da08c794b7fe9ddd42ec98199da61ab040e.
    - **Item 7 wording note:** the withdrawn item 7 nonce anchor principle is not an active owner requirement; the merged #915 text stands unchanged.
  - **Additional (#919/#920):** #919 CLOSED 2026-10-26T14:31:03Z (not merged; head 9a5fa680316e9d08bed9e7ef539361d493bb3e02; GitHub merge_commit_sha field (closed-PR test-merge
    SHA; not an actual merge commit)
    4c9bf040f7765adab817768f1e8447d879c8990d). It changes only the four pinned actions/setup-python bump lines in
    .github/workflows/validate-skills.yml; under the standing dependabot rule it cannot merge because it touches a protected .github workflow path and
    its required gate-guard check fails, needing a separate owner/APR route - NOT because its content went beyond pinned bumps. #920 MERGED
    2026-10-26T14:31:49Z at merge commit a3b59f6dd76db8e700d5a2bb81d05d77abb6058b (head c2d6feeb266012a0baa30dfa49d3bfdc19f7934f) because checks were
    green and its diff was only pinned dependency bumps. No authority changes from either disposition.
  - **Second confirmation evidence:** OWNER-CONFIRMATION-2026-10-26T0749Z.md 1,310 B / 8 LF / sha256
    c6acab68d156cb2f757b97fff372b37e3359b2d3bc5dbe24efe760e1037acaf5; the three administrator merges stand.
  - **Append-only:** this entry follows D116 and appends to the latest tail; D113/D114/D115/D116 bytes are unchanged; no existing line is edited. No
    secrets or PII are recorded beyond the owner-authored decision/evidence pointers above; no implementation, merge authority, approval or CI-green
    claim is created by this record.
  - **Recording attribution:** produced by AI agent sd-b-fu, model route DeepSeek-V41-Flash (registered id deepseek-flash @ deepseek-account, DeepSeek Harness); not an approval/waiver; no merge authority.

- **D118 (2026-10-26) - Owner standing instructions recorded (APR-146); APR-143 no-protected-path clarification verified.**
  - **APR-146 recorded:** the owner's 2026-10-26 standing instructions are recorded in the approval register as APR-146 (POLICY/STANDING-INSTRUCTION, recording-only; adds no authority and removes no gate; AGENTS.md, docs/delivery-workflow.md and the approval register govern; APR-140/APR-142/APR-143 are unchanged; no new protected-path exception). Owner source: Peter, typed directly in my session at approximately 10:10 AM PDT; owner evidence: _A/evidence/owner-decisions/OWNER-STANDING-INSTRUCTIONS-2026-10-26.md (3,565 B / 10 LF / sha256 bb1e759aec7da9570061d2fd54031ece8b38cac9f7d87bc7531994fe0dd7914a).
  - **APR-143 no-protected-path verification (verification only, not a grant):** the register's recorded reading at heading line 7031 and body lines 7059-7066 remains valid for a PR touching NO protected path, subject to each grant's own conditions (exact head, receipt, binding, check state); this entry verifies that recorded reading and creates no grant, authority or protected-path exception.
  - **#910/#926 owner-record lineage:** #926 merged as 86de6e02f11ecd1dcf1208c55836d3f9bb885ec7 and carries APR-144/APR-145 + D117; the #910 owner inbox is the owner-decision source surface. This entry follows D117.
  - **Case B coordination:** #927 had not merged at this C, and latest main D was D117; when #927 merges it must use D119 (coordinated; no duplicate id; no skip/renumber). No D119 entry exists in this C.
  - **Append-only / no claims:** D113-D117 unchanged; append-only; no secrets/PII; no authority/approval/CI-green/merge claim is created by this record; recording attribution sd-a, DeepSeek V4 Flash (deepseek-flash @ deepseek-account, DeepSeek Harness).
