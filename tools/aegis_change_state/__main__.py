"""Command line entry point for the change-state producers/validators.

    python -m tools.aegis_change_state self-test
    python -m tools.aegis_change_state validate --bundle <dir> [--repo <repo>]
    python -m tools.aegis_change_state build --out <dir>
    python -m tools.aegis_change_state snapshot-manifest --repo <repo> ...

Exit codes mirror the merged checker: 0 = the supplied records are internally
valid (never readiness, never approval), 1 = defects/blocked, 2 = invalid
input/usage, 3 = internal error.  Output is deterministic JSON; no timestamp
or environment value is generated.  The only writes are to an explicit
caller-supplied --out path; nothing is written into the repository.
"""

from __future__ import annotations

import argparse
import json
import shutil
import tempfile
import typing
from pathlib import Path

from . import ASSURANCE, NOT_VERIFIABLE, TOOL_NAME, __version__
from . import checks, records, schema, snapshot

EXIT_OK = 0
EXIT_BLOCKED = 1
EXIT_INVALID = 2
EXIT_INTERNAL = 3

FIXTURE_DIR = Path(__file__).resolve().parent / "tests" / "fixtures"


def _json_text(document: object) -> str:
    return json.dumps(document, indent=2, sort_keys=True, ensure_ascii=False) + "\n"


def _fixture(name: str) -> typing.Dict[str, object]:
    document = schema.load_json(FIXTURE_DIR / name)
    if not isinstance(document, dict):
        raise schema.SchemaError("fixture %s is not an object" % name)
    return document


def _payload(name: str) -> typing.Dict[str, object]:
    document = _fixture(name)
    payload = document.get("payload")
    if not isinstance(payload, dict):
        raise schema.SchemaError("fixture %s has no payload" % name)
    return payload


def _envelope(
    payload: typing.Mapping[str, object],
    hint: typing.Mapping[str, object],
    *,
    default_role: str,
    status: typing.Optional[str] = None,
) -> typing.Dict[str, object]:
    provenance = hint.get("provenance") if isinstance(hint.get("provenance"), dict) else {}
    return schema.build_envelope(
        payload,
        source_ref=str(provenance.get("source_ref") or "change-state-fixture"),
        as_of=str(provenance.get("as_of") or "2026-11-11T00:00:00Z"),
        producer_role=str(provenance.get("producer_role") or default_role),
        producer_identity_ref=str(provenance.get("producer_identity_ref") or default_role),
        status=status if status is not None else provenance.get("status"),
    )


def build_bundle(out: typing.Union[str, Path], fixture_dir: typing.Union[str, Path] = FIXTURE_DIR) -> typing.Dict[str, object]:
    """Materialise the valid fixture set into a bundle at a caller-supplied path.

    Only mechanical values are computed (payload hashes, stage-record bytes and
    hashes, the ledger chain, the manifest digest).  Semantic values - the
    freeze "valid" flag, the settlement "settled" flag and the stage verdicts -
    are authored in the fixture and are never "fixed" by the builder.
    """

    global FIXTURE_DIR
    original = FIXTURE_DIR
    FIXTURE_DIR = Path(fixture_dir)
    try:
        freeze_payload = dict(_payload("valid-freeze.json"))
        settlement_payload = dict(_payload("valid-settlement.json"))
        snapshot_payload = dict(_payload("snapshot-manifest-valid.json"))
        head_payload = dict(_payload("head-history-valid.json"))
        freeze_hint = _fixture("valid-freeze.json")
        settlement_hint = _fixture("valid-settlement.json")
        snapshot_hint = _fixture("snapshot-manifest-valid.json")
        head_hint = _fixture("head-history-valid.json")

        change_id = str(freeze_payload.get("change_id"))
        out_path = Path(out).resolve()
        if out_path.exists():
            shutil.rmtree(out_path)
        out_path.mkdir(parents=True)
        written: typing.List[typing.Dict[str, object]] = []

        immutable = freeze_payload.get("immutable_inputs")
        if isinstance(immutable, dict):
            freeze_payload["immutable_inputs_sha256"] = schema.immutable_inputs_digest(immutable)
        freeze_envelope = _envelope(freeze_payload, freeze_hint, default_role="freeze-holder")
        records.write_json(out_path / "freeze" / (change_id + ".json"), freeze_envelope)
        written.append(records.file_entry(out_path, "freeze/%s.json" % change_id, kind="freeze", record_id=str(freeze_payload.get("freeze_id"))))

        settlement_envelope = _envelope(settlement_payload, settlement_hint, default_role="reviewer-coordinator")
        records.write_json(out_path / "settlement" / (change_id + ".json"), settlement_envelope)
        written.append(records.file_entry(out_path, "settlement/%s.json" % change_id, kind="settlement", record_id=str(settlement_payload.get("settlement_id"))))

        snapshot_id = str(snapshot_payload.get("snapshot_id"))
        snapshot_envelope = _envelope(snapshot_payload, snapshot_hint, default_role="snapshot-producer")
        records.write_json(out_path / "snapshots" / (change_id + ".json"), snapshot_envelope)
        written.append(records.file_entry(out_path, "snapshots/%s.json" % change_id, kind="snapshot", record_id=snapshot_id))

        for stage in ("B", "D", "E"):
            fixture = _fixture("stage-%s.json" % stage)
            payload = dict(_payload("stage-%s.json" % stage))
            body = fixture.get("record")
            if not isinstance(body, dict):
                raise schema.SchemaError("stage-%s fixture carries no record body" % stage)
            body_path = "records/%s.json" % stage
            body_bytes = schema.dumps(body).encode("utf-8")
            (out_path / "records").mkdir(exist_ok=True)
            (out_path / body_path).write_bytes(body_bytes + b"\n")
            payload["record_path"] = body_path
            payload["bytes"] = len(body_bytes) + 1
            payload["sha256"] = schema.sha256_hex(body_bytes + b"\n")
            payload["snapshot_identity"] = snapshot_id
            envelope = _envelope(payload, fixture, default_role="%s-stage-holder" % stage)
            records.write_json(out_path / "stage-records" / (stage + ".json"), envelope)
            written.append(records.file_entry(out_path, body_path, kind="stage_record_body", record_id=str(payload.get("record_id"))))
            written.append(records.file_entry(out_path, "stage-records/%s.json" % stage, kind="stage_declaration", record_id=str(payload.get("record_id"))))

        head_envelope = _envelope(head_payload, head_hint, default_role="head-history-export", status="VERIFIED")
        records.write_json(out_path / "head-history" / (change_id + ".json"), head_envelope)
        written.append(records.file_entry(out_path, "head-history/%s.json" % change_id, kind="head_history", record_id=str(head_payload.get("export_ref"))))

        events = []
        heads = head_payload.get("heads") if isinstance(head_payload.get("heads"), list) else []
        for head in heads:
            events.append(
                {
                    "head_sha": head.get("head_sha"),
                    "kind": head.get("kind"),
                    "exception_ref": head.get("exception_ref"),
                    "counted_at": head.get("counted_at"),
                    "recorded_by": "change-state-producer",
                }
            )
        ledger_path = out_path / "ledger" / (change_id + ".jsonl")
        records.write_ledger(ledger_path, events)
        written.append(
            records.file_entry(
                out_path,
                "ledger/%s.jsonl" % change_id,
                kind="change_ledger",
                record_id=change_id,
                event_count=len(events),
            )
        )

        manifest = records.build_manifest(
            change_id,
            sorted(written, key=lambda entry: str(entry.get("path"))),
            {
                "review_heads": {
                    "used": len(events),
                    "source": "change ledger (previously published heads only)",
                },
                "records": {
                    "freeze": 1,
                    "settlement": 1,
                    "stage_records": 3,
                    "snapshots": 1,
                    "ledgers": 1,
                },
            },
        )
        records.write_json(out_path / "manifest.json", manifest)
        return {"ok": True, "out": str(out_path), "files": sorted([entry["path"] for entry in written] + ["manifest.json"])}
    finally:
        FIXTURE_DIR = original


def cmd_build(args: argparse.Namespace) -> int:
    fixture_dir = Path(args.source).resolve() if args.source else FIXTURE_DIR
    result = build_bundle(args.out, fixture_dir)
    print(_json_text(result))
    return EXIT_OK


def cmd_validate(args: argparse.Namespace) -> int:
    identity = None
    if args.repo_slug and args.merge_target and args.head and args.change_id:
        identity = {
            "repo": args.repo_slug,
            "change_id": args.change_id,
            "head_sha": args.head,
            "merge_target_ref": args.merge_target,
        }
    report = checks.validate_bundle(
        args.bundle,
        identity=identity,
        base_ref=args.base_ref,
        plan_audit_applies=not args.no_plan_audit_applies,
        snapshot_repo=args.repo,
    )
    report["bundle"] = str(Path(args.bundle))
    print(_json_text(report))
    return EXIT_OK if report["ok"] else EXIT_BLOCKED


def cmd_snapshot_manifest(args: argparse.Namespace) -> int:
    manifest = snapshot.build_manifest(
        args.repo,
        args.commit,
        change_id=args.change_id,
        base=args.base,
        retention_ref=args.retention_ref,
        created_by=args.created_by,
        created_at=args.created_at,
    )
    issues = snapshot.verify_manifest(args.repo, manifest)
    out = Path(args.out)
    records.write_json(out, manifest)
    print(
        _json_text(
            {
                "ok": not issues,
                "out": str(out),
                "manifest": manifest,
                "issues": [issue.as_dict() for issue in issues],
                "assurance": {
                    "claim": ASSURANCE["claim"],
                    "mounted_coverage": ASSURANCE["mounted_coverage"],
                    "enforced": "BLOCKED",
                },
            }
        )
    )
    return EXIT_OK if not issues else EXIT_BLOCKED


def cmd_self_test(args: argparse.Namespace) -> int:
    results: typing.List[typing.Dict[str, object]] = []

    value = {"b": [True, None, "x"], "a": 1}
    text = schema.dumps(value)
    expected = '{"a":1,"b":[true,null,"x"]}'
    results.append(
        {
            "name": "canonicalization",
            "ok": text == expected and schema.digest(value) == schema.sha256_hex(expected.encode("utf-8")),
            "detail": text,
        }
    )

    temporary = Path(tempfile.mkdtemp(prefix="aegis-change-state-"))
    try:
        bundle = temporary / "bundle"
        build_bundle(bundle)
        report = checks.validate_bundle(bundle)
        results.append(
            {
                "name": "bundle-round-trip",
                "ok": report["ok"],
                "detail": "%d blocker(s)" % len(report["blockers"]),
            }
        )

        ledgers = sorted((bundle / "ledger").glob("*.jsonl"))
        tamper_detail: typing.List[str] = ["no ledger"]
        tamper_ok = False
        if ledgers:
            raw = ledgers[0].read_bytes()
            fake = schema.dumps(
                {
                    "seq": 99,
                    "head_sha": "d" * 40,
                    "kind": "INITIAL",
                    "exception_ref": None,
                    "counted_at": "2026-11-11T00:00:00Z",
                    "recorded_by": "tamper",
                    "prev_event_sha256": None,
                }
            ).encode("utf-8")
            ledgers[0].write_bytes(raw + fake + b"\n")
            tampered = checks.validate_bundle(bundle)
            codes = sorted({blocker["code"] for blocker in tampered["blockers"]})
            tamper_ok = (not tampered["ok"]) and "STATE_TAMPER_SUSPECTED" in codes
            tamper_detail = codes
        results.append({"name": "tamper-detection", "ok": tamper_ok, "detail": tamper_detail})

        overclaim = checks.assurance_issues({"assurance_claim": "ENFORCED", "mounted_coverage": "VERIFIED"})
        results.append(
            {
                "name": "overclaim-refusal",
                "ok": len(overclaim) >= 2,
                "detail": [issue.code for issue in overclaim],
            }
        )
    finally:
        shutil.rmtree(temporary, ignore_errors=True)

    ok = all(bool(item["ok"]) for item in results)
    print(
        _json_text(
            {
                "ok": ok,
                "tool": TOOL_NAME,
                "version": __version__,
                "checks": results,
                "assurance": {
                    "claim": ASSURANCE["claim"],
                    "mounted_coverage": ASSURANCE["mounted_coverage"],
                    "enforced": "BLOCKED",
                },
                "readiness": "NOT_COMPUTED",
                "not_verifiable": list(NOT_VERIFIABLE),
            }
        )
    )
    return EXIT_OK if ok else EXIT_BLOCKED


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="python -m tools.aegis_change_state",
        description="Aegis C1.2 change-state producers/validators (auditable tooling, not enforcement)",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    self_test = subparsers.add_parser("self-test", help="run the built-in canonical/append-only checks")
    self_test.set_defaults(func=cmd_self_test)

    validate = subparsers.add_parser("validate", help="validate one complete change-state bundle")
    validate.add_argument("--bundle", required=True)
    validate.add_argument("--repo", default=None, help="repository a snapshot manifest must reproduce from")
    validate.add_argument("--base-ref", default=None, help="git base for the append-only prefix check")
    validate.add_argument("--repo-slug", default=None, help="owner/name, for a disposition-authority scope")
    validate.add_argument("--change-id", default=None)
    validate.add_argument("--head", default=None)
    validate.add_argument("--merge-target", default=None)
    validate.add_argument("--no-plan-audit-applies", action="store_true")
    validate.add_argument("--json", action="store_true", help="accepted; output is always JSON")
    validate.set_defaults(func=cmd_validate)

    build = subparsers.add_parser("build", help="materialise the valid fixture set into a bundle")
    build.add_argument("--out", required=True)
    build.add_argument("--from", dest="source", default=None)
    build.set_defaults(func=cmd_build)

    snap = subparsers.add_parser("snapshot-manifest", help="write one per-head snapshot manifest")
    snap.add_argument("--repo", required=True)
    snap.add_argument("--commit", required=True)
    snap.add_argument("--change-id", required=True)
    snap.add_argument("--base", required=True)
    snap.add_argument("--retention-ref", required=True)
    snap.add_argument("--created-by", required=True)
    snap.add_argument("--created-at", required=True)
    snap.add_argument("--out", required=True)
    snap.set_defaults(func=cmd_snapshot_manifest)
    return parser


def main(argv: typing.Optional[typing.Sequence[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return int(args.func(args))
    except (schema.SchemaError, snapshot.SnapshotError) as error:
        print(_json_text({"ok": False, "error": "invalid input", "detail": str(error)}))
        return EXIT_INVALID
    except OSError as error:
        print(_json_text({"ok": False, "error": "invalid input", "detail": str(error)}))
        return EXIT_INVALID
    except Exception as error:  # internal error must never exit 0
        import traceback

        traceback.print_exc()
        print(_json_text({"ok": False, "error": "internal error", "detail": str(error)}))
        return EXIT_INTERNAL


if __name__ == "__main__":
    raise SystemExit(main())
