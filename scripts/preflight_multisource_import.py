"""Inventaire à blanc pour l'import multi-source C4.

Ne modifie pas SQLite ni les images.
Il calcule les empreintes SHA-256 afin de connaître exactement les
images uniques, doublons et conflits éventuels avant l'import final.
"""

from __future__ import annotations

import hashlib
import json
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path


CONFIG_PATH = Path("config/dataset_sources.json")
CATALOG_EXCLUSIONS_PATH = Path("data/catalog_exclusions.json")
REPORT_PATH = Path("reports/c4_multisource_preflight.json")

CLASSES = ("cardboard", "glass", "metal", "paper", "plastic", "trash")
IMAGE_SUFFIXES = {".jpg", ".jpeg", ".png"}


def sha256_file(path: Path) -> str:
    """Calcule une empreinte sans charger le fichier entier en mémoire."""
    digest = hashlib.sha256()

    with path.open("rb") as file:
        for chunk in iter(lambda: file.read(1024 * 1024), b""):
            digest.update(chunk)

    return digest.hexdigest()


def load_catalog_exclusions() -> set[tuple[str, str]]:
    """Charge les exclusions validées pour chaque source."""
    payload = json.loads(
        CATALOG_EXCLUSIONS_PATH.read_text(encoding="utf-8")
    )

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


def run_preflight() -> dict:
    """Analyse V1 et V2 sans modifier les données."""
    configuration = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
    exclusions = load_catalog_exclusions()

    entries_by_hash: dict[str, list[dict[str, str]]] = defaultdict(list)
    sources_report: list[dict] = []

    for source in configuration["sources"]:
        source_id = source["id"]
        role = source["role"]

        # RealWaste reste volontairement hors catalogue d'entraînement.
        if role == "external_evaluation_only":
            sources_report.append(
                {
                    "id": source_id,
                    "role": role,
                    "imported_to_training_catalog": False,
                    "reason": "Jeu réservé à l'évaluation externe.",
                }
            )
            continue

        class_root = resolve_class_root(source)

        report = {
            "id": source_id,
            "role": role,
            "class_root": str(class_root),
            "imported_to_training_catalog": True,
            "discovered": 0,
            "excluded_by_quality_rules": 0,
            "candidates": 0,
            "by_class": {},
        }

        for class_name in CLASSES:
            files = sorted(
                path
                for path in (class_root / class_name).iterdir()
                if path.is_file() and path.suffix.lower() in IMAGE_SUFFIXES
            )

            report["discovered"] += len(files)
            kept_for_class = 0

            for path in files:
                relative_path = f"{class_name}/{path.name}"

                if (source_id, relative_path) in exclusions:
                    report["excluded_by_quality_rules"] += 1
                    continue

                entries_by_hash[sha256_file(path)].append(
                    {
                        "source_id": source_id,
                        "category": class_name,
                        "path": str(path),
                    }
                )
                kept_for_class += 1

            report["by_class"][class_name] = kept_for_class
            report["candidates"] += kept_for_class

        sources_report.append(report)

    duplicate_groups = [
        {"sha256": digest, "files": files}
        for digest, files in entries_by_hash.items()
        if len(files) > 1
    ]

    label_conflicts = [
        group
        for group in duplicate_groups
        if len({file["category"] for file in group["files"]}) > 1
    ]

    total_candidates = sum(
        source.get("candidates", 0)
        for source in sources_report
    )

    report = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "purpose": "Préparation de l'import multi-source C4",
        "sources": sources_report,
        "total_candidates": total_candidates,
        "unique_images_by_sha256": len(entries_by_hash),
        "duplicate_entries": total_candidates - len(entries_by_hash),
        "duplicate_groups": len(duplicate_groups),
        "label_conflict_groups": len(label_conflicts),
        "label_conflicts": label_conflicts,
        "status": "review_required" if label_conflicts else "ok",
    }

    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text(
        json.dumps(report, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    return report


if __name__ == "__main__":
    result = run_preflight()

    print("Pré-inventaire C4 terminé.")
    print(f"Images candidates : {result['total_candidates']}")
    print(f"Images uniques SHA-256 : {result['unique_images_by_sha256']}")
    print(f"Doublons exacts : {result['duplicate_entries']}")
    print(f"Groupes en conflit d'étiquette : {result['label_conflict_groups']}")
    print(f"Rapport créé : {REPORT_PATH}")