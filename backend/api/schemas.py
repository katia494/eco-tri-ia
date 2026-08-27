from pydantic import BaseModel, Field
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

    class Config:
        from_attributes = True

class PredictResponse(BaseModel):
    """Schéma de réponse de l'endpoint /predict."""
    waste_class: str
    confidence: float
    message: str
    image_name: str
