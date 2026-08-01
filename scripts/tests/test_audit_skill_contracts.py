#!/usr/bin/env python3
"""Self-tests for scripts/audit-skill-contracts.py (AEGIS program, PR 1).

Run:  python scripts/tests/test_audit_skill_contracts.py   # exit 0 = all held
      (set PYTHONIOENCODING=utf-8 on Windows so evidence arrows print)

WHY THIS EXISTS
    The corpus contract audit is the evidence layer the AEGIS-001..059
    remediation program stands on. A finding it reports steers a remediation
    batch; a finding it MISSES ships a defect as "audited clean". So EACH rule
    is proved able to fire on ITS OWN designated positive fixture and proved
    able to stay silent on ITS OWN designated negative fixture (not merely
    "fired somewhere"), the COMPLETE rule inventory — including rules that fire
    zero times — is asserted present, provenance is proved to carry real
    dirty-state/hash evidence (not just a shape), and the scanner is pinned to
    the real corpus so a pathing refactor cannot turn the audit into a green
    no-op — a wrong-path run must EXIT 2, never a clean scan of nothing (the
    AEGIS-016/-017 lesson: evidence hygiene before scoring).

NO PYTEST, DELIBERATELY
    Same rule as test_validator.py (decision D55): the repo's dependency
    surface is one package (PyYAML); plain asserts suffice.

FIXTURES
    scripts/tests/fixtures/contract-audit/repo/ is a miniature repository:
    nine defective skills, each isolating one rule family, plus `clean-skill`,
    which every rule must ignore. The per-skill rule multisets asserted below
    are EXACT — a new rule that fires on an old fixture is a deliberate decision
    to record here, not drift to absorb.
"""
from __future__ import annotations

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


def run_fixture_audit():
    a = audit_mod.Audit(FIXTURE_REPO)
    a.run()
    return a


def rules_by_skill(a) -> dict[str, list[str]]:
    out: dict[str, list[str]] = {}
    for f in a.findings:
        out.setdefault(f.owning_skill, []).append(f.rule)
    return {k: sorted(v) for k, v in out.items()}


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


# --- every rule fires on ITS OWN positive fixture, silent on ITS OWN negative
# (the §6.H upgrade over v1's weaker "every rule fired somewhere") -----------


def test_every_rule_has_own_positive_and_negative(a) -> None:
    per = rules_by_skill(a)
    for r in audit_mod.RULES:
        rid = r["id"]
        pos = r["positive_fixture"]
        neg = r["negative_fixture"]
        assert rid in per.get(pos, []), (
            f"{rid} must FIRE on its own positive fixture {pos!r}; got {per.get(pos)}"
        )
        assert rid not in per.get(neg, []), (
            f"{rid} must be SILENT on its own negative fixture {neg!r}"
        )
    ok(f"all {len(audit_mod.RULES)} rules fire on their own positive fixture and "
       "stay silent on their own negative fixture")


# --- rule-specific semantics ------------------------------------------------


def test_route_rules(a) -> None:
    r1 = [f for f in a.findings if f.rule == "ROUTE-001"]
    # the flagged token is the one the evidence text NAMES, before the quoted
    # line (which may legitimately contain other tokens)
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


def test_route002_is_unmapped_census(a) -> None:
    r2 = [f for f in a.findings if f.rule == "ROUTE-002"]
    assert r2, "ROUTE-002 must fire on the stale-linker fixture"
    for f in r2:
        assert f.aegis_map == [], (
            f"ROUTE-002 is census evidence and maps to NO AEGIS id (fix v1#3); "
            f"got {f.aegis_map}"
        )
        assert f.severity == "info", f.severity
    ok("ROUTE-002 carries no AEGIS mapping (census, not the unrelated AEGIS-044)")


def test_side004_is_scoped_candidate(a) -> None:
    s4 = [f for f in a.findings if f.rule == "SIDE-004"]
    assert s4, "SIDE-004 must fire on the auto-deployer fixture"
    for f in s4:
        assert f.mechanical is False, "SIDE-004 is a SEMANTIC-REVIEW CANDIDATE, not mechanical"
        assert f.owning_skill == "auto-deployer"
    # SIDE-004 scans ALL non-manual skills (not only read-only-declared ones) —
    # the v1#2 coverage gap is closed.
    ok("SIDE-004 fires on an auto-invocable hard side effect as a semantic candidate")


def test_eval004_two_classes(a) -> None:
    hits = sorted(
        (f.severity, f.evidence) for f in a.findings if f.rule == "EVAL-004"
    )
    sevs = [s for s, _ in hits]
    assert sevs == ["P1", "P2"], f"EVAL-004 must yield one P1 + one P2, got {sevs}"
    assert "ghost-neighbor" in hits[0][1], hits
    assert "clean-skill (subagent)" in hits[1][1], hits
    ok("EVAL-004 separates a stale neighbor (P1) from an annotated real one (P2)")


def test_state_rules_map_to_aegis(a) -> None:
    for f in a.findings:
        if f.rule == "STATE-001":
            assert "AEGIS-002" in f.aegis_map, f.aegis_map
    ok("STATE-001 maps to AEGIS-002 (append-only vs mutable placeholder)")


# --- negation guard (calibrated on the live corpus: adr-sequencer et al.) ---


def test_negation_guard() -> None:
    neg = audit_mod.negated
    for phrase in (
        "you supersede, you never overwrite the file here",
        "the overwrite of the file is never allowed at all",
        "you don't overwrite the file in this flow",
        "this skill doesn't rewrite the neighbor",
        "no field is ever overwritten in place",
    ):
        m = audit_mod.OVERWRITE_VERB.search(phrase)
        assert m, phrase
        assert neg(phrase, m.start(), m.end()), f"must be treated as negated: {phrase!r}"
    ok("negation guard covers never/don't/doesn't/no-...-ever forms")

    hot = "when the scope changes, overwrite the file with the new content"
    m = audit_mod.OVERWRITE_VERB.search(hot)
    assert m and not neg(hot, m.start(), m.end()), "a real instruction must NOT be negated"
    ok("negation guard does not swallow a genuine overwrite instruction")


# --- append-only declaration: contract vs domain vocabulary -----------------


def test_append_decl_scoping() -> None:
    decl = audit_mod.APPEND_ONLY_DECL
    assert decl.search("The state log file is append-only."), "contract form must match"
    assert decl.search("## Decision log (append-only)"), "heading form must match"
    assert not decl.search("append-only formats needing rewrite jobs"), (
        "domain vocabulary (storage formats) must NOT count as a contract declaration"
    )
    ok("APPEND_ONLY_DECL binds contracts, not storage-domain vocabulary")


# --- Stage-2 segment helper (the v1 vacuous `or True` case, done right) ------


def test_stage2_segment() -> None:
    good = (
        "- **Stage 2 — define.** x `prioritization-frame-picker` then "
        "`roadmap-under-uncertainty-planner` then `roadmap-to-commitments-translator`.\n"
        "- **Stage 3 — design.** other things.\n"
    )
    seg = audit_mod.Audit.stage2_segment(good)
    assert seg is not None, "a Stage-2 route must produce a segment"
    assert "roadmap-under-uncertainty-planner" in seg, "planner must be inside the segment"
    # the REAL assertion the v1 `or True` neutered: Stage-3 content is EXCLUDED.
    assert "Stage 3" not in seg, "the segment MUST end before the Stage-3 marker"
    ok("stage2_segment captures the Stage-2 slice and EXCLUDES Stage-3 content")
    # malformed ordering / Stage-3 leakage: with no Stage-3 marker the segment
    # runs to EOF (and a Stage-3-only body yields no Stage-2 segment at all).
    leaky = "- **Stage 2 — define.** `roadmap-under-uncertainty-planner`.\nno terminator here.\n"
    seg2 = audit_mod.Audit.stage2_segment(leaky)
    assert seg2 is not None and "no terminator here" in seg2, (
        "absent Stage-3 marker → the Stage-2 segment must run to EOF"
    )
    ok("stage2_segment runs to EOF when no Stage-3 marker terminates the route")
    assert audit_mod.Audit.stage2_segment("no stages here") is None
    ok("stage2_segment returns None when no Stage-2 route exists")


# --- complete rule inventory: zero-hit rules are present (fix v1#5/#11) ------


def test_rule_inventory_complete(a) -> None:
    inv = a.to_json()["rule_inventory"]
    ids = [r["id"] for r in inv]
    assert ids == [r["id"] for r in audit_mod.RULES], "inventory lists every rule, in order"
    assert len(ids) == len(set(ids)), "no duplicate rule ids"
    for r in inv:
        assert isinstance(r.get("hit_count"), int), r
        assert r["classification"] in ("mechanical", "semantic-candidate"), r
        assert r["severity"] in audit_mod.SEVERITIES, r
        for key in ("purpose", "authority", "positive_fixture", "negative_fixture", "limits"):
            assert str(r.get(key, "")).strip(), f"{r['id']} missing {key}"
        assert isinstance(r["aegis_map"], list), r  # [] is valid (census)
    ok(f"JSON rule_inventory lists all {len(ids)} implemented rules with metadata + hit_count")


def test_real_inventory_includes_zero_hit_rules() -> None:
    a = audit_mod.Audit(REAL_REPO)
    a.run()
    inv = {r["id"]: r for r in a.to_json()["rule_inventory"]}
    assert set(inv) == {r["id"] for r in audit_mod.RULES}, "inventory covers every rule"
    zero = [rid for rid, r in inv.items() if r["hit_count"] == 0]
    assert zero, "the live corpus has zero-hit rules; they MUST still be inventoried (fix v1#5)"
    assert inv["SIDE-004"]["hit_count"] == 0, (
        "SIDE-004 is a scanned zero on the live corpus — present in the inventory, count 0"
    )
    ok(f"live-corpus inventory keeps {len(zero)} zero-hit rule(s) visible (a zero is a scanned zero)")


# --- provenance: real dirty-state/hash evidence, captured ONCE (fix v1#6/v2#5/#12)


def test_provenance_snapshot(a) -> None:
    p = a.provenance()
    for k in ("tool", "version", "engine_sha256", "repo_sha", "branch",
              "working_tree_dirty", "dirty_paths_in_scanned_surfaces",
              "audited_file_count", "audited_byte_count", "corpus_content_hash",
              "corpus_hash_byte_form"):
        assert k in p, f"provenance missing {k}"
    assert re.fullmatch(r"[0-9a-f]{64}", p["corpus_content_hash"]), p["corpus_content_hash"]
    assert re.fullmatch(r"[0-9a-f]{64}", p["engine_sha256"]), p["engine_sha256"]
    assert isinstance(p["working_tree_dirty"], bool)
    assert isinstance(p["dirty_paths_in_scanned_surfaces"], list)
    assert isinstance(p["audited_file_count"], int) and p["audited_file_count"] > 0
    assert isinstance(p["audited_byte_count"], int) and p["audited_byte_count"] > 0
    # captured ONCE: a second call returns the identical snapshot (no recompute)
    assert a.provenance() == p, "provenance must be captured once and reused"
    ok("provenance carries counts + dirty-state + corpus hash + byte-form + engine hash, captured once")


def test_provenance_content_sensitivity_and_inclusion() -> None:
    fixture = run_fixture_audit()
    real = audit_mod.Audit(REAL_REPO)
    real.run()
    # mutation/inclusion sensitivity: different corpora MUST hash differently
    assert (fixture.provenance()["corpus_content_hash"]
            != real.provenance()["corpus_content_hash"]), "distinct corpora must hash differently"
    audited = [f.as_posix() for f in real.audited_files()]
    assert audited, "the real corpus must have audited files"
    # inclusion boundary: agents and guided paths are ENUMERATED, never hashed
    assert all("/.claude/skills/" in a for a in audited), "audited set is the skills corpus only"
    assert not any("/.claude/agents/" in a for a in audited), "agents must not be in the audited hash"
    assert not any("/docs/paths/" in a for a in audited), "guided paths must not be in the audited hash"
    ok("corpus hash is content-sensitive and excludes agents/guided-paths (inclusion boundary)")


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
    ok("output inside .claude/skills/ is refused (the tool stays read-only)")


def test_write_refusal_resolves_symlink_escape() -> None:
    # Containment is checked on the RESOLVED path, so a traversal that lands
    # inside .claude/skills/ is refused even via ../ (fix §6.L).
    sneaky = FIXTURE_REPO / ".claude" / "agents" / ".." / "skills" / "escape.json"
    rc = audit_mod.main(["--repo", str(FIXTURE_REPO), "--json", str(sneaky), "--quiet"])
    assert rc == 2, f"a traversal into .claude/skills/ must be refused, got {rc}"
    ok("output-path containment refuses a ../ traversal into .claude/skills/")


# --- real-surface pinning (decision D55 pattern) ----------------------------


def test_real_corpus_pinned() -> None:
    skills_dir = REAL_REPO / ".claude" / "skills"
    assert skills_dir.is_dir(), "self-tests must run from the real repo checkout"
    on_disk = sorted(
        c.name for c in skills_dir.iterdir()
        if c.is_dir() and c.name not in audit_mod.IGNORED_DIRS
    )
    a = audit_mod.Audit(REAL_REPO)
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
    assert audit_mod.APPEND_ONLY_DECL.search(text), (
        "the real project-state template must still register as an append-only "
        "CONTRACT surface — if this fails, the STATE family just went blind to "
        "its primary real target"
    )
    ok("real project-state template still binds as an append-only contract surface")


# --- determinism ------------------------------------------------------------


def test_deterministic(a) -> None:
    b = run_fixture_audit()
    assert a.to_json() == b.to_json(), "two runs on the same tree must be identical"
    ok("audit output is deterministic across runs")


def main() -> int:
    a = run_fixture_audit()
    test_clean_skill_is_silent(a)
    test_exact_rule_multisets(a)
    test_every_rule_has_own_positive_and_negative(a)
    test_route_rules(a)
    test_route002_is_unmapped_census(a)
    test_side004_is_scoped_candidate(a)
    test_eval004_two_classes(a)
    test_state_rules_map_to_aegis(a)
    test_negation_guard()
    test_append_decl_scoping()
    test_stage2_segment()
    test_rule_inventory_complete(a)
    test_real_inventory_includes_zero_hit_rules()
    test_provenance_snapshot(a)
    test_provenance_content_sensitivity_and_inclusion()
    test_wrong_path_fails()
    test_refuses_to_write_into_skills()
    test_write_refusal_resolves_symlink_escape()
    test_real_corpus_pinned()
    test_deterministic(a)
    print(f"\nOK: {len(PASSES)} contract-audit self-test assertion(s) passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
