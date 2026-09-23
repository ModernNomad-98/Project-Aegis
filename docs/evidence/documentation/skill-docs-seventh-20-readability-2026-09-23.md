# Seventh 20 skill documents: bounded readability correction — 2026-09-23

## Scope and estimate

A read-only audit of the 20 sorted skill guides after
`product-analytics-instrumenter`, from `product-spec-writer` through
`rollback-runbook-author`, identified unclear authority and security/transport
shorthand. This writer batch changes only the [Query Plan Reader](../../../.claude/skills/query-plan-reader/SKILL.md),
[Reviewable Diff Discipline](../../../.claude/skills/reviewable-diff-discipline/SKILL.md),
[RAG Security Architect](../../../.claude/skills/rag-security-architect/SKILL.md),
[Realtime Subscription Architect](../../../.claude/skills/realtime-subscription-architect/SKILL.md),
and this dated note. The other 16 screened skills were not rewritten. The
coordinator owns any shared documentation readability ledger update.

The isolated worktree began from `origin/main` at
`e900a0455c5ee3bb138b9292a6bcb71cbdfe7be8`. Work started at
**2026-09-23 20:03:28 UTC** (Coordinated Universal Time). The previous sixth
batch estimate was **2–4 active hours**, and this bounded seventh batch is
estimated at **2–4 active hours**. The selected remaining backlog estimate at
start was **175–394 active hours**. These planning ranges are separate from
observed wall time; active-only labor is not instrumented.

## Contract-preserving changes

- The two manual-only skills spell out Task-Authorized Local Implementation
  (TALI) and link the [governing standard](../../skill-generation-standard.md#5-least-privilege--side-effects).
  Explicit invocation still does not activate TALI or expand the allowed
  target; existing-grant and state-changing-command checks remain.
- The RAG guide defines retrieval-augmented generation, access control list,
  the Open Worldwide Application Security Project (OWASP) LLM08 risk identifier,
  insecure direct object reference, and
  personally identifiable information. Its output labels spell out
  authorization and severity; retrieval-time filtering and negative tests
  remain required. The risk identifier is consistent with the repository's
  [OWASP reconciliation](../../reconciliation/step-0-reconciliation-v4.md).
- The realtime guide defines server-sent events, database, dead-letter queue,
  change data capture, time to live, load balancer, insecure direct object
  reference, and out of memory. Its output template expands transport,
  authorization, connection, and presence labels while preserving the
  per-tenant and per-user subscribe-time checks, backpressure, and replay.

The four frontmatter blocks, written in YAML (a text serialization format),
and eight trigger/behavior evaluation files
remain unchanged. The manual-only markers and disabled model invocation on
the two execution-capable skills remain. No skill was invoked, no provider
call or real-host action was made, and no credentials or private data were
accessed.

## Verification and timing

At the **20:05:44 UTC** local checkpoint, the observed start-to-checkpoint
wall interval was **2 minutes 16 seconds**. `python -B
scripts/validate-skills.py` passed with **185 valid skills and zero warnings**.
The four skill pages' **6 local links** resolved, including both TALI standard
anchors; the original 20-page screen's **40 local links** also resolved.
`git diff --check` passed, and status showed only the four authorized skill
paths before this note was added. Independent read-only review remains pending
before a local Developer Certificate of Origin signed commit. No push or pull
request is part of this writer batch. Independent coordinator review found the
first-use OWASP and YAML expansions missing; those were added, and no other
technical or authority blocker was reported. Exact-head review remains a
delivery gate.
