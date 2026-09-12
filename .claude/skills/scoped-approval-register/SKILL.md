---
name: scoped-approval-register
description: 'Preserve granted human approvals as immutable grant records and later lifecycle events, with verbatim scope and evidence. Derive effective authority from the complete history so revoked, expired, consumed, or superseded grants cannot revive. Use when an approval must be recorded, agents re-ask an existing permission, or an authorization needs a citable source. Draft first; persist only within applicable user authorization. Existing current-session grants remain valid without repeat consent. Do NOT use to decide whether approval is needed (human-approval-boundary), design standing approval policy (standing-approval-and-auto-advance), codify authority floors (agent-authorization-matrix), or record design choices (adr-writer).'
---

# Scoped Approval Register

## Purpose

Make granted approvals scoped and citable. A draft is transcript-only; a verified
file write is workspace-persisted. Git-tracked, locally committed, and
remote-persisted require their own verified Git/remote evidence. Approvals granted in
conversation evaporate when the conversation does — the next session either
re-asks (fatigue) or assumes (hazard). This skill records each grant as an
immutable register entry with five mandatory fields — Status, Reason,
Scope allowed, Scope FORBIDDEN, Evidence — so that months later an agent can
cite exactly what is and is not authorized, and negative scope is as explicit
as positive scope. The register is the TRACK half of the approval discipline:
`human-approval-boundary` obtains the decision; this skill makes it outlive
the chat. Evidence for the pattern: a production multi-agent repo (Repo A)
maintained ~60 such "narrow exception" blocks in its context map, each with
exactly these fields.

## Use When

- Use when: a human just granted an approval (in chat, PR comment, or issue)
  and it must be recorded before the wording is lost.
- Use when: an agent re-asks permission for something already decided, and no
  one can point to where the decision lives.
- Use when: "am I allowed to do X?" has no citable answer — set up or extend
  the register.
- Use when: auditing whether a past action was covered by a recorded grant
  (read the register; cite the entry).
- Do NOT use when: deciding whether the NEXT step needs approval or halting
  for it — that is `human-approval-boundary`; this skill records what that
  boundary obtains.
- Do NOT use when: designing a STANDING approval for the mechanical delivery
  loop with opt-out and phase-advance semantics — that is
  `standing-approval-and-auto-advance`; once designed and human-granted, its
  standing scope is recorded HERE as an entry.
- Do NOT use when: defining which actions agents may ever take autonomously —
  that is `agent-authorization-matrix` (the standing policy); the register
  records individual grants made under or beyond it.
- Do NOT use when: recording an architecture/technology decision with
  alternatives and consequences — that is `adr-writer`. Approvals authorize
  actions; ADRs record design choices.

## Inputs to Inspect

1. The grant itself — the human's exact wording, verbatim (chat message, PR
   comment, issue reply). The wording IS the scope; paraphrase widens or
   narrows it silently.
2. The existing register, if any (`docs/approvals/`, a context-map exceptions
   section, or wherever the repo keeps it) — to append, supersede, or detect
   conflicts with prior entries.
3. What was actually requested when the approval was sought — the
   `human-approval-boundary` request block if one exists (action, blast
   radius, options), so the recorded scope matches what was asked.
4. Expiry signals: did the grantor say "this once", "for this phase",
   "until X"? Durable vs one-time must come from the wording, not assumption.
5. Repo conventions for where governance records live (see
   [references/register-format.md](references/register-format.md) placement
   options).

## Workflow

1. **Capture the grant and the proposal it answers.** Quote the approving words
   and their source with the relevant request. A contextual "yes" to a complete
   proposal is usable approval; do not ask again because the answer is short.
   Clarify only scope still unresolved after reading the actual conversation.
2. **Locate or propose the register.** Prefer one dedicated, append-only file
   (e.g. `docs/approvals/APPROVAL_REGISTER.md`); a context-map exceptions
   section is an equally valid house pattern. One register per repo — split
   registers fragment citation.
3. **Draft the immutable entry** with all mandatory fields (full template and field
   semantics: [references/register-format.md](references/register-format.md)):
   Status, Date + Grantor, Reason, **Scope allowed** (as worded), **Scope
   FORBIDDEN** (explicit negatives — what this approval does NOT cover),
   Evidence (link/pointer to the grant), Expiry/review-by.
4. **Preserve the grant's boundaries.** Record explicit prohibitions and what
   the stated allowed scope excludes. If none were additionally stated, say so;
   do not invent a restriction, expiry, or one-use limit that narrows the human's
   instruction. Proposed safeguards are not existing grantor prohibitions.
5. **Check interactions without inventing supersession.** Preserve compatible
   overlapping grants. Append `SUPERSEDED` only when the human instruction
   actually replaces a predecessor, naming both grants and that evidence.
   Clarify unresolved conflicts only. Revocation, expiry and one-time consumption
   append events; no old field is edited. Apply the reference's full effective-status
   procedure, including malformed histories and late-recorded facts.
6. **State the citation rule with the register** (once, at the top): an
   action is covered only by an effectively ACTIVE grant whose actual scope
   includes it. Historical ACTIVE text alone does not authorize action. Current
   direct human instructions are themselves evidence; delayed transcription
   does not invalidate them or require repeat consent.
7. **Persist only within applicable authorization.** Show the exact target and
   proposed append. Use an existing current-session instruction covering this
   recording; ask once only if authority is missing. The documentation exception
   covers transcription, not changing permission controls or agent instructions.
   Verify the append and unchanged prior records. Report achieved persistence
   and entry IDs; a local write alone does not survive loss of the computer.

## Output Format

```
APPROVAL REGISTER ENTRY
Id:              <register-id — sequential or date-based>
Event:           GRANT | SUPERSEDED | EXPIRED | REVOKED | CONSUMED
Target:          <grant ID for lifecycle events; none for a new grant>
Successor:       <new grant ID for SUPERSEDED; otherwise none>
Status:          <state recorded by THIS immutable event, not a mutable field>
Date / Grantor:  <grant only: ISO timestamp / human or accountable role>
Effective at:    <lifecycle only: timestamp or ordered condition>
Recorded at/By:  <lifecycle only: transcription timestamp / recorder>
New authority:   <lifecycle only: none; scope fields refer to target grant>
Reason:          <why this authorization exists>
Scope allowed:   <exact actions, files, branches, environments — as worded by the grantor>
Scope FORBIDDEN: <actual prohibitions and scope limits; no invented restriction>
Evidence:        <link: PR comment / issue / chat record / commit>
Expiry:          <actual date/condition/use limit; none stated if absent>
Persistence:     transcript-only | workspace-persisted | Git-tracked | locally committed | remote-persisted
```

## Validation Checklist

- [ ] The grant is quoted or linked verbatim — the entry's scope matches the
      grantor's wording, not a paraphrase.
- [ ] Scope FORBIDDEN preserves actual limits without inventing restrictions.
- [ ] Evidence identifies the actual human source: a retrievable pointer or
      dated verbatim current-session record with its proposal context.
- [ ] Expiry/one-time vs durable comes from the wording, not assumption.
- [ ] Lifecycle events append by unique ID; prior entries remain unchanged.
- [ ] Full-history effective status and expiry/use limits are checked; revoking
      a successor does not revive its predecessor.
- [ ] Existing current-session authorization was honored without repeat consent.
- [ ] Persistence claims match the write/Git/remote verification actually done.
- [ ] No secrets, tokens, or live identifiers in the entry — reference
      environments and tenants by placeholder or name, never credential.

## Gotchas

- **Paraphrase drift:** "yes, go ahead" recorded as "approved schema changes"
  is a fabricated widening. Record the words and what they answered.
- **Invented negatives:** a recorder cannot withdraw part of a grant by adding
  a FORBIDDEN clause the human did not authorize.
- **Approval of a different step:** a grant for step A cited to authorize
  step B is the classic misuse; the citation rule (covered-by-wording) is
  what blocks it. See also `human-approval-boundary`'s rule that enthusiasm
  is not approval.
- **Stale ACTIVE text:** check later events and expiry/use conditions each time.
  Append observed expiry/consumption; do not rewrite the historical grant.
- **Two registers:** once approvals live in two places, every citation is
  contestable. Merge before appending.
- **Recording ≠ granting:** cite the actual human source. A missing archival
  pointer limits future verification; it does not erase a direct instruction
  still present in the current session. The register cannot create authority.

## Stop Conditions

- Asked to record an approval that was never actually granted (no quotable
  wording, no evidence) — refuse: the register preserves real grants; it
  does not manufacture them. This includes backdating entries "so the audit
  passes."
- The grant's wording is too ambiguous to scope and the grantor is
  unavailable — record nothing yet; a scoped question back to the grantor is
  the output.
- The new entry would contradict an ACTIVE entry and it is unclear which the
  grantor intends to stand — surface both, ask; do not pick.
- Asked to widen an existing entry's scope "since it's basically the same" —
  refuse; widening requires a new grant from the grantor.

## Supporting Files

- [references/register-format.md](references/register-format.md) — full entry
  template, field semantics, lifecycle states, placement options, a worked
  example, and anti-patterns.
- `evals/evals.json` — behavior cases incl. refusing to fabricate or backdate
  an entry.
- `evals/trigger-evals.json` — discrimination against `human-approval-boundary`,
  `standing-approval-and-auto-advance`, `agent-authorization-matrix`, and
  `adr-writer`.
