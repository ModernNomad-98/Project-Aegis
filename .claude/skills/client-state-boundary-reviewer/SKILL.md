---
name: client-state-boundary-reviewer
description: 'Use when reviewing where UI state lives: classify state as local, shared, URL, server cache or persistent, and flag over-globalization, duplication, hydration and persistence risks with evidence.'
---

# Client State Boundary Reviewer

Terms: **family 14** - the discipline family in README.md and docs/skills-catalog.md; **read-only** means this skill inspects and returns guidance/records and never edits code or runs production actions.

## Purpose

Review where UI state lives: classify each state item as local, shared, URL, server cache or persistent, flag over-globalization, duplication, derived-state and hydration/persistence risks with file-level evidence, and recommend the minimal placement changes. Review-only.

The skill is **advisory and auto-invocable**. It produces guidance, records and review structure only; it does not edit code, run commands, use the network or grant production authority. Any implementation, execution or approval is a delegated host/user action under existing authority. It composes the nearest owners rather than duplicating them.

## Use When

- State placement in a frontend is being reviewed and may be over-globalized.
- UI state is duplicated or derived inconsistently across components.
- Hydration or persistence risks from state placement need review.
- A frontend review needs an evidence-based state map and ranked findings.

**Do not use when:** the request belongs to a named neighbouring owner (see Stop Conditions), or when inspection evidence is unavailable and the question would have to be answered by guessing.

## Inputs to Inspect

- State tree, stores/contexts and their consumers.
- URL schema and what navigation state is encoded.
- Server-cache library usage and query state.
- Persistence (localStorage/sessionStorage/IndexedDB) usage.
- Hydration/SSR setup and known mismatch reports.

## Workflow

1. Inventory state items and classify each by placement: local, shared, URL, server cache, persistent.
2. Map consumers and lifetimes; flag items whose placement does not match their scope.
3. Find duplication and derived state that can drift, with file-level evidence.
4. Assess hydration/persistence risks: server/client mismatch, sensitive-data persistence, stale restores.
5. Rank findings by risk and effort; propose the minimal placement change per finding.
6. Record what could not be inspected and the evidence needed.
7. Return the state map, ranked findings, placement recommendations and risks; do not refactor.

## Output Format

Return, in this order:

1. State inventory classified by placement and lifetime.
2. Consumer/lifetime map with misplacement findings.
3. Duplication/derived-state findings with file evidence.
4. Hydration/persistence risk findings.
5. Ranked recommendations with minimal-change options and not-inspected list.

## Validation Checklist

- Every reviewed state item has a placement classification and consumer evidence.
- Findings name file/line evidence, not adjectives.
- Duplication/derived-state drift is called out with impact.
- Hydration and persistence risks (incl. sensitive data) are assessed.
- Recommendations are minimal-change and ranked.
- The review is evidence-based and performs no refactor.

## Gotchas

- A global store is not a default; flag over-globalization with consumer evidence.
- Derived state stored twice drifts after the first update path forgets to sync.
- Persisting UI state can leak sensitive data or show stale permissions after a role change.
- Hydration mismatches are often client-only state rendered during SSR; classify it, not just the symptom.

## Stop Conditions

- The request is flag system and targeting state (existing pre-Batch-3 owner): route to `feature-flag-architect`.
- The request is server-data contract and cache ownership (Batch-3 sibling): route to `server-state-architect`.
- The request is URL representation and schema ownership (Batch-3 sibling): route to `url-state-architect`.
- The trigger-evals file lists a broader discrimination set (all named in the reference Boundaries); the routes above are the primary Stop Conditions.
- The caller wants this skill to implement, provision or execute the design: refuse; return the design for the authorized host/user.
- Required evidence (routes, state, cache config or policy) is unavailable: state UNKNOWN and ask instead of inventing it.

## Supporting Files

- [client-state-boundary-review](references/client-state-boundary-review.md) - Client-state boundary review: classification and risk findings.
- [evals/evals.json](evals/evals.json) - the 6 behaviour cases for this skill.
- [evals/trigger-evals.json](evals/trigger-evals.json) - 8 positive and 14 negative trigger-discrimination cases against the nearest owners.

**Source:** docs/skills-catalog.md - D12.2 product engineering craft pack (Batch 3/D110); coverage roadmap #168. The trigger description is the frontmatter description above; keep it under 1,024 parsed characters, concrete and trigger-oriented.
