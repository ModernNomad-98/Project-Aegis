# Prompt Contract Template

Detail file for `model-context-designer`, workflow step 9. Loaded on demand.

A prompt contract is the one record that ties a model call's parts together:
which instruction runs, who owns it, what it may read, what it must return,
when it must decline, and which edits need an evaluation rerun before they
ship. The contract points to the owners of each part; it does not restate
them.

## The record

```
PROMPT CONTRACT — <instruction id>
Version: <semantic or sequential version> (previous: <version or "none">)
Owner: <named person or team who approves edits>
Call site: <feature / endpoint / job that makes the call>
Declared inputs: <segment names from the context design — nothing else
  may enter the window>
Output contract: <pointer to the structured-output-validator contract and
  its version — never a restated schema>
Decline when:
  - <condition> → <expected decline response or error code>
  - <condition> → <...>
Change policy: <table below, filled for this instruction>
Last evaluation run: <suite id + result + date, or "none yet">
Agent instruction custody: <for an agent: pointer to the versioned
  instruction artifact agent-harness-architect keeps; otherwise "not an
  agent">
```

## Change policy

Classify every kind of edit before it happens. The rule of thumb: if the
edit can change what the model returns, whether it declines, or what it
reads, the edit needs a rerun.

| Edit kind | Evaluation rerun | Why |
| --- | --- | --- |
| Output field added, renamed, removed or retyped | Needed; also update the output contract with `structured-output-validator` | Downstream parsers and graders depend on the shape. |
| Declared input added, removed or re-sourced | Needed | The model sees different content, so answers can change. |
| Decline condition added, removed or reworded | Needed | Refusal behavior is part of what the contract promises. |
| Instruction wording that changes task, tone or priority | Needed | Small wording edits routinely move outputs and refusals. |
| Model or provider version change behind the same instruction | Needed | Same prompt, different model, different behavior. |
| Typo or whitespace fix with no change in meaning, confirmed by the owner | Not needed; record the version bump | Keeps the history honest without spending a run. |
| Metadata only (owner, ticket link, comments outside the prompt text) | Not needed | The model never sees it. |

When in doubt, treat the edit as needing a rerun. The rerun itself is run
under `ai-evaluation-harness` *(manual-only)*, because running evaluations
spends tokens and money; this contract only says when one is required.

## Decline conditions

Every contract lists at least one. Typical sources:

- The request is outside the instruction's declared task.
- A required declared input is missing or failed its schema.
- The answer would need data the context design deliberately excludes.
- Confidence is below the grounding bar `ai-misinformation-guard` sets.

Each condition names the expected response (a fixed decline message, an
error code, or a hand-off to a person) so a grader can check it.

## Filled example

```
PROMPT CONTRACT — support-ticket-summarizer
Version: 4 (previous: 3)
Owner: Support tooling team (lead approves edits)
Call site: POST /tickets/{id}/summary
Declared inputs: system-instructions, ticket-body (capped), last-3-replies
  (capped), product-area tag
Output contract: structured-output-validator contract
  "ticket-summary" v2 (field "issue" renamed to "problem" in this version)
Decline when:
  - ticket-body is empty or failed its schema → error SUMMARY_NO_INPUT
  - ticket is in a language the evaluation suite does not cover →
    "Summary unavailable for this language" and route to a person
Change policy: v3 → v4 renames an output field → evaluation rerun needed;
  output contract updated to v2 first
Last evaluation run: summarizer-suite v7, passed, 2026-09-20 (v3)
Agent instruction custody: not an agent
```

Here the version bump is blocked from shipping until the rerun passes on
version 4, and the schema change goes to `structured-output-validator`
before the prompt changes.
