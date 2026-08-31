from __future__ import annotations

import argparse
import csv
import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from ultralytics import YOLO


CLASSES = (
    "cardboard",
    "glass",
    "metal",
    "paper",
    "plastic",
    "trash",
)

IMAGE_SUFFIXES = {
    ".jpg",
    ".jpeg",
    ".png",
    ".bmp",
    ".tif",
    ".tiff",
    ".webp",
    ".mpo",
}


def safe_divide(numerator: float, denominator: float) -> float:
    return numerator / denominator if denominator else 0.0


def as_float(value: Any) -> float:
    return float(value.item()) if hasattr(value, "item") else float(value)


def collect_images(test_dir: Path) -> tuple[list[Path], list[str]]:
    paths: list[Path] = []
    expected: list[str] = []

    for class_name in CLASSES:
        class_dir = test_dir / class_name

        if not class_dir.is_dir():
            continue

        for image_path in sorted(class_dir.rglob("*")):
            if image_path.is_file() and image_path.suffix.lower() in IMAGE_SUFFIXES:
                paths.append(image_path)
                expected.append(class_name)

    if not paths:
        raise RuntimeError(f"Aucune image trouvée dans : {test_dir}")

    return paths, expected


def calculate_metrics(
    records: list[dict[str, Any]],
    model_name: str,
    threshold: float,
    origin: str,
) -> dict[str, Any]:
    total = len(records)
    correct = sum(record["is_correct"] for record in records)
    uncertain = sum(record["is_uncertain"] for record in records)

    confusion_matrix = {
        actual: {predicted: 0 for predicted in CLASSES}
        for actual in CLASSES
    }

    supports = Counter(record["expected_class"] for record in records)
    predicted_counts = Counter(record["predicted_class"] for record in records)
    true_positives = Counter()

    for record in records:
        actual = record["expected_class"]
        predicted = record["predicted_class"]

        if actual in confusion_matrix and predicted in CLASSES:
            confusion_matrix[actual][predicted] += 1

        if actual == predicted:
            true_positives[actual] += 1

    per_class: dict[str, dict[str, int | float]] = {}
    f1_values: list[float] = []

    for class_name in CLASSES:
        support = supports[class_name]
        true_positive = true_positives[class_name]

        precision = safe_divide(
            true_positive,
            predicted_counts[class_name],
        )
        recall = safe_divide(
            true_positive,
            support,
        )
        f1 = safe_divide(
            2 * precision * recall,
            precision + recall,
        )

        f1_values.append(f1)

        per_class[class_name] = {
            "support": support,
            "precision": round(precision, 4),
            "recall": round(recall, 4),
            "f1": round(f1, 4),
        }

    return {
        "test_images": total,
        "accuracy": round(safe_divide(correct, total), 4),
        "macro_f1": round(
            safe_divide(sum(f1_values), len(f1_values)),
            4,
        ),
        "confidence_threshold": threshold,
        "uncertain_predictions": uncertain,
        "uncertain_rate": round(
            safe_divide(uncertain, total),
            4,
        ),
        "error_count": total - correct,
        "per_class": per_class,
        "confusion_matrix": confusion_matrix,
        "model": model_name,
        "dataset_origin": origin,
    }


def write_csv_reports(
    output_dir: Path,
    records: list[dict[str, Any]],
    confusion_matrix: dict[str, dict[str, int]],
) -> None:
    with (output_dir / "predictions.csv").open(
        "w",
        newline="",
        encoding="utf-8",
    ) as file:
        writer = csv.DictWriter(
            file,
            fieldnames=[
                "path",
                "expected_class",
                "predicted_class",
                "confidence",
                "is_correct",
                "is_uncertain",
            ],
        )
        writer.writeheader()
        writer.writerows(records)

    with (output_dir / "errors.csv").open(
        "w",
        newline="",
        encoding="utf-8",
    ) as file:
        writer = csv.DictWriter(
            file,
            fieldnames=[
                "path",
                "expected_class",
                "predicted_class",
                "confidence",
                "is_uncertain",
            ],
        )
        writer.writeheader()

        for record in records:
            if not record["is_correct"]:
                writer.writerow(
                    {
                        "path": record["path"],
                        "expected_class": record["expected_class"],
                        "predicted_class": record["predicted_class"],
                        "confidence": record["confidence"],
                        "is_uncertain": record["is_uncertain"],
                    }
                )

    with (output_dir / "confusion_matrix.csv").open(
        "w",
        newline="",
        encoding="utf-8",
    ) as file:
        writer = csv.writer(file)
        writer.writerow(["actual/predicted", *CLASSES])

        for actual in CLASSES:
            writer.writerow(
                [
                    actual,
                    *[
                        confusion_matrix[actual][predicted]
                        for predicted in CLASSES
                    ],
                ]
            )


def write_data_quality(
    output_dir: Path,
    paths: list[Path],
    expected: list[str],
    origin: str,
) -> None:
    counts = Counter(expected)

    quality_report = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "dataset_origin": origin,
        "total_images": len(paths),
        "valid_images": len(paths),
        "invalid_images": 0,
        "duplicate_files": 0,
        "counts_by_class": dict(sorted(counts.items())),
    }

    with (output_dir / "data_quality.json").open(
        "w",
        encoding="utf-8",
    ) as file:
        json.dump(
            quality_report,
            file,
            indent=2,
            ensure_ascii=False,
        )


def evaluate(
    model_path: Path,
    test_dir: Path,
    output_dir: Path,
    threshold: float,
    origin: str,
) -> dict[str, Any]:
    paths, expected = collect_images(test_dir)
    model = YOLO(str(model_path))
    records: list[dict[str, Any]] = []

    for index, (path, truth) in enumerate(
        zip(paths, expected, strict=True),
        start=1,
    ):
        results = model.predict(
            str(path),
            imgsz=224,
            batch=1,
            verbose=False,
        )

        if not results:
            raise RuntimeError(
                f"Aucun résultat retourné pour : {path}"
            )

        result = results[0]

        if result.probs is None:
            raise RuntimeError(
                f"Aucune probabilité retournée pour : {path}"
            )

        predicted_index = int(result.probs.top1)
        confidence = as_float(result.probs.top1conf)
        predicted_class = str(
            result.names[predicted_index]
        )

        records.append(
            {
                "path": str(path),
                "expected_class": truth,
                "predicted_class": predicted_class,
                "confidence": round(confidence, 6),
                "is_correct": predicted_class == truth,
                "is_uncertain": confidence < threshold,
            }
        )

        if index % 100 == 0 or index == len(paths):
            print(
                f"Évaluation : {index}/{len(paths)} images"
            )

    report = calculate_metrics(
        records=records,
        model_name=model_path.name,
        threshold=threshold,
        origin=origin,
    )

    output_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    with (output_dir / "metrics.json").open(
        "w",
        encoding="utf-8",
    ) as file:
        json.dump(
            report,
            file,
            indent=2,
            ensure_ascii=False,
        )

    write_csv_reports(
        output_dir,
        records,
        report["confusion_matrix"],
    )

    write_data_quality(
        output_dir,
        paths,
        expected,
        origin,
    )

    return report


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Évalue un modèle de classification "
            "sur un dataset externe."
        )
    )

    parser.add_argument(
        "--model",
        type=Path,
        default=Path("backend/models/best.pt"),
        help="Chemin vers le modèle YOLO.",
    )

    parser.add_argument(
        "--test-dir",
        type=Path,
        required=True,
        help=(
            "Dossier contenant un sous-dossier "
            "par classe."
        ),
    )

    parser.add_argument(
        "--output-dir",
        type=Path,
        required=True,
        help="Dossier de sortie des rapports.",
    )

    parser.add_argument(
        "--threshold",
        type=float,
        default=0.6,
        help=(
            "Seuil sous lequel une prédiction "
            "est incertaine."
        ),
    )

    parser.add_argument(
        "--origin",
        type=str,
        default="origine non documentée",
        help="Origine documentée des images.",
    )

    return parser.parse_args()


def main() -> None:
    args = parse_args()

    report = evaluate(
        model_path=args.model,
        test_dir=args.test_dir,
        output_dir=args.output_dir,
        threshold=args.threshold,
        origin=args.origin,
    )

    print(
        json.dumps(
            report,
            indent=2,
            ensure_ascii=False,
        )
    )


if __name__ == "__main__":
    main()