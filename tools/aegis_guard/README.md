# Aegis Guard v1

Aegis Guard is a local, fail-closed policy check for one proposed coding-agent
tool call, plus a session check for a repository's Aegis adoption files. It is
standard library only and runs on Python 3.14. It reads a JSON policy and a
repository path, writes one JSON decision to standard output, and never
executes the proposed tool call, starts a shell, opens a network connection, or
writes to the repository.

**No host hook is installed by this package, and no enforcement is claimed.**
Aegis Guard is a command. It constrains an agent only when a host adapter calls
it before acting and blocks on a non-zero exit code.

Bash is denied by default; only exact `bash_allowlist` entries pass. Builds
require an external sandbox. This is L2 only: a local policy check, not
containment.

The user guide, including the host status matrix, is
[`docs/aegis-enforcement/README.md`](../../docs/aegis-enforcement/README.md).

## Invocation

Run from the Aegis checkout root. The current directory is not used for path
containment; the explicit repository and policy arguments are.

```bash
python -m tools.aegis_guard --version
python -m tools.aegis_guard check --policy POLICY.json --repo REPO --tool TOOL --args-json JSON [--cwd CWD]
python -m tools.aegis_guard session --policy POLICY.json --repo REPO
```

`check` evaluates one proposed tool call. `session` requires
`.aegis/project.json` with schema `aegis.adopt/1` and every
`required_session_files` entry from the policy.

## Exit contract

| Exit | Meaning | Adapter action |
| --- | --- | --- |
| `0` | allow | Proceed only on this code. |
| `10` | deny | Block. |
| `2` | usage or argument error | Block and fix the invocation. |
| `3` | policy, environment or internal error | Block. Do not fall back to allow. |

Host adapters **must map 10 and 3 to block, never to allow**. Exit 2 is also not
an allow. Only exit 0 permits an action.

A deny or allow decision is printed as one JSON object with keys
`decision`, `reason` and `policy_sha256`; the
SHA-256 is over the exact policy bytes. Errors print one JSON object with an
`error` key to standard error and nothing to standard output.

```json
{"decision": "deny", "reason": "path denied by pattern '**/.env' for file_path: .env", "policy_sha256": "<64 lowercase hex characters>"}
```

## Policy: `aegis.policy/1`

Eight core fields are required; `bash_allowlist` is optional and
defaults to `[]`. Types are checked; unknown fields and invalid
`denied_paths` globs are errors (exit 3). The
[JSON Schema](policy.schema.json) mirrors the contract.

```json
{
  "schema": "aegis.policy/1",
  "allowed_tools": ["Read", "Write", "Bash", "NotebookEdit"],
  "denied_tools": ["WebFetch"],
  "allowed_roots": ["."],
  "denied_paths": [],
  "deny_outside_repo": true,
  "network_commands": [],
  "required_session_files": [".aegis/SESSION.md"],
  "bash_allowlist": ["git status", "python -m unittest"]
}
```

| Field | Type | Meaning |
| --- | --- | --- |
| `schema` | string | Exactly `aegis.policy/1`. |
| `allowed_tools` | string array | Exact, case-sensitive tool allow-list. An unlisted tool is denied. An empty list denies every tool. |
| `denied_tools` | string array | Exact, case-sensitive deny-list. A deny wins over the allow-list. |
| `allowed_roots` | string array | Path roots for `path`, `file_path` and `notebook_path` arguments. Relative entries resolve against the repository. An empty list denies every path argument. |
| `denied_paths` | string array | Additional glob deny patterns. A pattern without `/` matches any path component; a trailing `/**` also matches its directory. Matching is case-insensitive. Invalid globs exit 3. |
| `deny_outside_repo` | boolean | Boolean declaration. v1 always requires a path to be inside both an allowed root and the repository; `false` is accepted but does not disable containment. |
| `network_commands` | string array | Additional tokens or token phrases to reject. Built-in program basenames and subcommand rules are always enforced. |
| `required_session_files` | string array | Repository-relative files required by `session`, in addition to `.aegis/project.json`. Absolute paths and `..` are policy errors. |
| `bash_allowlist` | string array | Optional exact Bash command allow-list, default `[]`. Bash is denied unless the command token list exactly equals an entry; no prefix or fnmatch matching. |

Built-in secret patterns are always enforced in addition to
`denied_paths`: `.env`, `.env.*`, `.envrc`, `.envrc.*`,
`.ssh/**`, `.aws/**`, `.gnupg/**`, `.git-credentials`,
`id_rsa*`, `*.pem`, `*.key`,
`secrets/**` and `credentials*`. Built-in network rules are always
enforced in addition to `network_commands`: the program basenames
`curl`, `wget`, `Invoke-WebRequest`, `Invoke-RestMethod`, `ssh`,
`scp` and `sftp`; and the subcommand patterns `git push`, `git fetch`,
`git clone`, `npm publish`, `npx publish`, `pip install`, `pip3 install`
and `uv pip install`.

## `check` behavior

1. Load and validate the policy; missing or malformed policy exits 3.
2. Deny a tool in `denied_tools` or not in `allowed_tools`.
3. For `path`, `file_path` and `notebook_path`,
   reject traversal and UNC/device/drive-relative paths, resolve against
   `--cwd` (default: the repository), then require the result inside
   both the repository and an allowed root. Symlinks and junctions are resolved
   before containment, so an escape is denied. Case is folded for Windows
   containment. `Grep` and `Glob` must carry an explicit, non-empty
   `path`; a missing or empty path is denied, and no repository-root default
   is applied. The default Claude adapter allow-list does not include either
   tool; the rule applies when a custom policy enables them.
4. Always deny a path argument that resolves exactly to the loaded policy
   file, compared case-insensitively, or whose file identity
   (`st_dev`, `st_ino`) equals the policy file's identity. The identity check
   denies a hard link to the policy at another path. This runs before
   repository and allowed-root containment, so the policy file is protected
   regardless of where it lives and regardless of `allowed_tools`,
   `allowed_roots` or `denied_paths`.
5. Reject a built-in secret path or a `denied_paths` match.
6. For a `command` argument, first deny shell syntax: `;`,
   `&`, `|`, `<`, `>`, `(`,
   `)`, `$(`, backtick or newline. Then deny backslash,
   single quote, double quote or dollar sign. This blocks `g\it`,
   `'pu'sh`, `$'...'` and ${IFS}. Bash commands with
   Windows backslash paths or quoted arguments are denied; use
   `Read`/`Write` path arguments for paths. Commands that
   pass are tokenized with `shlex.split(posix=False)`.
7. For Bash, the allowlist is the primary gate: allow only when the command
   token list exactly equals an entry in `bash_allowlist`. A missing
   or empty allowlist denies every Bash command; no prefix or fnmatch matching
   is used. Shell/network heuristics remain defense-in-depth and can deny an
   allowlisted command.

Bash is denied by default. A build or other side-effecting run requires an
external OS or container sandbox. This is **L2 only**: a local policy check,
not containment.

Only top-level argument keys are inspected. A tool that carries a path or
command in a nested structure is not path-checked by this version. For
`Grep` and `Glob`, the named `path` is checked, not the files a recursive
search would reach: an explicit path that is the repository root or an ancestor
of a denied directory can still traverse denied descendants. The guard does not
enumerate results or inspect `pattern`/`glob` content. This residual
parent-path traversal is reported, not addressed by a heuristic.

## Tests

```bash
python -m unittest discover -s tools/aegis_guard/tests -v
```

The suite is standard library only and makes no network call. It covers Bash
default-deny and exact allowlist matching, shell syntax and wrapper denial,
backslash/quote/dollar escapes and concatenation, redirects and parentheses,
non-adjacent subcommands, every built-in secret pattern including `.envrc`,
invalid `denied_paths` globs, and the path/session rules. The Claude
adapter suite additionally covers the explicit-path requirement for `Grep` and
`Glob`. One Windows-only fixture
creates a junction with `cmd /c mklink /J` to prove the escape is denied. The
guard itself imports no `subprocess`, `socket` or HTTP client.

## Limits

Aegis Guard does not provide an OS sandbox, process containment, host
interception, secret detection inside file contents, or a guarantee that a host
honours its exit code. Bash is denied by default and only exact allowlist
entries pass. The allowlist binds command text, not executable identity, PATH,
environment, shell functions, or program behavior: an allowlisted `npm test`
or `python script.py` can still run arbitrary or network code, and an
allowlisted name can resolve to a different binary. Builds require an external
OS or container sandbox. This is L2 only: a local policy check, not
containment. It is one policy layer, useful only when an adapter invokes it and
blocks on 10, 3, 2 and every other non-zero result. Policy-file protection uses
the resolved case-folded path and the file's st_dev/st_ino identity; a
pre-existing hard link at a different path is denied. Residual short-name/path
alias risks require the external sandbox. Host status and evidence
are in the [user guide](../../docs/aegis-enforcement/README.md).
