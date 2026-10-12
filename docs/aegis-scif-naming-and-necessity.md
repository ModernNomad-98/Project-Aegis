# Aegis SCIF — the naming record and the necessity/reuse check

**Aegis SCIF — Secure Compartmented Integrity Framework** is the name of the
engineering framework this repository's delivery rule serves; **Aegis SCIF** is
the short form, used after this first substantive mention. The plain-language
definition is:

> An engineering framework that separates responsibilities and approval
> authority, requires independent verification, and binds delivery decisions to
> evidence.

The same idea in one line: **Separate duties. Independently verify. Deliver with evidence.**

**This page explains; it holds no normative force.** The normative rule is
[docs/delivery-workflow.md](delivery-workflow.md) — in particular
[the necessity and reuse subsection](delivery-workflow.md#necessity-and-reuse-the-five-questions-owed-at-stage-a-and-tested-at-stage-b),
which is the single source of the check explained in part 2 below. Where this
page and that page differ, that page governs. This page renames no repository,
package, command, path or API identifier; creates no skill, harness, runner,
coordinator, dashboard, register or report; and grants no execution,
publication, review or merge authority.

## 1. The naming record

### 1.1 The name and the forms it takes

| Form | Text | Where it is used |
| --- | --- | --- |
| Full expansion | **Aegis SCIF — Secure Compartmented Integrity Framework** | The first substantive mention on a page or document, once. |
| Short form | **Aegis SCIF** | Every later mention. |
| Plain-language definition | *An engineering framework that separates responsibilities and approval authority, requires independent verification, and binds delivery decisions to evidence.* | Wherever a reader needs to know what the name means rather than what it is called. |
| Explanatory line | **Separate duties. Independently verify. Deliver with evidence.** | Titles, summaries and status lines. |

The record is **added, not applied**: the rename surface was empty (1.3), so
there was no existing prose to edit. The repository's operative term for the rule
itself remains "the delivery workflow"; **Aegis SCIF** names the framework that
rule serves, and the delivery page stays the canonical text.

### 1.2 The package decisions (D1–D7) and the limits they carry

The SCIF package carries owner decisions **D1–D7**. The records retained in this
workspace — `SCIF-PLAN-rev5.md`, `SCIF-recon.md` and
`FAST-CHECKPOINT-2026-10-11D.md` — name those decisions by number and
quote their effects; the brief's verbatim list is **not retained in this
workspace**, so this table records the effect each number is used for and labels
that attribution **carried, not verbatim**. Nothing in this table is a fresh
owner decision, and this page grants nothing.

| Decision (carried) | What it decides, as the retained records use it | The limit it records |
| --- | --- | --- |
| **D1–D4 — the naming decision as rendered** | Use **Aegis SCIF** in maintained documentation: the full expansion on the first substantive mention and the short form after; **no** repository, package, command or path renames; historical quotes, receipts and hashes are preserved rather than rewritten; a residual-occurrence inventory is required. | Renames no identifier and edits no historical record; the inventory (1.5) is the evidence that the outcome is complete rather than partly applied. |
| **D5 — history is preserved** | Records are corrected **forward**, never rewritten: dated appends and addenda keep every earlier byte intact. | No merged record is rewritten; a correction is a new dated block beside the original claim. |
| **D6 — no new machinery, no unrelated bundling** | No new skill, harness, runner, coordinator, dashboard, register or report; no unrelated cleanup; no private or production data. | The check rides on the plan Stage A already owes and on Stage B's existing verdict — it is not a new field, gate or report. |
| **D7 — no retrospective approval** | The package touches no approval-register entry, claims no waived check, and holds no provider-budget, deployment or repository-settings authority. | This page and the package grant no approval, no waiver and no merge permission; a missing authority is named as the exact missing grant. |

### 1.3 The discovery finding: the rename surface is empty

**The former name has zero occurrences in the tree at this base, and zero in
reachable git history.** The searches that produced zero, run at base
`09a5d2b3c9a3e9e3cff307d94b6f241600e0dc2d`:

| Search | Command (at the base) | Result |
| --- | --- | --- |
| The former name, any separator | `git grep -i -E 'aegis[ _-]factory' <base>` | **0** lines |
| The phrase "factory framework" | `git grep -i -E 'factory[ _-]framework' <base>` | **0** lines |
| The new name before this PR | `git grep -i 'aegis scif' <base>` | **0** lines |
| History, all reachable commits | a `git log --oneline -S` pickaxe for the former name (the phrase quoted once at 1.4), its underscored spelling, `Aegis SCIF` and `factory framework` | **no commits** for any term |

Consequence — **add, do not edit**: there is no class-(a) explanatory prose to
rename and no class-(b) historical quote to preserve, so this page **adds** the
record, and the inventory below is the deliverable. The zero is the finding: a
rename whose rename surface is empty can only be evidenced by an inventory of
what remains.

### 1.4 The alias: the P2 workstream

The P0 directive names the supervisor workstream in its historical wording,
**"P2 Aegis Factory supervisor"**. In every document written from this point on,
that workstream is transcribed as **"P2 Aegis SCIF supervisor"**. The two
phrasings name the **same workstream** — an alias, not a second lane and not a
scope change. The one quotation above is deliberate and counted (1.5, class
(e)); it exists so the alias is defined rather than assumed. The transcription
itself belongs to the P0-B transcription workstream, not to this page.

### 1.5 The residual-occurrence inventory

Every remaining old-name or `factory`-substring occurrence in the tree at
base `09a5d2b3c9a3e9e3cff307d94b6f241600e0dc2d` is classified below with its
disposition. Counts are measurements at that named revision: they move when the
tree moves, and they are re-derivable with the commands in part 4.

| Class | What it is | Count at the base | Disposition |
| --- | --- | --- | --- |
| (a) current explanatory prose using the old name | — | **0** | nothing to rename; the absence is the finding |
| (b) immutable historical quote, receipt or approval using the old name | — | **0** | nothing to preserve; no such quote exists |
| (c) technical identifier, path or API | `sqlite3 row_factory`, `factory=CheckedSQLiteConnection`, `dataclasses default_factory`, the test name `test_client_factory_configuration` (in code and inside immutable evidence logs) | **113** | intentional-technical: renaming these would break code or falsify retained logs; listed with file:line below |
| (d) unrelated use, different referent | QA fixture vocabulary, the "skill-and-agent factory" build-phase referent, SDK client-factory prose, generic design-pattern prose, one substring false positive | **29** | intentional-unrelated: outside the naming decision's scope; listed with file:line below |
| (e) the P0 directive's historical wording | the alias phrase, quoted **once** at 1.4 | **1 deliberate occurrence added by this PR** (1.4); **0** at the pre-PR-2 base | explicitly unresolved: transcribed as "P2 Aegis SCIF supervisor" in the P0-B transcription workstream; the quotation at 1.4 defines the alias, and it is the only old-name phrase this PR adds |

**Class (c) — 113, intentional-technical (never rename).** 83 `row_factory`
lines, 15 `default_factory` lines, 1 line whose `factory=` argument
is the checked SQLite connection class, and 14 lines naming
`test_client_factory_configuration` (1 in code, 13 inside immutable evidence
logs). The `CheckedSQLiteConnection` lines that do not contain the substring
`factory` are not counted:

- `docs/evidence/ber-pr88-closeout-2026-09-12/preflight/corrections-6.log` - 343
- `docs/evidence/ber-pr88-closeout-2026-09-12/preflight/corrections-posix.log` - 662, 663
- `docs/evidence/ber-pr88-closeout-2026-09-12/verification/pr88-5863fb1-6.log` - 344
- `docs/evidence/ber-pr88-closeout-2026-09-12/verification/pr88-5863fb1-posix.log` - 347
- `docs/evidence/offline-ci-2026-09-12/hosted-34675606660/linux/ber.log` - 362
- `docs/evidence/offline-ci-2026-09-12/hosted-34675606660/windows/ber.log` - 362
- `docs/evidence/offline-ci-2026-09-12/windows/ber.log` - 362
- `docs/evidence/shared-contracts-closeout-2026-09-12/logs/4d6d292-posix.log` - 697
- `docs/evidence/shared-contracts-closeout-2026-09-12/logs/61f2a46-posix.log` - 695
- `docs/evidence/shared-contracts-closeout-2026-09-12/logs/windows-4d6d292-5.log` - 362
- `docs/evidence/shared-contracts-closeout-2026-09-12/logs/windows-61f2a46-5.log` - 360
- `docs/evidence/shared-contracts-closeout-2026-09-12/logs/windows-working-5.log` - 360
- `tools/aegis_delivery_control/adapters.py` - 430, 827
- `tools/aegis_delivery_control/authority.py` - 590
- `tools/aegis_delivery_control/owned_paths.py` - 973
- `tools/aegis_delivery_control/storage.py` - 1094, 1127, 44726
- `tools/aegis_delivery_control/tests/_trusted_readiness_store.py` - 134, 162
- `tools/aegis_delivery_control/tests/test_dispatch.py` - 861, 950, 999, 2411, 2470, 3229, 3295, 3678, 4390, 4711, 6168
- `tools/aegis_delivery_control/tests/test_storage.py` - 360, 390, 1512, 4284, 4631, 5019, 5116, 5340, 6268, 6319, 6385, 7325, 7380, 7412, 7836, 7972, 7994, 8074, 8096, 8193, 8276, 8336, 8593, 8673, 9375, 10536, 11149, 11369, 11418, 11794, 11818, 12190, 12907, 13004, 13244, 13396, 14583, 14631, 14702, 14763, 15178, 15262, 15307, 15588, 16168, 16236, 17858, 17923, 17977, 18040, 18570, 18738, 19270, 19527, 19602, 19857, 20142, 21607, 21683, 24125, 24393, 24463, 24567, 26093
- `tools/behavioral_eval_runner/budget.py` - 60
- `tools/behavioral_eval_runner/containment.py` - 152, 153
- `tools/behavioral_eval_runner/evidence.py` - 318
- `tools/behavioral_eval_runner/materialize.py` - 381, 397, 761
- `tools/behavioral_eval_runner/models.py` - 246, 247, 248, 323, 1040, 1041
- `tools/behavioral_eval_runner/preflight.py` - 79
- `tools/behavioral_eval_runner/scheduler.py` - 68
- `tools/behavioral_eval_runner/tests/test_calibration_transport.py` - 374

**Class (d) — 29, intentional-unrelated (different referents).** The five
sub-classes and their measured splits: 13 QA fixture-factory vocabulary; 6
"skill-and-agent factory" build-phase architecture; 5 SDK client-factory prose;
4 generic design-pattern/test-pattern prose; 1 substring false positive
("satisfactory"):

- `.claude/skills/integration-test-designer/SKILL.md:119` - Data strategy: <seed/factory source, isolation mechanism, cleanup>
- `.claude/skills/performance-test-harness/evals/trigger-evals.json:44` - "prompt": "Design our test automation architecture: runner choice per layer, fixture and factory structure, pa
- `.claude/skills/qa-automation-architect/SKILL.md:3` - description: Design the test-automation architecture that implements a QA strategy — tool/runner selection per
- `.claude/skills/qa-automation-architect/SKILL.md:118` - Structure: <directory layout, naming, fixture/helper/factory placement>
- `.claude/skills/qa-automation-architect/evals/evals.json:14` - "Designs directory structure, fixture/factory placement, import boundaries, and an auth-state strategy.",
- `.claude/skills/test-data-architect/SKILL.md:3` - description: Design the test-data strategy across all test layers — deterministic seed/fixture/factory design
- `.claude/skills/test-data-architect/SKILL.md:16` - tenant catalog, factory/seed architecture per layer, isolation and cleanup
- `.claude/skills/test-data-architect/SKILL.md:72` - preconditions. One factory definition feeding all layers where feasible
- `.claude/skills/test-data-architect/SKILL.md:101` - Factory architecture: <single shape-truth definitions, overrides, id strategy>
- `.claude/skills/test-data-architect/SKILL.md:160` - persona catalog template, factory patterns (shape truth, overrides,
- `.claude/skills/test-data-architect/references/test-data-patterns.md:23` - ## Factory patterns
- `.claude/skills/test-data-architect/references/test-data-patterns.md:25` - - **Single shape truth:** one factory definition per entity used by all
- `.claude/skills/vitest-unit-component-engineer/SKILL.md:111` - between tests; prefer factory mocks and `vi.resetModules` when it bites.
- `docs/evidence/behavioral-eval-runner-wp-2b-3-summary.md:57` - | `calibration_transport.py` | Pinned terms as code: OpenAI Responses API; exact snapshot `gpt-5.5-2026-04-23`
- `docs/evidence/behavioral-eval-runner-wp-2b-3-summary.md:95` - factory); `max_retries=0` yields exactly one transport attempt
- `docs/evidence/behavioral-eval-runner-wp-2b-3-summary.md:473` - passes it only to the pinned SDK client factory, and no secret can reach the
- `docs/prompts/master-claude-skills-and-agents-development-prompt.md:62` - Create the skill-and-agent factory before creating real skills:
- `docs/prompts/phased-claude-skills-prompts.md:18` - ## Phase 0 Prompt - Build the skill and agent factory
- `docs/research/claude-skills-principal-architecture-findings.md:59` - The right architecture is a skill-and-agent factory:
- `docs/research/claude-skills-principal-architecture-findings.md:177` - ### Phase 0 - Skill and agent factory
- `docs/roadmaps/aegis-documentation-readability-backlog.md:2907` - claim that zero pages are satisfactory. The correction work is retained;
- `docs/roadmaps/product-agnostic-skill-and-agent-roadmap.md:59` - | 1 | Skill factory | Standards, templates, eval schema, and validators exist. |
- `docs/roadmaps/product-agnostic-skill-and-agent-roadmap.md:69` - | 0 | P0 | Skill and agent factory | Prevents low-quality bulk generation. |
- `tools/aegis_delivery_control/tests/test_platform.py:545` - for factory in factories:
- `tools/aegis_delivery_control/tests/test_platform.py:546` - with self.subTest(factory=factory):
- `tools/aegis_delivery_control/tests/test_platform.py:551` - factory()
- `tools/behavioral_eval_runner/judge/calibration_credential.py:30` - sole legitimate caller is the transport client factory.
- `tools/behavioral_eval_runner/judge/calibration_gates.py:587` - Object identity is registered only by the factory. A forged ``__new__``
- `tools/behavioral_eval_runner/judge/calibration_transport.py:10` - - the client factory fails closed on proxy/TLS/base-URL environment

Each remaining old-name reference is therefore **intentional-technical**,
**intentional-unrelated** or **explicitly unresolved**; none is left
unclassified. No unrelated occurrence is edited by this PR, and nothing above
renames an identifier.

## 2. The necessity/reuse check (plain language)

**The normative rendering of this check is
[the delivery workflow's necessity and reuse subsection](delivery-workflow.md#necessity-and-reuse-the-five-questions-owed-at-stage-a-and-tested-at-stage-b);
this part explains it and holds no normative force.** Stage A owes the answers in
its plan; Stage B tests them and records a per-question routing disposition
before it accepts. The point is not paperwork: it is to stop a change being built
because it was asked for, before anyone has shown that the need exists, checked
what already does the job, or said what the smallest safe version is.

### 2.1 The five questions

1. **Necessity** — what need does this serve, and what is the evidence that the
   need exists? *Routing:* **satisfied** → cite the proof (an issue, a defect, a
   decision, a measurement).
2. **Reuse** — what existing mechanism, skill, script, document or decision
   already does this? *Routing:* **owned elsewhere** → preserve that ownership
   and cite it; nothing suitable → build the smallest new thing.
3. **Ownership** — who holds the authority and the responsibility for this
   surface, at this revision? *Routing:* **owned** → proceed inside the existing
   authority and do not re-ask; absent, expired or out of scope → prepare one
   concrete decision for the owner instead of proceeding.
4. **Minimum-safe action** — the smallest action that satisfies the need without
   weakening a control: no removal of a required check, no tier downgrade, no
   scope widening to make a pass.
5. **Complexity justification** — why the machinery is warranted, and what would
   be smaller? *Routing:* **uncertain** → run a bounded check (a time-boxed,
   read-only investigation) before building.

An answered question is **cited, not re-asked** — that sentence is normative on
the delivery page, and it is what keeps this check from becoming another round of
ceremony.

### 2.2 Reuse is conditional: the six tests

Reusing evidence is not automatic. Before an earlier result is carried into this
decision, all six properties are re-checked:

| Test | The question it asks |
| --- | --- |
| **Revision** | Is the fact still true at this head, or was it true only at an earlier one? |
| **Policy** | Has the rule that governed it changed since? |
| **Environment** | Same host, runner or profile as the one that produced it? |
| **Scope** | Does the original scope reach this action? |
| **Provenance** | Is the source retrievable, and is it the right author? |
| **Validity** | Is it still in force and un-superseded? |

### 2.3 What reuse never does

Reuse **never** transfers roles, **never** treats a publisher as a reviewer,
**never** reuses a previous-head verdict, and **never** replaces fresh validation
where a stage's own requirement is a fresh check. The delivery page carries those
rules in its own words — the skills-row protocol (exact copying transfers no
stage credit or authority), the exact-head invalidation rule (a result at a
superseded head satisfies nothing) and the merge prohibition (a reviewer does not
merge what it reviewed).

## 3. What this page deliberately does not do

- It renames **nothing**: no repository, package, command, path, API or skill
  identifier changes, and no historical quote, receipt or hash is rewritten.
- It creates **no new machinery**: no skill, harness, runner, coordinator,
  dashboard, register or report (D6), and no new dependency or workflow file.
- It adds **no bound field, no CI gate and no register entry** (D7); the check
  rides on Stage A's plan and Stage B's existing verdict.
- It **grants nothing**: no approval, no waiver, and no execution, publication,
  review or merge authority.
- It **restates no condition**: for merge-gate and stage conditions this page is
  a reader's explanation; the normative text is
  [docs/delivery-workflow.md](delivery-workflow.md).
- It does **not re-count the inventory after the base**: the figures in 1.5
  belong to `09a5d2b3` and are re-derived, not remembered, when the tree
  moves.

## 4. Re-deriving the figures on this page

All commands run at base `09a5d2b3c9a3e9e3cff307d94b6f241600e0dc2d` in a
clone whose `origin` is `https://github.com/ModernNomad-98/Project-Aegis.git`:

```text
git grep -i -c factory <base>                    # 142 matching lines over 44 files
git grep -i -E 'row_factory|default_factory|factory=CheckedSQLiteConnection|test_client_factory_configuration' <base>   # 113 lines (class c)
git grep -i -E 'aegis[ _-]factory|factory[ _-]framework' <base>    # 0 lines at the base
git grep -i 'aegis scif' <base>                  # 0 lines at the base
```

The history search is a `git log -S` pickaxe over all reachable commits whose
search term is the one phrase quoted at 1.4; it returned no commits.

The class split is a classification of those 142 lines, not a second grep: the
113 lines whose `factory` substring is a technical identifier are class (c),
and the remaining 29 are class (d). At this PR's head the same greps return
**1** old-name line — the deliberate alias quotation at 1.4 — and the class
(c)/(d) figures are unchanged, because this PR edits none of those lines.

**Dated re-derivation — 2026-10-12: the closing sentence above was already false at the head it names.**
The part-4 commands were re-run at three refs on 2026-10-12. At base `09a5d2b3` they reproduce the
base measurement exactly — `factory` **142 matching lines over 44 files**, class (c) **113**, the
old-name grep **0** and `aegis scif` **0**. At **this page's own PR #739 head `4d5ccb0b`** they
already return **187 lines over 45 files, class (c) 118, old-name 3 and `aegis scif` 16**, and
`7fbc2335` returns the **same five figures** (187 / 45 files / 118 / 3 / 16). The whole delta is this
page's own inventory text: a per-file comparison of the `factory` count between the base and the head
returns exactly **one** differing file — `docs/aegis-scif-naming-and-necessity.md` itself (absent at
the base tree, 45 lines at the head; class (c) 5, and 113 + 5 = 118) — and **zero** common files
changed their count, so no product or code file contributed a `factory` line. The closing sentence is
therefore **already 3 at this PR's head**, not "0 → 3 since". It is left as written, because records
are corrected forward and never rewritten; this note is its correction. Commands, each at all three
refs: `git grep -i -c factory`, `git grep -i -E
'row_factory|default_factory|factory=CheckedSQLiteConnection|test_client_factory_configuration'`,
`git grep -i -E 'aegis[ _-]factory|factory[ _-]framework'` and `git grep -i 'aegis scif'`.

**Dated addendum — 2026-10-12: the PR body's witness count 33 / 46 is a
matching-line count, and it reproduces.** Re-read at base `09a5d2b3` and at
`d6d186c8` (**PR #739 head**; merged as `4d5ccb0b` — the page's own L274 note
names the merge, and the two commits carry the same tree `2e35f9a7…`):
`git grep -c -E 'MG[1-5]' -- docs/delivery-workflow.md` → **33** matching
lines; `git grep -c -E 'SD-[A-G]' -- docs/delivery-workflow.md` → **46**
matching lines. The figures the Stage F review could not reproduce — 42 and 66
— are the **occurrence** counts of the same patterns in the same file:
`git grep -o -E …` → 42 and 66. Two methods, one file, no contradiction; the
method is named here because the figure is (PROC-04). R5's own parenthetical
"grep -n line counts 74 / 136" is the same **matching-line** method over the
**whole tree** at that head: `git grep -c -E 'MG[1-5]'` sums to **74** lines
and `git grep -c -E 'SD-[A-G]'` to **136** (whole-tree occurrences 91 / 168).
All four published numbers are therefore one method at three scopes — 33 / 46
in this file, 74 / 136 in the tree, 42 / 66 occurrences in this file — and
none is contradicted. The counts are identical at the base and the head, which
is the witness's substantive claim (no `MG` or `SD` token was added or
edited). They are revision-bound: at `ad1e40fc` the same four commands return
34 / 44 and 48 / 68. For completeness of the part-4 correction above, at that
head the `factory` class (d) figure is **69** (= 187 − 118), beside class (c)
118 and the base 29.
