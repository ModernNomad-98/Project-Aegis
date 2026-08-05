# `docs/project-state.md` — schema and template

This is the durable memory of a project's journey from idea to shipped. The
orchestrator **reads it first every session** (the latest STATE SNAPSHOT entry
locates the project on the lifecycle map), **appends** immutable evidence to it
as the project advances, and **refreshes** its mutable projection sections at
approved logical checkpoints — each write previewed (exact path + content) and
explicitly approved by the user before it happens, and the file itself created
at cold start only after the COMPLETE initial document has been previewed and
approved (the orchestrator's Capability 4 propose → approve → append/refresh
contract). It lives in the **user's product repo** at `docs/project-state.md` —
never in the skills library, and never confused with it.

## Composition (what this schema reuses, by name)

- **Decision log** composes `phased-work-handoff-designer`'s decision-ID
  register: every binding decision gets a stable ID and is carried forward;
  each entry declares whether it **still binds**; a changed decision is a **new
  entry that flags the deviation**, never a silent overwrite.
- **Approvals** composes `scoped-approval-register`'s citation pattern: Status /
  Scope allowed / **Scope FORBIDDEN** / Evidence, append-style, supersede-never-
  rewrite, deny-by-default (an action is authorized only if an ACTIVE entry's
  allowed scope covers it as worded). An ACTIVE approval's allowed scope is
  **frozen to immutable evidence** — stated inline exactly, or referenced by a
  DECISION id or an accepted-artifact path + SHA-256, never by pointer to a
  mutable projection — so a later projection refresh cannot change what was
  approved; a scope change is a NEW superseding approval entry. **Scope
  agreement, spec acceptance, and design acceptance are NOT implementation
  authority** — that is a separate,
  explicitly previewed and separately recorded grant.
- **Plain-language summaries** are the house decision-log format: a human
  reading months later understands each entry without re-deriving it.

## Non-negotiable rules

1. **Two dated entry types.** A log entry is exactly one of: a **DECISION**
   (a choice made — the decision log) or a **STATE SNAPSHOT** (where the
   project stands: current stage + next recommended action — the snapshots
   table). Both go through the same propose → approve → append flow
   (Capability 4). **Latest snapshot wins:** the newest snapshot row IS the
   current state; there is no mutable header field, and no immutable row is ever
   changed in place.
2. **Append-only immutable evidence.** The evidence sections — State snapshots,
   Decision log, Approvals, Deviations — are append-only. Never edit, delete,
   reorder, or silently replace a past row. A correction is a NEW dated entry
   that references and supersedes the old one, which stays unedited above — the
   Zero Trust AI Engineering Discipline applied to the build journey.
3. **Mutable projection, refreshed not rewritten as evidence.** The
   current-view sections (below) are mutable projections of the current truth.
   They are **re-derived from the authoritative immutable evidence** at approved
   checkpoints; they are never treated as evidence and never contradict it.
4. **Dated.** Every entry carries an ISO date (`YYYY-MM-DD`; add time where two
   entries land the same day and order matters).
5. **Plain language.** Summaries are readable by a non-developer. Technical
   terms, when unavoidable, are explained in the same line.
6. **Rationale required.** Every DECISION entry carries its **"(chosen over …,
   because …)"** clause — the main rejected alternative and the why, in plain
   language. An entry without it is not ready to propose.
7. **Attributed.** Every decision says who decided: `user` (a business decision
   the user authorized) or `orchestrator-via-<skill>` (an engineering decision
   the orchestrator made through the owning skill and explained).
8. **No secrets, no live identifiers.** Reference environments, tenants, and
   people by role or placeholder, never by credential or real name.
9. **Empty-state rows are preserved, not overwritten.** An empty-state
   placeholder row in an immutable table (e.g. the `SS-001 | <YYYY-MM-DD> | …`
   scaffolding row, or a decision-log row that reads `(none recorded)`) is
   template scaffolding. The first REAL entry is **appended after it**; the
   placeholder row is never edited into the real entry. A defined
   mutable-template-initialization may drop the scaffolding row ONCE, before any
   real evidence exists; once real evidence exists the immutable rows are
   append-only.
10. **Conflict detection — immutable evidence wins.** If a mutable projection
    disagrees with the immutable Decision log, Approvals, or an accepted spec,
    the immutable record is authoritative and the projection is stale. A stale
    projection is refreshed (from the records) before a stage is reported
    complete; the projection never overrides the evidence.

## Section mutability — immutable evidence vs mutable projection

Two kinds of section, governed differently. A future session must find **one
coherent current truth**: the projections agree with the evidence, or they are
refreshed until they do.

**A. Immutable evidence history (append-only — rules 1, 2):**

- **State snapshots** — the dated stage + next-action log (latest row wins).
- **Decision log** — every binding decision, with its chosen-over rationale.
- **Approvals** — scope grants and irreversible-step authorizations.
- **Deviations** — a decision that changed course (superseding entries).

These are never edited, deleted, reordered, or replaced. Corrections append a
new superseding entry.

**B. Mutable current projection (refresh at approved checkpoints — rule 3):**

- **Current product summary** — what the product is, today.
- **Current approved scope** — what v1 will and will not do, today.
- **Current users/roles** — who uses it, today.
- **Current success definition** — what "done enough" means, today.
- **Open questions** — what still needs the user, today.
- **Next recommended action** — when it is not simply the latest snapshot's.

Each mutable section is marked **"Current projection — refresh from
authoritative recorded decisions and accepted artifacts."** It is re-derived
from the evidence at a logical recording checkpoint (not after every answer),
and the exact proposed refresh is previewed as part of the same low-risk
recording batch that the user approves. A projection never contradicts binding
evidence; if it would, it is stale and is refreshed first (rule 10). Nothing in
a projection is itself a binding decision or an approval.

**C. Pending low-risk decision batch (conversation-only, not in the file yet).**
Low-risk, reversible product-definition decisions may accumulate in the
conversation as a visible pending batch. The batch is not binding and not
recorded; it is shown completely before approval and disappears after it is
recorded (append) or explicitly rejected. High-risk, authority-changing, or
irreversible actions are never batched — each takes its own explicit approval.

**Stage 2 owner status uses the existing DECISION entry type.** Under the
orchestrator's Stage 2 exit gate, each Stage 2 owner becomes ONE append-only
DECISION entry — product specification complete; prioritization complete or
`not applicable` (reason); roadmap complete or `not applicable` (reason);
commitment readiness complete, `not applicable` (reason), or `NOT COMMIT-ABLE`
(missing evidence + reassessment point). **A terminal analytical result does
NOT record itself.** Reaching a terminal result first puts the owner in an
`*-awaiting-record` state; the DECISION entry becomes recorded only after the
exact entry is previewed (exact path + id + date + byte-for-byte content),
explicitly approved by the user, appended, and confirmed — the Capability 4
flow. Until that append is confirmed the owner is NOT recorded and the exit gate
stays BLOCKED.

**The product-spec owner needs the user's acceptance of the specification —
not just an approval to append a row.** Approving the exact WORDING of a DECISION
entry (Capability 4) is a different act from the user accepting what the
specification actually says. So the product-spec owner records TWO append-only
decisions, in order: first the **user's acceptance of the specification**,
attributed to `user` and anchored to the accepted artifact by its path + a
SHA-256 of that artifact + the acceptance date (a status a later reader can
verify, never the bare token `spec`); then the **owner-completion** entry
(attributed to `orchestrator-via-product-spec-writer`) whose Evidence REFERENCES
that acceptance decision and the same artifact. Without a recorded,
artifact-anchored user acceptance the product-spec owner stays BLOCKED, and the
four-owner gate can never open — and Stage 3 never begins — on a specification no
human durably accepted. Pending, unclassified, and `*-awaiting-record` owner states may
appear in the orchestrator's current-turn output but are NOT persisted as
binding decisions. The Stage 3 STATE SNAPSHOT is appended only after all four
owner DECISION entries are recorded and satisfy the exit gate. This adds NO new
entry type — it uses the existing DECISION, APPROVAL, and STATE SNAPSHOT entry
types exactly as defined above.

---

## Template (copy into `docs/project-state.md`)

```markdown
# Project State — <plain project name>

<!-- IMMUTABLE EVIDENCE (append-only) — never edit, delete, reorder, or replace a row -->

## State snapshots (append-only) — the LATEST row is the current state

| ID | Date | Current stage (plain language) | Next recommended action |
|----|------|--------------------------------|-------------------------|
| SS-001 | <YYYY-MM-DD> | <e.g. "Design: how it will be built"> | <one plain-language sentence> |

## Decision log (append-only)

| ID | Date | Decision (plain language) | Who decided | Still binding? | Evidence / next gate |
|----|------|---------------------------|-------------|----------------|----------------------|
| PS-001 | <date> | <what was decided (chosen over <the main rejected alternative>, because <the plain-language why>)> | user \| orchestrator-via-<skill> | yes | <link / skill output / the gate this unblocks> |
| PS-002 | <date> | User accepted the product specification — the actual spec content, not merely the wording of this row (chosen over proceeding on an unread draft, because Stage 3 must build the spec the user endorsed). | user | yes | accepted artifact `docs/specs/<product>-v1.md` @ sha256:<64-hex of that file>; accepted by user on <date> |
| PS-003 | <date> | Product specification owner complete — Stage 2 can classify the remaining owners (chosen over jumping to design, because the accepted spec is the Stage 2 foundation). | orchestrator-via-product-spec-writer | yes | references PS-002 (user acceptance) + `docs/specs/<product>-v1.md`; unblocks Stage 2 owner classification |
| PS-004 | <date> | Prioritization not applicable (chosen over ranking, because one bounded MVP with no competing initiative to rank). | orchestrator-via-project-orchestrator | yes | Stage 2 exit gate |
| PS-005 | <date> | Roadmap planning not applicable (chosen over sequencing horizons, because one bounded release with no sequencing decision). | orchestrator-via-project-orchestrator | yes | Stage 2 exit gate |
| PS-006 | <date> | Commitment readiness not applicable (chosen over a delivery promise, because no deadline or delivery commitment was requested). | orchestrator-via-project-orchestrator | yes | Stage 2 exit gate MET |

## Approvals (irreversible steps & scope grants)

| ID | Status | Date / who | Scope allowed | Scope FORBIDDEN | Evidence |
|----|--------|-----------|---------------|-----------------|----------|
| A-001 | ACTIVE \| SUPERSEDED by <id> \| EXPIRED <date> | <date> / user | <the exact allowed scope stated inline — or referenced to immutable evidence: a DECISION id, or an accepted-artifact path + SHA-256; NEVER a mutable projection> | <adjacent action this does NOT authorize — e.g. this is scope agreement only, NOT authority to implement> | <immutable reference: DECISION id / accepted-artifact path + SHA-256> |

## Deviations (a decision changed course)

- <PS-00x superseded by PS-00y on <date>: what changed and why — the old entry
  stays above, unedited>

<!-- MUTABLE PROJECTION — refresh from the authoritative records above at approved checkpoints; never contradicts them -->

## Current product summary — projection (refresh from records)

> Current projection — refresh from authoritative recorded decisions and accepted artifacts.

- What the business does: <one line>
- What goes wrong today: <the problem, in the user's words>
- Who the customers/users are: <one line>
- What "done enough to ship" means (MVP): <the agreed first-release scope>

## Current approved scope — projection (refresh from records)

> Current projection — refresh from authoritative recorded decisions and accepted artifacts.

- In scope for v1: <bullet list — what the first release WILL do>
- Explicitly OUT of scope for v1: <bullet list — what it deliberately will NOT do>
- Basis: approved by <user> on <YYYY-MM-DD> (see Approval A-001 and Decision PS-001)

## Current users/roles — projection (refresh from records)

- <role — what they do with the product>

## Current success definition — projection (refresh from records)

- <the observable outcome that means v1 worked, derived from the accepted spec>

## Open questions — projection (refresh from records)

> Current projection — refresh from authoritative recorded decisions and accepted artifacts.
> An answered question is removed here once its DECISION is recorded above.

- <one plain-language question at a time; the decision it unblocks>
```

---

## Worked example (generic maintenance-company illustration)

```markdown
# Project State — Maintenance job-tracking app

## State snapshots (append-only) — the LATEST row is the current state

| ID | Date | Current stage (plain language) | Next recommended action |
|----|------|--------------------------------|-------------------------|
| SS-001 | 2026-02-20 | Defining the product (the need is understood) | Approve the first-release scope, then I hand it to the product-spec skill. |
| SS-002 | 2026-03-04 | Design: how it will be built | Answer one question about customer data separation, then I hand the data design to the multi-tenant data skill. |

## Decision log (append-only)

| ID | Date | Decision (plain language) | Who decided | Still binding? | Evidence / next gate |
|----|------|---------------------------|-------------|----------------|----------------------|
| PS-001 | 2026-02-20 | Ship a small first version: create/assign/complete a job + a customer status link (chosen over a bigger first release, because a small v1 ships sooner and teaches us more). Everything else waits. | user | yes | brief above; unblocks product spec |
| PS-002 | 2026-02-24 | User accepted the product specification — the actual spec content, not merely this row's wording (chosen over proceeding on an unread draft, because Stage 3 must build the spec the user endorsed). | user | yes | accepted artifact `docs/specs/maintenance-job-tracker-v1.md` @ sha256:<64-hex of that file>; accepted by user on 2026-02-24 |
| PS-003 | 2026-02-24 | Product specification owner complete — Stage 2 can classify the remaining owners (chosen over jumping straight to design, because the accepted spec is the Stage 2 foundation). | orchestrator-via-product-spec-writer | yes | references PS-002 (user acceptance) + `docs/specs/maintenance-job-tracker-v1.md`; unblocks Stage 2 owner classification |
| PS-004 | 2026-02-25 09:00 | Prioritization not applicable (chosen over ranking, because there is one bounded MVP and no competing initiative to rank). | orchestrator-via-project-orchestrator | yes | Stage 2 exit gate |
| PS-005 | 2026-02-25 09:05 | Roadmap planning not applicable (chosen over sequencing horizons, because there is one bounded release and no sequencing decision). | orchestrator-via-project-orchestrator | yes | Stage 2 exit gate |
| PS-006 | 2026-02-25 09:10 | Commitment readiness not applicable (chosen over a delivery promise, because no deadline or delivery commitment was requested). | orchestrator-via-project-orchestrator | yes | Stage 2 exit gate MET → design may begin |
| PS-007 | 2026-02-27 | Build it as one connected system for now (chosen over many separate services, because one system is cheaper and simpler for a small team and a few hundred users). | orchestrator-via-architecture-advisor | yes | advisor output; unblocks data design |
| PS-008 | 2026-03-04 | Status links stop working when the job closes (chosen over "expire in 30 days" / "last forever", because a closed job's details shouldn't stay reachable). | user | yes | unblocks share-link design |

## Approvals (irreversible steps & scope grants)

| ID | Status | Date / who | Scope allowed | Scope FORBIDDEN | Evidence |
|----|--------|-----------|---------------|-----------------|----------|
| A-001 | ACTIVE | 2026-02-20 / user | The v1 scope EXACTLY as recorded in immutable Decision PS-001: create/assign/complete a job + a customer status link — the agreed first-release scope. (Authority source: Decision PS-001, not the mutable current-scope projection.) | Scope agreement ONLY — this is NOT authority to write code, install packages, run a migration, commit, push, or deploy. Implementation authority is a separate later approval. Adding invoicing or a mobile app needs a new decision. | Decision PS-001; brief sign-off, this file |

## Deviations (a decision changed course)

- (none recorded — no prior decision has been superseded)

## Current product summary — projection (refresh from records)

> Current projection — refresh from authoritative recorded decisions and accepted artifacts.

- What the business does: dispatches maintenance crews to customer sites.
- What goes wrong today: jobs get missed because they're tracked on paper.
- Who the customers/users are: office dispatchers (internal) and site contacts
  (external, who want a status link).
- What "done enough to ship" means (MVP): create a job, assign a crew, mark it
  done, and send the site contact a status link.

## Current approved scope — projection (refresh from records)

> Current projection — refresh from authoritative recorded decisions and accepted artifacts.

- In scope for v1: job create/assign/complete; crew list; customer status link.
- Explicitly OUT of scope for v1: invoicing, scheduling optimization, a mobile app.
- Basis: approved by user on 2026-02-20 (see Approval A-001 and Decision PS-001).

## Current success definition — projection (refresh from records)

- A dispatcher can create a job, assign a crew, and mark it done, and the site
  contact receives a working status link — with no job lost on paper.

## Open questions — projection (refresh from records)

> Current projection — refresh from authoritative recorded decisions and accepted artifacts.
> An answered question is removed here once its DECISION is recorded above.

- Should every customer's data sit in its own separate space, or share one space
  with strict rules keeping them apart? (Separate costs more; shared is cheaper
  and still safe when done right.) — unblocks the data design.
```

Note how the user only ever answered **business** questions (what to ship, when a
link should die, how separate customer data should feel), while the
"one connected system vs many services" call was made by the orchestrator through
`architecture-advisor` and recorded as `orchestrator-via-…` — explained in plain
language, never handed to the user as a technical choice. Every decision row
carries its "(chosen over …, because …)" clause. Where the project stands lives
in the snapshots table — the stage advance on 2026-03-04 is a NEW snapshot row
(SS-002), not an edit to a header or to SS-001. SS-002 advances to design only
after the user's own recorded spec acceptance (PS-002, attributed to `user` and
anchored to the accepted artifact by path + SHA-256 — an append approval is not a
content acceptance) and the four Stage 2 owner decisions — PS-003 (product-spec
owner complete, whose Evidence references PS-002) and PS-004 / PS-005 / PS-006
(prioritization / roadmap / commitment readiness each *not applicable*, with a
reason) — the Stage 2 exit gate, recorded as ordinary append-only DECISION
entries, each after its own previewed approval. The
current-view sections are **projections**: they render today's truth from the
records and are refreshed at checkpoints, while Approval A-001 makes explicit
that agreeing the scope is **not** authority to build — implementation is a
separate grant taken later.
