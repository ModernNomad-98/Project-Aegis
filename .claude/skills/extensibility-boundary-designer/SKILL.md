---
name: extensibility-boundary-designer
description: 'Design extensibility boundaries: extension points, plugin contracts, capability limits, versioning, isolation and failure containment.'
---

# Extensibility Boundary Designer

Terms: **family 3** - core architecture & engineering (README roster family 3; docs/skills-catalog.md Phase 2 pack). **Advisory/design-only:** produces the named artifact and records; never edits code, runs commands, uses the network or grants production authority.

## Purpose

Design extension points and plugin contracts: isolation, permissions, versioning, compatibility and safe lifecycle without exposing unstable internals.

**Output artifact:** extension point map, plugin contract and capability/failure boundaries. The skill is auto-invocable and advisory: it composes the named neighbouring owners instead of duplicating them, and it returns the artifact plus open questions for the authorized implementer.

## Use When

- The request needs extension point map, plugin contract and capability/failure boundaries for a real system.
- The design is implicit/disputed or about to harden an assumption.
- A spec or review must record the artifact fields and boundaries explicitly.
- Implementation is about to start and the record it builds against is missing.

**Do not use when** the request belongs to a named neighbouring owner in Stop Conditions, or when the evidence needed for the artifact is unavailable.

## Inputs to Inspect

- Supported extension points and why each exists
- Plugin/extension contract and declared capabilities
- Permission and capability scope
- Lifecycle (install/upgrade/disable/remove)
- Isolation: process/tenant/resource limits
- Failure containment and timeout policy

## Workflow

1. Decide which extension points are justified by a real consumer need.
2. Define the contract and capability vocabulary.
3. Set lifecycle and compatibility rules.
4. Design isolation and failure containment.
5. Define permission model and review process.
6. Plan deprecation and versioning.
7. Write the extension acceptance tests.

## Output Format

Return, in this order:

1. Scope, evidence inventory and what could not be inspected.
2. Extension point map, plugin contract and capability/failure boundaries, with the fields listed in Inputs to Inspect.
3. Edge/failure cases and the chosen handling.
4. Boundary/handoff note naming the neighbouring owners (including the eval-only list below).
5. Verified facts, assumptions, UNKNOWN/UNVERIFIED items and the validation/test plan.

## Validation Checklist

- Every extension point has a consumer and a contract
- Capabilities are explicit and least-privilege
- Failures are contained with timeouts and limits
- Versioning/deprecation is documented
- Contract does not leak internal domain types

## Gotchas

- An extension point without a contract is an unstable API
- Unbounded plugins can exhaust shared resources
- Silent deprecation breaks tenant integrations

## Stop Conditions

- interface first designer requests route to `interface-first-designer`; this skill owns a different artifact.
- supply chain security reviewer requests route to `supply-chain-security-reviewer`; this skill owns a different artifact.
- api event architect requests route to `api-event-architect`; this skill owns a different artifact.
- The caller wants implementation, execution or approval: refuse; return the artifact for the authorized owner.
- Required evidence is unavailable: mark the artifact UNVERIFIED and state what is missing instead of inventing facts.
- **Eval-only discrimination set** (from `evals/trigger-evals.json` overlaps_with; eval-only, not a routing contract): `adr-writer`, `api-event-architect`, `architecture-designer`, `authorization-matrix-designer`, `change-classification-gate`, `code-reviewer`, `design-review-facilitator`, `human-approval-boundary`, `interface-first-designer`, `layered-architecture-enforcer`, `release-readiness-reviewer`, `security-pr-reviewer`, `supply-chain-security-reviewer`, `tech-spec-writer`.

## Supporting Files

- [plugin-contract-checklist](references/plugin-contract-checklist.md) - the concrete extension point map, plugin contract and capability/failure boundaries fields, construction method, checks and a worked table.
- [evals/evals.json](evals/evals.json) - six domain-specific behaviour cases.
- [evals/trigger-evals.json](evals/trigger-evals.json) - 8 positive and 14 negative trigger-discrimination cases against real manifest owners (including the reciprocal sibling case).

**Source:** docs/skills-catalog.md Phase 2 core architecture & engineering pack (Batch 4/D112); coverage cat 01 rows #29, #30. Description is trigger-first (capability front-loaded for truncated listings).
