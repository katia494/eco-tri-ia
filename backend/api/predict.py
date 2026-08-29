"""Service d'inférence YOLOv8 pour la classification des déchets."""

from __future__ import annotations

import io
from pathlib import Path
from threading import Lock

from PIL import Image, UnidentifiedImageError

from backend.api.config import settings
from backend.api.exceptions import InvalidImageError, ModelNotFoundError


CATEGORIES = ["cardboard", "glass", "metal", "paper", "plastic", "trash"]
WASTE_CLASSES = CATEGORIES

SORTING_INSTRUCTIONS = {
    "cardboard": "Videz et aplatissez le carton avant de le déposer dans le bac de tri.",
    "glass": "Déposez le verre dans le conteneur à verre, sans bouchon ni couvercle.",
    "metal": "Déposez l'emballage métallique vide dans le bac de tri.",
    "paper": "Déposez le papier propre et sec dans le bac de tri.",
    "plastic": "Videz l'emballage plastique et déposez-le dans le bac de tri.",
    "trash": "Ce déchet n'est pas identifié comme recyclable : utilisez les ordures ménagères.",
}


class YoloClassificationService:
    """Charge le modèle une seule fois et expose une méthode de prédiction."""

    def __init__(self, model_path: Path) -> None:
        self.model_path = model_path
        self._model = None
        self._lock = Lock()

    def _load_model(self):
        if self._model is not None:
            return self._model
        if not self.model_path.is_file():
            raise ModelNotFoundError(
                f"Modèle absent : {self.model_path}. Lancez l'entraînement puis copiez best.pt."
            )
        with self._lock:
            if self._model is None:
                from ultralytics import YOLO

                self._model = YOLO(str(self.model_path))
        return self._model

    def predict(self, image: Image.Image) -> tuple[str, float]:
        model = self._load_model()
        result = model.predict(image, imgsz=224, verbose=False)[0]
        if result.probs is None:
            raise RuntimeError("Le modèle n'a retourné aucune probabilité de classification.")
        class_index = int(result.probs.top1)
        confidence = float(result.probs.top1conf.item())
        class_name = str(result.names[class_index])
        if class_name not in CATEGORIES:
            raise RuntimeError(f"Classe inattendue retournée par le modèle : {class_name}")
        return class_name, confidence


service = YoloClassificationService(Path(settings.model_path))


def decode_image(image_bytes: bytes) -> Image.Image:
    """Vérifie le contenu réel du fichier et retourne une image RGB."""
    try:
        with Image.open(io.BytesIO(image_bytes)) as source:
            source.verify()
        with Image.open(io.BytesIO(image_bytes)) as source:
            return source.convert("RGB")
    except (UnidentifiedImageError, OSError, ValueError) as exc:
        raise InvalidImageError("Le contenu envoyé n'est pas une image JPG ou PNG valide.") from exc


def predict_waste(image_bytes: bytes, filename: str = "") -> dict:
    """Classifie une image et retourne un contrat JSON stable."""
    image = decode_image(image_bytes)
    waste_class, confidence = service.predict(image)
    confidence = round(confidence, 4)
    return {
        "waste_class": waste_class,
        "confidence": confidence,
        "model": settings.model_version,
        "image_name": filename,
        "sorting_instruction": SORTING_INSTRUCTIONS[waste_class],
        "message": (
            f"Déchet classifié comme {waste_class} "
            f"avec {confidence * 100:.1f} % de confiance."
        ),
    }
