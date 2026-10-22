# Client-state boundary review: classification and risk findings

Reference for the client-state-boundary-reviewer skill. It is method and record guidance only: it never directs the skill to edit code, run commands, use the network or claim production authority.

## 1. Core model

- Every reviewed state item has a placement classification and consumer evidence.
- Findings name file/line evidence, not adjectives.
- Duplication/derived-state drift is called out with impact.
- Hydration and persistence risks (incl. sensitive data) are assessed.
- Recommendations are minimal-change and ranked.
- Every claim is backed by inspected evidence or labeled **assumption**, **UNKNOWN** or **UNRUN**; an empty check is never a PASS.

## 2. When this applies

- State placement in a frontend is being reviewed and may be over-globalized.
- UI state is duplicated or derived inconsistently across components.
- Hydration or persistence risks from state placement need review.
- A frontend review needs an evidence-based state map and ranked findings.

## 3. Output and evidence rules

1. State inventory classified by placement and lifetime.
2. Consumer/lifetime map with misplacement findings.
3. Duplication/derived-state findings with file evidence.
4. Hydration/persistence risk findings.
5. Ranked recommendations with minimal-change options and not-inspected list.

The returned record must name the evidence source for each decision, separate verified facts from assumptions, and list what could not be inspected. The skill does not edit files or execute commands; delegated actions go to the host/user or the existing implementation owner under existing authority.

## 4. Boundaries

- Inputs inspected: see the SKILL.md Inputs to Inspect section.
- Flag system and targeting state (existing pre-Batch-3 owner) routes to `feature-flag-architect`; this skill does not perform that owner's work.
- Server-data contract and cache ownership (batch-3 sibling) routes to `server-state-architect`; this skill does not perform that owner's work.
- Url representation and schema ownership (batch-3 sibling) routes to `url-state-architect`; this skill does not perform that owner's work.
- Broader discrimination set from evals/trigger-evals.json: the following owners' requests route away from this skill - `feature-flag-architect`, `performance-test-harness`, `load-test-planner`, `code-reviewer`, `full-codebase-auditor`, `caching-strategy-designer`, `observability-by-design`, `frontend-perf-engineer`, `edge-state-ux-designer`, `error-taxonomy-designer`, `mobile-viewport-craft`, `architecture-designer`, `api-event-architect`, `validation-boundary-designer` (discrimination neighbours, not in-scope work).
- No production, deployment, spending or approval authority is granted by this reference.

## 5. Validation before returning

- Every reviewed state item has a placement classification and consumer evidence.
- Findings name file/line evidence, not adjectives.
- Duplication/derived-state drift is called out with impact.
- Hydration and persistence risks (incl. sensitive data) are assessed.
- Recommendations are minimal-change and ranked.
- The review is evidence-based and performs no refactor.

