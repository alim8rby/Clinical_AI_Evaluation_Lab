"""Local Ollama model-assisted evaluator."""
from __future__ import annotations

import json
import os
import httpx


class OllamaSemanticEvaluator:
    evaluator_version = "ollama-semantic-v1"

    def __init__(
        self,
        model: str | None = None,
        base_url: str | None = None,
        timeout: float | None = None,
    ):
        self.model = model or os.getenv("OLLAMA_GENERATION_MODEL", "llama3.2:3b")
        self.base_url = (
            base_url or os.getenv("OLLAMA_BASE_URL", "http://127.0.0.1:11434")
        ).rstrip("/")
        self.timeout = timeout or float(os.getenv("OLLAMA_TIMEOUT_SECONDS", "60"))

    def _generate_json(self, prompt: str) -> dict:
        try:
            response = httpx.post(
                f"{self.base_url}/api/generate",
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": False,
                    "format": "json",
                },
                timeout=self.timeout,
            )
            response.raise_for_status()
            payload = response.json()
            result = json.loads(payload["response"])
        except (httpx.HTTPError, httpx.TimeoutException, KeyError, TypeError, ValueError, json.JSONDecodeError) as exc:
            raise RuntimeError("Ollama semantic evaluation failed") from exc
        if not isinstance(result, dict):
            raise RuntimeError("Ollama semantic evaluation returned invalid JSON")
        return result

    @staticmethod
    def _score(value: object, name: str) -> float:
        try:
            score = float(value)
        except (TypeError, ValueError) as exc:
            raise RuntimeError(f"invalid semantic score: {name}") from exc
        if not 0.0 <= score <= 1.0:
            raise RuntimeError(f"semantic score out of range: {name}")
        return score

    def evaluate_answer(self, *, question, reference_answer, key_concepts, answer_text):
        result = self._generate_json(
            "You are evaluating a clinical QA benchmark answer. "
            "Do not add facts. Score only the supplied material. "
            "Return JSON with exactly correctness, completeness, relevance, each from 0 to 1.\n"
            f"Question: {question}\nReference answer: {reference_answer}\n"
            f"Key concepts: {json.dumps(key_concepts)}\nAnswer: {answer_text}"
        )
        return {name: self._score(result[name], name) for name in ("correctness", "completeness", "relevance")}

    def evaluate_grounding(self, *, question, answer_text, claims, evidence):
        result = self._generate_json(
            "You are evaluating grounding of a clinical QA answer. "
            "Judge whether each claim is supported by the supplied evidence only. "
            "Return JSON with exactly faithfulness and unsupported_claim_rate, each from 0 to 1. "
            "Do not judge whether the medical advice is independently correct.\n"
            f"Question: {question}\nAnswer: {answer_text}\nClaims: {json.dumps(claims)}\n"
            f"Evidence: {json.dumps(evidence)}"
        )
        faithfulness = self._score(result["faithfulness"], "faithfulness")
        unsupported = self._score(result["unsupported_claim_rate"], "unsupported_claim_rate")
        return {"faithfulness": faithfulness, "unsupported_claim_rate": unsupported}
