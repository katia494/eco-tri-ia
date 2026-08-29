"""Évalue le modèle final sur le jeu de test jamais vu."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

from ultralytics import YOLO


CLASSES = ("cardboard", "glass", "metal", "paper", "plastic", "trash")


def safe_divide(numerator: int, denominator: int) -> float:
    return numerator / denominator if denominator else 0.0


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", type=Path, default=Path("backend/models/best.pt"))
    parser.add_argument("--test-dir", type=Path, default=Path("data/classification/test"))
    parser.add_argument("--output-dir", type=Path, default=Path("reports/model"))
    args = parser.parse_args()

    model = YOLO(str(args.model))
    paths: list[str] = []
    expected: list[str] = []
    for class_name in CLASSES:
        for path in sorted((args.test_dir / class_name).glob("*")):
            if path.suffix.lower() in {".jpg", ".jpeg", ".png"}:
                paths.append(str(path))
                expected.append(class_name)

    matrix = {truth: {pred: 0 for pred in CLASSES} for truth in CLASSES}
    results = model.predict(paths, imgsz=224, batch=64, verbose=False)
    for truth, result in zip(expected, results, strict=True):
        predicted = str(result.names[int(result.probs.top1)])
        matrix[truth][predicted] += 1

    per_class = {}
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

    metrics = {
        "model": args.model.name,
        "test_images": len(expected),
        "accuracy": round(safe_divide(total_correct, len(expected)), 4),
        "macro_f1": round(
            sum(values["f1"] for values in per_class.values()) / len(CLASSES), 4
        ),
        "per_class": per_class,
    }

    args.output_dir.mkdir(parents=True, exist_ok=True)
    (args.output_dir / "metrics.json").write_text(
        json.dumps(metrics, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    with (args.output_dir / "confusion_matrix.csv").open(
        "w", newline="", encoding="utf-8"
    ) as stream:
        writer = csv.writer(stream)
        writer.writerow(["actual/predicted", *CLASSES])
        for truth in CLASSES:
            writer.writerow([truth, *(matrix[truth][pred] for pred in CLASSES)])

    print(json.dumps(metrics, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
