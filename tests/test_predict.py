# tests/test_predict.py
# Tests du module de prédiction ECO-TRI
# Compétence C13 — Tests automatisés

import pytest
import numpy as np
from unittest.mock import patch, MagicMock
from backend.api.predict import predict_waste, CATEGORIES, WASTE_CLASSES

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
    from PIL import Image
    import io

    # Créer une image factice en mémoire
    img = Image.new("RGB", (64, 64), color=(100, 150, 200))
    buf = io.BytesIO()
    img.save(buf, format="JPEG")
    image_bytes = buf.getvalue()

    result = predict_waste(image_bytes, "test.jpg")

    assert isinstance(result, dict), "❌ Le résultat doit être un dictionnaire !"
    print(f"✅ Résultat : {result}")

# ─── Test 3 — La confiance est entre 0 et 1 ───────────────────────
def test_predict_returns_valid_confidence():
    """Vérifie que la confiance est entre 0 et 1."""
    from PIL import Image
    import io

    img = Image.new("RGB", (64, 64), color=(200, 100, 50))
    buf = io.BytesIO()
    img.save(buf, format="JPEG")
    image_bytes = buf.getvalue()

    result = predict_waste(image_bytes, "test.jpg")

    assert "confidence" in result, "❌ Clé confidence manquante !"
    assert 0.0 <= result["confidence"] <= 1.0, f"❌ Confiance hors limites : {result['confidence']}"
    print(f"✅ Confiance valide : {result['confidence']}")

# ─── Test 4 — La classe retournée est valide ──────────────────────
def test_predict_returns_valid_class():
    """Vérifie que la classe retournée est dans CATEGORIES."""
    from PIL import Image
    import io

    img = Image.new("RGB", (64, 64), color=(50, 200, 100))
    buf = io.BytesIO()
    img.save(buf, format="JPEG")
    image_bytes = buf.getvalue()

    result = predict_waste(image_bytes, "test.jpg")

    assert "waste_class" in result, "❌ Clé waste_class manquante !"
    assert result["waste_class"] in CATEGORIES, f"❌ Classe inconnue : {result['waste_class']}"
    print(f"✅ Classe valide : {result['waste_class']}")