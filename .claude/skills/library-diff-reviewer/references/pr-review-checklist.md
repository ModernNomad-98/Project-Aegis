# Library diff review — per-area criteria and procedures

Companion to [../SKILL.md](../SKILL.md). Everything here operates at the PR
level; single-skill judgment lives in `skill-quality-reviewer` and is
composed, never restated.

## Area 1 — registration consistency: pass criteria

The mechanical validator already proves each skill NAME appears in the
catalog and README. This area checks what presence cannot:

| Check | PASS means | Typical FAIL |
| --- | --- | --- |
| Placement | Each added skill sits in the catalog section/cluster its scope claims | New meta-skill filed under a product pack |
| Summary truth | The catalog/README row describes what the skill actually does | Row copied from a sibling and half-edited |
| Post-merge voice | Status text reads true AFTER merge | "added in this branch", "this PR ships…" |
| Graduation | A banked candidate the PR builds is marked built at its banking site | Candidate table still says "not built" |
| Decision entry | A dated decision-log entry exists, matches the diff, and APPENDS (older entries untouched) | Entry missing, undated, or an older entry edited |
| Count arithmetic | The before→after count agrees at every site (see list below) | One site still shows the old total |

### Count-arithmetic site list

Sweep every place a skill count or skill list appears. In a typical library
repo that is at least:

- the catalog status block or header,
- the README narrative paragraph(s),
- the README phase/status table,
- any "map of the system" or overview count,
- the new decision-log entry itself,
- CI/validator expectations if a count is pinned anywhere.

Historical decision entries stating older counts are IMMUTABLE — they were
true when written. Never "fix" them; the new entry records the new total.

## Area 2 — collision sweep: shipped AND in-batch

1. For each added or trigger-modified skill, compose `skill-quality-reviewer`
   (its check 2 sweeps the shipped corpus and NAMES colliders).
2. PR-level addition — the sibling sweep: pairwise-compare the descriptions
   of all skills added in this PR against each other. For each pair, ask:
   is there a plausible request for which a model could not decide the
   winner? If yes, the pair is a finding: quote the request, name the pair,
   and require a discriminating case in BOTH skills' trigger-evals plus
   yield clauses in their Use When sections.
3. A collision with shipped discrimination already in place (trigger-evals
   naming that exact neighbor on both sides) is a documented seam — PASS
   with citation, not a finding.

## Area 3 — diff coherence: classification rules

Classify every changed file exactly once:

| Class | Coherent when |
| --- | --- |
| New skill directory | Skill named in the stated intent |
| Modified skill | Modification declared, or it is the pinned other half of a seam the intent names |
| Registration doc | Edit matches the declared count/status change |
| Decision log | Appends a new dated entry only |
| Anything else | Declared explicitly in the intent — otherwise a finding |

Undeclared deletions and edits to skills the intent never mentions are
findings even when the edits look like improvements — one intent per PR;
drive-bys go to their own PR.

## Area 4 — inner-loop conventions

- Run `skill-quality-reviewer` per added skill and per substantially
  modified skill (a description/trigger rewrite is substantial; a typo fix
  is not).
- Verdict inheritance: any inner-loop revise or reject ⇒ PR verdict is
  REQUEST CHANGES. Inner-loop ship for every skill is necessary but not
  sufficient — areas 1–3 can still block.
- Do not re-run the inner loop's checks at the PR level; cite its verdicts.

## Retirement-PR checks

When the PR removes or deprecates a skill:

- Registration rows MOVE to a retired record (catalog retired section,
  decision-log entry) — a skill that simply vanishes from the lists is a
  FAIL.
- Reverse-link sweep: search every remaining `SKILL.md`, every
  `trigger-evals.json` (`expected_skill`, `should_not_trigger`,
  `overlaps_with`), the catalog, the README, and any agent definitions for
  the removed skill's name. Every surviving reference must be repointed,
  rewritten, or explicitly annotated as historical.
- Count arithmetic decrements at every site (same list as area 1).
- Plan conformance: when a `skill-deprecation-planner` plan exists, the
  executed steps match it; deviations are findings, not improvisations.

## Post-merge re-verification (squash-merge platforms)

- The merged result is ONE commit on the default branch; the PR's individual
  commits do not exist there. Re-verify against the merged tree at that
  squash SHA — not against the branch.
- Rollback of a bad library merge is an ordinary `git revert <squash-sha>`
  producing one revert commit; no merge-commit `-m` parent selection is
  involved.
- If the review must reason about merge PROCESS (who armed auto-merge, in
  what order events fired), stop — that trail is `agent-governance-audit`'s
  target, and auto-merge timeline events are strategy-specific there.

## Freshness tells (validator evidence)

- The CI run's recorded head SHA ≠ the PR's current head → stale, reject.
- "It passed locally yesterday" → not evidence; re-run on the pinned head.
- A pass pasted into the PR body with no run linkage → claim, not evidence.
