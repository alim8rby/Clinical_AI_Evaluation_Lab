from __future__ import annotations
import json
import httpx

from src.retrieval.search import EvidenceSet
from .models import Answer, Claim
from .prompt import build_prompt


class OllamaGenerationProvider:
    """Local Ollama generation provider with provider-neutral Answer output."""

    def __init__(self, model: str = "llama3.2:3b", base_url: str = "http://127.0.0.1:11434", timeout: float = 60.0):
        self.model = model
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.last_usage = {"input_tokens": None, "output_tokens": None, "cost": None}

    def generate(self, question: str, evidence: EvidenceSet, *, prompt_version: str) -> Answer:
        if not question.strip():
            raise ValueError("question must not be empty")
        if not evidence.evidence:
            raise ValueError("evidence must not be empty")

        evidence_text = "\n".join(
            f"[{i}] {item.chunk.text}" for i, item in enumerate(evidence.evidence, start=1)
        )
        prompt = build_prompt(question, evidence_text)
        schema = {
            "answer_text": "string",
            "uncertainty": "string or null",
            "claims": [{"text": "string", "citation_indices": [1]}],
        }
        self.last_usage = {"input_tokens": None, "output_tokens": None, "cost": None}
        try:
            response = httpx.post(
                f"{self.base_url}/api/generate",
                json={
                    "model": self.model,
                    "prompt": prompt + "\n\nReturn JSON matching this shape:\n" + json.dumps(schema),
                    "stream": False,
                    "format": "json",
                },
                timeout=self.timeout,
            )
            response.raise_for_status()
            payload = response.json()
            generated = json.loads(payload["response"])
            self.last_usage = {
                "input_tokens": payload.get("prompt_eval_count"),
                "output_tokens": payload.get("eval_count"),
                "cost": None,
            }
        except (httpx.HTTPError, httpx.TimeoutException, KeyError, TypeError, ValueError, json.JSONDecodeError) as exc:
            raise RuntimeError("Ollama generation failed") from exc

        claims = [
            Claim(text=str(item["text"]), citation_indices=[int(i) for i in item["citation_indices"]])
            for item in generated.get("claims", [])
        ]
        if not generated.get("answer_text"):
            raise RuntimeError("Ollama returned an empty answer")
        return Answer(
            answer_text=str(generated["answer_text"]),
            claims=claims,
            uncertainty=generated.get("uncertainty"),
            model=self.model,
            prompt_version=prompt_version,
        )
