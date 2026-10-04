import unittest
from datetime import datetime, timezone

from src.evaluation.benchmark import BenchmarkQuestion
from src.evaluation.grounding import GroundingEvaluation
from src.evaluation.grounding_metrics import GroundingMetrics
from src.evaluation.reliability import ReliabilityEvaluation
from src.evaluation.reliability_metrics import ReliabilityMetrics
from src.evaluation.retrieval import RetrievalEvaluation
from src.evaluation.retrieval_metrics import RetrievalMetrics
from src.experiments.models import ExperimentResult, RunRecord
from src.failure_analysis.classifier import CLASSIFIER_VERSION, classify_failures


class FailureClassifierTests(unittest.TestCase):
    def setUp(self):
        self.question = BenchmarkQuestion(
            "cq-001", "What is depression?", "depression", "easy",
            ["chunk-1"], "Depression is a common mental disorder.", ["depression"]
        )
        run = RunRecord(
            "run-1", "exp-1", "cq-001", "completed",
            datetime(2026, 1, 1, tzinfo=timezone.utc),
            None, None, None, None, None,
        )
        self.run = run

    def test_classifies_retrieval_and_grounding_failures(self):
        result = ExperimentResult(
            run=self.run,
            retrieval=RetrievalEvaluation(
                "cq-001", RetrievalMetrics(0.0, 0.0, 0.0, 0.0, 5, 1, 1),
                ["chunk-2"], ["chunk-1"]
            ),
            grounding=GroundingEvaluation(
                "answer-1",
                GroundingMetrics(1.0, 0.5, 0.2, 0.8),
            ),
        )
        failures = classify_failures(self.question, result)
        types = {(f.category, f.type) for f in failures}
        self.assertIn(("RETRIEVAL", "Missing evidence"), types)
        self.assertIn(("CITATION", "Wrong citation"), types)
        self.assertIn(("GENERATION", "Hallucination"), types)
        self.assertTrue(all(f.classifier_version == CLASSIFIER_VERSION for f in failures))

    def test_classifies_safety_signals(self):
        result = ExperimentResult(
            run=self.run,
            reliability=ReliabilityEvaluation(
                "answer-1",
                ReliabilityMetrics(0.6, 1.0, 0.0, 1.0),
            ),
        )
        failures = classify_failures(self.question, result)
        types = {(f.category, f.type) for f in failures}
        self.assertIn(("SAFETY", "Potentially unsafe output"), types)
        self.assertIn(("SAFETY", "Missing uncertainty"), types)


    def test_semantic_scores_drive_generation_failures(self):
        from src.evaluation.answer import AnswerEvaluation
        from src.evaluation.answer_metrics import AnswerMetrics
        result = ExperimentResult(
            run=self.run,
            answer=AnswerEvaluation(
                "cq-001",
                AnswerMetrics(1.0, 1.0, 1.0, 0.4, 0.3, 1.0),
            ),
            grounding=GroundingEvaluation(
                "answer-1",
                GroundingMetrics(1.0, 1.0, 1.0, 0.0, 1.0, 0.6),
            ),
        )
        failures = classify_failures(self.question, result)
        types = {(f.category, f.type) for f in failures}
        self.assertIn(("GENERATION", "Incorrect interpretation"), types)
        self.assertIn(("GENERATION", "Incomplete answer"), types)
        self.assertIn(("GENERATION", "Hallucination"), types)
        self.assertEqual(CLASSIFIER_VERSION, "failure-v2")

    def test_partial_multi_evidence_retrieval_surfaces_ranking_failure(self):
        result = ExperimentResult(
            run=self.run,
            retrieval=RetrievalEvaluation(
                "cq-001",
                RetrievalMetrics(0.5, 0.5, 1.0, 0.6, 5, 1, 2),
                ["chunk-1"], ["chunk-1", "chunk-2"],
            ),
        )
        failures = classify_failures(self.question, result)
        self.assertIn(
            ("RETRIEVAL", "Ranking failure"),
            {(f.category, f.type) for f in failures},
        )

    def test_clean_result_produces_no_failures(self):
        result = ExperimentResult(run=self.run)
        self.assertEqual(classify_failures(self.question, result), ())
