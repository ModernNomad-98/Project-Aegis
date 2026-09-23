# Issue #101 package 3 — offline advisory contract evidence

Implementation branch starts at the exact AEGIS-APR-008 grant merge
`1af342712d27d5e6ea482b3f451106b4dccaf125`. Scope is the seven paths in
that grant. The contract is provider neutral, advisory only and offline.
No host hook, provider call, installation or model inference was performed.

## Contract and authority

The host supplies a minimized request with catalog and policy versions,
offered eligible IDs, mandatory IDs and explicit selections. The parser
enforces closed fields, byte/item bounds, exact IDs and versions, and a
manual-only invocation precondition. The synopsis is free text, and its basic
shape checks cannot prove it contains no secrets or copied source; a future
host must curate it. The response validator returns one of
five typed dispositions. It rejects unknown IDs, omitted mandatory or
explicit IDs, unauthorized manual-only skills, stale versions, malformed
output, destination fields and attempts to modify permission flags. Failures
have no recommended IDs. Read-only agent status stays in the host-supplied
offer; the response has no permission or dispatch field. Scores remain
uncalibrated metadata. The future host must independently recheck policy.

The compatibility checker only compares supplied synthetic facts. It cannot
claim support for a real host/version. The scripted fake adapter cannot
contact a service or switch from local to online. Actual fallback and result
consumption require a separately authorized package-4 host proof.

## Checks

- `python -m unittest tools.aegis_setup.tests.test_routing_contract -v`:
  9 tests passed on Windows PowerShell with synthetic in-memory inputs.
- `python scripts/validate-skills.py`: 184 skills valid, 0 warnings.
- `git diff --check`: passed.
- Independent authority review and exact-head Actions: pending.

The tests use synthetic in-memory inputs. No accuracy, token saving or real
host compatibility is claimed.
