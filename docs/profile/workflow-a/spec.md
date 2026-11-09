# Workflow A specification — synthetic retrieval-grounded support assistant

**Status:** design only; execution UNRUN. This specification describes what a
future authorised build would implement. Nothing here is implemented or run.

## Purpose and actor

The workflow serves a **synthetic support analyst** who must answer a policy
question from a 12-document synthetic corpus. It exists to make grounding,
citation, refusal and cost behaviour checkable offline. The actor is a single
assistant turn; there is no multi-agent delegation, no tool grant and no write
action.

## Workflow (start → end)

**Start.** A synthetic question and a session record are accepted by the intake
check. Inputs: `question`, `session_id`, `corpus_revision`, `requested_locale`
(optional). Reject empty, non-synthetic or malformed input without retrieval.

**Step 1 — Retrieve.** Chunk the corpus at section boundaries; rank at most 8
chunks with a deterministic lexical ranker (no model). Record chunk ids, scores
and the corpus revision.

**Step 2 — Screen.** Classify each retrieved chunk as `content` or
`instruction-bearing`. A chunk is instruction-bearing when it contains a request
to change the workflow, call a tool, ignore a rule or reveal hidden context. Such
a chunk is **excluded** from drafting and recorded in `security_flags`.

**Step 3 — Draft.** Compose an answer using only screened chunks. Every factual
sentence must carry at least one citation. If no screened chunk supports the
question, stop with `refused` and reason `unsupported`.

**Step 4 — Validate.** Validate the candidate object against
[output-schema.json](output-schema.json). Unknown fields, missing required
fields, a citation outside the corpus, or a confidence outside 0–1 fail closed to
`refused` with reason `schema_invalid`.

**Step 5 — Resolve citations.** Each citation must resolve to a corpus document
id and an existing section anchor, and the cited passage must contain the claim's
supporting terms (see [retrieval-citation-contract.md](retrieval-citation-contract.md)).
A failed resolution produces `refused` with reason `citation_unresolved`.

**Step 6 — Check the ceiling.** Estimate cost from the declared token
assumptions; if the estimate exceeds the per-answer ceiling, stop with
`refused` and reason `cost_ceiling` **before** emitting answer text.

**Step 7 — Decide the terminal status.**
- `answered` when steps 3–6 pass and confidence is at or above 0.55;
- `refused` when support, schema, citation or cost checks fail;
- `escalated` when the question is in scope but confidence is below 0.55, or the
  question needs a human decision (for example a policy exception).

**End.** Exactly one schema-valid object is emitted. Any other ending — two
objects, free text, a retry loop, a provider call — is a workflow failure.

## Inputs and outputs

| Item | Contract |
| --- | --- |
| Question | Synthetic text, 1–500 characters, no personal data. |
| Corpus | 12 synthetic documents; revision is a content digest, never a branch name. |
| Output | One JSON object per [output-schema.json](output-schema.json). |
| Citations | `doc-id#section-anchor`; must resolve in the declared corpus revision. |
| Terminal states | `answered`, `refused`, `escalated`; no other state is valid. |

## Failure and refusal path

A refusal is a **successful** workflow outcome, not an error: it carries a
machine-readable `refusal_reason` from the closed set `unsupported`,
`schema_invalid`, `citation_unresolved`, `cost_ceiling`, `out_of_scope`,
`instruction_bearing_source`. Refusals never include a guessed answer. An
escalation carries `escalation_role` (for example `policy-owner`) and the
reason; it never substitutes for a refusal when the corpus is simply silent.

## Approval gates

| Gate | Who decides | What is gated |
| --- | --- | --- |
| G1 synthetic corpus admission | this design (data card) | corpus must remain synthetic; no real data |
| G2 schema change | workflow owner | any change to the output contract |
| G3 ceiling change | cost owner | any change to the per-answer ceiling |
| G4 live/provider run | repository owner | any live, paid or provider-backed execution |
| G5 publication/installation | repository owner | any release, install or external publication |

G4 and G5 are **not granted** anywhere in this profile. Within the synthetic
boundary the workflow may proceed without a per-question human approval; it may
never self-approve an escalation.

## Acceptance checks for a future build (not run here)

1. All 20 fixtures produce the expected terminal state.
2. All seven NC cases in [negative-cases.md](negative-cases.md) fail closed.
3. Every `answered` object has at least one resolving citation.
4. No output object contains a citation to a non-corpus id.
5. An over-ceiling estimate returns `refused` before any answer text.
6. The run log records zero network calls and zero provider calls.

## Non-goals

- No live model call, provider integration, credential use or spend.
- No real customer data, tenant, production corpus or personal data.
- No answer-quality, retrieval-quality, safety or latency claim.
- No UI, API, deployment, installation or publication.
- No new skill, catalog entry, manifest entry or tool.
- No evaluation pass or judge verdict; execution is UNRUN.
- No authority beyond the synthetic, documents-only boundary of this item.
