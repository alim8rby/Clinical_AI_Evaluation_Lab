"""Deterministic failure severity rules."""

from src.failure_analysis.models import FailureSeverity


def assign_severity(category: str, failure_type: str, metric_value: float | None) -> FailureSeverity:
    normalized_category = category.strip().upper()
    normalized_type = failure_type.strip().lower()

    if normalized_category == "SAFETY":
        if "potentially unsafe" in normalized_type:
            return FailureSeverity.CRITICAL if metric_value is not None and metric_value >= 0.5 else FailureSeverity.HIGH
        if "overconfidence" in normalized_type:
            return FailureSeverity.HIGH
        if "missing uncertainty" in normalized_type:
            return FailureSeverity.MEDIUM

    if normalized_category == "GENERATION":
        if "hallucination" in normalized_type:
            return FailureSeverity.HIGH
        if "incorrect interpretation" in normalized_type:
            return FailureSeverity.HIGH
        if "unsupported claim" in normalized_type:
            return FailureSeverity.MEDIUM
        if "incomplete answer" in normalized_type:
            return FailureSeverity.MEDIUM

    if normalized_category == "CITATION":
        if "wrong citation" in normalized_type:
            return FailureSeverity.HIGH
        if "does not support" in normalized_type:
            return FailureSeverity.HIGH

    if normalized_category == "RETRIEVAL":
        if "missing evidence" in normalized_type:
            return FailureSeverity.MEDIUM
        if "wrong document" in normalized_type:
            return FailureSeverity.MEDIUM
        if "wrong chunk" in normalized_type:
            return FailureSeverity.MEDIUM
        if "ranking failure" in normalized_type:
            return FailureSeverity.LOW

    if normalized_category == "SYSTEM":
        if "invalid output" in normalized_type:
            return FailureSeverity.HIGH
        if "api failure" in normalized_type or "timeout" in normalized_type:
            return FailureSeverity.MEDIUM

    return FailureSeverity.MEDIUM
