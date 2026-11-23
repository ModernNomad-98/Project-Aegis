# L3 containment: Codex CLI container profile

This page records container containment for the Codex CLI: **L3 (container
confinement) is recorded only when Codex is launched through the Aegis
container described here.** It is **not** the Aegis tool-policy gate. Every
other host status in the [host status matrix](README.md#host-status-matrix) is
unchanged.

## What L1, L2 and L3 mean here

- **L1, session gate:** the host refuses to start a session. Not achieved
  anywhere in this repository and not claimed for Codex.
- **L2, tool gate:** the [Aegis Guard CLI](../../tools/aegis_guard/cli.py)
  decides each tool call. It is not wired to Codex in this profile, so no L2
  claim is made.
- **L3, containment:** the host runs inside a container boundary it cannot
  escape by ignoring a policy decision: a read-only root, dropped
  capabilities, no privilege escalation, a non-root user and egress only
  through an allow-list proxy.

## Scope

**L3 applies only when Codex is started through this container.** Run natively
on Windows it is unqualified. A launch outside the container bypasses L3
entirely, and nothing here constrains that run.

**Containment is the only boundary.** Codex exposes no hook that this profile
wires to Aegis Guard, so the tool-policy denies for `.env`, secret paths and
specific tools are **not** enforced inside the workspace. **Secrets must be
excluded by the mount set:** a secret that is present in the mounted
workspace is readable by Codex and is not blocked by any Aegis policy.
Container confinement limits where damage can land; it does not classify what
Codex may read.

## Profile

| Item | Exact value |
| --- | --- |
| Host | Windows, **Docker Engine 29.9.2**, Linux containers |
| Codex image | `aegis-codex-l3:latest`, `codex-cli` 0.171.0 |
| Codex image digest | `sha256:5f6ab402d6219c233c58a37a7adfd8313749b118a647bdb3feb6a277bdb5162c` |
| Egress proxy image | `aegis-egress-proxy:2` |
| Egress proxy digest | `sha256:145c9cfefafbc33cd2222e948768fc8d3344291c869b6072fddc90dbe657e155` |
| Internal network | `aegis-int`, `internal=true` |
| Network attachment | the proxy container is dual-homed: default bridge network for upstream egress, `aegis-int` for its clients; the Claude and Codex containers attach only to `aegis-int` |
| Proxy allow-list | `CONNECT` to `api.anthropic.com`, `chatgpt.com`, `api.openai.com`, `auth.openai.com`, `cdn.openai.com` and `platform.openai.com` on 443; every other target gets `403` |
| Root filesystem | read-only |
| Capabilities | `--cap-drop ALL` |
| Privilege escalation | `no-new-privileges` |
| User | uid `1000`, non-root |
| `/tmp` and `/home/node/.codex` | `tmpfs`, writable and not persisted |
| Workspace | `/work`, mounted read-write |
| Codex config | `auth.json` and `config.toml` mounted read-only; no credential is copied into the image or printed |
| Egress | `HTTPS_PROXY` points at the proxy; `internal=true` means the network has no route out except through it |
| Inner Codex sandbox | `--sandbox danger-full-access`; bubblewrap fails with `bwrap: No permissions to create a new namespace` in this container, so the container is the boundary |

## Results

| Test | Observed result | What it shows |
| --- | --- | --- |
| Model `gpt-6-astra` through the proxy | Output OK, exit `0` | The allow-listed endpoint works through the proxy. |
| Shell write `/work/ok.txt` | Success, content OK | The read-write workspace accepts writes. |
| Shell write `/etc/codex-canary` | `OSError 30`, read-only file system | The read-only root refuses writes even with the inner sandbox disabled. |
| Direct egress from `aegis-int` | `Network is unreachable` | The internal network has no route out. |
| Proxy `CONNECT` to `github.com` (marketplace) | `403` | The proxy refuses non-allow-listed targets; the marketplace MCP endpoint was denied. |

## Limits

- **Native Codex CLI 0.149.1 remains unqualified.** No containment or hook
  evidence covers a native launch; running it inside this container profile is a
  candidate, not a run.
- `gpt-5.1-codex` is rejected by the account, and `gpt-6-astra` works only on
  `codex-cli` 0.171 and later. Earlier versions are unqualified for this
  profile.
- The Codex inner sandbox is unusable in this container because bubblewrap
  cannot create a namespace. `danger-full-access` is bounded only by the
  container, so it must never be used outside it.
- No L2 tool gate and no L1 session gate: neither is available for Codex here.
- No Cursor, Gemini, VS Code or native Windows coverage.
- No global install, host configuration change or credential copied by this
  profile.

## Verification

```bash
python scripts/ci/check-markdown-links.py docs/aegis-enforcement/L3-codex-container.md docs/aegis-enforcement/README.md
```

## Provenance

Drafted by DeepSeek (DeepSeek Harness) on 2026-11-22 from the L3 Codex
evidence record captured the same day. The values are transcribed from that
record; no run was repeated for this page.
