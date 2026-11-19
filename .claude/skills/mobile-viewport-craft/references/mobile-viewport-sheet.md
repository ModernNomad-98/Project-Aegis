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

Both columns are the SAME recorded arrangement: the recorded order and
prominence come from `screen-composition-designer` — app bar, the recorded
welcome hero and subhead, the recorded sign-up button, the recorded newsletter
card, the search field, the filter chips, and the 73-entry list. The comparison
measures two LAYOUTS of that one recorded arrangement: Candidate A renders the
recorded blocks at their recorded size, Candidate B renders the same recorded
order and prominence more compactly. It does not compare arrangements and it
does not decide what leads, what is deferred, or whether an intro is shown.

| Above-the-fold element | Candidate A — recorded arrangement at recorded size | Candidate B — same recorded arrangement, compact layout |
| --- | --- | --- |
| App bar | 56 | 56 |
| Title / intro (recorded) | hero headline + subhead ≈ 128 | compact rendering ≈ 96 |
| Hero media (recorded) | ≈ 288 | ≈ 200 |
| Search + filters | below the first viewport | search ≈ 48 + chips ≈ 40 (visible) |
| Primary app button (recorded) | ≈ 56 | ≈ 48 |
| Secondary card (recorded newsletter / sign-up) | ≈ 144 | ≈ 120 |
| List section header | — | ≈ 32 |
| Approximate used height | ≈ 700–712 incl. gaps (consumes the viewport) | ≈ 560 incl. gaps |
| Remaining before first scroll | ≈ 0–24 | ≈ 140–164 |
| Rows fully visible | 0 (no result row visible) | 0 (search, chips and header fit; no 56–72 px result row fits) |
| Primary task on entry | not visible or actionable | search visible; no result row visible, so selecting an entry is not actionable |

**The secondary-feature displacement test.** List every element whose top edge is
inside the first viewport; mark each primary or secondary. If a secondary
element consumes space that would otherwise show the primary content or its
first action, measure the cost at the real content volume and report the layout
options inside the same recorded order; moving it below the primary task,
deferring it, or putting it behind deliberate disclosure changes the
arrangement, so record the trade-off and hand that decision to
`screen-composition-designer`. Record the before/after counts and the
remaining trade-off. Repeat at the largest
supported text scale, where two-line rows grow and the visible row count drops.

**Overview/intro test.** An overview-first or intro-first first viewport is a
composition decision: `screen-composition-designer` records it, and this
skill checks the layout of the recorded choice. A recorded overview or intro is
legitimate when it carries a written reason tied to the brief — a monitoring
dashboard whose recorded job is several signals at a glance, or a first-run
orientation screen with a way past it (skip/exit); brand preference alone is
not sufficient when it delays the recorded primary task. If the recorded intro
stays, record what it costs at the real content volume (rows or actions below
the fold) and why that is acceptable; if no reason is recorded, surface the
missing arrangement decision to its owner instead of assuming it. Whether an
overview or intro is shown is never decided here: if the recorded arrangement
has no answer, surface the missing decision to `screen-composition-designer`.

**No universal above-the-fold button.** Do not turn this into "every screen
needs the primary button above the fold". Work from the recorded primary task:
list search and selection, record inspection, dashboard monitoring (signals
may be the recorded prominence) or reading (recorded content may lead). A
button is one possible control, not the rule.

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
