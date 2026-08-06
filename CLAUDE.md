@AGENTS.md

## Claude Code — startup routing

1. **Determine the workspace role FIRST — before listing or selecting a skill, and before any file operation.** `AGENTS.md`, `CLAUDE.md`, and `.claude/skills/` are copied, by design, into consumer/product repositories, so their presence never proves this is the Project Aegis source library. Inspect the local source-package landmarks — a `# Project Aegis` `README.md`, `docs/skills-catalog.md`, `scripts/validate-skills.py`, and `artifacts/audits/skill-contract-audit-baseline.json` — before deciding. Do NOT infer source-library role from `.claude/skills`, `AGENTS.md`, or `CLAUDE.md` alone. When those source landmarks are absent, treat the CURRENT workspace as the user's consumer/product repository and work in it; for a fresh consumer repo (no commits, no application files, no `docs/project-state.md`), `project-orchestrator` starts at Stage 0 in this workspace. Never propose a second or sibling app directory merely because the Aegis skills are copied in. If the role is genuinely ambiguous, ask exactly one clarification question and write nothing.

2. Before asking product questions, choosing any technology, installing anything, or creating or editing any file: list the available skills under `.claude/skills/` and select the one that owns the request; open its `SKILL.md` and follow it before acting.

3. For an end-to-end, vague, or nontechnical request ("I have an idea for an app…", "where do I start?"): open `.claude/skills/project-orchestrator/SKILL.md` and follow it from Stage 0 — requirements discovery precedes every technical choice.

4. For a clearly scoped single-stage request (review this diff, design this schema, fix this bug): use the owning skill directly. Do NOT route it through `project-orchestrator`.

5. Skills whose description begins "MANUAL-ONLY" are never auto-invoked — only when the user names them explicitly.

6. If the matching skill is not present in this copy of the library, say so plainly and continue with ordinary care — never invent a skill or silently substitute a different one.
