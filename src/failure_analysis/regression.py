"""Deterministic regression checks for failure classification and severity."""

from dataclasses import dataclass

from .models import FailureSeverity


@dataclass(frozen=True)
class RegressionCase:
    case_id: str
    category: str
    failure_type: str
    metric_value: float | None
    expected_severity: FailureSeverity

    def __post_init__(self) -> None:
        for name, value in (("case_id", self.case_id), ("category", self.category), ("failure_type", self.failure_type)):
            if not isinstance(value, str) or not value.strip():
                raise ValueError(f"{name} must not be empty")


@dataclass(frozen=True)
class RegressionResult:
    case_id: str
    passed: bool
    expected_severity: FailureSeverity
    actual_severity: FailureSeverity | None
    reason: str


def default_regression_cases() -> tuple[RegressionCase, ...]:
    return (
        RegressionCase("retrieval-missing-evidence", "RETRIEVAL", "Missing evidence", 0.0, FailureSeverity.MEDIUM),
        RegressionCase("retrieval-ranking-failure", "RETRIEVAL", "Ranking failure", 0.0, FailureSeverity.LOW),
        RegressionCase("generation-hallucination", "GENERATION", "Hallucination", 0.75, FailureSeverity.HIGH),
        RegressionCase("generation-unsupported-claim", "GENERATION", "Unsupported claim", 0.25, FailureSeverity.MEDIUM),
        RegressionCase("citation-wrong-citation", "CITATION", "Wrong citation", 0.5, FailureSeverity.HIGH),
        RegressionCase("safety-missing-uncertainty", "SAFETY", "Missing uncertainty", 0.0, FailureSeverity.MEDIUM),
        RegressionCase("safety-unsafe-high", "SAFETY", "Potentially unsafe output", 0.5, FailureSeverity.CRITICAL),
        RegressionCase("safety-unsafe-low", "SAFETY", "Potentially unsafe output", 0.25, FailureSeverity.HIGH),
        RegressionCase("system-timeout", "SYSTEM", "Timeout", None, FailureSeverity.MEDIUM),
    )


def evaluate_regression_case(case: RegressionCase, assigner) -> RegressionResult:
    actual = assigner(case.category, case.failure_type, case.metric_value)
    passed = actual == case.expected_severity
    reason = "matched expected severity" if passed else f"expected {case.expected_severity.value}, got {actual.value}"
    return RegressionResult(case.case_id, passed, case.expected_severity, actual, reason)


def run_regression_suite(cases=None, *, assigner=None) -> tuple[RegressionResult, ...]:
    from .severity import assign_severity
    selected = tuple(default_regression_cases() if cases is None else cases)
    implementation = assign_severity if assigner is None else assigner
    return tuple(evaluate_regression_case(case, implementation) for case in selected)


def assert_regression_suite(cases=None, *, assigner=None) -> None:
    results = run_regression_suite(cases, assigner=assigner)
    failures = [result for result in results if not result.passed]
    if failures:
        details = "; ".join(f"{item.case_id}: {item.reason}" for item in failures)
        raise AssertionError(f"failure regression suite failed: {details}")
