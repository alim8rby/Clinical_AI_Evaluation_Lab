from app.backend.observability import JsonFormatter, Timer, get_correlation_id, set_correlation_id
from app.backend.schemas import MetricsResponse

def test_correlation_id_roundtrip():
    value=set_correlation_id("corr-test")
    assert value=="corr-test"
    assert get_correlation_id()=="corr-test"

def test_timer_returns_nonnegative_duration():
    assert Timer.start().elapsed_ms() >= 0

def test_metrics_contract():
    metrics=MetricsResponse(
        runs_total=2,
        runs_completed=1,
        runs_failed=1,
        failures_total=1,
        average_latency_ms=10.0,
        input_tokens_total=20,
        output_tokens_total=10,
        cost_total=0.0,
    )
    assert metrics.runs_total==2

def test_json_formatter_includes_correlation_id():
    import logging
    record=logging.LogRecord("test",logging.INFO,"",1,"message",(),None)
    set_correlation_id("corr-json")
    payload=JsonFormatter().format(record)
    assert '"correlation_id": "corr-json"' in payload
