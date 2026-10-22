# Audit evidence registers

This directory holds the dated, row-level evidence registers that accompany the
authoritative skill coverage map in [docs/skills/coverage-map.json](../skills/coverage-map.json).

## Contents

- [Aegis-Audit-Register-2026-10-20.json](Aegis-Audit-Register-2026-10-20.json) -
  the dated audit register, `b222ad604b00fd4cb577d9ee90a9288287a06872b195a927e89915efaa836354`
  (5,125,392 B). It is the source register for the Step 0 re-triage (D111).
- [Aegis-Coverage-Register-2026-10-20.md](Aegis-Coverage-Register-2026-10-20.md) -
  the dated coverage register, `bd3b6e9633c407e57b466f75ec665b812b22e4208ce4b33fd8332678cfc46819`
  (399,618 B). It records the row-level audit evidence; it has no relative links.

## Provenance and scope limits

- Both files are byte-identical copies of the owner-held 2026-10-20 registers
  (sha256 verified at copy time); the copies were added by Step 0 PR-S0-2 and are
  read-only evidence, not build authorization.
- The registers are a row-level companion to the maintained coverage map; the
  machine map in `docs/skills/coverage-map.json` stays authoritative for status.
- Frontend-batch closure (Batch 3, D110) is recorded as **UNRUN** for host/runtime
  behavior: no host execution or acceptance evidence exists, and UNRUN is never a pass.
- No claim of completeness: the register scope is the 300-row roadmap basis it was
  produced against, and later batches/decisions are recorded elsewhere (D-records).
