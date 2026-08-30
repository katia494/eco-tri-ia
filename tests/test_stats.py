import pytest
from fastapi.testclient import TestClient
from backend.api.main import app

client = TestClient(app)

def test_get_stats_empty():
    """Teste les stats quand il n'y a pas de prédictions."""
    response = client.get("/stats/")
    assert response.status_code == 200
    data = response.json()
    assert "total_predictions" in data
    assert "average_confidence" in data
    assert "most_common_class" in data
    assert data["total_predictions"] == 0

def test_get_stats_by_class_empty():
    """Teste les stats par classe quand il n'y a pas de prédictions."""
    response = client.get("/stats/by-class")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

def test_stats_after_prediction():
    """Teste les stats après une prédiction."""
    import io
    from PIL import Image
    from unittest.mock import patch

    img = Image.new("RGB", (100, 100), color=(0, 0, 255))
    img_bytes = io.BytesIO()
    img.save(img_bytes, format="JPEG")
    img_bytes.seek(0)

    with patch("backend.api.routes.predict_waste") as mock_predict:
        mock_predict.return_value = {
            "waste_class": "glass",
            "confidence": 0.88,
            "model": "yolov8n-cls-v2",
            "image_name": "test.jpg",
            "message": "Déchet classifié : glass",
            "sorting_instruction": "Conteneur à verre.",
            "is_uncertain": False,
        }
        client.post(
            "/predict",
            files={"file": ("test.jpg", img_bytes, "image/jpeg")}
        )

    response = client.get("/stats/")
    assert response.status_code == 200
    data = response.json()
    assert data["total_predictions"] >= 0


def test_get_monitoring_metrics():
    """Vérifie le contrat des métriques de monitoring."""
    response = client.get("/stats/monitoring")

    assert response.status_code == 200
    data = response.json()
    assert data["application"]["request_count"] >= 0
    assert data["model"]["confidence_threshold"] == 0.60
    assert data["model"]["uncertain_prediction_rate"] == 0.0
    assert data["alert_thresholds"]["latency_ms"] == 2000
