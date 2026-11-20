# Skill reachability reporter (local-only)

This directory is a **local-only** tool. It is **not wired into CI**, and it runs no network calls. It ports the
`_gap-plans/measure-routed.py` D-23 measure into the repository so the same tier counts can be reproduced from a
checkout. It is read-only inside the scanned tree; the only write is an explicit `--json OUT` path outside the tree.

## What it measures

For every skill in `.claude/skills/` it reports exactly one D-23 tier, first match wins:

- **door** — named by a front door: the README `### Start here: pick your path` section, `CLAUDE.md`, `AGENTS.md`,
  a `docs/paths/` page linked from that README section, or `project-orchestrator` (SKILL.md and `references/*.md`).
- **play** — named in the SKILL.md or `references/*.md` of a door-named conductor (a skill whose name ends in
  `-orchestrator`, other than `project-orchestrator`).
- **handoff** — named on a routing line of a door- or play-named skill's SKILL.md (arrow, `route(s) to`,
  `invoke`, `hand off/over/to`, `delegate to`, `belongs to`, `owned by`, `goes to`).
- **none** — none of the above.

`routed` is `door + play`; `handoff` is reported separately because a user only reaches it if an earlier skill
sends them on. A mention never counts when its line contains `do not use` (any case), and names match as whole
kebab names (`ai-threat-modeler` is not `threat-modeler`). Guide links are normalized by stripping a
`#fragment` before matching, so `(docs/paths/guide.md#start)` counts as linked.

## What it does not prove

The GAP-EXECUTION-PLAN-r1 section 1.4 limit is quoted exactly:

> It counts names. It does not prove a first-time user can follow a route.

Additional limits below are the author's own, not section 1.4: this measure does not prove consumer readiness,
user success on a real task, skill quality, eval detection, or that an unreachable skill is unneeded. A
name-only-by-design allow-list entry is a policy record, not evidence of use.

## Source-library role check

Before measuring, the tool verifies that REPO is the Project Aegis **source library**, not a consumer
repository that copied `.claude/skills/`: `README.md` must start with `# Project Aegis`, and
`docs/skills-catalog.md`, `scripts/validate-skills.py` and
`artifacts/audits/skill-contract-audit-baseline.json` must exist. A directory that fails any landmark is
rejected with exit 2 instead of producing a misleading library report.

## Allow-list (name-only by design)

`allow-list.json` records exactly the nine T-08 batch-f rows that were triaged name-only by design, with the
schema `aegis.skill-reachability-allow-list/1`, `expected_count` 9, and for each row `name`, `tier_at_triage`,
`triage_row` and `reason`. Tier at triage is historical provenance: the checker tolerates a move between `none`
and `handoff` while the skill stays unrouted, and fails on a routed (`door`/`play`) skill, a missing name, a
duplicate, a blank reason, a wrong count, an unknown skill, or a missing/malformed manifest entry (a manifest
that is valid JSON but not an object with a list of object entries is reported as an `allow-list: FAIL`
diagnostic, not a traceback). The checker also pins the exact historical nine name-to-triage_row mapping
(eval-runner-designer 9, framework-edition-tracker 17, framework-mapping-refresher 18, library-diff-reviewer 10,
skill-deprecation-planner 11, skill-quality-reviewer 12, skill-usage-instrumenter 13, skill-usage-ledger 3,
source-currency-auditor 19), so a substituted, added or renumbered name fails even if it is still unrouted.
The allow-list is not a routing waiver: `--require` on an allow-listed name still exits 1.

## Commands

```console
python -P tools/skill_reachability/measure_routed.py .                  # default measure
python -P tools/skill_reachability/measure_routed.py . --list           # list unrouted skills and tiers
python -P tools/skill_reachability/measure_routed.py . --require name1,name2
python -P tools/skill_reachability/measure_routed.py . --json OUT.json  # explicit write; OUT must resolve outside REPO
python -P tools/skill_reachability/measure_routed.py . --check-allow-list
python -P tools/skill_reachability/measure_routed.py . --check-allow-list --allow-list PATH
```

The options `--json`, `--require` and `--allow-list` each require a value; a missing operand is a usage error
(exit 2). Recognized options are `--json`, `--require`, `--allow-list`, `--list` and
`--check-allow-list`; unknown options and unexpected positional arguments are rejected with the same usage error
(exit 2), so a typo such as `--check-allowlist` cannot fall through to a normal measure. A write failure on
`--json OUT` (for example a missing parent directory) is reported as an output error (exit 2) instead of a
traceback. `--json OUT` must resolve outside REPO; an OUT path inside the scanned tree (for example
`--json report.json` with REPO `.`) is rejected with exit 2 before any write, preserving the read-only
guarantee inside the tree.

Exit codes: `0` = ran (and every `--require` name is routed; in check mode the allow-list is valid); `1` = a
`--require` name is not routed or the allow-list check failed; `2` = a usage/role/containment error — the path
does not look like the Project Aegis source library, the README door section is missing, an option has no value,
or `--json OUT` resolves inside REPO. `--check-allow-list` is an additive local-only mode: default output is
unchanged and the allow-list is never read in default mode.

## Provenance and status

The script is a behaviour-preserving port of the D-23 `_gap-plans/measure-routed.py` (8,021 B / 183 LF /
sha256 `01d6ec3f55522a584122f25c13b57ae84d9ff6089706bd76e5910a3005fcf750`): same tiers, name matching,
exclusion rule, routing-line grammar, stdout lines, JSON schema, `--list` output and 0/1/2 exit codes. The only
added behaviour is the optional `--check-allow-list` mode and its `--allow-list` override, plus the role check,
operand validation and output-containment guards described above; usage text documents those flags. Standard
library only.

Local-only status: this tool is not referenced by `.github/workflows/` or any script and is not part of CI.
CI wiring, a validator/engine rule, or a skill-standard line for it is a separate owner-gated decision (P-2) and
is deliberately out of this task; the precedent `tools/skill_preservation/` is likewise local-only.

## Tests

The fixture tests are local-only and use temporary directories; no fixture files are committed.

```console
python -P -m unittest discover -s tools/skill_reachability/tests -p 'test_*.py' -v
```

Run the suite under the workspace guard. The guard snapshots every file and directory in the checkout
(tracked and untracked alike; the top-level `.git` metadata entry is the only exclusion) before and after
the run, and fails on any entry added, removed or modified. This is the issue #1140 test-hygiene guard: the
T-13 review found that a test had deleted a pre-existing repository file, and the guard makes that class of
regression fail instead of passing silently. The committed unit tests plant a deleting test in a temporary
fixture tree and prove the guard catches it.

```console
python -P tools/skill_reachability/tests/workspace_guard.py            # guard the default local suite
python -P tools/skill_reachability/tests/workspace_guard.py -- COMMAND # guard any other command
```

Guard exit codes: `0` = the command exited 0 and the tree is unchanged; `1` = the tree changed or the
command exited non-zero; `2` = usage error (bad option, missing tree, empty command). The guarded command
runs with `PYTHONDONTWRITEBYTECODE=1` so interpreter bytecode caches written inside the tree are not
misreported as mutations.

## Limitations

- It counts name mentions in a fixed set of front-door and routing sources; it does not build a dependency graph
  and does not execute skills or evals.
- It does not judge whether a routed skill is reachable in a consumer install, whether the starter package
  includes it, or whether a user can complete a task with it.
- The tier is a static classification; page or skill edits move it, and re-running the measure is required
  after such edits.
