"""Collecte et vérification reproductible des sources ECO-TRI (C1)."""

from __future__ import annotations

import argparse
import json
import logging
import shutil
import sys
import tempfile
import urllib.request
import zipfile
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}


class SourceCollectionError(RuntimeError):
    """Erreur contrôlée lors de la récupération d'une source."""


def project_root() -> Path:
    """Retourne la racine du projet à partir du dossier scripts/."""
    return Path(__file__).resolve().parents[1]


def load_sources(config_path: Path) -> list[dict[str, Any]]:
    """Charge et valide le fichier de configuration des sources."""
    with config_path.open(encoding="utf-8") as file:
        config = json.load(file)

    sources = config.get("sources")

    if not isinstance(sources, list) or not sources:
        raise SourceCollectionError(
            "Le fichier de configuration ne contient aucune source."
        )

    return sources


def select_sources(
    sources: list[dict[str, Any]],
    source_id: str,
) -> list[dict[str, Any]]:
    """Sélectionne toutes les sources ou une source précise."""
    if source_id == "all":
        return sources

    for source in sources:
        if source.get("id") == source_id:
            return [source]

    available_sources = ", ".join(
        str(source.get("id"))
        for source in sources
    )

    raise SourceCollectionError(
        f"Source inconnue : {source_id}. "
        f"Sources possibles : {available_sources}."
    )


def get_local_directory(root: Path, source: dict[str, Any]) -> Path:
    """Retourne le dossier brut attendu pour une source."""
    return root / str(source["local_directory"])


def get_data_directory(root: Path, source: dict[str, Any]) -> Path:
    """
    Retourne le sous-dossier réellement utilisé.

    Garbage Classification V2 utilise uniquement original/ afin de ne pas
    mélanger les mêmes images avec les versions standardized_256 et
    standardized_384.
    """
    local_directory = get_local_directory(root, source)
    subdirectory = source.get("source_subdirectory_used")

    if subdirectory:
        candidate = local_directory / str(subdirectory)

        if candidate.exists():
            return candidate

    return local_directory


def find_images(directory: Path) -> list[Path]:
    """Trouve toutes les images compatibles dans un dossier."""
    if not directory.exists():
        return []

    return sorted(
        path
        for path in directory.rglob("*")
        if path.is_file() and path.suffix.lower() in IMAGE_EXTENSIONS
    )


def count_images_by_parent_directory(
    image_paths: list[Path],
) -> dict[str, int]:
    """Compte les images selon le nom de leur dossier parent."""
    counts = Counter(path.parent.name for path in image_paths)

    return dict(
        sorted(
            counts.items(),
            key=lambda item: item[0].lower(),
        )
    )


def inspect_source(root: Path, source: dict[str, Any]) -> dict[str, Any]:
    """Inspecte une source locale sans modifier les fichiers."""
    local_directory = get_local_directory(root, source)
    data_directory = get_data_directory(root, source)
    image_paths = find_images(data_directory)

    expected_count = source.get(
        "expected_image_count",
        source.get("expected_image_count_for_project"),
    )

    status = "ok" if image_paths else "missing"

    return {
        "id": source["id"],
        "name": source["name"],
        "provider": source["provider"],
        "url": source["url"],
        "role": source["role"],
        "local_directory": str(local_directory),
        "data_directory_used": str(data_directory),
        "exists": local_directory.exists(),
        "status": status,
        "raw_image_count_found": len(image_paths),
        "expected_image_count_for_project": expected_count,
        "class_counts_found": count_images_by_parent_directory(
            image_paths
        ),
        "contains_personal_data": source["contains_personal_data"],
        "license_note": source["license_note"],
    }


def safe_extract(archive_path: Path, destination: Path) -> None:
    """Extrait une archive ZIP sans autoriser de fichier hors destination."""
    destination = destination.resolve()

    with zipfile.ZipFile(archive_path) as archive:
        for member in archive.infolist():
            member_path = (destination / member.filename).resolve()

            if (
                member_path != destination
                and destination not in member_path.parents
            ):
                raise SourceCollectionError(
                    "Archive refusée : chemin dangereux détecté "
                    f"({member.filename})."
                )

        archive.extractall(destination)


def download_kaggle_source(
    source: dict[str, Any],
    destination: Path,
) -> None:
    """Télécharge une source Kaggle via kagglehub."""
    try:
        import kagglehub
    except ImportError as error:
        raise SourceCollectionError(
            "kagglehub est requis. Lance : "
            "pip install -r requirements-data.txt"
        ) from error

    handle = str(source["dataset_handle"])

    logging.info("Téléchargement Kaggle : %s", handle)

    cached_path = Path(kagglehub.dataset_download(handle))

    if not cached_path.is_dir():
        raise SourceCollectionError(
            f"Kaggle n'a retourné aucun dossier valide pour {handle}."
        )

    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(cached_path, destination)

    logging.info("Source copiée dans : %s", destination)


def download_github_archive(
    source: dict[str, Any],
    destination: Path,
) -> None:
    """Télécharge et extrait l'archive GitHub officielle de RealWaste."""
    archive_url = (
        f"{str(source['url']).rstrip('/')}/archive/refs/heads/main.zip"
    )

    logging.info("Téléchargement GitHub : %s", archive_url)

    destination.mkdir(parents=True, exist_ok=True)

    with tempfile.TemporaryDirectory() as temporary_directory:
        archive_path = Path(temporary_directory) / "source.zip"

        try:
            urllib.request.urlretrieve(archive_url, archive_path)
        except OSError as error:
            raise SourceCollectionError(
                f"Impossible de télécharger : {archive_url}"
            ) from error

        safe_extract(archive_path, destination)

    logging.info("Archive extraite dans : %s", destination)


def download_if_missing(root: Path, source: dict[str, Any]) -> None:
    """
    Télécharge seulement une source absente.

    Cette fonction ne remplace jamais un dossier déjà présent.
    """
    destination = get_local_directory(root, source)

    if destination.exists():
        logging.info(
            "Déjà présent, aucun téléchargement : %s",
            destination,
        )
        return

    method = source["download_method"]

    if method == "kagglehub":
        download_kaggle_source(source, destination)
        return

    if method == "github_archive":
        download_github_archive(source, destination)
        return

    raise SourceCollectionError(
        f"Méthode de téléchargement inconnue : {method}."
    )


def write_manifest(
    report_path: Path,
    inspected_sources: list[dict[str, Any]],
) -> None:
    """Écrit le manifeste de traçabilité utilisé comme preuve C1."""
    report_path.parent.mkdir(parents=True, exist_ok=True)

    manifest = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "project": "ECO-TRI IA",
        "purpose": (
            "Traçabilité de la collecte multi-source. "
            "RealWaste est réservé à l'évaluation externe."
        ),
        "sources": inspected_sources,
    }

    with report_path.open("w", encoding="utf-8") as file:
        json.dump(
            manifest,
            file,
            indent=2,
            ensure_ascii=False,
        )

    logging.info("Manifeste créé : %s", report_path)


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Vérifie ou récupère les sources de données ECO-TRI."
        )
    )

    parser.add_argument(
        "--source",
        default="all",
        help="ID d'une source ou 'all' (valeur par défaut).",
    )

    parser.add_argument(
        "--download-missing",
        action="store_true",
        help=(
            "Télécharge uniquement les sources absentes. "
            "Ne remplace jamais les dossiers existants."
        ),
    )

    parser.add_argument(
        "--config",
        type=Path,
        default=Path("config/dataset_sources.json"),
        help="Chemin du registre de sources.",
    )

    parser.add_argument(
        "--report",
        type=Path,
        default=Path("reports/data_collection_manifest.json"),
        help="Chemin du manifeste généré.",
    )

    args = parser.parse_args()

    logging.basicConfig(
        level=logging.INFO,
        format="%(levelname)s | %(message)s",
    )

    root = project_root()
    config_path = root / args.config
    report_path = root / args.report

    try:
        sources = load_sources(config_path)
        selected_sources = select_sources(sources, args.source)

        if args.download_missing:
            for source in selected_sources:
                download_if_missing(root, source)

        inspected_sources = [
            inspect_source(root, source)
            for source in selected_sources
        ]

        for source in inspected_sources:
            logging.info(
                "%s | statut=%s | images=%s | dossier=%s",
                source["name"],
                source["status"],
                source["raw_image_count_found"],
                source["data_directory_used"],
            )

        write_manifest(report_path, inspected_sources)

        missing_sources = [
            source["name"]
            for source in inspected_sources
            if source["status"] != "ok"
        ]

        if missing_sources:
            raise SourceCollectionError(
                "Source(s) absente(s) ou vide(s) : "
                + ", ".join(missing_sources)
            )

    except (
        OSError,
        ValueError,
        json.JSONDecodeError,
        SourceCollectionError,
    ) as error:
        logging.error("%s", error)
        sys.exit(1)


if __name__ == "__main__":
    main()