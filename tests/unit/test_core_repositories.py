import unittest
from datetime import datetime, date
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.backend.database import Base
from app.backend.repositories import DocumentRepository, ChunkRepository, ExperimentRepository, RunRepository
from src.ingestion.models import SourceDocument
from src.preprocessing.models import Chunk
from src.experiments.models import Experiment, ExperimentConfig, RunRecord


class CoreRepositoryTests(unittest.TestCase):
    def setUp(self):
        self.engine = create_engine("sqlite:///:memory:")
        Base.metadata.create_all(self.engine)
        self.session = sessionmaker(bind=self.engine)()

    def tearDown(self):
        self.session.close()
        self.engine.dispose()

    def test_document_and_chunks_roundtrip(self):
        document = SourceDocument("doc-1", "Depression", "WHO", "WHO", date(2026, 1, 1), "https://example.com/depression", "content")
        DocumentRepository(self.session).save(document)
        self.assertEqual(DocumentRepository(self.session).get("doc-1"), document)
        chunks = [Chunk("c-2", "doc-1", "second", None, None, 1), Chunk("c-1", "doc-1", "first", None, None, 0)]
        ChunkRepository(self.session).save_many(chunks)
        self.assertEqual([c.chunk_id for c in ChunkRepository(self.session).list_by_document("doc-1")], ["c-1", "c-2"])

    def test_experiment_and_run_roundtrip(self):
        config = ExperimentConfig({"model":"mock"}, {"embedding":"local"}, {"method":"dense"}, 5, "v1", "ClinicalQA-v1")
        experiment = Experiment.create("baseline", "baseline experiment", config, created_at=datetime(2026, 10, 4, 12))
        ExperimentRepository(self.session).save(experiment)
        self.assertEqual(ExperimentRepository(self.session).get(experiment.experiment_id), experiment)
        run = RunRecord("run-1", experiment.experiment_id, "cq-1", "completed", datetime(2026,10,4,12), None, 10.0, 2, 3, 0.0, None)
        RunRepository(self.session).save(run)
        self.assertEqual(RunRepository(self.session).get("run-1"), run)


if __name__ == "__main__":
    unittest.main()
