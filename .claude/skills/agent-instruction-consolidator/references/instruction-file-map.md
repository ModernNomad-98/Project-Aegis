# Agent Instruction File Map

Supporting detail for `agent-instruction-consolidator`. Locations, owning
tools, scope, and precedence semantics. Verify against current tool docs when
something looks off — tools change these conventions.

## Known instruction files

| File / location | Read by | Scope | Precedence notes |
| --- | --- | --- | --- |
| `CLAUDE.md` (repo root) | Claude Code | repo | Base project instructions. |
| `<dir>/CLAUDE.md` (nested) | Claude Code | directory | Loaded in addition to root when working under that dir; usually a deliberate override/supplement. |
| `CLAUDE.local.md` | Claude Code | repo, per-machine | Gitignored by convention; explains per-machine behavior differences. |
| `~/.claude/CLAUDE.md` | Claude Code | user (all repos) | Outside the repo; can contradict repo files invisibly. |
| `AGENTS.md` | Multiple tools (Codex-style agents; adoption varies) | repo | Some tools treat it as primary, others ignore it — verify per tool. |
| `.cursorrules` | Cursor (legacy) | repo | Deprecated in favor of `.cursor/rules/`; both may exist and disagree. |
| `.cursor/rules/*.mdc` | Cursor | repo or glob-scoped | Rules can be scoped to file patterns; scoped rules are intent, not drift. |
| `.github/copilot-instructions.md` | GitHub Copilot | repo | Single file, repo-wide. |
| `.github/instructions/*.instructions.md` | GitHub Copilot | glob-scoped | `applyTo` frontmatter scopes each file. |
| `.windsurfrules` | Windsurf | repo | Repo-wide. |
| `.clinerules` / `.clinerules/` | Cline | repo | File or directory form. |
| Repo-custom standards docs | Any (via pointers) | repo | E.g. an authoring standard that instruction files point at — part of the graph even though no tool loads it directly. |

## Consolidation guidance

- **Canonical-source choice:** prefer the file read by the tool the team
  actually uses most, or `AGENTS.md` when several tools honor it. Every other
  file becomes a thin pointer ("See <canonical>; tool-specific notes below")
  plus ONLY the rules that are genuinely tool-specific.
- **Pointers beat copies.** A copied rule is a future conflict. If a tool
  cannot follow pointers (reads only its own file), keep that file minimal and
  add a sync note naming the canonical source.
- **Scoped rules stay scoped.** Nested CLAUDE.md, `.cursor/rules` globs, and
  Copilot `applyTo` files encode intentional scope — consolidate their content
  only into equally-scoped locations, never "up" into repo-wide files.
- **User-level files are out of consolidation reach** (not in the repo) but in
  diagnostic scope: when behavior differs between machines, ask about
  `~/.claude/CLAUDE.md` and local variants.

## Rule normalization categories

When extracting rules for the matrix, bucket them as: build/test commands ·
code style · security/safety rules · workflow/process · tone/communication ·
tool permissions. Conflicts inside "build/test commands" and "security/safety"
are the ones that bite hardest — check those first.
