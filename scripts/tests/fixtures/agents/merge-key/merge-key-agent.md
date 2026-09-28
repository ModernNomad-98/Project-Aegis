---
name: merge-key-agent
description: SYNTHETIC TEST FIXTURE, not a shipped agent. Its only `tools` arrives through a YAML merge key, which a YAML 1.2 reader without merge support would not see, so the agent would inherit every tool.
<<: {tools: 'Read, Grep, Glob'}
model: opus
---

Fixture body for `scripts/tests/test_validator.py`.
