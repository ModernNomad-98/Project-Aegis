---
name: playwright-e2e-engineer
description: 'SIDE-004 regression fixture derived from the live playwright-e2e-engineer Workflow: an auto-invocable skill whose Workflow instructs a deployment gate and browser-test spec writes.'
---

# Playwright E2E Engineer - SIDE-004 regression fixture

## Purpose

SIDE-004 regression fixture. Auto-invocable copy of the live playwright-e2e-engineer Workflow mutation instructions. It must yield exactly one deploy-provision candidate and one source-write candidate, and nothing else.

## Workflow

1. The smoke tier gives fast deployment evidence but misses lower-priority paths; nightly adds coverage at the cost of runner minutes, fixture upkeep and later feedback.
2. Write specs with resilient locators: getByRole/getByLabel/getByText (user-facing) first; data-testid only where semantics do not exist.
