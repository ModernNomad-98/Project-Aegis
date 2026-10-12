# FAST SAVE handoff protocol v1 (draft)

The FAST SAVE handoff protocol: the operator-facing procedure an agent follows when the owner says
**"save progress and pause"** or **"fast save"**. It is the **HAND OFF pillar's operational protocol** — the
policy an agent applies — and **not** the control plane.

- **Companion directive record:**
  [p0b-fast-save-directive-2026-10-11](../roadmaps/p0b-fast-save-directive-2026-10-11.md) — the on-main
  transcription of the owner's 2026-10-11 P0 directive this protocol implements.
- **Relationship to the control plane.** This protocol is separate from
  [resumable-control-plane-v1](resumable-control-plane-v1.md). It grants no delivery action, introduces no
  kernel, and does not unblock or depend on the control plane's blocked work packages: **CP-WP-003 and
  CP-WP-004 remain BLOCKED** ([resumable control plane backlog](../roadmaps/resumable-control-plane-backlog.md)
  L266-271).
- **Class:** DOCUMENTED POLICY. **No mechanical enforcement exists, and none is claimed.** Enforcement is
  future host router work and is **owner-decision gated** (G4).
- **Standing reminder:** **"Fast save is not QA."**

## P1. Invocation

The owner invokes FAST SAVE with either phrase:

- **"save progress and pause"** — the directive's own phrasing; or
- **"fast save"** — the shorthand.

An invocation is a **trigger for this procedure, not an authorization**: it grants nothing, widens no scope,
and does not lift any prohibition in [P3](#p3-prohibited-actions). If an agent cannot complete the
procedure, it reports the checkpoint **FAILED** and the execution state honestly
([P5](#p5-two-status-contract)) rather than continuing to work.

## P2. Required behaviors — FS-B1…FS-B9

| ID | Behavior | What it requires |
| --- | --- | --- |
| **FS-B1** | Stop dispatching work | Dispatch no new work item and start no new step of the current one. Dispatch stops at the command, not at the next convenient point. |
| **FS-B2** | Capture progress | Record where the work actually stands, read from the artifacts — not from memory or expectation. |
| **FS-B3** | Preserve unfinished files | Leave unfinished work in place and intact. Nothing is deleted, reverted, stashed, cleaned or "tidied". |
| **FS-B4** | Write a small versioned checkpoint to an approved durable location | Write one small checkpoint, versioned, to the approved durable location (G3). Durability rules: [P7](#p7-durability-rules). |
| **FS-B5** | Bounded readback | Read the checkpoint back, bounded in scope, to show it is complete and consumable. |
| **FS-B6** | Safe-stop known operations, where authorized | Stop only operations the agent is already authorized to stop. Authorization is a precondition, never an assumption; where it is absent, the operation is reported, not stopped. |
| **FS-B7** | Report work stopped / active / uncertain | Report the true state of every tracked operation in the vocabulary of [P5](#p5-two-status-contract). Uncertainty is reported as **UNKNOWN**; it is never upgraded to STOPPED for tidiness. |
| **FS-B8** | Return checkpoint location + one-line resume | Return the checkpoint's location and one line that resumes the work from a cold start. |
| **FS-B9** | Stop | Then stop. FAST SAVE ends the work; it is not a transition into further work. |

## P3. Prohibited actions

On a FAST SAVE command the directive's clause applies **verbatim**:

> PROHIBITED: CI/tests/lint/build/security reviews/audits/filesystem inventories/context-map regen/GitHub
> ops/new agents/dependency installs/code correction/commits/staging/reset/cleanup/revalidation of recorded
> work.

Enumerated item by item, **without dropping or merging any term**:

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

**Flagged gap G2 — count.** The workstream brief says *"the 16 prohibited actions"*; the relayed clause
contains **17** slash-separated terms as enumerated above. The clause ships verbatim with the count flagged
and **no silent resolution**; **owner question:** confirm the authoritative count and grouping. The
enumeration is an expansion of the clause, never a widening of it: a term absent from the clause is not
prohibited by this protocol, and a term present in it is not exempted.

**A prohibited action performed during a FAST SAVE command is an acceptance failure**, not a minor
deviation — see [P9](#p9-acceptance-tests-at-01at-15).

## P4. Checkpoint contents

The directive says *"Checkpoint contents list per the directive"*; **the list itself was not in the relay
received by the drafting agent** (flagged as **G1**). The directive record carries the same gap
([directive record, S7](../roadmaps/p0b-fast-save-directive-2026-10-11.md#s7-checkpoint-contents)).

**Provisional scaffold — NOT authority.** This field list is a *provisional* scaffold derived from the nine
behaviors, the five durability rules and the two-status contract. It is labeled provisional, is subject to
the G1 owner question, and must not be read as the directive's own list:

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

Three of these fields carry rules that are worth stating on their own:

- **"safe-stopped operations (where authorized; list or none)"** records what FS-B6 actually stopped. When
  nothing was stopped, the field says so — it is never left blank, because a blank field cannot be
  distinguished from an omitted one.
- **"checkpoint carries no credentials/tokens/secrets"** is an exclusion, not a reminder: a checkpoint is not
  a place to preserve secrets, and no field above may carry one.
- **"dispatch state (reported: stopped / not stopped / unknown)"** reports the prior dispatch state; it does
  **not** assert that the previous agent stopped. The separate *execution status* field carries the
  two-status contract.

**Owner question (G1):** provide the directive's verbatim checkpoint-contents list, or confirm that the
labeled provisional scaffold may stand in its place.

## P5. Two-status contract

FAST SAVE reports **two independent statuses**:

| Status | Vocabulary |
| --- | --- |
| **Checkpoint** | SAVED / FAILED |
| **Execution** | STOPPED / ACTIVE / UNKNOWN / PAUSE INCOMPLETE |

They are separate facts and neither may be inferred from the other: a **SAVED** checkpoint does not imply
execution **STOPPED**, and execution **STOPPED** does not imply a **SAVED** checkpoint. **UNKNOWN is a
first-class reported state** — the honest report when the state cannot be established — and **PAUSE
INCOMPLETE** is the honest report when the pause did not complete.

## P6. Idle target

The directive's target is **under 60 seconds** from command to a completed pause. It is a **MEASUREMENT
TARGET, not a guarantee**: **measured, never guaranteed without evidence.** An idle time is reported only
when it was measured, and the measurement discipline is the name-and-time rule — state what was measured and
when it was measured ([execution metrics](../roadmaps/aegis-execution-metrics.md)). This protocol makes no
latency promise and quotes no measured figure of its own.

## P7. Durability rules

The five durability rules the checkpoint must satisfy:

1. **No partial writes mistaken for saved** — a checkpoint is complete and readable, or it is not a
   checkpoint.
2. **Preserve the previous valid checkpoint on failure** — a failed save must not destroy the last good
   state; the previous-valid-checkpoint reference in [P4](#p4-checkpoint-contents) is the anchor.
3. **No overwriting unrelated user work.**
4. **Machine-readable and human-readable** — a fresh session and a human reader can both consume it.
5. **No provider call to save known state** — saving known state never spends a provider call.

## P8. Handoff protocol structure

The handoff this protocol produces follows the shipped
[phased-work-handoff-designer](../../.claude/skills/phased-work-handoff-designer/SKILL.md) format
(Output Format, SKILL.md L96-111; template, references/handoff-sheet.md L11-79):

The **FS-…** IDs below are this effort's own decision identifiers and govern nothing outside the FAST SAVE
protocol; they are unrelated to the repository's approval-register grants and to decision (D) entries, and
minting one here creates no governance record.

**Decision-ID register (carried across stages).** Every binding decision gets a stable **FS-…** ID with a
one-line statement and a **still-binding** column, so a later stage marks prior decisions binding or
supersedes them explicitly — never by silent edit.

| FS-id | Decision | Still binding? | Superseded-by |
| --- | --- | --- | --- |
| FS-B1…FS-B9 | The nine required behaviors ([P2](#p2-required-behaviors--fs-b1fs-b9)). | yes | — |
| FS-D1 | The five durability rules ([P7](#p7-durability-rules)). | yes | — |
| FS-S1 | The two-status contract, with UNKNOWN first-class ([P5](#p5-two-status-contract)). | yes | — |
| FS-P1 | The prohibited-actions clause, carried verbatim with the G2 count flagged ([P3](#p3-prohibited-actions)). | yes | — |
| FS-A1 | Acceptance evidence must be a real tool-call trace ([P9](#p9-acceptance-tests-at-01at-15)). | yes | — |
| FS-C1 | Checkpoint contents: provisional scaffold until G1 is answered ([P4](#p4-checkpoint-contents)). | yes, provisional | — |

**Per stage:**

- **Changed files:** the files this stage changed, each with what and why.
- **NOT touched (intentional):** what the stage deliberately left alone, with the reason — silence reads as
  "forgotten" and invites the cleanup that undoes restraint.
- **Proven invocation:** the command **and its tell-tale output** (counts, IDs, the distinctive line). A bare
  assertion is not evidence.
- **Deviations:** any departure from the plan or a prior decision, with its rationale, flagged in-flight.
- **Open items → next stage:** what the next stage must pick up, with entry criteria.

**Continuation contract.** A fresh stage or agent picks up **cold** from the register, the changed /
not-touched state, the proven-invocation evidence so far, and the open items — and **the one-line resume is
that continuation entry line**.

**Code block — the format, with sample values (illustrative only; not evidence of any real stage):**

```text
FAST SAVE HANDOFF — <workstream/item>

Decision register (carried across stages)
| FS-id | Decision | Still binding? | Superseded-by |
| --- | --- | --- | --- |
| FS-B1…FS-B9 | nine required behaviors | yes | — |

Changed files
- <path> — <what/why>

NOT touched (intentional)
- <path> — left alone because <reason>

Proven invocation
$ <command>
<tell-tale output: counts / ids / output line>

Deviations
- Departed from <decision> because <rationale> — flagged.

Open items -> next stage
- <item>; entry criteria for the next stage

Continuation contract
- Register + changed/NOT-touched state + proven invocations + open items.
- One-line resume: <the single line that resumes the work cold>
```

## P9. Acceptance tests AT-01…AT-15

The directive's fifteen scenarios, mapped to observable pass/fail statements. The scenario names are the
directive's, in the directive's order. The directive also relays the same fifteen in a shorter form, and the
two forms are one-to-one in this order — including `AT-10`, *interrupted write* = *interrupted checkpoint
write*, and `AT-15`, *agent launching CI during pause* = *agent attempting to launch CI during a pause*.

| AT | Scenario | Expected behavior | Pass condition |
| --- | --- | --- | --- |
| AT-01 | clean idle | Nothing is in flight; checkpoint records an idle workstream. | A SAVED checkpoint exists and the execution status reports no active work. |
| AT-02 | dirty worktree | Uncommitted changes exist and are **preserved**, not reset or stashed. | Checkpoint SAVED; the dirty paths are still present and unmodified after the pause. |
| AT-03 | untracked files | Untracked files are **preserved**, not cleaned up. | Checkpoint SAVED; every untracked path still exists after the pause. |
| AT-04 | previously failed validation | The earlier failure is **reported as history**, not re-run and not revalidated. | Checkpoint SAVED; the prior failure is recorded; no validation command was invoked. |
| AT-05 | existing large worktree population | The pause completes within the idle target without inventorying the tree. | Checkpoint SAVED; no filesystem inventory was run; if idle time was measured it was under 60s (never inferred, never assumed). |
| AT-06 | missing network access | The pause completes **offline**; no GitHub op, fetch or provider call is attempted. | Checkpoint SAVED; the failure of any network operation is reported, and no network attempt was made. |
| AT-07 | expired grant | The expired grant is reported; no action is taken under it and none is silently renewed. | Checkpoint SAVED; the grant's state is recorded as expired; no action rests on it. |
| AT-08 | active operation | The active operation is safely stopped **where authorized**, or reported where it is not. | Checkpoint SAVED; the operation's state is reported; any stop was authorized and is listed in safe-stopped operations. |
| AT-09 | uncertain operation | Uncertainty is reported as **UNKNOWN**; it is not upgraded to STOPPED. | Checkpoint SAVED; the execution status for that operation reads UNKNOWN. |
| AT-10 | interrupted checkpoint write | The interruption is visible; a partial write is **not** mistaken for saved. | Checkpoint reports FAILED (or the partial write is shown to be incomplete); any previous valid checkpoint is intact. |
| AT-11 | failed persistence | The failure is reported, and the **previous valid checkpoint survives** untouched. | Checkpoint FAILED; the previous-valid-checkpoint reference resolves to an intact checkpoint. |
| AT-12 | successful readback | The bounded readback confirms the checkpoint is complete and consumable. | Readback output is shown; checkpoint SAVED; the readback stayed bounded. |
| AT-13 | fresh-session reopening | A fresh session can resume from the checkpoint alone, via the one-line resume. | The one-line resume plus the checkpoint is sufficient to continue without re-deriving. |
| AT-14 | missing source bytes after transfer | Missing bytes are reported as a gap; nothing is fabricated to fill them. | Checkpoint SAVED; the missing bytes are named as missing; no invented content appears. |
| AT-15 | agent attempting to launch CI during a pause | The attempt **must not happen**; if it does, it is a failure. | **Acceptance FAILURE** — see the verdict rule below. |

**Binding evidence standard.** Every AT's pass evidence **MUST be a REAL tool-call trace** — the actual
invocation and its observed tell-tale output (the proven-invocation pattern). **Prose assertions are not
acceptance evidence.** "AT-12 passed" is not evidence; the readback command and its output are. A test whose
only support is a written claim is **UNRUN**, not passed.

**Verdict rule — scenario 15.** **AT-15 has expected verdict acceptance FAILURE.** The scenario is a
negative control: an agent attempting to launch CI during a pause has already failed it. The same verdict
extends to **any unsolicited test/CI/audit/new task during a FAST SAVE command**, and — more generally — to
**any prohibited action performed during a FAST SAVE command**: it is an acceptance FAILURE, recorded as a
failure, never as a minor deviation and never waived.

## P10. Flagged gaps, owner questions and residual limits

- **G1 — checkpoint contents list.** Relayed as *"per the directive"*; the list itself was not in the relay.
  **Owner question:** provide the verbatim list, or confirm the labeled provisional scaffold
  ([P4](#p4-checkpoint-contents)) may ship.
- **G2 — prohibited-actions count.** The brief says 16; the relayed clause has 17 slash-separated terms.
  **Owner question:** confirm the authoritative count and grouping.
- **G3 — approved durable location.** The rule is transcribed; the concrete location is not in the relay.
  **Owner question:** name the approved durable location, or confirm it stays directive/owner-named at
  runtime.
- **G4 — enforcement (residual limit, stated plainly).** **This protocol has no mechanical enforcement.** No
  host router implements it today; nothing here blocks, intercepts, or interrupts a prohibited action.
  Enforcement is future host router work and is **owner-decision gated**, and it is **not** part of this
  increment. Until then the protocol is **documented policy**, honored by the agent applying it and verified
  by evidence after the fact.

## P11. Citation re-verification (Stage C/D constraint)

Every repository citation in this protocol and in the companion directive record is **re-verified by grepping
the claimed text at the cited line before it is relied on**. Two carried range citations were widened to
**docs/delivery-workflow.md L126-131** at Stage C (re-audit advisory ADV-1): the SD-A change-classification
duty is in the SD-A row at L128, and the SD-C immutable-head rule (commit SHA, `git rev-parse <head>^{tree}`,
and the base commit) is in the SD-C row at L130. Citations that cannot be confirmed at their cited line are
corrected or removed, never carried.

## P12. Status

**Draft v1 — DOCUMENTED POLICY, unenforced.** This protocol records the FAST SAVE procedure derived from the
owner's 2026-10-11 P0 directive. It **grants nothing and closes nothing**: no grant is created or consumed,
no decision (D) entry is minted, no register, backlog, index or instruction file is edited, and no
implementation exists behind it. Nothing here is mechanically enforced (G4). Later increments (B2/B3) remain
separate and are not scoped or authorized by this page.

**Forward pointer — 2026-10-12: an offline synthetic demonstration of the checkpoint capture
exists.** PR #741 (merge `6c83b723`, on `main` at `7fbc2335`) landed the P0-B **B2** increment:
an offline synthetic FAST SAVE checkpoint capture in `tools/aegis_delivery_control`
(`fast_save.py`; see the [delivery control plane
README](../../tools/aegis_delivery_control/README.md)). It is the nearest artifact to this
protocol's checkpoint rules and the first executable demonstration of the capture. **It does
not enforce this protocol and does not change P12:** enforcement remains future host router
work and is **owner-decision gated** (G4), and no runtime behavior, host router or delivery
action exists behind this page. B3 remains unscoped and unauthorized.
