---
name: pwa-boundary-reviewer
description: 'Use when a web app adds PWA behavior: review service-worker registration/scope, per-class cache strategy, update/activation flow, offline fallback, install prompt, push boundary and production-only behavior.'
---

# PWA Boundary Reviewer

Terms: **family 14** - the discipline family in README.md and docs/skills-catalog.md; **read-only** means this skill inspects and returns guidance/records and never edits code or runs production actions.

## Purpose

Review PWA boundaries: service-worker registration and scope, per-asset-class cache strategy, update/activation flow, offline fallback and stale UX, install-prompt behavior, push-notification boundary, cached-data security/privacy and production-only behavior. Review-only.

The skill is **advisory and auto-invocable**. It produces guidance, records and review structure only; it does not edit code, run commands, use the network or grant production authority. Any implementation, execution or approval is a delegated host/user action under existing authority. It composes the nearest owners rather than duplicating them.

## Use When

- A web app is adding or reviewing PWA/service-worker behavior.
- Cache strategy, update/activation or offline fallback behavior needs review.
- Install-prompt or push-notification boundaries are unclear.
- Cached data may create security/privacy or stale-behavior risks.

**Do not use when:** the request belongs to a named neighbouring owner (see Stop Conditions), or when inspection evidence is unavailable and the question would have to be answered by guessing.

## Inputs to Inspect

- Service-worker registration code, scope and build integration.
- Asset classes and desired cache policy per class.
- Update/activation flow and user-facing prompts.
- Offline fallback UX and stale-data behavior.
- Push-notification setup and install-prompt behavior; production/dev differences.

## Workflow

1. Review service-worker registration: scope, build integration, production-only gating and failure behavior.
2. Classify assets (shell, static, API, documents, media) and review the cache strategy per class.
3. Review update/activation flow: waiting workers, skipWaiting control, reload behavior and stale-client UX.
4. Review offline fallback: what is served offline, which navigation fallbacks exist and how stale data is labeled.
5. Review install-prompt behavior and when it is offered.
6. Review the push-notification boundary and the security/privacy of cached data (tokens, PII, per-user content).
7. Return the boundary review, cache policy, update flow, risks and checklist; do not change the service worker.

## Output Format

Return, in this order:

1. Registration/scope review with production gating.
2. Per-class cache strategy review.
3. Update/activation flow review and stale-client behavior.
4. Offline fallback and install/push boundary review.
5. Cached-data security/privacy findings and a risk checklist.

## Validation Checklist

- Registration scope and production-only gating are reviewed.
- Cache policy is explicit per asset class.
- Update/activation flow defines waiting/skipWaiting and reload behavior.
- Offline fallback is defined and stale data is labeled.
- Install prompt and push boundaries are reviewed.
- Cached-data security/privacy risks are named; no service-worker edit claimed.

## Gotchas

- Caching an API response with per-user data can leak one user's data to another on a shared browser.
- A skipWaiting activation without a reload leaves clients running mixed assets.
- An offline shell that hides errors makes users think data is current.
- A service worker scoped too broadly can intercept unrelated routes.

## Stop Conditions

- The request is offline persistence/sync architecture: route to `offline-first-sync-architect`.
- The request is notification/webhook UX and delivery behavior: route to `notification-webhook-ux-designer`.
- The request is security review of an actual diff: route to `security-pr-reviewer`.
- The trigger-evals file lists a broader 14-owner discrimination set (all named in the reference Boundaries); the routes above are the primary Stop Conditions.
- The caller wants this skill to implement, provision or execute the design: refuse; return the design for the authorized host/user.
- Required evidence (routes, state, cache config or policy) is unavailable: state UNKNOWN and ask instead of inventing it.

## Supporting Files

- [pwa-boundary-checklist](references/pwa-boundary-checklist.md) - PWA boundary checklist: scope, caches, updates and privacy.
- [evals/evals.json](evals/evals.json) - the 6 behaviour cases for this skill.
- [evals/trigger-evals.json](evals/trigger-evals.json) - 8 positive and 14 negative trigger-discrimination cases against the nearest owners.

**Source:** docs/skills-catalog.md - D12.2 product engineering craft pack (Batch 3/D110); coverage roadmap #176. The trigger description is the frontmatter description above; keep it under 1,024 parsed characters, concrete and trigger-oriented.
