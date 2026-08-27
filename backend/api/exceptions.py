from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse

class ImageTooLargeError(Exception):
    """Exception levée quand l'image est trop grande."""
    pass

class InvalidImageError(Exception):
    """Exception levée quand le fichier n'est pas une image valide."""
    pass

class ModelNotFoundError(Exception):
    """Exception levée quand le modèle IA n'est pas trouvé."""
    pass

async def image_too_large_handler(
    request: Request,
    exc: ImageTooLargeError
):
    """Gestionnaire pour les images trop grandes."""
    return JSONResponse(
        status_code=413,
        content={
            "error": "Image trop grande",
            "message": str(exc),
            "max_size": "10MB"
        }
    )

async def invalid_image_handler(
    request: Request,
    exc: InvalidImageError
):
    """Gestionnaire pour les images invalides."""
    return JSONResponse(
        status_code=400,
        content={
            "error": "Image invalide",
            "message": str(exc)
        }
    )

async def model_not_found_handler(
    request: Request,
    exc: ModelNotFoundError
):
    """Gestionnaire pour le modèle manquant."""
    return JSONResponse(
        status_code=503,
        content={
            "error": "Modèle IA non disponible",
            "message": str(exc)
        }
    )