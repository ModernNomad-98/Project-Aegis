---
name: edge-state-ux-designer
description: Design the non-happy-path UI states for a view or flow — the distinct empty states (first-run vs filtered-to-nothing vs error-emptied, each with its own copy and next action), loading states (skeleton vs spinner vs inline, a delay threshold to avoid flash, optimistic updates with rollback), error states (inline vs toast vs full-page, retry affordance, partial failure, stale-on-error), and the permutations teams forget (offline, refetching/stale, slow, partial data, permission-denied, too-much-data). Produces a per-view state matrix so every state is deliberate, never a blank screen or an eternal spinner. Renders the codes/messages from error-taxonomy-designer; owns presentation, not the error model. Use when designing empty/loading/error states, first-run experiences, or when a screen shows nothing on the unhappy path. Do NOT use to design error codes/taxonomy (error-taxonomy-designer), mobile viewport/touch craft (mobile-viewport-craft), or to verify state accessibility (accessibility-test-harness).
---

# Edge State UX Designer

## Purpose

Product design covers the happy path and forgets the other twelve
states. The result ships to production: a list that shows a blank white
rectangle when it's empty (is it loading? broken? actually empty?), a
spinner that never resolves when the network drops, a search that
returns "No results" with the same dead-end copy whether you have no
data yet or just filtered too hard. This skill produces the design for
every non-happy-path state of a view — the three different empties,
loading that doesn't flash or lie, errors placed and retried
appropriately, and the permutations everyone forgets (offline, stale,
partial, forbidden) — as a per-view state matrix where each state has a
deliberate trigger, visual, copy, and next action. It RENDERS the error
model that `error-taxonomy-designer` defines; it does not design the
codes.

## Use When

- Use when: designing the empty, loading, and error states for a view,
  list, form, or flow — or auditing a screen that only handles success.
- Use when: a screen shows a blank area, a raw error, or an eternal
  spinner on the unhappy path, and users can't tell which state they're
  in.
- Use when: designing a first-run / zero-data experience, or the
  difference between "you have nothing yet" and "your filter matched
  nothing".
- Use when: adding optimistic updates and you need the rollback/failure
  presentation, or designing partial-failure UX (some widgets load, some
  fail).
- Do NOT use when: the task is the error MODEL — categories, machine
  codes, retryable flags, the envelope — that is `error-taxonomy-designer`;
  this skill renders what that produces.
- Do NOT use when: the task is mobile viewport / touch / responsive
  layout craft (breakpoints, touch targets, safe areas) — that is
  `mobile-viewport-craft`.
- Do NOT use when: the task is VERIFYING accessibility of these states
  (keyboard, screen-reader announcements, contrast) as a test pass —
  that is `accessibility-test-harness`; this skill designs the states and
  notes their a11y intent, which that harness then checks.

## Inputs to Inspect

1. The view's data lifecycle: where the data comes from, whether it can
   be empty legitimately, how long it typically takes to load, and
   whether it refetches/polls (each is a state).
2. The error surface for this view: which taxonomy codes it can receive
   (from `error-taxonomy-designer` output), which are retryable, and
   which are per-field vs whole-view.
3. First-run reality: what a brand-new user/tenant sees before any data
   exists, and what the desired first action is (create, import, invite).
4. Existing state handling in the codebase: shared empty/loading/error
   components if any, and screens that currently mishandle these states
   (blank renders, infinite spinners) as the concrete gap.
5. Product tone/content conventions and any design-system components for
   skeletons, toasts, banners, and empty states already available to
   reuse.

## Workflow

1. **Enumerate the view's states.** Beyond "loaded": uninitialized,
   loading-first-time, loaded-empty, loaded-partial, loaded-full,
   refetching/stale, error (whole-view), error (partial), offline, and
   permission-denied. Not every view has all — but each is decided IN or
   OUT deliberately, not by omission.
2. **Split the empties — they are not one state.** First-run / never-had-
   data (onboarding copy + a create/import CTA), filtered-or-searched-to-
   nothing (a "clear filters" affordance, and DON'T imply the user has no
   data), and error-emptied (this is an error, show retry — not a
   cheerful empty). Each gets distinct copy and a distinct next action.
3. **Design loading honestly.** Choose skeleton (layout known, content
   coming — reserves space, no layout shift) vs spinner (short/unknown
   shape) vs inline indicator (background refresh). Apply a small delay
   threshold before showing a loader so fast responses don't flash one.
   For optimistic updates, design the rollback: what the UI shows if the
   write fails, and how the user learns it reverted.
4. **Place errors by blast radius.** Field/section error → inline near
   the cause; transient action failure → toast (with retry if
   retryable); whole-view failure → full-view error with a retry and a
   correlation id to quote. Design partial failure: the working parts
   render, the failed widget shows its own error, and the page is not
   held hostage by one failed call.
5. **Design stale/offline/refetch.** On refetch, keep the last-good data
   visible with a subtle refreshing indicator rather than flashing to a
   skeleton. On error-during-refetch, keep last-good + a banner ("couldn't
   update"). Offline: distinguish it from a server error and say what's
   safe to do.
6. **Cover the forgotten permutations.** Permission-denied is not empty
   (403 → "you don't have access", not "no items"). Too-much-data →
   pagination/virtualization handoff (`pagination-cursor-designer`).
   Zero-after-filter vs zero-ever. Slow-but-working (progress, not just a
   spinner).
7. **Note accessibility intent per state.** Loading announced to screen
   readers (aria-live/busy), focus moved to the error on failure, empty-
   state not a silent visual — record the intent; VERIFICATION is
   `accessibility-test-harness`.
8. **Design for reuse.** Factor shared empty/loading/error components and
   copy patterns so states are consistent across views, not reinvented
   per screen. Keep the error copy keyed to taxonomy codes.
9. **Deliver** the per-view state matrix in the Output Format.

The full state checklist, the three-empties comparison, loading-pattern
selection, and copy patterns:
[references/edge-state-sheet.md](references/edge-state-sheet.md).

## Output Format

```
EDGE-STATE MATRIX — <view/flow>
Per state row:
  <state> | trigger=<what puts the view here> | visual=<skeleton|spinner|inline|
           banner|toast|full-view|empty-illustration> | copy="<actionable>" |
           action=<primary CTA / retry / clear-filter / none> | a11y=<announce/focus intent>
States covered: uninitialized, loading-first, empty(first-run), empty(filtered),
  empty(error), loaded-partial, refetching/stale, error(view), error(partial),
  offline, forbidden   — each IN or OUT with reason
Optimistic writes: <rollback presentation + how user learns of revert> | n/a
Reuse: <shared components/copy patterns factored>
Handoffs: error codes/messages ← error-taxonomy-designer; a11y verification →
  accessibility-test-harness; huge lists → pagination-cursor-designer
```

## Validation Checklist

- [ ] Every plausible state for this view is listed and marked IN or OUT
      with a reason — no state left to accidental blank render.
- [ ] The three empties are distinct: first-run, filtered-to-nothing, and
      error-emptied each have their own copy and next action.
- [ ] Loading uses skeleton vs spinner vs inline deliberately, with a
      delay threshold so fast responses don't flash a loader.
- [ ] Errors are placed by blast radius (inline / toast / full-view) and
      retryable errors offer retry; whole-view errors surface a
      correlation id.
- [ ] Partial failure is designed — one failed call does not blank the
      whole page.
- [ ] Refetch keeps last-good data visible rather than flashing to a
      skeleton; offline is distinguished from a server error.
- [ ] Permission-denied is rendered as forbidden, not as empty.
- [ ] Error copy is keyed to `error-taxonomy-designer` codes, and a11y
      verification is handed to `accessibility-test-harness`.

## Gotchas

- A blank rectangle is three bugs wearing a trench coat: the user can't
  tell empty from loading from broken. Every "nothing here" must say
  WHICH nothing it is.
- "No results" after a filter that reads like "you have no data" makes
  users think their data is gone. Filtered-empty must point at the
  filter, not the void.
- Showing a spinner with zero delay makes every fast page flicker; never
  showing one makes a slow page look frozen. A short delay threshold
  (then a skeleton) is the honest middle.
- Optimistic UI without a rollback design is a data-integrity illusion:
  the user sees success, the write failed, and nobody told them. Design
  the revert and its notification, or don't go optimistic.
- One failed side-panel call should not blank the entire dashboard.
  Partial failure is a first-class state, not an afterthought — isolate
  the failed region.
- Flashing loaded data back to a skeleton on every background refetch is
  visual noise that reads as breakage. Keep last-good visible; indicate
  refreshing subtly.
- 403 is not 404 is not empty. "You don't have access" and "this doesn't
  exist" and "there's nothing here yet" are three different messages;
  collapsing them confuses and can leak existence.
- Designing these states as one-off markup per screen guarantees drift.
  Factor shared components so the empty state on view A matches view B.

## Stop Conditions

- The request is to design the error MODEL — codes, retryable semantics,
  the envelope, disclosure rules → route to `error-taxonomy-designer`;
  this skill renders that model, it does not define it.
- The request is mobile viewport / responsive / touch craft (breakpoints,
  touch-target sizing, safe areas) → route to `mobile-viewport-craft`.
- The request is to VERIFY accessibility of the states as a test pass
  (keyboard traversal, screen-reader announcement checks, contrast in CI)
  → route to `accessibility-test-harness`; this skill records a11y intent
  but does not run the verification.
- A "permission-denied" state's copy would reveal whether a resource
  exists to someone not allowed to see it → flag the existence-disclosure
  risk and coordinate the wording with the authorization owner rather
  than guessing.

## Supporting Files

- [references/edge-state-sheet.md](references/edge-state-sheet.md) — the
  full state checklist, the three-empties comparison, loading-pattern
  selection table, and reusable copy patterns per state.
- `evals/evals.json` — behavior cases including the three-empties split,
  the optimistic-rollback design, and the partial-failure state.
- `evals/trigger-evals.json` — discrimination against `error-taxonomy-designer`
  (the model), `mobile-viewport-craft`, and `accessibility-test-harness`.
