import numpy as np
from PIL import Image
import io

# Taille standard pour YOLOv8
IMAGE_SIZE = (640, 640)

def preprocess_image(image_bytes: bytes) -> np.ndarray:
    """
    Prétraite une image pour l'inférence YOLOv8.
    
    Étapes :
    1. Chargement de l'image
    2. Redimensionnement à 640x640
    3. Normalisation des pixels (0-255 → 0.0-1.0)
    4. Conversion en tableau numpy
    
    Args:
        image_bytes: Image en bytes
    
    Returns:
        np.ndarray: Image prétraitée
    """
    # Charger l'image
    image = Image.open(io.BytesIO(image_bytes))
    
    # Convertir en RGB si nécessaire
    if image.mode != "RGB":
        image = image.convert("RGB")
    
    # Redimensionner
    image = image.resize(IMAGE_SIZE)
    
    # Convertir en numpy
    img_array = np.array(image)
    
    # Normaliser (0-255 → 0.0-1.0)
    img_array = img_array.astype(np.float32) / 255.0
    
    return img_array

def validate_image(image_bytes: bytes) -> bool:
    """
    Valide qu'un fichier est une image valide.
    
    Args:
        image_bytes: Fichier en bytes
    
    Returns:
        bool: True si valide, False sinon
    """
    try:
        image = Image.open(io.BytesIO(image_bytes))
        image.verify()
        return True
    except Exception:
        return False

def get_image_info(image_bytes: bytes) -> dict:
    """
    Retourne les informations d'une image.
    
    Args:
        image_bytes: Image en bytes
    
    Returns:
        dict: Informations sur l'image
    """
    image = Image.open(io.BytesIO(image_bytes))
    return {
        "width": image.width,
        "height": image.height,
        "mode": image.mode,
        "format": image.format
    }