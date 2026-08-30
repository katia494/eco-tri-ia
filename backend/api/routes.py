from fastapi import APIRouter, UploadFile, File, Depends, HTTPException,Query
from sqlalchemy.orm import Session
from typing import List
from backend.api.database import get_db
from backend.api.models import Prediction
from backend.api.schemas import (
    PredictionResponse,
    PredictResponse,
    ModelInfoResponse,
    CollectionPointsResponse,
)
from backend.api.predict import CATEGORIES, predict_waste
from backend.api.config import settings
from backend.api.exceptions import ImageTooLargeError, InvalidImageError
from backend.api.collection_points import (
    CollectionPointsProviderError,
    get_collection_points,
)
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


@router.get(
    "/collection-points",
    response_model=CollectionPointsResponse,
    tags=["Points de collecte"],
)
def get_nearby_collection_points(
    latitude: float = Query(..., ge=-90, le=90),
    longitude: float = Query(..., ge=-180, le=180),
    waste_type: str = Query(..., min_length=3, max_length=20),
    radius_meters: int = Query(3000, ge=100, le=10_000),
):
    """
    Recherche les points de collecte proches compatibles avec
    le type de déchet reconnu.
    """
    try:
        points = get_collection_points(
            latitude=latitude,
            longitude=longitude,
            waste_type=waste_type,
            radius_meters=radius_meters,
        )
    except ValueError as error:
        raise HTTPException(status_code=422, detail=str(error)) from error
    except CollectionPointsProviderError as error:
        raise HTTPException(status_code=503, detail=str(error)) from error

    return {
        "waste_type": waste_type,
        "radius_meters": radius_meters,
        "provider": "OpenStreetMap / Overpass",
        "points": points,
    }
