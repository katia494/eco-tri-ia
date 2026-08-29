import os
import pickle
import numpy as np
from PIL import Image
import io

# Même ordre que pendant l'entraînement (alphabétique)
CATEGORIES = ["cardboard", "glass", "metal", "paper", "plastic", "trash"]

# Traduction français pour l'affichage
TRADUCTION = {
    "cardboard": "carton",
    "glass": "verre",
    "metal": "métal",
    "paper": "papier",
    "plastic": "plastique",
    "trash": "déchets généraux"
}

IMG_SIZE = (64, 64)

def load_model():
    """Charge le modèle RandomForest depuis le fichier .pkl"""
    model_path = os.getenv("MODEL_PATH", "backend/models/model_eco_tri.pkl")
    try:
        with open(model_path, "rb") as f:
            model = pickle.load(f)
        print(f"✅ Modèle chargé depuis {model_path}")
        return model
    except Exception as e:
        print(f"❌ Erreur chargement modèle: {e}")
        return None

# Chargement du modèle une seule fois au démarrage
model = load_model()

def predict_waste(image_bytes: bytes, filename: str) -> dict:
    """Classifie un déchet à partir d'une image."""

    if model is None:
        return {
            "waste_class": "inconnu",
            "confidence": 0.0,
            "image_name": filename,
            "message": "Modèle non disponible"
        }

    # Préparer l'image exactement comme dans le notebook
    image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    image = image.resize(IMG_SIZE)
    img_array = np.array(image).flatten().reshape(1, -1)

    # Prédiction
    pred_index = int(model.predict(img_array)[0])
    probabilities = model.predict_proba(img_array)[0]
    confidence = round(float(probabilities.max()), 2)

    # Convertir le numéro en mot anglais, puis en français
    pred_label = CATEGORIES[pred_index]
    label_fr = TRADUCTION.get(pred_label, pred_label)

    return {
        "waste_class": label_fr,
        "confidence": confidence,
        "image_name": filename,
        "message": f"Déchet classifié : {label_fr}"
    }