---
name: data-flow-diagrammer
description: 'Use when data movement is unclear: inventory sources, sinks, stores, transforms and side effects, produce a trustworthy text/Mermaid data-flow diagram with trust boundaries, assumptions and explicitly unverified elements. Documentation-only; it does not design components, instrument telemetry, or claim runtime truth.'
---

# Data Flow Diagrammer

Terms: **family 3** - the discipline family in README.md and docs/skills-catalog.md; **read-only** means this skill inspects and returns guidance/records and never edits code or runs production actions.

## Purpose

Produce a trustworthy data-flow view of an existing system: inventory inputs, outputs, stores, transforms, trust boundaries and side effects; render a diagram with assumptions and unverified elements clearly marked.

The skill is **advisory and auto-invocable**. It produces guidance, records and review structure only; it does not edit code, run commands, use the network or grant production authority. Any implementation, execution or approval is a delegated host/user action under existing authority. It composes the nearest owners rather than duplicating them.

## Use When

- Data movement, storage or side effects are unclear from code and docs.
- Security, privacy, tenancy or data-retention review needs a data-flow view.
- An existing diagram is stale and nobody trusts it.
- You need to show where data crosses trust boundaries or where side effects occur.

**Do not use when:** the request belongs to a named neighbouring owner (see Stop Conditions), or when inspection evidence is unavailable and the question would have to be answered by guessing. This skill diagrams flows only: generic PII location/lifecycle requests (retention, deletion, residency, derived copies) route to `pii-lifecycle-designer`.

## Inputs to Inspect

- Code paths that read/write data, API handlers, jobs, integrations and storage definitions.
- Requirements and privacy/security classification for the data involved.
- Existing diagrams and their dates; treat them as claims to verify.
- Trust-boundary definitions and tenant/identity context.
- Known side effects: emails, payments, events, webhooks, file writes.

## Workflow

1. Define scope and the level of detail; exclude unrelated subsystems explicitly.
2. Inventory sources, sinks, stores, transforms and side effects from evidence.
3. Trace each principal data item from source through transforms to sinks; mark where it crosses trust boundaries.
4. Render a text or Mermaid flow with a legend and numbered nodes/edges.
5. Mark assumptions, stale claims and unverified elements distinctly; never present them as fact.
6. List open questions that would change the diagram.
7. Return the diagram plus legend, assumptions and questions; do not design components or claim runtime behavior.

## Output Format

Return, in this order:

1. Data-flow diagram (Mermaid or plain text) with legend and numbered nodes.
2. Sources/sinks/stores/transforms/side-effects inventory with evidence.
3. Trust-boundary overlay and data-item trace table.
4. Assumptions, stale claims and unverified elements list.
5. Open questions that would change the picture.

## Validation Checklist

- Scope and detail level stated; out-of-scope marked.
- Every node/edge has evidence or is labeled unverified.
- Trust boundaries drawn and data crossings identified.
- Side effects included, not just storage.
- Legend explains notation; assumptions/questions separated from verified facts.
- No component design, telemetry design or runtime claim was made.

## Gotchas

- Never reproduce secrets, tokens or PII in the diagram; use classification labels and compose with sensitive-disclosure-guard.
- A diagram copied from docs is a claim, not evidence; verify it against code.
- Missing side effects (emails, payments, webhooks) is the most common false diagram.
- Too much detail hides the trust boundary; choose a named level.
- Unverified elements presented as facts corrupt security and privacy review.
- A data-flow diagram is not a component or deployment diagram.

## Stop Conditions

- The request is component design or placement: route to architecture-designer.
- The request is telemetry/logging design: route to observability-by-design.
- The request is threat modeling rather than a diagram: route to threat-modeler.
- The request is PII location or lifecycle design (retention, deletion, residency, derived copies): route to `pii-lifecycle-designer`; this skill only diagrams the current flows.
- The caller wants runtime traces or measured behaviour: the diagram is static evidence; delegate execution.
- Source code is unavailable and requirements too thin: state UNKNOWN and ask.

## Supporting Files

- [data-flow-conventions](references/data-flow-conventions.md) - Data-flow notation, trust boundaries and evidence rules.
- [evals/evals.json](evals/evals.json) - the 5 behaviour cases for this skill.
- [evals/trigger-evals.json](evals/trigger-evals.json) - 8 positive and 14 negative trigger-discrimination cases against the nearest owners.

**Source:** docs/skills-catalog.md - cat 01 #49 (Data Flow Diagramming); coverage roadmap #49. The trigger description is the frontmatter description above; keep it under 1,024 parsed characters, concrete and trigger-oriented.
