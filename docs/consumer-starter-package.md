# Consumer starter package (v1)

Status: **normative definition of the v1 consumer starter package.** This page
defines one fixed, dependency-checked installation for a beginner's first product
slice. It is measured against the Project Aegis source tree at commit
`ffb040c7a363648856475280646bbd142dfabe4e` (tree
`88a5aee4ad928a49c2fb945032585843ec652da7`). It does not itself record an
installation, a test run or an acceptance result: the first native-host acceptance
record is produced separately, after the run it describes, and nothing here is
evidence that the procedure has already been executed on your machine.

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

1. install into a fresh consumer repository (section 7);
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

The package is **complete for J1** under two rules that are checked, not asserted:

1. every file J1's documented workflow reads is either copied or classified in
   section 4 with the reason it is not needed; and
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
- This package installs files; it does not run your project, choose your
  technology, or approve anything. Approvals remain the human's.

**Not claimed by this package:** production readiness, multi-tenant or SaaS
readiness, a second host, a hosted deployment, live-model evaluation, CI-green
equivalence, or "complete native consumer testing". One host's evidence is bounded
to that host and that run.

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
| `project-orchestrator` | The front door and stage detector; the startup routing hands the beginner to it (`CLAUDE.md` startup item 3; `README.md:715-725`). Its Capability 4 owns the `docs/project-state.md` write loop (`SKILL.md:309-332`). |
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
| `screenshot-evidence-planner` | J1 step 11 and the policy half of the screenshot handoff. It captures nothing by contract (`SKILL.md:16`; Use-When 27-28 hands capture to a manual-only owner). |

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
installed, and any difference is a finding, not a rounding.

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
  a sibling `SKILL.md` (delegation — it resolves because every named sibling is
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

No source-repo-root file is copied for J1. Deliberately not copied:
`docs/skills-catalog.md`, `docs/paths/*`, `docs/acceptance/*` and every
`docs/evidence/**` page. The copies stay byte-identical — no link rewriting —
because rewriting would change the pinned `SKILL.md` hashes, put a second
divergent copy of routing text in your tree, and break the manifest comparison
that makes the install verifiable. The five non-resolving links are disclosed here
and in your install record.

The package adds no cross-skill internal links. The sibling links that do exist
resolve because every named sibling is installed; the install procedure's
dependency check stops if a named sibling `SKILL.md` is absent.

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
| Stage 4 security lenses | `threat-modeler`, `ai-threat-modeler`, `tenant-isolation-reviewer`, `share-link-access-architect`, `file-upload-storage-architect`, `structured-output-validator`, `ai-cost-guardrail-designer`, `agent-harness-architect`, `model-context-designer`, `agentic-loop-designer` | The slice actually has the feature each skill governs (`SKILL.md:243-248`). |
| Work split across several PRs | `ai-task-decomposer` | The change is too big for one reviewable change (`SKILL.md:249-251`). |
| Security review required by the change class | `security-pr-reviewer` | The declared class's review row requires the security lens (stage map's Review row; `change-classification-gate` matrix). |
| QA strategy beyond case design | `qa-strategy-architect` | The project needs a test strategy, not just cases (`SKILL.md:260`). |
| Hosted release (Stage 8 hosted branch) | `cloud-architecture-decider` and the provider/hosted family | Approved requirements establish hosting. J1 uses the local-only branch (`SKILL.md:265`). |
| Release-with-agents route | `risk-tiered-validation-selector`, `sharded-validation-with-resume` | A multi-reviewer release is in scope (`SKILL.md:278-280`). |
| Close — the map's Close row, entered on "merged (or work stopped)" | `ai-closeout-reporter` | The stage map's Close row names it (`stage-gate-map.md:24`) and the orchestrator lists it among the Stage-6 enforcers (`project-orchestrator/SKILL.md:255-259`). J1 stops at local delivery and does not merge, so J1 never enters that row. Trigger: the change is merged or the work is stopped and a closeout report is required, including its "intentionally not done" section -> allow-list copy, recorded as a DECISION before the step runs. Never present it as a J1 dependency. |
| A shared local stack, port, database or fixture set | none | The gate's lock protocol applies only when parallel agents could share a local resource (`SKILL.md:227-249`). J1 is single-agent; on Windows that lane is SKIP/UNRUN by the gate's own platform rule and is never a pass. |
| Any MANUAL-ONLY skill (for example `clickthrough-test-engineer`, `aegis-setup`, `tdd-engineer`, `agent-authorization-matrix`, `ci-pipeline-architect`, `observability-operator`, `prompt-injection-defender`, `playwright-e2e-engineer`) | not installed by v1 at all | A human names the exact skill for the task; the consumer records a trigger-scoped override in its own append-only register before use (`docs/consumer-contract-manual-only.md:5-15`). v1 installs none of them, so the default is a clean refusal, not a latent auto-invocation risk. |

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
appears. The Python pins in `requirements.txt` belong to the source repository's
own merge gate ("Runtime dependencies for scripts/validate-skills.py — the repo's
merge gate") and are **not** consumer dependencies; a consumer install runs no
Python.

## 6. Before you install: prerequisites

| Dependency | Why it is required | Present on the measured host |
| --- | --- | --- |
| Git (2.x) with network access to github.com | The package is copied from a clone; both identity checks use Git | git 2.55.0.windows.5 |
| **A POSIX `sh`, invoked by absolute path** | The startup gate's presence/owner check and its illustrative hook are POSIX `sh` snippets (`agent-startup-context-gate/SKILL.md:117-141, 189-214`); a consumer cannot run the gate's own check without a shell that executes them. Naming the shell is not enough: the invocation must be absolute. | `C:\Program Files\Git\bin\sh.exe` exists and runs (exit 0); `C:\Program Files\Git\usr\bin\sh.exe` is a second candidate. **On this host** `Get-Command sh` is empty (no `sh` on PATH) and `Get-Command bash` resolves to the WindowsApps WSL stub, which fails. A bare `sh -c` therefore throws and a bare `bash -c` fails, so resolve the path in P0 and use it in P8. |
| PowerShell 7 for scripted runs; PowerShell 5.1 only **pasted** into an interactive session | The documented copy/verifier block is PowerShell, and the two hosts differ in what they will load | 7.6.6 and 5.1.26100.9711. On this host the 5.1 effective policy is **Restricted**, so a `.ps1` run through `powershell.exe -File` fails at load (exit 1) while the same file under pwsh 7 exits 0: script it under 7, or paste it into a 5.1 session, and record build 9711 rather than the build documented in the README. |
| A host coding agent that reads `AGENTS.md`/`CLAUDE.md` | The journey runs in the host agent, and the gate is behaviour that agent executes | Claude Code 2.1.311 |
| A product repository (Role B), **git-initialised**, with a human owner | The install target; the owner record is `--local` Git config, and a fresh repository may legitimately have **zero commits** | created per run (`git init` if the product repo has no repository yet) |
| Python, Node, pip, any package manager | **Not required.** The Python pins belong to the source merge gate, not to a consumer, and no packaged skill's workflow needs Python | n/a — deliberately not used |

## 7. The install procedure

`$TGT` below is your product repository. The steps are written for Windows
PowerShell; the same order applies elsewhere, and P6's copy loop is the only
platform-specific part (the repository's own POSIX copy variant is marked "NOT
validated on macOS or Linux", and this package does not extend that claim). The
gate's own check runs under `sh`; on Windows that is the `sh.exe` resolved in P0.

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
if (-not $sh) { Write-Error 'STOP: no Git sh.exe found'; exit 1 }
& $sh -c 'echo ok'
```

### P1 — Prove the target is a consumer repository, not the library

Run this step **from `$TGT`** (or prefix every probe with
`-LiteralPath (Join-Path $TGT '...')`), so each relative path names a file in the
target and not in whatever directory you happen to be in. The target may be empty
apart from `.git`.

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

### P3 — Clone the source at a pinned commit

```powershell
git clone --no-checkout https://github.com/ModernNomad-98/Project-Aegis.git "$env:TEMP/aegis-src"
git -C "$env:TEMP/aegis-src" checkout --detach ffb040c7a363648856475280646bbd142dfabe4e
```

The commit is the one your install record will name; never `main` for a
verification run, because the identities in section 2 are measured at a commit.

### P4 — Name the package

The copy list is the 39 paths in section 2.3. The loop is driven by that list,
never by a directory enumeration of `.claude/skills`.

### P5 — Destination pre-checks (before any write)

The pre-checks run in this order and before anything is written:

- none of the **17 destination skill directories** (`.claude/skills/<name>`) may
  exist: each directory is refused whole, so the installer never merges into a
  skill directory a beginner has already copied by hand (**exit 20**, matching
  the established `A20-E-DEST-EXISTS` semantics at `README.md:530-535`, where
  `$dst` is the skill directory `$root\<skill-name>`, not a file inside it);
- a source path must contain no `..` segment, must not be a reparse
  point/symlink, and must resolve inside the clone (**exit 21**);
- an existing `AGENTS.md`/`CLAUDE.md` that differs byte-wise from the source is
  never overwritten (**exit 22**), while an identical one is accepted and
  counted. The two startup files are deliberately outside the directory check
  above, so this branch is reachable.

```powershell
# The 17 skill directories, derived from the 39-path list; the 2 startup files
# are excluded so their identical case reaches the exit-22 branch below.
$skillDirs = @($package |
  Where-Object { $_ -like '.claude/skills/*' } |
  ForEach-Object { ($_ -split '/')[0..2] -join '/' } |
  Sort-Object -Unique)
foreach ($rel in $skillDirs) {
  $dst = Join-Path $TGT $rel
  if (Test-Path -LiteralPath $dst) {
    Write-Error "exit 20: refusing to install over an existing skill directory: $dst"; exit 20
  }
}
foreach ($rel in $package) {
  if ($rel -match '(^|/)\.\.(/|$)') { Write-Error "exit 21: unsafe source path $rel"; exit 21 }
  $srcPath = Join-Path $SRC $rel
  $item = Get-Item -LiteralPath $srcPath -Force
  if ($item.Attributes -band [IO.FileAttributes]::ReparsePoint) {
    Write-Error "exit 21: reparse-point source $srcPath"; exit 21
  }
  $srcFull = [IO.Path]::GetFullPath($srcPath)
  if (-not $srcFull.StartsWith(([IO.Path]::GetFullPath($SRC) + [IO.Path]::DirectorySeparatorChar), [StringComparison]::OrdinalIgnoreCase)) {
    Write-Error "exit 21: source resolves outside the clone: $srcFull"; exit 21
  }
}
foreach ($rel in 'AGENTS.md', 'CLAUDE.md') {
  $dst = Join-Path $TGT $rel
  if (Test-Path -LiteralPath $dst) {
    $a = (Get-FileHash -LiteralPath $dst -Algorithm SHA256).Hash
    $b = (Get-FileHash -LiteralPath (Join-Path $SRC $rel) -Algorithm SHA256).Hash
    if ($a -ne $b) { Write-Error "exit 22: startup file differs: $dst"; exit 22 }
  }
}
```

### P6 — Copy by allow-list only, then the startup files

Per selected skill: create the directory (without `-Force`), copy `SKILL.md`, then
every file under `references/`, preserving the relative path; nothing else. Then
copy the two startup files to the target root — `AGENTS.md` -> `<target>/AGENTS.md`
and `CLAUDE.md` -> `<target>/CLAUDE.md` — byte-identically and **never overwriting
an existing file**. Fourteen skills contribute 2 files, three contribute 3, so the
copy leaves 37 skill files plus 2 startup files. Nothing is ever deleted, so the
procedure cannot damage an existing tree.

```powershell
foreach ($rel in $package) {
  $dst = Join-Path $TGT $rel
  $parent = Split-Path -Parent $dst
  if (-not (Test-Path -LiteralPath $parent)) { New-Item -ItemType Directory -Path $parent | Out-Null }
  if (Test-Path -LiteralPath $dst) {
    # only the two identical startup files may already exist
    if ($rel -notin 'AGENTS.md','CLAUDE.md') { Write-Error "exit 20: $dst appeared after P5"; exit 20 }
    continue
  }
  Copy-Item -LiteralPath (Join-Path $SRC $rel) -Destination $dst
}
```

### P7 — Refuse eval material

After the copy, any file named `evals`, `evals.json` or `trigger-evals.json`
anywhere in the destination fails the run (**exit 30**) and the file is named.
This is the established verifier's semantics, including its stated limit: the check
runs after the write, so a contaminated *source* would be copied first and
reported. Remove it (with the human's approval, because deletion is a boundary)
before retrying.

```powershell
$bad = @(Get-ChildItem -LiteralPath $TGT -Recurse -Force -File |
         Where-Object { $_.Name -in 'evals','evals.json','trigger-evals.json' })
if ($bad.Count) { Write-Error "exit 30: eval material present: $($bad[0].FullName)"; exit 30 }
```

### P8 — Verify the closure and the pins

1. **Count:** exactly **39** installed files and no path outside the list
   (**exit 30**).
2. **Skill pins:** each `SKILL.md` SHA-256, with CRLF->LF normalization, equals its
   `tools/skills-manifest.json` entry (**exit 31**).
3. **Reference and startup pins:** each of the 20 reference files and the 2 startup
   files matches its source SHA-256 (**exit 31**).
4. **Siblings:** every sibling `SKILL.md` named by an installed skill exists in the
   destination (**exit 32**).
5. **No forbidden material:** no `scripts/`, no executable, no `.claude/agents`, no
   settings/hooks/plugin files (**exit 30**).

```powershell
$missing = @($package | Where-Object { -not (Test-Path -LiteralPath (Join-Path $TGT $_)) })
if ($missing.Count) { Write-Error "exit 30: missing $($missing.Count) of 39: $($missing[0])"; exit 30 }
$extra = @(Get-ChildItem -LiteralPath $TGT -Recurse -Force -File |
           Where-Object { $_.FullName -notlike "*\.git\*" } |
           ForEach-Object { $_.FullName.Substring($TGT.Length + 1).Replace('\','/') } |
           Where-Object { $_ -notin $package -and $_ -ne 'docs/consumer-install-record.md' })
if ($extra.Count) { Write-Error "exit 30: file outside the package: $($extra[0])"; exit 30 }
# Then compare each file's SHA-256 with the source (startup files and references),
# and each SKILL.md with its manifest entry using CRLF->LF normalized bytes.
```

### P9 — Write the consumer install record

Write `docs/consumer-install-record.md` in your product repository. It records:
the source commit; tool versions; the resolved `sh` path; the date; the **39 rows**
(path, bytes, LF, SHA-256) in ordinal order; the aggregate computed by section 9.2
together with its three published numbers; the five disclosed non-resolving
repo-root links (section 3); the owner record's presence (not its value); and the
rule that a later mismatch is a stop. Then hand over to your host agent: the front
door reads `docs/project-state.md` first, finds none, proposes the cold-start
document, and begins Stage 0.

### 7.1 Exit codes

Each code stops; none warns and continues.

| Code | Meaning | What you see |
| --- | --- | --- |
| 1 | Prerequisite failure | `STOP: no Git sh.exe found`; nothing written |
| 20 | Destination skill directory exists | The skill directory that already exists; nothing written |
| 21 | Unsafe source path | The `..`/reparse-point segment; nothing written |
| 22 | Startup-file conflict | The differing file; existing bytes unchanged |
| 30 | Closure, count or eval-material failure | The offending path or the count found |
| 31 | Pin mismatch | The exact file whose SHA-256 differs |
| 32 | Missing sibling dependency | The installed skill that names the absent sibling |
| 40 | Wrong repository role | The four-landmark stop message |
| 41 | Owner record missing | The exact `aegis.*` remediation text (section 8.2) |
| 42 | Commit identity missing or owner-matching | The resolved author/committer values and one question (section 8.3) |

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
repository is refused — including the owner's own. The documented resolution is a
repository-local **agent** identity (a name and email that are not the owner's)
used for the agent's commits, with the owner record keeping the human's own values.
That resolution is the gate's rule, not this package's invention; whether a solo
consumer should instead be allowed to commit as the owner is an open policy
question, and the gate's fail-closed behaviour is the default until it is answered.

## 9. The install record and its aggregate

The install record is the consumer's own artifact. It is not the source
repository's evidence and does not replace the separate acceptance record.

### 9.1 What it contains

- The source commit and the date.
- The tool versions from P0 and the resolved `sh` path.
- One row per installed file: consumer-relative path, bytes, LF count, SHA-256.
- The aggregate and its three published numbers (rows, serialized bytes, SHA-256).
- The five non-resolving repo-root links disclosed in section 3.
- The owner record's presence (not its value).
- The statement that a later mismatch is a stop.

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
   re-requested.
2. **An effectively ACTIVE consumer-local grant** — an `A-*` entry in
   `docs/project-state.md` whose allowed scope names the action, the exact path
   and the exact content hash, with its full lifecycle history considered.
3. **A trigger-scoped manual-only override** in your own append-only register —
   valid only for exactly the named MANUAL-ONLY skill, the named trigger, the
   current pin and the recorded scope; revoked or un-re-pinned means invalid
   (`docs/consumer-contract-manual-only.md:9-15`).
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
  independent verifier is the human — their own content-specific yes to that exact
  path and content is the independent check, and the DECISION entry records that
  the human verified it. An agent's self-verification is never recorded as one.
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
configuration, and no `AGENTS.md`/validator installation that would make your
product repository look like the library. The package contains no approval record
of any kind; the copy never reads the register, and a source-repository grant is
never authority in your repository.

## 11. Screenshot evidence: policy versus capture

Policy is a design act; capture is an action that creates new data about a real
screen. v1 installs only the policy side.

| Side | Owner | What it may do | What it must not do |
| --- | --- | --- | --- |
| Policy | `screenshot-evidence-planner` (installed) | Decide which checkpoints are evidence-worthy, the deterministic naming convention, mandatory pre-storage masking (block-out, not blur), per-capture metadata, storage/retention/access, linkage to cases/PRs/closeout, capture-quality rules | Capture, store or delete any evidence (`SKILL.md:16, 58-102, 137`) |
| Execution — screen clickthrough | `clickthrough-test-engineer` — **MANUAL-ONLY**, not installed | Run the authorized clickthrough pass under the policy | Be auto-applied, chained, preloaded or simulated; be replaced by a paraphrased procedure (`docs/consumer-contract-manual-only.md:5-15`; planner Use-When 27-28 and hand-off stop condition 173-174) |
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

In J1 there is no UI slice, so the honest record is: policy produced when your
first UI slice exists; **no captures in J1**; the capture case is UNRUN with the
exact remaining action (a human names the MANUAL-ONLY executor for the evidence
type and records the override). The measured host has no Playwright runner and the
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
- **The startup gate is behaviour, not a boundary** (section 1.3): it can be
  bypassed by anyone who chooses to, and its Windows lock lane is SKIP/UNRUN.
- **The install record is evidence of identity, not a signature or a tamper-proof
  seal.** The clone and the manifest come from the same checkout.
- **Report UNRUN as UNRUN.** A check that was skipped, blocked by host policy, or
  not applicable is recorded with its exact remaining action; it is never converted
  to a pass.

If an installation or a later check fails, record the exact command, the exit code,
the message and the state it left behind. A failed or partial result is evidence; a
softened one is not.
