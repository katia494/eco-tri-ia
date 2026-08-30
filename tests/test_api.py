from fastapi.testclient import TestClient
from unittest.mock import patch
from backend.api.main import app

client = TestClient(app)

def test_health_check():
    """Teste que l'API répond correctement sur /health."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert "message" in data
    assert "version" in data

def test_root():
    """Teste la route racine."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data

def test_predict_no_file():
    """Teste que /predict renvoie une erreur sans fichier."""
    response = client.post("/predict")
    assert response.status_code == 422

def test_predict_with_image():
    """Teste la classification d'une image."""
    import io
    from PIL import Image

    # Crée une image de test en mémoire
    img = Image.new("RGB", (100, 100), color=(255, 0, 0))
    img_bytes = io.BytesIO()
    img.save(img_bytes, format="JPEG")
    img_bytes.seek(0)

    with patch("backend.api.routes.predict_waste") as mock_predict:
        mock_predict.return_value = {
            "waste_class": "plastic",
            "confidence": 0.92,
            "model": "yolov8n-cls-v1",
            "image_name": "test.jpg",
            "message": "Déchet classifié : plastic",
            "sorting_instruction": "Déposez-le dans le bac de tri.",
            "is_uncertain": False,
        }
        response = client.post(
            "/predict",
            files={"file": ("test.jpg", img_bytes, "image/jpeg")}
        )

    assert response.status_code == 200
    data = response.json()
    assert data["waste_class"] == "plastic"
    assert data["confidence"] == 0.92

def test_predict_rejects_text_file():
    response = client.post(
        "/predict",
        files={"file": ("notes.txt", b"pas une image", "text/plain")},
    )
    assert response.status_code == 400

def test_model_info():
    response = client.get("/model/info")
    assert response.status_code == 200
    data = response.json()
    assert data["task"] == "image-classification"
    assert len(data["classes"]) == 6

def test_get_predictions():
    """Teste la récupération de l'historique."""
    response = client.get("/predictions")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
