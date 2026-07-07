# Agent Identity & Delegation Patterns (ASI03)

Detail file for `agent-identity-privilege-reviewer`. Read on demand.

## 1. Identity models, weakest to strongest

| Model | Description | Verdict |
| --- | --- | --- |
| Ambient platform credentials | Agents inherit whatever the host process/VM can do | Finding — no per-agent boundary at all |
| One shared service account | All agents authenticate as `agents-svc` | Finding — fleet-wide blast radius, no attribution |
| Identity per agent, static keys | Distinct identities, long-lived credentials | Baseline — scoping possible, theft durable |
| Identity per agent, short-lived tokens | Distinct identities, task-time issuance (OIDC/STS-style) | Good — theft expires with the task |
| Identity per agent + per-task on-behalf-of | Short-lived token binding agent identity AND principal context | Target — attenuation and dual attribution built in |

## 2. Short-lived, task-scoped issuance

- Mint at task start, scoped to the task's needs (resources, tenant, verbs),
  expiring at/near task end. A credential that outlives its task is standing
  privilege.
- Bind tokens to context: principal, tenant, task id. A stolen token that
  works from any context for any purpose is unbound.
- Sub-agent spawn = new issuance: narrower scope, shorter life, chain
  recorded. Never hand the parent's token down.
- Storage/rotation/exposure of whatever material exists →
  `secrets-identity-hardener`.

## 3. Delegation/attenuation trace method

For each chain, fill and verify hop-by-hop:

```
user (authority A0)
  → agent (holds A1; A1 ⊆ A0 for user-driven actions? authorized by whom?)
    → sub-agent (A2 ⊆ A1? minted fresh or inherited?)
      → tool (executes with A3 = calling user's authority per agent-tool-safety-guard)
```

- Any hop where Aₙ₊₁ ⊄ Aₙ is an amplification finding.
- Agent authority beyond the user's (maintenance/system tasks) must trace to
  its own named principal (an operator/owner), not float free.
- "Delegation" that exists only in prompt text is unverifiable → treat the
  hop as broken; require token/claim-carried context.

## 4. Confused-deputy catalog

| Pattern | Example | Check |
| --- | --- | --- |
| Fetch/read proxy | "Summarize <other tenant's doc>" — agent's read scope crosses tenants | Requester's authority checked at the resource, not the agent's |
| Write proxy | Low-privilege user asks agent to modify config only admins may touch | Action authorized against requester, agent identity irrelevant |
| Peer-agent laundering | Agent B (privileged) executes requests from agent A (unprivileged) | Carry originating principal through A2A hops (`inter-agent-comms-reviewer` secures the transport; the CLAIM must still be verified) |
| Queue laundering | Privileged worker consumes attacker-writable queue | Queue writers are part of the chain; verify producer authority |
| Tool-description bait | Tool described so the model routes privileged actions through it | Compose `agent-tool-safety-guard` tool-surface review |

## 5. Dual-attribution audit schema

Every side-effecting agent action logs (compose `audit-log-architect`):

| Field | Why |
| --- | --- |
| `principal` | The human (or named system owner) whose authority the action used |
| `agent` | The acting agent identity (and version/config hash if available) |
| `chain` | Delegation path (agent → sub-agent ids) for multi-hop runs |
| `task/run id` | Correlates to the goal record (`agent-goal-hijack-defender`) and run telemetry |
| `authority basis` | Token/claim id or approval reference (`human-approval-boundary`) |

Failure smells: logs naming only the service account; sub-agent actions
recorded under the parent; approvals recorded without the acting agent.

## 6. Escalation-path severity rubric

High severity requires a concrete path: requester/attacker → flaw (shared
identity, amplifying hop, deputy pattern, unbound standing credential) →
reach they should not have (cross-tenant read/write, admin action, external
send). "Scope is broad" with no path is hygiene, ranked below any finding
with a path. Cross-tenant paths outrank same-tenant; write outranks read.
