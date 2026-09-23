# Offline advisory routing contract

This standard-library package is a synthetic seam for issue #101 package 3.
It has no host hook, provider, network client, credential, write operation or
dispatch function. A valid recommendation is still only advice. The future
host must independently establish eligibility, explicit invocation, mandatory
reviews, permissions and final dispatch authority.

`parse_request(raw)` accepts a JSON object (or mapping) with contract `version`
`"1"`, `catalog_version`, `policy_version`, a one-line `synopsis` (1–512
characters), `stage` (`discovery`, `design`, `implementation`, `review` or
`release`), and `agents` and `skills` arrays of at most 16 offered entries each.
Agent entries have exactly `id`, `description`, `read_only`; skill entries have
exactly `id`, `description`, `manual_only`. IDs are lowercase ASCII letters,
digits and hyphens, starting with a letter (maximum 64 characters).
Descriptions are 1–120 characters. Versions are 1–64 ASCII letters, digits,
periods, underscores or hyphens, starting with a letter or digit.

The host also supplies `mandatory_agents`, `mandatory_skills`,
`selected_agents`, `selected_skills` and `invoked_manual_skills` as unique ID
lists (up to 16 each). Every ID must be offered. A manual-only skill requires
both an explicit selection and invocation. The total encoded request is at
most 4096 UTF-8 bytes. No other fields are accepted. The synopsis rejects
line breaks, common URL/path shapes and key/value secret markers; this is a
minimization check, not a guarantee that human text contains no sensitive
information. A future host must curate the synopsis before constructing it.

`decide(request, raw)` accepts a JSON response of at most 1024 UTF-8 bytes
with exactly `version`, `catalog_version`, `policy_version`, `status`, `agents`,
`skills`, and optional `score`. Versions must match exactly. `status` is
`recommend` or `abstain`; selections are unique subsets of offered IDs. A
recommendation includes every mandatory and explicit ID. Manual-only skills
require invocation. `score`, when supplied, is a number between 0 and 1;
it is uncalibrated and grants no authority. An abstention has empty selections
and no score. The validated `Decision` has one of `recommend`, `abstain`,
`timeout`, `invalid` or `unavailable`; every failure carries empty selections.
Unexpected fields, including destination or permission flags, fail closed.

`check_compatibility(facts, request)` only compares supplied synthetic
installed-catalog facts with request versions and offered IDs. Missing or
malformed facts are `unknown`; version mismatch or absent offered IDs are
`unsupported`; consistent facts are `compatible`. None of these states proves
real assistant support. `FakeAdapter` returns a scripted response or a typed
failure without retry or local-to-online fallback.

Offline check from the repository root:

```text
python -m unittest tools.aegis_setup.tests.test_routing_contract -v
python scripts/validate-skills.py
```
