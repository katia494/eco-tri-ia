"""Entraîne le modèle final ECO-TRI avec YOLOv8n-cls."""

from __future__ import annotations

import argparse
from pathlib import Path

from ultralytics import YOLO


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", type=Path, default=Path("data/classification"))
    parser.add_argument("--epochs", type=int, default=30)
    parser.add_argument("--batch", type=int, default=32)
    parser.add_argument("--device", default="cpu")
    parser.add_argument("--workers", type=int, default=2)
    args = parser.parse_args()

    if not (args.data / "train").is_dir() or not (args.data / "val").is_dir():
        raise FileNotFoundError(
            "Dataset préparé absent. Lancez d'abord "
            "python scripts/prepare_classification_dataset.py"
        )

    model = YOLO("yolov8n-cls.pt")
    model.train(
        data=str(args.data.resolve()),
        epochs=args.epochs,
        imgsz=224,
        batch=args.batch,
        patience=7,
        seed=42,
        deterministic=True,
        device=args.device,
        workers=args.workers,
        project="runs/classify",
        name="eco_tri_yolov8n_cls",
    )


if __name__ == "__main__":
    main()
