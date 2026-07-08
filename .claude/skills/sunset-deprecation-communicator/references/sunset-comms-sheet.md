# Sunset Comms Sheet

Detail for `sunset-deprecation-communicator`. Read on demand.

## Impact-assessment checklist

- Who uses it: segments, integrators, internal dependents.
- How much: volume/traffic, share of users, revenue attached.
- How hard to leave: shallow use vs deep integration/automation.
- Contractual: any agreement naming the feature/endpoint (→ commitment
  owner; a Stop Condition).
- Hardest-hit list: the few users who drive window length and outreach.

## Window length by impact

| Impact | Suggested deprecation window |
|---|---|
| Internal / trivial external use | Short (weeks) |
| Public API, moderate integration | Months; ≥ standing policy minimum |
| Public API, deep/contractual integration | Long (2+ quarters); targeted outreach |
| No parity replacement | Reconsider or extend; state honestly |

Always meet at least the standing policy's minimum
(`api-event-architect`). Hold the date; use grandfathering, not
date-slipping, as the pressure valve.

## Escalating communication schedule

| When | Channels | Message |
|---|---|---|
| Announcement | Blog/changelog, email, in-app | What, why, when, migration link |
| Deprecation start | Docs marked deprecated; API warnings/headers | Discouraged; migrate now |
| Mid-window reminders | Email, in-app, targeted outreach to heavy users | Date approaching; how to migrate |
| Final notice (e.g. T-2wk, T-2d) | Email, in-app banner | Firm date; help channel |
| Sunset day | Tombstone response; status/changelog | Retired on X; use Y |

Every message: what / why / when / what-to-do / where-to-get-help.

## API deprecation signals

- `Deprecation: <date>` and `Sunset: <date>` response headers (RFC-style)
  on the deprecated surface.
- `Link` header to the migration docs where supported.
- Changelog + versioned docs marking the version/endpoint deprecated.
- Optional: warning field in the response body during the window.

The header CONVENTIONS are api-event-architect's policy; this plan
applies them to a specific sunset.

## Post-sunset behavior

- Tombstone: an explanatory error/redirect ("this was retired on X; use
  Y") — never a silent 404 or generic 500.
- Monitor stragglers still calling the dead surface; consider one more
  targeted nudge before hard removal.
- Keep the migration docs live past the sunset for latecomers.

## Boundaries (repeat)

- Standing deprecation policy / versioning conventions → `api-event-architect`.
- Notification delivery system (channels, preferences, in-app center) →
  `notification-webhook-ux-designer`.
- Retiring a LIBRARY SKILL (reverse-link sweep, catalog rows,
  mark→redirect→remove) → `skill-deprecation-planner`.
