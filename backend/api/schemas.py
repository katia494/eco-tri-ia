from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime
from typing import Optional

class PredictionBase(BaseModel):
    """Schéma de base pour une prédiction."""
    image_name: str
    waste_class: str
    confidence: float = Field(ge=0.0, le=1.0)

class PredictionCreate(PredictionBase):
    """Schéma pour créer une prédiction."""
    pass

class PredictionResponse(PredictionBase):
    """Schéma de réponse avec l'ID et la date."""
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class PredictResponse(BaseModel):
    """Schéma de réponse de l'endpoint /predict."""
    waste_class: str
    confidence: float
    model: str
    message: str
    image_name: str
    sorting_instruction: str

class ModelInfoResponse(BaseModel):
    """Informations publiques sur le modèle chargé par l'API."""
    name: str
    task: str
    classes: list[str]
    input_size: int
