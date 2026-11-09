# Cost model — workflow A (offline, $0)

**Status:** design model. No provider is contacted, no credential is read and no
metered call is made, so the design's measured spend is **$0** and its offline
path is **no provider**. The ceiling below is a *token* ceiling plus a mapping
rule; no price is invented.

## 1. Offline posture

| Item | Value |
| --- | --- |
| Provider calls | 0 |
| Network calls | 0 |
| Credentials read | 0 |
| Measured spend | **$0** |
| Execution status | UNRUN (design only) |

The design is deliberately cost-free: retrieval is lexical, screening is a rule
set, validation is a JSON Schema check and fixtures are hand-written. Nothing in
the offline path can incur a metered charge.

## 2. Per-answer ceiling

The ceiling is expressed in tokens so it does not depend on a price that could
change:

| Bound | Value | Rationale |
| --- | --- | --- |
| Input tokens per answer | 2,000 | 8 chunks × ≈200 tokens plus the question and instructions |
| Output tokens per answer | 400 | One short answer plus the JSON envelope |
| Retrieval chunks | 8 | Bounded ranker output |
| Retries | 0 | A failed check refuses; it does not retry |
| Wall-clock timeout | 30 s | A slow step stops the workflow, it does not extend the budget |

An estimate at or below both token bounds passes. An estimate above either bound
stops the workflow with `refused` and reason `cost_ceiling` **before** answer
text is produced. The output schema's `input_tokens` and `output_tokens` are
non-negative integers with no maximum, so the over-ceiling estimate itself can be
recorded in the refused object (`within_ceiling: false`); a schema bound at the
ceiling would have made a cost refusal unrepresentable.

## 3. Mapping to money (for a future authorised run only)

A future live run must map tokens to cents using the repository's owner-reviewed
price table at that time; this design asserts no rate. The mapping rule is:

```text
estimated_cents = ceil(input_tokens/1e6 * input_rate_cents_per_mtok)
                + ceil(output_tokens/1e6 * output_rate_cents_per_mtok)
```

The workflow stops when `estimated_cents` exceeds the ceiling recorded in the
owner-approved live configuration for that run. No such configuration exists for
this item, and none is proposed here.

## 4. Cost and provenance of the design itself

The profile's **offline workflow path** costs $0: it makes no model call, no
provider call and no metered spend. That statement is about the designed
workflow, not about the authoring process.

The documents and fixtures were **agent-assisted authoring**: composed in a
DeepSeek Harness session (configured route `deepseek-flash`; the serving model is
not observable), not produced by a provider API call, credential or metered
spend recorded by this item. `$0` is the item-scoped measured spend and the
offline path's cost; it is not a claim that no language model was involved in
drafting the pages.

The twenty fixtures are **hand-authored fixture text**: written as synthetic
question/expected-observation records, not captured model transcripts. "Hand-
written" describes that authorship form, not the absence of tooling.

## 5. Non-claims

- No price, rate or provider term is asserted.
- The token bounds are design assumptions, not measurements.
- The ceiling is not a billing guarantee; it is a stop rule a future build must
  enforce.
- No live or paid run is authorised by this model.
