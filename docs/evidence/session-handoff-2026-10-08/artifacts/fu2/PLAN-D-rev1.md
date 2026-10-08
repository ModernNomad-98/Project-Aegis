# PLAN-D rev1 — FU-2 Part D: skill contract-audit baseline refresh

Stage: **A — PLAN** (docs/delivery-workflow.md). Author: the Part D PLAN-stage subagent.
This plan writes nothing to the repository. Every figure below carries the command that produced it
(run 2026-10-08 between 14:13Z and 14:27Z) or is labelled **unverified**.

- Repository: `/home/user/Project-Aegis`, Role A (landmarks present: `head -1 README.md` → `# Project Aegis`;
  `ls docs/skills-catalog.md scripts/validate-skills.py artifacts/audits/skill-contract-audit-baseline.json` → all three listed).
- Base: `git fetch origin main; git rev-parse origin/main` → `c060a7cb09758fa2f4f6b67ab00094f01d7c6a46`
  (tree `0c5a2400e3a739f28d74ee36dc206e68a1d73dcb`); clone is not shallow (`git rev-parse --is-shallow-repository` → `false`).
- Delivery branch (from the brief's appended owner answers): `claude/sharp-lovelace-urgxpz-fu2`, created from origin/main by the
  FU-2 implementer. Part E (library-diff-reviewer description) is in the **same PR**.

## 1. What and why

**What.** Regenerate the four skill contract-audit baseline files with the audit engine **as it is on main (v1.13.4, unchanged)**,
over a clean checkout of the FU-2 branch commit that carries Part E's last change to an audited input; carry the generated
report's hand-written preface forward with updated wording; add one dated note to the AEGIS-060+ register; append one new
GRANT entry to the owner approval register recording the owner's request verbatim.

**Why.** The committed baselines freeze an old corpus. AEGIS-APR-066 and AEGIS-APR-084 say any further regeneration needs a new
grant, and the owner has now asked for the refresh ("Skill contract-audit baseline refresh (186 skills / 316 findings frozen vs
339 today)", brief, owner message 2026-10-08).

**This is a pure regeneration. No engine change.** The engine on main is byte-identical to the engine that wrote the frozen
baseline, and it reproduces the frozen files byte-for-byte (evidence E3). Nothing under `scripts/` or `tools/` changes, so
`gate-guard` is not triggered and no gate-guard exception is needed (evidence E8).

## 2. Evidence (re-derived this turn)

E1 — **Frozen baseline (186 skills / 316 findings): VERIFIED.** `python3 -B` read of
`artifacts/audits/skill-contract-audit-baseline.json` summary → `version 1.13.4`, `engine_sha256 e64b7430488c5f47c31faf1abcfa5f46aae876f3362ed8e0de105e988ff10153`,
`repo_sha 5dbf7bc9e958d932bd0c5b093ebecfe61be41840`, `branch chore/audit-engine-v1134-report-format`, `working_tree_dirty False`,
`skill_count 186`, `finding_count 316`, `by_severity {P0 2, P1 82, P2 0, info 232}`,
`by_rule {ARTF-001 9, ROUTE-002 232, SIDE-004 73, STATE-001 2}`, `audited_file_count 715`, `corpus_content_hash a14f70c9…146b73b`.
The manifest JSON carries the same provenance. `git diff --quiet c14338d2 origin/main -- artifacts/audits docs/audits/skill-contract-audit-baseline.md`
→ exit 0: unchanged since PR #503's merge `c14338d254bde3fd7fb9b8060033299cde5d5197`.

E2 — **Engine on main = engine that wrote the baseline.** `sha256sum scripts/audit-skill-contracts.py` →
`e64b7430488c5f47c31faf1abcfa5f46aae876f3362ed8e0de105e988ff10153` (equal to the baseline's `engine_sha256`);
`TOOL_VERSION = "1.13.4"` (line 107). Last engine change: `git log -1 -- scripts/audit-skill-contracts.py` → `9a1d8412 … (engine v1.13.4, AEGIS-APR-079)`.

E3 — **The current engine byte-reproduces the frozen baseline.** Fresh scratch clone (`-c core.autocrlf=false --no-hardlinks`),
`git checkout -b chore/audit-engine-v1134-report-format 5dbf7bc9…`, `git status --porcelain | wc -l` → `0`, engine run with
`--json/--graph/--manifest` → `cmp` against the committed files: `IDENTICAL` ×3. The committed Markdown equals the generated
Markdown plus a 16-line block (15 `>` preface lines + one blank) inserted after line 2 (`diff` shows only `2a3,18`; 339 vs 355 lines).

E4 — **Today's audit at origin/main (339): VERIFIED, with 195 skills.** Scratch clone at `c060a7cb` on branch `audit-scan-main`,
two runs: `audit-skill-contracts v1.13.4 — repo c060a7cb0975 (audit-scan-main), 195 skill(s), 27 rule(s)`,
`corpus hash 899ddf10d91e2467…  dirty: false`,
`findings: 339 (P0 2, P1 82, P2 0, info 255; 255 mechanical / 84 semantic-review candidates)`,
`ARTF-001: 9  ROUTE-002: 255  SIDE-004: 73  STATE-001: 2`. Both runs: all four outputs identical sha256
(`7d816d6a…` JSON, `44eb437f…` graph, `890c7592…` manifest, `63086864…` md). `audited_file_count 755`, `audited_byte_count 5193047`.
(This figure is **not** the number the refreshed baseline will record: Part E changes an audited input — see §4.)

E5 — **What changed since the frozen baseline, and why** (scratch script `dwork-cmp.py`, key = rule+file+evidence):
- Skills 186 → 195; **9 added, 0 removed**: `acceptance-criteria-reviewer` (89eec69c), `ai-human-in-the-loop-designer` (18299596),
  `ai-task-decomposer` (6a31a789), `ci-failure-classifier` (18e8a280), `cloud-security-baseline-reviewer` (287bf5b7),
  `database-backup-verifier` (5cc09e6d), `environment-parity-reviewer` (f9634b01), `resilience-architecture-reviewer` (58ba4701),
  `test-tenant-provisioner` (ebc9225d) — `git log --diff-filter=A 5dbf7bc9..c060a7cb -- '.claude/skills/*/SKILL.md'`, all 2026-09-28.
- Findings 316 → 339 = **+24 −1, all ROUTE-002** (info, mechanical). 23 of the +24 are exclusions written by the nine new skills;
  1 is `data-migration-runbook-author` → `gated-deployment-prompt-template` (that skill was edited in eaa50c58/e011dbda/ba190ccd).
  The −1 is `agent-harness-architect` → `model-context-designer`, now reciprocated (484b40f5/602addad edited model-context-designer).
- The 84 semantic-review candidates (SIDE-004 73, ARTF-001 9, STATE-001 2) are unchanged except **line numbers of 8 ARTF-001 rows**
  (only the `line` field differs). Rule inventory definitions identical; vocabulary census changed (per-skill counts).
- Route graph: nodes 186 → 195, edges 990 → 1075, unreferenced skills 12 → 10. Auxiliary input `docs/skills-catalog.md`
  changed since 5dbf7bc9 (`git diff --stat` → 177+/47−); `docs/paths/add-ai-safely.md` content changed (only names are inputs).
- The 24 new ROUTE-002 edges are **absent from** `docs/evidence/route002-dispositions-2026-09-26/route002-dispositions.json`
  (255 current edges; 24 not in its 268 triaged pairs — exactly the +24 above). They are untriaged census rows; this PR does not triage them.

E6 — **Part E changes the audit result, so D must run after E.** Scratch experiment only (synthetic text, not Part E's wording):
appending one clause to the `library-diff-reviewer` description changed 4 ROUTE-002 rows (−2 rows owned by library-diff-reviewer,
+2 rows owned by `code-reviewer` and `skill-quality-reviewer`), the corpus hash (`899ddf10…` → `6469e0bb…`) and the route graph.
Today 4 ROUTE-002 rows and 9 graph edges involve `library-diff-reviewer`. The description also feeds the manifest's `description_chars`.

E7 — **No CI job compares against the baseline.** `grep -rn -i 'baseline\|artifacts/\|audit-skill-contracts\|docs/audits' .github/` → no hits.
CI runs the engine's self-tests only (`.github/workflows/validate-skills.yml` step "Run contract-audit self-tests", comment
"Audit candidates remain advisory"). Every code reference to the baseline JSON is an existence/landmark check
(`scripts/tests/test_validator.py:1545,1705`; `tools/behavioral_eval_runner/materialize.py:91`, `graders/controls.py:41`,
`tests/helpers.py:117`, `tests/test_materialize.py:42`). `tools/readability_acceptance/build_index.py:65` and
`verify_ground_truth.py:222` use the report path only for class membership (generated report). The engine's docstring: "Not a merge gate (yet)".

E8 — **gate-guard does not match any Part D path.** Pattern read from `.github/workflows/validate-skills.yml:528`, tested with bash
`[[ =~ ]]` under `nocasematch`: `not-protected` for all three `artifacts/audits/*.json`, both `docs/audits/*.md`,
`docs/approvals/APPROVAL_REGISTER.md` (also `.claude/skills/library-diff-reviewer/SKILL.md`, `docs/skills-catalog.md`);
`PROTECTED scripts/audit-skill-contracts.py` (control).

E9 — **Register precedent (lifecycle read in full).** APR-058 (GRANT, v1.13.1 overwrite; its PR also appended the entry itself) →
APR-060 CONSUMED. APR-065 (GRANT, engine v1.13.2, "clean checkout of a main commit", exact 4 files + 060+ register notes,
"No further regeneration is covered", one PR) → APR-066 CONSUMED: "**Any further regeneration needs a new grant.**"
APR-073 (v1.13.3 format) → APR-076 CONSUMED; APR-079 (v1.13.4 format, frozen 5dbf7bc9, branch named, JSON-field equality rule)
→ APR-084 CONSUMED: "Any further change to the audit engine or regeneration of the baselines needs a new grant." No ACTIVE
baseline grant exists. APR-114 is the newest precedent for recording "Yes, same terms" merge terms.

E10 — **Next free register ID at c060a7cb: AEGIS-APR-119.** `grep -o '^### AEGIS-APR-[0-9]\+' … | sort -n` → 118 headings,
IDs 1–118 with no gap or duplicate. Open PRs: `gh api 'repos/ModernNomad-98/Project-Aegis/pulls?state=open'` → `length 0` at ~14:22Z.
**Re-check at implementation and again at merge** (FU-1 adds none per the brief, but others may).

E11 — **Readability status (instrument, read-only).** `python3 -B -I tools/readability_acceptance/check_index.py --path <p>` at c060a7cb:
`docs/audits/aegis-060-plus-register.md` → PROVABLY PENDING, 148 lines since `8ed59cd761d1`;
`docs/approvals/APPROVAL_REGISTER.md` → PROVABLY PENDING, 4690 lines + new section since `8ed59cd761d1`;
`docs/audits/skill-contract-audit-baseline.md` → not a reader page (generated-report class).

E12 — **Base checks pass** (scratch clone at c060a7cb, `TMPDIR` in scratch): `validate-skills.py` → `OK: 195 skill(s) valid, 0 warning(s)`;
`test_audit_skill_contracts.py` → `OK: 76 contract-audit self-test assertion(s) passed.`; `test_validator.py` → `OK: 181 gate self-test assertion(s) passed.`;
`test_markdown_links.py` → `OK`; corpus link check over 619 pages → `broken: 0   dead: 0`.

E13 — **Merge style matters for provenance.** `git log --first-parent --format='%h %p'` since 2026-10-03 → 24 single-parent (squash)
commits; earlier baseline PRs #432/#441/#461/#503 were merged with merge commits. Repo settings (`gh api repos/…` → `allow_merge_commit true,
allow_squash_merge true, allow_rebase_merge true`). Branch protection: `403 Resource not accessible` → **unverified** whether linear history is required.

## 3. Classification (change-classification-gate) and validation tier (risk-tiered-validation-selector)

```
CHANGE CLASSIFICATION — Part D
Deliverables:    (1) 3 regenerated JSON baselines + regenerated report body; (2) report preface + 060+ register dated note;
                 (3) one appended GRANT entry in the owner approval register
Classes:         (1) docs-only (generated data, no code; landmark file kept); (2) docs-only; (3) docs-only by file type,
                 but the approval register is a CONTRIBUTING.md security-relevant surface
Governing class: docs-only for Part D. The combined FU-2 PR's governing class is set by Part E (a skill description that steers
                 routing — ai-agentic per the gate's gotcha on instruction-steering text); Part E's plan owns that call.
Approval path:   owner approval already obtained (direct instruction 2026-10-08, verbatim in the brief); recorded as the new GRANT.
Scope contract:  the 6 paths in §6, nothing else.
```

```
VALIDATION TIER SELECTION — Part D (6 files vs origin/main)
No diffable tier-rules artifact exists in this repository (search for "never docs-only"/"forced-full" outside .claude/skills/
found only skill text and evidence copies) → every file is unmatched → FULL (fail-closed). Aggregate tier: FULL.
Tier contents (local mirror of the unconditional validate-skills job): validate-skills.py; scripts/tests/test_validator.py;
scripts/tests/test_audit_skill_contracts.py; scripts/tests/test_markdown_links.py; the corpus link check
(git ls-files | grep -v scripts/tests/fixtures/ | grep '[.]md$' → scripts/ci/check-markdown-links.py); BER self-check and offline
suite (they read the landmark path). Plus the Part-D-specific reproduction checks R1–R4 (§5).
Rules-file gaps: the repository has no tier rules file (recorded, not fixed here).
```

## 4. Sequencing with Part E — D runs **after** E, inside the same PR

The engine's inputs are: every file under `.claude/skills/**` (SKILL.md, references, eval JSONs, directory set), the **content** of
`docs/skills-catalog.md`, the **names** of `.claude/agents/*.md` and `docs/paths/*.md`, and Markdown-link targets' existence
(REF-001). Part E edits `.claude/skills/library-diff-reviewer/SKILL.md` (and possibly its evals or `docs/skills-catalog.md`), which
changes findings, corpus hash, graph and manifest (E6). Therefore:

1. Commit order on `claude/sharp-lovelace-urgxpz-fu2`: Part E commit(s) first (the register GRANT may come first or with D — it is
   not an audited input); then **one Part D commit** with the regenerated files.
2. **Scan target `S`** = the branch tip immediately before the Part D commit, which must contain Part E's final content.
3. If Part E is revised after D (e.g., a REVISE at Stage D/F), or any later commit touches an audited input, **regenerate** at the new
   `S` (criterion AC-8 detects this mechanically).
4. If FU-1 merges first and the branch must be updated, **merge** `origin/main` into the branch (do not rebase): a rebase rewrites `S`.
   FU-1's paths are not audited inputs, so AC-8 should still pass; if it does not, regenerate.

## 5. Exact regeneration commands and byte-reproducibility check

Run from the FU-2 worktree root `$REPO`, all Python with `-B`. `$SCR` is a fresh scratch directory outside the repository.

```bash
BR=claude/sharp-lovelace-urgxpz-fu2
test -z "$(git -C "$REPO" status --porcelain)"                 # Part E committed, tree clean
S=$(git -C "$REPO" rev-parse HEAD)                             # scan target
git -C "$REPO" diff --quiet origin/main "$S" -- scripts/ tools/ && echo "engine and tools unchanged vs main"
sha256sum "$REPO/scripts/audit-skill-contracts.py"            # expect e64b7430488c5f47c31faf1abcfa5f46aae876f3362ed8e0de105e988ff10153

for n in 1 2; do                                               # two independent fresh clones of S, branch named $BR
  git clone -q -c core.autocrlf=false --no-hardlinks "$REPO" "$SCR/clone$n"
  git -C "$SCR/clone$n" checkout -q -B "$BR" "$S"
  test -z "$(git -C "$SCR/clone$n" status --porcelain)" && echo "clone$n clean at $S"
  for r in a b; do                                              # two runs per clone
    o="$SCR/out$n$r"; mkdir -p "$o"
    python3 -B "$SCR/clone$n/scripts/audit-skill-contracts.py" --repo "$SCR/clone$n" \
      --json "$o/skill-contract-audit-baseline.json" --markdown "$o/generated.md" \
      --graph "$o/corpus-route-graph.json" --manifest "$o/corpus-manifest-baseline.json"
  done
done
# R1/R2 — four runs, two clones: every output byte-identical
for f in skill-contract-audit-baseline.json corpus-route-graph.json corpus-manifest-baseline.json generated.md; do
  cmp "$SCR/out1a/$f" "$SCR/out1b/$f" && cmp "$SCR/out1a/$f" "$SCR/out2a/$f" && cmp "$SCR/out1a/$f" "$SCR/out2b/$f" && echo "IDENTICAL $f"
done

# Install
cp "$SCR/out1a/"{skill-contract-audit-baseline.json,corpus-route-graph.json,corpus-manifest-baseline.json} "$REPO/artifacts/audits/"
P=$(wc -l < "$SCR/preface.md")       # preface block = '>' lines + one trailing blank line
{ head -n 2 "$SCR/out1a/generated.md"; cat "$SCR/preface.md"; tail -n +3 "$SCR/out1a/generated.md"; } \
  > "$REPO/docs/audits/skill-contract-audit-baseline.md"
# R4 — the report is the generated output plus the preface, nothing else
diff <(sed "3,$((2+P))d" "$REPO/docs/audits/skill-contract-audit-baseline.md") "$SCR/out1a/generated.md" && echo "R4 body == generated"
```

**R3 — head re-scan (the reviewers' and validator's check, at the PR head `H`).** Fresh clone, `git checkout -B "$BR" "$H"`, same
engine run into `$SCR/outH`. Expected: `diff artifacts/audits/<f> outH/<f>` shows **exactly one changed line — `repo_sha`** — in
`skill-contract-audit-baseline.json` and `corpus-manifest-baseline.json`; **no difference** in `corpus-route-graph.json`; and the
report body differs from `outH/generated.md` only in the `- Repo SHA:` line. This was rehearsed end-to-end in scratch with a synthetic
Part E edit (scan `S=2505a2f5…`, head `H=4befcdfa…`): output was exactly that (one `repo_sha` line per JSON, graph identical,
md one line); a fresh clone at `S` on the same branch name reproduced all four outputs `IDENTICAL`. Note that `branch` is part of the
output, so reproduction at `S` must use the branch name `$BR`.

## 6. Path allow-list (Part D) and NOT-touched list

Changed by Part D — exactly these six paths:
1. `artifacts/audits/skill-contract-audit-baseline.json` — regenerated, engine output byte-for-byte.
2. `artifacts/audits/corpus-route-graph.json` — regenerated (changes at c060a7cb already; listed "only if regeneration changes it").
3. `artifacts/audits/corpus-manifest-baseline.json` — regenerated.
4. `docs/audits/skill-contract-audit-baseline.md` — regenerated body + hand-written preface (preface wording updated).
5. `docs/audits/aegis-060-plus-register.md` — one appended dated note in "Historical baseline", after the 2026-09-28 "Report key extended" note; no existing line edited.
6. `docs/approvals/APPROVAL_REGISTER.md` — one appended GRANT entry at the end; no existing line edited.

NOT touched by Part D: `scripts/**`, `tools/**`, `.github/**`, `.claude/**` (Part E alone edits `.claude/skills/library-diff-reviewer/`),
`docs/skills-catalog.md` and `README.md` (Part E's, if any), `docs/roadmaps/aegis-backlog-forecast.md`, and all FU-1 files
(`docs/reconciliation/step-0-reconciliation-v4.md`, `docs/roadmaps/aegis-documentation-readability-backlog.md`,
`docs/roadmaps/aegis-open-decisions-2026-09-23.md`, `docs/offline-ci.md`, `.github/pull_request_template.md`). Dated session
checkpoints that quote 316 (`docs/roadmaps/session-checkpoint-2026-09-2{7,8}*.md`) are dated history and stay unchanged.

**Overlap:** Part D ∩ FU-1 = ∅. Part D ∩ Part E = ∅ unless Part E also wants a register entry — then the coordinator merges both
into the single GRANT below (variant B), because both items come from one owner message.

## 7. DRAFT register entry (transcript-only; persisted by the implementer under the owner's instruction)

ID: **next free at implementation time** (AEGIS-APR-119 at c060a7cb; re-check at implementation and at merge — whichever PR merges
second renumbers). Placement: appended after the last entry. Variant A (Part D only) is the default; it matches the question's
promise to record "the baseline refresh".

```markdown
### AEGIS-APR-NNN: Refresh the skill-contract audit baselines with engine v1.13.4

- **Event:** GRANT; a new grant. AEGIS-APR-058, AEGIS-APR-065, AEGIS-APR-073 and
  AEGIS-APR-079 were each consumed (AEGIS-APR-060, -066, -076, -084); this entry
  renews or widens none of them.
- **Status at recording:** ACTIVE; granted and not yet consumed. A later
  lifecycle event records its consumption. It cannot authorize the merge of
  the pull request that records it; that merge rests on the owner's
  instructions quoted verbatim in the merge agent's brief, which `AGENTS.md`
  accepts as authority.
- **Date / Grantor:** 2026-10-08 / Peter Nguyen.
- **Reason:** The committed baselines record engine v1.13.4 over the frozen
  commit `5dbf7bc9e958d932bd0c5b093ebecfe61be41840`: 186 skills and 316
  findings. At main `c060a7cb09758fa2f4f6b67ab00094f01d7c6a46` the same
  engine, unchanged, reports 195 skills and 339 findings: nine skills were
  added on 2026-09-28, and every finding added or removed is a ROUTE-002 row.
  AEGIS-APR-066 and AEGIS-APR-084 state that any further regeneration needs
  a new grant.
- **Owner decision, as transcribed by the coordinator from the session chat**
  (recorded 2026-10-08T14:13:30Z, an upper bound). The owner's message:

  > also work on these:
  > Skill contract-audit baseline refresh (186 skills / 316 findings frozen vs 339 today)
  > Aligning library-diff-reviewer's description with its "skill-library PR" wording

  The two item lines are the coordinating agent's own descriptions, which
  the owner copied into the message; the figures are the coordinator's and
  were re-measured as above. Asked "How should the two new items (audit
  baseline refresh, library-diff-reviewer wording) ship? They're separate
  from FU-1, and my session is set up to push to one branch.", the owner
  chose **"Second branch, in parallel"**, whose option text reads:

  > You allow one extra branch so FU-2 is built and reviewed alongside FU-1. Faster, but two PRs are open at once.

  Asked "May FU-2 merge on the same terms (every stage passed, all checks
  green, admin merge allowed, fix and retry)? Your request to do the
  baseline refresh will also be recorded as a new approval register grant,
  quoted word for word, because the register says any further regeneration
  needs a new grant." (recorded 2026-10-08T14:15:33Z, an upper bound), the
  owner chose **"Yes, same terms (Recommended)"**. The terms are the owner's
  two instructions for PR #677, recorded in AEGIS-APR-114:

  > I approve for you to merge once all checks are green. Including admin merge

  > if a check fails, diagnose and fix the issue and try to merge again. Do not stop until it is merged

- **Scope allowed:** The owner named no paths, engine or procedure; the
  following is the recorder's reading of "baseline refresh", modelled on
  AEGIS-APR-065. One pull request, from branch
  `claude/sharp-lovelace-urgxpz-fu2`, that regenerates, with
  `scripts/audit-skill-contracts.py` at engine v1.13.4 (SHA-256
  `e64b7430488c5f47c31faf1abcfa5f46aae876f3362ed8e0de105e988ff10153`) run
  unchanged on a clean checkout (`core.autocrlf=false`) of that branch's
  last commit that changes an audited input, checked out on a branch of the
  same name, exactly these files:
  `artifacts/audits/skill-contract-audit-baseline.json`,
  `artifacts/audits/corpus-route-graph.json`,
  `artifacts/audits/corpus-manifest-baseline.json` and
  `docs/audits/skill-contract-audit-baseline.md` with its hand-written
  preface; adds one dated note to `docs/audits/aegis-060-plus-register.md`;
  and appends this entry. Before that pull request merges, the files may be
  regenerated again whenever an audited input changes; the merged files are
  the output of the last such run. The merge terms are those quoted above.
- **Scope FORBIDDEN:** None additionally stated by the owner. Not covered by
  this grant: any change under `scripts/` or `tools/` (an engine change is
  not a baseline refresh and would need its own grant and a one-time
  `gate-guard` exception); rewriting any historical count in the AEGIS-060+
  register; any regeneration after this pull request merges. AEGIS-APR-100
  (including its `Scope FORBIDDEN`), AEGIS-APR-048, AEGIS-APR-050 and
  AEGIS-APR-105 continue unchanged.
- **Evidence:** Direct owner message and answers in the Project Aegis Claude
  Code session chat of 2026-10-08, as transcribed by the coordinator. None
  is a repository artifact. The baselines this grant's pull request
  replaces are in git history at `c14338d254bde3fd7fb9b8060033299cde5d5197`
  (PR #503's merge, recorded in AEGIS-APR-084).
- **Expiry / use limit:** One pull request; consumed by its merge, which a
  later lifecycle event records. (The request names one refresh.)
```

Variant B (only if the coordinator decides Part E is recorded too): retitle "…and align the library-diff-reviewer description";
add to Scope allowed "and changes the `library-diff-reviewer` description as Part E's accepted plan specifies (paths named there)".
Plan auditors: the one-PR use limit and the path list are the recorder's reading, labelled as such in the entry; the owner did not word them.

## 8. Drafts for the two hand-written texts (values `<…>` filled from the actual run at `S`)

Report preface (replaces the current 15 lines; independently reviewed per the generated-report rule):

```markdown
> **What this page is.** The machine-generated summary of the latest
> skill-contract audit, for maintainers checking which skill texts the audit
> script flags for review. Everything below this note is script output.
>
> **Regenerated 2026-10-08 under AEGIS-APR-NNN** (an owner grant in the
> [approval register](../approvals/APPROVAL_REGISTER.md)) with engine v1.13.4,
> unchanged, over `<S>` on branch `claude/sharp-lovelace-urgxpz-fu2`: the
> pull request's last change to an audited input, after its
> `library-diff-reviewer` description edit (checkout with core.autocrlf=false,
> so the corpus hash is over LF (line feed, Unix-style line ending) bytes).
> The previous baseline (186 skills, 316 findings, engine v1.13.4 over
> `5dbf7bc9e958d932bd0c5b093ebecfe61be41840`, pull request (PR) #503 under
> AEGIS-APR-079) is in git history at
> `c14338d254bde3fd7fb9b8060033299cde5d5197` (#503's merge).
> Structural findings are not behavioral proof.
```

AEGIS-060+ register note (appended after "Report key extended, 2026-09-28"):

```markdown
**Baseline files regenerated, 2026-10-08.** Under AEGIS-APR-NNN, an owner grant
in the [approval register](../approvals/APPROVAL_REGISTER.md), the same four
files were regenerated with engine v1.13.4, unchanged, from `<S>` on branch
`claude/sharp-lovelace-urgxpz-fu2` (<N> skills, <F> findings, of which <R> are
ROUTE-002). Since the v1.13.4 baseline, nine skills were added and every
finding added or removed is a ROUTE-002 row; the 84 semantic-review candidates
are the same rows, eight with moved line numbers. <K> ROUTE-002 rows are not in the
[2026-09-26 dispositions](../evidence/route002-dispositions-2026-09-26/README.md)
and are untriaged census rows. The v1.13.4 files remain in git history at
[`c14338d`](https://github.com/ModernNomad-98/Project-Aegis/tree/c14338d254bde3fd7fb9b8060033299cde5d5197/artifacts/audits)
(PR #503's merge). The historical counts below are unchanged.
```

(At c060a7cb, before Part E, the values would be N=195, F=339, R=255, K=24; the implementer must use the values measured at `S`, and
must re-check the "eight moved line numbers" and "every finding added or removed is ROUTE-002" claims at `S` with a comparison like `dwork-cmp.py`.)

## 9. Readability ledger implications (recorded honestly — corrects the brief's premise)

- The brief expects the regenerated `docs/audits` pages to "return to pending". Measured, that is **not** what happens:
  - `docs/audits/skill-contract-audit-baseline.md` is a **generated report**, not a reader page (ledger rule "Generated reports
    (owner decision, 2026-09-28)"; `build_index.py:65`). Each regeneration is verified **by reproducing it from the script** (R1–R4);
    its one-time format review was completed on the v1.13.4 output (#503) and the engine format is unchanged, so it stays a
    generated report. The **hand-written preface** is not script output: its change needs an independent review covering every changed
    preface line (Stage D/F can do this).
  - `docs/audits/aegis-060-plus-register.md` is **already provably pending** (148 lines past `8ed59cd`, E11). The appended note (about 14 lines) keeps it pending; no acceptance is gained or lost.
  - `docs/approvals/APPROVAL_REGISTER.md` is **already provably pending** (4690 lines, E11); it stays pending.
- Part D adds no Markdown file, so the tracked-page count is unchanged.
- The readability ledger is FU-1's file and the readability program is paused (AEGIS-APR-113); Part D writes nothing there and confers
  or claims no acceptance. The PR body states these facts so the ledger keeper (AEGIS-APR-101, a different agent) can record them.

## 10. Checks (Stage C local, Stage E full tier)

C1 R1–R4 (§5) at `S`; C2 R3 at the PR head `H`; C3 `python3 -B scripts/validate-skills.py`; C4 `scripts/tests/test_validator.py`;
C5 `scripts/tests/test_audit_skill_contracts.py`; C6 `scripts/tests/test_markdown_links.py` and the corpus link check (619+ pages,
`broken: 0 dead: 0`); C7 `python -m tools.behavioral_eval_runner self-check` and the offline BER unittest suite (landmark path);
C8 `git diff --numstat origin/main...H -- docs/approvals/APPROVAL_REGISTER.md docs/audits/aegis-060-plus-register.md` → deleted = 0 on both;
C9 `git diff --name-only origin/main...H` ⊆ Part D's 6 paths ∪ Part E's accepted paths; C10 gate-guard pattern applied to that list → no match;
C11 next-free-ID re-check (`grep -o '^### AEGIS-APR-[0-9]\+'`) shows the new ID unique and = max+1.
CI on push: `validate-skills` and `gate-guard` (required) must pass; tools/Windows jobs are path-scoped and will report skipped when no
`tools/` path changes — the merge agent decides how MG1 reads a skipped job (not decided here).

## 11. Acceptance criteria (numbered)

- **AC-1** The PR changes, for Part D, exactly the six §6 paths; with Part E's accepted paths, nothing else (C9). No path matches the gate-guard pattern (C10).
- **AC-2** `scripts/audit-skill-contracts.py` is unchanged vs origin/main, and both JSON baselines record `version 1.13.4` and
  `engine_sha256 e64b7430488c5f47c31faf1abcfa5f46aae876f3362ed8e0de105e988ff10153`.
- **AC-3** Both JSON baselines record `repo_sha = S`, `branch = claude/sharp-lovelace-urgxpz-fu2`, `working_tree_dirty false`,
  `dirty_paths_in_scanned_surfaces []`; `S` is an ancestor of the PR head and contains Part E's final edit to every audited input.
- **AC-4** R1/R2: four runs across two fresh clones of `S` produce byte-identical outputs, equal to the committed JSON files.
- **AC-5** R4: the committed report minus its preface block (lines 3..2+P) is byte-identical to the generated report.
- **AC-6** The preface is updated (no stale "AEGIS-APR-079 … same corpus" claim), names the new grant ID, `S`, the branch and the
  previous baseline's location, and has been independently reviewed line by line.
- **AC-7** The AEGIS-060+ note is appended only (0 deleted lines), and its figures equal the committed JSON summary at `S`
  (skill_count, finding_count, ROUTE-002 count) and a measured count of ROUTE-002 rows absent from the 2026-09-26 dispositions.
- **AC-8** R3 at the final PR head `H`: the only differences from the committed files are the `repo_sha` line in each JSON and the
  report's `- Repo SHA:` line; the route graph is identical. (Fails if any audited input changed after `S` → regenerate.)
- **AC-9** The register gains exactly one entry, appended (0 deleted lines), with ID = next free at merge time, quoting the owner's
  message and both answers verbatim from the brief, and no other entry byte-changed.
- **AC-10** Base checks C3–C7 pass at `H` with their tell-tale output lines quoted.
- **AC-11** The PR body states: security-relevant surface **Yes — the owner approval register** (no extra review for an agent PR, MG5);
  the readability facts of §9; the 24 (or measured) untriaged ROUTE-002 rows; and the "Aegis skills used" table.

**Declared not verifiable at this head (SD-A):** exact counts (Part E's edit is not written yet); AC-3/AC-4/AC-8 (need `S` and `H`);
CI results (need a push); whether `S` stays reachable from main after merge (depends on the merge method — §12 R-1); the ID number at merge.

## 12. Risks

- **R-1 Provenance after squash merge.** `S` is a branch commit. A squash merge (the current main habit, E13) leaves `S` reachable only
  through the PR's head ref; a rebase merge rewrites it. Corpus identity is still proven by `corpus_content_hash` (AC-8 at the merge
  commit). Recommendation to the merge stage (not a condition this plan can impose): a merge commit keeps `S` in main's history, as
  #432/#441/#461/#503 did. The consumption record should state which happened.
- **R-2 Part E revised after regeneration** → stale baseline. Mitigated by AC-8; regenerate.
- **R-3 FU-1 merges first and the branch is rebased** → `S` rewritten. Mitigated by §4.4 (merge, not rebase) and AC-8.
- **R-4 ID collision** with another register entry merged first. Mitigated by AC-9/C11 re-check at merge.
- **R-5 Grant wording read as wider or narrower than the owner's words.** Mitigated: verbatim quotes, recorder's reading labelled, no invented prohibitions; Stage B should check this.
- **R-6 Readers mistake the 24 new ROUTE-002 rows for defects.** Mitigated by the 060+ note and PR body (info, census, untriaged).
- **R-7 Large generated diff (~+1.2k/−0.15k JSON lines at c060a7cb)** hides a hand edit. Mitigated by R1–R4: the JSON must equal fresh engine output byte-for-byte.

## 13. Follow-ups (not in this PR)

1. CONSUMED event for the new grant, after merge, in a register-only PR sequenced by the coordinator (precedent APR-060/066/076/084);
   it records merge commit, head, paths, findings, and whether `S` is reachable from main.
2. Owner-decision rows in `docs/roadmaps/aegis-open-decisions-2026-09-23.md` and the forecast (precedent rows exist for #432/#441):
   FU-1-owned / coordinator-sequenced; Part D does not touch them.
3. Optional triage of the untriaged ROUTE-002 rows — owner decision, not scheduled here.

## 14. ETA

Implementation of Part D (after Part E's edit is committed): **45–90 min active** (regeneration and R1–R4 ~15 min; preface, note and
register entry ~30–45 min; checks C3–C11 ~15–30 min). Each re-regeneration after a Part E revision: ~15–20 min. Agent estimate, unmeasured.

## 15. Skills used by this PLAN stage

| Skill | How applied | Result |
| --- | --- | --- |
| `scoped-approval-register` | Read SKILL.md; drafted the GRANT in its field set: verbatim grant + the proposal it answered, Scope allowed as worded with the recorder's reading labelled, no invented prohibitions ("None additionally stated"), full lifecycle read of APR-058/060/065/066/073/076/079/084, draft-only persistence. | §7 draft (transcript-only). |
| `change-classification-gate` | Classified the three deliverables and declared the scope contract. | §3: docs-only for Part D; register is a security-relevant surface; approval obtained. |
| `risk-tiered-validation-selector` | Searched for a repo tier-rules artifact; none → fail-closed FULL; listed the tier's checks. Selector only — executes nothing. | §3, §10. |
| `skill-quality-reviewer` | Read SKILL.md and checked scope: it reviews ONE skill's quality and changes nothing; it does not own a baseline regeneration. **Not applied to Part D.** It (or `library-diff-reviewer` for the whole PR) belongs to Part E's review stages. | Scope confirmed: excluded. |

No skill owns writing a single change's plan (docs/delivery-workflow.md, "Recorded deviation"); this stage is procedural.

## 16. Handoff

- Binding decisions: SD-A…SD-G and MG1–MG5 unchanged; APR-066/084's "new grant" rule satisfied by the drafted GRANT; APR-100/048/050/105 unchanged.
- Changed files: none (plan stage). Scratch only: `…/fu2/dwork/` (clones and outputs), `…/fu2/dwork-cmp.py`.
- Deviation flags: the brief's "pages return to pending" premise corrected (§9); one-PR limit and path list are the recorder's reading (§7).
- Continuation: Stage B audits this file's captured sha256; the implementer starts only after Part E's edit is committed, then runs §5.
