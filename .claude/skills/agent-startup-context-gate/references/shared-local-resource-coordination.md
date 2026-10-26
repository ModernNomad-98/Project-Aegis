# Shared Local-Resource Coordination for Parallel Agents

Supporting reference for agent-startup-context-gate. Use before any E2E or validation
run when parallel agents could share a local stack, port, database, lock directory or
fixture set. This reference defines ownership, exclusive locking, the isolation
alternative, fail-safe stops and unique-prefix cleanup; it never authorizes deleting
another run's resources.

## Ownership

One owner per local stack, port and database at a time. The owner records the agent
identity, run id, acquisition time and ttl before use, and no second agent uses a
shared mutable resource without an explicit ownership handoff recorded in the run log.

## Lock before E2E/validation

Before any E2E or validation run, create an exclusive lock DIRECTORY atomically
`.local/stack.lock` (or `.local/<stack>.stack.lock`). `.local` is untracked and never
committed. The executable example writes the token to a unique temp directory, then
atomically renames it to the lock path; it installs traps before acquisition, reports
contention separately from acquisition I/O errors, writes a ready marker before the
workload starts, and only removes a lock whose full stored token matches its own.
Set `AEGIS_STACK_WORKLOAD` to the bounded direct-child command and optionally
`AEGIS_STACK_TTL_MINUTES` (default 120). Supported model is POSIX `sh` with a direct
child owned by this script (no descendant-tree guarantee); zombie checks use `ps`.

```bash
#!/bin/sh
set -u
LOCK="${AEGIS_STACK_LOCK:-.local/stack.lock}"
WORKLOAD="${AEGIS_STACK_WORKLOAD:-true}"
TTL_MINUTES="${AEGIS_STACK_TTL_MINUTES:-120}"
RUN_ID="$(date -u +%Y%m%dT%H%M%SZ)-$$"
ACQUIRED="$(date -u +%s)"
OWNER_NAME="$(git config user.name 2>/dev/null || true)"
OWNER_EMAIL="$(git config user.email 2>/dev/null || true)"
if [ -z "$OWNER_NAME" ] || [ -z "$OWNER_EMAIL" ]; then
  echo "STOP: lock owner identity is missing; set git user.name/user.email before acquiring the lock" >&2
  exit 1
fi
TOKEN="owner=$OWNER_NAME email=$OWNER_EMAIL run=$RUN_ID acquired=$ACQUIRED ttl_minutes=$TTL_MINUTES"
CHILD=""
CLEANED=0
TMP=""
stop_child() {
  pid="$CHILD"
  if [ -z "$pid" ] && [ -f "$LOCK/workload.pid" ]; then pid="$(cat "$LOCK/workload.pid" 2>/dev/null || true)"; fi
  if [ -n "$pid" ]; then
    if kill -0 "$pid" 2>/dev/null; then
      state=$(ps -o stat= -p "$pid" 2>/dev/null || true)
      case "$state" in Z*) wait "$pid" 2>/dev/null || true; CHILD=""; return 0 ;; esac
      kill -TERM "$pid" 2>/dev/null || true
      i=0
      while kill -0 "$pid" 2>/dev/null && [ "$i" -lt 5 ]; do
        i=$((i+1)); sleep 1
        state=$(ps -o stat= -p "$pid" 2>/dev/null || true)
        case "$state" in Z*) break ;; esac
      done
      if kill -0 "$pid" 2>/dev/null; then
        echo "INCOMPLETE: owned workload still live after TERM; retaining ownership" >&2
        return 1
      fi
    fi
    [ "$pid" = "$CHILD" ] && wait "$CHILD" 2>/dev/null || true
    CHILD=""
  fi
  return 0
}
cleanup() {
  if [ "$CLEANED" -eq 1 ]; then return 0; fi
  if [ -d "$LOCK" ]; then : > "$LOCK/abort" 2>/dev/null || true; fi
  if ! stop_child; then return 1; fi
  if [ -d "$LOCK" ]; then
    current="$(cat "$LOCK/token" 2>/dev/null || true)"
    if [ "$current" = "$TOKEN" ]; then
      if ! rm -f "$LOCK"; then echo "INCOMPLETE: failed to remove owned lock" >&2; return 1; fi
    fi
  fi
  if [ -n "$TMP" ] && [ -d "$TMP" ]; then rm -rf "$TMP" 2>/dev/null || true; fi
  CLEANED=1
  return 0
}
on_signal() { trap - INT TERM; echo "interrupted: stopping owned workload before release" >&2; exit 130; }
trap 'cleanup' EXIT
trap 'on_signal' INT TERM
if ! mkdir -p "$(dirname "$LOCK")"; then echo "LOCK ERROR: cannot create lock parent directory" >&2; exit 2; fi
TMP="$LOCK.tmp.$RUN_ID"
if ! mkdir "$TMP"; then echo "LOCK ERROR: cannot create temporary lock directory" >&2; exit 2; fi
if ! printf '%s\n' "$TOKEN" > "$TMP/token"; then rm -rf "$TMP"; echo "LOCK ERROR: cannot write lock token" >&2; exit 2; fi
if ! ln -s "$TMP" "$LOCK" 2>/dev/null; then
  if [ -L "$LOCK" ] || [ -e "$LOCK" ]; then
    if [ -f "$LOCK/token" ]; then cat "$LOCK/token" >&2; fi
    echo "STOP: stack.lock is held; inspect owner/run/acquired/ttl_minutes and wait or escalate" >&2
    rm -rf "$TMP"; exit 1
  fi
  rm -rf "$TMP"
  echo "LOCK ERROR: atomic lock acquisition failed" >&2
  exit 2
fi
LOCK_LINK=1
sh -c '
  echo $$ > "$1/workload.pid" || exit 1
  : > "$1/ready" || exit 1
  i=0
  while [ ! -f "$1/ack" ] && [ ! -f "$1/abort" ] && [ "$i" -lt 5 ]; do i=$((i+1)); sleep 1; done
  [ -f "$1/abort" ] && exit 0
  [ -f "$1/ack" ] || exit 1
  exec sh -c "$2"
' sh "$LOCK" "$WORKLOAD" &
CHILD=$!
if ! : > "$LOCK/ack"; then cleanup; exit 2; fi
wait "$CHILD"; rc=$?
CHILD=""
if ! cleanup; then if [ "$rc" -eq 0 ]; then rc=1; fi; fi
exit "$rc"
```

Foreign/stale rule: if the lock exists, read owner/email/run/acquired/ttl_minutes from
the token. If the owner is not this agent, stop: it is a foreign lock and must never be
stolen or deleted. If the owner is this agent but `now - acquired > ttl_minutes * 60`,
stop, report the stale lock and require owner confirmation before removal. Release only
your own lock, only after the owned workload has stopped and been reaped, and only when
the full stored token matches exactly. Acquisition errors are reported separately with
exit 2; contention exits 1. The temp directory is unique to the run, so a signal before
the atomic rename can only remove this run's temp/lock, never a successor's.

## Isolation alternative

Isolation avoids a shared lock: give each agent its own isolated stacks, ports and
databases with unique names/prefixes, allocate ports from a recorded range, and never
reuse another agent's port. Isolated resources need no shared lock; record the isolation
mapping in the run log. Use this documented full-resource-isolation option for
workloads outside the supported shell/direct-child model; it is a distinct scope
option, not proof that the shared-lock example is fixed.

## Fixture cleanup (unique prefix only)

Clean up only the run's own unique prefix; validate RUN_ID against a safe character set
before building the glob, print the exact cleanup command and target paths, and record
the result. The signal handler exits nonzero after cleanup; EXIT cleanup is idempotent:

```bash
#!/bin/sh
set -u
RUN_ID="${RUN_ID:?RUN_ID required}"
case "$RUN_ID" in *[!A-Za-z0-9._-]*) echo "STOP: unsafe RUN_ID" >&2; exit 2 ;; esac
UNIQUE_PREFIX="aegis-run-$RUN_ID"
CLEANED=0
cleanup_fixtures() {
  if [ "$CLEANED" -eq 1 ]; then return 0; fi
  CLEANED=1
  # find matches are checked against the literal prefix before deletion
  printf 'cleanup prefix %s\n' "$UNIQUE_PREFIX"
  find .local/fixtures -maxdepth 1 -name "$UNIQUE_PREFIX*" -print
}
on_signal() { trap - INT TERM; cleanup_fixtures; exit 130; }
trap 'cleanup_fixtures' EXIT
trap 'on_signal' INT TERM
# stop if any target outside the unique prefix would be removed
```

## Stop conditions

- The lock is held by another owner (foreign lock) -> stop, inspect owner/run/acquired/ttl_minutes,
  wait or escalate; never delete it.
- A stale lock (owner is this agent, age beyond ttl_minutes) without owner confirmation -> stop and
  report it; removal requires explicit owner confirmation recorded in the run log.
- The owned workload is still live after the bounded stop window -> retain ownership and
  report incomplete cleanup; never report the resource free.
- Any cleanup would touch a path outside the run's unique prefix, or requires a broad
  delete/reset -> stop; no broad cleanup is ever performed.
- Two agents would use one shared mutable stack/port/database without a recorded
  ownership handoff -> stop and isolate or hand off explicitly.
- Unsupported platform/shell/descendant model -> use the isolation alternative or record
  an explicit UNRUN/skip; never treat an unsupported run as a pass.
