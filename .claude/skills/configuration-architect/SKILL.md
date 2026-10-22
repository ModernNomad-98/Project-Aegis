---
name: configuration-architect
description: 'Design config layers: build/runtime/tenant/user precedence, validation, ownership, secret references, drift detection and migration.'
---

# Configuration Architect

Terms: **family 3** - core architecture & engineering (README roster family 3; docs/skills-catalog.md Phase 2 pack). **Advisory/design-only:** produces the named artifact and records; never edits code, runs commands, uses the network or grants production authority.

## Purpose

Separate build-time config, runtime config, tenant settings, secrets, defaults and validation; define precedence and ownership; close the tenant-settings residual of #66.

**Output artifact:** configuration layer matrix with precedence and validation rules. The skill is auto-invocable and advisory: it composes the named neighbouring owners instead of duplicating them, and it returns the artifact plus open questions for the authorized implementer.

## Use When

- The request needs configuration layer matrix with precedence and validation rules for a real system.
- The design is implicit/disputed or about to harden an assumption.
- A spec or review must record the artifact fields and boundaries explicitly.
- Implementation is about to start and the record it builds against is missing.

**Do not use when** the request belongs to a named neighbouring owner in Stop Conditions, or when the evidence needed for the artifact is unavailable.

## Inputs to Inspect

- Layers: build, runtime, tenant, user
- Precedence/override rules and conflict handling
- Validation per layer and on load
- Secret references vs literal values
- Ownership and change process per layer
- Drift detection and audit trail

## Workflow

1. Inventory the config surface and hardcoded values.
2. Assign each setting to exactly one layer.
3. Define precedence and conflict resolution.
4. Specify validation and fail-fast behaviour.
5. Design secret references and precedence.
6. Plan ownership, audit and drift detection.
7. Define migration and rollback for layer moves.

## Output Format

Return, in this order:

1. Scope, evidence inventory and what could not be inspected.
2. Configuration layer matrix with precedence and validation rules, with the fields listed in Inputs to Inspect.
3. Edge/failure cases and the chosen handling.
4. Boundary/handoff note naming the neighbouring owners (including the eval-only list below).
5. Verified facts, assumptions, UNKNOWN/UNVERIFIED items and the validation/test plan.

## Validation Checklist

- Every setting has one owning layer
- Precedence is total and documented
- Secrets are references not literals
- Invalid config fails at startup with a safe message
- Drift is detectable and auditable

## Gotchas

- Two sources of truth for one setting cause silent tenant bugs
- Validation that happens after use is decoration
- Moving a setting between layers without migration breaks environments

## Stop Conditions

- environment parity reviewer requests route to `environment-parity-reviewer`; this skill owns a different artifact.
- secrets identity hardener requests route to `secrets-identity-hardener`; this skill owns a different artifact.
- vite build qa engineer requests route to `vite-build-qa-engineer`; this skill owns a different artifact.
- The caller wants implementation, execution or approval: refuse; return the artifact for the authorized owner.
- Required evidence is unavailable: mark the artifact UNVERIFIED and state what is missing instead of inventing facts.
- **Eval-only discrimination set** (from `evals/trigger-evals.json` overlaps_with; eval-only, not a routing contract): `adr-writer`, `architecture-designer`, `code-reviewer`, `design-review-facilitator`, `environment-parity-reviewer`, `feature-flag-architect`, `human-approval-boundary`, `observability-by-design`, `plan-entitlement-architect`, `secrets-identity-hardener`, `tech-spec-writer`, `tenant-modeler`, `user-preference-architect`, `vite-build-qa-engineer`.

## Supporting Files

- [config-layer-matrix](references/config-layer-matrix.md) - the concrete configuration layer matrix with precedence and validation rules fields, construction method, checks and a worked table.
- [evals/evals.json](evals/evals.json) - six domain-specific behaviour cases.
- [evals/trigger-evals.json](evals/trigger-evals.json) - 8 positive and 14 negative trigger-discrimination cases against real manifest owners (including the reciprocal sibling case).

**Source:** docs/skills-catalog.md Phase 2 core architecture & engineering pack (Batch 4/D112); coverage cat 01, 02 rows #28, #66. Description is trigger-first (capability front-loaded for truncated listings).
