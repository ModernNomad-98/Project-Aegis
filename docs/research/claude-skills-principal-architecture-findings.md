# Principal Claude Skills and Agents Architecture Findings

Prepared: 2026-07-06
Repository: `nguyenpv1980-wq/Claude-Skills`
Role lens: Senior Principal Claude / AI Architect

## 1. Scope and source audit

This document combines the available project evidence into one implementation-ready architecture brief for Claude Code.

Sources used:

- Current repository inspection through GitHub.
- Existing repository files:
  - `README.md`
  - `docs/150-claude-skills-roadmap.md`
- Uploaded v3 knowledge base:
  - `claude-skills-saas-cloud-security-knowledge-base-v3.md`
- Uploaded v3 execution prompt:
  - `prompt-for-claude-to-generate-skills-v3.md`
- Retrieved prior chat memory for the two requested conversations:
  - `AI Skills Development List`
  - `Claude Skills Development`
- Official public documentation reviewed on 2026-07-06:
  - Claude Code Skills documentation
  - Agent Skills specification, best practices, description optimization, and eval guidance
  - Claude Code custom subagents documentation

Important limitation: I could not retrieve exact full standalone chat exports named `AI Skills Development List` or `Claude Skills Development` as literal files. I used retrievable conversation memory plus the uploaded v3 files and the live repo state. Do not treat this as a verbatim transcript archive of those chats.

## 2. Current repo findings

The repo already had:

- `README.md`, focused on a 150-skill roadmap across WayPoint, Brigara OS / opsflow, Carrot & Daikon Ordering System, Memora, Evanna-AI, and SaaS-Founder-Coaching.
- `docs/150-claude-skills-roadmap.md`, a useful but older roadmap with project-specific references.

The current user direction changes the repo strategy:

- The new skill library should be product-agnostic first.
- Project/domain skills may exist later, but they must not pollute the reusable engineering foundation.
- The work should include skills and agents, not only skills.
- The output should be phased and reusable for future Claude Code execution.

## 3. Executive summary

The right architecture is not to generate 150 or 300 skills immediately. That would create noise, duplicate instructions, weak descriptions, missing evals, and unsafe tool boundaries.

The right architecture is a skill-and-agent factory:

1. Define standards, templates, eval schemas, and validators.
2. Build a small foundation layer of high-leverage skills.
3. Add a small set of least-privilege project subagents.
4. Expand into SaaS, cloud, security, AI security, QA, manual QA, E2E, code audit, and troubleshooting waves.
5. Only after the first waves pass validation should Claude generate the broader 300-skill backlog.

The reusable foundation should make Claude behave like a serious engineering partner:

- Model before code.
- Read docs before implementation.
- Write tests before fixes where practical.
- Make small patches.
- State assumptions.
- Keep security and tenant isolation explicit.
- Use risk-based QA.
- Produce validation evidence.
- Use agents for isolated specialist work, not as an excuse for broad tool access.

## 4. Key architectural decision: skills vs agents

### Skills

Use skills for reusable procedures. A skill should answer:

- When should Claude use this?
- What inputs should Claude inspect?
- What exact workflow should Claude follow?
- What should Claude produce?
- What should stop Claude?
- How is the output validated?

Skills belong under:

```text
.claude/skills/<skill-name>/SKILL.md
```

Each skill may optionally include:

```text
references/
assets/
examples/
scripts/
evals/
```

Use a flat skill layout first. Do not create nested skill directories unless invocation behavior is tested and there is a strong packaging reason.

### Agents

Use project subagents for specialist work that benefits from isolated context or constrained tools.

Agents belong under:

```text
.claude/agents/<agent-name>.md
```

Good agent use cases:

- Read-only codebase exploration.
- Architecture review.
- Security review.
- QA strategy review.
- Senior debugging analysis.
- Dependency/static-analysis triage.

Bad agent use cases:

- Broad autonomous editing.
- Deployments without approval.
- Secret access.
- Repo-wide rewrites.
- Replacing skill quality with a vague role prompt.

## 5. Main finding: v3 is strong but needs an agent layer

The uploaded v3 knowledge base is strong on skills, quality gates, QA, Playwright, Vite, Vitest, code audit, and senior troubleshooting. It already captures the right skill waves and correctly avoids final `SKILL.md` generation inside the knowledge base.

The gap is agent architecture. The repo needs explicit guidance for `.claude/agents/` so Claude Code can create isolated specialist workers with least-privilege tools. Skills and agents should be designed together:

- Skills define reusable workflows.
- Agents execute specialized inspection or review with isolated context.
- Skills can call for an agent only when isolation or tooling control adds value.

## 6. Reconciliation with existing 150-skill roadmap

The existing `docs/150-claude-skills-roadmap.md` is valuable but should be treated as historical foundation material, not the final plan.

Keep from the existing roadmap:

- Architecture Decision Record Authoring.
- System Context Mapping.
- Module Boundary Design.
- Domain Model Discovery.
- Bounded Context Identification.
- API Contract Design.
- Refactor Safety Planning.
- Agent Startup Context Gate.
- Human Approval Boundary.
- Risk-Based Validation Matrix.
- RLS Policy Authoring and RLS Test Harness Design.
- AI Prompt Injection Defense.
- AI Closeout Report.

Change from the existing roadmap:

- Move project-specific skills to later backlog.
- Make the first waves product-agnostic.
- Add explicit agent design.
- Add Phase 0 standards and validators before skill creation.
- Replace bulk generation with gated waves.

## 7. Priority recommendation

### Phase 0 - Skill and agent factory

Create standards and validation before actual skills:

- `docs/standards/skill-authoring-standard.md`
- `docs/standards/agent-authoring-standard.md`
- `docs/templates/skill-template.md`
- `docs/templates/agent-template.md`
- `docs/templates/evals-template.json`
- `scripts/validate-skills.py`
- `scripts/validate-agents.py`

### Phase 1 - Foundation engineering discipline

Create these first:

1. `domain-modeler`
2. `architecture-designer`
3. `grill-with-docs`
4. `tdd-engineer`
5. `systematic-debugger`
6. `code-reviewer`
7. `code-simplifier`
8. `adr-writer`

Create these agents:

1. `codebase-explorer`
2. `principal-architect-reviewer`
3. `security-reviewer`
4. `qa-strategy-reviewer`
5. `senior-debugger`

### Phase 2 - SaaS and cloud architecture

Create SaaS platform and cloud design skills after Phase 1 validates:

- SaaS platform architecture.
- Tenant modeling.
- Multi-tenant data architecture.
- Entitlement and billing architecture.
- Reliability and SLO architecture.
- Observability and operations.
- Cost architecture.
- API and event architecture.
- Cloud-neutral decisioning.
- Azure SaaS architecture.
- AWS SaaS architecture.
- IaC and resilience review.

### Phase 3 - Security and AI security

Create security and AI security skills after the SaaS model exists:

- Threat modeling.
- AppSec implementation.
- Secure SDLC review.
- Multi-tenant security testing.
- Secrets and identity hardening.
- Supply-chain review.
- Security PR review.
- AI threat modeling.
- Prompt-injection defense.
- RAG security.
- Agent tool safety.
- AI red-team and eval harness.
- AI governance and output safety.

### Phase 4 - QA, E2E, manual QA, and frontend validation

Create QA skills only after the foundation skills exist:

- QA strategy.
- Acceptance criteria testing.
- Test plan design.
- Coverage mapping.
- QA automation architecture.
- E2E test architecture.
- Playwright engineering.
- Clickthrough testing.
- Manual test case creation.
- Screenshot evidence planning.
- Vitest unit/component testing.
- Vite build QA.
- Flaky-test investigation.
- Regression suite curation.
- Test data architecture.
- Accessibility, performance, and visual regression.

### Phase 5 - Audit, troubleshooting, and principal code analysis

Create these after QA and security standards exist:

- Full-codebase auditor.
- Code audit orchestrator.
- Static-analysis reviewer.
- Dependency/license auditor.
- Code quality auditor.
- Principal code analyst.
- Senior troubleshooter.

### Phase 6 - Product-agnostic 300-skill expansion

After Phases 0-5 are validated, expand into the full 300-skill roadmap. The 300 skills should be generated from category maps, not hand-written in one uncontrolled pass.

## 8. Product-agnostic 300-skill target

Use this as a long-term capacity target, not a first-pass build target.

| Category | Target count |
|---|---:|
| Software architecture and engineering | 55 |
| SaaS architecture | 35 |
| SaaS security and tenant isolation | 40 |
| Backend, API, and data engineering | 30 |
| Frontend, UX, and product engineering | 20 |
| QA, test automation, validation, and evidence | 55 |
| DevOps, reliability, and operations | 25 |
| AI-era SDLC and agent governance | 20 |
| AI software engineering and AI security | 20 |
| Total | 300 |

## 9. Non-negotiable quality gates

Every generated skill must pass:

- Directory exists under `.claude/skills/<skill-name>/`.
- `SKILL.md` exists.
- `name` matches the directory.
- `description` is specific, trigger-oriented, and under 1024 characters.
- `SKILL.md` is under 500 lines.
- The workflow is procedural, not generic advice.
- Supporting files are referenced explicitly and relatively.
- No broad `allowed-tools` unless justified.
- Side-effect workflows use explicit stop/approval gates.
- Each skill has evals.
- README catalog matches the actual files.

Every generated agent must pass:

- File exists under `.claude/agents/<agent-name>.md`.
- Agent name is specific and lowercase-hyphenated.
- Description says when Claude should delegate to it.
- Tools are least-privilege.
- Read-only agents are actually read-only.
- Editing, deployment, or side-effect agents require explicit user approval.
- Agent output format is defined.
- Agent stop conditions are defined.

## 10. Anti-patterns to reject

Reject any generated skill or agent that:

- Sounds like a generic best-practice essay.
- Has a weak description like `helps with architecture`.
- Grants broad tools without a need.
- Creates huge monolithic `SKILL.md` files.
- Repeats the same guidance across many skills.
- Does not include evals.
- Tells Claude to make security changes without tests.
- Lets AI tools perform external side effects without approval.
- Treats E2E as the only validation layer.
- Treats scanner output as truth without human-style triage.
- Calls a symptom a root cause without evidence.

## 11. Bottom-line recommendation

Proceed with a controlled, phase-gated build.

The best next action for Claude Code is Phase 0, then Phase 1. Do not build all waves at once. The user needs a reusable engineering operating system for Claude, not a large folder of weak prompts.