# URL state schema: serialization, canonicalization and privacy

Reference for the url-state-architect skill. It is method and record guidance only: it never directs the skill to edit code, run commands, use the network or claim production authority.

## 1. Core model

- Each state item is explicitly URL vs local with a reason.
- Schema is versioned and serialization rules cover complex values.
- Defaults/canonicalization produce one canonical URL.
- Invalid/untrusted inputs have defined fallback behavior.
- History semantics and deep-link behavior are explicit.
- Every claim is backed by inspected evidence or labeled **assumption**, **UNKNOWN** or **UNRUN**; an empty check is never a PASS.

## 2. When this applies

- UI state such as filters, tabs or pagination should be shareable via URL.
- URL parameters are inconsistent, unvalidated or not canonicalized.
- History/back behavior or deep links break with current URL state.
- URL state may expose sensitive data and needs privacy rules.

## 3. Output and evidence rules

1. URL-state inclusion rule (navigational vs local).
2. Versioned parameter schema and serialization table.
3. Defaults/canonicalization and invalid-input fallback.
4. History/back behavior and deep-link contract.
5. Privacy redaction list and compatibility/migration note.

The returned record must name the evidence source for each decision, separate verified facts from assumptions, and list what could not be inspected. The skill does not edit files or execute commands; delegated actions go to the host/user or the existing implementation owner under existing authority.

## 4. Boundaries

- Inputs inspected: see the SKILL.md Inputs to Inspect section.
- External api contract semantics routes to `api-event-architect`; this skill does not perform that owner's work.
- Route gates and denial behavior (batch-3 sibling) routes to `route-protection-designer`; this skill does not perform that owner's work.
- UI state placement review (batch-3 sibling) routes to `client-state-boundary-reviewer`; this skill does not perform that owner's work.
- Broader discrimination set from evals/trigger-evals.json: the following owners' requests route away from this skill - `accessibility-test-harness`, `api-event-architect`, `code-reviewer`, `edge-state-ux-designer`, `error-taxonomy-designer`, `frontend-perf-engineer`, `mobile-viewport-craft`, `notification-webhook-ux-designer`, `product-spec-writer`, `route-protection-designer`, `tech-spec-writer`, `ux-design-iteration`, `validation-boundary-designer`, `visual-regression-test-designer` (discrimination neighbours, not in-scope work).
- No production, deployment, spending or approval authority is granted by this reference.

## 5. Validation before returning

- Each state item is explicitly URL vs local with a reason.
- Schema is versioned and serialization rules cover complex values.
- Defaults/canonicalization produce one canonical URL.
- Invalid/untrusted inputs have defined fallback behavior.
- History semantics and deep-link behavior are explicit.
- Privacy rules exclude sensitive values; no routing code claimed.
