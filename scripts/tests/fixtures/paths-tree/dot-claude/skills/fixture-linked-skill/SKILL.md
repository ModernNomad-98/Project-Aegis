# Fixture link target

NEUTRAL SYNTHETIC TEST-FIXTURE SOURCE for `scripts/tests/test_validator.py`, not
a shipped skill. It is stored under a neutral `dot-claude/` directory on purpose:
`test_docs_paths_links` copies this `paths-tree` fixture into a throwaway
temporary repository and materializes `dot-claude` -> `.claude` ONLY there, so
the link-resolution cases run against a real `.claude/skills/...` target without
this file ever living under a literal `.claude/skills/` path in the tracked tree.

WHY the neutral layout (correction of record, Gate 2.8): the Claude Code SESSION
harness discovers ANY nested `.claude/skills/**/SKILL.md` and exposes it as a
live, invocable session skill — regardless of frontmatter. An earlier rationale
claimed a no-frontmatter fixture at a nested `.claude/skills/` path was
"undiscoverable"; that was FALSE (it only holds for `scripts/validate-skills.py`,
which scans the repo-root `.claude/skills/` only). Keeping this source under
`dot-claude/` is what actually prevents the contamination. This file must never
be discoverable as a live Project Aegis session skill.

It has no frontmatter on purpose: the link-resolution check asserts only that a
linked target EXISTS on disk, so nothing here is ever parsed.
