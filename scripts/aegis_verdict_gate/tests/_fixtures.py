"""Build the self-contained fixture bundles into a temporary repository.

Each file under fixtures/ is one complete bundle:

    {case_id, notes, verdict, inputs:{freeze, settlement, revision_state,
     head_history, stage_records[]}, expected:{readiness, blocker_codes[]}}

No fixture shares data with another and no fixture reads the real repository:
build() writes a throw-away repository (register, record store, stage record
declarations, input envelopes) under a temporary directory and run() executes
the checker against it.

Only mechanical values are computed here (hashes, byte counts, manifest
indexes, event hash chains and the conditionals table); every semantic value
is authored in the bundle, and a bundle can deliberately corrupt a computed
value through its "overrides" block.  Data is synthetic: no real PR, no real
identity, no secret.  The register text each bundle carries is marked
SYNTHETIC and is not an approval.
"""

from __future__ import annotations

import copy
import json
import pathlib
import subprocess
import sys
import tempfile

SCRIPTS_DIR = pathlib.Path(__file__).resolve().parents[2]
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from aegis_verdict_gate import canonical, gate, records  # noqa: E402

FIXTURE_DIR = pathlib.Path(__file__).resolve().parent / "fixtures"
FIXTURE_AUTH_METHOD = "provider-event-author"
RECORDS_DIR = "docs/approvals/revision-state"


def load_bundle(name: str) -> dict:
    """Load one fixture bundle by file stem."""

    path = FIXTURE_DIR / (name if name.endswith(".json") else name + ".json")
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def fixture_names() -> list:
    return sorted(path.stem for path in FIXTURE_DIR.glob("*.json"))


def load_bundles() -> list:
    return [load_bundle(name) for name in fixture_names()]


def _write(path: pathlib.Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")


def _git(root: pathlib.Path, *args: str) -> str:
    """Run one git command for the synthetic base commit (fixture plumbing)."""

    completed = subprocess.run(
        ["git", "-C", str(root)] + list(args), capture_output=True, check=False, timeout=60
    )
    if completed.returncode != 0:
        raise RuntimeError(
            "fixture git %s failed: %s" % (args, completed.stderr.decode("utf-8", "replace"))
        )
    return completed.stdout.decode("utf-8", "replace")


def commit_base(root: pathlib.Path) -> None:
    """Make the fixture repository a real worktree with a resolvable git base.

    The store's append-only prefix invariant is a required input, so a fixture
    repository without a base would (correctly) fail closed.  The synthetic
    base commit and refs/remotes/origin/main are fixture plumbing only.
    """

    _git(root, "init", "-q", "-b", "main")
    _git(root, "config", "user.email", "fixture@example.invalid")
    _git(root, "config", "user.name", "Fixture Builder")
    _git(root, "config", "core.autocrlf", "false")
    _git(root, "add", "-A")
    _git(root, "commit", "-q", "-m", "synthetic fixture base")
    _git(root, "update-ref", "refs/remotes/origin/main", "HEAD")


def _write_envelope(path: pathlib.Path, payload: dict, provenance_extra: dict) -> None:
    provenance = {
        "source_ref": provenance_extra["source_ref"],
        "as_of": provenance_extra["as_of"],
        "producer_role": provenance_extra["producer_role"],
        "producer_identity_ref": provenance_extra.get("producer_identity_ref"),
        "declared_payload_sha256": canonical.digest(payload),
        "declared_payload_bytes": len(canonical.canonical_bytes(payload)),
    }
    if "status" in provenance_extra:
        provenance["status"] = provenance_extra["status"]
    document = {"payload": payload, "provenance": provenance}
    _write(path, json.dumps(document, sort_keys=True, indent=2, ensure_ascii=False) + "\n")


def _conditionals(doc: dict) -> list:
    applied = []
    plan = doc.get("plan") if isinstance(doc.get("plan"), dict) else {}
    if plan.get("sha256"):
        applied.append({"condition_id": "VB-C03", "applied": True, "basis_ref": "plan-of-record applies"})
    else:
        applied.append({"condition_id": "VB-C05", "applied": True, "basis_ref": "no plan-of-record basis cited"})
    exception = doc.get("review_heads", {}).get("exception_id")
    if exception:
        applied.append({"condition_id": "VB-C08", "applied": True, "basis_ref": str(exception)})
    if doc.get("plan_audit_applies") is False:
        applied.append({"condition_id": "VB-D03", "applied": True, "basis_ref": str(doc.get("plan_audit_waiver_ref"))})
    if not doc.get("merge_authority_ref"):
        applied.append(
            {"condition_id": "VB-G03", "applied": False, "basis_ref": "readiness gate only; merge authority is separate"}
        )
    skills = doc.get("skills") if isinstance(doc.get("skills"), dict) else {}
    if not skills.get("rows") and skills.get("none_reason"):
        applied.append({"condition_id": "VB-H02", "applied": True, "basis_ref": "no skill applied"})
    return sorted(applied, key=lambda entry: entry["condition_id"])


def build(bundle: dict, root: pathlib.Path) -> dict:
    """Materialise one bundle under root and return the paths the CLI needs."""

    overrides = bundle.get("overrides", {})
    register_text = bundle["inputs"]["revision_state"]["register_text"]
    register_path = root / records.REGISTER_RELATIVE_PATH
    _write(register_path, register_text)
    register_sha = canonical.sha256_hex(register_path.read_bytes())

    # --- record store -----------------------------------------------------
    store_dir = root / RECORDS_DIR
    items_dir = store_dir / "items"
    changes_dir = store_dir / "changes"
    items_dir.mkdir(parents=True, exist_ok=True)
    changes_dir.mkdir(parents=True, exist_ok=True)
    file_entries = []
    derived_items = []
    for item_id, events in sorted(bundle["inputs"]["revision_state"]["items"].items()):
        slug = item_id.rsplit(".", 1)[-1]
        relative = "items/%s.jsonl" % slug
        lines = []
        previous = None
        revision_count = 0
        reopen_count = 0
        stop_state = None
        for index, raw_event in enumerate(events):
            event = copy.deepcopy(raw_event)
            event.setdefault("event_id", "%s-%04d" % (slug[:8].upper(), index + 1))
            authority = event.get("authority_ref")
            if isinstance(authority, dict) and not authority.get("authority_ref_sha256"):
                authority["authority_ref_sha256"] = register_sha
            event["prev_event_sha256"] = previous
            line = canonical.dumps(event).encode("utf-8")
            lines.append(line)
            previous = canonical.sha256_hex(line)
            if event.get("event_kind") == "REVISION_RECORDED":
                revision_count += 1
            if event.get("reopen_counted") is True:
                reopen_count += 1
            if event.get("event_kind") == "STOP_STATE_SET":
                stop_state = event.get("stop_state")
        raw = b"\n".join(lines) + b"\n"
        (store_dir / relative).write_bytes(raw)
        file_entries.append(
            {
                "path": relative,
                "kind": "plan_item",
                "id": item_id,
                "bytes": len(raw),
                "sha256": canonical.sha256_hex(raw),
                "event_count": len(lines),
                "first_event_id": json.loads(lines[0].decode("utf-8")).get("event_id"),
                "last_event_id": json.loads(lines[-1].decode("utf-8")).get("event_id"),
            }
        )
        derived_items.append(
            {
                "item_id": item_id,
                "revision_count": revision_count,
                "reopen_used": reopen_count > 0,
                "stop_state": stop_state,
            }
        )
    ledger_events = bundle["inputs"]["revision_state"].get("change_ledger", [])
    ledger_relative = "changes/c1-1-b1-minimal-2026-11-10.jsonl"
    ledger_lines = []
    for index, raw_event in enumerate(ledger_events):
        event = copy.deepcopy(raw_event)
        event["seq"] = index + 1
        ledger_lines.append(canonical.dumps(event).encode("utf-8"))
    ledger_raw = b"\n".join(ledger_lines) + b"\n" if ledger_lines else b""
    (store_dir / ledger_relative).write_bytes(ledger_raw)
    file_entries.append(
        {
            "path": ledger_relative,
            "kind": "change_ledger",
            "id": "c1-1-b1-minimal-2026-11-10",
            "bytes": len(ledger_raw),
            "sha256": canonical.sha256_hex(ledger_raw),
            "event_count": len(ledger_lines),
            "first_event_id": None,
            "last_event_id": None,
        }
    )
    derived_counts = {
        "items": sorted(derived_items, key=lambda entry: entry["item_id"]),
        "review_heads": {
            "used": len(ledger_lines),
            "source": "change ledger (previously published heads only)",
        },
    }
    digest_files = [
        {
            "path": entry["path"],
            "bytes": entry["bytes"],
            "sha256": entry["sha256"],
            "event_count": entry["event_count"],
            "id": entry["id"],
            "kind": entry["kind"],
        }
        for entry in sorted(file_entries, key=lambda entry: entry["path"])
    ]
    store_digest = canonical.digest(
        {
            "schema_version": "aegis.revision-store/v1",
            "files": digest_files,
            "derived_counts_at_binding": derived_counts,
        }
    )
    binding = {
        "authority_kind": "REGISTER_ENTRY",
        "authority_ref_id": "APR-FIXTURE-STORE-0001",
        "authority_ref_sha256": register_sha,
        "holder_role": "programme-lead",
        "holder_identity_ref": None,
        "binding_commit_or_pr": "fixture-build",
        "binding_status": "VERIFIED",
        "unverified_reason": None,
    }
    manifest = {
        "schema_version": "aegis.revision-store/v1",
        "files": file_entries,
        "derived_counts_at_binding": derived_counts,
        "store_digest": store_digest,
        "provenance_binding": binding,
    }
    manifest.update(bundle["inputs"]["revision_state"].get("manifest_overrides", {}))
    if overrides.get("store_digest"):
        manifest["store_digest"] = overrides["store_digest"]
    _write(store_dir / "manifest.json", json.dumps(manifest, sort_keys=True, indent=2, ensure_ascii=False) + "\n")

    # --- stage records ----------------------------------------------------
    head = bundle["verdict"]["head_sha"]
    declarations = []
    for declaration in bundle["inputs"]["stage_records"]:
        stage = declaration["stage"]
        record_path = "stage-records/%s.md" % stage.lower()
        _write(root / record_path, declaration["content"])
        raw = (root / record_path).read_bytes()
        sha = canonical.sha256_hex(raw)
        if isinstance(overrides.get("stage_record_sha"), dict) and overrides["stage_record_sha"].get(stage):
            sha = overrides["stage_record_sha"][stage]
        payload = {
            "stage": stage,
            "record_id": declaration["record_id"],
            "record_path": record_path,
            "bytes": len(raw),
            "sha256": sha,
            "head_sha": head,
            "verdict": declaration["verdict"],
            "holder_identity_ref": declaration["holder_identity_ref"],
            "independence_class": declaration["independence_class"],
            "snapshot_identity": declaration["snapshot_identity"],
            "completed_at": declaration["completed_at"],
        }
        declarations.append(payload)
        _write_envelope(
            root / "stage-records" / ("%s.json" % stage.lower()),
            payload,
            {
                "source_ref": "fixture-stage-%s" % stage.lower(),
                "as_of": declaration["completed_at"],
                "producer_role": declaration["holder_identity_ref"],
            },
        )
    declarations.sort(key=lambda entry: entry["stage"])

    # --- verdict ----------------------------------------------------------
    doc = copy.deepcopy(bundle["verdict"])
    record = doc["record"]
    body = record.get("body_text") or ("F verdict for %s\n\nAffirmative at this head.\n" % head)
    record["body_text"] = body
    doc["verdict"]["record_sha256"] = overrides.get(
        "record_sha256", canonical.sha256_hex(body.encode("utf-8"))
    )
    doc["stage_records"] = declarations
    doc["owner_line"]["register_sha256"] = register_sha
    record.setdefault("evidence_set", [])
    doc["evidence_inputs_sha256"] = canonical.digest(
        [
            {
                "evidence_id": item.get("evidence_id"),
                "sha256": item.get("sha256"),
                "head": item.get("head"),
            }
            for item in record["evidence_set"]
        ]
    )
    rows = sorted(
        [row for row in record.get("triage_rows", []) if isinstance(row, dict)],
        key=lambda row: (str(row.get("finding_id")), str(row.get("candidate_head"))),
    )
    doc["triage"]["sha256"] = canonical.digest(
        {"schema_version": "aegis.triage/v1", "rows": rows}
    )
    skills = doc["skills"]
    doc["skills"]["sha256"] = canonical.digest(
        {key: skills[key] for key in ("rows", "none_reason") if key in skills}
    )
    security = doc["security"]
    doc["security"]["sha256"] = canonical.digest(
        {
            "surfaces_touched": security["surfaces_touched"],
            "mitigations": security["mitigations"],
            "residual": security["residual"],
            "secret_read_or_logged": security["secret_read_or_logged"],
        }
    )
    witness = doc["witness"]
    doc["witness"]["sha256"] = canonical.digest(
        {"diff_name_only": witness["diff_name_only"], "probes": witness["probes"]}
    )
    doc["revision_state_sha256"] = overrides.get(
        "revision_state_sha256",
        canonical.digest(
            {
                "schema_version": "aegis.revision-state/v1",
                "items": [
                    {
                        "item_id": entry["item_id"],
                        "revision_count": entry["revision_count"],
                        "reopen_used": entry["reopen_used"],
                        "stop_state": entry["stop_state"],
                    }
                    for entry in sorted(derived_items, key=lambda entry: entry["item_id"])
                ],
            }
        ),
    )
    resolution = record.get("owner_line_resolution")
    if isinstance(resolution, dict) and not resolution.get("register_sha256"):
        resolution["register_sha256"] = register_sha
    doc["conditionals_applied"] = _conditionals(doc)
    doc["bound_fields_sha256"] = overrides.get(
        "bound_fields_sha256", canonical.bound_fields_sha256(doc)
    )
    verdict_path = root / "inputs" / "verdict.json"
    _write_envelope(
        verdict_path,
        doc,
        {
            "source_ref": "fixture-verdict",
            "as_of": "2026-11-10T20:03:00Z",
            "producer_role": "independent-f-reviewer",
        },
    )

    # --- freeze / settlement / head history -------------------------------
    freeze_payload = copy.deepcopy(bundle["inputs"]["freeze"])
    freeze_payload["candidate_id"] = freeze_payload.get("candidate_id") or doc["candidate_id"]
    freeze_payload["head_sha"] = freeze_payload.get("head_sha") or doc["head_sha"]
    freeze_payload["tree_sha"] = freeze_payload.get("tree_sha") or doc["tree_sha"]
    freeze_payload["base_sha"] = freeze_payload.get("base_sha") or doc["base_sha"]
    freeze_payload["immutable_inputs_sha256"] = canonical.digest(
        {
            "head": freeze_payload["head_sha"],
            "tree": freeze_payload["tree_sha"],
            "base": freeze_payload["base_sha"],
            "policy_sha256": doc["policy_sha256"],
            "plan_sha256": doc["plan"]["sha256"],
            "evidence_inputs_sha256": doc["evidence_inputs_sha256"],
        }
    )
    freeze_path = root / "inputs" / "freeze.json"
    _write_envelope(
        freeze_path,
        freeze_payload,
        {
            "source_ref": "fixture-freeze",
            "as_of": freeze_payload.get("frozen_at", "2026-11-10T19:30:00Z"),
            "producer_role": "freeze-holder",
        },
    )
    settlement_path = root / "inputs" / "settlement.json"
    if bundle["inputs"].get("settlement") is not None:
        _write_envelope(
            settlement_path,
            bundle["inputs"]["settlement"],
            {
                "source_ref": "fixture-settlement",
                "as_of": bundle["inputs"]["settlement"].get("as_of", "2026-11-10T19:45:00Z"),
                "producer_role": "reviewer-coordinator",
            },
        )
    head_history = copy.deepcopy(bundle["inputs"]["head_history"])
    status = head_history.pop("status", "VERIFIED")
    head_history.setdefault("change_id", doc["change"]["id"])
    head_history.setdefault("candidate_head", doc["head_sha"])
    head_history_path = root / "inputs" / "head-history.json"
    _write_envelope(
        head_history_path,
        head_history,
        {
            "source_ref": "fixture-head-history",
            "as_of": "2026-11-10T20:05:00Z",
            "producer_role": "records-steward",
            "status": status,
        },
    )
    commit_base(root)
    return {
        "root": root,
        "verdict": verdict_path,
        "freeze": freeze_path,
        "settlement": settlement_path,
        "head_history": head_history_path,
        "stage_records_dir": root / "stage-records",
        "store_dir": store_dir,
        "manifest": store_dir / "manifest.json",
    }


def run_bundle(bundle: dict, supported_auth_methods=(FIXTURE_AUTH_METHOD,), keep: bool = False) -> tuple:
    """Build the bundle in a temporary repository and run the checker."""

    temporary = pathlib.Path(tempfile.mkdtemp(prefix="aegis-verdict-gate-"))
    paths = build(bundle, temporary)
    result = gate.evaluate(
        repo_root=paths["root"],
        verdict_path=paths["verdict"],
        freeze_path=paths["freeze"],
        settlement_path=paths["settlement"],
        head_history_path=paths["head_history"],
        stage_records_dir=paths["stage_records_dir"],
        records_dir=RECORDS_DIR,
        supported_auth_methods=supported_auth_methods,
        fixture_mode=True,
    )
    if keep:
        return result, paths
    import shutil

    shutil.rmtree(str(temporary), ignore_errors=True)
    return result, None


def cleanup(paths) -> None:
    """Remove a built fixture repository (best effort)."""

    if paths is None:
        return
    import shutil

    shutil.rmtree(str(paths), ignore_errors=True)
