# Issue #101 Stage 4B preflight manifest template

**Status: unfilled planning template, 2026-09-25 UTC.** Copy this page into a separately reviewed execution packet. Resolve every **preflight** `UNKNOWN` before requesting a live Stage 4B grant; leave **post-run** observations as `NOT RUN` until an authorized session produces receipts. Record the owner-grant receipt later as a separate approval attachment. This page authorizes no SDK session, provider call, credential use, installation, host probe, VM work, helper comparison, deployment, or deletion. The [Stage 4B proof protocol](aegis-setup-package-4b-host-proof-protocol.md) defines the required cases and stop rules. [PR #291](https://github.com/ModernNomad-98/Project-Aegis/pull/291) corrected the offline bridge's permission response, but its synthetic tests do not prove host behavior. An execution packet must pin the corrected source commit and verify the selected runtime independently.

## Choice and plain terms

An **SDK** (software development kit) lets a separate program start and control assistant sessions. A **provider** operates the remote model service that a live session may call and bill. A **host** is the actual program running that session. A **hook** is a callback before an action; **decision consumption** means the host's observed action follows the callback, rather than merely receiving its return value. A **permission mode** and its allow, ask and deny rules determine ordinary tool authority. **`canUseTool`** is an SDK callback for tool approvals that earlier rules have not resolved; earlier approval may skip it. A **whole-experiment meter** combines every case, session, retry and subagent so resetting one SDK call cannot reset the owner's budget.

| Path | Reason and benefit | Drawback | Money, setup and upkeep |
| --- | --- | --- | --- |
| **A. Native Windows SDK session with invented cases (recommended for a later proof)** | Matches the selected Stage 4A bridge boundary and tests real hook invocation, permission consumption and usage receipts. | A live SDK session can reach a provider and does not prove CLI/editor behavior or token savings. | Provider/account price and total spend **UNKNOWN** until verified; setup needs a pinned host and reviewed packet; SDK/host updates need reproof. |
| B. Current CLI/editor proof | Tests the owner's current workflow directly. | Its hook coverage and fail-closed behavior need separate research and a new protocol. | Live usage price **UNKNOWN**; additional research/setup and update-dependent reproof. |
| C. Aegis only | Uses existing skills with no new host boundary. | Gives no optional-routing or savings claim. | No incremental helper/provider experiment spend; existing assistant costs remain. |

**Recommendation:** prepare A first because the merged offline bridge gives it the narrowest candidate boundary. Execute A only after the exact packet, account, credentials class, meter and caps receive separate owner approval. If an effective setting or mandatory receipt cannot be verified, select C for ordinary use while researching B. Preparation has no external usage cost; a future live session is **not** assumed to cost $0.

## 1. Identity and frozen profile

Fill preflight values, evidence source, reviewer and capture time. A requested setting is not proof of its effective value: freeze its expected value before the grant request, then attach the effective-host receipt after an authorized run. Canonicalize and hash the frozen **preflight fields excluding the digest field itself, approval attachment and all post-run receipt fields**; store that detached digest before the grant request. The later approval attachment records the owner grant ID, exact approved scope and the preflight digest it approves. Approval cannot silently change a planned field: any changed planned field is a new profile and needs review.

| Required field | Frozen value / evidence |
| --- | --- |
| Packet ID, issue/PR, preflight profile digest and proposed exact grant scope | `UNKNOWN` |
| Operator, independent reviewer, review date and sign-off receipts | `UNKNOWN` |
| Native Windows host alias (nonpersonal), edition/build, architecture, CPU, RAM and isolation | `UNKNOWN` |
| Repository commit with PR #291 fix, worktree/fixture digest, allowed files and commands | `UNKNOWN` |
| Node, npm, Python, SDK, bundled Claude executable, API/MCP/Zod versions, lockfile and script digests | `UNKNOWN` |
| Package license/terms and source of exact runtime-version documentation | `UNKNOWN` |
| `query()` entry point, model, endpoint, provider, working directory and environment allowlist | `UNKNOWN` |
| Expected `settingsSources`, project/user settings, plugins, hooks, sandbox, network and subprocess policy; effective-host receipt after run | `UNKNOWN`; receipt: `NOT RUN` |
| Expected `allowedTools`, `disallowedTools`, `permissionMode`, `permissionPrompts`, `canUseTool`, tool/agent/skill definitions and max turns; effective-host receipt after run | `UNKNOWN`; receipt: `NOT RUN` |
| Planned mid-session `setPermissionMode()` calls (or explicit prohibition), permitted transitions and per-turn receipts | `UNKNOWN`; receipts: `NOT RUN` |
| Hook event, matcher, timeout, overlap order and isolated negative unmatched-matcher outcome | `UNKNOWN` |

The offline Stage 4A lock is a source artifact, **not** a Stage 4B runtime pin. Review the pinned SDK's documented behavior against the official [permissions guide](https://code.claude.com/docs/en/agent-sdk/permissions) and [hook reference](https://code.claude.com/docs/en/hooks#pretooluse-decision-control) before requesting approval; verify actual effective behavior during the authorized run. `allowedTools` preapproves matching tools but leaves other tools available; an earlier approval can skip `canUseTool`. A `PreToolUse` hook `allow` can skip a prompt. Record the expected and then observed results in the matrix below.

**Approval attachment (outside the preflight digest):** owner grant ID/receipt `PENDING OWNER DECISION`; approved preflight digest `PENDING OWNER DECISION`; exact approved scope and caps `PENDING OWNER DECISION`. Before any session, verify this attachment names the unchanged frozen digest and that its scope and caps cover the run. A narrower grant controls; any changed plan requires a new reviewed digest.

## 2. Host authority and effective permission matrix

Before approval, name the planned host-owned source, maximum age and expected receipt for eligible agent/skill IDs, manual-only and read-only flags, required specialists, explicit user selections, genuine typed `/skill` origin, policy/catalog version, local-only destination and ordinary permission. During an authorized run, record each actual read time and digest/generation, then read again immediately before consumption; changed, missing, stale or conflicting facts deny. The bridge worker's invented snapshot is not an authority source.

| Source or proposed tool | Preflight: expected loaded state, hook/event return, deny/ask/allow rule and mode | Preflight: expected `canUseTool` reach and final action | Post-run: effective settings, callback, permission and observed action receipts |
| --- | --- | --- | --- |
| `Agent` and each offered agent ID | `UNKNOWN` | `UNKNOWN` | `NOT RUN` |
| `Skill` and each offered skill ID | `UNKNOWN` | `UNKNOWN` | `NOT RUN` |
| Direct typed `/skill` / `UserPromptExpansion` | `UNKNOWN` | `UNKNOWN` | `NOT RUN` |
| File reads/writes, shell and code tools | `UNKNOWN` | `UNKNOWN` | `NOT RUN` |
| MCP, connector and task tools; any no-prompt tool | `UNKNOWN` | `UNKNOWN` | `NOT RUN` |

List every expected path, including an unavailable or excluded path and why. One row per rule/mode variant is required in the frozen execution copy. Record the permission mode effective at each turn, including any authorized mid-session change. After the run, compare the effective paths with those expected. If the selected host cannot expose a required authority fact or dispatch path, narrow the claim and leave assisted dispatch disabled.

## 3. Frozen synthetic case register

Use invented prompts, paths and IDs only. Before execution, replace each `UNKNOWN` with exact prompt/fixture digest, offered IDs, expected hook and host result, maximum repeats, and per-case call/token/time reservation. Each receipt needs one run/session/turn/case/target correlation ID, monotonic timestamps, bounded sanitized input hash, before/after authority digests, callback decision, final permission decision and observed action or absence. A callback return alone never passes.

| Case | Required observation | Fixture / expected result / repeat cap |
| --- | --- | --- |
| 01 `Agent` positive and negative | Eligible read-only launch; unknown or non-read-only launch absent | `UNKNOWN` |
| 02 model `Skill` positive and negative | Eligible load; unknown/manual-only load absent | `UNKNOWN` |
| 03 genuine typed `/skill` and spoof | Real expansion consumed; quoted/model-origin command denied | `UNKNOWN` |
| 04 required and explicit choices across turns | Omission denied; later requirement remains open after first valid dispatch | `UNKNOWN` |
| 05 host permissions | Deny, ask, default/selected mode, allow and no-prompt cases; record whether `canUseTool` ran | `UNKNOWN` |
| 06 freshness and destination | Changed/expired authority or online destination under local-only rule denied | `UNKNOWN` |
| 07 fail closed | Abstention, malformed/duplicate/oversized frame, worker exit, timeout, exception and unknown tool denied | `UNKNOWN` |
| 08 coverage and overlap | Every effective path observed; isolated unmatched-matcher case cannot launch; deny wins overlap | `UNKNOWN` |

For each case mark layer **manual live-host observation**, with local synthetic fixtures prepared before the run. There is no CI host proof. Run the unmatched-matcher negative only in an isolated case whose expected tool action is safe and pinned. An uncovered path that launches an agent or skill marks this host boundary **unsupported**. Record actual status as `NOT RUN`, `PASS`, `FAIL` or `UNVERIFIED`; a missing receipt is `UNVERIFIED` and blocks the host claim. See the [numbered protocol cases](aegis-setup-package-4b-host-proof-protocol.md#numbered-hook-and-consumption-cases) for detailed negative paths.

## 4. Session, privacy and evidence

| Required field | Frozen value / evidence |
| --- | --- |
| `persistSession`, `continue`, `resume`, `/clear` policy; transcript path if any | `UNKNOWN` |
| Planned session/turn/subagent correlation format and reset/resume reconciliation method; actual IDs after run | `UNKNOWN`; IDs: `NOT RUN` |
| Invented-only input boundary, no private repository/messages, egress destinations | `UNKNOWN` |
| Credential class and custody without exposing secret to worker, log, issue or PR | `UNKNOWN` |
| Provider retention and account terms; owner-approved private raw-record location and access | `UNKNOWN` |
| Sanitization method; publishable hashes/counts/settings/receipts; retention/deletion date and authority | `UNKNOWN` |
| Preflight source/lock/profile hashes and planned result-table signatories; post-run result signatures | `UNKNOWN`; result signatures: `NOT RUN` |

Prefer `persistSession: false` if supported by the pinned TypeScript runtime and if no resume case is required. The official [session guide](https://code.claude.com/docs/en/agent-sdk/sessions) says this avoids writing a transcript for that call; resume restores a prior session and must stay within the experiment total. If persistence is necessary, approve storage, access, redaction and retention before any session. Never place raw transcripts, credentials or private account records in the source repository.

## 5. Whole-experiment meter, caps and abort

| Owner-set ceiling or meter fact | Frozen value / evidence |
| --- | --- |
| Account, credential class, model, provider/endpoint, price schedule and allowance coverage | `UNKNOWN` |
| Maximum provider calls, input/output/cache tokens, dollars, cases, repeats and subagents | `UNKNOWN` |
| Maximum wall time, active work time, turns, concurrent queries and retries | `UNKNOWN` |
| Pre-call reservation, abort margin, polling interval and reliable provider/account meter | `UNKNOWN` |
| One ledger across all sessions, retries, resets and subagents; deduplication key | `UNKNOWN` |
| Failure/crash reconciliation and stop operator; explicit rollback to Aegis only | `UNKNOWN` |

Do not start while any ceiling, price, allowance, meter or abort margin is `UNKNOWN`. Record result `modelUsage` for whole-query-tree tokens and `total_cost_usd` as an estimate; `usage` omits subagent work. Reconcile reset/resume and any calls outside the SDK tree with the provider/account record. The official [cost guide](https://code.claude.com/docs/en/agent-sdk/cost-tracking) says `maxBudgetUsd` covers one `query()` call's own spend, `/clear` starts that cap over, and SDK dollar fields are estimates. A missing or zeroed crash result is unknown spend, not zero spend: stop until reconciled.

Abort before a cap can be crossed, and immediately on missing authority, unexpected dispatch, permission or manual-only bypass, unmatched hook, online fallback, data egress, unknown charge, incomplete trace or telemetry gap. End the separate SDK session and use ordinary Aegis only. Preserve sanitized diagnostic receipts; no automatic retry changes a failed result.

## 6. Review and release gates

1. **Maintainer:** sign the exact planned runtime, expected loaded-tool inventory, authority-source mapping and case fixtures; resolve each preflight `UNKNOWN` or block. Post-run receipts remain `NOT RUN`.
2. **Independent reviewer:** sign privacy, expected permission matrix, whole-experiment meter, abort margin and evidence plan; unresolved preflight facts block.
3. **Owner:** decide a separate exact Stage 4B execution grant specifying host, operator, credentials class, provider, allowed actions and all ceilings. A reviewed manifest or previous Stage 4A grant is not that decision.
4. **After an authorized run:** classify each result as **observed**, **inferred** or **unverified**, reconcile usage and charges, and publish only sanitized evidence for the tested profile. A failed or incomplete case blocks a supported-host claim.

**Open facts for owner/account review:** selected Windows host and its effective settings; provider/account/credential class; price and allowance; network destination and retention; exact call/token/dollar/time caps; reliable whole-experiment meter; transcript policy; independent reviewer; and separate execution grant. All remain `UNKNOWN` here.
