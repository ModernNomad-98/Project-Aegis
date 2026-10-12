# P0-B FAST SAVE directive — on-main record (owner directive 2026-10-11)

This page transcribes the owner's P0 directive of **2026-10-11** for the **P0-B FAST SAVE** workstream onto
`main`: the operational definition of the FAST SAVE command ("Save progress and pause"), its prohibited
actions, its acceptance tests, its checkpoint contents, its durability rules, its two-status contract and its
idle target. It is a decision/status record in the pattern of the
[setup routing plan status section](aegis-setup-routing-plan.md#status--reconciled-2026-10-11-issue-101-d97):
it records what the owner directed, and **it closes nothing and grants nothing**.

- **Item:** P0-B B1 — FAST SAVE directive record (documentation only).
- **Command:** FAST SAVE, invoked as *save progress and pause* or *fast save*.
- **Companion protocol draft:** [fast-save-handoff-protocol-v1](../design/fast-save-handoff-protocol-v1.md) —
  the operator-facing handoff protocol derived from this directive.
- **Class:** DOCUMENTED POLICY. **No mechanical enforcement exists or is claimed here**; enforcement is future
  host router work and is owner-decision gated.

## S1. Source and authority

- **Source.** The owner's 2026-10-11 live-chat P0 directive, relayed verbatim to the agent that transcribed
  this page. Per the [approval register preamble](../approvals/APPROVAL_REGISTER.md) (L12-13), **"Current direct
  user instructions are valid source evidence before transcription and do not need repeated consent."** The
  transcription therefore rests on the current owner instruction itself, not on a pre-existing grant.
- **What this page is not.** This page is a record, not an authorization. **It grants nothing by itself.** The
  [approval register](../approvals/APPROVAL_REGISTER.md) remains the sole documentary grant register for this
  repository: an action is covered only by an effectively ACTIVE human grant whose scope includes it.
- **Invocation is not authorization.** Saying "fast save" is a trigger for the procedure below, never an
  approval, a scope change, or a permission to touch anything the FAST SAVE procedure does not name.
- **Provenance of the relayed wording.** Every quoted clause on this page is carried **verbatim** from the
  directive relay; nothing is paraphrased, merged, softened or invented. Where the relay is incomplete, the
  gap is carried openly as **G1/G2/G3** in [S11](#s11-status--transcribed-2026-10-11-p0-directive-2026-10-11)
  with an owner question — never silently filled.

## S2. Priority text

The directive's priority wording, verbatim:

> P0-B FAST SAVE workstream — FIRST eligible increment B1: transcribe the P0 directive onto main as a docs
> record + a FAST SAVE handoff protocol draft, per the owner's 2026-10-11 P0 directive.

P0-B FAST SAVE is therefore the workstream's priority; **B1** (this record plus the companion protocol draft)
is its first eligible increment. Later increments — any FAST SAVE mechanics — are separate and are not
authorized by this page.

## S3. Operational definition — the nine required behaviors

The directive defines FAST SAVE as a **lightweight operational command**: *"Save progress and pause"*. On a
FAST SAVE command, the agent performing it must do exactly these nine things, in this order:

1. **Stop dispatching work** — dispatch no new work items, and start no new step of the current item.
2. **Capture progress** — record where the work actually stands, from the artifacts, not from memory.
3. **Preserve unfinished files** — leave unfinished work in place and intact; nothing is discarded.
4. **Write a small versioned checkpoint to an approved durable location** — see
   [S7](#s7-checkpoint-contents) for contents and [G3](#s11-status--transcribed-2026-10-11-p0-directive-2026-10-11)
   for the location, which the relay does not name.
5. **Bounded readback** — read the checkpoint back, bounded in scope, to show it is consumable.
6. **Safe-stop known operations where authorized** — stop only operations the agent is already authorized to
   stop; authorization is a precondition, not an assumption.
7. **Report work stopped / active / uncertain** — report the true state of every tracked operation, using the
   vocabulary of [S8](#s8-two-status-contract); uncertainty is reported as uncertainty.
8. **Return checkpoint location + one-line resume** — give the checkpoint's location and a single line that
   resumes the work.
9. **Stop** — then stop. FAST SAVE ends the turn's work; it is not a transition into further work.

**"Fast save is not QA."** — see [S10](#s10-fast-save-is-not-qa).

## S4. Prohibited actions

On a FAST SAVE command, the following clause applies **verbatim**:

> PROHIBITED: CI/tests/lint/build/security reviews/audits/filesystem inventories/context-map regen/GitHub
> ops/new agents/dependency installs/code correction/commits/staging/reset/cleanup/revalidation of recorded
> work.

The clause is a slash-separated list. Enumerated item by item, **without dropping or merging any term**, it
reads:

1. CI
2. tests
3. lint
4. build
5. security reviews
6. audits
7. filesystem inventories
8. context-map regen
9. GitHub ops
10. new agents
11. dependency installs
12. code correction
13. commits
14. staging
15. reset
16. cleanup
17. revalidation of recorded work

**Flagged gap G2 — count.** The workstream brief says *"the 16 prohibited actions"*, while the relayed clause
contains **17** slash-separated terms as enumerated above. Both figures are recorded as received; **no silent
resolution is made** and no term is dropped, merged or renamed to force the count to 16. **Owner question
(G2):** confirm the authoritative count and grouping — in particular whether *"new agents/dependency
installs"* is one grouped term and which term the brief's count excludes.

The enumeration above is a faithful expansion of the clause; it is **not** a widening of it. A term that is not
in the verbatim clause is not prohibited by this record, and a term that is in the clause is not exempted by
anything on this page.

## S5. Acceptance tests — the fifteen scenarios

The directive's acceptance-test table, verbatim and in the directive's order:

| # | Scenario |
| --- | --- |
| 1 | clean idle |
| 2 | dirty worktree |
| 3 | untracked files |
| 4 | previously failed validation |
| 5 | existing large worktree population |
| 6 | missing network access |
| 7 | expired grant |
| 8 | active operation |
| 9 | uncertain operation |
| 10 | interrupted checkpoint write |
| 11 | failed persistence |
| 12 | successful readback |
| 13 | fresh-session reopening |
| 14 | missing source bytes after transfer |
| 15 | agent attempting to launch CI during a pause |

The directive relays the same fifteen scenarios in a second, shorter form, and the two forms are one-to-one in
this order: *clean idle; dirty worktree; untracked files; previously failed validation; large worktree;
missing network; expired grant; active operation; uncertain operation; interrupted write; failed persistence;
successful readback; fresh-session reopening; missing source bytes; agent launching CI during pause.*

Two rules bind the acceptance mechanism, and they are part of the directive, not commentary on it:

1. **Every acceptance test must be evidenced by a REAL tool-call trace** — every AT must be evidenced by a
   REAL tool-call trace — proven-invocation pattern — the actual invocation and its observed tell-tale output;
   **prose assertions do not count** as acceptance evidence. A written claim that a scenario passed is not a pass.
2. **Scenario 15 — scenario 15 + any unsolicited test/CI/audit/new task during a FAST SAVE command is an
   acceptance FAILURE.** The prohibition in [S4](#s4-prohibited-actions) is not advisory during a FAST SAVE: an
   agent that launches CI while a pause is in effect has failed the scenario, and the failure is recorded as
   a failure.

The companion protocol maps these fifteen scenarios to **AT-01…AT-15** with observable pass/fail statements
and the same evidence standard:
[fast-save-handoff-protocol-v1, P9](../design/fast-save-handoff-protocol-v1.md#p9-acceptance-tests-at-01at-15).

## S6. Durability rules

The directive's five durability rules — declared in the same single clause as the required behaviors
(*"Durability: no partial writes mistaken for saved; preserve previous valid checkpoint on failure; no
overwriting unrelated user work; machine-readable + human-readable; no provider call to save known state."*):

1. **No partial writes mistaken for saved** — a checkpoint is either complete and readable, or it is not a
   checkpoint.
2. **Preserve the previous valid checkpoint on failure** — a failed save must not destroy the last good state.
3. **No overwriting unrelated user work** — the checkpoint touches only its own location.
4. **Machine-readable and human-readable** — the checkpoint supports both a fresh session and a human reader.
5. **No provider call to save known state** — saving known state never spends a provider call.

## S7. Checkpoint contents

The directive says *"Checkpoint contents list per the directive"*; **the list itself was not included in the
relay received by the transcribing agent.** This is flagged as **G1** and is not resolved silently.

**Provisional scaffold — NOT authority.** The following field list is a *provisional* scaffold derived from the
nine behaviors, the five durability rules and the two-status contract. It is labeled provisional, is subject
to the G1 owner question, and must not be read as the directive's own list:

- checkpoint version / sequence
- created timestamp
- invocation phrase
- workstream / item id
- dispatch state (reported: stopped / not stopped / unknown)
- progress captured
- unfinished-files list (preserved)
- execution status
- checkpoint status
- durable location
- bounded readback result
- one-line resume
- previous-valid-checkpoint reference
- no-provider-call attestation
- safe-stopped operations (where authorized; list or none)
- checkpoint carries no credentials/tokens/secrets
- idle measurement (only if measured)

**Owner question (G1):** provide the directive's verbatim checkpoint-contents list, or confirm that the
labeled provisional scaffold above may stand in its place.

## S8. Two-status contract

The directive declares the contract in one clause: *"Two statuses: Checkpoint SAVED/FAILED and Execution
STOPPED/ACTIVE/UNKNOWN/PAUSE INCOMPLETE."*

FAST SAVE reports **two independent statuses**. They are separate on purpose: the checkpoint's fate and the
work's execution state are different facts, and neither may be inferred from the other.

| Status | Vocabulary |
| --- | --- |
| **Checkpoint** | SAVED / FAILED |
| **Execution** | STOPPED / ACTIVE / UNKNOWN / PAUSE INCOMPLETE |

**UNKNOWN is a first-class reported state.** An agent that cannot establish whether an operation stopped
reports UNKNOWN; it does not report STOPPED, and it does not omit the field. **A checkpoint must report the
prior dispatch state, not assert it** — hence the reported form *stopped / not stopped / unknown* in
[S7](#s7-checkpoint-contents).

## S9. Idle target

The directive declares the target in one clause: *"Idle target <60s measured, never guaranteed without
evidence."* Read out — **under 60 seconds** (`<60s`) from command to a completed pause — it is a
**measurement target, never a guarantee**: the figure may be quoted as an expectation and may not be quoted as
a promise, a service level, or a demonstrated result **without evidence**. An idle time is reported only when it was
actually measured. This record invents no latency figure and makes no claim about a measured idle time.

## S10. Fast save is not QA

> **"Fast save is not QA."**

FAST SAVE preserves state and stops cleanly. It validates nothing: it is not a test run, not a review, not an
audit, and not an acceptance gate. **A successful FAST SAVE says the work was saved — nothing about whether
the work is correct.**

## S11. Status — transcribed 2026-10-11 (P0 directive 2026-10-11)

**Shipped.** This page records the owner's 2026-10-11 P0 directive for the P0-B FAST SAVE workstream: the
priority text ([S2](#s2-priority-text)), the nine required behaviors
([S3](#s3-operational-definition--the-nine-required-behaviors)), the verbatim PROHIBITED clause with its
item-by-item enumeration ([S4](#s4-prohibited-actions)), the fifteen acceptance scenarios with their two
binding evidence rules ([S5](#s5-acceptance-tests--the-fifteen-scenarios)), the five durability rules
([S6](#s6-durability-rules)), the checkpoint-contents question ([S7](#s7-checkpoint-contents)), the
two-status contract ([S8](#s8-two-status-contract)), the idle target
([S9](#s9-idle-target)) and the standing reminder ([S10](#s10-fast-save-is-not-qa)).
The operator-facing companion is
[fast-save-handoff-protocol-v1](../design/fast-save-handoff-protocol-v1.md).

**Grants nothing; closes nothing.** This record creates no grant, consumes none, mints no decision (D) entry,
and edits no register, backlog, index or instruction file. **No D-entry was minted here.** The
[approval register](../approvals/APPROVAL_REGISTER.md) remains the sole documentary grant register.

**Flagged gaps and owner questions** (one question each; nothing silently resolved):

| Gap | What is missing | Owner question |
| --- | --- | --- |
| **G1** | The directive's checkpoint-contents list was not in the relay; a labeled provisional scaffold stands in ([S7](#s7-checkpoint-contents)). | Provide the verbatim list, or confirm the provisional scaffold may ship. |
| **G2** | The brief says 16 prohibited actions; the relayed clause has 17 slash-separated terms ([S4](#s4-prohibited-actions)). | Confirm the authoritative count and grouping. |
| **G3** | *"an approved durable location"* is transcribed as a rule but the concrete location is not in the relay. | Name the approved durable location, or confirm it stays directive/owner-named at runtime. |

**Next-step pointers (stated, never started).**

1. **Enforcement is future host router work and is owner-decision gated (G4).** Nothing on this page is
   mechanically enforced today and no host router implementing it exists.
2. **Later P0-B increments (B2/B3) remain separate increments.** They are not scoped, planned or authorized
   by this record.
3. **The five behaviors that need runtime mechanics — durable write, bounded readback, safe-stop, the status
   report, and the one-line resume — are documentation here, not implementation.**
4. **Stage C/D re-verify each citation at its cited line.** Every repository citation on this page and in the
   companion protocol is re-grepped — re-verified by grepping the claimed text at the cited line — before it is relied on
   (re-audit advisory ADV-2). For the two carried range cites this Stage C implementation widened both to
   **docs/delivery-workflow.md L126-131** (ADV-1): the SD-A change-classification duty is in the SD-A row at
   L128 and the SD-C immutable-head rule is in the SD-C row at L130.

**This record closes nothing and grants nothing** (2026-10-11).
