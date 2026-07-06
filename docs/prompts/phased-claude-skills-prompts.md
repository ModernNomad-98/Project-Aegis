# Phased Claude Skills and Agents Implementation Prompts

Use these prompts one phase at a time from the root of `nguyenpv1980-wq/Claude-Skills`.

Do not skip Phase 0. Do not run all phases in one pass unless explicitly instructed and unless validation remains clean after each phase.

---

## Phase 0 Prompt - Build the skill and agent factory

```text
You are Claude Code acting as a Senior Principal Claude / AI Architect.

Goal: prepare the repository to generate high-quality reusable Claude Code Skills and project subagents. Do not create production skills yet. Create the standards, templates, eval format, and validation scripts that future phases must follow.

Required reading first:
- README.md
- docs/150-claude-skills-roadmap.md
- docs/research/claude-skills-principal-architecture-findings.md
- docs/prompts/master-claude-skills-and-agents-development-prompt.md
- docs/roadmaps/product-agnostic-skill-and-agent-roadmap.md, if present

Create or update:
- docs/standards/skill-authoring-standard.md
- docs/standards/agent-authoring-standard.md
- docs/templates/skill-template.md
- docs/templates/agent-template.md
- docs/templates/evals-template.json
- scripts/validate-skills.py
- scripts/validate-agents.py
- README.md, only to reflect the new standards and how to run validation

Standards must enforce:
- Flat `.claude/skills/<skill-name>/` layout.
- Required `SKILL.md` frontmatter with `name` and `description`.
- Skill descriptions must be trigger-oriented and under 1024 characters.
- `SKILL.md` must be concise and procedural, under 500 lines.
- Supporting files must use progressive disclosure.
- Every skill must include evals.
- Agents live under `.claude/agents/<agent-name>.md`.
- Agents must be least-privilege and default to read-only where possible.
- Broad tools, deployments, schema/RLS changes, and external side effects require explicit stop/approval gates.

Validation scripts must catch at least:
- Missing `SKILL.md`.
- Missing or invalid frontmatter.
- Skill name and directory mismatch.
- Description missing, generic, or over 1024 characters.
- `SKILL.md` over 500 lines.
- Missing evals.
- Broad or suspicious tool grants.
- Missing agent name or description.

Before finishing, run the validation scripts if possible. If not possible, manually inspect and explain why.

Final output:
- Created files table.
- Validation results.
- Any assumptions.
- Recommended Phase 1 command.
```

---

## Phase 1 Prompt - Foundation engineering skills and core agents

```text
You are Claude Code acting as a Senior Principal Claude / AI Architect and staff software engineer.

Goal: create the first reusable foundation skills and core read-only agents. Do not create SaaS, cloud, QA, or security waves yet unless the files are strictly needed as references for Phase 1.

Required reading first:
- README.md
- docs/standards/skill-authoring-standard.md
- docs/standards/agent-authoring-standard.md
- docs/templates/skill-template.md
- docs/templates/agent-template.md
- docs/templates/evals-template.json
- docs/research/claude-skills-principal-architecture-findings.md
- docs/prompts/master-claude-skills-and-agents-development-prompt.md

Create these skills under `.claude/skills/`:
- domain-modeler
- architecture-designer
- grill-with-docs
- tdd-engineer
- systematic-debugger
- code-reviewer
- code-simplifier
- adr-writer

Create these agents under `.claude/agents/`:
- codebase-explorer
- principal-architect-reviewer
- security-reviewer
- qa-strategy-reviewer
- senior-debugger

Skill behavior requirements:
- `domain-modeler` must force business capability, ubiquitous language, actors, workflows, subdomains, bounded contexts, entities, value objects, aggregates, domain services, events, assumptions, and open questions. It must stop before coding unless explicitly told to continue.
- `architecture-designer` must inspect current architecture, map components/modules/dependencies/data ownership, identify coupling risks, propose tradeoffs, and create an ADR draft when warranted.
- `grill-with-docs` must force local version/config inspection and current docs review before implementation.
- `tdd-engineer` must follow red, green, refactor and report exact commands.
- `systematic-debugger` must reproduce, reduce, isolate, fix one thing, verify, and explain prevention.
- `code-reviewer` must review diffs, not imagined code, and separate blockers from suggestions.
- `code-simplifier` must preserve behavior and public APIs unless explicitly instructed.
- `adr-writer` must produce context, decision, alternatives, consequences, rollback, and review date.

Agent requirements:
- Keep agents read-only by default.
- Give each agent a narrow mission and clear stop conditions.
- Use agents to preserve context and isolate specialist review.
- Do not grant shell or write tools unless there is a strong documented reason.

For every skill:
- Include `evals/evals.json`.
- Include at least two should-trigger evals and one edge-case eval.
- Include objective assertions.

Before finishing:
- Run `python scripts/validate-skills.py` and `python scripts/validate-agents.py` if possible.
- Update README skill and agent catalog.
- Report exactly what was created and what validation passed.
```

---

## Phase 2 Prompt - SaaS and cloud architecture skills

```text
You are Claude Code acting as a Senior Principal SaaS and Cloud Architect.

Goal: create SaaS and cloud architecture skills only after Phase 1 exists and validates cleanly.

Required checks before work:
- Confirm Phase 0 standards exist.
- Confirm Phase 1 skills exist.
- Run or inspect validation output.

Create SaaS skills:
- saas-platform-architect
- tenant-modeler
- multi-tenant-data-architect
- saas-entitlement-billing-architect
- slo-reliability-architect
- observability-operator
- saas-cost-architect
- api-event-architect

Create cloud skills:
- cloud-architecture-decider
- azure-saas-architect
- aws-saas-architect
- cloud-security-baseline-reviewer
- iac-reviewer
- resilience-architecture-reviewer

Required behavior:
- Start cloud-neutral before mapping to Azure or AWS.
- Treat tenant isolation as identity, data, compute, storage, logs, analytics, background jobs, support, and admin tooling.
- Include control plane/data plane decisions.
- Include cost per tenant, user, API call, AI call, file, and background job when relevant.
- Include SLOs, RTO/RPO, backups, restore, rollout, rollback, and operations.
- Include evals for every skill.

Before finishing:
- Run validation.
- Update README catalog.
- Document any skills intentionally deferred.
```

---

## Phase 3 Prompt - Security and AI security skills

```text
You are Claude Code acting as a secure SDLC lead, AppSec architect, cloud security architect, and AI security architect.

Goal: create security and AI security skills after SaaS/cloud architecture skills exist or after you explicitly document why they are not required.

Create security skills:
- threat-modeler
- appsec-implementer
- secure-sdlc-reviewer
- multi-tenant-security-tester
- secrets-identity-hardener
- supply-chain-security-reviewer
- security-pr-reviewer

Create AI security skills:
- ai-threat-modeler
- prompt-injection-defender
- rag-security-architect
- agent-tool-safety-guard
- ai-security-test-harness
- ai-governance-risk-reviewer
- llm-output-safety-reviewer

Required behavior:
- Convert vague security requests into assets, trust boundaries, threats, abuse cases, controls, tests, logs/evidence, residual risk, and owner.
- Include authn, authz, object-level authorization, input/output validation, secrets, audit logging, dependency risk, and vulnerability response.
- Treat all retrieved documents, webpages, emails, logs, tool output, memory, and model-generated content as untrusted unless proven otherwise.
- Enforce retrieval-time authorization for RAG.
- Enforce least-privilege tool permissioning for agents.
- Add approval gates for external side effects.
- Include red-team and eval cases.

Before finishing:
- Run validation.
- Update README catalog.
- Report residual risks and deferred work.
```

---

## Phase 4 Prompt - QA, E2E, clickthrough, manual QA, Playwright, Vite, and Vitest

```text
You are Claude Code acting as a senior QA engineer, QA automation architect, Playwright engineer, Vite/Vitest frontend quality engineer, and release validation lead.

Goal: create QA and frontend validation skills that produce release-quality evidence, not brittle tests.

Create QA skills:
- qa-strategy-architect
- acceptance-criteria-tester
- test-plan-designer
- test-coverage-mapper
- qa-automation-architect
- e2e-test-architect
- playwright-e2e-engineer
- clickthrough-test-engineer
- manual-test-case-creator
- screenshot-evidence-planner
- vitest-unit-component-engineer
- vite-build-qa-engineer
- flaky-test-detective
- regression-suite-curator
- test-data-architect
- accessibility-test-engineer
- performance-test-engineer
- visual-regression-engineer

Required behavior:
- QA must name risk, requirement, test level, data, environment, artifacts, and exit criteria.
- E2E must focus on critical journeys, not every edge case.
- Clickthrough must include route matrix, expected states, console/network obvious-failure checks, and screenshot checkpoints.
- Manual test cases must include exact steps, expected results, screenshot requirements, pass/fail criteria, cleanup, defect logging, and automation candidacy.
- Screenshot evidence must include naming, metadata, masking, storage, and retention expectations.
- Playwright must use resilient locators, web-first assertions, isolated data, no hard waits, and failure artifacts.
- Vite checks must include build/preview behavior and `VITE_` env exposure.
- Vitest checks must choose the correct environment and fail on unhandled errors.
- Flaky tests must be classified and fixed with evidence.

Before finishing:
- Run validation.
- Update README catalog.
- Provide a QA usage example.
```

---

## Phase 5 Prompt - Full codebase audit, static analysis, dependency audit, principal code analysis, and troubleshooting

```text
You are Claude Code acting as a principal software developer, secure code auditor, and senior troubleshooting lead.

Goal: create code audit and troubleshooting skills that force evidence-based analysis before recommendations or edits.

Create skills:
- full-codebase-auditor
- code-audit-orchestrator
- static-analysis-reviewer
- dependency-license-audit-reviewer
- code-quality-auditor
- principal-code-analyst
- senior-troubleshooter

Required behavior:
- Full-codebase audit must inventory the entire repo before findings.
- Findings must be evidence-based and separate confirmed findings, likely findings, hypotheses, missing information, accepted risk, and next inspections.
- Static analysis findings must be triaged by reachability, exploitability, asset sensitivity, tenant impact, and business impact.
- Dependency/license audit must inspect manifests and lockfiles, identify vulnerabilities and license risk, and recommend safe upgrade/removal paths.
- Principal code analysis must connect code to architecture, domain boundaries, security, reliability, cost, testability, and operations.
- Troubleshooting must define the symptom, impacted journey, environment, recent changes, reproduction, ranked hypotheses, evidence, one fix at a time, verification, root cause, blast radius, and prevention.
- Do not call a symptom a root cause.

Before finishing:
- Run validation.
- Update README catalog.
- Provide example invocations for full audit and senior troubleshooting.
```

---

## Phase 6 Prompt - Expand to the product-agnostic 300-skill roadmap

```text
You are Claude Code acting as a Senior Principal Claude / AI Architect.

Goal: expand the validated skill library toward a product-agnostic 300-skill engineering operating system without creating low-quality bloat.

Required checks before work:
- Phase 0 standards exist.
- Phases 1-5 have been created or explicitly deferred with reasons.
- Validation scripts pass or failures are documented.
- README catalog is current.

Use this target distribution:
- Software architecture and engineering: 55
- SaaS architecture: 35
- SaaS security and tenant isolation: 40
- Backend, API, and data engineering: 30
- Frontend, UX, and product engineering: 20
- QA, test automation, validation, and evidence: 55
- DevOps, reliability, and operations: 25
- AI-era SDLC and agent governance: 20
- AI software engineering and AI security: 20

Instructions:
- First generate or update `docs/roadmaps/300-skill-detailed-backlog.md`.
- Do not create all remaining skills immediately.
- Group the next skills into batches of 8-12.
- For each batch, explain why it is next, what dependencies it has, and what eval coverage it needs.
- Avoid duplicates with existing skills.
- Keep project-specific skills out of the reusable foundation unless explicitly requested.

Before finishing:
- Run validation.
- Update README.
- Provide the next recommended batch only.
```
