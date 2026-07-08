# API Doc Sheet

Detail for `api-doc-generator-designer`. Read on demand.

## Source-of-truth options

| Source | Good for | Notes |
|---|---|---|
| OpenAPI/Swagger | REST APIs | Rich ecosystem; validate examples against it |
| GraphQL schema | GraphQL APIs | Introspection = built-in SoT |
| Protobuf/gRPC | RPC APIs | Generate from `.proto` |
| Typed signatures | SDK/library APIs | TypeDoc, Sphinx autodoc, etc. |
| Structured docstrings | Library APIs | Only as complete as the docstrings |

No machine-readable SoT → adopting one is the real first task. Generating
accurate reference from nothing isn't possible; hand-writing restarts the
drift.

## Generated vs authored split

| Content | Generated | Authored |
|---|---|---|
| Endpoints/operations | ✅ | |
| Types/schemas/params | ✅ | |
| Responses/status codes | ✅ | |
| Error catalog | ✅ (from taxonomy) | |
| Quickstart | | ✅ |
| How-to guides | | ✅ |
| Conceptual overview / "why" | | ✅ |
| Curated end-to-end examples | | ✅ (validated) |

Map to Diátaxis: **reference = generated**; tutorials/how-to/explanation =
authored and placed by `diataxis-doc-organizer`.

## Schema-enrichment patterns

Put the narrative IN the source of truth so it regenerates:
- OpenAPI: `description`, `example`, `examples`, `x-` extensions.
- GraphQL: schema descriptions on types/fields.
- Docstrings: structured params/returns/examples.

Never edit generated output directly — the next regen wipes it.

## Example validation

- Validate request/response examples against the schema in CI.
- Prefer examples derived from real, tested calls.
- A stale example is a broken example; make it fail the build (ties into
  `docs-as-code-architect`'s sample testing).

## Versioning & deprecation surfacing

- Reference for version X matches version X (version selector).
- Deprecations flow FROM the schema (`deprecated: true`) INTO the docs.
- Generate a diff/changelog between versions where the toolchain allows.
- The versioning/deprecation POLICY itself is `api-event-architect`'s;
  this skill surfaces it, doesn't set it.

## Auth & try-it

- Document the auth model clearly (how to get and send credentials).
- Try-it/interactive consoles help, but never against production without
  scoped test credentials.
