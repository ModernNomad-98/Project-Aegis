# PWA boundary checklist: scope, caches, updates and privacy

Reference for the pwa-boundary-reviewer skill. It is method and record guidance only: it never directs the skill to edit code, run commands, use the network or claim production authority.

## 1. Core model

- Registration scope and production-only gating are reviewed.
- Cache policy is explicit per asset class.
- Update/activation flow defines waiting/skipWaiting and reload behavior.
- Offline fallback is defined and stale data is labeled.
- Install prompt and push boundaries are reviewed.
- Every claim is backed by inspected evidence or labeled **assumption**, **UNKNOWN** or **UNRUN**; an empty check is never a PASS.

## 2. When this applies

- A web app is adding or reviewing PWA/service-worker behavior.
- Cache strategy, update/activation or offline fallback behavior needs review.
- Install-prompt or push-notification boundaries are unclear.
- Cached data may create security/privacy or stale-behavior risks.

## 3. Output and evidence rules

1. Registration/scope review with production gating.
2. Per-class cache strategy review.
3. Update/activation flow review and stale-client behavior.
4. Offline fallback and install/push boundary review.
5. Cached-data security/privacy findings and a risk checklist.

The returned record must name the evidence source for each decision, separate verified facts from assumptions, and list what could not be inspected. The skill does not edit files or execute commands; delegated actions go to the host/user or the existing implementation owner under existing authority.

## 4. Boundaries

- Inputs inspected: see the SKILL.md Inputs to Inspect section.
- Offline persistence/sync architecture routes to `offline-first-sync-architect`; this skill does not perform that owner's work.
- Notification/webhook ux and delivery behavior routes to `notification-webhook-ux-designer`; this skill does not perform that owner's work.
- Security review of an actual diff routes to `security-pr-reviewer`; this skill does not perform that owner's work.
- Broader discrimination set from evals/trigger-evals.json: the following owners' requests route away from this skill - `accessibility-test-harness`, `caching-strategy-designer`, `edge-state-ux-designer`, `error-taxonomy-designer`, `frontend-perf-engineer`, `incident-response-runbook`, `mobile-viewport-craft`, `notification-webhook-ux-designer`, `observability-by-design`, `offline-first-sync-architect`, `security-pr-reviewer`, `slo-reliability-architect`, `synthetic-monitoring-architect`, `vite-build-qa-engineer` (discrimination neighbours, not in-scope work).
- No production, deployment, spending or approval authority is granted by this reference.

## 5. Validation before returning

- Registration scope and production-only gating are reviewed.
- Cache policy is explicit per asset class.
- Update/activation flow defines waiting/skipWaiting and reload behavior.
- Offline fallback is defined and stale data is labeled.
- Install prompt and push boundaries are reviewed.
- Cached-data security/privacy risks are named; no service-worker edit claimed.
