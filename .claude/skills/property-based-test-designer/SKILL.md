---
name: property-based-test-designer
description: 'Designs property-based test coverage for a given unit — parsers, validators, math, state machines, transformations: the properties and invariants that must hold, generator domains with shrinking, and the counterexample-triage and runner handoff. Produces the design only — writes and runs no tests. Use when asked to design property-based coverage, choose properties or invariants for a function or module, or plan generator domains and shrinking. Do NOT use for per-change test plans (test-plan-designer), test-data catalog design (test-data-architect), writing or running the actual test files (vitest-unit-component-engineer), or flake root-causing (flaky-test-detective).'
---

# Property Based Test Designer

**Reading key:** A property-based test states an invariant that must hold for
ALL inputs from a domain, then checks it against many generated examples. A
generator produces those examples; shrinking reduces a failing example toward
a minimal counterexample. Example-based tests check one hand-picked input
each; property tests check a whole domain at once.

## Purpose

Produce the property-based test coverage design for a given unit — parsers,
validators, math, state machines, transformations: which properties and
invariants must hold, the generator domains and shrinking, and the
counterexample-triage rules plus the runner handoff. It is on-demand,
specialized coverage: it names where property testing earns its cost and
where example tests suffice. It designs; it writes and runs no tests.

## Use When

- Use when: asked to design property-based coverage for a function or module.
- Use when: asked to choose properties or invariants for a unit.
- Use when: asked to plan generator domains and shrinking for a property suite.
- Use when: asked to hand a designed property suite to an implementer.
- Do NOT use when: the ask is a per-change test plan across layers — that is `test-plan-designer`.
- Do NOT use when: the ask is the test-data catalog design (personas, datasets, fixtures) — that is `test-data-architect`.
- Do NOT use when: the ask is writing or running the actual test files — that is `vitest-unit-component-engineer` *(manual-only)*.
- Do NOT use when: the ask is flake root-causing or stability repair — that is `flaky-test-detective` *(manual-only)*.

## Inputs to Inspect

1. The target functions and types: parsers, validators, math, state machines, transformations — with their signatures and semantics.
2. Existing unit tests, so the design names what property coverage adds instead of duplicating.
3. The domain rules and edge-case notes the properties must express.
4. The runner and generator library in use, to hand off implementable specs.

## Workflow

1. **Identify the targets.** List the units whose domain-wide invariants are worth the cost: parsing, validation, math, state transitions, serialization round-trips. State why property coverage earns its cost here.
2. **State properties and invariants per target.** For each target, the invariant in one sentence (for example: parse-then-print round-trips; a validator rejects exactly the invalid inputs; a state machine's transitions never reach a forbidden state). A property that restates the implementation is rejected.
3. **Specify generator domains and shrinking.** For each property: the input domain, its bounds, and the shrink direction that yields a minimal counterexample.
4. **Define counterexample triage.** What a failing example is reported as (a bug in the target, a bug in the property, or an invalid assumption) and where each routes.
5. **Hand off the runner.** Name the implementer (`vitest-unit-component-engineer` *(manual-only)* or the repository's property runner) — a handoff, never an execution here.
6. **Emit the design** in the Output Format, stating what was chosen, why, and the main rejected alternative.

## Output Format

Emit the design in the conversation (nothing is written to the repo):

```
PROPERTY-BASED TEST DESIGN — <module / unit>
Targets: <each target and why property coverage earns its cost here>
Properties per target:
  <target> — property <one-sentence invariant> — domain <bounds> — shrink <direction>
Counterexample triage: <target bug | property bug | invalid assumption → where each routes>
Runner handoff: <implementer named (vitest-unit-component-engineer, manual-only) — not executed here>
Out of scope:
  per-change plan → test-plan-designer
  test-data catalog → test-data-architect
  writing/running tests → vitest-unit-component-engineer
  flake repair → flaky-test-detective
Chosen / why / rejected: <the key choices, the reason for each, and the main
  rejected alternative>
```

## Validation Checklist

- [ ] Every target has at least one property; each property states its domain and shrink direction.
- [ ] No property restates the implementation (a property that only passes when the code is copied into the test is not a property).
- [ ] Generator domains are bounded; unbounded generation is named and justified.
- [ ] Counterexample triage routes each failure class to an owner.
- [ ] The runner handoff names the implementer; the design claims to write or run no tests.

## Gotchas

- A property that restates the implementation (parse exactly what print emits, with the same code path) proves nothing; the invariant must come from the domain, not the code.
- Unbounded generators produce slow runs and unreadable failures; bound the domain and name the shrink direction.
- Flaky randomness: a property suite that fails intermittently is a property or generator bug, not a product race to paper over; root-causing stays with `flaky-test-detective`.
- Property tests replace neither example tests nor a per-change plan; they are on-demand, specialized coverage for domain-wide invariants.
- Writing or running the files is `vitest-unit-component-engineer`'s (manual-only); this skill designs the suite and hands it off.

## Stop Conditions

- No target unit is supplied or findable → stop and ask for it; a design cannot start from "add property tests".
- The request becomes writing or running test files → hand off to `vitest-unit-component-engineer` *(manual-only)*.
- The request becomes a per-change test plan → hand off to `test-plan-designer`.
- The request becomes flake root-causing → hand off to `flaky-test-detective` *(manual-only)*.
- The request involves destructive or live-state action → stop and refuse.

## Supporting Files

- `evals/evals.json` — trigger + behavior cases.
- `evals/trigger-evals.json` — discrimination against `test-plan-designer`, `test-data-architect`, `vitest-unit-component-engineer`, and `flaky-test-detective`.
- `references/` — None: the design is self-contained.
