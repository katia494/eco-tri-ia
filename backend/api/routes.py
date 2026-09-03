from typing import List

from fastapi import APIRouter, Depends, File, HTTPException, Query, UploadFile
from sqlalchemy import or_
from sqlalchemy.orm import Session

from backend.api.collection_points import (
    CollectionPointsProviderError,
    get_collection_points,
)
from backend.api.config import settings
from backend.api.database import get_db
from backend.api.exceptions import ImageTooLargeError, InvalidImageError
from backend.api.models import Prediction, WasteRecord
from backend.api.predict import CATEGORIES, predict_waste
from backend.api.schemas import (
    CollectionPointsResponse,
    ModelInfoResponse,
    PredictResponse,
    PredictionResponse,
    RecordsPageResponse,
    WasteRecordResponse,
)
from backend.api.security import require_data_api_key

router = APIRouter()


@router.post(
    "/predict",
    response_model=PredictResponse,
    dependencies=[Depends(require_data_api_key)],
)
async def predict(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    """
    Classifie un déchet à partir d'une image uploadée.
    Sauvegarde le résultat en base de données.
    """
    if file.content_type not in {"image/jpeg", "image/png"}:
        raise HTTPException(
            status_code=400,
            detail="Seuls les fichiers JPG et PNG sont acceptés.",
        )

    image_bytes = await file.read()

    if not image_bytes:
        raise InvalidImageError("Le fichier envoyé est vide.")

    if len(image_bytes) > settings.max_upload_bytes:
        raise ImageTooLargeError(
            f"Le fichier fait {len(image_bytes)} octets, "
            f"limite : {settings.max_upload_bytes}."
        )

    result = predict_waste(image_bytes, file.filename)

    prediction = Prediction(
        image_name=result["image_name"],
        waste_class=result["waste_class"],
        confidence=result["confidence"],
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
    db: Session = Depends(get_db),
):
    """Récupère l'historique des prédictions."""
    return db.query(Prediction).offset(skip).limit(limit).all()


@router.get("/predictions/{prediction_id}", response_model=PredictionResponse)
def get_prediction(
    prediction_id: int,
    db: Session = Depends(get_db),
):
    """Récupère une prédiction par son ID."""
    prediction = (
        db.query(Prediction)
        .filter(Prediction.id == prediction_id)
        .first()
    )

    if not prediction:
        raise HTTPException(
            status_code=404,
            detail="Prédiction non trouvée",
        )

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


@router.get(
    "/records",
    response_model=RecordsPageResponse,
    tags=["Données"],
)
def get_records(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    category: str | None = Query(None, min_length=3, max_length=20),
    db: Session = Depends(get_db),
    _: None = Depends(require_data_api_key),
):
    """Liste paginée des enregistrements importés."""
    query = db.query(WasteRecord)

    if category:
        query = query.filter(WasteRecord.category == category.lower())

    total = query.count()
    items = query.order_by(WasteRecord.id).offset(skip).limit(limit).all()

    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "items": items,
    }


@router.get(
    "/records/{record_id}",
    response_model=WasteRecordResponse,
    tags=["Données"],
)
def get_record(
    record_id: int,
    db: Session = Depends(get_db),
    _: None = Depends(require_data_api_key),
):
    """Retourne un enregistrement par son identifiant."""
    record = (
        db.query(WasteRecord)
        .filter(WasteRecord.id == record_id)
        .first()
    )

    if record is None:
        raise HTTPException(
            status_code=404,
            detail="Enregistrement non trouvé.",
        )

    return record


@router.get(
    "/search",
    response_model=RecordsPageResponse,
    tags=["Données"],
)
def search_records(
    q: str = Query(..., min_length=1, max_length=100),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    category: str | None = Query(None, min_length=3, max_length=20),
    db: Session = Depends(get_db),
    _: None = Depends(require_data_api_key),
):
    """Recherche un enregistrement par nom de fichier ou catégorie."""
    pattern = f"%{q.strip()}%"

    query = db.query(WasteRecord).filter(
        or_(
            WasteRecord.file_name.ilike(pattern),
            WasteRecord.category.ilike(pattern),
        )
    )

    if category:
        query = query.filter(WasteRecord.category == category.lower())

    total = query.count()
    items = query.order_by(WasteRecord.id).offset(skip).limit(limit).all()

    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "items": items,
    }
