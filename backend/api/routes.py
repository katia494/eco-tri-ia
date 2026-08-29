from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from backend.api.database import get_db
from backend.api.models import Prediction
from backend.api.schemas import PredictionResponse, PredictResponse, ModelInfoResponse
from backend.api.predict import CATEGORIES, predict_waste
from backend.api.config import settings
from backend.api.exceptions import ImageTooLargeError, InvalidImageError

router = APIRouter()

@router.post("/predict", response_model=PredictResponse)
async def predict(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """
    Classifie un déchet à partir d'une image uploadée.
    Sauvegarde le résultat en base de données.
    """
    if file.content_type not in {"image/jpeg", "image/png"}:
        raise HTTPException(
            status_code=400,
            detail="Seuls les fichiers JPG et PNG sont acceptés."
        )

    image_bytes = await file.read()
    if not image_bytes:
        raise InvalidImageError("Le fichier envoyé est vide.")
    if len(image_bytes) > settings.max_upload_bytes:
        raise ImageTooLargeError(
            f"Le fichier fait {len(image_bytes)} octets, limite : {settings.max_upload_bytes}."
        )
    result = predict_waste(image_bytes, file.filename)

    # Sauvegarde en base de données
    prediction = Prediction(
        image_name=result["image_name"],
        waste_class=result["waste_class"],
        confidence=result["confidence"]
    )
    db.add(prediction)
    db.commit()
    db.refresh(prediction)

    return result

@router.get("/model/info", response_model=ModelInfoResponse, tags=["Modèle"])
def get_model_info():
    """Décrit le modèle utilisé sans déclencher une inférence."""
    return {
        "name": settings.model_version,
        "task": "image-classification",
        "classes": CATEGORIES,
        "input_size": 224,
    }

@router.get("/predictions", response_model=List[PredictionResponse])
def get_predictions(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    """Récupère l'historique des prédictions."""
    predictions = db.query(Prediction).offset(skip).limit(limit).all()
    return predictions

@router.get("/predictions/{prediction_id}", response_model=PredictionResponse)
def get_prediction(prediction_id: int, db: Session = Depends(get_db)):
    """Récupère une prédiction par son ID."""
    prediction = db.query(Prediction).filter(
        Prediction.id == prediction_id
    ).first()
    if not prediction:
        raise HTTPException(status_code=404, detail="Prédiction non trouvée")
    return prediction
