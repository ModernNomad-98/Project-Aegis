# Sixth skill-reference readability batch — 2026-09-23

## Scope and timing

This bounded documentation batch corrects four standalone reference pages in
the sixth sorted skill-reference screen. Editing began at **2026-09-23
20:43:34 UTC** (Coordinated Universal Time) in an isolated worktree based on
merged pull request #160, `origin/main` commit
`770c49ef875dfbcac63c3f3bb596bc694f5d536e`.

The previous fifth-screen half-batch estimate was **1–3 active hours**. The
new sixth-batch estimate is **2–4 active hours**; the selected backlog total
remains **175–394 active hours**. These are planning estimates. Active work
time was not instrumented. The observed interval from edit start to the local
check at **2026-09-23 20:45:11 UTC** was **1 minute 37 seconds**.

## Reader path and changes

Read each owning skill for invocation and authority, then use its reference:

- [Prompt-injection defense patterns](../../../.claude/skills/prompt-injection-defender/references/injection-defense-patterns.md) define risk terms and the manual-only boundary. A confirmed live hit routes to the human incident owner and current approved runbook; the incident-response skill remains for authoring.
- [RAG retrieval authorization](../../../.claude/skills/rag-security-architect/references/rag-retrieval-authz.md) defines the retrieval and authorization abbreviations before the control choices.
- [RLS audit checklist](../../../.claude/skills/rls-policy-auditor/references/rls-audit-checklist.md) defines policy terms and marks the write-statement test plan for synthetic disposable non-production fixtures, with transaction rollback and post-test verification.
- [Rollback runbook template](../../../.claude/skills/rollback-runbook-author/references/rollback-runbook-template.md) defines operations terms and includes `DRAFT` in the copyable status field; `CURRENT` requires rehearsal and verification.

Only these four reference pages and this record are in scope. Existing SQL
statements, test expectations, authorization rules, rollback steps, approval
gates, parent `SKILL.md` files, and evaluation fixtures are unchanged. No live
database, provider, private data, or real incident was accessed.

## Local verification and review

- `python -B scripts/validate-skills.py`: **185 valid skills, 0 warnings**.
- All four owning-skill links and four evidence links resolve to local files.
- The four existing table row sets and code-fence counts match the base; the
  RLS SQL fenced block is byte-equivalent to the base. The added safety text
  changes execution posture without changing test commands or expectations.
- `git diff --check` passes. The changed-path set is exactly the four
  references and this record; the record has no trailing whitespace.
- Independent read-only review is pending on this frozen draft. The writer
  has stopped editing and will not commit, push, or open a pull request.
