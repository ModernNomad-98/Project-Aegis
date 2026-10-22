# Design-token governance model: taxonomy, naming and drift

Reference for the design-system-token-governor skill. It is method and record guidance only: it never directs the skill to edit code, run commands, use the network or claim production authority.

## 1. Core model

- Token taxonomy and ownership are explicit; semantic layer is the only consumption surface.
- Single source of truth and export pipeline are named.
- Theme/dark-mode contract states fallback and per-tenant limits.
- Change governance defines add/rename/remove and deprecation evidence.
- Drift audit and migration plan include visual-regression protection.
- Every claim is backed by inspected evidence or labeled **assumption**, **UNKNOWN** or **UNRUN**; an empty check is never a PASS.

## 2. When this applies

- Design tokens are duplicated, hard-coded or drifting across components.
- Theming or dark mode needs a single token contract.
- Token naming/ownership needs rules and a change process.
- A design-system migration must avoid drift and visual regressions.

## 3. Output and evidence rules

1. Semantic token taxonomy with layers and owners.
2. Naming rules and component consumption policy.
3. Single source of truth and export/generation pipeline.
4. Theme/dark-mode contract with per-tenant limits and fallback.
5. Change governance and drift-proof migration/audit plan.

The returned record must name the evidence source for each decision, separate verified facts from assumptions, and list what could not be inspected. The skill does not edit files or execute commands; delegated actions go to the host/user or the existing implementation owner under existing authority.

## 4. Boundaries

- Inputs inspected: see the SKILL.md Inputs to Inspect section.
- Responsive layout and viewport behaviour routes to `mobile-viewport-craft`; this skill does not perform that owner's work.
- Design iteration and ux convergence routes to `ux-design-iteration`; this skill does not perform that owner's work.
- Component layer/ownership decisions (batch-3 sibling) routes to `component-boundary-designer`; this skill does not perform that owner's work.
- Broader discrimination set from evals/trigger-evals.json: the following owners' requests route away from this skill - `accessibility-test-harness`, `architecture-designer`, `code-reviewer`, `component-boundary-designer`, `edge-state-ux-designer`, `error-taxonomy-designer`, `frontend-perf-engineer`, `mobile-viewport-craft`, `notification-webhook-ux-designer`, `product-spec-writer`, `tech-spec-writer`, `ux-design-iteration`, `validation-boundary-designer`, `visual-regression-test-designer` (discrimination neighbours, not in-scope work).
- No production, deployment, spending or approval authority is granted by this reference.

## 5. Validation before returning

- Token taxonomy and ownership are explicit; semantic layer is the only consumption surface.
- Single source of truth and export pipeline are named.
- Theme/dark-mode contract states fallback and per-tenant limits.
- Change governance defines add/rename/remove and deprecation evidence.
- Drift audit and migration plan include visual-regression protection.
- No style or token file was edited or migration claimed.
