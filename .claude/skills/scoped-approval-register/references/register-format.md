# Approval Register — Immutable Records and Effective Authority

A grant records what a human authorized; later events record its lifecycle.
Neither record creates authority by itself.

## Immutable grant template

```markdown
### APR-013: Staging backfill

- **Event:** GRANT
- **Status at recording:** ACTIVE
- **Date / Grantor:** <ISO timestamp> / <named human or accountable role>
- **Reason:** <why this authorization was given>
- **Scope allowed:** <verbatim grant plus the exact proposal it answered>
- **Scope FORBIDDEN:** <actual prohibitions and allowed-scope boundaries;
  "none additionally stated" when appropriate>
- **Evidence:** <human source and retrievable pointer or dated verbatim record>
- **Expiry / use limit:** <actual date, condition or use count; none stated if absent>
```

The entry ID and every recorded byte are immutable. Legacy `Status: ACTIVE`
grant entries are read as their initial state, never as a live status cache.
A grant limited to one use remains limited even before consumption is transcribed.
An instruction to repeat an authorized repair loop must not be reduced to one use.

## Lifecycle event template

```markdown
### APR-014: Staging backfill consumed

- **Event:** CONSUMED
- **Target grant:** APR-013
- **Successor grant:** none
- **Effective at:** <ISO timestamp or unambiguous ordered condition>
- **Recorded at / By:** <ISO timestamp> / <recorder identity>
- **Reason / Evidence:** <actual action or human decision, with source>
- **New authority:** none
```

Event kinds are `REVOKED`, `EXPIRED`, `CONSUMED`, and `SUPERSEDED`.
`SUPERSEDED` names an earlier target grant and a distinct, already-recorded
successor GRANT with actual human evidence that explicitly replaces the
predecessor; overlap alone is not supersession. Revocation requires the human
withdrawal; expiry and consumption record facts under the original grant's terms.
Recording a fact later does not backdate the record or fabricate earlier approval.
Record the effective time separately from the transcription time.

The same form fits a project's Approvals table: use its next unique approval ID
for each event, name the event and target in the immutable row, and keep its
scope/evidence fields explicit. Do not add a mutable status column or change old
rows. Lifecycle rows belong to the APPROVAL entry type, not a new state type.

## Effective-status procedure

1. Validate unique record IDs, event kinds, target references and human source
   evidence. Preserve append/transcription order; effective times may precede
   transcription and need not increase with row order. Establish applicability
   by evidenced effective time, including late-recorded facts. An event targets an existing
   GRANT; a successor must be a distinct GRANT. Missing targets, duplicate IDs,
   self-links, cycles or contradictory events make affected authority unresolved;
   do not use those records to authorize action. Preserve and identify defective
   occurrences by location/hash in a non-authorizing annotation. An annotation
   does not repair or validate malformed history. Further authority requires a
   separately evidenced human grant with a fresh unambiguous ID; never edit old bytes.
2. Replay applicable events for the target through the proposed action time.
   A grant begins ACTIVE only if supported by the actual human decision. Apply
   revocation, supersession, expiry and exhaustion of its use limit. Evaluate the
   expiry/condition even if no EXPIRED event has been appended. If whether a use
   occurred is unknown, do not retry by assuming a one-use grant is unused.
3. Invalidation is terminal for that grant. A later literal ACTIVE row or
   removal/revocation/expiry of a successor cannot reactivate a predecessor.
   Reauthorization requires a NEW grant ID and a new human decision. Repeated
   reports of the same invalidating fact do not restore authority.
4. Only effectively ACTIVE grants can cover an action. Match actual allowed
   scope, environment, target, limits and applicable prohibitions. Inactive old
   FORBIDDEN clauses do not veto an explicitly authorized replacement forever.
   Where active human instructions conflict, use their actual precedence and
   explicit supersession; if still unresolved, ask about that conflict only.
5. Cite the grant, lifecycle records and time/use facts used for the decision.
   A current direct instruction is also valid source evidence; a lagging register
   is a recording gap, not grounds to demand the same grant again. Preserve its
   scope exactly when transcribing it.

An append-only register documents history; it is not a concurrency lock or a
tamper-proof authorization service. Concurrent consumption and permission
enforcement belong to the executing system. This document does not prove those
operational guarantees. Keep a granted recurring scope active until its actual
conditions end; routine use does not consume it as though it were one-time.

## Citation rule

> Register-derived authorization requires an effectively ACTIVE, evidenced human
> grant covering the action as worded, after full lifecycle and limit checks.
> Absence of a prohibition is not permission. Historical ACTIVE text is
> insufficient. Recording preserves existing human authority; it never creates,
> enlarges or silently narrows it, and does not require repeat consent for a
> current instruction already covering the action.

## Persistence and placement

Prefer one authoritative `docs/approvals/APPROVAL_REGISTER.md` or the product
repo's existing Approvals table. Other files link to it rather than creating
competing registers. This is a non-executable documentary record; it must not
double as permission configuration, policy code or agent instructions.

Draft in the conversation first. Show the exact path and appended content and
check whether current authorization covers recording it. Use that authorization
without asking again; if absent, obtain approval before writing. Keep prior bytes
unchanged. Authority comes from the human decision, not the act of writing.

Report storage precisely: draft = transcript-only; verified file write =
workspace-persisted. Claim Git-tracked, locally committed or remote-persisted only
after separately verifying each state. A local file is not a backup on GitHub.
Recording does not authorize a commit or push outside the user's applicable grant.

## Worked lifecycle

- APR-010 grants recurring staging validation until superseded, with human evidence.
- APR-011 records a newly granted staging-and-demo scope. APR-012 explicitly
  supersedes APR-010 with APR-011; APR-010's historical ACTIVE field is unchanged.
- APR-013 records revocation of APR-011. Neither grant now authorizes execution;
  APR-010 does not revive because its successor was revoked.
- APR-014 records a separate, human-approved one-time backfill. APR-015 records
  consumption. Another run cannot cite APR-014 even though its initial field
  still reads ACTIVE. It requires a new human grant.

## Anti-patterns

- Editing an old Status field, including a harmless-looking expiry update.
- Treating an old ACTIVE field as sufficient after a later revocation.
- Letting a new projection or revoked successor resurrect an old grant.
- Inventing prohibitions, expiry or use limits during transcription.
- Calling a local write remote-persisted without checking its published commit.
- Backdating a grant to excuse an earlier action or treating a machine record as
  independent evidence that a human gave approval.
