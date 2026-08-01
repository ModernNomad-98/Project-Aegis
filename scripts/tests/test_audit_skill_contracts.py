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
    "fired somewhere"); the COMPLETE rule inventory — including rules that fire
    zero times — is asserted present; SIDE-004 is proved against the KNOWN
    live-corpus targets (a fixture pass must never coexist with a real-corpus
    false-clean — the Gate 2.5 lesson); audited-input containment is proved to
    fail closed on symlinks and repository-escaping paths BEFORE any read;
    the corpus hash is proved to follow its DECLARED repo-relative POSIX
    ordering on every platform; and the scanner is pinned to the real corpus
    so a pathing refactor cannot turn the audit into a green no-op — a
    wrong-path run must EXIT 2, never a clean scan of nothing (AEGIS-016/-017).

NO PYTEST, DELIBERATELY
    Same rule as test_validator.py (decision D55): the repo's dependency
    surface is one package (PyYAML); plain asserts suffice.

FIXTURES
    scripts/tests/fixtures/contract-audit/repo/ is a miniature repository:
    nine defective skills, each isolating one rule family, plus two that must
    stay silent — `clean-skill` (every rule's negative) and
    `approved-doc-writer` (the SIDE-004 approved-write exception, protocol
    markers NEXT TO the write). The per-skill rule multisets asserted below
    are EXACT — a new rule that fires on an old fixture is a deliberate
    decision to record here, not drift to absorb.
"""
from __future__ import annotations

import atexit
import contextlib
import hashlib
import importlib.util
import io
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from unittest import mock

TESTS_DIR = Path(__file__).resolve().parent
REAL_REPO = TESTS_DIR.parent.parent
AUDIT_PATH = TESTS_DIR.parent / "audit-skill-contracts.py"

# Gate 2.7 item 2: the TRACKED fixture source uses a NEUTRAL `dot-claude/`
# layout, so the Claude Code harness never discovers fixture skills (auto-
# deployer, clean-skill, …) as live invocable session skills. Tests run against
# a THROWAWAY copy OUTSIDE the repo in which `dot-claude` is materialized to
# `.claude`. Nothing tracked ever contains a nested literal `.claude/skills`.
_FIXTURE_SRC = TESTS_DIR / "fixtures" / "contract-audit" / "repo"  # contains dot-claude/


def _materialize_fixture_repo() -> Path:
    tmp = Path(tempfile.mkdtemp(prefix="aegis-fixture-"))
    dst = tmp / "repo"
    shutil.copytree(_FIXTURE_SRC, dst)
    neutral = dst / "dot-claude"
    assert neutral.is_dir(), f"neutral fixture source must exist: {neutral}"
    neutral.rename(dst / ".claude")
    atexit.register(lambda: shutil.rmtree(tmp, ignore_errors=True))
    return dst


FIXTURE_REPO = _materialize_fixture_repo()


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


_REAL_AUDIT = None


def real_audit():
    """One cached full real-corpus run shared by every real-surface test."""
    global _REAL_AUDIT
    if _REAL_AUDIT is None:
        _REAL_AUDIT = audit_mod.Audit(REAL_REPO)
        _REAL_AUDIT.run()
    return _REAL_AUDIT


def rules_by_skill(a) -> dict[str, list[str]]:
    out: dict[str, list[str]] = {}
    for f in a.findings:
        out.setdefault(f.owning_skill, []).append(f.rule)
    return {k: sorted(v) for k, v in out.items()}


# --- the silent fixtures (negative cases) -----------------------------------


def test_clean_skill_is_silent(a) -> None:
    per = rules_by_skill(a)
    assert "clean-skill" not in per, (
        f"clean-skill must produce ZERO findings, got {per.get('clean-skill')}"
    )
    ok("clean-skill produces zero findings (negative fixture for every rule)")


def test_approved_doc_writer_is_silent(a) -> None:
    per = rules_by_skill(a)
    assert "approved-doc-writer" not in per, (
        f"approved-doc-writer must be silent — its only write carries the §5 "
        f"protocol markers NEXT TO the instruction; got {per.get('approved-doc-writer')}"
    )
    ok("approved-doc-writer is silent (approved-write exception scoped to the write)")


# --- exact per-fixture rule multisets (every rule's positive case) ----------

EXPECTED = {
    "readonly-scratch-writer": ["EVAL-001", "SIDE-001", "SIDE-002", "SIDE-003", "SIDE-004"],
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


def test_side004_fixture_classes(a) -> None:
    s4 = [f for f in a.findings if f.rule == "SIDE-004"]
    owners = {f.owning_skill for f in s4}
    assert owners == {"auto-deployer", "readonly-scratch-writer"}, owners
    for f in s4:
        assert f.mechanical is False, "SIDE-004 is a SEMANTIC-REVIEW CANDIDATE, not mechanical"
    by_owner = {f.owning_skill: f.evidence for f in s4}
    assert "[deploy-provision]" in by_owner["auto-deployer"], by_owner
    assert "[doc-state-write]" in by_owner["readonly-scratch-writer"], by_owner
    ok("SIDE-004 fires per §5 class ([deploy-provision], [doc-state-write]) as candidates")


def test_side004_real_corpus_targets() -> None:
    """The Gate 2.5 blocker-1 regression: the KNOWN auto-invocable mutating
    skills must never again be a silent scanned-zero. Every named target is
    auto-invocable on disk and must carry at least one SIDE-004 candidate."""
    targets = [
        "docs-first-implementer", "tdd-engineer", "systematic-debugger",
        "flaky-test-detective", "reviewable-diff-discipline",
        "local-ci-mirror-preflight", "multi-tenant-security-tester",
        "n-plus-one-detector", "query-plan-reader", "adr-writer",
        "chat-backlog-reconciliation", "scoped-approval-register",
        "merge-is-deploy-governance",
    ]
    ra = real_audit()
    skills = {s.name: s for s in ra.skills}
    s4_owners = {f.owning_skill for f in ra.findings if f.rule == "SIDE-004"}
    for t in targets:
        assert t in skills, f"target skill {t} missing from the corpus"
        assert not skills[t].classify()["manual_only"], (
            f"{t} is expected auto-invocable (a manual-only flip is a posture "
            "change to re-account here deliberately)"
        )
        assert t in s4_owners, (
            f"{t} must yield at least one SIDE-004 semantic-review candidate — "
            "a silent clean here is the Gate 2.5 blocker-1 false-clean"
        )
    ok(f"all {len(targets)} known live mutation targets carry SIDE-004 candidates "
       "(no silent clean)")


def test_side004_approval_elsewhere_never_suppresses() -> None:
    """An approval phrase far from the instruction must suppress NOTHING —
    neither a hard class (vcs) nor a doc write outside the marker window."""
    tmp = Path(tempfile.mkdtemp(prefix="aegis-s4-"))
    try:
        skill = tmp / ".claude" / "skills" / "pushy"
        skill.mkdir(parents=True)
        (skill / "SKILL.md").write_text(
            "---\n"
            "name: pushy\n"
            "description: 'Pushes the release branch after checks.'\n"
            "---\n\n# Pushy\n\n## Workflow\n\n"
            "1. Approvals gathered: explicit, content-specific, single-use approval\n"
            "   was granted earlier for the exact target path and the exact content\n"
            "   diff of the changelog note.\n"
            "2. Step filler.\n3. Step filler.\n4. Step filler.\n5. Step filler.\n"
            "6. Step filler.\n7. Step filler.\n8. Step filler.\n9. Step filler.\n"
            "10. Step filler.\n"
            "11. Run git push origin main.\n"
            "12. Then write the summary report for the team.\n",
            encoding="utf-8",
        )
        a = audit_mod.Audit(tmp)
        a.run()
        s4 = [f for f in a.findings if f.rule == "SIDE-004" and f.owning_skill == "pushy"]
        classes = sorted(f.evidence.split("[")[1].split("]")[0] for f in s4)
        assert "vcs-mutation" in classes, (
            f"the distant approval paragraph must not suppress the git push: {classes}"
        )
        assert "doc-state-write" in classes, (
            f"a doc write OUTSIDE the marker window must still fire: {classes}"
        )
        ok("an approval phrase elsewhere suppresses nothing (vcs + out-of-window "
           "doc write both fire)")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


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


def test_mechanical_flag_matches_inventory(a) -> None:
    cls = {r["id"]: r["classification"] for r in audit_mod.RULES}
    for f in a.findings:
        expected = cls[f.rule] == "mechanical"
        assert f.mechanical == expected, (
            f"{f.rule}: emitted mechanical={f.mechanical} but inventory says "
            f"{cls[f.rule]!r} — classification must be consistent (Gate 2.5 blocker 4)"
        )
    reclassified = {"STATE-001", "VOCAB-002", "VOCAB-003", "EVAL-003", "SIDE-004"}
    for rid in reclassified:
        assert cls[rid] == "semantic-candidate", (
            f"{rid} admits use-vs-mention/contextual ambiguity in its own limits "
            "and must be a semantic-candidate"
        )
    ok("every finding's mechanical flag mirrors the inventory; ambiguous rules "
       "are semantic-candidates")


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


# --- Stage-2 segment: normal boundary AND malformed/leakage cases -----------


def test_stage2_segment() -> None:
    good = (
        "- **Stage 2 — define.** x `prioritization-frame-picker` then "
        "`roadmap-under-uncertainty-planner` then `roadmap-to-commitments-translator`.\n"
        "- **Stage 3 — design.** other things.\n"
    )
    seg = audit_mod.Audit.stage2_segment(good)
    assert seg is not None, "a Stage-2 route must produce a segment"
    assert "roadmap-under-uncertainty-planner" in seg, "planner must be inside the segment"
    assert "Stage 3" not in seg, "the segment MUST end before the Stage-3 marker"
    ok("stage2_segment captures the Stage-2 slice and EXCLUDES Stage-3 content")
    assert audit_mod.Audit.stage2_segment("no stages here") is None
    ok("stage2_segment returns None when no Stage-2 route exists")


def test_stage2_malformed_and_leakage() -> None:
    """Gate 2.5 blocker 5: genuine malformed-ordering / Stage-3-leakage cases.
    Each would FAIL under a broken segmentation (whole-body or slice-to-EOF
    implementations leak the Stage-3 text into the Stage-2 segment)."""
    # (a) malformed ordering: Stage 3 BEFORE Stage 2. The Stage-3 text names
    # the planner; a broken whole-body implementation would leak it into the
    # segment and false-clean the ROUTE-003 condition.
    disordered = (
        "- **Stage 3 — design.** handled by `roadmap-under-uncertainty-planner`.\n"
        "- **Stage 2 — define.** `roadmap-to-commitments-translator` only.\n"
    )
    seg = audit_mod.Audit.stage2_segment(disordered)
    assert seg is not None
    assert "roadmap-to-commitments-translator" in seg
    assert "roadmap-under-uncertainty-planner" not in seg, (
        "Stage-3 text appearing BEFORE Stage 2 must not leak into the segment"
    )
    ok("malformed ordering (Stage 3 before Stage 2) does not leak into the segment")

    # (b) duplicate/out-of-order markers: the segment is exactly first-Stage-2
    # to first-following-Stage-3; later repeats never leak in.
    dup = (
        "- **Stage 2 — define.** alpha `roadmap-to-commitments-translator`.\n"
        "- **Stage 3 — design.** leak-one `roadmap-under-uncertainty-planner`.\n"
        "- **Stage 2 — define (again).** beta.\n"
        "- **Stage 3 — design (again).** leak-two.\n"
    )
    seg = audit_mod.Audit.stage2_segment(dup)
    assert seg is not None and "alpha" in seg
    for leaked in ("leak-one", "leak-two", "beta", "roadmap-under-uncertainty-planner"):
        assert leaked not in seg, f"duplicate-marker body leaked {leaked!r} into the segment"
    ok("duplicate/out-of-order markers: only first Stage-2..Stage-3 slice is kept")

    # (c) the leakage consequence itself: Stage 2 omits the planner, Stage 3
    # CONTAINS it. A leaking implementation would see the planner and
    # false-clean the ROUTE-003 gap; the correct segment keeps the gap visible.
    leaky_route = (
        "- **Stage 2 — define.** `product-spec-writer` then "
        "`roadmap-to-commitments-translator`.\n"
        "- **Stage 3 — design.** later work by `roadmap-under-uncertainty-planner`.\n"
    )
    seg = audit_mod.Audit.stage2_segment(leaky_route)
    assert seg is not None
    assert "roadmap-to-commitments-translator" in seg
    assert "roadmap-under-uncertainty-planner" not in seg, (
        "a leaking segment would hide the Stage-2 route gap (ROUTE-003 false-clean)"
    )
    ok("Stage-3 leakage cannot false-clean the ROUTE-003 route-gap condition")


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
    ra = real_audit()
    inv = {r["id"]: r for r in ra.to_json()["rule_inventory"]}
    assert set(inv) == {r["id"] for r in audit_mod.RULES}, "inventory covers every rule"
    zero = [rid for rid, r in inv.items() if r["hit_count"] == 0]
    assert zero, "the live corpus has zero-hit rules; they MUST still be inventoried (fix v1#5)"
    assert inv["SIDE-004"]["hit_count"] >= 13, (
        "SIDE-004 must carry at least the 13 known live targets — a scanned zero "
        "here is the Gate 2.5 blocker-1 false-clean"
    )
    ok(f"live-corpus inventory keeps {len(zero)} zero-hit rule(s) visible and "
       f"SIDE-004 carries {inv['SIDE-004']['hit_count']} candidates")


# --- provenance: real dirty-state/hash evidence, captured ONCE ---------------


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
    assert a.provenance() == p, "provenance must be captured once and reused"
    ok("provenance carries counts + dirty-state + corpus hash + byte-form + engine hash, captured once")


def test_provenance_content_sensitivity_and_inclusion() -> None:
    fixture = run_fixture_audit()
    ra = real_audit()
    assert (fixture.provenance()["corpus_content_hash"]
            != ra.provenance()["corpus_content_hash"]), "distinct corpora must hash differently"
    audited = [f.as_posix() for f in ra.audited_files()]
    assert audited, "the real corpus must have audited files"
    assert all("/.claude/skills/" in x for x in audited), "audited set is the skills corpus only"
    assert not any("/.claude/agents/" in x for x in audited), "agents must not be in the audited hash"
    assert not any("/docs/paths/" in x for x in audited), "guided paths must not be in the audited hash"
    ok("corpus hash is content-sensitive and excludes agents/guided-paths (inclusion boundary)")


def test_auxiliary_inputs_provenance() -> None:
    """§8 provenance honesty: auxiliary inputs (catalog content + agent/path
    filenames) that affect output are recorded in a SEPARATELY-NAMED field, not
    folded into the corpus hash; the byte-form note says so explicitly."""
    ra = real_audit()
    p = ra.provenance()
    aux = p["auxiliary_inputs"]
    assert set(aux) == {"skills_catalog", "agent_names_enumerated",
                        "guided_path_names_enumerated"}, aux
    cat = aux["skills_catalog"]["sha256"]
    assert cat == "absent" or re.fullmatch(r"[0-9a-f]{64}", cat), cat
    assert isinstance(aux["agent_names_enumerated"]["names"], list)
    assert isinstance(aux["guided_path_names_enumerated"]["names"], list)
    # the corpus hash must NOT be silently described as covering auxiliary inputs
    bf = p["corpus_hash_byte_form"].lower()
    assert "auxiliary" in bf and "does not cover" in bf, bf
    # and the auxiliary inputs are NOT in the audited (hashed) file set
    audited = {f.as_posix() for f in ra.audited_files()}
    assert not any("skills-catalog.md" in x for x in audited)
    ok("auxiliary inputs (catalog/agents/paths) recorded separately; corpus hash "
       "honestly scoped to the skill corpus")


def test_corpus_hash_follows_declared_posix_order() -> None:
    """Gate 2.5 blocker 3: the hash's file order must be the DECLARED key —
    repo-relative POSIX path strings — not platform-native Path ordering.
    `B.md` sorts BEFORE `a.md` in POSIX byte order; Windows-native casefolded
    Path ordering would flip them and silently change the hash."""
    tmp = Path(tempfile.mkdtemp(prefix="aegis-order-"))
    try:
        refs = tmp / ".claude" / "skills" / "case-order" / "references"
        refs.mkdir(parents=True)
        (refs.parent / "SKILL.md").write_text(
            "---\nname: case-order\ndescription: 'Orders nothing.'\n---\n\n# X\n",
            encoding="utf-8")
        (refs / "B.md").write_text("upper\n", encoding="utf-8")
        (refs / "a.md").write_text("lower\n", encoding="utf-8")
        a = audit_mod.Audit(tmp)
        a.run()
        rels = [f.relative_to(tmp).as_posix() for f in a.audited_files()]
        assert rels == sorted(rels), (
            f"audited_files must be ordered by the POSIX path string: {rels}"
        )
        b_idx = next(i for i, r in enumerate(rels) if r.endswith("/B.md"))
        a_idx = next(i for i, r in enumerate(rels) if r.endswith("/a.md"))
        assert b_idx < a_idx, (
            f"POSIX byte order puts B.md before a.md; got {rels} — platform-native "
            "(casefolded) ordering leaked back in"
        )
        # the hash equals a manual recomputation following the DECLARED byte form
        h = hashlib.sha256()
        for rel in rels:
            h.update(rel.encode("utf-8")); h.update(b"\0")
            h.update((tmp / rel).read_bytes()); h.update(b"\0")
        assert h.hexdigest() == a.provenance()["corpus_content_hash"], (
            "implementation hash must equal the declared-byte-form recomputation"
        )
        ok("corpus hash follows its declared repo-relative POSIX ordering "
           "(B.md < a.md) and byte form on every platform")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


# --- audited-input containment (Gate 2.5 blocker 2) --------------------------


def _copy_fixture(dst_parent: Path) -> Path:
    dst = dst_parent / "repo-copy"
    shutil.copytree(FIXTURE_REPO, dst)
    return dst


def test_input_symlink_reference_fails_closed() -> None:
    tmp = Path(tempfile.mkdtemp(prefix="aegis-cont-"))
    try:
        marker = tmp / "external-secret.md"
        marker_text = "AEGIS-G26-EXTERNAL-MARKER C:/Users/fakeuser-g26/private-notes.md"
        marker.write_text(marker_text, encoding="utf-8")
        repo = _copy_fixture(tmp)
        link = repo / ".claude" / "skills" / "stale-linker" / "references" / "leak.md"
        link.parent.mkdir(parents=True, exist_ok=True)
        try:
            os.symlink(marker, link)
        except OSError as exc:
            if getattr(exc, "winerror", None) == 1314:  # privilege not held
                print(f"  SKIP  symlink privilege unavailable on this host ({exc}) — "
                      "input containment NOT proven here")
                return
            raise
        # direct API: the run must raise BEFORE reading
        raised = False
        try:
            audit_mod.Audit(repo).run()
        except audit_mod.InputContainmentError as exc:
            raised = True
            assert marker_text not in str(exc), "the error must not carry file content"
        assert raised, "a symlinked reference must raise InputContainmentError"
        # CLI: exit 2, no output written, no marker anywhere in stdout
        out = tmp / "never.json"
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            rc = audit_mod.main(["--repo", str(repo), "--json", str(out), "--quiet"])
        assert rc == 2, f"symlinked audited input must exit 2, got {rc}"
        assert not out.exists(), "no output may be written on a containment refusal"
        assert marker_text not in buf.getvalue(), (
            "external content must never appear in any output"
        )
        assert "AEGIS-G26-EXTERNAL-MARKER" not in buf.getvalue()
        ok("a symlinked reference fails closed (exit 2) BEFORE reading; external "
           "content appears nowhere")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def test_input_symlink_skill_dir_fails_closed() -> None:
    tmp = Path(tempfile.mkdtemp(prefix="aegis-cont2-"))
    try:
        external = tmp / "external-skill"
        external.mkdir()
        (external / "SKILL.md").write_text(
            "---\nname: outside\ndescription: 'x'\n---\n\n# Outside\n", encoding="utf-8")
        repo = _copy_fixture(tmp)
        link = repo / ".claude" / "skills" / "outside"
        try:
            os.symlink(external, link, target_is_directory=True)
        except OSError as exc:
            if getattr(exc, "winerror", None) == 1314:  # privilege not held
                print(f"  SKIP  symlink privilege unavailable on this host ({exc}) — "
                      "input containment NOT proven here")
                return
            raise
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            rc = audit_mod.main(["--repo", str(repo), "--quiet"])
        assert rc == 2, f"a symlinked skill directory must exit 2, got {rc}"
        ok("a symlinked skill directory fails closed (exit 2)")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def test_input_containment_accepts_regular_files() -> None:
    tmp = Path(tempfile.mkdtemp(prefix="aegis-cont3-"))
    try:
        repo = _copy_fixture(tmp)
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            rc = audit_mod.main(["--repo", str(repo), "--quiet"])
        assert rc == 0, (
            f"an all-regular-files in-repo corpus must still audit (exit 0), got {rc}"
        )
        ok("regular in-repository audited files remain accepted (exit 0)")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def test_escaping_markdown_link_is_flagged_not_passed() -> None:
    """A Markdown link resolving OUTSIDE the repository must be flagged even
    though its target exists on the machine — and must never be read."""
    tmp = Path(tempfile.mkdtemp(prefix="aegis-cont4-"))
    try:
        marker_text = "AEGIS-G26-LINK-MARKER do-not-disclose"
        (tmp / "external.md").write_text(marker_text, encoding="utf-8")
        repo = _copy_fixture(tmp)
        skill_md = repo / ".claude" / "skills" / "stale-linker" / "SKILL.md"
        skill_md.write_text(
            skill_md.read_text(encoding="utf-8")
            + "\nAlso see [the archive](../../../../external.md) for older notes.\n",
            encoding="utf-8",
        )
        a = audit_mod.Audit(repo)
        a.run()
        outside = [f for f in a.findings
                   if f.rule == "REF-001" and "OUTSIDE the repository" in f.evidence]
        assert outside, "an escaping link that EXISTS must still be flagged"
        assert any("external.md" in f.evidence for f in outside)
        for f in a.findings:
            assert marker_text not in f.evidence, (
                "the external target's content must never be read into a finding"
            )
        ok("an escaping Markdown link is flagged (existence is not a pass) and "
           "its content is never read")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


# --- auxiliary-input containment: catalog / agents / paths (Gate 2.7) -------


def _run_capture(repo: Path, *extra: str) -> tuple[int, str]:
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        rc = audit_mod.main(["--repo", str(repo), "--quiet", *extra])
    return rc, buf.getvalue()


def _skip_if_no_symlink(exc: OSError) -> bool:
    if getattr(exc, "winerror", None) == 1314:
        print(f"  SKIP  symlink privilege unavailable on this host ({exc})")
        return True
    return False


def test_catalog_symlink_fails_closed() -> None:
    tmp = Path(tempfile.mkdtemp(prefix="aegis-cat-"))
    try:
        marker = "AEGIS-G27-CATALOG-MARKER external-catalog-secret-heading"
        (tmp / "external.md").write_text(f"# {marker}\n| `x` |\n", encoding="utf-8")
        repo = _copy_fixture(tmp)
        (repo / "docs").mkdir(parents=True, exist_ok=True)
        cat = repo / "docs" / "skills-catalog.md"
        try:
            os.symlink(tmp / "external.md", cat)
        except OSError as exc:
            if _skip_if_no_symlink(exc):
                return
            raise
        outs = {n: tmp / n for n in ("o.json", "m.json", "o.md", "g.json")}
        rc, stdout = _run_capture(
            repo, "--json", str(outs["o.json"]), "--manifest", str(outs["m.json"]),
            "--markdown", str(outs["o.md"]), "--graph", str(outs["g.json"]))
        assert rc == 2, f"a symlinked docs/skills-catalog.md must exit 2, got {rc}"
        for p in outs.values():
            assert not p.exists(), f"no output may be written on containment refusal: {p}"
        assert marker not in stdout, "external catalog heading must not appear in output"
        ok("symlinked docs/skills-catalog.md fails closed (exit 2); no output, marker nowhere")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def test_agents_dir_symlink_leaks_no_filenames() -> None:
    tmp = Path(tempfile.mkdtemp(prefix="aegis-ag-"))
    try:
        ext = tmp / "external-agents"
        ext.mkdir()
        secret_name = "SECRET-AGENT-DIR-LISTING-G27.md"
        (ext / secret_name).write_text("x", encoding="utf-8")
        repo = _copy_fixture(tmp)
        agents = repo / ".claude" / "agents"
        shutil.rmtree(agents)
        try:
            os.symlink(ext, agents, target_is_directory=True)
        except OSError as exc:
            if _skip_if_no_symlink(exc):
                return
            raise
        rc, stdout = _run_capture(repo, "--manifest", str(tmp / "m.json"))
        assert rc == 2, f"a symlinked .claude/agents/ must exit 2, got {rc}"
        assert not (tmp / "m.json").exists()
        assert secret_name not in stdout, "external agent filename must not leak"
        ok("symlinked .claude/agents/ fails closed; external filename never enumerated")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def test_paths_dir_symlink_leaks_no_filenames() -> None:
    tmp = Path(tempfile.mkdtemp(prefix="aegis-gp-"))
    try:
        ext = tmp / "external-paths"
        ext.mkdir()
        secret_name = "SECRET-GUIDED-PATH-LISTING-G27.md"
        (ext / secret_name).write_text("x", encoding="utf-8")
        repo = _copy_fixture(tmp)
        (repo / "docs").mkdir(parents=True, exist_ok=True)
        try:
            os.symlink(ext, repo / "docs" / "paths", target_is_directory=True)
        except OSError as exc:
            if _skip_if_no_symlink(exc):
                return
            raise
        rc, stdout = _run_capture(repo, "--manifest", str(tmp / "m.json"))
        assert rc == 2, f"a symlinked docs/paths/ must exit 2, got {rc}"
        assert not (tmp / "m.json").exists()
        assert secret_name not in stdout, "external guided-path filename must not leak"
        ok("symlinked docs/paths/ fails closed; external filename never enumerated")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def test_skills_root_symlink_rejected() -> None:
    tmp = Path(tempfile.mkdtemp(prefix="aegis-sr-"))
    try:
        ext_skills = tmp / "external-skills"
        (ext_skills / "outside").mkdir(parents=True)
        (ext_skills / "outside" / "SKILL.md").write_text(
            "---\nname: outside\ndescription: 'x'\n---\n\n# Outside\n", encoding="utf-8")
        repo = tmp / "repo2"
        (repo / ".claude").mkdir(parents=True)
        try:
            os.symlink(ext_skills, repo / ".claude" / "skills", target_is_directory=True)
        except OSError as exc:
            if _skip_if_no_symlink(exc):
                return
            raise
        rc, stdout = _run_capture(repo)
        assert rc == 2, f"a symlinked .claude/skills/ root must exit 2, got {rc}"
        ok("symlinked .claude/skills/ root is rejected (exit 2)")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def _create_junction(link: Path, target: Path) -> tuple[str, str]:
    """Try to create a Windows directory JUNCTION at `link` -> `target`.

    Returns ("created", "") on success, or ("skip", reason) when the host cannot
    create one — and NEVER raises for host incapability (Gate 2.9 portability):
      * a non-Windows host has no junctions at all;
      * a Windows host may lack the `cmd` interpreter on PATH;
      * `cmd` may vanish between discovery and invocation (a PATH race);
      * `mklink /J` may return non-zero (privilege/filesystem).
    A genuine containment FAILURE is NOT this helper's concern — that is asserted
    by the caller only after ("created", "")."""
    if os.name != "nt":
        return "skip", "not a Windows host (junctions are Windows-only)"
    cmd_exe = shutil.which("cmd.exe") or shutil.which("cmd")
    if cmd_exe is None:
        return "skip", "no Windows command interpreter (cmd.exe) on PATH"
    try:
        r = subprocess.run(
            [cmd_exe, "/c", "mklink", "/J", str(link), str(target)],
            capture_output=True, text=True,
        )
    except FileNotFoundError as exc:
        # defensive: the interpreter disappeared after discovery (PATH race)
        return "skip", f"Windows command interpreter unavailable mid-call ({exc})"
    if r.returncode != 0 or not link.exists():
        return "skip", (
            f"mklink /J failed (rc={r.returncode}: "
            f"{r.stderr.strip() or r.stdout.strip()})"
        )
    return "created", ""


def test_junction_escape_rejected() -> None:
    """Windows junctions are reparse points os.walk does not treat as links;
    _check_input's is_junction/resolve backstop must still reject them. On a
    Windows host the junction is created and the containment assertion runs
    (PASS); on an unsupported host the case reports an honest SKIP and is NEVER
    counted as passed (Gate 2.9)."""
    tmp = Path(tempfile.mkdtemp(prefix="aegis-jn-"))
    try:
        ext = tmp / "external-ref-dir"
        ext.mkdir()
        (ext / "OUTSIDE-JUNCTION-TARGET.md").write_text("x", encoding="utf-8")
        repo = _copy_fixture(tmp)
        junction = repo / ".claude" / "skills" / "clean-skill" / "references"
        status, reason = _create_junction(junction, ext)
        if status == "skip":
            print(f"  SKIP  Windows junction test not executed: {reason}")
            return
        # status == "created": the real security assertion (a FAILURE here is a
        # genuine FAIL of the suite, never a SKIP).
        rc, stdout = _run_capture(repo, "--json", str(tmp / "o.json"))
        assert rc == 2, f"a junctioned references dir must exit 2, got {rc}"
        assert not (tmp / "o.json").exists()
        assert "OUTSIDE-JUNCTION-TARGET" not in stdout
        ok("a Windows junction into the audited corpus is rejected (exit 2)")
        # remove the junction link (not its target) before cleanup
        try:
            os.rmdir(junction)
        except OSError:
            pass
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def test_junction_helper_is_portable() -> None:
    """Gate 2.9 portability regression: the unsupported-host branches must SKIP
    WITHOUT invoking subprocess.run and WITHOUT raising — proven deterministically
    by forcing command discovery to fail, so no real non-Windows host is needed.
    A `subprocess.run` invocation on either branch fails the test loudly."""
    def _boom(*_a, **_k):
        raise AssertionError("subprocess.run must NOT be called on an unsupported host")

    # (a) non-Windows host: skip before any interpreter lookup or run.
    with mock.patch.object(os, "name", "posix"), \
            mock.patch.object(subprocess, "run", _boom):
        status, reason = _create_junction(Path("link"), Path("target"))
    assert status == "skip" and "Windows" in reason, (status, reason)

    # (b) Windows host but no cmd interpreter on PATH: skip before any run.
    with mock.patch.object(os, "name", "nt"), \
            mock.patch.object(shutil, "which", return_value=None), \
            mock.patch.object(subprocess, "run", _boom):
        status, reason = _create_junction(Path("link"), Path("target"))
    assert status == "skip" and "interpreter" in reason, (status, reason)

    # (c) Windows host, interpreter found, but it vanishes at call time
    # (PATH race): the FileNotFoundError is caught and turned into a SKIP.
    def _raise_fnf(*_a, **_k):
        raise FileNotFoundError(2, "No such file or directory", "cmd.exe")

    with mock.patch.object(os, "name", "nt"), \
            mock.patch.object(shutil, "which", return_value="cmd.exe"), \
            mock.patch.object(subprocess, "run", _raise_fnf):
        status, reason = _create_junction(Path("link"), Path("target"))
    assert status == "skip" and "unavailable" in reason, (status, reason)

    ok("junction helper is portable: unsupported hosts SKIP with no subprocess.run "
       "and no raise (non-Windows / no-cmd / PATH-race)")


def test_agent_file_symlink_rejected() -> None:
    tmp = Path(tempfile.mkdtemp(prefix="aegis-af-"))
    try:
        marker = "AEGIS-G27-AGENT-FILE-CONTENT"
        (tmp / "external-agent.md").write_text(marker + "\n", encoding="utf-8")
        repo = _copy_fixture(tmp)
        link = repo / ".claude" / "agents" / "linked-agent.md"
        try:
            os.symlink(tmp / "external-agent.md", link)
        except OSError as exc:
            if _skip_if_no_symlink(exc):
                return
            raise
        rc, stdout = _run_capture(repo)
        assert rc == 2, f"a symlinked agent file must exit 2, got {rc}"
        assert marker not in stdout
        ok("a symlinked agent file is rejected before its stem/content is used")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


# --- fixture layout: neutral source, no live-session discovery (Gate 2.7) ----


def test_fixture_source_is_neutral_layout() -> None:
    # the TRACKED source must use dot-claude and contain NO literal .claude that
    # the harness would discover as live skills.
    assert (_FIXTURE_SRC / "dot-claude" / "skills").is_dir(), (
        "tracked fixture source must use the neutral dot-claude/skills layout"
    )
    assert not (_FIXTURE_SRC / ".claude").exists(), (
        "tracked fixture source must NOT contain a literal .claude/ directory"
    )
    # the audited copy is a throwaway OUTSIDE the repo with a materialized .claude
    assert (FIXTURE_REPO / ".claude" / "skills").is_dir()
    assert str(REAL_REPO.resolve()) not in str(FIXTURE_REPO.resolve()), (
        "materialized fixture must live outside the Project Aegis repository"
    )
    ok("fixture source uses neutral dot-claude; .claude is materialized only in a temp repo")


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
    test_approved_doc_writer_is_silent(a)
    test_exact_rule_multisets(a)
    test_every_rule_has_own_positive_and_negative(a)
    test_route_rules(a)
    test_route002_is_unmapped_census(a)
    test_side004_fixture_classes(a)
    test_side004_real_corpus_targets()
    test_side004_approval_elsewhere_never_suppresses()
    test_eval004_two_classes(a)
    test_state_rules_map_to_aegis(a)
    test_mechanical_flag_matches_inventory(a)
    test_negation_guard()
    test_append_decl_scoping()
    test_stage2_segment()
    test_stage2_malformed_and_leakage()
    test_rule_inventory_complete(a)
    test_real_inventory_includes_zero_hit_rules()
    test_provenance_snapshot(a)
    test_provenance_content_sensitivity_and_inclusion()
    test_corpus_hash_follows_declared_posix_order()
    test_input_symlink_reference_fails_closed()
    test_input_symlink_skill_dir_fails_closed()
    test_input_containment_accepts_regular_files()
    test_escaping_markdown_link_is_flagged_not_passed()
    test_catalog_symlink_fails_closed()
    test_agents_dir_symlink_leaks_no_filenames()
    test_paths_dir_symlink_leaks_no_filenames()
    test_agent_file_symlink_rejected()
    test_skills_root_symlink_rejected()
    test_junction_escape_rejected()
    test_junction_helper_is_portable()
    test_fixture_source_is_neutral_layout()
    test_auxiliary_inputs_provenance()
    test_wrong_path_fails()
    test_refuses_to_write_into_skills()
    test_write_refusal_resolves_symlink_escape()
    test_real_corpus_pinned()
    test_deterministic(a)
    print(f"\nOK: {len(PASSES)} contract-audit self-test assertion(s) passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
