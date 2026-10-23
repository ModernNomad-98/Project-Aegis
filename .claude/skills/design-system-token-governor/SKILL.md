---
name: design-system-token-governor
description: 'Use when design tokens need governing: semantic tokens for color, spacing, typography, state and theme, one source of truth, naming rules, theming/dark mode and migration-drift-resistant change.'
---

# Design System Token Governor

Terms: **family 14** - the discipline family in README.md and docs/skills-catalog.md; **read-only** means this skill inspects and returns guidance/records and never edits code or runs production actions.

## Purpose

Govern design tokens as one source of truth: a semantic token taxonomy (color, spacing, typography, state, theme) with naming rules, export pipeline, component consumption rules, theming/dark-mode contract, change governance and a migration-drift-resistant change.

The skill is **advisory and auto-invocable**. It produces guidance, records and review structure only; it does not edit code, run commands, use the network or grant production authority. Any implementation, execution or approval is a delegated host/user action under existing authority. It composes the nearest owners rather than duplicating them.

## Use When

- Design tokens are duplicated, hard-coded or drifting across components.
- Theming or dark mode needs a single token contract.
- Token naming/ownership needs rules and a change process.
- A design-system migration must avoid drift and visual regressions.

**Do not use when:** the request belongs to a named neighbouring owner (see Stop Conditions), or when inspection evidence is unavailable and the question would have to be answered by guessing.

## Inputs to Inspect

- Brand/theme requirements and existing design tokens.
- Component library usage of colors, spacing, typography and states.
- Theming requirements (light/dark/high-contrast, per-tenant theme).
- Build/export pipeline and how tokens reach components.
- Known drift, hard-coded values and visual-regression findings.

## Workflow

1. Define the semantic token taxonomy and the layers (primitive/reference/system/semantic) with owners.
2. Set naming rules and decide which tokens components may consume (semantic only).
3. Define the single source of truth and the export/generation pipeline to CSS/JS targets.
4. Design the theming/dark-mode contract, including per-tenant theme limits and fallback.
5. Define change governance: who may add/rename/remove tokens, deprecation and review evidence.
6. Plan the migration-drift-resistant change: codemods/lint rules, visual-regression baselines and staged adoption.
7. Return the token model, naming rules, theme contract, drift audit and migration plan; do not edit styles.

## Output Format

Return, in this order:

1. Semantic token taxonomy with layers and owners.
2. Naming rules and component consumption policy.
3. Single source of truth and export/generation pipeline.
4. Theme/dark-mode contract with per-tenant limits and fallback.
5. Change governance and migration-drift-resistant change/audit plan.

## Validation Checklist

- Token taxonomy and ownership are explicit; semantic layer is the only consumption surface.
- Single source of truth and export pipeline are named.
- Theme/dark-mode contract states fallback and per-tenant limits.
- Change governance defines add/rename/remove and deprecation evidence.
- Drift audit and migration plan include visual-regression protection.
- No style or token file was edited or migration claimed.

## Gotchas

- Components consuming primitive tokens directly make theming and dark mode unmaintainable.
- Renaming a token without a deprecation window breaks consumer builds silently.
- Hard-coded hex values are token drift even if they match today's palette.
- Per-tenant themes without limits can break contrast and accessibility requirements.

## Stop Conditions

- The request is responsive layout and viewport behaviour: route to `mobile-viewport-craft`.
- The request is design iteration and UX convergence: route to `ux-design-iteration`.
- The request is component layer/ownership decisions (Batch-3 sibling): route to `component-boundary-designer`.
- The trigger-evals file lists a broader discrimination set (all named in the reference Boundaries); the routes above are the primary Stop Conditions.
- The caller wants this skill to implement, provision or execute the design: refuse; return the design for the authorized host/user.
- Required evidence (routes, state, cache config or policy) is unavailable: state UNKNOWN and ask instead of inventing it.

## Supporting Files

- [token-governance-model](references/token-governance-model.md) - Design-token governance model: taxonomy, naming and drift.
- [evals/evals.json](evals/evals.json) - the 6 behaviour cases for this skill.
- [evals/trigger-evals.json](evals/trigger-evals.json) - 8 positive and 14 negative trigger-discrimination cases against the nearest owners.

**Source:** docs/skills-catalog.md - D12.2 product engineering craft pack (Batch 3/D110); coverage roadmap #163. The trigger description is the frontmatter description above; keep it under 1,024 parsed characters, concrete and trigger-oriented.
