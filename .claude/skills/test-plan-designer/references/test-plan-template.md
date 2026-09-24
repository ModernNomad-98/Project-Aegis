# Test Plan Template & Behavior Catalog

Detail file for `test-plan-designer`. Loaded on demand.

## Behavior catalog — prompts per risk

For each risk, walk this list and keep what applies:

- **Happy path:** the documented success behavior, once, at the cheapest layer.
- **Negative paths:** unauthorized, invalid input, expired, missing, duplicate,
  conflicting, out-of-order.
- **Boundaries:** empty, one, many, max size, date/timezone edges, precision.
- **State transitions:** create→edit→delete cycles, idempotent retries,
  concurrent modification where plausible.
- **Failure handling:** dependency down/slow/erroring — what the user sees.
- **Data visibility:** who can see the result; cross-tenant/roles → delegate
  to `multi-tenant-security-tester` line items.

## Plan item quality bar

A plan item is executable when a stranger can answer: what do I set up, what
do I do, what exactly should happen, and where do I record the result. Items
failing that bar get fixed at planning time.

## Plan template

Record the scope, excluded behaviors, environment and data prerequisites,
entry criteria, and exit criteria before the item table. Give each requirement
or risk and each test a stable ID. Replace the example row with executable
steps and an observed evidence location; do not count a planned item as passed.

| Requirement or risk ID | Test ID | Behavior | Setup and data | Action | Expected result | Layer | Environment | Evidence location | CI tier | Owner |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `R-tenant-01` | `T-tenant-01` | A member cannot read another tenant's invoice | Two synthetic tenants, member of only tenant A, invoice owned by B | Request B's invoice by ID as A's member | Denied with no B data returned or leaked in logs | integration | isolated test database | `reports/tenant-01.json` after execution | change gate | security-test owner |

`CI` means continuous integration. Choose a layer from unit, integration,
contract, end-to-end (E2E), or manual. Accessibility checks run within one
of those layers, with `accessibility-test-harness` owning their criteria.

## Exit-criteria patterns (objective)

- "All P0/P1 plan items pass; P2 failures triaged with owner + ticket."
- "Zero open sev-1/sev-2 defects in the changed area."
- "Contract suite green against provider version X."
- "Screenshots captured for checkpoints C1–C4 per evidence rules."
- Anti-pattern: "testing complete", "QA approves", "looks good".

## Layer assignment quick table

| Behavior | Layer | Implementer skill |
| --- | --- | --- |
| pure logic/validation | unit | `vitest-unit-component-engineer` |
| service/command through DB + auth | integration | `integration-test-designer` |
| API/webhook shape & compat | contract | `api-contract-test-designer` |
| critical journey in real UI | E2E | `playwright-e2e-engineer` |
| visual/UX judgment | manual | `manual-test-case-creator` + evidence plan |
| keyboard/focus/contrast/screen reader | integration, E2E, or manual | `accessibility-test-harness` |

## Release-plan extras

For release-scope plans add: regression tier selection
(`regression-suite-curator`), build QA (`vite-build-qa-engineer` for Vite
apps), clickthrough pass on changed routes (`clickthrough-test-engineer`),
and closeout via `ai-closeout-reporter` with the evidence bundle.
