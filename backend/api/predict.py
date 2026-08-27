import os
import numpy as np
from PIL import Image
import io

# Classes de déchets reconnus par le modèle
WASTE_CLASSES = {
    0: "carton",
    1: "verre",
    2: "métal",
    3: "papier",
    4: "plastique",
    5: "déchets généraux"
}

def load_model():
    """Charge le modèle YOLOv8 depuis le chemin configuré."""
    try:
        from ultralytics import YOLO
        model_path = os.getenv("MODEL_PATH", "backend/models/yolo_waste.pt")
        if os.path.exists(model_path):
            model = YOLO(model_path)
            return model
        else:
            print(f"Modèle non trouvé à {model_path}, mode simulation activé")
            return None
    except Exception as e:
        print(f"Erreur chargement modèle: {e}")
        return None

def predict_waste(image_bytes: bytes, filename: str) -> dict:
    """
    Classifie un déchet à partir d'une image.
    Retourne la classe et le score de confiance.
    """
    model = load_model()

    if model is None:
        # Mode simulation si le modèle n'est pas disponible
        import random
        waste_class = random.choice(list(WASTE_CLASSES.values()))
        confidence = round(random.uniform(0.65, 0.95), 2)
        return {
            "waste_class": waste_class,
            "confidence": confidence,
            "image_name": filename,
            "message": f"Déchet classifié : {waste_class} (simulation)"
        }

    # Mode réel avec YOLOv8
    image = Image.open(io.BytesIO(image_bytes))
    results = model(image)

    if results and len(results[0].boxes) > 0:
        box = results[0].boxes[0]
        class_id = int(box.cls[0])
        confidence = float(box.conf[0])
        waste_class = WASTE_CLASSES.get(class_id, "inconnu")
    else:
        waste_class = "non détecté"
        confidence = 0.0

    return {
        "waste_class": waste_class,
        "confidence": round(confidence, 2),
        "image_name": filename,
        "message": f"Déchet classifié : {waste_class}"
    }