"""Évalue le modèle ECO-TRI sur un jeu externe jamais utilisé à l'entraînement."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

from ultralytics import YOLO


CLASSES = ("cardboard", "glass", "metal", "paper", "plastic", "trash")
IMAGE_SUFFIXES = {".jpg", ".jpeg", ".png"}


def safe_divide(numerator: int, denominator: int) -> float:
    return numerator / denominator if denominator else 0.0


def compute_report(records: list[dict[str, object]], threshold: float) -> dict:
    """Calcule les métriques sans dépendre du moteur d'inférence."""
    matrix = {truth: {pred: 0 for pred in CLASSES} for truth in CLASSES}
    for record in records:
        matrix[str(record["expected_class"])][str(record["predicted_class"])] += 1

    per_class: dict[str, dict[str, float | int]] = {}
    total_correct = 0
    for class_name in CLASSES:
        true_positive = matrix[class_name][class_name]
        total_correct += true_positive
        actual = sum(matrix[class_name].values())
        predicted = sum(matrix[truth][class_name] for truth in CLASSES)
        precision = safe_divide(true_positive, predicted)
        recall = safe_divide(true_positive, actual)
        f1 = safe_divide(2 * precision * recall, precision + recall)
        per_class[class_name] = {
            "support": actual,
            "precision": round(precision, 4),
            "recall": round(recall, 4),
            "f1": round(f1, 4),
        }

    uncertain_count = sum(
        float(record["confidence"]) < threshold for record in records
    )
    error_count = len(records) - total_correct
    return {
        "test_images": len(records),
        "accuracy": round(safe_divide(total_correct, len(records)), 4),
        "macro_f1": round(
            sum(float(values["f1"]) for values in per_class.values())
            / len(CLASSES),
            4,
        ),
        "confidence_threshold": threshold,
        "uncertain_predictions": uncertain_count,
        "uncertain_rate": round(safe_divide(uncertain_count, len(records)), 4),
        "error_count": error_count,
        "per_class": per_class,
        "confusion_matrix": matrix,
    }


def collect_images(test_dir: Path) -> tuple[list[str], list[str]]:
    paths: list[str] = []
    expected: list[str] = []
    for class_name in CLASSES:
        class_dir = test_dir / class_name
        if not class_dir.is_dir():
            raise FileNotFoundError(f"Dossier de classe absent : {class_dir}")
        class_paths = sorted(
            path
            for path in class_dir.iterdir()
            if path.is_file() and path.suffix.lower() in IMAGE_SUFFIXES
        )
        if len(class_paths) < 5:
            raise ValueError(
                f"{class_name}: {len(class_paths)} image(s), au moins 5 requises"
            )
        paths.extend(str(path) for path in class_paths)
        expected.extend([class_name] * len(class_paths))
    return paths, expected


def write_reports(
    output_dir: Path,
    report: dict,
    records: list[dict[str, object]],
) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "metrics.json").write_text(
        json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8"
    )

    fieldnames = [
        "image_path",
        "origin",
        "expected_class",
        "predicted_class",
        "confidence",
        "is_uncertain",
        "is_correct",
    ]
    with (output_dir / "predictions.csv").open(
        "w", newline="", encoding="utf-8"
    ) as stream:
        writer = csv.DictWriter(stream, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(records)

    matrix = report["confusion_matrix"]
    with (output_dir / "confusion_matrix.csv").open(
        "w", newline="", encoding="utf-8"
    ) as stream:
        writer = csv.writer(stream)
        writer.writerow(["actual/predicted", *CLASSES])
        for truth in CLASSES:
            writer.writerow([truth, *(matrix[truth][pred] for pred in CLASSES)])

    errors = [record for record in records if not record["is_correct"]]
    with (output_dir / "errors.csv").open(
        "w", newline="", encoding="utf-8"
    ) as stream:
        writer = csv.DictWriter(stream, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(errors)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", type=Path, default=Path("backend/models/best.pt"))
    parser.add_argument(
        "--test-dir", type=Path, default=Path("data/external_test")
    )
    parser.add_argument(
        "--output-dir", type=Path, default=Path("reports/external")
    )
    parser.add_argument("--threshold", type=float, default=0.60)
    parser.add_argument(
        "--origin",
        required=True,
        help="Origine documentée des images, par ex. 'photos personnelles'",
    )
    args = parser.parse_args()

    paths, expected = collect_images(args.test_dir)
    model = YOLO(str(args.model))
    predictions = model.predict(paths, imgsz=224, batch=32, verbose=False)

    records: list[dict[str, object]] = []
    for path, truth, result in zip(paths, expected, predictions, strict=True):
        predicted = str(result.names[int(result.probs.top1)])
        confidence = round(float(result.probs.top1conf), 4)
        records.append(
            {
                "image_path": str(Path(path).relative_to(args.test_dir)),
                "origin": args.origin,
                "expected_class": truth,
                "predicted_class": predicted,
                "confidence": confidence,
                "is_uncertain": confidence < args.threshold,
                "is_correct": predicted == truth,
            }
        )

    report = compute_report(records, args.threshold)
    report["model"] = args.model.name
    report["dataset_origin"] = args.origin
    write_reports(args.output_dir, report, records)
    print(json.dumps(report, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
