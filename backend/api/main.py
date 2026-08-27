from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

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