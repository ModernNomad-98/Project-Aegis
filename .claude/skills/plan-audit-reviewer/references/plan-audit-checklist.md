# Plan audit checklist reference

## Audit dimensions
1. Completeness: objective, necessity/reuse answers, scope/non-goals, blast radius, inventory, counts, gates, closures, owner decisions, verification.
2. Feasibility: every claimed file/count/gate is measured at the claimed base; deltas are mechanically achievable; protected paths identified.
3. Authority/boundary: no self-approval; owner decisions surfaced with sources; protected-path and approval routes named; no merge/approval authority claimed.
4. Acceptance observability: each criterion names an observable result and the evidence that proves it.
5. Closure validity: each closure executed on the clean base and fails; after-state expectations are specific and executable.
6. Owner-decision disclosure: defaults and consequences recorded; no decision taken by the agent.
7. Evidence binding: identities measured after final edits; non-circular (INDEX no own/binding hash; final neither own nor binding hash).

## Verdict rules
- CONFIRM only when every dimension passes and no material defect remains.
- REVISE when a material defect is reproducible and fixable without redesign; enumerate the minimal fixes.
- REJECT when the plan's premise or authority is unsound.
- Bind the verdict to the captured revision hash; any post-capture edit voids it.

## Backlog-input routing
Findings are evidence for the existing backlog: dedupe first, owner-ordered queue only, never a second queue or execution plan. Record provider, comment/report id, head, disposition and reason.

## What the auditor must not do
- Do not edit the plan or capture, implement, push, approve or merge.
- Do not accept presence as proof; re-run the checks and cite observed output.
- Do not substitute an advisory review for the owner's decision.
