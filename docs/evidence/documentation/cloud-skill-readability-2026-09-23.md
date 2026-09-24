# Cloud architecture skill readability — 2026-09-23

> **Current reading, checked 2026-09-24:** This is the earlier AWS and Azure
> skill reading batch. Its no-push/no-pull-request statements describe the
> writer's checkpoint, not the delivered state. Read the current
> [AWS skill](../../../.claude/skills/aws-saas-architect/SKILL.md) and
> [Azure skill](../../../.claude/skills/azure-saas-architect/SKILL.md);
> pull request #214 later revised the Azure guidance. The original review
> findings and timing below remain historical evidence.

## Scope and timing

This bounded documentation batch improves the Amazon Web Services (AWS) and
Azure software-as-a-service (SaaS) architecture skill guides for human readers
and artificial intelligence (AI) agents. It changes only the two `SKILL.md`
files linked below and this record. The work began at
**2026-09-23 19:34:25 UTC** (Coordinated Universal
Time), in an isolated worktree from `origin/main` at
`70ca4eef13521d27c11754979b2bfb90ce3981c5`.

The earlier estimate for this batch was **2–4 active hours**; the current
bounded estimate remains **2–4 active hours**. The selected backlog total is
**175–394 active hours**. These are estimates for different scopes, not
measured time. The observed wall interval and any measured active time will be
recorded at the final local checkpoint. From the first recorded start to the
local check at **19:38:01 UTC**, observed wall time was **3 minutes 36 seconds**;
active time was not instrumented.

## Reader path and change

For a decided AWS or Azure platform, read the matching skill's Purpose and
term definitions, check Use When, then follow its Workflow and Output Format.
The definitions expand the provider, identity, networking, compute, security,
and delivery abbreviations used throughout each guide. The output templates
now label the security/delivery and infrastructure-as-code sections in plain
words. The definitions do not make a provider choice or claim current service
availability, limits, or prices.

- [AWS SaaS architect](../../../.claude/skills/aws-saas-architect/SKILL.md)
- [Azure SaaS architect](../../../.claude/skills/azure-saas-architect/SKILL.md)

The metadata frontmatter, trigger descriptions, routing boundaries, service
choices, tenant-isolation criteria, verification-item requirements, and
stop conditions are retained. The existing skill evaluation fixtures were
reviewed for impact and are unchanged.

## Local verification

- `python -B scripts/validate-skills.py`: **185 valid skills, 0 warnings**.
- Existing AWS and Azure `evals.json` and `trigger-evals.json`: inspected;
  their trigger and behavior expectations still apply to the edited text.
- Both relative links resolve to the intended skill files. The writer's local
  scope was the three listed files; the final branch also adds one row to the
  documentation readability backlog. `git diff --check` passes, and the new
  record has no trailing whitespace.
- Independent read-only review reported no blocker at
  **2026-09-23 19:38:46 UTC**, before the Developer Certificate of Origin
  (DCO) signed commit. No remote push or pull request is part of this writer
  batch.
