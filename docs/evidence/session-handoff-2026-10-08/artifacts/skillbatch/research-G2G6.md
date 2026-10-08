# Research: G2 (QA Tier 3) + G6 (Phase 5 extras and untiered category-06 rows)

Helper QA-B, Stage A support only (planning research). Writes no repository file, makes no commit, no
GitHub write. Started `2026-10-08T17:11:39Z` (`date -u` at start). Finish time is in the handback.

## 0. Base, role, method

- **Base.** `git ls-remote origin main` -> `5228977920ee479e1fe1ec6b8d56f8fc24c14947`; REST
  `repos/.../commits/main` -> same SHA. The local checkout is detached at `c060a7cb` (behind), so
  every file below was read from `git archive 52289779 | tar -x` into
  `$S/skillbatch/g2g6-tree/`. Line numbers are at `52289779`. Earlier helpers' partial files
  (`desc*.txt`, `qab-*`) were NOT used.
- **Role A confirmed** from the four landmarks at base: `README.md` line 1 `# Project Aegis`,
  `docs/skills-catalog.md`, `scripts/validate-skills.py`,
  `artifacts/audits/skill-contract-audit-baseline.json` (all present, `ls`).
- **Shipped set.** `ls .claude/skills | wc -l` -> 196 entries (195 skills + `_template`); a YAML
  parse of every `SKILL.md` (`$S/skillbatch/g2g6-scripts/desc.py`) -> 196 parsed, 30 with
  `disable-model-invocation: true`, the same 30 leading with `MANUAL-ONLY`. Agents:
  `.claude/agents/` has 7 definitions, including `qa-automation-lead.md` and
  `senior-troubleshooting-lead.md` (both relevant below).
- **Open work.** REST `pulls?state=open` -> 0 open PRs, so no lane already holds any candidate.
- **Demand evidence in-repo.** All 680 issues+PRs listed via REST (7 pages: 100x6 + 80); only one
  non-PR issue exists (#101, reserved scope). Title grep for property-based / mutation / soak / chaos /
  bug report / triage / smoke / e2e-test / qa-closeout -> no hits except ai-closeout-reporter work
  (#362, #462, #511). A docs grep for the Tier 3 topics finds only the backlog rows themselves plus
  the resilience scope rows cited below. **So demand for every candidate is "no in-repo evidence
  found"; it is not used to support the recommendation.** (Cross-cutting demand is the DEMAND helper's job.)
- **Skills used (dogfood).** `prioritization-frame-picker` (`.claude/skills/prioritization-frame-picker/SKILL.md`)
  for the ranking method: a coarse value-vs-effort cut because every input is a guess or a
  planning label, ranges not decimals, items marked evidence/guess, a sensitivity check (§6). The
  overlap lens is `skill-quality-reviewer` check 2 (trigger collision) and check 3
  (duplication / make-it-an-extension) (`skill-quality-reviewer/SKILL.md:79-89`), applied to
  candidates rather than to drafted skills. Workspace-role check follows `agent-startup-context-gate`.
  No MANUAL-ONLY skill was used.

## 1. The library's MANUAL-ONLY rule (applies to every candidate)

- `docs/skill-generation-standard.md:116`: `disable-model-invocation: true` "for any skill that performs
  **side effects** (writes files outside scratch, calls networks, mutates external state, spends money,
  deploys)", with the `MANUAL-ONLY; never auto-invoke. ` sentinel (:167-169).
- `:48-50` "A read-only reporting skill can normally be auto-invoked. A skill with side effects is
  manual-only unless ... section 5's bounded exceptions"; `:271-275` and `:287` ("Install, call a
  network, mutate external state, deploy or spend -> Manual-only").
- **Library pattern for QA:** design/plan skills are auto-invocable and execute nothing
  (`load-test-planner:3` "PLANS only", `:241-245`; `performance-test-harness:3` "this design executes
  nothing against production"; `resilience-architecture-reviewer:3` "Review only; runs no fault
  injection", Security Rules `:231-234`); executing skills are MANUAL-ONLY
  (`vitest-unit-component-engineer:3` "WRITES test files and RUNS the suite";
  `test-tenant-provisioner:3` "WRITES to an environment"; `database-backup-verifier`, restore drills).
- **Consequence for chaos/soak:** *planning* a soak or a fault-injection drill is auto-invocable;
  *running* one against any environment mutates external state and would be MANUAL-ONLY. The shipped
  owners already refuse execution (`resilience-architecture-reviewer:276-279`,
  `load-test-planner:241-245`), so no candidate here needs an executing variant.

## 2. G6 enumeration — "remaining untiered cat-06 rows"

Command (rows 219-270 of `docs/reconciliation/step-0-reconciliation-v4.md` = covered table + Tiers 1-3,
against the 55 rows of `docs/skills/06-qa-test-engineering.md:27-81`) -> 18 numbers not mentioned:
`188, 189, 191, 193, 202, 213, 216, 217, 218, 219, 220, 224, 225, 231, 232, 233, 234, 235`. #199 is
mentioned only inside the Tier 1 #198 note ("source range #196-#199", v4:247), and v4:274 lists it as
untiered, so the set is **19 rows**, matching v4:274-276 exactly (#188, #189, #191, #193, #199, #202,
#213, #216-#220, #224, #225 + tail #231-#235). Plus the two execution-plan extras
`e2e-test-architect`, `qa-closeout-reporter` (v4:196-198; catalog :503-506, :1334-1342).

**Inconsistency found (documentation, not a blocker):** v4:277-278 names the rows "partially absorbed via
shipped catalog source mappings" as #191, #199, #217, but the catalog also maps **#189** to
`playwright-e2e-engineer` (`docs/skills-catalog.md:523`, "cat 06 #187/#189"). The v4 list says
"Several", so it is incomplete rather than contradictory.

## 3. Summary table

Verdict key: NEW = no shipped owner; PARTIAL = shipped owner + named residual gap; COVERED = shipped
owner(s), new skill would collide. Estimates are agent estimates in active hours, **low confidence**
(basis §5).

| # | Candidate / row (priority) | Verdict | Owner(s) today | Form if built | Invocation | Est. (h) |
|---|---|---|---|---|---|---:|
| G2-1 | `property-based-test-designer` #194 (P2) | **NEW** | none (passing mention only, `systematic-debugger/references/isolation-tactics.md:28`) | new design skill | auto-invocable (design only) | 2.5–4 |
| G2-2 | `mutation-testing-reviewer` #195 (P2) | **PARTIAL** | `test-coverage-mapper` (theater rubric), `vitest-unit-component-engineer` step 6, `qa-automation-lead` agent | **extension** of `test-coverage-mapper` | stays auto-invocable | 0.75–1.5 |
| G2-3 | `soak-test-planner` #207 (P2) | **COVERED** (tiny residual) | `load-test-planner` (+ `performance-test-harness`) | drop; optional micro-extension | n/a | 0–0.25 (+0.25–0.5 optional) |
| G2-4 | `chaos-test-planner` #208 (P2) | **COVERED** | `resilience-architecture-reviewer` (+ `integration-test-designer` seam failures) | drop | n/a (execution would be MANUAL-ONLY) | 0–0.25 |
| G6-1 | `e2e-test-architect` (product-agnostic roadmap P0) | **COVERED** (composition) | `qa-strategy-architect`, `test-plan-designer`, `qa-automation-architect`, `regression-suite-curator`, `test-data-architect`, `playwright-e2e-engineer` | drop | n/a | 0–0.25 |
| G6-2 | `qa-closeout-reporter` = #235 (P0) | **COVERED** | `ai-closeout-reporter` + `release-readiness-reviewer` (two pinned evals) | drop | n/a | 0–0.25 |
| G6-3 | #224 Bug Report Authoring (P1) + #225 QA Triage (P1) | **PARTIAL** (largest residual in G6) | only inside `clickthrough-test-engineer` sessions (manual-only); `prioritization-frame-picker` ranks "bugs" generically | **one new skill** | auto-invocable (drafts; files nothing) | 3–4.5 |
| G6-4 | #188 Production-Safe Smoke Testing (P0) | **PARTIAL** | `synthetic-monitoring-architect` (prod-safety contract, scheduled), `merge-is-deploy-governance` (post-merge = verification), `playwright-e2e-engineer` step 8 (manual-only) | **extension** of `synthetic-monitoring-architect` | stays auto-invocable | 1–2 |
| G6-5 | #231 Timezone QA (P1), #232 Notification QA (P1) | **PARTIAL-minor** | `test-plan-designer` (per-feature plans), scattered domain owners | optional reference-sheet extension of `test-plan-designer` | stays auto-invocable | 1–1.5 (optional) |
| G6-6 | #213 Test Timeout Policy (P1), #202 Snapshot Governance (P2) | **PARTIAL-minor** | `ci-failure-classifier`, `ci-pipeline-architect`, `flaky-test-detective`; `change-classification-gate`, `test-coverage-mapper`, `vitest` | route to G1 planning (overlaps G1 `ci-shard-parallel-isolation`, `visual-regression-test-designer`) or a `qa-automation-architect` extension | auto-invocable | 0.75–1.5 (if done here) |
| G6-7 | #189, #191, #193, #199, #216, #217, #218, #219, #220, #233, #234 | **COVERED** | see §4.G6-7 | record as "Already covered" | n/a | together 0.5–1 (records) |

## 4. Per-candidate evidence

### G2-1 `property-based-test-designer` — NEW

1. **Source:** `docs/skills/06-qa-test-engineering.md:40` "#194 Property-Based Test Design | P2 | Generate broad
   input combinations for validation, parsing, math, state, and transformation logic."; v4:267 (Tier 3,
   "specialized, defer ... build on demand only", v4:263).
2. **Overlap:** grep of all skills for `property-based|property based|fast-check|fuzz|generated input|randomi[sz]ed input`
   -> only `systematic-debugger/references/isolation-tactics.md:28` ("property-based fuzz around the
   boundary", a debugging amplifier) and unrelated "hypothesis" hits in `ab-test-designer`. Nearest neighbors
   do example-based boundaries: `test-plan-designer/references/test-plan-template.md:13` ("Boundaries: empty, one,
   many, max size, date/timezone edges, precision"), `vitest-unit-component-engineer/SKILL.md:60-62`. **Seam risk:**
   `test-data-architect` deliberately prefers named fixtures over random draws
   (`references/test-data-patterns.md:52-53` "as named fixtures, not random draws"; `SKILL.md:138-139`
   "determinism beats variety in fixtures"). A PBT skill must state the reconciliation: generated inputs run
   with a recorded seed + shrinking, and every found counterexample is promoted to a named fixture/regression
   case. Verdict **NEW**.
3. **Invocation:** design only (properties, generators, shrinking, seed policy, which modules qualify), hands
   implementation to `vitest-unit-component-engineer` (manual-only) / `integration-test-designer` ->
   **auto-invocable**, precedent `integration-test-designer:3` ("Produces implementable specs and hands
   implementation off", not manual-only). Writing and running the property suites would be MANUAL-ONLY (§1).
4. **Estimate:** 2.5–4 h (a new read-only skill with one reference sheet; basis §5). Low confidence.
5. **Value/dependencies:** useful for validators, parsers, serializers (round-trip), money/precision math,
   state machines; P2 by the roadmap; no in-repo demand found (§0). Depends on nothing unbuilt. Tooling
   names/versions are volatile and must be verified at build time, not hard-coded.
6. **Trigger boundary:** use when deciding which invariants/properties to test with generated inputs, designing
   generators and shrinking, or making generated tests reproducible; not when implementing/running tests
   (`vitest-unit-component-engineer`), designing the fixture catalog (`test-data-architect`), planning one
   change's boundaries (`test-plan-designer`), fuzzing a running app for security (`dast-safety-harness-designer`).
   **Pin against:** `vitest-unit-component-engineer`, `test-data-architect`, `test-plan-designer`.

### G2-2 `mutation-testing-reviewer` — PARTIAL -> extension of `test-coverage-mapper`

1. **Source:** cat06:41 "#195 Mutation Testing Review | P2 | Use mutation thinking to identify tests that pass
   without proving important behavior."; v4:268.
2. **Overlap:** `test-coverage-mapper:3` "Distinguishes real verification from tests that execute code without
   asserting behavior"; body `:54-57` (verifying vs theater); `references/coverage-mapping-method.md:23-39`
   rubric ending "ask: 'what real bug would make this test fail?' No answer -> theater" — this IS mutation
   thinking, qualitatively. `vitest-unit-component-engineer:73-76` "A new test must fail when the behavior it
   guards is broken — spot-check with ... a scoped temporary mutation". Agent `qa-automation-lead.md:14`
   "Assertion strength — tests that pass trivially or assert too little to catch regressions". grep for
   `mutation test|mutant|stryker|mutation score` -> **0 hits** in skills.
   **Remaining gap:** systematic mutation evidence — reading a supplied mutation-tool report (surviving
   mutants per critical surface), equivalent-mutant triage, mapping survivors to the missing assertion, and
   "mutation score is an input, not the verdict" (mirrors the existing coverage-percentage rule, `:43-44`).
   A new skill would collide with `test-coverage-mapper`'s description phrase above (check 2) and restate
   its rubric (check 3) -> **make-it-an-extension**.
3. **Invocation:** extension reads reports it is given -> base stays **auto-invocable** (precedent
   `ci-failure-classifier:3` "Reads logs supplied ... fetches and reruns nothing"). Running a mutation tool
   rewrites code and runs suites -> MANUAL-ONLY, so the extension's Stop Condition must refuse to run one.
   Adoption/CI placement of a mutation tool stays with `qa-automation-architect` ("tool/runner selection per
   layer", description).
4. **Estimate:** 0.75–1.5 h (input row + rubric bucket + 2 eval cases; description has room: 866/1023 chars,
   measured). Basis: negative-path extension 0.75–1.5 (qa-tier1 proposal table), ai-sdlc :387.
5. **Value:** directly targets "tests that pass without proving behavior", a known failure mode of
   AI-written tests; cheap. P2. No in-repo demand found.
6. **Pin against:** `qa-automation-architect` (tool adoption), `vitest-unit-component-engineer` (writes/fixes the
   tests), `code-reviewer` (diff review).

### G2-3 `soak-test-planner` — COVERED

1. **Source:** cat06:53 "#207 Soak Test Planning | P2 | ... memory leaks, queue buildup, token expiry, and
   degradation."; v4:269.
2. **Overlap:** `load-test-planner:3` "test types chosen by the question (load-at-target, stress-to-break,
   soak, spike)" and "Use when planning load/stress/soak/spike testing"; `:25`, `:85-91` (endurance question
   "what leaks, drifts, or fills over hours"), Gotcha `:227-230` ("The soak test nobody watches ... names which
   resources the harness must trend"); `references/workload-model-worksheet.md:29` (soak/endurance row:
   "drift curves on NAMED resources (memory, pools, disk, queues)"). Two pinned trigger evals already route
   soak prompts to it: `load-test-planner/evals/trigger-evals.json:30` ("a soak overnight") and
   `performance-test-harness/evals/trigger-evals.json:21` ("a 12-hour soak"). Measurement:
   `performance-test-harness/SKILL.md:150` and harness sheet `:76`. **Residual:** "token expiry" — grep of both
   skills for `expir` -> 0 hits; time-based expiries (auth tokens, sessions, signed URLs, TTL caches) crossing
   during a long run are not named. Verdict **COVERED**; optional micro-extension (one worksheet row + one
   gotcha line; body only, because the description is at 1006/1023 chars, measured).
3. **Invocation:** planning only; executing a soak = load against an environment -> MANUAL-ONLY/person's act
   (`load-test-planner:241-245`).
4. **Estimate:** drop 0–0.25 h; optional micro-extension 0.25–0.5 h.
6. **Pins if extended:** existing `performance-test-harness`, `slo-reliability-architect` cases stay.

### G2-4 `chaos-test-planner` — COVERED

1. **Source:** cat06:54 "#208 Chaos Test Planning | P2 | Inject service failures, timeouts, retries, and partial
   outage scenarios safely."; v4:270.
2. **Overlap:** `resilience-architecture-reviewer:3` "a fault-injection or game-day plan to prove it ... Review
   only; runs no fault injection"; Use When `:68-69` ("planning a fault-injection experiment or a game day ...
   hypotheses, limits, abort criteria and a named human owner"); workflow step 7 `:158-163`;
   `references/resilience-review-sheet.md:99-115` (game-day template with hypothesis, steady state, fault,
   environment, blast-radius limit, abort criteria, rollback, approvals); pinned eval
   `evals/trigger-evals.json:94-101` "game-day-plan-wins-here". Scope was assigned on purpose: roadmap row
   "Review availability, failover, DR, dependency failure, backups, chaos tests, and rollback"
   (`docs/roadmaps/product-agnostic-skill-and-agent-roadmap.md:117`; phase6 proposal `:205-206`, boundary table
   `:239` "fault-injection plan | resilience-architecture-reviewer"). Test-layer fault injection:
   `integration-test-designer:89-90` ("failure modes of faked seams (provider timeout/error surfaced
   correctly)"); job retries: `background-job-orchestration-architect`. A new skill would collide with the
   pinned game-day eval. Verdict **COVERED**.
3. **Invocation:** any executing chaos skill is MANUAL-ONLY (§1); resilience Security Rules `:231-234` make
   execution "a person's act" across `human-approval-boundary`.
4. **Estimate:** 0–0.25 h (record only).

### G6-1 `e2e-test-architect` — COVERED (composition)

1. **Source:** `docs/roadmaps/product-agnostic-skill-and-agent-roadmap.md:147` "P0 | Select critical journeys
   for E2E and define tags, data, roles, tenants, CI placement, and artifacts."; execution plan
   `docs/prompts/senior-principal-claude-skills-execution-plan.md:419`; v4:196.
2. **Overlap, element by element:** journey selection + why-E2E — `playwright-e2e-engineer:61-73` (small
   critical list, smoke vs nightly choice), `qa-strategy-architect:3` (test-layer split, CI gate placement);
   tags/tiers — `regression-suite-curator:3` (smoke/PR/full/nightly tiers, quarantine tags); data/roles/tenants
   — `test-data-architect:3` ("API-created fixtures for E2E", personas, tenants, roles), `test-tenant-provisioner`;
   CI placement + artifacts — `qa-automation-architect:3` ("auth-state handling ... reporting/artifact
   conventions, CI pipeline placement (what runs on PR vs merge vs nightly, sharding, retry policy)"),
   `test-plan-designer:3` ("named artifacts, and CI placement"), `playwright-e2e-engineer:88-99`. Role
   matrix -> G1 `role-based-qa-matrix` (#229). A new description would overlap at least four shipped
   descriptions (check 2 FAIL). Verdict **COVERED**.
4. **Estimate:** 0–0.25 h (record only).

### G6-2 `qa-closeout-reporter` (#235) — COVERED

1. **Source:** cat06:81 "#235 QA Closeout Report | P0 | Summarize tests run, evidence, skips, failures, risks, and
   recommended release decision."; v4:197-198 ("overlaps `ai-closeout-reporter` + `screenshot-evidence-planner`;
   keep as backlog to avoid trigger overlap").
2. **Overlap:** `ai-closeout-reporter:3` (tests and validation actually run, evidence, known skips, risks,
   skipped checks), body `:61-65` (per-surface pass/fail table, negative-path table, skips decomposed by
   reason); the release decision is `release-readiness-reviewer:3` (go/no-go on evidence). Two pinned evals:
   `screenshot-evidence-planner/evals/trigger-evals.json:21` ("closeout-goes-to-ai-closeout-reporter", prompt
   "Write the end-of-release report summarizing what was tested ...") and
   `ai-closeout-reporter/evals/trigger-evals.json:63-64` ("closeout-bundling-evidence-wins-here", "The release test
   pass is finished ... Write the closeout"), plus `:84-88` routing go/no-go to `release-readiness-reviewer`.
   Verdict **COVERED**; building it would break two pinned evals.
4. **Estimate:** 0–0.25 h (record only).

### G6-3 #224 Bug Report Authoring + #225 QA Triage Facilitation — PARTIAL -> one new skill

1. **Source:** cat06:70 "#224 ... P1 | Document reproduction steps, expected result, actual result, environment,
   logs, and suspected area."; cat06:71 "#225 ... P1 | Prioritize bugs by severity, frequency, customer impact,
   security risk, and release impact." Untiered (v4:274-275).
2. **Overlap:** `clickthrough-test-engineer:73-74`, `:92` files defects with severity + repro steps + evidence,
   but only inside its own MANUAL-ONLY session. `manual-test-case-creator` has verdict rules only
   (`:72` "fail = cite the first failing step + capture evidence"; grep `defect|bug` in it -> 0 hits).
   `prioritization-frame-picker:53-55` lists "bugs" as a rankable object but owns frame selection, not a defect
   severity/priority rubric. `incident-response-runbook:68` owns the SEV ladder for production incidents.
   `systematic-debugger` (manual-only) and agent `senior-troubleshooting-lead.md:3` ("Use to triage a bug ...
   drive to root cause") own diagnosis and *consume* repro steps (`:29-30` "do not fabricate a repro").
   `regression-suite-curator` uses a severity threshold but defines none. grep `bug report|defect report|
   steps to reproduce|bug triage` across skills -> no owner. **Gap:** an auto-invocable owner for (a) writing a
   reproducible, redacted bug report from an observed failure, with an explicit "repro verified / unverified"
   flag, and (b) per-defect severity vs priority, duplicate detection, release-impact mapping (blockers handed
   to `release-readiness-reviewer`), and routing security defects to the private path (`SECURITY.md:16-18`
   "report security issues privately ... Do not open a public issue"). Verdict **PARTIAL**, residual large
   enough for one skill (merging #224+#225 follows D10's merge-not-multiply rule, v4:991-993).
   **Collision risk:** the word "triage" in `senior-troubleshooting-lead`'s description; the new skill must say
   "severity/priority classification", not root-cause triage.
3. **Invocation:** drafts the report and the classification as text; filing into a tracker would be a network
   write -> MANUAL-ONLY, so the skill files nothing -> **auto-invocable** (precedent `ci-failure-classifier`,
   `acceptance-criteria-reviewer`).
4. **Estimate:** 3–4.5 h (new read-only skill; above the 2.5–4 precedent band because it needs seams to
   ~6 neighbors and a severity reference sheet). Low confidence.
5. **Value:** daily work for any SaaS team and for nontechnical owners (P1 x2); fits the library's
   "report the gap, never fill it" rule (fabricated repros). No in-repo demand found.
6. **Trigger boundary:** use when writing up an observed defect for someone else to reproduce, or deciding how
   severe/urgent reported defects are and which block a release; not when finding the cause
   (`systematic-debugger`, agent `senior-troubleshooting-lead`), ranking a mixed feature+bug portfolio
   (`prioritization-frame-picker`), classifying a live incident (`incident-response-runbook`), deciding
   ship/no-ship (`release-readiness-reviewer`). **Pin against:** `prioritization-frame-picker`,
   `incident-response-runbook`, `release-readiness-reviewer`. A case routing root-cause work to the
   manual-only `systematic-debugger` must start `Explicitly invoke systematic-debugger. ` (standard :574-576).
   Name is provisional (e.g. `defect-report-triager`); the plan author chooses.

### G6-4 #188 Production-Safe Smoke Testing — PARTIAL -> extension of `synthetic-monitoring-architect`

1. **Source:** cat06:34 "#188 ... P0 | Run safe checks against production without creating unsafe records or using
   fixture-only routes." The only P0 untiered row with a residual gap.
2. **Overlap:** `synthetic-monitoring-architect:3` (scheduled probes, "a HARD prod-safety contract (probes never
   mutate real data, never leak test fixtures, use ring-fenced synthetic accounts, self-clean)"), body `:81-96`;
   it is explicitly *scheduled/ongoing* (`:3` "ongoing", "on a schedule" `:30-32`). One-shot post-deploy smoke:
   `merge-is-deploy-governance:103-105` classifies post-merge smoke as verification (does not design the set);
   `playwright-e2e-engineer:95-99` places post-merge smoke (MANUAL-ONLY, never auto-routed);
   `data-migration-runbook-author:151-154` covers post-apply smoke for migrations only.
   `test-tenant-provisioner` lints the opposite risk (automation reaching production). **Gap:** no
   auto-invocable owner designs the *post-deploy* production-safe smoke set; the natural home is the skill that
   already owns the prod-safety contract. Which skill a "design our post-deploy production smoke checks" prompt
   reaches today is **unverified** (no routing run).
3. **Invocation:** design only; running against production stays a person's act
   (`synthetic-monitoring-architect:196-200`) -> base stays auto-invocable.
4. **Estimate:** 1–2 h; the description is at 985/1023 chars (measured), so adding the post-deploy mode needs a
   reword, plus trigger-eval re-pins. Basis: ai-sdlc extension rows 1–2 (`ai-sdlc-skill-batch-proposal.md:301`).
6. **Pin against:** `merge-is-deploy-governance`, `release-readiness-reviewer`, and `playwright-e2e-engineer`
   (manual-only, so a case expecting it must start `Explicitly invoke playwright-e2e-engineer. `, standard :574-576).

### G6-5 #231 Timezone QA, #232 Notification QA (and #233/#234) — PARTIAL-minor / COVERED

- **#233 Import QA (P1) COVERED:** `test-plan-designer/evals/evals.json:9` is a pinned positive case "Write the test
  plan for our new CSV import feature — upload, mapping preview, confirm, and failure recovery" (the #233 text
  almost verbatim), and `qa-strategy-architect/evals/evals.json:50` routes the same prompt away.
- **#234 Export QA (P2) COVERED by composition:** per-feature plan `test-plan-designer`; isolation of exports
  `multi-tenant-security-tester:51`, `:123`; export audit events `audit-log-architect:78`; file export via
  short-lived signed URLs `file-upload-storage-architect:3`, `:37`.
- **#231 Timezone QA (P1) PARTIAL-minor:** only the boundary line `test-plan-designer/references/test-plan-template.md:13`
  ("date/timezone edges"), plus scattered owners: `background-job-orchestration-architect:124`, `:180` (timezone/DST
  scheduling), `notification-webhook-ux-designer:85` (quiet hours), `environment-parity-reviewer:265`,
  `flaky-test-detective:153` (time bombs), `vitest .../vitest-patterns.md:56`. No multi-zone test matrix
  (tenant/user zones x reports' day boundaries x reminders across DST).
- **#232 Notification QA (P1) PARTIAL-minor:** `notification-webhook-ux-designer:3` designs channels, preferences,
  digests and "opt-out that truly stops the messages"; `api-event-architect` owns retry/at-least-once. No QA
  checklist for verifying them (test inbox/SMS/push sandbox, unsubscribe proof, duplicate-on-retry).
- **Form:** both are per-feature plans that already route to `test-plan-designer`; an optional reference sheet
  ("time-and-timezone" and "notification" surface checklists) would close them without a new skill.
  Estimate 1–1.5 h. Pin: `qa-strategy-architect`, `notification-webhook-ux-designer`,
  `background-job-orchestration-architect`.

### G6-6 #213 Test Timeout Policy, #202 Snapshot Governance — PARTIAL-minor, route to G1

- **#213 (P1):** classification exists (`ci-failure-classifier:3`, `:105-108`, refusal `:246-248`), stage timeouts in
  `ci-pipeline-architect:83` (manual-only), widening rule `flaky-test-detective/references/flake-taxonomy.md:57`,
  resume `sharded-validation-with-resume`. `grep -c -i timeout` in `qa-automation-architect` SKILL.md and its
  reference -> 0 and 0: no per-layer timeout-setting policy.
- **#202 (P2):** "No snapshot-everything" `vitest-unit-component-engineer:70`; theater signal
  `test-coverage-mapper/references/coverage-mapping-method.md:32`; update review
  `change-classification-gate/SKILL.md:118-119` and `references/classification-matrix.md:46` ("Confirm the
  behavior change was intended before updating snapshots"). `grep -c -i snapshot` in `qa-automation-architect` -> 0.
  Missing: the positive "when a snapshot is appropriate" policy.
- **Recommendation:** do not plan these in G2/G6. #213 sits on G1 `ci-shard-parallel-isolation` ("Extends
  `qa-automation-architect`'s blueprint into enforceable rules", v4:261); #202 sits next to G1
  `visual-regression-test-designer` (#203, baselines with reviewable diffs). Two helpers proposing edits to
  `qa-automation-architect` would collide; the coordinator should hand both rows to the QA-A (G1) plan.
  If kept here: one `qa-automation-architect` extension, 0.75–1.5 h.

### G6-7 Covered untiered rows (record only)

| Row (priority) | Owner evidence |
|---|---|
| #189 Fixture Mode E2E (P1) | catalog `:523` maps it to `playwright-e2e-engineer`; that skill rejects breadth at E2E (`:61-63`) and treats test-only routes as a separate classified change (`:157-158`); breadth/mocking is G1 (#200/#201, #203). |
| #191 Golden Path Mapping (P1) | catalog `:521` `test-coverage-mapper` (#191/#192); smoke members need "a named critical-journey reason" (`regression-suite-curator:126`). |
| #193 Boundary Value (P1) | `test-plan-designer/references/test-plan-template.md:13`; `vitest-unit-component-engineer:60-62`; `acceptance-criteria-reviewer:107-110`; `test-data-architect/references/test-data-patterns.md:52-53`. |
| #199 Test Cleanup (P1) | catalog `:530` (#196–#199); `test-data-architect:3` "cleanup/TTL and traceability rules"; patterns `:55` "TTL & traceability". |
| #216 GitHub Actions Evidence Review (P0) | `release-readiness-reviewer:74-77` (enumerate required checks on the exact tree), `:154-156`; `ci-failure-classifier:3` (green-run hidden markers), eval list `:265` (skipped required job). |
| #217 Local Validation (P0) | `local-ci-mirror-preflight:3` (manual-only, "mirror the repository's CI locally"); catalog `:528` maps #217 to `vite-build-qa-engineer`. |
| #218 Docs-Only Validation (P0) | `risk-tiered-validation-selector:3` ("docs-only fast path ... explicit docs-only definition PLUS a 'never docs-only' list"). |
| #219 Backup-Gated Validation (P0) | `data-migration-runbook-author:118-122` (verified backup prerequisite), `:126`, `:151-154` (smoke); `database-backup-verifier` (manual-only). Storage-policy changes are not named explicitly (minor, unverified gap). |
| #220 Deployment-Gated Validation (P1) | `merge-is-deploy-governance:103-105`; `playwright-e2e-engineer:95-99`; `release-readiness-reviewer:74-77`. |
| #233, #234 | see G6-5. |

## 5. Estimate basis (why every figure is low confidence)

- **No measured active time exists for any skill build.** `grep -c "active time not measured"
  docs/roadmaps/aegis-execution-metrics.md` -> 146; the D68 build PRs have only wall time, open-to-merge
  (REST `pulls/{n}` created_at/merged_at): #498 3:54:17, #499 3:16:02, #500 3:45:55, #502 4:12:36 — these
  include review waits and parallel lanes, so they do not measure active effort.
- **Precedent agent estimates** (the only basis): new read-only skill 2–4 h (`qa-tier1-skill-batch-proposal.md`
  table: ci-failure-classifier 2.5–4, acceptance-criteria-reviewer 2–3.5; ai-sdlc `:206` 2.5–4; phase6 `:287`
  3–4.5, `:457` 2.5–4); extension 0.75–2 h (qa-tier1 negative-path 0.75–1.5; ai-sdlc `:301` 1–2, `:387`
  0.75–1.5; phase7 `:173` 1–2); drop 0–0.25 h (qa-tier1, ai-sdlc `:441`, phase7 `:452`); batch overhead 1–3.5 h
  (ai-sdlc `:70` 1–2, phase7 `:71` 1.5–2.5, qa-tier1 1.5–3, phase6 `:80` 2–3.5).
- **Against the forecast:** G2 is forecast at 8–16 h and G6 at 2–8 h (`aegis-backlog-forecast.md:727`, `:731`;
  sum 10–24). If all G2+G6 items were done in their recommended *form*: PBT 2.5–4 + mutation ext 0.75–1.5 +
  soak drop/micro 0.25–0.75 + chaos drop 0–0.25 + e2e/closeout drops 0–0.5 + defect skill 3–4.5 + #188 ext 1–2
  + #231/#232 ext 1–1.5 + records 0.5–1 + overhead 1.5–3 = **10.5–19 h** (excluding #213/#202, routed to G1).
  The lower-than-forecast new-skill count follows the precedent pattern (drops and extensions replace skills).

## 6. Recommendation

**Ranking method** (`prioritization-frame-picker`, value-vs-effort, buckets): value = roadmap priority
(evidence: cat06 labels, but cat06:15-17 warns a label is an original planning tier, not demand) x
residual-gap size (evidence: §4 overlap findings); effort = §5 (guess). Must-do lane: none (no compliance or
security item here). Sensitivity: doubling any single effort estimate does not change which items are drops;
it can reorder the two smallest extensions only.

**Recommended sub-batch (5 items): "QA residual-gap closure"**

| Item | Row(s), priority | Form | Invocation | Est. (h) |
|---|---|---|---|---:|
| 1 | #224 + #225 (P1, P1) | BUILD one new skill (defect report + severity/priority classification) | auto-invocable | 3–4.5 |
| 2 | #188 (P0) | EXTEND `synthetic-monitoring-architect` with a post-deploy production-safe smoke mode | stays auto | 1–2 |
| 3 | #195 (P2) | EXTEND `test-coverage-mapper` with mutation-report evidence | stays auto | 0.75–1.5 |
| 4 | #207 (P2) residual | EXTEND `load-test-planner` body: time-based expiries in soak runs | stays auto | 0.25–0.5 |
| 5 | #207, #208, #235, `e2e-test-architect`, #189, #191, #193, #199, #216–#220, #233, #234 | RECORD as covered (drops), in the build's decision row and the D10 "Already covered" table, adding the missing #189 catalog mapping to the v4 absorbed list by a dated note | n/a | 0.5–1 |
| — | batch overhead (registration, decision row, reciprocity edits, reviews) | | | 1.5–2.5 |
| | **Total: 1 new skill, 3 extensions, ~16 rows recorded covered** | | | **7–12** |

**Why this set:** it is the only arrangement that addresses the one P0 row with a real residual (#188) and
the two P1 rows with the largest unowned residual (#224/#225), at low cost, while the G2 candidates are mostly
already owned (soak, chaos) or fit as an extension (mutation). It also clears the backlog of rows that are
already covered, which the forecast still counts as 2–8 + 8–16 h of candidates.

**Alternatives:**
- **B. Add `property-based-test-designer`** (+2.5–4 h -> 9.5–16 h, 6 items). The only genuinely NEW skill in
  G2/G6, but P2 and under D10's "build on demand only" (v4:263; v4:272-273 also allows "after the core
  phases (7, 7.5)", which catalog `:1367`, `:1389` show as implemented). Choose it if the owner wants a new
  test-design capability rather than gap closure.
- **C. Add the #231/#232 checklist extension to `test-plan-designer`** (+1–1.5 h). Small P1 value; per-feature
  plans already route there (import case pinned).
- **D. "None" from G2/G6** and spend the batch on another group: defensible because no candidate has in-repo
  demand evidence; the recording item (5) alone would still clean the backlog (0.5–1 h + overhead).

**Cross-lane hand-offs for the coordinator:** #213 and #202 go to the G1 (QA-A) plan (§4.G6-6); #189's
mocking/breadth question overlaps G1 `mock-strategy-designer` (#200/#201) and `visual-regression-test-designer` (#203).

## 7. Self-scrutiny

- **Strongest counter-argument.** Item 1 is a new skill on rows D10 deliberately left untiered, and its
  ground is crowded: `prioritization-frame-picker` already lists bugs as a rankable object, clickthrough already
  files defects, and the `senior-troubleshooting-lead` agent owns "triage" in its description. A reviewer
  could call it a collision (check 2) and say "bugs are ranked by prioritization-frame-picker; repro is
  systematic-debugger's input". If a trigger-eval run showed bug-write-up prompts already land cleanly on an
  existing skill, item 1 should shrink to an extension of `prioritization-frame-picker` (a defect severity
  reference sheet) or be dropped.
- **Second counter-argument.** Ranking by P0/P1/P2 leans on 2026 planning labels that the category page says
  are not demand (cat06:15-17); G2's P2 items (PBT, mutation) may matter more for AI-written code than their
  label suggests. That argues for alternative B.
- **Least certain claims.** (a) All estimates (§5: no measured active time). (b) Routing claims are from
  reading descriptions and pinned evals, not from a routing run; in particular, where a "post-deploy production
  smoke" prompt lands today is unverified. (c) The #188 extension's fit inside a 985-character description
  needs an actual reword to prove. (d) "Storage-policy changes not named" under #219 is a grep result, not a
  body-wide read of every storage skill. (e) Demand: none found in-repo; not used as support either way.
- **What would change the recommendation.** DEMAND-helper evidence for property-based or mutation testing
  (-> alternative B); a routing/trigger-eval run showing defect prompts route cleanly today (-> drop item 1);
  the owner preferring new skills over extensions; the QA-A plan claiming `test-coverage-mapper` or
  `synthetic-monitoring-architect` edits (-> merge or re-sequence items 2–3); MECH-helper measured costs that
  change the per-item bands.
