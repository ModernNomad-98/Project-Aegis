# Issue #101 Stage 4A offline bridge review

This page is for maintainers of the issue #101 setup router. Stage 4A is the
offline bridge stage of that plan, tested only with invented inputs; Stage 4B
is the later, separately approved real-host proof. The page records the
dependency assessment and the synthetic offline test evidence for the
[AEGIS-APR-031](../../approvals/APPROVAL_REGISTER.md#aegis-apr-031-issue-101-stage-4a-offline-bridge-implementation)
owner grant. It is not a deployed host integration and not a measured
real-host result.

> **Current reading, checked 2026-09-30:** the counts in the 2026-09-24 block
> below are that run's and have since drifted (now 14 bridge tests, 12 routing
> tests, 195 skills). Its sentence calling Linux and Windows Actions "the merge
> gate for this branch" is wrong: only `validate-skills` and `gate-guard` are
> required checks, and the bridge test runs in the non-required
> `tools-tests-linux` and `tools-tests-windows` jobs, so a red bridge test does
> not by itself block a merge. The permission boundary did change after this
> page's first version. The 2026-09-30 sections at the end correct all three
> and supersede the statements above.

Here, **SDK** is a software development kit, **CLI** a command-line interface,
**VM** a virtual machine, **CI** continuous integration, **PR** a GitHub pull
request, **UTC** Coordinated Universal Time, **Node** the Node.js runtime,
**JSON** JavaScript Object Notation, **`npm ci`** Node Package Manager's clean
lock-exact install, **lock** the committed `package-lock.json`, **roots** the
four directly requested dependency entries, **peer** a dependency the wrapper
declares it expects alongside it, **SHA-256** and **SHA-512** the 256-bit and
512-bit Secure Hash Algorithm digests, **`gate-guard`** the required check
that fails a change touching the merge gate or its enforcement surfaces, and
**exact head** the specific latest commit of a pull request that was checked.
Historic test counts below belong to the dated record that reports them.

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
The wrapper's SDK `peer` constraints (Anthropic API SDK `>=0.93.0`, Model
Context Protocol SDK `^1.29.0`, Zod `^4.0.0`) are why those three appear as
roots beside it.

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

## Lock re-review on 2026-09-29

The committed lock now pins Claude Agent SDK `0.3.283` instead of `0.3.281`.
The other three roots are unchanged, and the owner chose on 2026-09-29 to keep
the API SDK at `0.94.0`. The lock still has 107 non-root entries. Compared
with the previous lock, only the wrapper and its eight native packages
changed, and no package was added or removed. `standardwebhooks` is still
absent. The
[re-review of the archives](issue-101-package-4a-host-feasibility.md#re-review-on-2026-09-29-agent-sdk-03283-with-api-sdk-0940-kept)
records the new archive checks and native binary hashes. Installation still
uses `npm ci --ignore-scripts --no-audit --no-fund`. The boundary above is
unchanged.

## Correction on 2026-09-30: merge checks and permission boundary

An independent review on 2026-09-30 found two statements in the dated blocks
above to be wrong today. They are left in place as the record of what was
written, and corrected here.

**Which checks block a merge.** The 2026-09-24 sentence "Linux and Windows
GitHub Actions remain the merge gate for this branch" does not hold. Branch
protection on `main` requires exactly two contexts, `gate-guard` and
`validate-skills`; `strict` is `false`, so the required checks need only pass
on the current head, not on the merge result. The `windows-offline-checks` job
was already commented "Additional coverage; not registered in branch
protection" in the workflow at that same 2026-09-24 commit, so the sentence
was wrong when written, not merely stale. The bridge test runs today in the
`tools-tests-linux` and `tools-tests-windows` jobs, which are also not
required. **A red bridge, routing or delivery-control test therefore does not
by itself block a merge; only a failing `validate-skills` or `gate-guard` does.
The tools-tests jobs are additional coverage that closeout still expects to be
green.** Those suites moved into their own jobs on 2026-09-28 so that
pull-request-controlled test code could not reach a gate job; before that the
bridge step ran inside the `validate-skills` and `windows-offline-checks` jobs.

**The permission boundary did change.** The sentence "The boundary above is
unchanged" in the 2026-09-29 block is false for the permission boundary
described in the contract section. That section's "a passed recommendation
cannot override ordinary host permissions" (line 47 of the authoring version,
line 80 of this one) was also false when first written: the initial bridge
returned `permissionDecision: 'allow'` on a pass. Three 2026-09-25 merges
changed it:

- [PR #291](https://github.com/ModernNomad-98/Project-Aegis/pull/291)
  (`e9f8d234`, merged 08:33:12 UTC) replaced that `allow` with an empty object
  on a pass and left `deny` for a failure, which is what makes the
  host-permission sentence true; it was false before this merge.
- [PR #299](https://github.com/ModernNomad-98/Project-Aegis/pull/299)
  (`db2a3ae2`, merged 09:58:00 UTC) split the offer type into `AgentOffer` and
  `SkillOffer`, making `read_only` and `manual_only` required rather than
  optional, and bound the before/after snapshots by canonical (key-order
  independent) JSON.
- [PR #319](https://github.com/ModernNomad-98/Project-Aegis/pull/319)
  (`550151dc`, merged 2026-09-26 02:24:21 UTC) added the per-callback 128-bit
  `request_id` that the worker must echo exactly; there is no version-1
  fallback.

Only the three paths of PR #319 touched this page's scope; the first two
refined the boundary without adding a path. A real host receiving these
callbacks, and its timing or token cost, remains unproven and belongs to
separately approved Stage 4B.

## Re-derived counts on 2026-09-30

Re-derived at `origin/main` `1955c2229328ba8968bb2c0d5e5d4a91f05c556e`. Each
command below was run from the repository root of a detached worktree at that
commit.

| Figure | Command | Today | At `0bb51c19` (2026-09-24) |
| --- | --- | --- | --- |
| Bridge tests | `git grep -c '^test(' -- tools/aegis_setup/host_bridge/bridge.test.ts` | **14** | 10 |
| Routing tests | `git grep -c '^[[:space:]]*def test' -- tools/aegis_setup/tests/test_routing_contract.py` | **12** | 11 |
| Validated skills | `python -B scripts/validate-skills.py` | **195** | 185 |

The counting commands were confirmed by running the suites: `node --test
tools/aegis_setup/host_bridge/bridge.test.ts` reported `pass 14`, `fail 0`,
and `python -m unittest discover -s tools/aegis_setup/tests -p 'test_*.py'`
reported `Ran 12 tests ... OK` (no `-P`, which would hide the `tools` package
from that command); `python -B scripts/validate-skills.py`
reported `OK: 195 skill(s) valid, 0 warning(s)`. The 185 column was measured
the same way (the validator prints its own count) on a worktree at `0bb51c19`,
which is this page's authoring commit.

Each figure is the same check the 2026-09-24 block reports, re-run against
today's tree; the numbers grew because the repository did, and this page
records no result it did not measure. The lock is still 107 non-root entries
and the four root versions are unchanged since the 2026-09-29 block.

For example, the TAP summary of the bridge run from this worktree ended:

```text
# tests 14
# pass 14
# fail 0
# cancelled 0
# skipped 0
# todo 0
# duration_ms 2626.3831
```

That is a local offline test result over invented inputs, not a host
integration: it starts no SDK session, so it says nothing about a real host
or about provider cost.
