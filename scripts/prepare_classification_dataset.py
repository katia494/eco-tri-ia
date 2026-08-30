"""Prépare un split reproductible train/val/test pour YOLO classification."""

from __future__ import annotations

import argparse
import json
import random
import shutil
from pathlib import Path


CLASSES = ("cardboard", "glass", "metal", "paper", "plastic", "trash")
IMAGE_SUFFIXES = {".jpg", ".jpeg", ".png"}


def load_exclusions(path: Path | None) -> set[str]:
    """Charge les chemins relatifs exclus après l'audit qualité."""
    if path is None or not path.exists():
        return set()
    payload = json.loads(path.read_text(encoding="utf-8"))
    return {str(item["path"]).replace("\\", "/") for item in payload["files"]}


def split_items(items: list[Path], seed: int) -> dict[str, list[Path]]:
    """Découpe une classe en 70 % train, 15 % val et 15 % test."""
    shuffled = items.copy()
    random.Random(seed).shuffle(shuffled)
    train_end = int(len(shuffled) * 0.70)
    val_end = train_end + int(len(shuffled) * 0.15)
    return {
        "train": shuffled[:train_end],
        "val": shuffled[train_end:val_end],
        "test": shuffled[val_end:],
    }


def prepare(
    source: Path,
    destination: Path,
    seed: int = 42,
    exclusions_path: Path | None = Path("data/quality_exclusions.json"),
) -> dict:
    """Crée les dossiers attendus par Ultralytics sans modifier les sources."""
    if not source.is_dir():
        raise FileNotFoundError(f"Dataset source introuvable : {source}")

    exclusions = load_exclusions(exclusions_path)
    manifest: dict[str, object] = {
        "seed": seed,
        "ratios": {"train": 0.70, "val": 0.15, "test": 0.15},
        "excluded_files": sorted(exclusions),
        "classes": {},
    }

    for class_index, class_name in enumerate(CLASSES):
        class_dir = source / class_name
        images = sorted(
            path
            for path in class_dir.iterdir()
            if path.is_file() and path.suffix.lower() in IMAGE_SUFFIXES
            and f"{class_name}/{path.name}" not in exclusions
        )
        if not images:
            raise ValueError(f"Aucune image trouvée pour la classe {class_name}")

        splits = split_items(images, seed + class_index)
        manifest["classes"][class_name] = {
            split_name: len(split_images)
            for split_name, split_images in splits.items()
        }

        for split_name, split_images in splits.items():
            output_dir = destination / split_name / class_name
            output_dir.mkdir(parents=True, exist_ok=True)
            for image in split_images:
                target = output_dir / image.name
                if not target.exists():
                    shutil.copy2(image, target)

    destination.mkdir(parents=True, exist_ok=True)
    (destination / "manifest.json").write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    return manifest


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--source",
        type=Path,
        default=Path("data/raw/Garbage classification/Garbage classification"),
    )
    parser.add_argument(
        "--destination", type=Path, default=Path("data/classification")
    )
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument(
        "--exclusions",
        type=Path,
        default=Path("data/quality_exclusions.json"),
    )
    args = parser.parse_args()
    manifest = prepare(
        args.source,
        args.destination,
        args.seed,
        exclusions_path=args.exclusions,
    )
    print(json.dumps(manifest, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
