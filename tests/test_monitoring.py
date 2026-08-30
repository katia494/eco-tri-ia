from backend.api.monitoring import MonitoringRegistry


def test_monitoring_registry_aggregates_requests():
    registry = MonitoringRegistry()
    registry.record("GET", "/health", 200, 10.0)
    registry.record("POST", "/predict", 422, 30.0)

    snapshot = registry.snapshot()

    assert snapshot["request_count"] == 2
    assert snapshot["error_count"] == 1
    assert snapshot["error_rate"] == 0.5
    assert snapshot["average_latency_ms"] == 20.0
    assert snapshot["max_latency_ms"] == 30.0
    assert snapshot["status_counts"] == {"200": 1, "422": 1}
