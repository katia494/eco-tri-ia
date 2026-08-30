"""Audite réellement la qualité du dataset d'images ECO-TRI."""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

from PIL import Image, UnidentifiedImageError


CLASSES = ("cardboard", "glass", "metal", "paper", "plastic", "trash")
IMAGE_SUFFIXES = {".jpg", ".jpeg", ".png"}


def file_sha256(path: Path) -> str:
    """Calcule l'empreinte du contenu sans charger tout le fichier en mémoire."""
    digest = hashlib.sha256()
    with path.open("rb") as image_file:
        for chunk in iter(lambda: image_file.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def inspect_image(path: Path) -> dict[str, object]:
    """Ouvre et vérifie une image avec Pillow puis retourne ses propriétés."""
    try:
        with Image.open(path) as image:
            image.verify()
        with Image.open(path) as image:
            width, height = image.size
            return {
                "valid": True,
                "format": image.format or "unknown",
                "mode": image.mode,
                "width": width,
                "height": height,
            }
    except (OSError, ValueError, UnidentifiedImageError) as exc:
        return {"valid": False, "error": str(exc)}


def audit_dataset(source: Path) -> dict[str, object]:
    """Contrôle formats, corruption, dimensions et doublons exacts."""
    if not source.is_dir():
        raise FileNotFoundError(f"Dataset introuvable : {source}")

    counts: Counter[str] = Counter()
    formats: Counter[str] = Counter()
    modes: Counter[str] = Counter()
    invalid_files: list[dict[str, str]] = []
    unexpected_files: list[str] = []
    hashes: dict[str, list[str]] = defaultdict(list)
    dimensions: list[tuple[int, int]] = []

    for class_name in CLASSES:
        class_dir = source / class_name
        if not class_dir.is_dir():
            invalid_files.append(
                {"path": str(class_dir), "error": "dossier de classe absent"}
            )
            continue

        for path in sorted(class_dir.iterdir()):
            if not path.is_file():
                continue
            if path.suffix.lower() not in IMAGE_SUFFIXES:
                unexpected_files.append(str(path))
                continue

            counts[class_name] += 1
            inspection = inspect_image(path)
            if not inspection["valid"]:
                invalid_files.append(
                    {"path": str(path), "error": str(inspection["error"])}
                )
                continue

            formats[str(inspection["format"])] += 1
            modes[str(inspection["mode"])] += 1
            dimensions.append(
                (int(inspection["width"]), int(inspection["height"]))
            )
            hashes[file_sha256(path)].append(str(path))

    duplicate_groups = [paths for paths in hashes.values() if len(paths) > 1]
    total_discovered = sum(counts.values())
    valid_images = total_discovered - len(invalid_files)
    duplicate_files = sum(len(group) - 1 for group in duplicate_groups)

    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "source": str(source),
        "classes_expected": list(CLASSES),
        "counts_by_class": dict(counts),
        "total_discovered": total_discovered,
        "valid_images": valid_images,
        "invalid_images": len(invalid_files),
        "invalid_files": invalid_files,
        "unexpected_files": unexpected_files,
        "duplicate_files": duplicate_files,
        "duplicate_groups": duplicate_groups,
        "formats": dict(formats),
        "modes": dict(modes),
        "dimensions": {
            "min_width": min((width for width, _ in dimensions), default=0),
            "max_width": max((width for width, _ in dimensions), default=0),
            "min_height": min((height for _, height in dimensions), default=0),
            "max_height": max((height for _, height in dimensions), default=0),
        },
        "usable_images": valid_images - duplicate_files,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--source",
        type=Path,
        default=Path("data/raw/Garbage classification/Garbage classification"),
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("reports/data_quality.json"),
    )
    parser.add_argument("--fail-on-invalid", action="store_true")
    args = parser.parse_args()

    report = audit_dataset(args.source)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    print(json.dumps(report, indent=2, ensure_ascii=False))

    if args.fail_on_invalid and report["invalid_images"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
