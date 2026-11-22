# Aegis Claude adapter

This page describes the repository-local Claude Code adapter for Aegis Guard.
It is a pilot at **L2 only**: a local policy check, not an operating-system
sandbox, not process containment, and not an enforcement claim.

**Observed host fact (Claude Code 2.1.311):** a <code>SessionStart</code> hook
exiting <code>2</code> did **not** block the session. The session continued
without <code>.aegis/project.json</code>. The L1 session gate is therefore
**UNRUN and not achieved**, and the adapter makes no
<code>SessionStart</code> enforcement claim. Only the <code>PreToolUse</code>
L2 tool gate is effective.

## Status matrix

| Surface | L2 tool gate (<code>PreToolUse</code>) | L1 session gate (<code>SessionStart</code>) |
| --- | --- | --- |
| Claude CLI 2.1.311 | L2 (tool gate) | UNRUN (not achieved: exit 2 did not block) |
| Claude VS Code extension | unqualified | unqualified |

<code>L2</code> is the per-tool policy gate. <code>L1</code> is the session gate
that would block a session before any tool runs. The observed 2.1.311 session
continued after the <code>SessionStart</code> hook exited <code>2</code>, so L1
is UNRUN. The VS Code extension is unqualified in both layers: it is not
covered by this adapter and has no interception evidence.

The adapter is implemented in
[<code>tools/aegis_claude</code>](../../tools/aegis_claude/README.md). It pairs
with [Aegis Guard](../aegis-enforcement/README.md), which makes the actual
allow-or-deny decision.

## Scope

The adapter installs exactly two repository-local hooks:

- **SessionStart** requires <code>.aegis/project.json</code> and the policy to
  be present and readable, and exits <code>2</code> when either is missing. It
  is advisory on Claude Code 2.1.311: the observed session continued after
  exit <code>2</code>. It is not an L1 session gate.
- **PreToolUse** asks Aegis Guard about one proposed tool call and maps the
  guard result to a hook exit code. This is the effective L2 tool gate.

The hooks live in the repository's own <code>.claude/settings.json</code>.
There is no global, user-level, plugin or extension installation, and the
adapter never reads or writes a global Claude Code settings file. The scope is
the single repository passed as <code>--repo</code>.

In the default profile, L2 means file <code>Read</code>, <code>Write</code> and
<code>Edit</code> inside that repository. There is no search tool, no shell
tool and no command execution. Builds and other side-effecting runs require an
external OS or container sandbox. Guard checks only the top-level path
argument these tools carry; these three tools have no nested path argument.

This change adds a reusable adapter and its tests. It does not install hooks
into this source checkout. It makes no L1 session-enforcement claim, and no
claim about a host that does not run the hooks or does not block on their exit
codes.

## Install, inspect, remove

~~~bash
python -m tools.aegis_claude install \
  --repo C:/work/app \
  --aegis-path C:/work/aegis \
  --policy C:/work/app/.aegis/policy.json
python -m tools.aegis_claude doctor --repo C:/work/app
python -m tools.aegis_claude uninstall --repo C:/work/app
~~~

<code>--aegis-path</code> must contain
<code>tools/aegis_guard/__main__.py</code> and must be outside the repository.
<code>install</code> rejects a checkout inside <code>--repo</code>, using
resolved and case-folded path comparison. <code>--policy</code> is created with
the documented default when absent; an existing policy is never rewritten. <code>--force</code> replaces only hook commands that contain
<code>tools.aegis_claude.hook</code>; all other hooks and settings keys are
preserved.

Before a changed settings file is written, its exact bytes are backed up to
<code>.aegis/backup/claude-settings.json.&lt;timestamp&gt;</code>. The backup is
written first; if it cannot be created, the settings write is aborted.
<code>uninstall</code> removes only the adapter's hooks and retains the
backups for manual inspection or restore.

The generated hook command has this shape:

~~~text
PYTHONPATH=<A> python -P -m tools.aegis_claude.hook --repo <R> --policy <P>
~~~

The <code>SessionStart</code> group has no matcher. The
<code>PreToolUse</code> group uses matcher <code>.*</code>.

## Default policy

The default policy name is <code>aegis.policy/1</code> and its allow-list is
<code>Read</code>, <code>Write</code> and <code>Edit</code> only.
<code>Grep</code>, <code>Glob</code>, <code>Bash</code>, <code>WebFetch</code>,
<code>WebSearch</code> and <code>Task</code> are denied. Paths are confined to the repository and to
<code>.</code>; the default denied patterns cover environment files, SSH, AWS
and GPG material, Git credentials, private keys, <code>secrets</code> and
<code>credentials</code> paths. <code>bash_allowlist</code> and
<code>network_commands</code> start empty, and
<code>.aegis/project.json</code> is the required session file.

The exact object is documented in the
[package README](../../tools/aegis_claude/README.md). Aegis Guard's built-in
secret and network rules apply in addition to the policy. The default profile
allows file read, write and edit inside the repository only: there is no search
tool and no command execution. Builds and other side-effecting runs require an
external OS or container sandbox.

The default policy also protects the adapter's control surface. These paths
are denied for every tool path, including Read, Write and Edit, so a tool call
cannot rewrite the policy, hooks, session marker or Git metadata to disarm
itself:

- <code>**/.aegis/**</code>
- <code>**/.claude/settings.json</code>
- <code>**/.claude/settings.local.json</code>
- <code>**/.git/**</code>

A user who needs to change these files must do so outside the guarded tool
call, with their own authority. Independently of these patterns, Aegis Guard
always denies a Read, Write or Edit whose resolved path is exactly the loaded
<code>--policy</code> file, compared case-insensitively, or whose file identity
(<code>st_dev</code>, <code>st_ino</code>) matches it, which also denies a hard
link to the policy at another path, wherever that file lives. The SessionStart hook reads the marker and policy directly and does not
pass them through the Guard path check.

## Hook contract

The hook reads one JSON object from standard input.

<code>SessionStart</code> exits <code>0</code> only when both
<code>R/.aegis/project.json</code> and the policy can be opened and read. A
missing or unreadable file exits <code>2</code> with a reason on standard
error. On Claude Code 2.1.311, that exit <code>2</code> did not stop the
session; see the L1 note below.

<code>PreToolUse</code> runs:

~~~text
python -P -m tools.aegis_guard check --policy P --repo R \
  --tool <tool_name> --args-json <tool_input JSON> --cwd <event cwd>
~~~

with <code>PYTHONPATH=A</code>. Exit <code>0</code> allows. Exit
<code>10</code> (deny), <code>3</code> (policy or environment error) and
<code>2</code> (guard usage error) become hook exit <code>2</code>; the reason
is printed to standard error. Every other nonzero guard result also fails
closed. The hook does not execute the proposed tool, does not use a shell, and
makes no network call.

The default policy does not allow <code>Grep</code> or <code>Glob</code>. If a
custom policy enables them, both require an explicit, non-empty
<code>path</code>. A missing path is denied; no repository-root default is
applied. The path must be inside an allowed root and must not match a denied
pattern. Only that path argument is checked: a search rooted at a parent
directory can still traverse denied descendants, because the guard does not
enumerate results or inspect <code>pattern</code>/<code>glob</code> content.
This residual limitation is reported, not covered by a heuristic.

## SessionStart (L1) is UNRUN

The adapter's <code>SessionStart</code> contract is only the process exit code.
It is not an L1 session gate. In Claude Code 2.1.311, a
<code>SessionStart</code> hook exiting <code>2</code> did not block the
session; the session started and continued without
<code>.aegis/project.json</code>. The L1 result is therefore **UNRUN and not
achieved**. Do not describe <code>SessionStart</code> as enforcing a session
precondition, and do not rely on it to stop a tool call.

The effective layer is the <code>PreToolUse</code> L2 tool gate. Even there the
hook is a policy request to the host, not containment: the host must actually
block the tool call on hook exit <code>2</code>. The tests here exercise the
hook module directly; the 2.1.311 observation is host evidence recorded from
that host, not a result reproduced by the test suite.

## Not covered

- **Claude VS Code extension.** This adapter targets the repository-local
  Claude Code CLI hook surface. No VS Code extension integration, interception
  test or containment evidence is provided.
- **Global settings and enterprise policy.** The adapter edits only the named
  repository's <code>.claude/settings.json</code>. User-level settings and
  managed enterprise configuration are outside its scope.
- **External sandboxing.** There is no OS sandbox or container here. Where
  containment is required, run the host inside an external sandbox and treat
  this adapter as one additional local check. It is L2 only.
- **Live-host evidence.** The test suite invokes the hook module and Aegis
  Guard as subprocesses against temporary repositories. It is not evidence
  that every installed Claude Code build executes repository hooks or honours
  their exit codes. On Claude Code 2.1.311 for Windows, a live disposable-repo
  run blocked a <code>Write</code> to <code>.aegis/policy.json</code> with
  <code>path denied by pattern '**/.aegis/**'</code> and blocked Bash with
  <code>tool 'Bash' is not in allowed_tools</code>; neither target file was
  created. The same host recorded the L1 result: <code>SessionStart</code>
  exit <code>2</code> did not block. These are 2.1.311 observations, not a
  claim about other versions or the VS Code extension.

## Native Windows

The generated hook command uses a POSIX-style
<code>PYTHONPATH=...</code> environment assignment. A native host shell that
does not support that syntax may fail to start the hook, and a shell that does
not understand the quoting may fail on paths containing spaces. The generated
command double-quotes paths with whitespace. The adapter was exercised on
Windows with Claude Code 2.1.311 for the protected-path and Bash cases; other
native shells and Claude Code versions remain unverified. Verify the actual
host shell and command invocation before relying on the hook. Python and the
command line are otherwise ordinary Windows paths. Install rejects a path containing a double quote, dollar sign,
backtick, percent sign or newline instead of writing an ambiguous shell
command.

## Doctor and evidence

<code>doctor --repo R</code> is read-only. It verifies the settings file, both
hook events, the <code>PreToolUse</code> matcher, the command's
<code>--repo</code> and <code>--policy</code>, the policy schema and fields,
and the presence of the guard and hook modules in the named Aegis checkout.
Doctor always warns that <code>SessionStart</code> is advisory and may be
ignored; it names the observed Claude Code 2.1.311 behavior and states that L1
is UNRUN. A missing <code>.aegis/project.json</code> is also a warning; it is
not a doctor failure and does not imply session enforcement.

The adapter's test suite covers install merge, foreign-hook preservation,
idempotence, backups, forced replacement, uninstall, the default policy,
read-only doctor behavior, <code>SessionStart</code> presence and absence,
<code>PreToolUse</code> allow and deny paths, protected
<code>.aegis</code>/<code>.claude</code>/<code>.git</code> path denial,
Read/Write/Edit of a non-default policy path, a hard link to the policy
path, default Grep/Glob denial, custom-policy Grep/Glob explicit-path rules,
vendored-checkout rejection, malformed and invalid-UTF-8 stdin, and no
<code>__pycache__</code> residue.

~~~bash
python -B -m unittest discover -s tools/aegis_claude/tests -v
python -m json.tool tools/aegis_guard/policy.schema.json
python scripts/validate-skills.py
python scripts/ci/check-markdown-links.py \
  tools/aegis_claude/README.md docs/aegis-claude/README.md
~~~

## Limits

- **L1 is not achieved.** <code>SessionStart</code> is advisory on Claude Code
  2.1.311: exit <code>2</code> did not block the session. Only the L2
  <code>PreToolUse</code> tool gate is effective, and only when the host blocks
  on it.
- The policy is a lexical local check. It cannot prove that a tool call is
  safe, detect secrets inside file contents, intercept a process already
  running, or replace an OS sandbox.
- Bash is not available in the default adapter profile. If a custom policy
  enables it, an allow-listed command binds command text, not executable
  identity, and an allow-listed program can still run arbitrary code. Builds
  require external containment.
- The hook checks only top-level argument keys. A path nested inside another
  object is not path-checked by this version. The default Read, Write and Edit
  tools carry their path in top-level <code>file_path</code>, so this does not
  apply to the default profile.
- The default profile has no search or execution tools. If a custom policy
  enables Grep and Glob, they are path-checked only at their explicit
  <code>path</code>. A path that is the repository root or an ancestor of a
  denied directory can allow a recursive search to reach denied descendants;
  the guard does not enumerate results, inspect
  <code>pattern</code>/<code>glob</code> content, or model symlink traversal
  inside an allowed directory. This is a reported residual, not silently
  treated as covered.
- The policy file is protected by resolved path and
  <code>st_dev</code>/<code>st_ino</code> identity, so a hard link to it is
  denied. The <code>.claude/settings.json</code>,
  <code>.claude/settings.local.json</code> and <code>.git/**</code> patterns
  are path-based, not identity-based; a pre-existing hard link to one of those
  at an unlisted path is a residual. The default Read/Write/Edit tools cannot
  create hard links.
- Settings merge preserves foreign hooks and keys, but it rewrites the JSON
  file in the adapter's formatting. Byte-for-byte preservation is not claimed;
  the pre-change bytes are in the backup.
- Backups are not an automatic rollback. <code>uninstall</code> removes only
  the adapter's hooks.

## Provenance

Drafted by DeepSeek (DeepSeek Harness; configured route
<code>deepseek-flash</code>) on 2026-11-22. The pilot plan is
[<code>PLAN.md</code>](../../PLAN.md). Live evidence was produced on Claude
Code 2.1.311 for Windows against a disposable repository; the L1 observation
was supplied for the earlier status update. The local verification evidence is
the adapter's test suite and the read-only repository checks listed above.
