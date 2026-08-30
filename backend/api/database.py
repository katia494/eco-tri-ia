from pathlib import Path

from sqlalchemy import create_engine, inspect, text
from sqlalchemy.orm import declarative_base, sessionmaker

from backend.api.config import settings


DATABASE_URL = settings.database_url

if not DATABASE_URL.startswith("sqlite"):
    raise ValueError(
        "ECO-TRI MVP utilise SQLite. DATABASE_URL doit commencer par 'sqlite'."
    )

if DATABASE_URL.startswith("sqlite:///./"):
    database_path = Path(DATABASE_URL.removeprefix("sqlite:///./"))
    database_path.parent.mkdir(parents=True, exist_ok=True)

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def migrate_legacy_predictions_schema(target_engine=engine) -> bool:
    """Archive l'ancienne table française sans supprimer ses données."""
    expected_columns = {"id", "image_name", "waste_class", "confidence", "created_at"}
    legacy_columns = {
        "id",
        "image_path",
        "categorie_predite",
        "confiance",
        "date_prediction",
    }

    with target_engine.begin() as connection:
        inspector = inspect(connection)
        tables = set(inspector.get_table_names())
        if "predictions" not in tables:
            return False

        columns = {
            column["name"] for column in inspector.get_columns("predictions")
        }
        if expected_columns.issubset(columns):
            return False
        if legacy_columns.issubset(columns):
            if "predictions_legacy" in tables:
                raise RuntimeError(
                    "Migration impossible : predictions_legacy existe déjà."
                )
            connection.execute(
                text("ALTER TABLE predictions RENAME TO predictions_legacy")
            )
            return True

        raise RuntimeError(
            "Schéma SQLite inconnu pour predictions : " + ", ".join(sorted(columns))
        )


def get_db():
    """Fournit une session de base de données."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
