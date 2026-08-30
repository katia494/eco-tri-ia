from unittest.mock import Mock, patch

import httpx
from fastapi.testclient import TestClient

from backend.api.main import app


client = TestClient(app)


def test_collection_points_returns_nearby_compatible_places():
    fake_response = Mock()
    fake_response.raise_for_status.return_value = None
    fake_response.json.return_value = {
        "elements": [
            {
                "type": "node",
                "lat": 48.7982,
                "lon": 2.3125,
                "tags": {
                    "amenity": "recycling",
                    "name": "Collecte de piles",
                    "recycling:batteries": "yes",
                    "addr:street": "Avenue Henri Ravera",
                    "addr:city": "Bagneux",
                },
            },
            {
                "type": "node",
                "lat": 48.7990,
                "lon": 2.3150,
                "tags": {
                    "amenity": "recycling",
                    "name": "Conteneur à verre",
                    "recycling:glass_bottles": "yes",
                },
            },
        ]
    }

    with patch(
        "backend.api.collection_points.httpx.post",
        return_value=fake_response,
    ):
        response = client.get(
            "/collection-points",
            params={
                "latitude": 48.7980,
                "longitude": 2.3130,
                "waste_type": "battery",
            },
        )

    assert response.status_code == 200

    data = response.json()
    assert data["waste_type"] == "battery"
    assert data["provider"] == "OpenStreetMap / Overpass"
    assert len(data["points"]) == 1
    assert data["points"][0]["name"] == "Collecte de piles"
    assert data["points"][0]["address"] == "Avenue Henri Ravera, Bagneux"
    assert data["points"][0]["distance_meters"] >= 0


def test_collection_points_rejects_unsupported_waste_type():
    response = client.get(
        "/collection-points",
        params={
            "latitude": 48.7980,
            "longitude": 2.3130,
            "waste_type": "wood",
        },
    )

    assert response.status_code == 422


def test_collection_points_returns_503_when_provider_is_unavailable():
    with patch(
        "backend.api.collection_points.httpx.post",
        side_effect=httpx.ConnectError("provider unavailable"),
    ):
        response = client.get(
            "/collection-points",
            params={
                "latitude": 48.7980,
                "longitude": 2.3130,
                "waste_type": "glass",
            },
        )

    assert response.status_code == 503