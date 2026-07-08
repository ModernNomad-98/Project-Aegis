# Mobile Viewport Sheet

Detail tables for `mobile-viewport-craft`. Read on demand.

## Breakpoints — content-driven, not device-driven

- Design mobile-first; add a breakpoint where THIS layout breaks (line
  length, cramped columns), not at a phone's pixel width.
- Prefer `min-width` (mobile-first) media queries; enhance upward.
- Reach for **container queries** when a component's layout depends on its
  own available space (a card in a sidebar vs a full row), not the
  viewport's.
- Keep the count small; each breakpoint is a layout you must maintain.

## Viewport unit cheat sheet (the 100vh trap)

| Unit | Meaning | Use for |
|---|---|---|
| `vh` / `100vh` | Largest viewport (URL bar collapsed) — **clips on mobile** | avoid for full-height mobile |
| `svh` | Small viewport (URL bar shown) | guarantees visible; safe minimum |
| `lvh` | Large viewport (URL bar hidden) | max height |
| `dvh` | Dynamic — tracks current chrome | full-height panels, drawers, hero |

Rule: full-height mobile layouts use `dvh` (or `svh` when you must never
overflow). `100vh` is the classic "bottom cut off" bug.

## Safe areas

```css
padding-bottom: env(safe-area-inset-bottom);
padding-top:    env(safe-area-inset-top);
```
- Needed for notches, rounded corners, and the home indicator.
- Requires `viewport-fit=cover` in the viewport meta.
- Apply to fixed headers/footers and full-bleed content.

## Touch targets

- Minimum ~44×44px (iOS HIG) / 48dp (Material) with spacing between
  adjacent targets.
- The HIT AREA must match the visual — pad the control, don't rely on the
  glyph. Two 44px targets with no gap still cause mis-taps.
- Place primary actions in the thumb-reachable zone (bottom third on
  large phones); top corners are a stretch one-handed.

## Input types / keyboard

| Field | `type` / `inputmode` | Effect |
|---|---|---|
| Email | `type=email` | @ + .com keyboard |
| Phone | `type=tel` | numeric dial pad |
| Number/amount | `inputmode=numeric` / `decimal` | number pad |
| URL | `type=url` | / and .com |
| Search | `type=search` | "Go"/"Search" key |

- Input font-size **≥16px** or iOS auto-zooms on focus.
- Scroll the focused field above the on-screen keyboard (it covers ~40%
  of the screen); watch fixed "Save" bars.
- Set `autocomplete`/`autofill` tokens so the platform can fill.

## Hover & gestures

- Every hover-only affordance (tooltip, menu, row action) needs a
  touch-reachable equivalent — there is no hover on touch.
- Custom gestures must be discoverable (affordance/hint) and must not
  conflict with browser gestures: edge back-swipe, pull-to-refresh,
  overscroll.
- Long-press as the ONLY path to an action is undiscoverable; pair it with
  a visible control.

## Wide-table reflow options

| Pattern | How | Best when |
|---|---|---|
| Stack-to-cards | Each row becomes a labeled card | Few columns matter per row |
| Scroll + frozen column | Horizontal scroll, key column pinned | Many columns, comparison needed |
| Priority collapse | Show top columns; expand row for the rest | One key metric + details |

Never hide a critical column or action just to fit. State the tradeoff of
the chosen pattern.

## Orientation & text scaling

- Rotation must not lose state or break layout.
- Respect OS text-size / browser zoom; layout must not clip or overlap at
  200% (record as a11y intent → `accessibility-test-harness` verifies).
