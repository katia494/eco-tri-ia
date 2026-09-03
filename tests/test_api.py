import io
from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient
from PIL import Image

from backend.api.config import settings
from backend.api.main import app


client = TestClient(app)


@pytest.fixture
def model_api_key(monkeypatch):
    """Clé isolée pour tester la protection de /predict."""
    key = "test-c9-api-key"
    monkeypatch.setattr(settings, "data_api_key", key)
    return key


def make_test_image() -> io.BytesIO:
    """Crée une image JPEG valide en mémoire."""
    image = Image.new("RGB", (100, 100), color=(255, 0, 0))
    image_bytes = io.BytesIO()
    image.save(image_bytes, format="JPEG")
    image_bytes.seek(0)
    return image_bytes


def test_health_check():
    response = client.get("/health")

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert "message" in data
    assert "version" in data


def test_root():
    response = client.get("/")

    assert response.status_code == 200
    assert "message" in response.json()


def test_predict_rejects_request_without_api_key(model_api_key):
    response = client.post(
        "/predict",
        files={"file": ("test.jpg", make_test_image(), "image/jpeg")},
    )

    assert response.status_code == 401


def test_predict_no_file(model_api_key):
    response = client.post(
        "/predict",
        headers={"x-api-key": model_api_key},
    )

    assert response.status_code == 422


def test_predict_with_image(model_api_key):
    with patch("backend.api.routes.predict_waste") as mock_predict:
        mock_predict.return_value = {
            "waste_class": "plastic",
            "confidence": 0.92,
            "model": "yolov8n-cls-v3",
            "image_name": "test.jpg",
            "message": "Déchet classifié : plastic",
            "sorting_instruction": "Déposez-le dans le bac de tri.",
            "is_uncertain": False,
        }

        response = client.post(
            "/predict",
            files={"file": ("test.jpg", make_test_image(), "image/jpeg")},
            headers={"x-api-key": model_api_key},
        )

    assert response.status_code == 200
    data = response.json()
    assert data["waste_class"] == "plastic"
    assert data["confidence"] == 0.92


def test_predict_rejects_text_file(model_api_key):
    response = client.post(
        "/predict",
        files={"file": ("notes.txt", b"pas une image", "text/plain")},
        headers={"x-api-key": model_api_key},
    )

    assert response.status_code == 400


def test_model_info():
    response = client.get("/model/info")

    assert response.status_code == 200
    data = response.json()
    assert data["task"] == "image-classification"
    assert len(data["classes"]) == 6


def test_get_predictions():
    response = client.get("/predictions")

    assert response.status_code == 200
    assert isinstance(response.json(), list)