# Risk-Tiered Validation — Classifier Rules Artifact

Companion to `risk-tiered-validation-selector`. The rules live in the repo as
a diffable artifact (a rules table consumed by a script, or the script
itself); edits to the rules are themselves forced-full changes.

## Rule semantics

1. Rules are ORDERED, most-specific first. First match wins per file.
2. Two override lists run BEFORE the ordered rules:
   - **forced-full** — any hit ⇒ the whole change is `full`;
   - **never-docs-only** — any hit disqualifies `docs-only` for the whole
     change (the file itself then classifies by the ordered rules).
3. The last ordered rule is always the fail-closed catch-all:
   `** → full (unmatched — add a rule)`.
4. Aggregate tier = MAX over per-file classes (`docs-only < fast < full`).
5. Renames classify by BOTH old and new path; deletions classify like edits.
6. Classifier errors (no diff, unparseable rules, glob failure) ⇒ `full`.

## Starter rules table (calibrate per repo)

```
# overrides — forced-full (whole change)
**/migrations/**            # schema is never cheap
**/*.sql
**/auth/**  **/rls/**  **/policies/**
**/billing/**  **/payments/**
.github/workflows/**        # CI definitions
scripts/**                  # repo automation
package-lock.json  pnpm-lock.yaml  *.lockb   # dependency reality
CLAUDE.md  AGENTS.md  .cursor/**             # agent instruction files
validation-rules.*          # this artifact itself

# overrides — never-docs-only (disqualify docs-only; classify per rules)
(the same list as forced-full, plus:)
**/*.config.*  **/tsconfig*.json

# ordered rules
docs/**           → docs-only
**/*.md           → docs-only        # unless caught by overrides above
assets/** images  → docs-only
tests/**          → fast             # test-only changes: run the affected suites
src/**            → fast             # unless a forced-full path matched
**                → full             # fail-closed catch-all
```

Notes on contentious rows:

- **`**/*.md` docs-only**: safe ONLY because agent-instruction files are in
  the override lists — a rulebook .md steers behavior and is not
  documentation in the validation sense.
- **`scripts/**` forced-full**: repo automation runs with repo authority;
  treat as code with reach.
- **Lockfiles**: a lockfile-only diff means the dependency graph changed —
  that is never docs-only and deserves full (supply-chain surface).
- **Generated trees** (`**/*.g.*`, `gen/**`): classify explicitly by what
  consumes them (usually `fast` at minimum); never "skip, it's generated".

## Tier contents (name real checks)

| Tier | Runs (example bundle) |
| --- | --- |
| docs-only | link/reference check, docs build, any docs-scoped CI jobs |
| fast | typecheck, lint, build, unit tests scoped to affected packages |
| full | everything: fast + integration + e2e (via the shard runner where `sharded-validation-with-resume` is in place) + repo validators |

A tier bundle names commands/jobs that exist. If the "fast" bundle's scoping
mechanism doesn't exist yet (no affected-package mapping), fast = typecheck +
lint + build + FULL unit suite until it does — honest tiers over optimistic
ones.

## Worked classification

Change: `docs/upgrade-guide.md`, `README.md`, `.github/workflows/ci.yml`,
`src/lib/retry.ts`, `tools/gen/schema.g.ts` (no rule for `tools/gen/**` yet)

| file | match | class |
| --- | --- | --- |
| docs/upgrade-guide.md | `docs/**` | docs-only |
| README.md | `**/*.md` | docs-only |
| .github/workflows/ci.yml | forced-full override | full (forced) |
| src/lib/retry.ts | `src/**` | fast |
| tools/gen/schema.g.ts | catch-all (unmatched) | full (fail-closed) |

Aggregate: **FULL** — deciding files: the workflow file (forced) and the
unmatched generated file (fail-closed). Record instructs: add a
`tools/gen/**` rule via a reviewed rules-file change (which is itself
forced-full).

The same change through `change-classification-gate` would ALSO flag the
workflow file for its approval path — two verdicts, two authorities, shared
file list: the gate decides who must approve; the selector decides what must
run.

## Anti-patterns

- **Averaging** ("mostly docs, call it docs-only") — one workflow file in a
  40-file docs diff is a full change.
- **File-count heuristics** ("small diff, fast tier") — size is not risk.
- **Trusting the PR description** — the classifier's input is
  `git diff --name-only <base>...HEAD`, nothing else.
- **Silent rules growth** — rules added ad hoc in someone's head. The
  artifact is the classifier; if it isn't in the diff, it isn't a rule.
- **Exception culture** — "just this once, fast" is how fail-closed dies;
  the lawful exception is a reviewed rules change that survives the next
  diff too.
