import time
from typing import Any, Optional

class SimpleCache:
    """
    Cache simple en mémoire avec expiration.
    Évite les requêtes répétées à la base de données.
    """
    def __init__(self):
        self._cache = {}
        self._expiry = {}

    def get(self, key: str) -> Optional[Any]:
        """Récupère une valeur du cache si elle n'est pas expirée."""
        if key in self._cache:
            if time.time() < self._expiry[key]:
                return self._cache[key]
            else:
                # Cache expiré
                del self._cache[key]
                del self._expiry[key]
        return None

    def set(self, key: str, value: Any, ttl: int = 300):
        """
        Stocke une valeur dans le cache.
        
        Args:
            key: Clé du cache
            value: Valeur à stocker
            ttl: Durée de vie en secondes (défaut: 5 minutes)
        """
        self._cache[key] = value
        self._expiry[key] = time.time() + ttl

    def delete(self, key: str):
        """Supprime une valeur du cache."""
        if key in self._cache:
            del self._cache[key]
            del self._expiry[key]

    def clear(self):
        """Vide tout le cache."""
        self._cache.clear()
        self._expiry.clear()

# Instance globale du cache
cache = SimpleCache()