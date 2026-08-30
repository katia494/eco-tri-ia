from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from backend.api.routes import router
from backend.api.routes_stats import router_stats
from backend.api.database import engine, Base, migrate_legacy_predictions_schema
from backend.api.logger import logger
from backend.api.middleware import log_requests
from backend.api.exceptions import (
    ImageTooLargeError,
    InvalidImageError,
    ModelNotFoundError,
    image_too_large_handler,
    invalid_image_handler,
    model_not_found_handler
)
from backend.api.config import settings

# Archive un éventuel ancien schéma puis crée les tables attendues.
migrate_legacy_predictions_schema()
Base.metadata.create_all(bind=engine)

@asynccontextmanager
async def lifespan(_app: FastAPI):
    logger.info("ECO-TRI API démarrée avec succès")
    logger.info("Documentation disponible sur /docs")
    yield
    logger.info("ECO-TRI API arrêtée")


app = FastAPI(
    title="ECO-TRI API",
    description="API de classification d'images de déchets avec YOLOv8n-cls",
    version="1.0.0",
    lifespan=lifespan,
)

# Middleware de logging
app.add_middleware(BaseHTTPMiddleware, dispatch=log_requests)

# Configuration CORS pour le frontend React
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Gestionnaires d'erreurs personnalisés
app.add_exception_handler(ImageTooLargeError, image_too_large_handler)
app.add_exception_handler(InvalidImageError, invalid_image_handler)
app.add_exception_handler(ModelNotFoundError, model_not_found_handler)

# Inclusion des routes
app.include_router(router)
app.include_router(router_stats)

@app.get("/health")
def health_check():
    """Vérifie que l'API est opérationnelle."""
    logger.info("Health check effectué")
    return {
        "status": "ok",
        "message": "ECO-TRI API is running",
        "version": "1.0.0",
        "model": settings.model_version
    }

@app.get("/")
def root():
    """Route racine."""
    return {"message": "Bienvenue sur l'API ECO-TRI 🌿"}
