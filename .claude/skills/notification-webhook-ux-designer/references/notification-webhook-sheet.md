# Notification & Webhook UX Sheet

Detail tables for `notification-webhook-ux-designer`. Read on demand.

## Channel / default posture matrix

| Category | In-app | Email | Push | Default | Opt-out? |
|---|---|---|---|---|---|
| Security (new-device login, password change) | yes | yes | yes | on | No (labeled) |
| Transactional (receipt, failed payment) | yes | yes | optional | on | No (labeled) |
| Direct (mention, assignment, DM) | yes | opt | opt | on | Yes |
| Activity (comment, reaction, follow) | yes | digest | off | digest | Yes |
| Product/marketing (tips, announcements) | opt | opt-in | off | off/opt-in | Yes (one-click) |

"Non-optional" categories still deliver on opt-out but must be clearly
labeled as security/transactional so expectations are set.

## Realtime vs digest decision

| Signal | Realtime | Digest |
|---|---|---|
| Urgency | High / time-critical / security | Low, informational |
| Volume | Low, individually meaningful | High, individually trivial |
| Action needed | Immediate | Review-later |
| Example | Failed payment, mention | "12 people viewed your post" |

Criticality overrides batching: never digest a security or
payment-failure notice. Let users choose realtime vs digest cadence for
the low-urgency band.

## Collapse / dedup patterns

- **Aggregate:** "3 people reacted to X" (one item, a count) not three items.
- **Supersede:** a later state replaces an earlier one ("build failed" →
  "build passed on retry") rather than stacking.
- **Thread:** group by object (all activity on one document → one
  expandable item).
- **Frequency cap:** at most N notifications per object per window.

## Webhook delivery-log fields (developer view)

| Field | Purpose |
|---|---|
| Event type + id | What fired |
| Timestamp | When |
| Endpoint | Which subscription |
| Response status | 2xx / 4xx / 5xx / timeout |
| Latency | Consumer responsiveness |
| Attempt count | Which retry (retry policy = api-event-architect) |
| Payload | Inspect the exact body sent (signed per contract) |
| Actions | Replay this delivery; copy payload |

Replay note: manual replay re-sends the SAME event; it is safe only
because the consumer is idempotent (a contract requirement, not an
option). Surface that caveat next to the replay control.

## Signing-secret rotation UX

1. Show current secret presence (reveal-once on creation).
2. "Rotate" generates a new secret; BOTH old and new are valid during an
   overlap window (dual-valid) so in-flight deliveries verifying the old
   secret succeed.
3. After the window, the old secret is retired.
4. Verification instructions (how to check the signature) are discoverable
   from this screen; the algorithm itself is api-event-architect's.

## Boundaries (repeat)

- Delivery contract (envelope, signing algorithm, retry/at-least-once,
  versioning, subscription scoping) → `api-event-architect`.
- Empty/loading/error rendering of these screens → `edge-state-ux-designer`.
- Internal on-call alerts (worker backlog, error-rate pages) →
  `observability-operator` / `slo-reliability-architect`.
