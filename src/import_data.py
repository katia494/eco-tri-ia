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
    cur = conn.cursor()
    cur.executescript("""
        CREATE TABLE IF NOT EXISTS dechets (
            id           INTEGER PRIMARY KEY AUTOINCREMENT,
            nom_fichier  TEXT NOT NULL,
            categorie    TEXT NOT NULL,
            chemin_image TEXT,
            source       TEXT DEFAULT 'Kaggle-GarbageClassification',
            date_ajout   TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS predictions (
            id                INTEGER PRIMARY KEY AUTOINCREMENT,
            image_path        TEXT,
            categorie_predite TEXT NOT NULL,
            confiance         REAL,
            date_prediction   TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS statistiques_categories (
            id                   INTEGER PRIMARY KEY AUTOINCREMENT,
            categorie            TEXT UNIQUE NOT NULL,
            nombre_images        INTEGER DEFAULT 0,
            pourcentage          REAL,
            derniere_mise_a_jour TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)
    conn.commit()
    print("  ✅ Tables créées (ou déjà existantes)")


def importer_images(conn: sqlite3.Connection) -> int:
    cur = conn.cursor()
    total = 0

    print("\n  📂 Import des images par catégorie :")
    for cat in CATEGORIES:
        dossier = RAW_DATA_PATH / cat
        if not dossier.exists():
            print(f"    ⚠️  Dossier manquant : {cat}")
            continue

        fichiers = list(dossier.glob("*.jpg"))
        nb = len(fichiers)

        cur.executemany(
            "INSERT OR IGNORE INTO dechets (nom_fichier, categorie, chemin_image) VALUES (?, ?, ?)",
            [(f.name, cat, str(f)) for f in fichiers],
        )

        cur.execute(
            "INSERT OR REPLACE INTO statistiques_categories (categorie, nombre_images, derniere_mise_a_jour) VALUES (?, ?, ?)",
            (cat, nb, datetime.now()),
        )

        total += nb
        print(f"    ✅ {TRADUCTION[cat]:12s} : {nb:4d} images")

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
