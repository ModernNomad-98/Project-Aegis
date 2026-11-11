#!/usr/bin/env python3
"""Read-only provider adapter for the C1.1b aegis-verdict-gate workflow.

The adapter answers one question: given the event payload and read-only GitHub
REST data, which C1.1a input envelopes can be written for the evaluated pull
request without executing any pull-request code and without inventing a value?

It never decides readiness.  The moved checker (scripts/aegis_verdict_gate/run.py)
is the only decision-maker; the adapter only assembles the checker's documented
input envelopes and records what it could not source.  The publisher
(scripts/ci/aegis_verdict_gate_publish.py) is the only write path.

Contract (C1.1b Stage A plan REV2 sections 5.2/6, authority REV6):
  * Inputs: GITHUB_TOKEN, GITHUB_REPOSITORY, GITHUB_API_URL, GITHUB_EVENT_NAME,
    GITHUB_EVENT_PATH, GITHUB_RUN_ID, RUNNER_TEMP, AEGIS_VERDICT_RUN_DIR,
    AEGIS_VERDICT_CHECKOUT_SHA.  The token is read from the environment only:
    it is never a command-line argument, never written to disk, never printed
    and never placed in a URL.
  * Outputs (under AEGIS_VERDICT_RUN_DIR, which must be under RUNNER_TEMP):
    gate-context.json, verdict.json, freeze.json, settlement.json,
    head-history.json, stage-records/ (empty unless a stage declaration can be
    sourced), provenance-manifest.json and adapter-result.json.
  * Every written envelope is re-read with the moved package's own
    inputs.load_envelope validator (M4); no second envelope or canonical
    definition is defined here.
  * The adapter fails closed with a stable exit code on every provider,
    identity, base or head failure.  A pre-F pull request is not an adapter
    failure: the envelopes are written with no verdict and the checker blocks.

Field-source policy (plan section 6).  A value is written only when it is read
from a provider object or base-tree record, or computed by the moved package's
own derivation.  The repository has no captured plan annex pinning the mapping
for candidate_id, policy/plan identity, triage rows, skills/security/witness or
stage-record declarations, so those required fields are deliberately omitted
and listed in adapter-result.json "unavailable".  Omitting a required input is
fail-closed (the checker reports REQUIRED_INPUT_UNAVAILABLE or the specific
canonical blocker); fabricating one is not permitted.  The head-history export
is always UNVERIFIED: the read-only provider endpoints cannot establish a
complete, attributable published-head sequence, so the adapter never guesses
"used=0" (plan section 6, D2).

Exit codes (stable; recorded in adapter-result.json):
    0  context/envelopes written; the gate outcome is the checker's
    2  usage error, malformed event payload or unsupported event
    3  internal error (never a success)
    4  provider unavailable/denied/unexpected/oversized/truncated/timeout
    5  foreign repository, not a pull request in this repository, or PR closed
    6  base mismatch (stale base or checkout drift)
    7  token absent or provider authentication denied (401/403)
    8  head moved between resolve and fetch

No network is used when a transport object is injected (the tests inject a
mocked transport); no pull-request code is read or executed.
"""

from __future__ import annotations

import argparse
import datetime
import json
import os
import re
import subprocess
import sys
import typing
import urllib.error as urlerror
import urllib.request as urlrequest
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parents[1]
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from aegis_verdict_gate import canonical, catalogue, inputs, records  # noqa: E402

SCHEMA_CONTEXT = "aegis.verdict-gate-context/v1"
SCHEMA_RESULT = "aegis.verdict-gate-adapter-result/v1"
SCHEMA_PROVENANCE = "aegis.verdict-gate-provenance/v1"

EXIT_OK = 0
EXIT_USAGE = 2
EXIT_INTERNAL = 3
EXIT_PROVIDER = 4
EXIT_FOREIGN = 5
EXIT_BASE_MISMATCH = 6
EXIT_AUTH = 7
EXIT_HEAD_MOVED = 8

MAX_EVENT_BYTES = 5 * 1024 * 1024
MAX_BODY_BYTES = 2 * 1024 * 1024
MAX_PAGES = 10
REQUEST_TIMEOUT = 20
RUN_DIR_NAME = "aegis-verdict-gate"
RECORDS_DIR = "docs/approvals/revision-state"
DEFAULT_BASE_REF = "origin/main"

HEX40 = re.compile(r"^[0-9a-f]{40}$")
HEX40_IN_TEXT = re.compile(r"(?<![0-9A-Za-z])([0-9a-f]{40})(?![0-9A-Za-z])")
VERDICT_TOKEN = re.compile(r"(?<![A-Za-z])(PASS|REVISE|BLOCKED|FAIL)(?![A-Za-z])")
# An explicit disposition line, for a comment whose first line names the head
# but not the value.  Prose mentions are deliberately not accepted.
DISPOSITION_LINE = re.compile(
    r"^\s*(?:SD-F\s*)?(?:F\s+)?(?:VERDICT|DISPOSITION)\s*[:\u2014-]?\s*(PASS|REVISE|BLOCKED|FAIL)\s*$"
)
APR_ID = re.compile(r"\b(AEGIS-APR-[0-9]{3,4})\b")

# The fields the adapter deliberately does not populate (see the module
# docstring).  Kept as data so the result, the tests and the PR body agree.
UNAVAILABLE_FIELDS: typing.Dict[str, str] = {
    "candidate_id": "VB-A07 is an owner-assigned identifier; no provider or base-tree source exposes it",
    "conditionals_applied": "VB-A12 records contract conditional applications; no provider source",
    "policy_ref/policy_sha256": "the policy-of-record identity is not exposed by the provider or a pinned PR-body field",
    "plan.sha256/plan.basis_ref": "the audited plan revision is free-form in the PR body; no pinned machine field",
    "review_heads": "head-history is UNVERIFIED; the read-only API cannot establish a complete published-head sequence",
    "evidence_inputs_sha256": "the F verdict's evidence set has no pinned machine-readable form",
    "stage_records": "the B/D/E record declarations have no pinned machine-readable form in the F verdict or PR body",
    "triage": "the PR template has no canonical triage table; a parse failure must not become open_blocking=0",
    "skills/security/witness": "the PR-body bound fields are free-form tables; no pinned mapping to the checker's shapes",
    "post_f_state": "the post-F state is an owner record; the provider does not expose it",
    "merge_authority_ref": "no provider or base-tree source",
    "bound_fields_sha256": "VB-I01 is the verdict author's bound hash; the adapter must not self-certify it",
}


class AdapterError(Exception):
    """A fail-closed adapter condition with a stable exit code."""

    def __init__(self, exit_code: int, detail: str) -> None:
        super().__init__(detail)
        self.exit_code = exit_code
        self.detail = detail


class TransportError(Exception):
    """A transport failure; the message never contains headers or a token."""


class Response(typing.NamedTuple):
    status: int
    headers: typing.Mapping[str, str]
    body: bytes


class Transport(typing.Protocol):
    def get(self, url: str, headers: typing.Mapping[str, str]) -> Response:
        ...


class UrllibTransport:
    """Minimal read-only HTTP transport (standard library only)."""

    def get(self, url: str, headers: typing.Mapping[str, str]) -> Response:
        request = urlrequest.Request(url, headers=dict(headers), method="GET")
        try:
            with urlrequest.urlopen(request, timeout=REQUEST_TIMEOUT) as response:
                body = response.read(MAX_BODY_BYTES + 1)
                if len(body) > MAX_BODY_BYTES:
                    raise TransportError("response exceeds the %d-byte bound" % MAX_BODY_BYTES)
                return Response(int(response.status), dict(response.headers), body)
        except urlerror.HTTPError as error:
            try:
                body = error.read(MAX_BODY_BYTES + 1)[:MAX_BODY_BYTES]
            except OSError:
                body = b""
            return Response(int(error.code), dict(error.headers or {}), body)
        except (urlerror.URLError, TimeoutError, OSError) as error:
            # Name the failure class only: URLs and headers never reach a log.
            raise TransportError("request failed: %s" % type(error).__name__) from None


def _redact(text: str, token: str) -> str:
    return text.replace(token, "[REDACTED]") if token else text


def _next_link(headers: typing.Mapping[str, str]) -> typing.Optional[str]:
    value = None
    for key, header_value in headers.items():
        if key.lower() == "link":
            value = header_value
            break
    if not value:
        return None
    for part in value.split(","):
        piece = part.strip()
        if 'rel="next"' not in piece:
            continue
        start, end = piece.find("<"), piece.find(">")
        if start != -1 and end > start:
            return piece[start + 1 : end]
    return None


def _parse_time(value: object) -> typing.Optional[datetime.datetime]:
    if not isinstance(value, str) or not value.strip():
        return None
    text = value.strip()
    if text.endswith("Z"):
        text = text[:-1] + "+00:00"
    try:
        parsed = datetime.datetime.fromisoformat(text)
    except ValueError:
        return None
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=datetime.timezone.utc)
    return parsed


class GitHubClient:
    """Read-only GitHub REST client with bounded parsing and no token logging."""

    def __init__(self, transport: Transport, *, api_url: str, token: str) -> None:
        self._transport = transport
        self._api_url = api_url.rstrip("/")
        self._token = token
        self.calls = 0

    def _headers(self) -> typing.Dict[str, str]:
        return {
            "Accept": "application/vnd.github+json",
            "Authorization": "Bearer " + self._token,
            "X-GitHub-Api-Version": "2022-11-28",
            "User-Agent": "aegis-verdict-gate-fetch",
        }

    def _get(self, url: str, what: str) -> Response:
        self.calls += 1
        try:
            response = self._transport.get(url, self._headers())
        except TransportError as error:
            raise AdapterError(EXIT_PROVIDER, "%s: %s" % (what, error)) from None
        if response.status in (401, 403):
            raise AdapterError(
                EXIT_AUTH, "%s: provider denied the request (HTTP %d)" % (what, response.status)
            )
        if response.status == 404:
            raise AdapterError(EXIT_PROVIDER, "%s: provider has no such resource (HTTP 404)" % what)
        if response.status == 429:
            raise AdapterError(EXIT_PROVIDER, "%s: provider rate limit (HTTP 429)" % what)
        if response.status >= 500:
            raise AdapterError(EXIT_PROVIDER, "%s: provider error (HTTP %d)" % (what, response.status))
        if response.status != 200:
            raise AdapterError(EXIT_PROVIDER, "%s: unexpected provider status %d" % (what, response.status))
        if len(response.body) > MAX_BODY_BYTES:
            raise AdapterError(EXIT_PROVIDER, "%s: response exceeds the %d-byte bound" % (what, MAX_BODY_BYTES))
        return response

    def _json(self, url: str, what: str) -> typing.Tuple[object, typing.Mapping[str, str]]:
        response = self._get(url, what)
        try:
            document = json.loads(response.body.decode("utf-8"))
        except (UnicodeDecodeError, ValueError):
            raise AdapterError(EXIT_PROVIDER, "%s: response is not UTF-8 JSON" % what) from None
        return document, response.headers

    def get_object(self, path: str, what: str) -> typing.Dict[str, object]:
        document, _ = self._json(self._api_url + path, what)
        if not isinstance(document, dict):
            raise AdapterError(EXIT_PROVIDER, "%s: response is not a JSON object" % what)
        return typing.cast(typing.Dict[str, object], document)

    def get_array(self, path: str, what: str) -> typing.List[typing.Dict[str, object]]:
        """Fetch a complete array; any truncation or non-array is fail-closed."""

        url = self._api_url + path
        collected: typing.List[typing.Dict[str, object]] = []
        for _ in range(MAX_PAGES):
            document, headers = self._json(url, what)
            if not isinstance(document, list):
                raise AdapterError(EXIT_PROVIDER, "%s: response is not a JSON array" % what)
            for entry in document:
                if not isinstance(entry, dict):
                    raise AdapterError(EXIT_PROVIDER, "%s: array entry is not an object" % what)
                collected.append(typing.cast(typing.Dict[str, object], entry))
            next_url = _next_link(headers)
            if next_url is None:
                return collected
            if not next_url.startswith(self._api_url + "/"):
                raise AdapterError(EXIT_PROVIDER, "%s: pagination link escapes the API" % what)
            url = next_url
        raise AdapterError(
            EXIT_PROVIDER, "%s: pagination exceeded %d pages; the history is not complete" % (what, MAX_PAGES)
        )


# ---------------------------------------------------------------------------
# Event and pull-request resolution
# ---------------------------------------------------------------------------


class Event(typing.NamedTuple):
    event_name: str
    action: str
    decision: str
    reason: str
    repo: str
    pr_number: typing.Optional[int]
    head_sha: typing.Optional[str]
    base_sha: typing.Optional[str]
    base_ref: typing.Optional[str]
    head_ref: typing.Optional[str]
    head_repo: typing.Optional[str]


def _repo_full_name(document: object) -> typing.Optional[str]:
    if not isinstance(document, dict):
        return None
    full = document.get("full_name")
    if isinstance(full, str) and full:
        return full
    owner = document.get("owner")
    name = document.get("name")
    if isinstance(owner, dict) and isinstance(owner.get("login"), str) and isinstance(name, str):
        return "%s/%s" % (owner["login"], name)
    return None


def resolve_event(
    event_name: str, payload: typing.Mapping[str, object], github_repository: str
) -> Event:
    if event_name not in ("pull_request_target", "issue_comment"):
        raise AdapterError(EXIT_USAGE, "unsupported event %r" % (event_name,))
    repository = payload.get("repository")
    full_name = _repo_full_name(repository)
    if full_name is None or full_name.lower() != github_repository.lower():
        raise AdapterError(
            EXIT_FOREIGN,
            "the event repository is not the workflow repository (foreign repository refused)",
        )
    action = payload.get("action") if isinstance(payload.get("action"), str) else ""
    if event_name == "pull_request_target":
        pull_request = payload.get("pull_request")
        number = payload.get("number")
        if not isinstance(pull_request, dict) or not isinstance(number, int):
            raise AdapterError(EXIT_USAGE, "pull_request_target payload has no pull_request/number")
        head = pull_request.get("head") if isinstance(pull_request.get("head"), dict) else {}
        base = pull_request.get("base") if isinstance(pull_request.get("base"), dict) else {}
        head_sha = head.get("sha") if isinstance(head.get("sha"), str) else None
        base_sha = base.get("sha") if isinstance(base.get("sha"), str) else None
        base_ref = base.get("ref") if isinstance(base.get("ref"), str) else None
        if not (head_sha and HEX40.match(head_sha) and base_sha and HEX40.match(base_sha) and base_ref):
            raise AdapterError(EXIT_USAGE, "pull_request_target payload has no usable head/base identity")
        if pull_request.get("state") != "open":
            return Event(
                event_name, action, "no-op", "the pull request is not open", full_name, number,
                head_sha, base_sha, base_ref,
                head.get("ref") if isinstance(head.get("ref"), str) else None,
                _repo_full_name(head.get("repo")),
            )
        return Event(
            event_name, action, "evaluate", "", full_name, number, head_sha, base_sha, base_ref,
            head.get("ref") if isinstance(head.get("ref"), str) else None,
            _repo_full_name(head.get("repo")),
        )
    issue = payload.get("issue")
    if not isinstance(issue, dict):
        raise AdapterError(EXIT_USAGE, "issue_comment payload has no issue object")
    if not isinstance(issue.get("pull_request"), dict):
        return Event(
            event_name, action, "no-op", "the issue is not a pull request", full_name,
            issue.get("number") if isinstance(issue.get("number"), int) else None,
            None, None, None, None, None,
        )
    number = issue.get("number")
    if not isinstance(number, int):
        raise AdapterError(EXIT_USAGE, "issue_comment payload has no issue number")
    return Event(event_name, action, "evaluate", "", full_name, number, None, None, None, None, None)


def _require_pr(document: typing.Mapping[str, object], repo: str, number: int) -> None:
    pr_number = document.get("number")
    if not isinstance(pr_number, int) or pr_number != number:
        raise AdapterError(EXIT_FOREIGN, "the provider returned a different pull request")
    base = document.get("base") if isinstance(document.get("base"), dict) else {}
    base_repo = _repo_full_name(base.get("repo")) if isinstance(base.get("repo"), dict) else None
    if base_repo is None or base_repo.lower() != repo.lower():
        raise AdapterError(EXIT_FOREIGN, "the pull request base repository is not this repository")
    head = document.get("head") if isinstance(document.get("head"), dict) else {}
    if not isinstance(head.get("sha"), str) or not HEX40.match(head["sha"]):
        raise AdapterError(EXIT_PROVIDER, "the pull request has no usable head sha")
    if not isinstance(base.get("sha"), str) or not HEX40.match(base["sha"]):
        raise AdapterError(EXIT_PROVIDER, "the pull request has no usable base sha")
    if not isinstance(base.get("ref"), str) or not base["ref"]:
        raise AdapterError(EXIT_PROVIDER, "the pull request has no usable base ref")


def _git_head(repo_root: Path) -> str:
    try:
        completed = subprocess.run(
            ["git", "-C", str(repo_root), "rev-parse", "HEAD"],
            capture_output=True,
            check=False,
            timeout=30,
        )
    except (OSError, subprocess.SubprocessError):
        raise AdapterError(EXIT_INTERNAL, "cannot read the checked-out commit") from None
    if completed.returncode != 0:
        raise AdapterError(EXIT_INTERNAL, "cannot read the checked-out commit")
    head = completed.stdout.decode("ascii", "replace").strip()
    if not HEX40.match(head):
        raise AdapterError(EXIT_INTERNAL, "the checked-out commit is not a 40-character sha")
    return head


def _checksum_bytes(raw: bytes) -> str:
    return canonical.sha256_hex(raw)


# ---------------------------------------------------------------------------
# Verdict-record extraction (provider data only)
# ---------------------------------------------------------------------------


class VerdictComment(typing.NamedTuple):
    comment_id: int
    body: str
    created_at: str
    updated_at: str
    author: typing.Optional[str]
    html_url: str
    head_sha: str
    value: str
    deleted: bool
    edited: bool


def _first_line(body: str) -> str:
    for line in body.splitlines():
        if line.strip():
            return line.strip()
    return ""


def _as_verdict_comment(
    comment: typing.Mapping[str, object], *, deleted: bool = False, edited: bool = False
) -> typing.Optional[VerdictComment]:
    body = comment.get("body")
    if not isinstance(body, str) or not body:
        return None
    first = _first_line(body)
    head_match = HEX40_IN_TEXT.search(first)
    value_match = VERDICT_TOKEN.search(first)
    if value_match is None:
        for line in body.splitlines():
            disposition = DISPOSITION_LINE.match(line)
            if disposition is not None:
                value_match = disposition
                break
    if head_match is None or value_match is None:
        return None
    comment_id = comment.get("id")
    if not isinstance(comment_id, int):
        return None
    user = comment.get("user") if isinstance(comment.get("user"), dict) else {}
    author = user.get("login") if isinstance(user.get("login"), str) else None
    created = comment.get("created_at") if isinstance(comment.get("created_at"), str) else ""
    updated = comment.get("updated_at") if isinstance(comment.get("updated_at"), str) else ""
    if not created:
        return None
    return VerdictComment(
        comment_id=comment_id,
        body=body,
        created_at=created,
        updated_at=updated or created,
        author=author,
        html_url=comment.get("html_url") if isinstance(comment.get("html_url"), str) else "",
        head_sha=head_match.group(1),
        value=value_match.group(1),
        deleted=deleted,
        edited=edited or (updated or created) != created,
    )


def _select_verdict(
    comments: typing.Sequence[typing.Mapping[str, object]],
    head_sha: str,
    event: Event,
    event_comment: typing.Optional[typing.Mapping[str, object]],
) -> typing.Tuple[
    typing.Optional[VerdictComment],
    typing.List[VerdictComment],
    typing.List[VerdictComment],
    typing.Optional[str],
]:
    """Return (bound, stale, ambiguous, ambiguity_detail).

    A verdict comment is one whose first non-empty line names a 40-character
    head and one of the record tokens PASS/REVISE/BLOCKED/FAIL.  Comments that
    name another head are recorded as stale; more than one comment naming the
    evaluated head is ambiguous and fails closed (no verdict group is bound).
    """

    candidates: typing.List[VerdictComment] = []
    seen: typing.Set[int] = set()
    for comment in comments:
        parsed = _as_verdict_comment(comment)
        if parsed is not None and parsed.comment_id not in seen:
            candidates.append(parsed)
            seen.add(parsed.comment_id)
    if (
        event.event_name == "issue_comment"
        and event.action in ("edited", "deleted")
        and isinstance(event_comment, dict)
    ):
        comment_id = event_comment.get("id")
        if isinstance(comment_id, int) and comment_id not in seen:
            parsed = _as_verdict_comment(
                event_comment,
                deleted=event.action == "deleted",
                edited=event.action == "edited",
            )
            if parsed is not None:
                candidates.append(parsed)
                seen.add(comment_id)
    current = [candidate for candidate in candidates if candidate.head_sha == head_sha]
    stale = [candidate for candidate in candidates if candidate.head_sha != head_sha]
    if len(current) > 1:
        return (None, stale, current, "more than one active F verdict names the evaluated head")
    if len(current) == 1:
        return (current[0], stale, [], None)
    if stale and not current:
        return (None, stale, [], "an F verdict exists only for a different head")
    return (None, stale, [], None)


# ---------------------------------------------------------------------------
# Envelope writing and package validation
# ---------------------------------------------------------------------------


def _write_json(path: Path, document: typing.Mapping[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(document, sort_keys=True, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def _write_envelope(
    path: Path,
    payload: typing.Dict[str, object],
    provenance: typing.Dict[str, object],
) -> typing.Dict[str, object]:
    record = dict(provenance)
    record["declared_payload_sha256"] = canonical.digest(payload)
    record["declared_payload_bytes"] = len(canonical.canonical_bytes(payload))
    document = {"payload": payload, "provenance": record}
    _write_json(path, document)
    return document


def _validate_envelope(path: Path) -> inputs.Envelope:
    """Re-read a written envelope through the moved package validator (M4)."""

    try:
        envelope = inputs.load_envelope(path)
    except inputs.InputError as error:
        raise AdapterError(EXIT_INTERNAL, "written envelope failed package validation: %s" % error.detail) from None
    if envelope.issues:
        raise AdapterError(
            EXIT_INTERNAL,
            "written envelope failed package validation: %s" % envelope.issues[0].detail,
        )
    return envelope


def _issue_records(issues: typing.Iterable[records.Issue]) -> typing.List[typing.Dict[str, str]]:
    return [{"code": issue.code, "detail": issue.detail} for issue in issues]


# ---------------------------------------------------------------------------
# Fetch phase
# ---------------------------------------------------------------------------


def _pr_parts(pr: typing.Mapping[str, object]) -> typing.Tuple[str, str, str, str, str]:
    head = pr.get("head") if isinstance(pr.get("head"), dict) else {}
    base = pr.get("base") if isinstance(pr.get("base"), dict) else {}
    return (
        typing.cast(str, head.get("sha")),
        typing.cast(str, base.get("sha")),
        typing.cast(str, base.get("ref")),
        typing.cast(str, head.get("ref")) if isinstance(head.get("ref"), str) else "",
        _repo_full_name(head.get("repo")) or "",
    )


def _commit_author(commit: typing.Mapping[str, object]) -> typing.Optional[str]:
    author = commit.get("author")
    if isinstance(author, dict) and isinstance(author.get("login"), str) and author["login"]:
        return typing.cast(str, author["login"])
    inner = commit.get("commit") if isinstance(commit.get("commit"), dict) else {}
    author_record = inner.get("author") if isinstance(inner.get("author"), dict) else {}
    email = author_record.get("email")
    if isinstance(email, str) and email:
        return email
    return None


def _commit_time(commit: typing.Mapping[str, object]) -> typing.Optional[datetime.datetime]:
    inner = commit.get("commit") if isinstance(commit.get("commit"), dict) else {}
    for key in ("committer", "author"):
        record = inner.get(key) if isinstance(inner.get(key), dict) else {}
        parsed = _parse_time(record.get("date"))
        if parsed is not None:
            return parsed
    return None


def _as_of(pr: typing.Mapping[str, object], bound: typing.Optional[VerdictComment]) -> str:
    if bound is not None and _parse_time(bound.created_at) is not None:
        return bound.created_at
    updated = pr.get("updated_at")
    if isinstance(updated, str) and updated:
        return updated
    created = pr.get("created_at")
    if isinstance(created, str) and created:
        return created
    return "UNKNOWN"


def _store_summary(store: records.StoreResult) -> typing.Dict[str, object]:
    return {
        "binding_status": store.binding_status,
        "binding_detail": store.binding_detail,
        "issues": _issue_records(store.issues),
        "revision_state_sha256": store.revision_state_sha256() if not store.issues else "",
        "git_base": store.git_base,
        "prefix_status": store.prefix_checks.get("__status__", ""),
    }


def _resolve_owner_line(
    repo_root: Path, texts: typing.Sequence[str]
) -> typing.Tuple[typing.Optional[typing.Dict[str, object]], typing.Optional[typing.Dict[str, object]], str]:
    """Resolve the one cited owner-line entry from the base-tree register.

    Returns (owner_line, owner_line_resolution, detail).  Two different cited
    entry ids are ambiguous and are not resolved.
    """

    cited: typing.Set[str] = set()
    for text in texts:
        cited.update(APR_ID.findall(text))
    if len(cited) != 1:
        return (None, None, "no single owner-line entry is cited" if not cited else "more than one owner-line entry is cited")
    entry_id = cited.pop()
    register_path = repo_root / records.REGISTER_RELATIVE_PATH
    if not register_path.is_file():
        return (None, None, "the approval register is absent from the base checkout")
    raw = register_path.read_bytes()
    register_sha = _checksum_bytes(raw)
    text = raw.decode("utf-8", "replace")
    entry = records.resolve_register_entry(text, entry_id)
    owner_line: typing.Dict[str, object] = {"id": entry_id, "register_sha256": register_sha}
    if entry is None:
        return (owner_line, None, "the cited owner-line entry is absent from the register")
    resolution: typing.Dict[str, object] = {
        "entry_id": entry_id,
        "register_sha256": register_sha,
        "effective_status": entry.status,
    }
    if entry.scope_present:
        resolution["scope"] = dict(entry.scope)
    return (owner_line, resolution, "register entry %s resolves %s" % (entry_id, entry.status))


def _fetch_payloads(
    client: GitHubClient,
    pr: typing.Dict[str, object],
    pr_number: int,
    repo: str,
    head_sha: str,
    base_sha: str,
    tree_sha: str,
    parents: typing.List[str],
    comments: typing.List[typing.Dict[str, object]],
    commits: typing.List[typing.Dict[str, object]],
    event: Event,
    event_comment: typing.Optional[typing.Mapping[str, object]],
    repo_root: Path,
) -> typing.Tuple[
    typing.Dict[str, object],
    typing.Optional[VerdictComment],
    typing.List[VerdictComment],
    typing.List[VerdictComment],
    typing.Optional[str],
    typing.Dict[str, object],
]:
    owner, name = repo.split("/", 1)
    base_ref = pr["base"]["ref"] if isinstance(pr.get("base"), dict) else ""
    base_ref = typing.cast(str, base_ref)
    bound, stale, ambiguous, ambiguity = _select_verdict(comments, head_sha, event, event_comment)

    verdict_records: typing.List[typing.Dict[str, object]] = []
    for candidate in [*([bound] if bound else []), *stale, *ambiguous]:
        verdict_records.append(
            {
                "record_id": "issue-comment-%d" % candidate.comment_id,
                "head_sha": candidate.head_sha,
                "value": candidate.value,
                "active": True,
            }
        )

    last_commit = max(
        (value for value in (_commit_time(commit) for commit in commits) if value is not None),
        default=None,
    )
    posted_after = (
        bound is not None
        and last_commit is not None
        and _parse_time(bound.created_at) is not None
        and typing.cast(datetime.datetime, _parse_time(bound.created_at)) > last_commit
    )

    payload: typing.Dict[str, object] = {
        "repo": {"owner": owner, "name": name},
        "change": {"type": "PR", "id": pr_number},
        "merge_target": {"ref": "refs/heads/" + base_ref},
        "contract_schema_version": catalogue.CONTRACT_SCHEMA_ID,
        "bound_set_id": catalogue.BOUND_SET_ID,
        "bound_set_version": catalogue.BOUND_SET_VERSION,
        "canonicalization_version": catalogue.CANONICALIZATION_VERSION,
        "head_sha": head_sha,
        "tree_sha": tree_sha,
        "base_sha": base_sha,
    }
    if parents:
        payload["parents"] = parents
    if isinstance(pr.get("html_url"), str) and pr["html_url"]:
        typing.cast(typing.Dict[str, object], payload["change"])["url"] = pr["html_url"]
    store = records.load_store(repo_root, RECORDS_DIR, DEFAULT_BASE_REF)
    if not store.issues:
        payload["revision_state_sha256"] = store.revision_state_sha256()

    commit_authors: typing.List[str] = []
    missing_author = False
    for commit in commits:
        identity = _commit_author(commit)
        if identity is None:
            missing_author = True
        elif identity not in commit_authors:
            commit_authors.append(identity)

    record: typing.Dict[str, object] = {
        "verdict_records": verdict_records,
        "identity_attestation": {
            "repo": {"owner": owner, "name": name},
            "change": {"type": "PR", "id": pr_number},
        },
    }
    if commit_authors and not missing_author:
        record["commit_authors"] = sorted(commit_authors)

    if bound is not None:
        record["body_text"] = bound.body
        payload["verdict"] = {
            "stage": "F",
            "value": bound.value,
            "record_id": "issue-comment-%d" % bound.comment_id,
            "record_sha256": _checksum_bytes(bound.body.encode("utf-8")),
            "posted_at": bound.created_at,
            "posted_after_last_commit": bool(posted_after),
            "edit_state": {
                "post_post_edits": 0 if not bound.edited else 1,
                "deleted": bool(bound.deleted),
                "body_hash_match": not bound.edited and not bound.deleted,
            },
            "event_ref": bound.html_url or ("issue-comment:%d" % bound.comment_id),
        }
        distinct = sorted(
            {
                "implementer",
                "pr-author",
                *([typing.cast(str, pr["user"]["login"])] if isinstance(pr.get("user"), dict)
                  and isinstance(pr["user"].get("login"), str) else []),
                *commit_authors,
            }
        )
        if bound.author and not missing_author:
            reviewer: typing.Dict[str, object] = {
                "identity_ref": bound.author,
                "role": "F",
                "auth_method": "UNVERIFIED",
                "auth_verified": False,
                "independence": {"distinct_from": distinct},
            }
            if "INDEPENDENT" in bound.body:
                typing.cast(typing.Dict[str, object], reviewer["independence"])["class"] = "INDEPENDENT"
            payload["reviewer"] = reviewer

    texts = [typing.cast(str, record.get("body_text") or "")]
    if isinstance(pr.get("body"), str):
        texts.append(typing.cast(str, pr["body"]))
    owner_line, resolution, owner_detail = _resolve_owner_line(repo_root, texts)
    if owner_line is not None:
        payload["owner_line"] = owner_line
    if resolution is not None:
        record["owner_line_resolution"] = resolution
    payload["record"] = record

    return payload, bound, stale, ambiguous, ambiguity, {
        "store": _store_summary(store),
        "owner_line": owner_detail,
        "commit_authors": commit_authors,
        "missing_commit_author": missing_author,
        "posted_after_last_commit": bool(posted_after),
        "last_commit_time": last_commit.strftime("%Y-%m-%dT%H:%M:%SZ") if last_commit else "",
    }


def _freeze_payload(head_sha: str, base_sha: str, tree_sha: str) -> typing.Dict[str, object]:
    return {
        "head_sha": head_sha,
        "tree_sha": tree_sha,
        "base_sha": base_sha,
        "settlement_ref": "aegis-verdict-gate-settlement",
    }


def _settlement_payload(
    bound: typing.Optional[VerdictComment],
) -> typing.Dict[str, object]:
    if bound is not None and not bound.edited and not bound.deleted:
        sources = [
            {
                "source_id": "f-verdict-%d" % bound.comment_id,
                "state": "SETTLED",
                "disposition_authority_ref": None,
                "disposition_scope": None,
                "expires": None,
            }
        ]
        settled = True
    else:
        sources = [
            {
                "source_id": "f-verdict",
                "state": "PENDING",
                "disposition_authority_ref": None,
                "disposition_scope": None,
                "expires": None,
            }
        ]
        settled = False
    return {
        "settlement_id": "aegis-verdict-gate-settlement",
        "pre_audit_checks": [],
        "review_sources": sources,
        "settled": settled,
    }


def _head_history_payload(pr_number: int, head_sha: str) -> typing.Dict[str, object]:
    # Never guessed: an empty list with provenance.status UNVERIFIED.  The
    # checker blocks the budget term; the adapter does not claim used=0.
    return {"change_id": pr_number, "candidate_head": head_sha, "heads": []}


def _fetch(
    run_dir: Path,
    repo_root: Path,
    environ: typing.Mapping[str, str],
    transport: Transport,
) -> int:
    context_path = run_dir / "gate-context.json"
    if not context_path.is_file():
        raise AdapterError(EXIT_USAGE, "no resolved gate context in the run directory")
    context = json.loads(context_path.read_text(encoding="utf-8"))
    if not isinstance(context, dict) or context.get("schema") != SCHEMA_CONTEXT:
        raise AdapterError(EXIT_USAGE, "the resolved gate context is not usable")
    if context.get("decision") != "evaluate":
        raise AdapterError(EXIT_USAGE, "the resolved gate context is not an evaluation")
    repo = typing.cast(str, context["repo"])
    pr_number = typing.cast(int, context["pull_request"])
    head_sha = typing.cast(str, context["head_sha"])
    base_sha = typing.cast(str, context["base_sha"])
    # The fetch phase must run from the resolved base tree.  For
    # pull_request_target that is the event base checkout; for issue_comment
    # the workflow checks the resolved base out after the resolve phase.
    if _git_head(repo_root) != base_sha:
        raise AdapterError(
            EXIT_BASE_MISMATCH,
            "the fetch phase is not running at the resolved base; refusing to evaluate a stale base",
        )
    token = environ.get("GITHUB_TOKEN")
    if not token:
        raise AdapterError(EXIT_AUTH, "GITHUB_TOKEN is absent: refusing to call the provider")
    client = GitHubClient(
        transport,
        api_url=environ.get("GITHUB_API_URL") or "https://api.github.com",
        token=token,
    )
    pr = client.get_object("/repos/%s/pulls/%d" % (repo, pr_number), "pull request")
    _require_pr(pr, repo, pr_number)
    if pr["head"]["sha"] != head_sha:
        raise AdapterError(EXIT_HEAD_MOVED, "the pull request head moved after the event")
    if pr["base"]["sha"] != base_sha:
        raise AdapterError(EXIT_BASE_MISMATCH, "the pull request base moved after the event")
    if pr.get("state") != "open":
        raise AdapterError(EXIT_FOREIGN, "the pull request is not open")
    head_commit = client.get_object("/repos/%s/commits/%s" % (repo, head_sha), "head commit")
    commit_inner = head_commit.get("commit") if isinstance(head_commit.get("commit"), dict) else {}
    tree = commit_inner.get("tree") if isinstance(commit_inner.get("tree"), dict) else {}
    tree_sha = tree.get("sha") if isinstance(tree.get("sha"), str) else ""
    if not tree_sha or not HEX40.match(tree_sha):
        raise AdapterError(EXIT_PROVIDER, "the head commit has no usable tree sha")
    parents = [
        parent["sha"]
        for parent in (head_commit.get("parents") or [])
        if isinstance(parent, dict) and isinstance(parent.get("sha"), str) and HEX40.match(parent["sha"])
    ]
    commits = client.get_array(
        "/repos/%s/pulls/%d/commits?per_page=100" % (repo, pr_number), "pull request commits"
    )
    comments = client.get_array(
        "/repos/%s/issues/%d/comments?per_page=100" % (repo, pr_number), "pull request comments"
    )
    event = Event(
        typing.cast(str, context["event_name"]),
        typing.cast(str, context.get("event_action") or ""),
        "evaluate",
        "",
        repo,
        pr_number,
        head_sha,
        base_sha,
        typing.cast(str, context["base_ref"]),
        context.get("head_ref") if isinstance(context.get("head_ref"), str) else None,
        context.get("head_repo") if isinstance(context.get("head_repo"), str) else None,
    )
    event_comment = None
    if event.event_name == "issue_comment" and event.action in ("edited", "deleted"):
        event_path = environ.get("GITHUB_EVENT_PATH")
        if event_path and Path(event_path).is_file():
            try:
                event_payload = json.loads(Path(event_path).read_text(encoding="utf-8"))
            except (OSError, ValueError):
                event_payload = {}
            if isinstance(event_payload, dict) and isinstance(event_payload.get("comment"), dict):
                event_comment = typing.cast(typing.Dict[str, object], event_payload["comment"])

    payload, bound, stale, ambiguous, ambiguity, findings = _fetch_payloads(
        client, pr, pr_number, repo, head_sha, base_sha, tree_sha, parents,
        comments, commits, event, event_comment, repo_root,
    )
    as_of = _as_of(pr, bound)
    provenance = {
        "source_ref": "GET /repos/%s/pulls/%d + /issues/%d/comments + /commits" % (repo, pr_number, pr_number),
        "as_of": as_of,
        "producer_role": "provider-adapter",
        "producer_identity_ref": "aegis-verdict-gate-fetch",
    }
    envelope_paths: typing.List[str] = []
    envelope_paths.append("verdict.json")
    _write_envelope(run_dir / "verdict.json", payload, provenance)
    _validate_envelope(run_dir / "verdict.json")

    freeze_payload = _freeze_payload(head_sha, base_sha, tree_sha)
    _write_envelope(
        run_dir / "freeze.json",
        freeze_payload,
        dict(provenance, source_ref="provider/event identity + base-only checkout"),
    )
    freeze_envelope = _validate_envelope(run_dir / "freeze.json")
    envelope_paths.append("freeze.json")

    settlement_payload = _settlement_payload(bound)
    _write_envelope(
        run_dir / "settlement.json",
        settlement_payload,
        dict(provenance, source_ref="F verdict comment state"),
    )
    settlement_envelope = _validate_envelope(run_dir / "settlement.json")
    envelope_paths.append("settlement.json")

    head_history_payload = _head_history_payload(pr_number, head_sha)
    _write_envelope(
        run_dir / "head-history.json",
        head_history_payload,
        dict(
            provenance,
            status="UNVERIFIED",
            source_ref="no authoritative published-head export is available from the read-only API",
            detail="the provider cannot establish a complete, attributable published-head sequence",
        ),
    )
    history_envelope = _validate_envelope(run_dir / "head-history.json")
    envelope_paths.append("head-history.json")

    stage_dir = run_dir / "stage-records"
    stage_dir.mkdir(parents=True, exist_ok=True)
    envelope_paths.append("stage-records/")

    manifest = {
        "schema": SCHEMA_PROVENANCE,
        "sources": [
            {
                "name": "event_payload",
                "ref": "GITHUB_EVENT_PATH",
                "event_name": event.event_name,
                "event_action": event.action,
            },
            {
                "name": "pull_request",
                "ref": "GET /repos/%s/pulls/%d" % (repo, pr_number),
                "sha256": canonical.digest(pr),
            },
            {
                "name": "pull_request_commits",
                "ref": "GET /repos/%s/pulls/%d/commits" % (repo, pr_number),
                "entries": len(commits),
            },
            {
                "name": "pull_request_comments",
                "ref": "GET /repos/%s/issues/%d/comments" % (repo, pr_number),
                "entries": len(comments),
            },
        ],
        "files": {
            name: {
                "sha256": _checksum_bytes((run_dir / name).read_bytes()),
                "bytes": (run_dir / name).stat().st_size,
            }
            for name in ("verdict.json", "freeze.json", "settlement.json", "head-history.json")
        },
        "unavailable_fields": dict(UNAVAILABLE_FIELDS),
    }
    _write_json(run_dir / "provenance-manifest.json", manifest)
    envelope_paths.append("provenance-manifest.json")

    derivations = {
        "freeze": _issue_records(inputs.derive_freeze(freeze_envelope, payload).issues),
        "settlement": _issue_records(
            inputs.derive_settlement(settlement_envelope, payload, repo_root).issues
        ),
        "head_history": _issue_records(inputs.validate_head_history(history_envelope, payload).issues),
    }
    result = {
        "schema": SCHEMA_RESULT,
        "phase": "fetch",
        "outcome": "ok",
        "exit_code": EXIT_OK,
        "decision": "evaluate",
        "repo": repo,
        "pull_request": pr_number,
        "head_sha": head_sha,
        "base_sha": base_sha,
        "files": envelope_paths,
        "unavailable": dict(UNAVAILABLE_FIELDS),
        "pre_f": bound is None,
        "verdict": None if bound is None else {
            "value": bound.value,
            "record_id": "issue-comment-%d" % bound.comment_id,
        },
        "stale_verdict_comment_ids": [candidate.comment_id for candidate in stale],
        "ambiguous_verdict_comment_ids": [candidate.comment_id for candidate in ambiguous],
        "ambiguity_detail": ambiguity,
        "findings": findings,
        "derivations": derivations,
        "provider_calls": client.calls,
    }
    _write_json(run_dir / "adapter-result.json", result)
    print(json.dumps(result, sort_keys=True))
    return EXIT_OK


# ---------------------------------------------------------------------------
# Resolve phase
# ---------------------------------------------------------------------------


def _resolve(
    run_dir: Path,
    repo_root: Path,
    environ: typing.Mapping[str, str],
    transport: Transport,
) -> int:
    repository = environ.get("GITHUB_REPOSITORY")
    if not repository or "/" not in repository:
        raise AdapterError(EXIT_USAGE, "GITHUB_REPOSITORY is absent or invalid")
    event_name = environ.get("GITHUB_EVENT_NAME")
    if not event_name:
        raise AdapterError(EXIT_USAGE, "GITHUB_EVENT_NAME is absent")
    event_path = environ.get("GITHUB_EVENT_PATH")
    if not event_path or not Path(event_path).is_file():
        raise AdapterError(EXIT_USAGE, "GITHUB_EVENT_PATH is absent or unreadable")
    raw = Path(event_path).read_bytes()
    if len(raw) > MAX_EVENT_BYTES:
        raise AdapterError(EXIT_USAGE, "the event payload exceeds the %d-byte bound" % MAX_EVENT_BYTES)
    try:
        payload = json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, ValueError):
        raise AdapterError(EXIT_USAGE, "the event payload is not UTF-8 JSON") from None
    if not isinstance(payload, dict):
        raise AdapterError(EXIT_USAGE, "the event payload is not a JSON object")
    event = resolve_event(event_name, payload, repository)
    base_context: typing.Dict[str, object] = {
        "schema": SCHEMA_CONTEXT,
        "event_name": event.event_name,
        "event_action": event.action,
        "decision": event.decision,
        "reason": event.reason,
        "repo": repository,
        "change_type": "PR" if event.pr_number is not None else "",
        "pull_request": event.pr_number,
        "head_sha": "",
        "base_sha": "",
        "base_ref": "",
        "head_ref": "",
        "head_repo": "",
        "tree_sha": "",
        "checkout_sha": "",
        "base_matches": False,
        "checkout_expected": environ.get("AEGIS_VERDICT_CHECKOUT_SHA", ""),
        "run_id": environ.get("GITHUB_RUN_ID", ""),
        "workflow_ref": environ.get("GITHUB_WORKFLOW_REF", ""),
    }
    if event.decision == "no-op":
        _write_json(run_dir / "gate-context.json", base_context)
        result = {
            "schema": SCHEMA_RESULT,
            "phase": "resolve",
            "outcome": "ok",
            "exit_code": EXIT_OK,
            "decision": "no-op",
            "reason": event.reason,
            "repo": repository,
            "pull_request": event.pr_number,
            "files": ["gate-context.json"],
            "provider_calls": 0,
        }
        _write_json(run_dir / "adapter-result.json", result)
        print(json.dumps(result, sort_keys=True))
        return EXIT_OK
    if event.pr_number is None:
        raise AdapterError(EXIT_USAGE, "the event did not resolve a pull request number")
    token = environ.get("GITHUB_TOKEN")
    if not token:
        raise AdapterError(EXIT_AUTH, "GITHUB_TOKEN is absent: refusing to call the provider")
    client = GitHubClient(
        transport,
        api_url=environ.get("GITHUB_API_URL") or "https://api.github.com",
        token=token,
    )
    pr = client.get_object("/repos/%s/pulls/%d" % (repository, event.pr_number), "pull request")
    _require_pr(pr, repository, event.pr_number)
    if pr.get("state") != "open":
        base_context["decision"] = "no-op"
        base_context["reason"] = "the pull request is not open"
        _write_json(run_dir / "gate-context.json", base_context)
        _write_json(
            run_dir / "adapter-result.json",
            {
                "schema": SCHEMA_RESULT,
                "phase": "resolve",
                "outcome": "ok",
                "exit_code": EXIT_OK,
                "decision": "no-op",
                "reason": "the pull request is not open",
                "repo": repository,
                "pull_request": event.pr_number,
                "files": ["gate-context.json"],
                "provider_calls": client.calls,
            },
        )
        return EXIT_OK
    pr_head, pr_base, pr_base_ref, pr_head_ref, pr_head_repo = _pr_parts(pr)
    head_sha = event.head_sha or pr_head
    base_sha = event.base_sha or pr_base
    base_ref = event.base_ref or pr_base_ref
    checkout = _git_head(repo_root)
    base_context.update(
        {
            "head_sha": head_sha,
            "base_sha": base_sha,
            "base_ref": base_ref,
            "head_ref": event.head_ref or pr_head_ref,
            "head_repo": event.head_repo or pr_head_repo,
            "checkout_sha": checkout,
            "base_matches": base_sha == checkout,
        }
    )
    _write_json(run_dir / "gate-context.json", base_context)
    if event.event_name == "pull_request_target" and pr_head != event.head_sha:
        raise AdapterError(EXIT_HEAD_MOVED, "the pull request head moved after the event")
    if pr_base != base_sha:
        raise AdapterError(EXIT_BASE_MISMATCH, "the resolved base is not the provider's current base")
    if event.event_name == "pull_request_target":
        # The event base is the checkout.  A differing resolved base would be
        # evaluated against the wrong tree, so this fails closed.
        expected = environ.get("AEGIS_VERDICT_CHECKOUT_SHA", "")
        if base_sha != checkout or (expected and expected != checkout):
            raise AdapterError(
                EXIT_BASE_MISMATCH,
                "the resolved base does not equal the base-only checkout; refusing to evaluate a stale base",
            )
    result = {
        "schema": SCHEMA_RESULT,
        "phase": "resolve",
        "outcome": "ok",
        "exit_code": EXIT_OK,
        "decision": "evaluate",
        "repo": repository,
        "pull_request": event.pr_number,
        "head_sha": head_sha,
        "base_sha": base_sha,
        "checkout_sha": checkout,
        "files": ["gate-context.json"],
        "provider_calls": client.calls,
    }
    _write_json(run_dir / "adapter-result.json", result)
    print(json.dumps(result, sort_keys=True))
    return EXIT_OK


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def _run_dir(environ: typing.Mapping[str, str]) -> Path:
    supplied = environ.get("AEGIS_VERDICT_RUN_DIR")
    runner_temp = environ.get("RUNNER_TEMP")
    if supplied:
        candidate = Path(supplied)
    elif runner_temp:
        candidate = Path(runner_temp) / RUN_DIR_NAME
    else:
        raise AdapterError(EXIT_USAGE, "refusing to write outside RUNNER_TEMP: set RUNNER_TEMP or AEGIS_VERDICT_RUN_DIR")
    if runner_temp:
        try:
            candidate.resolve().relative_to(Path(runner_temp).resolve())
        except ValueError:
            raise AdapterError(EXIT_USAGE, "AEGIS_VERDICT_RUN_DIR is not under RUNNER_TEMP") from None
    return candidate


def _write_result(
    run_dir: Path, phase: str, exit_code: int, reason: str, detail: typing.Optional[str] = None
) -> None:
    document = {
        "schema": SCHEMA_RESULT,
        "phase": phase,
        "outcome": "ok" if exit_code == EXIT_OK else "failed",
        "exit_code": exit_code,
        "reason": reason,
        "detail": detail or "",
    }
    try:
        _write_json(run_dir / "adapter-result.json", document)
    except OSError:
        pass


def main(
    argv: typing.Optional[typing.Sequence[str]] = None,
    *,
    transport: typing.Optional[Transport] = None,
    environ: typing.Optional[typing.Mapping[str, str]] = None,
) -> int:
    parser = argparse.ArgumentParser(
        prog="aegis_verdict_gate_fetch.py",
        description="Read-only provider adapter for the aegis-verdict-gate workflow.",
    )
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--resolve-only", action="store_true", help="resolve the event/PR/base and write gate-context.json")
    mode.add_argument("--fetch", action="store_true", help="write the C1.1a input envelopes from read-only provider data")
    parser.add_argument("--repo-root", default=".", help="base-only checkout root")
    args = parser.parse_args(argv)
    environment = dict(os.environ if environ is None else environ)
    token = environment.get("GITHUB_TOKEN", "")
    phase = "resolve" if args.resolve_only else "fetch"
    try:
        run_dir = _run_dir(environment)
        run_dir.mkdir(parents=True, exist_ok=True)
    except AdapterError as error:
        print(json.dumps({"outcome": "failed", "exit_code": error.exit_code, "reason": _redact(error.detail, token)}, sort_keys=True))
        return error.exit_code
    except OSError:
        print(json.dumps({"outcome": "failed", "exit_code": EXIT_INTERNAL, "reason": "cannot create the run directory"}, sort_keys=True))
        return EXIT_INTERNAL
    chosen = transport or UrllibTransport()
    try:
        if args.resolve_only:
            return _resolve(run_dir, Path(args.repo_root), environment, chosen)
        return _fetch(run_dir, Path(args.repo_root), environment, chosen)
    except AdapterError as error:
        _write_result(run_dir, phase, error.exit_code, _redact(error.detail, token))
        print(json.dumps({"outcome": "failed", "exit_code": error.exit_code, "reason": _redact(error.detail, token)}, sort_keys=True))
        return error.exit_code
    except Exception as error:  # noqa: BLE001 - an internal failure must never exit 0
        _write_result(run_dir, phase, EXIT_INTERNAL, "internal error: %s" % type(error).__name__)
        print(json.dumps({"outcome": "failed", "exit_code": EXIT_INTERNAL, "reason": "internal error: %s" % type(error).__name__}, sort_keys=True))
        return EXIT_INTERNAL


if __name__ == "__main__":
    sys.exit(main())
