from typing import Annotated

from fastapi import Header, HTTPException, status

from .config import settings


def require_data_api_key(
    x_api_key: Annotated[str | None, Header()] = None,
) -> None:
    """Autorise l'accès uniquement avec la clé envoyée dans x-api-key."""
    expected_key = settings.data_api_key

    if not expected_key or expected_key == "replace_with_a_long_random_key":
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="DATA_API_KEY n'est pas configurée sur le serveur.",
        )

    if x_api_key != expected_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Clé API absente ou invalide.",
        )