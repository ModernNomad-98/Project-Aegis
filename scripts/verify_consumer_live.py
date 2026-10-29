#!/usr/bin/env python3
"""Compare the live consumer site's served bytes against a retained manifest.

Read-only by construction: the only I/O is one HTTP GET per required file (no
request body, no cookies, no deployment API) plus one read of the retained
manifest. Nothing is written, no temporary file is created, no output directory
is touched, so running this during an evidence review cannot change the
evidence it is reviewing.

WHAT IS COMPARED, AND WHY IN THIS ORDER

    1. The manifest's own shape. Its rows bind file name, byte count, LF count
       and SHA-256; a malformed manifest is refused before any fetch, because a
       check that reads a broken expectation can only produce a meaningless
       verdict.
    2. The row set. A required file with no row, and a row outside the required
       set, are findings rather than silent skips: the retained manifest is the
       expected file list, so a missing row would otherwise shrink the check.
    3. Per file bytes, LF count and SHA-256, reported separately. One blanket
       "content mismatch" cannot tell a reader that an editor normalised line
       endings (LF count and bytes both move) from one that rewrote a byte
       inside a line (SHA-256 moves alone).
    4. The serialized aggregate, computed over the SERVED rows rather than over
       the manifest's recorded rows. Both numbers from the aggregate comment are
       checked: serialized_bytes and sha256 against a fresh serialization of
       what the network returned. An aggregate copied from the manifest can only
       agree with the manifest.

THE DOCUMENTED SERIALIZATION RULE (mirrored, not invented)

Each row is: name, TAB, byte count, TAB, LF count, TAB, SHA-256, then one LF.
Rows are sorted by the file name's UTF-8 bytes. The aggregate is the SHA-256 of
that concatenation and its length is serialized_bytes. The producing side is
the consumer repository's Pages workflow (build mode writes the manifest,
deploy mode re-verifies it from the retained tree); this script reproduces the
rule so a third party can re-derive the retained aggregate from live bytes
alone, without trusting this repository's own records.

WHAT IS DELIBERATELY NOT DONE

    - No content policy is replayed. The producer's name and secret-pattern
      gates are its own defence; this script answers one question only: do the
      served bytes equal the retained ones?
    - No deployment, no cache purge, no repository write, no request with a
      body. A failed run changes nothing.

EXIT CODES, MOST SEVERE FIRST

    2  the manifest cannot be read or does not have the documented shape
    3  the transport failed (a URL could not be reached, or answered non-200
       and non-404) -- no verdict about content is possible
    1  the bytes disagree: a required file is missing on the server, or a
       per-file value, the row set, or the aggregate differs
    0  every required file and the aggregate match

Every finding prints one line, "FAIL <code>: <reason>", naming the file and both
values, so a mismatch is actionable without reading this script. Output order is
fixed (manifest findings, row-set findings, per-file findings in name order,
then the aggregate) and no timestamp or duration is printed, so two runs over
the same inputs produce identical stdout.

Usage (from the repository root; point --manifest at the release you retained):

    python scripts/verify_consumer_live.py \
        --manifest docs/evidence/releases/B/manifest.txt

    python scripts/verify_consumer_live.py \
        --base-url https://modernnomad-98.github.io/aegis-consumer-proof/ \
        --manifest docs/evidence/aep3-item2-consumer-proof-20261029/deployments/release-B-manifest.txt
"""
from __future__ import annotations

import argparse
import hashlib
import http.client
import os
import re
import sys
import urllib.error
import urllib.request

DEFAULT_BASE_URL = "https://modernnomad-98.github.io/aegis-consumer-proof/"
# The frozen allowlist the consumer workflow publishes. It doubles as the
# default required set, so an invocation with no --require checks the same three
# names the producing side binds.
FROZEN_ALLOWLIST = ("app.js", "index.html", "styles.css")
USER_AGENT = "aegis-verify-consumer-live/1 (read-only byte comparison)"
# Fixed rather than random: the query defeats a stale CDN object by changing the
# cache key, while a constant token keeps stdout identical between runs.
CACHE_BUST_TOKEN = "live-verify"

EXIT_OK = 0
EXIT_FINDING = 1
EXIT_MANIFEST = 2
EXIT_TRANSPORT = 3

AGGREGATE = re.compile(
    r"# aggregate rows=(\d+) serialized_bytes=(\d+) sha256=([0-9a-f]{64})")
SHA256_HEX = re.compile(r"[0-9a-f]{64}")
HTTP_SCHEME = re.compile(r"(?i)^https?://")


class ManifestError(Exception):
    """The retained manifest is unreadable or off-spec (exit 2)."""


class HttpOnlyRedirect(urllib.request.HTTPRedirectHandler):
    """Follow redirects only to http(s), never to a local file scheme."""

    def redirect_request(self, req, fp, code, msg, headers, newurl):
        if not HTTP_SCHEME.match(newurl):
            raise urllib.error.URLError(
                "refusing a non-http(s) redirect to " + repr(newurl))
        return super().redirect_request(req, fp, code, msg, headers, newurl)


OPENER = urllib.request.build_opener(HttpOnlyRedirect)


class Row:
    """One manifest data row, or one served file's measurements."""

    __slots__ = ("name", "nbytes", "nlf", "sha256")

    def __init__(self, name: str, nbytes: int, nlf: int, sha256: str) -> None:
        self.name = name
        self.nbytes = nbytes
        self.nlf = nlf
        self.sha256 = sha256

    def fields(self) -> tuple[str, int, int, str]:
        return (self.name, self.nbytes, self.nlf, self.sha256)


def name_key(name: str) -> bytes:
    return name.encode("utf-8")


def serialize(rows: list[Row]) -> bytes:
    """The documented serialization: sorted rows, TAB fields, one LF each."""
    ordered = sorted(rows, key=lambda row: name_key(row.name))
    return "".join(
        "%s\t%d\t%d\t%s\n" % row.fields() for row in ordered
    ).encode("utf-8")


def measure(name: str, data: bytes) -> Row:
    return Row(name, len(data), data.count(b"\n"), hashlib.sha256(data).hexdigest())


def parse_manifest(raw: bytes) -> tuple[list[Row], int, str]:
    """Return (rows, serialized_bytes, aggregate) or raise ManifestError.

    These rules mirror the producing workflow: no BOM, no CR, exactly one
    aggregate comment, four TAB-separated fields per row, decimal counts and
    lowercase hex. Order inside the file is not significant, so the rows are
    returned already sorted on the name's UTF-8 bytes exactly as the producer
    sorted them; serialize() sorts again, which makes it idempotent.
    """
    if raw.startswith(b"\xef\xbb\xbf"):
        raise ManifestError("manifest-bom: the manifest starts with a UTF-8 BOM")
    if b"\r" in raw:
        raise ManifestError("manifest-cr: the manifest contains a CR byte; LF only")
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ManifestError("manifest-encoding: not valid UTF-8: " + str(exc))
    lines = [line for line in text.splitlines() if line.strip()]
    data_lines = [line for line in lines if not line.startswith("#")]
    comment_lines = [line for line in lines if line.startswith("#")]
    if len(comment_lines) != 1:
        raise ManifestError(
            "manifest-comment-count: expected exactly 1 aggregate comment, found "
            + str(len(comment_lines)))
    match = AGGREGATE.fullmatch(comment_lines[0])
    if not match:
        raise ManifestError(
            "manifest-comment-format: malformed aggregate comment: "
            + repr(comment_lines[0]))
    agg_rows = int(match.group(1))
    agg_bytes = int(match.group(2))
    agg_sha = match.group(3)
    if agg_rows != len(data_lines):
        raise ManifestError(
            "manifest-row-count: the aggregate comment claims " + str(agg_rows)
            + " rows but the manifest carries " + str(len(data_lines)))
    rows: list[Row] = []
    seen: set[str] = set()
    for line in data_lines:
        fields = line.split("\t")
        if len(fields) != 4:
            raise ManifestError(
                "manifest-row-fields: a row must have 4 TAB-separated fields: "
                + repr(line))
        name, nbytes, nlf, sha = fields
        if not name:
            raise ManifestError("manifest-row-name: a row has an empty file name")
        if name in seen:
            raise ManifestError(
                "manifest-row-duplicate: the manifest lists " + repr(name) + " twice")
        seen.add(name)
        if not nbytes.isdigit() or not nlf.isdigit():
            raise ManifestError(
                "manifest-row-counts: bytes and LF must be decimal: " + repr(line))
        if not SHA256_HEX.fullmatch(sha):
            raise ManifestError(
                "manifest-row-sha: SHA-256 must be 64 lowercase hex characters: "
                + repr(line))
        rows.append(Row(name, int(nbytes), int(nlf), sha))
    rows.sort(key=lambda row: name_key(row.name))
    return rows, agg_bytes, agg_sha


def read_manifest(path: str) -> bytes:
    if os.path.islink(path):
        # A symlinked manifest re-points the binding while every downstream check
        # still passes, so the retained manifest must be a real file.
        raise ManifestError("manifest-symlink: the manifest path is a symlink: " + path)
    try:
        with open(path, "rb") as handle:
            return handle.read()
    except OSError as exc:
        raise ManifestError("manifest-unreadable: " + str(exc))


def file_url(base_url: str, name: str, cache_bust: bool) -> str:
    url = base_url.rstrip("/") + "/" + name
    if cache_bust:
        url += "?v=" + CACHE_BUST_TOKEN
    return url


def fetch(url: str, timeout: float) -> tuple[int, bytes]:
    """GET one file. Returns (status, body); raises on transport failure."""
    request = urllib.request.Request(
        url, headers={"User-Agent": USER_AGENT, "Cache-Control": "no-cache"})
    with OPENER.open(request, timeout=timeout) as response:
        return int(response.status), response.read()


def parse_require(values: list[str] | None) -> list[str]:
    if not values:
        return list(FROZEN_ALLOWLIST)
    names: list[str] = []
    for value in values:
        for part in value.split(","):
            part = part.strip()
            if part and part not in names:
                names.append(part)
    if not names:
        raise ValueError("--require selected no file names")
    return names


def per_file_findings(served: list[Row], recorded: dict[str, Row]) -> list[str]:
    findings: list[str] = []
    for row in sorted(served, key=lambda item: name_key(item.name)):
        expected = recorded.get(row.name)
        if expected is None:
            continue  # already reported as row-missing
        if row.nbytes != expected.nbytes:
            findings.append(
                "FAIL file-bytes: " + row.name + " served " + str(row.nbytes)
                + " B, the manifest records " + str(expected.nbytes) + " B ("
                + ("+" if row.nbytes > expected.nbytes else "")
                + str(row.nbytes - expected.nbytes) + ")")
        if row.nlf != expected.nlf:
            findings.append(
                "FAIL file-lf: " + row.name + " served " + str(row.nlf)
                + " LF, the manifest records " + str(expected.nlf) + " LF ("
                + ("+" if row.nlf > expected.nlf else "")
                + str(row.nlf - expected.nlf) + ")")
        if row.sha256 != expected.sha256:
            findings.append(
                "FAIL file-sha: " + row.name + " served sha256 " + row.sha256
                + ", the manifest records " + expected.sha256)
    return findings


def verify(base_url: str, manifest_path: str, required: list[str],
           timeout: float, cache_bust: bool) -> tuple[int, list[str]]:
    rows, agg_bytes, agg_sha = parse_manifest(read_manifest(manifest_path))
    recorded = {row.name: row for row in rows}
    # One sorted order for fetches, for the required-set echo and for findings,
    # so the report does not depend on the command line's argument order.
    required = sorted(set(required), key=name_key)

    findings: list[str] = []
    for name in required:
        if name not in recorded:
            findings.append(
                "FAIL row-missing: the manifest has no row for required file "
                + repr(name) + " (required set: " + ", ".join(required) + ")")
    for name in sorted(recorded, key=name_key):
        if name not in required:
            findings.append(
                "FAIL row-extra: the manifest records a row for " + repr(name)
                + ", which is outside the required set ("
                + ", ".join(required) + ")")

    transport: list[str] = []
    served: list[Row] = []
    for name in required:
        url = file_url(base_url, name, cache_bust)
        try:
            status, data = fetch(url, timeout)
        except urllib.error.HTTPError as exc:
            if exc.code == 404:
                findings.append(
                    "FAIL served-missing: " + name
                    + " is not served (HTTP 404) at " + url)
            else:
                transport.append(
                    "FAIL transport: " + url + " answered HTTP " + str(exc.code))
            continue
        except (urllib.error.URLError, http.client.HTTPException, OSError) as exc:
            transport.append(
                "FAIL transport: " + url + " is unreachable: "
                + str(getattr(exc, "reason", exc)))
            continue
        if status != 200:
            transport.append(
                "FAIL transport: " + url + " answered HTTP " + str(status))
            continue
        served.append(measure(name, data))

    findings.extend(per_file_findings(served, recorded))
    if transport:
        # A partial fetch cannot produce a content verdict, so the aggregate is
        # never compared and the transport class wins.
        return EXIT_TRANSPORT, findings + transport
    if {row.name for row in served} != set(required):
        # A required file is missing from the server, so no serialization of
        # what was fetched could stand in for the published one.
        return EXIT_FINDING, findings

    # Compared even when a per-file finding already exists: one run should
    # produce the whole diagnosis, and the aggregate is an independent check of
    # the serialization rather than a restatement of the per-file values.
    serialized = serialize(served)
    actual_sha = hashlib.sha256(serialized).hexdigest()
    if len(serialized) != agg_bytes:
        findings.append(
            "FAIL aggregate-bytes: the served rows serialize to "
            + str(len(serialized)) + " B, the manifest records "
            + str(agg_bytes) + " B")
    if actual_sha != agg_sha:
        findings.append(
            "FAIL aggregate-sha: the served rows aggregate to " + actual_sha
            + ", the manifest records " + agg_sha)
    if findings:
        return EXIT_FINDING, findings
    return EXIT_OK, served_report(base_url, manifest_path, served, serialized,
                                  actual_sha)


def served_report(base_url: str, manifest_path: str, served: list[Row],
                  serialized: bytes, aggregate: str) -> list[str]:
    """The deterministic success report: same inputs, same lines, no clock."""
    lines = [
        "OK: " + base_url.rstrip("/") + "/ matches " + manifest_path,
        "files=" + str(len(served))
        + " serialized_bytes=" + str(len(serialized))
        + " aggregate=" + aggregate,
    ]
    for row in sorted(served, key=lambda item: name_key(item.name)):
        lines.append("  " + row.name + "\t" + str(row.nbytes) + " B\t"
                     + str(row.nlf) + " LF\t" + row.sha256)
    return lines


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Compare live consumer-site bytes against a retained "
                    "release manifest. Read-only: GET only, writes nothing.")
    parser.add_argument(
        "--base-url", default=DEFAULT_BASE_URL,
        help="public base URL that serves the files (default: %(default)s)")
    parser.add_argument(
        "--manifest", required=True,
        help="retained manifest, e.g. docs/evidence/releases/B/manifest.txt")
    parser.add_argument(
        "--require", action="append", default=None, metavar="NAME",
        help="required file name or names, comma-separated; repeatable "
             "(default: " + ", ".join(FROZEN_ALLOWLIST) + ")")
    parser.add_argument(
        "--timeout", type=float, default=20.0, metavar="SECONDS",
        help="per-request timeout (default: %(default)s)")
    parser.add_argument(
        "--no-cache-bust", action="store_true",
        help="request the bare URL without the cache-busting query")
    args = parser.parse_args(argv)

    if not HTTP_SCHEME.match(args.base_url):
        print("ERROR usage: --base-url must be an http(s) URL, got "
              + repr(args.base_url))
        return EXIT_MANIFEST
    try:
        required = parse_require(args.require)
    except ValueError as exc:
        print("ERROR usage: " + str(exc))
        return EXIT_MANIFEST
    if args.timeout <= 0:
        print("ERROR usage: --timeout must be positive")
        return EXIT_MANIFEST

    try:
        code, lines = verify(args.base_url, args.manifest, required,
                             args.timeout, not args.no_cache_bust)
    except ManifestError as exc:
        print("ERROR " + str(exc))
        return EXIT_MANIFEST
    for line in lines:
        print(line)
    if code != EXIT_OK:
        failed = len([line for line in lines if line.startswith("FAIL")])
        print("MISMATCH: " + str(failed)
              + " finding(s); the served bytes do not match the retained manifest.")
    return code


if __name__ == "__main__":
    sys.exit(main())
