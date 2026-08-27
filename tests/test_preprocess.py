import pytest
import numpy as np
import io
from PIL import Image
from backend.models.preprocess import (
    preprocess_image,
    validate_image,
    get_image_info,
    IMAGE_SIZE
)

def create_test_image(width=100, height=100, color=(255, 0, 0)):
    """Crée une image de test en mémoire."""
    img = Image.new("RGB", (width, height), color=color)
    img_bytes = io.BytesIO()
    img.save(img_bytes, format="JPEG")
    return img_bytes.getvalue()

def test_preprocess_image_shape():
    """Vérifie que l'image prétraitée a la bonne forme."""
    image_bytes = create_test_image()
    result = preprocess_image(image_bytes)
    assert result.shape == (IMAGE_SIZE[0], IMAGE_SIZE[1], 3)

def test_preprocess_image_normalized():
    """Vérifie que les pixels sont normalisés entre 0 et 1."""
    image_bytes = create_test_image()
    result = preprocess_image(image_bytes)
    assert result.min() >= 0.0
    assert result.max() <= 1.0

def test_preprocess_image_dtype():
    """Vérifie que le type de données est float32."""
    image_bytes = create_test_image()
    result = preprocess_image(image_bytes)
    assert result.dtype == np.float32

def test_validate_image_valid():
    """Vérifie qu'une image valide est acceptée."""
    image_bytes = create_test_image()
    assert validate_image(image_bytes) == True

def test_validate_image_invalid():
    """Vérifie qu'un fichier invalide est rejeté."""
    fake_bytes = b"ceci n'est pas une image"
    assert validate_image(fake_bytes) == False

def test_get_image_info():
    """Vérifie les informations retournées sur l'image."""
    image_bytes = create_test_image(width=200, height=150)
    info = get_image_info(image_bytes)
    assert info["width"] == 200
    assert info["height"] == 150
    assert info["mode"] == "RGB"