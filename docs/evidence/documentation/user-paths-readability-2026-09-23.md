# Guided user paths readability batch — 2026-09-23

## Scope and decision

This batch reviews three user-facing paths:
[`something-is-broken.md`](../../paths/something-is-broken.md),
[`check-your-app.md`](../../paths/check-your-app.md), and
[`add-ai-safely.md`](../../paths/add-ai-safely.md). Its other edit is one row in
the [documentation readability backlog](../../roadmaps/aegis-documentation-readability-backlog.md).
The branch began from the signed pull request (PR) #138 head in an isolated
worktree. The
paths are guides to existing skills, not new runtime procedures or authority.

The prior full-documentation estimate remains **80–200 active hours**. This
bounded three-path batch was estimated at **1–3 active hours**. The selected
remaining backlog was **175–394 active hours** at start. These are scope
forecasts; observed wall time below is not a measure of active-only labor.

## Findings resolved

- The live-outage row previously named `incident-response-runbook` as a live
  responder. Its skill contract authors documents only. The path now sends a
  live incident to the existing runbook and human on-call owner, with explicit
  manual `systematic-debugger` invocation for unknown-cause diagnosis.
- Release readiness now uses the shipped skill's GO (ready to ship) or NO-GO
  (blocked from shipping) outcome. The
  secrets step reports approval-dependent rotation honestly, and the database
  policy step distinguishes an audit from a requested, separately reviewed
  migration that is never applied by the auditor.
- The artificial intelligence (AI) path describes evaluation evidence as
  scoped and revisitable, rather
  than a guarantee of general safety. Its harness, context and loop choices
  now name the feature shapes that call for each design.
- The pages define continuous integration (CI), software as a service (SaaS),
  personally identifiable information (PII), and retrieval-augmented
  generation (RAG) on first use. Each gives a copyable starting prompt and
  shows how to explicitly request manual-only skills.

The original path order and skill links were retained. No skill body, test,
runtime, provider, secret or deployment setting was changed. The rest of the
repository documentation sweep remains open.

## Verification and timing

- Checked the referenced skill frontmatter and relevant use/stop conditions
  for live incident, debugging, secret rotation, row-level security,
  release readiness, prompt injection and AI evaluation.
- All 51 local links across the five scoped files resolved, including 34 skill
  links. `python -B scripts/validate-skills.py` passed: 185 valid skills and
  zero warnings. `git diff --check` passed.
- Independent read-only review at 18:14:49–18:17:17 Coordinated Universal Time
  (UTC; 2 minutes 28 seconds) found additional undefined AI and command-line
  interface (CLI) terms and unsupported claims
  about Vite secret coverage, automatic error fixes, cost controls, retrieval
  authorization, injection findings and regression coverage. The five scoped
  files were corrected. The 18:18:57–18:20:00 UTC follow-up review found no
  blocker, resolved all 51 local links, and checked the three guide pages
  against their referenced skill contracts.

Work started at **2026-09-23 18:10:57 UTC**. The local verification checkpoint
was **18:13:38 UTC**, an observed wall interval of **2 minutes 41 seconds**.
Active-only implementation time was not instrumented; this interval is not
an estimate of the remaining full documentation sweep.
