---
name: allowed-keys-agent
description: SYNTHETIC TEST FIXTURE, not a shipped agent. Uses every optional key on the agent allow-list; each one only narrows, bounds or labels the agent.
tools: Read, Grep, Glob
disallowedTools: Bash
model: sonnet
maxTurns: 10
effort: medium
color: blue
---

Fixture body for `scripts/tests/test_validator.py`.
