from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.api.routes import router
from backend.api.database import engine, Base

# Crée les tables automatiquement au démarrage
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="ECO-TRI API",
    description="API de classification des déchets par IA (YOLOv8)",
    version="1.0.0"
)

# Configuration CORS pour le frontend React
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclusion des routes
app.include_router(router)

@app.get("/health")
def health_check():
    """Vérifie que l'API est opérationnelle."""
    return {
        "status": "ok",
        "message": "ECO-TRI API is running",
        "version": "1.0.0"
    }

@app.get("/")
def root():
    """Route racine."""
    return {"message": "Bienvenue sur l'API ECO-TRI 🌿"}