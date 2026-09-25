# Offline host bridge candidate (Stage 4A)

This package exercises a candidate Claude Agent SDK callback shape with
invented host facts. It does not open an SDK session, invoke `query()`, start
Claude, connect a provider, or dispatch an actual agent or skill. The TypeScript
module has only Node built-in runtime imports; its SDK type import is erased.
The Python worker uses the shipped
`tools.aegis_setup.routing_contract` validator. Installing the pinned SDK
packages makes CI resolution reproducible but the offline tests do not import
or execute those packages.

The owner approved only the bounded [Stage 4A proposal](../../../docs/roadmaps/aegis-setup-package-4a-host-preparation-proposal.md).
The host must supply a fresh `AuthoritySnapshot` before each proposed dispatch.
It owns eligibility, mandatory and explicit choices, manual invocation,
catalog and policy versions, local-only destination, and ordinary permission.
The bridge asks a synthetic `advice` function for a reply, checks a second
snapshot, then sends one bounded frame to a local Python process. The worker
runs without site-package startup and inherits only the minimum path/OS/temp
environment values, not provider credentials. The worker
validates the existing 4,096-byte request and 1,024-byte response contracts.
Only a recommendation that includes the actual target can pass. Unknown tools,
IDs and failures explicitly deny. A passed callback returns no permission
decision, so the host's normal permission flow still applies; it grants no
whole-task review completion.

For a local offline check from the repository root:

```text
npm ci --prefix tools/aegis_setup/host_bridge --ignore-scripts --no-audit --no-fund
node --test tools/aegis_setup/host_bridge/bridge.test.ts
```

The [review record](../../../docs/evidence/setup/issue-101-package-4a-offline-review.md)
states the lock and archive checks that must precede installation. The
scripts-disabled install downloads packages and uses disk space but has no
task-controlled external purchase. No real-host callback has been tested;
Stage 4B requires separate approval and evidence.
