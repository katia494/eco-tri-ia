from unittest.mock import patch

from fastapi.testclient import TestClient

from backend.api.main import app
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


def test_monitoring_endpoint_returns_latency_alert():
    fake_snapshot = {
        "scope": "current_process",
        "request_count": 1,
        "error_count": 0,
        "error_rate": 0.0,
        "average_latency_ms": 2500.0,
        "max_latency_ms": 2500.0,
        "status_counts": {"200": 1},
        "endpoint_counts": {"GET /health": 1},
    }

    with patch(
        "backend.api.routes_stats.monitoring_registry.snapshot",
        return_value=fake_snapshot,
    ):
        response = TestClient(app).get("/stats/monitoring")

    assert response.status_code == 200
    data = response.json()
    assert data["monitoring_status"] == "alert"
    assert any(
        alert["metric"] == "average_latency_ms"
        for alert in data["alerts"]
    )