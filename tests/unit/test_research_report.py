import unittest
from datetime import datetime

from src.experiments.models import Experiment, ExperimentConfig
from src.experiments.research_report import render_research_report


class ResearchReportTests(unittest.TestCase):
    def setUp(self):
        config = ExperimentConfig(
            {"provider": "ollama", "model": "model-a"},
            {"provider": "local", "model": "embed-a"},
            {"type": "hybrid", "version": "retriever-a"},
            5,
            "prompt-v1",
            "ClinicalQA-v2",
            model_version="model-a",
            embedding_version="embed-a",
            retriever_version="retriever-a",
            evaluator_versions={"answer": "answer-v1", "retrieval": "retrieval-v1"},
            runtime_version="caiel-runtime-v1",
        )
        self.experiment = Experiment.create(
            "Demo experiment",
            "A deterministic report test.",
            config,
            created_at=datetime(2026, 1, 1),
        )

    def test_report_is_deterministic(self):
        kwargs = {
            "experiment": self.experiment,
            "sample_count": 3,
            "metrics": {"correctness": 0.75, "faithfulness": 0.9},
            "failures": [
                {"category": "GENERATION"},
                {"category": "RETRIEVAL"},
                {"category": "GENERATION"},
            ],
        }
        self.assertEqual(render_research_report(**kwargs), render_research_report(**kwargs))

    def test_report_contains_provenance_results_and_limitations(self):
        report = render_research_report(
            experiment=self.experiment,
            sample_count=3,
            metrics={"correctness": 0.75},
            failures=[{"category": "GENERATION"}],
        )
        for expected in (
            "Reproducibility configuration",
            "model-a",
            "ClinicalQA-v2",
            "0.750000",
            "Failure signals",
            "Methodology",
            "Limitations",
            "bit-for-bit",
        ):
            self.assertIn(expected, report)


if __name__ == "__main__":
    unittest.main()
