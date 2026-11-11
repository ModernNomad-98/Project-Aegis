"""Build synthetic preflight cases.

The record inputs come from the merged C1.1a checker's own synthetic fixture
builder (so PF-07 is composed against real fixture-mode checker behaviour).
The preflight bundle, its evidence/triage projections, the reuse record and the
small conformance catalogs are built here.  No real PR, identity, secret or
approval is used.

Each fixture JSON is a case: checker_case, mutations, optional include_reuse,
optional store/malformed-input mutations, and the expected statuses.
"""

from __future__ import annotations

import copy
import importlib.util
import json
import pathlib

from tools.aegis_preflight import models

REPO_ROOT = pathlib.Path(__file__).resolve().parents[3]
FIXTURE_DIR = pathlib.Path(__file__).resolve().parent / "fixtures"


def case_names() -> list:
    return sorted(path.stem for path in FIXTURE_DIR.glob("*.json"))


def load_case(name: str) -> dict:
    path = FIXTURE_DIR / (name if name.endswith(".json") else name + ".json")
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def _checker_fixtures():
    path = REPO_ROOT / "tools" / "aegis_verdict_gate" / "tests" / "_fixtures.py"
    spec = importlib.util.spec_from_file_location("aegis_merged_checker_fixtures", path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def _write(path: pathlib.Path, document: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(document, indent=2, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")


def _part(container: object, part: str):
    return int(part) if isinstance(container, list) else part


def _get(document: dict, dotted: str):
    current = document
    for part in dotted.split("."):
        key = _part(current, part)
        if isinstance(current, list):
            try:
                current = current[key]
            except IndexError as error:
                raise KeyError(dotted) from error
        elif not isinstance(current, dict) or key not in current:
            raise KeyError(dotted)
        else:
            current = current[key]
    return current


def _set(document: dict, dotted: str, value: object) -> None:
    parts = dotted.split(".")
    current: object = document
    for part in parts[:-1]:
        current = current[_part(current, part)]
    key = _part(current, parts[-1])
    current[key] = copy.deepcopy(value)


def _delete(document: dict, dotted: str) -> None:
    parts = dotted.split(".")
    current: object = document
    for part in parts[:-1]:
        current = current[_part(current, part)]
    key = _part(current, parts[-1])
    if isinstance(current, list):
        current.pop(key)
    else:
        current.pop(key, None)


def _apply(document: dict, mutations: list) -> None:
    for mutation in mutations:
        operation = mutation.get("op")
        path = mutation["path"]
        if operation == "set":
            _set(document, path, mutation["value"])
        elif operation == "delete":
            _delete(document, path)
        elif operation == "append":
            target = _get(document, path)
            if not isinstance(target, list):
                raise TypeError("%s is not a list" % path)
            target.append(copy.deepcopy(mutation["value"]))
        else:
            raise ValueError("unknown mutation op %r" % operation)


def _evidence_entries(payload: dict) -> list:
    record = payload.get("record") if isinstance(payload.get("record"), dict) else {}
    entries = []
    for item in record.get("evidence_set", []):
        if not isinstance(item, dict):
            continue
        entries.append(
            {
                "evidence_id": item.get("evidence_id"),
                "kind": "test-run",
                "bytes": 128,
                "sha256": item.get("sha256"),
                "scope": "tools/aegis_preflight/",
                "source_head": item.get("head"),
                "method": "python -m unittest",
                "environment": "python-3.14",
                "result": "PASS",
                "retention": "repository",
                "assurance": "AUDITABLE",
                "invalidation": "head-move",
                "evidence_ref": "../evidence/%s.stdout.txt" % item.get("evidence_id"),
            }
        )
    return entries


def _finding_entries(payload: dict, evidence: list) -> list:
    record = payload.get("record") if isinstance(payload.get("record"), dict) else {}
    evidence_ref = evidence[0]["evidence_id"] if evidence else "EV-NONE"
    findings = []
    for row in record.get("triage_rows", []):
        if not isinstance(row, dict):
            continue
        findings.append(
            {
                "finding_id": row.get("finding_id"),
                "class": row.get("class"),
                "disposition": row.get("disposition"),
                "candidate_head": row.get("candidate_head") or payload.get("head_sha"),
                "evidence_ref": evidence_ref,
                "decided_by": row.get("decided_by") or {"role": "F", "identity_ref": "role-f-fixture"},
                "backlog_id": row.get("backlog_id"),
            }
        )
    return findings


def _base_bundle(payload: dict, evidence: list, findings: list, paths: dict) -> dict:
    stage_dir = pathlib.Path(paths["stage_records_dir"])
    stage_names = sorted(path.name for path in stage_dir.glob("*.json"))
    assert len(stage_names) == 3, stage_names
    open_blocking = sum(
        1 for row in findings if row["class"] == "BLOCKING" and row["disposition"] != "FIXED"
    )
    residual_accepted = sum(1 for row in findings if row["disposition"] == "RESIDUAL_ACCEPTED")
    return {
        "schema_version": models.SCHEMA_VERSION,
        "subject": {
            "repo": payload["repo"],
            "change_id": payload["change"]["id"],
            "candidate": {
                "head_sha": payload["head_sha"],
                "tree_sha": payload["tree_sha"],
                "base_sha": payload["base_sha"],
            },
        },
        "inputs": {
            "verdict": "../inputs/verdict.json",
            "freeze": "../inputs/freeze.json",
            "settlement": "../inputs/settlement.json",
            "head_history": "../inputs/head-history.json",
            "stage_records": ["../stage-records/%s" % name for name in stage_names],
            "evidence": evidence,
            "triage": {
                "schema_version": "aegis.triage/v1",
                "findings": findings,
                "open_blocking": open_blocking,
                "residual_accepted_count": residual_accepted,
            },
            "reuse_decisions": [],
            "gate_status": {
                "MG1": "present",
                "MG2": "present",
                "MG3": "present",
                "MG4": "present",
                "MG5": "not applicable",
            },
        },
        "declared": {
            "claim": "MECHANICAL_CHECKS_ONLY",
            "generated_by": "c2-preflight-fixture-builder",
            "as_of": "2026-11-11T00:00:00Z",
        },
        "provenance": {
            "source_ref": "fixture:preflight",
            "as_of": "2026-11-11T00:00:00Z",
            "producer_role": "implementer",
            "producer_identity_ref": None,
            "declared_payload_sha256": "0" * 64,
            "declared_payload_bytes": 0,
            "status": "UNVERIFIED",
        },
    }


def _reuse_record(payload: dict, evidence: list) -> dict:
    first = evidence[0]
    record = {
        "schema_version": "aegis.evidence-reuse/1",
        "reuse_id": "REUSE-CLEAN-0001",
        "subject": {"repo": payload["repo"], "change_id": payload["change"]["id"]},
        "source": {
            "evidence_ids": [first["evidence_id"]],
            "source_head": payload["head_sha"],
            "source_tree": payload["tree_sha"],
            "source_base": payload["base_sha"],
            "source_records_sha256": [first["sha256"]],
            "requirement_ids": ["MG1"],
        },
        "target": {
            "target_head": payload["head_sha"],
            "target_tree": payload["tree_sha"],
            "target_base": payload["base_sha"],
        },
        "delta_class": "DOCS_TEXT_ONLY",
        "affected_inputs": ["docs/example.md"],
        "full_diff": {"name_only_ref": "fixture-diff-0001", "name_only_sha256": "2" * 64, "file_count": 1},
        "comparison": {
            "method": "name-only-diff",
            "tool": "git",
            "tool_version": "2.x",
            "ast_stripped": False,
            "ast_equality_sha256": None,
        },
        "excluded_claims": ["APPROVAL", "BEHAVIORAL_EQUIVALENCE", "CI_WAIVER", "COPIED_PASS"],
        "target_delta_checks": [
            {"check_id": "CI-REQUIRED", "kind": "REQUIRED_CI", "result": "PASS", "evidence_ref": first["evidence_id"]}
        ],
        "independence": {
            "qualifier_identity_ref": "role-e-fixture",
            "class": "INDEPENDENT",
            "attestation_ref": "ATT-FIXTURE-0001",
        },
        "decision": "VALID",
        "decision_authority": {
            "authority_kind": "OWNER_LINE_RECORD",
            "authority_ref_id": "OWNER-LINE-FIXTURE-0001",
            "authority_ref_sha256": "3" * 64,
        },
        "invalid_after": ["TARGET_HEAD_MOVE", "SOURCE_EVIDENCE_CHANGE"],
        "provenance": {
            "source_ref": "fixture:reuse",
            "as_of": "2026-11-11T00:00:00Z",
            "producer_role": "implementer",
            "producer_identity_ref": None,
            "declared_payload_sha256": "0" * 64,
            "declared_payload_bytes": 0,
        },
    }
    provenance = record["provenance"]
    provenance["declared_payload_sha256"] = models.digest(
        {key: value for key, value in record.items() if key != "provenance"}
    )
    provenance["declared_payload_bytes"] = len(
        models.canonical_bytes({key: value for key, value in record.items() if key != "provenance"})
    )
    return record


def _write_conformance(root: pathlib.Path) -> None:
    conformance = root / "docs" / "conformance"
    requirements = {
        "catalog_version": "fixture-1.0.0",
        "profiles": [],
        "requirements": [{"requirement_id": "MG1"}, {"requirement_id": "AEGIS-REQ-EVID-01"}],
    }
    requirements_path = conformance / "requirements.v1.json"
    _write(requirements_path, requirements)
    payload_path = conformance / "evidence" / "preflight.stdout.txt"
    payload_path.parent.mkdir(parents=True, exist_ok=True)
    payload_path.write_text("synthetic preflight evidence\n", encoding="utf-8", newline="\n")
    requirements_raw = requirements_path.read_bytes()
    payload_raw = payload_path.read_bytes()
    binding = {
        "schema": "aegis.evidence-binding/1",
        "catalog": {
            "path": "docs/conformance/requirements.v1.json",
            "bytes": len(requirements_raw),
            "sha256": models.sha256_bytes(requirements_raw),
        },
        "source_revision": "0" * 40,
        "records": [
            {
                "evidence_id": "L4-E-01",
                "requirement_ids": ["MG1"],
                "classification": "EXECUTED",
                "stdout_path": "evidence/preflight.stdout.txt",
                "stdout_bytes": len(payload_raw),
                "stdout_sha256": models.sha256_bytes(payload_raw),
            }
        ],
    }
    _write(conformance / "evidence-binding-v1.json", binding)


def build_case(case: dict, directory) -> dict:
    case_dir = pathlib.Path(directory)
    checker = _checker_fixtures()
    checker_bundle = checker.load_bundle(case["checker_case"])
    paths = checker.build(checker_bundle, case_dir)
    root = pathlib.Path(paths["root"])
    verdict_document = json.loads(pathlib.Path(paths["verdict"]).read_text(encoding="utf-8"))
    payload = verdict_document["payload"]
    evidence = _evidence_entries(payload)
    findings = _finding_entries(payload, evidence)
    bundle = _base_bundle(payload, evidence, findings, paths)
    _apply(bundle, case.get("mutations", []))
    if case.get("include_reuse"):
        reuse = _reuse_record(payload, evidence)
        _write(root / "preflight" / "reuse" / "REUSE-CLEAN-0001.json", reuse)
        bundle["inputs"]["reuse_decisions"] = ["reuse/REUSE-CLEAN-0001.json"]
    payload_without_provenance = {key: value for key, value in bundle.items() if key != "provenance"}
    bundle["provenance"]["declared_payload_sha256"] = models.digest(payload_without_provenance)
    bundle["provenance"]["declared_payload_bytes"] = len(models.canonical_bytes(payload_without_provenance))
    bundle_path = root / "preflight" / "bundle.json"
    _write(bundle_path, bundle)
    _write_conformance(root)
    if case.get("mutate_store"):
        item_files = sorted((root / "docs" / "approvals" / "revision-state" / "items").glob("*.jsonl"))
        with item_files[0].open("a", encoding="utf-8", newline="\n") as handle:
            handle.write('{"event_id": "TAMPER", "note": "synthetic stale-manifest fixture"}\n')
    if case.get("malformed_checker_input"):
        name = case["malformed_checker_input"]
        target = root / "inputs" / (name + ".json")
        target.write_text("{not json", encoding="utf-8", newline="\n")
    return {"root": root, "bundle": bundle_path, "paths": paths, "payload": payload, "case": case}
