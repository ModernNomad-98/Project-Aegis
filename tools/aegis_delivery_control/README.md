# Aegis delivery control kernel

This package is the CP-WP-002 offline state and recovery kernel. It provides a
deterministic transition authority, a repository-scoped SQLite state owner,
durable effect/use/budget/slot invariants, and a durable synthetic target
fixture. It is not a delivery integration.

## Boundary

- Only `SyntheticAuthority`, `SyntheticExecutionAdapter` and
  `SyntheticValidatorAdapter` exist.
- No network, provider, credential, shell, subprocess, Git mutation,
  deployment, production-data or real execution interface exists.
- The CLI is read-only. Lifecycle mutations are not exposed as commands.
- `SyntheticDispatchCoordinator` is the supported dispatch path: it authorizes
  T03, commits intent and capability redemption, then contacts the synthetic
  target. A committed intent is never silently redispatched after a crash.
- `SyntheticValidationCoordinator` commits a distinct T27 validator sub-intent
  before contacting the synthetic validator ledger. T24 intake reconstructs a
  final result from that canonical ledger, records it once, and leaves it
  unapplied for a later T11/T12 command.
- A local permission-use reservation is accounting, not real human authority.
- Recovery requires an independently obtained repository identity, catalog
  head, and complete run-id/head vector. A self-consistent SQLite file is not
  freshness proof, and an omitted or additional run fails verification.

## Storage and crash model

The state owner uses one standard-library SQLite database with foreign keys,
rollback-journal mode and `synchronous=FULL`. Each intent transaction commits
the event, effect index, synthetic permission use, budget reservation, command
outcome and repository-wide outstanding slot together. Budget settlement and
slot release are similarly atomic and append to the same run/catalog event
chain, so the independently supplied freshness vector advances with accounting.
Supported dispatch opens both controller and target ledgers only at the
repository-derived canonical state root; alternate roots are rejected.

The synthetic target uses a separate SQLite ledger. Its accepted effect and
receipt survive a controller restart, allowing a fresh adapter instance to
reconcile a lost receipt without contacting the target again.
The synthetic validator uses another repository-scoped SQLite ledger. Writes
require the exact issued validator capability, and a lost final result can be
reconciled without rerunning validation. Validator reservations are subordinate
to the existing operation slot; an active validator prevents slot release.

Tests establish process-crash and transaction-rollback behavior. They do not
establish power-loss durability for a filesystem, disk controller or host.
Unsupported or uncertain guarantees close dispatch.

The default database location is outside the checkout:

- Windows: `%LOCALAPPDATA%/ProjectAegis/control-plane/<repo-id-hash>/state.sqlite3`
- Linux: `${XDG_STATE_HOME:-$HOME/.local/state}/project-aegis/control-plane/<repo-id-hash>/state.sqlite3`

The stable `writer.lock` supplies cooperative OS-backed writer exclusion. It is
never deleted to take ownership and does not replace the durable outstanding
operation slot.

## Commands

```powershell
python -m tools.aegis_delivery_control --repository-id <id> capabilities
python -m tools.aegis_delivery_control --repository-id <id> status
python -m tools.aegis_delivery_control --repository-id <id> verify --expected-vector <json-file>
```

`status` reports stored facts without verifying freshness. `verify` requires a
JSON object containing exactly `repository_id`, `catalog_head`, and `run_heads`
obtained independently of the database; any identity, inventory, or head
difference fails closed.

## Validation

```powershell
python -m unittest discover -s tools/aegis_delivery_control/tests -v
```

The tests cover the T01-T28 transition registry and deny-by-default behavior,
atomic intent rollback and replay, mediated T03 dispatch, durable cross-instance
claim redemption in one state database, budget uncertainty/release rules,
settlement-tail freshness, projection tamper rejection, restart-safe lost-receipt
reconciliation, pre-commit settlement rollback, post-commit settlement replay
without duplicate slot release, T27 validator-intent crash/replay and guard
behavior, T24 canonical result intake without application, unknown-accounting
reconciliation, active-validator slot retention, and cross-process writer
exclusion. The backlog remains the source of truth for acceptance cases not yet
implemented, including complete transition application and filesystem
ownership/reparse/path-swap enforcement.