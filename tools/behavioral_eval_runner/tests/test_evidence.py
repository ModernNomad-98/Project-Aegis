"""Two-stage evidence finalization: verification, detached marker,
circularity and corruption rejection (areas 31–34)."""

from __future__ import annotations

import json
import os
import tempfile
import unittest
from typing import Any

from tools.behavioral_eval_runner import RUNNER_VERSION, SCHEMA_VERSION
from tools.behavioral_eval_runner.canonical import canonical_bytes, sha256_hex
from tools.behavioral_eval_runner.errors import CircularEvidenceError, EvidenceError, EvidenceIntegrityError
from tools.behavioral_eval_runner.evidence import (
    _POSIX_EVIDENCE_ATOMIC,
    ArtifactMetadata,
    EvidenceArtifact,
    EvidenceWriter,
    FINAL_MANIFEST_NAME,
    FINAL_REPORT_NAME,
    INPUT_MANIFEST_NAME,
    JudgeInputGate,
    MARKER_NAME,
    verify_final_bundle,
    verify_input_evidence,
    verify_local_bundle,
)
from tools.behavioral_eval_runner.models import (
    default_unselected_aggregate,
    planned_unrun_attempt,
)
from tools.behavioral_eval_runner.tests.helpers import make_case_uid

RUN = "run-ev"


def _artifacts() -> list[EvidenceArtifact]:
    return [
        EvidenceArtifact("transcripts/attempt-1.txt", b"synthetic transcript"),
        EvidenceArtifact("audit/sandbox-log.txt", b"synthetic audit log"),
    ]


class _BundleCase(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.root = self._tmp.name
        self.writer = EvidenceWriter(self.root, RUN)

    def _report(self, input_sha: str) -> dict:
        return {
            "report_kind": "behavioral_eval_run_report",
            "schema_version": SCHEMA_VERSION,
            "runner_version": RUNNER_VERSION,
            "run_id": RUN,
            "run_evidence_binding": {"input_evidence_manifest_sha256": input_sha},
            "aggregates": [],
        }

    def _full_bundle(self):
        stage_a = self.writer.finalize_input_evidence(_artifacts())
        stage_b = self.writer.finalize_final_bundle(
            final_report=self._report(stage_a.input_evidence_manifest_sha256),
            artifacts=[EvidenceArtifact("judge/none.txt", b"no judge in WP-2B-1")],
            input_manifest_sha256=stage_a.input_evidence_manifest_sha256,
            final_status="OFFLINE_DEMONSTRATION",
        )
        return stage_a, stage_b

    def _rewrite_json(self, name: str, payload: dict) -> str:
        content = canonical_bytes(payload)
        with open(os.path.join(self.root, name), "wb") as fh:
            fh.write(content)
        return sha256_hex(content)

    def _mutate_final_component(self, name: str, field: str, value: Any) -> None:
        """Keep every outer hash valid so version rejection is the tested boundary."""
        def read(component: str) -> dict:
            with open(os.path.join(self.root, component), encoding="utf-8") as fh:
                return json.load(fh)

        component = read(name)
        if value is None:
            component.pop(field)
        else:
            component[field] = value
        component_sha = self._rewrite_json(name, component)
        if name == FINAL_REPORT_NAME:
            manifest = read(FINAL_MANIFEST_NAME)
            for entry in manifest["artifacts"]:
                if entry["path"] == FINAL_REPORT_NAME:
                    entry["sha256"] = component_sha
                    entry["bytes"] = len(canonical_bytes(component))
            manifest_sha = self._rewrite_json(FINAL_MANIFEST_NAME, manifest)
            marker = read(MARKER_NAME)
            marker["final_report_sha256"] = component_sha
            marker["final_evidence_manifest_sha256"] = manifest_sha
            self._rewrite_json(MARKER_NAME, marker)
        elif name == FINAL_MANIFEST_NAME:
            marker = read(MARKER_NAME)
            marker["final_evidence_manifest_sha256"] = component_sha
            self._rewrite_json(MARKER_NAME, marker)


class TestStageA(_BundleCase):
    def test_legacy_serialized_hashes_match_pre_policy_writer(self) -> None:
        """Golden bytes captured from the exact pre-policy grant base."""
        fixed = "2030-01-01T00:00:00Z"
        writer = EvidenceWriter(self.root, "legacy-regression")
        stage_a = writer.finalize_input_evidence([
            EvidenceArtifact("input.txt", b"synthetic", ArtifactMetadata(created_at=fixed))
        ])
        report = {
            "report_kind": "behavioral_eval_run_report",
            "schema_version": SCHEMA_VERSION,
            "runner_version": RUNNER_VERSION,
            "run_id": "legacy-regression",
            "run_evidence_binding": {
                "input_evidence_manifest_sha256": stage_a.input_evidence_manifest_sha256
            },
            "aggregates": [],
        }
        writer.finalize_final_bundle(
            report,
            [EvidenceArtifact("output.txt", b"synthetic output", ArtifactMetadata(created_at=fixed))],
            stage_a.input_evidence_manifest_sha256,
            "OFFLINE",
            finalized_at=fixed,
        )
        expected = {
            INPUT_MANIFEST_NAME: "d6e8783139dfccbccc54ce9bca9be21a6a88dc7bc2f5c19301f87fe57535b2b8",
            FINAL_MANIFEST_NAME: "303e9256803ed21fec7a31d654c6c615533e1392e18feaec8ac19237339cdcbe",
            MARKER_NAME: "988457c4f55b557c249d3a25f0acdf05d84530afacb49e67fbb0cfcee7d95970",
        }
        for name, pinned_sha in expected.items():
            with self.subTest(name=name), open(os.path.join(self.root, name), "rb") as handle:
                self.assertEqual(sha256_hex(handle.read()), pinned_sha)
        self.assertEqual(
            verify_local_bundle(self.root)["input_evidence_manifest_sha256"],
            stage_a.input_evidence_manifest_sha256,
        )
        with self.assertRaises(EvidenceIntegrityError):
            verify_local_bundle(self.root, require_policy=True)

    def test_input_manifest_requires_supported_version(self) -> None:
        self.writer.finalize_input_evidence(_artifacts())
        for version in (None, "future-wp2b1"):
            with self.subTest(version=version):
                with open(os.path.join(self.root, INPUT_MANIFEST_NAME), encoding="utf-8") as fh:
                    manifest = json.load(fh)
                if version is None:
                    manifest.pop("schema_version", None)
                else:
                    manifest["schema_version"] = version
                self._rewrite_json(INPUT_MANIFEST_NAME, manifest)
                with self.assertRaises(EvidenceIntegrityError):
                    verify_input_evidence(self.root)

    def test_finalize_and_verify(self) -> None:
        bundle = self.writer.finalize_input_evidence(_artifacts())
        self.assertEqual(bundle.artifact_count, 2)
        self.assertEqual(
            verify_input_evidence(self.root), bundle.input_evidence_manifest_sha256
        )

    def test_manifest_excludes_itself(self) -> None:
        self.writer.finalize_input_evidence(_artifacts())
        with open(os.path.join(self.root, INPUT_MANIFEST_NAME), encoding="utf-8") as fh:
            manifest = json.load(fh)
        paths = [entry["path"] for entry in manifest["artifacts"]]
        self.assertNotIn(INPUT_MANIFEST_NAME, paths)

    def test_metadata_on_every_artifact(self) -> None:
        self.writer.finalize_input_evidence(_artifacts())
        with open(os.path.join(self.root, INPUT_MANIFEST_NAME), encoding="utf-8") as fh:
            manifest = json.load(fh)
        for entry in manifest["artifacts"]:
            for key in (
                "retention_class",
                "sensitivity",
                "redaction_state",
                "created_at",
                "expiration_at",
                "access_policy_ref",
                "preserve_on_failure",
            ):
                self.assertIn(key, entry)

    def test_corrupted_artifact_fails_closed(self) -> None:
        self.writer.finalize_input_evidence(_artifacts())
        target = os.path.join(self.root, "transcripts", "attempt-1.txt")
        with open(target, "ab") as fh:
            fh.write(b" TAMPERED")
        with self.assertRaises(EvidenceIntegrityError) as ctx:
            verify_input_evidence(self.root)
        self.assertEqual(ctx.exception.reason_code, "EVIDENCE_INTEGRITY_FAILURE")

    def test_truncated_artifact_fails_closed(self) -> None:
        self.writer.finalize_input_evidence(_artifacts())
        target = os.path.join(self.root, "audit", "sandbox-log.txt")
        with open(target, "rb") as fh:
            content = fh.read()
        with open(target, "wb") as fh:
            fh.write(content[:-3])
        with self.assertRaises(EvidenceIntegrityError):
            verify_input_evidence(self.root)

    def test_missing_artifact_fails_closed(self) -> None:
        self.writer.finalize_input_evidence(_artifacts())
        os.remove(os.path.join(self.root, "transcripts", "attempt-1.txt"))
        with self.assertRaises(EvidenceIntegrityError):
            verify_input_evidence(self.root)

    def test_judge_gate_requires_verification_first(self) -> None:
        self.writer.finalize_input_evidence(_artifacts())
        gate = JudgeInputGate(self.root)
        with self.assertRaises(EvidenceIntegrityError):
            gate.read_artifact("transcripts/attempt-1.txt")
        gate.verify()
        self.assertEqual(
            gate.read_artifact("transcripts/attempt-1.txt"), b"synthetic transcript"
        )

    def test_judge_gate_fails_closed_on_tamper(self) -> None:
        self.writer.finalize_input_evidence(_artifacts())
        with open(
            os.path.join(self.root, "transcripts", "attempt-1.txt"), "ab"
        ) as fh:
            fh.write(b"x")
        gate = JudgeInputGate(self.root)
        with self.assertRaises(EvidenceIntegrityError):
            gate.verify()
        self.assertFalse(gate.verified)

    def test_reserved_and_traversal_paths_refused(self) -> None:
        for path in (INPUT_MANIFEST_NAME, MARKER_NAME, "../escape.txt", "a/../b"):
            with self.assertRaises(EvidenceError):
                self.writer.finalize_input_evidence(
                    [EvidenceArtifact(path, b"x")]
                )


class TestStageB(_BundleCase):
    def test_nested_report_records_require_supported_versions(self) -> None:
        uid = make_case_uid()
        attempt = planned_unrun_attempt(RUN, uid, 1).to_dict()
        attempt["schema_version"] = "future-wp2b1"
        aggregate = default_unselected_aggregate(uid).to_dict()
        del aggregate["schema_version"]
        examples = {
            "attempts": [attempt],
            "aggregates": [aggregate],
        }
        for field, value in examples.items():
            with self.subTest(field=field), tempfile.TemporaryDirectory() as root:
                original_root, original_writer = self.root, self.writer
                try:
                    self.root, self.writer = root, EvidenceWriter(root, RUN)
                    self._full_bundle()
                    self._mutate_final_component(FINAL_REPORT_NAME, field, value)
                    with self.assertRaises(EvidenceIntegrityError):
                        verify_final_bundle(self.root)
                finally:
                    self.root, self.writer = original_root, original_writer

    def test_final_report_requires_runner_version_with_valid_hashes(self) -> None:
        self._full_bundle()
        self._mutate_final_component(FINAL_REPORT_NAME, "runner_version", None)
        with self.assertRaises(EvidenceIntegrityError):
            verify_final_bundle(self.root)

    def test_final_components_require_supported_versions_with_valid_hashes(self) -> None:
        for name in (FINAL_MANIFEST_NAME, MARKER_NAME, FINAL_REPORT_NAME):
            for version in (None, "future-wp2b1"):
                with self.subTest(name=name, version=version):
                    with tempfile.TemporaryDirectory() as root:
                        original_root, original_writer = self.root, self.writer
                        try:
                            self.root, self.writer = root, EvidenceWriter(root, RUN)
                            self._full_bundle()
                            self._mutate_final_component(name, "schema_version", version)
                            with self.assertRaises(EvidenceIntegrityError):
                                verify_final_bundle(self.root)
                        finally:
                            self.root, self.writer = original_root, original_writer

    def test_detached_marker_binds_report_and_manifest(self) -> None:
        _stage_a, stage_b = self._full_bundle()
        result = verify_final_bundle(self.root)
        self.assertEqual(
            result["final_evidence_manifest_sha256"],
            stage_b.final_evidence_manifest_sha256,
        )
        self.assertEqual(result["final_report_sha256"], stage_b.final_report_sha256)

    def test_final_manifest_excludes_itself_and_marker(self) -> None:
        self._full_bundle()
        with open(os.path.join(self.root, FINAL_MANIFEST_NAME), encoding="utf-8") as fh:
            manifest = json.load(fh)
        paths = [entry["path"] for entry in manifest["artifacts"]]
        self.assertNotIn(FINAL_MANIFEST_NAME, paths)
        self.assertNotIn(MARKER_NAME, paths)
        self.assertIn(FINAL_REPORT_NAME, paths)

    def test_report_carries_input_hash_never_final_hash(self) -> None:
        stage_a, stage_b = self._full_bundle()
        with open(os.path.join(self.root, FINAL_REPORT_NAME), "rb") as fh:
            report_bytes = fh.read()
        self.assertIn(
            stage_a.input_evidence_manifest_sha256.encode("ascii"), report_bytes
        )
        self.assertNotIn(
            stage_b.final_evidence_manifest_sha256.encode("ascii"), report_bytes
        )

    def test_marker_contains_no_self_hash(self) -> None:
        _stage_a, stage_b = self._full_bundle()
        with open(os.path.join(self.root, MARKER_NAME), "rb") as fh:
            marker_bytes = fh.read()
        self.assertNotIn(
            stage_b.finalization_marker_sha256.encode("ascii"), marker_bytes
        )

    def test_report_with_final_hash_field_refused(self) -> None:
        stage_a = self.writer.finalize_input_evidence(_artifacts())
        report = self._report(stage_a.input_evidence_manifest_sha256)
        report["run_evidence_binding"]["final_report_sha256"] = "0" * 64
        with self.assertRaises(CircularEvidenceError):
            self.writer.finalize_final_bundle(
                report,
                [],
                stage_a.input_evidence_manifest_sha256,
                "X",
            )

    def test_report_without_binding_refused(self) -> None:
        stage_a = self.writer.finalize_input_evidence(_artifacts())
        with self.assertRaises(EvidenceError):
            self.writer.finalize_final_bundle(
                {"report_kind": "x"}, [], stage_a.input_evidence_manifest_sha256, "X"
            )

    def test_tampered_final_report_fails_closed(self) -> None:
        self._full_bundle()
        target = os.path.join(self.root, FINAL_REPORT_NAME)
        with open(target, "ab") as fh:
            fh.write(b" ")
        with self.assertRaises(EvidenceIntegrityError):
            verify_final_bundle(self.root)

    def test_missing_marker_never_trusted(self) -> None:
        self._full_bundle()
        os.remove(os.path.join(self.root, MARKER_NAME))
        with self.assertRaises(EvidenceIntegrityError):
            verify_final_bundle(self.root)

    def test_marker_manifest_mismatch_fails_closed(self) -> None:
        self._full_bundle()
        marker_path = os.path.join(self.root, MARKER_NAME)
        with open(marker_path, encoding="utf-8") as fh:
            marker = json.load(fh)
        marker["final_evidence_manifest_sha256"] = "f" * 64
        with open(marker_path, "w", encoding="utf-8") as fh:
            json.dump(marker, fh)
        with self.assertRaises(EvidenceIntegrityError):
            verify_final_bundle(self.root)

    def test_manifest_listing_marker_is_circular(self) -> None:
        self._full_bundle()
        manifest_path = os.path.join(self.root, FINAL_MANIFEST_NAME)
        with open(manifest_path, encoding="utf-8") as fh:
            manifest = json.load(fh)
        with open(os.path.join(self.root, MARKER_NAME), "rb") as fh:
            marker_bytes = fh.read()
        manifest["artifacts"].append(
            {
                "path": MARKER_NAME,
                "bytes": len(marker_bytes),
                "sha256": sha256_hex(marker_bytes),
                "sensitivity": "INTERNAL",
                "redaction_state": "sanitized_by_construction",
                "retention_class": "days_30",
                "created_at": "2026-08-12T00:00:00Z",
                "expiration_at": "2026-09-11T00:00:00Z",
                "access_policy_ref": "x",
                "preserve_on_failure": True,
            }
        )
        with open(manifest_path, "w", encoding="utf-8") as fh:
            json.dump(manifest, fh)
        with self.assertRaises(EvidenceIntegrityError):
            verify_final_bundle(self.root)

    def test_unfinalized_bundle_never_trusted(self) -> None:
        # Stage A only — no final manifest, no marker: rollups must refuse.
        self.writer.finalize_input_evidence(_artifacts())
        with self.assertRaises(EvidenceIntegrityError):
            verify_final_bundle(self.root)


# =============================================================== Round 3 §5
class TestEvidenceWriterTrustedRoot(unittest.TestCase):
    """§5: the evidence writer must anchor to a trusted root, refuse a symlink
    root, never write/replace outside it, and never claim fail-closed prevention
    on a platform where the atomic no-reparse guarantee is unavailable."""

    def test_atomic_write_refuses_symlink_root(self) -> None:
        from tools.behavioral_eval_runner.evidence import _atomic_write

        with tempfile.TemporaryDirectory() as root:
            outside = os.path.join(root, "outside")
            os.makedirs(outside)
            link_root = os.path.join(root, "linkroot")
            try:
                os.symlink(outside, link_root, target_is_directory=True)
            except (OSError, NotImplementedError):
                self.skipTest("symlink creation unavailable")
            with self.assertRaises(EvidenceError):
                _atomic_write(link_root, "escaped.json", b"{}")
            # The write must NOT have landed in the symlink target.
            self.assertFalse(os.path.exists(os.path.join(outside, "escaped.json")))

    def test_evidence_write_capability_non_baseline(self) -> None:
        from tools.behavioral_eval_runner.evidence import evidence_write_capability

        report = evidence_write_capability()
        self.assertEqual(report["baseline_status"], "NON_BASELINE")
        if os.name == "nt":
            self.assertEqual(report["implementation_state"], "UNAVAILABLE")
            self.assertEqual(report["root_anchor"], "UNTRUSTED_REALPATH_DERIVED")

    def test_dirfd_replace_probe_measures_not_assumes(self) -> None:
        """The gate must measure the runtime dir-fd replace capability; the
        static supports_dir_fd membership is only the documented fallback."""
        from tools.behavioral_eval_runner.evidence import (
            _dirfd_replace_probe,
            _dirfd_replace_supported,
        )

        if os.name == "posix" and _dirfd_replace_probe():
            # The 3.12/Ubuntu host class the defect was found on: the static
            # set omits os.replace but the real call succeeds.
            self.assertTrue(_dirfd_replace_supported())
            self.assertTrue(_POSIX_EVIDENCE_ATOMIC)
        else:
            # Windows, or POSIX without a working dir-fd replace: the gate
            # must never claim prevention it cannot run.
            self.assertFalse(_POSIX_EVIDENCE_ATOMIC)

    @unittest.skipUnless(
        _POSIX_EVIDENCE_ATOMIC,
        "dir-fd atomic evidence write is POSIX-only (UNRUN on Windows)",
    )
    def test_posix_parent_swap_fails_closed(self) -> None:  # pragma: no cover - POSIX only
        from unittest import mock

        from tools.behavioral_eval_runner.evidence import _atomic_write

        with tempfile.TemporaryDirectory() as root:
            dest = os.path.join(root, "evroot")
            os.makedirs(dest)
            outside = os.path.join(root, "outside")
            os.makedirs(outside)

            def swapping_mkdir(name, mode=0o777, *, dir_fd=None):
                os.symlink(outside, name, dir_fd=dir_fd)

            with mock.patch("os.mkdir", side_effect=swapping_mkdir):
                with self.assertRaises(EvidenceError):
                    _atomic_write(dest, "sub/escaped.json", b"{}")
            self.assertFalse(os.path.exists(os.path.join(outside, "escaped.json")))


def _dirfd_open_constructible() -> bool:
    """Can this host open a directory descriptor at all? Windows
    cannot - the honest disposition there is UNRUN (skip), and the operand
    oracle runs on the POSIX distro (AC7), never converted into a pass."""
    with tempfile.TemporaryDirectory() as tmp:
        probe_dir = os.path.join(tmp, "d")
        os.mkdir(probe_dir)
        try:
            fd = os.open(probe_dir,
                         os.O_RDONLY | getattr(os, "O_DIRECTORY", 0))
        except (NotImplementedError, OSError, AttributeError):
            return False
        os.close(fd)
        return True


def _replace_oracle(probe_fn) -> bool:
    """Run probe_fn while spying on os.replace. The oracle passes only when
    the recorded call used RELATIVE basename operands, DISTINCT src/dst
    directory descriptors, and — where the call succeeded — the observable
    descriptor-relative filesystem outcomes hold (destination exists with the
    exact payload; source absent). The probe's Boolean is never the
    evidence; the operands and outcomes are (dirfd-probe-repair AC2)."""
    from unittest import mock

    from tools.behavioral_eval_runner.evidence import _DIRFD_PROBE_PAYLOAD

    calls: list = []
    outcomes = {"checked": False, "ok": None}
    real_replace = os.replace
    real_open = os.open

    def plain_open(path, flags, *args, **kw):
        # A directory descriptor obtained WITHOUT O_DIRECTORY still IS a
        # directory descriptor, and plain O_RDONLY opens succeed on every
        # host — so the operand/outcome oracle exercises the replace call
        # itself even where O_DIRECTORY opens fail (Windows). The production
        # probe keeps its O_DIRECTORY opens, exercised without substitution
        # on the POSIX distro run (AC7). Extra positional args (tempfile's
        # internal os.open calls) pass through untouched.
        return real_open(path, flags & ~getattr(os, "O_DIRECTORY", 0),
                         *args, **kw)

    def spy(src, dst, **kw):
        calls.append((src, dst, dict(kw)))
        try:
            real_replace(src, dst, **kw)
            replaced = True
        except (NotImplementedError, OSError, AttributeError):
            replaced = False
        src_fd = kw.get("src_dir_fd")
        dst_fd = kw.get("dst_dir_fd")
        if replaced and src_fd is not None and dst_fd is not None:
            outcomes["checked"] = True
            fd = os.open("probe", os.O_RDONLY, dir_fd=dst_fd)
            try:
                payload_ok = os.read(fd, 4096) == _DIRFD_PROBE_PAYLOAD
            finally:
                os.close(fd)
            try:
                os.stat("probe", dir_fd=src_fd)
                src_ok = False
            except FileNotFoundError:
                src_ok = True
            outcomes["ok"] = payload_ok and src_ok

    with mock.patch("os.replace", side_effect=spy), \
            mock.patch("os.open", side_effect=plain_open):
        probe_fn()
    assert calls, "the probe never called os.replace"
    src_op, dst_op, kw = calls[0]
    if os.path.isabs(src_op) or os.path.isabs(dst_op):
        raise AssertionError(
            "probe passed ABSOLUTE operands - dir_fd is ignored for absolute "
            "paths, so the call did not exercise descriptor-relative "
            "replacement")
    if not src_op or not dst_op or os.sep in src_op or os.sep in dst_op:
        raise AssertionError("probe operands are not plain relative basenames")
    if kw.get("src_dir_fd") is None or kw.get("dst_dir_fd") is None:
        raise AssertionError("probe did not pass directory descriptors")
    if kw["src_dir_fd"] == kw["dst_dir_fd"]:
        raise AssertionError("probe passed the SAME descriptor for src and dst")
    if outcomes["checked"] and not outcomes["ok"]:
        raise AssertionError(
            "observable outcomes failed: destination content mismatch or "
            "source still present")
    return True


# ================================================== dirfd-probe-repair (D91-brief)
class TestDirfdProbeRepair(unittest.TestCase):
    """The repaired probe's contract: relative operands, distinct retained
    descriptors, verified observable outcomes, honest failure categories, and
    the static-first short circuit."""

    def test_oracle_rejects_old_absolute_probe_accepts_repair(self) -> None:
        if not _dirfd_open_constructible():
            self.skipTest(
                "directory descriptors not openable on this host - the "
                "operand oracle runs on the POSIX distro (AC7); UNRUN here, "
                "never a pass")
        from tools.behavioral_eval_runner.evidence import _dirfd_replace_probe

        # A scratch copy of the PRE-REPAIR probe (absolute operands,
        # unverified outcome) lives in this bounded fixture only - the
        # retained baseline and every other checkout are untouched.
        def old_probe_scratch() -> bool:
            fd_src = -1
            fd_dst = -1
            try:
                with tempfile.TemporaryDirectory() as tmp:
                    src_dir = os.path.join(tmp, "srcd")
                    dst_dir = os.path.join(tmp, "dstd")
                    os.mkdir(src_dir)
                    os.mkdir(dst_dir)
                    fd_src = os.open(src_dir, os.O_RDONLY | os.O_DIRECTORY)
                    fd_dst = os.open(dst_dir, os.O_RDONLY | os.O_DIRECTORY)
                    src = os.path.join(src_dir, "probe")
                    dst = os.path.join(dst_dir, "probe")
                    with open(src, "wb") as handle:
                        handle.write(b"probe")
                    os.replace(src, dst,
                               src_dir_fd=fd_src, dst_dir_fd=fd_dst)
                    return True
            except (NotImplementedError, OSError, AttributeError):
                return False
            finally:
                if fd_src >= 0:
                    os.close(fd_src)
                if fd_dst >= 0:
                    os.close(fd_dst)
            return False

        with self.assertRaises(AssertionError) as ctx:
            _replace_oracle(old_probe_scratch)
        self.assertIn("ABSOLUTE", str(ctx.exception))
        self.assertTrue(_replace_oracle(_dirfd_replace_probe))

    def test_probe_false_when_replace_moves_nothing(self) -> None:
        from unittest import mock

        import tools.behavioral_eval_runner.evidence as ev

        fd_counter = {"n": 0}
        real_open = os.open
        real_close = os.close

        def noop(src, dst, **kw):
            return None

        def fake_open(path, flags, *args, **kw):
            # The distinguishing property (SD-E round 2): the probe's OWN two
            # directory opens carry NO dir_fd kwarg, while the ambient
            # cleanup opens (POSIX shutil.rmtree walking the fixture)
            # DO carry dir_fd. Count only probe-class opens; pass everything
            # else through untouched so the fixture is really created.
            if os.path.basename(os.fspath(path)) in ("srcd", "dstd") \
                    and "dir_fd" not in kw:
                fd_counter["n"] += 1
                return 1000 + fd_counter["n"]
            return real_open(path, flags, *args, **kw)

        def close_fake_only(fd):
            if 1000 <= fd < 5000:
                return None
            return real_close(fd)

        with mock.patch.object(ev.os, "replace", side_effect=noop), \
                mock.patch.object(ev.os, "open", side_effect=fake_open), \
                mock.patch.object(ev.os, "close",
                                  side_effect=close_fake_only):
            # The noop replace moves nothing: the destination file never
            # appears, so the observable outcome fails and the probe returns
            # False - the intended mechanism, not a fixture failure.
            self.assertFalse(ev._dirfd_replace_probe())
            # Exactly 2 probe-class opens (no dir_fd kwarg): the probe's own
            # source-directory and destination-directory opens. Ambient
            # cleanup opens carry dir_fd and are excluded by the
            # discriminator, not guessed away.
            self.assertEqual(fd_counter["n"], 2)

    def test_probe_false_when_replace_ignores_descriptors(self) -> None:
        from unittest import mock

        import tools.behavioral_eval_runner.evidence as ev

        def cwd_only(src, dst, **kw):
            # Accepts the descriptor arguments but ignores them: the relative
            # basenames would resolve against the process cwd where the
            # fixture does not exist, so the descriptor-relative destination
            # never appears - an observable outcome, not a Boolean. No real
            # rename is attempted at all.
            return None

        fd_counter = {"n": 0}
        real_open = os.open
        real_close = os.close

        def fake_open(path, flags, *args, **kw):
            # Same discriminator as the moves-nothing sibling: only the
            # probe's own two directory opens (no dir_fd kwarg) count;
            # ambient cleanup opens carry dir_fd and pass through.
            if os.path.basename(os.fspath(path)) in ("srcd", "dstd") \
                    and "dir_fd" not in kw:
                fd_counter["n"] += 1
                return 2000 + fd_counter["n"]
            return real_open(path, flags, *args, **kw)

        def close_fake_only(fd):
            if 1000 <= fd < 5000:
                return None
            return real_close(fd)

        with mock.patch.object(ev.os, "replace", side_effect=cwd_only), \
                mock.patch.object(ev.os, "open", side_effect=fake_open), \
                mock.patch.object(ev.os, "close",
                                  side_effect=close_fake_only):
            self.assertFalse(ev._dirfd_replace_probe())
            self.assertEqual(fd_counter["n"], 2)

    def test_setup_failure_closes_every_opened_descriptor(self) -> None:
        from unittest import mock

        import tools.behavioral_eval_runner.evidence as ev

        real_open = os.open
        real_close = os.close
        real_td = tempfile.TemporaryDirectory
        opened: list = []
        closed: list = []
        counter = {"n": 0}
        fixtures: list = []

        def flaky_open(path, flags, *args, **kw):
            if os.path.basename(os.fspath(path)) in ("srcd", "dstd"):
                counter["n"] += 1
                if counter["n"] == 2:
                    raise OSError("injected dst-directory open failure")
                fd = 3000 + counter["n"]
                opened.append(fd)
                return fd
            return real_open(path, flags, *args, **kw)

        class SpyTD(real_td):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)
                fixtures.append(self)
                self.cleaned = False

            def cleanup(self) -> None:
                try:
                    return super().cleanup()
                finally:
                    self.cleaned = True

        def spy_close(fd):
            if 3000 <= fd < 5000:
                closed.append(fd)
                return None
            return real_close(fd)

        with mock.patch.object(ev.os, "open", side_effect=flaky_open), \
                mock.patch.object(ev.os, "close", side_effect=spy_close), \
                mock.patch.object(ev.tempfile, "TemporaryDirectory", SpyTD):
            self.assertFalse(ev._dirfd_replace_probe())
        self.assertEqual(sorted(opened), sorted(closed),
                         "every opened descriptor must be released")
        self.assertTrue(fixtures, "the probe must build its temp fixture")
        self.assertTrue(fixtures[0].cleaned,
                        "the temp fixture must be removed after the probe")

    def test_exception_categories_at_replace_boundary_return_false(self) -> None:
        from unittest import mock

        import tools.behavioral_eval_runner.evidence as ev

        fd_counter = {"n": 0}
        real_open = os.open
        real_close = os.close

        def fake_open(path, flags, *args, **kw):
            if os.path.basename(os.fspath(path)) in ("srcd", "dstd"):
                fd_counter["n"] += 1
                return 4000 + fd_counter["n"]
            return real_open(path, flags, *args, **kw)

        def close_fake_only(fd):
            if 1000 <= fd < 5000:
                return None
            return real_close(fd)

        for exc in (NotImplementedError, OSError, AttributeError):
            with mock.patch.object(
                    ev.os, "replace",
                    side_effect=exc("injected replace-boundary failure")), \
                    mock.patch.object(ev.os, "open",
                                      side_effect=fake_open), \
                    mock.patch.object(ev.os, "close",
                                      side_effect=close_fake_only):
                self.assertFalse(
                    ev._dirfd_replace_probe(),
                    exc.__name__ + " must yield False, not propagate")

    def test_static_membership_short_circuits_without_probe(self) -> None:
        from unittest import mock

        import tools.behavioral_eval_runner.evidence as ev

        calls: list = []

        def recording_probe():
            calls.append(1)
            return False

        with mock.patch.object(ev.os, "supports_dir_fd",
                               {os.replace}, create=True), \
                mock.patch.object(ev, "_dirfd_replace_probe",
                                  side_effect=recording_probe):
            self.assertTrue(ev._dirfd_replace_supported())
        self.assertEqual(calls, [],
                         "static membership is the FIRST short circuit - the "
                         "probe must not be consulted")

    def test_static_absent_delegates_to_probe(self) -> None:
        from unittest import mock

        import tools.behavioral_eval_runner.evidence as ev

        for probe_result in (True, False):
            with mock.patch.object(ev.os, "supports_dir_fd", frozenset(),
                                   create=True), \
                    mock.patch.object(ev, "_dirfd_replace_probe",
                                      return_value=probe_result):
                self.assertIs(ev._dirfd_replace_supported(), probe_result)


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
