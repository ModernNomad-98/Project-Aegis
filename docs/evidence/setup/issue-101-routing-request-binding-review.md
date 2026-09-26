# Issue #101 offline routing request binding review

This record covers the bounded version-2 synthetic routing change proposed in
[the request-binding proposal](../../roadmaps/aegis-setup-routing-request-binding-proposal.md).
It is an implementation review input, not evidence of a real host integration.
Here, **SDK** means software development kit, the host's application
interface; **Agent** means the host's agent-dispatch route; and **Skill** means
a named instruction/tool capability selected by the host. The bridge handles
Agent, model Skill and direct typed-skill dispatch, but the host keeps the
permission decision.

## Contract and authority

- The bridge creates a new 16-byte cryptographically random `request_id` for
  each callback evaluation and sends its 32-character lowercase hexadecimal
  encoding with the version-2 request.
- Python validates the closed request and response schemas, ID shape and exact
  response echo, including abstention. Version 1 fails closed. The ID is a
  correlation value, not a permission credential.
- The existing host-owned snapshot recheck, local-only destination, normal
  permission decision, explicit and mandatory selections, manual invocation,
  read-only checks, and Python worker target check remain in force.
- All checks use invented local fixtures. No SDK session, provider, credential,
  VM, deployment or real callback was used.

## Verification

The isolated implementation worktree began from `origin/main` `6d6fefb`.
The completed PR #319 merged exact head
`550151dcf286f8ec64480bc91f47e390454417d2` as
`a59c015c01b4035ab1a438533736134f96deac13` at 2026-09-26 02:24:21
UTC. These offline commands were rerun against the merged implementation:

```text
python -B -m unittest tools.aegis_setup.tests.test_routing_contract -v
node --test tools/aegis_setup/host_bridge/bridge.test.ts
python -B scripts/validate-skills.py
```

Results: **12 Python tests passed**, **14 Node tests passed**, and **185 skills
validated with zero warnings**. The Python suite covers v2 acceptance,
malformed, missing and duplicate IDs, stale responses, version 1 rejection
and mismatched abstention. The Node suite covers
fresh IDs for repeated identical callbacks, stale advice rejection across
Agent, model Skill and direct typed skill, and the existing authority and
worker failure cases. The implementation had independent contract and
authority review before merge; the review focused on ID binding, fail-closed
parsing, host permission ownership and the no-real-host boundary. The exact
PR head then passed [Linux skill validation, Windows offline checks and
`gate-guard`](https://github.com/ModernNomad-98/Project-Aegis/actions/runs/36211342637).
The [PR #319 merge receipt](https://github.com/ModernNomad-98/Project-Aegis/pull/319)
records the final head and merge. [APR-043](../../approvals/APPROVAL_REGISTER.md#aegis-apr-043-consumption-of-issue-101-offline-routing-grant)
records consumption of the bounded APR-040 grant.

Stage 4B host proof, real routing behavior and any helper selection remain
separately gated.
