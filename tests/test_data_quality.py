from pathlib import Path

from PIL import Image

from scripts.audit_dataset import audit_dataset, file_sha256, inspect_image


def save_image(path: Path, color: tuple[int, int, int]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    Image.new("RGB", (16, 12), color).save(path, format="JPEG")


def test_inspect_image_detects_valid_and_invalid_files(tmp_path):
    valid_path = tmp_path / "valid.jpg"
    invalid_path = tmp_path / "invalid.jpg"
    save_image(valid_path, (0, 128, 0))
    invalid_path.write_bytes(b"not-an-image")

    assert inspect_image(valid_path)["valid"] is True
    assert inspect_image(invalid_path)["valid"] is False


def test_sha256_detects_identical_content(tmp_path):
    first = tmp_path / "first.jpg"
    second = tmp_path / "second.jpg"
    save_image(first, (255, 0, 0))
    second.write_bytes(first.read_bytes())

    assert file_sha256(first) == file_sha256(second)


def test_audit_reports_counts_corruption_and_duplicates(tmp_path):
    for index, class_name in enumerate(
        ("cardboard", "glass", "metal", "paper", "plastic", "trash")
    ):
        save_image(
            tmp_path / class_name / f"{class_name}.jpg",
            (index * 40, 255 - index * 30, index * 20),
        )

    duplicate = tmp_path / "glass" / "duplicate.jpg"
    duplicate.write_bytes((tmp_path / "cardboard" / "cardboard.jpg").read_bytes())
    (tmp_path / "metal" / "broken.jpg").write_bytes(b"broken")

    report = audit_dataset(tmp_path)

    assert report["total_discovered"] == 8
    assert report["valid_images"] == 7
    assert report["invalid_images"] == 1
    assert report["duplicate_files"] == 1
    assert report["usable_images"] == 6
