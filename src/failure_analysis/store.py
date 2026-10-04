from __future__ import annotations
"""Local structured persistence for failure records."""

from pathlib import Path
import json
import os
from tempfile import NamedTemporaryFile

from .models import Failure, failure_from_dict


class FailureStoreError(Exception):
    """Base error for failure-store operations."""


class FailureAlreadyExistsError(FailureStoreError):
    """Raised when an ID exists with different content."""


class FailureStore:
    """Deterministic JSON-backed store for structured failure records."""

    def __init__(self, path: str | Path) -> None:
        self.path = Path(path)

    def save(self, failure: Failure) -> None:
        """Persist a failure, rejecting conflicting reuse of its ID."""
        records = self._read_records()
        existing = next(
            (record for record in records if record.failure_id == failure.failure_id),
            None,
        )
        if existing is not None:
            if existing != failure:
                raise FailureAlreadyExistsError(
                    f"failure_id already exists with different content: {failure.failure_id}"
                )
            return

        records.append(failure)
        self._write_records(records)

    def save_many(self, failures: list[Failure] | tuple[Failure, ...]) -> None:
        """Persist multiple failures while enforcing stable IDs."""
        records = self._read_records()
        by_id = {record.failure_id: record for record in records}

        for failure in failures:
            existing = by_id.get(failure.failure_id)
            if existing is not None and existing != failure:
                raise FailureAlreadyExistsError(
                    f"failure_id already exists with different content: {failure.failure_id}"
                )
            by_id[failure.failure_id] = failure

        self._write_records(sorted(by_id.values(), key=lambda item: item.failure_id))

    def get(self, failure_id: str) -> Failure | None:
        """Return a failure by ID, or None when it does not exist."""
        if not isinstance(failure_id, str) or not failure_id.strip():
            raise ValueError("failure_id must not be empty")
        return next(
            (failure for failure in self._read_records() if failure.failure_id == failure_id),
            None,
        )

    def list(self) -> list[Failure]:
        """Return all failures in deterministic ID order."""
        return self._read_records()

    def count(self) -> int:
        """Return the number of persisted failures."""
        return len(self._read_records())

    def _read_records(self) -> list[Failure]:
        if not self.path.exists():
            return []
        if not self.path.is_file():
            raise FailureStoreError(f"store path is not a file: {self.path}")

        try:
            payload = json.loads(self.path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            raise FailureStoreError(f"invalid failure store JSON: {self.path}") from exc

        if not isinstance(payload, list):
            raise FailureStoreError("failure store root must be a JSON list")

        try:
            records = [failure_from_dict(item) for item in payload]
        except (TypeError, KeyError, ValueError) as exc:
            raise FailureStoreError("invalid failure record in store") from exc

        return sorted(records, key=lambda item: item.failure_id)

    def _write_records(self, records: list[Failure]) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        payload = [failure.to_dict() for failure in sorted(records, key=lambda item: item.failure_id)]
        serialized = json.dumps(payload, indent=2, sort_keys=True) + "\n"

        with NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            dir=self.path.parent,
            prefix=f".{self.path.name}.",
            suffix=".tmp",
            delete=False,
        ) as temp:
            temp.write(serialized)
            temp_path = Path(temp.name)

        os.replace(temp_path, self.path)
