# Offline setup routing advice

This Python package helps Project Aegis maintainers test how an optional setup
helper might suggest agents and skills for a task. It validates a small offer
and a proposed selection entirely offline. Use it to inspect the contract and
exercise synthetic cases; it is not the conversational setup skill that product
users invoke. The [issue #101 setup plan](../../docs/roadmaps/aegis-setup-routing-plan.md)
calls this delivered offline contract **package 3**. Host integration and
real-world helper evaluation belong to later package 4 work.

It has no host hook, provider, network client, credential, write operation or
dispatch function. A valid recommendation is still only advice. The future
host must independently establish eligibility, explicit invocation, mandatory
reviews, permissions and final dispatch authority.

## Try a synthetic decision

From the repository root, run the offline tests shown [below](#offline-checks).
This Python example uses the same request and response shapes as the
[contract tests](tests/test_routing_contract.py). It calls local functions only;
the offered names are illustrative, not an installed catalog or a real task
assignment.

```python
from tools.aegis_setup import decide, parse_request

request = parse_request({
    "version": "2", "request_id": "0123456789abcdef0123456789abcdef",
    "catalog_version": "cat-1", "policy_version": "pol-1",
    "synopsis": "Review an application programming interface (API) change", "stage": "review",
    "agents": [{"id": "reviewer", "description": "Reviews code", "read_only": True}],
    "skills": [{"id": "api", "description": "API review", "manual_only": False}],
    "mandatory_agents": ["reviewer"], "mandatory_skills": [],
    "selected_agents": [], "selected_skills": [], "invoked_manual_skills": [],
})
reply = {
    "version": "2", "request_id": "0123456789abcdef0123456789abcdef",
    "catalog_version": "cat-1", "policy_version": "pol-1",
    "status": "recommend", "agents": ["reviewer"], "skills": ["api"],
}
recommended = decide(request, reply)
abstained = decide(request, {**reply, "status": "abstain", "agents": [], "skills": []})
print(recommended.disposition, recommended.agents, recommended.skills)
print(abstained.disposition, abstained.agents, abstained.skills)
```

The `api` skill identifier in this example means an application programming
interface review. The output is `recommend ('reviewer',) ('api',)` followed by
`abstain () ()`. Neither result invokes an agent or skill. The abstention has
no selections, and a malformed or unavailable response also yields no
selections.

## Entry points and outcomes

JSON means JavaScript Object Notation, a text format for structured data.

| Entry point | What it accepts | What it produces or refuses |
| --- | --- | --- |
| `parse_request(raw)` | A bounded JSON object or Python mapping supplied by a synthetic caller or future host | A validated `Request`; raises `ContractError` for malformed or unsafe input before an adapter is used. |
| `decide(request, raw)` | A validated request and an untrusted JSON response or mapping | A `Decision`: `recommend`, `abstain`, `timeout`, `invalid` or `unavailable`. Failure dispositions contain no selections. |
| `check_compatibility(facts, request)` | Supplied synthetic installed-catalog facts and a validated request | `compatible`, `unsupported` or `unknown`; it does not probe a real assistant. |
| `FakeAdapter` | A scripted response or typed failure | One local decision for tests, without retry or local-to-online fallback. |

## Contract details

`parse_request(raw)` accepts a JSON object (or mapping) with contract `version`
`"2"`, `request_id`, `catalog_version`, `policy_version`, a one-line `synopsis` (1–512
characters), `stage` (`discovery`, `design`, `implementation`, `review` or
`release`), and `agents` and `skills` arrays of at most 16 offered entries each.
Agent entries have exactly `id`, `description`, `read_only`; skill entries have
exactly `id`, `description`, `manual_only`. ID means identifier; ASCII is a
seven-bit character encoding. IDs use lowercase ASCII
letters, digits and hyphens, starting with a letter (maximum 64 characters).
Descriptions are 1–120 characters. Versions are 1–64 ASCII letters, digits,
periods, underscores or hyphens, starting with a letter or digit.

A future host also supplies `mandatory_agents`, `mandatory_skills`,
`selected_agents`, `selected_skills` and `invoked_manual_skills` as unique ID
lists (up to 16 each). Every ID must be offered. A manual-only skill requires
both an explicit selection and invocation. The total encoded request is at
most 4096 UTF-8 (Unicode text encoding) bytes. No other fields are accepted.
The `request_id` must be exactly 32 lowercase hexadecimal characters. A host
generates a fresh unpredictable 128-bit value for every callback; a response
must echo it exactly. Version 1 responses and requests are rejected, including
by offline adapters that have not migrated. The ID only pairs a response with
its request; it grants no permission or dispatch authority.
The synopsis rejects line breaks, common URL (web address) or file-path shapes
and key/value secret markers; this is a
minimization check, not a guarantee that human text contains no sensitive
information. A future host must curate the synopsis before constructing it.

`decide(request, raw)` accepts a JSON response of at most 1024 UTF-8 bytes
with exactly `version`, `request_id`, `catalog_version`, `policy_version`, `status`, `agents`,
`skills`, and optional `score`. Versions and request ID must match exactly. `status` is
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

## Offline checks

Run from the repository root with Python available. The first command checks
the synthetic contract cases; the second validates the Aegis skills library.
Neither calls a provider.

```text
python -B -m unittest tools.aegis_setup.tests.test_routing_contract -v
python -B scripts/validate-skills.py
```
