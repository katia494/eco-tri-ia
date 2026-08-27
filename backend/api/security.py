from fastapi import Security, HTTPException, status
from fastapi.security import APIKeyHeader
import os

API_KEY_NAME = "X-API-Key"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

def get_api_key(api_key: str = Security(api_key_header)) -> str:
    """
    Vérifie la clé API dans les headers de la requête.
    
    En développement, la clé est optionnelle.
    En production, elle est obligatoire.
    """
    expected_key = os.getenv("API_KEY", None)
    
    # Si pas de clé configurée = mode développement
    if expected_key is None:
        return "dev-mode"
    
    # Vérification de la clé
    if api_key == expected_key:
        return api_key
    
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Clé API invalide ou manquante"
    )