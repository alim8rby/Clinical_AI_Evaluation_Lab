import tempfile
import unittest
from datetime import datetime, timezone

from src.evaluation.benchmark import BenchmarkQuestion
from src.evaluation.grounding_metrics import GroundingMetrics
from src.evaluation.reliability_metrics import ReliabilityMetrics
from src.evaluation.retrieval_metrics import RetrievalMetrics
from src.experiments.models import ExperimentResult, RunRecord
from src.failure_analysis.models import FailureSeverity
from src.failure_analysis.observatory import FailureQuery
from src.failure_analysis.store import FailureStore
from src.failure_analysis.regression import assert_regression_suite
from src.failure_analysis.workflow import process_result


class FailureWorkflowIntegrationTests(unittest.TestCase):
    def setUp(self):
        self.question = BenchmarkQuestion(
            question_id="cq-integration-001",
            question="What is the benchmark question?",
            domain="depression",
            difficulty="medium",
            expected_evidence=("chunk-expected",),
            reference_answer="The reference answer.",
            key_concepts=("reference",),
        )
        self.run = RunRecord(
            run_id="run-integration-001",
            experiment_id="exp-integration-001",
            question_id=self.question.question_id,
            status="completed",
            started_at=datetime(2026, 1, 1, tzinfo=timezone.utc),
            finished_at=datetime(2026, 1, 1, 0, 0, 1, tzinfo=timezone.utc),
            latency_ms=100.0,
            input_tokens=10,
            output_tokens=20,
            cost=0.01,
            error=None,
        )

    def _result(self):
        retrieval = type("Retrieval", (), {
            "metrics": RetrievalMetrics(
                precision_at_k=0.0,
                recall_at_k=0.0,
                mrr=0.0,
                ndcg=0.0,
                k=5,
                retrieved_count=0,
                expected_count=1,
            )
        })()
        grounding = type("Grounding", (), {
            "metrics": GroundingMetrics(
                citation_coverage=1.0,
                citation_validity=1.0,
                faithfulness=0.0,
                unsupported_claim_rate=1.0,
            )
        })()
        reliability = type("Reliability", (), {
            "metrics": ReliabilityMetrics(
                hallucination_rate=1.0,
                critical_error_rate=0.0,
                uncertainty_handling=1.0,
                unsupported_recommendation_rate=0.0,
            )
        })()
        return ExperimentResult(
            run=self.run,
            retrieval=retrieval,
            grounding=grounding,
            reliability=reliability,
        )

    def test_result_flows_from_classification_to_store_and_observatory(self):
        with tempfile.TemporaryDirectory() as tmp:
            store = FailureStore(f"{tmp}/failures.json")
            output = process_result(
                self.question,
                self._result(),
                store,
                created_at=datetime(2026, 1, 1, tzinfo=timezone.utc),
            )

            self.assertEqual(len(output.failures), 2)
            self.assertEqual(store.count(), 2)
            self.assertEqual(len(output.result.failures), 2)

            from src.failure_analysis.workflow import build_observatory
            observatory = build_observatory(store)
            snapshot = observatory.snapshot()
            self.assertEqual(snapshot.summary.total, 2)
            self.assertEqual(
                snapshot.summary.by_category,
                {"GENERATION": 1, "RETRIEVAL": 1},
            )

            critical = observatory.list_failures(
                FailureQuery(severity=FailureSeverity.HIGH)
            )
            self.assertEqual(len(critical), 1)
            self.assertEqual(critical[0].type, "Hallucination")

    def test_regression_guard_remains_green(self):
        assert_regression_suite()

    def test_processing_same_result_is_idempotent(self):
        with tempfile.TemporaryDirectory() as tmp:
            store = FailureStore(f"{tmp}/failures.json")
            first = process_result(self.question, self._result(), store)
            second = process_result(self.question, self._result(), store)

            self.assertEqual(first.failures, second.failures)
            self.assertEqual(store.count(), 2)


if __name__ == "__main__":
    unittest.main()
