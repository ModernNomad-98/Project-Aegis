# Interface contract template, compatibility and migration

Reference for the interface-first-designer skill. It is method and record guidance only: it never directs the skill to edit code, run commands, use the network or claim production authority.

## 1. Core model

- Template fields: purpose, callers, operations, inputs/outputs, errors, invariants, compatibility, versions.
- Ports vs adapters: inner layers own interfaces; adapters implement them.
- Compatibility: additive vs breaking, versioning, deprecation window, stored command/message impact.
- Migration order: expand -> migrate callers -> contract; rollback at each step.
- Test doubles: fake adapter, contract tests, golden payloads.
- Smallest proving slice and stop-before-implementation rule.

## 2. When this applies

- Multiple callers or teams will depend on a new or changing interface.
- Internals are unsettled but the external contract must be stable first.
- A change risks breaking callers, stored commands/messages, or compatibility guarantees.
- You need the seam for test doubles and an ordered migration before coding.

## 3. Output and evidence rules

1. Contract specification: operations, inputs/outputs, errors and invariants.
2. Adapter plan distinguishing ports from implementations.
3. Compatibility/versioning and migration/rollback plan.
4. Test-double plan and contract-test strategy.
5. Open questions and the smallest proving slice.

Every claim in the returned record is backed by inspected evidence or explicitly labeled **assumption**, **UNKNOWN** or **UNRUN**. An empty or unrun check is never a PASS. The skill does not edit files or execute commands; delegated actions go to the host/user or the existing implementation owner under existing authority.

## 4. Boundaries

- Inputs inspected: see the SKILL.md Inputs to Inspect section.
- Stop and route out when the request matches another owner; see Stop Conditions.
- No production, deployment, spending or approval authority is granted by this reference.

## 5. Validation before returning

- Callers and constraints inventoried; unknown callers labeled.
- Contract derived from use cases and invariants, not current internals.
- Error semantics, compatibility and versioning explicit.
- Adapters and test doubles specified without implementation.
- Migration order and rollback recorded.
- No implementation was performed or claimed.
