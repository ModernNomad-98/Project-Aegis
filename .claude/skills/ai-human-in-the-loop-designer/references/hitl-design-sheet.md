# Human-in-the-loop design sheet

Detail for `ai-human-in-the-loop-designer`. Read on demand from the
workflow. AI means artificial intelligence; a proposal is an AI output held
as a suggestion that is not yet product state. AUTONOMOUS means the AI acts
alone while a person watches; CONFIRM means a person approves first;
FORBIDDEN means never. A tenant is one customer organization whose data the
product keeps apart; blast radius is how much harm one wrong action can do.

## 1. Classification rubric

Start every action at ADVISORY-ONLY (the AI suggests; a person performs the
action through the normal user interface). Move it only with a reason.

| Question | If yes | If no |
| --- | --- | --- |
| Could a person perform this action today with their own permissions? | continue | FORBIDDEN (the AI cannot gain an action nobody has) |
| Does the applicable written policy or the risk tier bar it? | FORBIDDEN | continue |
| Does it reach another tenant's data? | FORBIDDEN | continue |
| Is it irreversible OR non-compensable OR not judgeable by one reviewer? | FORBIDDEN | continue |
| Does it reach beyond one record or one user? | FORBIDDEN | continue |
| Is it a single-record action that is reversible AND compensable AND judgeable by one reviewer, and does written policy permit it with approval (e.g. a refund under a set amount)? | CONFIRM | continue |
| Does a written policy require approval, or is there no written policy explicitly permitting autonomy? | CONFIRM | continue |
| Does the risk tier allow autonomy AND is the action reversible AND compensable AND do the watch-and-undo controls exist AND does written policy explicitly permit autonomy? | AUTONOMOUS | CONFIRM or ADVISORY-ONLY |

A single-record action that is reversible AND compensable AND judgeable by one
reviewer, and that written policy permits with approval, is CONFIRM. Any action that
is irreversible, non-compensable, cross-tenant, wide-blast-radius, or not judgeable by
a single reviewer is FORBIDDEN regardless of approval or policy.

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

Timing/bulk approval is a signal that triggers inspection, never proof of fatigue or approval quality (shared rule with agent-governance-audit and human-agent-trust-reviewer).

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
## Canonical class/eligibility/blast/batch rules (R8-CONV-4)

Class order: FORBIDDEN first, then the AUTONOMOUS gate, else CONFIRM default; a class is never downgraded by availability. eligible_reviewer = active, unexpired, in-scope authority in the tenant, not requester/triggerer/service account. Reviewer_candidate = a proposed reviewer; eligible_reviewer = candidate with active, unexpired, in-scope tenant authority, not requester/triggerer/service account. If no eligible reviewer candidate exists at all the action is FORBIDDEN (not judgeable) with named owner escalation; a candidate that is ineligible => CONFIRM pending escalation; a candidate that is eligible but unavailable => CONFIRM pending recorded availability. wide_blast_radius = more than one record/user OR aggregate/batch OR cross-tenant OR unrecorded/unbounded; wide is never AUTONOMOUS; inherently FORBIDDEN => FORBIDDEN; otherwise CONFIRM only after recorded reduction to one record/user. CONFIRM batch exception: a multi-record batch is never AUTONOMOUS; it is CONFIRM (not FORBIDDEN for wideness alone) only when all four conditions hold (reversible AND compensable AND judgeable for every action; written policy explicitly permits the batch; eligible reviewer can judge the aggregate; one recorded aggregate confirmation); any FORBIDDEN action makes the batch FORBIDDEN.
