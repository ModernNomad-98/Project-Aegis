---
name: layered-architecture-enforcer
description: 'Use when code is layered or hexagonal: check presentation, domain, application, platform, data-access and infrastructure separation, flag layer violations and dependency leaks, and propose the smallest compliant change. Read-only architecture enforcement; it does not redesign the system, review ordinary diffs, or edit code.'
---

# Layered Architecture Enforcer

Terms: **family 3** - the discipline family in README.md and docs/skills-catalog.md; **read-only** means this skill inspects and returns guidance/records and never edits code or runs production actions.

## Purpose

Keep an existing layered or hexagonal architecture honest by mapping real layers, finding cross-layer calls, leaked persistence or framework types, and proposing the smallest compliant change with verification.

The skill is **advisory and auto-invocable**. It produces guidance, records and review structure only; it does not edit code, run commands, use the network or grant production authority. Any implementation, execution or approval is a delegated host/user action under existing authority. It composes the nearest owners rather than duplicating them.

## Use When

- A repository or module claims a layered/hexagonal/clean architecture and someone asks whether that still holds.
- A change crosses presentation, application, domain, platform, data-access or infrastructure boundaries.
- A review found domain code importing infrastructure, a controller holding business rules, or an adapter leaking framework types.
- Before a refactor you need the current layer map and the smallest compliant fix rather than a rewrite.

**Do not use when:** the request belongs to a named neighbouring owner (see Stop Conditions), or when inspection evidence is unavailable and the question would have to be answered by guessing.

## Inputs to Inspect

- Repository/module tree, build files and import graph rather than an assumed diagram.
- Architecture docs, ADRs or diagrams claiming the intended layers and dependency rule.
- Framework entry points, domain entities and adapters actually present.
- Existing tests and build boundaries that reveal intended seams.
- The change or question under review, with the files it touches.

## Workflow

1. State the claimed layer model and allowed dependency direction; mark unstated rules as assumptions.
2. Map each module to a layer from imports, build config, annotations and package naming, not folder names alone.
3. Trace cross-layer edges and identify persistence/framework types leaking into inner layers.
4. Classify findings as violation, allowed exception with recorded reason, or uncertain with missing evidence named.
5. Propose the smallest compliant change per violation and its trade-off.
6. Define verification: import/architecture test, focused unit tests, and a manual re-check of affected edges.
7. Return the layer map, violations, fixes and verification plan; do not edit code or claim a fix was verified.

## Output Format

Return, in this order:

1. Layer map with evidence for each assignment.
2. Cross-layer edge table with allowed/forbidden status.
3. Violation list with exact location and reasoning.
4. Smallest compliant change per finding, with trade-offs and verification steps.
5. Assumptions, UNKNOWNs and what could not be inspected.

## Validation Checklist

- Layer model and allowed direction stated before judging violations; unstated rules labeled assumptions.
- Layers mapped from imports/config/annotations, not only directory names.
- Every violation names the exact edge and evidence; exceptions carry a recorded reason.
- Each fix is the smallest compliant change, not a redesign; no code edited.
- Verification includes an architecture/import rule where feasible plus focused tests.
- Uninspected areas and uncertain edges reported, never guessed.

## Gotchas

- Folder names are not layers; a 'domain' directory importing the ORM is not a domain layer.
- An allowed exception without a recorded reason becomes a silent second architecture.
- A grand refactor hides the smallest fix and makes verification impossible.
- Hexagonal ports are often present in name only; check who implements and calls them.
- Framework types in service interfaces are violations even when tests pass.

## Stop Conditions

- The request is greenfield system design: route to architecture-designer.
- The request is an ordinary diff review: route to code-reviewer.
- The request is feature coupling / import-cycle policy: route to dependency-direction-guard.
- The request is whole-system style selection: route to architecture-advisor.
- The caller wants code edited: return the minimal change plan and delegate implementation.
- The tree cannot be inspected: state UNKNOWN and ask for evidence instead of inventing a layer map.

## Supporting Files

- [layer-rules](references/layer-rules.md) - Layer model, allowed edges and violation checklist.
- [evals/evals.json](evals/evals.json) - the 6 behaviour cases for this skill.
- [evals/trigger-evals.json](evals/trigger-evals.json) - 8 positive and 14 negative trigger-discrimination cases against the nearest owners.

**Source:** docs/skills-catalog.md - cat 01 #6 (Layered Architecture Enforcement); coverage roadmap #6. The trigger description is the frontmatter description above; keep it under 1,024 parsed characters, concrete and trigger-oriented.
