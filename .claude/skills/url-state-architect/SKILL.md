---
name: url-state-architect
description: 'Use when UI state should be shareable: design which filters, tabs, search, sort, pagination and dialogs live in the URL, with versioned schema, defaults, validation, history and privacy rules.'
---

# URL State Architect

Terms: **family 14** - the discipline family in README.md and docs/skills-catalog.md; **read-only** means this skill inspects and returns guidance/records and never edits code or runs production actions.

## Purpose

Design URL state deliberately: which filters, tabs, search, sort, pagination and dialogs belong in the URL; a versioned schema with serialization rules, defaults/canonicalization, untrusted-input validation, history/back behavior, privacy redaction, compatibility and deep-link rules.

The skill is **advisory and auto-invocable**. It produces guidance, records and review structure only; it does not edit code, run commands, use the network or grant production authority. Any implementation, execution or approval is a delegated host/user action under existing authority. It composes the nearest owners rather than duplicating them.

## Use When

- UI state such as filters, tabs or pagination should be shareable via URL.
- URL parameters are inconsistent, unvalidated or not canonicalized.
- History/back behavior or deep links break with current URL state.
- URL state may expose sensitive data and needs privacy rules.

**Do not use when:** the request belongs to a named neighbouring owner (see Stop Conditions), or when inspection evidence is unavailable and the question would have to be answered by guessing.

## Inputs to Inspect

- Navigable state and which user intent should be shareable.
- Current route/query schema and any existing deep links.
- Constraints: cache keys, analytics, privacy and compatibility.
- Server/data expectations for validated parameters.
- Known broken back-button or canonicalization issues.

## Workflow

1. Decide the URL-state rule: which state is navigational/shareable versus local-only.
2. Design the schema and serialization: parameter names, types, arrays/nested objects, versioning.
3. Define defaults and canonicalization so equivalent states produce one canonical URL.
4. Define validation for untrusted URL input and the fallback behavior on invalid values.
5. Define history semantics: push vs replace, back/forward behavior and dialog/tab transitions.
6. Define privacy rules: which values must never appear in URLs and how they are redacted.
7. Return the URL schema, serialization table, validation/default rules, history model, privacy list and migration note; do not implement routing.

## Output Format

Return, in this order:

1. URL-state inclusion rule (navigational vs local).
2. Versioned parameter schema and serialization table.
3. Defaults/canonicalization and invalid-input fallback.
4. History/back behavior and deep-link contract.
5. Privacy redaction list and compatibility/migration note.

## Validation Checklist

- Each state item is explicitly URL vs local with a reason.
- Schema is versioned and serialization rules cover complex values.
- Defaults/canonicalization produce one canonical URL.
- Invalid/untrusted inputs have defined fallback behavior.
- History semantics and deep-link behavior are explicit.
- Privacy rules exclude sensitive values; no routing code claimed.

## Gotchas

- Encoding arrays/objects ad hoc produces incompatible URLs across releases; version it.
- Non-canonical URLs duplicate cache entries and analytics rows.
- Trusting URL parameters without validation turns a shareable link into an injection path.
- Dialog or tab state in the URL without history rules breaks the back button.

## Stop Conditions

- The request is external API contract semantics: route to `api-event-architect`.
- The request is route gates and denial behavior (Batch-3 sibling): route to `route-protection-designer`.
- The request is UI state placement review (Batch-3 sibling): route to `client-state-boundary-reviewer`.
- The trigger-evals file lists a broader 14-owner discrimination set (all named in the reference Boundaries); the routes above are the primary Stop Conditions.
- The caller wants this skill to implement, provision or execute the design: refuse; return the design for the authorized host/user.
- Required evidence (routes, state, cache config or policy) is unavailable: state UNKNOWN and ask instead of inventing it.

## Supporting Files

- [url-state-schema](references/url-state-schema.md) - URL state schema: serialization, canonicalization and privacy.
- [evals/evals.json](evals/evals.json) - the 6 behaviour cases for this skill.
- [evals/trigger-evals.json](evals/trigger-evals.json) - 8 positive and 14 negative trigger-discrimination cases against the nearest owners.

**Source:** docs/skills-catalog.md - D12.2 product engineering craft pack (Batch 3/D110); coverage roadmap #169. The trigger description is the frontmatter description above; keep it under 1,024 parsed characters, concrete and trigger-oriented.
