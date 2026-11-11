"""Record-store tests: counts, hash chain, append-only prefix, digest, budget.

Covers AC1, AC2 and the record half of AC5: the seeded store derives
A=5/B=7/C=2 with no reopen, an edited/removed line or a decreased count is
refused, the manifest is re-derived, the store_digest is deterministic and
the review-head count is the exclusive previously-published-head definition.
"""

from __future__ import annotations

import hashlib
import json
import pathlib
import shutil
import subprocess
import sys
import tempfile
import unittest

REPO_ROOT = pathlib.Path(__file__).resolve().parents[3]
SCRIPTS_DIR = pathlib.Path(__file__).resolve().parents[2]
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from aegis_verdict_gate import canonical, records  # noqa: E402

ITEM = "aegis.plan.fixture-0001"
HEAD = "a" * 40
EXPORT_HEAD_1 = "1" * 40
EXPORT_HEAD_2 = "2" * 40
EXPORT_HEAD_3 = "3" * 40


def _event(event_id, kind="REVISION_RECORDED", stop=None, reopen=False, item_id=ITEM):
    return {
        "event_id": event_id,
        "item_id": item_id,
        "plan_id": "PLAN-FIXTURE-0001",
        "event_kind": kind,
        "revision_counted": kind == "REVISION_RECORDED",
        "reopen_counted": reopen,
        "stop_state": stop,
        "authority_ref": {
            "authority_kind": "UNKNOWN",
            "authority_ref_id": None,
            "authority_ref_sha256": None,
            "holder_role": "programme-lead",
            "holder_identity_ref": None,
        },
        "evidence_refs": [{"ref_id": "fixture", "ref_sha256": "0" * 64}],
        "recorded_at": "2026-11-10T18:00:00Z",
        "recorded_by": "fixture-holder",
    }


def build_store(root, items, ledger=(), reverse_manifest_files=False):
    """Write a minimal consistent store and return its manifest."""

    root = pathlib.Path(root)
    store = root / records_store_dir()
    (store / "items").mkdir(parents=True, exist_ok=True)
    (store / "changes").mkdir(parents=True, exist_ok=True)
    files = []
    derived_items = []
    for item_id, events in items.items():
        slug = item_id.rsplit(".", 1)[-1]
        relative = "items/%s.jsonl" % slug
        lines = []
        previous = None
        revision_count = 0
        reopen_count = 0
        stop_state = None
        for event in events:
            payload = dict(event)
            payload["prev_event_sha256"] = previous
            line = canonical.dumps(payload).encode("utf-8")
            lines.append(line)
            previous = canonical.sha256_hex(line)
            if payload["event_kind"] == "REVISION_RECORDED":
                revision_count += 1
            if payload["reopen_counted"]:
                reopen_count += 1
            if payload["event_kind"] == "STOP_STATE_SET":
                stop_state = payload["stop_state"]
        raw = b"\n".join(lines) + b"\n"
        (store / relative).write_bytes(raw)
        files.append(
            {
                "path": relative,
                "kind": "plan_item",
                "id": item_id,
                "bytes": len(raw),
                "sha256": canonical.sha256_hex(raw),
                "event_count": len(lines),
                "first_event_id": json.loads(lines[0].decode("utf-8"))["event_id"],
                "last_event_id": json.loads(lines[-1].decode("utf-8"))["event_id"],
            }
        )
        derived_items.append(
            {
                "item_id": item_id,
                "revision_count": revision_count,
                "reopen_used": reopen_count > 0,
                "stop_state": stop_state,
            }
        )
    ledger_relative = "changes/c1-1-b1-minimal-2026-11-10.jsonl"
    ledger_lines = []
    for index, event in enumerate(ledger):
        payload = dict(event)
        payload["seq"] = index + 1
        ledger_lines.append(canonical.dumps(payload).encode("utf-8"))
    ledger_raw = b"\n".join(ledger_lines) + b"\n" if ledger_lines else b""
    (store / ledger_relative).write_bytes(ledger_raw)
    files.append(
        {
            "path": ledger_relative,
            "kind": "change_ledger",
            "id": "c1-1-b1-minimal-2026-11-10",
            "bytes": len(ledger_raw),
            "sha256": canonical.sha256_hex(ledger_raw),
            "event_count": len(ledger_lines),
            "first_event_id": None,
            "last_event_id": None,
        }
    )
    derived = {
        "items": sorted(derived_items, key=lambda entry: entry["item_id"]),
        "review_heads": {"used": len(ledger_lines), "source": "change ledger"},
    }
    ordered = sorted(files, key=lambda entry: entry["path"], reverse=reverse_manifest_files)
    digest_files = [
        {key: entry[key] for key in ("path", "bytes", "sha256", "event_count", "id", "kind")}
        for entry in sorted(files, key=lambda entry: entry["path"])
    ]
    manifest = {
        "schema_version": "aegis.revision-store/v1",
        "files": ordered,
        "derived_counts_at_binding": derived,
        "store_digest": canonical.digest(
            {
                "schema_version": "aegis.revision-store/v1",
                "files": digest_files,
                "derived_counts_at_binding": derived,
            }
        ),
        "provenance_binding": {
            "authority_kind": "UNKNOWN",
            "authority_ref_id": None,
            "authority_ref_sha256": None,
            "holder_role": "plan-holder",
            "holder_identity_ref": None,
            "binding_commit_or_pr": "fixture",
            "binding_status": "UNVERIFIED",
            "unverified_reason": "fixture",
        },
    }
    (store / "manifest.json").write_text(
        json.dumps(manifest, sort_keys=True, indent=2) + "\n", encoding="utf-8", newline="\n"
    )
    commit_git_base(root)
    return manifest


def records_store_dir():
    return "docs/approvals/revision-state"


def git(root, *args):
    completed = subprocess.run(
        ["git", "-C", str(root)] + list(args), capture_output=True, check=False, timeout=60
    )
    if completed.returncode != 0:
        raise AssertionError("git %s failed: %s" % (args, completed.stderr.decode("utf-8", "replace")))
    return completed.stdout.decode("utf-8", "replace")


def commit_git_base(root):
    """Give the scratch store a real worktree base.

    The append-only prefix invariant is a required input, so a store without a
    base fails closed.  A caller that has already created the repository (the
    dedicated prefix test) owns its own commits.
    """

    if (pathlib.Path(root) / ".git").exists():
        return
    git(root, "init", "-q", "-b", "main")
    git(root, "config", "user.email", "fixture@example.invalid")
    git(root, "config", "user.name", "Fixture Holder")
    git(root, "config", "core.autocrlf", "false")
    git(root, "add", "-A")
    git(root, "commit", "-q", "-m", "fixture base")
    git(root, "update-ref", "refs/remotes/origin/main", "HEAD")


def write_manifest(root, manifest):
    path = pathlib.Path(root) / records_store_dir() / "manifest.json"
    path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    return path


def rebind(manifest):
    """Recompute store_digest so only the tested binding term is inconsistent."""

    digest_files = [
        {key: entry[key] for key in ("path", "bytes", "sha256", "event_count", "id", "kind")}
        for entry in sorted(manifest["files"], key=lambda entry: entry["path"])
    ]
    manifest["store_digest"] = canonical.digest(
        {
            "schema_version": "aegis.revision-store/v1",
            "files": digest_files,
            "derived_counts_at_binding": manifest["derived_counts_at_binding"],
        }
    )
    return manifest


def ledger_event(head, kind="INITIAL", at="2026-11-10T18:00:00Z"):
    return {
        "head_sha": head,
        "kind": kind,
        "exception_ref": None,
        "counted_at": at,
        "authority_ref": {
            "authority_kind": "REGISTER_ENTRY",
            "authority_ref_id": "APR-FIXTURE-C1-0001",
            "holder_role": "programme-lead",
            "holder_identity_ref": None,
        },
    }


class SeedStoreTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # HEAD is always resolvable in a worktree; origin/main is not guaranteed
        # in every checkout, and an unresolvable base is now a required-input
        # blocker (B2), so the seed read names its base explicitly.
        cls.store = records.load_store(REPO_ROOT, base_ref="HEAD")

    def test_seed_counts_and_stop_states(self):
        self.assertEqual(self.store.issues, [])
        counts = {
            item_id: (state.revision_count, state.reopen_count, state.stop_state)
            for item_id, state in self.store.items.items()
        }
        self.assertEqual(
            counts,
            {
                "aegis.plan.maturity-package": (5, 0, "WAITING_ON_OWNER"),
                "aegis.plan.post-delivery-2026-11-09": (7, 0, "CLOSED"),
                "aegis.plan.integrated-2026-11-10": (2, 0, "OPEN"),
            },
        )

    def test_manifest_digest_recomputes(self):
        self.assertEqual(self.store.declared_store_digest, self.store.recomputed_store_digest)
        self.assertRegex(self.store.declared_store_digest, "^[0-9a-f]{64}$")

    def test_binding_is_unverified_without_a_fabricated_id(self):
        binding = self.store.manifest["provenance_binding"]
        self.assertEqual(binding["authority_kind"], "UNKNOWN")
        self.assertEqual(binding["binding_status"], "UNVERIFIED")
        self.assertIsNone(binding["authority_ref_id"])
        self.assertIsNone(binding["authority_ref_sha256"])
        self.assertEqual(self.store.binding_status, "UNVERIFIED")

    def test_manifest_is_deterministic_and_has_no_volatile_field(self):
        raw = (REPO_ROOT / records_store_dir() / "manifest.json").read_bytes()
        manifest = json.loads(raw.decode("utf-8"))
        for volatile in ("generated_at", "as_of", "timestamp"):
            self.assertNotIn(volatile, manifest)
        self.assertEqual(self.store.declared_store_digest, self.store.recomputed_store_digest)

    def test_revision_state_hash_is_derived_from_item_state(self):
        expected = canonical.digest(
            {
                "schema_version": "aegis.revision-state/v1",
                "items": [
                    {
                        "item_id": item_id,
                        "revision_count": state.revision_count,
                        "reopen_used": state.reopen_count > 0,
                        "stop_state": state.stop_state,
                    }
                    for item_id, state in sorted(self.store.items.items())
                ],
            }
        )
        self.assertEqual(self.store.revision_state_sha256(), expected)
        self.assertNotEqual(self.store.revision_state_sha256(), self.store.declared_store_digest)

    def test_change_ledger_has_zero_published_heads(self):
        self.assertEqual(self.store.change_events, [])


class TamperTest(unittest.TestCase):
    def setUp(self):
        self.root = pathlib.Path(tempfile.mkdtemp(prefix="aegis-records-"))

    def tearDown(self):
        shutil.rmtree(str(self.root), ignore_errors=True)

    def test_edited_prev_hash_breaks_the_chain(self):
        items = {ITEM: [_event("FX-0001"), _event("FX-0002", "STOP_STATE_SET", stop="OPEN")]}
        manifest = build_store(self.root, items)
        path = self.root / records_store_dir() / "items" / "fixture-0001.jsonl"
        lines = path.read_bytes().split(b"\n")
        payload = json.loads(lines[0].decode("utf-8"))
        payload["recorded_by"] = "someone-else"
        lines[0] = canonical.dumps(payload).encode("utf-8")
        path.write_bytes(b"\n".join(lines))
        store = records.load_store(self.root)
        details = " ".join(issue.detail for issue in store.issues)
        self.assertIn("hash chain", details)
        self.assertTrue(any(issue.code == "STATE_TAMPER_SUSPECTED" for issue in store.issues))

    def test_manifest_bytes_mismatch_is_tamper(self):
        items = {ITEM: [_event("FX-0001"), _event("FX-0002", "STOP_STATE_SET", stop="OPEN")]}
        manifest = build_store(self.root, items)
        manifest["files"][0]["bytes"] = manifest["files"][0]["bytes"] + 1
        path = self.root / records_store_dir() / "manifest.json"
        path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
        store = records.load_store(self.root)
        self.assertTrue(any("bytes mismatch" in issue.detail for issue in store.issues))

    def test_removed_line_is_refused(self):
        items = {ITEM: [_event("FX-0001"), _event("FX-0002", "STOP_STATE_SET", stop="OPEN")]}
        build_store(self.root, items)
        path = self.root / records_store_dir() / "items" / "fixture-0001.jsonl"
        path.write_bytes(path.read_bytes().split(b"\n")[0] + b"\n")
        store = records.load_store(self.root)
        self.assertTrue(store.issues)

    def test_unlisted_record_file_is_tamper(self):
        items = {ITEM: [_event("FX-0001"), _event("FX-0002", "STOP_STATE_SET", stop="OPEN")]}
        build_store(self.root, items)
        extra = self.root / records_store_dir() / "items" / "extra.jsonl"
        extra.write_text("{}\n", encoding="utf-8")
        store = records.load_store(self.root)
        self.assertTrue(any("not listed" in issue.detail for issue in store.issues))

    def test_second_counted_reopen_is_refused(self):
        items = {
            ITEM: [
                _event("FX-0001"),
                _event("FX-0002", "REOPEN_COUNTED", reopen=True),
                _event("FX-0003", "REOPEN_COUNTED", reopen=True),
                _event("FX-0004", "STOP_STATE_SET", stop="OPEN"),
            ]
        }
        build_store(self.root, items)
        store = records.load_store(self.root)
        self.assertTrue(any("second counted reopen" in issue.detail for issue in store.issues))

    def test_decreased_revision_count_below_binding_is_tamper(self):
        items = {ITEM: [_event("FX-0001"), _event("FX-0002", "STOP_STATE_SET", stop="OPEN")]}
        manifest = build_store(self.root, items)
        manifest["derived_counts_at_binding"]["items"][0]["revision_count"] = 3
        digest_files = [
            {key: entry[key] for key in ("path", "bytes", "sha256", "event_count", "id", "kind")}
            for entry in sorted(manifest["files"], key=lambda entry: entry["path"])
        ]
        manifest["store_digest"] = canonical.digest(
            {
                "schema_version": "aegis.revision-store/v1",
                "files": digest_files,
                "derived_counts_at_binding": manifest["derived_counts_at_binding"],
            }
        )
        (self.root / records_store_dir() / "manifest.json").write_text(
            json.dumps(manifest, indent=2) + "\n", encoding="utf-8"
        )
        store = records.load_store(self.root)
        self.assertTrue(any("decreased" in issue.detail for issue in store.issues))

    def test_bound_stop_state_mismatch_is_tamper(self):
        items = {ITEM: [_event("FX-0001"), _event("FX-0002", "STOP_STATE_SET", stop="OPEN")]}
        manifest = build_store(self.root, items)
        manifest["derived_counts_at_binding"]["items"][0]["stop_state"] = "CLOSED"
        write_manifest(self.root, rebind(manifest))
        store = records.load_store(self.root)
        self.assertTrue(any("stop_state" in issue.detail and "disagrees" in issue.detail for issue in store.issues))

    def test_bound_reopen_decrease_is_tamper(self):
        items = {ITEM: [_event("FX-0001"), _event("FX-0002", "STOP_STATE_SET", stop="OPEN")]}
        manifest = build_store(self.root, items)
        manifest["derived_counts_at_binding"]["items"][0]["reopen_used"] = True
        write_manifest(self.root, rebind(manifest))
        store = records.load_store(self.root)
        self.assertTrue(any("reopen_used" in issue.detail and "decreased" in issue.detail for issue in store.issues))

    def test_appended_counted_reopen_is_not_a_decrease(self):
        items = {
            ITEM: [
                _event("FX-0001"),
                _event("FX-0002", "REOPEN_COUNTED", reopen=True),
                _event("FX-0003", "STOP_STATE_SET", stop="OPEN"),
            ]
        }
        manifest = build_store(self.root, items)
        self.assertTrue(manifest["derived_counts_at_binding"]["items"][0]["reopen_used"])
        # The manifest bound no reopen before the (single) counted reopen was
        # appended: a legitimate append, never a tamper finding.
        manifest["derived_counts_at_binding"]["items"][0]["reopen_used"] = False
        write_manifest(self.root, rebind(manifest))
        store = records.load_store(self.root)
        self.assertEqual(store.issues, [])
        self.assertEqual(store.items[ITEM].reopen_count, 1)

    def test_bound_review_head_count_above_the_ledger_is_tamper(self):
        items = {ITEM: [_event("FX-0001"), _event("FX-0002", "STOP_STATE_SET", stop="OPEN")]}
        manifest = build_store(self.root, items, ledger=[ledger_event("1" * 40)])
        manifest["derived_counts_at_binding"]["review_heads"]["used"] = 3
        write_manifest(self.root, rebind(manifest))
        store = records.load_store(self.root)
        self.assertTrue(
            any("review-head count decreased" in issue.detail for issue in store.issues)
        )

    def test_appended_ledger_head_is_not_a_review_head_decrease(self):
        items = {ITEM: [_event("FX-0001"), _event("FX-0002", "STOP_STATE_SET", stop="OPEN")]}
        manifest = build_store(
            self.root, items, ledger=[ledger_event("1" * 40), ledger_event("2" * 40, "RESYNC")]
        )
        # Bound before the second head was published: derived 2 >= bound 1 is a
        # legitimate append, not a decrease.
        manifest["derived_counts_at_binding"]["review_heads"]["used"] = 1
        write_manifest(self.root, rebind(manifest))
        store = records.load_store(self.root)
        self.assertEqual(store.issues, [])

    def test_derived_item_missing_from_the_binding_is_tamper(self):
        items = {ITEM: [_event("FX-0001"), _event("FX-0002", "STOP_STATE_SET", stop="OPEN")]}
        manifest = build_store(self.root, items)
        manifest["derived_counts_at_binding"]["items"] = []
        write_manifest(self.root, rebind(manifest))
        store = records.load_store(self.root)
        self.assertTrue(any("is not bound in the manifest" in issue.detail for issue in store.issues))

    def test_manifest_file_order_does_not_change_the_digest(self):
        items = {ITEM: [_event("FX-0001"), _event("FX-0002", "STOP_STATE_SET", stop="OPEN")]}
        build_store(self.root, items)
        first = records.load_store(self.root).recomputed_store_digest
        build_store(self.root, items, reverse_manifest_files=True)
        second = records.load_store(self.root)
        self.assertEqual(second.issues, [])
        self.assertEqual(first, second.recomputed_store_digest)


class AppendOnlyPrefixTest(unittest.TestCase):
    def setUp(self):
        self.root = pathlib.Path(tempfile.mkdtemp(prefix="aegis-prefix-"))
        self.git("init", "-b", "main")
        self.git("config", "user.email", "fixture@example.invalid")
        self.git("config", "user.name", "Fixture Holder")
        self.git("config", "core.autocrlf", "false")

    def tearDown(self):
        shutil.rmtree(str(self.root), ignore_errors=True)

    def git(self, *args):
        completed = subprocess.run(
            ["git", "-C", str(self.root)] + list(args), capture_output=True, text=True, check=False
        )
        self.assertEqual(completed.returncode, 0, completed.stderr)
        return completed.stdout

    def test_appended_file_passes_and_rewritten_prefix_fails(self):
        items = {ITEM: [_event("FX-0001"), _event("FX-0002", "STOP_STATE_SET", stop="OPEN")]}
        build_store(self.root, items)
        self.git("add", "-A")
        self.git("commit", "-m", "base store")
        self.git("update-ref", "refs/remotes/origin/main", "HEAD")
        self.git("switch", "-c", "feature")

        base = records.load_store(self.root, base_ref="origin/main")
        self.assertEqual(base.issues, [])
        self.assertEqual(
            base.prefix_checks["items/fixture-0001.jsonl"], "APPEND_ONLY_OK"
        )

        appended = {
            ITEM: [
                _event("FX-0001"),
                _event("FX-0002", "STOP_STATE_SET", stop="OPEN"),
                _event("FX-0003"),
            ]
        }
        build_store(self.root, appended)
        appended_store = records.load_store(self.root, base_ref="origin/main")
        self.assertEqual(appended_store.issues, [])
        self.assertEqual(appended_store.items[ITEM].revision_count, 2)

        path = self.root / records_store_dir() / "items" / "fixture-0001.jsonl"
        lines = path.read_bytes().split(b"\n")
        payload = json.loads(lines[0].decode("utf-8"))
        payload["recorded_by"] = "rewritten"
        lines[0] = canonical.dumps(payload).encode("utf-8")
        path.write_bytes(b"\n".join(lines))
        rewritten = records.load_store(self.root, base_ref="origin/main")
        self.assertEqual(rewritten.prefix_checks["items/fixture-0001.jsonl"], "PREFIX_VIOLATION")
        self.assertTrue(any("append-only prefix" in issue.detail for issue in rewritten.issues))

    def test_whole_file_deletion_is_detected(self):
        items = {ITEM: [_event("FX-0001"), _event("FX-0002", "STOP_STATE_SET", stop="OPEN")]}
        build_store(self.root, items)
        self.git("add", "-A")
        self.git("commit", "-m", "base store")
        self.git("update-ref", "refs/remotes/origin/main", "HEAD")
        self.git("switch", "-c", "feature")

        item_path = self.root / records_store_dir() / "items" / "fixture-0001.jsonl"
        item_path.unlink()
        build_store(self.root, {})
        deleted = records.load_store(self.root, base_ref="origin/main")
        self.assertIn("items/fixture-0001.jsonl", deleted.prefix_checks)
        self.assertEqual(deleted.prefix_checks["items/fixture-0001.jsonl"], "BASE_FILE_MISSING")
        self.assertTrue(any("whole-file deletion" in issue.detail for issue in deleted.issues))


def _head(seq, head_sha, kind="INITIAL"):
    return {"seq": seq, "head_sha": head_sha, "kind": kind, "published_at": "2026-11-10T18:00:00Z"}


def _mirror(heads):
    """The exact change-ledger mirror the export requires (A10)."""

    return [
        {
            "seq": head["seq"],
            "head_sha": head["head_sha"],
            "kind": head["kind"],
            "exception_ref": None,
            "counted_at": head["published_at"],
            "authority_ref": {
                "authority_kind": "REGISTER_ENTRY",
                "authority_ref_id": "APR-FIXTURE-C1-0001",
                "holder_role": "programme-lead",
                "holder_identity_ref": None,
            },
        }
        for head in heads
        if head["head_sha"] != HEAD
    ]


class ReviewHeadBudgetTest(unittest.TestCase):
    def test_boundaries_zero_to_three(self):
        cases = [
            ([_head(1, HEAD)], 0, 1),
            ([_head(1, EXPORT_HEAD_1), _head(2, HEAD)], 1, 2),
            ([_head(1, EXPORT_HEAD_1), _head(2, EXPORT_HEAD_2), _head(3, HEAD)], 2, 3),
            (
                [
                    _head(1, EXPORT_HEAD_1),
                    _head(2, EXPORT_HEAD_2),
                    _head(3, EXPORT_HEAD_3),
                    _head(4, HEAD, "FINAL_BLOCKING_FIX"),
                ],
                3,
                4,
            ),
        ]
        for heads, used, ordinal in cases:
            result = records.derive_review_heads(_mirror(heads), heads, HEAD)
            self.assertEqual(result.used, used)
            self.assertEqual(result.ordinal, ordinal)
            self.assertEqual(result.issues, [])

    def test_resync_and_fix_heads_count(self):
        heads = [
            _head(1, EXPORT_HEAD_1),
            _head(2, EXPORT_HEAD_2, "RESYNC"),
            _head(3, EXPORT_HEAD_3, "BATCHED_BLOCKING_FIX"),
            _head(4, HEAD, "FINAL_BLOCKING_FIX"),
        ]
        self.assertEqual(records.derive_review_heads(_mirror(heads), heads, HEAD).used, 3)

    def test_duplicate_head_and_bad_ordinal_are_refused(self):
        heads = [_head(1, EXPORT_HEAD_1), _head(2, EXPORT_HEAD_1), _head(3, HEAD)]
        result = records.derive_review_heads(_mirror(heads), heads, HEAD)
        self.assertTrue(any("duplicate" in issue.detail for issue in result.issues))
        bad_ordinal = [_head(2, EXPORT_HEAD_1), _head(3, HEAD)]
        result = records.derive_review_heads(_mirror(bad_ordinal), bad_ordinal, HEAD)
        self.assertTrue(any("contiguous" in issue.detail for issue in result.issues))

    def test_candidate_must_be_last(self):
        heads = [_head(1, HEAD), _head(2, EXPORT_HEAD_1)]
        result = records.derive_review_heads(_mirror(heads), heads, HEAD)
        self.assertTrue(any("not the last" in issue.detail for issue in result.issues))

    def test_ledger_must_mirror_every_published_head_exactly(self):
        heads = [_head(1, EXPORT_HEAD_1), _head(2, EXPORT_HEAD_2), _head(3, HEAD)]
        mirror = _mirror(heads)
        ok = records.derive_review_heads(mirror, heads, HEAD)
        self.assertEqual(ok.issues, [])
        self.assertEqual(ok.ledger_count, 2)

    def test_truncated_ledger_is_tamper_not_a_mirror(self):
        # The previous behaviour accepted 1-of-2 as a consistent mirror; a
        # truncated ledger undercounts the published-head budget and is tamper.
        heads = [_head(1, EXPORT_HEAD_1), _head(2, EXPORT_HEAD_2), _head(3, HEAD)]
        truncated = _mirror(heads)[:1]
        result = records.derive_review_heads(truncated, heads, HEAD)
        self.assertTrue(any("disagrees" in issue.detail for issue in result.issues))
        self.assertTrue(any("exactly" in issue.detail for issue in result.issues))

    def test_empty_ledger_is_tamper_when_heads_were_published(self):
        heads = [_head(1, EXPORT_HEAD_1), _head(2, HEAD)]
        result = records.derive_review_heads([], heads, HEAD)
        self.assertTrue(any("disagrees" in issue.detail for issue in result.issues))

    def test_disagreeing_ledger_head_is_tamper(self):
        heads = [_head(1, EXPORT_HEAD_1), _head(2, EXPORT_HEAD_2), _head(3, HEAD)]
        disagreeing = _mirror(heads)
        disagreeing[0]["head_sha"] = EXPORT_HEAD_3
        result = records.derive_review_heads(disagreeing, heads, HEAD)
        self.assertTrue(any("disagrees" in issue.detail for issue in result.issues))

    def test_ledger_cannot_record_the_candidate(self):
        heads = [_head(1, HEAD)]
        ledger = [{"seq": 1, "head_sha": HEAD, "kind": "INITIAL", "exception_ref": None}]
        result = records.derive_review_heads(ledger, heads, HEAD)
        self.assertTrue(any("candidate head" in issue.detail for issue in result.issues))


REGISTER_TEXT = (
    "# Register (fixture text, grants nothing)\n"
    "\n"
    "| Entry | Status | Scope |\n"
    "| --- | --- | --- |\n"
    "| APR-TEST-0001 | ACTIVE | repo=example-org/example-repo; change_id=42; head_sha="
    + "a" * 40
    + "; merge_target_ref=refs/heads/main |\n"
    "| APR-TEST-0002 | ACTIVE | fixture repo/change/head only |\n"
    "| APR-TEST-0009 | INACTIVE | repo=example-org/example-repo; change_id=42; head_sha="
    + "a" * 40
    + "; merge_target_ref=refs/heads/main |\n"
    "\n"
    "### AEGIS-APR-0100: A heading entry\n"
    "\n"
    "- **Event:** GRANT\n"
    "- **Status at recording:** **ACTIVE - recorded, not granted.**\n"
    "- **Gate scope:** repo=example-org/example-repo; change_id=7; head_sha="
    + "b" * 40
    + "; merge_target_ref=refs/heads/main\n"
    "\n"
    "### AEGIS-APR-0101: Revocation of AEGIS-APR-0100\n"
    "\n"
    "- **Event:** REVOKED - the grant named above is withdrawn.\n"
)


class RegisterResolutionTest(unittest.TestCase):
    """B5: the G group and exceptions are resolved from the register bytes."""

    def test_table_row_resolves_status_and_scope(self):
        entry = records.resolve_register_entry(REGISTER_TEXT, "APR-TEST-0001")
        self.assertIsNotNone(entry)
        self.assertEqual(entry.status, "ACTIVE")
        self.assertTrue(entry.scope_present)
        self.assertTrue(entry.covers("example-org/example-repo", 42, "a" * 40, "refs/heads/main"))
        self.assertFalse(entry.covers("example-org/example-repo", 42, "f" * 40, "refs/heads/main"))
        self.assertFalse(entry.covers("example-org/other-repo", 42, "a" * 40, "refs/heads/main"))

    def test_heading_block_resolves_status_and_scope(self):
        entry = records.resolve_register_entry(REGISTER_TEXT, "AEGIS-APR-0100")
        self.assertIsNotNone(entry)
        self.assertEqual(entry.status, "REVOKED")
        self.assertFalse(entry.scope_present)

    def test_a_later_lifecycle_event_overrides_status_at_recording(self):
        entry = records.resolve_register_entry(REGISTER_TEXT, "AEGIS-APR-0100")
        self.assertEqual(entry.status, "REVOKED")

    def test_entry_without_a_machine_checkable_scope(self):
        entry = records.resolve_register_entry(REGISTER_TEXT, "APR-TEST-0002")
        self.assertIsNotNone(entry)
        self.assertEqual(entry.status, "ACTIVE")
        self.assertFalse(entry.scope_present)
        self.assertFalse(entry.covers("example-org/example-repo", 42, "a" * 40, "refs/heads/main"))

    def test_status_is_matched_as_a_whole_token(self):
        entry = records.resolve_register_entry(REGISTER_TEXT, "APR-TEST-0009")
        self.assertIsNotNone(entry)
        self.assertEqual(entry.status, "UNKNOWN")

    def test_absent_entry_resolves_to_none(self):
        self.assertIsNone(records.resolve_register_entry(REGISTER_TEXT, "APR-TEST-0404"))
        self.assertIsNone(records.resolve_register_entry(REGISTER_TEXT, ""))

    def test_negated_or_unknown_status_is_not_active(self):
        for text in ("NOT ACTIVE", "NOT-ACTIVE", "INACTIVE", "unknown", "UNKNOWN STATUS", "NONE"):
            self.assertEqual(records._status_token(text), "", text)

    def test_scope_parser_keeps_only_known_keys(self):
        self.assertEqual(
            records.parse_gate_scope(
                "repo=o/r; change_id=1; head_sha=" + "a" * 40 + "; merge_target_ref=refs/heads/main; x=1"
            ),
            {
                "repo": "o/r",
                "change_id": "1",
                "head_sha": "a" * 40,
                "merge_target_ref": "refs/heads/main",
            },
        )


class GitBaseRequiredTest(unittest.TestCase):
    """B2: the append-only check is never skipped when no base resolves."""

    def setUp(self):
        self.root = pathlib.Path(tempfile.mkdtemp(prefix="aegis-nobase-"))

    def tearDown(self):
        shutil.rmtree(str(self.root), ignore_errors=True)

    def test_unresolvable_base_is_a_required_input_issue(self):
        items = {ITEM: [_event("FX-0001"), _event("FX-0002", "STOP_STATE_SET", stop="OPEN")]}
        build_store(self.root, items)
        # Rename, not delete: Windows refuses to unlink git's read-only objects.
        (self.root / ".git").rename(self.root / ".git-disabled")
        store = records.load_store(self.root, base_ref="origin/main")
        self.assertEqual(store.prefix_checks["__status__"], "GIT_BASE_UNRESOLVED")
        self.assertTrue(
            any(
                issue.code == "REQUIRED_INPUT_UNAVAILABLE" and "no git base" in issue.detail
                for issue in store.issues
            )
        )

    def test_unknown_base_ref_is_a_required_input_issue(self):
        items = {ITEM: [_event("FX-0001"), _event("FX-0002", "STOP_STATE_SET", stop="OPEN")]}
        build_store(self.root, items)
        store = records.load_store(self.root, base_ref="refs/heads/does-not-exist")
        self.assertEqual(store.prefix_checks["__status__"], "GIT_BASE_UNRESOLVED")
        self.assertTrue(any(issue.code == "REQUIRED_INPUT_UNAVAILABLE" for issue in store.issues))


class DigestDeterminismTest(unittest.TestCase):
    def test_revision_state_hash_changes_with_counts(self):
        def state(count, stop):
            return canonical.digest(
                {
                    "schema_version": "aegis.revision-state/v1",
                    "items": [
                        {"item_id": ITEM, "revision_count": count, "reopen_used": False, "stop_state": stop}
                    ],
                }
            )

        self.assertNotEqual(state(5, "OPEN"), state(6, "OPEN"))
        self.assertNotEqual(state(5, "OPEN"), state(5, "CLOSED"))
        self.assertEqual(state(5, "OPEN"), state(5, "OPEN"))


if __name__ == "__main__":
    unittest.main()
