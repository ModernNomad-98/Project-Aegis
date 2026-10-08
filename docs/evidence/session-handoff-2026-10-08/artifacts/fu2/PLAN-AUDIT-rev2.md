# PLAN-AUDIT rev2: FU-2 Part D, Stage B independent plan audit (round 2)

Auditor: the same Stage B subagent as round 1 (`PLAN-AUDIT-rev1.md`, sha256 `9acd2e50…72a5fab`). I wrote neither plan, and I hold no other stage.
Repository: `/home/user/Project-Aegis`, Role A.
Base: `git fetch origin main; git rev-parse HEAD origin/main` → `c060a7cb09758fa2f4f6b67ab00094f01d7c6a46` (both). `git status --short | wc -l` → `0`, at start and at end.
Method: read-only. All Python ran with `-B`; scratch scripts also ran with `-I`. Scratch clones are under `…/fu2/b-audit2/`. Nothing was written to the repository or to GitHub.
Started 2026-10-08T14:51:19Z. Hashes re-checked at 14:54:51Z.

## Captured revision and verdict

| Plan | sha256 (identical at start and end) | Verdict |
| --- | --- | --- |
| `PLAN-D-rev2.md` | `9490f2c1b116ac34de33945b44dc783aad30b7564083ea6f581c4f98a44895a2` | **`SD-B: ACCEPT`** |
| `PLAN-D-rev1.md` (unchanged) | `d1152150…a9df56` | superseded by rev2 |
| `PLAN-E-rev1.md` (unchanged) | `22d0f970…31499b9a` | `SD-B: ACCEPT` stands (round 1) |

`BRIEF.md` is unchanged (`e504a786…48597`).
The tokens are from `docs/delivery-workflow.md:129`.

Coordinator rule applied: I did not run the BER self-check or the offline BER suite locally. The declared evidence is the CI `validate-skills` job's steps `ber-self-check` and `ber` (`validate-skills.yml:229-233`).

## Round-1 blocking findings: all resolved

**B-D1, one definition of S: RESOLVED.**
- §4.1 states one definition: "a commit on branch `claude/sharp-lovelace-urgxpz-fu2` that contains every change the pull request makes to an audited input; its SHA is recorded as `repo_sha`".
- The same definition appears in §4.2/§5.1, in the grant's *Scope allowed* (`diff` rev1→rev2 of the grant block: lines 57–61), in the preface ("over the Repo SHA below …: a commit that contains every change the regenerating pull request (PR) makes to the files the audit reads") and in AC-3.
- The old wording ("last commit that changes" / "last change to an audited input") is gone: grep finds no hit.
- The GRANT is pinned to the D commit (§4.2.2).

I reproduced it myself with the real drafts:
- S = `d7e64978…` (E1 commit), H = `baa7b824…`.
- §5.1's check `git diff --name-only $(merge-base S BASE) S -- <audited>` → only `…/library-diff-reviewer/evals/trigger-evals.json`.
- AC-3: `merge-base --is-ancestor S H` passes, and `git diff --quiet S H -- .claude/skills docs/skills-catalog.md .claude/agents docs/paths` passes.

Robustness:
- **Scenario A** (a fake FU-1 commit on main that changes only `docs/offline-ci.md`, merged into the branch after D → H2 `c509a976…`): AC-3 still holds, and R3 at H2 shows only the `repo_sha` line in each JSON, 0 graph lines, and only the `- Repo SHA:` line in the report.
- **Scenario B** (main changes `.claude/skills/adr-writer/SKILL.md` and is not merged in): AC-12's audited-path diff exits **1**, and `is-ancestor main H2` exits **1**. So staleness is detected and regeneration is required.

**B-D2, E1's measured effect restated: RESOLVED.**
- `grep -n -i 'description edit' PLAN-D-rev2.md` finds only two places: the §0 fix table (:14) and AC-6's negative test (:501).
- E6 (:82-89) gives E1's measured effect: findings, rule inventory, census, graph and manifest `skills` are equal; bytes 5193047 → 5193044; corpus hash `899ddf10…` → `673e7fe9…`. This matches my round-1 measurement and my fresh round-2 run ("corpus hash 673e7fe93c6ddfb8…", "findings: 339 …").
- §3 now classifies the PR as ai-agentic **by location** (no routing text changes).

**B-D3, mechanical definitions and inline scripts: RESOLVED.**
- §5.3 defines added/removed, line-only, semantic, K and skills.
- I extracted the three Python blocks from the plan file. Their sha256 equal the stated values and the `dwork2/tools/` copies:
  - `cmp.py` `5f6ec1fe…`, identical to my own `b-audit/tools-b/cmp.py`
  - `k_untriaged.py` `6f426070…`
  - `skills_diff.py` `265495ad…`
- I re-ran them myself. OLD = `git show c14338d2:artifacts/audits/…`. NEW = my fresh E1 regeneration in a new clone.
  - `counts 316 -> 339`
  - `added (ignoring line): 24 {'ROUTE-002': 24}`
  - `removed (ignoring line): 1 {'ROUTE-002': 1}` (agent-harness-architect → model-context-designer)
  - `rows differing only in line: 8 {'ARTF-001': 8}`
  - `semantic multiset equal ignoring line: True 84 84`
  - `ROUTE-002 rows: 255 K (pair absent from dispositions): 24` (the one-target assert passed)
  - old baseline: `K …: 0`
  - `skills 186 -> 195 | added 9 [...] | removed 0 []`
- So **24 / 1 / 8 / 84 / K = 24 / +9** all reproduce.

## Round-1 nits: all addressed

- **N-D1:** the *Expiry* line now reads "(recorder's reading: … 'Faster, but two PRs are open at once' …)".
- **N-D2:** the question's parenthetical is primary, and the APR-114 mapping is labelled "Recorder's reading", with "every stage passed" attributed to the question. This matches APR-114's own Scope FORBIDDEN.
- **N-D3:** the seventh path is attributed to the owner's direct request, not to this grant.
- **N-D4:** §9 attributes the premise to the planner's task message. I cannot see that message, so the attribution is **unverified by me**, but it no longer cites BRIEF.md.
- **N-D5:** AC-12 freshness is defined, and I tested it (scenario B above).
- **N-D6:** hunk checks rehearsed with the **real** drafts: 060+ note `@@ -121,0 +122,13 @@`, numstat `13 0`; register `@@ -5062,0 +5063,90 @@`, numstat `90 0`, where `git show B:… | wc -l` = 5062. The anchor sentence is unique (`grep -n` → only :120), and :121 is blank. After the append: 0 duplicate IDs, max 119.
- **N-D7:** R-4 names the cost of renumbering.
- **N-D8:** "author dates 2026-09-28 to 2026-09-29 UTC" is correct. 287bf5b7 is 2026-09-29T00:15Z; the other eight are 2026-09-28 UTC.
- **N-D9:** C7 is declared CI-only.

## New R-8 pitfall: confirmed

- `git -C /home/user/Project-Aegis rev-parse main` → `03c93c77…`.
- A clone of the local path (`b-audit2/e1`) reports `rev-parse origin/main` → `03c93c77…`, and `remote -v` → `/home/user/Project-Aegis`.
- The real worktree's `origin` is the GitHub URL and its `origin/main` is `c060a7cb`.
- The planner's own rehearsal clone (`dwork2/clone-e1`) shows the same stale `origin/main`.
- Round 1 used explicit SHAs everywhere, so its results stand.

## Grant still verbatim and invents nothing

- After normalising blockquote markers and whitespace, all eight owner strings are byte-present in both BRIEF.md and the rev2 grant. The two APR-114 quotes and the cited option text are present in the register or BRIEF.md.
- The grant diff rev1 → rev2 is exactly five hunks: the author-date wording, the labelled "same terms" reading, the S definition, the scanned-SHA sentence plus the seventh-path sentence, and the labelled Expiry.
- No prohibition, expiry or limit was added beyond rev1. FORBIDDEN still says "None additionally stated by the owner".

## Other re-checks

- Preface draft: 15 `>` lines (awk count).
- My full rehearsal with the real drafts:
  - R4 → `R4 body == generated` (P = 16).
  - AC-1 → exactly the 7 expected paths.
  - R3 at H → one `repo_sha` line changed in each JSON (old and new), graph 0, report only the `- Repo SHA:` line.
- The planner's E14 rehearsal (`dwork2/clone-e1`: `daa3459d` / `66c7418e`, hunks `-5062,0 +5063,4` / `-121,0 +122,3`, 7 paths) is confirmed by `git log` and `git diff`.

## Nits (non-blocking; for the implementer and the Stage D/F reviewers)

- **N2-1. "Audited input" is listed two ways.** The grant's parenthetical list (skill files, catalog, agent and path file names) omits §4.1's REF-001 item (Markdown-link targets existing on disk; engine `audit-skill-contracts.py:785`). This is practically moot: the PR deletes nothing, R3 and AC-12's `--diff-filter=DR` cover it, and there are 0 REF-001 findings at the base. Still, the plan's claim that the term is "defined once" is slightly overstated. Optionally add "or the existence of a Markdown link target" to the grant's parenthetical.
- **N2-2. R-8's fix assumes `$REPO`'s origin is GitHub.** If the implementer works in a clone of the local path, `git -C "$REPO" fetch origin main` fetches the stale local `main` (`03c93c77`), and BASE is wrong. Add a guard in §5.1 and in AC-12: `git -C "$REPO" remote get-url origin` must be the GitHub URL, or BASE must equal `git ls-remote origin refs/heads/main` taken against GitHub.
- **N2-3. Seventh-path sentence.** "rests on the owner's direct request quoted above" implicitly includes the coordinator's E1 reading of that request: #542 had already aligned the frontmatter. Optionally add "(as the coordinator read it: the residual eval-file note)".
- **N2-4. AC-7 hunk pattern.** The 060+ insertion sits between two blank-line boundaries. A different note text could, in principle, make `git diff` slide the hunk one line (`-120,0 +121,`) without any content difference. With the real draft it did not slide. If AC-7 ever fails only on the hunk header, check the content instead: B's file with the block inserted after line 121 must equal H's file.

## Skills used

- **`scoped-approval-register`** (SKILL.md and `references/register-format.md`, read in round 1 and re-applied). Checks: verbatim capture, recorder's readings labelled, no invented prohibitions or limits, prior grants unchanged. Result: passes. N2-3 is optional.
- **`skill-quality-reviewer`**: **scope re-confirmed; not applicable to Part D.** It reviews one skill's quality. Part D changes no skill. It was not used in this round.
- Stage B itself is procedural (`docs/delivery-workflow.md`, "Recorded deviation").

## Not run

- BER self-check and offline suite (coordinator rule; CI `validate-skills` is the evidence).
- CI on a pushed head (no push).
- Live-model checks.

## Handoff

- Binding decisions SD-A…SD-G and MG1–MG5 are unchanged. The coordinator decisions (E1, variant A, E1 then D, merge commit preferred, consumption later, skipped recorded as skipped, BER CI-only) are all reflected in rev2.
- Routing: Part E (`22d0f970…`) and Part D (`9490f2c1…`) are both `SD-B: ACCEPT`. The implementer commits E1 first, then the single D commit per rev2 §5, and applies N2-2.
- Scratch: `…/fu2/b-audit2/` contains:
  - `extracted/` (the plan's three inline scripts)
  - `e1/` (S `d7e64978`, H `baa7b824`, H2 `c509a976`, branch `fake-main`)
  - `out/`, `r3H/`, `r3H2/`
  - the filled drafts `grant-f.md`, `preface-f.md`, `note-f.md`
