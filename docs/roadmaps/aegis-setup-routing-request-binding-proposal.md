# Issue #101: bind offline routing advice to one request

For the owner and reviewers of [issue #101](https://github.com/ModernNomad-98/Project-Aegis/issues/101),
this page explains a flaw in the synthetic offline routing candidate and
proposes a bounded repair. The [routing plan](aegis-setup-routing-plan.md)
describes the wider work. A **callback** is one check before an agent or skill
could run. A **response replay** reuses advice from an earlier callback. An
**identifier (ID)** pairs or names an item; here a fresh request ID would pair
one advice response with one callback. A **stable digest** is a repeatable
fingerprint of request content: identical content has the same digest.

Reader terms: A **pull request (PR)** proposes a repository change. The
**software development kit (SDK)** is a package for building a host
integration. **Node** runs JavaScript outside a browser; **TypeScript** adds
types to JavaScript. **Continuous integration (CI)** runs automated checks.
A **virtual machine (VM)** is a separate simulated computer. **UTF-8** is the
text encoding used to count contract bytes. An **AuthoritySnapshot** is the
bridge's copy of host-owned eligibility, selection, destination and permission
facts for one check; the bridge reads it again before allowing a result.

**Status:** proposed scope only. This document grants no implementation or
real-host authority. The package-3 grant covered one bounded implementation,
delivered in [PR #121](https://github.com/ModernNomad-98/Project-Aegis/pull/121)
under [AEGIS-APR-008](../approvals/APPROVAL_REGISTER.md#aegis-apr-008-issue-101-offline-advisory-routing-contract).
The Stage 4A grant in
[AEGIS-APR-031](../approvals/APPROVAL_REGISTER.md#aegis-apr-031-issue-101-stage-4a-offline-bridge-implementation)
was consumed by [PR #281](https://github.com/ModernNomad-98/Project-Aegis/pull/281),
as recorded in
[AEGIS-APR-036](../approvals/APPROVAL_REGISTER.md#aegis-apr-036-stage-4a-offline-bridge-package-completed).
Its exact path list excludes the Python routing contract and its tests, which
this repair must change.

## Observed failure

The current [Python contract](../../tools/aegis_setup/routing_contract.py)
compares a response's contract, catalog and policy
versions with a request and checks that its recommended IDs were offered. It
does not bind a response to the task synopsis, stage, or an individual call.
An advice response produced for synthetic task A can therefore pass validation
for synthetic task B when both share versions and offers. The offline bridge
then permits the proposed target if it appears in that stale response. This
is a local synthetic routing defect; no real host use has been established.

The current [TypeScript bridge](../../tools/aegis_setup/host_bridge/bridge.ts)
rechecks `AuthoritySnapshot` to protect against changes to the
host-owned facts during one callback. It cannot identify a response cached
from another callback with the same catalog and policy versions.

## Recommended repair

Create contract version `"2"` with a required `request_id` field in both the
request and response. The bridge generates a fresh, unpredictable 128-bit ID
for **each** callback evaluation before asking for advice. The Python parser
accepts only a 32-character lowercase hexadecimal ID. The validator requires
the response ID to match that request ID exactly, including for abstention.
The bridge does not accept version `"1"` as a fallback. A response replayed
from any earlier call is denied even when all other fields are identical.

The ID is a one-call correlation value, not a credential, permission grant,
signature, or proof of model behavior. An untrusted adapter seeing the current
request can echo its ID; the existing host-owned authority checks and ordinary
permission flow remain necessary. Generate the ID locally with Node's
cryptographic random source; no package or network connection is needed.

### Why this choice

The ID and digest options identify advice; neither grants dispatch permission.

| Choice | Reason and benefit | Drawback and cost |
| --- | --- | --- |
| Fresh random ID per callback — recommended | Distinguishes even identical successive requests, so cached advice cannot pass a later check. Uses Node's built-in cryptographic source and needs no network or new package. | Changes the closed wire contract to version 2; offline adapters and fixtures must echo the new ID. Estimated 6–10 active implementation hours, within the proposed 12-hour cap; $0 task-controlled external spend. Ongoing maintenance includes keeping both sides of the contract aligned. |
| Stable digest of request content | Rejects advice for different task text or other included facts while remaining reproducible for debugging. No external service or package is needed. | Identical repeated requests have the same digest, so an old response can pass a later callback. Canonicalizing every field consistently adds implementation and upkeep work. Time cost has not been estimated; $0 external spend is expected for an offline design. |
| Defer the repair | Avoids immediate code and migration work; $0 implementation spend now. | The demonstrated stale-response path remains in the offline candidate. Do not treat that candidate as ready for a host proof while the defect remains. Later investigation and repair time remain unknown. |

I recommend the fresh ID because the bridge makes a new dispatch decision on
every callback, including when task details repeat. It closes that replay
case without treating the ID as authority. The existing host-owned checks
still decide eligibility and permission.

## Proposed bounded implementation grant

| Field | Proposed bound |
| --- | --- |
| Source | `ModernNomad-98/Project-Aegis`, Role A source library, after a separate reviewed grant |
| Limits | At most 12 active implementation hours, 500 added handwritten code/test lines and $0 task-controlled external spend; stop before exceeding a bound |
| Data and execution | Invented offline fixtures only. No SDK `query()`, Claude process, provider call, credential, private data, VM work, dependency change, deployment or real callback invocation |
| Delivery | One signed implementation PR with exact-path staging, focused Python and Node tests, skill validation, independent contract and authority review, and green exact-head GitHub Actions before merge |

Proposed exact implementation paths:

- `tools/aegis_setup/routing_contract.py` — request and response validator.
- `tools/aegis_setup/tests/test_routing_contract.py` — Python contract tests.
- `tools/aegis_setup/README.md` — published contract description.
- `tools/aegis_setup/host_bridge/bridge.ts` — offline callback bridge.
- `tools/aegis_setup/host_bridge/bridge.test.ts` — synthetic callback tests.
- `tools/aegis_setup/host_bridge/README.md` — bridge instructions.
- `docs/roadmaps/aegis-setup-routing-plan.md` — issue #101 plan.
- `docs/evidence/setup/issue-101-routing-request-binding-review.md` (new)
  — implementation review record.

The proposed paths include the Python parser and test because the bridge's
worker calls `parse_request` and `decide`; changing TypeScript alone cannot
make the published response contract reject a stale reply. The worker needs
no edit if it continues to pass the request and response unchanged. The
existing CI test command can exercise the new cases without a workflow edit.

## Acceptance checks

1. A version-2 request and matching response recommend only offered IDs while
   preserving mandatory, explicit, manual-only and read-only checks.
2. A response for task A is invalid for task B with the same versions and
   offers. Repeat with otherwise identical tasks and verify that separate
   callback invocations still have different IDs.
3. Missing, malformed or duplicate-key IDs in either the request or response,
   mismatched IDs, and version-1 requests or responses deny. Abstentions also
   require the matching ID.
4. The request remains within 4,096 UTF-8 bytes, the response within 1,024,
   and the local worker frame within 6,144; oversized inputs deny.
5. Both `Agent` and model `Skill` callbacks, plus direct typed `/skill`, deny
   stale responses. No online fallback or actual dispatch occurs in tests.
6. Existing synthetic behavior, including callback error and timeout denial,
   remains covered; documentation states the v1-to-v2 break for offline
   adapters rather than silently accepting old replies.
7. A response carrying the correct current ID still denies if the second
   host-owned authority snapshot changes or the ordinary host permission
   decision is no longer `allow`.

## Decision boundary

Reviewing or merging this proposal does not authorize its implementation.
The owner would need to approve this exact bounded contract revision in a
separate approval-register event before code changes. The approval should not
be read as Stage 4B host-proof authority or as a gate-guard exception for a
future protected PR head.
