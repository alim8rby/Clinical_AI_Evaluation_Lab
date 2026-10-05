import unittest
from datetime import datetime

from src.failure_analysis.models import Failure, FailureSeverity
from src.failure_analysis.observatory_v2 import analyze_experiment, compare_failure_rates, dimension_summary
from src.failure_analysis.observatory_v2_service import FailureObservatoryV2


def failure(fid, run_id, qid, category, kind="Hallucination"):
    return Failure(
        failure_id=fid,
        run_id=run_id,
        question_id=qid,
        category=category,
        type=kind,
        severity=FailureSeverity.HIGH,
        description="failure",
        evidence="evidence",
        created_at=datetime(2026, 1, 1),
    )


class FailureObservatoryV2Tests(unittest.TestCase):
    def setUp(self):
        self.failures = (
            failure("f1", "r1", "q1", "GENERATION"),
            failure("f2", "r1", "q2", "SAFETY", "Missing uncertainty"),
            failure("f3", "r2", "q1", "RETRIEVAL", "Missing evidence"),
        )
        self.run_map = {"r1": "exp-a", "r2": "exp-b"}
        self.metadata = {
            "q1": {"difficulty": "easy", "question_type": "fact"},
            "q2": {"difficulty": "hard", "question_type": "safety"},
        }

    def test_experiment_analysis_enriches_frozen_failures(self):
        result = analyze_experiment(
            self.failures,
            experiment_id="exp-a",
            run_to_experiment=self.run_map,
            question_metadata=self.metadata,
        )
        self.assertEqual(result.total_failures, 2)
        self.assertEqual(result.unique_questions, 2)
        self.assertEqual(result.by_difficulty, {"easy": 1, "hard": 1})
        self.assertEqual(result.by_question_type, {"fact": 1, "safety": 1})

    def test_dimension_summary_is_deterministic(self):
        result = dimension_summary(
            self.failures,
            dimension="category",
            question_metadata=self.metadata,
        )
        self.assertEqual([item.value for item in result], ["GENERATION", "RETRIEVAL", "SAFETY"])

    def test_regression_compares_failure_rates(self):
        result = compare_failure_rates(
            self.failures[:2],
            self.failures[2:],
            baseline_question_count=2,
            candidate_question_count=2,
        )
        generation = next(item for item in result if item.category == "GENERATION")
        retrieval = next(item for item in result if item.category == "RETRIEVAL")
        self.assertAlmostEqual(generation.baseline_rate, 0.5)
        self.assertAlmostEqual(generation.candidate_rate, 0.0)
        self.assertAlmostEqual(retrieval.rate_difference, 0.5)

    def test_service_scopes_dimensions_and_regressions(self):
        observatory = FailureObservatoryV2(
            self.failures, self.run_map, self.metadata
        )
        self.assertEqual(
            observatory.for_experiment("exp-a").total_failures, 2
        )
        safety = observatory.by_dimension("question_type", experiment_id="exp-a")
        self.assertEqual([(x.value, x.failure_count) for x in safety], [("fact", 1), ("safety", 1)])


if __name__ == "__main__":
    unittest.main()
