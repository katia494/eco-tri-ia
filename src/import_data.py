"""
Script d'import des données dans SQLite – ECO-TRI
Compétence C4 : Intégration du dataset dans une base de données
Dataset : Garbage Classification (Kaggle – asdasdasasdas)
"""

import sqlite3
from pathlib import Path
from datetime import datetime

# ─── Chemins ───────────────────────────────────────────────────────────────
RAW_DATA_PATH = Path("data/raw/Garbage classification/Garbage classification")
DB_PATH       = Path("data/eco_tri.db")
CATEGORIES    = ["cardboard", "glass", "metal", "paper", "plastic", "trash"]

TRADUCTION = {
    "cardboard": "Carton",
    "glass":     "Verre",
    "metal":     "Métal",
    "paper":     "Papier",
    "plastic":   "Plastique",
    "trash":     "Ordures",
}


def creer_tables(conn: sqlite3.Connection) -> None:
    schema_path = Path("sql/schema.sql")
    if not schema_path.exists():
        raise FileNotFoundError(f"Schéma SQL introuvable : {schema_path}")
    conn.executescript(schema_path.read_text(encoding="utf-8"))
    conn.commit()
    print(f"  ✅ Schéma SQLite appliqué depuis {schema_path}")


def importer_images(conn: sqlite3.Connection) -> int:
    cur = conn.cursor()
    total = 0

    print("\n  📂 Import des images par catégorie :")
    for cat in CATEGORIES:
        dossier = RAW_DATA_PATH / cat
        if not dossier.exists():
            print(f"    ⚠️  Dossier manquant : {cat}")
            continue

        fichiers = sorted(dossier.glob("*.jpg"))
        nb = len(fichiers)

        cur.executemany(
            "INSERT OR IGNORE INTO dechets (nom_fichier, categorie, chemin_image) VALUES (?, ?, ?)",
            [(f.name, cat, str(f)) for f in fichiers],
        )

        total += nb
        print(f"    ✅ {TRADUCTION[cat]:12s} : {nb:4d} images")

    for cat in CATEGORIES:
        cur.execute(
            "SELECT COUNT(*) FROM dechets WHERE categorie = ?",
            (cat,),
        )
        count = cur.fetchone()[0]
        percentage = round(count * 100 / total, 2) if total else 0.0
        cur.execute(
            """
            INSERT INTO statistiques_categories
                (categorie, nombre_images, pourcentage, derniere_mise_a_jour)
            VALUES (?, ?, ?, ?)
            ON CONFLICT(categorie) DO UPDATE SET
                nombre_images = excluded.nombre_images,
                pourcentage = excluded.pourcentage,
                derniere_mise_a_jour = excluded.derniere_mise_a_jour
            """,
            (cat, count, percentage, datetime.now().isoformat()),
        )

    conn.commit()
    return total


def afficher_resume(conn: sqlite3.Connection) -> None:
    cur = conn.cursor()
    print("\n" + "=" * 55)
    print("📊 RÉSUMÉ DE LA BASE DE DONNÉES ECO-TRI")
    print("=" * 55)

    cur.execute("SELECT categorie, COUNT(*) AS n FROM dechets GROUP BY categorie ORDER BY n DESC")
    grand_total = 0
    for categorie, n in cur.fetchall():
        grand_total += n
        print(f"  {TRADUCTION.get(categorie, categorie):12s} ({categorie:10s}) : {n:4d} images")

    print(f"\n  TOTAL : {grand_total} images importées dans {DB_PATH}")


if __name__ == "__main__":
    print("🚀 ECO-TRI — Import des données dans SQLite")
    print("=" * 55)

    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    print(f"  🗄️  Base de données : {DB_PATH}")

    creer_tables(conn)
    total = importer_images(conn)
    afficher_resume(conn)

    conn.close()
    print("\n✅ Import terminé avec succès !")
