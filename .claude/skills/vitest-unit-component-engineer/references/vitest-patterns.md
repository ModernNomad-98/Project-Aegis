# Vitest Patterns

Detail file for [vitest-unit-component-engineer](../SKILL.md). Loaded on demand.

## Environment selection table

| Subject | Environment | Why |
| --- | --- | --- |
| pure functions, validators, mappers, reducers | `node` | fastest; catches accidental DOM/window reliance |
| framework-free DOM utilities | `jsdom` or `happy-dom` | DOM APIs needed, no browser fidelity required |
| components (render + interact) | `jsdom` (default) / `happy-dom` (speed, check API gaps) | Testing Library needs a DOM |
| anything needing layout, real navigation, downloads | none — wrong layer | Playwright territory |

Declare per file with `// @vitest-environment jsdom` or per glob with
`environmentMatchGlobs` — visible intent either way.

A small pure-function test stays in `node` and checks behavior, not just
construction:

```ts
import { expect, test } from 'vitest';
import { clamp } from '../src/clamp'; // replace with the real module path
test('clamps above the allowed range', () => expect(clamp(12)).toBe(10));
```

## Mock-seam patterns

- **Clock:** `vi.useFakeTimers()` + `vi.setSystemTime()`; restore in
  `afterEach(() => vi.useRealTimers())`.
- **Network:** mock the repo's OWN api-client module, or use an interceptor
  (e.g., MSW) at the fetch boundary; add a setup guard that fails on
  unexpected real fetch.
- **Randomness/ids:** inject or seed; asserting on random output is flake
  authorship (`flaky-test-detective` will be back for you).
- **Never:** mocking the module under test, partial-mocking its private
  functions, or deep-mocking third-party internals (wrap the library in an
  owned adapter and mock the adapter).

## Testing Library query priority

`getByRole` (with accessible name) → `getByLabelText` → `getByPlaceholderText`
→ `getByText` → `getByTestId` (last resort, and a hint to improve the
component's semantics — which also feeds `accessibility-test-harness`).

Interactions: `userEvent` over `fireEvent` (real event sequences).
Async: `findBy*` / `waitFor` with a specific assertion — never sleep.
For a component test, declare `// @vitest-environment jsdom`, render the
component, find the button with `getByRole('button', { name: 'Save' })`, click
with `userEvent`, and assert the visible saved state. An owned API-adapter
call can be a secondary assertion, but cannot replace the rendered outcome.
Restore owned-boundary mocks and real timers in `afterEach`; when fake timers
are needed with `userEvent`, configure its timer-advance hook explicitly.

## Determinism recipes

- Freeze time zone in the test runner's cross-platform environment setup (for
  example, set `process.env.TZ = 'UTC'` before date-sensitive modules load) or
  make code time-zone explicit; POSIX `TZ=UTC command` syntax is not portable
  to every Windows shell.
- One assertion of truth per behavior; table-drive boundaries with
  `test.each`.
- Isolation check: run with `--sequence.shuffle` locally when touching suite
  structure — order dependence is a bug now, not later.

## Coverage stance

Thresholds come from the automation blueprint. Locally meaningful signal:
uncovered branches in the file you just tested. Repo-wide percentages belong
to `test-coverage-mapper`'s analysis, not to this skill's exit criteria.
