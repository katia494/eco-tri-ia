import json
import sqlite3
from pathlib import Path

from PIL import Image

from src import import_data


CLASSES = ("cardboard", "glass", "metal", "paper", "plastic", "trash")


def create_image(path: Path, color: tuple[int, int, int]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    Image.new("RGB", (12, 12), color).save(path, format="JPEG")


def create_source(
    root: Path,
    prefix: str,
    duplicate_glass_path: Path | None = None,
) -> None:
    """Crée six images, avec un doublon glass seulement si demandé."""
    source_offset = 20 if prefix == "v1" else 180

    for index, category in enumerate(CLASSES):
        target = root / category / f"{prefix}_{category}.jpg"

        if category == "glass" and duplicate_glass_path is not None:
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(duplicate_glass_path.read_bytes())
        else:
            create_image(
                target,
                (
                    (source_offset + index * 7) % 255,
                    (index * 53 + 20) % 255,
                    (index * 71 + 40) % 255,
                ),
            )


def write_configuration(path: Path, v1_root: Path, v2_root: Path) -> None:
    payload = {
        "sources": [
            {
                "id": "garbage_classification_v1",
                "name": "Garbage Classification",
                "role": "training_historical_v2",
                "local_directory": str(v1_root),
            },
            {
                "id": "garbage_classification_v2",
                "name": "Garbage Classification V2",
                "role": "training_extension_v3",
                "local_directory": str(v2_root),
            },
            {
                "id": "realwaste",
                "name": "RealWaste",
                "role": "external_evaluation_only",
                "local_directory": str(path.parent / "realwaste"),
            },
        ]
    }
    path.write_text(json.dumps(payload), encoding="utf-8")


def test_multisource_import_deduplicates_and_keeps_provenance(
    tmp_path,
    monkeypatch,
):
    """Deux sources, un doublon : une image canonique et deux provenances."""
    v1_root = tmp_path / "v1"
    v2_root = tmp_path / "v2"

    create_source(v1_root, "v1")
    create_source(
        v2_root,
        "v2",
        duplicate_glass_path=v1_root / "glass" / "v1_glass.jpg",
    )

    config_path = tmp_path / "dataset_sources.json"
    exclusions_path = tmp_path / "catalog_exclusions.json"
    database_path = tmp_path / "catalog.db"
    report_path = tmp_path / "report.json"

    write_configuration(config_path, v1_root, v2_root)
    exclusions_path.write_text('{"files": []}', encoding="utf-8")

    monkeypatch.setattr(import_data, "CONFIG_PATH", config_path)
    monkeypatch.setattr(import_data, "EXCLUSIONS_PATH", exclusions_path)
    monkeypatch.setattr(
        import_data,
        "SCHEMA_PATH",
        Path("sql/schema.sql"),
    )

    report = import_data.import_catalog(
        database_path=database_path,
        report_path=report_path,
    )

    assert report["total_candidates"] == 12
    assert report["canonical_images"] == 11
    assert report["provenance_links"] == 12
    assert report["duplicate_occurrences"] == 1
    assert report["foreign_key_errors"] == 0

    connection = sqlite3.connect(database_path)

    try:
        assert connection.execute(
            "SELECT COUNT(*) FROM sources_donnees"
        ).fetchone()[0] == 3

        assert connection.execute(
            "SELECT COUNT(*) FROM dechets"
        ).fetchone()[0] == 11

        assert connection.execute(
            "SELECT COUNT(*) FROM dechet_sources"
        ).fetchone()[0] == 12

    finally:
        connection.close()

    # Un second import explicite reconstruit la même base sans changer le résultat.
    repeated_report = import_data.import_catalog(
        database_path=database_path,
        report_path=report_path,
        replace_output=True,
    )

    assert repeated_report["canonical_images"] == 11
    assert repeated_report["provenance_links"] == 12
    assert repeated_report["duplicate_occurrences"] == 1