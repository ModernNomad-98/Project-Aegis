# `docs/project-state.md` — schema and template

This is the durable memory of a project's journey from idea to shipped. The
orchestrator **reads it first every session** (the latest STATE SNAPSHOT entry
locates the project on the lifecycle map) and **appends to it** as the project
advances — each entry previewed (exact path + content) and explicitly approved
by the user before it is written, and the file itself created at cold start
only after the COMPLETE initial document has been previewed and approved (the
orchestrator's Capability 4 propose → approve → append/create contract). It
lives in the **user's product repo** at `docs/project-state.md` — never in the
skills library.

## Composition (what this schema reuses, by name)

- **Decision log** composes `phased-work-handoff-designer`'s decision-ID
  register: every binding decision gets a stable ID and is carried forward;
  each entry declares whether it **still binds**; a changed decision is a **new
  entry that flags the deviation**, never a silent overwrite.
- **Approvals** composes `scoped-approval-register`'s citation pattern: Status /
  Scope allowed / **Scope FORBIDDEN** / Evidence, append-style, supersede-never-
  rewrite, deny-by-default (an action is authorized only if an ACTIVE entry's
  allowed scope covers it as worded).
- **Plain-language summaries** are the house decision-log format: a human
  reading months later understands each entry without re-deriving it.

## Non-negotiable rules

1. **Two dated entry types.** A log entry is exactly one of: a **DECISION**
   (a choice made — the decision log) or a **STATE SNAPSHOT** (where the
   project stands: current stage + next recommended action — the snapshots
   table). Both go through the same propose → approve → append flow
   (Capability 4). **Latest snapshot wins:** the newest snapshot row IS the
   current state; there is no mutable header field, and no field is ever
   overwritten in place.
2. **Append-only.** Never edit or delete a past entry. A correction is a NEW
   dated entry that references and supersedes the old one — the Zero Trust AI
   Engineering Discipline applied to the build journey.
3. **Dated.** Every entry carries an ISO date (`YYYY-MM-DD`; add time where two
   entries land the same day and order matters).
4. **Plain language.** Summaries are readable by a non-developer. Technical
   terms, when unavoidable, are explained in the same line.
5. **Rationale required.** Every DECISION entry carries its **"(chosen over …,
   because …)"** clause — the main rejected alternative and the why, in plain
   language. An entry without it is not ready to propose.
6. **Attributed.** Every decision says who decided: `user` (a business decision
   the user authorized) or `orchestrator-via-<skill>` (an engineering decision
   the orchestrator made through the owning skill and explained).
7. **No secrets, no live identifiers.** Reference environments, tenants, and
   people by role or placeholder, never by credential or real name.

---

## Template (copy into `docs/project-state.md`)

```markdown
# Project State — <plain project name>

## State snapshots (append-only) — the LATEST row is the current state

| ID | Date | Current stage (plain language) | Next recommended action |
|----|------|--------------------------------|-------------------------|
| SS-001 | <YYYY-MM-DD> | <e.g. "Design: how it will be built"> | <one plain-language sentence> |

## The idea (approved brief)

- What the business does: <one line>
- What goes wrong today: <the problem, in the user's words>
- Who the customers/users are: <one line>
- What "done enough to ship" means (MVP): <the agreed first-release scope>

## MVP scope (approved)

- In scope for v1: <bullet list — what the first release WILL do>
- Explicitly OUT of scope for v1: <bullet list — what it deliberately will NOT do>
- Approved by: <user> on <YYYY-MM-DD>   (see Approval A-001)

## Decision log (append-only)

| ID | Date | Decision (plain language) | Who decided | Still binding? | Evidence / next gate |
|----|------|---------------------------|-------------|----------------|----------------------|
| PS-001 | <date> | <what was decided (chosen over <the main rejected alternative>, because <the plain-language why>)> | user \| orchestrator-via-<skill> | yes | <link / skill output / the gate this unblocks> |

## Approvals (irreversible steps & scope grants)

| ID | Status | Date / who | Scope allowed | Scope FORBIDDEN | Evidence |
|----|--------|-----------|---------------|-----------------|----------|
| A-001 | ACTIVE \| SUPERSEDED by <id> \| EXPIRED <date> | <date> / user | <exactly what was authorized, as worded> | <adjacent action this does NOT authorize> | <where the grant is recorded> |

## Open questions (still need the user)

- <one plain-language question at a time; the decision it unblocks>

## Deviations (a decision changed course)

- <PS-00x superseded by PS-00y on <date>: what changed and why — the old entry
  stays above, unedited>
```

---

## Worked example (generic maintenance-company illustration)

```markdown
# Project State — Maintenance job-tracking app

## State snapshots (append-only) — the LATEST row is the current state

| ID | Date | Current stage (plain language) | Next recommended action |
|----|------|--------------------------------|-------------------------|
| SS-001 | 2026-02-20 | Defining the product (the need is understood) | Approve the first-release scope below, then I hand it to the product-spec skill. |
| SS-002 | 2026-03-04 | Design: how it will be built | Answer one question about customer data separation, then I hand the data design to the multi-tenant data skill. |

## The idea (approved brief)

- What the business does: dispatches maintenance crews to customer sites.
- What goes wrong today: jobs get missed because they're tracked on paper.
- Who the customers/users are: office dispatchers (internal) and site contacts
  (external, who want a status link).
- What "done enough to ship" means (MVP): create a job, assign a crew, mark it
  done, and send the site contact a status link.

## MVP scope (approved)

- In scope for v1: job create/assign/complete; crew list; customer status link.
- Explicitly OUT of scope for v1: invoicing, scheduling optimization, a mobile app.
- Approved by: user on 2026-02-20 (see Approval A-001)

## Decision log (append-only)

| ID | Date | Decision (plain language) | Who decided | Still binding? | Evidence / next gate |
|----|------|---------------------------|-------------|----------------|----------------------|
| PS-001 | 2026-02-20 | Ship a small first version: create/assign/complete a job + a customer status link (chosen over a bigger first release, because a small v1 ships sooner and teaches us more). Everything else waits. | user | yes | brief above; unblocks product spec |
| PS-002 | 2026-02-27 | Build it as one connected system for now (chosen over many separate services, because one system is cheaper and simpler for a small team and a few hundred users). | orchestrator-via-architecture-advisor | yes | advisor output; unblocks data design |
| PS-003 | 2026-03-04 | Status links stop working when the job closes (chosen over "expire in 30 days" / "last forever", because a closed job's details shouldn't stay reachable). | user | yes | unblocks share-link design |

## Approvals (irreversible steps & scope grants)

| ID | Status | Date / who | Scope allowed | Scope FORBIDDEN | Evidence |
|----|--------|-----------|---------------|-----------------|----------|
| A-001 | ACTIVE | 2026-02-20 / user | Build the v1 scope listed above. | Adding invoicing or a mobile app without a new decision. | brief sign-off, this file |

## Open questions (still need the user)

- Should every customer's data sit in its own separate space, or share one space
  with strict rules keeping them apart? (Separate costs more; shared is cheaper
  and still safe when done right.) — unblocks the data design.
```

Note how the user only ever answered **business** questions (what to ship, when a
link should die, how separate customer data should feel), while the
"one connected system vs many services" call was made by the orchestrator through
`architecture-advisor` and recorded as `orchestrator-via-…` — explained in plain
language, never handed to the user as a technical choice. Every decision row
carries its "(chosen over …, because …)" clause, and where the project stands
lives in the snapshots table — the stage advance on 2026-03-04 is a NEW
snapshot row (SS-002), not an edit to a header or to SS-001.
