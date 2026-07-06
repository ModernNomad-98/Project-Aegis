# Claude-Skills

Reusable planning repository for product-agnostic Claude Code Skills and project subagents.

This repo is the documentation and execution-planning home for building a reusable Claude engineering operating system. The current strategy is to seed research, architecture findings, roadmaps, prompts, standards, templates, evals, and validators before generating actual skills.

The goal is not a pile of prompts. The goal is reusable Claude Code Skills and agents that make Claude behave like a disciplined senior engineering partner.

## Start here

Read these files in order:

1. `docs/research/claude-skills-principal-architecture-findings.md`
2. `docs/prompts/master-claude-skills-and-agents-development-prompt.md`
3. `docs/prompts/phased-claude-skills-prompts.md`
4. `docs/roadmaps/product-agnostic-skill-and-agent-roadmap.md`
5. `docs/150-claude-skills-roadmap.md`

## Current documents

| File | Purpose |
|---|---|
| `docs/research/claude-skills-principal-architecture-findings.md` | Senior-principal architecture findings, source reconciliation, phase recommendations, and quality gates. |
| `docs/prompts/master-claude-skills-and-agents-development-prompt.md` | Master prompt for Claude Code to build the skill and agent library. |
| `docs/prompts/phased-claude-skills-prompts.md` | Phase-by-phase implementation prompts for controlled execution. |
| `docs/roadmaps/product-agnostic-skill-and-agent-roadmap.md` | Product-agnostic roadmap for skills, agents, and the long-term 300-skill target. |
| `docs/150-claude-skills-roadmap.md` | Earlier 150-skill roadmap. Treat as historical foundation and input, not the final architecture. |

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
| 0 | Create standards, templates, eval schema, and validation scripts. |
| 1 | Create foundation engineering skills and core read-only agents. |
| 2 | Create SaaS and cloud architecture skills. |
| 3 | Create security and AI security skills. |
| 4 | Create QA, E2E, clickthrough, manual QA, Playwright, Vite, and Vitest skills. |
| 5 | Create full-codebase audit, static-analysis, dependency audit, principal analysis, and troubleshooting skills. |
| 6 | Expand toward the product-agnostic 300-skill roadmap in validated batches. |

## Recommended Phase 1 skills

- `domain-modeler`
- `architecture-designer`
- `grill-with-docs`
- `tdd-engineer`
- `systematic-debugger`
- `code-reviewer`
- `code-simplifier`
- `adr-writer`

## Recommended Phase 1 agents

- `codebase-explorer`
- `principal-architect-reviewer`
- `security-reviewer`
- `qa-strategy-reviewer`
- `senior-debugger`

## Safety note

Claude Code Skills and subagents can influence future code, tests, reviews, and tool usage. Review every generated skill and agent before trusting it. A reusable skill library is useful only if it is specific, testable, constrained, maintained, and validated.