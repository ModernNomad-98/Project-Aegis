# Offline host bridge candidate (Stage 4A)

This package is for maintainers of the issue #101 setup router. Stage 4A is
the offline bridge stage of that plan, tested only with invented inputs;
Stage 4B is the later, separately approved real-host proof. The package
exercises a candidate Claude Agent software development kit (SDK) callback
shape with invented host facts. It does not open an SDK session, invoke `query()`, start
Claude, connect a provider, or dispatch an actual agent or skill. The TypeScript
module has only Node built-in runtime imports; its SDK type import is erased.
The Python worker uses the shipped
`tools.aegis_setup.routing_contract` validator. Installing the pinned SDK
packages makes continuous integration (CI) resolution reproducible but the offline tests do not import
or execute those packages.

The owner approved only the bounded [Stage 4A proposal](../../../docs/roadmaps/aegis-setup-package-4a-host-preparation-proposal.md).
The host must supply a fresh `AuthoritySnapshot` before each proposed dispatch.
It owns eligibility, mandatory and explicit choices, manual invocation,
catalog and policy versions, local-only destination, and ordinary permission.
The bridge asks a synthetic `advice` function for a reply, checks a second
snapshot, then sends one bounded frame to a local Python process. The worker
runs without site-package startup and inherits only the minimum path/operating system (OS)/temp
environment values, not provider credentials. The worker
validates the existing 4,096-byte request and 1,024-byte response contracts.
For each callback, the bridge creates a fresh 128-bit `request_id` using Node's
cryptographic random source. The closed version-2 request and response include
that 32-character lowercase hexadecimal identifier (ID), which the Python worker checks
for an exact echo. Version-1 offline adapters must migrate; there is no v1
fallback. The ID prevents an earlier callback's response from being reused,
but is not an authorization token. The request, response and worker frame
remain limited to 4,096, 1,024 and 6,144 bytes of UTF-8 (Unicode text encoding) respectively.
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
