"""Read-only CLI for the C2.2 preflight (aegis.preflight/v1).

Usage (from the repository root):

    python -m tools.aegis_preflight --self-test
    python -m tools.aegis_preflight check --bundle bundle.json [--repo-root .] \
        [--json] [--fixture-mode [--supported-auth-method NAME]...]

Exit codes:
    0  all ten checks PASS
    1  any check FAIL/BLOCKED/UNRUN (fail closed)
    2  invalid input / usage / parse failure
    3  internal error (never 0)

The CLI writes nothing, calls no network, and runs no command other than the
two allowlisted read-only tools (the merged C1.1a checker in PF-07 and the
C2.3 reuse validator in PF-08).  Exit 0 means "mechanical checks passed"; it
is not approval, readiness or merge permission.
"""

from __future__ import annotations

import argparse
import json
import sys
import traceback
import typing
from pathlib import Path

from . import checks, models

EXIT_PASS = 0
EXIT_BLOCKED = 1
EXIT_USAGE = 2
EXIT_INTERNAL = 3


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="python -m tools.aegis_preflight",
        description=(
            "Read-only preflight over supplied governance records: composes the merged "
            "C1.1a checker and the C2.3 reuse validator, and adds completeness, "
            "arithmetic, staleness, reference and status checks. Auditable tooling, "
            "not enforcement."
        ),
    )
    parser.add_argument("command", nargs="?", choices=("check",), default="check")
    parser.add_argument("--bundle")
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--fixture-mode", action="store_true")
    parser.add_argument("--supported-auth-method", action="append", default=[])
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--self-test", action="store_true")
    return parser


def _dump(result: typing.Mapping[str, object]) -> str:
    return json.dumps(result, sort_keys=True, indent=2, ensure_ascii=False)


def _summary(output: typing.Mapping[str, object]) -> str:
    lines = [
        "aegis.preflight/v1 - mechanical preflight",
        "assurance: %s (mounted coverage %s; mode %s)"
        % (
            output["assurance"]["claim"],
            output["assurance"]["mounted_coverage"],
            output["assurance"]["mode"],
        ),
    ]
    for check in output["checks"]:
        lines.append("%s %s %s - %s" % (check["check_id"], check["status"], check["reason_code"], check["message"]))
    totals = output["totals"]
    lines.append(
        "totals: pass=%d fail=%d blocked=%d unrun=%d"
        % (totals["pass"], totals["fail"], totals["blocked"], totals["unrun"])
    )
    lines.append("exit_code: %d (0 means mechanical checks passed, not approval or readiness)" % output["exit_code"])
    return "\n".join(lines)


def _self_test() -> int:
    report = checks.self_test()
    print(_dump(report))
    return EXIT_PASS if report["ok"] else EXIT_INTERNAL


def main(argv: typing.Optional[typing.Sequence[str]] = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)
    if args.self_test:
        return _self_test()
    if args.supported_auth_method and not args.fixture_mode:
        parser.error("--supported-auth-method requires --fixture-mode")
    if not args.bundle:
        parser.error("check requires --bundle")
    try:
        bundle = models.load_bundle(Path(args.bundle))
    except models.ModelError as error:
        print("invalid input: %s" % error, file=sys.stderr)
        return EXIT_USAGE
    try:
        results = checks.run_all(
            bundle,
            Path(args.repo_root),
            fixture_mode=args.fixture_mode,
            supported_auth_methods=tuple(args.supported_auth_method),
        )
        output = models.build_output(
            bundle.document.get("subject"),
            results,
            args.fixture_mode,
        )
    except Exception:  # noqa: BLE001 - internal failures must never exit 0
        print("internal error", file=sys.stderr)
        traceback.print_exc(file=sys.stderr)
        return EXIT_INTERNAL
    print(_dump(output) if args.json else _summary(output))
    return int(output["exit_code"])


if __name__ == "__main__":
    sys.exit(main())
