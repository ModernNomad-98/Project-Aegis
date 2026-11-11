"""Append-only revision/review-head record store: reader, derivation, checks.

The store is data only (no writer runtime).  This module reads it, re-derives
every count, and fails closed on any inconsistency:

  * JSONL hash chain (prev_event_sha256 over the previous raw line);
  * append-only prefix invariant against the git base version of each file
    (read-only git plumbing only: rev-parse, cat-file, log, merge-base);
  * manifest re-hash (bytes/sha256/event counts/ids), deterministic
    store_digest recomputation and derived_counts_at_binding comparison;
  * derived revision/reopen/stop counts and revision_state_sha256 (VB-C06);
  * review-head derivation from the authoritative published-head export, with
    the change ledger required to be a consistent, never-disagreeing mirror;
  * provenance binding re-check (REGISTER_ENTRY / OWNER_LINE_RECORD / UNKNOWN).

No count is trusted from the manifest: every count is re-derived from the
record bytes.  Standard library only; no network.
"""

from __future__ import annotations

import dataclasses
import hashlib
import json
import subprocess
import typing
from pathlib import Path

from . import canonical, catalogue

ITEM_EVENT_KINDS = ("REVISION_RECORDED", "REOPEN_COUNTED", "STOP_STATE_SET", "LIFECYCLE_EVENT")
STOP_STATES = ("OPEN", "WAITING_ON_OWNER", "PARKED_UNMERGED", "CLOSED")
AUTHORITY_KINDS = ("REGISTER_ENTRY", "OWNER_LINE_RECORD", "UNKNOWN")
BINDING_STATUSES = ("VERIFIED", "UNVERIFIED", "ABSENT")
HEAD_EVENT_KINDS = ("INITIAL", "BATCHED_BLOCKING_FIX", "FINAL_BLOCKING_FIX", "EXCEPTION", "RESYNC")
FILE_KINDS = ("plan_item", "change_ledger")
REGISTER_RELATIVE_PATH = "docs/approvals/APPROVAL_REGISTER.md"
ALLOWED_GIT_SUBCOMMANDS = ("rev-parse", "cat-file", "log", "merge-base")

# Register resolution vocabulary.  A register entry is ACTIVE/REVOKED/EXPIRED/
# CONSUMED/SUPERSEDED; a later lifecycle event naming an earlier entry
# overrides that entry's "status at recording".
REGISTER_STATUSES = ("ACTIVE", "REVOKED", "EXPIRED", "CONSUMED", "SUPERSEDED")
REGISTER_LIFECYCLE_EVENTS = {
    "REVOKED": "REVOKED",
    "REVOCATION": "REVOKED",
    "EXPIRED": "EXPIRED",
    "EXPIRY": "EXPIRED",
    "CONSUMED": "CONSUMED",
    "SUPERSEDED": "SUPERSEDED",
    "SUPERSESSION": "SUPERSEDED",
}
# The machine-checkable gate scope an owner-line or exception entry must carry
# before it can authorise anything: the G group is resolved at gate time, never
# taken from unhashed record metadata.
GATE_SCOPE_FIELDS = ("repo", "change_id", "head_sha", "merge_target_ref")
AUTHORITY_RECORD_SCHEMA = "aegis.authority-record/v1"

BLOCKER_TAMPER = "STATE_TAMPER_SUSPECTED"
BLOCKER_REQUIRED_INPUT = "REQUIRED_INPUT_UNAVAILABLE"


class Issue(typing.NamedTuple):
    """A fail-closed finding: contract blocker code plus a specific detail."""

    code: str
    detail: str


def sha256_hex(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _is_hex(value: object, length: int) -> bool:
    if not isinstance(value, str) or len(value) != length:
        return False
    return all(char in "0123456789abcdef" for char in value)


def _read_json(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8"))


def _split_jsonl(raw: bytes) -> typing.List[bytes]:
    if raw == b"":
        return []
    if not raw.endswith(b"\n"):
        raise ValueError("record file does not end with LF")
    body = raw[:-1]
    return body.split(b"\n")


def _git(repo_root: Path, *args: str) -> typing.Tuple[int, str]:
    """Run one allow-listed read-only git command; returns (rc, stdout)."""

    if not args or args[0] not in ALLOWED_GIT_SUBCOMMANDS:
        raise ValueError("refused git subcommand: %r" % (args[0] if args else ""))
    try:
        completed = subprocess.run(
            ["git", "-C", str(repo_root)] + list(args),
            capture_output=True,
            check=False,
            timeout=60,
        )
    except (OSError, subprocess.SubprocessError):
        return (127, "")
    if completed.returncode != 0:
        return (completed.returncode, "")
    return (0, completed.stdout.decode("utf-8", "replace"))


def resolve_base(repo_root: Path, base_ref: str) -> typing.Optional[str]:
    """Resolve the base commit for the append-only prefix check."""

    code, out = _git(repo_root, "merge-base", "HEAD", base_ref)
    if code == 0 and out.strip():
        return out.strip().splitlines()[0].strip()
    code, out = _git(repo_root, "rev-parse", "--verify", base_ref + "^{commit}")
    if code == 0 and out.strip():
        return out.strip().splitlines()[0].strip()
    return None


def _base_file_bytes(repo_root: Path, base: str, relative_path: str) -> typing.Optional[bytes]:
    code, out = _git(repo_root, "cat-file", "-p", "%s:%s" % (base, relative_path))
    if code != 0:
        return None
    return out.encode("utf-8")


@dataclasses.dataclass
class RegisterEntry:
    """One resolved approval-register entry (G group, gate time).

    The G group is resolved from the register bytes the verdict cites, never
    from a supplied record's own claim about itself: `status` is the entry's
    effectively-ACTIVE status after later lifecycle events, and `scope` is the
    machine-checkable gate scope the entry carries.
    """

    entry_id: str
    status: str
    scope: typing.Dict[str, str]
    scope_present: bool
    line: int
    detail: str

    def covers(
        self,
        repo: str,
        change_id: object,
        head_sha: str,
        merge_target_ref: str,
    ) -> bool:
        """True only when the entry's gate scope covers this exact target."""

        if not self.scope_present:
            return False
        expected = {
            "repo": repo,
            "change_id": change_id,
            "head_sha": head_sha,
            "merge_target_ref": merge_target_ref,
        }
        for key in GATE_SCOPE_FIELDS:
            if str(self.scope.get(key, "")) != str(expected[key]):
                return False
        return True


def _words(text: str) -> typing.List[str]:
    """Split on non-alphanumeric characters (status tokens survive ** and —)."""

    words: typing.List[str] = []
    current: typing.List[str] = []
    for character in text:
        if character.isalnum() or character == "_":
            current.append(character)
        elif current:
            words.append("".join(current))
            current = []
    if current:
        words.append("".join(current))
    return words


def _status_token(text: str) -> str:
    for word in _words(text.upper()):
        if word in REGISTER_STATUSES:
            return word
    return ""


def _mentions(text: str, token: str) -> bool:
    """Whole-token mention (a register id is not matched inside a longer id)."""

    start = 0
    while True:
        index = text.find(token, start)
        if index < 0:
            return False
        before = text[index - 1] if index else " "
        after = text[index + len(token)] if index + len(token) < len(text) else " "
        if not (before.isalnum() or before == "-") and not (after.isalnum() or after == "-"):
            return True
        start = index + 1


def parse_gate_scope(text: str) -> typing.Dict[str, str]:
    """Parse a machine-checkable gate scope: `key=value; key=value`."""

    scope: typing.Dict[str, str] = {}
    for part in text.split(";"):
        if "=" not in part:
            continue
        key, value = part.split("=", 1)
        key = key.strip().lower().replace(" ", "_").replace("*", "")
        if key in GATE_SCOPE_FIELDS and value.strip():
            scope[key] = value.strip()
    return scope


def resolve_register_entry(raw_text: str, entry_id: str) -> typing.Optional[RegisterEntry]:
    """Resolve one register entry from the register bytes.

    Supported shapes (both are documented in the tool README):

    * a heading block `### <ENTRY-ID>: <title>` carrying `- **Status ...:**`
      and `- **Gate scope:** repo=…; change_id=…; head_sha=…; merge_target_ref=…`
      bullets;
    * a table row `| <ENTRY-ID> | <STATUS> | <gate scope> |`.

    The last declaration in document order governs, and a later lifecycle
    block (`Event:` REVOKED/REVOCATION/EXPIRED/EXPIRY/CONSUMED/SUPERSEDED)
    that names the entry overrides its status.  No entry, or an unparseable
    entry, resolves to None/`UNKNOWN` and never to ACTIVE.
    """

    if not entry_id:
        return None
    lines = raw_text.splitlines()
    blocks: typing.List[typing.Dict[str, object]] = []
    current: typing.Optional[typing.Dict[str, object]] = None
    for index, line in enumerate(lines):
        stripped = line.strip()
        if stripped.startswith("#"):
            if current is not None:
                current["end"] = index
                blocks.append(current)
            heading = stripped.lstrip("#").strip()
            current = {
                "start": index,
                "end": len(lines),
                "id": heading.split(":", 1)[0].strip(),
                "status": "",
                "scope": {},
                "scope_present": False,
                "event": "",
            }
            continue
        if current is None:
            current = {
                "start": 0,
                "end": len(lines),
                "id": "",
                "status": "",
                "scope": {},
                "scope_present": False,
                "event": "",
            }
        if not stripped.startswith("- **"):
            continue
        label, _, value = stripped[2:].partition(":")
        label = label.strip().lower()
        if label.startswith("**status") and not current["status"]:
            current["status"] = _status_token(value)
        elif label.startswith("**gate scope"):
            scope = parse_gate_scope(value)
            if scope:
                current["scope"] = scope
                current["scope_present"] = True
        elif label.startswith("**event") and not current["event"]:
            for word in _words(value.upper()):
                if word in REGISTER_LIFECYCLE_EVENTS:
                    current["event"] = REGISTER_LIFECYCLE_EVENTS[word]
                    break
    if current is not None:
        blocks.append(current)

    declarations: typing.List[typing.Dict[str, object]] = []
    for block in blocks:
        if block["id"] != entry_id:
            continue
        declarations.append(
            {
                "line": block["start"],
                "status": block["status"],
                "scope": block["scope"],
                "scope_present": block["scope_present"],
                "source": "heading block",
            }
        )
    for index, line in enumerate(lines):
        stripped = line.strip()
        if not stripped.startswith("|"):
            continue
        cells = [cell.strip() for cell in stripped.strip("|").split("|")]
        if len(cells) < 2 or cells[0] != entry_id:
            continue
        scope = parse_gate_scope(cells[2]) if len(cells) > 2 else {}
        declarations.append(
            {
                "line": index,
                "status": _status_token(cells[1]),
                "scope": scope,
                "scope_present": bool(scope),
                "source": "table row",
            }
        )
    if not declarations:
        return None
    declarations.sort(key=lambda entry: int(entry["line"]))
    chosen = declarations[-1]
    status = str(chosen["status"])
    scope = typing.cast(typing.Dict[str, str], chosen["scope"])
    scope_present = bool(chosen["scope_present"])
    for block in blocks:
        if int(block["start"]) <= int(chosen["line"]) or not block["event"]:
            continue
        text = "\n".join(lines[int(block["start"]) : int(block["end"])])
        if _mentions(text, entry_id):
            status = str(block["event"])
            scope = {}
            scope_present = False
    if status not in REGISTER_STATUSES:
        status = "UNKNOWN"
    return RegisterEntry(
        entry_id=entry_id,
        status=status,
        scope=scope,
        scope_present=scope_present,
        line=int(chosen["line"]),
        detail="%s at line %d" % (chosen["source"], int(chosen["line"]) + 1),
    )


@dataclasses.dataclass
class ItemState:
    item_id: str
    plan_id: str
    revision_count: int
    reopen_count: int
    stop_state: typing.Optional[str]
    relative_path: str
    event_ids: typing.List[str]

    def as_derived(self) -> typing.Dict[str, object]:
        return {
            "item_id": self.item_id,
            "revision_count": self.revision_count,
            "reopen_used": self.reopen_count > 0,
            "stop_state": self.stop_state,
        }


@dataclasses.dataclass
class ReviewHeads:
    used: int
    ordinal: int
    ledger_count: int
    heads: typing.List[str]
    issues: typing.List[Issue]


@dataclasses.dataclass
class StoreResult:
    repo_root: Path
    records_dir: Path
    schema_version: str
    manifest: typing.Dict[str, object]
    files: typing.List[typing.Dict[str, object]]
    items: typing.Dict[str, ItemState]
    change_events: typing.List[typing.Dict[str, object]]
    issues: typing.List[Issue]
    git_base: typing.Optional[str]
    prefix_checks: typing.Dict[str, str]
    declared_store_digest: str
    recomputed_store_digest: str
    binding: typing.Dict[str, object]
    binding_status: str
    binding_detail: str
    binding_issues: typing.List[Issue]

    def derived_counts(self) -> typing.Dict[str, object]:
        items = [self.items[key].as_derived() for key in sorted(self.items)]
        return {
            "items": items,
            "review_heads": {
                "used": len(self.change_events),
                "source": "change ledger (previously published heads only)",
            },
        }

    def revision_state_sha256(self) -> str:
        items = [
            {
                "item_id": self.items[key].item_id,
                "revision_count": self.items[key].revision_count,
                "reopen_used": self.items[key].reopen_count > 0,
                "stop_state": self.items[key].stop_state,
            }
            for key in sorted(self.items)
        ]
        return canonical.digest(
            {"schema_version": catalogue.REVISION_STATE_SCHEMA, "items": items}
        )


def _event_issues(
    event: typing.Any,
    index: int,
    previous_line: typing.Optional[bytes],
    relative_path: str,
) -> typing.List[Issue]:
    issues: typing.List[Issue] = []
    where = "%s line %d" % (relative_path, index + 1)
    if not isinstance(event, dict):
        return [Issue(BLOCKER_TAMPER, "%s is not a JSON object" % where)]
    for key, kind in (
        ("event_id", str),
        ("item_id", str),
        ("plan_id", str),
        ("event_kind", str),
        ("recorded_at", str),
        ("recorded_by", str),
    ):
        if not isinstance(event.get(key), kind) or (kind is str and not event.get(key)):
            issues.append(Issue(BLOCKER_TAMPER, "%s missing or invalid %s" % (where, key)))
    kind = event.get("event_kind")
    if kind not in ITEM_EVENT_KINDS:
        issues.append(Issue(BLOCKER_TAMPER, "%s unknown event_kind %r" % (where, kind)))
    if not isinstance(event.get("revision_counted"), bool):
        issues.append(Issue(BLOCKER_TAMPER, "%s revision_counted must be boolean" % where))
    if not isinstance(event.get("reopen_counted"), bool):
        issues.append(Issue(BLOCKER_TAMPER, "%s reopen_counted must be boolean" % where))
    stop_state = event.get("stop_state")
    if stop_state is not None and stop_state not in STOP_STATES:
        issues.append(Issue(BLOCKER_TAMPER, "%s unknown stop_state %r" % (where, stop_state)))
    if not isinstance(event.get("evidence_refs"), list) or not event.get("evidence_refs"):
        issues.append(Issue(BLOCKER_TAMPER, "%s evidence_refs must be a non-empty list" % where))
    authority = event.get("authority_ref")
    if not isinstance(authority, dict):
        issues.append(Issue(BLOCKER_TAMPER, "%s authority_ref missing" % where))
    else:
        if authority.get("authority_kind") not in AUTHORITY_KINDS:
            issues.append(
                Issue(BLOCKER_TAMPER, "%s authority_kind is not a contract enum" % where)
            )
        for key in ("holder_role",):
            if not isinstance(authority.get(key), str) or not authority.get(key):
                issues.append(Issue(BLOCKER_TAMPER, "%s authority_ref.%s missing" % (where, key)))
    expected_previous = None if previous_line is None else sha256_hex(previous_line)
    if event.get("prev_event_sha256") != expected_previous:
        issues.append(Issue(BLOCKER_TAMPER, "%s hash chain does not link to the previous line" % where))
    return issues


def _derive_item(
    item_id: str,
    relative_path: str,
    events: typing.List[typing.Dict[str, object]],
) -> typing.Tuple[ItemState, typing.List[Issue]]:
    issues: typing.List[Issue] = []
    revision_count = 0
    reopen_count = 0
    stop_state: typing.Optional[str] = None
    seen_ids: typing.List[str] = []
    plan_id = ""
    for event in events:
        if not isinstance(event, dict):
            continue
        plan_id = str(event.get("plan_id", plan_id))
        event_id = str(event.get("event_id", ""))
        if event_id in seen_ids:
            issues.append(Issue(BLOCKER_TAMPER, "%s duplicate event_id %s" % (relative_path, event_id)))
        elif seen_ids and event_id < seen_ids[-1]:
            issues.append(
                Issue(BLOCKER_TAMPER, "%s event_id %s is not in ascending order" % (relative_path, event_id))
            )
        seen_ids.append(event_id)
        kind = event.get("event_kind")
        if kind == "REVISION_RECORDED":
            revision_count += 1
            if event.get("revision_counted") is not True:
                issues.append(
                    Issue(BLOCKER_TAMPER, "%s REVISION_RECORDED %s is not revision_counted" % (relative_path, event_id))
                )
        if event.get("reopen_counted") is True:
            if kind != "REOPEN_COUNTED":
                issues.append(
                    Issue(BLOCKER_TAMPER, "%s reopen_counted is only valid on REOPEN_COUNTED" % relative_path)
                )
            reopen_count += 1
            if reopen_count > 1:
                issues.append(
                    Issue(BLOCKER_TAMPER, "%s second counted reopen is refused" % relative_path)
                )
        if kind == "STOP_STATE_SET":
            stop_state = typing.cast(typing.Optional[str], event.get("stop_state"))
            if stop_state is None:
                issues.append(
                    Issue(BLOCKER_TAMPER, "%s STOP_STATE_SET %s has no stop_state" % (relative_path, event_id))
                )
    if events and stop_state is None:
        issues.append(Issue(BLOCKER_TAMPER, "%s has no STOP_STATE_SET event" % relative_path))
    if not events:
        issues.append(Issue(BLOCKER_TAMPER, "%s is empty (a plan item needs recorded history)" % relative_path))
    return (
        ItemState(
            item_id=item_id,
            plan_id=plan_id,
            revision_count=revision_count,
            reopen_count=reopen_count,
            stop_state=stop_state,
            relative_path=relative_path,
            event_ids=seen_ids,
        ),
        issues,
    )


def _derive_change_events(
    relative_path: str,
    events: typing.List[typing.Dict[str, object]],
) -> typing.List[Issue]:
    issues: typing.List[Issue] = []
    expected_seq = 1
    for event in events:
        if not isinstance(event, dict):
            issues.append(Issue(BLOCKER_TAMPER, "%s ledger line is not an object" % relative_path))
            continue
        if event.get("seq") != expected_seq:
            issues.append(
                Issue(BLOCKER_TAMPER, "%s ledger seq is not contiguous at %r" % (relative_path, event.get("seq")))
            )
        expected_seq += 1
        if not _is_hex(event.get("head_sha"), 40):
            issues.append(Issue(BLOCKER_TAMPER, "%s ledger head_sha is not 40 lowercase hex" % relative_path))
        if event.get("kind") not in HEAD_EVENT_KINDS:
            issues.append(Issue(BLOCKER_TAMPER, "%s ledger kind is not a contract enum" % relative_path))
        exception_ref = event.get("exception_ref")
        if event.get("kind") == "EXCEPTION" and not exception_ref:
            issues.append(Issue(BLOCKER_TAMPER, "%s EXCEPTION row has no exception_ref" % relative_path))
        if event.get("kind") != "EXCEPTION" and exception_ref:
            issues.append(Issue(BLOCKER_TAMPER, "%s exception_ref on a non-EXCEPTION row" % relative_path))
        if not isinstance(event.get("counted_at"), str) or not str(event.get("counted_at")).endswith("Z"):
            issues.append(Issue(BLOCKER_TAMPER, "%s ledger counted_at is not ISO-8601 Z" % relative_path))
        if not isinstance(event.get("authority_ref"), dict):
            issues.append(Issue(BLOCKER_TAMPER, "%s ledger authority_ref missing" % relative_path))
    return issues


def derive_review_heads(
    change_events: typing.List[typing.Dict[str, object]],
    heads: typing.List[typing.Dict[str, object]],
    candidate_head: str,
) -> ReviewHeads:
    """Derive the exclusive previously-published head count from the export.

    used = published heads of this change excluding the candidate head under
    validation (initial = 0, second = 1, third = 2, fourth = 3).  The change
    ledger must be a consistent mirror that never disagrees with the export.
    """

    issues: typing.List[Issue] = []
    seqs = [head.get("seq") for head in heads]
    if seqs != list(range(1, len(seqs) + 1)):
        issues.append(Issue(BLOCKER_TAMPER, "head-history ordinals are not contiguous from 1"))
    export_heads: typing.List[str] = []
    for head in heads:
        head_sha = head.get("head_sha")
        if not _is_hex(head_sha, 40):
            issues.append(Issue(BLOCKER_TAMPER, "head-history entry %r is not 40 lowercase hex" % (head_sha,)))
            continue
        export_heads.append(typing.cast(str, head_sha))
        if head.get("kind") not in HEAD_EVENT_KINDS:
            issues.append(Issue(BLOCKER_TAMPER, "head-history kind is not a contract enum"))
    if len(set(export_heads)) != len(export_heads):
        issues.append(Issue(BLOCKER_TAMPER, "head-history contains a duplicate head"))
    is_candidate = [head == candidate_head for head in export_heads]
    if is_candidate and any(is_candidate[:-1]):
        issues.append(Issue(BLOCKER_TAMPER, "the candidate head is not the last published head"))
    used = sum(1 for head in export_heads if head != candidate_head)
    ledger_heads: typing.List[str] = []
    for event in change_events:
        if isinstance(event, dict) and _is_hex(event.get("head_sha"), 40):
            ledger_heads.append(typing.cast(str, event.get("head_sha")))
    if len(set(ledger_heads)) != len(ledger_heads):
        issues.append(Issue(BLOCKER_TAMPER, "change ledger repeats a head"))
    if candidate_head and candidate_head in ledger_heads:
        issues.append(Issue(BLOCKER_TAMPER, "change ledger records the candidate head as already published"))
    prior_export = [head for head in export_heads if head != candidate_head]
    if ledger_heads != prior_export:
        # Exact mirror, never a prefix: a ledger that records fewer heads than
        # the export is an undercount of the published-head budget, and a
        # ledger that records more heads than the export is an overcount.
        # Both are tamper; neither may be accepted as "model lag".
        issues.append(
            Issue(
                BLOCKER_TAMPER,
                "change ledger disagrees with the authoritative head export: the ledger must mirror all "
                "%d previously published head(s) exactly (it records %d)"
                % (len(prior_export), len(ledger_heads)),
            )
        )
    return ReviewHeads(
        used=used,
        ordinal=used + 1,
        ledger_count=len(ledger_heads),
        heads=export_heads,
        issues=issues,
    )


def _authority_record_problem(raw: bytes, entry_id: str) -> typing.Optional[str]:
    """Why a cited owner-line/authority record cannot be trusted (None = ok).

    The record must be a closed-schema authority record, not any repository
    file that happens to hash to the cited digest: the citation alone is not a
    grant, and a markdown page or a fixture cannot stand in for one.
    """

    try:
        document = json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, ValueError):
        return "is not UTF-8 JSON"
    if not isinstance(document, dict):
        return "is not a JSON object"
    if document.get("schema_version") != AUTHORITY_RECORD_SCHEMA:
        return "does not declare schema %s" % AUTHORITY_RECORD_SCHEMA
    if document.get("record_id") != entry_id:
        return "declares a different record_id"
    if document.get("authority_kind") != "OWNER_LINE_RECORD":
        return "declares a different authority_kind"
    if document.get("status") != "ACTIVE":
        return "is not ACTIVE"
    holder = document.get("holder_role")
    if not isinstance(holder, str) or not holder:
        return "names no holder_role"
    scope = document.get("scope")
    if not isinstance(scope, dict) or any(key not in scope for key in GATE_SCOPE_FIELDS):
        return "carries no complete scope"
    return None


def _verify_binding(repo_root: Path, binding: typing.Any) -> typing.Tuple[str, str, typing.List[Issue]]:
    """Re-check the manifest provenance binding at gate time."""

    if not isinstance(binding, dict):
        return ("UNVERIFIED", "no provenance_binding in manifest", [])
    issues: typing.List[Issue] = []
    kind = binding.get("authority_kind")
    status = binding.get("binding_status")
    if kind not in AUTHORITY_KINDS:
        issues.append(Issue(BLOCKER_TAMPER, "provenance_binding.authority_kind is not a contract enum"))
        return ("UNVERIFIED", "authority_kind is not a contract enum", issues)
    if status not in BINDING_STATUSES:
        issues.append(Issue(BLOCKER_TAMPER, "provenance_binding.binding_status is not a contract enum"))
        return ("UNVERIFIED", "binding_status is not a contract enum", issues)
    if status != "VERIFIED":
        return ("UNVERIFIED", "recorded binding_status is %s" % status, issues)
    if kind == "UNKNOWN":
        issues.append(Issue(BLOCKER_TAMPER, "an UNKNOWN authority cannot be recorded as VERIFIED"))
        return ("UNVERIFIED", "UNKNOWN authority cannot be VERIFIED", issues)
    declared_sha = binding.get("authority_ref_sha256")
    if kind == "REGISTER_ENTRY":
        register_path = repo_root / REGISTER_RELATIVE_PATH
        if not register_path.is_file():
            issues.append(Issue(BLOCKER_TAMPER, "claimed VERIFIED binding cites a missing register"))
            return ("UNVERIFIED", "approval register is missing", issues)
        raw = register_path.read_bytes()
        if sha256_hex(raw) != declared_sha:
            issues.append(Issue(BLOCKER_TAMPER, "claimed VERIFIED binding cites an edited register"))
            return ("UNVERIFIED", "register bytes do not match authority_ref_sha256", issues)
        entry_id = binding.get("authority_ref_id")
        if not isinstance(entry_id, str) or not _mentions(raw.decode("utf-8", "replace"), entry_id):
            issues.append(Issue(BLOCKER_TAMPER, "cited register entry id is absent from the register"))
            return ("UNVERIFIED", "cited register entry id is absent", issues)
        return ("VERIFIED", "register entry %s resolves at the cited sha256" % entry_id, issues)
    entry_id = binding.get("authority_ref_id")
    if not isinstance(entry_id, str) or "/" not in entry_id:
        return ("UNVERIFIED", "owner-line record id is not a resolvable repository path", issues)
    record_path = (repo_root / entry_id).resolve()
    try:
        record_path.relative_to(repo_root.resolve())
    except ValueError:
        issues.append(Issue(BLOCKER_TAMPER, "owner-line record path escapes the repository"))
        return ("UNVERIFIED", "owner-line record path escapes the repository", issues)
    if not record_path.is_file():
        issues.append(Issue(BLOCKER_TAMPER, "claimed VERIFIED binding cites a missing owner-line record"))
        return ("UNVERIFIED", "owner-line record is missing", issues)
    record_bytes = record_path.read_bytes()
    if sha256_hex(record_bytes) != declared_sha:
        issues.append(Issue(BLOCKER_TAMPER, "claimed VERIFIED binding cites an edited owner-line record"))
        return ("UNVERIFIED", "owner-line record bytes do not match authority_ref_sha256", issues)
    problem = _authority_record_problem(record_bytes, entry_id)
    if problem is not None:
        issues.append(
            Issue(
                BLOCKER_TAMPER,
                "claimed VERIFIED owner-line record %s %s (an arbitrary repository file is not an authority record)"
                % (entry_id, problem),
            )
        )
        return ("UNVERIFIED", "owner-line record %s %s" % (entry_id, problem), issues)
    return ("VERIFIED", "owner-line record %s resolves at the cited sha256" % entry_id, issues)


def load_store(
    repo_root: Path,
    records_dir: str = "docs/approvals/revision-state",
    base_ref: str = "origin/main",
) -> StoreResult:
    """Load, re-derive and validate the append-only record store."""

    root = Path(repo_root)
    store_dir = root / records_dir
    issues: typing.List[Issue] = []
    manifest: typing.Dict[str, object] = {}
    files: typing.List[typing.Dict[str, object]] = []
    items: typing.Dict[str, ItemState] = {}
    change_events: typing.List[typing.Dict[str, object]] = []
    prefix_checks: typing.Dict[str, str] = {}
    declared_digest = ""
    recomputed_digest = ""
    binding: typing.Dict[str, object] = {}
    binding_status = "UNVERIFIED"
    binding_detail = "no manifest read"
    binding_issues: typing.List[Issue] = []
    schema_version = ""

    manifest_path = store_dir / "manifest.json"
    if not manifest_path.is_file():
        issues.append(Issue(BLOCKER_REQUIRED_INPUT, "record store manifest is absent: %s" % manifest_path))
        return StoreResult(
            repo_root=root,
            records_dir=store_dir,
            schema_version="",
            manifest=manifest,
            files=files,
            items=items,
            change_events=change_events,
            issues=issues,
            git_base=None,
            prefix_checks=prefix_checks,
            declared_store_digest="",
            recomputed_store_digest="",
            binding=binding,
            binding_status=binding_status,
            binding_detail=binding_detail,
            binding_issues=binding_issues,
        )

    try:
        loaded = _read_json(manifest_path)
    except (OSError, ValueError) as error:
        issues.append(Issue(BLOCKER_TAMPER, "manifest is unparseable: %s" % error))
        loaded = {}
    if not isinstance(loaded, dict):
        issues.append(Issue(BLOCKER_TAMPER, "manifest is not a JSON object"))
        loaded = {}
    manifest = loaded
    schema_version = str(manifest.get("schema_version", ""))
    if schema_version != catalogue.REVISION_STORE_SCHEMA:
        issues.append(
            Issue(BLOCKER_TAMPER, "manifest schema_version is not %s" % catalogue.REVISION_STORE_SCHEMA)
        )
    for volatile in ("generated_at", "as_of", "timestamp"):
        if volatile in manifest:
            issues.append(Issue(BLOCKER_TAMPER, "manifest carries volatile field %s (deterministic bytes required)" % volatile))
    declared_digest = str(manifest.get("store_digest", ""))
    binding = manifest.get("provenance_binding") if isinstance(manifest.get("provenance_binding"), dict) else {}
    raw_files = manifest.get("files")
    if not isinstance(raw_files, list):
        issues.append(Issue(BLOCKER_TAMPER, "manifest files[] missing"))
        raw_files = []
    listed: typing.Dict[str, typing.Dict[str, object]] = {}
    for entry in raw_files:
        if not isinstance(entry, dict):
            issues.append(Issue(BLOCKER_TAMPER, "manifest files[] entry is not an object"))
            continue
        path = entry.get("path")
        if not isinstance(path, str):
            issues.append(Issue(BLOCKER_TAMPER, "manifest files[] entry has no path"))
            continue
        listed[path] = entry
        files.append(entry)
    expected_paths: typing.List[str] = []
    for pattern in ("items/*.jsonl", "changes/*.jsonl"):
        for path in sorted(store_dir.glob(pattern)):
            expected_paths.append(path.relative_to(store_dir).as_posix())
    for path in expected_paths:
        if path not in listed:
            issues.append(Issue(BLOCKER_TAMPER, "record file is not listed in the manifest: %s" % path))
    for path in sorted(listed):
        if path not in expected_paths:
            issues.append(Issue(BLOCKER_TAMPER, "manifest lists a record file that does not exist: %s" % path))

    for relative_path in sorted(listed):
        entry = listed[relative_path]
        file_path = store_dir / relative_path
        if not file_path.is_file():
            continue
        raw = file_path.read_bytes()
        actual_sha = sha256_hex(raw)
        if entry.get("bytes") != len(raw):
            issues.append(Issue(BLOCKER_TAMPER, "manifest bytes mismatch for %s" % relative_path))
        if entry.get("sha256") != actual_sha:
            issues.append(Issue(BLOCKER_TAMPER, "manifest sha256 mismatch for %s" % relative_path))
        kind = entry.get("kind")
        if kind not in FILE_KINDS:
            issues.append(Issue(BLOCKER_TAMPER, "manifest kind is not a contract enum for %s" % relative_path))
        try:
            lines = _split_jsonl(raw)
        except ValueError as error:
            issues.append(Issue(BLOCKER_TAMPER, "%s: %s" % (relative_path, error)))
            continue
        events: typing.List[typing.Dict[str, object]] = []
        for index, line in enumerate(lines):
            try:
                event = json.loads(line.decode("utf-8"))
            except (UnicodeDecodeError, ValueError):
                issues.append(Issue(BLOCKER_TAMPER, "%s line %d is not valid JSON" % (relative_path, index + 1)))
                break
            events.append(event if isinstance(event, dict) else {"__invalid__": True})
        if entry.get("event_count") != len(events):
            issues.append(Issue(BLOCKER_TAMPER, "manifest event_count mismatch for %s" % relative_path))
        first_id = events[0].get("event_id") if events else None
        last_id = events[-1].get("event_id") if events else None
        if events and entry.get("first_event_id") != first_id:
            issues.append(Issue(BLOCKER_TAMPER, "manifest first_event_id mismatch for %s" % relative_path))
        if events and entry.get("last_event_id") != last_id:
            issues.append(Issue(BLOCKER_TAMPER, "manifest last_event_id mismatch for %s" % relative_path))
        previous = None
        for index, line in enumerate(lines):
            try:
                event = json.loads(line.decode("utf-8"))
            except (UnicodeDecodeError, ValueError):
                break
            if kind == "plan_item":
                issues.extend(_event_issues(event, index, previous, relative_path))
            previous = line
        if kind == "plan_item" and events:
            item_id = str(entry.get("id", ""))
            state, item_issues = _derive_item(item_id, relative_path, events)
            issues.extend(item_issues)
            if item_id and item_id in items:
                issues.append(Issue(BLOCKER_TAMPER, "duplicate item id %s" % item_id))
            items[item_id] = state
        elif kind == "change_ledger":
            issues.extend(_derive_change_events(relative_path, events))
            change_events.extend(events)

    derived_at_binding = manifest.get("derived_counts_at_binding")
    if not isinstance(derived_at_binding, dict):
        issues.append(Issue(BLOCKER_TAMPER, "manifest derived_counts_at_binding missing"))
        derived_at_binding = {}
    bound_items = derived_at_binding.get("items")
    if not isinstance(bound_items, list):
        issues.append(Issue(BLOCKER_TAMPER, "manifest derived_counts_at_binding.items missing"))
        bound_items = []
    bound_by_id = {
        str(entry.get("item_id")): entry for entry in bound_items if isinstance(entry, dict)
    }
    for item_id, state in sorted(items.items()):
        bound = bound_by_id.get(item_id)
        if not isinstance(bound, dict):
            issues.append(Issue(BLOCKER_TAMPER, "derived item %s is not bound in the manifest" % item_id))
            continue
        # Every bound count/state is compared to the re-derived state.  The
        # integer counters are monotone: a decrease is tamper and an increase
        # is a legitimate append (a later counted reopen keeps its own
        # one-only rule).  stop_state is a bound state, so it must equal the
        # derivation; a transition needs a refreshed manifest, which the
        # per-file bytes/sha256 binding already requires.
        bound_revision = bound.get("revision_count")
        if not isinstance(bound_revision, int) or isinstance(bound_revision, bool):
            issues.append(Issue(BLOCKER_TAMPER, "manifest binds no integer revision_count for %s" % item_id))
        elif state.revision_count < bound_revision:
            issues.append(
                Issue(
                    BLOCKER_TAMPER,
                    "revision_count for %s decreased below the bound value (%d < %d)"
                    % (item_id, state.revision_count, bound_revision),
                )
            )
        bound_reopen = bound.get("reopen_used")
        if not isinstance(bound_reopen, bool):
            issues.append(Issue(BLOCKER_TAMPER, "manifest binds no boolean reopen_used for %s" % item_id))
        elif bound_reopen and state.reopen_count == 0:
            issues.append(
                Issue(BLOCKER_TAMPER, "reopen_used for %s decreased below the bound value (True -> False)" % item_id)
            )
        if "stop_state" not in bound:
            issues.append(Issue(BLOCKER_TAMPER, "manifest binds no stop_state for %s" % item_id))
        elif bound.get("stop_state") != state.stop_state:
            issues.append(
                Issue(
                    BLOCKER_TAMPER,
                    "stop_state for %s (%r) disagrees with the manifest binding (%r)"
                    % (item_id, state.stop_state, bound.get("stop_state")),
                )
            )
    if set(bound_by_id) - set(items):
        issues.append(Issue(BLOCKER_TAMPER, "manifest binds an item with no record file"))
    bound_heads = derived_at_binding.get("review_heads")
    if not isinstance(bound_heads, dict):
        issues.append(Issue(BLOCKER_TAMPER, "manifest derived_counts_at_binding.review_heads missing"))
    else:
        declared_used = bound_heads.get("used")
        if not isinstance(declared_used, int) or isinstance(declared_used, bool):
            issues.append(Issue(BLOCKER_TAMPER, "manifest review_heads.used is not an integer"))
        elif declared_used > len(change_events):
            issues.append(
                Issue(
                    BLOCKER_TAMPER,
                    "review-head count decreased below the bound value (%d < %d)"
                    % (len(change_events), declared_used),
                )
            )
    digest_files = [
        {
            "path": str(entry.get("path")),
            "bytes": entry.get("bytes"),
            "sha256": entry.get("sha256"),
            "event_count": entry.get("event_count"),
            "id": entry.get("id"),
            "kind": entry.get("kind"),
        }
        for entry in sorted(files, key=lambda item: str(item.get("path")))
    ]
    recomputed_digest = canonical.digest(
        {
            "schema_version": schema_version,
            "files": digest_files,
            "derived_counts_at_binding": derived_at_binding,
        }
    )
    if declared_digest != recomputed_digest:
        issues.append(Issue(BLOCKER_TAMPER, "manifest store_digest does not recompute"))

    base = resolve_base(root, base_ref)
    if base is None:
        # Fail closed: the append-only prefix invariant is a required input.
        # Without a resolvable base there is no evidence that a prior line was
        # not removed, so the check is never silently skipped.
        prefix_checks["__status__"] = "GIT_BASE_UNRESOLVED"
        issues.append(
            Issue(
                BLOCKER_REQUIRED_INPUT,
                "append-only prefix invariant cannot be verified: no git base resolved from %r in %s "
                "(a required input; the check is never skipped)" % (base_ref, root),
            )
        )
    else:
        prefix_checks["__status__"] = "GIT_BASE_RESOLVED"
        for relative_path in sorted(listed):
            repository_path = (Path(records_dir) / relative_path).as_posix()
            base_bytes = _base_file_bytes(root, base, repository_path)
            current_path = store_dir / relative_path
            if base_bytes is None:
                prefix_checks[relative_path] = "NEW_AT_BASE"
                continue
            current = current_path.read_bytes() if current_path.is_file() else b""
            if not current.startswith(base_bytes):
                issues.append(
                    Issue(BLOCKER_TAMPER, "record file %s is not an append-only prefix of its git base" % relative_path)
                )
                prefix_checks[relative_path] = "PREFIX_VIOLATION"
            else:
                prefix_checks[relative_path] = "APPEND_ONLY_OK"

    binding_status, binding_detail, binding_issues = _verify_binding(root, binding)
    if binding_status != "VERIFIED" and binding.get("binding_status") == "VERIFIED":
        issues.extend(binding_issues)
        issues.append(
            Issue(BLOCKER_TAMPER, "manifest claims a VERIFIED binding that does not re-check")
        )
    return StoreResult(
        repo_root=root,
        records_dir=store_dir,
        schema_version=schema_version,
        manifest=manifest,
        files=files,
        items=items,
        change_events=change_events,
        issues=issues,
        git_base=base,
        prefix_checks=prefix_checks,
        declared_store_digest=declared_digest,
        recomputed_store_digest=recomputed_digest,
        binding=binding,
        binding_status=binding_status,
        binding_detail=binding_detail,
        binding_issues=binding_issues,
    )
