# Component boundary rules: layers, contracts and dependencies

Reference for the component-boundary-designer skill. It is method and record guidance only: it never directs the skill to edit code, run commands, use the network or claim production authority.

## 1. Core model

- Layer taxonomy and ownership are explicit and non-overlapping.
- Contracts name what each boundary accepts and forbids.
- Dependency direction is stated and shared components are constrained.
- Violations have locations and evidence, not adjectives.
- Abstraction-vs-duplication rule is stated; migration is ordered.
- Every claim is backed by inspected evidence or labeled **assumption**, **UNKNOWN** or **UNRUN**; an empty check is never a PASS.

## 2. When this applies

- Component ownership is unclear or duplicated across features.
- A component tree mixes page, container, feature and primitive responsibilities.
- Dependency direction or shared-component policy needs defining.
- Abstraction vs duplication decisions need an explicit rule.

## 3. Output and evidence rules

1. Layer taxonomy with responsibilities and one owner per concern.
2. Component contracts (props/events/context/slots) and forbidden couplings.
3. Dependency-direction rules and shared-component policy.
4. Violation list with location and severity.
5. Abstraction-vs-duplication rule and migration plan.

The returned record must name the evidence source for each decision, separate verified facts from assumptions, and list what could not be inspected. The skill does not edit files or execute commands; delegated actions go to the host/user or the existing implementation owner under existing authority.

## 4. Boundaries

- Inputs inspected: see the SKILL.md Inputs to Inspect section.
- Telemetry contract and instrumentation design (real owner, not a sibling) routes to `observability-by-design`; this skill does not perform that owner's work.
- Actual-diff review routes to `code-reviewer`; this skill does not perform that owner's work.
- Frontend app mapping (batch-3 sibling seam) routes to `frontend-architecture-mapper`; this skill does not perform that owner's work.
- Design-token governance or theming (batch-3 sibling seam) routes to `design-system-token-governor`; this skill does not perform that owner's work.
- Broader discrimination set from evals/trigger-evals.json: the following owners' requests route away from this skill - `observability-by-design`, `architecture-designer`, `code-reviewer`, `domain-modeler`, `error-taxonomy-designer`, `edge-state-ux-designer`, `ux-design-iteration`, `mobile-viewport-craft`, `accessibility-test-harness`, `frontend-perf-engineer`, `validation-boundary-designer`, `tech-spec-writer`, `principal-code-analyst`, `performance-test-harness` (discrimination neighbours, not in-scope work).
- No production, deployment, spending or approval authority is granted by this reference.

## 5. Validation before returning

- Layer taxonomy and ownership are explicit and non-overlapping.
- Contracts name what each boundary accepts and forbids.
- Dependency direction is stated and shared components are constrained.
- Violations have locations and evidence, not adjectives.
- Abstraction-vs-duplication rule is stated; migration is ordered.
- No component was edited or refactor claimed.

