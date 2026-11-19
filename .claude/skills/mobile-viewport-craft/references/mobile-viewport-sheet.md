# Mobile Viewport Sheet

Use these tables with [mobile viewport craft](../SKILL.md) to choose layout,
safe-area, and touch behavior for small screens. **URL** means Uniform Resource
Locator (web address),
**HIG** means Human Interface Guidelines, **OS** means operating system, and
**a11y** abbreviates accessibility. In the touch-target row, **dp** means
density-independent pixels; the viewport-height units are defined below.

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

## First viewport — worked comparison (390×844 phone)

Assumptions: 390×844 CSS px (a common small phone); browser chrome with the
URL bar shown takes roughly 120 px, so the guaranteed visible content height
is about 700–724 px — use `svh` for the guaranteed region and `dvh`
for a panel that must track the chrome. Text at 100% scale; 16 px body text;
32 px horizontal padding. Content is the guide fixture shape: **73 entries**,
at least 12 long titles that wrap to two lines, single-line rows about 48–56 px
and two-line rows about 64–72 px, a search field 44–48 px, a filter-chip row
36–40 px and an app bar 52–56 px.

| Above-the-fold element | Candidate A — welcome hero first | Candidate B — task first |
| --- | --- | --- |
| App bar | 56 | 56 |
| Title / intro | hero headline + subhead ≈ 108 | compact title ≈ 32 |
| Hero media | ≈ 160 | — |
| Search + filters | below the first viewport | search ≈ 48 + chips ≈ 40 |
| Primary app button | ≈ 48 | search is the primary action |
| Secondary card (newsletter / sign-up) | ≈ 120 | below the list or deferred |
| List section header | — | ≈ 32 |
| Approximate used height | ≈ 552 incl. gaps | ≈ 232 incl. gaps |
| Remaining before first scroll | ≈ 150–170 | ≈ 470–490 |
| Rows fully visible | 0 (search partly cut) | 6–8 at 56–72 px |
| Primary task on entry | not visible or actionable | find/select an entry is visible and actionable |

**The secondary-feature displacement test.** List every element whose top edge is
inside the first viewport; mark each primary or secondary. If a secondary
element consumes space that would otherwise show the primary content or its
first action, move it below the primary task or put it behind deliberate
disclosure, then re-measure; record the before/after counts and the remaining
trade-off. Repeat at the largest supported text scale, where two-line rows grow
and the visible row count drops.

**Overview/intro test.** An overview-first or intro-first first viewport is
legitimate only with a written reason tied to the brief: a monitoring
dashboard whose primary job is several signals at a glance, or a first-run
orientation screen with a way past it (skip/exit). Brand preference alone is
not sufficient when it delays the primary task; if the intro stays, record
what it costs (rows or actions below the fold) and why that is acceptable.

**No universal above-the-fold button.** Do not turn this into "every screen
needs the primary button above the fold". Name the actual primary task first:
list search and selection, record inspection, dashboard monitoring (signals
may be the prominence) or reading (content may lead). A button is one possible
control, not the rule.

## Safe areas

```css
padding-bottom: env(safe-area-inset-bottom);
padding-top:    env(safe-area-inset-top);
```
- Needed for notches, rounded corners, and the home indicator.
- Requires `viewport-fit=cover` in the viewport meta.
- Apply to fixed headers/footers and full-bleed content.

## Touch targets

- iOS hit region generally at least 44×44 points (pt); apply the platform's
  corresponding web/CSS sizing rules and Material's 48dp guidance, with spacing between
  adjacent targets.
- The hit area may exceed the visual glyph; pad the control. Adjacent targets
  with no gap can still cause mis-taps.
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
