# Issue #101 package 4A: host-routing preparation proposal

This is a decision packet for the owner and maintainers of the
[conversational setup backlog](aegis-setup-routing-plan.md). Package 2's
four-choice conversation and package 3's Python offline advisory contract have
shipped. Package 4's actual host proof and comparison remain pending. This
page proposes a preparation boundary; it grants no host hook, model call,
dependency installation, provider connection or measured-savings claim.
Package 4's earlier **8–16 active-hour** whole-item estimate and this
preparation packet's **1–2 active-hour** estimate are planning ranges, not
measured work. The [current backlog forecast](aegis-backlog-forecast.md#start-here--current-reading)
has a separate selected-work view and no finite total because later BER work
remains unscoped. Active-only time was not instrumented for this packet.

**Candidate surface, not selected host:** Claude Agent SDK for TypeScript.
The locally available Claude Code command-line interface (CLI) reports
`2.1.246` on 2026-09-24, but no SDK package version is pinned or installed by
this packet. SDK behavior does not prove that the CLI, editor or a consumer's
existing assistant uses the same hook path. The [source review](../evidence/setup/issue-101-package-4a-host-feasibility.md)
records the documented interface and its limits.

## Candidate refresh for the next owner decision (2026-09-25 UTC)

The earlier CLI observation is historical, not an SDK dependency pin. Public
[npm package metadata](https://www.npmjs.com/package/@anthropic-ai/claude-agent-sdk/v/0.3.281)
now identifies `@anthropic-ai/claude-agent-sdk@0.3.281` as a
**candidate**: it declares Node.js `>=18`, `claudeCodeVersion: 2.1.281`, and a
Windows x64 optional package at the same version. Its published tarball
integrity is
`sha512-JTbluTKmY3wKQPIXzeCTvz/K0FElTuQU5Y7ueLgUOBrHcks8cHlGugEgIRezffhc13WzBAqYtaY15tJ+Bfunzg==`.
The [upstream release](https://github.com/anthropics/claude-agent-sdk-typescript/releases/tag/v0.3.281)
states parity with Claude Code 2.1.281. This verifies a candidate package
identity, not the installed binary, callback behavior, or compatibility with
the owner's current CLI/editor. The SDK is governed by
[Anthropic's commercial terms](https://github.com/anthropics/claude-agent-sdk-typescript/blob/main/LICENSE.md),
not the MIT license of the separate `@anthropic-ai/sdk` API client. Review the
exact package contents, transitive licenses and lockfile before any install.

Evidence checked on 2026-09-25 UTC: `npm.cmd view
'@anthropic-ai/claude-agent-sdk@0.3.281' version engines license
dist.integrity claudeCodeVersion optionalDependencies --json` returned the
fields above without installing the package. `node --version`,
`npm.cmd --version` and `python --version` returned `v24.19.0`, `11.17.0`
and `Python 3.14.7` on the candidate Windows host. The npm license field
says `SEE LICENSE IN README.md`; the linked upstream license supplies the
commercial-terms text. These checks do not verify downloaded tarball contents.

The owner has one product-path choice before a scoped implementation grant.
Decision 1 in the list below records that choice; the later questions depend
on it:

| First host path | Benefit | Cost and limitation |
| --- | --- | --- |
| Separate SDK-managed Claude session on native Windows, recommended for an **offline prototype only** | Documented TypeScript callback surfaces let synthetic tests exercise typed `/skill` and model tool dispatch. | Adds Node/TypeScript dependencies and maintenance under the SDK's commercial terms; it does not establish that the current CLI/editor uses these callbacks. Synthetic testing can spend $0 on providers; any real session needs a later grant and may incur usage cost. |
| Current CLI/editor only | Preserves the existing-assistant experience directly. | No complete fail-closed interception path is established; more host research is needed before code or a credible time estimate. |
| Keep Aegis-only for now | No new dependency, host setup or provider spend. | Optional routing and any savings remain unavailable and unmeasured. |

Choosing a path selects a planning direction, **not** an SDK installation,
implementation, host session, provider call or release claim. If the SDK path
is selected, the proposed first profile is the existing native Windows host
with Node 24.19.0, npm 11.17.0 via `npm.cmd`, and Python 3.14.7. These tool
versions were observed locally; other operating systems remain unverified.

For review, a possible **separate Stage 4A-offline grant** would cap work at
12 active implementation hours, 1,200 added handwritten code/test lines and
$0 external spend. The 12-hour figure is a **ceiling, not an estimate** or
time already spent.
If this split scope is selected, the older 8–16-hour whole-package estimate
above cannot safely be relied on to cover Stage 4B host proof and comparison.
Reforecast package 4 as separate 4A and 4B work before implementation; 4B
remains TBD until its host and execution boundary are approved.
The hypothetical grant would permit only synthetic fixtures and these exact
candidate paths:

```text
tools/aegis_setup/host_bridge/.gitignore
tools/aegis_setup/host_bridge/package.json
tools/aegis_setup/host_bridge/package-lock.json
tools/aegis_setup/host_bridge/tsconfig.json
tools/aegis_setup/host_bridge/bridge.ts
tools/aegis_setup/host_bridge/contract_worker.py
tools/aegis_setup/host_bridge/bridge.test.ts
tools/aegis_setup/host_bridge/README.md
docs/roadmaps/aegis-setup-routing-plan.md
docs/evidence/setup/issue-101-package-4a-offline-review.md
.github/workflows/validate-skills.yml
```

That hypothetical bridge would call the shipped Python advisory contract
through bounded local stdin/stdout, inject synthetic host-owned eligibility
and policy facts, and export callback functions without starting `query()` or
a Claude process. Tests must cover direct `/skill`, model `Skill`, agent and
subagent dispatch, unknown tools/IDs, mandatory and explicit selections,
manual-only skills, stale facts, malformed/oversized frames, subprocess
failure/timeout, and no online fallback. A valid advisory result must still
pass the host's ordinary permissions; it cannot independently grant a tool
call. The existing 4,096-byte request and 1,024-byte response limits remain.
The CI workflow must run the new offline tests on the pinned package.

This is **not yet an implementation-ready grant**. The owner must first choose
the host path, and maintainers must inspect the exact SDK/native tarballs,
dependencies, license terms, integrity and lockfile, then record authority
sources for eligibility, catalog/policy versions and destinations. A later
reviewed approval must make the file list, limits and denial behavior
effective. Actual SDK callback invocation, dispatch consumption and
main/subagent token evidence remain Stage 4B host proof.

## Owner decisions needed before code

1. Select the exact host surface: an SDK-managed TypeScript session, its
   package and bundled CLI versions, operating-system profiles, and whether
   this qualifies as the user's existing coding assistant for issue #101.
   Record the exact dependency source, license and lockfile strategy. This
   repository currently has no Node package manifest or lockfile.
2. Choose the separate implementation grant's exact files, hours, added-line
   cap and zero or bounded external spend. An offline callback test cannot
   establish actual host interception. Any actual SDK session, model-backed
   call, credential or external telemetry needs its own explicit authority.
3. Define where eligibility, mandatory reviewers/skills, manual-only status,
   explicit user selections, catalog/policy versions, and destination policy
   come from in that host. A helper never supplies those authority facts.
4. Set the host acceptance profile: direct user-typed `/skill`, model-invoked
   `Skill`, `Agent`/subagent dispatch, other dispatch tools and fallback;
   identify unsupported paths rather than calling partial coverage complete.
   Pin what main/subagent token and cache usage must be observable before
   comparing complete tasks.

## Proposed two-stage proof, each separately authorized

**Stage 4A-offline: callback contract only.** After a scoped implementation
grant, implement a TypeScript host-bridge candidate that calls the shipped
`tools/aegis_setup` advisory contract through a pinned, explicitly bounded
interface. A catch-all `PreToolUse` callback should recheck host-owned
eligibility and mandatory selections immediately before `Agent` or
model-invoked `Skill` dispatch. A TypeScript `UserPromptExpansion` callback
should cover direct user-typed `/skill` commands, which bypass `PreToolUse`.
Unknown tool or ID, stale catalog/policy, missing mandatory or explicit
selection, uninvoked manual-only skill, malformed/oversized synopsis, unsafe
destination, callback exception, timeout or adapter failure must block the
proposed assisted dispatch. An Aegis-only fallback may proceed only after
the host independently rechecks its own permissions and mandatory selections;
it must not silently switch local processing online. Synthetic tests
can prove this decision logic with fake hook inputs. They cannot prove that a
real SDK session invokes or obeys the callback. `canUseTool` is not the sole
gate because prior permission approvals can skip it.

**Stage 4B-host: actual invocation and comparison.** A later grant must
authorize one pinned SDK session and verify hook invocation, decision
consumption, dispatch/fallback, direct and model-invoked skill paths,
subagents, failure behavior, and complete-task main/subagent token evidence.
Only then can package 4 compare Aegis-only rules with shortlisted local
helpers under the [predeclared protocol](aegis-setup-routing-plan.md#predeclared-evaluation-protocol-for-package-4).
An offline pass must be labeled preparation, not completed host proof.

The owner-approved package-3 grant [AEGIS-APR-008](../approvals/APPROVAL_REGISTER.md#aegis-apr-008-issue-101-offline-advisory-routing-contract)
does not cover either stage's host hook. No proposed file list here overrides
its exact boundaries or the later package-4 authorization requirement.
