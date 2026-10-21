# Data-flow notation, trust boundaries and evidence rules

Reference for the data-flow-diagrammer skill. It is method and record guidance only: it never directs the skill to edit code, run commands, use the network or claim production authority.

## 1. Core model

- Levels: context, level-1 data flows, focused detail; name the chosen level.
- Nodes: sources, sinks, stores, transforms, external systems, side effects.
- Edges: data items with classification and crossing direction.
- Trust boundaries: identity/tenant/network/process boundaries marked and crossings listed.
- Evidence rules: code/doc reference per node or 'unverified' label.
- Assumption/questions section separate from verified facts.

## 2. When this applies

- Data movement, storage or side effects are unclear from code and docs.
- Security, privacy, tenancy or data-retention review needs a data-flow view.
- An existing diagram is stale and nobody trusts it.
- You need to show where data crosses trust boundaries or where side effects occur.

## 3. Output and evidence rules

1. Data-flow diagram (Mermaid or plain text) with legend and numbered nodes.
2. Sources/sinks/stores/transforms/side-effects inventory with evidence.
3. Trust-boundary overlay and data-item trace table.
4. Assumptions, stale claims and unverified elements list.
5. Open questions that would change the picture.

Every claim in the returned record is backed by inspected evidence or explicitly labeled **assumption**, **UNKNOWN** or **UNRUN**. An empty or unrun check is never a PASS. The skill does not edit files or execute commands; delegated actions go to the host/user or the existing implementation owner under existing authority.

## 4. Boundaries

- Inputs inspected: see the SKILL.md Inputs to Inspect section.
- Stop and route out when the request matches another owner; see Stop Conditions.
- No production, deployment, spending or approval authority is granted by this reference.

## 5. Validation before returning

- Scope and detail level stated; out-of-scope marked.
- Every node/edge has evidence or is labeled unverified.
- Trust boundaries drawn and data crossings identified.
- Side effects included, not just storage.
- Legend explains notation; assumptions/questions separated from verified facts.
- No component design, telemetry design or runtime claim was made.
