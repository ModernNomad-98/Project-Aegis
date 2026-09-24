# Project Aegis — instructions for coding agents

Project Aegis is a library of role and discipline skills for AI-assisted SaaS engineering. These startup instructions (this `AGENTS.md`, the `CLAUDE.md` that imports it, and `.claude/skills/`) are intentionally reusable in TWO roles: the Project Aegis source-library checkout, and a user's own consumer/product repository that copied the skills in. This file therefore does not, by itself, prove which repository you are in — determine the workspace role from evidence before acting.

**Determine workspace role before acting.** Classify the workspace as either the Project Aegis source library (Role A) or the user's consumer/product repository (Role B):

- **Source-library role requires corroborating local source-package landmarks.** Treat the workspace as the Project Aegis source library only when these landmarks are present in the checkout: a `README.md` whose top identifies the repository as `# Project Aegis`, `docs/skills-catalog.md`, `scripts/validate-skills.py`, and `artifacts/audits/skill-contract-audit-baseline.json`. A genuine Aegis clone or fork keeps these landmarks; role detection reads them locally and needs no network call.
- **Copied startup files never prove source-library role.** The presence of `.claude/skills`, `AGENTS.md`, and `CLAUDE.md` — alone or together, and however many skills are copied — does NOT make a workspace the Project Aegis source library. The README tells users to copy exactly those files into their own product repository, so copied skills are tools inside a product repo, not evidence of the source library.
- **A product repository with copied Aegis skills stays the product repository.** A workspace that carries the copied skills but lacks the source-package landmarks above is the user's consumer/product repository. A zero-commit consumer repo with no application files and no `docs/project-state.md` is a fresh Stage 0 product repository — work in the CURRENT workspace as that product repo; never call it the skills library or a mere toolbox, and never redirect the user into a second/sibling product folder merely because the Aegis skills are present.
- **Ambiguous role gets one question and no write.** When the source-package landmarks are incomplete and the intended role genuinely cannot be determined, surface the ambiguity, ask exactly one role/location clarification question, write nothing, and do not default to declaring the workspace a library.

Skills live in `.claude/skills/<skill-name>/SKILL.md` (open Agent Skills format: YAML frontmatter + workflow doc).
Before designing, reviewing, or fixing anything, find the matching skill there and follow its SKILL.md.
Skills whose description begins "MANUAL-ONLY" must never be auto-applied — use them only when the user names them explicitly.
**Teach build choices before requesting a decision.** Whenever a skill presents
viable ways to build or run the user's product and asks the user to choose,
explain unfamiliar terms in plain language. For each relevant option, say why
it is on the table, its practical benefits and drawbacks, and its costs in
money, setup time, and ongoing maintenance. Identify unknown or changing costs
instead of inventing prices. Recommend the option that best fits the user's
known goals and constraints, explain why, then ask one question about one
decision. Ask for a missing constraint first when a sound comparison depends
on it. Keep factual discovery questions and simple execution approvals concise;
do not turn them into option comparisons. A choice or preference does not by
itself authorize installation, spending, provisioning, deployment, or another
side effect; apply the relevant skill's authority rules separately.
**Source-library owner preference, 2026-09-24: dogfood Aegis skills.** In
Role A, every coding agent and delegated subagent must identify and read the
matching Aegis skill before any source-library task, including task management,
troubleshooting, design, implementation, review, investigation, delivery, or
documentation, then use its applicable workflow and checks. Name the skill
used in the work report; if no skill fits, say so briefly. Pass this
requirement to delegated agents. This applies to future
source-library work and does not make a MANUAL-ONLY skill automatic or grant
any new execution, publication, or merge authority. The owner's direct task
instructions still take precedence.
When actually invoking any Aegis skill, tell the user its exact name and, in
plain language, why it applies now, what it will inspect or do, and what
result or decision it will produce. Afterward, explain what it found, what
remains uncertain, and which action needs the user's decision. Keep this brief
and tied to the actual work; announcing a possible skill is not an invocation.
This teaching step never relaxes a manual-only boundary or substitutes
explanation for evidence or approval.
Evidence over assumption: verify against the repo and live systems before acting, and treat volatile facts (versions, counts, tool behavior) as verification items, not truths.

**Source-library owner approvals.** For work on `ModernNomad-98/Project-Aegis` in
Role A, read [the owner approval register](docs/approvals/APPROVAL_REGISTER.md)
before asking for an approval already granted. Apply the recorded human scope and
later lifecycle events. These are this source repository's owner instructions;
consumer/product repositories and unrelated forks do not inherit them by copying
Aegis files. Current direct user instructions retain their authority before they
are transcribed into the register.
