from app.backend.schemas import EvidenceResponse, ReportResponse, RunEvidenceResponse

def test_evidence_score_is_optional_until_persisted():
    response=EvidenceResponse(chunk_id="c1",document_id="d1",score=None,rank=1,text="text")
    assert response.score is None

def test_report_contract():
    report=ReportResponse(
        experiment_id="exp_1",
        benchmark_version="ClinicalQA-v1",
        sample_count=1,
        configuration={"top_k":5},
        metrics={"recall_at_k":1.0},
        failures=[],
    )
    assert report.sample_count==1

def test_run_evidence_contract():
    response=RunEvidenceResponse(run_id="run_1",answer_id="answer_1",evidence=[])
    assert response.run_id=="run_1"
