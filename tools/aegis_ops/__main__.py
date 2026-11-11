"""Read-only CLI for tools/aegis_ops.

Usage (from the repository root):

    python -m tools.aegis_ops --self-test
    python -m tools.aegis_ops validate --input PATH [--json]
    python -m tools.aegis_ops settle --input PATH [--json]
    python -m tools.aegis_ops routing --input PATH [--workflow PATH] [--json]
    python -m tools.aegis_ops holders --input PATH [--json]
    python -m tools.aegis_ops inbox --input PATH [--json]
    python -m tools.aegis_ops pilot-metrics --input PATH [--json]

Exit codes: 0 supplied records valid and not blocked; 1 defects or a blocked
condition; 2 invalid input/usage; 3 internal error.  Output is deterministic
JSON; the tool writes nothing, makes no network call and reads no clock.
"""

from __future__ import annotations

import argparse
import json
import sys
import traceback
import typing

from . import events, holders, inbox_activity, pilot_metrics, routing, schema, settlement

EXIT_OK = 0
EXIT_BLOCKED = 1
EXIT_USAGE = 2
EXIT_INTERNAL = 3


class UsageError(Exception):
    pass


def _dump(value: object) -> str:
    return json.dumps(value, sort_keys=True, indent=2, ensure_ascii=False)


def _load(path: str) -> typing.Dict[str, object]:
    try:
        with open(path, "r", encoding="utf-8") as handle:
            document = json.load(handle)
    except OSError as error:
        raise UsageError("cannot read %s: %s" % (path, error))
    except (UnicodeDecodeError, ValueError) as error:
        raise UsageError("%s is not valid UTF-8 JSON: %s" % (path, error))
    if not isinstance(document, dict):
        raise UsageError("%s must contain a JSON object" % path)
    return typing.cast(typing.Dict[str, object], document)


def _dispatch(document: typing.Mapping[str, object]) -> typing.Dict[str, object]:
    version = document.get("schema_version")
    if version == schema.SCHEMA_EVENT:
        return events.validate(document)
    if version == schema.SCHEMA_SETTLEMENT:
        return settlement.settle(document)
    if version == schema.SCHEMA_ROUTING:
        return routing.validate_matrix(document)
    if version == schema.SCHEMA_HOLDERS:
        return holders.validate(document)
    if version == schema.SCHEMA_INBOX:
        return inbox_activity.validate(document)
    if version == schema.SCHEMA_PILOT_METRICS:
        return pilot_metrics.validate_pilot(document)
    if version == schema.SCHEMA_SUPPORT_MATRIX:
        return pilot_metrics.validate_support_matrix(document)
    raise UsageError(
        "unknown schema_version %r; expected one of %s"
        % (version, ", ".join(schema.KNOWN_SCHEMAS))
    )


def _result_exit(result: typing.Mapping[str, object]) -> int:
    if not result.get("valid", False):
        return EXIT_BLOCKED
    if result.get("blocked", False):
        return EXIT_BLOCKED
    return EXIT_OK


def _build_parser() -> argparse.ArgumentParser:
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--json", action="store_true", help="emit deterministic JSON (the default)")
    parser = argparse.ArgumentParser(
        prog="python -m tools.aegis_ops",
        description="Read-only C3/C4 ops record validation and derivation.",
    )
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--json", action="store_true", help="emit deterministic JSON (the default)")
    subparsers = parser.add_subparsers(dest="command")
    validate = subparsers.add_parser("validate", parents=[common])
    validate.add_argument("--input", required=True)
    settle = subparsers.add_parser("settle", parents=[common])
    settle.add_argument("--input", required=True)
    route = subparsers.add_parser("routing", parents=[common])
    route.add_argument("--input", required=True)
    route.add_argument("--workflow", default=None)
    hold = subparsers.add_parser("holders", parents=[common])
    hold.add_argument("--input", required=True)
    inbox = subparsers.add_parser("inbox", parents=[common])
    inbox.add_argument("--input", required=True)
    metrics = subparsers.add_parser("pilot-metrics", parents=[common])
    metrics.add_argument("--input", required=True)
    return parser


def main(argv: typing.Optional[typing.Sequence[str]] = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)
    if args.self_test:
        report = schema.self_test()
        print(_dump(report))
        return EXIT_OK if report["ok"] else EXIT_INTERNAL
    if not args.command:
        parser.print_usage(sys.stderr)
        return EXIT_USAGE
    try:
        document = _load(args.input)
        if args.command == "settle":
            result = settlement.settle(document)
            if result.get("valid") and result.get("envelope"):
                print(_dump(result["envelope"]))
            else:
                print(_dump(result))
            return _result_exit(result)
        if args.command == "routing":
            result = routing.validate_matrix(document)
            if args.workflow:
                workflow = routing.check_workflow(args.workflow)
                result = dict(result)
                result["workflow"] = workflow
                if not workflow.get("valid"):
                    result["valid"] = False
            print(_dump(result))
            return _result_exit(result)
        result = _dispatch(document)
        print(_dump(result))
        return _result_exit(result)
    except UsageError as error:
        print("invalid input: %s" % error, file=sys.stderr)
        return EXIT_USAGE
    except Exception:  # noqa: BLE001 - internal failure must never exit 0
        print("internal error", file=sys.stderr)
        traceback.print_exc(file=sys.stderr)
        return EXIT_INTERNAL


if __name__ == "__main__":
    sys.exit(main())
