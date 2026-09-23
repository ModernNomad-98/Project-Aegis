# Aegis delivery control plane

The **delivery control plane** is a safety kernel for continuing a long-running
engineering task after a pause, crash or uncertain external effect. It is for
Project Aegis maintainers building controlled delivery workflows. Its job is
to decide, from durable facts, whether a proposed next operation still has
valid authority, budget, identity and evidence. The shipped package is an
**offline synthetic kernel**: it demonstrates those decisions with fake
authorities and targets, not with GitHub, a model provider or a production
deployment.

For example, if a synthetic target accepts a change but the controller crashes
before receiving the receipt, the controller must not assume the change failed
and send it again. It retains the outstanding operation and budget liability,
then reconciles the target's durable receipt. If the evidence is missing or
contradictory, further dispatch stays blocked. This is the problem the kernel
is designed to solve.

Control-plane work package 003A (CP-WP-003A) added offline negative capability
probes in `capabilities.py` and tests. The dispatch coordinators reject a
lookalike authority or target before committing an intent. Passing synthetic
source, freshness, containment, owned-path, evidence or accounting probes
does not authorize a real route; `require_real_dispatch` always denies it. A
selected source and host, independent freshness proof, actual evidence and
billing policy remain open work-package 003 gates.

## Boundary

The [control-plane design](../../docs/design/resumable-control-plane-v1.md)
defines the full intended system. The
[backlog](../../docs/roadmaps/resumable-control-plane-backlog.md) separates
delivered synthetic behavior from real source, host and integration gates.
**Control-plane work package 002** delivered the offline state and recovery
kernel. **Work package 003A** delivered a bounded offline capability-proof
increment; it did not establish a real authority source or host. These numbers
name work packages, not runtime versions.

## How a controlled operation works

1. **Accept an exact plan.** The kernel binds a repository, source revision,
   item, policy and validation checks to one immutable operation identity.
2. **Check authority and reserve capacity.** A synthetic issuer grants a
   one-use capability. The kernel verifies its current status, reserves a
   bounded budget and occupies one repository-wide outstanding operation slot.
3. **Commit intent before contact.** A transaction records permission use,
   budget liability, the operation intent and its expected target identity.
   The synthetic adapter may contact its target only after that commit.
4. **Record receipts and validation.** The synthetic target and validator keep
   separate durable ledgers. A receipt or validator result is checked against
   the exact operation, then applied once. An uncertain result retains the
   slot and worst-case liability until authoritative reconciliation.
5. **Recover conservatively.** After restart, the kernel replays its events,
   checks hashes and source freshness, and preserves fences from pauses,
   revocations, stop requests or conflicting observations. It never converts
   an unknown effect into permission to retry.

The lifecycle includes explicit pause, resume, stop and finalization routes.
Design identifiers such as `T03` (transition 03, dispatch intent) and `T27`
(transition 27, validator intent) refer to rows in the
[design transition table](../../docs/design/resumable-control-plane-v1.md);
they are not commands a user should type.

## What the package files do

**Reading key:** SQLite is the embedded database engine that stores local
state in a file. SHA-256 (Secure Hash Algorithm 256-bit) is a digest of bytes:
it helps detect changes against a trusted value, but does not itself grant
authority or prove the source is fresh.

| File | Responsibility |
| --- | --- |
| `contracts.py` | Define typed operation, event, permission, budget and result records; reject malformed or ambiguous inputs. |
| `engine.py` | Apply allowed state transitions, fences, validation results, pauses, stops and recovery rules. |
| `storage.py` | Keep an append-only event chain and transactionally owned projections in a repository-scoped SQLite database. |
| `authority.py` | Verify and redeem synthetic issuer permissions; a local permission is not a real external approval. |
| `adapters.py` | Provide the synthetic execution and validator targets with separate durable receipt ledgers. There are no real adapters. |
| `dispatch.py` | Coordinate permission, intent and synthetic target contact order; compare a returned receipt with the exact committed operation before intake. |
| `evidence.py` | Canonicalize a synthetic evidence record, create a new evidence file and return its SHA-256 hash. Receipt and authority checks occur in the dispatch, authority and storage paths. |
| `owned_paths.py` | Resolve the user-state root and reject unsafe links, ownership and path substitutions. |
| `cli.py` | Provide a read-only command-line interface for capabilities, status and verification. No lifecycle mutation command is exposed. |

The kernel allows one outstanding synthetic operation per repository. The
operation slot remains occupied while an effect, validator or accounting
obligation is unresolved. Event replay is checked against the stored sequence,
predecessor hashes and identity bindings before projections are trusted.

## Read-only commands

From the Project Aegis source checkout, this command reports what the local
package can actually do without opening a state database:

```powershell
python -m tools.aegis_delivery_control --repository-id example-project capabilities
```

`status` reads the repository's local state if it exists. It does **not**
establish that the state is fresh against an independent source:

```powershell
python -m tools.aegis_delivery_control --repository-id example-project status
```

`verify` compares the stored state with an independently supplied freshness
vector and checks synthetic issuer evidence. It requires both a vector file
containing exactly `repository_id`, `catalog_head` and `run_heads`, and a
separate file containing the synthetic issuer key under
`synthetic_issuer_key_hex`. These are test inputs, not production credentials.
Both files are JavaScript Object Notation (JSON). In the expected vector,
`repository_id` must match the command's repository identity, `catalog_head`
is the independently expected catalog revision, and `run_heads` maps each run
identifier to its independently expected head. The separate key file has
exactly `synthetic_issuer_key_hex`, a hexadecimal synthetic issuer key from
the same offline test authority. The
[command-line test fixture](tests/test_dispatch.py) shows the two JSON shapes
and obtains their values from a synthetic setup; `verify --help` lists the
required file arguments. That fixture exercises the command shape, not an
independent freshness proof. Do not derive the expected vector from the state
being checked when making a freshness claim, or substitute a real credential.
Create both files from an
independently trusted synthetic fixture before using these ordinary path
examples:

```powershell
python -m tools.aegis_delivery_control --repository-id example-project verify --expected-vector .\vector.json --authority-key-file .\synthetic-key.json
```

Verification denies a missing database, mismatched identity or head, malformed
input, unsafe path, or unavailable source fact. A state file's own contents
cannot prove its freshness. The command reads only; it does not repair or
advance a run.

## Storage and current guarantees

State lives outside the repository checkout in a user-local directory:

- Windows: the operating system's LocalAppData known folder, then
  `ProjectAegis/control-plane/<repository-hash>/state.sqlite3`.
- Linux: the `XDG_STATE_HOME` environment variable selects the user-state
  directory when set; otherwise use
  `$HOME/.local/state/project-aegis/control-plane/<repository-hash>/state.sqlite3`.

The database uses SQLite transactions, rollback journaling and
`synchronous=FULL`, SQLite's request to sync transaction writes to storage.
The process-crash tests do not prove physical power-loss durability. A stable
operating-system lock excludes cooperating writers. The synthetic target and
validator each have their own SQLite
ledger, so a restarted controller can reconcile an accepted effect or result
without issuing it again. Checked paths reject unsafe links and ownership;
unsupported path guarantees close dispatch.

Tests establish process-crash and transaction-rollback behavior for the
supported local fixtures. They do not prove power-loss durability of a disk,
real source-atomic approval across other consumers, independent monotonic
freshness, real-host process containment, a production evidence access policy,
or billing reconciliation. Those remain later gates. A successful synthetic
test never authorizes an external side effect.

## Tests and further reading

The focused offline suite runs without a real target or provider:

```powershell
python -m unittest discover -s tools/aegis_delivery_control/tests -p "test_*.py" -v
```

Record the exact revision, platform and skips with results. The
[work package 002 review](../../docs/evidence/control-plane/cp-wp-002-codex-handoff.md)
contains the accepted transition, crash and recovery evidence. The
[work package 003A proposal](../../docs/roadmaps/cp-wp-003-offline-proof-proposal.md)
explains the delivered synthetic proof boundary. The
[backlog](../../docs/roadmaps/resumable-control-plane-backlog.md) is the
current status source for any real integration claim.
