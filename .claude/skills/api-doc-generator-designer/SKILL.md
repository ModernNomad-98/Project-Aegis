---
name: api-doc-generator-designer
description: Design GENERATED API reference documentation — reference produced from the API's source of truth (OpenAPI/GraphQL schema, type annotations, docstrings) so it can't drift from the implementation, the split between what to auto-generate (the exhaustive reference) and what to hand-write (guides, examples, overviews), enriching the source of truth so descriptions/examples are single-sourced, the generation toolchain and where it slots into the docs pipeline, try-it/auth/error docs, and versioning the reference with the API. Documents an API that api-event-architect designed; keeps the reference honest by generating it, not hand-maintaining it. Use when generating API reference from a schema or code, keeping API docs in sync, or choosing an API-doc toolchain. Do NOT use to design the API CONTRACT itself (api-event-architect), the general docs pipeline (docs-as-code-architect), or organize docs by type (diataxis-doc-organizer).
---

# API Doc Generator Designer

## Purpose

Hand-maintained API reference is wrong the moment the API changes and
nobody edits the docs — a parameter gets renamed, the docs still show the
old name, and every integrator hits the wall. The fix is to stop
maintaining reference by hand: generate it from the API's source of truth
so it CAN'T drift. This skill designs that generation — what the source of
truth is (OpenAPI/GraphQL schema, type annotations, docstrings), how the
exhaustive reference is generated from it, the clean split between
generated reference and hand-written guides/examples, enriching the
schema so descriptions and examples are single-sourced, the toolchain and
its place in the docs pipeline, and versioning the reference with the API.
It documents an API that `api-event-architect` designed; its whole point
is a reference that stays honest because it's generated, not typed.

## Use When

- Use when: generating API reference from an OpenAPI/GraphQL schema, type
  annotations, or docstrings.
- Use when: API docs keep drifting from the implementation and you need
  them generated and in-sync.
- Use when: choosing an API-doc toolchain, or deciding what to auto-
  generate vs hand-write.
- Use when: designing try-it consoles, auth docs, or a generated error
  catalog for an API reference.
- Do NOT use when: the task is designing the API CONTRACT itself — routes,
  versioning policy, envelopes, rate limits, webhooks — that is
  `api-event-architect`; this skill DOCUMENTS that contract, it doesn't
  define it.
- Do NOT use when: the task is the general docs pipeline (generator,
  build, CI, deploy for all docs) — that is `docs-as-code-architect`; API
  reference generation is a slice that plugs into it.
- Do NOT use when: the task is organizing the whole docs corpus by mode —
  that is `diataxis-doc-organizer` (reference is one mode; this generates
  it).

## Inputs to Inspect

1. The API's source of truth: is there an OpenAPI/GraphQL schema, typed
   handlers, or docstrings the reference can generate from — and how
   complete/accurate is it?
2. The API contract (from `api-event-architect` outputs where present):
   routes, versioning/deprecation policy, error envelope, auth model —
   the reference documents these, it doesn't redefine them.
3. The current API docs: hand-written or generated, how stale, and where
   they drift from the implementation.
4. The docs pipeline (from `docs-as-code-architect` where present): how
   generated reference will build, publish, and version alongside the rest
   of the docs.
5. The consumers: who reads the reference (external integrators, internal
   teams) and whether they need try-it consoles, SDK docs, or multiple
   language examples.

## Workflow

1. **Establish the source of truth.** Reference generates FROM a machine-
   readable definition — an OpenAPI/GraphQL schema, typed signatures, or
   structured docstrings. If none exists, creating/adopting one is the
   real first task; generating from nothing isn't possible.
2. **Generate the exhaustive reference.** Endpoints/operations, types,
   parameters (required/optional, formats), responses, and the error
   catalog — all generated so they match the implementation by
   construction. This is the drift-killer: generated reference can't fall
   behind because it IS the schema, rendered.
3. **Split generated vs authored.** Generate the reference (the complete
   machinery). Hand-write the quickstart, guides/how-tos, conceptual
   overviews, and curated examples — generation produces those badly. Map
   to Diátaxis: reference = generated; tutorials/how-to/explanation =
   authored (`diataxis-doc-organizer` places them).
4. **Enrich the source of truth, not the output.** Descriptions,
   examples, and metadata live IN the schema/docstrings so they're
   single-sourced and regenerate automatically. Editing the generated
   output directly re-creates the drift problem — push enrichments
   upstream.
5. **Design examples, auth, and errors.** Request/response examples
   (ideally validated against the schema so they can't lie), the
   authentication/authorization docs, and the error catalog generated from
   the error model (`error-taxonomy-designer`'s codes) rather than
   hand-listed.
6. **Choose the toolchain and slot it in.** The generator (OpenAPI→docs,
   GraphQL doc gen, TypeDoc/Sphinx/etc.), optional try-it/interactive
   console, and how it builds and publishes within the docs pipeline
   (`docs-as-code-architect`).
7. **Version the reference with the API.** The reference for version X
   matches version X; deprecations flow from the schema into the docs; a
   changelog/diff between versions is generated where possible. Coordinate
   the versioning/deprecation POLICY with `api-event-architect`.
8. **Deliver** the generation design in the Output Format, with the
   source of truth, the generated/authored split, and the sync guarantee
   explicit.

Source-of-truth options, the generated-vs-authored split table, schema-
enrichment patterns, and example-validation techniques:
[references/api-doc-sheet.md](references/api-doc-sheet.md).

## Output Format

```
API-DOC GENERATION DESIGN — <API>
Source of truth: <OpenAPI | GraphQL schema | typed handlers | docstrings> — completeness noted
Generated:      endpoints/operations, types, params, responses, error catalog — from SoT
Authored:       quickstart, guides/how-to, overviews, curated examples (→ diataxis-doc-organizer)
Enrichment:     descriptions/examples live IN the schema/docstrings (single-sourced)
Examples:       request/response validated against schema; auth docs; error catalog from taxonomy
Toolchain:      generator=<...>; try-it console?; plugs into docs pipeline (docs-as-code-architect)
Versioning:     reference matches API version; deprecations from schema; diff/changelog
Sync guarantee: reference generated, never hand-maintained → cannot drift
Boundaries:     contract → api-event-architect; pipeline → docs-as-code-architect;
                corpus org → diataxis-doc-organizer
```

## Validation Checklist

- [ ] The reference generates from a machine-readable source of truth; if
      none exists, adopting one is named as the first task.
- [ ] The exhaustive reference (endpoints/types/params/responses/errors)
      is generated, not hand-written.
- [ ] The generated-vs-authored split is explicit (reference generated;
      guides/examples authored).
- [ ] Enrichments (descriptions/examples) live in the source of truth and
      regenerate — not edited into the output.
- [ ] Examples are validated against the schema; auth and the error
      catalog are documented (errors from the taxonomy).
- [ ] The toolchain is chosen and slots into the docs pipeline.
- [ ] The reference is versioned with the API; deprecations flow from the
      schema.
- [ ] Contract, pipeline, and corpus-organization concerns are handed to
      their owning skills.

## Gotchas

- Hand-maintained reference is drift waiting to happen: the code changes
  in one PR, the docs in another (or never), and integrators get burned by
  a renamed field. Generate reference or accept that it will be wrong.
- Editing the GENERATED output to fix a description re-creates the exact
  problem — next regen wipes it. Enrichments belong upstream in the schema/
  docstrings so they survive regeneration and stay single-sourced.
- Generation is great for reference and terrible for teaching: an
  auto-generated "guide" is a wall of endpoints with no path through.
  Generate the machinery; hand-write the narrative.
- Examples that aren't validated against the schema lie as easily as
  hand-written docs — a stale example is a broken example. Validate them
  against the source of truth.
- "No schema, just generate from the code comments" often means the
  comments ARE the missing source of truth and are themselves incomplete;
  adopting a real schema is frequently the actual work.
- The reference documents the contract; it doesn't define it. Deciding
  routes, versioning policy, or rate limits inside the doc generator is
  `api-event-architect`'s job leaking into the wrong place.

## Stop Conditions

- The task is designing the API CONTRACT — routes, versioning/deprecation
  policy, envelopes, rate limits, webhooks → route to `api-event-architect`;
  this skill documents that contract.
- The task is the general docs pipeline or organizing the whole corpus →
  route to `docs-as-code-architect` or `diataxis-doc-organizer`.
- No machine-readable source of truth exists and the API is large/
  unstable → flag that adopting a schema is the prerequisite; generating
  accurate reference from nothing isn't possible, and hand-writing it just
  restarts the drift.
- The versioning/deprecation POLICY the reference must reflect is
  undefined → obtain it from `api-event-architect` rather than inventing a
  policy in the docs.

## Supporting Files

- [references/api-doc-sheet.md](references/api-doc-sheet.md) — source-of-
  truth options, the generated-vs-authored split table, schema-enrichment
  patterns, example-validation techniques, and versioning/deprecation
  surfacing.
- `evals/evals.json` — behavior cases including the drift-killing
  generation, the enrich-upstream discipline, and the no-schema
  prerequisite.
- `evals/trigger-evals.json` — discrimination against `api-event-architect`
  (contract vs its reference), `docs-as-code-architect`, and
  `diataxis-doc-organizer`.
