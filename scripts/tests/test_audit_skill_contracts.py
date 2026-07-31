#!/usr/bin/env python3
"""Self-tests for the corpus contract audit (engine + rule catalog, v2).

Run:  python scripts/tests/test_audit_skill_contracts.py   # exit 0 = all held

WHY THIS EXISTS
    The corpus contract audit is the evidence layer the AEGIS-001..059
    remediation program stands on. In the v2 hybrid architecture the POLICY
    lives in scripts/audit-rules.yaml and the ENGINE
    (scripts/audit-skill-contracts.py) is generic mechanism — so this suite
    proves BOTH: every catalog rule is complete (all required fields, real
    fixtures) and fires on its positive fixture; the clean fixture stays
    silent; the catalog loader fails closed on a broken policy; and the
    scanner is pinned to the real corpus so a pathing refactor cannot turn
    the audit into a green no-op — a wrong-path run must EXIT 2, never
    report a clean scan of nothing (the AEGIS-016/-017 lesson).

NO PYTEST, DELIBERATELY
    Same rule as test_validator.py (decision D55): the repo's dependency
    surface is one package (PyYAML); plain asserts suffice.

FIXTURES
    scripts/tests/fixtures/contract-audit/repo/ is a miniature repository:
    nine defective skills, each isolating one rule family, plus
    `clean-skill`, which every rule must ignore. The per-skill rule
    multisets asserted below are EXACT — a new rule that fires on an old
    fixture is a deliberate decision to record here, not drift to absorb.
"""
from __future__ import annotations

import copy
import importlib.util
import re
import sys
from pathlib import Path

TESTS_DIR = Path(__file__).resolve().parent
FIXTURE_REPO = TESTS_DIR / "fixtures" / "contract-audit" / "repo"
REAL_REPO = TESTS_DIR.parent.parent
AUDIT_PATH = TESTS_DIR.parent / "audit-skill-contracts.py"


def _load_by_path(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise SystemExit(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


audit_mod = _load_by_path(AUDIT_PATH, "aegis_contract_audit")

PASSES: list[str] = []


def ok(label: str) -> None:
    PASSES.append(label)
    print(f"  PASS  {label}")


def rule_by_id(catalog: dict, rid: str) -> dict:
    return next(r for r in catalog["rules"] if r["id"] == rid)


def run_fixture_audit(catalog: dict):
    a = audit_mod.Audit(FIXTURE_REPO, catalog)
    a.run()
    return a


def rules_by_skill(a) -> dict[str, list[str]]:
    out: dict[str, list[str]] = {}
    for f in a.findings:
        out.setdefault(f.owning_skill, []).append(f.rule)
    return {k: sorted(v) for k, v in out.items()}


# --- catalog completeness (the policy is itself under test) -----------------


def test_catalog_loads_and_is_complete(catalog: dict) -> None:
    assert catalog["catalog_version"], "catalog_version must be set"
    for rule in catalog["rules"]:
        for field in audit_mod.REQUIRED_RULE_FIELDS:
            assert field in rule, f"{rule.get('id')} missing {field}"
        assert rule["authority"].strip(), f"{rule['id']} has empty authority"
        assert rule["false_positive_limits"].strip(), (
            f"{rule['id']} has empty false_positive_limits"
        )
    ok(f"catalog v{catalog['catalog_version']}: all {len(catalog['rules'])} rules "
       "carry every required field (authority, fixtures, limits, owner, ...)")


def test_catalog_fails_closed() -> None:
    # A broken POLICY must stop the engine (CatalogError), not degrade into a
    # partial scan. Each tampered copy is written to a temp file and loaded
    # through the real loader.
    import tempfile

    import yaml as _yaml

    good = audit_mod.load_catalog()

    def expect_catalog_error(tampered: dict, label: str) -> None:
        with tempfile.NamedTemporaryFile(
            "w", suffix=".yaml", delete=False, encoding="utf-8"
        ) as tf:
            _yaml.safe_dump(tampered, tf)
            tmp = Path(tf.name)
        try:
            try:
                audit_mod.load_catalog(tmp)
            except audit_mod.CatalogError:
                ok(label)
                return
            raise AssertionError(f"loader accepted a broken catalog: {label}")
        finally:
            tmp.unlink(missing_ok=True)

    broken = copy.deepcopy(good)
    del broken["rules"][0]["authority"]
    expect_catalog_error(broken, "loader rejects a rule missing a required field")

    bad_detector = copy.deepcopy(good)
    bad_detector["rules"][0]["detector"] = {"type": "no-such-detector"}
    expect_catalog_error(bad_detector, "loader rejects an unknown detector type")

    bad_fixture = copy.deepcopy(good)
    bad_fixture["rules"][0]["positive_fixture"] = ".claude/skills/does-not-exist/SKILL.md"
    expect_catalog_error(bad_fixture, "loader rejects a fixture path that does not exist")


def test_every_rule_fires_on_fixtures(a, catalog: dict) -> None:
    fired = {f.rule for f in a.findings}
    all_ids = {r["id"] for r in catalog["rules"]}
    silent = sorted(all_ids - fired)
    assert not silent, (
        f"every catalog rule must fire on its positive fixture; silent: {silent}"
    )
    ok(f"all {len(all_ids)} catalog rules fire on the fixture repo "
       "(no rule exists only on paper)")


# --- the clean fixture must be silent (every rule's negative case) ----------


def test_clean_skill_is_silent(a) -> None:
    per = rules_by_skill(a)
    assert "clean-skill" not in per, (
        f"clean-skill must produce ZERO findings, got {per.get('clean-skill')}"
    )
    ok("clean-skill produces zero findings (negative fixture for every rule)")


# --- exact per-fixture rule multisets (every rule's positive case) ----------

EXPECTED = {
    "readonly-scratch-writer": ["EVAL-001", "SIDE-001", "SIDE-002", "SIDE-003"],
    "auto-deployer": ["SIDE-004"],
    "generic-approval": ["APPR-001", "APPR-002", "APPR-003", "EVAL-003"],
    "state-contradictor": ["STATE-001", "STATE-002", "STATE-003", "STATE-004", "STATE-005"],
    "committed-roadmap": ["VOCAB-002", "VOCAB-003"],
    "durable-vague": ["ARTF-001"],
    "bad-stage-router": ["ROUTE-001", "ROUTE-001", "ROUTE-001", "ROUTE-001", "ROUTE-003"],
    "thin-contract": ["EVAL-002", "EVAL-002", "EVAL-004", "EVAL-004", "PARITY-001", "PARITY-002"],
    "stale-linker": ["REF-001", "REF-002", "REF-003", "ROUTE-002"],
}


def test_exact_rule_multisets(a) -> None:
    per = rules_by_skill(a)
    for skill, expected in EXPECTED.items():
        got = per.get(skill, [])
        assert got == expected, f"[{skill}] expected {expected}, got {got}"
        ok(f"{skill} yields exactly {expected}")
    total = sum(len(v) for v in EXPECTED.values())
    assert len(a.findings) == total, (
        f"fixture repo must yield exactly {total} findings, got {len(a.findings)}"
    )
    ok(f"fixture repo yields exactly {total} findings in total")


# --- rule-specific semantics ------------------------------------------------


def test_route_rules(a) -> None:
    r1 = [f for f in a.findings if f.rule == "ROUTE-001"]
    flagged = {f.evidence.split("`")[1] for f in r1 if "`" in f.evidence}
    assert "ghost-skill-name" in flagged, f"ROUTE-001 must flag ghost-skill-name: {flagged}"
    ok("ROUTE-001 flags the ghost skill reference")
    assert "fixture-agent" not in flagged, (
        f"ROUTE-001 must NOT flag `fixture-agent` — reviewer agents are known names: {flagged}"
    )
    ok("ROUTE-001 does not flag a real reviewer agent")
    r3 = [f for f in a.findings if f.rule == "ROUTE-003"]
    assert r3 and "AEGIS-035" in r3[0].aegis_map, "ROUTE-003 must map to AEGIS-035"
    ok("ROUTE-003 (Stage-2 route gap) fires and maps to AEGIS-035")


def test_route002_census_mapping(a) -> None:
    r2 = [f for f in a.findings if f.rule == "ROUTE-002"]
    assert r2, "ROUTE-002 must fire on the fixture"
    for f in r2:
        assert f.aegis_map == [], (
            f"ROUTE-002 is census evidence and maps to NO AEGIS id, got {f.aegis_map}"
        )
        assert f.severity == "info", f.severity
    ok("ROUTE-002 carries no AEGIS mapping (census, not a mapped defect)")


def test_eval004_two_classes(a) -> None:
    hits = sorted(
        (f.severity, f.evidence) for f in a.findings if f.rule == "EVAL-004"
    )
    sevs = [s for s, _ in hits]
    assert sevs == ["P1", "P2"], f"EVAL-004 must yield one P1 + one P2, got {sevs}"
    assert "ghost-neighbor" in hits[0][1], hits
    assert "clean-skill (subagent)" in hits[1][1], hits
    ok("EVAL-004 separates a stale neighbor (P1) from an annotated real one (P2)")


def test_semantic_rules_are_candidates(a, catalog: dict) -> None:
    for f in a.findings:
        rule = rule_by_id(catalog, f.rule)
        assert f.mechanical == (rule["classification"] == "mechanical"), f.rule
        if not f.mechanical:
            assert f.semantic_review_owner, (
                f"{f.rule}: a semantic candidate must name its reviewer skill"
            )
    ok("semantic candidates carry their reviewer skill; mechanical flag mirrors the catalog")


# --- negation guard (calibrated on the live corpus) -------------------------


def test_negation_guard(catalog: dict) -> None:
    neg = audit_mod.negated
    overwrite = re.compile(rule_by_id(catalog, "STATE-002")["detector"]["violation_pattern"])
    for phrase in (
        "you supersede, you never overwrite the file here",
        "the overwrite of the file is never allowed at all",
        "you don't overwrite the file in this flow",
        "this skill doesn't rewrite the neighbor",
        "no field is ever overwritten in place",
    ):
        m = overwrite.search(phrase)
        assert m, phrase
        assert neg(phrase, m.start(), m.end()), f"must be treated as negated: {phrase!r}"
    ok("negation guard covers never/don't/doesn't/no-...-ever forms")

    hot = "when the scope changes, overwrite the file with the new content"
    m = overwrite.search(hot)
    assert m and not neg(hot, m.start(), m.end()), "a real instruction must NOT be negated"
    ok("negation guard does not swallow a genuine overwrite instruction")


# --- append-only declaration: contract vs domain vocabulary -----------------


def test_append_decl_scoping(catalog: dict) -> None:
    decl = re.compile(catalog["config"]["append_contract_declaration"])
    assert decl.search("The state log file is append-only."), "contract form must match"
    assert decl.search("## Decision log (append-only)"), "heading form must match"
    assert not decl.search("append-only formats needing rewrite jobs"), (
        "domain vocabulary (storage formats) must NOT count as a contract declaration"
    )
    ok("append-contract declaration binds contracts, not storage-domain vocabulary")


# --- Stage-2 segment helper (the v1 vacuous `or True` case, done right) -----


def test_route_segment_helper() -> None:
    good = (
        "- **Stage 2 - define.** x `prioritization-frame-picker` then "
        "`roadmap-under-uncertainty-planner` then `roadmap-to-commitments-translator`.\n"
        "- **Stage 3 - design.** other things.\n"
    )
    seg = audit_mod.Audit.route_segment(good, r"\*\*Stage 2\b", r"\*\*Stage 3\b")
    assert seg is not None, "segment must be found"
    assert "roadmap-under-uncertainty-planner" in seg, "planner must be inside the segment"
    assert "Stage 3" not in seg, "the segment must END before the Stage-3 marker"
    ok("route_segment captures exactly the Stage-2 slice (complete route = no finding)")
    assert audit_mod.Audit.route_segment("no stages here", r"\*\*Stage 2\b", r"\*\*Stage 3\b") is None
    ok("route_segment returns None when no Stage-2 route exists")


# --- provenance: what was scanned, exactly ----------------------------------


def test_provenance_content_hash(a) -> None:
    p = a.provenance()
    assert re.fullmatch(r"[0-9a-f]{64}", p["corpus_content_hash"]), p
    assert isinstance(p["working_tree_dirty"], bool)
    assert isinstance(p["dirty_paths_in_scanned_surfaces"], list)
    assert p["catalog_version"] == a.catalog["catalog_version"]
    ok("provenance carries corpus content hash + dirty-state evidence + versions")


# --- the scanner cannot green-pass a wrong path -----------------------------


def test_wrong_path_fails() -> None:
    rc = audit_mod.main(["--repo", str(TESTS_DIR / "fixtures" / "contract-audit"), "--quiet"])
    assert rc == 2, f"a path with no .claude/skills must exit 2, got {rc}"
    ok("wrong path exits 2 — never a clean scan of nothing (AEGIS-016/-017 lesson)")


def test_refuses_to_write_into_skills() -> None:
    out = FIXTURE_REPO / ".claude" / "skills" / "must-not-exist.json"
    rc = audit_mod.main(["--repo", str(FIXTURE_REPO), "--json", str(out), "--quiet"])
    assert rc == 2, f"writing output into .claude/skills/ must be refused, got {rc}"
    assert not out.exists(), "the refused output file must not have been created"
    ok("output inside .claude/skills/ is refused (the engine stays read-only)")


# --- real-surface pinning (decision D55 pattern) ----------------------------


def test_real_corpus_pinned(catalog: dict) -> None:
    skills_dir = REAL_REPO / ".claude" / "skills"
    assert skills_dir.is_dir(), "self-tests must run from the real repo checkout"
    on_disk = sorted(
        c.name for c in skills_dir.iterdir()
        if c.is_dir() and c.name not in audit_mod.IGNORED_DIRS
    )
    a = audit_mod.Audit(REAL_REPO, catalog)
    a.discover()
    scanned = sorted(s.name for s in a.skills)
    assert scanned == on_disk, (
        f"scanner must see exactly the on-disk corpus: {len(scanned)} vs {len(on_disk)}"
    )
    assert "project-orchestrator" in scanned, "the canonical route surface must be scanned"
    ok(f"scanner enumerates exactly the on-disk corpus ({len(scanned)} skills)")

    template = (
        skills_dir / "project-orchestrator" / "references" / "project-state-template.md"
    )
    text = template.read_text(encoding="utf-8")
    decl = re.compile(catalog["config"]["append_contract_declaration"])
    assert decl.search(text), (
        "the real project-state template must still register as an append-only "
        "CONTRACT surface — if this fails, the STATE family just went blind to "
        "its primary real target"
    )
    ok("real project-state template still binds as an append-only contract surface")


# --- review queue: routed, never executed -----------------------------------


def test_review_queue(a) -> None:
    q = a.review_queue()
    assert all(e["status"] == "queued" for e in q["finding_reviews"]), (
        "no queue entry may claim execution"
    )
    assert all(e["status"] == "queued" for e in q["rubric_queue"])
    reviewers = {e["reviewer"] for e in q["finding_reviews"]}
    assert reviewers <= {"skill-quality-reviewer", "agent-governance-audit",
                         "library-diff-reviewer", "code-reviewer",
                         "security-pr-reviewer"}, reviewers
    assert len(q["rubric_queue"]) == len(a.skills), (
        "every scanned skill gets a rubric-queue entry"
    )
    ok("review queue routes candidates to reviewer skills, all entries QUEUED")


# --- determinism ------------------------------------------------------------


def test_deterministic(a, catalog: dict) -> None:
    b = run_fixture_audit(catalog)
    assert a.to_json() == b.to_json(), "two runs on the same tree must be identical"
    ok("audit output is deterministic across runs")


def main() -> int:
    catalog = audit_mod.load_catalog()
    a = run_fixture_audit(catalog)
    test_catalog_loads_and_is_complete(catalog)
    test_catalog_fails_closed()
    test_every_rule_fires_on_fixtures(a, catalog)
    test_clean_skill_is_silent(a)
    test_exact_rule_multisets(a)
    test_route_rules(a)
    test_route002_census_mapping(a)
    test_eval004_two_classes(a)
    test_semantic_rules_are_candidates(a, catalog)
    test_negation_guard(catalog)
    test_append_decl_scoping(catalog)
    test_route_segment_helper()
    test_provenance_content_hash(a)
    test_wrong_path_fails()
    test_refuses_to_write_into_skills()
    test_real_corpus_pinned(catalog)
    test_review_queue(a)
    test_deterministic(a, catalog)
    print(f"\nOK: {len(PASSES)} contract-audit self-test assertion(s) passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
