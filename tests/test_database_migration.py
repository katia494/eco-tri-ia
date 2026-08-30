from sqlalchemy import create_engine, inspect, text

from backend.api.database import migrate_legacy_predictions_schema


def test_legacy_prediction_table_is_archived(tmp_path):
    test_engine = create_engine(f"sqlite:///{tmp_path / 'legacy.db'}")
    with test_engine.begin() as connection:
        connection.execute(
            text(
                """
                CREATE TABLE predictions (
                    id INTEGER PRIMARY KEY,
                    image_path TEXT,
                    categorie_predite TEXT,
                    confiance REAL,
                    date_prediction TEXT
                )
                """
            )
        )
        connection.execute(
            text(
                """
                INSERT INTO predictions
                    (image_path, categorie_predite, confiance, date_prediction)
                VALUES ('scan.jpg', 'glass', 0.9, CURRENT_TIMESTAMP)
                """
            )
        )

    assert migrate_legacy_predictions_schema(test_engine) is True

    tables = inspect(test_engine).get_table_names()
    assert "predictions" not in tables
    assert "predictions_legacy" in tables
    with test_engine.connect() as connection:
        count = connection.execute(
            text("SELECT COUNT(*) FROM predictions_legacy")
        ).scalar_one()
    assert count == 1
