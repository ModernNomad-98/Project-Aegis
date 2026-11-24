# Aegis enforcement

This page documents Aegis Guard v1, a local policy check for coding-agent tool
calls, and the current, deliberately narrow host status for enforcement work.

**This repository ships no installed host hooks. The Claude adapter installs
repository-local hooks only into a repository you name, and no enforcement claim
is made.** Aegis Guard is a command that returns a decision. It does not
intercept a host's tool calls by itself, does not install a plugin, extension,
settings file, wrapper or host hook, and does not provide an operating-system
sandbox.

Bash is denied by default; only exact `bash_allowlist` entries pass. Builds
require an external OS or container sandbox. This is L2 only: a local policy
check, not containment.

Two containment results are recorded, both for the container launch only. The
[Claude Code CLI container profile](L3-claude-container.md) qualifies for L3
when the CLI is launched through that container; the
[Codex CLI container profile](L3-codex-container.md) gives container
containment with no Aegis tool-policy gate inside it, so its secrets are
excluded by the mount set rather than by policy. No other host has containment
evidence, and no enforcement claim is made for any other launch path.

The implementation is [`tools/aegis_guard/cli.py`](../../tools/aegis_guard/cli.py),
the contract is
[`policy.schema.json`](../../tools/aegis_guard/policy.schema.json), and
package usage is in the
[package README](../../tools/aegis_guard/README.md).

## What the check does

`check` evaluates one proposed tool call against a policy:

```bash
python -m tools.aegis_guard check \
  --policy C:/work/aegis-policy.json \
  --repo C:/work/app \
  --tool Read \
  --args-json "{\"file_path\":\"docs/design.md\"}" \
  --cwd C:/work/app
```

`session` checks that the repository has an Aegis adoption marker and
the files the policy requires:

```bash
python -m tools.aegis_guard session \
  --policy C:/work/aegis-policy.json \
  --repo C:/work/app
```

`--version` prints the tool version. `check` needs
`--policy`, `--repo`, `--tool` and
`--args-json`; `--cwd` is optional and defaults to the
repository. `session` needs `--policy` and
`--repo`.

## Exit contract

| Exit | Meaning | Host adapter action |
| --- | --- | --- |
| `0` | allow | Proceed only on this code. |
| `10` | deny | Block. |
| `2` | usage or argument error | Block and fix the invocation. |
| `3` | policy, environment or internal error | Block. |

**Adapters must map 10 and 3 to block, never to allow.** Exit 2 is also not an
allow. A host that ignores a non-zero result, or never invokes the check, is not
constrained by it.

A decision is emitted as one JSON object:

```json
{"decision": "allow", "reason": "allowed by policy", "policy_sha256": "<64 lowercase hex characters>"}
```

The SHA-256 covers the exact policy bytes. Errors write
`{"error": "..."}` to standard error and nothing to standard output.

## Policy fields (`aegis.policy/1`)

The eight core fields are required; `bash_allowlist` is optional and
defaults to `[]`. Unknown fields, missing core fields, wrong types and
invalid `denied_paths` globs exit 3. A policy is read-only input; the check
never rewrites it.

| Field | Type | Behavior |
| --- | --- | --- |
| `schema` | string | Must be `aegis.policy/1`. |
| `allowed_tools` | string array | Exact, case-sensitive allow-list. An unlisted tool is denied; an empty list denies all tools. |
| `denied_tools` | string array | Exact, case-sensitive deny-list. A deny wins over the allow-list. |
| `allowed_roots` | string array | Roots for path arguments. Relative entries resolve against the repository; absolute entries are used as written. An empty list denies every path argument. |
| `denied_paths` | string array | Additional glob deny patterns. A pattern without `/` matches any path component; a trailing `/**` also matches its directory; matching is case-insensitive. Invalid globs exit 3. |
| `deny_outside_repo` | boolean | Boolean declaration. v1 always requires both an allowed root and repository containment; `false` is accepted but does not disable the boundary. |
| `network_commands` | string array | Additional tokens or token phrases. Built-in program and subcommand rules cannot be removed. |
| `required_session_files` | string array | Repository-relative files required by `session`, in addition to `.aegis/project.json`. |
| `bash_allowlist` | string array | Optional exact Bash command allow-list, default `[]`. Bash is denied unless the command token list exactly equals an entry; no prefix or fnmatch matching. |

### Bash default-deny

Bash is denied by default. A Bash call is allowed only when the command
tokenizes with `shlex.split(posix=False)` to exactly the same token
list as an entry in `bash_allowlist` (default `[]`). No
prefix, glob or fnmatch matching is used. Every other Bash command exits 10.

Shell and network heuristics remain defense-in-depth and can deny an
allowlisted command. A build or other side-effecting run requires an external
OS or container sandbox. **This is L2 only: a local policy check, not
containment.**

### Built-in secret paths

These patterns are always denied, in addition to `denied_paths`:
`.env`, `.env.*`, `.envrc`, `.envrc.*`, `.ssh/**`,
`.aws/**`, `.gnupg/**`, `.git-credentials`, `id_rsa*`,
`*.pem`, `*.key`, `secrets/**` and
`credentials*`. They match at any depth and case-insensitively.
The policy list can add patterns but cannot remove these.

### Built-in network tokens

These rules are always enforced in a `command` argument:
`curl`, `wget`, `Invoke-WebRequest`,
`Invoke-RestMethod`, `ssh`, `scp`,
`sftp`, `git push`, `git fetch`,
`git clone`, `npm publish`, `npx publish`, `pip install`,
`pip3 install` and `uv pip install`. `network_commands` adds
rules; it cannot remove the built-ins.

### Command scanning

Before tokenization, any command containing `;`, `&`, `|`, `<`, `>`,
`(`, `)`, `$(`, backtick or newline is denied. Then any command containing
a backslash, single quote, double quote or dollar sign is denied. This blocks
`g\it`, `'pu'sh`, `$'...'` and `${IFS}`. Bash commands with Windows
backslash paths or quoted arguments are therefore denied; use `Read`/`Write`
path arguments for file paths.

Commands that pass are tokenized with `shlex.split(posix=False)`. The
tokenizer preserves backslashes and strips surrounding quotes, but commands
containing either were already denied. A shell wrapper is denied when the first
token basename is `bash`, `sh`, `zsh`, `cmd`, `powershell` or `pwsh`
and any argument is `-c`, `/c`, `-Command` or `-EncodedCommand`; quoted
wrappers are already denied by the quote rule. The scanner then:

- denies a network program when its basename appears in any token: curl,
  wget, ssh, scp, sftp, Invoke-WebRequest or Invoke-RestMethod;
- denies `git` (including `git.exe`) when any later token is `push`,
  `fetch` or `clone`;
- denies `npm` or `npx` when any later token is `publish`;
- denies `pip` or `pip3` when any later token is `install`;
- denies `uv` when a later token is `pip`/`pip3` and a still later token
  is `install`;
- applies additional `network_commands` entries by basename or token phrase.

Subcommands need not be adjacent: `git -C . push`,
`npm --prefix . publish`, `git.exe -c x=y push`, `/usr/bin/git push`,
`pip --disable-pip-version-check install x` and `uv pip install` are all
denied. Shell wrappers and syntax are denied independently of network content:
`bash -c "echo hi"` is denied by the quote rule, `git push>out.log` by the
redirect rule, and `(git push)` by the parenthesis rule. No recursive parsing
is attempted; quoted text is denied before tokenization. No shell is executed
and no general shell parser is implemented; false positives are accepted.

**The command scanner is defense-in-depth, not a sandbox.** It is a lexical
policy check, not process containment. Use an OS or container sandbox for any
host the matrix records without containment evidence.

These syntax and heuristic checks run before the Bash allowlist gate. A command
must pass both; an allowlisted command can still be denied here.

The allowlist closes common bypass candidates: glob or brace forms,
renamed or symlinked binaries, `env bash -c ...`, and
`python -c ...` are not allowed unless an administrator explicitly
lists that exact token string. The allowlist binds command text, not executable
identity, PATH, environment, shell functions, or program behavior. An allowlisted
`npm test` or `python script.py` can still run arbitrary or
network code. Builds require an external OS or container sandbox; this remains
L2 only.

## Path containment

For `path`, `file_path` and `notebook_path`:

- Relative values resolve against `--cwd` (default: the repository).
- Any `..` path segment is denied as traversal.
- UNC paths (`\\server\share`), device paths
  (`\\.\` and `\\?\`) and drive-relative paths
  (`C:foo`) are denied, as are reserved device names.
- A path that resolves exactly to the loaded policy file is always denied,
  compared case-insensitively, before repository or allowed-root containment.
  A path whose file identity (`st_dev`, `st_ino`) matches the policy file is
  also denied, which catches a hard link to the policy at another path. The
  policy file is therefore protected wherever it lives, regardless of
  `allowed_tools`, `allowed_roots` or `denied_paths`.
- `Grep` and `Glob` must supply an explicit, non-empty `path`. A missing
  path is denied; no repository-root default is applied. The supplied path is
  checked by the same containment and deny rules. Only that path is checked:
  an explicit root or ancestor of a denied directory can still let a recursive
  search reach denied descendants, because the guard does not enumerate results
  or inspect `pattern`/`glob` content. This residual parent-path traversal
  is reported, not addressed by a heuristic. The default Claude adapter does
  not allow `Grep` or `Glob`; this rule applies only to a custom policy that
  enables them.
- The resolved path must be inside the repository **and** an allowed root.
  `allowed_roots` alone is not sufficient; repository containment
  cannot be disabled.
- Existing paths resolve strictly, and existing symlinks or junctions are
  followed before containment. A link that escapes the repository is denied.
  A non-existent leaf is resolved with its existing components, so a symlinked
  parent still cannot escape.
- Windows containment compares case-insensitively.
- The check denies before execution. It does not open the target file.

Only top-level `path`, `file_path` and
`notebook_path` keys are inspected. A host that passes a path inside
a nested argument object bypasses this check.

## Session check

`session` requires:

- `.aegis/project.json` in the repository, as a regular file, with
  JSON object field `schema` equal to `aegis.adopt/1`;
- every `required_session_files` entry, resolved from the repository
  root and confined to it.

A missing marker, malformed marker, wrong schema, missing file or escaping file
exits 10. A missing or malformed policy exits 3. The adoption format is
documented in [Aegis Adopt](../aegis-adopt/README.md).

## Host status matrix

The versions below are the recorded host matrix for this work. Aegis Guard does
not detect host versions. The two Claude Code CLI rows and the Codex CLI
container row are based on live runs on 2026-11-22: one Claude run in a
disposable repository on Windows and two runs inside containers; the container
versions are the image tags, not a live detection result. The Cursor and Codex
VS Code rows are based on hosted runs recorded on 2026-11-23, plus the Cursor
follow-up retest on 2026-11-24 at PR #1215 (merged in `626d304`). The Gemini
row rests on an external record dated 2026-11-23, not a repository-hosted run.
The Cursor row also cites a separate 3.31.15 payload capture dated 2026-11-23;
that capture is provenance for the adapter fix, not a support run. The evidence
column names the records; the artifacts are retained in an external evidence
archive, and no artifact hash is presented as verifiable from this repository.
The remaining rows are target versions that were not executed for this
evidence. The status is a statement about available evidence and permitted
reliance, not a claim that the host is configured or protected.

| Host | Version | Status | Plain-language meaning | Evidence basis |
| --- | --- | --- | --- | --- |
| Claude CLI | 2.1.311 | L2 tool gate; L1 UNRUN | The PreToolUse tool gate blocked a protected Write and a Bash call. The SessionStart hook exited 2, but the session continued, so the L1 session gate is not achieved. | Live disposable-repo run on Windows, 2026-11-22: Write to the policy path and Bash were denied by the hook; SessionStart exit 2 did not block. |
| Claude Code CLI, container | 2.1.311 in `aegis-claude-l3:2.1.311-python` | L3 qualified (container launch only) | L3 holds only when the CLI is started through the Aegis container: read-only root, dropped capabilities, non-root, and no route out except an allow-list proxy. Started natively on Windows it is still L2. | Live container run on Windows, 2026-11-22: direct egress was unreachable, the proxy refused a non-allow-listed target, a workspace write succeeded, and a write to `/etc/passwd` was denied; see [the L3 profile](L3-claude-container.md). |
| Claude VS Code | 2.1.330 | unqualified | Not exercised for this evidence: no Aegis-specific interception test or containment evidence; do not rely on it. | No hook installed and no interception evidence in this change; no functional run is recorded. |
| Codex CLI | 0.149.1 | unqualified | Not exercised for this evidence: no hook and no containment evidence for this native version. Running it inside the container profile is a candidate, not a tested run. | No native run and no tested pre-tool hook; the container profile was exercised only on 0.171.0. |
| Codex CLI, container | 0.171.0 in `aegis-codex-l3:latest` | L3 containment (container launch only; not Aegis tool policy) | L3 holds only when Codex is started through the Aegis container: read-only root, dropped capabilities, non-root, and no route out except an allow-list proxy. Aegis Guard is not wired to Codex, so `.env` and tool denies are not enforced inside it; secrets must be excluded by the mount set. | Live container run on Windows, 2026-11-22: the model call through the proxy succeeded, a workspace write succeeded, a root write was refused, direct egress was unreachable, and the proxy refused a non-allow-listed target; see [the L3 profile](L3-codex-container.md). |
| Codex VS Code | 26.51120.41243 on VS Code 1.147.0 | instruction-only; functional smoke test; uncontained | The Codex panel rendered over Remote-SSH and one bounded prompt (`Reply exactly: READY`) returned READY. That is a functional smoke test only: it does not show that instruction files were honored or that a task can complete. There is no Aegis hook; the extension host runs as the VM user, and the record states UFW (the host firewall) was off; egress was not probed. `instruction-only` here means no Aegis hook, not a tested enforcement mode. Not protected, not qualified, not contained; Codex CLI in the container remains the contained Codex path. | Hosted run 2026-11-23 (HOSTED-4): `retest2/codex-ready.png`, `retest2/latest-session-log.txt` (`outcome=success`); no instruction-adherence or Aegis-hook test. |
| Cursor | 3.24.18 | L2 partial — UI-observed; raw hook exit codes/JSON not logged; L3 UNRUN; uncontained | In one 3.24.18 Remote-SSH session on 2026-11-23 the Cursor UI showed Shell blocked, a README read allowed and a secret read denied. Those outcomes are UI-observed only: the agent relayed them and the screenshots show them, but the raw hook exit codes and JSON were not logged, so the hook layer is not proven. The first Shell call was blocked by a fail-closed adapter error on an empty `cwd` (the pre-#1215 behavior), not by policy; the retry was denied by default-deny. Any hook gate here is advisory and bypassable, the agent ran as the VM user and Cursor's terminal sandbox did not start, so this is not containment. The empty-string `cwd` Shell path was retested on 2026-11-24 at PR #1215 (3.24.18 session A and a 3.31.15 E1 run; sessions B/C covered the README and secret reads), merged in `626d304`; the empty-string Read default remains unit-tested only. The separate 3.31.15 payload capture (2026-11-23 23:48 PT) is provenance for the adapter fix, not a support run. | Hosted run 2026-11-23 (HOSTED-2): `shell-denied.png`, `readme-allowed.png`, `secret-blocked.png`; exact hook exit codes and raw JSON were not logged. Separate 3.31.15 payload capture on 2026-11-23 23:48 PT (HOSTED-2A): raw payload not published; sanitized copy retained. Retest 2026-11-24 at PR #1215 (merged `626d304`); exact session times are not recorded; the empty-string Read default is unit-tested only. |
| Gemini | 0.70.0 (external record) | L2 UNKNOWN — no Aegis tool-gate result proven | A Gemini CLI 0.70.0 session in an external record read a README. The record lists `secrets/credential.txt` as blocked but does not say which layer blocked it; it attributes the `~/.gemini/.env` refusal to Gemini's own path guard, not Aegis Guard. The same record says both that `run_shell_command` was denied and that a shell ran `echo hi` under YOLO (auto-approve mode), so the shell outcome is UNKNOWN and no Aegis policy decision is proven. The host was exercised, but no Aegis layer is proven; this is not instruction-only and not contained. | External NEXT-HOSTED-1 record, 2026-11-23; adapter support for Gemini hook events merged in PR #1213 (`7afbb6fc`), but this repository installs no Gemini hook. No repository-side run; L3 UNRUN. |

Owner decision: the 2026-11-23 acceptance of Codex VS Code as functional
but uncontained is a reliance decision, not test evidence.

**Artifacts.** The 2026-11-23 hosted artifacts and the 2026-11-24 retest
artifacts are retained in an external evidence archive; they are not in this
repository. The SHA-256 values recorded in that archive are not reproduced
here and cannot be verified from this repository. The Gemini row has no
artifact; it rests on the external NEXT-HOSTED-1 record only.

Exact labels: Claude CLI 2.1.311 (L2 tool gate; L1 UNRUN), Claude Code CLI
container profile (L3 qualified; container launch only), Claude VS Code
2.1.330 (unqualified), Codex CLI 0.149.1 (unqualified), Codex CLI container
profile (L3 containment; container launch only, not Aegis tool policy),
Codex VS Code 26.51120.41243 on VS Code 1.147.0 (instruction-only; functional
smoke test; uncontained), Cursor 3.24.18 (L2 partial — UI-observed; raw hook
exit codes/JSON not logged; L3 UNRUN; uncontained), Gemini 0.70.0 (L2 UNKNOWN —
no Aegis tool-gate result proven).

### Status definitions

- **L2 tool gate; L1 UNRUN**: the PreToolUse hook blocked tool calls on the
  observed host, but the SessionStart hook did not block the session. Only the
  per-tool layer is effective; do not claim a session gate.
- **L2 partial — UI-observed; raw hook exit codes/JSON not logged; L3 UNRUN;
  uncontained**: the host was exercised and its UI showed tool outcomes
  consistent with a hook, but no raw hook exit code or JSON was logged, so a
  policy decision is not proven. A fail-closed adapter error is not counted as
  a policy denial. The host ran with ordinary user rights and no containment
  test was run. The label covers only the observed host and launch path; do not
  describe the host as gated, contained or protected.
- **L2 UNKNOWN — no Aegis tool-gate result proven**: the host was exercised,
  but the recorded outcomes do not establish that Aegis acted, or they
  contradict each other. This is not a partial L2 result: no Aegis tool-gate
  result is proven, and no containment result is claimed.
- **instruction-only; functional smoke test; uncontained**: the host runs and
  one bounded smoke-test prompt completed, but it has no Aegis hook or policy
  gate. `instruction-only` here means only that no hook is present; reliance is
  on the host's own instructions and behavior, not on Aegis. It is not a tested
  enforcement mode and the run does not show that instruction files were
  honored. It must not be described as protected, qualified or contained.
- **L3 qualified (container launch only)**: the CLI ran inside a container the
  host cannot escape, and the recorded tests confirm the boundary. The claim
  covers that one launch path; the same CLI started natively is still L2.
- **L3 containment (container launch only; not Aegis tool policy)**: the CLI
  ran inside a container with no observed route out. The recorded tests confirm
  the tool, workspace and network outcomes only: a model call and a workspace
  write succeeded, a root write was refused by the read-only root, direct egress
  was unreachable and the proxy refused a non-allow-listed target. Capability
  dropping, `no-new-privileges`, uid `1000` and the tmpfs mounts are launch
  flags, not individually probed. Unlike the L3 qualified row, no Aegis
  tool-policy hook runs inside this container, so tool and secret-path denies
  are not enforced; the claim covers containment for that launch path only.
- **unqualified**: the host was not exercised for this evidence, or it has no
  working surface or hook to exercise, and it has no Aegis-specific
  interception test or containment evidence. This is distinct from
  **instruction-only**, which records an exercised working surface with no
  Aegis hook. It must not be described as protected or enforced.
- **external containment required**: no row currently carries this status. It
  records the requirement that a host hook is not the boundary: run such a host
  inside an operating-system or container sandbox and treat Aegis Guard as one
  additional policy check, never as the containment layer.
- **blocked**: no installed host or no viable test path. No support claim.

## No hooks installed

This source repository ships no Claude CLI, Claude VS Code, Codex CLI, Codex VS
Code, Cursor, Gemini, shell, Git or package-manager hook, and it installs no
global or user-level settings. The Claude CLI and Cursor runs used the
repository-local adapter installed only in disposable test repositories, not in
this source checkout. The Gemini record describes a hook migration, but it
attributes the `.env` refusal to Gemini's own path guard, not to that adapter;
adapter support for Gemini hook events merged in PR #1213, but this repository
installs no Gemini hook. Codex VS Code has no adapter. The matrix records
observed status, not a source-checkout installation. Installing a hook
elsewhere is a separate change with its own evidence.

## No enforcement claim

Aegis Guard is advisory infrastructure. It provides a policy decision and a
stable exit code, not confinement. The command scanner is defense-in-depth,
not a sandbox. Aegis Guard cannot stop a process that is already running,
inspect a host's internal tool dispatch, prevent a host from ignoring exit 10
or 3, or prove that any host honours the contract. Even a correct
adapter is only as strong as the host's willingness to block. Use OS or
container containment for any host the matrix records without containment evidence.

## Verification

```bash
python -m unittest discover -s tools/aegis_guard/tests -v
python -m unittest discover -s tools/aegis_claude/tests -v
python -m json.tool tools/aegis_guard/policy.schema.json
python scripts/ci/check-markdown-links.py docs/aegis-enforcement/README.md tools/aegis_guard/README.md docs/aegis-claude/README.md tools/aegis_claude/README.md
```

The test suite covers allow/deny decisions, fail-closed unlisted tools, Bash
default-deny and exact allowlist matching, missing and malformed policies,
invalid `denied_paths` globs, malformed arguments, Windows backslash paths,
case-insensitive matching,
UNC/device/drive-relative paths, symlink or junction escape, every built-in
secret pattern and network rule, non-adjacent git/npm/npx/pip/pip3/uv
subcommands, shell metacharacters, redirects, parentheses, shell wrappers,
backslash/quote/dollar escapes, quote and variable concatenation, and the
session marker and required files. The adapter suite adds install/uninstall,
hook mapping, protected-path, and non-default policy-path cases. Neither suite
makes a network call. The guard imports no `subprocess`, `socket` or HTTP
client; the only `subprocess` use is a Windows-only `mklink /J` test fixture
for the junction case.

## Provenance

Drafted by DeepSeek (DeepSeek Harness) on 2026-11-22. Claude CLI 2.1.311 was
executed live on Windows for the L2/L1 evidence. The two container rows were
live launches whose versions come from the image names, not from Aegis Guard
detection. Cursor 3.24.18 and Codex VS Code 26.51120.41243 on VS Code 1.147.0
are reported from hosted records dated 2026-11-23; Gemini 0.70.0 is reported
from an external record dated 2026-11-23. Cursor also has a separate 3.31.15
payload capture dated 2026-11-23 23:48 PT (HOSTED-2A) and a 2026-11-24 retest
at PR #1215, merged in `626d304`; exact retest session times are not recorded.
The versions were observed in those records, not detected by Aegis Guard. The
remaining host version values are the supplied matrix, not a live detection
result.
