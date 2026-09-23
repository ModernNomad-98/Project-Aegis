# BER selected-host R4/R5 capability decision proposal

> **Current reading, checked 2026-09-23:** The owner selected a disposable
> Unix-like host *direction*, but no named host or selected-host proof is recorded.
> This page remains a proposal; even its offline Stage A probe needs a separate
> grant. Use the [BER backlog](behavioral-eval-runner-backlog.md#start-here-status-and-routes)
> for current work-package and evidence-gate status.

**Reading key:** Behavioral Eval Runner (BER) is the evaluation tool; work
package 2B-0 (WP-2B-0) is its earlier evidence phase. Requirement R4 concerns
effective tool-path confinement; R5 concerns execution-profile observability
and isolation. POSIX is a Unix-like operating-system interface; continuous
integration (CI) is repository test automation, not selected-host proof.
Access control list (ACL), Model Context Protocol (MCP), and Secure Hash
Algorithm (SHA, used here for source identity) name technical surfaces in the
proposed probe. `NON_BASELINE` means the result cannot qualify for a measured
baseline; `UNAVAILABLE` means the named capability was not demonstrated.

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
and the R4/R5 backlog entries. No additional host is selected or provisioned.

| Candidate | Useful next evidence | Current limit / decision |
| --- | --- | --- |
| Existing Windows host | Reproduce known negative path/process result, inspect profile surface and prove denial paths without network/model dispatch | Cannot claim baseline while mid-write prevention and post-leader reaping are unproven; a Windows fix needs a separately reviewed native/host mechanism and exact tests |
| Owner-selected disposable POSIX host | Reproduce POSIX writer/process negative tests and inspect a clean execution profile on the actual chosen host | Host availability, identity, isolation, permissions, secret custody and probe authority are unknown; generic Linux CI has run but selected-host proof remains absent |

**Recommendation:** choose a specifically identified disposable POSIX host as
the *candidate for offline capability proof*, if the owner can provide or
authorize one. This is a shorter path to testing the implemented mechanisms,
not a claim that POSIX already meets R4/R5. If only Windows is available,
perform the Windows negative/profiling report and keep the live gate closed
until the missing mechanisms are implemented and proven. Do not substitute
an arbitrary CI runner for the selected deployment host.

## Proposed two-stage proof and authority

### Stage A — offline, non-model host capability probe

The owner first names host/OS/version, physical or virtual boundary, permitted
scratch root, execution account, allowed tools, and whether the existing
machine or a new disposable host is in scope. Then a *reviewed and merged
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

## Exact owner decision needed next

1. Select a named disposable POSIX host for Stage A, select the existing
   Windows host for a negative-only report, or defer until a host exists.
   Provide the OS/version, account and scratch-root boundary if selecting a
   host. A new host or access credential needs its own authorization.
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
