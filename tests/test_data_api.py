import pytest
from fastapi.testclient import TestClient

from backend.api.config import settings
from backend.api.main import app
from backend.api.models import WasteRecord
from tests.conftest import TestingSessionLocal

client = TestClient(app)


@pytest.fixture
def api_key(monkeypatch):
    """Clé isolée pour les tests : aucune clé privée locale n'est utilisée."""
    key = "test-c5-api-key"
    monkeypatch.setattr(settings, "data_api_key", key)
    return key


@pytest.fixture
def records(api_key):
    """Insère trois enregistrements temporaires dans SQLite pour les tests."""
    db = TestingSessionLocal()

    try:
        first_record = WasteRecord(
            file_name="plastic_bottle.jpg",
            category="plastic",
            image_path="data/raw/sample/plastic_bottle.jpg",
            source="Garbage Classification V2",
            created_at="2026-09-01",
        )
        second_record = WasteRecord(
            file_name="cardboard_box.jpg",
            category="cardboard",
            image_path="data/raw/sample/cardboard_box.jpg",
            source="Garbage Classification",
            created_at="2026-09-01",
        )
        third_record = WasteRecord(
            file_name="glass_jar.jpg",
            category="glass",
            image_path="data/raw/sample/glass_jar.jpg",
            source="RealWaste",
            created_at="2026-09-01",
        )

        db.add_all([first_record, second_record, third_record])
        db.commit()
        db.refresh(first_record)

        yield first_record

    finally:
        db.close()


def test_health_remains_public():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_records_rejects_request_without_api_key(api_key):
    response = client.get("/records")

    assert response.status_code == 401
    assert response.json()["detail"] == "Clé API absente ou invalide."


def test_records_rejects_wrong_api_key(api_key):
    response = client.get(
        "/records",
        headers={"x-api-key": "wrong-key"},
    )

    assert response.status_code == 401


def test_records_returns_paginated_data_with_valid_api_key(api_key, records):
    response = client.get(
        "/records?skip=0&limit=2",
        headers={"x-api-key": api_key},
    )

    assert response.status_code == 200

    data = response.json()
    assert data["total"] == 3
    assert data["skip"] == 0
    assert data["limit"] == 2
    assert len(data["items"]) == 2


def test_record_by_id_returns_data_with_valid_api_key(api_key, records):
    response = client.get(
        f"/records/{records.id}",
        headers={"x-api-key": api_key},
    )

    assert response.status_code == 200

    data = response.json()
    assert data["id"] == records.id
    assert data["file_name"] == "plastic_bottle.jpg"
    assert data["category"] == "plastic"


def test_record_by_unknown_id_returns_404(api_key):
    response = client.get(
        "/records/99999",
        headers={"x-api-key": api_key},
    )

    assert response.status_code == 404


def test_search_filters_records_with_valid_api_key(api_key, records):
    response = client.get(
        "/search?q=plastic",
        headers={"x-api-key": api_key},
    )

    assert response.status_code == 200

    data = response.json()
    assert data["total"] == 1
    assert data["items"][0]["category"] == "plastic"
    assert data["items"][0]["file_name"] == "plastic_bottle.jpg"