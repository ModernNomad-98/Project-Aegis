---
name: mobile-viewport-craft
description: Design the mobile and responsive viewport craft for a web UI — a content-driven breakpoint strategy (mobile-first; breakpoints where the layout breaks), touch-target sizing and spacing, safe-area/notch handling, the dynamic-viewport-unit fix for the URL-bar resize (the 100vh trap → svh/lvh/dvh), input behavior (right types, no focus-zoom, keyboard occlusion), hover-absence (no hover-only affordances) and gestures, and responsive layout patterns (reflow, wide tables, orientation). Produces a per-surface viewport/touch craft spec. Owns layout/touch/viewport CORRECTNESS on small screens; mobile page WEIGHT and network cost are frontend-perf-engineer's. Use when designing responsive layout, breakpoints, or touch interactions, or when a UI overflows, mis-sizes taps, or hides content behind browser chrome. Do NOT use for mobile performance/bundle weight (frontend-perf-engineer), non-happy-path states (edge-state-ux-designer), or accessibility VERIFICATION (accessibility-test-harness).
---

# Mobile Viewport Craft

## Purpose

The desktop layout "works on mobile" until a real thumb hits it: taps
land on the wrong control because targets are 24px and crammed together,
a full-height panel is cut off because `100vh` includes the space the
browser's URL bar will later reclaim, the bottom action button sits
under the home indicator, and a hover-only menu simply never opens
because touch has no hover. This skill produces the viewport craft for a
web surface — a content-driven breakpoint strategy, touch-target sizing,
safe-area and dynamic-viewport-unit handling, input/keyboard behavior,
hover-absence and gesture design, and the responsive layout patterns for
reflowing real content (including wide tables) onto small screens. It
owns layout, touch, and viewport CORRECTNESS; the page's WEIGHT and
network performance on mobile are `frontend-perf-engineer`'s.

## Use When

- Use when: designing responsive layout or a mobile breakpoint strategy,
  or making a desktop-first UI work on phones/tablets.
- Use when: designing touch interactions — target sizing, thumb reach,
  gestures — or replacing hover-only affordances for touch.
- Use when: a UI overflows horizontally, mis-sizes tap targets, or hides
  content behind the mobile browser chrome / notch / home indicator (the
  `100vh` trap).
- Use when: designing form input behavior on mobile — keyboard types,
  focus-zoom, the focused field hidden behind the on-screen keyboard.
- Use when: reflowing wide content (tables, dashboards) onto small
  screens, or supporting orientation and OS text-scaling.
- Do NOT use when: the task is mobile PERFORMANCE — bundle weight, image
  payload, JS execution cost on low-end devices — that is
  `frontend-perf-engineer`; this skill owns layout/touch, not kilobytes.
- Do NOT use when: the task is the view's empty/loading/error STATES —
  that is `edge-state-ux-designer`; those states still need mobile craft,
  but the state design itself is separate.
- Do NOT use when: the task is VERIFYING accessibility (screen-reader,
  contrast, keyboard) as a test pass — that is `accessibility-test-harness`;
  this skill designs touch/viewport craft and notes a11y intent (target
  size, zoom-safety) that the harness then checks.

## Inputs to Inspect

1. The real device/context mix for this product (from usage data if
   available): which viewport widths, OS/browsers, and input modes
   actually matter, and the minimum supported width.
2. The surfaces in scope and their content: navigation, forms, data
   tables/dashboards, media — each has different reflow needs.
3. The existing layout system: CSS approach (fl/grid, framework), current
   breakpoints, use of viewport units, and any known mobile breakage
   (horizontal scroll, clipped panels, tiny taps).
4. Interaction inventory: anything currently hover-dependent (tooltips,
   dropdowns, row actions), custom gestures, and fixed/sticky elements
   that interact with the keyboard.
5. Constraints from siblings: `frontend-perf-engineer`'s device/network
   class (so the craft targets the same baseline), and any a11y
   obligations (target size, 200% zoom) that `accessibility-test-harness`
   will verify.

## Workflow

1. **Set the target context and go mobile-first.** State the minimum
   supported width, the device/input classes that matter, and design up
   from the smallest — progressive enhancement, not desktop shrunk down.
2. **Choose breakpoints by content, not devices.** Add a breakpoint where
   THIS layout starts to break (line length too long, columns too
   cramped), not at a list of named phone widths that dates instantly.
   Fluid between breakpoints; reach for container queries when a
   component's layout depends on its own space, not the viewport's.
3. **Design touch targets.** Minimum hit area (~44×44px guideline) with
   adequate spacing so adjacent targets aren't mis-hit; put primary
   actions in the thumb-reachable zone; ensure the tappable area matches
   the visual (padding, not just the icon glyph).
4. **Handle the viewport chrome honestly.** Replace `100vh` with dynamic
   viewport units (`dvh`/`svh`/`lvh`) so full-height layouts account for
   the collapsing URL bar; apply `safe-area-inset-*` for notches and the
   home indicator; verify fixed headers/footers don't cover content or
   collide with the keyboard.
5. **Design input and keyboard behavior.** Correct input types and
   `inputmode` for the right on-screen keyboard; input font-size that
   avoids iOS focus-zoom (≥16px); ensure the focused field scrolls above
   the keyboard rather than hiding behind it; sensible autofill/
   autocomplete.
6. **Eliminate hover dependence and design gestures.** Every hover-only
   affordance (tooltip, menu, row action) needs a touch-reachable
   equivalent (tap, disclosure, long-press with a visible alternative).
   Custom gestures must be discoverable and must not fight the browser's
   own (back-swipe, pull-to-refresh, scroll).
7. **Reflow real content.** Choose reflow (stack columns) vs hide
   (progressive disclosure — never hide a critical action). For wide
   tables pick a pattern deliberately: stack-to-cards, horizontal scroll
   with a frozen key column, or priority-column collapse — and state the
   tradeoff. Long forms, nav (bottom-bar vs hamburger), and responsive
   media all get an explicit pattern.
8. **Support orientation and OS text-scaling.** Rotation doesn't break
   layout or lose state; respect OS text-size / browser zoom (don't clip
   or overlap at 200%) — record this as a11y intent for
   `accessibility-test-harness` to verify.
9. **Name boundaries and deliver** the per-surface craft spec: weight/
   network → `frontend-perf-engineer`; states → `edge-state-ux-designer`;
   a11y verification → `accessibility-test-harness`.

Breakpoint patterns, the touch-target and safe-area reference, the
viewport-unit cheat sheet, and wide-table reflow options:
[references/mobile-viewport-sheet.md](references/mobile-viewport-sheet.md).

## Output Format

```
MOBILE VIEWPORT CRAFT — <surface(s)>
Targets:      min-width=<n>; device/input classes; mobile-first stated
Breakpoints:  <content-driven list + rationale>; container queries where component-scoped
Touch:        min target ~44px + spacing; thumb-zone for primaries; hit-area = visual
Viewport:     100vh → dvh/svh/lvh; safe-area-inset applied; fixed elements vs keyboard checked
Input:        input types/inputmode; font-size ≥16px (no focus-zoom); focused field above keyboard
Hover/gesture: hover-only affordances → touch equivalents; custom gestures discoverable, no browser conflict
Layout:       reflow-vs-hide per region; wide-table pattern chosen (cards|scroll+frozen|priority) w/ tradeoff;
              nav pattern; responsive media
Orientation:  rotation-safe; OS text-scale/200% zoom respected (a11y intent)
Boundaries:   weight/network → frontend-perf-engineer; states → edge-state-ux-designer;
              a11y verify → accessibility-test-harness
```

## Validation Checklist

- [ ] Design is mobile-first with a stated minimum width; breakpoints are
      content-driven, not a list of device widths.
- [ ] Touch targets meet a minimum size with spacing, and the tappable
      area matches the visual; primaries are thumb-reachable.
- [ ] Full-height layouts use dynamic viewport units, not `100vh`; safe-
      area insets are applied for notch/home-indicator.
- [ ] Inputs use correct types, avoid focus-zoom (≥16px), and the focused
      field is not hidden behind the on-screen keyboard.
- [ ] No affordance is hover-only; each has a touch equivalent, and custom
      gestures don't conflict with browser gestures.
- [ ] Wide content has a deliberate reflow pattern with its tradeoff
      stated; nothing critical is hidden to "fit".
- [ ] Orientation change is safe and OS text-scaling/200% zoom doesn't
      clip or overlap (recorded for a11y verification).
- [ ] Weight/performance, state design, and a11y verification are handed
      to their owning skills, not solved here.

## Gotchas

- `100vh` on mobile is taller than the visible viewport because it
  includes the space the URL bar will reclaim — the bottom of a
  full-height layout gets cut off or sits under browser chrome. `dvh`/
  `svh`/`lvh` exist precisely for this; `100vh` is the single most common
  mobile layout bug.
- A 44px visual button with a 44px tap area is fine; a 44px icon with
  only the 16px glyph tappable is a miss-fest. Size the hit area, not
  just the picture.
- Inputs with font-size below 16px trigger auto-zoom on iOS, jarring the
  whole layout on focus. 16px is a functional floor, not a style choice.
- Hover-only menus and tooltips are invisible on touch — there is no
  hover event. Every hover affordance needs a tap path, or it doesn't
  exist for half your users.
- Breakpoints named after last year's flagship phone are obsolete on
  arrival and miss foldables, tablets, and split-screen. Break where the
  content breaks.
- The on-screen keyboard covers the bottom ~40% of the screen; a focused
  input or a fixed "Save" bar down there disappears behind it unless you
  scroll it into view or adjust for the keyboard.
- Hiding "secondary" content to fit mobile often hides the thing the user
  came for. Progressive disclosure is fine; hiding the primary action to
  win space is not.
- Custom left-swipe gestures fight the browser's back-swipe and pull-to-
  refresh; design gestures that coexist with the platform, not against it.

## Stop Conditions

- The request is about mobile PERFORMANCE — bundle size, image weight, JS
  cost on low-end devices, metric budgets → route to
  `frontend-perf-engineer`; this skill owns layout/touch/viewport, not
  payload.
- The request is the view's empty/loading/error STATE design → route to
  `edge-state-ux-designer` (those states still need mobile craft, but the
  state model is separate).
- The request is to VERIFY accessibility (screen-reader announcements,
  contrast ratios, keyboard traversal) as a test pass → route to
  `accessibility-test-harness`; this skill records a11y intent, it does
  not run the checks.
- Meeting a touch-target or zoom-safety minimum would require dropping a
  feature or an a11y obligation the product must keep → surface the
  tradeoff to a human rather than silently shrinking targets below the
  usable/accessible floor.

## Supporting Files

- [references/mobile-viewport-sheet.md](references/mobile-viewport-sheet.md)
  — content-driven breakpoint patterns, the touch-target and safe-area
  reference, the viewport-unit cheat sheet, input-type/keyboard table, and
  wide-table reflow options.
- `evals/evals.json` — behavior cases including the `100vh` trap fix, the
  hover-only-to-touch conversion, and the wide-table reflow.
- `evals/trigger-evals.json` — discrimination against `frontend-perf-engineer`
  (weight vs craft), `edge-state-ux-designer`, and `accessibility-test-harness`.
