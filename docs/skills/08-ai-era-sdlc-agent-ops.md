# AI-Era SDLC & Agent Operating Discipline

Skills that make AI-assisted development controlled, traceable, reviewable, and safe.

These are product-agnostic, repeatable Claude skills. They are meant to become executable `SKILL.md` workflows, not one-off prompts.

| # | Skill | Priority | Usage |
|---:|---|---|---|
| 261 | AI-Era SDLC Operating Model | P0 | Define how humans and AI agents plan, implement, validate, review, merge, and close software work. |
| 262 | Agent Startup Context Gate | P0 | Require Claude to read project rules, status, architecture, security, tests, and relevant docs before work. |
| 263 | Phase-Locked Execution | P0 | Prevent agents from jumping ahead, adding bonus scope, or modifying unapproved areas. |
| 264 | Change Classification Gate | P0 | Classify changes before work and choose the correct approval and validation path. |
| 265 | Human Approval Boundary | P0 | Stop for explicit approval when work touches schema, security, deployments, production data, or unclear behavior. |
| 266 | AI Task Decomposition | P0 | Break broad goals into small, testable, reviewable tasks with acceptance criteria and risks. |
| 267 | Prompt-to-Diff Traceability | P1 | Connect prompt, plan, touched files, tests, PR, and closeout evidence into a traceable chain. |
| 268 | Agent Authorization Matrix | P1 | Define what the agent may plan, edit, test, commit, deploy, or merge without further approval. |
| 269 | Source-of-Truth Reconciliation | P0 | Resolve conflicts between chat, docs, code, PRs, tests, and current user instructions. |
| 270 | No-Silent-Assumptions Protocol | P0 | State assumptions, ask when ambiguity changes outcome, and stop when security or data behavior is unclear. |
| 271 | Reviewable Diff Discipline | P0 | Keep changes small, intentional, isolated, and understandable for human review. |
| 272 | Exact File Staging Discipline | P0 | Stage only intended files and avoid generated noise, secrets, backups, or unrelated edits. |
| 273 | AI Work Evidence Pack | P1 | Collect validation output, logs, screenshots, migration proof, CI status, and known skips. |
| 274 | AI Closeout Report | P0 | Summarize changes, non-changes, tests, evidence, risks, and next actions. |
| 275 | Agent Failure Recovery | P1 | Recover from failed tests, interrupted runs, dirty trees, broken branches, and partial implementations. |
| 276 | Agent Instruction Consolidation | P0 | Keep Claude, Codex, Copilot, Cursor, and other agent rules aligned to one source of truth. |
| 277 | AI Code Review Protocol | P1 | Review diffs for architecture drift, security gaps, missing tests, and validation weakness. |
| 278 | AI Pair Engineering Protocol | P1 | Guide inspect, plan, implement, validate, explain, and handoff behavior for agent-assisted coding. |
| 279 | Agent Memory Governance | P1 | Update persistent project memory only when confirmed facts change and avoid storing secrets. |
| 280 | Agent Governance Audit | P1 | Audit whether AI-assisted changes followed planning, approval, validation, security, and closeout discipline. |

## Skill implementation standard

When this category is converted into executable skills, each `SKILL.md` should include:

- Purpose
- When to use
- Required inputs
- Step-by-step workflow
- Expected outputs
- Validation checklist
- Anti-patterns / stop conditions
