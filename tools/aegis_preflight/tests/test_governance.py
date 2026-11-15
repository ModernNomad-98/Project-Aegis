"""T-GOV acceptance tests for the required-governance contract, resolver, receipts and admission.

One test per acceptance case in the P0-GOV plan of record r3 section 10; each test
names the case, its evidence label (S = synthetic fixture/test evidence; R = real
repository read-only execution at the candidate head; H = live installed-host
evidence, UNRUN) and a fail-before expectation.  Synthetic evidence never
certifies a live host boundary: live-host cases 09/10/11/16/22/25 remain UNRUN
and are recorded as such in the implementation evidence.
"""
from __future__ import annotations

import copy
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from tools.aegis_preflight import governance as gov  # noqa: E402

FIXTURES = Path(__file__).resolve().parent / "fixtures" / "governance"
SCHEMAS = gov.load_schemas(REPO_ROOT)
CONTRACT, CONTRACT_RAW = gov.load_contract(REPO_ROOT)
CONTRACT_SHA = gov.sha256_upper(CONTRACT_RAW)
DECISION_TIME = "2026-11-15T05:00:00Z"
PACKAGING = gov.build_packaging_binding(
    REPO_ROOT,
    detached_binding_evidence_ref="stage-c/C1-EVIDENCE.md#packaging-binding",
    detached_binding_sha256="a" * 64,
    commands=[
        {"verb": "build", "command": "synthetic command form", "exit_code": 0},
        {"verb": "verify", "command": "synthetic command form", "exit_code": 0},
        {"verb": "check-manifest", "command": "synthetic command form", "exit_code": 0},
    ],
    stage_a_feasibility_ref="FEASIBILITY-P0-GOV-r3.md",
    c1_dependency_consumption_used=True,
    dependency_closure_verified=True,
)
DOCUMENTS = {document["doc_id"]: document for document in CONTRACT["documents"]}


def make_temp_dir(prefix: str) -> str:
    """Unique directory via os.mkdir (portable on restricted Windows test hosts)."""
    import uuid

    base = Path(tempfile.gettempdir())
    for _ in range(20):
        candidate = base / (prefix + uuid.uuid4().hex)
        try:
            candidate.mkdir()
            return str(candidate)
        except FileExistsError:
            continue
    raise RuntimeError("could not create a unique temporary directory")


def source_target() -> dict:
    return {
        "target_repo": "ModernNomad-98/Project-Aegis",
        "target_kind": "source-library-checkout",
        "workspace_role": "source-library",
        "role_evidence": [
            "README.md '# Project Aegis' identity",
            "docs/skills-catalog.md",
            "scripts/validate-skills.py",
            "artifacts/audits/skill-contract-audit-baseline.json",
        ],
    }


def consumer_target() -> dict:
    return {
        "target_repo": "example-consumer/aegis-consumer",
        "target_kind": "consumer-copy",
        "workspace_role": "consumer",
        "role_evidence": ["copied AGENTS.md/CLAUDE.md", "no source landmarks present"],
    }


def host_session() -> dict:
    session = gov._default_host_session()
    session.update(
        {
            "host_product": "DeepSeek Harness Desktop",
            "host_version": "0.2.2-rc.1",
            "host_build_sha256": "5FA8A6B21BCEB8F3E99E30EFA2270EFD0CC773A11E42AA0488F804A64B34E637",
            "profile_digest": "76ACFA89CB81E7A123ECB47CB744F7A1C82A4C6F21DBA93FAC8CC33960C2BA01",
            "session_id": "synthetic-session",
            "origin": "synthetic-fixture",
            "delegation_depth": 0,
            "agent_preset": "synthetic",
            "requested_model_route": "synthetic/route",
            "reasoning_effort": "synthetic",
            "permission_preset": "synthetic",
            "sandbox_mode": "synthetic",
            "approval_policy": "synthetic",
            "gates_active": "none",
        }
    )
    return session


def make_task(authority: str = "synthetic fixture owner line for the acceptance case") -> dict:
    return {
        "task_id": "task-55",
        "task_ref": "task-55",
        "scope_summary": "synthetic P0-GOV acceptance case",
        "task_authority_ref": authority,
    }


def make_root(
    directory: str,
    *,
    role: str = "source-library",
    overrides: dict | None = None,
    removals: tuple = (),
    extra_files: dict | None = None,
    contract_raw: bytes | None = None,
) -> Path:
    """Materialise a synthetic target root: the role's required docs + the contract."""
    root = Path(directory) / "target"
    root.mkdir(parents=True, exist_ok=True)
    overrides = overrides or {}
    for doc_id in CONTRACT["roles"][role]["required_documents"]:
        document = DOCUMENTS[doc_id]
        destination = root / document["path"]
        destination.parent.mkdir(parents=True, exist_ok=True)
        if doc_id in removals:
            continue
        payload = overrides.get(doc_id)
        if payload is None:
            payload = (REPO_ROOT / document["path"]).read_bytes()
        destination.write_bytes(payload)
    contract_path = root / gov.CONTRACT_RELPATH
    contract_path.parent.mkdir(parents=True, exist_ok=True)
    contract_path.write_bytes(contract_raw if contract_raw is not None else CONTRACT_RAW)
    for relative, payload in (extra_files or {}).items():
        destination = root / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(payload if isinstance(payload, bytes) else str(payload).encode("utf-8"))
    return root


def materialise_adoption(name: str = "adoption/copied-starter-adoption.json") -> dict:
    text = (FIXTURES / name).read_text(encoding="utf-8")
    text = text.replace("__CONTRACT_SHA256__", CONTRACT_SHA).replace(
        "__CONTRACT_VERSION__", str(CONTRACT["contract_version"])
    )
    return json.loads(text)


def write_adoption(root: Path, adoption: dict, relative: str = "docs/aegis-adoption.json") -> tuple:
    destination = root / relative
    destination.parent.mkdir(parents=True, exist_ok=True)
    payload = (json.dumps(adoption, indent=2, sort_keys=True) + "\n").encode("utf-8")
    destination.write_bytes(payload)
    return relative, adoption, gov.sha256_raw(payload)


def ensure_manifest_binding() -> None:
    assert (REPO_ROOT / gov.MANIFEST_RELPATH).is_file(), "the committed governance manifest must exist for receipts"


def do_resolve(
    contract: dict | None = None,
    raw: bytes | None = None,
    *,
    root: Path | None = None,
    role: str = "source-library",
    route: str = "source-checkout",
    adoption: dict | None = None,
    adoption_ref: str | None = None,
    adoption_sha256: str | None = None,
    nested_policies: list | None = None,
    conditions: dict | None = None,
    target: dict | None = None,
    operation_class: str = "read-only-diagnostic",
):
    return gov.resolve(
        contract if contract is not None else CONTRACT,
        role=role,
        route_id=route,
        repo_root=root if root is not None else REPO_ROOT,
        schemas=SCHEMAS,
        adoption=adoption,
        adoption_ref=adoption_ref,
        adoption_sha256=adoption_sha256,
        nested_policies=nested_policies,
        conditions=conditions,
        target=target if target is not None else (source_target() if role == "source-library" else consumer_target()),
        operation_class=operation_class,
    )


def do_receipt(
    resolution,
    *,
    root: Path | None = None,
    contract: dict | None = None,
    raw: bytes | None = None,
    observation_type: str = "fresh-start",
    receipt_id: str = "CR-synthetic-0001",
    observed_at: str = DECISION_TIME,
    task: dict | None = None,
    target: dict | None = None,
    adoption: dict | None = None,
    adoption_ref: str | None = None,
    adoption_sha256: str | None = None,
    prior_receipt: dict | None = None,
) -> dict:
    ensure_manifest_binding()
    role = resolution.role
    return gov.derive_receipt(
        contract if contract is not None else CONTRACT,
        raw if raw is not None else CONTRACT_RAW,
        resolution,
        repo_root=root if root is not None else REPO_ROOT,
        schemas=SCHEMAS,
        receipt_id=receipt_id,
        observation_type=observation_type,
        observed_at_utc=observed_at,
        task=task if task is not None else make_task(),
        target=target if target is not None else (source_target() if role == "source-library" else consumer_target()),
        host_session=host_session(),
        instructions={"baseline_identity": None, "files": [], "budget_omissions": []},
        packaging_binding=PACKAGING,
        adoption=adoption,
        adoption_ref=adoption_ref,
        adoption_sha256=adoption_sha256,
        prior_receipt=prior_receipt,
    )


def do_admit(
    receipt,
    *,
    root: Path | None = None,
    contract: dict | None = None,
    raw: bytes | None = None,
    operation_class: str = "commit",
    current_role: str | None = None,
    current_repo: str | None = None,
    current_pin: dict | None = None,
    session_boundary_utc: str | None = None,
    current_adoption: dict | None = None,
    current_authority_ref: str | None = None,
    decision_id: str = "AD-synthetic-0001",
):
    return gov.admit(
        contract if contract is not None else CONTRACT,
        raw if raw is not None else CONTRACT_RAW,
        receipt,
        SCHEMAS,
        repo_root=root if root is not None else REPO_ROOT,
        operation_class=operation_class,
        decision_id=decision_id,
        requested_at_utc=DECISION_TIME,
        operation_ref={"kind": "commit", "ref": "deadbeef" if operation_class != "read-only-diagnostic" else "diagnostic"},
        authority_ref="synthetic fixture authority reference",
        current_role=current_role,
        current_repo=current_repo,
        current_pin=current_pin,
        session_boundary_utc=session_boundary_utc,
        current_adoption=current_adoption,
        current_authority_ref=current_authority_ref,
    )


class GovernanceRenderTests(unittest.TestCase):
    """Deterministic regeneration of the committed artifacts (plan 5.1/5.2.1)."""

    def test_committed_contract_equals_render(self) -> None:
        self.assertEqual(gov.render_contract_bytes(REPO_ROOT), CONTRACT_RAW)

    def test_committed_projection_equals_render(self) -> None:
        committed = (REPO_ROOT / gov.PROJECTION_RELPATH).read_bytes()
        self.assertEqual(gov.render_projection_bytes(REPO_ROOT), committed)

    def test_committed_governance_dependencies_equals_render(self) -> None:
        committed = (REPO_ROOT / gov.GOVERNANCE_DEPENDENCIES_RELPATH).read_bytes()
        self.assertEqual(gov.render_governance_dependencies_bytes(REPO_ROOT), committed)

    def test_payload_root_contains_exactly_the_six_entries(self) -> None:
        payload_files = sorted(
            path.relative_to(REPO_ROOT / gov.PAYLOAD_DIR).as_posix()
            for path in (REPO_ROOT / gov.PAYLOAD_DIR).rglob("*")
            if path.is_file()
        )
        self.assertEqual(
            payload_files,
            sorted(
                [
                    "required-governance-contract.v1.json",
                    "rule-projection.v1.json",
                    "schemas/admission-decision-v1.schema.json",
                    "schemas/adoption-record-v1.schema.json",
                    "schemas/context-receipt-v1.schema.json",
                    "schemas/governance-contract-v1.schema.json",
                ]
            ),
        )

    def test_manifest_is_outside_the_payload_root_and_reproducible(self) -> None:
        self.assertFalse(str(REPO_ROOT / gov.MANIFEST_RELPATH).startswith(str(REPO_ROOT / gov.PAYLOAD_DIR)))
        with tempfile.TemporaryDirectory(prefix="gov-render-") as temporary:
            output = Path(temporary) / "manifest.json"
            from tools.distributed_payload import manifest as payload_manifest

            source = gov.load_source_identity(REPO_ROOT)
            dependencies = gov.load_dependencies_input(REPO_ROOT)
            document = payload_manifest.build_manifest(
                REPO_ROOT / gov.PAYLOAD_DIR,
                "aegis.required-governance",
                "1.0.0",
                source,
                dependencies=dependencies,
            )
            payload_manifest.write_manifest_atomic(document, output)
            self.assertEqual(output.read_bytes(), (REPO_ROOT / gov.MANIFEST_RELPATH).read_bytes())

    def test_validate_committed_contract_passes(self) -> None:
        _, _, findings = gov.validate_contract_at_repo(REPO_ROOT)
        self.assertEqual([finding.as_dict() for finding in findings], [])

    def test_contract_source_matches_source_json(self) -> None:
        source = gov.load_source_identity(REPO_ROOT)
        self.assertEqual(CONTRACT["source"]["repository"], source["repository"])
        self.assertEqual(CONTRACT["source"]["commit"], source["commit"])
        self.assertEqual(CONTRACT["source"]["tree"], source["tree"])

    def test_contract_version_bump_required_on_document_change(self) -> None:
        previous = copy.deepcopy(CONTRACT)
        previous["documents"][0]["sha256"] = "0" * 64
        with self.assertRaises(gov.GovernanceError) as raised:
            gov.build_contract_document(REPO_ROOT, previous_contract=previous)
        self.assertEqual(raised.exception.code, "contract_version_bump_required")


class AcceptanceCaseTests(unittest.TestCase):
    """One test per plan section 10 acceptance case (S/R executed; H UNRUN)."""

    def setUp(self) -> None:
        self._temporary = make_temp_dir("gov-case-")
        self.tmp = Path(self._temporary)
        self.addCleanup(shutil.rmtree, self._temporary, True)

    # --- CASE 01 (S+R): source checkout resolves applicable source governance.
    def test_case01_source_checkout_resolves(self) -> None:
        # Fail-before: without the committed contract, resolution cannot start.
        with tempfile.TemporaryDirectory(prefix="gov-nocontract-") as empty:
            with self.assertRaises(gov.GovernanceError):
                gov.load_contract(Path(empty))
        resolution = do_resolve(root=REPO_ROOT, role="source-library", route="source-checkout")
        self.assertEqual(resolution.status, "RESOLVED")
        self.assertEqual(len(resolution.resolved_documents), 10)
        self.assertEqual(len(resolution.resolved_rules), 147)
        self.assertEqual(len(resolution.exclusions), 57)
        self.assertEqual(resolution.findings, [])
        self.assertIn("PROPOSED-CONTRACT", resolution.labels)
        self.assertEqual(resolution.enforcement_claim, "GUIDANCE-ONLY")
        self.assertEqual(resolution.gates_active, "none")
        receipt = do_receipt(resolution)
        self.assertGreater(len(gov.receipt_sha256(receipt)), 32)
        decision = do_admit(receipt, operation_class="protected-write")
        self.assertEqual(decision.decision, "ALLOW")

    # --- CASE 02 (S): copied starter resolves with consumer scope.
    def test_case02_copied_starter_resolves_with_consumer_scope(self) -> None:
        root = make_root(self._temporary, role="consumer")
        adoption = materialise_adoption()
        adoption_ref, adoption_doc, adoption_sha = write_adoption(root, adoption)
        resolution = do_resolve(
            root=root,
            role="consumer",
            route="copied-starter",
            adoption=adoption_doc,
            adoption_ref=adoption_ref,
            adoption_sha256=adoption_sha,
        )
        self.assertEqual(resolution.status, "RESOLVED")
        self.assertEqual(resolution.adoption_state, "adopted")
        resolved_doc_ids = {document.doc_id for document in resolution.resolved_documents}
        self.assertEqual(resolved_doc_ids, {"AGENTS", "CLAUDE", "CONSUMER-MANUAL-ONLY", "MANUAL-ONLY-POLICY", "STARTER"})
        excluded_refs = {exclusion["ref"] for exclusion in resolution.exclusions}
        self.assertIn("REGISTER", excluded_refs)
        self.assertIn("DW", excluded_refs)
        receipt = do_receipt(
            resolution,
            root=root,
            target=consumer_target(),
            adoption=adoption_doc,
            adoption_ref=adoption_ref,
            adoption_sha256=adoption_sha,
        )
        self.assertEqual(receipt["local_adoption"]["state"], "adopted")
        self.assertEqual(len(receipt["required_documents"]), 5)
        # The live starter install is a separate governed outcome (O12) and is UNRUN.

    # --- CASE 03 (S): external skill path, pin mismatch blocks with both versions.
    def test_case03_external_skill_pin_mismatch_blocks(self) -> None:
        dependencies = json.loads(
            (FIXTURES / "external-skill" / "opsflow-skill-dependencies.json")
            .read_text(encoding="utf-8")
            .replace("__CONTRACT_VERSION__", str(CONTRACT["contract_version"]))
            .replace("__TARGET_CONTRACT_SHA256__", "F" * 64)
        )
        findings = gov.validate_skill_dependency(dependencies, "plan-of-record-author", CONTRACT, CONTRACT_RAW)
        self.assertTrue(findings)
        self.assertEqual(findings[0].status, "BLOCKED")
        self.assertIn("F" * 64, findings[0].message)
        self.assertIn(CONTRACT_SHA, findings[0].message)
        matching = json.loads(
            (FIXTURES / "external-skill" / "opsflow-skill-dependencies.json")
            .read_text(encoding="utf-8")
            .replace("__CONTRACT_VERSION__", str(CONTRACT["contract_version"]))
            .replace("__TARGET_CONTRACT_SHA256__", CONTRACT_SHA)
        )
        self.assertEqual(gov.validate_skill_dependency(matching, "plan-of-record-author", CONTRACT, CONTRACT_RAW), [])
        # Reading the external skill never switches the target repository: the
        # resolution target remains the consumer repository.
        resolution = do_resolve(root=REPO_ROOT, role="consumer", route="external-skill")
        self.assertEqual(resolution.status, "BLOCKED")  # no consumer adoption record supplied
        self.assertIn("ADOPTION", "".join(finding.message for finding in resolution.findings).upper())

    # --- CASE 05 (S): missing referenced document blocks; diagnostics allowed.
    def test_case05_missing_document_blocks(self) -> None:
        root = make_root(self._temporary, role="source-library", removals=("REGISTER",))
        resolution = do_resolve(root=root, role="source-library", route="source-checkout")
        self.assertEqual(resolution.status, "BLOCKED")
        messages = " ".join(finding.message for finding in resolution.findings)
        self.assertIn("APPROVAL_REGISTER", messages + " ".join(str(item) for item in resolution.excluded_documents))
        diagnostic = do_admit(None, root=root, operation_class="read-only-diagnostic")
        self.assertEqual(diagnostic.decision, "ALLOW")
        self.assertEqual(diagnostic.reason_code, "READ_ONLY_DIAGNOSTIC_PERMITTED")

    # --- CASE 06 (S): contradictory rules block; the resolver never picks a winner.
    def test_case06_contradictory_rules_block(self) -> None:
        contract = copy.deepcopy(CONTRACT)
        contract["conflicts"].append(
            {
                "conflict_id": "C13",
                "title": "synthetic rule-level contradiction for the acceptance case",
                "status": "UNRESOLVED",
                "documents": [],
                "rule_ids": ["AG-02", "CT-09"],
                "resolution_owner": "synthetic fixture owner",
            }
        )
        resolution = do_resolve(contract=contract, raw=None, root=REPO_ROOT)
        self.assertEqual(resolution.status, "BLOCKED")
        conflict = next(item for item in resolution.conflicts if item["conflict_id"] == "C13")
        self.assertFalse(conflict["resolved_by_resolver"])
        self.assertEqual(conflict["rule_ids"], ["AG-02", "CT-09"])
        self.assertEqual(set(conflict["anchors"]), {"AG-02", "CT-09"})
        self.assertTrue(any("C13" in finding.message for finding in resolution.findings))

    # --- CASE 07 (S; H note): nested policy enters closure for the applicable path only.
    def test_case07_nested_policy_scope(self) -> None:
        nested = (FIXTURES / "nested-policy" / "AGENTS.local.md").read_bytes()
        unrelated = (FIXTURES / "nested-policy" / "CLAUDE.local.md").read_bytes()
        root = make_root(
            self._temporary,
            role="source-library",
            extra_files={"nested/work/AGENTS.local.md": nested, "unrelated/CLAUDE.local.md": unrelated},
        )
        resolution = do_resolve(
            root=root, role="source-library", route="source-checkout", nested_policies=["nested/work/AGENTS.local.md"]
        )
        receipt = do_receipt(resolution, root=root)
        paths = [item["path"] for item in receipt["nested_local_policy"]]
        self.assertEqual(paths, ["nested/work/AGENTS.local.md"])
        self.assertNotIn("unrelated/CLAUDE.local.md", paths)
        # Host discovery of nested instruction files is H evidence and remains UNRUN.

    # --- CASE 08 (S): local-only policy change invalidates the receipt.
    def test_case08_local_policy_change_invalidates(self) -> None:
        nested = (FIXTURES / "nested-policy" / "AGENTS.local.md").read_bytes()
        root = make_root(self._temporary, role="source-library", extra_files={"nested/AGENTS.local.md": nested})
        resolution = do_resolve(root=root, nested_policies=["nested/AGENTS.local.md"])
        receipt = do_receipt(resolution, root=root)
        first = do_admit(receipt, root=root, operation_class="commit")
        self.assertEqual(first.decision, "ALLOW")
        (root / "nested/AGENTS.local.md").write_bytes(nested + b"\n- local rule changed\n")
        second = do_admit(receipt, root=root, operation_class="commit", decision_id="AD-synthetic-0002")
        self.assertEqual(second.decision, "BLOCKED")
        self.assertEqual(second.reason_code, "OBSERVATION_STALE")
        differing = second.recheck["differing_inputs"]
        self.assertIn("nested/AGENTS.local.md", [item["path"] for item in differing])

    # --- CASE 09 (S; H UNRUN): a prior-session receipt cannot alone authorize work.
    def test_case09_resume_receipt_typing(self) -> None:
        resolution = do_resolve(root=REPO_ROOT, route="source-checkout")
        receipt = do_receipt(resolution, observed_at="2026-11-15T04:00:00Z")
        before = do_admit(receipt, operation_class="protected-write", session_boundary_utc="2026-11-15T04:30:00Z")
        self.assertEqual(before.decision, "BLOCKED")
        self.assertEqual(before.reason_code, "OBSERVATION_PRE_BOUNDARY")
        resume_resolution = do_resolve(root=REPO_ROOT, role="source-library", route="resume")
        resume_receipt = do_receipt(
            resume_resolution, observation_type="resume", receipt_id="CR-synthetic-resume", observed_at=DECISION_TIME
        )
        after = do_admit(
            resume_receipt,
            operation_class="protected-write",
            session_boundary_utc="2026-11-15T04:30:00Z",
            decision_id="AD-synthetic-0003",
        )
        self.assertEqual(after.decision, "ALLOW")
        # Live DSH resume evidence remains UNRUN.

    # --- CASE 10 (S; H UNRUN): compaction restoration runs before the next protected operation.
    def test_case10_compaction_restoration_order(self) -> None:
        no_receipt = do_admit(None, operation_class="protected-write")
        self.assertEqual(no_receipt.decision, "DENY")
        self.assertEqual(no_receipt.reason_code, "RECEIPT_INVALID")
        compaction_resolution = do_resolve(root=REPO_ROOT, role="source-library", route="compaction")
        receipt = do_receipt(compaction_resolution, observation_type="compaction", receipt_id="CR-synthetic-compaction")
        outcome = do_admit(receipt, operation_class="protected-write", decision_id="AD-synthetic-0004")
        self.assertEqual(outcome.decision, "ALLOW")
        self.assertEqual(receipt["observation_type"], "compaction")
        # Live DSH compaction evidence remains UNRUN.

    # --- CASE 11 (S; H UNRUN): handoff restores context; an authority assertion alone is denied.
    def test_case11_handoff_convention(self) -> None:
        handoff_resolution = do_resolve(root=REPO_ROOT, role="source-library", route="handoff")
        receipt = do_receipt(handoff_resolution, observation_type="handoff", receipt_id="CR-synthetic-handoff")
        self.assertEqual(receipt["observation_type"], "handoff")
        outcome = do_admit(receipt, operation_class="protected-write", decision_id="AD-synthetic-0005")
        self.assertEqual(outcome.decision, "ALLOW")
        assertion = do_admit(None, operation_class="protected-write", decision_id="AD-synthetic-0006")
        self.assertEqual(assertion.decision, "DENY")
        consumer_receipt = do_receipt(
            do_resolve(root=REPO_ROOT, role="consumer", route="handoff"),
            root=REPO_ROOT,
            task=make_task("AEGIS-APR-100"),
            target=consumer_target(),
            observation_type="handoff",
        )
        mixed = do_admit(consumer_receipt, operation_class="protected-write", decision_id="AD-synthetic-0007")
        self.assertEqual(mixed.decision, "DENY")
        self.assertEqual(mixed.reason_code, "AUTHORITY_ISOLATION_VIOLATION")
        # The host has no handoff primitive: the H case cannot pass by simulation.

    # --- CASE 12 (S): changed upstream requirement requires refreshed closure.
    def test_case12_pin_change_requires_refresh(self) -> None:
        resolution = do_resolve(root=REPO_ROOT)
        receipt = do_receipt(resolution)
        blocked = do_admit(
            receipt,
            operation_class="commit",
            current_pin={"commit": "0" * 40, "tree": "0" * 40},
        )
        self.assertEqual(blocked.decision, "BLOCKED")
        self.assertEqual(blocked.reason_code, "PIN_CHANGED")
        previous = copy.deepcopy(receipt)
        previous["contract"]["approved_upstream_pin"]["commit"] = "0" * 40
        refreshed = do_receipt(resolution, receipt_id="CR-synthetic-refresh", prior_receipt=previous)
        combined = " ".join(refreshed["limitations"])
        self.assertIn("0" * 40, combined)
        self.assertIn(str(CONTRACT["source"]["commit"]), combined)
        self.assertTrue(any("PIN_CHANGED" in line for line in refreshed["limitations"]))
        self.assertEqual(previous["contract"]["approved_upstream_pin"]["commit"], "0" * 40)

    # --- CASE 13 (S): an approved old/offline pin stays historical/unmigrated.
    def test_case13_historical_pin_labelled(self) -> None:
        root = make_root(self._temporary, role="consumer")
        adoption = materialise_adoption()
        adoption["installation"]["aegis_pin_commit"] = "66620739818466d3fa9646e7fbf85671284e4ebf"
        adoption["installation"]["aegis_pin_tree"] = "2" * 40
        adoption_ref, adoption_doc, adoption_sha = write_adoption(root, adoption)
        resolution = do_resolve(
            root=root,
            role="consumer",
            route="copied-starter",
            adoption=adoption_doc,
            adoption_ref=adoption_ref,
            adoption_sha256=adoption_sha,
        )
        self.assertIn("HISTORICAL-UNMIGRATED", resolution.labels)
        self.assertEqual(resolution.adoption_authority_ref, adoption_doc["authority"]["ref"])
        receipt = do_receipt(
            resolution,
            root=root,
            target=consumer_target(),
            adoption=adoption_doc,
            adoption_ref=adoption_ref,
            adoption_sha256=adoption_sha,
        )
        pin = receipt["contract"]["approved_upstream_pin"]
        self.assertEqual(pin["commit"], "66620739818466d3fa9646e7fbf85671284e4ebf")
        self.assertEqual(CONTRACT["contract_version"], receipt["contract"]["contract_version"])

    # --- CASE 14 (S): a local owner withdrawal defeats an otherwise valid receipt.
    def test_case14_withdrawn_adoption(self) -> None:
        root = make_root(self._temporary, role="consumer")
        valid = materialise_adoption()
        valid_ref, valid_doc, valid_sha = write_adoption(root, valid)
        resolution = do_resolve(
            root=root,
            role="consumer",
            route="copied-starter",
            adoption=valid_doc,
            adoption_ref=valid_ref,
            adoption_sha256=valid_sha,
        )
        receipt = do_receipt(
            resolution,
            root=root,
            target=consumer_target(),
            adoption=valid_doc,
            adoption_ref=valid_ref,
            adoption_sha256=valid_sha,
        )
        self.assertEqual(do_admit(receipt, root=root, operation_class="commit").decision, "ALLOW")
        withdrawn = materialise_adoption("adoption/withdrawn-adoption.json")
        withdrawn_ref, withdrawn_doc, withdrawn_sha = write_adoption(root, withdrawn)
        blocked = do_admit(
            receipt,
            root=root,
            operation_class="commit",
            current_adoption=withdrawn_doc,
            decision_id="AD-synthetic-0008",
        )
        self.assertEqual(blocked.decision, "BLOCKED")
        self.assertEqual(blocked.reason_code, "ADOPTION_WITHDRAWN")
        withdrawn_resolution = do_resolve(
            root=root,
            role="consumer",
            route="copied-starter",
            adoption=withdrawn_doc,
            adoption_ref=withdrawn_ref,
            adoption_sha256=withdrawn_sha,
        )
        self.assertEqual(withdrawn_resolution.status, "BLOCKED")
        self.assertTrue(any("withdrawn" in finding.message.lower() for finding in withdrawn_resolution.findings))

    # --- CASE 15 (S): a forged/edited receipt cannot satisfy admission.
    def test_case15_forged_receipt_rejected(self) -> None:
        resolution = do_resolve(root=REPO_ROOT)
        receipt = do_receipt(resolution)
        forged = copy.deepcopy(receipt)
        forged["required_documents"][0]["sha256"] = "0" * 64
        denied = do_admit(forged, operation_class="commit")
        self.assertEqual(denied.decision, "DENY")
        self.assertEqual(denied.reason_code, "RECEIPT_INVALID")
        self_consistent = copy.deepcopy(receipt)
        for item in self_consistent["invalidation_inputs_digest"]["inputs"]:
            if item["kind"] == "document":
                item["sha256"] = "0" * 64
        self_consistent["invalidation_inputs_digest"]["digest"] = gov.invalidation_digest(
            self_consistent["invalidation_inputs_digest"]["inputs"]
        )
        denied_again = do_admit(self_consistent, operation_class="commit", decision_id="AD-synthetic-0009")
        self.assertNotEqual(denied_again.decision, "ALLOW")
        self.assertIn(denied_again.decision, ("DENY", "BLOCKED"))
        if denied_again.decision == "BLOCKED":
            self.assertEqual(denied_again.reason_code, "OBSERVATION_STALE")
            self.assertTrue(denied_again.recheck["differing_inputs"])
        else:
            self.assertEqual(denied_again.reason_code, "RECEIPT_INVALID")

    # --- CASE 16 (S; H UNRUN): bypass routes are disclosed; enforcement labels are honest.
    def test_case16_bypass_disclosure_and_gate_labels(self) -> None:
        resolution = do_resolve(root=REPO_ROOT)
        self.assertEqual(resolution.enforcement_claim, "GUIDANCE-ONLY")
        self.assertEqual(resolution.gates_active, "none")
        self.assertIn("GUIDANCE-ONLY", resolution.labels)
        claims = CONTRACT["enforcement_claims"]
        self.assertEqual(claims["claim"], "GUIDANCE-ONLY")
        self.assertIsNone(claims["host_plugin"])
        self.assertGreaterEqual(len(claims["bypass_routes"]), 7)
        bad_contract = copy.deepcopy(CONTRACT)
        bad_contract["enforcement_claims"]["claim"] = "HOST-PLUGIN"
        findings = gov.validate_contract_document(
            bad_contract,
            SCHEMAS,
            repo_root=REPO_ROOT,
            inventory=gov.load_inventory(REPO_ROOT),
            projection=gov.load_projection(REPO_ROOT),
        )
        self.assertTrue(any(finding.code == "GR-10" and finding.status == "FAIL" for finding in findings))
        receipt = do_receipt(resolution)
        claimed = copy.deepcopy(receipt)
        claimed["host_session"]["gates_active"] = "unknown"
        denied = do_admit(claimed, operation_class="commit", decision_id="AD-synthetic-0010")
        self.assertEqual(denied.decision, "DENY")
        self.assertEqual(denied.reason_code, "HOST_CLAIM_UNSUPPORTED")
        # The live bypass suite is H evidence and remains UNRUN.

    # --- CASE 17 (S): a change after the check invalidates admission.
    def test_case17_change_after_check(self) -> None:
        root = make_root(self._temporary, role="source-library")
        resolution = do_resolve(root=root)
        receipt = do_receipt(resolution, root=root)
        contributing = root / DOCUMENTS["CONTRIBUTING"]["path"]
        contributing.write_bytes(contributing.read_bytes() + b"\n- changed after the check\n")
        blocked = do_admit(receipt, root=root, operation_class="commit")
        self.assertEqual(blocked.decision, "BLOCKED")
        self.assertEqual(blocked.reason_code, "OBSERVATION_STALE")
        recheck = blocked.recheck
        self.assertNotEqual(recheck["digest_before"], recheck["digest_after"])
        self.assertIn("CONTRIBUTING.md", [item["path"] for item in recheck["differing_inputs"]])

    # --- CASE 18 (S): wrong target/role cannot be authorized by the other role's receipt.
    def test_case18_role_target_mismatch(self) -> None:
        resolution = do_resolve(root=REPO_ROOT)
        receipt = do_receipt(resolution)
        denied = do_admit(receipt, operation_class="commit", current_role="consumer")
        self.assertEqual(denied.decision, "DENY")
        self.assertEqual(denied.reason_code, "ROLE_TARGET_MISMATCH")
        consumer_receipt = do_receipt(
            do_resolve(root=REPO_ROOT, role="consumer", route="copied-starter"),
            root=REPO_ROOT,
            target=consumer_target(),
        )
        other = do_admit(
            consumer_receipt, operation_class="commit", current_repo="other-tenant/other-repo", decision_id="AD-synthetic-0011"
        )
        self.assertEqual(other.decision, "DENY")
        self.assertEqual(other.reason_code, "ROLE_TARGET_MISMATCH")
        self.assertEqual(consumer_receipt["target"]["target_repo"], "example-consumer/aegis-consumer")

    # --- CASE 19 (S): source merge/admin grants do not authorize consumer actions.
    def test_case19_permission_isolation(self) -> None:
        root = make_root(self._temporary, role="consumer")
        adoption = materialise_adoption()
        adoption_ref, adoption_doc, adoption_sha = write_adoption(root, adoption)
        resolution = do_resolve(
            root=root,
            role="consumer",
            route="copied-starter",
            adoption=adoption_doc,
            adoption_ref=adoption_ref,
            adoption_sha256=adoption_sha,
        )
        self.assertEqual(resolution.status, "RESOLVED")
        illegal = do_receipt(
            resolution,
            root=root,
            target=consumer_target(),
            task=make_task("AEGIS-APR-100 standing merge grant"),
            adoption=adoption_doc,
            adoption_ref=adoption_ref,
            adoption_sha256=adoption_sha,
        )
        denied = do_admit(illegal, root=root, operation_class="consumer-repository-write")
        self.assertEqual(denied.decision, "DENY")
        self.assertEqual(denied.reason_code, "AUTHORITY_ISOLATION_VIOLATION")
        local = do_receipt(
            resolution,
            root=root,
            target=consumer_target(),
            task=make_task("consumer owner line 2026-11-14 (consumer-local authority)"),
            adoption=adoption_doc,
            adoption_ref=adoption_ref,
            adoption_sha256=adoption_sha,
            receipt_id="CR-synthetic-local-authority",
        )
        allowed = do_admit(
            local, root=root, operation_class="consumer-repository-write", decision_id="AD-synthetic-0012"
        )
        self.assertEqual(allowed.decision, "ALLOW")

    # --- CASE 20 (S): source staffing/reporting duties are not imported without adoption.
    def test_case20_staffing_reporting_isolation(self) -> None:
        resolution = do_resolve(root=REPO_ROOT, role="consumer", route="copied-starter")
        staffing_rules = {
            rule["rule_id"]
            for rule in CONTRACT["rule_applicability"]
            if rule["dimension"] == "staffing" and rule["applies_to_roles"] == ["source-library"]
        }
        self.assertTrue(staffing_rules)
        resolved_ids = {rule["rule_id"] for rule in resolution.resolved_rules}
        self.assertFalse(staffing_rules & resolved_ids)
        role_excluded = {item["ref"] for item in resolution.exclusions if item["reason"] == "role-excluded"}
        self.assertTrue(staffing_rules & role_excluded)
        self.assertIn("AG-09", role_excluded)
        by_id = {rule["rule_id"]: rule for rule in CONTRACT["rule_applicability"]}
        self.assertEqual(by_id["AG-09"]["adoption_status"], "not-portable")
        excluded_refs = {item["ref"] for item in resolution.exclusions}
        for rule_id in ("AG-09", "DW-23"):
            self.assertIn(rule_id, excluded_refs)

    # --- CASE 21 (S/R): planning lineage and budgets are separate and no count is invented.
    def test_case21_lineage_budget_separation(self) -> None:
        lineage = json.loads((FIXTURES / "lineage" / "plan-lineage.json").read_text(encoding="utf-8"))
        self.assertEqual([entry["id"] for entry in lineage["entries"]], ["L%02d" % index for index in range(1, 18)])
        self.assertFalse(any(entry["counted_as_plan_revision"] for entry in lineage["entries"]))
        self.assertEqual([capture["revision"] for capture in lineage["plan_captures"]], ["r1", "r2", "r3"])
        self.assertEqual(lineage["plan_captures"][-1]["audit_verdict"], "ACCEPT")
        self.assertIsNone(lineage["counts_asserted"])
        records = [
            gov.build_budget_record("planning-revision", "aegis.plan.p0-governance-discovery-2026-11-14", 0),
            gov.build_budget_record("code-review-round", "PR-A review rounds", 2),
            gov.build_budget_record("review-head", "published candidate heads", 1),
            gov.build_budget_record("host-evidence", "live host cases", 0),
        ]
        totals = gov.sum_budgets(records)
        self.assertEqual(set(totals), set(governance_budget_categories()))
        self.assertEqual(totals["planning-revision"], 0)
        self.assertEqual(totals["code-review-round"], 2)
        with self.assertRaises(gov.GovernanceError):
            gov.build_budget_record("planning-revision+review-head", "converted count", 1)
        receipt_schema = SCHEMAS["receipt"]
        admission_schema = SCHEMAS["admission"]
        self.assertNotIn("revision_count", json.dumps(receipt_schema))
        self.assertNotIn("revision_count", json.dumps(admission_schema))

    # --- CASE 22 (S; H UNRUN): MANUAL-ONLY skills are never auto-applied.
    def test_case22_manual_only_never_auto_invoked(self) -> None:
        dependencies = gov.read_repo_json(REPO_ROOT, gov.GOVERNANCE_DEPENDENCIES_RELPATH)
        manual = [entry for entry in dependencies["entrypoints"] if entry.get("manual_only")]
        self.assertTrue(manual)
        skill_id = manual[0]["name"]
        auto = gov.skill_invocation_decision(dependencies, skill_id, mode="auto")
        self.assertEqual(auto["decision"], "DENY")
        self.assertEqual(auto["reason_code"], "MANUAL_ONLY_AUTO_INVOCATION_DENIED")
        discovery = gov.skill_invocation_decision(dependencies, skill_id, mode="discovery")
        self.assertEqual(discovery["decision"], "DENY")
        no_override = gov.skill_invocation_decision(dependencies, skill_id, mode="explicit")
        self.assertEqual(no_override["decision"], "DENY")
        overridden = gov.skill_invocation_decision(
            dependencies, skill_id, mode="explicit", override_ref="consumer manual-only overrides register row 1"
        )
        self.assertEqual(overridden["decision"], "ALLOW")
        undeclared = gov.skill_invocation_decision(dependencies, "not-a-skill", mode="auto")
        self.assertEqual(undeclared["reason_code"], "SKILL_NOT_DECLARED")
        # Live host invocation is H evidence and remains UNRUN; .claude/skills is not discovered here.

    # --- CASE 23 (R): pre-existing work remains byte-identical (bounded manifest).
    def test_case23_preservation_manifest(self) -> None:
        relpaths = [DOCUMENTS[doc_id]["path"] for doc_id in CONTRACT["roles"]["source-library"]["required_documents"]]
        relpaths.append(gov.CONTRACT_RELPATH)
        before = gov.preservation_manifest(REPO_ROOT, relpaths)
        resolution = do_resolve(root=REPO_ROOT)
        receipt = do_receipt(resolution)
        do_admit(receipt, operation_class="commit")
        after = gov.preservation_manifest(REPO_ROOT, relpaths)
        self.assertEqual(gov.preservation_diff(before, after), [])
        self.assertEqual(before["digest"], after["digest"])
        root = make_root(self._temporary, role="source-library")
        scratch_before = gov.preservation_manifest(root, ["AGENTS.md"])
        (root / "AGENTS.md").write_bytes((root / "AGENTS.md").read_bytes() + b"\n")
        scratch_after = gov.preservation_manifest(root, ["AGENTS.md"])
        self.assertEqual(gov.preservation_diff(scratch_before, scratch_after), ["AGENTS.md"])

    # --- CASE 24 (S): lifecycle and dependency outcomes are deterministic.
    def test_case24_lifecycle_and_cycle_findings(self) -> None:
        superseded = copy.deepcopy(CONTRACT)
        for document in superseded["documents"]:
            if document["doc_id"] == "DW":
                document["lifecycle"] = {"state": "superseded", "effective_from": "2026-11-01", "superseded_by": "REGISTER"}
        blocked = do_resolve(contract=superseded, root=REPO_ROOT)
        self.assertEqual(blocked.status, "BLOCKED")
        self.assertTrue(
            any("superseded" in finding.message.lower() for finding in blocked.findings)
            or any(item.get("reason") == "superseded" for item in blocked.excluded_documents)
        )
        cyclic = copy.deepcopy(CONTRACT)
        cyclic["dependency_graph"].append(
            {"from_node": "doc:REGISTER", "to_doc_id": "AGENTS", "class": "required", "rule": None, "reason": "synthetic cycle"}
        )
        cyclic_result = do_resolve(contract=cyclic, root=REPO_ROOT)
        self.assertEqual(cyclic_result.status, "BLOCKED")
        serialized = json.dumps(cyclic_result.as_dict(), sort_keys=True)
        self.assertEqual(serialized, json.dumps(do_resolve(contract=cyclic, root=REPO_ROOT).as_dict(), sort_keys=True))
        self.assertTrue(any("cycle" in finding.message.lower() for finding in cyclic_result.findings))

    # --- CASE 25 (S + H UNRUN): no unsupported host/enforcement claim is accepted.
    def test_case25_host_claim_discipline(self) -> None:
        unsupported = {
            "host_product": "DeepSeek Harness Desktop",
            "host_version": "0.2.2-rc.1",
            "host_build_sha256": "5FA8A6B21BCEB8F3E99E30EFA2270EFD0CC773A11E42AA0488F804A64B34E637",
            "claim": "OBSERVED-TESTED",
            "evidence_refs": [],
            "limitations": [],
        }
        self.assertTrue(gov.validate_host_claim(unsupported))
        supported = dict(
            unsupported,
            evidence_refs=["synthetic host record"],
            tested_boundaries=["fresh-start context restore"],
            limitations=["live protected-action denial is not available on this host"],
        )
        self.assertEqual(gov.validate_host_claim(supported), [])
        host = CONTRACT["host_boundary"]["supported_hosts"][0]
        self.assertEqual(host["claim"], "OBSERVED-IDENTITY-ONLY")
        self.assertEqual(CONTRACT["enforcement_claims"]["host_plugin"], None)
        self.assertFalse(any(entry["claim"] == "OBSERVED-TESTED" for entry in CONTRACT["host_boundary"]["supported_hosts"]))
        # H case 25 cannot pass on this host by design and stays UNRUN.

    # --- CASE 26 (S): rollback restores bytes but never revoked authority.
    def test_case26_rollback_semantics(self) -> None:
        request = json.loads((FIXTURES / "rollback" / "rollback-target.json").read_text(encoding="utf-8"))
        target_contract = {"contract_version": request["target_contract_version"]}
        target_raw = gov.canonical_bytes(target_contract)
        record = gov.plan_rollback(
            current_contract=CONTRACT,
            target_contract=target_contract,
            target_contract_raw=target_raw,
            target_manifest_sha256=request["target_manifest_sha256"],
            revocation_state={
                "revoked_at_utc": "2026-11-15T00:00:00Z",
                "revocation_authority": {"kind": "OWNER_LINE", "ref": "consumer owner withdrawal"},
            },
            local_policy_paths=request["local_policy_paths"],
            triggers=request["triggers"],
        )
        self.assertTrue(record["restores_payload_bytes"])
        self.assertFalse(record["restores_authority"])
        self.assertFalse(record["revoked_authority_restored"])
        self.assertEqual(record["local_policy_deletions"], [])
        self.assertEqual(record["local_policy_retained"], sorted(request["local_policy_paths"]))
        self.assertEqual(record["to_contract_sha256"], gov.sha256_upper(target_raw))
        self.assertEqual(record["to_manifest_sha256"], request["target_manifest_sha256"])
        self.assertEqual(record["revocation_state"]["revoked_at_utc"], "2026-11-15T00:00:00Z")
        again = gov.plan_rollback(
            current_contract=CONTRACT,
            target_contract=target_contract,
            target_contract_raw=target_raw,
            target_manifest_sha256=request["target_manifest_sha256"],
            revocation_state={
                "revoked_at_utc": "2026-11-15T00:00:00Z",
                "revocation_authority": {"kind": "OWNER_LINE", "ref": "consumer owner withdrawal"},
            },
            local_policy_paths=request["local_policy_paths"],
            triggers=request["triggers"],
        )
        self.assertEqual(record, again)


class GovernanceCliTests(unittest.TestCase):
    """CLI smoke tests for the second verb family (read-only; stdout only)."""

    @classmethod
    def setUpClass(cls) -> None:
        identity = gov.load_manifest_binding(REPO_ROOT)
        cls.binding_document = {
            "schema": gov.BINDING_SCHEMA_ID,
            "manifest": {
                "path": identity["manifest_path"],
                "bytes": identity["manifest_bytes"],
                "lf": identity["manifest_lf"],
                "sha256": identity["manifest_sha256"],
            },
            "contract": {"version": CONTRACT["contract_version"], "sha256": CONTRACT_SHA},
            "source": CONTRACT["source"],
            "commands": [
                {"verb": "build", "command": "synthetic command form", "exit_code": 0},
                {"verb": "verify", "command": "synthetic command form", "exit_code": 0},
                {"verb": "check-manifest", "command": "synthetic command form", "exit_code": 0},
            ],
            "stage_a_feasibility_ref": "FEASIBILITY-P0-GOV-r3.md",
            "c1_dependency_consumption_used": True,
            "dependency_closure_verified": True,
            "non_claims": ["synthetic binding for the CLI smoke test"],
        }

    def setUp(self) -> None:
        self._temporary = make_temp_dir("gov-cli-")
        self.tmp = Path(self._temporary)
        self.addCleanup(shutil.rmtree, self._temporary, True)
        self.binding_path = self.tmp / "binding.json"
        self.binding_path.write_bytes(gov.canonical_bytes(self.binding_document))

    def run_cli(self, arguments) -> "subprocess.CompletedProcess[str]":
        return subprocess.run(
            [sys.executable, "-m", "tools.aegis_preflight", "governance", *arguments],
            cwd=str(REPO_ROOT),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
        )

    def test_validate_cli(self) -> None:
        completed = self.run_cli(["validate", "--repo-root", str(REPO_ROOT)])
        self.assertEqual(completed.returncode, 0, completed.stderr)
        parsed = json.loads(completed.stdout)
        self.assertEqual(parsed["status"], "PASS")
        self.assertEqual(parsed["contract_sha256"], CONTRACT_SHA)

    def test_render_cli_matches_committed_contract(self) -> None:
        completed = self.run_cli(["render", "--artifact", "contract", "--repo-root", str(REPO_ROOT)])
        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertEqual(completed.stdout.encode("utf-8"), CONTRACT_RAW)

    def test_resolve_cli(self) -> None:
        completed = self.run_cli(
            ["resolve", "--role", "source-library", "--route", "source-checkout", "--repo-root", str(REPO_ROOT)]
        )
        self.assertEqual(completed.returncode, 0, completed.stderr)
        parsed = json.loads(completed.stdout)
        self.assertEqual(parsed["resolution"]["status"], "RESOLVED")

    def test_receipt_and_admit_cli(self) -> None:
        receipt_run = self.run_cli(
            [
                "receipt",
                "--role", "source-library",
                "--route", "source-checkout",
                "--observation-type", "fresh-start",
                "--receipt-id", "CR-cli-smoke-0001",
                "--observed-at", DECISION_TIME,
                "--task-id", "task-55",
                "--task-ref", "task-55",
                "--task-authority-ref", "synthetic CLI authority",
                "--binding", str(self.binding_path),
                "--repo-root", str(REPO_ROOT),
            ]
        )
        self.assertEqual(receipt_run.returncode, 0, receipt_run.stderr)
        receipt = json.loads(receipt_run.stdout)["receipt"]
        self.assertEqual(receipt["packaging_manifest_binding"]["manifest_sha256"],
                         gov.load_manifest_binding(REPO_ROOT)["manifest_sha256"])
        receipt_path = self.tmp / "receipt.json"
        receipt_path.write_bytes(gov.canonical_bytes(receipt))
        admit_run = self.run_cli(
            [
                "admit",
                "--receipt", str(receipt_path),
                "--operation-class", "commit",
                "--decision-id", "AD-cli-smoke-0001",
                "--requested-at", DECISION_TIME,
                "--authority-ref", "synthetic CLI authority",
                "--current-role", "source-library",
                "--current-repo", "ModernNomad-98/Project-Aegis",
                "--repo-root", str(REPO_ROOT),
            ]
        )
        self.assertEqual(admit_run.returncode, 0, admit_run.stderr)
        self.assertEqual(json.loads(admit_run.stdout)["outcome"]["decision"], "ALLOW")

    def test_receipt_cli_requires_a_binding(self) -> None:
        completed = self.run_cli(
            [
                "receipt",
                "--role", "source-library",
                "--route", "source-checkout",
                "--observation-type", "fresh-start",
                "--receipt-id", "CR-cli-smoke-0002",
                "--observed-at", DECISION_TIME,
                "--task-id", "task-55",
                "--task-ref", "task-55",
                "--task-authority-ref", "synthetic CLI authority",
                "--repo-root", str(REPO_ROOT),
            ]
        )
        self.assertEqual(completed.returncode, 2)


def governance_budget_categories() -> tuple:
    from tools.aegis_preflight import models

    return models.BUDGET_CATEGORIES


if __name__ == "__main__":
    unittest.main()
