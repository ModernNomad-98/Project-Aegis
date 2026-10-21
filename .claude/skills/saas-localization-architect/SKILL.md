---
name: saas-localization-architect
description: 'Use when a SaaS product must serve multiple locales: define locale, currency, date/time, language and content-localization boundaries, precedence and fallback without cross-tenant/cross-locale leaks.'
---

# SaaS Localization Architect

Terms: **family 4** - the discipline family in README.md and docs/skills-catalog.md; **read-only** means this skill inspects and returns guidance/records and never edits code or runs production actions.

## Purpose

Define the localization system boundaries for a multi-tenant SaaS product: which dimensions are localized and who owns them, locale negotiation and fallback, translated content versus formatting, currency/date/number rules, storage keys, caching/CDN behaviour and a test matrix, without cross-tenant or cross-locale data leaks.

The skill is **advisory and auto-invocable**. It produces guidance, records and review structure only; it does not edit code, run commands, use the network or grant production authority. Any implementation, execution or approval is a delegated host/user action under existing authority. It composes the nearest owners rather than duplicating them.

## Use When

- The product must serve multiple languages, locales, currencies or date/format conventions.
- It is unclear which layer owns translation versus formatting versus user preference.
- Locale negotiation, fallback or caching rules need to be designed or reviewed.
- A localization change risks cross-tenant/cross-locale leakage or stale cached text.

**Do not use when:** the request belongs to a named neighbouring owner (see Stop Conditions), or when inspection evidence is unavailable and the question would have to be answered by guessing.

## Inputs to Inspect

- Target markets and their locale/currency/format requirements.
- Content sources and the translation workflow.
- Tenant and user locale preferences and precedence.
- Storage, cache/CDN topology and keys.
- Test environments and supported locale coverage.
- Translation provenance: human vs machine translation, per-tenant policy and review/quality status.

## Workflow

1. Enumerate localizable dimensions (language, locale, currency, dates/numbers, content) and assign an owner per dimension.
2. Define locale negotiation and the fallback chain (user -> tenant -> product default) with explicit precedence.
3. Separate translated content from runtime formatting (dates, numbers, currency) and state the formatting library/contract.
4. Define currency presentation vs settlement rules and where each is decided.
5. Define storage/cache/CDN keys and invalidation so locale variants never bleed across tenants or locales.
6. Define the localization test matrix: locale coverage, fallbacks, RTL/formatting, and leak checks.
7. Define TWO separate algorithms: (1) locale preference resolution (user -> tenant -> product) and (2) translation-resource fallback (selected locale -> its parent-locale chain -> product default), so missing content never falls back to an unrelated tenant-default language.
8. Define translation provenance (human/machine, tenant policy, review status) and how it is stored, cached and invalidated.
9. Define currency presentation only; settlement remains with the billing/subscription owner and the boundary is recorded.
10. Return the boundary model, fallback matrix, storage/cache contract and test plan; do not implement UI or translations.

## Output Format

Return, in this order:

1. Localizable-dimension/owner map.
2. Locale negotiation and fallback matrix with precedence.
3. Content-translation vs formatting boundary.
4. Currency/date/number rules and storage/cache keys.
5. Localization test matrix and leak checks.

## Validation Checklist

- Every localizable dimension has an owner and a scope.
- Fallback chain is explicit and single per surface.
- Translation and formatting are separated; currency settlement vs display is stated.
- Cache/CDN keys are locale- and tenant-safe with invalidation rules.
- Test matrix covers locales, fallbacks and cross-locale leakage.
- No UI implementation or translation execution is claimed.
- Locale preference resolution and translation-resource fallback are separate, explicit algorithms.
- Translation provenance is defined in inputs, output and cache invalidation.
- Currency presentation is in scope; settlement is deferred with the boundary recorded.

## Gotchas

- Caching by URL without locale/tenant in the key serves the wrong language or another tenant's content.
- Storing formatted dates/numbers in the database freezes one locale's format into data.
- Fallback without an owner becomes 'English everywhere' after the first missing key.
- Currency formatting and currency settlement are different problems; conflating them misprices customers.
- Using one locale chain for both preference and translation fallback renders missing fr-CA strings in an unrelated tenant-default language.
- Runtime machine translation without provenance hides quality/review status and tenant policy.

## Stop Conditions

- The request is responsive layout and viewport behaviour: route to `mobile-viewport-craft`.
- The request is accessibility verification for localized UI: route to `accessibility-test-harness`.
- The request is frontend performance of localized bundles: route to `frontend-perf-engineer`.
- The trigger-evals file lists a broader 14-owner discrimination set (all named in the reference Boundaries); the three routes above are the primary Stop Conditions and the broader set is discrimination guidance.
- The caller wants this skill to implement, provision or execute the design: refuse; return the design for the authorized host/user.
- Required evidence (state, data map, policy or configuration) is unavailable: state UNKNOWN and ask instead of inventing it.

## Supporting Files

- [localization-boundaries](references/localization-boundaries.md) - Localization boundaries, fallback and cache rules.
- [evals/evals.json](evals/evals.json) - the 6 behaviour cases for this skill.
- [evals/trigger-evals.json](evals/trigger-evals.json) - 8 positive and 14 negative trigger-discrimination cases against the nearest owners.

**Source:** docs/skills-catalog.md - cat 02 #86 (Batch 2); coverage roadmap #86. The trigger description is the frontmatter description above; keep it under 1,024 parsed characters, concrete and trigger-oriented.
