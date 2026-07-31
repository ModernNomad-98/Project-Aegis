# Semantic-review rubric — Project Aegis corpus audit

Companion to `scripts/audit-skill-contracts.py`. The mechanical audit finds
what regexes can bind; THIS rubric is the repeatable judgment pass for what
they cannot. It is applied per shipped skill, by inspecting the skill's
contracts and its connected surfaces (description, body, references, evals,
named neighbors) — never by manually invoking the skill (the AEGIS program
forbids another manual journey; behavioral proof comes from the future
behavioral-eval runner, AEGIS-018).

## Provenance

- Program: AEGIS-001..059 remediation (baseline frozen under
  `docs/audits/volunteerflow/`).
- A rubric verdict is a **semantic finding**: it must cite file:line evidence
  and is still not behavioral proof. Proof types stay separated (structural
  validator / static contract audit / fixture tests / behavioral evals /
  fresh-session regression / manual review).

## The twelve questions

Score each PASS / CONCERN / FAIL, with evidence, or N/A with a reason.

1. **Routing.** Does the description route the correct requests — and only
   those? (Trigger-oriented, not merely descriptive.)
2. **Exclusions.** Are the exclusions complete and reciprocal? Does every
   named neighbor point back where the seam is genuinely shared?
3. **Authority.** Does the workflow stay inside the skill's authority — no
   step that decides, writes, advances, or promises something a different
   skill or the human owns?
4. **Preservation.** Does it preserve source requirements and user
   constraints across its transformation (nothing silently dropped,
   downgraded to "assumption", or invented — AEGIS-021/-022/-026)?
5. **Evidence honesty.** Does it claim evidence it cannot possess (verified
   absence from unknowns, fit from targets, confidence from authorization —
   AEGIS-042/-047/-048)?
6. **Word discipline.** Does it confuse approval, scope, rank, sequence,
   plan, estimate, commitment, or result (AEGIS-033/-037/-039/-044)?
7. **Scope containment.** Does it introduce unapproved work (invented
   backlog items, polish categories, silently split releases — AEGIS-022/-037)?
8. **Stop Conditions.** Are they sufficient — do they actually refuse the
   forbidden action, or only describe it?
9. **Eval bite.** Do the evals challenge the highest-risk behavior, or only
   the happy path (AEGIS-014/-018)?
10. **Resumability.** Does the output create a durable, resumable artifact
    when one is required — owner, path, provenance, durability level
    (AEGIS-049/-050/-053..056)?
11. **Return control.** Does the skill return control to the correct outer
    owner, carrying the interaction contract with it (AEGIS-007/-032)?
12. **Novice legibility.** Could a genuine novice understand any approval
    decision this skill assigns to them (AEGIS-030)?

## How results are recorded

- Per-skill worksheet rows: `skill | question | verdict | evidence | note`.
- A FAIL that is materially distinct, reusable as a failure mode, not covered
  by AEGIS-001..059, surface-attributed, and remediation-ownable becomes a
  **candidate AEGIS-060+ entry** in
  [aegis-060-plus-register.md](aegis-060-plus-register.md).
- Everything else lands as a remediation-batch note. Do NOT mint an ID for a
  minor wording issue.

## Coverage record (kept honest)

The register records which skills have received a full twelve-question pass
and which have received only the mechanical audit. Unreviewed is stated as
unreviewed — never implied as clean.

## The executable queue

The engine's `--queue` output
(`artifacts/audits/semantic-review-queue.json`) is the structured to-do list
this rubric is executed FROM: each semantic-candidate finding routed to its
owning reviewer skill, plus a rubric-pass entry per shipped skill. A future
runner executes queue entries in isolated sessions; the queue is never
worked by manually invoking reviewer skills across the corpus in one
conversation.
