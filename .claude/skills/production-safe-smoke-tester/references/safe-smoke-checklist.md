# Production-safe smoke checklist and evidence rules

Reference for the production-safe-smoke-tester skill. It is method and record guidance only: it never directs the skill to edit code, run commands, use the network or claim production authority.

## 1. Core model

- Classification: read-only, seeded-fixture (read-only probes only), unsafe/forbidden. Any mutating probe is OUT OF SCOPE for smoke.
- Preferred probes: health, version, read-only queries, seeded-tenant reads. A dry-run/rollback plan is evidence about a future mutation, not a smoke probe.
- Evidence per probe: command, response, timestamp, environment/version, verdict.
- Stop conditions: unexpected status, data anomaly, permission denial, elevated latency.
- Unexercised list: auth, payments, mutations, jobs, third parties.
- Authority: host/user executes under production permission; skill only designs.

## 2. When this applies

- A deploy needs a quick production check without writing unsafe data.
- You must decide which probes are read-only and which are forbidden.
- A smoke plan exists but does not state what it does not exercise.
- The user asks how to design or validate a safe smoke plan or checklist for a deploy (a live production-health determination is an operational action for observability-operator, not a design task).

## 3. Output and evidence rules

1. Safe/unsafe operation inventory with classification.
2. Chosen probes with expected observables and evidence.
3. Stop conditions and escalation/rollback path.
4. Explicitly unexercised areas and residual risk.
5. Permissions/authority statement for the host/user.

Every claim in the returned record is backed by inspected evidence or explicitly labeled **assumption**, **UNKNOWN** or **UNRUN**. An empty or unrun check is never a PASS. The skill does not edit files or execute commands; delegated actions go to the host/user or the existing implementation owner under existing authority.

## 4. Boundaries

- Inputs inspected: see the SKILL.md Inputs to Inspect section.
- Stop and route out when the request matches another owner; see Stop Conditions.
- No production, deployment, spending or approval authority is granted by this reference.

## 5. Validation before returning

- Every probe classified as read-only, seeded-fixture (read-only probes only) or forbidden; any mutating probe is OUT OF SCOPE for smoke.
- No unsafe/destructive operation proposed as a smoke check.
- Expected observables and evidence defined per probe.
- Stop conditions, escalation and rollback owner stated.
- Unexercised areas and risk listed explicitly.
- Execution delegated; no production run claimed by the skill.
