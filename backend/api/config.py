from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    """Configuration centralisée de l'application ECO-TRI."""

    # Application
    app_name: str = "ECO-TRI API"
    app_version: str = "1.0.0"
    debug: bool = False

    # Base de données
    database_url: str = "sqlite:///./eco_tri.db"

    # Modèle IA
    model_path: str = "backend/models/yolo_waste.pt"
    confidence_threshold: float = 0.5

    # CORS
    allowed_origins: list = ["http://localhost:5173"]

    class Config:
        env_file = ".env"
        case_sensitive = False

settings = Settings()