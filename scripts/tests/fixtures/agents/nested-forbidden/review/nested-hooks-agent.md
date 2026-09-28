---
name: nested-hooks-agent
description: SYNTHETIC TEST FIXTURE, not a shipped agent. Sits one directory below the agents root, where Claude Code still finds it, and declares hooks.
tools: Read, Grep, Glob
model: opus
hooks:
  SubagentStart:
    - hooks:
        - type: command
          command: echo fixture
---

Fixture body for `scripts/tests/test_validator.py`.
