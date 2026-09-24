# Issue #101 package 4A host-interface feasibility screen

Reviewed 2026-09-24 against the [issue #101 setup plan](../../roadmaps/aegis-setup-routing-plan.md),
the shipped [offline contract](../../../tools/aegis_setup/README.md), and
official [Agent SDK hooks](https://code.claude.com/docs/en/agent-sdk/hooks),
[SDK permissions](https://code.claude.com/docs/en/agent-sdk/permissions), and
[hook failure behavior](https://code.claude.com/docs/en/hooks), plus official
[usage monitoring](https://code.claude.com/docs/en/monitoring-usage).
This is source-based feasibility evidence, not an installed or exercised host.

| Question | Documented candidate finding | What remains unproved |
| --- | --- | --- |
| Before-dispatch gate | SDK `PreToolUse` callbacks can deny or modify a tool request before normal permissions. A timed-out Agent SDK callback blocks the tool request; a timed-out CLI command hook instead proceeds through normal permissions. | Hook invocation, error behavior and full tool-path coverage in a selected session. |
| Approval order | SDK `canUseTool` can be skipped when an earlier mode or allow rule approves a call. A policy gate therefore needs `PreToolUse` or another independently verified earlier boundary. | Effective permission/settings interactions on the selected host. |
| Skill paths | TypeScript SDK offers `UserPromptExpansion` for user-typed commands; model-invoked `Skill` uses the tool path. | Direct `/skill`, subagent and other host paths in an actual session. |
| Telemetry | Claude Code documentation describes token usage by main/subagent query source and token type. | Exact per-agent correlation, complete-task accounting and comparison fidelity on this version. |

Local `claude --version` returned **2.1.246**. No `package.json`, lockfile or
installed Agent SDK version was found in this repository checkout. No hook was
installed or executed; no model, provider, credential, private input or
external telemetry was used. Synthetic callback inputs could test allow,
deny, rewrite, stale policy, manual-only, timeout and fallback behavior after
a separate implementation grant. Only an authorized host session can prove
that the host actually calls and consumes the callback. The
[package 4A proposal](../../roadmaps/aegis-setup-package-4a-host-preparation-proposal.md)
keeps those evidence levels separate.
