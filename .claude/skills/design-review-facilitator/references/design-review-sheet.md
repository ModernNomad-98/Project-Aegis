# Design Review Sheet

Detail for `design-review-facilitator`. Read on demand.

The owning [design review skill](../SKILL.md) defines the meeting and decision
workflow. Pre-read means material circulated before the review; HiPPO means
highest-paid person's opinion; ADR means architecture decision record.

## Preparation checklist

- [ ] Design circulated with a REQUIRED pre-read by an authorized sender (or postpone).
- [ ] Purpose stated: what decision must this review reach?
- [ ] Right people invited by an authorized sender: domain owners, skeptics, cross-cutting owners
      (security, data, ops) — not just allies.
- [ ] Reversibility/stakes assessed → sets scrutiny depth.
- [ ] Time-box and an explicit outcome expected.

## Anti-pattern countermeasures

| Anti-pattern | What it looks like | Counter |
|---|---|---|
| Rubber stamp | Approved because the author is senior | Require reasoning; invite skeptics; probe risks |
| Bikeshed | Hour on trivia; risks unaddressed | Steer time to expensive-to-reverse parts |
| HiPPO | Highest-paid opinion ends it | "What's the argument?" not "what does X think?" |
| No decision | Great chat, decides nothing | Force approved/changes/rework/blocked |
| Silent flaw | Nobody voices the objection | Actively elicit the strongest objection |

## Outcome taxonomy

| Outcome | Meaning | Next |
|---|---|---|
| Approved | Build it as designed | Record decision (adr-writer) |
| Approved-with-changes | Build only with the bounded changes listed in the decision | Owner applies listed changes; re-review if they alter the agreed design, risk or authority boundary |
| Needs-rework | Material issues | Author revises; re-review |
| Blocked-on-X | Can't decide until X | Name X + owner + date |

Always land on exactly one. "Circle back" is not an outcome.

## Facilitation prompts (elicit dissent)

- "What's the strongest reason this is the wrong approach?"
- "<Domain expert>, what worries you about the data/security/rollout?"
- "If this fails in production, what's the most likely cause?"
- "What are we assuming that might not hold?"
- "What did we NOT consider?"

## Capture format

```
Decisions: <what was decided> → adr-writer for binding ones
Actions:   <item — owner — date>
Open Qs:   <question — owner>
Outcome:   <one of the taxonomy>
```

A review whose outcome isn't written down didn't happen.
