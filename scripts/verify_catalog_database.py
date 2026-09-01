"""Contrôle reproductible de l'intégrité du catalogue SQLite C4."""

from __future__ import annotations

import argparse
import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path

PREFLIGHT_PATH = Path("reports/c4_multisource_preflight.json")


def scalar(connection: sqlite3.Connection, query: str) -> int:
    """Retourne une valeur entière issue d'une requête SQL."""
    return int(connection.execute(query).fetchone()[0])


def verify_database(database_path: Path, report_path: Path) -> dict:
    """Vérifie les volumes, métadonnées et relations du catalogue C4."""
    if not database_path.exists():
        raise FileNotFoundError(f"Base introuvable : {database_path}")

    if not PREFLIGHT_PATH.exists():
        raise FileNotFoundError(
            f"Rapport de pré-inventaire introuvable : {PREFLIGHT_PATH}"
        )

    expected = json.loads(PREFLIGHT_PATH.read_text(encoding="utf-8"))

    connection = sqlite3.connect(database_path)

    try:
        connection.execute("PRAGMA foreign_keys = ON")

        canonical_images = scalar(
            connection,
            "SELECT COUNT(*) FROM dechets",
        )

        provenance_links = scalar(
            connection,
            "SELECT COUNT(*) FROM dechet_sources",
        )

        sources_count = scalar(
            connection,
            "SELECT COUNT(*) FROM sources_donnees",
        )

        orphan_links = scalar(
            connection,
            """
            SELECT COUNT(*)
            FROM dechet_sources AS ds
            LEFT JOIN dechets AS d ON d.id = ds.dechet_id
            LEFT JOIN sources_donnees AS s ON s.id = ds.source_id
            WHERE d.id IS NULL OR s.id IS NULL
            """,
        )

        missing_sha256 = scalar(
            connection,
            """
            SELECT COUNT(*)
            FROM dechets
            WHERE contenu_sha256 IS NULL
               OR length(contenu_sha256) <> 64
            """,
        )

        missing_source = scalar(
            connection,
            """
            SELECT COUNT(*)
            FROM dechets
            WHERE source_id IS NULL
               OR source IS NULL
               OR TRIM(source) = ''
            """,
        )

        missing_date = scalar(
            connection,
            """
            SELECT COUNT(*)
            FROM dechets
            WHERE date_ajout IS NULL
               OR TRIM(date_ajout) = ''
            """,
        )

        source_links = {
            code: int(count)
            for code, count in connection.execute(
                """
                SELECT s.code, COUNT(ds.dechet_id)
                FROM sources_donnees AS s
                LEFT JOIN dechet_sources AS ds ON ds.source_id = s.id
                GROUP BY s.code
                ORDER BY s.code
                """
            ).fetchall()
        }

        category_counts = {
            category: int(count)
            for category, count in connection.execute(
                """
                SELECT categorie, COUNT(*)
                FROM dechets
                GROUP BY categorie
                ORDER BY categorie
                """
            ).fetchall()
        }

        foreign_key_errors = connection.execute(
            "PRAGMA foreign_key_check"
        ).fetchall()

    finally:
        connection.close()

    expected_links = {
        str(source["id"]): int(source.get("candidates", 0))
        for source in expected["sources"]
    }

    checks = {
        "canonical_images_match_preflight": (
            canonical_images == int(expected["unique_images_by_sha256"])
        ),
        "provenance_links_match_candidates": (
            provenance_links == int(expected["total_candidates"])
        ),
        "source_links_match_preflight": source_links == expected_links,
        "three_sources_registered": sources_count == 3,
        "no_orphan_links": orphan_links == 0,
        "no_missing_sha256": missing_sha256 == 0,
        "no_missing_source": missing_source == 0,
        "no_missing_date": missing_date == 0,
        "no_foreign_key_error": len(foreign_key_errors) == 0,
    }

    report = {
        "check": "c4_catalog_database_integrity",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "database": str(database_path),
        "expected_from_preflight": {
            "candidates": int(expected["total_candidates"]),
            "unique_images": int(expected["unique_images_by_sha256"]),
        },
        "observed": {
            "canonical_images": canonical_images,
            "provenance_links": provenance_links,
            "sources_count": sources_count,
            "source_links": source_links,
            "category_counts": category_counts,
            "orphan_links": orphan_links,
            "missing_sha256": missing_sha256,
            "missing_source": missing_source,
            "missing_date": missing_date,
            "foreign_key_errors": len(foreign_key_errors),
        },
        "checks": checks,
        "status": "ok" if all(checks.values()) else "error",
    }

    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(
        json.dumps(report, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    if report["status"] != "ok":
        raise SystemExit("Échec des contrôles d'intégrité C4.")

    return report


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Vérifie l'intégrité de la base catalogue C4."
    )
    parser.add_argument(
        "--database",
        type=Path,
        default=Path("data/eco_tri.db"),
        help="Base SQLite à contrôler.",
    )
    parser.add_argument(
        "--report",
        type=Path,
        default=Path("reports/c4_database_checks.json"),
        help="Rapport JSON généré.",
    )
    args = parser.parse_args()

    result = verify_database(args.database, args.report)

    print("Contrôles C4 réussis.")
    print(f"Images canoniques : {result['observed']['canonical_images']}")
    print(f"Liens de provenance : {result['observed']['provenance_links']}")
    print(f"Sources : {result['observed']['source_links']}")
    print(f"Rapport créé : {args.report}")


if __name__ == "__main__":
    main()