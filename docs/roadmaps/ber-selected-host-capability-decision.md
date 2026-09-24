# BER selected-host R4/R5 capability decision proposal

**Reading key for owner and host reviewers:** Behavioral Eval Runner (BER) is
the evaluation tool; work
package 2B-0 (WP-2B-0) is its earlier evidence phase. Requirement R4 concerns
effective tool-path confinement; R5 concerns execution-profile observability
and isolation. POSIX is a Unix-like operating-system interface; continuous
integration (CI) is repository test automation, not selected-host proof.
Access control list (ACL), Model Context Protocol (MCP), and Secure Hash
Algorithm (SHA, used here for source identity) name technical surfaces in the
proposed probe. `NON_BASELINE` means the result cannot qualify for a measured
baseline; `UNAVAILABLE` means the named capability was not demonstrated.
Operating system (OS) means the selected host platform; `BER-DEC` identifies
an entry in the runner decision log. Stage A is the proposed offline host
probe without model or provider calls.

> **Current reading, checked 2026-09-24:** The owner selected a **new disposable
> Linux virtual machine under their control** as the Stage A candidate. No
> machine identity, configuration, provisioning approval or selected-host proof
> is recorded.
> This page remains a proposal; even its offline Stage A probe needs a separate
> grant. Use the [BER backlog](behavioral-eval-runner-backlog.md#start-here-status-and-routes)
> for current work-package and evidence-gate status.

Prepared 2026-09-23 from public `main` at
`75d1e6e662ed48f0ec9f6b04c4c52e6f39ead319`. **Decision proposal only.**
The [BER backlog](behavioral-eval-runner-backlog.md) records the WP-2B-0
R4/R5 *dispositions* as DONE under accepted Outcome B, with effective
confinement and profile isolation INCOMPLETE/BLOCKED. This proposal does not
reopen WP-2B-0 or change those historical statuses. Later-phase live
eligibility remains blocked until new host evidence is reviewed. The
[execution handoff](aegis-efficient-execution-handoff-2026-09-23.md) and
[open-decision index](aegis-open-decisions-2026-09-23.md) call for a selected
host and a fresh, separately authorized proof.

## Verified starting point and candidate choice

The current Windows checkout has a real runtime report. The BER evidence
writer's retained no-follow descriptor writer is POSIX-only; its Windows
path cannot prevent a mid-write ancestor/reparse swap. The supervised-process
report records Windows `taskkill /T` while the leader lives, but
post-leader descendant reaping is `UNAVAILABLE`. Linux GitHub Actions runs
the complete offline BER suite, including POSIX-specific synthetic writer
tests. Those CI results are not a reviewed R4/R5 capability proof on a
selected deployment host. The source's older `UNRUN` labels describe the
original local Windows work package and require this date-aware reading.
R5 configuration existence checks are partial; no complete profile isolation
has been demonstrated. These limits are recorded in
[`evidence.py`](../../tools/behavioral_eval_runner/evidence.py),
[`process_control.py`](../../tools/behavioral_eval_runner/process_control.py),
and the R4/R5 backlog entries. The owner chose a new disposable Linux virtual
machine as the candidate; none has been identified or provisioned.

| Candidate | Useful next evidence | Current limit / decision |
| --- | --- | --- |
| Existing Windows host | Reproduce known negative path/process result, inspect profile surface and prove denial paths without network/model dispatch | Cannot claim baseline while mid-write prevention and post-leader reaping are unproven; a Windows fix needs a separately reviewed native/host mechanism and exact tests |
| Owner-selected disposable POSIX host | Reproduce POSIX writer/process negative tests and inspect a clean execution profile on the actual chosen host | Host availability, identity, isolation, permissions, secret custody and probe authority are unknown; generic Linux CI has run but selected-host proof remains absent |

**Chosen candidate direction:** a new disposable Linux virtual machine under
the owner's control. Its identity, configuration, provisioning and probe
authority remain pending. This is a path to testing the implemented mechanisms,
not a claim that Linux already meets R4/R5. Do not substitute an arbitrary CI
runner for the selected deployment host.

## Proposed two-stage proof and authority

### Stage A — offline, non-model host capability probe

The owner next specifies the new Linux virtual machine's host identity,
OS/version, virtual boundary, permitted scratch root, execution account and
allowed tools. Then a *reviewed and merged
BER-DEC follow-up* may authorize one bounded read-only configuration inventory
and synthetic temporary-fixture probe. It should pin the runner source and
test commands, run only in the named disposable root, record host/version and
sanitized evidence, and stop on any path/ACL/identity ambiguity. No eval corpus,
private holdout, provider request, credential, package install, deployment,
or paid provisioning is implied by this proposal.

| Stage A proof | Expected disposition |
| --- | --- |
| Evidence writer under root/parent/leaf swaps, symlink/reparse/hardlink/rename races, interruption and cleanup | `VERIFIED` only for paths actually prevented or contained on the named OS; otherwise `UNAVAILABLE`/`NON_BASELINE` with exact failure |
| Supervised process with leader exit, live descendant, timeout and emergency stop | Verify creation-bound tree cleanup and no surviving descendant; an unobservable tree remains `UNAVAILABLE` |
| Ownership marker, exact-root cleanup, ACL/permission and encrypted external root where selected | Record exact reader and volume mechanism; unknown ACL/encryption state stops evidence production |
| R5 config surface: managed/user/project/local settings, all `CLAUDE.md` scopes, memory, user/project skills and agents, plugins, hooks, MCP, permission/sandbox/tool rules, executable path/hash, adapter version, configuration-home identity, environment-variable allowlist, managed-policy identity and runtime/update state | For each item, record observed version, isolation mechanism and whether it can affect the test session; unobservable or inherited state makes affected runs `NON_BASELINE` |

Stage A is a capability report, not full R4. The report records commands,
synthetic fixtures, negative results, exact source SHA, host fingerprint that
does not expose private identifiers, reviewer disposition, skipped probes and
known limitations. Publish only a sanitized summary in Git; keep raw host
evidence in the approved external root under its own access/retention rules.

### Stage B — bounded effective tool-path proof, later decision

R4's actual requirement is confinement **through every enumerated agent tool
path**, not only shell or Python unit tests. A later, separate authorization
must pin the exact host/adapter and profile, source/evidence root, synthetic
probe tasks, model/provider and call/token/dollar ceilings before any
model-driven session. Probe shell/subprocess, built-in Read, Edit/Write,
WebFetch/network, MCP, plugins, hooks, subagent permissions, unsandboxed
commands, excluded commands and merged effective permission rules. Test
control-plane eval-corpus inaccessibility without exposing real expectations
to the agent. Prove workspace-only writes, read-only corpus, caller-directory
inaccessibility, no provider credentials in the sandbox, deny-by-default
egress, bounded process lifetime and tree-wide emergency kill. An unsupported
path blocks broad live dispatch or the adapter; a narrower claim requires an
explicit owner choice after actual evidence. R5 must bind the fully observed
and isolated profile into each run's baseline identity.

The Stage B probe is still not WP-2B-4's live scenario suite and does not
approve calibration labels, renewed WP-2B-3 spending, BER evidence policy, or
CP execution. Each has its own authority and prerequisite. No approval of a
model-driven call is requested by this document.

## Source-only Stage A test plan — prepared 2026-09-24

This is a **candidate command and evidence plan**, not permission to execute
on a host. The selected host, operating-system version, execution account,
owned absolute scratch root, source revision, Python version, evidence access,
duration and exact command list must first be named in a separate reviewed
and merged BER-DEC Stage A grant. The commands below refer to tests already
in this repository; a later grant must pin their exact source SHA and arguments.
Generic CI success does not substitute for a run on that chosen host. The
proposed host run would put every synthetic temporary path inside the approved
root, including `TMPDIR`/`TMP` and Windows `TEMP` if that negative-only option
is later selected, and stop if that confinement cannot be shown.

| Candidate command from pinned repository root | Required observation and limit |
| --- | --- |
| `python -B -m tools.behavioral_eval_runner version` | Capture the runner version. Record Python, adapter and host versions separately in the later authorized host inventory. |
| `python -B -m tools.behavioral_eval_runner capabilities` | Capture source-reported statuses, including `UNRUN`, `UNAVAILABLE` and `NON_BASELINE`; this command does not report runner version or attest to the selected host. |
| `python -B -m unittest tools.behavioral_eval_runner.tests.test_evidence.TestEvidenceWriterTrustedRoot -v` | Symlinked evidence roots and POSIX parent swaps fail closed; no outside write. The POSIX parent-swap case must run, not skip, if selected. |
| `python -B -m unittest tools.behavioral_eval_runner.tests.test_review_blockers.TestMaterializationWriteReparse tools.behavioral_eval_runner.tests.test_materialize.TestSyntheticMaterialization.test_empty_area_swap_cannot_redirect_creation -v` | Synthetic parent/area-root and reparse/symlink swaps cannot redirect writes; no outside file appears. Required POSIX swap cases must run. |
| `python -B -m unittest tools.behavioral_eval_runner.tests.test_process_control.TestProcessTreeKill tools.behavioral_eval_runner.tests.test_review_blockers.TestSupervisorDescendantCleanup -v` | Check watchdog timeout, leader termination and fail-closed handling of an unobservable tree. `test_posix_background_child_terminated_after_leader_exit` independently checks one background child's process ID after its leader exits and must run on the selected POSIX host. The timeout test does not independently check the grandchild ID on POSIX, and one child fixture cannot prove every escape or descendant path. Record process IDs only in protected raw evidence. |
| `python -B -m unittest tools.behavioral_eval_runner.tests.test_execution_profile tools.behavioral_eval_runner.tests.test_review_blockers.TestExecutionProfileIsolation tools.behavioral_eval_runner.tests.test_review_blockers.TestExecutionProfileDerivedClaims tools.behavioral_eval_runner.tests.test_containment -v` | Missing or inherited profile fields prevent baseline eligibility; synthetic containment denies disallowed reads and egress. Mocks cannot prove the real selected profile or effective agent tool paths. |
| No candidate command yet for hardlink, leaf-rename and interrupted-write cases in the Stage A proof table above | Record `NOT_RUN` for each until the exact host grant names a reviewed synthetic fixture and expected negative result. These gaps cannot be inferred from passing parent/root swap tests. |

The later grant should name all five required POSIX test IDs explicitly:
`test_posix_parent_swap_fails_closed`,
`test_posix_area_root_swap_fails_closed`,
`test_posix_parent_swap_between_check_and_open_fails_closed`,
`test_empty_area_swap_cannot_redirect_creation`, and
`test_posix_background_child_terminated_after_leader_exit`. A skip of any
required case is an unmet proof, not a pass.

Entry criteria for any later host execution are an exact approved host/account
and scratch-root boundary, a pinned signed source commit and tree, approved
synthetic fixture/command list, evidence readers and retention, and a stop
rule for unclear path, identity, access-control list, encryption or key custody.
The later host reviewer must also perform a separately authorized read-only
inventory of the actual R5 configuration surfaces listed above: managed,
user, project and local settings; every `CLAUDE.md` scope; memory, skills,
agents, plugins, hooks and Model Context Protocol servers; sandbox, tool and
permission rules; executable path/hash, adapter version, configuration home,
environment allowlist, managed-policy identity and update state. Existing
`synthetic_isolated_profile` fixtures and `RealHostContainment` capability
reports do not establish these facts. No installation, credential or provider
call is part of this source-only plan.

The sanitized `stage-a-capability-summary/v1` record would contain: grant ID;
exact source commit/tree and runner/adapter/Python versions; an owner-assigned
host alias whose real identifier remains outside Git; OS/version and disposable
boundary class; scratch-root alias; UTC start/end; each approved command's
exit status, test count, skips and skip IDs, elapsed time and sanitized output
digest; an R4/R5 row with observed mechanism, `VERIFIED`, `UNAVAILABLE`,
`UNKNOWN` or `NOT_RUN`, limitation and protected-artifact reference; the R5
configuration inventory with source/isolation/impact; and an independent
reviewer disposition. Raw host paths, process IDs, users, secrets and evidence
stay in the separately approved external root under its access and retention
rules. A missing fact remains unknown in the public summary.

Stop and preserve the synthetic evidence on a source/root/account mismatch,
path escape, unresolved ACL or encryption fact, unexpected network/provider/
credential/private access, nonzero test, required POSIX skip, surviving child,
or inherited/unisolated R5 configuration. The one-child POSIX no-survivor
test above supports only its observed fixture; broader descendant/escape
paths require a separately named host-specific observation. Such a result is
`NON_BASELINE` or
`UNAVAILABLE`, not a partial pass. Passing these offline cases could support
a **Stage A capability observation only**. Effective Read/Edit/Write,
WebFetch/network, MCP, plugin, hook and subagent confinement requires the
separate model-driven Stage B authorization and proof.

## Exact owner decision needed next

1. The owner selected a new disposable Linux virtual machine under their
   control as the Stage A candidate in the Project Aegis conversation on
   2026-09-24. Specify its virtualization platform, OS/version, account,
   isolation boundary, permitted scratch root and allowed tools; separately
   authorize any provisioning or access credential. This choice alone grants
   no host operation.
2. After selection, review a BER-DEC Stage A grant with exact commands,
   source pin, root, evidence handling, time ceiling and stop conditions.
   The current proposal does not authorize even a read-only host probe on a
   newly provisioned machine.
3. Use Stage A results to decide whether to prepare a Stage B model-driven
   authorization, remediate the host, or mark it unsuitable. Preserve
   `NON_BASELINE` and blocked live status until the full evidence is accepted.

The host choice changes the critical path and should trigger an early backlog
forecast review. No current ETA for R4/R5 can include unknown provisioning or
owner waiting as though it were active engineering time.
