from sqlalchemy import select
from sqlalchemy.orm import Session

from app.backend.db_models import FailureRow
from src.failure_analysis.models import Failure, FailureSeverity


class FailureRepository:
    """SQLAlchemy adapter for Failure domain persistence."""

    def __init__(self, session: Session):
        self.session = session

    def save(self, failure: Failure) -> None:
        existing = self.session.get(FailureRow, failure.failure_id)
        if existing is not None:
            if self._to_domain(existing) != failure:
                raise ValueError(
                    f"failure_id already exists with different content: {failure.failure_id}"
                )
            return
        self.session.add(self._to_row(failure))
        self.session.commit()

    def save_many(self, failures: list[Failure] | tuple[Failure, ...]) -> None:
        for failure in failures:
            existing = self.session.get(FailureRow, failure.failure_id)
            if existing is not None and self._to_domain(existing) != failure:
                raise ValueError(
                    f"failure_id already exists with different content: {failure.failure_id}"
                )
            if existing is None:
                self.session.add(self._to_row(failure))
        self.session.commit()

    def get(self, failure_id: str) -> Failure | None:
        row = self.session.get(FailureRow, failure_id)
        return self._to_domain(row) if row else None

    def list(self) -> list[Failure]:
        rows = self.session.scalars(select(FailureRow).order_by(FailureRow.failure_id)).all()
        return [self._to_domain(row) for row in rows]

    def count(self) -> int:
        return len(self.list())

    @staticmethod
    def _to_row(failure: Failure) -> FailureRow:
        return FailureRow(
            failure_id=failure.failure_id,
            run_id=failure.run_id,
            question_id=failure.question_id,
            answer_id=failure.answer_id,
            category=failure.category,
            type=failure.type,
            severity=failure.severity.value,
            description=failure.description,
            evidence=failure.evidence,
            metric=failure.metric,
            metric_value=failure.metric_value,
            classifier_version=failure.classifier_version,
            created_at=failure.created_at,
        )

    @staticmethod
    def _to_domain(row: FailureRow) -> Failure:
        return Failure(
            failure_id=row.failure_id,
            run_id=row.run_id,
            question_id=row.question_id,
            category=row.category,
            type=row.type,
            severity=FailureSeverity(row.severity),
            description=row.description,
            evidence=row.evidence,
            answer_id=row.answer_id,
            metric=row.metric,
            metric_value=row.metric_value,
            classifier_version=row.classifier_version,
            created_at=row.created_at,
        )
