# Recording & authority discipline

The detail behind the orchestrator's **Capability 4** (propose → approve →
append/refresh) and its human gate. The orchestrator stays thin and CITES this;
the schema and section mutability live in
[project-state-template.md](project-state-template.md). Four controls: risk-tiered
recording, authority-grant separation, idempotent-and-exact recording, and the
mutable-projection refresh.

## 1. Risk-tiered recording (do not ceremony every answer)

A file-operation ceremony after every ordinary product answer is
approval theater. Tier the recording by risk.

**Low-risk, reversible product-definition decisions** — status ownership, a
link's display fields, a link's lifetime, whether notifications exist, ordinary
terminology and workflow choices:

1. ask ONE question that turn;
2. acknowledge the answer;
3. add it to a **visible pending-decision batch** (conversation-only — not
   binding, not recorded);
4. continue discovery or spec clarification;
5. at a logical checkpoint, show EVERY exact proposed entry in the batch;
6. request ONE explicit approval to append the complete, bounded batch;
7. append the approved batch atomically where practical;
8. confirm every appended entry (§3).

The pending batch is shown completely before approval and disappears after it is
recorded or explicitly rejected.

**Never batched — each takes its own explicit approval:** implementation
authority; scope expansion or removal after approval; security or privacy risk
acceptance; consequential architecture; data migration; deletion; any
irreversible action; package installation; network execution; a version-control
commit or push; deployment; a financial commitment; a delivery promise; a
production change. Bundling any of these into a low-risk batch is the AR-A-004
failure.

### The recording forms

Capability 4's preview → approve → append is instantiated as exactly ONE of three
declared forms. MOST turns record nothing and use the none-this-turn form; every
high-risk / authority-changing / irreversible action uses the single-entry form;
only the low-risk decisions of §1 may use the batch form. The mandatory Output
Format always names which form is in effect, so a normal turn is never forced to
invent a log entry or open an approval ceremony for a decision not yet reached.

**NONE THIS TURN form** (the default — a turn that performs NO recording
operation: a pure skill invocation, an owner classification decision, a discovery
or clarification question, or an answer that only updates the conversation-only
pending batch of §1):

- no terminal result exists yet, so there is nothing to preview, approve, or
  append this turn;
- the Output Format states `RECORDING STATUS: NONE THIS TURN`; the orchestrator
  does NOT fabricate a decision/approval row and does NOT start an approval
  ceremony for a decision that has not been reached;
- a low-risk batch still being ASSEMBLED (not yet at its §1 checkpoint) is
  none-this-turn — it becomes a BATCH record only when §1 steps 5–7 fire;
- invocation is not a recording: routing to an owning skill, and recording that
  skill's terminal result, are different turns.

**SINGLE-ENTRY form** (any one immutable entry — a **DECISION**, an **APPROVAL**
(`A-*`), or a **STATE SNAPSHOT**; ALWAYS used for a high-risk action, and ALWAYS
for an implementation-authority Approval grant, which is never batched):

- exact target path;
- exactly one entry ID (a `PS-*` decision, an `A-*` approval, or an `SS-*` snapshot);
- the entry's date;
- attribution (`user` | `orchestrator-via-<skill>`);
- the byte-for-byte full entry (no ellipsis, no omitted column) — for an APPROVAL
  entry this includes its ACTIVE status, its allowed scope, AND its **FORBIDDEN**
  scope, each anchored to immutable evidence, never a mutable projection;
- ONE approval question for that entry;
- exact post-write confirmation — the appended entry reproduced, or an exact
  hash + complete path + entry id.

**LOW-RISK-BATCH form** (only the low-risk, reversible product-definition
decisions of §1):

- the exact target path (or paths);
- the ORDERED list of EVERY entry ID in the batch;
- each entry's date and attribution;
- the byte-for-byte full content of EVERY entry (nothing summarized or omitted
  from the preview);
- the exact mutable-projection refresh, if one is included, shown in the SAME
  preview;
- ONE approval question covering exactly that complete, bounded batch — no entry
  is added to or removed from it after it is shown;
- an atomic append where practical (all entries, then the projection refresh);
- post-write confirmation LISTING every recorded ID and every refreshed
  projection;
- partial-failure handling: if the atomic append cannot complete, report EXACTLY
  which entries and which projection refresh did and did NOT land, and treat the
  batch as not fully recorded (re-propose the remainder).

The batch preview is complete or it is not shown: an orchestrator never omits an
entry from the preview or the confirmation, and never silently reverts a batch to
several separate approval turns.

## 2. Authority grants are separate and explicit (deny-by-default)

Scope agreement, product-spec acceptance, design acceptance, and "permission to
proceed" are **not** implementation authority. Authority to implement is a
SEPARATE grant, recorded as its own Approval entry whose allowed scope and
**FORBIDDEN** scope are previewed and recorded before anything runs
(`scoped-approval-register` via the template's Approvals table).

- Ambiguous words — "yes", "continue", "proceed", "looks good", "that works" —
  apply ONLY to the exact proposal immediately awaiting approval. Approval is
  never widened by inference to an adjacent or later action.
- Nothing that changes the world — installing a package, scaffolding, editing
  source, running a migration, a network action, a commit or push, a
  deployment, any implementation — happens without the relevant ACTIVE
  authority grant covering it as worded. Absent that grant, halt and route
  through `human-approval-boundary` + `change-classification-gate` +
  `agent-authorization-matrix`.

## 3. Idempotent and exact recording

- **Exact means complete, byte-for-byte.** A preview or confirmation that must
  be exact never uses an ellipsis, an omitted column, a truncated anchor, a
  summary, or a paraphrase. Post-write confirmation reproduces the exact entry,
  OR gives an exact hash plus the complete file location and the entry
  identifier.
- **Proposal fingerprint (do not repeat a corrected proposal).** A user
  correction supersedes the prior proposal: the rejected proposal is invalid
  and is discarded, not offered again unless the user explicitly restores it.
  Keep an in-turn fingerprint of the proposal awaiting approval so a rejected
  one is not re-emitted.
- **Already-recorded scan (no duplicates).** Before proposing a new entry, scan
  the existing IDs and the semantic content of the records. If the decision is
  already recorded, report it AS recorded and move to the next valid action —
  never mint a duplicate ID or a semantically duplicate row.
- **Checklist-derived counts.** Any "question X of Y" progress count is derived
  from an explicit checklist, not conversational memory. When the set changes,
  show the corrected count; never claim "X of Y" unless Y is stable and
  evidence-backed.

## 4. Mutable-projection refresh (cite the template)

The current-view sections are mutable **projections** re-derived from the
immutable records; the immutable evidence sections are append-only. A projection
never contradicts the records — if it would, it is stale and is refreshed from
the records (the exact refresh previewed inside the same low-risk batch) before
a stage is reported complete. See
[project-state-template.md](project-state-template.md) for the section list and
the conflict rule; nothing here changes that schema.

## Stop conditions

- A consequential, authority-changing, or irreversible action is in a low-risk
  batch → pull it out; it gets its own explicit approval.
- Scope, spec, or design acceptance is being read as authority to implement →
  it is not; require a separate, previewed, recorded implementation grant.
- A rejected proposal is about to be re-offered, or an already-recorded decision
  re-proposed → stop; report the recorded state and take the next valid action.
