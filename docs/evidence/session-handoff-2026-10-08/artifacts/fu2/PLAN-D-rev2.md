# PLAN-D rev2 — FU-2 Part D: skill contract-audit baseline refresh

> **Revision marker.** rev2 supersedes rev1 (`PLAN-D-rev1.md`, sha256
> `d1152150beeb07cb496db35c799c82d1189860ac3d55fc8adef1912176a9df56`, left unchanged). It answers
> `SD-B: REVISE` in `PLAN-AUDIT-rev1.md` (sha256 `9acd2e50818e2aa290b89b1ffd4b322076212574b23dcc9795475e35e72a5fab`)
> and the coordinator decisions appended to `BRIEF.md` (sha256 `e504a786515e7d408c8d99479c93973621488fc743ac4fb4dbb2fae44bb48597`).
> Rework started 2026-10-08T14:44:26Z. Stage A only; no repository edits.

## 0. Finding → fix

| Finding | Fix in rev2 | Where |
| --- | --- | --- |
| **B-D1** Two definitions of the scan commit S | **One definition, used in every place:** *S is a commit on branch `claude/sharp-lovelace-urgxpz-fu2` that contains every change the pull request makes to an audited input. Its SHA is recorded in the regenerated files as `repo_sha`.* "Audited input" is defined once (§4.1). The definition still holds after a later merge of `origin/main`, and AC-3 and AC-8 test it mechanically. The GRANT goes **in the D commit**, so no register commit can sit between E1 and D. | §4, §5, §7 grant, §8 preface, AC-3 |
| **B-D2** Plan assumed a SKILL.md description edit | Restated to match coordinator decision E1: the only Part E change is the top-level `description` note in `library-diff-reviewer/evals/trigger-evals.json`. Measured effect: findings, graph, manifest `skills`, rule inventory and census are all unchanged. `corpus_content_hash` goes `899ddf10…` → `673e7fe9…` and `audited_byte_count` drops by 3. The words "description edit" are removed from the plan and the page drafts. §3 is corrected: ai-agentic by location. | E6, §3, §4, §8 |
| **B-D3** K, 24/1/8 not mechanically defined | Exact definitions, and the scripts inlined in §5.3: the auditor's `cmp.py` copied verbatim, plus `k_untriaged.py` and `skills_diff.py`. Re-run this turn on the real E1 simulation, they give 24 / 1 / 8 / K = 24 / +9 −0 skills. | §5.3, AC-7 |
| N-D1 Expiry label | "(recorder's reading)" added. The entry cites the selected option text "Faster, but two PRs are open at once". | §7 |
| N-D2 "Same terms" referent | The question's own parenthetical is kept as the primary words. Mapping it to the PR #677 instructions (APR-114) is labelled as the recorder's reading. | §7 |
| N-D3 Seventh path | One sentence added: the same PR also carries Part E's eval edit, authorized by the owner's direct request and not by this grant. | §7 |
| N-D4 Premise attribution | The "pages return to pending" premise is attributed to the planner's task message, not to BRIEF.md. | §9 |
| N-D5 Merge-time freshness | AC-12 is a freshness check against freshly fetched `origin/main` at Stage E and Stage G. | §11 |
| N-D6 "Appended" | AC-9 and AC-7 now check hunk positions with `git diff -U0`. I rehearsed both commands. | §11 |
| N-D7 Renumbering cost | Named in R-4: a renumber touches three files, moves the head, and Stages D–F re-run. | §12 |
| N-D8 Dates | Now reads "author dates 2026-09-28 to 2026-09-29 UTC". | E5, §7 |
| N-D9 / N-E2 BER locally | Coordinator rule applied. The BER self-check and offline suite are **not run locally**. The evidence is CI's `validate-skills` job steps `ber-self-check` and `ber` (`validate-skills.yml:229-233`), declared as such. | §3, §10 |
| (new, found while rehearsing) Stale `origin/main` in scratch clones | A clone made from the local repo path inherits that repo's local `main` as its `origin/main`. Measured: `03c93c77`, while the real `origin/main` is `c060a7cb`. All base and freshness checks therefore take SHAs from the real worktree after `git fetch origin main` and pass them in explicitly. | §5, §11 |

Every figure carries its command and observed output, or is labelled **unverified**. Runs used `python3 -B` (and `-I` for scratch scripts),
2026-10-08 14:13–14:29Z (rev1) and 14:44–14:50Z (rev2).

- Repository: `/home/user/Project-Aegis`, Role A. Landmarks: `head -1 README.md` → `# Project Aegis`; the other three paths are listed by `ls`.
- Base: `git rev-parse origin/main` → `c060a7cb09758fa2f4f6b67ab00094f01d7c6a46` (tree `0c5a2400e3a739f28d74ee36dc206e68a1d73dcb`). The clone is not shallow.
- Delivery branch: `claude/sharp-lovelace-urgxpz-fu2` (owner answer "Second branch, in parallel"). Part E (E1) and Part D are in the
  same PR. Order: **E1 commit first, then D** (coordinator decision).

## 1. What and why

**What.** Regenerate the four contract-audit baseline files with the engine on main (v1.13.4, unchanged), over S as defined in §4.1.
Carry the report's hand-written preface forward with updated wording. Add one dated note to the AEGIS-060+ register. Append one new
GRANT entry (variant A) that quotes the owner verbatim.

**Why.** The committed baselines freeze an old corpus. AEGIS-APR-066 and AEGIS-APR-084 say any further regeneration needs a new grant.
The owner asked for "Skill contract-audit baseline refresh (186 skills / 316 findings frozen vs 339 today)" (BRIEF.md, 2026-10-08).

**A pure regeneration; no engine change.** Main's engine is byte-identical to the one that wrote the frozen baseline, and it reproduces
the frozen files byte-for-byte (E3). Nothing under `scripts/` or `tools/` changes, so gate-guard is not triggered (E8).

## 2. Evidence

E1 — **Frozen baseline: 186 skills, 316 findings (verified).** `artifacts/audits/skill-contract-audit-baseline.json` summary:
`version 1.13.4`, `engine_sha256 e64b7430488c5f47c31faf1abcfa5f46aae876f3362ed8e0de105e988ff10153`, `repo_sha 5dbf7bc9e958d932bd0c5b093ebecfe61be41840`,
`branch chore/audit-engine-v1134-report-format`, `working_tree_dirty False`, 186 skills, 316 findings
(`ARTF-001 9, ROUTE-002 232, SIDE-004 73, STATE-001 2`), 715 files, corpus hash `a14f70c9…146b73b`.
`git diff --quiet c14338d2 origin/main -- artifacts/audits docs/audits/skill-contract-audit-baseline.md` → exit 0, so nothing has
changed since PR #503's merge `c14338d254bde3fd7fb9b8060033299cde5d5197`.

E2 — **Engine.** `sha256sum scripts/audit-skill-contracts.py` on main → `e64b7430…10153`, the same value as the baseline's
`engine_sha256`. `TOOL_VERSION = "1.13.4"` (line 107). Last change: `9a1d8412` (APR-079). The engine file *at* `5dbf7bc9` is a
different file (the auditor measured sha256 `8622bac7…`). "Main's engine" always means main's file, run against the given corpus.

E3 — **Main's engine reproduces the frozen baseline byte-for-byte.** Fresh clone (`-c core.autocrlf=false --no-hardlinks`) at
`5dbf7bc9`, on branch `chore/audit-engine-v1134-report-format`, porcelain empty. `cmp` gives `IDENTICAL` for all three JSON
files. The committed report = generated report + a 16-line block (15 `>` lines + 1 blank) after line 2. `diff` shows only `2a3,18`.

E4 — **Today at `c060a7cb`.** Clone on branch `audit-scan-main`, two runs:
`195 skill(s), 27 rule(s)`, `findings: 339 (P0 2, P1 82, P2 0, info 255; 255 mechanical / 84 semantic-review candidates)`,
`ROUTE-002: 255`. The two runs gave identical outputs.

E5 — **Change since the frozen baseline: definitions in §5.3, values from that procedure** (old = `c14338d2`'s committed JSON;
new = the E1 simulation below):
- Skills (`skills_diff.py`): `186 -> 195 | added 9 [acceptance-criteria-reviewer, ai-human-in-the-loop-designer, ai-task-decomposer,
  ci-failure-classifier, cloud-security-baseline-reviewer, database-backup-verifier, environment-parity-reviewer,
  resilience-architecture-reviewer, test-tenant-provisioner] | removed 0`. Author dates are 2026-09-28 to 2026-09-29 UTC
  (`TZ=UTC git log --date=iso-strict-local --format='%h %ad' --diff-filter=A 5dbf7bc9..c060a7cb -- '.claude/skills/*/SKILL.md'`).
- Findings (`cmp.py`): `counts 316 -> 339`; `added (ignoring line): 24 {'ROUTE-002': 24}`;
  `removed (ignoring line): 1 {'ROUTE-002': 1}` (`agent-harness-architect ('model-context-designer',)`);
  `rows differing only in line: 8 {'ARTF-001': 8}`; `semantic multiset equal ignoring line: True 84 84`.
  23 of the 24 added rows come from the nine new skills; 1 comes from `data-migration-runbook-author`.
- K (`k_untriaged.py`): `dispositions pairs: 268 of 268 entries`; `ROUTE-002 rows: 255 K (pair absent from dispositions): 24`.
  For the frozen baseline: `ROUTE-002 rows: 232 K …: 0`.
- Route graph: nodes 186 → 195, edges 990 → 1075, unreferenced 12 → 10.

E6 — **Part E (E1) is an audited input: it changes the corpus hash only.** Real E1 applied in scratch: clone at `c060a7cb`, branch
`claude/sharp-lovelace-urgxpz-fu2`, a byte-exact single replacement (`library-changing PR` → `skill-library PR`) in
`.claude/skills/library-diff-reviewer/evals/trigger-evals.json`. The file goes `4044 -> 4041` bytes, sha256 `2e54cf0f…` → `52e7eb47…`.
`numstat 1 1`. Committed as `daa3459d…`. Two engine runs were identical. Against `c060a7cb`'s output:
`findings equal True rule_inventory equal True census equal True`; graph `cmp` identical; `manifest skills equal True`. The summary keys
that differ are `audited_byte_count` (5193047 → 5193044), `corpus_content_hash` (`899ddf10d91e24675c5c5435af5902eb359418b94d346e1ab377c97de35ac3b3` →
`673e7fe93c6ddfb84e485dae4be1f1538f85af6c4fbaed893323e42e7e886b14`), `repo_sha` and `branch`. This matches the auditor's measurement and PLAN-E §4.
So D must run after E1, or the committed corpus hash will not match the merged tree. The findings figures are the same as at `c060a7cb`.

E7 — **No CI job compares against the baseline.** `grep -rn -i 'baseline\|artifacts/\|audit-skill-contracts\|docs/audits' .github/` → no hits.
Code references are existence or landmark checks only (`test_validator.py:1545,1705`; BER `materialize.py:91`, `graders/controls.py:41`,
`tests/helpers.py:117`, `tests/test_materialize.py:42`). `build_index.py:65` and `verify_ground_truth.py:222` use the report path for
class membership only. The engine's own docstring says: "Not a merge gate (yet)".

E8 — **gate-guard.** Pattern from `.github/workflows/validate-skills.yml:528`, tested with bash `[[ =~ ]]` under `nocasematch`: `not-protected` for all six Part D paths
(and for both Part E paths). `PROTECTED scripts/audit-skill-contracts.py` (control).

E9 — **Register lifecycle.** APR-058→060, 065→066 ("Any further regeneration needs a new grant."), 073→076 and 079→084 ("Any further
change to the audit engine or regeneration of the baselines needs a new grant.") are all CONSUMED. No baseline grant is ACTIVE.

E10 — **Next free ID at `c060a7cb`: AEGIS-APR-119.** There are 118 headings, IDs 1–118, no gap or duplicate. The last entry in the file is APR-118, and file
order is not numeric. Open PRs: `gh api …/pulls?state=open` → `0`. **Re-check at implementation and at merge.**

E11 — **Readability (instrument).** `check_index.py --path` at `c060a7cb`: `aegis-060-plus-register.md` PROVABLY PENDING (148 lines since
`8ed59cd761d1`); `APPROVAL_REGISTER.md` PROVABLY PENDING (4690 lines plus a new section); the audit report is not a reader page.

E12 — **Base checks pass** (scratch at `c060a7cb`): `validate-skills.py` → `OK: 195 skill(s) valid, 0 warning(s)`;
`test_audit_skill_contracts.py` → `OK: 76 …`; `test_validator.py` → `OK: 181 …`; `test_markdown_links.py` → `OK`; corpus link check
over 619 pages → `broken: 0   dead: 0`.

E13 — **Merge method.** Since 2026-10-03 main shows 24 single-parent commits. PRs #432, #441, #461 and #503 were merged with merge commits. All
three merge methods are allowed (`gh api repos/…`). Branch protection could not be read (403), so whether linear history is required is **unverified**.
Coordinator decision: prefer a merge commit, which keeps S in main's history. The merge agent verifies that it is allowed; otherwise it records the provenance consequence.

E14 — **Full Part D rehearsal with the real E1 edit** (scratch; SHAs passed explicitly):
- S = `daa3459d…` (E1 commit).
- Installed outputs and a 3-line test preface: `R4 body == generated`.
- Test 060+ note inserted after the anchor and a test entry appended to the register; committed as H = `66c7418e…`.
- `git diff --quiet S H -- .claude/skills docs/skills-catalog.md .claude/agents docs/paths` → `audited inputs S==H`.
- Register hunk: `@@ -5062,0 +5063,4 @@` (old line count 5062 → appended at the end).
- 060+ hunk: `@@ -121,0 +122,3 @@` (anchor line 120 + its blank line 121).
- Numstat vs `c060a7cb`: 7 paths (6 Part D + E1).
- R3: fresh clone at H on the same branch name → JSON: `2 changed line(s)` each (`repo_sha` old/new), graph `0`, report body:
  only the `- Repo SHA:` line.
- Pitfall found: the scratch clone's `origin/main` was `03c93c77` (the local repo's stale local `main`, `git rev-parse main`), not `c060a7cb`.

## 3. Classification and validation tier

```
CHANGE CLASSIFICATION — Part D
Deliverables:    (1) 3 regenerated JSON baselines + regenerated report body; (2) report preface + 060+ register dated note;
                 (3) one appended GRANT entry (variant A)
Classes:         (1)(2) docs-only (generated data and prose; landmark file kept); (3) docs-only by file type, on a
                 CONTRIBUTING.md security-relevant surface (the owner approval register)
Governing class: docs-only for Part D. The combined PR's governing class is ai-agentic BY LOCATION: Part E edits an eval file
                 inside a skill directory (PLAN-E §1). No routing text changes.
Approval path:   owner's direct instruction 2026-10-08 (verbatim in BRIEF.md), recorded as the new GRANT
Scope contract:  the 6 paths in §6
```

```
VALIDATION TIER SELECTION — Part D
No tier-rules artifact in this repository → all files unmatched → FULL (fail-closed).
Local mirror: validate-skills.py; test_validator.py; test_audit_skill_contracts.py; test_markdown_links.py; corpus link check;
              the Part D reproduction checks (§5, §11).
Declared CI-only (coordinator rule, not run locally): BER self-check and offline BER suite — evidence = `validate-skills` job steps
              `ber-self-check` and `ber` (validate-skills.yml:229-233) at the head. `windows-offline-checks` (if: …offline == 'true',
              :275) and the tools jobs are path-scoped and will be SKIPPED; record them as skipped, not green.
```

## 4. Definition of S and sequencing

**4.1 Audited input** (the engine's inputs, from `audit-skill-contracts.py`): any file under `.claude/skills/`, including the directory set;
the content of `docs/skills-catalog.md`; the file names under `.claude/agents/` and `docs/paths/`; and, for REF-001, whether
Markdown-link targets exist.

**S (the only definition, used in the procedure, the grant, the preface and AC-3):** *a commit on branch
`claude/sharp-lovelace-urgxpz-fu2` that contains every change the pull request makes to an audited input. Its SHA is recorded in the
regenerated files as `repo_sha`.*

Mechanical test at any head H: `git merge-base --is-ancestor S H`, **and**
`git diff --quiet S H -- .claude/skills docs/skills-catalog.md .claude/agents docs/paths`, **and** R3 (§5.2) passes. R3 also covers
REF-001 link-target existence. The test is conservative: a content change under `.claude/agents/` or `docs/paths/` also fails it.

**4.2 Sequencing.**
1. The E1 commit is first on the branch (coordinator decision).
2. **One D commit** carries all six Part D paths, the GRANT included. Nothing for Part D is committed before it.
3. When regenerating, take `S=$(git rev-parse HEAD)` immediately before the D commit. This is the E1 commit, or a later merge of `origin/main`.
   Both satisfy the definition.
4. If E1 is revised, or any later commit changes an audited input, the test fails: regenerate at a new S, in a new commit.
5. If FU-1 or another PR merges first, **merge** `origin/main` into the branch. Do not rebase, because a rebase rewrites S.
   - If the merge brings in no audited-input change, S still satisfies the definition (AC-8 confirms).
   - If it does, regenerate.

## 5. Procedure (exact commands)

**Pitfall:** a scratch clone made from the local repo path has a stale `origin/main`. Take every base SHA from `$REPO` after
`git -C "$REPO" fetch origin main`, and pass SHAs in explicitly.

### 5.1 Regenerate (R1/R2/R4)

```bash
BR=claude/sharp-lovelace-urgxpz-fu2
git -C "$REPO" fetch origin main; BASE=$(git -C "$REPO" rev-parse origin/main)
test -z "$(git -C "$REPO" status --porcelain)"                  # E1 committed, tree clean
S=$(git -C "$REPO" rev-parse HEAD)
git -C "$REPO" diff --name-only "$(git -C "$REPO" merge-base "$S" "$BASE")" "$S" -- .claude/skills docs/skills-catalog.md .claude/agents docs/paths
#   expect exactly: .claude/skills/library-diff-reviewer/evals/trigger-evals.json
git -C "$REPO" diff --quiet "$BASE" "$S" -- scripts/ tools/ && echo "engine and tools unchanged vs main"
sha256sum "$REPO/scripts/audit-skill-contracts.py"             # expect e64b7430488c5f47c31faf1abcfa5f46aae876f3362ed8e0de105e988ff10153
for n in 1 2; do
  git clone -q -c core.autocrlf=false --no-hardlinks "$REPO" "$SCR/clone$n"
  git -C "$SCR/clone$n" checkout -q -B "$BR" "$S"
  test -z "$(git -C "$SCR/clone$n" status --porcelain)" && echo "clone$n clean at $S"
  for r in a b; do
    o="$SCR/out$n$r"; mkdir -p "$o"
    python3 -B "$SCR/clone$n/scripts/audit-skill-contracts.py" --repo "$SCR/clone$n" \
      --json "$o/skill-contract-audit-baseline.json" --markdown "$o/generated.md" \
      --graph "$o/corpus-route-graph.json" --manifest "$o/corpus-manifest-baseline.json"
  done
done
for f in skill-contract-audit-baseline.json corpus-route-graph.json corpus-manifest-baseline.json generated.md; do
  cmp "$SCR/out1a/$f" "$SCR/out1b/$f" && cmp "$SCR/out1a/$f" "$SCR/out2a/$f" && cmp "$SCR/out1a/$f" "$SCR/out2b/$f" && echo "IDENTICAL $f"
done
cp "$SCR/out1a/"{skill-contract-audit-baseline.json,corpus-route-graph.json,corpus-manifest-baseline.json} "$REPO/artifacts/audits/"
P=$(wc -l < "$SCR/preface.md")                                   # '>' lines + one trailing blank line
{ head -n 2 "$SCR/out1a/generated.md"; cat "$SCR/preface.md"; tail -n +3 "$SCR/out1a/generated.md"; } > "$REPO/docs/audits/skill-contract-audit-baseline.md"
diff <(sed "3,$((2+P))d" "$REPO/docs/audits/skill-contract-audit-baseline.md") "$SCR/out1a/generated.md" && echo "R4 body == generated"
```

Then write the 060+ note (inserted after the blank line that follows the line
`(PR #461's merge). The historical counts below are unchanged.`, which is line 120 at `c060a7cb`) and append the GRANT. Fill the `<…>`
values from §5.3 run on `$SCR/out1a`. Commit all six paths as the D commit.

### 5.2 Head re-scan (R3), at the PR head H

Fresh clone of `$REPO`, `git checkout -B "$BR" "$H"`, then the same engine run into `$SCR/outH`. Expected:
- `diff artifacts/audits/<f> outH/<f>` shows only the `repo_sha` line in each of the two JSON files.
- The route graph has no difference.
- `diff <(sed "3,$((2+P))d" docs/audits/skill-contract-audit-baseline.md) outH/generated.md` shows only the `- Repo SHA:` line.

### 5.3 Mechanical definitions and scripts (inline; run with `python3 -B -I`)

- **Added / removed findings** = multiset difference on key `(rule, file, owning_skill, related_skills, evidence)`, line ignored, between OLD and NEW.
- **Rows differing only in line** = NEW rows (key including `line`) absent from OLD whose line-free key is not in the added set.
- **Semantic candidates unchanged** = equal multisets of the line-free key over findings with `mechanical == false`.
- **K** = the number of NEW findings with `rule == "ROUTE-002"` whose pair `(owning_skill, related_skills[0])` is absent from
  `{(f.source_skill, f.target_skill) for f in route002-dispositions.json.findings}`. The script asserts that every ROUTE-002 row has exactly one related skill, named in its evidence.
- **Skills added / removed** = set difference of manifest `skills[].name`.
- OLD = `git show c14338d254bde3fd7fb9b8060033299cde5d5197:artifacts/audits/<file>`; NEW = the regenerated file;
  dispositions = `docs/evidence/route002-dispositions-2026-09-26/route002-dispositions.json`.

`cmp.py` — copied verbatim from the auditor (`…/fu2/b-audit/tools-b/cmp.py`, sha256 `5f6ec1fe77961fdf1b76b79bcd252709dbbb0a5c104e69c4ae4113649b0bed44`); usage `cmp.py OLD.json NEW.json`:

```python
import json, sys
from collections import Counter
a = json.load(open(sys.argv[1])); b = json.load(open(sys.argv[2]))
def key(f, with_line=True):
    k = (f['rule'], f['file'], f['owning_skill'], tuple(f.get('related_skills') or []), f['evidence'])
    return k + ((f['line'],) if with_line else ())
A = Counter(key(f) for f in a['findings']); B = Counter(key(f) for f in b['findings'])
An = Counter(key(f, False) for f in a['findings']); Bn = Counter(key(f, False) for f in b['findings'])
added = Bn - An; removed = An - Bn
print('counts', len(a['findings']), '->', len(b['findings']))
print('added (ignoring line):', sum(added.values()), dict(Counter(k[0] for k in added.elements())))
print('removed (ignoring line):', sum(removed.values()), dict(Counter(k[0] for k in removed.elements())))
for k in removed.elements(): print('  -', k[0], k[2], k[3])
lineonly = [k for k in (B - A).elements() if k[:-1] not in added]
print('rows differing only in line:', len(lineonly), dict(Counter(k[0] for k in lineonly)))
sem = lambda d: Counter(key(f, False) for f in d['findings'] if not f['mechanical'])
print('semantic multiset equal ignoring line:', sem(a) == sem(b), sum(sem(a).values()), sum(sem(b).values()))
print('added by owner:', dict(Counter(k[2] for k in added.elements())))
for k in ['skill_count','finding_count','by_rule','mechanical_count','semantic_review_candidates','audited_file_count','audited_byte_count','corpus_content_hash']:
    print(k, a['summary'][k], '->', b['summary'][k])
print('rule_inventory equal:', a['rule_inventory'] == b['rule_inventory'])
print('vocab equal:', a['vocabulary_census'] == b['vocabulary_census'])
print('findings list equal:', a['findings'] == b['findings'])
```

`k_untriaged.py` (sha256 `6f42607091e45066ead80a3f3ad534b0f3b2de4a6fae8babd5170d8798c6a79b`); usage `k_untriaged.py NEW.json DISPOSITIONS.json`:

```python
import json, re, sys
from collections import Counter
new = json.load(open(sys.argv[1], encoding="utf-8"))
disp = json.load(open(sys.argv[2], encoding="utf-8"))
pairs = {(d["source_skill"], d["target_skill"]) for d in disp["findings"]}
rows = [f for f in new["findings"] if f["rule"] == "ROUTE-002"]
bad = [f for f in rows if len(f["related_skills"]) != 1
       or f"toward `{f['related_skills'][0]}`" not in f["evidence"]]
assert not bad, f"{len(bad)} ROUTE-002 row(s) do not name exactly one target"
untriaged = [(f["owning_skill"], f["related_skills"][0]) for f in rows
             if (f["owning_skill"], f["related_skills"][0]) not in pairs]
print("dispositions pairs:", len(pairs), "of", len(disp["findings"]), "entries")
print("ROUTE-002 rows:", len(rows), "K (pair absent from dispositions):", len(untriaged))
print("K by owning skill:", dict(sorted(Counter(s for s, _ in untriaged).items())))
```

`skills_diff.py` (sha256 `265495ad392c7229486d768a8eab9c0e1974b2c7837eb69455edf4f46652d6af`); usage `skills_diff.py OLD-manifest.json NEW-manifest.json`:

```python
import json, sys
old = {s["name"] for s in json.load(open(sys.argv[1], encoding="utf-8"))["skills"]}
new = {s["name"] for s in json.load(open(sys.argv[2], encoding="utf-8"))["skills"]}
print("skills", len(old), "->", len(new), "| added", len(new - old), sorted(new - old), "| removed", len(old - new), sorted(old - new))
```

Expected at S, if nothing but E1 changes an audited input: 195 skills, 339 findings, ROUTE-002 255; added 24 / removed 1 / line-only 8 /
semantic 84 = 84 / K 24 / skills +9 −0; corpus hash `673e7fe9…`, bytes 5193044. These are predictions. The implementer records the measured values.

## 6. Path allow-list (Part D) and NOT-touched list

Part D changes exactly six paths, all in the D commit:
1. `artifacts/audits/skill-contract-audit-baseline.json`
2. `artifacts/audits/corpus-route-graph.json`
3. `artifacts/audits/corpus-manifest-baseline.json`
4. `docs/audits/skill-contract-audit-baseline.md` (body regenerated; preface rewritten)
5. `docs/audits/aegis-060-plus-register.md` (one inserted note; no line edited)
6. `docs/approvals/APPROVAL_REGISTER.md` (one entry appended at the end; no line edited)

The PR's seventh path is Part E's `.claude/skills/library-diff-reviewer/evals/trigger-evals.json`.

Not touched by Part D:
- `scripts/**`, `tools/**`, `.github/**`, `.claude/**`
- `docs/skills-catalog.md`, `README.md`, `docs/roadmaps/aegis-backlog-forecast.md`
- the five FU-1 files
- the dated session checkpoints that quote 316

Overlap: Part D ∩ FU-1 = ∅. Part D ∩ Part E = ∅. Variant A was chosen, so Part E has no register entry.

## 7. DRAFT register entry (variant A; transcript-only)

ID = next free at implementation time (AEGIS-APR-119 at `c060a7cb`). Re-check at merge; whichever PR merges second renumbers. Append it after the last entry.

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
  added (author dates 2026-09-28 to 2026-09-29 UTC), and every finding added
  or removed is a ROUTE-002 row. AEGIS-APR-066 and AEGIS-APR-084 state that
  any further regeneration needs a new grant.
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
  owner chose **"Yes, same terms (Recommended)"**. The terms are the ones
  the question lists in parentheses. Recorder's reading: they are the terms
  of the owner's two instructions for PR #677, recorded in AEGIS-APR-114,
  where "every stage passed" comes from the question rather than the
  owner's prose:

  > I approve for you to merge once all checks are green. Including admin merge

  > if a check fails, diagnose and fix the issue and try to merge again. Do not stop until it is merged

- **Scope allowed:** The owner named no paths, engine or procedure; the
  following is the recorder's reading of "baseline refresh", modelled on
  AEGIS-APR-065. One pull request, from branch
  `claude/sharp-lovelace-urgxpz-fu2`, that regenerates, with
  `scripts/audit-skill-contracts.py` at engine v1.13.4 (SHA-256
  `e64b7430488c5f47c31faf1abcfa5f46aae876f3362ed8e0de105e988ff10153`) run
  unchanged on a clean checkout (`core.autocrlf=false`) of a commit on that
  branch that contains every change the pull request makes to an audited
  input (a file under `.claude/skills/`, `docs/skills-catalog.md`, or a file
  name under `.claude/agents/` or `docs/paths/`), checked out on a branch of
  the same name, exactly these files:
  `artifacts/audits/skill-contract-audit-baseline.json`,
  `artifacts/audits/corpus-route-graph.json`,
  `artifacts/audits/corpus-manifest-baseline.json` and
  `docs/audits/skill-contract-audit-baseline.md` with its hand-written
  preface; adds one dated note to `docs/audits/aegis-060-plus-register.md`;
  and appends this entry. The scanned commit's SHA is recorded in the
  regenerated files. Before that pull request merges, the files may be
  regenerated again whenever an audited input changes; the merged files are
  the output of the last such run. The same pull request also carries a
  one-line change to
  `.claude/skills/library-diff-reviewer/evals/trigger-evals.json`, which
  rests on the owner's direct request quoted above, not on this grant. The
  merge terms are those quoted above.
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
- **Expiry / use limit:** One pull request (recorder's reading: the request
  names one refresh, and the owner's selected option, "Faster, but two PRs
  are open at once", treats FU-2 as one pull request); consumed by its
  merge, which a later lifecycle event records.
```

The consumption event comes later, in a register-only PR after merge (coordinator decision; precedent APR-066/084). It records the merge
commit, head, paths, findings and whether S is reachable from main.

## 8. Drafts for the hand-written texts

Report preface: 15 `>` lines + a trailing blank line, replacing the current 15. It names S indirectly, through the generated `Repo SHA` line,
so it cannot disagree with it:

```markdown
> **What this page is.** The machine-generated summary of the latest
> skill-contract audit, for maintainers checking which skill texts the audit
> script flags for review. Everything below this note is script output.
>
> **Regenerated 2026-10-08 under AEGIS-APR-NNN** (an owner grant in the
> [approval register](../approvals/APPROVAL_REGISTER.md)) with engine v1.13.4,
> unchanged, over the Repo SHA below on branch
> `claude/sharp-lovelace-urgxpz-fu2`: a commit that contains every change the
> regenerating pull request (PR) makes to the files the audit reads (checkout
> with core.autocrlf=false, so the corpus hash is over LF (line feed,
> Unix-style line ending) bytes). The previous baseline (186 skills, 316
> findings, engine v1.13.4 over `5dbf7bc9e958d932bd0c5b093ebecfe61be41840`,
> PR #503 under AEGIS-APR-079) is in git history at
> `c14338d254bde3fd7fb9b8060033299cde5d5197` (#503's merge).
> Structural findings are not behavioral proof.
```

AEGIS-060+ note. Insert it after the blank line that follows "(PR #461's merge). The historical counts below are unchanged.", followed
by one blank line. Each `<…>` is a §5.3 output:

```markdown
**Baseline files regenerated, 2026-10-08.** Under AEGIS-APR-NNN, an owner grant
in the [approval register](../approvals/APPROVAL_REGISTER.md), the same four
files were regenerated with engine v1.13.4, unchanged, from `<S>` on branch
`claude/sharp-lovelace-urgxpz-fu2` (<N> skills, <F> findings, of which <R> are
ROUTE-002). Against the v1.13.4 baseline, <A> findings were added and <D>
removed, all ROUTE-002, <L> rows differ only in their line number, and the
<SEM> semantic-review candidates are otherwise the same rows; <SK> skills were
added and none removed. <K> ROUTE-002 rows name a skill pair absent from the
[2026-09-26 dispositions](../evidence/route002-dispositions-2026-09-26/README.md)
and are untriaged census rows. The v1.13.4 files remain in git history at
[`c14338d`](https://github.com/ModernNomad-98/Project-Aegis/tree/c14338d254bde3fd7fb9b8060033299cde5d5197/artifacts/audits)
(PR #503's merge). The historical counts below are unchanged.
```

"All ROUTE-002" is written only if `cmp.py` shows a single rule in both the added and removed sets. Otherwise, name the rules it reports.

## 9. Readability implications

- The planner's task message expected the regenerated `docs/audits` pages to "return to pending". BRIEF.md does not say this. Measured against the ledger's
  own rules, it is not what happens:
  - **The audit report is a generated report.** It is its own class (ledger "Generated reports (owner decision, 2026-09-28)";
    `build_index.py:65`), and each regeneration is verified by reproduction (R1–R4). Its format review was completed on v1.13.4 output in #503, and the format is unchanged.
    The hand-written preface needs an independent review covering every changed preface line.
  - **The AEGIS-060+ register is already provably pending** (148 lines). The note (about 14 lines) keeps it pending.
  - **The approval register is already provably pending** (4690 lines) and stays pending.
- Part D adds no Markdown file. It does not write the readability ledger (FU-1's file; the program is paused under AEGIS-APR-113), and it confers or claims
  no acceptance. The PR body states these facts for the ledger keeper (AEGIS-APR-101).

## 10. Checks

| Check | Command | Expected | Where it runs |
| --- | --- | --- | --- |
| C1 | R1/R2/R4 (§5.1) at S | | local |
| C2 | R3 (§5.2) at H | | local |
| C3 | `validate-skills.py` | | local |
| C4 | `test_validator.py` | `TMPDIR` outside the checkout | local |
| C5 | `test_audit_skill_contracts.py` | | local |
| C6 | `test_markdown_links.py` and the corpus link check | `broken: 0 dead: 0` | local |
| C7 | BER self-check and offline suite | | **not run locally** (coordinator rule); CI `validate-skills` steps `ber-self-check`/`ber` at H are the declared evidence |
| C8 | §5.3 scripts on the committed JSON | values written in the 060+ note | local |
| C9 | AC-1 path list | | local |
| C10 | gate-guard pattern over that list | no match | local |
| C11 | ID uniqueness / max+1 | | local |
| C12 | AC-12 freshness | | at Stage E and Stage G |

- **CI required checks:** `validate-skills` and `gate-guard`.
- **Path-scoped jobs:** tools jobs and `windows-offline-checks` are recorded as **skipped, not green** (coordinator decision).

## 11. Acceptance criteria

`B` = `git merge-base H <BASE>`, where `<BASE>` is `$REPO`'s `origin/main` after a fresh fetch.

- **AC-1** `git diff --name-only B H` = the six §6 paths plus `.claude/skills/library-diff-reviewer/evals/trigger-evals.json`, and
  nothing else. No path matches the gate-guard pattern.
- **AC-2** `scripts/audit-skill-contracts.py` is unchanged vs `<BASE>`. Both JSON files record `version 1.13.4` and
  `engine_sha256 e64b7430488c5f47c31faf1abcfa5f46aae876f3362ed8e0de105e988ff10153`.
- **AC-3** Both JSON files record `repo_sha = S`, `branch = claude/sharp-lovelace-urgxpz-fu2`, `working_tree_dirty false` and
  `dirty_paths_in_scanned_surfaces []`. S satisfies §4.1:
  - `git merge-base --is-ancestor S H` succeeds;
  - `git diff --quiet S H -- .claude/skills docs/skills-catalog.md .claude/agents docs/paths` succeeds.
- **AC-4** R1/R2: four runs across two fresh clones of S are byte-identical, and equal to the committed JSON files.
- **AC-5** R4: the committed report minus lines `3..2+P` is byte-identical to the generated report.
- **AC-6** The preface matches §8 in substance: it names the new grant ID, refers to the Repo SHA line, and contains no "description edit"
  or stale APR-079 claim. It has an independent line-by-line review.
- **AC-7** The 060+ change is one inserted hunk with 0 deleted lines. In `git diff -U0 B H -- docs/audits/aegis-060-plus-register.md`, the
  single `@@` line matches `-<a+1>,0 +<a+2>,` (a = line of the anchor sentence in `B`; 120 at `c060a7cb`). Each `<…>` value equals the
  §5.3 output on the committed JSON (OLD = `c14338d2`).
- **AC-8** R3 at the final head H: the only differences from the committed files are one `repo_sha` line per JSON and the report's `- Repo SHA:`
  line. The route graph is identical.
- **AC-9** The register change is one hunk with 0 deleted lines, appended at the end. `git diff -U0 B H -- docs/approvals/APPROVAL_REGISTER.md`
  shows exactly one `@@` line, matching `-<n>,0 +<n+1>,` (n = `git show B:docs/approvals/APPROVAL_REGISTER.md | wc -l`; 5062 at `c060a7cb`).
  Its ID is unique and equals max+1 at merge. It quotes all eight owner strings verbatim from BRIEF.md.
- **AC-10** C3–C6 pass at H, with their tell-tale lines quoted. C7 is declared CI-only and shown by the CI job result at H.
- **AC-11** The PR body states:
  - the security-relevant surface: **Yes — the owner approval register** (MG5 extra review not required for an agent PR);
  - the §9 readability facts;
  - K and the untriaged rows;
  - the skipped jobs as skipped;
  - the "Aegis skills used" table.
- **AC-12** (freshness, at Stage E and again at Stage G) After `git fetch origin main`, either `git merge-base --is-ancestor origin/main H`,
  or both of these hold:
  - `git diff --quiet B origin/main -- .claude/skills docs/skills-catalog.md .claude/agents docs/paths`;
  - `git diff --name-only --diff-filter=DR B origin/main` is empty.

  Otherwise, merge `origin/main`, regenerate, and re-run AC-3 to AC-9.

**Declared not verifiable at this plan's revision (SD-A):**
- the exact values (measured at S, predicted in §5.3);
- AC-3 to AC-9 and AC-12 (they need S and H);
- CI results (they need a push);
- whether S stays reachable from main after merge (merge method, R-1);
- the final ID number.

## 12. Risks

- **R-1 Provenance after merge.** A squash merge leaves S reachable only through the PR head ref, and a rebase merge rewrites it. Corpus identity still
  rests on `corpus_content_hash`. The coordinator prefers a merge commit; the consumption record states what happened.
- **R-2 E1 revised after regeneration.** AC-3 and AC-8 catch it; regenerate.
- **R-3 Base moves (FU-1 merges first).** Merge `origin/main`, do not rebase. AC-12, then AC-8.
- **R-4 ID collision at merge.** Renumbering touches three files (register heading, preface, 060+ note) and moves the head, so Stages D, E and F
  re-run at the new head. AC-9 and C11 re-check the ID.
- **R-5 Grant read wider or narrower than the owner's words.** Verbatim quotes; every recorder's reading is labelled; no invented prohibitions.
- **R-6 The 24 new ROUTE-002 rows misread as defects.** The note and the PR body state they are info-level, census and untriaged.
- **R-7 The large generated diff hides a hand edit** (rehearsed: +1185/−143 JSON lines). AC-4 requires byte-equality with fresh engine output.
- **R-8 Stale `origin/main` in scratch clones.** All base SHAs come from `$REPO` after a fetch (§5 pitfall).

## 13. Follow-ups (not in this PR)

1. CONSUMED event for the grant, in a later register-only PR (coordinator decision).
2. Rows in the open-decisions page and the forecast are FU-1-owned or coordinator-sequenced; Part D does not touch them.
3. Optional triage of the untriaged ROUTE-002 rows is an owner decision.

## 14. ETA

Part D implementation after the E1 commit: **45–90 min active**. Each re-regeneration: 15–20 min. Agent estimate, unmeasured.

## 15. Skills used (this stage)

| Skill | How applied | Result |
| --- | --- | --- |
| `scoped-approval-register` | Re-applied to the rev2 grant: verbatim quotes, each with the question it answers. The recorder's readings are labelled (scope, "same terms" referent, one-PR limit). No invented prohibitions ("None additionally stated"). The seventh path is attributed to its own authority. Draft only. | §7 |
| `change-classification-gate` | Re-classified with the E1 decision: Part D is docs-only; the PR is ai-agentic by location. | §3 |
| `risk-tiered-validation-selector` | Fail-closed FULL. The BER checks are declared CI-only under the coordinator rule. Selects; executes nothing. | §3, §10 |
| `skill-quality-reviewer` | Scope re-confirmed: it reviews ONE skill and does not own Part D. Not applied. | — |

No skill owns writing a plan. Stage A is procedural (docs/delivery-workflow.md, "Recorded deviation").

## 16. Handoff

- **Decisions:** SD-A…SD-G and MG1–MG5 are unchanged. The coordinator decisions are applied: E1, variant A, E1 then D, merge commit preferred, consumption later, skipped recorded as skipped.
- **Changed repository files:** none.
- **Scratch:**
  - rev1 work: `…/fu2/dwork/`
  - rev2 work: `…/fu2/dwork2/`, containing `tools/{cmp.py,k_untriaged.py,skills_diff.py}`, `clone-e1` (S=`daa3459d…`, H=`66c7418e…`), `cloneH` and `outH`
- **Deviations:** the B-D1 definition is new wording in the grant. R-8 and AC-12's DR check go beyond what the audit asked.
- **Continuation:** Stage B re-audits this file's captured sha256. The implementer commits E1, then runs §5 and makes the single D commit.
