# Skill-Preservation Guard

A deterministic, offline, read-only check that reports when the shipped Aegis skill library loses a
skill, a required supporting file, discovery coverage or availability. It **reports only**: it never
repairs, prunes, deletes, installs or writes inside the scanned tree.

**Status of this slice:** local-only tool plus a generated baseline. **It is NOT wired into CI.**
CI wiring is a separate owner-gated decision (program decision OD-W04-1; it would touch the
gate-guard-protected workflow surface and needs its own authorization and review). The repository's
required merge gate is unchanged; this tool does not block merges today.

## Quick start

Run from a repository checkout root (a candidate tree to inspect) with a baseline JSON that was
generated from a clean, reviewed baseline tree:

~~~text
# 1. Build a baseline from a clean baseline tree (write OUTSIDE that tree; atomic write)
python -P -B tools/skill_preservation/check_skill_preservation.py baseline     --tree <clean-baseline-tree>     --out <evidence-dir>/skill-baseline.json     --source-revision <40-hex-revision>

# 2. Check a candidate tree against the baseline (read-only; JSON to stdout)
python -P -B tools/skill_preservation/check_skill_preservation.py check     --tree <candidate-tree>     --baseline <evidence-dir>/skill-baseline.json     --json
~~~

The committed generated baseline for this slice is at
tools/skill_preservation/baseline.json and was generated from the verified baseline tree
(tree 4e584f59287f8b8fc3d10d3567158f52bff99a18, revision f69c6e9219335d1979b8ec9658cc86e0a7a5583a).

## Exit codes

| Exit | Meaning |
|---|---|
| 0 | no BLOCK findings (a clean result, or warnings/info/unrun only) |
| 1 | at least one BLOCK finding |
| 2 | usage or input error; fail closed - missing/malformed/tampered baseline, unknown baseline schema, missing or empty candidate tree, output/report path inside the scanned tree, symlinked tree or baseline, duplicate/case-colliding baseline paths |
| 3 | internal error |

**WARN**, **INFO** and **UNRUN** entries are reported but do not fail the run. BLOCK entries fail it.
An UNRUN item is never a pass.

## What the check verifies

BLOCK findings (availability loss; fail closed):
- **Disappeared Skill** - a baseline skill directory is absent from the candidate.
- **Renamed or Hidden Skill** - a missing skill whose SKILL.md bytes reappear under a new skill id.
- **Missing Supporting File** - a baseline per-skill file (SKILL.md, references, evals) is missing.
- **Discovery Omission** - a skill is no longer mentioned in docs/skills-catalog.md or the README
  roster; a skills-manifest entry is dropped; or the manifest schema/hash_input semantics changed.
- **Silent Disable** - a previously active skill gains disable-model-invocation: true and/or the
  exact 32-character MANUAL-ONLY description sentinel (both variants BLOCK).
- **Name/Directory Mismatch** and **Empty Description** - frontmatter no longer matches the tree.
- **Declared Installed-Set Reduction** - a source-side file or skill declared in
  docs/consumer-starter-package.md is missing from the candidate.
- **Added Path in Skill Surface** - any candidate-added file under .claude/skills/.
- **Cleanup-Path Addition (BLOCK)** - a removal-looking path that names skills inside this tool's own
  package (the guard acquiring a removal path is explicitly forbidden).

WARN / INFO findings (reported, not failing):
- content-only SKILL.md changes (typo fixes and approved improvements are allowed; the repository
  validator remains the per-tree strictness gate), added skill files, added skills, added manifest
  entries, a changed starter-package definition (a reviewed re-pin decision is required), a
  removal-looking added path outside the skill surface (name/path rule only), and frontmatter the
  guard's line parser cannot read (the validator is authoritative).

UNRUN (reported, never PASS):
- a consumer install record: no consumer install-record format or target is authorized, so
  installed-set evidence is UNRUN. Only the source-side declared set is checked.

## Limits

- Baseline JSON is a **generated artifact reviewed in a change**, not repository history. When an
  approved availability change occurs, re-freeze the baseline deliberately (a reviewed change with a
  recorded reason); the freeze rule is program decision OD-W04-2 and is not decided by this tool.
- The frontmatter reader is a minimal line parser for the three invariants the guard needs. It never
  reasons from a parse failure to a BLOCK; the repository validator is the strict YAML gate.
- The cleanup-path rule is a deterministic name/path rule over candidate-added paths only; it does
  not scan file contents and does not detect a renamed pre-existing cleanup tool.
- Byte identity is not functional availability. A guard pass does not prove the validator passes, and
  the validator does not prove preservation; run both. Neither one repairs anything.
- The check is local evidence only. It is not a required check, not a CI result, not a merge gate and
  not a consumer-install proof.

## Relationship to the repository validator

scripts/validate-skills.py validates the current tree strictly (structure, frontmatter, manifest
identity, catalog/README coverage). This guard compares a candidate tree to a frozen baseline and
reports reduction. The guard does not duplicate the validator's job and never replaces it.

## Tests

~~~text
python -B -m unittest discover -s tools/skill_preservation/tests -p "test_*.py" -v
~~~

Tests use synthetic temporary fixtures only; they need no network, no credentials and no repository
data beyond the tool source. The suite covers the acceptance matrix C01-C26 (including the negative
and adversarial cases) and the baseline determinism/tamper checks. Two host-limited cases are
documented as UNRUN: case-variant directories and non-UTF-8 path bytes cannot be created reliably on
this Windows host; the corresponding baseline rejection paths are exercised instead.

## Files

| File | Purpose |
|---|---|
| check_skill_preservation.py | The guard CLI (standard library only; no network; no subprocess). |
| baseline.json | Generated, schema-versioned baseline of the shipped skill library. |
| README.md | This file. |
| tests/__init__.py | Test package marker. |
| tests/test_skill_preservation.py | Synthetic-fixture self-tests. |
