# Debt Ledger Template - technical-debt ledger with interest, cost, owner and priority

Concrete artifact guide for the `technical-debt-classifier` skill. Method and record guidance only: it never directs the skill to edit code, run commands, use the network or claim production authority.

## 1. Artifact fields

- **Debt type taxonomy (code, design, test, doc, infra, data)**
- **Evidence per item with file/link**
- **Interest: what worsens if deferred**
- **Principal/reversal cost estimate**
- **Owner and decision route**
- **Priority ranking and rationale**
- **Ledger update/review process**

## 2. Worked table (technical-debt ledger with interest, cost, owner and priority)

| ID | Type | Evidence | Interest | Reversal cost | Owner | Priority |
| --- | --- | --- | --- | --- | --- | --- |
| D-1 | design | duplicate order models | rising change cost | 3 sprints | platform | P1 |
| D-2 | test | flaky payment suite | release delay | 1 sprint | payments | P1 |

## 3. Construction steps

1. Collect candidate debt items from evidence, not opinion.
2. Classify each item with the taxonomy.
3. Attach evidence and affected components.
4. Estimate interest and reversal cost.
5. Assign owner and decision route.
6. Rank with an explicit frame.
7. Define ledger cadence and retirement rule.

## 4. Quality checks before returning

- Every item has evidence and a type
- Interest and cost estimates are separate
- Owner and decision route are named
- Ranking is explained not asserted
- Retired items are removed or marked

## 5. Failure/gotcha handling

- Debt without evidence is a wish list
- Interest and principal conflated produce wrong priorities
- A ledger nobody reviews becomes stale in one quarter

## 6. Boundaries

- principal code analyst requests route to `principal-code-analyst`; this skill does not perform that owner work.
- full codebase auditor requests route to `full-codebase-auditor`; this skill does not perform that owner work.
- staff scope selector requests route to `staff-scope-selector`; this skill does not perform that owner work.
- prioritization frame picker requests route to `prioritization-frame-picker`; this skill does not perform that owner work.
- code reviewer requests route to `code-reviewer`; this skill does not perform that owner work.
- architecture designer requests route to `architecture-designer`; this skill does not perform that owner work.
- Broader eval-only discrimination set from evals/trigger-evals.json: `adr-writer`, `architecture-designer`, `change-classification-gate`, `code-reviewer`, `design-review-facilitator`, `full-codebase-auditor`, `human-approval-boundary`, `principal-code-analyst`, `prioritization-frame-picker`, `release-readiness-reviewer`, `roadmap-under-uncertainty-planner`, `rollback-runbook-author`, `staff-scope-selector`, `tech-spec-writer` (neighbours for discrimination, not in-scope work).
- No production, deployment, spending or approval authority is granted by this reference.
