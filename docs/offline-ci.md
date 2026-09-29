# Offline verification in GitHub Actions

This guide is for contributors and reviewers checking a Project Aegis change.
It explains what the automated **continuous integration (CI)** jobs prove, how
to reproduce important checks locally, and how to interpret a failure or skip.
The jobs test skills and the **Behavioral Eval Runner (BER)** with synthetic
inputs; they do not run a live model evaluation.

## A normal verification pass

1. Run the [local checks](#local-reproduction) on the changed revision and
   record the command, result and any skip.
2. Open a pull request (PR) and wait for all five jobs in the table below
   (the Linux and Windows verification jobs, the two tools-test jobs and the
   protected-file guard) on its exact head revision. A later push starts new
   checks; older green results do not cover the new head.
3. Read the job logs and retained evidence if a check fails. Fix a test or
   environment failure and rerun the new candidate. A documented protected
   path guard failure needs an owner disposition under the
   [merge policy](reconciliation/auto-merge-policy.md); it is not green. For
   four named BER reporting/aggregation files, the owner's standing exception
   [AEGIS-APR-047](approvals/APPROVAL_REGISTER.md#aegis-apr-047-standing-gate-guard-exception-for-four-ber-files)
   supplies that disposition when all its conditions are met.
4. Close out only after independent review and all applicable execution jobs
   have passed. A skipped capability remains unproven.

The `validate-skills` workflow runs on every pull request targeting `main` and
every push to `main`. Pull requests have no path filter. The existing required
check names stay `validate-skills` and `gate-guard`; branch protection is unchanged.

| Job | Coverage | Merge role | Timeout |
| --- | --- | --- | --- |
| `validate-skills` on Ubuntu | CI recorder/guard regressions, validator and audit self-tests, skill validation, BER self-check and full suite, PowerShell Core Scenario A acceptance, pull-request-only Developer Certificate of Origin (DCO) check | Existing required check | 15 minutes |
| `windows-offline-checks` on Windows | Recorder regressions, validator and audit self-tests, skill validation, BER self-check and full suite, sequential PowerShell Desktop 5.1 and Core acceptance | Additional visible coverage; not registered as required | 20 minutes |
| `gate-guard` on Ubuntu | Detect changes to the merge gate and its enforcement surfaces | Existing required check; PR only | 5 minutes |
| `tools-tests-linux` on Ubuntu | Host-bridge Node callback tests, setup routing-contract suite, delivery-control suite | Isolated from the gates; not registered as required | 15 minutes |
| `tools-tests-windows` on Windows | The same three suites, plus a read-only ownership diagnostic (token user, default owner, elevation, temp-root owners) recorded before the delivery-control suite | Isolated from the gates; not registered as required | 20 minutes |

The two verification jobs run independently, without cross-platform fail-fast,
automatic retries, quarantine or `continue-on-error`. A delivery closeout waits
for both verification jobs. A post-merge run detects regressions on `main`; it
cannot retroactively prevent a merge.

### Gate isolation

The two verification jobs execute only repository code that `gate-guard`
protects (see [Protected files](#protected-files)), plus pinned actions and
pinned dependencies. PR files outside that set are read only as
data, for example skills checked by the validator. Test code that a pull
request can change without tripping `gate-guard` runs in the separate
`tools-tests-linux` and `tools-tests-windows` jobs instead. That covers the
host-bridge Node tests, `tools/aegis_setup/tests` and
`tools/aegis_delivery_control/tests`. A step in a gate job could write to
`$GITHUB_ENV` or `$GITHUB_PATH`, or rewrite a gate script before it runs, and
make a failing gate pass. A separate job shares no runner, environment file,
`PATH` or checkout with the gates, so this code cannot reach them.

The tools jobs use a read-only token, reference no secrets and do not persist
checkout credentials. `scripts/tests/test_offline_ci.py` checks this layout. The
CI self-tests fail when a gate job does any of these:

- runs Node or a tools suite;
- names a repository path outside the `gate-guard` pattern in a command,
  `working-directory`, `-m` module, `-r` file, `env` value or action input, or
  puts `..` in an `env` value or action input;
- uses a local, Docker or tag-pinned action instead of one pinned to a commit
  SHA (the commit's full 40-character hash);
- runs a step, or sets a job default, with a shell other than `bash`, `pwsh`
  or `powershell`, or sets a job-default `working-directory`;
- sets, in the workflow, job or step `env`, one of the listed variables that
  point a tool at other code or configuration:
  - interpreter and loader paths: `PATH`, `PYTHONPATH`, `PYTHONHOME`,
    `PYTHONSTARTUP`, `PYTHONUSERBASE`, `PYTHONPLATLIBDIR`, `PYTHONEXECUTABLE`,
    `NODE_OPTIONS`, `NODE_PATH`, `PSMODULEPATH`, `BASH_ENV`, `ENV`,
    `LD_PRELOAD` and `LD_LIBRARY_PATH`;
  - Git: `GIT_EXEC_PATH`, `GIT_DIR`, `GIT_WORK_TREE`, `GIT_TEMPLATE_DIR` and
    every `GIT_CONFIG*` variable. These can inject configuration such as
    `core.fsmonitor`, which the recorder's `git status` would run.

  Names are matched case-insensitively. Other variables are not denied by
  name, but their values are still checked as paths.

The tests read the workflow text. They cannot see what a protected script does
internally; `gate-guard` covers that by requiring review of every protected
change.

On Windows, `CreateProcess` looks for a program such as `git` or `python` in
the current directory before `PATH`. The recorder runs from the checkout root,
so the workflow sets `NoDefaultCurrentDirectoryInExePath=1` to turn that search
off, and `gate-guard` also protects root-level `.exe`, `.com`, `.bat`, `.cmd`,
`.ps1` and `.dll` files. A Windows-only self-test proves that a root `git.exe` runs
without the variable and does not run with it.

Whether the tools jobs become required status checks is a separate
branch-protection decision for the owner. Until then they are visible
coverage, and a delivery closeout waits for them like the Windows job.

## Dependencies and environment

Both verification jobs use Python 3.14 and full Git history. Some BER fixtures
verify historical authorization commits, so a shallow checkout is insufficient.
`requirements-ci.txt` is a complete hash lock. It pins the validator dependency,
the OpenAI software development kit (SDK) used by mocked transport tests, and
every transitive dependency, each with the SHA-256 hash of every published file
for that version. Both jobs install it with
`pip install --require-hashes --only-binary :all: --no-deps -r requirements-ci.txt`
and then run `pip check`: a file whose hash is not in the lock fails the install,
no source distribution is built, and nothing outside the lock is resolved. The
lock's `openai` hashes must equal `AUTHORIZED_SDK_WHEEL_SHA256` and
`AUTHORIZED_SDK_SDIST_SHA256` in
`tools/behavioral_eval_runner/judge/calibration_transport.py`;
`scripts/tests/test_offline_ci.py` checks this, so an SDK bump must update the
constants and the lock together. The validator's ordinary runtime dependency
remains separately available in `requirements.txt`.

### Updating the lock

Edit `requirements-ci.in`, never `requirements-ci.txt` by hand. Then, in a Python
3.14 environment with `pip-tools` installed, regenerate the lock from the
repository root:

```text
CUSTOM_COMPILE_COMMAND="python -m piptools compile --generate-hashes --strip-extras --output-file=requirements-ci.txt requirements-ci.in" python -m piptools compile --generate-hashes --strip-extras --output-file=requirements-ci.txt requirements-ci.in
```

`CUSTOM_COMPILE_COMMAND` keeps the lock header stable and records the intended
compile options. Dependabot is expected to regenerate the lock with those
options, including `--generate-hashes`; confirm this on its first pull request
rather than assuming it. `requirements-ci.in` pins `colorama` on every
platform because `tqdm` needs it only on Windows, so a lock compiled on Linux,
as Dependabot's is, still installs on `windows-latest`.

Dependabot opens one grouped Python pull request a week for everything except
`openai`, which gets its own pull request so an SDK release, which also needs the
`AUTHORIZED_SDK_*` constants updated, cannot block the other bumps. It also opens
one grouped pull request a week for the host bridge's npm packages, and weekly
pull requests for the pinned GitHub Actions. The lock and the workflow are
protected paths, so each Python or Actions bump needs the owner's exact-head
merge exception.

On Windows, installing `openai` into a virtual environment under a deep
directory can fail with `OSError: [Errno 2]` because some of its files exceed
the 260-character path limit. Use a short path such as `C:\venv\aegis`, or
enable long paths in Windows.

The environment precheck imports `openai`, `httpx2` and `yaml`, verifies the SDK's
existing authorized version, and requires the reviewed Python minor. A missing
SDK must fail that step instead of silently skipping SDK-dependent cases. The
resolved dependency inventory is retained with the run.

Fixture storage uses the runner's temporary directory outside the checkout.
`PYTHONDONTWRITEBYTECODE=1` avoids generated bytecode in source/fixture trees.
The acceptance suite invokes its current PowerShell host in child processes;
Windows runs Desktop and Core sequentially in the same checkout.
The Desktop step itself uses `shell: powershell`: starting its Python recorder
from Core would pass Core's module search path through to the Desktop child and
can break `Get-FileHash` discovery. See Microsoft's
[cross-edition module-path documentation](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_psmodulepath#starting-windows-powershell-from-powershell-7).

The checks use synthetic fixtures, fake credentials and mocked transports.
Dependency installation and evidence upload use network access; this workflow
is not a network-isolation mechanism. It does not dispatch live model evaluations,
run measured calibration, provide human labels, or execute a sealed holdout.
Audit self-tests are required, while the audit's semantic candidates remain
advisory findings that need triage.

## Evidence and failures

`scripts/ci/record-check.py` runs the existing command once, streams its combined
output, preserves raw log bytes and writes a JavaScript Object Notation (JSON)
record containing the native exit code, elapsed time, checkout and pull-request
revision hashes, dirty state, Python/platform
and key package versions. It propagates failure and refuses to replace an earlier
log or metadata record with the same label. It does not reinterpret a test runner's
result or retry a command.

Each verification job uploads its logs and records on success or failure, with a
unique operating-system (OS)/run/attempt artifact name and **14-day retention**.
Setup failures before
the recorder runs remain visible in native Actions logs. The upload action is
pinned to the verified `actions/upload-artifact` v7.0.1 commit
`043fb46d1a93c77aae656e7c1c64a875d1fc6a0a`; checkout and setup-python retain their
existing reviewed pins. See the action's
[retention documentation](https://github.com/actions/upload-artifact#retention-period).

Full test output retains skip reasons. Capability differences can change skip
counts: the precheck records both Portable Operating System Interface (POSIX)
no-follow materialization and atomic
evidence-write capabilities rather than assuming either from the OS name.
Windows may lack symlink privileges or distinct short (8.3) file-name
aliases; Linux acceptance does not execute Windows file-lock behavior. Hosted
results must be reported as actually observed, not as a fixed expected count.

The [delivery record](evidence/offline-ci-2026-09-12/DELIVERY.md) links the merged
implementation and successful post-merge run. The retained
[hosted verification evidence](evidence/offline-ci-2026-09-12/HOSTED.md)
includes 19 successful recorded commands (nine Ubuntu, ten Windows), their
raw logs and environment metadata. These are command records, not a count of
individual tests.

## Reading a failure

| Finding | What it means for this revision |
| --- | --- |
| Environment precheck fails | The expected interpreter or pinned dependency is absent or changed; later skipped tests cannot be counted as passing coverage. |
| Validator or test job fails | Read its recorded command, native exit code and raw log. Correct the cause and rerun checks on the new revision. |
| Protected-file guard fails | A changed path needs deliberate manual review and merge. The guard is reporting its intended condition; it was not bypassed or made green. Follow the owner approval register and current merge policy. |
| Capability test skips | That capability was not exercised on this host. Keep the skip in the closeout and seek another host or proof when required. |

## Protected files

Following recorded [decision D60](reconciliation/step-0-reconciliation-v4.md),
the guard retains its original protected paths and includes the
new checks' dependencies: `scripts/ci/`, the contract-audit script, all acceptance
scripts and fixtures, the entire BER package (runtime, tests, schemas and fixtures),
its parent import paths `tools.py` and `tools/__init__.py`, and both root requirements
files. The lock's input, `requirements-ci.in`, is not protected: editing it
changes nothing in CI until the protected lock is regenerated. The guard also
protects the Dependabot configuration, `.github/dependabot.yml` (or `.yaml`),
because its ignore rules and groups decide which dependency bumps are ever
proposed (owner decision, 2026-09-29). Changes to these
paths require explicit review and deliberate merge.
The guard also protects all of `scripts/`, every root-level Python module,
extension, `.pth` file or package `__init__`, and every root-level `.exe`, `.com`,
`.bat`, `.cmd`, `.ps1` or `.dll` file, matched case-insensitively. Those
are the directories Python puts first on the import path when the workflow runs
`python scripts/<name>.py` or `python -m <module>`, so a new file there could
shadow the standard library or PyYAML and turn a failing check green. Every
script and `pip` call in the workflow also runs with `python -P`, which keeps
the script directory off the import path; `-I` is not used because it also
ignores the `PYTHONIOENCODING` and `PYTHONDONTWRITEBYTECODE` settings. The
`python -m tools.behavioral_eval_runner` and `python -m unittest` runs need
the checkout root on the import path, so they cannot use `-P`; the guard's
root-level protection covers them instead.
The guard also protects any `.claude/agents/` directory, recursively, at the
root or nested anywhere in the repository (for example `docs/.claude/agents/`).
Claude Code honours `hooks`, `mcpServers` and `permissionMode` in a project
agent file, searches `.claude/agents/` recursively, and loads every
`.claude/agents/` from the working directory up to the repository root. So an
agent file anywhere on that path can run shell commands, start a process or
skip permission prompts. The skill validator separately checks every agent file
under the root `.claude/agents/`, recursively, and rejects any frontmatter key
outside a short allow-list (`name`, `description`, `tools`, `model`,
`disallowedTools`, `maxTurns`, `effort`, `color`), any repeated key, any YAML
anchor, alias, tag (such as `!!merge`), directive or merge key (`<<` or any
merge-tagged key), and any tracked agent file outside the root
directory. It names `hooks`, `mcpServers` and `permissionMode` as forbidden.
A tracked entry named `.claude` or `.claude/agents` anywhere in the repository,
such as a git symlink, is protected by the guard and rejected by the validator,
because it could point an agent lookup at a directory with any name. The
validator lists tracked files with `git ls-files`; when git is unavailable it
falls back to a filesystem walk, which also sees untracked files.
The guard also protects Claude Code and Git configuration at any depth,
matched case-insensitively: `.claude/settings.json` and
`.claude/settings.local.json` (hooks, credential helpers, permissions),
`.mcp.json` (starts Model Context Protocol (MCP) server processes, without a
prompt in `-p` and SDK runs), `.claude/commands/` (skill-style frontmatter the
validator does not check), `.claude/hooks/` (scripts that hooks call), `.claude-plugin/` (bundles
hooks and MCP servers) and `.gitattributes` (can hide diffs and change the
bytes that evidence hashes cover). The commands, hooks and plugin entries match
with or without a trailing slash, so a symlink standing in for the directory is
protected too.
The skill validator separately keeps shipped skills free of executable
configuration. A skill's frontmatter may only use `name`, `description`,
`disable-model-invocation`, `license`, `compatibility` and `metadata`, with no
repeated key, no YAML anchor, alias, tag, directive or merge key, and no
`---` inside the block; it names `hooks`, `allowed-tools` and `shell` as
forbidden. No markdown file in a skill folder may contain `!`-prefixed shell
injection (an inline `` !`command` ``, or a fence of three or more backticks or
tildes followed by `!` anywhere on a line). These two checks also run on
`_template`, which Claude Code loads and consumers copy. Over tracked paths
only, so untracked local worktrees are ignored, it also rejects a
`.claude-plugin/`, nested `.claude/`, `hooks/`, `.mcp.json` or `.lsp.json`
inside a skill folder; any `.claude/skills/` tree other than the root one; any
tracked `.mcp.json` or `.claude/settings*.json` anywhere in the repository; and
any tracked symlink under `.claude/skills/`.
The source repository's
[owner grant](approvals/APPROVAL_REGISTER.md#aegis-apr-002-administrator-merges)
permits authorized agents to perform administrator merges without repeat
consent, subject to the owner's later merge conditions; it does not by itself
waive a protected-path guard failure. See the
[current merge policy](reconciliation/auto-merge-policy.md). Documentation
inside protected paths also triggers the guard.

The guard reads null-byte (NUL) delimited paths and disables rename detection
so renaming a
protected file out of the protected set still exposes its deletion. Regressions
execute the actual workflow guard against synthetic Git repositories, including
Unicode/newline filenames. These guard tests run on Linux, matching the guard job;
Windows explicitly skips them while running the recorder tests.

## Local reproduction

Use an isolated Python 3.14 environment and install the lock the way CI does:
`python -m pip install --require-hashes --only-binary :all: --no-deps -r requirements-ci.txt`,
then `python -m pip check`. Set `AEGIS_CI_EVIDENCE_DIR` to a new
empty directory for each local attempt; otherwise the recorder defaults to
`aegis-ci` inside `RUNNER_TEMP` or the system temporary directory. Use the same
environment's `python` for the recorder and child command.

Run the commands shown in `.github/workflows/validate-skills.yml` from the repository
root. For example:

```text
python -P scripts/ci/record-check.py environment -- python -P scripts/ci/check-environment.py
python -P scripts/ci/record-check.py ci-tests -- python -P scripts/tests/test_offline_ci.py
python -P scripts/ci/record-check.py ber -- python -m unittest discover -s tools/behavioral_eval_runner/tests -p test_*.py -v
python -P scripts/ci/record-check.py delivery-control -- python -m unittest discover -s tools/aegis_delivery_control/tests -p test_*.py -v
```

Use `powershell -NoProfile -ExecutionPolicy Bypass -File
scripts/acceptance/Test-ScenarioAEvidence.ps1` for Desktop, and `pwsh -NoProfile
-File scripts/acceptance/Test-ScenarioAEvidence.ps1` for Core, each on one line.
Missing local shells are unrun coverage, not passing checks; the hosted jobs
exercise their declared shells before delivery is closed.
