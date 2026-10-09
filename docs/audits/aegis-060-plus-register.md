# AEGIS-060+ register — proposed new findings, dedup map, and batch notes

> **Current reading, checked 2026-09-23:** This register is for maintainers
> tracking contract-audit findings numbered AEGIS-060 and later (AEGIS-001..059
> are the frozen earlier defect IDs). The AEGIS-060 rejection and typed
> skill/subagent correction below remain the disposition of that candidate.
> Sections 3–5 preserve the original 184-skill baseline's deduplication (dedup) map, coverage,
> and planned remediation sequence. Phrases there such as "current main" and
> "planned PR" (pull request) refer to that baseline, not today's source
> tree. For current skill contracts, inspect the
> [skills catalog](../skills-catalog.md) and
> [source files](../../.claude/skills/); do not schedule work solely from the
> historical rows.

**Current disposition, reconciled 2026-09-12:** AEGIS-060 is a **REJECTED
CANDIDATE / FALSE POSITIVE; ID RETIRED AND NEVER REUSED**. Merged
[PR #89](https://github.com/ModernNomad-98/Project-Aegis/pull/89), commit
`000352f55b71f0c3e897a482d279d34bfaa3d66b`, corrected contract-audit rule
EVAL-004 (which checks that each target named in a skill's trigger-eval file
exists), which had merged the separate skill and subagent namespaces. A
trigger-eval file is a skill's test file listing prompts that should or should
not trigger it. The `(subagent)`
annotations are valid typed targets; do not schedule their removal as
unfinished fixture work.

PR #89's audit-engine and regression-test corrections are integrated into
the calibration branch by merge `c7a92d208a8aec7295afa3e3188dce03a8331d0b`.
The historical baseline below is retained for provenance; it does not reopen
the rejected candidate.
The [merged disposition](https://github.com/ModernNomad-98/Project-Aegis/blob/000352f55b71f0c3e897a482d279d34bfaa3d66b/docs/audits/aegis-060-plus-register.md)
is authoritative.

**Shared-contract implementation checkpoint, 2026-09-12:** the fresh audit and
[complete candidate dispositions](../evidence/shared-contracts-closeout-2026-09-12/README.md)
record 19 confirmed repairs, 79 false positives and three adjacent write-boundary
repairs. This current checkpoint supersedes backlog assumptions about those
specific contracts; the frozen historical evidence and retired AEGIS-060 ID below
remain intact. It does not close unrelated AEGIS items or measured calibration.

**Delivery checkpoint:** [PR #90](https://github.com/ModernNomad-98/Project-Aegis/pull/90)
merged as `82dfebee7dadb68207bead5cb10fa3c562f21c1e`; the post-merge Actions run
passed. Its [final correction evidence](../evidence/shared-contracts-closeout-2026-09-12/corrected-verification.md)
also records the two addressed GitHub findings and corrected manual-skill count.

**Skill-contract disposition follow-up, 2026-09-26:** a fresh audit of main
`4227b71b7b8ede5d2670a0ca709fa9cfb5afce78` matched 75 of 84 semantic candidates
to the 2026-09-12 dispositions. The
[dated disposition record](../evidence/skill-contract-dispositions-2026-09-26/candidate-dispositions.md)
reviews the other nine: five new false positives and four rewordings where the
earlier judgment still applies. It finds no skill defect and changes no skill
text, frozen baseline or unrelated AEGIS item.

**ROUTE-002 disposition, 2026-09-26:** by owner decision, the
[ROUTE-002 dispositions record](../evidence/route002-dispositions-2026-09-26/README.md)
closes the §2 triage of ROUTE-002, the audit rule that reports one-way
exclusion edges (skill A says "use B instead" but B never names A). 31 edges
into 23 target skills were reciprocated in three merged batch PRs, and #395
also closed one edge added by reconciliation decision D64. Of the other 236,
235 are census data, not defects, and one is an engine false positive.
On 2026-09-27, PR #429 (`169e8be`, engine v1.13.2) fixed that false positive
by matching whole skill names only.

## Historical baseline (superseded where the current disposition says so)

Companion to the frozen AEGIS-001..059 baseline
([Project-Aegis-VolunteerFlow-Defect-Handoff-AEGIS-001-to-059.md](volunteerflow/Project-Aegis-VolunteerFlow-Defect-Handoff-AEGIS-001-to-059.md))
and the corpus contract audit (`scripts/audit-skill-contracts.py`; baseline
run: [`docs/audits/skill-contract-audit-baseline.md` at `6561944`](https://github.com/ModernNomad-98/Project-Aegis/blob/656194426e2ea3358fa29fcf19e05f0278d9c270/docs/audits/skill-contract-audit-baseline.md),
corpus tree `08727adf8f3e0f54226fa18639c9a50f2562ed22`, 184 skills).

**Baseline files regenerated, 2026-09-27.** By owner decision, the baseline
report and its three `artifacts/audits/` JSON (JavaScript Object Notation)
files were overwritten with a fresh engine v1.13.1 audit of main (186 skills,
317 findings). The numbers in sections 1–5 of this register still describe the
184-skill baselines, not today's files: section 1 uses the v1.12.0 baseline
(414 findings), while the section 3 table and its fixture note keep the first
v1.3.0 baseline from PR #75 (commit `469d4e5`, 416 findings), whose APPR-002
(a build scope granted at requirements approval), ROUTE-003 (a Stage-2 route
that reaches the commitments skill without a readiness guard) and STATE-005
(an "approved" narrative section inside an append-only file) rows do not
appear in the v1.12.0 report. The v1.12.0
files remain in git history
at commit `e2f1da0beb6e4aed07044ca3a90e841962bfd590` (PR #77). The report
link above points to its last copy, at commit
`656194426e2ea3358fa29fcf19e05f0278d9c270`, which adds the 2026-09-23 note
that its five EVAL-004 rows are rejected false positives; its measurements
are unchanged from `e2f1da0`. The historical counts below are unchanged.

**Baseline files regenerated again, 2026-09-27.** Under AEGIS-APR-065, an owner grant in the
[approval register](../approvals/APPROVAL_REGISTER.md), the
same four files were regenerated with engine v1.13.2 from main
`5dbf7bc9e958d932bd0c5b093ebecfe61be41840` (186 skills, 316 findings, of
which 232 are ROUTE-002). The v1.13.1 files described in the paragraph above
remain in git history at
[`7894567`](https://github.com/ModernNomad-98/Project-Aegis/tree/7894567d49d301f82f40cb6445b668581d5799ac/artifacts/audits)
(PR #432's merge; report:
[`docs/audits/skill-contract-audit-baseline.md` at `7894567`](https://github.com/ModernNomad-98/Project-Aegis/blob/7894567d49d301f82f40cb6445b668581d5799ac/docs/audits/skill-contract-audit-baseline.md)).
The historical counts below are unchanged.

**Report format updated, 2026-09-28.** Under AEGIS-APR-073, engine v1.13.3
rescanned the same commit `5dbf7bc9e958d932bd0c5b093ebecfe61be41840` and
changed only the report's format: a "How to read this report" key, the
ROUTE-002 example shown whole, and a corrected sentence that had said the
report froze the corpus before remediation. The findings (316), rule
inventory, vocabulary census and corpus hash are identical to v1.13.2, whose
files remain in git history at
[`3c51fb2`](https://github.com/ModernNomad-98/Project-Aegis/tree/3c51fb2f6f4a22c6120b38d2a7e9f0074b6bf69c/artifacts/audits)
(PR #441's merge). The historical counts below are unchanged.

**Report key extended, 2026-09-28.** Under AEGIS-APR-079, engine v1.13.4
rescanned the same commit `5dbf7bc9e958d932bd0c5b093ebecfe61be41840` and
changed only the report's format: the "How to read this report" key now
explains the rule-table tags (CENSUS, STRUCTURAL), Stage 2 and NOT
COMMIT-ABLE, auto-invocable, the SIDE-004 side-effect classes and the other
names used for semantic-review candidates, and spells out "hexadecimal";
the Coverage section now names `scripts/validate-skills.py`. The findings
(316), rule inventory, vocabulary census and corpus hash are identical to
v1.13.3, whose files remain in git history at
[`dc3c767`](https://github.com/ModernNomad-98/Project-Aegis/tree/dc3c767dc91d936cc8cc70589137ca33e6f44b7c/artifacts/audits)
(PR #461's merge). The historical counts below are unchanged.

**Baseline files regenerated, 2026-10-08.** Under AEGIS-APR-119, an owner grant
in the [approval register](../approvals/APPROVAL_REGISTER.md), the same four
files were regenerated with engine v1.13.4, unchanged, from
`cbb084d6f1f2acbd2373510dbd5290dcb18f285a` on branch
`claude/sharp-lovelace-urgxpz-fu2` (195 skills, 339 findings, of which 255 are
ROUTE-002). Against the v1.13.4 baseline, 24 findings were added and 1
removed, all ROUTE-002, 8 rows differ only in their line number, and the
84 semantic-review candidates are otherwise the same rows; 9 skills were
added and none removed. 24 ROUTE-002 rows name a skill pair absent from the
[2026-09-26 dispositions](../evidence/route002-dispositions-2026-09-26/README.md)
and are untriaged census rows. The v1.13.4 files remain in git history at
[`c14338d`](https://github.com/ModernNomad-98/Project-Aegis/tree/c14338d254bde3fd7fb9b8060033299cde5d5197/artifacts/audits)
(PR #503's merge). The historical counts below are unchanged.

**ROUTE-002 new-edge triage, 2026-10-09.** A fresh v1.13.4 audit at main `8e11c8f4c2777265e254057ce0fa1e52f0cf03bf` still reports 255 ROUTE-002 informational findings: 231 unchanged prior census pairs and 24 newly [reviewed textual pairs](../evidence/route002-triage-2026-10-09/README.md) (17 a, 2 b-high, 5 b-medium). N12 and N13 are candidates for a separately owner-selected reciprocal proposal only. The review records no owner selection of new skill edits, observed model misrouting, behavioral pass or new defect ID; the historical baseline paragraph above remains as recorded.

Rules of this register (from the program's operating rules):

- AEGIS-001..059 are never renumbered, merged, or reused. New IDs start at
  AEGIS-060 and are assigned sequentially.
- An entry here is a **candidate** until a remediation batch confirms it;
  incomplete evidence is marked as such, never rounded up to certainty.
- A baseline finding that maps onto an EXISTING ID is dedup-mapped below, not
  given a new ID.

---

## 1. New candidate findings

### AEGIS-060 (REJECTED CANDIDATE) — trigger-eval subagent annotations are valid typed-target syntax, not defects

- **Classification / severity / status:** Candidate fixture-hygiene defect / P2
  (severity level; the report orders P0, P1, P2, then info from most to least
  severe) / **REJECTED CANDIDATE — FALSE POSITIVE
  CAUSED BY EVAL-004 TYPE COLLAPSE; ID RETIRED AND NEVER REUSED**
- **What the candidate claimed (superseded):** that five trigger-eval files
  wrote neighbor identifiers as `"<name> (subagent)"` — "prose annotation
  inside the name field" — so a machine consumer could not resolve them
  against disk:
  - `.claude/skills/agent-goal-hijack-defender/evals/trigger-evals.json`
  - `.claude/skills/ai-evaluation-harness/evals/trigger-evals.json`
  - `.claude/skills/ai-threat-modeler/evals/trigger-evals.json`
  - `.claude/skills/prompt-injection-defender/evals/trigger-evals.json`
  - `.claude/skills/release-readiness-reviewer/evals/trigger-evals.json`
- **Why it is a false positive:** the annotation is **required target-kind
  syntax**, not prose. A bare name declares the SKILL namespace
  (`.claude/skills/<name>/`); an exact trailing `(subagent)` declares the
  SUBAGENT namespace (`.claude/agents/<name>.md`). The candidate's evidence
  came entirely from audit rule EVAL-004 as implemented in
  `audit-skill-contracts` v1.12.0, which unioned the two namespaces into one
  `known_names` set and regex-stripped `\s*\((?:sub)?agent\)\s*$` as
  removable prose — a **type collapse in the audit rule**, reported against
  correctly authored fixtures.
- **Reconciliation that settled it (authority order: merged implementation →
  effective merged design → audit logic → candidate register):**
  1. **Merged implementation** — `tools/behavioral_eval_runner/models.py::parse_target`
     returns `TargetKind.SUBAGENT` for a trailing `(subagent)`, retains the
     bare name as `target_name`, and retains `"(subagent)"` as
     `target_annotation`; a bare name returns `TargetKind.SKILL`.
     `census.py` applies that parser to `expected_skill`,
     `should_not_trigger`, and `overlaps_with`, and keys routing identities as
     `target_kind::target_name`, so a skill and a subagent sharing a name never
     collapse.
  2. **Effective merged design** — `behavioral-eval-runner-v1.md` §3 item 3
     ("typed, **NOT stripped**") and §5d (the parenthetical is "preserved,
     because it CHANGES the kind"; "a skill activation never satisfies a
     subagent-delegation expectation"). §20a-S4 records the strip-and-treat-as-
     metadata approach as already **superseded**. The fast-track successor
     (§1, §9) leaves §3/§5d untouched and authoritative.
  3. Both corrected targets exist as reviewer agents:
     `.claude/agents/ai-security-red-team-reviewer.md` (agent only — no skill
     of that name to collapse into) and `.claude/agents/release-readiness-reviewer.md`
     (the dual-namespace case, where a same-named skill also exists).
- **Corrected expected behavior:** trigger-eval machine fields hold the exact
  on-disk name **in the syntax that declares the target's kind**. Agent-vs-skill
  kind belongs in that syntax — NOT in `reason` prose, and not in a new field.
- **What happened in draft PR #89:**
  1. Commits `3944f25` / `c01a1c2` / `9d8d8eb` acted on the false candidate and
     stripped **nine** machine-resolved values across the five files above
     (agent-goal-hijack-defender 2, ai-evaluation-harness 1, ai-threat-modeler
     2, prompt-injection-defender 2, release-readiness-reviewer 2). Every one
     changed machine semantics; the `release-readiness-reviewer` case became
     indistinguishable from its own inline-skill case.
  2. A focused exact-diff review discovered the conflict **before merge**, and
     the owner rejected the remediation premise.
  3. A later **additive** correction commit in the same PR restored all nine
     values byte-for-byte — the five trigger-eval files are blob-equal to base
     `1c3e4931329179d9a3f9cc9ec1bb93020378c043` and leave the net PR diff.
  4. The actual correction was to EVAL-004: namespace-aware typed-target
     resolution, matching the merged runtime contract without importing it.
- **Corrected EVAL-004 behavior:** valid bare skill target → no finding; valid
  `(subagent)` target whose agent exists → no finding; name present only in the
  opposite namespace → **kind mismatch, mechanical P2**; name in neither
  namespace → **unknown target, mechanical P1**; unsupported trailing
  annotation → deterministic P1, never silently resolved to the leading name.
- **Measured result:** live EVAL-004 findings **5 → 0**, achieved by correcting
  the rule while the corpus is byte-identical to base (corpus content hash
  `9443a936961bb15a…` matches the pre-change measurement exactly). Total
  findings 414 → 409; the five removals are exactly the five false EVAL-004
  rows. Every other rule count is unchanged (ARTF-001, a durability claim with no
  named durability level, 10; ROUTE-002 311; SIDE-004, a side-effect
  instruction in a skill that may run automatically, 82; STATE-001, an
  editable placeholder in an append-only file, 2; VOCAB-002, "committed" used
  as a roadmap horizon label, 4; P0 2, P1 96, info 311). Route graph
  **byte-identical** — re-measured under v1.13.0 rather than carried over:
  SHA-256 (Secure Hash Algorithm 256) fingerprint `6c844eb6c35e1b40…`, 184 nodes / 968 edges, topology and bytes both
  unchanged (the route graph carries no tool-version provenance). Validator:
  184 skills valid, 0 warnings. Audit self-tests: **69** assertions pass (57 on
  the uncorrected engine, then +9 typed-target regressions, then +3 closing the
  automatic review findings below). Validator gate self-tests: 91 assertions
  pass.
- **Corrected engine version — `1.13.0`.** The type-collapsing engine that
  produced the AEGIS-060 false positives remains historically identified as
  **v1.12.0**, and every frozen artifact recording 1.12.0 is left exactly as it
  is. EVAL-004's observable semantics changed, so the corrected engine is
  **v1.13.0**: a corrected live report must be distinguishable by version, not
  only by `engine_sha256`. Read any 1.12.0-stamped EVAL-004 row as the old
  namespace-collapsing rule.
  *Amendment, 2026-09-27:* the promise above to leave every 1.12.0 artifact
  as it is was superseded by owner decision. The baseline report and its three
  `artifacts/audits/` JSON files were regenerated with engine v1.13.1; the
  1.12.0 files remain in git history at commit
  `e2f1da0beb6e4aed07044ca3a90e841962bfd590`. A later 2026-09-27
  regeneration under AEGIS-APR-065 used engine v1.13.2; the v1.13.1 files
  remain in git history at commit
  `7894567d49d301f82f40cb6445b668581d5799ac` (PR #432).
- **Automatic review findings closed (PR #89, reviewed commit `2d769dec87`).**
  The ready-for-review transition triggered an automatic review that raised
  three P2 findings against the correction itself; all three were valid and are
  closed additively:
  1. *Engine version.* Semantics changed while `TOOL_VERSION` still read
     1.12.0 → bumped to 1.13.0 (above), with a binding assertion.
  2. *Machine-surface coverage.* The typed-target fixture repeated one target
     across `overlaps_with`, `expected_skill`, and `should_not_trigger`, which
     `audit_evals` unions into a set — so deleting any single collector was
     masked by the other two. Each surface now carries its **own** unique
     target, positive and negative, and each collector is independently
     binding: removing any one of the three makes the regression fail on its
     own (verified by mutation).
  3. *Parser parity.* The audit's local parser rejected every trailing
     parenthetical other than the exact `(subagent)`, while the merged
     `models.parse_target` treats every other nonempty value as a **skill**
     target named by the complete string. Being stricter than the runtime is
     itself a defect: the audit now mirrors the runtime exactly, so
     `x (agent)` is a skill named `x (agent)` and surfaces as an ordinary
     unknown target (P1) rather than a special malformed class. The parity test
     covers bare, `(subagent)`, `(agent)`, `(subagent )`, `(reviewer)`,
     `(sub agent)`, `()`, a leading-marker string, and padded forms, asserting
     kind, complete name, and annotation. The Behavioral Eval Runner (BER)
     runtime is unchanged.
- **Negative regression retained:** the `thin-contract` fixture still proves
  EVAL-004 can fire — `ghost-neighbor` as an unknown target (P1) and
  `clean-skill (subagent)` as a **kind mismatch** (P2, because only the
  same-named skill exists and no `.claude/agents/clean-skill.md` does). The
  valid annotation was never the defect; the missing agent is.
- **Explicitly NOT claimed:** no behavioral eval was executed — every result
  above is mechanical. **No AEGIS-060 source remediation reached `main`**: the
  strip existed only in draft PR #89 and was reverted additively within it.
- **ID disposition:** AEGIS-060 is retained, never renumbered, never reused,
  and no successor ID is created for it. Its surfaces are **not** defective.

No further new IDs are proposed by this baseline pass. Two observations were
deliberately NOT given IDs (below) because their evidence is incomplete or
their materiality is unconfirmed.

## 2. Systemic observations — no ID assigned (evidence incomplete)

- **Exclusion reciprocity at scale.** Audit rule ROUTE-002 records 311
  one-directional exclusion edges (skill A excludes toward B; B's description
  never names A). Many are legitimate (hub skills cannot name every
  excluder), some are the collision failure mode `skill-quality-reviewer`
  calls the corpus's main one. Needs semantic triage against rubric question
  2 before any ID is assigned. Full edge list: the
  [`artifacts/audits/` route-graph and baseline JSON files at `e2f1da0`](https://github.com/ModernNomad-98/Project-Aegis/tree/e2f1da0beb6e4aed07044ca3a90e841962bfd590/artifacts/audits).
  **Dispositioned by owner decision, 2026-09-26.** The
  [ROUTE-002 dispositions record](../evidence/route002-dispositions-2026-09-26/README.md)
  triages all 268 edges reported on `0f46808`. Three merged batch PRs
  (#394, #395, #396) reciprocated 31 edges into 23 target skills. One of
  those 31 also got a source-side fix. #395 also closed one D64 edge, and the
  owner kept that yield (a dated D64 amendment records it). One other edge is
  an engine false positive. The other 235 are census data, not defects. A
  fresh audit of `56ea7e4` reports 234 ROUTE-002 findings, because #393 also
  closed two census edges; a 2026-09-27 audit of `b553d91` reports 233,
  because #409 closed one more census edge.
  On 2026-09-27, #429 (`169e8be`) fixed the engine false positive (engine
  v1.13.2 matches whole skill names only); an audit of `169e8be` reports 232
  ROUTE-002 findings, all census data.
  No AEGIS ID is assigned.
- **Orchestrator capability numbering.** `project-orchestrator` presents its
  workflow as Capability 1 → 3 → 2 → 4. The sequence matches the declared
  loop (detect → translate → route → record); only the numbering is
  non-sequential. Legibility note for the PR-6 batch, not a behavioral
  defect — a minor wording issue does not earn an ID.

## 3. Dedup map — baseline findings → existing AEGIS-001..059 IDs

| Audit rule | Count | Surfaces | Maps to | Effect on the existing ID |
|---|---:|---|---|---|
| APPR-002 | 1 | `project-orchestrator/references/project-state-template.md:140` — worked example grants `Scope allowed: Build the v1 scope` at brief-approval time | AEGIS-003, AEGIS-008 | **Root cause upgraded to repository-verified**: the template's own example teaches requirements-approval→build-authorization laundering |
| STATE-005 | 2 | same template: `## MVP scope (approved)` (minimum viable product) narrative sections (template + worked example) with no supersession mechanics | AEGIS-002, AEGIS-006 | Confirms the residue left after reconciliation decision D54: append-only contract coexists with narrative sections that cannot be updated append-only |
| ROUTE-003 | 1 | `project-orchestrator/SKILL.md` Stage-2 route (spec → prioritization → commitments; planner absent) | AEGIS-035, AEGIS-045 | **Root cause confirmed on current main** exactly as the handoff recorded |
| VOCAB-002 | 4 | `roadmap-under-uncertainty-planner` description, body ×2, reference sheet — "committed/planned/exploratory", "Now (committed)" | AEGIS-044, AEGIS-039 | **Root cause confirmed on current main**: committed-as-horizon vs commitments-skill's reserved meaning |
| ARTF-001 | 10 | `project-orchestrator`, `human-approval-boundary`, `scoped-approval-register`, `agent-authorization-matrix`, `audit-log-architect`, `agent-containment-reviewer`, `agent-memory-governance`, `offline-first-sync-architect`, `operational-vs-analytical-splitter`, `streaming-event-architect` | AEGIS-056, AEGIS-049 | Corroborates corpus-wide: "durable" claims never name a durability level (semantic-review candidates, not asserted defects) |
| EVAL-004 | 5 | five trigger-evals files (typed `(subagent)` targets) | **AEGIS-060 — REJECTED, false positive** | Baseline count, frozen. All five were **false positives** from EVAL-004 v1.12.0 collapsing the skill and subagent namespaces. The rule now resolves each target in the namespace its syntax declares; with the corpus byte-identical to baseline, live EVAL-004 = 0. The authored files were never defective — see AEGIS-060 above |
| SIDE-004 | 82 | Workflow sections of 64 auto-invocable skills — skill-generation-standard §5 mutation-class candidates (source/test/config writes, version control (VCS), install, network, deploy/provision, data-store writes, doc/state writes) | AEGIS-020, AEGIS-057 | Semantic-review candidates corroborating the §5 posture gap corpus-wide — queued for review, not asserted defects |
| ROUTE-002 | 311 | corpus-wide exclusion edges | none yet | Systemic observation §2; dispositioned by owner decision 2026-09-26 ([record](../evidence/route002-dispositions-2026-09-26/README.md)) |

Rules that fired zero times on the live corpus (SIDE-001..003, APPR-001,
APPR-003, STATE-001..004, VOCAB-003, PARITY-001..002, EVAL-001..003,
ROUTE-001, REF-001..003) are each proven ABLE to fire by fixture
(`scripts/tests/test_audit_skill_contracts.py`, 54 assertions): a zero is a
scanned zero, not an unscanned one.

## 4. Semantic-review coverage record

- **Mechanical audit:** all 184 shipped skills (this baseline).
- **Rubric-guided targeted review** (against
  [semantic-review-rubric.md](semantic-review-rubric.md)): performed for the
  Stage-2 route cluster — `project-orchestrator` and its project-state
  template read in full; `prioritization-frame-picker`,
  `roadmap-under-uncertainty-planner`, `roadmap-to-commitments-translator`,
  and `product-spec-writer` reviewed at contract (description) level — the
  surfaces AEGIS-032..052 name. Its confirmations are the §3 rows. This was
  a targeted pass, NOT a formal per-question worksheet for each skill.
- **No skill outside that cluster has received any semantic review yet** —
  their audit coverage is mechanical-only. Full per-skill worksheet passes
  are scheduled across the remediation batches, cluster by cluster, and get
  recorded here as they land.

## 5. Remediation-batch adjustments recommended by this baseline

The planned PR 2..11 sequence stands. Three adjustments:

1. **PR 3 vs PR 4 both touch `project-state-template.md`.** Keep the
   boundary: PR 3 (approval taxonomy) corrects the Approvals-section worked
   example (APPR-002 → AEGIS-003/-008); PR 4 (event model / append safety)
   restructures the narrative "(approved)" sections (STATE-005 →
   AEGIS-002/-006). Sequence PR 3 before PR 4 so the approval vocabulary the
   state template cites is fixed first.
2. **PR 9 (roadmap ↔ commitments alignment) has its exact surface list**:
   the four VOCAB-002 hits. No scope growth needed.
3. **PR 11 no longer carries AEGIS-060** — the candidate is REJECTED as a
   false positive (above). There is no fixture-hygiene precondition for the
   behavioral-eval pilot: the five files were already correct typed-target
   syntax, and the corrective work landed in the audit rule instead. PR 11
   loses this item and gains no replacement.

ROUTE-002 triage (311 edges) is NOT assigned to a numbered batch yet;
recommend triaging it inside PR 5 (shared vocabulary) discovery, splitting a
dedicated batch only if the confirmed subset is large.
*Superseded 2026-09-26:* the triage ran as its own record, the
[ROUTE-002 dispositions](../evidence/route002-dispositions-2026-09-26/README.md),
with three dedicated reciprocity batches.
