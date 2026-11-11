#!/usr/bin/env python3
"""Head-bound commit-status publisher for the C1.1b aegis-verdict-gate workflow.

The publisher is the workflow's single write path.  It maps the checker's
already-evaluated result to exactly one commit status and refuses everything
that is not the evaluated pull request head.

Contract (C1.1b Stage A plan REV2 sections 5.1/5.3, authority REV6):
  * It validates the repository, pull request and head against the read-only
    inputs the adapter evaluated (gate-context.json, adapter-result.json and
    verdict.json), then re-reads the pull request and refuses a head that is
    not the pull request's current head at publication time.
  * It posts exactly one commit status, context "aegis-verdict-gate", to the
    resolved head sha: success only when the checker exited 0 AND its output
    says readiness true; failure when the checker is blocked/invalid (exit
    1/2) or an adapter condition blocks the evaluation; error on an internal
    failure (exit 3) or an unreadable/unconfirmed result.  It never posts
    pending and never retries: one bounded attempt.
  * A non-pull-request issue comment is a recorded no-op: no status is posted
    and the command exits 0 (plan section 5.2).  Every other refusal exits
    nonzero without posting, so the required context is absent (fail closed).
  * The token comes from GITHUB_TOKEN in the environment only; it is never a
    command-line argument, never written to an artifact, never printed and
    never placed in a URL or a request body.

Exit codes (stable; recorded in publish-result.json):
    0  a status was posted, or the event was a recorded no-op
    2  usage error or unusable run directory
    3  internal error or an unreadable/unconfirmed result
    4  provider failure (re-check or status POST)
    5  refusal: foreign repository, non-PR, stale/closed PR or head mismatch
    7  token absent or provider authentication denied (401/403)

No network is used when a transport object is injected (the tests inject a
mocked transport).  No pull-request code is read or executed.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import typing
import urllib.error as urlerror
import urllib.request as urlrequest
from pathlib import Path

SCHEMA_CONTEXT = "aegis.verdict-gate-context/v1"
SCHEMA_RESULT = "aegis.verdict-gate-publish-result/v1"

STATUS_CONTEXT = "aegis-verdict-gate"
MAX_DESCRIPTION = 140

EXIT_OK = 0
EXIT_USAGE = 2
EXIT_INTERNAL = 3
EXIT_PROVIDER = 4
EXIT_REFUSED = 5
EXIT_AUTH = 7

MAX_BODY_BYTES = 1024 * 1024
REQUEST_TIMEOUT = 20


class PublisherError(Exception):
    """A fail-closed publication condition with a stable exit code."""

    def __init__(self, exit_code: int, detail: str, *, posted: typing.Union[bool, str] = False) -> None:
        super().__init__(detail)
        self.exit_code = exit_code
        self.detail = detail
        self.posted = posted


class TransportError(Exception):
    """A transport failure; the message never contains headers or a token."""


class Response(typing.NamedTuple):
    status: int
    headers: typing.Mapping[str, str]
    body: bytes


class Transport(typing.Protocol):
    def get(self, url: str, headers: typing.Mapping[str, str]) -> Response:
        ...

    def post(self, url: str, headers: typing.Mapping[str, str], body: bytes) -> Response:
        ...


class UrllibTransport:
    """Minimal HTTP transport (standard library only); one attempt per call."""

    def _open(self, request: urlrequest.Request) -> Response:
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
            raise TransportError("request failed: %s" % type(error).__name__) from None

    def get(self, url: str, headers: typing.Mapping[str, str]) -> Response:
        return self._open(urlrequest.Request(url, headers=dict(headers), method="GET"))

    def post(self, url: str, headers: typing.Mapping[str, str], body: bytes) -> Response:
        return self._open(
            urlrequest.Request(url, data=body, headers=dict(headers), method="POST")
        )


def _redact(text: str, token: str) -> str:
    return text.replace(token, "[REDACTED]") if token else text


def _read_json(path: Path, what: str) -> typing.Dict[str, object]:
    if not path.is_file():
        raise PublisherError(EXIT_INTERNAL, "%s is absent: %s" % (what, path.name))
    try:
        document = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, ValueError):
        raise PublisherError(EXIT_INTERNAL, "%s is not UTF-8 JSON: %s" % (what, path.name)) from None
    if not isinstance(document, dict):
        raise PublisherError(EXIT_INTERNAL, "%s is not a JSON object: %s" % (what, path.name))
    return typing.cast(typing.Dict[str, object], document)


def _bounded_description(text: str) -> str:
    return " ".join(text.split())[:MAX_DESCRIPTION]


class StatusClient:
    """One read-only re-check and at most one status POST."""

    def __init__(self, transport: Transport, *, api_url: str, token: str) -> None:
        self._transport = transport
        self._api_url = api_url.rstrip("/")
        self._token = token
        self.gets = 0
        self.posts = 0

    def _headers(self) -> typing.Dict[str, str]:
        return {
            "Accept": "application/vnd.github+json",
            "Authorization": "Bearer " + self._token,
            "X-GitHub-Api-Version": "2022-11-28",
            "User-Agent": "aegis-verdict-gate-publish",
        }

    def _send(self, method: str, url: str, what: str, body: bytes = b"") -> Response:
        try:
            if method == "GET":
                self.gets += 1
                response = self._transport.get(url, self._headers())
            else:
                self.posts += 1
                headers = dict(self._headers())
                headers["Content-Type"] = "application/json"
                response = self._transport.post(url, headers, body)
        except TransportError as error:
            raise PublisherError(EXIT_PROVIDER, "%s: %s" % (what, error)) from None
        if response.status in (401, 403):
            raise PublisherError(EXIT_AUTH, "%s: provider denied the request (HTTP %d)" % (what, response.status))
        if response.status == 404:
            raise PublisherError(EXIT_REFUSED, "%s: provider has no such resource (HTTP 404)" % what)
        if response.status == 429:
            raise PublisherError(EXIT_PROVIDER, "%s: provider rate limit (HTTP 429)" % what)
        if response.status >= 500:
            raise PublisherError(EXIT_PROVIDER, "%s: provider error (HTTP %d)" % (what, response.status))
        return response

    def get_object(self, path: str, what: str) -> typing.Dict[str, object]:
        response = self._send("GET", self._api_url + path, what)
        if response.status != 200:
            raise PublisherError(EXIT_PROVIDER, "%s: unexpected provider status %d" % (what, response.status))
        try:
            document = json.loads(response.body.decode("utf-8"))
        except (UnicodeDecodeError, ValueError):
            raise PublisherError(EXIT_PROVIDER, "%s: response is not UTF-8 JSON" % what) from None
        if not isinstance(document, dict):
            raise PublisherError(EXIT_PROVIDER, "%s: response is not a JSON object" % what)
        return typing.cast(typing.Dict[str, object], document)

    def post_status(self, path: str, payload: typing.Mapping[str, object]) -> typing.Dict[str, object]:
        body = json.dumps(payload, sort_keys=True).encode("utf-8")
        response = self._send("POST", self._api_url + path, "commit status", body)
        if response.status != 201:
            raise PublisherError(
                EXIT_PROVIDER,
                "commit status: unexpected provider status %d" % response.status,
                posted=False,
            )
        try:
            document = json.loads(response.body.decode("utf-8"))
        except (UnicodeDecodeError, ValueError):
            raise PublisherError(EXIT_INTERNAL, "commit status: the confirmation is not UTF-8 JSON", posted="unknown") from None
        if not isinstance(document, dict):
            raise PublisherError(EXIT_INTERNAL, "commit status: the confirmation is not a JSON object", posted="unknown")
        return typing.cast(typing.Dict[str, object], document)


def _checker_exit(record_path: Path) -> int:
    document = _read_json(record_path, "the checker evidence record")
    code = document.get("exit_code")
    if not isinstance(code, int) or isinstance(code, bool):
        raise PublisherError(EXIT_INTERNAL, "the checker evidence record has no integer exit_code")
    return code


def _checker_json(log_path: Path) -> typing.Optional[typing.Dict[str, object]]:
    if not log_path.is_file():
        return None
    try:
        text = log_path.read_text(encoding="utf-8", errors="replace").strip()
    except OSError:
        return None
    if not text:
        return None
    try:
        document = json.loads(text)
    except ValueError:
        return None
    return typing.cast(typing.Dict[str, object], document) if isinstance(document, dict) else None


def _state(
    adapter: typing.Mapping[str, object], checker_record: Path, checker_log: Path
) -> typing.Tuple[str, str]:
    """Map the adapter/checker result to one status state; never defaults to success."""

    if adapter.get("outcome") != "ok":
        code = adapter.get("exit_code")
        reason = str(adapter.get("reason") or "the provider adapter failed")
        if code in (2, 4, 5, 6, 8):
            return ("failure", _bounded_description("blocked: " + reason))
        return ("error", _bounded_description("error: " + reason))
    checker_exit = _checker_exit(checker_record)
    if checker_exit == 0:
        result = _checker_json(checker_log)
        if result is None:
            raise PublisherError(
                EXIT_INTERNAL,
                "the checker exited 0 but its output is not parseable; refusing to post success",
            )
        if result.get("readiness") is not True:
            raise PublisherError(
                EXIT_INTERNAL,
                "the checker exited 0 without readiness true; refusing to post success",
            )
        return ("success", "readiness true; auditable tooling, not merge authority")
    if checker_exit in (1, 2):
        result = _checker_json(checker_log) or {}
        blockers = result.get("blockers")
        if isinstance(blockers, list) and blockers and isinstance(blockers[0], dict):
            code = str(blockers[0].get("code") or "BLOCKED")
            detail = str(blockers[0].get("detail") or "")
            return ("failure", _bounded_description("blocked: %s: %s" % (code, detail)))
        return ("failure", _bounded_description("blocked: the checker exited %d" % checker_exit))
    return ("error", _bounded_description("error: the checker exited %d" % checker_exit))


def _target_url(environ: typing.Mapping[str, str], repo: str, run_id: str) -> str:
    if not run_id:
        return ""
    server = (environ.get("GITHUB_SERVER_URL") or "https://github.com").rstrip("/")
    return "%s/%s/actions/runs/%s" % (server, repo, run_id)


def _validate_context(
    context: typing.Mapping[str, object], github_repository: str
) -> typing.Tuple[str, int, str]:
    if context.get("schema") != SCHEMA_CONTEXT:
        raise PublisherError(EXIT_USAGE, "the gate context schema is not recognised")
    repo = context.get("repo")
    if not isinstance(repo, str) or repo.lower() != github_repository.lower():
        raise PublisherError(EXIT_REFUSED, "the evaluated repository is not the workflow repository")
    if context.get("change_type") != "PR":
        raise PublisherError(EXIT_REFUSED, "the evaluated change is not a pull request")
    number = context.get("pull_request")
    if not isinstance(number, int) or number <= 0:
        raise PublisherError(EXIT_REFUSED, "the evaluated pull request number is not usable")
    head = context.get("head_sha")
    if not isinstance(head, str) or len(head) != 40 or set(head) - set("0123456789abcdef"):
        raise PublisherError(EXIT_REFUSED, "the evaluated head is not a 40-character lowercase sha")
    return (repo, number, head)


def _validate_evaluated_inputs(
    run_dir: Path, context: typing.Mapping[str, object], adapter: typing.Mapping[str, object]
) -> None:
    """Refuse a context that does not bind the inputs the checker evaluated."""

    repo = typing.cast(str, context["repo"])
    owner, name = repo.split("/", 1)
    payload = _read_json(run_dir / "verdict.json", "the evaluated verdict").get("payload")
    if not isinstance(payload, dict):
        raise PublisherError(EXIT_REFUSED, "the evaluated verdict has no payload object")
    verdict_repo = payload.get("repo") if isinstance(payload.get("repo"), dict) else {}
    change = payload.get("change") if isinstance(payload.get("change"), dict) else {}
    if verdict_repo.get("owner") != owner or verdict_repo.get("name") != name:
        raise PublisherError(EXIT_REFUSED, "the evaluated verdict names a different repository")
    if change.get("id") != context.get("pull_request") or change.get("type") != "PR":
        raise PublisherError(EXIT_REFUSED, "the evaluated verdict names a different pull request")
    if payload.get("head_sha") != context.get("head_sha"):
        raise PublisherError(EXIT_REFUSED, "the evaluated verdict does not bind the resolved head")
    if payload.get("base_sha") != context.get("base_sha"):
        raise PublisherError(EXIT_REFUSED, "the evaluated verdict does not bind the resolved base")
    adapter_head = adapter.get("head_sha")
    if isinstance(adapter_head, str) and adapter_head != context.get("head_sha"):
        raise PublisherError(EXIT_REFUSED, "the adapter result does not bind the resolved head")


def _summary(
    context: typing.Mapping[str, object],
    *,
    state: typing.Optional[str],
    description: str,
    posted: typing.Union[bool, str],
    reason: str,
    checker: typing.Optional[typing.Dict[str, object]],
) -> str:
    readiness = checker.get("readiness") if isinstance(checker, dict) else None
    assurance = checker.get("assurance") if isinstance(checker, dict) else None
    blockers = checker.get("blockers") if isinstance(checker, dict) else None
    lines = [
        "# aegis-verdict-gate",
        "",
        "- event: %s %s" % (context.get("event_name", ""), context.get("event_action", "")),
        "- evaluated head: %s" % (context.get("head_sha") or "(none)"),
        "- base: %s" % (context.get("base_sha") or "(none)"),
        "- checker readiness: %s" % ("true" if readiness is True else "false" if readiness is False else "not evaluated"),
        "- assurance: %s" % (json.dumps(assurance, sort_keys=True) if assurance else "not evaluated"),
    ]
    if isinstance(blockers, list) and blockers:
        lines.append("- blockers:")
        for blocker in blockers[:10]:
            if isinstance(blocker, dict):
                lines.append("  - %s [%s] %s" % (blocker.get("code"), blocker.get("classification"), blocker.get("detail")))
    if posted is True:
        lines.append("- published status: %s (context %s)" % (state, STATUS_CONTEXT))
    elif posted == "unknown":
        lines.append("- published status: unknown (one POST was attempted; it was not confirmed)")
    else:
        lines.append("- published status: none (%s)" % reason)
    lines.extend(
        [
            "",
            "Readiness is not merge authority. This job reports post-F readiness evidence only;",
            "it does not approve a B/D/E/F stage, grant merge authority, or register a required context.",
            "",
        ]
    )
    return "\n".join(lines)


def _write_result(path: Path, document: typing.Mapping[str, object]) -> None:
    try:
        path.write_text(
            json.dumps(document, sort_keys=True, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
            newline="\n",
        )
    except OSError:
        pass


def main(
    argv: typing.Optional[typing.Sequence[str]] = None,
    *,
    transport: typing.Optional[Transport] = None,
    environ: typing.Optional[typing.Mapping[str, str]] = None,
) -> int:
    parser = argparse.ArgumentParser(
        prog="aegis_verdict_gate_publish.py",
        description="Head-bound commit-status publisher for the aegis-verdict-gate workflow.",
    )
    parser.add_argument("--run-dir", required=True)
    parser.add_argument("--checker-record", required=True)
    parser.add_argument("--checker-log", required=True)
    args = parser.parse_args(argv)
    environment = dict(os.environ if environ is None else environ)
    token = environment.get("GITHUB_TOKEN", "")
    run_dir = Path(args.run_dir)
    try:
        run_dir.mkdir(parents=True, exist_ok=True)
    except OSError:
        print(json.dumps({"posted": False, "exit_code": EXIT_USAGE,
                          "reason": "the run directory is not writable"}, sort_keys=True))
        return EXIT_USAGE
    result_path = run_dir / "publish-result.json"
    summary_path = run_dir / "summary.md"
    state: typing.Optional[str] = None
    description = ""
    posted: typing.Union[bool, str] = False
    context: typing.Dict[str, object] = {}
    try:
        if not run_dir.is_dir():
            raise PublisherError(EXIT_USAGE, "the run directory is not usable")
        context = _read_json(run_dir / "gate-context.json", "the gate context")
        decision = context.get("decision")
        if decision == "no-op":
            reason = str(context.get("reason") or "the event is not a pull request in this repository")
            _write_result(
                result_path,
                {
                    "schema": SCHEMA_RESULT,
                    "posted": False,
                    "state": None,
                    "reason": reason,
                    "context": STATUS_CONTEXT,
                    "repo": context.get("repo"),
                    "pull_request": context.get("pull_request"),
                    "head_sha": context.get("head_sha"),
                },
            )
            summary_path.write_text(
                _summary(context, state=None, description="", posted=False, reason=reason, checker=None),
                encoding="utf-8",
                newline="\n",
            )
            print(json.dumps({"posted": False, "reason": reason}, sort_keys=True))
            return EXIT_OK
        if decision != "evaluate":
            raise PublisherError(EXIT_REFUSED, "the gate context decision is not recognised")
        github_repository = environment.get("GITHUB_REPOSITORY", "")
        if not github_repository:
            raise PublisherError(EXIT_USAGE, "GITHUB_REPOSITORY is absent")
        repo, number, head_sha = _validate_context(context, github_repository)
        adapter = _read_json(run_dir / "adapter-result.json", "the adapter result")
        if adapter.get("outcome") == "ok":
            _validate_evaluated_inputs(run_dir, context, adapter)
        else:
            # A failed adapter may not have written verdict.json; the resolved
            # context and the adapter's own head binding are still validated,
            # and the result is published as failure/error (never success).
            adapter_head = adapter.get("head_sha")
            if isinstance(adapter_head, str) and adapter_head != context.get("head_sha"):
                raise PublisherError(EXIT_REFUSED, "the adapter result does not bind the resolved head")
        state, description = _state(adapter, Path(args.checker_record), Path(args.checker_log))
        checker = _checker_json(Path(args.checker_log)) or {}
        if not token:
            raise PublisherError(EXIT_AUTH, "GITHUB_TOKEN is absent: refusing to publish")
        client = StatusClient(
            transport or UrllibTransport(),
            api_url=environment.get("GITHUB_API_URL") or "https://api.github.com",
            token=token,
        )
        pr = client.get_object("/repos/%s/pulls/%d" % (repo, number), "pull request")
        if pr.get("number") != number:
            raise PublisherError(EXIT_REFUSED, "the provider returned a different pull request")
        if pr.get("state") != "open":
            raise PublisherError(EXIT_REFUSED, "the pull request is not open; no status is posted")
        head = pr.get("head") if isinstance(pr.get("head"), dict) else {}
        if head.get("sha") != head_sha:
            raise PublisherError(EXIT_REFUSED, "the pull request head moved after evaluation; no status is posted")
        target = _target_url(environment, repo, str(context.get("run_id") or ""))
        payload: typing.Dict[str, object] = {
            "state": state,
            "context": STATUS_CONTEXT,
            "description": _bounded_description(description),
        }
        if target:
            payload["target_url"] = target
        confirmation = client.post_status("/repos/%s/statuses/%s" % (repo, head_sha), payload)
        if (
            confirmation.get("sha") != head_sha
            or confirmation.get("context") != STATUS_CONTEXT
            or confirmation.get("state") != state
        ):
            raise PublisherError(
                EXIT_INTERNAL,
                "the provider did not confirm the posted status for the evaluated head",
                posted="unknown",
            )
        posted = True
        result = {
            "schema": SCHEMA_RESULT,
            "posted": True,
            "state": state,
            "reason": description,
            "context": STATUS_CONTEXT,
            "repo": repo,
            "pull_request": number,
            "head_sha": head_sha,
            "target_url": target,
            "provider_gets": client.gets,
            "provider_posts": client.posts,
        }
        _write_result(result_path, result)
        summary_path.write_text(
            _summary(context, state=state, description=description, posted=True, reason="", checker=checker),
            encoding="utf-8",
            newline="\n",
        )
        print(json.dumps(result, sort_keys=True))
        return EXIT_OK
    except PublisherError as error:
        detail = _redact(error.detail, token)
        posted = error.posted
        _write_result(
            result_path,
            {
                "schema": SCHEMA_RESULT,
                "posted": posted,
                "state": None,
                "reason": detail,
                "context": STATUS_CONTEXT,
                "repo": context.get("repo"),
                "pull_request": context.get("pull_request"),
                "head_sha": context.get("head_sha"),
            },
        )
        try:
            summary_path.write_text(
                _summary(context, state=None, description="", posted=posted, reason=detail, checker=None),
                encoding="utf-8",
                newline="\n",
            )
        except OSError:
            pass
        print(json.dumps({"posted": posted, "exit_code": error.exit_code, "reason": detail}, sort_keys=True))
        return error.exit_code
    except Exception as error:  # noqa: BLE001 - an internal failure must never exit 0
        detail = "internal error: %s" % type(error).__name__
        _write_result(
            result_path,
            {
                "schema": SCHEMA_RESULT,
                "posted": posted,
                "state": None,
                "reason": detail,
                "context": STATUS_CONTEXT,
                "repo": context.get("repo"),
                "pull_request": context.get("pull_request"),
                "head_sha": context.get("head_sha"),
            },
        )
        print(json.dumps({"posted": posted, "exit_code": EXIT_INTERNAL, "reason": detail}, sort_keys=True))
        return EXIT_INTERNAL


if __name__ == "__main__":
    sys.exit(main())
