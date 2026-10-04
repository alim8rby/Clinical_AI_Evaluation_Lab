from datetime import datetime
from src.experiments.models import Experiment, ExperimentConfig, RunRecord

def test_experiment_identity_is_stable():
    config=ExperimentConfig({"provider":"mock"},{"provider":"hashed"},{"type":"dense"},5,"v1","ClinicalQA-v1")
    first=Experiment.create("runtime-test","runtime",config,created_at=datetime(2026,10,4))
    second=Experiment.create("runtime-test","runtime",config,created_at=datetime(2027,1,1))
    assert first.experiment_id==second.experiment_id

def test_run_record_carries_experiment_identity():
    run=RunRecord("run-1","exp-1","cq-001","completed",datetime(2026,10,4),datetime(2026,10,4),10.0,None,None,None,None)
    assert run.experiment_id=="exp-1"
