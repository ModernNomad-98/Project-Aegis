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
text is produced.

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

## 4. Cost of the design itself

Authoring this profile cost $0: no model call, no provider call, no spend. The
twenty fixtures are hand-written text, not generated transcripts.

## 5. Non-claims

- No price, rate or provider term is asserted.
- The token bounds are design assumptions, not measurements.
- The ceiling is not a billing guarantee; it is a stop rule a future build must
  enforce.
- No live or paid run is authorised by this model.
