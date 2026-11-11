"""Read-only CLI for the aegis.evidence-reuse/1 validator.

Usage (from the repository root):

    python -m tools.aegis_evidence_reuse --self-test
    python -m tools.aegis_evidence_reuse validate --record reuse.json \
        --target-head <40-hex> [--evidence evidence.json | --evidence -] \
        [--change-id ID] [--repo-root .] [--json]

Exit codes:
    0  the record is schema-valid and its effective decision is VALID
    1  the record is invalid, stale or not yet VALID (fail closed)
    2  invalid input / usage / parse failure
    3  internal error (never 0)

The CLI never writes, never approves and never claims enforcement.  A VALID
decision is a record, not an approval, and cannot waive required CI.
"""

from __future__ import annotations

import argparse
import json
import sys
import traceback
import typing
from pathlib import Path

from . import schema, validate

EXIT_VALID = 0
EXIT_INVALID = 1
EXIT_USAGE = 2
EXIT_INTERNAL = 3


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="python -m tools.aegis_evidence_reuse",
        description=(
            "Read-only validator for aegis.evidence-reuse/1 decisions. "
            "Auditable tooling, not enforcement."
        ),
    )
    parser.add_argument("command", nargs="?", choices=("validate",), default="validate")
    parser.add_argument("--record")
    parser.add_argument("--target-head")
    parser.add_argument("--change-id")
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--evidence", action="append", default=[])
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--self-test", action="store_true")
    return parser


def _dump(result: typing.Mapping[str, object]) -> str:
    return json.dumps(result, sort_keys=True, indent=2, ensure_ascii=False)


def _load_requirements(repo_root: Path) -> typing.Optional[typing.Set[str]]:
    path = repo_root / "docs" / "conformance" / "requirements.v1.json"
    try:
        document = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None
    requirements = document.get("requirements") if isinstance(document, dict) else None
    if not isinstance(requirements, list):
        return None
    return {
        str(entry.get("requirement_id"))
        for entry in requirements
        if isinstance(entry, dict) and entry.get("requirement_id")
    }


def _load_evidence(paths: typing.Sequence[str]) -> typing.List[typing.Mapping[str, object]]:
    records: typing.List[typing.Mapping[str, object]] = []
    for value in paths:
        if value == "-":
            raw = sys.stdin.read()
            document = json.loads(raw)
        else:
            document = json.loads(Path(value).read_text(encoding="utf-8"))
        if isinstance(document, list):
            entries: typing.List[object] = list(document)
        else:
            entries = [document]
        for entry in entries:
            if not isinstance(entry, dict):
                raise ValueError("evidence set entries must be JSON objects")
            records.append(entry)
    return records


def _self_test() -> int:
    report = schema.self_test()
    sample = schema.sample_record()
    evidence = {"evidence_id": "EV-SELFTEST-1", "sha256": "1" * 64, "head": "a" * 40, "kind": "docs-review"}
    result = validate.validate_record(
        sample,
        target_head="d" * 40,
        change_id=42,
        evidence_records=[evidence],
        requirement_ids={"MG1"},
    )
    report["validation_ok"] = result["valid"] is True and result["effective_decision"] == "VALID"
    report["ok"] = bool(report["ok"] and report["validation_ok"])
    print(_dump(report))
    return EXIT_VALID if report["ok"] else EXIT_INTERNAL


def main(argv: typing.Optional[typing.Sequence[str]] = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)
    if args.self_test:
        return _self_test()
    if not args.record:
        parser.error("validate requires --record")
    if not args.target_head:
        parser.error("validate requires --target-head (the current authoritative target)")
    try:
        record = json.loads(Path(args.record).read_text(encoding="utf-8"))
    except (OSError, ValueError) as error:
        print("invalid input: record is unreadable or not JSON: %s" % error, file=sys.stderr)
        return EXIT_USAGE
    try:
        evidence_records = _load_evidence(args.evidence)
    except (OSError, ValueError) as error:
        print("invalid input: evidence set is unreadable or not JSON: %s" % error, file=sys.stderr)
        return EXIT_USAGE
    requirements = _load_requirements(Path(args.repo_root).resolve())
    if requirements is None:
        # Fail closed for requirement references: an unavailable catalog cannot
        # verify them, so the empty set denies every cited id.
        requirements = set()
    try:
        result = validate.validate_record(
            record,
            target_head=args.target_head,
            change_id=args.change_id,
            evidence_records=evidence_records,
            requirement_ids=requirements,
        )
    except Exception:  # noqa: BLE001 - internal failures must never exit 0
        print("internal error", file=sys.stderr)
        traceback.print_exc(file=sys.stderr)
        return EXIT_INTERNAL
    print(_dump(result))
    return EXIT_VALID if result["valid"] else EXIT_INVALID


if __name__ == "__main__":
    sys.exit(main())
