# Aegis enforcement

This page documents Aegis Guard v1, a local policy check for coding-agent tool
calls, and the current, deliberately narrow host status for enforcement work.

**No hooks are installed by this repository or by this change. No enforcement
claim is made.** Aegis Guard is a command that returns a decision. It does not
intercept a host's tool calls by itself, does not install a plugin, extension,
settings file, wrapper or host hook, and does not provide an operating-system
sandbox.

Bash is denied by default; only exact `bash_allowlist` entries pass. Builds
require an external OS or container sandbox. This is L2 only: a local policy
check, not containment.

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
defaults to `[]`. Unknown fields, missing core fields and wrong
types exit 3. A policy is read-only input; the check never rewrites it.

| Field | Type | Behavior |
| --- | --- | --- |
| `schema` | string | Must be `aegis.policy/1`. |
| `allowed_tools` | string array | Exact, case-sensitive allow-list. An unlisted tool is denied; an empty list denies all tools. |
| `denied_tools` | string array | Exact, case-sensitive deny-list. A deny wins over the allow-list. |
| `allowed_roots` | string array | Roots for path arguments. Relative entries resolve against the repository; absolute entries are used as written. An empty list denies every path argument. |
| `denied_paths` | string array | Additional glob deny patterns. A pattern without `/` matches any path component; a trailing `/**` also matches its directory; matching is case-insensitive. |
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
`.env*`, `.ssh/**`, `.aws/**`,
`.gnupg/**`, `.git-credentials`, `id_rsa*`,
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
policy check, not process containment. Use an OS or container sandbox where the
host matrix says external containment is required.

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

The versions below are the recorded target matrix for this work. Aegis Guard
does not detect host versions, and no host was executed to produce this table.
The status is a statement about available evidence and permitted reliance, not
a claim that the host is configured or protected.

| Host | Version | Status | Plain-language meaning | Evidence basis |
| --- | --- | --- | --- | --- |
| Claude CLI | 2.1.311 | candidate | The next integration candidate; not installed as a hook here and not validated for this work. | No hook installed and no pre-tool event captured. Candidate only. |
| Claude VS Code | 2.1.330 | unqualified | No Aegis-specific interception test or containment evidence; do not rely on it. | No hook installed and no interception evidence in this change. |
| Codex CLI | 0.149.1 | external containment required | Do not rely on a host hook; run the host inside an OS or container sandbox. | No tested pre-tool hook in this change; external containment is the boundary. |
| Codex VS Code | 26.1117.41037 | unqualified | No Aegis-specific interception test or containment evidence; do not rely on it. | No hook installed and no interception evidence in this change. |
| Cursor | 3.24.18 | unqualified | No Aegis-specific interception test or containment evidence; do not rely on it. | No hook installed and no interception evidence in this change. |
| Gemini | not installed | blocked | No installed host and no test path; do not claim support. | Not installed; no run or test possible. |

Exact labels: Claude CLI 2.1.311 (candidate), Claude VS Code 2.1.330
(unqualified), Codex CLI 0.149.1 (external containment required), Codex VS Code
26.1117.41037 (unqualified), Cursor 3.24.18 (unqualified), Gemini (blocked; not
installed).

### Status definitions

- **candidate**: the host is the next integration candidate. No hook is
  installed and no pre-tool interception test exists in this change.
- **unqualified**: no Aegis-specific hook, interception test or containment
  evidence. It must not be described as protected or enforced.
- **external containment required**: a host hook is not the boundary. Run the
  host inside an operating-system or container sandbox and treat Aegis Guard as
  one additional policy check, never as the containment layer.
- **blocked**: no installed host or no viable test path. No support claim.

## No hooks installed

This repository installs no Claude CLI, Claude VS Code, Codex CLI, Codex VS
Code, Cursor, Gemini, shell, Git or package-manager hook. It writes no host
settings, plugin, extension or wrapper. The matrix records status, not an
installed integration. Installing a hook would be a separate, reviewed change
with its own evidence.

## No enforcement claim

Aegis Guard is advisory infrastructure. It provides a policy decision and a
stable exit code, not confinement. The command scanner is defense-in-depth,
not a sandbox. Aegis Guard cannot stop a process that is already running,
inspect a host's internal tool dispatch, prevent a host from ignoring exit 10
or 3, or prove that any host honours the contract. Even a correct
adapter is only as strong as the host's willingness to block. Use OS or
container containment where the matrix says it is required.

## Verification

```bash
python -m unittest discover -s tools/aegis_guard/tests -v
python -m json.tool tools/aegis_guard/policy.schema.json
python scripts/ci/check-markdown-links.py docs/aegis-enforcement/README.md tools/aegis_guard/README.md
```

The test suite covers allow/deny decisions, fail-closed unlisted tools, Bash
default-deny and exact allowlist matching, missing and malformed policies,
malformed arguments, Windows backslash paths, case-insensitive matching,
UNC/device/drive-relative paths, symlink or junction escape, every built-in
secret pattern and network rule, non-adjacent git/npm/npx/pip/pip3/uv
subcommands, shell metacharacters, redirects, parentheses, shell wrappers,
backslash/quote/dollar escapes, quote and variable concatenation, and the
session marker and required files. It makes no network call. The guard imports
no `subprocess`, `socket` or HTTP client; the only `subprocess` use is a
Windows-only `mklink /J` test fixture for the junction case.

## Provenance

Drafted by DeepSeek (DeepSeek Harness) on 2026-11-22. Host version values are
the supplied matrix, not a live detection result. No host was executed for this
document.
