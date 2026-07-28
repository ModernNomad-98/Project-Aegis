@AGENTS.md

## Claude Code — startup routing

1. Before asking product questions, choosing any technology, installing anything, or creating or editing any file: list the available skills under `.claude/skills/` and select the one that owns the request; open its `SKILL.md` and follow it before acting.

2. For an end-to-end, vague, or nontechnical request ("I have an idea for an app…", "where do I start?"): open `.claude/skills/project-orchestrator/SKILL.md` and follow it from Stage 0 — requirements discovery precedes every technical choice.

3. For a clearly scoped single-stage request (review this diff, design this schema, fix this bug): use the owning skill directly. Do NOT route it through `project-orchestrator`.

4. Skills whose description begins "MANUAL-ONLY" are never auto-invoked — only when the user names them explicitly.

5. If the matching skill is not present in this copy of the library, say so plainly and continue with ordinary care — never invent a skill or silently substitute a different one.
