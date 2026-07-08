---
name: docs-as-code-architect
description: Design the docs-as-code TOOLCHAIN and pipeline — docs living in the repo beside the code, the format and static-site generator, the build/preview/deploy pipeline, versioning docs with the code they describe, review via pull requests, link-checking and prose/style linting in CI, testing that code samples actually run, search, and the docs contribution workflow. This is the ENGINEERING of documentation — the infrastructure that keeps docs building, published, and honest — not their content or organization. Use when setting up docs-as-code, choosing a docs generator/pipeline, wiring docs checks into CI, or versioning docs with releases. Do NOT use to organize docs by type/content (diataxis-doc-organizer), write the README (readme-craftsman), design generated API reference specifically (api-doc-generator-designer), or author the contribution guide's content (contribution-guide-author).
---

# Docs-as-Code Architect

## Purpose

Docs rot because they live outside the workflow that changes the code:
someone ships a feature, the wiki nobody owns stays wrong for a year, and
the "examples" haven't compiled since a major version ago. Docs-as-code
fixes this structurally — docs live in the repo, change in the same PR as
the code, and are gated by CI like anything else. This skill designs that
toolchain: where docs live and in what format, the generator and build/
preview/deploy pipeline, versioning docs with the releases they describe,
PR-based review, CI that checks links, prose, and buildability, and
testing that code samples actually run. It's the ENGINEERING of docs —
the machinery that keeps them building, published, and honest. It does not
organize the content (that's `diataxis-doc-organizer`) or write it.

## Use When

- Use when: setting up docs-as-code for a project, or choosing/replacing a
  docs generator and publishing pipeline.
- Use when: docs drift from the code and you need them in-repo, PR-
  reviewed, and CI-gated.
- Use when: wiring docs checks into CI — link-checking, prose/style
  linting, buildability, executable-sample testing.
- Use when: versioning docs with releases (a version selector; "docs match
  the shipped version").
- Do NOT use when: the task is organizing docs by type/content
  (tutorials/how-to/reference/explanation) — that is
  `diataxis-doc-organizer`; this skill builds the pipeline, not the
  taxonomy.
- Do NOT use when: the task is the README content — that is
  `readme-craftsman`.
- Do NOT use when: the task is specifically GENERATING API reference from
  a schema/docstrings — that is `api-doc-generator-designer` (a slice this
  pipeline hosts).
- Do NOT use when: the task is authoring the contribution guide's CONTENT
  — that is `contribution-guide-author`; this skill designs the docs
  contribution WORKFLOW/infra.

## Inputs to Inspect

1. The current docs setup: where docs live (repo, wiki, separate site),
   the format, how they're built and published, and how stale they are.
2. The stack and team: languages/frameworks (which influence generator
   choice and sample-testing), team size, and who will maintain docs.
3. Requirements: versioning needs, i18n, API reference, search, offline/
   PDF, and any hosting/CDN constraints.
4. The release process: how and when the code ships, so docs versioning
   aligns with it (from `merge-is-deploy-governance` / release skills
   where relevant).
5. Existing CI: the pipeline docs checks will plug into, and whether docs
   builds can be a required gate.

## Workflow

1. **Locate docs in the repo and choose the format.** Docs live beside the
   code they describe so they change in the same PR — the core docs-as-
   code move. Pick a format (Markdown/MDX, reStructuredText, AsciiDoc) and
   a static-site generator matched to needs (versioning, API docs, search,
   i18n), not fashion. State why.
2. **Design the build/preview/deploy pipeline.** Local preview for
   authors; per-PR preview builds so reviewers see rendered changes;
   deploy on merge; and a rollback path. The pipeline is boring on
   purpose — reliable and fast.
3. **Make docs review like code.** Docs change via PR, reviewed by a docs
   owner (CODEOWNERS for docs paths). This is what couples docs to code
   changes and gives them the same rigor.
4. **Wire CI checks.** Buildability (broken docs fail the build), internal
   and (sampled) external link-checking, broken-anchor detection, prose/
   style linting (a vale-style rule set), and spelling. Decide which are
   blocking vs advisory and where docs are a required check.
5. **Test the code samples.** Examples that don't run are the most
   damaging docs. Design executable-sample testing (doctest-style, or
   snippets included from tested source files) so examples can't silently
   rot. This is the highest-value check.
6. **Version docs with the code.** Docs for a version live/change with
   that version; a version selector lets readers pick their release; the
   published docs match what's shipped. Single-source version numbers and
   commands rather than hardcoding them across pages.
7. **Provide search and navigation infra.** Client-side or hosted search,
   generated nav, and stable URLs (redirects on moves so links don't rot).
8. **Define the docs contribution workflow.** How outside/inside
   contributors edit docs (edit-on-this-page, preview, checks) — the
   MECHANICS; the human-facing guide content is `contribution-guide-author`'s.
9. **Deliver** the pipeline design in the Output Format, with the CI gate
   and sample-testing explicitly specified.

Generator selection factors, the CI-checks catalog (link/prose/build/
sample), and the docs-versioning patterns:
[references/docs-pipeline-sheet.md](references/docs-pipeline-sheet.md).

## Output Format

```
DOCS-AS-CODE PIPELINE — <project>
Location/format: in-repo path; <Markdown/MDX/rST/AsciiDoc>; generator=<...> — why
Pipeline:       local preview; per-PR preview build; deploy-on-merge; rollback
Review:         docs via PR; CODEOWNERS for docs paths
CI checks:      build gate; link-check (internal + sampled external); prose/style lint;
                anchors; spelling — blocking vs advisory noted
Sample testing: executable examples (doctest/snippet-include) so samples can't rot
Versioning:     docs-with-release; version selector; single-sourced versions/commands
Search/nav:     <search>; generated nav; stable URLs + redirects on moves
Contribution:   edit workflow/mechanics (guide CONTENT → contribution-guide-author)
Boundaries:     content org → diataxis-doc-organizer; README → readme-craftsman;
                API reference generation → api-doc-generator-designer
```

## Validation Checklist

- [ ] Docs live in the repo and change via PR alongside code, with a docs
      CODEOWNER.
- [ ] A generator/format is chosen for stated reasons (versioning/API/
      search/i18n), not fashion.
- [ ] Per-PR preview builds exist; deploy-on-merge and rollback are
      defined.
- [ ] CI checks cover buildability, link-checking, prose/style, and
      spelling, with blocking vs advisory decided.
- [ ] Code samples are tested (executable or snippet-included) so they
      can't silently rot.
- [ ] Docs are versioned with releases; a version selector exists; version
      values are single-sourced.
- [ ] Search, generated navigation, and stable URLs with redirects are
      provided.
- [ ] Content organization, README, API-reference generation, and
      contribution-guide CONTENT are handed to their owning skills.

## Gotchas

- Docs that live outside the code's PR flow are docs that rot — the whole
  point of docs-as-code is that a feature change and its docs change land
  together and are reviewed together. If docs can be updated without
  touching the code repo, they won't be.
- Untested code samples are the most harmful documentation: a reader
  copies an example that no longer compiles and blames themselves.
  Executable-sample testing is the highest-leverage check, not an optional
  extra.
- A docs build that isn't a required check will break silently; someone
  merges a broken link or a failed build and nobody notices until a user
  hits it. Gate it.
- Hardcoding version numbers and commands across dozens of pages
  guarantees drift; single-source them (variables/includes) or they'll
  contradict each other by the next release.
- Moving a page without a redirect breaks every external link to it. URL
  stability is part of the pipeline, not an afterthought.
- Choosing a generator for novelty over fit (no versioning support when
  you need versioned docs, no API-doc integration when you need it) is a
  migration you'll pay for later. Match the tool to the requirements.
- Building the pipeline is not organizing the content. A perfect toolchain
  publishing a mode-mixed mess is still a mess — that's
  `diataxis-doc-organizer`'s job.

## Stop Conditions

- The task is organizing docs by type/content, or writing the README →
  route to `diataxis-doc-organizer` or `readme-craftsman`.
- The task is specifically generating API reference from a schema/
  docstrings → route to `api-doc-generator-designer` (this pipeline hosts
  it, but its design is that skill's).
- The task is the human-facing contribution guide CONTENT → route to
  `contribution-guide-author`; this skill designs the contribution
  mechanics/infra.
- Making docs a required CI gate would block merges on flaky external
  link-checks → design the check to sample/soft-fail external links rather
  than gate on third-party uptime; flag the tradeoff.

## Supporting Files

- [references/docs-pipeline-sheet.md](references/docs-pipeline-sheet.md) —
  generator selection factors, the CI-checks catalog (link/prose/build/
  sample), docs-versioning patterns, and URL-stability/redirect
  conventions.
- `evals/evals.json` — behavior cases including the in-repo/PR/CI setup,
  the executable-sample testing, and the required-gate flaky-external-link
  tradeoff.
- `evals/trigger-evals.json` — discrimination against `diataxis-doc-organizer`
  (org vs pipeline), `api-doc-generator-designer`, and
  `contribution-guide-author`.
