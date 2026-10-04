"""Application runtime for evaluated clinical QA runs."""
from dataclasses import dataclass
from datetime import datetime, timezone
from time import perf_counter
import hashlib
import json

from src.evaluation.answer import evaluate_question_answer
from src.evaluation.grounding import evaluate_answer_grounding
from src.evaluation.reliability import evaluate_answer_reliability
from src.evaluation.retrieval import evaluate_question_retrieval
from src.evaluation.benchmark import BenchmarkQuestion
from src.experiments.models import Experiment, ExperimentResult, RunRecord
from src.failure_analysis.workflow import process_result
from src.pipeline import ClinicalRAG

from app.backend.repositories import AnswerRepository, CitationRepository, EvaluationRepository, ExperimentRepository, FailureRepository, RunRepository


@dataclass(frozen=True)
class RuntimeResult:
    experiment: Experiment
    result: ExperimentResult


class EvaluationRuntime:
    """Orchestrates frozen domain modules and V4 persistence adapters."""

    def __init__(self, session, rag: ClinicalRAG):
        self.rag = rag
        self.experiments = ExperimentRepository(session)
        self.runs = RunRepository(session)
        self.answers = AnswerRepository(session)
        self.citations = CitationRepository(session)
        self.evaluations = EvaluationRepository(session)
        self.failures = FailureRepository(session)

    def create_experiment(self, experiment: Experiment) -> Experiment:
        self.experiments.save(experiment)
        return experiment

    def run_question(self, experiment: Experiment, question: BenchmarkQuestion) -> RuntimeResult:
        started = datetime.now(timezone.utc).replace(tzinfo=None)
        run_id = self._run_id(experiment.experiment_id, question.question_id)
        answer_id = f"answer_{run_id}"
        start_clock = perf_counter()
        running = RunRecord(run_id, experiment.experiment_id, question.question_id, "running", started, None, None, None, None, None, None)
        self.runs.save(running)
        try:
            rag_result = self.rag.ask(question.question, top_k=experiment.config.top_k, answer_id=answer_id, prompt_version=experiment.config.prompt_version)
            retrieval = evaluate_question_retrieval(question, rag_result.evidence, k=experiment.config.top_k)
            answer_eval = evaluate_question_answer(question, rag_result.answer)
            grounding = evaluate_answer_grounding(answer_id, rag_result.answer, rag_result.citations, rag_result.evidence)
            reliability = evaluate_answer_reliability(answer_id, rag_result.answer, grounding.metrics)
            finished = datetime.now(timezone.utc).replace(tzinfo=None)
            run = RunRecord(run_id, experiment.experiment_id, question.question_id, "completed", started, finished, (perf_counter() - start_clock) * 1000, None, None, None, None)
            result = ExperimentResult(run=run, retrieval=retrieval, answer=answer_eval, grounding=grounding, reliability=reliability)
            workflow = process_result(question, result, self.failures, created_at=finished)
            result = workflow.result
            self.runs.save(result.run)
            self.answers.save(answer_id, run_id, rag_result.answer)
            self.citations.save_many(rag_result.citations)
            self._save_evaluations(answer_id, retrieval, answer_eval, grounding, reliability)
            return RuntimeResult(experiment, result)
        except Exception as exc:
            failed = RunRecord(run_id, experiment.experiment_id, question.question_id, "failed", started, datetime.now(timezone.utc).replace(tzinfo=None), (perf_counter() - start_clock) * 1000, None, None, None, str(exc))
            self.runs.save(failed)
            raise

    def _save_evaluations(self, answer_id, retrieval, answer, grounding, reliability):
        for name, evaluation in (("retrieval", retrieval), ("answer", answer), ("grounding", grounding), ("reliability", reliability)):
            metrics = evaluation.metrics
            scores = {key: value for key, value in vars(metrics).items() if isinstance(value, (int, float))}
            details = {"question_id": getattr(evaluation, "question_id", None), "answer_id": getattr(evaluation, "answer_id", None)}
            evaluator_version = getattr(evaluation, "evaluator_version", f"{name}-v1")
            raw_id = f"{answer_id}:{name}:{evaluator_version}"
            evaluation_id = "eval_" + hashlib.sha256(raw_id.encode()).hexdigest()[:24]
            self.evaluations.save(evaluation_id, answer_id, evaluator_version, scores, details)

    @staticmethod
    def _run_id(experiment_id: str, question_id: str) -> str:
        raw = json.dumps({"experiment_id": experiment_id, "question_id": question_id}, sort_keys=True)
        return "run_" + hashlib.sha256(raw.encode()).hexdigest()[:24]
