"""CLI for the Aegis distributed-payload manifest and read-only verifier.

Only three verbs exist: build, verify, check-manifest. There is intentionally no
install, repair, upgrade, uninstall, prune, cleanup or approve verb, and verify
never mutates its target.

Exit codes:
  build:          0 success, 2 usage/invalid input, 3 internal error
  verify:         0 clean, 1 findings, 2 usage/invalid/unsafe input, 3 internal error
  check-manifest: 0 valid identity, 2 usage/invalid, 3 internal error
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

from . import manifest as manifest_module
from . import verify as verify_module


def _build(args: argparse.Namespace) -> int:
    raw_root = Path(args.root)
    if raw_root.is_symlink() or (callable(getattr(os.path, "isjunction", None))
                                and os.path.isjunction(raw_root)):
        raise manifest_module.ManifestError(
            "reparse_point", "symlinked/junction payload root is not supported")
    out_path = Path(args.out).resolve()
    payload_root = raw_root.resolve()
    try:
        out_path.relative_to(payload_root)
    except ValueError:
        pass
    else:
        raise manifest_module.ManifestError(
            "out_inside_payload", "manifest output must be outside the payload root")
    source = manifest_module.load_source_identity(Path(args.source))
    document = manifest_module.build_manifest(
        Path(args.root), args.package_id, args.package_version, source, label=args.label)
    manifest_module.write_manifest_atomic(document, out_path)
    print(json.dumps({"schema": document["schema"], "out": str(args.out),
                      "entries": len(document["entries"])}, sort_keys=True))
    return 0


def _verify(args: argparse.Namespace) -> int:
    report, exit_code = verify_module.verify_target(
        Path(args.manifest), Path(args.target),
        report_out=Path(args.report_out) if args.report_out else None)
    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        print(f"verify: {report['summary']['entries']} entries, "
              f"{report['summary']['findings']} finding(s), "
              f"ok={report['summary']['ok']}, absent={report['summary']['absent']}, "
              f"changed={report['summary']['changed']}, "
              f"changed_type={report['summary']['changed_type']}, "
              f"unrecognized={report['summary']['unrecognized']}")
        for finding in report["findings"]:
            print(f"  {finding['class']}: {finding['path']}")
        if report["host_limitations"]:
            for limitation in report["host_limitations"]:
                print(f"  host-limitation: {limitation}")
        print("repair: none (read-only verifier; findings are never repaired)")
    return exit_code


def _check_manifest(args: argparse.Namespace) -> int:
    identity = verify_module.check_manifest(Path(args.manifest))
    print(json.dumps(identity, indent=2, sort_keys=True))
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="python -m tools.distributed_payload",
        description="Distributed-payload manifest builder and read-only verifier (stdlib only).")
    subparsers = parser.add_subparsers(dest="verb", required=True)

    build_parser = subparsers.add_parser("build", help="build a manifest from a payload tree")
    build_parser.add_argument("--root", required=True, help="payload root directory")
    build_parser.add_argument("--package-id", required=True, help="package profile id")
    build_parser.add_argument("--package-version", required=True, help="package profile version")
    build_parser.add_argument("--source", required=True,
                              help="source identity JSON file (repository, commit, tree[, note])")
    build_parser.add_argument("--out", required=True, help="manifest output path (outside the payload root)")
    build_parser.add_argument("--label", default=None, help="optional human-readable label")
    build_parser.set_defaults(handler=_build)

    verify_parser = subparsers.add_parser("verify", help="read-only verification of a target tree")
    verify_parser.add_argument("--manifest", required=True, help="manifest file")
    verify_parser.add_argument("--target", required=True, help="target root to verify read-only")
    verify_parser.add_argument("--report-out", default=None,
                               help="optional JSON report path outside the target and package dirs")
    verify_parser.add_argument("--json", action="store_true", help="print the full JSON report")
    verify_parser.set_defaults(handler=_verify)

    check_parser = subparsers.add_parser("check-manifest",
                                         help="validate a manifest and print its detached identity")
    check_parser.add_argument("--manifest", required=True, help="manifest file")
    check_parser.set_defaults(handler=_check_manifest)
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return int(args.handler(args))
    except manifest_module.ManifestError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return verify_module.EXIT_USAGE
    except OSError as exc:
        print(f"ERROR: {type(exc).__name__}: {exc}", file=sys.stderr)
        return verify_module.EXIT_USAGE
    except Exception as exc:  # internal error is never reported as a finding or a pass
        print(f"INTERNAL ERROR: {type(exc).__name__}: {exc}", file=sys.stderr)
        return verify_module.EXIT_INTERNAL


if __name__ == "__main__":
    sys.exit(main())