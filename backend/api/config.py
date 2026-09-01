from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    """Configuration centralisée de l'application ECO-TRI."""

    # Application
    app_name: str = "ECO-TRI API"
    app_version: str = "1.0.0"
    debug: bool = False

    # Base de données
    # Une base SQLite unique pour le MVP. Le fichier est généré localement et
    # n'est pas versionné afin d'éviter de commiter l'historique des utilisateurs.
    database_url: str = "sqlite:///./data/eco_tri.db"

    # Modèle IA
    model_path: str = "backend/models/best.pt"
    model_version: str = "yolov8n-cls-v2"
    confidence_threshold: float = 0.60
    max_upload_bytes: int = 10 * 1024 * 1024
    data_api_key: str | None = None
    # CORS
    allowed_origins: list = ["http://localhost:5173"]

    model_config = SettingsConfigDict(env_file=".env", case_sensitive=False)

settings = Settings()
