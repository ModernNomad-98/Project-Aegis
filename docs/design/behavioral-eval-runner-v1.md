# Behavioral Eval Runner v1 — design (specification only)

**Status:** DESIGN / SPECIFICATION ONLY — nothing here is built, wired, or executed.
**Owning skill:** [`eval-runner-designer`](../../.claude/skills/eval-runner-designer/SKILL.md)
(+ [`references/runner-design-blueprint.md`](../../.claude/skills/eval-runner-designer/references/runner-design-blueprint.md)).
**Design baseline (main HEAD):** `e2f1da0beb6e4aed07044ca3a90e841962bfd590`.
**Design branch:** `design/behavioral-eval-runner-v1`.
**Prepared:** 2026-08-07. **Revised:** 2026-08-07 (Phase 2A owner-decision review).

This document specifies how Project Aegis's **structural-only** eval corpus *would* be
executed against live agent behavior, and how the first canonical behavioral suite
(Scenario A) *would* run. It follows the owning skill's Output Format, Validation
Checklist, and Stop Conditions. Per decision **D3** (recorded in
[`docs/skill-generation-standard.md` §6](../skill-generation-standard.md) and in the
generation standard's own words: *"There is no eval runner yet — do not claim evals
'pass,' only that they are present and well-formed"*), the eval convention is validated
**structurally only**. This design does not change that convention; it specifies the
runner that could, once built and run, close the execution half of the gap.

> **Location note.** `docs/design/` is new. `docs/` is organized topically
> (`acceptance/`, `reconciliation/`, `research/`, `roadmaps/`, `prompts/`, `audits/`,
> `paths/`, `skills/`); a design spec is a distinct topical class, so a new
> `docs/design/` subdirectory matches the existing structure rather than overloading
> `research/` (findings) or `acceptance/` (evidence runbooks). No validator or audit
> surface reads `docs/design/` (verified: `scripts/validate-skills.py` inspects skills,
> `docs/paths/`, README markers, `.claude/agents/`, workflows, `CLAUDE.md`;
> `scripts/audit-skill-contracts.py` scans `.claude/skills/` + `docs/skills-catalog.md`
> + `.claude/agents/` + `docs/paths/`), so this file joins no mechanically-governed index.

---

## Owning-skill Output Format block

```
EVAL RUNNER DESIGN — Project Aegis skill library (main @ e2f1da0)
Corpus:         184 shipped skills. 882 evals.json behavior cases + 858 trigger-evals.json
                discrimination cases = 1,740 AUTHORED cases (all single-prompt). Canonical
                end-to-end scenario suites = 1 (Scenario A, multi-turn). EXECUTABLE UNITS per
                full run = 1,740 single-turn + 1 multi-turn suite = 1,741 (Scenario A anchors
                to EXISTING authored cases; nothing double-counted, §3/§11). Case types:
                should_trigger 690 (incl. refusal), should_not_trigger 190, should_not_do 2
                (LEGACY/DIVERGENT refusal outlier). 3 degenerate empty-should_not_trigger cases.
Convention:     structural-only today (decision D3; docs/skill-generation-standard.md §6).
                This design changes no convention and no eval assertion.
Execution:      one FRESH, isolated session per case, full library visible (real selection
                surface); should_trigger ⇒ target activates; refusal ⇒ activates AND refuses;
                should_not_trigger ⇒ named skill silent (record what fired); discrimination ⇒
                expected_skill wins AND every should_not_trigger neighbor silent (pairwise).
                Scenario A is a MULTI-TURN conversation suite (distinct execution mode).
Judging:        deterministic (activation events / required Output-Format block) via code;
                semantic (e.g. "one coherent discovery topic per turn", "refuses the
                shortcut") via a PINNED, independent rubric-guided judge seeing only transcript
                + rubric; judge failure ⇒ JUDGE-ERROR, never PASS/FAIL.
Reporting:      per-case PASS/FAIL/ERROR/JUDGE-ERROR/QUARANTINED/UNRUN (UNRUN default). Six
                states only — ambiguous activation is ERROR + reason_code AMBIGUOUS_ACTIVATION,
                NOT a seventh state. Per-skill rollup; corpus metrics; transcripts external.
Flake policy:   N=3 repeats, quorum 2-of-3 (DECIDED; N configurable; N=5 only for RC/disputed/
                high-risk). Oscillation ⇒ QUARANTINED (dated, always visible). Never retry-
                until-green.
Cost & sampling:cost ≈ sessions×session_cost + judge_calls×judge_cost. HARD guardrails (DECIDED,
                NOT predicted costs): PR ≤$5/run, daily ≤$20, cadence ≤$20/run, full-corpus
                DISABLED by default (owner-authorized + run cap). $-unavailable ⇒ token/call/
                session caps, monetary UNKNOWN, cap reached ⇒ stop, remainder UNRUN. Cadence =
                weekly rotating stratified ~10% of skills.
CI posture:     ADVISORY / NON-BLOCKING first. Structural validator stays the required floor.
                Promotion (DECIDED) needs ≥10 scheduled runs + ≥2 full-corpus baselines + <1%
                ERROR + <1% JUDGE-ERROR + <2% quarantined + flat/shrinking quarantine + spend
                within guardrails + durable human approval.
Gate:           Phase 2B-0 Activation Observability Capability Spike precedes broad behavioral
                execution — prove the real activation signal by EVIDENCE, or record an owner-
                approved limitation on what v1 may claim (§17a, §19).
Decided:        all 10 prior owner decisions now DECIDED (§20).
Deferred (2B-0, EVIDENCE REQUIRED): the activation-observation mechanism + truthful v1 claim
                scope; the exact pinned judge model + calibration; monetary-cost observability
                vs token/call/session proxy.
Non-claims:     No runner exists as of this design. No eval case has been executed. Nothing
                here is an eval result. Manual live Scenario A acceptance already exists (two
                accepted runs); no GENERAL AUTOMATED behavioral runner exists yet.
```

---

## 1. Executive summary

Project Aegis ships **184 skills** carrying **882 behavior-eval cases** and **858
trigger-discrimination cases** — **1,740 authored cases** — but by decision **D3** the
`scripts/validate-skills.py` gate only proves each eval file **exists and parses**.
Nothing exercises the cases against a live model, so no one may claim any eval
"passes." The repository is explicit and self-consistent about this: even the
static contract auditor states of itself, *"Not a behavioral eval runner … no
behavioral eval is executed or reported by this tool. Structural validity is never
behavioral proof"* ([`scripts/audit-skill-contracts.py`](../../scripts/audit-skill-contracts.py)).

This document specifies — **without building** — a behavioral eval runner that would
exercise the corpus as written: one fresh isolated session per case, the full skill
library visible so the real selection surface is reproduced, deterministic activation
observation plus a pinned, independent rubric-guided judge for semantic assertions,
repeats-with-quorum for stochastic routing, honest `UNRUN` accounting under hard spend
guardrails, three cost tiers (PR / cadence / full), and an **advisory-first** CI posture
that never replaces the structural validator. Across a full run the executable units are
**1,741** — the 1,740 single-turn authored cases plus **one** canonical multi-turn suite
(Scenario A), which is anchored to existing cases and adds no new authored case (§3, §11).

It also designs **Scenario A** — the beginner `project-orchestrator` flow — as the first
end-to-end **behavioral** suite, automating the currently-manual fresh-session
acceptance (Control I of
[`docs/acceptance/scenario-a-runbook.md`](../acceptance/scenario-a-runbook.md)) while
**complementing, never replacing**, the existing mechanical evidence harness
(`scripts/acceptance/Invoke-ScenarioAEvidence.ps1` /
`Test-ScenarioAEvidence.ps1`). The design encodes the PR #77 lesson: the accepted
Scenario A rule is **one coherent discovery topic per turn** (supporting details within
that topic allowed) — a semantic property that a keyword/`?`/`and`-counting rule would
mis-fail, so the corpus's own semantic atomicity test is used instead.

A hard **implementation gate — Phase 2B-0, the Activation Observability Capability Spike
(§17a, §19)** — precedes broad runner construction: the project must prove, by evidence
rather than assumption, what activation signal Claude Code actually exposes (or record an
explicit owner-approved limitation on what v1 may truthfully claim) before executing the
general corpus. Implementation is a **separate, separately-approved** task. This is the spec.

## 2. Current-state gap

| Layer | Exists today? | What it proves | What it does NOT prove |
| --- | --- | --- | --- |
| `scripts/validate-skills.py` (required CI gate) | Yes | Each `evals.json`/`trigger-evals.json` **exists and parses**; structure/order/counts/portability of SKILL.md | That any case, run against a model, produces the expected behavior |
| `scripts/audit-skill-contracts.py` (read-only, not a gate) | Yes | Static contract-rot findings across skill text | Same — it explicitly disclaims being a behavioral runner |
| Scenario A mechanical harness (`Invoke-/Test-ScenarioAEvidence.ps1`) | Yes | Append-only/manifest/containment properties of **fixture** `project-state.md` sequences, deterministically | That a live agent, driven through Scenario A, actually behaves that way |
| Manual fresh-session Scenario A rerun (runbook Control I) | Yes (2 accepted runs) | The live agent behaved correctly **in those two runs** | Repeatability, drift detection, or coverage beyond Scenario A |
| **General automated behavioral eval runner** | **No** | — | — |

The gap this design targets: **no general automated runner exercises the 1,740 authored
cases against live behavior.** The structural floor is real and stays; the behavioral
ceiling is unbuilt.

## 3. Repository / eval-corpus census (deterministic)

Produced by a read-only census over `.claude/skills/*/evals/*.json` at baseline
`e2f1da0` (script and JSON output retained under `C:\temp`, outside every repo; not
committed). The census is **evidence for the design, not an eval result**.

| Metric | Value |
| --- | --- |
| Shipped skills (excl. `_template`) | **184** |
| Skills shipping `evals.json` | 184 (100%) |
| Total `evals.json` behavior cases | **882** |
| Skills shipping `trigger-evals.json` | 181 |
| Total `trigger-evals.json` discrimination cases | **858** |
| Distinct `evals.json` case types | `should_trigger`, `should_not_trigger`, **`should_not_do`** |
| `type` distribution | should_trigger 690 · should_not_trigger 190 · should_not_do 2 |
| `expect.triggers` distribution | true 692 · false 190 |
| Refusal-style should_trigger cases (heuristic: fire + refuse-shaped assertion) | ~268 |
| Eval assertions total / min / max / avg per case | 2,834 / 1 / 6 / 3.21 |
| Discrimination cases with `expected_skill` | 858 (100%) |
| `should_not_trigger` list size per discrimination case | 1→660 · 2→136 · 3→57 · 4→2 · **0→3** |
| `trigger-evals.json` with `overlaps_with` | 181 (100%) |
| Structural/parse outliers | **0** (validator guarantees parse) |

**Authored cases vs executable units (arithmetic reconciliation).** The two figures the
owner flagged (1,740 vs 1,741) are different quantities; both are correct once named:

- **Authored corpus cases = 882 (`evals.json`) + 858 (`trigger-evals.json`) = 1,740** —
  each is a **single-prompt** case.
- **Canonical end-to-end scenario suites = 1** (Scenario A, §9) — a **multi-turn**
  conversation script whose per-turn assertions are **anchored to** a subset of the
  already-counted `project-orchestrator` authored cases. It adds **no** new authored case,
  and its anchoring cases are **not** re-counted.
- **Executable units per full run = 1,740 single-turn + 1 multi-turn suite = 1,741.** The
  §11 cost formula counts **executable units**; the one scenario suite is a single, heavier
  **multi-turn session** per repeat — *not* a duplicate of its anchoring cases (which run
  as their own single-turn units). The earlier bare "1,741 × N" is corrected to a split
  formula in §11 so nothing is double-counted and the count is unambiguous.

**Most-contested discrimination neighbors** (top `should_not_trigger` targets — where
single-shot routing results mislead most, so repeats-with-quorum matters most):
`api-event-architect` (23), `observability-operator` (18), `authorization-matrix-designer`
(17), `multi-tenant-data-architect` (15), `agent-governance-audit` (13), `code-reviewer`
(13), `streaming-event-architect` (12), `slo-reliability-architect` (12).

**Outliers — recorded, NOT silently normalized** (per the owning skill: divergences are
findings for authors, not things the runner quietly rewrites):

1. **`should_not_do` type — 2 cases**, both in
   [`superadmin-observability-console-designer/evals/evals.json`](../../.claude/skills/superadmin-observability-console-designer/evals/evals.json)
   (`refusal-admin-write-access-to-metrics`, `refusal-content-reveal-without-incident`),
   both `triggers: true`. Semantically these are **refusal cases** (skill activates AND
   refuses the unsafe action) but they use a `type` label outside the library's
   "refusal-as-`should_trigger`" convention. **Runner treatment (owner-decided, §20 D8):**
   support them explicitly in v1 as a **LEGACY / DIVERGENT REFUSAL CASE TYPE** — execute
   with refusal-case semantics (activate AND refuse) and **emit an author-facing
   schema/corpus warning** that the `type` label diverges (feeds `skill-quality-reviewer`
   check 4). The runner does not silently rewrite or auto-normalize them; v1 is not blocked
   on retyping; any normalization is a separate future scoped change.
2. **Empty `should_not_trigger` — 3 discrimination cases**
   (`release-readiness-reviewer/delegated-review-composes-subagent`,
   `skill-quality-reviewer/whole-skill-adding-pr-is-the-library-diff-reviewer-seam`,
   `source-of-truth-reconciler/security-conflict-still-triggers-then-routes`). Pairwise
   scoring degenerates (no neighbor whose silence to check). **Runner treatment:** score as
   a **positive-activation-only** assertion (expected_skill must win; no silence check);
   record the degeneracy as a finding.
3. **Non-bare `expected_skill` token.** `release-readiness-reviewer (subagent)` carries a
   parenthetical. **Runner treatment:** the activation matcher parses the leading skill
   name and records the annotation as metadata; it never string-equals the whole token
   against a skill name.

These three are the only shape variances in the corpus; everything else conforms to the
blueprint's case-type table.

## 4. Requirements

**Functional.** (F1) Execute every corpus case type discovered in §3 with defined
semantics. (F2) Reproduce the **real** skill-selection surface — all 184 descriptions
visible, real matching — never a mock router. (F3) One fresh isolated session per case.
(F4) Observe skill activation from machine evidence, not model prose alone — and only on a
mechanism proven by Phase 2B-0 (§17a). (F5) Deterministic assertions graded by code;
semantic assertions by an independent judge. (F6) Repeats-with-quorum for stochastic cases.
(F7) Multi-turn conversation suites (Scenario A). (F8) Versioned machine-readable report
with `UNRUN` as the default state and exactly six top-level states. (F9) Hard spend
guardrails + kill switch with honest `UNRUN` remainder. (F10) Three execution tiers.

**Non-functional.** (N1) Containment-first (§15): the runner executes an agent, so its
blast radius must be bounded. (N2) Advisory-first CI; structural validator stays required.
(N3) Determinism where possible: graders, report ordering, and evidence layout are
reproducible; only the model calls are stochastic, and that stochasticity is measured, not
hidden. (N4) Honesty invariants: errors never become pass/fail; quarantine is always
visible; no retry-until-green; no auto-pruning. (N5) Host-honest: no fabricated API/event
stream — the activation mechanism is whatever Phase 2B-0 proves real (§6, §17a).

## 5. Case execution semantics

One case = one **fresh** session. No case inherits another's context; no session that has
already routed a prompt is reused (the most expensive and least negotiable rule — a prior
skill load is context that biases every later case).

| Case type (as found) | Session setup | PASS condition | Notes |
| --- | --- | --- | --- |
| `should_trigger` (`triggers: true`) | Fresh session, full library visible, prompt verbatim | Target skill **activates** (§6) | Repeats-with-quorum (§10) |
| Refusal case (typed `should_trigger`, `triggers: true`) | Same | Target **activates** AND response satisfies the refusal assertions | Two-part; report each part separately |
| `should_not_do` (2 outliers, §3; legacy/divergent refusal) | Same | Same as refusal (activate AND refuse) | + author-facing warning re: divergent `type` label |
| `should_not_trigger` (`triggers: false`) | Same | Named skill **does NOT activate** | Record what fired instead — routing telemetry, not a verdict |
| Discrimination case (trigger-evals) | Same | `expected_skill` **activates** AND every `should_not_trigger` neighbor **silent** | Scored **pairwise**; partial wins reported as partial |
| Discrimination, empty `should_not_trigger` (3 outliers, §3) | Same | `expected_skill` activates (no silence check) | Degenerate pairwise; finding emitted |
| **Conversation suite** (Scenario A, §9) | Fresh session; scripted ordered user turns | Per-turn deterministic + semantic assertions all hold; end-state gates hold | Distinct multi-turn mode; not in the single-prompt corpus |

**Isolation, explicit vs model-selected.** Trigger/discrimination cases test **model-
selected** activation: the runner presents the prompt and the model chooses. The runner
MUST NOT pre-invoke the skill (e.g. type `/skill-name`) to satisfy a `should_trigger`
case — that tests the harness, not the router. Explicit invocation is a separate signal,
used only where a case's own text is about explicit invocation.

**Errors are not verdicts.** Infrastructure/runtime failures (session spawn failure,
transport error, timeout of the *session*, container fault) yield `ERROR`, never `PASS`/
`FAIL`. **Ambiguous activation** (§6) also yields `ERROR` (with `reason_code:
AMBIGUOUS_ACTIVATION`). Judge failures yield `JUDGE-ERROR` (§8). Budget exhaustion yields
`UNRUN` (§11).

## 6. Activation observability

Determining **what skill actually activated** is the central hard problem, and the reason
Phase 2B-0 (§17a, §19) exists as a gate. Model-visible prose such as
`→ invokes requirements-gathering-facilitator` is a **model-generated claim** — indeed
`project-orchestrator`'s own evals *require* the orchestrator to print that exact line — so
the prose proves the model *said* it would route, not that the skill's instructions
actually loaded. The design therefore ranks evidence and is explicit that the mechanism
must be **proven on the real host before broad execution**, never assumed.

**Evidence tiers.**

- **Tier 1 — structured activation event (preferred, deterministic).** The execution
  adapter captures the session's tool-use / event stream (the Claude Agent SDK surfaces
  assistant messages and `tool_use` blocks). A skill activation appears as a `Skill`
  tool-use naming the skill, and/or a load/read of
  `.claude/skills/<name>/SKILL.md` into context. Either is machine evidence of activation.
  **Whether a given Claude Code build actually emits such a signal is exactly what Phase
  2B-0 determines — it is not assumed here.**
- **Tier 2 — output-signature fallback (deterministic, weaker).** Many skills mandate a
  characteristic **Output Format block** (e.g. `project-orchestrator`'s `RECORDING STATUS`
  / `STAGE-2 OWNERS` / `EXIT GATE` block; a review skill's severity-ranked findings block).
  When the host does not emit a discrete skill-load event, presence of the skill's required
  block is a corroborating deterministic signal.
- **Tier 3 — model routing prose (secondary, a claim).** `→ invokes X` and similar. Used
  only to **corroborate** Tier 1/2, **never** as sole proof — this is stated as a Phase
  2B-0 constraint too.

**Ambiguous activation ⇒ `ERROR` (`reason_code: AMBIGUOUS_ACTIVATION`).** If the activation
signals **conflict or are insufficient** (e.g. Tier-3 prose claims activation but no Tier-1
event and no Tier-2 signature corroborates it, or two signals disagree), the case is
**`ERROR`** with **`reason_code: AMBIGUOUS_ACTIVATION`** — **not** a seventh top-level
state. It is **never** mapped to PASS or FAIL, for either `should_trigger` or
`should_not_trigger`. The evidence record MUST still capture: **every activation signal
observed**, **which evidence tier produced each signal**, and **why they conflict or are
insufficient**. Ambiguous-activation `ERROR`s feed the flake window (§10) and raise an
**observability finding** (improve the adapter or the skill's output signature).

**False-positive prevention.** Merely **naming** a skill in prose ("you could use
`code-reviewer`") is NOT activation. Activation requires a Tier-1 event or a Tier-2 output
signature — not a name mention, not a recommendation, not a routing plan the model did not
execute.

**Nested / composed activation.** Represented as an ordered **activation tree** (parent →
children), each node carrying its own evidence tier. Example: `project-orchestrator`
composing `requirements-gathering-facilitator` records two activations; Scenario A
assertions check the composition, not just the root.

**Multiple activations.** Recorded as an ordered multiset. Discrimination scoring checks
`expected_skill ∈ activations` AND `should_not_trigger ∩ activations = ∅`.

**Host-honesty caveat (no fabricated stream).** Whether a specific Claude Code / SDK build
emits a *discrete* "skill activated" event is **version-dependent and a verification item**,
not an assumption. The Claude Agent SDK's message/tool-use stream is real and is the
intended Tier-1 source; but if a target host exposes only prose, this design does **not**
pretend otherwise — it falls back to Tier-2 signatures plus an explicit confidence level,
and records `ERROR` / `reason_code: AMBIGUOUS_ACTIVATION` rather than inventing certainty.

**Implementation gate (Phase 2B-0).** This entire §6 mechanism is a **hypothesis until
proven on the real host**. Before any broad general-corpus behavioral execution, the
**Activation Observability Capability Spike (Phase 2B-0, §17a/§19)** must establish — by
evidence, not assumption — which activation signal Claude Code actually exposes, or produce
an explicit **owner-approved limitation** on exactly what v1 may claim. No Claude Code API,
event stream, hook, or telemetry source is assumed to exist; the runner is built only on
what 2B-0 establishes.

## 7. Deterministic grading

Graded by code, no model in the loop:

- **Activation / non-activation** — from §6 evidence (Tier 1, or Tier 2 signature), on the
  mechanism Phase 2B-0 proved real.
- **Discrimination pairwise** — expected fired AND each neighbor silent.
- **Artifact/really-happened checks** — required Output-Format header/block present;
  a prohibited side effect did or did not occur. For Scenario A the strongest of these
  reuse the mechanical harness's oracles: **0 commits** in the disposable repo
  (`Test-ZeroCommitCount` fail-closed logic), **untracked-only** `project-state.md`,
  **append-only** immutable rows (`Test-AppendOnly`), **manifest/artifact digest** match
  (`Test-ManifestStep` / `Test-SpecArtifact`), and **no forbidden `SS-003`**.
- **Absence-of-mutation checks** — no network egress, no package install, no git mutation,
  no deploy/migration occurred (verified from the contained sandbox, §15, not from the
  model's say-so).

Deterministic results carry an evidence pointer (event id, matched header, or oracle
output). They are reproducible given the same transcript.

## 8. Semantic judging

For assertions that are qualitative ("refuses the shortcut", "names the colliding skill",
**"one coherent discovery topic per turn"**), an independent rubric-guided judge is used.

**Rubric derivation.** Each assertion is classified once, up front, into
**deterministic** (→ §7 code), **semantic** (→ judge, rubric = the assertion text turned
into a checkable question), or **unjudgeable-as-written** ("handles it well"). The
unjudgeable set is a **deliverable** (a census fed to `skill-quality-reviewer`), not a
silent pass. With avg 3.21 assertions/case over 882 behavior cases, this classification is
sized per-assertion and cached by assertion hash. The **human approval owner for this
classification is Peter Nguyen** (§20 D9); `skill-quality-reviewer` may advise but is not
the approval authority.

**Judge configuration + independence (hard rules; §20 D1).**

- Semantic judging uses a **separately configured, pinned judge identifier**; the exact
  initial judge is **selected and calibration-tested during Phase 2B-0** (§17a). No specific
  current model name is hard-coded in this design.
- The judge is a **separate call** seeing ONLY: the case (prompt + rubric) and the
  transcript/evidence required for that judgment.
- The judge session is **independent** of the system-under-test session; it does **NOT**
  receive the tested session's private reasoning / chain-of-thought, does **NOT** share or
  run inside the tested session, and does **NOT** see unrelated expected-answer material
  beyond the rubric.
- **Changing the judge model/version after behavioral baselining requires behavioral
  re-baselining**, recorded as such.
- Judge failure — malformed verdict, refusal, timeout, transport error — ⇒ **`JUDGE-ERROR`**,
  counted separately, **never** mapped to case PASS or FAIL.

**Scenario A semantic anchor (the PR #77 lesson).** The accepted rule is exactly:

> **ONE COHERENT DISCOVERY TOPIC PER TURN.**
> **Related supporting details within that topic are allowed.**

A brittle keyword / `?` / `and`-counting rule would **wrongly fail** legitimately coherent
turns such as *"Who manages appointments today — just you, or is there also a receptionist
and/or several therapists involved?"* (one topic: current appointment-management
participants) or *"Walk me through how a single appointment gets booked today, including
who handles each step and where the information is recorded."* (one topic: the current
booking workflow). The corpus **already** frames this semantically: `project-orchestrator`'s
ATOMIC-QUESTION GATE uses *"could one requested part be answered while another remains
unanswered?"* — explicitly *"rather than question-mark or 'and' counting"* — and ships an
**anti-overcorrection** case
(`regression-one-process-walkthrough-is-one-valid-target`) proving a single process
walkthrough that narrates several steps is ONE valid target. The judge rubric **reuses that
exact semantic test.** This assertion class is **explicitly semantic**: a regex cannot
reliably judge conversational coherence, and the design says so plainly.

**Judge rubric — coherent-topic (illustrative).** PASS when: exactly one coherent
discovery topic is advanced; any supporting details are subordinate to that topic; no
independent second topic and no unrelated decision/request is bundled. FAIL when:
a questionnaire dump; ≥2 unrelated discovery topics in one turn; "answer these in any
order"; or multiple independent product decisions bundled. The judge returns a structured
verdict (pass/fail + which failure mode + the offending span), enabling a deterministic
outer check of the verdict's shape (a malformed verdict ⇒ `JUDGE-ERROR`).

## 9. Scenario A behavioral suite (first canonical suite)

Scenario A is designed as the first **multi-turn** behavioral suite: a scripted sequence
of beginner user turns driving a **fresh** `project-orchestrator` session from cold start to
the start of design, with per-turn deterministic + semantic assertions and end-state gates.
It **automates the runbook's Control I** (currently a manual fresh-session rerun) and
**complements, never replaces**, the mechanical evidence harness. As one **executable unit**
it is a single multi-turn session per repeat (§3, §11); its assertions are anchored to
existing authored cases and add no new authored case.

**Two harnesses, complementary (must stay distinct).**

| | Mechanical evidence harness (exists) | Behavioral runner (this design) |
| --- | --- | --- |
| Input | Pre-authored **fixture** `project-state.md` sequence + manifest | A live **fresh agent session** driven by a conversation script |
| Proves | Append-only / manifest / artifact-digest / containment / 0-commit properties of the fixtures, deterministically | The live agent actually *behaves* — routes, asks one coherent topic/turn, previews-before-create, refuses unauthorized action |
| Nature | Deterministic replay; no model call | Stochastic live behavior; repeats-with-quorum |
| Files | `scripts/acceptance/Invoke-/Test-ScenarioAEvidence.ps1` | New runner (§14); **does not modify or replace the PS1 harness** |

The behavioral runner **reuses the mechanical harness's oracles** on any `project-state.md`
the live agent actually writes (append-only, manifest, 0-commit), but the *behavioral*
judgments (coherent topic, routing evidence, refusal) are its own.

**Coverage — required controls A–Q mapped to existing corpus cases** (all in
[`project-orchestrator/evals/evals.json`](../../.claude/skills/project-orchestrator/evals/evals.json)
unless noted):

| # | Control | Grading | Anchoring corpus case(s) |
| --- | --- | --- | --- |
| A | Workspace-role recognition (consumer vs source library) | Semantic + deterministic (landmark checks) | `edge-consumer-repo-not-skills-library`; `regression-fresh-consumer-with-copied-aegis-files-stays-product`; `regression-actual-project-aegis-source-landmarks-remain-library` |
| B | Fresh Stage 0 identification | Deterministic (no state file / no code) + semantic | `positive-cold-vague-idea`; `regression-fresh-consumer-…` |
| C | Stays in current consumer/product repo (no sibling redirect) | Semantic | `regression-fresh-consumer-…` |
| D | COMPLETE project-state preview **before** creation (byte-for-byte, no ellipsis) | Deterministic (preview vs created bytes) + semantic | `positive-cold-vague-idea`; `edge-exact-preview-is-byte-for-byte-no-ellipsis` |
| E | Explicit approval **before** creation (decline/ambiguous ⇒ nothing) | Deterministic (no file until yes) | `positive-cold-vague-idea` |
| F | Requirements-facilitator routing/invocation evidence (exact name / `→ invokes …`) | §6 activation (Tier 1 preferred; prose corroborates) | `regression-clinic-stage1-handoff-one-question`; `positive-cold-vague-idea` |
| G | **One coherent discovery topic per turn** | **Semantic** (atomicity rubric, §8) | `regression-clinic-stage1-handoff-one-question`; `regression-clinic-stage1-many-areas-one-question`; `regression-clinic-observed-compound-question-is-rejected`; `regression-orchestrator-atomic-gate-rewrites-delegated-candidate`; `regression-one-process-walkthrough-is-one-valid-target` |
| H | No questionnaire dump | Semantic + deterministic (no numbered bank emitted) | `regression-clinic-stage1-many-areas-one-question` |
| I | No unrelated-topic bundling | Semantic | atomic-gate cases above |
| J | No unauthorized implementation | Deterministic (no source edits) + semantic | `should-not-treat-scope-acceptance-as-build-authority`; `regression-fresh-consumer-…` |
| K | No package installation | Deterministic (sandbox, §15) | `should-not-treat-scope-acceptance-as-build-authority` |
| L | No network/API action | Deterministic (sandbox egress = none) | `regression-fresh-consumer-…` |
| M | No Git mutation | Deterministic (`Test-ZeroCommitCount`; untracked-only) | `should-not-auto-merge-or-apply-migration` |
| N | No deployment/migration action | Deterministic + semantic | `should-not-auto-merge-or-apply-migration`; `should-not-batch-high-risk-actions` |
| O | Correct recording boundary (append-only; preview→approve→append; placeholders preserved) | Deterministic (`Test-AppendOnly`) + semantic | `edge-immutable-history-is-append-only-placeholder-preserved`; `should-not-treat-business-answer-as-write-approval`; `edge-no-recording-operation-this-turn` |
| P | Evidence/transcript capture | Runner-provided (external evidence dir) | — |
| Q | Model/runtime/session metadata capture | Runner-provided (report schema, §13) | — |

Scenario A runs as **one fresh session per repeat** (N repeats, §10); each turn's
assertions are graded as the conversation proceeds; the run fails if any required control
fails at quorum. The suite is the runner's own first self-proof once built (Phase 2B-4, §19).

## 10. Flake / repetition / quarantine policy (DECIDED)

Live routing is **stochastic**: a single clean win proves little; a single miss proves
less. The unit of evidence is **repeats-with-quorum**.

**Sizing for Aegis (owner-decided, §20 D2).** The runnable single-turn set is **1,740**
cases (882 behavior + 858 discrimination); with the one multi-turn Scenario A suite the
executable units are **1,741** (§3). At `N` repeats a full run is `1,741 × N` executable-
unit sessions plus judge calls. **v1 is fixed at `N=3` with quorum `2-of-3`**: it
distinguishes stable from flaky at materially lower cost than `N=5`, and the cadence/PR
tiers (§12) keep routine spend bounded. **`N` is configurable**; **`N=5` (or higher) is
used only for explicitly configured** release-candidate, disputed, or high-risk cases.

| Parameter | v1 (DECIDED) | Rationale |
| --- | --- | --- |
| `N_repeats` (trigger/discrimination/conversation) | **3** (configurable) | Quorum without `N=5` cost at ~1,741-unit scale |
| Quorum | **2 of 3** (`k > N/2`) | Majority; report `wins/N`, not just the verdict |
| Escalated `N` | **5+** only for explicitly configured RC / disputed / high-risk cases | Never a default; never retry-until-green |
| Instability | quorum verdict **flips ≥2×** in the rolling window of the last **5** scheduled runs | Oscillation, not a single miss |
| Quarantine | unstable case ⇒ `QUARANTINED` with a **dated reason**; still **runs** (to gather data) but is **excluded from pass/fail gates**, **never from the report** | Visibility is the point |
| Un-quarantine | stable across the next **3** scheduled runs ⇒ eligible to leave quarantine (recorded) | Symmetric, evidence-based |

**Forbidden (result laundering, all rejected):** auto-retry-until-green; auto-pruning
failing cases; excluding quarantined cases from the report; silently raising thresholds to
turn a FAIL green.

**State set (exactly six; distinct, never conflated):** `PASS` · `FAIL` · `ERROR`
(infra/runtime **and** ambiguous activation via `reason_code: AMBIGUOUS_ACTIVATION`) ·
`JUDGE-ERROR` (judge failed) · `QUARANTINED` (unstable) · `UNRUN` (never executed —
default, budget-capped, or not selected this tier). **Ambiguous activation is not a
seventh state** — it is `ERROR` with a reason code (§6), and like every `ERROR` never
counts as PASS or FAIL.

## 11. Cost / budget controls (DECIDED guardrails)

**Cost model (blueprint arithmetic, real counts, split to avoid double-counting):**

```
authored_corpus_cases     = 882 (evals.json) + 858 (trigger-evals.json) = 1,740   # single-prompt
canonical_scenario_suites = 1  (Scenario A; multi-turn; anchored to EXISTING cases, NOT re-counted)
executable_units          = 1,740 + 1 = 1,741

sessions    = single_turn_sessions + suite_sessions
            = 1,740 × N            +  1 × N        # the suite is ONE multi-turn (heavier) session/repeat
            = 1,741 × N            ⇒  N=3: 5,223 executable-unit sessions
judge_calls = semantic_assertions_exercised × N   # up-front classification output (§8), not assumed here
cost        ≈ sessions × session_cost + judge_calls × judge_cost
```

`session_cost` and `judge_cost` depend on the chosen model(s), tokens, and tool-turns per
case; the multi-turn suite session is heavier than a single-turn session and is metered
distinctly. Session/model calls and judge calls are **separate line items** in the report
(§13).

**Owner-ratified HARD CEILINGS (DECIDED — guardrails, NOT predicted run costs; §20 D3):**

| Tier | Hard ceiling |
| --- | --- |
| PR tier | **≤ $5 per run** |
| Daily behavioral-eval total (all tiers) | **≤ $20** |
| Cadence tier | **≤ $20 per run** |
| Full-corpus tier | **DISABLED BY DEFAULT** — requires explicit owner authorization AND a specific run-level spend cap |

These are **hard stops, not forecasts**. **Kill switch:** on ceiling breach or manual
trigger, the runner **stops launching sessions** and marks every not-yet-run case
**`UNRUN`** — **never** a silent partial report that looks complete; a capped run states,
prominently, coverage vs cap and the `UNRUN` count.

**When the execution/provider surface cannot reliably expose monetary cost** (a real
possibility, resolved by evidence in Phase 2B-0): the runner does **not** fabricate a dollar
figure. It **enforces the available token / call / session ceilings**, reports monetary
spend as **`UNKNOWN`** where appropriate, **stops launching** new cases when the enforceable
cap is reached, and marks the remainder **`UNRUN`**. Budget-guardrail patterns compose
[`ai-cost-guardrail-designer`](../../.claude/skills/ai-cost-guardrail-designer/SKILL.md)
if the runner is adopted.

## 12. PR / cadence / full tiers (DECIDED)

| Tier | Scope | When | Purpose |
| --- | --- | --- | --- |
| **PR tier** | Cases of skills **changed in the PR** (diff touches `.claude/skills/<name>/`) + their named `overlaps_with` / `should_not_trigger` neighbors + **required regression suites** tied to the change (e.g. any change to `project-orchestrator` or a Scenario-A-touching skill ⇒ run the **Scenario A** behavioral suite) | Per PR, **advisory** lane; **≤ $5/run** | Catch regressions where they were edited |
| **Cadence tier** | A **weekly rotating, stratified** sample of **~10% of shipped skills** per run — stratified to **span families** (never clustering in one), **including the named overlap/discrimination neighbors** required by selected cases, rotating **deterministically** so the **entire shipped corpus** is eventually covered; each run **reports its rotation coverage** | Weekly (scheduled); **≤ $20/run** | Drift detection in **untouched** skills at bounded cost |
| **Full tier** | Entire corpus, required repeats, required judges | **DISABLED BY DEFAULT**: only on **explicit owner authorization + a run-level spend cap** — runner-architecture changes, judge swaps, eval-convention changes, release-candidate baseline | Re-baseline |

The PR tier's "changed skills" set is computed from the PR diff; its regression triggers are
declared in the case manifest (§14), not hard-coded. Cadence sampling parameters are
owner-decided (§20 D4); the full tier is owner-gated (§11).

## 13. Evidence / result schema (versioned, machine-readable)

Every report carries `schema_version` and `runner_version`. Raw transcripts are stored as
evidence in an **external** directory (like the Scenario A harness) and are **never
auto-committed** (§20 D6): the runner does not commit raw transcripts; only deliberately
curated, sanitized, synthetic regression fixtures may later be added to Git via normal
reviewed changes. Preserve-on-failure external evidence is retained.

**Per case:**

```
schema_version, runner_version
case_id, skill, case_type            # incl. should_not_do (legacy-refusal) / degenerate-discrimination flags
repo_sha, skill_corpus_tree_id       # corpus content hash (identity of what was exercised)
model_id (as available), host_tool_version (as available)
tier                                 # pr | cadence | full
timestamp
fresh_session_ref                    # id/handle of the isolated session
repetition_number, repeats_run, wins # e.g. 2 of 3
expected_activation
observed_activation(s)               # activation tree/multiset + evidence tier per node
what_fired_instead                   # should_not_trigger / discrimination losses
deterministic_results[]              # {assertion, pass, evidence_ref}
semantic_results[]                   # {assertion, verdict, judge_id, JUDGE-ERROR?, evidence_ref}
state                                # PASS | FAIL | ERROR | JUDGE-ERROR | QUARANTINED | UNRUN
reason_code                          # e.g. AMBIGUOUS_ACTIVATION (on ERROR); BUDGET_CAP (on UNRUN); ...
reason
transcript_ref                       # external evidence pointer
cost_meta                            # {session_tokens, judge_tokens, session_calls, judge_calls,
                                     #  monetary_spend | UNKNOWN}
duration_meta                        # latency, if available
```

**Per skill:** totals by state; trigger accuracy (quorum wins / trigger cases run);
discrimination record (pairwise wins/losses, with `what_fired_instead`); refusal
compliance.

**Corpus:** run coverage (run vs `UNRUN`); spend vs cap (monetary, or `UNKNOWN` with
token/call/session totals); judge-error rate; **ambiguous-activation `ERROR` rate
(`reason_code: AMBIGUOUS_ACTIVATION`)**; quarantine inventory (with dated reasons); cases
flagged **unjudgeable-as-written**; overall **advisory** summary (never a pass/fail gate
verdict).

`UNRUN` is the **default state of every case in every report**; a case acquires another
state only from an actual execution in the reported run — the report shape itself preserves
the no-runner-yet honesty.

## 14. Runner architecture (future implementation — designed, NOT built)

Proposed layout (illustrative; a build task decides final names):

```
tools/behavioral-eval-runner/
  runner.(entrypoint)                 # orchestrates: select → run → observe → grade → judge → report
  manifest/
    cases.(schema)                    # case selection + tier rules + regression triggers
    conversation-suites/scenario-a.(script)   # ordered user turns + per-turn assertions
  adapters/
    host-adapter.iface                # abstract execution host (spawn fresh session, stream events)
    claude-code-adapter.*             # FIRST supported adapter (Claude Code / Claude Agent SDK)
  observe/activation-observer.*       # §6 tiers; mechanism as PROVEN by Phase 2B-0; ambiguity ⇒ ERROR
  grade/deterministic-grader.*        # §7; reuses Scenario A oracles for project-state
  judge/semantic-judge.*              # §8 pinned independent judge; JUDGE-ERROR handling
  evidence/evidence-writer.*          # external, contained, preserve-on-failure, never auto-commit
  report/report-generator.*          # §13 schema; UNRUN default; six states + reason_code
  guard/cost-guard.*                  # §11 hard ceilings + kill switch (monetary or token/call/session)
  flake/flake-controller.*           # §10 repeats/quorum/quarantine
  tests/                             # runner self-tests (§18)
```

**Interfaces (boundaries, not implementations).**

- **Host adapter** — `spawn_fresh_session(prompt|script) → session handle`,
  `stream_events(session) → event stream`, `capability_report()` (does this host emit
  Tier-1 activation events? deny-by-default on unknown). **Claude Code / Claude Agent SDK is
  the first supported adapter** (§20 D7) because that is the repository's reference surface
  (`docs/skill-generation-standard.md`: "Claude Code is the reference surface"). The adapter
  boundary keeps Aegis from being permanently tied to one vendor **without pretending
  cross-provider parity exists** — a second adapter is added only when a real host
  demonstrably satisfies the same activation-observation contract (§6). No parity is claimed
  for any unimplemented adapter (§21).
- **Activation observer** — consumes the event stream, emits an activation tree with a
  confidence tier per node (§6); its concrete mechanism is whatever **Phase 2B-0** proves.
- **Deterministic grader** — pure functions over transcript + sandbox state (§7).
- **Semantic judge** — pinned, independent call, rubric-only input, structured verdict (§8).
- **Evidence writer / report generator / cost guard / flake controller** — as above.

## 15. Containment / security model

Because a behavioral eval **executes an agent**, the runner is **containment-first**, and it
**reuses the Scenario A harness's proven safety semantics** rather than reinventing them.

- **Disposable workspace per case.** A throwaway git repo + evidence dir under system temp,
  **outside** any Aegis/consumer repo — mirroring
  `Invoke-ScenarioAEvidence.ps1`. A per-run **ownership marker** (`.scenario-a-run-id`-style
  `run-id`) gates cleanup; cleanup deletes **only** the owned child, **only after** the
  marker's run-id matches, with deletion **proven** (`Remove-Item -ErrorAction Stop` then
  `Test-Path` verifies absence) — the `Remove-OwnedRunRoot` discipline.
- **Physical path containment, fail-closed.** Resolve reparse points (symlink / junction /
  mount) at **every** path component before any read/write (`Resolve-PhysicalDir`); a
  workspace resolving inside a real repo is **refused**; unresolvable ⇒ fail closed.
- **No credentials / secrets / prod.** No production secrets, database, or deploy target in
  the test workspace. No secret is embedded in any case.
- **Network posture:** **deny-by-default egress.** The agent-under-test cannot reach the
  network; attempts are both blocked (containment) and observable (an assertion oracle for
  controls L, and for "no network action").
- **Package-install / command posture:** installs **blocked**; a command/tool **allowlist or
  approval boundary** bounds what the agent-under-test may execute. Blocked attempts are
  recorded as evidence (they are often exactly what a `should_not_*` case asserts must not
  happen).
- **Filesystem containment:** writes confined to the owned workspace; **caller-owned
  directories are never deleted or recursed**; an explicit **test-workspace marker** is
  required before any destructive cleanup.
- **Deterministic cleanup ownership + preserve-on-failure.** A **passing** run cleans up its
  owned child; a **failing** run **preserves** evidence for inspection (as the PS1 harness
  does). Cleanup never reports unproven success.
- **Fail-closed oracles.** The "no git mutation" oracle reuses `Test-ZeroCommitCount`: a zero
  is accepted only on git exit 0 + exactly one clean integer `0`; a broken check never
  certifies "0 commits."
- **Limits + emergency kill.** Max wall-clock per case/session; max command count where
  practical; an **emergency kill** that terminates the session, marks it `ERROR` (never
  PASS/FAIL), and preserves evidence.

## 16. CI posture

- **Advisory / non-blocking first.** The behavioral runner attaches as a **non-blocking**
  lane; a failure **informs**, it does not gate merge. It is **not** a required check on day
  one.
- **Structural validator stays the required floor.** `scripts/validate-skills.py` (and its
  self-tests, and the DCO / `gate-guard` jobs) remain **required and independent** — even
  after any future promotion (§17). The runner **consumes** what the validator proves
  parseable; it never replaces it. Weakening or removing the validator "because the runner
  covers it" is refused.
- **Independent of the merge gate surfaces.** The runner's lane must not touch the
  `gate-guard`-protected set (`.github/workflows/`, `CODEOWNERS`, `validate-skills.py`,
  `check_dco.py`, `scripts/tests/`); adding it is a normal reviewed change.

## 17. Promotion-to-gate criteria (DECIDED — before it could ever block)

Behavioral CI remains **advisory / non-blocking** initially. It is **not** eligible for
promotion to a required merge gate until **ALL** of the following hold, and the last is
non-negotiable (§20 D5):

1. At least **10 consecutive scheduled** behavioral runs have completed.
2. At least **2 full-corpus** behavioral baselines have completed successfully (each an
   owner-authorized event, §11).
3. Infrastructure **`ERROR` rate < 1%**.
4. **`JUDGE-ERROR` rate < 1%**.
5. **Quarantined runnable cases < 2%** of the runnable corpus.
6. **Quarantine count flat or shrinking** over the stability window.
7. **Observed spend within** the established guardrails (§11).
8. A **durable, explicit human-owner approval** recorded in the repository.

Even after promotion, `scripts/validate-skills.py` and the existing structural-validation
floor remain **independently mandatory**. **This phase does not activate blocking CI.**

## 17a. Phase 2B-0 — Activation Observability Capability Spike (implementation GATE)

An explicit gate **before general runner construction** (also the first build phase, §19).
**Purpose:** prove what activation evidence Claude Code can ACTUALLY expose **before** the
project builds a behavioral runner around assumed telemetry. It must determine, **by
evidence rather than assumption**:

1. **Whether Claude Code exposes a structured, machine-readable skill-activation signal.**
2. **If yes:** its signal/event **shape**; its **reliability**; **explicit vs
   model-selected** invocation behavior; **nested/composed** invocation behavior; and
   whether it **survives fresh, isolated sessions**.
3. **If no:** evaluate the strongest **truthful fallback** — the required **Output-Format /
   signature** evidence (§6 Tier 2) or other **durable, machine-observable** evidence
   actually available.
4. Prose such as `→ invokes skill-name` is **NEVER sufficient by itself** for deterministic
   activation proof.
5. Where only **ambiguous** evidence exists, the state is **`ERROR`** with **`reason_code:
   AMBIGUOUS_ACTIVATION`** (never PASS/FAIL).
6. The project **must NOT proceed to broad general-corpus behavioral execution** until the
   spike has either **(A)** proven a reliable activation-observation mechanism, **or (B)**
   produced an **explicit owner-approved limitation** defining exactly what v1 can and
   cannot truthfully claim.

**Constraint.** The spike does **not** invent a Claude Code API, event stream, hook, or
telemetry source; it reports what is real. The runner is built only on what 2B-0 establishes
(mechanism), or on the owner-approved limitation (scope). The spike also **selects and
calibration-tests the pinned semantic judge** (§8, §20 D1) and **establishes whether
monetary cost is observable** or only token/call/session proxies are (§11).

## 18. Testing strategy for the runner itself

The runner is code and gets its own tests, none of which spend live model tokens by
default:

- **Deterministic-grader unit tests** over recorded fixture transcripts (good/bad), incl.
  the reused Scenario A oracles — mirroring `Test-ScenarioAEvidence.ps1`'s good/bad fixture
  method.
- **Activation-observer tests** over synthetic event streams: Tier-1 event present / absent;
  Tier-2 signature only; **prose-only ⇒ `ERROR` / `reason_code: AMBIGUOUS_ACTIVATION`**;
  name-mention ⇒ NOT activation (false-positive guard); nested/multiple activations.
- **Semantic-judge harness tests** with a **mock judge**: well-formed pass/fail verdicts;
  malformed / timeout / refusal ⇒ `JUDGE-ERROR` (never PASS/FAIL); rubric-only input
  enforced (no leakage of expected answers or session reasoning).
- **Flake-controller tests**: quorum math; quarantine on oscillation; un-quarantine on
  stability; **assert** retry-until-green and auto-prune are absent.
- **Cost-guard tests**: ceiling breach ⇒ remainder `UNRUN`, no silent partial success; kill
  switch; monetary-`UNKNOWN` fallback enforcing token/call/session caps.
- **Containment tests**: reparse-point refusal, ownership-marker-gated cleanup, preserve-on-
  failure, deny-by-default egress — reusing the Scenario A safety-test patterns.
- **Report-schema tests**: `UNRUN` default; exactly six top-level states; `ERROR`/
  `JUDGE-ERROR` never collapse into pass/fail; `reason_code` present; schema version present.
- **A single live smoke** (opt-in, budgeted): one `should_trigger`, one `should_not_trigger`,
  one discrimination, and the Scenario A suite — to validate the real host adapter end-to-end
  before any wider run (and only after Phase 2B-0).

## 19. Implementation phases (future BUILD — designed, not scheduled here)

Each phase is separately approved; nothing here authorizes a build. **No later phase may
erase the evidence boundaries an earlier phase establishes** (isolation, activation-evidence
tiers, error/judge-error separation, six-state + `UNRUN` honesty, containment).

| Phase | Name | Delivers |
| --- | --- | --- |
| **2B-0** | **Activation-observability capability spike (implementation GATE, §17a)** | Evidence — not assumption — of the real activation signal; a go / owner-approved-limitation decision; the pinned judge + calibration; monetary-cost observability finding |
| **2B-1** | Runner core + versioned result/evidence schema | Entry point, case manifest, host-adapter interface + Claude Code adapter, evidence writer, report generator (`UNRUN` default, six states + `reason_code`), containment |
| **2B-2** | Deterministic graders | §7 graders incl. reused Scenario A oracles; activation matcher built on 2B-0's proven mechanism |
| **2B-3** | Independent semantic judge | §8 pinned judge, rubric derivation + unjudgeable-as-written census, `JUDGE-ERROR` handling |
| **2B-4** | Scenario A automated behavioral suite | Conversation-script driver + controls A–Q; automates runbook Control I; first end-to-end self-proof |
| **2B-5** | Generic `evals.json` + `trigger-evals.json` execution | The 1,740 single-turn corpus cases under §5 semantics |
| **2B-6** | Cost, repetition, quorum, quarantine, and sampling controls | §10–§12 (N=3/2-of-3, hard guardrails + kill switch, weekly stratified cadence) |
| **2B-7** | Advisory CI integration | Non-blocking lane; structural validator stays required (§16) |

Broad general-corpus behavioral execution (2B-5 onward) does not begin until the 2B-0 gate
has resolved to outcome A (proven mechanism) or B (owner-approved limitation).

## 20. Decisions (owner-ratified) and remaining evidence-gated items

### Owner-ratified decisions (DECIDED — Phase 2A owner review, 2026-08-07)

1. **Judge — DECIDED.** Semantic judging uses a separately configured, **pinned** judge
   identifier; the judge session is **independent** of the system-under-test session; the
   exact initial judge is **selected and calibration-tested during Phase 2B-0**; changing the
   judge model/version after behavioral baselining **requires behavioral re-baselining**. No
   specific current model name is hard-coded in this design.
2. **Repetition / quorum — DECIDED.** v1 **N=3**, **quorum 2-of-3**. **N is configurable**;
   **N=5** (or higher) only for **explicitly configured** release-candidate, disputed, or
   high-risk cases. **Never retry-until-green.**
3. **Cost guardrails — DECIDED (hard ceilings, NOT predicted costs).** PR **≤$5/run**; daily
   behavioral-eval total **≤$20**; cadence **≤$20/run**; **full-corpus DISABLED BY DEFAULT**
   (explicit owner authorization + a specific run-level cap). If monetary cost is not reliably
   exposable: no fabricated dollar figure — enforce token/call/session ceilings, report
   monetary spend **`UNKNOWN`**, **stop** at the enforceable cap, mark the remainder
   **`UNRUN`** (§11).
4. **Cadence sampling — DECIDED.** Weekly rotating **stratified ~10% of shipped skills** per
   run; spans families; includes required overlap/discrimination neighbors; rotates
   deterministically; eventually covers the whole corpus; reports rotation coverage (§12).
5. **CI promotion criteria — DECIDED.** Advisory/non-blocking; not promotable to a required
   gate until ALL of: ≥10 consecutive scheduled runs; ≥2 successful full-corpus baselines;
   `ERROR` rate <1%; `JUDGE-ERROR` rate <1%; quarantined runnable cases <2% of the runnable
   corpus; quarantine count flat/shrinking; spend within guardrails; durable explicit
   human-owner approval recorded in the repo. Structural validation stays independently
   mandatory even after promotion (§17).
6. **Transcripts — DECIDED.** Raw behavioral transcripts are **external and uncommitted by
   default**; the runner **never** auto-commits raw transcripts; only deliberately
   **curated, sanitized, synthetic** regression fixtures may later be added to Git via normal
   reviewed changes; **preserve-on-failure** external evidence remains allowed (§13, §15).
7. **Host adapter — DECIDED.** **Claude Code is the first supported behavioral-execution
   adapter**; the architecture may expose an adapter interface for future hosts, but Project
   Aegis makes **no parity claim** for another adapter until it is implemented and
   **behaviorally verified**. No invented cross-provider equivalence (§14).
8. **`should_not_do` outlier — DECIDED.** Supported explicitly in v1 as a **LEGACY /
   DIVERGENT REFUSAL CASE TYPE**: semantics = target activates AND required refusal is
   satisfied; the runner emits an **author-facing schema/corpus warning** about the
   divergence. The runner does **not** silently rewrite or auto-normalize the cases, and v1
   is **not** blocked on retyping; any corpus normalization is a separate future scoped
   change (§3, §5).
9. **Assertion-classification sign-off — DECIDED.** Human approval owner: **Peter Nguyen**.
   `skill-quality-reviewer` may provide **advisory** analysis (deterministic-vs-semantic
   classification, eval integrity, unjudgeable-as-written findings) but is **not** the
   approval authority (§8).
10. **Doc retention — DECIDED.** **No** docs-retention/index change in this Phase 2A design
    branch; the change stays scoped to this single primary design document; retention/index
    integration may be revisited during implementation/release only if repository policy
    actually requires it.

### Remaining — DEFERRED TO 2B-0 — EVIDENCE REQUIRED

These cannot be honestly finalized until the Phase 2B-0 capability spike (§17a, §19) produces
real host evidence; they are **not** open-ended design questions, and none is invented to
fill a section:

- **R1 — Activation-observation mechanism + the truthful scope of v1's claims.** Whether
  Claude Code exposes a reliable structured activation signal — and, if not, the strongest
  truthful fallback and the explicit owner-approved limitation on what v1 can/cannot claim —
  is decided by 2B-0's evidence (outcome A or B). Broad general-corpus behavioral execution
  does not proceed until then.
- **R2 — Exact pinned judge model/version + calibration result.** The *policy* is DECIDED
  (D1); the concrete pinned identifier and its calibration outcome are produced during 2B-0.
- **R3 — Monetary-cost observability vs proxy enforcement.** Whether the provider surface can
  expose monetary cost (enforce `$` ceilings directly) or only token/call/session proxies
  (monetary = `UNKNOWN`) is a host-evidence question resolved in 2B-0; the *fallback* is
  already DECIDED (D3).

## 21. Non-goals (what v1 does NOT do)

- No full production certification of the library.
- No guarantee of deterministic model behavior.
- No automatic rewriting, "fixing", or retyping of failing or outlier skills/evals (incl. the
  `should_not_do` cases, §20 D8).
- No retry-until-green; no auto-pruning of failing cases; no hidden quarantine.
- No replacement of human review.
- **No replacement of the structural validator** (it stays the required floor, always).
- No merge automation; no enabling of auto-merge; no blocking CI in this phase.
- No claim that any unexecuted structural eval "passes."
- No autonomous spend without the owner-defined guardrails; **no full-corpus run without
  explicit owner authorization**.
- **No fabricated cross-provider parity** — the host-adapter boundary is honest; only Claude
  Code / Claude Agent SDK is a claimed adapter until a second host demonstrably satisfies the
  activation-observation contract.
- **No assumed Claude Code activation API/event/hook/telemetry** — the mechanism is whatever
  Phase 2B-0 proves real (§17a).
- No modification of Scenario A behavior, existing eval assertions, or the mechanical
  Scenario A harness.

## 22. Risks

| Risk | Mitigation in this design |
| --- | --- |
| **Activation can't be observed deterministically on a host** | Evidence tiers (§6); ambiguity ⇒ `ERROR` + `reason_code: AMBIGUOUS_ACTIVATION` (never a verdict); **Phase 2B-0 gate blocks broad execution until proven or owner-limited**; no fabricated event stream (§6, §17a) |
| **Pass-claim leakage** (design prose drifting into "the evals pass") | Every capability statement stays conditional; verbatim non-claims (§24); `UNRUN` default |
| **Single-shot stochastic overclaim** | Repeats-with-quorum as the unit of evidence (§10) |
| **Context leakage between cases** | Fresh isolated session per case; no reuse of a routed session (§5) |
| **Judge judging itself / leaking answers** | Pinned, independent call, rubric-only input, no session reasoning; `JUDGE-ERROR` isolated (§8) |
| **Coherent-topic rule mis-graded by a regex** | Explicitly semantic; reuses the corpus atomicity test + anti-overcorrection case (§8, §9) |
| **Cost blow-up** | Hard ceilings + kill switch ⇒ `UNRUN` remainder; full-corpus disabled by default (§11, §12) |
| **Monetary cost not exposable by the provider** | Enforce token/call/session ceilings; report monetary `UNKNOWN`; stop + `UNRUN` (§11; resolved in 2B-0) |
| **Runner executes an agent that mutates/exfiltrates** | Containment-first, reusing Scenario A safety semantics; deny-by-default egress; fail-closed oracles (§15) |
| **Structural floor dropped as "redundant"** | Validator stays required and independent, even post-promotion (§16, §17) |
| **Outliers silently normalized** | Recorded as findings, given explicit semantics, never rewritten (§3, §5, §20 D8) |

## 23. Acceptance criteria for the future BUILD phase

A built runner is acceptable when (separately approved and evidenced):

1. **Phase 2B-0 gate satisfied** — a reliable activation-observation mechanism proven, OR an
   explicit owner-approved limitation recorded — **before** any broad general-corpus
   behavioral execution (§17a).
2. Every corpus case type in §3 — incl. refusal-as-`should_trigger`, the `should_not_do`
   legacy-refusal outlier, and degenerate discrimination — has a **working execution path**
   with the §5 semantics.
3. The **fresh-session isolation** rule holds (proven: no case sees another's context).
4. Activation observation implements the §6 tiers on the 2B-0-proven mechanism; **ambiguous
   activation is `ERROR` / `reason_code: AMBIGUOUS_ACTIVATION`** (never PASS/FAIL); name-
   mention is **not** counted as activation.
5. Deterministic vs semantic routing per §7/§8; the judge is **pinned + independent**;
   **`JUDGE-ERROR` never becomes PASS/FAIL**; the unjudgeable-as-written census is produced.
6. The report carries `UNRUN` as default and **exactly six** top-level states (§13); `ERROR`
   and `JUDGE-ERROR` never collapse into pass/fail; `reason_code` is present where applicable.
7. Cost model + hard ceilings (PR ≤$5, daily ≤$20, cadence ≤$20, full disabled-by-default) +
   kill switch ⇒ honest `UNRUN` remainder; monetary-`UNKNOWN` fallback enforces token/call/
   session caps (§11).
8. Flake policy (N=3/quorum 2-of-3/visible quarantine) implemented and configurable;
   retry-until-green and auto-prune provably **absent** (§10, §18).
9. **Scenario A** behavioral suite passes its own self-proof, covering controls A–Q, with the
   coherent-topic rule graded semantically (§9) — and it does **not** modify or replace the
   mechanical harness.
10. Containment per §15 (reparse refusal, ownership-marker cleanup, preserve-on-failure,
    deny-by-default egress) proven by the runner's own safety tests.
11. CI lane is advisory/non-blocking; the structural validator remains required; promotion
    criteria (§17) are only *proposed*, never auto-activated.

## 24. Non-claims

> No runner exists as of this design. No eval case has been executed. This document
> specifies how execution WOULD work; nothing in it is an eval result, and the library's
> eval convention remains structural-only until a built runner produces real, reported runs.

Additionally, and preserved exactly:

- No runner exists as of this design.
- No eval case has been executed by this proposed runner.
- This design is not an eval result.
- Existing structural validation (`scripts/validate-skills.py`, decision D3) remains the
  current **execution floor** until a built runner produces real, reported runs.

**Manual vs general-automated (do not conflate).** Live behavioral testing of Scenario A
**has** occurred: the acceptance runbook's Control I fresh-session rerun has **two accepted
manual runs** on current head. That is *manual live Scenario A acceptance*. It is **not** a
general automated behavioral eval runner — **no such runner exists yet**, and this document
is its design, not its output. The census in §3 is evidence for the design, not an eval
result.
