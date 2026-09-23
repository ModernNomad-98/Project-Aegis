# Project Aegis — Construction History

Curated construction history of Project Aegis: the original phase narrative through
**decision 47 (D47)**, followed by dated delivery updates. The
complete authoritative record is the dated decision log in `docs/reconciliation/` —
[`step-0-reconciliation-v4.md`](reconciliation/step-0-reconciliation-v4.md),
its version 4 (v4) reconciliation. For what Project
Aegis *is* and how to start, see the [README](../README.md).

See the [changelog](../CHANGELOG.md) for recent deliveries and the
[documentation index](README.md) for current continuation. The original phase
narrative below preserves the state and sequence at each historical checkpoint.

**Reading key for the original narrative:** `D` plus a number names a decision
in the linked log; a decimal suffix, such as `D12.8`, names a subentry. The
shorthand below includes artificial intelligence (AI), software development
lifecycle (SDLC), software as a service (SaaS), row-level security (RLS),
quality assurance (QA), end-to-end (E2E), and large language model (LLM).
Framework names are the Open Worldwide Application Security Project (OWASP),
International Organization for Standardization (ISO), System and Organization
Controls 2 (SOC 2), and National Institute of Standards and Technology (NIST);
RMF means risk management framework. Later passages use product management
(PM), individual contributor (IC), Google Cloud Platform (GCP), static and
dynamic application security testing (SAST and DAST), and information
architecture (IA). Counts in the original narrative are dated milestones;
use the [current skills catalog](skills-catalog.md) for today's shipped count.
`ASI08` and `ASI10` are OWASP Agentic Security Initiative categories 08 and 10;
`A09` and `A10` are OWASP web-application Top 10 categories 09 and 10. Later
delivery updates use
Behavioral Eval Runner (BER), pull request (PR), continuous integration (CI),
owner decision 1 (OD-1), and work package 2B-4 (WP-2B-4).

## Original construction through D47

The repo is built in **phases**, each a validated batch that builds on the ones before it.
**Phase 0** established the foundation — the authoring standard, templates, eval convention,
validator, catalog, the seven read-only reviewer subagents, and the Step 0 reconciliation of
the two earlier planning tracks. On that base, **Phase 1** shipped the 8-skill AI engineering
**operating-discipline pack** (decision D4); **Phase 1.5** added the 4-skill **AI-SDLC
governance completion** (roadmap #261/#268/#279/#280), finishing the category-08 governance
layer Phase 1 began; **Phase 2** shipped the 10-skill **core architecture & engineering
pack**; **Phase 3** the 9-skill **SaaS & tenant isolation pack**; **Phase 4** the 9-skill
**security, RLS & supply-chain pack**; and **Phase 5** the 16-skill **QA, E2E, manual QA &
evidence pack** (13 canonical skills plus 3 pulled forward from the QA backlog: roadmap
#184/#185/#204).

**Phase 6** shipped the 10-skill **cloud, DevOps, reliability & release pack**; **Phase 7**
the 14-skill **AI security & LLM systems pack** (v4's 10 plus 4 OWASP LLM Top 10 gap
additions, D6); and **Phase 7.5** the **agentic AI security pack** (OWASP Agentic Top 10 for
2026, D7: 6 new skills plus 3 extensions of existing ones, with ASI08 and ASI10 merged into a
single containment reviewer).

The **Compliance & Governance batch** (D9) shipped the 9-skill **compliance pack** — ISO
27001:2022 + ISO 42001:2023 + SOC 2 with NIST AI RMF as companion: one shared control
foundation, framework projections, and a crosswalk that map controls which largely already
exist and produce auditor-grade evidence on top. The **library-meta pack (D13)** then turned
the library on itself — `skill-quality-reviewer` (D18) as the judgment layer atop the
mechanical validator, and D22's four remaining skills (`library-diff-reviewer`,
`eval-runner-designer`, `skill-usage-instrumenter`, `skill-deprecation-planner`) — so the
library now reviews its own additions and PRs, designs how its evals run, measures which
skills actually fire, and can retire a skill as deliberately as it ships one.

A run of **D12 craft packs** followed. The **operational workflow patterns pack** (D12.8, D21)
shipped the 10 evidence-extracted skills that are the concrete, invocable rules of the
**Zero Trust AI Engineering Discipline** (D16). The **data/performance/QA-validation batch**
(D23) shipped three at once — the 7-skill **D12.1 data engineering pack**, the 6-skill
**D12.3 performance engineering pack**, and the 2-skill **D10 Tier 1 performance/load
validation pair** (D12.3 designs *for* performance; D10 *measures* it). The
**product/PM/growth batch** (D24) shipped the 5-skill **D12.2 product-engineering craft
pack**, the 6-skill **D12.5 PM/product-engineering interface pack**, and the 4-skill **D12.6
growth/analytics engineering pack**. The **docs-engineering batch** (D25) shipped the 8-skill
**D12.4 technical writing / docs engineering pack**, and the **staff-IC / architecture /
framework-refresh batch** (D26) shipped the 7-skill **D12.7 staff+ IC craft pack**, the
1-skill **D12.9 architecture-advisory pack**, and the 3-skill **D14 framework-refresh /
source-currency pack**.

The **OWASP web-app gap-closure pair** (D28) closed the last two zero-coverage categories from
the D8 OWASP Top 10:2025 audit — `security-logging-alerting-architect` (A09) and
`error-handling-security-reviewer` (A10) — so all 10 web-app categories now have an owning
skill. The **SaaS architecture-depth pack** (D12.11) then completed in two builds: the
10-skill **strong cluster** (D31) and the 4-skill **low-priority set** (D32), resolving all 14
candidates and bringing the library to **175 skills**. **D33** then ran a library-wide
`skill-quality-reviewer` sweep that landed corrections only, and D34–D36 were
documentation-only — no change to the count. **D38** added
`project-orchestrator`, the beginner-facing top-level lifecycle router that is the library's
front door (175→176). **D42** built the **CONSTRAIN/CURATE design pack** —
`agent-harness-architect`, `model-context-designer`, and `agentic-loop-designer`, plus an
extension of `structured-output-validator` — making the doctrine's D41 inward-facing pillars
real: the DESIGN skills for the AI's own operating environment (harness, context, loop) that
produce what the agentic-security clusters review (176→179). Most recently, **D44** built the **Security scanning & orchestration pack** (D12.10, the last banked capability) — `security-scan-orchestrator`, `sast-orchestration-designer`, and `dast-safety-harness-designer` — the ORCHESTRATION layer that runs and aggregates security scans (SAST/DAST/whole-repo) and yields finding TRIAGE to the judgment skills (179→182). **D45** extended `cloud-architecture-decider` with the full deployment abstraction ladder — rung × provider × posture, adding the modern managed-platform tier and GCP — with no count change. **D46** built `authority-invalidation-architect` — the symptom-triggered owner of the "change didn't take effect" access-bug class (a removed user still sees data, a revoked role still works, logout doesn't end the session), composing the per-surface mechanism owners rather than restating them (182→183). Most recently, **D47** built `superadmin-observability-console-designer` — the cross-tenant superadmin MONITORING-console design owner, closing the three-way pointer hole (`admin-console-architect` punts telemetry to `observability-operator`, which operates backends rather than designing consoles): the layered panel IA plus the cross-tenant read-security model, composing the ~12 feed owners rather than restating them — bringing it to **184 skills** (183→184).

## Delivery update — 2026-09-12

Later work strengthened the library's contracts and built the Behavioral Eval
Runner's offline core, Scenario A grading and gated calibration controls. The
[decision log](reconciliation/step-0-reconciliation-v4.md#5-recorded-decisions)
retains intervening decisions; the
[BER backlog](roadmaps/behavioral-eval-runner-backlog.md) retains its separate
phase authorizations and completion evidence.

PR #89 retired an audit false positive in August. Following the loss of the
previous computer, D62 made GitHub the durable
continuation location for the reviewed source and useful recovery records.
PR #88 integrated and delivered the reviewed calibration-engineering fixes;
PR #90 reconciled shared skill contracts;
PR #91 added permanent Linux/Windows offline CI. PR #93 preserved the owner's
recurring read-only-agent and administrator-merge grants in the repository.
D63 reconciles current documentation with those deliveries.

The [changelog](../CHANGELOG.md) links each delivery and its evidence. Skill
count remains at the D47 total. Measured calibration is unfinished: original
calibration inputs remain unavailable, OD-1 remains open and WP-2B-4 remains
blocked. The [documentation index](README.md) points returning contributors to
current setup and the remaining work, without treating old plans as new tasks.
