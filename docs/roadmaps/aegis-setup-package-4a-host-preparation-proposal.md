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
has a separate selected-work view and no finite total because later Behavioral
Eval Runner (BER) work and both package-4 stages remain unestimated. Active-only
time was not instrumented for this packet.

**Selected planning direction:** a separate Claude Agent software development
kit (SDK) managed session on the owner's native Windows host, first exercised
with synthetic offline
callbacks. The owner's reply was "your recommendation. do not stop for
decision, i can always come back and ask. follow my rules" to the question
that recommended this path and explicitly limited the choice to planning.
The selected session is a prototype target, not a claim that the current
command-line interface (CLI), editor or another consumer assistant uses its
callbacks.
The locally available Claude Code CLI reports
`2.1.246` on 2026-09-24, but no SDK package version is pinned or installed by
this packet. SDK behavior does not prove that the CLI, editor or a consumer's
existing assistant uses the same hook path. The [source review](../evidence/setup/issue-101-package-4a-host-feasibility.md)
records the documented interface and its limits.

## Selected candidate and package review (2026-09-25 UTC)

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
not the MIT license of the separate `@anthropic-ai/sdk` API client. The package
review below distinguishes verified archives from the dependency tree that
still needs a committed, reviewed lockfile. No package has been installed or
executed.

Evidence checked on 2026-09-25 UTC: `npm.cmd view
'@anthropic-ai/claude-agent-sdk@0.3.281' version engines license
dist.integrity claudeCodeVersion optionalDependencies --json` returned the
fields above without installing the package. `node --version`,
`npm.cmd --version` and `python --version` returned `v24.19.0`, `11.17.0`
and `Python 3.14.7` on the candidate Windows host. The npm license field
says `SEE LICENSE IN README.md`; the linked upstream license supplies the
commercial-terms text. These checks do not verify downloaded tarball contents.

The owner selected the first path for planning. The alternatives explain its
cost and limit for readers making the same choice:

| First host path | Benefit | Cost and limitation |
| --- | --- | --- |
| Separate SDK-managed Claude session on native Windows, recommended for an **offline prototype only** | Documented TypeScript callback surfaces let synthetic tests exercise typed `/skill` and model tool dispatch. | Adds Node/TypeScript dependencies and maintenance under the SDK's commercial terms; it does not establish that the current CLI/editor uses these callbacks. Synthetic testing can spend $0 on providers; any real session needs a later grant and may incur usage cost. |
| Current CLI/editor only | Preserves the existing-assistant experience directly. | No complete fail-closed interception path is established; more host research is needed before code or a credible time estimate. |
| Keep Aegis-only for now | No new dependency, host setup or provider spend. | Optional routing and any savings remain unavailable and unmeasured. |

Choosing this path selects a planning direction, **not** an SDK installation,
implementation, host session, provider call or release claim. The first
profile is the existing native Windows host
with Node 24.19.0, npm 11.17.0 via `npm.cmd`, and Python 3.14.7. These tool
versions were observed locally; other operating systems remain unverified.

The public `0.3.281` SDK and Windows x64 npm archives passed whole-archive
SHA-512 checks against their registry integrity fields. The Windows archive
has a 240,767,648-byte `claude.exe` whose SHA-256 is
`39be063c2512b43347fe7b0ab18c46f1596141701c9c5fc895ddfca9a051067c`;
it matches the SDK manifest. The Windows archive integrity is
`sha512-hbnymWj9O31K0VMd/VOpMTZ0CNT3BkwgGGe84zHdAP6MDxmoZvqyS94UEaLQit3xmozCxfkfGns7/WgWH1Q6Sg==`.
The SDK and Windows package manifests declare no install scripts or ordinary
`dependencies` entries. The SDK declares peer ranges for `@anthropic-ai/sdk`,
`@modelcontextprotocol/sdk` and `zod`, plus exact-version platform packages.
The first peer examples were `0.128.0`, `1.30.1` and `4.6.5`;
these were **examples, not an approved resolved tree**. The Model Context
Protocol (MCP) peer alone
declares 16 direct dependencies. A generated exact lockfile must fix every
resolved package and integrity value; separately inspect each resolved
manifest/archive for license and lifecycle scripts before install.
The two inspected archives reference Anthropic commercial terms and include a
large closed-source binary; the candidate peers declare MIT. npm registry
signatures were present but were not cryptographically verified. The SDK
manifest's explicit tested-wrapper list ends at `0.3.280`, so metadata does
not establish compatibility of wrapper `0.3.281` with its bundled CLI. The
[package evidence](../evidence/setup/issue-101-package-4a-host-feasibility.md)
records the checks and their limits.

A temporary npm lockfile candidate with exact roots SDK
`0.3.281`, Anthropic API SDK `0.128.0`, MCP SDK `1.30.1` and Zod `4.6.5`
resolved 110 dependency entries besides the root record, all with integrity
values. A later read-only static screen downloaded and inspected all 110
public archives. All archive SHA-512 values matched the lock, all embedded
name/version/license metadata matched, and the eight native binary SHA-256 and
size values matched the SDK manifest. The 110 tarballs generated 842,011,242
compressed bytes of cumulative download traffic including all eight optional
platforms; one-platform CI is not expected to install all eight. The archive
manifests declare no
`preinstall`, `install` or `postinstall` hooks and eight `prepare` scripts.
No package was installed or executed. This candidate includes
`@hono/node-server@2.1.1`,
which requires Node.js 20 or newer, so the candidate's effective minimum is
20 even though the top-level SDK metadata says 18. The local Node 24.19.0
meets that constraint. The candidate lock is not yet a committed dependency
set or a safety audit of 110 package bodies. A specific license ambiguity
remains: `standardwebhooks@1.1.1` declares MIT in its package manifest but
bundles no license file, as do the other checked releases allowed by its
`^1.0.0` dependency range, `1.0.0` and `1.1.0`. Its upstream
[JavaScript package manifest](https://github.com/standard-webhooks/standard-webhooks/blob/main/libraries/javascript/package.json)
says MIT, while the
[repository root license](https://github.com/standard-webhooks/standard-webhooks/blob/main/LICENSE)
says Apache-2.0. Resolve the applicable package terms
before closing the dependency review. The SDK and native packages point to
[Anthropic commercial terms](https://github.com/anthropics/claude-agent-sdk-typescript/blob/main/LICENSE.md).
Older allowed API SDK peer releases
[0.93.0](https://www.npmjs.com/package/@anthropic-ai/sdk/v/0.93.0) and
[0.94.0](https://www.npmjs.com/package/@anthropic-ai/sdk/v/0.94.0) omit
`standardwebhooks`; [0.95.0](https://www.npmjs.com/package/@anthropic-ai/sdk/v/0.95.0)
introduces it. A second temporary exact lock uses API SDK `0.94.0`. Its
SHA-256 is
`403a823392845956bde0f7a8d78c103571dc86c680659194f8f231cc7f52776d`.
It has 107 dependency entries including eight native packages. Of those,
106 have the same name, version and integrity as the fully inspected
`0.128.0` lock. The one changed API SDK archive is 706,201 bytes, matches its
registry SHA-512, bundles an MIT `LICENSE`, declares no installation hook and
has `json-schema-to-ts` as its sole ordinary dependency. The alternate removes
`standardwebhooks`, `@stablelib/base64` and `fast-sha256` without adding a
package. All 107 exact archives therefore have static identity, license and
script coverage by reuse plus the new check. Its license metadata fields are
88 MIT, seven ISC, two BSD-3-Clause, one BSD-2-Clause, one Anthropic SDK
pointer and eight native-package pointers. No archive declares an
installation hook. **Prefer this `0.94.0` peer for the offline TypeScript
candidate** because it removes the unresolved `standardwebhooks` package.
This does not prove the older peer is compatible with wrapper `0.3.281` or
its bundled CLI. Neither lock is committed, installed or a final dependency
approval. The [archive evidence](../evidence/setup/issue-101-package-4a-host-feasibility.md#preferred-offline-peer-candidate-api-sdk-0940)
records both digests, all eight native hashes and review limits.

For review, a possible **separate Stage 4A-offline grant** would cap work at
12 active implementation hours, 1,200 added handwritten code/test lines and
$0 external spend. The 12-hour figure is a **ceiling, not an estimate** or
time already spent.
The selected path splits package 4. The older 8–16-hour whole-package estimate
cannot safely cover Stage 4A plus Stage 4B. The
[current forecast](aegis-backlog-forecast.md#material-owner-decision--2026-09-25-issue-101-host-path)
lists both separately; neither has a defensible remaining-work estimate yet.
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
The continuous integration (CI) workflow must run the new offline tests on
the pinned package.

For a later authorized implementation, add a recorded offline bridge test
step to each existing CI job: Linux `validate-skills` and Windows
`windows-offline-checks`. Use a full commit SHA for `actions/setup-node`, pin
Node 24 on both hosts, disable the package-manager cache, supply no provider
credentials, and install only from the committed lock with
`npm ci --ignore-scripts --no-audit --no-fund`. Run
`node --test tools/aegis_setup/host_bridge/bridge.test.ts` through the
repository's record-check mechanism
so the existing required checks cover it. The test process must import only
the bridge and synthetic fixtures: no SDK `query()`, bundled CLI process,
provider call or real host callback. CI must assert the positive and denial
cases listed below, plus that every failure returns an explicit denial and
does not invoke an online fallback. A later CI workflow edit is a protected
path and requires its own exact-head gate-guard disposition if that check
blocks a PR; this packet does not grant such an exception.

For offline tests, a trusted synthetic `AuthoritySnapshot` must supply
current eligible agent and skill IDs and their flags; mandatory and explicit
selections; genuine direct manual invocation; catalog and policy versions;
stage; destination and local-only policy; and the ordinary host permission
decision. The helper may recommend among those IDs but cannot create or
modify authority. The bridge must bind its decision to the actual proposed
tool target, recheck a fresh snapshot before each dispatch, and deny on a
changed or missing fact. A valid recommendation does not complete a whole
task's mandatory review plan, so tests must include more than one dispatch.
For Stage 4A these sources are **injected synthetic fixtures**. The real host
source, refresh timing and consumption of each fact require Stage 4B proof.

The proposed test matrix includes `Agent`, model `Skill` and direct typed
`/skill` paths, including a direct command absent from the model skill
allowlist; unknown tools and IDs; manual-only spoofing; mandatory, explicit,
read-only and ordinary-permission checks; unsafe destination; stale snapshots;
malformed, duplicate-key and oversized frames; worker exit, timeout and
contaminated output; callback exceptions; abstention; and no online fallback.
The SDK docs distinguish `PreToolUse` from `UserPromptExpansion`, and say that
the latter covers direct typed commands. `canUseTool` alone is insufficient
because an earlier permission may skip it. Documented timeout blocking does
not prove every exception path, so the callback must explicitly catch errors
and return a denial. The proposed lockfile review must precede any
`npm ci --ignore-scripts` installation; tests must never start `query()` or a
Claude process.

This is **not yet an implementation-ready grant**. The host path is selected,
both exact candidate resolutions and all eight native hashes passed static
identity checks. The original `0.128.0` resolution still has the
`standardwebhooks` license ambiguity; the preferred `0.94.0` resolution
excludes it. A committed lockfile, package-body safety review, and wrapper/CLI
compatibility remain open. A later
reviewed approval must make the exact file list, limits and denial behavior
effective. Actual SDK callback
invocation, dispatch consumption and main/subagent token evidence remain
Stage 4B host proof.

## Owner decisions needed before code

1. **Planning choice resolved:** use a separate SDK-managed TypeScript
   session on native Windows as the first offline prototype. SDK `0.3.281`
   bundles CLI `2.1.281`; this does not qualify the owner's current CLI/editor
   as a verified supported host. Both temporary transitive resolutions passed
   static archive checks. Prefer API SDK `0.94.0` for the offline candidate;
   a committed lockfile and executable compatibility remain unverified.
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
