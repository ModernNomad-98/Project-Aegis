# Project Aegis — instructions for coding agents

This repository is a skills library: role and discipline skills for AI-assisted SaaS engineering.
Skills live in `.claude/skills/<skill-name>/SKILL.md` (open Agent Skills format: YAML frontmatter + workflow doc).
Before designing, reviewing, or fixing anything, find the matching skill there and follow its SKILL.md.
Skills whose description begins "MANUAL-ONLY" must never be auto-applied — use them only when the user names them explicitly.
Evidence over assumption: verify against the repo and live systems before acting, and treat volatile facts (versions, counts, tool behavior) as verification items, not truths.
