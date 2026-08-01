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

### AEGIS-060 (candidate) — Trigger-eval neighbor identifiers are annotated prose, not machine-resolvable names

- **Classification / severity / status:** Candidate fixture-hygiene defect / P2 / **Candidate — mechanically evidenced, unremediated**
- **Observed behavior and evidence:** Five trigger-eval files write neighbor
  identifiers as `"<name> (subagent)"` — prose annotation inside the name
  field — so a machine consumer cannot resolve them against disk:
  - `.claude/skills/agent-goal-hijack-defender/evals/trigger-evals.json`
  - `.claude/skills/ai-evaluation-harness/evals/trigger-evals.json`
  - `.claude/skills/ai-threat-modeler/evals/trigger-evals.json`
  - `.claude/skills/prompt-injection-defender/evals/trigger-evals.json`
  - `.claude/skills/release-readiness-reviewer/evals/trigger-evals.json`
  (audit rule EVAL-004; the annotated targets exist as reviewer agents, so
  these are hygiene defects, not stale references.)
- **Expected behavior:** Neighbor fields hold exact on-disk names; agent-vs-
  skill kind belongs in a separate field or note.
- **Why a new ID:** Not covered by AEGIS-001..059 — AEGIS-053 concerns
  non-durable defect-ID references, AEGIS-018 concerns the missing behavioral
  runner. This blocks the AEGIS-018 remediation (a runner cannot match
  annotated names), so it is a distinct, reusable failure mode with named
  surfaces and a clear owner.
- **Likely owner:** Eval fixture conventions (`eval-runner-designer`
  guidance, the five files above).
- **Suggested batch:** PR 11 (test bootstrap / behavioral-eval pilot).
- **Positive regression:** EVAL-004 reports zero findings.
- **Negative regression:** The EVAL-004 fixture case
  (`scripts/tests/fixtures/contract-audit/`) keeps proving the rule fires on
  an annotated name.

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
| EVAL-004 | 5 | five trigger-evals files (annotated neighbor names) | **new: AEGIS-060 (candidate)** | — |
| SIDE-004 | 82 | Workflow sections of 64 auto-invocable skills — §5 mutation-class candidates (source/test/config writes, VCS, install, network, deploy/provision, data-store writes, doc/state writes) | AEGIS-020, AEGIS-057 | Semantic-review candidates corroborating the §5 posture gap corpus-wide — queued for review, not asserted defects |
| ROUTE-002 | 311 | corpus-wide exclusion edges | none yet | Systemic observation §2; triage pending |

Rules that fired zero times on the live corpus (SIDE-001..003, APPR-001,
APPR-003, STATE-001..004, VOCAB-003, PARITY-001..002, EVAL-001..003,
ROUTE-001, REF-001..003) are each proven ABLE to fire by fixture
(`scripts/tests/test_audit_skill_contracts.py`, 46 assertions): a zero is a
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
3. **PR 11 absorbs AEGIS-060 (candidate)** — fixture hygiene is a
   precondition of the behavioral-eval pilot, and the fix is five small,
   mechanically-regressed edits.

ROUTE-002 triage (311 edges) is NOT assigned to a numbered batch yet;
recommend triaging it inside PR 5 (shared vocabulary) discovery, splitting a
dedicated batch only if the confirmed subset is large.
