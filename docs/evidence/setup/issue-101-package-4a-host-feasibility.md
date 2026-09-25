# Issue #101 package 4A host-interface feasibility screen

**2026-09-25 status update:** This page preserves its source-screening
snapshot and the then-pending statements below. The separate bounded Stage 4A
offline bridge later merged in [PR #281](https://github.com/ModernNomad-98/Project-Aegis/pull/281)
as `ea40ab481ff78267cd5f151c393e946805ba8d01` at 07:43:44 UTC;
[APR-036](../../approvals/APPROVAL_REGISTER.md#aegis-apr-036-stage-4a-offline-bridge-package-completed)
records completion of that one implementation. The merge does not establish
real-host callback invocation, decision consumption or token telemetry.

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

## Full public archive screen for the initial candidate lock (2026-09-25 UTC)

The temporary version-3 lock above was used as the exact dependency population
for a **read-only static archive screen**. Its SHA-256 is
`dc869bd02f2ff679fb91c26ced5c7670ddb2156f91744a972d05e64d1d906df7`.
All 110 public registry tarballs were downloaded to temporary storage and
parsed without installing packages, running scripts, importing modules,
starting the bundled CLI, or contacting a model provider. The tarballs total
**842,011,242 compressed bytes** of cumulative download traffic across all
eight optional platform packages. The temporary audit retained roughly 1.3 MB
of report data, not the tarballs. The traffic figure is not the expected size
of one platform's installed tree. All 110 whole-archive SHA-512 values matched
the exact lock integrity values, and all embedded package names, versions and
license fields matched the lock metadata. The screen recorded zero download, parse or
integrity errors. This supports archive identity for this temporary resolution;
it does not establish safe code, reproducible builds or SDK runtime behavior.

The archive manifests declare **zero `preinstall`, `install` or `postinstall`
hooks** and eight `prepare` scripts. An eventual offline installation should
still use `npm ci --ignore-scripts --no-audit --no-fund` only after a separately
approved implementation grant and committed lockfile review. The 110 license
metadata fields remain 90 MIT, seven ISC, two BSD-3-Clause, one BSD-2-Clause,
one Unlicense, one Anthropic SDK license pointer and eight Anthropic native
package pointers. License text or a license pointer was found in 109 of the
110 archives. The exception is `standardwebhooks@1.1.1`: its package manifest
says MIT and its tarball lacks `LICENSE`, `COPYING` or `NOTICE`. The other
checked releases allowed by the `^1.0.0` dependency range, `1.0.0` and
`1.1.0`, also lack those files. The upstream
[JavaScript package manifest](https://github.com/standard-webhooks/standard-webhooks/blob/main/libraries/javascript/package.json)
identifies MIT while the
[repository root license](https://github.com/standard-webhooks/standard-webhooks/blob/main/LICENSE)
says Apache-2.0.
Resolve the applicable published-package text with its maintainer or an
authoritative package-specific source before treating this license review as
closed. The SDK and native packages point to
[Anthropic commercial terms](https://github.com/anthropics/claude-agent-sdk-typescript/blob/main/LICENSE.md).
The SDK peer range also permits `@anthropic-ai/sdk@0.93.0` and `0.94.0`;
their public manifests omit `standardwebhooks`, while `0.95.0` introduces it.
This was checked with `npm.cmd view '@anthropic-ai/sdk@<version>' dependencies
--json` for each exact version. See the npm package records for
[0.93.0](https://www.npmjs.com/package/@anthropic-ai/sdk/v/0.93.0),
[0.94.0](https://www.npmjs.com/package/@anthropic-ai/sdk/v/0.94.0), and
[0.95.0](https://www.npmjs.com/package/@anthropic-ai/sdk/v/0.95.0).
An exact `0.94.0` alternate lock was subsequently screened below. Neither
the peer range nor static archives demonstrate runtime compatibility.

Each of the eight native binary sizes and SHA-256 values below matched the SDK
archive manifest. These are **binary-content checks**, separate from the
whole-tarball SHA-512 checks; no binary was executed.

| `@anthropic-ai/claude-agent-sdk-` suffix, all `0.3.281` | Binary bytes | SHA-256 |
| --- | ---: | --- |
| `darwin-arm64` | 220,931,760 | `a922981f6f3b55a251ef9f9dbaa0621a5f99cbcb5ca67f8a797476ccfc83f626` |
| `darwin-x64` | 229,263,712 | `a9355cbb0d291ce948efcf61a6ef397401672f64fa5e5e67bca092fed6cd9088` |
| `linux-arm64` | 236,773,368 | `dd27b36438a4fed1670cd29bad2fda6a73b628b6da55443e5c2f647fe6ed328f` |
| `linux-arm64-musl` | 229,128,008 | `4f72ebbb08706651e7a2204303793700698f4046bc31f3e7e65b381063b7c210` |
| `linux-x64` | 237,375,560 | `56fe3da88458465fb27d7e9299dddb3fead55750fb9c2de795f233b5eea6dce1` |
| `linux-x64-musl` | 231,137,376 | `30220a5cf0628634599e0ede13a5cc814d21880116abf762f0598a33636f7bca` |
| `win32-arm64` | 228,774,560 | `103730182fe4dd36b8ff7791a408ac6144b2c40e35ab7b56b3561ce1d385ecbb` |
| `win32-x64` | 240,767,648 | `39be063c2512b43347fe7b0ab18c46f1596141701c9c5fc895ddfca9a051067c` |

The SDK manifest's explicit `testedWrapperVersions` list ends at `0.3.280`,
although this candidate wrapper and bundled CLI are `0.3.281` and `2.1.281`.
Archive identity therefore does not demonstrate this wrapper/CLI pair's
compatibility. The selected Windows prototype also cannot establish Linux
runtime compatibility merely because the Linux x64 binary hash matches. Those
checks belong to later, separately authorized host execution.

## Preferred offline peer candidate: API SDK 0.94.0

A second temporary version-3 lock keeps Agent SDK `0.3.281`, MCP SDK `1.30.1`
and Zod `4.6.5`, and resolves the allowed `@anthropic-ai/sdk@0.94.0` peer.
Its SHA-256 is
`403a823392845956bde0f7a8d78c103571dc86c680659194f8f231cc7f52776d`.
It has 107 dependency entries, including the same eight native packages.
**106 entries have identical name, version and integrity** to the 110-entry
lock above, so their archive checks are reusable. The one changed archive is
`@anthropic-ai/sdk@0.94.0`: its 706,201-byte tarball matched registry SHA-512
`sha512-OVlCttk5MyeTGtrWX5+F3MJOfEMDuEjK8+rm9aQMDfRPWndVMbhk37QG8WLnVbcc7huyUGngVMjT7iMN2llySA==`.
It bundles an MIT `LICENSE`, declares no `preinstall`, `install` or
`postinstall` hook, and lists `json-schema-to-ts` as its only ordinary
dependency. The alternate drops `standardwebhooks`, `@stablelib/base64` and
`fast-sha256`, with no newly added package. Thus all **107/107** exact
archives have static integrity, manifest and license coverage through the
106 reused checks plus the new archive check. Its license metadata population
is 88 MIT, seven ISC, two BSD-3-Clause, one BSD-2-Clause, one Anthropic SDK
pointer and eight native-package pointers. No archive in this alternate
resolution declares an installation hook; the reviewed `prepare` scripts
still justify `--ignore-scripts` for any later authorized install.

The `0.94.0` resolution is the **preferred candidate for an offline TypeScript
bridge** because it removes the package with unresolved published-license
attribution while preserving the SDK's declared peer range. This is a
supply-chain preference, not a claim that the SDK wrapper, bundled CLI and
older API SDK work together at runtime. A committed lock, package-body safety
review and separate Stage 4A implementation grant remained pending at this
2026-09-24 screening point. The later
host proof must test executable compatibility without assuming it from the
static archive screen. No package was installed or executed in this review.
