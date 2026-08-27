import pytest
import io
from PIL import Image
from unittest.mock import patch
from backend.api.predict import predict_waste, WASTE_CLASSES

def create_test_image():
    """Crée une image de test en mémoire."""
    img = Image.new("RGB", (100, 100), color=(0, 255, 0))
    img_bytes = io.BytesIO()
    img.save(img_bytes, format="JPEG")
    return img_bytes.getvalue()

def test_waste_classes_defined():
    """Vérifie que les classes de déchets sont définies."""
    assert len(WASTE_CLASSES) > 0
    assert 0 in WASTE_CLASSES
    assert isinstance(WASTE_CLASSES[0], str)

def test_predict_simulation_mode():
    """Teste la prédiction en mode simulation (sans modèle)."""
    with patch("backend.api.predict.load_model", return_value=None):
        image_bytes = create_test_image()
        result = predict_waste(image_bytes, "test.jpg")

        assert "waste_class" in result
        assert "confidence" in result
        assert "image_name" in result
        assert "message" in result
        assert result["image_name"] == "test.jpg"
        assert 0.0 <= result["confidence"] <= 1.0
        assert result["waste_class"] in WASTE_CLASSES.values()

def test_predict_returns_valid_confidence():
    """Vérifie que la confiance est entre 0 et 1."""
    with patch("backend.api.predict.load_model", return_value=None):
        image_bytes = create_test_image()
        result = predict_waste(image_bytes, "image.jpg")
        assert 0.0 <= result["confidence"] <= 1.0

def test_predict_returns_valid_class():
    """Vérifie que la classe retournée est valide."""
    with patch("backend.api.predict.load_model", return_value=None):
        image_bytes = create_test_image()
        result = predict_waste(image_bytes, "image.jpg")
        assert result["waste_class"] in WASTE_CLASSES.values()