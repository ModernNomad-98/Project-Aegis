# Consumer starter package (v1)

Status: **normative definition of the v1 consumer starter package.** This page
defines one fixed, dependency-checked installation for a beginner's first product
slice. It is measured against the Project Aegis source tree at commit
`ffb040c7a363648856475280646bbd142dfabe4e` (tree
`88a5aee4ad928a49c2fb945032585843ec652da7`). It is not an installation log
and not an acceptance record: the first native-host acceptance record is produced
separately, after the run it describes, and nothing here is evidence that the
procedure has already been executed on your machine. Section 7.1 does report a
local verification run of the published block; that is a check of the block, not
an acceptance result for your repository.

**Reading key.** **Role A** is the Project Aegis source repository; **Role B** is
your own consumer/product repository, which copies Aegis files into its workspace.
**J1** is the first consumer journey this package supports (below). **MANUAL-ONLY**
marks a skill a human must name explicitly before it is used. **UNRUN** means not
executed, with the exact remaining action named; it is never a pass. `$SRC` is a
clone of the source repository at the pinned commit and `$TGT` is your product
repository.

## 1. What this package is, and what it does not prove

The starter package is the exact, enumerated set of files a beginner copies into a
new product repository so that the Aegis front door works with nothing missing. It
exists because the previously documented beginner route — clone the whole source
repository, then copy the skill folders you want — carries no statement of which
files a chosen skill actually needs, and the front door's documented workflow reads
files that route does not copy.

### 1.1 The journey it supports (J1)

J1 is the beginner's first end-to-end slice, delivered locally:

1. install into your consumer repository (section 7);
2. startup and consumer-role recognition (Role B, Stage 0), with the startup
   context gate's report and identity check (section 8);
3. requirements (Stage 1 owner `requirements-gathering-facilitator`);
4. product definition (Stage 2 owner `product-spec-writer`) and
   design/refinement (Stage 3 owners `domain-modeler`, `architecture-designer`;
   the orchestrator's Stage-3 line also names `architecture-advisor` and
   `adr-writer`, which are classified in section 4 and deliberately not installed);
5. an independently audited plan (`plan-of-record-author` revision plus a
   separate `plan-audit-reviewer` verdict bound to the captured hash);
6. implementation of that plan through `ai-sdlc-operating-model`'s inner
   lifecycle and the enforcers its stage map names, including
   `agent-startup-context-gate`. No shipped skill owns general implementation
   (`docs/delivery-workflow.md:100` records that absence), so your host agent
   implements and this package does not pretend a skill does;
7. independent review (`code-reviewer`);
8. positive and negative functional tests (cases from `test-plan-designer`,
   executed by your host agent);
9. local delivery (Stage 8's local-only branch; `release-readiness-reviewer`
   applied to local artifact evidence);
10. interruption and fresh-session continuation (`docs/project-state.md`'s
    latest STATE SNAPSHOT wins);
11. policy handoffs: recording authority and screenshot evidence (sections 10
    and 11).

### 1.2 The claim boundary

The package is **complete for J1** under two rules that the procedure in section
7 applies file by file and the install verifies for the enumerated set:

1. every file J1's documented workflow reads is either copied or classified in
   section 3 with the reason it is not needed; and
2. every skill the stage map tells a J1 stage to invoke is either installed or
   classified the same way.

Both rules hold for the 17 skills in section 2. The claim is **not** complete for
journeys outside J1 — UI slices, AI features, hosted deployment, SaaS or
multi-tenant design, migrations, security-lens reviews, or release-with-agents.
For any step outside J1 the rule is fail-closed: stop and name the owning skill and
the exact install-on-demand action (section 4.2); never improvise and never
silently skip a gate.

### 1.3 Limits stated inside the claim

- The startup gate is **required behaviour, not automatic enforcement**
  (`.claude/skills/agent-startup-context-gate/SKILL.md:86-97`). Installing it
  ships the contract and its check, not a hook and not a security boundary.
- The gate's shared-local-resource lane records Windows as **SKIP/UNRUN with a
  nonzero required skip** (`SKILL.md:247-249`). J1 is single-agent with no shared
  local stack, port, database or fixture set, so that lane is not exercised and is
  never reported as a pass.
- The gate's mandatory manual provenance step is a human/agent decision recorded
  in its report (`SKILL.md:143-169`); no automation is claimed for it.
- The solo-owner commit-identity policy is an **open owner decision**
  (section 8.3). The package ships the gate's fail-closed behaviour and asserts no
  policy; that is one reason it makes no consumer-readiness claim.
- A destination `AGENTS.md`/`CLAUDE.md` that differs by any byte stops the
  install (exit 22), and v1 documents no in-place merge: reconcile the two files
  to the pinned bytes before installing, or install into a tree that has neither.
- The procedure checks the source chain for reparse points but not your
  destination tree, so a junction or symlink that already exists inside the target
  is not detected by the published harness.
- This package installs files; it does not run your project, choose your
  technology, or approve anything. Approvals remain the human's.

**Not claimed by this package:** consumer readiness, production readiness,
multi-tenant or SaaS readiness, a second host, a hosted deployment, live-model
evaluation, CI-green equivalence, or "complete native consumer testing". One
host's evidence is bounded to that host and that run.

## 2. The 39 files: 17 skills and 2 startup files

### 2.1 Selection rule

A skill is in the package when J1's documented workflow reads or invokes it — that
is, when it is (i) the front door, (ii) a gate or authority artifact the front door
is told to read and cite, (iii) the owning skill of a J1 step, (iv) a skill whose
output J1's recording schema composes by name, or (v) an enforcer the stage map
names for a J1 stage, even when no skill links to it. Everything
conditional-by-evidence, everything MANUAL-ONLY, and every owner of a stage
outside J1 is excluded (section 4).

### 2.2 The skills and why each one is a direct dependency

| Skill | Why it is a J1 direct dependency |
| --- | --- |
| `project-orchestrator` | The front door and stage detector; the startup routing hands the beginner to it (`CLAUDE.md` startup item 3; `README.md`, section "Your first session"). Its Capability 4 owns the `docs/project-state.md` write loop (`SKILL.md:309-332`). |
| `ai-sdlc-operating-model` | Orchestrator input 5: "the cited gate/authority artifacts … Read to CITE, never copy" (`SKILL.md:83-86`); its `references/stage-gate-map.md` is the stage table J1's gates come from. |
| `agent-startup-context-gate` | The stage map's Context row is entered "task received" for every slice and names this enforcer (`stage-gate-map.md:16`); the orchestrator's Stage 6 sends each slice through that map and names the gate first among "the enforcers to invoke" (`SKILL.md:252-259`); `ai-sdlc-operating-model/SKILL.md:39` repeats it. Its presence/owner check is the hard stop the install must satisfy (`SKILL.md:84-141`). |
| `change-classification-gate` | Same input 5; owns the class-to-validation-floor matrix the workflow cites (`project-orchestrator/SKILL.md:25-28, 301-302`). |
| `human-approval-boundary` | Orchestrator: "Before anything irreversible … route through `human-approval-boundary`" (`SKILL.md:298-302`). It also carries the copied consumer manual-only policy (`references/consumer-manual-only-policy.md`), which is J1's manual-only rule. |
| `requirements-gathering-facilitator` | Stage 1 owner, invoked by the orchestrator (`SKILL.md:148-173`); J1 step 3. |
| `product-spec-writer` | Stage 2 owner: "ALWAYS begins -> invoke `product-spec-writer`" (`SKILL.md:174`); J1 step 4. |
| `domain-modeler` | Stage 3 first owner (`SKILL.md:239`); J1 design/refinement. |
| `architecture-designer` | Stage 3 owner (`SKILL.md:239`); J1 design/refinement. |
| `tech-spec-writer` | Stage 5 first owner (`SKILL.md:249`); the plan J1 audits is written from it. |
| `phased-work-handoff-designer` | Stage 5 owner (`SKILL.md:249`); the `docs/project-state.md` decision log composes its decision-ID register (`project-state-template.md:25-28`). |
| `plan-of-record-author` | Owns the Stage A plan-of-record (`docs/delivery-workflow.md:98, 106-108`) that J1 step 5 independently audits. |
| `plan-audit-reviewer` | Owns the Stage B plan-level ACCEPT/REVISE audit bound to the captured revision (`docs/delivery-workflow.md:99`). |
| `code-reviewer` | The review lens for Stage D/F (`docs/delivery-workflow.md:101, 103`) and the independent review of J1 step 7. |
| `test-plan-designer` | Stage 7 owner (`SKILL.md:260-261`); J1 step 8's positive/negative cases. |
| `release-readiness-reviewer` | Stage 9 gate (`SKILL.md:278`) and the evidence table J1 step 9 needs for a local delivery; its own contract requires an artifact per blocking dimension or a MISSING entry (`SKILL.md:12-21, 105-110`). |
| `screenshot-evidence-planner` | J1 step 11, **policy half only**. J1 has no UI slice, so step 11 invokes the planner to produce the policy handoff (checkpoints, deterministic naming, pre-storage masking, retention) and nothing is captured; the handoff is recorded as AC-30's policy answer in the evidence record. It captures nothing by contract (`SKILL.md:16`; its Use-When 27-28 hands capture to a manual-only owner). |

The two startup files are `AGENTS.md` (the role-detection and operating contract,
25,228 B) and `CLAUDE.md` (`@AGENTS.md` import plus startup routing, 2,687 B).
Both are required because the role recognition J1 step 2 tests lives in them.

### 2.3 The file list (39 paths, bytes and LF at the base)

Every file is copied byte-identically by the allow-list rule: `SKILL.md` plus
everything under `references/`, plus the two startup files. This is the exact
closure measured at `ffb040c7a363648856475280646bbd142dfabe4e`, sorted by path in
ordinal order (the same order the install-record aggregate uses).

| Path (consumer-relative) | Bytes | LF |
| --- | --- | --- |
| `.claude/skills/agent-startup-context-gate/SKILL.md` | 21084 | 336 |
| `.claude/skills/agent-startup-context-gate/references/context-source-checklist.md` | 3325 | 59 |
| `.claude/skills/agent-startup-context-gate/references/shared-local-resource-coordination.md` | 16797 | 297 |
| `.claude/skills/ai-sdlc-operating-model/SKILL.md` | 9650 | 167 |
| `.claude/skills/ai-sdlc-operating-model/references/stage-gate-map.md` | 5596 | 65 |
| `.claude/skills/architecture-designer/SKILL.md` | 8491 | 158 |
| `.claude/skills/architecture-designer/references/architecture-artifacts.md` | 3110 | 66 |
| `.claude/skills/change-classification-gate/SKILL.md` | 7185 | 141 |
| `.claude/skills/change-classification-gate/references/classification-matrix.md` | 3781 | 49 |
| `.claude/skills/code-reviewer/SKILL.md` | 9404 | 165 |
| `.claude/skills/code-reviewer/references/severity-rubric.md` | 5151 | 86 |
| `.claude/skills/domain-modeler/SKILL.md` | 7031 | 129 |
| `.claude/skills/domain-modeler/references/domain-artifacts.md` | 3737 | 77 |
| `.claude/skills/human-approval-boundary/SKILL.md` | 8301 | 146 |
| `.claude/skills/human-approval-boundary/references/consumer-manual-only-policy.md` | 3764 | 35 |
| `.claude/skills/phased-work-handoff-designer/SKILL.md` | 10070 | 175 |
| `.claude/skills/phased-work-handoff-designer/references/handoff-sheet.md` | 2433 | 80 |
| `.claude/skills/plan-audit-reviewer/SKILL.md` | 7353 | 72 |
| `.claude/skills/plan-audit-reviewer/references/plan-audit-checklist.md` | 2299 | 25 |
| `.claude/skills/plan-of-record-author/SKILL.md` | 6244 | 71 |
| `.claude/skills/plan-of-record-author/references/plan-of-record-package.md` | 1973 | 25 |
| `.claude/skills/product-spec-writer/SKILL.md` | 13519 | 234 |
| `.claude/skills/product-spec-writer/references/product-spec-sheet.md` | 3940 | 111 |
| `.claude/skills/project-orchestrator/SKILL.md` | 42794 | 494 |
| `.claude/skills/project-orchestrator/references/project-state-template.md` | 22454 | 357 |
| `.claude/skills/project-orchestrator/references/recording-and-authority.md` | 10024 | 180 |
| `.claude/skills/release-readiness-reviewer/SKILL.md` | 10663 | 192 |
| `.claude/skills/release-readiness-reviewer/references/readiness-evidence.md` | 3645 | 48 |
| `.claude/skills/requirements-gathering-facilitator/SKILL.md` | 16061 | 271 |
| `.claude/skills/requirements-gathering-facilitator/references/elicitation-sheet.md` | 6524 | 174 |
| `.claude/skills/screenshot-evidence-planner/SKILL.md` | 10878 | 183 |
| `.claude/skills/screenshot-evidence-planner/references/evidence-rules.md` | 3389 | 66 |
| `.claude/skills/tech-spec-writer/SKILL.md` | 10865 | 191 |
| `.claude/skills/tech-spec-writer/references/tech-spec-sheet.md` | 2935 | 72 |
| `.claude/skills/test-plan-designer/SKILL.md` | 9662 | 158 |
| `.claude/skills/test-plan-designer/references/qa-scenario-extensions.md` | 2450 | 32 |
| `.claude/skills/test-plan-designer/references/test-plan-template.md` | 5256 | 77 |
| `AGENTS.md` | 25228 | 231 |
| `CLAUDE.md` | 2687 | 17 |
| **Total: 39 files** | **349753** | **5512** |

Composition: 17 `SKILL.md` + 20 `references/*` files = 37 skill files, plus the 2
startup files. Fourteen skills carry 2 files each; `project-orchestrator`,
`test-plan-designer` and `agent-startup-context-gate` carry 3. There are zero
`assets/`, zero `scripts/` and zero `evals/` files in the list.

Aggregate over these 39 rows, using the algorithm in section 9.2:
`0c885bcd07d62d244da06748e81f006c0f4f93b3fae3cc54f611c7c72218a5a7` over
**5,152 serialized bytes** for **39 rows**. That is the base measurement; your
install record records the same three numbers for the files you actually
installed, and any difference is a finding, not a rounding. The 39 per-file
SHA-256 values are published in the evidence record
(`docs/evidence/consumer-readiness/local-starter-v1.md`, section 4); the
aggregate is their compact, independently pinned form, not a substitute for
inspection.

## 3. How the closure was derived

The dependency definition is the repository validator's own: a link to a sibling
skill's `SKILL.md` is allowed delegation, a link into another skill's internals is a
forbidden file dependency (`scripts/validate-skills.py:1767-1787`), and repo-root
relative citations are outside that rule but must still be classified for a copy
(`scripts/validate-skills.py:1789-1795`).

**Two passes, because a link scan cannot see a routing instruction.**

- **Pass 1 — file links.** For each selected skill, extract every relative link
  and backticked relative path from its `SKILL.md` and `references/*.md`, then
  classify each target: inside its own directory (carried by the allow-list copy);
  a sibling `SKILL.md` (delegation — it resolves because the linked sibling is
  installed); anything else (a repo-root citation, classified below).
- **Pass 2 — stage-map enforcers and the orchestrator's stage lines.** Read both
  routing surfaces: the stage map's Enforcing-skill cell for the inner-lifecycle
  rows (Context, Classify, Plan/approve, Implement, Validate, Review), and the
  orchestrator's stage line for each outer stage J1 traverses — Stage 1
  requirements, Stage 2 product definition, Stage 3 design/refinement
  (`project-orchestrator/SKILL.md:239-240`), Stage 5 planning, Stage 6 build,
  Stage 7 tests, Stage 8/9 local delivery — then classify every named skill as
  installed or excluded with a trigger.

Pass 2 also reads the map's Merge, Close and Learn rows even though J1 stops before
merge, so a consumer who continues past J1 finds every owner already classified
instead of meeting a gap mid-route.

Measured at the base for the 17 selected skills: all file links are intra-skill or
sibling-`SKILL.md` delegation **except five repo-root citations**, all in two
skills. `agent-startup-context-gate` adds none: its three files carry two relative
links, both inside its own directory (`SKILL.md:74, 331`).

| Citation | In | Classification | Why it is not copied |
| --- | --- | --- | --- |
| `../../../docs/skills-catalog.md#…` | `ai-sdlc-operating-model/SKILL.md:21` | Source-repo-bound reference | The catalog is the source library's shipped-skill roster; your inventory is your own `.claude/skills/` directory. J1 needs no catalog file. The link does not resolve in your copy. |
| `../../../docs/paths/design-and-build-ui.md` | `project-orchestrator/SKILL.md` (UI path) | Install-on-demand | UI slices are outside J1. If a J1 slice acquires UI work, this is the first item to install. |
| `../../../docs/paths/add-ai-safely.md` | `project-orchestrator/SKILL.md` (AI path) | Install-on-demand | AI-feature slices are outside J1. |
| `../../../docs/paths/release-with-agents.md` | `project-orchestrator/SKILL.md` (release path) | Install-on-demand | Hosted release is outside J1, which delivers locally. |
| `../../../docs/acceptance/scenario-a-runbook.md` | `project-orchestrator/SKILL.md` (Scenario A findings) | Not a read dependency | A source-repository acceptance record cited as evidence for a finding; nothing in J1 reads it. |

No source-repo-root documentation or support file is copied for J1 except the
two startup files (`AGENTS.md`, `CLAUDE.md`). Deliberately not copied:
`docs/skills-catalog.md`, `docs/paths/*`, `docs/acceptance/*` and every
`docs/evidence/**` page. The copies stay byte-identical — no link rewriting —
because rewriting would change the pinned `SKILL.md` hashes, put a second
divergent copy of routing text in your tree, and break the manifest comparison
that makes the install verifiable. The five non-resolving links are disclosed here
and in your install record.

The source repository's `docs/consumer-contract-manual-only.md` is **not copied,
and J1 never reads it.** Its normative content — the eight rules — is carried by
the copied, verbatim-derived
`human-approval-boundary/references/consumer-manual-only-policy.md` (row 15 of
section 2.3), which is the consumer's authority and the file every consumer
instruction cites (sections 4.1, 10.1 and 11). This is the copy-or-classify rule
applied: the policy is copied in its consumer form, and the source page is
source-repository-bound. A consumer never needs the source page.

The package adds no cross-skill internal links. The sibling links that do exist
are links to a sibling's `SKILL.md`, and every such sibling `SKILL.md` is
installed. A routing mention of a skill that is not installed is not a link and
is classified in section 4. The install procedure's sibling check stops if a
linked sibling `SKILL.md` is absent.

## 4. What is not installed, and how to add it

### 4.1 The exclusion ledger

Nothing outside the package is silently assumed. Each row names the owner, the
trigger and the route. The route is always the same allow-list copy from the same
pinned clone — never a recursive tree copy, which would carry `evals/`.

| Journey step outside J1 | Owning skill(s) not installed | Install-on-demand trigger |
| --- | --- | --- |
| A skills-used record for a consumer PR or ledger | `skill-usage-ledger` | **Deliberately excluded.** Its workflow resolves each name against `tools/skills-manifest.json` and stops on a name that is not there (`SKILL.md:36-51`); that manifest and `scripts/validate-skills.py` are source-repository files this package does not carry, and a consumer install runs no Python. Use your host agent's own report; a consumer that also copies the manifest tooling may install the skill with the allow-list copy. Never present it as a J1 dependency. |
| Stage 2 conditional owners | `prioritization-frame-picker`, `roadmap-under-uncertainty-planner`, `roadmap-to-commitments-translator` | The orchestrator classifies one applicable (competing initiatives, sequencing uncertainty, or a requested date/commitment). A bounded MVP with none of those signals is `n/a` with a reason and does not invoke them (`project-orchestrator/SKILL.md:186-209`). |
| Stage 3 design — the two owners the orchestrator names but J1 does not require | `architecture-advisor`, `adr-writer` | **A routing mention, not a read dependency.** `project-orchestrator/SKILL.md:239-240` routes Stage 3 `domain-modeler` -> `architecture-advisor` -> `architecture-designer` -> `adr-writer`; this package installs the first and the third. Neither excluded skill is a gate, a stop or MANUAL-ONLY, and no packaged skill reads either one's files: `architecture-designer` writes its own ADR **draft** and hands the text over (`architecture-designer/SKILL.md:31, 83, 104, 158`). Trigger: the slice makes a significant architecture decision whose style or paradigm is genuinely open, or a decision must be recorded durably as an ADR -> allow-list copy of `.claude/skills/architecture-advisor/` or `.claude/skills/adr-writer/`, recorded as a DECISION in `docs/project-state.md` before the step runs. Never present either as a J1 dependency. |
| Stage 3 SaaS/multi-tenant and feature-flag families | `saas-platform-architect`, `tenant-modeler`, `multi-tenant-data-architect`, `authorization-matrix-designer`, `feature-flag-architect`, `feature-flag-rollout-strategist` | The approved requirements establish multi-customer data or a staged-rollout need (`project-orchestrator/SKILL.md:239-242`; "invoke by evidence, not by default"). |
| Stage 4 security lenses (AI-runtime family) | `threat-modeler`, `ai-threat-modeler`, `tenant-isolation-reviewer`, `share-link-access-architect`, `file-upload-storage-architect`, `structured-output-validator`, `ai-cost-guardrail-designer`, `agent-harness-architect`, `model-context-designer`, `agentic-loop-designer` | The slice actually has the feature each skill governs (`SKILL.md:243-248`). |
| Work split across several PRs | `ai-task-decomposer` | The change is too big for one reviewable change (`SKILL.md:249-251`). |
| Security review required by the change class | `security-pr-reviewer` | The declared class's review row requires the security lens (stage map's Review row; `change-classification-gate` matrix). |
| QA strategy beyond case design | `qa-strategy-architect` | The project needs a test strategy, not just cases (`SKILL.md:260`). |
| Hosted release (Stage 8 hosted branch) | `cloud-architecture-decider` and the provider/hosted family | Approved requirements establish hosting. J1 uses the local-only branch (`SKILL.md:265`). |
| Release-with-agents route | `risk-tiered-validation-selector`, `sharded-validation-with-resume` | A multi-reviewer release is in scope (`SKILL.md:278-280`). |
| Close — the map's Close row, entered on "merged (or work stopped)" | `ai-closeout-reporter` | The stage map's Close row names it (`stage-gate-map.md:24`) and the orchestrator lists it among the Stage-6 enforcers (`project-orchestrator/SKILL.md:255-259`). J1 stops at local delivery and does not merge, so J1 never enters that row. Trigger: the change is merged or the work is stopped and a closeout report is required, including its "intentionally not done" section -> allow-list copy, recorded as a DECISION before the step runs. Never present it as a J1 dependency. |
| A shared local stack, port, database or fixture set | none | The gate's lock protocol applies only when parallel agents could share a local resource (`SKILL.md:227-249`). J1 is single-agent; on Windows that lane is SKIP/UNRUN by the gate's own platform rule and is never a pass. |
| Any MANUAL-ONLY skill (for example `clickthrough-test-engineer`, `aegis-setup`, `tdd-engineer`, `agent-authorization-matrix`, `ci-pipeline-architect`, `observability-operator`, `prompt-injection-defender`, `playwright-e2e-engineer`) | not installed by v1 at all | A human names the exact skill for the task; the consumer records a trigger-scoped override in its own append-only register before use (`.claude/skills/human-approval-boundary/references/consumer-manual-only-policy.md:19-27`). v1 installs none of them, so the default is a clean refusal, not a latent auto-invocation risk. |

The Stage-3 set is the one place where a default routing chain names owners this
package does not install. For a bounded J1 slice the installed pair produces the
design artifacts J1 uses; the excluded pair is advisory (a style recommendation)
and recording (a durable ADR), and their absence is a named, trigger-scoped
install-on-demand rather than a silent gap.

### 4.2 If the step's owning skill is missing

When the skill that owns a step is not in the package, the fail-closed rule applies:

1. name the step and the owning skill from the table above;
2. state that it is not in the package and why (outside J1);
3. give the exact allow-list copy command and the directory it targets;
4. require the extension to be recorded as a DECISION in `docs/project-state.md`
   before the step runs;
5. **do not** substitute a paraphrase, a different skill, or an `n/a`
   classification to get past a gate. The orchestrator's own input says the owning
   skill "already exists; route to it, do not invent a new procedure"
   (`SKILL.md:81-82, 518-520`), which is why absence must stop the route rather
   than be improvised around.

This rule is also the consumer-side answer when an installed skill's routing text
names one of the excluded skills: the ledger in section 4.1 and this rule are the
instruction to follow, and the copied `SKILL.md` stays byte-identical (section 3)
so it cannot carry a local "not installed" note.

## 5. Package layout in your repository

```text
<product repository>/
  AGENTS.md                                  copied, byte-identical, never overwritten
  CLAUDE.md                                  copied, byte-identical, never overwritten
  .claude/skills/<17 skill directories>/      SKILL.md + references/*.md only
  docs/project-state.md                      created by project-orchestrator at Stage 0 (not copied)
  docs/consumer-install-record.md            written by install step P9 (path/bytes/LF/sha256 x39 + aggregate + source commit)
  docs/consumer-authority-register.md        only if a manual-only override is ever recorded
```

Never present in the package: `evals/`, `evals.json`, `trigger-evals.json`,
`.claude/agents/`, `.claude/settings*.json`, `.claude/commands/`, `.claude/hooks/`,
`.claude-plugin/`, `.mcp.json`, any `scripts/` file, any executable, any
`requirements*.txt`. The startup gate ships with an `evals/` directory upstream;
the allow-list rule excludes it, and the install's eval check fails the run if it
appears inside an installed skill directory. The Python pins in `requirements.txt` belong to the source repository's
own merge gate ("Runtime dependencies for scripts/validate-skills.py — the repo's
merge gate") and are **not** consumer dependencies; a consumer install runs no
Python.

## 6. Before you install: prerequisites

These prerequisites are **observed on one host** — the measured host named in
the evidence record. They are a checklist, not a claim that another host behaves
the same way.

| Dependency | Why it is required | Present on the measured host |
| --- | --- | --- |
| Git (2.x) with network access to github.com | The package is copied from a clone; both identity checks use Git | git 2.55.0.windows.5 |
| **An LF checkout of the pinned commit** | Every pin and the aggregate are computed over LF bytes; a CRLF checkout changes the bytes and the aggregate. The source `.gitattributes:6` is `* text=auto eol=lf`, so a clone checks out LF on every platform. **Do not rely on a default:** a zip export, a copied working tree, or an overridden attribute carries no such guarantee. | `core.autocrlf` is `true` (the Git for Windows common default) and `git ls-files --eol` still reports `w/lf` for all 39 paths, with 0 CRLF bytes — measured 2026-10-27. |
| **A POSIX `sh`, invoked by absolute path** | The startup gate's presence/owner check and its illustrative hook are POSIX `sh` snippets (`agent-startup-context-gate/SKILL.md:117-141, 189-214`); a consumer cannot run the gate's own check without a shell that executes them. Naming the shell is not enough: the invocation must be absolute. | `C:\Program Files\Git\bin\sh.exe` exists and runs (exit 0); `C:\Program Files\Git\usr\bin\sh.exe` is a second candidate. **On this host** `Get-Command sh` is empty (no `sh` on PATH) and `Get-Command bash` resolves to the WindowsApps WSL stub, which fails. A bare `sh -c` therefore throws and a bare `bash -c` fails, so resolve the path in P0 and let P8 verify it executes. The gate's own presence/owner check is run by your host agent at J1 step 2; the install does not run it. |
| PowerShell 7 for the scripted procedure; PowerShell 5.1 for interactive inspection only | The published harness (section 7.1) is a script whose control flow is its exit codes, which requires a script host. | 7.6.6 and 5.1.26100.9711. On this host the 5.1 effective policy is **Restricted**, so a `.ps1` run through `powershell.exe -File` fails at load (exit 1) while the same file under pwsh 7 exits 0. **Do not paste the harness into a 5.1 session:** `exit N` closes the session and the code cannot be observed. Record build 9711 rather than the build documented in the README. |
| A host coding agent that reads `AGENTS.md`/`CLAUDE.md` | The journey runs in the host agent, and the gate is behaviour that agent executes | **DeepSeek Harness (`deepseek-flash`)** — the agent used for the measured run. **Claude Code 2.1.311** was installed at `C:\Users\PeterNguyen\.local\bin\claude.exe` and was present, but it was **not** the agent used. |
| A product repository (Role B), **git-initialised**, with a human owner | The install target; the owner record is `--local` Git config, and a fresh repository may legitimately have **zero commits** | created per run (`git init` if the product repo has no repository yet) |
| Python, Node, pip, any package manager | **Not required.** The Python pins belong to the source merge gate, not to a consumer, and no packaged skill's workflow needs Python | n/a — deliberately not used |

## 7. The install procedure

`$TGT` below is your product repository and `$SRC` is the pinned clone from P3.

**Target scope.** The procedure writes exactly 39 files: the 17 skill
directories, `AGENTS.md` and `CLAUDE.md` — plus
`docs/consumer-install-record.md` when P9 runs. Everything else in `$TGT` — your
`README.md`, source tree, `.gitignore`, your own `.claude/skills/*`, your own
`.claude/settings.json` — is outside the package. It is never read, overwritten
or rejected: P7 and P8 scope every closure, eval and forbidden-material check to
the installed paths. A populated product repository is the supported target; a
`.git`-only repository also works but is not required.

**Platform.** The whole procedure is Windows PowerShell 7 specific: P0 resolves a
Windows `sh.exe`, P5 uses Windows separators and .NET path APIs, and P8 compares
Windows paths. The order and the checks are portable in principle, but **macOS and
Linux are unvalidated** and this package claims nothing there. Run the scripted
procedure under PowerShell 7: its control flow is its exit codes, and a 5.1
interactive paste would close the session instead of reporting a code.

### P0 — Record the host

Record `$PSVersionTable.PSVersion.ToString()`, `git --version`, the resolved `sh`
path and your host agent's version. Resolve the shell explicitly rather than
trusting PATH: test `C:\Program Files\Git\bin\sh.exe`, then
`C:\Program Files\Git\usr\bin\sh.exe`, and if neither exists derive it from
`(Get-Command git).Source` (Git's `cmd\git.exe` sits beside a `bin` and a `usr\bin`
that both carry `sh.exe`). Confirm the resolved path with `& <path> -c 'echo ok'`
and stop if it does not print `ok`; a bare `sh` or `bash` is not a substitute.
These values go into the install record; a run on a different build is a different
environment, not a repeat.

```powershell
$PSVersionTable.PSVersion.ToString()
git --version
$shCandidates = @('C:\Program Files\Git\bin\sh.exe', 'C:\Program Files\Git\usr\bin\sh.exe')
$sh = $shCandidates | Where-Object { Test-Path -LiteralPath $_ } | Select-Object -First 1
if (-not $sh) {
  $gitDir = Split-Path -Parent (Split-Path -Parent (Get-Command git).Source)
  $sh = @((Join-Path $gitDir 'bin\sh.exe'), (Join-Path $gitDir 'usr\bin\sh.exe')) |
        Where-Object { Test-Path -LiteralPath $_ } | Select-Object -First 1
}
if (-not $sh) { [Console]::Error.WriteLine('STOP: no Git sh.exe found'); exit 1 }
& $sh -c 'echo ok'
```

### P1 — Prove the target is a consumer repository, not the library

Run this step **from `$TGT`** (or prefix every probe with
`-LiteralPath (Join-Path $TGT '...')`), so each relative path names a file in the
target and not in whatever directory you happen to be in. The target may be empty
apart from `.git`, or a populated product repository; P1 reads only the four
landmarks and writes nothing.

```powershell
$landmarks = @(
  [bool]((Test-Path -LiteralPath 'README.md') -and
         (Select-String -LiteralPath 'README.md' -Pattern '^# Project Aegis' -Quiet -ErrorAction SilentlyContinue)),
  (Test-Path -LiteralPath 'docs/skills-catalog.md'),
  (Test-Path -LiteralPath 'scripts/validate-skills.py'),
  (Test-Path -LiteralPath 'artifacts/audits/skill-contract-audit-baseline.json'))
$count = @($landmarks | Where-Object { $_ }).Count
```

The guard is part of the contract: a missing `README.md` is a **false** landmark,
not an exception. The decision is exhaustive:

| `$count` | Classification | Exact action | Exact message |
| --- | --- | --- | --- |
| **4** | The source library or a fork of it | **STOP, exit 40**; write nothing | "STOP: this workspace carries all four Project Aegis source-package landmarks, so it is the Project Aegis source library or a fork of it, not an installation target. Install into your own product repository instead. Nothing was changed by this attempt." |
| **1-3** | Genuinely ambiguous | **Ask exactly one role/location question and write nothing**; then act on the answer: "library/fork" -> exit 40; "my product repository" -> continue to P2; no clear answer -> stop | "This workspace has <N> of the four Project Aegis source-package landmarks (<the ones present>). Is it (a) a copy of the Project Aegis source library or a fork of it, or (b) your own product repository? Nothing has been written." |
| **0** | Role B — the consumer/product repository | Continue to P2 | none |

### P2 — Record and verify the two identity records

They are different records with different jobs (section 8).

```powershell
$ownerName  = (git -C $TGT config --local --get aegis.ownerName)  2>$null
$ownerEmail = (git -C $TGT config --local --get aegis.ownerEmail) 2>$null
if ([string]::IsNullOrWhiteSpace($ownerName) -or [string]::IsNullOrWhiteSpace($ownerEmail)) {
  # print the exact section 8.2 remediation text; write nothing
  exit 41
}
$authorLine    = (git -C $TGT var GIT_AUTHOR_IDENT)    2>$null
$committerLine = (git -C $TGT var GIT_COMMITTER_IDENT) 2>$null
# parse 'Name <email> <epoch> <tz>' from each; empty or unparsable -> exit 42
# if either parsed name/email equals the owner record -> print the resolved values,
# ask exactly ONE question, write nothing, exit 42
```

Scope is part of the contract, not an implementation detail: the **owner record is
read with `--local` only** (the gate's own check does the same,
`SKILL.md:117-120, 126-127`), while the **commit identity may come from any
scope** — `git var` is authoritative (`SKILL.md:99-110`). A globally configured
`user.name` therefore satisfies the commit-identity side and can never satisfy the
owner-record side. Do not substitute the installing agent's identity, the source
repository's author, or a placeholder.

The gate's own snippet is a **different layer**: it exits 1 when the commit
identity matches the owner record (`SKILL.md:137-138`), while this procedure's
prerequisite layer exits 42 (section 7.2). A consumer who sees exit 1 from the
gate has a gate refusal, not an install failure.

### P3 — Clone the source at a pinned commit, and prove the checkout

```powershell
$SRC = Join-Path ([IO.Path]::GetTempPath()) ('aegis-src-' + [guid]::NewGuid().ToString('N'))
git clone --no-checkout -c core.autocrlf=false -c core.eol=lf https://github.com/ModernNomad-98/Project-Aegis.git $SRC
git -C $SRC checkout --detach ffb040c7a363648856475280646bbd142dfabe4e
$head = ((& git -C $SRC rev-parse HEAD) -join '').Trim()
$tree = ((& git -C $SRC rev-parse 'HEAD^{tree}') -join '').Trim()
if ($head -ne 'ffb040c7a363648856475280646bbd142dfabe4e') { [Console]::Error.WriteLine("exit 31: HEAD $head is not the pinned commit"); exit 31 }
if ($tree -ne '88a5aee4ad928a49c2fb945032585843ec652da7') { [Console]::Error.WriteLine("exit 31: tree $tree is not the pinned tree"); exit 31 }
if (@(git -C $SRC status --porcelain).Count) { [Console]::Error.WriteLine('exit 31: the source clone is not clean'); exit 31 }
$badEol = @(git -C $SRC ls-files --eol -- AGENTS.md CLAUDE.md .claude/skills | Where-Object { $_ -match 'w/crlf' })
if ($badEol.Count) { [Console]::Error.WriteLine('exit 31: CRLF checkout: ' + $badEol[0]); exit 31 }
```

A unique temporary directory is used so a pre-created `$env:TEMP/aegis-src`
cannot be mistaken for the clone, and the checkout is **proven** — commit, tree
and a clean status — before anything is copied. The commit is the one your install
record will name; never `main` for a verification run, because the identities in
section 2 are measured at a commit.

**Line endings are part of the pin.** Every pin and the aggregate are computed
over LF bytes. The source repository's `.gitattributes:6` is `* text=auto eol=lf`
at the pinned commit, so a clone checks out LF even where Git for Windows sets
`core.autocrlf=true` — measured on 2026-10-27: `core.autocrlf` was `true` and
`git ls-files --eol` still reported `w/lf` for all 39 paths, with 0 CRLF bytes.
That is a property of the attribute, **not of the defaults**: a zip export, a
copied working tree, or an overridden attribute carries no guarantee. Clone with
the two `-c` flags above, fail closed on the `ls-files --eol` check, and rely on
the harness's byte-level CRLF check after the copy (`exit 31`).

### P4 — Name the package

The copy list is the 39 paths in section 2.3. The loop is driven by that list,
never by a directory enumeration of `.claude/skills`. The published harness in
section 7.1 carries the list as `$package`; a mistyped row changes the row count
or the aggregate, and both fail closed.

### P5 — Destination pre-checks (before any write)

The runnable implementation of P5-P9 is the harness in section 7.1; the bullets
below state what each step requires and why. The pre-checks run in this order and
before anything is written:

- **Scope.** Only the 17 destination skill directories (`.claude/skills/<name>`) and
  the two startup files are examined. A file elsewhere in your repository is never
  considered, so a populated product repository is a supported target.
- **Existing skill directories are resume-or-refuse.** A directory that already
  exists is accepted only when every file in it is one of that skill's packaged
  files and byte-identical to the pinned source — an install interrupted mid-copy
  then resumes. A file outside the package is refused as foreign material
  (**exit 20**); a byte that differs is refused as a pin mismatch (**exit 31**).
  Both name the file. This keeps the established `A20-E-DEST-EXISTS` semantics —
  the destination is the skill directory `$root\<skill-name>`, not a file inside
  it — while making a partial install recoverable instead of permanently blocked.
- **Source paths fail closed.** Every packaged path must exist; must contain no
  `..` segment; must not be a reparse point at the leaf **or at any parent
  segment** (the check walks `.claude`, `.claude/skills`, the skill directory and
  `references/`); and must resolve inside the clone (**exit 21**).
- **Startup files never overwrite.** An existing `AGENTS.md`/`CLAUDE.md` that
  differs byte-wise from the source is refused (**exit 22**); an identical one is
  accepted and counted, and is re-checked at copy time rather than trusted from
  P5.
- **Paths are normalized before comparison.** `$SRC` and `$TGT` are made absolute
  with no trailing separator, the package list is matched case-sensitively
  (`-cnotin`), and the aggregate's row order is ordinal — a relative or
  trailing-separator target cannot make every file look foreign, and a
  culture-aware sort cannot reorder the rows.

### P6 — Copy by allow-list only, then the startup files

Per selected skill: create the directory, copy `SKILL.md`, then every file under
`references/`, preserving the relative path; nothing else. Then copy the two
startup files to the target root — `AGENTS.md` -> `<target>/AGENTS.md` and
`CLAUDE.md` -> `<target>/CLAUDE.md` — byte-identically. Fourteen skills
contribute 2 files and three contribute 3, so the copy leaves 37 skill files plus
2 startup files. Nothing is ever deleted, so the procedure cannot damage an
existing tree, and an existing file is **never overwritten**: it is skipped only
after its hash matches the pinned source, so an interrupted run resumes where it
stopped.

### P7 — Refuse eval material, scoped to the installed skills

After the copy, a directory or file named `evals`, `evals.json` or
`trigger-evals.json` anywhere **inside the 17 installed skill directories** fails
the run (**exit 30**) and is named. A directory named `evals` is caught as well as
the eval files; your own unrelated skills and files elsewhere are not scanned.
This is the established verifier's semantics, including its stated limit: the check
runs after the write, so a contaminated *source* would be copied first and
reported. Remove it (with the human's approval, because deletion is a boundary)
before retrying.

### P8 — Verify the closure and the pins, against independent values

The published harness in section 7.1 implements every check and exits nonzero on
the first failure:

1. **Count and scope:** exactly 39 packaged files present, and under the 17
   installed skill directories no file outside the list (**exit 30**); 37 skill
   files plus the 2 startup files.
2. **Skill pins:** each of the 17 `SKILL.md` files, with CRLF->LF normalization,
   equals its `tools/skills-manifest.json` entry (**exit 31**).
3. **Reference and startup pins:** each of the 20 reference files and the 2
   startup files matches the pinned source, after P3 has proven the source is the
   pinned commit and tree and is clean (**exit 31**).
4. **Siblings:** every sibling `SKILL.md` linked by an installed skill exists in
   the destination (**exit 32**).
5. **No forbidden material:** no eval material, `scripts/`, executable or other
   file outside the package inside an installed skill directory (**exit 30**).
6. **Startup shell:** the recorded `sh` executes `echo ok` (**exit 1**). The
   gate's own presence/owner check is a J1 step, not an install check.

**The independent anchor is the aggregate, not the destination.** Checks 2 and 3
compare the destination with the same clone used for copying, so on their own they
prove only internal consistency. P8 therefore recomputes the aggregate over the
installed 39 rows and **fails closed unless it equals the published
`0c885bcd07d62d244da06748e81f006c0f4f93b3fae3cc54f611c7c72218a5a7` over 5,152
serialized bytes and 39 rows**, and P3/P8 verify `git rev-parse HEAD` and
`HEAD^{tree}` against the pinned commit and tree before trusting any source-side
pin. A contaminated clone that does not reproduce the published aggregate does not
pass.

### P9 — Write the consumer install record

The harness writes `docs/consumer-install-record.md` when given `-RecordPath`.
The record contains the source commit and tree; the date; the PowerShell, Git and
`sh` versions; the owner record's **presence only** (never its value); the 39
rows (path, bytes, LF, SHA-256) in ordinal order; the aggregate with its row count
and serialized byte length; the five disclosed non-resolving repo-root links
(section 3); and the rule that a later mismatch is a stop. Without `-RecordPath`
the harness still prints the three aggregate numbers. Then hand over to your host
agent: the front door reads `docs/project-state.md` first, finds none, proposes
the cold-start document, and begins Stage 0.

### 7.1 The published harness (P5-P9, runnable as written)

Save the block below as `install-starter.ps1` and run it under PowerShell 7:

```powershell
pwsh -NoProfile -File .\install-starter.ps1 -Src C:\path\to\pinned-clone -Tgt C:\path\to\product -Sh 'C:\Program Files\Git\bin\sh.exe' -RecordPath C:\path\to\product\docs\consumer-install-record.md
```

It is a complete, runnable form of P5-P9: the failure paths write to stderr and
`exit`, never `Write-Error`, so an inherited `$ErrorActionPreference = 'Stop'`
cannot turn a documented code into exit 1. It defines `$package` (the 39 paths)
and takes `$Src`, `$Tgt`, `$Sh` and `-RecordPath` as parameters; it writes
nothing outside the 39 package paths and the install record.

```powershell
param(
  [Parameter(Mandatory)][string]$Src,
  [Parameter(Mandatory)][string]$Tgt,
  [string]$Sh = 'C:\Program Files\Git\bin\sh.exe',
  [string]$RecordPath
)
# Published P5-P9 harness for docs/consumer-starter-package.md (v1).
# Requires PowerShell 7. Failure paths write to stderr and exit; they never use
# Write-Error, so an inherited $ErrorActionPreference = 'Stop' cannot turn a
# documented exit code into exit 1.
$ErrorActionPreference = 'Stop'
$PinCommit = 'ffb040c7a363648856475280646bbd142dfabe4e'
$PinTree   = '88a5aee4ad928a49c2fb945032585843ec652da7'
$AggSha    = '0c885bcd07d62d244da06748e81f006c0f4f93b3fae3cc54f611c7c72218a5a7'
$AggRows   = 39
$AggBytes  = 5152

function Stop-Step([int]$Code, [string]$Message) {
  [Console]::Error.WriteLine(('exit {0}: {1}' -f $Code, $Message))
  exit $Code
}

$Tgt = [IO.Path]::GetFullPath($Tgt).TrimEnd([IO.Path]::DirectorySeparatorChar)
$Src = [IO.Path]::GetFullPath($Src).TrimEnd([IO.Path]::DirectorySeparatorChar)
if (-not (Test-Path -LiteralPath $Tgt -PathType Container)) { Stop-Step 1 "target not found: $Tgt" }
if (-not (Test-Path -LiteralPath $Src -PathType Container)) { Stop-Step 1 "source clone not found: $Src" }

# P4 - the 39-path package list, transcribed from section 2.3 (ordinal order).
$package = @(
  '.claude/skills/agent-startup-context-gate/SKILL.md'
  '.claude/skills/agent-startup-context-gate/references/context-source-checklist.md'
  '.claude/skills/agent-startup-context-gate/references/shared-local-resource-coordination.md'
  '.claude/skills/ai-sdlc-operating-model/SKILL.md'
  '.claude/skills/ai-sdlc-operating-model/references/stage-gate-map.md'
  '.claude/skills/architecture-designer/SKILL.md'
  '.claude/skills/architecture-designer/references/architecture-artifacts.md'
  '.claude/skills/change-classification-gate/SKILL.md'
  '.claude/skills/change-classification-gate/references/classification-matrix.md'
  '.claude/skills/code-reviewer/SKILL.md'
  '.claude/skills/code-reviewer/references/severity-rubric.md'
  '.claude/skills/domain-modeler/SKILL.md'
  '.claude/skills/domain-modeler/references/domain-artifacts.md'
  '.claude/skills/human-approval-boundary/SKILL.md'
  '.claude/skills/human-approval-boundary/references/consumer-manual-only-policy.md'
  '.claude/skills/phased-work-handoff-designer/SKILL.md'
  '.claude/skills/phased-work-handoff-designer/references/handoff-sheet.md'
  '.claude/skills/plan-audit-reviewer/SKILL.md'
  '.claude/skills/plan-audit-reviewer/references/plan-audit-checklist.md'
  '.claude/skills/plan-of-record-author/SKILL.md'
  '.claude/skills/plan-of-record-author/references/plan-of-record-package.md'
  '.claude/skills/product-spec-writer/SKILL.md'
  '.claude/skills/product-spec-writer/references/product-spec-sheet.md'
  '.claude/skills/project-orchestrator/SKILL.md'
  '.claude/skills/project-orchestrator/references/project-state-template.md'
  '.claude/skills/project-orchestrator/references/recording-and-authority.md'
  '.claude/skills/release-readiness-reviewer/SKILL.md'
  '.claude/skills/release-readiness-reviewer/references/readiness-evidence.md'
  '.claude/skills/requirements-gathering-facilitator/SKILL.md'
  '.claude/skills/requirements-gathering-facilitator/references/elicitation-sheet.md'
  '.claude/skills/screenshot-evidence-planner/SKILL.md'
  '.claude/skills/screenshot-evidence-planner/references/evidence-rules.md'
  '.claude/skills/tech-spec-writer/SKILL.md'
  '.claude/skills/tech-spec-writer/references/tech-spec-sheet.md'
  '.claude/skills/test-plan-designer/SKILL.md'
  '.claude/skills/test-plan-designer/references/qa-scenario-extensions.md'
  '.claude/skills/test-plan-designer/references/test-plan-template.md'
  'AGENTS.md'
  'CLAUDE.md'
)
if ($package.Count -ne 39) { Stop-Step 31 "package list has $($package.Count) rows, expected 39" }
$skillDirs = @($package | Where-Object { $_ -like '.claude/skills/*' } |
  ForEach-Object { ($_ -split '/')[0..2] -join '/' } | Sort-Object -Unique)
if ($skillDirs.Count -ne 17) { Stop-Step 31 "package list yields $($skillDirs.Count) skill directories, expected 17" }

# P3 identity - the clone must be the pinned commit/tree and clean.
$head = (& git -C $Src rev-parse HEAD 2>$null | Out-String).Trim()
$tree = (& git -C $Src rev-parse 'HEAD^{tree}' 2>$null | Out-String).Trim()
$dirty = @(& git -C $Src status --porcelain 2>$null)
if ($head -ne $PinCommit) { Stop-Step 31 "source HEAD $head is not the pinned commit $PinCommit" }
if ($tree -ne $PinTree) { Stop-Step 31 "source tree $tree is not the pinned tree $PinTree" }
if ($dirty.Count) { Stop-Step 31 "source clone is not clean: $($dirty[0])" }

function Get-FileSha256([string]$Path) {
  $sha = [Security.Cryptography.SHA256]::Create()
  try { return ([BitConverter]::ToString($sha.ComputeHash([IO.File]::ReadAllBytes($Path)))).Replace('-','').ToLowerInvariant() }
  finally { $sha.Dispose() }
}
function Get-LfCount([byte[]]$Bytes) { return @($Bytes | Where-Object { $_ -eq 10 }).Count }
function Get-CrCount([byte[]]$Bytes) { return @($Bytes | Where-Object { $_ -eq 13 }).Count }

# P5 - destination pre-checks. An existing skill directory is accepted only as a
# resume of a prior partial install: every file already there must be one of that
# skill's packaged files and byte-identical to the pinned source.
foreach ($rel in $package) {
  if ($rel -match '(^|/)\.\.(/|$)') { Stop-Step 21 "unsafe source path $rel" }
  $srcPath = Join-Path $Src ($rel -replace '/', [IO.Path]::DirectorySeparatorChar)
  if (-not (Test-Path -LiteralPath $srcPath -PathType Leaf)) { Stop-Step 21 "missing source file: $srcPath" }
  $segments = @(($rel -split '/') | Select-Object -SkipLast 1)
  $walk = $Src
  foreach ($seg in $segments) {
    $walk = Join-Path $walk $seg
    $parentItem = Get-Item -LiteralPath $walk -Force -ErrorAction Stop
    if ($parentItem.Attributes -band [IO.FileAttributes]::ReparsePoint) { Stop-Step 21 "reparse-point source segment: $walk" }
  }
  $leafItem = Get-Item -LiteralPath $srcPath -Force -ErrorAction Stop
  if ($leafItem.Attributes -band [IO.FileAttributes]::ReparsePoint) { Stop-Step 21 "reparse-point source: $srcPath" }
  $resolved = (Resolve-Path -LiteralPath $srcPath).ProviderPath
  $srcPrefix = $Src + [IO.Path]::DirectorySeparatorChar
  if (-not $resolved.StartsWith($srcPrefix, [StringComparison]::OrdinalIgnoreCase)) {
    Stop-Step 21 "source resolves outside the clone: $resolved"
  }
}
foreach ($rel in $skillDirs) {
  $dst = Join-Path $Tgt ($rel -replace '/', [IO.Path]::DirectorySeparatorChar)
  if (-not (Test-Path -LiteralPath $dst)) { continue }
  $existing = @(Get-ChildItem -LiteralPath $dst -Recurse -Force -File -ErrorAction Stop)
  foreach ($file in $existing) {
    $candidate = $file.FullName.Substring($Tgt.Length + 1).Replace('\','/')
    if ($candidate -cnotin $package) { Stop-Step 20 "existing skill directory holds a file outside the package: $candidate" }
    $sourceHash = Get-FileSha256 (Join-Path $Src ($candidate -replace '/', [IO.Path]::DirectorySeparatorChar))
    if ((Get-FileSha256 $file.FullName) -ne $sourceHash) { Stop-Step 31 "existing installed file differs from the pinned source: $candidate" }
  }
}
foreach ($rel in 'AGENTS.md','CLAUDE.md') {
  $dst = Join-Path $Tgt $rel
  if (Test-Path -LiteralPath $dst) {
    if ((Get-FileSha256 $dst) -ne (Get-FileSha256 (Join-Path $Src $rel))) { Stop-Step 22 "startup file differs: $dst" }
  }
}

# P6 - copy by allow-list only. Existing identical files are skipped, never
# overwritten, so a partial install resumes instead of blocking every retry.
foreach ($rel in $package) {
  $srcPath = Join-Path $Src ($rel -replace '/', [IO.Path]::DirectorySeparatorChar)
  $dst = Join-Path $Tgt ($rel -replace '/', [IO.Path]::DirectorySeparatorChar)
  $parent = Split-Path -Parent $dst
  if (-not (Test-Path -LiteralPath $parent)) { New-Item -ItemType Directory -Path $parent | Out-Null }
  if (Test-Path -LiteralPath $dst) {
    if ((Get-FileSha256 $dst) -eq (Get-FileSha256 $srcPath)) { continue }
    if ($rel -cnotin 'AGENTS.md','CLAUDE.md') { Stop-Step 20 "$dst appeared after P5 and differs from the pinned source" }
    Stop-Step 22 "startup file changed during the copy: $dst"
  }
  Copy-Item -LiteralPath $srcPath -Destination $dst -ErrorAction Stop
}

# P7 - eval material, scoped to the 17 installed skill directories. A directory
# named evals is caught as well as the eval files. Unrelated files elsewhere in
# the target are outside the install and are neither read nor rejected.
foreach ($dir in $skillDirs) {
  $full = Join-Path $Tgt ($dir -replace '/', [IO.Path]::DirectorySeparatorChar)
  $bad = @(Get-ChildItem -LiteralPath $full -Recurse -Force -ErrorAction Stop |
    Where-Object { $_.Name -in 'evals','evals.json','trigger-evals.json' })
  if ($bad.Count) { Stop-Step 30 "eval material present: $($bad[0].FullName)" }
}

# P8 - closure, pins, siblings, forbidden material and the independent aggregate.
$rows = New-Object System.Collections.Generic.List[object]
$missing = @($package | Where-Object {
  -not (Test-Path -LiteralPath (Join-Path $Tgt ($_ -replace '/', [IO.Path]::DirectorySeparatorChar)) -PathType Leaf)
})
if ($missing.Count) { Stop-Step 30 "missing $($missing.Count) of 39: $($missing[0])" }

$extra = @()
foreach ($dir in $skillDirs) {
  $full = Join-Path $Tgt ($dir -replace '/', [IO.Path]::DirectorySeparatorChar)
  foreach ($file in @(Get-ChildItem -LiteralPath $full -Recurse -Force -File -ErrorAction Stop)) {
    $candidate = $file.FullName.Substring($Tgt.Length + 1).Replace('\','/')
    if ($candidate -cnotin $package) { $extra += $candidate }
  }
}
if ($extra.Count) { Stop-Step 30 "file outside the package in an installed skill directory: $($extra[0])" }

$installedSkillFiles = 0
foreach ($dir in $skillDirs) {
  $full = Join-Path $Tgt ($dir -replace '/', [IO.Path]::DirectorySeparatorChar)
  $installedSkillFiles += @(Get-ChildItem -LiteralPath $full -Recurse -Force -File -ErrorAction Stop).Count
}
if ($installedSkillFiles -ne 37) { Stop-Step 30 "installed skill files: $installedSkillFiles, expected 37 (39 paths minus the 2 startup files)" }

foreach ($rel in $package) {
  $dst = Join-Path $Tgt ($rel -replace '/', [IO.Path]::DirectorySeparatorChar)
  $bytes = [IO.File]::ReadAllBytes($dst)
  if ((Get-CrCount $bytes) -ne 0) { Stop-Step 31 "CRLF bytes in $rel - the aggregate and pins are LF-based" }
  $item = Get-Item -LiteralPath $dst -Force
  $rows.Add([pscustomobject]@{
    Path = $rel; Bytes = $item.Length; LF = (Get-LfCount $bytes); SHA256 = (Get-FileSha256 $dst)
  })
}
$ordered = @($rows | Sort-Object -Property Path -CaseSensitive)
# Ordinal sort: culture-aware ordering is not acceptable for the aggregate.
$paths = [string[]]@($ordered | ForEach-Object { $_.Path })
[Array]::Sort($paths, [System.StringComparer]::Ordinal)
$sb = New-Object System.Text.StringBuilder
$byPath = @{}
foreach ($r in $ordered) { $byPath[$r.Path] = $r }
foreach ($p in $paths) {
  $r = $byPath[$p]
  [void]$sb.Append(('{0}' -f $r.Path) + [char]9 + ('{0}' -f $r.Bytes) + [char]9 + ('{0}' -f $r.LF) + [char]9 + $r.SHA256 + [char]10)
}
$serialized = [Text.Encoding]::UTF8.GetBytes($sb.ToString())
$sha = [Security.Cryptography.SHA256]::Create()
try { $aggregate = ([BitConverter]::ToString($sha.ComputeHash($serialized))).Replace('-','').ToLowerInvariant() }
finally { $sha.Dispose() }
if ($rows.Count -ne $AggRows) { Stop-Step 31 "aggregate rows: $($rows.Count), expected $AggRows" }
if ($serialized.Length -ne $AggBytes) { Stop-Step 31 "serialized bytes: $($serialized.Length), expected $AggBytes" }
if ($aggregate -ne $AggSha) { Stop-Step 31 "aggregate $aggregate does not match the published $AggSha" }

$manifest = Get-Content -LiteralPath (Join-Path $Src 'tools/skills-manifest.json') -Raw | ConvertFrom-Json
$manifestPins = 0
foreach ($rel in ($package | Where-Object { $_ -like '.claude/skills/*/SKILL.md' })) {
  $skill = ($rel -split '/')[2]
  $entry = @($manifest.skills | Where-Object { $_.name -eq $skill })
  if ($entry.Count -ne 1) { Stop-Step 31 "no unique manifest entry for $skill" }
  $dst = Join-Path $Tgt ($rel -replace '/', [IO.Path]::DirectorySeparatorChar)
  $text = [Text.Encoding]::UTF8.GetString([IO.File]::ReadAllBytes($dst)).Replace(([string][char]13 + [char]10), [string][char]10)
  $h = [Security.Cryptography.SHA256]::Create()
  try { $actual = ([BitConverter]::ToString($h.ComputeHash([Text.Encoding]::UTF8.GetBytes($text)))).Replace('-','').ToLowerInvariant() }
  finally { $h.Dispose() }
  if ($actual -ne $entry[0].sha256) { Stop-Step 31 "manifest pin mismatch: $rel" }
  $manifestPins++
}

$sourcePins = 0
foreach ($rel in ($package | Where-Object { $_ -notlike '.claude/skills/*/SKILL.md' })) {
  $dst = Join-Path $Tgt ($rel -replace '/', [IO.Path]::DirectorySeparatorChar)
  $srcFile = Join-Path $Src ($rel -replace '/', [IO.Path]::DirectorySeparatorChar)
  if ((Get-FileSha256 $dst) -ne (Get-FileSha256 $srcFile)) { Stop-Step 31 "source pin mismatch: $rel" }
  $sourcePins++
}
if ($manifestPins -ne 17 -or $sourcePins -ne 22) { Stop-Step 31 "pin counts $manifestPins/$sourcePins, expected 17/22" }

$siblingMissing = @()
foreach ($rel in ($package | Where-Object { $_ -like '.claude/skills/*' })) {
  $dst = Join-Path $Tgt ($rel -replace '/', [IO.Path]::DirectorySeparatorChar)
  $text = Get-Content -LiteralPath $dst -Raw
  foreach ($m in [regex]::Matches($text, '\.\./([a-z0-9-]+)/SKILL\.md')) {
    $sibling = $m.Groups[1].Value
    if (-not (Test-Path -LiteralPath (Join-Path (Join-Path $Tgt '.claude\skills') (Join-Path $sibling 'SKILL.md')) -PathType Leaf)) {
      $siblingMissing += ('{0} links {1}/SKILL.md' -f (($rel -split '/')[2]), $sibling)
    }
  }
}
if ($siblingMissing.Count) { Stop-Step 32 "missing sibling SKILL.md: $($siblingMissing -join '; ')" }

if (-not (Test-Path -LiteralPath $Sh -PathType Leaf)) { Stop-Step 1 "no sh at $Sh" }
$shOut = (& $Sh -c 'echo ok' 2>$null | Out-String).Trim()
if ($LASTEXITCODE -ne 0 -or $shOut -ne 'ok') { Stop-Step 1 "sh did not answer: $Sh" }

Write-Output ('P8: count_check=PASS installed={0} extra=0' -f $rows.Count)
Write-Output ('P8: manifest_pins=PASS {0}/{0}' -f $manifestPins)
Write-Output ('P8: source_pins=PASS {0}/{0}' -f $sourcePins)
Write-Output 'P8: siblings=PASS absent=0'
Write-Output 'P8: forbidden=PASS none'
Write-Output ('P9: rows={0} serialized_bytes={1} aggregate={2} (matches the published value)' -f $rows.Count, $serialized.Length, $aggregate)
if ($RecordPath) {
  $RecordPath = [IO.Path]::GetFullPath($RecordPath)
  if (Test-Path -LiteralPath $RecordPath) {
    Write-Output "P9: install record already present, left unchanged: $RecordPath"
  } else {
    $record = New-Object System.Text.StringBuilder
    $ownerName = (& git -C $Tgt config --local --get aegis.ownerName 2>$null)
    $ownerEmail = (& git -C $Tgt config --local --get aegis.ownerEmail 2>$null)
    $ownerPresent = 'absent - P2 (exit 41) stops before an install; this harness does not enforce P2; values never recorded'
    if ($ownerName -and $ownerEmail) { $ownerPresent = 'present on both keys (values not recorded)' }
    elseif ($ownerName -or $ownerEmail) { $ownerPresent = 'incomplete - one key missing; P2 (exit 41) stops before an install; values never recorded' }
    $branch = (& git -C $Src symbolic-ref -q --short HEAD 2>$null)
    $headState = 'detached HEAD'
    if ($branch) { $headState = 'on branch ' + $branch }
    [void]$record.AppendLine('# Consumer install record - starter package v1')
    [void]$record.AppendLine('')
    [void]$record.AppendLine('- Source: ModernNomad-98/Project-Aegis at commit ' + $head + ' (tree ' + $tree + '), ' + $headState + ', clean.')
    [void]$record.AppendLine('- Installed: ' + (Get-Date -Format 'yyyy-MM-ddTHH:mm:ssK'))
    [void]$record.AppendLine('- Tools: PowerShell ' + $PSVersionTable.PSVersion.ToString() + '; ' + ((& git --version) -join '').Trim() + '; sh ' + $Sh)
    [void]$record.AppendLine('- Owner record: ' + $ownerPresent)
    [void]$record.AppendLine('- Rows: 39; serialized bytes: ' + $serialized.Length + '; aggregate: ' + $aggregate)
    [void]$record.AppendLine('- Result: P5-P8 exit 0. A later mismatch in any row is a stop, not a warning.')
    [void]$record.AppendLine('- Five non-resolving source-repo citations are disclosed in docs/consumer-starter-package.md section 3: docs/skills-catalog.md, docs/paths/design-and-build-ui.md, docs/paths/add-ai-safely.md, docs/paths/release-with-agents.md, docs/acceptance/scenario-a-runbook.md')
    [void]$record.AppendLine('')
    [void]$record.AppendLine('| Path (consumer-relative) | Bytes | LF | SHA-256 |')
    [void]$record.AppendLine('| --- | --- | --- | --- |')
    foreach ($pth in $paths) {
      $r = $byPath[$pth]
      [void]$record.AppendLine(('| {0} | {1} | {2} | {3} |' -f $r.Path, $r.Bytes, $r.LF, $r.SHA256))
    }
    $recordDir = Split-Path -Parent $RecordPath
    if (-not (Test-Path -LiteralPath $recordDir)) { New-Item -ItemType Directory -Path $recordDir | Out-Null }
    [IO.File]::WriteAllText($RecordPath, $record.ToString(), (New-Object Text.UTF8Encoding($false)))
    Write-Output "P9: install record written: $RecordPath"
  }
}
Write-Output 'OK: 39 installed files; closure, pins, siblings, eval and aggregate checks passed'
exit 0
```

If `-RecordPath` already exists, the block prints the path and leaves the file
unchanged - it never overwrites a record - so choose a new path for a fresh one.

**Verified, not illustrative.** The block was extracted from this page and run on
2026-10-27 against (a) a fresh local clone of the pinned commit `ffb040c7` and
(b) a populated target containing `README.md`, `.gitignore`, a source directory,
an unrelated skill directory and `.claude/settings.json`. Result: exit 0; 39
installed files; 17/17 manifest pins; 22/22 source pins; 0 missing siblings;
aggregate `0c885bcd...a5a7` over 5,152 bytes; install record written and **6,586 B**.
The block was re-extracted and re-run on 2026-10-27 after the P9 record line above
was corrected; that run also recorded `present on both keys` on a target that
carries both `aegis.*` keys, and `on branch <name>` on a clone checked out to a
branch. Negative runs: one changed byte in an installed reference -> **exit 31**
naming that file; an `evals/` directory inside an installed skill -> **exit 30**; a
second run on the completed target -> **exit 0** (resume), and a run whose
`-RecordPath` already exists also exits 0 and reports the record left unchanged.
The command, outputs and the extraction method are recorded in the fix-round
evidence record. The Stage E
validation used a larger harness that is not part of this repository; this page now
carries its own executable form, so a reader does not have to take the checks on
trust.

### 7.2 Exit codes

Each code stops; none warns and continues.

| Code | Meaning | What you see |
| --- | --- | --- |
| 1 | Prerequisite failure | `STOP: no Git sh.exe found`, a missing source/target clone, or a `sh` that did not answer. The source/target checks run before any write. The published harness probes `sh` at the end of P8, so that path stops **after** the 39 files are written - the install is resumable from there and no record is written |
| 20 | Foreign material in a destination skill directory | The exact file that is outside the package; nothing overwritten |
| 21 | Unsafe or missing source path | The `..`/reparse-point segment or the missing file; nothing written |
| 22 | Startup-file conflict | The differing file; existing bytes unchanged |
| 30 | Closure, count or eval-material failure | The offending path or the count found |
| 31 | Pin or byte mismatch (including a CRLF checkout or an aggregate mismatch) | The exact file, or the aggregate comparison that failed |
| 32 | Missing sibling dependency | The installed skill that links it and the absent sibling it names, as `<skill> links <sibling>/SKILL.md` |
| 40 | Wrong repository role | The four-landmark stop message (P1) |
| 41 | Owner record missing | The exact `aegis.*` remediation text (section 8.2) |
| 42 | Commit identity missing or owner-matching | The resolved author/committer values and one question (section 8.3). This is the **prerequisite layer**; the gate's own snippet exits **1** for the same owner match (`SKILL.md:137-138`), so a gate refusal is not an install failure |

## 8. The two identity records

### 8.1 What "owner" means

The human who authorizes: the person the Aegis route calls "you" and the actor an
`A-*` approval names. The owner is **not** the source repository's owner and
**not** the agent.

| Record | Keys | Scope that counts | What it is for | Who reads it |
| --- | --- | --- | --- | --- |
| **Owner record** | `aegis.ownerName`, `aegis.ownerEmail` | `--local` **only** — the gate reads these with `git config --local` (`SKILL.md:117-120, 126-127`) | Names the human every approval belongs to; never committed; the identity the gate refuses to see commit | The gate's presence/owner check before the first commit (`SKILL.md:126-141`) |
| **Commit identity** | `user.name`, `user.email` (any scope; `git var` is authoritative) | local, global, `GIT_AUTHOR_*`/`GIT_COMMITTER_*`, `GIT_CONFIG_*`, or `git -c` (`SKILL.md:99-110`) | Signs the commit | Git, and the gate, which compares it with the owner record and **refuses a match on either name or email** (`SKILL.md:105-110, 137, 209-211`) |

The approval record stays separate from both: `docs/project-state.md` carries the
role ("project owner") and the approval ID, because the schema forbids identifying
people in the committed file ("No secrets, no live identifiers … never by
credential or real name") and the manual-only contract forbids personal data in its
register. The install record therefore stores only the owner record's **presence**
(not its value): never the name, the email address or any hash of it.

### 8.2 If the owner record is absent (exit 41)

Stop before writing anything, then show exactly this and nothing else:

```text
The starter package records who owns this repository, because every approval in
docs/project-state.md names the person who authorized it. No owner record exists in
this repository's local Git configuration.

Set it for this repository only (it is never committed):
  git config --local aegis.ownerName  "Your Name"
  git config --local aegis.ownerEmail "you@example.com"

These two keys are the record the startup gate reads before your first commit.
Your user.name and user.email are a different record: they sign the commits, and the
gate refuses a commit whose identity matches the owner on either name or email.

Then run the installation again. Nothing was changed by this attempt.
```

Never proceed with an invented identity; never reuse the source repository's
committer; never write the installing agent's name; never set identity on the
human's behalf without their words.

### 8.3 If the commit identity is missing or matches the owner (exit 42)

Show the resolved values and ask **exactly one** question:

> Git reports this repository's author and committer as `<name> <email>`, which is the recorded owner. Should the agent commit under a different identity for this repository, or will you commit yourself?

Then:

- If the human names a distinct agent identity, set it **only with their words**,
  for that repository (`git config --local user.name` / `user.email`), and re-run
  P2; a passing run prints the resolved author and committer and continues.
- If the human says they will commit themselves, stop the install and say plainly
  that the gate will refuse a commit whose identity is the owner's — the same
  exit-42 condition — so a distinct identity is still needed for any commit made in
  this repository.
- If the answer is unclear, do not guess and do not write.

**A solo consumer is the normal case, and it is the hard case.** If the owner's
name and email are the same as the machine's Git identity, every commit in that
repository is refused — including the owner's own. The documented workaround is a
repository-local **agent** identity (a name and email that are not the owner's)
used for the agent's commits, with the owner record keeping the human's own values.
That workaround is the gate's fail-closed rule, not this package's policy invention.

#### Owner decision still needed (review row 6)

**This package does not decide the solo-owner policy, and it does not invent one.**
The open question is whether a solo owner may commit under their own identity —
which the gate refuses — or must use a repository-local agent identity. Two
answers are on the table, and only the repository owner can choose:

1. **Owner commits are allowed**; only agent commits must differ from the owner,
   with the gate changed to distinguish the acting identity from the owner record.
2. **The agent identity is the supported solo flow**, with exact per-command
   identity commands documented and the gate left fail-closed.

Until that decision is recorded, the shipped behaviour is the gate's fail-closed
refusal: exit 42 at this prerequisite layer and exit 1 at the gate. The package is
therefore **not consumer-ready**, and the evidence record does not claim it is. No
instruction in this page grants an exception, and a consumer must not treat the
workaround as an approved policy.

## 9. The install record and its aggregate

The install record is the consumer's own artifact. It is not the source
repository's evidence and does not replace the separate acceptance record.

### 9.1 What it contains

- The source commit **and tree**, and the date.
- The tool versions from P0 and the resolved `sh` path.
- One row per installed file: consumer-relative path, bytes, LF count, SHA-256.
- The aggregate and its three published numbers (rows, serialized bytes, SHA-256).
- The five non-resolving repo-root links disclosed in section 3.
- The owner record's presence (not its value).
- The statement that a later mismatch is a stop.

The section 7.1 harness writes this file when given `-RecordPath`, so the record
is produced by the same run that passed the checks; it is not retyped by hand.

### 9.2 The aggregate algorithm

The aggregate is a SHA-256 over a byte-exact serialization, so two operators can
reproduce it:

1. **Row set.** One row per installed file: all 39 package paths, consumer
   relative, using `/` separators (no leading `./`).
2. **Row fields, in this order:** `path`, `bytes` (decimal, no padding), `lf`
   (decimal count of `0x0A` bytes), `sha256` (lowercase hex, 64 chars).
3. **Separators:** one TAB (`0x09`) between fields, one LF (`0x0A`) after the last
   field of each row, including the final row. No header, no trailing blank line,
   no spaces.
4. **Sort order:** paths in **ordinal** (byte-wise, case-sensitive) order —
   `[Array]::Sort($paths, [System.StringComparer]::Ordinal)` in PowerShell,
   `LC_ALL=C sort` in a POSIX shell. Culture-aware sorts are not acceptable: they
   order differently on different hosts.
5. **Encoding:** UTF-8 with no BOM. All paths are ASCII, so the serialization is
   stable.
6. **Aggregate:** SHA-256 of the concatenated serialization, lowercase hex,
   published with the row count and the serialization byte length
   (`rows=39`, `serialized_bytes=5152` at the base) so a mismatch is diagnosable by
   inspection.
7. **Base value (commit `ffb040c7`):**
   `0c885bcd07d62d244da06748e81f006c0f4f93b3fae3cc54f611c7c72218a5a7` over
   **5,152** serialized bytes for **39** rows.

The section 7.1 harness computes this exact serialization and **compares it
fail-closed** with the base value above; it exits 31 on a row-count,
serialized-length or hash difference, naming the first row that breaks a check.
A mismatch is a finding, not a rounding.

The arithmetic makes the length checkable: the 39 consumer-relative paths total
2,233 bytes and the 39 full 64-character digests total 2,496 bytes, so 4,729 bytes
is the minimum before separators; adding three TABs per row (117), one LF per row
(39) and the decimal fields (267 characters across the `bytes` and `lf` columns)
gives exactly 5,152.

## 10. Recording authority on the consumer route

### 10.1 Precedence

Highest first, applied in your product repository:

1. **A current direct human instruction in this session** for this exact action.
   Existing authorization stays effective and is transcribed rather than
   re-requested. **For a MANUAL-ONLY skill, the instruction is not sufficient by
   itself:** the exact skill name, reason, trigger, scope and date are transcribed
   into your own append-only register before invocation
   (`.claude/skills/human-approval-boundary/references/consumer-manual-only-policy.md:19-23`),
   or the skill is not invoked.
2. **An effectively ACTIVE consumer-local grant** — an `A-*` entry in
   `docs/project-state.md` whose allowed scope names the action, the exact path
   and the exact content hash, with its full lifecycle history considered.
3. **A trigger-scoped manual-only override** in your own append-only register —
   valid only for exactly the named MANUAL-ONLY skill, the named trigger, the
   current pin and the recorded scope; revoked or un-re-pinned means invalid
   (`.claude/skills/human-approval-boundary/references/consumer-manual-only-policy.md:23-27`).
4. **The skill default**: preview the exact path and byte-for-byte content, ask
   once, append only after the yes.
5. **Never**: a source-repository register entry. `AEGIS-APR-*` grants apply to
   `ModernNomad-98/Project-Aegis` and do not transfer to any other repository. A
   consumer that cites one is claiming authority it does not have.

### 10.2 Preservation and denial

- **Valid scoped-authority reuse is preserved.** A grant whose scope, path and
  content hash match is used without asking again, and the reasoning entry names
  the grant ID. Reuse never widens the wording.
- **Stale, revoked, consumed or superseded authority is denied — hard.** A later
  lifecycle event governs; revoking a successor never revives a predecessor;
  historical `ACTIVE` text is never sufficient.
- **Changed content is denied.** Any byte change between the previewed content and
  the write invalidates the authorization and needs a new preview and approval.
  Implementation authority is never inferred from scope, spec or design acceptance.
- **Grant verification is independent of the writer.** A grant is verified
  independently of the actor that writes the state file; the DECISION entry records
  the grant ID, the content hash compared, and that independent verification
  result. A writing agent may not verify its own grant and then cite its own
  verification. **Solo-consumer reading:** in a one-agent product repository the
  human's content-specific yes to that exact path and content is the check that
  stands in for independent verification - human confirmation, not a second
  independent agent - and the DECISION entry records it as human confirmation.
  An agent's self-verification is never recorded as one.
- **Missing owner is a stop, not a default.** No owner record -> exit 41; no
  acceptable commit identity -> exit 42 (section 8). No covering grant -> stop and
  request one. No owning skill -> stop and name the install (section 4.2).

### 10.3 Two records, one domain split

The override register governs only manual-only triggers; `A-*` entries govern
everything else. Where they overlap, the later lifecycle event wins. That ordering
is this package's reading of two documents that do not address each other; if the
case is genuinely unclear, stop and ask rather than picking one.

### 10.4 What a consumer must never import

No file from `docs/approvals/`, no `AEGIS-APR-*` text, no source-repository
configuration, and no source-repository landmark or validator installation that
would make your product repository look like the library — specifically, do not
install the four landmarks P1 probes for, the source `scripts/` tree, or the
source repository's own configuration. The two startup files `AGENTS.md` and
`CLAUDE.md` **are** installed deliberately (section 2.2); this rule does not
exclude them. The package contains no approval record of any kind; the copy never
reads the register, and a source-repository grant is never authority in your
repository.

## 11. Screenshot evidence: policy versus capture

Policy is a design act; capture is an action that creates new data about a real
screen. v1 installs only the policy side.

| Side | Owner | What it may do | What it must not do |
| --- | --- | --- | --- |
| Policy | `screenshot-evidence-planner` (installed) | Decide which checkpoints are evidence-worthy, the deterministic naming convention, mandatory pre-storage masking (block-out, not blur), per-capture metadata, storage/retention/access, linkage to cases/PRs/closeout, capture-quality rules | Capture, store or delete any evidence (`SKILL.md:16, 58-102, 137`) |
| Execution — screen clickthrough | `clickthrough-test-engineer` — **MANUAL-ONLY**, not installed | Run the authorized clickthrough pass under the policy | Be auto-applied, chained, preloaded or simulated; be replaced by a paraphrased procedure (`.claude/skills/human-approval-boundary/references/consumer-manual-only-policy.md:11, 35`; planner Use-When 27-28 and hand-off stop condition 173-174) |
| Execution — browser/Playwright screenshot capture | `playwright-e2e-engineer` — **MANUAL-ONLY**, not installed | Capture the screenshot/Playwright artifacts the policy defines | Same prohibitions; it is a *different* owner from the clickthrough case, and each action needs that owner's own authority |

**Handoff rules.**

1. The policy is written first, as your own file, and a capture run must cite it.
2. Captures are never taken before masking exists, because "evidence is stored
   masked or not stored" (`screenshot-evidence-planner/SKILL.md:139-147`).
3. A capture request is answered with the exact MANUAL-ONLY skill name for that
   evidence type and the requirement that a human name it and that a trigger-scoped
   override be recorded first — or with a refusal.
4. The planner's own owner-question rule applies if checkpoints, storage or
   retention are undecided (`SKILL.md:65-71, 84-96`), and its answer sets policy
   only, never authorization to capture.

In J1 there is no UI slice, so the honest record is: **the planner is invoked for
the policy half only** — it produces the policy handoff (checkpoints, naming,
masking, retention) that AC-30 records — with **no captures in J1**; the capture
case is UNRUN with the exact remaining action (a human names the MANUAL-ONLY
executor for the evidence type and records the override). The 39-file set
therefore includes the planner as a policy dependency, not as a capture
dependency. The measured host has no Playwright runner and the
local GUI answers unauthenticated, so even outside J1 a capture claim would be
UNRUN until a runner exists or an authenticated context is supplied. That is never
a pass.

## 12. Limits, and how to report them

- **The package is complete for J1 only** (section 1.2). Anything else is a stop
  with the owning skill named, never an improvisation.
- **No machine enforcement of the selection.** Nothing checks that the 17-skill
  list is still the right minimum; the derivation rule, the install checks and this
  disclosure are the mitigation. A future change to the package needs a new
  measurement, not a memory.
- **Five links do not resolve in your copy** (section 3), by design: rewriting them
  would change pinned bytes. The install record lists them.
- **One host is one host.** The measured acceptance evidence covers one Windows
  machine, one slice and J1. macOS and Linux remain not validated.
- **The solo-owner commit-identity policy is an open owner decision**
  (section 8.3). The package ships the gate's fail-closed behaviour and asserts no
  policy; that is one reason it makes no consumer-readiness claim.
- **The startup gate is behaviour, not a boundary** (section 1.3): it can be
  bypassed by anyone who chooses to, and its Windows lock lane is SKIP/UNRUN.
- **The install record is evidence of identity, not a signature or a tamper-proof
  seal.** The manifest and the per-file source pins come from the same checkout;
  the independent anchors are the pinned commit/tree and the published aggregate,
  which P8 compares fail-closed (section 7.1).
- **Report UNRUN as UNRUN.** A check that was skipped, blocked by host policy, or
  not applicable is recorded with its exact remaining action; it is never converted
  to a pass.

If an installation or a later check fails, record the exact command, the exit code,
the message and the state it left behind. A failed or partial result is evidence; a
softened one is not.
