# AEGIS-060+ register — proposed new findings, dedup map, and batch notes

Companion to the frozen AEGIS-001..059 baseline
([Project-Aegis-VolunteerFlow-Defect-Handoff-AEGIS-001-to-059.md](volunteerflow/Project-Aegis-VolunteerFlow-Defect-Handoff-AEGIS-001-to-059.md))
and the corpus contract audit (`scripts/audit-skill-contracts.py`; baseline
run: `docs/audits/skill-contract-audit-baseline.md`, corpus tree
`08727adf8f3e0f54226fa18639c9a50f2562ed22`, 184 skills).

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

- **Classification / severity / status:** Candidate fixture-hygiene defect /
  P2 / **REJECTED CANDIDATE — FALSE POSITIVE CAUSED BY EVAL-004 TYPE COLLAPSE;
  ID RETIRED AND NEVER REUSED**
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
  rows. Every other rule count is unchanged (ARTF-001 10, ROUTE-002 311,
  SIDE-004 82, STATE-001 2, VOCAB-002 4; P0 2, P1 96, info 311). Route graph
  byte-identical. Validator: 184 skills valid, 0 warnings. Audit self-tests:
  **66** assertions pass (57 before, +9 typed-target regressions, including
  parity with `models.parse_target` and a live-corpus assertion that the four
  authored subagent expectations and five annotated overlaps remain intact).
  Validator gate self-tests: 91 assertions pass.
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
  2 before any ID is assigned. Full edge list: `artifacts/audits/`
  route-graph and baseline JSON.
- **Orchestrator capability numbering.** `project-orchestrator` presents its
  workflow as Capability 1 → 3 → 2 → 4. The sequence matches the declared
  loop (detect → translate → route → record); only the numbering is
  non-sequential. Legibility note for the PR-6 batch, not a behavioral
  defect — a minor wording issue does not earn an ID.

## 3. Dedup map — baseline findings → existing AEGIS-001..059 IDs

| Audit rule | Count | Surfaces | Maps to | Effect on the existing ID |
|---|---:|---|---|---|
| APPR-002 | 1 | `project-orchestrator/references/project-state-template.md:140` — worked example grants `Scope allowed: Build the v1 scope` at brief-approval time | AEGIS-003, AEGIS-008 | **Root cause upgraded to repository-verified**: the template's own example teaches requirements-approval→build-authorization laundering |
| STATE-005 | 2 | same template: `## MVP scope (approved)` narrative sections (template + worked example) with no supersession mechanics | AEGIS-002, AEGIS-006 | Confirms the post-D54 residue: append-only contract coexists with narrative sections that cannot be updated append-only |
| ROUTE-003 | 1 | `project-orchestrator/SKILL.md` Stage-2 route (spec → prioritization → commitments; planner absent) | AEGIS-035, AEGIS-045 | **Root cause confirmed on current main** exactly as the handoff recorded |
| VOCAB-002 | 4 | `roadmap-under-uncertainty-planner` description, body ×2, reference sheet — "committed/planned/exploratory", "Now (committed)" | AEGIS-044, AEGIS-039 | **Root cause confirmed on current main**: committed-as-horizon vs commitments-skill's reserved meaning |
| ARTF-001 | 10 | `project-orchestrator`, `human-approval-boundary`, `scoped-approval-register`, `agent-authorization-matrix`, `audit-log-architect`, `agent-containment-reviewer`, `agent-memory-governance`, `offline-first-sync-architect`, `operational-vs-analytical-splitter`, `streaming-event-architect` | AEGIS-056, AEGIS-049 | Corroborates corpus-wide: "durable" claims never name a durability level (semantic-review candidates, not asserted defects) |
| EVAL-004 | 5 | five trigger-evals files (typed `(subagent)` targets) | **AEGIS-060 — REJECTED, false positive** | Baseline count, frozen. All five were **false positives** from EVAL-004 v1.12.0 collapsing the skill and subagent namespaces. The rule now resolves each target in the namespace its syntax declares; with the corpus byte-identical to baseline, live EVAL-004 = 0. The authored files were never defective — see AEGIS-060 above |
| SIDE-004 | 82 | Workflow sections of 64 auto-invocable skills — §5 mutation-class candidates (source/test/config writes, VCS, install, network, deploy/provision, data-store writes, doc/state writes) | AEGIS-020, AEGIS-057 | Semantic-review candidates corroborating the §5 posture gap corpus-wide — queued for review, not asserted defects |
| ROUTE-002 | 311 | corpus-wide exclusion edges | none yet | Systemic observation §2; triage pending |

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
