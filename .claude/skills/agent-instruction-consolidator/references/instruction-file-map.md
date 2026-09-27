# Agent Instruction File Map

Supporting detail for the owning [Agent Instruction Consolidator](../SKILL.md).
Locations, owning tools, scope, and precedence semantics are examples to
verify against current tool documentation before changing instructions;
tool conventions change. `AGENTS.md` is a repository instruction file used
by some coding agents; `applyTo` is Copilot's file-pattern scope field;
`.mdc` is a Cursor rule-file format. `cwd` means the current working directory.

## Known instruction files

| File / location | Read by | Scope | Precedence notes |
| --- | --- | --- | --- |
| `CLAUDE.md` or `.claude/CLAUDE.md` (repo root) | Claude Code | repo | Base project instructions. `@path/to/file` imports are expanded into context at launch; an import that resolves outside the working directory needs one-time approval (checked 2026-09-26 against [code.claude.com/docs/en/memory](https://code.claude.com/docs/en/memory)). |
| `<dir>/CLAUDE.md` (nested) | Claude Code | directory | Loaded in addition to root when working under that dir; usually a deliberate override/supplement. |
| `CLAUDE.local.md` | Claude Code | repo, per-machine | Gitignored by convention; explains per-machine behavior differences. |
| `~/.claude/CLAUDE.md` | Claude Code | user (all repos) | Outside the repo; can contradict repo files invisibly. |
| `AGENTS.md` | Multiple tools (Codex-style agents; adoption varies) | repo | Some tools treat it as primary, others ignore it — verify per tool. Per-tool behavior below. |
| `AGENTS.md` / `AGENTS.override.md` (root down to cwd) | Codex | repo, per directory | Codex walks from the project root (typically the Git root) down to the cwd and takes at most one file per directory: `AGENTS.override.md`, else `AGENTS.md`, else a `project_doc_fallback_filenames` name. Files concatenate root-first, so deeper files win; loading stops at `project_doc_max_bytes` (32 KiB default) (checked 2026-09-26 against [learn.chatgpt.com/docs/agent-configuration/agents-md](https://learn.chatgpt.com/docs/agent-configuration/agents-md)). |
| `~/.codex/AGENTS.md` / `AGENTS.override.md` | Codex | user (all repos) | In the Codex home (`~/.codex` or `CODEX_HOME`); the override is used first and only the first non-empty file counts (checked 2026-09-26 against [learn.chatgpt.com/docs/agent-configuration/agents-md](https://learn.chatgpt.com/docs/agent-configuration/agents-md)). Outside the repo, like `~/.claude/CLAUDE.md`. |
| `AGENTS.md` / `.claude/AGENTS.md` | Claude Code | repo | By default read directly only when no `CLAUDE.md`, `.claude/CLAUDE.md`, or `CLAUDE.local.md` exists in the cwd or above; if one exists, only the CLAUDE.md files load unless they `@AGENTS.md`-import it or the Project instructions setting is changed. Direct reading requires Claude Code v2.1.277 or later; on older versions or where support is unavailable, import it from `CLAUDE.md` (checked 2026-09-26 against [code.claude.com/docs/en/memory](https://code.claude.com/docs/en/memory)). |
| `AGENTS.md` (root and nested) | Cursor | repo, per directory | Plain-markdown alternative to `.cursor/rules`; nested files are more specific and take precedence over parent ones (checked 2026-09-26 against [cursor.com/docs/context/rules](https://cursor.com/docs/context/rules)). |
| `.cursorrules` | Cursor (legacy) | repo | Legacy; Cursor says it will be deprecated and recommends moving its content into a `.cursor/rules/` rule set to Always Apply. Both may exist and disagree (checked 2026-09-26 against [cursor.com/help/customization/rules](https://cursor.com/help/customization/rules)). |
| `.cursor/rules/*.mdc` | Cursor | repo or glob-scoped | Rules can be scoped to file patterns; scoped rules are intent, not drift. Rule files need the `.mdc` extension; a plain `.md` file in `.cursor/rules/` is ignored (checked 2026-09-27 against [cursor.com/docs/context/rules](https://cursor.com/docs/context/rules)). |
| `GEMINI.md`, `~/.gemini/GEMINI.md` | Gemini CLI | user, workspace + ancestors, or directory | Global file plus workspace/ancestor files, and just-in-time files found when tools touch a directory. Supports `@file.md` imports; `context.fileName` in `settings.json` can make it read `AGENTS.md` or other names instead of, or in addition to, `GEMINI.md` (checked 2026-09-26 against [geminicli.com/docs/cli/gemini-md](https://geminicli.com/docs/cli/gemini-md/)). |
| `.github/copilot-instructions.md` | GitHub Copilot | repo | Single file, repo-wide. |
| `.github/instructions/*.instructions.md` | GitHub Copilot | glob-scoped | `applyTo` frontmatter scopes each file. |
| `.devin/rules/*.md`; `.windsurf/rules/*.md`; `.windsurfrules` | Windsurf | repo | `.devin/rules/` is preferred and takes precedence; `.windsurf/rules/` is a backward-compatibility fallback and `.windsurfrules` the legacy single-file form. Windsurf also reads `AGENTS.md` in any workspace directory (checked 2026-09-27 against [docs.devin.ai/desktop/cascade/memories](https://docs.devin.ai/desktop/cascade/memories)). |
| `.clinerules` / `.clinerules/` | Cline | repo | File or directory form. |
| `.claude/skills/<name>/SKILL.md`, `~/.claude/skills/` | Claude Code | repo (cwd and parents up to repo root; nested dirs on demand) or user | Skill workflows, not always-loaded instructions, but part of the graph when they carry rules (checked 2026-09-26 against [code.claude.com/docs/en/skills](https://code.claude.com/docs/en/skills)). |
| `.agents/skills/<name>/SKILL.md`, `~/.agents/skills/` | Codex | repo (cwd, parents, repo root), user; also `/etc/codex/skills` (admin) and bundled system skills | Codex's skill locations; it does not list `.claude/skills` (checked 2026-09-26 against [learn.chatgpt.com/docs/build-skills](https://learn.chatgpt.com/docs/build-skills)). |
| `<skill>/agents/openai.yaml` | Codex | per skill | Optional metadata; `policy.allow_implicit_invocation: false` stops automatic invocation (explicit `$skill` still works); the default is `true` (checked 2026-09-26 against [learn.chatgpt.com/docs/build-skills](https://learn.chatgpt.com/docs/build-skills)). |
| `.cursor/skills/`, `.agents/skills/` (+ `~/` forms); compat `.claude/skills/`, `.codex/skills/` (+ `~/` forms) | Cursor | repo (including nested subdirectories) or user | Cursor also loads the Claude and Codex skill directories for compatibility, so one skill directory can be discovered by several tools — check for duplicates (checked 2026-09-26 against [cursor.com/docs/context/skills](https://cursor.com/docs/context/skills)). |
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
