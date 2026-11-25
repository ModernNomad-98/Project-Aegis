# Offline verification in GitHub Actions

This guide is for contributors and reviewers checking a Project Aegis change.
It explains what the automated **continuous integration (CI)** jobs prove, how
to reproduce important checks locally, and how to interpret a failure or skip.
The jobs test skills and the **Behavioral Eval Runner (BER)** with synthetic
inputs; they do not run a live model evaluation.

## A normal verification pass

1. Run the [local checks](#local-reproduction) on the changed revision and
   record the command, result and any skip.
2. Open a pull request (PR) and wait for every job in the table below that
   runs on the pull request's latest commit (its head). `changes`,
   `validate-skills` and `gate-guard` run on every pull request to `main`;
   `windows-offline-checks` runs only when the change touches `tools/`,
   `requirements-ci.in` or `requirements-ci.txt`, and `tools-tests-linux` and
   `tools-tests-windows` only when it touches `tools/` or
   `docs/instrumentation/workflow-outcomes-v1.schema.json`, and
   `local-tool-tests` only when it touches `scripts/` or `tools/`. A later
   push starts new checks; older green results do not cover the new head.
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
every push to `main`. Inside it, a path filter decides whether four advisory
jobs run. On a pull request, the `changes` job lists the paths the pull
request changes against `main` (a three-dot `git diff --name-only` against
the base branch) and selects:

- `windows-offline-checks` only when the change touches `tools/`,
  `requirements-ci.in` or `requirements-ci.txt`;
- `tools-tests-linux` and `tools-tests-windows` only when it touches
  `tools/` or `docs/instrumentation/workflow-outcomes-v1.schema.json`;
- `local-tool-tests` only when it touches `scripts/` or `tools/`.

A job the filter does not select is skipped. A pull request that touches
none of those inputs skips all four, whatever else it changes — with one
exception: `docs/instrumentation/workflow-outcomes-v1.schema.json` is a tools
input, so a change touching only that file runs `tools-tests-linux` and
`tools-tests-windows` while `windows-offline-checks` stays skipped. Skills,
other documentation or `.github/` alone run none of the advisory jobs; a
change touching `scripts/` runs `local-tool-tests` but neither the Windows
verification job nor the tools-test jobs. On a push to
`main` the `changes` job selects all four, so the post-merge run is the
full suite. `validate-skills` and `gate-guard` have no path filter. The four
selected jobs need `changes`, so they are also skipped when `changes` itself
does not succeed; [Reading a failure](#reading-a-failure) says how to tell
the two apart. Record a skipped job as skipped, not as passed. The existing
required check names stay `validate-skills` and `gate-guard`; branch
protection is unchanged.

| Job | Coverage | Merge role | Timeout |
| --- | --- | --- | --- |
| `changes` on Ubuntu | Lists the pull request's changed paths and selects the Windows verification, tools-test and local-tool-test jobs (on a push to `main`, all four); those jobs need it, so they are skipped if it does not succeed | Not registered as required; runs on every pull request and push | 5 minutes |
| `validate-skills` on Ubuntu | CI recorder/guard regressions, validator, audit and link-checker self-tests, skill validation, BER self-check and full suite, PowerShell Core Scenario A acceptance, pull-request-only Developer Certificate of Origin (DCO) check, the Markdown link checker over the repository's own tracked pages (the corpus step, with its 600-path floor), and the pull-request body bound-field check (`Run PR-body bound-field checker self-tests` plus `pr-body-skills-check`) | Existing required check | 15 minutes |
| `windows-offline-checks` on Windows | Recorder regressions, validator, audit and link-checker self-tests, skill validation, BER self-check and full suite, sequential PowerShell Desktop 5.1 and Core acceptance | Additional visible coverage; not registered as required | 20 minutes |
| `gate-guard` on Ubuntu | Detect changes to the merge gate and its enforcement surfaces | Existing required check; PR only | 5 minutes |
| `tools-tests-linux` on Ubuntu | Host-bridge Node callback tests, setup routing-contract suite, delivery-control suite | Isolated from the gates; not registered as required | 15 minutes |
| `tools-tests-windows` on Windows | The same three suites, plus a read-only ownership diagnostic (token user, default owner, elevation, temp-root owners) recorded before the delivery-control suite | Isolated from the gates; not registered as required | 20 minutes |
| `local-tool-tests` on Ubuntu | The seven local-tool self-test suites — manifest ancestry (13 tests), evidence pack (16), scaffold (19), run-record (72), adopt (61), guard (93) and Claude adapter (104) — 378 in total. The first three run directly with `python -P -B`; the four Aegis tool suites run `python -m unittest discover` and need `python` on `PATH` and the runner's `git` binary, not a Git work tree | Advisory: path-filtered to a change under `scripts/` or `tools/`; a `.github`-only pull request cannot run it, so the post-merge push run is the binding proof; not registered as required | 10 minutes |

**Update (2026-10-15):** the two `tools-tests-*` rows above now additionally run the readability-acceptance suite (`tools/readability_acceptance/tests`), matching the workflow's `readability-tests` record-check step.

**Update (2026-11-20):** the required `validate-skills` job and the Windows
verification job above now additionally run the bound-fields hash self-tests
(`scripts/tests/test_bound_fields_hash.py`, recorded as
`bound-fields-hash-tests`) after the PR-body bound-field checker self-tests.
The two `tools-tests-*` rows above now additionally run the three issue-#1145
suites — skill-reachability (`tools/skill_reachability/tests`),
skill-preservation (`tools/skill_preservation/tests`) and plan-preservation
(`tools/plan_preservation/tests`) — matching the workflow's
`skill-reachability`, `skill-preservation` and `plan-preservation`
record-check steps. Each suite is offline and cross-platform; one
skill-preservation case needs symlink-creation privilege and skips on a host
that lacks it (an explicit UNRUN, never a pass).

**Update (2026-11-21):** the table above gains `local-tool-tests`, which runs
the three local-tool self-test suites described under
[Local tool self-tests](#local-tool-self-tests) — 48 tests in total — when a
pull request touches `scripts/` or `tools/`, and on every push to `main`.
It installs nothing (the suites import only the standard library), has no
secret and no `permissions` block, and is not a required check: it is
advisory, so a skipped run is recorded as skipped, never as passed.

**Update (2026-11-24):** `local-tool-tests` now also runs the run-record (72),
adopt (61), guard (93) and Claude adapter (104) suites — **330** tests — as four
`python -m unittest discover` steps, for **378** in the job. The adapter is
included because PR #1215 merged at `626d304`; there is no deferred increment.
The job remains path-filtered to a change under `scripts/` or `tools/`, so a
pull request that changes only `.github/` and documentation does not run it at
its final head: no pre-merge result exists for those steps, and the post-merge
push run on `main` is the binding proof that they execute.

The two verification jobs run independently, without cross-platform fail-fast,
automatic retries, quarantine or `continue-on-error`. A delivery closeout waits
for each verification job that runs on the head. Record a skipped job as
skipped, not as passed. The post-merge run on `main` runs every job except
the pull-request-only `gate-guard`, so it detects regressions there; it
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
The readability-acceptance suite (`tools/readability_acceptance/tests`) also runs in those two jobs (added 2026-10-15).
The issue-#1145 suites (`tools/skill_reachability/tests`,
`tools/skill_preservation/tests` and `tools/plan_preservation/tests`) also run
in those two jobs (added 2026-11-20).
The local-tool self-test suites (`scripts/tests/test_manifest_ancestry.py`,
`scripts/tests/test_generate_evidence_pack.py` and
`scripts/tests/test_scaffold_skill.py`) run in the separate
`local-tool-tests` job (added 2026-11-21) for the same reason, although their
paths are inside the `gate-guard` set: that job is advisory, shares no runner
with a gate, and the suites are test code, not gate code.
The four Aegis tool suites (`tools/aegis_run/tests`, `tools/aegis_adopt/tests`,
`tools/aegis_guard/tests` and `tools/aegis_claude/tests`) also run in
`local-tool-tests` (added 2026-11-24). They are outside the `gate-guard` set,
so the same isolation rule applies.

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
coverage, and a delivery closeout waits for them, as for the Windows job,
whenever they run.

## The aegis-verdict-gate workflow (C1.1b)

The C1.1b slice adds one dedicated workflow,
`.github/workflows/aegis-verdict-gate.yml`, with one job,
`aegis-verdict-gate`. It is **non-required evidence**: it publishes the commit
status context `aegis-verdict-gate`, but branch protection does not register
that context. Stage 3 registration is an owner action behind T4/T6/T24/T7 and is
not performed by this change. Readiness is not merge authority.

### Default-branch execution and base-only checkout

The workflow is triggered by `pull_request_target` (`opened`,
`synchronize`, `reopened`, `edited`) and `issue_comment` (`created`,
`edited`, `deleted`). Both events execute the workflow definition from the
default branch; a pull request cannot change the workflow that evaluates it, and
no pull-request head ref is checked out or executed. The checkout is base-only:
the pull request's base SHA for `pull_request_target`; for `issue_comment` the
default branch first (to run the adapter), then the resolved base SHA. The
adapter resolves the pull request read-only, and the fetch phase fails closed
with `BASE_MISMATCH` unless the working tree is the resolved base. The job
records `github.workflow_ref` and `github.workflow_sha`
and refuses to run unless the executed file is the default-branch
`aegis-verdict-gate.yml`.

The workflow has no `push`, `workflow_dispatch` or `workflow_run` trigger and
no `continue-on-error`; it has one deliberate job-level operator switch,
`AEGIS_VERDICT_GATE`. When the variable is unset (the default) the job is
**skipped**: it publishes **no commit status** and **evaluates nothing**. The
skipped run is itself recorded by Actions — run id, event, ref, conclusion
`skipped` — so the accurate statement is that it leaves **a record that no
evaluation occurred**; it is not evidence of a verdict, and it is not the
absence of a record. A skipped job is neutral in the UI but is **not a pass**:
GitHub may treat a skipped required check as satisfied, which is why this job
must never be registered as required. When enabled with no valid signed
attestation, the job posts a **failure** naming `REQUIRED_INPUT_UNAVAILABLE`;
that failure is evidence about the input, not a merge gate, and no unrelated
merge is blocked by it. Enable the variable only when B/D/E records and T6/T24
authority exist; it is not automatic record detection.

The signed attestation is a **planned** contract, described in
[delivery-workflow.md](delivery-workflow.md#the-planned-stage-attestation-contract);
no verifier, signing key or gate argument for it exists in this repository, and
this page describes only the shipped neutral state.

### Adapter, checker and publisher

1. `scripts/ci/aegis_verdict_gate_fetch.py` is a read-only provider adapter.
   It reads `GITHUB_TOKEN` from the environment, the event payload, the pull
   request, its issue comments and its commits, and writes the C1.1a input
   envelopes (`verdict.json`, `freeze.json`, `settlement.json`,
   `head-history.json`, `stage-records/`) plus `gate-context.json`,
   `provenance-manifest.json` and `adapter-result.json` under
   `RUNNER_TEMP`. Every envelope is re-read with the moved package's own
   `inputs.load_envelope` validator. The adapter never decides readiness and
   never defaults a required field to true: a field without a trustworthy
   source is omitted and listed in `adapter-result.json` as unavailable, so
   the checker reports `REQUIRED_INPUT_UNAVAILABLE` or the specific canonical
   blocker. The head-history export is always `UNVERIFIED` because the
   read-only provider cannot establish a complete published-head sequence. It
   does not synthesize owner-assigned identifiers or free-form PR-body fields,
   so a run can be blocked with `REQUIRED_INPUT_UNAVAILABLE` (or a canonical
   blocker) until those records are supplied: that is fail-closed evidence, not
   a readiness claim.
2. `scripts/aegis_verdict_gate/run.py` runs the merged C1.1a checker from
   the base-only checkout; it is the only decision-maker.
3. `scripts/ci/aegis_verdict_gate_publish.py` is the only write path. It
   validates the repository, pull request and head against the evaluated
   inputs, re-reads the pull request, refuses a head that has moved or a
   foreign, closed or non-PR change, and posts **exactly one** commit status
   (context `aegis-verdict-gate`) on the resolved head: `success` only
   when the checker exited 0 *and* reported readiness true; `failure` for a
   blocked or invalid result; `error` otherwise. It never posts `pending`,
   never retries, and exits nonzero on a refusal or provider failure, leaving
   no success status. A non-pull-request issue comment is a recorded no-op: no
   status and exit 0.

The token is read only from `GITHUB_TOKEN`, never passed as an argument,
never written to an artifact and never printed. The job's permissions are
`contents: read`, `pull-requests: read`, `issues: read` and
`statuses: write`. GitHub Actions permissions are job-scoped, not
step-scoped, so the single job holds `statuses: write`; only the
`publish-status` step invokes the publisher, and the isolation tests assert
that no other step names the writer or a status endpoint.

### Evidence and isolation coverage

The job records `environment`, `resolve`, `fetch-inputs`,
`verdict-gate`, `publish-status`, `self-test` and `checker-tests` with
`scripts/ci/record-check.py` (distinct lowercase labels), writes a job summary
naming readiness, blockers, assurance and the published state, and retains
`$RUNNER_TEMP/aegis-ci/` and the run directory with 14-day retention.

`scripts/tests/test_offline_ci.py` parses the new workflow separately from
`validate-skills.yml` and asserts: the exact trigger set; one job that always
runs; the exact permissions map with `statuses` as the only write scope;
exactly one base-only checkout that never names a head ref; SHA-pinned actions;
`bash` only; `python -P` for every Python call; distinct lowercase evidence
labels; no Node, npm, tools suite or pip install; and no gate-isolation
violation. Mutation tests prove each new check fails on an unpinned action, an
unguarded path, a loader variable, a widened write permission, a `push`
trigger, a head-ref checkout and a Node step. The existing `validate-skills`
gate-job assertions and thresholds are unchanged.

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
pinned to the verified `actions/upload-artifact` v7.0.2 commit
`cf430e030ddbb5b0abf93d22962f4752f3646cd9`; checkout and setup-python retain their
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
| Every job is cancelled at the same moment | When the durations match none of the jobs' own timeouts, this is the infrastructure-flake signature documented on the `changes` job in `.github/workflows/validate-skills.yml`: re-run the workflow on the same head. A cancelled run is not a pass. |
| Protected-file guard fails | A changed path needs deliberate manual review and merge. The guard is reporting its intended condition; it was not bypassed or made green. Follow the owner approval register and current merge policy. |
| Capability test skips | That capability was not exercised on this host. Keep the skip in the closeout and seek another host or proof when required. |
| An advisory job is skipped | Check the `changes` job first. If it failed, timed out or was cancelled, every job that needs it is skipped too, and that failure is the finding to fix. Otherwise the path filter did not select the job for this pull request. Either way the job did not run: record a skipped job as skipped, not as passed. The post-merge run on `main` selects it. |

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
`python -m` runs of `tools.behavioral_eval_runner`, `unittest` and the
Windows tools job's ownership diagnostic need the checkout root on the import
path, so they cannot use `-P`; in the gate jobs, the guard's root-level
protection covers them instead.
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
consent, subject to the owner's later condition that local tests and GitHub
Actions checks are green
([AEGIS-APR-013](approvals/APPROVAL_REGISTER.md#aegis-apr-013-later-condition-on-standing-administrator-merges),
[AEGIS-APR-048](approvals/APPROVAL_REGISTER.md#aegis-apr-048-standing-administrator-merge-once-checks-are-green));
it does not by itself
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
empty directory for each local attempt; otherwise the recorder uses
`aegis-ci` under a set `RUNNER_TEMP`, or a unique per-run directory under the
system temporary directory. Use the same
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

## Manifest ancestry pre-push check

The skills manifest (`tools/skills-manifest.json`) records the commit whose
skill content it describes in `source_revision`. Prove that revision is part
of this branch's history before pushing:

```text
python -P scripts/check-manifest-ancestry.py
python -P scripts/check-manifest-ancestry.py --json
```

`--repo-root` defaults to `.`; `--manifest` defaults to
`tools/skills-manifest.json` and is resolved against the repository root. An
absolute path, or one containing a `..` component, is rejected. `--json`
prints the result's `status`, `source_revision`, `head` and `reason`
fields.

The check proves one narrow fact: the recorded revision is an ancestor of
`HEAD`. PASS means `git merge-base --is-ancestor <source_revision> HEAD`
exited 0. FAIL means the revision is a commit in this repository but not an
ancestor of `HEAD`, or is not a commit at all. The check does not prove that
the manifest hashes match the working tree; `scripts/validate-skills.py`
checks the manifest content.

Exit codes:

- `0` PASS: the recorded revision is an ancestor of `HEAD`.
- `1` FAIL: the recorded revision is not an ancestor of `HEAD`, or is not a
  commit in this repository.
- `2` ERROR: the manifest is missing, unreadable or invalid; `HEAD` cannot
  be resolved; Git cannot run; or history is shallow. Argument-parsing usage
  errors also exit `2`.

A shallow clone is always ERROR (`history is shallow; ancestry cannot be
proven`), never PASS or FAIL: truncated history cannot distinguish a missing
ancestor from a revision that never existed.

**No git hook is installed.** This is a MANUAL command run by hand before
pushing, not a hook and not a CI gate; nothing runs it automatically. Wiring it
into CI would need a protected `.github/` change and a separate owner grant.

## Evidence pack (generated facts)

Auditors re-measure mechanical facts (commit identities, changed-file hashes
and line counts, manifest provenance) in prose and find stale numbers.
Generate those facts once instead:

```text
python -P scripts/generate-evidence-pack.py --base origin/main \
    --gate-pattern '^scripts/' --gate-pattern '^docs/' \
    --plan docs/offline-ci.md --out ../evidence-pack.json
```

`--repo-root` defaults to `.`; `--base` is required; `--head` defaults to
`HEAD` and must resolve to the commit the working tree has checked out;
`--manifest` defaults to `tools/skills-manifest.json` and must be
repository-relative (an absolute path or one containing `..` is rejected);
`--plan` optionally hashes one more file, and an absolute path is recorded
relative to the repository root; `--gate-pattern` repeats. `--out` is
required, must be outside the repository, and needs `--force` to replace an
existing file.

The pack records the schema (`aegis.evidence-pack/1`) and a status, the
resolved base and head commits and their merge base, and for each changed path
its status, mode, added/deleted line counts and, for regular files, its
sha256, byte count and line count. Deleted files and symlinks or submodules
record nulls for the content facts. It also records the manifest's
working-tree sha256 and the manifest-ancestry result verbatim, reusing
`scripts/check-manifest-ancestry.py`; the caller's gate patterns and the
changed paths each matched; and the optional plan file's sha256/bytes/lines.

Two runs with the same inputs produce byte-identical JSON: there are no
timestamps, run ids or absolute repository paths. Blob content is read as
bytes from the named commit, so a binary file and a path containing a tab or
non-ASCII characters are recorded without text conversion.

Gate patterns are caller-supplied. The workflow that invokes the generator
owns the real pattern; the pack records the pattern it was given verbatim and
the paths it matched, so a pack cannot by itself assert which gate should have
run.

The generator runs no shell commands and no repository hooks or scripts: it
invokes Git only as an argument list (`shell=False`, 60 second timeout) and
imports the repository's `scripts/check-manifest-ancestry.py` in-process,
calling `check_manifest_ancestry` for the manifest fact (that module issues
its own Git calls). It has no network access and writes nothing except
`--out`. It is a local/PR aid, not a CI gate: nothing runs it automatically,
and its output is evidence for a reviewer. Wiring it into CI would need a
protected `.github/` change and a separate owner grant. Exit `0` means the
pack was written, even when the recorded ancestry result is `FAIL` or
`ERROR`; exit `2` means the pack could not be generated.

## Local tool self-tests

Seven self-test suites cover the local tools added for the process-overhead work: three script suites and four Aegis tool suites. They run in the advisory `local-tool-tests` job when a change touches `scripts/` or `tools/`, and that job is path-filtered and not a required check, so also run them by hand before changing those tools or their docs:

- `python -B -P scripts/tests/test_manifest_ancestry.py` — 13 tests for `scripts/check-manifest-ancestry.py`.
- `python -B -P scripts/tests/test_generate_evidence_pack.py` — 16 tests for `scripts/generate-evidence-pack.py`.
- `python -B -P scripts/tests/test_scaffold_skill.py` — 19 tests for `scripts/scaffold-skill.py`.

All 48 passed locally on `main` at `1a871a48` (2026-11-20). The job is advisory coverage, not a substitute for a required check. The scaffold generator itself is documented under "Scaffolding" in [agent-speed-protocol.md](agent-speed-protocol.md#scaffolding); this page covers the ancestry checker and the evidence pack.

### Aegis tool suites (added 2026-11-24)

Four Aegis tool suites also run in `local-tool-tests`:

- `python -m unittest discover -s tools/aegis_run/tests -v` — 72 tests for the run record.
- `python -m unittest discover -s tools/aegis_adopt/tests -v` — 61 tests for adopt.
- `python -m unittest discover -s tools/aegis_guard/tests -v` — 93 tests for the guard.
- `python -m unittest discover -s tools/aegis_claude/tests -v` — 104 tests for the Claude adapter.

They need `python` on `PATH` and the runner's `git` binary; they do not need the
checkout to be a Git work tree. The adapter's 104 tests arrived with PR #1215
(merge `626d304`), so no later increment is required. All 330 Aegis tool-suite
tests were measured at `626d304` on Windows 11 / CPython 3.14.7 and Ubuntu
24.04 / CPython 3.12.3. Because the job is path-filtered to `scripts/` or
`tools/`, a pull request that changes only `.github/` and documentation cannot
run these steps at its final head; the post-merge push run on `main` is the
binding evidence for this wiring.

## Review packet (machine-readable)

`scripts/build-review-packet.py` records the mechanical facts of one pull
request as JSON: the base and head commits, the optional PR number, the body's
size and bound-fields hash, and every reported check run with the required
checks resolved. It is offline and deterministic, and it is a reviewer aid,
not a gate: nothing runs it automatically.

```text
python -P scripts/build-review-packet.py --body body.md \
    --head 0123456789abcdef0123456789abcdef01234567 \
    --base f37fd8f43b1a974d8700014246c0466a837f88c9 \
    --checks checks.json --pr 123 --out ../review-packet.json
```

`--checks` is required, so a packet can never assert an assumed check state.
`--required` names the checks that must pass; it is repeatable and defaults to
`gate-guard` and `validate-skills` (passing it replaces the default list).
`--pr` is optional and must be a positive integer. An existing `--out` is
refused unless `--force` is given, and its parent directory must exist.

`--checks` accepts a JSON list of check-run objects or the `gh api` shape
`{"check_runs": [...]}`. Each object has a string `name`, and `status` and
`conclusion` values that are strings or null.

The packet uses schema `aegis.review-packet/1` and these fields:

- `pr`, `head`, `base` — the pull request number (or null) and the two
  40-character lowercase hexadecimal commit ids.
- `body` — `bytes`, `lines`, `sha256` and `bound_fields` (`hash16`,
  `sha256`, `method`, `tool`, `version`), the five bound-field values
  reused from `scripts/ci/bound_fields_hash.py`'s `report(text)`.
- `checks.entries` — every check-run entry as `name`, `status`,
  `conclusion` and the derived booleans `is_success` and `is_failure`.
- `checks.required` — one record per required name with `name`, `present`
  and `success`.
- `checks.all_required_success` — true only when every required name is
  present and successful.
- `checks.failures`, `checks.skipped`, `checks.cancelled` — unique, sorted
  name lists.

Only the literal conclusion `success` is a success. A null conclusion is
recorded as `pending`; `neutral`, `stale`, `queued`, `in_progress`,
`cancelled`, `skipped` and any unlisted conclusion are not success.
`failure`, `timed_out`, `action_required` and `startup_failure` are the
failure conclusions. Duplicate names are all kept, and a name counts as a
success only when every entry for it is `success`; one non-success duplicate
fails the name. A required name that is missing fails
`all_required_success`.

A body must be strict UTF-8 and contain the three bound-field sentinels
(witness, skills, security); an invalid or unterminated body is an input
error. Errors print one line and exit 2; success exits 0.

Two runs with the same inputs produce byte-identical output: there are no
timestamps, run ids or absolute paths, keys are sorted, and the file uses LF.
The builder makes no network calls and starts no subprocesses; it imports the
bound-fields module in-process and writes nothing except `--out`.

The suite `scripts/tests/test_build_review_packet.py` covers the packet shape
and these rules; run it with
`python -B -P scripts/tests/test_build_review_packet.py`.
