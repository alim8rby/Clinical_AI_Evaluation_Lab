from datetime import datetime, timezone

from src.evaluation.benchmark import BenchmarkQuestion
from src.experiments.models import Experiment, ExperimentConfig


def test_runtime_run_id_is_deterministic():
    from app.backend.runtime import EvaluationRuntime
    assert EvaluationRuntime._run_id("exp-1", "cq-001") == EvaluationRuntime._run_id("exp-1", "cq-001")


def test_benchmark_question_is_constructible():
    question = BenchmarkQuestion("cq-001", "What is depression?", "depression", "easy", ("chunk-1",), "reference", ("depression",))
    assert question.question_id == "cq-001"


def test_runtime_can_build_frozen_experiment():
    config = ExperimentConfig({"provider": "mock"}, {"provider": "hashed"}, {"type": "dense"}, 5, "v1", "ClinicalQA-v1")
    experiment = Experiment.create("runtime-test", "runtime", config, created_at=datetime.now(timezone.utc).replace(tzinfo=None))
    assert experiment.experiment_id.startswith("exp_")
