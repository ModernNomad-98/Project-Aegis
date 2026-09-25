# Issue #101 package 4A host-interface feasibility screen

Reviewed 2026-09-24 against the [issue #101 setup plan](../../roadmaps/aegis-setup-routing-plan.md),
the shipped [offline contract](../../../tools/aegis_setup/README.md), and
official [Agent software development kit (SDK) hooks](https://code.claude.com/docs/en/agent-sdk/hooks),
[SDK permissions](https://code.claude.com/docs/en/agent-sdk/permissions), and
[hook failure behavior](https://code.claude.com/docs/en/hooks), plus official
[usage monitoring](https://code.claude.com/docs/en/monitoring-usage).
This is source-based feasibility evidence, not an installed or exercised host.
CLI means command-line interface.

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

## 2026-09-25 package and callback follow-up

The owner selected a separate SDK managed Windows session as the **planning
target for an offline prototype**. This does not select the currently
installed CLI/editor as a supported host or authorize a package installation
or session. The proposed SDK wrapper is `@anthropic-ai/claude-agent-sdk@0.3.281`;
its manifest identifies bundled Claude Code `2.1.281`, which differs from the
locally observed CLI `2.1.246`.

Public npm metadata and archives were inspected without install or execution.
The SDK archive matched registry SHA-512 integrity
`sha512-JTbluTKmY3wKQPIXzeCTvz/K0FElTuQU5Y7ueLgUOBrHcks8cHlGugEgIRezffhc13WzBAqYtaY15tJ+Bfunzg==`.
The Windows x64 `0.3.281` archive matched
`sha512-hbnymWj9O31K0VMd/VOpMTZ0CNT3BkwgGGe84zHdAP6MDxmoZvqyS94UEaLQit3xmozCxfkfGns7/WgWH1Q6Sg==`.
Its 240,767,648-byte `claude.exe` matched the SDK manifest SHA-256
`39be063c2512b43347fe7b0ab18c46f1596141701c9c5fc895ddfca9a051067c`.
The SDK manifest names build 2026-09-23 and commit
`3e320108de6831eb996e9a3f7795152073cc0d0c`. Neither inspected package
declares an install script or ordinary `dependencies` entry. The SDK declares exact
`0.3.281` platform packages and peer ranges for `@anthropic-ai/sdk >=0.93.0`,
`@modelcontextprotocol/sdk ^1.29.0`, and `zod ^4.0.0`. Compatible registry
examples `0.128.0`, `1.30.1`, and `4.6.5` do not fix the actual transitive
tree; the Model Context Protocol (MCP) peer alone declares 16 direct
dependencies. Both inspected
archives point to Anthropic commercial terms; the three peer examples declare
MIT. Registry signatures were observed but not cryptographically validated.
The manifest's explicit tested-wrapper list ends at `0.3.280`. No exact
wrapper/CLI runtime compatibility is claimed from this metadata.

Before installation, generate and independently review a lockfile with exact
versions and integrity for every resolved node, and separately inspect each
resolved package manifest/archive for licenses and lifecycle scripts.
Then use `npm ci --ignore-scripts` in an isolated test fixture, after a
separate Stage 4A implementation grant. Do not execute the bundled binary in
Stage 4A. The 240 MB closed-source executable remains a later host execution
trust boundary.

In a temporary directory, `npm.cmd install --package-lock-only
--ignore-scripts --no-audit --no-fund --save-exact` generated a version-3
candidate lock with SDK `0.3.281`, Anthropic API SDK `0.128.0`, MCP SDK
`1.30.1` and Zod `4.6.5` as exact roots. It resolved 110 dependency entries
besides the root record, including eight optional platform binaries; all 110
dependency entries have integrity and license fields. SHA-256 of this
temporary lock was
`DC869BD02F2FF679FB91C26CED5C7670DDB2156F91744A972D05E64D1D906DF7`.
The 110 metadata license fields were 90 MIT, eight Anthropic binary
references, one Anthropic SDK reference, seven ISC, two BSD-3-Clause, one
BSD-2-Clause and one Unlicense. All 110 exact public registry manifests were
read; none declared `preinstall`, `install` or `postinstall`. Some declared
publish-time scripts, so `--ignore-scripts` remains prudent. The candidate
contains `@hono/node-server@2.1.1`, whose Node.js `>=20` requirement is the
highest declared minimum across all 110 resolved entries (76 declare a Node
constraint and 34 do not). Thus this lock's effective **declared** minimum is
20, above the top-level SDK's `>=18`. Local Node 24.19.0 meets it. No
`node_modules` directory was created, and this
metadata check did not audit all package bodies or prove runtime compatibility.

Official [SDK hooks](https://code.claude.com/docs/en/agent-sdk/hooks),
[permissions](https://code.claude.com/docs/en/agent-sdk/permissions), and
[skills](https://code.claude.com/docs/en/agent-sdk/skills) explain that
`PreToolUse` applies to model `Skill` and `Agent` dispatch, while TypeScript
`UserPromptExpansion` covers a directly typed `/skill`. A direct command can
still run when its skill is absent from the model-facing allowlist. Earlier
permissions can skip `canUseTool`. The documented timeout blocking does not
establish every callback-exception outcome, so a candidate bridge must catch
errors and return a denial explicitly. No callback was registered or invoked.

The shipped Python contract checks bounded request/advice shape and selection
preservation, but it does not authenticate host-supplied eligibility, mandatory
reviewers, explicit choices, manual invocation, catalog or policy currency,
destination, or ordinary permissions. Stage 4A can use fresh **synthetic**
host-owned snapshots to test denial before each proposed dispatch. Stage 4B
must identify real sources and prove real callback invocation, consumption,
full dispatch coverage and complete-task main/subagent telemetry.
