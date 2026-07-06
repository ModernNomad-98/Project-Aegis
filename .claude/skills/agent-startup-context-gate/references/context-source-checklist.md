# Context Source Checklist

Supporting detail for `agent-startup-context-gate`. Read on demand.

## Identity signals (need at least two independent ones)

| Signal | How to check | What confirms |
| --- | --- | --- |
| Git remote | `git remote -v` | URL matches the repo the task names (org + name). |
| README identity | first heading + purpose paragraph | Title/purpose matches the expected project. |
| Landmark layout | `ls` top level | Expected directories exist (`src/`, `docs/`, `.claude/`, …). |
| Manifest | `package.json` name, `pyproject.toml` name, `.sln` | Project name matches. |
| Recent history | `git log --oneline -5` | Commit subjects are plausibly this project's work. |

Two signals from the SAME row (e.g. two README lines) count as one. Path
existence and directory name count as zero signals — near-miss and empty
directories pass both.

## Reading precedence (stop at the depth the task needs)

1. Agent instruction files: root `CLAUDE.md`, nested `CLAUDE.md`, `AGENTS.md`,
   tool-specific instruction files.
2. Repo-designated canonical docs (reconciliation records, "single source of
   truth" docs, standards the instructions point to).
3. `README.md` — orientation and links, but its process claims can be stale.
4. Status docs: roadmap, catalog, changelog, open PRs.
5. Architecture/design docs relevant to the task area.
6. Tests covering the task area (they encode actual current behavior).
7. The specific files the task names.

## Per-repo-type additions

| Repo type | Also inspect |
| --- | --- |
| Library/package | public API surface, versioning/release config, CI matrix |
| Service/app | entry points, config/env handling, migration dir, deploy config |
| Monorepo | workspace layout, per-package instruction files, ownership map |
| Docs/skills repo | authoring standard, validator script, catalog integrity rules |

## Resume checklist (session was interrupted or compacted)

- Re-verify branch and working-tree state — do not trust remembered state.
- `git log` since the last verified point; someone (or you) may have committed.
- Re-read any doc the task treats as canonical if it could have changed.
- Restate the task's remaining scope before acting.
