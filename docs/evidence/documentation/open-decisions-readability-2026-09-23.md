# Open decisions index readability batch — 2026-09-23

## Scope and forecast

This bounded batch updates the [open-decisions page](../../roadmaps/aegis-open-decisions-2026-09-23.md)
and one row in the [documentation readability backlog](../../roadmaps/aegis-documentation-readability-backlog.md).
It started at `adcef2b97a34c018da76c6b7cae673e62a2365cd`, the current
`origin/main` after pull request (PR) #144, in an isolated worktree. The
owner's original post-#107 proposal text is preserved below a new dated
current index; the index is explanatory and grants no new authority.

No item estimate had previously been stated for this page. This bounded batch
was estimated at **1–3 active hours**. The prior full-documentation estimate
remains **80–200 active hours**, and the selected remaining backlog was
**175–394 active hours** at start. These are scope forecasts; observed wall
time below is not active-only labor.

## Reconciliation

The 2026-09-23 post-#107 packet used then-current proposal language. For
today's status, the merged [approval register](../../approvals/APPROVAL_REGISTER.md),
the [latest forecast](../../roadmaps/aegis-backlog-forecast.md), and owning
[Behavioral Eval Runner](../../roadmaps/behavioral-eval-runner-backlog.md),
[control-plane](../../roadmaps/resumable-control-plane-backlog.md), and
[setup](../../roadmaps/aegis-setup-routing-plan.md) records take precedence
over that historical planning snapshot.

- The 30-day complete-bundle policy was selected in APR-009. APR-012 granted
  only an offline synthetic first proof; [PR #139](https://github.com/ModernNomad-98/Project-Aegis/pull/139)
  remained open at the review checkpoint. Real-host enforcement and operator
  cleanup controls remain incomplete.
- The 160 replacement candidates still need owner semantic and exact-byte
  label approval. The public sanitized checkpoint was used; no private input
  or sealed holdout was accessed. Source/accounting reconciliation, an exact
  execution-source amendment, renewed provider allowance, and owner decision
  1 result ratification remain open.
- A disposable POSIX host direction was chosen, but a named selected host and
  its R4/R5 capability proof remain absent. Generic Linux continuous
  integration cannot stand in for that proof.
- CP-WP-003A's synthetic negative proof shipped through PR #123. The broader
  CP-WP-003 real-source and host gates and CP-WP-004 target selection remain
  blocked.
- Issue #101 packages 1, 2, and 3 shipped under their own bounded grants;
  package 4 host proof and comparison, conditional packages 5/6, and package 7
  remain future work. No optional helper is selected.

The new page defines its abbreviations and status code before the current
index. It leaves the original table, proposed near-term sequence and closing
qualification available as dated evidence rather than rewriting the owner's
proposal. No runtime, approval, provider, host, private data or deployment
surface was changed.

## Verification and timing

- Checked the current approval register through APR-012, merged history through
  PR #144, the open PR #139 status, and the latest forecast and owning records.
- All 38 local links and six anchors across the three scoped pages resolved.
  The original post-#107 packet remained byte-equal to its starting revision
  after newline normalization (5,179 bytes). `python -B
  scripts/validate-skills.py` passed with 185 valid skills and zero warnings;
  `git diff --check` passed. Git status showed only the three authorized paths.
- Independent read-only review and exact-head PR checks remain delivery gates.
  This batch does not complete the wider documentation sweep.

Work started at **2026-09-23 18:56:54 UTC**. The local verification checkpoint
was **2026-09-23 19:01:17 UTC**, an observed wall interval of **4 minutes 23
seconds**. Active-only implementation time was not instrumented; PR review and
Actions waiting occur later.
