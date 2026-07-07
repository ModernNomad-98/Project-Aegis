---
name: agent-identity-privilege-reviewer
description: Review agent identities and privilege paths (OWASP Agentic ASI03) — verify every agent has a distinct least-privilege identity (no shared god service account), credentials are task- and time-scoped, delegation chains (user → agent → sub-agent → tool) attenuate authority and never amplify it, confused-deputy paths are closed (agent privilege exploited by a lower-privilege requester), and every action attributes to both the human principal and the acting agent. Complements secrets-identity-hardener (custody/rotation fixer); this reviews the identity ARCHITECTURE. Use when reviewing what identities agents run as, scoping agent credentials, designing delegation/on-behalf-of semantics, or hunting privilege escalation in multi-agent systems. Do NOT use for secret storage/rotation (secrets-identity-hardener), per-tool authority enforcement (agent-tool-safety-guard), standing agent-vs-human SDLC authority (agent-authorization-matrix), or end-user RBAC (authorization-matrix-designer).
---

# Agent Identity & Privilege Reviewer

## Purpose

Review the identity architecture of an agent system (ASI03): what identity
each agent runs as, what privileges that identity holds, and how authority
flows when work is delegated — user to agent, agent to sub-agent, agent to
tool. The output is findings ranked by escalation path: shared or over-broad
agent identities, long-lived standing credentials, delegation that amplifies
instead of attenuates, confused-deputy paths where a low-privilege requester
harvests an agent's higher privilege, and actions that cannot be attributed
to both the human principal and the acting agent. Credential custody and
rotation mechanics belong to `secrets-identity-hardener`; per-tool
enforcement belongs to `agent-tool-safety-guard` — this skill reviews the
identity model those enforce against.

## Use When

- Use when: reviewing what identities/credentials agents and sub-agents run
  as, or designing them for a new agent system.
- Use when: agents share a service account, hold admin/broad API keys, or
  keep standing credentials that outlive tasks.
- Use when: designing delegation or on-behalf-of semantics — how a user's
  authority is carried through agents to actions — or hunting
  privilege-escalation / confused-deputy paths in a multi-agent system.
- Use when: audit/attribution can't answer "which human and which agent did
  this?"
- Do NOT use when: the finding is how secrets are STORED, exposed, or
  rotated — `secrets-identity-hardener` (this skill decides what identities
  and scopes should exist; that one fixes custody).
- Do NOT use when: the question is whether a specific tool call runs with the
  calling user's authority (`agent-tool-safety-guard`), what a dev-agent may
  merge/deploy in the SDLC (`agent-authorization-matrix`), or end-user
  roles×permissions (`authorization-matrix-designer`).

## Inputs to Inspect

1. The agent inventory and what identity each runs as: per-agent identities,
   shared service accounts, or the platform's ambient credentials.
2. Credential material per agent: scopes, lifetime, issuance (static keys vs
   short-lived tokens), where they live (route custody findings to
   `secrets-identity-hardener`).
3. The delegation design: how a user's request becomes an agent's authority —
   on-behalf-of tokens, impersonation, session propagation — and what
   happens at each hop (agent → sub-agent → tool).
4. The permission each identity actually holds vs what its tasks need
   (IAM policies, API scopes, DB roles), including tenant reach.
5. Attribution: logs/audit records for agent actions — do they carry BOTH
   the human principal and the acting agent (`audit-log-architect` schema)?
6. Existing authority artifacts: `agent-authorization-matrix` (SDLC standing
   authority), `authorization-matrix-designer` output (end-user RBAC the
   delegation must respect).

## Workflow

1. **Inventory identities.** List every agent/sub-agent and the identity it
   executes under. Flag immediately: multiple agents on one identity, agents
   on a human's personal credentials, or ambient platform credentials. No
   identity information available → Stop Conditions.
2. **Map privilege vs need.** For each identity: what can it actually do
   (scopes, roles, tenant reach) vs what do its tasks require? Excess is a
   finding with an escalation path, not a style note.
3. **Trace delegation chains** using
   [references/agent-identity-patterns.md](references/agent-identity-patterns.md):
   for each chain (user → agent → sub-agent → tool), write who authorized
   the hop, what authority crosses it, and whether it attenuates. Authority
   must never grow along a chain; a sub-agent holding more than its parent
   is an amplification finding.
4. **Hunt confused-deputy paths.** Anywhere an agent performs privileged
   actions on requests from less-privileged sources (users, peer agents,
   queued jobs): can the requester steer the agent's privilege to targets
   they couldn't touch themselves? Cross-tenant variants first
   (`tenant-isolation-reviewer` composes).
5. **Check credential lifetime and binding.** Standing long-lived credentials
   on agents are findings when task-scoped short-lived issuance is feasible;
   tokens should bind to the task/principal context so a stolen credential
   doesn't outlive or outrange the task.
6. **Verify dual attribution.** Every side-effecting action must be
   attributable to the human principal AND the acting agent (and the chain
   between them). "The service account did it" is an attribution failure.
7. **Rank findings by escalation path.** Each finding: identity → excess or
   chain flaw → concrete abuse (what an attacker or manipulated agent
   reaches) → fix (split identities, narrow scopes, attenuate hop, add
   attribution). Custody fixes route to `secrets-identity-hardener`;
   per-tool enforcement to `agent-tool-safety-guard`.

## Output Format

```
AGENT IDENTITY & PRIVILEGE REVIEW — <system>
Identity inventory: <agent → identity → shared? → credential type/lifetime>
Privilege vs need: <identity → holds vs needs → excess>
Delegation chains: <user → agent → sub-agent → tool; authority at each hop; attenuates?>
Findings (severity-ranked):
  [SEV] <identity/chain> — Escalation path: <requester/attacker → abuse → reach>
    Fix: <split identity | narrow scope | short-lived issuance | attenuate hop | add attribution>
Confused-deputy paths: <requester → agent privilege → target they couldn't reach>
Attribution: <dual (principal + agent) attribution status per action class>
Handoffs: custody → secrets-identity-hardener | tool enforcement → agent-tool-safety-guard
Not reviewed: <areas + why>
```

## Validation Checklist

- [ ] Every agent/sub-agent's executing identity is inventoried; shared and
      ambient identities are flagged.
- [ ] Privilege vs need compared per identity; excess carries an escalation
      path, not just a "too broad" label.
- [ ] Every delegation chain is traced hop-by-hop and attenuates; no
      sub-agent or tool hop holds more authority than its delegator.
- [ ] Confused-deputy paths checked wherever privileged agents serve
      less-privileged requesters; cross-tenant variants first.
- [ ] Credential lifetime/binding reviewed; standing credentials justified
      or flagged with a short-lived alternative.
- [ ] Dual attribution (human principal + acting agent) verified for
      side-effecting actions.
- [ ] Custody/rotation findings routed to `secrets-identity-hardener`, not
      re-solved here.

## AI Security Rules

- Agent identities are scoped and least-privilege: one agent, one identity,
  the minimum scopes its tasks need, for the minimum time.
- Delegation attenuates: authority may narrow at each hop of
  user → agent → sub-agent → tool, never widen. Amplification is a finding
  by definition.
- No confused deputy: an agent must not let a requester achieve through the
  agent's privilege what the requester's own authority forbids.
- Every action is attributable to the human principal AND the acting agent;
  anonymous service-account attribution fails the review.

## Gotchas

- The shared "agents" service account is the default failure: convenient at
  setup, it makes every agent as powerful as the strongest one and turns any
  single compromise into fleet-wide privilege. Split it before scoping it.
- Delegation by prompt is not delegation: passing "acting for user X" as
  text grants nothing and attenuates nothing — authority must travel as
  verifiable context (token, signed claim), or the deputy is confused by
  design.
- Sub-agent spawning quietly amplifies: a child agent inheriting the
  parent's full credentials for a narrower task violates attenuation — mint
  narrower, shorter-lived credentials per spawn.
- Confused deputy hides behind helpfulness: "fetch this URL for me,"
  "summarize that tenant's doc" — the agent's privilege makes it a proxy for
  reaches the requester lacks. The check is the REQUESTER's authority, not
  the agent's.
- Machine identity sprawl: agents accumulate roles over time (each incident
  adds one); nobody subtracts. Review holds-vs-needs against current tasks,
  not historical ones.
- Attribution that stops at the agent ("agent-7 deleted it") is half an
  answer — without the principal and chain, incident response and
  `agent-governance-audit` dead-end.

## Stop Conditions

- No identity/credential information is available for the agent system —
  stop; this skill reviews concrete identity architecture, not intentions.
- A live over-privileged path with active abuse indicators is found
  (credential used from unexpected context, cross-tenant reach exercised) —
  route to `incident-response-runbook`; revocation is a human call executed
  via `secrets-identity-hardener`.
- Fixes require creating/splitting identities or changing IAM/scopes in a
  live system — propose the target model; applying it is a classified,
  approved step (`human-approval-boundary`).
- The question turns out to be end-user RBAC, SDLC merge/deploy authority,
  or per-tool argument enforcement — hand to the owning skill and stop.

## Supporting Files

- [references/agent-identity-patterns.md](references/agent-identity-patterns.md)
  — identity-per-agent patterns, short-lived task-scoped issuance, the
  delegation/attenuation trace method, the confused-deputy catalog, and the
  dual-attribution audit schema.
- `evals/evals.json` — trigger + behavior cases.
- `evals/trigger-evals.json` — discrimination within the agentic cluster and
  against `secrets-identity-hardener`, `agent-tool-safety-guard`,
  `agent-authorization-matrix`, and `authorization-matrix-designer`.
