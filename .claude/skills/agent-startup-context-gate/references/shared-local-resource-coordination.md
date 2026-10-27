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

## Effective Identity Policy (guidance only; not enforced today)

**Status: guidance only; not a security boundary.** This repository does NOT enforce the identity gate described here. The earlier enforcement implementation in this PR was withdrawn after independent review; implementation is queued as backlog item DS-R1b. This is best-effort design guidance, not verified identity or complete enforcement.

A correct implementation should: use git var GIT_AUTHOR_IDENT/GIT_COMMITTER_IDENT as the effective identity with a separately recorded owner identity; accept only full same-scope config user.name+user.email (the same config scope; Git config is not role-specific, so require the pair to match the effective author pair or the effective committer pair), a full caller author+committer environment (both fields) with clean fallbacks, a single differing caller env override over a resolvable fallback, or a field-specific caller author OR committer override; read config key-exactly and reject duplicate keys and malformed/multiline/control values; validate raw git var output as exactly one strict identity line; clear ALL author and committer identity env vars when computing fallbacks; require same-scope AND same-role config pairing; require per-field justification. Known limits: inherited-global-only is not accepted; same-value caller env is inherited, not explicit; the same-value local/command config restatement exception applies only to config, not env; mixed config+one-field-env can be rejected when fallback cannot resolve; --show-scope/version dependencies and hook bypass via git commit --no-verify are disclosed. git var does not account for command-level git commit --author overrides; any future enforcement implementation must also verify the final commit identity or parse/reject --author (DS-R1b design item). No complete-enforcement, verified-identity, unbypassable, readiness or CI-green claim is made.

## Lock before E2E/validation

Before any E2E or validation run, create an exclusive lock DIRECTORY atomically
`.local/stack.lock` (or `.local/<stack>.stack.lock`). `.local` is untracked and never
committed. The executable example atomically creates the lock directory with mkdir,
writes the owner marker and token immediately inside the created directory, installs traps before acquisition,
reports contention separately from acquisition I/O errors, writes a ready marker before
the workload starts, and only removes a lock whose full stored token matches its own (or
a partially-created own lock with no token).
Platform policy: Linux is the required POSIX lane (exit 0, marker OK, required true). macOS is local/UNRUN only (no readiness claim). Windows is SKIP/UNRUN and a required skip stays nonzero; SKIP/UNRUN is never PASS and no all-skip success is accepted. Unsupported shell/tool capability is UNRUN, never a pass.

Set `AEGIS_STACK_WORKLOAD` to the bounded direct-child command (required; no silent
no-op) and optionally `AEGIS_STACK_TTL_MINUTES` (default 120). Run from the repo root
or set an absolute `AEGIS_STACK_LOCK`; the default lock path is caller-relative.
Supported model is POSIX `sh` with a direct
child owned by this script (no descendant-tree guarantee); zombie checks use `ps`.

```bash
#!/bin/sh
set -u
LOCK="${AEGIS_STACK_LOCK:-.local/stack.lock}"
while [ "${LOCK%/}" != "$LOCK" ]; do LOCK="${LOCK%/}"; done
if [ -z "$LOCK" ]; then echo "STOP: AEGIS_STACK_LOCK is empty" >&2; exit 2; fi
WORKLOAD="${AEGIS_STACK_WORKLOAD:-}"
if [ -z "$WORKLOAD" ]; then echo "STOP: AEGIS_STACK_WORKLOAD is required; refusing silent no-op" >&2; exit 2; fi
TTL_MINUTES="${AEGIS_STACK_TTL_MINUTES:-120}"
case "$TTL_MINUTES" in ''|*[!0-9]*|0) echo "STOP: AEGIS_STACK_TTL_MINUTES must be a positive integer" >&2; exit 2 ;; esac
umask 077
RUN_ID="$(date -u +%Y%m%dT%H%M%SZ)-$$"
ACQUIRED="$(date -u +%s)"
OWNER_NAME="$(git config user.name 2>/dev/null || true)"
OWNER_EMAIL="$(git config user.email 2>/dev/null || true)"
if [ -z "$OWNER_NAME" ] || [ -z "$OWNER_EMAIL" ]; then
  IDENT=$(git var GIT_AUTHOR_IDENT 2>/dev/null || true)
  OWNER_NAME=$(printf "%s\n" "$IDENT" | sed -n "s/^\(.*\) <\([^>]*\)>.*$/\1/p")
  OWNER_EMAIL=$(printf "%s\n" "$IDENT" | sed -n "s/^\(.*\) <\([^>]*\)>.*$/\2/p")
fi
if [ -z "$OWNER_NAME" ] || [ -z "$OWNER_EMAIL" ]; then
  echo "STOP: lock owner identity missing from configured and effective Git identity" >&2
  exit 1
fi
TOKEN="owner=$OWNER_NAME email=$OWNER_EMAIL run=$RUN_ID acquired=$ACQUIRED ttl_minutes=$TTL_MINUTES"
CHILD=""
CREATED_LOCK=0
CLEANED=0
CLEANING=0
STOP_ATTEMPTED=0
stop_child() {
  if [ "$STOP_ATTEMPTED" -eq 1 ]; then
    if [ -n "$CHILD" ] && kill -0 "$CHILD" 2>/dev/null; then echo "INCOMPLETE: stop already attempted; not waiting again" >&2; return 1; fi
    return 0
  fi
  STOP_ATTEMPTED=1
  if [ -n "$CHILD" ]; then
    if kill -0 "$CHILD" 2>/dev/null; then
      state=$(ps -o stat= -p "$CHILD" 2>/dev/null || true)
      case "$state" in Z*) wait "$CHILD" 2>/dev/null || true; CHILD=""; return 0 ;; esac
      kill -TERM "$CHILD" 2>/dev/null || true
      i=0
      while kill -0 "$CHILD" 2>/dev/null && [ "$i" -lt 5 ]; do
        i=$((i+1)); sleep 1
        state=$(ps -o stat= -p "$CHILD" 2>/dev/null || true)
        case "$state" in Z*) break ;; esac
      done
      state=$(ps -o stat= -p "$CHILD" 2>/dev/null || true)
      case "$state" in
        Z*) wait "$CHILD" 2>/dev/null || true; CHILD=""; return 0 ;;
      esac
      if kill -0 "$CHILD" 2>/dev/null; then
        kill -KILL "$CHILD" 2>/dev/null || true
        i=0
        while kill -0 "$CHILD" 2>/dev/null && [ "$i" -lt 5 ]; do
          i=$((i+1)); sleep 1
        done
      fi
      state=$(ps -o stat= -p "$CHILD" 2>/dev/null || true)
      case "$state" in Z*) wait "$CHILD" 2>/dev/null || true; CHILD=""; return 0 ;; esac
      if kill -0 "$CHILD" 2>/dev/null; then
        echo "INCOMPLETE: owned workload still live after TERM/KILL; retaining ownership" >&2
        return 1
      fi
      wait "$CHILD" 2>/dev/null || true
      CHILD=""
      return 0
    fi
    wait "$CHILD" 2>/dev/null || true
    CHILD=""
  fi
  return 0
}
cleanup() {
  if [ "$CLEANED" -eq 1 ]; then return 0; fi
  if [ "$CLEANING" -eq 1 ]; then return 0; fi
  CLEANING=1
  trap '' INT TERM
  # Generic child-lifetime rule: ALWAYS bound/stop/reap the owned direct child
  # BEFORE any token/ownership early return. Otherwise a still-live child holds
  # inherited stdout/stderr pipes and can hang the caller even when cleanup is
  # correctly reporting INCOMPLETE.
  if ! stop_child; then CLEANING=0; return 1; fi
  OWNED=0
  if [ -d "$LOCK" ]; then
    if [ -e "$LOCK/token" ]; then
      if ! current="$(cat "$LOCK/token" 2>/dev/null)" || [ -z "$current" ]; then
        echo "INCOMPLETE: lock token unreadable; ownership cannot be verified" >&2
        CLEANING=0; return 1
      fi
      if [ "$current" = "$TOKEN" ]; then OWNED=1; fi
    elif [ -e "$LOCK/owner.$RUN_ID" ]; then
      OWNED=1
    elif [ "$CREATED_LOCK" -eq 1 ] && [ -z "$(ls -A "$LOCK" 2>/dev/null)" ]; then
      OWNED=1
    fi
  fi
  if [ "$CREATED_LOCK" -eq 0 ] && [ "$OWNED" -eq 0 ]; then CLEANING=0; return 0; fi
  if [ "$OWNED" -eq 1 ] && [ -d "$LOCK" ]; then : > "$LOCK/abort" 2>/dev/null || true; fi
  if [ "$OWNED" -eq 1 ] && [ -f "$LOCK/workload.pid" ]; then rm -f "$LOCK/workload.pid" 2>/dev/null || true; fi
  if [ "$OWNED" -eq 1 ] && [ -d "$LOCK" ]; then
    current="$(cat "$LOCK/token" 2>/dev/null || true)"
    if [ "$current" = "$TOKEN" ] || [ ! -e "$LOCK/token" ]; then
      QUAR="$LOCK.quarantine.$RUN_ID"
      if ! mv "$LOCK" "$QUAR" 2>/dev/null; then
        echo "INCOMPLETE: cannot quarantine owned lock; evidence retained" >&2
        CLEANING=0; return 1
      fi
      if ! rm -rf "$QUAR"; then
        if [ ! -e "$LOCK" ] && mv "$QUAR" "$LOCK" 2>/dev/null; then
          echo "INCOMPLETE: quarantine removal failed; owned lock restored" >&2
        else
          echo "OWNERSHIP LOST: quarantine $QUAR retained; lock path $LOCK unavailable" >&2
        fi
        CLEANING=0; return 1
      fi
    fi
  fi
  CLEANED=1
  CLEANING=0
  return 0
}
on_signal() { sig="${1:-INT}"; trap '' INT TERM; echo "interrupted: stopping owned workload before release" >&2; if [ "$sig" = TERM ]; then exit 143; fi; exit 130; }
trap 'cleanup' EXIT
trap 'on_signal TERM' TERM
trap 'on_signal INT' INT
if [ -L "$LOCK" ]; then echo "STOP: refusing symlinked lock path" >&2; exit 2; fi
if ! mkdir -p "$(dirname "$LOCK")"; then echo "LOCK ERROR: cannot create lock parent directory" >&2; exit 2; fi
if ! mkdir "$LOCK"; then
  if [ -f "$LOCK" ]; then echo "LOCK MIGRATION: legacy lock file found at $LOCK; inspect and remove manually" >&2; exit 2; fi
  if [ -d "$LOCK" ]; then
    if [ -f "$LOCK/token" ]; then cat "$LOCK/token" >&2; fi
    echo "STOP: stack.lock is held; inspect owner/run/acquired/ttl_minutes and wait or escalate" >&2
    exit 1
  fi
  echo "LOCK ERROR: atomic lock mkdir failed" >&2
  exit 2
fi
CREATED_LOCK=1
if ! chmod 700 "$LOCK"; then rm -rf "$LOCK"; echo "LOCK ERROR: cannot set lock permissions" >&2; exit 2; fi
MARKER="$LOCK/owner.$RUN_ID"
if ! : > "$MARKER" 2>/dev/null; then rm -rf "$LOCK"; echo "LOCK ERROR: cannot create owner marker" >&2; exit 2; fi
if ! printf '%s\n' "$TOKEN" > "$LOCK/token"; then rm -rf "$LOCK"; echo "LOCK ERROR: cannot write lock token" >&2; exit 2; fi
# supervisor launch (stable test anchor)
sh -c '
  echo $$ > "$1/workload.pid" || exit 1
  : > "$1/ready" || exit 1
  i=0
  while [ ! -f "$1/ack" ] && [ ! -f "$1/abort" ] && [ "$i" -lt 5 ]; do i=$((i+1)); sleep 1; done
  [ -f "$1/abort" ] && exit 0
  [ -f "$1/ack" ] || exit 1
  exec sh -c "$2"
' sh "$LOCK" "$WORKLOAD" > "$LOCK/workload.out" 2> "$LOCK/workload.err" &
CHILD=$!
if ! : > "$LOCK/ack"; then cleanup; exit 2; fi
wait "$CHILD"; rc=$?
CHILD=""
if ! cleanup; then if [ "$rc" -eq 0 ]; then rc=1; fi; fi
exit "$rc"
```

Foreign/stale rule: if the lock exists, read owner/email/run/acquired/ttl_minutes from
the token. If the owner is not this agent, stop: it is a foreign lock and must never be
stolen or deleted. Tokenless lock: never delete a tokenless lock; if this run created it and it is empty, bootstrapping cleanup may remove that empty directory, otherwise preserve it. A readable token that does not exactly match this run's full token is a successor/foreign owner: preserve it and report; an unreadable token fails closed and retains ownership. If the owner is this agent but the stored age exceeds ttl_minutes,
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
CLEANED=0
RUN_BASE="${AEGIS_FIXTURE_BASE:-${TMPDIR:-/tmp}}"
if [ -L "$RUN_BASE" ]; then echo "STOP: refusing symlinked fixture base" >&2; exit 2; fi
if ! mkdir -p "$RUN_BASE" 2>/dev/null; then echo "FAILED: cannot create fixture base" >&2; exit 2; fi
UNIQUE_DIR=$(mktemp -d "$RUN_BASE/aegis-run-$RUN_ID.XXXXXX") || { echo "FAILED: cannot create private fixture dir" >&2; exit 2; }
if [ -L "$UNIQUE_DIR" ]; then echo "STOP: refusing symlinked fixture dir" >&2; exit 2; fi
if ! chmod 700 "$UNIQUE_DIR"; then echo "FAILED: cannot set fixture dir mode" >&2; exit 2; fi
case "$UNIQUE_DIR" in "$RUN_BASE"/aegis-run-*) ;; *) echo "STOP: fixture dir outside private base" >&2; exit 2 ;; esac
cleanup_fixtures() {
  if [ "$CLEANED" -eq 1 ]; then return 0; fi
  case "$UNIQUE_DIR" in
    "$RUN_BASE"/aegis-run-*) ;;
    *) echo "STOP: cleanup dir outside private fixture base" >&2; return 1 ;;
  esac
  printf 'cleanup command: rm -rf -- %s\n' "$UNIQUE_DIR" >&2
  printf 'cleanup targets: %s\n' "$UNIQUE_DIR" >&2
  if ! rm -rf -- "$UNIQUE_DIR"; then echo "FAILED: fixture removal failed: $UNIQUE_DIR" >&2; return 1; fi
  CLEANED=1
  return 0
}
on_signal() { trap '' INT TERM; cleanup_fixtures; exit 130; }
trap 'cleanup_fixtures' EXIT
trap 'on_signal' INT TERM
# stop if any target outside the unique prefix would be removed
```

## Effective Hook Path Resolution (core.hooksPath first)

Resolve the install/check path BEFORE inspecting or installing a hook. core.hooksPath
(local or effective config) takes precedence over the default hooks directory; resolve a
relative value against the repository top level and expand a leading tilde to HOME.
Use git rev-parse --git-path hooks/pre-commit only when core.hooksPath is unset; it
is the fallback, not the first authority. Hook-file presence is presence, never
authenticity: inspect contents/owner/mode and report the resolved path with the result.

```sh
#!/bin/sh
# AEGIS_HOOK_PATH_RESOLVE (resolve core.hooksPath first; git rev-parse fallback only when unset)
set -u
HOOKS_PATH=$(git config --get core.hooksPath 2>/dev/null || true)
if [ -n "$HOOKS_PATH" ]; then
  case "$HOOKS_PATH" in
    '~/'*) HOOKS_DIR="$HOME/$(printf '%s' "$HOOKS_PATH" | sed 's|^~/||')" ;;
    '~') HOOKS_DIR="$HOME" ;;
    /*) HOOKS_DIR="$HOOKS_PATH" ;;
    *) TOP=$(git rev-parse --show-toplevel 2>/dev/null) || { echo 'STOP: not a Git repository' >&2; exit 2; }; HOOKS_DIR="$TOP/$HOOKS_PATH" ;;
  esac
else
  HOOK_DIR=$(git rev-parse --git-path hooks 2>/dev/null) || { echo 'STOP: cannot resolve Git hooks directory' >&2; exit 2; }
  HOOKS_DIR="$HOOK_DIR"
fi
printf '%s\n' "$HOOKS_DIR/pre-commit"
```

CL-13 regression: relative and tilde values resolve from core.hooksPath before the
git rev-parse --git-path fallback; absolute values are used as-is.
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
