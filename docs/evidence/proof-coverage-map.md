# Proof coverage map: 23 discipline families × Proof #1

**Status:** point-in-time map, compiled 2026-10-29. **Docs-only.** This page adds no skill,
workflow, code or bundle bytes.

**Base:** `501dff1f57246c25ae099b7b21d40915e373e9a3` (Project-Aegis `main`,
2026-10-29T22:35:09Z). **Proof #1 bundle:**
[`docs/evidence/aep3-item2-consumer-proof-20261029/`](aep3-item2-consumer-proof-20261029/)
(22 rows; 18 PASS / 3 FAIL / 1 UNRUN / 0 BLOCKED — bundle README §1). The bundle was last
changed by `63eb91794020f790be970d2c175447530d57681c` (2026-10-29T13:41:03-07:00), which
is contained in the base.

**Headline: 1 of 23 families is EXERCISED by Proof #1; 22 of 23 are NOT EXERCISED.** That
is the whole finding. This map records what the proof bundle records. It does not claim
that the other 22 families are absent, unused or defective, and it does not claim the one
exercised family was exercised well.

**Reading key.**
- **EXERCISED** — the proof bundle contains a primary record stating that a named skill
  from the family was invoked, loaded or followed by the performing session, at a cited
  bundle-relative `file:line`.
- **NOT EXERCISED** — no such record was found in the bundle. A skill named in an install
  manifest, an exclusion ledger, a review, or an ownership mapping is a mention, not an
  invocation; see [What counts as a recorded invocation](#what-counts-as-a-recorded-invocation).

## The map

All evidence paths are relative to `docs/evidence/aep3-item2-consumer-proof-20261029/`.

| # | Family | Skills | Proof #1 | Recorded invocation (bundle-relative) | Date · commit |
| --- | --- | ---: | --- | --- | --- |
| 1 | Operating discipline | 9 | **EXERCISED** | `records/CP-01-RECORD.md:90` — `agent-startup-context-gate`; `records/CP-01-RECORD.md:91` — `human-approval-boundary`; `records/CP-05-ROW-UPDATE.md:99-100` — `source-of-truth-reconciler` (loaded by the harness) | 2026-10-29 · `501dff1f` |
| 2 | AI-SDLC governance | 7 | NOT EXERCISED | no recorded invocation found | 2026-10-29 · `501dff1f` |
| 3 | Core architecture & engineering | 30 | NOT EXERCISED | no recorded invocation found | 2026-10-29 · `501dff1f` |
| 4 | SaaS & tenant isolation | 20 | NOT EXERCISED | no recorded invocation found | 2026-10-29 · `501dff1f` |
| 5 | Security, RLS & supply chain | 14 | NOT EXERCISED | no recorded invocation found | 2026-10-29 · `501dff1f` |
| 6 | QA, E2E & evidence | 28 | NOT EXERCISED | no recorded invocation found | 2026-10-29 · `501dff1f` |
| 7 | Cloud, DevOps, reliability & release | 15 | NOT EXERCISED | no recorded invocation found | 2026-10-29 · `501dff1f` |
| 8 | AI security & LLM systems | 16 | NOT EXERCISED | no recorded invocation found | 2026-10-29 · `501dff1f` |
| 9 | Agentic AI security | 6 | NOT EXERCISED | no recorded invocation found | 2026-10-29 · `501dff1f` |
| 10 | Compliance & governance | 9 | NOT EXERCISED | no recorded invocation found | 2026-10-29 · `501dff1f` |
| 11 | Library meta / self-application | 6 | NOT EXERCISED | no recorded invocation found | 2026-10-29 · `501dff1f` |
| 12 | Operational workflow patterns | 10 | NOT EXERCISED | no recorded invocation found | 2026-10-29 · `501dff1f` |
| 13 | Data + performance engineering & load validation | 15 | NOT EXERCISED | no recorded invocation found | 2026-10-29 · `501dff1f` |
| 14 | Product, PM & growth | 24 | NOT EXERCISED | no recorded invocation found | 2026-10-29 · `501dff1f` |
| 15 | Docs engineering | 8 | NOT EXERCISED | no recorded invocation found | 2026-10-29 · `501dff1f` |
| 16 | Staff+ IC, architecture advisory & framework refresh | 11 | NOT EXERCISED | no recorded invocation found | 2026-10-29 · `501dff1f` |
| 17 | OWASP web-app gap closure | 2 | NOT EXERCISED | no recorded invocation found | 2026-10-29 · `501dff1f` |
| 18 | SaaS architecture depth — strong cluster | 11 | NOT EXERCISED | no recorded invocation found | 2026-10-29 · `501dff1f` |
| 19 | SaaS architecture depth — low-priority set | 4 | NOT EXERCISED | no recorded invocation found | 2026-10-29 · `501dff1f` |
| 20 | CONSTRAIN/CURATE design pack | 3 | NOT EXERCISED | no recorded invocation found | 2026-10-29 · `501dff1f` |
| 21 | Security scanning & orchestration | 3 | NOT EXERCISED | no recorded invocation found | 2026-10-29 · `501dff1f` |
| 22 | Authority invalidation & propagation | 1 | NOT EXERCISED | no recorded invocation found | 2026-10-29 · `501dff1f` |
| 23 | Optional Aegis setup | 1 | NOT EXERCISED | no recorded invocation found | 2026-10-29 · `501dff1f` |

**Skill counts.** Each `Skills` value is the count printed in the README roster
([What's in the library](../../README.md#whats-in-the-library)); the 23 counts sum to the
**253 skills in 23 families** stated there. Two families print a sum: family 11 is
`5 + selector, 6` and family 14 is `23 + iteration, 24`; the table uses 6 and 24.

**Totals for this proof.**

| Measure | Value |
| --- | ---: |
| Families mapped | 23 |
| EXERCISED | 1 (family 1, Operating discipline) |
| NOT EXERCISED | 22 |
| Skills in the 23 families | 253 |
| Skills with a recorded invocation | 3 (all in family 1) |
| Recorded invocations in families 2–23 | 0 |

## What counts as a recorded invocation

The rule is the one in the 15:59 STATUS proposal (Block 2a): *EXERCISED only where a skill
in the family was actually invoked in the consumer proof with a recorded invocation;
everything else NOT EXERCISED — not inflated.*

Counted, because the record states the session read, loaded or followed the named skill:

- `agent-startup-context-gate` — `records/CP-01-RECORD.md:90`: the session "read
  `agent-startup-context-gate/SKILL.md` from line 270, its checklist reference,
  `docs/consumer-install-record.md` … followed the skill the startup rule requires".
- `human-approval-boundary` — `records/CP-01-RECORD.md:91`: the session "read `AGENTS.md`
  lines 86–145, skill lines 230–273, `human-approval-boundary` … found the authority/merge
  rules and the manual-only policy".
- `source-of-truth-reconciler` — `records/CP-05-ROW-UPDATE.md:99-100`: "the CLI loaded its
  own user-level plugins and one user-level skill (`source-of-truth-reconciler`, visible in
  the `system/init` event)".

Not counted, because none of these records states that a skill was invoked:

- `records/CP03-04-INSTALL-CONTROLS.json` lists installed skill files by path — an install
  manifest, not a session record.
- `records/CP03-REVIEW.md` names skills in an exclusion ledger and in review prose — package
  composition, not invocation.
- `records/CP-06-RECORD.md:9-22` names `product-spec-writer`, `prioritization-frame-picker`,
  `roadmap-under-uncertainty-planner` and `roadmap-to-commitments-translator` as the owners
  of four owner-stated outcomes. The record maps outcomes to owning skills; it does not say
  the session invoked them, and the outcomes are quoted from the owner's answers.
- `records/CP-CLOSEOUT-RECORD.md:190` names a missing `code-reviewer/SKILL.md` in a verifier
  fixture — a negative test, not an invocation.

**Absence check.** Every skill name under `.claude/skills/` was searched against the
bundle's 93 files. 41 names occur somewhere in the bundle; each occurrence was read and
classified into the two groups above. Only the three family-1 records state an invocation.
This is a text-and-records check, not a telemetry capture: the bundle cannot show a skill
that a session consulted without naming it, and a skill named once as background is still
not an invocation.

## How to update this map per proof

1. **Add a column, do not overwrite.** When Proof #2 lands, add a `P2` status column after
   `Proof #1`; then `P3`, `P4`, `P5` in order. A later proof never rewrites an earlier
   proof's cell: each cell is the status at that proof's own bundle and commit.
2. **Change NOT EXERCISED → EXERCISED only with a recorded invocation.** The evidence cell
   must name the skill and a bundle-relative `file:line`, prefixed by the proof id, for
   example `P2 records/CP-30-RECORD.md:41 — tenant-isolation-reviewer`. A skill that appears
   only in a plan, an install manifest, a review's exclusion ledger, a task list or an
   ownership mapping stays NOT EXERCISED.
3. **Record date and commit per proof.** Add the proof's bundle date and the base commit it
   was assessed at, in the same style as the `Date · commit` column. Do not backdate a
   later record into an earlier proof's column.
4. **Update the totals before publishing.** Recompute the `EXERCISED` / `NOT EXERCISED`
   counts and the per-proof covered-family counts; the totals table must equal the rows.
5. **Re-verify the citations.** Re-read every cited line at the new base, run the repository's
   Markdown link checker over this page and the README, and run `git diff --check` before
   committing. A cited line that has moved is a map defect, not a formatting nit.
6. **Keep the roster in step with the README.** Family names and `Skills` counts come from
   the README roster. If the README roster changes, update this page in the same change and
   restate the total; do not silently carry stale counts.
7. **Docs-only discipline.** Adding a proof row is a docs change: no skill, workflow, code
   or proof-bundle byte is edited to make a family fit.

## Planned proof shapes and coverage order

These are the shapes proposed in the 15:59 STATUS (Block 2b), in the proposed order. **None
is authorized, scheduled or run by this map**; the families listed are expected coverage,
not evidence.

| Order | Proof | Families covered (new) | Count | Minimal shape |
| ---: | --- | --- | ---: | --- |
| 1 | Proof #2 — small multi-tenant SaaS | 2, 3, 4, 5, 6, 7, 11, 12, 13, 18, 19 | 11 | Node 22 LTS + TypeScript + Fastify; Postgres 16 with row-level security; one migration; Vitest + supertest (unit, integration, cross-tenant negatives); two synthetic tenants; member vs admin; a feature flag; deploy gate + rollback; a sealed cross-tenant defect reviewed by fresh independent reviewers with the review skills installed; a reproduce runner |
| 2 | Proof #3 — LLM feature + agentic security | 8, 9, 17, 21, 22 | 5 | A chat feature over a synthetic corpus with tool calls, prompt-injection fixtures, cost/latency guardrails and an agent handoff; A09/A10 logging and error-path security; scan orchestration; authority invalidation |
| 3 | Proof #4 — product, docs, staff, design, setup | 14, 15, 16, 20, 23 | 5 | A no-code-ish product slice with specs/ADRs, a docs site, design-review artifacts and a setup walkthrough |
| 4 | Proof #5 — compliance evidence pack | 10 | 1 | Evidence collection over the outputs of Proofs #2–#4, producing a control crosswalk, evidence pack and gap audit |

The counts reconcile to 22 remaining families: 11 + 5 + 5 + 1 = 22, plus the family already
EXERCISED by Proof #1 = 23. The proposal counts Proof #2 as "12/22" because it also
reinforces family 1; the 11 families new to Proof #2 are the ones listed above.

## Limitations

1. **This is a self-reported map.** It was compiled by an agent from the proof bundle, not
   produced by a machine check. Every row is re-derivable from the cited lines, but a wrong
   citation is a wrong row; the map has no independent verifier of its own.
2. **Absence of evidence is not abstention.** `NOT EXERCISED` means no invocation was found
   in the Proof #1 bundle. It does not mean the family was considered and deliberately
   skipped, that it is irrelevant to a static-site product, or that no session ever consulted
   one of its skills outside the recorded bundle. Conversely, `EXERCISED` does not show the
   skill was used well, that its procedure changed the outcome, or that the family would be
   exercised on another host, model or product.
3. **Proof #1's consumer repository is outside this repository's check surface.** The proof
   ran against `ModernNomad-98/aegis-consumer-proof` and a GitHub Pages deployment — separate
   systems that an outside tool reading only Project-Aegis cannot read. This repository's link
   checker and CI can verify the exported bundle's bytes and links; they cannot re-read the
   consumer repository's historical deployment state, the owner-run browser session, the
   provider API responses or the temporary settings change the bundle records. Those are
   citations into the export, not live observability.
4. **This map is not a certification.** It is not readiness, quality, coverage, security or
   compliance evidence, and `1 of 23` is not a score. It does not say the library is
   one-twenty-third useful; it says the recorded proof exercised one family.
5. **Point-in-time and non-retroactive.** The map is bound to base `501dff1f` and the bundle
   at `63eb9179`. A later proof, a later bundle revision or a later README roster does not
   retroactively change a cell; it adds a new column or a new revision row.
6. **The planned proofs are proposals.** Proofs #2–#5 have no app, host, review, bundle or
   result. Nothing in the coverage table above should be read as a commitment or a date.

## Verification

```sh
git rev-parse 501dff1f57246c25ae099b7b21d40915e373e9a3
# 501dff1f57246c25ae099b7b21d40915e373e9a3
git log -1 --format='%H %cI' -- docs/evidence/aep3-item2-consumer-proof-20261029
# 63eb91794020f790be970d2c175447530d57681c 2026-10-29T13:41:03-07:00
sed -n '90,91p' docs/evidence/aep3-item2-consumer-proof-20261029/records/CP-01-RECORD.md
sed -n '99,100p' docs/evidence/aep3-item2-consumer-proof-20261029/records/CP-05-ROW-UPDATE.md
```

The counts in this page were checked against the README roster at the same base: 23 family
entries, counts summing to 253, one family with a recorded invocation and 22 without.

## Change log

| Date | Change | Basis |
| --- | --- | --- |
| 2026-10-29 | Initial map: 23 families × Proof #1; 1 EXERCISED, 22 NOT EXERCISED | Base `501dff1f`; bundle `63eb9179`; proposal in the 15:59 STATUS, Block 2 |
