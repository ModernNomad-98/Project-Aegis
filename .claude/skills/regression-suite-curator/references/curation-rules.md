# Curation Rules

Use this reference with the [Regression Suite Curator](../SKILL.md). Loaded
on demand.

## Promotion rules

| Trigger | Rule |
| --- | --- |
| Bug fixed (severity at or above the agreed threshold) | regression test exists at the layer that would have caught it, or a work item is filed — no fix closes without one (the regression-first rule; `roadmap #190` is historical planning context, not a current gate) |
| Incident postmortem | named untested paths → tests promoted to the tier the postmortem implies (usually PR or smoke) |
| Smoke candidacy | proves a critical journey or invariant; runtime-cheap; historically stable; each member has a one-line reason |
| Security negative test | permanent by default on arrival (from multi-tenant-security-tester / incident fixes) |

## Retirement evidence standards

A retirement decision requires ALL of:

1. Category named: dead feature / duplicate / theater / unreachable.
2. Evidence: feature-removal PR link; the surviving duplicate cited with
   assertion comparison; theater rubric result; reachability argument.
3. Protection-lost statement: what bug class becomes undetected, and why
   that is acceptable now.
4. Protected-class check: security/compliance guards → human-approval-boundary.

"Slow" and "flaky" are NOT retirement categories — they are inputs to
demotion (tier change) or `flaky-test-detective` casework respectively.

## Quarantine registry schema

`{test id, quarantined date, owner, ticket, expiry, reason, case status}`

Enforcement loop each curation pass: expired → decision required now
(diagnose / fix / retire-with-rationale). An entry missing owner/ticket/
expiry is not quarantined — it is hidden red, and gets surfaced as such.

## Tier-fit worksheet

Per tier: budget (from the automation blueprint) vs sum of member runtimes.
Overflow resolution order:

1. Retire decided-retirements first (free protection-neutral wins).
2. Consider demotion only when equivalent surviving coverage is demonstrated
   by assertion and failure-mode comparison, and the next tier still meets
   the required detection time. A test's never-failed history or proximity
   to a similar test is insufficient; protected tests retain their gate
   unless the applicable owner approves a change.
3. Parallelize/shard (architecture change → qa-automation-architect).
4. Only then trade protection — escalated, never silent.

Catch-rate-per-runtime = (real failures caught historically) / (runtime ×
run frequency); use as a ranking aid, never as the sole retirement basis
(see never-fails gotcha).
