---
name: hooks-agent
description: SYNTHETIC TEST FIXTURE, not a shipped agent. Declares lifecycle hooks, which would run a shell command when the agent is used.
tools: Read, Grep, Glob
model: opus
hooks:
  PreToolUse:
    - matcher: Read
      hooks:
        - type: command
          command: echo fixture
---

Fixture body for `scripts/tests/test_validator.py`.
