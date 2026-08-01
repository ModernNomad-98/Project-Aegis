---
name: readonly-scratch-writer
description: 'Read-only review of build configs; changes nothing in the repository.'
allowed-tools:
  - Read
  - Write
---

# Readonly Scratch Writer

## Purpose

Read-only review of build configuration.

## Workflow

1. Inspect the config.
2. Write the findings to docs/review.md for the record.
3. Save the raw output to a scratchpad file for later comparison.

## Output Format

A review report listing each configuration issue found and its impact.
