---
name: approved-doc-writer
description: 'Records a decision note after content-specific approval. Use when a decision needs recording.'
---

# Approved Doc Writer

## Purpose

An auto-invocable skill whose only write follows the standard-§5 approved-write
protocol — the SIDE-004 exception-scoping negative fixture: suppression must
require the protocol markers NEXT TO the write instruction, and this skill has
them there. It must yield zero findings.

## Workflow

1. Draft the decision note in the conversation.
2. Show the exact target path and the exact content diff, and only after
   explicit, content-specific, single-use approval in the current session,
   append the note to the decisions file.
