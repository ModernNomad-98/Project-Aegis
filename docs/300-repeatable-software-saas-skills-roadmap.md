# 300 Repeatable Claude Skills Roadmap

This roadmap replaces the earlier 150-skill product-influenced draft with product-agnostic, repeatable Claude skills for software and SaaS architecture, design, engineering, security, AI engineering, and QA.

## What changed

- Expanded from 150 to 300 skills.
- Removed individual product-feature skills.
- Reweighted the roadmap toward architecture, SaaS engineering, security/RLS, QA, AI-era SDLC, and AI software engineering.
- Split the backlog into category documents so the skills can be converted into executable `SKILL.md` workflows.

## Category index

| Category | Count | Document |
|---|---:|---|
| Software Architecture & Engineering | 55 | [`docs/skills/01-software-architecture-engineering.md`](skills/01-software-architecture-engineering.md) |
| SaaS Platform Architecture | 35 | [`docs/skills/02-saas-platform-architecture.md`](skills/02-saas-platform-architecture.md) |
| SaaS Security, Multi-Tenancy & RLS | 40 | [`docs/skills/03-saas-security-rls.md`](skills/03-saas-security-rls.md) |
| Backend, API & Data Engineering | 30 | [`docs/skills/04-backend-api-data-engineering.md`](skills/04-backend-api-data-engineering.md) |
| Frontend & UX Engineering | 20 | [`docs/skills/05-frontend-ux-engineering.md`](skills/05-frontend-ux-engineering.md) |
| QA, Test Architecture & Validation | 55 | [`docs/skills/06-qa-test-engineering.md`](skills/06-qa-test-engineering.md) |
| DevOps, Release & Reliability Engineering | 25 | [`docs/skills/07-devops-release-reliability.md`](skills/07-devops-release-reliability.md) |
| AI-Era SDLC & Agent Operating Discipline | 20 | [`docs/skills/08-ai-era-sdlc-agent-ops.md`](skills/08-ai-era-sdlc-agent-ops.md) |
| AI Software Engineering & LLM Systems | 20 | [`docs/skills/09-ai-software-engineering.md`](skills/09-ai-software-engineering.md) |
| **Total** | **300** |  |

## Recommended first 25 skills to turn into executable SKILL.md workflows

1. **Architecture Decision Record Authoring** (P0) — Capture context, decision, alternatives, consequences, rollback, and operational impact for major technical choices.
2. **System Context Mapping** (P0) — Map actors, systems, boundaries, integrations, trust zones, and ownership before design or implementation.
3. **Domain Model Discovery** (P0) — Extract entities, workflows, invariants, lifecycle states, and business rules from requirements, code, and docs.
4. **Bounded Context Identification** (P0) — Separate business domains into clear ownership areas with minimal coupling and explicit contracts.
5. **Modular Monolith Design** (P0) — Design cohesive modules inside one deployable system before introducing distributed-system complexity.
6. **Layered Architecture Enforcement** (P0) — Keep presentation, domain, application service, platform, data access, and infrastructure concerns separated.
7. **Dependency Direction Guard** (P0) — Detect dependency inversions, feature-to-feature coupling, platform leaks, and circular imports.
8. **Interface-First Engineering** (P0) — Design stable interfaces, adapters, command shapes, and contracts before changing implementation internals.
9. **API Contract Design** (P0) — Define request and response schemas, validation, error shapes, compatibility, and versioning strategy.
10. **Backward-Compatible Change Design** (P0) — Prefer additive changes, feature flags, migration phases, and compatibility shims over breaking changes.
11. **Refactor Safety Planning** (P0) — Plan behavior inventory, tests, rollout, rollback, and risk boundaries before restructuring code.
12. **Architecture Drift Review** (P0) — Compare code, docs, tests, and implementation patterns to identify drift from intended architecture.
13. **Data Ownership Modeling** (P0) — Define which module owns each table, record type, command, mutation path, event, and read model.
14. **State Machine Modeling** (P1) — Model lifecycle states, legal transitions, terminal states, retries, and invalid transition handling.
15. **Workflow Orchestration Design** (P1) — Design multi-step workflows with clear triggers, dependencies, compensations, and audit points.
16. **Event-Driven Design** (P1) — Use domain events for async reactions while keeping commands deterministic and auditable.
17. **Idempotency-First Design** (P0) — Prevent duplicate side effects from retries, double-clicks, webhook replays, and automation reruns.
18. **Consistency Boundary Design** (P1) — Choose where strong consistency, eventual consistency, queues, or repair jobs are appropriate.
19. **Transactional Boundary Review** (P1) — Define which operations must succeed atomically and which can safely be split into stages.
20. **CQRS Read/Write Separation** (P1) — Separate mutation paths from optimized read models when complexity or performance justifies it.
21. **Error Taxonomy Design** (P1) — Create consistent safe error categories for validation, auth, authorization, conflict, dependency, and unknown failures.
22. **Observability-by-Design** (P0) — Add correlation IDs, structured logs, metrics, traces, and diagnostic context from the beginning.
23. **Operational Runbook Authoring** (P1) — Document deploy, verify, rollback, recover, rotate secrets, inspect logs, and troubleshoot procedures.
24. **Scalability Constraint Mapping** (P1) — Identify bottlenecks across database, RLS, queues, browser automation, storage, API calls, and AI calls.
25. **Performance Budget Design** (P1) — Set budgets for load time, query count, payload size, render cost, latency, memory, and background work.

## Skill implementation standard

Each future `skills/<skill-name>/SKILL.md` should include:

- Purpose
- When to use
- Required inputs
- Step-by-step workflow
- Expected outputs
- Validation checklist
- Anti-patterns and stop conditions

Keep every skill small, executable, repeatable, product-agnostic, and safe to reuse across multiple software and SaaS repositories.
