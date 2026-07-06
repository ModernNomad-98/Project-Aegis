# Claude-Skills

Reusable planning repository for product-agnostic Claude Code Skills and project subagents.

This repo is the documentation and execution-planning home for building a reusable Claude engineering operating system. The current strategy is to seed research, architecture findings, roadmaps, prompts, standards, templates, evals, validators, and agent specs before generating actual skills.

The goal is not a pile of prompts. The goal is reusable Claude Code Skills and agents that make Claude behave like a disciplined senior/principal engineering partner.

## Start here

For the latest execution path, read these files in order:

1. `docs/research/claude-skills-architecture-audit-findings-v4.md`
2. `docs/prompts/claude-skills-master-generation-prompts-v4.md`
3. `docs/300-repeatable-software-saas-skills-roadmap.md`
4. `docs/skills/`
5. `docs/prompts/senior-principal-claude-skills-execution-plan.md`

Earlier planning documents are retained as historical/reference inputs:

- `docs/research/claude-skills-principal-architecture-findings.md`
- `docs/prompts/master-claude-skills-and-agents-development-prompt.md`
- `docs/prompts/phased-claude-skills-prompts.md`
- `docs/roadmaps/product-agnostic-skill-and-agent-roadmap.md`
- `docs/150-claude-skills-roadmap.md`

## Current documents

| File | Purpose |
|---|---|
| `docs/research/claude-skills-architecture-audit-findings-v4.md` | Current senior-principal architecture audit, recommendations, phase priorities, and skill/agent design rules. |
| `docs/prompts/claude-skills-master-generation-prompts-v4.md` | Current master and phase-by-phase prompts for Claude Code to create reusable skills and agent/orchestrator prompts. |
| `docs/300-repeatable-software-saas-skills-roadmap.md` | Product-agnostic 300-skill roadmap for repeatable software and SaaS architecture, engineering, security, AI engineering, and QA skills. |
| `docs/skills/` | Category-level skill backlogs that break the 300 skills into focused engineering domains. |
| `docs/prompts/senior-principal-claude-skills-execution-plan.md` | Earlier combined execution plan based on prior chat requirements, uploaded v3 files, repo roadmap, and Claude skill guidance. |
| `docs/research/claude-skills-principal-architecture-findings.md` | Earlier senior-principal findings retained for historical context. |
| `docs/prompts/master-claude-skills-and-agents-development-prompt.md` | Earlier master prompt retained as a source input. |
| `docs/prompts/phased-claude-skills-prompts.md` | Earlier phased prompts retained as source input. |
| `docs/roadmaps/product-agnostic-skill-and-agent-roadmap.md` | Earlier product-agnostic roadmap retained as source input. |
| `docs/150-claude-skills-roadmap.md` | Superseded by the 300-skill roadmap and kept only as a redirect for older references. |

## Target repository layout

```text
.claude/
  skills/
    <skill-name>/
      SKILL.md
      references/
      assets/
      evals/
  agents/
    <agent-name>.md

docs/
  prompts/
  research/
  roadmaps/
  standards/
  templates/

scripts/
  validate-skills.py
  validate-agents.py
```

## Architecture decision

Use a flat skill layout under `.claude/skills/<skill-name>/` unless a future package or plugin requires nesting.

Use project subagents under `.claude/agents/<agent-name>.md` only when an isolated worker, tool boundary, or specialist review role is actually useful.

## Core rules

- Skills are reusable procedures, not essays.
- Agents are isolated specialist workers, not replacements for skill quality.
- Build in waves. Do not create all 300 skills at once.
- Start with authoring standards, templates, eval schema, and validators.
- Every skill needs `SKILL.md`, clear frontmatter, concise workflow, output format, validation checklist, gotchas, stop conditions, and evals.
- Every agent needs a narrow job, clear routing description, least-privilege tools, and explicit boundaries.
- Avoid broad `allowed-tools` and broad agent tool access.
- Use read-only exploration first for audits, architecture review, code review, security review, and QA strategy review.
- Treat security, tenant isolation, QA evidence, and verification as first-class design requirements.
- Keep project-specific skills out of the reusable foundation until the product-agnostic foundation is validated.

## Recommended implementation order

| Phase | Outcome |
|---:|---|
| 0 | Create standards, templates, eval schema, agent specs, and validation scripts. |
| 1 | Create foundation engineering skills and core read-only agents. |
| 2 | Create SaaS and cloud architecture skills. |
| 3 | Create security and AI security skills. |
| 4 | Create QA, E2E, clickthrough, manual QA, Playwright, Vite, and Vitest skills. |
| 5 | Create full-codebase audit, static-analysis, dependency audit, principal analysis, and troubleshooting skills. |
| 6 | Expand toward the product-agnostic 300-skill roadmap in validated batches. |

## Recommended Claude Code starting point

Ask Claude Code to read:

```text
docs/research/claude-skills-architecture-audit-findings-v4.md
docs/prompts/claude-skills-master-generation-prompts-v4.md
```

Then run the Master Role Prompt and Phase 0 only. Do not generate all 300 skills in one pass.

## Safety note

Claude Code Skills and subagents can influence future code, tests, reviews, and tool usage. Review every generated skill and agent before trusting it. A reusable skill library is useful only if it is specific, testable, constrained, maintained, and validated.
