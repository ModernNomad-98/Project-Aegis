# Fifth skill-reference screen, first half — 2026-09-23

## Current reading

This is dated delivery evidence. Its original base commit, estimates, counts,
and pending-review language describe that historical batch. For current
acceptance totals and remaining work, use the [documentation ledger](../../roadmaps/aegis-documentation-readability-backlog.md) and [forecast](../../roadmaps/aegis-backlog-forecast.md); follow the linked owning skill or reference for current guidance. This note does not grant implementation or merge authority.

Reading key: D6 is the [recorded Phase 7 reconciliation decision](../../reconciliation/step-0-reconciliation-v4.md#phase-7--ai-security--llm-systems-p1)
anchoring the security mapping to the Open Worldwide Application Security
Project (OWASP) Top 10 for large language model (LLM) applications
(2025). The historical D6 link below points to that decision, not a new grant.

## Scope and timing

This bounded documentation batch makes the first ten reference pages in the
fifth sorted screen readable on their own. It began at **2026-09-23 20:27:55
UTC** (Coordinated Universal Time) in an isolated worktree based on merged pull
request #158, `origin/main` commit
`f5373fa47b73f9aeb8de34670140202aac22e8aa`.

The earlier whole-screen estimate was **2–4 active hours**. The new first-half
estimate is **1–3 active hours**; the selected backlog total remains
**175–394 active hours**. These are planning estimates. Active work time was
not instrumented. The observed wall interval from start to the final local
check at **2026-09-23 20:36:40 UTC** was **8 minutes 45 seconds**.

## Reader path and change

Open the owning skill guide for its invocation and authority boundary, then
use its linked reference for the detailed template or table:

| Reference | Readability change |
| --- | --- |
| [Manual test case template](../../../.claude/skills/manual-test-case-creator/references/manual-case-template.md) | Defines case, trace, priority, and capture-point labels. |
| [Memory poisoning controls](../../../.claude/skills/memory-context-poisoning-reviewer/references/memory-poisoning-controls.md) | Defines risk IDs and memory/retrieval terms. |
| [Merge-is-deploy governance template](../../../.claude/skills/merge-is-deploy-governance/references/governance-doc-template.md) | Adds an owning-skill link and corrects revert guidance against official Git documentation. |
| [Mobile viewport sheet](../../../.claude/skills/mobile-viewport-craft/references/mobile-viewport-sheet.md) | Defines viewport and touch guidance shorthand. |
| [Model poisoning controls](../../../.claude/skills/model-poisoning-reviewer/references/poisoning-controls.md) | Defines model-risk terms and sends a live incident to the human incident owner and existing runbook. |
| [Tenant data scoping](../../../.claude/skills/multi-tenant-data-architect/references/scoping-strategy-tradeoffs.md) | Defines database and mapping terms, with no executable instruction. |
| [Tenant negative-test matrix](../../../.claude/skills/multi-tenant-security-tester/references/negative-test-matrix.md) | Defines security terms and names the manual-only boundary. |
| [Notification and webhook sheet](../../../.claude/skills/notification-webhook-ux-designer/references/notification-webhook-sheet.md) | Defines direct-message and response-class shorthand. |
| [Chatty access patterns](../../../.claude/skills/n-plus-one-detector/references/chatty-access-patterns.md) | Defines data and monitoring terms and names the manual-only boundary. |
| [Instrumentation checklist](../../../.claude/skills/observability-operator/references/instrumentation-checklist.md) | Defines metric acronyms and names the manual-only boundary. |

The governance template now uses `git revert <sha>` for an ordinary squash
commit, requiring inspection of merge parents before choosing `-m`. It also
requires inspection with
`git rev-list` before reversing a rebase series and explains that
`<oldest>..<newest>` excludes the oldest. Its official sources are the Git
[revert](https://git-scm.com/docs/git-revert),
[revision syntax](https://git-scm.com/docs/gitrevisions), and
[`rev-list`](https://git-scm.com/docs/git-rev-list) manuals.

Only these ten reference pages and this record are in scope. All other
templates, criteria, manual-only posture, approval boundaries, parent
`SKILL.md` files, and evaluation fixtures are unchanged. No live system,
provider, private data, or real tenant evidence was accessed.

## Local verification and review

- `python -B scripts/validate-skills.py`: **185 valid skills, 0 warnings**.
- All ten owning-skill links and ten reference links resolve; the three Git
  documentation links were checked against Git's official manuals.
- Nine pages' table rows and all ten pages' code-fence counts match the base.
  The governance template changes only its three targeted revert rows and adds
  the explanation and sources. The poisoning page changes only its targeted
  live-incident routing sentence outside the term definitions, and links its
  D6 code to the recorded reconciliation decision.
- `git diff --check` passes. The changed-path set is exactly these ten
  reference pages and this note; the note has no trailing whitespace.
- Independent coordinator read-only review found no other blocker. It asked
  that the copyable merge-commit command choose an inspected parent rather
  than hardcode `-m 1`, and that D6 link to its source. Both corrections are
  included. Final checks are rerun before a Developer Certificate of Origin
  (DCO) signed local commit. No push or pull request is part of this writer
  batch.
