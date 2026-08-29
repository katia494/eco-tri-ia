"""Télécharge automatiquement le dataset public utilisé par ECO-TRI."""

from __future__ import annotations

import argparse
import logging
import shutil
from pathlib import Path

DATASET_HANDLE = "asdasdasasdas/garbage-classification"


def download(destination: Path) -> Path:
    """Télécharge le dataset Kaggle public et le copie dans data/raw."""
    target = destination / "Garbage classification"
    if target.exists():
        logging.info("Le dossier cible existe déjà : %s", target)
        return target

    import kagglehub

    logging.info("Téléchargement du dataset Kaggle %s", DATASET_HANDLE)
    cached_path = Path(kagglehub.dataset_download(DATASET_HANDLE))
    if not cached_path.is_dir():
        raise RuntimeError(f"Kaggle n'a retourné aucun dossier valide : {cached_path}")

    destination.mkdir(parents=True, exist_ok=True)
    shutil.copytree(cached_path, target)
    logging.info("Dataset copié dans %s", target)
    return target


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--destination", type=Path, default=Path("data/raw"))
    args = parser.parse_args()
    logging.basicConfig(level=logging.INFO, format="%(levelname)s | %(message)s")
    print(download(args.destination))


if __name__ == "__main__":
    main()
