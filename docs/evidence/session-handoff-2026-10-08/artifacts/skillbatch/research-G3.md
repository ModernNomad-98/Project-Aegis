# Research G3 — Phase 2 expansion (nine candidates)

Stage A support only (planning research). Writes no repo file, makes no commit, no GitHub write.

- **Base:** `origin/main` = `5228977920ee479e1fe1ec6b8d56f8fc24c14947` (`git ls-remote origin refs/heads/main`, re-run 17:24:09Z).
  Read from a fresh `git archive 52289779 | tar -x` into `$S/skillbatch/g3-tree` (the earlier partial trees were not trusted).
  Role A confirmed there: `README.md` line 1 `# Project Aegis`; `docs/skills-catalog.md`, `scripts/validate-skills.py`,
  `artifacts/audits/skill-contract-audit-baseline.json` all present. `python3 -B scripts/validate-skills.py` on that tree:
  `OK: 195 skill(s) valid, 0 warning(s)`; `.claude/skills/` has 196 entries (195 skills + `_template`); 30 carry
  `disable-model-invocation: true` (my `yaml.safe_load` script `$S/skillbatch/g3-scripts/desc.py` → `$S/skillbatch/g3-desc.json`).
- **Aegis skills used (dogfood):** `skill-quality-reviewer` — its check 2 (trigger collision, `SKILL.md:79-84`) and check 3
  (extension vs separate skill, `references/quality-review-checklist.md:91-106`) are the overlap criteria applied below;
  `prioritization-frame-picker` — value-vs-effort buckets, must-do lane, sensitivity check (`SKILL.md` Workflow steps 1–6)
  for the sub-batch choice. Neither is MANUAL-ONLY (`g3-desc.json`: `dmi` = None for both).
- **Group membership source (the set-defining artifact):** `docs/skills-catalog.md:1300-1304` (the nine names, "remains backlog,
  built in Phase 8 batches"), from `docs/reconciliation/step-0-reconciliation-v4.md:123-128`. Forecast row
  `docs/roadmaps/aegis-backlog-forecast.md:728` "Phase 2 expansion (nine skills) | 18–36". The names come from the execution
  plan (`docs/prompts/senior-principal-claude-skills-execution-plan.md:351-356, 373-377`), not from the roadmap tables; I
  mapped each to roadmap rows by topic (cited per candidate).
- `grep -rn` for all nine names over `.claude/`, `scripts/`, `tests/` returned nothing: no shipped skill names any of them
  as a seam today.

## Summary table

| # | Candidate | Source rows (priority) | Verdict | Nearest shipped owner(s) | Recommendation | Invocation | Est. active h (low confidence) |
|---|---|---|---|---|---|---|---:|
| 1 | `observability-by-design` | cat01 #22 P0 (`docs/skills/01-…:45`); cat04 #160 P1 (`04-…:54`); cat07 #252 P1 (`07-…:43`) | **PARTIAL** — design half missing | `observability-operator` (MANUAL-ONLY, implements), `slo-reliability-architect` (SLO/alert design) | **BUILD** | auto-invocable (design only) | 3–5 |
| 2 | `validation-boundary-designer` | cat01 #37 P0, #38 P0 (`01-…:60-61`); cat04 #141 P0, #157 P0 (`04-…:35, 51`) | **PARTIAL** — layered placement missing | `command-gateway-architect` (one layer), `error-taxonomy-designer` (error shape), `domain-modeler` (invariants named) | **BUILD** | auto-invocable | 3–5 |
| 3 | `idempotency-first-designer` | cat01 #17 P0 (`01-…:40`); cat04 #144 P0 (`04-…:38`); D30 "TOP pull-forward" (reconciliation `:745-749`, `:1328`) | **PARTIAL** — core shipped | `command-gateway-architect` (owns key/store/replay + the trigger) | **MERGE** into `command-gateway-architect` | n/a (base auto-invocable) | 1–2 |
| 4 | `api-contract-designer` | cat01 #9 P0 (`01-…:32`); cat04 #133/#134 P1 (`04-…:27-28`) | **PARTIAL** — per-operation schema missing | `api-event-architect` (conventions/versioning), `error-taxonomy-designer`, `pagination-cursor-designer` | **MERGE** into `api-event-architect` (optional in this batch) | n/a (base auto-invocable) | 1–2 |
| 5 | `refactor-safety-planner` | cat01 #11 P0 (`01-…:34`); #45 P1, #46 P2 (`:68-69`) | **PARTIAL** — catalog itself says only "adjacent" | `code-simplifier` (MANUAL-ONLY, small-scale, edits), `architecture-designer` (structural migration plan) | **BUILD later** (next batch) | auto-invocable (plan only) | 3–4.5 |
| 6 | `dependency-direction-guard` | cat01 #7 P0, #6 P0 (`01-…:29-30`); #50 P1 (`:73`) | **PARTIAL** — enforcement/ratchet missing | `architecture-designer` (states directions), `code-reviewer` (diff drift), `principal-architecture-reviewer` agent | **DEFER**; reconcile with unlisted `code-quality-auditor` first | auto-invocable (design/review) | 2.5–4.5 |
| 7 | `operational-runbook-author` | cat01 #23 P1 (`01-…:46`) | **COVERED** (small residual) | `incident-response-runbook`, `rollback-runbook-author`, `data-migration-runbook-author`, `gated-deployment-prompt-template`, `onboarding-doc-designer` | **DROP** (record as covered) | n/a | 0–0.25 |
| 8 | `system-context-mapper` | cat01 #2 P0 (`01-…:25`) | **COVERED** | `architecture-designer` (+ references), `threat-modeler`, `domain-modeler` | **DROP** | n/a | 0–0.25 |
| 9 | `bounded-context-identifier` | cat01 #4 P0 (`01-…:27`) | **COVERED** | `domain-modeler` step 4 | **DROP** | n/a | 0–0.25 |

Batch overhead (registration, decision row, reciprocity edits, reviews): 1.5–3.5 h (precedent range, see Estimates).

**Recommended sub-batch (6 dispositions):** BUILD #1 and #2, MERGE #3, DROP #7, #8, #9 — **8.5–16.25 provisional active hours**
(3–5 + 3–5 + 1–2 + 0–0.75 + 1.5–3.5, summed by `python3 -I -c`). Library would go 195 → 197 skills.

---

## Per-candidate evidence

Paths are repo-relative at `52289779`. "Desc" = the shipped `description` as parsed by `yaml.safe_load`.

### 1. `observability-by-design` — PARTIAL → BUILD

1. **Source:** cat01 #22 "Observability-by-Design | P0 | Add correlation IDs, structured logs, metrics, traces, and diagnostic
   context from the beginning" (`docs/skills/01-software-architecture-engineering.md:45`); cat04 #160 Backend Observability
   Hooks P1 (`docs/skills/04-backend-api-data-engineering.md:54`); cat07 #252 Log Taxonomy Design P1
   (`docs/skills/07-devops-release-reliability.md:43`). Execution plan: "Observability/runbook skills must produce durable
   operational evidence" (`docs/prompts/senior-principal-claude-skills-execution-plan.md:708`).
2. **Overlap.** `observability-operator` desc (verbatim start): "MANUAL-ONLY; never auto-invoke. Operate the observability stack
   hands-on — instrument services (structured logs with correlation IDs, tenant context, redaction before emission; metrics;
   traces) … EDITS LIVE ALERT/DASHBOARD CONFIG AND EXECUTES OPERATIONAL QUERIES — manual invocation only." Catalog sources it
   from cat07 #246/#247/#248/#252 (`docs/skills-catalog.md:589`). It is `disable-model-invocation: true` (`SKILL.md:4`).
   Its own Inputs assume a design may or may not exist: "The log taxonomy if one exists … extend it, don't fork it"
   (`observability-operator/SKILL.md:50-51`). `slo-reliability-architect` designs SLIs/SLOs and paging ("Produces the SLO catalog
   and alert spec that observability-operator implements"), not the telemetry schema. `security-logging-alerting-architect`
   covers security detection events only; `audit-log-architect` audit records; `product-analytics-instrumenter` product
   analytics ("NOT system telemetry for engineers (observability-operator)"). `error-taxonomy-designer` puts a correlation id
   in the error envelope (13 telemetry-term hits, `grep -c`), not propagation.
   **Remaining gap:** no auto-invocable skill designs, at feature-design time, the telemetry contract — log event taxonomy and
   required fields, correlation/trace-context propagation across sync and async hops (request → queue → job → webhook),
   per-boundary RED/USE metrics, tenant tagging under a cardinality budget, redaction-at-source rules, diagnostic context.
   `project-orchestrator` routes observability only at Stage 8, to `slo-reliability-architect` → `observability-operator
   (manual-only)` (`project-orchestrator/SKILL.md:264-277`); Stage 3 design (`:238`) and Stage 5 planning name no observability
   skill (`grep -n -i observab project-orchestrator/SKILL.md` → only `:275`, `:436`). Library rule for a separate skill: the output
   differs in kind and the base would need a new Output Format (`quality-review-checklist.md:104-106`); extending the
   manual-only operator would not make design auto-invocable, and extending `slo-reliability-architect` would change its
   Purpose (journeys → SLOs).
3. **Invocation:** design only → auto-invocable under `docs/skill-generation-standard.md:270-275` (read-only default; manual-only
   is required only for write/network/deploy/spend). Must hand implementation to `observability-operator` by name, per the
   orchestrator's manual-only routing invariant (`project-orchestrator/SKILL.md:284`).
4. **Estimate:** 3–5 h (precedent: new design skills at 3–5 h, `phase7-…-proposal.md:68`, `phase6-…-proposal.md:75,79`); upper
   end because it seams with six neighbors. Low confidence (see Estimates).
5. **Value/dependencies:** P0 in the roadmap; fills the design-time hole the orchestrator map shows. Composes
   `slo-reliability-architect` (consumes SLIs), `error-taxonomy-designer` (correlation id in envelope),
   `latency-budget-architect` (span/budget annotation, `latency-budget-architect/SKILL.md:171`). Cross-group seam: G5's
   "logging redaction" topic, cat03 #124 Logging Redaction Review P0 (`docs/skills/03-saas-security-rls.md:66`) — decide which
   owns redaction rules. Optional follow-up: an orchestrator route (precedent `#384`, a separate PR; not estimated).
6. **Trigger boundary:** use when designing what a new feature/service must emit (log fields, correlation propagation, metrics,
   trace spans, tenant tags, redaction) before or during build, or when a service is undiagnosable because telemetry was never
   designed. Not when: wiring/editing live instrumentation, dashboards or alerts (`observability-operator`, manual-only);
   setting SLOs or deciding what pages (`slo-reliability-architect`); security detection coverage
   (`security-logging-alerting-architect`). **Trigger-eval pins:** `observability-operator` (with the `Explicitly invoke
   observability-operator. ` prefix, standard `:574-576`), `slo-reliability-architect`, `security-logging-alerting-architect`.
   **Name note:** `observability-by-design` vs `observability-operator` share a first word; `skill-quality-reviewer` treats
   near-miss names as CONCERN by closeness (`quality-review-checklist.md:86-89`). Owner question at build.

### 2. `validation-boundary-designer` — PARTIAL → BUILD

1. **Source:** cat01 #37 Validation Boundary Design P0 "Place validation at API, command, form, database, and integration boundaries
   without relying on one layer" (`01-…:60`); #38 Invariant Enforcement P0 (`:61`); cat04 #141 Validation Schema Design P0 (`04-…:35`);
   #157 Data Integrity Constraint Review P0 (`04-…:51`). Execution plan: "API/idempotency/validation skills must handle … validation
   layers, and safe errors" (`execution-plan.md:707`). Reconciliation lists it as a backlog component seam of
   `command-gateway-architect` (`step-0-reconciliation-v4.md:639-640`).
2. **Overlap.** `command-gateway-architect` validates one layer: "**Validate** the payload against a schema (shape, types, required,
   bounds) — reject malformed input before any authz work" (`command-gateway-architect/SKILL.md:80-81`). `error-taxonomy-designer`
   owns field-level error details. `domain-modeler` names "the invariant each aggregate protects" (`domain-modeler/SKILL.md:62-63`)
   but stops at a model. `structured-output-validator` is LLM output only. `appsec-implementer` (MANUAL-ONLY) implements "a named,
   already-decided" control "such as input validation". `grep` over all `SKILL.md`: no hit for DB integrity constraints
   (NOT NULL / CHECK / FK / unique as a validation backstop) and none for unknown-field / mass-assignment / over-posting policy.
   **Remaining gap:** the end-to-end placement design — which rule is enforced at which layer (form = UX only; API edge = shape and
   size; command/domain = business invariants; database constraints = last line; inbound integration payloads parsed, never
   trusted), shared vs boundary-specific schemas, unknown-field policy, normalization before validation, and an
   invariant → enforcement-point → negative-test matrix. Output differs in kind from the gateway's pipeline contract →
   separate skill under `quality-review-checklist.md:104-106`.
3. **Invocation:** design only → auto-invocable (`skill-generation-standard.md:270-275`).
4. **Estimate:** 3–5 h (same precedent as #1). Low confidence.
5. **Value/dependencies:** four P0 rows across two categories; currently the only DB-constraint coverage is none (grep).
   Cross-group dependency: G5 "CSRF/XSS/SQLi deep-dives" (cat03 #111 P0, #112 P0, `03-…:53-54`) — injection defense is output
   encoding/parameterization, not input validation, but a G5 build could claim "validate input"; decide G2/G5 seams together.
   Reciprocity edit on `command-gateway-architect` (desc 944 chars; 80 chars of room) — same file as #3, so sequence or combine.
6. **Trigger boundary:** use when deciding where validation and invariants are enforced across layers, unifying scattered
   validation, or after a bug where one layer was trusted. Not when: designing the write pipeline (`command-gateway-architect`),
   the error envelope (`error-taxonomy-designer`), LLM output schemas (`structured-output-validator`), or implementing one named
   control (`appsec-implementer`, manual-only). **Pins:** `command-gateway-architect`, `error-taxonomy-designer`,
   `structured-output-validator`.

### 3. `idempotency-first-designer` — PARTIAL → MERGE into `command-gateway-architect`

1. **Source:** cat01 #17 Idempotency-First Design P0 "Prevent duplicate side effects from retries, double-clicks, webhook replays, and
   automation reruns" (`01-…:40`); cat04 #144 Idempotency Key Middleware P0 "request keys, payload hashes, actor scope, and terminal
   response replay" (`04-…:38`). D30 named it the "TOP pull-forward … table-stakes for any mutating API" (`step-0-reconciliation-v4.md:745-749`,
   repeated `:1328`). Of the three D30 pull-forwards, `resilience-architecture-reviewer` shipped (catalog `:593`), rate-limit design
   is a G5 topic (catalog `:1323-1324`), and this one remains.
2. **Overlap.** D31 built `command-gateway-architect` (reconciliation `:1334-1337`), which now owns the core and the trigger:
   "Use when: retries or double-submits cause duplicate side effects and the write path has no idempotency contract"
   (`command-gateway-architect/SKILL.md:40-41`); "Design idempotency concretely. Key source …, the dedup store and its retention, what
   'same request' means, and the response for a replayed key. Distinguish idempotency (safe replay) from concurrency control"
   (`:104-108`); gotchas on body-keyed dedup and idempotency-vs-concurrency (`:176-181`); refusal of unqualified exactly-once
   (`:200-203`). Elsewhere: `api-event-architect` "retried requests return the original result within a stated window" (`:91-94`);
   job idempotency (`background-job-orchestration-architect` desc); idempotent consumers (`streaming-event-architect` desc);
   client-id idempotency (`offline-first-sync-architect` desc); idempotent cost entries (`usage-metering-…` desc).
   `grep -c -i idempoten` ranks the gateway 16 and background jobs 17 hits.
   **Collision:** a standalone skill's core trigger equals the gateway's Use When at `:40-41` — a check-2 FAIL "when the loser would
   fire on the winner's core case" (`skill-quality-reviewer/SKILL.md:79-84`).
   **Remaining gap (grep-verified absent):** same key with a different payload (fingerprint mismatch → reject); a concurrent
   in-flight duplicate of the same key (lock or "in progress" response); propagating the key to third-party side effects
   (payment/email providers) and an outbox for at-least-once effects (the gateway's only "outbox" use is for audit, `:173-175`).
   These fit the gateway's fixed pipeline without a new Output Format (its output already has
   `Idempotency: <key source, dedup store, replay response, concurrency control>`, `:136`) → extension rule
   (`quality-review-checklist.md:101-103`).
   **Left out on purpose:** inbound third-party webhook dedup — no shipped skill covers it (`grep` for inbound/incoming webhook,
   webhook intake: no hits); it belongs with G5's cat03 #116 Webhook Security Design P1 ("signatures, replay protection,
   idempotency", `03-…:58`) or cat04 #145 Webhook Intake Pipeline P1 (`04-…:39`).
3. **Invocation:** base stays auto-invocable (desc has no sentinel; `dmi` None).
4. **Estimate:** 1–2 h (precedent extensions 1–2 h: `phase7-…:66`, `phase6-…:77`). Body-only change is possible; the description has
   80 chars of room. Low confidence.
5. **Value:** highest value per hour in the group (two P0 rows plus the D30 pull-forward), cheap because the core exists.
6. **Trigger boundary:** unchanged gateway triggers; add trigger-eval cases for payload-mismatch and in-flight duplicates.
   **Pins:** `background-job-orchestration-architect` (job reruns), `streaming-event-architect` (consumer dedup),
   `api-event-architect` (public-API window).

### 4. `api-contract-designer` — PARTIAL → MERGE into `api-event-architect` (optional)

1. **Source:** cat01 #9 API Contract Design P0 "Define request and response schemas, validation, error shapes, compatibility, and
   versioning strategy" (`01-…:32`); cat04 #133 REST API Design P1, #134 RPC API Design P1 (`04-…:27-28`).
2. **Overlap.** `api-event-architect` desc: "Design external application programming interface (API) and event contracts for
   multi-tenant software as a service (SaaS) … Define routes, versioning, idempotency, rate limits, and signed tenant-scoped webhook
   delivery … Use for public API or webhook design and partner contract changes." Body: resource conventions (naming, ids,
   pagination, error shape, 404-vs-403, `:86-90`), versioning/deprecation (`:99-117`); Use When includes "imposing conventions on one
   that grew endpoint by endpoint" (`:30-31`). Error shapes → `error-taxonomy-designer`; pagination → `pagination-cursor-designer`
   ("Owns pagination mechanics within the endpoint contract owned by api-event-architect"); compatibility tests →
   `api-contract-test-designer`; reference docs → `api-doc-generator-designer`.
   **Remaining gap:** per-operation request/response schema discipline — schema-first source of truth, required vs optional vs
   nullable, partial-update (PATCH) semantics, enum forward-compatibility, standard formats — absent from the skill and its only
   reference file (`grep` for nullab/PATCH/enum/optional/OpenAPI/first-party in `api-event-architect/`: no hits; the reference's
   headings are envelope, webhook policy, consumer checklist, deprecation). Also, first-party APIs used only by the product's own
   clients are not named in scope ("public/partner", `:30`). A standalone skill would collide with `api-event-architect` on
   "design our API" (check 2); a bounded additive slice fits its Purpose ("the external contracts of a multi-tenant SaaS — the API surface", `:18`) → extension, IF a first-party network API counts as an external contract (my judgment, unverified; `skill-quality-reviewer` to confirm at build).
3. **Invocation:** base auto-invocable.
4. **Estimate:** 1–2 h (precedent extensions). Description has 232 chars of room (792 measured). Low confidence.
5. **Value:** moderate; strongest link is to #2 (the API edge is one validation layer). Include only if the batch wants the API
   boundary complete; otherwise next batch.
6. **Pins for the extension's trigger evals:** `error-taxonomy-designer`, `pagination-cursor-designer`, `command-gateway-architect`.

### 5. `refactor-safety-planner` — PARTIAL → BUILD in a later batch

1. **Source:** cat01 #11 Refactor Safety Planning P0 "Plan behavior inventory, tests, rollout, rollback, and risk boundaries before
   restructuring code" (`01-…:34`); #45 Incremental Modernization P1, #46 Strangler Fig Planning P2 (`:68-69`).
2. **Overlap.** The catalog itself records `code-simplifier` as only "cat 01 #11 adjacent" (`docs/skills-catalog.md:395`).
   `code-simplifier` desc: "MANUAL-ONLY; never auto-invoke. Apply behavior-preserving simplifications to explicitly named code … Do NOT
   use … to restructure architecture or change public contracts (architecture-designer + approval)"; it does add characterization
   tests first (`code-simplifier/SKILL.md:65`). `architecture-designer` writes "ordered, individually shippable increments" for a
   structural redesign (`architecture-designer/SKILL.md` workflow step 8). `change-classification-gate` requires
   "behavior-preservation proof (tests before/after)" for refactors but does not plan them. No skill names branch-by-abstraction or
   strangler techniques (`grep`: no hits); the "parallel run" hits mean parallel test execution (`integration-test-designer/SKILL.md:101, 148`; `qa-automation-architect/SKILL.md:123`), not old-vs-new comparison.
   **Remaining gap:** an auto-invocable plan for a medium/large behavior-preserving restructure that is not an architecture redesign
   (module extraction, library replacement, framework upgrade): behavior inventory, characterization-coverage gate, technique
   choice, step slicing with green-and-reversible steps, stop points.
3. **Invocation:** plan only → auto-invocable.
4. **Estimate:** 3–4.5 h (precedent `phase6-…:76`). Low confidence.
5. **Value:** moderate; overlaps the unlisted `code-quality-auditor` ("refactor safety", see Adjacent findings).
6. **Pins:** `architecture-designer`, `code-simplifier` (manual-only prefix rule), `test-coverage-mapper`.

### 6. `dependency-direction-guard` — PARTIAL → DEFER

1. **Source:** cat01 #7 Dependency Direction Guard P0 "Detect dependency inversions, feature-to-feature coupling, platform leaks, and
   circular imports" (`01-…:30`); #6 Layered Architecture Enforcement P0 (`:29`); #50 Architecture Fitness Function Design P1 (`:73`).
2. **Overlap.** `architecture-designer` states allowed directions in design: "Allowed dependency directions are stated … A map without
   directions cannot detect violations later" (`architecture-designer/references/architecture-artifacts.md:26-27`), and delegates
   judging an existing design to the `principal-architecture-reviewer` subagent (`architecture-designer/SKILL.md:32-33`), whose focus
   includes "**Coupling** — hidden dependencies, leaky abstractions, circular references" (`.claude/agents/principal-architecture-reviewer.md:13`).
   `code-reviewer` treats drift "from an accepted ADR or a layering rule in the repository's docs" as MAJOR in a diff
   (`code-reviewer/SKILL.md:88`). `grep` for fitness function / import-linter / dependency-cruiser / ArchUnit / circular import:
   only test-import boundaries in `qa-automation-architect` (`SKILL.md:76, 145`).
   **Remaining gap:** codifying the allowed directions as CI-checkable architecture rules with a baseline-and-ratchet for existing
   violations, plus a whole-graph violation scan. Real but narrow; three shipped surfaces already catch the most common cases.
3. **Invocation:** design/review → auto-invocable; installing a graph tool or editing CI config would be a Stop Condition handed to
   the user / `ci-pipeline-architect` (MANUAL-ONLY).
4. **Estimate:** 2.5–4.5 h (no close precedent; nearest is a file-reading reviewer at 2.5–4, `phase6-…:78`). Low confidence.
5. **Value:** lower than #1–#3 on repo evidence. Also: whether it should be standalone or an `architecture-designer` extension is
   unresolved (triggers "circular imports / enforce layering in CI" are disjoint from the designer's, but the rule set is the
   designer's own map made executable).
6. **Pins:** `architecture-designer`, `code-reviewer`, `principal-code-analyst`.

### 7. `operational-runbook-author` — COVERED → DROP

1. **Source:** cat01 #23 Operational Runbook Authoring P1 "Document deploy, verify, rollback, recover, rotate secrets, inspect logs, and
   troubleshoot procedures" (`01-…:46`).
2. **Overlap, per verb:** rollback → `rollback-runbook-author` (desc "author the rollback RUNBOOK a stranger can execute under
   pressure"); recover/inspect/troubleshoot during incidents → `incident-response-runbook`, which also writes the runbook behind an
   alert ("Use when: an alert exists but its runbook link points at nothing", `incident-response-runbook/SKILL.md:36-38`); migration
   deploy/verify → `data-migration-runbook-author`; recurring risky operations → `gated-deployment-prompt-template` ("Use when: a class
   of risky operations recurs (migrations, prod grants, backfills, data corrections)", `:29-30`); developer setup runbook (cat07 #259)
   → `onboarding-doc-designer`. **Residual:** secret-rotation procedure and a per-service "operations handbook" are not named by any
   doc skill (`grep` for service runbook / operations manual / routine operation: no hits). Too small for a fifth runbook skill, which
   would collide with four. Optional micro-extension (not in the recommended set): name key/secret rotation as an operation class in
   `gated-deployment-prompt-template` (unestimated).
3–6. n/a for a drop; estimate 0–0.25 h for the covered-table row (precedent `qa-tier1-…:130`, `phase7-…:452`).

### 8. `system-context-mapper` — COVERED → DROP

1. **Source:** cat01 #2 System Context Mapping P0 "Map actors, systems, boundaries, integrations, trust zones, and ownership before design
   or implementation" (`01-…:25`).
2. **Overlap:** `architecture-designer` step 1 "Inspect current state first. Map the real components, their dependencies (including
   direction), and data ownership" (`SKILL.md:57-58`) and "Every external system appears at the edge with its adapter named"
   (`references/architecture-artifacts.md:28`); `threat-modeler` "Map the system: assets …, actors …, entry points, and data flows" and
   "Draw trust boundaries" (`threat-modeler/SKILL.md:67-73`); `domain-modeler` actors; `saas-platform-architect` control/data plane.
   No residual a stranger would call a different job (check 3, `quality-review-checklist.md:94-96`).
3–6. n/a; 0–0.25 h.

### 9. `bounded-context-identifier` — COVERED → DROP

1. **Source:** cat01 #4 Bounded Context Identification P0 (`01-…:27`).
2. **Overlap:** `domain-modeler` desc "extract … subdomains, bounded contexts, … and context relationships"; body step 4 "Draw bounded
   contexts … Name the relationship between each context pair (shared kernel, customer–supplier, conformist, anticorruption layer,
   separate ways)" (`domain-modeler/SKILL.md:55-59`); catalog row "language, contexts, aggregates + invariants" (`skills-catalog.md:388`).
   Ownership/contract per context → `architecture-designer` data-ownership map. The product-agnostic roadmap also assigned bounded
   contexts to `domain-modeler` (`docs/roadmaps/product-agnostic-skill-and-agent-roadmap.md:81`).
3–6. n/a; 0–0.25 h.

---

## Adjacent findings the proposal should carry

1. **Unlisted backlog item that overlaps #5 and #6.** Reconciliation `:200-205` says the whole-codebase audit skills
   (`code-quality-auditor`, `dependency-license-audit-reviewer`, `code-audit-orchestrator`, …) "are absorbed into v4 Phase 2 … with the
   remainder in the Phase 2/5 expansion backlog". `code-quality-auditor` ("coupling, circular dependencies, unclear boundaries, and
   refactor safety", `product-agnostic-…-roadmap.md:169`) is NOT in the catalog's Phase 2 list (`skills-catalog.md:1300-1304`) or the
   forecast's nine. Set membership follows the catalog; the inconsistency should be recorded, and #5/#6 decided together with it.
2. **G5 seams.** #1 ↔ cat03 #124 Logging Redaction (`03-…:66`); #2 ↔ cat03 #111/#112 XSS/SQLi (`:53-54`); #3's left-out inbound-webhook
   dedup ↔ cat03 #116 Webhook Security (`:58`). If G5 is chosen too, the seams must be pinned in one plan.
3. **Same-file sequencing.** #2's reciprocity edit and #3's extension both touch `command-gateway-architect/SKILL.md`; put them in one PR
   or merge sequentially.
4. **Execution-plan pairing.** The plan grouped API/idempotency/validation and observability/runbook (`execution-plan.md:707-708`); the
   recommended set keeps that grouping minus the covered runbook item.

## Estimates — basis and confidence

- Per-item ranges reuse the precedent proposals' agent estimates: new design skill 3–5 h (`phase7-…:68`; `phase6-…:75, 79`), 3–4.5
  (`phase6-…:76`), file-reading reviewer 2.5–4 (`phase6-…:78`; `qa-tier1-…:62`); extension 1–2 (`phase7-…:66`; `phase6-…:77`);
  drop 0–0.25 (`qa-tier1-…:130`; `phase7-…:452`); batch overhead 1.5–2.5 (`phase7-…:71`), 2–3.5 (`phase6-…:80`), 1.5–3 (`qa-tier1-…:515`).
- **No measured active time exists** for any comparable build: the metrics rows say "active time not measured" (e.g.
  `aegis-execution-metrics.md:377` for #383).
- **Wall-time cross-check only** (GitHub REST, first commit author date → merge; includes review/CI waits, excludes pre-commit
  authoring): #499 new skill 3h21m57s; #518 new skill 3h15m32s; #522 new skill 3h43m33s; #527 extension 3h18m18s; #383 new skill
  1h56m30s. Not active time; not used to set ranges.
- **Process changed after every precedent.** The seven-stage rule was codified 2026-10-03 (`git log -- docs/delivery-workflow.md` →
  `c3527560 … (#653)`); the precedents are 2026-09-27/28; `git log --first-parent --since=2026-10-03 -- .claude/skills` shows no new
  skill built since. Overhead under seven separate-agent stages is therefore unmeasured for skill builds and likely above the
  precedent 1.5–3.5 h — magnitude **unverified**; the MECH helper's measured FU-1/FU-2 figures should replace this line.
- Totals (`python3 -I -c` sums): recommended 8.5–16.25; recommended + #4 9.5–18.25; alternative B (#5 + #6 + two drops) 7–12.5; all nine
  per these verdicts 15.5–27.25 (vs forecast 18–36, `aegis-backlog-forecast.md:728`).

## Prioritization (`prioritization-frame-picker`)

Frame: value-vs-effort in buckets (coarse cut; inputs are roadmap priority, verified coverage gap, and precedent effort — all soft except
the coverage greps). No must-do (compliance/security) item exists in G3, so no protected lane.

| Item | Value bucket (evidence) | Effort | Order |
|---|---|---|---|
| #3 idempotency MERGE | High per hour: 2 P0 rows + D30 top pull-forward; residual verified absent | S | 1 |
| #1 observability BUILD | High: P0; no auto-invocable telemetry design; orchestrator Stage 3/5 has none | M | 2 |
| #2 validation BUILD | High: 4 P0 rows; DB-constraint and unknown-field policy verified absent | M | 3 |
| #7/#8/#9 DROP | Clears backlog; ~0 effort | ~0 | with the batch |
| #4 api-contract MERGE | Medium: P0 row, residual per-operation schema | S | 4 (optional) |
| #5 refactor BUILD | Medium: P0, catalog says "adjacent" only; overlaps `code-quality-auditor` | M | 5 |
| #6 dependency guard | Medium-low: three surfaces already catch common cases | M | 6 |

Sensitivity: dropping #1's value one bucket (if the Stage 8 operator route is judged enough) ties it with #5 but keeps it above #6; the
#2 value depends on G5 not building an input-validation skill — the one input that could flip the order.

## Recommendation

**Build sub-batch "boundary engineering" (6 dispositions):** BUILD `observability-by-design` and `validation-boundary-designer`;
MERGE `idempotency-first-designer` into `command-gateway-architect`; DROP `operational-runbook-author`, `system-context-mapper`,
`bounded-context-identifier` as covered. 8.5–16.25 provisional active hours (overhead likely understated, see Estimates). 195 → 197.

Alternatives: (A+) add #4 as a second extension (9.5–18.25 h); (B) architecture-hygiene pair #5 + #6 with #8/#9 drops (7–12.5 h), lower
evidence of gap; (C) "none" from G3 if G5 is chosen and the owner prefers to settle the validation/redaction seams there first.

Owner questions this would raise: approve the set; keep the name `observability-by-design` despite the near-miss with
`observability-operator`; include #4 or not; record #5/#6 together with `code-quality-auditor` in a later batch.

### Self-scrutiny

- **Strongest counter-argument (against MERGE for #3):** a small CRUD SaaS with no command bus that double-charges on retry triggers
  `command-gateway-architect` (`:40-41`) and gets a whole command-bus design when it needs one endpoint's idempotency key. A standalone
  idempotency skill would fit that user better. I still recommend MERGE because the standalone would fail check 2 on the gateway's core
  trigger; the extension should add a "single endpoint, no bus yet" path. If the owner weighs the small-app case higher, the
  alternative is a standalone skill with the gateway's Use When at `:40-41` narrowed — costs a gateway description edit and ~2–3 extra hours
  (unverified estimate).
- **Counter-argument for #1:** design-then-operate already exists as `slo-reliability-architect` → `observability-operator`; a third
  observability skill adds a hop and a near-miss name. Answer: neither designs the telemetry schema/propagation, and the operator is
  manual-only, so nothing auto-invocable covers it at design time (`project-orchestrator/SKILL.md:238, 264-277`).
- **Counter-argument for #2:** "validation" is broad and could become a checklist that restates the gateway and appsec skills. Answer: the
  greps show the DB-constraint and unknown-field slices absent, and the output (placement matrix) differs in kind.
- **Least certain claims:** (a) every hour figure — agent estimates with no measured active time, from a lighter pre-#653 process;
  (b) the near-miss name risk — untested, since evals are validated structurally only (`skill-generation-standard.md:583-586`);
  (c) the G5 seam outcomes — depend on another helper's findings; (d) "value to a SaaS builder" rests on roadmap priority and coverage gaps,
  not user-demand data (unverified; DEMAND helper's area). (e) ROUTE-002 effects were not measured (`scripts/audit-skill-contracts.py` not
  run on drafted descriptions).
- **What would change the recommendation:** a G5 plan that claims input validation or redaction (re-scope #2 or #1); measured seven-stage
  build costs far above precedent (shrink to #3 + #1 + drops); evidence that small apps without a command bus are the main audience (make #3
  standalone); a decision that `code-quality-auditor` joins the Phase 2 set (re-plan #5/#6 with it).

## Checked / not checked

Checked: catalog `:1295-1304`, reconciliation `:100-128`, `:200-205`, `:625-640`, `:745-753`, `:1312-1340`; execution plan `:340-381`,
`:674-711`; roadmap cat01 (all rows), cat04 (all rows), cat07 rows matching runbook/observability, cat03 rows matching validation/webhook/
redaction; descriptions of 45+ neighbors via `yaml.safe_load`; bodies of `command-gateway-architect`, `api-event-architect` (+ reference),
`observability-operator`, `architecture-designer` (+ reference), `domain-modeler`, `incident-response-runbook`,
`gated-deployment-prompt-template`, `code-simplifier`, `threat-modeler` (mapping steps), `code-reviewer` (layering line),
`project-orchestrator` stage map, the `principal-architecture-reviewer` agent; standard §5 and §6; `skill-quality-reviewer` checks 2–3.
Not checked: neighbors' trigger-eval case texts beyond counts; `docs/paths/*`; ROUTE-002 output; other helpers' findings (none existed at
17:19:03Z).

Timestamps (`date -u`): start 2026-10-08T17:11:39Z (first command). No initial ETA was recorded at start, so no ETA comparison is possible.

Finish (`date -u`): 2026-10-08T17:27:02Z. Measured wall time: 0:15:23 (start to finish). Active time not measured separately.
