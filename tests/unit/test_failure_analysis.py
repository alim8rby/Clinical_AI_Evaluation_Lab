import tempfile
import unittest
from pathlib import Path

from src.failure_analysis.analysis import (
    analyze_store,
    filter_failures,
    summarize_failures,
)
from src.failure_analysis.models import Failure, FailureSeverity
from src.failure_analysis.store import FailureStore


def make_failure(
    failure_id: str,
    *,
    category: str = "GENERATION",
    failure_type: str = "Hallucination",
    severity: FailureSeverity = FailureSeverity.HIGH,
    run_id: str = "run-1",
    question_id: str = "cq-001",
) -> Failure:
    return Failure(
        failure_id=failure_id,
        run_id=run_id,
        question_id=question_id,
        category=category,
        type=failure_type,
        severity=severity,
        description="Failure description.",
        evidence="Failure evidence.",
    )


class FailureAnalysisTests(unittest.TestCase):
    def test_filter_by_multiple_dimensions(self):
        failures = [
            make_failure("f-1"),
            make_failure("f-2", category="RETRIEVAL", severity=FailureSeverity.MEDIUM),
            make_failure("f-3", run_id="run-2"),
        ]

        result = filter_failures(
            failures,
            category="GENERATION",
            severity=FailureSeverity.HIGH,
            run_id="run-1",
        )

        self.assertEqual([failure.failure_id for failure in result], ["f-1"])

    def test_filter_accepts_string_severity(self):
        result = filter_failures(
            [make_failure("f-1")],
            severity="HIGH",
        )
        self.assertEqual(len(result), 1)

    def test_filter_rejects_empty_filter(self):
        with self.assertRaises(ValueError):
            filter_failures([make_failure("f-1")], category="")

    def test_filter_rejects_invalid_severity(self):
        with self.assertRaises(ValueError):
            filter_failures([make_failure("f-1")], severity="URGENT")

    def test_summary_counts_are_deterministic(self):
        failures = [
            make_failure("f-2", category="RETRIEVAL", severity=FailureSeverity.MEDIUM),
            make_failure("f-1"),
            make_failure("f-3", failure_type="Missing uncertainty", severity=FailureSeverity.MEDIUM),
        ]

        summary = summarize_failures(failures)

        self.assertEqual(summary.total, 3)
        self.assertEqual(summary.by_category, {"GENERATION": 2, "RETRIEVAL": 1})
        self.assertEqual(
            summary.by_type,
            {"Hallucination": 2, "Missing uncertainty": 1},
        )

    def test_store_analysis_uses_persisted_records(self):
        with tempfile.TemporaryDirectory() as directory:
            store = FailureStore(Path(directory) / "failures.json")
            store.save_many(
                [
                    make_failure("f-1"),
                    make_failure("f-2", category="RETRIEVAL", severity=FailureSeverity.MEDIUM),
                ]
            )

            summary = analyze_store(store, category="RETRIEVAL")

            self.assertEqual(summary.total, 1)
            self.assertEqual(summary.by_category, {"RETRIEVAL": 1})
