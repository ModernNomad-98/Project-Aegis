# Shared Local-Resource Coordination for Parallel Agents

Supporting reference for agent-startup-context-gate. Use before any E2E or validation
run when parallel agents could share a local stack, port, database, lock file or fixture
set. This reference defines ownership, exclusive locking, the isolation alternative,
fail-safe stops and unique-prefix cleanup; it never authorizes deleting another run's
resources.

## Ownership

One owner per local stack, port and database at a time. The owner records the agent
identity, run id, held resources and expiry (ttl) before use, and no second agent uses a
shared mutable resource without an explicit ownership handoff recorded in the run log.

## Lock before E2E/validation

Before any E2E or validation run, atomically create an exclusive lock file
.local/stack.lock (or .local/<stack>.stack.lock). .local is untracked and never
committed. Use shell noclobber (set -C / O_CREAT|O_EXCL) and always release through
a trap so the lock is released after the run even on failure:

```bash
#!/bin/sh
set -u
LOCK=".local/stack.lock"
RUN_ID="$(date -u +%Y%m%dT%H%M%SZ)-$$"
mkdir -p "$(dirname "$LOCK")"
if ! ( set -C; printf 'owner=%s email=%s run=%s acquired=%s ttl_minutes=60\n' "$(git config user.name)" "$(git config user.email)" "$RUN_ID" "$(date -u +%FT%TZ)" > "$LOCK" ) 2>/dev/null; then
  echo "STOP: stack.lock is held; inspect owner/run/acquired and wait or escalate" >&2
  cat "$LOCK" >&2
  exit 1
fi
trap 'rm -f "$LOCK"' EXIT INT TERM
# run E2E/validation here; the trap releases the lock on success or failure
```

Foreign/stale rule: if the lock exists, read owner/run/acquired/ttl. If the owner is not
this agent, stop: it is a foreign lock and must never be stolen or deleted. If the owner
is this agent but the run is older than its ttl, stop, report the stale lock and require
owner confirmation before any removal. Release only your own lock through the trap.

## Isolation alternative

Isolation avoids a shared lock: give each agent its own isolated stacks, ports and
databases with unique names/prefixes, allocate ports from a recorded range, and never
reuse another agent's port. Isolated resources need no shared lock; record the isolation
mapping in the run log.

## Fixture cleanup (unique prefix only)

Clean up only the run's own unique prefix; print the exact cleanup command and target
paths before running it, never broad delete/reset, and record the result:

```bash
PREFIX="aegis-run-$RUN_ID"
cleanup_fixtures() { printf 'cleanup prefix %s\n' "$PREFIX"; find .local/fixtures -maxdepth 1 -name "$PREFIX*" -print -delete; }
trap 'cleanup_fixtures; rm -f "$LOCK"' EXIT INT TERM
# stop if any target outside the unique prefix would be removed
```

## Stop conditions

- The lock is held by another owner (foreign lock) → stop, inspect owner/run/acquired/ttl,
  wait or escalate; never delete it.
- A stale lock (owner is this agent, run beyond ttl) without owner confirmation → stop and
  report it; removal requires explicit owner confirmation recorded in the run log.
- Any cleanup would touch a path outside the run's unique prefix, or requires a broad
  delete/reset → stop; no broad cleanup is ever performed.
- Two agents would use one shared mutable stack/port/database without a recorded
  ownership handoff → stop and isolate or hand off explicitly.
