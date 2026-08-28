"""
Script de collecte des données - ECO-TRI
Compétence C1 : Collecte de données réelles depuis une source externe
Dataset : Garbage Classification (Kaggle - cchangcs)
URL : https://www.kaggle.com/datasets/asdasdasasdas/garbage-classification
"""

import os
import json
from pathlib import Path
from datetime import datetime

# ─── Chemins ───────────────────────────────────────────────────────────────
RAW_DATA_PATH = Path("data/raw/Garbage classification/Garbage classification")
OUTPUT_PATH   = Path("data/processed")

# ─── Catégories de déchets (6 classes) ─────────────────────────────────────
CATEGORIES = ["cardboard", "glass", "metal", "paper", "plastic", "trash"]

TRADUCTION = {
    "cardboard": "Carton",
    "glass":     "Verre",
    "metal":     "Métal",
    "paper":     "Papier",
    "plastic":   "Plastique",
    "trash":     "Ordures",
}


def collecter_statistiques() -> dict:
    """
    Parcourt le dataset Kaggle et collecte :
    - le nombre d'images par catégorie
    - quelques exemples de noms de fichiers
    - la date de collecte
    Sauvegarde le résultat dans data/processed/statistiques_dataset.json
    """
    stats = {
        "source":        "Kaggle – Garbage Classification par cchangcs",
        "url":           "https://www.kaggle.com/datasets/asdasdasasdas/garbage-classification",
        "date_collecte": datetime.now().isoformat(),
        "categories":    {},
        "total_images":  0,
    }

    print("🚀 ECO-TRI — Collecte des données réelles")
    print("=" * 55)

    total = 0
    for cat in CATEGORIES:
        dossier = RAW_DATA_PATH / cat
        if not dossier.exists():
            print(f"  ❌ Dossier introuvable : {cat}")
            continue

        fichiers = sorted(dossier.glob("*.jpg"))
        nb = len(fichiers)
        stats["categories"][cat] = {
            "nom_francais":   TRADUCTION[cat],
            "nombre_images":  nb,
            "exemples":       [f.name for f in fichiers[:3]],
        }
        total += nb
        print(f"  ✅ {TRADUCTION[cat]:12s} ({cat:10s}) : {nb:4d} images")

    stats["total_images"] = total
    print(f"\n  📊 TOTAL : {total} images réelles")

    # ── Sauvegarde JSON ───────────────────────────────────────────────────
    OUTPUT_PATH.mkdir(parents=True, exist_ok=True)
    sortie = OUTPUT_PATH / "statistiques_dataset.json"
    with open(sortie, "w", encoding="utf-8") as f:
        json.dump(stats, f, indent=2, ensure_ascii=False)

    print(f"\n  💾 Statistiques sauvegardées → {sortie}")
    return stats


if __name__ == "__main__":
    stats = collecter_statistiques()
    print("\n✅ Collecte terminée avec succès !")