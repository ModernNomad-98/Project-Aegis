# Issue #101 package 4A: host-routing preparation proposal

This is a decision packet for the owner and maintainers of the
[conversational setup backlog](aegis-setup-routing-plan.md). Package 2's
four-choice conversation and package 3's Python offline advisory contract have
shipped. Package 4's actual host proof and comparison remain pending. This
page proposes a preparation boundary; it grants no host hook, model call,
dependency installation, provider connection or measured-savings claim.
At this packet's start, package 4 remained estimated at **8–16 active hours**;
this separate preparation packet is estimated at **1–2 active hours**. After
PR #236, selected remaining work is **120–299 active hours**, including
**25–105** for documentation; the full optional adoption backlog has no
finite total. Active-only time was not instrumented for this packet.

**Candidate surface, not selected host:** Claude Agent SDK for TypeScript.
The locally available Claude Code command-line interface (CLI) reports
`2.1.246` on 2026-09-24, but no SDK package version is pinned or installed by
this packet. SDK behavior does not prove that the CLI, editor or a consumer's
existing assistant uses the same hook path. The [source review](../evidence/setup/issue-101-package-4a-host-feasibility.md)
records the documented interface and its limits.

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
destination, callback exception, timeout or adapter failure must deny or
abstain without silently switching local processing online. Synthetic tests
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
