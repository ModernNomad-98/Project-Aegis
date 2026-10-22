# State Table Template - state/event/guard table plus transition matrix

Concrete artifact guide for the `state-machine-modeler` skill. Method and record guidance only: it never directs the skill to edit code, run commands, use the network or claim production authority.

## 1. Artifact fields

- **Every state named, with owner and meaning**
- **Events/commands that trigger transitions**
- **Guards as explicit predicates**
- **Side effects per transition**
- **Terminal states and re-open rules**
- **Retry/compensation edges and their bounds**
- **Invalid transitions and the refusal behaviour**

## 2. Worked table (state/event/guard table plus transition matrix)

| From | Event | Guard | To | Side effect |
| --- | --- | --- | --- | --- |
| draft | submit | all required fields present | submitted | emit OrderSubmitted |
| submitted | cancel | not yet shipped | cancelled | release reservation |

## 3. Construction steps

1. Inventory states from code, schema and incidents; mark inferred ones.
2. List events/commands and who may emit them.
3. Write guards as predicates over named evidence.
4. Attach side effects and failure handling per transition.
5. Mark terminal states and any re-open path.
6. Enumerate illegal moves and the expected refusal.
7. Review the matrix with the domain owner.

## 4. Quality checks before returning

- Every state reachable and every state has an exit or is terminal
- Every transition has trigger, guard and effect
- Retries bounded with a failure terminal
- Illegal transitions are refused not silently ignored
- Matrix covers the incidents/open questions that motivated it

## 5. Failure/gotcha handling

- A status column is not a state machine until guards and illegal moves are explicit
- Retries without a terminal failure can loop forever
- Terminal states that can silently re-open corrupt consumer assumptions

## 6. Boundaries

- tenant modeler requests route to `tenant-modeler`; this skill does not perform that owner work.
- subscription lifecycle designer requests route to `subscription-lifecycle-designer`; this skill does not perform that owner work.
- domain modeler requests route to `domain-modeler`; this skill does not perform that owner work.
- property based test designer requests route to `property-based-test-designer`; this skill does not perform that owner work.
- product spec writer requests route to `product-spec-writer`; this skill does not perform that owner work.
- architecture designer requests route to `architecture-designer`; this skill does not perform that owner work.
- Broader eval-only discrimination set from evals/trigger-evals.json: `adr-writer`, `architecture-designer`, `change-classification-gate`, `code-reviewer`, `design-review-facilitator`, `domain-modeler`, `human-approval-boundary`, `product-spec-writer`, `property-based-test-designer`, `release-readiness-reviewer`, `rollback-runbook-author`, `subscription-lifecycle-designer`, `tech-spec-writer`, `tenant-modeler` (neighbours for discrimination, not in-scope work).
- No production, deployment, spending or approval authority is granted by this reference.
