import os
import joblib
import numpy as np
from PIL import Image
import io

# ─── Chemins des modèles ───────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, "models", "model_eco_tri_xgb.pkl")
ENCODER_PATH = os.path.join(BASE_DIR, "models", "label_encoder.pkl")

# ─── Catégories dans le bon ordre ──────────────────────────────────
CATEGORIES = ["cardboard", "glass", "metal", "paper", "plastic", "trash"]

# ─── Chargement du modèle ──────────────────────────────────────────
model = joblib.load(MODEL_PATH)
label_encoder = joblib.load(ENCODER_PATH)
print(f"✅ Modèle XGBoost chargé depuis {MODEL_PATH}")


# ─── Fonction de prédiction ────────────────────────────────────────
def predict_waste(image_bytes: bytes, filename: str = "") -> dict:
    """Prédit la catégorie d'un déchet à partir d'une image"""

    # 1. Ouvrir l'image et la convertir en RGB
    img = Image.open(io.BytesIO(image_bytes)).convert("RGB")

    # 2. Redimensionner en 64x64
    img = img.resize((64, 64))

    # 3. Convertir en tableau numpy et aplatir
    img_array = np.array(img).flatten().reshape(1, -1)

    # 4. Normaliser entre 0 et 1
    img_array = img_array / 255.0

    # 5. Prédiction
    prediction = int(model.predict(img_array)[0])
    probabilities = model.predict_proba(img_array)[0]
    confidence = float(probabilities[prediction])

    # 6. Convertir le chiffre en nom de catégorie
    label = CATEGORIES[prediction]

    # 7. Retourner le résultat complet
    return {
        "waste_class": label,
        "confidence": round(confidence, 2),
        "model": "XGBoost",
        "image_name": filename,
        "message": f"Déchet classifié comme {label} avec {round(confidence, 2)}% de confiance"
    }