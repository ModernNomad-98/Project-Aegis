# Shared Local-Resource Coordination for Parallel Agents

Supporting reference for agent-startup-context-gate. Use before any E2E or validation
run when parallel agents could share a local stack, port, database, lock file or fixture
set. This reference defines ownership, exclusive locking, the isolation alternative,
fail-safe stops and unique-prefix cleanup; it never authorizes deleting another run's
resources.

## Ownership

One owner per local stack, port and database at a time. The owner records the agent
identity, run id, acquisition time and ttl before use, and no second agent uses a
shared mutable resource without an explicit ownership handoff recorded in the run log.

## Lock before E2E/validation

Before any E2E or validation run, atomically create an exclusive lock file
`.local/stack.lock` (or `.local/<stack>.stack.lock`). `.local` is untracked and never
committed. Use shell noclobber (`set -C` / `O_CREAT|O_EXCL`). The complete executable
example below records `owner/email/run/acquired/ttl_minutes`, installs the EXIT and
signal traps BEFORE acquiring the lock, owns a direct child workload, separates signal
handling from final cleanup, stops and reaps the child before releasing ownership,
refuses to delete a foreign/replaced lock, and exits without continuing the command
body after INT/TERM. Set `AEGIS_STACK_WORKLOAD` to the bounded direct-child command and
optionally `AEGIS_STACK_TTL_MINUTES` (default 120). Supported model is POSIX `sh` with a
direct child owned by this script (no descendant-tree guarantee); the zombie check uses
`ps` and falls back to the bounded kill check when `ps` is unavailable.

```bash
#!/bin/sh
set -u
LOCK="${AEGIS_STACK_LOCK:-.local/stack.lock}"
WORKLOAD="${AEGIS_STACK_WORKLOAD:-true}"
TTL_MINUTES="${AEGIS_STACK_TTL_MINUTES:-120}"
RUN_ID="$(date -u +%Y%m%dT%H%M%SZ)-$$"
ACQUIRED="$(date -u +%s)"
TOKEN="owner=$(git config user.name) email=$(git config user.email) run=$RUN_ID acquired=$ACQUIRED ttl_minutes=$TTL_MINUTES"
CHILD=""
CLEANED=0
stop_child() {
  if [ -n "$CHILD" ]; then
    if ! kill -0 "$CHILD" 2>/dev/null; then CHILD=""; return 0; fi
    state=$(ps -o stat= -p "$CHILD" 2>/dev/null || true)
    case "$state" in
      Z*) wait "$CHILD" 2>/dev/null || true; CHILD=""; return 0 ;;
    esac
    kill -TERM "$CHILD" 2>/dev/null || true
    i=0
    while kill -0 "$CHILD" 2>/dev/null && [ "$i" -lt 5 ]; do
      i=$((i+1)); sleep 1
      state=$(ps -o stat= -p "$CHILD" 2>/dev/null || true)
      case "$state" in
        Z*) wait "$CHILD" 2>/dev/null || true; CHILD=""; return 0 ;;
      esac
    done
    if kill -0 "$CHILD" 2>/dev/null; then
      echo "INCOMPLETE: owned workload still live after TERM; retaining ownership" >&2
      return 1
    fi
    wait "$CHILD" 2>/dev/null || true
    CHILD=""
  fi
  return 0
}
cleanup() {
  if [ "$CLEANED" -eq 1 ]; then return 0; fi
  if ! stop_child; then return 1; fi
  CLEANED=1
  if [ -f "$LOCK" ] && grep -q "run=$RUN_ID" "$LOCK" 2>/dev/null; then
    rm -f "$LOCK"
  fi
  return 0
}
on_signal() {
  trap - INT TERM
  echo "interrupted: stopping owned workload before release" >&2
  exit 130
}
trap 'cleanup' EXIT
trap 'on_signal' INT TERM
mkdir -p "$(dirname "$LOCK")"
if ! ( set -C; printf '%s\n' "$TOKEN" > "$LOCK" ) 2>/dev/null; then
  echo "STOP: stack.lock is held; inspect owner/run/acquired/ttl_minutes and wait or escalate" >&2
  cat "$LOCK" >&2 || true
  exit 1
fi
sh -c "$WORKLOAD" &
CHILD=$!
wait "$CHILD"; rc=$?
CHILD=""
cleanup
exit "$rc"
```

Foreign/stale rule: if the lock exists, read owner/email/run/acquired/ttl_minutes. If
the owner is not this agent, stop: it is a foreign lock and must never be stolen or
deleted. If the owner is this agent but `now - acquired > ttl_minutes * 60`, stop,
report the stale lock and require owner confirmation before any removal. Release only
your own lock, and only after the owned workload has stopped and been reaped; if
termination times out, retain ownership and report incomplete cleanup rather than
falsely declaring the resource free. Trap installation before acquisition closes the
signal window; cleanup marks itself complete only after a successful child stop. The
old process's cleanup must not delete a successor's lock: the token check refuses a
replaced ownership record. A shell token check plus unlink cannot prove arbitrary
adversarial atomicity; this is a bounded local guard, not a distributed-lock guarantee.

## Isolation alternative

Isolation avoids a shared lock: give each agent its own isolated stacks, ports and
databases with unique names/prefixes, allocate ports from a recorded range, and never
reuse another agent's port. Isolated resources need no shared lock; record the isolation
mapping in the run log. Use this documented full-resource-isolation option for
workloads outside the supported shell/direct-child model; it is a distinct scope
option, not proof that the shared-lock example is fixed.

## Fixture cleanup (unique prefix only)

Clean up only the run's own unique prefix; print the exact cleanup command and target
paths before running it, never broad delete/reset, and record the result. The signal
handler exits nonzero after cleanup; EXIT cleanup is idempotent:

```bash
#!/bin/sh
set -u
UNIQUE_PREFIX="aegis-run-${RUN_ID:?RUN_ID required}"
CLEANED=0
cleanup_fixtures() {
  if [ "$CLEANED" -eq 1 ]; then return 0; fi
  CLEANED=1
  printf 'cleanup prefix %s\n' "$UNIQUE_PREFIX"
  find .local/fixtures -maxdepth 1 -name "$UNIQUE_PREFIX*" -print -delete
}
on_signal() {
  trap - INT TERM
  cleanup_fixtures
  exit 130
}
trap 'cleanup_fixtures' EXIT
trap 'on_signal' INT TERM
# stop if any target outside the unique prefix would be removed
```

## Stop conditions

- The lock is held by another owner (foreign lock) -> stop, inspect owner/email/run/acquired/ttl_minutes,
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
