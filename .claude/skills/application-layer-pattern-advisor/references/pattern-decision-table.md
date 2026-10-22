# Pattern Decision Table - pattern decision table with placement and side-effect visibility

Concrete artifact guide for the `application-layer-pattern-advisor` skill. Method and record guidance only: it never directs the skill to edit code, run commands, use the network or claim production authority.

## 1. Artifact fields

- **Patterns considered: adapter, facade, repository, service object, use-case layer**
- **Cost and benefit per pattern**
- **Placement and allowed dependencies**
- **Side-effect visibility and transaction boundary**
- **Introduction/removal/refactor path**
- **Over-abstraction stop rules**
- **Where external integration adapters yield to outbound-integration-adapter-designer**

## 2. Worked table (pattern decision table with placement and side-effect visibility)

| Pattern | Cost | Benefit | Placement | Stop rule |
| --- | --- | --- | --- | --- |
| repository | mapping + indirection | isolate persistence | adapter layer | stop if it only forwards calls |
| use-case layer | orchestration code | explicit side effects | application boundary | stop if it duplicates controllers |

## 3. Construction steps

1. State the actual change pressure and coupling evidence.
2. List candidate patterns with cost/benefit.
3. Decide placement per layer and dependency direction.
4. Make side effects and transaction boundaries visible.
5. Define introduction or removal steps.
6. Set the stop rules for over-abstraction.
7. Yield external-provider adapter contracts to outbound-integration-adapter-designer.

## 4. Quality checks before returning

- Each pattern has a concrete cost and benefit
- Placement respects dependency direction
- Side effects are visible at the application boundary
- Removal/introduction path is incremental
- External provider adapter details are not stolen from the sibling owner

## 5. Failure/gotcha handling

- An abstraction that only forwards calls is cost without benefit
- Hiding side effects behind a facade makes retries unsafe
- Pattern advice and external adapter design are different decisions

## 6. Boundaries

- layered architecture enforcer requests route to `layered-architecture-enforcer`; this skill does not perform that owner work.
- interface first designer requests route to `interface-first-designer`; this skill does not perform that owner work.
- code simplifier requests route to `code-simplifier`; this skill does not perform that owner work.
- command gateway architect requests route to `command-gateway-architect`; this skill does not perform that owner work.
- domain modeler requests route to `domain-modeler`; this skill does not perform that owner work.
- architecture designer requests route to `architecture-designer`; this skill does not perform that owner work.
- Broader eval-only discrimination set from evals/trigger-evals.json: `adr-writer`, `architecture-designer`, `change-classification-gate`, `code-reviewer`, `code-simplifier`, `command-gateway-architect`, `dependency-direction-guard`, `design-review-facilitator`, `domain-modeler`, `human-approval-boundary`, `interface-first-designer`, `layered-architecture-enforcer`, `release-readiness-reviewer`, `tech-spec-writer` (neighbours for discrimination, not in-scope work).
- No production, deployment, spending or approval authority is granted by this reference.
