# Localization boundaries, fallback and cache rules

Reference for the saas-localization-architect skill. It is method and record guidance only: it never directs the skill to edit code, run commands, use the network or claim production authority.

## 1. Core model

- Every localizable dimension has an owner and a scope.
- Fallback chain is explicit and single per surface.
- Translation and formatting are separated; currency settlement vs display is stated.
- Cache/CDN keys are locale- and tenant-safe with invalidation rules.
- Test matrix covers locales, fallbacks and cross-locale leakage.
- Every claim is backed by inspected evidence or labeled **assumption**, **UNKNOWN** or **UNRUN**; an empty check is never a PASS.

## 2. When this applies

- The product must serve multiple languages, locales, currencies or date/format conventions.
- It is unclear which layer owns translation versus formatting versus user preference.
- Locale negotiation, fallback or caching rules need to be designed or reviewed.
- A localization change risks cross-tenant/cross-locale leakage or stale cached text.

## 3. Output and evidence rules

1. Localizable-dimension/owner map.
2. Locale negotiation and fallback matrix with precedence.
3. Content-translation vs formatting boundary.
4. Currency/date/number rules and storage/cache keys.
5. Localization test matrix and leak checks.

The returned record must name the evidence source for each decision, separate verified facts from assumptions, and list what could not be inspected. The skill does not edit files or execute commands; delegated actions go to the host/user or the existing implementation owner under existing authority.

## 4. Boundaries

- Inputs inspected: see the SKILL.md Inputs to Inspect section.
- Responsive layout and viewport behaviour routes to `mobile-viewport-craft`; this skill does not perform that owner's work.
- Accessibility verification for localized ui routes to `accessibility-test-harness`; this skill does not perform that owner's work.
- Frontend performance of localized bundles routes to `frontend-perf-engineer`; this skill does not perform that owner's work.
- No production, deployment, spending or approval authority is granted by this reference.

## 5. Validation before returning

- Every localizable dimension has an owner and a scope.
- Fallback chain is explicit and single per surface.
- Translation and formatting are separated; currency settlement vs display is stated.
- Cache/CDN keys are locale- and tenant-safe with invalidation rules.
- Test matrix covers locales, fallbacks and cross-locale leakage.
- No UI implementation or translation execution is claimed.
