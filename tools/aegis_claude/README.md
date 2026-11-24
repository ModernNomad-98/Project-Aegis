# Aegis Claude adapter v1

The Aegis Claude adapter installs two repository-local Claude Code hooks that
call [Aegis Guard](../aegis_guard/README.md) before a tool runs. It is a
standard-library Python package.

**Status: L2 tool gate only. The L1 session gate is UNRUN and not achieved
on Claude Code 2.1.311.** On that host, a <code>SessionStart</code> hook exiting
<code>2</code> did not block the session; the session continued without
<code>.aegis/project.json</code>. Only the <code>PreToolUse</code> L2 tool gate
is effective. Do not claim <code>SessionStart</code> enforcement.

This is L2 only: a local policy check, not an operating-system sandbox and not
containment. The adapter makes no network call, installs no plugin or
extension, and edits only the repository-local
<code>.claude/settings.json</code> named by <code>--repo</code>. It never reads
or writes a user-level or global Claude Code settings file.

## Status matrix

| Surface | L2 tool gate (<code>PreToolUse</code>) | L1 session gate (<code>SessionStart</code>) |
| --- | --- | --- |
| Claude CLI 2.1.311 | L2 (tool gate) | UNRUN (not achieved: exit 2 did not block) |
| Claude VS Code extension | unqualified | unqualified |

<code>L2</code> is the per-tool policy gate. <code>L1</code> is the session
gate that would block a session before any tool runs. The observed 2.1.311
session continued after the <code>SessionStart</code> hook exited
<code>2</code>, so L1 is UNRUN. The VS Code extension is unqualified in both
layers: it is not covered by this adapter and has no interception evidence.

## Commands

Run from the Aegis checkout root, or put the checkout on
<code>PYTHONPATH</code>:

~~~bash
python -m tools.aegis_claude install --repo R --aegis-path A --policy P [--force]
python -m tools.aegis_claude uninstall --repo R
python -m tools.aegis_claude doctor --repo R
python -m tools.aegis_claude --version
~~~

- <code>R</code> is the repository to protect. It must already exist.
- <code>A</code> is an Aegis checkout containing
  <code>tools/aegis_guard/__main__.py</code>. It must be outside <code>R</code>.
  <code>install</code> rejects an Aegis checkout inside the repository, using
  resolved and case-folded path comparison.
- <code>P</code> is the policy path. <code>install</code> creates a default
  policy there when the file is absent; an existing policy is never rewritten.
- <code>--force</code> replaces an existing Aegis Claude hook with the freshly
  rendered command. It never removes or rewrites a foreign hook.

<code>install</code>, <code>uninstall</code> and <code>doctor</code> exit
<code>0</code> on success, <code>1</code> on a validation or filesystem
failure, and <code>2</code> on a command-line usage error.
<code>doctor</code> exits <code>0</code> only when it finds no
<code>FAIL</code> line.

## Default policy

When <code>P</code> is absent, <code>install</code> writes this
<code>aegis.policy/1</code> object:

~~~json
{
  "schema": "aegis.policy/1",
  "allowed_tools": ["Read", "Write", "Edit"],
  "denied_tools": ["WebFetch", "WebSearch", "Task"],
  "allowed_roots": ["."],
  "denied_paths": [
    "**/.aegis/**",
    "**/.claude/settings.json",
    "**/.claude/settings.local.json",
    "**/.git/**",
    "**/.env*",
    "**/.envrc*",
    "**/.ssh/**",
    "**/.aws/**",
    "**/.gnupg/**",
    "**/.git-credentials",
    "**/id_rsa*",
    "**/*.pem",
    "**/*.key",
    "**/secrets/**",
    "**/credentials*"
  ],
  "deny_outside_repo": true,
  "network_commands": [],
  "required_session_files": [".aegis/project.json"],
  "bash_allowlist": []
}
~~~

The default L2 profile allows file read, write and edit inside the repository
and nothing else. <code>Grep</code>, <code>Glob</code> and <code>Bash</code>
are absent from <code>allowed_tools</code>, so the adapter provides no search
or command execution. Builds and other side-effecting runs require an external
OS or container sandbox. The guard's built-in secret and network rules still
apply in addition to this policy. The policy format is documented in
[Aegis Guard](../aegis_guard/README.md) and its
[JSON Schema](../aegis_guard/policy.schema.json).

The first four denied patterns protect the adapter's own control surface:
<code>**/.aegis/**</code>, <code>**/.claude/settings.json</code>,
<code>**/.claude/settings.local.json</code> and <code>**/.git/**</code>. They
deny every tool path through Aegis Guard, including Read, Write and Edit, so a
tool call cannot rewrite the policy, the hooks, the session marker or Git
metadata to disarm itself. Independently of these patterns, Aegis Guard always
denies a Read, Write or Edit whose resolved path is exactly the loaded
<code>--policy</code> file, compared case-insensitively, or whose file identity
(<code>st_dev</code>, <code>st_ino</code>) matches it, which also denies a hard
link to the policy at another path, wherever that file lives. The SessionStart hook reads the marker and policy directly and does not
pass them through this path check. A user who needs to change the policy or
settings must edit the files outside the guarded tool call, with their own
authority.

## What install writes

<code>install</code> merges two entries into
<code>R/.claude/settings.json</code>:

~~~json
{
  "hooks": {
    "SessionStart": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "PYTHONPATH=A python -P -m tools.aegis_claude.hook --repo R --policy P"
          }
        ]
      }
    ],
    "PreToolUse": [
      {
        "matcher": ".*",
        "hooks": [
          {
            "type": "command",
            "command": "PYTHONPATH=A python -P -m tools.aegis_claude.hook --repo R --policy P"
          }
        ]
      }
    ]
  }
}
~~~

All other top-level keys, hook events, groups and commands are preserved. A
path containing whitespace is enclosed in double quotes in the generated
command. The command is otherwise the documented
<code>PYTHONPATH=&lt;A&gt; python -P -m tools.aegis_claude.hook --repo &lt;R&gt; --policy &lt;P&gt;</code>
shape.

Installation is idempotent: a second identical install makes no write and
creates no additional backup. With <code>--force</code>, only commands
containing <code>tools.aegis_claude.hook</code> are replaced; foreign hooks and
their ordering are left in place.

When an existing settings file must change, its exact previous bytes are
copied to:

~~~text
R/.aegis/backup/claude-settings.json.<UTC timestamp>
~~~

The backup is written before the merge. A failure to create it aborts the
settings write. Backups are deliberately retained after
<code>uninstall</code> so an operator can inspect or restore them manually;
<code>uninstall</code> does not overwrite current settings with a backup.

## Hook behavior

The hook reads one JSON object from standard input. Malformed input, an
unsupported event, a missing <code>tool_name</code>, or a
<code>tool_input</code> that is not a JSON object exits <code>2</code>.

### SessionStart

The hook requires <code>R/.aegis/project.json</code> and <code>P</code> to
exist and be readable. A missing or unreadable file prints a reason to standard
error and exits <code>2</code>. Otherwise it exits <code>0</code> and writes
nothing to standard output.

**This hook is advisory on Claude Code 2.1.311.** A hook exit of <code>2</code>
did not stop that host from starting the session; the session continued without
<code>.aegis/project.json</code>. The adapter does not claim an L1 session
gate. Do not rely on <code>SessionStart</code> to prevent a tool call; the
<code>PreToolUse</code> L2 gate is the effective layer.

Cursor Agent sends the same hook events with camelCase names. The adapter
accepts <code>preToolUse</code> as an alias for <code>PreToolUse</code> and
<code>sessionStart</code> for <code>SessionStart</code>, so a Cursor-invoked
hook reaches the same policy check rather than being rejected as an
unsupported event. Cursor can omit <code>cwd</code> or may send an empty
string; in both cases the hook defaults to the repository root. A non-string,
non-null <code>cwd</code> (number, boolean, array or object) exits 2;
<code>null</code> is treated like an omitted <code>cwd</code>. The default is
the repository root, not the host's working directory; see the limits below.

Gemini CLI's <code>gemini hooks migrate --from-claude</code> emits a
<code>BeforeTool</code> event and Gemini-specific tool names. The adapter maps
<code>BeforeTool</code> to <code>PreToolUse</code> and maps
<code>run_shell_command</code>, <code>read_file</code>, <code>write_file</code>,
<code>replace</code>, <code>glob</code>, <code>search_file_content</code>,
<code>web_fetch</code> and <code>google_web_search</code> to the canonical Aegis
tool names before policy evaluation.

### PreToolUse

The hook runs:

~~~text
python -P -m tools.aegis_guard check --policy P --repo R --tool tool_name \
  --args-json <tool_input as JSON> --cwd <event cwd>
~~~

with <code>PYTHONPATH=A</code>. It maps:

| Aegis Guard exit | Hook exit | Meaning |
| --- | --- | --- |
| <code>0</code> | <code>0</code> | Allow the tool call. |
| <code>10</code> | <code>2</code> | Deny. A reason is printed to standard error. |
| <code>3</code> | <code>2</code> | Policy or environment error. A reason is printed to standard error. |
| <code>2</code> | <code>2</code> | Guard usage error. A reason is printed to standard error. |
| any other nonzero | <code>2</code> | Fail closed. |

Only hook exit <code>0</code> is an allow. The hook never turns a guard error
into an allow and never runs the proposed tool itself.

The default policy does not allow <code>Grep</code> or <code>Glob</code>. If a
custom policy enables them, both require an explicit, non-empty
<code>path</code>. A missing <code>path</code> is denied; the guard does not
substitute the repository root. A supplied path must be inside an allowed root
and must not match a denied pattern. The guard checks that path argument only;
it does not enumerate the files a recursive search would reach from a parent
directory. See the limits below.

## Uninstall

<code>uninstall --repo R</code> loads <code>R/.claude/settings.json</code> and
removes every hook command whose text contains
<code>tools.aegis_claude.hook</code>, in any hook event. It drops a group that
becomes empty, keeps every foreign hook and top-level key, and leaves
<code>.aegis/backup/</code> untouched. A missing settings file or a repository
with no Aegis Claude hooks is a successful no-op. Malformed settings are
refused without a write.

## Doctor

<code>doctor --repo R</code> writes nothing. It checks:

- the repository and <code>.claude/settings.json</code> exist and parse;
- a <code>SessionStart</code> and a <code>PreToolUse</code> Aegis Claude hook
  are present;
- the <code>PreToolUse</code> group has matcher <code>.*</code>;
- each command names <code>tools.aegis_claude.hook</code>, passes
  <code>-P</code>, sets <code>PYTHONPATH</code>, and carries
  <code>--repo</code> and <code>--policy</code>;
- the command's repository matches <code>R</code>;
- the named Aegis checkout still has <code>tools/aegis_guard/__main__.py</code>
  and <code>tools/aegis_claude/hook.py</code>;
- the policy exists, parses, has schema <code>aegis.policy/1</code>, and
  carries the expected fields.

Doctor always prints a warning that <code>SessionStart</code> is advisory and
may be ignored, names the observed Claude Code 2.1.311 behavior, and states
that L1 is UNRUN. A missing <code>.aegis/project.json</code> is also a warning;
it is not a doctor failure and it does not imply session enforcement.

## Tests

~~~bash
python -B -m unittest discover -s tools/aegis_claude/tests -v
~~~

The suite uses temporary repositories and temporary settings files. It covers
settings merge and foreign-hook preservation, idempotence, backups, forced
replacement, the default policy, uninstall, the read-only doctor, SessionStart
presence and absence, PreToolUse allow and deny cases, including Bash, curl,
outside-repository paths, <code>.env</code>, <code>WebFetch</code>, protected
<code>.aegis</code>/<code>.claude</code>/<code>.git</code> paths, non-default
policy paths, default Grep/Glob denial, the custom-policy Grep/Glob
explicit-path rule, and hard-link identity denial, malformed and
invalid-UTF-8 stdin, missing tool fields, omitted, null, empty, relative and
non-string, non-null payload <code>cwd</code> (null is accepted as omitted),
duplicate <code>cwd</code> keys, and no <code>__pycache__</code> residue. It
makes no network call.

## Limits

- **L2 only; L1 is UNRUN.** This adapter is a local policy check, not an OS
  sandbox, not process containment, and not an enforcement claim. On Claude
  Code 2.1.311, <code>SessionStart</code> exit <code>2</code> did not block the
  session. The adapter makes no L1 session-gate claim; only the
  <code>PreToolUse</code> L2 tool gate is effective. Use an external OS or
  container sandbox where containment is required.
- **SessionStart is host-dependent and advisory.** The hook returns the
  documented exit code, but a host may ignore it. The adapter's contract is the
  exit code; a host that ignores it is not constrained.
- **No global settings.** The adapter edits only
  <code>R/.claude/settings.json</code>. User-level and enterprise-managed
  settings are out of scope.
- **Claude VS Code extension not covered.** This adapter targets the
  repository-local CLI hook surface. No VS Code extension integration,
  interception test or containment evidence is provided.
- **Native Windows limits.** The generated command uses a POSIX
  <code>PYTHONPATH=...</code> prefix. A native host shell that does not support
  that assignment may fail to start the hook; verify the host's shell before
  relying on it. A live Claude Code 2.1.311 run on Windows blocked a
  <code>Write</code> to <code>.aegis/policy.json</code> and a Bash call through
  this hook; the test suite itself still invokes the hook module directly.
  A repository, policy or Aegis path containing a double quote,
  dollar sign, backtick, percent sign or newline is rejected at install time
  rather than embedded in a shell command.
- **An absent, null or empty <code>cwd</code> is assumed to be the repository
  root.** The hook has no other way to learn the host's working directory. A
  host that resolves relative tool paths from a different directory could
  therefore have a path checked under a different base than the one it actually
  uses. The guard's repository and allowed-root containment still applies, but
  the checked path may not be the touched path. In the Cursor 3.31.15 payload
  captured for HOSTED-2A, both the top-level <code>cwd</code> and the
  <code>cwd</code> inside <code>tool_input</code> were the empty string.
- **Only top-level tool arguments are inspected** by Aegis Guard. A custom
  tool with a path nested inside another argument object is outside its check.
  The default <code>Read</code>, <code>Write</code> and <code>Edit</code> tools
  carry their path in the top-level <code>file_path</code>, so this does not
  apply to the default profile.
- **Grep and Glob are outside the default profile.** If a custom policy
  enables them, the guard checks one explicit <code>path</code>, not recursive
  results. An explicit path that is the repository root or a parent of a denied
  directory can still let the search traverse denied descendants; the guard
  does not enumerate results, inspect <code>pattern</code> or
  <code>glob</code> content, or model symlink traversal inside an allowed
  directory. Supplying an explicit denied directory such as
  <code>secrets</code> is denied. This residual parent-path traversal is
  reported rather than addressed by a heuristic.
- **Other control files use path patterns, not file identity.** The policy
  file is protected by resolved path and <code>st_dev</code>/<code>st_ino</code>
  identity, so a hard link to the policy is denied. The
  <code>.claude/settings.json</code>, <code>.claude/settings.local.json</code>
  and <code>.git/**</code> patterns are path-based; a pre-existing hard link to
  one of those files at an unlisted path is a residual. The default Read, Write
  and Edit tools cannot create hard links.
- **Backups are not automatic rollback.** <code>uninstall</code> removes only
  the Aegis Claude hooks. It does not restore a <code>.aegis/backup/</code>
  snapshot.

See the [user-facing guide](../../docs/aegis-claude/README.md) for the pilot
scope and status.
