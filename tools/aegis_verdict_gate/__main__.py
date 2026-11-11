"""Read-only CLI for the aegis.verdict-bound/v2.1 verdict/readiness checker.

Usage (from the repository root):

    python -m tools.aegis_verdict_gate --self-test
    python -m tools.aegis_verdict_gate check --repo-root . \
        --verdict verdict.json --head-history history.json \
        --freeze freeze.json --settlement settlement.json \
        --stage-records-dir stage-records [--candidate-head HEX40] [--json]
        [--fixture-mode [--supported-auth-method NAME]]

A supported authentication method is a fixture-only affordance: it is refused
unless --fixture-mode is also given, and readiness is reported in
assurance.mode = "FIXTURE".  A production run (no --fixture-mode) has no
supported method while owner decision T6 is undecided, so it has no path to
readiness=true.

Exit codes:
    0  readiness true (reachable only in --fixture-mode; a production run has
       no supported authentication method while owner decision T6 is undecided)
    1  not ready / blocked, including UNVERIFIED auth and
       REQUIRED_INPUT_UNAVAILABLE
    2  invalid input / usage / parse failure (fail closed)
    3  internal error (never 0)

The CLI never writes, never approves and never claims enforcement.  Output is
deterministic JSON with sorted keys, no timestamps and no environment values.
"""

from __future__ import annotations

import argparse
import json
import sys
import traceback
import typing
from pathlib import Path

from . import canonical, gate, inputs

EXIT_READY = 0
EXIT_BLOCKED = 1
EXIT_USAGE = 2
EXIT_INTERNAL = 3


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="python -m tools.aegis_verdict_gate",
        description=(
            "Read-only fail-closed checker for aegis.verdict-bound/v2.1 verdicts and "
            "readiness. Auditable tooling, not enforcement."
        ),
    )
    parser.add_argument("command", nargs="?", choices=("check", "validate"), default="check")
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--records-dir", default="docs/approvals/revision-state")
    parser.add_argument("--verdict")
    parser.add_argument("--head-history")
    parser.add_argument("--freeze")
    parser.add_argument("--settlement")
    parser.add_argument("--stage-records-dir")
    parser.add_argument("--candidate-head")
    parser.add_argument("--base-ref", default="origin/main")
    parser.add_argument("--supported-auth-method", action="append", default=[])
    parser.add_argument(
        "--fixture-mode",
        action="store_true",
        help=(
            "run against synthetic fixtures only: permits --supported-auth-method and marks "
            "assurance.mode=FIXTURE; never valid for a production readiness claim"
        ),
    )
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--json", action="store_true")
    return parser


def _dump(result: typing.Mapping[str, object]) -> str:
    return json.dumps(result, sort_keys=True, indent=2, ensure_ascii=False)


def _self_test() -> int:
    report = canonical.self_test()
    print(_dump(report))
    return EXIT_READY if report["ok"] else EXIT_INTERNAL


def _summary(result: gate.GateResult) -> str:
    lines = [
        "aegis.verdict-bound/v2.1 readiness check",
        "readiness: %s" % ("true" if result.readiness else "false"),
        "assurance: %s (mounted coverage %s; mode %s)"
        % (
            result.assurance["claim"],
            result.assurance["mounted_coverage"],
            result.assurance["mode"],
        ),
    ]
    if result.blockers:
        lines.append("blockers:")
        for blocker in result.blockers:
            lines.append("  - %s [%s] %s" % (blocker.code, blocker.classification, blocker.detail))
    for check in result.checks:
        lines.append("  %s %s%s" % (check["check"], check["status"], (" " + ",".join(check["codes"])) if check["codes"] else ""))
    lines.append(
        "next action: %s (%s)"
        % (result.permitted_next_action["action"], result.permitted_next_action["actor_role"])
    )
    lines.append("revision_state_sha256: %s" % result.revision_state_sha256)
    lines.append("store_digest: %s" % result.store_digest)
    lines.append("not verifiable: " + "; ".join(result.not_verifiable))
    return "\n".join(lines)


def main(argv: typing.Optional[typing.Sequence[str]] = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)
    if args.self_test:
        return _self_test()
    missing = [
        name
        for name, value in (
            ("--verdict", args.verdict),
            ("--head-history", args.head_history),
            ("--freeze", args.freeze),
            ("--settlement", args.settlement),
            ("--stage-records-dir", args.stage_records_dir),
        )
        if not value
    ]
    if missing:
        parser.error("check requires %s" % ", ".join(missing))
    if args.supported_auth_method and not args.fixture_mode:
        parser.error(
            "--supported-auth-method requires --fixture-mode: no supported authentication method "
            "exists while owner decision T6 is undecided, so production has no path to readiness"
        )
    try:
        result = gate.evaluate(
            repo_root=Path(args.repo_root),
            verdict_path=args.verdict,
            freeze_path=args.freeze,
            settlement_path=args.settlement,
            head_history_path=args.head_history,
            stage_records_dir=args.stage_records_dir,
            records_dir=args.records_dir,
            candidate_head=args.candidate_head,
            supported_auth_methods=tuple(args.supported_auth_method),
            base_ref=args.base_ref,
            fixture_mode=args.fixture_mode,
        )
    except inputs.InputError as error:
        print("invalid input: %s" % error.detail, file=sys.stderr)
        print(_dump({"error": error.detail, "code": error.code}), file=sys.stderr)
        return EXIT_USAGE if error.fatal else EXIT_BLOCKED
    except Exception:  # noqa: BLE001 - internal failure must never exit 0
        print("internal error", file=sys.stderr)
        traceback.print_exc(file=sys.stderr)
        return EXIT_INTERNAL
    if args.json:
        print(_dump(result.as_dict()))
    else:
        print(_summary(result))
    return EXIT_READY if result.readiness else EXIT_BLOCKED


if __name__ == "__main__":
    sys.exit(main())
