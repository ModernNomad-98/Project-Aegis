# Dependency direction policy, graph checks and exception register

Reference for the dependency-direction-guard skill. It is method and record guidance only: it never directs the skill to edit code, run commands, use the network or claim production authority.

## 1. Core model

- Policy fields: allowed, forbidden, exception, owner, review date.
- Graph checks: cycles, inversions, feature-to-feature edges, platform leaks, generated-code edge cases.
- Detection sources: language import syntax, package manifests, build files, lint rules.
- Ranking: blast radius x coupling cost x fix size.
- Minimal fixes: invert via interface, extract shared primitive, move ownership, record exception.
- Enforcement: dependency-rule CI, import lint, exception register checked in review.

## 2. When this applies

- Two features or modules seem unexpectedly coupled, or a dependency points the wrong way.
- You suspect import cycles or a shared 'utils' package that everything depends on.
- A boundary map or architecture doc exists but nobody knows whether the code still follows it.
- Before adding a dependency, you need to know which direction is allowed and what would be a violation.

## 3. Output and evidence rules

1. Dependency direction policy (allowed/forbidden/exception edges).
2. Real import graph with cycle and inversion evidence.
3. Ranked fix list with blast radius and effort.
4. Exception register entries with owner and review date.
5. Enforcement recommendation and verification plan.

Every claim in the returned record is backed by inspected evidence or explicitly labeled **assumption**, **UNKNOWN** or **UNRUN**. An empty or unrun check is never a PASS. The skill does not edit files or execute commands; delegated actions go to the host/user or the existing implementation owner under existing authority.

## 4. Boundaries

- Inputs inspected: see the SKILL.md Inputs to Inspect section.
- Stop and route out when the request matches another owner; see Stop Conditions.
- No production, deployment, spending or approval authority is granted by this reference.

## 5. Validation before returning

- Policy stated before judging edges; unstated rules marked assumptions.
- Graph derived from actual imports/manifests, not intended design.
- Cycles and inversions have exact paths, not adjectives.
- Fixes are minimal and ranked; no build or code changes made.
- Exceptions include owner, reason and review date.
- Enforcement mechanism named and testable.
