"""Human calibration utilities for semantic evaluation.

Human labels are treated as reference annotations, not clinical ground truth.
"""
from __future__ import annotations

from dataclasses import dataclass
from math import fsum


CALIBRATION_VERSION = "calibration-v1"
DIMENSIONS = ("correctness", "completeness", "relevance", "faithfulness", "unsupported_claim_rate")


class CalibrationValidationError(ValueError):
    """Raised when calibration data is invalid."""


@dataclass(frozen=True)
class CalibrationLabel:
    item_id: str
    dimension: str
    human_score: float
    model_score: float

    def __post_init__(self) -> None:
        if not self.item_id.strip():
            raise CalibrationValidationError("item_id must not be empty")
        if self.dimension not in DIMENSIONS:
            raise CalibrationValidationError("invalid calibration dimension")
        for name, value in (("human_score", self.human_score), ("model_score", self.model_score)):
            if not 0.0 <= value <= 1.0:
                raise CalibrationValidationError(f"{name} must be between 0 and 1")


@dataclass(frozen=True)
class CalibrationResult:
    dimension: str
    sample_count: int
    mean_absolute_error: float
    mean_bias: float
    within_tolerance_rate: float
    tolerance: float
    calibration_version: str = CALIBRATION_VERSION


def validate_calibration_payload(payload: object) -> list[CalibrationLabel]:
    if not isinstance(payload, list):
        raise CalibrationValidationError("calibration data must be a list")
    labels: list[CalibrationLabel] = []
    seen: set[tuple[str, str]] = set()
    required = {"item_id", "dimension", "human_score", "model_score"}
    for item in payload:
        if not isinstance(item, dict) or set(item) != required:
            raise CalibrationValidationError("calibration label has invalid fields")
        try:
            label = CalibrationLabel(
                item_id=item["item_id"],
                dimension=item["dimension"],
                human_score=float(item["human_score"]),
                model_score=float(item["model_score"]),
            )
        except (TypeError, ValueError) as exc:
            raise CalibrationValidationError("invalid calibration score") from exc
        key = (label.item_id, label.dimension)
        if key in seen:
            raise CalibrationValidationError("duplicate calibration label")
        seen.add(key)
        labels.append(label)
    return labels


def evaluate_calibration(
    labels: list[CalibrationLabel],
    *,
    tolerance: float = 0.20,
) -> list[CalibrationResult]:
    if not 0.0 <= tolerance <= 1.0:
        raise CalibrationValidationError("tolerance must be between 0 and 1")
    results: list[CalibrationResult] = []
    for dimension in DIMENSIONS:
        subset = [label for label in labels if label.dimension == dimension]
        if not subset:
            continue
        errors = [abs(label.model_score - label.human_score) for label in subset]
        biases = [label.model_score - label.human_score for label in subset]
        results.append(
            CalibrationResult(
                dimension=dimension,
                sample_count=len(subset),
                mean_absolute_error=fsum(errors) / len(errors),
                mean_bias=fsum(biases) / len(biases),
                within_tolerance_rate=sum(error <= tolerance for error in errors) / len(errors),
                tolerance=tolerance,
            )
        )
    return results
