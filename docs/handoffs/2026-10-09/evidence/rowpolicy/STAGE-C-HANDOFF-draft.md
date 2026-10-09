# ROWPOLICY-1 Stage C — implementation handoff (draft; SD-C INCOMPLETE)

Holder: `/root/rowpolicy_impl`, Stage C only. Start UTC: 2026-10-08 21:15:44.0377100Z. Initial active-work estimate: 45–75 minutes; active time is not separately measured. Finish, wall time and immutable H/tree/B are pending.

## Binding inputs and classification

- PLAN-rev1 SHA-256: `adb968cdbad28215fb261f8a8b90f4e202cc8874f903fc0f6d8965bde65aad63` (Get-FileHash, current turn).
- Corrected independent Stage B audit SHA-256: `912ca4cc55c7566f13dc2baaca032929612b8cd66e14776c2fbe59bfd75a32be` (Get-FileHash, current turn); it says `SD-B: ACCEPT` for that exact plan hash. The earlier audit digest is superseded.
- Classification: ai-agentic governance instruction change in `docs/delivery-workflow.md` and `.github/pull_request_template.md`; two documentary records. Security answer for eventual PR: **Yes — `.github/pull_request_template.md` and `docs/approvals/APPROVAL_REGISTER.md`** under CONTRIBUTING. This maintainer/agent work does not make MG5's outside-only additional review applicable.
- Exact final PR path contract: `docs/delivery-workflow.md`, `.github/pull_request_template.md`, `docs/approvals/APPROVAL_REGISTER.md`, `docs/reconciliation/step-0-reconciliation-v4.md`.
- Fresh read-only `gh api repos/ModernNomad-98/Project-Aegis/branches/main --jq .commit.sha` returned `5228977920ee479e1fe1ec6b8d56f8fc24c14947` at about 21:18 UTC on 2026-10-08. Open `gh pr list` returned #682 at `a33aa2a...` and #681 at `c76114e...`; `gh pr view --json files` showed neither currently edits the register or reconciliation. Recheck for final allocation and before publication; CIFIX still has prior claim on the expected next APR ID.

## Current candidate and intentional hold

- Isolated checkout: `C:\src\Codex Projects\Project Aegis\rowpolicy\implementation`, branch `docs/rowpolicy-1-sourced-skills-rows`, base `5228977920ee479e1fe1ec6b8d56f8fc24c14947`. The dirty source clone `C:\src\Project Aegis\Project-Aegis` was read only and retains pre-existing `artifacts/recovery/` and `artifacts/reviews/` untracked state.
- Modified in candidate so far: workflow, PR template, reconciliation. The D entry now uses **provisional D74** after coordinator confirmation that CIFIX P-REG is register-only; uniqueness must be refreshed before commit. Register is **unmodified**; proposed append text is at `rowpolicy/PROPOSED-APR-entry.md` outside the Git candidate, with no assigned APR ID.
- No commit, push, PR or provider write. Hold until coordinator confirms CIFIX ordering, current main and record IDs. Then replace D-TBD, append the approved APR entry at EOF, run final checks and commit only the exact four paths with DCO sign-off.
- Intentionally not touched: AGENTS.md, CLAUDE.md, CONTRIBUTING.md, scripts, CI, skills, protected enforcement files, evaluation, VM, ISO, Stage 4B and provider surfaces.

## Rule-preservation inventory at current uncommitted candidate

1. Seven stage names, order, distinct-holder rule, stage table exit-ID column and chain rule are unedited; the only SD-block diff is the SD-F source-verification pointer/clause.
2. `git`/Python byte-slice comparison of the base and candidate found `MG` block, dependency block, receipt block and bound-fields block equal (`True` each). Exact-head and bound-field invalidation text remain intact.
3. Handoff block adds only a self-authored row/source pointer. Skills chapter holds one new row-content/provenance protocol and replaces the literal ambiguous bullet. Agreement-check ownership list adds only that skills block with row-content scope. The template points there and retains its four-column header.
   `git diff --unified=0 -- docs/delivery-workflow.md | rg '^\+[^+].*(MG[1-5]|SD-[A-G])'` returned only the changed `SD-F` table row; the new protocol has no second ID-bearing condition text.
4. `AGENTS.md`, `CLAUDE.md`, CONTRIBUTING.md, D72 and APR-105 have no candidate diff. The AGENTS summary reread has green exact-head/exception at lines 92–95, final review at 70, review wait at 95, merge authority at 97–100, and outside-only security scope at 73; it still has no P1/P2 automated-review triage text. The final PR divergence table must record marker-by-marker command output.
5. Template whole-line marker extraction returned exactly six existing sentinels in order: skills/end, security/end, witness/end. Exactly one four-column skills table header. No new sentinel or bound field.
6. D-entry byte proof so far: base prefix before `## 6. Post-merge corrections` is 300091 bytes and suffix from that heading is 6769 bytes; both are unchanged, with a 1098-byte insertion between them. D74 uniqueness and its APR link remain pending.
7. Register prefix proof, exact owner question/label, unique ID and four-path B...H diff remain pending until allocation and commit. No old register bytes have been edited.

## Proven invocations so far

| Command | Observed result |
| --- | --- |
| `python -B -P scripts/validate-skills.py` | Exit 0; `OK: 195 skill(s) valid, 0 warning(s)` |
| `python -B -P scripts/tests/test_validator.py` | Exit 0; `OK: 181 gate self-test assertion(s) passed.` |
| `python -B -P scripts/ci/check-markdown-links.py docs/delivery-workflow.md .github/pull_request_template.md docs/approvals/APPROVAL_REGISTER.md docs/reconciliation/step-0-reconciliation-v4.md` | Exit 0; files 4, links checked 131, anchors checked 92, broken 0, dead 0. External links not fetched. |
| `git diff --check` | Exit 0 on the current uncommitted three-file candidate. Must rerun on final four-file commit range. |
| Inline Python synthetic parser over the current template | Whole-line sentinel extraction and witness→skills→security normalized SHA-256 first16 gave `7bef210cdde4351a`; changing only the source-record placeholder gave `f323898417cfba21`; deleting the skills opening marker raised `skills opening marker count`. This is a fixture demonstration, not live PR serialization or CI enforcement. |

These local checks are Stage C implementation evidence, not an independent Stage E verdict. Actual PR CI, D/E/F/G evidence, live body readback and merge are UNRUN at this point.

## Decision/authority carry-forward and deviations

- Binding: `SD-A` accepted plan target, `SD-B` exact-hash ACCEPT; existing `MG1`–`MG5` and `SD-A`–`SD-G` still govern their later holders. The current owner choice authorizes the narrow policy; it does not appoint a PR editor or grant merge power.
- Deviation: none from the accepted design. Provisional D74 and external proposed APR text are deliberate collision holds, not final output.
- Continue by asking coordinator for confirmed order/main/IDs. On a changed main or record collision, reconcile before editing identifiers; on a conflicting policy change, return to Stage A/B. A separate agent must hold D implementation audit, another E validation, another F final review, and another G merge.

## Stage C self-authored skills rows

These are pending final candidate H/round binding and will be authored here at closeout. The eventual publisher must copy the final row strings exactly and cite this handoff's retained digest or immutable revision.

## 2026-10-08 21:34:14 UTC checkpoint

Elapsed wall from observed start: 18 minutes 30 seconds. Active time was not separately measured, so this is an imperfect comparison with the 45–75 active-minute estimate. Remaining implementation after the CIFIX register merge is estimated at 15–30 active minutes, dependent on ID/base reconciliation and rerunning checks. `git rev-parse HEAD` remains M; branch is `docs/rowpolicy-1-sourced-skills-rows`; `git status --short` lists only the three intended modified paths above. `git diff --check` exited 0. Current numstat: template 9 added/5 deleted, workflow 96 added/3 deleted, reconciliation 16 added/0 deleted. No commit, push, PR or register edit has occurred.

## 2026-10-08 21:39:38 UTC focused wording correction

Independent read-only precommit feedback identified three clarity points. In the workflow, retained older rows are now kept byte-exact while **their source records** carry historical/superseded status (current lines 554–557). F's self-row language now says it does not author another stage's row or relax independence, and that F still reviews the implementation independently (current lines 580–581). In the external proposed APR draft, a `Recorded at / by` field and scratch-only instruction require the actual UTC append time and recorder identity before copying into the register; the unknown owner-answer timestamp remains unclaimed. No source register edit occurred.

Focused checks after this wording change: `git diff --check` exit 0; `python -B -P scripts/ci/check-markdown-links.py docs/delivery-workflow.md .github/pull_request_template.md docs/reconciliation/step-0-reconciliation-v4.md` exit 0, files 3, links 82, anchors 81, broken 0, dead 0. Current numstat is template 9/5, workflow 98/3, reconciliation 16/0. Full four-file validation still awaits APR allocation and final append.

## 2026-10-09 06:52 UTC continued Stage C preparation

Same holder `/root/rowpolicy_impl` resumed. Branch `docs/rowpolicy-1-sourced-skills-rows` remains at M, with exactly the template, workflow and D-entry modified and register untouched; `git diff --check` exits 0. Fresh read-only GitHub main was `8e11c8f4c2777265e254057ce0fa1e52f0cf03bf` at 06:47 UTC. The GitHub compare from M to that main listed only `docs/reconciliation/auto-merge-policy.md` and `docs/roadmaps/aegis-backlog-forecast.md`, neither a ROWPOLICY target. PR #683 was OPEN at `abc49113a83a5fce54ce525912416b79859ba232` with only `docs/approvals/APPROVAL_REGISTER.md` changed (+77/0). Those are point-in-time reads, not final ID allocation; APR122 remains tentative. No PR #683 bytes were copied.

Offline synthetic AC3/AC5 artifacts are `rowpolicy/scratch-stage-c/fixture_check.py`, `fixture_result.json` and `AC3-AC5-case-record.md` outside the Git candidate. The script exits 0. It records four exact author captures/digests and all 13 plan cases, with executable equality/hash checks where possible and explicit procedural/unverified limits for authority, races, F/G and data loss. Exact B0 row matched; paraphrase, changed link/backticks, removed `UNRUN`, changed target and changed author failed raw comparison. Baseline witness→skills→security hash was `99431074c7e96f53`; changing only source metadata gave `e679db3d990515c6`; a known whitespace-only row edit left the normalized hash equal but changed raw body. Missing/duplicate opener, missing end and literal `\\n` body raised marker errors. Other decoded sections stayed equal; a quoted marker outside bound fields was ignored. These figures are fixture evidence, not live publication or CI enforcement.

Mechanical preservation rerun against M: MG, dependency, receipt and bound-field blocks are byte-identical; SD A–E/G rows and the seven stage-table exit IDs are identical; `AGENTS.md`, `CLAUDE.md`, `CONTRIBUTING.md` and register are byte-identical; D-entry insertion preserves the exact base prefix/suffix around §6 (1098 inserted bytes). Template has exactly the original six whole-line sentinel strings and one four-column skills header. A first temporary preservation command failed with `TypeError` from its own bytes/int concatenation; corrected rerun exited 0 with all comparisons true. This was a scratch checker error, not a source validation failure.

Focused current check: Markdown link checker on the three modified paths exited 0: files 3, links 82, anchors 81, broken 0, dead 0. No further source-doc defect found from these fixtures. Full four-file AC1/AC4/AC6 checks, exact APR record link, commit H/tree/B, CI, D/E/F/G and live PR body remain UNVERIFIED and held until coordinator resolves #683's main merge and the subsequent ID/base union.

## 2026-10-09 08:49 UTC offline handoff and PR-metadata preparation

**Scope and time.** This continuation started at 08:41:48 UTC. The 15–30 minute estimate was for active work; active time is not separately metered. This checkpoint is offline preparation only, not `SD-C: COMPLETE`. The matching Aegis skill applied was `.claude/skills/phased-work-handoff-designer/SKILL.md`: it supplied the cross-stage decision carry-forward, changed/not-touched inventory, proven-command receipts and continuation structure. `agent-governance-audit` was inspected but not applied because its retrospective independent-audit scope did not fit an implementer's own preparation.

**Correction to earlier checkpoint.** The preceding sentence about waiting for #683's **merge** is superseded as allocation guidance. Accepted PLAN-rev1 §5 requires coordinator allocation against current main **plus every open record-touching head**; #683's open APR120/121 head enters that union. Neither APR122 nor D74 is allocated by this scratch work. A coordinator may resolve the union before #683 merges. No #683 register bytes may be copied into this candidate merely to prepare the ID. Register edit, commit, push, PR create/edit and provider calls remain held by the current assignment.

**Artifacts outside the candidate.** `scratch-stage-c/AC7-evidence-draft.md` contains the local MG/SD agreement check, eight-site witness and per-marker AGENTS divergence results. `ac7-grep-current.txt` and `ac7-grep-base.txt` retain each 74-hit `git grep -n -E 'MG[1-5]|SD-[A-G]' -- docs/delivery-workflow.md` sweep. `scratch-stage-c/build_pr_draft.py` regenerates `PR-BODY-DRAFT.md` from the current template and the exact five A/two B self-authored source rows; it asserts source hashes, seven exact row matches, six unchanged sentinels, seven draft source records and eight witness rows. `PR-METADATA-DRAFT.md` records proposed title, classification, four-path plan, security answer and publication gates. All are unpublished scratch, not a live PR body or fixed retrievable source.

**Proven current local commands.** `python -B -P rowpolicy/scratch-stage-c/build_pr_draft.py` exited 0: `A exact rows=5 B exact rows=2 source records=7`, `sentinels=6 witness rows=8`, draft SHA-256 `a89fc63340a31cf4d4e4fc4211b8f3c8deb833b12ac9790a9fcc2ad92b236500`. `python -B -P rowpolicy/scratch-stage-c/fixture_check.py` exited 0 with the 13 synthetic AC3/AC5 case results; its baseline and changed-source first16 hashes differ (`99431074c7e96f53` versus `e679db3d990515c6`). `python -B -P scripts/validate-skills.py` exited 0 with 195 skills, 0 warnings; `python -B -P scripts/tests/test_validator.py` exited 0 with 181 assertions; `python -B -P scripts/ci/check-markdown-links.py docs/delivery-workflow.md .github/pull_request_template.md docs/reconciliation/step-0-reconciliation-v4.md` exited 0 with 3 files, 82 links, 81 anchors, 0 broken, 0 dead and 13 external links not fetched. `git diff --check` exited 0.

**Current candidate inventory.** `git status --short` has only three modified paths: template (9 additions/5 deletions), workflow (98/3), reconciliation (16/0). `docs/approvals/APPROVAL_REGISTER.md` remains untouched. Source root, AGENTS.md, CLAUDE.md, CONTRIBUTING.md, scripts, CI, skills and reserved evaluation/VM/ISO/Stage 4B/provider work remain untouched. No candidate-document defect was found in this continuation and no candidate document was edited.

**AC7 limits.** Both raw ID sweeps have 74 hits; the only added/changed ID-bearing line is the owning `SD-F` row. The eight-site witness lists sites 1/3/6/8 locally unchanged and 2/4/5 locally changed; site 7 is **UNVERIFIED** because no PR exists. Separate `rg -ni` AGENTS markers found MG1 at 92/93/95, MG2 at 70, MG3 review wait at 96, MG4 at 97–99 and MG5 at 71/73. The MG3 `P2|automated review|triag` marker and sourced-row marker each exited 1, documenting partial/absent startup-summary coverage without claiming contradiction. Final B/H and actual raw-body readback must replace every local-draft disposition. Semantic agreement and AC judgments belong to the independent D holder; CI, F hash/verdict and G receipt remain UNVERIFIED.

**Deviation and continuation.** No accepted-plan deviation or scope growth. The next authorized Stage C action requires coordinator's fresh main/open-head ID allocation and explicit release of the register/commit hold, then exact APR append with actual recorded-at/by, D-anchor update, four-path AC6 validation and immutable H/tree/B. Recheck A/B source-row capture against final publication form; later holders author their own rows. Stage D/E/F/G remain independent.
