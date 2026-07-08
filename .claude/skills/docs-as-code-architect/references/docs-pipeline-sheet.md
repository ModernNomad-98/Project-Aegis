# Docs Pipeline Sheet

Detail for `docs-as-code-architect`. Read on demand.

## Generator selection factors

Match the tool to requirements, not fashion. Key factors:

| Need | Favor a generator with… |
|---|---|
| Versioned docs | First-class version management + selector |
| API reference | Integration with OpenAPI/GraphQL/docstrings |
| i18n | Built-in translation workflow |
| Rich components | MDX / component support |
| Search | Built-in or easy hosted search |
| Low maintenance | Convention over config; stable ecosystem |
| Offline/PDF | Export support |

State the choice AND why it fits — the migration cost of a wrong pick is
paid later.

## CI checks catalog

| Check | Catches | Blocking? |
|---|---|---|
| Build | Broken syntax, missing includes | Yes (required gate) |
| Internal link check | Dead internal links, bad anchors | Yes |
| External link check | Dead outbound links | Sampled / scheduled (not hard-gate) |
| Prose/style lint | Style-guide violations, banned terms | Advisory → blocking as adopted |
| Spelling | Typos | Advisory/blocking |
| **Code-sample test** | Examples that no longer run | **Yes — highest value** |

Do NOT hard-gate merges on external link liveness — it couples you to
third-party uptime. Sample or run it on a schedule.

## Code-sample testing patterns

- **Doctest-style:** examples embedded in docs are executed in CI.
- **Snippet include:** docs include ranges from real, tested source
  files, so the example IS the tested code.
- **Compile/run harness:** extract fenced code blocks, compile/run them in
  CI against the current version.

Goal: a sample can't silently rot; if it breaks, CI does.

## Docs versioning patterns

- Docs for version X live/change with version X (branch or versioned dir).
- A version selector lets readers choose their release.
- Published docs match the shipped version — no "latest" shown to
  old-version users.
- Single-source version numbers/commands (variables/includes), never
  hardcoded across pages.

## URL stability

- Stable URLs; when a page moves, add a redirect.
- Broken external inbound links are a support cost you can avoid.
- Generated nav + stable slugs so deep links survive restructuring.

## Boundaries

- Content organization by mode → `diataxis-doc-organizer`.
- README content → `readme-craftsman`.
- API reference generation → `api-doc-generator-designer` (hosted by this
  pipeline).
- Contribution-guide CONTENT → `contribution-guide-author` (this skill
  designs the edit mechanics/infra).
