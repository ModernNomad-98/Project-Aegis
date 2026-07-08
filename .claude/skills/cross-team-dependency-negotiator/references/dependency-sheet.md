# Dependency Sheet

Detail for `cross-team-dependency-negotiator`. Read on demand.

## Dependency-map format (both ways)

```
| Dir | Deliverable | Team/Owner | By | Interface/contract | Critical? | Status |
|-----|-------------|-----------|----|--------------------|-----------|--------|
| NEED | auth token API | Platform / A. | wk6 | api-event-architect spec | yes | at-risk |
| OWE  | event schema  | to Data / B. | wk4 | tracking plan | yes | on-track |
```

Map what you OWE as rigorously as what you NEED — your slip is someone's
crisis.

## Concrete-commitment template

A commitment has all five, written down:
- **Deliverable** — the specific thing.
- **Interface/contract** — against what (so "done" is unambiguous).
- **Date** — when.
- **Owner** — named, both sides.
- **What-if-slips** — the agreed fallback/escalation.

"We'll help when we can" has none of these. Reject it as a plan.

## De-risking patterns

| Pattern | Turns… |
|---|---|
| Stub/mock the contract | Blocked-until-they-finish → build in parallel |
| Feature-flag the integration | Hard launch dependency → soft, toggled later |
| Parallel path | Serial wait → concurrent work |
| Fallback deliverable | Single point of failure → degraded-but-shipping |

Build against the CONTRACT, not their implementation, so their timeline
stops being your timeline.

## Accounting for their priorities

- Find where your ask sits on their backlog — honestly.
- Align incentives: why does helping you help them / the company?
- Offer a trade (you do X for them; they do Y for you).
- If still deprioritized: escalate to shared management for an EXPLICIT
  prioritization decision. Don't assume goodwill.

## Escalation-trigger design

Agree BEFORE you need it:
```
If <dependency> is at-risk by <date>:
  → notify <both owners + managers>
  → decide <reprioritize | fallback | move the date> by <date+N>
```
Escalation agreed in advance is routine; invented in a crisis it's a
blame fight.
