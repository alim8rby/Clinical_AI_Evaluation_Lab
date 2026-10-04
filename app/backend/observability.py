"""Structured application observability."""
from __future__ import annotations
import json
import logging
import time
import uuid
from contextvars import ContextVar
from dataclasses import dataclass

_correlation_id: ContextVar[str] = ContextVar("correlation_id", default="-")


def set_correlation_id(value: str | None = None) -> str:
    correlation_id = value or uuid.uuid4().hex
    _correlation_id.set(correlation_id)
    return correlation_id


def get_correlation_id() -> str:
    return _correlation_id.get()


class JsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        payload = {
            "timestamp": self.formatTime(record, "%Y-%m-%dT%H:%M:%S%z"),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "correlation_id": get_correlation_id(),
        }
        for key in ("request_id", "run_id", "experiment_id", "question_id", "latency_ms", "input_tokens", "output_tokens", "cost", "status_code"):
            value = getattr(record, key, None)
            if value is not None:
                payload[key] = value
        return json.dumps(payload, sort_keys=True)


def configure_logging(level: str = "INFO") -> None:
    handler = logging.StreamHandler()
    handler.setFormatter(JsonFormatter())
    root = logging.getLogger()
    root.handlers.clear()
    root.addHandler(handler)
    root.setLevel(getattr(logging, level.upper(), logging.INFO))


@dataclass(frozen=True)
class Timer:
    started: float

    @classmethod
    def start(cls) -> "Timer":
        return cls(time.perf_counter())

    def elapsed_ms(self) -> float:
        return round((time.perf_counter() - self.started) * 1000, 3)


logger = logging.getLogger("caiel")
