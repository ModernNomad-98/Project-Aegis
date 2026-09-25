# Issue #101 Stage 4A offline bridge review

Scope: the owner's 2026-09-25 grant for the exact 11 paths in the
[Stage 4A proposal](../../roadmaps/aegis-setup-package-4a-host-preparation-proposal.md),
at most 12 active implementation hours, 1,200 added handwritten code/test
lines, and $0 task-controlled external spend. This record does not approve an
SDK session, CLI, provider, credential, private data, VM action or deployment.

## Dependency and package-body assessment before install

The committed lock resolves exactly 107 non-root packages from four exact
roots: Claude Agent SDK `0.3.281`, Anthropic API SDK `0.94.0`, Model Context
Protocol SDK `1.30.1`, and Zod `4.6.5`. All 107 have registry integrity fields;
none is marked with an install script. A per-path comparison of all 107
name/version/integrity records against the retained, previously reviewed
preferred candidate found zero differences. That candidate's SHA-256 is
`403a823392845956bde0f7a8d78c103571dc86c680659194f8f231cc7f52776d`.
The [archive audit](issue-101-package-4a-host-feasibility.md#preferred-offline-peer-candidate-api-sdk-0940)
checked all 107 exact archive SHA-512 values, embedded package identities,
license metadata, lifecycle script declarations and native binary hashes.
The `0.94.0` API peer removes the unresolved `standardwebhooks` license case.

Package-body execution in this increment is bounded further: installation
uses `npm ci --ignore-scripts --no-audit --no-fund`; the test script uses
Node's built-in test runner; `bridge.ts` has only Node built-in runtime imports
and its SDK type import is erased, while the
test imports only that module. The local worker imports only the shipped Python
contract. There is no dynamic import of installed SDK packages, `query()` call,
Claude executable call, plugin discovery, or online fallback. This static
assessment supports a scripts-disabled install for the offline tests. It does
**not** prove arbitrary JavaScript package behavior safe, verify wrapper/CLI
runtime compatibility, or grant future imports or execution of the SDK body.
The SDK and native archives refer to Anthropic commercial terms; that is a
license and maintenance consideration despite $0 provider spend here.
After this assessment, the local Windows `npm ci --ignore-scripts --no-audit
--no-fund` completed and installed 100 platform-applicable packages. The
remaining optional native platform archives remain pinned in the 107-entry
lock. `npm ls --all --omit=optional --depth=0` showed the four exact roots.

## Contract and denial boundary

The host injects synthetic authority facts and supplies untrusted synthetic
advice. Each proposed `Agent`, model `Skill` or direct typed `/skill` dispatch
gets a fresh fact check before and after advice. The Python worker validates
the bounded request and response and checks that the recommendation includes
the proposed target. Failure, abstention, stale facts or a changed snapshot
denies; a passed recommendation cannot override ordinary host permissions.
The worker runs with Python site loading disabled and a narrow environment
allowlist, so it does not inherit provider credentials. Direct typed commands
are evaluated separately from model `Skill` calls.
Unknown tools also deny. There is no online fallback in the bridge.

Offline tests cover positive agent and skill cases; more than one dispatch;
unknown tool and ID; manual-only spoofing; missing mandatory or explicit
selection; read-only and permission denials; unsafe destination; stale facts;
malformed, duplicate-key and oversized replies; worker exit and timeout;
and callback exceptions. The tests use invented facts only. They cannot show
that a real SDK host invokes or consumes these callbacks. A real host source,
timing and end-to-end token comparison belong to separately approved Stage 4B.

Local Windows checks: `node --test bridge.test.ts` passed 10/10, the existing
Python routing contract passed 11/11, and `scripts/validate-skills.py`
validated 185 skills with zero warnings. The bridge test also passed through
`scripts/ci/record-check.py setup-bridge`, proving the proposed CI command
and evidence recorder work together. These checks did not start an SDK
session or provider call. Linux and Windows GitHub Actions remain the merge
gate for this branch, and the protected workflow change may require a
separate exact-head gate-guard exception.
