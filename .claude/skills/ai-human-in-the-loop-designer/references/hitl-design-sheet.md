# Human-in-the-loop design sheet

Detail for `ai-human-in-the-loop-designer`. Read on demand from the
workflow. AI means artificial intelligence; a proposal is an AI output held
as a suggestion that is not yet product state.

## 1. Classification rubric

Start every action at ADVISORY-ONLY (the AI suggests; a person performs the
action through the normal user interface). Move it only with a reason.

| Question | If yes | If no |
| --- | --- | --- |
| Could a person perform this action today with their own permissions? | continue | FORBIDDEN (the AI cannot gain an action nobody has) |
| Is it irreversible (money moved, message sent to someone outside the product, data destroyed)? | CONFIRM at most; FORBIDDEN if one reviewer cannot judge it | continue |
| Does it reach beyond one record or one user (whole tenant, many customers, another tenant)? | FORBIDDEN, or CONFIRM with a second reviewer if the tier allows | continue |
| Does the risk tier allow autonomy for this action? | AUTONOMOUS is possible | CONFIRM or ADVISORY-ONLY |
| Do the watch-and-undo controls exist (monitoring, sampling, undo window, pause thresholds)? | AUTONOMOUS | CONFIRM until they exist |

Examples:

| Action | Typical class | Why |
| --- | --- | --- |
| Suggest tags on a support ticket, user applies them | ADVISORY-ONLY | low impact; the user already performs it |
| Draft a reply the agent edits and sends | ADVISORY-ONLY | the person sends it |
| Issue a refund under a set amount | CONFIRM | money moves and cannot be recalled cleanly |
| Fill extracted invoice fields into a record | CONFIRM, or AUTONOMOUS with sampling when the tier allows | reversible, one record |
| Delete inactive customer accounts | FORBIDDEN | irreversible, wide blast radius, no single reviewer can judge "inactive" |
| Change another tenant's data | FORBIDDEN | crosses the tenant boundary |

## 2. Proposal lifecycle

```
created ──► pending ──► approved ──► committed
               │   └──► edited ────► committed (reviewer's version)
               ├──► rejected (reason recorded; nothing committed)
               ├──► expired  (nothing committed; owner notified)
               └──► stale    (base version changed) ──► re-checked → pending
                                                      └► expired
```

Rules:

- Only `committed` changes product state.
- `stale` is detected at commit time by comparing the stored base version
  with the current record, not only when the reviewer opens the item.
- A re-check creates a new proposal version; the reviewer sees what changed.

## 3. Proposal and queue item fields

| Field | Purpose |
| --- | --- |
| proposal id, version | stable reference for review and audit |
| tenant | scope check at review and commit |
| action and target record | what will change |
| before and after values (field level) | what the reviewer is approving |
| base version of the target | staleness check |
| side effects on commit | emails, payments, notifications the commit triggers |
| sources the AI relied on | the evidence the reviewer checks against |
| model and prompt version | traceability and evaluation |
| trigger identity | enforces no self-approval |
| created and expiry time | queue ordering and expiry |
| confidence or risk flags, if the feature has them | ordering, never auto-approval |

## 4. Audit record fields

Proposal id and version, action, tenant, trigger identity, reviewer
identity (and second reviewer where required), decision (approve, edit,
reject, expire, autonomous, undo), reason, before and after values, sources,
model and prompt version, and timestamps for creation, decision and commit.
Schema, storage and retention are designed by `audit-log-architect`.

## 5. Consent-fatigue signals

- CONFIRM volume per reviewer per hour against the budget set in the design.
- Approval rate per reviewer; near 100% over a long window is a warning.
- Median time to decision; seconds-long decisions on complex items mean the
  item is not being read.
- Bulk approvals attempted on high-blast-radius items (should be blocked).

These are design-time signals. Testing whether the flow can be gamed is
`human-agent-trust-reviewer`'s job.

## 6. Worked example: AI refund proposals

A support assistant reads a ticket and proposes a refund.

- **Classification:** refund is CONFIRM (money moves). Refunds above the
  plan's threshold are FORBIDDEN for the AI and stay a manual action. Ticket
  tags stay ADVISORY-ONLY.
- **Proposal:** amount, currency, order id, customer, the ticket text and
  order history the AI cited, base version of the order, expiry of 24 hours.
- **Queue:** support leads in the same tenant; each item shows the amount,
  the order, and the cited ticket lines; no bulk approval.
- **Who may review:** a support lead with refund permission. The agent who
  asked the AI to draft the refund cannot approve it.
- **Commit:** through the normal refund command, re-authorized as the
  approving lead, with an idempotency key.
- **Stale:** if the order was already refunded or changed, the proposal is
  re-checked or expired, never committed.
- **Audit:** every proposal and decision recorded with the fields in
  section 4.
