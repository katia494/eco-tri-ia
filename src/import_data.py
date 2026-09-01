"""Import reproductible multi-source du catalogue ECO-TRI — C4.

Sources intégrées au catalogue :
- Garbage Classification V1 ;
- Garbage Classification V2, six catégories utiles au projet.

RealWaste reste documenté dans sources_donnees, mais n'est pas intégré au
catalogue d'entraînement car il est réservé à l'évaluation externe.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sqlite3
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path


CONFIG_PATH = Path("config/dataset_sources.json")
EXCLUSIONS_PATH = Path("data/catalog_exclusions.json")
SCHEMA_PATH = Path("sql/schema.sql")

CLASSES = ("cardboard", "glass", "metal", "paper", "plastic", "trash")
IMAGE_SUFFIXES = {".jpg", ".jpeg", ".png"}


def sha256_file(path: Path) -> str:
    """Calcule l'empreinte SHA-256 du contenu d'une image."""
    digest = hashlib.sha256()

    with path.open("rb") as file:
        for chunk in iter(lambda: file.read(1024 * 1024), b""):
            digest.update(chunk)

    return digest.hexdigest()


def load_exclusions() -> set[tuple[str, str]]:
    """Charge les exclusions qualité validées pour chaque source."""
    payload = json.loads(EXCLUSIONS_PATH.read_text(encoding="utf-8"))

    return {
        (
            str(item["source_id"]),
            str(item["path"]).replace("\\", "/"),
        )
        for item in payload["files"]
    }


def resolve_class_root(source: dict) -> Path:
    """Trouve le dossier qui contient directement les six catégories."""
    root = Path(source["local_directory"])

    if source.get("source_subdirectory_used"):
        root = root / source["source_subdirectory_used"]

    candidates = [root]

    if root.is_dir():
        candidates.extend(path for path in root.iterdir() if path.is_dir())

    for candidate in candidates:
        if all((candidate / class_name).is_dir() for class_name in CLASSES):
            return candidate

    raise FileNotFoundError(
        f"Classes introuvables pour {source['id']} sous : {root}"
    )


def get_source_ids(connection: sqlite3.Connection) -> dict[str, int]:
    """Retourne les identifiants SQLite des sources référencées."""
    rows = connection.execute(
        "SELECT id, code FROM sources_donnees"
    ).fetchall()

    return {str(code): int(identifier) for identifier, code in rows}


def update_statistics(
    connection: sqlite3.Connection,
    imported_at: str,
) -> dict[str, int]:
    """Recalcule les statistiques à partir des images uniques."""
    counts = {
        category: connection.execute(
            "SELECT COUNT(*) FROM dechets WHERE categorie = ?",
            (category,),
        ).fetchone()[0]
        for category in CLASSES
    }

    total = sum(counts.values())

    for category, count in counts.items():
        percentage = round((count * 100 / total), 2) if total else 0.0

        connection.execute(
            """
            INSERT INTO statistiques_categories
                (categorie, nombre_images, pourcentage, derniere_mise_a_jour)
            VALUES (?, ?, ?, ?)
            ON CONFLICT(categorie) DO UPDATE SET
                nombre_images = excluded.nombre_images,
                pourcentage = excluded.pourcentage,
                derniere_mise_a_jour = excluded.derniere_mise_a_jour
            """,
            (category, count, percentage, imported_at),
        )

    return counts


def import_catalog(
    database_path: Path,
    report_path: Path,
    replace_output: bool = False,
) -> dict:
    """Crée une base catalogue multi-source depuis les données brutes."""
    if database_path.exists():
        if not replace_output:
            raise FileExistsError(
                f"La base existe déjà : {database_path}. "
                "Choisis un nouveau nom ou utilise --replace-output."
            )
        database_path.unlink()

    configuration = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
    exclusions = load_exclusions()
    imported_at = datetime.now(timezone.utc).isoformat()

    database_path.parent.mkdir(parents=True, exist_ok=True)

    connection = sqlite3.connect(database_path)

    try:
        connection.execute("PRAGMA foreign_keys = ON")
        connection.executescript(SCHEMA_PATH.read_text(encoding="utf-8"))

        source_ids = get_source_ids(connection)
        sources_report: list[dict] = []

        total_candidates = 0
        canonical_images_added = 0
        provenance_links_added = 0
        duplicate_occurrences = 0

        for source in configuration["sources"]:
            source_code = source["id"]
            role = source["role"]

            if role == "external_evaluation_only":
                sources_report.append(
                    {
                        "id": source_code,
                        "role": role,
                        "imported_to_training_catalog": False,
                        "reason": "Jeu réservé à l'évaluation externe.",
                    }
                )
                continue

            if source_code not in source_ids:
                raise RuntimeError(
                    f"Source absente du schéma SQL : {source_code}"
                )

            source_id = source_ids[source_code]
            source_name = str(source["name"])
            class_root = resolve_class_root(source)

            source_report = {
                "id": source_code,
                "role": role,
                "class_root": str(class_root),
                "discovered": 0,
                "excluded_by_quality_rules": 0,
                "candidates": 0,
                "canonical_images_added": 0,
                "duplicate_occurrences": 0,
                "provenance_links_added": 0,
            }

            for category in CLASSES:
                files = sorted(
                    path
                    for path in (class_root / category).iterdir()
                    if path.is_file()
                    and path.suffix.lower() in IMAGE_SUFFIXES
                )

                source_report["discovered"] += len(files)

                for path in files:
                    relative_path = f"{category}/{path.name}"

                    if (source_code, relative_path) in exclusions:
                        source_report["excluded_by_quality_rules"] += 1
                        continue

                    total_candidates += 1
                    source_report["candidates"] += 1

                    digest = sha256_file(path)

                    existing = connection.execute(
                        """
                        SELECT id, categorie
                        FROM dechets
                        WHERE contenu_sha256 = ?
                        """,
                        (digest,),
                    ).fetchone()

                    if existing is None:
                        cursor = connection.execute(
                            """
                            INSERT INTO dechets
                                (
                                    contenu_sha256,
                                    nom_fichier,
                                    categorie,
                                    chemin_image,
                                    source_id,
                                    source,
                                    date_ajout
                                )
                            VALUES (?, ?, ?, ?, ?, ?, ?)
                            """,
                            (
                                digest,
                                path.name,
                                category,
                                str(path),
                                source_id,
                                source_name,
                                imported_at,
                            ),
                        )
                        dechet_id = int(cursor.lastrowid)

                        canonical_images_added += 1
                        source_report["canonical_images_added"] += 1
                    else:
                        dechet_id = int(existing[0])
                        canonical_category = str(existing[1])

                        if canonical_category != category:
                            raise ValueError(
                                "Conflit d'étiquette non exclu : "
                                f"{path} ({category}) contre "
                                f"{canonical_category}."
                            )

                        duplicate_occurrences += 1
                        source_report["duplicate_occurrences"] += 1

                    cursor = connection.execute(
                        """
                        INSERT OR IGNORE INTO dechet_sources
                            (
                                dechet_id,
                                source_id,
                                chemin_source,
                                nom_fichier_source,
                                categorie_source,
                                date_import
                            )
                        VALUES (?, ?, ?, ?, ?, ?)
                        """,
                        (
                            dechet_id,
                            source_id,
                            str(path),
                            path.name,
                            category,
                            imported_at,
                        ),
                    )

                    if cursor.rowcount == 1:
                        provenance_links_added += 1
                        source_report["provenance_links_added"] += 1

            sources_report.append(source_report)

        statistics = update_statistics(connection, imported_at)

        canonical_images = connection.execute(
            "SELECT COUNT(*) FROM dechets"
        ).fetchone()[0]

        provenance_links = connection.execute(
            "SELECT COUNT(*) FROM dechet_sources"
        ).fetchone()[0]

        foreign_key_errors = connection.execute(
            "PRAGMA foreign_key_check"
        ).fetchall()

        if foreign_key_errors:
            raise RuntimeError(
                f"Erreurs de clés étrangères : {foreign_key_errors}"
            )

        connection.commit()

    finally:
        connection.close()

    report = {
        "import": "c4_multisource_catalog",
        "generated_at": imported_at,
        "database": str(database_path),
        "sources": sources_report,
        "total_candidates": total_candidates,
        "canonical_images": canonical_images,
        "provenance_links": provenance_links,
        "duplicate_occurrences": duplicate_occurrences,
        "statistics_by_category": statistics,
        "foreign_key_errors": 0,
        "status": "ok",
    }

    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(
        json.dumps(report, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    return report


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Import multi-source dédoublonné du catalogue ECO-TRI."
    )
    parser.add_argument(
        "--database",
        type=Path,
        default=Path("data/eco_tri.db"),
        help="Chemin de la base SQLite à créer.",
    )
    parser.add_argument(
        "--report",
        type=Path,
        default=Path("reports/c4_multisource_import.json"),
        help="Chemin du rapport JSON généré.",
    )
    parser.add_argument(
        "--replace-output",
        action="store_true",
        help="Supprime uniquement la base cible si elle existe déjà.",
    )
    args = parser.parse_args()

    result = import_catalog(
        database_path=args.database,
        report_path=args.report,
        replace_output=args.replace_output,
    )

    print("Import multi-source C4 terminé.")
    print(f"Images candidates : {result['total_candidates']}")
    print(f"Images canoniques : {result['canonical_images']}")
    print(f"Liens de provenance : {result['provenance_links']}")
    print(f"Doublons non dupliqués : {result['duplicate_occurrences']}")
    print(f"Erreurs de clé étrangère : {result['foreign_key_errors']}")
    print(f"Rapport créé : {args.report}")


if __name__ == "__main__":
    main()