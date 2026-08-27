from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.sql import func
from backend.api.database import Base

class Prediction(Base):
    """Modèle SQLAlchemy pour stocker les prédictions de déchets."""
    __tablename__ = "predictions"

    id = Column(Integer, primary_key=True, index=True)
    image_name = Column(String, nullable=False)
    waste_class = Column(String, nullable=False)
    confidence = Column(Float, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return (
            f"<​Prediction(id={self.id}, "
            f"class={self.waste_class}, "
            f"confidence={self.confidence:.2f})>"
        )