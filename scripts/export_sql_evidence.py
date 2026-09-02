"""Exécute des requêtes C2 et exporte leurs résultats en CSV."""

from __future__ import annotations

import argparse
import csv
import sqlite3
from pathlib import Path


QUERIES = {
    "distribution_categories": """
        SELECT categorie, COUNT(*) AS nombre_images,
               ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (), 2) AS pourcentage
        FROM dechets
        GROUP BY categorie
        ORDER BY nombre_images DESC
    """,
    "statistiques_globales": """
        SELECT COUNT(*) AS total_images,
               COUNT(DISTINCT categorie) AS nombre_categories,
               MIN(date_ajout) AS premiere_entree,
               MAX(date_ajout) AS derniere_entree
        FROM dechets
    """,
    "categories_sous_representees": """
        SELECT categorie, COUNT(*) AS nombre
        FROM dechets
        GROUP BY categorie
        HAVING COUNT(*) < 200
        ORDER BY nombre ASC
    """,
    "predictions_par_classe": """
        SELECT waste_class, COUNT(*) AS nombre_predictions,
               ROUND(AVG(confidence) * 100, 2) AS confiance_moyenne_pct
        FROM predictions
        GROUP BY waste_class
        ORDER BY nombre_predictions DESC
    """,
}


def export_query(
    connection: sqlite3.Connection, query: str, destination: Path
) -> int:
    cursor = connection.execute(query)
    rows = cursor.fetchall()
    destination.parent.mkdir(parents=True, exist_ok=True)
    with destination.open("w", newline="", encoding="utf-8") as csv_file:
        writer = csv.writer(csv_file, lineterminator="\n")
        writer.writerow(column[0] for column in cursor.description)
        writer.writerows(rows)
    return len(rows)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--database", type=Path, default=Path("data/eco_tri.db"))
    parser.add_argument("--output", type=Path, default=Path("reports/sql"))
    args = parser.parse_args()

    if not args.database.exists():
        raise FileNotFoundError(
            f"Base absente : {args.database}. Lancez d'abord python src/import_data.py"
        )

    with sqlite3.connect(args.database) as connection:
        for name, query in QUERIES.items():
            destination = args.output / f"{name}.csv"
            row_count = export_query(connection, query, destination)
            print(f"[OK] {name}: {row_count} ligne(s) -> {destination}")


if __name__ == "__main__":
    main()
