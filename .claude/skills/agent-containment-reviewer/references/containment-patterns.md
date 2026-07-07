# Agent Containment Patterns (ASI08 + ASI10)

Detail file for `agent-containment-reviewer`. Read on demand.

## 1. Failure-domain mapping

- Group agents by "fails together": shared queue, shared store, shared
  budget, shared model endpoint, common upstream agent.
- For each domain, name the boundary that stops propagation OUT of it — if
  none exists, the whole system is one domain (finding).
- Fan-out points multiply domains' exposure: one orchestrator feeding N
  workers puts N domains downstream of one output.

## 2. Propagation-path catalog (ASI08)

| Cascade type | Path | Primary controls |
| --- | --- | --- |
| Bad-output (hallucination) | Agent A emits plausible-wrong → B trusts it → acts | Validate BETWEEN agents (`structured-output-validator` + semantic checks); provenance on inter-agent data; bounded trust |
| Failure/latency | A stalls → B's retries pile → queues fill → fleet stalls | Timeouts, bounded retries + backoff, queue depth limits, backpressure, circuit breaker per edge |
| Flood | A loops/fans out → downstream and shared APIs saturate | Fan-out caps, per-agent rate limits, bulkheads on shared resources |
| Cost | Any of the above × tokens | `ai-cost-guardrail-designer` budgets/loop bounds wired per agent AND per pipeline |
| Contamination | Poisoned artifact persisted → consumed by later runs/agents | Checkpoint + purge/rollback (`memory-context-poisoning-reviewer` for memory stores) |

## 3. Breakers, bulkheads, backpressure

- **Circuit breaker per inter-agent edge:** open on error-rate/latency
  threshold; downstream gets a typed failure, not silence; half-open probes
  re-close it. Thresholds justified, alerts on state change
  (`observability-operator`).
- **Bulkheads:** per-agent quotas on shared resources (connections, queue
  slots, budget) so one agent cannot exhaust the pool.
- **Backpressure over buffering:** unbounded queues convert overload into
  delayed disasters; bound depth and shed/park work explicitly.
- **Bounded retries everywhere:** retries at agent, queue, and client
  layers multiply — budget them jointly, not per layer.

## 4. Checkpoint & rollback design

- Checkpoint = durable, resumable state at step boundaries: inputs, plan
  position, side effects SO FAR (enumerated), artifacts.
- Resume = re-validate the checkpoint (a contaminated checkpoint replays
  the contamination), then continue.
- Rollback = the enumerated side effects since the checkpoint get the
  `rollback-runbook-author` treatment: reversible ones reversed,
  irreversible ones surfaced to a human.
- Pipelines with mid-stream external side effects and no checkpoints are
  all-or-nothing bombs — finding.

## 5. Agent inventory schema (ASI10)

| Field | Why |
| --- | --- |
| `agent id / version` | What exactly is running (config/prompt hash if available) |
| `owner` | Named human accountable; orphaned = finding |
| `purpose / autonomy level` | What it should be doing; ceiling for drift comparison |
| `identity / credentials` | What a kill must sever (`agent-identity-privilege-reviewer` inventory) |
| `edges` | Topology membership (`inter-agent-comms-reviewer` map) |
| `kill path` | The tested procedure that stops THIS agent |
| `lifecycle state` | provisioning / active / suspended / decommissioned — zombies (decommissioned + live credentials) are findings |

Sweep for SHADOW agents: processes/credentials acting agent-like that are
in no registry — check identity provider logs, API consumers, queue
producers against the inventory.

## 6. Drift-baseline signals (ASI10)

Baseline the SHAPE of behavior per agent, then alert on deviation:

- Action rate and error profile (volume drift).
- Tool mix (an agent that never used `send_email` starting to — shape
  drift even at normal volume).
- Target scope (tenants/systems touched vs baseline — overlap with
  `agent-goal-hijack-defender` scope predicates; drift here without an
  attacker is ASI10, with one it's ASI01).
- Cost per task (`ai-cost-guardrail-designer` burn signals).
- Temporal pattern (activity at hours/rates unlike the baseline).

State detection latency per signal: baseline-to-alert time is the
containment gap being measured.

## 7. Authority-severing kill-switch rubric

A kill switch passes only if ALL hold:

1. **Severs authority:** credentials revoked/expired, tool access removed,
   broker/topology ACLs closed — not merely process termination.
2. **Handles the supervisor:** orchestrators/supervisors won't restart or
   re-credential the killed agent.
3. **Fences work in flight:** queued tasks drained or quarantined;
   downstream consumers notified with a typed signal.
4. **Scoped levels:** per-agent, per-pipeline, fleet-wide — each reachable
   independently; fleet kill doesn't lock out the humans operating it.
5. **Audited:** who killed what, when, why — feeds `agent-governance-audit`.
6. **Tested:** rehearsal cadence with a log; staleness triggers (topology
   or identity changes invalidate the last rehearsal) — same discipline as
   `rollback-runbook-author`.
7. **Reachable:** named humans, bounded time-to-execute, works when the
   agent platform itself is degraded.

Execution order during a real event belongs to `incident-response-runbook`;
this rubric is what that runbook invokes by reference.
