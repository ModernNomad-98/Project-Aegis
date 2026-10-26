---
name: flaky-test-detective
description: 'SIDE-004 regression fixture derived from the live flaky-test-detective Workflow: an auto-invocable skill whose Workflow instructs a test-layer fix.'
---

# Flaky Test Detective - SIDE-004 regression fixture

## Purpose

SIDE-004 regression fixture. Auto-invocable copy of the live flaky-test-detective Workflow mutation instruction. It must yield exactly one source-write candidate, and nothing else.

## Workflow

1. Fix that one cause at the test layer when it is a test bug: real isolation, await the actual condition, control time/seed, remove order dependence.
