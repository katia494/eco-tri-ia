import math
from typing import Any

import httpx

OVERPASS_URLS = (
    "https://overpass-api.de/api/interpreter",
    "https://overpass.private.coffee/api/interpreter",
)

WASTE_TAGS = {
    "battery": ["recycling:batteries"],
    "glass": ["recycling:glass_bottles", "recycling:glass"],
    "metal": ["recycling:metal", "recycling:aluminium"],
    "paper": ["recycling:paper"],
    "cardboard": ["recycling:cardboard", "recycling:paper"],
    "plastic": ["recycling:plastic", "recycling:plastic_bottles"],
}

SUPPORTED_WASTE_TYPES = set(WASTE_TAGS) | {"trash"}


class CollectionPointsProviderError(RuntimeError):
    """Erreur lors de l'appel au fournisseur de points de collecte."""


def _distance_meters(
    latitude_a: float,
    longitude_a: float,
    latitude_b: float,
    longitude_b: float,
) -> int:
    """Calcule la distance entre deux coordonnées GPS en mètres."""
    earth_radius_meters = 6_371_000

    latitude_delta = math.radians(latitude_b - latitude_a)
    longitude_delta = math.radians(longitude_b - longitude_a)

    haversine = (
        math.sin(latitude_delta / 2) ** 2
        + math.cos(math.radians(latitude_a))
        * math.cos(math.radians(latitude_b))
        * math.sin(longitude_delta / 2) ** 2
    )

    return round(
        2 * earth_radius_meters * math.asin(math.sqrt(haversine))
    )


def _is_accepted(tags: dict[str, str], waste_type: str) -> bool:
    """Vérifie qu'un point accepte le type de déchet demandé."""
    if waste_type == "trash":
        return tags.get("amenity") == "waste_disposal"

    accepted_values = {"yes", "only", "designated"}

    return any(
        tags.get(tag_name, "").lower() in accepted_values
        for tag_name in WASTE_TAGS[waste_type]
    )


def _build_overpass_query(
    latitude: float,
    longitude: float,
    radius_meters: int,
) -> str:
    """Construit une requête Overpass autour de la position utilisateur."""
    return f"""
[out:json][timeout:10];
(
  nwr(around:{radius_meters},{latitude},{longitude})["amenity"="recycling"];
  nwr(around:{radius_meters},{latitude},{longitude})["amenity"="waste_disposal"];
);
out center tags;
"""


def _fetch_overpass_elements(
    latitude: float,
    longitude: float,
    radius_meters: int,
) -> list[dict[str, Any]]:
    """Interroge Overpass avec un fournisseur de secours."""
    query = _build_overpass_query(latitude, longitude, radius_meters)
    last_error: Exception | None = None

    for provider_url in OVERPASS_URLS:
        try:
            response = httpx.post(
                provider_url,
                data={"data": query},
                headers={
                    "User-Agent": "eco-tri-ia/1.0 (projet pedagogique)"
                },
                timeout=10.0,
            )
            response.raise_for_status()
            return response.json().get("elements", [])
        except (httpx.HTTPError, ValueError) as error:
            last_error = error

    raise CollectionPointsProviderError(
        "Les services de points de collecte sont temporairement indisponibles."
    ) from last_error


def get_collection_points(
    latitude: float,
    longitude: float,
    waste_type: str,
    radius_meters: int = 3000,
    limit: int = 5,
) -> list[dict[str, Any]]:
    """
    Retourne les points de collecte OpenStreetMap compatibles,
    triés du plus proche au plus éloigné.
    """
    waste_type = waste_type.lower()

    if waste_type not in SUPPORTED_WASTE_TYPES:
        raise ValueError(
            f"Type de déchet non pris en charge : {waste_type}"
        )

    elements = _fetch_overpass_elements(
        latitude=latitude,
        longitude=longitude,
        radius_meters=radius_meters,
    )

    collection_points = []

    for element in elements:
        tags = element.get("tags", {})

        if not _is_accepted(tags, waste_type):
            continue

        point_latitude = element.get("lat") or element.get(
            "center", {}
        ).get("lat")
        point_longitude = element.get("lon") or element.get(
            "center", {}
        ).get("lon")

        if point_latitude is None or point_longitude is None:
            continue

        street = " ".join(
            value
            for value in [
                tags.get("addr:housenumber"),
                tags.get("addr:street"),
            ]
            if value
        )

        address = ", ".join(
            value
            for value in [
                street,
                tags.get("addr:postcode"),
                tags.get("addr:city"),
            ]
            if value
        ) or None

        collection_points.append(
            {
                "name": tags.get("name", "Point de collecte"),
                "latitude": point_latitude,
                "longitude": point_longitude,
                "distance_meters": _distance_meters(
                    latitude,
                    longitude,
                    point_latitude,
                    point_longitude,
                ),
                "address": address,
                "source": "OpenStreetMap",
            }
        )

    return sorted(
        collection_points,
        key=lambda point: point["distance_meters"],
    )[:limit]