"""Domain models for failure analysis."""

from dataclasses import dataclass
from datetime import datetime
from enum import Enum
import json


class FailureSeverity(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


@dataclass(frozen=True)
class Failure:
    failure_id: str
    run_id: str
    question_id: str
    category: str
    type: str
    severity: FailureSeverity
    description: str
    evidence: str
    answer_id: str | None = None
    metric: str | None = None
    metric_value: float | None = None
    classifier_version: str = "failure-v1"
    created_at: datetime | None = None

    def __post_init__(self) -> None:
        required = {
            "failure_id": self.failure_id,
            "run_id": self.run_id,
            "question_id": self.question_id,
            "category": self.category,
            "type": self.type,
            "description": self.description,
            "evidence": self.evidence,
            "classifier_version": self.classifier_version,
        }
        for name, value in required.items():
            if not isinstance(value, str) or not value.strip():
                raise ValueError(f"{name} must not be empty")
        if not isinstance(self.severity, FailureSeverity):
            raise ValueError("severity must be a FailureSeverity")
        if self.metric_value is not None and not isinstance(self.metric_value, (int, float)):
            raise ValueError("metric_value must be numeric")

    def to_dict(self) -> dict:
        return {
            "failure_id": self.failure_id,
            "run_id": self.run_id,
            "question_id": self.question_id,
            "answer_id": self.answer_id,
            "category": self.category,
            "type": self.type,
            "severity": self.severity.value,
            "description": self.description,
            "evidence": self.evidence,
            "metric": self.metric,
            "metric_value": self.metric_value,
            "classifier_version": self.classifier_version,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), sort_keys=True)


def failure_from_dict(data: dict) -> Failure:
    required = {
        "failure_id", "run_id", "question_id", "category", "type",
        "severity", "description", "evidence", "classifier_version",
    }
    missing = required - data.keys()
    if missing:
        raise ValueError(f"missing failure fields: {sorted(missing)}")
    created_at = data.get("created_at")
    return Failure(
        failure_id=data["failure_id"],
        run_id=data["run_id"],
        question_id=data["question_id"],
        answer_id=data.get("answer_id"),
        category=data["category"],
        type=data["type"],
        severity=FailureSeverity(data["severity"]),
        description=data["description"],
        evidence=data["evidence"],
        metric=data.get("metric"),
        metric_value=data.get("metric_value"),
        classifier_version=data["classifier_version"],
        created_at=datetime.fromisoformat(created_at) if created_at else None,
    )
