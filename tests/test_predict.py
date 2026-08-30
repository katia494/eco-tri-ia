# tests/test_predict.py
# Tests du module de prédiction ECO-TRI
# Compétence C13 — Tests automatisés

import io
from unittest.mock import patch

import pytest
from PIL import Image

from backend.api.exceptions import InvalidImageError
from backend.api.predict import predict_waste, CATEGORIES, WASTE_CLASSES


def create_image_bytes() -> bytes:
    image = Image.new("RGB", (64, 64), color=(100, 150, 200))
    buffer = io.BytesIO()
    image.save(buffer, format="JPEG")
    return buffer.getvalue()

# ─── Test 1 — Les catégories sont bien définies ────────────────────
def test_waste_classes_defined():
    """Vérifie que les classes de déchets sont définies."""
    assert len(WASTE_CLASSES) == 6
    assert "cardboard" in WASTE_CLASSES
    assert "plastic" in WASTE_CLASSES
    assert "glass" in WASTE_CLASSES
    assert "metal" in WASTE_CLASSES
    assert "paper" in WASTE_CLASSES
    assert "trash" in WASTE_CLASSES
    print(f"✅ 6 catégories définies : {WASTE_CLASSES}")

# ─── Test 2 — La prédiction retourne un dict valide ───────────────
def test_predict_returns_dict():
    """Vérifie que predict_waste retourne un dictionnaire."""
    with patch("backend.api.predict.service.predict", return_value=("plastic", 0.91)):
        result = predict_waste(create_image_bytes(), "test.jpg")

    assert isinstance(result, dict), "❌ Le résultat doit être un dictionnaire !"
    print(f"✅ Résultat : {result}")

# ─── Test 3 — La confiance est entre 0 et 1 ───────────────────────
def test_predict_returns_valid_confidence():
    """Vérifie que la confiance est entre 0 et 1."""
    with patch("backend.api.predict.service.predict", return_value=("metal", 0.73)):
        result = predict_waste(create_image_bytes(), "test.jpg")

    assert "confidence" in result, "❌ Clé confidence manquante !"
    assert 0.0 <= result["confidence"] <= 1.0, f"❌ Confiance hors limites : {result['confidence']}"
    print(f"✅ Confiance valide : {result['confidence']}")

def test_low_confidence_prediction_is_marked_uncertain():
    """Une confiance sous le seuil ne doit pas produire une consigne catégorique."""
    with patch("backend.api.predict.service.predict", return_value=("paper", 0.52)):
        result = predict_waste(create_image_bytes(), "metal-externe.jpg")

    assert result["is_uncertain"] is True
    assert "Résultat incertain" in result["sorting_instruction"]

# ─── Test 4 — La classe retournée est valide ──────────────────────
def test_predict_returns_valid_class():
    """Vérifie que la classe retournée est dans CATEGORIES."""
    with patch("backend.api.predict.service.predict", return_value=("glass", 0.82)):
        result = predict_waste(create_image_bytes(), "test.jpg")

    assert "waste_class" in result, "❌ Clé waste_class manquante !"
    assert result["waste_class"] in CATEGORIES, f"❌ Classe inconnue : {result['waste_class']}"
    print(f"✅ Classe valide : {result['waste_class']}")

def test_predict_rejects_invalid_image_content():
    with pytest.raises(InvalidImageError):
        predict_waste(b"ceci n'est pas une image", "fake.jpg")
