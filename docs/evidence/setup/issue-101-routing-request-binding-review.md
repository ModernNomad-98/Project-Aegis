# Issue #101 offline routing request binding review

This record covers the bounded version-2 synthetic routing change proposed in
[the request-binding proposal](../../roadmaps/aegis-setup-routing-request-binding-proposal.md).
It is an implementation review input, not evidence of a real host integration.

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

From the isolated implementation worktree rooted at `origin/main` `6d6fefb`:

```text
python -B -m unittest tools.aegis_setup.tests.test_routing_contract -v
node --test tools/aegis_setup/host_bridge/bridge.test.ts
python -B scripts/validate-skills.py
```

The Python suite covers v2 acceptance, malformed/missing/duplicate IDs, stale
responses, version 1 rejection and mismatched abstention. The Node suite covers
fresh IDs for repeated identical callbacks, stale advice rejection across
Agent, model Skill and direct typed skill, and the existing authority and
worker failure cases. Record final command results and independent review at
the implementation PR before merge.

Stage 4B host proof, real routing behavior and any helper selection remain
separately gated.
