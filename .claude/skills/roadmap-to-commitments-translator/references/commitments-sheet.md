# Commitments Sheet

Detail for `roadmap-to-commitments-translator`. Read on demand.

## Commit-able criteria (all three)

An item becomes a COMMITMENT only if:
1. **High confidence** — the team knows how to build it.
2. **Capacity-backed** — it fits real available capacity (below).
3. **Dependency-clear** — no uncommitted external dependency gates it.

Miss any → it stays directional, explicitly.

## Capacity-math worksheet

```
Raw capacity        = team size × sprint velocity (from EVIDENCE, not hope)
  − maintenance/support load
  − interrupt/on-call load
  − risk buffer (higher if past commitments missed)
= Committable capacity
```

Committable capacity is always well below headcount. Commit to that, not
to the best case.

## Outcome → deliverable translation

| Roadmap (theme/outcome) | Commitment (deliverable + range) |
|---|---|
| "Improve onboarding" | "Ship the new onboarding flow, weeks 6–8" |
| "Reduce checkout friction" | "Launch one-page checkout to 50%, weeks 4–6" |
| "Explore AI assist" | (stays directional — not committable) |

Commit to a concrete, verifiable deliverable with an honest RANGE.

## Date discipline

- Ranges ("weeks 6–8"), not false-precise single dates, on multi-week
  uncertain work.
- Precision only where confidence supports it.
- A padded single date is a hidden over-commitment.

## Gap communication

State BOTH lists, always:
```
COMMITTED (we will deliver): <...>
NOT COMMITTED (directional, and why): <item — capacity | dependency | uncertainty>
```
The unstated gap is where stakeholders invent promises you never made.

## Over-commitment tradeoff (when asked for more than capacity)

Present, don't pad:
- Commit to fewer items, or
- Add capacity (people/time), or
- Explicitly accept lower confidence on the extra (labeled as such).

Escalate the choice; never manufacture a commitment by padding.
