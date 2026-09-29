---
name: mcp-agent
description: SYNTHETIC TEST FIXTURE, not a shipped agent. Declares an inline MCP server, which would start a process when the agent is used.
tools: Read, Grep, Glob
model: opus
mcpServers:
  fixture-server:
    type: stdio
    command: echo
    args: [fixture]
---

Fixture body for `scripts/tests/test_validator.py`.
