# L3 containment: Claude Code CLI container profile

This page records the one containment result in this repository: **L3
(container confinement) is qualified for the Claude Code CLI only when it is
launched through the Aegis container described here.** Every other host status
in the [host status matrix](README.md#host-status-matrix) is unchanged.

## What L1, L2 and L3 mean here

- **L1, session gate:** the host refuses to start a session. Not achieved
  anywhere in this repository; the SessionStart hook is still not enforcing.
- **L2, tool gate:** a per-tool check, the [Aegis Guard CLI]
  (../../tools/aegis_guard/cli.py), decides each tool call. This is a policy
  decision, not confinement.
- **L3, containment:** the host runs inside an operating-system or container
  boundary it cannot escape by ignoring exit `10`: a read-only root, dropped
  capabilities, no privilege escalation, a non-root user and egress only
  through an allow-list proxy.

## Scope

**L3 applies only when the CLI is started through this container/launcher.**
Native Claude Code on Windows remains L2. A user who starts the CLI outside
the container bypasses L3 entirely, and nothing here constrains that run.
The container launch is the boundary; no host hook supplies it.

## Profile

| Item | Exact value |
| --- | --- |
| Host | Windows 11, **Docker Engine 29.9.2** (Docker Desktop on Windows; Desktop version not recorded), Linux containers |
| Claude image | `aegis-claude-l3:2.1.311-python` |
| Claude image digest | `sha256:1c4e965c06f8478c57eff62bc25fbc0db94b915539fb117f2938a7675d639e86` |
| Egress proxy image | `aegis-egress-proxy:1` |
| Egress proxy digest | `sha256:41714c3eef0be68a904f1e379391197231c52d02759a03f75b95f9a2c4be528e` |
| Internal network | `aegis-int`, id `b71aa24770e1426601e3b3f2f47532e8d8635488b0dc8e6525bc3c9462262921`, `internal=true` |
| Root filesystem | read-only |
| Capabilities | `--cap-drop ALL` |
| Privilege escalation | `no-new-privileges` |
| User | uid `1000`, non-root |
| `/tmp` | `tmpfs`, writable and not persisted |
| Workspace | `/work`, mounted read-write; the Aegis checkout is mounted `/aegis`, read-only |
| Claude auth | the host's `<host-home>/.claude`, mounted read-only; no credential is copied into the image or printed |
| Egress | `HTTPS_PROXY=http://aegis-proxy:3128`; the proxy allows only `CONNECT api.anthropic.com:443` and answers `403` to every other target |

`internal=true` means the container network has no route off the host: a
process inside cannot reach the internet except through the proxy.

## Results

| Test | Observed result | What it shows |
| --- | --- | --- |
| Claude API call through the proxy | OK, exit `0` | The allow-listed endpoint works through the proxy. |
| Bash `echo hi` | Blocked by the PreToolUse hook before execution | The L2 tool gate still runs inside the container. |
| Read `README.md` | Allowed, content `hello` | Reads inside the mounted repository work. |
| Read `.env` | Blocked by policy `**/.env` | Secret paths stay denied under containment. |
| Write `/work/allowed.txt` (Claude tool) | Created, content `OK`, exit `0` | The read-write workspace takes writes from the host tool path. |
| Direct egress to `1.1.1.1:80` | `Network is unreachable` | The internal network has no route out. |
| Proxy `CONNECT` to `1.1.1.1:443` | `HTTP/1.1 403 Forbidden` | The proxy refuses every non-allow-listed target. |
| Canary container write `/work/canary.txt` | `Read-only file system`; host canary unchanged | Control run in a separate container started with `/work:ro`: a read-only mount cannot modify the host workspace. |
| Write `/etc/passwd` | `Permission denied` | The write did not land; the non-root user has no writable path there. |

The workspace row and the canary row are two different containers, not one
contradictory result. The Claude container mounts `/work` read-write and its
Write tool created `/work/allowed.txt`. The canary control was launched with
`/work:ro` and refused its write, which confirms that the mount flag is what
decides workspace writability.

## Limits

- L1 SessionStart is still not enforcing. The container launch is the
  boundary, not a session gate.
- Only `api.anthropic.com:443` is allowed. Telemetry and other endpoints are
  denied, so a host that needs them fails closed.
- Auth is the owner's Claude config mounted read-only. No credential was
  copied or printed.
- **No Codex, Cursor, Gemini or VS Code extension is covered by this
  profile.** Their rows in the host status matrix are unchanged.
- No provider spend beyond the normal Claude subscription; no global install;
  no host configuration change.

## Verification

```bash
python scripts/ci/check-markdown-links.py docs/aegis-enforcement/L3-claude-container.md docs/aegis-enforcement/README.md
```

## Provenance

Drafted by DeepSeek (DeepSeek Harness) on 2026-11-22 from the L3 evidence
record captured the same day, including a later live workspace-write
verification. The values are transcribed from that record; no run was
repeated for this page.
