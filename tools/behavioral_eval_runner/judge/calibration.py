"""Deterministic/mock calibration harness (WP-2B-2; prompt section 12).

- The dataset contract is the minimum versioned structure for FUTURE
  human-labeled calibration data; this phase's fixtures are clearly labeled
  SYNTHETIC_MOCK and are never the owner-approved measured dataset.
- Metrics (confusion matrix, agreement, false-PASS/FAIL, abstention,
  JUDGE_ERROR, separate CRITICAL false-PASS) are computed deterministically
  over recorded mock verdicts with explicit denominators.
- Thresholds are EXPLICIT INPUTS with the only representable status
  MOCK_UNRATIFIED (OD-1 is OPEN; a RATIFIED status does not exist here).
  Under-threshold results are rejected; missing thresholds cannot produce
  eligibility; nothing here can ever be baseline-eligible.
- Every drift trigger invalidates prior mock-eligibility state.

NON-CLAIM: this harness proves only that metric computation and threshold
enforcement work over recorded deterministic inputs. It does not prove any
real judge is calibrated."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping

from .. import GRADING_SCHEMA_VERSION
from ..canonical import sha256_of_obj
from ..enums import RiskClass, StrictEnum
from ..errors import SchemaValidationError

HARNESS_NON_CLAIM = (
    "Deterministic MOCK metrics over recorded synthetic inputs; NO MEASURED "
    "judge calibration exists or is claimed; OD-1 remains OPEN; R2 remains "
    "BLOCKED; no baseline-eligible semantic verdict may result."
)


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise SchemaValidationError(message)


class CalibrationProvenance(StrictEnum):
    """This phase can only represent synthetic/mock provenance; the future
    human-labeled value exists so the CONTRACT is complete, but no fixture
    here may claim it as a measured dataset."""

    SYNTHETIC_MOCK = "SYNTHETIC_MOCK"
    HUMAN_LABELED_FUTURE = "HUMAN_LABELED_FUTURE"


class CalibrationLabel(StrictEnum):
    PASS = "PASS"
    FAIL = "FAIL"
    ABSTAIN = "ABSTAIN"


class ObservedOutcome(StrictEnum):
    PASS = "PASS"
    FAIL = "FAIL"
    ABSTAIN = "ABSTAIN"
    JUDGE_ERROR = "JUDGE_ERROR"


class SplitFold(StrictEnum):
    TRAIN = "TRAIN"
    HOLDOUT = "HOLDOUT"


class ThresholdStatus(StrictEnum):
    """MOCK_UNRATIFIED is the ONLY representable status: OD-1 is OPEN and no
    code in this phase may represent a ratified threshold set."""

    MOCK_UNRATIFIED = "MOCK_UNRATIFIED"


class ThresholdOutcome(StrictEnum):
    MOCK_THRESHOLDS_MET = "MOCK_THRESHOLDS_MET"
    REJECTED_UNDER_THRESHOLD = "REJECTED_UNDER_THRESHOLD"
    REJECTED_NO_THRESHOLDS = "REJECTED_NO_THRESHOLDS"
    REJECTED_INDETERMINATE = "REJECTED_INDETERMINATE"


class DriftTrigger(StrictEnum):
    JUDGE_MODEL_CHANGE = "JUDGE_MODEL_CHANGE"
    JUDGE_VERSION_CHANGE = "JUDGE_VERSION_CHANGE"
    SYSTEM_POLICY_CHANGE = "SYSTEM_POLICY_CHANGE"
    RUBRIC_CHANGE = "RUBRIC_CHANGE"
    RUBRIC_DERIVATION_CHANGE = "RUBRIC_DERIVATION_CHANGE"
    DATASET_CHANGE = "DATASET_CHANGE"
    DATASET_LABEL_CHANGE = "DATASET_LABEL_CHANGE"
    VERDICT_SCHEMA_CHANGE = "VERDICT_SCHEMA_CHANGE"


@dataclass(frozen=True, slots=True)
class CalibrationEntry:
    entry_id: str
    control_id: str
    risk_class: RiskClass
    expected_label: CalibrationLabel
    input_artifact_refs: tuple[str, ...]
    split: SplitFold
    assertion_uid: str | None = None

    def validate(self) -> None:
        _require(
            isinstance(self.entry_id, str) and bool(self.entry_id),
            "entry_id required",
        )
        _require(
            isinstance(self.control_id, str) and bool(self.control_id),
            "control_id required",
        )
        _require(isinstance(self.risk_class, RiskClass), "risk_class enum required")
        _require(
            isinstance(self.expected_label, CalibrationLabel),
            "expected_label enum required",
        )
        _require(
            isinstance(self.input_artifact_refs, tuple)
            and all(isinstance(ref, str) and ref for ref in self.input_artifact_refs),
            "input_artifact_refs must be a tuple of non-empty strings",
        )
        _require(isinstance(self.split, SplitFold), "split enum required")
        if self.assertion_uid is not None:
            _require(
                isinstance(self.assertion_uid, str) and bool(self.assertion_uid),
                "assertion_uid must be non-empty or None",
            )

    def to_dict(self) -> dict[str, Any]:
        return {
            "entry_id": self.entry_id,
            "control_id": self.control_id,
            "risk_class": self.risk_class.value,
            "expected_label": self.expected_label.value,
            "input_artifact_refs": list(self.input_artifact_refs),
            "split": self.split.value,
            "assertion_uid": self.assertion_uid,
        }

    _KEYS = frozenset(
        {
            "entry_id",
            "control_id",
            "risk_class",
            "expected_label",
            "input_artifact_refs",
            "split",
            "assertion_uid",
        }
    )

    @classmethod
    def from_dict(cls, payload: Mapping[str, Any]) -> "CalibrationEntry":
        unknown = set(payload) - cls._KEYS
        _require(not unknown, f"CalibrationEntry: unknown keys {sorted(unknown)}")
        entry = cls(
            entry_id=payload.get("entry_id", ""),
            control_id=payload.get("control_id", ""),
            risk_class=RiskClass.parse(payload.get("risk_class")),
            expected_label=CalibrationLabel.parse(payload.get("expected_label")),
            input_artifact_refs=tuple(payload.get("input_artifact_refs", ())),
            split=SplitFold.parse(payload.get("split")),
            assertion_uid=payload.get("assertion_uid"),
        )
        entry.validate()
        return entry


@dataclass(frozen=True, slots=True)
class CalibrationDataset:
    dataset_id: str
    version: str
    labeler_role: str
    provenance: CalibrationProvenance
    entries: tuple[CalibrationEntry, ...]
    schema_version: str = GRADING_SCHEMA_VERSION

    def validate(self) -> None:
        _require(
            isinstance(self.dataset_id, str) and bool(self.dataset_id),
            "dataset_id required",
        )
        _require(
            isinstance(self.version, str) and bool(self.version), "version required"
        )
        _require(
            isinstance(self.labeler_role, str) and bool(self.labeler_role),
            "labeler_role (role only, no personal data) required",
        )
        _require(
            isinstance(self.provenance, CalibrationProvenance),
            "provenance enum required",
        )
        _require(
            isinstance(self.entries, tuple) and len(self.entries) > 0,
            "entries must be non-empty",
        )
        seen: set[str] = set()
        for entry in self.entries:
            entry.validate()
            _require(
                entry.entry_id not in seen, f"duplicate entry_id {entry.entry_id!r}"
            )
            seen.add(entry.entry_id)
        _require(
            self.schema_version == GRADING_SCHEMA_VERSION,
            f"schema_version must be {GRADING_SCHEMA_VERSION}",
        )

    def dataset_sha256(self) -> str:
        return sha256_of_obj(self.to_dict())

    def to_dict(self) -> dict[str, Any]:
        return {
            "dataset_id": self.dataset_id,
            "version": self.version,
            "labeler_role": self.labeler_role,
            "provenance": self.provenance.value,
            "entries": [entry.to_dict() for entry in self.entries],
            "schema_version": self.schema_version,
        }

    _KEYS = frozenset(
        {
            "dataset_id",
            "version",
            "labeler_role",
            "provenance",
            "entries",
            "schema_version",
        }
    )

    @classmethod
    def from_dict(cls, payload: Mapping[str, Any]) -> "CalibrationDataset":
        unknown = set(payload) - cls._KEYS
        _require(not unknown, f"CalibrationDataset: unknown keys {sorted(unknown)}")
        _require(
            "schema_version" in payload,
            "CalibrationDataset requires an explicit schema_version "
            "(a missing version is never silently defaulted)",
        )
        dataset = cls(
            dataset_id=payload.get("dataset_id", ""),
            version=payload.get("version", ""),
            labeler_role=payload.get("labeler_role", ""),
            provenance=CalibrationProvenance.parse(payload.get("provenance")),
            entries=tuple(
                CalibrationEntry.from_dict(entry)
                for entry in payload.get("entries", ())
            ),
            schema_version=payload.get("schema_version", ""),
        )
        dataset.validate()
        return dataset


@dataclass(frozen=True, slots=True)
class CalibrationReport:
    dataset_id: str
    dataset_version: str
    dataset_sha256_value: str
    provenance: CalibrationProvenance
    confusion_matrix: Mapping[str, Mapping[str, int]]
    metrics: Mapping[str, float | None]
    sample_counts: Mapping[str, int]
    non_claim: str = HARNESS_NON_CLAIM
    schema_version: str = GRADING_SCHEMA_VERSION

    def to_dict(self) -> dict[str, Any]:
        return {
            "dataset_id": self.dataset_id,
            "dataset_version": self.dataset_version,
            "dataset_sha256": self.dataset_sha256_value,
            "provenance": self.provenance.value,
            "confusion_matrix": {
                expected: dict(observed)
                for expected, observed in self.confusion_matrix.items()
            },
            "metrics": dict(self.metrics),
            "sample_counts": dict(self.sample_counts),
            "non_claim": self.non_claim,
            "schema_version": self.schema_version,
        }

    def report_sha256(self) -> str:
        return sha256_of_obj(self.to_dict())


def compute_calibration_metrics(
    dataset: CalibrationDataset,
    observed: Mapping[str, ObservedOutcome],
) -> CalibrationReport:
    """Deterministic metrics over recorded mock outcomes (denominators
    explicit; a metric with denominator 0 is None, never silently 0)."""
    dataset.validate()
    entry_ids = {entry.entry_id for entry in dataset.entries}
    observed_ids = set(observed)
    missing = entry_ids - observed_ids
    _require(not missing, f"missing observed outcomes for {sorted(missing)}")
    extra = observed_ids - entry_ids
    _require(not extra, f"observed outcomes for unknown entries {sorted(extra)}")
    for entry_id, outcome in observed.items():
        _require(
            isinstance(outcome, ObservedOutcome),
            f"observed[{entry_id}] must be ObservedOutcome",
        )

    matrix: dict[str, dict[str, int]] = {
        label.value: {outcome.value: 0 for outcome in ObservedOutcome}
        for label in CalibrationLabel
    }
    total = len(dataset.entries)
    agree = 0
    expected_pass = expected_fail = expected_abstain = 0
    false_pass = false_fail = abstain_count = judge_error_count = 0
    critical_expected_fail = critical_false_pass = 0

    for entry in dataset.entries:
        outcome = observed[entry.entry_id]
        matrix[entry.expected_label.value][outcome.value] += 1
        if entry.expected_label.value == outcome.value:
            agree += 1
        if entry.expected_label is CalibrationLabel.PASS:
            expected_pass += 1
            if outcome is ObservedOutcome.FAIL:
                false_fail += 1
        elif entry.expected_label is CalibrationLabel.FAIL:
            expected_fail += 1
            if outcome is ObservedOutcome.PASS:
                false_pass += 1
            if entry.risk_class is RiskClass.CRITICAL:
                critical_expected_fail += 1
                if outcome is ObservedOutcome.PASS:
                    critical_false_pass += 1
        else:
            expected_abstain += 1
        if outcome is ObservedOutcome.ABSTAIN:
            abstain_count += 1
        if outcome is ObservedOutcome.JUDGE_ERROR:
            judge_error_count += 1

    def _rate(numerator: int, denominator: int) -> float | None:
        return numerator / denominator if denominator else None

    metrics: dict[str, float | None] = {
        "agreement_rate": _rate(agree, total),
        "false_pass_rate": _rate(false_pass, expected_fail),
        "false_fail_rate": _rate(false_fail, expected_pass),
        "abstention_rate": _rate(abstain_count, total),
        "judge_error_rate": _rate(judge_error_count, total),
        "critical_false_pass_rate": _rate(
            critical_false_pass, critical_expected_fail
        ),
    }
    sample_counts = {
        "total": total,
        "expected_pass": expected_pass,
        "expected_fail": expected_fail,
        "expected_abstain": expected_abstain,
        "observed_abstain": abstain_count,
        "observed_judge_error": judge_error_count,
        "critical_expected_fail": critical_expected_fail,
        "critical_false_pass": critical_false_pass,
    }
    return CalibrationReport(
        dataset_id=dataset.dataset_id,
        dataset_version=dataset.version,
        dataset_sha256_value=dataset.dataset_sha256(),
        provenance=dataset.provenance,
        confusion_matrix=matrix,
        metrics=metrics,
        sample_counts=sample_counts,
    )


@dataclass(frozen=True, slots=True)
class CalibrationThresholds:
    """Explicit threshold inputs; the ONLY status is MOCK_UNRATIFIED."""

    status: ThresholdStatus
    min_agreement_rate: float
    max_false_pass_rate: float
    max_false_fail_rate: float
    max_abstention_rate: float
    max_judge_error_rate: float
    max_critical_false_pass_rate: float

    def validate(self) -> None:
        _require(
            isinstance(self.status, ThresholdStatus),
            "threshold status must be ThresholdStatus (MOCK_UNRATIFIED)",
        )
        for name in (
            "min_agreement_rate",
            "max_false_pass_rate",
            "max_false_fail_rate",
            "max_abstention_rate",
            "max_judge_error_rate",
            "max_critical_false_pass_rate",
        ):
            value = getattr(self, name)
            _require(
                isinstance(value, (int, float))
                and not isinstance(value, bool)
                and 0.0 <= float(value) <= 1.0,
                f"{name} must be a number in [0, 1]",
            )

    _KEYS = frozenset(
        {
            "status",
            "min_agreement_rate",
            "max_false_pass_rate",
            "max_false_fail_rate",
            "max_abstention_rate",
            "max_judge_error_rate",
            "max_critical_false_pass_rate",
        }
    )

    @classmethod
    def from_dict(cls, payload: Mapping[str, Any]) -> "CalibrationThresholds":
        unknown = set(payload) - cls._KEYS
        _require(not unknown, f"CalibrationThresholds: unknown keys {sorted(unknown)}")
        thresholds = cls(
            status=ThresholdStatus.parse(payload.get("status")),
            min_agreement_rate=payload.get("min_agreement_rate", -1),
            max_false_pass_rate=payload.get("max_false_pass_rate", -1),
            max_false_fail_rate=payload.get("max_false_fail_rate", -1),
            max_abstention_rate=payload.get("max_abstention_rate", -1),
            max_judge_error_rate=payload.get("max_judge_error_rate", -1),
            max_critical_false_pass_rate=payload.get(
                "max_critical_false_pass_rate", -1
            ),
        )
        thresholds.validate()
        return thresholds


@dataclass(frozen=True, slots=True)
class ThresholdEvaluation:
    outcome: ThresholdOutcome
    baseline_eligible: bool
    failed_criteria: tuple[str, ...]
    eligibility_note: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "outcome": self.outcome.value,
            "baseline_eligible": self.baseline_eligible,
            "failed_criteria": list(self.failed_criteria),
            "eligibility_note": self.eligibility_note,
        }


_NO_ELIGIBILITY_NOTE = (
    "MOCK/UNRATIFIED evaluation: no baseline-eligible semantic verdict may "
    "result; OD-1 remains OPEN and measured calibration belongs to the "
    "blocked WP-2B-3 gate."
)


def evaluate_thresholds(
    report: CalibrationReport,
    thresholds: CalibrationThresholds | None,
) -> ThresholdEvaluation:
    """Enforce explicit mock thresholds; baseline_eligible is ALWAYS False."""
    if thresholds is None:
        return ThresholdEvaluation(
            outcome=ThresholdOutcome.REJECTED_NO_THRESHOLDS,
            baseline_eligible=False,
            failed_criteria=("no thresholds supplied",),
            eligibility_note=_NO_ELIGIBILITY_NOTE,
        )
    thresholds.validate()
    metrics = report.metrics
    checks: tuple[tuple[str, float | None, float, bool], ...] = (
        ("agreement_rate", metrics["agreement_rate"], thresholds.min_agreement_rate, True),
        ("false_pass_rate", metrics["false_pass_rate"], thresholds.max_false_pass_rate, False),
        ("false_fail_rate", metrics["false_fail_rate"], thresholds.max_false_fail_rate, False),
        ("abstention_rate", metrics["abstention_rate"], thresholds.max_abstention_rate, False),
        ("judge_error_rate", metrics["judge_error_rate"], thresholds.max_judge_error_rate, False),
        (
            "critical_false_pass_rate",
            metrics["critical_false_pass_rate"],
            thresholds.max_critical_false_pass_rate,
            False,
        ),
    )
    indeterminate = [name for name, value, _limit, _is_min in checks if value is None]
    if indeterminate:
        return ThresholdEvaluation(
            outcome=ThresholdOutcome.REJECTED_INDETERMINATE,
            baseline_eligible=False,
            failed_criteria=tuple(
                f"{name} has no denominator (indeterminate)" for name in indeterminate
            ),
            eligibility_note=_NO_ELIGIBILITY_NOTE,
        )
    failed: list[str] = []
    for name, value, limit, is_min in checks:
        assert value is not None
        if is_min and value < limit:
            failed.append(f"{name}={value} below minimum {limit}")
        if not is_min and value > limit:
            failed.append(f"{name}={value} above maximum {limit}")
    if failed:
        return ThresholdEvaluation(
            outcome=ThresholdOutcome.REJECTED_UNDER_THRESHOLD,
            baseline_eligible=False,
            failed_criteria=tuple(failed),
            eligibility_note=_NO_ELIGIBILITY_NOTE,
        )
    return ThresholdEvaluation(
        outcome=ThresholdOutcome.MOCK_THRESHOLDS_MET,
        baseline_eligible=False,
        failed_criteria=(),
        eligibility_note=_NO_ELIGIBILITY_NOTE,
    )


@dataclass(frozen=True, slots=True)
class MockEligibilityState:
    """The (never-eligible) recorded state of a mock evaluation."""

    state: str
    baseline_eligible: bool
    trigger: DriftTrigger | None = None

    @classmethod
    def from_evaluation(cls, evaluation: ThresholdEvaluation) -> "MockEligibilityState":
        return cls(
            state=evaluation.outcome.value,
            baseline_eligible=False,
            trigger=None,
        )


def apply_drift_trigger(
    state: MockEligibilityState, trigger: DriftTrigger
) -> MockEligibilityState:
    """ANY drift trigger invalidates prior mock state; future recalibration
    (and, for real use, the WP-2B-3 measured gate) is required."""
    _require(isinstance(trigger, DriftTrigger), "trigger must be DriftTrigger")
    return MockEligibilityState(
        state="INVALIDATED_REQUIRES_RECALIBRATION",
        baseline_eligible=False,
        trigger=trigger,
    )
