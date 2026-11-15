# Governance resolver fixture families (synthetic)

These fixtures are synthetic specifications for tools/aegis_preflight/tests/test_governance.py,
test_rule_projection.py and tools/distributed_payload/tests/test_dependency_closure.py. They contain no
credential, approval, private identity or live-host evidence. Nothing here is a real consumer repository.

Templates use uppercase placeholders (`__CONTRACT_SHA256__`, `__CONTRACT_VERSION__`,
`__TARGET_CONTRACT_SHA256__`) that the tests substitute from the committed contract before use, so a
fixture can never silently pin a stale contract identity: materialisation is explicit in each test.

| Family | Files | Acceptance cases |
| --- | --- | --- |
| source / copied-starter / external trees | built in-test from the committed documents with the role's required set (no real tree is copied from outside the repository) | 01-03, 05-11, 14-26 |
| adoption records | adoption/copied-starter-adoption.json, adoption/withdrawn-adoption.json | 02, 13, 14, 19 |
| external skill | external-skill/opsflow-skill-dependencies.json | 03, 04 |
| nested policy | nested-policy/AGENTS.local.md, nested-policy/CLAUDE.local.md | 07, 08 |
| packaging graph | packaging/dependencies-cycle.json, packaging/dependencies-duplicate.json, packaging/dependencies-scope.json, packaging/dependencies-missing-target.json | 02, 04, 24 |
| lineage budget | lineage/plan-lineage.json | 21 |
| rollback | rollback/rollback-target.json | 26 |
