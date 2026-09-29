---
name: merge-tag-agent
description: SYNTHETIC TEST FIXTURE, not a shipped agent. The key `foo` carries the merge tag, so PyYAML merges its mapping in even though no `<<` appears.
!!merge foo: {tools: 'Read, Grep, Glob'}
model: opus
---

Fixture body for `scripts/tests/test_validator.py`.
