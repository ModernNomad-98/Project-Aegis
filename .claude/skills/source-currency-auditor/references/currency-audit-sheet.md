# Currency Audit Sheet

Use this reference with the [Source Currency Auditor](../SKILL.md).

Detail for `source-currency-auditor`. Read on demand.

API means application programming interface; URL means uniform resource
locator.

## Citation-class thresholds (by volatility)

| Fact class | Goes stale in | Suggested threshold |
|---|---|---|
| Prices / quotas / limits | weeks | very tight |
| Model ids / API versions | weeks–months | tight |
| Tool / library versions | months | months |
| Standard editions | years (irregular) | track via framework-edition-tracker |
| External docs/URLs (existence) | any time | flag for live check unless a dated verification is supplied |
| Foundational research | years | loose |

One flat threshold both over-nags stable facts and misses volatile ones.

## Flag taxonomy

| Flag | Meaning | Severity |
|---|---|---|
| STALE | Older than its class threshold; may still be valid | Re-verify |
| SUPERSEDED | A newer/replacement source exists; actively misinforms | High |
| BROKEN | Dead link / removed source; no backing | High |
| UNVERIFIED | No dated authoritative comparison is available; age alone does not certify current | Re-verify |

Broken and superseded outrank merely stale.

## Load-bearing × volatility priority

```
Priority = load-bearing-ness × volatility
```
- Stale core recommendation on a volatile fact → top.
- Stale footnote on a stable fact → bottom.
Order re-verification so wrongness cost drives effort.

## Flag, don't verify

Currency is confirmed only against the live source or a supplied dated
authoritative verification. This skill:
- Flags citations needing re-verification (with reason + priority).
- Does NOT certify "still current" from age or memory; live lookup is a
  separate authorized step.
- Does NOT edit/fix — re-verification and updates follow their own
  applicable authorization.

## Handoffs

- A flag that's specifically a framework EDITION change → deep dive via
  `framework-edition-tracker` (then `framework-mapping-refresher`).
- Skill quality (triggers/sections/evals) → `skill-quality-reviewer`.

## Cadence

State a re-run interval; tighter for skills carrying volatile facts
(prices, model ids). Currency is a habit, not a one-off.
