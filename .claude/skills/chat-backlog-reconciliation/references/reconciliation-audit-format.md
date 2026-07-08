# Chat Backlog Reconciliation — Verdicts, Evidence Rules, Worked Example

Companion to `chat-backlog-reconciliation`.

## Verdict taxonomy with evidence rules

| Verdict | Meaning | Minimum evidence | Common misuse |
| --- | --- | --- | --- |
| `completed` | The item is fully done in the repo. | Merged PR # or commit SHA whose diff covers the item, or the file/test state proving it (file:line). | Granting it because the chat said "done" or a closeout claimed it. Chat and closeouts are claims — the audit verifies claims against the primary record. |
| `partial` | Real evidence of some of it; the rest absent. | Same evidence class as completed, PLUS a named list of what is missing. | Using `partial` as a polite `unknown`. If no evidence at all was found, it is not partial. |
| `active` | Work is in flight now. | Open PR, live branch with relevant commits, assigned issue with recent activity — cited. | Calling something active because someone said they'd get to it. Intent is not activity. |
| `not-active` | Nothing started. Must sub-classify: still-wanted (→ route to backlog) or deliberately dropped (→ record the drop + who decided). | Absence of evidence after a real search, plus the still-wanted/dropped determination. | Leaving the sub-class blank — the item then wrongly resurrects or silently dies. |
| `unknown` | Cannot determine from available evidence. | A statement of what was searched and what artifact would resolve it. | Avoiding it. `unknown` is an honest verdict, and the ceiling for any chat-only claim. |

Hard rule: **a chat message asserting completion caps at `unknown`** until
repo evidence upgrades it. This mirrors the house governance rule that
missing evidence is never a PASS (`agent-governance-audit`).

## Extraction rules

- One row per DISTINCT item after dedup: the same decision discussed in
  three conversations is one row with three sources.
- Preserve the chat's own status claim in its own column ("chat claimed") —
  the gap between claimed and audited is the sweep's most useful signal.
- Date every source. An undated chat export is still usable; write
  `date unknown` rather than inventing one.
- Template out anything live: tokens, URLs with credentials, tenant/user
  ids → `<tenant-id>`, `<api-key — not copied>`. The extraction doc is a
  tracked repo file; treat it as public within the repo's audience.
- Decisions get filed in the repo's decision convention (dated decision
  log or ADR via `adr-writer`), with the reconciliation doc linking rather
  than duplicating.

## Worked example (abbreviated)

```
CHAT BACKLOG RECONCILIATION — 2026-07-07
Sweep boundary: assistant conversations 2026-06-01 → 2026-07-06 (prior sweep: none)

| # | Item | Chat source + date | Chat claimed | Verdict | Evidence | Routed to |
|---|---|---|---|---|---|---|
| 1 | Rate-limit the invite endpoint | conv "abuse review", 2026-06-04 | "done" | completed | PR #61 merged 2026-06-06; `api/invites.ts:88` | — |
| 2 | Drop the legacy `v1/export` route | conv "cleanup", 2026-06-12 | "agreed, next sprint" | not-active (still wanted) | no PR/branch/issue found (searched `v1/export`, PR list June) | backlog issue #97 (created) |
| 3 | "Fixed the flaky invoice test" | conv "CI triage", 2026-06-20 | "fixed" | unknown | test unchanged since May (`git log tests/invoice.spec.ts`); no related PR. Resolves with: the fix commit SHA, or a re-run showing stability | backlog (re-opened) |
| 4 | Owner approved staging backfill runs | conv "backfill", 2026-06-28 | approval granted | active (grant unrecorded) | quoted grant in chat; nothing in repo | scoped-approval-register (entry drafted) |

Unresolved: item 3 (needs fix SHA or stability evidence).
Standing rule: tracked repo docs are the working record; this doc supersedes
the chats it drained. Next sweep: 2026-08-01 or phase close, whichever first.
```

Note item 3: the chat's "fixed" plus an unchanged test file does NOT yield
`not-active` (maybe it was fixed elsewhere) nor `completed` (no evidence) —
it yields `unknown` with the resolving artifact named. Note item 4: the sweep
does not RECORD the approval itself; it routes it to the register skill.

## Cadence guidance

- Default: per phase-close or monthly, whichever comes first; plus an
  ad-hoc sweep before resuming any work that lives mainly in old chats.
- Each sweep starts at the prior sweep's boundary. Overlap is allowed
  (dedup handles it); gaps are not — a gap is where decisions die.
- If the repo has agent-instruction files that sessions read at startup,
  the standing rule ("use tracked repo docs, not stale chat") belongs there
  too — one line with a pointer to the latest reconciliation doc.
