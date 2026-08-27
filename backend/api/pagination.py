from pydantic import BaseModel, Field
from typing import TypeVar, Generic, List
from fastapi import Query

T = TypeVar("T")

class PaginationParams:
    """Paramètres de pagination réutilisables."""
    def __init__(
        self,
        page: int = Query(default=1, ge=1, description="Numéro de page"),
        size: int = Query(default=10, ge=1, le=100, description="Taille de la page")
    ):
        self.page = page
        self.size = size
        self.skip = (page - 1) * size

class PageResponse(BaseModel, Generic[T]):
    """Réponse paginée générique."""
    items: List[T]
    total: int
    page: int
    size: int
    pages: int

    @classmethod
    def create(cls, items: list, total: int, params: PaginationParams):
        """Crée une réponse paginée."""
        return cls(
            items=items,
            total=total,
            page=params.page,
            size=params.size,
            pages=(total + params.size - 1) // params.size
        )