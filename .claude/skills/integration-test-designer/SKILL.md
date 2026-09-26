---
name: integration-test-designer
description: Design integration tests — the layer BETWEEN unit and E2E — that exercise modules through REAL service, command, database, auth, and permission boundaries with no browser. Every suite names exactly which boundaries are real and which seams stay faked (third-party APIs, clocks, email), with rationale per seam; defines the seeded-data and transaction/cleanup strategy, auth-context minting through real code paths, and per-boundary negative cases. Produces implementable specs and hands implementation off. Use when asked to design integration tests, test a command/service through the real database and permission checks, verify module wiring beyond mocked units, or when mocked-everything tests keep passing while real wiring breaks. Do NOT use for isolated unit/component tests (vitest-unit-component-engineer), browser journeys (playwright-e2e-engineer), API schema/compatibility verification (api-contract-test-designer), or cross-tenant/authz negative suites (multi-tenant-security-tester).
---

# Integration Test Designer

Terms: **E2E** means end to end; **CI** means continuous integration;
**API** means application programming interface; **DB** means database;
**UI** means user interface; **IDOR** means insecure direct object reference;
**HTTP** means Hypertext Transfer Protocol; **SMS** means Short Message
Service; **PR** means pull request; **SDK** means software development kit.

## Purpose

Design the test layer that proves modules work through their REAL boundaries
— service to command to database, with real auth context and real permission
checks — while explicitly naming the seams that stay faked. This is the layer
between unit (everything isolated) and E2E (browser journey): no browser, no
mocked database, no pretending. The deliverable is an implementable suite
design: boundary map, fixture/transaction strategy, per-behavior specs with
negative cases, and CI placement.

## Use When

- Use when: asked to design integration tests for commands, services, API
  handlers, repositories, or background jobs through real infrastructure.
- Use when: units are green but wiring keeps breaking — mocks drifted from
  real service/DB behavior.
- Use when: a test plan hands over items marked "integration layer".
- Use when: a module's auth/permission enforcement must be tested through the
  real middleware/guard path (functional correctness of the check).
- Do NOT use when: the subject is pure logic or an isolated component —
  `vitest-unit-component-engineer`.
- Do NOT use when: the ask is a user journey through the real UI —
  `playwright-e2e-engineer`.
- Do NOT use when: the ask is schema/shape/version compatibility of an API or
  webhook — `api-contract-test-designer` (contract ≠ flow).
- Do NOT use when: the ask is PROVING tenant isolation or authorization as a
  security property (cross-tenant matrices, IDOR enumeration, escalation) —
  the shipped `multi-tenant-security-tester` owns that negative suite; this
  skill covers functional boundary behavior and defers security matrices to it.

## Inputs to Inspect

1. The module and its real dependencies: which services, DB tables,
   auth/permission middleware, queues it actually touches (read the code, not
   the diagram).
2. Infrastructure availability: can tests get a real database (local
   container, CI service)? Existing integration setup/config if any.
3. How auth context is established in production code (session, token,
   middleware) — tests must mint context through that path, not by faking
   internals.
4. Existing fixtures/factories (`test-data-architect` output) and migration
   state — what schema the suite runs against.
5. The plan items or bug history this suite must verify (risk-traced).

## Workflow

When a human must choose a real-dependency environment for a local or CI
integration suite, define unfamiliar terms and each viable option and why it
fits. Compare case-specific fidelity, isolation, CI runtime, money, setup
time, and ongoing upkeep; state unknown costs instead of guessing. Recommend
one from the affected environment's constraints and explain why it fits the
user's goals and what fact would change the recommendation before one atomic
decision question. Ask for a missing deciding fact first when needed. Keep
routine design choices within this skill; a preference does not authorize
provisioning or test execution.

1. **Draw the boundary map first.** For the module under test, list every
   boundary and classify: REAL in this suite (service calls, DB reads/writes,
   auth middleware, permission checks) or FAKED seam (third-party HTTP, email/
   SMS, payment provider, clock, randomness). Every fake gets a one-line
   rationale (non-deterministic, costs money, external ownership). The
   classification table template is in
   [references/boundary-catalog.md](references/boundary-catalog.md).
2. **Define the data strategy:** seeded baseline via real
   migrations + factories; per-test isolation via transaction-rollback or
   per-worker schema (pick per the automation blueprint; compose
   `test-data-architect` for fixture design). Cleanup is structural, not
   manual DELETE lists.
3. **Define auth-context minting:** create users/roles through real code
   paths (signup service, membership creation) or documented test bootstrap
   endpoints — never by injecting a fabricated session object the middleware
   would have rejected.
4. **Specify behaviors per boundary:** for each command/service under test —
   happy path through the full real stack (assert the DB state AND the
   response), negative paths (invalid input rejected at the boundary,
   permission denied for wrong role — functional check), and failure modes of
   faked seams (provider timeout/error surfaced correctly).
5. **Keep the layer honest:** if a spec needs a browser, it moved to E2E; if
   it mocks the DB, it moved to unit; if it enumerates cross-tenant access,
   it belongs to `multi-tenant-security-tester` — record these reroutes.
6. **Define execution & CI placement:** runtime budget, parallelization
   constraints (per-worker DB), which tier runs the suite (usually PR,
   blocking). If the owner must choose the real test database environment,
   define an ephemeral local/CI database (created for a run and discarded)
   and a shared CI/staging database (reused across runs). Explain why each
   is viable, its production-fidelity and data-isolation benefits and
   drawbacks, setup/run/upkeep effort, and money cost or unknowns.
   Recommend the path fitting the boundary and parallel-run evidence,
   explain why and what constraint could change it, then ask one decision
   question. Keep third-party seams faked and design only; this skill does
   not provision either environment.
7. **Hand off implementation** with the spec quality bar: each spec names
   setup, action, and observable assertions: response plus relevant persisted
   state for writes, unchanged state for rejected writes, and response plus
   relevant baseline for reads.

## Output Format

When asking for this build choice, show each option's meaning, reason,
case-specific benefits and limits, money/setup/upkeep or unknowns, and
a justified recommendation before the one decision question.

```
INTEGRATION TEST DESIGN — <module/scope>
Boundary map: <boundary → REAL | FAKED (rationale)>
Data strategy: <seed/factory source, isolation mechanism, cleanup>
Auth-context minting: <how personas/roles are created via real paths>
Specs:
  <id> — <behavior> — setup <fixtures/persona> — action <real call path>
       — assert <response + write state | rejected-write unchanged state |
         read response + relevant baseline> — negatives <invalid/denied/failure>
Rerouted items: <specs that belong to unit/E2E/security layers + where sent>
Environment assumptions: <DB/container/CI services required>
Owner environment choice (only if needed): <plain terms; ephemeral/local vs
  shared CI/staging; reasons, fidelity/isolation pros/cons, setup/run/upkeep
  and money costs or unknowns; recommendation and why; one question>
CI placement: <tier, runtime budget, parallelization constraints>
Handoffs: <implementation → engineer executing the suite;
          security matrices → multi-tenant-security-tester>
Exit criteria: <what "this layer is covered" means for the module>
```

## Validation Checklist

- [ ] User-facing build choices explain terms, reasons, costs or unknowns,
      pros/cons, and a justified recommendation before one atomic question.
- [ ] Boundary map classifies EVERY dependency as real or faked, each fake
      with rationale — no ambient unlisted mocks.
- [ ] Database, auth, and permission paths under test are REAL; any mock of
      them reroutes the spec to unit.
- [ ] Auth context minted through real code paths, not fabricated internals.
- [ ] Write specs assert relevant persisted state; rejected writes assert
      unchanged state; read-only specs assert response and relevant baseline.
- [ ] Negative cases present per boundary (invalid, denied, seam failure).
- [ ] Data isolation strategy supports parallel runs.
- [ ] No browser anywhere in the design; no cross-tenant security matrices
      re-owned from `multi-tenant-security-tester`.
- [ ] CI placement and runtime budget stated.
- [ ] Any owner-facing database-environment choice explains terms, viable
      paths, fidelity/isolation tradeoffs, costs or unknowns, and a
      reasoned recommendation before one question; nothing is provisioned.

## Gotchas

- "Integration" suites where the DB is mocked test serialization, not
  integration — the most common false-confidence pattern; reroute honestly.
- Asserting only the HTTP response misses write bugs — a 200 with the wrong
  row persisted passes such tests; always assert stored state.
- Fabricated auth contexts (injecting a session object directly) skip the
  middleware being tested and rot silently when auth changes.
- Faked seams drift: a payment-provider fake that never returns the real
  error shape hides handling bugs — pin fakes to recorded/documented shapes
  and note drift risk (contract verification of the real provider belongs to
  `api-contract-test-designer`).
- Shared seed data across parallel workers causes intermittent failures that
  get misfiled as flakes — isolation is a design property, not a retrofit.

## Stop Conditions

- A real database/service is unavailable for local test runs, CI runs, or
  both → identify the affected environment. Compare viable ways to provision
  a real dependency there; a local container and a CI service may both be
  needed. Explain each option under the build-choice rule and ask only one
  environment's decision per turn. Never silently degrade to mocked
  "integration".
- The module has no seam between it and a third-party dependency (direct SDK
  calls everywhere) → designing the test requires a product refactor;
  surface it as a separate classified change.
- Tenant semantics/authorization matrix undefined while permission behavior
  is in scope → functional checks proceed, but security-matrix design halts
  and routes to `multi-tenant-security-tester` / `tenant-modeler`.
- Asked to also implement and run the suite → implementation is a separate
  side-effecting step; hand off with the specs.

## Supporting Files

- [references/boundary-catalog.md](references/boundary-catalog.md) —
  boundary classification table, transaction/cleanup patterns compared,
  auth-minting recipes, and seam-failure case catalog.
- `evals/evals.json` — trigger + behavior cases.
- `evals/trigger-evals.json` — discrimination within the test-level cluster
  and against the shipped `multi-tenant-security-tester`.
