# Edge State Sheet

Detail tables for `edge-state-ux-designer`. Read on demand.

## Full state checklist (per view)

Decide each IN or OUT with a reason — never by omission.

- **uninitialized** — before any fetch starts (often instant; may not need art).
- **loading (first)** — first load, no prior data → skeleton/spinner.
- **empty (first-run)** — never had data → onboarding copy + create/import CTA.
- **empty (filtered)** — filter/search matched nothing → clear-filter affordance.
- **empty (error-emptied)** — load failed, so nothing to show → this is an ERROR.
- **loaded (partial)** — some regions/widgets loaded, some failed.
- **loaded (full)** — the happy path.
- **refetching / stale** — background refresh over existing data.
- **error (whole-view)** — the view's primary data failed → full-view error + retry.
- **error (partial)** — one region failed → scoped error, page survives.
- **offline** — no connectivity → distinct from a server error.
- **permission-denied (forbidden)** — 403 → NOT empty, NOT not-found.

## The three empties — never one state

| Empty | Trigger | Copy intent | Primary action |
|---|---|---|---|
| First-run | User/tenant has never created data | "Get started" — warm, instructive | Create / import / invite |
| Filtered | Query/filter excluded everything | "No matches for X" — point at the filter | Clear / adjust filters |
| Error-emptied | Load failed | "Couldn't load" — this is a failure | Retry (+ correlation id) |

Collapsing these confuses users: filtered-empty that reads like first-run
makes people think their data vanished; error-emptied shown as a cheerful
empty hides a real failure.

## Loading pattern selection

| Pattern | Use when | Notes |
|---|---|---|
| Skeleton | Layout known, content shape stable | Reserves space, no layout shift; best default for content |
| Spinner | Short wait, unknown/variable shape | Fine for buttons, small regions |
| Inline indicator | Background refresh over existing data | Keep last-good visible |
| Progress | Long, measurable operation | Show progress, not an indefinite spinner |

Apply a **delay threshold** (~150–300ms) before showing a loader so fast
responses don't flash one. Don't flash back to a skeleton on every
refetch — indicate "refreshing" subtly instead.

## Error placement by blast radius

| Scope | Surface | Notes |
|---|---|---|
| One field | Inline, at the field | From validation.* codes |
| One action | Toast | Add retry if the code is retryable |
| One region/widget | Scoped error in that region | Page survives (partial failure) |
| Whole view | Full-view error | Retry + correlation id to quote support |
| Session/auth lost | Full-view / redirect | Re-auth path, not a generic error |

## Copy patterns

- Empty (first-run): what this is for + one clear next step.
- Empty (filtered): name the active filter; offer to clear it.
- Error: what happened (in user terms) + retry + correlation id; NEVER the
  raw taxonomy detail or internals (that boundary is
  `error-taxonomy-designer`'s disclosure rule).
- Offline: "You're offline" + what still works locally, if anything.
- Forbidden: "You don't have access" + how to request it; avoid revealing
  whether the resource exists if the viewer isn't allowed to know.

## Accessibility intent (design here, VERIFY in accessibility-test-harness)

- Loading: `aria-busy` / polite live region so the wait is announced.
- Error: move focus to the error, announce it (assertive where urgent).
- Empty: not a purely visual illustration — include a text alternative.
- Retry/CTA: real, focusable, labeled controls.

Record these as intent; `accessibility-test-harness` designs the pass
that checks them.
