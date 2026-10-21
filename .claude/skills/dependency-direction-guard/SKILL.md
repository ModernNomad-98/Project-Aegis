---
name: dependency-direction-guard
description: 'Use when modules, features or packages depend unexpectedly: derive the real import graph, detect inversions, feature coupling, platform leaks and cycles, state the allowed direction, rank fixes and record exceptions. Read-only dependency governance; it does not build, lint, or rewrite the graph.'
---

# Dependency Direction Guard

Terms: **family 3** - the discipline family in README.md and docs/skills-catalog.md; **read-only** means this skill inspects and returns guidance/records and never edits code or runs production actions.

## Purpose

Make dependency direction explicit and enforce it in an existing codebase: derive the real graph, find cycles, inversions, feature-to-feature coupling and platform leaks, then rank minimal fixes and record exceptions.

The skill is **advisory and auto-invocable**. It produces guidance, records and review structure only; it does not edit code, run commands, use the network or grant production authority. Any implementation, execution or approval is a delegated host/user action under existing authority. It composes the nearest owners rather than duplicating them.

## Use When

- Two features or modules seem unexpectedly coupled, or a dependency points the wrong way.
- You suspect import cycles or a shared 'utils' package that everything depends on.
- A boundary map or architecture doc exists but nobody knows whether the code still follows it.
- Before adding a dependency, you need to know which direction is allowed and what would be a violation.

**Do not use when:** the request belongs to a named neighbouring owner (see Stop Conditions), or when inspection evidence is unavailable and the question would have to be answered by guessing.

## Inputs to Inspect

- The actual source/import graph and package manifests for the modules in scope.
- Stated layering or allowed-direction policy, dependency rules in CI, and recorded exceptions.
- Feature/module ownership map and platform vs product code split.
- Recent changes that may have introduced a new edge.
- Known build-boundary constraints that affect allowed dependencies.

## Workflow

1. Define scope and the dependency policy; state allowed, forbidden and exception edges explicitly.
2. Derive the real graph from imports/manifests, not from intended diagrams.
3. Find cycles, inward/outward inversions, feature-to-feature coupling and platform leaks.
4. Rank findings by blast radius, coupling cost and fix size.
5. Propose the smallest fix per edge: invert via interface, extract shared primitive, move ownership, or record an exception.
6. Specify enforcement: dependency-rule CI, import lint, or a written exception register.
7. Return the graph findings, direction policy, ranked fixes and exceptions; edit nothing.

## Output Format

Return, in this order:

1. Dependency direction policy (allowed/forbidden/exception edges).
2. Real import graph with cycle and inversion evidence.
3. Ranked fix list with blast radius and effort.
4. Exception register entries with owner and review date.
5. Enforcement recommendation and verification plan.

## Validation Checklist

- Policy stated before judging edges; unstated rules marked assumptions.
- Graph derived from actual imports/manifests, not intended design.
- Cycles and inversions have exact paths, not adjectives.
- Fixes are minimal and ranked; no build or code changes made.
- Exceptions include owner, reason and review date.
- Enforcement mechanism named and testable.

## Gotchas

- A 'shared' package can become a second coupling layer that hides feature coupling.
- An allowed exception without review date becomes permanent policy.
- Type-only imports still couple modules at compile time in many stacks.
- Acyclic graph pictures can be stale; derive the graph from the tree.
- Fixing every edge at once is a rewrite; rank and sequence.

## Stop Conditions

- The question is layer semantics inside one module: route to layered-architecture-enforcer.
- The request is architectural design or placement: route to architecture-designer.
- The request is ordinary diff review: route to code-reviewer.
- The caller wants imports rewritten: return the plan and delegate edits.
- The graph cannot be derived: state what evidence is missing rather than guessing.

## Supporting Files

- [dependency-rules](references/dependency-rules.md) - Dependency direction policy, graph checks and exception register.
- [evals/evals.json](evals/evals.json) - the 6 behaviour cases for this skill.
- [evals/trigger-evals.json](evals/trigger-evals.json) - 8 positive and 14 negative trigger-discrimination cases against the nearest owners.

**Source:** docs/skills-catalog.md - cat 01 #7 (Dependency Direction Guard); coverage roadmap #7. The trigger description is the frontmatter description above; keep it under 1,024 parsed characters, concrete and trigger-oriented.
