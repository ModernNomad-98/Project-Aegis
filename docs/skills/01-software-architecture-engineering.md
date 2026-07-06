# Software Architecture & Engineering

Reusable architecture and design skills for clean, evolvable systems.

These are product-agnostic, repeatable Claude skills. They are meant to become executable `SKILL.md` workflows, not one-off prompts.

| # | Skill | Priority | Usage |
|---:|---|---|---|
| 1 | Architecture Decision Record Authoring | P0 | Capture context, decision, alternatives, consequences, rollback, and operational impact for major technical choices. |
| 2 | System Context Mapping | P0 | Map actors, systems, boundaries, integrations, trust zones, and ownership before design or implementation. |
| 3 | Domain Model Discovery | P0 | Extract entities, workflows, invariants, lifecycle states, and business rules from requirements, code, and docs. |
| 4 | Bounded Context Identification | P0 | Separate business domains into clear ownership areas with minimal coupling and explicit contracts. |
| 5 | Modular Monolith Design | P0 | Design cohesive modules inside one deployable system before introducing distributed-system complexity. |
| 6 | Layered Architecture Enforcement | P0 | Keep presentation, domain, application service, platform, data access, and infrastructure concerns separated. |
| 7 | Dependency Direction Guard | P0 | Detect dependency inversions, feature-to-feature coupling, platform leaks, and circular imports. |
| 8 | Interface-First Engineering | P0 | Design stable interfaces, adapters, command shapes, and contracts before changing implementation internals. |
| 9 | API Contract Design | P0 | Define request and response schemas, validation, error shapes, compatibility, and versioning strategy. |
| 10 | Backward-Compatible Change Design | P0 | Prefer additive changes, feature flags, migration phases, and compatibility shims over breaking changes. |
| 11 | Refactor Safety Planning | P0 | Plan behavior inventory, tests, rollout, rollback, and risk boundaries before restructuring code. |
| 12 | Architecture Drift Review | P0 | Compare code, docs, tests, and implementation patterns to identify drift from intended architecture. |
| 13 | Data Ownership Modeling | P0 | Define which module owns each table, record type, command, mutation path, event, and read model. |
| 14 | State Machine Modeling | P1 | Model lifecycle states, legal transitions, terminal states, retries, and invalid transition handling. |
| 15 | Workflow Orchestration Design | P1 | Design multi-step workflows with clear triggers, dependencies, compensations, and audit points. |
| 16 | Event-Driven Design | P1 | Use domain events for async reactions while keeping commands deterministic and auditable. |
| 17 | Idempotency-First Design | P0 | Prevent duplicate side effects from retries, double-clicks, webhook replays, and automation reruns. |
| 18 | Consistency Boundary Design | P1 | Choose where strong consistency, eventual consistency, queues, or repair jobs are appropriate. |
| 19 | Transactional Boundary Review | P1 | Define which operations must succeed atomically and which can safely be split into stages. |
| 20 | CQRS Read/Write Separation | P1 | Separate mutation paths from optimized read models when complexity or performance justifies it. |
| 21 | Error Taxonomy Design | P1 | Create consistent safe error categories for validation, auth, authorization, conflict, dependency, and unknown failures. |
| 22 | Observability-by-Design | P0 | Add correlation IDs, structured logs, metrics, traces, and diagnostic context from the beginning. |
| 23 | Operational Runbook Authoring | P1 | Document deploy, verify, rollback, recover, rotate secrets, inspect logs, and troubleshoot procedures. |
| 24 | Scalability Constraint Mapping | P1 | Identify bottlenecks across database, RLS, queues, browser automation, storage, API calls, and AI calls. |
| 25 | Performance Budget Design | P1 | Set budgets for load time, query count, payload size, render cost, latency, memory, and background work. |
| 26 | Caching Strategy Design | P1 | Define cache scope, invalidation, TTLs, permissions, stale data behavior, and tenant-safe keys. |
| 27 | Feature Flag Architecture | P1 | Design safe rollout, kill switches, experiments, tenant scopes, and phased migrations. |
| 28 | Configuration Architecture | P1 | Separate build-time config, runtime config, tenant settings, secrets, defaults, and validation. |
| 29 | Extensibility Point Design | P1 | Create extension points that support future needs without exposing unstable internals. |
| 30 | Plugin Boundary Design | P2 | Define plugin contracts, isolation, versioning, permissions, and safe extension lifecycle. |
| 31 | Adapter Pattern Application | P1 | Wrap external systems or unstable libraries behind stable internal interfaces. |
| 32 | Facade Pattern Application | P1 | Provide a simpler interface over complex subsystem behavior without hiding critical side effects. |
| 33 | Repository Pattern Governance | P1 | Use repositories or data access layers only where they reduce coupling and preserve security rules. |
| 34 | Service Object Design | P1 | Place business operations in cohesive services rather than bloated controllers, hooks, or components. |
| 35 | Use Case Layer Design | P1 | Represent user or system actions as explicit use cases with inputs, outputs, and authorization. |
| 36 | Policy Object Design | P1 | Encapsulate authorization and business rules in testable policy units. |
| 37 | Validation Boundary Design | P0 | Place validation at API, command, form, database, and integration boundaries without relying on one layer. |
| 38 | Invariant Enforcement | P0 | Identify non-negotiable business and security invariants and enforce them in code and tests. |
| 39 | Concurrency Control Design | P1 | Choose optimistic locking, pessimistic locking, unique constraints, queues, or idempotency for race prevention. |
| 40 | Retry and Compensation Design | P1 | Define retryable operations, non-retryable operations, backoff, compensation, and dead-letter handling. |
| 41 | Auditability Design | P0 | Ensure important actions produce durable evidence with actor, target, reason, outcome, and trace context. |
| 42 | Architecture Review Checklist | P0 | Review proposals for boundaries, coupling, security, tests, observability, migration, and rollback. |
| 43 | Technical Debt Classification | P1 | Classify debt by risk, owner, impact, payoff, and whether it blocks future architecture. |
| 44 | Decision Reversal Planning | P1 | Design decisions so they can be reversed or replaced when assumptions fail. |
| 45 | Incremental Modernization Planning | P1 | Modernize legacy areas through seams, tests, adapters, and safe migration slices. |
| 46 | Strangler Fig Planning | P2 | Replace legacy behavior gradually behind routing, adapters, and controlled cutover gates. |
| 47 | Monolith-to-Service Readiness Review | P2 | Evaluate whether a boundary is ready to become a service based on ownership, data, operations, and failure modes. |
| 48 | Distributed Systems Risk Review | P1 | Identify latency, partial failure, retries, ordering, duplication, and observability risks before distribution. |
| 49 | Data Flow Diagramming | P0 | Produce clear diagrams showing inputs, outputs, storage, trust boundaries, and side effects. |
| 50 | Architecture Fitness Function Design | P1 | Define tests or checks that continuously verify architectural constraints. |
| 51 | Nonfunctional Requirement Modeling | P0 | Translate reliability, security, performance, privacy, compliance, and maintainability into measurable requirements. |
| 52 | Tradeoff Analysis Facilitation | P0 | Compare options across complexity, cost, security, delivery speed, operability, and reversibility. |
| 53 | Build vs Buy Evaluation | P1 | Assess whether to build, integrate, or buy based on strategic value, risk, cost, and lock-in. |
| 54 | Architecture Spike Planning | P1 | Design time-boxed experiments with hypotheses, success criteria, artifacts, and decision outputs. |
| 55 | System Decomposition Review | P0 | Decompose systems into modules, services, workflows, and data ownership without prematurely overengineering. |

## Skill implementation standard

When this category is converted into executable skills, each `SKILL.md` should include:

- Purpose
- When to use
- Required inputs
- Step-by-step workflow
- Expected outputs
- Validation checklist
- Anti-patterns / stop conditions
