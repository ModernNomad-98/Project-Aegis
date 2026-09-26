# Issue #101 Stage 4B preflight draft

**Status: source-only draft, 2026-09-26 UTC.** This is a partial fill of the
[preflight manifest template](aegis-setup-package-4b-preflight-manifest-template.md),
not a frozen execution profile or an approval request. It records facts from
Project Aegis source at merge `658fa22edbfde2c953f7d21678d08baa79b75052`.
No SDK package was installed or session run to prepare this page; local read-only
hashing was performed. No provider call, credential use, VM work, host probe,
helper comparison, deployment or
deletion is authorized by it. Recheck every source pin against the exact commit
chosen for a later run. The [proof protocol](aegis-setup-package-4b-host-proof-protocol.md)
and the template govern the eventual packet. The
[offline synthetic case draft](aegis-setup-package-4b-synthetic-case-fixtures.md)
provides candidate invented prompts and expected action/receipt rows for all
eight cases; it is not a frozen manifest or a run result.

## What is already known

An **SDK** is a software development kit that lets a program start an
assistant session. A **lockfile** records the dependency versions and package
integrities selected for a software install. A source hash checks whether a
file changed; it says nothing about what ran on a host. Stage 4A is an
**offline synthetic** callback bridge, so its source pins are candidates for
Stage 4B, not evidence of a working live session.

| Source fact at the commit above | Verified value | What it does not prove |
| --- | --- | --- |
| Offline bridge location | `tools/aegis_setup/host_bridge/` | It has not launched an SDK session. |
| Declared Node range | `>=24 <25` in `package.json` | Node is installed or compatible on the selected host. |
| Declared direct dependencies | Claude Agent SDK `0.3.281`, Anthropic API SDK `0.94.0`, MCP SDK `1.30.1`, Zod `4.6.5` | These packages were loaded in a live Stage 4B session. |
| Offline bridge behavior | A passed recommendation returns no tool permission approval; a failure denies. Version 2 binds a response to a fresh request ID. | Host permission order, callback reach or action consumption. |
| `package-lock.json` SHA-256 | `68979B1A544A4CE94A1A6DD6825DCACA258E5C59B92277BFEF2D6C31367628CC` | Runtime binary and installed tree identity. |
| `bridge.ts` SHA-256 | `B3A2AA5AC52FABA9BEAC2FB67B24A1AFEBE2C708D88AA48722F4C64049B7E5DC` | A callback was registered or invoked. |
| `contract_worker.py` SHA-256 | `A5159B4D39BEF972E535C3C08110E9159387DE5B955C0FE060C36AB3F9A2B3C5` | A worker ran with the expected environment. |

The lock and file hashes are SHA-256 of canonical Git blob bytes at the stated
commit, without Windows checkout line-ending conversion. A later execution
packet must hash its entire frozen preflight profile
separately, attach independent review, then bind a separate owner grant to that
profile digest. The Stage 4A lock does not choose the Stage 4B runtime.

## Choices and unresolved preflight facts

The earlier [host-path proposal](aegis-setup-package-4b-host-proof-protocol.md#decision-requested-and-plain-terms)
recommends a narrow native Windows SDK session with invented cases. That path
tests callback invocation and observed permission/action behavior on one
selected host. It can incur provider charges and does not prove the current
CLI or editor. Direct CLI/editor proof needs separate hook research; ordinary
Aegis-only use needs no helper experiment but cannot support routing or savings
claims. **Recommendation:** keep the narrow SDK path as the planning candidate
because the shipped offline bridge already defines its callback boundary.
Choose an executable path only after the exact profile, permissions, meter and
spend ceiling have been reviewed.

| Required before a Stage 4B grant request | Current status | Owner or reviewer action |
| --- | --- | --- |
| Selected host, nonpersonal alias, Windows build, isolation and operator | `UNKNOWN` | Name and verify the host and operator. This is not the paused Linux VM. |
| Exact source commit, runtime versions, installed package and executable hashes | Candidate source above; runtime `UNKNOWN` | Recheck the lock and pin the actual runtime. |
| Model, endpoint, account and credential class | `UNKNOWN` | Approve a bounded account path without placing secrets in the packet. |
| Effective settings, tool/agent/skill inventory, hook matchers and ordinary permission modes | `UNKNOWN` | Freeze expected values and the host-owned authority sources; later observe effective values. |
| Invented prompts, fixture digests, expected permission/action matrix and repeat caps | `UNKNOWN` | Freeze one row per protocol case and rule variant. |
| Transcript policy, retention, redaction, private receipt location and access | `UNKNOWN` | Approve the evidence boundary; publish sanitized receipts only. |
| Price/allowance, call/token/dollar/time ceilings, abort margin and whole-experiment meter | `UNKNOWN` | Verify current terms and set a stop-before-cap plan across sessions, retries and subagents. |
| Maintainer and independent review, frozen preflight digest, exact owner grant | `PENDING` | Review the filled template, then decide one separate execution grant. |

All eight [numbered protocol cases](aegis-setup-package-4b-host-proof-protocol.md#numbered-hook-and-consumption-cases)
are `NOT RUN`. No effective settings, callback, permission, observed action,
token, cost or host-support result exists. If a mandatory fact or reliable
meter cannot be verified, stop the live plan and use ordinary Aegis-only setup
while researching the gap. The [package 7 readiness matrix](aegis-setup-routing-plan.md#package-7-readiness-against-issue-101-acceptance)
remains blocked after this draft.
